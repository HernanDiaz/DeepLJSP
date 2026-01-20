"""
Problema INT__TAI100_20_02.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI100_20_02_F_15_01_INTERVAL_DATA = {
    'num_jobs': 100,
    'num_machines': 20,
    'problem_id': 'int__tai100_20_02.F.15_01_interval',
    'sequences': [
        [8, 10, 5, 0, 7, 2, 14, 12, 3, 15, 18, 9, 11, 16, 4, 13, 19, 17, 6, 1],
        [3, 4, 6, 10, 16, 5, 13, 18, 1, 0, 14, 9, 15, 7, 17, 12, 8, 2, 11, 19],
        [0, 8, 13, 5, 2, 9, 18, 1, 14, 6, 17, 15, 3, 19, 12, 10, 7, 4, 16, 11],
        [12, 9, 14, 19, 16, 2, 0, 6, 1, 13, 17, 8, 7, 5, 10, 15, 4, 11, 3, 18],
        [9, 17, 12, 18, 13, 8, 15, 10, 6, 14, 19, 4, 5, 2, 0, 11, 7, 3, 16, 1],
        [11, 5, 18, 0, 9, 16, 19, 15, 4, 7, 8, 3, 17, 13, 2, 1, 14, 10, 12, 6],
        [7, 3, 9, 10, 13, 19, 6, 14, 5, 16, 0, 1, 2, 18, 4, 17, 8, 12, 15, 11],
        [4, 5, 9, 18, 10, 8, 11, 0, 16, 13, 12, 14, 19, 7, 15, 2, 1, 17, 6, 3],
        [17, 4, 8, 3, 7, 13, 12, 14, 9, 0, 5, 10, 15, 19, 2, 1, 6, 16, 18, 11],
        [0, 8, 19, 18, 13, 7, 17, 3, 15, 6, 2, 14, 9, 4, 16, 5, 11, 12, 1, 10],
        [10, 12, 1, 6, 2, 5, 0, 13, 16, 17, 3, 18, 8, 15, 11, 7, 14, 4, 19, 9],
        [6, 7, 5, 10, 1, 3, 18, 2, 15, 16, 4, 14, 0, 11, 13, 9, 8, 19, 17, 12],
        [18, 2, 4, 15, 7, 5, 11, 3, 13, 6, 0, 9, 17, 16, 1, 19, 8, 14, 12, 10],
        [17, 13, 14, 19, 0, 4, 9, 6, 5, 1, 8, 12, 18, 7, 3, 11, 10, 16, 15, 2],
        [15, 1, 13, 8, 19, 17, 6, 2, 9, 0, 14, 7, 4, 5, 16, 18, 10, 3, 11, 12],
        [8, 12, 5, 2, 19, 0, 15, 14, 4, 18, 11, 1, 17, 3, 9, 10, 16, 7, 13, 6],
        [14, 6, 16, 9, 11, 12, 13, 4, 2, 15, 19, 17, 5, 18, 3, 10, 7, 1, 0, 8],
        [12, 2, 13, 16, 11, 18, 19, 17, 15, 7, 1, 8, 3, 0, 4, 14, 10, 6, 9, 5],
        [14, 6, 9, 18, 3, 13, 2, 15, 19, 17, 12, 5, 1, 7, 0, 10, 4, 8, 11, 16],
        [14, 19, 5, 3, 12, 15, 16, 13, 9, 18, 10, 1, 7, 17, 0, 4, 11, 2, 8, 6],
        [11, 7, 14, 13, 3, 17, 9, 8, 0, 5, 4, 19, 6, 15, 10, 16, 2, 12, 1, 18],
        [7, 18, 17, 0, 1, 16, 12, 9, 14, 6, 8, 3, 4, 15, 2, 19, 13, 5, 11, 10],
        [1, 5, 16, 3, 17, 2, 15, 6, 4, 9, 11, 8, 13, 10, 14, 12, 18, 0, 7, 19],
        [1, 0, 16, 10, 8, 14, 2, 17, 6, 5, 11, 13, 4, 9, 15, 12, 7, 19, 3, 18],
        [14, 0, 5, 18, 10, 7, 17, 13, 2, 19, 6, 15, 3, 16, 11, 1, 12, 9, 4, 8],
        [10, 7, 14, 6, 13, 11, 15, 9, 4, 8, 19, 12, 16, 1, 5, 3, 0, 18, 17, 2],
        [0, 5, 10, 2, 1, 8, 9, 4, 12, 6, 11, 18, 3, 7, 13, 16, 19, 17, 14, 15],
        [18, 17, 16, 8, 19, 6, 10, 14, 2, 15, 7, 9, 3, 4, 0, 12, 1, 11, 13, 5],
        [18, 7, 6, 14, 5, 8, 16, 19, 3, 2, 17, 4, 1, 13, 0, 15, 10, 12, 11, 9],
        [19, 1, 11, 17, 7, 3, 4, 6, 18, 16, 15, 9, 12, 5, 0, 8, 10, 2, 13, 14],
        [2, 13, 5, 16, 0, 11, 7, 17, 9, 15, 18, 6, 14, 3, 19, 10, 12, 8, 1, 4],
        [10, 4, 5, 0, 8, 9, 1, 6, 17, 13, 7, 16, 11, 3, 19, 14, 12, 18, 15, 2],
        [17, 10, 12, 7, 19, 2, 15, 9, 0, 11, 3, 5, 8, 14, 4, 1, 16, 6, 18, 13],
        [15, 2, 16, 6, 4, 8, 14, 1, 11, 13, 17, 12, 18, 7, 9, 0, 19, 5, 10, 3],
        [6, 4, 5, 18, 7, 9, 0, 15, 17, 1, 11, 12, 3, 2, 10, 13, 16, 19, 8, 14],
        [5, 14, 0, 8, 11, 6, 4, 15, 16, 3, 13, 2, 19, 9, 7, 18, 17, 1, 10, 12],
        [15, 6, 2, 12, 1, 9, 4, 17, 5, 3, 10, 0, 18, 14, 13, 8, 16, 11, 7, 19],
        [6, 9, 2, 0, 10, 11, 8, 18, 13, 7, 3, 14, 15, 16, 4, 17, 19, 12, 1, 5],
        [0, 1, 7, 9, 12, 2, 6, 16, 5, 3, 19, 10, 4, 13, 8, 15, 17, 11, 18, 14],
        [2, 18, 8, 0, 3, 5, 9, 15, 7, 11, 4, 16, 10, 14, 12, 6, 1, 17, 19, 13],
        [7, 5, 11, 2, 8, 15, 12, 18, 14, 17, 3, 16, 10, 1, 0, 19, 9, 6, 4, 13],
        [15, 16, 7, 3, 9, 1, 17, 0, 14, 8, 2, 10, 19, 6, 11, 13, 18, 4, 12, 5],
        [3, 13, 16, 10, 2, 0, 15, 17, 4, 5, 8, 7, 9, 11, 18, 19, 14, 12, 1, 6],
        [7, 8, 3, 19, 1, 12, 11, 2, 5, 0, 16, 18, 14, 17, 15, 4, 6, 9, 13, 10],
        [1, 19, 12, 8, 10, 14, 11, 9, 2, 18, 0, 5, 13, 7, 6, 15, 4, 17, 16, 3],
        [16, 14, 10, 11, 9, 17, 13, 18, 12, 2, 1, 4, 0, 8, 15, 5, 3, 7, 19, 6],
        [7, 15, 11, 1, 13, 3, 14, 9, 4, 10, 6, 8, 2, 18, 12, 19, 5, 0, 17, 16],
        [8, 1, 10, 3, 12, 17, 15, 7, 16, 9, 4, 5, 19, 11, 2, 6, 13, 0, 18, 14],
        [9, 18, 4, 14, 12, 5, 6, 8, 17, 10, 2, 15, 3, 19, 1, 11, 7, 0, 16, 13],
        [5, 8, 14, 10, 12, 0, 4, 11, 2, 1, 13, 15, 17, 19, 16, 9, 18, 6, 7, 3],
        [3, 15, 9, 5, 18, 7, 1, 17, 12, 0, 6, 19, 11, 14, 4, 8, 16, 13, 10, 2],
        [15, 13, 1, 7, 0, 4, 17, 9, 19, 5, 18, 11, 16, 14, 8, 3, 6, 2, 12, 10],
        [12, 9, 8, 2, 18, 1, 19, 4, 10, 0, 13, 17, 15, 16, 6, 11, 3, 14, 7, 5],
        [17, 18, 14, 8, 12, 5, 11, 2, 1, 15, 7, 16, 10, 6, 13, 9, 0, 3, 4, 19],
        [5, 12, 16, 11, 0, 8, 10, 4, 7, 3, 2, 13, 17, 1, 14, 15, 18, 19, 9, 6],
        [19, 11, 2, 3, 14, 10, 1, 12, 9, 6, 18, 13, 5, 8, 7, 17, 0, 15, 16, 4],
        [9, 8, 4, 1, 5, 12, 16, 19, 3, 10, 15, 14, 2, 6, 11, 18, 13, 0, 7, 17],
        [12, 16, 2, 18, 3, 5, 4, 11, 13, 14, 10, 1, 9, 6, 17, 15, 7, 0, 8, 19],
        [17, 2, 5, 11, 16, 12, 14, 3, 15, 13, 4, 1, 6, 9, 18, 10, 7, 0, 19, 8],
        [18, 13, 1, 3, 0, 14, 12, 6, 11, 8, 15, 16, 7, 19, 9, 10, 4, 2, 17, 5],
        [7, 6, 16, 0, 2, 5, 19, 15, 1, 10, 8, 14, 18, 4, 3, 13, 9, 11, 12, 17],
        [17, 8, 19, 13, 9, 16, 7, 0, 3, 18, 10, 2, 1, 6, 11, 14, 4, 15, 5, 12],
        [1, 10, 7, 0, 15, 16, 17, 9, 13, 5, 2, 3, 6, 11, 12, 14, 8, 18, 19, 4],
        [9, 14, 17, 18, 13, 12, 4, 15, 7, 3, 5, 19, 0, 6, 1, 11, 8, 16, 2, 10],
        [1, 9, 4, 5, 7, 8, 15, 13, 12, 10, 3, 0, 14, 19, 2, 6, 16, 18, 11, 17],
        [1, 8, 16, 19, 9, 2, 12, 17, 0, 10, 5, 3, 11, 18, 15, 4, 6, 13, 14, 7],
        [16, 5, 6, 9, 8, 15, 7, 17, 1, 10, 2, 14, 0, 18, 12, 13, 3, 4, 11, 19],
        [15, 18, 16, 19, 2, 14, 6, 7, 5, 12, 3, 0, 11, 17, 1, 8, 9, 10, 13, 4],
        [12, 18, 15, 11, 8, 7, 3, 1, 2, 5, 17, 16, 10, 14, 13, 9, 4, 19, 0, 6],
        [12, 10, 4, 2, 5, 7, 9, 11, 19, 18, 14, 17, 15, 3, 0, 13, 8, 6, 1, 16],
        [15, 8, 4, 14, 19, 13, 5, 17, 1, 0, 9, 3, 11, 6, 10, 7, 12, 18, 16, 2],
        [12, 3, 6, 10, 18, 14, 11, 15, 0, 17, 1, 13, 4, 9, 19, 5, 2, 16, 7, 8],
        [14, 4, 2, 10, 17, 6, 0, 7, 19, 1, 11, 3, 16, 15, 8, 13, 12, 9, 18, 5],
        [17, 18, 9, 4, 5, 2, 8, 13, 6, 15, 12, 3, 14, 1, 0, 7, 16, 11, 10, 19],
        [12, 11, 3, 1, 0, 18, 8, 16, 14, 19, 13, 10, 9, 4, 17, 5, 2, 7, 6, 15],
        [17, 11, 2, 14, 19, 10, 3, 6, 8, 9, 13, 0, 15, 1, 16, 5, 7, 12, 4, 18],
        [18, 19, 3, 17, 1, 5, 4, 10, 2, 7, 12, 14, 9, 15, 8, 11, 13, 16, 6, 0],
        [11, 0, 13, 14, 19, 3, 7, 4, 6, 10, 2, 5, 8, 12, 9, 17, 15, 16, 18, 1],
        [7, 17, 3, 9, 4, 8, 19, 15, 14, 2, 0, 11, 13, 16, 10, 5, 12, 6, 1, 18],
        [11, 17, 9, 1, 10, 12, 4, 0, 13, 6, 19, 5, 2, 7, 3, 14, 16, 8, 15, 18],
        [15, 0, 2, 9, 3, 7, 6, 12, 17, 4, 19, 14, 18, 5, 11, 1, 16, 8, 10, 13],
        [12, 16, 10, 13, 7, 19, 2, 6, 1, 15, 11, 0, 5, 9, 4, 17, 3, 18, 8, 14],
        [19, 5, 10, 15, 8, 7, 6, 1, 14, 9, 16, 0, 11, 12, 17, 18, 3, 2, 13, 4],
        [10, 13, 9, 14, 18, 5, 19, 15, 3, 8, 6, 4, 7, 1, 17, 11, 12, 0, 2, 16],
        [2, 15, 11, 14, 8, 16, 19, 7, 4, 1, 0, 12, 9, 13, 18, 6, 5, 10, 17, 3],
        [4, 2, 3, 15, 8, 11, 18, 17, 16, 12, 1, 13, 14, 19, 5, 7, 0, 10, 6, 9],
        [12, 0, 4, 8, 19, 6, 5, 10, 9, 15, 7, 18, 3, 14, 2, 13, 11, 17, 16, 1],
        [13, 15, 19, 5, 4, 7, 18, 16, 3, 11, 12, 2, 9, 0, 10, 1, 14, 8, 17, 6],
        [14, 13, 16, 8, 6, 10, 11, 0, 9, 15, 17, 18, 7, 1, 3, 4, 19, 5, 12, 2],
        [6, 3, 12, 13, 2, 15, 0, 10, 19, 18, 9, 1, 7, 17, 4, 5, 11, 16, 8, 14],
        [2, 14, 9, 6, 4, 16, 11, 8, 12, 13, 1, 18, 0, 7, 17, 3, 15, 5, 19, 10],
        [16, 8, 9, 12, 18, 11, 13, 5, 4, 19, 6, 1, 17, 15, 7, 2, 3, 0, 10, 14],
        [15, 16, 11, 18, 14, 10, 5, 0, 7, 3, 6, 8, 9, 12, 1, 17, 2, 4, 19, 13],
        [14, 12, 6, 8, 4, 16, 5, 19, 15, 11, 17, 1, 2, 9, 13, 18, 3, 7, 0, 10],
        [10, 11, 14, 12, 4, 9, 5, 18, 17, 3, 1, 7, 16, 13, 6, 0, 2, 8, 19, 15],
        [16, 6, 3, 15, 7, 4, 12, 9, 8, 13, 2, 10, 1, 19, 14, 0, 18, 5, 11, 17],
        [5, 19, 8, 4, 0, 1, 14, 18, 13, 7, 17, 11, 2, 6, 3, 10, 15, 9, 16, 12],
        [9, 6, 16, 4, 19, 5, 18, 11, 13, 15, 1, 2, 7, 8, 3, 14, 17, 12, 0, 10],
        [4, 6, 5, 7, 8, 0, 17, 9, 13, 19, 12, 14, 11, 16, 1, 3, 10, 2, 18, 15],
        [17, 14, 2, 12, 7, 9, 8, 5, 16, 18, 0, 3, 13, 15, 19, 4, 11, 6, 1, 10],
    ],
    'durations': [
        # Job 0
        [Interval(47, 59), Interval(37, 43), Interval(79, 85), Interval(39, 45), Interval(88, 108),
         Interval(75, 97), Interval(48, 52), Interval(49, 65), Interval(24, 32), Interval(6, 8),
         Interval(12, 14), Interval(23, 25), Interval(52, 70), Interval(52, 56), Interval(88, 106),
         Interval(85, 99), Interval(80, 92), Interval(5, 5), Interval(28, 36), Interval(10, 12)],
        # Job 1
        [Interval(39, 49), Interval(49, 51), Interval(38, 40), Interval(81, 81), Interval(46, 56),
         Interval(91, 93), Interval(63, 67), Interval(19, 21), Interval(68, 82), Interval(59, 61),
         Interval(81, 109), Interval(25, 31), Interval(12, 16), Interval(25, 31), Interval(54, 54),
         Interval(54, 56), Interval(85, 97), Interval(3, 3), Interval(25, 31), Interval(82, 104)],
        # Job 2
        [Interval(52, 52), Interval(61, 73), Interval(57, 71), Interval(78, 88), Interval(34, 40),
         Interval(21, 21), Interval(9, 11), Interval(61, 63), Interval(63, 85), Interval(80, 92),
         Interval(69, 73), Interval(39, 47), Interval(24, 24), Interval(5, 5), Interval(74, 82),
         Interval(9, 11), Interval(39, 41), Interval(51, 51), Interval(77, 101), Interval(52, 56)],
        # Job 3
        [Interval(71, 77), Interval(83, 89), Interval(70, 72), Interval(74, 86), Interval(18, 24),
         Interval(14, 14), Interval(42, 56), Interval(16, 16), Interval(23, 29), Interval(29, 39),
         Interval(2, 2), Interval(16, 18), Interval(44, 50), Interval(62, 74), Interval(18, 24),
         Interval(7, 9), Interval(8, 8), Interval(47, 55), Interval(18, 24), Interval(65, 77)],
        # Job 4
        [Interval(78, 100), Interval(47, 53), Interval(80, 80), Interval(84, 92), Interval(14, 18),
         Interval(55, 61), Interval(17, 23), Interval(29, 35), Interval(41, 43), Interval(79, 99),
         Interval(76, 82), Interval(86, 88), Interval(63, 83), Interval(66, 82), Interval(15, 19),
         Interval(52, 54), Interval(75, 87), Interval(85, 85), Interval(49, 61), Interval(51, 63)],
        # Job 5
        [Interval(72, 74), Interval(5, 5), Interval(25, 27), Interval(50, 64), Interval(42, 48),
         Interval(40, 40), Interval(46, 46), Interval(15, 15), Interval(76, 82), Interval(47, 49),
         Interval(17, 23), Interval(61, 77), Interval(15, 17), Interval(28, 30), Interval(44, 52),
         Interval(37, 39), Interval(6, 6), Interval(18, 18), Interval(57, 67), Interval(82, 90)],
        # Job 6
        [Interval(55, 59), Interval(83, 95), Interval(88, 94), Interval(94, 98), Interval(61, 71),
         Interval(45, 53), Interval(82, 94), Interval(56, 68), Interval(74, 98), Interval(74, 86),
         Interval(12, 14), Interval(54, 62), Interval(80, 82), Interval(67, 73), Interval(42, 54),
         Interval(53, 69), Interval(12, 12), Interval(67, 71), Interval(68, 84), Interval(20, 26)],
        # Job 7
        [Interval(26, 34), Interval(65, 65), Interval(25, 27), Interval(56, 64), Interval(33, 43),
         Interval(64, 68), Interval(76, 76), Interval(73, 97), Interval(37, 41), Interval(95, 97),
         Interval(19, 19), Interval(69, 81), Interval(5, 5), Interval(83, 99), Interval(13, 15),
         Interval(40, 52), Interval(27, 27), Interval(59, 79), Interval(93, 97), Interval(3, 3)],
        # Job 8
        [Interval(1, 1), Interval(99, 99), Interval(87, 107), Interval(15, 19), Interval(45, 57),
         Interval(59, 67), Interval(76, 88), Interval(74, 84), Interval(52, 68), Interval(57, 65),
         Interval(92, 92), Interval(58, 58), Interval(13, 13), Interval(2, 2), Interval(3, 3),
         Interval(72, 76), Interval(37, 49), Interval(31, 37), Interval(6, 6), Interval(1, 1)],
        # Job 9
        [Interval(18, 18), Interval(70, 84), Interval(11, 13), Interval(32, 40), Interval(61, 67),
         Interval(33, 37), Interval(60, 72), Interval(83, 89), Interval(89, 107), Interval(53, 55),
         Interval(10, 12), Interval(41, 41), Interval(15, 15), Interval(78, 96), Interval(66, 86),
         Interval(29, 37), Interval(80, 90), Interval(12, 12), Interval(1, 1), Interval(62, 62)],
        # Job 10
        [Interval(26, 32), Interval(17, 17), Interval(19, 23), Interval(90, 96), Interval(35, 43),
         Interval(46, 50), Interval(45, 47), Interval(56, 64), Interval(9, 9), Interval(55, 67),
         Interval(43, 43), Interval(44, 50), Interval(47, 47), Interval(79, 105), Interval(2, 2),
         Interval(73, 81), Interval(51, 65), Interval(63, 79), Interval(16, 16), Interval(48, 52)],
        # Job 11
        [Interval(87, 95), Interval(42, 42), Interval(31, 33), Interval(93, 99), Interval(51, 65),
         Interval(21, 27), Interval(55, 57), Interval(55, 71), Interval(67, 81), Interval(1, 1),
         Interval(38, 46), Interval(76, 92), Interval(51, 61), Interval(43, 45), Interval(53, 63),
         Interval(1, 1), Interval(5, 5), Interval(47, 59), Interval(44, 44), Interval(52, 52)],
        # Job 12
        [Interval(43, 53), Interval(15, 17), Interval(32, 42), Interval(55, 65), Interval(52, 56),
         Interval(31, 33), Interval(59, 79), Interval(23, 27), Interval(41, 55), Interval(67, 77),
         Interval(75, 79), Interval(28, 30), Interval(60, 68), Interval(10, 10), Interval(51, 55),
         Interval(80, 100), Interval(63, 79), Interval(74, 94), Interval(82, 82), Interval(91, 95)],
        # Job 13
        [Interval(20, 26), Interval(26, 30), Interval(89, 109), Interval(47, 51), Interval(73, 85),
         Interval(6, 8), Interval(30, 34), Interval(88, 90), Interval(11, 13), Interval(22, 22),
         Interval(54, 54), Interval(82, 94), Interval(65, 73), Interval(63, 67), Interval(87, 103),
         Interval(73, 95), Interval(28, 36), Interval(62, 66), Interval(29, 37), Interval(51, 59)],
        # Job 14
        [Interval(90, 104), Interval(49, 49), Interval(10, 12), Interval(79, 79), Interval(75, 97),
         Interval(65, 69), Interval(44, 58), Interval(76, 84), Interval(26, 32), Interval(67, 83),
         Interval(59, 69), Interval(59, 59), Interval(79, 105), Interval(85, 85), Interval(89, 95),
         Interval(3, 3), Interval(94, 94), Interval(62, 76), Interval(29, 39), Interval(26, 28)],
        # Job 15
        [Interval(70, 80), Interval(18, 22), Interval(78, 96), Interval(63, 71), Interval(70, 70),
         Interval(23, 23), Interval(88, 98), Interval(29, 33), Interval(70, 74), Interval(16, 16),
         Interval(31, 41), Interval(5, 5), Interval(56, 62), Interval(69, 81), Interval(80, 90),
         Interval(23, 25), Interval(27, 31), Interval(5, 5), Interval(45, 49), Interval(1, 1)],
        # Job 16
        [Interval(21, 27), Interval(13, 13), Interval(26, 28), Interval(18, 24), Interval(26, 32),
         Interval(19, 19), Interval(86, 96), Interval(34, 40), Interval(89, 97), Interval(67, 85),
         Interval(75, 75), Interval(15, 15), Interval(67, 73), Interval(65, 75), Interval(86, 96),
         Interval(57, 57), Interval(16, 20), Interval(7, 9), Interval(29, 29), Interval(68, 78)],
        # Job 17
        [Interval(15, 17), Interval(14, 16), Interval(72, 80), Interval(1, 1), Interval(80, 106),
         Interval(86, 88), Interval(60, 60), Interval(60, 74), Interval(23, 31), Interval(87, 95),
         Interval(41, 49), Interval(27, 29), Interval(6, 8), Interval(64, 72), Interval(83, 111),
         Interval(6, 6), Interval(47, 53), Interval(65, 77), Interval(46, 58), Interval(98, 100)],
        # Job 18
        [Interval(73, 89), Interval(47, 59), Interval(14, 18), Interval(76, 100), Interval(14, 18),
         Interval(3, 3), Interval(42, 56), Interval(54, 70), Interval(23, 29), Interval(26, 26),
         Interval(38, 48), Interval(30, 32), Interval(71, 79), Interval(31, 39), Interval(68, 76),
         Interval(37, 37), Interval(72, 86), Interval(88, 100), Interval(85, 103), Interval(6, 8)],
        # Job 19
        [Interval(80, 106), Interval(20, 22), Interval(85, 99), Interval(55, 65), Interval(39, 45),
         Interval(8, 10), Interval(80, 106), Interval(65, 71), Interval(27, 29), Interval(26, 32),
         Interval(42, 48), Interval(86, 102), Interval(93, 101), Interval(70, 86), Interval(5, 5),
         Interval(57, 75), Interval(75, 95), Interval(39, 39), Interval(16, 20), Interval(78, 82)],
        # Job 20
        [Interval(42, 44), Interval(32, 34), Interval(19, 23), Interval(59, 67), Interval(50, 62),
         Interval(81, 99), Interval(11, 13), Interval(12, 12), Interval(70, 88), Interval(51, 51),
         Interval(92, 106), Interval(88, 108), Interval(68, 68), Interval(8, 8), Interval(58, 64),
         Interval(38, 44), Interval(55, 61), Interval(8, 8), Interval(37, 47), Interval(9, 9)],
        # Job 21
        [Interval(60, 72), Interval(80, 86), Interval(35, 41), Interval(37, 43), Interval(50, 64),
         Interval(62, 62), Interval(27, 35), Interval(21, 21), Interval(75, 101), Interval(52, 66),
         Interval(79, 85), Interval(90, 102), Interval(63, 75), Interval(10, 12), Interval(47, 51),
         Interval(1, 1), Interval(54, 58), Interval(94, 100), Interval(19, 23), Interval(26, 26)],
        # Job 22
        [Interval(46, 60), Interval(12, 12), Interval(80, 102), Interval(81, 91), Interval(64, 68),
         Interval(73, 97), Interval(2, 2), Interval(75, 81), Interval(20, 26), Interval(25, 31),
         Interval(14, 18), Interval(30, 40), Interval(47, 63), Interval(35, 35), Interval(45, 57),
         Interval(3, 3), Interval(24, 26), Interval(46, 62), Interval(6, 6), Interval(9, 11)],
        # Job 23
        [Interval(10, 10), Interval(54, 72), Interval(3, 3), Interval(63, 71), Interval(77, 87),
         Interval(12, 12), Interval(99, 99), Interval(50, 64), Interval(62, 78), Interval(60, 74),
         Interval(79, 85), Interval(32, 42), Interval(16, 16), Interval(47, 47), Interval(82, 98),
         Interval(65, 77), Interval(72, 76), Interval(64, 86), Interval(30, 32), Interval(63, 75)],
        # Job 24
        [Interval(80, 92), Interval(17, 17), Interval(1, 1), Interval(36, 42), Interval(36, 48),
         Interval(30, 40), Interval(73, 97), Interval(30, 40), Interval(86, 100), Interval(45, 51),
         Interval(22, 22), Interval(72, 80), Interval(22, 28), Interval(37, 47), Interval(59, 71),
         Interval(3, 3), Interval(79, 79), Interval(90, 100), Interval(55, 63), Interval(24, 24)],
        # Job 25
        [Interval(78, 88), Interval(65, 79), Interval(45, 55), Interval(86, 100), Interval(7, 9),
         Interval(7, 7), Interval(70, 88), Interval(51, 63), Interval(92, 98), Interval(68, 68),
         Interval(57, 77), Interval(13, 17), Interval(58, 58), Interval(2, 2), Interval(33, 35),
         Interval(81, 109), Interval(62, 82), Interval(89, 103), Interval(29, 31), Interval(26, 26)],
        # Job 26
        [Interval(11, 11), Interval(22, 22), Interval(72, 90), Interval(55, 71), Interval(89, 101),
         Interval(2, 2), Interval(22, 22), Interval(81, 81), Interval(2, 2), Interval(81, 101),
         Interval(6, 8), Interval(33, 39), Interval(26, 28), Interval(75, 99), Interval(51, 57),
         Interval(24, 24), Interval(4, 4), Interval(80, 108), Interval(7, 7), Interval(24, 28)],
        # Job 27
        [Interval(11, 11), Interval(20, 22), Interval(43, 49), Interval(86, 96), Interval(28, 32),
         Interval(16, 20), Interval(33, 41), Interval(35, 35), Interval(4, 4), Interval(60, 68),
         Interval(9, 9), Interval(53, 61), Interval(49, 53), Interval(38, 44), Interval(82, 98),
         Interval(23, 25), Interval(26, 30), Interval(81, 107), Interval(70, 90), Interval(30, 34)],
        # Job 28
        [Interval(17, 17), Interval(37, 43), Interval(41, 47), Interval(65, 79), Interval(35, 47),
         Interval(29, 33), Interval(81, 91), Interval(6, 8), Interval(54, 66), Interval(39, 43),
         Interval(11, 11), Interval(34, 38), Interval(20, 20), Interval(21, 25), Interval(72, 90),
         Interval(23, 31), Interval(53, 53), Interval(7, 9), Interval(95, 97), Interval(71, 83)],
        # Job 29
        [Interval(34, 44), Interval(40, 40), Interval(32, 42), Interval(61, 79), Interval(12, 14),
         Interval(42, 44), Interval(35, 37), Interval(72, 90), Interval(48, 62), Interval(4, 4),
         Interval(56, 64), Interval(18, 22), Interval(29, 33), Interval(61, 71), Interval(9, 9),
         Interval(22, 22), Interval(6, 6), Interval(83, 85), Interval(84, 104), Interval(13, 17)],
        # Job 30
        [Interval(49, 55), Interval(11, 13), Interval(1, 1), Interval(32, 32), Interval(49, 55),
         Interval(6, 6), Interval(9, 9), Interval(6, 6), Interval(16, 20), Interval(91, 103),
         Interval(77, 87), Interval(12, 12), Interval(56, 68), Interval(43, 43), Interval(87, 89),
         Interval(4, 4), Interval(8, 8), Interval(87, 91), Interval(42, 56), Interval(27, 27)],
        # Job 31
        [Interval(62, 76), Interval(98, 98), Interval(37, 49), Interval(85, 103), Interval(63, 79),
         Interval(78, 86), Interval(37, 47), Interval(79, 103), Interval(20, 20), Interval(45, 59),
         Interval(45, 45), Interval(50, 66), Interval(1, 1), Interval(19, 19), Interval(6, 8),
         Interval(9, 9), Interval(77, 89), Interval(84, 102), Interval(53, 71), Interval(58, 78)],
        # Job 32
        [Interval(6, 6), Interval(75, 81), Interval(50, 60), Interval(62, 62), Interval(1, 1),
         Interval(29, 37), Interval(26, 26), Interval(19, 21), Interval(21, 21), Interval(91, 107),
         Interval(7, 9), Interval(85, 97), Interval(68, 84), Interval(46, 58), Interval(32, 34),
         Interval(14, 16), Interval(62, 82), Interval(34, 34), Interval(34, 34), Interval(82, 110)],
        # Job 33
        [Interval(45, 53), Interval(17, 23), Interval(47, 61), Interval(34, 34), Interval(42, 44),
         Interval(28, 28), Interval(54, 64), Interval(56, 70), Interval(90, 100), Interval(30, 34),
         Interval(22, 24), Interval(26, 30), Interval(40, 54), Interval(41, 49), Interval(27, 29),
         Interval(43, 49), Interval(24, 26), Interval(46, 60), Interval(16, 20), Interval(51, 55)],
        # Job 34
        [Interval(37, 45), Interval(12, 14), Interval(41, 45), Interval(7, 9), Interval(94, 102),
         Interval(72, 78), Interval(70, 72), Interval(51, 69), Interval(18, 22), Interval(15, 15),
         Interval(11, 11), Interval(61, 69), Interval(55, 57), Interval(87, 91), Interval(45, 51),
         Interval(82, 84), Interval(69, 83), Interval(77, 87), Interval(48, 56), Interval(25, 27)],
        # Job 35
        [Interval(38, 42), Interval(18, 22), Interval(55, 71), Interval(9, 11), Interval(23, 23),
         Interval(78, 80), Interval(61, 81), Interval(12, 12), Interval(37, 49), Interval(14, 16),
         Interval(53, 71), Interval(18, 20), Interval(4, 4), Interval(40, 52), Interval(62, 78),
         Interval(86, 88), Interval(40, 50), Interval(22, 26), Interval(27, 33), Interval(76, 76)],
        # Job 36
        [Interval(32, 42), Interval(50, 66), Interval(5, 5), Interval(28, 30), Interval(17, 23),
         Interval(24, 24), Interval(39, 41), Interval(29, 39), Interval(53, 53), Interval(64, 80),
         Interval(12, 12), Interval(25, 27), Interval(12, 12), Interval(37, 43), Interval(64, 84),
         Interval(25, 33), Interval(39, 47), Interval(40, 44), Interval(12, 12), Interval(37, 49)],
        # Job 37
        [Interval(61, 63), Interval(32, 38), Interval(58, 66), Interval(19, 21), Interval(15, 19),
         Interval(43, 45), Interval(91, 97), Interval(6, 6), Interval(82, 84), Interval(81, 89),
         Interval(14, 14), Interval(68, 74), Interval(5, 5), Interval(7, 7), Interval(46, 60),
         Interval(41, 45), Interval(2, 2), Interval(11, 11), Interval(18, 18), Interval(77, 101)],
        # Job 38
        [Interval(60, 76), Interval(94, 94), Interval(84, 90), Interval(29, 39), Interval(9, 11),
         Interval(65, 87), Interval(28, 30), Interval(38, 44), Interval(30, 30), Interval(53, 63),
         Interval(31, 37), Interval(74, 92), Interval(14, 16), Interval(26, 34), Interval(26, 30),
         Interval(23, 25), Interval(38, 42), Interval(1, 1), Interval(64, 80), Interval(71, 93)],
        # Job 39
        [Interval(47, 63), Interval(8, 10), Interval(78, 92), Interval(63, 85), Interval(6, 6),
         Interval(16, 16), Interval(5, 5), Interval(24, 24), Interval(12, 12), Interval(31, 35),
         Interval(30, 30), Interval(31, 37), Interval(31, 37), Interval(17, 17), Interval(70, 80),
         Interval(34, 42), Interval(49, 49), Interval(71, 85), Interval(17, 21), Interval(33, 37)],
        # Job 40
        [Interval(50, 52), Interval(40, 40), Interval(28, 28), Interval(84, 84), Interval(67, 89),
         Interval(90, 96), Interval(38, 40), Interval(14, 14), Interval(50, 64), Interval(51, 53),
         Interval(80, 108), Interval(9, 11), Interval(33, 37), Interval(93, 101), Interval(85, 101),
         Interval(80, 94), Interval(42, 52), Interval(26, 28), Interval(18, 18), Interval(24, 24)],
        # Job 41
        [Interval(42, 44), Interval(9, 9), Interval(58, 68), Interval(11, 11), Interval(25, 27),
         Interval(36, 48), Interval(48, 58), Interval(37, 47), Interval(8, 8), Interval(7, 7),
         Interval(67, 87), Interval(88, 106), Interval(42, 44), Interval(50, 54), Interval(30, 34),
         Interval(20, 26), Interval(30, 34), Interval(45, 55), Interval(86, 112), Interval(77, 89)],
        # Job 42
        [Interval(47, 55), Interval(14, 18), Interval(73, 93), Interval(32, 34), Interval(79, 101),
         Interval(22, 26), Interval(18, 24), Interval(95, 95), Interval(11, 11), Interval(49, 63),
         Interval(20, 22), Interval(32, 42), Interval(70, 74), Interval(5, 5), Interval(93, 95),
         Interval(27, 29), Interval(25, 27), Interval(58, 76), Interval(47, 57), Interval(90, 100)],
        # Job 43
        [Interval(79, 85), Interval(65, 79), Interval(58, 66), Interval(52, 70), Interval(20, 24),
         Interval(17, 19), Interval(65, 67), Interval(28, 28), Interval(82, 94), Interval(48, 48),
         Interval(80, 94), Interval(36, 46), Interval(75, 81), Interval(66, 74), Interval(2, 2),
         Interval(13, 17), Interval(13, 13), Interval(22, 28), Interval(41, 47), Interval(55, 69)],
        # Job 44
        [Interval(24, 32), Interval(24, 24), Interval(48, 64), Interval(73, 81), Interval(21, 21),
         Interval(42, 50), Interval(29, 31), Interval(80, 98), Interval(52, 60), Interval(62, 80),
         Interval(22, 24), Interval(28, 34), Interval(25, 27), Interval(74, 78), Interval(61, 79),
         Interval(81, 105), Interval(76, 96), Interval(69, 79), Interval(74, 84), Interval(52, 62)],
        # Job 45
        [Interval(37, 43), Interval(64, 80), Interval(89, 103), Interval(51, 53), Interval(4, 4),
         Interval(17, 17), Interval(22, 28), Interval(86, 98), Interval(61, 73), Interval(77, 77),
         Interval(58, 66), Interval(10, 12), Interval(3, 3), Interval(66, 84), Interval(20, 22),
         Interval(70, 88), Interval(90, 90), Interval(65, 75), Interval(39, 41), Interval(49, 53)],
        # Job 46
        [Interval(7, 7), Interval(6, 8), Interval(2, 2), Interval(56, 66), Interval(30, 38),
         Interval(43, 49), Interval(7, 7), Interval(21, 23), Interval(36, 36), Interval(33, 39),
         Interval(11, 11), Interval(86, 104), Interval(11, 11), Interval(61, 77), Interval(7, 9),
         Interval(48, 64), Interval(29, 37), Interval(69, 69), Interval(78, 96), Interval(57, 59)],
        # Job 47
        [Interval(30, 32), Interval(10, 12), Interval(5, 5), Interval(14, 16), Interval(51, 51),
         Interval(70, 82), Interval(1, 1), Interval(46, 56), Interval(29, 31), Interval(36, 36),
         Interval(17, 17), Interval(45, 59), Interval(60, 62), Interval(9, 9), Interval(69, 91),
         Interval(10, 10), Interval(70, 80), Interval(58, 74), Interval(31, 33), Interval(12, 16)],
        # Job 48
        [Interval(72, 96), Interval(86, 102), Interval(57, 65), Interval(88, 92), Interval(9, 9),
         Interval(70, 74), Interval(64, 68), Interval(5, 5), Interval(72, 80), Interval(41, 41),
         Interval(75, 99), Interval(78, 82), Interval(44, 56), Interval(42, 48), Interval(82, 108),
         Interval(12, 12), Interval(31, 33), Interval(51, 53), Interval(25, 31), Interval(64, 86)],
        # Job 49
        [Interval(58, 62), Interval(18, 24), Interval(58, 62), Interval(50, 54), Interval(40, 44),
         Interval(43, 51), Interval(76, 78), Interval(82, 104), Interval(25, 29), Interval(62, 62),
         Interval(22, 26), Interval(35, 39), Interval(4, 4), Interval(65, 85), Interval(48, 64),
         Interval(14, 18), Interval(65, 87), Interval(57, 71), Interval(80, 90), Interval(11, 11)],
        # Job 50
        [Interval(21, 21), Interval(9, 11), Interval(74, 100), Interval(42, 52), Interval(40, 40),
         Interval(39, 51), Interval(46, 50), Interval(24, 30), Interval(55, 71), Interval(29, 29),
         Interval(34, 38), Interval(25, 25), Interval(68, 80), Interval(19, 19), Interval(20, 20),
         Interval(76, 80), Interval(48, 54), Interval(29, 35), Interval(64, 74), Interval(22, 24)],
        # Job 51
        [Interval(70, 72), Interval(6, 8), Interval(57, 71), Interval(53, 53), Interval(77, 101),
         Interval(34, 44), Interval(83, 89), Interval(2, 2), Interval(91, 93), Interval(5, 5),
         Interval(49, 55), Interval(54, 72), Interval(27, 27), Interval(70, 80), Interval(45, 47),
         Interval(3, 3), Interval(90, 106), Interval(75, 89), Interval(6, 6), Interval(70, 70)],
        # Job 52
        [Interval(47, 55), Interval(89, 89), Interval(36, 36), Interval(73, 95), Interval(82, 108),
         Interval(11, 13), Interval(90, 104), Interval(70, 80), Interval(53, 61), Interval(71, 87),
         Interval(86, 96), Interval(77, 77), Interval(15, 19), Interval(79, 93), Interval(51, 65),
         Interval(41, 45), Interval(14, 16), Interval(88, 92), Interval(25, 31), Interval(41, 49)],
        # Job 53
        [Interval(3, 3), Interval(29, 33), Interval(71, 71), Interval(51, 51), Interval(6, 6),
         Interval(33, 41), Interval(4, 4), Interval(72, 90), Interval(88, 108), Interval(86, 108),
         Interval(57, 59), Interval(18, 20), Interval(76, 92), Interval(3, 3), Interval(96, 96),
         Interval(44, 56), Interval(19, 23), Interval(81, 91), Interval(44, 44), Interval(69, 83)],
        # Job 54
        [Interval(61, 71), Interval(8, 10), Interval(31, 33), Interval(76, 80), Interval(19, 21),
         Interval(60, 78), Interval(45, 47), Interval(1, 1), Interval(90, 96), Interval(70, 92),
         Interval(18, 18), Interval(61, 67), Interval(38, 42), Interval(37, 41), Interval(76, 96),
         Interval(86, 98), Interval(65, 73), Interval(68, 70), Interval(16, 18), Interval(10, 12)],
        # Job 55
        [Interval(94, 102), Interval(72, 88), Interval(7, 9), Interval(95, 101), Interval(56, 56),
         Interval(42, 52), Interval(26, 26), Interval(29, 31), Interval(46, 52), Interval(51, 59),
         Interval(66, 84), Interval(59, 73), Interval(40, 48), Interval(11, 13), Interval(51, 69),
         Interval(80, 82), Interval(72, 92), Interval(33, 43), Interval(28, 30), Interval(72, 72)],
        # Job 56
        [Interval(47, 63), Interval(16, 20), Interval(30, 34), Interval(78, 78), Interval(89, 101),
         Interval(40, 40), Interval(75, 83), Interval(34, 36), Interval(37, 45), Interval(38, 42),
         Interval(59, 71), Interval(84, 94), Interval(16, 16), Interval(18, 22), Interval(76, 96),
         Interval(52, 66), Interval(49, 49), Interval(81, 91), Interval(35, 37), Interval(25, 25)],
        # Job 57
        [Interval(6, 6), Interval(51, 51), Interval(25, 27), Interval(59, 59), Interval(17, 23),
         Interval(65, 65), Interval(45, 55), Interval(87, 111), Interval(92, 100), Interval(59, 65),
         Interval(45, 49), Interval(89, 89), Interval(34, 44), Interval(61, 75), Interval(28, 28),
         Interval(61, 79), Interval(26, 32), Interval(69, 73), Interval(88, 100), Interval(77, 81)],
        # Job 58
        [Interval(46, 56), Interval(64, 82), Interval(20, 20), Interval(26, 26), Interval(11, 11),
         Interval(43, 49), Interval(31, 39), Interval(75, 99), Interval(74, 94), Interval(91, 99),
         Interval(81, 87), Interval(89, 105), Interval(46, 54), Interval(9, 11), Interval(99, 99),
         Interval(96, 98), Interval(74, 98), Interval(80, 86), Interval(23, 31), Interval(77, 91)],
        # Job 59
        [Interval(54, 62), Interval(24, 24), Interval(87, 111), Interval(75, 85), Interval(71, 85),
         Interval(9, 11), Interval(51, 55), Interval(9, 11), Interval(97, 101), Interval(81, 89),
         Interval(78, 82), Interval(7, 7), Interval(22, 26), Interval(58, 74), Interval(80, 104),
         Interval(69, 79), Interval(87, 109), Interval(9, 9), Interval(27, 33), Interval(24, 32)],
        # Job 60
        [Interval(8, 10), Interval(80, 96), Interval(54, 58), Interval(20, 26), Interval(81, 103),
         Interval(33, 43), Interval(88, 88), Interval(62, 66), Interval(68, 74), Interval(55, 63),
         Interval(10, 12), Interval(32, 32), Interval(70, 72), Interval(62, 62), Interval(25, 29),
         Interval(20, 20), Interval(53, 55), Interval(41, 45), Interval(2, 2), Interval(63, 83)],
        # Job 61
        [Interval(62, 76), Interval(43, 51), Interval(59, 61), Interval(65, 85), Interval(12, 14),
         Interval(20, 24), Interval(16, 16), Interval(54, 66), Interval(87, 87), Interval(78, 82),
         Interval(33, 33), Interval(12, 16), Interval(59, 59), Interval(90, 108), Interval(97, 97),
         Interval(50, 60), Interval(3, 3), Interval(40, 40), Interval(27, 33), Interval(34, 38)],
        # Job 62
        [Interval(55, 57), Interval(2, 2), Interval(29, 33), Interval(69, 71), Interval(87, 97),
         Interval(85, 89), Interval(45, 53), Interval(23, 27), Interval(5, 5), Interval(42, 42),
         Interval(59, 73), Interval(18, 18), Interval(1, 1), Interval(42, 44), Interval(31, 33),
         Interval(46, 46), Interval(47, 49), Interval(18, 22), Interval(10, 12), Interval(20, 26)],
        # Job 63
        [Interval(26, 32), Interval(20, 24), Interval(15, 19), Interval(19, 19), Interval(31, 39),
         Interval(27, 29), Interval(17, 21), Interval(26, 32), Interval(76, 84), Interval(55, 63),
         Interval(75, 97), Interval(88, 102), Interval(34, 38), Interval(74, 84), Interval(76, 88),
         Interval(76, 102), Interval(71, 73), Interval(24, 30), Interval(79, 93), Interval(4, 4)],
        # Job 64
        [Interval(72, 80), Interval(29, 33), Interval(80, 106), Interval(58, 70), Interval(86, 88),
         Interval(77, 91), Interval(54, 70), Interval(36, 46), Interval(6, 6), Interval(34, 38),
         Interval(11, 13), Interval(16, 20), Interval(60, 76), Interval(83, 109), Interval(81, 99),
         Interval(33, 35), Interval(65, 69), Interval(60, 62), Interval(73, 73), Interval(58, 70)],
        # Job 65
        [Interval(41, 41), Interval(27, 29), Interval(38, 40), Interval(32, 36), Interval(36, 36),
         Interval(13, 13), Interval(88, 102), Interval(11, 13), Interval(9, 11), Interval(30, 30),
         Interval(30, 38), Interval(89, 95), Interval(13, 15), Interval(15, 15), Interval(10, 10),
         Interval(96, 100), Interval(66, 84), Interval(55, 69), Interval(12, 12), Interval(88, 88)],
        # Job 66
        [Interval(8, 10), Interval(81, 85), Interval(83, 103), Interval(87, 109), Interval(33, 33),
         Interval(79, 83), Interval(37, 43), Interval(17, 19), Interval(96, 96), Interval(45, 59),
         Interval(45, 57), Interval(94, 104), Interval(34, 34), Interval(46, 46), Interval(29, 31),
         Interval(55, 55), Interval(42, 46), Interval(28, 36), Interval(66, 76), Interval(10, 10)],
        # Job 67
        [Interval(73, 93), Interval(60, 72), Interval(17, 23), Interval(19, 25), Interval(68, 78),
         Interval(75, 77), Interval(54, 64), Interval(73, 75), Interval(21, 25), Interval(77, 103),
         Interval(47, 59), Interval(10, 12), Interval(43, 43), Interval(79, 97), Interval(74, 78),
         Interval(57, 73), Interval(43, 45), Interval(49, 55), Interval(23, 27), Interval(52, 56)],
        # Job 68
        [Interval(76, 80), Interval(79, 103), Interval(41, 41), Interval(47, 61), Interval(58, 78),
         Interval(55, 65), Interval(86, 102), Interval(3, 3), Interval(36, 40), Interval(20, 24),
         Interval(33, 33), Interval(36, 38), Interval(68, 84), Interval(28, 34), Interval(24, 24),
         Interval(41, 51), Interval(18, 22), Interval(61, 77), Interval(49, 57), Interval(55, 59)],
        # Job 69
        [Interval(68, 92), Interval(12, 12), Interval(40, 52), Interval(5, 5), Interval(17, 23),
         Interval(37, 47), Interval(58, 74), Interval(31, 33), Interval(42, 44), Interval(57, 59),
         Interval(56, 70), Interval(84, 94), Interval(46, 62), Interval(78, 80), Interval(26, 30),
         Interval(42, 42), Interval(89, 91), Interval(6, 6), Interval(66, 66), Interval(26, 32)],
        # Job 70
        [Interval(63, 63), Interval(48, 64), Interval(41, 45), Interval(32, 34), Interval(9, 11),
         Interval(52, 54), Interval(2, 2), Interval(24, 24), Interval(6, 6), Interval(54, 68),
         Interval(12, 16), Interval(89, 95), Interval(23, 31), Interval(78, 86), Interval(57, 69),
         Interval(2, 2), Interval(27, 27), Interval(24, 26), Interval(45, 57), Interval(80, 102)],
        # Job 71
        [Interval(22, 24), Interval(54, 70), Interval(40, 48), Interval(28, 36), Interval(61, 77),
         Interval(79, 93), Interval(21, 27), Interval(40, 44), Interval(28, 34), Interval(31, 39),
         Interval(21, 27), Interval(34, 34), Interval(12, 12), Interval(35, 35), Interval(51, 51),
         Interval(65, 81), Interval(5, 5), Interval(12, 12), Interval(51, 53), Interval(12, 14)],
        # Job 72
        [Interval(46, 60), Interval(59, 75), Interval(91, 91), Interval(54, 72), Interval(91, 103),
         Interval(83, 83), Interval(46, 56), Interval(53, 57), Interval(14, 14), Interval(76, 80),
         Interval(16, 18), Interval(68, 80), Interval(9, 9), Interval(56, 70), Interval(22, 22),
         Interval(61, 81), Interval(38, 44), Interval(73, 89), Interval(46, 62), Interval(45, 47)],
        # Job 73
        [Interval(24, 32), Interval(16, 16), Interval(12, 12), Interval(28, 32), Interval(95, 99),
         Interval(74, 98), Interval(8, 10), Interval(62, 68), Interval(48, 54), Interval(29, 31),
         Interval(13, 17), Interval(36, 46), Interval(78, 104), Interval(42, 50), Interval(18, 18),
         Interval(19, 23), Interval(84, 94), Interval(2, 2), Interval(67, 87), Interval(70, 86)],
        # Job 74
        [Interval(80, 102), Interval(29, 37), Interval(82, 86), Interval(74, 84), Interval(4, 4),
         Interval(6, 8), Interval(43, 55), Interval(40, 50), Interval(8, 10), Interval(60, 78),
         Interval(75, 97), Interval(93, 95), Interval(90, 90), Interval(24, 24), Interval(18, 24),
         Interval(14, 16), Interval(38, 38), Interval(25, 31), Interval(25, 27), Interval(54, 66)],
        # Job 75
        [Interval(84, 104), Interval(42, 52), Interval(85, 107), Interval(64, 76), Interval(48, 54),
         Interval(90, 96), Interval(61, 67), Interval(24, 24), Interval(40, 50), Interval(31, 41),
         Interval(59, 65), Interval(90, 92), Interval(16, 20), Interval(33, 43), Interval(41, 53),
         Interval(96, 100), Interval(46, 56), Interval(11, 13), Interval(25, 27), Interval(44, 58)],
        # Job 76
        [Interval(50, 50), Interval(72, 76), Interval(32, 36), Interval(41, 49), Interval(30, 36),
         Interval(46, 54), Interval(67, 71), Interval(14, 14), Interval(82, 96), Interval(82, 90),
         Interval(49, 65), Interval(16, 18), Interval(73, 87), Interval(28, 36), Interval(69, 75),
         Interval(30, 36), Interval(49, 53), Interval(30, 32), Interval(39, 47), Interval(61, 69)],
        # Job 77
        [Interval(14, 14), Interval(4, 4), Interval(19, 25), Interval(25, 29), Interval(50, 66),
         Interval(11, 13), Interval(80, 104), Interval(24, 30), Interval(23, 25), Interval(13, 13),
         Interval(8, 8), Interval(47, 63), Interval(64, 68), Interval(81, 81), Interval(11, 13),
         Interval(13, 13), Interval(57, 57), Interval(67, 87), Interval(24, 26), Interval(89, 109)],
        # Job 78
        [Interval(85, 113), Interval(72, 96), Interval(67, 77), Interval(74, 84), Interval(63, 81),
         Interval(43, 51), Interval(43, 51), Interval(81, 103), Interval(49, 49), Interval(43, 55),
         Interval(40, 46), Interval(32, 34), Interval(27, 33), Interval(14, 18), Interval(32, 38),
         Interval(2, 2), Interval(47, 47), Interval(51, 67), Interval(42, 46), Interval(98, 98)],
        # Job 79
        [Interval(1, 1), Interval(68, 82), Interval(2, 2), Interval(24, 28), Interval(19, 21),
         Interval(46, 62), Interval(55, 71), Interval(30, 32), Interval(44, 44), Interval(97, 99),
         Interval(72, 74), Interval(41, 41), Interval(46, 58), Interval(80, 82), Interval(28, 32),
         Interval(55, 59), Interval(22, 28), Interval(60, 80), Interval(51, 65), Interval(81, 85)],
        # Job 80
        [Interval(19, 23), Interval(14, 16), Interval(53, 67), Interval(26, 34), Interval(47, 53),
         Interval(29, 33), Interval(15, 19), Interval(34, 34), Interval(15, 15), Interval(92, 104),
         Interval(70, 84), Interval(52, 62), Interval(58, 58), Interval(34, 46), Interval(18, 24),
         Interval(24, 26), Interval(37, 45), Interval(72, 84), Interval(40, 48), Interval(24, 28)],
        # Job 81
        [Interval(13, 15), Interval(31, 31), Interval(82, 90), Interval(58, 78), Interval(65, 73),
         Interval(68, 74), Interval(38, 50), Interval(10, 10), Interval(67, 85), Interval(77, 87),
         Interval(54, 54), Interval(37, 43), Interval(46, 46), Interval(43, 51), Interval(38, 46),
         Interval(81, 91), Interval(56, 68), Interval(37, 45), Interval(25, 29), Interval(12, 12)],
        # Job 82
        [Interval(18, 18), Interval(40, 52), Interval(21, 23), Interval(63, 69), Interval(5, 5),
         Interval(11, 13), Interval(23, 31), Interval(76, 88), Interval(24, 24), Interval(51, 69),
         Interval(9, 11), Interval(82, 104), Interval(47, 61), Interval(10, 10), Interval(53, 67),
         Interval(13, 15), Interval(14, 18), Interval(43, 53), Interval(17, 19), Interval(73, 91)],
        # Job 83
        [Interval(84, 84), Interval(15, 15), Interval(54, 64), Interval(41, 49), Interval(61, 65),
         Interval(63, 79), Interval(83, 89), Interval(2, 2), Interval(38, 46), Interval(45, 47),
         Interval(34, 44), Interval(8, 10), Interval(7, 7), Interval(30, 34), Interval(70, 86),
         Interval(11, 13), Interval(71, 85), Interval(58, 78), Interval(70, 84), Interval(85, 95)],
        # Job 84
        [Interval(31, 35), Interval(2, 2), Interval(31, 39), Interval(85, 97), Interval(47, 51),
         Interval(19, 23), Interval(28, 30), Interval(52, 68), Interval(77, 99), Interval(67, 75),
         Interval(14, 14), Interval(6, 6), Interval(35, 45), Interval(53, 53), Interval(2, 2),
         Interval(88, 88), Interval(36, 40), Interval(6, 8), Interval(40, 46), Interval(30, 38)],
        # Job 85
        [Interval(16, 16), Interval(86, 104), Interval(2, 2), Interval(81, 95), Interval(45, 45),
         Interval(93, 93), Interval(67, 87), Interval(9, 11), Interval(66, 76), Interval(66, 72),
         Interval(32, 34), Interval(20, 24), Interval(51, 57), Interval(52, 60), Interval(28, 34),
         Interval(18, 18), Interval(61, 65), Interval(81, 83), Interval(85, 111), Interval(60, 80)],
        # Job 86
        [Interval(13, 17), Interval(42, 42), Interval(44, 44), Interval(74, 86), Interval(14, 16),
         Interval(22, 26), Interval(75, 77), Interval(71, 71), Interval(33, 43), Interval(27, 27),
         Interval(43, 53), Interval(38, 38), Interval(69, 77), Interval(39, 45), Interval(8, 8),
         Interval(48, 56), Interval(20, 20), Interval(35, 45), Interval(48, 54), Interval(93, 105)],
        # Job 87
        [Interval(44, 48), Interval(3, 3), Interval(77, 87), Interval(18, 22), Interval(1, 1),
         Interval(45, 45), Interval(77, 81), Interval(62, 78), Interval(44, 48), Interval(42, 54),
         Interval(60, 66), Interval(81, 93), Interval(40, 54), Interval(41, 45), Interval(1, 1),
         Interval(43, 53), Interval(60, 70), Interval(11, 11), Interval(24, 26), Interval(9, 9)],
        # Job 88
        [Interval(12, 12), Interval(17, 17), Interval(51, 59), Interval(66, 84), Interval(48, 64),
         Interval(89, 89), Interval(6, 6), Interval(40, 52), Interval(19, 25), Interval(43, 45),
         Interval(2, 2), Interval(13, 15), Interval(34, 38), Interval(89, 103), Interval(6, 6),
         Interval(36, 38), Interval(54, 70), Interval(90, 98), Interval(71, 83), Interval(13, 15)],
        # Job 89
        [Interval(36, 38), Interval(27, 29), Interval(15, 17), Interval(74, 86), Interval(10, 10),
         Interval(85, 95), Interval(5, 5), Interval(17, 17), Interval(28, 28), Interval(38, 42),
         Interval(74, 78), Interval(27, 33), Interval(52, 52), Interval(71, 83), Interval(14, 16),
         Interval(44, 56), Interval(86, 112), Interval(90, 108), Interval(62, 66), Interval(62, 64)],
        # Job 90
        [Interval(80, 96), Interval(4, 4), Interval(26, 26), Interval(8, 10), Interval(79, 83),
         Interval(41, 53), Interval(71, 93), Interval(49, 55), Interval(57, 73), Interval(60, 66),
         Interval(37, 37), Interval(59, 59), Interval(69, 87), Interval(48, 54), Interval(71, 79),
         Interval(23, 25), Interval(75, 79), Interval(27, 29), Interval(86, 108), Interval(92, 104)],
        # Job 91
        [Interval(77, 81), Interval(6, 8), Interval(25, 25), Interval(83, 101), Interval(7, 9),
         Interval(87, 93), Interval(72, 92), Interval(9, 9), Interval(50, 56), Interval(85, 105),
         Interval(47, 55), Interval(47, 61), Interval(25, 33), Interval(74, 98), Interval(7, 7),
         Interval(54, 62), Interval(58, 74), Interval(72, 96), Interval(41, 43), Interval(10, 10)],
        # Job 92
        [Interval(5, 5), Interval(45, 59), Interval(64, 76), Interval(54, 64), Interval(9, 11),
         Interval(77, 99), Interval(55, 57), Interval(55, 55), Interval(72, 74), Interval(63, 67),
         Interval(59, 73), Interval(16, 18), Interval(5, 5), Interval(21, 23), Interval(34, 46),
         Interval(38, 46), Interval(1, 1), Interval(49, 53), Interval(86, 104), Interval(28, 28)],
        # Job 93
        [Interval(28, 32), Interval(56, 68), Interval(42, 50), Interval(14, 14), Interval(58, 66),
         Interval(15, 17), Interval(24, 24), Interval(17, 17), Interval(66, 74), Interval(65, 67),
         Interval(52, 62), Interval(51, 59), Interval(78, 80), Interval(98, 100), Interval(27, 27),
         Interval(16, 18), Interval(67, 83), Interval(6, 6), Interval(12, 16), Interval(60, 62)],
        # Job 94
        [Interval(70, 72), Interval(19, 25), Interval(63, 73), Interval(67, 81), Interval(35, 43),
         Interval(58, 78), Interval(25, 31), Interval(7, 7), Interval(62, 72), Interval(7, 7),
         Interval(88, 96), Interval(39, 51), Interval(65, 69), Interval(35, 35), Interval(68, 72),
         Interval(49, 55), Interval(65, 65), Interval(97, 101), Interval(18, 24), Interval(50, 52)],
        # Job 95
        [Interval(5, 5), Interval(63, 83), Interval(10, 10), Interval(68, 82), Interval(16, 16),
         Interval(69, 71), Interval(36, 42), Interval(56, 68), Interval(65, 65), Interval(91, 107),
         Interval(52, 62), Interval(6, 8), Interval(53, 55), Interval(52, 52), Interval(45, 49),
         Interval(41, 45), Interval(1, 1), Interval(63, 67), Interval(80, 96), Interval(34, 38)],
        # Job 96
        [Interval(26, 34), Interval(82, 82), Interval(75, 89), Interval(46, 62), Interval(91, 97),
         Interval(27, 29), Interval(72, 78), Interval(1, 1), Interval(77, 91), Interval(53, 69),
         Interval(17, 17), Interval(39, 51), Interval(68, 76), Interval(51, 65), Interval(70, 86),
         Interval(62, 64), Interval(47, 53), Interval(75, 79), Interval(7, 9), Interval(24, 26)],
        # Job 97
        [Interval(17, 17), Interval(74, 82), Interval(18, 22), Interval(90, 94), Interval(51, 63),
         Interval(85, 105), Interval(24, 26), Interval(40, 48), Interval(7, 9), Interval(80, 106),
         Interval(18, 24), Interval(19, 23), Interval(43, 51), Interval(33, 43), Interval(33, 33),
         Interval(44, 52), Interval(38, 40), Interval(67, 71), Interval(13, 17), Interval(69, 71)],
        # Job 98
        [Interval(2, 2), Interval(4, 4), Interval(39, 49), Interval(36, 40), Interval(91, 95),
         Interval(88, 100), Interval(84, 102), Interval(16, 20), Interval(36, 40), Interval(65, 67),
         Interval(36, 40), Interval(53, 67), Interval(78, 96), Interval(47, 51), Interval(51, 53),
         Interval(64, 80), Interval(12, 12), Interval(5, 5), Interval(21, 21), Interval(6, 6)],
        # Job 99
        [Interval(58, 68), Interval(19, 23), Interval(19, 23), Interval(48, 58), Interval(68, 90),
         Interval(10, 10), Interval(12, 14), Interval(40, 50), Interval(60, 66), Interval(36, 42),
         Interval(37, 39), Interval(47, 53), Interval(80, 80), Interval(43, 47), Interval(84, 84),
         Interval(2, 2), Interval(29, 29), Interval(30, 32), Interval(24, 30), Interval(88, 104)],
    ],
    'name': 'INT__TAI100_20_02.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai100_20_02_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI100_20_02.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI100_20_02.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI100_20_02_F_15_01_INTERVAL_DATA
