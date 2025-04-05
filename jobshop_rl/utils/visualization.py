"""
Utilidades para visualización de resultados y métricas.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Optional, Any

def plot_schedule(schedule: List[Dict], title: str, num_jobs: int, num_machines: int):
    """
    Visualiza una programación como un diagrama de Gantt.
    
    Args:
        schedule: Lista de operaciones programadas (diccionarios)
        title: Título del gráfico
        num_jobs: Número de trabajos
        num_machines: Número de máquinas
        
    Returns:
        Objeto figura de matplotlib
    """
    if not schedule:
        return None

    plt.figure(figsize=(15, 8))
    colors = plt.cm.tab10(np.linspace(0, 1, num_jobs))

    for op in schedule:
        plt.barh(op['machine'],
                op['end'] - op['start'],
                left=op['start'],
                color=colors[op['job']],
                edgecolor='black',
                alpha=0.8)

        plt.text(op['start'] + (op['end'] - op['start'])/2,
                op['machine'],
                f"J{op['job']},{op['operation']}",
                va='center',
                ha='center',
                color='white',
                fontweight='bold')

    plt.yticks(range(num_machines), [f'M{i}' for i in range(num_machines)])
    plt.xlabel('Tiempo')
    plt.ylabel('Máquina')
    plt.title(f"{title}\nMakespan: {max(max(op['end'] for op in schedule), 0)}")
    plt.grid(axis='x')

    return plt.gcf()

def plot_makespan_history(makespan_history: List[float], title: str = "Evolución del Makespan", 
                         optimal_makespan: Optional[float] = 930):
    """
    Visualiza la evolución del makespan a lo largo del tiempo.
    
    Args:
        makespan_history: Lista de valores de makespan
        title: Título del gráfico
        optimal_makespan: Valor óptimo conocido (si existe)
        
    Returns:
        Objeto figura de matplotlib
    """
    plt.figure(figsize=(12, 6))
    plt.plot(makespan_history, '-o')
    
    if optimal_makespan is not None:
        plt.axhline(y=optimal_makespan, color='r', linestyle='--', label=f'Óptimo: {optimal_makespan}')
    
    plt.xlabel('Pasos')
    plt.ylabel('Makespan')
    plt.title(title)
    plt.legend()
    plt.grid(True)

    return plt.gcf()

def plot_training_metrics(metrics: Dict[str, List[float]], window_size: int = 30):
    """
    Visualiza múltiples métricas de entrenamiento.
    
    Args:
        metrics: Diccionario con métricas (ej: {'makespan': [...], 'reward': [...]})
        window_size: Tamaño de la ventana para la media móvil
        
    Returns:
        Diccionario de figuras matplotlib
    """
    figures = {}
    
    # Crear una figura para cada métrica
    for metric_name, values in metrics.items():
        if not values:
            continue
            
        plt.figure(figsize=(12, 6))
        plt.plot(values, label=f'{metric_name} por episodio')
        
        # Calcular y añadir media móvil si hay suficientes datos
        if len(values) > window_size:
            moving_avg = [sum(values[max(0, i-window_size):i])/min(i, window_size) 
                         for i in range(1, len(values)+1)]
            plt.plot(moving_avg, linewidth=2, label=f'Media móvil ({window_size} episodios)')
        
        plt.xlabel('Episodios')
        plt.ylabel(metric_name.capitalize())
        plt.title(f'Evolución de {metric_name} durante el entrenamiento')
        plt.legend()
        plt.grid(True)
        
        figures[metric_name] = plt.gcf()
    
    return figures


def save_plots(plots: Dict[str, Any], directory: str = "./plots", prefix: str = ""):
    """
    Guarda una colección de gráficos en archivos.

    Args:
        plots: Diccionario de plots matplotlib
        directory: Directorio donde guardar los gráficos
        prefix: Prefijo para los nombres de archivos
    """
    import os
    import matplotlib.pyplot as plt

    # Crear directorio si no existe
    os.makedirs(directory, exist_ok=True)

    # Verificar que plots es un diccionario
    if not isinstance(plots, dict):
        print(f"Error: plots debe ser un diccionario, pero es {type(plots)}")
        return

    # Guardar cada gráfico
    for name, plot in plots.items():
        if plot is not None:
            try:
                filename = f"{prefix}_{name}.png" if prefix else f"{name}.png"
                filepath = os.path.join(directory, filename)

                # Verificar si el plot tiene el método savefig
                if hasattr(plot, 'savefig'):
                    plot.savefig(filepath)
                    plt.close(plot)
                else:
                    print(f"Error: plot '{name}' no tiene método savefig. Tipo: {type(plot)}")
            except Exception as e:
                print(f"Error al guardar plot '{name}': {e}")
