"""
Mejoras en las características para problemas con intervalos.

Este módulo proporciona funciones para calcular características normalizadas
y con información de incertidumbre para mejorar el aprendizaje con intervalos.
"""

import numpy as np
from typing import List, Dict, Union, Optional, Tuple
from dataclasses import dataclass

from jobshop_rl.models.interval import Interval


@dataclass
class ImprovedOperationFeatures:
    """
    Características mejoradas de una operación para problemas con intervalos.
    
    Añade:
    - Normalización por el lower bound del problema
    - Características de incertidumbre (anchura de intervalos)
    - Características relativas (en lugar de absolutas)
    
    Dimensiones:
    - Escalares: 7 características (sin cambios para backward compatibility)
    - Intervalos: 14 características (expandido con info de incertidumbre)
    """
    job_id: int
    op_idx: int
    machine: int
    num_jobs: int
    num_machines: int
    duration: Union[int, Interval]
    earliest_start: Union[int, Interval]
    remaining_time: Union[int, Interval]
    remaining_ops: int
    
    # Para normalización
    lower_bound: float = 1.0  # Límite inferior del makespan para normalizar
    max_duration: float = 1.0  # Duración máxima para normalizar
    
    def to_array(self, normalize: bool = True) -> List[float]:
        """
        Convierte las características a un array para la red neuronal.
        
        Para intervalos, incluye:
        - Valores normalizados (lower y upper divididos por lower_bound)
        - Anchura de incertidumbre normalizada
        - Características relativas (progreso en el trabajo)
        
        Args:
            normalize: Si normalizar las características (recomendado para intervalos)
        
        Returns:
            Lista de características en formato float
        """
        has_intervals = (isinstance(self.duration, Interval) or 
                        isinstance(self.earliest_start, Interval) or 
                        isinstance(self.remaining_time, Interval))
        
        # Factor de normalización (evitar división por cero)
        norm_factor = max(self.lower_bound, 1.0) if normalize else 1.0
        dur_norm = max(self.max_duration, 1.0) if normalize else 1.0
        
        if has_intervals:
            # Extraer bounds de intervalos
            dur_lower = self.duration.lower if isinstance(self.duration, Interval) else float(self.duration)
            dur_upper = self.duration.upper if isinstance(self.duration, Interval) else float(self.duration)
            
            start_lower = (self.earliest_start.lower if isinstance(self.earliest_start, Interval) 
                          else float(self.earliest_start))
            start_upper = (self.earliest_start.upper if isinstance(self.earliest_start, Interval) 
                          else float(self.earliest_start))
            
            rem_lower = (self.remaining_time.lower if isinstance(self.remaining_time, Interval) 
                        else float(self.remaining_time))
            rem_upper = (self.remaining_time.upper if isinstance(self.remaining_time, Interval) 
                        else float(self.remaining_time))
            
            # Calcular características de incertidumbre (anchura normalizada)
            dur_uncertainty = (dur_upper - dur_lower) / dur_norm
            start_uncertainty = (start_upper - start_lower) / norm_factor
            rem_uncertainty = (rem_upper - rem_lower) / norm_factor
            
            # Calcular progreso normalizado en el trabajo (0 a 1)
            progress = self.op_idx / max(self.num_machines - 1, 1)
            
            # Calcular índices normalizados
            job_norm = self.job_id / max(self.num_jobs - 1, 1)
            machine_norm = self.machine / max(self.num_machines - 1, 1)
            remaining_ops_norm = self.remaining_ops / max(self.num_machines, 1)
            
            return [
                # Índices normalizados (3 features)
                job_norm,
                progress,  # En lugar de op_idx absoluto
                machine_norm,
                
                # Duración normalizada (2 features)
                dur_lower / dur_norm,
                dur_upper / dur_norm,
                
                # Earliest start normalizado (2 features)  
                start_lower / norm_factor,
                start_upper / norm_factor,
                
                # Remaining time normalizado (2 features)
                rem_lower / norm_factor,
                rem_upper / norm_factor,
                
                # Operaciones restantes normalizadas (1 feature)
                remaining_ops_norm,
                
                # NUEVAS: Características de incertidumbre (3 features)
                dur_uncertainty,
                start_uncertainty,
                rem_uncertainty,
                
                # NUEVA: Midpoint de duración normalizado (útil para comparación directa)
                (dur_lower + dur_upper) / (2 * dur_norm),
            ]
        else:
            # Características escalares originales (7 features) para backward compatibility
            return [
                float(self.job_id) / max(self.num_jobs - 1, 1),
                float(self.op_idx) / max(self.num_machines - 1, 1),
                float(self.machine) / max(self.num_machines - 1, 1),
                float(self.duration) / dur_norm,
                float(self.earliest_start) / norm_factor,
                float(self.remaining_time) / norm_factor,
                float(self.remaining_ops) / max(self.num_machines, 1)
            ]
    
    @property
    def feature_dimension(self) -> int:
        """
        Get the number of features this operation will produce.
        
        Returns:
            7 for scalar problems, 14 for interval problems (expanded)
        """
        has_intervals = (isinstance(self.duration, Interval) or 
                        isinstance(self.earliest_start, Interval) or 
                        isinstance(self.remaining_time, Interval))
        return 14 if has_intervals else 7


def get_improved_features(
    env,
    state: Dict,
    normalize: bool = True
) -> np.ndarray:
    """
    Extrae características mejoradas para todas las operaciones elegibles.
    
    Esta función reemplaza a env.get_features() con características mejor
    diseñadas para problemas con intervalos:
    
    1. Normalización por el lower bound del makespan
    2. Características de incertidumbre (anchura de intervalos)
    3. Características relativas en lugar de absolutas
    
    Args:
        env: Entorno JobShopEnv
        state: Estado actual del entorno
        normalize: Si normalizar las características
        
    Returns:
        Array de características (n_ops, feature_dim)
        - feature_dim = 7 para escalares
        - feature_dim = 14 para intervalos (expandido)
    """
    features = []
    
    # Obtener parámetros de normalización del análisis del problema
    if hasattr(env, 'problem_analysis') and env.problem_analysis:
        lower_bound = env.problem_analysis.get('best_lower_bound', 1.0)
        if isinstance(lower_bound, Interval):
            # Usar el midpoint del lower bound para normalización
            norm_factor = (lower_bound.lower + lower_bound.upper) / 2
        else:
            norm_factor = float(lower_bound)
        
        max_duration = env.problem_analysis.get('max_op_duration', 1.0)
        if isinstance(max_duration, Interval):
            max_dur = max_duration.upper
        else:
            max_dur = float(max_duration)
    else:
        # Calcular valores por defecto
        norm_factor = env.num_jobs * env.num_machines * 10  # Estimación conservadora
        max_dur = 100.0
    
    for job_id in state['eligible_ops']:
        op_idx = state['job_status'][job_id]
        machine = env.sequences[job_id][op_idx]
        duration = env.durations[job_id][op_idx]

        # Calcular earliest start
        job_completion = state['job_completion_time'][job_id]
        machine_completion = state['machine_completion_time'][machine]
        
        if env.has_intervals:
            earliest_start = Interval.max(job_completion, machine_completion)
        else:
            earliest_start = max(job_completion, machine_completion)

        # Calcular remaining time
        remaining_ops = env.num_machines - op_idx - 1
        
        if remaining_ops > 0:
            remaining_durations = env.durations[job_id][op_idx+1:]
            if env.has_intervals:
                remaining_time = sum(remaining_durations, Interval(0, 0))
            else:
                remaining_time = sum(remaining_durations)
        else:
            if env.has_intervals:
                remaining_time = Interval(0, 0)
            else:
                remaining_time = 0

        # Crear objeto de características mejoradas
        op_features = ImprovedOperationFeatures(
            job_id=job_id,
            op_idx=op_idx,
            machine=machine,
            num_jobs=env.num_jobs,
            num_machines=env.num_machines,
            duration=duration,
            earliest_start=earliest_start,
            remaining_time=remaining_time,
            remaining_ops=remaining_ops,
            lower_bound=norm_factor,
            max_duration=max_dur
        )

        features.append(op_features.to_array(normalize=normalize))

    if not features:
        feature_dim = 14 if env.has_intervals else 7
        return np.zeros((0, feature_dim))

    return np.array(features)


def compute_urgency_features(
    env,
    state: Dict
) -> np.ndarray:
    """
    Calcula características de urgencia para cada operación elegible.
    
    La urgencia se basa en cuánto retraso potencial puede causar una operación
    si no se planifica pronto.
    
    Returns:
        Array de urgencia (n_ops,)
    """
    urgencies = []
    
    for job_id in state['eligible_ops']:
        op_idx = state['job_status'][job_id]
        
        # Calcular tiempo restante del trabajo
        remaining_ops = env.num_machines - op_idx
        remaining_durations = env.durations[job_id][op_idx:]
        
        if env.has_intervals:
            total_remaining = sum(remaining_durations, Interval(0, 0))
            # Usar el upper bound como indicador de urgencia (peor caso)
            urgency = total_remaining.upper * remaining_ops
        else:
            total_remaining = sum(remaining_durations)
            urgency = total_remaining * remaining_ops
        
        urgencies.append(urgency)
    
    if not urgencies:
        return np.array([])
    
    # Normalizar urgencias
    urgencies = np.array(urgencies)
    if urgencies.max() > 0:
        urgencies = urgencies / urgencies.max()
    
    return urgencies
