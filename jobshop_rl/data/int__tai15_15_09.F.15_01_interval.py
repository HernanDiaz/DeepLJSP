"""
Problema INT__TAI15_15_09.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI15_15_09_F_15_01_INTERVAL_DATA = {
    'num_jobs': 15,
    'num_machines': 15,
    'problem_id': 'int__tai15_15_09.F.15_01_interval',
    'sequences': [
        [3, 13, 11, 4, 2, 9, 10, 6, 12, 7, 5, 14, 8, 1, 0],
        [13, 9, 14, 0, 4, 5, 6, 11, 1, 7, 8, 12, 10, 3, 2],
        [1, 14, 13, 8, 10, 4, 0, 12, 5, 2, 11, 6, 9, 7, 3],
        [14, 5, 4, 3, 10, 7, 1, 11, 13, 6, 9, 12, 2, 8, 0],
        [14, 1, 13, 6, 12, 4, 5, 2, 9, 0, 3, 7, 11, 8, 10],
        [9, 11, 14, 10, 13, 7, 8, 2, 1, 0, 12, 5, 4, 6, 3],
        [3, 7, 11, 8, 4, 9, 1, 12, 10, 6, 0, 14, 5, 2, 13],
        [14, 13, 5, 0, 9, 8, 2, 3, 1, 11, 6, 10, 4, 7, 12],
        [3, 2, 0, 11, 1, 4, 5, 13, 7, 12, 9, 10, 8, 6, 14],
        [14, 9, 11, 13, 1, 5, 3, 4, 0, 12, 6, 2, 8, 10, 7],
        [14, 12, 2, 5, 4, 1, 13, 0, 8, 10, 7, 11, 3, 6, 9],
        [4, 13, 3, 1, 11, 8, 9, 7, 0, 2, 6, 10, 5, 12, 14],
        [11, 9, 1, 8, 12, 14, 2, 10, 7, 0, 13, 6, 3, 5, 4],
        [1, 4, 5, 6, 11, 3, 9, 10, 8, 2, 7, 13, 14, 12, 0],
        [13, 2, 4, 12, 7, 3, 8, 0, 11, 14, 9, 6, 1, 5, 10],
    ],
    'durations': [
        # Job 0
        [Interval(90, 92), Interval(15, 15), Interval(39, 51), Interval(25, 27), Interval(83, 97),
         Interval(46, 60), Interval(7, 7), Interval(72, 84), Interval(94, 94), Interval(7, 9),
         Interval(17, 21), Interval(53, 59), Interval(59, 79), Interval(66, 66), Interval(88, 108)],
        # Job 1
        [Interval(30, 38), Interval(1, 1), Interval(39, 41), Interval(68, 80), Interval(37, 49),
         Interval(68, 78), Interval(95, 97), Interval(68, 92), Interval(84, 90), Interval(70, 86),
         Interval(79, 97), Interval(84, 96), Interval(46, 52), Interval(76, 94), Interval(3, 3)],
        # Job 2
        [Interval(75, 101), Interval(95, 101), Interval(74, 90), Interval(42, 50), Interval(72, 86),
         Interval(61, 77), Interval(83, 107), Interval(38, 44), Interval(36, 42), Interval(11, 13),
         Interval(1, 1), Interval(67, 75), Interval(26, 28), Interval(68, 86), Interval(85, 113)],
        # Job 3
        [Interval(44, 56), Interval(1, 1), Interval(18, 24), Interval(70, 74), Interval(40, 52),
         Interval(18, 22), Interval(57, 67), Interval(30, 36), Interval(78, 80), Interval(51, 61),
         Interval(61, 73), Interval(23, 23), Interval(56, 56), Interval(42, 46), Interval(52, 60)],
        # Job 4
        [Interval(15, 15), Interval(14, 16), Interval(14, 18), Interval(75, 83), Interval(8, 8),
         Interval(72, 74), Interval(77, 95), Interval(52, 52), Interval(69, 89), Interval(56, 68),
         Interval(93, 93), Interval(76, 96), Interval(39, 49), Interval(78, 82), Interval(16, 20)],
        # Job 5
        [Interval(68, 90), Interval(56, 70), Interval(80, 108), Interval(8, 10), Interval(74, 98),
         Interval(86, 92), Interval(11, 13), Interval(64, 68), Interval(47, 63), Interval(67, 73),
         Interval(34, 36), Interval(14, 14), Interval(3, 3), Interval(47, 61), Interval(60, 64)],
        # Job 6
        [Interval(39, 45), Interval(34, 44), Interval(37, 47), Interval(8, 10), Interval(32, 42),
         Interval(24, 26), Interval(68, 88), Interval(68, 84), Interval(16, 16), Interval(38, 38),
         Interval(30, 30), Interval(68, 92), Interval(34, 34), Interval(82, 102), Interval(29, 29)],
        # Job 7
        [Interval(92, 100), Interval(22, 28), Interval(47, 51), Interval(66, 68), Interval(52, 54),
         Interval(19, 21), Interval(52, 52), Interval(29, 29), Interval(45, 57), Interval(32, 38),
         Interval(36, 40), Interval(17, 19), Interval(43, 43), Interval(40, 52), Interval(90, 106)],
        # Job 8
        [Interval(69, 77), Interval(61, 75), Interval(3, 3), Interval(84, 112), Interval(59, 77),
         Interval(7, 9), Interval(15, 15), Interval(88, 88), Interval(65, 79), Interval(17, 23),
         Interval(79, 99), Interval(54, 64), Interval(62, 74), Interval(56, 70), Interval(41, 41)],
        # Job 9
        [Interval(26, 34), Interval(43, 43), Interval(76, 84), Interval(60, 68), Interval(14, 14),
         Interval(6, 6), Interval(31, 41), Interval(80, 96), Interval(61, 81), Interval(44, 58),
         Interval(57, 69), Interval(32, 32), Interval(16, 16), Interval(55, 71), Interval(7, 7)],
        # Job 10
        [Interval(18, 18), Interval(84, 96), Interval(48, 62), Interval(22, 28), Interval(70, 74),
         Interval(88, 96), Interval(82, 94), Interval(66, 72), Interval(85, 93), Interval(76, 90),
         Interval(58, 58), Interval(34, 36), Interval(71, 87), Interval(37, 49), Interval(75, 97)],
        # Job 11
        [Interval(48, 52), Interval(57, 71), Interval(88, 88), Interval(56, 58), Interval(23, 27),
         Interval(69, 77), Interval(17, 19), Interval(4, 4), Interval(64, 74), Interval(35, 45),
         Interval(26, 30), Interval(33, 41), Interval(39, 45), Interval(77, 87), Interval(75, 91)],
        # Job 12
        [Interval(2, 2), Interval(39, 43), Interval(13, 13), Interval(67, 83), Interval(29, 33),
         Interval(60, 72), Interval(65, 79), Interval(66, 66), Interval(87, 105), Interval(40, 50),
         Interval(27, 31), Interval(47, 51), Interval(83, 109), Interval(44, 56), Interval(38, 38)],
        # Job 13
        [Interval(71, 89), Interval(78, 102), Interval(34, 38), Interval(49, 51), Interval(75, 77),
         Interval(14, 16), Interval(27, 35), Interval(81, 97), Interval(77, 97), Interval(54, 56),
         Interval(44, 54), Interval(20, 26), Interval(17, 21), Interval(37, 39), Interval(89, 97)],
        # Job 14
        [Interval(69, 81), Interval(43, 47), Interval(66, 84), Interval(66, 78), Interval(57, 73),
         Interval(6, 6), Interval(16, 16), Interval(24, 24), Interval(23, 25), Interval(40, 48),
         Interval(4, 4), Interval(22, 22), Interval(85, 113), Interval(9, 11), Interval(78, 92)],
    ],
    'name': 'INT__TAI15_15_09.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai15_15_09_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI15_15_09.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI15_15_09.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI15_15_09_F_15_01_INTERVAL_DATA
