"""
Utilidades para gestión de rutas y directorios.
Proporciona funciones para estandarizar el manejo de rutas en todo el proyecto.
"""

import os
from typing import Optional, List

# Constantes para directorios comunes
DEFAULT_OUTPUT_DIR = "outputs"
CHECKPOINTS_DIR = "checkpoints"
PLOTS_DIR = "plots"
RESULTS_DIR = "results"
GENERATED_PROBLEMS_DIR = "generated_problems"

def ensure_dir(dir_path: str) -> str:
    """
    Asegura que un directorio exista, creándolo si es necesario.
    
    Args:
        dir_path: Ruta al directorio que debe existir
        
    Returns:
        La ruta del directorio (igual a dir_path)
    """
    os.makedirs(dir_path, exist_ok=True)
    return dir_path

def get_output_dir(subdirs: Optional[List[str]] = None) -> str:
    """
    Obtiene la ruta al directorio de salida, creándolo si es necesario.
    
    Args:
        subdirs: Lista opcional de subdirectorios para incluir en la ruta
        
    Returns:
        Ruta al directorio de salida
    """
    path = DEFAULT_OUTPUT_DIR
    if subdirs:
        for subdir in subdirs:
            path = os.path.join(path, subdir)
    
    return ensure_dir(path)

def get_checkpoint_path(filename: str) -> str:
    """
    Obtiene la ruta completa para un archivo de checkpoint.
    
    Args:
        filename: Nombre del archivo de checkpoint
        
    Returns:
        Ruta completa al archivo de checkpoint
    """
    checkpoint_dir = get_output_dir([CHECKPOINTS_DIR])
    return os.path.join(checkpoint_dir, filename)

def get_plots_dir(experiment_name: Optional[str] = None) -> str:
    """
    Obtiene el directorio para gráficos, creándolo si es necesario.
    
    Args:
        experiment_name: Nombre opcional del experimento para subdirectorio
        
    Returns:
        Ruta al directorio de gráficos
    """
    subdirs = [PLOTS_DIR]
    if experiment_name:
        subdirs.append(experiment_name)
    
    return get_output_dir(subdirs)

def join_paths(*paths) -> str:
    """
    Une rutas de manera portátil.
    
    Args:
        *paths: Componentes de la ruta a unir
        
    Returns:
        Ruta unida
    """
    return os.path.join(*paths)
