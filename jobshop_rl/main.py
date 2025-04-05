"""
Punto de entrada principal para el sistema JobShopRL.
"""

import os
import argparse
import logging
import time
from typing import Dict, Any, Optional

from jobshop_rl.experiments.factory import ExperimentFactory
from jobshop_rl.experiments.batch_experimenter import BatchExperimenter
from jobshop_rl.data.problem_loader import ProblemLoader
from jobshop_rl.utils.logging import TrainingLogger

def parse_args():
    """Configura y parsea los argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(description='Sistema de RL para Job Shop Scheduling')
    
    # Modo de ejecución
    parser.add_argument('--mode', type=str, default='single', choices=['single', 'batch', 'generate'],
                        help='Modo de ejecución: single (un problema), batch (múltiples problemas) o generate (generar problemas)')
    
    # Parámetros para modo single
    parser.add_argument('--episodes', type=int, default=300,
                       help='Número de episodios para entrenar (modo single)')
    parser.add_argument('--reward', type=str, default='advanced',
                       help='Estrategia de recompensa: basic, advanced o combined')
    parser.add_argument('--visualize', action='store_true',
                       help='Generar visualizaciones')
    parser.add_argument('--save-plots', action='store_true',
                       help='Guardar visualizaciones en archivos')
    
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
    """Ejecuta un experimento con un único problema (FT10)"""
    # Asegurar que existe el directorio de salida
    output_dir = "outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    reward_params = {
        "makespan_weight": 1.0,
        "idle_weight": 0.2,
        "critical_weight": 0.1,
        "balance_weight": 0.05,
        "progress_weight": 0.2,
        "local_improvement_weight": 0.15
    }
    
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
    
    agent, results = ExperimentFactory.run_full_experiment(
        episodes=args.episodes,
        reward_strategy=args.reward,
        agent_params=agent_params,
        reward_params=reward_params,
        seed=args.seed,
        visualize=args.visualize,
        save_plots=args.save_plots,
        csv_logging=args.csv_logging,
        csv_filename=args.csv_file,
        csv_base_dir=output_dir,
        output_dir=output_dir,
        experiment_name=args.experiment_name
    )
    
    total_time = time.time() - start_time
    
    print(f"\n===== Resultados del experimento =====")
    print(f"Tiempo total: {total_time:.2f} segundos")
    print(f"Mejor makespan: {agent.best_makespan}")
    print(f"Makespan final: {results['final_makespan']}")
    
    if 'comparison' in results:
        print("\nComparación con heurísticas:")
        for heuristic, improvement in results['comparison'].items():
            print(f"  vs {heuristic}: {improvement:.2f}% de mejora")
            
    return agent, results

def run_batch_experiment(args):
    """Ejecuta un experimento por lotes con múltiples problemas"""
    # Asegurar que existe el directorio de salida principal
    output_dir = "outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # Modificar el directorio de salida para usar outputs/results
    batch_output_dir = os.path.join(output_dir, os.path.basename(args.output_dir))
    
    reward_params = {
        "makespan_weight": 1.0,
        "idle_weight": 0.2,
        "critical_weight": 0.1,
        "balance_weight": 0.05,
        "progress_weight": 0.2,
        "local_improvement_weight": 0.15
    }
    
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
    
    # Crear directorios si no existen
    os.makedirs(args.training_dir, exist_ok=True)
    os.makedirs(args.test_dir, exist_ok=True)
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
    
    # Entrenar el agente
    start_time = time.time()
    best_agent = experimenter.train_agent(episodes_per_problem=args.episodes_per_problem)
    training_time = time.time() - start_time
    
    if best_agent is None:
        print("No se pudo completar el entrenamiento. Revise los logs para más detalles.")
        return None
    
    # Evaluar en problemas de prueba
    start_time = time.time()
    results = experimenter.evaluate_on_test_set(best_agent)
    eval_time = time.time() - start_time
    
    # Mostrar resumen
    print(f"\n===== Resultados del experimento por lotes =====")
    print(f"Tiempo total de entrenamiento: {training_time:.2f} segundos")
    print(f"Tiempo total de evaluación: {eval_time:.2f} segundos")
    print(f"Problemas entrenados: {len(experimenter.training_problems)}")
    print(f"Problemas evaluados: {len(experimenter.test_problems)}")
    
    if not results.empty:
        print(f"\nResumen de evaluación:")
        print(f"  Makespan promedio: {results['makespan'].mean():.2f}")
        
        # Calcular gap promedio para problemas con óptimo conocido
        if 'gap' in results.columns:
            valid_gaps = results['gap'].dropna()
            if len(valid_gaps) > 0:
                print(f"  Gap promedio del óptimo: {valid_gaps.mean():.2f}%")
                print(f"  Gap mínimo: {valid_gaps.min():.2f}%")
                print(f"  Gap máximo: {valid_gaps.max():.2f}%")
    
    print(f"\nResultados completos guardados en: {batch_output_dir}")
    
    return best_agent, results

def generate_problems(args):
    """Genera problemas aleatorios y los guarda en archivos"""
    # Asegurar que existe el directorio de salida principal
    main_output_dir = "outputs"
    if not os.path.exists(main_output_dir):
        os.makedirs(main_output_dir, exist_ok=True)
        
    # Crear directorio de salida para problemas generados
    output_dir = os.path.join(main_output_dir, 'generated_problems')
    os.makedirs(output_dir, exist_ok=True)
    
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
