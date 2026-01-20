"""
Componente de recompensa basado en el tiempo inactivo de máquinas.

Soporta tanto problemas determinísticos (escalares) como problemas con
incertidumbre (intervalos) en los tiempos de procesamiento.
"""

from typing import Dict, Optional, Union

from jobshop_rl.rewards.base import RewardComponent
from jobshop_rl.models.interval import Interval


class IdleTimeRewardComponent(RewardComponent):
    """
    Calcula la penalización por tiempo inactivo en máquinas.
    
    Para intervalos, calcula el idle time usando aritmética de intervalos
    y usa el upper bound (peor caso) para la penalización.
    """
    
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
            
            # Extract scalar value for scale
            if isinstance(avg_duration, Interval):
                avg_value = avg_duration.midpoint
            elif isinstance(avg_duration, (int, float)):
                avg_value = avg_duration
            else:
                avg_value = avg_duration  # Fallback
            
            if avg_value > 0:
                self.idle_scale = max(10, avg_value * 2)
    
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
        Calcula la recompensa basada en el tiempo inactivo.
        
        Para problemas con intervalos:
        - Calcula idle time usando aritmética de intervalos
        - Usa upper bound para penalización (peor caso)
        """
        if action is None or not state['eligible_ops']:
            return 0
        
        # Obtener información de la operación programada
        job_id = state['eligible_ops'][action]
        op_idx = state['job_status'][job_id]
        machine = env.sequences[job_id][op_idx]
        
        # Calcular tiempo de inicio (puede ser escalar o intervalo)
        job_time = state['job_completion_time'][job_id]
        machine_time = state['machine_completion_time'][machine]
        
        # Use max (works for both scalars and Intervals with lexicographic comparison)
        start_time = max(job_time, machine_time)
        
        # Calcular tiempo inactivo
        # For intervals: idle_time will be an Interval
        # For scalars: idle_time will be a scalar
        if start_time > machine_time:
            idle_time = start_time - machine_time
        else:
            # No idle time
            if isinstance(start_time, Interval):
                idle_time = Interval(0, 0)
            else:
                idle_time = 0
        
        # Convert to scalar for reward calculation
        idle_value = self._get_scalar_value(idle_time)
        
        # Penalización normalizada (negativa porque queremos minimizar idle time)
        idle_reward = -idle_value / self.idle_scale
        
        return self.weight * idle_reward
    
    def set_problem_analysis(self, problem_analysis: Dict) -> None:
        """Configura el análisis del problema y actualiza escalas"""
        self.problem_analysis = problem_analysis
        self._adapt_scale()
