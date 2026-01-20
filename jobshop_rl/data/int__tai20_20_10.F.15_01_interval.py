"""
Problema INT__TAI20_20_10.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI20_20_10_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 20,
    'problem_id': 'int__tai20_20_10.F.15_01_interval',
    'sequences': [
        [18, 15, 6, 8, 14, 12, 19, 11, 7, 4, 9, 16, 10, 13, 3, 5, 2, 0, 1, 17],
        [18, 13, 8, 3, 1, 19, 14, 16, 0, 2, 9, 10, 11, 4, 5, 12, 6, 7, 15, 17],
        [10, 7, 4, 17, 14, 0, 8, 1, 16, 5, 3, 13, 2, 15, 6, 18, 19, 12, 11, 9],
        [2, 19, 5, 16, 11, 15, 13, 4, 0, 8, 17, 6, 18, 10, 9, 3, 1, 7, 12, 14],
        [12, 15, 2, 3, 11, 7, 10, 17, 9, 16, 0, 13, 4, 14, 1, 19, 8, 6, 5, 18],
        [6, 12, 13, 8, 14, 0, 5, 11, 7, 2, 19, 3, 1, 18, 4, 15, 10, 16, 9, 17],
        [11, 15, 17, 7, 18, 9, 12, 4, 16, 1, 2, 10, 8, 5, 0, 3, 14, 6, 13, 19],
        [18, 17, 0, 7, 4, 12, 1, 10, 2, 15, 13, 14, 19, 5, 6, 3, 9, 8, 11, 16],
        [15, 11, 12, 7, 1, 0, 14, 9, 18, 8, 13, 5, 16, 3, 19, 4, 10, 6, 17, 2],
        [7, 18, 4, 19, 12, 9, 13, 5, 2, 15, 10, 14, 0, 16, 1, 6, 8, 17, 11, 3],
        [17, 13, 18, 14, 19, 1, 6, 11, 12, 4, 15, 0, 16, 3, 10, 8, 2, 9, 7, 5],
        [10, 14, 12, 9, 2, 0, 19, 5, 4, 13, 7, 11, 3, 15, 18, 16, 1, 6, 17, 8],
        [7, 19, 1, 10, 11, 14, 8, 9, 4, 5, 12, 15, 17, 13, 3, 6, 2, 18, 0, 16],
        [17, 11, 13, 1, 2, 4, 7, 0, 10, 8, 3, 19, 14, 6, 9, 5, 18, 16, 12, 15],
        [11, 3, 5, 19, 10, 1, 17, 7, 6, 13, 2, 18, 0, 15, 12, 8, 14, 16, 9, 4],
        [12, 8, 16, 0, 18, 13, 7, 19, 4, 9, 17, 5, 11, 14, 10, 3, 6, 15, 1, 2],
        [9, 5, 19, 7, 11, 12, 16, 14, 13, 0, 8, 4, 10, 18, 1, 6, 3, 17, 15, 2],
        [19, 4, 6, 1, 14, 2, 0, 18, 7, 10, 3, 12, 15, 9, 13, 5, 8, 17, 16, 11],
        [19, 3, 15, 4, 7, 12, 13, 16, 18, 14, 17, 5, 8, 0, 2, 11, 6, 10, 9, 1],
        [11, 17, 13, 4, 3, 15, 18, 12, 0, 10, 5, 19, 9, 2, 7, 14, 6, 8, 1, 16],
    ],
    'durations': [
        # Job 0
        [Interval(77, 91), Interval(9, 9), Interval(32, 36), Interval(62, 62), Interval(11, 11),
         Interval(56, 64), Interval(40, 46), Interval(45, 59), Interval(70, 84), Interval(33, 41),
         Interval(13, 17), Interval(41, 45), Interval(8, 8), Interval(5, 5), Interval(32, 40),
         Interval(53, 59), Interval(40, 52), Interval(47, 55), Interval(79, 93), Interval(82, 90)],
        # Job 1
        [Interval(55, 67), Interval(55, 57), Interval(60, 60), Interval(78, 78), Interval(72, 74),
         Interval(12, 12), Interval(8, 8), Interval(15, 17), Interval(11, 13), Interval(62, 64),
         Interval(31, 31), Interval(59, 65), Interval(91, 103), Interval(49, 57), Interval(1, 1),
         Interval(3, 3), Interval(88, 110), Interval(58, 72), Interval(62, 64), Interval(29, 35)],
        # Job 2
        [Interval(82, 90), Interval(50, 56), Interval(58, 60), Interval(12, 12), Interval(32, 36),
         Interval(27, 27), Interval(2, 2), Interval(79, 93), Interval(73, 97), Interval(21, 21),
         Interval(51, 65), Interval(69, 71), Interval(52, 58), Interval(68, 86), Interval(15, 15),
         Interval(19, 21), Interval(32, 32), Interval(39, 45), Interval(17, 17), Interval(35, 41)],
        # Job 3
        [Interval(3, 3), Interval(12, 14), Interval(59, 75), Interval(13, 13), Interval(59, 67),
         Interval(86, 90), Interval(67, 69), Interval(21, 21), Interval(19, 23), Interval(76, 96),
         Interval(7, 7), Interval(83, 99), Interval(8, 8), Interval(52, 60), Interval(84, 100),
         Interval(51, 65), Interval(91, 97), Interval(47, 61), Interval(49, 65), Interval(78, 96)],
        # Job 4
        [Interval(26, 32), Interval(73, 75), Interval(77, 101), Interval(17, 19), Interval(37, 39),
         Interval(69, 81), Interval(17, 19), Interval(15, 15), Interval(94, 96), Interval(10, 12),
         Interval(22, 26), Interval(4, 4), Interval(12, 12), Interval(15, 19), Interval(34, 34),
         Interval(31, 39), Interval(57, 67), Interval(90, 90), Interval(43, 53), Interval(21, 21)],
        # Job 5
        [Interval(11, 11), Interval(13, 15), Interval(77, 103), Interval(71, 77), Interval(66, 68),
         Interval(79, 103), Interval(66, 74), Interval(8, 8), Interval(7, 7), Interval(49, 49),
         Interval(12, 14), Interval(74, 82), Interval(75, 75), Interval(80, 80), Interval(30, 32),
         Interval(21, 23), Interval(87, 111), Interval(63, 69), Interval(72, 88), Interval(61, 71)],
        # Job 6
        [Interval(95, 99), Interval(60, 66), Interval(11, 11), Interval(66, 76), Interval(1, 1),
         Interval(58, 68), Interval(68, 72), Interval(32, 34), Interval(67, 81), Interval(72, 80),
         Interval(75, 97), Interval(76, 98), Interval(9, 9), Interval(17, 19), Interval(45, 57),
         Interval(24, 30), Interval(42, 54), Interval(30, 32), Interval(39, 51), Interval(75, 77)],
        # Job 7
        [Interval(17, 21), Interval(58, 70), Interval(89, 99), Interval(4, 4), Interval(76, 86),
         Interval(5, 5), Interval(63, 81), Interval(29, 31), Interval(2, 2), Interval(16, 16),
         Interval(36, 40), Interval(84, 102), Interval(15, 15), Interval(15, 19), Interval(58, 64),
         Interval(64, 78), Interval(17, 19), Interval(21, 23), Interval(17, 17), Interval(20, 20)],
        # Job 8
        [Interval(57, 65), Interval(57, 75), Interval(59, 65), Interval(68, 72), Interval(58, 60),
         Interval(80, 80), Interval(75, 89), Interval(2, 2), Interval(95, 99), Interval(70, 82),
         Interval(68, 76), Interval(77, 103), Interval(68, 80), Interval(93, 97), Interval(38, 44),
         Interval(9, 9), Interval(42, 50), Interval(20, 20), Interval(68, 88), Interval(32, 32)],
        # Job 9
        [Interval(55, 67), Interval(90, 90), Interval(35, 39), Interval(75, 97), Interval(15, 15),
         Interval(17, 21), Interval(53, 71), Interval(76, 88), Interval(78, 94), Interval(53, 65),
         Interval(88, 96), Interval(80, 98), Interval(73, 91), Interval(44, 52), Interval(13, 13),
         Interval(26, 32), Interval(25, 31), Interval(43, 47), Interval(73, 95), Interval(55, 69)],
        # Job 10
        [Interval(7, 7), Interval(83, 89), Interval(73, 85), Interval(66, 68), Interval(76, 94),
         Interval(62, 74), Interval(87, 101), Interval(53, 69), Interval(45, 49), Interval(43, 55),
         Interval(46, 54), Interval(55, 55), Interval(3, 3), Interval(17, 19), Interval(77, 81),
         Interval(32, 32), Interval(38, 48), Interval(85, 109), Interval(50, 56), Interval(43, 45)],
        # Job 11
        [Interval(20, 20), Interval(45, 55), Interval(68, 76), Interval(84, 96), Interval(25, 25),
         Interval(23, 25), Interval(41, 45), Interval(4, 4), Interval(23, 29), Interval(55, 69),
         Interval(37, 47), Interval(68, 86), Interval(8, 10), Interval(57, 65), Interval(18, 20),
         Interval(66, 72), Interval(9, 9), Interval(54, 66), Interval(5, 5), Interval(49, 59)],
        # Job 12
        [Interval(44, 46), Interval(67, 79), Interval(49, 51), Interval(53, 63), Interval(94, 94),
         Interval(77, 103), Interval(93, 101), Interval(42, 42), Interval(35, 37), Interval(69, 75),
         Interval(79, 89), Interval(29, 37), Interval(44, 44), Interval(59, 59), Interval(46, 48),
         Interval(38, 42), Interval(75, 87), Interval(77, 93), Interval(26, 26), Interval(27, 29)],
        # Job 13
        [Interval(63, 71), Interval(46, 46), Interval(9, 9), Interval(39, 41), Interval(76, 86),
         Interval(91, 103), Interval(7, 7), Interval(2, 2), Interval(68, 70), Interval(9, 9),
         Interval(16, 18), Interval(73, 89), Interval(80, 82), Interval(41, 51), Interval(25, 27),
         Interval(27, 33), Interval(83, 93), Interval(71, 75), Interval(39, 49), Interval(86, 112)],
        # Job 14
        [Interval(15, 17), Interval(60, 64), Interval(3, 3), Interval(29, 31), Interval(15, 17),
         Interval(38, 42), Interval(55, 69), Interval(96, 96), Interval(74, 76), Interval(60, 78),
         Interval(83, 89), Interval(83, 97), Interval(84, 102), Interval(14, 16), Interval(29, 31),
         Interval(40, 52), Interval(50, 50), Interval(26, 32), Interval(9, 9), Interval(93, 101)],
        # Job 15
        [Interval(5, 5), Interval(64, 82), Interval(51, 57), Interval(76, 86), Interval(24, 28),
         Interval(33, 39), Interval(33, 37), Interval(51, 61), Interval(57, 67), Interval(31, 31),
         Interval(2, 2), Interval(21, 25), Interval(52, 68), Interval(12, 12), Interval(87, 89),
         Interval(35, 41), Interval(83, 107), Interval(60, 70), Interval(86, 86), Interval(60, 68)],
        # Job 16
        [Interval(3, 3), Interval(99, 99), Interval(75, 87), Interval(81, 105), Interval(72, 92),
         Interval(17, 17), Interval(1, 1), Interval(1, 1), Interval(28, 36), Interval(36, 36),
         Interval(27, 33), Interval(56, 68), Interval(80, 100), Interval(20, 20), Interval(97, 99),
         Interval(3, 3), Interval(64, 68), Interval(73, 77), Interval(78, 80), Interval(63, 71)],
        # Job 17
        [Interval(50, 54), Interval(66, 86), Interval(71, 87), Interval(58, 68), Interval(50, 54),
         Interval(23, 23), Interval(31, 39), Interval(21, 23), Interval(54, 62), Interval(12, 14),
         Interval(25, 27), Interval(61, 75), Interval(75, 93), Interval(16, 16), Interval(28, 28),
         Interval(28, 28), Interval(49, 59), Interval(73, 79), Interval(79, 93), Interval(46, 48)],
        # Job 18
        [Interval(71, 77), Interval(32, 36), Interval(64, 72), Interval(35, 39), Interval(25, 27),
         Interval(43, 53), Interval(28, 30), Interval(22, 26), Interval(53, 67), Interval(91, 105),
         Interval(54, 54), Interval(84, 110), Interval(18, 20), Interval(88, 110), Interval(62, 62),
         Interval(44, 48), Interval(23, 27), Interval(48, 58), Interval(10, 12), Interval(4, 4)],
        # Job 19
        [Interval(15, 15), Interval(85, 99), Interval(38, 44), Interval(55, 71), Interval(83, 91),
         Interval(65, 69), Interval(75, 79), Interval(82, 96), Interval(62, 68), Interval(17, 17),
         Interval(23, 25), Interval(63, 71), Interval(10, 10), Interval(82, 92), Interval(87, 95),
         Interval(55, 61), Interval(45, 59), Interval(24, 28), Interval(29, 37), Interval(3, 3)],
    ],
    'name': 'INT__TAI20_20_10.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai20_20_10_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI20_20_10.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI20_20_10.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI20_20_10_F_15_01_INTERVAL_DATA
