"""
Problema INT__TAI30_20_02.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI30_20_02_F_15_01_INTERVAL_DATA = {
    'num_jobs': 30,
    'num_machines': 20,
    'problem_id': 'int__tai30_20_02.F.15_01_interval',
    'sequences': [
        [4, 10, 12, 5, 3, 8, 19, 15, 6, 0, 11, 13, 1, 16, 17, 18, 2, 14, 7, 9],
        [6, 1, 2, 13, 11, 3, 12, 14, 10, 19, 7, 18, 16, 17, 15, 5, 0, 4, 9, 8],
        [17, 15, 8, 16, 1, 10, 13, 14, 6, 12, 0, 9, 5, 18, 2, 4, 3, 19, 11, 7],
        [7, 1, 2, 17, 16, 8, 9, 4, 15, 14, 6, 18, 13, 3, 0, 11, 19, 12, 5, 10],
        [10, 1, 7, 3, 17, 0, 2, 18, 12, 16, 6, 13, 11, 8, 15, 19, 9, 14, 5, 4],
        [4, 8, 3, 9, 12, 2, 6, 18, 5, 19, 1, 11, 17, 0, 13, 16, 14, 7, 15, 10],
        [17, 4, 13, 19, 15, 3, 2, 1, 7, 16, 8, 10, 12, 6, 11, 9, 14, 18, 5, 0],
        [10, 1, 0, 17, 18, 7, 16, 6, 15, 12, 2, 11, 4, 8, 14, 5, 19, 13, 3, 9],
        [17, 0, 9, 7, 4, 2, 5, 18, 11, 12, 14, 13, 19, 3, 8, 10, 1, 15, 6, 16],
        [11, 1, 9, 16, 12, 3, 6, 13, 10, 14, 8, 19, 4, 18, 0, 5, 17, 15, 2, 7],
        [19, 18, 14, 10, 13, 5, 3, 11, 8, 7, 16, 0, 6, 4, 2, 12, 9, 15, 17, 1],
        [5, 18, 6, 9, 17, 12, 3, 14, 15, 0, 19, 4, 2, 1, 10, 8, 16, 11, 13, 7],
        [2, 0, 5, 18, 19, 9, 7, 10, 11, 4, 8, 15, 17, 1, 14, 6, 12, 13, 16, 3],
        [10, 12, 4, 8, 13, 17, 2, 19, 15, 16, 3, 0, 6, 5, 1, 11, 18, 14, 7, 9],
        [1, 16, 19, 0, 17, 15, 2, 9, 3, 6, 10, 18, 7, 14, 13, 8, 12, 11, 4, 5],
        [2, 14, 9, 16, 3, 0, 4, 12, 13, 19, 17, 15, 8, 18, 11, 7, 6, 1, 5, 10],
        [17, 8, 19, 7, 4, 18, 12, 13, 3, 11, 6, 9, 1, 5, 10, 15, 0, 14, 2, 16],
        [13, 2, 6, 14, 18, 7, 8, 0, 16, 1, 3, 10, 19, 4, 12, 11, 5, 15, 17, 9],
        [15, 19, 11, 0, 4, 10, 7, 1, 8, 6, 9, 18, 14, 13, 3, 12, 2, 5, 16, 17],
        [17, 8, 4, 10, 12, 0, 11, 9, 7, 16, 18, 19, 1, 13, 3, 6, 2, 14, 15, 5],
        [8, 1, 11, 19, 16, 5, 17, 7, 2, 15, 12, 0, 9, 3, 13, 6, 4, 10, 14, 18],
        [16, 13, 0, 1, 10, 15, 14, 8, 17, 18, 19, 2, 4, 12, 7, 6, 9, 11, 3, 5],
        [7, 6, 4, 17, 15, 14, 19, 8, 10, 0, 3, 12, 16, 5, 13, 9, 18, 2, 1, 11],
        [9, 1, 4, 11, 17, 16, 12, 14, 6, 2, 15, 5, 10, 0, 8, 13, 18, 3, 7, 19],
        [12, 3, 14, 10, 0, 4, 11, 5, 15, 9, 2, 6, 8, 13, 18, 17, 1, 16, 7, 19],
        [13, 8, 4, 6, 3, 7, 19, 2, 5, 9, 18, 11, 10, 16, 0, 1, 14, 12, 17, 15],
        [10, 0, 1, 13, 12, 11, 5, 8, 19, 2, 3, 7, 4, 6, 17, 9, 15, 16, 14, 18],
        [16, 19, 13, 3, 15, 1, 8, 14, 12, 2, 5, 17, 0, 9, 11, 10, 18, 4, 6, 7],
        [11, 4, 8, 13, 5, 3, 18, 1, 17, 14, 12, 9, 6, 19, 10, 2, 0, 7, 15, 16],
        [16, 11, 14, 8, 19, 5, 17, 12, 3, 15, 13, 18, 9, 6, 1, 0, 7, 10, 4, 2],
    ],
    'durations': [
        # Job 0
        [Interval(11, 11), Interval(42, 48), Interval(30, 38), Interval(57, 65), Interval(8, 8),
         Interval(89, 105), Interval(52, 66), Interval(70, 74), Interval(74, 90), Interval(57, 57),
         Interval(78, 96), Interval(60, 62), Interval(85, 95), Interval(4, 4), Interval(15, 19),
         Interval(67, 71), Interval(92, 98), Interval(14, 16), Interval(92, 102), Interval(87, 99)],
        # Job 1
        [Interval(49, 65), Interval(62, 66), Interval(14, 16), Interval(19, 19), Interval(14, 14),
         Interval(54, 54), Interval(69, 73), Interval(29, 29), Interval(17, 17), Interval(42, 44),
         Interval(80, 82), Interval(86, 88), Interval(62, 68), Interval(62, 62), Interval(71, 89),
         Interval(68, 82), Interval(17, 21), Interval(41, 55), Interval(32, 34), Interval(61, 75)],
        # Job 2
        [Interval(68, 74), Interval(1, 1), Interval(78, 102), Interval(74, 88), Interval(78, 90),
         Interval(17, 21), Interval(66, 84), Interval(75, 91), Interval(24, 26), Interval(65, 73),
         Interval(1, 1), Interval(69, 91), Interval(31, 39), Interval(74, 78), Interval(37, 37),
         Interval(23, 23), Interval(12, 14), Interval(4, 4), Interval(71, 91), Interval(18, 22)],
        # Job 3
        [Interval(14, 18), Interval(80, 102), Interval(22, 22), Interval(25, 31), Interval(83, 95),
         Interval(95, 103), Interval(61, 77), Interval(21, 23), Interval(85, 85), Interval(24, 26),
         Interval(55, 65), Interval(33, 33), Interval(15, 19), Interval(6, 6), Interval(94, 94),
         Interval(53, 59), Interval(8, 8), Interval(68, 86), Interval(47, 61), Interval(71, 93)],
        # Job 4
        [Interval(3, 3), Interval(49, 53), Interval(42, 44), Interval(20, 22), Interval(64, 68),
         Interval(68, 74), Interval(16, 18), Interval(95, 101), Interval(70, 76), Interval(73, 79),
         Interval(93, 93), Interval(80, 96), Interval(58, 64), Interval(76, 82), Interval(9, 9),
         Interval(18, 18), Interval(27, 35), Interval(74, 86), Interval(4, 4), Interval(30, 34)],
        # Job 5
        [Interval(41, 47), Interval(85, 109), Interval(7, 7), Interval(50, 58), Interval(12, 12),
         Interval(63, 73), Interval(24, 28), Interval(38, 46), Interval(17, 21), Interval(82, 102),
         Interval(51, 63), Interval(67, 75), Interval(62, 72), Interval(2, 2), Interval(48, 50),
         Interval(38, 42), Interval(46, 56), Interval(27, 27), Interval(34, 36), Interval(21, 23)],
        # Job 6
        [Interval(5, 5), Interval(48, 62), Interval(2, 2), Interval(6, 6), Interval(59, 71),
         Interval(39, 45), Interval(18, 20), Interval(64, 64), Interval(48, 54), Interval(4, 4),
         Interval(12, 14), Interval(44, 48), Interval(51, 53), Interval(38, 38), Interval(14, 16),
         Interval(76, 98), Interval(67, 81), Interval(57, 71), Interval(69, 91), Interval(80, 102)],
        # Job 7
        [Interval(83, 101), Interval(38, 40), Interval(21, 27), Interval(71, 71), Interval(11, 13),
         Interval(33, 41), Interval(56, 72), Interval(16, 18), Interval(95, 95), Interval(48, 56),
         Interval(9, 9), Interval(3, 3), Interval(87, 87), Interval(42, 50), Interval(62, 80),
         Interval(28, 30), Interval(22, 22), Interval(59, 65), Interval(41, 45), Interval(46, 56)],
        # Job 8
        [Interval(68, 88), Interval(79, 103), Interval(23, 29), Interval(81, 81), Interval(40, 46),
         Interval(40, 46), Interval(86, 100), Interval(35, 35), Interval(34, 38), Interval(68, 80),
         Interval(18, 18), Interval(30, 30), Interval(14, 16), Interval(57, 71), Interval(79, 101),
         Interval(66, 84), Interval(33, 41), Interval(31, 39), Interval(38, 40), Interval(84, 90)],
        # Job 9
        [Interval(12, 16), Interval(20, 22), Interval(66, 82), Interval(26, 34), Interval(56, 68),
         Interval(60, 80), Interval(84, 90), Interval(29, 29), Interval(85, 87), Interval(83, 93),
         Interval(24, 24), Interval(49, 59), Interval(11, 11), Interval(15, 15), Interval(20, 22),
         Interval(29, 29), Interval(55, 59), Interval(72, 78), Interval(50, 64), Interval(38, 48)],
        # Job 10
        [Interval(35, 45), Interval(31, 37), Interval(41, 51), Interval(94, 100), Interval(61, 73),
         Interval(52, 66), Interval(63, 67), Interval(43, 51), Interval(20, 20), Interval(21, 23),
         Interval(15, 15), Interval(63, 69), Interval(19, 21), Interval(39, 41), Interval(65, 79),
         Interval(72, 74), Interval(46, 54), Interval(4, 4), Interval(85, 91), Interval(43, 45)],
        # Job 11
        [Interval(32, 34), Interval(9, 9), Interval(77, 91), Interval(64, 76), Interval(52, 60),
         Interval(58, 62), Interval(15, 17), Interval(83, 85), Interval(13, 13), Interval(43, 51),
         Interval(63, 67), Interval(69, 83), Interval(45, 57), Interval(33, 35), Interval(48, 58),
         Interval(61, 65), Interval(13, 15), Interval(81, 87), Interval(72, 84), Interval(85, 99)],
        # Job 12
        [Interval(61, 73), Interval(17, 19), Interval(58, 74), Interval(36, 38), Interval(57, 73),
         Interval(85, 99), Interval(27, 33), Interval(52, 62), Interval(1, 1), Interval(14, 18),
         Interval(79, 99), Interval(36, 36), Interval(27, 33), Interval(48, 50), Interval(7, 7),
         Interval(64, 82), Interval(18, 22), Interval(26, 26), Interval(25, 33), Interval(39, 45)],
        # Job 13
        [Interval(90, 108), Interval(69, 75), Interval(20, 24), Interval(68, 90), Interval(57, 63),
         Interval(25, 31), Interval(55, 63), Interval(95, 95), Interval(74, 94), Interval(45, 53),
         Interval(74, 98), Interval(34, 40), Interval(10, 10), Interval(64, 72), Interval(69, 71),
         Interval(20, 20), Interval(68, 74), Interval(20, 26), Interval(64, 78), Interval(49, 53)],
        # Job 14
        [Interval(37, 41), Interval(86, 90), Interval(77, 87), Interval(35, 47), Interval(86, 112),
         Interval(45, 45), Interval(10, 12), Interval(43, 53), Interval(2, 2), Interval(8, 8),
         Interval(82, 94), Interval(89, 101), Interval(56, 72), Interval(7, 7), Interval(56, 68),
         Interval(17, 21), Interval(57, 65), Interval(54, 66), Interval(40, 50), Interval(31, 33)],
        # Job 15
        [Interval(76, 86), Interval(16, 20), Interval(74, 80), Interval(30, 36), Interval(17, 17),
         Interval(8, 10), Interval(5, 5), Interval(73, 79), Interval(66, 84), Interval(57, 73),
         Interval(11, 11), Interval(68, 70), Interval(17, 17), Interval(58, 74), Interval(36, 36),
         Interval(20, 26), Interval(67, 83), Interval(56, 72), Interval(13, 15), Interval(37, 47)],
        # Job 16
        [Interval(47, 47), Interval(49, 53), Interval(52, 68), Interval(89, 99), Interval(15, 15),
         Interval(13, 13), Interval(8, 8), Interval(16, 16), Interval(60, 62), Interval(63, 81),
         Interval(69, 69), Interval(17, 17), Interval(39, 49), Interval(83, 85), Interval(93, 101),
         Interval(93, 93), Interval(84, 98), Interval(53, 67), Interval(99, 99), Interval(55, 59)],
        # Job 17
        [Interval(25, 31), Interval(70, 70), Interval(36, 48), Interval(87, 105), Interval(14, 14),
         Interval(76, 86), Interval(53, 61), Interval(15, 17), Interval(43, 47), Interval(40, 48),
         Interval(36, 44), Interval(10, 12), Interval(63, 77), Interval(92, 102), Interval(19, 21),
         Interval(73, 87), Interval(23, 25), Interval(25, 29), Interval(55, 55), Interval(12, 14)],
        # Job 18
        [Interval(80, 104), Interval(4, 4), Interval(28, 34), Interval(70, 82), Interval(89, 93),
         Interval(65, 67), Interval(58, 60), Interval(94, 100), Interval(13, 17), Interval(26, 28),
         Interval(15, 15), Interval(60, 64), Interval(78, 86), Interval(92, 96), Interval(53, 57),
         Interval(47, 57), Interval(74, 80), Interval(39, 39), Interval(35, 41), Interval(47, 59)],
        # Job 19
        [Interval(17, 17), Interval(97, 101), Interval(46, 48), Interval(71, 93), Interval(13, 15),
         Interval(2, 2), Interval(79, 85), Interval(60, 78), Interval(6, 6), Interval(77, 101),
         Interval(64, 68), Interval(34, 44), Interval(9, 9), Interval(89, 91), Interval(82, 100),
         Interval(57, 69), Interval(12, 14), Interval(32, 36), Interval(33, 39), Interval(79, 83)],
        # Job 20
        [Interval(92, 106), Interval(67, 69), Interval(49, 63), Interval(61, 79), Interval(65, 79),
         Interval(72, 82), Interval(48, 54), Interval(61, 67), Interval(59, 73), Interval(54, 60),
         Interval(72, 76), Interval(9, 9), Interval(63, 81), Interval(81, 107), Interval(58, 68),
         Interval(20, 22), Interval(38, 40), Interval(22, 24), Interval(74, 86), Interval(8, 8)],
        # Job 21
        [Interval(64, 70), Interval(20, 24), Interval(56, 62), Interval(36, 38), Interval(6, 6),
         Interval(64, 64), Interval(16, 18), Interval(49, 51), Interval(42, 48), Interval(30, 30),
         Interval(7, 7), Interval(71, 85), Interval(70, 74), Interval(34, 38), Interval(22, 24),
         Interval(90, 98), Interval(25, 25), Interval(71, 77), Interval(6, 6), Interval(96, 98)],
        # Job 22
        [Interval(37, 47), Interval(86, 94), Interval(25, 31), Interval(18, 20), Interval(7, 7),
         Interval(89, 105), Interval(78, 86), Interval(39, 43), Interval(64, 74), Interval(46, 48),
         Interval(70, 82), Interval(78, 98), Interval(11, 11), Interval(66, 70), Interval(62, 78),
         Interval(28, 34), Interval(8, 8), Interval(77, 85), Interval(3, 3), Interval(82, 86)],
        # Job 23
        [Interval(61, 63), Interval(34, 34), Interval(89, 107), Interval(63, 67), Interval(12, 12),
         Interval(64, 68), Interval(32, 32), Interval(57, 63), Interval(12, 12), Interval(74, 96),
         Interval(65, 81), Interval(47, 63), Interval(83, 111), Interval(24, 24), Interval(8, 10),
         Interval(23, 29), Interval(79, 105), Interval(3, 3), Interval(36, 46), Interval(79, 87)],
        # Job 24
        [Interval(11, 13), Interval(81, 105), Interval(69, 79), Interval(20, 20), Interval(30, 36),
         Interval(82, 96), Interval(36, 46), Interval(94, 98), Interval(4, 4), Interval(96, 102),
         Interval(42, 52), Interval(23, 23), Interval(12, 12), Interval(88, 94), Interval(22, 28),
         Interval(79, 87), Interval(31, 37), Interval(75, 91), Interval(65, 75), Interval(25, 29)],
        # Job 25
        [Interval(93, 105), Interval(46, 54), Interval(17, 17), Interval(9, 9), Interval(66, 78),
         Interval(87, 95), Interval(36, 38), Interval(36, 42), Interval(70, 74), Interval(30, 32),
         Interval(64, 80), Interval(95, 99), Interval(36, 44), Interval(37, 49), Interval(91, 101),
         Interval(45, 57), Interval(28, 30), Interval(21, 21), Interval(17, 19), Interval(44, 56)],
        # Job 26
        [Interval(52, 58), Interval(37, 45), Interval(4, 4), Interval(72, 78), Interval(82, 90),
         Interval(56, 62), Interval(39, 49), Interval(66, 80), Interval(65, 67), Interval(64, 76),
         Interval(72, 86), Interval(81, 89), Interval(47, 55), Interval(5, 5), Interval(35, 35),
         Interval(16, 18), Interval(27, 33), Interval(35, 35), Interval(33, 35), Interval(82, 100)],
        # Job 27
        [Interval(85, 109), Interval(29, 35), Interval(39, 43), Interval(30, 36), Interval(23, 23),
         Interval(36, 42), Interval(65, 83), Interval(43, 55), Interval(65, 73), Interval(26, 30),
         Interval(48, 62), Interval(56, 64), Interval(54, 68), Interval(73, 95), Interval(2, 2),
         Interval(73, 95), Interval(17, 17), Interval(69, 77), Interval(23, 29), Interval(83, 99)],
        # Job 28
        [Interval(21, 21), Interval(49, 53), Interval(91, 107), Interval(70, 88), Interval(19, 23),
         Interval(45, 51), Interval(42, 46), Interval(66, 68), Interval(46, 50), Interval(91, 101),
         Interval(18, 20), Interval(39, 39), Interval(56, 56), Interval(74, 78), Interval(15, 17),
         Interval(39, 41), Interval(61, 77), Interval(87, 99), Interval(15, 15), Interval(49, 55)],
        # Job 29
        [Interval(41, 49), Interval(22, 22), Interval(86, 92), Interval(36, 48), Interval(41, 45),
         Interval(99, 99), Interval(91, 91), Interval(33, 35), Interval(42, 44), Interval(67, 69),
         Interval(72, 80), Interval(48, 62), Interval(1, 1), Interval(70, 76), Interval(50, 62),
         Interval(82, 96), Interval(13, 13), Interval(96, 102), Interval(72, 92), Interval(64, 80)],
    ],
    'name': 'INT__TAI30_20_02.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai30_20_02_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI30_20_02.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI30_20_02.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI30_20_02_F_15_01_INTERVAL_DATA
