"""
Implementación de agente PPO (Proximal Policy Optimization) con 
soporte para arquitecturas GNN y Transformer para problemas de Job Shop Scheduling.

Este módulo extiende el agente PPO original para permitir el uso de
redes neuronales basadas en grafos y mecanismos de atención.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Categorical
import numpy as np
import time
import logging
from typing import Dict, List, Tuple, Any, Union, Optional
from copy import deepcopy

from jobshop_rl.models.gnn_models import (
    GNNModel, TransformerModel, HybridGNNAttentionModel, BaseModel
)
from jobshop_rl.preprocessing.state_processors import (
    JSPGraphBuilder, SequenceBuilder, JSPFeatureExtractor
)
from jobshop_rl.utils.path_utils import get_checkpoint_path
from jobshop_rl.utils.checkpoint_manager import CheckpointManager
from jobshop_rl.utils.visualization import plot_makespan_history, plot_training_metrics

# Configurar logger
logger = logging.getLogger("JobShopRL.PPOAgentGNN")


class AdvancedPPOAgent:
    """
    Agente de aprendizaje por refuerzo basado en PPO con soporte para
    arquitecturas avanzadas de GNN y Transformer.
    """
    
    def __init__(
        self, 
        env,
        model_type: str = 'gnn',  # 'gnn', 'transformer', 'hybrid'
        hidden_dim: int = 128, 
        lr: float = 0.0003,
        gamma: float = 0.99,
        eps_clip: float = 0.2,
        K_epochs: int = 4,
        entropy_coef: float = 0.01,
        use_lr_decay: bool = True,
        use_grad_clip: bool = True,
        advantage_normalization: bool = True,
        gae_lambda: float = 0.95,
        node_feature_dim: int = 7,
        edge_feature_dim: int = 3,
        sequence_feature_dim: int = 9,
        num_gnn_layers: int = 2,
        num_heads: int = 4,
        num_attn_layers: int = 1,
        csv_logger = None,
        device = None
    ):
        """
        Inicializa el agente PPO con arquitecturas avanzadas.
        
        Args:
            env: Entorno de Job Shop Scheduling
            model_type: Tipo de modelo a utilizar ('gnn', 'transformer', 'hybrid')
            hidden_dim: Dimensión de las capas ocultas
            lr: Tasa de aprendizaje
            gamma: Factor de descuento
            eps_clip: Parámetro de recorte de PPO
            K_epochs: Número de epochs para actualización PPO
            entropy_coef: Coeficiente para regularización de entropía
            use_lr_decay: Si se debe reducir lr durante el entrenamiento
            use_grad_clip: Si se debe recortar el gradiente
            advantage_normalization: Si se deben normalizar las ventajas
            gae_lambda: Factor lambda para GAE (Generalized Advantage Estimation)
            node_feature_dim: Dimensión de características de nodos para GNN
            edge_feature_dim: Dimensión de características de aristas para GNN
            sequence_feature_dim: Dimensión de características de secuencia para Transformer
            num_gnn_layers: Número de capas GNN
            num_heads: Número de cabezas de atención
            num_attn_layers: Número de capas de atención para modelo híbrido
            csv_logger: Logger opcional para métricas
            device: Dispositivo para tensores (CPU/GPU)
        """
        self.env = env
        self.model_type = model_type
        self.lr = lr
        self.gamma = gamma
        self.eps_clip = eps_clip
        self.K_epochs = K_epochs
        self.entropy_coef = entropy_coef
        self.initial_entropy_coef = entropy_coef
        self.use_lr_decay = use_lr_decay
        self.use_grad_clip = use_grad_clip
        self.advantage_normalization = advantage_normalization
        self.gae_lambda = gae_lambda
        self.csv_logger = csv_logger
        
        # Determinar dispositivo (CPU/GPU)
        self.device = device if device else torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Usando dispositivo: {self.device}")
        
        # Obtener dimensiones del problema
        self.num_jobs = env.num_jobs
        self.num_machines = env.num_machines
        
        # Crear preprocesadores según el tipo de modelo
        self.feature_extractor = JSPFeatureExtractor(self.num_jobs, self.num_machines)
        
        if model_type in ['gnn', 'hybrid']:
            self.graph_builder = JSPGraphBuilder(
                self.num_jobs, 
                self.num_machines,
                feature_extractor=lambda state, job_idx, op_idx: self.feature_extractor.extract_features(state, job_idx, op_idx, self.env)
            )
        
        if model_type in ['transformer', 'hybrid']:
            self.sequence_builder = SequenceBuilder(
                self.num_jobs,
                self.num_machines,
                feature_extractor=lambda state, job_idx, op_idx: self.feature_extractor.extract_features(state, job_idx, op_idx, self.env)
            )
        
        # Inicializar modelo según el tipo especificado
        if model_type == 'gnn':
            self.model = GNNModel(
                node_feature_dim=node_feature_dim,
                edge_feature_dim=edge_feature_dim,
                hidden_dim=hidden_dim,
                num_gnn_layers=num_gnn_layers
            ).to(self.device)
        elif model_type == 'transformer':
            self.model = TransformerModel(
                feature_dim=sequence_feature_dim,
                hidden_dim=hidden_dim,
                num_heads=num_heads,
                num_layers=num_attn_layers
            ).to(self.device)
        elif model_type == 'hybrid':
            self.model = HybridGNNAttentionModel(
                node_feature_dim=node_feature_dim,
                edge_feature_dim=edge_feature_dim,
                hidden_dim=hidden_dim,
                num_gnn_layers=num_gnn_layers,
                num_heads=num_heads,
                num_attn_layers=num_attn_layers
            ).to(self.device)
        else:
            raise ValueError(f"Tipo de modelo desconocido: {model_type}")
        
        # Optimizador
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        
        # Listas para almacenar historial de entrenamiento
        self.rewards = []
        self.saved_log_probs = []
        self.saved_values = []
        self.saved_actions = []
        self.saved_states = []
        self.saved_masks = []
        self.entropies = []
        
        # Métricas de entrenamiento
        self.policy_losses = []
        self.value_losses = []
        self.total_losses = []
        self.episode_rewards = []
        self.episode_lengths = []
        self.makespan_history = []
        self.training_makespan_history = []
        
        # Mejor solución encontrada
        self.best_makespan = float('inf')
        self.best_schedule = None
        self.best_makespan_history = []
        self.best_model_state = None
        
        # Inicializar checkpoint manager
        self.checkpoint_manager = CheckpointManager()
        
        # Contador de episodios totales
        self.total_episodes = 0
        
        logger.info(f"Agente PPO avanzado inicializado con modelo {model_type}")
    
    def preprocess_state(self, state):
        """
        Preprocesa el estado según el tipo de modelo seleccionado.
        
        Args:
            state: Estado del entorno
            
        Returns:
            Inputs procesados para el modelo y máscara de acciones válidas
        """
        # Obtener máscara de acciones válidas del estado
        eligible_ops = state.get('eligible_ops', [])
        action_mask = torch.zeros(self.num_jobs * self.num_machines, dtype=torch.bool)
        
        for job_idx in eligible_ops:
            # Obtener el índice de operación del estado del trabajo
            op_idx = state['job_status'][job_idx]
            node_idx = job_idx * self.num_machines + op_idx
            action_mask[node_idx] = True
        
        # Preprocesar según tipo de modelo
        if self.model_type == 'gnn':
            # Pasar el entorno al graph_builder para que pueda acceder a las secuencias y duraciones
            node_features, edge_index, edge_features, _ = self.graph_builder.build_graph(state, action_mask, self.env)
            
            # Mover tensores al dispositivo
            node_features = node_features.to(self.device)
            edge_index = edge_index.to(self.device)
            edge_features = edge_features.to(self.device)
            action_mask = action_mask.to(self.device)
            
            return (node_features, edge_index, edge_features, action_mask)
            
        elif self.model_type == 'transformer':
            sequence_features, _ = self.sequence_builder.build_sequence(state, action_mask, self.env)
            
            # Mover tensores al dispositivo
            sequence_features = sequence_features.to(self.device)
            action_mask = action_mask.to(self.device)
            
            return (sequence_features, action_mask)
            
        elif self.model_type == 'hybrid':
            # Para el modelo híbrido, necesitamos tanto la representación de grafo como de secuencia
            node_features, edge_index, edge_features, _ = self.graph_builder.build_graph(state, action_mask, self.env)
            
            # Mover tensores al dispositivo
            node_features = node_features.to(self.device)
            edge_index = edge_index.to(self.device)
            edge_features = edge_features.to(self.device)
            action_mask = action_mask.to(self.device)
            
            return (node_features, edge_index, edge_features, action_mask)
        
        else:
            raise ValueError(f"Tipo de modelo no soportado para preprocesamiento: {self.model_type}")
    
    def select_action(self, state, training=True):
        """
        Selecciona una acción basándose en la política actual.
        
        Args:
            state: Estado del entorno
            training: Si estamos en modo entrenamiento o evaluación
            
        Returns:
            Acción seleccionada como índice en la lista eligible_ops
        """
        # Guardar estado para entrenamiento si estamos en ese modo
        if training:
            self.saved_states.append(state)
        
        # Preprocesar estado
        inputs = self.preprocess_state(state)
        action_mask = inputs[-1]  # La máscara siempre es el último elemento
        
        if training:
            self.saved_masks.append(action_mask)
        
        # Obtener puntuaciones y valor del estado del modelo
        with torch.no_grad():
            if self.model_type == 'gnn':
                node_features, edge_index, edge_features, mask = inputs
                action_scores, state_value = self.model(node_features, edge_index, edge_features, mask)
            elif self.model_type == 'transformer':
                sequence_features, mask = inputs
                action_scores, state_value = self.model(sequence_features, mask)
            elif self.model_type == 'hybrid':
                node_features, edge_index, edge_features, mask = inputs
                action_scores, state_value = self.model(node_features, edge_index, edge_features, mask)
            
            # Filtrar acciones inválidas asignando probabilidad cero
            action_scores = action_scores.masked_fill(~action_mask, -1e9)
            
            # Convertir puntuaciones a distribución de probabilidad
            action_probs = F.softmax(action_scores, dim=0)
            
            # Crear distribución categórica
            dist = Categorical(action_probs)
            
            # Seleccionar acción: aleatoria en entrenamiento, greedy en evaluación
            if training:
                action_idx = dist.sample()
            else:
                action_idx = torch.argmax(action_probs)
            
            # Guardar log probabilidad y valor para entrenamiento
            if training:
                self.saved_log_probs.append(dist.log_prob(action_idx))
                self.saved_values.append(state_value.item())
                
                # Calcular entropía para monitoreo
                entropy = dist.entropy().item()
                self.entropies.append(entropy)
        
        # Convertir índice de acción a índice en eligible_ops
        action_idx = action_idx.item()
        
        # Para almacenar en la memoria, transformar el índice a (job_idx, op_idx)
        node_idx = action_idx
        job_idx = node_idx // self.num_machines
        op_idx = node_idx % self.num_machines
        
        # Guardar acción para entrenamiento
        if training:
            self.saved_actions.append((job_idx, op_idx))
        
        # Encontrar el índice correspondiente en eligible_ops
        eligible_ops = state.get('eligible_ops', [])
        if len(eligible_ops) == 0:
            return 0  # Si no hay operaciones elegibles, devolver un valor por defecto
            
        # Convertir el índice global del nodo seleccionado al índice en la lista eligible_ops
        # Esto es necesario porque el entorno espera un índice en eligible_ops, no una tupla (job_idx, op_idx)
        for i, job_id in enumerate(eligible_ops):
            if job_id == job_idx:
                return i
                
        # Si no se encuentra, devolver el primer índice (como fallback)
        return 0
    
    def update_policy(self):
        """
        Actualiza la política usando el algoritmo PPO.
        
        Esta función implementa el proceso de optimización de PPO,
        calculando ventajas, ratio de probabilidades y aplicando
        el recorte de objetivos según el algoritmo.
        
        Returns:
            Pérdidas de política, valor y total
        """
        # Convertir listas a tensores
        old_states = self.saved_states
        old_actions = self.saved_actions
        old_log_probs = torch.stack(self.saved_log_probs).to(self.device)
        old_values = torch.tensor(self.saved_values, dtype=torch.float).to(self.device)
        old_masks = self.saved_masks
        rewards = torch.tensor(self.rewards, dtype=torch.float).to(self.device)
        
        # Calcular retornos y ventajas usando GAE (Generalized Advantage Estimation)
        returns = []
        advantages = []
        next_value = 0  # Valor final es 0 (episodio terminado)
        next_advantage = 0
        
        for r, v in zip(reversed(rewards), reversed(old_values)):
            # Cálculo de retorno: R_t = r_t + gamma * R_{t+1}
            ret = r + self.gamma * next_value
            returns.insert(0, ret)
            
            # Cálculo de ventaja usando GAE
            delta = r + self.gamma * next_value - v
            advantage = delta + self.gamma * self.gae_lambda * next_advantage
            advantages.insert(0, advantage)
            
            next_value = v
            next_advantage = advantage
        
        # Convertir a tensores
        returns = torch.tensor(returns, dtype=torch.float).to(self.device)
        advantages = torch.tensor(advantages, dtype=torch.float).to(self.device)
        
        # Normalizar ventajas (mejora estabilidad)
        if self.advantage_normalization and len(advantages) > 1:
            advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        
        # Inicializar pérdidas acumuladas
        policy_loss_epoch = 0
        value_loss_epoch = 0
        total_loss_epoch = 0
        
        # Iteraciones de optimización de PPO
        for _ in range(self.K_epochs):
            # Recalcular log_probs y values con parámetros actuales
            current_log_probs = []
            current_values = []
            current_entropies = []
            
            for i, (state, action, mask) in enumerate(zip(old_states, old_actions, old_masks)):
                # Preprocesar estado
                inputs = self.preprocess_state(state)
                
                # Obtener puntuaciones y valor actuales
                if self.model_type == 'gnn':
                    node_features, edge_index, edge_features, _ = inputs
                    action_scores, state_value = self.model(node_features, edge_index, edge_features, mask)
                elif self.model_type == 'transformer':
                    sequence_features, _ = inputs
                    action_scores, state_value = self.model(sequence_features, mask)
                elif self.model_type == 'hybrid':
                    node_features, edge_index, edge_features, _ = inputs
                    action_scores, state_value = self.model(node_features, edge_index, edge_features, mask)
                
                # Filtrar acciones inválidas
                action_scores = action_scores.masked_fill(~mask, -1e9)
                
                # Convertir a distribución de probabilidad
                action_probs = F.softmax(action_scores, dim=0)
                dist = Categorical(action_probs)
                
                # Calcular log prob de la acción tomada
                action_idx = action[0] * self.num_machines + action[1]
                action_tensor = torch.tensor(action_idx, device=self.device)
                log_prob = dist.log_prob(action_tensor)
                
                # Guardar resultados
                current_log_probs.append(log_prob)
                current_values.append(state_value)
                current_entropies.append(dist.entropy())
            
            # Concatenar resultados
            current_log_probs = torch.stack(current_log_probs)
            current_values = torch.cat(current_values)
            current_entropies = torch.stack(current_entropies)
            
            # Calcular ratio para clipping
            ratios = torch.exp(current_log_probs - old_log_probs)
            
            # Calcular pérdidas surrogate de PPO
            surr1 = ratios * advantages
            surr2 = torch.clamp(ratios, 1 - self.eps_clip, 1 + self.eps_clip) * advantages
            
            # Pérdida de política (objetivo a maximizar, por eso el signo negativo)
            policy_loss = -torch.min(surr1, surr2).mean()
            
            # Pérdida de función de valor (MSE entre valores actuales y retornos objetivo)
            value_loss = F.mse_loss(current_values, returns)
            
            # Regularización de entropía (fomenta exploración)
            entropy_loss = -current_entropies.mean() * self.entropy_coef
            
            # Pérdida total
            total_loss = policy_loss + 0.5 * value_loss + entropy_loss
            
            # Optimización
            self.optimizer.zero_grad()
            total_loss.backward()
            
            # Recorte de gradiente opcional
            if self.use_grad_clip:
                nn.utils.clip_grad_norm_(self.model.parameters(), 0.5)
            
            self.optimizer.step()
            
            # Acumular pérdidas
            policy_loss_epoch += policy_loss.item()
            value_loss_epoch += value_loss.item()
            total_loss_epoch += total_loss.item()
        
        # Promediar pérdidas por época
        policy_loss_avg = policy_loss_epoch / self.K_epochs
        value_loss_avg = value_loss_epoch / self.K_epochs
        total_loss_avg = total_loss_epoch / self.K_epochs
        
        # Guardar pérdidas para análisis
        self.policy_losses.append(policy_loss_avg)
        self.value_losses.append(value_loss_avg)
        self.total_losses.append(total_loss_avg)
        
        # Registrar métricas si hay un logger
        if self.csv_logger:
            self.csv_logger.log_metrics({
                'policy_loss': policy_loss_avg,
                'value_loss': value_loss_avg,
                'total_loss': total_loss_avg,
                'entropy': sum(self.entropies) / len(self.entropies) if self.entropies else 0
            })
        
        # Limpiar memorias
        self.rewards.clear()
        self.saved_log_probs.clear()
        self.saved_values.clear()
        self.saved_actions.clear()
        self.saved_states.clear()
        self.saved_masks.clear()
        self.entropies.clear()
        
        return policy_loss_avg, value_loss_avg, total_loss_avg
    
    def train(self, episodes=1000, early_stopping=True, patience=50, 
              min_improvement=0.01, dynamic_entropy=True, verbose=True):
        """
        Entrena al agente durante un número específico de episodios.
        
        Args:
            episodes: Número de episodios de entrenamiento
            early_stopping: Si se debe usar early stopping
            patience: Número de episodios sin mejora para early stopping
            min_improvement: Mejora mínima requerida como fracción
            dynamic_entropy: Si se debe ajustar dinámicamente la entropía
            verbose: Si se debe mostrar información detallada durante entrenamiento
            
        Returns:
            Historial de makespan durante el entrenamiento
        """
        start_time = time.time()
        best_makespan = float('inf')
        episodes_without_improvement = 0
        entropy_decay_factor = 0.9995  # Factor para reducir entropía gradualmente
        
        # Registrar inicio de entrenamiento
        logger.info(f"Iniciando entrenamiento por {episodes} episodios...")
        
        for episode in range(1, episodes + 1):
            # Reiniciar entorno
            state = self.env.reset()
            episode_reward = 0
            episode_length = 0
            done = False
            
            # Ejecutar episodio
            while not done:
                # Seleccionar acción y ejecutarla
                action = self.select_action(state)
                next_state, reward, done, info = self.env.step(action)
                
                # Guardar recompensa
                self.rewards.append(reward)
                
                # Actualizar estado
                state = next_state
                
                # Acumular recompensa y longitud
                episode_reward += reward
                episode_length += 1
            
            # Registrar métricas del episodio
            makespan = info.get('makespan', float('inf'))
            self.makespan_history.append(makespan)
            self.training_makespan_history.append(makespan)
            self.episode_rewards.append(episode_reward)
            self.episode_lengths.append(episode_length)
            self.total_episodes += 1
            
            # Actualizar mejor solución
            if makespan < self.best_makespan:
                improvement = 0 if self.best_makespan == float('inf') else (self.best_makespan - makespan) / self.best_makespan
                self.best_makespan = makespan
                self.best_schedule = info.get('schedule')
                episodes_without_improvement = 0
                
                # Guardar mejor modelo
                self.best_model_state = {
                    'model': self.model.state_dict(),
                    'optimizer': self.optimizer.state_dict(),
                    'makespan': makespan,
                    'episode': episode
                }
                
                # Registrar mejora significativa
                if improvement >= min_improvement:
                    logger.info(f"Episodio {episode}: Nuevo mejor makespan: {makespan} (mejora: {improvement:.2%})")
            else:
                episodes_without_improvement += 1
            
            # Añadir mejor makespan al historial
            self.best_makespan_history.append(self.best_makespan)
            
            # Actualizar política
            policy_loss, value_loss, total_loss = self.update_policy()
            
            # Ajustar entropía si está habilitado
            if dynamic_entropy:
                self.entropy_coef = max(0.001, self.entropy_coef * entropy_decay_factor)
            
            # Ajustar tasa de aprendizaje si está habilitado
            if self.use_lr_decay:
                # Reducción lineal hasta 10% del valor inicial
                progress = min(1.0, episode / episodes)
                lr = self.lr * (1.0 - 0.9 * progress)
                for param_group in self.optimizer.param_groups:
                    param_group['lr'] = lr
            
            # Registrar progreso periódicamente
            if verbose and episode % 10 == 0:
                elapsed = time.time() - start_time
                logger.info(f"Episodio {episode}/{episodes} - Makespan: {makespan} - Mejor: {self.best_makespan} "
                           f"- Pérdida: {total_loss:.4f} - Tiempo: {elapsed:.1f}s")
                
                # Registrar métricas adicionales para análisis
                if self.csv_logger:
                    self.csv_logger.log_metrics({
                        'episode': episode,
                        'makespan': makespan,
                        'best_makespan': self.best_makespan,
                        'episode_reward': episode_reward,
                        'episode_length': episode_length,
                        'entropy_coef': self.entropy_coef,
                        'learning_rate': self.optimizer.param_groups[0]['lr'],
                        'training_time': elapsed
                    })
            
            # Comprobar early stopping
            if early_stopping and episodes_without_improvement >= patience:
                logger.info(f"Early stopping activado después de {patience} episodios sin mejora")
                break
        
        # Registrar fin del entrenamiento
        total_time = time.time() - start_time
        logger.info(f"Entrenamiento completado en {total_time:.2f} segundos. "
                    f"Mejor makespan: {self.best_makespan}")
        
        # Restaurar al mejor modelo si existe
        if self.best_model_state:
            logger.info("Restaurando el mejor modelo encontrado...")
            self.model.load_state_dict(self.best_model_state['model'])
            self.optimizer.load_state_dict(self.best_model_state['optimizer'])
        
        return self.training_makespan_history

    def evaluate(self, num_episodes=10):
        """
        Evalúa el rendimiento del agente en un conjunto de episodios.
        
        Args:
            num_episodes: Número de episodios para evaluación
            
        Returns:
            Dict con resultados de evaluación (makespan promedio, mejor, etc)
        """
        logger.info(f"Iniciando evaluación con {num_episodes} episodios...")
        start_time = time.time()
        
        makespans = []
        rewards = []
        
        for episode in range(1, num_episodes + 1):
            state = self.env.reset()
            episode_reward = 0
            done = False
            
            while not done:
                # Seleccionar acción en modo evaluación (determinístico)
                action = self.select_action(state, training=False)
                next_state, reward, done, info = self.env.step(action)
                
                episode_reward += reward
                state = next_state
            
            # Registrar métricas
            makespan = info.get('makespan', float('inf'))
            makespans.append(makespan)
            rewards.append(episode_reward)
            
            logger.info(f"Episodio {episode}/{num_episodes} - Makespan: {makespan}")
        
        # Calcular estadísticas
        avg_makespan = sum(makespans) / len(makespans)
        best_makespan = min(makespans)
        worst_makespan = max(makespans)
        avg_reward = sum(rewards) / len(rewards)
        
        eval_time = time.time() - start_time
        
        results = {
            'avg_makespan': avg_makespan,
            'best_makespan': best_makespan,
            'worst_makespan': worst_makespan,
            'std_makespan': np.std(makespans),
            'avg_reward': avg_reward,
            'evaluation_time': eval_time
        }
        
        logger.info(f"Evaluación completada en {eval_time:.2f} segundos")
        logger.info(f"Makespan promedio: {avg_makespan:.2f}, Mejor: {best_makespan}, Peor: {worst_makespan}")
        
        return results
    
    def save_checkpoint(self, path=None):
        """
        Guarda el estado actual del agente en un archivo.
        
        Args:
            path: Ruta del archivo donde guardar el checkpoint
        """
        import os
        
        if path is None:
            # Usar directorio de checkpoints predeterminado
            from jobshop_rl.utils.path_utils import get_checkpoint_path
            checkpoint_path = get_checkpoint_path(f"checkpoint_{self.model_type}.pt")
        else:
            # Ruta personalizada, guardar directamente ahí
            checkpoint_path = path
            
            # Asegurarse de que el directorio padre exista
            checkpoint_dir = os.path.dirname(checkpoint_path)
            if checkpoint_dir:
                os.makedirs(checkpoint_dir, exist_ok=True)
            
        checkpoint = {
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'model_type': self.model_type,
            'best_makespan': self.best_makespan,
            'best_schedule': self.best_schedule,
            'makespan_history': self.makespan_history,
            'training_makespan_history': self.training_makespan_history,
            'total_episodes': self.total_episodes if hasattr(self, 'total_episodes') else 0
        }
        
        # Guardar el checkpoint
        self.checkpoint_manager.save_checkpoint(checkpoint, checkpoint_path)
        logger.info(f"Checkpoint guardado en: {checkpoint_path}")
        
        return checkpoint_path
        
    def load_checkpoint(self, path):
        """
        Carga un modelo desde un checkpoint.
        
        Args:
            path: Ruta al archivo de checkpoint
            
        Returns:
            True si se cargó correctamente, False en caso contrario
        """
        try:
            checkpoint = self.checkpoint_manager.load_checkpoint(path)
            
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            
            # Cargar métricas si existen
            if 'best_makespan' in checkpoint:
                self.best_makespan = checkpoint['best_makespan']
            if 'best_schedule' in checkpoint:
                self.best_schedule = checkpoint['best_schedule']
            if 'makespan_history' in checkpoint:
                self.makespan_history = checkpoint['makespan_history']
            if 'training_makespan_history' in checkpoint:
                self.training_makespan_history = checkpoint['training_makespan_history']
            if 'total_episodes' in checkpoint:
                self.total_episodes = checkpoint['total_episodes']
                
            logger.info(f"Checkpoint cargado desde: {path}")
            logger.info(f"Mejor makespan cargado: {self.best_makespan}")
            
            return True
        except Exception as e:
            logger.error(f"Error al cargar checkpoint: {e}")
            return False
            
    def plot_training_history(self, optimal_makespan: Optional[int] = None):
        """
        Visualiza la evolución del makespan durante el entrenamiento.
        
        Args:
            optimal_makespan: Valor óptimo de makespan para referencia (opcional)
            
        Returns:
            Figura de matplotlib con la visualización
        """
        return plot_makespan_history(
            makespan_history=self.training_makespan_history,
            title='Evolución del Makespan durante el entrenamiento (GNN)',
            optimal_makespan=optimal_makespan
        )

    def plot_reward_history(self):
        """
        Visualiza la evolución de las recompensas durante el entrenamiento.
        
        Returns:
            Figura de matplotlib con la visualización
        """
        return plot_makespan_history(
            makespan_history=self.episode_rewards,
            title='Evolución de la recompensa durante el entrenamiento (GNN)',
            optimal_makespan=None  # No hay valor óptimo para recompensas
        )

    def plot_losses(self):
        """
        Visualiza la evolución de las pérdidas durante el entrenamiento.
        
        Returns:
            Figura de matplotlib con la visualización
        """
        if not self.policy_losses or not self.value_losses:
            return None
            
        # Crear un diccionario con las métricas para usar plot_training_metrics
        metrics = {
            'policy_loss': self.policy_losses,
            'value_loss': self.value_losses,
            'total_loss': self.total_losses if hasattr(self, 'total_losses') else []
        }
        
        return plot_training_metrics(metrics)

    def plot_exploration_history(self):
        """
        Visualiza la evolución del parámetro epsilon (exploración) durante el entrenamiento.
        
        Returns:
            Figura de matplotlib con la visualización
        """
        if hasattr(self, 'entropy_history'):
            history = self.entropy_history
        elif hasattr(self, 'entropies'):
            # Calcular promedio de entropía por episodio
            history = []
            episode_entropies = []
            for entropy in self.entropies:
                episode_entropies.append(entropy)
                if len(episode_entropies) >= self.episode_lengths[-1]:
                    history.append(sum(episode_entropies) / len(episode_entropies))
                    episode_entropies = []
        else:
            return None
        
        return plot_makespan_history(
            makespan_history=history,
            title='Evolución del parámetro de exploración (entropía)',
            optimal_makespan=None
        )
        
    def plot_best_solution_makespan(self, optimal_makespan: Optional[int] = None):
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
            title='Evolución del Makespan de la Mejor Solución (GNN)',
            optimal_makespan=optimal_makespan
        )
        
    def evaluate_policy(self, num_episodes=1) -> Tuple[float, List[Dict], List[float], float]:
        """
        Evalúa la política actual en un episodio completo.
        (Método compatible con la interfaz del PPOAgent clásico)
        
        Args:
            num_episodes: Número de episodios a evaluar (por defecto 1)
            
        Returns:
            Tuple[float, List[Dict], List[float], float]: 
                - makespan (float)
                - schedule (List[Dict])
                - makespan_history (List[float])
                - execution_time (float)
        """
        # Llamar al método evaluate existente
        eval_results = self.evaluate(num_episodes=num_episodes)
        
        # Extraer los datos necesarios del resultado
        makespan = eval_results.get('best_makespan', float('inf'))
        
        # Obtener historial del último episodio de evaluación (puede no estar disponible)
        makespan_history = []
        execution_time = eval_results.get('evaluation_time', 0.0)
        
        # Intentar reconstruir el schedule a partir del último episodio de evaluación
        # Esto es una aproximación, ya que el método evaluate no devuelve el schedule directamente
        schedule = self.best_schedule if makespan == self.best_makespan else []
        
        return makespan, schedule, makespan_history, execution_time
        
    def save_best_checkpoint(self):
        """
        Guarda el mejor modelo encontrado durante el entrenamiento.
        """
        if self.best_model_state is None:
            logger.warning("No hay mejor modelo para guardar.")
            return None
        
        path = f"best_{self.model_type}_makespan_{int(self.best_makespan)}.pt"
        checkpoint_path = get_checkpoint_path(path)
        
        checkpoint = {
            'model_state_dict': self.best_model_state['model'],
            'optimizer_state_dict': self.best_model_state['optimizer'],
            'model_type': self.model_type,
            'hidden_dim': self.model.hidden_dim if hasattr(self.model, 'hidden_dim') else None,
            'best_makespan': self.best_makespan,
            'best_schedule': self.best_schedule,
            'episode': self.best_model_state.get('episode', 0)
        }
        
        self.checkpoint_manager.save_checkpoint(checkpoint, checkpoint_path)
        logger.info(f"Mejor modelo guardado en: {checkpoint_path} (makespan: {self.best_makespan})")
        
        return checkpoint_path