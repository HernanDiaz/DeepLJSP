"""
Implementación de la estrategia de recompensa combinada.
"""

from typing import Dict, Optional, List, Tuple

from jobshop_rl.rewards.base import RewardStrategy

class CombinedRewardStrategy(RewardStrategy):
    """Estrategia de recompensa que combina múltiples estrategias con pesos"""
    
    def __init__(self, strategies_with_weights: List[Tuple[RewardStrategy, float]], 
                 problem_analysis: Optional[Dict] = None):
        super().__init__(problem_analysis)
        self.strategies_with_weights = strategies_with_weights
        
        # Propagar análisis del problema a todas las estrategias
        if problem_analysis:
            for strategy, _ in self.strategies_with_weights:
                strategy.set_problem_analysis(problem_analysis)
    
    def calculate_reward(self, env, state, next_state, action, done, info) -> float:
        """Calcula la recompensa combinando estrategias ponderadas"""
        total_reward = 0
        for strategy, weight in self.strategies_with_weights:
            reward = strategy.calculate_reward(env, state, next_state, action, done, info)
            total_reward += weight * reward
        return total_reward
    
    def reset(self) -> None:
        """Reinicia el estado interno de todas las estrategias"""
        for strategy, _ in self.strategies_with_weights:
            strategy.reset()
    
    def set_problem_analysis(self, problem_analysis: Dict) -> None:
        """Configura el análisis del problema para todas las estrategias"""
        super().set_problem_analysis(problem_analysis)
        for strategy, _ in self.strategies_with_weights:
            strategy.set_problem_analysis(problem_analysis)
