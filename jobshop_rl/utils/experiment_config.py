"""
Utilidades para guardar y cargar configuraciones de experimentos.
"""

import json
import os
import datetime
from typing import Dict, Any, Optional

from jobshop_rl.models.interval import Interval

def _json_default(obj: Any):
    """
    Serializador de respaldo para tipos no soportados por JSON.

    Los Interval (problemas con incertidumbre) se guardan como
    {"lower": x, "upper": y}; cualquier otro tipo se guarda como str
    para no perder la configuración completa por un solo campo.
    """
    if isinstance(obj, Interval):
        return {'lower': obj.lower, 'upper': obj.upper}
    if hasattr(obj, 'item'):  # escalares de numpy/torch
        return obj.item()
    return str(obj)


class ExperimentConfig:
    """Clase para manejar la configuración de experimentos"""

    @staticmethod
    def save_config(config: Dict[str, Any], experiment_name: Optional[str] = None, output_dir: str = "outputs/configs"):
        """
        Guarda la configuración de un experimento en un archivo JSON.
        
        Args:
            config: Diccionario con la configuración del experimento
            experiment_name: Nombre opcional para el experimento (si no se proporciona, se genera uno)
            output_dir: Directorio donde guardar el archivo de configuración
        
        Returns:
            Ruta al archivo de configuración guardado
        """
        # Asegurar que el directorio existe
        os.makedirs(output_dir, exist_ok=True)
        
        # Generar nombre de archivo si no se proporciona
        if experiment_name is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            experiment_name = f"experiment_{timestamp}"
            
        # Añadir timestamp a la configuración para registro
        config_with_meta = config.copy()
        config_with_meta['timestamp'] = datetime.datetime.now().isoformat()
        config_with_meta['experiment_name'] = experiment_name
        
        # Construir ruta del archivo
        filename = f"{experiment_name}.json"
        filepath = os.path.join(output_dir, filename)
        
        # Guardar configuración (default maneja Interval y otros tipos no JSON)
        with open(filepath, 'w') as f:
            json.dump(config_with_meta, f, indent=4, default=_json_default)
            
        return filepath
    
    @staticmethod
    def load_config(filepath: str) -> Dict[str, Any]:
        """
        Carga la configuración de un experimento desde un archivo JSON.
        
        Args:
            filepath: Ruta al archivo de configuración
            
        Returns:
            Diccionario con la configuración del experimento
        """
        with open(filepath, 'r') as f:
            config = json.load(f)
            
        return config
    
    @staticmethod
    def print_config(config: Dict[str, Any]):
        """
        Imprime la configuración de un experimento de forma legible.
        
        Args:
            config: Diccionario con la configuración del experimento
        """
        print("\n===== Configuración del experimento =====")
        
        # Mostrar metadatos primero si están presentes
        if 'experiment_name' in config:
            print(f"Experimento: {config['experiment_name']}")
        if 'timestamp' in config:
            print(f"Fecha: {config['timestamp']}")
            
        # Mostrar el resto de parámetros agrupados por categorías
        categories = {
            'Entorno': ['seed', 'reward_strategy'],
            'Agente': ['lr', 'gamma', 'eps_clip', 'K_epochs', 'entropy_coef', 
                     'use_lr_decay', 'use_grad_clip', 'advantage_normalization', 
                     'gae_lambda', 'feature_dim', 'hidden_dim'],
            'Recompensa': ['makespan_weight', 'idle_weight', 'critical_weight', 
                         'balance_weight', 'progress_weight', 'local_improvement_weight'],
            'Entrenamiento': ['episodes', 'checkpoint_interval', 'early_stopping'],
            'Problema': ['num_jobs', 'num_machines', 'problem_name', 'optimal_makespan']
        }
        
        # Imprimir parámetros por categoría
        for category, keys in categories.items():
            category_params = {k: config[k] for k in keys if k in config}
            if category_params:
                print(f"\n{category}:")
                for k, v in category_params.items():
                    print(f"  {k}: {v}")
                    
        # Imprimir parámetros que no entran en ninguna categoría
        other_keys = set(config.keys()) - {'experiment_name', 'timestamp'}
        for category in categories.values():
            other_keys -= set(category)
            
        if other_keys:
            print("\nOtros parámetros:")
            for k in sorted(other_keys):
                print(f"  {k}: {config[k]}")
