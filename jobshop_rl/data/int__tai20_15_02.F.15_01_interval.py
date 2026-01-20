"""
Problema INT__TAI20_15_02.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI20_15_02_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__tai20_15_02.F.15_01_interval',
    'sequences': [
        [2, 5, 1, 8, 3, 4, 14, 7, 10, 13, 11, 9, 12, 6, 0],
        [14, 8, 12, 4, 11, 3, 6, 9, 0, 10, 1, 13, 2, 7, 5],
        [7, 12, 1, 8, 2, 10, 3, 11, 13, 14, 5, 6, 0, 9, 4],
        [1, 8, 5, 11, 7, 6, 3, 2, 4, 9, 12, 13, 0, 14, 10],
        [8, 4, 12, 1, 3, 14, 2, 9, 13, 6, 5, 10, 11, 7, 0],
        [2, 14, 10, 7, 3, 0, 1, 13, 9, 6, 11, 12, 4, 5, 8],
        [0, 4, 13, 1, 8, 10, 11, 6, 9, 2, 5, 12, 7, 3, 14],
        [12, 2, 11, 9, 8, 10, 13, 4, 5, 14, 6, 3, 1, 7, 0],
        [7, 3, 4, 5, 13, 0, 11, 10, 9, 1, 8, 6, 12, 14, 2],
        [7, 14, 12, 6, 5, 9, 10, 0, 3, 4, 2, 1, 8, 13, 11],
        [0, 9, 13, 7, 6, 3, 11, 8, 10, 4, 2, 1, 14, 12, 5],
        [14, 10, 3, 12, 5, 7, 4, 6, 1, 2, 0, 13, 9, 11, 8],
        [11, 10, 5, 1, 3, 13, 9, 7, 8, 14, 0, 2, 6, 12, 4],
        [7, 6, 13, 10, 3, 1, 5, 11, 4, 8, 0, 12, 9, 2, 14],
        [2, 4, 14, 5, 0, 7, 10, 12, 1, 9, 3, 8, 6, 13, 11],
        [5, 14, 12, 7, 3, 13, 0, 9, 10, 6, 1, 2, 8, 4, 11],
        [14, 8, 1, 10, 11, 12, 7, 0, 3, 2, 9, 13, 5, 6, 4],
        [5, 2, 10, 3, 12, 4, 6, 11, 0, 13, 8, 14, 7, 1, 9],
        [0, 9, 10, 4, 2, 6, 13, 1, 3, 14, 7, 8, 5, 12, 11],
        [2, 12, 9, 8, 4, 6, 10, 14, 7, 5, 1, 11, 3, 0, 13],
    ],
    'durations': [
        # Job 0
        [Interval(55, 55), Interval(66, 66), Interval(41, 55), Interval(57, 61), Interval(7, 9),
         Interval(18, 24), Interval(64, 64), Interval(6, 8), Interval(80, 80), Interval(5, 5),
         Interval(52, 66), Interval(7, 9), Interval(86, 96), Interval(10, 12), Interval(81, 81)],
        # Job 1
        [Interval(77, 95), Interval(68, 84), Interval(39, 41), Interval(70, 82), Interval(8, 10),
         Interval(22, 24), Interval(79, 81), Interval(44, 58), Interval(45, 47), Interval(43, 53),
         Interval(61, 75), Interval(48, 54), Interval(14, 16), Interval(5, 5), Interval(73, 91)],
        # Job 2
        [Interval(72, 96), Interval(94, 100), Interval(24, 28), Interval(63, 77), Interval(31, 35),
         Interval(27, 35), Interval(17, 23), Interval(36, 42), Interval(39, 45), Interval(30, 36),
         Interval(66, 74), Interval(81, 87), Interval(20, 26), Interval(46, 62), Interval(49, 61)],
        # Job 3
        [Interval(51, 69), Interval(79, 85), Interval(12, 16), Interval(33, 39), Interval(20, 24),
         Interval(19, 23), Interval(3, 3), Interval(11, 11), Interval(75, 89), Interval(84, 100),
         Interval(52, 52), Interval(85, 85), Interval(73, 81), Interval(3, 3), Interval(83, 95)],
        # Job 4
        [Interval(81, 85), Interval(31, 35), Interval(13, 17), Interval(34, 38), Interval(90, 102),
         Interval(98, 100), Interval(72, 90), Interval(24, 24), Interval(52, 66), Interval(81, 97),
         Interval(11, 11), Interval(12, 14), Interval(23, 29), Interval(89, 93), Interval(77, 97)],
        # Job 5
        [Interval(44, 58), Interval(17, 23), Interval(76, 102), Interval(92, 106), Interval(82, 108),
         Interval(40, 42), Interval(6, 8), Interval(65, 69), Interval(66, 88), Interval(43, 47),
         Interval(72, 76), Interval(91, 91), Interval(76, 98), Interval(1, 1), Interval(54, 56)],
        # Job 6
        [Interval(32, 38), Interval(62, 80), Interval(41, 53), Interval(29, 39), Interval(67, 87),
         Interval(63, 73), Interval(74, 96), Interval(24, 30), Interval(2, 2), Interval(98, 100),
         Interval(9, 9), Interval(18, 18), Interval(24, 32), Interval(33, 33), Interval(82, 102)],
        # Job 7
        [Interval(76, 76), Interval(56, 60), Interval(32, 42), Interval(27, 29), Interval(78, 82),
         Interval(93, 99), Interval(92, 102), Interval(92, 92), Interval(82, 86), Interval(59, 77),
         Interval(1, 1), Interval(78, 94), Interval(32, 34), Interval(61, 71), Interval(20, 20)],
        # Job 8
        [Interval(15, 19), Interval(10, 12), Interval(17, 19), Interval(81, 99), Interval(49, 65),
         Interval(83, 107), Interval(15, 19), Interval(33, 33), Interval(61, 61), Interval(44, 54),
         Interval(31, 41), Interval(34, 42), Interval(57, 67), Interval(67, 79), Interval(23, 27)],
        # Job 9
        [Interval(81, 83), Interval(72, 96), Interval(86, 88), Interval(42, 46), Interval(90, 102),
         Interval(61, 67), Interval(58, 78), Interval(52, 62), Interval(56, 74), Interval(76, 102),
         Interval(38, 46), Interval(76, 78), Interval(42, 44), Interval(67, 85), Interval(38, 38)],
        # Job 10
        [Interval(52, 56), Interval(62, 70), Interval(7, 9), Interval(41, 55), Interval(82, 86),
         Interval(14, 16), Interval(87, 99), Interval(89, 99), Interval(55, 59), Interval(15, 17),
         Interval(64, 64), Interval(13, 13), Interval(56, 68), Interval(54, 72), Interval(47, 59)],
        # Job 11
        [Interval(20, 22), Interval(62, 78), Interval(42, 42), Interval(28, 30), Interval(74, 92),
         Interval(5, 5), Interval(15, 17), Interval(70, 82), Interval(62, 72), Interval(41, 51),
         Interval(63, 71), Interval(73, 93), Interval(43, 49), Interval(27, 31), Interval(24, 28)],
        # Job 12
        [Interval(91, 101), Interval(40, 44), Interval(44, 54), Interval(50, 58), Interval(53, 63),
         Interval(7, 9), Interval(41, 41), Interval(13, 15), Interval(31, 39), Interval(9, 9),
         Interval(70, 78), Interval(14, 18), Interval(44, 56), Interval(68, 70), Interval(41, 49)],
        # Job 13
        [Interval(60, 78), Interval(85, 95), Interval(17, 17), Interval(18, 18), Interval(42, 48),
         Interval(41, 55), Interval(28, 34), Interval(26, 32), Interval(27, 27), Interval(76, 94),
         Interval(62, 80), Interval(82, 102), Interval(19, 21), Interval(11, 11), Interval(79, 93)],
        # Job 14
        [Interval(39, 43), Interval(21, 27), Interval(75, 89), Interval(43, 57), Interval(24, 24),
         Interval(73, 77), Interval(32, 36), Interval(73, 87), Interval(69, 73), Interval(46, 62),
         Interval(5, 5), Interval(36, 48), Interval(7, 9), Interval(30, 40), Interval(84, 102)],
        # Job 15
        [Interval(63, 63), Interval(4, 4), Interval(77, 93), Interval(51, 55), Interval(54, 68),
         Interval(46, 62), Interval(14, 18), Interval(17, 19), Interval(5, 5), Interval(42, 44),
         Interval(21, 27), Interval(84, 92), Interval(61, 73), Interval(70, 88), Interval(36, 46)],
        # Job 16
        [Interval(17, 17), Interval(35, 39), Interval(54, 58), Interval(66, 74), Interval(53, 59),
         Interval(21, 27), Interval(88, 102), Interval(11, 13), Interval(82, 110), Interval(27, 27),
         Interval(48, 62), Interval(33, 39), Interval(40, 42), Interval(65, 65), Interval(22, 24)],
        # Job 17
        [Interval(77, 81), Interval(6, 6), Interval(77, 101), Interval(65, 73), Interval(15, 17),
         Interval(48, 64), Interval(70, 92), Interval(96, 100), Interval(12, 12), Interval(17, 21),
         Interval(87, 89), Interval(3, 3), Interval(31, 41), Interval(64, 70), Interval(64, 84)],
        # Job 18
        [Interval(36, 40), Interval(67, 85), Interval(45, 49), Interval(19, 23), Interval(78, 82),
         Interval(95, 99), Interval(31, 39), Interval(41, 49), Interval(65, 83), Interval(81, 103),
         Interval(96, 100), Interval(48, 60), Interval(80, 102), Interval(72, 86), Interval(41, 51)],
        # Job 19
        [Interval(32, 36), Interval(51, 61), Interval(23, 29), Interval(55, 69), Interval(78, 86),
         Interval(37, 39), Interval(82, 96), Interval(31, 35), Interval(49, 51), Interval(53, 71),
         Interval(37, 41), Interval(56, 70), Interval(85, 91), Interval(13, 13), Interval(37, 47)],
    ],
    'name': 'INT__TAI20_15_02.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai20_15_02_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI20_15_02.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI20_15_02.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI20_15_02_F_15_01_INTERVAL_DATA
