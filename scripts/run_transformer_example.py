"""
Script para ejecutar el ejemplo de Transformer del archivo example_usage.py
"""

import os
import sys

# Añadir el directorio raíz del proyecto al path para poder importar jobshop_rl
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from jobshop_rl.example_usage import example_transformer_large_problem

if __name__ == "__main__":
    print("Ejecutando ejemplo de entrenamiento Transformer en problema TAI20_20_01...")
    agent, best_makespan, final_makespan = example_transformer_large_problem()
    print(f"Ejemplo completado. Mejor makespan: {best_makespan}, Makespan final: {final_makespan}")
