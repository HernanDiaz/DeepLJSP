"""
Utilidades para la gestión de semillas aleatorias y reproducibilidad.
"""

import random
import numpy as np
import torch
import logging

logger = logging.getLogger("JobShopRL.SeedUtils")

def set_random_seed(seed=None):
    """
    Establece la semilla aleatoria para todas las bibliotecas relevantes (random, numpy, torch).
    
    Args:
        seed (int, optional): Semilla a establecer. Si es None, no se aplicará ninguna semilla.
        
    Returns:
        int: La semilla aplicada, o None si no se aplicó ninguna.
    """
    if seed is None:
        return None
    
    # Convertir la semilla a int para evitar errores
    seed = int(seed)
    
    # Establecer semillas para todas las fuentes de aleatoriedad
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    
    # Establecer semilla para CUDA si está disponible
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        # Para reproducibilidad completa en CUDA
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    
    logger.info(f"Semilla aleatoria establecida: {seed}")
    return seed
