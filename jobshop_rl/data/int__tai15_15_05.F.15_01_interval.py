"""
Problema INT__TAI15_15_05.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI15_15_05_F_15_01_INTERVAL_DATA = {
    'num_jobs': 15,
    'num_machines': 15,
    'problem_id': 'int__tai15_15_05.F.15_01_interval',
    'sequences': [
        [12, 1, 4, 9, 13, 0, 11, 8, 3, 5, 6, 14, 10, 2, 7],
        [5, 1, 14, 10, 13, 9, 6, 12, 8, 2, 7, 0, 3, 4, 11],
        [6, 3, 10, 7, 13, 4, 5, 9, 8, 2, 0, 1, 11, 14, 12],
        [10, 7, 5, 0, 9, 13, 2, 8, 1, 14, 11, 3, 12, 6, 4],
        [6, 12, 14, 1, 7, 5, 11, 0, 2, 3, 8, 13, 4, 9, 10],
        [4, 7, 6, 0, 8, 13, 12, 14, 3, 2, 5, 9, 10, 1, 11],
        [10, 11, 6, 9, 0, 2, 1, 8, 12, 7, 5, 3, 13, 14, 4],
        [3, 10, 5, 6, 8, 4, 0, 14, 2, 7, 9, 11, 12, 1, 13],
        [1, 2, 6, 7, 10, 12, 14, 8, 0, 3, 13, 5, 4, 9, 11],
        [12, 7, 6, 14, 3, 4, 0, 13, 10, 8, 11, 9, 5, 2, 1],
        [4, 3, 8, 14, 2, 13, 5, 6, 10, 12, 7, 11, 1, 9, 0],
        [6, 12, 7, 5, 2, 4, 13, 11, 8, 0, 10, 3, 1, 9, 14],
        [12, 13, 8, 7, 1, 6, 0, 5, 9, 10, 4, 2, 14, 3, 11],
        [12, 1, 4, 8, 6, 10, 7, 3, 0, 5, 13, 2, 9, 14, 11],
        [7, 5, 0, 10, 2, 3, 9, 6, 11, 8, 1, 4, 14, 12, 13],
    ],
    'durations': [
        # Job 0
        [Interval(40, 40), Interval(95, 97), Interval(51, 67), Interval(91, 99), Interval(70, 82),
         Interval(65, 85), Interval(23, 23), Interval(60, 70), Interval(65, 65), Interval(14, 18),
         Interval(62, 80), Interval(49, 55), Interval(72, 96), Interval(99, 99), Interval(22, 26)],
        # Job 1
        [Interval(2, 2), Interval(78, 98), Interval(96, 102), Interval(48, 56), Interval(58, 78),
         Interval(13, 13), Interval(38, 38), Interval(30, 40), Interval(55, 59), Interval(33, 41),
         Interval(84, 102), Interval(36, 40), Interval(63, 73), Interval(84, 104), Interval(61, 81)],
        # Job 2
        [Interval(84, 90), Interval(42, 50), Interval(12, 16), Interval(79, 95), Interval(26, 34),
         Interval(70, 88), Interval(57, 67), Interval(34, 40), Interval(49, 59), Interval(1, 1),
         Interval(91, 103), Interval(16, 16), Interval(2, 2), Interval(45, 57), Interval(82, 110)],
        # Job 3
        [Interval(17, 21), Interval(13, 17), Interval(41, 43), Interval(7, 9), Interval(66, 78),
         Interval(14, 16), Interval(69, 83), Interval(25, 25), Interval(72, 84), Interval(77, 91),
         Interval(62, 62), Interval(70, 70), Interval(76, 86), Interval(15, 17), Interval(95, 99)],
        # Job 4
        [Interval(63, 73), Interval(61, 81), Interval(3, 3), Interval(64, 72), Interval(86, 96),
         Interval(37, 37), Interval(65, 81), Interval(21, 21), Interval(74, 96), Interval(72, 86),
         Interval(51, 51), Interval(44, 56), Interval(18, 24), Interval(30, 30), Interval(57, 71)],
        # Job 5
        [Interval(12, 16), Interval(1, 1), Interval(26, 32), Interval(62, 82), Interval(6, 6),
         Interval(29, 33), Interval(85, 111), Interval(49, 51), Interval(77, 89), Interval(2, 2),
         Interval(83, 89), Interval(29, 37), Interval(32, 34), Interval(96, 100), Interval(59, 59)],
        # Job 6
        [Interval(18, 24), Interval(78, 82), Interval(91, 107), Interval(61, 79), Interval(70, 90),
         Interval(61, 81), Interval(40, 54), Interval(89, 103), Interval(49, 63), Interval(70, 86),
         Interval(53, 53), Interval(10, 10), Interval(92, 92), Interval(1, 1), Interval(29, 37)],
        # Job 7
        [Interval(29, 29), Interval(76, 94), Interval(89, 89), Interval(10, 10), Interval(26, 34),
         Interval(36, 40), Interval(37, 39), Interval(47, 49), Interval(15, 17), Interval(65, 65),
         Interval(88, 92), Interval(64, 82), Interval(79, 97), Interval(44, 48), Interval(43, 51)],
        # Job 8
        [Interval(37, 37), Interval(8, 10), Interval(45, 53), Interval(22, 24), Interval(1, 1),
         Interval(71, 85), Interval(34, 44), Interval(13, 17), Interval(8, 10), Interval(41, 41),
         Interval(35, 35), Interval(74, 92), Interval(7, 9), Interval(54, 68), Interval(55, 65)],
        # Job 9
        [Interval(1, 1), Interval(67, 79), Interval(42, 52), Interval(46, 46), Interval(9, 11),
         Interval(37, 37), Interval(57, 63), Interval(79, 89), Interval(25, 27), Interval(10, 12),
         Interval(34, 40), Interval(68, 90), Interval(64, 86), Interval(44, 54), Interval(51, 51)],
        # Job 10
        [Interval(22, 22), Interval(43, 55), Interval(33, 33), Interval(2, 2), Interval(24, 24),
         Interval(3, 3), Interval(68, 78), Interval(60, 76), Interval(18, 24), Interval(59, 63),
         Interval(66, 72), Interval(88, 100), Interval(41, 45), Interval(38, 40), Interval(44, 52)],
        # Job 11
        [Interval(80, 82), Interval(45, 47), Interval(19, 23), Interval(20, 26), Interval(75, 97),
         Interval(19, 19), Interval(57, 71), Interval(52, 52), Interval(22, 22), Interval(45, 55),
         Interval(11, 11), Interval(67, 79), Interval(72, 82), Interval(14, 18), Interval(70, 80)],
        # Job 12
        [Interval(18, 24), Interval(74, 86), Interval(28, 32), Interval(29, 35), Interval(21, 23),
         Interval(22, 24), Interval(76, 94), Interval(86, 98), Interval(13, 15), Interval(12, 14),
         Interval(68, 68), Interval(54, 66), Interval(40, 50), Interval(30, 34), Interval(86, 94)],
        # Job 13
        [Interval(25, 33), Interval(83, 107), Interval(52, 52), Interval(53, 65), Interval(29, 37),
         Interval(12, 12), Interval(72, 74), Interval(94, 98), Interval(69, 81), Interval(11, 13),
         Interval(75, 91), Interval(3, 3), Interval(80, 100), Interval(56, 58), Interval(6, 6)],
        # Job 14
        [Interval(84, 104), Interval(16, 20), Interval(48, 60), Interval(40, 44), Interval(67, 73),
         Interval(27, 31), Interval(41, 45), Interval(44, 56), Interval(69, 81), Interval(61, 79),
         Interval(39, 41), Interval(47, 49), Interval(1, 1), Interval(26, 28), Interval(11, 13)],
    ],
    'name': 'INT__TAI15_15_05.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai15_15_05_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI15_15_05.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI15_15_05.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI15_15_05_F_15_01_INTERVAL_DATA
