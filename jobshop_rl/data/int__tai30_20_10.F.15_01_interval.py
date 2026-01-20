"""
Problema INT__TAI30_20_10.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI30_20_10_F_15_01_INTERVAL_DATA = {
    'num_jobs': 30,
    'num_machines': 20,
    'problem_id': 'int__tai30_20_10.F.15_01_interval',
    'sequences': [
        [2, 8, 6, 0, 4, 15, 16, 13, 5, 12, 10, 7, 14, 19, 1, 3, 18, 17, 9, 11],
        [0, 10, 13, 3, 2, 7, 1, 16, 9, 17, 18, 15, 11, 8, 19, 5, 4, 12, 14, 6],
        [0, 19, 11, 9, 15, 3, 13, 18, 1, 5, 7, 6, 10, 4, 14, 8, 12, 2, 16, 17],
        [7, 19, 10, 11, 9, 14, 6, 12, 16, 13, 5, 15, 4, 3, 17, 8, 1, 18, 2, 0],
        [0, 6, 11, 1, 3, 16, 19, 12, 10, 7, 5, 2, 15, 4, 18, 14, 9, 8, 13, 17],
        [17, 8, 19, 16, 0, 12, 13, 14, 3, 2, 1, 10, 7, 9, 15, 4, 6, 11, 18, 5],
        [18, 1, 9, 11, 17, 0, 2, 6, 16, 10, 4, 14, 19, 12, 15, 7, 3, 5, 8, 13],
        [14, 9, 11, 8, 2, 16, 4, 1, 19, 6, 0, 7, 15, 18, 12, 17, 13, 3, 5, 10],
        [3, 14, 9, 0, 11, 10, 4, 12, 5, 16, 2, 1, 13, 7, 17, 19, 6, 18, 8, 15],
        [13, 7, 9, 0, 3, 8, 11, 4, 5, 14, 15, 6, 2, 17, 1, 10, 19, 18, 16, 12],
        [4, 17, 2, 8, 11, 19, 18, 13, 12, 3, 1, 10, 5, 15, 14, 9, 16, 6, 7, 0],
        [6, 0, 12, 18, 1, 14, 19, 16, 10, 8, 17, 11, 2, 13, 7, 4, 5, 15, 3, 9],
        [2, 7, 13, 0, 19, 4, 9, 11, 16, 3, 5, 6, 14, 18, 12, 15, 10, 1, 17, 8],
        [14, 3, 6, 7, 8, 12, 15, 5, 16, 4, 0, 17, 1, 18, 2, 19, 10, 11, 9, 13],
        [18, 11, 2, 3, 5, 4, 15, 13, 19, 6, 1, 14, 0, 12, 8, 9, 16, 7, 10, 17],
        [10, 13, 16, 8, 17, 11, 7, 5, 14, 15, 6, 3, 0, 19, 18, 2, 4, 12, 1, 9],
        [2, 10, 19, 7, 18, 4, 6, 5, 0, 11, 13, 1, 9, 12, 8, 16, 14, 3, 15, 17],
        [1, 13, 11, 2, 3, 18, 17, 9, 16, 6, 12, 15, 0, 4, 7, 14, 8, 5, 10, 19],
        [18, 10, 12, 16, 1, 11, 8, 19, 9, 17, 5, 2, 13, 14, 7, 6, 15, 0, 3, 4],
        [7, 8, 14, 11, 10, 13, 6, 16, 19, 2, 18, 3, 5, 4, 1, 12, 15, 0, 9, 17],
        [11, 6, 17, 8, 4, 12, 1, 0, 19, 9, 16, 18, 2, 3, 10, 15, 14, 7, 5, 13],
        [16, 19, 4, 5, 3, 18, 15, 8, 13, 0, 10, 14, 11, 1, 12, 2, 9, 6, 17, 7],
        [3, 4, 2, 9, 7, 16, 0, 5, 13, 11, 8, 14, 18, 10, 17, 6, 12, 15, 1, 19],
        [7, 2, 14, 5, 6, 9, 10, 15, 3, 16, 18, 12, 11, 17, 0, 8, 4, 13, 19, 1],
        [17, 11, 18, 7, 12, 4, 10, 3, 8, 13, 2, 9, 15, 19, 6, 1, 16, 14, 5, 0],
        [1, 4, 10, 7, 0, 9, 14, 5, 2, 18, 6, 3, 19, 16, 11, 12, 15, 17, 13, 8],
        [10, 14, 12, 6, 18, 2, 13, 8, 9, 19, 11, 15, 17, 7, 0, 5, 16, 3, 1, 4],
        [14, 13, 1, 5, 17, 2, 4, 18, 3, 12, 19, 0, 10, 9, 11, 8, 7, 15, 16, 6],
        [5, 11, 16, 12, 15, 10, 0, 2, 14, 4, 8, 1, 18, 9, 17, 7, 19, 6, 3, 13],
        [19, 14, 4, 8, 0, 1, 15, 9, 3, 12, 6, 13, 17, 7, 11, 16, 5, 2, 18, 10],
    ],
    'durations': [
        # Job 0
        [Interval(85, 107), Interval(26, 26), Interval(32, 34), Interval(19, 19), Interval(38, 48),
         Interval(17, 17), Interval(26, 26), Interval(57, 75), Interval(78, 90), Interval(54, 58),
         Interval(76, 90), Interval(58, 74), Interval(70, 78), Interval(24, 24), Interval(82, 88),
         Interval(41, 53), Interval(85, 91), Interval(93, 101), Interval(37, 45), Interval(73, 81)],
        # Job 1
        [Interval(68, 72), Interval(41, 51), Interval(85, 95), Interval(53, 69), Interval(23, 25),
         Interval(63, 63), Interval(95, 95), Interval(32, 36), Interval(42, 52), Interval(48, 52),
         Interval(62, 62), Interval(10, 10), Interval(66, 66), Interval(51, 53), Interval(45, 53),
         Interval(4, 4), Interval(81, 107), Interval(34, 42), Interval(82, 104), Interval(84, 84)],
        # Job 2
        [Interval(43, 53), Interval(52, 68), Interval(14, 16), Interval(25, 25), Interval(19, 23),
         Interval(97, 101), Interval(50, 62), Interval(29, 35), Interval(29, 33), Interval(32, 40),
         Interval(74, 74), Interval(66, 78), Interval(80, 102), Interval(26, 32), Interval(31, 37),
         Interval(50, 50), Interval(21, 21), Interval(33, 39), Interval(1, 1), Interval(29, 31)],
        # Job 3
        [Interval(48, 52), Interval(82, 86), Interval(69, 79), Interval(33, 37), Interval(78, 94),
         Interval(40, 44), Interval(30, 32), Interval(59, 65), Interval(81, 83), Interval(65, 67),
         Interval(36, 42), Interval(42, 54), Interval(98, 98), Interval(95, 103), Interval(44, 52),
         Interval(77, 77), Interval(29, 33), Interval(48, 54), Interval(40, 48), Interval(36, 46)],
        # Job 4
        [Interval(77, 103), Interval(24, 30), Interval(29, 31), Interval(58, 78), Interval(23, 27),
         Interval(81, 107), Interval(61, 71), Interval(43, 53), Interval(41, 53), Interval(16, 16),
         Interval(83, 97), Interval(22, 24), Interval(5, 5), Interval(3, 3), Interval(10, 10),
         Interval(37, 37), Interval(69, 79), Interval(26, 30), Interval(24, 26), Interval(84, 88)],
        # Job 5
        [Interval(32, 32), Interval(73, 79), Interval(26, 32), Interval(53, 67), Interval(60, 60),
         Interval(19, 23), Interval(2, 2), Interval(58, 72), Interval(20, 24), Interval(34, 38),
         Interval(76, 84), Interval(55, 67), Interval(52, 58), Interval(75, 93), Interval(87, 111),
         Interval(24, 26), Interval(62, 74), Interval(76, 84), Interval(62, 72), Interval(44, 56)],
        # Job 6
        [Interval(81, 99), Interval(9, 9), Interval(25, 31), Interval(38, 38), Interval(35, 37),
         Interval(19, 19), Interval(4, 4), Interval(44, 48), Interval(74, 94), Interval(67, 75),
         Interval(53, 67), Interval(23, 23), Interval(55, 71), Interval(73, 81), Interval(66, 78),
         Interval(2, 2), Interval(55, 71), Interval(24, 24), Interval(52, 68), Interval(92, 106)],
        # Job 7
        [Interval(84, 108), Interval(75, 81), Interval(74, 84), Interval(87, 93), Interval(55, 71),
         Interval(76, 84), Interval(9, 11), Interval(2, 2), Interval(59, 75), Interval(83, 109),
         Interval(66, 72), Interval(13, 13), Interval(40, 44), Interval(49, 59), Interval(73, 79),
         Interval(31, 33), Interval(66, 84), Interval(49, 55), Interval(92, 104), Interval(15, 17)],
        # Job 8
        [Interval(29, 33), Interval(73, 87), Interval(75, 79), Interval(51, 61), Interval(85, 85),
         Interval(92, 98), Interval(59, 59), Interval(41, 51), Interval(4, 4), Interval(77, 93),
         Interval(37, 47), Interval(13, 15), Interval(4, 4), Interval(38, 42), Interval(39, 41),
         Interval(44, 52), Interval(88, 92), Interval(73, 91), Interval(4, 4), Interval(84, 90)],
        # Job 9
        [Interval(3, 3), Interval(46, 60), Interval(33, 33), Interval(82, 104), Interval(60, 64),
         Interval(16, 18), Interval(59, 71), Interval(21, 25), Interval(10, 10), Interval(39, 49),
         Interval(44, 54), Interval(2, 2), Interval(51, 57), Interval(22, 28), Interval(37, 47),
         Interval(50, 64), Interval(21, 25), Interval(14, 18), Interval(69, 83), Interval(11, 13)],
        # Job 10
        [Interval(63, 73), Interval(47, 61), Interval(67, 83), Interval(26, 32), Interval(26, 32),
         Interval(91, 105), Interval(17, 17), Interval(4, 4), Interval(10, 10), Interval(65, 77),
         Interval(26, 26), Interval(3, 3), Interval(45, 57), Interval(69, 89), Interval(27, 33),
         Interval(56, 60), Interval(72, 80), Interval(72, 90), Interval(61, 65), Interval(57, 63)],
        # Job 11
        [Interval(94, 102), Interval(6, 6), Interval(60, 72), Interval(53, 53), Interval(52, 68),
         Interval(84, 102), Interval(46, 58), Interval(61, 75), Interval(72, 90), Interval(49, 53),
         Interval(81, 89), Interval(67, 81), Interval(12, 12), Interval(23, 23), Interval(38, 48),
         Interval(98, 98), Interval(25, 27), Interval(44, 58), Interval(19, 25), Interval(26, 26)],
        # Job 12
        [Interval(87, 93), Interval(31, 39), Interval(72, 80), Interval(7, 7), Interval(62, 72),
         Interval(10, 10), Interval(37, 45), Interval(37, 45), Interval(18, 18), Interval(41, 41),
         Interval(31, 39), Interval(13, 13), Interval(27, 33), Interval(27, 29), Interval(31, 33),
         Interval(92, 98), Interval(88, 96), Interval(64, 78), Interval(67, 85), Interval(73, 83)],
        # Job 13
        [Interval(31, 31), Interval(56, 72), Interval(21, 21), Interval(68, 76), Interval(78, 78),
         Interval(77, 99), Interval(4, 4), Interval(69, 79), Interval(25, 27), Interval(11, 11),
         Interval(38, 44), Interval(83, 103), Interval(32, 32), Interval(69, 79), Interval(18, 18),
         Interval(35, 39), Interval(27, 29), Interval(42, 52), Interval(89, 107), Interval(62, 68)],
        # Job 14
        [Interval(10, 10), Interval(33, 41), Interval(95, 103), Interval(27, 29), Interval(79, 89),
         Interval(84, 100), Interval(12, 12), Interval(62, 82), Interval(84, 84), Interval(83, 97),
         Interval(31, 39), Interval(36, 44), Interval(56, 70), Interval(26, 32), Interval(82, 96),
         Interval(16, 16), Interval(4, 4), Interval(33, 43), Interval(21, 23), Interval(76, 92)],
        # Job 15
        [Interval(38, 44), Interval(33, 43), Interval(68, 74), Interval(58, 72), Interval(77, 95),
         Interval(30, 30), Interval(53, 61), Interval(69, 73), Interval(21, 27), Interval(10, 10),
         Interval(74, 82), Interval(67, 81), Interval(15, 17), Interval(22, 28), Interval(6, 6),
         Interval(73, 77), Interval(65, 71), Interval(61, 73), Interval(65, 73), Interval(51, 61)],
        # Job 16
        [Interval(45, 47), Interval(73, 85), Interval(31, 41), Interval(13, 13), Interval(3, 3),
         Interval(54, 60), Interval(75, 83), Interval(48, 58), Interval(10, 12), Interval(39, 51),
         Interval(39, 39), Interval(75, 99), Interval(25, 25), Interval(62, 62), Interval(30, 34),
         Interval(13, 13), Interval(21, 23), Interval(93, 93), Interval(88, 92), Interval(86, 94)],
        # Job 17
        [Interval(61, 67), Interval(64, 76), Interval(9, 9), Interval(87, 97), Interval(15, 15),
         Interval(29, 35), Interval(6, 6), Interval(92, 100), Interval(45, 57), Interval(77, 97),
         Interval(43, 55), Interval(73, 77), Interval(79, 89), Interval(1, 1), Interval(10, 10),
         Interval(34, 44), Interval(3, 3), Interval(80, 98), Interval(13, 13), Interval(21, 21)],
        # Job 18
        [Interval(45, 45), Interval(40, 40), Interval(13, 15), Interval(66, 72), Interval(45, 45),
         Interval(97, 99), Interval(85, 95), Interval(18, 20), Interval(35, 45), Interval(2, 2),
         Interval(41, 53), Interval(67, 73), Interval(43, 49), Interval(62, 78), Interval(90, 96),
         Interval(67, 73), Interval(86, 100), Interval(30, 36), Interval(9, 9), Interval(85, 85)],
        # Job 19
        [Interval(12, 14), Interval(80, 90), Interval(29, 35), Interval(27, 33), Interval(61, 79),
         Interval(59, 63), Interval(38, 46), Interval(41, 41), Interval(88, 96), Interval(78, 96),
         Interval(31, 41), Interval(57, 59), Interval(60, 72), Interval(67, 73), Interval(21, 21),
         Interval(22, 22), Interval(38, 44), Interval(87, 89), Interval(78, 104), Interval(91, 97)],
        # Job 20
        [Interval(18, 20), Interval(44, 58), Interval(8, 8), Interval(83, 105), Interval(69, 75),
         Interval(87, 111), Interval(17, 19), Interval(34, 44), Interval(28, 32), Interval(55, 67),
         Interval(18, 20), Interval(66, 82), Interval(2, 2), Interval(73, 81), Interval(66, 66),
         Interval(28, 28), Interval(23, 23), Interval(12, 16), Interval(79, 105), Interval(90, 90)],
        # Job 21
        [Interval(86, 106), Interval(87, 97), Interval(30, 38), Interval(10, 10), Interval(66, 70),
         Interval(89, 99), Interval(59, 65), Interval(71, 95), Interval(23, 29), Interval(81, 93),
         Interval(26, 32), Interval(85, 105), Interval(30, 30), Interval(47, 51), Interval(38, 48),
         Interval(80, 90), Interval(1, 1), Interval(53, 67), Interval(70, 90), Interval(47, 49)],
        # Job 22
        [Interval(38, 46), Interval(14, 14), Interval(53, 57), Interval(83, 111), Interval(60, 70),
         Interval(62, 64), Interval(71, 77), Interval(63, 63), Interval(61, 73), Interval(43, 53),
         Interval(57, 69), Interval(80, 82), Interval(8, 8), Interval(7, 7), Interval(19, 25),
         Interval(40, 46), Interval(53, 53), Interval(21, 23), Interval(88, 98), Interval(84, 94)],
        # Job 23
        [Interval(14, 14), Interval(2, 2), Interval(8, 8), Interval(21, 23), Interval(80, 106),
         Interval(53, 65), Interval(14, 16), Interval(9, 9), Interval(10, 10), Interval(71, 91),
         Interval(77, 93), Interval(54, 70), Interval(66, 74), Interval(61, 67), Interval(92, 94),
         Interval(25, 27), Interval(28, 32), Interval(6, 6), Interval(82, 90), Interval(24, 30)],
        # Job 24
        [Interval(10, 10), Interval(36, 42), Interval(52, 60), Interval(23, 23), Interval(40, 48),
         Interval(86, 100), Interval(82, 98), Interval(93, 105), Interval(79, 81), Interval(43, 51),
         Interval(38, 38), Interval(15, 15), Interval(41, 41), Interval(24, 28), Interval(43, 53),
         Interval(48, 56), Interval(65, 85), Interval(57, 73), Interval(4, 4), Interval(51, 63)],
        # Job 25
        [Interval(44, 48), Interval(70, 86), Interval(9, 11), Interval(13, 13), Interval(32, 32),
         Interval(58, 68), Interval(67, 75), Interval(61, 71), Interval(38, 42), Interval(13, 13),
         Interval(47, 53), Interval(97, 97), Interval(40, 42), Interval(85, 105), Interval(57, 59),
         Interval(51, 63), Interval(58, 68), Interval(37, 47), Interval(54, 58), Interval(31, 31)],
        # Job 26
        [Interval(78, 98), Interval(2, 2), Interval(34, 34), Interval(19, 19), Interval(82, 90),
         Interval(88, 92), Interval(76, 92), Interval(35, 45), Interval(52, 52), Interval(59, 73),
         Interval(76, 76), Interval(59, 65), Interval(24, 30), Interval(25, 31), Interval(5, 5),
         Interval(66, 78), Interval(52, 56), Interval(44, 48), Interval(52, 62), Interval(59, 73)],
        # Job 27
        [Interval(88, 108), Interval(43, 45), Interval(33, 33), Interval(18, 22), Interval(69, 79),
         Interval(30, 30), Interval(4, 4), Interval(86, 90), Interval(18, 20), Interval(74, 96),
         Interval(81, 81), Interval(26, 32), Interval(66, 78), Interval(72, 86), Interval(47, 61),
         Interval(33, 41), Interval(83, 107), Interval(10, 12), Interval(11, 11), Interval(2, 2)],
        # Job 28
        [Interval(48, 48), Interval(30, 38), Interval(23, 27), Interval(24, 28), Interval(47, 59),
         Interval(85, 109), Interval(26, 26), Interval(21, 25), Interval(33, 39), Interval(16, 18),
         Interval(59, 71), Interval(87, 107), Interval(5, 5), Interval(13, 13), Interval(63, 79),
         Interval(29, 35), Interval(24, 28), Interval(6, 6), Interval(45, 49), Interval(54, 60)],
        # Job 29
        [Interval(20, 24), Interval(85, 89), Interval(82, 96), Interval(39, 43), Interval(70, 70),
         Interval(33, 37), Interval(92, 98), Interval(61, 63), Interval(49, 65), Interval(47, 57),
         Interval(18, 18), Interval(87, 101), Interval(60, 60), Interval(34, 34), Interval(75, 99),
         Interval(21, 23), Interval(84, 108), Interval(59, 59), Interval(72, 90), Interval(81, 99)],
    ],
    'name': 'INT__TAI30_20_10.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai30_20_10_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI30_20_10.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI30_20_10.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI30_20_10_F_15_01_INTERVAL_DATA
