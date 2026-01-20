"""
Problema INT__TAI15_15_01.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI15_15_01_F_15_01_INTERVAL_DATA = {
    'num_jobs': 15,
    'num_machines': 15,
    'problem_id': 'int__tai15_15_01.F.15_01_interval',
    'sequences': [
        [6, 12, 4, 7, 3, 2, 10, 11, 8, 14, 9, 13, 5, 0, 1],
        [4, 5, 7, 14, 13, 8, 11, 9, 6, 10, 0, 3, 12, 1, 2],
        [1, 8, 9, 12, 6, 11, 13, 5, 0, 2, 7, 10, 4, 3, 14],
        [5, 2, 9, 6, 10, 0, 13, 4, 7, 14, 11, 8, 12, 1, 3],
        [7, 8, 6, 10, 4, 9, 2, 14, 12, 5, 1, 13, 11, 0, 3],
        [5, 3, 12, 13, 11, 4, 14, 7, 2, 1, 10, 0, 9, 6, 8],
        [12, 3, 7, 8, 14, 6, 1, 11, 4, 5, 2, 10, 0, 13, 9],
        [11, 5, 0, 7, 12, 13, 14, 1, 2, 8, 4, 3, 9, 6, 10],
        [10, 11, 6, 14, 0, 1, 2, 5, 12, 4, 8, 7, 9, 13, 3],
        [6, 11, 9, 2, 8, 0, 13, 3, 10, 7, 1, 12, 14, 4, 5],
        [4, 7, 13, 0, 5, 12, 6, 8, 14, 10, 3, 1, 11, 9, 2],
        [2, 14, 0, 12, 6, 10, 7, 5, 8, 9, 13, 1, 3, 11, 4],
        [5, 8, 10, 2, 3, 6, 9, 0, 13, 4, 1, 11, 12, 7, 14],
        [8, 14, 4, 13, 5, 6, 9, 1, 12, 7, 11, 10, 3, 2, 0],
        [10, 8, 12, 6, 4, 1, 13, 14, 11, 0, 7, 3, 2, 9, 5],
    ],
    'durations': [
        # Job 0
        [Interval(93, 95), Interval(66, 66), Interval(9, 11), Interval(51, 55), Interval(24, 28),
         Interval(13, 17), Interval(65, 65), Interval(75, 89), Interval(10, 10), Interval(23, 31),
         Interval(82, 104), Interval(87, 97), Interval(82, 110), Interval(70, 70), Interval(74, 92)],
        # Job 1
        [Interval(66, 82), Interval(30, 32), Interval(81, 95), Interval(44, 58), Interval(53, 61),
         Interval(77, 79), Interval(7, 9), Interval(7, 7), Interval(81, 101), Interval(72, 86),
         Interval(17, 19), Interval(48, 54), Interval(16, 20), Interval(85, 113), Interval(32, 34)],
        # Job 2
        [Interval(4, 4), Interval(74, 90), Interval(36, 44), Interval(79, 93), Interval(44, 56),
         Interval(47, 61), Interval(19, 23), Interval(6, 6), Interval(50, 58), Interval(61, 75),
         Interval(77, 87), Interval(19, 21), Interval(35, 43), Interval(30, 40), Interval(60, 76)],
        # Job 3
        [Interval(63, 83), Interval(22, 24), Interval(26, 34), Interval(28, 32), Interval(49, 57),
         Interval(85, 103), Interval(57, 59), Interval(86, 100), Interval(30, 34), Interval(91, 91),
         Interval(30, 30), Interval(53, 59), Interval(25, 29), Interval(90, 94), Interval(8, 10)],
        # Job 4
        [Interval(67, 89), Interval(22, 24), Interval(20, 22), Interval(59, 61), Interval(32, 40),
         Interval(29, 29), Interval(82, 108), Interval(90, 108), Interval(79, 79), Interval(67, 85),
         Interval(83, 103), Interval(41, 43), Interval(47, 57), Interval(36, 48), Interval(85, 107)],
        # Job 5
        [Interval(25, 33), Interval(56, 66), Interval(75, 101), Interval(68, 72), Interval(15, 17),
         Interval(30, 32), Interval(56, 74), Interval(79, 87), Interval(76, 80), Interval(26, 26),
         Interval(44, 56), Interval(84, 90), Interval(57, 67), Interval(12, 16), Interval(27, 33)],
        # Job 6
        [Interval(16, 20), Interval(65, 85), Interval(19, 21), Interval(4, 4), Interval(80, 102),
         Interval(61, 75), Interval(19, 19), Interval(54, 54), Interval(85, 85), Interval(63, 83),
         Interval(43, 43), Interval(22, 26), Interval(37, 37), Interval(83, 91), Interval(57, 75)],
        # Job 7
        [Interval(31, 33), Interval(51, 53), Interval(9, 9), Interval(46, 52), Interval(61, 61),
         Interval(34, 36), Interval(87, 111), Interval(56, 68), Interval(6, 6), Interval(59, 65),
         Interval(6, 8), Interval(80, 80), Interval(3, 3), Interval(50, 64), Interval(6, 8)],
        # Job 8
        [Interval(80, 90), Interval(27, 33), Interval(82, 110), Interval(80, 102), Interval(12, 14),
         Interval(87, 87), Interval(82, 82), Interval(74, 92), Interval(68, 88), Interval(50, 62),
         Interval(78, 92), Interval(7, 9), Interval(59, 73), Interval(87, 89), Interval(13, 17)],
        # Job 9
        [Interval(5, 5), Interval(59, 59), Interval(29, 31), Interval(56, 64), Interval(39, 43),
         Interval(15, 19), Interval(60, 72), Interval(76, 102), Interval(67, 89), Interval(79, 97),
         Interval(68, 70), Interval(44, 46), Interval(72, 92), Interval(6, 6), Interval(13, 13)],
        # Job 10
        [Interval(87, 93), Interval(25, 29), Interval(1, 1), Interval(7, 9), Interval(78, 104),
         Interval(78, 82), Interval(85, 93), Interval(46, 52), Interval(31, 33), Interval(27, 29),
         Interval(82, 98), Interval(92, 94), Interval(6, 6), Interval(34, 36), Interval(66, 80)],
        # Job 11
        [Interval(40, 54), Interval(37, 49), Interval(72, 78), Interval(7, 9), Interval(51, 51),
         Interval(3, 3), Interval(82, 86), Interval(30, 38), Interval(26, 30), Interval(55, 65),
         Interval(64, 74), Interval(40, 50), Interval(63, 71), Interval(52, 64), Interval(81, 93)],
        # Job 12
        [Interval(61, 69), Interval(56, 68), Interval(92, 102), Interval(19, 21), Interval(28, 34),
         Interval(31, 35), Interval(30, 36), Interval(70, 84), Interval(50, 50), Interval(72, 88),
         Interval(42, 54), Interval(85, 95), Interval(71, 79), Interval(83, 109), Interval(38, 50)],
        # Job 13
        [Interval(28, 28), Interval(19, 23), Interval(45, 57), Interval(71, 79), Interval(17, 17),
         Interval(88, 90), Interval(55, 63), Interval(48, 64), Interval(57, 69), Interval(16, 20),
         Interval(17, 17), Interval(27, 33), Interval(14, 18), Interval(6, 8), Interval(34, 36)],
        # Job 14
        [Interval(55, 59), Interval(15, 17), Interval(40, 44), Interval(30, 38), Interval(34, 40),
         Interval(23, 29), Interval(66, 70), Interval(71, 75), Interval(5, 5), Interval(8, 8),
         Interval(11, 13), Interval(84, 90), Interval(71, 95), Interval(17, 23), Interval(88, 106)],
    ],
    'name': 'INT__TAI15_15_01.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai15_15_01_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI15_15_01.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI15_15_01.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI15_15_01_F_15_01_INTERVAL_DATA
