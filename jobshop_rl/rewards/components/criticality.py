"""
Componente de recompensa basado en la criticidad de las operaciones.

Soporta tanto problemas determinísticos (escalares) como problemas con
incertidumbre (intervalos) en los tiempos de procesamiento.
"""

from typing import Dict, Optional, Union

from jobshop_rl.rewards.base import RewardComponent
from jobshop_rl.models.interval import Interval


class CriticalityRewardComponent(RewardComponent):
    """
    Calcula la recompensa basada en la criticidad de las operaciones.
    
    Para intervalos, usa el upper bound (peor caso) del tiempo restante
    para calcular la criticidad.
    """
    
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
                
                # Extract scalar value
                if isinstance(total_work, Interval):
                    work_value = total_work.upper
                else:
                    work_value = total_work
                
                if work_value > 0 and num_jobs > 0:
                    self.critical_scale = max(50, work_value / (num_jobs * 2))
    
    def _get_scalar_value(self, value: Union[float, Interval]) -> float:
        """
        Extrae un valor escalar de un valor que puede ser intervalo.
        
        Para intervalos, usa el upper bound (peor caso).
        
        Args:
            value: Valor escalar o intervalo
            
        Returns:
            Valor escalar para cálculo de recompensa
        """
        if isinstance(value, Interval):
            return value.upper
        return value
    
    def calculate(self, env, state, next_state, action, done, info) -> float:
        """
        Calcula la recompensa basada en la criticidad.
        
        Para problemas con intervalos:
        - Suma duraciones restantes usando aritmética de intervalos
        - Usa upper bound para el cálculo de criticidad
        """
        if action is None or not state['eligible_ops'] or done:
            return 0
        
        # Obtener información de la operación programada
        job_id = state['eligible_ops'][action]
        op_idx = state['job_status'][job_id]
        
        # Calcular criticidad basada en tiempo restante
        remaining_ops = env.num_machines - op_idx - 1
        if remaining_ops > 0:
            # Sum remaining durations (works for both scalars and Intervals)
            remaining_durations = env.durations[job_id][op_idx+1:]
            
            # Check if we have intervals
            has_intervals = any(isinstance(d, Interval) for d in remaining_durations)
            
            if has_intervals:
                # Use interval arithmetic
                remaining_time = sum(remaining_durations, Interval(0, 0))
            else:
                # Regular sum
                remaining_time = sum(remaining_durations)
            
            # Convert to scalar for reward calculation
            remaining_value = self._get_scalar_value(remaining_time)
            
            criticality = remaining_value / self.critical_scale
            return self.weight * criticality
        
        return 0
    
    def set_problem_analysis(self, problem_analysis: Dict) -> None:
        """Configura el análisis del problema y actualiza escalas"""
        self.problem_analysis = problem_analysis
        self._adapt_scale()
