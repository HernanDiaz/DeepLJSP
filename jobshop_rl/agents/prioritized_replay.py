"""
Prioritized Experience Replay para PPO.

Guarda episodios completos y los prioriza por calidad (makespan).
Permite re-entrenar con los mejores episodios encontrados.
"""

import random
import numpy as np
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
from collections import deque
import torch


@dataclass
class Episode:
    """Representa un episodio completo guardado."""
    states: List[Dict]
    actions: List[int]
    rewards: List[float]
    log_probs: List[torch.Tensor]
    features: List[torch.Tensor]
    values: List[float]
    makespan_midpoint: float
    total_reward: float
    
    def __len__(self) -> int:
        return len(self.states)


class PrioritizedEpisodeReplay:
    """
    Buffer de replay que guarda episodios completos priorizados por makespan.
    
    Características:
    - Guarda los N mejores episodios encontrados
    - Prioriza episodios con menor makespan
    - Permite sampling para re-entrenamiento
    """
    
    def __init__(self, capacity: int = 20, alpha: float = 0.6):
        """
        Args:
            capacity: Número máximo de episodios a guardar
            alpha: Exponente de priorización (0 = uniforme, 1 = greedy)
        """
        self.capacity = capacity
        self.alpha = alpha
        self.episodes: List[Episode] = []
        self.best_makespan: float = float('inf')
        
    def add(self, episode: Episode) -> bool:
        """
        Añade un episodio al buffer si es suficientemente bueno.
        
        Returns:
            True si el episodio fue añadido
        """
        # Siempre añadir si no está lleno
        if len(self.episodes) < self.capacity:
            self.episodes.append(episode)
            self._sort_episodes()
            self._update_best()
            return True
        
        # Si está lleno, solo añadir si es mejor que el peor guardado
        worst_makespan = self.episodes[-1].makespan_midpoint
        if episode.makespan_midpoint < worst_makespan:
            self.episodes[-1] = episode  # Reemplazar el peor
            self._sort_episodes()
            self._update_best()
            return True
        
        return False
    
    def _sort_episodes(self) -> None:
        """Ordena episodios por makespan (menor = mejor = primero)"""
        self.episodes.sort(key=lambda e: e.makespan_midpoint)
    
    def _update_best(self) -> None:
        """Actualiza el mejor makespan visto"""
        if self.episodes:
            self.best_makespan = self.episodes[0].makespan_midpoint
    
    def sample(self, n: int = 5, beta: float = 0.4) -> List[Tuple[Episode, float]]:
        """
        Muestrea episodios con priorización.
        
        Los episodios con menor makespan tienen mayor probabilidad.
        
        Args:
            n: Número de episodios a muestrear
            beta: Exponente para importance sampling weights
            
        Returns:
            Lista de (episodio, importance_weight)
        """
        if not self.episodes:
            return []
        
        n = min(n, len(self.episodes))
        
        # Calcular prioridades (invertir makespan para que menor = mayor prioridad)
        # Normalizar respecto al mejor
        priorities = []
        for ep in self.episodes:
            # Ratio: mejor_makespan / este_makespan (cercano a 1 para los mejores)
            ratio = self.best_makespan / max(ep.makespan_midpoint, 1)
            priorities.append(ratio ** self.alpha)
        
        # Normalizar a probabilidades
        total = sum(priorities)
        probs = [p / total for p in priorities]
        
        # Muestrear
        indices = np.random.choice(len(self.episodes), size=n, replace=False, p=probs)
        
        # Calcular importance sampling weights
        N = len(self.episodes)
        results = []
        for idx in indices:
            # Weight = (1 / (N * P(i))) ^ beta, normalizado
            weight = (1.0 / (N * probs[idx])) ** beta
            results.append((self.episodes[idx], weight))
        
        # Normalizar weights
        max_weight = max(w for _, w in results)
        results = [(ep, w / max_weight) for ep, w in results]
        
        return results
    
    def get_best_episodes(self, n: int = 5) -> List[Episode]:
        """Retorna los N mejores episodios (sin sampling)"""
        return self.episodes[:min(n, len(self.episodes))]
    
    def __len__(self) -> int:
        return len(self.episodes)
    
    def is_ready(self, min_episodes: int = 5) -> bool:
        """Verifica si hay suficientes episodios para replay"""
        return len(self.episodes) >= min_episodes
    
    def get_stats(self) -> Dict[str, float]:
        """Retorna estadísticas del buffer"""
        if not self.episodes:
            return {"count": 0, "best": float('inf'), "worst": float('inf'), "mean": 0}
        
        makespans = [e.makespan_midpoint for e in self.episodes]
        return {
            "count": len(self.episodes),
            "best": min(makespans),
            "worst": max(makespans),
            "mean": sum(makespans) / len(makespans)
        }


class ReplayEnhancedPPOMemory:
    """
    Memoria PPO mejorada con replay de episodios buenos.
    
    Combina:
    1. Memoria on-policy estándar para el episodio actual
    2. Buffer de replay con los mejores episodios
    """
    
    def __init__(self, gamma: float = 0.99, gae_lambda: float = 0.95,
                 advantage_normalization: bool = True,
                 replay_capacity: int = 20,
                 replay_ratio: float = 0.3,
                 predict_makespan: bool = True):
        """
        Args:
            gamma: Factor de descuento
            gae_lambda: Lambda para GAE
            advantage_normalization: Si normalizar advantages
            replay_capacity: Capacidad del buffer de replay
            replay_ratio: Proporción de datos de replay vs on-policy
            predict_makespan: Si el crítico predice makespan (True) o returns (False)
        """
        self.gamma = gamma
        self.gae_lambda = gae_lambda
        self.advantage_normalization = advantage_normalization
        self.replay_ratio = replay_ratio
        self.predict_makespan = predict_makespan
        
        # Memoria on-policy (episodio actual)
        self.states: List[Dict] = []
        self.actions: List[int] = []
        self.log_probs: List[torch.Tensor] = []
        self.rewards: List[float] = []
        self.features: List[torch.Tensor] = []
        self.is_terminals: List[bool] = []
        self.values: List[float] = []
        
        # Buffer de replay
        self.replay_buffer = PrioritizedEpisodeReplay(capacity=replay_capacity)
        
        # Tracking del episodio actual
        self.current_episode_reward = 0.0
        self.final_makespan: Optional[float] = None  # Para modo makespan
    
    def store(self, state: Dict, action: int, log_prob: torch.Tensor,
              reward: float, features: torch.Tensor, is_terminal: bool,
              value: float) -> None:
        """Almacena una transición del episodio actual"""
        self.states.append(state)
        self.actions.append(action)
        self.log_probs.append(log_prob)
        self.rewards.append(reward)
        self.features.append(features)
        self.is_terminals.append(is_terminal)
        self.values.append(value)
        self.current_episode_reward += reward
    
    def finish_episode(self, makespan_midpoint: float) -> bool:
        """
        Finaliza el episodio actual y lo añade al buffer de replay si es bueno.
        
        Args:
            makespan_midpoint: Midpoint del makespan del episodio
            
        Returns:
            True si el episodio fue añadido al buffer de replay
        """
        if not self.states:
            return False
        
        # Crear episodio
        episode = Episode(
            states=list(self.states),
            actions=list(self.actions),
            rewards=list(self.rewards),
            log_probs=[lp.clone() for lp in self.log_probs],
            features=[f.clone() for f in self.features],
            values=list(self.values),
            makespan_midpoint=makespan_midpoint,
            total_reward=self.current_episode_reward
        )
        
        # Intentar añadir al buffer
        added = self.replay_buffer.add(episode)
        
        # Reset reward tracking
        self.current_episode_reward = 0.0
        
        return added
    
    def set_final_makespan(self, makespan: float):
        """
        Establece el makespan final del episodio.
        
        Usado cuando predict_makespan=True para entrenar el crítico.
        """
        self.final_makespan = makespan
    
    def clear(self) -> None:
        """Limpia la memoria on-policy (no el buffer de replay)"""
        self.states.clear()
        self.actions.clear()
        self.log_probs.clear()
        self.rewards.clear()
        self.features.clear()
        self.is_terminals.clear()
        self.values.clear()
        self.current_episode_reward = 0.0
        self.final_makespan = None
    
    def is_empty(self) -> bool:
        """Verifica si la memoria on-policy está vacía"""
        return len(self.states) == 0
    
    def calculate_gae(self, rewards: List[float], values: List[float], 
                      is_terminals: List[bool],
                      final_makespan: Optional[float] = None) -> Tuple[List[float], List[float]]:
        """
        Calcula Generalized Advantage Estimation.
        
        Soporta dos modos:
        1. Tradicional (final_makespan=None): Returns = Σ γ^t r_t
        2. Makespan (final_makespan!=None): Returns = makespan final
        
        Args:
            rewards: Lista de rewards
            values: Lista de valores predichos por el crítico
            is_terminals: Lista de flags de terminal
            final_makespan: Makespan final (solo para modo makespan)
        
        Returns:
            (returns, advantages)
        """
        advantages = []
        returns = []
        gae = 0
        
        if self.predict_makespan and final_makespan is not None:
            # MODO MAKESPAN: Crítico predice E[C_max | s]
            # Returns son todos iguales al makespan final
            # GAE se calcula con rewards + diferencia en predicciones
            for t in reversed(range(len(rewards))):
                if is_terminals[t]:
                    next_value = final_makespan
                    delta = rewards[t]  # En el último paso, delta = reward_final
                else:
                    next_value = values[t + 1] if t + 1 < len(values) else final_makespan
                    delta = rewards[t] + self.gamma * (next_value - values[t])
                
                gae = delta + self.gamma * self.gae_lambda * gae
                
                advantages.insert(0, gae)
                returns.insert(0, final_makespan)  # Target = makespan para todos
        else:
            # MODO TRADICIONAL: Crítico predice E[Σ γ^t r_t | s]
            for t in reversed(range(len(rewards))):
                if is_terminals[t]:
                    next_value = 0
                    gae = 0
                else:
                    next_value = values[t + 1] if t + 1 < len(values) else 0
                
                delta = rewards[t] + self.gamma * next_value - values[t]
                gae = delta + self.gamma * self.gae_lambda * gae
                
                advantages.insert(0, gae)
                returns.insert(0, gae + values[t])
        
        return returns, advantages
    
    def get_training_data(self, include_replay: bool = True) -> Dict[str, Any]:
        """
        Obtiene datos para entrenamiento, combinando on-policy y replay.
        
        Args:
            include_replay: Si incluir datos del buffer de replay
            
        Returns:
            Diccionario con todos los datos necesarios para entrenar
        """
        # Datos on-policy
        on_policy_returns, on_policy_advantages = self.calculate_gae(
            self.rewards, self.values, self.is_terminals,
            final_makespan=self.final_makespan  # Pasar makespan si está disponible
        )
        
        all_data = {
            'states': list(self.states),
            'actions': list(self.actions),
            'log_probs': list(self.log_probs),
            'features': list(self.features),
            'returns': on_policy_returns,
            'advantages': on_policy_advantages,
            'weights': [1.0] * len(self.states),  # Weight 1 para on-policy
            'is_replay': [False] * len(self.states)
        }
        
        # Añadir datos de replay si está habilitado y hay suficientes
        if include_replay and self.replay_buffer.is_ready(min_episodes=3):
            # Calcular cuántos ejemplos de replay añadir
            n_on_policy = len(self.states)
            n_replay_episodes = max(1, int(n_on_policy * self.replay_ratio / 50))  # Asumiendo ~50 steps/episodio
            
            # Muestrear episodios
            replay_samples = self.replay_buffer.sample(n=n_replay_episodes)
            
            for episode, weight in replay_samples:
                # Recalcular GAE para este episodio
                ep_returns, ep_advantages = self.calculate_gae(
                    episode.rewards, episode.values, 
                    [False] * (len(episode.rewards) - 1) + [True],
                    final_makespan=episode.makespan_midpoint  # Usar makespan del episodio
                )
                
                # Añadir datos
                all_data['states'].extend(episode.states)
                all_data['actions'].extend(episode.actions)
                all_data['log_probs'].extend(episode.log_probs)
                all_data['features'].extend(episode.features)
                all_data['returns'].extend(ep_returns)
                all_data['advantages'].extend(ep_advantages)
                all_data['weights'].extend([weight] * len(episode.states))
                all_data['is_replay'].extend([True] * len(episode.states))
        
        # Normalizar advantages si está habilitado
        if self.advantage_normalization and all_data['advantages']:
            adv_array = np.array(all_data['advantages'])
            adv_mean = adv_array.mean()
            adv_std = adv_array.std() + 1e-8
            all_data['advantages'] = ((adv_array - adv_mean) / adv_std).tolist()
        
        return all_data
    
    def get_replay_stats(self) -> Dict[str, float]:
        """Retorna estadísticas del buffer de replay"""
        return self.replay_buffer.get_stats()
