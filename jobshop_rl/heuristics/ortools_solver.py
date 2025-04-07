"""
Implementación de un solucionador de Job Shop Scheduling usando Google OR-Tools.
"""

import time
import logging
import os
from typing import Dict, List, Tuple, Any

# Configuración de logging
logger = logging.getLogger("JobShopRL.ORToolsSolver")

# Importación condicional de OR-Tools
try:
    from ortools.sat.python import cp_model
    ORTOOLS_AVAILABLE = True
    logger.info("Google OR-Tools importado correctamente.")
except ImportError:
    ORTOOLS_AVAILABLE = False
    logger.warning("Google OR-Tools no está instalado. El solucionador OR-Tools no estará disponible.")
    logger.warning("Para instalar OR-Tools: pip install ortools")

logger = logging.getLogger("JobShopRL.ORToolsSolver")

class JobShopORToolsSolver:
    """Solucionador de Job Shop Scheduling usando Google OR-Tools CP-SAT solver"""

    @staticmethod
    def check_ortools_availability():
        """Comprueba si OR-Tools está disponible"""
        return ORTOOLS_AVAILABLE

    @staticmethod
    def solve(sequences: List[List[int]], durations: List[List[int]], 
              time_limit_seconds: int = 60) -> Tuple[int, List[Dict], float]:
        """
        Resuelve un problema de Job Shop Scheduling usando CP-SAT solver de OR-Tools.
        
        Args:
            sequences: Lista de secuencias de máquinas para cada trabajo
            durations: Lista de duraciones para cada operación de cada trabajo
            time_limit_seconds: Tiempo límite para la búsqueda en segundos
            
        Returns:
            Tupla con (makespan, schedule, tiempo_ejecución)
            - makespan: El makespan de la solución encontrada
            - schedule: Lista de diccionarios, cada uno con datos de una operación programada
            - tiempo_ejecución: Tiempo en segundos empleado por el solver
        """
        if not ORTOOLS_AVAILABLE:
            logger.error("Google OR-Tools no está instalado. No se puede resolver el problema.")
            return float('inf'), [], 0
            
        # Verificar que los datos de entrada son válidos
        if not sequences or not durations:
            logger.error("Secuencias o duraciones vacías. No se puede resolver el problema.")
            return float('inf'), [], 0
            
        # Verificar dimensiones
        if len(sequences) != len(durations):
            logger.error(f"Dimensiones inconsistentes: {len(sequences)} trabajos en secuencias vs {len(durations)} en duraciones")
            return float('inf'), [], 0
            
        # Verificar que todas las secuencias tienen la misma longitud
        lengths = set(len(seq) for seq in sequences)
        if len(lengths) > 1:
            logger.error(f"No todas las secuencias tienen la misma longitud: {lengths}")
            return float('inf'), [], 0
            
        # Lo mismo para las duraciones
        lengths = set(len(dur) for dur in durations)
        if len(lengths) > 1:
            logger.error(f"No todas las listas de duraciones tienen la misma longitud: {lengths}")
            return float('inf'), [], 0
            
        start_time = time.time()
        
        # Crear el modelo
        model = cp_model.CpModel()
        
        num_jobs = len(sequences)
        num_machines = len(sequences[0])  # Asumimos que todos los trabajos tienen el mismo número de operaciones
        
        # Diccionario para almacenar intervalos de tareas
        all_tasks = {}
        # Diccionario para almacenar variables de inicio para cada tarea
        all_starts = {}
        # Diccionario para almacenar variables de finalización para cada tarea
        all_ends = {}
        
        # Crear variables de intervalo para cada operación
        horizon = sum(sum(durations[j]) for j in range(num_jobs))
        
        for job_id in range(num_jobs):
            for task_id in range(num_machines):
                machine = sequences[job_id][task_id]
                duration = durations[job_id][task_id]
                
                # Variables para tiempos de inicio y fin
                start_var = model.NewIntVar(0, horizon, f'start_{job_id}_{task_id}')
                end_var = model.NewIntVar(0, horizon, f'end_{job_id}_{task_id}')
                
                # Intervalo que representa la operación
                interval_var = model.NewIntervalVar(start_var, duration, end_var, f'interval_{job_id}_{task_id}')
                
                # Almacenar variables
                all_tasks[(job_id, task_id)] = interval_var
                all_starts[(job_id, task_id)] = start_var
                all_ends[(job_id, task_id)] = end_var
        
        # Restricciones de precedencia en los trabajos
        for job_id in range(num_jobs):
            for task_id in range(num_machines - 1):
                model.Add(all_ends[(job_id, task_id)] <= all_starts[(job_id, task_id + 1)])
        
        # Restricciones de recursos (no solapamiento en las máquinas)
        machines_to_intervals = {}
        
        for job_id in range(num_jobs):
            for task_id in range(num_machines):
                machine = sequences[job_id][task_id]
                if machine not in machines_to_intervals:
                    machines_to_intervals[machine] = []
                machines_to_intervals[machine].append(all_tasks[(job_id, task_id)])
        
        for machine, intervals in machines_to_intervals.items():
            model.AddNoOverlap(intervals)
        
        # Objetivo: minimizar makespan (tiempo de finalización del último trabajo)
        makespan_var = model.NewIntVar(0, horizon, 'makespan')
        for job_id in range(num_jobs):
            model.Add(all_ends[(job_id, num_machines - 1)] <= makespan_var)
        
        model.Minimize(makespan_var)
        
        # Crear el solucionador
        solver = cp_model.CpSolver()
        
        # Configurar tiempo límite
        solver.parameters.max_time_in_seconds = time_limit_seconds
        
        # Añadir callbacks para logging (opcional)
        class SolutionPrinter(cp_model.CpSolverSolutionCallback):
            def __init__(self):
                cp_model.CpSolverSolutionCallback.__init__(self)
                self.solutions = 0
                
            def on_solution_callback(self):
                self.solutions += 1
                makespan = self.Value(makespan_var)
                if self.solutions <= 5:  # Limitar logs para no saturar
                    logger.info(f'Solución #{self.solutions}, makespan actual: {makespan}')
                
        solution_printer = SolutionPrinter()
        
        # Resolver el problema
        logger.info(f"Iniciando OR-Tools CP-SAT solver con tiempo límite de {time_limit_seconds} segundos...")
        status = solver.Solve(model, solution_printer)
        
        # Procesar resultados
        execution_time = time.time() - start_time
        
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            makespan = solver.Value(makespan_var)
            
            # Crear el programa de operaciones
            schedule = []
            for job_id in range(num_jobs):
                for task_id in range(num_machines):
                    machine = sequences[job_id][task_id]
                    start_time = solver.Value(all_starts[(job_id, task_id)])
                    duration = durations[job_id][task_id]
                    end_time = solver.Value(all_ends[(job_id, task_id)])
                    
                    schedule.append({
                        'job': job_id,
                        'task': task_id,
                        'machine': machine,
                        'start': start_time,
                        'duration': duration,
                        'end': end_time
                    })
            
            if status == cp_model.OPTIMAL:
                logger.info(f"Solución óptima encontrada con makespan: {makespan}")
            else:
                logger.info(f"Solución factible encontrada con makespan: {makespan} (no se probó la optimalidad)")
                
            logger.info(f"Tiempo total de ejecución: {execution_time:.4f} segundos")
            
            return makespan, schedule, execution_time
        else:
            logger.warning(f"No se encontró solución. Estado: {solver.StatusName(status)}")
            return float('inf'), [], execution_time
