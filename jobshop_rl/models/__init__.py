"""
Paquete de modelos de datos y redes neuronales para JobShopRL.

Incluye soporte para intervalos en tiempos de procesamiento.
"""

from jobshop_rl.models.data_models import (
    Operation, 
    SchedulingStep, 
    StateFeatures, 
    OperationFeatures
)
from jobshop_rl.models.neural_models import PolicyNetwork, ValueNetwork
from jobshop_rl.models.interval import Interval, ensure_interval

__all__ = [
    'Operation',
    'SchedulingStep',
    'StateFeatures',
    'OperationFeatures',
    'PolicyNetwork',
    'ValueNetwork',
    'Interval',
    'ensure_interval'
]
