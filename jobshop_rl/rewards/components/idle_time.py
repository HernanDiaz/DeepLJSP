"""
Componente de recompensa basado en el tiempo inactivo de máquinas.
"""

from typing import Dict, Optional

from jobshop_rl.rewards.base import RewardComponent

class IdleTimeRewardComponent(RewardComponent):
    """Calcula la penalización por tiempo inactivo en máquinas"""
    
    def __init__(self, weight: float = 0.2, problem_analysis: Optional[Dict] = None):
        self.weight = weight
        self.problem_analysis = problem_analysis
        self.idle_scale = 50.0
        
        if problem_analysis:
            self._adapt_scale()
    
    def _adapt_scale(self) -> None:
        """Adapta la escala de recompensa según el problema"""
        if self.problem_analysis and 'avg_op_duration' in self.problem_analysis:
            avg_duration = self.problem_analysis['avg_op_duration']
            if avg_duration > 0:
                self.idle_scale = max(10, avg_duration * 2)
    
    def calculate(self, env, state, next_state, action, done, info) -> float:
        """Calcula la recompensa basada en el tiempo inactivo"""
        if action is None or not state['eligible_ops']:
            return 0
            
        # Obtener información de la operación programada
        job_id = state['eligible_ops'][action]
        op_idx = state['job_status'][job_id]
        machine = env.sequences[job_id][op_idx]
        
        # Calcular tiempo inactivo
        start_time = max(state['job_completion_time'][job_id],
                         state['machine_completion_time'][machine])
        
        idle_time = 0
        if start_time > state['machine_completion_time'][machine]:
            idle_time = start_time - state['machine_completion_time'][machine]
        
        # Penalización normalizada
        idle_reward = -idle_time / self.idle_scale
        
        return self.weight * idle_reward
    
    def set_problem_analysis(self, problem_analysis: Dict) -> None:
        """Configura el análisis del problema y actualiza escalas"""
        self.problem_analysis = problem_analysis
        self._adapt_scale()
