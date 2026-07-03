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
from jobshop_rl.experiments.factory import EnvironmentFactory, AgentFactory
from jobshop_rl.utils.logging import TrainingLogger
from jobshop_rl.agents.ppo_agent import PPOAgent
from jobshop_rl.utils.visualization import save_plots
from jobshop_rl.utils.path_utils import ensure_dir, join_paths
from jobshop_rl.utils.experiment_config import ExperimentConfig

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
        try:
            self.training_problems = ProblemLoader.load_from_directory(training_dir)
        except Exception as e:
            logger.warning(f"No se pudieron cargar problemas desde {training_dir}: {str(e)}")
            self.training_problems = []
        
        logger.info(f"Cargando problemas de prueba desde: {test_dir}")
        try:
            self.test_problems = ProblemLoader.load_from_directory(test_dir)
        except Exception as e:
            logger.warning(f"No se pudieron cargar problemas desde {test_dir}: {str(e)}")
            self.test_problems = []
        
        self.output_dir = ensure_dir(output_dir)
        self.agent_params = agent_params or {}
        self.reward_strategy = reward_strategy
        self.reward_params = reward_params or {}
        self.seed = seed
        self.experiment_name = None  # Se puede establecer externamente
        self.save_config = True  # Se puede deshabilitar externamente
        
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
        env = EnvironmentFactory.create_from_problem(
            first_problem, 
            self.reward_strategy,
            seed=self.seed,
            **self.reward_params
        )
        
        best_agent = AgentFactory.create_agent(
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
            env = EnvironmentFactory.create_from_problem(
                problem,
                self.reward_strategy,
                seed=self.seed,
                **self.reward_params
            )
            
            # Si no es el primer problema, transferir conocimiento del mejor agente
            if i > 0:
                # CORRECCIÓN: Pasar csv_logger como un parámetro separado, no dentro del diccionario
                # Crear el nuevo agente con los parámetros adecuados
                current_agent = AgentFactory.create_agent(
                    env, 
                    csv_logger=problem_logger,
                    **self.agent_params
                )
                # Transferir los pesos del modelo
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
            makespan, _, _, _ = current_agent.evaluate_policy()
            
            # Asegurar que el directorio de salida existe antes de guardar
            import os
            checkpoint_path = f"{self.output_dir}/{problem_name}_model.pt"
            model_dir = os.path.dirname(checkpoint_path)
            os.makedirs(model_dir, exist_ok=True)
            
            # Guardar checkpoint
            try:
                current_agent.save_checkpoint(checkpoint_path)
            except Exception as e:
                logger.error(f"Error al guardar checkpoint: {str(e)}")
                # Intentar guardar en un directorio de respaldo
                backup_path = f"checkpoints/{problem_name}_model.pt"
                os.makedirs("checkpoints", exist_ok=True)
                current_agent.save_checkpoint(backup_path)
                logger.info(f"Checkpoint guardado en ruta alternativa: {backup_path}")
            
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
        plots_dir = ensure_dir(join_paths(self.output_dir, "plots", problem_name))
        
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
    
    def evaluate_on_test_set(self, agent: Optional[PPOAgent] = None, use_ortools: bool = False) -> pd.DataFrame:
        """
        Evalúa el agente en los problemas de prueba.
        
        Args:
            agent: Agente PPO a evaluar (si es None, se carga el mejor modelo guardado)
            use_ortools: Si se debe incluir comparación con OR-Tools
            
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
            env = EnvironmentFactory.create_from_problem(
                self.test_problems[0], 
                self.reward_strategy,
                **self.reward_params
            )
            agent = AgentFactory.create_agent(env, **self.agent_params)
            agent.load_checkpoint(model_path)
            logger.info(f"Modelo cargado desde {model_path}")
        
        test_results = []
        test_start_time = time.time()
        
        for i, problem in enumerate(self.test_problems):
            # Obtener el nombre real del problema
            problem_name = problem.get('name', f"test_{i}")
            # Si el nombre no está definido, intentar extraerlo de problem_id
            if problem_name.startswith("test_") and 'problem_id' in problem:
                problem_name = problem['problem_id']
            logger.info(f"Evaluando en problema: {problem_name} ({i+1}/{len(self.test_problems)})")
            
            # Configurar entorno para este problema de prueba
            env = EnvironmentFactory.create_from_problem(
                problem, 
                self.reward_strategy,
                **self.reward_params
            )
            
            # Transferir el modelo al nuevo entorno
            test_agent = AgentFactory.create_agent(env, **self.agent_params)
            
            # Cargar el mejor modelo guardado durante el entrenamiento
            if hasattr(agent, 'best_model_state') and agent.best_model_state:
                test_agent.policy.load_state_dict(agent.best_model_state["policy"])
                test_agent.value.load_state_dict(agent.best_model_state["value"])
            else:
                test_agent.policy.load_state_dict(agent.policy.state_dict())
                test_agent.value.load_state_dict(agent.value.state_dict())
            
            # Evaluar con inferencia best-of-N: la política es estocástica y
            # su mejor muestreo supera con claridad a un único rollout greedy
            start_time = time.time()
            makespan, schedule, makespan_history, _ = test_agent.evaluate_policy(n_samples=64)
            eval_time = time.time() - start_time
            
            # Evaluar heurísticas para comparación
            if use_ortools:
                logger.info(f"Evaluando heurísticas y OR-Tools para comparación...")
                from jobshop_rl.experiments.evaluator import HeuristicEvaluator
                heuristic_evaluator = HeuristicEvaluator(env)
                heuristic_results, execution_times = heuristic_evaluator.evaluate_all(return_times=True, use_ortools=True)
                comparison = heuristic_evaluator.compare_with_agent(makespan)
                logger.info(f"Comparación con heurísticas: {comparison}")
            else:
                heuristic_results = None
                execution_times = None
                comparison = None
            
            # Guardar programación resultante como visualización
            fig = env.render_schedule(f"Solución para {problem_name}")
            plots_dir = ensure_dir(join_paths(self.output_dir, "plots", "test"))
            fig.savefig(join_paths(plots_dir, f"{problem_name}_schedule.png"))
            plt.close(fig)
            
            # Calcular gap si hay valor óptimo
            optimal = problem.get('optimal_makespan')
            if optimal and isinstance(optimal, (int, float)):
                gap = (makespan - optimal) / optimal * 100
            else:
                gap = None
            
            # Límite inferior teórico del problema (peor caso si es intervalo)
            lower_bound = None
            if hasattr(env, 'problem_analysis') and env.problem_analysis:
                lower_bound = env.problem_analysis.get('best_lower_bound')
                if lower_bound is not None and hasattr(lower_bound, 'upper'):
                    lower_bound = float(lower_bound.upper)

            # Preparar resultado
            result = {
                'problem': problem_name,
                'makespan': makespan,
                'evaluation_time': eval_time,
                'optimal': optimal,
                'gap': gap,
                'lower_bound': lower_bound
            }
            
            # Añadir el orden de las tareas (schedule) al resultado
            if schedule:
                try:
                    # Ordenar el schedule por tiempo de inicio
                    sorted_schedule = sorted(schedule, key=lambda x: x.get('start', 0) if not hasattr(x.get('start', 0), 'lower') else x.get('start', 0).lower)
                    
                    # Crear una representación del orden de tareas como string para el CSV
                    task_order = []
                    for task in sorted_schedule:
                        # Usar get() para acceder a las claves con valores por defecto si no existen
                        job_id = task.get('job', '?')
                        # La clave puede ser 'task' o 'operation' dependiendo de la implementación
                        op_id = task.get('task', task.get('operation', '?'))
                        machine = task.get('machine', '?')
                        start = task.get('start', '?')
                        end = task.get('end', '?')
                        
                        # Convertir intervalos a string para el CSV
                        if hasattr(start, 'lower'):
                            start_str = f"[{start.lower},{start.upper}]"
                        else:
                            start_str = str(start)
                        
                        if hasattr(end, 'lower'):
                            end_str = f"[{end.lower},{end.upper}]"
                        else:
                            end_str = str(end)
                            
                        task_order.append(f"(J{job_id}-O{op_id}-M{machine}:{start_str}-{end_str})")
                    
                    result['task_order'] = ",".join(task_order)
                    
                    # Convertir schedule a formato JSON-serializable
                    json_schedule = []
                    for task in schedule:
                        json_task = {}
                        for key, value in task.items():
                            if hasattr(value, 'lower'):
                                # Es un Interval - convertir a dict
                                json_task[key] = {
                                    'lower': float(value.lower),
                                    'upper': float(value.upper)
                                }
                            else:
                                # Valor normal
                                json_task[key] = value
                        json_schedule.append(json_task)
                    
                    # Guardar el archivo JSON con la planificación completa
                    import json
                    schedule_file = os.path.join(plots_dir, f"{problem_name}_schedule.json")
                    with open(schedule_file, 'w') as f:
                        json.dump(json_schedule, f, indent=2)
                except Exception as e:
                    # Si hay algún error, registrarlo pero continuar con la evaluación
                    logger.error(f"Error al procesar el orden de tareas: {str(e)}")
                    import traceback
                    logger.error(traceback.format_exc())
                    # Guardar el schedule como está, sin procesamiento
                    result['task_order'] = "Error al procesar el orden de tareas"
            
            # Añadir resultados de heurísticas si están disponibles
            if heuristic_results:
                result['heuristic_results'] = heuristic_results
                result['heuristic_times'] = execution_times
                result['comparison'] = comparison
                
                # Si OR-Tools está disponible, añadir comparación específica
                if 'OR-Tools' in heuristic_results:
                    ortools_makespan = heuristic_results['OR-Tools']
                    ortools_time = execution_times.get('OR-Tools', 0)
                    gap_vs_ortools = ((makespan - ortools_makespan) / ortools_makespan) * 100 if ortools_makespan > 0 else 0
                    result['ortools_makespan'] = ortools_makespan
                    result['ortools_time'] = ortools_time
                    result['ortools_gap'] = gap_vs_ortools
            
            test_results.append(result)
        
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
            
            # Añadir estadísticas de comparación con heurísticas
            if any('heuristic_results' in result for result in test_results):
                f.write("\n===== Comparación con heurísticas =====\n")
                
                # Calcular promedios de comparación para cada heurística
                heuristic_types = set()
                for result in test_results:
                    if 'comparison' in result:
                        heuristic_types.update(result['comparison'].keys())
                
                for heuristic in sorted(heuristic_types):
                    comparisons = [result['comparison'][heuristic] for result in test_results 
                                  if 'comparison' in result and heuristic in result['comparison']]
                    if comparisons:
                        avg_comparison = sum(comparisons) / len(comparisons)
                        f.write(f"vs {heuristic}: {avg_comparison:.2f}% de mejora promedio\n")
                
                # Añadir estadísticas específicas de OR-Tools
                if any('ortools_gap' in result for result in test_results):
                    f.write("\n===== Comparación con OR-Tools =====\n")
                    ortools_gaps = [result['ortools_gap'] for result in test_results if 'ortools_gap' in result]
                    if ortools_gaps:
                        avg_ortools_gap = sum(ortools_gaps) / len(ortools_gaps)
                        f.write(f"Gap promedio vs OR-Tools: {avg_ortools_gap:.2f}%\n")
                        
                        # Contar cuántas veces el modelo fue mejor o igual que OR-Tools
                        better_count = sum(1 for gap in ortools_gaps if gap <= 0)
                        f.write(f"El modelo fue mejor o igual que OR-Tools en {better_count}/{len(ortools_gaps)} casos\n")
        
        # Crear gráfico comparativo
        self._create_comparison_chart(results_df)
        
        # Crear gráfico comparativo con heurísticas si hay datos
        if any('heuristic_results' in result for result in test_results):
            self._create_heuristic_comparison_chart(test_results)
        
        logger.info(f"Evaluación completada. Resultados guardados en {self.output_dir}/test_results.csv")
        return results_df
    
    def _create_heuristic_comparison_chart(self, test_results):
        """
        Crea un gráfico de barras comparando el agente RL con las heurísticas.

        Todos los valores se muestran como escalares (peor caso / límite
        superior para problemas con intervalos, que es el criterio con el que
        se evalúan RL y heurísticas). Incluye el límite inferior teórico del
        problema como línea de referencia.
        """
        if not test_results:
            return

        # Verificar si hay resultados de heurísticas
        if not any('heuristic_results' in result for result in test_results):
            return

        from jobshop_rl.models.interval import Interval
        from matplotlib.patches import Patch
        from matplotlib.lines import Line2D

        def to_scalar(value):
            """Escalar de peor caso: upper para intervalos, el valor si no"""
            return float(value.upper) if isinstance(value, Interval) else float(value)

        # Crear un gráfico de barras para cada problema
        for result in test_results:
            if 'heuristic_results' not in result:
                continue

            problem_name = result['problem']
            makespan = result['makespan']
            heuristic_results = result['heuristic_results']
            lower_bound = result.get('lower_bound')

            # Detectar si el problema usa intervalos (basándose en el nombre del problema)
            is_interval_problem = 'INTERVAL' in problem_name.upper() or '_interval' in problem_name.lower()

            # Si es un problema con intervalos, excluir OR-Tools
            if is_interval_problem and 'OR-Tools' in heuristic_results:
                heuristic_results = {k: v for k, v in heuristic_results.items() if k != 'OR-Tools'}
                logger.info(f"Excluyendo OR-Tools del gráfico de comparación para {problem_name} (problema con intervalos)")

            # Preparar datos: todos los métodos como barras escalares
            methods = ['RL'] + list(heuristic_results.keys())
            values = [to_scalar(makespan)] + [to_scalar(v) for v in heuristic_results.values()]

            # Colores por tipo de método
            colors = []
            for method in methods:
                if method == 'RL':
                    colors.append('seagreen')
                elif method == 'OR-Tools':
                    colors.append('indianred')
                elif method.startswith('Random'):
                    colors.append('sandybrown')
                else:
                    colors.append('steelblue')

            plt.figure(figsize=(14, 7))
            bars = plt.bar(methods, values, color=colors, edgecolor='black', linewidth=0.6)

            # Etiquetas de valores encima de las barras
            for bar, value in zip(bars, values):
                plt.text(bar.get_x() + bar.get_width() / 2., bar.get_height(),
                         f'{value:.0f}', ha='center', va='bottom',
                         fontsize=10, fontweight='bold')

            # Línea de referencia con el límite inferior teórico del problema
            if lower_bound is not None and lower_bound > 0:
                plt.axhline(y=lower_bound, color='crimson', linestyle='--', linewidth=1.5, zorder=0)

            # Leyenda explícita
            legend_elements = [
                Patch(facecolor='seagreen', edgecolor='black', label='Agente RL'),
                Patch(facecolor='steelblue', edgecolor='black', label='Heurísticas'),
                Patch(facecolor='sandybrown', edgecolor='black', label='Random (250 soluciones)'),
            ]
            if 'OR-Tools' in heuristic_results:
                legend_elements.append(Patch(facecolor='indianred', edgecolor='black', label='OR-Tools'))
            if lower_bound is not None and lower_bound > 0:
                legend_elements.append(Line2D([0], [0], color='crimson', linestyle='--', linewidth=1.5,
                                              label=f'Límite inferior teórico: {lower_bound:.0f}'))
            plt.legend(handles=legend_elements, loc='upper left', framealpha=0.9)

            # Dejar espacio para las etiquetas de valor
            plt.ylim(0, max(values) * 1.12)

            plt.xticks(rotation=45, ha='right')
            plt.title(f'Comparación de Makespan para {problem_name}', fontsize=14, fontweight='bold')
            plt.xlabel('Método', fontsize=12)
            ylabel = 'Makespan (peor caso)' if is_interval_problem else 'Makespan'
            plt.ylabel(ylabel, fontsize=12)
            plt.grid(axis='y', alpha=0.3, linestyle='--')
            plt.tight_layout()

            # Guardar gráfico
            plots_dir = ensure_dir(join_paths(self.output_dir, "plots", "comparisons"))
            plt.savefig(join_paths(plots_dir, f"{problem_name}_comparison.png"), dpi=150)
            plt.close()
    
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
        plots_dir = ensure_dir(join_paths(self.output_dir, "plots"))
        plt.savefig(join_paths(plots_dir, "test_gaps.png"))
        plt.close()
    
    def save_batch_config(self):
        """Guarda la configuración del experimento por lotes usando ExperimentConfig.save_config()"""
        if not self.save_config:
            logger.info("Guardado de configuración deshabilitado para este experimento")
            return
            
        import datetime
        
        logger.info(f"Guardando configuración: {len(self.training_problems)} problemas de entrenamiento, {len(self.test_problems)} problemas de test")
        
        # Generar nombre de experimento PRIMERO
        if self.experiment_name:
            experiment_name = self.experiment_name
        else:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            experiment_name = f"batch_experiment_{timestamp}"
        
        # Para capturar parámetros adaptive, necesitamos crear un entorno de ejemplo
        sample_env = None
        final_config = {}
        
        if self.training_problems and self.reward_strategy.lower() == "adaptive":
            try:
                # Crear entorno con el primer problema para obtener parámetros adaptive
                sample_problem = self.training_problems[0]
                sample_env = EnvironmentFactory.create_from_problem(
                    sample_problem,
                    self.reward_strategy,
                    seed=self.seed,
                    **self.reward_params
                )
                
                # Crear agente de ejemplo para obtener parámetros finales
                sample_agent = AgentFactory.create_agent(sample_env, **self.agent_params)
                
                # Usar el método de extracción completa
                from jobshop_rl.experiments.factory import ExperimentFactory
                final_config = ExperimentFactory._extract_complete_configuration(
                    sample_env, sample_agent, experiment_name, 0, self.reward_strategy, 
                    sample_problem.get('problem_id', 'batch_sample'), self.seed, 
                    False, False, False
                )
                
                logger.info("Parámetros adaptive completos capturados del primer problema de entrenamiento")
                
            except Exception as e:
                logger.warning(f"No se pudieron capturar parámetros adaptive completos: {str(e)}")
                # Usar configuración básica como fallback
                final_config = self._create_basic_config()
        else:
            # No es adaptive o no hay problemas, usar configuración básica
            final_config = self._create_basic_config()
        
        # Sobrescribir metadatos específicos del batch
        final_config.update({
            'experiment_type': 'batch',
            'experiment_name': experiment_name,
            'reward_strategy': self.reward_strategy,
            'seed': self.seed,
            'training_problems_count': len(self.training_problems),
            'test_problems_count': len(self.test_problems),
            'output_dir': self.output_dir,
            'adaptive_modifications_applied': self.reward_strategy.lower() == "adaptive"
        })
        
        # Añadir lista de problemas de entrenamiento
        training_problem_names = []
        for problem in self.training_problems:
            name = problem.get('name') or problem.get('problem_id') or 'unknown'
            training_problem_names.append(name)
        final_config['training_problems'] = training_problem_names
        
        # Añadir lista de problemas de test
        test_problem_names = []
        for problem in self.test_problems:
            name = problem.get('name') or problem.get('problem_id') or 'unknown'
            test_problem_names.append(name)
        final_config['test_problems'] = test_problem_names
        
        # Usar directamente ExperimentConfig.save_config()
        try:
            config_path = ExperimentConfig.save_config(
                final_config, 
                experiment_name=experiment_name,
                output_dir=os.path.join(self.output_dir, "configs")
            )
            logger.info(f"Configuración completa del experimento por lotes guardada en: {config_path}")
        except Exception as e:
            logger.error(f"Error al guardar configuración: {str(e)}")
            # Intentar guardar en directorio alternativo
            try:
                config_path = ExperimentConfig.save_config(
                    final_config, 
                    experiment_name=experiment_name,
                    output_dir="outputs/configs"
                )
                logger.info(f"Configuración guardada en directorio alternativo: {config_path}")
            except Exception as e2:
                logger.error(f"Error al guardar en directorio alternativo: {str(e2)}")
    
    def _create_basic_config(self):
        """Crea configuración básica cuando no se pueden capturar parámetros adaptive."""
        return {
            'experiment_type': 'batch',
            'reward_strategy': self.reward_strategy,
            'seed': self.seed,
            'agent_params': self.agent_params,
            'reward_params': self.reward_params,
            'note': 'Configuración básica - no se pudieron capturar parámetros adaptive'
        }
