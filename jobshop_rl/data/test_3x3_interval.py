"""
Problema pequeño 3x3 para pruebas con intervalos.

Este problema pequeño es útil para:
- Debugging de algoritmos con intervalos
- Validación manual de resultados
- Pruebas rápidas de funcionalidad
- Ejemplos en documentación
"""

from jobshop_rl.models.interval import Interval


# Problema 3x3 con intervalos
TEST_3X3_INTERVAL = {
    'num_jobs': 3,
    'num_machines': 3,
    'problem_id': 'test_3x3_interval',
    'sequences': [
        [0, 1, 2],  # Job 0: M0 → M1 → M2
        [1, 0, 2],  # Job 1: M1 → M0 → M2
        [2, 1, 0]   # Job 2: M2 → M1 → M0
    ],
    'durations': [
        # Job 0: Moderate uncertainty
        [Interval(5, 7), Interval(3, 5), Interval(8, 10)],
        
        # Job 1: Low uncertainty
        [Interval(4, 5), Interval(7, 8), Interval(2, 3)],
        
        # Job 2: High uncertainty
        [Interval(3, 9), Interval(5, 7), Interval(6, 10)]
    ],
    'name': 'Test_3x3_Interval',
    'has_intervals': True,
    'description': 'Small 3x3 test problem with varied uncertainty levels'
}


# Problema 3x3 determinístico
TEST_3X3_DETERMINISTIC = {
    'num_jobs': 3,
    'num_machines': 3,
    'problem_id': 'test_3x3_deterministic',
    'sequences': [
        [0, 1, 2],
        [1, 0, 2],
        [2, 1, 0]
    ],
    'durations': [
        [6, 4, 9],   # Job 0: midpoints from interval version
        [5, 7, 2],   # Job 1
        [6, 6, 8]    # Job 2
    ],
    'name': 'Test_3x3_Deterministic',
    'has_intervals': False,
    'description': 'Small 3x3 deterministic test problem (midpoints of interval version)'
}


# Problema 3x3 con una sola operación incierta
TEST_3X3_PARTIAL_INTERVAL = {
    'num_jobs': 3,
    'num_machines': 3,
    'problem_id': 'test_3x3_partial',
    'sequences': [
        [0, 1, 2],
        [1, 0, 2],
        [2, 1, 0]
    ],
    'durations': [
        [6, 4, Interval(8, 10)],  # Only last operation is uncertain
        [5, 7, 2],                # All deterministic
        [6, 6, 8]                 # All deterministic
    ],
    'name': 'Test_3x3_Partial_Interval',
    'has_intervals': True,
    'description': '3x3 problem with only one uncertain operation (for edge case testing)'
}


def get_test_3x3_interval():
    """
    Obtiene el problema de prueba 3x3 con intervalos.
    
    Returns:
        Diccionario con los datos del problema 3x3 con intervalos
    """
    return TEST_3X3_INTERVAL


def get_test_3x3_deterministic():
    """
    Obtiene el problema de prueba 3x3 determinístico.
    
    Returns:
        Diccionario con los datos del problema 3x3 determinístico
    """
    return TEST_3X3_DETERMINISTIC


def get_test_3x3_partial_interval():
    """
    Obtiene el problema de prueba 3x3 con incertidumbre parcial.
    
    Returns:
        Diccionario con los datos del problema 3x3 con incertidumbre parcial
    """
    return TEST_3X3_PARTIAL_INTERVAL


def get_all_test_3x3_variants():
    """
    Obtiene todas las variantes del problema 3x3.
    
    Returns:
        Lista de diccionarios con las tres variantes
    """
    return [
        TEST_3X3_INTERVAL,
        TEST_3X3_DETERMINISTIC,
        TEST_3X3_PARTIAL_INTERVAL
    ]


# Example usage and expected behavior
if __name__ == '__main__':
    """
    Ejemplo de uso y validación básica.
    """
    print("=" * 60)
    print("3x3 Test Problems")
    print("=" * 60)
    
    # Interval version
    interval_prob = get_test_3x3_interval()
    print(f"\n{interval_prob['name']}:")
    print(f"  Jobs: {interval_prob['num_jobs']}, Machines: {interval_prob['num_machines']}")
    print(f"  Has intervals: {interval_prob['has_intervals']}")
    print(f"  Sample duration (Job 0, Op 0): {interval_prob['durations'][0][0]}")
    
    # Deterministic version
    det_prob = get_test_3x3_deterministic()
    print(f"\n{det_prob['name']}:")
    print(f"  Jobs: {det_prob['num_jobs']}, Machines: {det_prob['num_machines']}")
    print(f"  Has intervals: {det_prob['has_intervals']}")
    print(f"  Sample duration (Job 0, Op 0): {det_prob['durations'][0][0]}")
    
    # Partial interval version
    partial_prob = get_test_3x3_partial_interval()
    print(f"\n{partial_prob['name']}:")
    print(f"  Jobs: {partial_prob['num_jobs']}, Machines: {partial_prob['num_machines']}")
    print(f"  Has intervals: {partial_prob['has_intervals']}")
    print(f"  Sample durations (Job 0):")
    for i, dur in enumerate(partial_prob['durations'][0]):
        print(f"    Operation {i}: {dur}")
    
    print("\n" + "=" * 60)
    print("Validation complete!")
    print("=" * 60)
