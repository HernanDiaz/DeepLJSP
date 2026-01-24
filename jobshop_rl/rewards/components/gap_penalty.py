"""
Componente de recompensa que penaliza crear huecos (gaps) en el schedule.

Este componente ayuda a evitar que el agente planifique trabajos enteros
dejando grandes huecos entre operaciones en las máquinas.
"""

from typing import Dict, Optional, Union

from jobshop_rl.rewards.base import RewardComponent
from jobshop_rl.models.interval import Interval


class GapPenaltyComponent(RewardComponent):
    """
    Penaliza la creación de huecos (gaps) en el schedule.
    
    Un gap se define como la diferencia entre el tiempo de finalización
    de la máquina y el tiempo de inicio de la nueva operación.
    
    Para intervalos, usa el upper bound (peor caso) para calcular gaps.
    """
    
    def __init__(self, weight: float = 0.3, problem_analysis: Optional[Dict] = None):
        self.weight = weight
        self.problem_analysis = problem_analysis
        self.gap_scale = 50.0
        self.gap_threshold = 5.0  # Gaps menores a este valor no se penalizan
        
        if problem_analysis:
            self._adapt_scale()
    
    def _adapt_scale(self) -> None:
        """Adapta la escala y threshold según el problema"""
        if self.problem_analysis:
            if 'avg_op_duration' in self.problem_analysis:
                avg_duration = self.problem_analysis['avg_op_duration']
                
                # Extract scalar value
                if isinstance(avg_duration, Interval):
                    avg_value = avg_duration.midpoint
                else:
                    avg_value = avg_duration
                
                if avg_value > 0:
                    # Scale basada en duración promedio
                    self.gap_scale = max(20, avg_value * 3)
                    # Threshold: gaps menores al 10% de duración promedio se ignoran
                    self.gap_threshold = max(1.0, avg_value * 0.1)
    
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
        Calcula la penalización por crear gaps en el schedule.
        
        Para problemas con intervalos:
        - Calcula gap usando aritmética de intervalos
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
        
        # Calcular gap solo si la máquina tiene que esperar al trabajo
        # Gap = tiempo que la máquina está inactiva esperando
        if machine_time < job_time:
            gap = job_time - machine_time
            
            # Convert to scalar for penalty calculation
            gap_value = self._get_scalar_value(gap)
            
            # Solo penalizar si el gap supera el threshold
            if gap_value > self.gap_threshold:
                # Penalización cuadrática para gaps grandes
                # Esto penaliza más fuertemente gaps grandes
                normalized_gap = (gap_value - self.gap_threshold) / self.gap_scale
                gap_penalty = -(normalized_gap ** 1.5)  # Exponente > 1 para penalizar más gaps grandes
                
                return self.weight * gap_penalty
        
        return 0
    
    def set_problem_analysis(self, problem_analysis: Dict) -> None:
        """Configura el análisis del problema y actualiza escalas"""
        self.problem_analysis = problem_analysis
        self._adapt_scale()
