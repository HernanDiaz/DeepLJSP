"""
Estrategias heurísticas para la resolución del problema de Job Shop Scheduling.
"""

import random
import numpy as np
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Any, Optional

# Importar el solucionador de OR-Tools (de forma segura)
try:
    from jobshop_rl.heuristics.ortools_solver import JobShopORToolsSolver
except ImportError:
    logging.warning("No se pudo importar el solucionador de OR-Tools. La heurística OR-Tools no funcionará correctamente.")
    
logger = logging.getLogger("JobShopRL.Heuristics")

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


class ORToolsHeuristic(HeuristicStrategy):
    """Heurística que utiliza Google OR-Tools para resolver el problema completo"""
    
    def __init__(self, sequences=None, durations=None, time_limit_seconds=30):
        """
        Inicializa la heurística de OR-Tools.
        
        Args:
            sequences: Secuencias de máquinas para cada trabajo
            durations: Duraciones para cada operación de cada trabajo
            time_limit_seconds: Tiempo límite para la búsqueda en segundos
        """
        self.sequences = sequences
        self.durations = durations
        self.time_limit_seconds = time_limit_seconds
        self.solved = False
        self.solution = []
        self.makespan = float('inf')
        
        # Verificar disponibilidad de OR-Tools
        if not hasattr(self, 'ortools_available'):
            try:
                self.ortools_available = JobShopORToolsSolver.check_ortools_availability()
            except:
                self.ortools_available = False
        
        # Mostrar advertencia si OR-Tools no está disponible
        if not self.ortools_available:
            logger.warning("OR-Tools no está disponible. La heurística OR-Tools no funcionará correctamente.")
    
    def _solve_problem(self):
        """Resuelve el problema utilizando OR-Tools y almacena la solución"""
        if not self.ortools_available:
            logger.error("OR-Tools no está disponible. No se puede resolver el problema.")
            self.solved = False
            return
            
        if self.sequences is None or self.durations is None:
            logger.error("Secuencias o duraciones no proporcionadas a la heurística OR-Tools.")
            self.solved = False
            return
            
        logger.info("Resolviendo el problema con OR-Tools...")
        makespan, schedule, execution_time = JobShopORToolsSolver.solve(
            self.sequences, 
            self.durations, 
            self.time_limit_seconds
        )
        
        # Guardar la solución
        self.makespan = makespan
        self.solution = schedule
        self.solved = True
        self.execution_time = execution_time
        
        # Convertir la solución a un plan de acción
        self._create_action_plan()
        
        logger.info(f"Problema resuelto con OR-Tools. Makespan: {makespan}, Tiempo: {execution_time:.4f}s")
        
    def _create_action_plan(self):
        """
        Convierte la solución obtenida en un plan de acciones ordenadas por tiempo de inicio.
        Esto nos permitirá luego seleccionar la acción correcta basada en el estado actual.
        """
        if not self.solved or not self.solution:
            return
            
        # Ordenar la solución por tiempo de inicio
        self.action_plan = sorted(self.solution, key=lambda x: x['start'])
        
        # Crear una secuencia de operaciones por trabajos y tareas
        self.operation_sequence = [op for op in self.action_plan]
        self.current_op_index = 0
    
    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        """
        Selecciona la acción basada en la solución de OR-Tools.
        
        Para heurísticas offline como OR-Tools, este método no requiere exploración.
        En su lugar, seguimos la secuencia de operaciones preprocesada.
        
        Args:
            eligible_ops: Lista de índices de operaciones elegibles
            features: Matriz de características de las operaciones
            
        Returns:
            Índice de la acción seleccionada
        """
        # Si no hemos resuelto el problema aún, resolverlo primero
        if not self.solved:
            self._solve_problem()
            
        # Si no tenemos solución, usar una heurística aleatoria como fallback
        if not self.solved or not self.operation_sequence:
            return RandomHeuristic().select_action(eligible_ops, features)
        
        # Extraer información de las operaciones elegibles
        eligible_ops_info = []
        for i, feature in enumerate(features):
            job_id = int(feature[0])  # El índice 0 corresponde al job_id
            op_id = int(feature[1])   # El índice 1 corresponde al op_id
            eligible_ops_info.append((i, job_id, op_id))
        
        if not eligible_ops_info:
            # Si no hay operaciones elegibles, devolver acción aleatoria
            return RandomHeuristic().select_action(eligible_ops, features)
            
        # Crear un diccionario para acceso más rápido
        eligible_dict = {(j, op): idx for idx, j, op in eligible_ops_info}
        
        # Avanzar en el plan hasta encontrar una operación elegible
        found = False
        while self.current_op_index < len(self.operation_sequence) and not found:
            next_op = self.operation_sequence[self.current_op_index]
            job = next_op['job']
            task = next_op['task']
            
            # Verificar si esta operación está entre las elegibles
            if (job, task) in eligible_dict:
                idx = eligible_dict[(job, task)]
                self.current_op_index += 1
                return idx
            
            # Si la operación no está entre las elegibles, pasar a la siguiente
            self.current_op_index += 1
        
        # Si llegamos aquí, es porque no encontramos una operación elegible
        # Usar una heurística sencilla como fallback
        return SPTHeuristic().select_action(eligible_ops, features)

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
        elif heuristic_type == "ortools":
            # Tomar parámetros para OR-Tools
            sequences = kwargs.get("sequences", None)
            durations = kwargs.get("durations", None)
            time_limit = kwargs.get("time_limit", 30)
            return ORToolsHeuristic(sequences, durations, time_limit)
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
