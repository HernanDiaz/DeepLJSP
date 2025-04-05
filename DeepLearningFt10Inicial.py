import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Categorical
import matplotlib.pyplot as plt
import random
from copy import deepcopy
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Any, Optional, Union, Callable
from dataclasses import dataclass
import logging
import warnings

# Ignora advertencias de deprecación para una salida más limpia
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("JobShopRL")

# ===== MODELOS DE DATOS =====

@dataclass
class Operation:
    """Representa una operación dentro de un trabajo"""
    job_id: int
    op_idx: int
    machine: int
    duration: int
    start_time: Optional[int] = None
    end_time: Optional[int] = None

@dataclass
class SchedulingStep:
    """Representa un paso en la programación"""
    job: int
    operation: int
    machine: int
    start: int
    end: int

@dataclass
class StateFeatures:
    """Encapsula las características extraídas de un estado"""
    eligible_ops: List[int]
    job_status: List[int]
    job_completion_time: List[int]
    machine_completion_time: List[int]

@dataclass
class OperationFeatures:
    """Características de una operación para toma de decisiones"""
    job_id: int
    op_idx: int
    machine: int
    duration: int
    earliest_start: int
    remaining_time: int
    remaining_ops: int

    def to_array(self) -> List[float]:
        """Convierte las características a un array para la red neuronal"""
        return [
            float(self.job_id), float(self.op_idx), float(self.machine), float(self.duration),
            float(self.earliest_start), float(self.remaining_time), float(self.remaining_ops)
        ]

# ===== SISTEMA DE RECOMPENSAS =====

class RewardStrategy(ABC):
    """Estrategia base para el cálculo de recompensas (patrón Strategy)"""

    @abstractmethod
    def calculate_reward(self, env, state, next_state, action, done, info) -> float:
        """Calcula la recompensa basada en el estado, la acción y el resultado"""
        pass

class BasicRewardStrategy(RewardStrategy):
    """Estrategia de recompensa básica: solo recompensa al final basada en makespan"""

    def calculate_reward(self, env, state, next_state, action, done, info) -> float:
        if done:
            makespan = max(env.job_completion_time)
            optimal_makespan = 930  # Óptimo para FT10
            reward = -makespan / 100  # Escalar la recompensa

            # Bonus por acercarse al óptimo
            if makespan <= optimal_makespan:
                reward += 10
            return reward
        return 0

class AdvancedRewardStrategy(RewardStrategy):
    """Estrategia de recompensa avanzada con señales intermedias"""

    def __init__(self, makespan_weight=1.0, idle_weight=0.2, critical_weight=0.1, balance_weight=0.05,
                 progress_weight=0.2, local_improvement_weight=0.15):
        self.makespan_weight = makespan_weight
        self.idle_weight = idle_weight
        self.critical_weight = critical_weight
        self.balance_weight = balance_weight
        self.progress_weight = progress_weight
        self.local_improvement_weight = local_improvement_weight

        # Estado para seguimiento de mejora relativa
        self.last_projected_makespan = float('inf')
        self.best_seen_makespan = float('inf')

    def calculate_reward(self, env, state, next_state, action, done, info) -> float:
        reward = 0

        # Si la acción fue None o no hay operaciones elegibles
        if action is None or not state['eligible_ops']:
            return 0

        # Obtener información de la operación programada
        job_id = state['eligible_ops'][action]
        op_idx = state['job_status'][job_id]
        machine = env.sequences[job_id][op_idx]

        # Calcular tiempos
        start_time = max(state['job_completion_time'][job_id],
                         state['machine_completion_time'][machine])
        duration = env.durations[job_id][op_idx]
        end_time = start_time + duration

        # 1. Recompensa final basada en makespan
        if done:
            makespan = max(env.job_completion_time)
            optimal_makespan = 930  # Óptimo para FT10
            makespan_reward = -makespan / 100

            # Bonus por acercarse al óptimo
            if makespan <= optimal_makespan:
                makespan_reward += 10

            reward += self.makespan_weight * makespan_reward

            # Actualizar mejor makespan visto
            if makespan < self.best_seen_makespan:
                self.best_seen_makespan = makespan

        # 2. Penalización por tiempo de inactividad en máquinas
        idle_time = 0
        if start_time > state['machine_completion_time'][machine]:
            idle_time = start_time - state['machine_completion_time'][machine]
        idle_reward = -idle_time / 50  # Normalizado
        reward += self.idle_weight * idle_reward

        # 3. Recompensa por priorizar operaciones críticas
        remaining_ops = env.num_machines - op_idx - 1
        if remaining_ops > 0:
            remaining_time = sum(env.durations[job_id][op_idx+1:])
            criticality = remaining_time / 100  # Normalizado
            reward += self.critical_weight * criticality

        # 4. Penalización por desequilibrio de carga
        completion_times = [t for t in next_state['machine_completion_time'] if t > 0]
        if completion_times:
            std_dev = np.std(completion_times)
            balance_reward = -std_dev / 50
            reward += self.balance_weight * balance_reward

        # 5. Recompensa por progreso general
        if not done:
            # Calcular proporción de operaciones completadas
            total_ops = env.num_jobs * env.num_machines
            completed_ops = sum(state['job_status'])
            progress = completed_ops / total_ops

            # Recompensa pequeña por avanzar en el plan
            progress_reward = progress * 0.1
            reward += self.progress_weight * progress_reward

        # 6. Recompensa por mejora local (proyección de makespan)
        current_projected_makespan = max(next_state['machine_completion_time'])

        # Mejora relativa desde la última acción
        if self.last_projected_makespan != float('inf'):
            improvement = (self.last_projected_makespan - current_projected_makespan)
            # Normalizar y solo recompensar mejoras
            if improvement > 0:
                local_reward = improvement / 100
                reward += self.local_improvement_weight * local_reward

        self.last_projected_makespan = current_projected_makespan

        return reward

    def reset(self):
        """Reinicia el estado interno de la estrategia"""
        self.last_projected_makespan = float('inf')
        # No reiniciamos best_seen_makespan para mantener referencia entre episodios

# Fábrica de estrategias de recompensa
class CombinedRewardStrategy(RewardStrategy):
    """Estrategia de recompensa que combina múltiples estrategias con pesos"""

    def __init__(self, strategies_with_weights: List[Tuple[RewardStrategy, float]]):
        self.strategies_with_weights = strategies_with_weights

    def calculate_reward(self, env, state, next_state, action, done, info) -> float:
        total_reward = 0
        for strategy, weight in self.strategies_with_weights:
            reward = strategy.calculate_reward(env, state, next_state, action, done, info)
            total_reward += weight * reward
        return total_reward

class RewardStrategyFactory:
    """Fábrica para crear estrategias de recompensa (patrón Factory)"""

    @staticmethod
    def create_strategy(strategy_type: str, **kwargs) -> RewardStrategy:
        """Crea una estrategia de recompensa basada en el tipo especificado"""
        if strategy_type.lower() == "basic":
            return BasicRewardStrategy()
        elif strategy_type.lower() == "advanced":
            return AdvancedRewardStrategy(**kwargs)
        elif strategy_type.lower() == "combined":
            # Ejemplo: combined_params = {"strategies": [("basic", 0.3), ("advanced", 0.7, {advanced_params})]}
            strategies_with_weights = []

            for strat_config in kwargs.get("strategies", []):
                if len(strat_config) >= 2:
                    strat_name = strat_config[0]
                    strat_weight = strat_config[1]
                    strat_params = strat_config[2] if len(strat_config) > 2 else {}

                    strategy = RewardStrategyFactory.create_strategy(strat_name, **strat_params)
                    strategies_with_weights.append((strategy, strat_weight))

            return CombinedRewardStrategy(strategies_with_weights)
        else:
            raise ValueError(f"Estrategia de recompensa desconocida: {strategy_type}")

# ===== ENTORNO DE JOB SHOP SCHEDULING =====

class JobShopEnv:
    """Entorno para el problema de Job Shop Scheduling"""

    def __init__(self, num_jobs: int, num_machines: int,
                 sequences: List[List[int]], durations: List[List[int]],
                 reward_strategy: Optional[RewardStrategy] = None,
                 seed: Optional[int] = None):
        self.num_jobs = num_jobs
        self.num_machines = num_machines
        self.sequences = sequences
        self.durations = durations
        self.reward_strategy = reward_strategy or BasicRewardStrategy()

        # Establecer semilla para reproducibilidad
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
            torch.manual_seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed(seed)
                torch.cuda.manual_seed_all(seed)

        self.reset()

    def set_reward_strategy(self, strategy: RewardStrategy):
        """Cambia la estrategia de recompensa (patrón Strategy)"""
        self.reward_strategy = strategy

        # Si la estrategia tiene un método reset, llamarlo
        if hasattr(self.reward_strategy, 'reset') and callable(getattr(self.reward_strategy, 'reset')):
            self.reward_strategy.reset()

    def reset(self) -> Dict:
        """Reinicia el entorno a su estado inicial"""
        # Estado de cada trabajo: posición actual en su secuencia
        self.job_status = [0] * self.num_jobs

        # Tiempo de finalización para cada trabajo y máquina
        self.job_completion_time = [0] * self.num_jobs
        self.machine_completion_time = [0] * self.num_machines

        # Operaciones ya programadas
        self.scheduled_ops = []

        # Operaciones elegibles
        self.eligible_ops = self._get_eligible_ops()

        # Historia para visualización
        self.schedule_history = []
        self.makespan_history = []

        return self._get_state()

    def _get_eligible_ops(self) -> List[int]:
        """Determina qué operaciones son elegibles para programar en el estado actual"""
        eligible = []
        for job_id in range(self.num_jobs):
            if self.job_status[job_id] < self.num_machines:
                # Si es la primera operación o la anterior ya está programada
                if self.job_status[job_id] == 0 or (job_id, self.job_status[job_id] - 1) in self.scheduled_ops:
                    eligible.append(job_id)
        return eligible

    def _get_state(self) -> Dict:
        """Obtiene el estado actual del entorno"""
        state = {
            'eligible_ops': self.eligible_ops,
            'job_status': self.job_status.copy(),
            'job_completion_time': self.job_completion_time.copy(),
            'machine_completion_time': self.machine_completion_time.copy(),
        }
        return state

    def get_features(self, state: Dict) -> np.ndarray:
        """Extrae características para todas las operaciones elegibles"""
        features = []
        for job_id in state['eligible_ops']:
            op_idx = state['job_status'][job_id]
            machine = self.sequences[job_id][op_idx]
            duration = self.durations[job_id][op_idx]

            earliest_start = max(state['job_completion_time'][job_id],
                                state['machine_completion_time'][machine])

            # Tiempo restante para este trabajo
            remaining_ops = self.num_machines - op_idx - 1
            remaining_time = sum(self.durations[job_id][op_idx+1:]) if remaining_ops > 0 else 0

            # Crear objeto de características
            op_features = OperationFeatures(
                job_id=job_id,
                op_idx=op_idx,
                machine=machine,
                duration=duration,
                earliest_start=earliest_start,
                remaining_time=remaining_time,
                remaining_ops=remaining_ops
            )

            features.append(op_features.to_array())

        if not features:
            return np.zeros((0, 7))

        return np.array(features)

    def step(self, action_idx: int) -> Tuple[Dict, float, bool, Dict]:
        """Ejecuta un paso en el entorno basado en la acción seleccionada"""
        if len(self.eligible_ops) == 0:
            return self._get_state(), 0, True, {}

        # Guardar el estado actual para el cálculo de recompensa
        current_state = self._get_state()

        # Seleccionar un trabajo
        job_id = self.eligible_ops[action_idx]

        # Obtener operación
        op_idx = self.job_status[job_id]
        machine = self.sequences[job_id][op_idx]
        duration = self.durations[job_id][op_idx]

        # Calcular tiempos
        start_time = max(self.job_completion_time[job_id],
                         self.machine_completion_time[machine])
        end_time = start_time + duration

        # Actualizar estado
        self.job_completion_time[job_id] = end_time
        self.machine_completion_time[machine] = end_time
        self.scheduled_ops.append((job_id, op_idx))
        self.job_status[job_id] += 1
        self.eligible_ops = self._get_eligible_ops()

        # Guardar historial
        scheduling_step = SchedulingStep(
            job=job_id,
            operation=op_idx,
            machine=machine,
            start=start_time,
            end=end_time
        )
        self.schedule_history.append(vars(scheduling_step))

        # Actualizar makespan history
        current_makespan = max(self.job_completion_time)
        self.makespan_history.append(current_makespan)

        # Verificar si terminó
        done = all(status == self.num_machines for status in self.job_status)

        # Obtener nuevo estado
        next_state = self._get_state()

        # Información adicional
        info = {'makespan': max(self.job_completion_time) if done else None}

        # Calcular recompensa usando la estrategia actual
        reward = self.reward_strategy.calculate_reward(
            self, current_state, next_state, action_idx, done, info
        )

        return next_state, reward, done, info

    def render_schedule(self, title="Job Shop Schedule"):
        """Visualiza la programación actual"""
        if not self.schedule_history:
            return None

        plt.figure(figsize=(15, 8))
        colors = plt.cm.tab10(np.linspace(0, 1, self.num_jobs))

        for op in self.schedule_history:
            plt.barh(op['machine'],
                    op['end'] - op['start'],
                    left=op['start'],
                    color=colors[op['job']],
                    edgecolor='black',
                    alpha=0.8)

            plt.text(op['start'] + (op['end'] - op['start'])/2,
                    op['machine'],
                    f"J{op['job']},{op['operation']}",
                    va='center',
                    ha='center',
                    color='white',
                    fontweight='bold')

        plt.yticks(range(self.num_machines), [f'M{i}' for i in range(self.num_machines)])
        plt.xlabel('Tiempo')
        plt.ylabel('Máquina')
        plt.title(f"{title}\nMakespan: {max(max(op['end'] for op in self.schedule_history), 0)}")
        plt.grid(axis='x')

        return plt.gcf()

    def plot_makespan_history(self):
        """Visualiza la evolución del makespan durante un episodio"""
        plt.figure(figsize=(12, 6))
        plt.plot(self.makespan_history, '-o')
        plt.axhline(y=930, color='r', linestyle='--', label='Óptimo: 930')
        plt.xlabel('Pasos')
        plt.ylabel('Makespan')
        plt.title('Evolución del Makespan')
        plt.legend()
        plt.grid(True)

        return plt.gcf()

# ===== MODELOS DE REDES NEURONALES =====

class FeatureExtractor(nn.Module):
    """Extractor de características para las operaciones"""

    def __init__(self, input_dim: int, hidden_dim: int):
        super(FeatureExtractor, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return x

class PolicyNetwork(nn.Module):
    """Red neuronal para la política de selección de acciones"""

    def __init__(self, input_dim: int, hidden_dim: int):
        super(PolicyNetwork, self).__init__()
        self.feature_extractor = FeatureExtractor(input_dim, hidden_dim)
        self.output = nn.Linear(hidden_dim, 1)

    def forward(self, x: torch.Tensor) -> Optional[torch.Tensor]:
        if x.size(0) == 0:
            return None

        features = self.feature_extractor(x)
        logits = self.output(features).squeeze(-1)
        return F.softmax(logits, dim=0)

class ValueNetwork(nn.Module):
    """Red neuronal para la función de valor"""

    def __init__(self, state_dim: int, hidden_dim: int):
        super(ValueNetwork, self).__init__()
        self.fc1 = nn.Linear(state_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)

# ===== AGENTE PPO =====

class PPOAgent:
    """Agente de Proximal Policy Optimization para Job Shop Scheduling"""

    def __init__(self, env: JobShopEnv, feature_dim: int = 7, hidden_dim: int = 128,
                 lr: float = 0.0003, gamma: float = 0.99, eps_clip: float = 0.2,
                 K_epochs: int = 4, entropy_coef: float = 0.01,
                 use_lr_decay: bool = True, use_grad_clip: bool = True,
                 advantage_normalization: bool = True, gae_lambda: float = 0.95,
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

        # Establecer semilla para reproducibilidad
        if seed is not None:
            torch.manual_seed(seed)
            np.random.seed(seed)
            random.seed(seed)
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
        self.training_makespan_history = []
        self.episode_rewards = []
        self.training_losses = {"policy": [], "value": []}
        self.epsilon_history = []  # Para tracking de la exploración
        self.total_episodes = 0

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
                logger.info(f"Nuevo mejor makespan: {makespan}")

        self.episode_rewards.append(episode_reward)
        self.epsilon_history.append(self.eps_clip)  # Tracking de epsilon

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
                    logger.info(f"Episodio {i}/{episodes}, Recompensa promedio: {avg_reward:.4f}, Makespan promedio: {avg_makespan:.2f}, Mejor: {self.best_makespan}")

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

    def save_checkpoint(self, path: str):
        """Guarda el modelo en un checkpoint"""
        checkpoint = {
            'policy_state_dict': self.policy.state_dict(),
            'value_state_dict': self.value.state_dict(),
            'optimizer_policy_state_dict': self.optimizer_policy.state_dict(),
            'optimizer_value_state_dict': self.optimizer_value.state_dict(),
            'best_makespan': self.best_makespan,
            'best_schedule': self.best_schedule,
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
        plt.figure(figsize=(12, 6))
        plt.plot(self.training_makespan_history)
        plt.axhline(y=930, color='r', linestyle='--', label='Óptimo: 930')

        window_size = min(30, len(self.training_makespan_history))
        if window_size > 0:
            moving_avg = [sum(self.training_makespan_history[max(0, i-window_size):i])/min(i, window_size)
                         for i in range(1, len(self.training_makespan_history)+1)]
            plt.plot(moving_avg, color='blue', linewidth=2, label=f'Media móvil ({window_size} episodios)')

        plt.xlabel('Episodios')
        plt.ylabel('Makespan')
        plt.title('Evolución del Makespan durante el entrenamiento')
        plt.legend()
        plt.grid(True)

        return plt.gcf()

    def plot_reward_history(self):
        """Visualiza la evolución de las recompensas durante el entrenamiento"""
        plt.figure(figsize=(12, 6))
        plt.plot(self.episode_rewards)

        window_size = min(30, len(self.episode_rewards))
        if window_size > 0:
            moving_avg = [sum(self.episode_rewards[max(0, i-window_size):i])/min(i, window_size)
                         for i in range(1, len(self.episode_rewards)+1)]
            plt.plot(moving_avg, color='green', linewidth=2, label=f'Media móvil ({window_size} episodios)')

        plt.xlabel('Episodios')
        plt.ylabel('Recompensa')
        plt.title('Evolución de la recompensa durante el entrenamiento')
        plt.legend()
        plt.grid(True)

        return plt.gcf()

    def plot_losses(self):
        """Visualiza la evolución de las pérdidas durante el entrenamiento"""
        if not self.training_losses["policy"] or not self.training_losses["value"]:
            return None

        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.plot(self.training_losses["policy"])
        plt.xlabel('Episodios')
        plt.ylabel('Pérdida de política')
        plt.title('Evolución de la pérdida de política')
        plt.grid(True)

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
        plt.figure(figsize=(12, 6))
        plt.plot(self.epsilon_history)
        plt.xlabel('Episodios')
        plt.ylabel('Epsilon (clip)')
        plt.title('Evolución del parámetro de exploración (epsilon)')
        plt.grid(True)
        return plt.gcf()

# ===== HEURÍSTICAS =====

class HeuristicStrategy(ABC):
    """Estrategia base para heurísticas (patrón Strategy)"""

    @abstractmethod
    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        """Selecciona una acción basada en las operaciones elegibles y sus características"""
        pass

class SPTHeuristic(HeuristicStrategy):
    """Heurística de Shortest Processing Time"""

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        return np.argmin([f[3] for f in features])

class LPTHeuristic(HeuristicStrategy):
    """Heurística de Longest Processing Time"""

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        return np.argmax([f[3] for f in features])

class MORHeuristic(HeuristicStrategy):
    """Heurística de Most Operations Remaining"""

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        return np.argmax([f[6] for f in features])

class MWKRHeuristic(HeuristicStrategy):
    """Heurística de Most Work Remaining"""

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        return np.argmax([f[5] for f in features])

class RandomHeuristic(HeuristicStrategy):
    """Heurística aleatoria"""

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        return random.randint(0, len(eligible_ops)-1)

# ===== EVALUADOR DE HEURÍSTICAS =====

class HeuristicEvaluator:
    """Evaluador para comparar diferentes heurísticas"""

    def __init__(self, env: JobShopEnv):
        self.env = env
        self.results = {}

    def evaluate_heuristic(self, heuristic: HeuristicStrategy, name: str) -> float:
        """Evalúa una heurística específica"""
        state = self.env.reset()
        done = False

        while not done:
            eligible_ops = state['eligible_ops']
            if not eligible_ops:
                break

            features = self.env.get_features(state)

            if len(eligible_ops) > 0:
                action_idx = heuristic.select_action(eligible_ops, features)
                action_idx = min(action_idx, len(eligible_ops)-1)  # Asegurar índice válido
                next_state, _, done, _ = self.env.step(action_idx)
                state = next_state

        makespan = max(self.env.job_completion_time) if done else float('inf')
        self.results[name] = makespan
        logger.info(f"{name}: Makespan = {makespan}")
        return makespan

    def evaluate_all(self) -> Dict[str, float]:
        """Evalúa todas las heurísticas comunes"""
        self.evaluate_heuristic(SPTHeuristic(), "SPT")
        self.evaluate_heuristic(LPTHeuristic(), "LPT")
        self.evaluate_heuristic(MORHeuristic(), "MOR")
        self.evaluate_heuristic(MWKRHeuristic(), "MWKR")
        self.evaluate_heuristic(RandomHeuristic(), "Random")
        return self.results

    def compare_with_agent(self, agent_makespan: float) -> Dict[str, float]:
        """Compara el rendimiento del agente con las heurísticas"""
        comparison = {}
        for name, makespan in self.results.items():
            improvement = (makespan - agent_makespan) / makespan * 100
            comparison[name] = improvement
            logger.info(f"vs {name}: {improvement:.2f}% de mejora")
        return comparison

# ===== FÁBRICA DE EXPERIMENTOS =====

class ExperimentFactory:
    """Fábrica para crear y ejecutar experimentos (patrón Factory)"""

    @staticmethod
    def create_ft10_env(reward_strategy: str = "basic", seed: Optional[int] = None, **reward_params) -> JobShopEnv:
        """Crea un entorno con el benchmark FT10"""
        # Configuración del problema FT10
        num_jobs = 10
        num_machines = 10
        sequences = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [0, 2, 4, 9, 3, 1, 6, 5, 7, 8],
            [1, 0, 3, 2, 8, 5, 7, 6, 9, 4],
            [1, 2, 0, 4, 6, 8, 7, 3, 9, 5],
            [2, 0, 1, 5, 3, 4, 8, 7, 9, 6],
            [2, 1, 5, 3, 8, 9, 0, 6, 4, 7],
            [1, 0, 3, 2, 6, 5, 9, 8, 7, 4],
            [2, 0, 1, 5, 4, 6, 8, 9, 7, 3],
            [0, 1, 3, 5, 2, 9, 6, 7, 4, 8],
            [1, 0, 2, 6, 8, 9, 5, 3, 4, 7]
        ]
        durations = [
            [29, 78, 9, 36, 49, 11, 62, 56, 44, 21],
            [43, 90, 75, 11, 69, 28, 46, 46, 72, 30],
            [91, 85, 39, 74, 90, 10, 12, 89, 45, 33],
            [81, 95, 71, 99, 9, 52, 85, 98, 22, 43],
            [14, 6, 22, 61, 26, 69, 21, 49, 72, 53],
            [84, 2, 52, 95, 48, 72, 47, 65, 6, 25],
            [46, 37, 61, 13, 32, 21, 32, 89, 30, 55],
            [31, 86, 46, 74, 32, 88, 19, 48, 36, 79],
            [76, 69, 76, 51, 85, 11, 40, 89, 26, 74],
            [85, 13, 61, 7, 64, 76, 47, 52, 90, 45]
        ]

        # Crear estrategia de recompensa
        reward_strategy_obj = RewardStrategyFactory.create_strategy(reward_strategy, **reward_params)

        # Crear y devolver el entorno
        return JobShopEnv(num_jobs, num_machines, sequences, durations, reward_strategy_obj, seed=seed)

    @staticmethod
    def create_agent(env: JobShopEnv, **agent_params) -> PPOAgent:
        """Crea un agente PPO con los parámetros especificados"""
        return PPOAgent(env, **agent_params)

    @staticmethod
    def run_full_experiment(episodes: int = 100, reward_strategy: str = "basic",
                           agent_params: Dict = None, reward_params: Dict = None,
                           seed: Optional[int] = None, visualize: bool = True,
                           save_plots: bool = True) -> Tuple[PPOAgent, Dict]:
        """Ejecuta un experimento completo con evaluación de heurísticas y entrenamiento"""
        if agent_params is None:
            agent_params = {}
        if reward_params is None:
            reward_params = {}

        # Aplicar semilla para reproducibilidad si se proporciona
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
            torch.manual_seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed(seed)
                torch.cuda.manual_seed_all(seed)
            agent_params['seed'] = seed

        logger.info(f"Iniciando experimento de Job Shop Scheduling con RL (reward_strategy={reward_strategy})...")

        # Crear entorno
        env = ExperimentFactory.create_ft10_env(reward_strategy, seed=seed, **reward_params)

        # Evaluar heurísticas básicas
        logger.info("Evaluando heurísticas básicas como referencia:")
        evaluator = HeuristicEvaluator(env)
        heuristic_results = evaluator.evaluate_all()

        # Crear y entrenar agente
        logger.info("Creando y entrenando agente PPO...")
        default_params = {
            "feature_dim": 7,
            "hidden_dim": 128,
            "lr": 0.0003,
            "gamma": 0.99,
            "eps_clip": 0.2,
            "K_epochs": 4,
            "entropy_coef": 0.01,
            "use_lr_decay": True,
            "use_grad_clip": True,
            "advantage_normalization": True,
            "gae_lambda": 0.95
        }
        # Actualizar con parámetros proporcionados
        default_params.update(agent_params)

        agent = ExperimentFactory.create_agent(env, **default_params)
        agent.train(episodes=episodes, dynamic_entropy=True, early_stopping=True)

        # Evaluar la política final
        logger.info("Evaluando la política final...")
        makespan, schedule, makespan_history = agent.evaluate_policy()
        logger.info(f"Makespan final: {makespan}")
        logger.info(f"Mejor makespan durante entrenamiento: {agent.best_makespan}")
        logger.info(f"Óptimo conocido para FT10: 930")

        # Comparar con las heurísticas
        comparison = evaluator.compare_with_agent(agent.best_makespan)

        # Generar visualizaciones
        plots = {}
        if visualize:
            logger.info("Generando visualizaciones...")
            plots["schedule"] = env.render_schedule("Planificación Final con RL-PPO")
            plots["episode_makespan"] = env.plot_makespan_history()
            plots["training_makespan"] = agent.plot_training_history()
            plots["rewards"] = agent.plot_reward_history()
            plots["losses"] = agent.plot_losses()
            plots["exploration"] = agent.plot_exploration_history()

            # Guardar gráficos si está habilitado
            if save_plots:
                for name, plot in plots.items():
                    if plot is not None:
                        plot.savefig(f"{name}.png")
                        plt.close(plot)

        return agent, {
            "heuristic_results": heuristic_results,
            "comparison": comparison,
            "best_makespan": agent.best_makespan,
            "final_makespan": makespan,
            "plots": plots if visualize else None
        }

# ===== EJEMPLO DE USO =====

# ===== SCRIPT PRINCIPAL CON EJEMPLO DE USO =====

def main():
    """Función principal para ejecutar el experimento"""

    # Ejemplo de experimento con recompensa avanzada
    agent, results = ExperimentFactory.run_full_experiment(
        episodes=300,
        reward_strategy="advanced",
        agent_params={
            "lr": 0.0003,
            "gamma": 0.99,
            "entropy_coef": 0.02,
            "K_epochs": 4,
            "use_lr_decay": True,
            "use_grad_clip": True,
            "advantage_normalization": True,
            "gae_lambda": 0.95,
            "seed": None  # Para reproducibilidad
        },
        reward_params={
            "makespan_weight": 1.0,
            "idle_weight": 0.2,
            "critical_weight": 0.1,
            "balance_weight": 0.05,
            "progress_weight": 0.2,
            "local_improvement_weight": 0.15
        }
    )

    # Imprimir la mejor planificación
    logger.info("Mejor planificación encontrada:")
    best_makespan = max(op['end'] for op in agent.best_schedule) if agent.best_schedule else float('inf')
    logger.info(f"Makespan: {best_makespan}")

    if agent.best_schedule:
        # Ordenar por tiempo de inicio
        sorted_schedule = sorted(agent.best_schedule, key=lambda x: x['start'])

        logger.info("Secuencia de operaciones:")
        logger.info("Job | Op | Machine | Start | End | Duration")
        logger.info("-" * 50)
        for op in sorted_schedule:
            logger.info(f"{op['job']:3d} | {op['operation']:2d} | {op['machine']:7d} | {op['start']:5d} | {op['end']:3d} | {op['end'] - op['start']:8d}")

    # Guardar el mejor modelo
    agent.save_checkpoint("best_ppo_agent.pt")

if __name__ == "__main__":
    main()