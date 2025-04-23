"""
Implementación de agente PPO (Proximal Policy Optimization) para Job Shop Scheduling.
"""

import torch
import torch.nn.functional as F  # Nombre común en la comunidad PyTorch
import torch.optim as optim
from torch.distributions import Categorical
import numpy as np
import time
import logging
from typing import List, Dict, Tuple, Optional
from copy import deepcopy


from jobshop_rl.agents.base_agent import Agent
from jobshop_rl.agents.ppo_memory import PPOMemory
from jobshop_rl.models.neural_models import PolicyNetwork, ValueNetwork, calculate_hidden_dim
from jobshop_rl.environment.job_shop_env import JobShopEnv
from jobshop_rl.utils.logging import TrainingLogger
from jobshop_rl.utils.path_utils import get_checkpoint_path
from jobshop_rl.utils.checkpoint_manager import CheckpointManager
from jobshop_rl.utils.visualization import plot_makespan_history, plot_training_metrics

logger = logging.getLogger("JobShopRL.PPOAgent")

class PPOAgent(Agent):
    """Agente de Proximal Policy Optimization para Job Shop Scheduling"""

    def __init__(self, env: JobShopEnv, feature_dim: int = 7, hidden_dim: int = None,
                 lr: float = 0.0003, gamma: float = 0.99, eps_clip: float = 0.2,
                 K_epochs: int = 4, entropy_coef: float = 0.01,
                 use_lr_decay: bool = True, use_grad_clip: bool = True,
                 advantage_normalization: bool = True, gae_lambda: float = 0.95,
                 csv_logger: Optional[TrainingLogger] = None,
                 seed: Optional[int] = None,
                 policy_depth: int = 2,
                 value_depth: int = 3):
    
        self.env = env
        self.feature_dim = feature_dim
        
        # Calcular dimensión oculta automáticamente si no se proporciona
        if hidden_dim is None:
            self.hidden_dim = calculate_hidden_dim(env.num_jobs, env.num_machines)
        else:
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
        self.policy_depth = policy_depth
        self.value_depth = value_depth

        # Para problemas grandes, aumentar la profundidad de las redes
        # y decidir si usar arquitectura avanzada
        problem_size = env.num_jobs * env.num_machines
        self.use_advanced_networks = False
        self.dropout_rate = 0.1
        
        if problem_size > 400:  # Para problemas > 20x20
            self.policy_depth = max(3, policy_depth)
            self.value_depth = max(4, value_depth)
            
        if problem_size > 750:  # Para problemas ≥ 50x15
            self.use_advanced_networks = True
            self.dropout_rate = 0.15
            
        if problem_size > 1500:  # Para problemas muy grandes (100x20)
            self.policy_depth = max(5, policy_depth)  # Incrementado de 4 a 5
            self.value_depth = max(6, value_depth)    # Incrementado de 5 a 6
            self.dropout_rate = 0.2
            
            # Para problemas 100x20, usar arquitectura avanzada con capacidad aumentada
            if problem_size >= 2000:
                self.dropout_rate = 0.25
                # Incrementar el número de épocas de actualización para PPO
                self.K_epochs = max(5, self.K_epochs)
                # Reducir el learning rate para problemas más grandes
                self.lr = min(0.0002, self.lr)

        # Establecer semilla para reproducibilidad
        if seed is not None:
            torch.manual_seed(seed)
            np.random.seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed(seed)
                torch.cuda.manual_seed_all(seed)

        # Dimensión del estado para la red de valor
        self.state_dim = env.num_jobs + env.num_machines + 2

        # Inicializar redes con la arquitectura apropiada
        if self.use_advanced_networks:
            from jobshop_rl.models.neural_models import AdvancedPolicyNetwork, AdvancedValueNetwork
            self.policy = AdvancedPolicyNetwork(feature_dim, self.hidden_dim, 
                                              self.policy_depth, self.dropout_rate)
            self.value = AdvancedValueNetwork(self.state_dim, self.hidden_dim, 
                                            self.value_depth, self.dropout_rate)
            logger.info(f"Usando arquitectura de red avanzada con dropout {self.dropout_rate}")
        else:
            self.policy = PolicyNetwork(feature_dim, self.hidden_dim, self.policy_depth)
            self.value = ValueNetwork(self.state_dim, self.hidden_dim, self.value_depth)

        # Optimizadores
        self.optimizer_policy = optim.Adam(self.policy.parameters(), lr=lr)
        self.optimizer_value = optim.Adam(self.value.parameters(), lr=lr)

        # Tracking del rendimiento
        self.best_makespan = float('inf')
        self.best_schedule = None
        self.best_makespan_history = None
        self.best_model_state = None  # Para guardar el estado del mejor modelo
        self.training_makespan_history = []
        self.episode_rewards = []
        self.training_losses = {"policy": [], "value": []}
        self.epsilon_history = []  # Para tracking de la exploración
        self.total_episodes = 0
        
        # Guardar valores iniciales para uso en schedulers
        self.initial_entropy_coef = entropy_coef
        
        # Tiempo de inicio para tracking de duración
        self.training_start_time = None
        
        # Inicializar componentes modulares
        self.memory = PPOMemory(
            gamma=gamma, 
            gae_lambda=gae_lambda,
            advantage_normalization=advantage_normalization
        )
        self.checkpoint_manager = CheckpointManager()

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

    # El método calculate_gae ha sido movido a la clase PPOMemory

    def _run_episode_without_training(self) -> Tuple[bool, Dict]:
        """
        Ejecuta un episodio completo sin entrenamiento para evaluación o recreación de soluciones.
        
        Returns:
            Tuple[bool, Dict]: Indicador de si el episodio terminó correctamente y la info del último step
        """
        # Poner las redes en modo de evaluación
        self.policy.eval()
        self.value.eval()
        
        state = self.env.reset()
        done = False
        info = {}

        while not done:
            action_idx, _, _ = self.select_action(state, training=False)

            if action_idx is None:
                break

            state, reward, done, info = self.env.step(action_idx)

        return done, info

    def _recreate_best_solution(self) -> List[float]:
        """Recrea la mejor solución encontrada para obtener el makespan history"""
        self._run_episode_without_training()
        return self.env.makespan_history

    def update_learning_rate(self, current_episode: int, total_episodes: int):
        """
        Actualiza la tasa de aprendizaje según la programación definida.
        
        Args:
            current_episode: Episodio actual
            total_episodes: Total de episodios planificados
        """
        if not self.use_lr_decay:
            return
        
        # Programación del learning rate (decaimiento lineal)
        decay_factor = max(0.1, 1.0 - (current_episode / total_episodes))
        current_lr = self.lr * decay_factor
        
        # Actualizar optimizadores
        for param_group in self.optimizer_policy.param_groups:
            param_group['lr'] = current_lr
        for param_group in self.optimizer_value.param_groups:
            param_group['lr'] = current_lr
            
    def _log_training_progress(self, current_episode: int, total_episodes: int, log_interval: int) -> float:
        """
        Registra el progreso del entrenamiento periódicamente.
        
        Args:
            current_episode: Episodio actual
            total_episodes: Total de episodios
            log_interval: Intervalo para el cálculo de promedios
            
        Returns:
            float: Recompensa promedio (para uso en early stopping)
        """
        if not self.training_makespan_history:
            logger.info(f"Episodio {current_episode}/{total_episodes}, Sin makespan válido aún")
            return 0.0
            
        # Calcular promedios sobre los últimos log_interval episodios
        avg_makespan = sum(self.training_makespan_history[-log_interval:]) / min(log_interval, len(self.training_makespan_history[-log_interval:]))
        avg_reward = sum(self.episode_rewards[-log_interval:]) / min(log_interval, len(self.episode_rewards[-log_interval:]))
        
        training_time = time.time() - self.training_start_time
        
        # Registrar progreso
        logger.info(f"Episodio {current_episode}/{total_episodes}, "
                    f"Recompensa promedio: {avg_reward:.4f}, "
                    f"Makespan promedio: {avg_makespan:.2f}, "
                    f"Mejor: {self.best_makespan}, "
                    f"Tiempo: {training_time:.2f}s")
        
        return avg_reward
    
    def _check_early_stopping(self, avg_reward: float, best_avg_reward: float, 
                             no_improvement_count: int, patience: int) -> Tuple[float, int, bool]:
        """
        Comprueba si se cumplen las condiciones para early stopping.
        
        Args:
            avg_reward: Recompensa promedio actual
            best_avg_reward: Mejor recompensa promedio hasta ahora
            no_improvement_count: Contador de episodios sin mejora
            patience: Número de episodios sin mejora para activar early stopping
            
        Returns:
            Tuple[float, int, bool]: Nueva mejor recompensa, nuevo contador, y si debe detenerse
        """
        should_stop = False
        new_best = best_avg_reward
        new_count = no_improvement_count
        
        if avg_reward > best_avg_reward:
            new_best = avg_reward
            new_count = 0
        else:
            new_count += 1

        if new_count >= patience:
            logger.info(f"Early stopping activado después de {new_count} episodios sin mejora en la recompensa promedio")
            should_stop = True
            
        return new_best, new_count, should_stop
    
    def _update_exploration_parameters(self, current_episode: int, total_episodes: int, 
                               initial_eps_clip: float, dynamic_entropy: bool):
        """
        Actualiza los parámetros relacionados con la exploración.
        
        Args:
            current_episode: Episodio actual
            total_episodes: Total de episodios
            initial_eps_clip: Valor inicial de epsilon
            dynamic_entropy: Si se debe ajustar dinámicamente el coeficiente de entropía
        """
        if not dynamic_entropy:
            return
            
        # Gradualmente reducir epsilon para fomentar explotación
        self.eps_clip = initial_eps_clip * (1 - (current_episode / total_episodes) * 0.7)  # Mínimo 30% del original

        # Ajuste dinámico del coeficiente de entropía
        progress = current_episode / total_episodes
        self.entropy_coef = max(0.001, self.entropy_coef * (1 - progress * 0.9))  # Mínimo 10% del original
    
    def _update_networks(self) -> Tuple[float, float]:
        """
        Actualiza las redes de política y valor usando la experiencia recopilada.
        
        Returns:
            Tuple con pérdidas medias de política y valor
        """
        # Asegurar que estamos en modo de entrenamiento
        self.policy.train()
        self.value.train()
        
        # Obtener tensores de la memoria
        old_actions, old_log_probs, returns, advantages, features_list = self.memory.get_tensors()

        # Realizar actualizaciones de PPO
        policy_losses = []
        value_losses = []
        
        # Determinar el tamaño de mini-batch apropiado
        total_samples = len(self.memory.states)
        # Para redes avanzadas con BatchNorm, queremos mini-batches de al menos 4 ejemplos
        if self.use_advanced_networks and total_samples >= 8:
            batch_size = min(4, total_samples // 2)  # Al menos 2 mini-batches
            
            # Generador de índices para mini-batches
            def get_minibatch_indices():
                indices = np.arange(total_samples)
                np.random.shuffle(indices)
                start_idx = 0
                while start_idx < total_samples:
                    end_idx = min(start_idx + batch_size, total_samples)
                    yield indices[start_idx:end_idx]
                    start_idx = end_idx
            
            # Mini-batch updates for K epochs
            for _ in range(self.K_epochs):
                for batch_indices in get_minibatch_indices():
                    # Preparar mini-batch
                    batch_features = [features_list[i] for i in batch_indices]
                    batch_states = [self.memory.states[i] for i in batch_indices]
                    batch_actions = [self.memory.actions[i] for i in batch_indices]
                    batch_old_log_probs = torch.stack([old_log_probs[i] for i in batch_indices])
                    batch_returns = torch.stack([returns[i] for i in batch_indices])
                    batch_advantages = torch.stack([advantages[i] for i in batch_indices])
                    
                    # Procesar features y valores
                    value_inputs = torch.stack([self._state_to_value_input(state) for state in batch_states])
                    values = self.value(value_inputs)
                    
                    # Procesar mini-batch de features para la política
                    # Cada elemento de batch_features puede tener diferente tamaño, no podemos usar torch.stack
                    batch_new_log_probs = []
                    batch_dist_entropy = []
                    
                    for i, idx in enumerate(batch_indices):
                        state_features = batch_features[i]
                        action = torch.tensor(batch_actions[i], dtype=torch.int64)
                        new_log_prob, dist_entropy = self.evaluate(state_features, action)
                        batch_new_log_probs.append(new_log_prob)
                        batch_dist_entropy.append(dist_entropy)
                    
                    batch_new_log_probs = torch.stack(batch_new_log_probs)
                    batch_dist_entropy = torch.stack(batch_dist_entropy)
                    
                    # Calcular ratios y pérdida de política
                    ratios = torch.exp(batch_new_log_probs - batch_old_log_probs.detach())
                    surr1 = ratios * batch_advantages
                    surr2 = torch.clamp(ratios, 1-self.eps_clip, 1+self.eps_clip) * batch_advantages
                    policy_loss = -torch.min(surr1, surr2).mean() - self.entropy_coef * batch_dist_entropy.mean()
                    
                    # Calcular pérdida de valor
                    value_loss = F.mse_loss(values.squeeze(), batch_returns)
                    
                    # Actualizar política
                    self.optimizer_policy.zero_grad()
                    policy_loss.backward()
                    if self.use_grad_clip:
                        torch.nn.utils.clip_grad_norm_(self.policy.parameters(), 0.5)
                    self.optimizer_policy.step()
                    
                    # Actualizar valor
                    self.optimizer_value.zero_grad()
                    value_loss.backward()
                    if self.use_grad_clip:
                        torch.nn.utils.clip_grad_norm_(self.value.parameters(), 0.5)
                    self.optimizer_value.step()
                    
                    policy_losses.append(policy_loss.item())
                    value_losses.append(value_loss.item())
        else:
            # Si no estamos usando redes avanzadas o hay pocos ejemplos, usar el enfoque original
            # Mini-batch updates for K epochs
            for _ in range(self.K_epochs):
                for i in range(len(self.memory.states)):
                    state_features = features_list[i]
                    value_input = self._state_to_value_input(self.memory.states[i])
    
                    value = self.value(value_input)
    
                    new_log_probs, dist_entropy = self.evaluate(state_features, torch.tensor(self.memory.actions[i], dtype=torch.int64))
    
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

        # Calcular pérdidas medias
        policy_loss_mean = float(np.mean(policy_losses))
        value_loss_mean = float(np.mean(value_losses))
        
        # Registrar pérdidas medias
        self.training_losses["policy"].append(policy_loss_mean)
        self.training_losses["value"].append(value_loss_mean)
        
        return policy_loss_mean, value_loss_mean
    
    def _log_episode_metrics(self, episode_reward: float, info: Dict, done: bool):
        """
        Registra métricas después de un episodio completo.
        
        Args:
            episode_reward: Recompensa total del episodio
            info: Información del último step
            done: Si el episodio terminó correctamente
        """
        # Registrar makespan si el episodio terminó correctamente
        if done and info.get('makespan') is not None:
            makespan = info['makespan']
            self.training_makespan_history.append(makespan)

            if makespan < self.best_makespan:
                self.best_makespan = makespan
                self.best_schedule = deepcopy(self.env.schedule_history)
                self.best_makespan_history = deepcopy(self.env.makespan_history)
                
                # Guardar también el estado del modelo para uso futuro
                self.best_model_state = {
                    "policy": deepcopy(self.policy.state_dict()),
                    "value": deepcopy(self.value.state_dict())
                }
                
                logger.info(f"Nuevo mejor makespan: {makespan}")
                
                # Comentado el guardado del mejor checkpoint para mejorar eficiencia
                # self.save_best_checkpoint()

        self.episode_rewards.append(episode_reward)
        self.epsilon_history.append(self.eps_clip)  # Tracking de epsilon

        # Actualizar el CSV logger si está configurado
        if self.csv_logger:
            # Verificar que csv_logger es un objeto TrainingLogger válido y no un diccionario
            if not hasattr(self.csv_logger, 'log_step'):
                # Si no es un objeto válido, intentar recuperarse
                from jobshop_rl.utils.logging import TrainingLogger
                if isinstance(self.csv_logger, dict) and 'filename' in self.csv_logger:
                    # Intentar crear un nuevo logger con la información del diccionario
                    logger.warning("csv_logger es un diccionario en lugar de un objeto TrainingLogger. Intentando recuperar.")
                    try:
                        self.csv_logger = TrainingLogger(filename=self.csv_logger.get('filename'))
                    except:
                        logger.error("No se pudo recuperar el csv_logger. Deshabilitando logging CSV.")
                        self.csv_logger = None
                else:
                    logger.error("csv_logger no es un objeto TrainingLogger válido. Deshabilitando logging CSV.")
                    self.csv_logger = None
            
            # Continuar solo si tenemos un logger válido
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
    
    def train_episode(self) -> float:
        """Entrena un episodio completo y devuelve la recompensa total"""
        # Registrar tiempo de inicio para problemas grandes
        start_time = time.time()
        
        # Asegurar que las redes estén en modo de entrenamiento
        self.policy.train()
        self.value.train()
        
        state = self.env.reset()
        done = False
        episode_reward = 0
        info = {}  # Inicializar info con un diccionario vacío por defecto
        self.total_episodes += 1
        
        # Limpiar memoria para el nuevo episodio
        self.memory.clear()

        while not done:
            action_idx, action_log_prob, features = self.select_action(state, training=True)

            if action_idx is None:
                break

            # Calcular valor para GAE
            value_input = self._state_to_value_input(state)
            with torch.no_grad():
                # Si estamos usando redes avanzadas, usar evaluación para BatchNorm
                if self.use_advanced_networks:
                    was_training = self.value.training
                    self.value.eval()
                    value = self.value(value_input).item()
                    if was_training:
                        self.value.train()
                else:
                    value = self.value(value_input).item()

            next_state, reward, done, info = self.env.step(action_idx)
            
            # Almacenar en memoria
            self.memory.store(
                state=state,
                action=action_idx,
                log_prob=action_log_prob,
                reward=reward,
                features=features,
                is_terminal=done,
                value=value
            )

            episode_reward += reward
            state = next_state

        # Registrar métricas del episodio
        self._log_episode_metrics(episode_reward, info, done)

        # Si no hay experiencias, terminar
        if self.memory.is_empty():
            return episode_reward

        # Actualizar redes (las pérdidas se registran dentro del método)
        policy_loss_mean, value_loss_mean = self._update_networks()
        
        # Registrar el tiempo de procesamiento para diagnóstico en problemas grandes
        end_time = time.time()
        if self.env.num_jobs * self.env.num_machines > 750:  # Solo para problemas grandes
            episode_time = end_time - start_time
            logger.info(f"Episodio {self.total_episodes} completado en {episode_time:.2f}s. Pérdidas: P={policy_loss_mean:.4f}, V={value_loss_mean:.4f}")
            
        return episode_reward

    def train(self, episodes: int = 500, lr_decay: bool = True,
              log_interval: int = 10, checkpoint_interval: int = 50,
              dynamic_entropy: bool = True, early_stopping: bool = False,
              early_stopping_patience: int = 50):
        """Entrena el agente por un número específico de episodios"""
        logger.info("Iniciando entrenamiento...")

        # Iniciar cronómetro para tracking de duración
        self.training_start_time = time.time()

        # Guardar configuración de lr_decay para update_learning_rate
        self.use_lr_decay = lr_decay
        
        # Guardar valores iniciales para referencia
        initial_eps_clip = self.eps_clip

        # Seguimiento para early stopping
        best_avg_reward = float('-inf')
        no_improvement_count = 0

        for i in range(1, episodes+1):
            # Actualizar learning rate una sola vez por episodio
            self.update_learning_rate(i, episodes)

            # Ajustar parámetros de exploración
            self._update_exploration_parameters(i, episodes, initial_eps_clip, dynamic_entropy)

            # Entrenar un episodio
            self.train_episode()

            # Registrar métricas periódicamente
            if i % log_interval == 0:
                avg_reward = self._log_training_progress(i, episodes, log_interval)
                
                # Comprobar early stopping si está habilitado
                if early_stopping and self.training_makespan_history:
                    best_avg_reward, no_improvement_count, should_stop = self._check_early_stopping(
                        avg_reward, best_avg_reward, no_improvement_count, early_stopping_patience
                    )
                    if should_stop:
                        break

            # Comentado el guardado periódico para mejorar eficiencia
            # if checkpoint_interval > 0 and i % checkpoint_interval == 0:
            #     self.save_checkpoint(f"checkpoint_ep{i}.pt")
        
        # Registrar el tiempo total de entrenamiento
        total_training_time = time.time() - self.training_start_time
        logger.info(f"Entrenamiento completado en {total_training_time:.2f} segundos")
        
        # Guardar el mejor modelo encontrado durante todo el entrenamiento
        if self.best_model_state:
            logger.info(f"Guardando el mejor modelo encontrado (makespan: {self.best_makespan})")
            self.save_best_checkpoint()
            
            # Cargar el mejor modelo para la evaluación final
            policy_backup = self.policy.state_dict().copy()
            value_backup = self.value.state_dict().copy()
            
            # Cargar el mejor modelo
            self.policy.load_state_dict(self.best_model_state["policy"])
            self.value.load_state_dict(self.best_model_state["value"])
            
            # Evaluación final con el mejor modelo
            logger.info("Evaluando el mejor modelo encontrado...")
            best_makespan, best_schedule, _, _ = self.evaluate_policy()
            logger.info(f"Makespan con el mejor modelo: {best_makespan}")
            
            # Restaurar el modelo actual
            self.policy.load_state_dict(policy_backup)
            self.value.load_state_dict(value_backup)
        
        # Registrar el registro final en el CSV si está configurado
        if self.csv_logger:
            self.csv_logger.save()

    def save_checkpoint(self, path: str, output_dir: str = None):
        """
        Guarda el modelo en un checkpoint.
        
        Args:
            path: Nombre del archivo de checkpoint
            output_dir: Directorio de salida opcional (usa el predeterminado si es None)
        """
        # Si tenemos un directorio específico, usarlo; de lo contrario, usar el predeterminado
        if output_dir:
            # Asegurar que el directorio existe
            os.makedirs(output_dir, exist_ok=True)
            checkpoint_path = os.path.join(output_dir, path)
        else:
            # Obtener la ruta completa para el checkpoint
            checkpoint_path = get_checkpoint_path(path)
            
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
        
        # Usar el CheckpointManager para guardar
        self.checkpoint_manager.save_checkpoint(checkpoint, checkpoint_path)
        
    def save_best_checkpoint(self):
        """
        Guarda el checkpoint del modelo que ha conseguido el mejor makespan.
        Este método se llama automáticamente cuando se encuentra un nuevo mejor makespan.
        """
        # Obtener la ruta para el checkpoint del mejor modelo
        checkpoint_path = get_checkpoint_path("best_model.pt")
        
        checkpoint = {
            'policy_state_dict': self.policy.state_dict(),
            'value_state_dict': self.value.state_dict(),
            'optimizer_policy_state_dict': self.optimizer_policy.state_dict(),
            'optimizer_value_state_dict': self.optimizer_value.state_dict(),
            'best_makespan': self.best_makespan,
            'best_schedule': self.best_schedule,
            'best_makespan_history': self.best_makespan_history,
            'best_model_state': self.best_model_state,
            'training_history': self.training_makespan_history,
            'episode_rewards': self.episode_rewards,
            'training_losses': self.training_losses,
            'total_episodes': self.total_episodes
        }
        
        # Usar el CheckpointManager para guardar
        self.checkpoint_manager.save_checkpoint(checkpoint, checkpoint_path)
        logger.info(f"Guardado checkpoint del mejor modelo (makespan: {self.best_makespan}) en {checkpoint_path}")

    def load_checkpoint(self, path: str):
        """
        Carga un modelo desde un checkpoint.
        
        Args:
            path: Ruta al archivo de checkpoint
        """
        # Usar el CheckpointManager para cargar
        checkpoint = self.checkpoint_manager.load_checkpoint(path)
        
        # Cargar los datos al agente
        self.policy.load_state_dict(checkpoint['policy_state_dict'])
        self.value.load_state_dict(checkpoint['value_state_dict'])
        self.optimizer_policy.load_state_dict(checkpoint['optimizer_policy_state_dict'])
        self.optimizer_value.load_state_dict(checkpoint['optimizer_value_state_dict'])
        self.best_makespan = checkpoint['best_makespan']
        self.best_schedule = checkpoint['best_schedule']
        self.best_makespan_history = checkpoint.get('best_makespan_history')
        self.best_model_state = checkpoint.get('best_model_state')
        self.training_makespan_history = checkpoint['training_history']
        self.episode_rewards = checkpoint.get('episode_rewards', [])
        self.training_losses = checkpoint.get('training_losses', {"policy": [], "value": []})

    def evaluate_policy(self) -> Tuple[float, List[Dict], List[float], float]:
        """Evalúa la política actual en un episodio completo"""
        start_time = time.time()
        done, info = self._run_episode_without_training()
        execution_time = time.time() - start_time
        
        makespan = max(self.env.job_completion_time) if done else float('inf')
        return makespan, self.env.schedule_history, self.env.makespan_history, execution_time

    def plot_training_history(self, optimal_makespan: Optional[int] = 930):
        """
        Visualiza la evolución del makespan durante el entrenamiento.
        
        Args:
            optimal_makespan: Valor óptimo de makespan para referencia (opcional)
            
        Returns:
            Figura de matplotlib con la visualización
        """
        return plot_makespan_history(
            makespan_history=self.training_makespan_history,
            title='Evolución del Makespan durante el entrenamiento',
            optimal_makespan=optimal_makespan
        )

    def plot_reward_history(self):
        """
        Visualiza la evolución de las recompensas durante el entrenamiento.
        
        Returns:
            Figura de matplotlib con la visualización
        """
        # Usar plot_makespan_history de utils.visualization pero adaptado para recompensas
        return plot_makespan_history(
            makespan_history=self.episode_rewards,
            title='Evolución de la recompensa durante el entrenamiento',
            optimal_makespan=None  # No hay valor óptimo para recompensas
        )

    def plot_losses(self):
        """
        Visualiza la evolución de las pérdidas durante el entrenamiento.
        
        Returns:
            Diccionario de figuras de matplotlib
        """
        if not self.training_losses["policy"] or not self.training_losses["value"]:
            return None
            
        # Crear un diccionario con las métricas para usar plot_training_metrics
        metrics = {
            'policy_loss': self.training_losses["policy"],
            'value_loss': self.training_losses["value"]
        }
        
        return plot_training_metrics(metrics)

    def plot_exploration_history(self):
        """
        Visualiza la evolución del parámetro epsilon (exploración) durante el entrenamiento.
        
        Returns:
            Figura de matplotlib con la visualización
        """
        return plot_makespan_history(
            makespan_history=self.epsilon_history,
            title='Evolución del parámetro de exploración (epsilon)',
            optimal_makespan=None
        )
        
    def plot_best_solution_makespan(self, optimal_makespan: Optional[int] = 930):
        """
        Visualiza la evolución del makespan de la mejor solución encontrada.
        
        Args:
            optimal_makespan: Valor óptimo de makespan para referencia (opcional)
            
        Returns:
            Figura de matplotlib con la visualización
        """
        if not self.best_makespan_history:
            return None
            
        return plot_makespan_history(
            makespan_history=self.best_makespan_history,
            title='Evolución del Makespan de la Mejor Solución',
            optimal_makespan=optimal_makespan
        )