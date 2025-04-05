"""
Clase base abstracta para agentes de aprendizaje por refuerzo.
"""

from abc import ABC, abstractmethod
from typing import Dict, Tuple, List, Optional, Any

class Agent(ABC):
    """Clase base para todos los agentes de RL"""
    
    @abstractmethod
    def select_action(self, state: Dict, training: bool = True) -> Tuple[Optional[int], Any, Any]:
        """
        Selecciona una acción basada en el estado actual.
        
        Args:
            state: El estado actual del entorno.
            training: Si estamos en modo entrenamiento (True) o evaluación (False).
            
        Returns:
            Tuple que contiene:
            - Índice de la acción seleccionada
            - Información adicional sobre la acción (como log_prob)
            - Información sobre características extraídas
        """
        pass
    
    @abstractmethod
    def train_episode(self) -> float:
        """
        Entrena al agente por un episodio completo.
        
        Returns:
            Recompensa total obtenida en el episodio.
        """
        pass
    
    @abstractmethod
    def train(self, episodes: int, **kwargs):
        """
        Entrena al agente por un número específico de episodios.
        
        Args:
            episodes: Número de episodios a entrenar.
            **kwargs: Parámetros adicionales de entrenamiento.
        """
        pass
    
    @abstractmethod
    def evaluate_policy(self) -> Tuple[float, List[Dict], List[float]]:
        """
        Evalúa la política actual en un episodio completo.
        
        Returns:
            Tuple que contiene:
            - Makespan final
            - Historial de la programación
            - Historial de makespan
        """
        pass
    
    @abstractmethod
    def save_checkpoint(self, path: str):
        """
        Guarda el modelo en un checkpoint.
        
        Args:
            path: Ruta donde guardar el checkpoint.
        """
        pass
    
    @abstractmethod
    def load_checkpoint(self, path: str):
        """
        Carga un modelo desde un checkpoint.
        
        Args:
            path: Ruta desde donde cargar el checkpoint.
        """
        pass
