"""
Fábrica para la creación de experimentos de Job Shop Scheduling.
"""

import random
import numpy as np
import torch
import matplotlib.pyplot as plt
import logging
import time
import os
import datetime
from typing import Dict, List, Tuple, Any, Optional

from jobshop_rl.utils.visualization import save_plots as visualization_save_plots
from jobshop_rl.environment.job_shop_env import JobShopEnv
from jobshop_rl.agents.ppo_agent import PPOAgent
from jobshop_rl.rewards.strategies import RewardStrategyFactory
from jobshop_rl.experiments.evaluator import HeuristicEvaluator
from jobshop_rl.utils.logging import TrainingLogger
from jobshop_rl.utils.problem_analyzer import ProblemAnalyzer, AdaptiveConfigGenerator
from jobshop_rl.data.problem_loader import ProblemLoader
from jobshop_rl.data.ft20 import get_ft20_problem
from jobshop_rl.data.abz10 import get_abz10_problem

logger = logging.getLogger("JobShopRL.ExperimentFactory")

class ExperimentFactory:
    """Fábrica para crear y ejecutar experimentos (patrón Factory)"""

    @staticmethod
    def load_problem_by_id(problem_id: str) -> Dict[str, Any]:
        """
        Carga los datos de un problema por su ID.
        
        Args:
            problem_id: Identificador del problema (ft10, ft20, abz10, etc.)
            
        Returns:
            Diccionario con los datos del problema
            
        Raises:
            ValueError: Si el problema no es reconocido
        """
        problem_id = problem_id.lower()
        
        if problem_id == "ft10":
            # Configuración del problema FT10
            return {
                'num_jobs': 10,
                'num_machines': 10,
                'problem_id': 'ft10',
                'sequences': [
                    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    [0, 2, 4, 9, 3, 1, 6, 5, 7, 8],
                    [1, 0, 3, 2, 8, 5, 7, 6, 9, 4],
                    [1, 2, 0, 4, 6, 8, 7, 3, 9, 5],
                    [2, 0, 1, 5, 3, 4, 8, 7, 9, 6],
                    [2, 1, 5, 3, 8, 9, 0, 6, 4, 7],
                    [1, 0, 3, 2, 6, 5, 9, 8, 7, 4],
                    [2, 0, 1, 5, 4, 6, 8, 9, 7, 3],
                    [0, 1, 3, 5, 2, 9, 6, 7, 4, 8],
                    [1, 0, 2, 6, 8, 9, 5, 3, 4, 7]
                ],
                'durations': [
                    [29, 78, 9, 36, 49, 11, 62, 56, 44, 21],
                    [43, 90, 75, 11, 69, 28, 46, 46, 72, 30],
                    [91, 85, 39, 74, 90, 10, 12, 89, 45, 33],
                    [81, 95, 71, 99, 9, 52, 85, 98, 22, 43],
                    [14, 6, 22, 61, 26, 69, 21, 49, 72, 53],
                    [84, 2, 52, 95, 48, 72, 47, 65, 6, 25],
                    [46, 37, 61, 13, 32, 21, 32, 89, 30, 55],
                    [31, 86, 46, 74, 32, 88, 19, 48, 36, 79],
                    [76, 69, 76, 51, 85, 11, 40, 89, 26, 74],
                    [85, 13, 61, 7, 64, 76, 47, 52, 90, 45]
                ]
            }
        elif problem_id == "ft20":
            return get_ft20_problem()
        elif problem_id == "abz10":
            return get_abz10_problem()
        else:
            # Intentar cargar desde archivo usando el ProblemLoader
            try:
                return ProblemLoader.load_problem(problem_id)
            except Exception as e:
                logger.error(f"Error cargando problema {problem_id}: {str(e)}")
                raise ValueError(f"Problema no reconocido o no pudo cargarse: {problem_id}")

    @staticmethod
    def create_env_from_problem_id(problem_id: str, reward_strategy: str = "adaptive", seed: Optional[int] = None, **reward_params) -> JobShopEnv:
        """
        Crea un entorno para un problema específico a partir de su ID.
        
        Args:
            problem_id: Identificador del problema
            reward_strategy: Estrategia de recompensa a utilizar
            seed: Semilla para reproducibilidad
            **reward_params: Parámetros adicionales para la estrategia de recompensa
            
        Returns:
            Entorno de JobShop configurado para el problema especificado
        """
        problem_data = ExperimentFactory.load_problem_by_id(problem_id)
        
        # Analizar el problema para obtener sus características
        num_jobs = problem_data['num_jobs']
        num_machines = problem_data['num_machines']
        sequences = problem_data['sequences']
        durations = problem_data['durations']
        
        # Análisis automático del problema
        problem_analysis = ProblemAnalyzer.analyze_problem(sequences, durations)
        
        # Adaptar parámetros de recompensa según el análisis del problema si se usa la estrategia adaptativa
        if reward_strategy.lower() == "adaptive" and not reward_params:
            reward_params = AdaptiveConfigGenerator.generate_reward_config(problem_analysis)
            logger.info("Usando configuración de recompensa adaptativa generada automáticamente")
        
        # Crear estrategia de recompensa con el análisis del problema
        reward_strategy_obj = RewardStrategyFactory.create_strategy(
            reward_strategy, 
            problem_analysis=problem_analysis, 
            **reward_params
        )
        
        # Crear y devolver el entorno con el problema ID
        return JobShopEnv(
            num_jobs=num_jobs, 
            num_machines=num_machines, 
            sequences=sequences, 
            durations=durations, 
            reward_strategy=reward_strategy_obj, 
            problem_id=problem_id,
            seed=seed
        )

    @staticmethod
    def create_env_from_problem(problem_data: Dict[str, Any], reward_strategy: str = "adaptive", **kwargs) -> JobShopEnv:
        """
        Crea un entorno a partir de los datos de un problema.
        
        Args:
            problem_data: Datos del problema (secuencias, duraciones, etc.)
            reward_strategy: Estrategia de recompensa a utilizar
            **kwargs: Parámetros adicionales
            
        Returns:
            Entorno de JobShop configurado para el problema especificado
        """
        num_jobs = problem_data.get('num_jobs')
        num_machines = problem_data.get('num_machines')
        sequences = problem_data.get('sequences')
        durations = problem_data.get('durations')
        problem_id = problem_data.get('problem_id', 'custom')
        seed = kwargs.get('seed')
        
        # Validar datos
        if not all([num_jobs, num_machines, sequences, durations]):
            raise ValueError("Datos de problema incompletos o en formato incorrecto")
        
        # Extraer parámetros para la estrategia de recompensa
        reward_params = {k: v for k, v in kwargs.items() if k not in ['seed']}
        
        # Análisis automático del problema
        problem_analysis = ProblemAnalyzer.analyze_problem(sequences, durations)
        
        # Adaptar parámetros de recompensa según el análisis del problema si se usa la estrategia adaptativa
        if reward_strategy.lower() == "adaptive" and not reward_params:
            reward_params = AdaptiveConfigGenerator.generate_reward_config(problem_analysis)
            logger.info("Usando configuración de recompensa adaptativa generada automáticamente")
        
        # Crear estrategia de recompensa con el análisis del problema
        reward_strategy_obj = RewardStrategyFactory.create_strategy(
            reward_strategy, 
            problem_analysis=problem_analysis, 
            **reward_params
        )
        
        # Crear y devolver el entorno
        return JobShopEnv(
            num_jobs=num_jobs, 
            num_machines=num_machines, 
            sequences=sequences, 
            durations=durations, 
            reward_strategy=reward_strategy_obj, 
            problem_id=problem_id,
            seed=seed
        )

    @staticmethod
    def create_agent(env: JobShopEnv, csv_logger: Optional[TrainingLogger] = None, **agent_params) -> PPOAgent:
        """
        Crea un agente PPO con los parámetros especificados.
        
        Args:
            env: Entorno de JobShop
            csv_logger: Logger para datos de entrenamiento (opcional)
            **agent_params: Parámetros específicos del agente
            
        Returns:
            Agente PPO configurado
        """
        # Si el entorno tiene análisis del problema, adaptar los parámetros del agente
        if hasattr(env, 'problem_analysis') and not agent_params:
            adapted_params = AdaptiveConfigGenerator.generate_agent_config(env.problem_analysis)
            logger.info("Adaptando parámetros del agente según características del problema")
            # Combinar con parámetros proporcionados
            adapted_params.update(agent_params)
            agent_params = adapted_params
            
        return PPOAgent(env, csv_logger=csv_logger, **agent_params)

    @staticmethod
    def run_full_experiment(episodes: int = 100, reward_strategy: str = "adaptive",
                           agent_params: Dict = None, reward_params: Dict = None,
                           problem_id: str = "ft10", seed: Optional[int] = None, 
                           visualize: bool = True, save_plots: bool = True, 
                           csv_logging: bool = True, csv_filename: Optional[str] = None, 
                           csv_base_dir: str = 'outputs', output_dir: str = 'outputs', 
                           experiment_name: Optional[str] = None,
                           evaluate_abz10: bool = True) -> Tuple[PPOAgent, Dict]:
        """
        Ejecuta un experimento completo con evaluación de heurísticas y entrenamiento.
        
        El experimento incluye:
        1. Entrenamiento del agente en el problema especificado (por defecto FT10)
        2. Evaluación y comparación con heurísticas
        3. Opcionalmente, evaluación del mejor modelo encontrado con el problema ABZ10
        
        Args:
            episodes: Número de episodios a entrenar
            reward_strategy: Tipo de estrategia de recompensa
            agent_params: Parámetros del agente
            reward_params: Parámetros de la estrategia de recompensa
            problem_id: Identificador del problema (ft10, ft20, abz10, etc.)
            seed: Semilla para reproducibilidad
            visualize: Si se deben generar visualizaciones
            save_plots: Si se deben guardar las visualizaciones en archivos
            csv_logging: Si se deben registrar métricas en CSV
            csv_filename: Nombre del archivo CSV
            csv_base_dir: Directorio base para archivos CSV
            evaluate_abz10: Si se debe evaluar el mejor modelo con ABZ10 al finalizar
            
        Returns:
            Tupla (agente entrenado, resultados del experimento)
        """
        if agent_params is None:
            agent_params = {}
        if reward_params is None:
            reward_params = {}

        # Aplicar semilla para reproducibilidad si se proporciona
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
            torch.manual_seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed(seed)
                torch.cuda.manual_seed_all(seed)
            agent_params['seed'] = seed

        logger.info(f"Iniciando experimento de Job Shop Scheduling con RL (problema={problem_id}, reward_strategy={reward_strategy})...")

        # Guardar configuración del experimento
        from jobshop_rl.utils.experiment_config import ExperimentConfig
        
        # Generar un nombre de experimento único si no se proporcionó uno
        if experiment_name is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            experiment_name = f"{problem_id}_{reward_strategy}_{timestamp}"
        
        # Recopilar todos los parámetros en un solo diccionario
        config = {
            'experiment_name': experiment_name,
            'episodes': episodes,
            'reward_strategy': reward_strategy,
            'problem_id': problem_id,
            'seed': seed,
            'visualize': visualize,
            'save_plots': save_plots,
            'csv_logging': csv_logging,
        }
        
        # Añadir parámetros del agente
        if agent_params:
            config.update(agent_params)
            
        # Añadir parámetros de recompensa
        if reward_params:
            config.update(reward_params)
            
        # Guardar la configuración
        config_path = ExperimentConfig.save_config(
            config, 
            experiment_name=experiment_name,
            output_dir=os.path.join(output_dir, "configs")
        )
        logger.info(f"Configuración del experimento guardada en: {config_path}")
        
        # Crear entorno a partir del problema ID
        env = ExperimentFactory.create_env_from_problem_id(
            problem_id=problem_id,
            reward_strategy=reward_strategy, 
            seed=seed, 
            **reward_params
        )

        # Evaluar heurísticas básicas
        logger.info("Evaluando heurísticas básicas como referencia:")
        evaluator = HeuristicEvaluator(env)
        heuristic_results = evaluator.evaluate_all()
        
        # Configurar logger CSV si está habilitado
        csv_logger = None
        if csv_logging:
            logger.info("Inicializando registro CSV para datos de entrenamiento")
            csv_logger = TrainingLogger(filename=csv_filename, base_dir=csv_base_dir)

        # Crear y entrenar agente
        logger.info("Creando y entrenando agente PPO...")
        default_params = {
            "feature_dim": 7,
            "hidden_dim": 128,
            "lr": 0.0003,
            "gamma": 0.99,
            "eps_clip": 0.2,
            "K_epochs": 4,
            "entropy_coef": 0.01,
            "use_lr_decay": True,
            "use_grad_clip": True,
            "advantage_normalization": True,
            "gae_lambda": 0.95,
            "csv_logger": csv_logger
        }
        # Actualizar con parámetros proporcionados
        default_params.update(agent_params)

        agent = ExperimentFactory.create_agent(env, **default_params)
        agent.train(episodes=episodes, dynamic_entropy=True, early_stopping=True)

        # Evaluar la política final
        logger.info("Evaluando la política final...")
        makespan, schedule, makespan_history, _ = agent.evaluate_policy()
        logger.info(f"Makespan final: {makespan}")
        logger.info(f"Mejor makespan durante entrenamiento: {agent.best_makespan}")
        
        # Obtener información de límites del problema
        if hasattr(env, 'problem_analysis'):
            best_lower_bound = env.problem_analysis.get('best_lower_bound', 0)
            if best_lower_bound > 0:
                gap = ((agent.best_makespan - best_lower_bound) / best_lower_bound) * 100
                logger.info(f"Mejor límite inferior: {best_lower_bound}")
                logger.info(f"Gap respecto al límite: {gap:.2f}%")

        # Comparar con las heurísticas
        comparison = evaluator.compare_with_agent(agent.best_makespan)

        # Generar visualizaciones
        plots = {}
        if visualize:
            logger.info("Generando visualizaciones...")
            
            # Usar la mejor solución para las gráficas si está disponible
            if agent.best_schedule:
                plots["best_schedule"] = env.render_schedule("Mejor Planificación Encontrada con RL-PPO", agent.best_schedule)
                
            plots["schedule"] = env.render_schedule("Planificación Final con RL-PPO")
            
            # Usar el historial de makespan de la mejor solución si está disponible
            if agent.best_makespan_history:
                plots["best_solution_makespan"] = agent.plot_best_solution_makespan()
                
            # Usar referencia del límite inferior para el gráfico de makespan si está disponible
            reference_value = None
            if hasattr(env, 'problem_analysis') and 'best_lower_bound' in env.problem_analysis:
                reference_value = env.problem_analysis['best_lower_bound']
                
            plots["episode_makespan"] = env.plot_makespan_history(reference_value=reference_value)
            plots["training_makespan"] = agent.plot_training_history(optimal_makespan=reference_value)
            plots["rewards"] = agent.plot_reward_history()
            plots["losses"] = agent.plot_losses()
            plots["exploration"] = agent.plot_exploration_history()

            # Guardar gráficos si está habilitado
            if save_plots:
                plots_dir = os.path.join(output_dir, "plots")
                os.makedirs(plots_dir, exist_ok=True)
                plot_prefix = f"{problem_id}_{reward_strategy}_{episodes}ep"
                logger.info(f"Guardando visualizaciones en directorio: {plots_dir}")
                visualization_save_plots(plots, directory=plots_dir, prefix=plot_prefix)

        # Evaluación del mejor modelo con ABZ10 si está habilitado y no es el problema actual
        abz10_results = None
        if evaluate_abz10 and problem_id.lower() != "abz10":
            logger.info("Evaluando el mejor modelo con el problema ABZ10...")
            
            # Importar datos del problema ABZ10
            abz10_data = get_abz10_problem()
            
            # Crear entorno ABZ10 con la misma estrategia de recompensa
            abz10_env = ExperimentFactory.create_env_from_problem(
                abz10_data, 
                reward_strategy=reward_strategy, 
                seed=seed, 
                **reward_params
            )
            
            # Crear un agente de evaluación usando el mejor modelo encontrado
            abz10_agent = PPOAgent(abz10_env)
            
            # Cargar el mejor modelo si está disponible, si no, usar el modelo actual
            if agent.best_model_state:
                abz10_agent.policy.load_state_dict(agent.best_model_state["policy"])
                abz10_agent.value.load_state_dict(agent.best_model_state["value"])
                logger.info("Cargado el mejor modelo encontrado durante el entrenamiento")
            else:
                abz10_agent.policy.load_state_dict(agent.policy.state_dict())
                abz10_agent.value.load_state_dict(agent.value.state_dict())
                logger.info("Usando el modelo final del entrenamiento (no se encontró mejor modelo guardado)")
            
            # Evaluar en ABZ10 y medir tiempo
            abz10_makespan, abz10_schedule, abz10_makespan_history, rl_execution_time = abz10_agent.evaluate_policy()
            
            # Comparar con heurísticas
            logger.info("Comparando con heurísticas clásicas en ABZ10...")
            abz10_evaluator = HeuristicEvaluator(abz10_env)
            abz10_heuristic_results, abz10_execution_times = abz10_evaluator.evaluate_all(True)
            abz10_comparison = abz10_evaluator.compare_with_agent(abz10_makespan)
            
            # Registrar el orden de tareas y el makespan en el log
            logger.info("=== Resultados de la evaluación en ABZ10 ===")
            logger.info(f"Makespan ABZ10 (RL): {abz10_makespan}, Tiempo: {rl_execution_time:.4f} segundos")
            
            # Mostrar resultados de heurísticas
            logger.info("Comparación con heurísticas:")
            for heuristic, makespan in abz10_heuristic_results.items():
                exec_time = abz10_execution_times[heuristic]
                logger.info(f"{heuristic}: Makespan = {makespan}, Tiempo: {exec_time:.4f} segundos")
                
            logger.info("Mejora porcentual en makespan:")
            for heuristic, improvement in abz10_comparison.items():
                logger.info(f"vs {heuristic}: {improvement:.2f}%")
            
            # Ordenar las operaciones por tiempo de inicio
            sorted_schedule = sorted(abz10_schedule, key=lambda x: x['start'])
            
            # Mostrar el orden de tareas en el log
            logger.info("Orden de tareas de la planificación:")
            for i, op in enumerate(sorted_schedule):
                logger.info(f"{i+1}. Job {op['job']}, Operación {op['operation']}, Máquina {op['machine']}, Inicio: {op['start']}, Fin: {op['end']}")
            
            # Generar y guardar el diagrama de Gantt si está habilitado
            if visualize:
                abz10_gantt = abz10_env.render_schedule(f"Planificación ABZ10 con Mejor Modelo (Makespan: {abz10_makespan})", abz10_schedule)
                plots["abz10_schedule"] = abz10_gantt
                
                if save_plots:
                    plots_dir = os.path.join(output_dir, "plots")
                    timestamp = time.strftime("%Y%m%d-%H%M%S")
                    abz10_gantt_path = os.path.join(plots_dir, f"{problem_id}_{reward_strategy}_{episodes}ep_abz10_schedule_{timestamp}.png")
                    abz10_gantt.savefig(abz10_gantt_path)
                    logger.info(f"Diagrama de Gantt de ABZ10 guardado en: {abz10_gantt_path}")
            
            # Guardar resultados de ABZ10
            abz10_results = {
                "makespan": abz10_makespan,
                "schedule": abz10_schedule,
                "makespan_history": abz10_makespan_history,
                "execution_time": rl_execution_time,
                "heuristic_results": abz10_heuristic_results,
                "heuristic_times": abz10_execution_times,
                "comparison": abz10_comparison
            }
        
        return agent, {
            "heuristic_results": heuristic_results,
            "comparison": comparison,
            "best_makespan": agent.best_makespan,
            "final_makespan": makespan,
            "abz10_results": abz10_results,
            "plots": plots if visualize else None
        }
