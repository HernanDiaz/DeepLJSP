"""
Implementación de la estrategia de recompensa básica.
"""

from typing import Dict, Optional

from jobshop_rl.rewards.base import RewardStrategy
from jobshop_rl.rewards.components.makespan import MakespanRewardComponent

class BasicRewardStrategy(RewardStrategy):
    """Estrategia de recompensa básica: solo recompensa al final basada en makespan"""
    
    def __init__(self, problem_analysis: Optional[Dict] = None):
        super().__init__(problem_analysis)
        self.makespan_component = MakespanRewardComponent(
            weight=1.0,
            problem_analysis=problem_analysis
        )
    
    def calculate_reward(self, env, state, next_state, action, done, info) -> float:
        """Calcula la recompensa basada en el estado, la acción y el resultado"""
        if done:
            return self.makespan_component.calculate(env, state, next_state, action, done, info)
        return 0
    
    def reset(self) -> None:
        """Reinicia el estado interno de la estrategia"""
        self.makespan_component.reset()
    
    def set_problem_analysis(self, problem_analysis: Dict) -> None:
        """Configura el análisis del problema para esta estrategia"""
        super().set_problem_analysis(problem_analysis)
        self.makespan_component.set_problem_analysis(problem_analysis)
