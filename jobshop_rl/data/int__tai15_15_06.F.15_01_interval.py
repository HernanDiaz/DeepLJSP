"""
Problema INT__TAI15_15_06.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI15_15_06_F_15_01_INTERVAL_DATA = {
    'num_jobs': 15,
    'num_machines': 15,
    'problem_id': 'int__tai15_15_06.F.15_01_interval',
    'sequences': [
        [7, 12, 5, 8, 3, 14, 13, 9, 0, 1, 4, 2, 6, 11, 10],
        [8, 0, 5, 13, 6, 1, 4, 2, 3, 11, 10, 12, 9, 14, 7],
        [6, 8, 7, 1, 9, 5, 12, 4, 0, 2, 14, 11, 3, 13, 10],
        [12, 0, 14, 7, 13, 1, 6, 8, 11, 2, 3, 9, 5, 10, 4],
        [8, 2, 12, 11, 10, 9, 4, 3, 14, 5, 0, 7, 6, 13, 1],
        [13, 8, 6, 11, 14, 9, 12, 7, 0, 1, 10, 2, 5, 3, 4],
        [4, 1, 2, 13, 7, 6, 0, 8, 12, 14, 10, 9, 5, 3, 11],
        [4, 10, 14, 3, 6, 13, 11, 9, 0, 5, 1, 12, 8, 7, 2],
        [7, 1, 5, 4, 14, 8, 0, 9, 12, 3, 10, 2, 13, 11, 6],
        [3, 6, 13, 4, 5, 10, 2, 8, 12, 11, 9, 7, 14, 1, 0],
        [1, 4, 7, 2, 14, 10, 12, 13, 6, 5, 9, 0, 3, 8, 11],
        [0, 7, 14, 13, 8, 3, 6, 9, 5, 12, 10, 4, 1, 2, 11],
        [14, 10, 0, 8, 12, 13, 4, 11, 1, 3, 6, 5, 2, 9, 7],
        [13, 4, 8, 6, 5, 2, 9, 0, 11, 12, 1, 3, 14, 7, 10],
        [14, 2, 6, 4, 3, 11, 1, 5, 7, 0, 8, 10, 9, 12, 13],
    ],
    'durations': [
        # Job 0
        [Interval(95, 97), Interval(23, 23), Interval(61, 81), Interval(25, 27), Interval(26, 30),
         Interval(14, 18), Interval(27, 27), Interval(65, 77), Interval(18, 18), Interval(50, 64),
         Interval(38, 48), Interval(5, 5), Interval(12, 12), Interval(78, 104), Interval(63, 63)],
        # Job 1
        [Interval(29, 35), Interval(72, 90), Interval(92, 98), Interval(73, 85), Interval(47, 63),
         Interval(42, 48), Interval(59, 61), Interval(63, 83), Interval(22, 24), Interval(39, 49),
         Interval(83, 101), Interval(19, 21), Interval(5, 5), Interval(67, 77), Interval(66, 80)],
        # Job 2
        [Interval(54, 72), Interval(90, 96), Interval(57, 69), Interval(71, 87), Interval(9, 11),
         Interval(58, 74), Interval(23, 31), Interval(86, 100), Interval(22, 26), Interval(24, 28),
         Interval(8, 8), Interval(66, 72), Interval(26, 32), Interval(57, 75), Interval(86, 108)],
        # Job 3
        [Interval(68, 92), Interval(84, 90), Interval(58, 78), Interval(21, 25), Interval(50, 58),
         Interval(15, 17), Interval(67, 69), Interval(30, 34), Interval(68, 80), Interval(3, 3),
         Interval(2, 2), Interval(71, 71), Interval(4, 4), Interval(67, 67), Interval(26, 30)],
        # Job 4
        [Interval(43, 49), Interval(94, 98), Interval(10, 12), Interval(35, 47), Interval(88, 98),
         Interval(2, 2), Interval(92, 104), Interval(10, 10), Interval(38, 48), Interval(65, 65),
         Interval(23, 31), Interval(52, 62), Interval(75, 75), Interval(76, 98), Interval(72, 90)],
        # Job 5
        [Interval(5, 5), Interval(89, 93), Interval(82, 102), Interval(74, 100), Interval(59, 73),
         Interval(31, 41), Interval(62, 72), Interval(75, 101), Interval(89, 95), Interval(25, 29),
         Interval(13, 13), Interval(6, 8), Interval(91, 99), Interval(65, 67), Interval(13, 13)],
        # Job 6
        [Interval(79, 101), Interval(32, 34), Interval(72, 84), Interval(66, 86), Interval(83, 103),
         Interval(57, 77), Interval(71, 93), Interval(87, 101), Interval(11, 13), Interval(5, 5),
         Interval(77, 93), Interval(42, 42), Interval(4, 4), Interval(2, 2), Interval(70, 70)],
        # Job 7
        [Interval(79, 79), Interval(21, 27), Interval(41, 41), Interval(74, 92), Interval(45, 45),
         Interval(28, 30), Interval(3, 3), Interval(36, 48), Interval(5, 5), Interval(42, 46),
         Interval(81, 85), Interval(57, 61), Interval(57, 63), Interval(78, 78), Interval(43, 45)],
        # Job 8
        [Interval(17, 21), Interval(50, 60), Interval(19, 21), Interval(68, 80), Interval(66, 66),
         Interval(32, 42), Interval(51, 59), Interval(59, 67), Interval(36, 44), Interval(63, 83),
         Interval(48, 62), Interval(76, 92), Interval(54, 54), Interval(62, 62), Interval(6, 6)],
        # Job 9
        [Interval(24, 30), Interval(52, 66), Interval(6, 6), Interval(80, 100), Interval(6, 6),
         Interval(34, 40), Interval(58, 70), Interval(31, 39), Interval(25, 25), Interval(51, 67),
         Interval(77, 77), Interval(29, 31), Interval(1, 1), Interval(7, 7), Interval(67, 73)],
        # Job 10
        [Interval(4, 4), Interval(46, 60), Interval(6, 6), Interval(9, 11), Interval(44, 58),
         Interval(76, 102), Interval(35, 41), Interval(38, 38), Interval(34, 36), Interval(39, 49),
         Interval(98, 100), Interval(85, 91), Interval(49, 55), Interval(14, 18), Interval(85, 113)],
        # Job 11
        [Interval(27, 29), Interval(11, 11), Interval(71, 81), Interval(49, 53), Interval(34, 36),
         Interval(54, 66), Interval(44, 44), Interval(38, 40), Interval(60, 72), Interval(42, 56),
         Interval(34, 46), Interval(33, 35), Interval(70, 90), Interval(38, 38), Interval(28, 30)],
        # Job 12
        [Interval(28, 34), Interval(30, 34), Interval(37, 43), Interval(24, 26), Interval(35, 45),
         Interval(80, 90), Interval(35, 43), Interval(57, 65), Interval(14, 16), Interval(37, 45),
         Interval(88, 98), Interval(61, 67), Interval(14, 18), Interval(75, 87), Interval(88, 106)],
        # Job 13
        [Interval(8, 10), Interval(21, 21), Interval(7, 9), Interval(49, 61), Interval(74, 84),
         Interval(72, 80), Interval(69, 89), Interval(53, 69), Interval(67, 69), Interval(89, 109),
         Interval(21, 27), Interval(22, 24), Interval(90, 94), Interval(90, 92), Interval(20, 24)],
        # Job 14
        [Interval(69, 91), Interval(27, 33), Interval(59, 75), Interval(57, 59), Interval(40, 50),
         Interval(25, 33), Interval(43, 53), Interval(27, 29), Interval(61, 67), Interval(58, 68),
         Interval(77, 83), Interval(20, 26), Interval(85, 101), Interval(48, 62), Interval(47, 49)],
    ],
    'name': 'INT__TAI15_15_06.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai15_15_06_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI15_15_06.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI15_15_06.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI15_15_06_F_15_01_INTERVAL_DATA
