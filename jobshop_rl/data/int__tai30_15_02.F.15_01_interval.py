"""
Problema INT__TAI30_15_02.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI30_15_02_F_15_01_INTERVAL_DATA = {
    'num_jobs': 30,
    'num_machines': 15,
    'problem_id': 'int__tai30_15_02.F.15_01_interval',
    'sequences': [
        [13, 0, 10, 2, 12, 8, 5, 6, 4, 14, 1, 11, 9, 3, 7],
        [7, 3, 0, 12, 13, 14, 8, 1, 10, 4, 11, 2, 6, 9, 5],
        [12, 14, 10, 1, 13, 5, 3, 11, 6, 2, 4, 7, 8, 0, 9],
        [14, 13, 1, 12, 7, 0, 4, 5, 3, 2, 6, 8, 11, 10, 9],
        [7, 5, 1, 3, 8, 12, 2, 13, 0, 4, 6, 10, 11, 14, 9],
        [11, 5, 4, 14, 10, 3, 0, 9, 7, 12, 6, 2, 13, 8, 1],
        [5, 8, 12, 9, 3, 2, 14, 4, 1, 13, 7, 0, 11, 6, 10],
        [7, 14, 5, 9, 3, 1, 4, 10, 12, 2, 6, 13, 11, 0, 8],
        [10, 14, 6, 5, 13, 12, 3, 8, 0, 7, 2, 9, 4, 11, 1],
        [6, 5, 4, 3, 12, 14, 7, 9, 1, 13, 11, 8, 2, 0, 10],
        [5, 1, 0, 11, 13, 6, 12, 7, 2, 9, 3, 4, 10, 8, 14],
        [12, 13, 0, 3, 2, 5, 10, 11, 4, 1, 7, 14, 9, 6, 8],
        [11, 0, 9, 12, 7, 2, 13, 8, 5, 4, 3, 1, 14, 6, 10],
        [5, 8, 13, 10, 14, 7, 9, 0, 12, 2, 6, 4, 11, 3, 1],
        [9, 3, 10, 5, 2, 6, 7, 11, 4, 1, 12, 13, 14, 8, 0],
        [1, 7, 2, 5, 6, 9, 10, 8, 14, 11, 4, 12, 0, 3, 13],
        [13, 11, 5, 2, 0, 6, 8, 9, 10, 4, 7, 1, 12, 14, 3],
        [9, 8, 1, 10, 3, 2, 6, 11, 0, 7, 5, 12, 13, 14, 4],
        [5, 12, 3, 0, 13, 10, 7, 9, 6, 14, 1, 4, 2, 8, 11],
        [5, 10, 11, 7, 4, 6, 9, 0, 8, 12, 2, 3, 1, 13, 14],
        [10, 14, 3, 1, 11, 13, 9, 12, 6, 8, 0, 5, 2, 7, 4],
        [14, 12, 8, 13, 6, 9, 5, 2, 7, 10, 3, 1, 4, 11, 0],
        [11, 8, 7, 6, 0, 9, 13, 10, 12, 5, 2, 14, 1, 4, 3],
        [1, 9, 12, 7, 5, 8, 13, 2, 3, 14, 6, 0, 10, 11, 4],
        [2, 5, 13, 0, 9, 3, 8, 1, 12, 14, 6, 4, 10, 11, 7],
        [1, 8, 7, 14, 10, 3, 5, 6, 4, 12, 13, 11, 0, 2, 9],
        [2, 14, 3, 13, 10, 5, 12, 7, 1, 8, 0, 11, 4, 6, 9],
        [14, 4, 3, 2, 9, 0, 8, 6, 7, 11, 1, 13, 12, 5, 10],
        [9, 12, 5, 4, 2, 3, 0, 13, 8, 7, 6, 10, 1, 11, 14],
        [11, 6, 7, 8, 5, 14, 13, 3, 10, 1, 12, 0, 2, 9, 4],
    ],
    'durations': [
        # Job 0
        [Interval(68, 90), Interval(29, 33), Interval(40, 44), Interval(88, 88), Interval(14, 18),
         Interval(91, 107), Interval(77, 87), Interval(48, 58), Interval(26, 32), Interval(49, 49),
         Interval(8, 10), Interval(15, 15), Interval(79, 105), Interval(65, 81), Interval(98, 98)],
        # Job 1
        [Interval(72, 80), Interval(76, 102), Interval(46, 50), Interval(13, 17), Interval(49, 59),
         Interval(35, 39), Interval(50, 56), Interval(62, 64), Interval(39, 49), Interval(80, 102),
         Interval(12, 14), Interval(65, 81), Interval(42, 42), Interval(99, 99), Interval(38, 44)],
        # Job 2
        [Interval(42, 56), Interval(47, 57), Interval(24, 26), Interval(82, 96), Interval(3, 3),
         Interval(2, 2), Interval(34, 46), Interval(39, 49), Interval(81, 107), Interval(6, 8),
         Interval(58, 78), Interval(69, 77), Interval(72, 74), Interval(28, 32), Interval(14, 14)],
        # Job 3
        [Interval(24, 32), Interval(46, 52), Interval(13, 13), Interval(87, 87), Interval(61, 63),
         Interval(10, 10), Interval(26, 32), Interval(58, 66), Interval(31, 37), Interval(6, 8),
         Interval(44, 50), Interval(38, 42), Interval(55, 59), Interval(69, 91), Interval(85, 87)],
        # Job 4
        [Interval(39, 39), Interval(11, 13), Interval(30, 38), Interval(81, 101), Interval(46, 50),
         Interval(61, 81), Interval(43, 47), Interval(98, 98), Interval(20, 26), Interval(86, 96),
         Interval(81, 99), Interval(39, 43), Interval(79, 101), Interval(53, 55), Interval(83, 91)],
        # Job 5
        [Interval(30, 30), Interval(54, 72), Interval(50, 64), Interval(32, 40), Interval(67, 77),
         Interval(50, 58), Interval(65, 73), Interval(8, 10), Interval(46, 60), Interval(62, 82),
         Interval(59, 77), Interval(33, 33), Interval(52, 70), Interval(12, 12), Interval(82, 96)],
        # Job 6
        [Interval(59, 71), Interval(35, 45), Interval(29, 39), Interval(36, 38), Interval(62, 66),
         Interval(62, 62), Interval(14, 14), Interval(75, 81), Interval(1, 1), Interval(59, 71),
         Interval(2, 2), Interval(58, 76), Interval(52, 60), Interval(69, 81), Interval(26, 26)],
        # Job 7
        [Interval(20, 24), Interval(89, 107), Interval(65, 69), Interval(51, 61), Interval(37, 45),
         Interval(81, 97), Interval(23, 27), Interval(89, 99), Interval(73, 79), Interval(36, 38),
         Interval(8, 8), Interval(81, 87), Interval(66, 80), Interval(61, 69), Interval(69, 79)],
        # Job 8
        [Interval(43, 45), Interval(30, 36), Interval(41, 41), Interval(50, 54), Interval(84, 88),
         Interval(10, 12), Interval(59, 61), Interval(86, 88), Interval(13, 13), Interval(37, 43),
         Interval(61, 63), Interval(43, 51), Interval(37, 41), Interval(63, 67), Interval(75, 79)],
        # Job 9
        [Interval(85, 91), Interval(31, 31), Interval(62, 64), Interval(45, 53), Interval(47, 53),
         Interval(69, 85), Interval(6, 6), Interval(79, 81), Interval(17, 23), Interval(28, 32),
         Interval(10, 12), Interval(36, 46), Interval(40, 46), Interval(68, 80), Interval(65, 81)],
        # Job 10
        [Interval(7, 7), Interval(68, 70), Interval(59, 79), Interval(52, 54), Interval(47, 57),
         Interval(31, 35), Interval(19, 19), Interval(83, 85), Interval(12, 12), Interval(36, 36),
         Interval(80, 90), Interval(69, 79), Interval(2, 2), Interval(96, 98), Interval(45, 59)],
        # Job 11
        [Interval(33, 33), Interval(7, 9), Interval(69, 79), Interval(66, 84), Interval(48, 54),
         Interval(60, 68), Interval(47, 63), Interval(6, 8), Interval(69, 93), Interval(82, 82),
         Interval(68, 72), Interval(33, 33), Interval(78, 90), Interval(35, 39), Interval(42, 54)],
        # Job 12
        [Interval(46, 62), Interval(85, 109), Interval(70, 88), Interval(71, 71), Interval(63, 77),
         Interval(83, 85), Interval(28, 28), Interval(13, 15), Interval(20, 20), Interval(93, 105),
         Interval(6, 6), Interval(27, 33), Interval(51, 51), Interval(65, 71), Interval(37, 45)],
        # Job 13
        [Interval(10, 10), Interval(83, 97), Interval(14, 14), Interval(71, 73), Interval(27, 33),
         Interval(75, 79), Interval(63, 75), Interval(53, 59), Interval(77, 79), Interval(49, 61),
         Interval(86, 110), Interval(84, 98), Interval(26, 28), Interval(31, 41), Interval(80, 92)],
        # Job 14
        [Interval(85, 99), Interval(90, 104), Interval(64, 78), Interval(12, 14), Interval(81, 105),
         Interval(62, 68), Interval(42, 46), Interval(46, 46), Interval(67, 75), Interval(60, 78),
         Interval(24, 28), Interval(16, 20), Interval(30, 32), Interval(9, 11), Interval(41, 53)],
        # Job 15
        [Interval(47, 47), Interval(5, 5), Interval(12, 16), Interval(40, 54), Interval(80, 82),
         Interval(78, 90), Interval(53, 71), Interval(89, 93), Interval(5, 5), Interval(58, 58),
         Interval(68, 86), Interval(53, 57), Interval(48, 50), Interval(5, 5), Interval(5, 5)],
        # Job 16
        [Interval(40, 52), Interval(83, 109), Interval(55, 67), Interval(63, 71), Interval(2, 2),
         Interval(9, 9), Interval(84, 104), Interval(34, 42), Interval(61, 71), Interval(23, 27),
         Interval(63, 71), Interval(50, 64), Interval(70, 88), Interval(64, 84), Interval(47, 47)],
        # Job 17
        [Interval(65, 83), Interval(52, 52), Interval(50, 50), Interval(42, 44), Interval(89, 97),
         Interval(28, 32), Interval(82, 88), Interval(71, 79), Interval(55, 61), Interval(43, 51),
         Interval(64, 76), Interval(40, 44), Interval(60, 64), Interval(58, 58), Interval(74, 88)],
        # Job 18
        [Interval(5, 5), Interval(37, 47), Interval(54, 72), Interval(41, 43), Interval(27, 29),
         Interval(34, 46), Interval(34, 38), Interval(47, 51), Interval(60, 70), Interval(6, 6),
         Interval(12, 16), Interval(17, 23), Interval(75, 95), Interval(39, 43), Interval(67, 73)],
        # Job 19
        [Interval(7, 7), Interval(32, 40), Interval(51, 57), Interval(84, 98), Interval(91, 105),
         Interval(27, 35), Interval(31, 35), Interval(62, 82), Interval(18, 24), Interval(59, 63),
         Interval(1, 1), Interval(28, 32), Interval(83, 87), Interval(71, 87), Interval(29, 35)],
        # Job 20
        [Interval(71, 87), Interval(71, 93), Interval(44, 54), Interval(51, 51), Interval(38, 48),
         Interval(14, 18), Interval(39, 49), Interval(62, 62), Interval(18, 22), Interval(12, 12),
         Interval(7, 7), Interval(1, 1), Interval(63, 65), Interval(20, 22), Interval(35, 39)],
        # Job 21
        [Interval(87, 101), Interval(73, 77), Interval(49, 63), Interval(23, 27), Interval(85, 93),
         Interval(72, 72), Interval(72, 96), Interval(67, 75), Interval(64, 84), Interval(73, 93),
         Interval(6, 6), Interval(63, 75), Interval(85, 89), Interval(17, 21), Interval(61, 75)],
        # Job 22
        [Interval(7, 7), Interval(27, 31), Interval(14, 16), Interval(3, 3), Interval(53, 71),
         Interval(47, 59), Interval(80, 104), Interval(1, 1), Interval(27, 27), Interval(19, 23),
         Interval(61, 71), Interval(88, 96), Interval(17, 21), Interval(21, 23), Interval(41, 55)],
        # Job 23
        [Interval(70, 80), Interval(12, 12), Interval(42, 50), Interval(37, 37), Interval(71, 73),
         Interval(31, 39), Interval(6, 6), Interval(31, 33), Interval(44, 56), Interval(32, 34),
         Interval(12, 16), Interval(34, 34), Interval(92, 94), Interval(82, 84), Interval(10, 12)],
        # Job 24
        [Interval(87, 87), Interval(50, 62), Interval(70, 70), Interval(79, 83), Interval(78, 82),
         Interval(54, 62), Interval(73, 77), Interval(45, 51), Interval(47, 63), Interval(85, 99),
         Interval(8, 10), Interval(16, 16), Interval(35, 47), Interval(67, 75), Interval(63, 63)],
        # Job 25
        [Interval(29, 29), Interval(65, 67), Interval(17, 19), Interval(49, 61), Interval(52, 54),
         Interval(77, 85), Interval(42, 52), Interval(77, 95), Interval(30, 36), Interval(30, 30),
         Interval(74, 76), Interval(66, 80), Interval(23, 31), Interval(48, 54), Interval(67, 67)],
        # Job 26
        [Interval(54, 66), Interval(16, 18), Interval(16, 20), Interval(56, 66), Interval(70, 94),
         Interval(67, 77), Interval(5, 5), Interval(87, 97), Interval(70, 80), Interval(86, 96),
         Interval(79, 99), Interval(30, 40), Interval(48, 58), Interval(64, 72), Interval(75, 95)],
        # Job 27
        [Interval(78, 86), Interval(54, 54), Interval(87, 105), Interval(18, 20), Interval(19, 21),
         Interval(66, 68), Interval(27, 27), Interval(69, 85), Interval(59, 59), Interval(85, 89),
         Interval(37, 43), Interval(6, 8), Interval(43, 49), Interval(31, 33), Interval(76, 92)],
        # Job 28
        [Interval(68, 70), Interval(46, 58), Interval(26, 26), Interval(60, 70), Interval(78, 100),
         Interval(45, 57), Interval(75, 83), Interval(47, 55), Interval(25, 29), Interval(82, 100),
         Interval(23, 23), Interval(55, 63), Interval(85, 113), Interval(48, 54), Interval(69, 71)],
        # Job 29
        [Interval(61, 63), Interval(57, 57), Interval(27, 33), Interval(5, 5), Interval(28, 32),
         Interval(12, 14), Interval(38, 40), Interval(30, 32), Interval(14, 18), Interval(60, 76),
         Interval(28, 36), Interval(72, 94), Interval(4, 4), Interval(26, 28), Interval(26, 28)],
    ],
    'name': 'INT__TAI30_15_02.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai30_15_02_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI30_15_02.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI30_15_02.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI30_15_02_F_15_01_INTERVAL_DATA
