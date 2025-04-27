"""
Interfaces y clases base para el sistema de recompensas.
Define la estructura común que todas las estrategias y componentes deben seguir.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, Any

class RewardComponent(ABC):
    """Componente individual de cálculo de recompensa"""
    
    @abstractmethod
    def calculate(self, env, state, next_state, action, done, info) -> float:
        """Calcula un componente de recompensa basado en el estado actual y siguiente"""
        pass
    
    def reset(self) -> None:
        """Reinicia el estado interno del componente si es necesario"""
        pass
    
    def set_problem_analysis(self, problem_analysis: Dict) -> None:
        """Configura el análisis del problema para este componente"""
        pass

class RewardStrategy(ABC):
    """Estrategia base para el cálculo de recompensas (patrón Strategy)"""
    
    def __init__(self, problem_analysis: Optional[Dict] = None):
        self.problem_analysis = problem_analysis
    
    @abstractmethod
    def calculate_reward(self, env, state, next_state, action, done, info) -> float:
        """Calcula la recompensa basada en el estado, la acción y el resultado"""
        pass
    
    def reset(self) -> None:
        """Reinicia el estado interno de la estrategia"""
        pass
    
    def set_problem_analysis(self, problem_analysis: Dict) -> None:
        """Configura el análisis del problema para esta estrategia"""
        self.problem_analysis = problem_analysis
