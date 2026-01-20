"""
Problema INT__TAI15_15_07.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI15_15_07_F_15_01_INTERVAL_DATA = {
    'num_jobs': 15,
    'num_machines': 15,
    'problem_id': 'int__tai15_15_07.F.15_01_interval',
    'sequences': [
        [13, 12, 7, 0, 5, 11, 9, 10, 1, 2, 3, 14, 4, 6, 8],
        [2, 1, 8, 14, 13, 0, 5, 11, 9, 12, 10, 7, 3, 4, 6],
        [0, 3, 1, 7, 4, 8, 14, 5, 6, 2, 13, 12, 9, 10, 11],
        [9, 11, 0, 7, 12, 14, 6, 1, 13, 10, 4, 5, 3, 2, 8],
        [8, 13, 5, 10, 9, 14, 12, 2, 3, 0, 6, 11, 7, 4, 1],
        [12, 13, 14, 9, 5, 1, 6, 7, 0, 3, 8, 10, 4, 11, 2],
        [9, 0, 5, 4, 12, 14, 6, 1, 3, 8, 13, 11, 2, 10, 7],
        [12, 1, 9, 14, 6, 10, 2, 7, 4, 11, 13, 5, 3, 8, 0],
        [6, 5, 12, 4, 1, 14, 9, 0, 7, 8, 10, 13, 2, 11, 3],
        [8, 3, 5, 4, 1, 10, 7, 9, 13, 2, 0, 11, 6, 12, 14],
        [4, 2, 1, 0, 14, 10, 9, 6, 11, 12, 3, 8, 7, 13, 5],
        [8, 3, 13, 14, 2, 11, 5, 4, 9, 12, 10, 7, 1, 0, 6],
        [7, 1, 10, 4, 0, 8, 12, 6, 13, 2, 3, 9, 11, 14, 5],
        [8, 11, 3, 7, 1, 12, 6, 4, 10, 13, 2, 5, 14, 9, 0],
        [5, 13, 14, 6, 9, 11, 7, 2, 12, 8, 3, 4, 10, 1, 0],
    ],
    'durations': [
        # Job 0
        [Interval(52, 52), Interval(19, 19), Interval(6, 6), Interval(17, 23), Interval(1, 1),
         Interval(25, 27), Interval(83, 97), Interval(38, 50), Interval(27, 27), Interval(17, 19),
         Interval(51, 51), Interval(70, 90), Interval(9, 11), Interval(48, 54), Interval(35, 47)],
        # Job 1
        [Interval(44, 44), Interval(76, 94), Interval(2, 2), Interval(70, 86), Interval(83, 89),
         Interval(81, 95), Interval(52, 70), Interval(19, 21), Interval(56, 56), Interval(11, 13),
         Interval(67, 71), Interval(30, 38), Interval(50, 60), Interval(32, 36), Interval(78, 90)],
        # Job 2
        [Interval(56, 68), Interval(62, 82), Interval(72, 76), Interval(57, 69), Interval(85, 105),
         Interval(27, 31), Interval(21, 27), Interval(30, 38), Interval(82, 96), Interval(77, 89),
         Interval(81, 99), Interval(25, 27), Interval(94, 102), Interval(58, 72), Interval(27, 35)],
        # Job 3
        [Interval(9, 11), Interval(13, 17), Interval(90, 96), Interval(68, 90), Interval(71, 83),
         Interval(56, 66), Interval(1, 1), Interval(44, 52), Interval(22, 22), Interval(25, 29),
         Interval(19, 23), Interval(17, 17), Interval(45, 45), Interval(90, 102), Interval(11, 11)],
        # Job 4
        [Interval(81, 85), Interval(48, 56), Interval(60, 80), Interval(74, 82), Interval(7, 7),
         Interval(28, 28), Interval(86, 108), Interval(52, 52), Interval(25, 33), Interval(73, 89),
         Interval(60, 60), Interval(80, 102), Interval(71, 89), Interval(53, 55), Interval(31, 39)],
        # Job 5
        [Interval(3, 3), Interval(27, 35), Interval(87, 109), Interval(83, 111), Interval(71, 83),
         Interval(34, 44), Interval(40, 42), Interval(9, 11), Interval(9, 9), Interval(80, 106),
         Interval(7, 7), Interval(48, 50), Interval(20, 20), Interval(40, 50), Interval(58, 60)],
        # Job 6
        [Interval(26, 30), Interval(82, 104), Interval(4, 4), Interval(45, 57), Interval(57, 77),
         Interval(5, 5), Interval(16, 20), Interval(49, 55), Interval(41, 53), Interval(19, 23),
         Interval(49, 49), Interval(63, 63), Interval(96, 96), Interval(73, 97), Interval(90, 90)],
        # Job 7
        [Interval(23, 27), Interval(82, 82), Interval(56, 60), Interval(13, 17), Interval(64, 70),
         Interval(49, 51), Interval(64, 68), Interval(87, 97), Interval(56, 56), Interval(80, 84),
         Interval(50, 64), Interval(15, 17), Interval(32, 36), Interval(91, 107), Interval(61, 61)],
        # Job 8
        [Interval(71, 93), Interval(29, 33), Interval(21, 23), Interval(15, 17), Interval(74, 100),
         Interval(42, 54), Interval(53, 65), Interval(63, 63), Interval(29, 29), Interval(89, 109),
         Interval(41, 55), Interval(32, 40), Interval(83, 99), Interval(55, 67), Interval(53, 65)],
        # Job 9
        [Interval(28, 28), Interval(22, 28), Interval(69, 69), Interval(62, 68), Interval(58, 66),
         Interval(55, 59), Interval(83, 111), Interval(28, 34), Interval(13, 17), Interval(22, 28),
         Interval(75, 91), Interval(97, 99), Interval(54, 56), Interval(58, 74), Interval(31, 31)],
        # Job 10
        [Interval(20, 20), Interval(92, 106), Interval(12, 14), Interval(75, 101), Interval(25, 25),
         Interval(71, 79), Interval(84, 96), Interval(80, 88), Interval(67, 73), Interval(37, 45),
         Interval(17, 17), Interval(52, 56), Interval(57, 69), Interval(1, 1), Interval(81, 109)],
        # Job 11
        [Interval(52, 66), Interval(21, 23), Interval(41, 51), Interval(10, 10), Interval(1, 1),
         Interval(21, 21), Interval(3, 3), Interval(75, 93), Interval(87, 99), Interval(55, 63),
         Interval(73, 83), Interval(64, 82), Interval(56, 62), Interval(37, 47), Interval(59, 67)],
        # Job 12
        [Interval(68, 76), Interval(72, 88), Interval(12, 12), Interval(53, 59), Interval(20, 24),
         Interval(8, 8), Interval(85, 101), Interval(24, 30), Interval(17, 17), Interval(35, 41),
         Interval(23, 29), Interval(48, 54), Interval(41, 45), Interval(69, 91), Interval(82, 106)],
        # Job 13
        [Interval(71, 73), Interval(70, 86), Interval(25, 33), Interval(85, 95), Interval(45, 47),
         Interval(46, 46), Interval(40, 46), Interval(65, 85), Interval(82, 98), Interval(26, 32),
         Interval(8, 8), Interval(82, 102), Interval(14, 18), Interval(55, 69), Interval(6, 6)],
        # Job 14
        [Interval(85, 93), Interval(42, 46), Interval(37, 45), Interval(31, 33), Interval(9, 11),
         Interval(78, 92), Interval(14, 18), Interval(23, 23), Interval(89, 93), Interval(44, 48),
         Interval(32, 38), Interval(17, 17), Interval(80, 106), Interval(39, 51), Interval(85, 101)],
    ],
    'name': 'INT__TAI15_15_07.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai15_15_07_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI15_15_07.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI15_15_07.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI15_15_07_F_15_01_INTERVAL_DATA
