"""
Problema INT__TAI20_15_06.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI20_15_06_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__tai20_15_06.F.15_01_interval',
    'sequences': [
        [2, 11, 0, 13, 1, 8, 9, 6, 4, 7, 12, 3, 14, 5, 10],
        [5, 8, 9, 3, 1, 13, 11, 0, 14, 7, 4, 12, 10, 6, 2],
        [5, 2, 8, 14, 13, 1, 6, 9, 12, 4, 11, 0, 7, 3, 10],
        [8, 10, 4, 0, 3, 11, 13, 6, 1, 5, 2, 9, 12, 14, 7],
        [8, 11, 1, 0, 5, 13, 2, 14, 10, 12, 9, 3, 4, 6, 7],
        [11, 3, 13, 9, 14, 1, 0, 7, 4, 5, 10, 12, 6, 2, 8],
        [13, 3, 11, 10, 5, 12, 0, 4, 14, 6, 7, 8, 9, 2, 1],
        [5, 8, 6, 7, 2, 3, 10, 4, 1, 14, 11, 9, 13, 0, 12],
        [12, 8, 9, 7, 3, 6, 11, 13, 10, 0, 2, 5, 1, 4, 14],
        [5, 14, 11, 4, 10, 8, 9, 2, 13, 12, 7, 1, 0, 3, 6],
        [10, 9, 1, 12, 2, 7, 3, 4, 0, 5, 6, 8, 13, 14, 11],
        [9, 7, 5, 6, 0, 14, 1, 3, 8, 11, 2, 12, 10, 13, 4],
        [2, 13, 12, 3, 9, 1, 5, 10, 11, 6, 0, 7, 8, 14, 4],
        [3, 0, 9, 13, 8, 2, 6, 1, 10, 12, 7, 14, 4, 5, 11],
        [6, 5, 0, 13, 8, 14, 2, 7, 12, 4, 10, 3, 1, 9, 11],
        [6, 8, 0, 7, 4, 1, 11, 10, 13, 14, 12, 2, 9, 3, 5],
        [13, 2, 1, 8, 3, 12, 6, 14, 11, 9, 5, 7, 4, 10, 0],
        [13, 7, 5, 11, 4, 6, 10, 14, 2, 9, 0, 3, 8, 12, 1],
        [9, 2, 10, 11, 7, 1, 14, 3, 6, 8, 5, 4, 12, 0, 13],
        [13, 4, 11, 12, 7, 0, 5, 1, 8, 14, 9, 2, 3, 10, 6],
    ],
    'durations': [
        # Job 0
        [Interval(75, 77), Interval(17, 17), Interval(50, 66), Interval(25, 27), Interval(83, 97),
         Interval(67, 87), Interval(63, 63), Interval(80, 94), Interval(74, 74), Interval(31, 39),
         Interval(52, 68), Interval(85, 95), Interval(55, 73), Interval(68, 68), Interval(25, 31)],
        # Job 1
        [Interval(5, 5), Interval(71, 87), Interval(69, 73), Interval(39, 45), Interval(61, 81),
         Interval(19, 21), Interval(85, 87), Interval(75, 101), Interval(45, 49), Interval(55, 69),
         Interval(34, 40), Interval(81, 93), Interval(44, 50), Interval(87, 107), Interval(21, 27)],
        # Job 2
        [Interval(2, 2), Interval(65, 69), Interval(25, 31), Interval(88, 108), Interval(61, 71),
         Interval(37, 47), Interval(41, 51), Interval(21, 25), Interval(87, 101), Interval(23, 27),
         Interval(83, 95), Interval(3, 3), Interval(37, 39), Interval(67, 85), Interval(65, 87)],
        # Job 3
        [Interval(85, 107), Interval(68, 90), Interval(19, 19), Interval(31, 41), Interval(80, 94),
         Interval(6, 6), Interval(8, 10), Interval(17, 19), Interval(32, 32), Interval(34, 40),
         Interval(50, 60), Interval(3, 3), Interval(15, 15), Interval(12, 12), Interval(43, 47)],
        # Job 4
        [Interval(66, 76), Interval(72, 74), Interval(16, 18), Interval(35, 47), Interval(67, 75),
         Interval(83, 93), Interval(43, 43), Interval(53, 65), Interval(37, 37), Interval(19, 25),
         Interval(19, 23), Interval(77, 77), Interval(58, 74), Interval(41, 51), Interval(51, 53)],
        # Job 5
        [Interval(17, 21), Interval(11, 13), Interval(76, 98), Interval(19, 25), Interval(38, 44),
         Interval(25, 33), Interval(6, 6), Interval(4, 4), Interval(77, 81), Interval(72, 84),
         Interval(20, 22), Interval(23, 31), Interval(16, 16), Interval(53, 55), Interval(60, 60)],
        # Job 6
        [Interval(84, 108), Interval(38, 40), Interval(75, 89), Interval(13, 17), Interval(19, 25),
         Interval(25, 33), Interval(55, 73), Interval(86, 98), Interval(59, 77), Interval(54, 66),
         Interval(37, 37), Interval(10, 10), Interval(47, 47), Interval(58, 78), Interval(74, 74)],
        # Job 7
        [Interval(25, 31), Interval(3, 3), Interval(71, 71), Interval(57, 61), Interval(80, 108),
         Interval(57, 63), Interval(96, 100), Interval(75, 79), Interval(9, 9), Interval(57, 57),
         Interval(21, 21), Interval(64, 84), Interval(18, 20), Interval(70, 78), Interval(18, 20)],
        # Job 8
        [Interval(7, 7), Interval(33, 43), Interval(58, 68), Interval(65, 73), Interval(12, 14),
         Interval(48, 64), Interval(47, 59), Interval(52, 64), Interval(2, 2), Interval(93, 93),
         Interval(90, 90), Interval(6, 6), Interval(59, 73), Interval(66, 86), Interval(53, 67)],
        # Job 9
        [Interval(78, 92), Interval(42, 50), Interval(67, 83), Interval(34, 34), Interval(29, 37),
         Interval(93, 95), Interval(48, 52), Interval(19, 21), Interval(4, 4), Interval(27, 29),
         Interval(51, 69), Interval(67, 81), Interval(77, 103), Interval(44, 58), Interval(60, 74)],
        # Job 10
        [Interval(87, 89), Interval(11, 11), Interval(31, 39), Interval(86, 88), Interval(14, 14),
         Interval(79, 91), Interval(11, 13), Interval(18, 24), Interval(23, 23), Interval(35, 39),
         Interval(12, 12), Interval(84, 92), Interval(94, 102), Interval(30, 36), Interval(75, 77)],
        # Job 11
        [Interval(29, 31), Interval(80, 98), Interval(78, 104), Interval(3, 3), Interval(85, 109),
         Interval(68, 74), Interval(65, 81), Interval(16, 16), Interval(15, 15), Interval(88, 108),
         Interval(67, 75), Interval(18, 20), Interval(61, 69), Interval(78, 100), Interval(2, 2)],
        # Job 12
        [Interval(57, 65), Interval(76, 96), Interval(66, 76), Interval(71, 81), Interval(80, 96),
         Interval(31, 33), Interval(30, 32), Interval(45, 55), Interval(24, 26), Interval(76, 92),
         Interval(72, 86), Interval(34, 34), Interval(54, 64), Interval(66, 84), Interval(73, 83)],
        # Job 13
        [Interval(9, 9), Interval(51, 67), Interval(81, 105), Interval(68, 70), Interval(34, 42),
         Interval(57, 73), Interval(91, 101), Interval(66, 68), Interval(73, 75), Interval(38, 44),
         Interval(53, 69), Interval(61, 75), Interval(10, 12), Interval(24, 24), Interval(23, 27)],
        # Job 14
        [Interval(75, 97), Interval(69, 85), Interval(20, 22), Interval(48, 52), Interval(66, 78),
         Interval(65, 71), Interval(80, 102), Interval(66, 78), Interval(57, 73), Interval(51, 53),
         Interval(44, 46), Interval(5, 5), Interval(67, 75), Interval(62, 74), Interval(25, 25)],
        # Job 15
        [Interval(32, 42), Interval(23, 31), Interval(21, 25), Interval(23, 29), Interval(2, 2),
         Interval(32, 40), Interval(20, 20), Interval(59, 71), Interval(58, 64), Interval(24, 30),
         Interval(30, 40), Interval(45, 55), Interval(42, 48), Interval(78, 82), Interval(17, 21)],
        # Job 16
        [Interval(5, 5), Interval(55, 59), Interval(64, 76), Interval(84, 106), Interval(41, 51),
         Interval(35, 37), Interval(82, 94), Interval(41, 43), Interval(46, 52), Interval(22, 24),
         Interval(56, 70), Interval(71, 83), Interval(42, 52), Interval(75, 101), Interval(7, 7)],
        # Job 17
        [Interval(25, 33), Interval(58, 70), Interval(23, 23), Interval(42, 42), Interval(31, 35),
         Interval(64, 66), Interval(80, 104), Interval(75, 85), Interval(46, 52), Interval(3, 3),
         Interval(71, 95), Interval(17, 23), Interval(62, 64), Interval(77, 79), Interval(74, 96)],
        # Job 18
        [Interval(66, 68), Interval(40, 54), Interval(46, 50), Interval(50, 64), Interval(80, 88),
         Interval(55, 71), Interval(46, 50), Interval(65, 75), Interval(83, 87), Interval(91, 95),
         Interval(1, 1), Interval(56, 70), Interval(79, 95), Interval(26, 32), Interval(79, 101)],
        # Job 19
        [Interval(78, 82), Interval(12, 16), Interval(36, 46), Interval(67, 79), Interval(20, 24),
         Interval(87, 99), Interval(6, 6), Interval(74, 88), Interval(17, 21), Interval(55, 69),
         Interval(59, 65), Interval(82, 88), Interval(23, 27), Interval(65, 75), Interval(10, 10)],
    ],
    'name': 'INT__TAI20_15_06.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai20_15_06_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI20_15_06.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI20_15_06.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI20_15_06_F_15_01_INTERVAL_DATA
