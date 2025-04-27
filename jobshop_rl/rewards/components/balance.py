"""
Componente de recompensa basado en el balance de carga entre máquinas.
"""

import numpy as np
from typing import Dict, Optional

from jobshop_rl.rewards.base import RewardComponent

class BalanceRewardComponent(RewardComponent):
    """Calcula la recompensa basada en el balance de carga entre máquinas"""
    
    def __init__(self, weight: float = 0.05, problem_analysis: Optional[Dict] = None):
        self.weight = weight
        self.problem_analysis = problem_analysis
        self.balance_scale = 50.0
        
        if problem_analysis:
            self._adapt_scale()
    
    def _adapt_scale(self) -> None:
        """Adapta la escala de recompensa según el problema"""
        if self.problem_analysis and 'machine_loads' in self.problem_analysis:
            expected_std = np.std(self.problem_analysis['machine_loads']) * 1.5
            self.balance_scale = max(10, expected_std)
    
    def calculate(self, env, state, next_state, action, done, info) -> float:
        """Calcula la recompensa basada en el balance de carga"""
        if action is None or not state['eligible_ops']:
            return 0
            
        # Calcular desviación estándar de tiempos de finalización
        completion_times = [t for t in next_state['machine_completion_time'] if t > 0]
        if completion_times:
            std_dev = np.std(completion_times)
            balance_reward = -std_dev / self.balance_scale
            return self.weight * balance_reward
        
        return 0
    
    def set_problem_analysis(self, problem_analysis: Dict) -> None:
        """Configura el análisis del problema y actualiza escalas"""
        self.problem_analysis = problem_analysis
        self._adapt_scale()
