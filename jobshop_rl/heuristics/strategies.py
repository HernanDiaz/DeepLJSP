"""
Estrategias heurísticas para la resolución del problema de Job Shop Scheduling.

Soporta tanto problemas determinísticos (escalares) como problemas con
incertidumbre (intervalos) en los tiempos de procesamiento.
"""

import random
import numpy as np
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Any, Optional, Union

from jobshop_rl.models.interval import Interval

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
                     - Scalar problems: (n_ops, 7)
                     - Interval problems: (n_ops, 10)
            
        Returns:
            Índice de la acción seleccionada
        """
        pass
    
    @staticmethod
    def _is_interval_features(features: np.ndarray) -> bool:
        """
        Detecta si las características corresponden a un problema con intervalos.
        
        Args:
            features: Matriz de características
            
        Returns:
            True si es un problema con intervalos (10 features)
        """
        if len(features) == 0:
            return False
        return features.shape[1] == 10
    
    @staticmethod
    def _extract_duration(features: np.ndarray, idx: int) -> Union[float, Tuple[float, float]]:
        """
        Extrae la duración de las características.
        
        Args:
            features: Matriz de características
            idx: Índice de la operación
            
        Returns:
            Duración como float (scalar) o tupla (lower, upper) para intervalos
        """
        if HeuristicStrategy._is_interval_features(features):
            # Interval: features[idx][3] = duration_lower, features[idx][4] = duration_upper
            return (features[idx][3], features[idx][4])
        else:
            # Scalar: features[idx][3] = duration
            return features[idx][3]
    
    @staticmethod
    def _extract_earliest_start(features: np.ndarray, idx: int) -> Union[float, Tuple[float, float]]:
        """
        Extrae el earliest start de las características.
        
        Args:
            features: Matriz de características
            idx: Índice de la operación
            
        Returns:
            Earliest start como float (scalar) o tupla (lower, upper) para intervalos
        """
        if HeuristicStrategy._is_interval_features(features):
            # Interval: features[idx][5] = start_lower, features[idx][6] = start_upper
            return (features[idx][5], features[idx][6])
        else:
            # Scalar: features[idx][4] = earliest_start
            return features[idx][4]
    
    @staticmethod
    def _extract_remaining_time(features: np.ndarray, idx: int) -> Union[float, Tuple[float, float]]:
        """
        Extrae el remaining time de las características.
        
        Args:
            features: Matriz de características
            idx: Índice de la operación
            
        Returns:
            Remaining time como float (scalar) o tupla (lower, upper) para intervalos
        """
        if HeuristicStrategy._is_interval_features(features):
            # Interval: features[idx][7] = remain_lower, features[idx][8] = remain_upper
            return (features[idx][7], features[idx][8])
        else:
            # Scalar: features[idx][5] = remaining_time
            return features[idx][5]
    
    @staticmethod
    def _extract_remaining_ops(features: np.ndarray, idx: int) -> int:
        """
        Extrae el número de operaciones restantes.
        
        Args:
            features: Matriz de características
            idx: Índice de la operación
            
        Returns:
            Número de operaciones restantes
        """
        if HeuristicStrategy._is_interval_features(features):
            # Interval: features[idx][9] = remaining_ops
            return int(features[idx][9])
        else:
            # Scalar: features[idx][6] = remaining_ops
            return int(features[idx][6])
    
    @staticmethod
    def _lexicographic_compare(val1: Union[float, Tuple[float, float]], 
                               val2: Union[float, Tuple[float, float]], 
                               minimize: bool = True) -> int:
        """
        Compara dos valores usando ordenamiento lexicográfico.
        
        Para escalares: comparación directa
        Para intervalos: primero compara upper, luego lower
        
        Args:
            val1: Primer valor (scalar o tupla (lower, upper))
            val2: Segundo valor (scalar o tupla (lower, upper))
            minimize: Si True, retorna índice del menor; si False, del mayor
            
        Returns:
            0 si val1 es preferido, 1 si val2 es preferido
        """
        # Handle scalars
        if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
            if minimize:
                return 0 if val1 < val2 else 1
            else:
                return 0 if val1 > val2 else 1
        
        # Handle intervals
        if isinstance(val1, tuple) and isinstance(val2, tuple):
            lower1, upper1 = val1
            lower2, upper2 = val2
            
            if minimize:
                # Minimize: prefer (upper, lower) lexicographically
                if upper1 < upper2:
                    return 0
                elif upper1 > upper2:
                    return 1
                else:
                    # Upper bounds equal, compare lower bounds
                    return 0 if lower1 < lower2 else 1
            else:
                # Maximize: prefer (upper, lower) lexicographically
                if upper1 > upper2:
                    return 0
                elif upper1 < upper2:
                    return 1
                else:
                    return 0 if lower1 > lower2 else 1
        
        # Shouldn't reach here if types are consistent
        return 0


class SPTHeuristic(HeuristicStrategy):
    """
    Heurística de Shortest Processing Time (tiempo de procesamiento más corto).
    
    Para intervalos, usa comparación lexicográfica: prefiere (upper, lower) mínimo.
    """

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        """Selecciona la operación con el menor tiempo de procesamiento"""
        if len(features) == 0:
            return 0
        
        # Extract durations
        durations = [self._extract_duration(features, i) for i in range(len(features))]
        
        # Find minimum using lexicographic comparison
        min_idx = 0
        min_duration = durations[0]
        
        for i in range(1, len(durations)):
            if self._lexicographic_compare(durations[i], min_duration, minimize=True) == 0:
                min_idx = i
                min_duration = durations[i]
        
        return min_idx


class LPTHeuristic(HeuristicStrategy):
    """
    Heurística de Longest Processing Time (tiempo de procesamiento más largo).
    
    Para intervalos, usa comparación lexicográfica: prefiere (upper, lower) máximo.
    """

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        """Selecciona la operación con el mayor tiempo de procesamiento"""
        if len(features) == 0:
            return 0
        
        # Extract durations
        durations = [self._extract_duration(features, i) for i in range(len(features))]
        
        # Find maximum using lexicographic comparison
        max_idx = 0
        max_duration = durations[0]
        
        for i in range(1, len(durations)):
            if self._lexicographic_compare(durations[i], max_duration, minimize=False) == 0:
                max_idx = i
                max_duration = durations[i]
        
        return max_idx


class MORHeuristic(HeuristicStrategy):
    """
    Heurística de Most Operations Remaining (más operaciones restantes).
    
    Esta heurística no se ve afectada por intervalos (remaining_ops es siempre escalar).
    """

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        """Selecciona la operación con el mayor número de operaciones restantes"""
        if len(features) == 0:
            return 0
        
        remaining_ops = [self._extract_remaining_ops(features, i) for i in range(len(features))]
        return np.argmax(remaining_ops)


class MWKRHeuristic(HeuristicStrategy):
    """
    Heurística de Most Work Remaining (más trabajo restante).
    
    Para intervalos, usa comparación lexicográfica en remaining_time.
    """

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        """Selecciona la operación con el mayor tiempo de trabajo restante"""
        if len(features) == 0:
            return 0
        
        # Extract remaining times
        remaining_times = [self._extract_remaining_time(features, i) for i in range(len(features))]
        
        # Find maximum using lexicographic comparison
        max_idx = 0
        max_time = remaining_times[0]
        
        for i in range(1, len(remaining_times)):
            if self._lexicographic_compare(remaining_times[i], max_time, minimize=False) == 0:
                max_idx = i
                max_time = remaining_times[i]
        
        return max_idx


class ESTHeuristic(HeuristicStrategy):
    """
    Heurística de Earliest Start Time (tiempo de inicio más temprano).
    
    Para intervalos, usa comparación lexicográfica en earliest_start.
    """

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        """Selecciona la operación que puede comenzar más temprano"""
        if len(features) == 0:
            return 0
        
        # Extract earliest start times
        start_times = [self._extract_earliest_start(features, i) for i in range(len(features))]
        
        # Find minimum using lexicographic comparison
        min_idx = 0
        min_start = start_times[0]
        
        for i in range(1, len(start_times)):
            if self._lexicographic_compare(start_times[i], min_start, minimize=True) == 0:
                min_idx = i
                min_start = start_times[i]
        
        return min_idx


class CRHeuristic(HeuristicStrategy):
    """
    Heurística de Critical Ratio (relación crítica).
    
    Para intervalos, calcula el ratio usando upper bounds (peor caso).
    """

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        """
        Selecciona la operación con la menor relación de tiempo restante a operaciones restantes.
        Para evitar divisiones por cero, añadimos un pequeño valor epsilon.
        """
        if len(features) == 0:
            return 0
        
        epsilon = 1e-10
        
        # Extract remaining times and ops
        critical_ratios = []
        for i in range(len(features)):
            remaining_time = self._extract_remaining_time(features, i)
            remaining_ops = self._extract_remaining_ops(features, i)
            
            # For intervals, use upper bound (worst case)
            if isinstance(remaining_time, tuple):
                time_value = remaining_time[1]  # upper bound
            else:
                time_value = remaining_time
            
            ratio = time_value / (remaining_ops + epsilon)
            critical_ratios.append(ratio)
        
        return np.argmin(critical_ratios)


class RandomHeuristic(HeuristicStrategy):
    """Heurística aleatoria"""

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        """Selecciona una operación aleatoria"""
        if len(eligible_ops) == 0:
            return 0
        return random.randint(0, len(eligible_ops)-1)


class ORToolsHeuristic(HeuristicStrategy):
    """
    Heurística que utiliza Google OR-Tools para resolver el problema completo.
    
    IMPORTANTE: OR-Tools NO soporta problemas con intervalos. Esta heurística
    solo funciona para problemas determinísticos (escalares).
    """
    
    def __init__(self, sequences=None, durations=None, time_limit_seconds=30, has_intervals=False):
        """
        Inicializa la heurística de OR-Tools.
        
        Args:
            sequences: Secuencias de máquinas para cada trabajo
            durations: Duraciones para cada operación de cada trabajo
            time_limit_seconds: Tiempo límite para la búsqueda en segundos
            has_intervals: Si True, el problema tiene intervalos (OR-Tools no soportado)
        """
        self.sequences = sequences
        self.durations = durations
        self.time_limit_seconds = time_limit_seconds
        self.has_intervals = has_intervals
        self.solved = False
        self.solve_attempted = False
        self.solution = []
        self.makespan = float('inf')
        self.operation_sequence = []
        
        # Verificar disponibilidad de OR-Tools
        if not hasattr(self, 'ortools_available'):
            try:
                self.ortools_available = JobShopORToolsSolver.check_ortools_availability()
            except:
                self.ortools_available = False
        
        # Advertir si hay intervalos
        if self.has_intervals:
            logger.warning(
                "OR-Tools NO soporta problemas con intervalos. "
                "Esta heurística usará un fallback (SPT) para problemas con incertidumbre."
            )
        
        # Mostrar advertencia si OR-Tools no está disponible
        if not self.ortools_available and not self.has_intervals:
            logger.warning("OR-Tools no está disponible. La heurística OR-Tools no funcionará correctamente.")
    
    def _solve_problem(self):
        """Resuelve el problema utilizando OR-Tools y almacena la solución"""
        self.solve_attempted = True

        # Check for intervals first
        if self.has_intervals:
            logger.warning("Cannot solve interval problems with OR-Tools. Using fallback heuristic.")
            self.solved = False
            return
        
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
        
        # Guardar la solución; solo marcar como resuelto si el solver
        # devolvió una solución válida (con time limit puede terminar en
        # UNKNOWN/INFEASIBLE con makespan infinito y schedule vacío)
        self.makespan = makespan
        self.solution = schedule
        self.solved = bool(schedule) and makespan != float('inf')
        self.execution_time = execution_time

        if not self.solved:
            logger.warning(f"OR-Tools no encontró solución (makespan={makespan}). "
                           f"Se usará la heurística de fallback.")
            return

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
        
        Para problemas con intervalos, usa SPT como fallback.
        
        Args:
            eligible_ops: Lista de índices de operaciones elegibles
            features: Matriz de características de las operaciones
            
        Returns:
            Índice de la acción seleccionada
        """
        # Check if this is an interval problem
        if self._is_interval_features(features):
            # Use SPT as fallback for interval problems
            logger.debug("Using SPT fallback for interval problem")
            return SPTHeuristic().select_action(eligible_ops, features)
        
        # Si no hemos intentado resolver el problema aún, resolverlo primero
        # (solo un intento: si OR-Tools falla, no relanzarlo en cada acción)
        if not self.solved and not self.solve_attempted:
            self._solve_problem()
            
        # Si no tenemos solución, usar una heurística como fallback
        if not self.solved or not self.operation_sequence:
            return SPTHeuristic().select_action(eligible_ops, features)
        
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
        # Usar SPT como fallback
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
            has_intervals = kwargs.get("has_intervals", False)
            return ORToolsHeuristic(sequences, durations, time_limit, has_intervals)
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
