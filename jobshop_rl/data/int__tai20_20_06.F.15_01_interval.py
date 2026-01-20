"""
Problema INT__TAI20_20_06.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI20_20_06_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 20,
    'problem_id': 'int__tai20_20_06.F.15_01_interval',
    'sequences': [
        [10, 2, 9, 3, 7, 4, 18, 12, 6, 14, 15, 0, 5, 17, 8, 13, 19, 11, 16, 1],
        [0, 14, 2, 11, 8, 6, 7, 15, 12, 18, 1, 16, 13, 19, 10, 5, 4, 3, 17, 9],
        [8, 7, 1, 12, 4, 18, 14, 2, 15, 10, 11, 16, 0, 17, 9, 5, 13, 19, 6, 3],
        [10, 15, 0, 6, 18, 16, 9, 2, 19, 5, 11, 13, 8, 7, 4, 17, 12, 1, 3, 14],
        [10, 18, 16, 4, 5, 9, 8, 3, 12, 14, 17, 1, 0, 11, 2, 19, 15, 13, 7, 6],
        [3, 12, 9, 11, 19, 14, 2, 1, 10, 13, 5, 8, 7, 17, 16, 18, 0, 15, 4, 6],
        [2, 7, 6, 19, 5, 9, 11, 16, 10, 8, 1, 18, 4, 0, 13, 3, 15, 14, 12, 17],
        [12, 7, 18, 19, 5, 10, 8, 14, 11, 17, 0, 9, 15, 6, 1, 4, 3, 2, 16, 13],
        [8, 12, 7, 4, 5, 10, 3, 9, 0, 2, 13, 11, 1, 19, 14, 16, 17, 15, 18, 6],
        [17, 14, 5, 10, 13, 11, 9, 4, 2, 7, 0, 3, 6, 8, 18, 1, 15, 16, 19, 12],
        [2, 17, 9, 14, 1, 7, 15, 3, 4, 6, 5, 0, 18, 11, 10, 12, 16, 8, 19, 13],
        [19, 10, 9, 4, 1, 7, 18, 2, 15, 11, 3, 8, 13, 16, 6, 12, 17, 5, 14, 0],
        [0, 16, 1, 12, 17, 13, 8, 19, 4, 3, 7, 9, 18, 15, 10, 6, 2, 11, 5, 14],
        [7, 12, 13, 8, 17, 9, 16, 10, 6, 3, 14, 4, 11, 19, 5, 1, 18, 15, 0, 2],
        [5, 10, 1, 4, 2, 6, 14, 7, 11, 18, 9, 13, 15, 3, 0, 19, 17, 16, 12, 8],
        [4, 13, 18, 3, 19, 10, 14, 2, 12, 1, 7, 11, 5, 8, 15, 6, 9, 0, 16, 17],
        [8, 15, 16, 19, 5, 6, 12, 2, 10, 14, 0, 3, 9, 13, 1, 4, 11, 17, 18, 7],
        [5, 19, 11, 12, 6, 3, 4, 8, 1, 17, 18, 2, 13, 14, 15, 16, 10, 7, 0, 9],
        [7, 1, 10, 18, 14, 16, 5, 13, 4, 19, 2, 6, 0, 12, 11, 15, 3, 17, 8, 9],
        [0, 9, 16, 4, 2, 7, 15, 13, 1, 6, 19, 3, 10, 8, 11, 5, 18, 12, 17, 14],
    ],
    'durations': [
        # Job 0
        [Interval(42, 52), Interval(58, 64), Interval(7, 7), Interval(13, 13), Interval(50, 54),
         Interval(32, 34), Interval(75, 91), Interval(58, 62), Interval(57, 57), Interval(7, 7),
         Interval(65, 83), Interval(84, 102), Interval(54, 64), Interval(41, 51), Interval(7, 7),
         Interval(82, 86), Interval(49, 63), Interval(58, 58), Interval(43, 47), Interval(4, 4)],
        # Job 1
        [Interval(92, 102), Interval(15, 15), Interval(16, 20), Interval(70, 76), Interval(36, 38),
         Interval(89, 99), Interval(19, 21), Interval(61, 77), Interval(13, 13), Interval(26, 26),
         Interval(48, 48), Interval(67, 75), Interval(92, 100), Interval(5, 5), Interval(42, 42),
         Interval(14, 16), Interval(56, 72), Interval(36, 36), Interval(6, 6), Interval(69, 79)],
        # Job 2
        [Interval(81, 93), Interval(79, 99), Interval(28, 28), Interval(79, 83), Interval(43, 51),
         Interval(52, 54), Interval(58, 76), Interval(71, 85), Interval(14, 14), Interval(89, 95),
         Interval(92, 96), Interval(23, 29), Interval(60, 76), Interval(36, 36), Interval(74, 84),
         Interval(70, 72), Interval(87, 101), Interval(27, 29), Interval(22, 28), Interval(2, 2)],
        # Job 3
        [Interval(91, 107), Interval(61, 69), Interval(9, 9), Interval(46, 58), Interval(10, 10),
         Interval(50, 60), Interval(19, 21), Interval(65, 69), Interval(61, 77), Interval(16, 16),
         Interval(10, 10), Interval(50, 58), Interval(47, 47), Interval(4, 4), Interval(62, 70),
         Interval(33, 33), Interval(8, 10), Interval(51, 55), Interval(27, 33), Interval(28, 30)],
        # Job 4
        [Interval(33, 33), Interval(61, 67), Interval(16, 18), Interval(73, 89), Interval(39, 45),
         Interval(52, 68), Interval(13, 15), Interval(84, 106), Interval(31, 41), Interval(83, 107),
         Interval(35, 39), Interval(73, 97), Interval(48, 48), Interval(72, 76), Interval(73, 79),
         Interval(66, 70), Interval(67, 87), Interval(14, 14), Interval(89, 93), Interval(69, 69)],
        # Job 5
        [Interval(86, 86), Interval(16, 16), Interval(31, 37), Interval(71, 95), Interval(78, 80),
         Interval(82, 96), Interval(21, 23), Interval(70, 78), Interval(54, 62), Interval(67, 75),
         Interval(20, 24), Interval(34, 38), Interval(46, 60), Interval(79, 81), Interval(49, 57),
         Interval(1, 1), Interval(55, 59), Interval(63, 73), Interval(23, 29), Interval(23, 29)],
        # Job 6
        [Interval(4, 4), Interval(83, 83), Interval(24, 28), Interval(53, 55), Interval(14, 18),
         Interval(77, 99), Interval(16, 16), Interval(53, 69), Interval(36, 46), Interval(49, 59),
         Interval(91, 105), Interval(3, 3), Interval(81, 87), Interval(10, 12), Interval(53, 57),
         Interval(16, 20), Interval(62, 72), Interval(57, 67), Interval(15, 19), Interval(29, 33)],
        # Job 7
        [Interval(16, 16), Interval(96, 102), Interval(46, 46), Interval(40, 40), Interval(54, 54),
         Interval(24, 30), Interval(68, 74), Interval(95, 95), Interval(9, 9), Interval(44, 48),
         Interval(51, 63), Interval(85, 87), Interval(7, 7), Interval(16, 16), Interval(65, 75),
         Interval(15, 15), Interval(67, 75), Interval(41, 41), Interval(74, 92), Interval(13, 15)],
        # Job 8
        [Interval(27, 33), Interval(22, 26), Interval(94, 96), Interval(41, 41), Interval(50, 56),
         Interval(79, 89), Interval(48, 62), Interval(54, 54), Interval(38, 46), Interval(74, 76),
         Interval(53, 57), Interval(56, 58), Interval(58, 66), Interval(20, 26), Interval(28, 28),
         Interval(3, 3), Interval(79, 87), Interval(80, 96), Interval(10, 12), Interval(63, 73)],
        # Job 9
        [Interval(78, 78), Interval(62, 64), Interval(21, 21), Interval(56, 72), Interval(81, 101),
         Interval(74, 76), Interval(52, 54), Interval(31, 39), Interval(67, 87), Interval(27, 31),
         Interval(62, 74), Interval(85, 99), Interval(86, 92), Interval(47, 51), Interval(47, 47),
         Interval(33, 33), Interval(4, 4), Interval(58, 58), Interval(16, 20), Interval(32, 34)],
        # Job 10
        [Interval(22, 28), Interval(81, 91), Interval(51, 59), Interval(60, 76), Interval(50, 62),
         Interval(37, 49), Interval(23, 23), Interval(14, 16), Interval(78, 98), Interval(24, 32),
         Interval(40, 42), Interval(84, 90), Interval(65, 85), Interval(75, 79), Interval(48, 50),
         Interval(51, 53), Interval(72, 88), Interval(22, 28), Interval(89, 99), Interval(49, 61)],
        # Job 11
        [Interval(36, 44), Interval(28, 30), Interval(26, 28), Interval(68, 72), Interval(67, 85),
         Interval(18, 20), Interval(61, 73), Interval(9, 9), Interval(10, 10), Interval(8, 8),
         Interval(73, 93), Interval(43, 55), Interval(62, 78), Interval(60, 64), Interval(63, 77),
         Interval(37, 39), Interval(58, 78), Interval(42, 50), Interval(71, 83), Interval(9, 9)],
        # Job 12
        [Interval(68, 76), Interval(72, 92), Interval(73, 83), Interval(11, 13), Interval(86, 110),
         Interval(95, 101), Interval(41, 51), Interval(78, 80), Interval(86, 90), Interval(11, 11),
         Interval(31, 41), Interval(59, 75), Interval(89, 105), Interval(20, 24), Interval(53, 53),
         Interval(20, 22), Interval(20, 24), Interval(16, 18), Interval(43, 43), Interval(54, 66)],
        # Job 13
        [Interval(60, 60), Interval(67, 87), Interval(31, 33), Interval(44, 58), Interval(28, 34),
         Interval(61, 69), Interval(17, 19), Interval(3, 3), Interval(30, 32), Interval(11, 13),
         Interval(32, 38), Interval(48, 60), Interval(44, 44), Interval(9, 11), Interval(37, 49),
         Interval(69, 85), Interval(35, 45), Interval(96, 100), Interval(66, 72), Interval(29, 37)],
        # Job 14
        [Interval(71, 73), Interval(42, 42), Interval(19, 21), Interval(2, 2), Interval(43, 57),
         Interval(61, 73), Interval(71, 91), Interval(87, 103), Interval(38, 40), Interval(40, 50),
         Interval(77, 87), Interval(49, 51), Interval(82, 96), Interval(77, 77), Interval(55, 71),
         Interval(44, 44), Interval(40, 44), Interval(35, 45), Interval(75, 97), Interval(77, 91)],
        # Job 15
        [Interval(54, 70), Interval(6, 6), Interval(40, 52), Interval(38, 42), Interval(66, 84),
         Interval(80, 98), Interval(11, 11), Interval(13, 13), Interval(89, 89), Interval(62, 80),
         Interval(60, 78), Interval(74, 98), Interval(53, 67), Interval(81, 103), Interval(51, 61),
         Interval(79, 97), Interval(73, 87), Interval(16, 20), Interval(66, 84), Interval(63, 69)],
        # Job 16
        [Interval(44, 58), Interval(15, 17), Interval(56, 64), Interval(36, 40), Interval(39, 47),
         Interval(83, 105), Interval(3, 3), Interval(46, 60), Interval(78, 82), Interval(87, 105),
         Interval(63, 77), Interval(66, 66), Interval(79, 87), Interval(82, 82), Interval(81, 85),
         Interval(67, 73), Interval(20, 24), Interval(82, 106), Interval(45, 47), Interval(49, 65)],
        # Job 17
        [Interval(6, 6), Interval(25, 31), Interval(62, 80), Interval(8, 10), Interval(24, 30),
         Interval(80, 96), Interval(88, 92), Interval(62, 82), Interval(42, 44), Interval(16, 16),
         Interval(32, 40), Interval(38, 50), Interval(38, 44), Interval(33, 41), Interval(78, 82),
         Interval(73, 95), Interval(79, 93), Interval(86, 96), Interval(22, 26), Interval(3, 3)],
        # Job 18
        [Interval(41, 45), Interval(26, 28), Interval(41, 51), Interval(58, 76), Interval(77, 101),
         Interval(10, 10), Interval(55, 71), Interval(29, 37), Interval(13, 15), Interval(94, 96),
         Interval(57, 65), Interval(57, 75), Interval(62, 74), Interval(46, 46), Interval(27, 27),
         Interval(5, 5), Interval(15, 19), Interval(60, 68), Interval(9, 11), Interval(72, 76)],
        # Job 19
        [Interval(82, 84), Interval(34, 36), Interval(34, 44), Interval(93, 101), Interval(92, 106),
         Interval(75, 79), Interval(92, 104), Interval(87, 89), Interval(44, 58), Interval(29, 33),
         Interval(78, 98), Interval(24, 24), Interval(34, 34), Interval(41, 47), Interval(25, 33),
         Interval(37, 37), Interval(21, 25), Interval(14, 16), Interval(49, 51), Interval(50, 62)],
    ],
    'name': 'INT__TAI20_20_06.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai20_20_06_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI20_20_06.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI20_20_06.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI20_20_06_F_15_01_INTERVAL_DATA
