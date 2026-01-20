"""
Problema INT__TAI30_15_05.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI30_15_05_F_15_01_INTERVAL_DATA = {
    'num_jobs': 30,
    'num_machines': 15,
    'problem_id': 'int__tai30_15_05.F.15_01_interval',
    'sequences': [
        [3, 11, 14, 5, 8, 6, 13, 0, 1, 2, 9, 10, 7, 12, 4],
        [0, 3, 4, 8, 9, 10, 5, 1, 12, 7, 13, 14, 2, 6, 11],
        [12, 10, 5, 8, 7, 14, 11, 2, 1, 6, 13, 4, 9, 3, 0],
        [5, 0, 9, 1, 8, 14, 10, 7, 11, 13, 3, 4, 12, 2, 6],
        [12, 6, 3, 11, 2, 8, 14, 5, 0, 9, 13, 4, 7, 1, 10],
        [6, 7, 14, 13, 0, 2, 8, 4, 11, 9, 3, 12, 10, 5, 1],
        [8, 12, 9, 7, 11, 5, 6, 14, 4, 13, 0, 1, 10, 2, 3],
        [12, 7, 10, 1, 5, 4, 9, 13, 2, 0, 3, 6, 11, 8, 14],
        [8, 7, 13, 12, 10, 6, 1, 3, 4, 2, 0, 14, 5, 9, 11],
        [8, 7, 6, 3, 14, 1, 0, 2, 12, 11, 10, 5, 4, 9, 13],
        [2, 8, 13, 11, 1, 5, 12, 3, 6, 10, 7, 4, 0, 14, 9],
        [1, 6, 8, 4, 7, 5, 13, 0, 14, 11, 10, 3, 12, 2, 9],
        [14, 13, 9, 8, 7, 12, 1, 4, 10, 6, 2, 3, 0, 5, 11],
        [9, 2, 6, 1, 0, 3, 12, 14, 8, 7, 4, 5, 11, 13, 10],
        [11, 10, 8, 3, 5, 7, 2, 14, 13, 6, 9, 0, 4, 1, 12],
        [0, 13, 8, 6, 3, 10, 7, 11, 2, 14, 5, 9, 1, 4, 12],
        [9, 5, 1, 12, 11, 2, 14, 7, 4, 8, 3, 6, 13, 10, 0],
        [13, 12, 4, 2, 8, 11, 14, 10, 1, 3, 6, 5, 7, 0, 9],
        [12, 14, 10, 5, 2, 7, 11, 13, 8, 6, 3, 9, 1, 0, 4],
        [7, 12, 0, 10, 13, 8, 6, 5, 9, 1, 14, 3, 11, 4, 2],
        [6, 12, 7, 11, 13, 14, 3, 9, 10, 4, 1, 8, 2, 5, 0],
        [9, 2, 3, 1, 10, 11, 5, 8, 6, 14, 0, 13, 7, 12, 4],
        [0, 14, 1, 12, 5, 8, 11, 10, 13, 6, 9, 2, 4, 3, 7],
        [8, 10, 13, 5, 7, 9, 6, 0, 11, 12, 1, 14, 4, 3, 2],
        [3, 10, 9, 0, 5, 2, 12, 4, 14, 8, 6, 11, 7, 1, 13],
        [10, 7, 12, 3, 0, 8, 6, 14, 5, 11, 9, 4, 2, 1, 13],
        [0, 13, 2, 12, 5, 11, 6, 8, 4, 9, 3, 7, 10, 1, 14],
        [14, 3, 0, 7, 8, 9, 12, 10, 4, 11, 13, 5, 1, 2, 6],
        [13, 1, 5, 6, 2, 14, 8, 7, 9, 10, 3, 11, 4, 12, 0],
        [10, 7, 1, 14, 8, 5, 2, 13, 0, 4, 9, 12, 11, 3, 6],
    ],
    'durations': [
        # Job 0
        [Interval(4, 4), Interval(23, 31), Interval(83, 97), Interval(72, 80), Interval(76, 76),
         Interval(14, 18), Interval(35, 41), Interval(67, 77), Interval(71, 89), Interval(85, 103),
         Interval(96, 98), Interval(5, 5), Interval(39, 49), Interval(9, 9), Interval(20, 26)],
        # Job 1
        [Interval(41, 53), Interval(48, 48), Interval(66, 72), Interval(72, 96), Interval(24, 26),
         Interval(29, 39), Interval(7, 9), Interval(30, 34), Interval(59, 65), Interval(88, 92),
         Interval(2, 2), Interval(82, 102), Interval(48, 62), Interval(23, 27), Interval(33, 41)],
        # Job 2
        [Interval(87, 87), Interval(54, 54), Interval(71, 81), Interval(68, 92), Interval(15, 19),
         Interval(1, 1), Interval(25, 27), Interval(33, 39), Interval(11, 13), Interval(49, 63),
         Interval(61, 81), Interval(6, 6), Interval(38, 46), Interval(76, 102), Interval(91, 101)],
        # Job 3
        [Interval(25, 25), Interval(11, 11), Interval(69, 69), Interval(33, 43), Interval(92, 104),
         Interval(48, 52), Interval(98, 98), Interval(49, 51), Interval(19, 19), Interval(69, 83),
         Interval(6, 6), Interval(89, 101), Interval(18, 20), Interval(34, 40), Interval(32, 36)],
        # Job 4
        [Interval(10, 10), Interval(31, 33), Interval(82, 106), Interval(22, 22), Interval(55, 55),
         Interval(53, 63), Interval(6, 6), Interval(69, 87), Interval(32, 40), Interval(54, 58),
         Interval(14, 18), Interval(21, 23), Interval(59, 59), Interval(35, 47), Interval(60, 66)],
        # Job 5
        [Interval(11, 13), Interval(57, 61), Interval(83, 107), Interval(91, 95), Interval(89, 97),
         Interval(7, 7), Interval(81, 109), Interval(9, 11), Interval(20, 26), Interval(44, 52),
         Interval(78, 90), Interval(60, 68), Interval(12, 16), Interval(78, 102), Interval(59, 79)],
        # Job 6
        [Interval(38, 48), Interval(1, 1), Interval(27, 27), Interval(26, 34), Interval(25, 25),
         Interval(3, 3), Interval(86, 102), Interval(70, 84), Interval(6, 6), Interval(37, 47),
         Interval(15, 19), Interval(73, 79), Interval(28, 30), Interval(63, 63), Interval(57, 61)],
        # Job 7
        [Interval(14, 14), Interval(53, 65), Interval(23, 31), Interval(55, 63), Interval(52, 60),
         Interval(6, 6), Interval(47, 49), Interval(39, 47), Interval(24, 30), Interval(26, 28),
         Interval(40, 46), Interval(30, 34), Interval(10, 12), Interval(5, 5), Interval(23, 27)],
        # Job 8
        [Interval(13, 15), Interval(45, 49), Interval(20, 22), Interval(30, 34), Interval(28, 30),
         Interval(35, 45), Interval(59, 67), Interval(24, 26), Interval(48, 50), Interval(4, 4),
         Interval(60, 74), Interval(27, 27), Interval(9, 9), Interval(73, 77), Interval(13, 17)],
        # Job 9
        [Interval(69, 71), Interval(96, 98), Interval(52, 52), Interval(20, 24), Interval(86, 88),
         Interval(80, 94), Interval(34, 38), Interval(83, 89), Interval(2, 2), Interval(91, 95),
         Interval(1, 1), Interval(16, 16), Interval(69, 71), Interval(97, 101), Interval(39, 47)],
        # Job 10
        [Interval(5, 5), Interval(26, 30), Interval(69, 85), Interval(23, 23), Interval(56, 70),
         Interval(64, 74), Interval(31, 39), Interval(19, 25), Interval(83, 97), Interval(43, 49),
         Interval(59, 75), Interval(60, 66), Interval(62, 64), Interval(21, 27), Interval(77, 81)],
        # Job 11
        [Interval(62, 76), Interval(23, 27), Interval(63, 67), Interval(29, 29), Interval(49, 53),
         Interval(88, 88), Interval(66, 74), Interval(24, 26), Interval(58, 58), Interval(17, 23),
         Interval(24, 24), Interval(33, 43), Interval(32, 36), Interval(62, 80), Interval(62, 70)],
        # Job 12
        [Interval(4, 4), Interval(4, 4), Interval(32, 36), Interval(18, 24), Interval(53, 67),
         Interval(47, 63), Interval(70, 70), Interval(66, 70), Interval(78, 82), Interval(52, 60),
         Interval(28, 30), Interval(86, 108), Interval(73, 95), Interval(58, 74), Interval(44, 56)],
        # Job 13
        [Interval(88, 88), Interval(72, 90), Interval(50, 50), Interval(38, 38), Interval(48, 56),
         Interval(7, 7), Interval(31, 35), Interval(41, 51), Interval(59, 59), Interval(36, 40),
         Interval(12, 16), Interval(65, 67), Interval(67, 77), Interval(80, 80), Interval(95, 99)],
        # Job 14
        [Interval(31, 39), Interval(85, 91), Interval(89, 107), Interval(74, 82), Interval(84, 88),
         Interval(12, 14), Interval(82, 106), Interval(23, 27), Interval(48, 52), Interval(65, 87),
         Interval(83, 95), Interval(38, 44), Interval(50, 56), Interval(9, 11), Interval(86, 112)],
        # Job 15
        [Interval(36, 48), Interval(15, 17), Interval(42, 46), Interval(40, 40), Interval(33, 37),
         Interval(62, 80), Interval(47, 57), Interval(31, 39), Interval(93, 103), Interval(67, 79),
         Interval(81, 103), Interval(44, 44), Interval(31, 39), Interval(68, 90), Interval(17, 17)],
        # Job 16
        [Interval(43, 49), Interval(47, 63), Interval(72, 76), Interval(80, 80), Interval(78, 100),
         Interval(59, 63), Interval(33, 35), Interval(64, 86), Interval(34, 44), Interval(42, 52),
         Interval(66, 74), Interval(84, 84), Interval(24, 28), Interval(40, 48), Interval(75, 89)],
        # Job 17
        [Interval(70, 84), Interval(38, 42), Interval(38, 48), Interval(67, 85), Interval(60, 78),
         Interval(42, 42), Interval(22, 28), Interval(34, 34), Interval(8, 8), Interval(76, 78),
         Interval(55, 59), Interval(53, 59), Interval(77, 83), Interval(12, 12), Interval(83, 95)],
        # Job 18
        [Interval(87, 105), Interval(49, 57), Interval(3, 3), Interval(46, 52), Interval(73, 79),
         Interval(37, 37), Interval(46, 54), Interval(65, 81), Interval(84, 112), Interval(43, 45),
         Interval(85, 93), Interval(2, 2), Interval(1, 1), Interval(85, 113), Interval(83, 95)],
        # Job 19
        [Interval(7, 7), Interval(84, 98), Interval(28, 36), Interval(38, 50), Interval(2, 2),
         Interval(59, 73), Interval(59, 65), Interval(21, 23), Interval(22, 24), Interval(81, 103),
         Interval(66, 74), Interval(29, 33), Interval(9, 11), Interval(80, 108), Interval(82, 96)],
        # Job 20
        [Interval(40, 52), Interval(13, 17), Interval(22, 24), Interval(65, 75), Interval(55, 59),
         Interval(60, 74), Interval(53, 63), Interval(82, 102), Interval(58, 74), Interval(50, 60),
         Interval(13, 13), Interval(29, 37), Interval(57, 71), Interval(32, 40), Interval(21, 21)],
        # Job 21
        [Interval(36, 42), Interval(33, 37), Interval(84, 96), Interval(65, 69), Interval(67, 73),
         Interval(87, 101), Interval(44, 52), Interval(74, 78), Interval(82, 104), Interval(43, 49),
         Interval(33, 35), Interval(58, 58), Interval(63, 85), Interval(46, 52), Interval(69, 91)],
        # Job 22
        [Interval(88, 110), Interval(9, 11), Interval(88, 92), Interval(52, 68), Interval(5, 5),
         Interval(15, 19), Interval(24, 24), Interval(76, 90), Interval(34, 40), Interval(51, 67),
         Interval(15, 19), Interval(86, 112), Interval(42, 42), Interval(65, 79), Interval(33, 39)],
        # Job 23
        [Interval(90, 98), Interval(60, 78), Interval(44, 50), Interval(83, 109), Interval(28, 32),
         Interval(28, 30), Interval(20, 24), Interval(26, 26), Interval(98, 100), Interval(12, 14),
         Interval(56, 62), Interval(59, 73), Interval(84, 94), Interval(1, 1), Interval(21, 27)],
        # Job 24
        [Interval(90, 92), Interval(21, 21), Interval(42, 42), Interval(70, 88), Interval(8, 8),
         Interval(8, 10), Interval(66, 66), Interval(1, 1), Interval(58, 60), Interval(35, 37),
         Interval(50, 58), Interval(51, 53), Interval(82, 92), Interval(70, 94), Interval(31, 35)],
        # Job 25
        [Interval(28, 34), Interval(93, 93), Interval(59, 77), Interval(68, 76), Interval(22, 22),
         Interval(84, 86), Interval(39, 41), Interval(70, 82), Interval(43, 53), Interval(81, 85),
         Interval(85, 93), Interval(74, 92), Interval(39, 47), Interval(61, 77), Interval(66, 68)],
        # Job 26
        [Interval(63, 65), Interval(53, 65), Interval(54, 72), Interval(51, 57), Interval(21, 21),
         Interval(71, 87), Interval(33, 37), Interval(82, 108), Interval(6, 8), Interval(57, 77),
         Interval(14, 16), Interval(84, 94), Interval(51, 57), Interval(92, 104), Interval(23, 29)],
        # Job 27
        [Interval(12, 16), Interval(85, 101), Interval(82, 92), Interval(13, 17), Interval(38, 42),
         Interval(20, 20), Interval(55, 67), Interval(7, 9), Interval(8, 8), Interval(57, 57),
         Interval(14, 14), Interval(80, 100), Interval(16, 16), Interval(36, 36), Interval(54, 64)],
        # Job 28
        [Interval(2, 2), Interval(75, 99), Interval(8, 8), Interval(2, 2), Interval(12, 12),
         Interval(32, 38), Interval(6, 6), Interval(72, 74), Interval(72, 92), Interval(36, 38),
         Interval(18, 20), Interval(71, 91), Interval(17, 21), Interval(12, 12), Interval(55, 65)],
        # Job 29
        [Interval(4, 4), Interval(8, 10), Interval(6, 8), Interval(59, 59), Interval(27, 31),
         Interval(34, 44), Interval(51, 59), Interval(18, 18), Interval(68, 72), Interval(14, 14),
         Interval(43, 51), Interval(69, 81), Interval(71, 85), Interval(96, 102), Interval(9, 9)],
    ],
    'name': 'INT__TAI30_15_05.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai30_15_05_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI30_15_05.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI30_15_05.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI30_15_05_F_15_01_INTERVAL_DATA
