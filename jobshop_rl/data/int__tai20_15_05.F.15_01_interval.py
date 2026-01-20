"""
Problema INT__TAI20_15_05.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI20_15_05_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__tai20_15_05.F.15_01_interval',
    'sequences': [
        [7, 12, 6, 3, 8, 5, 0, 9, 1, 10, 2, 4, 13, 14, 11],
        [8, 3, 12, 5, 6, 9, 1, 14, 4, 2, 11, 0, 10, 13, 7],
        [1, 0, 8, 4, 11, 14, 12, 6, 13, 9, 2, 5, 7, 10, 3],
        [11, 13, 10, 0, 4, 7, 14, 5, 3, 2, 9, 1, 12, 8, 6],
        [14, 6, 2, 10, 11, 5, 12, 9, 3, 1, 13, 4, 0, 7, 8],
        [7, 5, 12, 13, 9, 11, 1, 4, 3, 6, 2, 8, 0, 14, 10],
        [14, 13, 8, 9, 1, 0, 11, 4, 2, 3, 10, 6, 7, 12, 5],
        [7, 13, 4, 11, 0, 10, 5, 2, 6, 1, 8, 12, 3, 9, 14],
        [5, 11, 4, 1, 12, 14, 13, 7, 8, 6, 9, 2, 0, 3, 10],
        [9, 4, 3, 8, 14, 5, 6, 13, 11, 10, 12, 7, 1, 2, 0],
        [11, 13, 6, 5, 10, 3, 12, 8, 2, 4, 9, 1, 0, 14, 7],
        [11, 1, 4, 7, 12, 3, 5, 10, 14, 2, 13, 0, 6, 9, 8],
        [1, 5, 7, 12, 13, 6, 11, 4, 8, 3, 14, 10, 0, 9, 2],
        [4, 10, 7, 8, 3, 13, 0, 14, 11, 12, 9, 6, 1, 2, 5],
        [8, 4, 11, 13, 1, 9, 0, 6, 12, 5, 2, 10, 3, 7, 14],
        [13, 8, 10, 5, 6, 14, 11, 7, 12, 0, 1, 4, 9, 2, 3],
        [5, 8, 13, 11, 9, 14, 10, 1, 12, 6, 4, 7, 3, 0, 2],
        [2, 9, 4, 0, 5, 7, 8, 10, 12, 11, 3, 13, 6, 1, 14],
        [1, 4, 8, 10, 6, 11, 9, 5, 13, 0, 7, 12, 3, 14, 2],
        [1, 10, 13, 12, 5, 4, 6, 14, 11, 7, 8, 2, 9, 0, 3],
    ],
    'durations': [
        # Job 0
        [Interval(15, 15), Interval(88, 90), Interval(42, 56), Interval(91, 99), Interval(37, 43),
         Interval(69, 89), Interval(44, 44), Interval(54, 64), Interval(87, 87), Interval(77, 99),
         Interval(42, 54), Interval(42, 46), Interval(37, 49), Interval(11, 11), Interval(67, 83)],
        # Job 1
        [Interval(6, 6), Interval(41, 51), Interval(18, 18), Interval(4, 4), Interval(52, 60),
         Interval(38, 50), Interval(14, 16), Interval(40, 40), Interval(38, 50), Interval(76, 82),
         Interval(1, 1), Interval(29, 35), Interval(5, 5), Interval(83, 101), Interval(71, 81)],
        # Job 2
        [Interval(73, 83), Interval(41, 49), Interval(52, 70), Interval(48, 50), Interval(24, 28),
         Interval(32, 40), Interval(86, 102), Interval(70, 90), Interval(43, 55), Interval(49, 57),
         Interval(4, 4), Interval(47, 55), Interval(74, 90), Interval(34, 38), Interval(73, 79)],
        # Job 3
        [Interval(51, 65), Interval(29, 39), Interval(62, 78), Interval(17, 21), Interval(82, 88),
         Interval(59, 79), Interval(80, 94), Interval(35, 41), Interval(5, 5), Interval(80, 96),
         Interval(65, 67), Interval(3, 3), Interval(9, 11), Interval(26, 30), Interval(18, 18)],
        # Job 4
        [Interval(78, 78), Interval(7, 7), Interval(77, 89), Interval(74, 76), Interval(36, 42),
         Interval(21, 27), Interval(10, 10), Interval(13, 13), Interval(42, 42), Interval(2, 2),
         Interval(54, 68), Interval(26, 26), Interval(10, 12), Interval(81, 97), Interval(39, 39)],
        # Job 5
        [Interval(70, 90), Interval(78, 98), Interval(13, 13), Interval(82, 102), Interval(10, 12),
         Interval(55, 69), Interval(36, 48), Interval(3, 3), Interval(6, 6), Interval(33, 39),
         Interval(42, 56), Interval(95, 101), Interval(37, 43), Interval(57, 61), Interval(13, 17)],
        # Job 6
        [Interval(79, 87), Interval(12, 12), Interval(48, 48), Interval(1, 1), Interval(66, 86),
         Interval(31, 33), Interval(1, 1), Interval(74, 88), Interval(47, 59), Interval(62, 78),
         Interval(67, 89), Interval(65, 85), Interval(7, 7), Interval(71, 93), Interval(28, 34)],
        # Job 7
        [Interval(74, 76), Interval(13, 13), Interval(9, 9), Interval(10, 12), Interval(49, 49),
         Interval(13, 17), Interval(57, 57), Interval(80, 88), Interval(66, 88), Interval(76, 84),
         Interval(40, 42), Interval(79, 85), Interval(64, 72), Interval(64, 64), Interval(49, 51)],
        # Job 8
        [Interval(34, 44), Interval(58, 70), Interval(83, 93), Interval(8, 10), Interval(97, 97),
         Interval(86, 112), Interval(25, 29), Interval(45, 51), Interval(17, 19), Interval(42, 56),
         Interval(44, 56), Interval(24, 28), Interval(54, 54), Interval(80, 80), Interval(69, 85)],
        # Job 9
        [Interval(58, 74), Interval(77, 97), Interval(25, 29), Interval(43, 51), Interval(61, 75),
         Interval(74, 76), Interval(27, 35), Interval(25, 25), Interval(47, 51), Interval(80, 90),
         Interval(82, 90), Interval(11, 13), Interval(24, 28), Interval(70, 94), Interval(67, 89)],
        # Job 10
        [Interval(84, 102), Interval(86, 88), Interval(72, 76), Interval(23, 29), Interval(59, 61),
         Interval(74, 78), Interval(3, 3), Interval(91, 105), Interval(64, 80), Interval(45, 59),
         Interval(71, 75), Interval(71, 79), Interval(26, 30), Interval(1, 1), Interval(49, 53)],
        # Job 11
        [Interval(76, 82), Interval(12, 14), Interval(14, 14), Interval(26, 28), Interval(12, 16),
         Interval(5, 5), Interval(50, 66), Interval(28, 36), Interval(37, 39), Interval(59, 75),
         Interval(70, 70), Interval(84, 88), Interval(25, 31), Interval(88, 100), Interval(31, 35)],
        # Job 12
        [Interval(78, 88), Interval(58, 76), Interval(17, 19), Interval(17, 23), Interval(4, 4),
         Interval(78, 90), Interval(21, 23), Interval(7, 9), Interval(86, 96), Interval(85, 93),
         Interval(23, 27), Interval(8, 8), Interval(63, 75), Interval(77, 93), Interval(46, 46)],
        # Job 13
        [Interval(58, 70), Interval(16, 20), Interval(12, 12), Interval(41, 45), Interval(68, 88),
         Interval(57, 73), Interval(20, 20), Interval(48, 58), Interval(28, 36), Interval(46, 52),
         Interval(25, 25), Interval(10, 10), Interval(40, 46), Interval(26, 34), Interval(3, 3)],
        # Job 14
        [Interval(90, 108), Interval(26, 32), Interval(49, 51), Interval(89, 109), Interval(46, 60),
         Interval(58, 72), Interval(22, 24), Interval(47, 51), Interval(83, 99), Interval(1, 1),
         Interval(83, 89), Interval(6, 8), Interval(62, 74), Interval(62, 80), Interval(86, 92)],
        # Job 15
        [Interval(13, 13), Interval(18, 20), Interval(29, 33), Interval(91, 97), Interval(67, 89),
         Interval(37, 49), Interval(15, 17), Interval(48, 64), Interval(68, 84), Interval(1, 1),
         Interval(11, 11), Interval(22, 26), Interval(13, 13), Interval(55, 69), Interval(47, 63)],
        # Job 16
        [Interval(39, 47), Interval(23, 25), Interval(83, 87), Interval(17, 23), Interval(6, 6),
         Interval(42, 46), Interval(45, 53), Interval(36, 46), Interval(58, 76), Interval(46, 48),
         Interval(24, 26), Interval(83, 89), Interval(6, 6), Interval(6, 6), Interval(28, 32)],
        # Job 17
        [Interval(64, 72), Interval(82, 102), Interval(14, 16), Interval(71, 89), Interval(25, 33),
         Interval(70, 74), Interval(19, 25), Interval(37, 45), Interval(48, 50), Interval(36, 36),
         Interval(91, 103), Interval(78, 82), Interval(20, 26), Interval(72, 82), Interval(4, 4)],
        # Job 18
        [Interval(48, 54), Interval(29, 39), Interval(9, 11), Interval(94, 98), Interval(73, 75),
         Interval(69, 91), Interval(64, 66), Interval(65, 85), Interval(14, 14), Interval(72, 94),
         Interval(13, 13), Interval(69, 87), Interval(58, 64), Interval(40, 46), Interval(57, 59)],
        # Job 19
        [Interval(67, 71), Interval(50, 62), Interval(14, 16), Interval(78, 100), Interval(19, 25),
         Interval(21, 21), Interval(79, 99), Interval(14, 18), Interval(54, 64), Interval(74, 92),
         Interval(19, 21), Interval(31, 35), Interval(10, 12), Interval(59, 75), Interval(86, 94)],
    ],
    'name': 'INT__TAI20_15_05.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai20_15_05_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI20_15_05.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI20_15_05.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI20_15_05_F_15_01_INTERVAL_DATA
