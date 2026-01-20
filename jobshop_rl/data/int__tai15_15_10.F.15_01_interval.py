"""
Problema INT__TAI15_15_10.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI15_15_10_F_15_01_INTERVAL_DATA = {
    'num_jobs': 15,
    'num_machines': 15,
    'problem_id': 'int__tai15_15_10.F.15_01_interval',
    'sequences': [
        [8, 2, 7, 14, 12, 0, 4, 3, 13, 5, 9, 10, 6, 1, 11],
        [2, 8, 6, 4, 11, 0, 9, 7, 5, 3, 1, 10, 13, 14, 12],
        [5, 11, 8, 14, 12, 1, 4, 9, 10, 6, 13, 0, 2, 3, 7],
        [9, 13, 8, 6, 12, 5, 10, 2, 1, 0, 14, 11, 3, 4, 7],
        [8, 10, 3, 13, 14, 5, 4, 0, 12, 11, 9, 6, 2, 1, 7],
        [7, 2, 9, 5, 10, 4, 3, 1, 11, 8, 6, 14, 13, 0, 12],
        [2, 10, 1, 12, 14, 3, 0, 4, 9, 5, 11, 13, 7, 8, 6],
        [13, 6, 11, 12, 8, 7, 14, 5, 3, 4, 0, 10, 2, 1, 9],
        [8, 4, 6, 7, 0, 11, 13, 12, 2, 3, 10, 1, 5, 14, 9],
        [2, 6, 12, 9, 8, 11, 1, 3, 13, 4, 10, 5, 0, 7, 14],
        [0, 9, 4, 8, 10, 2, 11, 12, 14, 6, 3, 7, 5, 1, 13],
        [8, 1, 12, 5, 7, 10, 9, 4, 11, 6, 13, 2, 14, 0, 3],
        [13, 14, 2, 9, 7, 8, 12, 4, 10, 6, 1, 0, 5, 11, 3],
        [1, 0, 12, 2, 13, 8, 3, 14, 4, 7, 6, 9, 11, 10, 5],
        [3, 13, 2, 5, 9, 6, 7, 4, 8, 0, 12, 10, 14, 1, 11],
    ],
    'durations': [
        # Job 0
        [Interval(35, 35), Interval(78, 78), Interval(68, 90), Interval(62, 68), Interval(49, 57),
         Interval(12, 16), Interval(93, 93), Interval(64, 76), Interval(14, 14), Interval(79, 101),
         Interval(83, 107), Interval(46, 52), Interval(31, 41), Interval(85, 85), Interval(1, 1)],
        # Job 1
        [Interval(74, 92), Interval(36, 46), Interval(22, 22), Interval(27, 31), Interval(45, 59),
         Interval(66, 76), Interval(16, 16), Interval(80, 106), Interval(52, 56), Interval(56, 70),
         Interval(11, 13), Interval(80, 90), Interval(58, 66), Interval(41, 49), Interval(26, 34)],
        # Job 2
        [Interval(58, 62), Interval(39, 47), Interval(64, 78), Interval(2, 2), Interval(46, 54),
         Interval(33, 41), Interval(76, 96), Interval(74, 88), Interval(55, 65), Interval(52, 62),
         Interval(62, 70), Interval(23, 25), Interval(87, 109), Interval(79, 105), Interval(61, 77)],
        # Job 3
        [Interval(12, 16), Interval(57, 61), Interval(30, 40), Interval(6, 6), Interval(23, 27),
         Interval(53, 61), Interval(1, 1), Interval(40, 48), Interval(93, 95), Interval(28, 32),
         Interval(87, 103), Interval(93, 93), Interval(51, 51), Interval(49, 55), Interval(15, 17)],
        # Job 4
        [Interval(94, 98), Interval(36, 42), Interval(64, 86), Interval(93, 103), Interval(2, 2),
         Interval(36, 40), Interval(68, 70), Interval(29, 35), Interval(95, 95), Interval(55, 71),
         Interval(4, 4), Interval(10, 12), Interval(50, 50), Interval(83, 107), Interval(69, 87)],
        # Job 5
        [Interval(71, 75), Interval(25, 31), Interval(37, 49), Interval(41, 53), Interval(49, 65),
         Interval(81, 95), Interval(29, 37), Interval(13, 13), Interval(6, 8), Interval(47, 51),
         Interval(20, 26), Interval(37, 39), Interval(21, 21), Interval(99, 99), Interval(63, 81)],
        # Job 6
        [Interval(3, 3), Interval(78, 82), Interval(61, 73), Interval(82, 104), Interval(81, 101),
         Interval(27, 35), Interval(45, 59), Interval(60, 68), Interval(72, 94), Interval(2, 2),
         Interval(81, 99), Interval(64, 64), Interval(16, 16), Interval(18, 18), Interval(22, 28)],
        # Job 7
        [Interval(23, 23), Interval(27, 33), Interval(22, 22), Interval(52, 56), Interval(58, 78),
         Interval(60, 66), Interval(87, 91), Interval(92, 98), Interval(5, 5), Interval(35, 39),
         Interval(5, 5), Interval(42, 42), Interval(17, 17), Interval(47, 61), Interval(42, 50)],
        # Job 8
        [Interval(42, 46), Interval(54, 64), Interval(87, 87), Interval(54, 70), Interval(47, 55),
         Interval(52, 58), Interval(3, 3), Interval(36, 44), Interval(23, 29), Interval(16, 20),
         Interval(13, 17), Interval(18, 18), Interval(72, 72), Interval(31, 39), Interval(52, 68)],
        # Job 9
        [Interval(24, 30), Interval(13, 15), Interval(70, 84), Interval(22, 26), Interval(54, 56),
         Interval(57, 77), Interval(59, 59), Interval(19, 19), Interval(27, 31), Interval(32, 34),
         Interval(75, 101), Interval(27, 33), Interval(78, 104), Interval(10, 12), Interval(10, 12)],
        # Job 10
        [Interval(66, 68), Interval(91, 97), Interval(44, 56), Interval(2, 2), Interval(82, 84),
         Interval(19, 19), Interval(27, 31), Interval(33, 41), Interval(50, 66), Interval(31, 33),
         Interval(36, 40), Interval(93, 105), Interval(84, 92), Interval(47, 51), Interval(64, 76)],
        # Job 11
        [Interval(60, 60), Interval(7, 7), Interval(73, 89), Interval(70, 94), Interval(51, 65),
         Interval(80, 86), Interval(14, 18), Interval(1, 1), Interval(69, 69), Interval(7, 7),
         Interval(3, 3), Interval(75, 93), Interval(8, 8), Interval(11, 13), Interval(87, 99)],
        # Job 12
        [Interval(81, 103), Interval(76, 86), Interval(4, 4), Interval(69, 87), Interval(9, 9),
         Interval(73, 83), Interval(68, 82), Interval(5, 5), Interval(47, 53), Interval(8, 8),
         Interval(39, 49), Interval(4, 4), Interval(56, 64), Interval(85, 103), Interval(67, 81)],
        # Job 13
        [Interval(32, 32), Interval(79, 97), Interval(28, 34), Interval(64, 72), Interval(30, 32),
         Interval(9, 11), Interval(39, 51), Interval(74, 76), Interval(73, 91), Interval(45, 57),
         Interval(52, 58), Interval(97, 101), Interval(44, 44), Interval(77, 91), Interval(19, 25)],
        # Job 14
        [Interval(11, 13), Interval(31, 39), Interval(63, 65), Interval(15, 19), Interval(36, 48),
         Interval(41, 51), Interval(62, 68), Interval(71, 77), Interval(88, 104), Interval(27, 29),
         Interval(76, 96), Interval(87, 103), Interval(81, 105), Interval(65, 69), Interval(55, 57)],
    ],
    'name': 'INT__TAI15_15_10.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai15_15_10_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI15_15_10.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI15_15_10.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI15_15_10_F_15_01_INTERVAL_DATA
