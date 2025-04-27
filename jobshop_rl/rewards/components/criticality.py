"""
Componente de recompensa basado en la criticidad de las operaciones.
"""

from typing import Dict, Optional

from jobshop_rl.rewards.base import RewardComponent

class CriticalityRewardComponent(RewardComponent):
    """Calcula la recompensa basada en la criticidad de las operaciones"""
    
    def __init__(self, weight: float = 0.1, problem_analysis: Optional[Dict] = None):
        self.weight = weight
        self.problem_analysis = problem_analysis
        self.critical_scale = 100.0
        
        if problem_analysis:
            self._adapt_scale()
    
    def _adapt_scale(self) -> None:
        """Adapta la escala de recompensa según el problema"""
        if self.problem_analysis:
            if 'total_work' in self.problem_analysis and 'num_jobs' in self.problem_analysis:
                total_work = self.problem_analysis['total_work']
                num_jobs = self.problem_analysis['num_jobs']
                if total_work > 0 and num_jobs > 0:
                    self.critical_scale = max(50, total_work / (num_jobs * 2))
    
    def calculate(self, env, state, next_state, action, done, info) -> float:
        """Calcula la recompensa basada en la criticidad"""
        if action is None or not state['eligible_ops'] or done:
            return 0
            
        # Obtener información de la operación programada
        job_id = state['eligible_ops'][action]
        op_idx = state['job_status'][job_id]
        
        # Calcular criticidad basada en tiempo restante
        remaining_ops = env.num_machines - op_idx - 1
        if remaining_ops > 0:
            remaining_time = sum(env.durations[job_id][op_idx+1:])
            criticality = remaining_time / self.critical_scale
            return self.weight * criticality
        
        return 0
    
    def set_problem_analysis(self, problem_analysis: Dict) -> None:
        """Configura el análisis del problema y actualiza escalas"""
        self.problem_analysis = problem_analysis
        self._adapt_scale()
