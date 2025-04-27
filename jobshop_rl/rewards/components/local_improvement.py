"""
Componente de recompensa basado en la mejora local del makespan proyectado.
"""

from typing import Dict, Optional

from jobshop_rl.rewards.base import RewardComponent

class LocalImprovementRewardComponent(RewardComponent):
    """Calcula la recompensa basada en la mejora local del makespan proyectado"""
    
    def __init__(self, weight: float = 0.15, problem_analysis: Optional[Dict] = None):
        self.weight = weight
        self.problem_analysis = problem_analysis
        self.last_projected_makespan = float('inf')
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
        """Calcula la recompensa basada en la mejora local"""
        if action is None or not state['eligible_ops']:
            return 0
            
        # Calcular makespan proyectado actual
        current_projected_makespan = max(next_state['machine_completion_time'])
        
        # Inicializar recompensa
        reward = 0
        
        # Mejora relativa desde la última acción
        if self.last_projected_makespan != float('inf'):
            improvement = (self.last_projected_makespan - current_projected_makespan)
            # Normalizar y solo recompensar mejoras
            if improvement > 0:
                local_reward = improvement / (self.makespan_scale / 10)
                reward = self.weight * local_reward
        
        # Actualizar para el próximo cálculo
        self.last_projected_makespan = current_projected_makespan
        
        return reward
    
    def reset(self) -> None:
        """Reinicia el estado interno del componente"""
        self.last_projected_makespan = float('inf')
    
    def set_problem_analysis(self, problem_analysis: Dict) -> None:
        """Configura el análisis del problema y actualiza escalas"""
        self.problem_analysis = problem_analysis
        self._adapt_scale()
