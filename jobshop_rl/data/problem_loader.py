"""
Cargador de problemas de Job Shop Scheduling desde diferentes formatos.

Soporta tanto problemas determinísticos (escalares) como problemas con
incertidumbre (intervalos) en los tiempos de procesamiento.
"""

import os
import json
import csv
import pandas as pd
import numpy as np
import logging
import re
from typing import List, Dict, Any, Optional, Tuple, Union

from jobshop_rl.utils.seed_utils import set_random_seed
from jobshop_rl.models.interval import Interval

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
    def _parse_duration_value(value_str: str) -> Union[int, Interval]:
        """
        Parsea un valor de duración que puede ser escalar o intervalo.
        
        Formatos soportados:
        - Escalar: "42"
        - Intervalo: "(42,45)" o "[42,45]"
        
        Args:
            value_str: String con el valor a parsear
            
        Returns:
            int o Interval según el formato
            
        Raises:
            ValueError: Si el formato no es válido
        """
        value_str = value_str.strip()
        
        # Check for interval format: (min,max) or [min,max]
        interval_match = re.match(
            r'[\(\[]\s*(\d+\.?\d*)\s*,\s*(\d+\.?\d*)\s*[\)\]]',
            value_str)
        
        if interval_match:
            # Parse as interval
            lower = float(interval_match.group(1))
            upper = float(interval_match.group(2))
            
            # Validate interval
            if lower > upper:
                raise ValueError(f"Intervalo inválido: lower ({lower}) > upper ({upper})")
            
            return Interval(lower, upper)
        else:
            # Parse as scalar
            try:
                # Try int first
                return int(value_str)
            except ValueError:
                # Try float
                try:
                    value = float(value_str)
                    # Convert to Interval for consistency if it's a float
                    return Interval(value, value)
                except ValueError:
                    raise ValueError(f"No se pudo parsear el valor de duración: '{value_str}'")
    
    @staticmethod
    def _format_duration_value(value: Union[int, Interval]) -> str:
        """
        Convierte un valor de duración a string para guardar.
        
        Args:
            value: int o Interval
            
        Returns:
            String con el formato apropiado
        """
        if isinstance(value, Interval):
            if value.is_degenerate:
                # Degenerate interval -> scalar
                return str(int(value.lower) if value.lower == int(value.lower) else value.lower)
            else:
                # Non-degenerate interval -> (lower, upper)
                lower_str = str(int(value.lower) if value.lower == int(value.lower) else value.lower)
                upper_str = str(int(value.upper) if value.upper == int(value.upper) else value.upper)
                return f"({lower_str},{upper_str})"
        else:
            return str(value)
    
    @staticmethod
    def _validate_problem_intervals(problem: Dict[str, Any]) -> None:
        """
        Valida que todos los intervalos en un problema sean válidos.
        
        Args:
            problem: Diccionario con datos del problema
            
        Raises:
            ValueError: Si algún intervalo es inválido
        """
        durations = problem.get('durations', [])
        
        for job_idx, job_durations in enumerate(durations):
            for op_idx, duration in enumerate(job_durations):
                if isinstance(duration, Interval):
                    if duration.lower > duration.upper:
                        raise ValueError(
                            f"Intervalo inválido en job {job_idx}, operación {op_idx}: "
                            f"[{duration.lower}, {duration.upper}]"
                        )
    
    @staticmethod
    def _check_if_interval_problem(problem: Dict[str, Any]) -> bool:
        """
        Verifica si un problema contiene intervalos.
        
        Args:
            problem: Diccionario con datos del problema
            
        Returns:
            True si el problema contiene al menos un intervalo
        """
        durations = problem.get('durations', [])
        
        for job_durations in durations:
            for duration in job_durations:
                if isinstance(duration, Interval) and not duration.is_degenerate:
                    return True
        
        return False
    
    @staticmethod
    def load_json(file_path: str) -> Dict[str, Any]:
        """
        Carga un problema desde formato JSON.
        
        Formatos soportados para duraciones:
        - Escalares: "durations": [[5, 7, 3], ...]
        - Intervalos (array): "durations": [[[5,7], [7,9], [3,3]], ...]
        - Intervalos (dict): "durations": [[{"lower":5,"upper":7}, ...], ...]
        
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
        
        # Procesar duraciones (convertir a Interval si es necesario)
        processed_durations = []
        for job_durations in data['durations']:
            processed_job = []
            for duration in job_durations:
                if isinstance(duration, dict):
                    # Format: {"lower": 5, "upper": 7}
                    if 'lower' in duration and 'upper' in duration:
                        processed_job.append(Interval(duration['lower'], duration['upper']))
                    else:
                        raise ValueError(f"Formato de intervalo inválido en JSON: {duration}")
                elif isinstance(duration, list):
                    # Format: [5, 7] for interval or [5] for scalar
                    if len(duration) == 2:
                        processed_job.append(Interval(duration[0], duration[1]))
                    elif len(duration) == 1:
                        processed_job.append(duration[0])
                    else:
                        raise ValueError(f"Lista de duración debe tener 1 o 2 elementos: {duration}")
                elif isinstance(duration, (int, float)):
                    # Scalar value
                    processed_job.append(int(duration) if isinstance(duration, int) else duration)
                else:
                    raise ValueError(f"Tipo de duración no soportado: {type(duration)}")
            
            processed_durations.append(processed_job)
        
        data['durations'] = processed_durations
        
        # Validar intervalos
        ProblemLoader._validate_problem_intervals(data)
        
        # Marcar si es un problema con intervalos
        data['has_intervals'] = ProblemLoader._check_if_interval_problem(data)
        
        return data
    
    @staticmethod
    def load_csv(file_path: str) -> Dict[str, Any]:
        """
        Carga un problema desde formato CSV.
        
        El formato esperado es:
        - Cada fila representa un trabajo
        - Para cada trabajo, hay pares (máquina, duración) consecutivos
        - Duraciones pueden ser escalares o intervalos en formato (min,max)
        
        Para intervalos, usar columnas pareadas:
        - duration_0_min, duration_0_max, duration_1_min, duration_1_max, ...
        O formato de tupla:
        - duration_0 = "(5,7)", duration_1 = "(3,4)", ...
        
        Args:
            file_path: Ruta del archivo CSV
            
        Returns:
            Diccionario con los datos del problema
        """
        df = pd.read_csv(file_path)
        
        # Detectar número de trabajos
        num_jobs = len(df)
        
        # Intentar detectar formato
        columns = df.columns.tolist()
        
        # Check for min/max column format
        has_min_max_format = any('_min' in col for col in columns)
        
        if has_min_max_format:
            # Formato: machine_0, duration_0_min, duration_0_max, machine_1, ...
            # Contar número de máquinas
            num_machines = sum(1 for col in columns if col.startswith('duration_') and col.endswith('_min'))
            
            sequences = []
            durations = []
            
            for _, row in df.iterrows():
                job_machines = []
                job_durations = []
                
                for i in range(num_machines):
                    machine_col = f"machine_{i}"
                    duration_min_col = f"duration_{i}_min"
                    duration_max_col = f"duration_{i}_max"
                    
                    machine = int(row[machine_col])
                    duration_min = float(row[duration_min_col])
                    duration_max = float(row[duration_max_col])
                    
                    job_machines.append(machine)
                    
                    if duration_min == duration_max:
                        job_durations.append(int(duration_min))
                    else:
                        job_durations.append(Interval(duration_min, duration_max))
                
                sequences.append(job_machines)
                durations.append(job_durations)
        else:
            # Formato tradicional con posible notación de intervalo en strings
            num_machines = sum(1 for col in columns if col.startswith('duration_'))
            
            sequences = []
            durations = []
            
            for _, row in df.iterrows():
                job_machines = []
                job_durations = []
                
                for i in range(num_machines):
                    machine_col = f"machine_{i}" if f"machine_{i}" in columns else i * 2
                    duration_col = f"duration_{i}" if f"duration_{i}" in columns else i * 2 + 1
                    
                    machine = int(row[machine_col])
                    duration_raw = row[duration_col]
                    
                    job_machines.append(machine)
                    
                    # Try to parse as interval or scalar
                    if isinstance(duration_raw, str):
                        job_durations.append(ProblemLoader._parse_duration_value(duration_raw))
                    else:
                        job_durations.append(int(duration_raw))
                
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
        
        # Validar intervalos
        ProblemLoader._validate_problem_intervals(problem)
        
        # Marcar si es un problema con intervalos
        problem['has_intervals'] = ProblemLoader._check_if_interval_problem(problem)
        
        return problem
    
    @staticmethod
    def load_taillard(file_path: str) -> Dict[str, Any]:
        """
        Carga un problema en formato Taillard (común en benchmarks).
        
        El formato Taillard tiene:
        - Número de trabajos y máquinas en la primera línea
        - Matriz de tiempos de procesamiento (cada fila es un trabajo)
        - Valores pueden ser escalares o intervalos en formato (min,max)
        
        Formato estándar:
        10 10 [optimal]
        machine1 time1 machine2 time2 ...
        
        Formato con intervalos:
        10 10 [optimal]
        machine1 (time_min,time_max) machine2 time2 ...
        
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
            
            # Split the line more carefully to handle intervals
            line = lines[line_index]
            line_index += 1
            
            # Parse tokens (can be numbers or intervals)
            tokens = []
            current_token = ""
            in_interval = False
            
            for char in line:
                if char == '(':
                    in_interval = True
                    current_token += char
                elif char == ')':
                    in_interval = False
                    current_token += char
                elif char.isspace() and not in_interval:
                    if current_token:
                        tokens.append(current_token)
                        current_token = ""
                else:
                    current_token += char
            
            # Don't forget last token
            if current_token:
                tokens.append(current_token)
            
            # Should have num_machines * 2 tokens (machine, duration pairs)
            if len(tokens) < num_machines * 2:
                raise ValueError(
                    f"No hay suficientes datos para el trabajo {j}: "
                    f"se esperaban {num_machines*2} valores, se encontraron {len(tokens)}"
                )
            
            # Process machine-duration pairs
            for m in range(num_machines):
                machine_str = tokens[m * 2]
                duration_str = tokens[m * 2 + 1]
                
                machine = int(machine_str)
                duration = ProblemLoader._parse_duration_value(duration_str)
                
                sequences[j].append(machine)
                durations[j].append(duration)
        
        # Crear diccionario de problema
        problem = {
            'num_jobs': num_jobs,
            'num_machines': num_machines,
            'sequences': sequences,
            'durations': durations
        }
        
        if optimal_makespan is not None:
            problem['optimal_makespan'] = optimal_makespan
        
        # Validar intervalos
        ProblemLoader._validate_problem_intervals(problem)
        
        # Marcar si es un problema con intervalos
        problem['has_intervals'] = ProblemLoader._check_if_interval_problem(problem)
        
        return problem
    
    @staticmethod
    def save_problem(problem: Dict[str, Any], file_path: str, format: str = 'json'):
        """
        Guarda un problema en un archivo.
        
        Soporta tanto problemas determinísticos como con intervalos.
        
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
        dir_path = os.path.dirname(os.path.abspath(file_path))
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        
        # Guardar en el formato especificado
        if format.lower() == 'json':
            # Prepare data for JSON serialization
            json_data = {
                'num_jobs': problem['num_jobs'],
                'num_machines': problem['num_machines'],
                'sequences': problem['sequences'],
                'durations': []
            }
            
            # Convert Intervals to serializable format
            for job_durations in problem['durations']:
                job_data = []
                for duration in job_durations:
                    if isinstance(duration, Interval):
                        if duration.is_degenerate:
                            job_data.append(int(duration.lower))
                        else:
                            job_data.append([duration.lower, duration.upper])
                    else:
                        job_data.append(duration)
                json_data['durations'].append(job_data)
            
            # Add optional fields
            if 'optimal_makespan' in problem:
                json_data['optimal_makespan'] = problem['optimal_makespan']
            if 'name' in problem:
                json_data['name'] = problem['name']
            if 'has_intervals' in problem:
                json_data['has_intervals'] = problem['has_intervals']
            
            with open(file_path, 'w') as f:
                json.dump(json_data, f, indent=2)
                
        elif format.lower() == 'csv':
            # Determinar si hay intervalos
            has_intervals = ProblemLoader._check_if_interval_problem(problem)
            
            rows = []
            for j in range(problem['num_jobs']):
                row = {}
                for m in range(problem['num_machines']):
                    row[f'machine_{m}'] = problem['sequences'][j][m]
                    
                    duration = problem['durations'][j][m]
                    if has_intervals and isinstance(duration, Interval):
                        row[f'duration_{m}_min'] = duration.lower
                        row[f'duration_{m}_max'] = duration.upper
                    else:
                        if isinstance(duration, Interval):
                            row[f'duration_{m}'] = int(duration.lower)
                        else:
                            row[f'duration_{m}'] = duration
                
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
                    line_parts = []
                    for m in range(problem['num_machines']):
                        machine = problem['sequences'][j][m]
                        duration = problem['durations'][j][m]
                        
                        line_parts.append(str(machine))
                        line_parts.append(ProblemLoader._format_duration_value(duration))
                    
                    f.write(' '.join(line_parts) + '\n')
        else:
            raise ValueError(f"Formato de salida '{format}' no soportado")
        
        logger.info(f"Problema guardado en {file_path}")
    
    @staticmethod
    def generate_random_problem(
        num_jobs: int, 
        num_machines: int, 
        min_duration: int = 1,
        max_duration: int = 100,
        uncertainty_ratio: float = 0.0,
        seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Genera un problema aleatorio de Job Shop.
        
        Args:
            num_jobs: Número de trabajos
            num_machines: Número de máquinas
            min_duration: Duración mínima de operaciones
            max_duration: Duración máxima de operaciones
            uncertainty_ratio: Ratio de incertidumbre (0.0 = determinístico, 0.1 = ±10%, etc.)
            seed: Semilla para reproducibilidad
            
        Returns:
            Diccionario con el problema generado
        """
        # Establecer semilla para reproducibilidad
        set_random_seed(seed)
        
        # Generar secuencias de máquinas (permutaciones aleatorias)
        sequences = []
        for _ in range(num_jobs):
            perm = np.random.permutation(num_machines).tolist()
            sequences.append(perm)
        
        # Generar duraciones
        durations = []
        for _ in range(num_jobs):
            job_durations = []
            for _ in range(num_machines):
                # Base duration
                base_duration = np.random.randint(min_duration, max_duration + 1)
                
                if uncertainty_ratio > 0:
                    # Add uncertainty
                    delta = int(base_duration * uncertainty_ratio)
                    if delta == 0:
                        delta = 1  # Minimum uncertainty
                    
                    lower = max(min_duration, base_duration - delta)
                    upper = min(max_duration, base_duration + delta)
                    
                    job_durations.append(Interval(lower, upper))
                else:
                    # Deterministic
                    job_durations.append(base_duration)
            
            durations.append(job_durations)
        
        problem = {
            'num_jobs': num_jobs,
            'num_machines': num_machines,
            'sequences': sequences,
            'durations': durations
        }
        
        # Marcar si tiene intervalos
        problem['has_intervals'] = uncertainty_ratio > 0
        
        return problem
