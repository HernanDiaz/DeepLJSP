"""
Paquete principal para JobShopRL - Sistema modular de aprendizaje por refuerzo para problemas de Job Shop Scheduling.
"""

__version__ = '1.0.0'

# Importar subpaquetes principales para facilitar su acceso
from jobshop_rl.environment.job_shop_env import JobShopEnv
from jobshop_rl.agents.ppo_agent import PPOAgent
from jobshop_rl.rewards.factory import RewardStrategyFactory
from jobshop_rl.data.problem_loader import ProblemLoader
from jobshop_rl.experiments.factory import ExperimentFactory

__all__ = [
    'JobShopEnv',
    'PPOAgent',
    'RewardStrategyFactory',
    'ProblemLoader',
    'ExperimentFactory',
]
