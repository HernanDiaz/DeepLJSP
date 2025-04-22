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
        # Asegurar que el directorio existe
        import os
        directory = os.path.dirname(checkpoint_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Asegurando que el directorio existe: {directory}")
        
        try:
            torch.save(checkpoint_data, checkpoint_path)
            logger.info(f"Checkpoint guardado en {checkpoint_path}")
        except Exception as e:
            logger.error(f"Error al guardar checkpoint en {checkpoint_path}: {str(e)}")
            # Intentar guardar en un directorio alternativo
            alt_path = os.path.join("checkpoints", os.path.basename(checkpoint_path))
            os.makedirs("checkpoints", exist_ok=True)
            logger.info(f"Intentando guardar en ruta alternativa: {alt_path}")
            torch.save(checkpoint_data, alt_path)
            logger.info(f"Checkpoint guardado en ruta alternativa: {alt_path}")
        
    @staticmethod
    def load_checkpoint(path: str) -> Dict[str, Any]:
        """
        Carga un checkpoint desde una ruta.
        
        Args:
            path: Ruta al archivo de checkpoint
            
        Returns:
            Diccionario con los datos del checkpoint
        """
        try:
            # Intentar cargar primero con weights_only=False (para compatibilidad con versiones más recientes de PyTorch)
            checkpoint = torch.load(path, weights_only=False)
            logger.info(f"Checkpoint cargado desde {path}")
            return checkpoint
        except TypeError:
            # Si el parámetro weights_only no es soportado (versiones antiguas de PyTorch)
            logger.warning("Compatibilidad: PyTorch no reconoce weights_only, intentando sin ese parámetro")
            checkpoint = torch.load(path)
            logger.info(f"Checkpoint cargado desde {path}")
            return checkpoint
        except Exception as e:
            logger.error(f"Error al cargar el checkpoint: {str(e)}")
            raise
