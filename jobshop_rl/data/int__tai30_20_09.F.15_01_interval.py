"""
Problema INT__TAI30_20_09.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI30_20_09_F_15_01_INTERVAL_DATA = {
    'num_jobs': 30,
    'num_machines': 20,
    'problem_id': 'int__tai30_20_09.F.15_01_interval',
    'sequences': [
        [8, 10, 5, 13, 11, 17, 19, 18, 9, 15, 3, 16, 0, 12, 7, 2, 1, 14, 6, 4],
        [14, 18, 1, 2, 13, 9, 16, 6, 19, 17, 7, 8, 3, 10, 0, 11, 15, 5, 12, 4],
        [9, 6, 13, 10, 5, 15, 2, 8, 19, 1, 4, 18, 11, 7, 16, 12, 0, 3, 14, 17],
        [14, 3, 10, 16, 18, 1, 17, 0, 6, 8, 2, 11, 19, 5, 7, 15, 12, 9, 4, 13],
        [5, 16, 11, 9, 17, 10, 18, 15, 0, 19, 6, 4, 13, 2, 1, 14, 3, 12, 7, 8],
        [7, 9, 1, 2, 4, 6, 10, 18, 17, 8, 5, 0, 19, 15, 14, 13, 11, 12, 3, 16],
        [0, 12, 1, 14, 18, 6, 8, 17, 10, 2, 19, 5, 16, 11, 7, 13, 9, 3, 15, 4],
        [16, 14, 18, 11, 1, 10, 5, 9, 7, 2, 12, 15, 17, 8, 0, 4, 19, 3, 6, 13],
        [10, 19, 18, 15, 8, 0, 2, 9, 13, 3, 6, 7, 12, 11, 1, 4, 5, 16, 14, 17],
        [9, 14, 10, 19, 8, 12, 7, 6, 18, 2, 11, 0, 13, 15, 16, 1, 17, 4, 3, 5],
        [3, 4, 18, 15, 6, 2, 16, 7, 5, 12, 9, 17, 0, 8, 1, 10, 14, 11, 19, 13],
        [2, 4, 1, 15, 16, 3, 17, 6, 11, 12, 7, 18, 8, 13, 0, 14, 19, 10, 9, 5],
        [16, 19, 10, 9, 14, 12, 18, 2, 17, 15, 6, 7, 5, 11, 1, 0, 4, 3, 8, 13],
        [12, 3, 17, 4, 8, 9, 2, 11, 13, 5, 18, 10, 6, 7, 1, 15, 16, 14, 0, 19],
        [7, 0, 18, 19, 15, 2, 9, 1, 10, 6, 3, 11, 13, 12, 8, 4, 16, 17, 5, 14],
        [1, 19, 14, 7, 17, 0, 13, 11, 16, 12, 10, 9, 6, 3, 18, 8, 15, 5, 4, 2],
        [10, 17, 9, 16, 18, 4, 2, 11, 5, 15, 8, 3, 7, 0, 12, 6, 14, 19, 13, 1],
        [12, 11, 7, 9, 19, 16, 17, 6, 15, 13, 10, 4, 1, 8, 5, 0, 2, 3, 14, 18],
        [15, 17, 10, 4, 14, 1, 3, 18, 8, 16, 6, 2, 0, 7, 11, 12, 5, 13, 19, 9],
        [0, 11, 17, 10, 15, 5, 12, 9, 6, 3, 4, 1, 7, 14, 16, 2, 8, 13, 18, 19],
        [13, 6, 4, 8, 18, 12, 0, 5, 3, 9, 1, 14, 11, 16, 2, 15, 7, 19, 17, 10],
        [8, 6, 14, 12, 0, 9, 10, 2, 18, 19, 13, 5, 17, 1, 11, 7, 4, 15, 3, 16],
        [12, 16, 8, 4, 19, 9, 13, 6, 3, 2, 10, 5, 14, 11, 15, 1, 17, 18, 0, 7],
        [10, 18, 8, 15, 6, 7, 2, 0, 11, 5, 17, 12, 14, 9, 13, 3, 4, 1, 19, 16],
        [6, 16, 4, 15, 0, 12, 7, 10, 5, 13, 17, 3, 14, 18, 1, 19, 8, 2, 9, 11],
        [13, 19, 0, 5, 14, 8, 10, 17, 15, 12, 18, 3, 16, 11, 6, 1, 7, 2, 9, 4],
        [16, 18, 11, 15, 17, 4, 9, 1, 10, 5, 13, 3, 8, 0, 14, 2, 19, 12, 7, 6],
        [7, 0, 18, 16, 6, 13, 17, 5, 14, 11, 9, 19, 3, 12, 4, 8, 10, 15, 1, 2],
        [17, 16, 9, 1, 0, 15, 11, 5, 3, 18, 12, 14, 13, 2, 7, 19, 10, 8, 4, 6],
        [7, 1, 16, 17, 3, 13, 0, 19, 6, 10, 9, 8, 15, 18, 5, 2, 11, 14, 12, 4],
    ],
    'durations': [
        # Job 0
        [Interval(17, 17), Interval(36, 48), Interval(3, 3), Interval(71, 83), Interval(51, 55),
         Interval(62, 68), Interval(13, 15), Interval(13, 15), Interval(74, 80), Interval(19, 25),
         Interval(26, 26), Interval(48, 58), Interval(34, 38), Interval(60, 72), Interval(26, 26),
         Interval(52, 60), Interval(13, 15), Interval(41, 41), Interval(60, 78), Interval(74, 96)],
        # Job 1
        [Interval(54, 60), Interval(87, 99), Interval(73, 97), Interval(18, 22), Interval(91, 97),
         Interval(3, 3), Interval(54, 64), Interval(76, 84), Interval(40, 40), Interval(73, 93),
         Interval(67, 67), Interval(55, 55), Interval(25, 25), Interval(22, 26), Interval(70, 78),
         Interval(46, 48), Interval(35, 39), Interval(97, 99), Interval(8, 10), Interval(76, 92)],
        # Job 2
        [Interval(2, 2), Interval(55, 69), Interval(35, 35), Interval(85, 89), Interval(33, 41),
         Interval(72, 86), Interval(4, 4), Interval(71, 87), Interval(55, 67), Interval(32, 38),
         Interval(37, 41), Interval(26, 26), Interval(24, 24), Interval(17, 17), Interval(8, 8),
         Interval(77, 99), Interval(38, 40), Interval(25, 25), Interval(91, 93), Interval(42, 54)],
        # Job 3
        [Interval(48, 54), Interval(27, 33), Interval(72, 86), Interval(26, 28), Interval(24, 26),
         Interval(12, 14), Interval(3, 3), Interval(21, 25), Interval(16, 18), Interval(19, 25),
         Interval(45, 45), Interval(13, 13), Interval(70, 74), Interval(48, 56), Interval(55, 57),
         Interval(53, 59), Interval(74, 94), Interval(16, 16), Interval(49, 51), Interval(58, 70)],
        # Job 4
        [Interval(69, 75), Interval(78, 82), Interval(4, 4), Interval(7, 7), Interval(78, 92),
         Interval(29, 31), Interval(70, 80), Interval(45, 49), Interval(94, 94), Interval(10, 12),
         Interval(73, 77), Interval(61, 65), Interval(55, 61), Interval(57, 69), Interval(4, 4),
         Interval(32, 34), Interval(41, 53), Interval(71, 85), Interval(8, 8), Interval(20, 20)],
        # Job 5
        [Interval(29, 35), Interval(77, 87), Interval(42, 48), Interval(14, 14), Interval(10, 10),
         Interval(52, 68), Interval(98, 98), Interval(92, 98), Interval(55, 67), Interval(84, 92),
         Interval(57, 75), Interval(78, 80), Interval(92, 104), Interval(39, 49), Interval(47, 49),
         Interval(26, 28), Interval(41, 53), Interval(28, 34), Interval(12, 14), Interval(45, 55)],
        # Job 6
        [Interval(30, 34), Interval(51, 55), Interval(32, 34), Interval(68, 72), Interval(54, 64),
         Interval(35, 47), Interval(92, 98), Interval(61, 69), Interval(88, 94), Interval(7, 7),
         Interval(18, 20), Interval(72, 92), Interval(87, 99), Interval(54, 58), Interval(42, 46),
         Interval(47, 47), Interval(30, 34), Interval(62, 62), Interval(49, 55), Interval(14, 16)],
        # Job 7
        [Interval(5, 5), Interval(41, 47), Interval(94, 94), Interval(18, 22), Interval(32, 38),
         Interval(65, 85), Interval(92, 92), Interval(28, 32), Interval(60, 78), Interval(4, 4),
         Interval(89, 109), Interval(70, 72), Interval(18, 18), Interval(1, 1), Interval(73, 77),
         Interval(41, 47), Interval(30, 40), Interval(34, 40), Interval(48, 58), Interval(83, 109)],
        # Job 8
        [Interval(56, 64), Interval(53, 55), Interval(36, 46), Interval(40, 50), Interval(75, 83),
         Interval(19, 19), Interval(50, 56), Interval(89, 93), Interval(1, 1), Interval(70, 78),
         Interval(15, 17), Interval(49, 63), Interval(68, 82), Interval(95, 95), Interval(85, 95),
         Interval(75, 97), Interval(55, 61), Interval(42, 42), Interval(78, 80), Interval(8, 8)],
        # Job 9
        [Interval(73, 83), Interval(50, 62), Interval(23, 25), Interval(53, 67), Interval(84, 92),
         Interval(44, 50), Interval(31, 35), Interval(11, 11), Interval(79, 105), Interval(62, 82),
         Interval(42, 42), Interval(76, 100), Interval(30, 30), Interval(54, 60), Interval(96, 98),
         Interval(23, 27), Interval(25, 27), Interval(5, 5), Interval(61, 63), Interval(45, 45)],
        # Job 10
        [Interval(86, 104), Interval(59, 65), Interval(47, 59), Interval(66, 72), Interval(44, 46),
         Interval(46, 50), Interval(49, 49), Interval(59, 59), Interval(33, 41), Interval(23, 23),
         Interval(88, 100), Interval(19, 19), Interval(71, 87), Interval(70, 92), Interval(9, 9),
         Interval(64, 68), Interval(30, 34), Interval(16, 18), Interval(34, 42), Interval(54, 64)],
        # Job 11
        [Interval(57, 65), Interval(63, 83), Interval(77, 81), Interval(23, 27), Interval(74, 76),
         Interval(5, 5), Interval(73, 79), Interval(23, 29), Interval(69, 69), Interval(16, 20),
         Interval(21, 21), Interval(21, 21), Interval(16, 16), Interval(36, 42), Interval(15, 15),
         Interval(64, 64), Interval(93, 103), Interval(65, 75), Interval(54, 54), Interval(32, 32)],
        # Job 12
        [Interval(46, 46), Interval(83, 105), Interval(32, 34), Interval(23, 25), Interval(29, 33),
         Interval(49, 65), Interval(57, 57), Interval(8, 8), Interval(88, 88), Interval(51, 59),
         Interval(68, 70), Interval(51, 51), Interval(93, 95), Interval(42, 44), Interval(34, 36),
         Interval(60, 62), Interval(13, 15), Interval(27, 33), Interval(74, 94), Interval(77, 81)],
        # Job 13
        [Interval(87, 107), Interval(7, 7), Interval(53, 65), Interval(87, 87), Interval(54, 60),
         Interval(36, 38), Interval(4, 4), Interval(2, 2), Interval(21, 25), Interval(44, 46),
         Interval(66, 80), Interval(65, 79), Interval(96, 100), Interval(74, 84), Interval(58, 64),
         Interval(14, 16), Interval(80, 80), Interval(73, 81), Interval(13, 17), Interval(73, 79)],
        # Job 14
        [Interval(50, 56), Interval(57, 75), Interval(37, 47), Interval(58, 60), Interval(6, 6),
         Interval(56, 64), Interval(26, 34), Interval(58, 60), Interval(54, 72), Interval(56, 66),
         Interval(74, 92), Interval(13, 15), Interval(69, 87), Interval(83, 97), Interval(36, 40),
         Interval(86, 90), Interval(20, 20), Interval(20, 26), Interval(79, 83), Interval(64, 64)],
        # Job 15
        [Interval(75, 75), Interval(36, 40), Interval(15, 15), Interval(47, 49), Interval(34, 40),
         Interval(90, 94), Interval(96, 102), Interval(32, 42), Interval(73, 85), Interval(26, 30),
         Interval(60, 76), Interval(19, 21), Interval(6, 6), Interval(52, 62), Interval(68, 90),
         Interval(88, 106), Interval(66, 86), Interval(11, 11), Interval(6, 6), Interval(93, 97)],
        # Job 16
        [Interval(70, 78), Interval(41, 49), Interval(87, 99), Interval(9, 9), Interval(56, 60),
         Interval(15, 17), Interval(24, 30), Interval(17, 21), Interval(19, 19), Interval(63, 75),
         Interval(82, 82), Interval(23, 27), Interval(31, 31), Interval(47, 55), Interval(74, 96),
         Interval(42, 42), Interval(10, 10), Interval(82, 88), Interval(84, 86), Interval(25, 29)],
        # Job 17
        [Interval(28, 32), Interval(5, 5), Interval(48, 60), Interval(3, 3), Interval(63, 63),
         Interval(45, 49), Interval(54, 64), Interval(44, 46), Interval(63, 63), Interval(37, 43),
         Interval(10, 10), Interval(16, 16), Interval(36, 48), Interval(43, 49), Interval(57, 75),
         Interval(31, 37), Interval(1, 1), Interval(14, 16), Interval(73, 89), Interval(69, 69)],
        # Job 18
        [Interval(98, 98), Interval(80, 98), Interval(42, 48), Interval(11, 11), Interval(12, 12),
         Interval(47, 51), Interval(44, 44), Interval(92, 104), Interval(13, 17), Interval(77, 81),
         Interval(94, 102), Interval(46, 50), Interval(17, 21), Interval(82, 98), Interval(20, 20),
         Interval(19, 21), Interval(13, 13), Interval(70, 86), Interval(29, 35), Interval(35, 43)],
        # Job 19
        [Interval(20, 20), Interval(4, 4), Interval(64, 66), Interval(90, 108), Interval(54, 58),
         Interval(59, 63), Interval(45, 45), Interval(90, 96), Interval(30, 34), Interval(44, 44),
         Interval(55, 69), Interval(90, 98), Interval(50, 64), Interval(56, 60), Interval(43, 45),
         Interval(85, 91), Interval(1, 1), Interval(56, 74), Interval(69, 77), Interval(55, 73)],
        # Job 20
        [Interval(14, 16), Interval(64, 78), Interval(38, 40), Interval(28, 34), Interval(28, 36),
         Interval(69, 91), Interval(48, 60), Interval(34, 42), Interval(47, 55), Interval(48, 52),
         Interval(52, 64), Interval(90, 102), Interval(94, 98), Interval(9, 9), Interval(64, 66),
         Interval(31, 33), Interval(18, 20), Interval(48, 60), Interval(7, 7), Interval(10, 10)],
        # Job 21
        [Interval(46, 60), Interval(18, 20), Interval(63, 73), Interval(95, 103), Interval(73, 81),
         Interval(11, 13), Interval(74, 88), Interval(85, 107), Interval(44, 48), Interval(51, 61),
         Interval(37, 45), Interval(7, 9), Interval(89, 97), Interval(9, 11), Interval(67, 83),
         Interval(66, 84), Interval(84, 86), Interval(30, 34), Interval(69, 91), Interval(76, 92)],
        # Job 22
        [Interval(93, 99), Interval(9, 9), Interval(40, 44), Interval(52, 52), Interval(63, 69),
         Interval(71, 89), Interval(41, 49), Interval(79, 103), Interval(29, 33), Interval(37, 43),
         Interval(12, 12), Interval(56, 64), Interval(89, 109), Interval(55, 59), Interval(59, 77),
         Interval(42, 46), Interval(14, 18), Interval(48, 62), Interval(6, 6), Interval(83, 85)],
        # Job 23
        [Interval(89, 107), Interval(28, 30), Interval(68, 82), Interval(37, 43), Interval(74, 88),
         Interval(70, 76), Interval(62, 78), Interval(26, 32), Interval(74, 96), Interval(3, 3),
         Interval(76, 102), Interval(11, 13), Interval(1, 1), Interval(43, 49), Interval(28, 32),
         Interval(25, 31), Interval(72, 92), Interval(9, 11), Interval(17, 19), Interval(94, 100)],
        # Job 24
        [Interval(20, 22), Interval(41, 53), Interval(2, 2), Interval(58, 68), Interval(49, 65),
         Interval(23, 27), Interval(23, 27), Interval(76, 84), Interval(66, 74), Interval(44, 44),
         Interval(7, 7), Interval(28, 32), Interval(59, 65), Interval(50, 60), Interval(66, 70),
         Interval(52, 60), Interval(1, 1), Interval(23, 27), Interval(5, 5), Interval(12, 14)],
        # Job 25
        [Interval(38, 44), Interval(6, 6), Interval(7, 7), Interval(69, 91), Interval(87, 99),
         Interval(12, 12), Interval(53, 55), Interval(12, 12), Interval(36, 40), Interval(27, 33),
         Interval(65, 71), Interval(34, 38), Interval(18, 20), Interval(46, 46), Interval(67, 75),
         Interval(63, 79), Interval(90, 98), Interval(57, 75), Interval(95, 103), Interval(51, 63)],
        # Job 26
        [Interval(49, 65), Interval(53, 57), Interval(43, 49), Interval(14, 16), Interval(58, 64),
         Interval(59, 69), Interval(19, 19), Interval(13, 15), Interval(49, 49), Interval(52, 64),
         Interval(49, 59), Interval(49, 59), Interval(50, 50), Interval(31, 33), Interval(39, 41),
         Interval(45, 49), Interval(64, 76), Interval(89, 105), Interval(46, 54), Interval(58, 72)],
        # Job 27
        [Interval(48, 58), Interval(32, 32), Interval(2, 2), Interval(84, 86), Interval(15, 19),
         Interval(94, 94), Interval(42, 50), Interval(79, 87), Interval(56, 70), Interval(64, 70),
         Interval(45, 47), Interval(78, 90), Interval(31, 37), Interval(22, 22), Interval(21, 27),
         Interval(67, 73), Interval(55, 71), Interval(13, 15), Interval(75, 77), Interval(61, 73)],
        # Job 28
        [Interval(23, 27), Interval(74, 92), Interval(79, 95), Interval(47, 53), Interval(55, 65),
         Interval(59, 67), Interval(86, 86), Interval(5, 5), Interval(11, 11), Interval(24, 30),
         Interval(8, 8), Interval(30, 34), Interval(15, 17), Interval(46, 52), Interval(18, 22),
         Interval(37, 47), Interval(52, 66), Interval(13, 13), Interval(82, 90), Interval(38, 38)],
        # Job 29
        [Interval(62, 66), Interval(18, 22), Interval(27, 35), Interval(14, 14), Interval(49, 51),
         Interval(82, 104), Interval(68, 76), Interval(64, 84), Interval(12, 14), Interval(37, 47),
         Interval(17, 19), Interval(23, 27), Interval(71, 95), Interval(29, 37), Interval(21, 21),
         Interval(86, 98), Interval(47, 49), Interval(57, 63), Interval(4, 4), Interval(78, 82)],
    ],
    'name': 'INT__TAI30_20_09.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai30_20_09_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI30_20_09.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI30_20_09.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI30_20_09_F_15_01_INTERVAL_DATA
