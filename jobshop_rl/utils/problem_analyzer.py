"""
Utilidades para analizar problemas de Job Shop y calcular límites inferiores.

Soporta tanto problemas determinísticos (escalares) como problemas con
incertidumbre (intervalos) en los tiempos de procesamiento.
"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple, Union

from jobshop_rl.models.interval import Interval


class MakespanBoundCalculator:
    """
    Calcula diversos límites inferiores para el makespan.
    
    Soporta tanto duraciones escalares como intervalos.
    Los límites inferiores para problemas con intervalos también son intervalos.
    """
    
    @staticmethod
    def capacity_bound(
        sequences: List[List[int]], 
        durations: List[List[Union[int, Interval]]]
    ) -> Union[float, Interval]:
        """
        Cálculo del límite de capacidad (carga máxima en una máquina).
        
        Relaja las restricciones de precedencia y considera solo la capacidad
        de cada máquina.
        
        Para intervalos: usa aritmética de intervalos para calcular cargas.
        
        Args:
            sequences: Secuencias de máquinas de cada trabajo
            durations: Duraciones de las operaciones (escalares o intervalos)
            
        Returns:
            Límite inferior de capacidad (escalar o intervalo)
        """
        num_jobs = len(sequences)
        num_machines = max(max(seq) for seq in sequences) + 1 if sequences else 0
        
        # Detect if we have intervals
        has_intervals = any(
            isinstance(dur, Interval) 
            for job_durs in durations 
            for dur in job_durs
        )
        
        # Initialize machine loads
        if has_intervals:
            machine_loads = [Interval(0, 0) for _ in range(num_machines)]
        else:
            machine_loads = [0] * num_machines
        
        # Calculate total load per machine
        for j in range(num_jobs):
            for op_idx, machine in enumerate(sequences[j]):
                machine_loads[machine] += durations[j][op_idx]
        
        # Return maximum load (lexicographic for intervals)
        return max(machine_loads)
    
    @staticmethod
    def critical_path_bound(
        sequences: List[List[int]], 
        durations: List[List[Union[int, Interval]]]
    ) -> Union[float, Interval]:
        """
        Cálculo del límite del camino crítico (camino más largo en un trabajo).
        
        Relaja las restricciones de recursos y considera solo la precedencia
        dentro de cada trabajo.
        
        Para intervalos: suma las duraciones de cada trabajo usando aritmética
        de intervalos.
        
        Args:
            sequences: Secuencias de máquinas de cada trabajo
            durations: Duraciones de las operaciones (escalares o intervalos)
            
        Returns:
            Límite inferior del camino crítico (escalar o intervalo)
        """
        num_jobs = len(sequences)
        
        # Detect if we have intervals
        has_intervals = any(
            isinstance(dur, Interval) 
            for job_durs in durations 
            for dur in job_durs
        )
        
        # Calculate path length for each job
        job_paths = []
        for j in range(num_jobs):
            if has_intervals:
                # Sum using interval arithmetic
                path_length = sum(durations[j], Interval(0, 0))
            else:
                # Regular sum for scalars
                path_length = sum(durations[j])
            job_paths.append(path_length)
        
        # Return maximum (lexicographic for intervals)
        return max(job_paths)
    
    @staticmethod
    def one_machine_relaxation(
        sequences: List[List[int]], 
        durations: List[List[Union[int, Interval]]]
    ) -> Union[float, Interval]:
        """
        Relajación de una máquina (considera solo las operaciones en la máquina más cargada).
        
        Identifica la máquina bottleneck y calcula un límite inferior considerando
        solo las operaciones en esa máquina.
        
        Para intervalos: usa aritmética de intervalos para todos los cálculos.
        
        Args:
            sequences: Secuencias de máquinas de cada trabajo
            durations: Duraciones de las operaciones (escalares o intervalos)
            
        Returns:
            Límite inferior de relajación de una máquina (escalar o intervalo)
        """
        num_jobs = len(sequences)
        num_machines = max(max(seq) for seq in sequences) + 1 if sequences else 0
        
        # Detect if we have intervals
        has_intervals = any(
            isinstance(dur, Interval) 
            for job_durs in durations 
            for dur in job_durs
        )
        
        # Identify the bottleneck machine (highest total load)
        if has_intervals:
            machine_loads = [Interval(0, 0) for _ in range(num_machines)]
        else:
            machine_loads = [0] * num_machines
            
        for j in range(num_jobs):
            for op_idx, machine in enumerate(sequences[j]):
                machine_loads[machine] += durations[j][op_idx]
        
        # Find bottleneck machine
        # For intervals, use lexicographic comparison (upper, then lower)
        bottleneck_machine = 0
        max_load = machine_loads[0]
        for m in range(1, num_machines):
            if machine_loads[m] > max_load:
                max_load = machine_loads[m]
                bottleneck_machine = m
        
        # Collect operations data for bottleneck machine
        operations_data = []  # (job_id, op_idx, processing_time, release_time, tail_time)
        
        for j in range(num_jobs):
            # Find the operation that uses the bottleneck machine
            bottleneck_op_idx = None
            for idx, machine in enumerate(sequences[j]):
                if machine == bottleneck_machine:
                    bottleneck_op_idx = idx
                    break
            
            if bottleneck_op_idx is not None:
                # Calculate times before and after the bottleneck operation
                if has_intervals:
                    # Use interval arithmetic
                    if bottleneck_op_idx > 0:
                        release_time = sum(durations[j][:bottleneck_op_idx], Interval(0, 0))
                    else:
                        release_time = Interval(0, 0)
                    
                    processing_time = durations[j][bottleneck_op_idx]
                    
                    if bottleneck_op_idx < len(durations[j]) - 1:
                        tail_time = sum(durations[j][bottleneck_op_idx+1:], Interval(0, 0))
                    else:
                        tail_time = Interval(0, 0)
                else:
                    # Regular arithmetic for scalars
                    release_time = sum(durations[j][:bottleneck_op_idx])
                    processing_time = durations[j][bottleneck_op_idx]
                    tail_time = sum(durations[j][bottleneck_op_idx+1:])
                
                operations_data.append((j, bottleneck_op_idx, processing_time, release_time, tail_time))
        
        # Calculate lower bounds using the formula
        
        # 1. Sum of all processing times on the bottleneck machine
        if has_intervals:
            sum_processing_times = sum(
                (op[2] for op in operations_data), 
                Interval(0, 0)
            )
        else:
            sum_processing_times = sum(op[2] for op in operations_data)
        
        # 2. Maximum of r_i + p_i + q_i for all operations
        if operations_data:
            max_critical_path = operations_data[0][3] + operations_data[0][2] + operations_data[0][4]
            
            for _, _, p_i, r_i, q_i in operations_data[1:]:
                critical_path = r_i + p_i + q_i
                if critical_path > max_critical_path:
                    max_critical_path = critical_path
        else:
            if has_intervals:
                max_critical_path = Interval(0, 0)
            else:
                max_critical_path = 0
        
        # The lower bound is the maximum of these two values
        return max(sum_processing_times, max_critical_path)
    
    @staticmethod
    def get_best_lower_bound(
        sequences: List[List[int]], 
        durations: List[List[Union[int, Interval]]]
    ) -> Union[float, Interval]:
        """
        Devuelve el mejor (más alto) límite inferior calculado.
        
        Para intervalos, usa comparación lexicográfica.
        
        Args:
            sequences: Secuencias de máquinas de cada trabajo
            durations: Duraciones de las operaciones (escalares o intervalos)
            
        Returns:
            El mejor límite inferior calculado (escalar o intervalo)
        """
        bounds = [
            MakespanBoundCalculator.capacity_bound(sequences, durations),
            MakespanBoundCalculator.critical_path_bound(sequences, durations),
            MakespanBoundCalculator.one_machine_relaxation(sequences, durations)
        ]
        
        # Use lexicographic max for intervals
        return max(bounds)
    
    @staticmethod
    def get_all_bounds(
        sequences: List[List[int]], 
        durations: List[List[Union[int, Interval]]]
    ) -> Dict[str, Union[float, Interval]]:
        """
        Calcula y devuelve todos los límites inferiores disponibles.
        
        Args:
            sequences: Secuencias de máquinas de cada trabajo
            durations: Duraciones de las operaciones (escalares o intervalos)
            
        Returns:
            Diccionario con los diferentes límites inferiores calculados
        """
        return {
            "capacity": MakespanBoundCalculator.capacity_bound(sequences, durations),
            "critical_path": MakespanBoundCalculator.critical_path_bound(sequences, durations),
            "one_machine": MakespanBoundCalculator.one_machine_relaxation(sequences, durations),
        }


class ProblemAnalyzer:
    """
    Analiza problemas de Job Shop para extraer características e información útil.
    
    Soporta tanto problemas determinísticos como problemas con intervalos.
    """
    
    @staticmethod
    def analyze_problem(
        sequences: List[List[int]], 
        durations: List[List[Union[int, Interval]]]
    ) -> Dict[str, Any]:
        """
        Analiza un problema y devuelve sus características clave.
        
        Para problemas con intervalos, las estadísticas también son intervalos.
        
        Args:
            sequences: Secuencias de máquinas de cada trabajo
            durations: Duraciones de las operaciones (escalares o intervalos)
            
        Returns:
            Diccionario con las características del problema y límites calculados
        """
        num_jobs = len(sequences)
        num_machines = max(max(seq) for seq in sequences) + 1 if sequences else 0
        
        # Detect if we have intervals
        has_intervals = any(
            isinstance(dur, Interval) 
            for job_durs in durations 
            for dur in job_durs
        )
        
        # Basic characteristics
        if has_intervals:
            # Total work as interval
            total_work = Interval(0, 0)
            for job in durations:
                total_work = total_work + sum(job, Interval(0, 0))
            
            # Average operation duration
            total_ops = num_jobs * num_machines
            if total_ops > 0:
                # Use midpoint for average
                avg_op_duration = total_work.midpoint / total_ops
            else:
                avg_op_duration = 0
            
            # Max and min operation durations
            # For intervals, use lexicographic comparison
            all_durations = [dur for job in durations for dur in job]
            max_op_duration = max(all_durations)
            min_op_duration = min(all_durations)
            
            # Duration variability (use interval widths)
            duration_widths = [
                dur.width if isinstance(dur, Interval) else 0 
                for dur in all_durations
            ]
            duration_std = np.std(duration_widths) if duration_widths else 0
        else:
            # Regular scalar calculations
            total_work = sum(sum(job) for job in durations)
            avg_op_duration = total_work / (num_jobs * num_machines) if num_jobs * num_machines > 0 else 0
            max_op_duration = max(max(job) for job in durations) if durations else 0
            min_op_duration = min(min(job) for job in durations) if durations else 0
            
            durations_flat = [d for job in durations for d in job]
            duration_std = np.std(durations_flat) if durations_flat else 0
        
        # Calculate theoretical bounds
        lower_bounds = MakespanBoundCalculator.get_all_bounds(sequences, durations)
        best_lower_bound = max(lower_bounds.values())
        
        # Problem structure - machine loads
        if has_intervals:
            machine_loads = [Interval(0, 0) for _ in range(num_machines)]
        else:
            machine_loads = [0] * num_machines
            
        for j in range(num_jobs):
            for op_idx, machine in enumerate(sequences[j]):
                machine_loads[machine] += durations[j][op_idx]
        
        # Load variance (for intervals, use midpoints)
        if has_intervals:
            load_values = [load.midpoint for load in machine_loads]
        else:
            load_values = machine_loads
            
        load_variance = np.var(load_values)
        avg_load = sum(load_values) / num_machines if num_machines > 0 else 0
        bottleneck_ratio = max(load_values) / avg_load if avg_load > 0 else 1.0
        
        # Identify bottleneck machine (use lexicographic comparison for intervals)
        bottleneck_machine = 0
        max_load = machine_loads[0]
        for m in range(1, num_machines):
            if machine_loads[m] > max_load:
                max_load = machine_loads[m]
                bottleneck_machine = m
        
        analysis = {
            "num_jobs": num_jobs,
            "num_machines": num_machines,
            "has_intervals": has_intervals,
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
        
        return analysis


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
        
        # Adapt parameters based on problem size/complexity
        num_jobs = problem_analysis["num_jobs"]
        num_machines = problem_analysis["num_machines"]
        
        # Larger problems need more exploration
        if num_jobs * num_machines > 100:
            config["entropy_coef"] = 0.03
            config["K_epochs"] = 5
        
        # Problems with high variability need lower learning rate
        avg_duration = problem_analysis.get("avg_op_duration", 1)
        duration_std = problem_analysis.get("duration_std", 0)
        
        # Handle interval case (avg_duration might be Interval)
        if isinstance(avg_duration, Interval):
            avg_duration = avg_duration.midpoint
            
        if duration_std > avg_duration * 1.5:
            config["lr"] = 0.0002
        
        # For interval problems, increase exploration
        if problem_analysis.get("has_intervals", False):
            config["entropy_coef"] *= 1.2
            
        return config
    
    @staticmethod
    def generate_reward_config(problem_analysis: Dict) -> Dict:
        """Genera configuración para la estrategia de recompensa basada en el análisis"""
        # Calculate weights adapted to characteristics
        weights = {
            "makespan_weight": 1.0,
            "idle_weight": 0.2,
            "critical_weight": 0.1,
            "balance_weight": 0.05,
            "progress_weight": 0.2,
            "local_improvement_weight": 0.15,
        }
        
        # Adapt weights based on characteristics
        avg_duration = problem_analysis.get("avg_op_duration", 1)
        
        # Handle interval case
        if isinstance(avg_duration, Interval):
            avg_duration = avg_duration.midpoint
        
        # If there is high variance between jobs, increase critical_weight
        if problem_analysis.get("load_variance", 0) > 0 and avg_duration > 0:
            weights["balance_weight"] = min(
                0.1, 
                0.05 + 0.01 * (problem_analysis["load_variance"] / avg_duration)
            )
            
        # If there is a clear bottleneck, increase idle_weight
        if "bottleneck_ratio" in problem_analysis:
            weights["idle_weight"] = min(
                0.3, 
                0.2 + 0.02 * (problem_analysis["bottleneck_ratio"] - 1) * 10
            )
        
        # For interval problems, increase progress_weight (reward making progress despite uncertainty)
        if problem_analysis.get("has_intervals", False):
            weights["progress_weight"] *= 1.3
            
        return weights
