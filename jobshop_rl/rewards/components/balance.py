"""
Componente de recompensa basado en el balance de carga entre máquinas.

Soporta tanto problemas determinísticos (escalares) como problemas con
incertidumbre (intervalos) en los tiempos de procesamiento.
"""

import numpy as np
from typing import Dict, Optional, Union

from jobshop_rl.rewards.base import RewardComponent
from jobshop_rl.models.interval import Interval


class BalanceRewardComponent(RewardComponent):
    """
    Calcula la recompensa basada en el balance de carga entre máquinas.
    
    Para intervalos, usa el upper bound (peor caso) de los tiempos de completion
    para calcular el balance.
    """
    
    def __init__(self, weight: float = 0.05, problem_analysis: Optional[Dict] = None):
        self.weight = weight
        self.problem_analysis = problem_analysis
        self.balance_scale = 50.0
        
        if problem_analysis:
            self._adapt_scale()
    
    def _adapt_scale(self) -> None:
        """Adapta la escala de recompensa según el problema"""
        if self.problem_analysis and 'machine_loads' in self.problem_analysis:
            machine_loads = self.problem_analysis['machine_loads']
            
            # Extract scalar values for std calculation
            load_values = []
            for load in machine_loads:
                if isinstance(load, Interval):
                    load_values.append(load.upper)
                else:
                    load_values.append(load)
            
            expected_std = np.std(load_values) * 1.5
            self.balance_scale = max(10, expected_std)
    
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
        Calcula la recompensa basada en el balance de carga.
        
        Para problemas con intervalos:
        - Usa upper bound de cada tiempo de completion
        - Calcula desviación estándar con valores escalares
        """
        if action is None or not state['eligible_ops']:
            return 0
        
        # Extraer tiempos de finalización y convertir a escalares
        completion_times = []
        for t in next_state['machine_completion_time']:
            scalar_t = self._get_scalar_value(t)
            if scalar_t > 0:
                completion_times.append(scalar_t)
        
        if completion_times:
            std_dev = np.std(completion_times)
            balance_reward = -std_dev / self.balance_scale
            return self.weight * balance_reward
        
        return 0
    
    def set_problem_analysis(self, problem_analysis: Dict) -> None:
        """Configura el análisis del problema y actualiza escalas"""
        self.problem_analysis = problem_analysis
        self._adapt_scale()
