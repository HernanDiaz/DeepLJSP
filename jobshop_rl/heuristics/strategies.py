"""
Estrategias heurísticas para la resolución del problema de Job Shop Scheduling.
"""

import random
import numpy as np
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Any, Optional

class HeuristicStrategy(ABC):
    """Estrategia base para heurísticas (patrón Strategy)"""

    @abstractmethod
    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        """
        Selecciona una acción basada en las operaciones elegibles y sus características.
        
        Args:
            eligible_ops: Lista de índices de operaciones elegibles
            features: Matriz de características de operaciones
            
        Returns:
            Índice de la acción seleccionada
        """
        pass

class SPTHeuristic(HeuristicStrategy):
    """Heurística de Shortest Processing Time (tiempo de procesamiento más corto)"""

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        """Selecciona la operación con el menor tiempo de procesamiento"""
        return np.argmin([f[3] for f in features])  # El índice 3 corresponde a la duración

class LPTHeuristic(HeuristicStrategy):
    """Heurística de Longest Processing Time (tiempo de procesamiento más largo)"""

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        """Selecciona la operación con el mayor tiempo de procesamiento"""
        return np.argmax([f[3] for f in features])  # El índice 3 corresponde a la duración

class MORHeuristic(HeuristicStrategy):
    """Heurística de Most Operations Remaining (más operaciones restantes)"""

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        """Selecciona la operación con el mayor número de operaciones restantes"""
        return np.argmax([f[6] for f in features])  # El índice 6 corresponde a remaining_ops

class MWKRHeuristic(HeuristicStrategy):
    """Heurística de Most Work Remaining (más trabajo restante)"""

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        """Selecciona la operación con el mayor tiempo de trabajo restante"""
        return np.argmax([f[5] for f in features])  # El índice 5 corresponde a remaining_time

class ESTHeuristic(HeuristicStrategy):
    """Heurística de Earliest Start Time (tiempo de inicio más temprano)"""

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        """Selecciona la operación que puede comenzar más temprano"""
        return np.argmin([f[4] for f in features])  # El índice 4 corresponde a earliest_start

class CRHeuristic(HeuristicStrategy):
    """Heurística de Critical Ratio (relación crítica)"""

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        """
        Selecciona la operación con la menor relación de tiempo restante a operaciones restantes.
        Para evitar divisiones por cero, añadimos un pequeño valor epsilon.
        """
        epsilon = 1e-10
        critical_ratios = [(f[5] / (f[6] + epsilon)) for f in features]
        return np.argmin(critical_ratios)

class RandomHeuristic(HeuristicStrategy):
    """Heurística aleatoria"""

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        """Selecciona una operación aleatoria"""
        return random.randint(0, len(eligible_ops)-1)

class CompositeHeuristic(HeuristicStrategy):
    """Heurística compuesta que combina múltiples heurísticas con pesos"""

    def __init__(self, heuristics_with_weights: List[Tuple[HeuristicStrategy, float]]):
        """
        Inicializa la heurística compuesta.
        
        Args:
            heuristics_with_weights: Lista de tuplas (heurística, peso)
        """
        self.heuristics_with_weights = heuristics_with_weights

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        """
        Combina las decisiones de múltiples heurísticas.
        
        Implementación: Para cada operación, calcula una puntuación compuesta basada 
        en el rango que cada heurística le asignaría, ponderado por los pesos.
        """
        if not eligible_ops:
            return -1  # Sin operaciones elegibles
            
        if len(eligible_ops) == 1:
            return 0  # Solo hay una opción
        
        # Inicializar puntuaciones
        scores = np.zeros(len(eligible_ops))
        
        # Acumular puntuaciones de cada heurística
        for heuristic, weight in self.heuristics_with_weights:
            # Obtener acción de esta heurística
            action = heuristic.select_action(eligible_ops, features)
            # Sumar el peso a la puntuación de la acción elegida
            scores[action] += weight
        
        # Seleccionar la acción con mayor puntuación
        return np.argmax(scores)

class HeuristicFactory:
    """Fábrica para crear estrategias heurísticas (patrón Factory)"""

    @staticmethod
    def create_heuristic(heuristic_type: str, **kwargs) -> HeuristicStrategy:
        """
        Crea una estrategia heurística basada en el tipo especificado.
        
        Args:
            heuristic_type: Tipo de heurística ("spt", "lpt", "mor", etc.)
            **kwargs: Parámetros adicionales
            
        Returns:
            Instancia de una estrategia heurística
        """
        heuristic_type = heuristic_type.lower()
        
        if heuristic_type == "spt":
            return SPTHeuristic()
        elif heuristic_type == "lpt":
            return LPTHeuristic()
        elif heuristic_type == "mor":
            return MORHeuristic()
        elif heuristic_type == "mwkr":
            return MWKRHeuristic()
        elif heuristic_type == "est":
            return ESTHeuristic()
        elif heuristic_type == "cr":
            return CRHeuristic()
        elif heuristic_type == "random":
            return RandomHeuristic()
        elif heuristic_type == "composite":
            # Ejemplo: {"heuristics": [("spt", 0.5), ("mor", 0.3), ("est", 0.2)]}
            heuristics_with_weights = []
            
            for config in kwargs.get("heuristics", []):
                if len(config) >= 2:
                    h_name = config[0]
                    h_weight = config[1]
                    h_params = config[2] if len(config) > 2 else {}
                    
                    heuristic = HeuristicFactory.create_heuristic(h_name, **h_params)
                    heuristics_with_weights.append((heuristic, h_weight))
            
            return CompositeHeuristic(heuristics_with_weights)
        else:
            raise ValueError(f"Tipo de heurística desconocido: {heuristic_type}")
