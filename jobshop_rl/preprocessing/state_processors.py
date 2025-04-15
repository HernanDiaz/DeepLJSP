"""
Módulo de preprocesamiento para modelos GNN y Transformer
en problemas de Job Shop Scheduling.

Proporciona funcionalidad para convertir estados del entorno JSP a
formatos de entrada adecuados para los diferentes modelos (grafos y secuencias).
"""

import torch
import numpy as np


class JSPGraphBuilder:
    """
    Clase para construir representaciones en forma de grafo para el problema JSP.
    
    Convierte estados del entorno de Job Shop Scheduling a formato de grafo
    compatible con Graph Neural Networks.
    """
    def __init__(self, num_jobs, num_machines, feature_extractor=None):
        """
        Inicializa el constructor de grafos.
        
        Args:
            num_jobs: Número de trabajos en el problema
            num_machines: Número de máquinas en el problema
            feature_extractor: Función opcional para extraer características
                               personalizadas de los nodos
        """
        self.num_jobs = num_jobs
        self.num_machines = num_machines
        self.feature_extractor = feature_extractor
        
        # Número total de operaciones/nodos
        self.total_operations = num_jobs * num_machines
        
        # Tipos de aristas
        self.EDGE_TYPE_PRECEDENCE = 0  # Precedencia dentro del mismo trabajo
        self.EDGE_TYPE_MACHINE = 1     # Competencia por la misma máquina
        self.EDGE_TYPE_CRITICAL = 2    # Arista en el camino crítico
    
    def _get_node_idx(self, job_idx, op_idx):
        """
        Obtiene el índice global del nodo dada su posición (trabajo, operación).
        
        Args:
            job_idx: Índice del trabajo
            op_idx: Índice de la operación dentro del trabajo
            
        Returns:
            Índice único del nodo en el grafo
        """
        return job_idx * self.num_machines + op_idx
    
    def build_graph(self, state, action_mask=None, env=None):
        """
        Construye un grafo a partir del estado actual del entorno.
        
        Args:
            state: Estado del entorno JSP (incluyendo información de operaciones)
            action_mask: Máscara de acciones válidas (opcional)
            env: Entorno JSP para acceder a secuencias y duraciones
            
        Returns:
            node_features: Características de los nodos [num_nodes, feature_dim]
            edge_index: Índices de aristas [2, num_edges]
            edge_features: Características de aristas [num_edges, edge_feature_dim]
            valid_mask: Máscara de operaciones elegibles
        """
        # Extraer componentes relevantes del estado
        # Usar atributos del entorno o campos del estado, según disponibilidad
        sequences = env.sequences if env is not None else state.get('sequences', [])
        durations = env.durations if env is not None else state.get('durations', [])
        progress = state.get('progress', {})
        machine_usage = state.get('machine_usage', [])
        current_time = state.get('current_time', 0)
        
        # Obtener información de operaciones completadas y elegibles
        job_progress = state.get('job_progress', [])
        eligible_ops = state.get('eligible_ops', [])
        
        # Inicializar listas para nodos y aristas
        node_features = []
        edge_indices = []
        edge_features = []
        
        # Crear nodos para cada operación
        for job_idx in range(self.num_jobs):
            for op_idx in range(self.num_machines):
                # Índice global del nodo
                node_idx = self._get_node_idx(job_idx, op_idx)
                
                # Caracterización básica del nodo/operación
                machine_id = sequences[job_idx][op_idx]
                duration = durations[job_idx][op_idx]
                job_prog = job_progress[job_idx] if job_progress else 0
                is_completed = job_prog > op_idx
                is_in_progress = job_prog == op_idx and progress.get((job_idx, op_idx), 0) > 0
                is_eligible = (job_idx, op_idx) in eligible_ops if eligible_ops else False
                
                # Normalizar características numéricas
                normalized_job_idx = job_idx / self.num_jobs
                normalized_op_idx = op_idx / self.num_machines
                normalized_machine_id = machine_id / self.num_machines
                normalized_duration = duration / max(d for job_d in durations for d in job_d) if durations else 0
                
                # Recopilar características del nodo
                node_feature = [
                    normalized_job_idx,       # Trabajo normalizado
                    normalized_op_idx,        # Posición de operación normalizada
                    normalized_machine_id,    # Máquina normalizada
                    normalized_duration,      # Duración normalizada
                    float(is_completed),      # Si la operación está completada
                    float(is_in_progress),    # Si la operación está en progreso
                    float(is_eligible),       # Si la operación es elegible ahora
                ]
                
                # Añadir características adicionales si hay un extractor personalizado
                if self.feature_extractor:
                    custom_features = self.feature_extractor(state, job_idx, op_idx)
                    node_feature.extend(custom_features)
                
                node_features.append(node_feature)
        
        # Crear aristas para relaciones de precedencia dentro de los trabajos
        for job_idx in range(self.num_jobs):
            for op_idx in range(1, self.num_machines):
                # Arista desde operación anterior a la actual
                src = self._get_node_idx(job_idx, op_idx - 1)
                dst = self._get_node_idx(job_idx, op_idx)
                
                edge_indices.append([src, dst])
                
                # Características de la arista: tipo, peso, etc.
                edge_feature = [
                    1.0,                      # Indicador de tipo = precedencia
                    0.0,                      # No es relación de máquina
                    0.0                       # No es parte del camino crítico (por ahora)
                ]
                edge_features.append(edge_feature)
        
        # Crear aristas para relaciones de máquina (competencia por recursos)
        for machine_id in range(self.num_machines):
            # Encontrar operaciones que usan esta máquina
            machine_ops = []
            for job_idx in range(self.num_jobs):
                for op_idx in range(self.num_machines):
                    if sequences[job_idx][op_idx] == machine_id:
                        machine_ops.append((job_idx, op_idx))
            
            # Crear aristas entre todas las operaciones de esta máquina
            for i, (job_i, op_i) in enumerate(machine_ops):
                for job_j, op_j in machine_ops[i+1:]:
                    src = self._get_node_idx(job_i, op_i)
                    dst = self._get_node_idx(job_j, op_j)
                    
                    # Arista bidireccional para relaciones de máquina
                    edge_indices.append([src, dst])
                    edge_indices.append([dst, src])
                    
                    # Características de la arista: tipo = máquina
                    edge_feature = [
                        0.0,                  # No es relación de precedencia
                        1.0,                  # Indicador de tipo = máquina
                        0.0                   # No es parte del camino crítico (por ahora)
                    ]
                    edge_features.append(edge_feature.copy())
                    edge_features.append(edge_feature.copy())
        
        # Si hay información de camino crítico disponible, añadir ese tipo de aristas
        critical_path = state.get('critical_path', [])
        if critical_path:
            for i in range(len(critical_path) - 1):
                job_i, op_i = critical_path[i]
                job_j, op_j = critical_path[i + 1]
                
                src = self._get_node_idx(job_i, op_i)
                dst = self._get_node_idx(job_j, op_j)
                
                # Añadir arista del camino crítico
                edge_indices.append([src, dst])
                
                # Características de la arista: tipo = crítica
                edge_feature = [
                    0.0,                      # No es relación de precedencia
                    0.0,                      # No es relación de máquina
                    1.0                       # Es parte del camino crítico
                ]
                edge_features.append(edge_feature)
                
                # Actualizar características de aristas existentes si ya están en el camino crítico
                # Esto implica buscar si ya existe la arista y actualizar su valor
                for e_idx, (s, d) in enumerate(edge_indices[:-1]):  # Excluir la que acabamos de añadir
                    if s == src and d == dst:
                        edge_features[e_idx][2] = 1.0  # Marcar como parte del camino crítico
        
        # Convertir listas a tensores de PyTorch
        node_features_tensor = torch.FloatTensor(node_features)
        edge_index_tensor = torch.LongTensor(edge_indices).t()  # Formato [2, num_edges]
        edge_features_tensor = torch.FloatTensor(edge_features)
        
        # Crear máscara de nodos elegibles si no se proporcionó
        if action_mask is None:
            action_mask = torch.zeros(self.total_operations, dtype=torch.bool)
            for job_idx, op_idx in eligible_ops:
                node_idx = self._get_node_idx(job_idx, op_idx)
                action_mask[node_idx] = True
        
        return node_features_tensor, edge_index_tensor, edge_features_tensor, action_mask


class SequenceBuilder:
    """
    Clase para construir representaciones secuenciales para el problema JSP.
    
    Convierte estados del entorno a una secuencia de operaciones para
    modelos basados en atención como Transformer.
    """
    def __init__(self, num_jobs, num_machines, feature_extractor=None):
        """
        Inicializa el constructor de secuencias.
        
        Args:
            num_jobs: Número de trabajos en el problema
            num_machines: Número de máquinas en el problema
            feature_extractor: Función opcional para extraer características
                               personalizadas de las operaciones
        """
        self.num_jobs = num_jobs
        self.num_machines = num_machines
        self.feature_extractor = feature_extractor
        
        # Número total de operaciones
        self.total_operations = num_jobs * num_machines
    
    def build_sequence(self, state, action_mask=None, env=None):
        """
        Construye una representación secuencial a partir del estado actual.
        
        Args:
            state: Estado del entorno JSP
            action_mask: Máscara de acciones válidas (opcional)
            env: Entorno JSP para acceder a secuencias y duraciones
            
        Returns:
            sequence_features: Características de la secuencia [seq_len, feature_dim]
            valid_mask: Máscara de operaciones elegibles
        """
        # Extraer componentes relevantes del estado
        sequences = env.sequences if env is not None else state.get('sequences', [])
        durations = env.durations if env is not None else state.get('durations', [])
        progress = state.get('progress', {})
        current_time = state.get('current_time', 0)
        job_progress = state.get('job_progress', [])
        eligible_ops = state.get('eligible_ops', [])
        
        # Inicializar lista de características de la secuencia
        sequence_features = []
        
        # Construir representación de cada operación
        for job_idx in range(self.num_jobs):
            for op_idx in range(self.num_machines):
                # Características básicas
                machine_id = sequences[job_idx][op_idx]
                duration = durations[job_idx][op_idx]
                
                # Estado de la operación
                job_prog = job_progress[job_idx] if job_progress else 0
                is_completed = job_prog > op_idx
                is_in_progress = job_prog == op_idx and progress.get((job_idx, op_idx), 0) > 0
                is_eligible = (job_idx, op_idx) in eligible_ops if eligible_ops else False
                
                # Normalizar características numéricas
                normalized_job_idx = job_idx / self.num_jobs
                normalized_op_idx = op_idx / self.num_machines
                normalized_machine_id = machine_id / self.num_machines
                max_duration = max(d for job_d in durations for d in job_d) if durations else 1
                normalized_duration = duration / max_duration
                
                # Características adicionales para enriquecer la representación
                remaining_ops_in_job = self.num_machines - op_idx - 1
                normalized_remaining = remaining_ops_in_job / self.num_machines
                
                # Dependencias completadas (operaciones anteriores en el trabajo)
                deps_completed = 1.0 if op_idx == 0 else float(job_prog >= op_idx - 1)
                
                # Construir vector de características
                feature_vector = [
                    normalized_job_idx,       # Trabajo normalizado
                    normalized_op_idx,        # Posición de operación normalizada
                    normalized_machine_id,    # Máquina normalizada
                    normalized_duration,      # Duración normalizada
                    float(is_completed),      # Si la operación está completada
                    float(is_in_progress),    # Si la operación está en progreso
                    float(is_eligible),       # Si la operación es elegible ahora
                    normalized_remaining,     # Operaciones restantes en el trabajo
                    deps_completed            # Si las dependencias están completadas
                ]
                
                # Añadir características personalizadas si hay un extractor
                if self.feature_extractor:
                    custom_features = self.feature_extractor(state, job_idx, op_idx)
                    feature_vector.extend(custom_features)
                
                sequence_features.append(feature_vector)
        
        # Convertir a tensor de PyTorch
        sequence_tensor = torch.FloatTensor(sequence_features)
        
        # Crear máscara de operaciones elegibles si no se proporcionó
        if action_mask is None:
            action_mask = torch.zeros(self.total_operations, dtype=torch.bool)
            for job_idx, op_idx in eligible_ops:
                node_idx = job_idx * self.num_machines + op_idx
                action_mask[node_idx] = True
        
        return sequence_tensor, action_mask


class JSPFeatureExtractor:
    """
    Extractor de características avanzadas para problemas de Job Shop Scheduling.
    
    Implementa cálculos de características especializadas que capturan aspectos
    importantes del problema JSP, como métricas de urgencia, utilización, etc.
    """
    def __init__(self, num_jobs, num_machines):
        """
        Inicializa el extractor de características.
        
        Args:
            num_jobs: Número de trabajos en el problema
            num_machines: Número de máquinas en el problema
        """
        self.num_jobs = num_jobs
        self.num_machines = num_machines
    
    def extract_features(self, state, job_idx, op_idx, env=None):
        """
        Extrae características avanzadas para una operación específica.
        
        Args:
            state: Estado actual del entorno
            job_idx: Índice del trabajo
            op_idx: Índice de la operación dentro del trabajo
            env: Entorno JSP para acceder a secuencias y duraciones
            
        Returns:
            Lista de características adicionales
        """
        # Extraer datos relevantes del estado
        durations = env.durations if env is not None else state.get('durations', [])
        sequences = env.sequences if env is not None else state.get('sequences', [])
        job_progress = state.get('job_progress', [])
        current_time = state.get('current_time', 0)
        makespan_est = state.get('makespan_estimate', 0)
        
        # Características a calcular
        features = []
        
        # 1. Tiempo de procesamiento restante para este trabajo
        remaining_time = 0
        if job_progress and op_idx >= job_progress[job_idx]:
            remaining_ops = range(max(op_idx, job_progress[job_idx]), self.num_machines)
            remaining_time = sum(durations[job_idx][i] for i in remaining_ops)
        
        # Normalizar
        max_total_duration = max(sum(durations[j]) for j in range(self.num_jobs)) if durations else 1
        normalized_remaining = remaining_time / max_total_duration
        features.append(normalized_remaining)
        
        # 2. Ratio de tiempo restante respecto a otros trabajos (urgencia relativa)
        other_jobs_remaining = []
        for j in range(self.num_jobs):
            if j != job_idx and job_progress:
                j_remaining = sum(durations[j][i] for i in range(job_progress[j], self.num_machines))
                other_jobs_remaining.append(j_remaining)
        
        avg_others_remaining = sum(other_jobs_remaining) / len(other_jobs_remaining) if other_jobs_remaining else 0
        urgency_ratio = 0.5  # Valor neutro por defecto
        if avg_others_remaining > 0:
            urgency_ratio = remaining_time / avg_others_remaining
            # Normalizar a [0,1] mediante función sigmoide
            urgency_ratio = 1 / (1 + np.exp(-(urgency_ratio - 1) * 3))
        features.append(urgency_ratio)
        
        # 3. Carga de trabajo en la máquina asignada
        if op_idx < self.num_machines:
            machine_id = sequences[job_idx][op_idx]
            machine_workload = 0
            machine_queued_ops = 0
            
            for j in range(self.num_jobs):
                for o in range(self.num_machines):
                    if sequences[j][o] == machine_id:
                        # Si la operación aún no se ha completado
                        if job_progress and o >= job_progress[j]:
                            machine_workload += durations[j][o]
                            machine_queued_ops += 1
            
            # Normalizar carga y número de operaciones
            max_possible_workload = sum(max(row) for row in durations) if durations else 1
            normalized_workload = machine_workload / max_possible_workload
            normalized_queued = machine_queued_ops / self.num_jobs
            
            features.append(normalized_workload)
            features.append(normalized_queued)
        else:
            # Valores por defecto si la operación no es válida
            features.extend([0.0, 0.0])
        
        # 4. Estimación de impacto en makespan
        # Cuánto contribuiría esta operación al makespan total
        op_duration = durations[job_idx][op_idx] if op_idx < self.num_machines else 0
        normalized_impact = op_duration / makespan_est if makespan_est > 0 else 0
        features.append(normalized_impact)
        
        # 5. Posición relativa en el camino crítico (si está disponible)
        critical_path_position = 0.0
        critical_path = state.get('critical_path', [])
        
        if critical_path:
            if (job_idx, op_idx) in critical_path:
                # Índice normalizado en el camino crítico
                position = critical_path.index((job_idx, op_idx))
                critical_path_position = position / len(critical_path)
                features.append(1.0)  # Está en el camino crítico
                features.append(critical_path_position)
            else:
                features.append(0.0)  # No está en el camino crítico
                features.append(0.0)  # Posición = 0
        else:
            features.extend([0.0, 0.0])  # Sin información de camino crítico
        
        return features