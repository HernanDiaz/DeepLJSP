"""
Problema INT__TAI20_20_08.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI20_20_08_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 20,
    'problem_id': 'int__tai20_20_08.F.15_01_interval',
    'sequences': [
        [17, 7, 9, 12, 4, 5, 14, 8, 0, 2, 18, 3, 10, 11, 16, 13, 19, 15, 1, 6],
        [18, 10, 6, 3, 4, 16, 1, 14, 15, 13, 11, 19, 17, 8, 0, 9, 2, 5, 12, 7],
        [13, 16, 8, 7, 4, 3, 15, 19, 18, 17, 5, 1, 10, 14, 12, 11, 6, 9, 2, 0],
        [13, 18, 4, 6, 5, 14, 9, 19, 1, 3, 10, 7, 12, 2, 15, 11, 8, 17, 16, 0],
        [17, 10, 8, 12, 3, 14, 16, 15, 2, 0, 7, 5, 13, 19, 11, 18, 6, 4, 9, 1],
        [5, 0, 19, 17, 8, 7, 12, 6, 1, 3, 13, 16, 15, 2, 14, 10, 9, 11, 18, 4],
        [17, 14, 6, 8, 18, 2, 16, 12, 5, 0, 4, 15, 7, 10, 3, 19, 1, 11, 9, 13],
        [11, 1, 15, 16, 2, 13, 9, 14, 0, 6, 18, 10, 7, 5, 4, 17, 3, 19, 12, 8],
        [17, 10, 7, 2, 16, 13, 11, 0, 8, 4, 19, 3, 1, 12, 5, 18, 9, 14, 6, 15],
        [18, 15, 14, 12, 9, 19, 10, 16, 7, 17, 6, 11, 0, 2, 4, 8, 13, 5, 3, 1],
        [1, 0, 9, 6, 19, 17, 11, 18, 15, 16, 14, 8, 7, 13, 3, 10, 12, 4, 5, 2],
        [15, 2, 10, 19, 9, 3, 17, 16, 13, 11, 4, 6, 1, 7, 14, 12, 5, 18, 0, 8],
        [6, 1, 19, 14, 17, 11, 10, 3, 13, 2, 12, 15, 4, 16, 8, 18, 5, 0, 9, 7],
        [2, 10, 1, 19, 5, 12, 8, 14, 17, 13, 11, 4, 16, 18, 15, 0, 6, 7, 9, 3],
        [14, 0, 8, 3, 9, 10, 2, 17, 4, 6, 19, 1, 16, 5, 12, 13, 15, 7, 18, 11],
        [8, 12, 13, 10, 7, 0, 4, 16, 5, 15, 18, 3, 9, 2, 11, 19, 14, 6, 1, 17],
        [8, 12, 19, 11, 10, 4, 2, 7, 9, 6, 0, 15, 13, 1, 16, 14, 5, 3, 17, 18],
        [9, 6, 16, 4, 3, 2, 14, 8, 12, 7, 17, 15, 19, 18, 1, 0, 5, 10, 13, 11],
        [9, 18, 12, 10, 14, 16, 1, 17, 4, 7, 0, 8, 2, 15, 19, 6, 5, 3, 11, 13],
        [6, 2, 17, 9, 19, 11, 14, 7, 4, 3, 8, 12, 18, 15, 16, 0, 5, 1, 10, 13],
    ],
    'durations': [
        # Job 0
        [Interval(24, 24), Interval(8, 8), Interval(37, 47), Interval(77, 97), Interval(84, 106),
         Interval(14, 14), Interval(30, 30), Interval(88, 90), Interval(61, 77), Interval(32, 32),
         Interval(56, 62), Interval(19, 21), Interval(24, 28), Interval(34, 36), Interval(72, 94),
         Interval(23, 27), Interval(46, 50), Interval(46, 56), Interval(54, 62), Interval(87, 111)],
        # Job 1
        [Interval(5, 5), Interval(31, 37), Interval(30, 34), Interval(29, 29), Interval(43, 45),
         Interval(69, 89), Interval(72, 74), Interval(12, 14), Interval(23, 27), Interval(8, 8),
         Interval(37, 37), Interval(6, 6), Interval(1, 1), Interval(31, 31), Interval(86, 108),
         Interval(7, 7), Interval(45, 49), Interval(85, 97), Interval(64, 84), Interval(38, 38)],
        # Job 2
        [Interval(63, 71), Interval(62, 74), Interval(41, 47), Interval(30, 32), Interval(84, 96),
         Interval(27, 31), Interval(19, 23), Interval(34, 40), Interval(74, 90), Interval(27, 27),
         Interval(31, 35), Interval(1, 1), Interval(72, 74), Interval(33, 37), Interval(73, 93),
         Interval(69, 89), Interval(70, 88), Interval(79, 105), Interval(42, 46), Interval(78, 78)],
        # Job 3
        [Interval(12, 14), Interval(84, 86), Interval(68, 84), Interval(77, 91), Interval(68, 86),
         Interval(18, 22), Interval(60, 66), Interval(1, 1), Interval(5, 5), Interval(5, 5),
         Interval(45, 55), Interval(11, 11), Interval(8, 8), Interval(14, 14), Interval(34, 34),
         Interval(19, 21), Interval(58, 58), Interval(32, 32), Interval(53, 59), Interval(74, 74)],
        # Job 4
        [Interval(67, 75), Interval(11, 13), Interval(77, 81), Interval(72, 84), Interval(25, 27),
         Interval(37, 39), Interval(65, 79), Interval(78, 88), Interval(51, 51), Interval(9, 9),
         Interval(39, 51), Interval(12, 14), Interval(28, 34), Interval(90, 92), Interval(37, 43),
         Interval(5, 5), Interval(88, 94), Interval(24, 24), Interval(89, 103), Interval(71, 73)],
        # Job 5
        [Interval(75, 91), Interval(91, 105), Interval(80, 86), Interval(22, 22), Interval(8, 8),
         Interval(25, 31), Interval(81, 105), Interval(5, 5), Interval(76, 88), Interval(63, 67),
         Interval(74, 80), Interval(48, 64), Interval(66, 66), Interval(61, 61), Interval(71, 93),
         Interval(9, 9), Interval(75, 89), Interval(30, 40), Interval(80, 86), Interval(46, 56)],
        # Job 6
        [Interval(37, 39), Interval(76, 80), Interval(90, 92), Interval(20, 22), Interval(85, 91),
         Interval(83, 103), Interval(15, 15), Interval(10, 10), Interval(66, 70), Interval(69, 81),
         Interval(52, 54), Interval(35, 35), Interval(10, 12), Interval(60, 76), Interval(97, 99),
         Interval(50, 62), Interval(36, 38), Interval(53, 61), Interval(15, 15), Interval(73, 93)],
        # Job 7
        [Interval(3, 3), Interval(91, 105), Interval(17, 21), Interval(60, 74), Interval(30, 36),
         Interval(72, 84), Interval(54, 64), Interval(2, 2), Interval(31, 33), Interval(70, 86),
         Interval(96, 98), Interval(67, 87), Interval(70, 74), Interval(32, 36), Interval(43, 47),
         Interval(25, 27), Interval(74, 84), Interval(27, 29), Interval(88, 88), Interval(17, 21)],
        # Job 8
        [Interval(42, 50), Interval(27, 29), Interval(89, 109), Interval(93, 97), Interval(15, 19),
         Interval(82, 86), Interval(66, 70), Interval(25, 27), Interval(30, 34), Interval(74, 96),
         Interval(86, 110), Interval(54, 64), Interval(62, 72), Interval(41, 47), Interval(76, 84),
         Interval(70, 70), Interval(88, 102), Interval(61, 79), Interval(8, 10), Interval(47, 51)],
        # Job 9
        [Interval(24, 30), Interval(17, 17), Interval(6, 6), Interval(54, 70), Interval(79, 101),
         Interval(15, 19), Interval(58, 58), Interval(85, 103), Interval(11, 11), Interval(60, 70),
         Interval(82, 110), Interval(75, 77), Interval(50, 66), Interval(52, 68), Interval(50, 52),
         Interval(45, 57), Interval(95, 101), Interval(26, 26), Interval(88, 96), Interval(62, 70)],
        # Job 10
        [Interval(92, 92), Interval(8, 10), Interval(66, 76), Interval(62, 70), Interval(55, 59),
         Interval(50, 62), Interval(8, 8), Interval(72, 88), Interval(11, 11), Interval(73, 83),
         Interval(48, 52), Interval(34, 40), Interval(82, 102), Interval(5, 5), Interval(12, 14),
         Interval(62, 64), Interval(19, 23), Interval(6, 6), Interval(2, 2), Interval(24, 30)],
        # Job 11
        [Interval(70, 70), Interval(55, 55), Interval(12, 14), Interval(44, 56), Interval(23, 23),
         Interval(75, 75), Interval(24, 24), Interval(66, 72), Interval(67, 77), Interval(52, 54),
         Interval(82, 106), Interval(24, 26), Interval(20, 22), Interval(50, 64), Interval(16, 16),
         Interval(17, 17), Interval(70, 70), Interval(34, 34), Interval(38, 46), Interval(6, 6)],
        # Job 12
        [Interval(90, 98), Interval(72, 88), Interval(71, 77), Interval(65, 77), Interval(7, 9),
         Interval(51, 51), Interval(87, 87), Interval(85, 87), Interval(36, 38), Interval(82, 104),
         Interval(80, 84), Interval(1, 1), Interval(67, 85), Interval(47, 51), Interval(35, 35),
         Interval(41, 47), Interval(49, 51), Interval(69, 81), Interval(63, 63), Interval(4, 4)],
        # Job 13
        [Interval(17, 21), Interval(37, 43), Interval(27, 33), Interval(85, 99), Interval(10, 10),
         Interval(52, 68), Interval(30, 34), Interval(64, 78), Interval(65, 81), Interval(61, 61),
         Interval(28, 34), Interval(85, 103), Interval(61, 61), Interval(76, 94), Interval(89, 93),
         Interval(96, 100), Interval(32, 38), Interval(50, 60), Interval(78, 90), Interval(81, 105)],
        # Job 14
        [Interval(64, 72), Interval(13, 13), Interval(30, 30), Interval(78, 88), Interval(44, 48),
         Interval(8, 8), Interval(36, 46), Interval(74, 92), Interval(32, 34), Interval(17, 21),
         Interval(71, 79), Interval(35, 39), Interval(16, 18), Interval(26, 32), Interval(5, 5),
         Interval(62, 62), Interval(93, 99), Interval(7, 7), Interval(65, 81), Interval(34, 44)],
        # Job 15
        [Interval(46, 52), Interval(18, 20), Interval(9, 11), Interval(58, 76), Interval(6, 6),
         Interval(38, 46), Interval(77, 97), Interval(73, 93), Interval(7, 7), Interval(44, 58),
         Interval(53, 57), Interval(70, 88), Interval(21, 27), Interval(2, 2), Interval(83, 93),
         Interval(79, 81), Interval(36, 38), Interval(52, 64), Interval(19, 21), Interval(39, 51)],
        # Job 16
        [Interval(87, 91), Interval(29, 37), Interval(27, 27), Interval(20, 20), Interval(2, 2),
         Interval(26, 26), Interval(87, 89), Interval(24, 24), Interval(57, 67), Interval(64, 72),
         Interval(53, 65), Interval(47, 59), Interval(7, 7), Interval(78, 92), Interval(60, 72),
         Interval(14, 14), Interval(21, 23), Interval(15, 15), Interval(8, 8), Interval(56, 60)],
        # Job 17
        [Interval(87, 89), Interval(84, 92), Interval(87, 95), Interval(64, 80), Interval(9, 9),
         Interval(39, 43), Interval(71, 81), Interval(22, 26), Interval(73, 81), Interval(52, 68),
         Interval(92, 94), Interval(35, 43), Interval(91, 95), Interval(66, 76), Interval(12, 14),
         Interval(67, 79), Interval(44, 44), Interval(15, 15), Interval(19, 19), Interval(91, 99)],
        # Job 18
        [Interval(89, 97), Interval(30, 38), Interval(33, 39), Interval(73, 91), Interval(28, 28),
         Interval(49, 55), Interval(21, 23), Interval(29, 37), Interval(68, 86), Interval(24, 30),
         Interval(55, 69), Interval(51, 67), Interval(52, 52), Interval(1, 1), Interval(39, 39),
         Interval(73, 97), Interval(55, 69), Interval(31, 37), Interval(69, 85), Interval(64, 84)],
        # Job 19
        [Interval(14, 16), Interval(33, 43), Interval(80, 86), Interval(32, 32), Interval(11, 13),
         Interval(40, 42), Interval(71, 91), Interval(75, 83), Interval(88, 92), Interval(11, 13),
         Interval(17, 19), Interval(36, 38), Interval(1, 1), Interval(85, 97), Interval(72, 74),
         Interval(5, 5), Interval(78, 86), Interval(58, 70), Interval(34, 40), Interval(85, 97)],
    ],
    'name': 'INT__TAI20_20_08.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai20_20_08_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI20_20_08.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI20_20_08.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI20_20_08_F_15_01_INTERVAL_DATA
