"""
Problema INT__TAI30_15_07.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI30_15_07_F_15_01_INTERVAL_DATA = {
    'num_jobs': 30,
    'num_machines': 15,
    'problem_id': 'int__tai30_15_07.F.15_01_interval',
    'sequences': [
        [4, 12, 9, 11, 5, 14, 10, 0, 2, 1, 7, 6, 3, 8, 13],
        [0, 9, 14, 12, 1, 4, 11, 10, 6, 3, 2, 7, 8, 5, 13],
        [0, 5, 3, 8, 7, 14, 12, 13, 9, 4, 10, 2, 11, 6, 1],
        [6, 5, 3, 4, 14, 8, 12, 10, 7, 2, 1, 9, 11, 0, 13],
        [8, 13, 10, 0, 6, 2, 7, 12, 11, 14, 1, 5, 3, 9, 4],
        [5, 9, 13, 2, 11, 0, 7, 14, 4, 6, 12, 10, 8, 1, 3],
        [9, 10, 7, 8, 1, 4, 6, 13, 14, 12, 0, 3, 2, 11, 5],
        [7, 9, 11, 13, 10, 1, 5, 14, 8, 2, 4, 6, 0, 12, 3],
        [10, 3, 2, 14, 12, 13, 8, 6, 11, 0, 1, 9, 7, 5, 4],
        [11, 3, 10, 1, 0, 14, 13, 2, 5, 4, 7, 6, 9, 8, 12],
        [5, 2, 9, 8, 3, 4, 10, 12, 1, 11, 13, 7, 14, 6, 0],
        [13, 14, 1, 0, 9, 2, 4, 11, 3, 5, 12, 6, 8, 10, 7],
        [1, 14, 12, 9, 5, 11, 3, 10, 13, 4, 0, 2, 8, 6, 7],
        [11, 4, 13, 14, 7, 6, 2, 9, 1, 12, 0, 5, 3, 8, 10],
        [6, 13, 0, 5, 11, 9, 3, 12, 2, 8, 10, 4, 14, 1, 7],
        [8, 4, 7, 13, 6, 14, 9, 1, 12, 5, 2, 3, 0, 10, 11],
        [7, 11, 2, 12, 10, 1, 5, 14, 3, 8, 6, 0, 9, 4, 13],
        [6, 8, 9, 13, 10, 3, 14, 12, 7, 1, 4, 0, 5, 2, 11],
        [12, 10, 7, 4, 1, 11, 0, 6, 3, 8, 14, 5, 2, 13, 9],
        [9, 5, 12, 11, 2, 7, 0, 13, 14, 1, 6, 8, 3, 10, 4],
        [7, 3, 13, 8, 6, 11, 2, 14, 4, 9, 10, 1, 5, 0, 12],
        [0, 1, 2, 6, 14, 5, 3, 12, 10, 13, 7, 4, 9, 8, 11],
        [1, 3, 6, 5, 2, 8, 0, 7, 10, 14, 12, 11, 9, 13, 4],
        [6, 11, 9, 13, 3, 0, 1, 10, 12, 2, 14, 4, 7, 5, 8],
        [2, 3, 0, 4, 9, 1, 12, 5, 10, 8, 13, 14, 6, 7, 11],
        [7, 4, 9, 11, 3, 5, 1, 10, 14, 12, 8, 2, 13, 6, 0],
        [9, 12, 7, 5, 2, 10, 4, 14, 8, 6, 1, 0, 3, 11, 13],
        [10, 14, 11, 0, 4, 13, 1, 9, 7, 6, 5, 12, 3, 8, 2],
        [13, 14, 5, 4, 6, 1, 0, 12, 11, 3, 10, 2, 9, 7, 8],
        [14, 6, 8, 2, 7, 5, 11, 10, 4, 0, 3, 13, 1, 12, 9],
    ],
    'durations': [
        # Job 0
        [Interval(82, 110), Interval(43, 51), Interval(38, 42), Interval(68, 68), Interval(42, 56),
         Interval(84, 98), Interval(53, 61), Interval(72, 90), Interval(78, 96), Interval(6, 6),
         Interval(81, 83), Interval(41, 53), Interval(97, 97), Interval(80, 108), Interval(66, 84)],
        # Job 1
        [Interval(42, 42), Interval(52, 58), Interval(70, 94), Interval(58, 64), Interval(57, 77),
         Interval(72, 86), Interval(37, 41), Interval(41, 45), Interval(61, 63), Interval(36, 46),
         Interval(69, 87), Interval(32, 40), Interval(7, 9), Interval(21, 21), Interval(91, 91)],
        # Job 2
        [Interval(49, 55), Interval(24, 32), Interval(43, 53), Interval(24, 26), Interval(2, 2),
         Interval(90, 106), Interval(81, 109), Interval(6, 8), Interval(58, 78), Interval(86, 106),
         Interval(62, 82), Interval(47, 53), Interval(67, 69), Interval(50, 58), Interval(37, 37)],
        # Job 3
        [Interval(69, 93), Interval(56, 62), Interval(44, 48), Interval(61, 61), Interval(42, 44),
         Interval(70, 72), Interval(22, 26), Interval(67, 75), Interval(28, 32), Interval(80, 94),
         Interval(81, 91), Interval(10, 10), Interval(10, 10), Interval(81, 105), Interval(93, 95)],
        # Job 4
        [Interval(30, 30), Interval(64, 78), Interval(58, 72), Interval(12, 14), Interval(29, 31),
         Interval(19, 25), Interval(44, 48), Interval(70, 70), Interval(75, 101), Interval(74, 82),
         Interval(72, 86), Interval(55, 59), Interval(63, 79), Interval(57, 59), Interval(35, 37)],
        # Job 5
        [Interval(67, 69), Interval(28, 36), Interval(28, 36), Interval(13, 17), Interval(91, 105),
         Interval(88, 102), Interval(54, 60), Interval(58, 74), Interval(37, 49), Interval(27, 35),
         Interval(30, 38), Interval(59, 61), Interval(63, 83), Interval(56, 56), Interval(37, 43)],
        # Job 6
        [Interval(24, 30), Interval(37, 47), Interval(21, 27), Interval(12, 12), Interval(21, 23),
         Interval(57, 57), Interval(89, 97), Interval(56, 60), Interval(60, 74), Interval(56, 72),
         Interval(28, 32), Interval(15, 17), Interval(21, 21), Interval(17, 21), Interval(30, 36)],
        # Job 7
        [Interval(42, 44), Interval(47, 55), Interval(49, 57), Interval(57, 67), Interval(53, 63),
         Interval(36, 40), Interval(81, 87), Interval(62, 68), Interval(81, 93), Interval(26, 26),
         Interval(85, 105), Interval(57, 65), Interval(72, 82), Interval(48, 50), Interval(44, 54)],
        # Job 8
        [Interval(93, 93), Interval(77, 85), Interval(54, 56), Interval(51, 67), Interval(69, 71),
         Interval(68, 68), Interval(96, 98), Interval(52, 62), Interval(47, 49), Interval(85, 99),
         Interval(78, 86), Interval(86, 92), Interval(85, 89), Interval(13, 13), Interval(53, 55)],
        # Job 9
        [Interval(59, 61), Interval(31, 35), Interval(62, 70), Interval(85, 107), Interval(23, 23),
         Interval(32, 40), Interval(26, 30), Interval(47, 59), Interval(68, 88), Interval(72, 84),
         Interval(87, 101), Interval(64, 80), Interval(44, 50), Interval(28, 28), Interval(74, 100)],
        # Job 10
        [Interval(96, 100), Interval(80, 98), Interval(25, 29), Interval(33, 35), Interval(87, 89),
         Interval(15, 15), Interval(64, 64), Interval(5, 5), Interval(4, 4), Interval(59, 67),
         Interval(65, 73), Interval(82, 82), Interval(25, 33), Interval(52, 54), Interval(60, 78)],
        # Job 11
        [Interval(90, 104), Interval(76, 98), Interval(47, 53), Interval(64, 72), Interval(65, 87),
         Interval(66, 82), Interval(76, 102), Interval(15, 15), Interval(5, 5), Interval(2, 2),
         Interval(76, 82), Interval(58, 60), Interval(86, 100), Interval(18, 20), Interval(76, 96)],
        # Job 12
        [Interval(51, 69), Interval(41, 53), Interval(12, 14), Interval(62, 62), Interval(85, 105),
         Interval(66, 68), Interval(89, 89), Interval(10, 12), Interval(28, 30), Interval(49, 55),
         Interval(55, 69), Interval(31, 31), Interval(49, 53), Interval(49, 61), Interval(39, 39)],
        # Job 13
        [Interval(70, 82), Interval(92, 92), Interval(84, 86), Interval(18, 22), Interval(59, 63),
         Interval(13, 15), Interval(59, 65), Interval(51, 53), Interval(5, 5), Interval(56, 70),
         Interval(25, 33), Interval(79, 91), Interval(75, 83), Interval(45, 59), Interval(48, 54)],
        # Job 14
        [Interval(56, 66), Interval(42, 48), Interval(84, 102), Interval(45, 57), Interval(84, 110),
         Interval(44, 48), Interval(84, 92), Interval(28, 28), Interval(54, 60), Interval(39, 51),
         Interval(21, 25), Interval(80, 102), Interval(63, 69), Interval(67, 79), Interval(36, 46)],
        # Job 15
        [Interval(49, 49), Interval(52, 64), Interval(28, 36), Interval(30, 30), Interval(55, 63),
         Interval(49, 65), Interval(14, 14), Interval(33, 33), Interval(12, 16), Interval(57, 61),
         Interval(40, 42), Interval(51, 67), Interval(43, 57), Interval(60, 74), Interval(50, 56)],
        # Job 16
        [Interval(94, 94), Interval(47, 57), Interval(6, 8), Interval(47, 55), Interval(7, 9),
         Interval(94, 104), Interval(85, 109), Interval(59, 73), Interval(86, 110), Interval(58, 58),
         Interval(46, 58), Interval(43, 43), Interval(80, 80), Interval(23, 23), Interval(18, 18)],
        # Job 17
        [Interval(91, 103), Interval(55, 59), Interval(69, 75), Interval(91, 103), Interval(11, 13),
         Interval(64, 76), Interval(31, 35), Interval(69, 75), Interval(14, 14), Interval(2, 2),
         Interval(91, 107), Interval(26, 34), Interval(16, 20), Interval(91, 99), Interval(2, 2)],
        # Job 18
        [Interval(61, 67), Interval(64, 86), Interval(59, 67), Interval(13, 15), Interval(51, 59),
         Interval(9, 11), Interval(77, 101), Interval(79, 99), Interval(23, 25), Interval(31, 33),
         Interval(66, 74), Interval(70, 88), Interval(67, 75), Interval(39, 45), Interval(13, 15)],
        # Job 19
        [Interval(1, 1), Interval(70, 94), Interval(25, 29), Interval(19, 25), Interval(38, 50),
         Interval(93, 101), Interval(71, 81), Interval(16, 16), Interval(24, 30), Interval(22, 26),
         Interval(88, 108), Interval(22, 28), Interval(74, 90), Interval(74, 76), Interval(13, 17)],
        # Job 20
        [Interval(24, 28), Interval(4, 4), Interval(16, 20), Interval(51, 51), Interval(43, 51),
         Interval(25, 29), Interval(6, 6), Interval(79, 89), Interval(70, 74), Interval(28, 30),
         Interval(85, 97), Interval(70, 82), Interval(76, 80), Interval(32, 40), Interval(86, 100)],
        # Job 21
        [Interval(34, 36), Interval(39, 39), Interval(76, 102), Interval(50, 56), Interval(74, 96),
         Interval(6, 8), Interval(83, 97), Interval(16, 16), Interval(61, 79), Interval(44, 54),
         Interval(72, 74), Interval(12, 14), Interval(11, 13), Interval(77, 101), Interval(8, 10)],
        # Job 22
        [Interval(49, 63), Interval(40, 40), Interval(46, 56), Interval(43, 51), Interval(74, 80),
         Interval(57, 73), Interval(78, 90), Interval(81, 105), Interval(50, 58), Interval(63, 69),
         Interval(6, 6), Interval(33, 39), Interval(86, 88), Interval(41, 41), Interval(6, 8)],
        # Job 23
        [Interval(53, 59), Interval(1, 1), Interval(51, 63), Interval(43, 47), Interval(3, 3),
         Interval(12, 16), Interval(74, 74), Interval(29, 29), Interval(64, 66), Interval(38, 48),
         Interval(13, 13), Interval(37, 47), Interval(67, 67), Interval(44, 46), Interval(76, 80)],
        # Job 24
        [Interval(75, 87), Interval(70, 74), Interval(93, 105), Interval(45, 59), Interval(64, 74),
         Interval(35, 43), Interval(74, 74), Interval(40, 54), Interval(28, 30), Interval(73, 73),
         Interval(6, 6), Interval(5, 5), Interval(2, 2), Interval(8, 8), Interval(25, 25)],
        # Job 25
        [Interval(16, 18), Interval(57, 71), Interval(95, 99), Interval(90, 98), Interval(88, 110),
         Interval(61, 75), Interval(32, 40), Interval(21, 21), Interval(22, 22), Interval(55, 67),
         Interval(37, 49), Interval(88, 98), Interval(82, 82), Interval(82, 100), Interval(80, 92)],
        # Job 26
        [Interval(17, 23), Interval(26, 30), Interval(84, 112), Interval(6, 8), Interval(17, 19),
         Interval(35, 39), Interval(56, 64), Interval(41, 53), Interval(53, 71), Interval(68, 82),
         Interval(40, 44), Interval(46, 58), Interval(92, 102), Interval(46, 46), Interval(89, 107)],
        # Job 27
        [Interval(8, 10), Interval(15, 15), Interval(84, 86), Interval(54, 56), Interval(6, 8),
         Interval(6, 6), Interval(3, 3), Interval(27, 27), Interval(11, 11), Interval(29, 33),
         Interval(78, 102), Interval(76, 86), Interval(5, 5), Interval(84, 88), Interval(27, 33)],
        # Job 28
        [Interval(53, 53), Interval(76, 98), Interval(91, 95), Interval(57, 67), Interval(17, 21),
         Interval(11, 13), Interval(51, 55), Interval(68, 78), Interval(4, 4), Interval(1, 1),
         Interval(60, 70), Interval(31, 39), Interval(65, 65), Interval(21, 25), Interval(34, 46)],
        # Job 29
        [Interval(13, 13), Interval(22, 22), Interval(33, 35), Interval(5, 5), Interval(68, 68),
         Interval(74, 88), Interval(49, 57), Interval(60, 72), Interval(93, 99), Interval(49, 51),
         Interval(35, 45), Interval(62, 78), Interval(80, 104), Interval(12, 14), Interval(42, 44)],
    ],
    'name': 'INT__TAI30_15_07.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai30_15_07_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI30_15_07.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI30_15_07.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI30_15_07_F_15_01_INTERVAL_DATA
