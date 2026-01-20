"""
Problema INT__TAI20_15_01.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI20_15_01_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__tai20_15_01.F.15_01_interval',
    'sequences': [
        [3, 11, 14, 1, 10, 2, 4, 7, 0, 12, 5, 9, 6, 13, 8],
        [5, 0, 3, 8, 4, 1, 12, 14, 6, 7, 10, 2, 9, 13, 11],
        [2, 3, 14, 0, 9, 12, 5, 4, 7, 10, 8, 11, 13, 1, 6],
        [8, 10, 1, 13, 3, 4, 14, 9, 2, 5, 11, 7, 0, 6, 12],
        [14, 8, 1, 2, 10, 9, 12, 4, 6, 5, 0, 13, 3, 11, 7],
        [3, 10, 1, 5, 6, 0, 8, 7, 11, 13, 2, 14, 12, 9, 4],
        [2, 10, 1, 12, 8, 0, 7, 6, 14, 13, 4, 3, 5, 9, 11],
        [1, 0, 2, 4, 7, 13, 11, 3, 12, 5, 6, 14, 9, 8, 10],
        [4, 5, 9, 10, 7, 6, 2, 1, 12, 3, 13, 0, 8, 14, 11],
        [1, 4, 3, 10, 14, 0, 6, 13, 11, 8, 5, 12, 7, 9, 2],
        [3, 10, 1, 0, 9, 8, 14, 6, 4, 7, 2, 12, 5, 11, 13],
        [2, 7, 6, 8, 3, 5, 14, 4, 1, 0, 9, 10, 13, 11, 12],
        [0, 7, 14, 8, 12, 10, 9, 3, 6, 1, 4, 2, 11, 13, 5],
        [12, 3, 9, 4, 1, 0, 10, 6, 5, 2, 14, 13, 7, 8, 11],
        [3, 14, 6, 5, 13, 9, 1, 0, 12, 7, 2, 4, 10, 8, 11],
        [5, 14, 6, 12, 8, 2, 4, 9, 11, 13, 3, 1, 7, 0, 10],
        [3, 7, 10, 14, 0, 8, 1, 11, 5, 13, 4, 12, 6, 9, 2],
        [10, 8, 2, 11, 13, 6, 14, 3, 9, 7, 4, 5, 12, 0, 1],
        [3, 2, 12, 13, 1, 6, 14, 5, 4, 8, 9, 11, 0, 10, 7],
        [11, 14, 5, 6, 10, 9, 13, 1, 4, 8, 0, 3, 12, 2, 7],
    ],
    'durations': [
        # Job 0
        [Interval(25, 25), Interval(75, 75), Interval(64, 86), Interval(73, 79), Interval(35, 41),
         Interval(54, 70), Interval(38, 38), Interval(54, 64), Interval(14, 14), Interval(12, 14),
         Interval(41, 51), Interval(30, 32), Interval(49, 65), Interval(92, 92), Interval(3, 3)],
        # Job 1
        [Interval(60, 74), Interval(5, 5), Interval(10, 12), Interval(11, 11), Interval(37, 43),
         Interval(29, 39), Interval(72, 82), Interval(42, 42), Interval(30, 40), Interval(92, 100),
         Interval(20, 24), Interval(50, 60), Interval(20, 22), Interval(27, 31), Interval(14, 18)],
        # Job 2
        [Interval(19, 25), Interval(95, 101), Interval(7, 9), Interval(31, 39), Interval(54, 64),
         Interval(27, 35), Interval(12, 14), Interval(43, 49), Interval(48, 56), Interval(20, 24),
         Interval(17, 19), Interval(19, 19), Interval(57, 71), Interval(25, 33), Interval(62, 78)],
        # Job 3
        [Interval(85, 113), Interval(41, 43), Interval(2, 2), Interval(30, 40), Interval(10, 12),
         Interval(85, 99), Interval(80, 96), Interval(96, 98), Interval(19, 23), Interval(51, 61),
         Interval(17, 17), Interval(43, 43), Interval(25, 29), Interval(18, 20), Interval(23, 23)],
        # Job 4
        [Interval(46, 54), Interval(5, 5), Interval(51, 67), Interval(67, 75), Interval(44, 50),
         Interval(39, 39), Interval(73, 91), Interval(35, 35), Interval(11, 13), Interval(2, 2),
         Interval(36, 42), Interval(42, 42), Interval(46, 58), Interval(58, 72), Interval(34, 36)],
        # Job 5
        [Interval(43, 53), Interval(49, 65), Interval(5, 5), Interval(2, 2), Interval(53, 67),
         Interval(55, 73), Interval(80, 92), Interval(3, 3), Interval(44, 58), Interval(26, 26),
         Interval(31, 37), Interval(38, 40), Interval(39, 51), Interval(60, 66), Interval(53, 55)],
        # Job 6
        [Interval(40, 40), Interval(38, 48), Interval(49, 51), Interval(65, 77), Interval(41, 51),
         Interval(88, 110), Interval(57, 77), Interval(29, 39), Interval(6, 6), Interval(88, 102),
         Interval(58, 76), Interval(48, 60), Interval(29, 29), Interval(30, 30), Interval(60, 60)],
        # Job 7
        [Interval(51, 67), Interval(3, 3), Interval(85, 85), Interval(6, 6), Interval(41, 51),
         Interval(49, 49), Interval(5, 5), Interval(78, 86), Interval(16, 20), Interval(68, 74),
         Interval(47, 49), Interval(77, 81), Interval(59, 65), Interval(65, 65), Interval(74, 78)],
        # Job 8
        [Interval(57, 73), Interval(50, 60), Interval(77, 85), Interval(14, 16), Interval(32, 32),
         Interval(45, 59), Interval(89, 105), Interval(65, 73), Interval(74, 90), Interval(76, 102),
         Interval(60, 78), Interval(78, 96), Interval(22, 22), Interval(71, 71), Interval(56, 70)],
        # Job 9
        [Interval(61, 79), Interval(66, 82), Interval(48, 56), Interval(85, 103), Interval(12, 16),
         Interval(80, 82), Interval(21, 27), Interval(14, 14), Interval(31, 33), Interval(37, 41),
         Interval(64, 70), Interval(51, 67), Interval(17, 19), Interval(66, 88), Interval(43, 57)],
        # Job 10
        [Interval(17, 19), Interval(6, 6), Interval(95, 97), Interval(52, 54), Interval(31, 39),
         Interval(98, 100), Interval(38, 40), Interval(17, 19), Interval(12, 16), Interval(77, 103),
         Interval(62, 66), Interval(77, 85), Interval(83, 95), Interval(46, 50), Interval(77, 83)],
        # Job 11
        [Interval(40, 48), Interval(74, 76), Interval(12, 12), Interval(12, 14), Interval(63, 85),
         Interval(52, 66), Interval(68, 74), Interval(66, 84), Interval(30, 30), Interval(91, 95),
         Interval(24, 28), Interval(28, 32), Interval(77, 91), Interval(85, 97), Interval(82, 104)],
        # Job 12
        [Interval(37, 41), Interval(50, 62), Interval(13, 13), Interval(27, 31), Interval(50, 60),
         Interval(65, 73), Interval(25, 27), Interval(6, 8), Interval(51, 59), Interval(43, 53),
         Interval(20, 24), Interval(46, 46), Interval(45, 55), Interval(85, 107), Interval(16, 18)],
        # Job 13
        [Interval(54, 60), Interval(12, 16), Interval(7, 9), Interval(13, 13), Interval(85, 105),
         Interval(47, 59), Interval(74, 82), Interval(24, 24), Interval(91, 93), Interval(83, 97),
         Interval(59, 77), Interval(79, 95), Interval(38, 48), Interval(73, 77), Interval(84, 104)],
        # Job 14
        [Interval(81, 105), Interval(82, 102), Interval(18, 18), Interval(27, 29), Interval(25, 29),
         Interval(38, 42), Interval(49, 63), Interval(76, 90), Interval(44, 58), Interval(15, 15),
         Interval(94, 100), Interval(46, 50), Interval(49, 57), Interval(76, 80), Interval(34, 44)],
        # Job 15
        [Interval(40, 54), Interval(31, 37), Interval(36, 48), Interval(25, 31), Interval(11, 11),
         Interval(10, 12), Interval(29, 31), Interval(12, 16), Interval(9, 11), Interval(4, 4),
         Interval(18, 22), Interval(86, 98), Interval(19, 19), Interval(52, 66), Interval(27, 29)],
        # Job 16
        [Interval(63, 75), Interval(72, 92), Interval(56, 72), Interval(39, 41), Interval(25, 29),
         Interval(79, 85), Interval(25, 29), Interval(41, 45), Interval(50, 62), Interval(16, 18),
         Interval(16, 20), Interval(17, 23), Interval(96, 100), Interval(37, 49), Interval(62, 74)],
        # Job 17
        [Interval(82, 86), Interval(26, 26), Interval(81, 93), Interval(60, 62), Interval(83, 107),
         Interval(22, 24), Interval(82, 94), Interval(77, 101), Interval(42, 56), Interval(83, 85),
         Interval(12, 12), Interval(44, 58), Interval(3, 3), Interval(44, 44), Interval(17, 23)],
        # Job 18
        [Interval(41, 45), Interval(47, 61), Interval(17, 19), Interval(64, 80), Interval(67, 73),
         Interval(26, 30), Interval(20, 20), Interval(22, 22), Interval(53, 65), Interval(33, 39),
         Interval(75, 95), Interval(12, 14), Interval(71, 75), Interval(26, 32), Interval(40, 50)],
        # Job 19
        [Interval(6, 8), Interval(86, 108), Interval(4, 4), Interval(21, 23), Interval(67, 81),
         Interval(40, 50), Interval(55, 69), Interval(90, 100), Interval(64, 68), Interval(13, 15),
         Interval(37, 43), Interval(23, 23), Interval(68, 90), Interval(32, 36), Interval(7, 9)],
    ],
    'name': 'INT__TAI20_15_01.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai20_15_01_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI20_15_01.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI20_15_01.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI20_15_01_F_15_01_INTERVAL_DATA
