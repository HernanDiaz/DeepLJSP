"""
Problema INT__TAI20_15_08.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI20_15_08_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__tai20_15_08.F.15_01_interval',
    'sequences': [
        [1, 6, 10, 14, 7, 5, 13, 4, 3, 8, 0, 9, 12, 2, 11],
        [0, 9, 3, 2, 8, 5, 14, 12, 6, 11, 10, 7, 4, 1, 13],
        [1, 6, 2, 11, 3, 4, 10, 9, 12, 8, 7, 5, 0, 14, 13],
        [12, 14, 8, 9, 5, 3, 0, 1, 13, 10, 6, 11, 4, 7, 2],
        [14, 10, 8, 6, 0, 4, 5, 9, 11, 3, 7, 13, 1, 12, 2],
        [8, 2, 9, 12, 3, 0, 13, 14, 5, 11, 7, 1, 4, 6, 10],
        [5, 3, 8, 7, 0, 12, 4, 2, 14, 6, 10, 11, 9, 1, 13],
        [5, 8, 12, 1, 7, 4, 2, 9, 6, 14, 13, 0, 3, 10, 11],
        [14, 8, 7, 12, 6, 10, 0, 1, 11, 9, 5, 4, 2, 3, 13],
        [0, 14, 2, 5, 10, 4, 9, 7, 11, 6, 3, 13, 1, 12, 8],
        [1, 3, 11, 0, 9, 5, 2, 14, 6, 7, 8, 12, 13, 10, 4],
        [12, 8, 3, 10, 2, 0, 7, 9, 14, 5, 4, 1, 11, 13, 6],
        [1, 6, 14, 2, 11, 4, 8, 3, 13, 10, 0, 9, 12, 7, 5],
        [1, 4, 9, 3, 11, 14, 8, 0, 13, 10, 2, 6, 5, 7, 12],
        [2, 7, 3, 1, 8, 4, 14, 11, 12, 5, 10, 0, 13, 6, 9],
        [10, 2, 4, 6, 1, 9, 7, 12, 3, 11, 13, 14, 5, 8, 0],
        [2, 0, 5, 14, 4, 6, 11, 10, 8, 7, 13, 1, 3, 9, 12],
        [3, 0, 11, 14, 5, 10, 4, 13, 9, 6, 8, 1, 7, 2, 12],
        [1, 0, 7, 5, 9, 8, 14, 13, 2, 10, 4, 3, 12, 11, 6],
        [1, 12, 14, 4, 7, 9, 8, 3, 6, 0, 10, 2, 11, 13, 5],
    ],
    'durations': [
        # Job 0
        [Interval(69, 71), Interval(6, 6), Interval(29, 29), Interval(47, 63), Interval(14, 14),
         Interval(31, 35), Interval(58, 74), Interval(14, 14), Interval(6, 8), Interval(57, 57),
         Interval(48, 62), Interval(16, 20), Interval(59, 65), Interval(40, 52), Interval(92, 92)],
        # Job 1
        [Interval(27, 33), Interval(48, 58), Interval(19, 19), Interval(1, 1), Interval(90, 106),
         Interval(69, 93), Interval(59, 67), Interval(61, 63), Interval(9, 11), Interval(15, 15),
         Interval(65, 81), Interval(68, 82), Interval(75, 85), Interval(78, 90), Interval(87, 107)],
        # Job 2
        [Interval(36, 48), Interval(59, 63), Interval(6, 6), Interval(54, 66), Interval(22, 26),
         Interval(64, 76), Interval(69, 87), Interval(10, 12), Interval(32, 38), Interval(35, 41),
         Interval(55, 67), Interval(84, 96), Interval(71, 77), Interval(1, 1), Interval(53, 67)],
        # Job 3
        [Interval(65, 87), Interval(75, 93), Interval(62, 82), Interval(17, 17), Interval(23, 31),
         Interval(79, 93), Interval(78, 90), Interval(65, 77), Interval(89, 91), Interval(25, 29),
         Interval(12, 14), Interval(98, 98), Interval(3, 3), Interval(57, 57), Interval(62, 70)],
        # Job 4
        [Interval(36, 40), Interval(57, 59), Interval(74, 86), Interval(21, 27), Interval(48, 52),
         Interval(72, 80), Interval(6, 6), Interval(12, 12), Interval(24, 28), Interval(14, 14),
         Interval(30, 40), Interval(35, 41), Interval(55, 55), Interval(29, 37), Interval(37, 47)],
        # Job 5
        [Interval(75, 79), Interval(77, 97), Interval(51, 67), Interval(17, 21), Interval(72, 96),
         Interval(79, 91), Interval(54, 72), Interval(50, 52), Interval(17, 19), Interval(28, 30),
         Interval(2, 2), Interval(12, 14), Interval(1, 1), Interval(24, 26), Interval(53, 55)],
        # Job 6
        [Interval(19, 19), Interval(72, 94), Interval(69, 73), Interval(20, 24), Interval(4, 4),
         Interval(59, 77), Interval(60, 76), Interval(75, 101), Interval(69, 91), Interval(51, 59),
         Interval(10, 12), Interval(17, 21), Interval(39, 39), Interval(68, 68), Interval(37, 37)],
        # Job 7
        [Interval(33, 43), Interval(98, 98), Interval(10, 12), Interval(3, 3), Interval(33, 33),
         Interval(41, 45), Interval(17, 21), Interval(86, 94), Interval(55, 57), Interval(80, 86),
         Interval(72, 80), Interval(97, 97), Interval(2, 2), Interval(74, 78), Interval(1, 1)],
        # Job 8
        [Interval(22, 28), Interval(59, 71), Interval(83, 93), Interval(51, 61), Interval(75, 75),
         Interval(41, 55), Interval(37, 43), Interval(18, 20), Interval(36, 42), Interval(34, 46),
         Interval(38, 48), Interval(89, 109), Interval(23, 23), Interval(74, 74), Interval(35, 43)],
        # Job 9
        [Interval(84, 110), Interval(59, 73), Interval(49, 59), Interval(26, 32), Interval(21, 25),
         Interval(9, 9), Interval(63, 85), Interval(46, 46), Interval(81, 89), Interval(92, 104),
         Interval(71, 77), Interval(11, 13), Interval(65, 77), Interval(56, 74), Interval(22, 28)],
        # Job 10
        [Interval(3, 3), Interval(36, 44), Interval(80, 82), Interval(72, 76), Interval(58, 76),
         Interval(92, 94), Interval(74, 78), Interval(15, 17), Interval(11, 13), Interval(57, 77),
         Interval(51, 53), Interval(19, 21), Interval(23, 25), Interval(68, 74), Interval(86, 94)],
        # Job 11
        [Interval(12, 14), Interval(59, 59), Interval(92, 98), Interval(71, 87), Interval(40, 52),
         Interval(14, 18), Interval(64, 70), Interval(59, 75), Interval(64, 64), Interval(83, 87),
         Interval(76, 94), Interval(25, 29), Interval(24, 28), Interval(52, 60), Interval(1, 1)],
        # Job 12
        [Interval(56, 72), Interval(1, 1), Interval(27, 31), Interval(59, 73), Interval(30, 34),
         Interval(33, 37), Interval(7, 9), Interval(25, 27), Interval(89, 99), Interval(84, 104),
         Interval(58, 66), Interval(38, 46), Interval(54, 66), Interval(56, 56), Interval(6, 8)],
        # Job 13
        [Interval(3, 3), Interval(6, 8), Interval(38, 42), Interval(89, 97), Interval(47, 63),
         Interval(65, 85), Interval(25, 25), Interval(19, 23), Interval(26, 34), Interval(77, 87),
         Interval(1, 1), Interval(57, 59), Interval(52, 54), Interval(81, 95), Interval(17, 21)],
        # Job 14
        [Interval(60, 72), Interval(78, 98), Interval(47, 49), Interval(69, 85), Interval(33, 43),
         Interval(70, 86), Interval(16, 16), Interval(39, 43), Interval(85, 101), Interval(37, 39),
         Interval(22, 28), Interval(47, 55), Interval(12, 16), Interval(95, 101), Interval(59, 63)],
        # Job 15
        [Interval(32, 34), Interval(21, 25), Interval(7, 7), Interval(51, 69), Interval(64, 84),
         Interval(49, 59), Interval(2, 2), Interval(19, 25), Interval(29, 35), Interval(15, 15),
         Interval(71, 87), Interval(79, 87), Interval(61, 77), Interval(35, 47), Interval(17, 21)],
        # Job 16
        [Interval(57, 65), Interval(26, 26), Interval(58, 74), Interval(81, 89), Interval(31, 37),
         Interval(13, 17), Interval(52, 66), Interval(73, 77), Interval(3, 3), Interval(75, 85),
         Interval(38, 40), Interval(65, 73), Interval(6, 6), Interval(69, 77), Interval(58, 72)],
        # Job 17
        [Interval(89, 103), Interval(6, 6), Interval(47, 57), Interval(19, 25), Interval(34, 36),
         Interval(69, 89), Interval(15, 17), Interval(70, 74), Interval(29, 29), Interval(25, 27),
         Interval(51, 53), Interval(51, 65), Interval(54, 60), Interval(29, 33), Interval(63, 85)],
        # Job 18
        [Interval(36, 48), Interval(78, 80), Interval(83, 85), Interval(22, 28), Interval(69, 71),
         Interval(78, 102), Interval(8, 8), Interval(52, 68), Interval(77, 85), Interval(77, 99),
         Interval(11, 11), Interval(66, 76), Interval(59, 63), Interval(48, 50), Interval(72, 90)],
        # Job 19
        [Interval(47, 57), Interval(3, 3), Interval(50, 64), Interval(58, 74), Interval(86, 90),
         Interval(37, 47), Interval(20, 26), Interval(66, 78), Interval(86, 108), Interval(85, 97),
         Interval(46, 54), Interval(38, 48), Interval(73, 91), Interval(59, 65), Interval(26, 28)],
    ],
    'name': 'INT__TAI20_15_08.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai20_15_08_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI20_15_08.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI20_15_08.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI20_15_08_F_15_01_INTERVAL_DATA
