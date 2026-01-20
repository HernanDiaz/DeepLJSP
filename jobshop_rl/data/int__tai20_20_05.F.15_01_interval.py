"""
Problema INT__TAI20_20_05.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI20_20_05_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 20,
    'problem_id': 'int__tai20_20_05.F.15_01_interval',
    'sequences': [
        [9, 6, 2, 14, 18, 13, 0, 1, 10, 19, 17, 16, 11, 15, 7, 8, 12, 4, 5, 3],
        [10, 5, 17, 19, 4, 11, 9, 12, 0, 7, 8, 15, 1, 6, 13, 14, 2, 3, 16, 18],
        [6, 8, 19, 10, 14, 5, 4, 17, 2, 11, 15, 0, 7, 3, 1, 13, 9, 12, 16, 18],
        [11, 4, 17, 15, 8, 13, 9, 6, 16, 19, 0, 7, 1, 10, 18, 3, 2, 5, 12, 14],
        [11, 19, 16, 0, 8, 5, 2, 10, 18, 13, 9, 3, 12, 15, 7, 4, 1, 17, 6, 14],
        [11, 9, 16, 7, 6, 15, 1, 19, 10, 18, 8, 17, 2, 14, 4, 12, 13, 3, 0, 5],
        [3, 12, 2, 7, 16, 14, 15, 9, 19, 18, 1, 5, 0, 10, 11, 8, 13, 6, 17, 4],
        [18, 12, 0, 9, 3, 7, 16, 8, 4, 17, 11, 10, 5, 2, 14, 15, 6, 19, 1, 13],
        [0, 17, 8, 12, 6, 15, 13, 1, 9, 5, 11, 2, 18, 3, 7, 4, 16, 10, 19, 14],
        [11, 18, 5, 6, 0, 10, 2, 1, 15, 14, 3, 12, 4, 19, 16, 8, 13, 7, 17, 9],
        [13, 7, 6, 17, 15, 10, 2, 19, 12, 11, 1, 16, 8, 14, 3, 0, 5, 4, 9, 18],
        [6, 19, 12, 13, 5, 10, 9, 18, 14, 16, 7, 11, 0, 2, 3, 15, 4, 17, 1, 8],
        [6, 9, 10, 14, 12, 5, 11, 7, 2, 17, 19, 4, 15, 0, 1, 13, 16, 3, 18, 8],
        [11, 19, 5, 7, 10, 9, 15, 4, 2, 14, 6, 12, 0, 13, 16, 17, 1, 18, 3, 8],
        [9, 19, 5, 10, 4, 11, 0, 6, 2, 3, 7, 13, 1, 18, 8, 15, 16, 14, 17, 12],
        [7, 4, 6, 2, 3, 18, 0, 5, 1, 8, 13, 17, 11, 14, 19, 16, 12, 15, 10, 9],
        [15, 12, 5, 2, 8, 7, 14, 9, 4, 3, 13, 6, 16, 17, 19, 1, 11, 10, 18, 0],
        [19, 13, 9, 5, 6, 4, 8, 3, 15, 10, 2, 12, 0, 1, 18, 16, 14, 11, 7, 17],
        [7, 17, 5, 12, 4, 14, 13, 2, 18, 9, 1, 11, 0, 6, 16, 10, 15, 8, 19, 3],
        [8, 14, 11, 18, 15, 16, 19, 13, 17, 1, 9, 5, 6, 0, 3, 4, 10, 2, 7, 12],
    ],
    'durations': [
        # Job 0
        [Interval(14, 14), Interval(54, 70), Interval(28, 36), Interval(78, 84), Interval(64, 66),
         Interval(51, 55), Interval(29, 33), Interval(85, 111), Interval(34, 34), Interval(25, 29),
         Interval(60, 60), Interval(38, 48), Interval(28, 32), Interval(22, 26), Interval(61, 61),
         Interval(38, 42), Interval(7, 7), Interval(14, 16), Interval(49, 51), Interval(10, 10)],
        # Job 1
        [Interval(12, 12), Interval(38, 46), Interval(67, 71), Interval(12, 12), Interval(74, 94),
         Interval(22, 26), Interval(76, 98), Interval(60, 78), Interval(45, 45), Interval(35, 39),
         Interval(38, 38), Interval(68, 76), Interval(53, 55), Interval(62, 70), Interval(41, 49),
         Interval(4, 4), Interval(56, 66), Interval(18, 22), Interval(48, 50), Interval(17, 17)],
        # Job 2
        [Interval(55, 65), Interval(43, 47), Interval(33, 35), Interval(73, 75), Interval(64, 66),
         Interval(64, 86), Interval(85, 99), Interval(63, 75), Interval(35, 45), Interval(23, 29),
         Interval(64, 74), Interval(30, 30), Interval(18, 18), Interval(77, 99), Interval(44, 54),
         Interval(61, 75), Interval(24, 26), Interval(1, 1), Interval(88, 102), Interval(23, 27)],
        # Job 3
        [Interval(72, 82), Interval(56, 66), Interval(42, 42), Interval(57, 73), Interval(89, 109),
         Interval(75, 87), Interval(78, 90), Interval(31, 35), Interval(8, 8), Interval(19, 23),
         Interval(26, 26), Interval(52, 64), Interval(85, 97), Interval(7, 7), Interval(94, 96),
         Interval(85, 97), Interval(87, 95), Interval(14, 14), Interval(46, 46), Interval(43, 55)],
        # Job 4
        [Interval(59, 65), Interval(86, 90), Interval(2, 2), Interval(11, 13), Interval(63, 73),
         Interval(88, 110), Interval(45, 47), Interval(33, 37), Interval(76, 98), Interval(53, 53),
         Interval(60, 60), Interval(50, 58), Interval(96, 102), Interval(57, 61), Interval(10, 10),
         Interval(31, 37), Interval(60, 74), Interval(29, 33), Interval(52, 52), Interval(49, 57)],
        # Job 5
        [Interval(21, 21), Interval(89, 95), Interval(29, 37), Interval(7, 9), Interval(9, 9),
         Interval(44, 58), Interval(40, 48), Interval(1, 1), Interval(69, 69), Interval(77, 89),
         Interval(15, 19), Interval(76, 96), Interval(48, 54), Interval(87, 103), Interval(35, 45),
         Interval(30, 34), Interval(75, 93), Interval(52, 56), Interval(3, 3), Interval(28, 34)],
        # Job 6
        [Interval(40, 52), Interval(82, 92), Interval(42, 48), Interval(57, 67), Interval(9, 11),
         Interval(17, 21), Interval(3, 3), Interval(66, 72), Interval(50, 52), Interval(50, 62),
         Interval(20, 20), Interval(49, 53), Interval(35, 47), Interval(12, 12), Interval(6, 6),
         Interval(43, 47), Interval(17, 17), Interval(2, 2), Interval(84, 102), Interval(38, 40)],
        # Job 7
        [Interval(10, 10), Interval(81, 83), Interval(39, 49), Interval(22, 22), Interval(9, 9),
         Interval(54, 56), Interval(27, 31), Interval(3, 3), Interval(3, 3), Interval(70, 84),
         Interval(77, 79), Interval(42, 44), Interval(8, 10), Interval(75, 93), Interval(1, 1),
         Interval(10, 12), Interval(52, 66), Interval(90, 104), Interval(21, 25), Interval(77, 89)],
        # Job 8
        [Interval(3, 3), Interval(77, 101), Interval(31, 37), Interval(4, 4), Interval(84, 104),
         Interval(10, 10), Interval(88, 92), Interval(15, 17), Interval(16, 20), Interval(49, 61),
         Interval(59, 79), Interval(36, 42), Interval(93, 105), Interval(69, 85), Interval(59, 71),
         Interval(51, 59), Interval(24, 30), Interval(78, 90), Interval(84, 104), Interval(2, 2)],
        # Job 9
        [Interval(84, 86), Interval(88, 108), Interval(6, 6), Interval(71, 77), Interval(24, 24),
         Interval(53, 55), Interval(82, 88), Interval(7, 7), Interval(54, 66), Interval(47, 51),
         Interval(79, 105), Interval(53, 65), Interval(23, 29), Interval(90, 104), Interval(81, 93),
         Interval(26, 30), Interval(78, 84), Interval(43, 49), Interval(4, 4), Interval(75, 89)],
        # Job 10
        [Interval(43, 55), Interval(96, 102), Interval(92, 92), Interval(51, 59), Interval(38, 38),
         Interval(22, 24), Interval(94, 100), Interval(40, 44), Interval(82, 106), Interval(85, 105),
         Interval(85, 101), Interval(31, 31), Interval(78, 104), Interval(3, 3), Interval(28, 32),
         Interval(28, 28), Interval(55, 57), Interval(20, 22), Interval(50, 52), Interval(20, 24)],
        # Job 11
        [Interval(46, 56), Interval(57, 73), Interval(69, 73), Interval(71, 91), Interval(50, 62),
         Interval(42, 48), Interval(36, 46), Interval(24, 28), Interval(52, 52), Interval(84, 92),
         Interval(92, 102), Interval(3, 3), Interval(32, 32), Interval(15, 17), Interval(1, 1),
         Interval(12, 14), Interval(8, 8), Interval(44, 56), Interval(57, 75), Interval(5, 5)],
        # Job 12
        [Interval(93, 93), Interval(68, 88), Interval(83, 97), Interval(23, 27), Interval(80, 86),
         Interval(35, 45), Interval(75, 91), Interval(61, 73), Interval(53, 65), Interval(88, 92),
         Interval(86, 96), Interval(44, 56), Interval(21, 23), Interval(9, 9), Interval(12, 12),
         Interval(26, 30), Interval(28, 28), Interval(35, 45), Interval(43, 43), Interval(26, 32)],
        # Job 13
        [Interval(58, 72), Interval(28, 32), Interval(13, 15), Interval(31, 35), Interval(46, 54),
         Interval(89, 93), Interval(18, 20), Interval(47, 53), Interval(83, 89), Interval(79, 87),
         Interval(12, 14), Interval(44, 54), Interval(26, 34), Interval(42, 44), Interval(41, 51),
         Interval(63, 71), Interval(6, 6), Interval(73, 81), Interval(85, 89), Interval(60, 68)],
        # Job 14
        [Interval(79, 105), Interval(88, 104), Interval(73, 79), Interval(39, 45), Interval(35, 43),
         Interval(16, 18), Interval(44, 48), Interval(52, 70), Interval(15, 19), Interval(28, 30),
         Interval(59, 79), Interval(54, 62), Interval(64, 74), Interval(97, 99), Interval(56, 64),
         Interval(96, 98), Interval(70, 82), Interval(39, 43), Interval(52, 58), Interval(31, 33)],
        # Job 15
        [Interval(34, 40), Interval(37, 39), Interval(71, 83), Interval(4, 4), Interval(68, 76),
         Interval(30, 32), Interval(32, 32), Interval(88, 108), Interval(40, 48), Interval(57, 73),
         Interval(15, 17), Interval(72, 96), Interval(58, 62), Interval(82, 94), Interval(18, 22),
         Interval(60, 60), Interval(88, 96), Interval(84, 98), Interval(72, 72), Interval(58, 58)],
        # Job 16
        [Interval(14, 16), Interval(37, 37), Interval(46, 56), Interval(9, 9), Interval(15, 15),
         Interval(14, 14), Interval(71, 75), Interval(82, 104), Interval(72, 86), Interval(61, 65),
         Interval(21, 21), Interval(61, 75), Interval(9, 9), Interval(46, 56), Interval(22, 28),
         Interval(54, 60), Interval(37, 45), Interval(46, 56), Interval(72, 88), Interval(19, 21)],
        # Job 17
        [Interval(44, 56), Interval(44, 56), Interval(17, 21), Interval(75, 87), Interval(1, 1),
         Interval(6, 6), Interval(14, 16), Interval(30, 30), Interval(19, 19), Interval(31, 41),
         Interval(62, 66), Interval(70, 82), Interval(35, 45), Interval(32, 32), Interval(72, 82),
         Interval(57, 67), Interval(50, 54), Interval(7, 7), Interval(90, 104), Interval(35, 45)],
        # Job 18
        [Interval(28, 30), Interval(30, 40), Interval(6, 8), Interval(55, 63), Interval(1, 1),
         Interval(65, 65), Interval(85, 99), Interval(34, 44), Interval(50, 62), Interval(90, 96),
         Interval(26, 32), Interval(51, 57), Interval(36, 46), Interval(53, 55), Interval(7, 7),
         Interval(79, 91), Interval(64, 84), Interval(68, 90), Interval(64, 80), Interval(69, 89)],
        # Job 19
        [Interval(30, 32), Interval(9, 9), Interval(68, 84), Interval(47, 61), Interval(43, 45),
         Interval(35, 43), Interval(43, 53), Interval(17, 17), Interval(4, 4), Interval(12, 14),
         Interval(76, 98), Interval(21, 27), Interval(63, 73), Interval(78, 90), Interval(78, 86),
         Interval(1, 1), Interval(4, 4), Interval(52, 68), Interval(52, 60), Interval(51, 65)],
    ],
    'name': 'INT__TAI20_20_05.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai20_20_05_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI20_20_05.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI20_20_05.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI20_20_05_F_15_01_INTERVAL_DATA
