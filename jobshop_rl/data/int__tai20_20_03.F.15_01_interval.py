"""
Problema INT__TAI20_20_03.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI20_20_03_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 20,
    'problem_id': 'int__tai20_20_03.F.15_01_interval',
    'sequences': [
        [7, 4, 0, 10, 17, 18, 16, 15, 3, 11, 5, 6, 9, 19, 12, 8, 14, 13, 2, 1],
        [3, 19, 17, 14, 11, 1, 2, 7, 16, 13, 9, 5, 8, 0, 18, 10, 6, 4, 15, 12],
        [15, 0, 4, 8, 2, 14, 18, 12, 7, 5, 6, 16, 17, 11, 10, 13, 19, 9, 1, 3],
        [17, 7, 12, 9, 0, 13, 1, 14, 2, 16, 10, 18, 8, 4, 6, 15, 19, 5, 3, 11],
        [19, 6, 5, 15, 13, 4, 2, 18, 3, 16, 11, 14, 1, 17, 8, 9, 7, 10, 12, 0],
        [14, 0, 5, 18, 11, 2, 12, 7, 6, 13, 4, 19, 15, 1, 3, 10, 16, 17, 9, 8],
        [8, 14, 18, 7, 6, 3, 1, 11, 17, 10, 15, 19, 4, 2, 16, 13, 9, 0, 5, 12],
        [17, 18, 13, 15, 5, 8, 19, 16, 0, 2, 7, 3, 1, 9, 11, 14, 6, 10, 4, 12],
        [11, 0, 9, 18, 1, 19, 16, 12, 6, 10, 7, 14, 15, 8, 4, 13, 17, 5, 2, 3],
        [0, 8, 18, 4, 13, 14, 1, 7, 19, 15, 16, 10, 3, 6, 11, 5, 12, 17, 9, 2],
        [16, 6, 3, 8, 10, 1, 19, 17, 0, 13, 2, 4, 5, 12, 9, 15, 7, 18, 11, 14],
        [4, 7, 16, 10, 9, 0, 18, 1, 19, 8, 14, 2, 13, 11, 6, 5, 12, 15, 3, 17],
        [12, 13, 2, 18, 9, 8, 0, 10, 7, 3, 15, 17, 6, 16, 14, 5, 4, 11, 1, 19],
        [17, 18, 5, 8, 2, 4, 9, 15, 7, 10, 3, 12, 13, 16, 14, 1, 0, 6, 11, 19],
        [12, 7, 10, 2, 18, 4, 19, 14, 13, 3, 6, 1, 5, 16, 15, 8, 9, 0, 11, 17],
        [0, 3, 15, 1, 16, 13, 14, 7, 18, 10, 5, 11, 6, 19, 2, 17, 8, 9, 12, 4],
        [3, 15, 1, 4, 2, 11, 13, 17, 18, 14, 16, 0, 6, 8, 12, 5, 9, 19, 7, 10],
        [2, 17, 10, 1, 19, 12, 6, 8, 15, 14, 5, 9, 3, 18, 11, 13, 0, 4, 16, 7],
        [11, 3, 19, 1, 15, 14, 8, 6, 4, 16, 0, 5, 13, 10, 17, 2, 18, 12, 7, 9],
        [2, 17, 9, 10, 3, 5, 1, 0, 16, 14, 15, 12, 11, 8, 18, 4, 13, 19, 6, 7],
    ],
    'durations': [
        # Job 0
        [Interval(30, 36), Interval(8, 8), Interval(74, 88), Interval(61, 75), Interval(28, 28),
         Interval(79, 103), Interval(86, 96), Interval(72, 76), Interval(7, 7), Interval(7, 7),
         Interval(18, 20), Interval(46, 54), Interval(59, 71), Interval(46, 60), Interval(9, 9),
         Interval(85, 95), Interval(60, 78), Interval(46, 54), Interval(57, 59), Interval(12, 14)],
        # Job 1
        [Interval(65, 73), Interval(10, 10), Interval(53, 63), Interval(10, 10), Interval(91, 91),
         Interval(5, 5), Interval(34, 40), Interval(9, 9), Interval(82, 104), Interval(92, 96),
         Interval(44, 48), Interval(52, 58), Interval(87, 111), Interval(25, 31), Interval(82, 108),
         Interval(92, 96), Interval(4, 4), Interval(46, 56), Interval(54, 64), Interval(10, 10)],
        # Job 2
        [Interval(79, 79), Interval(70, 70), Interval(31, 39), Interval(70, 94), Interval(33, 37),
         Interval(72, 96), Interval(33, 35), Interval(84, 90), Interval(90, 92), Interval(66, 72),
         Interval(12, 12), Interval(29, 33), Interval(87, 101), Interval(56, 74), Interval(13, 13),
         Interval(15, 17), Interval(34, 44), Interval(41, 51), Interval(4, 4), Interval(71, 77)],
        # Job 3
        [Interval(45, 55), Interval(37, 43), Interval(76, 86), Interval(47, 47), Interval(90, 102),
         Interval(60, 74), Interval(85, 103), Interval(49, 57), Interval(21, 23), Interval(17, 17),
         Interval(21, 25), Interval(23, 25), Interval(59, 73), Interval(14, 16), Interval(48, 64),
         Interval(72, 96), Interval(72, 86), Interval(24, 26), Interval(12, 14), Interval(66, 78)],
        # Job 4
        [Interval(7, 7), Interval(75, 87), Interval(55, 69), Interval(44, 56), Interval(82, 100),
         Interval(68, 86), Interval(31, 33), Interval(10, 10), Interval(73, 83), Interval(73, 83),
         Interval(19, 23), Interval(76, 80), Interval(21, 21), Interval(10, 10), Interval(83, 93),
         Interval(22, 24), Interval(91, 93), Interval(32, 36), Interval(83, 93), Interval(42, 54)],
        # Job 5
        [Interval(61, 71), Interval(63, 79), Interval(52, 58), Interval(23, 27), Interval(41, 45),
         Interval(21, 27), Interval(78, 96), Interval(59, 59), Interval(83, 97), Interval(60, 66),
         Interval(87, 93), Interval(22, 22), Interval(6, 6), Interval(47, 53), Interval(9, 9),
         Interval(17, 19), Interval(19, 19), Interval(47, 57), Interval(72, 94), Interval(60, 72)],
        # Job 6
        [Interval(65, 67), Interval(39, 39), Interval(10, 10), Interval(73, 87), Interval(49, 61),
         Interval(38, 38), Interval(29, 29), Interval(41, 41), Interval(63, 63), Interval(31, 33),
         Interval(83, 99), Interval(26, 28), Interval(71, 73), Interval(69, 73), Interval(58, 64),
         Interval(34, 36), Interval(17, 17), Interval(25, 27), Interval(41, 43), Interval(61, 67)],
        # Job 7
        [Interval(11, 11), Interval(29, 37), Interval(77, 91), Interval(11, 13), Interval(16, 20),
         Interval(56, 58), Interval(39, 47), Interval(22, 26), Interval(70, 84), Interval(79, 91),
         Interval(62, 62), Interval(46, 52), Interval(5, 5), Interval(42, 50), Interval(80, 106),
         Interval(80, 90), Interval(89, 95), Interval(28, 32), Interval(63, 65), Interval(70, 84)],
        # Job 8
        [Interval(36, 40), Interval(28, 32), Interval(31, 31), Interval(22, 28), Interval(86, 94),
         Interval(72, 86), Interval(3, 3), Interval(47, 57), Interval(83, 91), Interval(27, 33),
         Interval(85, 89), Interval(4, 4), Interval(54, 60), Interval(40, 46), Interval(50, 60),
         Interval(20, 22), Interval(27, 33), Interval(1, 1), Interval(68, 76), Interval(66, 84)],
        # Job 9
        [Interval(9, 9), Interval(43, 55), Interval(87, 95), Interval(35, 43), Interval(35, 45),
         Interval(56, 62), Interval(18, 22), Interval(26, 28), Interval(67, 67), Interval(21, 23),
         Interval(2, 2), Interval(42, 52), Interval(79, 103), Interval(11, 11), Interval(68, 72),
         Interval(84, 110), Interval(77, 79), Interval(67, 71), Interval(17, 17), Interval(37, 43)],
        # Job 10
        [Interval(51, 63), Interval(31, 33), Interval(65, 69), Interval(24, 28), Interval(22, 24),
         Interval(51, 59), Interval(14, 14), Interval(67, 87), Interval(77, 77), Interval(82, 82),
         Interval(33, 35), Interval(1, 1), Interval(64, 64), Interval(89, 91), Interval(32, 42),
         Interval(41, 53), Interval(25, 29), Interval(49, 59), Interval(3, 3), Interval(87, 101)],
        # Job 11
        [Interval(24, 26), Interval(30, 36), Interval(11, 13), Interval(27, 27), Interval(28, 36),
         Interval(43, 55), Interval(31, 39), Interval(5, 5), Interval(72, 74), Interval(3, 3),
         Interval(25, 31), Interval(50, 58), Interval(43, 47), Interval(30, 34), Interval(50, 56),
         Interval(87, 111), Interval(83, 87), Interval(76, 96), Interval(13, 13), Interval(95, 103)],
        # Job 12
        [Interval(61, 67), Interval(70, 84), Interval(74, 90), Interval(32, 32), Interval(75, 75),
         Interval(32, 32), Interval(67, 69), Interval(15, 17), Interval(61, 65), Interval(80, 82),
         Interval(30, 32), Interval(57, 59), Interval(64, 82), Interval(12, 12), Interval(22, 28),
         Interval(58, 70), Interval(86, 110), Interval(72, 72), Interval(47, 47), Interval(76, 92)],
        # Job 13
        [Interval(15, 19), Interval(97, 99), Interval(99, 99), Interval(35, 43), Interval(63, 83),
         Interval(77, 87), Interval(1, 1), Interval(43, 43), Interval(42, 54), Interval(55, 69),
         Interval(43, 45), Interval(47, 53), Interval(43, 45), Interval(71, 73), Interval(86, 92),
         Interval(41, 49), Interval(39, 49), Interval(21, 21), Interval(76, 82), Interval(52, 68)],
        # Job 14
        [Interval(79, 95), Interval(63, 63), Interval(8, 8), Interval(19, 21), Interval(78, 98),
         Interval(82, 94), Interval(70, 84), Interval(80, 96), Interval(46, 46), Interval(28, 32),
         Interval(43, 45), Interval(37, 47), Interval(82, 86), Interval(40, 42), Interval(73, 75),
         Interval(51, 53), Interval(24, 26), Interval(75, 99), Interval(39, 47), Interval(73, 81)],
        # Job 15
        [Interval(38, 40), Interval(88, 98), Interval(38, 50), Interval(23, 23), Interval(68, 82),
         Interval(7, 7), Interval(57, 63), Interval(43, 47), Interval(71, 71), Interval(48, 50),
         Interval(3, 3), Interval(64, 72), Interval(56, 56), Interval(20, 20), Interval(32, 38),
         Interval(8, 8), Interval(70, 88), Interval(20, 22), Interval(43, 53), Interval(42, 44)],
        # Job 16
        [Interval(64, 86), Interval(92, 92), Interval(81, 85), Interval(45, 51), Interval(7, 7),
         Interval(92, 106), Interval(43, 43), Interval(89, 99), Interval(6, 6), Interval(33, 35),
         Interval(46, 50), Interval(60, 60), Interval(33, 33), Interval(15, 17), Interval(33, 35),
         Interval(99, 99), Interval(79, 87), Interval(10, 12), Interval(73, 87), Interval(39, 47)],
        # Job 17
        [Interval(96, 98), Interval(70, 90), Interval(2, 2), Interval(35, 39), Interval(31, 31),
         Interval(34, 40), Interval(52, 64), Interval(11, 11), Interval(23, 25), Interval(76, 92),
         Interval(10, 10), Interval(28, 32), Interval(89, 105), Interval(89, 89), Interval(41, 53),
         Interval(36, 38), Interval(64, 82), Interval(11, 11), Interval(84, 96), Interval(54, 54)],
        # Job 18
        [Interval(1, 1), Interval(91, 103), Interval(64, 72), Interval(8, 8), Interval(7, 7),
         Interval(67, 77), Interval(37, 39), Interval(46, 54), Interval(39, 45), Interval(30, 34),
         Interval(54, 54), Interval(90, 98), Interval(30, 32), Interval(48, 56), Interval(68, 84),
         Interval(19, 21), Interval(27, 31), Interval(53, 59), Interval(34, 38), Interval(15, 17)],
        # Job 19
        [Interval(27, 31), Interval(27, 35), Interval(49, 49), Interval(88, 94), Interval(7, 7),
         Interval(34, 40), Interval(79, 93), Interval(70, 80), Interval(19, 23), Interval(41, 51),
         Interval(43, 51), Interval(1, 1), Interval(16, 16), Interval(27, 31), Interval(42, 52),
         Interval(75, 87), Interval(51, 53), Interval(39, 49), Interval(86, 104), Interval(78, 80)],
    ],
    'name': 'INT__TAI20_20_03.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai20_20_03_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI20_20_03.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI20_20_03.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI20_20_03_F_15_01_INTERVAL_DATA
