"""
Problema INT__TAI15_15_04.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI15_15_04_F_15_01_INTERVAL_DATA = {
    'num_jobs': 15,
    'num_machines': 15,
    'problem_id': 'int__tai15_15_04.F.15_01_interval',
    'sequences': [
        [3, 7, 6, 14, 9, 8, 5, 4, 10, 1, 0, 12, 11, 2, 13],
        [1, 11, 0, 5, 8, 13, 3, 10, 9, 2, 12, 6, 4, 7, 14],
        [7, 3, 8, 11, 0, 4, 9, 13, 1, 10, 6, 5, 14, 12, 2],
        [6, 11, 5, 13, 3, 2, 1, 4, 9, 12, 8, 0, 14, 7, 10],
        [1, 11, 6, 5, 8, 7, 12, 9, 2, 14, 13, 3, 0, 4, 10],
        [11, 2, 12, 1, 14, 0, 6, 9, 3, 13, 7, 10, 4, 5, 8],
        [14, 7, 11, 0, 12, 8, 9, 10, 3, 13, 4, 1, 2, 6, 5],
        [7, 4, 13, 5, 14, 11, 2, 12, 6, 1, 0, 10, 9, 3, 8],
        [7, 4, 14, 10, 3, 0, 13, 8, 1, 2, 6, 12, 11, 9, 5],
        [2, 12, 10, 3, 6, 5, 14, 9, 13, 4, 0, 11, 7, 8, 1],
        [11, 9, 3, 7, 6, 4, 0, 2, 5, 1, 10, 8, 13, 12, 14],
        [0, 4, 1, 9, 2, 11, 13, 10, 7, 6, 8, 12, 14, 3, 5],
        [6, 0, 4, 10, 2, 14, 9, 13, 11, 12, 1, 8, 5, 3, 7],
        [5, 10, 13, 2, 7, 4, 8, 6, 9, 0, 12, 11, 1, 14, 3],
        [11, 2, 0, 4, 14, 5, 9, 10, 6, 12, 8, 1, 7, 3, 13],
    ],
    'durations': [
        # Job 0
        [Interval(71, 73), Interval(51, 51), Interval(36, 48), Interval(30, 32), Interval(56, 66),
         Interval(40, 52), Interval(88, 88), Interval(31, 35), Interval(27, 27), Interval(75, 95),
         Interval(61, 79), Interval(53, 59), Interval(60, 80), Interval(50, 50), Interval(23, 27)],
        # Job 1
        [Interval(17, 21), Interval(77, 81), Interval(73, 85), Interval(40, 54), Interval(37, 43),
         Interval(66, 68), Interval(37, 49), Interval(63, 67), Interval(75, 93), Interval(55, 67),
         Interval(28, 32), Interval(52, 60), Interval(17, 21), Interval(78, 104), Interval(66, 70)],
        # Job 2
        [Interval(85, 103), Interval(6, 8), Interval(2, 2), Interval(87, 103), Interval(52, 68),
         Interval(72, 92), Interval(70, 82), Interval(33, 39), Interval(7, 9), Interval(80, 90),
         Interval(7, 7), Interval(39, 49), Interval(2, 2), Interval(62, 82), Interval(81, 101)],
        # Job 3
        [Interval(50, 66), Interval(65, 69), Interval(72, 96), Interval(31, 37), Interval(18, 20),
         Interval(18, 20), Interval(93, 95), Interval(38, 44), Interval(90, 106), Interval(96, 96),
         Interval(25, 25), Interval(38, 42), Interval(69, 79), Interval(86, 90), Interval(68, 80)],
        # Job 4
        [Interval(39, 51), Interval(57, 63), Interval(8, 8), Interval(29, 29), Interval(29, 35),
         Interval(42, 42), Interval(22, 28), Interval(4, 4), Interval(64, 78), Interval(79, 79),
         Interval(82, 104), Interval(25, 31), Interval(30, 30), Interval(15, 19), Interval(37, 49)],
        # Job 5
        [Interval(74, 94), Interval(48, 64), Interval(43, 49), Interval(80, 106), Interval(64, 68),
         Interval(78, 90), Interval(39, 41), Interval(4, 4), Interval(13, 17), Interval(15, 15),
         Interval(53, 55), Interval(39, 39), Interval(67, 87), Interval(54, 56), Interval(29, 33)],
        # Job 6
        [Interval(57, 73), Interval(81, 101), Interval(15, 19), Interval(40, 54), Interval(72, 82),
         Interval(59, 77), Interval(56, 68), Interval(22, 22), Interval(72, 72), Interval(47, 47),
         Interval(33, 43), Interval(7, 7), Interval(10, 12), Interval(22, 22), Interval(60, 66)],
        # Job 7
        [Interval(11, 13), Interval(20, 22), Interval(59, 61), Interval(41, 43), Interval(21, 23),
         Interval(84, 84), Interval(59, 61), Interval(46, 58), Interval(23, 27), Interval(51, 55),
         Interval(49, 57), Interval(56, 56), Interval(25, 33), Interval(76, 90), Interval(30, 34)],
        # Job 8
        [Interval(43, 53), Interval(24, 32), Interval(61, 79), Interval(24, 28), Interval(68, 68),
         Interval(4, 4), Interval(19, 19), Interval(82, 102), Interval(21, 27), Interval(48, 60),
         Interval(52, 62), Interval(43, 51), Interval(75, 93), Interval(84, 86), Interval(82, 108)],
        # Job 9
        [Interval(36, 36), Interval(33, 35), Interval(61, 69), Interval(61, 67), Interval(26, 34),
         Interval(37, 45), Interval(46, 60), Interval(63, 85), Interval(40, 48), Interval(13, 13),
         Interval(40, 42), Interval(6, 6), Interval(28, 36), Interval(93, 95), Interval(36, 38)],
        # Job 10
        [Interval(58, 66), Interval(8, 10), Interval(76, 102), Interval(36, 38), Interval(27, 29),
         Interval(22, 24), Interval(13, 13), Interval(58, 62), Interval(42, 50), Interval(93, 95),
         Interval(82, 88), Interval(65, 79), Interval(16, 20), Interval(69, 89), Interval(11, 11)],
        # Job 11
        [Interval(65, 83), Interval(61, 61), Interval(42, 44), Interval(24, 28), Interval(91, 103),
         Interval(57, 67), Interval(37, 43), Interval(52, 68), Interval(58, 66), Interval(69, 87),
         Interval(39, 45), Interval(8, 8), Interval(19, 23), Interval(11, 11), Interval(67, 73)],
        # Job 12
        [Interval(8, 10), Interval(21, 23), Interval(8, 10), Interval(7, 9), Interval(54, 54),
         Interval(29, 35), Interval(82, 102), Interval(71, 81), Interval(2, 2), Interval(60, 66),
         Interval(55, 71), Interval(86, 110), Interval(42, 42), Interval(11, 13), Interval(35, 47)],
        # Job 13
        [Interval(63, 71), Interval(7, 7), Interval(90, 92), Interval(48, 56), Interval(75, 99),
         Interval(4, 4), Interval(1, 1), Interval(51, 61), Interval(72, 92), Interval(46, 48),
         Interval(31, 39), Interval(7, 9), Interval(82, 102), Interval(38, 40), Interval(11, 11)],
        # Job 14
        [Interval(40, 48), Interval(23, 25), Interval(21, 27), Interval(13, 15), Interval(29, 39),
         Interval(55, 59), Interval(29, 31), Interval(61, 67), Interval(4, 4), Interval(13, 15),
         Interval(67, 71), Interval(81, 109), Interval(19, 25), Interval(54, 66), Interval(52, 70)],
    ],
    'name': 'INT__TAI15_15_04.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai15_15_04_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI15_15_04.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI15_15_04.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI15_15_04_F_15_01_INTERVAL_DATA
