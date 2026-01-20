"""
Problema INT__TAI20_15_07.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI20_15_07_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__tai20_15_07.F.15_01_interval',
    'sequences': [
        [6, 8, 11, 0, 14, 13, 9, 5, 3, 12, 10, 2, 7, 4, 1],
        [0, 9, 1, 6, 5, 13, 11, 8, 3, 4, 12, 14, 7, 2, 10],
        [8, 3, 9, 1, 0, 10, 5, 14, 12, 13, 6, 2, 7, 11, 4],
        [5, 1, 7, 10, 0, 2, 13, 11, 14, 3, 6, 9, 8, 12, 4],
        [2, 9, 6, 7, 0, 8, 13, 5, 10, 3, 12, 4, 14, 1, 11],
        [5, 3, 9, 2, 1, 4, 10, 8, 13, 0, 11, 12, 6, 14, 7],
        [8, 7, 12, 9, 6, 14, 4, 11, 5, 1, 3, 13, 10, 0, 2],
        [13, 7, 6, 11, 2, 0, 14, 4, 3, 1, 10, 8, 9, 12, 5],
        [1, 14, 0, 10, 11, 8, 7, 5, 9, 3, 4, 6, 12, 2, 13],
        [13, 1, 3, 14, 5, 9, 2, 0, 11, 7, 12, 4, 10, 6, 8],
        [10, 5, 9, 13, 6, 8, 11, 4, 14, 0, 7, 2, 12, 1, 3],
        [13, 9, 14, 10, 3, 7, 2, 5, 6, 11, 8, 1, 0, 12, 4],
        [5, 9, 7, 8, 10, 13, 2, 6, 1, 0, 12, 11, 3, 4, 14],
        [9, 11, 6, 7, 2, 8, 14, 3, 0, 12, 4, 13, 5, 1, 10],
        [10, 2, 1, 5, 0, 3, 14, 11, 4, 8, 9, 7, 12, 6, 13],
        [12, 14, 0, 2, 10, 5, 13, 3, 7, 11, 1, 9, 6, 8, 4],
        [8, 6, 12, 4, 13, 10, 5, 7, 9, 0, 1, 14, 3, 2, 11],
        [14, 5, 12, 4, 1, 13, 6, 2, 8, 7, 10, 11, 9, 3, 0],
        [7, 2, 6, 3, 8, 14, 5, 9, 4, 13, 0, 11, 12, 1, 10],
        [10, 7, 13, 4, 5, 3, 6, 1, 8, 0, 12, 11, 9, 14, 2],
    ],
    'durations': [
        # Job 0
        [Interval(40, 40), Interval(57, 57), Interval(81, 109), Interval(32, 34), Interval(67, 77),
         Interval(27, 35), Interval(55, 55), Interval(33, 39), Interval(92, 92), Interval(64, 80),
         Interval(69, 91), Interval(37, 41), Interval(3, 3), Interval(74, 98), Interval(29, 29)],
        # Job 1
        [Interval(18, 22), Interval(50, 62), Interval(66, 70), Interval(45, 53), Interval(30, 40),
         Interval(54, 62), Interval(89, 91), Interval(45, 59), Interval(93, 101), Interval(84, 106),
         Interval(85, 103), Interval(30, 34), Interval(52, 60), Interval(64, 78), Interval(71, 95)],
        # Job 2
        [Interval(95, 101), Interval(5, 5), Interval(88, 106), Interval(76, 94), Interval(29, 33),
         Interval(5, 5), Interval(14, 18), Interval(17, 21), Interval(69, 81), Interval(46, 54),
         Interval(21, 25), Interval(59, 67), Interval(86, 92), Interval(58, 72), Interval(21, 27)],
        # Job 3
        [Interval(71, 89), Interval(50, 66), Interval(40, 42), Interval(29, 39), Interval(86, 102),
         Interval(58, 68), Interval(7, 9), Interval(74, 76), Interval(55, 65), Interval(38, 46),
         Interval(38, 38), Interval(3, 3), Interval(73, 73), Interval(75, 83), Interval(34, 38)],
        # Job 4
        [Interval(70, 72), Interval(60, 70), Interval(23, 29), Interval(56, 62), Interval(51, 57),
         Interval(68, 70), Interval(77, 95), Interval(86, 86), Interval(37, 49), Interval(6, 8),
         Interval(35, 35), Interval(76, 96), Interval(88, 110), Interval(92, 96), Interval(89, 109)],
        # Job 5
        [Interval(70, 94), Interval(62, 78), Interval(46, 60), Interval(68, 80), Interval(50, 66),
         Interval(68, 72), Interval(46, 54), Interval(36, 38), Interval(77, 103), Interval(21, 23),
         Interval(9, 9), Interval(98, 98), Interval(26, 34), Interval(91, 97), Interval(40, 46)],
        # Job 6
        [Interval(62, 80), Interval(56, 70), Interval(56, 74), Interval(13, 17), Interval(37, 41),
         Interval(82, 104), Interval(87, 107), Interval(66, 68), Interval(5, 5), Interval(61, 61),
         Interval(64, 64), Interval(58, 78), Interval(2, 2), Interval(31, 31), Interval(15, 19)],
        # Job 7
        [Interval(7, 7), Interval(10, 10), Interval(56, 74), Interval(60, 66), Interval(90, 94),
         Interval(87, 93), Interval(80, 90), Interval(81, 81), Interval(32, 32), Interval(54, 70),
         Interval(5, 5), Interval(19, 23), Interval(5, 5), Interval(47, 51), Interval(33, 39)],
        # Job 8
        [Interval(9, 9), Interval(27, 35), Interval(71, 83), Interval(46, 52), Interval(22, 26),
         Interval(57, 77), Interval(58, 74), Interval(33, 41), Interval(82, 82), Interval(69, 69),
         Interval(56, 70), Interval(4, 4), Interval(54, 70), Interval(47, 57), Interval(61, 71)],
        # Job 9
        [Interval(61, 73), Interval(66, 80), Interval(86, 88), Interval(24, 32), Interval(43, 43),
         Interval(13, 13), Interval(17, 19), Interval(70, 76), Interval(59, 79), Interval(18, 22),
         Interval(83, 111), Interval(63, 83), Interval(58, 70), Interval(8, 8), Interval(13, 13)],
        # Job 10
        [Interval(75, 95), Interval(30, 30), Interval(78, 82), Interval(60, 68), Interval(16, 20),
         Interval(62, 82), Interval(64, 68), Interval(69, 75), Interval(26, 30), Interval(13, 13),
         Interval(17, 17), Interval(50, 60), Interval(17, 17), Interval(41, 43), Interval(52, 64)],
        # Job 11
        [Interval(74, 100), Interval(31, 41), Interval(83, 91), Interval(24, 30), Interval(23, 23),
         Interval(70, 74), Interval(44, 54), Interval(74, 84), Interval(28, 32), Interval(16, 18),
         Interval(50, 64), Interval(53, 59), Interval(72, 92), Interval(4, 4), Interval(62, 70)],
        # Job 12
        [Interval(6, 6), Interval(58, 66), Interval(71, 85), Interval(74, 82), Interval(59, 65),
         Interval(15, 19), Interval(40, 46), Interval(17, 19), Interval(48, 58), Interval(16, 16),
         Interval(60, 72), Interval(17, 23), Interval(65, 73), Interval(47, 51), Interval(4, 4)],
        # Job 13
        [Interval(29, 39), Interval(77, 101), Interval(23, 23), Interval(62, 76), Interval(11, 13),
         Interval(56, 62), Interval(49, 51), Interval(56, 58), Interval(78, 92), Interval(14, 18),
         Interval(50, 60), Interval(72, 92), Interval(60, 62), Interval(5, 5), Interval(32, 40)],
        # Job 14
        [Interval(62, 80), Interval(17, 21), Interval(92, 100), Interval(9, 9), Interval(78, 92),
         Interval(84, 92), Interval(3, 3), Interval(60, 76), Interval(48, 56), Interval(25, 33),
         Interval(28, 30), Interval(22, 22), Interval(10, 10), Interval(8, 10), Interval(63, 67)],
        # Job 15
        [Interval(20, 26), Interval(29, 39), Interval(67, 79), Interval(29, 39), Interval(77, 93),
         Interval(40, 40), Interval(66, 80), Interval(14, 16), Interval(46, 56), Interval(78, 104),
         Interval(1, 1), Interval(39, 47), Interval(7, 7), Interval(62, 64), Interval(6, 8)],
        # Job 16
        [Interval(18, 18), Interval(57, 67), Interval(86, 108), Interval(43, 55), Interval(4, 4),
         Interval(69, 73), Interval(64, 72), Interval(49, 53), Interval(39, 45), Interval(38, 42),
         Interval(29, 35), Interval(85, 99), Interval(10, 12), Interval(40, 52), Interval(97, 101)],
        # Job 17
        [Interval(1, 1), Interval(81, 105), Interval(42, 50), Interval(12, 12), Interval(11, 11),
         Interval(77, 87), Interval(55, 57), Interval(34, 44), Interval(79, 89), Interval(40, 46),
         Interval(66, 88), Interval(19, 25), Interval(23, 23), Interval(47, 47), Interval(37, 49)],
        # Job 18
        [Interval(97, 99), Interval(33, 43), Interval(88, 96), Interval(63, 81), Interval(74, 82),
         Interval(62, 78), Interval(45, 49), Interval(30, 34), Interval(82, 86), Interval(82, 86),
         Interval(56, 70), Interval(86, 104), Interval(52, 66), Interval(23, 29), Interval(14, 14)],
        # Job 19
        [Interval(71, 89), Interval(47, 59), Interval(66, 78), Interval(8, 10), Interval(83, 95),
         Interval(28, 32), Interval(30, 40), Interval(30, 38), Interval(50, 54), Interval(84, 90),
         Interval(89, 105), Interval(32, 36), Interval(71, 75), Interval(58, 78), Interval(29, 33)],
    ],
    'name': 'INT__TAI20_15_07.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai20_15_07_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI20_15_07.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI20_15_07.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI20_15_07_F_15_01_INTERVAL_DATA
