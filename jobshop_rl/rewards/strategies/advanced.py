"""
Implementación de la estrategia de recompensa avanzada.
"""

from typing import Dict, Optional

from jobshop_rl.rewards.base import RewardStrategy
from jobshop_rl.rewards.components.makespan import MakespanRewardComponent
from jobshop_rl.rewards.components.idle_time import IdleTimeRewardComponent
from jobshop_rl.rewards.components.criticality import CriticalityRewardComponent
from jobshop_rl.rewards.components.balance import BalanceRewardComponent
from jobshop_rl.rewards.components.progress import ProgressRewardComponent
from jobshop_rl.rewards.components.local_improvement import LocalImprovementRewardComponent

class AdvancedRewardStrategy(RewardStrategy):
    """Estrategia de recompensa avanzada con señales intermedias"""
    
    def __init__(self, problem_analysis: Optional[Dict] = None, makespan_weight=1.0, 
                 idle_weight=0.2, critical_weight=0.1, balance_weight=0.05, 
                 progress_weight=0.2, local_improvement_weight=0.15):
        super().__init__(problem_analysis)
        
        # Inicializar componentes
        self.components = [
            MakespanRewardComponent(makespan_weight, problem_analysis),
            IdleTimeRewardComponent(idle_weight, problem_analysis),
            CriticalityRewardComponent(critical_weight, problem_analysis),
            BalanceRewardComponent(balance_weight, problem_analysis),
            ProgressRewardComponent(progress_weight),
            LocalImprovementRewardComponent(local_improvement_weight, problem_analysis)
        ]
    
    def calculate_reward(self, env, state, next_state, action, done, info) -> float:
        """Calcula la recompensa combinando todos los componentes"""
        if action is None or not state['eligible_ops']:
            return 0
            
        total_reward = 0
        for component in self.components:
            total_reward += component.calculate(env, state, next_state, action, done, info)
            
        return total_reward
    
    def reset(self) -> None:
        """Reinicia el estado interno de todos los componentes"""
        for component in self.components:
            component.reset()
    
    def set_problem_analysis(self, problem_analysis: Dict) -> None:
        """Configura el análisis del problema para todos los componentes"""
        super().set_problem_analysis(problem_analysis)
        for component in self.components:
            component.set_problem_analysis(problem_analysis)
