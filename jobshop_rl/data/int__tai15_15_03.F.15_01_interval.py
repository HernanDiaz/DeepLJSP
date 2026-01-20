"""
Problema INT__TAI15_15_03.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI15_15_03_F_15_01_INTERVAL_DATA = {
    'num_jobs': 15,
    'num_machines': 15,
    'problem_id': 'int__tai15_15_03.F.15_01_interval',
    'sequences': [
        [7, 11, 8, 3, 12, 1, 13, 0, 14, 6, 9, 4, 2, 10, 5],
        [12, 1, 11, 9, 6, 3, 2, 4, 5, 8, 13, 14, 10, 0, 7],
        [1, 2, 9, 0, 3, 5, 8, 4, 14, 10, 12, 13, 7, 6, 11],
        [13, 10, 6, 2, 14, 7, 4, 11, 0, 5, 9, 3, 8, 1, 12],
        [1, 8, 4, 14, 6, 5, 3, 2, 9, 10, 13, 7, 11, 0, 12],
        [5, 14, 2, 12, 10, 1, 11, 4, 6, 9, 0, 13, 8, 3, 7],
        [5, 2, 0, 1, 8, 14, 11, 10, 7, 9, 6, 12, 4, 13, 3],
        [4, 7, 10, 1, 9, 8, 2, 14, 11, 3, 5, 6, 13, 12, 0],
        [14, 11, 0, 9, 10, 5, 3, 12, 8, 13, 6, 1, 7, 2, 4],
        [9, 0, 3, 10, 12, 13, 5, 1, 6, 14, 8, 11, 2, 7, 4],
        [7, 2, 1, 12, 3, 14, 4, 6, 5, 9, 8, 13, 10, 0, 11],
        [0, 8, 14, 12, 9, 5, 6, 10, 7, 11, 3, 4, 1, 13, 2],
        [8, 12, 10, 11, 14, 3, 6, 1, 4, 5, 0, 9, 13, 2, 7],
        [13, 2, 11, 0, 14, 10, 3, 1, 12, 4, 5, 6, 7, 9, 8],
        [1, 13, 0, 11, 2, 10, 4, 8, 3, 5, 7, 6, 9, 12, 14],
    ],
    'durations': [
        # Job 0
        [Interval(68, 70), Interval(80, 82), Interval(69, 93), Interval(59, 65), Interval(74, 86),
         Interval(3, 3), Interval(33, 43), Interval(62, 62), Interval(49, 59), Interval(66, 66),
         Interval(77, 99), Interval(71, 93), Interval(3, 3), Interval(12, 12), Interval(75, 101)],
        # Job 1
        [Interval(83, 83), Interval(46, 56), Interval(42, 52), Interval(15, 15), Interval(82, 96),
         Interval(65, 87), Interval(49, 55), Interval(18, 18), Interval(19, 25), Interval(82, 88),
         Interval(24, 28), Interval(27, 33), Interval(5, 5), Interval(83, 95), Interval(21, 23)],
        # Job 2
        [Interval(56, 68), Interval(40, 54), Interval(90, 96), Interval(49, 59), Interval(34, 42),
         Interval(71, 85), Interval(63, 79), Interval(84, 108), Interval(18, 20), Interval(31, 35),
         Interval(40, 48), Interval(67, 75), Interval(87, 93), Interval(8, 10), Interval(18, 24)],
        # Job 3
        [Interval(30, 36), Interval(70, 94), Interval(77, 83), Interval(26, 34), Interval(88, 104),
         Interval(29, 33), Interval(10, 12), Interval(26, 26), Interval(38, 44), Interval(50, 60),
         Interval(12, 12), Interval(10, 10), Interval(87, 97), Interval(3, 3), Interval(70, 80)],
        # Job 4
        [Interval(36, 36), Interval(45, 53), Interval(9, 11), Interval(41, 45), Interval(65, 73),
         Interval(71, 73), Interval(17, 21), Interval(65, 65), Interval(32, 42), Interval(52, 62),
         Interval(32, 32), Interval(10, 12), Interval(65, 81), Interval(87, 91), Interval(11, 13)],
        # Job 5
        [Interval(71, 95), Interval(29, 35), Interval(6, 6), Interval(12, 14), Interval(80, 94),
         Interval(81, 107), Interval(35, 37), Interval(70, 82), Interval(45, 47), Interval(26, 34),
         Interval(54, 58), Interval(61, 63), Interval(32, 32), Interval(46, 58), Interval(70, 74)],
        # Job 6
        [Interval(27, 31), Interval(68, 88), Interval(18, 24), Interval(23, 31), Interval(15, 19),
         Interval(40, 46), Interval(12, 16), Interval(13, 17), Interval(16, 16), Interval(49, 49),
         Interval(72, 72), Interval(17, 21), Interval(99, 99), Interval(34, 42), Interval(64, 64)],
        # Job 7
        [Interval(12, 12), Interval(63, 85), Interval(4, 4), Interval(3, 3), Interval(14, 16),
         Interval(61, 63), Interval(49, 51), Interval(36, 40), Interval(49, 49), Interval(25, 25),
         Interval(16, 20), Interval(50, 60), Interval(5, 5), Interval(67, 75), Interval(25, 29)],
        # Job 8
        [Interval(69, 69), Interval(12, 14), Interval(31, 35), Interval(44, 50), Interval(78, 94),
         Interval(27, 35), Interval(85, 109), Interval(43, 53), Interval(25, 25), Interval(40, 40),
         Interval(84, 104), Interval(19, 25), Interval(54, 68), Interval(54, 64), Interval(15, 17)],
        # Job 9
        [Interval(24, 30), Interval(4, 4), Interval(35, 35), Interval(68, 92), Interval(49, 49),
         Interval(44, 48), Interval(79, 89), Interval(44, 48), Interval(82, 110), Interval(66, 78),
         Interval(16, 20), Interval(20, 26), Interval(87, 105), Interval(73, 75), Interval(23, 23)],
        # Job 10
        [Interval(32, 40), Interval(17, 17), Interval(79, 83), Interval(62, 72), Interval(41, 53),
         Interval(5, 5), Interval(44, 58), Interval(23, 23), Interval(78, 86), Interval(33, 37),
         Interval(91, 101), Interval(7, 7), Interval(49, 59), Interval(91, 93), Interval(37, 39)],
        # Job 11
        [Interval(70, 86), Interval(50, 66), Interval(54, 70), Interval(41, 45), Interval(1, 1),
         Interval(50, 62), Interval(76, 76), Interval(48, 50), Interval(71, 89), Interval(25, 27),
         Interval(73, 85), Interval(9, 9), Interval(21, 27), Interval(23, 25), Interval(37, 47)],
        # Job 12
        [Interval(36, 40), Interval(81, 91), Interval(35, 41), Interval(36, 40), Interval(79, 87),
         Interval(32, 40), Interval(11, 11), Interval(16, 18), Interval(90, 108), Interval(14, 14),
         Interval(52, 62), Interval(57, 71), Interval(55, 61), Interval(91, 101), Interval(15, 19)],
        # Job 13
        [Interval(9, 11), Interval(85, 87), Interval(84, 102), Interval(55, 71), Interval(58, 64),
         Interval(61, 63), Interval(74, 76), Interval(83, 97), Interval(34, 46), Interval(70, 84),
         Interval(7, 9), Interval(27, 27), Interval(86, 106), Interval(60, 78), Interval(57, 71)],
        # Job 14
        [Interval(70, 76), Interval(12, 12), Interval(13, 15), Interval(68, 74), Interval(3, 3),
         Interval(41, 53), Interval(77, 91), Interval(73, 95), Interval(52, 54), Interval(57, 59),
         Interval(90, 100), Interval(79, 95), Interval(87, 93), Interval(58, 78), Interval(65, 85)],
    ],
    'name': 'INT__TAI15_15_03.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai15_15_03_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI15_15_03.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI15_15_03.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI15_15_03_F_15_01_INTERVAL_DATA
