"""
Problema INT__TAI20_15_10.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI20_15_10_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__tai20_15_10.F.15_01_interval',
    'sequences': [
        [7, 0, 12, 4, 1, 9, 2, 11, 10, 14, 5, 6, 13, 3, 8],
        [4, 8, 7, 3, 9, 13, 12, 0, 11, 10, 1, 6, 5, 14, 2],
        [1, 4, 7, 13, 3, 8, 10, 5, 12, 14, 9, 6, 2, 0, 11],
        [5, 11, 9, 12, 7, 1, 6, 13, 8, 2, 0, 14, 3, 4, 10],
        [4, 11, 12, 1, 0, 9, 6, 13, 2, 14, 5, 10, 3, 8, 7],
        [2, 6, 3, 8, 14, 0, 4, 10, 11, 1, 7, 13, 12, 5, 9],
        [4, 14, 5, 10, 8, 7, 6, 1, 0, 12, 9, 13, 11, 3, 2],
        [7, 10, 11, 14, 3, 2, 4, 5, 1, 12, 9, 6, 13, 0, 8],
        [14, 11, 0, 13, 3, 2, 1, 8, 5, 7, 4, 12, 6, 10, 9],
        [0, 5, 12, 1, 13, 10, 9, 4, 2, 8, 14, 11, 7, 6, 3],
        [4, 3, 8, 12, 9, 11, 2, 14, 5, 7, 13, 6, 10, 1, 0],
        [9, 6, 1, 0, 14, 7, 13, 12, 2, 11, 5, 8, 10, 3, 4],
        [4, 3, 0, 14, 13, 9, 7, 2, 11, 8, 10, 1, 6, 12, 5],
        [12, 10, 3, 6, 4, 5, 0, 7, 2, 8, 13, 11, 14, 9, 1],
        [14, 7, 5, 8, 11, 0, 2, 13, 12, 4, 6, 1, 10, 9, 3],
        [6, 14, 12, 2, 7, 5, 8, 13, 11, 9, 0, 3, 4, 1, 10],
        [9, 5, 14, 10, 12, 1, 4, 13, 0, 11, 3, 2, 7, 6, 8],
        [9, 12, 4, 14, 11, 8, 0, 7, 5, 3, 1, 10, 6, 13, 2],
        [12, 2, 3, 14, 5, 1, 6, 11, 13, 9, 7, 10, 8, 0, 4],
        [3, 12, 10, 5, 14, 0, 9, 8, 13, 6, 11, 1, 7, 2, 4],
    ],
    'durations': [
        # Job 0
        [Interval(83, 85), Interval(58, 58), Interval(61, 81), Interval(25, 27), Interval(91, 105),
         Interval(31, 41), Interval(12, 12), Interval(28, 32), Interval(87, 87), Interval(83, 107),
         Interval(40, 50), Interval(27, 29), Interval(63, 83), Interval(73, 73), Interval(41, 49)],
        # Job 1
        [Interval(26, 32), Interval(22, 22), Interval(43, 51), Interval(64, 86), Interval(87, 101),
         Interval(15, 15), Interval(4, 4), Interval(70, 94), Interval(14, 14), Interval(31, 39),
         Interval(72, 86), Interval(32, 36), Interval(53, 61), Interval(21, 25), Interval(48, 64)],
        # Job 2
        [Interval(71, 75), Interval(33, 39), Interval(43, 53), Interval(24, 28), Interval(43, 55),
         Interval(52, 68), Interval(14, 16), Interval(61, 71), Interval(81, 99), Interval(37, 41),
         Interval(8, 8), Interval(65, 83), Interval(54, 72), Interval(83, 105), Interval(78, 104)],
        # Job 3
        [Interval(1, 1), Interval(34, 36), Interval(20, 26), Interval(86, 100), Interval(69, 81),
         Interval(46, 54), Interval(40, 40), Interval(55, 65), Interval(37, 45), Interval(7, 7),
         Interval(57, 57), Interval(68, 76), Interval(37, 43), Interval(74, 76), Interval(6, 8)],
        # Job 4
        [Interval(12, 14), Interval(14, 16), Interval(16, 18), Interval(14, 14), Interval(59, 75),
         Interval(94, 94), Interval(16, 20), Interval(47, 57), Interval(53, 53), Interval(14, 18),
         Interval(30, 36), Interval(60, 62), Interval(42, 52), Interval(56, 74), Interval(35, 43)],
        # Job 5
        [Interval(46, 62), Interval(74, 86), Interval(74, 100), Interval(35, 37), Interval(50, 58),
         Interval(70, 74), Interval(15, 19), Interval(42, 46), Interval(36, 38), Interval(88, 88),
         Interval(67, 87), Interval(82, 86), Interval(16, 18), Interval(71, 93), Interval(80, 100)],
        # Job 6
        [Interval(4, 4), Interval(53, 71), Interval(29, 37), Interval(58, 66), Interval(75, 97),
         Interval(27, 33), Interval(39, 39), Interval(67, 67), Interval(42, 42), Interval(27, 35),
         Interval(83, 83), Interval(35, 43), Interval(67, 67), Interval(64, 70), Interval(27, 35)],
        # Job 7
        [Interval(28, 30), Interval(29, 29), Interval(67, 71), Interval(25, 27), Interval(55, 55),
         Interval(45, 47), Interval(47, 59), Interval(59, 71), Interval(92, 102), Interval(22, 26),
         Interval(69, 69), Interval(19, 25), Interval(16, 18), Interval(37, 41), Interval(12, 14)],
        # Job 8
        [Interval(11, 13), Interval(64, 82), Interval(32, 40), Interval(70, 70), Interval(12, 12),
         Interval(71, 89), Interval(86, 112), Interval(63, 77), Interval(47, 55), Interval(13, 15),
         Interval(64, 78), Interval(28, 28), Interval(30, 40), Interval(58, 58), Interval(34, 36)],
        # Job 9
        [Interval(57, 65), Interval(47, 51), Interval(63, 85), Interval(82, 98), Interval(51, 69),
         Interval(75, 101), Interval(3, 3), Interval(54, 66), Interval(58, 60), Interval(91, 97),
         Interval(80, 102), Interval(34, 34), Interval(26, 26), Interval(4, 4), Interval(25, 27)],
        # Job 10
        [Interval(79, 99), Interval(77, 103), Interval(92, 98), Interval(31, 33), Interval(17, 19),
         Interval(70, 76), Interval(9, 9), Interval(18, 20), Interval(96, 98), Interval(56, 60),
         Interval(32, 40), Interval(53, 71), Interval(12, 14), Interval(16, 16), Interval(1, 1)],
        # Job 11
        [Interval(63, 79), Interval(47, 47), Interval(92, 98), Interval(6, 8), Interval(59, 67),
         Interval(45, 53), Interval(23, 25), Interval(41, 51), Interval(68, 76), Interval(65, 81),
         Interval(18, 20), Interval(90, 102), Interval(37, 45), Interval(14, 16), Interval(77, 85)],
        # Job 12
        [Interval(40, 50), Interval(9, 9), Interval(88, 106), Interval(56, 68), Interval(77, 77),
         Interval(71, 85), Interval(62, 78), Interval(18, 20), Interval(82, 90), Interval(13, 17),
         Interval(20, 26), Interval(46, 46), Interval(29, 35), Interval(6, 6), Interval(61, 79)],
        # Job 13
        [Interval(70, 78), Interval(45, 47), Interval(96, 100), Interval(1, 1), Interval(49, 57),
         Interval(51, 67), Interval(78, 94), Interval(87, 109), Interval(74, 78), Interval(11, 13),
         Interval(79, 103), Interval(87, 109), Interval(94, 102), Interval(11, 11), Interval(25, 29)],
        # Job 14
        [Interval(70, 76), Interval(62, 78), Interval(13, 15), Interval(28, 36), Interval(19, 19),
         Interval(56, 58), Interval(16, 18), Interval(88, 104), Interval(54, 58), Interval(63, 83),
         Interval(28, 36), Interval(6, 8), Interval(69, 89), Interval(9, 11), Interval(90, 92)],
        # Job 15
        [Interval(35, 43), Interval(83, 91), Interval(10, 12), Interval(69, 93), Interval(6, 8),
         Interval(74, 84), Interval(24, 24), Interval(8, 10), Interval(56, 60), Interval(38, 46),
         Interval(59, 75), Interval(23, 31), Interval(20, 20), Interval(18, 20), Interval(65, 69)],
        # Job 16
        [Interval(71, 81), Interval(84, 94), Interval(57, 71), Interval(13, 15), Interval(10, 12),
         Interval(12, 16), Interval(97, 101), Interval(74, 96), Interval(74, 88), Interval(3, 3),
         Interval(45, 47), Interval(47, 47), Interval(37, 43), Interval(79, 83), Interval(23, 31)],
        # Job 17
        [Interval(52, 58), Interval(66, 76), Interval(5, 5), Interval(71, 95), Interval(14, 18),
         Interval(4, 4), Interval(20, 20), Interval(15, 15), Interval(51, 69), Interval(8, 8),
         Interval(81, 105), Interval(32, 34), Interval(55, 71), Interval(67, 75), Interval(25, 33)],
        # Job 18
        [Interval(87, 97), Interval(23, 27), Interval(8, 8), Interval(84, 88), Interval(20, 24),
         Interval(72, 86), Interval(20, 26), Interval(84, 108), Interval(24, 24), Interval(84, 104),
         Interval(85, 109), Interval(16, 18), Interval(43, 53), Interval(62, 72), Interval(43, 51)],
        # Job 19
        [Interval(5, 5), Interval(67, 87), Interval(65, 83), Interval(56, 62), Interval(13, 13),
         Interval(53, 61), Interval(58, 66), Interval(36, 38), Interval(46, 62), Interval(64, 74),
         Interval(71, 89), Interval(34, 36), Interval(87, 89), Interval(42, 52), Interval(87, 109)],
    ],
    'name': 'INT__TAI20_15_10.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai20_15_10_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI20_15_10.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI20_15_10.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI20_15_10_F_15_01_INTERVAL_DATA
