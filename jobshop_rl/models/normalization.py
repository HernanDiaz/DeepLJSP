"""
Módulo de normalización estabilizada para redes neuronales.
Implementa versiones mejoradas de BatchNorm para manejar problemas grandes de Job Shop.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple
import logging

logger = logging.getLogger("JobShopRL.Normalization")


class StabilizedBatchNorm1d(nn.Module):
    """
    BatchNorm estabilizado que maneja mejor casos edge como batch size pequeño.
    
    Características:
    - Momentum adaptativo según el tamaño del batch
    - Manejo especial para batch size = 1
    - Mayor epsilon para estabilidad numérica
    - Opción de usar Instance Normalization como fallback
    """
    
    def __init__(self, 
                 num_features: int, 
                 eps: float = 1e-3,
                 momentum: float = 0.01,
                 affine: bool = True,
                 track_running_stats: bool = True,
                 min_batch_size: int = 2):
        """
        Args:
            num_features: Número de características de entrada
            eps: Epsilon para estabilidad numérica (mayor que el default)
            momentum: Momentum para estadísticas running (menor que el default)
            affine: Si usar parámetros aprendibles gamma y beta
            track_running_stats: Si mantener estadísticas running
            min_batch_size: Tamaño mínimo de batch para usar BatchNorm
        """
        super(StabilizedBatchNorm1d, self).__init__()
        
        self.num_features = num_features
        self.eps = eps
        self.base_momentum = momentum
        self.affine = affine
        self.track_running_stats = track_running_stats
        self.min_batch_size = min_batch_size
        
        # Crear la capa BatchNorm base
        self.batch_norm = nn.BatchNorm1d(
            num_features=num_features,
            eps=eps,
            momentum=momentum,
            affine=affine,
            track_running_stats=track_running_stats
        )
        
        # LayerNorm como fallback para batch pequeño (más estable que InstanceNorm)
        self.layer_norm = nn.LayerNorm(
            normalized_shape=num_features,
            eps=eps,
            elementwise_affine=affine
        )
        
        # Contador para estadísticas de uso
        self.batch_norm_count = 0
        self.layer_norm_count = 0
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass con manejo adaptativo según el tamaño del batch.
        
        Args:
            x: Tensor de entrada [batch_size, num_features] o [num_features]
            
        Returns:
            Tensor normalizado
        """
        # Manejar caso de entrada 1D
        original_shape = x.shape
        if x.dim() == 1:
            x = x.unsqueeze(0)
            
        batch_size = x.size(0)
        
        # Decidir qué normalización usar
        if self.training and batch_size < self.min_batch_size:
            # En entrenamiento con batch pequeño, usar Layer Norm
            self.layer_norm_count += 1
            output = self.layer_norm(x)
            
            # Log ocasional para monitoreo
            if self.layer_norm_count % 100 == 0:
                logger.debug(f"Usando Layer Norm (batch_size={batch_size}). "
                           f"Conteo: LN={self.layer_norm_count}, BN={self.batch_norm_count}")
        else:
            # Usar BatchNorm con momentum adaptativo
            if self.training and batch_size < 32:
                # Reducir momentum para batches pequeños
                adaptive_momentum = self.base_momentum * (batch_size / 32.0)
                self.batch_norm.momentum = max(0.001, adaptive_momentum)
            else:
                self.batch_norm.momentum = self.base_momentum
                
            self.batch_norm_count += 1
            output = self.batch_norm(x)
            
        # Restaurar forma original si era necesario
        if len(original_shape) == 1:
            output = output.squeeze(0)
            
        return output
        
    def reset_running_stats(self):
        """Resetea las estadísticas running de BatchNorm."""
        self.batch_norm.reset_running_stats()
        self.batch_norm_count = 0
        self.layer_norm_count = 0
        
    def reset_parameters(self):
        """Resetea todos los parámetros aprendibles."""
        self.batch_norm.reset_parameters()
        if hasattr(self.layer_norm, 'reset_parameters'):
            self.layer_norm.reset_parameters()


class AdaptiveNormalization(nn.Module):
    """
    Capa de normalización adaptativa que puede cambiar entre BatchNorm y LayerNorm
    según las características del problema y el contexto de ejecución.
    """
    
    def __init__(self,
                 num_features: int,
                 problem_size: int,
                 eps: float = 1e-3,
                 affine: bool = True):
        """
        Args:
            num_features: Número de características
            problem_size: Tamaño del problema (num_jobs * num_machines)
            eps: Epsilon para estabilidad numérica
            affine: Si usar parámetros aprendibles
        """
        super(AdaptiveNormalization, self).__init__()
        
        self.num_features = num_features
        self.problem_size = problem_size
        
        # Siempre usar LayerNorm como fallback (más estable)
        self.fallback_norm = nn.LayerNorm(num_features, eps=eps, elementwise_affine=affine)
        
        # Determinar estrategia según el tamaño del problema
        if problem_size <= 400:  # Problemas pequeños (≤20x20)
            self.primary_norm = nn.BatchNorm1d(num_features, eps=eps, momentum=0.1, affine=affine)
            self.strategy = "small"
            self.min_batch_size = 2
        elif problem_size <= 2000:  # Problemas medianos-grandes (≤100x20, incluido)
            self.primary_norm = StabilizedBatchNorm1d(
                num_features, eps=eps, momentum=0.01, affine=affine, min_batch_size=4
            )
            self.strategy = "medium"
            self.min_batch_size = 4
        else:  # Problemas extremadamente grandes (>100x20)
            self.primary_norm = StabilizedBatchNorm1d(
                num_features, eps=eps*2, momentum=0.005, affine=affine, min_batch_size=8
            )
            self.strategy = "large"
            self.min_batch_size = 8
            
        logger.info(f"AdaptiveNormalization configurado para problema {self.strategy} "
                   f"(size={problem_size}, features={num_features})")
            
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass con selección adaptativa de normalización.
        
        Args:
            x: Tensor de entrada
            
        Returns:
            Tensor normalizado
        """
        # En entrenamiento, BatchNorm es inestable con batches pequeños:
        # usar LayerNorm. En evaluación la norma primaria usa las estadísticas
        # running acumuladas y es válida para cualquier tamaño de batch;
        # desviarse al fallback aplicaría una transformación nunca entrenada.
        if self.training and x.dim() == 2 and x.size(0) < self.min_batch_size:
            return self.fallback_norm(x)

        # Intentar usar la normalización primaria
        try:
            return self.primary_norm(x)
        except (RuntimeError, ValueError) as e:
            # Si falla por cualquier razón, usar fallback
            logger.debug(f"Primary norm failed: {e}. Using LayerNorm fallback.")
            return self.fallback_norm(x)
            
    def reset_stats(self):
        """Resetea las estadísticas de las capas de normalización."""
        if hasattr(self.primary_norm, 'reset_running_stats'):
            self.primary_norm.reset_running_stats()
        if isinstance(self.primary_norm, StabilizedBatchNorm1d):
            self.primary_norm.reset_running_stats()


def create_normalization_layer(
    num_features: int,
    problem_size: int,
    normalization_type: str = "adaptive",
    **kwargs
) -> nn.Module:
    """
    Factory function para crear la capa de normalización apropiada.
    
    Args:
        num_features: Número de características
        problem_size: Tamaño del problema
        normalization_type: Tipo de normalización ('adaptive', 'batch', 'layer', 'stabilized')
        **kwargs: Argumentos adicionales para la capa
        
    Returns:
        Capa de normalización
    """
    if normalization_type == "adaptive":
        return AdaptiveNormalization(num_features, problem_size, **kwargs)
    elif normalization_type == "stabilized":
        return StabilizedBatchNorm1d(num_features, **kwargs)
    elif normalization_type == "batch":
        # Para BatchNorm estándar, usar LayerNorm si es más seguro
        if problem_size > 400:
            logger.debug(f"Usando LayerNorm en lugar de BatchNorm para problema grande (size={problem_size})")
            return nn.LayerNorm(num_features, **kwargs)
        return nn.BatchNorm1d(num_features, **kwargs)
    elif normalization_type == "layer":
        return nn.LayerNorm(num_features, **kwargs)
    else:
        raise ValueError(f"Tipo de normalización no soportado: {normalization_type}")
