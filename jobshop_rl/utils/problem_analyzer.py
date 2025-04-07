"""
Utilidades para analizar problemas de Job Shop y calcular límites inferiores.
"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple

class MakespanBoundCalculator:
    """Calcula diversos límites inferiores para el makespan"""
    
    @staticmethod
    def capacity_bound(sequences: List[List[int]], durations: List[List[int]]) -> float:
        """Cálculo del límite de capacidad (carga máxima en una máquina)"""
        num_jobs = len(sequences)
        num_machines = max(max(seq) for seq in sequences) + 1 if sequences else 0
        
        # Carga total por máquina (relaja restricciones de precedencia)
        machine_loads = [0] * num_machines
        for j in range(num_jobs):
            for op_idx, machine in enumerate(sequences[j]):
                machine_loads[machine] += durations[j][op_idx]
        
        # La máquina más cargada es un límite inferior
        return max(machine_loads)
    
    @staticmethod
    def critical_path_bound(sequences: List[List[int]], durations: List[List[int]]) -> float:
        """Cálculo del límite del camino crítico (camino más largo en un trabajo)"""
        num_jobs = len(sequences)
        
        # Longitud del camino crítico para cada trabajo (relaja restricciones de recursos)
        job_paths = [sum(durations[j]) for j in range(num_jobs)]
        
        # El trabajo más largo es un límite inferior
        return max(job_paths)
    
    @staticmethod
    def one_machine_relaxation(sequences: List[List[int]], durations: List[List[int]]) -> float:
        """Relajación de una máquina (considera solo las operaciones en la máquina más cargada)"""
        num_jobs = len(sequences)
        num_machines = max(max(seq) for seq in sequences) + 1 if sequences else 0
        
        # Identificar la máquina más cargada
        machine_loads = [0] * num_machines
        for j in range(num_jobs):
            for op_idx, machine in enumerate(sequences[j]):
                machine_loads[machine] += durations[j][op_idx]
                
        bottleneck_machine = machine_loads.index(max(machine_loads))
        
        # Calcular datos para operaciones en la máquina más cargada
        operations_data = []  # Lista para almacenar (job_id, op_idx, processing_time, release_time, tail_time)
        
        for j in range(num_jobs):
            # Encontrar la operación que usa la máquina bottleneck
            bottleneck_op_idx = None
            for idx, machine in enumerate(sequences[j]):
                if machine == bottleneck_machine:
                    bottleneck_op_idx = idx
                    break
            
            if bottleneck_op_idx is not None:
                # Calcular tiempos antes y después de la operación en la bottleneck
                release_time = sum(durations[j][:bottleneck_op_idx])
                processing_time = durations[j][bottleneck_op_idx]
                tail_time = sum(durations[j][bottleneck_op_idx+1:])
                
                operations_data.append((j, bottleneck_op_idx, processing_time, release_time, tail_time))
        
        # Calcular límites inferiores usando la fórmula correcta
        
        # 1. Suma de todos los tiempos de procesamiento en la máquina bottleneck
        sum_processing_times = sum(op[2] for op in operations_data)
        
        # 2. Máximo de r_i + p_i + q_i para todas las operaciones
        max_critical_path = 0
        for _, _, p_i, r_i, q_i in operations_data:
            critical_path = r_i + p_i + q_i
            max_critical_path = max(max_critical_path, critical_path)
        
        # El límite inferior es el máximo de estos dos valores
        return max(sum_processing_times, max_critical_path)
    
    @staticmethod
    def get_best_lower_bound(sequences: List[List[int]], durations: List[List[int]]) -> float:
        """
        Devuelve el mejor (más alto) límite inferior calculado
        
        Args:
            sequences: Secuencias de máquinas de cada trabajo
            durations: Duraciones de las operaciones
            
        Returns:
            El mejor límite inferior calculado
        """
        bounds = [
            MakespanBoundCalculator.capacity_bound(sequences, durations),
            MakespanBoundCalculator.critical_path_bound(sequences, durations),
            MakespanBoundCalculator.one_machine_relaxation(sequences, durations)
        ]
        
        return max(bounds)
    
    @staticmethod
    def get_all_bounds(sequences: List[List[int]], durations: List[List[int]]) -> Dict[str, float]:
        """
        Calcula y devuelve todos los límites inferiores disponibles
        
        Args:
            sequences: Secuencias de máquinas de cada trabajo
            durations: Duraciones de las operaciones
            
        Returns:
            Diccionario con los diferentes límites inferiores calculados
        """
        return {
            "capacity": MakespanBoundCalculator.capacity_bound(sequences, durations),
            "critical_path": MakespanBoundCalculator.critical_path_bound(sequences, durations),
            "one_machine": MakespanBoundCalculator.one_machine_relaxation(sequences, durations),
        }

class ProblemAnalyzer:
    """Analiza problemas de Job Shop para extraer características e información útil"""
    
    @staticmethod
    def analyze_problem(sequences: List[List[int]], durations: List[List[int]]) -> Dict[str, Any]:
        """
        Analiza un problema y devuelve sus características clave
        
        Args:
            sequences: Secuencias de máquinas de cada trabajo
            durations: Duraciones de las operaciones
            
        Returns:
            Diccionario con las características del problema y límites calculados
        """
        num_jobs = len(sequences)
        num_machines = max(max(seq) for seq in sequences) + 1 if sequences else 0
        
        # Características básicas
        total_work = sum(sum(job) for job in durations)
        avg_op_duration = total_work / (num_jobs * num_machines) if num_jobs * num_machines > 0 else 0
        max_op_duration = max(max(job) for job in durations) if durations else 0
        min_op_duration = min(min(job) for job in durations) if durations else 0
        
        # Variabilidad de duraciones
        durations_flat = [d for job in durations for d in job]
        duration_std = np.std(durations_flat) if durations_flat else 0
        
        # Calcular límites teóricos
        lower_bounds = MakespanBoundCalculator.get_all_bounds(sequences, durations)
        best_lower_bound = max(lower_bounds.values())
        
        # Estructura del problema
        machine_loads = [0] * num_machines
        for j in range(num_jobs):
            for op_idx, machine in enumerate(sequences[j]):
                machine_loads[machine] += durations[j][op_idx]
        
        load_variance = np.var(machine_loads)
        avg_load = sum(machine_loads) / num_machines if num_machines > 0 else 0
        bottleneck_ratio = max(machine_loads) / avg_load if avg_load > 0 else 1.0
        
        # Identificar la máquina bottleneck
        bottleneck_machine = machine_loads.index(max(machine_loads))
        
        return {
            "num_jobs": num_jobs,
            "num_machines": num_machines,
            "total_work": total_work,
            "avg_op_duration": avg_op_duration,
            "max_op_duration": max_op_duration,
            "min_op_duration": min_op_duration,
            "duration_std": duration_std,
            "lower_bounds": lower_bounds,
            "best_lower_bound": best_lower_bound,
            "machine_loads": machine_loads,
            "load_variance": load_variance,
            "bottleneck_ratio": bottleneck_ratio,
            "bottleneck_machine": bottleneck_machine,
        }
        
class AdaptiveConfigGenerator:
    """Genera configuraciones adaptadas a las características del problema"""
    
    @staticmethod
    def generate_agent_config(problem_analysis: Dict) -> Dict:
        """Genera configuración para el agente basada en el análisis del problema"""
        config = {
            "lr": 0.0003,
            "gamma": 0.99,
            "entropy_coef": 0.02,
            "K_epochs": 4,
            "use_lr_decay": True,
            "use_grad_clip": True,
            "advantage_normalization": True,
            "gae_lambda": 0.95,
        }
        
        # Adaptar parámetros según el tamaño/complejidad del problema
        num_jobs = problem_analysis["num_jobs"]
        num_machines = problem_analysis["num_machines"]
        
        # Problemas más grandes necesitan más exploración
        if num_jobs * num_machines > 100:
            config["entropy_coef"] = 0.03
            config["K_epochs"] = 5
        
        # Problemas con alta variabilidad necesitan learning rate más bajo
        if problem_analysis.get("duration_std", 0) > problem_analysis.get("avg_op_duration", 1) * 1.5:
            config["lr"] = 0.0002
            
        return config
    
    @staticmethod
    def generate_reward_config(problem_analysis: Dict) -> Dict:
        """Genera configuración para la estrategia de recompensa basada en el análisis"""
        # Calcular pesos adaptados a las características
        weights = {
            "makespan_weight": 1.0,
            "idle_weight": 0.2,
            "critical_weight": 0.1,
            "balance_weight": 0.05,
            "progress_weight": 0.2,
            "local_improvement_weight": 0.15,
        }
        
        # Adaptar pesos según las características
        # Por ejemplo: si hay mucha variabilidad entre trabajos, aumentar critical_weight
        if problem_analysis.get("load_variance", 0) > 0:
            weights["balance_weight"] = min(0.1, 0.05 + 0.01 * (problem_analysis["load_variance"] / 
                                                           problem_analysis["avg_op_duration"]))
            
        # Si hay un claro bottleneck, aumentar idle_weight
        if "bottleneck_ratio" in problem_analysis:
            weights["idle_weight"] = min(0.3, 0.2 + 0.02 * (problem_analysis["bottleneck_ratio"] - 1) * 10)
            
        return weights
