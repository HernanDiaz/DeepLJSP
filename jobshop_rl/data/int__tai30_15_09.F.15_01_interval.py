"""
Problema INT__TAI30_15_09.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI30_15_09_F_15_01_INTERVAL_DATA = {
    'num_jobs': 30,
    'num_machines': 15,
    'problem_id': 'int__tai30_15_09.F.15_01_interval',
    'sequences': [
        [5, 3, 12, 6, 9, 1, 14, 4, 2, 13, 10, 0, 8, 11, 7],
        [1, 7, 0, 2, 4, 11, 10, 14, 5, 12, 8, 3, 9, 6, 13],
        [9, 1, 6, 4, 0, 10, 5, 13, 7, 11, 14, 2, 3, 8, 12],
        [5, 8, 6, 14, 1, 0, 3, 11, 12, 10, 7, 13, 4, 2, 9],
        [0, 11, 1, 5, 9, 13, 14, 2, 7, 12, 3, 8, 4, 10, 6],
        [12, 1, 10, 7, 14, 9, 0, 2, 6, 13, 8, 3, 11, 5, 4],
        [8, 12, 3, 11, 6, 5, 2, 7, 10, 13, 14, 1, 4, 0, 9],
        [8, 4, 10, 0, 14, 2, 12, 1, 6, 9, 3, 13, 7, 5, 11],
        [12, 5, 3, 8, 4, 11, 7, 14, 2, 1, 13, 6, 9, 10, 0],
        [0, 9, 5, 14, 1, 13, 6, 11, 7, 10, 4, 8, 2, 3, 12],
        [13, 6, 4, 7, 2, 8, 12, 10, 5, 11, 0, 1, 3, 9, 14],
        [6, 0, 7, 8, 4, 13, 2, 1, 9, 14, 12, 10, 5, 11, 3],
        [6, 0, 4, 7, 2, 12, 10, 8, 13, 11, 14, 9, 3, 5, 1],
        [3, 12, 5, 1, 6, 4, 7, 2, 11, 9, 13, 14, 0, 8, 10],
        [11, 3, 1, 13, 7, 9, 8, 14, 10, 4, 6, 2, 12, 0, 5],
        [7, 13, 9, 4, 10, 2, 0, 6, 5, 3, 8, 1, 14, 11, 12],
        [7, 5, 14, 10, 13, 6, 3, 2, 9, 12, 4, 8, 1, 0, 11],
        [13, 7, 10, 1, 5, 11, 8, 0, 14, 6, 4, 3, 12, 2, 9],
        [5, 10, 7, 11, 14, 1, 12, 0, 13, 2, 4, 6, 3, 9, 8],
        [10, 7, 5, 2, 11, 14, 3, 9, 0, 6, 4, 12, 13, 8, 1],
        [11, 3, 6, 2, 7, 10, 1, 13, 0, 4, 8, 5, 14, 9, 12],
        [10, 9, 0, 3, 4, 5, 8, 11, 1, 7, 6, 14, 12, 13, 2],
        [10, 9, 0, 4, 7, 2, 1, 13, 6, 14, 12, 8, 11, 3, 5],
        [6, 0, 7, 13, 5, 3, 14, 1, 9, 12, 8, 2, 4, 11, 10],
        [7, 6, 11, 5, 13, 12, 8, 4, 14, 9, 0, 3, 1, 2, 10],
        [7, 5, 10, 6, 11, 13, 9, 0, 12, 2, 8, 14, 1, 3, 4],
        [13, 7, 2, 9, 1, 11, 0, 5, 8, 10, 12, 6, 3, 14, 4],
        [7, 9, 4, 14, 13, 2, 12, 3, 8, 10, 0, 6, 11, 5, 1],
        [9, 12, 7, 11, 4, 5, 0, 1, 13, 8, 3, 10, 2, 6, 14],
        [10, 11, 14, 13, 5, 1, 12, 9, 3, 6, 8, 2, 0, 4, 7],
    ],
    'durations': [
        # Job 0
        [Interval(17, 23), Interval(51, 61), Interval(65, 73), Interval(15, 15), Interval(6, 6),
         Interval(64, 86), Interval(77, 91), Interval(23, 25), Interval(57, 71), Interval(34, 40),
         Interval(78, 80), Interval(84, 106), Interval(27, 27), Interval(51, 69), Interval(31, 39)],
        # Job 1
        [Interval(27, 27), Interval(55, 61), Interval(48, 64), Interval(29, 31), Interval(26, 34),
         Interval(52, 62), Interval(51, 59), Interval(60, 66), Interval(32, 32), Interval(38, 48),
         Interval(39, 49), Interval(66, 82), Interval(41, 51), Interval(11, 11), Interval(41, 41)],
        # Job 2
        [Interval(40, 46), Interval(64, 86), Interval(7, 9), Interval(69, 73), Interval(46, 54),
         Interval(48, 64), Interval(12, 14), Interval(12, 16), Interval(89, 109), Interval(49, 65),
         Interval(81, 91), Interval(28, 28), Interval(35, 39), Interval(83, 83), Interval(60, 80)],
        # Job 3
        [Interval(64, 72), Interval(63, 69), Interval(27, 27), Interval(33, 33), Interval(46, 48),
         Interval(67, 79), Interval(81, 93), Interval(65, 75), Interval(19, 23), Interval(21, 23),
         Interval(29, 31), Interval(10, 10), Interval(10, 12), Interval(10, 10), Interval(17, 17)],
        # Job 4
        [Interval(6, 6), Interval(44, 54), Interval(10, 12), Interval(61, 77), Interval(48, 52),
         Interval(43, 57), Interval(12, 12), Interval(73, 73), Interval(72, 96), Interval(87, 97),
         Interval(1, 1), Interval(76, 92), Interval(84, 92), Interval(46, 58), Interval(45, 47)],
        # Job 5
        [Interval(14, 14), Interval(7, 7), Interval(10, 12), Interval(70, 88), Interval(40, 50),
         Interval(20, 24), Interval(79, 91), Interval(63, 71), Interval(56, 72), Interval(64, 86),
         Interval(19, 25), Interval(31, 39), Interval(64, 66), Interval(26, 34), Interval(68, 68)],
        # Job 6
        [Interval(61, 73), Interval(16, 18), Interval(51, 65), Interval(17, 23), Interval(43, 47),
         Interval(53, 57), Interval(53, 53), Interval(10, 10), Interval(3, 3), Interval(64, 68),
         Interval(57, 69), Interval(32, 40), Interval(87, 99), Interval(37, 43), Interval(82, 88)],
        # Job 7
        [Interval(7, 9), Interval(24, 30), Interval(66, 70), Interval(36, 42), Interval(22, 26),
         Interval(61, 73), Interval(30, 34), Interval(40, 44), Interval(52, 56), Interval(18, 18),
         Interval(54, 62), Interval(73, 77), Interval(33, 41), Interval(59, 67), Interval(15, 17)],
        # Job 8
        [Interval(81, 85), Interval(24, 30), Interval(3, 3), Interval(25, 25), Interval(65, 71),
         Interval(62, 64), Interval(29, 37), Interval(85, 87), Interval(12, 12), Interval(22, 22),
         Interval(69, 81), Interval(16, 16), Interval(41, 47), Interval(76, 84), Interval(47, 49)],
        # Job 9
        [Interval(91, 95), Interval(52, 56), Interval(79, 83), Interval(14, 14), Interval(63, 75),
         Interval(62, 70), Interval(18, 22), Interval(2, 2), Interval(6, 6), Interval(87, 89),
         Interval(6, 8), Interval(68, 78), Interval(58, 74), Interval(58, 74), Interval(74, 88)],
        # Job 10
        [Interval(57, 67), Interval(72, 90), Interval(34, 38), Interval(84, 88), Interval(81, 109),
         Interval(90, 94), Interval(42, 50), Interval(9, 11), Interval(6, 6), Interval(18, 18),
         Interval(41, 41), Interval(67, 73), Interval(29, 29), Interval(21, 23), Interval(14, 16)],
        # Job 11
        [Interval(47, 47), Interval(33, 43), Interval(58, 60), Interval(85, 109), Interval(58, 66),
         Interval(8, 10), Interval(20, 22), Interval(28, 32), Interval(7, 9), Interval(21, 25),
         Interval(63, 85), Interval(48, 48), Interval(14, 14), Interval(66, 70), Interval(51, 59)],
        # Job 12
        [Interval(63, 71), Interval(23, 29), Interval(3, 3), Interval(72, 94), Interval(64, 82),
         Interval(17, 21), Interval(12, 12), Interval(72, 90), Interval(15, 15), Interval(34, 34),
         Interval(80, 96), Interval(53, 55), Interval(33, 37), Interval(52, 64), Interval(69, 69)],
        # Job 13
        [Interval(7, 7), Interval(38, 46), Interval(32, 32), Interval(86, 100), Interval(97, 97),
         Interval(4, 4), Interval(96, 100), Interval(72, 88), Interval(87, 93), Interval(53, 63),
         Interval(38, 42), Interval(15, 15), Interval(30, 38), Interval(51, 65), Interval(3, 3)],
        # Job 14
        [Interval(63, 73), Interval(3, 3), Interval(37, 41), Interval(44, 58), Interval(66, 76),
         Interval(71, 83), Interval(41, 47), Interval(39, 47), Interval(6, 6), Interval(33, 43),
         Interval(9, 11), Interval(77, 85), Interval(40, 44), Interval(28, 28), Interval(62, 68)],
        # Job 15
        [Interval(25, 33), Interval(11, 13), Interval(56, 72), Interval(52, 58), Interval(70, 84),
         Interval(17, 23), Interval(77, 79), Interval(35, 43), Interval(75, 101), Interval(46, 48),
         Interval(75, 87), Interval(35, 47), Interval(18, 18), Interval(7, 7), Interval(35, 45)],
        # Job 16
        [Interval(59, 63), Interval(26, 26), Interval(21, 27), Interval(51, 69), Interval(68, 84),
         Interval(54, 60), Interval(67, 67), Interval(25, 31), Interval(55, 67), Interval(55, 65),
         Interval(3, 3), Interval(18, 22), Interval(44, 50), Interval(23, 29), Interval(80, 100)],
        # Job 17
        [Interval(29, 37), Interval(82, 82), Interval(32, 40), Interval(51, 51), Interval(97, 97),
         Interval(19, 19), Interval(60, 66), Interval(25, 29), Interval(34, 36), Interval(27, 29),
         Interval(25, 27), Interval(12, 14), Interval(61, 71), Interval(11, 11), Interval(25, 27)],
        # Job 18
        [Interval(49, 49), Interval(65, 77), Interval(87, 111), Interval(57, 77), Interval(74, 80),
         Interval(19, 21), Interval(82, 110), Interval(1, 1), Interval(82, 94), Interval(20, 22),
         Interval(74, 88), Interval(73, 95), Interval(43, 55), Interval(82, 102), Interval(7, 7)],
        # Job 19
        [Interval(80, 86), Interval(16, 18), Interval(81, 103), Interval(82, 92), Interval(16, 18),
         Interval(56, 66), Interval(27, 35), Interval(1, 1), Interval(62, 72), Interval(69, 91),
         Interval(7, 9), Interval(16, 16), Interval(47, 53), Interval(9, 9), Interval(62, 76)],
        # Job 20
        [Interval(35, 41), Interval(65, 81), Interval(75, 97), Interval(59, 71), Interval(82, 84),
         Interval(22, 28), Interval(31, 39), Interval(19, 25), Interval(81, 81), Interval(13, 15),
         Interval(18, 20), Interval(39, 45), Interval(21, 21), Interval(29, 31), Interval(77, 89)],
        # Job 21
        [Interval(62, 72), Interval(60, 62), Interval(85, 107), Interval(41, 47), Interval(13, 13),
         Interval(38, 38), Interval(44, 58), Interval(85, 95), Interval(73, 95), Interval(27, 33),
         Interval(12, 14), Interval(59, 61), Interval(17, 23), Interval(12, 16), Interval(81, 83)],
        # Job 22
        [Interval(79, 95), Interval(69, 81), Interval(21, 27), Interval(58, 76), Interval(17, 23),
         Interval(95, 97), Interval(69, 83), Interval(56, 66), Interval(42, 46), Interval(45, 57),
         Interval(84, 96), Interval(34, 46), Interval(4, 4), Interval(15, 17), Interval(49, 53)],
        # Job 23
        [Interval(20, 24), Interval(52, 52), Interval(35, 35), Interval(52, 64), Interval(1, 1),
         Interval(59, 65), Interval(4, 4), Interval(60, 76), Interval(8, 8), Interval(35, 43),
         Interval(48, 48), Interval(75, 77), Interval(51, 51), Interval(22, 28), Interval(37, 37)],
        # Job 24
        [Interval(30, 38), Interval(51, 51), Interval(27, 27), Interval(39, 41), Interval(10, 12),
         Interval(93, 99), Interval(76, 86), Interval(75, 101), Interval(83, 97), Interval(29, 35),
         Interval(62, 62), Interval(45, 59), Interval(86, 96), Interval(54, 54), Interval(95, 97)],
        # Job 25
        [Interval(39, 41), Interval(1, 1), Interval(3, 3), Interval(65, 77), Interval(18, 22),
         Interval(51, 53), Interval(88, 96), Interval(65, 81), Interval(15, 19), Interval(77, 97),
         Interval(79, 83), Interval(35, 35), Interval(22, 26), Interval(20, 26), Interval(88, 98)],
        # Job 26
        [Interval(58, 58), Interval(59, 71), Interval(1, 1), Interval(75, 87), Interval(29, 39),
         Interval(44, 52), Interval(70, 94), Interval(30, 34), Interval(22, 24), Interval(41, 47),
         Interval(19, 21), Interval(71, 89), Interval(73, 97), Interval(51, 61), Interval(85, 95)],
        # Job 27
        [Interval(72, 92), Interval(58, 64), Interval(68, 68), Interval(59, 71), Interval(44, 52),
         Interval(85, 91), Interval(2, 2), Interval(75, 77), Interval(37, 37), Interval(65, 79),
         Interval(18, 18), Interval(11, 11), Interval(31, 35), Interval(21, 27), Interval(61, 69)],
        # Job 28
        [Interval(91, 97), Interval(13, 15), Interval(17, 17), Interval(22, 28), Interval(56, 58),
         Interval(74, 88), Interval(7, 9), Interval(72, 90), Interval(56, 62), Interval(90, 104),
         Interval(39, 47), Interval(30, 38), Interval(55, 55), Interval(33, 39), Interval(2, 2)],
        # Job 29
        [Interval(20, 26), Interval(60, 68), Interval(7, 7), Interval(87, 91), Interval(13, 13),
         Interval(87, 105), Interval(77, 91), Interval(83, 99), Interval(20, 20), Interval(3, 3),
         Interval(44, 46), Interval(45, 55), Interval(1, 1), Interval(36, 46), Interval(49, 65)],
    ],
    'name': 'INT__TAI30_15_09.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai30_15_09_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI30_15_09.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI30_15_09.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI30_15_09_F_15_01_INTERVAL_DATA
