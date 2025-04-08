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
import traceback
from typing import Dict, List, Tuple, Any, Optional

from jobshop_rl.utils.visualization import save_plots as visualization_save_plots
from jobshop_rl.environment.job_shop_env import JobShopEnv
from jobshop_rl.agents.ppo_agent import PPOAgent
from jobshop_rl.rewards.strategies import RewardStrategyFactory
from jobshop_rl.experiments.evaluator import HeuristicEvaluator
from jobshop_rl.utils.logging import TrainingLogger
from jobshop_rl.utils.problem_analyzer import ProblemAnalyzer, AdaptiveConfigGenerator
from jobshop_rl.data.problem_loader import ProblemLoader
from jobshop_rl.data.ft10 import get_ft10_problem
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
            return get_ft10_problem()
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
                           evaluate_other_problem: bool = False,
                           evaluation_problem_id: Optional[str] = None,
                           use_ortools: bool = False,
                           ortools_time_limit: int = 60) -> Tuple[PPOAgent, Dict]:
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
        heuristic_results = evaluator.evaluate_all(use_ortools=use_ortools)
        
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

        # No evaluamos la política final para evitar discrepancias con el entrenamiento
        logger.info("Obteniendo resultados finales...")
        # Usamos el último makespan registrado durante el entrenamiento
        last_makespan = agent.training_makespan_history[-1] if agent.training_makespan_history else float('inf')
        logger.info(f"Makespan final (último episodio): {last_makespan}")
        logger.info(f"Mejor makespan durante entrenamiento: {agent.best_makespan}")
        
        # Evaluar con OR-Tools para comparación
        ortools_results = None
        if use_ortools:
            try:
                from jobshop_rl.heuristics.ortools_solver import JobShopORToolsSolver, ORTOOLS_AVAILABLE
                
                if ORTOOLS_AVAILABLE:
                    logger.info(f"Evaluando con Google OR-Tools para comparación (tiempo límite: {ortools_time_limit} segundos)...")
                    ortools_makespan, _, ortools_time = JobShopORToolsSolver.solve(
                        env.sequences, env.durations, time_limit_seconds=ortools_time_limit
                    )
                    
                    if ortools_makespan < float('inf'):
                        gap_vs_ortools = ((agent.best_makespan - ortools_makespan) / ortools_makespan) * 100
                        logger.info(f"Makespan con OR-Tools: {ortools_makespan} (tiempo: {ortools_time:.2f}s)")
                        logger.info(f"Gap respecto a OR-Tools: {gap_vs_ortools:.2f}%")
                        
                        # Guardar resultados
                        ortools_results = {
                            "makespan": ortools_makespan,
                            "execution_time": ortools_time,
                            "gap": gap_vs_ortools
                        }
                    else:
                        logger.warning("OR-Tools no pudo encontrar una solución factible.")
                else:
                    logger.info("Google OR-Tools no está disponible. Instálelo con: pip install ortools")
            except ImportError:
                logger.info("No se pudo importar OR-Tools. Instálelo con: pip install ortools")
            except Exception as e:
                logger.error(f"Error al evaluar con OR-Tools: {str(e)}")
        
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

        # Evaluación del mejor modelo con otro problema si está habilitado y no es el problema de entrenamiento
        eval_results = None
        if evaluate_other_problem and evaluation_problem_id and evaluation_problem_id.lower() != problem_id.lower():
            logger.info(f"Evaluando el mejor modelo con el problema {evaluation_problem_id}...")
            
            try:
                # Obtener datos del problema de evaluación
                eval_data = ExperimentFactory.load_problem_by_id(evaluation_problem_id)
                
                # Crear entorno de evaluación con la misma estrategia de recompensa
                eval_env = ExperimentFactory.create_env_from_problem(
                    eval_data, 
                    reward_strategy=reward_strategy, 
                    seed=seed, 
                    **reward_params
                )
                
                # Crear un agente de evaluación usando el mejor modelo encontrado
                eval_agent = PPOAgent(eval_env)
                
                # Cargar el mejor modelo si está disponible, si no, usar el modelo actual
                if agent.best_model_state:
                    eval_agent.policy.load_state_dict(agent.best_model_state["policy"])
                    eval_agent.value.load_state_dict(agent.best_model_state["value"])
                    logger.info("Cargado el mejor modelo encontrado durante el entrenamiento")
                else:
                    eval_agent.policy.load_state_dict(agent.policy.state_dict())
                    eval_agent.value.load_state_dict(agent.value.state_dict())
                    logger.info("Usando el modelo final del entrenamiento (no se encontró mejor modelo guardado)")
                
                # Evaluar en el problema de evaluación y medir tiempo
                eval_makespan, eval_schedule, eval_makespan_history, rl_execution_time = eval_agent.evaluate_policy()
                
                # Comparar con heurísticas
                logger.info(f"Comparando con heurísticas clásicas en {evaluation_problem_id}...")
                eval_evaluator = HeuristicEvaluator(eval_env)
                eval_heuristic_results, eval_execution_times = eval_evaluator.evaluate_all(True, use_ortools)
                eval_comparison = eval_evaluator.compare_with_agent(eval_makespan)
                
                # Registrar el orden de tareas y el makespan en el log
                logger.info(f"=== Resultados de la evaluación en {evaluation_problem_id} ===")
                logger.info(f"Makespan {evaluation_problem_id} (RL): {eval_makespan}, Tiempo: {rl_execution_time:.4f} segundos")
                
                # Mostrar resultados de heurísticas
                logger.info("Comparación con heurísticas:")
                for heuristic, makespan in eval_heuristic_results.items():
                    exec_time = eval_execution_times[heuristic]
                    logger.info(f"{heuristic}: Makespan = {makespan}, Tiempo: {exec_time:.4f} segundos")
                    
                logger.info("Mejora porcentual en makespan:")
                for heuristic, improvement in eval_comparison.items():
                    logger.info(f"vs {heuristic}: {improvement:.2f}%")
                
                # Ordenar las operaciones por tiempo de inicio
                sorted_schedule = sorted(eval_schedule, key=lambda x: x['start'])
                
                # Mostrar el orden de tareas en el log
                logger.info("Orden de tareas de la planificación:")
                for i, op in enumerate(sorted_schedule):
                    logger.info(f"{i+1}. Job {op['job']}, Operación {op['operation']}, Máquina {op['machine']}, Inicio: {op['start']}, Fin: {op['end']}")
                
                # Generar y guardar el diagrama de Gantt si está habilitado
                if visualize:
                    eval_gantt = eval_env.render_schedule(f"Planificación {evaluation_problem_id} con Mejor Modelo (Makespan: {eval_makespan})", eval_schedule)
                    plots[f"{evaluation_problem_id}_schedule"] = eval_gantt
                    
                    if save_plots:
                        plots_dir = os.path.join(output_dir, "plots")
                        timestamp = time.strftime("%Y%m%d-%H%M%S")
                        eval_gantt_path = os.path.join(plots_dir, f"{problem_id}_{reward_strategy}_{episodes}ep_{evaluation_problem_id}_schedule_{timestamp}.png")
                        eval_gantt.savefig(eval_gantt_path)
                        logger.info(f"Diagrama de Gantt de {evaluation_problem_id} guardado en: {eval_gantt_path}")
                
                # Guardar resultados de evaluación
                eval_results = {
                    "problem_id": evaluation_problem_id,
                    "makespan": eval_makespan,
                    "schedule": eval_schedule,
                    "makespan_history": eval_makespan_history,
                    "execution_time": rl_execution_time,
                    "heuristic_results": eval_heuristic_results,
                    "heuristic_times": eval_execution_times,
                    "comparison": eval_comparison
                }
            except Exception as e:
                logger.error(f"Error al evaluar el problema {evaluation_problem_id}: {str(e)}")
                logger.error(f"Detalles: {traceback.format_exc()}")
        
        # Obtener el último makespan registrado durante el entrenamiento
        last_makespan = agent.training_makespan_history[-1] if agent.training_makespan_history else float('inf')
        
        return agent, {
            "heuristic_results": heuristic_results,
            "comparison": comparison,
            "best_makespan": agent.best_makespan,
            "final_makespan": last_makespan,
            "evaluation_results": eval_results,
            "ortools_results": ortools_results,
            "plots": plots if visualize else None
        }
