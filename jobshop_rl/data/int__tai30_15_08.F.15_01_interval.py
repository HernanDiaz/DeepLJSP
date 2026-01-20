"""
Problema INT__TAI30_15_08.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI30_15_08_F_15_01_INTERVAL_DATA = {
    'num_jobs': 30,
    'num_machines': 15,
    'problem_id': 'int__tai30_15_08.F.15_01_interval',
    'sequences': [
        [2, 13, 1, 9, 8, 12, 4, 10, 11, 3, 6, 7, 14, 5, 0],
        [6, 3, 0, 10, 13, 7, 4, 14, 11, 5, 1, 8, 12, 9, 2],
        [4, 6, 12, 11, 0, 7, 14, 13, 5, 1, 9, 8, 10, 2, 3],
        [11, 4, 14, 0, 1, 9, 2, 8, 5, 10, 12, 3, 7, 13, 6],
        [0, 5, 11, 1, 7, 4, 14, 13, 2, 6, 3, 9, 8, 12, 10],
        [11, 5, 3, 2, 0, 1, 4, 12, 7, 8, 13, 14, 9, 6, 10],
        [11, 9, 6, 7, 2, 14, 12, 5, 1, 3, 10, 13, 4, 8, 0],
        [4, 11, 8, 2, 5, 6, 12, 7, 13, 0, 9, 1, 10, 3, 14],
        [1, 2, 12, 7, 5, 13, 10, 9, 4, 14, 0, 8, 11, 6, 3],
        [11, 12, 8, 7, 10, 3, 6, 9, 2, 1, 0, 13, 4, 5, 14],
        [3, 2, 14, 7, 9, 6, 10, 0, 11, 1, 5, 8, 12, 13, 4],
        [1, 5, 13, 6, 8, 10, 3, 2, 12, 0, 9, 4, 14, 7, 11],
        [2, 8, 13, 5, 9, 0, 12, 1, 6, 3, 7, 11, 14, 4, 10],
        [11, 12, 9, 13, 10, 4, 5, 7, 8, 3, 2, 0, 1, 14, 6],
        [11, 13, 12, 7, 6, 5, 0, 1, 3, 9, 4, 8, 14, 10, 2],
        [0, 2, 1, 6, 9, 3, 12, 5, 13, 8, 7, 4, 14, 10, 11],
        [14, 8, 1, 3, 13, 4, 0, 2, 10, 11, 12, 6, 7, 9, 5],
        [3, 5, 10, 1, 4, 6, 8, 14, 7, 11, 12, 9, 13, 2, 0],
        [0, 12, 1, 13, 3, 4, 9, 14, 11, 10, 8, 5, 2, 7, 6],
        [1, 9, 13, 7, 0, 10, 2, 11, 14, 12, 8, 6, 4, 3, 5],
        [4, 2, 3, 12, 13, 10, 6, 7, 9, 8, 14, 11, 5, 0, 1],
        [8, 11, 3, 6, 12, 2, 10, 9, 7, 4, 13, 14, 0, 5, 1],
        [4, 1, 6, 10, 8, 3, 11, 12, 2, 9, 0, 5, 14, 13, 7],
        [13, 9, 5, 12, 6, 8, 3, 1, 7, 2, 11, 14, 4, 10, 0],
        [3, 10, 14, 5, 11, 7, 8, 13, 1, 6, 4, 9, 12, 0, 2],
        [0, 12, 6, 1, 4, 9, 7, 10, 14, 5, 13, 11, 8, 3, 2],
        [10, 2, 0, 5, 4, 9, 13, 14, 12, 8, 7, 3, 1, 6, 11],
        [9, 3, 8, 13, 4, 6, 14, 5, 2, 12, 0, 10, 11, 1, 7],
        [14, 2, 6, 10, 1, 5, 11, 7, 0, 9, 13, 4, 12, 8, 3],
        [6, 7, 12, 5, 4, 9, 1, 13, 2, 10, 8, 14, 11, 0, 3],
    ],
    'durations': [
        # Job 0
        [Interval(69, 93), Interval(54, 64), Interval(8, 8), Interval(88, 88), Interval(12, 16),
         Interval(17, 19), Interval(21, 23), Interval(47, 57), Interval(68, 82), Interval(33, 33),
         Interval(20, 26), Interval(69, 69), Interval(36, 48), Interval(23, 29), Interval(54, 54)],
        # Job 1
        [Interval(4, 4), Interval(75, 83), Interval(65, 87), Interval(56, 62), Interval(36, 48),
         Interval(26, 30), Interval(70, 80), Interval(57, 63), Interval(40, 42), Interval(12, 16),
         Interval(87, 111), Interval(52, 64), Interval(36, 46), Interval(66, 66), Interval(1, 1)],
        # Job 2
        [Interval(37, 37), Interval(59, 67), Interval(40, 52), Interval(71, 87), Interval(37, 39),
         Interval(41, 47), Interval(16, 20), Interval(40, 50), Interval(47, 63), Interval(70, 86),
         Interval(68, 90), Interval(26, 28), Interval(6, 6), Interval(21, 21), Interval(66, 74)],
        # Job 3
        [Interval(58, 58), Interval(54, 72), Interval(53, 59), Interval(26, 28), Interval(37, 37),
         Interval(50, 52), Interval(37, 37), Interval(28, 34), Interval(23, 25), Interval(68, 78),
         Interval(6, 8), Interval(68, 76), Interval(33, 35), Interval(31, 33), Interval(23, 31)],
        # Job 4
        [Interval(94, 96), Interval(33, 33), Interval(73, 89), Interval(20, 26), Interval(24, 28),
         Interval(12, 12), Interval(28, 36), Interval(57, 63), Interval(89, 89), Interval(67, 89),
         Interval(19, 21), Interval(32, 38), Interval(34, 36), Interval(30, 38), Interval(17, 17)],
        # Job 5
        [Interval(61, 67), Interval(11, 11), Interval(50, 66), Interval(61, 79), Interval(28, 34),
         Interval(68, 80), Interval(76, 88), Interval(29, 33), Interval(57, 73), Interval(78, 102),
         Interval(54, 72), Interval(71, 91), Interval(78, 82), Interval(60, 80), Interval(82, 82)],
        # Job 6
        [Interval(91, 107), Interval(25, 31), Interval(55, 71), Interval(70, 92), Interval(82, 90),
         Interval(10, 10), Interval(7, 7), Interval(17, 17), Interval(21, 23), Interval(41, 49),
         Interval(81, 103), Interval(1, 1), Interval(35, 39), Interval(34, 40), Interval(42, 44)],
        # Job 7
        [Interval(78, 94), Interval(84, 100), Interval(72, 76), Interval(86, 100), Interval(38, 46),
         Interval(26, 30), Interval(54, 64), Interval(73, 81), Interval(78, 84), Interval(39, 43),
         Interval(11, 11), Interval(44, 46), Interval(55, 69), Interval(21, 23), Interval(54, 60)],
        # Job 8
        [Interval(12, 12), Interval(81, 99), Interval(70, 70), Interval(85, 93), Interval(36, 38),
         Interval(48, 64), Interval(21, 21), Interval(74, 74), Interval(62, 64), Interval(36, 42),
         Interval(37, 37), Interval(76, 90), Interval(74, 82), Interval(64, 68), Interval(6, 6)],
        # Job 9
        [Interval(37, 39), Interval(64, 70), Interval(27, 27), Interval(11, 11), Interval(41, 49),
         Interval(20, 22), Interval(65, 81), Interval(47, 47), Interval(28, 34), Interval(22, 26),
         Interval(52, 66), Interval(80, 102), Interval(43, 49), Interval(44, 52), Interval(37, 47)],
        # Job 10
        [Interval(60, 66), Interval(17, 17), Interval(51, 67), Interval(27, 27), Interval(73, 89),
         Interval(6, 8), Interval(19, 19), Interval(52, 52), Interval(71, 77), Interval(9, 9),
         Interval(47, 53), Interval(55, 63), Interval(41, 41), Interval(55, 73), Interval(94, 98)],
        # Job 11
        [Interval(71, 91), Interval(85, 97), Interval(9, 11), Interval(43, 49), Interval(61, 69),
         Interval(63, 83), Interval(53, 65), Interval(80, 106), Interval(75, 75), Interval(45, 49),
         Interval(60, 62), Interval(80, 92), Interval(62, 68), Interval(26, 32), Interval(18, 24)],
        # Job 12
        [Interval(55, 71), Interval(8, 10), Interval(81, 81), Interval(33, 41), Interval(32, 32),
         Interval(62, 62), Interval(85, 101), Interval(61, 65), Interval(50, 56), Interval(89, 109),
         Interval(62, 62), Interval(10, 10), Interval(77, 93), Interval(43, 43), Interval(23, 27)],
        # Job 13
        [Interval(26, 26), Interval(46, 46), Interval(6, 8), Interval(49, 51), Interval(62, 74),
         Interval(77, 85), Interval(86, 90), Interval(59, 73), Interval(79, 101), Interval(47, 55),
         Interval(59, 65), Interval(25, 33), Interval(81, 93), Interval(38, 44), Interval(8, 8)],
        # Job 14
        [Interval(81, 99), Interval(7, 9), Interval(55, 71), Interval(54, 60), Interval(22, 24),
         Interval(5, 5), Interval(20, 20), Interval(6, 6), Interval(30, 32), Interval(36, 48),
         Interval(78, 94), Interval(67, 85), Interval(93, 103), Interval(41, 49), Interval(76, 96)],
        # Job 15
        [Interval(11, 11), Interval(83, 105), Interval(36, 48), Interval(94, 96), Interval(40, 46),
         Interval(44, 58), Interval(41, 43), Interval(39, 39), Interval(72, 92), Interval(1, 1),
         Interval(92, 100), Interval(35, 37), Interval(63, 85), Interval(63, 85), Interval(66, 82)],
        # Job 16
        [Interval(12, 12), Interval(77, 77), Interval(12, 14), Interval(28, 34), Interval(8, 10),
         Interval(36, 42), Interval(54, 60), Interval(22, 28), Interval(49, 61), Interval(52, 68),
         Interval(87, 87), Interval(49, 61), Interval(85, 85), Interval(12, 12), Interval(77, 79)],
        # Job 17
        [Interval(53, 57), Interval(4, 4), Interval(12, 12), Interval(40, 44), Interval(44, 48),
         Interval(83, 95), Interval(40, 48), Interval(31, 35), Interval(14, 16), Interval(70, 76),
         Interval(47, 47), Interval(66, 78), Interval(71, 91), Interval(68, 90), Interval(6, 6)],
        # Job 18
        [Interval(74, 80), Interval(42, 46), Interval(53, 71), Interval(16, 18), Interval(67, 73),
         Interval(18, 20), Interval(60, 78), Interval(61, 79), Interval(27, 33), Interval(93, 101),
         Interval(79, 85), Interval(34, 38), Interval(17, 21), Interval(31, 35), Interval(46, 54)],
        # Job 19
        [Interval(91, 105), Interval(36, 48), Interval(4, 4), Interval(24, 28), Interval(73, 95),
         Interval(29, 39), Interval(3, 3), Interval(57, 61), Interval(49, 55), Interval(68, 72),
         Interval(44, 54), Interval(38, 46), Interval(6, 6), Interval(6, 8), Interval(6, 6)],
        # Job 20
        [Interval(2, 2), Interval(73, 95), Interval(1, 1), Interval(69, 83), Interval(10, 10),
         Interval(2, 2), Interval(65, 85), Interval(9, 11), Interval(85, 109), Interval(3, 3),
         Interval(18, 18), Interval(49, 57), Interval(29, 33), Interval(79, 89), Interval(17, 17)],
        # Job 21
        [Interval(60, 66), Interval(6, 6), Interval(72, 82), Interval(79, 91), Interval(20, 20),
         Interval(25, 31), Interval(75, 87), Interval(73, 79), Interval(33, 33), Interval(65, 87),
         Interval(26, 28), Interval(75, 99), Interval(12, 14), Interval(34, 40), Interval(61, 63)],
        # Job 22
        [Interval(17, 23), Interval(63, 77), Interval(87, 91), Interval(55, 65), Interval(59, 69),
         Interval(34, 44), Interval(58, 76), Interval(68, 88), Interval(7, 7), Interval(42, 50),
         Interval(23, 27), Interval(47, 51), Interval(23, 31), Interval(71, 81), Interval(85, 111)],
        # Job 23
        [Interval(3, 3), Interval(21, 23), Interval(9, 9), Interval(61, 71), Interval(39, 39),
         Interval(51, 51), Interval(27, 33), Interval(88, 96), Interval(83, 105), Interval(8, 8),
         Interval(21, 27), Interval(27, 27), Interval(87, 89), Interval(9, 9), Interval(57, 73)],
        # Job 24
        [Interval(79, 79), Interval(30, 36), Interval(62, 62), Interval(83, 87), Interval(17, 17),
         Interval(59, 69), Interval(64, 68), Interval(2, 2), Interval(67, 75), Interval(75, 101),
         Interval(59, 69), Interval(3, 3), Interval(40, 48), Interval(60, 60), Interval(6, 6)],
        # Job 25
        [Interval(79, 103), Interval(23, 25), Interval(5, 5), Interval(31, 31), Interval(53, 53),
         Interval(52, 54), Interval(7, 9), Interval(13, 17), Interval(11, 11), Interval(51, 55),
         Interval(20, 24), Interval(74, 92), Interval(45, 55), Interval(79, 83), Interval(52, 52)],
        # Job 26
        [Interval(78, 96), Interval(53, 71), Interval(79, 89), Interval(91, 91), Interval(48, 58),
         Interval(16, 18), Interval(63, 81), Interval(12, 14), Interval(79, 105), Interval(85, 99),
         Interval(15, 17), Interval(13, 13), Interval(13, 13), Interval(61, 77), Interval(38, 50)],
        # Job 27
        [Interval(75, 91), Interval(59, 65), Interval(53, 69), Interval(25, 27), Interval(14, 14),
         Interval(63, 75), Interval(31, 37), Interval(59, 63), Interval(12, 12), Interval(2, 2),
         Interval(27, 27), Interval(46, 56), Interval(64, 64), Interval(14, 14), Interval(75, 89)],
        # Job 28
        [Interval(47, 61), Interval(77, 87), Interval(66, 70), Interval(75, 91), Interval(70, 72),
         Interval(71, 91), Interval(6, 6), Interval(41, 43), Interval(20, 24), Interval(19, 25),
         Interval(83, 105), Interval(24, 26), Interval(49, 57), Interval(5, 5), Interval(64, 76)],
        # Job 29
        [Interval(60, 74), Interval(72, 72), Interval(43, 51), Interval(30, 40), Interval(73, 83),
         Interval(34, 34), Interval(65, 69), Interval(86, 86), Interval(81, 97), Interval(63, 75),
         Interval(42, 50), Interval(55, 59), Interval(84, 90), Interval(20, 24), Interval(77, 97)],
    ],
    'name': 'INT__TAI30_15_08.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai30_15_08_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI30_15_08.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI30_15_08.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI30_15_08_F_15_01_INTERVAL_DATA
