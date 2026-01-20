"""
Problema INT__TAI20_15_09.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI20_15_09_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__tai20_15_09.F.15_01_interval',
    'sequences': [
        [8, 1, 10, 7, 9, 5, 6, 3, 2, 13, 4, 0, 14, 11, 12],
        [1, 9, 4, 5, 0, 11, 6, 7, 12, 2, 14, 8, 13, 10, 3],
        [6, 2, 8, 9, 3, 5, 4, 12, 11, 7, 10, 13, 0, 14, 1],
        [4, 9, 1, 2, 13, 3, 6, 0, 12, 5, 10, 7, 8, 11, 14],
        [6, 7, 9, 13, 11, 1, 5, 0, 12, 3, 14, 2, 4, 8, 10],
        [2, 12, 6, 13, 8, 4, 1, 14, 5, 9, 10, 0, 3, 7, 11],
        [13, 2, 12, 5, 11, 6, 8, 4, 10, 7, 1, 0, 3, 9, 14],
        [9, 8, 14, 7, 3, 10, 1, 12, 4, 13, 11, 6, 5, 0, 2],
        [14, 3, 6, 8, 12, 9, 4, 5, 1, 7, 0, 10, 2, 11, 13],
        [11, 4, 14, 8, 13, 10, 9, 0, 5, 6, 2, 12, 3, 1, 7],
        [6, 2, 8, 0, 3, 5, 7, 10, 14, 9, 11, 13, 4, 1, 12],
        [9, 1, 14, 0, 13, 2, 7, 8, 5, 11, 4, 10, 6, 3, 12],
        [8, 11, 12, 3, 7, 13, 6, 1, 14, 5, 9, 2, 4, 0, 10],
        [8, 12, 7, 11, 3, 14, 6, 10, 5, 1, 2, 9, 0, 4, 13],
        [10, 13, 12, 8, 3, 11, 5, 14, 0, 4, 2, 6, 1, 9, 7],
        [8, 6, 10, 14, 1, 11, 3, 5, 12, 9, 2, 4, 0, 7, 13],
        [13, 2, 8, 14, 7, 0, 9, 6, 3, 11, 10, 5, 12, 1, 4],
        [0, 13, 12, 6, 7, 2, 11, 14, 8, 3, 4, 10, 1, 5, 9],
        [9, 6, 2, 12, 0, 8, 11, 4, 5, 1, 7, 3, 14, 10, 13],
        [2, 8, 6, 12, 14, 10, 13, 5, 0, 7, 11, 9, 3, 4, 1],
    ],
    'durations': [
        # Job 0
        [Interval(77, 79), Interval(22, 22), Interval(76, 102), Interval(44, 48), Interval(39, 45),
         Interval(52, 66), Interval(13, 13), Interval(83, 97), Interval(41, 41), Interval(61, 77),
         Interval(62, 80), Interval(13, 13), Interval(41, 55), Interval(97, 97), Interval(55, 69)],
        # Job 1
        [Interval(77, 97), Interval(54, 58), Interval(41, 47), Interval(1, 1), Interval(63, 85),
         Interval(3, 3), Interval(83, 95), Interval(76, 78), Interval(25, 33), Interval(17, 17),
         Interval(11, 13), Interval(54, 66), Interval(86, 98), Interval(33, 37), Interval(22, 26)],
        # Job 2
        [Interval(49, 65), Interval(6, 6), Interval(71, 75), Interval(33, 39), Interval(51, 63),
         Interval(23, 27), Interval(82, 106), Interval(18, 24), Interval(43, 49), Interval(82, 96),
         Interval(42, 52), Interval(2, 2), Interval(54, 60), Interval(64, 70), Interval(48, 62)],
        # Job 3
        [Interval(63, 85), Interval(35, 45), Interval(1, 1), Interval(32, 42), Interval(50, 54),
         Interval(72, 96), Interval(46, 54), Interval(36, 42), Interval(59, 71), Interval(79, 81),
         Interval(41, 47), Interval(64, 76), Interval(25, 25), Interval(27, 27), Interval(12, 12)],
        # Job 4
        [Interval(14, 16), Interval(71, 73), Interval(23, 27), Interval(59, 79), Interval(8, 8),
         Interval(90, 102), Interval(14, 14), Interval(12, 14), Interval(31, 31), Interval(64, 84),
         Interval(12, 14), Interval(91, 91), Interval(35, 43), Interval(51, 63), Interval(45, 47)],
        # Job 5
        [Interval(85, 105), Interval(2, 2), Interval(58, 78), Interval(19, 25), Interval(34, 46),
         Interval(31, 35), Interval(31, 41), Interval(31, 33), Interval(46, 54), Interval(31, 33),
         Interval(9, 11), Interval(60, 66), Interval(83, 87), Interval(16, 16), Interval(1, 1)],
        # Job 6
        [Interval(13, 17), Interval(95, 101), Interval(19, 23), Interval(9, 11), Interval(31, 39),
         Interval(65, 87), Interval(25, 33), Interval(60, 68), Interval(29, 39), Interval(23, 27),
         Interval(87, 89), Interval(30, 30), Interval(52, 52), Interval(37, 49), Interval(45, 45)],
        # Job 7
        [Interval(12, 16), Interval(21, 21), Interval(82, 90), Interval(2, 2), Interval(17, 21),
         Interval(74, 82), Interval(90, 94), Interval(82, 88), Interval(51, 57), Interval(61, 61),
         Interval(6, 6), Interval(13, 13), Interval(75, 95), Interval(78, 96), Interval(41, 45)],
        # Job 8
        [Interval(7, 9), Interval(58, 58), Interval(58, 76), Interval(15, 17), Interval(93, 105),
         Interval(30, 36), Interval(12, 16), Interval(41, 53), Interval(19, 23), Interval(77, 77),
         Interval(64, 64), Interval(26, 32), Interval(64, 82), Interval(9, 11), Interval(43, 51)],
        # Job 9
        [Interval(50, 60), Interval(75, 93), Interval(54, 56), Interval(23, 29), Interval(83, 83),
         Interval(6, 6), Interval(95, 103), Interval(48, 54), Interval(27, 29), Interval(54, 72),
         Interval(85, 101), Interval(45, 59), Interval(74, 98), Interval(61, 75), Interval(46, 46)],
        # Job 10
        [Interval(42, 44), Interval(17, 21), Interval(32, 32), Interval(35, 37), Interval(17, 19),
         Interval(53, 67), Interval(83, 111), Interval(13, 13), Interval(46, 50), Interval(34, 38),
         Interval(75, 83), Interval(14, 14), Interval(63, 75), Interval(15, 15), Interval(23, 23)],
        # Job 11
        [Interval(11, 13), Interval(58, 78), Interval(31, 41), Interval(69, 75), Interval(80, 100),
         Interval(68, 68), Interval(27, 29), Interval(12, 14), Interval(17, 19), Interval(62, 74),
         Interval(46, 52), Interval(46, 58), Interval(47, 53), Interval(56, 70), Interval(10, 10)],
        # Job 12
        [Interval(71, 81), Interval(68, 82), Interval(69, 77), Interval(38, 42), Interval(52, 64),
         Interval(22, 24), Interval(6, 6), Interval(28, 34), Interval(5, 5), Interval(15, 17),
         Interval(73, 73), Interval(37, 45), Interval(41, 53), Interval(63, 71), Interval(35, 39)],
        # Job 13
        [Interval(81, 105), Interval(51, 65), Interval(58, 58), Interval(84, 102), Interval(18, 24),
         Interval(85, 95), Interval(13, 13), Interval(81, 83), Interval(6, 6), Interval(57, 67),
         Interval(45, 59), Interval(40, 48), Interval(4, 4), Interval(26, 32), Interval(20, 20)],
        # Job 14
        [Interval(88, 108), Interval(58, 74), Interval(56, 70), Interval(60, 66), Interval(68, 74),
         Interval(8, 10), Interval(10, 10), Interval(83, 105), Interval(85, 101), Interval(67, 87),
         Interval(46, 48), Interval(39, 41), Interval(23, 25), Interval(88, 104), Interval(54, 58)],
        # Job 15
        [Interval(29, 37), Interval(16, 20), Interval(86, 104), Interval(69, 91), Interval(78, 96),
         Interval(3, 3), Interval(72, 72), Interval(16, 20), Interval(29, 31), Interval(29, 35),
         Interval(80, 106), Interval(9, 11), Interval(81, 91), Interval(57, 59), Interval(40, 50)],
        # Job 16
        [Interval(66, 72), Interval(76, 90), Interval(55, 69), Interval(67, 87), Interval(40, 42),
         Interval(13, 13), Interval(8, 8), Interval(81, 93), Interval(3, 3), Interval(61, 69),
         Interval(35, 45), Interval(10, 12), Interval(29, 35), Interval(61, 81), Interval(84, 88)],
        # Job 17
        [Interval(18, 24), Interval(70, 84), Interval(74, 78), Interval(77, 77), Interval(57, 65),
         Interval(80, 84), Interval(66, 86), Interval(39, 45), Interval(6, 6), Interval(82, 94),
         Interval(44, 58), Interval(43, 57), Interval(29, 29), Interval(62, 64), Interval(16, 20)],
        # Job 18
        [Interval(86, 88), Interval(14, 18), Interval(94, 102), Interval(23, 31), Interval(55, 61),
         Interval(52, 66), Interval(66, 72), Interval(88, 102), Interval(83, 87), Interval(78, 82),
         Interval(87, 107), Interval(80, 96), Interval(10, 12), Interval(7, 9), Interval(41, 43)],
        # Job 19
        [Interval(23, 27), Interval(14, 18), Interval(18, 22), Interval(59, 75), Interval(79, 91),
         Interval(67, 81), Interval(42, 54), Interval(39, 49), Interval(90, 100), Interval(27, 29),
         Interval(61, 71), Interval(32, 36), Interval(25, 25), Interval(80, 108), Interval(18, 20)],
    ],
    'name': 'INT__TAI20_15_09.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai20_15_09_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI20_15_09.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI20_15_09.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI20_15_09_F_15_01_INTERVAL_DATA
