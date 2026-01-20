"""
Problema FT10 con incertidumbre en tiempos de procesamiento.

Esta versión del FT10 clásico utiliza duraciones con intervalos
personalizados para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


# Configuración del problema FT10 con intervalos
# 10 trabajos x 10 máquinas
# Cada duración tiene aproximadamente ±10% de incertidumbre

FT10_INTERVAL_DATA = {
    'num_jobs': 10,
    'num_machines': 10,
    'problem_id': 'ft10_interval',
    'sequences': [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [0, 2, 4, 9, 3, 1, 6, 5, 7, 8],
        [1, 0, 3, 2, 8, 5, 7, 6, 9, 4],
        [1, 2, 0, 4, 6, 8, 7, 3, 9, 5],
        [2, 0, 1, 5, 3, 4, 8, 7, 9, 6],
        [2, 1, 5, 3, 8, 9, 0, 6, 4, 7],
        [1, 0, 3, 2, 6, 5, 9, 8, 7, 4],
        [2, 0, 1, 5, 4, 6, 8, 9, 7, 3],
        [0, 1, 3, 5, 2, 9, 6, 7, 4, 8],
        [1, 0, 2, 6, 8, 9, 5, 3, 4, 7]
    ],
    'durations': [
        # Job 0
        [Interval(25, 33), Interval(74, 82), Interval(9, 9), Interval(32, 40), 
         Interval(49, 49), Interval(11, 11), Interval(59, 65), Interval(56, 56), 
         Interval(39, 49), Interval(20, 22)],
        
        # Job 1
        [Interval(39, 47), Interval(89, 91), Interval(67, 83), Interval(11, 11), 
         Interval(63, 75), Interval(25, 31), Interval(46, 46), Interval(43, 49), 
         Interval(71, 73), Interval(27, 33)],
        
        # Job 2
        [Interval(86, 96), Interval(77, 93), Interval(34, 44), Interval(64, 84), 
         Interval(89, 91), Interval(10, 10), Interval(11, 13), Interval(87, 91), 
         Interval(41, 49), Interval(31, 35)],
        
        # Job 3
        [Interval(79, 83), Interval(94, 96), Interval(62, 80), Interval(92, 106), 
         Interval(9, 9), Interval(46, 58), Interval(74, 96), Interval(90, 106), 
         Interval(21, 23), Interval(41, 45)],
        
        # Job 4
        [Interval(13, 15), Interval(6, 6), Interval(22, 22), Interval(53, 69), 
         Interval(25, 27), Interval(64, 74), Interval(20, 22), Interval(46, 52), 
         Interval(72, 72), Interval(46, 60)],
        
        # Job 5
        [Interval(75, 93), Interval(2, 2), Interval(52, 52), Interval(89, 101), 
         Interval(43, 53), Interval(70, 74), Interval(44, 50), Interval(62, 68), 
         Interval(6, 6), Interval(23, 27)],
        
        # Job 6
        [Interval(43, 49), Interval(34, 40), Interval(60, 62), Interval(13, 13), 
         Interval(28, 36), Interval(20, 22), Interval(29, 35), Interval(83, 95), 
         Interval(29, 31), Interval(54, 56)],
        
        # Job 7
        [Interval(29, 33), Interval(86, 86), Interval(46, 46), Interval(65, 83), 
         Interval(29, 35), Interval(79, 97), Interval(17, 21), Interval(45, 51), 
         Interval(35, 37), Interval(69, 89)],
        
        # Job 8
        [Interval(72, 80), Interval(63, 75), Interval(67, 85), Interval(51, 51), 
         Interval(77, 93), Interval(10, 12), Interval(36, 44), Interval(83, 95), 
         Interval(26, 26), Interval(73, 75)],
        
        # Job 9
        [Interval(81, 89), Interval(13, 13), Interval(58, 64), Interval(7, 7), 
         Interval(59, 69), Interval(70, 82), Interval(46, 48), Interval(50, 54), 
         Interval(82, 98), Interval(41, 49)]
    ],
    'name': 'FT10_Interval',
    'has_intervals': True,
    'description': 'FT10 benchmark problem with custom interval processing times'
}


def get_ft10_interval_problem():
    """
    Obtiene los datos del problema FT10 con intervalos.
    
    Returns:
        Diccionario con los datos del problema FT10 con incertidumbre
    """
    return FT10_INTERVAL_DATA


def get_ft10_deterministic_as_intervals():
    """
    Obtiene FT10 determinístico representado como intervalos degenerados.
    
    Útil para validar que el sistema maneja correctamente el caso especial
    donde todos los intervalos son puntos (p⁻ = p⁺).
    
    Returns:
        Diccionario con los datos del problema FT10 con intervalos degenerados
    """
    # Duraciones originales del FT10
    original_durations = [
        [29, 78, 9, 36, 49, 11, 62, 56, 44, 21],
        [43, 90, 75, 11, 69, 28, 46, 46, 72, 30],
        [91, 85, 39, 74, 90, 10, 12, 89, 45, 33],
        [81, 95, 71, 99, 9, 52, 85, 98, 22, 43],
        [14, 6, 22, 61, 26, 69, 21, 49, 72, 53],
        [84, 2, 52, 95, 48, 72, 47, 65, 6, 25],
        [46, 37, 61, 13, 32, 21, 32, 89, 30, 55],
        [31, 86, 46, 74, 32, 88, 19, 48, 36, 79],
        [76, 69, 76, 51, 85, 11, 40, 89, 26, 74],
        [85, 13, 61, 7, 64, 76, 47, 52, 90, 45]
    ]
    
    # Convertir a intervalos degenerados
    interval_durations = []
    for job_durations in original_durations:
        interval_job = [Interval(d, d) for d in job_durations]
        interval_durations.append(interval_job)
    
    return {
        'num_jobs': 10,
        'num_machines': 10,
        'problem_id': 'ft10_deterministic_intervals',
        'sequences': FT10_INTERVAL_DATA['sequences'],
        'durations': interval_durations,
        'name': 'FT10_Deterministic_As_Intervals',
        'has_intervals': False,  # All intervals are degenerate
        'optimal_makespan': 930,  # Known optimal for FT10
        'description': 'FT10 with degenerate intervals (for backward compatibility testing)'
    }
