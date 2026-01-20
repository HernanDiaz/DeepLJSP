"""
Problema INT__TAI20_15_03.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI20_15_03_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__tai20_15_03.F.15_01_interval',
    'sequences': [
        [12, 11, 8, 9, 7, 13, 0, 10, 2, 4, 5, 6, 3, 14, 1],
        [2, 5, 0, 10, 4, 1, 13, 11, 3, 14, 6, 8, 9, 12, 7],
        [3, 2, 6, 9, 5, 12, 0, 13, 7, 10, 14, 1, 4, 8, 11],
        [9, 14, 5, 7, 13, 10, 12, 2, 3, 8, 1, 6, 11, 0, 4],
        [3, 8, 6, 1, 13, 0, 9, 5, 14, 2, 12, 7, 4, 11, 10],
        [3, 8, 13, 11, 12, 1, 4, 14, 6, 5, 9, 0, 7, 10, 2],
        [11, 2, 0, 6, 4, 1, 5, 12, 9, 7, 3, 8, 13, 10, 14],
        [12, 3, 4, 11, 8, 1, 5, 0, 13, 6, 10, 9, 2, 14, 7],
        [5, 8, 7, 0, 12, 13, 1, 6, 4, 14, 10, 9, 3, 2, 11],
        [6, 3, 9, 8, 2, 1, 12, 7, 5, 14, 0, 4, 11, 13, 10],
        [6, 0, 4, 14, 8, 13, 12, 11, 10, 1, 9, 7, 5, 3, 2],
        [0, 6, 4, 3, 8, 2, 11, 1, 9, 5, 13, 12, 10, 14, 7],
        [2, 9, 5, 12, 3, 14, 4, 13, 11, 7, 1, 10, 8, 6, 0],
        [11, 7, 10, 4, 8, 14, 6, 3, 9, 5, 1, 13, 2, 12, 0],
        [8, 13, 10, 12, 0, 9, 2, 6, 11, 1, 3, 14, 5, 7, 4],
        [14, 7, 11, 6, 10, 9, 2, 0, 1, 12, 8, 3, 4, 13, 5],
        [8, 13, 7, 9, 11, 12, 5, 4, 2, 3, 14, 6, 0, 10, 1],
        [8, 14, 5, 11, 1, 0, 7, 3, 12, 2, 9, 10, 13, 6, 4],
        [8, 6, 1, 11, 7, 12, 14, 10, 0, 9, 3, 4, 5, 13, 2],
        [13, 1, 4, 0, 5, 7, 3, 6, 12, 8, 11, 2, 10, 14, 9],
    ],
    'durations': [
        # Job 0
        [Interval(90, 92), Interval(17, 17), Interval(4, 4), Interval(54, 72), Interval(64, 70),
         Interval(28, 32), Interval(75, 99), Interval(80, 80), Interval(87, 103), Interval(14, 14),
         Interval(15, 19), Interval(19, 25), Interval(1, 1), Interval(80, 90), Interval(35, 47)],
        # Job 1
        [Interval(77, 77), Interval(69, 85), Interval(8, 10), Interval(75, 79), Interval(22, 26),
         Interval(7, 9), Interval(60, 68), Interval(6, 6), Interval(12, 12), Interval(12, 14),
         Interval(69, 73), Interval(68, 84), Interval(86, 104), Interval(8, 8), Interval(6, 6)],
        # Job 2
        [Interval(86, 98), Interval(3, 3), Interval(11, 13), Interval(23, 31), Interval(57, 59),
         Interval(60, 72), Interval(89, 109), Interval(31, 35), Interval(6, 8), Interval(69, 87),
         Interval(88, 104), Interval(28, 32), Interval(49, 59), Interval(22, 24), Interval(85, 91)],
        # Job 3
        [Interval(17, 21), Interval(39, 51), Interval(58, 72), Interval(21, 27), Interval(29, 31),
         Interval(26, 34), Interval(45, 53), Interval(30, 34), Interval(71, 85), Interval(31, 31),
         Interval(3, 3), Interval(23, 27), Interval(8, 10), Interval(2, 2), Interval(22, 22)],
        # Job 4
        [Interval(84, 84), Interval(57, 65), Interval(33, 37), Interval(43, 45), Interval(34, 40),
         Interval(14, 18), Interval(92, 102), Interval(80, 90), Interval(50, 52), Interval(24, 28),
         Interval(13, 13), Interval(66, 86), Interval(37, 45), Interval(2, 2), Interval(96, 96)],
        # Job 5
        [Interval(75, 95), Interval(49, 61), Interval(2, 2), Interval(64, 66), Interval(47, 57),
         Interval(83, 111), Interval(71, 91), Interval(7, 9), Interval(20, 24), Interval(51, 67),
         Interval(92, 98), Interval(48, 56), Interval(82, 88), Interval(55, 73), Interval(13, 13)],
        # Job 6
        [Interval(63, 65), Interval(94, 94), Interval(4, 4), Interval(12, 14), Interval(95, 101),
         Interval(24, 28), Interval(28, 36), Interval(17, 23), Interval(83, 111), Interval(24, 32),
         Interval(59, 67), Interval(2, 2), Interval(20, 26), Interval(12, 16), Interval(62, 62)],
        # Job 7
        [Interval(56, 56), Interval(98, 98), Interval(48, 64), Interval(28, 28), Interval(1, 1),
         Interval(85, 107), Interval(27, 27), Interval(37, 39), Interval(35, 47), Interval(89, 99),
         Interval(75, 79), Interval(61, 65), Interval(60, 66), Interval(81, 81), Interval(6, 6)],
        # Job 8
        [Interval(62, 64), Interval(86, 110), Interval(58, 70), Interval(35, 39), Interval(82, 96),
         Interval(96, 96), Interval(76, 100), Interval(12, 14), Interval(68, 76), Interval(25, 31),
         Interval(49, 65), Interval(87, 111), Interval(10, 12), Interval(8, 8), Interval(96, 96)],
        # Job 9
        [Interval(15, 19), Interval(62, 80), Interval(71, 89), Interval(31, 35), Interval(79, 95),
         Interval(73, 91), Interval(44, 44), Interval(12, 16), Interval(85, 85), Interval(2, 2),
         Interval(57, 63), Interval(68, 76), Interval(26, 28), Interval(54, 72), Interval(60, 72)],
        # Job 10
        [Interval(40, 54), Interval(36, 48), Interval(55, 67), Interval(17, 17), Interval(63, 67),
         Interval(5, 5), Interval(84, 108), Interval(47, 47), Interval(9, 9), Interval(19, 21),
         Interval(9, 11), Interval(10, 12), Interval(84, 88), Interval(86, 94), Interval(61, 69)],
        # Job 11
        [Interval(63, 69), Interval(87, 95), Interval(7, 9), Interval(37, 37), Interval(96, 102),
         Interval(81, 99), Interval(14, 18), Interval(77, 101), Interval(17, 17), Interval(87, 109),
         Interval(87, 87), Interval(8, 8), Interval(35, 45), Interval(31, 35), Interval(34, 40)],
        # Job 12
        [Interval(93, 105), Interval(2, 2), Interval(19, 25), Interval(12, 12), Interval(12, 14),
         Interval(58, 66), Interval(28, 32), Interval(40, 48), Interval(24, 26), Interval(53, 59),
         Interval(9, 11), Interval(41, 47), Interval(23, 27), Interval(36, 42), Interval(65, 65)],
        # Job 13
        [Interval(32, 38), Interval(55, 69), Interval(49, 55), Interval(80, 88), Interval(26, 34),
         Interval(2, 2), Interval(44, 56), Interval(68, 70), Interval(58, 70), Interval(47, 61),
         Interval(43, 47), Interval(38, 38), Interval(89, 91), Interval(65, 75), Interval(32, 42)],
        # Job 14
        [Interval(66, 80), Interval(35, 45), Interval(16, 16), Interval(19, 23), Interval(43, 57),
         Interval(9, 11), Interval(44, 48), Interval(2, 2), Interval(46, 50), Interval(15, 17),
         Interval(56, 60), Interval(33, 41), Interval(11, 13), Interval(26, 34), Interval(79, 85)],
        # Job 15
        [Interval(74, 78), Interval(38, 42), Interval(19, 23), Interval(88, 94), Interval(41, 55),
         Interval(6, 6), Interval(79, 103), Interval(68, 82), Interval(69, 89), Interval(46, 56),
         Interval(51, 51), Interval(73, 89), Interval(67, 73), Interval(58, 72), Interval(17, 21)],
        # Job 16
        [Interval(44, 54), Interval(5, 5), Interval(55, 63), Interval(39, 41), Interval(64, 84),
         Interval(67, 73), Interval(77, 91), Interval(41, 53), Interval(22, 28), Interval(84, 88),
         Interval(70, 80), Interval(25, 27), Interval(48, 54), Interval(30, 34), Interval(13, 17)],
        # Job 17
        [Interval(10, 12), Interval(16, 20), Interval(6, 6), Interval(51, 69), Interval(81, 85),
         Interval(56, 72), Interval(78, 92), Interval(21, 21), Interval(52, 52), Interval(46, 52),
         Interval(30, 30), Interval(49, 63), Interval(29, 33), Interval(24, 26), Interval(27, 35)],
        # Job 18
        [Interval(72, 94), Interval(41, 43), Interval(11, 11), Interval(55, 73), Interval(44, 44),
         Interval(78, 102), Interval(8, 8), Interval(30, 40), Interval(68, 76), Interval(59, 75),
         Interval(69, 75), Interval(51, 59), Interval(42, 44), Interval(86, 90), Interval(31, 39)],
        # Job 19
        [Interval(18, 20), Interval(47, 59), Interval(69, 91), Interval(87, 91), Interval(19, 23),
         Interval(30, 38), Interval(51, 61), Interval(79, 99), Interval(47, 53), Interval(26, 30),
         Interval(13, 17), Interval(24, 30), Interval(70, 78), Interval(80, 86), Interval(73, 85)],
    ],
    'name': 'INT__TAI20_15_03.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai20_15_03_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI20_15_03.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI20_15_03.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI20_15_03_F_15_01_INTERVAL_DATA
