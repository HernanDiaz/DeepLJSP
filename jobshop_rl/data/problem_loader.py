"""
Cargador de problemas de Job Shop Scheduling desde diferentes formatos.
"""

import os
import json
import csv
import pandas as pd
import numpy as np
import logging
from typing import List, Dict, Any, Optional, Tuple

from jobshop_rl.utils.seed_utils import set_random_seed

logger = logging.getLogger("JobShopRL.ProblemLoader")

class ProblemLoader:
    """Carga problemas de Job Shop desde diferentes formatos de archivo"""
    
    @staticmethod
    def load_from_directory(directory_path: str) -> List[Dict[str, Any]]:
        """
        Carga todos los problemas en un directorio.
        
        Args:
            directory_path: Ruta del directorio con archivos de problemas
            
        Returns:
            Lista de problemas cargados
        """
        problems = []
        
        if not os.path.exists(directory_path):
            logger.error(f"El directorio {directory_path} no existe")
            return problems
            
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            
            # Ignorar directorios
            if os.path.isdir(file_path):
                continue
                
            try:
                # Intentar cargar el problema según su extensión
                if filename.endswith('.json'):
                    problem = ProblemLoader.load_json(file_path)
                elif filename.endswith('.csv'):
                    problem = ProblemLoader.load_csv(file_path)
                elif filename.endswith('.txt'):
                    problem = ProblemLoader.load_taillard(file_path)
                else:
                    logger.warning(f"Formato no soportado para {filename}, omitiendo")
                    continue
                    
                # Añadir nombre del problema basado en el nombre del archivo
                problem['name'] = os.path.splitext(filename)[0]
                problems.append(problem)
                logger.info(f"Problema cargado: {problem['name']}")
                
            except Exception as e:
                logger.error(f"Error al cargar {filename}: {str(e)}")
        
        logger.info(f"Total de problemas cargados: {len(problems)}")
        return problems
    
    @staticmethod
    def load_json(file_path: str) -> Dict[str, Any]:
        """
        Carga un problema desde formato JSON.
        
        Args:
            file_path: Ruta del archivo JSON
            
        Returns:
            Diccionario con los datos del problema
        """
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        # Validar estructura del problema
        required_fields = ['num_jobs', 'num_machines', 'sequences', 'durations']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Campo requerido '{field}' no encontrado en el archivo JSON")
                
        return data
    
    @staticmethod
    def load_csv(file_path: str) -> Dict[str, Any]:
        """
        Carga un problema desde formato CSV.
        
        El formato esperado es:
        - Cada fila representa un trabajo
        - Para cada trabajo, hay pares (máquina, duración) consecutivos
        
        Args:
            file_path: Ruta del archivo CSV
            
        Returns:
            Diccionario con los datos del problema
        """
        df = pd.read_csv(file_path)
        
        # Detectar número de trabajos y máquinas
        num_jobs = len(df)
        num_machines = (len(df.columns) - 1) // 2  # -1 para excluir la columna de índice si existe
        
        # Inicializar listas para secuencias y duraciones
        sequences = []
        durations = []
        
        # Procesar cada trabajo
        for _, row in df.iterrows():
            job_machines = []
            job_durations = []
            
            # Recorrer pares (máquina, duración)
            for i in range(num_machines):
                machine_col = f"machine_{i}" if f"machine_{i}" in df.columns else i * 2
                duration_col = f"duration_{i}" if f"duration_{i}" in df.columns else i * 2 + 1
                
                machine = int(row[machine_col])
                duration = int(row[duration_col])
                
                job_machines.append(machine)
                job_durations.append(duration)
            
            sequences.append(job_machines)
            durations.append(job_durations)
        
        # Crear diccionario de problema
        problem = {
            'num_jobs': num_jobs,
            'num_machines': num_machines,
            'sequences': sequences,
            'durations': durations
        }
        
        # Extraer valor óptimo si está presente
        if 'optimal' in df.columns:
            problem['optimal_makespan'] = int(df['optimal'].iloc[0])
        
        return problem
    
    @staticmethod
    def load_taillard(file_path: str) -> Dict[str, Any]:
        """
        Carga un problema en formato Taillard (común en benchmarks).
        
        El formato Taillard tiene:
        - Número de trabajos y máquinas en la primera línea
        - Matriz de tiempos de procesamiento
        - Matriz de secuencias de máquinas
        
        Args:
            file_path: Ruta del archivo Taillard
            
        Returns:
            Diccionario con los datos del problema
        """
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # Eliminar líneas vacías y comentarios
        lines = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
        
        # Primera línea: num_jobs num_machines [optimal]
        parts = lines[0].split()
        num_jobs = int(parts[0])
        num_machines = int(parts[1])
        optimal_makespan = int(parts[2]) if len(parts) > 2 else None
        
        # Inicializar matrices
        sequences = [[] for _ in range(num_jobs)]
        durations = [[] for _ in range(num_jobs)]
        
        # Leer matriz de tiempos (cada fila es un trabajo)
        line_index = 1
        for j in range(num_jobs):
            if line_index >= len(lines):
                raise ValueError(f"No hay suficientes líneas en el archivo para {num_jobs} trabajos")
                
            parts = lines[line_index].split()
            line_index += 1
            
            if len(parts) < num_machines * 2:
                raise ValueError(f"No hay suficientes datos para el trabajo {j}: se esperaban {num_machines*2} valores")
                
            for m in range(num_machines):
                machine = int(parts[m*2])
                time = int(parts[m*2+1])
                sequences[j].append(machine)
                durations[j].append(time)
        
        # Crear diccionario de problema
        problem = {
            'num_jobs': num_jobs,
            'num_machines': num_machines,
            'sequences': sequences,
            'durations': durations
        }
        
        if optimal_makespan is not None:
            problem['optimal_makespan'] = optimal_makespan
        
        return problem
        
    @staticmethod
    def save_problem(problem: Dict[str, Any], file_path: str, format: str = 'json'):
        """
        Guarda un problema en un archivo.
        
        Args:
            problem: Diccionario con los datos del problema
            file_path: Ruta donde guardar el archivo
            format: Formato de salida ('json', 'csv', 'taillard')
        """
        # Validar datos del problema
        required_fields = ['num_jobs', 'num_machines', 'sequences', 'durations']
        for field in required_fields:
            if field not in problem:
                raise ValueError(f"Campo requerido '{field}' no encontrado en el problema")
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        
        # Guardar en el formato especificado
        if format.lower() == 'json':
            with open(file_path, 'w') as f:
                json.dump(problem, f, indent=2)
        elif format.lower() == 'csv':
            # Crear DataFrame
            rows = []
            for j in range(problem['num_jobs']):
                row = {}
                for m in range(problem['num_machines']):
                    row[f'machine_{m}'] = problem['sequences'][j][m]
                    row[f'duration_{m}'] = problem['durations'][j][m]
                rows.append(row)
            
            df = pd.DataFrame(rows)
            
            # Añadir valor óptimo si existe
            if 'optimal_makespan' in problem:
                df['optimal'] = problem['optimal_makespan']
                
            # Guardar CSV
            df.to_csv(file_path, index=False)
        elif format.lower() == 'taillard':
            with open(file_path, 'w') as f:
                # Escribir encabezado
                header = f"{problem['num_jobs']} {problem['num_machines']}"
                if 'optimal_makespan' in problem:
                    header += f" {problem['optimal_makespan']}"
                f.write(header + '\n')
                
                # Escribir datos de cada trabajo
                for j in range(problem['num_jobs']):
                    line = ""
                    for m in range(problem['num_machines']):
                        line += f"{problem['sequences'][j][m]} {problem['durations'][j][m]} "
                    f.write(line.strip() + '\n')
        else:
            raise ValueError(f"Formato de salida '{format}' no soportado")
        
        logger.info(f"Problema guardado en {file_path}")
        
    @staticmethod
    def generate_random_problem(num_jobs: int, num_machines: int, min_duration: int = 1, 
                               max_duration: int = 100, seed: Optional[int] = None) -> Dict[str, Any]:
        """
        Genera un problema aleatorio de Job Shop.
        
        Args:
            num_jobs: Número de trabajos
            num_machines: Número de máquinas
            min_duration: Duración mínima de operaciones
            max_duration: Duración máxima de operaciones
            seed: Semilla para reproducibilidad
            
        Returns:
            Diccionario con el problema generado
        """
        # Establecer semilla para reproducibilidad usando la utilidad centralizada
        set_random_seed(seed)
        
        # Generar secuencias de máquinas (permutaciones aleatorias)
        sequences = []
        for _ in range(num_jobs):
            perm = np.random.permutation(num_machines).tolist()
            sequences.append(perm)
        
        # Generar duraciones aleatorias
        durations = []
        for _ in range(num_jobs):
            job_durations = np.random.randint(min_duration, max_duration + 1, size=num_machines).tolist()
            durations.append(job_durations)
        
        return {
            'num_jobs': num_jobs,
            'num_machines': num_machines,
            'sequences': sequences,
            'durations': durations
        }
