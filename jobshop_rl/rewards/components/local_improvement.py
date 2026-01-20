"""
Componente de recompensa basado en la mejora local del makespan proyectado.

Soporta tanto problemas determinísticos (escalares) como problemas con
incertidumbre (intervalos) en los tiempos de procesamiento.
"""

from typing import Dict, Optional, Union

from jobshop_rl.rewards.base import RewardComponent
from jobshop_rl.models.interval import Interval


class LocalImprovementRewardComponent(RewardComponent):
    """
    Calcula la recompensa basada en la mejora local del makespan proyectado.
    
    Para intervalos, usa el upper bound (peor caso) para calcular mejoras,
    pero mantiene comparaciones lexicográficas.
    """
    
    def __init__(self, weight: float = 0.15, problem_analysis: Optional[Dict] = None):
        self.weight = weight
        self.problem_analysis = problem_analysis
        self.last_projected_makespan: Optional[Union[float, Interval]] = None
        self.makespan_scale = 100.0
        
        if problem_analysis:
            self._adapt_scale()
    
    def _adapt_scale(self) -> None:
        """Adapta la escala de recompensa según el problema"""
        if self.problem_analysis and 'best_lower_bound' in self.problem_analysis:
            lower_bound = self.problem_analysis['best_lower_bound']
            
            # Extract scalar value for scale
            if isinstance(lower_bound, Interval):
                lb_value = lower_bound.upper  # Use worst case for scale
            else:
                lb_value = lower_bound
            
            if lb_value > 0:
                self.makespan_scale = max(100, lb_value / 10)
    
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
        Calcula la recompensa basada en la mejora local.
        
        Para problemas con intervalos:
        - Usa comparación lexicográfica para determinar mejoras
        - Usa upper bound para el cálculo numérico de la recompensa
        """
        if action is None or not state['eligible_ops']:
            return 0
        
        # Calcular makespan proyectado actual (puede ser escalar o Interval)
        current_projected_makespan = max(next_state['machine_completion_time'])
        
        # Inicializar recompensa
        reward = 0
        
        # Mejora relativa desde la última acción
        if self.last_projected_makespan is not None:
            # Check if there's an improvement (lexicographic for intervals)
            if self.last_projected_makespan > current_projected_makespan:
                # Convert to scalars for reward calculation
                last_value = self._get_scalar_value(self.last_projected_makespan)
                current_value = self._get_scalar_value(current_projected_makespan)
                
                improvement = last_value - current_value
                
                # Normalizar y solo recompensar mejoras
                if improvement > 0:
                    local_reward = improvement / (self.makespan_scale / 10)
                    reward = self.weight * local_reward
        
        # Actualizar para el próximo cálculo
        self.last_projected_makespan = current_projected_makespan
        
        return reward
    
    def reset(self) -> None:
        """Reinicia el estado interno del componente"""
        self.last_projected_makespan = None
    
    def set_problem_analysis(self, problem_analysis: Dict) -> None:
        """Configura el análisis del problema y actualiza escalas"""
        self.problem_analysis = problem_analysis
        self._adapt_scale()
