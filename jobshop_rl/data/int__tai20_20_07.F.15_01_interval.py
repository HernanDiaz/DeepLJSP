"""
Problema INT__TAI20_20_07.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI20_20_07_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 20,
    'problem_id': 'int__tai20_20_07.F.15_01_interval',
    'sequences': [
        [7, 13, 17, 6, 8, 11, 4, 3, 12, 18, 9, 2, 0, 1, 10, 16, 15, 14, 5, 19],
        [7, 17, 16, 10, 0, 15, 12, 1, 2, 9, 18, 5, 3, 6, 19, 14, 4, 11, 8, 13],
        [11, 17, 19, 0, 2, 4, 8, 14, 10, 3, 5, 12, 18, 15, 1, 16, 6, 7, 9, 13],
        [2, 7, 17, 12, 1, 16, 13, 6, 19, 3, 18, 11, 5, 0, 4, 14, 8, 10, 15, 9],
        [3, 5, 12, 0, 10, 17, 16, 2, 7, 8, 9, 18, 19, 4, 13, 11, 1, 6, 15, 14],
        [9, 13, 6, 0, 7, 18, 12, 17, 19, 10, 3, 4, 16, 1, 15, 8, 2, 11, 14, 5],
        [7, 3, 5, 17, 14, 19, 8, 9, 13, 11, 1, 12, 16, 0, 2, 18, 15, 4, 10, 6],
        [15, 16, 12, 5, 4, 9, 18, 3, 8, 19, 17, 6, 13, 11, 0, 7, 14, 10, 1, 2],
        [2, 5, 6, 19, 4, 18, 1, 0, 8, 9, 7, 12, 13, 14, 17, 15, 16, 3, 10, 11],
        [19, 0, 17, 14, 7, 11, 8, 6, 12, 4, 10, 2, 16, 13, 3, 9, 1, 15, 18, 5],
        [10, 4, 14, 9, 19, 6, 18, 0, 13, 12, 16, 5, 7, 8, 17, 3, 1, 2, 15, 11],
        [4, 18, 12, 15, 3, 8, 19, 9, 5, 6, 16, 14, 10, 0, 2, 1, 17, 13, 11, 7],
        [4, 5, 6, 7, 11, 10, 0, 17, 2, 9, 14, 13, 1, 16, 8, 19, 15, 12, 3, 18],
        [5, 0, 17, 14, 8, 12, 2, 9, 18, 6, 19, 3, 13, 7, 4, 15, 11, 1, 10, 16],
        [10, 1, 15, 5, 8, 4, 9, 13, 14, 2, 17, 6, 3, 16, 19, 11, 7, 18, 0, 12],
        [1, 5, 2, 16, 11, 17, 14, 8, 9, 18, 4, 12, 15, 19, 7, 0, 13, 6, 10, 3],
        [1, 18, 2, 14, 5, 8, 10, 6, 19, 4, 13, 9, 16, 7, 11, 12, 15, 0, 3, 17],
        [11, 3, 14, 7, 1, 13, 18, 9, 19, 12, 8, 15, 4, 6, 16, 17, 2, 10, 0, 5],
        [10, 2, 17, 7, 8, 18, 13, 6, 5, 16, 0, 15, 1, 3, 12, 11, 9, 14, 19, 4],
        [8, 16, 0, 2, 11, 10, 19, 17, 7, 14, 3, 4, 13, 15, 6, 5, 1, 9, 12, 18],
    ],
    'durations': [
        # Job 0
        [Interval(78, 94), Interval(41, 45), Interval(61, 61), Interval(86, 112), Interval(7, 7),
         Interval(63, 77), Interval(20, 22), Interval(2, 2), Interval(84, 92), Interval(33, 43),
         Interval(59, 71), Interval(70, 92), Interval(35, 41), Interval(49, 53), Interval(74, 88),
         Interval(35, 39), Interval(68, 76), Interval(86, 102), Interval(42, 46), Interval(92, 106)],
        # Job 1
        [Interval(79, 81), Interval(58, 74), Interval(80, 100), Interval(80, 86), Interval(82, 96),
         Interval(7, 7), Interval(54, 56), Interval(16, 18), Interval(13, 13), Interval(41, 49),
         Interval(25, 31), Interval(69, 77), Interval(40, 48), Interval(64, 66), Interval(48, 52),
         Interval(83, 85), Interval(63, 77), Interval(69, 73), Interval(28, 36), Interval(82, 100)],
        # Job 2
        [Interval(88, 92), Interval(39, 47), Interval(35, 39), Interval(69, 73), Interval(56, 72),
         Interval(88, 88), Interval(24, 30), Interval(26, 34), Interval(32, 36), Interval(96, 102),
         Interval(9, 11), Interval(39, 49), Interval(85, 113), Interval(82, 106), Interval(93, 99),
         Interval(88, 108), Interval(38, 50), Interval(7, 7), Interval(33, 33), Interval(59, 59)],
        # Job 3
        [Interval(33, 35), Interval(47, 57), Interval(5, 5), Interval(4, 4), Interval(72, 96),
         Interval(51, 57), Interval(3, 3), Interval(92, 102), Interval(36, 42), Interval(9, 9),
         Interval(9, 9), Interval(91, 91), Interval(59, 61), Interval(4, 4), Interval(61, 65),
         Interval(3, 3), Interval(30, 40), Interval(77, 81), Interval(63, 69), Interval(95, 99)],
        # Job 4
        [Interval(51, 53), Interval(45, 57), Interval(68, 76), Interval(22, 26), Interval(90, 102),
         Interval(49, 59), Interval(51, 51), Interval(58, 64), Interval(88, 96), Interval(73, 89),
         Interval(72, 76), Interval(43, 55), Interval(24, 24), Interval(58, 60), Interval(4, 4),
         Interval(19, 23), Interval(74, 82), Interval(2, 2), Interval(3, 3), Interval(49, 49)],
        # Job 5
        [Interval(37, 47), Interval(42, 52), Interval(10, 10), Interval(27, 27), Interval(34, 42),
         Interval(80, 104), Interval(81, 95), Interval(16, 16), Interval(3, 3), Interval(51, 61),
         Interval(73, 87), Interval(10, 10), Interval(25, 27), Interval(70, 86), Interval(65, 73),
         Interval(85, 97), Interval(77, 87), Interval(77, 77), Interval(70, 76), Interval(95, 97)],
        # Job 6
        [Interval(18, 20), Interval(34, 42), Interval(77, 89), Interval(46, 54), Interval(28, 34),
         Interval(76, 98), Interval(66, 68), Interval(89, 109), Interval(66, 72), Interval(73, 81),
         Interval(4, 4), Interval(31, 31), Interval(85, 107), Interval(72, 82), Interval(73, 87),
         Interval(63, 73), Interval(74, 74), Interval(75, 97), Interval(30, 30), Interval(52, 56)],
        # Job 7
        [Interval(23, 27), Interval(45, 49), Interval(9, 11), Interval(15, 17), Interval(76, 90),
         Interval(61, 63), Interval(3, 3), Interval(35, 41), Interval(87, 87), Interval(17, 21),
         Interval(95, 101), Interval(2, 2), Interval(56, 60), Interval(27, 33), Interval(22, 22),
         Interval(51, 59), Interval(75, 85), Interval(64, 74), Interval(75, 79), Interval(38, 42)],
        # Job 8
        [Interval(16, 18), Interval(94, 102), Interval(24, 26), Interval(41, 41), Interval(60, 64),
         Interval(27, 29), Interval(47, 57), Interval(5, 5), Interval(25, 25), Interval(34, 40),
         Interval(82, 104), Interval(63, 63), Interval(22, 24), Interval(51, 65), Interval(84, 100),
         Interval(65, 75), Interval(80, 100), Interval(28, 30), Interval(26, 26), Interval(65, 73)],
        # Job 9
        [Interval(38, 44), Interval(61, 69), Interval(30, 38), Interval(4, 4), Interval(68, 78),
         Interval(78, 80), Interval(54, 62), Interval(14, 14), Interval(92, 102), Interval(70, 72),
         Interval(91, 103), Interval(85, 105), Interval(51, 65), Interval(12, 12), Interval(15, 19),
         Interval(63, 69), Interval(73, 83), Interval(61, 75), Interval(59, 79), Interval(48, 58)],
        # Job 10
        [Interval(24, 30), Interval(81, 85), Interval(18, 22), Interval(12, 12), Interval(79, 93),
         Interval(31, 37), Interval(35, 37), Interval(25, 31), Interval(57, 69), Interval(35, 39),
         Interval(20, 26), Interval(50, 50), Interval(79, 101), Interval(5, 5), Interval(17, 17),
         Interval(74, 86), Interval(32, 38), Interval(4, 4), Interval(36, 46), Interval(71, 91)],
        # Job 11
        [Interval(74, 96), Interval(90, 94), Interval(82, 98), Interval(85, 105), Interval(18, 20),
         Interval(58, 60), Interval(93, 95), Interval(73, 77), Interval(75, 75), Interval(47, 47),
         Interval(8, 10), Interval(6, 6), Interval(39, 47), Interval(28, 32), Interval(82, 94),
         Interval(18, 20), Interval(9, 11), Interval(68, 84), Interval(50, 66), Interval(29, 29)],
        # Job 12
        [Interval(21, 25), Interval(86, 88), Interval(47, 53), Interval(73, 79), Interval(24, 28),
         Interval(26, 30), Interval(35, 37), Interval(31, 39), Interval(4, 4), Interval(32, 32),
         Interval(21, 23), Interval(69, 79), Interval(45, 59), Interval(13, 13), Interval(14, 14),
         Interval(57, 65), Interval(46, 48), Interval(76, 98), Interval(73, 73), Interval(55, 73)],
        # Job 13
        [Interval(73, 87), Interval(43, 43), Interval(40, 50), Interval(86, 98), Interval(67, 69),
         Interval(57, 75), Interval(57, 63), Interval(32, 42), Interval(56, 64), Interval(44, 58),
         Interval(36, 46), Interval(61, 61), Interval(88, 108), Interval(56, 62), Interval(90, 100),
         Interval(37, 39), Interval(66, 68), Interval(11, 13), Interval(95, 95), Interval(19, 25)],
        # Job 14
        [Interval(56, 58), Interval(94, 98), Interval(11, 11), Interval(24, 26), Interval(62, 76),
         Interval(51, 67), Interval(44, 46), Interval(50, 54), Interval(78, 92), Interval(26, 26),
         Interval(81, 101), Interval(55, 59), Interval(26, 34), Interval(28, 36), Interval(52, 64),
         Interval(40, 40), Interval(10, 12), Interval(17, 21), Interval(19, 19), Interval(78, 86)],
        # Job 15
        [Interval(80, 82), Interval(82, 84), Interval(75, 79), Interval(44, 46), Interval(62, 64),
         Interval(91, 99), Interval(22, 28), Interval(48, 48), Interval(26, 28), Interval(51, 61),
         Interval(54, 54), Interval(76, 88), Interval(30, 34), Interval(88, 110), Interval(36, 46),
         Interval(1, 1), Interval(2, 2), Interval(57, 65), Interval(22, 24), Interval(23, 29)],
        # Job 16
        [Interval(43, 51), Interval(9, 9), Interval(86, 94), Interval(26, 30), Interval(60, 76),
         Interval(20, 26), Interval(62, 70), Interval(45, 47), Interval(75, 75), Interval(93, 99),
         Interval(68, 68), Interval(57, 63), Interval(44, 48), Interval(31, 39), Interval(9, 9),
         Interval(80, 98), Interval(93, 99), Interval(39, 45), Interval(2, 2), Interval(86, 86)],
        # Job 17
        [Interval(81, 99), Interval(45, 59), Interval(9, 11), Interval(24, 26), Interval(53, 65),
         Interval(48, 62), Interval(29, 31), Interval(29, 37), Interval(16, 20), Interval(78, 82),
         Interval(70, 76), Interval(38, 44), Interval(9, 9), Interval(64, 64), Interval(79, 79),
         Interval(28, 34), Interval(71, 87), Interval(42, 46), Interval(13, 15), Interval(66, 80)],
        # Job 18
        [Interval(54, 64), Interval(54, 60), Interval(63, 71), Interval(44, 50), Interval(13, 13),
         Interval(32, 38), Interval(64, 80), Interval(72, 76), Interval(55, 57), Interval(85, 85),
         Interval(48, 56), Interval(23, 27), Interval(86, 98), Interval(83, 101), Interval(77, 85),
         Interval(72, 80), Interval(89, 93), Interval(86, 100), Interval(36, 36), Interval(87, 89)],
        # Job 19
        [Interval(28, 28), Interval(79, 99), Interval(3, 3), Interval(69, 81), Interval(29, 33),
         Interval(76, 98), Interval(58, 74), Interval(62, 72), Interval(34, 34), Interval(17, 21),
         Interval(30, 30), Interval(86, 96), Interval(47, 59), Interval(75, 87), Interval(13, 13),
         Interval(14, 16), Interval(59, 59), Interval(17, 17), Interval(82, 88), Interval(10, 12)],
    ],
    'name': 'INT__TAI20_20_07.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai20_20_07_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI20_20_07.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI20_20_07.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI20_20_07_F_15_01_INTERVAL_DATA
