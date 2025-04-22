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
    try:
        # Normaliza la ruta para manejar diferentes formatos de separadores
        norm_path = os.path.normpath(dir_path)
        os.makedirs(norm_path, exist_ok=True)
        
        # Verificar que el directorio realmente existe después de crearlo
        if not os.path.isdir(norm_path):
            raise OSError(f"No se pudo crear o acceder al directorio: {norm_path}")
            
        return norm_path
    except Exception as e:
        # Obtener el logger para registrar el error
        import logging
        logger = logging.getLogger("JobShopRL.PathUtils")
        logger.error(f"Error al crear directorio {dir_path}: {str(e)}")
        
        # En caso de error, intentar crear un directorio alternativo
        try:
            fallback_dir = os.path.join("outputs", os.path.basename(dir_path))
            os.makedirs(fallback_dir, exist_ok=True)
            logger.warning(f"Usando directorio alternativo: {fallback_dir}")
            return fallback_dir
        except:
            # Si todo falla, usar el directorio actual
            logger.warning("Usando directorio actual como último recurso")
            return "."

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
