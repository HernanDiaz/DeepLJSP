"""
Problema INT__TAI15_15_02.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI15_15_02_F_15_01_INTERVAL_DATA = {
    'num_jobs': 15,
    'num_machines': 15,
    'problem_id': 'int__tai15_15_02.F.15_01_interval',
    'sequences': [
        [9, 14, 4, 13, 10, 3, 7, 8, 0, 5, 1, 2, 12, 6, 11],
        [10, 8, 11, 14, 3, 13, 9, 7, 4, 2, 6, 1, 5, 12, 0],
        [7, 0, 6, 5, 14, 13, 2, 11, 4, 12, 1, 9, 3, 10, 8],
        [9, 11, 14, 0, 1, 8, 5, 10, 12, 4, 13, 3, 6, 7, 2],
        [11, 4, 13, 3, 8, 1, 10, 12, 2, 14, 6, 7, 0, 9, 5],
        [5, 2, 1, 10, 0, 4, 8, 14, 6, 3, 9, 7, 11, 12, 13],
        [5, 10, 13, 0, 9, 8, 1, 11, 14, 7, 12, 2, 6, 4, 3],
        [12, 0, 9, 3, 13, 6, 5, 7, 2, 14, 11, 8, 10, 1, 4],
        [11, 10, 5, 13, 1, 9, 8, 7, 3, 6, 0, 2, 14, 12, 4],
        [2, 14, 3, 10, 6, 1, 0, 13, 11, 4, 5, 8, 7, 12, 9],
        [11, 14, 13, 5, 4, 9, 1, 6, 12, 0, 2, 8, 10, 3, 7],
        [12, 3, 10, 8, 4, 7, 13, 11, 14, 1, 2, 0, 5, 6, 9],
        [8, 13, 5, 0, 11, 9, 4, 12, 1, 10, 6, 2, 7, 14, 3],
        [2, 5, 4, 3, 9, 1, 11, 13, 7, 6, 10, 14, 0, 8, 12],
        [1, 10, 4, 2, 0, 7, 6, 9, 11, 12, 5, 14, 3, 13, 8],
    ],
    'durations': [
        # Job 0
        [Interval(85, 87), Interval(60, 60), Interval(9, 11), Interval(57, 61), Interval(60, 70),
         Interval(81, 107), Interval(71, 71), Interval(23, 27), Interval(98, 98), Interval(43, 55),
         Interval(38, 48), Interval(8, 8), Interval(77, 103), Interval(21, 21), Interval(66, 80)],
        # Job 1
        [Interval(60, 76), Interval(27, 29), Interval(35, 41), Interval(31, 41), Interval(87, 99),
         Interval(35, 35), Interval(32, 42), Interval(27, 29), Interval(55, 69), Interval(78, 94),
         Interval(61, 69), Interval(11, 11), Interval(18, 22), Interval(70, 94), Interval(23, 23)],
        # Job 2
        [Interval(30, 36), Interval(60, 74), Interval(88, 104), Interval(80, 102), Interval(73, 93),
         Interval(74, 88), Interval(55, 65), Interval(79, 97), Interval(19, 21), Interval(60, 64),
         Interval(19, 25), Interval(68, 90), Interval(34, 42), Interval(34, 46), Interval(79, 85)],
        # Job 3
        [Interval(12, 14), Interval(13, 15), Interval(68, 78), Interval(80, 96), Interval(24, 24),
         Interval(15, 17), Interval(72, 84), Interval(70, 70), Interval(53, 53), Interval(64, 72),
         Interval(68, 78), Interval(88, 92), Interval(54, 62), Interval(6, 8), Interval(4, 4)],
        # Job 4
        [Interval(88, 98), Interval(49, 55), Interval(62, 64), Interval(12, 14), Interval(19, 19),
         Interval(35, 47), Interval(64, 78), Interval(59, 59), Interval(17, 21), Interval(53, 67),
         Interval(83, 87), Interval(89, 109), Interval(63, 83), Interval(84, 106), Interval(17, 21)],
        # Job 5
        [Interval(57, 67), Interval(51, 69), Interval(90, 96), Interval(15, 17), Interval(10, 10),
         Interval(62, 82), Interval(84, 92), Interval(67, 71), Interval(58, 58), Interval(36, 46),
         Interval(45, 47), Interval(58, 68), Interval(66, 86), Interval(73, 93), Interval(53, 71)],
        # Job 6
        [Interval(43, 57), Interval(63, 73), Interval(79, 101), Interval(30, 38), Interval(44, 44),
         Interval(5, 5), Interval(8, 8), Interval(25, 25), Interval(60, 80), Interval(53, 53),
         Interval(70, 86), Interval(92, 92), Interval(59, 65), Interval(73, 97), Interval(67, 73)],
        # Job 7
        [Interval(59, 61), Interval(62, 66), Interval(87, 97), Interval(44, 44), Interval(62, 64),
         Interval(80, 102), Interval(19, 23), Interval(1, 1), Interval(91, 101), Interval(18, 20),
         Interval(59, 59), Interval(11, 13), Interval(38, 44), Interval(11, 11), Interval(85, 103)],
        # Job 8
        [Interval(80, 106), Interval(41, 51), Interval(46, 56), Interval(37, 37), Interval(91, 91),
         Interval(80, 100), Interval(55, 71), Interval(35, 45), Interval(62, 74), Interval(12, 14),
         Interval(14, 18), Interval(82, 84), Interval(42, 56), Interval(24, 24), Interval(22, 24)],
        # Job 9
        [Interval(5, 5), Interval(33, 37), Interval(20, 22), Interval(12, 16), Interval(60, 72),
         Interval(3, 3), Interval(6, 6), Interval(84, 112), Interval(54, 72), Interval(58, 70),
         Interval(75, 77), Interval(91, 97), Interval(15, 19), Interval(61, 63), Interval(36, 38)],
        # Job 10
        [Interval(33, 37), Interval(37, 47), Interval(53, 71), Interval(66, 70), Interval(70, 76),
         Interval(25, 29), Interval(50, 54), Interval(38, 40), Interval(37, 45), Interval(25, 25),
         Interval(9, 9), Interval(30, 38), Interval(43, 57), Interval(35, 47), Interval(94, 102)],
        # Job 11
        [Interval(20, 26), Interval(32, 32), Interval(34, 36), Interval(9, 11), Interval(27, 31),
         Interval(62, 74), Interval(19, 21), Interval(7, 9), Interval(55, 61), Interval(55, 69),
         Interval(37, 41), Interval(30, 34), Interval(7, 9), Interval(32, 34), Interval(87, 95)],
        # Job 12
        [Interval(25, 31), Interval(29, 33), Interval(3, 3), Interval(25, 31), Interval(60, 72),
         Interval(59, 59), Interval(22, 26), Interval(40, 50), Interval(76, 86), Interval(8, 8),
         Interval(38, 50), Interval(36, 48), Interval(2, 2), Interval(23, 23), Interval(48, 58)],
        # Job 13
        [Interval(10, 12), Interval(88, 98), Interval(27, 27), Interval(58, 60), Interval(57, 67),
         Interval(20, 26), Interval(21, 25), Interval(6, 8), Interval(75, 79), Interval(57, 71),
         Interval(52, 68), Interval(86, 108), Interval(35, 37), Interval(51, 55), Interval(66, 78)],
        # Job 14
        [Interval(35, 37), Interval(87, 109), Interval(35, 41), Interval(21, 27), Interval(81, 87),
         Interval(46, 48), Interval(68, 76), Interval(1, 1), Interval(83, 99), Interval(82, 88),
         Interval(58, 78), Interval(36, 48), Interval(18, 22), Interval(26, 34), Interval(27, 33)],
    ],
    'name': 'INT__TAI15_15_02.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai15_15_02_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI15_15_02.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI15_15_02.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI15_15_02_F_15_01_INTERVAL_DATA
