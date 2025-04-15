"""
Script para ejecutar el ejemplo de comparación de arquitecturas del archivo example_usage.py
"""

import os
import sys

# Añadir el directorio raíz del proyecto al path para poder importar jobshop_rl
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from jobshop_rl.example_usage import example_architecture_comparison

if __name__ == "__main__":
    print("Ejecutando comparación de arquitecturas en problema ABZ10...")
    results_df = example_architecture_comparison()
    print("\nComparación completada. Resumen de resultados:")
    print(results_df.groupby('Architecture').mean())
