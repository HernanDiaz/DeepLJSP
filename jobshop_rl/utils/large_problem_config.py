"""
Configuración especializada para problemas grandes de Job Shop.
"""

from typing import Dict, Any
import logging

logger = logging.getLogger("JobShopRL.LargeProblemConfig")


def get_ppo_config_for_large_problems(
    num_jobs: int, 
    num_machines: int,
    use_batch_norm: bool = True
) -> Dict[str, Any]:
    """
    Retorna configuración optimizada de PPO para problemas grandes.
    
    Args:
        num_jobs: Número de trabajos
        num_machines: Número de máquinas
        use_batch_norm: Si usar BatchNorm estabilizado
        
    Returns:
        Diccionario con parámetros de configuración
    """
    problem_size = num_jobs * num_machines
    
    # Configuración base
    config = {
        "feature_dim": 7,
        "lr": 0.0003,
        "gamma": 0.99,
        "eps_clip": 0.2,
        "K_epochs": 4,
        "entropy_coef": 0.01,
        "use_lr_decay": True,
        "use_grad_clip": True,
        "advantage_normalization": True,
        "gae_lambda": 0.95,
        "use_batch_norm": use_batch_norm
    }
    
    # Ajustes para problemas medianos (30x20, 50x20)
    if problem_size > 600:
        config.update({
            "lr": 0.0002,
            "K_epochs": 5,
            "entropy_coef": 0.015,
            "policy_depth": 4,
            "value_depth": 5
        })
        
    # Ajustes para problemas grandes (100x20)
    if problem_size >= 2000:
        config.update({
            "lr": 0.0001,
            "K_epochs": 6,
            "entropy_coef": 0.02,
            "eps_clip": 0.15,
            "policy_depth": 5,
            "value_depth": 6
        })
        
    logger.info(f"Configuración PPO para problema {num_jobs}x{num_machines} (tamaño={problem_size}):")
    logger.info(f"  - Learning rate: {config['lr']}")
    logger.info(f"  - K epochs: {config['K_epochs']}")
    logger.info(f"  - Entropy coef: {config['entropy_coef']}")
    logger.info(f"  - BatchNorm: {config['use_batch_norm']}")
    
    return config


def get_training_config_for_large_problems(
    num_jobs: int, 
    num_machines: int
) -> Dict[str, Any]:
    """
    Retorna configuración de entrenamiento para problemas grandes.
    
    Args:
        num_jobs: Número de trabajos
        num_machines: Número de máquinas
        
    Returns:
        Diccionario con parámetros de entrenamiento
    """
    problem_size = num_jobs * num_machines
    
    # Configuración base
    config = {
        "episodes": 500,
        "lr_decay": True,
        "log_interval": 10,
        "checkpoint_interval": 50,
        "dynamic_entropy": True,
        "early_stopping": True,
        "early_stopping_patience": 50
    }
    
    # Ajustes para problemas medianos
    if problem_size > 600:
        config.update({
            "episodes": 700,
            "log_interval": 20,
            "checkpoint_interval": 100,
            "early_stopping_patience": 75
        })
        
    # Ajustes para problemas grandes
    if problem_size >= 2000:
        config.update({
            "episodes": 1000,
            "log_interval": 25,
            "checkpoint_interval": 150,
            "early_stopping_patience": 100
        })
        
    return config


def get_memory_config_for_large_problems(
    num_jobs: int, 
    num_machines: int
) -> Dict[str, Any]:
    """
    Retorna configuración de memoria y batch para problemas grandes.
    
    Args:
        num_jobs: Número de trabajos
        num_machines: Número de máquinas
        
    Returns:
        Diccionario con parámetros de memoria
    """
    problem_size = num_jobs * num_machines
    
    # Configuración base
    config = {
        "buffer_size": 2048,
        "batch_size": 64,
        "min_batch_size": 8,
        "accumulation_steps": 1
    }
    
    # Ajustes según el tamaño
    if problem_size > 600:
        config.update({
            "buffer_size": 4096,
            "batch_size": 128,
            "min_batch_size": 16,
            "accumulation_steps": 2
        })
        
    if problem_size >= 1000:
        config.update({
            "buffer_size": 8192,
            "batch_size": 256,
            "min_batch_size": 32,
            "accumulation_steps": 4
        })
        
    if problem_size >= 2000:
        config.update({
            "buffer_size": 16384,
            "batch_size": 512,
            "min_batch_size": 64,
            "accumulation_steps": 8
        })
        
    return config


def create_optimized_ppo_agent(env, **kwargs):
    """
    Crea un agente PPO optimizado para el tamaño del problema.
    
    Args:
        env: Entorno de Job Shop
        **kwargs: Parámetros adicionales para sobrescribir la configuración
        
    Returns:
        Agente PPO configurado
    """
    from jobshop_rl.agents.ppo_agent import PPOAgent
    
    # Obtener configuración base
    ppo_config = get_ppo_config_for_large_problems(
        env.num_jobs, 
        env.num_machines,
        kwargs.get("use_batch_norm", True)
    )
    
    # Sobrescribir con parámetros proporcionados
    ppo_config.update(kwargs)
    
    # Crear el agente
    agent = PPOAgent(env, **ppo_config)
    
    return agent
