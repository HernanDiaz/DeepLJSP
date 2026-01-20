"""
Problema INT__TAI100_20_01.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI100_20_01_F_15_01_INTERVAL_DATA = {
    'num_jobs': 100,
    'num_machines': 20,
    'problem_id': 'int__tai100_20_01.F.15_01_interval',
    'sequences': [
        [11, 7, 18, 15, 0, 8, 19, 6, 13, 14, 17, 2, 4, 1, 16, 3, 9, 5, 12, 10],
        [0, 14, 7, 1, 11, 16, 6, 4, 8, 5, 13, 18, 9, 17, 15, 12, 19, 10, 2, 3],
        [15, 4, 10, 14, 5, 13, 9, 19, 8, 16, 7, 12, 11, 1, 3, 6, 0, 2, 18, 17],
        [0, 5, 11, 7, 6, 10, 4, 18, 3, 8, 14, 9, 17, 2, 19, 13, 1, 16, 15, 12],
        [3, 10, 1, 13, 18, 19, 5, 11, 6, 17, 8, 14, 9, 16, 4, 12, 2, 0, 15, 7],
        [3, 1, 17, 16, 2, 5, 14, 12, 11, 7, 13, 19, 15, 10, 0, 6, 18, 8, 9, 4],
        [17, 13, 18, 1, 9, 8, 11, 4, 16, 5, 3, 10, 2, 12, 14, 0, 6, 7, 19, 15],
        [19, 14, 16, 17, 7, 9, 11, 2, 15, 3, 18, 5, 12, 6, 1, 4, 8, 13, 10, 0],
        [10, 3, 5, 8, 14, 4, 16, 2, 17, 15, 18, 7, 12, 9, 19, 13, 0, 11, 1, 6],
        [15, 2, 7, 11, 12, 4, 17, 8, 0, 10, 14, 5, 9, 6, 3, 19, 13, 1, 18, 16],
        [16, 4, 1, 17, 5, 12, 15, 0, 14, 13, 18, 2, 19, 11, 3, 7, 8, 9, 10, 6],
        [15, 6, 7, 3, 19, 13, 14, 0, 12, 11, 17, 2, 4, 16, 1, 18, 10, 8, 9, 5],
        [10, 0, 7, 13, 4, 17, 2, 15, 14, 12, 5, 9, 18, 16, 19, 3, 1, 8, 11, 6],
        [8, 2, 7, 16, 18, 12, 11, 19, 15, 4, 14, 9, 3, 17, 6, 5, 10, 1, 13, 0],
        [18, 11, 13, 16, 17, 6, 0, 14, 12, 3, 15, 2, 8, 19, 4, 7, 10, 5, 9, 1],
        [13, 12, 9, 0, 17, 15, 1, 19, 6, 7, 5, 18, 14, 4, 16, 11, 2, 10, 3, 8],
        [13, 18, 9, 4, 1, 8, 17, 16, 5, 14, 19, 15, 3, 10, 7, 2, 6, 0, 12, 11],
        [13, 10, 12, 0, 19, 14, 18, 8, 5, 3, 11, 1, 9, 2, 16, 17, 6, 7, 15, 4],
        [10, 4, 3, 17, 13, 1, 2, 0, 12, 6, 7, 15, 8, 16, 9, 11, 18, 5, 19, 14],
        [18, 6, 9, 13, 19, 14, 3, 5, 12, 1, 4, 17, 7, 8, 2, 10, 16, 11, 15, 0],
        [15, 13, 1, 4, 19, 14, 18, 5, 8, 16, 10, 12, 6, 17, 7, 11, 3, 2, 0, 9],
        [9, 17, 5, 18, 8, 12, 14, 13, 0, 10, 6, 11, 1, 7, 4, 3, 19, 15, 2, 16],
        [1, 7, 17, 11, 9, 14, 18, 2, 15, 0, 4, 19, 10, 5, 12, 6, 16, 8, 3, 13],
        [19, 10, 13, 18, 7, 12, 11, 15, 3, 16, 9, 4, 0, 6, 2, 14, 17, 5, 1, 8],
        [6, 9, 17, 2, 11, 16, 4, 1, 13, 0, 10, 12, 18, 15, 5, 14, 19, 8, 3, 7],
        [10, 1, 14, 7, 15, 4, 13, 2, 5, 17, 0, 8, 18, 6, 12, 11, 9, 16, 3, 19],
        [8, 12, 13, 7, 5, 6, 19, 11, 3, 1, 9, 15, 17, 16, 10, 4, 14, 2, 18, 0],
        [17, 18, 1, 8, 16, 7, 5, 0, 11, 9, 4, 15, 12, 19, 2, 3, 13, 14, 6, 10],
        [6, 8, 7, 0, 16, 5, 18, 13, 9, 1, 2, 3, 14, 17, 10, 19, 15, 12, 4, 11],
        [10, 15, 7, 13, 9, 2, 8, 6, 1, 17, 11, 19, 5, 12, 4, 14, 3, 16, 0, 18],
        [17, 1, 4, 11, 13, 14, 9, 19, 6, 7, 15, 10, 0, 18, 8, 5, 3, 2, 12, 16],
        [10, 7, 13, 8, 9, 3, 12, 15, 6, 17, 19, 18, 4, 14, 16, 2, 1, 0, 11, 5],
        [14, 8, 7, 5, 13, 10, 6, 2, 18, 16, 15, 9, 3, 4, 11, 19, 0, 1, 17, 12],
        [9, 13, 16, 6, 10, 19, 12, 4, 17, 3, 5, 18, 11, 15, 7, 1, 0, 8, 2, 14],
        [9, 12, 6, 8, 11, 10, 3, 4, 15, 7, 14, 17, 1, 18, 19, 2, 5, 16, 13, 0],
        [12, 13, 11, 1, 10, 14, 19, 7, 6, 9, 8, 2, 5, 18, 0, 17, 15, 3, 4, 16],
        [1, 15, 12, 18, 10, 9, 13, 3, 8, 7, 5, 2, 19, 0, 14, 6, 4, 17, 16, 11],
        [14, 11, 2, 9, 10, 13, 15, 18, 3, 7, 17, 16, 5, 4, 1, 12, 6, 0, 8, 19],
        [14, 1, 13, 8, 6, 10, 7, 0, 9, 19, 16, 4, 15, 17, 2, 18, 3, 12, 11, 5],
        [2, 5, 16, 18, 0, 7, 13, 3, 4, 19, 8, 12, 17, 15, 14, 6, 1, 11, 10, 9],
        [9, 12, 6, 19, 2, 11, 1, 17, 13, 8, 7, 15, 4, 18, 10, 16, 0, 5, 3, 14],
        [14, 11, 3, 9, 6, 17, 4, 13, 19, 16, 10, 0, 7, 15, 18, 12, 5, 1, 2, 8],
        [12, 18, 6, 7, 13, 1, 19, 0, 10, 9, 15, 17, 11, 8, 5, 3, 16, 2, 14, 4],
        [18, 1, 10, 4, 7, 2, 14, 13, 3, 16, 12, 5, 6, 11, 19, 15, 17, 8, 9, 0],
        [7, 4, 6, 16, 12, 1, 18, 0, 8, 17, 19, 5, 13, 3, 10, 2, 14, 11, 9, 15],
        [16, 4, 1, 2, 0, 17, 6, 8, 9, 3, 12, 10, 7, 18, 13, 11, 5, 19, 14, 15],
        [17, 3, 2, 4, 8, 19, 16, 6, 15, 1, 10, 5, 7, 13, 12, 18, 0, 14, 9, 11],
        [16, 17, 4, 13, 18, 15, 7, 5, 0, 14, 8, 6, 9, 10, 1, 3, 12, 19, 11, 2],
        [3, 8, 7, 15, 9, 12, 17, 4, 2, 5, 11, 14, 6, 1, 13, 10, 0, 16, 18, 19],
        [3, 0, 17, 10, 4, 13, 18, 7, 9, 15, 2, 14, 5, 6, 8, 12, 19, 11, 16, 1],
        [12, 8, 6, 11, 3, 16, 10, 19, 1, 7, 15, 9, 2, 14, 13, 4, 0, 17, 18, 5],
        [17, 3, 2, 7, 1, 10, 6, 14, 19, 11, 13, 8, 4, 0, 5, 18, 16, 9, 15, 12],
        [1, 8, 7, 11, 15, 14, 10, 6, 9, 13, 17, 5, 4, 16, 18, 3, 2, 19, 12, 0],
        [4, 11, 8, 17, 3, 13, 9, 2, 0, 1, 5, 16, 15, 10, 12, 6, 14, 7, 18, 19],
        [18, 6, 17, 11, 3, 13, 9, 15, 8, 12, 5, 10, 2, 19, 16, 7, 14, 0, 4, 1],
        [13, 19, 7, 9, 2, 11, 14, 0, 16, 15, 1, 10, 4, 5, 3, 17, 18, 6, 8, 12],
        [11, 8, 10, 16, 12, 7, 15, 4, 14, 17, 19, 1, 5, 9, 2, 6, 18, 3, 13, 0],
        [4, 17, 6, 10, 16, 7, 2, 19, 11, 13, 3, 1, 8, 5, 0, 12, 15, 18, 14, 9],
        [17, 2, 7, 4, 9, 15, 19, 16, 5, 12, 11, 3, 1, 0, 8, 6, 10, 14, 18, 13],
        [12, 4, 19, 5, 17, 6, 14, 11, 0, 18, 8, 2, 13, 7, 1, 10, 3, 15, 16, 9],
        [7, 19, 12, 3, 15, 10, 2, 5, 0, 9, 18, 17, 1, 8, 6, 11, 16, 14, 13, 4],
        [7, 8, 4, 3, 18, 19, 11, 14, 6, 0, 16, 5, 17, 9, 10, 12, 15, 1, 2, 13],
        [17, 13, 19, 6, 3, 18, 12, 9, 16, 8, 5, 1, 7, 14, 11, 4, 15, 2, 0, 10],
        [16, 2, 11, 7, 12, 14, 9, 17, 0, 10, 4, 1, 6, 13, 19, 8, 5, 3, 15, 18],
        [16, 9, 7, 18, 11, 8, 4, 3, 2, 15, 1, 0, 19, 5, 10, 12, 13, 14, 17, 6],
        [4, 1, 17, 6, 8, 13, 19, 0, 14, 9, 3, 12, 10, 5, 18, 7, 16, 15, 2, 11],
        [12, 6, 16, 0, 2, 19, 4, 8, 7, 14, 5, 3, 18, 11, 15, 10, 13, 17, 1, 9],
        [15, 18, 11, 13, 19, 7, 1, 2, 16, 8, 14, 17, 4, 9, 12, 10, 3, 6, 5, 0],
        [2, 13, 11, 12, 4, 17, 7, 14, 6, 8, 5, 3, 15, 16, 19, 18, 9, 1, 10, 0],
        [9, 6, 7, 8, 14, 2, 3, 4, 18, 16, 15, 12, 0, 13, 10, 19, 17, 11, 5, 1],
        [9, 2, 12, 15, 8, 13, 1, 19, 5, 16, 14, 7, 4, 10, 11, 18, 17, 6, 0, 3],
        [6, 18, 11, 8, 4, 7, 19, 9, 5, 2, 17, 15, 0, 1, 16, 10, 13, 3, 12, 14],
        [12, 16, 8, 19, 17, 0, 14, 6, 18, 1, 5, 4, 9, 13, 7, 15, 3, 2, 11, 10],
        [10, 1, 2, 8, 7, 12, 4, 19, 16, 5, 6, 14, 9, 3, 18, 17, 11, 15, 0, 13],
        [7, 14, 12, 5, 10, 13, 3, 16, 2, 1, 4, 19, 15, 0, 11, 18, 9, 17, 6, 8],
        [1, 13, 17, 0, 19, 12, 15, 16, 10, 18, 4, 6, 5, 2, 14, 3, 8, 11, 7, 9],
        [13, 4, 7, 9, 8, 18, 2, 19, 12, 6, 17, 14, 0, 16, 5, 15, 11, 1, 10, 3],
        [14, 3, 1, 4, 17, 7, 16, 0, 8, 11, 10, 6, 12, 18, 5, 13, 9, 2, 15, 19],
        [12, 13, 11, 18, 9, 8, 2, 4, 5, 0, 14, 6, 10, 17, 7, 1, 3, 15, 16, 19],
        [18, 5, 7, 3, 19, 11, 1, 13, 9, 8, 6, 2, 14, 12, 4, 16, 0, 17, 10, 15],
        [6, 16, 10, 19, 13, 0, 15, 9, 12, 8, 17, 7, 4, 18, 14, 5, 2, 1, 11, 3],
        [17, 15, 10, 13, 11, 18, 9, 1, 5, 0, 7, 4, 12, 16, 14, 3, 2, 8, 19, 6],
        [2, 3, 8, 1, 13, 15, 19, 7, 6, 10, 5, 14, 0, 4, 11, 17, 9, 12, 16, 18],
        [15, 5, 1, 11, 16, 0, 4, 7, 13, 18, 8, 17, 12, 9, 6, 10, 3, 2, 19, 14],
        [6, 0, 3, 14, 12, 9, 8, 16, 4, 18, 13, 1, 10, 7, 5, 19, 15, 2, 11, 17],
        [2, 10, 19, 13, 11, 0, 17, 4, 12, 9, 5, 18, 1, 6, 14, 8, 7, 16, 3, 15],
        [7, 10, 4, 6, 12, 15, 16, 17, 11, 9, 1, 2, 19, 8, 18, 13, 14, 0, 5, 3],
        [7, 12, 3, 14, 10, 2, 15, 18, 16, 9, 5, 1, 11, 8, 19, 4, 17, 6, 13, 0],
        [17, 6, 8, 11, 7, 13, 0, 5, 1, 10, 16, 4, 9, 3, 18, 15, 19, 14, 12, 2],
        [15, 1, 7, 19, 10, 6, 5, 17, 2, 16, 8, 14, 13, 3, 4, 9, 11, 0, 18, 12],
        [17, 5, 19, 4, 16, 7, 13, 10, 11, 2, 8, 14, 9, 15, 18, 1, 0, 6, 3, 12],
        [17, 18, 19, 7, 6, 13, 15, 1, 16, 9, 8, 5, 14, 3, 11, 12, 0, 4, 2, 10],
        [8, 2, 13, 6, 18, 3, 19, 7, 0, 4, 1, 9, 10, 5, 14, 17, 12, 11, 15, 16],
        [14, 7, 17, 18, 4, 9, 12, 13, 10, 5, 6, 11, 0, 8, 19, 15, 1, 3, 16, 2],
        [18, 4, 1, 13, 6, 3, 16, 0, 8, 14, 11, 19, 9, 7, 17, 2, 10, 5, 12, 15],
        [16, 19, 13, 18, 7, 10, 17, 3, 9, 6, 0, 4, 8, 1, 15, 14, 5, 12, 2, 11],
        [10, 0, 1, 9, 3, 18, 13, 7, 8, 5, 15, 2, 17, 6, 11, 16, 12, 14, 19, 4],
        [4, 9, 3, 10, 8, 6, 12, 18, 17, 16, 7, 11, 15, 13, 19, 5, 0, 14, 1, 2],
        [5, 19, 0, 13, 16, 6, 17, 10, 15, 1, 3, 14, 2, 8, 9, 7, 12, 18, 4, 11],
        [4, 7, 14, 8, 13, 12, 11, 1, 17, 9, 19, 0, 2, 16, 6, 15, 3, 10, 5, 18],
    ],
    'durations': [
        # Job 0
        [Interval(73, 93), Interval(55, 63), Interval(47, 51), Interval(78, 90), Interval(31, 39),
         Interval(58, 78), Interval(56, 60), Interval(57, 75), Interval(38, 50), Interval(2, 2),
         Interval(57, 69), Interval(23, 27), Interval(67, 73), Interval(1, 1), Interval(72, 96),
         Interval(54, 58), Interval(32, 38), Interval(43, 49), Interval(75, 87), Interval(50, 66)],
        # Job 1
        [Interval(10, 12), Interval(59, 75), Interval(44, 46), Interval(83, 89), Interval(91, 91),
         Interval(54, 66), Interval(60, 62), Interval(6, 6), Interval(92, 98), Interval(18, 18),
         Interval(6, 8), Interval(72, 74), Interval(3, 3), Interval(79, 105), Interval(27, 33),
         Interval(84, 102), Interval(6, 8), Interval(37, 37), Interval(14, 14), Interval(9, 9)],
        # Job 2
        [Interval(30, 38), Interval(5, 5), Interval(2, 2), Interval(64, 80), Interval(26, 26),
         Interval(50, 60), Interval(22, 26), Interval(58, 64), Interval(26, 30), Interval(98, 98),
         Interval(3, 3), Interval(1, 1), Interval(25, 31), Interval(90, 94), Interval(34, 44),
         Interval(24, 28), Interval(88, 94), Interval(37, 45), Interval(6, 6), Interval(89, 95)],
        # Job 3
        [Interval(9, 9), Interval(70, 84), Interval(46, 48), Interval(45, 45), Interval(71, 93),
         Interval(19, 21), Interval(83, 89), Interval(85, 91), Interval(18, 18), Interval(77, 89),
         Interval(19, 25), Interval(70, 76), Interval(79, 105), Interval(82, 86), Interval(60, 76),
         Interval(47, 63), Interval(60, 70), Interval(10, 10), Interval(59, 69), Interval(51, 69)],
        # Job 4
        [Interval(55, 69), Interval(71, 79), Interval(27, 31), Interval(71, 91), Interval(81, 97),
         Interval(29, 39), Interval(32, 36), Interval(24, 24), Interval(94, 102), Interval(81, 109),
         Interval(57, 63), Interval(20, 26), Interval(47, 61), Interval(71, 73), Interval(3, 3),
         Interval(73, 91), Interval(39, 43), Interval(49, 49), Interval(83, 111), Interval(44, 54)],
        # Job 5
        [Interval(70, 90), Interval(92, 98), Interval(47, 55), Interval(96, 96), Interval(21, 27),
         Interval(13, 17), Interval(89, 91), Interval(68, 78), Interval(86, 112), Interval(62, 74),
         Interval(95, 97), Interval(67, 67), Interval(94, 98), Interval(54, 58), Interval(23, 23),
         Interval(33, 43), Interval(86, 108), Interval(42, 46), Interval(39, 43), Interval(76, 90)],
        # Job 6
        [Interval(8, 8), Interval(88, 96), Interval(61, 71), Interval(56, 62), Interval(30, 32),
         Interval(59, 67), Interval(2, 2), Interval(13, 13), Interval(32, 32), Interval(36, 42),
         Interval(49, 57), Interval(23, 25), Interval(77, 93), Interval(22, 28), Interval(50, 56),
         Interval(78, 102), Interval(45, 53), Interval(41, 43), Interval(52, 56), Interval(1, 1)],
        # Job 7
        [Interval(9, 11), Interval(59, 77), Interval(81, 91), Interval(26, 26), Interval(58, 70),
         Interval(27, 33), Interval(69, 87), Interval(70, 72), Interval(91, 99), Interval(16, 18),
         Interval(80, 104), Interval(29, 31), Interval(41, 41), Interval(46, 62), Interval(12, 12),
         Interval(4, 4), Interval(17, 17), Interval(57, 63), Interval(49, 59), Interval(76, 90)],
        # Job 8
        [Interval(22, 26), Interval(20, 26), Interval(45, 47), Interval(34, 44), Interval(32, 32),
         Interval(40, 40), Interval(47, 57), Interval(32, 40), Interval(73, 93), Interval(22, 24),
         Interval(17, 19), Interval(87, 97), Interval(82, 108), Interval(63, 71), Interval(31, 31),
         Interval(25, 25), Interval(64, 74), Interval(45, 47), Interval(45, 57), Interval(86, 100)],
        # Job 9
        [Interval(54, 54), Interval(73, 89), Interval(32, 42), Interval(47, 57), Interval(63, 69),
         Interval(2, 2), Interval(91, 101), Interval(86, 104), Interval(42, 46), Interval(83, 99),
         Interval(81, 85), Interval(59, 75), Interval(22, 22), Interval(44, 44), Interval(1, 1),
         Interval(19, 23), Interval(39, 51), Interval(32, 42), Interval(67, 75), Interval(47, 53)],
        # Job 10
        [Interval(52, 52), Interval(18, 20), Interval(8, 8), Interval(78, 92), Interval(62, 66),
         Interval(28, 36), Interval(21, 23), Interval(36, 38), Interval(51, 57), Interval(91, 101),
         Interval(84, 100), Interval(58, 58), Interval(15, 17), Interval(86, 86), Interval(49, 65),
         Interval(3, 3), Interval(64, 72), Interval(83, 105), Interval(15, 19), Interval(30, 30)],
        # Job 11
        [Interval(28, 30), Interval(8, 8), Interval(88, 90), Interval(32, 34), Interval(14, 14),
         Interval(87, 111), Interval(74, 94), Interval(76, 80), Interval(5, 5), Interval(67, 85),
         Interval(55, 67), Interval(86, 104), Interval(19, 23), Interval(8, 10), Interval(93, 97),
         Interval(51, 61), Interval(23, 31), Interval(75, 75), Interval(42, 42), Interval(5, 5)],
        # Job 12
        [Interval(51, 63), Interval(28, 32), Interval(45, 59), Interval(83, 97), Interval(56, 60),
         Interval(10, 10), Interval(37, 49), Interval(6, 8), Interval(68, 92), Interval(15, 17),
         Interval(10, 10), Interval(90, 94), Interval(52, 60), Interval(21, 21), Interval(73, 79),
         Interval(13, 17), Interval(84, 106), Interval(9, 11), Interval(64, 64), Interval(67, 69)],
        # Job 13
        [Interval(40, 52), Interval(73, 81), Interval(21, 25), Interval(32, 34), Interval(4, 4),
         Interval(61, 71), Interval(5, 5), Interval(45, 59), Interval(2, 2), Interval(32, 36),
         Interval(24, 24), Interval(79, 99), Interval(46, 46), Interval(35, 35), Interval(10, 10),
         Interval(23, 25), Interval(51, 55), Interval(90, 106), Interval(17, 21), Interval(43, 55)],
        # Job 14
        [Interval(88, 94), Interval(83, 107), Interval(1, 1), Interval(83, 97), Interval(69, 81),
         Interval(59, 59), Interval(32, 40), Interval(57, 57), Interval(64, 82), Interval(38, 40),
         Interval(71, 93), Interval(7, 7), Interval(24, 30), Interval(1, 1), Interval(35, 43),
         Interval(19, 23), Interval(70, 70), Interval(12, 16), Interval(12, 12), Interval(67, 71)],
        # Job 15
        [Interval(33, 33), Interval(12, 14), Interval(65, 87), Interval(32, 34), Interval(61, 69),
         Interval(22, 26), Interval(45, 55), Interval(37, 41), Interval(41, 41), Interval(68, 72),
         Interval(44, 50), Interval(83, 95), Interval(32, 32), Interval(49, 49), Interval(62, 80),
         Interval(30, 32), Interval(12, 14), Interval(64, 72), Interval(61, 69), Interval(87, 99)],
        # Job 16
        [Interval(53, 57), Interval(71, 91), Interval(35, 37), Interval(27, 29), Interval(80, 108),
         Interval(76, 94), Interval(20, 20), Interval(89, 99), Interval(70, 84), Interval(19, 21),
         Interval(65, 83), Interval(32, 32), Interval(66, 70), Interval(23, 25), Interval(1, 1),
         Interval(69, 81), Interval(15, 17), Interval(79, 79), Interval(72, 92), Interval(32, 38)],
        # Job 17
        [Interval(77, 79), Interval(83, 95), Interval(59, 67), Interval(37, 45), Interval(18, 20),
         Interval(58, 78), Interval(86, 88), Interval(6, 6), Interval(51, 51), Interval(1, 1),
         Interval(43, 53), Interval(64, 86), Interval(5, 5), Interval(45, 49), Interval(83, 101),
         Interval(43, 47), Interval(47, 57), Interval(20, 22), Interval(23, 31), Interval(79, 89)],
        # Job 18
        [Interval(82, 98), Interval(4, 4), Interval(61, 79), Interval(36, 36), Interval(42, 50),
         Interval(68, 88), Interval(53, 67), Interval(57, 77), Interval(35, 43), Interval(61, 81),
         Interval(53, 69), Interval(66, 84), Interval(13, 13), Interval(61, 77), Interval(73, 79),
         Interval(4, 4), Interval(51, 57), Interval(87, 107), Interval(27, 31), Interval(58, 60)],
        # Job 19
        [Interval(40, 48), Interval(83, 95), Interval(33, 39), Interval(22, 28), Interval(28, 36),
         Interval(74, 80), Interval(67, 77), Interval(36, 42), Interval(75, 87), Interval(53, 63),
         Interval(42, 56), Interval(54, 58), Interval(21, 23), Interval(42, 50), Interval(14, 16),
         Interval(53, 63), Interval(51, 55), Interval(24, 30), Interval(48, 64), Interval(10, 12)],
        # Job 20
        [Interval(25, 25), Interval(59, 73), Interval(4, 4), Interval(23, 23), Interval(75, 81),
         Interval(28, 30), Interval(14, 18), Interval(64, 74), Interval(24, 28), Interval(61, 75),
         Interval(83, 107), Interval(55, 57), Interval(27, 35), Interval(10, 10), Interval(77, 89),
         Interval(66, 82), Interval(3, 3), Interval(8, 8), Interval(24, 24), Interval(65, 71)],
        # Job 21
        [Interval(18, 20), Interval(28, 30), Interval(93, 95), Interval(21, 27), Interval(85, 87),
         Interval(15, 17), Interval(62, 66), Interval(36, 42), Interval(18, 22), Interval(50, 64),
         Interval(15, 15), Interval(29, 39), Interval(67, 69), Interval(70, 94), Interval(50, 64),
         Interval(13, 13), Interval(54, 60), Interval(79, 93), Interval(67, 77), Interval(32, 34)],
        # Job 22
        [Interval(45, 47), Interval(81, 87), Interval(15, 17), Interval(12, 12), Interval(19, 25),
         Interval(71, 75), Interval(27, 35), Interval(84, 96), Interval(56, 58), Interval(80, 108),
         Interval(22, 24), Interval(44, 58), Interval(15, 19), Interval(63, 83), Interval(20, 26),
         Interval(29, 39), Interval(48, 48), Interval(74, 92), Interval(31, 33), Interval(30, 40)],
        # Job 23
        [Interval(6, 6), Interval(28, 36), Interval(10, 10), Interval(53, 71), Interval(69, 79),
         Interval(77, 87), Interval(49, 53), Interval(51, 51), Interval(45, 57), Interval(63, 79),
         Interval(25, 31), Interval(26, 28), Interval(75, 99), Interval(22, 22), Interval(33, 33),
         Interval(41, 49), Interval(40, 48), Interval(94, 98), Interval(69, 93), Interval(52, 54)],
        # Job 24
        [Interval(39, 47), Interval(39, 45), Interval(64, 68), Interval(69, 81), Interval(57, 73),
         Interval(72, 94), Interval(55, 73), Interval(18, 24), Interval(6, 6), Interval(49, 57),
         Interval(1, 1), Interval(63, 71), Interval(80, 80), Interval(24, 26), Interval(33, 41),
         Interval(63, 79), Interval(16, 18), Interval(48, 48), Interval(41, 45), Interval(11, 13)],
        # Job 25
        [Interval(89, 91), Interval(63, 71), Interval(38, 46), Interval(65, 77), Interval(12, 14),
         Interval(84, 112), Interval(23, 25), Interval(68, 86), Interval(62, 76), Interval(87, 93),
         Interval(80, 80), Interval(63, 83), Interval(46, 62), Interval(13, 13), Interval(28, 30),
         Interval(22, 28), Interval(53, 71), Interval(11, 11), Interval(42, 46), Interval(13, 13)],
        # Job 26
        [Interval(69, 77), Interval(67, 67), Interval(47, 57), Interval(6, 6), Interval(26, 34),
         Interval(24, 26), Interval(72, 74), Interval(86, 86), Interval(48, 58), Interval(17, 21),
         Interval(76, 92), Interval(50, 54), Interval(69, 91), Interval(60, 66), Interval(21, 21),
         Interval(2, 2), Interval(67, 89), Interval(28, 30), Interval(41, 47), Interval(87, 93)],
        # Job 27
        [Interval(96, 102), Interval(6, 6), Interval(66, 78), Interval(63, 71), Interval(63, 75),
         Interval(45, 55), Interval(2, 2), Interval(48, 58), Interval(31, 31), Interval(57, 65),
         Interval(78, 84), Interval(87, 101), Interval(22, 24), Interval(82, 96), Interval(19, 23),
         Interval(72, 78), Interval(92, 106), Interval(44, 58), Interval(60, 76), Interval(90, 104)],
        # Job 28
        [Interval(46, 50), Interval(65, 75), Interval(57, 67), Interval(54, 66), Interval(64, 84),
         Interval(91, 105), Interval(25, 27), Interval(86, 106), Interval(9, 11), Interval(64, 72),
         Interval(35, 37), Interval(6, 6), Interval(23, 25), Interval(4, 4), Interval(12, 12),
         Interval(27, 31), Interval(42, 50), Interval(68, 90), Interval(28, 28), Interval(72, 86)],
        # Job 29
        [Interval(54, 54), Interval(38, 44), Interval(53, 69), Interval(56, 56), Interval(36, 48),
         Interval(52, 66), Interval(87, 103), Interval(45, 47), Interval(42, 44), Interval(1, 1),
         Interval(44, 54), Interval(37, 47), Interval(2, 2), Interval(30, 34), Interval(50, 60),
         Interval(2, 2), Interval(53, 61), Interval(55, 65), Interval(76, 76), Interval(40, 40)],
        # Job 30
        [Interval(78, 80), Interval(39, 47), Interval(69, 89), Interval(47, 53), Interval(47, 55),
         Interval(23, 23), Interval(12, 12), Interval(38, 38), Interval(69, 91), Interval(61, 69),
         Interval(39, 45), Interval(86, 96), Interval(68, 84), Interval(74, 74), Interval(36, 36),
         Interval(26, 28), Interval(46, 48), Interval(38, 50), Interval(10, 10), Interval(62, 76)],
        # Job 31
        [Interval(33, 33), Interval(56, 74), Interval(85, 101), Interval(39, 49), Interval(76, 84),
         Interval(74, 92), Interval(47, 61), Interval(88, 94), Interval(75, 99), Interval(37, 37),
         Interval(61, 81), Interval(3, 3), Interval(33, 33), Interval(34, 42), Interval(77, 83),
         Interval(84, 98), Interval(71, 87), Interval(47, 63), Interval(77, 103), Interval(5, 5)],
        # Job 32
        [Interval(73, 79), Interval(17, 19), Interval(19, 19), Interval(50, 64), Interval(69, 73),
         Interval(80, 92), Interval(58, 60), Interval(16, 18), Interval(18, 24), Interval(39, 45),
         Interval(2, 2), Interval(46, 56), Interval(75, 93), Interval(22, 22), Interval(6, 8),
         Interval(15, 19), Interval(52, 52), Interval(84, 84), Interval(14, 18), Interval(26, 30)],
        # Job 33
        [Interval(20, 26), Interval(42, 54), Interval(67, 69), Interval(88, 94), Interval(76, 76),
         Interval(85, 99), Interval(35, 43), Interval(12, 12), Interval(14, 16), Interval(39, 45),
         Interval(5, 5), Interval(5, 5), Interval(78, 92), Interval(68, 88), Interval(68, 82),
         Interval(78, 84), Interval(48, 54), Interval(33, 37), Interval(60, 80), Interval(76, 98)],
        # Job 34
        [Interval(2, 2), Interval(35, 39), Interval(27, 33), Interval(12, 16), Interval(42, 46),
         Interval(60, 76), Interval(21, 23), Interval(23, 25), Interval(13, 13), Interval(68, 92),
         Interval(45, 55), Interval(88, 90), Interval(12, 12), Interval(42, 48), Interval(36, 36),
         Interval(30, 30), Interval(26, 30), Interval(56, 56), Interval(53, 63), Interval(56, 64)],
        # Job 35
        [Interval(84, 100), Interval(32, 36), Interval(2, 2), Interval(34, 36), Interval(74, 90),
         Interval(52, 68), Interval(65, 87), Interval(3, 3), Interval(86, 92), Interval(8, 8),
         Interval(84, 110), Interval(22, 24), Interval(23, 29), Interval(45, 53), Interval(57, 75),
         Interval(35, 39), Interval(47, 63), Interval(64, 80), Interval(69, 71), Interval(56, 70)],
        # Job 36
        [Interval(66, 78), Interval(37, 45), Interval(53, 53), Interval(71, 95), Interval(4, 4),
         Interval(58, 78), Interval(38, 42), Interval(70, 90), Interval(17, 17), Interval(88, 92),
         Interval(50, 64), Interval(81, 81), Interval(22, 26), Interval(26, 26), Interval(33, 37),
         Interval(13, 13), Interval(36, 40), Interval(52, 66), Interval(41, 51), Interval(34, 42)],
        # Job 37
        [Interval(69, 75), Interval(61, 69), Interval(43, 57), Interval(90, 94), Interval(81, 95),
         Interval(11, 11), Interval(79, 87), Interval(77, 97), Interval(41, 43), Interval(55, 59),
         Interval(86, 88), Interval(79, 87), Interval(42, 44), Interval(94, 102), Interval(47, 47),
         Interval(63, 85), Interval(58, 64), Interval(3, 3), Interval(78, 84), Interval(18, 18)],
        # Job 38
        [Interval(12, 14), Interval(39, 49), Interval(84, 84), Interval(19, 19), Interval(59, 79),
         Interval(21, 25), Interval(28, 36), Interval(29, 31), Interval(25, 27), Interval(64, 64),
         Interval(50, 60), Interval(24, 30), Interval(47, 57), Interval(16, 18), Interval(83, 111),
         Interval(20, 22), Interval(69, 77), Interval(43, 47), Interval(28, 34), Interval(42, 56)],
        # Job 39
        [Interval(33, 43), Interval(68, 92), Interval(44, 52), Interval(46, 62), Interval(52, 56),
         Interval(38, 38), Interval(39, 39), Interval(45, 53), Interval(29, 29), Interval(89, 107),
         Interval(80, 92), Interval(20, 20), Interval(22, 24), Interval(19, 25), Interval(81, 81),
         Interval(35, 41), Interval(88, 108), Interval(90, 102), Interval(88, 92), Interval(14, 14)],
        # Job 40
        [Interval(70, 70), Interval(48, 48), Interval(80, 106), Interval(83, 89), Interval(20, 22),
         Interval(95, 99), Interval(6, 8), Interval(66, 70), Interval(5, 5), Interval(12, 14),
         Interval(23, 29), Interval(74, 84), Interval(90, 98), Interval(23, 27), Interval(46, 54),
         Interval(28, 34), Interval(35, 39), Interval(81, 85), Interval(40, 42), Interval(7, 7)],
        # Job 41
        [Interval(93, 93), Interval(69, 81), Interval(33, 33), Interval(44, 48), Interval(12, 16),
         Interval(16, 18), Interval(63, 77), Interval(59, 67), Interval(37, 39), Interval(55, 71),
         Interval(41, 49), Interval(96, 102), Interval(39, 43), Interval(11, 13), Interval(55, 73),
         Interval(31, 37), Interval(11, 13), Interval(46, 62), Interval(62, 70), Interval(29, 33)],
        # Job 42
        [Interval(53, 67), Interval(85, 109), Interval(91, 99), Interval(36, 46), Interval(65, 77),
         Interval(75, 101), Interval(91, 91), Interval(91, 93), Interval(87, 111), Interval(49, 55),
         Interval(59, 79), Interval(77, 81), Interval(30, 30), Interval(3, 3), Interval(52, 58),
         Interval(55, 63), Interval(76, 100), Interval(25, 31), Interval(67, 75), Interval(70, 76)],
        # Job 43
        [Interval(48, 58), Interval(90, 104), Interval(46, 60), Interval(26, 32), Interval(60, 68),
         Interval(19, 19), Interval(15, 15), Interval(74, 84), Interval(98, 100), Interval(36, 42),
         Interval(64, 80), Interval(79, 85), Interval(73, 81), Interval(22, 28), Interval(91, 101),
         Interval(81, 103), Interval(92, 104), Interval(70, 88), Interval(27, 35), Interval(19, 19)],
        # Job 44
        [Interval(48, 64), Interval(6, 6), Interval(60, 66), Interval(49, 51), Interval(61, 73),
         Interval(76, 84), Interval(54, 66), Interval(34, 38), Interval(9, 11), Interval(13, 15),
         Interval(39, 49), Interval(75, 87), Interval(53, 55), Interval(17, 23), Interval(57, 77),
         Interval(22, 28), Interval(46, 52), Interval(73, 83), Interval(69, 81), Interval(3, 3)],
        # Job 45
        [Interval(77, 89), Interval(65, 81), Interval(20, 24), Interval(4, 4), Interval(29, 31),
         Interval(26, 28), Interval(67, 85), Interval(50, 58), Interval(44, 52), Interval(82, 82),
         Interval(83, 95), Interval(7, 9), Interval(70, 90), Interval(25, 27), Interval(87, 109),
         Interval(97, 97), Interval(9, 11), Interval(64, 68), Interval(73, 79), Interval(76, 78)],
        # Job 46
        [Interval(66, 84), Interval(91, 107), Interval(63, 77), Interval(69, 81), Interval(16, 16),
         Interval(66, 72), Interval(52, 52), Interval(19, 23), Interval(23, 23), Interval(25, 31),
         Interval(54, 58), Interval(5, 5), Interval(69, 87), Interval(64, 80), Interval(48, 64),
         Interval(20, 26), Interval(30, 30), Interval(46, 56), Interval(27, 27), Interval(36, 40)],
        # Job 47
        [Interval(86, 106), Interval(24, 26), Interval(56, 56), Interval(61, 73), Interval(70, 84),
         Interval(58, 64), Interval(54, 56), Interval(86, 88), Interval(17, 23), Interval(59, 61),
         Interval(37, 43), Interval(20, 26), Interval(17, 17), Interval(23, 25), Interval(32, 42),
         Interval(50, 54), Interval(41, 51), Interval(82, 110), Interval(18, 20), Interval(44, 48)],
        # Job 48
        [Interval(33, 35), Interval(9, 9), Interval(13, 13), Interval(72, 76), Interval(4, 4),
         Interval(5, 5), Interval(39, 43), Interval(3, 3), Interval(61, 61), Interval(24, 32),
         Interval(47, 49), Interval(56, 70), Interval(35, 39), Interval(50, 66), Interval(6, 6),
         Interval(86, 96), Interval(34, 36), Interval(94, 96), Interval(89, 107), Interval(77, 103)],
        # Job 49
        [Interval(48, 52), Interval(23, 29), Interval(10, 10), Interval(72, 78), Interval(88, 98),
         Interval(8, 10), Interval(91, 93), Interval(48, 62), Interval(58, 68), Interval(51, 51),
         Interval(31, 35), Interval(56, 64), Interval(79, 103), Interval(44, 58), Interval(84, 108),
         Interval(16, 20), Interval(67, 83), Interval(69, 77), Interval(48, 52), Interval(61, 63)],
        # Job 50
        [Interval(24, 32), Interval(35, 47), Interval(83, 101), Interval(57, 57), Interval(9, 11),
         Interval(5, 5), Interval(82, 88), Interval(36, 46), Interval(85, 111), Interval(12, 12),
         Interval(59, 65), Interval(38, 40), Interval(49, 57), Interval(49, 53), Interval(79, 83),
         Interval(55, 57), Interval(37, 41), Interval(5, 5), Interval(82, 98), Interval(60, 70)],
        # Job 51
        [Interval(79, 87), Interval(57, 57), Interval(43, 51), Interval(33, 41), Interval(10, 10),
         Interval(12, 14), Interval(1, 1), Interval(84, 112), Interval(34, 36), Interval(17, 17),
         Interval(56, 62), Interval(74, 98), Interval(16, 16), Interval(62, 70), Interval(1, 1),
         Interval(19, 19), Interval(9, 11), Interval(1, 1), Interval(54, 64), Interval(67, 67)],
        # Job 52
        [Interval(22, 26), Interval(69, 69), Interval(86, 88), Interval(75, 99), Interval(82, 108),
         Interval(40, 48), Interval(7, 9), Interval(39, 45), Interval(19, 23), Interval(35, 43),
         Interval(71, 79), Interval(79, 79), Interval(63, 83), Interval(19, 23), Interval(7, 9),
         Interval(83, 91), Interval(62, 70), Interval(25, 25), Interval(52, 64), Interval(82, 100)],
        # Job 53
        [Interval(43, 47), Interval(29, 29), Interval(95, 95), Interval(49, 61), Interval(55, 69),
         Interval(87, 107), Interval(68, 86), Interval(2, 2), Interval(42, 44), Interval(63, 73),
         Interval(85, 103), Interval(20, 20), Interval(53, 69), Interval(70, 86), Interval(61, 69),
         Interval(69, 71), Interval(38, 46), Interval(63, 75), Interval(52, 66), Interval(37, 39)],
        # Job 54
        [Interval(77, 81), Interval(53, 57), Interval(57, 73), Interval(59, 63), Interval(82, 88),
         Interval(31, 41), Interval(31, 31), Interval(76, 84), Interval(1, 1), Interval(59, 65),
         Interval(70, 76), Interval(28, 34), Interval(58, 66), Interval(13, 13), Interval(27, 27),
         Interval(27, 29), Interval(47, 57), Interval(68, 74), Interval(69, 83), Interval(65, 81)],
        # Job 55
        [Interval(8, 8), Interval(75, 75), Interval(9, 11), Interval(63, 67), Interval(38, 40),
         Interval(47, 53), Interval(14, 16), Interval(41, 51), Interval(6, 6), Interval(14, 18),
         Interval(78, 96), Interval(27, 35), Interval(67, 89), Interval(33, 33), Interval(71, 91),
         Interval(1, 1), Interval(75, 97), Interval(16, 16), Interval(64, 64), Interval(47, 63)],
        # Job 56
        [Interval(41, 49), Interval(48, 54), Interval(66, 66), Interval(26, 30), Interval(55, 57),
         Interval(40, 44), Interval(90, 96), Interval(5, 5), Interval(90, 108), Interval(16, 16),
         Interval(69, 83), Interval(30, 34), Interval(29, 29), Interval(30, 36), Interval(20, 26),
         Interval(57, 73), Interval(52, 52), Interval(94, 104), Interval(88, 94), Interval(12, 12)],
        # Job 57
        [Interval(57, 57), Interval(87, 95), Interval(8, 8), Interval(70, 88), Interval(61, 61),
         Interval(49, 59), Interval(41, 53), Interval(89, 97), Interval(37, 41), Interval(59, 65),
         Interval(6, 6), Interval(63, 63), Interval(24, 32), Interval(4, 4), Interval(75, 93),
         Interval(60, 60), Interval(61, 79), Interval(20, 24), Interval(74, 78), Interval(57, 65)],
        # Job 58
        [Interval(95, 99), Interval(36, 44), Interval(35, 45), Interval(85, 87), Interval(94, 100),
         Interval(42, 48), Interval(29, 33), Interval(50, 62), Interval(82, 108), Interval(26, 34),
         Interval(83, 91), Interval(22, 24), Interval(65, 77), Interval(56, 66), Interval(80, 104),
         Interval(1, 1), Interval(5, 5), Interval(92, 92), Interval(26, 26), Interval(13, 17)],
        # Job 59
        [Interval(24, 24), Interval(50, 66), Interval(57, 67), Interval(38, 44), Interval(11, 11),
         Interval(15, 19), Interval(42, 48), Interval(66, 80), Interval(2, 2), Interval(50, 64),
         Interval(62, 68), Interval(45, 57), Interval(74, 76), Interval(57, 61), Interval(95, 99),
         Interval(86, 90), Interval(48, 56), Interval(7, 9), Interval(52, 66), Interval(66, 76)],
        # Job 60
        [Interval(16, 20), Interval(67, 69), Interval(62, 78), Interval(73, 97), Interval(7, 9),
         Interval(87, 105), Interval(78, 86), Interval(29, 39), Interval(66, 86), Interval(39, 51),
         Interval(99, 99), Interval(38, 40), Interval(25, 27), Interval(70, 82), Interval(39, 51),
         Interval(77, 77), Interval(96, 98), Interval(3, 3), Interval(5, 5), Interval(53, 53)],
        # Job 61
        [Interval(11, 13), Interval(58, 62), Interval(52, 54), Interval(49, 53), Interval(15, 19),
         Interval(37, 45), Interval(23, 27), Interval(89, 91), Interval(18, 24), Interval(59, 71),
         Interval(30, 38), Interval(50, 52), Interval(54, 66), Interval(51, 51), Interval(66, 68),
         Interval(97, 97), Interval(36, 44), Interval(24, 24), Interval(20, 24), Interval(29, 29)],
        # Job 62
        [Interval(26, 32), Interval(36, 36), Interval(82, 100), Interval(64, 72), Interval(63, 65),
         Interval(2, 2), Interval(6, 6), Interval(60, 70), Interval(43, 45), Interval(47, 53),
         Interval(21, 21), Interval(58, 70), Interval(6, 6), Interval(90, 108), Interval(44, 44),
         Interval(12, 14), Interval(41, 43), Interval(12, 12), Interval(15, 15), Interval(42, 42)],
        # Job 63
        [Interval(32, 32), Interval(54, 64), Interval(25, 33), Interval(64, 86), Interval(49, 59),
         Interval(84, 102), Interval(36, 46), Interval(10, 10), Interval(56, 70), Interval(67, 73),
         Interval(74, 94), Interval(20, 26), Interval(9, 9), Interval(37, 41), Interval(8, 10),
         Interval(21, 25), Interval(65, 71), Interval(61, 69), Interval(8, 10), Interval(55, 73)],
        # Job 64
        [Interval(81, 85), Interval(24, 28), Interval(3, 3), Interval(34, 40), Interval(63, 69),
         Interval(58, 68), Interval(9, 11), Interval(75, 91), Interval(80, 80), Interval(42, 48),
         Interval(14, 18), Interval(72, 92), Interval(12, 12), Interval(76, 94), Interval(26, 34),
         Interval(2, 2), Interval(6, 8), Interval(12, 14), Interval(32, 38), Interval(45, 47)],
        # Job 65
        [Interval(21, 21), Interval(29, 29), Interval(50, 50), Interval(5, 5), Interval(6, 6),
         Interval(6, 6), Interval(79, 97), Interval(50, 50), Interval(49, 51), Interval(63, 67),
         Interval(64, 72), Interval(71, 71), Interval(43, 47), Interval(47, 55), Interval(47, 57),
         Interval(49, 57), Interval(37, 37), Interval(1, 1), Interval(8, 10), Interval(40, 42)],
        # Job 66
        [Interval(84, 92), Interval(54, 56), Interval(64, 66), Interval(95, 99), Interval(82, 106),
         Interval(65, 81), Interval(46, 48), Interval(8, 8), Interval(68, 80), Interval(42, 44),
         Interval(87, 109), Interval(12, 14), Interval(8, 8), Interval(32, 32), Interval(50, 56),
         Interval(65, 75), Interval(70, 70), Interval(32, 42), Interval(46, 58), Interval(20, 22)],
        # Job 67
        [Interval(41, 41), Interval(31, 31), Interval(51, 55), Interval(34, 34), Interval(84, 92),
         Interval(84, 108), Interval(64, 74), Interval(89, 95), Interval(31, 39), Interval(3, 3),
         Interval(48, 58), Interval(82, 102), Interval(47, 61), Interval(20, 22), Interval(89, 91),
         Interval(62, 74), Interval(23, 23), Interval(15, 17), Interval(34, 44), Interval(22, 28)],
        # Job 68
        [Interval(32, 38), Interval(49, 49), Interval(2, 2), Interval(30, 38), Interval(87, 91),
         Interval(31, 41), Interval(78, 84), Interval(27, 31), Interval(90, 108), Interval(92, 100),
         Interval(5, 5), Interval(27, 29), Interval(84, 110), Interval(11, 11), Interval(69, 89),
         Interval(79, 103), Interval(60, 70), Interval(5, 5), Interval(86, 102), Interval(89, 99)],
        # Job 69
        [Interval(76, 92), Interval(34, 34), Interval(54, 58), Interval(69, 85), Interval(28, 34),
         Interval(97, 97), Interval(70, 90), Interval(81, 95), Interval(30, 36), Interval(67, 79),
         Interval(69, 73), Interval(32, 42), Interval(78, 78), Interval(70, 92), Interval(63, 79),
         Interval(44, 56), Interval(40, 52), Interval(87, 93), Interval(22, 22), Interval(25, 25)],
        # Job 70
        [Interval(69, 87), Interval(88, 98), Interval(10, 12), Interval(53, 53), Interval(53, 61),
         Interval(3, 3), Interval(52, 52), Interval(4, 4), Interval(98, 100), Interval(24, 24),
         Interval(9, 11), Interval(41, 41), Interval(8, 10), Interval(26, 28), Interval(18, 20),
         Interval(83, 97), Interval(53, 57), Interval(43, 43), Interval(5, 5), Interval(8, 10)],
        # Job 71
        [Interval(17, 23), Interval(45, 47), Interval(49, 65), Interval(60, 66), Interval(64, 76),
         Interval(64, 64), Interval(53, 57), Interval(26, 34), Interval(23, 29), Interval(6, 6),
         Interval(67, 73), Interval(42, 54), Interval(83, 99), Interval(85, 109), Interval(68, 86),
         Interval(86, 102), Interval(76, 100), Interval(71, 79), Interval(47, 57), Interval(69, 85)],
        # Job 72
        [Interval(30, 40), Interval(41, 41), Interval(45, 51), Interval(97, 97), Interval(72, 74),
         Interval(65, 81), Interval(62, 72), Interval(19, 19), Interval(65, 79), Interval(71, 93),
         Interval(71, 87), Interval(45, 45), Interval(24, 32), Interval(60, 68), Interval(22, 22),
         Interval(59, 71), Interval(76, 82), Interval(14, 14), Interval(28, 30), Interval(33, 39)],
        # Job 73
        [Interval(50, 60), Interval(51, 57), Interval(76, 96), Interval(10, 10), Interval(63, 83),
         Interval(30, 34), Interval(55, 67), Interval(43, 57), Interval(33, 33), Interval(70, 92),
         Interval(56, 58), Interval(95, 103), Interval(11, 13), Interval(48, 50), Interval(32, 42),
         Interval(64, 80), Interval(86, 94), Interval(56, 64), Interval(6, 6), Interval(64, 68)],
        # Job 74
        [Interval(30, 40), Interval(30, 38), Interval(83, 111), Interval(21, 25), Interval(66, 72),
         Interval(50, 62), Interval(36, 40), Interval(13, 17), Interval(60, 74), Interval(65, 85),
         Interval(45, 59), Interval(89, 93), Interval(52, 58), Interval(51, 61), Interval(65, 81),
         Interval(71, 89), Interval(77, 99), Interval(22, 28), Interval(17, 23), Interval(64, 66)],
        # Job 75
        [Interval(65, 65), Interval(74, 78), Interval(6, 6), Interval(34, 44), Interval(82, 100),
         Interval(83, 85), Interval(12, 16), Interval(13, 13), Interval(29, 35), Interval(26, 32),
         Interval(21, 25), Interval(11, 13), Interval(30, 36), Interval(55, 63), Interval(39, 41),
         Interval(20, 22), Interval(8, 8), Interval(72, 92), Interval(63, 83), Interval(73, 81)],
        # Job 76
        [Interval(52, 54), Interval(19, 23), Interval(5, 5), Interval(36, 46), Interval(82, 104),
         Interval(28, 28), Interval(33, 41), Interval(66, 86), Interval(41, 45), Interval(28, 36),
         Interval(17, 17), Interval(11, 11), Interval(69, 75), Interval(29, 35), Interval(41, 53),
         Interval(62, 74), Interval(87, 93), Interval(64, 66), Interval(58, 68), Interval(57, 63)],
        # Job 77
        [Interval(78, 104), Interval(74, 88), Interval(69, 83), Interval(38, 50), Interval(29, 31),
         Interval(75, 93), Interval(52, 56), Interval(25, 27), Interval(18, 20), Interval(88, 98),
         Interval(82, 84), Interval(6, 8), Interval(41, 47), Interval(7, 9), Interval(5, 5),
         Interval(59, 73), Interval(50, 66), Interval(88, 108), Interval(75, 87), Interval(34, 38)],
        # Job 78
        [Interval(31, 35), Interval(48, 64), Interval(82, 88), Interval(15, 15), Interval(35, 41),
         Interval(63, 65), Interval(24, 24), Interval(64, 82), Interval(19, 19), Interval(24, 28),
         Interval(51, 67), Interval(11, 13), Interval(13, 15), Interval(21, 23), Interval(33, 43),
         Interval(60, 70), Interval(53, 63), Interval(81, 103), Interval(40, 40), Interval(46, 58)],
        # Job 79
        [Interval(86, 98), Interval(12, 12), Interval(74, 90), Interval(35, 47), Interval(47, 55),
         Interval(46, 46), Interval(6, 8), Interval(29, 31), Interval(26, 26), Interval(81, 97),
         Interval(57, 67), Interval(77, 85), Interval(71, 93), Interval(75, 95), Interval(66, 74),
         Interval(34, 34), Interval(15, 15), Interval(96, 100), Interval(97, 97), Interval(42, 54)],
        # Job 80
        [Interval(11, 11), Interval(10, 10), Interval(70, 76), Interval(44, 56), Interval(3, 3),
         Interval(14, 18), Interval(21, 27), Interval(86, 90), Interval(85, 103), Interval(11, 11),
         Interval(52, 64), Interval(4, 4), Interval(57, 75), Interval(55, 61), Interval(39, 45),
         Interval(60, 78), Interval(97, 99), Interval(50, 50), Interval(24, 26), Interval(42, 50)],
        # Job 81
        [Interval(78, 96), Interval(97, 97), Interval(73, 95), Interval(42, 56), Interval(77, 87),
         Interval(3, 3), Interval(69, 83), Interval(71, 83), Interval(32, 38), Interval(36, 46),
         Interval(52, 60), Interval(31, 31), Interval(48, 52), Interval(48, 64), Interval(70, 80),
         Interval(40, 44), Interval(32, 42), Interval(93, 95), Interval(3, 3), Interval(12, 16)],
        # Job 82
        [Interval(82, 94), Interval(77, 77), Interval(60, 68), Interval(42, 42), Interval(6, 8),
         Interval(76, 92), Interval(15, 17), Interval(18, 22), Interval(50, 62), Interval(7, 7),
         Interval(44, 50), Interval(2, 2), Interval(48, 50), Interval(47, 59), Interval(62, 68),
         Interval(72, 80), Interval(73, 91), Interval(11, 13), Interval(38, 44), Interval(92, 96)],
        # Job 83
        [Interval(72, 96), Interval(85, 113), Interval(53, 69), Interval(24, 32), Interval(59, 59),
         Interval(57, 71), Interval(47, 55), Interval(66, 88), Interval(24, 28), Interval(41, 45),
         Interval(64, 80), Interval(63, 63), Interval(67, 69), Interval(4, 4), Interval(79, 93),
         Interval(79, 95), Interval(75, 79), Interval(7, 9), Interval(45, 49), Interval(35, 41)],
        # Job 84
        [Interval(7, 7), Interval(34, 46), Interval(83, 109), Interval(7, 7), Interval(76, 88),
         Interval(55, 67), Interval(77, 101), Interval(69, 83), Interval(30, 40), Interval(88, 106),
         Interval(89, 101), Interval(5, 5), Interval(4, 4), Interval(10, 12), Interval(75, 91),
         Interval(61, 69), Interval(83, 89), Interval(12, 16), Interval(17, 17), Interval(29, 39)],
        # Job 85
        [Interval(45, 57), Interval(68, 76), Interval(71, 77), Interval(30, 40), Interval(91, 93),
         Interval(53, 53), Interval(18, 20), Interval(83, 97), Interval(32, 38), Interval(42, 52),
         Interval(47, 51), Interval(31, 37), Interval(63, 73), Interval(46, 46), Interval(80, 80),
         Interval(26, 34), Interval(64, 78), Interval(29, 33), Interval(48, 52), Interval(67, 73)],
        # Job 86
        [Interval(29, 33), Interval(67, 75), Interval(42, 48), Interval(67, 83), Interval(40, 40),
         Interval(84, 90), Interval(55, 55), Interval(18, 24), Interval(16, 20), Interval(19, 23),
         Interval(1, 1), Interval(5, 5), Interval(17, 17), Interval(83, 83), Interval(54, 62),
         Interval(63, 73), Interval(60, 72), Interval(88, 90), Interval(35, 35), Interval(58, 76)],
        # Job 87
        [Interval(85, 85), Interval(12, 14), Interval(46, 46), Interval(91, 101), Interval(83, 97),
         Interval(31, 31), Interval(69, 81), Interval(87, 89), Interval(16, 20), Interval(75, 85),
         Interval(45, 51), Interval(70, 78), Interval(52, 58), Interval(61, 75), Interval(88, 88),
         Interval(83, 87), Interval(48, 62), Interval(6, 6), Interval(77, 87), Interval(72, 92)],
        # Job 88
        [Interval(84, 94), Interval(49, 55), Interval(25, 33), Interval(36, 40), Interval(80, 100),
         Interval(65, 75), Interval(4, 4), Interval(86, 86), Interval(46, 50), Interval(57, 61),
         Interval(75, 75), Interval(38, 38), Interval(35, 39), Interval(41, 51), Interval(34, 46),
         Interval(23, 23), Interval(17, 21), Interval(3, 3), Interval(30, 40), Interval(69, 73)],
        # Job 89
        [Interval(58, 70), Interval(56, 64), Interval(80, 92), Interval(14, 14), Interval(53, 69),
         Interval(84, 90), Interval(43, 51), Interval(76, 90), Interval(64, 68), Interval(75, 81),
         Interval(83, 97), Interval(74, 86), Interval(78, 82), Interval(55, 61), Interval(8, 8),
         Interval(14, 14), Interval(41, 45), Interval(4, 4), Interval(1, 1), Interval(3, 3)],
        # Job 90
        [Interval(5, 5), Interval(59, 63), Interval(20, 26), Interval(57, 57), Interval(62, 72),
         Interval(45, 53), Interval(77, 99), Interval(20, 26), Interval(11, 13), Interval(3, 3),
         Interval(28, 30), Interval(68, 70), Interval(48, 56), Interval(13, 13), Interval(14, 18),
         Interval(2, 2), Interval(13, 13), Interval(44, 56), Interval(40, 52), Interval(68, 78)],
        # Job 91
        [Interval(74, 96), Interval(82, 90), Interval(47, 49), Interval(71, 71), Interval(73, 93),
         Interval(16, 18), Interval(16, 18), Interval(18, 18), Interval(33, 35), Interval(7, 7),
         Interval(2, 2), Interval(36, 46), Interval(32, 36), Interval(36, 38), Interval(6, 8),
         Interval(87, 89), Interval(53, 65), Interval(49, 63), Interval(61, 65), Interval(44, 56)],
        # Job 92
        [Interval(56, 62), Interval(46, 52), Interval(73, 89), Interval(12, 14), Interval(25, 33),
         Interval(17, 21), Interval(5, 5), Interval(66, 88), Interval(67, 75), Interval(11, 11),
         Interval(59, 77), Interval(77, 103), Interval(60, 64), Interval(93, 99), Interval(60, 80),
         Interval(28, 34), Interval(50, 60), Interval(70, 90), Interval(48, 62), Interval(84, 86)],
        # Job 93
        [Interval(84, 86), Interval(86, 90), Interval(94, 100), Interval(52, 64), Interval(77, 89),
         Interval(44, 50), Interval(72, 96), Interval(85, 105), Interval(59, 65), Interval(65, 79),
         Interval(73, 77), Interval(37, 43), Interval(47, 57), Interval(73, 85), Interval(48, 48),
         Interval(50, 56), Interval(5, 5), Interval(35, 41), Interval(44, 44), Interval(28, 28)],
        # Job 94
        [Interval(4, 4), Interval(15, 17), Interval(80, 84), Interval(41, 49), Interval(60, 70),
         Interval(35, 35), Interval(57, 59), Interval(31, 31), Interval(42, 48), Interval(11, 13),
         Interval(52, 64), Interval(50, 52), Interval(43, 43), Interval(11, 13), Interval(44, 52),
         Interval(35, 41), Interval(65, 79), Interval(81, 105), Interval(10, 12), Interval(93, 95)],
        # Job 95
        [Interval(39, 45), Interval(47, 51), Interval(81, 87), Interval(78, 102), Interval(16, 16),
         Interval(78, 78), Interval(80, 86), Interval(77, 87), Interval(7, 7), Interval(97, 101),
         Interval(19, 25), Interval(14, 14), Interval(54, 72), Interval(81, 81), Interval(71, 85),
         Interval(7, 7), Interval(31, 31), Interval(13, 15), Interval(54, 64), Interval(33, 33)],
        # Job 96
        [Interval(13, 15), Interval(60, 74), Interval(58, 74), Interval(24, 24), Interval(75, 75),
         Interval(81, 89), Interval(60, 64), Interval(58, 60), Interval(59, 71), Interval(70, 78),
         Interval(51, 65), Interval(18, 18), Interval(82, 98), Interval(70, 92), Interval(51, 55),
         Interval(23, 25), Interval(8, 8), Interval(16, 18), Interval(86, 112), Interval(61, 63)],
        # Job 97
        [Interval(58, 78), Interval(88, 98), Interval(17, 21), Interval(46, 56), Interval(35, 37),
         Interval(79, 91), Interval(64, 68), Interval(6, 8), Interval(48, 54), Interval(86, 92),
         Interval(11, 11), Interval(63, 77), Interval(2, 2), Interval(11, 11), Interval(44, 54),
         Interval(36, 46), Interval(66, 70), Interval(71, 89), Interval(44, 58), Interval(2, 2)],
        # Job 98
        [Interval(79, 105), Interval(14, 18), Interval(6, 6), Interval(20, 24), Interval(86, 100),
         Interval(77, 101), Interval(29, 29), Interval(31, 37), Interval(59, 65), Interval(19, 19),
         Interval(53, 69), Interval(18, 18), Interval(81, 101), Interval(15, 17), Interval(27, 27),
         Interval(4, 4), Interval(65, 73), Interval(2, 2), Interval(6, 8), Interval(72, 94)],
        # Job 99
        [Interval(15, 17), Interval(19, 19), Interval(30, 34), Interval(35, 43), Interval(18, 20),
         Interval(49, 53), Interval(11, 11), Interval(27, 35), Interval(23, 23), Interval(71, 73),
         Interval(45, 53), Interval(64, 78), Interval(30, 36), Interval(65, 81), Interval(3, 3),
         Interval(46, 62), Interval(37, 37), Interval(22, 26), Interval(15, 19), Interval(57, 63)],
    ],
    'name': 'INT__TAI100_20_01.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai100_20_01_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI100_20_01.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI100_20_01.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI100_20_01_F_15_01_INTERVAL_DATA
