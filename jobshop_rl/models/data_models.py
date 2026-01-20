"""
Módulo para las clases de datos utilizadas en JobShopRL.
Contiene definiciones de operaciones, pasos de programación y características de estado.

Soporta tanto tiempos de procesamiento determinísticos (escalares) como intervalos.
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple, Any, Optional, Union, Callable

# Import Interval for interval-valued processing times
from jobshop_rl.models.interval import Interval, ensure_interval


@dataclass
class Operation:
    """
    Representa una operación dentro de un trabajo.
    
    Soporta tanto duraciones determinísticas (int) como intervalos (Interval).
    Los tiempos de inicio y fin también pueden ser intervalos.
    """
    job_id: int
    op_idx: int
    machine: int
    duration: Union[int, Interval]
    start_time: Optional[Union[int, Interval]] = None
    end_time: Optional[Union[int, Interval]] = None


@dataclass
class SchedulingStep:
    """
    Representa un paso en la programación.
    
    Soporta tanto tiempos escalares como intervalos para compatibilidad
    con problemas determinísticos e inciertos.
    """
    job: int
    operation: int
    machine: int
    start: Union[int, Interval]
    end: Union[int, Interval]


@dataclass
class StateFeatures:
    """
    Encapsula las características extraídas de un estado.
    
    Los tiempos de finalización pueden ser escalares o intervalos.
    """
    eligible_ops: List[int]
    job_status: List[int]
    job_completion_time: List[Union[int, Interval]]
    machine_completion_time: List[Union[int, Interval]]


@dataclass
class OperationFeatures:
    """
    Características de una operación para toma de decisiones.
    
    IMPORTANTE: Para problemas con intervalos, las características se expanden:
    - Escalares: 7 características
    - Intervalos: 10 características (algunos campos se dividen en lower/upper)
    
    Esta clase mantiene los valores originales (pueden ser Interval o int).
    El método to_array() maneja la conversión apropiada.
    """
    job_id: int
    op_idx: int
    machine: int
    duration: Union[int, Interval]
    earliest_start: Union[int, Interval]
    remaining_time: Union[int, Interval]
    remaining_ops: int

    def to_array(self) -> List[float]:
        """
        Convierte las características a un array para la red neuronal.
        
        Para escalares (backward compatible): 7 características
        Para intervalos: 10 características con bounds expandidos
        
        Returns:
            Lista de características en formato float
        """
        # Check if we're dealing with intervals
        has_intervals = (isinstance(self.duration, Interval) or 
                        isinstance(self.earliest_start, Interval) or 
                        isinstance(self.remaining_time, Interval))
        
        if has_intervals:
            # Extract interval bounds (10 features)
            duration_lower = self.duration.lower if isinstance(self.duration, Interval) else float(self.duration)
            duration_upper = self.duration.upper if isinstance(self.duration, Interval) else float(self.duration)
            
            earliest_start_lower = (self.earliest_start.lower if isinstance(self.earliest_start, Interval) 
                                   else float(self.earliest_start))
            earliest_start_upper = (self.earliest_start.upper if isinstance(self.earliest_start, Interval) 
                                   else float(self.earliest_start))
            
            remaining_time_lower = (self.remaining_time.lower if isinstance(self.remaining_time, Interval) 
                                   else float(self.remaining_time))
            remaining_time_upper = (self.remaining_time.upper if isinstance(self.remaining_time, Interval) 
                                   else float(self.remaining_time))
            
            return [
                float(self.job_id),
                float(self.op_idx),
                float(self.machine),
                duration_lower,
                duration_upper,
                earliest_start_lower,
                earliest_start_upper,
                remaining_time_lower,
                remaining_time_upper,
                float(self.remaining_ops)
            ]
        else:
            # Original 7 features for scalar values (backward compatibility)
            return [
                float(self.job_id),
                float(self.op_idx),
                float(self.machine),
                float(self.duration),
                float(self.earliest_start),
                float(self.remaining_time),
                float(self.remaining_ops)
            ]
    
    @property
    def feature_dimension(self) -> int:
        """
        Get the number of features this operation will produce.
        
        Returns:
            7 for scalar problems, 10 for interval problems
        """
        has_intervals = (isinstance(self.duration, Interval) or 
                        isinstance(self.earliest_start, Interval) or 
                        isinstance(self.remaining_time, Interval))
        return 10 if has_intervals else 7
