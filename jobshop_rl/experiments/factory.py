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
from typing import Dict, List, Tuple, Any, Optional
from jobshop_rl.utils.visualization import save_plots as visualization_save_plots
from jobshop_rl.environment.job_shop_env import JobShopEnv
from jobshop_rl.agents.ppo_agent import PPOAgent
from jobshop_rl.rewards.strategies import RewardStrategyFactory
from jobshop_rl.experiments.evaluator import HeuristicEvaluator
from jobshop_rl.utils.logging import TrainingLogger

logger = logging.getLogger("JobShopRL.ExperimentFactory")

class ExperimentFactory:
    """Fábrica para crear y ejecutar experimentos (patrón Factory)"""

    @staticmethod
    def create_ft10_env(reward_strategy: str = "basic", seed: Optional[int] = None, **reward_params) -> JobShopEnv:
        """
        Crea un entorno con el benchmark FT10.
        
        Args:
            reward_strategy: Estrategia de recompensa a utilizar
            seed: Semilla para reproducibilidad
            **reward_params: Parámetros adicionales para la estrategia de recompensa
            
        Returns:
            Entorno de JobShop configurado para el problema FT10
        """
        # Configuración del problema FT10
        num_jobs = 10
        num_machines = 10
        sequences = [
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
        ]
        durations = [
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

        # Crear estrategia de recompensa
        reward_strategy_obj = RewardStrategyFactory.create_strategy(reward_strategy, **reward_params)

        # Crear y devolver el entorno
        return JobShopEnv(num_jobs, num_machines, sequences, durations, reward_strategy_obj, seed=seed)

    @staticmethod
    def create_env_from_problem(problem_data: Dict[str, Any], reward_strategy: str = "basic", **kwargs) -> JobShopEnv:
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
        seed = kwargs.get('seed')
        
        # Validar datos
        if not all([num_jobs, num_machines, sequences, durations]):
            raise ValueError("Datos de problema incompletos o en formato incorrecto")
        
        # Extraer parámetros para la estrategia de recompensa
        reward_params = {k: v for k, v in kwargs.items() if k not in ['seed']}
        
        # Crear estrategia de recompensa
        reward_strategy_obj = RewardStrategyFactory.create_strategy(reward_strategy, **reward_params)
        
        # Crear y devolver el entorno
        return JobShopEnv(num_jobs, num_machines, sequences, durations, reward_strategy_obj, seed=seed)

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
        return PPOAgent(env, csv_logger=csv_logger, **agent_params)

    @staticmethod
    def run_full_experiment(episodes: int = 100, reward_strategy: str = "basic",
                           agent_params: Dict = None, reward_params: Dict = None,
                           seed: Optional[int] = None, visualize: bool = True,
                           save_plots: bool = True, csv_logging: bool = True, 
                           csv_filename: Optional[str] = None, csv_base_dir: str = './') -> Tuple[PPOAgent, Dict]:
        """
        Ejecuta un experimento completo con evaluación de heurísticas y entrenamiento.
        
        Args:
            episodes: Número de episodios a entrenar
            reward_strategy: Tipo de estrategia de recompensa
            agent_params: Parámetros del agente
            reward_params: Parámetros de la estrategia de recompensa
            seed: Semilla para reproducibilidad
            visualize: Si se deben generar visualizaciones
            save_plots: Si se deben guardar las visualizaciones en archivos
            csv_logging: Si se deben registrar métricas en CSV
            csv_filename: Nombre del archivo CSV
            csv_base_dir: Directorio base para archivos CSV
            
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

        logger.info(f"Iniciando experimento de Job Shop Scheduling con RL (reward_strategy={reward_strategy})...")

        # Crear entorno
        env = ExperimentFactory.create_ft10_env(reward_strategy, seed=seed, **reward_params)

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
        makespan, schedule, makespan_history = agent.evaluate_policy()
        logger.info(f"Makespan final: {makespan}")
        logger.info(f"Mejor makespan durante entrenamiento: {agent.best_makespan}")
        logger.info(f"Óptimo conocido para FT10: 930")

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
                
            plots["episode_makespan"] = env.plot_makespan_history()
            plots["training_makespan"] = agent.plot_training_history()
            plots["rewards"] = agent.plot_reward_history()
            plots["losses"] = agent.plot_losses()
            plots["exploration"] = agent.plot_exploration_history()

            # Guardar gráficos si está habilitado
            if save_plots:
                output_dir = "plots"
                experiment_name = f"{reward_strategy}_{episodes}ep"
                logger.info(f"Guardando visualizaciones en directorio: {output_dir}")
                visualization_save_plots(plots, directory=output_dir, prefix=experiment_name)

        return agent, {
            "heuristic_results": heuristic_results,
            "comparison": comparison,
            "best_makespan": agent.best_makespan,
            "final_makespan": makespan,
            "plots": plots if visualize else None
        }