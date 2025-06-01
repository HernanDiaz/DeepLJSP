"""
Configuración de redes neuronales para diferentes tamaños de problemas.
"""

def get_network_config(num_jobs: int, num_machines: int):
    """
    Obtiene la configuración óptima de red para un tamaño de problema dado.
    
    Args:
        num_jobs: Número de trabajos
        num_machines: Número de máquinas
        
    Returns:
        Dict con configuración de red
    """
    problem_size = num_jobs * num_machines
    
    config = {
        'use_batch_norm': True,  # Por defecto usar BatchNorm
        'momentum': 0.01,  # Momentum bajo para estabilidad
        'batch_size_min': 8,  # Tamaño mínimo de batch para BatchNorm
        'gradient_accumulation_steps': 1,
        'network_type': 'standard',  # 'standard', 'improved', o 'ensemble'
        'dropout_rate': 0.1,
        'skip_connections': False,
        'warmup_episodes': 50,
        'use_gradient_centralization': False,
        'use_swa': False  # Stochastic Weight Averaging
    }
    
    if problem_size <= 100:  # 10x10 o menos
        config.update({
            'use_batch_norm': False,  # LayerNorm para problemas pequeños
            'network_type': 'standard',
            'dropout_rate': 0.1,
        })
    elif problem_size <= 400:  # hasta 20x20
        config.update({
            'use_batch_norm': True,
            'momentum': 0.05,
            'network_type': 'standard',
            'dropout_rate': 0.15,
        })
    elif problem_size <= 1000:  # hasta 50x20
        config.update({
            'use_batch_norm': True,
            'momentum': 0.01,
            'batch_size_min': 16,
            'gradient_accumulation_steps': 4,
            'network_type': 'improved',
            'dropout_rate': 0.2,
            'skip_connections': True,
            'warmup_episodes': 100,
        })
    elif problem_size <= 2000:  # hasta 100x20
        config.update({
            'use_batch_norm': True,
            'momentum': 0.01,
            'batch_size_min': 32,
            'gradient_accumulation_steps': 8,
            'network_type': 'improved',
            'dropout_rate': 0.25,
            'skip_connections': True,
            'warmup_episodes': 150,
            'use_gradient_centralization': True,
        })
    else:  # Problemas extremadamente grandes
        config.update({
            'use_batch_norm': True,
            'momentum': 0.01,
            'batch_size_min': 64,
            'gradient_accumulation_steps': 16,
            'network_type': 'ensemble',
            'dropout_rate': 0.3,
            'skip_connections': True,
            'warmup_episodes': 200,
            'use_gradient_centralization': True,
            'use_swa': True,
        })
    
    return config


def apply_gradient_centralization(optimizer):
    """
    Aplica gradient centralization a un optimizador.
    Ayuda a estabilizar el entrenamiento en problemas grandes.
    """
    for group in optimizer.param_groups:
        for p in group['params']:
            if p.grad is not None and len(p.grad.shape) > 1:
                # Centralizar gradientes (restar la media)
                p.grad.data -= p.grad.data.mean(dim=tuple(range(1, len(p.grad.shape))), keepdim=True)
