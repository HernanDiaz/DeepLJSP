"""
Módulo para las clases de datos utilizadas en JobShopRL.
Contiene definiciones de operaciones, pasos de programación y características de estado.
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple, Any, Optional, Union, Callable

@dataclass
class Operation:
    """Representa una operación dentro de un trabajo"""
    job_id: int
    op_idx: int
    machine: int
    duration: int
    start_time: Optional[int] = None
    end_time: Optional[int] = None

@dataclass
class SchedulingStep:
    """Representa un paso en la programación"""
    job: int
    operation: int
    machine: int
    start: int
    end: int

@dataclass
class StateFeatures:
    """Encapsula las características extraídas de un estado"""
    eligible_ops: List[int]
    job_status: List[int]
    job_completion_time: List[int]
    machine_completion_time: List[int]

@dataclass
class OperationFeatures:
    """Características de una operación para toma de decisiones"""
    job_id: int
    op_idx: int
    machine: int
    duration: int
    earliest_start: int
    remaining_time: int
    remaining_ops: int

    def to_array(self) -> List[float]:
        """Convierte las características a un array para la red neuronal"""
        return [
            float(self.job_id), float(self.op_idx), float(self.machine), float(self.duration),
            float(self.earliest_start), float(self.remaining_time), float(self.remaining_ops)
        ]