"""
Módulo para la gestión de memoria de experiencias del agente PPO.
"""

import torch
import numpy as np
from typing import List, Tuple, Dict, Any, Optional

class PPOMemory:
    """Clase para gestionar la memoria de experiencias del agente PPO"""
    
    def __init__(self, gamma: float = 0.99, gae_lambda: float = 0.95, 
                advantage_normalization: bool = True):
        # Buffer para almacenar experiencias
        self.states = []
        self.actions = []
        self.log_probs = []
        self.rewards = []
        self.features_list = []
        self.is_terminals = []
        self.values = []
        
        # Parámetros de configuración
        self.gamma = gamma
        self.gae_lambda = gae_lambda
        self.advantage_normalization = advantage_normalization
        
    def store(self, state: Dict, action: int, log_prob: torch.Tensor, reward: float, 
             features: torch.Tensor, is_terminal: bool, value: float):
        """Almacena una transición en la memoria"""
        self.states.append(state)
        self.actions.append(action)
        self.log_probs.append(log_prob)
        self.rewards.append(reward)
        self.features_list.append(features)
        self.is_terminals.append(is_terminal)
        self.values.append(value)
    
    def clear(self):
        """Limpia todos los buffers de memoria"""
        self.states.clear()
        self.actions.clear()
        self.log_probs.clear()
        self.rewards.clear()
        self.features_list.clear()
        self.is_terminals.clear()
        self.values.clear()
    
    def is_empty(self) -> bool:
        """Verifica si la memoria está vacía"""
        return len(self.states) == 0
    
    def get_tensors(self) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, List[torch.Tensor]]:
        """
        Calcula retornos y ventajas y devuelve los tensores necesarios para el entrenamiento.
        
        Returns:
            Tupla con (old_actions, old_log_probs, returns, advantages, features_list)
        """
        if self.is_empty():
            raise ValueError("La memoria está vacía, no se pueden calcular los tensores")
        
        if self.gae_lambda > 0:
            returns, advantages = self._calculate_gae()
            returns = torch.tensor(returns, dtype=torch.float32)
            advantages = torch.tensor(advantages, dtype=torch.float32)
        else:
            # Método tradicional de retornos descontados
            returns = self._calculate_returns()
            returns = torch.tensor(returns, dtype=torch.float32)
            
            # Calcular ventajas como retornos - valores
            value_tensor = torch.tensor(self.values, dtype=torch.float32)
            advantages = returns - value_tensor
            
        # Normalizar ventajas si está habilitado
        if self.advantage_normalization and len(advantages) > 1:
            advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
            
        old_actions = torch.tensor([a for a in self.actions], dtype=torch.int64)
        old_log_probs = torch.stack(self.log_probs)
        
        return old_actions, old_log_probs, returns, advantages, self.features_list
        
    def _calculate_gae(self) -> Tuple[List[float], List[float]]:
        """
        Calcula ventajas usando Generalized Advantage Estimation.
        
        Returns:
            Tupla con (retornos, ventajas)
        """
        gae = 0
        returns = []
        advantages = []
        
        for i in reversed(range(len(self.rewards))):
            if i == len(self.rewards) - 1 or self.is_terminals[i]:
                next_value = 0  # Si es terminal, no hay próximo estado
            else:
                next_value = self.values[i + 1]
                
            delta = self.rewards[i] + self.gamma * next_value * (1 - self.is_terminals[i]) - self.values[i]
            gae = delta + self.gamma * self.gae_lambda * (1 - self.is_terminals[i]) * gae
            
            returns.insert(0, gae + self.values[i])
            advantages.insert(0, gae)
            
        return returns, advantages
    
    def _calculate_returns(self) -> List[float]:
        """
        Calcula retornos descontados tradicionales.
        
        Returns:
            Lista de retornos descontados
        """
        returns = []
        discounted_reward = 0
        
        for reward, is_terminal in zip(reversed(self.rewards), reversed(self.is_terminals)):
            if is_terminal:
                discounted_reward = 0
            discounted_reward = reward + (self.gamma * discounted_reward)
            returns.insert(0, discounted_reward)
            
        return returns
