"""
Fábrica para la creación de experimentos de Job Shop Scheduling.
Implementa el patrón Factory para la creación de componentes del sistema.
"""

import random
import numpy as np
import torch
import logging
import time
import os
import datetime
import traceback
import sys
from typing import Dict, List, Tuple, Any, Optional

from jobshop_rl.utils.seed_utils import set_random_seed

from jobshop_rl.utils.visualization import save_plots
from jobshop_rl.environment.job_shop_env import JobShopEnv
from jobshop_rl.agents.ppo_agent import PPOAgent
from jobshop_rl.rewards.factory import RewardStrategyFactory
from jobshop_rl.experiments.evaluator import HeuristicEvaluator
from jobshop_rl.utils.logging import TrainingLogger
from jobshop_rl.utils.problem_analyzer import ProblemAnalyzer, AdaptiveConfigGenerator
from jobshop_rl.data.problem_loader import ProblemLoader
from jobshop_rl.utils.experiment_config import ExperimentConfig

logger = logging.getLogger("JobShopRL.ExperimentFactory")

class ProblemFactory:
    """Fábrica para cargar y gestionar problemas de Job Shop"""

    @staticmethod
    def load_problem_by_id(problem_id: str) -> Dict[str, Any]:
        """
        Carga los datos de un problema por su ID.
        
        Args:
            problem_id: Identificador del problema (ft10, ft20, abz10, tai15_15_01, etc.)
            
        Returns:
            Diccionario con los datos del problema
            
        Raises:
            ValueError: Si el problema no es reconocido
        """
        problem_id = problem_id.lower()
        
        # Usar el registro de problemas del módulo data
        from jobshop_rl.data import PROBLEM_REGISTRY
        
        if problem_id in PROBLEM_REGISTRY:
            return PROBLEM_REGISTRY[problem_id]()
        
        # Intentar cargar desde archivo usando el ProblemLoader
        try:
            return ProblemLoader.load_problem(problem_id)
        except Exception as e:
            logger.error(f"Error cargando problema {problem_id}: {str(e)}")
            raise ValueError(f"Problema no reconocido o no pudo cargarse: {problem_id}")


class EnvironmentFactory:
    """Fábrica para crear entornos de Job Shop"""

    @staticmethod
    def create_from_problem_id(problem_id: str, reward_strategy: str = "adaptive", 
                              seed: Optional[int] = None, **reward_params) -> JobShopEnv:
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
        problem_data = ProblemFactory.load_problem_by_id(problem_id)
        return EnvironmentFactory.create_from_problem(
            problem_data, 
            reward_strategy=reward_strategy, 
            seed=seed, 
            problem_id=problem_id,
            **reward_params
        )
    
    @staticmethod
    def create_from_problem(problem_data: Dict[str, Any], reward_strategy: str = "adaptive", 
                          seed: Optional[int] = None, problem_id: Optional[str] = None, 
                          **reward_params) -> JobShopEnv:
        """
        Crea un entorno a partir de los datos de un problema.
        
        Args:
            problem_data: Datos del problema (secuencias, duraciones, etc.)
            reward_strategy: Estrategia de recompensa a utilizar
            seed: Semilla para reproducibilidad
            problem_id: Identificador del problema (opcional)
            **reward_params: Parámetros adicionales para la estrategia de recompensa
            
        Returns:
            Entorno de JobShop configurado para el problema especificado
        """
        num_jobs = problem_data.get('num_jobs')
        num_machines = problem_data.get('num_machines')
        sequences = problem_data.get('sequences')
        durations = problem_data.get('durations')
        problem_id = problem_id or problem_data.get('problem_id', 'custom')
        
        # Validar datos
        if not all([num_jobs, num_machines, sequences, durations]):
            raise ValueError("Datos de problema incompletos o en formato incorrecto")
        
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


class AgentFactory:
    """Fábrica para crear agentes de aprendizaje por refuerzo"""

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
        # Parámetros por defecto
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
            "gae_lambda": 0.95
        }
        
        # Si el entorno tiene análisis del problema, adaptar los parámetros del agente
        if hasattr(env, 'problem_analysis') and not agent_params:
            adapted_params = AdaptiveConfigGenerator.generate_agent_config(env.problem_analysis)
            logger.info("Adaptando parámetros del agente según características del problema")
            # Combinar con parámetros por defecto
            adapted_params = {**default_params, **adapted_params}
            # Combinar con parámetros proporcionados
            adapted_params.update(agent_params)
            agent_params = adapted_params
        else:
            # Combinar con parámetros por defecto
            default_params.update(agent_params)
            agent_params = default_params
            
        # Añadir logger CSV si se proporciona
        if csv_logger:
            agent_params['csv_logger'] = csv_logger
            
        return PPOAgent(env, **agent_params)


class ExperimentRunner:
    """Ejecutor de experimentos de Job Shop Scheduling con RL"""
    
    def __init__(self, env: JobShopEnv, agent: PPOAgent, 
                output_dir: str = 'outputs',
                experiment_name: Optional[str] = None,
                visualize: bool = True,
                save_plots: bool = True):
        """
        Inicializa el ejecutor de experimentos.
        
        Args:
            env: Entorno de JobShop
            agent: Agente de RL
            output_dir: Directorio de salida para resultados
            experiment_name: Nombre del experimento
            visualize: Si se deben generar visualizaciones
            save_plots: Si se deben guardar las visualizaciones
        """
        self.env = env
        self.agent = agent
        self.output_dir = output_dir
        self.visualize = visualize
        self.save_plots = save_plots
        
        # Generar un nombre de experimento único si no se proporcionó uno
        if experiment_name is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            problem_id = getattr(env, 'problem_id', 'unknown')
            self.experiment_name = f"{problem_id}_{timestamp}"
        else:
            self.experiment_name = experiment_name
            
        # Crear directorio para resultados del experimento
        os.makedirs(output_dir, exist_ok=True)
        
    def train(self, episodes: int, **train_params) -> Tuple[float, Dict[str, Any]]:
        """
        Entrena al agente para el experimento actual.
        
        Args:
            episodes: Número de episodios a entrenar
            **train_params: Parámetros adicionales para entrenamiento
            
        Returns:
            Tupla con el mejor makespan y un diccionario con resultados
        """
        logger.info(f"Iniciando entrenamiento para {self.experiment_name} ({episodes} episodios)")
        
        # Entrenar el agente
        start_time = time.time()
        self.agent.train(episodes=episodes, **train_params)
        training_time = time.time() - start_time
        
        logger.info(f"Entrenamiento completado en {training_time:.2f} segundos")
        logger.info(f"Mejor makespan: {self.agent.best_makespan}")
        
        # Obtener el último makespan registrado durante el entrenamiento
        last_makespan = self.agent.training_makespan_history[-1] if self.agent.training_makespan_history else float('inf')
        
        # Generar visualizaciones si está habilitado
        plots = {}
        if self.visualize:
            plots = self._generate_visualizations()
            
            # Guardar gráficos si está habilitado
            if self.save_plots:
                plots_dir = os.path.join(self.output_dir, "plots")
                os.makedirs(plots_dir, exist_ok=True)
                plot_prefix = f"{self.experiment_name}"
                logger.info(f"Guardando visualizaciones en directorio: {plots_dir}")
                save_plots(plots, directory=plots_dir, prefix=plot_prefix)
        
        return self.agent.best_makespan, {
            "best_makespan": self.agent.best_makespan,
            "final_makespan": last_makespan,
            "training_time": training_time,
            "plots": plots if self.visualize else None
        }
    
    def evaluate_heuristics(self, use_ortools: bool = False, time_limit: int = 60) -> Dict[str, float]:
        """
        Evalúa heurísticas básicas como referencia.
        
        Args:
            use_ortools: Si se debe evaluar también usando OR-Tools
            time_limit: Límite de tiempo para OR-Tools en segundos
            
        Returns:
            Diccionario con resultados de las heurísticas
        """
        logger.info("Evaluando heurísticas básicas como referencia")
        evaluator = HeuristicEvaluator(self.env)
        return evaluator.evaluate_all(use_ortools=use_ortools)
    
    def compare_with_heuristics(self, heuristic_results: Dict[str, float]) -> Dict[str, float]:
        """
        Compara el rendimiento del agente con las heurísticas evaluadas.
        
        Args:
            heuristic_results: Resultados de las heurísticas
            
        Returns:
            Diccionario con el porcentaje de mejora respecto a cada heurística
        """
        evaluator = HeuristicEvaluator(self.env)
        evaluator.results = heuristic_results
        return evaluator.compare_with_agent(self.agent.best_makespan)
    
    def evaluate_on_other_problem(self, problem_id: str, **kwargs) -> Dict[str, Any]:
        """
        Evalúa el mejor modelo encontrado en otro problema.
        
        Args:
            problem_id: Identificador del problema de evaluación
            **kwargs: Parámetros adicionales para la evaluación
            
        Returns:
            Diccionario con los resultados de la evaluación
        """
        logger.info(f"Evaluando el mejor modelo con el problema {problem_id}...")
        
        try:
            # Obtener datos del problema de evaluación
            eval_data = ProblemFactory.load_problem_by_id(problem_id)
            
            # Usar los mismos parámetros de recompensa que el experimento original
            reward_strategy = self.env.reward_strategy.__class__.__name__
            if reward_strategy.endswith('RewardStrategy'):
                reward_strategy = reward_strategy[:-14]  # Quitar el sufijo 'RewardStrategy'
            reward_strategy = reward_strategy.lower()
            
            # Crear entorno de evaluación con la misma estrategia de recompensa
            eval_env = EnvironmentFactory.create_from_problem(
                eval_data, 
                reward_strategy=reward_strategy
            )
            
            # Crear un agente de evaluación usando el mejor modelo encontrado
            eval_agent = AgentFactory.create_agent(eval_env)
            
            # Cargar el mejor modelo si está disponible, si no, usar el modelo actual
            if self.agent.best_model_state:
                eval_agent.policy.load_state_dict(self.agent.best_model_state["policy"])
                eval_agent.value.load_state_dict(self.agent.best_model_state["value"])
                logger.info("Cargado el mejor modelo encontrado durante el entrenamiento")
            else:
                eval_agent.policy.load_state_dict(self.agent.policy.state_dict())
                eval_agent.value.load_state_dict(self.agent.value.state_dict())
                logger.info("Usando el modelo final del entrenamiento (no se encontró mejor modelo guardado)")
            
            # Evaluar en el problema de evaluación y medir tiempo
            makespan, schedule, makespan_history, execution_time = eval_agent.evaluate_policy()
            
            # Comparar con heurísticas
            logger.info(f"Comparando con heurísticas clásicas en {problem_id}...")
            eval_evaluator = HeuristicEvaluator(eval_env)
            heuristic_results, execution_times = eval_evaluator.evaluate_all(True, use_ortools=kwargs.get('use_ortools', False))
            comparison = eval_evaluator.compare_with_agent(makespan)
            
            # Generar visualización del resultado si está habilitado
            if self.visualize:
                eval_gantt = eval_env.render_schedule(
                    f"Planificación {problem_id} con Mejor Modelo (Makespan: {makespan})", 
                    schedule
                )
                
                if self.save_plots:
                    plots_dir = os.path.join(self.output_dir, "plots")
                    os.makedirs(plots_dir, exist_ok=True)
                    timestamp = time.strftime("%Y%m%d-%H%M%S")
                    eval_gantt_path = os.path.join(
                        plots_dir, 
                        f"{self.experiment_name}_{problem_id}_schedule_{timestamp}.png"
                    )
                    eval_gantt.savefig(eval_gantt_path)
                    logger.info(f"Diagrama de Gantt de {problem_id} guardado en: {eval_gantt_path}")
            
            return {
                "problem_id": problem_id,
                "makespan": makespan,
                "schedule": schedule,
                "makespan_history": makespan_history,
                "execution_time": execution_time,
                "heuristic_results": heuristic_results,
                "heuristic_times": execution_times,
                "comparison": comparison
            }
        except Exception as e:
            logger.error(f"Error al evaluar el problema {problem_id}: {str(e)}")
            logger.error(f"Detalles: {traceback.format_exc()}")
            return {"error": str(e)}
    
    def _generate_visualizations(self) -> Dict[str, Any]:
        """
        Genera visualizaciones para el experimento.
        
        Returns:
            Diccionario con las visualizaciones generadas
        """
        plots = {}
        
        # Usar la mejor solución para las gráficas si está disponible
        if self.agent.best_schedule:
            plots["best_schedule"] = self.env.render_schedule(
                "Mejor Planificación Encontrada con RL-PPO", 
                self.agent.best_schedule
            )
            
        plots["schedule"] = self.env.render_schedule("Planificación Final con RL-PPO")
        
        # Usar el historial de makespan de la mejor solución si está disponible
        if self.agent.best_makespan_history:
            plots["best_solution_makespan"] = self.agent.plot_best_solution_makespan()
            
        # Usar referencia del límite inferior para el gráfico de makespan si está disponible
        reference_value = None
        if hasattr(self.env, 'problem_analysis') and 'best_lower_bound' in self.env.problem_analysis:
            reference_value = self.env.problem_analysis['best_lower_bound']
            
        plots["episode_makespan"] = self.env.plot_makespan_history(reference_value=reference_value)
        plots["training_makespan"] = self.agent.plot_training_history(optimal_makespan=reference_value)
        plots["rewards"] = self.agent.plot_reward_history()
        plots["losses"] = self.agent.plot_losses()
        plots["exploration"] = self.agent.plot_exploration_history()
        
        return plots


class ExperimentFactory:
    """Fábrica para crear y ejecutar experimentos (patrón Factory)"""

    @staticmethod
    def create_experiment(
        problem_id: str, 
        reward_strategy: str = "adaptive",
        agent_params: Dict = None, 
        reward_params: Dict = None,
        seed: Optional[int] = None,
        visualize: bool = True,
        save_plots: bool = True,
        output_dir: str = 'outputs',
        experiment_name: Optional[str] = None,
        csv_logger: Optional[TrainingLogger] = None
    ) -> Tuple[JobShopEnv, PPOAgent, ExperimentRunner]:
        """
        Crea un experimento completo con entorno, agente y ejecutor.
        
        Args:
            problem_id: Identificador del problema
            reward_strategy: Tipo de estrategia de recompensa
            agent_params: Parámetros del agente
            reward_params: Parámetros de la estrategia de recompensa
            seed: Semilla para reproducibilidad
            visualize: Si se deben generar visualizaciones
            save_plots: Si se deben guardar las visualizaciones
            output_dir: Directorio para resultados
            experiment_name: Nombre del experimento
            csv_logger: Logger para datos de entrenamiento
            
        Returns:
            Tupla (entorno, agente, ejecutor) configurados para el experimento
        """
        # Aplicar semilla para reproducibilidad usando la utilidad centralizada
        set_random_seed(seed)
                
        # Valores por defecto
        agent_params = agent_params or {}
        reward_params = reward_params or {}
        
        # Generar un nombre de experimento único si no se proporcionó uno
        if experiment_name is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            experiment_name = f"{problem_id}_{reward_strategy}_{timestamp}"
        
        # Crear entorno y agente
        env = EnvironmentFactory.create_from_problem_id(
            problem_id=problem_id,
            reward_strategy=reward_strategy,
            seed=seed,
            **reward_params
        )
        
        agent = AgentFactory.create_agent(
            env=env, 
            csv_logger=csv_logger,
            **agent_params
        )
        
        # Crear ejecutor de experimentos
        runner = ExperimentRunner(
            env=env,
            agent=agent,
            output_dir=output_dir,
            experiment_name=experiment_name,
            visualize=visualize,
            save_plots=save_plots
        )
        
        return env, agent, runner

    @staticmethod
    def run_full_experiment(
        episodes: int = 100, 
        reward_strategy: str = "adaptive",
        agent_params: Dict = None, 
        reward_params: Dict = None,
        problem_id: str = "ft10", 
        seed: Optional[int] = None, 
        visualize: bool = True, 
        save_plots: bool = True, 
        csv_logging: bool = True, 
        csv_filename: Optional[str] = None, 
        csv_base_dir: str = 'outputs', 
        output_dir: str = 'outputs', 
        experiment_name: Optional[str] = None,
        evaluate_other_problem: bool = False,
        evaluation_problem_id: Optional[str] = None,
        use_ortools: bool = False,
        ortools_time_limit: int = 60,
        save_config: bool = True
    ) -> Tuple[PPOAgent, Dict]:
        """
        Ejecuta un experimento completo con evaluación de heurísticas y entrenamiento.
        
        El experimento incluye:
        1. Entrenamiento del agente en el problema especificado (por defecto FT10)
        2. Evaluación y comparación con heurísticas
        3. Opcionalmente, evaluación del mejor modelo encontrado con otro problema
        
        Args:
            episodes: Número de episodios a entrenar
            reward_strategy: Tipo de estrategia de recompensa
            agent_params: Parámetros del agente
            reward_params: Parámetros de la estrategia de recompensa
            problem_id: Identificador del problema (ft10, ft20, abz10, etc.)
            seed: Semilla para reproducibilidad
            visualize: Si se deben generar visualizaciones
            save_plots: Si se deben guardar las visualizaciones
            csv_logging: Si se deben registrar métricas en CSV
            csv_filename: Nombre del archivo CSV
            csv_base_dir: Directorio base para archivos CSV
            output_dir: Directorio de salida para resultados
            experiment_name: Nombre del experimento
            evaluate_other_problem: Si se debe evaluar el mejor modelo con otro problema
            evaluation_problem_id: ID del problema para evaluación adicional
            use_ortools: Si se debe comparar con el solucionador OR-Tools
            ortools_time_limit: Límite de tiempo para OR-Tools
            save_config: Si se debe guardar la configuración del experimento
            
        Returns:
            Tupla (agente entrenado, resultados del experimento)
        """
        agent_params = agent_params or {}
        reward_params = reward_params or {}

        # Configurar CSV logger si está habilitado
        csv_logger = None
        if csv_logging:
            logger.info("Inicializando registro CSV para datos de entrenamiento")
            csv_logger = TrainingLogger(filename=csv_filename, base_dir=csv_base_dir)
            
        # Generar nombre de experimento si es necesario
        if experiment_name is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            experiment_name = f"{problem_id}_{reward_strategy}_{timestamp}"

        # Crear experimento completo (aquí se aplican las modificaciones adaptive)
        env, agent, runner = ExperimentFactory.create_experiment(
            problem_id=problem_id,
            reward_strategy=reward_strategy,
            agent_params=agent_params,
            reward_params=reward_params,
            seed=seed,
            visualize=visualize,
            save_plots=save_plots,
            output_dir=output_dir,
            experiment_name=experiment_name,
            csv_logger=csv_logger
        )
        
        # Guardar configuración del experimento DESPUÉS de aplicar modificaciones adaptive
        if save_config:
            # Extraer TODOS los parámetros para reproducibilidad exacta
            final_config = self._extract_complete_configuration(
                env, agent, experiment_name, episodes, reward_strategy, problem_id, 
                seed, visualize, save_plots, csv_logging
            )
                
            config_path = ExperimentConfig.save_config(
                final_config, 
                experiment_name=experiment_name,
                output_dir=os.path.join(output_dir, "configs")
            )
            logger.info(f"Configuración completa del experimento (con todos los parámetros) guardada en: {config_path}")
        else:
            logger.info("Guardado de configuración deshabilitado")
        
        # Evaluar heurísticas básicas
        logger.info("Evaluando heurísticas básicas como referencia")
        heuristic_results = runner.evaluate_heuristics(use_ortools=use_ortools)
        
        # Entrenar agente
        logger.info("Entrenando agente PPO...")
        _, training_results = runner.train(
            episodes=episodes, 
            dynamic_entropy=True, 
            early_stopping=True
        )
        
        # Comparar con heurísticas
        comparison = runner.compare_with_heuristics(heuristic_results)
        
        # Evaluación con otro problema si está habilitado
        eval_results = None
        if evaluate_other_problem and evaluation_problem_id and evaluation_problem_id.lower() != problem_id.lower():
            eval_results = runner.evaluate_on_other_problem(
                problem_id=evaluation_problem_id,
                use_ortools=use_ortools
            )
        
        # Extraer resultados de OR-Tools si están disponibles
        ortools_results = {}
        if use_ortools and 'OR-Tools' in heuristic_results:
            ortools_makespan = heuristic_results.get('OR-Tools', float('inf'))
            ortools_time = getattr(runner, 'ortools_time', 0)  # Si está disponible
            
            if ortools_makespan < float('inf'):
                gap_vs_ortools = ((agent.best_makespan - ortools_makespan) / ortools_makespan) * 100
                ortools_results = {
                    "makespan": ortools_makespan,
                    "execution_time": ortools_time,
                    "gap": gap_vs_ortools
                }

        return agent, {
            "heuristic_results": heuristic_results,
            "comparison": comparison,
            "best_makespan": agent.best_makespan,
            "final_makespan": training_results.get("final_makespan"),
            "evaluation_results": eval_results,
            "ortools_results": ortools_results,
            "plots": training_results.get("plots")
        }

    @staticmethod
    def _extract_complete_configuration(env, agent, experiment_name, episodes, reward_strategy, 
                                      problem_id, seed, visualize, save_plots, csv_logging):
        """
        Extrae TODOS los parámetros del experimento para reproducibilidad exacta.
        
        Args:
            env: Entorno configurado
            agent: Agente configurado
            experiment_name: Nombre del experimento
            episodes: Número de episodios
            reward_strategy: Estrategia de recompensa
            problem_id: ID del problema
            seed: Semilla usada
            visualize: Si se generan visualizaciones
            save_plots: Si se guardan gráficos
            csv_logging: Si se usa logging CSV
            
        Returns:
            Dict con configuración completa
        """
        import torch
        
        config = {
            # ==================== METADATOS DEL EXPERIMENTO ====================
            'experiment_name': experiment_name,
            'episodes': episodes,
            'reward_strategy': reward_strategy,
            'problem_id': problem_id,
            'seed': seed,
            'visualize': visualize,
            'save_plots': save_plots,
            'csv_logging': csv_logging,
            'adaptive_modifications_applied': reward_strategy.lower() == "adaptive",
            'timestamp': datetime.datetime.now().isoformat(),
            
            # ==================== INFORMACIÓN DEL PROBLEMA ====================
            'problem_info': {
                'num_jobs': env.num_jobs,
                'num_machines': env.num_machines,
                'problem_size': env.num_jobs * env.num_machines,
                'state_dim': getattr(agent, 'state_dim', env.num_jobs + env.num_machines + 2)
            },
            
            # ==================== PARÁMETROS DEL AGENTE PPO ====================
            'agent_params': {
                'lr': agent.lr,
                'current_lr_policy': agent.optimizer_policy.param_groups[0]['lr'],
                'current_lr_value': agent.optimizer_value.param_groups[0]['lr'],
                'gamma': agent.gamma,
                'eps_clip': agent.eps_clip,
                'K_epochs': agent.K_epochs,
                'entropy_coef': agent.entropy_coef,
                'initial_entropy_coef': getattr(agent, 'initial_entropy_coef', agent.entropy_coef),
                'use_lr_decay': agent.use_lr_decay,
                'use_grad_clip': agent.use_grad_clip,
                'advantage_normalization': agent.advantage_normalization,
                'gae_lambda': agent.gae_lambda,
                'feature_dim': agent.feature_dim,
                'hidden_dim': agent.hidden_dim,
                'policy_depth': getattr(agent, 'policy_depth', 2),
                'value_depth': getattr(agent, 'value_depth', 3),
                'use_batch_norm': getattr(agent, 'use_batch_norm', False),
                'use_advanced_networks': getattr(agent, 'use_advanced_networks', False),
                'dropout_rate': getattr(agent, 'dropout_rate', 0.1)
            },
            
            # ==================== PARÁMETROS DE MEMORIA PPO ====================
            'memory_params': {
                'gamma': agent.memory.gamma,
                'gae_lambda': agent.memory.gae_lambda,
                'advantage_normalization': agent.memory.advantage_normalization
            },
            
            # ==================== PARÁMETROS DEL OPTIMIZADOR ====================
            'optimizer_params': {
                'policy_optimizer': {
                    'type': agent.optimizer_policy.__class__.__name__,
                    'lr': agent.optimizer_policy.param_groups[0]['lr'],
                    'weight_decay': agent.optimizer_policy.param_groups[0].get('weight_decay', 0.0),
                    'eps': agent.optimizer_policy.param_groups[0].get('eps', 1e-8),
                },
                'value_optimizer': {
                    'type': agent.optimizer_value.__class__.__name__, 
                    'lr': agent.optimizer_value.param_groups[0]['lr'],
                    'weight_decay': agent.optimizer_value.param_groups[0].get('weight_decay', 0.0),
                    'eps': agent.optimizer_value.param_groups[0].get('eps', 1e-8),
                }
            },
            
            # ==================== CONFIGURACIÓN DE ENTRENAMIENTO AVANZADO ====================
            'advanced_training': {
                'use_gradient_accumulation': getattr(agent, 'use_gradient_accumulation', False),
                'accumulation_steps': getattr(agent, 'accumulation_steps', 1),
                'use_warmup': getattr(agent, 'use_warmup', False),
                'warmup_episodes': getattr(agent, 'warmup_episodes', 0),
                'min_batch_size': getattr(agent.batch_manager, 'min_batch_size', 4) if hasattr(agent, 'batch_manager') else 4,
                'target_batch_size': getattr(agent.batch_manager, 'target_batch_size', 8) if hasattr(agent, 'batch_manager') else 8
            },
            
            # ==================== ARQUITECTURA DE REDES NEURONALES ====================
            'network_architecture': {}
        }
        
        # Agregar parámetros específicos de Adam si aplica
        if isinstance(agent.optimizer_policy, torch.optim.Adam):
            config['optimizer_params']['policy_optimizer'].update({
                'betas': agent.optimizer_policy.param_groups[0].get('betas', (0.9, 0.999)),
                'amsgrad': agent.optimizer_policy.param_groups[0].get('amsgrad', False)
            })
            config['optimizer_params']['value_optimizer'].update({
                'betas': agent.optimizer_value.param_groups[0].get('betas', (0.9, 0.999)),
                'amsgrad': agent.optimizer_value.param_groups[0].get('amsgrad', False)
            })
        
        # Extraer arquitectura de redes neuronales
        try:
            # Información de la red de política
            policy_info = {
                'class_name': agent.policy.__class__.__name__,
                'total_params': sum(p.numel() for p in agent.policy.parameters()),
                'trainable_params': sum(p.numel() for p in agent.policy.parameters() if p.requires_grad)
            }
            
            # Información de la red de valor
            value_info = {
                'class_name': agent.value.__class__.__name__,
                'total_params': sum(p.numel() for p in agent.value.parameters()),
                'trainable_params': sum(p.numel() for p in agent.value.parameters() if p.requires_grad)
            }
            
            # Intentar extraer información detallada de las capas
            if hasattr(agent.policy, 'feature_extractor'):
                policy_info['has_feature_extractor'] = True
                if hasattr(agent.policy.feature_extractor, 'output_dim'):
                    policy_info['feature_extractor_output_dim'] = agent.policy.feature_extractor.output_dim
                    
            config['network_architecture'] = {
                'policy_network': policy_info,
                'value_network': value_info
            }
            
        except Exception as e:
            logger.warning(f"No se pudo extraer información completa de la arquitectura de red: {e}")
            config['network_architecture'] = {'error': str(e)}
        
        # ==================== PARÁMETROS DE ESTRATEGIA DE RECOMPENSA ====================
        config['reward_params'] = {}
        reward_strategy_obj = env.reward_strategy
        if hasattr(reward_strategy_obj, '__dict__'):
            for attr_name, attr_value in reward_strategy_obj.__dict__.items():
                if isinstance(attr_value, (int, float, bool, str, type(None))):
                    config['reward_params'][attr_name] = attr_value
        
        # Agregar información específica del tipo de estrategia
        config['reward_params']['strategy_class'] = reward_strategy_obj.__class__.__name__
        
        # ==================== ANÁLISIS DEL PROBLEMA ====================
        if hasattr(env, 'problem_analysis'):
            config['problem_analysis'] = env.problem_analysis
        
        # ==================== INFORMACIÓN DEL ENTORNO ====================
        config['environment_info'] = {
            'class_name': env.__class__.__name__,
            'action_space_size': len(env.get_features({'job_status': [0]*env.num_jobs, 
                                                      'machine_completion_time': [0]*env.num_machines})) 
                                  if hasattr(env, 'get_features') else 'unknown'
        }
        
        # ==================== INFORMACIÓN DEL SISTEMA ====================
        config['system_info'] = {
            'torch_version': torch.__version__,
            'cuda_available': torch.cuda.is_available(),
            'cuda_device_count': torch.cuda.device_count() if torch.cuda.is_available() else 0,
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        }
        
        return config
