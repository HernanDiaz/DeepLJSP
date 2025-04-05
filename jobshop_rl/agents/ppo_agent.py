"""
Implementación de agente PPO (Proximal Policy Optimization) para Job Shop Scheduling.
"""

import torch
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Categorical
import numpy as np
import time
import logging
from typing import List, Dict, Tuple, Optional, Any
from copy import deepcopy
import matplotlib.pyplot as plt

# Ensure the 'jobshop_rl' module is accessible. If it's a local module, add its directory to sys.path
import sys
sys.path.append('/path/to/jobshop_rl')
from jobshop_rl.agents.base_agent import Agent
from jobshop_rl.models.neural_models import PolicyNetwork, ValueNetwork
from jobshop_rl.environment.job_shop_env import JobShopEnv
from jobshop_rl.utils.logging import TrainingLogger

logger = logging.getLogger("JobShopRL.PPOAgent")

class PPOAgent(Agent):
    """Agente de Proximal Policy Optimization para Job Shop Scheduling"""

    def __init__(self, env: JobShopEnv, feature_dim: int = 7, hidden_dim: int = 128,
                 lr: float = 0.0003, gamma: float = 0.99, eps_clip: float = 0.2,
                 K_epochs: int = 4, entropy_coef: float = 0.01,
                 use_lr_decay: bool = True, use_grad_clip: bool = True,
                 advantage_normalization: bool = True, gae_lambda: float = 0.95,
                 csv_logger: Optional[TrainingLogger] = None,
                 seed: Optional[int] = None):
        self.env = env
        self.feature_dim = feature_dim
        self.hidden_dim = hidden_dim
        self.lr = lr
        self.gamma = gamma
        self.eps_clip = eps_clip
        self.K_epochs = K_epochs
        self.entropy_coef = entropy_coef
        self.use_lr_decay = use_lr_decay
        self.use_grad_clip = use_grad_clip
        self.advantage_normalization = advantage_normalization
        self.gae_lambda = gae_lambda
        self.csv_logger = csv_logger

        # Establecer semilla para reproducibilidad
        if seed is not None:
            torch.manual_seed(seed)
            np.random.seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed(seed)
                torch.cuda.manual_seed_all(seed)

        # Dimensión del estado para la red de valor
        self.state_dim = env.num_jobs + env.num_machines + 2

        # Inicializar redes
        self.policy = PolicyNetwork(feature_dim, hidden_dim)
        self.value = ValueNetwork(self.state_dim, hidden_dim)

        # Optimizadores
        self.optimizer_policy = optim.Adam(self.policy.parameters(), lr=lr)
        self.optimizer_value = optim.Adam(self.value.parameters(), lr=lr)

        # Tracking del rendimiento
        self.best_makespan = float('inf')
        self.best_schedule = None
        self.best_makespan_history = None
        self.training_makespan_history = []
        self.episode_rewards = []
        self.training_losses = {"policy": [], "value": []}
        self.epsilon_history = []  # Para tracking de la exploración
        self.total_episodes = 0
        
        # Tiempo de inicio para tracking de duración
        self.training_start_time = None

    def _state_to_value_input(self, state: Dict) -> torch.Tensor:
        """Convierte el estado a un tensor para la red de valor"""
        feature_vector = np.zeros(self.state_dim)
        feature_vector[:self.env.num_jobs] = state['job_status']
        feature_vector[self.env.num_jobs:self.env.num_jobs+self.env.num_machines] = state['machine_completion_time']
        feature_vector[-2] = max(state['machine_completion_time'])
        feature_vector[-1] = sum(state['machine_completion_time']) / self.env.num_machines
        return torch.FloatTensor(feature_vector)

    def select_action(self, state: Dict, training: bool = True) -> Tuple[Optional[int], Optional[torch.Tensor], Optional[torch.Tensor]]:
        """Selecciona una acción basada en el estado actual"""
        features = self.env.get_features(state)

        if len(features) == 0:
            return None, None, None

        features_tensor = torch.FloatTensor(features)

        with torch.no_grad():
            policy_logits = self.policy(features_tensor)

            if policy_logits is None:
                return None, None, None

            dist = Categorical(policy_logits)

            if training:
                action = dist.sample()
            else:
                action = torch.argmax(policy_logits)

            action_log_prob = dist.log_prob(action)

        return action.item(), action_log_prob, features_tensor

    def evaluate(self, features: torch.Tensor, action: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Evalúa la acción para calcular pérdidas PPO"""
        policy_logits = self.policy(features)
        dist = Categorical(policy_logits)

        action_log_probs = dist.log_prob(action)
        dist_entropy = dist.entropy()

        return action_log_probs, dist_entropy

    def calculate_gae(self, rewards, values, is_terminals, gamma, lam):
        """Calcula ventajas usando Generalized Advantage Estimation"""
        gae = 0
        returns = []
        advantages = []

        for i in reversed(range(len(rewards))):
            if i == len(rewards) - 1 or is_terminals[i]:
                # Si es terminal, no hay próximo estado
                next_value = 0
            else:
                next_value = values[i + 1]

            delta = rewards[i] + gamma * next_value * (1 - is_terminals[i]) - values[i]
            gae = delta + gamma * lam * (1 - is_terminals[i]) * gae

            returns.insert(0, gae + values[i])
            advantages.insert(0, gae)

        return returns, advantages

    def _recreate_best_solution(self) -> Tuple[float, List[Dict], List[float]]:
        """Recrea la mejor solución encontrada para obtener el makespan history"""
        state = self.env.reset()
        done = False

        while not done:
            action_idx, _, _ = self.select_action(state, training=False)

            if action_idx is None:
                break

            state, reward, done, info = self.env.step(action_idx)

        return self.env.makespan_history

    def train_episode(self) -> float:
        """Entrena un episodio completo y devuelve la recompensa total"""
        state = self.env.reset()
        done = False

        # Buffers para almacenar la experiencia
        states = []
        actions = []
        log_probs = []
        rewards = []
        features_list = []
        is_terminals = []
        values = []

        episode_reward = 0
        self.total_episodes += 1

        while not done:
            action_idx, action_log_prob, features = self.select_action(state, training=True)

            if action_idx is None:
                break

            # Calcular valor para GAE
            value_input = self._state_to_value_input(state)
            with torch.no_grad():
                value = self.value(value_input).item()

            next_state, reward, done, info = self.env.step(action_idx)

            states.append(state)
            actions.append(action_idx)
            log_probs.append(action_log_prob)
            rewards.append(reward)
            features_list.append(features)
            is_terminals.append(done)
            values.append(value)

            episode_reward += reward
            state = next_state

        if done and info['makespan'] is not None:
            makespan = info['makespan']
            self.training_makespan_history.append(makespan)

            if makespan < self.best_makespan:
                self.best_makespan = makespan
                self.best_schedule = deepcopy(self.env.schedule_history)
                self.best_makespan_history = deepcopy(self.env.makespan_history)
                logger.info(f"Nuevo mejor makespan: {makespan}")

        self.episode_rewards.append(episode_reward)
        self.epsilon_history.append(self.eps_clip)  # Tracking de epsilon

        # Actualizar el CSV logger si está configurado
        if self.csv_logger:
            # Calcular makespan promedio de los últimos 30 episodios (o menos si no hay suficientes)
            window_size = min(30, len(self.training_makespan_history))
            if window_size > 0:
                avg_makespan = sum(self.training_makespan_history[-window_size:]) / window_size
            else:
                avg_makespan = 0
                
            # Calcular tiempo transcurrido
            if self.training_start_time:
                training_time = time.time() - self.training_start_time
            else:
                training_time = 0
                
            current_makespan = self.training_makespan_history[-1] if self.training_makespan_history else 0
            self.csv_logger.log_step(
                episode=self.total_episodes,
                current_makespan=current_makespan,
                best_makespan=self.best_makespan,
                avg_makespan=avg_makespan,
                training_time=training_time
            )

        if len(states) == 0:
            return episode_reward

        # Calcular retornos y ventajas
        if self.gae_lambda > 0:
            returns, advantages = self.calculate_gae(
                rewards, values, is_terminals, self.gamma, self.gae_lambda
            )
            returns = torch.tensor(returns, dtype=torch.float32)
            advantages = torch.tensor(advantages, dtype=torch.float32)
        else:
            # Método tradicional de retornos descontados
            returns = []
            discounted_reward = 0
            for reward, is_terminal in zip(reversed(rewards), reversed(is_terminals)):
                if is_terminal:
                    discounted_reward = 0
                discounted_reward = reward + (self.gamma * discounted_reward)
                returns.insert(0, discounted_reward)

            returns = torch.tensor(returns, dtype=torch.float32)

            # Calcular ventajas como retornos - valores
            value_tensor = torch.tensor(values, dtype=torch.float32)
            advantages = returns - value_tensor

        # Normalizar ventajas si está habilitado
        if self.advantage_normalization and len(advantages) > 1:
            advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        old_actions = torch.tensor([a for a in actions], dtype=torch.int64)
        old_log_probs = torch.stack(log_probs)

        # Realizar actualizaciones de PPO
        policy_losses = []
        value_losses = []

        # Calcular un factor de decaimiento de learning rate si está activado
        if self.use_lr_decay:
            # Decaimiento lineal simple basado en episodios
            decay_factor = max(0.1, 1.0 - (self.total_episodes / 500))  # Mínimo 10% del lr original
            current_lr = self.lr * decay_factor

            # Actualizar lr en optimizadores
            for param_group in self.optimizer_policy.param_groups:
                param_group['lr'] = current_lr
            for param_group in self.optimizer_value.param_groups:
                param_group['lr'] = current_lr

        # Mini-batch updates for K epochs
        for _ in range(self.K_epochs):
            for i in range(len(states)):
                state_features = features_list[i]
                value_input = self._state_to_value_input(states[i])

                value = self.value(value_input)

                new_log_probs, dist_entropy = self.evaluate(state_features, torch.tensor(actions[i], dtype=torch.int64))

                ratio = torch.exp(new_log_probs - old_log_probs[i].detach())

                advantage = advantages[i]

                surr1 = ratio * advantage
                surr2 = torch.clamp(ratio, 1-self.eps_clip, 1+self.eps_clip) * advantage
                policy_loss = -torch.min(surr1, surr2) - self.entropy_coef * dist_entropy

                value_loss = F.mse_loss(value.squeeze(), returns[i])

                # Actualizar política
                self.optimizer_policy.zero_grad()
                policy_loss.backward()
                if self.use_grad_clip:
                    torch.nn.utils.clip_grad_norm_(self.policy.parameters(), 0.5)  # Clipping de gradientes
                self.optimizer_policy.step()

                # Actualizar valor
                self.optimizer_value.zero_grad()
                value_loss.backward()
                if self.use_grad_clip:
                    torch.nn.utils.clip_grad_norm_(self.value.parameters(), 0.5)  # Clipping de gradientes
                self.optimizer_value.step()

                policy_losses.append(policy_loss.item())
                value_losses.append(value_loss.item())

        # Registrar pérdidas medias
        self.training_losses["policy"].append(np.mean(policy_losses))
        self.training_losses["value"].append(np.mean(value_losses))

        return episode_reward

    def train(self, episodes: int = 500, lr_decay: bool = True,
              log_interval: int = 10, checkpoint_interval: int = 50,
              dynamic_entropy: bool = True, early_stopping: bool = False,
              early_stopping_patience: int = 50):
        """Entrena el agente por un número específico de episodios"""
        logger.info("Iniciando entrenamiento...")

        # Iniciar cronómetro para tracking de duración
        self.training_start_time = time.time()

        # Programación de la tasa de aprendizaje si está habilitada
        initial_lr = self.lr
        initial_eps_clip = self.eps_clip

        # Seguimiento para early stopping
        best_avg_reward = float('-inf')
        no_improvement_count = 0

        for i in range(1, episodes+1):
            # Ajustar la tasa de aprendizaje si está habilitado
            if lr_decay:
                new_lr = initial_lr * (1 - (i / episodes))
                for param_group in self.optimizer_policy.param_groups:
                    param_group['lr'] = new_lr
                for param_group in self.optimizer_value.param_groups:
                    param_group['lr'] = new_lr

            # Ajuste dinámico de epsilon para exploración
            if dynamic_entropy:
                # Gradualmente reducir epsilon para fomentar explotación
                self.eps_clip = initial_eps_clip * (1 - (i / episodes) * 0.7)  # Mínimo 30% del original

                # Ajuste dinámico del coeficiente de entropía
                progress = i / episodes
                self.entropy_coef = max(0.001, self.entropy_coef * (1 - progress * 0.9))  # Mínimo 10% del original

            # Entrenar un episodio
            episode_reward = self.train_episode()

            # Registrar métricas periódicamente
            if i % log_interval == 0:
                if self.training_makespan_history:
                    avg_makespan = sum(self.training_makespan_history[-log_interval:]) / min(log_interval, len(self.training_makespan_history[-log_interval:]))
                    avg_reward = sum(self.episode_rewards[-log_interval:]) / min(log_interval, len(self.episode_rewards[-log_interval:]))
                    training_time = time.time() - self.training_start_time
                    logger.info(f"Episodio {i}/{episodes}, Recompensa promedio: {avg_reward:.4f}, Makespan promedio: {avg_makespan:.2f}, Mejor: {self.best_makespan}, Tiempo: {training_time:.2f}s")

                    # Early stopping check
                    if early_stopping:
                        if avg_reward > best_avg_reward:
                            best_avg_reward = avg_reward
                            no_improvement_count = 0
                        else:
                            no_improvement_count += 1

                        if no_improvement_count >= early_stopping_patience:
                            logger.info(f"Early stopping activado después de {i} episodios sin mejora en la recompensa promedio")
                            break
                else:
                    logger.info(f"Episodio {i}/{episodes}, Sin makespan válido aún")

            # Guardar checkpoint si está habilitado
            if checkpoint_interval > 0 and i % checkpoint_interval == 0:
                self.save_checkpoint(f"checkpoint_ep{i}.pt")
        
        # Registrar el tiempo total de entrenamiento
        total_training_time = time.time() - self.training_start_time
        logger.info(f"Entrenamiento completado en {total_training_time:.2f} segundos")
        
        # Registrar el registro final en el CSV si está configurado
        if self.csv_logger:
            self.csv_logger.save()

    def save_checkpoint(self, path: str):
        """Guarda el modelo en un checkpoint"""
        checkpoint = {
            'policy_state_dict': self.policy.state_dict(),
            'value_state_dict': self.value.state_dict(),
            'optimizer_policy_state_dict': self.optimizer_policy.state_dict(),
            'optimizer_value_state_dict': self.optimizer_value.state_dict(),
            'best_makespan': self.best_makespan,
            'best_schedule': self.best_schedule,
            'best_makespan_history': self.best_makespan_history,
            'training_history': self.training_makespan_history,
            'episode_rewards': self.episode_rewards,
            'training_losses': self.training_losses
        }
        torch.save(checkpoint, path)
        logger.info(f"Checkpoint guardado en {path}")

    def load_checkpoint(self, path: str):
        """Carga un modelo desde un checkpoint"""
        checkpoint = torch.load(path)
        self.policy.load_state_dict(checkpoint['policy_state_dict'])
        self.value.load_state_dict(checkpoint['value_state_dict'])
        self.optimizer_policy.load_state_dict(checkpoint['optimizer_policy_state_dict'])
        self.optimizer_value.load_state_dict(checkpoint['optimizer_value_state_dict'])
        self.best_makespan = checkpoint['best_makespan']
        self.best_schedule = checkpoint['best_schedule']
        self.best_makespan_history = checkpoint.get('best_makespan_history')
        self.training_makespan_history = checkpoint['training_history']
        self.episode_rewards = checkpoint.get('episode_rewards', [])
        self.training_losses = checkpoint.get('training_losses', {"policy": [], "value": []})
        logger.info(f"Checkpoint cargado desde {path}")

    def evaluate_policy(self) -> Tuple[float, List[Dict], List[float]]:
        """Evalúa la política actual en un episodio completo"""
        state = self.env.reset()
        done = False

        while not done:
            action_idx, _, _ = self.select_action(state, training=False)

            if action_idx is None:
                break

            state, reward, done, info = self.env.step(action_idx)

        makespan = max(self.env.job_completion_time) if done else float('inf')
        return makespan, self.env.schedule_history, self.env.makespan_history

    def plot_training_history(self):
        """Visualiza la evolución del makespan durante el entrenamiento"""
        from jobshop_rl.utils.visualization import plot_makespan_history
        return plot_makespan_history(
            self.training_makespan_history,
            title='Evolución del Makespan durante el entrenamiento',
            optimal_makespan=930
        )

    def plot_reward_history(self):
        """Visualiza la evolución de las recompensas durante el entrenamiento"""
        from jobshop_rl.utils.visualization import plot_makespan_history
        return plot_makespan_history(
            self.episode_rewards,
            title='Evolución de la recompensa durante el entrenamiento',
            optimal_makespan=None
        )

    def plot_losses(self):
        """Visualiza la evolución de las pérdidas durante el entrenamiento"""
        if not self.training_losses["policy"] or not self.training_losses["value"]:
            return None

        # Crear una sola figura con dos subplots
        plt.figure(figsize=(12, 6))

        # Subplot para pérdida de política
        plt.subplot(1, 2, 1)
        plt.plot(self.training_losses["policy"])
        plt.xlabel('Episodios')
        plt.ylabel('Pérdida de política')
        plt.title('Evolución de la pérdida de política')
        plt.grid(True)

        # Subplot para pérdida de valor
        plt.subplot(1, 2, 2)
        plt.plot(self.training_losses["value"])
        plt.xlabel('Episodios')
        plt.ylabel('Pérdida de valor')
        plt.title('Evolución de la pérdida de valor')
        plt.grid(True)

        plt.tight_layout()
        return plt.gcf()

    def plot_exploration_history(self):
        """Visualiza la evolución del parámetro epsilon (exploración) durante el entrenamiento"""
        from jobshop_rl.utils.visualization import plot_makespan_history
        return plot_makespan_history(
            self.epsilon_history,
            title='Evolución del parámetro de exploración (epsilon)',
            optimal_makespan=None
        )
        
    def plot_best_solution_makespan(self):
        """Visualiza la evolución del makespan de la mejor solución encontrada"""
        from jobshop_rl.utils.visualization import plot_makespan_history
        
        if not self.best_makespan_history:
            return None
            
        return plot_makespan_history(
            self.best_makespan_history,
            title='Evolución del Makespan de la Mejor Solución',
            optimal_makespan=930
        )