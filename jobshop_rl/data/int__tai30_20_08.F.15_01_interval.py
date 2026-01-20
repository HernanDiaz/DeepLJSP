"""
Problema INT__TAI30_20_08.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI30_20_08_F_15_01_INTERVAL_DATA = {
    'num_jobs': 30,
    'num_machines': 20,
    'problem_id': 'int__tai30_20_08.F.15_01_interval',
    'sequences': [
        [6, 5, 15, 8, 13, 2, 10, 17, 11, 0, 9, 1, 19, 4, 16, 3, 12, 7, 18, 14],
        [2, 13, 11, 4, 18, 12, 16, 17, 19, 14, 5, 3, 1, 7, 9, 6, 15, 0, 8, 10],
        [18, 16, 14, 13, 0, 7, 1, 19, 3, 12, 15, 6, 5, 2, 8, 9, 4, 10, 17, 11],
        [9, 10, 5, 14, 18, 2, 8, 11, 12, 3, 4, 1, 6, 19, 13, 7, 0, 16, 15, 17],
        [8, 3, 7, 9, 5, 1, 17, 4, 14, 15, 13, 12, 16, 10, 11, 0, 19, 6, 2, 18],
        [6, 8, 9, 2, 13, 14, 1, 3, 15, 19, 4, 0, 18, 10, 12, 17, 5, 16, 11, 7],
        [16, 7, 12, 2, 13, 6, 5, 8, 3, 18, 9, 15, 17, 11, 14, 0, 19, 10, 1, 4],
        [9, 5, 2, 8, 10, 13, 4, 1, 11, 17, 19, 3, 14, 16, 0, 7, 15, 18, 12, 6],
        [16, 4, 15, 1, 11, 8, 3, 6, 9, 17, 0, 18, 10, 2, 12, 13, 19, 5, 14, 7],
        [3, 14, 15, 17, 8, 10, 6, 19, 0, 18, 9, 1, 16, 5, 4, 13, 11, 12, 7, 2],
        [2, 15, 4, 16, 7, 8, 1, 6, 18, 19, 10, 14, 5, 3, 17, 13, 0, 11, 12, 9],
        [13, 11, 5, 9, 17, 6, 7, 16, 0, 8, 15, 10, 18, 1, 2, 19, 4, 3, 14, 12],
        [16, 7, 13, 12, 2, 19, 10, 14, 15, 17, 5, 1, 4, 11, 0, 18, 3, 9, 6, 8],
        [2, 0, 19, 8, 18, 10, 17, 3, 13, 6, 14, 16, 12, 7, 4, 1, 11, 15, 5, 9],
        [5, 1, 14, 9, 8, 3, 11, 10, 0, 7, 13, 12, 2, 16, 19, 17, 4, 15, 18, 6],
        [17, 16, 4, 0, 15, 5, 3, 14, 12, 2, 10, 18, 8, 6, 1, 19, 11, 13, 9, 7],
        [10, 4, 3, 1, 17, 0, 5, 8, 7, 12, 19, 13, 15, 9, 14, 2, 16, 11, 6, 18],
        [3, 16, 15, 5, 13, 11, 19, 12, 8, 6, 18, 7, 17, 10, 0, 1, 14, 2, 4, 9],
        [14, 0, 11, 5, 4, 12, 18, 8, 10, 13, 16, 7, 6, 1, 3, 9, 15, 17, 2, 19],
        [7, 4, 11, 2, 15, 14, 5, 19, 16, 1, 9, 13, 3, 8, 10, 12, 0, 6, 17, 18],
        [8, 6, 10, 15, 5, 3, 18, 1, 17, 9, 19, 4, 16, 13, 0, 7, 11, 14, 2, 12],
        [10, 17, 6, 8, 7, 19, 2, 0, 3, 5, 4, 1, 14, 16, 9, 18, 12, 11, 15, 13],
        [7, 0, 14, 9, 1, 6, 11, 10, 2, 17, 15, 5, 19, 8, 18, 12, 4, 13, 16, 3],
        [18, 15, 16, 10, 12, 6, 2, 1, 17, 5, 13, 4, 7, 8, 9, 19, 11, 3, 0, 14],
        [0, 6, 12, 4, 8, 1, 5, 17, 15, 2, 7, 9, 11, 13, 16, 3, 10, 18, 14, 19],
        [18, 9, 6, 4, 11, 19, 8, 10, 3, 0, 13, 15, 12, 2, 16, 5, 17, 7, 1, 14],
        [5, 10, 1, 14, 11, 18, 16, 7, 9, 13, 17, 15, 2, 12, 6, 3, 8, 4, 0, 19],
        [5, 6, 8, 3, 15, 19, 4, 2, 16, 14, 13, 10, 1, 7, 18, 9, 0, 11, 12, 17],
        [18, 8, 1, 14, 4, 6, 15, 10, 7, 13, 17, 5, 11, 16, 3, 12, 2, 0, 9, 19],
        [6, 13, 5, 8, 2, 18, 17, 19, 14, 10, 7, 15, 0, 9, 11, 4, 1, 3, 16, 12],
    ],
    'durations': [
        # Job 0
        [Interval(52, 66), Interval(73, 81), Interval(70, 76), Interval(41, 51), Interval(92, 106),
         Interval(7, 7), Interval(10, 12), Interval(73, 77), Interval(27, 27), Interval(20, 24),
         Interval(29, 37), Interval(64, 76), Interval(9, 9), Interval(15, 19), Interval(33, 33),
         Interval(17, 17), Interval(40, 40), Interval(70, 80), Interval(15, 15), Interval(79, 81)],
        # Job 1
        [Interval(15, 17), Interval(23, 27), Interval(8, 8), Interval(37, 45), Interval(43, 53),
         Interval(84, 92), Interval(36, 40), Interval(59, 63), Interval(26, 28), Interval(72, 84),
         Interval(84, 84), Interval(7, 7), Interval(16, 16), Interval(78, 102), Interval(59, 73),
         Interval(41, 41), Interval(3, 3), Interval(46, 48), Interval(31, 35), Interval(57, 57)],
        # Job 2
        [Interval(80, 94), Interval(14, 14), Interval(43, 55), Interval(87, 93), Interval(84, 90),
         Interval(26, 32), Interval(41, 53), Interval(61, 75), Interval(12, 12), Interval(67, 69),
         Interval(66, 66), Interval(50, 66), Interval(60, 74), Interval(85, 93), Interval(29, 35),
         Interval(86, 92), Interval(2, 2), Interval(54, 72), Interval(67, 73), Interval(69, 85)],
        # Job 3
        [Interval(10, 10), Interval(67, 81), Interval(55, 57), Interval(85, 91), Interval(69, 85),
         Interval(71, 87), Interval(68, 70), Interval(39, 45), Interval(12, 12), Interval(72, 80),
         Interval(75, 81), Interval(72, 76), Interval(1, 1), Interval(16, 16), Interval(32, 36),
         Interval(60, 60), Interval(63, 69), Interval(69, 73), Interval(77, 77), Interval(84, 84)],
        # Job 4
        [Interval(81, 109), Interval(23, 25), Interval(75, 97), Interval(54, 68), Interval(62, 72),
         Interval(4, 4), Interval(24, 30), Interval(8, 8), Interval(13, 13), Interval(12, 12),
         Interval(40, 46), Interval(58, 70), Interval(6, 6), Interval(46, 54), Interval(35, 37),
         Interval(40, 52), Interval(71, 71), Interval(80, 82), Interval(38, 46), Interval(4, 4)],
        # Job 5
        [Interval(76, 88), Interval(92, 106), Interval(33, 35), Interval(4, 4), Interval(89, 89),
         Interval(77, 91), Interval(68, 86), Interval(48, 54), Interval(12, 12), Interval(70, 74),
         Interval(33, 41), Interval(4, 4), Interval(16, 20), Interval(88, 94), Interval(87, 111),
         Interval(15, 17), Interval(6, 6), Interval(4, 4), Interval(69, 85), Interval(88, 106)],
        # Job 6
        [Interval(37, 37), Interval(39, 49), Interval(75, 87), Interval(63, 81), Interval(12, 14),
         Interval(57, 75), Interval(47, 57), Interval(68, 68), Interval(4, 4), Interval(14, 14),
         Interval(27, 35), Interval(81, 101), Interval(64, 78), Interval(76, 96), Interval(4, 4),
         Interval(51, 59), Interval(6, 8), Interval(8, 8), Interval(80, 98), Interval(80, 80)],
        # Job 7
        [Interval(32, 36), Interval(29, 35), Interval(52, 58), Interval(59, 73), Interval(17, 19),
         Interval(68, 84), Interval(29, 35), Interval(25, 31), Interval(7, 7), Interval(75, 75),
         Interval(74, 80), Interval(24, 24), Interval(81, 101), Interval(4, 4), Interval(65, 79),
         Interval(76, 92), Interval(46, 54), Interval(43, 47), Interval(22, 28), Interval(6, 6)],
        # Job 8
        [Interval(6, 6), Interval(83, 111), Interval(66, 70), Interval(20, 24), Interval(81, 83),
         Interval(69, 79), Interval(12, 12), Interval(71, 89), Interval(78, 80), Interval(14, 16),
         Interval(43, 53), Interval(84, 98), Interval(47, 55), Interval(19, 19), Interval(63, 85),
         Interval(48, 48), Interval(59, 77), Interval(42, 44), Interval(13, 13), Interval(30, 32)],
        # Job 9
        [Interval(77, 87), Interval(19, 19), Interval(70, 90), Interval(13, 13), Interval(31, 39),
         Interval(93, 103), Interval(63, 73), Interval(11, 13), Interval(1, 1), Interval(15, 15),
         Interval(51, 65), Interval(84, 104), Interval(50, 58), Interval(72, 76), Interval(9, 9),
         Interval(50, 50), Interval(73, 91), Interval(63, 73), Interval(22, 24), Interval(69, 83)],
        # Job 10
        [Interval(71, 87), Interval(19, 21), Interval(71, 77), Interval(39, 47), Interval(76, 100),
         Interval(88, 110), Interval(40, 52), Interval(74, 76), Interval(60, 74), Interval(78, 84),
         Interval(94, 94), Interval(6, 6), Interval(55, 65), Interval(93, 93), Interval(88, 88),
         Interval(38, 40), Interval(28, 36), Interval(86, 90), Interval(69, 91), Interval(27, 33)],
        # Job 11
        [Interval(67, 81), Interval(51, 55), Interval(30, 32), Interval(1, 1), Interval(19, 19),
         Interval(18, 18), Interval(33, 43), Interval(75, 83), Interval(45, 47), Interval(72, 76),
         Interval(73, 91), Interval(79, 89), Interval(24, 30), Interval(44, 48), Interval(11, 11),
         Interval(34, 40), Interval(85, 109), Interval(84, 92), Interval(23, 27), Interval(44, 58)],
        # Job 12
        [Interval(55, 63), Interval(53, 65), Interval(54, 56), Interval(20, 20), Interval(90, 94),
         Interval(1, 1), Interval(31, 31), Interval(59, 63), Interval(81, 93), Interval(9, 11),
         Interval(36, 44), Interval(35, 35), Interval(15, 15), Interval(80, 92), Interval(18, 22),
         Interval(43, 43), Interval(37, 41), Interval(9, 9), Interval(34, 42), Interval(28, 28)],
        # Job 13
        [Interval(26, 26), Interval(2, 2), Interval(81, 81), Interval(61, 67), Interval(9, 9),
         Interval(43, 51), Interval(26, 30), Interval(71, 85), Interval(56, 72), Interval(68, 86),
         Interval(15, 17), Interval(63, 75), Interval(49, 51), Interval(70, 92), Interval(29, 33),
         Interval(86, 88), Interval(37, 47), Interval(23, 23), Interval(46, 46), Interval(40, 50)],
        # Job 14
        [Interval(55, 67), Interval(7, 7), Interval(74, 76), Interval(71, 73), Interval(72, 94),
         Interval(8, 8), Interval(59, 67), Interval(24, 30), Interval(76, 86), Interval(75, 77),
         Interval(56, 58), Interval(7, 7), Interval(77, 99), Interval(58, 66), Interval(5, 5),
         Interval(32, 32), Interval(22, 28), Interval(51, 55), Interval(39, 47), Interval(72, 78)],
        # Job 15
        [Interval(12, 12), Interval(48, 48), Interval(67, 75), Interval(47, 61), Interval(49, 49),
         Interval(43, 51), Interval(37, 37), Interval(69, 75), Interval(34, 44), Interval(69, 85),
         Interval(94, 94), Interval(76, 88), Interval(46, 52), Interval(42, 42), Interval(77, 97),
         Interval(2, 2), Interval(10, 10), Interval(51, 65), Interval(72, 90), Interval(39, 43)],
        # Job 16
        [Interval(78, 90), Interval(35, 37), Interval(95, 101), Interval(10, 10), Interval(20, 24),
         Interval(52, 54), Interval(50, 52), Interval(83, 107), Interval(54, 70), Interval(82, 82),
         Interval(44, 52), Interval(10, 10), Interval(28, 30), Interval(60, 76), Interval(59, 61),
         Interval(5, 5), Interval(41, 41), Interval(15, 15), Interval(77, 91), Interval(44, 46)],
        # Job 17
        [Interval(9, 9), Interval(40, 40), Interval(18, 22), Interval(36, 42), Interval(72, 94),
         Interval(27, 29), Interval(90, 98), Interval(68, 68), Interval(19, 19), Interval(22, 28),
         Interval(12, 14), Interval(59, 67), Interval(62, 76), Interval(17, 17), Interval(67, 81),
         Interval(82, 108), Interval(90, 92), Interval(87, 91), Interval(14, 18), Interval(33, 37)],
        # Job 18
        [Interval(69, 69), Interval(80, 80), Interval(19, 21), Interval(91, 107), Interval(22, 24),
         Interval(8, 8), Interval(41, 45), Interval(33, 35), Interval(31, 39), Interval(82, 84),
         Interval(36, 46), Interval(5, 5), Interval(77, 95), Interval(15, 17), Interval(26, 32),
         Interval(81, 103), Interval(42, 46), Interval(52, 56), Interval(19, 23), Interval(81, 81)],
        # Job 19
        [Interval(82, 82), Interval(84, 110), Interval(5, 5), Interval(36, 36), Interval(37, 43),
         Interval(52, 64), Interval(8, 8), Interval(56, 62), Interval(71, 85), Interval(17, 19),
         Interval(29, 35), Interval(32, 36), Interval(62, 70), Interval(25, 25), Interval(9, 11),
         Interval(35, 37), Interval(83, 93), Interval(44, 56), Interval(82, 82), Interval(31, 39)],
        # Job 20
        [Interval(63, 85), Interval(38, 46), Interval(81, 91), Interval(20, 24), Interval(36, 42),
         Interval(42, 48), Interval(25, 27), Interval(61, 65), Interval(64, 66), Interval(69, 71),
         Interval(32, 34), Interval(35, 43), Interval(71, 77), Interval(66, 84), Interval(8, 8),
         Interval(24, 28), Interval(22, 28), Interval(13, 13), Interval(65, 79), Interval(96, 100)],
        # Job 21
        [Interval(22, 28), Interval(43, 49), Interval(54, 68), Interval(72, 76), Interval(35, 45),
         Interval(25, 25), Interval(41, 43), Interval(5, 5), Interval(2, 2), Interval(63, 67),
         Interval(1, 1), Interval(77, 77), Interval(13, 13), Interval(38, 46), Interval(30, 32),
         Interval(41, 49), Interval(7, 7), Interval(18, 22), Interval(81, 109), Interval(65, 85)],
        # Job 22
        [Interval(47, 53), Interval(71, 85), Interval(68, 76), Interval(48, 58), Interval(66, 68),
         Interval(43, 49), Interval(92, 98), Interval(28, 30), Interval(3, 3), Interval(31, 31),
         Interval(8, 8), Interval(24, 28), Interval(53, 67), Interval(46, 58), Interval(30, 40),
         Interval(56, 58), Interval(49, 65), Interval(89, 93), Interval(86, 96), Interval(31, 39)],
        # Job 23
        [Interval(23, 29), Interval(74, 86), Interval(70, 72), Interval(62, 66), Interval(50, 64),
         Interval(42, 44), Interval(63, 81), Interval(97, 101), Interval(86, 88), Interval(69, 93),
         Interval(14, 16), Interval(20, 26), Interval(72, 74), Interval(7, 7), Interval(68, 72),
         Interval(87, 109), Interval(66, 66), Interval(44, 50), Interval(9, 11), Interval(63, 83)],
        # Job 24
        [Interval(20, 20), Interval(51, 59), Interval(79, 95), Interval(10, 10), Interval(16, 16),
         Interval(55, 63), Interval(88, 94), Interval(72, 92), Interval(53, 53), Interval(60, 74),
         Interval(58, 62), Interval(31, 37), Interval(67, 89), Interval(63, 69), Interval(90, 106),
         Interval(36, 42), Interval(14, 14), Interval(61, 69), Interval(50, 54), Interval(50, 58)],
        # Job 25
        [Interval(3, 3), Interval(25, 27), Interval(8, 8), Interval(38, 46), Interval(69, 71),
         Interval(17, 17), Interval(52, 60), Interval(28, 34), Interval(27, 31), Interval(78, 98),
         Interval(54, 66), Interval(77, 85), Interval(22, 24), Interval(23, 23), Interval(39, 47),
         Interval(25, 33), Interval(73, 75), Interval(25, 33), Interval(29, 31), Interval(57, 69)],
        # Job 26
        [Interval(62, 72), Interval(59, 73), Interval(79, 97), Interval(73, 83), Interval(69, 89),
         Interval(34, 40), Interval(6, 6), Interval(33, 37), Interval(61, 61), Interval(3, 3),
         Interval(62, 72), Interval(46, 56), Interval(60, 68), Interval(68, 70), Interval(59, 71),
         Interval(87, 93), Interval(91, 99), Interval(11, 11), Interval(27, 29), Interval(46, 54)],
        # Job 27
        [Interval(52, 56), Interval(49, 55), Interval(15, 17), Interval(38, 40), Interval(52, 60),
         Interval(45, 57), Interval(46, 52), Interval(66, 74), Interval(51, 67), Interval(66, 66),
         Interval(50, 64), Interval(71, 77), Interval(78, 94), Interval(71, 95), Interval(82, 82),
         Interval(57, 73), Interval(38, 42), Interval(88, 90), Interval(46, 60), Interval(3, 3)],
        # Job 28
        [Interval(65, 71), Interval(43, 45), Interval(54, 70), Interval(24, 26), Interval(65, 73),
         Interval(42, 54), Interval(59, 77), Interval(60, 80), Interval(61, 61), Interval(51, 51),
         Interval(68, 80), Interval(23, 25), Interval(52, 56), Interval(63, 75), Interval(62, 76),
         Interval(31, 35), Interval(61, 61), Interval(17, 19), Interval(32, 40), Interval(71, 85)],
        # Job 29
        [Interval(6, 8), Interval(25, 27), Interval(77, 81), Interval(56, 74), Interval(16, 16),
         Interval(3, 3), Interval(65, 77), Interval(55, 69), Interval(41, 43), Interval(42, 46),
         Interval(69, 77), Interval(77, 81), Interval(9, 9), Interval(57, 65), Interval(56, 70),
         Interval(12, 12), Interval(41, 53), Interval(62, 72), Interval(34, 34), Interval(5, 5)],
    ],
    'name': 'INT__TAI30_20_08.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai30_20_08_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI30_20_08.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI30_20_08.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI30_20_08_F_15_01_INTERVAL_DATA
