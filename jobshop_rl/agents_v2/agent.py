"""
AgentV2: agente PPO con representación invariante al tamaño.

Expone la misma superficie que el agente v1 usa desde el pipeline de
experimentos (select_action, train, evaluate_policy, save_checkpoint,
.policy para transferencia de pesos, best_model_state, best_makespan,
training_makespan_history) sin importar nada de jobshop_rl.agents.
"""

import os
import time
from copy import deepcopy
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn

from jobshop_rl.agents_v2.networks import PolicyValueNetV2
from jobshop_rl.agents_v2.ppo_trainer import PPOTrainerV2, RolloutBuffer
from jobshop_rl.agents_v2.state_encoder import StateEncoder
from jobshop_rl.models.interval import Interval
from jobshop_rl.utils.seed_utils import set_random_seed


class AgentV2:

    def __init__(self, env, csv_logger=None, seed: Optional[int] = None,
                 lr: float = 3e-4, gamma: float = 1.0, gae_lambda: float = 0.95,
                 eps_clip: float = 0.2, K_epochs: int = 4,
                 minibatch_size: int = 256, update_every_episodes: int = 4,
                 entropy_coef: float = 0.01, greedy_eval_every: int = 10,
                 hidden_dim: int = 128, attention_layers: int = 0,
                 attention_heads: int = 4, **_ignored_v1_params):
        set_random_seed(seed)

        self.env = env
        self.csv_logger = csv_logger
        self.encoder = StateEncoder(env)

        self.network = PolicyValueNetV2(
            hidden=hidden_dim,
            num_attention_layers=attention_layers,
            attention_heads=attention_heads,
        )
        self.trainer = PPOTrainerV2(
            self.network, lr=lr, gamma=gamma, gae_lambda=gae_lambda,
            eps_clip=eps_clip, k_epochs=K_epochs,
            minibatch_size=minibatch_size, entropy_coef=entropy_coef,
        )
        self.buffer = RolloutBuffer()
        self.update_every_episodes = update_every_episodes
        self.greedy_eval_every = greedy_eval_every

        # Superficie de compatibilidad con el pipeline v1:
        # .policy es LA red (transferencia de pesos entre problemas);
        # .value es un módulo vacío (el valor vive dentro de la misma red)
        self.policy = self.network
        self.value = nn.Module()

        # Tracking (misma semántica que v1)
        self.best_makespan = float("inf")
        self.best_schedule = None
        self.best_makespan_history = None
        self.best_model_state = None
        self.training_makespan_history: List[float] = []
        self.episode_rewards: List[float] = []
        self.training_losses = {"policy": [], "value": []}
        self.epsilon_history: List[float] = []
        self.total_episodes = 0

    # ------------------------------------------------------------------
    # Traza de entrenamiento
    # ------------------------------------------------------------------

    def _log_episode(self, inicio: float, ventana: int = 30):
        """Una fila por episodio: actual, mejor y media movil del makespan.

        Los makespan del v2 son escalares de peor caso, asi que ambos
        limites del logger reciben el mismo valor.
        """
        actual = self.training_makespan_history[-1]
        recientes = self.training_makespan_history[-ventana:]
        media = sum(recientes) / len(recientes)
        mejor = self.best_makespan
        self.csv_logger.log_step(
            episode=self.total_episodes,
            current_makespan_lower=actual, current_makespan_upper=actual,
            best_makespan_lower=mejor, best_makespan_upper=mejor,
            avg_makespan_lower=media, avg_makespan_upper=media,
            training_time=time.time() - inicio,
        )

    # ------------------------------------------------------------------
    # Interacción con el entorno
    # ------------------------------------------------------------------

    def _forward_state(self, state: Dict):
        """Features + forward de la red para un único estado."""
        op_f, glob_f = self.encoder.encode(state)
        if op_f.shape[0] == 0:
            return None, None, None, None, None
        op_t = torch.from_numpy(op_f).unsqueeze(0)
        glob_t = torch.from_numpy(glob_f).unsqueeze(0)
        with torch.no_grad():
            logits, value = self.network(op_t, glob_t)
        return op_f, glob_f, logits.squeeze(0), float(value.item()), None

    def select_action(self, state: Dict, training: bool = True):
        """Compatible con la firma del v1: (action_idx, log_prob, features)."""
        op_f, glob_f, logits, value, _ = self._forward_state(state)
        if logits is None:
            return None, None, None
        dist = torch.distributions.Categorical(logits=logits)
        if training:
            action = dist.sample()
        else:
            action = torch.argmax(logits)
        return int(action.item()), dist.log_prob(action), (op_f, glob_f, value)

    def _episode_makespan(self) -> float:
        """Valor a minimizar del estado final.

        Por defecto el peor caso. Con DEEPLJSP_V2_LAMBDA>0 se anade la
        penalizacion de anchura del objetivo robusto, para que la
        seleccion del mejor modelo y el best-of-N ordenen por lo mismo
        que premia la recompensa: optimizar una cosa y elegir por otra
        seria un experimento incoherente.
        """
        max_time = max(self.env.job_completion_time)
        if not isinstance(max_time, Interval):
            return float(max_time)
        up, lo = float(max_time.upper), float(max_time.lower)
        lam = float(os.environ.get("DEEPLJSP_V2_LAMBDA", "0") or 0)
        return up + lam * (up - lo) if lam else up

    def _run_episode(self, sample: bool, store: bool) -> Tuple[float, float]:
        """Ejecuta un episodio; devuelve (makespan, recompensa acumulada)."""
        state = self.env.reset()
        done = False
        total_reward = 0.0

        while not done:
            action_idx, log_prob, aux = self.select_action(state, training=sample)
            if action_idx is None:
                break
            op_f, glob_f, value = aux
            state, reward, done, info = self.env.step(action_idx)
            total_reward += reward
            if store:
                self.buffer.store(op_f, glob_f, action_idx,
                                  float(log_prob.item()), value, reward, done)

        makespan = self._episode_makespan() if done else float("inf")
        return makespan, total_reward

    def _track_best(self, makespan: float):
        if makespan < self.best_makespan:
            self.best_makespan = makespan
            self.best_schedule = self.env.schedule_history
            self.best_makespan_history = self.env.makespan_history
            self.best_model_state = {
                "policy": deepcopy(self.network.state_dict()),
                "value": {},
            }

    # ------------------------------------------------------------------
    # Entrenamiento
    # ------------------------------------------------------------------

    def train(self, episodes: int = 100, **_ignored_v1_kwargs):
        """Entrena con muestreo estocástico y evaluación greedy periódica."""
        inicio = time.time()
        for ep in range(1, episodes + 1):
            makespan, total_reward = self._run_episode(sample=True, store=True)
            self.total_episodes += 1
            self.training_makespan_history.append(makespan)
            self.episode_rewards.append(total_reward)
            self._track_best(makespan)

            if ep % self.update_every_episodes == 0:
                losses = self.trainer.update(self.buffer)
                self.training_losses["policy"].append(losses["policy_loss"])
                self.training_losses["value"].append(losses["value_loss"])

            # Evaluación greedy periódica: selección de mejor modelo sin el
            # ruido del muestreo de entrenamiento
            if ep % self.greedy_eval_every == 0:
                greedy_mk, _ = self._run_episode(sample=False, store=False)
                self._track_best(greedy_mk)

            # Traza por episodio. El v1 la escribia y el v2 no, de modo que
            # los logs de las campañas quedaban con cabecera y sin filas: sin
            # ellos no hay curva de aprendizaje que dibujar.
            if self.csv_logger is not None:
                self._log_episode(inicio)

        # No dejar gradientes parciales pendientes
        if len(self.buffer) > 0:
            losses = self.trainer.update(self.buffer)
            self.training_losses["policy"].append(losses["policy_loss"])
            self.training_losses["value"].append(losses["value_loss"])

        # El logger vuelca a disco cada 10 filas y nadie lo cierra: sin este
        # flush se pierden los ultimos episodios cuando el total no es
        # multiplo de 10 (con 1000 no se notaba; con 25 se pierden 5).
        if self.csv_logger is not None:
            self.csv_logger.save()

        return self, {"best_makespan": self.best_makespan}

    # ------------------------------------------------------------------
    # Evaluación (misma semántica que v1, incluida idea-16: best-of-N)
    # ------------------------------------------------------------------

    def evaluate_policy(self, n_samples: int = 1):
        start_time = time.time()

        best_makespan = float("inf")
        best_schedule: List[Dict] = []
        best_history: List[float] = []

        for i in range(max(1, n_samples)):
            makespan, _ = self._run_episode(sample=(i > 0), store=False)
            if makespan < best_makespan or i == 0:
                best_makespan = makespan
                best_schedule = self.env.schedule_history
                best_history = self.env.makespan_history

        return best_makespan, best_schedule, best_history, time.time() - start_time

    def evaluate(self, *args, **kwargs):
        raise NotImplementedError(
            "AgentV2 no expone evaluate() por muestra; el update vive en PPOTrainerV2")

    # ------------------------------------------------------------------
    # Visualización (superficie que usa BatchExperimenter)
    # ------------------------------------------------------------------

    def plot_training_history(self, optimal_makespan=None):
        from jobshop_rl.utils.visualization import plot_makespan_history
        return plot_makespan_history(
            makespan_history=self.training_makespan_history,
            title="Evolución del Makespan durante el entrenamiento (agente v2)",
            optimal_makespan=optimal_makespan,
        )

    def plot_best_solution_makespan(self):
        from jobshop_rl.utils.visualization import plot_makespan_history
        return plot_makespan_history(
            makespan_history=self.best_makespan_history,
            title="Makespan de la mejor solución (agente v2)",
        )

    # ------------------------------------------------------------------
    # Persistencia
    # ------------------------------------------------------------------

    def save_checkpoint(self, path: str):
        torch.save({
            "network": self.network.state_dict(),
            "optimizer": self.trainer.optimizer.state_dict(),
            "best_makespan": self.best_makespan,
            "total_episodes": self.total_episodes,
            "agent_version": "v2",
        }, path)
        return path

    def load_checkpoint(self, path: str):
        checkpoint = torch.load(path, map_location="cpu")
        self.network.load_state_dict(checkpoint["network"])
        if "optimizer" in checkpoint:
            self.trainer.optimizer.load_state_dict(checkpoint["optimizer"])
        self.best_makespan = checkpoint.get("best_makespan", float("inf"))
        self.total_episodes = checkpoint.get("total_episodes", 0)
        return checkpoint
