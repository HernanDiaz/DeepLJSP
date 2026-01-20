"""
Utilidades para visualización de resultados y métricas.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Optional, Any

def plot_schedule(schedule: List[Dict], title: str, num_jobs: int, num_machines: int, env=None):
    """
    Visualiza una programación como un diagrama de Gantt.
    
    Para problemas con intervalos, usa paralelogramos que muestran la incertidumbre.
    Para problemas escalares, usa barras rectangulares tradicionales.
    
    Args:
        schedule: Lista de operaciones programadas (diccionarios)
        title: Título del gráfico
        num_jobs: Número de trabajos
        num_machines: Número de máquinas
        env: (Opcional) Instancia de JobShopEnv para delegar el renderizado
        
    Returns:
        Objeto figura de matplotlib
    """
    if not schedule:
        return None

    # Si se proporciona el entorno, delegar el renderizado
    # El entorno tiene la lógica correcta para manejar intervalos
    if env is not None:
        return env.render_schedule(title=title, schedule=schedule)
    
    # Fallback: renderizado básico para escalares
    # (Este código solo se usa cuando no se pasa env)
    plt.figure(figsize=(15, 8))
    colors = plt.cm.tab10(np.linspace(0, 1, num_jobs))

    for op in schedule:
        # Extraer valores de tiempo (pueden ser escalares o intervalos)
        start = op['start']
        end = op['end']
        
        # Convertir a float si es intervalo (usar punto medio)
        if hasattr(start, 'midpoint'):
            start_val = start.midpoint
        else:
            start_val = float(start) if not isinstance(start, (int, float)) else start
            
        if hasattr(end, 'midpoint'):
            end_val = end.midpoint
        else:
            end_val = float(end) if not isinstance(end, (int, float)) else end
        
        plt.barh(op['machine'],
                end_val - start_val,
                left=start_val,
                color=colors[op['job']],
                edgecolor='black',
                alpha=0.8)

        plt.text(start_val + (end_val - start_val)/2,
                op['machine'],
                f"J{op['job']},O{op['operation']}",
                va='center',
                ha='center',
                color='white',
                fontweight='bold')

    plt.yticks(range(num_machines), [f'M{i}' for i in range(num_machines)])
    plt.xlabel('Tiempo')
    plt.ylabel('Máquina')
    
    # Calcular makespan
    if schedule:
        makespans = [op['end'] for op in schedule]
        # Si son intervalos, mostrar el rango
        if hasattr(makespans[0], 'upper'):
            max_makespan = max(makespans)
            title_str = f"{title}\nMakespan: [{max_makespan.lower:.1f}, {max_makespan.upper:.1f}]"
        else:
            max_makespan = max(makespans)
            title_str = f"{title}\nMakespan: {max_makespan}"
    else:
        title_str = title
        
    plt.title(title_str)
    plt.grid(axis='x')

    return plt.gcf()

def plot_makespan_history(makespan_history: List, title: str = "Evolución del Makespan", 
                         optimal_makespan: Optional[float] = 930):
    """
    Visualiza la evolución del makespan a lo largo del tiempo.
    Soporta valores escalares, intervalos (tuplas) y objetos Interval.
    
    Args:
        makespan_history: Lista de valores de makespan (números, tuplas (lower, upper), o objetos Interval)
        title: Título del gráfico
        optimal_makespan: Valor óptimo conocido (si existe)
        
    Returns:
        Objeto figura de matplotlib
    """
    if not makespan_history:
        return None
    
    # Importar Interval para detección de tipo
    try:
        from jobshop_rl.models.interval import Interval
    except:
        Interval = None
        
    plt.figure(figsize=(12, 6))
    
    # Detectar el tipo de datos
    first_element = makespan_history[0]
    
    # Determinar si son intervalos (tuplas, listas, o objetos Interval)
    is_tuple_interval = isinstance(first_element, (tuple, list)) and len(first_element) == 2
    is_interval_object = Interval is not None and isinstance(first_element, Interval)
    is_interval = is_tuple_interval or is_interval_object
    
    if is_interval:
        # Extraer límites inferior y superior
        if is_interval_object:
            # Objetos Interval
            lower_bounds = [float(m.lower) if hasattr(m, 'lower') else float(m) for m in makespan_history]
            upper_bounds = [float(m.upper) if hasattr(m, 'upper') else float(m) for m in makespan_history]
        else:
            # Tuplas o listas
            lower_bounds = [m[0] for m in makespan_history]
            upper_bounds = [m[1] for m in makespan_history]
        
        episodes = list(range(len(makespan_history)))
        
        # Graficar banda de incertidumbre
        plt.fill_between(episodes, lower_bounds, upper_bounds, alpha=0.3, 
                         color='blue', label='Rango de incertidumbre')
        
        # Graficar límites
        plt.plot(episodes, lower_bounds, '--', color='green', alpha=0.7, 
                label='Mejor caso (límite inferior)', linewidth=1.5)
        plt.plot(episodes, upper_bounds, '--', color='red', alpha=0.7, 
                label='Peor caso (límite superior)', linewidth=1.5)
        
        # Calcular y graficar media móvil de ambos límites
        window_size = min(30, len(makespan_history))
        if window_size > 0:
            moving_avg_lower = [sum(lower_bounds[max(0, i-window_size):i])/min(i, window_size)
                               for i in range(1, len(lower_bounds)+1)]
            moving_avg_upper = [sum(upper_bounds[max(0, i-window_size):i])/min(i, window_size)
                               for i in range(1, len(upper_bounds)+1)]
            
            plt.plot(episodes, moving_avg_lower, color='darkgreen', linewidth=2, 
                    label=f'Media móvil inferior ({window_size} eps)')
            plt.plot(episodes, moving_avg_upper, color='darkred', linewidth=2, 
                    label=f'Media móvil superior ({window_size} eps)')
    else:
        # Formato escalar tradicional
        # Convertir a float por si acaso hay algún tipo numérico extraño
        scalar_values = [float(m) for m in makespan_history]
        plt.plot(scalar_values, color='blue', label='Makespan')
        
        # Calcular y añadir media móvil
        window_size = min(30, len(scalar_values))
        if window_size > 0:
            moving_avg = [sum(scalar_values[max(0, i-window_size):i])/min(i, window_size)
                         for i in range(1, len(scalar_values)+1)]
            plt.plot(moving_avg, color='darkblue', linewidth=2, 
                    label=f'Media móvil ({window_size} episodios)')
    
    # Línea de valor óptimo si se proporciona
    if optimal_makespan is not None:
        plt.axhline(y=optimal_makespan, color='purple', linestyle='--', 
                   label=f'Óptimo: {optimal_makespan}', linewidth=2)
    
    plt.xlabel('Episodios')
    plt.ylabel('Makespan')
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)

    return plt.gcf()

def plot_training_metrics(metrics: Dict[str, List], window_size: int = 30):
    """
    Visualiza múltiples métricas de entrenamiento.
    Soporta valores escalares, intervalos (tuplas) y objetos Interval.
    
    Args:
        metrics: Diccionario con métricas (ej: {'makespan': [...], 'reward': [...]})
        window_size: Tamaño de la ventana para la media móvil
        
    Returns:
        Diccionario de figuras matplotlib
    """
    # Importar Interval para detección de tipo
    try:
        from jobshop_rl.models.interval import Interval
    except:
        Interval = None
    
    figures = {}
    
    # Crear una figura para cada métrica
    for metric_name, values in metrics.items():
        if not values:
            continue
        
        # Detectar si son intervalos
        first_element = values[0]
        is_tuple_interval = isinstance(first_element, (tuple, list)) and len(first_element) == 2
        is_interval_object = Interval is not None and isinstance(first_element, Interval)
        is_interval = is_tuple_interval or is_interval_object
        
        plt.figure(figsize=(12, 6))
        
        if is_interval:
            # Extraer límites
            if is_interval_object:
                lower_bounds = [float(v.lower) if hasattr(v, 'lower') else float(v) for v in values]
                upper_bounds = [float(v.upper) if hasattr(v, 'upper') else float(v) for v in values]
            else:
                lower_bounds = [v[0] for v in values]
                upper_bounds = [v[1] for v in values]
            
            episodes = list(range(len(values)))
            
            # Banda de incertidumbre
            plt.fill_between(episodes, lower_bounds, upper_bounds, alpha=0.3, 
                           color='blue', label='Rango')
            
            # Límites
            plt.plot(episodes, lower_bounds, '--', alpha=0.7, label='Límite inferior')
            plt.plot(episodes, upper_bounds, '--', alpha=0.7, label='Límite superior')
            
            # Media móvil
            window = min(window_size, len(values))
            if window > 0:
                moving_avg_lower = [sum(lower_bounds[max(0, i-window):i])/min(i, window) 
                                   for i in range(1, len(lower_bounds)+1)]
                moving_avg_upper = [sum(upper_bounds[max(0, i-window):i])/min(i, window) 
                                   for i in range(1, len(upper_bounds)+1)]
                
                plt.plot(episodes, moving_avg_lower, linewidth=2, 
                        label=f'Media móvil inferior ({window} eps)')
                plt.plot(episodes, moving_avg_upper, linewidth=2, 
                        label=f'Media móvil superior ({window} eps)')
        else:
            # Formato escalar tradicional
            scalar_values = [float(v) for v in values]
            plt.plot(scalar_values, label=metric_name)
            
            # Color específico para la media móvil según el tipo de métrica
            line_color = 'blue'
            if 'reward' in metric_name.lower():
                line_color = 'green'
            
            # Calcular y añadir media móvil
            window = min(window_size, len(scalar_values))
            if window > 0:
                moving_avg = [sum(scalar_values[max(0, i-window):i])/min(i, window) 
                             for i in range(1, len(scalar_values)+1)]
                plt.plot(moving_avg, color=line_color, linewidth=2, 
                        label=f'Media móvil ({window} episodios)')
        
        plt.xlabel('Episodios')
        plt.ylabel(metric_name.capitalize())
        plt.title(f'Evolución de {metric_name} durante el entrenamiento')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        figures[metric_name] = plt.gcf()
    
    return figures


def save_plots(plots: Dict[str, Any], directory: str = "outputs/plots", prefix: str = ""):
    """
    Guarda una colección de gráficos en archivos.

    Args:
        plots: Diccionario de plots matplotlib o diccionarios de plots
        directory: Directorio donde guardar los gráficos (por defecto outputs/plots)
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
        if plot is None:
            continue
            
        try:
            # Si plot es un diccionario de figuras (como el que devuelve plot_training_metrics)
            if isinstance(plot, dict):
                for subname, subfig in plot.items():
                    if subfig is not None and hasattr(subfig, 'savefig'):
                        # Crear un nombre único para cada subfigura
                        if prefix:
                            filename = f"{prefix}_{name}_{subname}.png"
                        else:
                            filename = f"{name}_{subname}.png"
                        filepath = os.path.join(directory, filename)
                        subfig.savefig(filepath)
                        plt.close(subfig)
            # Si plot es una figura directamente
            elif hasattr(plot, 'savefig'):
                filename = f"{prefix}_{name}.png" if prefix else f"{name}.png"
                filepath = os.path.join(directory, filename)
                plot.savefig(filepath)
                plt.close(plot)
            else:
                print(f"Error: plot '{name}' no tiene método savefig ni es un diccionario de figuras. Tipo: {type(plot)}")
        except Exception as e:
            print(f"Error al guardar plot '{name}': {e}")
