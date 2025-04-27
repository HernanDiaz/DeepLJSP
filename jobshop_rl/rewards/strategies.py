"""
Estrategias de recompensa para el entorno de Job Shop Scheduling.
Implementa el patrón Strategy para diferentes funciones de recompensa.

NOTA: Este archivo se mantiene por compatibilidad. Las implementaciones
se han movido a la estructura modular en los directorios:
  - jobshop_rl/rewards/strategies/
  - jobshop_rl/rewards/components/
"""

# Importar las clases desde la nueva estructura
from jobshop_rl.rewards.base import RewardStrategy
from jobshop_rl.rewards.strategies.basic import BasicRewardStrategy
from jobshop_rl.rewards.strategies.advanced import AdvancedRewardStrategy
from jobshop_rl.rewards.strategies.adaptive import AdaptiveRewardStrategy
from jobshop_rl.rewards.strategies.combined import CombinedRewardStrategy
from jobshop_rl.rewards.factory import RewardStrategyFactory, RewardStrategyRegistry

# Reexportar para mantener la compatibilidad
__all__ = [
    'RewardStrategy',
    'BasicRewardStrategy',
    'AdvancedRewardStrategy',
    'AdaptiveRewardStrategy',
    'CombinedRewardStrategy',
    'RewardStrategyFactory'
]
