"""
Módulo para entrenamiento de agentes con múltiples instancias.

Implementa un framework para entrenar agentes de aprendizaje por refuerzo
en múltiples instancias de problemas, lo que mejora la generalización y
el rendimiento en problemas de gran tamaño.
"""

import os
import time
import logging
import random
import numpy as np
import torch
from typing import List, Dict, Any, Tuple, Optional, Union

from jobshop_rl.agents.ppo_agent_gnn import AdvancedPPOAgent
from jobshop_rl.environment.job_shop_env import JobShopEnv
from jobshop_rl.experiments.factory import ProblemFactory
from jobshop_rl.utils.logging import TrainingLogger

# Configurar logger
logger = logging.getLogger("JobShopRL.MultiInstanceTrainer")


class MultiInstanceTrainer:
    """
    Entrenador para modelos con múltiples instancias de problemas.
    
    Permite entrenar un modelo en un conjunto de problemas de JSP
    para mejorar la generalización y rendimiento.
    """
    
    def __init__(
        self,
        problem_ids: List[str],
        agent_type: str = 'advanced',
        model_type: str = 'gnn',
        reward_strategy: str = 'adaptive',
        agent_params: Dict = None,
        reward_params: Dict = None,
        use_curriculum: bool = True,
        curriculum_strategy: str = 'size',
        batch_size: int = 5,
        epochs_per_instance: int = 20,
        total_episodes: int = 1000,
        seed: Optional[int] = None,
        output_dir: str = 'outputs',
        save_interval: int = 100,
        csv_logging: bool = True,
        device: Optional[torch.device] = None
    ):
        """
        Inicializa el entrenador multi-instancia.
        
        Args:
            problem_ids: Lista de IDs de problemas para entrenamiento
            agent_type: Tipo de agente ('advanced', 'ppo')
            model_type: Tipo de modelo para agentes avanzados
            reward_strategy: Estrategia de recompensa a utilizar
            agent_params: Parámetros del agente
            reward_params: Parámetros de la estrategia de recompensa
            use_curriculum: Si se debe usar curriculum learning
            curriculum_strategy: Estrategia de curriculum ('size', 'difficulty', 'random')
            batch_size: Número de instancias a usar en cada lote
            epochs_per_instance: Episodios de entrenamiento por instancia en cada época
            total_episodes: Total de episodios de entrenamiento
            seed: Semilla para reproducibilidad
            output_dir: Directorio para resultados
            save_interval: Intervalo para guardar modelo (en episodios)
            csv_logging: Si se deben registrar métricas en CSV
            device: Dispositivo para tensores (CPU/GPU)
        """
        self.problem_ids = problem_ids
        self.agent_type = agent_type
        self.model_type = model_type
        self.reward_strategy = reward_strategy
        self.agent_params = agent_params or {}
        self.reward_params = reward_params or {}
        self.use_curriculum = use_curriculum
        self.curriculum_strategy = curriculum_strategy
        self.batch_size = min(batch_size, len(problem_ids))
        self.epochs_per_instance = epochs_per_instance
        self.total_episodes = total_episodes
        self.seed = seed
        self.output_dir = output_dir
        self.save_interval = save_interval
        self.csv_logging = csv_logging
        self.device = device if device else torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Aplicar semilla si se proporciona
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
            torch.manual_seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed(seed)
                torch.cuda.manual_seed_all(seed)
        
        # Crear directorios de salida
        os.makedirs(output_dir, exist_ok=True)
        self.models_dir = os.path.join(output_dir, "models")
        os.makedirs(self.models_dir, exist_ok=True)
        
        # Inicializar logger CSV
        self.csv_logger = None
        if csv_logging:
            self.csv_logger = TrainingLogger(
                filename=f"multi_instance_{model_type}_{int(time.time())}",
                base_dir=os.path.join(output_dir, "logs")
            )
        
        # Organizar problemas según curriculum si está habilitado
        self._organize_problems()
        
        # Inicializar entornos y agente (se crearán en train)
        self.envs = {}
        self.agent = None
        self.current_episode = 0
        self.best_makespan_per_problem = {pid: float('inf') for pid in problem_ids}
        self.training_history = []
        
        logger.info(f"Trainer multi-instancia inicializado con {len(problem_ids)} problemas")
    
    def _organize_problems(self):
        """
        Organiza los problemas según la estrategia de curriculum seleccionada.
        """
        if not self.use_curriculum:
            return
        
        problem_sizes = {}
        problem_difficulties = {}
        
        # Obtener información de cada problema
        for pid in self.problem_ids:
            try:
                # Cargar datos del problema
                problem_data = ProblemFactory.load_problem_by_id(pid)
                num_jobs = problem_data.get('num_jobs', 0)
                num_machines = problem_data.get('num_machines', 0)
                
                # Calcular tamaño y dificultad aproximada
                size = num_jobs * num_machines
                difficulty = size  # Podríamos usar métricas más sofisticadas
                
                problem_sizes[pid] = size
                problem_difficulties[pid] = difficulty
                
            except Exception as e:
                logger.warning(f"Error al analizar problema {pid}: {str(e)}")
                # Asignar valor arbitrario alto para evitar este problema al principio
                problem_sizes[pid] = 9999
                problem_difficulties[pid] = 9999
        
        # Ordenar problemas según la estrategia seleccionada
        if self.curriculum_strategy == 'size':
            self.problem_ids = sorted(self.problem_ids, key=lambda pid: problem_sizes.get(pid, 9999))
            logger.info("Problemas ordenados por tamaño (de menor a mayor)")
        
        elif self.curriculum_strategy == 'difficulty':
            self.problem_ids = sorted(self.problem_ids, key=lambda pid: problem_difficulties.get(pid, 9999))
            logger.info("Problemas ordenados por dificultad estimada (de menor a mayor)")
        
        elif self.curriculum_strategy == 'random':
            random.shuffle(self.problem_ids)
            logger.info("Problemas ordenados aleatoriamente")
    
    def _create_environment(self, problem_id):
        """
        Crea un entorno para un problema específico.
        
        Args:
            problem_id: ID del problema
            
        Returns:
            Entorno de JobShop configurado
        """
        # Importar aquí para evitar dependencia circular
        from jobshop_rl.experiments.factory import EnvironmentFactory
        
        # Crear entorno con el problema especificado
        env = EnvironmentFactory.create_from_problem_id(
            problem_id=problem_id,
            reward_strategy=self.reward_strategy,
            seed=self.seed,
            **self.reward_params
        )
        
        return env
    
    def _create_agent(self, env):
        """
        Crea un agente para entrenamiento.
        
        Args:
            env: Entorno de referencia para inicializar el agente
            
        Returns:
            Agente de aprendizaje por refuerzo
        """
        # Importar aquí para evitar dependencia circular
        from jobshop_rl.experiments.factory_integration import ExtendedAgentFactory
        
        # Crear agente del tipo especificado
        agent = ExtendedAgentFactory.create_agent(
            env=env,
            agent_type=self.agent_type,
            model_type=self.model_type,
            csv_logger=self.csv_logger,
            **self.agent_params
        )
        
        return agent
    
    def _select_training_batch(self):
        """
        Selecciona un lote de problemas para entrenamiento según el curriculum.
        
        Returns:
            Lista de IDs de problemas para el lote actual
        """
        if not self.use_curriculum:
            # Seleccionar problemas aleatorios si no se usa curriculum
            return random.sample(self.problem_ids, self.batch_size)
        
        # Calcular progreso de entrenamiento (de 0 a 1)
        progress = min(1.0, self.current_episode / self.total_episodes)
        
        if self.curriculum_strategy in ['size', 'difficulty']:
            # Índice máximo basado en el progreso
            max_idx = int(len(self.problem_ids) * (0.2 + 0.8 * progress))
            max_idx = max(self.batch_size, min(max_idx, len(self.problem_ids)))
            
            # Seleccionar batch_size problemas aleatorios hasta el índice máximo
            candidate_problems = self.problem_ids[:max_idx]
            return random.sample(candidate_problems, min(self.batch_size, len(candidate_problems)))
        
        else:  # random
            return random.sample(self.problem_ids, self.batch_size)
    
    def train(self):
        """
        Entrena el agente usando múltiples instancias de problemas.
        
        Returns:
            Agente entrenado y resultados de entrenamiento
        """
        start_time = time.time()
        logger.info(f"Iniciando entrenamiento multi-instancia con {len(self.problem_ids)} problemas")
        
        # Inicializar con el primer problema
        initial_problem = self.problem_ids[0]
        env = self._create_environment(initial_problem)
        self.envs[initial_problem] = env
        
        # Crear agente
        self.agent = self._create_agent(env)
        
        # Variables para seguimiento
        best_global_performance = float('inf')
        improvement_count = 0
        
        # Realizar entrenamiento
        while self.current_episode < self.total_episodes:
            # Seleccionar lote de problemas para esta época
            batch_problems = self._select_training_batch()
            
            epoch_start_time = time.time()
            batch_metrics = {}
            
            # Entrenar en cada problema del lote
            for problem_id in batch_problems:
                # Crear entorno si no existe
                if problem_id not in self.envs:
                    self.envs[problem_id] = self._create_environment(problem_id)
                
                # Acceder al entorno
                current_env = self.envs[problem_id]
                
                # Establecer entorno actual para el agente
                self.agent.env = current_env
                
                # Entrenar agente en este problema
                logger.info(f"Episodio {self.current_episode}/{self.total_episodes} - "
                           f"Entrenando en problema {problem_id} por {self.epochs_per_instance} episodios")
                
                makespan_history = self.agent.train(
                    episodes=self.epochs_per_instance,
                    dynamic_entropy=True,
                    early_stopping=True,
                    patience=5,  # Menor paciencia por problema individual
                    verbose=False
                )
                
                # Registrar métricas
                best_makespan = self.agent.best_makespan
                batch_metrics[problem_id] = best_makespan
                
                # Actualizar mejor makespan para este problema
                if best_makespan < self.best_makespan_per_problem[problem_id]:
                    self.best_makespan_per_problem[problem_id] = best_makespan
                
                # Actualizar episodios
                self.current_episode += self.epochs_per_instance
                
                # Guardar modelo periódicamente
                if self.current_episode % self.save_interval < self.epochs_per_instance:
                    self._save_model()
            
            # Calcular rendimiento promedio en el lote
            avg_performance = sum(batch_metrics.values()) / len(batch_metrics)
            
            # Calcular tiempo de época
            epoch_time = time.time() - epoch_start_time
            
            # Registrar progreso
            logger.info(f"Época completada - Promedio: {avg_performance:.2f} - "
                       f"Tiempo: {epoch_time:.2f}s - "
                       f"Problemas: {', '.join(batch_problems)}")
            
            # Registrar métricas
            self.training_history.append({
                'episode': self.current_episode,
                'batch_problems': batch_problems,
                'batch_metrics': batch_metrics,
                'avg_performance': avg_performance,
                'epoch_time': epoch_time
            })
            
            # Registrar en CSV si está habilitado
            if self.csv_logger:
                self.csv_logger.log_metrics({
                    'episode': self.current_episode,
                    'avg_performance': avg_performance,
                    'num_problems': len(batch_problems),
                    'epoch_time': epoch_time
                })
            
            # Verificar mejora global
            if avg_performance < best_global_performance:
                improvement = (best_global_performance - avg_performance) / best_global_performance
                best_global_performance = avg_performance
                
                if improvement > 0.01:  # Mejora significativa
                    improvement_count += 1
                    logger.info(f"Mejora global #{improvement_count}: {best_global_performance:.2f} "
                               f"(+{improvement:.2%})")
                    
                    # Guardar mejor modelo
                    self._save_model(is_best=True)
        
        # Calcular tiempo total
        total_time = time.time() - start_time
        logger.info(f"Entrenamiento completado en {total_time:.2f} segundos")
        
        # Guardar modelo final
        self._save_model(is_final=True)
        
        return self.agent, {
            'training_history': self.training_history,
            'best_makespan_per_problem': self.best_makespan_per_problem,
            'best_global_performance': best_global_performance,
            'total_time': total_time
        }
    
    def _save_model(self, is_best=False, is_final=False):
        """
        Guarda el modelo actual en disco.
        
        Args:
            is_best: Si es el mejor modelo hasta ahora
            is_final: Si es el modelo final
        """
        if is_best:
            filename = f"best_model_{self.model_type}.pt"
        elif is_final:
            filename = f"final_model_{self.model_type}.pt"
        else:
            filename = f"model_{self.model_type}_ep{self.current_episode}.pt"
        
        filepath = os.path.join(self.models_dir, filename)
        
        try:
            self.agent.save_model(filepath)
            logger.info(f"Modelo guardado en {filepath}")
        except Exception as e:
            logger.error(f"Error al guardar modelo: {str(e)}")
    
    def evaluate(self, problem_ids=None, episodes_per_problem=5):
        """
        Evalúa el agente entrenado en un conjunto de problemas.
        
        Args:
            problem_ids: Lista de problemas para evaluación (usa todos si es None)
            episodes_per_problem: Número de episodios para evaluar cada problema
            
        Returns:
            Resultados de evaluación por problema
        """
        if not self.agent:
            raise ValueError("No hay agente entrenado para evaluar")
        
        # Usar todos los problemas si no se especifican
        eval_problems = problem_ids or self.problem_ids
        
        results = {}
        
        for problem_id in eval_problems:
            logger.info(f"Evaluando en problema {problem_id}...")
            
            # Crear entorno si no existe
            if problem_id not in self.envs:
                self.envs[problem_id] = self._create_environment(problem_id)
            
            # Acceder al entorno
            eval_env = self.envs[problem_id]
            
            # Establecer entorno actual para el agente
            self.agent.env = eval_env
            
            # Evaluar en este problema
            makespan, schedule, makespan_history, time_taken = self.agent.evaluate_policy(
                num_episodes=episodes_per_problem,
                render=False
            )
            
            # Guardar resultados
            results[problem_id] = {
                'makespan': makespan,
                'makespan_history': makespan_history,
                'time_taken': time_taken
            }
            
            logger.info(f"Problema {problem_id} - Makespan: {makespan} - "
                       f"Tiempo: {time_taken:.2f}s")
        
        # Calcular estadísticas globales
        avg_makespan = sum(r['makespan'] for r in results.values()) / len(results)
        avg_time = sum(r['time_taken'] for r in results.values()) / len(results)
        
        logger.info(f"Evaluación completada - Promedio: {avg_makespan:.2f} - "
                   f"Tiempo promedio: {avg_time:.2f}s")
        
        return results
    
    @classmethod
    def load_and_evaluate(cls, model_path, problem_ids, 
                          agent_type='advanced', model_type='gnn',
                          reward_strategy='adaptive', device=None):
        """
        Carga un modelo previamente entrenado y lo evalúa en los problemas especificados.
        
        Args:
            model_path: Ruta al modelo guardado
            problem_ids: Lista de problemas para evaluación
            agent_type: Tipo de agente ('advanced', 'ppo')
            model_type: Tipo de modelo para agentes avanzados
            reward_strategy: Estrategia de recompensa
            device: Dispositivo para tensores
            
        Returns:
            Resultados de evaluación por problema
        """
        # Crear instancia del entrenador
        trainer = cls(
            problem_ids=problem_ids,
            agent_type=agent_type,
            model_type=model_type,
            reward_strategy=reward_strategy,
            device=device,
            csv_logging=False
        )
        
        # Crear entorno para el primer problema
        initial_problem = problem_ids[0]
        env = trainer._create_environment(initial_problem)
        trainer.envs[initial_problem] = env
        
        # Cargar modelo
        from jobshop_rl.agents.ppo_agent_gnn import AdvancedPPOAgent
        trainer.agent = AdvancedPPOAgent.load_model(model_path, env, device=device)
        
        # Evaluar
        return trainer.evaluate(problem_ids)
