"""
Script para ejecutar el módulo principal de JobShopRL con parámetros específicos.
"""

import os
import sys
import subprocess
import argparse

# Añadir el directorio raíz del proyecto al path para poder importar jobshop_rl
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_dir)

def run_main_module(train_problem="ft10", eval_problem="abz10", episodes=300, 
                    reward="adaptive", visualize=True, save_plots=True):
    """
    Ejecuta el módulo principal de JobShopRL con los parámetros especificados.
    
    Args:
        train_problem: Problema para entrenamiento
        eval_problem: Problema para evaluación
        episodes: Número de episodios de entrenamiento
        reward: Estrategia de recompensa
        visualize: Si se deben mostrar visualizaciones
        save_plots: Si se deben guardar los gráficos
    """
    # Construir el comando
    cmd = [
        "python", "-m", "jobshop_rl.main",
        "--mode", "single",
        "--episodes", str(episodes),
        "--reward", reward,
        "--train-problem", train_problem,
        "--eval-problem", eval_problem
    ]
    
    # Añadir opciones booleanas
    if visualize:
        cmd.append("--visualize")
    if save_plots:
        cmd.append("--save-plots")
    
    # Ejecutar el comando
    print(f"Ejecutando: {' '.join(cmd)}")
    subprocess.run(cmd, cwd=root_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ejecutar el módulo principal de JobShopRL")
    parser.add_argument("--train-problem", default="ft10", help="Problema para entrenamiento")
    parser.add_argument("--eval-problem", default="abz10", help="Problema para evaluación")
    parser.add_argument("--episodes", type=int, default=300, help="Número de episodios")
    parser.add_argument("--reward", default="adaptive", help="Estrategia de recompensa")
    parser.add_argument("--visualize", action="store_true", help="Mostrar visualizaciones")
    parser.add_argument("--no-visualize", dest="visualize", action="store_false", help="No mostrar visualizaciones")
    parser.add_argument("--save-plots", action="store_true", help="Guardar gráficos")
    parser.add_argument("--no-save-plots", dest="save_plots", action="store_false", help="No guardar gráficos")
    
    # Establecer valores predeterminados para opciones booleanas
    parser.set_defaults(visualize=True, save_plots=True)
    
    args = parser.parse_args()
    
    # Ejecutar con los argumentos proporcionados
    run_main_module(
        train_problem=args.train_problem,
        eval_problem=args.eval_problem,
        episodes=args.episodes,
        reward=args.reward,
        visualize=args.visualize,
        save_plots=args.save_plots
    )
