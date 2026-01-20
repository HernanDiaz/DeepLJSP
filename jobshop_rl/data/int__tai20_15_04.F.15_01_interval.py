"""
Problema INT__TAI20_15_04.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI20_15_04_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__tai20_15_04.F.15_01_interval',
    'sequences': [
        [8, 13, 3, 7, 10, 6, 14, 12, 9, 2, 0, 4, 5, 11, 1],
        [11, 4, 6, 3, 8, 9, 12, 5, 13, 0, 7, 10, 14, 2, 1],
        [14, 9, 4, 0, 2, 13, 6, 7, 11, 1, 3, 5, 10, 12, 8],
        [0, 12, 10, 1, 11, 14, 8, 5, 9, 13, 2, 6, 3, 4, 7],
        [2, 6, 4, 13, 8, 12, 3, 10, 9, 11, 0, 7, 1, 5, 14],
        [1, 4, 13, 7, 12, 8, 3, 0, 14, 5, 10, 11, 9, 6, 2],
        [6, 12, 3, 11, 0, 1, 7, 13, 4, 8, 5, 9, 14, 10, 2],
        [5, 7, 14, 11, 4, 3, 10, 0, 1, 6, 13, 12, 8, 9, 2],
        [3, 2, 6, 4, 11, 10, 0, 8, 14, 7, 13, 5, 1, 9, 12],
        [3, 11, 14, 10, 2, 4, 1, 13, 6, 9, 5, 8, 12, 7, 0],
        [9, 10, 6, 7, 4, 12, 5, 14, 13, 1, 8, 0, 2, 3, 11],
        [7, 5, 11, 14, 8, 0, 13, 12, 2, 9, 10, 1, 4, 3, 6],
        [11, 0, 6, 12, 5, 10, 13, 3, 4, 1, 9, 14, 2, 8, 7],
        [2, 9, 4, 6, 3, 7, 13, 5, 12, 10, 1, 11, 8, 14, 0],
        [6, 14, 5, 8, 13, 4, 1, 3, 0, 7, 12, 2, 10, 11, 9],
        [10, 14, 8, 7, 6, 5, 1, 13, 11, 2, 3, 9, 12, 0, 4],
        [5, 11, 1, 4, 7, 6, 14, 13, 8, 12, 3, 2, 0, 9, 10],
        [4, 14, 2, 6, 0, 11, 7, 13, 9, 1, 5, 3, 8, 10, 12],
        [7, 14, 10, 1, 5, 9, 2, 4, 0, 11, 13, 3, 6, 12, 8],
        [11, 13, 7, 8, 6, 0, 5, 4, 10, 1, 3, 2, 9, 12, 14],
    ],
    'durations': [
        # Job 0
        [Interval(56, 56), Interval(25, 25), Interval(15, 19), Interval(60, 66), Interval(8, 10),
         Interval(26, 34), Interval(75, 75), Interval(20, 24), Interval(42, 42), Interval(73, 93),
         Interval(60, 78), Interval(85, 95), Interval(75, 101), Interval(20, 20), Interval(27, 33)],
        # Job 1
        [Interval(35, 43), Interval(20, 20), Interval(32, 38), Interval(68, 90), Interval(33, 37),
         Interval(65, 67), Interval(13, 17), Interval(54, 58), Interval(53, 67), Interval(65, 79),
         Interval(49, 55), Interval(13, 15), Interval(2, 2), Interval(14, 18), Interval(51, 67)],
        # Job 2
        [Interval(5, 5), Interval(30, 32), Interval(50, 60), Interval(63, 77), Interval(45, 53),
         Interval(62, 78), Interval(81, 103), Interval(37, 43), Interval(12, 14), Interval(13, 15),
         Interval(46, 52), Interval(29, 31), Interval(44, 56), Interval(66, 88), Interval(72, 90)],
        # Job 3
        [Interval(55, 73), Interval(61, 65), Interval(18, 24), Interval(19, 23), Interval(27, 31),
         Interval(9, 11), Interval(25, 25), Interval(55, 65), Interval(85, 101), Interval(24, 24),
         Interval(48, 48), Interval(49, 55), Interval(8, 8), Interval(30, 30), Interval(34, 40)],
        # Job 4
        [Interval(4, 4), Interval(28, 36), Interval(10, 10), Interval(73, 81), Interval(45, 45),
         Interval(33, 41), Interval(89, 89), Interval(52, 68), Interval(54, 64), Interval(42, 42),
         Interval(42, 54), Interval(27, 33), Interval(22, 22), Interval(21, 25), Interval(13, 17)],
        # Job 5
        [Interval(12, 16), Interval(9, 11), Interval(63, 73), Interval(82, 108), Interval(41, 43),
         Interval(27, 31), Interval(43, 45), Interval(20, 26), Interval(58, 64), Interval(56, 58),
         Interval(45, 45), Interval(86, 110), Interval(29, 31), Interval(25, 29), Interval(12, 14)],
        # Job 6
        [Interval(44, 56), Interval(47, 63), Interval(20, 26), Interval(24, 26), Interval(45, 57),
         Interval(49, 61), Interval(9, 9), Interval(87, 87), Interval(21, 21), Interval(41, 55),
         Interval(55, 55), Interval(20, 24), Interval(47, 47), Interval(48, 52), Interval(74, 98)],
        # Job 7
        [Interval(11, 11), Interval(42, 44), Interval(26, 26), Interval(30, 32), Interval(18, 18),
         Interval(58, 60), Interval(74, 94), Interval(30, 36), Interval(69, 77), Interval(18, 22),
         Interval(34, 34), Interval(80, 104), Interval(60, 70), Interval(81, 93), Interval(34, 40)],
        # Job 8
        [Interval(8, 10), Interval(17, 23), Interval(10, 12), Interval(21, 21), Interval(11, 11),
         Interval(86, 106), Interval(81, 107), Interval(81, 101), Interval(84, 100), Interval(88, 106),
         Interval(25, 31), Interval(54, 56), Interval(76, 102), Interval(34, 34), Interval(58, 64)],
        # Job 9
        [Interval(10, 10), Interval(56, 60), Interval(74, 98), Interval(78, 94), Interval(74, 100),
         Interval(16, 20), Interval(67, 81), Interval(63, 65), Interval(12, 12), Interval(19, 25),
         Interval(79, 81), Interval(5, 5), Interval(92, 98), Interval(6, 6), Interval(33, 37)],
        # Job 10
        [Interval(41, 53), Interval(58, 78), Interval(58, 62), Interval(19, 21), Interval(13, 15),
         Interval(6, 6), Interval(19, 21), Interval(6, 6), Interval(44, 48), Interval(72, 86),
         Interval(32, 32), Interval(79, 85), Interval(6, 8), Interval(63, 85), Interval(47, 61)],
        # Job 11
        [Interval(19, 21), Interval(88, 110), Interval(55, 55), Interval(76, 80), Interval(31, 39),
         Interval(25, 27), Interval(21, 25), Interval(81, 93), Interval(76, 96), Interval(24, 26),
         Interval(87, 109), Interval(1, 1), Interval(15, 17), Interval(31, 35), Interval(46, 54)],
        # Job 12
        [Interval(33, 37), Interval(32, 36), Interval(59, 73), Interval(44, 50), Interval(43, 53),
         Interval(47, 57), Interval(33, 33), Interval(70, 84), Interval(34, 42), Interval(61, 69),
         Interval(55, 61), Interval(62, 80), Interval(12, 16), Interval(84, 86), Interval(12, 14)],
        # Job 13
        [Interval(74, 96), Interval(81, 91), Interval(15, 15), Interval(67, 69), Interval(30, 34),
         Interval(72, 94), Interval(72, 88), Interval(71, 91), Interval(10, 10), Interval(11, 13),
         Interval(27, 35), Interval(34, 42), Interval(75, 81), Interval(42, 46), Interval(17, 19)],
        # Job 14
        [Interval(57, 63), Interval(51, 65), Interval(15, 17), Interval(21, 27), Interval(55, 59),
         Interval(8, 8), Interval(39, 43), Interval(36, 42), Interval(27, 29), Interval(48, 64),
         Interval(32, 42), Interval(31, 37), Interval(34, 44), Interval(62, 76), Interval(52, 52)],
        # Job 15
        [Interval(68, 84), Interval(83, 91), Interval(81, 101), Interval(12, 14), Interval(4, 4),
         Interval(29, 35), Interval(54, 62), Interval(61, 63), Interval(72, 94), Interval(46, 50),
         Interval(37, 45), Interval(32, 40), Interval(59, 77), Interval(27, 29), Interval(12, 12)],
        # Job 16
        [Interval(1, 1), Interval(65, 69), Interval(92, 104), Interval(39, 43), Interval(75, 93),
         Interval(31, 37), Interval(77, 95), Interval(64, 86), Interval(91, 95), Interval(72, 94),
         Interval(60, 72), Interval(91, 95), Interval(47, 47), Interval(55, 61), Interval(63, 65)],
        # Job 17
        [Interval(53, 69), Interval(46, 52), Interval(33, 37), Interval(80, 104), Interval(73, 95),
         Interval(56, 58), Interval(31, 31), Interval(43, 57), Interval(53, 53), Interval(10, 12),
         Interval(71, 77), Interval(7, 9), Interval(13, 15), Interval(11, 13), Interval(48, 52)],
        # Job 18
        [Interval(18, 20), Interval(87, 91), Interval(65, 69), Interval(9, 11), Interval(68, 82),
         Interval(43, 55), Interval(65, 85), Interval(65, 67), Interval(33, 41), Interval(68, 86),
         Interval(85, 103), Interval(53, 67), Interval(36, 40), Interval(48, 56), Interval(53, 69)],
        # Job 19
        [Interval(26, 32), Interval(70, 76), Interval(60, 64), Interval(18, 20), Interval(92, 106),
         Interval(92, 98), Interval(2, 2), Interval(34, 44), Interval(65, 75), Interval(81, 99),
         Interval(10, 10), Interval(60, 60), Interval(19, 23), Interval(35, 45), Interval(15, 19)],
    ],
    'name': 'INT__TAI20_15_04.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai20_15_04_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI20_15_04.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI20_15_04.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI20_15_04_F_15_01_INTERVAL_DATA
