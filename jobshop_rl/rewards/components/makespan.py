"""
Componente de recompensa basado en el makespan final.
"""

from typing import Dict, Optional

from jobshop_rl.rewards.base import RewardComponent

class MakespanRewardComponent(RewardComponent):
    """Calcula la recompensa basada en el makespan final"""
    
    def __init__(self, weight: float = 1.0, problem_analysis: Optional[Dict] = None):
        self.weight = weight
        self.problem_analysis = problem_analysis
        self.best_seen_makespan = float('inf')
        self.makespan_scale = 100.0
        
        if problem_analysis:
            self._adapt_scale()
    
    def _adapt_scale(self) -> None:
        """Adapta la escala de recompensa según el problema"""
        if self.problem_analysis and 'best_lower_bound' in self.problem_analysis:
            lower_bound = self.problem_analysis['best_lower_bound']
            if lower_bound > 0:
                self.makespan_scale = max(100, lower_bound / 10)
    
    def calculate(self, env, state, next_state, action, done, info) -> float:
        """Calcula la recompensa basada en el makespan"""
        if not done:
            return 0
            
        makespan = max(env.job_completion_time)
        
        # Actualizar mejor makespan visto
        if makespan < self.best_seen_makespan:
            self.best_seen_makespan = makespan
            
        # Recompensa base escalada
        reward = -makespan / self.makespan_scale
        
        # Bonus por acercarse al límite inferior
        if self.problem_analysis and 'best_lower_bound' in self.problem_analysis:
            lower_bound = self.problem_analysis['best_lower_bound']
            if lower_bound > 0:
                gap = (makespan - lower_bound) / lower_bound
                if gap <= 0.05:  # Dentro del 5% del límite inferior
                    reward += 10 * (1 - gap * 10)
        
        return self.weight * reward
    
    def set_problem_analysis(self, problem_analysis: Dict) -> None:
        """Configura el análisis del problema y actualiza escalas"""
        self.problem_analysis = problem_analysis
        self._adapt_scale()
