"""
Configuración global para activar las mejoras de red implementadas.
"""

# Activar las mejoras por defecto
USE_IMPROVED_NETWORKS = True

# Configuración específica por tamaño de problema
NETWORK_CONFIGS = {
    'small': {  # <= 10x10
        'use_batch_norm': False,
        'use_layer_norm': True,
        'network_type': 'standard',
        'features': 17,
    },
    'medium': {  # <= 20x20
        'use_batch_norm': True,
        'use_layer_norm': False,
        'network_type': 'standard',
        'features': 17,
    },
    'large': {  # <= 50x20
        'use_batch_norm': True,
        'use_layer_norm': False,
        'network_type': 'improved',
        'features': 17,
        'use_skip_connections': True,
    },
    'very_large': {  # <= 100x20
        'use_batch_norm': True,
        'use_layer_norm': False,
        'network_type': 'improved',
        'features': 17,
        'use_skip_connections': True,
        'use_gradient_centralization': True,
    },
    'huge': {  # > 100x20
        'use_batch_norm': True,
        'use_layer_norm': False,
        'network_type': 'ensemble',
        'features': 17,
        'use_skip_connections': True,
        'use_gradient_centralization': True,
        'use_swa': True,
    }
}

def get_problem_category(num_jobs, num_machines):
    """Determina la categoría del problema según su tamaño"""
    size = num_jobs * num_machines
    if size <= 100:
        return 'small'
    elif size <= 400:
        return 'medium'
    elif size <= 1000:
        return 'large'
    elif size <= 2000:
        return 'very_large'
    else:
        return 'huge'

def should_use_improved_networks(num_jobs, num_machines):
    """Determina si usar las redes mejoradas para un problema dado"""
    if not USE_IMPROVED_NETWORKS:
        return False
    
    category = get_problem_category(num_jobs, num_machines)
    config = NETWORK_CONFIGS[category]
    
    return config['network_type'] in ['improved', 'ensemble']
