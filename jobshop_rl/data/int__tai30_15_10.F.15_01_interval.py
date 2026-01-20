"""
Problema INT__TAI30_15_10.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI30_15_10_F_15_01_INTERVAL_DATA = {
    'num_jobs': 30,
    'num_machines': 15,
    'problem_id': 'int__tai30_15_10.F.15_01_interval',
    'sequences': [
        [5, 11, 1, 9, 6, 4, 13, 3, 7, 10, 12, 14, 2, 8, 0],
        [11, 8, 4, 9, 1, 2, 12, 5, 10, 13, 6, 7, 14, 0, 3],
        [9, 2, 0, 13, 10, 6, 11, 3, 8, 14, 12, 5, 7, 4, 1],
        [12, 1, 13, 5, 14, 0, 8, 11, 7, 3, 4, 6, 2, 10, 9],
        [5, 10, 12, 8, 7, 2, 14, 9, 13, 4, 11, 0, 6, 1, 3],
        [4, 11, 2, 14, 12, 5, 10, 8, 1, 6, 9, 0, 13, 3, 7],
        [2, 3, 0, 6, 14, 11, 7, 5, 4, 12, 13, 8, 9, 1, 10],
        [14, 5, 6, 8, 9, 10, 1, 2, 4, 7, 11, 3, 13, 12, 0],
        [13, 2, 10, 0, 6, 9, 8, 7, 4, 14, 5, 1, 3, 11, 12],
        [6, 1, 14, 10, 7, 2, 4, 11, 0, 13, 9, 8, 3, 5, 12],
        [4, 6, 7, 13, 11, 8, 10, 5, 3, 0, 9, 2, 14, 12, 1],
        [5, 13, 9, 2, 0, 12, 14, 7, 1, 10, 3, 6, 11, 8, 4],
        [12, 6, 2, 0, 10, 3, 11, 4, 14, 5, 7, 9, 13, 8, 1],
        [3, 12, 4, 10, 8, 7, 5, 1, 6, 11, 9, 14, 13, 2, 0],
        [10, 6, 11, 5, 13, 3, 1, 12, 0, 14, 8, 2, 7, 9, 4],
        [10, 13, 1, 4, 11, 5, 6, 7, 14, 3, 8, 2, 0, 12, 9],
        [2, 6, 5, 13, 4, 10, 14, 7, 0, 8, 3, 12, 11, 9, 1],
        [14, 13, 2, 1, 4, 9, 11, 0, 3, 12, 8, 7, 6, 5, 10],
        [7, 0, 3, 8, 2, 4, 10, 1, 13, 5, 6, 12, 14, 11, 9],
        [0, 1, 11, 14, 5, 2, 9, 13, 8, 4, 6, 10, 12, 3, 7],
        [12, 11, 13, 10, 14, 4, 8, 1, 9, 3, 7, 5, 0, 6, 2],
        [10, 0, 1, 4, 14, 13, 7, 9, 2, 3, 11, 12, 8, 5, 6],
        [0, 11, 8, 5, 6, 9, 14, 4, 2, 13, 10, 7, 12, 1, 3],
        [12, 5, 1, 7, 13, 4, 8, 11, 0, 10, 6, 14, 9, 2, 3],
        [5, 8, 3, 4, 13, 9, 12, 10, 1, 7, 0, 11, 2, 6, 14],
        [0, 14, 3, 12, 6, 10, 8, 7, 9, 13, 2, 1, 5, 4, 11],
        [8, 4, 14, 7, 2, 13, 11, 12, 0, 5, 6, 3, 9, 10, 1],
        [12, 2, 0, 3, 5, 13, 14, 1, 11, 4, 8, 7, 9, 6, 10],
        [10, 3, 2, 13, 8, 6, 11, 9, 0, 1, 4, 7, 5, 14, 12],
        [5, 10, 11, 4, 0, 2, 3, 9, 13, 8, 12, 7, 6, 14, 1],
    ],
    'durations': [
        # Job 0
        [Interval(65, 87), Interval(4, 4), Interval(90, 106), Interval(1, 1), Interval(48, 54),
         Interval(92, 92), Interval(64, 86), Interval(43, 51), Interval(33, 37), Interval(63, 77),
         Interval(19, 23), Interval(20, 20), Interval(70, 88), Interval(81, 81), Interval(54, 72)],
        # Job 1
        [Interval(63, 79), Interval(85, 85), Interval(3, 3), Interval(43, 47), Interval(12, 14),
         Interval(54, 60), Interval(23, 29), Interval(58, 68), Interval(36, 40), Interval(86, 96),
         Interval(71, 75), Interval(53, 65), Interval(65, 83), Interval(33, 41), Interval(58, 72)],
        # Job 2
        [Interval(60, 60), Interval(74, 74), Interval(33, 37), Interval(63, 83), Interval(44, 54),
         Interval(1, 1), Interval(89, 95), Interval(5, 5), Interval(38, 44), Interval(2, 2),
         Interval(81, 109), Interval(24, 32), Interval(32, 42), Interval(70, 86), Interval(74, 98)],
        # Job 3
        [Interval(90, 100), Interval(72, 74), Interval(22, 24), Interval(77, 77), Interval(40, 54),
         Interval(23, 25), Interval(28, 30), Interval(88, 88), Interval(67, 71), Interval(48, 50),
         Interval(25, 31), Interval(62, 70), Interval(4, 4), Interval(38, 44), Interval(3, 3)],
        # Job 4
        [Interval(26, 30), Interval(25, 27), Interval(68, 74), Interval(78, 84), Interval(31, 41),
         Interval(95, 97), Interval(94, 96), Interval(41, 49), Interval(9, 11), Interval(49, 61),
         Interval(84, 90), Interval(56, 74), Interval(52, 56), Interval(26, 26), Interval(51, 69)],
        # Job 5
        [Interval(38, 42), Interval(33, 39), Interval(5, 5), Interval(75, 81), Interval(55, 71),
         Interval(94, 98), Interval(24, 26), Interval(85, 87), Interval(73, 97), Interval(49, 63),
         Interval(22, 28), Interval(28, 32), Interval(91, 105), Interval(73, 83), Interval(35, 47)],
        # Job 6
        [Interval(78, 102), Interval(13, 17), Interval(78, 100), Interval(85, 89), Interval(45, 59),
         Interval(59, 59), Interval(20, 24), Interval(38, 46), Interval(41, 51), Interval(51, 69),
         Interval(52, 56), Interval(83, 91), Interval(22, 22), Interval(93, 101), Interval(1, 1)],
        # Job 7
        [Interval(49, 53), Interval(67, 83), Interval(2, 2), Interval(76, 96), Interval(18, 20),
         Interval(81, 95), Interval(20, 20), Interval(79, 97), Interval(22, 26), Interval(41, 43),
         Interval(83, 97), Interval(18, 22), Interval(27, 31), Interval(18, 22), Interval(48, 52)],
        # Job 8
        [Interval(11, 11), Interval(92, 100), Interval(86, 98), Interval(91, 97), Interval(70, 86),
         Interval(59, 67), Interval(41, 47), Interval(8, 8), Interval(61, 75), Interval(77, 77),
         Interval(50, 54), Interval(72, 76), Interval(37, 49), Interval(10, 10), Interval(86, 88)],
        # Job 9
        [Interval(74, 76), Interval(72, 84), Interval(27, 27), Interval(25, 29), Interval(78, 86),
         Interval(88, 94), Interval(86, 90), Interval(73, 79), Interval(36, 38), Interval(43, 43),
         Interval(48, 56), Interval(67, 75), Interval(40, 50), Interval(98, 100), Interval(62, 78)],
        # Job 10
        [Interval(43, 51), Interval(7, 9), Interval(87, 111), Interval(78, 92), Interval(10, 12),
         Interval(14, 18), Interval(23, 25), Interval(10, 10), Interval(9, 11), Interval(12, 12),
         Interval(33, 41), Interval(36, 42), Interval(37, 39), Interval(75, 77), Interval(87, 95)],
        # Job 11
        [Interval(62, 62), Interval(92, 104), Interval(64, 72), Interval(14, 14), Interval(49, 65),
         Interval(2, 2), Interval(51, 53), Interval(31, 41), Interval(54, 62), Interval(47, 61),
         Interval(93, 105), Interval(53, 61), Interval(45, 59), Interval(80, 100), Interval(50, 66)],
        # Job 12
        [Interval(53, 53), Interval(6, 6), Interval(63, 67), Interval(66, 70), Interval(49, 57),
         Interval(63, 69), Interval(13, 17), Interval(72, 94), Interval(69, 91), Interval(64, 82),
         Interval(86, 86), Interval(51, 63), Interval(23, 23), Interval(88, 88), Interval(34, 40)],
        # Job 13
        [Interval(71, 75), Interval(61, 69), Interval(48, 60), Interval(95, 95), Interval(12, 12),
         Interval(62, 76), Interval(4, 4), Interval(7, 7), Interval(11, 13), Interval(82, 82),
         Interval(5, 5), Interval(22, 22), Interval(13, 17), Interval(2, 2), Interval(37, 39)],
        # Job 14
        [Interval(54, 64), Interval(47, 51), Interval(29, 29), Interval(61, 77), Interval(69, 89),
         Interval(53, 61), Interval(26, 28), Interval(53, 71), Interval(53, 61), Interval(20, 24),
         Interval(27, 31), Interval(38, 46), Interval(52, 66), Interval(17, 23), Interval(82, 90)],
        # Job 15
        [Interval(77, 85), Interval(24, 24), Interval(52, 58), Interval(82, 108), Interval(2, 2),
         Interval(85, 103), Interval(34, 42), Interval(41, 45), Interval(14, 16), Interval(46, 58),
         Interval(54, 54), Interval(59, 73), Interval(55, 73), Interval(24, 24), Interval(27, 31)],
        # Job 16
        [Interval(17, 23), Interval(25, 25), Interval(70, 70), Interval(6, 6), Interval(3, 3),
         Interval(5, 5), Interval(64, 82), Interval(24, 26), Interval(57, 59), Interval(31, 41),
         Interval(78, 104), Interval(20, 24), Interval(58, 64), Interval(38, 38), Interval(30, 36)],
        # Job 17
        [Interval(55, 67), Interval(18, 22), Interval(19, 23), Interval(21, 23), Interval(19, 25),
         Interval(61, 77), Interval(86, 110), Interval(12, 12), Interval(27, 33), Interval(98, 98),
         Interval(28, 28), Interval(8, 8), Interval(7, 7), Interval(48, 54), Interval(64, 68)],
        # Job 18
        [Interval(73, 81), Interval(3, 3), Interval(11, 11), Interval(21, 25), Interval(51, 61),
         Interval(28, 32), Interval(74, 80), Interval(64, 64), Interval(48, 56), Interval(62, 78),
         Interval(3, 3), Interval(83, 111), Interval(90, 96), Interval(52, 56), Interval(13, 17)],
        # Job 19
        [Interval(1, 1), Interval(21, 23), Interval(94, 104), Interval(31, 37), Interval(42, 54),
         Interval(13, 17), Interval(8, 10), Interval(64, 70), Interval(82, 88), Interval(39, 43),
         Interval(12, 14), Interval(45, 51), Interval(6, 8), Interval(61, 71), Interval(47, 63)],
        # Job 20
        [Interval(41, 47), Interval(81, 107), Interval(29, 37), Interval(27, 29), Interval(22, 24),
         Interval(30, 32), Interval(9, 11), Interval(14, 16), Interval(45, 55), Interval(59, 77),
         Interval(6, 8), Interval(50, 50), Interval(69, 89), Interval(68, 84), Interval(78, 100)],
        # Job 21
        [Interval(73, 73), Interval(2, 2), Interval(69, 83), Interval(25, 27), Interval(47, 53),
         Interval(91, 95), Interval(89, 97), Interval(33, 37), Interval(59, 69), Interval(41, 43),
         Interval(15, 19), Interval(24, 28), Interval(57, 63), Interval(73, 73), Interval(49, 65)],
        # Job 22
        [Interval(75, 83), Interval(49, 63), Interval(19, 25), Interval(36, 42), Interval(27, 27),
         Interval(33, 43), Interval(12, 16), Interval(54, 56), Interval(59, 69), Interval(92, 106),
         Interval(24, 32), Interval(84, 110), Interval(6, 8), Interval(91, 93), Interval(64, 78)],
        # Job 23
        [Interval(2, 2), Interval(3, 3), Interval(31, 35), Interval(71, 77), Interval(60, 78),
         Interval(54, 62), Interval(86, 112), Interval(74, 84), Interval(80, 88), Interval(84, 100),
         Interval(97, 99), Interval(41, 41), Interval(33, 41), Interval(12, 12), Interval(11, 13)],
        # Job 24
        [Interval(44, 48), Interval(20, 26), Interval(48, 48), Interval(68, 70), Interval(70, 72),
         Interval(8, 10), Interval(94, 94), Interval(39, 49), Interval(1, 1), Interval(26, 26),
         Interval(91, 95), Interval(53, 55), Interval(22, 26), Interval(75, 79), Interval(42, 46)],
        # Job 25
        [Interval(71, 95), Interval(80, 92), Interval(6, 6), Interval(54, 68), Interval(39, 39),
         Interval(63, 81), Interval(1, 1), Interval(8, 8), Interval(17, 17), Interval(60, 60),
         Interval(40, 42), Interval(15, 17), Interval(19, 23), Interval(21, 21), Interval(6, 6)],
        # Job 26
        [Interval(27, 29), Interval(53, 65), Interval(56, 68), Interval(86, 108), Interval(51, 53),
         Interval(57, 59), Interval(44, 54), Interval(71, 95), Interval(11, 11), Interval(49, 49),
         Interval(22, 26), Interval(52, 60), Interval(37, 49), Interval(31, 37), Interval(20, 26)],
        # Job 27
        [Interval(69, 81), Interval(77, 87), Interval(70, 80), Interval(88, 100), Interval(59, 75),
         Interval(13, 17), Interval(21, 25), Interval(54, 60), Interval(4, 4), Interval(45, 57),
         Interval(22, 24), Interval(40, 40), Interval(57, 69), Interval(89, 105), Interval(19, 21)],
        # Job 28
        [Interval(14, 14), Interval(33, 33), Interval(14, 18), Interval(14, 14), Interval(24, 24),
         Interval(1, 1), Interval(18, 22), Interval(83, 109), Interval(70, 80), Interval(35, 37),
         Interval(83, 101), Interval(73, 75), Interval(12, 14), Interval(77, 81), Interval(44, 52)],
        # Job 29
        [Interval(30, 36), Interval(79, 99), Interval(84, 94), Interval(45, 53), Interval(53, 63),
         Interval(29, 35), Interval(95, 95), Interval(59, 69), Interval(10, 12), Interval(13, 13),
         Interval(43, 43), Interval(96, 100), Interval(32, 32), Interval(51, 61), Interval(57, 67)],
    ],
    'name': 'INT__TAI30_15_10.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai30_15_10_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI30_15_10.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI30_15_10.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI30_15_10_F_15_01_INTERVAL_DATA
