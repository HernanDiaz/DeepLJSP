"""
Utilidades para gestionar checkpoints de modelos.
"""

import torch
import logging
from typing import Dict, Any

logger = logging.getLogger("JobShopRL.CheckpointManager")

class CheckpointManager:
    """Clase para gestionar guardar y cargar checkpoints de modelos"""
    
    @staticmethod
    def save_checkpoint(checkpoint_data: Dict[str, Any], checkpoint_path: str):
        """
        Guarda el estado del modelo en un checkpoint.
        
        Args:
            checkpoint_data: Diccionario con datos a guardar
            checkpoint_path: Ruta completa donde guardar el checkpoint
        """
        torch.save(checkpoint_data, checkpoint_path)
        logger.info(f"Checkpoint guardado en {checkpoint_path}")
        
    @staticmethod
    def load_checkpoint(path: str) -> Dict[str, Any]:
        """
        Carga un checkpoint desde una ruta.
        
        Args:
            path: Ruta al archivo de checkpoint
            
        Returns:
            Diccionario con los datos del checkpoint
        """
        checkpoint = torch.load(path)
        logger.info(f"Checkpoint cargado desde {path}")
        return checkpoint
