"""
Script para ejecutar el ejemplo de GNN del archivo example_usage.py
"""

import os
import sys

# Añadir el directorio raíz del proyecto al path para poder importar jobshop_rl
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from jobshop_rl.example_usage import example_single_problem_gnn

if __name__ == "__main__":
    print("Ejecutando ejemplo de entrenamiento GNN en problema FT10...")
    agent, best_makespan, final_makespan = example_single_problem_gnn()
    print(f"Ejemplo completado. Mejor makespan: {best_makespan}, Makespan final: {final_makespan}")
