"""
Script para ejecutar el ejemplo de entrenamiento multi-instancia del archivo example_usage.py
"""

import os
import sys

# Añadir el directorio raíz del proyecto al path para poder importar jobshop_rl
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from jobshop_rl.example_usage import example_multi_instance_training

if __name__ == "__main__":
    print("Ejecutando ejemplo de entrenamiento multi-instancia...")
    agent, eval_results, results = example_multi_instance_training()
    print("Ejemplo completado.")
    
    print("\nResultados de evaluación:")
    for problem_id, result in eval_results.items():
        print(f"  {problem_id}: Makespan = {result['makespan']}")
