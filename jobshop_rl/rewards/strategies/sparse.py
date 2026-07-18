"""
Estrategia de recompensa sparse (solo al final del episodio).

Esta estrategia da recompensa SOLO cuando termina el episodio,
basada en qué tan bueno es el makespan comparado con el mejor visto.
"""

from typing import Dict, Optional, Union

from jobshop_rl.rewards.base import RewardStrategy
from jobshop_rl.models.interval import Interval, final_makespan


class SparseRewardStrategy(RewardStrategy):
    """
    Estrategia de recompensa sparse: solo recompensa al final.
    
    La idea es simple:
    - Durante el episodio: reward = 0
    - Al final: reward basado en qué tan bueno es el makespan
    
    Esto elimina el ruido de señales intermedias y deja que
    el agente descubra qué acciones llevan a buenos makespans.
    """
    
    def __init__(self, problem_analysis: Optional[Dict] = None):
        super().__init__(problem_analysis)
        self.best_makespan_midpoint: Optional[float] = None
        self.lower_bound: float = 1.0
        
        if problem_analysis:
            self._extract_bounds(problem_analysis)
    
    def _extract_bounds(self, problem_analysis: Dict) -> None:
        """Extrae límites del análisis del problema"""
        if 'best_lower_bound' in problem_analysis:
            lb = problem_analysis['best_lower_bound']
            if isinstance(lb, Interval):
                self.lower_bound = lb.midpoint
            else:
                self.lower_bound = float(lb)
    
    def _get_midpoint(self, value: Union[float, Interval]) -> float:
        """Extrae midpoint de intervalo o valor escalar"""
        if isinstance(value, Interval):
            return float(value.midpoint)
        return float(value)
    
    def calculate_reward(self, env, state, next_state, action, done, info) -> float:
        """
        Calcula la recompensa.
        
        Durante episodio: 0
        Al final: recompensa basada en makespan vs mejor visto
        """
        if not done:
            return 0.0
        
        # Calcular makespan final (componente a componente: el midpoint usa el
        # lower, que con max() lexicografico saldria sesgado hacia abajo).
        makespan = final_makespan(env.job_completion_time)
        current_midpoint = self._get_midpoint(makespan)
        
        # Inicializar mejor si es necesario
        if self.best_makespan_midpoint is None:
            self.best_makespan_midpoint = current_midpoint
        
        # Calcular recompensa basada en comparación con mejor
        # Normalizada por lower bound para que sea comparable entre problemas
        
        # Gap respecto al lower bound (0 = óptimo, 1 = 100% peor)
        gap = (current_midpoint - self.lower_bound) / self.lower_bound
        
        # Recompensa base: penalización por gap
        reward = -gap
        
        # Bonus por igualar o mejorar el mejor
        if current_midpoint <= self.best_makespan_midpoint:
            # Bonus grande por igualar el mejor
            reward += 1.0
            
            if current_midpoint < self.best_makespan_midpoint:
                # Bonus adicional proporcional a la mejora
                improvement = (self.best_makespan_midpoint - current_midpoint) / self.lower_bound
                reward += improvement * 5.0  # 5x bonus por mejora
                
                # Actualizar mejor
                self.best_makespan_midpoint = current_midpoint
        else:
            # Penalización por ser peor que el mejor conocido
            degradation = (current_midpoint - self.best_makespan_midpoint) / self.lower_bound
            reward -= degradation * 2.0  # Penalización por empeorar
        
        return reward
    
    def reset(self) -> None:
        """Reset - NO resetea best_makespan_midpoint"""
        pass
    
    def full_reset(self) -> None:
        """Reset completo incluyendo mejor makespan"""
        self.best_makespan_midpoint = None
    
    def set_problem_analysis(self, problem_analysis: Dict) -> None:
        """Configura el análisis del problema"""
        super().set_problem_analysis(problem_analysis)
        self._extract_bounds(problem_analysis)
