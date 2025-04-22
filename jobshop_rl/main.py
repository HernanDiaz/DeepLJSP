"""
Punto de entrada principal para el sistema JobShopRL.
"""

import os
import argparse
import logging
import time
import pandas as pd
from typing import Dict, Any, Optional

from jobshop_rl.experiments.factory import ExperimentFactory
from jobshop_rl.experiments.batch_experimenter import BatchExperimenter
from jobshop_rl.data.problem_loader import ProblemLoader
from jobshop_rl.utils.logging import TrainingLogger
from jobshop_rl.utils.path_utils import (
    ensure_dir, get_output_dir, get_checkpoint_path, 
    get_plots_dir, join_paths, DEFAULT_OUTPUT_DIR
)
from jobshop_rl.utils.problem_analyzer import AdaptiveConfigGenerator

def parse_args():
    """Configura y parsea los argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(description='Sistema de RL para Job Shop Scheduling')
    
    # Modo de ejecución
    parser.add_argument('--mode', type=str, default='single', choices=['single', 'batch', 'generate'],
                        help='Modo de ejecución: single (un problema), batch (múltiples problemas) o generate (generar problemas)')
    
    # Parámetros para modo single
    parser.add_argument('--episodes', type=int, default=300,
                       help='Número de episodios para entrenar (modo single)')
    parser.add_argument('--reward', type=str, default='adaptive', 
                       choices=['basic', 'advanced', 'adaptive', 'combined'],
                       help='Estrategia de recompensa')
    parser.add_argument('--visualize', action='store_true',
                       help='Generar visualizaciones')
    parser.add_argument('--save-plots', action='store_true',
                       help='Guardar visualizaciones en archivos')
    parser.add_argument('--train-problem', type=str, default='ft10',
                       help='ID del problema para entrenamiento (p.ej. ft10) o lista separada por comas (p.ej. ft10,ft20,abz7)')
    parser.add_argument('--eval-problem', type=str, default=None,
                       help='ID del problema para evaluación o lista separada por comas (p.ej. abz8,abz9)')
    parser.add_argument('--use-ortools', action='store_true',
                       help='Comparar con solucionador de Google OR-Tools')
    parser.add_argument('--ortools-time-limit', type=int, default=60,
                       help='Límite de tiempo (segundos) para el solucionador OR-Tools')
    
    # Parámetros para modo batch
    parser.add_argument('--training-dir', type=str, default='./data/training_problems',
                       help='Directorio con problemas de entrenamiento (modo batch)')
    parser.add_argument('--test-dir', type=str, default='./data/test_problems',
                       help='Directorio con problemas de prueba (modo batch)')
    parser.add_argument('--output-dir', type=str, default='outputs/results',
                       help='Directorio para guardar resultados (modo batch)')
    parser.add_argument('--episodes-per-problem', type=int, default=100,
                       help='Episodios para entrenar en cada problema (modo batch)')
    
    # Parámetros para modo generate
    parser.add_argument('--num-problems', type=int, default=5,
                       help='Número de problemas a generar (modo generate)')
    parser.add_argument('--num-jobs', type=int, default=10,
                       help='Número de trabajos por problema (modo generate)')
    parser.add_argument('--num-machines', type=int, default=10,
                       help='Número de máquinas por problema (modo generate)')
    parser.add_argument('--output-format', type=str, default='json', choices=['json', 'csv', 'taillard'],
                       help='Formato para guardar problemas generados (modo generate)')
    
    # Parámetros comunes
    parser.add_argument('--seed', type=int, default=None,
                       help='Semilla para reproducibilidad')
    parser.add_argument('--log-level', type=str, default='INFO',
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                       help='Nivel de logging')
    parser.add_argument('--csv-logging', action='store_true',
                       help='Habilitar logging de métricas en CSV')
    parser.add_argument('--csv-file', type=str, default=None,
                       help='Nombre del archivo CSV para logging de métricas')
    parser.add_argument('--experiment-name', type=str, default=None,
                       help='Nombre del experimento (para identificación y reproducibilidad)')
    
    return parser.parse_args()

def setup_logging(log_level):
    """Configura el sistema de logging"""
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Nivel de log inválido: {log_level}')
    
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def run_single_experiment(args):
    """Ejecuta un experimento con un único problema"""
    # Obtener el directorio de salida estandarizado
    output_dir = get_output_dir()
    
    # Verificar si se proporcionó una lista de problemas separados por comas
    if ',' in args.train_problem:
        logging.info(f"Se detectó una lista de problemas: {args.train_problem}")
        logging.info("Ejecutando en modo batch para procesar múltiples problemas...")
        return run_batch_experiment(args)
    
    # Cargar el problema especificado
    problem_id = args.train_problem.lower()
    
    # Los parámetros de recompensa serán configurados automáticamente por el analizador de problemas
    # basado en las características del problema, pero se pueden proporcionar valores por defecto
    reward_params = {
        "makespan_weight": 1.0,
        "idle_weight": 0.2,
        "critical_weight": 0.1,
        "balance_weight": 0.05,
        "progress_weight": 0.2,
        "local_improvement_weight": 0.15
    }
    
    # Los parámetros del agente también se pueden adaptar automáticamente, 
    # pero proporcionamos valores por defecto
    agent_params = {
        "lr": 0.0003,
        "gamma": 0.99,
        "entropy_coef": 0.02,
        "K_epochs": 4,
        "use_lr_decay": True,
        "use_grad_clip": True,
        "advantage_normalization": True,
        "gae_lambda": 0.95,
        "seed": args.seed
    }
    
    start_time = time.time()
    
    # Determinar si se debe realizar evaluación
    evaluate_other_problem = args.eval_problem is not None
    
    agent, results = ExperimentFactory.run_full_experiment(
        episodes=args.episodes,
        reward_strategy=args.reward,
        agent_params=agent_params,
        reward_params=reward_params,
        problem_id=problem_id,
        seed=args.seed,
        visualize=args.visualize,
        save_plots=args.save_plots,
        csv_logging=args.csv_logging,
        csv_filename=args.csv_file,
        csv_base_dir=output_dir,
        output_dir=output_dir,
        experiment_name=args.experiment_name,
        evaluate_other_problem=evaluate_other_problem,
        evaluation_problem_id=args.eval_problem,
        use_ortools=args.use_ortools,
        ortools_time_limit=args.ortools_time_limit
    )
    
    total_time = time.time() - start_time
    
    print(f"\n===== Resultados del experimento =====")
    print(f"Problema de entrenamiento: {problem_id}")
    print(f"Tiempo total: {total_time:.2f} segundos")
    print(f"Mejor makespan: {agent.best_makespan}")
    # Usar el makespan del último episodio de entrenamiento en lugar de una nueva evaluación
    last_makespan = agent.training_makespan_history[-1] if agent.training_makespan_history else float('inf')
    print(f"Makespan final: {last_makespan}")
    
    # Si tenemos el análisis del problema, mostrar información sobre los límites
    if hasattr(agent, 'env') and hasattr(agent.env, 'problem_analysis'):
        problem_analysis = agent.env.problem_analysis
        best_lower_bound = problem_analysis.get('best_lower_bound', 0)
        if best_lower_bound > 0:
            gap = ((agent.best_makespan - best_lower_bound) / best_lower_bound) * 100
            print(f"Mejor límite inferior: {best_lower_bound}")
            print(f"Gap respecto al límite: {gap:.2f}%")
            
        # Mostrar información sobre los límites individuales
        if 'lower_bounds' in problem_analysis:
            print("\nLímites inferiores calculados:")
            for bound_name, bound_value in problem_analysis['lower_bounds'].items():
                print(f"  {bound_name}: {bound_value}")
    
    # Mostrar resultados de OR-Tools si están disponibles
    if 'ortools_results' in results and results['ortools_results']:
        ortools_data = results['ortools_results']
        print("\n===== Resultados de Google OR-Tools =====")
        print(f"Makespan con OR-Tools: {ortools_data['makespan']}")
        print(f"Tiempo de ejecución: {ortools_data['execution_time']:.2f} segundos")
        print(f"Gap respecto a OR-Tools: {ortools_data['gap']:.2f}%")
        
        # Si el agente obtuvo un makespan mejor o igual que OR-Tools
        if agent.best_makespan <= ortools_data['makespan']:
            print(f"\n¡FELICIDADES! El agente RL encontró una solución mejor o igual que OR-Tools!")
        else:
            improvement_needed = ((agent.best_makespan - ortools_data['makespan']) / agent.best_makespan) * 100
            print(f"\nEl agente RL necesita mejorar un {improvement_needed:.2f}% para igualar a OR-Tools.")
            
    # Mostrar resultados de evaluación si están disponibles
    if 'evaluation_results' in results and results['evaluation_results']:
        eval_data = results['evaluation_results']
        print(f"\n===== Resultados de evaluación en {eval_data['problem_id']} =====")
        print(f"Makespan: {eval_data['makespan']}")
        print(f"Tiempo de ejecución: {eval_data['execution_time']:.2f} segundos")
        
        if 'heuristic_results' in eval_data:
            print("\nComparación con heurísticas:")
            for heuristic, makespan in eval_data['heuristic_results'].items():
                if heuristic in eval_data['comparison']:
                    improvement = eval_data['comparison'][heuristic]
                    print(f"  vs {heuristic}: Makespan = {makespan}, Mejora = {improvement:.2f}%")
    
    if 'comparison' in results:
        print("\nComparación con heurísticas:")
        for heuristic, improvement in results['comparison'].items():
            print(f"  vs {heuristic}: {improvement:.2f}% de mejora")
            
    return agent, results

def run_batch_experiment(args):
    """Ejecuta un experimento por lotes con múltiples problemas"""
    # Obtener el directorio de salida estandarizado para experimentos por lotes
    batch_output_dir = get_output_dir([os.path.basename(args.output_dir)])
    
    # Los parámetros de recompensa se configurarán dinámicamente por problema
    reward_params = {
        "makespan_weight": 1.0,
        "idle_weight": 0.2,
        "critical_weight": 0.1,
        "balance_weight": 0.05,
        "progress_weight": 0.2,
        "local_improvement_weight": 0.15
    }
    
    # Los parámetros del agente también se pueden adaptar automáticamente
    agent_params = {
        "lr": 0.0003,
        "gamma": 0.99,
        "entropy_coef": 0.02,
        "K_epochs": 4,
        "use_lr_decay": True,
        "use_grad_clip": True,
        "advantage_normalization": True,
        "gae_lambda": 0.95
    }
    
    # Verificar si hay IDs de problemas específicos para usar
    training_problems = []
    test_problems = []
    
    # Cargar problemas por IDs si se proporcionaron
    if ',' in args.train_problem:
        # Lista de IDs de problemas separados por comas
        train_problem_ids = [p.strip() for p in args.train_problem.split(',')]
        
        from jobshop_rl.data import PROBLEM_REGISTRY
        logging.info(f"Cargando problemas de entrenamiento por ID: {train_problem_ids}")
        
        for problem_id in train_problem_ids:
            if problem_id in PROBLEM_REGISTRY:
                try:
                    problem_data = PROBLEM_REGISTRY[problem_id]()
                    training_problems.append(problem_data)
                    logging.info(f"Problema {problem_id} cargado correctamente")
                except Exception as e:
                    logging.error(f"Error al cargar problema {problem_id}: {str(e)}")
            else:
                logging.error(f"Problema {problem_id} no encontrado en el registro")
                
    # Cargar problemas de evaluación por IDs si se proporcionaron
    if args.eval_problem is not None:
        from jobshop_rl.data import PROBLEM_REGISTRY
        
        # Procesar una lista separada por comas o un solo problema
        if ',' in args.eval_problem:
            # Lista de IDs de problemas separados por comas
            eval_problem_ids = [p.strip() for p in args.eval_problem.split(',')]
            logging.info(f"Cargando problemas de evaluación por ID: {eval_problem_ids}")
            
            for problem_id in eval_problem_ids:
                if problem_id in PROBLEM_REGISTRY:
                    try:
                        problem_data = PROBLEM_REGISTRY[problem_id]()
                        test_problems.append(problem_data)
                        logging.info(f"Problema {problem_id} cargado correctamente")
                    except Exception as e:
                        logging.error(f"Error al cargar problema {problem_id}: {str(e)}")
                else:
                    logging.error(f"Problema {problem_id} no encontrado en el registro")
        else:
            # Un solo problema de evaluación
            problem_id = args.eval_problem.strip()
            logging.info(f"Cargando problema de evaluación: {problem_id}")
            
            if problem_id in PROBLEM_REGISTRY:
                try:
                    problem_data = PROBLEM_REGISTRY[problem_id]()
                    test_problems.append(problem_data)
                    logging.info(f"Problema {problem_id} cargado correctamente")
                except Exception as e:
                    logging.error(f"Error al cargar problema {problem_id}: {str(e)}")
            else:
                logging.error(f"Problema {problem_id} no encontrado en el registro")
    
    # Crear directorios de salida si no existen
    os.makedirs(batch_output_dir, exist_ok=True)
    
    # Configurar experimentador por lotes
    experimenter = BatchExperimenter(
        training_dir=args.training_dir,
        test_dir=args.test_dir,
        output_dir=batch_output_dir,
        agent_params=agent_params,
        reward_strategy=args.reward,
        reward_params=reward_params,
        seed=args.seed
    )
    
    # Si tenemos problemas cargados por ID, sobreescribir los problemas del experimentador
    if training_problems:
        experimenter.training_problems = training_problems
        logging.info(f"Usando {len(training_problems)} problemas específicos para entrenamiento")
    
    if test_problems:
        experimenter.test_problems = test_problems
        logging.info(f"Usando {len(test_problems)} problemas específicos para evaluación")
    
    # Verificar que haya problemas para entrenar
    if not experimenter.training_problems:
        logging.error("No se encontraron problemas de entrenamiento. Abortando.")
        return None
    
    # Determinar el número de episodios para cada problema
    # Si se especificó episodes_per_problem, usar ese valor; de lo contrario, usar episodes
    episodes_to_train = args.episodes_per_problem
    # Si episodes se especificó explícitamente (diferente al valor por defecto de 300), usar ese valor
    if 'episodes' in args and args.episodes != 300:
        episodes_to_train = args.episodes
        logging.info(f"Usando {episodes_to_train} episodios por problema basado en el parámetro --episodes")
    else:
        logging.info(f"Usando {episodes_to_train} episodios por problema basado en el parámetro --episodes-per-problem")
    
    # Entrenar el agente
    start_time = time.time()
    best_agent = experimenter.train_agent(episodes_per_problem=episodes_to_train)
    training_time = time.time() - start_time
    
    if best_agent is None:
        print("No se pudo completar el entrenamiento. Revise los logs para más detalles.")
        return None
    
    # Evaluar en problemas de prueba si existen
    results = pd.DataFrame()
    eval_time = 0
    
    if experimenter.test_problems:
        logging.info(f"Iniciando evaluación con {len(experimenter.test_problems)} problemas de prueba")
        for i, test_problem in enumerate(experimenter.test_problems):
            problem_name = test_problem.get('name', f"problema_test_{i}")
            logging.info(f"Evaluando en el problema de prueba: {problem_name}")
            
        start_time = time.time()
        # Pasamos el parámetro use_ortools al método evaluate_on_test_set
        results = experimenter.evaluate_on_test_set(best_agent, use_ortools=args.use_ortools)
        eval_time = time.time() - start_time
        logging.info(f"Evaluación completada en {eval_time:.2f} segundos")
    else:
        logging.warning("No hay problemas de prueba para evaluación.")
        if args.eval_problem:
            logging.warning(f"El problema de evaluación '{args.eval_problem}' no pudo cargarse correctamente.")
            # Intentar cargar el problema directamente aquí
            try:
                from jobshop_rl.data import PROBLEM_REGISTRY
                if args.eval_problem in PROBLEM_REGISTRY:
                    test_problem = PROBLEM_REGISTRY[args.eval_problem]()
                    experimenter.test_problems = [test_problem]
                    logging.info(f"Se cargó el problema de evaluación '{args.eval_problem}' para un segundo intento de evaluación")
                    
                    start_time = time.time()
                    results = experimenter.evaluate_on_test_set(best_agent)
                    eval_time = time.time() - start_time
                    logging.info(f"Evaluación completada en {eval_time:.2f} segundos")
                else:
                    logging.error(f"El problema '{args.eval_problem}' no existe en el registro PROBLEM_REGISTRY")
                    logging.info(f"Problemas disponibles: {list(PROBLEM_REGISTRY.keys())}")
            except Exception as e:
                logging.error(f"Error al intentar cargar el problema '{args.eval_problem}': {str(e)}")
                import traceback
                logging.error(traceback.format_exc())
    
    # Mostrar resumen
    print(f"\n===== Resultados del experimento por lotes =====")
    print(f"Tiempo total de entrenamiento: {training_time:.2f} segundos")
    print(f"Problemas entrenados: {len(experimenter.training_problems)}")
    
    if experimenter.test_problems:
        print(f"Tiempo total de evaluación: {eval_time:.2f} segundos")
        print(f"Problemas evaluados: {len(experimenter.test_problems)}")
        
        if not results.empty:
            print(f"\nResumen de evaluación:")
            print(f"  Makespan promedio: {results['makespan'].mean():.2f}")
            
            # Calcular gap promedio para problemas con óptimo conocido o límite inferior
            if 'gap' in results.columns:
                valid_gaps = results['gap'].dropna()
                if len(valid_gaps) > 0:
                    print(f"  Gap promedio: {valid_gaps.mean():.2f}%")
                    print(f"  Gap mínimo: {valid_gaps.min():.2f}%")
                    print(f"  Gap máximo: {valid_gaps.max():.2f}%")
    
    print(f"\nResultados completos guardados en: {batch_output_dir}")
    
    return best_agent, results

def generate_problems(args):
    """Genera problemas aleatorios y los guarda en archivos"""
    # Obtener el directorio de salida estandarizado para problemas generados
    output_dir = get_output_dir(['generated_problems'])
    
    print(f"Generando {args.num_problems} problemas aleatorios...")
    
    for i in range(args.num_problems):
        # Generar problema
        problem = ProblemLoader.generate_random_problem(
            num_jobs=args.num_jobs,
            num_machines=args.num_machines,
            seed=args.seed + i if args.seed is not None else None
        )
        
        # Guardar problema
        filename = f"problem_{i+1}_{args.num_jobs}x{args.num_machines}.{args.output_format}"
        filepath = os.path.join(output_dir, filename)
        
        ProblemLoader.save_problem(
            problem=problem,
            file_path=filepath,
            format=args.output_format
        )
        
        print(f"  Problema {i+1} guardado en: {filepath}")
    
    print(f"\nGeneración completada. Problemas guardados en: {output_dir}")

def main():
    """Función principal"""
    args = parse_args()
    setup_logging(args.log_level)
    
    print(f"JobShopRL - Sistema de aprendizaje por refuerzo para problemas de Job Shop Scheduling")
    print(f"Modo: {args.mode}")
    
    if args.mode == 'single':
        run_single_experiment(args)
    elif args.mode == 'batch':
        run_batch_experiment(args)
    elif args.mode == 'generate':
        generate_problems(args)
    else:
        print(f"Modo no válido: {args.mode}")

if __name__ == "__main__":
    main()
