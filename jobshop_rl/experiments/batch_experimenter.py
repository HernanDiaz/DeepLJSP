"""
Sistema de experimentación por lotes para entrenar y evaluar en múltiples problemas.
"""

import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import logging
from typing import List, Dict, Tuple, Any, Optional
from copy import deepcopy

from jobshop_rl.data.problem_loader import ProblemLoader
from jobshop_rl.experiments.factory import ExperimentFactory
from jobshop_rl.utils.logging import TrainingLogger
from jobshop_rl.agents.ppo_agent import PPOAgent
from jobshop_rl.utils.visualization import save_plots

logger = logging.getLogger("JobShopRL.BatchExperimenter")

class BatchExperimenter:
    """Ejecuta experimentos por lotes en múltiples problemas"""
    
    def __init__(self, 
                 training_dir: str, 
                 test_dir: str,
                 output_dir: str,
                 agent_params: Dict = None,
                 reward_strategy: str = "advanced",
                 reward_params: Dict = None,
                 seed: Optional[int] = None):
        """
        Inicializa el experimentador por lotes.
        
        Args:
            training_dir: Directorio con problemas de entrenamiento
            test_dir: Directorio con problemas de prueba
            output_dir: Directorio para guardar resultados
            agent_params: Parámetros para el agente PPO
            reward_strategy: Estrategia de recompensa a utilizar
            reward_params: Parámetros para la estrategia de recompensa
            seed: Semilla para reproducibilidad
        """
        logger.info(f"Cargando problemas de entrenamiento desde: {training_dir}")
        self.training_problems = ProblemLoader.load_from_directory(training_dir)
        
        logger.info(f"Cargando problemas de prueba desde: {test_dir}")
        self.test_problems = ProblemLoader.load_from_directory(test_dir)
        
        self.output_dir = output_dir
        self.agent_params = agent_params or {}
        self.reward_strategy = reward_strategy
        self.reward_params = reward_params or {}
        self.seed = seed
        
        # Crear directorio de salida si no existe
        os.makedirs(output_dir, exist_ok=True)
        
        logger.info(f"Configuración completa: {len(self.training_problems)} problemas de entrenamiento, "
                   f"{len(self.test_problems)} problemas de prueba")
        
    def train_agent(self, episodes_per_problem: int = 100) -> PPOAgent:
        """
        Entrena un agente en todos los problemas de entrenamiento.
        
        Args:
            episodes_per_problem: Número de episodios para entrenar en cada problema
            
        Returns:
            El mejor agente entrenado
        """
        # Inicializar logger global
        global_logger = TrainingLogger(
            filename=f"{self.output_dir}/global_training_log.csv"
        )
        
        # Verificar que haya problemas de entrenamiento
        if not self.training_problems:
            logger.error("No hay problemas de entrenamiento. Abortando.")
            return None
        
        # Inicializar el mejor agente con el primer problema
        logger.info("Inicializando entrenamiento con el primer problema")
        first_problem = self.training_problems[0]
        env = ExperimentFactory.create_env_from_problem(
            first_problem, 
            self.reward_strategy,
            seed=self.seed,
            **self.reward_params
        )
        
        best_agent = ExperimentFactory.create_agent(
            env,
            csv_logger=global_logger,
            **self.agent_params
        )
        
        # Guardar mejor makespan global
        best_global_makespan = float('inf')
        
        # Entrenar con todos los problemas de manera secuencial
        problem_results = []
        start_time_global = time.time()
        
        for i, problem in enumerate(self.training_problems):
            problem_name = problem.get('name', f"problem_{i}")
            logger.info(f"Entrenando con problema: {problem_name} ({i+1}/{len(self.training_problems)})")
            
            # Crear logger para este problema específico
            problem_logger = TrainingLogger(
                filename=f"{self.output_dir}/{problem_name}_training_log.csv"
            )
            
            # Configurar entorno para este problema
            env = ExperimentFactory.create_env_from_problem(
                problem,
                self.reward_strategy,
                seed=self.seed,
                **self.reward_params
            )
            
            # Si no es el primer problema, transferir conocimiento del mejor agente
            if i > 0:
                current_agent = ExperimentFactory.create_agent(
                    env, 
                    {**self.agent_params, 'csv_logger': problem_logger}
                )
                current_agent.policy.load_state_dict(best_agent.policy.state_dict())
                current_agent.value.load_state_dict(best_agent.value.state_dict())
            else:
                current_agent = best_agent
                current_agent.csv_logger = problem_logger
            
            # Entrenar en este problema
            start_time = time.time()
            current_agent.train(episodes=episodes_per_problem)
            training_time = time.time() - start_time
            
            # Evaluar rendimiento
            makespan, _, _ = current_agent.evaluate_policy()
            
            # Guardar checkpoint
            current_agent.save_checkpoint(f"{self.output_dir}/{problem_name}_model.pt")
            
            # Generar visualizaciones
            self._generate_problem_visualizations(current_agent, problem_name, env)
            
            # Guardar resultados para este problema
            problem_results.append({
                'problem': problem_name,
                'best_makespan': current_agent.best_makespan,
                'final_makespan': makespan,
                'training_time': training_time,
                'episodes': episodes_per_problem,
                'optimal': problem.get('optimal_makespan', 'Unknown')
            })
            
            # Actualizar mejor agente si este tuvo mejor rendimiento
            if current_agent.best_makespan < best_global_makespan:
                logger.info(f"Nuevo mejor makespan global: {current_agent.best_makespan} "
                           f"(anterior: {best_global_makespan})")
                best_global_makespan = current_agent.best_makespan
                best_agent = current_agent
        
        total_time = time.time() - start_time_global
        
        # Guardar resultados completos
        results_df = pd.DataFrame(problem_results)
        results_df.to_csv(f"{self.output_dir}/training_summary.csv", index=False)
        
        # Añadir estadísticas globales
        with open(f"{self.output_dir}/training_stats.txt", 'w') as f:
            f.write(f"Total problemas entrenados: {len(self.training_problems)}\n")
            f.write(f"Tiempo total de entrenamiento: {total_time:.2f} segundos\n")
            f.write(f"Mejor makespan global: {best_global_makespan}\n")
            
            if 'optimal' in results_df.columns:
                # Calcular gap promedio para problemas con óptimo conocido
                numeric_optimal = pd.to_numeric(results_df['optimal'], errors='coerce')
                mask = ~numeric_optimal.isna()
                if mask.any():
                    avg_gap = ((results_df.loc[mask, 'best_makespan'] - numeric_optimal[mask]) / 
                              numeric_optimal[mask]).mean() * 100
                    f.write(f"Gap promedio del óptimo: {avg_gap:.2f}%\n")
        
        # Guardar el mejor modelo global
        best_agent.save_checkpoint(f"{self.output_dir}/best_model.pt")
        logger.info(f"Entrenamiento completado. Mejor modelo guardado en {self.output_dir}/best_model.pt")
        
        return best_agent
    
    def _generate_problem_visualizations(self, agent: PPOAgent, problem_name: str, env):
        """Genera visualizaciones para un problema específico"""
        plots_dir = os.path.join(self.output_dir, "plots", problem_name)
        os.makedirs(plots_dir, exist_ok=True)
        
        plots = {}
        
        # Visualización de la mejor solución
        if agent.best_schedule:
            plots["schedule"] = env.render_schedule(
                f"Mejor planificación para {problem_name}", 
                agent.best_schedule
            )
        
        # Evolución del makespan
        plots["makespan"] = agent.plot_training_history()
        
        # Si hay historial de makespan para la mejor solución
        if agent.best_makespan_history:
            plots["best_makespan"] = agent.plot_best_solution_makespan()
        
        # Guardar gráficas
        save_plots(plots, directory=plots_dir)
    
    def evaluate_on_test_set(self, agent: Optional[PPOAgent] = None) -> pd.DataFrame:
        """
        Evalúa el agente en los problemas de prueba.
        
        Args:
            agent: Agente PPO a evaluar (si es None, se carga el mejor modelo guardado)
            
        Returns:
            DataFrame con los resultados de evaluación
        """
        if not self.test_problems:
            logger.error("No hay problemas de prueba. Abortando evaluación.")
            return pd.DataFrame()
            
        if agent is None:
            # Cargar el mejor modelo guardado
            model_path = f"{self.output_dir}/best_model.pt"
            if not os.path.exists(model_path):
                logger.error(f"No se encontró un modelo guardado en {model_path}")
                return pd.DataFrame()
                
            # Usar primer problema de test para inicializar el agente
            env = ExperimentFactory.create_env_from_problem(
                self.test_problems[0], 
                self.reward_strategy,
                **self.reward_params
            )
            agent = ExperimentFactory.create_agent(env, **self.agent_params)
            agent.load_checkpoint(model_path)
            logger.info(f"Modelo cargado desde {model_path}")
        
        test_results = []
        test_start_time = time.time()
        
        for i, problem in enumerate(self.test_problems):
            problem_name = problem.get('name', f"test_{i}")
            logger.info(f"Evaluando en problema: {problem_name} ({i+1}/{len(self.test_problems)})")
            
            # Configurar entorno para este problema de prueba
            env = ExperimentFactory.create_env_from_problem(
                problem, 
                self.reward_strategy,
                **self.reward_params
            )
            
            # Transferir el modelo al nuevo entorno
            test_agent = ExperimentFactory.create_agent(env, **self.agent_params)
            test_agent.policy.load_state_dict(agent.policy.state_dict())
            test_agent.value.load_state_dict(agent.value.state_dict())
            
            # Evaluar
            start_time = time.time()
            makespan, schedule, makespan_history = test_agent.evaluate_policy()
            eval_time = time.time() - start_time
            
            # Guardar programación resultante como visualización
            fig = env.render_schedule(f"Solución para {problem_name}")
            plots_dir = os.path.join(self.output_dir, "plots", "test")
            os.makedirs(plots_dir, exist_ok=True)
            fig.savefig(f"{plots_dir}/{problem_name}_schedule.png")
            plt.close(fig)
            
            # Calcular gap si hay valor óptimo
            optimal = problem.get('optimal_makespan')
            if optimal and isinstance(optimal, (int, float)):
                gap = (makespan - optimal) / optimal * 100
            else:
                gap = None
            
            # Guardar resultado
            test_results.append({
                'problem': problem_name,
                'makespan': makespan,
                'evaluation_time': eval_time,
                'optimal': optimal,
                'gap': gap
            })
        
        total_eval_time = time.time() - test_start_time
        
        # Guardar resultados completos
        results_df = pd.DataFrame(test_results)
        results_df.to_csv(f"{self.output_dir}/test_results.csv", index=False)
        
        # Calcular y guardar estadísticas de evaluación
        with open(f"{self.output_dir}/test_stats.txt", 'w') as f:
            f.write(f"Total problemas evaluados: {len(self.test_problems)}\n")
            f.write(f"Tiempo total de evaluación: {total_eval_time:.2f} segundos\n")
            f.write(f"Makespan promedio: {results_df['makespan'].mean():.2f}\n")
            
            # Calcular gap promedio para problemas con óptimo conocido
            if 'gap' in results_df.columns:
                valid_gaps = results_df['gap'].dropna()
                if len(valid_gaps) > 0:
                    f.write(f"Gap promedio del óptimo: {valid_gaps.mean():.2f}%\n")
                    f.write(f"Gap mínimo: {valid_gaps.min():.2f}%\n")
                    f.write(f"Gap máximo: {valid_gaps.max():.2f}%\n")
        
        # Crear gráfico comparativo
        self._create_comparison_chart(results_df)
        
        logger.info(f"Evaluación completada. Resultados guardados en {self.output_dir}/test_results.csv")
        return results_df
    
    def _create_comparison_chart(self, results_df: pd.DataFrame):
        """Crea un gráfico comparativo de resultados de evaluación"""
        if 'gap' not in results_df.columns or results_df['gap'].isna().all():
            return
            
        plt.figure(figsize=(12, 6))
        
        # Ordenar por gap
        sorted_df = results_df.sort_values('gap')
        
        # Crear barras para cada problema
        plt.bar(sorted_df['problem'], sorted_df['gap'])
        plt.axhline(y=sorted_df['gap'].mean(), color='r', linestyle='--', 
                   label=f'Promedio: {sorted_df["gap"].mean():.2f}%')
        
        plt.title('Desviación porcentual del óptimo por problema')
        plt.xlabel('Problema')
        plt.ylabel('Gap (%)')
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()
        
        # Guardar gráfico
        plots_dir = os.path.join(self.output_dir, "plots")
        os.makedirs(plots_dir, exist_ok=True)
        plt.savefig(f"{plots_dir}/test_gaps.png")
        plt.close()
