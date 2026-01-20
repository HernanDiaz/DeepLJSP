"""
Problema INT__TAI100_20_10.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI100_20_10_F_15_01_INTERVAL_DATA = {
    'num_jobs': 100,
    'num_machines': 20,
    'problem_id': 'int__tai100_20_10.F.15_01_interval',
    'sequences': [
        [9, 12, 4, 7, 16, 0, 1, 18, 17, 5, 14, 11, 8, 10, 3, 15, 13, 2, 19, 6],
        [17, 13, 19, 6, 10, 11, 1, 7, 16, 18, 14, 15, 5, 3, 9, 2, 0, 4, 8, 12],
        [17, 10, 3, 4, 19, 7, 15, 0, 16, 12, 14, 18, 8, 11, 6, 2, 5, 1, 9, 13],
        [9, 19, 3, 10, 1, 5, 16, 14, 7, 17, 18, 13, 4, 0, 11, 15, 8, 12, 2, 6],
        [13, 16, 4, 15, 9, 10, 0, 2, 3, 11, 17, 5, 19, 7, 18, 6, 1, 12, 14, 8],
        [16, 7, 9, 6, 13, 5, 18, 11, 17, 19, 14, 15, 10, 0, 4, 12, 2, 1, 3, 8],
        [14, 5, 1, 10, 9, 13, 16, 17, 2, 18, 19, 12, 15, 6, 0, 3, 7, 4, 11, 8],
        [1, 11, 10, 3, 17, 9, 14, 18, 0, 4, 15, 16, 6, 12, 7, 5, 13, 8, 19, 2],
        [2, 17, 8, 19, 10, 13, 15, 12, 16, 1, 18, 6, 11, 0, 14, 3, 9, 7, 5, 4],
        [3, 17, 11, 0, 5, 15, 13, 12, 16, 10, 2, 6, 4, 9, 19, 8, 1, 7, 18, 14],
        [2, 8, 14, 5, 15, 13, 10, 19, 12, 9, 4, 0, 6, 3, 18, 7, 16, 11, 1, 17],
        [1, 13, 8, 3, 7, 14, 9, 6, 10, 15, 19, 11, 4, 16, 2, 0, 18, 17, 5, 12],
        [5, 0, 7, 1, 4, 8, 10, 3, 13, 9, 11, 17, 12, 14, 15, 6, 2, 19, 16, 18],
        [7, 19, 5, 6, 9, 14, 8, 4, 3, 15, 1, 10, 11, 12, 2, 16, 0, 13, 17, 18],
        [2, 18, 0, 13, 6, 16, 5, 19, 14, 9, 7, 3, 1, 10, 17, 8, 4, 11, 12, 15],
        [12, 11, 1, 17, 4, 13, 16, 18, 6, 7, 8, 10, 2, 14, 5, 3, 9, 19, 0, 15],
        [11, 8, 10, 17, 3, 14, 1, 9, 13, 5, 19, 4, 18, 6, 16, 12, 7, 0, 2, 15],
        [2, 7, 15, 0, 17, 18, 10, 3, 16, 11, 19, 13, 9, 14, 12, 5, 8, 1, 4, 6],
        [16, 12, 15, 11, 5, 3, 2, 8, 0, 6, 10, 7, 9, 18, 17, 19, 4, 14, 13, 1],
        [1, 14, 19, 0, 10, 16, 15, 7, 17, 18, 3, 4, 13, 8, 5, 9, 6, 11, 2, 12],
        [12, 9, 2, 15, 14, 8, 17, 6, 1, 11, 10, 5, 16, 13, 4, 3, 0, 7, 18, 19],
        [11, 17, 18, 12, 19, 14, 8, 10, 15, 7, 2, 1, 4, 16, 13, 9, 0, 6, 3, 5],
        [18, 12, 17, 8, 5, 10, 6, 9, 13, 0, 2, 15, 7, 4, 16, 1, 14, 11, 3, 19],
        [9, 12, 8, 18, 5, 2, 15, 11, 0, 6, 1, 4, 17, 3, 13, 7, 14, 19, 10, 16],
        [18, 16, 17, 11, 6, 8, 1, 7, 12, 10, 3, 9, 14, 0, 19, 2, 5, 4, 15, 13],
        [17, 15, 6, 4, 7, 1, 0, 13, 9, 19, 18, 5, 3, 10, 2, 16, 11, 8, 14, 12],
        [3, 15, 7, 8, 10, 9, 2, 17, 19, 14, 16, 5, 1, 18, 12, 11, 0, 4, 13, 6],
        [3, 17, 12, 9, 4, 10, 15, 13, 0, 11, 8, 2, 1, 5, 19, 7, 16, 18, 6, 14],
        [19, 16, 18, 13, 5, 11, 8, 9, 0, 2, 14, 17, 10, 4, 6, 1, 3, 12, 7, 15],
        [18, 8, 2, 6, 12, 17, 19, 10, 9, 15, 5, 1, 3, 7, 14, 13, 11, 4, 0, 16],
        [12, 13, 1, 3, 18, 17, 15, 6, 5, 9, 11, 16, 14, 10, 0, 8, 4, 7, 2, 19],
        [7, 8, 13, 0, 16, 12, 15, 17, 6, 4, 11, 18, 10, 9, 2, 14, 5, 19, 1, 3],
        [11, 17, 19, 7, 6, 12, 16, 9, 13, 0, 2, 15, 10, 5, 4, 1, 18, 14, 3, 8],
        [6, 8, 9, 17, 16, 4, 10, 14, 18, 2, 7, 19, 5, 0, 3, 11, 13, 1, 15, 12],
        [16, 8, 3, 4, 13, 1, 2, 9, 10, 7, 12, 6, 17, 5, 0, 18, 11, 19, 15, 14],
        [7, 11, 2, 15, 16, 4, 18, 0, 17, 13, 19, 10, 9, 12, 1, 6, 14, 8, 3, 5],
        [12, 6, 0, 17, 5, 10, 13, 8, 1, 16, 4, 7, 11, 19, 18, 2, 9, 14, 3, 15],
        [2, 8, 7, 10, 17, 6, 13, 3, 19, 18, 9, 12, 11, 14, 1, 16, 5, 4, 15, 0],
        [10, 3, 1, 15, 14, 11, 13, 2, 16, 4, 8, 18, 12, 9, 5, 7, 19, 0, 17, 6],
        [8, 14, 19, 2, 18, 17, 16, 5, 6, 13, 10, 3, 7, 0, 4, 12, 9, 1, 15, 11],
        [9, 1, 19, 6, 4, 17, 13, 7, 15, 8, 0, 2, 10, 16, 14, 18, 5, 3, 12, 11],
        [8, 7, 4, 14, 18, 16, 19, 15, 2, 10, 6, 12, 9, 5, 0, 1, 13, 3, 17, 11],
        [2, 9, 18, 7, 16, 13, 14, 15, 10, 17, 11, 3, 5, 0, 8, 12, 4, 19, 1, 6],
        [6, 2, 16, 10, 18, 0, 17, 19, 3, 5, 7, 14, 9, 12, 15, 8, 4, 13, 1, 11],
        [10, 0, 12, 1, 6, 14, 18, 11, 7, 16, 9, 8, 4, 15, 13, 19, 5, 3, 2, 17],
        [14, 5, 4, 19, 9, 8, 3, 12, 1, 0, 15, 18, 17, 13, 10, 6, 11, 7, 16, 2],
        [2, 13, 17, 11, 4, 9, 15, 1, 7, 0, 5, 12, 16, 14, 8, 10, 3, 6, 19, 18],
        [2, 5, 14, 10, 1, 7, 3, 18, 19, 6, 4, 8, 17, 12, 15, 0, 11, 13, 16, 9],
        [4, 13, 10, 15, 14, 12, 18, 11, 1, 5, 17, 9, 2, 16, 0, 8, 19, 6, 3, 7],
        [3, 17, 4, 13, 8, 15, 19, 7, 6, 11, 12, 14, 1, 10, 9, 0, 5, 18, 16, 2],
        [11, 8, 0, 13, 5, 7, 10, 9, 2, 4, 1, 12, 17, 6, 18, 15, 14, 19, 3, 16],
        [3, 11, 15, 8, 10, 6, 5, 18, 2, 9, 19, 16, 14, 17, 12, 4, 7, 1, 13, 0],
        [10, 18, 3, 8, 2, 12, 11, 13, 6, 14, 19, 1, 16, 17, 0, 7, 4, 15, 9, 5],
        [3, 14, 0, 4, 5, 7, 13, 6, 15, 17, 12, 10, 1, 9, 11, 2, 18, 8, 16, 19],
        [2, 8, 7, 9, 19, 16, 17, 15, 6, 3, 4, 13, 10, 12, 0, 5, 14, 18, 1, 11],
        [18, 12, 11, 7, 17, 8, 13, 15, 9, 14, 16, 5, 2, 10, 19, 3, 1, 0, 6, 4],
        [0, 7, 2, 16, 17, 4, 13, 1, 9, 10, 11, 14, 15, 3, 5, 6, 12, 8, 19, 18],
        [3, 13, 18, 9, 17, 12, 14, 19, 7, 10, 0, 11, 5, 8, 2, 4, 16, 1, 6, 15],
        [7, 18, 10, 5, 8, 13, 2, 16, 3, 14, 1, 4, 19, 9, 15, 0, 11, 17, 12, 6],
        [6, 12, 8, 0, 4, 16, 5, 19, 11, 2, 14, 13, 7, 18, 3, 10, 9, 1, 17, 15],
        [8, 17, 15, 10, 6, 3, 5, 1, 9, 2, 13, 11, 14, 7, 12, 18, 0, 4, 19, 16],
        [2, 7, 17, 10, 5, 12, 13, 18, 0, 15, 4, 1, 9, 8, 6, 11, 19, 3, 14, 16],
        [15, 5, 4, 19, 8, 13, 3, 0, 14, 1, 12, 11, 10, 17, 9, 2, 18, 7, 6, 16],
        [10, 16, 19, 6, 2, 5, 0, 1, 9, 4, 8, 12, 3, 17, 14, 7, 13, 15, 11, 18],
        [17, 4, 3, 11, 6, 12, 18, 14, 9, 19, 7, 15, 10, 0, 5, 13, 1, 2, 16, 8],
        [19, 1, 4, 6, 14, 2, 3, 8, 16, 11, 18, 13, 10, 15, 7, 9, 5, 12, 0, 17],
        [16, 17, 11, 1, 8, 6, 7, 13, 18, 4, 3, 0, 10, 9, 2, 14, 19, 5, 12, 15],
        [8, 3, 1, 14, 13, 7, 19, 10, 0, 17, 12, 2, 4, 16, 18, 6, 5, 9, 15, 11],
        [13, 16, 4, 17, 7, 19, 6, 3, 2, 12, 11, 10, 1, 14, 9, 15, 0, 8, 5, 18],
        [6, 17, 7, 14, 5, 4, 3, 10, 1, 12, 8, 15, 2, 18, 11, 9, 16, 13, 19, 0],
        [11, 6, 10, 4, 8, 18, 0, 16, 2, 17, 5, 14, 1, 15, 13, 7, 3, 9, 19, 12],
        [7, 17, 15, 1, 12, 9, 5, 14, 0, 2, 4, 11, 13, 18, 16, 3, 19, 6, 10, 8],
        [11, 16, 10, 17, 18, 5, 13, 19, 7, 14, 12, 15, 4, 9, 2, 3, 1, 6, 8, 0],
        [2, 13, 19, 4, 6, 7, 10, 18, 14, 17, 12, 16, 11, 8, 15, 5, 9, 0, 1, 3],
        [16, 11, 3, 10, 18, 14, 1, 7, 6, 17, 19, 15, 2, 0, 8, 13, 4, 12, 9, 5],
        [5, 13, 0, 1, 3, 6, 17, 19, 4, 2, 8, 9, 16, 7, 10, 11, 18, 12, 14, 15],
        [18, 17, 5, 10, 8, 9, 0, 11, 12, 2, 19, 14, 16, 1, 6, 15, 4, 3, 7, 13],
        [8, 15, 1, 6, 2, 19, 16, 17, 0, 10, 12, 5, 9, 13, 4, 14, 3, 11, 18, 7],
        [7, 8, 3, 17, 14, 5, 1, 11, 9, 15, 4, 12, 16, 6, 10, 2, 13, 19, 18, 0],
        [18, 15, 8, 16, 13, 6, 11, 4, 10, 2, 3, 1, 19, 7, 12, 9, 0, 14, 17, 5],
        [11, 3, 10, 17, 19, 16, 5, 6, 13, 9, 8, 14, 12, 18, 1, 15, 2, 4, 7, 0],
        [11, 8, 5, 13, 18, 16, 1, 3, 7, 6, 9, 14, 10, 2, 4, 19, 15, 17, 0, 12],
        [17, 19, 8, 0, 4, 1, 11, 3, 13, 16, 9, 10, 5, 14, 2, 18, 12, 7, 15, 6],
        [6, 5, 1, 18, 7, 0, 19, 16, 2, 12, 14, 17, 3, 10, 8, 4, 15, 13, 9, 11],
        [2, 17, 7, 12, 0, 14, 4, 19, 15, 10, 8, 1, 6, 3, 18, 5, 9, 11, 16, 13],
        [16, 12, 0, 2, 14, 5, 6, 3, 17, 15, 18, 10, 11, 7, 9, 1, 8, 19, 4, 13],
        [9, 3, 11, 18, 15, 1, 19, 16, 13, 17, 0, 5, 14, 10, 12, 4, 2, 8, 6, 7],
        [16, 14, 2, 11, 5, 13, 17, 19, 8, 15, 9, 10, 1, 12, 7, 4, 6, 3, 18, 0],
        [7, 9, 16, 2, 14, 3, 5, 6, 18, 19, 13, 8, 15, 17, 0, 12, 11, 10, 4, 1],
        [5, 18, 13, 10, 8, 14, 9, 12, 4, 2, 7, 11, 19, 6, 1, 17, 0, 15, 3, 16],
        [6, 11, 8, 0, 1, 2, 15, 7, 12, 14, 18, 5, 16, 10, 19, 17, 4, 3, 9, 13],
        [7, 10, 16, 9, 5, 15, 12, 6, 3, 2, 0, 19, 18, 8, 11, 4, 17, 1, 13, 14],
        [15, 18, 19, 0, 10, 12, 14, 9, 1, 3, 17, 2, 8, 6, 13, 16, 7, 5, 11, 4],
        [13, 19, 7, 4, 6, 18, 12, 1, 17, 16, 2, 14, 3, 5, 15, 0, 11, 9, 10, 8],
        [0, 3, 8, 12, 9, 16, 2, 6, 19, 14, 5, 17, 11, 15, 4, 1, 18, 7, 10, 13],
        [11, 9, 19, 3, 1, 7, 2, 4, 18, 6, 15, 17, 16, 14, 10, 0, 12, 8, 13, 5],
        [10, 5, 9, 8, 3, 1, 0, 4, 7, 15, 11, 19, 18, 13, 14, 17, 2, 12, 16, 6],
        [6, 10, 4, 19, 2, 13, 12, 11, 8, 9, 17, 0, 1, 7, 14, 15, 3, 16, 5, 18],
        [11, 9, 8, 16, 13, 7, 19, 5, 10, 3, 18, 2, 14, 17, 12, 4, 0, 6, 1, 15],
        [11, 12, 9, 7, 15, 18, 16, 8, 19, 4, 1, 17, 13, 5, 0, 14, 2, 6, 10, 3],
    ],
    'durations': [
        # Job 0
        [Interval(47, 61), Interval(80, 94), Interval(59, 63), Interval(33, 37), Interval(5, 5),
         Interval(43, 53), Interval(29, 37), Interval(20, 22), Interval(56, 74), Interval(72, 94),
         Interval(71, 85), Interval(13, 15), Interval(67, 73), Interval(22, 28), Interval(35, 37),
         Interval(51, 61), Interval(80, 94), Interval(30, 34), Interval(82, 110), Interval(53, 71)],
        # Job 1
        [Interval(60, 76), Interval(15, 15), Interval(21, 23), Interval(53, 53), Interval(30, 36),
         Interval(60, 62), Interval(71, 75), Interval(61, 65), Interval(87, 105), Interval(60, 62),
         Interval(75, 101), Interval(78, 94), Interval(48, 58), Interval(2, 2), Interval(26, 32),
         Interval(14, 14), Interval(48, 50), Interval(13, 15), Interval(20, 24), Interval(59, 73)],
        # Job 2
        [Interval(68, 68), Interval(64, 76), Interval(75, 93), Interval(18, 20), Interval(30, 34),
         Interval(58, 58), Interval(78, 96), Interval(80, 84), Interval(6, 8), Interval(43, 51),
         Interval(66, 70), Interval(65, 77), Interval(3, 3), Interval(90, 96), Interval(23, 25),
         Interval(28, 34), Interval(19, 19), Interval(56, 56), Interval(76, 100), Interval(69, 73)],
        # Job 3
        [Interval(56, 60), Interval(70, 74), Interval(50, 52), Interval(39, 45), Interval(27, 35),
         Interval(61, 65), Interval(42, 56), Interval(81, 85), Interval(25, 31), Interval(79, 105),
         Interval(76, 90), Interval(7, 7), Interval(6, 8), Interval(26, 34), Interval(12, 16),
         Interval(25, 29), Interval(54, 62), Interval(28, 36), Interval(15, 17), Interval(58, 76)],
        # Job 4
        [Interval(34, 38), Interval(51, 51), Interval(62, 68), Interval(34, 46), Interval(75, 83),
         Interval(34, 44), Interval(30, 36), Interval(76, 78), Interval(75, 93), Interval(65, 71),
         Interval(70, 72), Interval(46, 62), Interval(36, 44), Interval(83, 105), Interval(54, 58),
         Interval(87, 101), Interval(55, 55), Interval(9, 11), Interval(12, 14), Interval(13, 13)],
        # Job 5
        [Interval(48, 54), Interval(23, 31), Interval(29, 33), Interval(64, 66), Interval(26, 26),
         Interval(61, 63), Interval(85, 91), Interval(67, 71), Interval(40, 54), Interval(32, 40),
         Interval(3, 3), Interval(85, 95), Interval(86, 94), Interval(29, 33), Interval(24, 24),
         Interval(34, 36), Interval(22, 26), Interval(64, 72), Interval(18, 18), Interval(66, 74)],
        # Job 6
        [Interval(8, 8), Interval(6, 6), Interval(91, 95), Interval(55, 65), Interval(62, 74),
         Interval(30, 34), Interval(85, 105), Interval(15, 19), Interval(12, 12), Interval(69, 89),
         Interval(72, 84), Interval(26, 26), Interval(15, 15), Interval(73, 93), Interval(7, 9),
         Interval(29, 33), Interval(5, 5), Interval(6, 6), Interval(35, 37), Interval(67, 83)],
        # Job 7
        [Interval(36, 46), Interval(83, 107), Interval(4, 4), Interval(97, 99), Interval(21, 23),
         Interval(60, 68), Interval(35, 47), Interval(54, 58), Interval(23, 23), Interval(62, 82),
         Interval(10, 10), Interval(35, 35), Interval(53, 57), Interval(16, 18), Interval(9, 11),
         Interval(30, 34), Interval(66, 86), Interval(48, 50), Interval(81, 109), Interval(14, 14)],
        # Job 8
        [Interval(96, 96), Interval(21, 25), Interval(40, 48), Interval(17, 21), Interval(84, 96),
         Interval(6, 6), Interval(62, 72), Interval(35, 39), Interval(56, 72), Interval(75, 85),
         Interval(98, 98), Interval(66, 66), Interval(69, 79), Interval(63, 67), Interval(3, 3),
         Interval(13, 17), Interval(46, 54), Interval(97, 99), Interval(42, 50), Interval(69, 91)],
        # Job 9
        [Interval(1, 1), Interval(58, 72), Interval(35, 37), Interval(33, 37), Interval(86, 104),
         Interval(95, 103), Interval(74, 90), Interval(45, 47), Interval(23, 29), Interval(35, 35),
         Interval(96, 96), Interval(6, 6), Interval(25, 31), Interval(80, 104), Interval(11, 13),
         Interval(40, 44), Interval(44, 50), Interval(78, 78), Interval(9, 11), Interval(73, 79)],
        # Job 10
        [Interval(71, 85), Interval(96, 102), Interval(79, 101), Interval(44, 48), Interval(69, 73),
         Interval(71, 81), Interval(43, 47), Interval(87, 105), Interval(58, 58), Interval(3, 3),
         Interval(66, 74), Interval(80, 80), Interval(26, 34), Interval(81, 89), Interval(83, 103),
         Interval(14, 18), Interval(26, 26), Interval(76, 82), Interval(42, 46), Interval(21, 21)],
        # Job 11
        [Interval(79, 85), Interval(16, 16), Interval(49, 63), Interval(30, 40), Interval(79, 83),
         Interval(85, 109), Interval(5, 5), Interval(61, 75), Interval(54, 66), Interval(30, 36),
         Interval(52, 62), Interval(41, 43), Interval(66, 78), Interval(68, 86), Interval(53, 53),
         Interval(26, 26), Interval(60, 72), Interval(75, 87), Interval(72, 96), Interval(78, 90)],
        # Job 12
        [Interval(28, 30), Interval(6, 6), Interval(37, 39), Interval(82, 110), Interval(79, 91),
         Interval(31, 41), Interval(66, 76), Interval(5, 5), Interval(52, 54), Interval(11, 11),
         Interval(81, 93), Interval(99, 99), Interval(41, 43), Interval(61, 77), Interval(65, 83),
         Interval(30, 38), Interval(25, 25), Interval(10, 10), Interval(22, 28), Interval(30, 34)],
        # Job 13
        [Interval(35, 45), Interval(70, 76), Interval(73, 87), Interval(60, 80), Interval(7, 7),
         Interval(35, 35), Interval(31, 39), Interval(20, 20), Interval(68, 68), Interval(27, 31),
         Interval(7, 7), Interval(12, 12), Interval(64, 76), Interval(40, 54), Interval(41, 51),
         Interval(75, 81), Interval(24, 32), Interval(44, 52), Interval(46, 54), Interval(22, 22)],
        # Job 14
        [Interval(82, 106), Interval(79, 79), Interval(1, 1), Interval(34, 44), Interval(32, 34),
         Interval(81, 107), Interval(65, 73), Interval(18, 20), Interval(26, 32), Interval(31, 35),
         Interval(72, 72), Interval(41, 55), Interval(88, 88), Interval(9, 9), Interval(1, 1),
         Interval(99, 99), Interval(18, 22), Interval(25, 33), Interval(79, 87), Interval(41, 47)],
        # Job 15
        [Interval(4, 4), Interval(16, 20), Interval(8, 10), Interval(77, 87), Interval(59, 59),
         Interval(62, 66), Interval(53, 59), Interval(73, 83), Interval(23, 23), Interval(61, 61),
         Interval(69, 91), Interval(86, 96), Interval(35, 41), Interval(84, 94), Interval(80, 90),
         Interval(22, 24), Interval(46, 50), Interval(80, 100), Interval(28, 30), Interval(93, 101)],
        # Job 16
        [Interval(9, 11), Interval(8, 10), Interval(81, 83), Interval(27, 29), Interval(44, 52),
         Interval(63, 69), Interval(19, 25), Interval(32, 32), Interval(33, 35), Interval(41, 45),
         Interval(59, 69), Interval(41, 45), Interval(24, 24), Interval(77, 99), Interval(40, 48),
         Interval(15, 15), Interval(26, 30), Interval(51, 57), Interval(85, 103), Interval(75, 85)],
        # Job 17
        [Interval(43, 57), Interval(53, 55), Interval(27, 27), Interval(62, 76), Interval(29, 39),
         Interval(5, 5), Interval(21, 23), Interval(26, 32), Interval(45, 49), Interval(22, 26),
         Interval(49, 55), Interval(23, 29), Interval(48, 54), Interval(53, 63), Interval(44, 56),
         Interval(83, 85), Interval(13, 17), Interval(82, 104), Interval(2, 2), Interval(14, 18)],
        # Job 18
        [Interval(61, 81), Interval(23, 27), Interval(2, 2), Interval(64, 86), Interval(54, 70),
         Interval(70, 88), Interval(35, 35), Interval(77, 97), Interval(19, 19), Interval(48, 52),
         Interval(30, 36), Interval(74, 84), Interval(62, 64), Interval(8, 10), Interval(23, 25),
         Interval(36, 42), Interval(2, 2), Interval(17, 23), Interval(72, 96), Interval(51, 55)],
        # Job 19
        [Interval(72, 84), Interval(10, 12), Interval(39, 45), Interval(54, 66), Interval(65, 87),
         Interval(55, 59), Interval(28, 30), Interval(46, 54), Interval(73, 85), Interval(74, 88),
         Interval(19, 19), Interval(22, 26), Interval(79, 103), Interval(51, 63), Interval(79, 81),
         Interval(66, 82), Interval(97, 101), Interval(4, 4), Interval(60, 64), Interval(2, 2)],
        # Job 20
        [Interval(4, 4), Interval(62, 68), Interval(38, 46), Interval(91, 103), Interval(50, 62),
         Interval(83, 101), Interval(43, 55), Interval(81, 85), Interval(16, 20), Interval(86, 86),
         Interval(44, 52), Interval(22, 26), Interval(42, 42), Interval(99, 99), Interval(83, 91),
         Interval(55, 63), Interval(21, 23), Interval(34, 34), Interval(55, 71), Interval(45, 45)],
        # Job 21
        [Interval(49, 59), Interval(62, 66), Interval(72, 88), Interval(47, 55), Interval(66, 84),
         Interval(42, 42), Interval(52, 68), Interval(33, 33), Interval(6, 6), Interval(77, 103),
         Interval(29, 35), Interval(74, 80), Interval(11, 11), Interval(57, 69), Interval(37, 43),
         Interval(29, 31), Interval(36, 38), Interval(60, 64), Interval(86, 102), Interval(8, 8)],
        # Job 22
        [Interval(6, 6), Interval(66, 88), Interval(74, 78), Interval(20, 26), Interval(57, 65),
         Interval(88, 92), Interval(6, 6), Interval(73, 97), Interval(44, 46), Interval(74, 98),
         Interval(9, 11), Interval(61, 81), Interval(12, 14), Interval(59, 77), Interval(16, 16),
         Interval(30, 36), Interval(90, 100), Interval(45, 59), Interval(76, 100), Interval(39, 39)],
        # Job 23
        [Interval(40, 54), Interval(28, 32), Interval(63, 71), Interval(95, 103), Interval(52, 52),
         Interval(25, 33), Interval(20, 26), Interval(7, 9), Interval(75, 79), Interval(69, 91),
         Interval(46, 46), Interval(54, 54), Interval(59, 69), Interval(41, 49), Interval(17, 17),
         Interval(11, 13), Interval(34, 36), Interval(3, 3), Interval(74, 88), Interval(14, 16)],
        # Job 24
        [Interval(24, 24), Interval(46, 54), Interval(40, 54), Interval(76, 100), Interval(58, 78),
         Interval(36, 48), Interval(2, 2), Interval(22, 26), Interval(2, 2), Interval(59, 67),
         Interval(88, 88), Interval(68, 76), Interval(25, 31), Interval(42, 52), Interval(28, 34),
         Interval(62, 62), Interval(56, 62), Interval(6, 6), Interval(8, 10), Interval(59, 61)],
        # Job 25
        [Interval(64, 72), Interval(74, 90), Interval(20, 24), Interval(41, 47), Interval(47, 63),
         Interval(24, 26), Interval(40, 50), Interval(67, 83), Interval(13, 13), Interval(84, 84),
         Interval(15, 19), Interval(57, 77), Interval(21, 21), Interval(6, 6), Interval(48, 50),
         Interval(57, 77), Interval(6, 8), Interval(69, 79), Interval(28, 30), Interval(20, 20)],
        # Job 26
        [Interval(69, 77), Interval(2, 2), Interval(26, 26), Interval(13, 17), Interval(25, 33),
         Interval(41, 47), Interval(26, 26), Interval(98, 100), Interval(77, 95), Interval(51, 67),
         Interval(12, 14), Interval(86, 94), Interval(12, 14), Interval(16, 18), Interval(67, 69),
         Interval(75, 101), Interval(41, 43), Interval(56, 66), Interval(63, 67), Interval(70, 74)],
        # Job 27
        [Interval(3, 3), Interval(1, 1), Interval(37, 43), Interval(31, 35), Interval(27, 31),
         Interval(37, 47), Interval(12, 14), Interval(15, 15), Interval(74, 82), Interval(36, 38),
         Interval(28, 32), Interval(88, 96), Interval(45, 53), Interval(83, 99), Interval(40, 44),
         Interval(69, 79), Interval(46, 60), Interval(52, 66), Interval(52, 60), Interval(31, 33)],
        # Job 28
        [Interval(29, 33), Interval(78, 90), Interval(26, 32), Interval(65, 85), Interval(63, 73),
         Interval(12, 12), Interval(26, 32), Interval(46, 56), Interval(71, 81), Interval(95, 101),
         Interval(31, 35), Interval(97, 101), Interval(26, 30), Interval(15, 19), Interval(76, 102),
         Interval(4, 4), Interval(21, 21), Interval(76, 92), Interval(89, 91), Interval(4, 4)],
        # Job 29
        [Interval(5, 5), Interval(64, 74), Interval(17, 21), Interval(45, 45), Interval(30, 40),
         Interval(77, 101), Interval(37, 43), Interval(37, 39), Interval(29, 31), Interval(47, 57),
         Interval(64, 82), Interval(7, 7), Interval(41, 49), Interval(56, 64), Interval(40, 46),
         Interval(55, 55), Interval(10, 10), Interval(95, 99), Interval(84, 102), Interval(55, 71)],
        # Job 30
        [Interval(71, 81), Interval(56, 66), Interval(21, 21), Interval(38, 44), Interval(74, 74),
         Interval(45, 57), Interval(34, 38), Interval(46, 52), Interval(25, 27), Interval(28, 34),
         Interval(67, 67), Interval(68, 70), Interval(6, 6), Interval(52, 56), Interval(64, 66),
         Interval(6, 8), Interval(70, 70), Interval(41, 49), Interval(32, 32), Interval(22, 28)],
        # Job 31
        [Interval(1, 1), Interval(63, 75), Interval(24, 32), Interval(24, 26), Interval(23, 27),
         Interval(21, 27), Interval(72, 76), Interval(41, 55), Interval(4, 4), Interval(12, 12),
         Interval(68, 92), Interval(28, 28), Interval(67, 83), Interval(79, 85), Interval(31, 37),
         Interval(89, 109), Interval(17, 21), Interval(51, 67), Interval(10, 10), Interval(10, 12)],
        # Job 32
        [Interval(46, 46), Interval(70, 92), Interval(62, 66), Interval(26, 30), Interval(87, 91),
         Interval(65, 77), Interval(25, 33), Interval(25, 29), Interval(72, 90), Interval(30, 38),
         Interval(76, 80), Interval(6, 8), Interval(44, 58), Interval(25, 25), Interval(47, 47),
         Interval(12, 16), Interval(30, 34), Interval(40, 54), Interval(79, 101), Interval(31, 31)],
        # Job 33
        [Interval(4, 4), Interval(39, 41), Interval(32, 32), Interval(48, 56), Interval(33, 41),
         Interval(33, 37), Interval(79, 91), Interval(25, 27), Interval(42, 48), Interval(50, 66),
         Interval(38, 46), Interval(72, 78), Interval(13, 13), Interval(14, 16), Interval(75, 97),
         Interval(65, 83), Interval(93, 103), Interval(17, 21), Interval(41, 49), Interval(57, 63)],
        # Job 34
        [Interval(39, 49), Interval(63, 67), Interval(5, 5), Interval(29, 31), Interval(51, 51),
         Interval(36, 48), Interval(78, 98), Interval(78, 80), Interval(46, 48), Interval(43, 49),
         Interval(61, 63), Interval(49, 51), Interval(54, 62), Interval(81, 83), Interval(46, 56),
         Interval(84, 94), Interval(81, 97), Interval(59, 67), Interval(57, 61), Interval(76, 92)],
        # Job 35
        [Interval(44, 56), Interval(52, 70), Interval(35, 37), Interval(14, 14), Interval(56, 74),
         Interval(80, 92), Interval(74, 100), Interval(26, 30), Interval(43, 57), Interval(8, 8),
         Interval(86, 112), Interval(65, 81), Interval(95, 97), Interval(83, 105), Interval(79, 95),
         Interval(61, 75), Interval(96, 96), Interval(59, 79), Interval(17, 21), Interval(32, 34)],
        # Job 36
        [Interval(71, 91), Interval(81, 81), Interval(29, 29), Interval(47, 61), Interval(24, 24),
         Interval(49, 61), Interval(5, 5), Interval(36, 36), Interval(46, 50), Interval(38, 44),
         Interval(32, 36), Interval(29, 37), Interval(42, 54), Interval(33, 41), Interval(31, 33),
         Interval(32, 36), Interval(45, 59), Interval(27, 27), Interval(74, 86), Interval(13, 15)],
        # Job 37
        [Interval(35, 37), Interval(28, 34), Interval(7, 7), Interval(85, 91), Interval(98, 100),
         Interval(52, 58), Interval(11, 11), Interval(62, 68), Interval(47, 47), Interval(16, 20),
         Interval(44, 48), Interval(38, 40), Interval(78, 78), Interval(40, 52), Interval(71, 91),
         Interval(31, 31), Interval(78, 82), Interval(30, 40), Interval(82, 102), Interval(44, 58)],
        # Job 38
        [Interval(62, 68), Interval(43, 49), Interval(31, 31), Interval(3, 3), Interval(19, 23),
         Interval(50, 60), Interval(10, 12), Interval(5, 5), Interval(37, 43), Interval(45, 59),
         Interval(93, 105), Interval(11, 11), Interval(35, 37), Interval(73, 93), Interval(80, 104),
         Interval(5, 5), Interval(17, 21), Interval(50, 66), Interval(43, 51), Interval(29, 39)],
        # Job 39
        [Interval(48, 52), Interval(56, 56), Interval(57, 57), Interval(25, 29), Interval(20, 20),
         Interval(24, 28), Interval(66, 76), Interval(58, 60), Interval(13, 15), Interval(41, 51),
         Interval(22, 22), Interval(60, 72), Interval(18, 22), Interval(31, 35), Interval(38, 40),
         Interval(33, 33), Interval(86, 86), Interval(30, 30), Interval(32, 42), Interval(75, 79)],
        # Job 40
        [Interval(1, 1), Interval(49, 53), Interval(76, 78), Interval(63, 81), Interval(85, 89),
         Interval(43, 57), Interval(80, 108), Interval(79, 89), Interval(8, 8), Interval(66, 80),
         Interval(12, 14), Interval(11, 13), Interval(92, 102), Interval(84, 88), Interval(62, 64),
         Interval(43, 45), Interval(14, 14), Interval(61, 73), Interval(19, 19), Interval(50, 54)],
        # Job 41
        [Interval(19, 25), Interval(5, 5), Interval(46, 56), Interval(16, 20), Interval(22, 24),
         Interval(93, 101), Interval(80, 102), Interval(79, 93), Interval(13, 13), Interval(26, 28),
         Interval(62, 74), Interval(38, 50), Interval(86, 100), Interval(74, 90), Interval(15, 19),
         Interval(45, 51), Interval(90, 106), Interval(27, 33), Interval(76, 96), Interval(88, 96)],
        # Job 42
        [Interval(5, 5), Interval(81, 103), Interval(9, 11), Interval(54, 72), Interval(41, 41),
         Interval(26, 26), Interval(12, 16), Interval(28, 32), Interval(3, 3), Interval(8, 10),
         Interval(96, 102), Interval(54, 54), Interval(13, 15), Interval(91, 105), Interval(20, 26),
         Interval(10, 12), Interval(63, 69), Interval(46, 50), Interval(23, 27), Interval(74, 84)],
        # Job 43
        [Interval(71, 93), Interval(45, 55), Interval(81, 91), Interval(19, 19), Interval(70, 70),
         Interval(71, 81), Interval(98, 100), Interval(31, 37), Interval(48, 58), Interval(22, 24),
         Interval(84, 94), Interval(73, 91), Interval(18, 20), Interval(48, 62), Interval(14, 16),
         Interval(20, 26), Interval(87, 111), Interval(63, 63), Interval(1, 1), Interval(64, 86)],
        # Job 44
        [Interval(41, 45), Interval(25, 25), Interval(36, 44), Interval(17, 19), Interval(39, 47),
         Interval(80, 92), Interval(65, 85), Interval(23, 25), Interval(72, 92), Interval(23, 25),
         Interval(70, 72), Interval(78, 100), Interval(57, 77), Interval(24, 32), Interval(90, 102),
         Interval(19, 21), Interval(13, 15), Interval(79, 91), Interval(53, 65), Interval(35, 41)],
        # Job 45
        [Interval(27, 29), Interval(8, 8), Interval(88, 110), Interval(8, 8), Interval(49, 57),
         Interval(51, 51), Interval(86, 98), Interval(52, 70), Interval(70, 88), Interval(69, 77),
         Interval(70, 90), Interval(24, 24), Interval(51, 59), Interval(71, 75), Interval(53, 57),
         Interval(9, 9), Interval(58, 74), Interval(20, 24), Interval(85, 105), Interval(55, 65)],
        # Job 46
        [Interval(14, 14), Interval(85, 93), Interval(24, 24), Interval(34, 40), Interval(30, 30),
         Interval(80, 96), Interval(1, 1), Interval(15, 15), Interval(12, 16), Interval(32, 40),
         Interval(12, 16), Interval(54, 70), Interval(3, 3), Interval(27, 27), Interval(40, 48),
         Interval(49, 51), Interval(60, 66), Interval(24, 28), Interval(86, 96), Interval(85, 85)],
        # Job 47
        [Interval(22, 26), Interval(67, 81), Interval(40, 44), Interval(43, 43), Interval(57, 59),
         Interval(25, 33), Interval(57, 59), Interval(50, 58), Interval(66, 86), Interval(21, 23),
         Interval(39, 45), Interval(69, 91), Interval(44, 46), Interval(25, 31), Interval(28, 36),
         Interval(55, 63), Interval(1, 1), Interval(76, 86), Interval(47, 49), Interval(15, 15)],
        # Job 48
        [Interval(87, 93), Interval(20, 20), Interval(84, 92), Interval(84, 84), Interval(34, 44),
         Interval(6, 6), Interval(12, 12), Interval(12, 16), Interval(18, 20), Interval(38, 50),
         Interval(10, 10), Interval(26, 26), Interval(6, 6), Interval(74, 76), Interval(22, 26),
         Interval(33, 43), Interval(51, 55), Interval(33, 41), Interval(67, 71), Interval(44, 48)],
        # Job 49
        [Interval(51, 57), Interval(72, 84), Interval(20, 20), Interval(58, 74), Interval(2, 2),
         Interval(48, 56), Interval(47, 47), Interval(78, 90), Interval(26, 30), Interval(10, 12),
         Interval(57, 75), Interval(40, 50), Interval(7, 9), Interval(20, 24), Interval(13, 15),
         Interval(30, 32), Interval(86, 90), Interval(63, 83), Interval(18, 24), Interval(63, 77)],
        # Job 50
        [Interval(36, 36), Interval(25, 33), Interval(63, 67), Interval(29, 35), Interval(69, 89),
         Interval(2, 2), Interval(42, 42), Interval(90, 100), Interval(32, 34), Interval(5, 5),
         Interval(57, 67), Interval(45, 49), Interval(20, 20), Interval(2, 2), Interval(2, 2),
         Interval(35, 37), Interval(21, 23), Interval(87, 105), Interval(56, 66), Interval(81, 89)],
        # Job 51
        [Interval(27, 27), Interval(20, 24), Interval(53, 67), Interval(87, 87), Interval(26, 34),
         Interval(55, 73), Interval(72, 78), Interval(26, 26), Interval(24, 26), Interval(65, 87),
         Interval(28, 28), Interval(50, 56), Interval(63, 67), Interval(55, 63), Interval(84, 100),
         Interval(54, 54), Interval(85, 99), Interval(28, 28), Interval(20, 20), Interval(41, 55)],
        # Job 52
        [Interval(50, 64), Interval(12, 14), Interval(86, 100), Interval(44, 50), Interval(37, 43),
         Interval(72, 90), Interval(84, 94), Interval(52, 52), Interval(50, 66), Interval(18, 22),
         Interval(17, 21), Interval(36, 38), Interval(64, 74), Interval(1, 1), Interval(13, 13),
         Interval(54, 66), Interval(74, 92), Interval(33, 37), Interval(64, 64), Interval(73, 73)],
        # Job 53
        [Interval(57, 69), Interval(77, 95), Interval(32, 40), Interval(75, 95), Interval(89, 93),
         Interval(12, 12), Interval(42, 50), Interval(52, 52), Interval(61, 79), Interval(23, 27),
         Interval(47, 53), Interval(41, 41), Interval(4, 4), Interval(8, 10), Interval(33, 39),
         Interval(88, 110), Interval(55, 59), Interval(89, 93), Interval(92, 100), Interval(37, 49)],
        # Job 54
        [Interval(15, 15), Interval(81, 87), Interval(64, 82), Interval(93, 93), Interval(49, 53),
         Interval(14, 14), Interval(24, 26), Interval(66, 84), Interval(37, 41), Interval(13, 15),
         Interval(43, 43), Interval(70, 76), Interval(73, 91), Interval(2, 2), Interval(69, 75),
         Interval(60, 72), Interval(26, 34), Interval(62, 66), Interval(19, 19), Interval(56, 70)],
        # Job 55
        [Interval(37, 39), Interval(71, 77), Interval(56, 62), Interval(64, 74), Interval(52, 68),
         Interval(89, 109), Interval(12, 16), Interval(42, 54), Interval(8, 10), Interval(49, 51),
         Interval(73, 93), Interval(74, 96), Interval(72, 76), Interval(10, 10), Interval(81, 109),
         Interval(9, 11), Interval(75, 85), Interval(92, 92), Interval(87, 97), Interval(39, 39)],
        # Job 56
        [Interval(46, 50), Interval(73, 77), Interval(17, 19), Interval(62, 68), Interval(10, 12),
         Interval(30, 34), Interval(61, 61), Interval(42, 50), Interval(19, 25), Interval(1, 1),
         Interval(33, 43), Interval(33, 33), Interval(74, 82), Interval(38, 40), Interval(66, 68),
         Interval(79, 79), Interval(63, 69), Interval(99, 99), Interval(19, 25), Interval(66, 66)],
        # Job 57
        [Interval(78, 94), Interval(83, 107), Interval(29, 31), Interval(18, 20), Interval(86, 94),
         Interval(65, 65), Interval(69, 89), Interval(21, 25), Interval(69, 69), Interval(70, 92),
         Interval(27, 33), Interval(9, 9), Interval(93, 105), Interval(84, 88), Interval(60, 72),
         Interval(54, 70), Interval(32, 32), Interval(94, 100), Interval(24, 26), Interval(35, 39)],
        # Job 58
        [Interval(38, 46), Interval(58, 76), Interval(74, 94), Interval(53, 57), Interval(73, 79),
         Interval(44, 52), Interval(88, 102), Interval(52, 66), Interval(69, 69), Interval(53, 53),
         Interval(56, 74), Interval(29, 31), Interval(80, 108), Interval(78, 92), Interval(14, 16),
         Interval(94, 98), Interval(60, 76), Interval(1, 1), Interval(28, 32), Interval(85, 103)],
        # Job 59
        [Interval(25, 31), Interval(72, 80), Interval(2, 2), Interval(76, 96), Interval(57, 59),
         Interval(38, 42), Interval(14, 14), Interval(32, 32), Interval(10, 12), Interval(12, 14),
         Interval(1, 1), Interval(49, 63), Interval(86, 98), Interval(12, 14), Interval(83, 87),
         Interval(13, 17), Interval(63, 85), Interval(46, 56), Interval(4, 4), Interval(60, 72)],
        # Job 60
        [Interval(50, 54), Interval(64, 82), Interval(50, 64), Interval(12, 14), Interval(52, 52),
         Interval(47, 51), Interval(37, 39), Interval(13, 15), Interval(75, 99), Interval(63, 63),
         Interval(77, 79), Interval(40, 40), Interval(12, 14), Interval(23, 23), Interval(41, 43),
         Interval(94, 104), Interval(57, 77), Interval(25, 31), Interval(60, 70), Interval(91, 93)],
        # Job 61
        [Interval(78, 102), Interval(54, 64), Interval(78, 94), Interval(29, 31), Interval(30, 38),
         Interval(79, 79), Interval(76, 78), Interval(9, 9), Interval(75, 93), Interval(73, 73),
         Interval(8, 10), Interval(44, 44), Interval(39, 47), Interval(59, 59), Interval(6, 6),
         Interval(81, 99), Interval(3, 3), Interval(18, 20), Interval(4, 4), Interval(33, 33)],
        # Job 62
        [Interval(31, 37), Interval(18, 18), Interval(24, 26), Interval(50, 52), Interval(19, 23),
         Interval(84, 102), Interval(22, 22), Interval(50, 62), Interval(77, 83), Interval(75, 79),
         Interval(65, 69), Interval(88, 90), Interval(15, 15), Interval(54, 66), Interval(13, 17),
         Interval(68, 92), Interval(21, 25), Interval(81, 99), Interval(76, 96), Interval(17, 17)],
        # Job 63
        [Interval(18, 24), Interval(58, 64), Interval(22, 28), Interval(81, 101), Interval(63, 71),
         Interval(79, 89), Interval(13, 17), Interval(55, 63), Interval(33, 37), Interval(5, 5),
         Interval(36, 40), Interval(8, 10), Interval(46, 62), Interval(57, 59), Interval(32, 40),
         Interval(33, 39), Interval(65, 73), Interval(6, 8), Interval(19, 25), Interval(5, 5)],
        # Job 64
        [Interval(3, 3), Interval(66, 80), Interval(36, 36), Interval(69, 81), Interval(83, 107),
         Interval(63, 79), Interval(10, 10), Interval(6, 8), Interval(12, 14), Interval(30, 36),
         Interval(34, 44), Interval(27, 33), Interval(80, 84), Interval(74, 78), Interval(67, 69),
         Interval(37, 37), Interval(56, 68), Interval(44, 44), Interval(6, 6), Interval(50, 52)],
        # Job 65
        [Interval(84, 90), Interval(29, 33), Interval(28, 28), Interval(65, 71), Interval(6, 8),
         Interval(76, 94), Interval(52, 62), Interval(81, 83), Interval(88, 108), Interval(16, 16),
         Interval(12, 12), Interval(27, 29), Interval(5, 5), Interval(55, 57), Interval(77, 79),
         Interval(6, 8), Interval(16, 20), Interval(7, 7), Interval(9, 9), Interval(14, 16)],
        # Job 66
        [Interval(8, 8), Interval(2, 2), Interval(44, 56), Interval(45, 57), Interval(95, 99),
         Interval(84, 88), Interval(68, 76), Interval(85, 99), Interval(29, 29), Interval(50, 66),
         Interval(9, 11), Interval(13, 13), Interval(25, 25), Interval(42, 42), Interval(11, 11),
         Interval(46, 46), Interval(71, 77), Interval(76, 96), Interval(18, 22), Interval(30, 32)],
        # Job 67
        [Interval(38, 48), Interval(4, 4), Interval(28, 34), Interval(87, 109), Interval(33, 43),
         Interval(13, 13), Interval(9, 9), Interval(80, 94), Interval(67, 69), Interval(50, 58),
         Interval(64, 86), Interval(33, 41), Interval(10, 12), Interval(58, 58), Interval(42, 50),
         Interval(48, 50), Interval(6, 6), Interval(13, 17), Interval(27, 29), Interval(81, 91)],
        # Job 68
        [Interval(72, 88), Interval(87, 93), Interval(46, 48), Interval(23, 29), Interval(9, 9),
         Interval(9, 11), Interval(16, 20), Interval(87, 103), Interval(18, 20), Interval(49, 55),
         Interval(15, 19), Interval(55, 55), Interval(72, 76), Interval(22, 26), Interval(77, 93),
         Interval(40, 40), Interval(54, 70), Interval(55, 65), Interval(86, 106), Interval(88, 104)],
        # Job 69
        [Interval(29, 31), Interval(64, 86), Interval(59, 59), Interval(19, 25), Interval(4, 4),
         Interval(46, 58), Interval(86, 108), Interval(34, 44), Interval(47, 51), Interval(36, 36),
         Interval(90, 92), Interval(70, 88), Interval(16, 18), Interval(33, 43), Interval(4, 4),
         Interval(56, 58), Interval(41, 47), Interval(46, 46), Interval(17, 17), Interval(66, 66)],
        # Job 70
        [Interval(3, 3), Interval(63, 77), Interval(95, 95), Interval(19, 25), Interval(68, 76),
         Interval(37, 41), Interval(88, 104), Interval(91, 97), Interval(47, 47), Interval(31, 39),
         Interval(33, 41), Interval(57, 61), Interval(39, 51), Interval(83, 91), Interval(90, 108),
         Interval(33, 33), Interval(46, 50), Interval(4, 4), Interval(81, 103), Interval(59, 77)],
        # Job 71
        [Interval(18, 18), Interval(65, 83), Interval(80, 96), Interval(52, 68), Interval(7, 9),
         Interval(42, 48), Interval(1, 1), Interval(72, 94), Interval(68, 74), Interval(70, 86),
         Interval(64, 78), Interval(45, 59), Interval(36, 36), Interval(17, 19), Interval(12, 12),
         Interval(92, 94), Interval(64, 80), Interval(35, 39), Interval(31, 33), Interval(25, 31)],
        # Job 72
        [Interval(40, 52), Interval(71, 89), Interval(12, 12), Interval(37, 49), Interval(71, 81),
         Interval(83, 83), Interval(67, 81), Interval(42, 46), Interval(93, 101), Interval(45, 47),
         Interval(28, 32), Interval(51, 61), Interval(75, 83), Interval(30, 38), Interval(55, 57),
         Interval(42, 56), Interval(2, 2), Interval(58, 68), Interval(37, 45), Interval(75, 99)],
        # Job 73
        [Interval(52, 54), Interval(30, 40), Interval(97, 99), Interval(19, 19), Interval(20, 24),
         Interval(31, 31), Interval(76, 102), Interval(83, 105), Interval(26, 28), Interval(86, 98),
         Interval(77, 83), Interval(51, 69), Interval(19, 25), Interval(27, 35), Interval(21, 25),
         Interval(5, 5), Interval(38, 42), Interval(5, 5), Interval(80, 100), Interval(13, 13)],
        # Job 74
        [Interval(28, 36), Interval(39, 47), Interval(65, 85), Interval(13, 17), Interval(36, 38),
         Interval(5, 5), Interval(60, 68), Interval(4, 4), Interval(28, 32), Interval(25, 33),
         Interval(12, 16), Interval(30, 40), Interval(74, 96), Interval(65, 85), Interval(45, 45),
         Interval(45, 45), Interval(2, 2), Interval(7, 7), Interval(25, 33), Interval(61, 75)],
        # Job 75
        [Interval(94, 96), Interval(10, 12), Interval(5, 5), Interval(19, 21), Interval(44, 54),
         Interval(14, 18), Interval(45, 55), Interval(9, 11), Interval(14, 16), Interval(59, 67),
         Interval(94, 100), Interval(9, 9), Interval(87, 89), Interval(56, 72), Interval(11, 13),
         Interval(90, 100), Interval(19, 19), Interval(14, 18), Interval(47, 61), Interval(8, 10)],
        # Job 76
        [Interval(51, 53), Interval(30, 36), Interval(14, 18), Interval(10, 10), Interval(74, 100),
         Interval(62, 62), Interval(74, 78), Interval(84, 92), Interval(20, 24), Interval(56, 70),
         Interval(46, 54), Interval(84, 90), Interval(16, 16), Interval(52, 60), Interval(36, 40),
         Interval(49, 65), Interval(48, 56), Interval(65, 77), Interval(13, 17), Interval(17, 19)],
        # Job 77
        [Interval(79, 99), Interval(31, 33), Interval(73, 81), Interval(60, 72), Interval(83, 93),
         Interval(6, 6), Interval(37, 37), Interval(30, 40), Interval(45, 53), Interval(43, 57),
         Interval(78, 100), Interval(53, 71), Interval(25, 31), Interval(29, 33), Interval(58, 64),
         Interval(39, 43), Interval(61, 81), Interval(2, 2), Interval(22, 22), Interval(9, 9)],
        # Job 78
        [Interval(29, 35), Interval(20, 20), Interval(77, 77), Interval(61, 79), Interval(22, 24),
         Interval(73, 91), Interval(44, 58), Interval(64, 86), Interval(32, 36), Interval(52, 58),
         Interval(79, 103), Interval(45, 53), Interval(42, 50), Interval(70, 90), Interval(6, 6),
         Interval(69, 69), Interval(61, 79), Interval(93, 105), Interval(83, 87), Interval(41, 49)],
        # Job 79
        [Interval(28, 36), Interval(25, 29), Interval(43, 43), Interval(46, 60), Interval(67, 73),
         Interval(17, 17), Interval(52, 62), Interval(71, 83), Interval(87, 95), Interval(42, 56),
         Interval(6, 6), Interval(6, 6), Interval(41, 53), Interval(88, 98), Interval(4, 4),
         Interval(54, 54), Interval(92, 94), Interval(67, 69), Interval(48, 48), Interval(82, 104)],
        # Job 80
        [Interval(16, 16), Interval(5, 5), Interval(37, 41), Interval(76, 82), Interval(45, 57),
         Interval(34, 44), Interval(34, 44), Interval(32, 32), Interval(35, 41), Interval(27, 29),
         Interval(86, 106), Interval(30, 40), Interval(53, 59), Interval(39, 45), Interval(40, 50),
         Interval(83, 83), Interval(42, 42), Interval(37, 43), Interval(23, 27), Interval(3, 3)],
        # Job 81
        [Interval(70, 84), Interval(1, 1), Interval(11, 11), Interval(75, 99), Interval(18, 24),
         Interval(42, 46), Interval(84, 100), Interval(71, 83), Interval(8, 10), Interval(82, 102),
         Interval(10, 10), Interval(31, 31), Interval(59, 65), Interval(56, 74), Interval(41, 47),
         Interval(74, 82), Interval(19, 25), Interval(13, 13), Interval(23, 29), Interval(67, 77)],
        # Job 82
        [Interval(11, 11), Interval(43, 49), Interval(8, 8), Interval(71, 83), Interval(28, 34),
         Interval(45, 51), Interval(34, 40), Interval(89, 109), Interval(25, 29), Interval(92, 106),
         Interval(31, 31), Interval(64, 82), Interval(57, 63), Interval(38, 42), Interval(72, 90),
         Interval(8, 10), Interval(18, 22), Interval(80, 82), Interval(61, 81), Interval(2, 2)],
        # Job 83
        [Interval(51, 69), Interval(17, 23), Interval(54, 70), Interval(18, 18), Interval(16, 20),
         Interval(31, 35), Interval(33, 43), Interval(43, 53), Interval(35, 39), Interval(69, 87),
         Interval(76, 76), Interval(28, 28), Interval(59, 71), Interval(56, 66), Interval(39, 41),
         Interval(25, 31), Interval(64, 70), Interval(4, 4), Interval(16, 18), Interval(26, 26)],
        # Job 84
        [Interval(46, 62), Interval(77, 101), Interval(64, 74), Interval(86, 100), Interval(62, 76),
         Interval(81, 105), Interval(49, 59), Interval(26, 34), Interval(13, 15), Interval(13, 15),
         Interval(66, 76), Interval(44, 54), Interval(10, 10), Interval(83, 89), Interval(79, 97),
         Interval(65, 69), Interval(15, 19), Interval(2, 2), Interval(2, 2), Interval(17, 23)],
        # Job 85
        [Interval(51, 57), Interval(79, 87), Interval(52, 66), Interval(70, 70), Interval(18, 18),
         Interval(32, 36), Interval(6, 8), Interval(2, 2), Interval(42, 48), Interval(6, 6),
         Interval(71, 89), Interval(20, 22), Interval(65, 79), Interval(74, 86), Interval(88, 90),
         Interval(52, 52), Interval(29, 37), Interval(36, 46), Interval(71, 81), Interval(5, 5)],
        # Job 86
        [Interval(51, 55), Interval(14, 16), Interval(69, 81), Interval(10, 10), Interval(45, 51),
         Interval(48, 60), Interval(1, 1), Interval(43, 43), Interval(22, 22), Interval(31, 31),
         Interval(54, 72), Interval(1, 1), Interval(58, 78), Interval(66, 82), Interval(23, 23),
         Interval(32, 32), Interval(50, 56), Interval(66, 76), Interval(84, 102), Interval(22, 22)],
        # Job 87
        [Interval(21, 21), Interval(45, 57), Interval(56, 56), Interval(35, 43), Interval(32, 32),
         Interval(16, 18), Interval(34, 40), Interval(21, 21), Interval(39, 45), Interval(80, 82),
         Interval(50, 62), Interval(27, 31), Interval(11, 11), Interval(74, 82), Interval(38, 42),
         Interval(59, 73), Interval(57, 57), Interval(90, 94), Interval(5, 5), Interval(34, 42)],
        # Job 88
        [Interval(29, 31), Interval(27, 35), Interval(87, 97), Interval(25, 27), Interval(48, 64),
         Interval(63, 71), Interval(78, 98), Interval(10, 12), Interval(25, 25), Interval(23, 25),
         Interval(94, 102), Interval(8, 8), Interval(34, 34), Interval(17, 19), Interval(70, 90),
         Interval(70, 94), Interval(28, 28), Interval(75, 99), Interval(66, 88), Interval(14, 14)],
        # Job 89
        [Interval(36, 44), Interval(40, 46), Interval(79, 91), Interval(81, 87), Interval(66, 86),
         Interval(62, 66), Interval(6, 8), Interval(47, 55), Interval(49, 53), Interval(15, 15),
         Interval(89, 103), Interval(29, 33), Interval(83, 87), Interval(29, 31), Interval(84, 86),
         Interval(45, 45), Interval(69, 77), Interval(71, 75), Interval(15, 19), Interval(57, 57)],
        # Job 90
        [Interval(3, 3), Interval(30, 34), Interval(85, 99), Interval(85, 109), Interval(68, 88),
         Interval(75, 91), Interval(36, 38), Interval(40, 42), Interval(4, 4), Interval(56, 68),
         Interval(16, 16), Interval(32, 40), Interval(4, 4), Interval(26, 26), Interval(25, 31),
         Interval(2, 2), Interval(14, 18), Interval(35, 39), Interval(81, 105), Interval(25, 27)],
        # Job 91
        [Interval(63, 65), Interval(90, 90), Interval(77, 99), Interval(30, 34), Interval(13, 13),
         Interval(67, 73), Interval(5, 5), Interval(29, 31), Interval(43, 45), Interval(73, 91),
         Interval(92, 104), Interval(43, 45), Interval(61, 73), Interval(24, 24), Interval(44, 54),
         Interval(87, 111), Interval(9, 9), Interval(24, 32), Interval(91, 101), Interval(65, 75)],
        # Job 92
        [Interval(75, 91), Interval(27, 31), Interval(23, 31), Interval(67, 89), Interval(73, 97),
         Interval(10, 10), Interval(72, 82), Interval(79, 103), Interval(21, 27), Interval(94, 100),
         Interval(19, 19), Interval(46, 62), Interval(36, 44), Interval(36, 42), Interval(41, 51),
         Interval(78, 100), Interval(82, 84), Interval(92, 94), Interval(52, 54), Interval(87, 93)],
        # Job 93
        [Interval(68, 84), Interval(52, 60), Interval(37, 43), Interval(63, 83), Interval(12, 16),
         Interval(70, 78), Interval(68, 82), Interval(54, 56), Interval(84, 96), Interval(7, 9),
         Interval(8, 10), Interval(59, 59), Interval(56, 64), Interval(24, 30), Interval(1, 1),
         Interval(17, 17), Interval(6, 6), Interval(40, 42), Interval(39, 43), Interval(10, 10)],
        # Job 94
        [Interval(21, 25), Interval(71, 83), Interval(7, 7), Interval(65, 67), Interval(5, 5),
         Interval(85, 85), Interval(81, 93), Interval(1, 1), Interval(35, 45), Interval(61, 77),
         Interval(61, 63), Interval(89, 91), Interval(17, 23), Interval(17, 19), Interval(29, 35),
         Interval(32, 40), Interval(4, 4), Interval(6, 6), Interval(40, 54), Interval(25, 31)],
        # Job 95
        [Interval(45, 45), Interval(80, 94), Interval(4, 4), Interval(17, 17), Interval(6, 6),
         Interval(13, 13), Interval(63, 81), Interval(64, 68), Interval(68, 68), Interval(84, 90),
         Interval(1, 1), Interval(74, 84), Interval(44, 44), Interval(5, 5), Interval(33, 33),
         Interval(28, 36), Interval(20, 20), Interval(54, 72), Interval(73, 73), Interval(56, 68)],
        # Job 96
        [Interval(81, 81), Interval(3, 3), Interval(13, 13), Interval(38, 46), Interval(20, 24),
         Interval(32, 32), Interval(76, 90), Interval(51, 61), Interval(24, 32), Interval(94, 98),
         Interval(34, 34), Interval(40, 44), Interval(21, 23), Interval(84, 88), Interval(41, 49),
         Interval(75, 83), Interval(6, 8), Interval(43, 43), Interval(25, 29), Interval(35, 47)],
        # Job 97
        [Interval(4, 4), Interval(53, 57), Interval(30, 32), Interval(21, 23), Interval(26, 30),
         Interval(38, 50), Interval(15, 15), Interval(75, 101), Interval(25, 29), Interval(58, 74),
         Interval(45, 55), Interval(25, 25), Interval(25, 29), Interval(88, 94), Interval(47, 59),
         Interval(66, 76), Interval(10, 10), Interval(12, 12), Interval(2, 2), Interval(54, 68)],
        # Job 98
        [Interval(69, 71), Interval(61, 77), Interval(24, 28), Interval(75, 81), Interval(38, 46),
         Interval(83, 111), Interval(58, 78), Interval(77, 99), Interval(34, 40), Interval(21, 25),
         Interval(40, 52), Interval(54, 56), Interval(27, 31), Interval(77, 85), Interval(52, 56),
         Interval(61, 79), Interval(70, 72), Interval(2, 2), Interval(47, 59), Interval(27, 29)],
        # Job 99
        [Interval(39, 39), Interval(53, 59), Interval(78, 96), Interval(18, 24), Interval(9, 9),
         Interval(81, 83), Interval(41, 47), Interval(56, 70), Interval(8, 10), Interval(48, 52),
         Interval(33, 35), Interval(51, 65), Interval(18, 18), Interval(85, 89), Interval(39, 45),
         Interval(70, 86), Interval(87, 109), Interval(27, 33), Interval(40, 52), Interval(21, 21)],
    ],
    'name': 'INT__TAI100_20_10.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai100_20_10_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI100_20_10.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI100_20_10.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI100_20_10_F_15_01_INTERVAL_DATA
