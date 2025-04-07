"""
Script para evaluar un modelo entrenado con el problema ABZ10.
"""

import os
import logging
import argparse
import time
import matplotlib.pyplot as plt
from typing import Dict, Any, Optional

from jobshop_rl.data.abz10 import get_abz10_problem
from jobshop_rl.environment.job_shop_env import JobShopEnv
from jobshop_rl.agents.ppo_agent import PPOAgent
from jobshop_rl.rewards.strategies import RewardStrategyFactory
from jobshop_rl.experiments.evaluator import HeuristicEvaluator
from jobshop_rl.utils.path_utils import get_checkpoint_path, get_plots_dir

logger = logging.getLogger("JobShopRL.EvaluateABZ10")

def setup_logging(log_level):
    """Configura el sistema de logging"""
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Nivel de log inválido: {log_level}')
    
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def parse_args():
    """Configura y parsea los argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(description='Evaluación con ABZ10 para JobShopRL')
    
    # Parámetros para la evaluación
    parser.add_argument('--model-path', type=str, default='best_model.pt',
                       help='Ruta al archivo del modelo entrenado (relativa a outputs/checkpoints)')
    parser.add_argument('--reward', type=str, default='advanced',
                       help='Estrategia de recompensa: basic, advanced o combined')
    parser.add_argument('--seed', type=int, default=None,
                       help='Semilla para reproducibilidad')
    parser.add_argument('--visualize', action='store_true',
                       help='Generar visualizaciones')
    parser.add_argument('--save-plot', action='store_true',
                       help='Guardar diagrama de Gantt en archivo')
    parser.add_argument('--plot-prefix', type=str, default='abz10_evaluation',
                       help='Prefijo para el nombre del archivo de visualización')
    parser.add_argument('--log-level', type=str, default='INFO',
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                       help='Nivel de logging')
    
    return parser.parse_args()

def evaluate_abz10(args):
    """Evalúa un modelo entrenado con el problema ABZ10"""
    # Obtener datos del problema ABZ10
    abz10_data = get_abz10_problem()
    
    # Configurar la estrategia de recompensa
    reward_strategy = RewardStrategyFactory.create_strategy(args.reward)
    
    # Crear el entorno ABZ10
    env = JobShopEnv(
        num_jobs=abz10_data['num_jobs'],
        num_machines=abz10_data['num_machines'],
        sequences=abz10_data['sequences'],
        durations=abz10_data['durations'],
        reward_strategy=reward_strategy,
        seed=args.seed
    )
    
    # Crear un agente y cargar el modelo
    agent = PPOAgent(env)
    
    # Construir la ruta completa al modelo
    model_path = get_checkpoint_path(args.model_path)
    logger.info(f"Cargando modelo desde: {model_path}")
    
    # Cargar el modelo
    agent.load_checkpoint(model_path)
    
    # Evaluar en ABZ10 y medir tiempo
    logger.info("Evaluando modelo en ABZ10...")
    makespan, schedule, makespan_history, rl_execution_time = agent.evaluate_policy()
    
    # Comparar con heurísticas
    logger.info("Comparando con heurísticas clásicas en ABZ10...")
    evaluator = HeuristicEvaluator(env)
    heuristic_results, execution_times = evaluator.evaluate_all()
    comparison = evaluator.compare_with_agent(makespan)
    
    # Registrar resultados
    logger.info("=== Resultados de la evaluación en ABZ10 ===")
    logger.info(f"Makespan ABZ10 (RL): {makespan}, Tiempo: {rl_execution_time:.4f} segundos")
    
    # Mostrar resultados de heurísticas
    logger.info("Comparación con heurísticas:")
    for heuristic, heur_makespan in heuristic_results.items():
        exec_time = execution_times[heuristic]
        logger.info(f"{heuristic}: Makespan = {heur_makespan}, Tiempo: {exec_time:.4f} segundos")
        
    logger.info("Mejora porcentual en makespan:")
    for heuristic, improvement in comparison.items():
        logger.info(f"vs {heuristic}: {improvement:.2f}%")
    
    # Ordenar las operaciones por tiempo de inicio
    sorted_schedule = sorted(schedule, key=lambda x: x['start'])
    
    # Mostrar el orden de tareas en el log
    logger.info("Orden de tareas de la planificación:")
    for i, op in enumerate(sorted_schedule):
        logger.info(f"{i+1}. Job {op['job']}, Operación {op['operation']}, Máquina {op['machine']}, Inicio: {op['start']}, Fin: {op['end']}")
    
    # Generar visualización si está habilitado
    if args.visualize:
        logger.info("Generando diagrama de Gantt...")
        gantt = env.render_schedule(f"Planificación ABZ10 (Makespan: {makespan})", schedule)
        plt.tight_layout()
        
        # Guardar visualización si está habilitado
        if args.save_plot:
            plots_dir = get_plots_dir()
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            plot_path = os.path.join(plots_dir, f"{args.plot_prefix}_{timestamp}.png")
            gantt.savefig(plot_path)
            logger.info(f"Diagrama de Gantt guardado en: {plot_path}")
            
        # Mostrar visualización
        plt.show()
        
    return {
        'makespan': makespan,
        'schedule': schedule,
        'makespan_history': makespan_history,
        'execution_time': rl_execution_time,
        'heuristic_results': heuristic_results,
        'heuristic_times': execution_times,
        'comparison': comparison
    }

def main():
    """Función principal"""
    args = parse_args()
    setup_logging(args.log_level)
    
    print(f"JobShopRL - Evaluación con ABZ10")
    print(f"Cargando modelo desde: {args.model_path}")
    
    results = evaluate_abz10(args)
    
    print(f"\n===== Resultados de ABZ10 =====")
    print(f"Makespan (RL): {results['makespan']}, Tiempo: {results['execution_time']:.4f} segundos")
    
    # Mostrar comparación con heurísticas
    if 'heuristic_results' in results and 'heuristic_times' in results:
        print("\nComparación con heurísticas:")
        print(f"{'Heurística':<10} {'Makespan':<10} {'Tiempo (s)':<12} {'vs RL (%)':<10}")
        print("-" * 45)
        
        for heuristic, makespan in results['heuristic_results'].items():
            time_value = results['heuristic_times'][heuristic]
            improvement = results['comparison'][heuristic]
            print(f"{heuristic:<10} {makespan:<10} {time_value:.6f}s{'':5} {improvement:.2f}%")
    
    print("\nLa planificación detallada y el orden de tareas se pueden ver en el log.")
    if args.save_plot:
        print(f"El diagrama de Gantt se ha guardado en el directorio de plots.")

if __name__ == "__main__":
    main()