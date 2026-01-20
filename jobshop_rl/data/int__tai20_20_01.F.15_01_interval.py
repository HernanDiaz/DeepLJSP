"""
Problema INT__TAI20_20_01.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI20_20_01_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 20,
    'problem_id': 'int__tai20_20_01.F.15_01_interval',
    'sequences': [
        [6, 1, 15, 2, 19, 13, 16, 18, 3, 12, 14, 5, 10, 7, 8, 9, 0, 17, 11, 4],
        [8, 6, 10, 9, 19, 1, 0, 17, 2, 11, 7, 13, 18, 15, 4, 14, 5, 3, 16, 12],
        [1, 3, 4, 12, 0, 14, 7, 19, 10, 11, 5, 18, 13, 15, 16, 8, 9, 2, 17, 6],
        [18, 15, 10, 1, 19, 9, 2, 12, 4, 0, 13, 16, 14, 11, 3, 5, 8, 17, 6, 7],
        [2, 10, 12, 15, 7, 14, 17, 5, 8, 1, 13, 0, 3, 16, 4, 9, 11, 18, 6, 19],
        [0, 16, 10, 9, 17, 8, 5, 3, 19, 11, 15, 2, 14, 4, 12, 13, 1, 6, 7, 18],
        [11, 0, 1, 19, 9, 10, 8, 17, 18, 16, 4, 3, 12, 7, 6, 15, 5, 14, 2, 13],
        [16, 3, 8, 10, 18, 7, 1, 14, 19, 2, 12, 6, 5, 11, 17, 4, 13, 9, 15, 0],
        [17, 18, 15, 11, 10, 12, 14, 3, 1, 0, 16, 9, 6, 19, 7, 8, 4, 2, 13, 5],
        [9, 5, 3, 2, 11, 4, 16, 14, 7, 13, 1, 18, 8, 15, 12, 6, 17, 19, 0, 10],
        [5, 9, 18, 0, 3, 16, 6, 1, 2, 11, 15, 19, 7, 8, 4, 10, 12, 17, 14, 13],
        [11, 5, 9, 4, 3, 15, 17, 7, 18, 19, 13, 1, 6, 12, 10, 0, 14, 16, 2, 8],
        [15, 3, 4, 7, 18, 13, 19, 9, 2, 10, 11, 14, 6, 17, 12, 16, 0, 8, 1, 5],
        [13, 10, 16, 8, 4, 1, 2, 19, 14, 12, 18, 17, 0, 5, 9, 7, 6, 3, 11, 15],
        [0, 5, 4, 19, 14, 8, 1, 16, 15, 10, 12, 2, 11, 6, 7, 18, 13, 3, 17, 9],
        [11, 16, 17, 10, 15, 12, 0, 5, 4, 8, 3, 7, 13, 1, 18, 9, 19, 6, 14, 2],
        [7, 8, 5, 13, 19, 16, 11, 1, 14, 18, 10, 6, 3, 15, 4, 2, 0, 9, 17, 12],
        [17, 10, 15, 5, 4, 14, 8, 18, 13, 6, 19, 3, 1, 9, 11, 2, 12, 16, 7, 0],
        [14, 3, 16, 0, 10, 18, 4, 1, 5, 19, 12, 9, 11, 15, 13, 7, 17, 8, 6, 2],
        [13, 10, 3, 14, 1, 8, 0, 16, 19, 4, 6, 9, 11, 5, 2, 7, 17, 12, 15, 18],
    ],
    'durations': [
        # Job 0
        [Interval(60, 68), Interval(56, 58), Interval(75, 87), Interval(88, 108), Interval(56, 62),
         Interval(85, 89), Interval(86, 100), Interval(60, 64), Interval(19, 21), Interval(14, 14),
         Interval(85, 85), Interval(45, 45), Interval(43, 51), Interval(8, 10), Interval(91, 97),
         Interval(9, 9), Interval(14, 16), Interval(66, 66), Interval(1, 1), Interval(81, 107)],
        # Job 1
        [Interval(34, 44), Interval(89, 103), Interval(87, 89), Interval(75, 91), Interval(67, 87),
         Interval(54, 62), Interval(74, 92), Interval(3, 3), Interval(74, 82), Interval(64, 72),
         Interval(64, 64), Interval(92, 102), Interval(33, 33), Interval(23, 27), Interval(47, 47),
         Interval(44, 44), Interval(7, 7), Interval(57, 63), Interval(36, 48), Interval(81, 101)],
        # Job 2
        [Interval(85, 107), Interval(59, 73), Interval(88, 88), Interval(53, 67), Interval(21, 23),
         Interval(91, 93), Interval(53, 71), Interval(13, 15), Interval(85, 93), Interval(34, 44),
         Interval(82, 106), Interval(57, 75), Interval(9, 11), Interval(52, 54), Interval(26, 26),
         Interval(15, 15), Interval(56, 74), Interval(74, 90), Interval(10, 10), Interval(26, 28)],
        # Job 3
        [Interval(91, 95), Interval(88, 96), Interval(85, 107), Interval(67, 73), Interval(80, 86),
         Interval(73, 75), Interval(28, 34), Interval(83, 93), Interval(51, 51), Interval(55, 59),
         Interval(78, 78), Interval(8, 8), Interval(7, 7), Interval(90, 92), Interval(69, 89),
         Interval(16, 20), Interval(44, 58), Interval(17, 19), Interval(87, 111), Interval(32, 34)],
        # Job 4
        [Interval(4, 4), Interval(77, 87), Interval(40, 40), Interval(74, 98), Interval(44, 56),
         Interval(54, 54), Interval(21, 21), Interval(6, 6), Interval(48, 60), Interval(59, 77),
         Interval(72, 92), Interval(18, 22), Interval(34, 44), Interval(33, 37), Interval(60, 76),
         Interval(73, 73), Interval(23, 23), Interval(27, 33), Interval(29, 31), Interval(50, 56)],
        # Job 5
        [Interval(94, 94), Interval(50, 66), Interval(87, 99), Interval(30, 34), Interval(90, 92),
         Interval(28, 32), Interval(51, 61), Interval(27, 27), Interval(92, 92), Interval(8, 10),
         Interval(70, 86), Interval(20, 26), Interval(20, 22), Interval(55, 65), Interval(35, 37),
         Interval(28, 30), Interval(92, 98), Interval(92, 106), Interval(77, 81), Interval(75, 77)],
        # Job 6
        [Interval(92, 94), Interval(42, 42), Interval(47, 57), Interval(41, 43), Interval(96, 96),
         Interval(29, 29), Interval(57, 65), Interval(76, 100), Interval(67, 73), Interval(16, 16),
         Interval(28, 34), Interval(60, 70), Interval(73, 93), Interval(72, 84), Interval(23, 29),
         Interval(47, 53), Interval(77, 97), Interval(59, 65), Interval(13, 15), Interval(28, 32)],
        # Job 7
        [Interval(18, 18), Interval(67, 83), Interval(19, 21), Interval(4, 4), Interval(81, 101),
         Interval(59, 77), Interval(19, 19), Interval(52, 56), Interval(76, 94), Interval(64, 82),
         Interval(40, 46), Interval(22, 26), Interval(37, 37), Interval(84, 90), Interval(64, 68),
         Interval(31, 33), Interval(48, 56), Interval(9, 9), Interval(48, 50), Interval(61, 61)],
        # Job 8
        [Interval(31, 39), Interval(87, 111), Interval(59, 65), Interval(6, 6), Interval(62, 62),
         Interval(7, 7), Interval(75, 85), Interval(3, 3), Interval(55, 59), Interval(7, 7),
         Interval(74, 96), Interval(27, 33), Interval(91, 101), Interval(84, 98), Interval(13, 13),
         Interval(75, 99), Interval(77, 87), Interval(72, 94), Interval(71, 85), Interval(52, 60)],
        # Job 9
        [Interval(80, 90), Interval(7, 9), Interval(64, 68), Interval(85, 91), Interval(13, 17),
         Interval(5, 5), Interval(56, 62), Interval(27, 33), Interval(52, 68), Interval(41, 41),
         Interval(17, 17), Interval(61, 71), Interval(84, 94), Interval(75, 81), Interval(86, 90),
         Interval(60, 78), Interval(45, 45), Interval(79, 85), Interval(6, 6), Interval(13, 13)],
        # Job 10
        [Interval(81, 99), Interval(26, 28), Interval(1, 1), Interval(8, 8), Interval(90, 92),
         Interval(70, 90), Interval(79, 99), Interval(49, 49), Interval(31, 33), Interval(25, 31),
         Interval(88, 92), Interval(89, 97), Interval(6, 6), Interval(30, 40), Interval(67, 79),
         Interval(46, 48), Interval(43, 43), Interval(69, 81), Interval(8, 8), Interval(49, 53)],
        # Job 11
        [Interval(3, 3), Interval(79, 89), Interval(33, 35), Interval(26, 30), Interval(56, 64),
         Interval(62, 76), Interval(45, 45), Interval(63, 71), Interval(54, 62), Interval(86, 88),
         Interval(61, 69), Interval(57, 67), Interval(85, 109), Interval(19, 21), Interval(31, 31),
         Interval(30, 36), Interval(32, 34), Interval(70, 84), Interval(45, 55), Interval(75, 85)],
        # Job 12
        [Interval(46, 50), Interval(89, 91), Interval(66, 84), Interval(85, 107), Interval(44, 44),
         Interval(28, 28), Interval(21, 21), Interval(46, 56), Interval(67, 83), Interval(17, 17),
         Interval(76, 102), Interval(52, 66), Interval(49, 63), Interval(55, 71), Interval(18, 18),
         Interval(15, 19), Interval(29, 31), Interval(14, 18), Interval(6, 8), Interval(34, 36)],
        # Job 13
        [Interval(53, 61), Interval(16, 16), Interval(38, 46), Interval(33, 35), Interval(33, 41),
         Interval(26, 26), Interval(65, 71), Interval(72, 74), Interval(5, 5), Interval(8, 8),
         Interval(12, 12), Interval(76, 98), Interval(73, 93), Interval(20, 20), Interval(92, 102),
         Interval(19, 21), Interval(80, 90), Interval(58, 64), Interval(9, 9), Interval(34, 38)],
        # Job 14
        [Interval(61, 65), Interval(11, 11), Interval(44, 46), Interval(9, 11), Interval(33, 33),
         Interval(5, 5), Interval(38, 44), Interval(43, 51), Interval(8, 10), Interval(71, 77),
         Interval(33, 33), Interval(35, 35), Interval(73, 83), Interval(12, 12), Interval(19, 25),
         Interval(43, 45), Interval(7, 9), Interval(90, 104), Interval(9, 11), Interval(79, 93)],
        # Job 15
        [Interval(30, 36), Interval(57, 63), Interval(21, 21), Interval(85, 107), Interval(63, 75),
         Interval(33, 35), Interval(85, 103), Interval(15, 15), Interval(23, 23), Interval(74, 94),
         Interval(15, 17), Interval(53, 57), Interval(50, 50), Interval(5, 5), Interval(57, 61),
         Interval(34, 36), Interval(12, 12), Interval(50, 64), Interval(10, 12), Interval(44, 58)],
        # Job 16
        [Interval(68, 76), Interval(38, 46), Interval(4, 4), Interval(57, 67), Interval(15, 15),
         Interval(24, 30), Interval(16, 16), Interval(31, 37), Interval(7, 9), Interval(44, 56),
         Interval(83, 87), Interval(12, 12), Interval(42, 54), Interval(5, 5), Interval(25, 25),
         Interval(38, 42), Interval(78, 84), Interval(44, 48), Interval(59, 75), Interval(22, 28)],
        # Job 17
        [Interval(76, 90), Interval(83, 101), Interval(22, 28), Interval(35, 45), Interval(20, 22),
         Interval(4, 4), Interval(37, 49), Interval(36, 40), Interval(53, 67), Interval(23, 25),
         Interval(3, 3), Interval(25, 31), Interval(77, 95), Interval(60, 76), Interval(51, 59),
         Interval(89, 93), Interval(94, 100), Interval(19, 19), Interval(66, 80), Interval(18, 22)],
        # Job 18
        [Interval(27, 29), Interval(72, 90), Interval(44, 48), Interval(85, 111), Interval(45, 47),
         Interval(27, 31), Interval(94, 98), Interval(12, 12), Interval(63, 79), Interval(29, 35),
         Interval(63, 65), Interval(36, 42), Interval(16, 16), Interval(91, 103), Interval(91, 107),
         Interval(44, 54), Interval(64, 86), Interval(7, 7), Interval(69, 89), Interval(74, 86)],
        # Job 19
        [Interval(71, 71), Interval(8, 10), Interval(11, 11), Interval(8, 8), Interval(4, 4),
         Interval(42, 52), Interval(80, 106), Interval(76, 88), Interval(6, 6), Interval(48, 50),
         Interval(7, 7), Interval(23, 25), Interval(92, 92), Interval(12, 14), Interval(86, 86),
         Interval(72, 88), Interval(32, 36), Interval(72, 78), Interval(32, 38), Interval(28, 30)],
    ],
    'name': 'INT__TAI20_20_01.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai20_20_01_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI20_20_01.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI20_20_01.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI20_20_01_F_15_01_INTERVAL_DATA
