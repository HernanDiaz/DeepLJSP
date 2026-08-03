"""
Componente de recompensa basado en el makespan final.

Soporta tanto problemas determinísticos (escalares) como problemas con
incertidumbre (intervalos) en los tiempos de procesamiento.
"""

import os
from typing import Dict, Optional, Union

from jobshop_rl.rewards.base import RewardComponent
from jobshop_rl.models.interval import Interval, final_makespan


class MakespanRewardComponent(RewardComponent):
    """
    Calcula la recompensa basada en el makespan final.
    
    Para intervalos, usa el upper bound (peor caso) para calcular la recompensa,
    pero mantiene comparaciones lexicográficas para determinar mejoras.
    """
    
    def __init__(self, weight: float = 1.0, problem_analysis: Optional[Dict] = None):
        self.weight = weight
        self.problem_analysis = problem_analysis
        self.best_seen_makespan: Optional[Union[float, Interval]] = None
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
    
    def _robust_value(self, value: Union[float, Interval]) -> float:
        """Valor a minimizar: peor caso mas lambda por la anchura.

        DEEPLJSP_V2_LAMBDA=0 (defecto) deja el objetivo tal cual estaba,
        el peor caso puro. Con lambda>0 se penaliza explicitamente la
        anchura del intervalo predicho, el analogo del objetivo robusto
        f_lambda del estudio companion: up + lambda*(up - lo). Es la
        unica via por la que la anchura entra en lo que se optimiza.
        """
        lam = float(os.environ.get("DEEPLJSP_V2_LAMBDA", "0") or 0)
        if lam and isinstance(value, Interval):
            up, lo = float(value.upper), float(value.lower)
            return up + lam * (up - lo)
        return self._get_scalar_value(value)

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
        Calcula la recompensa basada en el makespan.
        
        Para problemas con intervalos:
        - Usa comparación lexicográfica para determinar mejoras
        - Usa upper bound para el cálculo numérico de la recompensa
        """
        if not done:
            return 0
        
        # Get makespan (can be scalar or Interval) — componente a componente.
        makespan = final_makespan(env.job_completion_time)
        
        # Actualizar mejor makespan visto (usando comparación lexicográfica)
        if self.best_seen_makespan is None or makespan < self.best_seen_makespan:
            self.best_seen_makespan = makespan
        
        # Convert to scalar for reward calculation
        makespan_value = self._robust_value(makespan)
        
        # Recompensa base escalada (negativa porque queremos minimizar)
        reward = -makespan_value / self.makespan_scale
        
        # Bonus por acercarse al límite inferior
        if self.problem_analysis and 'best_lower_bound' in self.problem_analysis:
            lower_bound = self.problem_analysis['best_lower_bound']
            lb_value = self._get_scalar_value(lower_bound)
            
            if lb_value > 0:
                # Calculate gap using scalar values
                gap = (makespan_value - lb_value) / lb_value
                
                if gap <= 0.05:  # Dentro del 5% del límite inferior
                    reward += 10 * (1 - gap * 10)
        
        return self.weight * reward
    
    def reset(self) -> None:
        """Reinicia el mejor makespan visto"""
        self.best_seen_makespan = None
    
    def set_problem_analysis(self, problem_analysis: Dict) -> None:
        """Configura el análisis del problema y actualiza escalas"""
        self.problem_analysis = problem_analysis
        self._adapt_scale()
