"""
Utilidades de entrenamiento para manejar problemas grandes.
Incluye gradient accumulation, warmup de learning rate, y gestión de batch size.
"""

import torch
import numpy as np
from typing import List, Dict, Tuple, Optional
import logging

logger = logging.getLogger("JobShopRL.TrainingUtils")


class GradientAccumulator:
    """
    Gestiona la acumulación de gradientes para entrenar con batches efectivos más grandes.
    """
    
    def __init__(self,
                 accumulation_steps: int,
                 models: List[torch.nn.Module],
                 optimizers: List[torch.optim.Optimizer],
                 max_grad_norm: Optional[float] = None):
        """
        Args:
            accumulation_steps: Número de pasos de acumulación antes de actualizar
            models: Lista de modelos a entrenar
            optimizers: Lista de optimizadores correspondientes
            max_grad_norm: Si se especifica, aplica clipping de gradientes
                antes de cada actualización de pesos
        """
        self.accumulation_steps = accumulation_steps
        self.models = models
        self.optimizers = optimizers
        self.max_grad_norm = max_grad_norm
        self.current_step = 0
        
    def zero_grad(self):
        """Limpia los gradientes solo cuando es apropiado."""
        if self.current_step == 0:
            for optimizer in self.optimizers:
                optimizer.zero_grad()
                
    def backward(self, loss: torch.Tensor):
        """
        Realiza backward con escalado apropiado del loss.
        
        Args:
            loss: Pérdida a propagar
        """
        # Escalar la pérdida por el número de pasos de acumulación
        scaled_loss = loss / self.accumulation_steps
        scaled_loss.backward()
        
    def step(self) -> bool:
        """
        Incrementa el contador y actualiza los optimizadores si es necesario.

        Returns:
            bool: True si se realizó una actualización de pesos
        """
        self.current_step += 1

        if self.current_step >= self.accumulation_steps:
            self._apply_step()
            return True

        return False

    def _apply_step(self):
        """Aplica los gradientes acumulados: clipping, step y reset del ciclo."""
        if self.max_grad_norm is not None:
            for model in self.models:
                torch.nn.utils.clip_grad_norm_(model.parameters(), self.max_grad_norm)
        for optimizer in self.optimizers:
            optimizer.step()
        self.current_step = 0

    def flush(self):
        """
        Aplica los gradientes parciales pendientes al final de un ciclo de
        actualización. Sin esto, los gradientes de un ciclo incompleto quedan
        acumulados y contaminan la primera actualización del episodio siguiente.
        """
        if self.current_step > 0:
            self._apply_step()
        
    def should_accumulate(self) -> bool:
        """Indica si debemos acumular gradientes."""
        return self.accumulation_steps > 1


class WarmupScheduler:
    """
    Implementa warmup de learning rate para estabilizar el entrenamiento inicial.
    """
    
    def __init__(self,
                 optimizer: torch.optim.Optimizer,
                 warmup_episodes: int,
                 base_lr: float,
                 warmup_type: str = "quadratic"):
        """
        Args:
            optimizer: Optimizador a controlar
            warmup_episodes: Número de episodios para warmup
            base_lr: Learning rate base después del warmup
            warmup_type: Tipo de warmup ('linear', 'quadratic', 'exponential')
        """
        self.optimizer = optimizer
        self.warmup_episodes = warmup_episodes
        self.base_lr = base_lr
        self.warmup_type = warmup_type
        self.current_episode = 0
        
    def step(self, episode: Optional[int] = None):
        """
        Actualiza el learning rate según el episodio actual.
        
        Args:
            episode: Número de episodio (usa contador interno si es None)
        """
        if episode is not None:
            self.current_episode = episode
        else:
            self.current_episode += 1
            
        if self.current_episode <= self.warmup_episodes:
            # Calcular factor de warmup
            progress = self.current_episode / self.warmup_episodes
            
            if self.warmup_type == "linear":
                warmup_factor = progress
            elif self.warmup_type == "quadratic":
                warmup_factor = progress ** 2
            elif self.warmup_type == "exponential":
                warmup_factor = 2 ** (10 * (progress - 1))  # De 0.001 a 1
            else:
                warmup_factor = progress
                
            # Aplicar el learning rate
            current_lr = self.base_lr * warmup_factor
            for param_group in self.optimizer.param_groups:
                param_group['lr'] = current_lr
                
            if self.current_episode % 10 == 0:
                logger.debug(f"Warmup episodio {self.current_episode}: lr={current_lr:.6f}")
                
    def is_warming_up(self) -> bool:
        """Indica si todavía estamos en fase de warmup."""
        return self.current_episode < self.warmup_episodes


class BatchSizeManager:
    """
    Gestiona el tamaño de batch mínimo garantizado para diferentes tamaños de problema.
    """
    
    def __init__(self, problem_size: int):
        """
        Args:
            problem_size: Tamaño del problema (num_jobs * num_machines)
        """
        self.problem_size = problem_size
        
        # Determinar configuración según el tamaño del problema
        if problem_size <= 100:  # ≤10x10
            self.min_batch_size = 4
            self.target_batch_size = 8
            self.accumulation_steps = 1
        elif problem_size <= 400:  # ≤20x20
            self.min_batch_size = 8
            self.target_batch_size = 16
            self.accumulation_steps = 1
        elif problem_size <= 2000:  # ≤100x20 (incluido)
            self.min_batch_size = 16
            self.target_batch_size = 32
            self.accumulation_steps = 4
        else:  # Problemas extremadamente grandes
            self.min_batch_size = 32
            self.target_batch_size = 64
            self.accumulation_steps = 8
            
        logger.info(f"BatchSizeManager configurado para problema de tamaño {problem_size}: "
                   f"min_batch={self.min_batch_size}, target_batch={self.target_batch_size}, "
                   f"accumulation_steps={self.accumulation_steps}")
                   
    def should_wait_for_batch(self, current_batch_size: int) -> bool:
        """
        Determina si debemos esperar a acumular más ejemplos.
        
        Args:
            current_batch_size: Tamaño actual del batch
            
        Returns:
            bool: True si debemos esperar
        """
        return current_batch_size < self.min_batch_size
        
    def get_accumulation_steps(self) -> int:
        """Retorna el número de pasos de acumulación recomendados."""
        return self.accumulation_steps
        
    def create_mini_batches(self, 
                           data: List[any], 
                           shuffle: bool = True) -> List[List[any]]:
        """
        Crea mini-batches del tamaño apropiado.
        
        Args:
            data: Lista de datos a dividir en batches
            shuffle: Si mezclar los datos antes de crear batches
            
        Returns:
            Lista de mini-batches
        """
        n_samples = len(data)
        indices = np.arange(n_samples)
        
        if shuffle:
            np.random.shuffle(indices)
            
        # Usar el target batch size pero asegurar el mínimo
        batch_size = max(self.min_batch_size, 
                        min(self.target_batch_size, n_samples // 2))
        
        mini_batches = []
        for start_idx in range(0, n_samples, batch_size):
            end_idx = min(start_idx + batch_size, n_samples)
            batch_indices = indices[start_idx:end_idx]
            
            # Solo incluir el batch si cumple el tamaño mínimo
            if len(batch_indices) >= self.min_batch_size:
                mini_batches.append([data[i] for i in batch_indices])
                
        return mini_batches


def reset_batch_norm_stats(model: torch.nn.Module, momentum: float = 0.01):
    """
    Resetea las estadísticas de BatchNorm en un modelo.
    
    Args:
        model: Modelo que contiene capas BatchNorm
        momentum: Nuevo valor de momentum a establecer
    """
    for module in model.modules():
        if isinstance(module, (torch.nn.BatchNorm1d, torch.nn.BatchNorm2d)):
            module.reset_running_stats()
            module.momentum = momentum
            logger.debug(f"Reset BatchNorm stats en {module.__class__.__name__}")
            

def configure_for_problem_size(
    problem_size: int
) -> Dict[str, any]:
    """
    Retorna configuración recomendada según el tamaño del problema.
    
    Args:
        problem_size: Tamaño del problema (num_jobs * num_machines)
        
    Returns:
        Diccionario con configuración recomendada
    """
    config = {
        "use_advanced_networks": False,
        "use_gradient_accumulation": False,
        "use_warmup": False,
        "warmup_episodes": 0,
        "dropout_rate": 0.1,
        "batch_norm_momentum": 0.1,
        "min_batch_size": 4,
        "accumulation_steps": 1
    }
    
    if problem_size > 400:  # >20x20
        config.update({
            "use_advanced_networks": True,
            "dropout_rate": 0.15,
            "batch_norm_momentum": 0.05,
            "min_batch_size": 8
        })
        
    if problem_size > 750:  # ≥50x15 (incluye 50x20 y 100x20)
        config.update({
            "use_gradient_accumulation": True,
            "use_warmup": True,
            "warmup_episodes": 20,
            "dropout_rate": 0.2,
            "batch_norm_momentum": 0.01,
            "min_batch_size": 16,
            "accumulation_steps": 4
        })
        
    return config
