"""
Problema INT__TAI100_20_05.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI100_20_05_F_15_01_INTERVAL_DATA = {
    'num_jobs': 100,
    'num_machines': 20,
    'problem_id': 'int__tai100_20_05.F.15_01_interval',
    'sequences': [
        [1, 0, 11, 9, 19, 8, 6, 14, 17, 13, 15, 7, 10, 2, 5, 18, 4, 12, 16, 3],
        [15, 1, 14, 9, 17, 11, 12, 3, 10, 7, 13, 19, 8, 16, 6, 0, 2, 18, 4, 5],
        [14, 9, 2, 0, 3, 6, 18, 8, 16, 19, 7, 12, 5, 4, 10, 15, 1, 13, 11, 17],
        [4, 9, 11, 8, 1, 18, 13, 16, 7, 12, 15, 10, 17, 14, 2, 5, 3, 19, 6, 0],
        [17, 9, 18, 14, 2, 0, 10, 7, 16, 11, 6, 4, 19, 8, 12, 13, 15, 1, 3, 5],
        [8, 11, 4, 7, 9, 16, 18, 15, 17, 19, 5, 6, 3, 2, 13, 12, 10, 0, 14, 1],
        [11, 1, 16, 3, 10, 0, 5, 6, 17, 18, 15, 7, 19, 13, 4, 12, 2, 14, 9, 8],
        [13, 14, 17, 2, 5, 16, 3, 6, 9, 15, 18, 7, 4, 11, 10, 8, 0, 1, 19, 12],
        [11, 9, 7, 16, 10, 18, 13, 12, 17, 6, 0, 4, 15, 5, 2, 1, 19, 8, 3, 14],
        [0, 10, 7, 13, 19, 9, 2, 11, 15, 14, 8, 12, 17, 5, 18, 3, 4, 1, 16, 6],
        [17, 2, 15, 8, 12, 9, 18, 16, 13, 7, 6, 19, 5, 1, 3, 10, 4, 0, 11, 14],
        [8, 2, 1, 18, 4, 11, 10, 17, 14, 9, 19, 13, 6, 5, 0, 16, 12, 3, 15, 7],
        [2, 12, 16, 5, 9, 14, 18, 10, 1, 7, 17, 4, 13, 8, 6, 0, 3, 15, 19, 11],
        [10, 8, 19, 2, 1, 17, 12, 18, 13, 14, 15, 4, 3, 11, 9, 6, 5, 0, 16, 7],
        [18, 15, 19, 9, 7, 1, 12, 3, 2, 11, 17, 16, 10, 0, 5, 4, 13, 6, 8, 14],
        [4, 8, 3, 7, 18, 16, 11, 13, 10, 5, 15, 17, 19, 9, 2, 1, 0, 14, 6, 12],
        [7, 1, 17, 0, 3, 14, 15, 18, 8, 13, 19, 2, 6, 16, 9, 12, 11, 4, 5, 10],
        [8, 15, 7, 19, 18, 17, 16, 6, 11, 10, 3, 12, 9, 0, 5, 14, 1, 4, 2, 13],
        [19, 7, 17, 6, 1, 4, 0, 8, 3, 11, 9, 12, 10, 2, 15, 14, 16, 5, 13, 18],
        [11, 8, 16, 19, 2, 10, 0, 9, 14, 17, 1, 3, 18, 13, 12, 5, 6, 4, 7, 15],
        [5, 11, 18, 2, 10, 15, 16, 8, 12, 1, 0, 14, 19, 4, 7, 6, 13, 17, 3, 9],
        [1, 12, 13, 14, 9, 8, 7, 5, 17, 0, 15, 10, 18, 6, 11, 4, 16, 3, 2, 19],
        [13, 2, 14, 17, 6, 10, 11, 0, 4, 7, 5, 18, 16, 19, 1, 15, 8, 9, 3, 12],
        [14, 15, 1, 11, 7, 13, 17, 12, 9, 3, 10, 6, 16, 18, 5, 8, 0, 2, 19, 4],
        [15, 12, 3, 13, 18, 5, 14, 19, 17, 1, 7, 16, 9, 2, 11, 0, 10, 4, 8, 6],
        [3, 9, 19, 17, 15, 2, 10, 16, 12, 11, 7, 14, 18, 8, 1, 13, 5, 4, 6, 0],
        [12, 18, 8, 10, 9, 13, 19, 16, 4, 1, 3, 15, 11, 5, 14, 6, 0, 7, 2, 17],
        [0, 10, 11, 5, 16, 15, 7, 3, 18, 4, 13, 1, 6, 2, 12, 9, 17, 8, 19, 14],
        [9, 7, 0, 3, 4, 15, 13, 17, 2, 6, 10, 19, 11, 5, 12, 1, 14, 8, 18, 16],
        [8, 3, 4, 7, 11, 6, 18, 14, 16, 19, 2, 1, 12, 15, 10, 13, 5, 17, 0, 9],
        [11, 14, 1, 15, 2, 10, 4, 16, 3, 9, 5, 12, 18, 7, 17, 8, 19, 0, 6, 13],
        [13, 8, 18, 19, 6, 9, 5, 1, 16, 11, 0, 2, 4, 14, 15, 12, 10, 3, 7, 17],
        [0, 14, 6, 19, 1, 3, 16, 18, 10, 2, 9, 8, 11, 15, 7, 4, 5, 13, 17, 12],
        [2, 3, 17, 14, 5, 18, 1, 0, 8, 16, 7, 12, 19, 11, 9, 15, 4, 10, 6, 13],
        [18, 9, 16, 3, 2, 11, 4, 5, 0, 12, 10, 15, 6, 8, 14, 7, 17, 19, 1, 13],
        [18, 5, 7, 10, 12, 19, 16, 17, 11, 3, 8, 4, 0, 14, 15, 9, 6, 2, 13, 1],
        [17, 7, 12, 4, 15, 6, 18, 5, 2, 16, 11, 19, 8, 10, 3, 1, 13, 9, 0, 14],
        [10, 6, 18, 4, 9, 16, 14, 2, 7, 13, 11, 19, 1, 8, 5, 3, 12, 17, 0, 15],
        [3, 1, 18, 5, 17, 4, 2, 10, 7, 14, 19, 0, 13, 12, 16, 9, 15, 11, 6, 8],
        [14, 4, 1, 12, 10, 3, 19, 7, 9, 8, 11, 18, 5, 2, 13, 6, 0, 17, 15, 16],
        [11, 3, 1, 0, 7, 12, 16, 19, 14, 4, 15, 5, 10, 2, 17, 9, 13, 8, 18, 6],
        [8, 10, 17, 13, 4, 19, 6, 2, 3, 5, 1, 14, 11, 7, 18, 15, 16, 0, 9, 12],
        [10, 15, 9, 7, 16, 13, 8, 5, 2, 17, 0, 12, 14, 19, 6, 18, 1, 4, 11, 3],
        [18, 3, 11, 9, 10, 0, 12, 7, 6, 4, 2, 1, 14, 17, 13, 8, 19, 5, 16, 15],
        [10, 12, 17, 1, 11, 9, 15, 6, 19, 2, 16, 18, 14, 13, 5, 7, 3, 8, 4, 0],
        [5, 16, 11, 8, 17, 4, 10, 6, 3, 14, 2, 7, 12, 9, 15, 1, 13, 0, 19, 18],
        [10, 11, 1, 16, 0, 3, 7, 19, 14, 17, 9, 4, 18, 8, 15, 12, 13, 5, 6, 2],
        [15, 10, 16, 11, 8, 0, 19, 5, 17, 7, 14, 12, 3, 1, 13, 9, 18, 2, 4, 6],
        [19, 2, 9, 12, 6, 11, 5, 16, 10, 15, 8, 7, 4, 13, 3, 1, 18, 17, 0, 14],
        [14, 4, 12, 16, 0, 9, 17, 2, 7, 6, 19, 1, 5, 3, 11, 13, 10, 8, 18, 15],
        [7, 0, 9, 13, 4, 11, 2, 10, 19, 1, 14, 3, 8, 5, 6, 12, 15, 18, 16, 17],
        [16, 7, 5, 10, 9, 13, 1, 3, 14, 15, 8, 12, 18, 0, 19, 11, 2, 17, 4, 6],
        [11, 3, 14, 2, 6, 9, 7, 19, 8, 15, 10, 12, 13, 18, 5, 16, 1, 0, 17, 4],
        [8, 10, 3, 16, 0, 6, 9, 11, 7, 1, 19, 17, 14, 4, 2, 13, 18, 5, 15, 12],
        [19, 11, 7, 12, 3, 16, 14, 6, 8, 10, 15, 0, 9, 13, 18, 17, 5, 4, 1, 2],
        [10, 14, 15, 12, 1, 8, 9, 18, 11, 2, 17, 5, 6, 19, 3, 4, 13, 7, 16, 0],
        [3, 8, 13, 12, 18, 15, 4, 7, 6, 16, 5, 9, 19, 2, 10, 11, 14, 0, 1, 17],
        [1, 3, 2, 7, 15, 0, 6, 5, 12, 4, 16, 9, 11, 17, 8, 18, 14, 19, 13, 10],
        [15, 18, 8, 5, 3, 4, 10, 14, 16, 7, 2, 19, 9, 13, 12, 0, 11, 6, 1, 17],
        [1, 3, 9, 6, 0, 16, 18, 4, 10, 15, 14, 19, 8, 12, 11, 2, 5, 17, 7, 13],
        [17, 3, 19, 13, 12, 1, 6, 16, 9, 10, 7, 18, 11, 8, 5, 2, 15, 0, 4, 14],
        [2, 4, 5, 0, 7, 3, 16, 11, 6, 8, 18, 10, 17, 12, 1, 14, 15, 13, 19, 9],
        [14, 5, 8, 3, 11, 15, 4, 13, 16, 1, 7, 12, 19, 9, 6, 2, 10, 0, 17, 18],
        [18, 0, 11, 2, 1, 4, 15, 16, 17, 3, 10, 5, 19, 9, 8, 14, 6, 12, 7, 13],
        [9, 0, 15, 13, 12, 18, 14, 6, 10, 7, 16, 1, 11, 5, 8, 2, 19, 4, 17, 3],
        [13, 7, 11, 2, 4, 10, 6, 19, 8, 0, 17, 1, 18, 14, 3, 9, 15, 12, 16, 5],
        [7, 9, 12, 11, 3, 2, 18, 13, 10, 1, 14, 16, 8, 6, 0, 4, 17, 5, 19, 15],
        [13, 16, 1, 19, 14, 11, 15, 4, 18, 5, 10, 0, 9, 7, 2, 12, 6, 8, 3, 17],
        [15, 10, 12, 13, 5, 17, 2, 6, 11, 0, 3, 1, 7, 19, 8, 14, 16, 4, 9, 18],
        [11, 4, 15, 8, 13, 14, 2, 3, 7, 10, 6, 0, 5, 12, 9, 16, 17, 19, 1, 18],
        [10, 9, 11, 19, 12, 7, 18, 6, 8, 14, 16, 0, 2, 3, 1, 5, 15, 17, 13, 4],
        [10, 18, 15, 19, 3, 1, 16, 2, 5, 13, 14, 12, 0, 7, 8, 11, 17, 9, 6, 4],
        [18, 10, 2, 6, 7, 1, 4, 5, 0, 17, 15, 3, 11, 9, 14, 16, 12, 13, 8, 19],
        [14, 18, 19, 11, 6, 16, 10, 15, 5, 1, 13, 8, 3, 12, 17, 7, 9, 2, 0, 4],
        [1, 14, 2, 18, 6, 3, 0, 4, 11, 12, 19, 13, 17, 16, 8, 5, 9, 7, 15, 10],
        [16, 1, 11, 17, 12, 9, 14, 0, 6, 18, 7, 3, 13, 19, 5, 4, 15, 8, 2, 10],
        [4, 3, 0, 8, 12, 2, 16, 18, 14, 17, 15, 6, 5, 11, 10, 13, 19, 7, 9, 1],
        [13, 9, 1, 12, 11, 18, 6, 8, 7, 2, 16, 5, 19, 3, 10, 0, 15, 4, 14, 17],
        [11, 19, 0, 12, 5, 18, 10, 17, 9, 2, 3, 6, 7, 16, 1, 13, 14, 4, 15, 8],
        [6, 13, 7, 19, 1, 14, 15, 3, 17, 11, 2, 12, 9, 8, 0, 10, 18, 4, 5, 16],
        [4, 7, 13, 9, 5, 6, 0, 15, 17, 14, 10, 19, 11, 2, 16, 8, 18, 1, 3, 12],
        [12, 18, 3, 13, 7, 10, 4, 6, 9, 8, 2, 5, 11, 19, 16, 17, 1, 14, 15, 0],
        [18, 15, 11, 7, 10, 14, 6, 16, 3, 2, 0, 4, 13, 9, 1, 8, 19, 5, 12, 17],
        [7, 18, 6, 4, 1, 9, 19, 17, 16, 2, 15, 5, 13, 8, 3, 14, 0, 12, 11, 10],
        [7, 0, 11, 14, 9, 2, 10, 3, 4, 1, 13, 8, 17, 16, 15, 19, 5, 18, 6, 12],
        [13, 14, 11, 7, 19, 1, 6, 15, 18, 4, 8, 5, 10, 3, 16, 12, 17, 9, 0, 2],
        [2, 6, 10, 8, 11, 15, 13, 5, 19, 18, 7, 12, 9, 1, 14, 3, 0, 17, 16, 4],
        [15, 7, 14, 0, 12, 3, 6, 19, 13, 9, 11, 10, 5, 2, 18, 17, 1, 8, 16, 4],
        [19, 4, 15, 13, 11, 7, 0, 3, 14, 6, 12, 17, 2, 16, 18, 1, 5, 9, 10, 8],
        [4, 0, 11, 10, 15, 8, 9, 16, 7, 6, 2, 19, 14, 12, 5, 1, 3, 18, 13, 17],
        [1, 2, 10, 4, 7, 14, 9, 11, 19, 18, 8, 5, 12, 0, 16, 3, 15, 17, 13, 6],
        [7, 18, 2, 15, 10, 11, 13, 17, 9, 19, 14, 1, 4, 6, 16, 5, 8, 12, 0, 3],
        [7, 8, 14, 15, 1, 10, 16, 3, 13, 0, 6, 2, 5, 17, 9, 4, 19, 18, 11, 12],
        [12, 17, 5, 18, 16, 1, 7, 2, 0, 10, 11, 3, 14, 9, 19, 13, 15, 4, 6, 8],
        [17, 10, 19, 4, 3, 8, 1, 5, 14, 12, 9, 2, 13, 18, 11, 16, 6, 0, 7, 15],
        [5, 11, 1, 6, 16, 14, 9, 15, 13, 3, 18, 7, 0, 2, 19, 17, 10, 4, 12, 8],
        [1, 3, 13, 17, 14, 19, 11, 6, 8, 10, 16, 12, 15, 7, 0, 9, 18, 5, 2, 4],
        [2, 3, 13, 4, 17, 14, 12, 19, 18, 15, 9, 11, 5, 10, 8, 0, 1, 7, 16, 6],
        [12, 14, 11, 5, 1, 6, 16, 9, 18, 13, 0, 10, 17, 3, 15, 4, 7, 19, 2, 8],
        [1, 11, 14, 0, 18, 13, 4, 19, 5, 12, 7, 16, 17, 15, 8, 2, 3, 6, 9, 10],
    ],
    'durations': [
        # Job 0
        [Interval(81, 101), Interval(18, 22), Interval(58, 62), Interval(13, 13), Interval(48, 60),
         Interval(33, 43), Interval(66, 72), Interval(57, 75), Interval(68, 88), Interval(29, 35),
         Interval(43, 51), Interval(78, 84), Interval(82, 110), Interval(67, 71), Interval(67, 81),
         Interval(84, 98), Interval(68, 78), Interval(57, 77), Interval(76, 102), Interval(72, 90)],
        # Job 1
        [Interval(62, 66), Interval(47, 51), Interval(88, 88), Interval(15, 19), Interval(30, 30),
         Interval(75, 79), Interval(94, 100), Interval(5, 5), Interval(78, 96), Interval(97, 101),
         Interval(19, 25), Interval(38, 46), Interval(45, 55), Interval(24, 30), Interval(19, 19),
         Interval(54, 56), Interval(72, 82), Interval(70, 86), Interval(17, 23), Interval(56, 56)],
        # Job 2
        [Interval(56, 68), Interval(55, 69), Interval(5, 5), Interval(68, 76), Interval(88, 104),
         Interval(25, 25), Interval(51, 63), Interval(4, 4), Interval(35, 37), Interval(2, 2),
         Interval(44, 58), Interval(12, 14), Interval(77, 83), Interval(75, 89), Interval(48, 50),
         Interval(91, 101), Interval(24, 30), Interval(25, 25), Interval(82, 84), Interval(36, 48)],
        # Job 3
        [Interval(81, 87), Interval(30, 32), Interval(2, 2), Interval(30, 32), Interval(15, 15),
         Interval(59, 67), Interval(17, 21), Interval(37, 39), Interval(64, 86), Interval(34, 36),
         Interval(46, 58), Interval(32, 42), Interval(84, 98), Interval(32, 36), Interval(6, 8),
         Interval(54, 72), Interval(6, 8), Interval(11, 11), Interval(42, 48), Interval(59, 77)],
        # Job 4
        [Interval(14, 16), Interval(65, 85), Interval(82, 94), Interval(47, 47), Interval(58, 64),
         Interval(78, 104), Interval(7, 7), Interval(24, 32), Interval(7, 9), Interval(94, 98),
         Interval(4, 4), Interval(81, 101), Interval(21, 23), Interval(60, 60), Interval(47, 63),
         Interval(20, 24), Interval(32, 40), Interval(36, 38), Interval(40, 46), Interval(13, 13)],
        # Job 5
        [Interval(2, 2), Interval(36, 46), Interval(25, 31), Interval(89, 91), Interval(13, 15),
         Interval(62, 80), Interval(65, 77), Interval(62, 64), Interval(90, 90), Interval(43, 45),
         Interval(84, 90), Interval(70, 74), Interval(27, 35), Interval(51, 63), Interval(40, 44),
         Interval(1, 1), Interval(6, 6), Interval(70, 78), Interval(25, 29), Interval(84, 88)],
        # Job 6
        [Interval(63, 67), Interval(51, 61), Interval(73, 81), Interval(29, 31), Interval(23, 25),
         Interval(57, 61), Interval(13, 13), Interval(43, 51), Interval(51, 61), Interval(48, 54),
         Interval(49, 61), Interval(10, 12), Interval(69, 79), Interval(74, 96), Interval(43, 49),
         Interval(14, 14), Interval(55, 59), Interval(7, 9), Interval(31, 41), Interval(16, 18)],
        # Job 7
        [Interval(39, 41), Interval(24, 30), Interval(62, 78), Interval(43, 55), Interval(96, 98),
         Interval(8, 8), Interval(19, 21), Interval(10, 12), Interval(75, 81), Interval(47, 47),
         Interval(59, 79), Interval(55, 61), Interval(35, 35), Interval(19, 21), Interval(48, 56),
         Interval(5, 5), Interval(51, 61), Interval(62, 74), Interval(38, 50), Interval(73, 75)],
        # Job 8
        [Interval(12, 14), Interval(46, 48), Interval(69, 69), Interval(22, 26), Interval(80, 98),
         Interval(85, 109), Interval(48, 54), Interval(38, 44), Interval(27, 31), Interval(60, 78),
         Interval(56, 64), Interval(50, 50), Interval(83, 83), Interval(60, 68), Interval(83, 89),
         Interval(84, 108), Interval(54, 62), Interval(57, 57), Interval(54, 66), Interval(41, 53)],
        # Job 9
        [Interval(21, 25), Interval(38, 42), Interval(79, 89), Interval(70, 84), Interval(58, 62),
         Interval(49, 57), Interval(47, 49), Interval(51, 65), Interval(14, 14), Interval(16, 16),
         Interval(18, 22), Interval(69, 89), Interval(75, 101), Interval(24, 26), Interval(27, 31),
         Interval(68, 68), Interval(3, 3), Interval(77, 93), Interval(47, 51), Interval(6, 6)],
        # Job 10
        [Interval(13, 15), Interval(40, 42), Interval(10, 12), Interval(34, 38), Interval(60, 64),
         Interval(77, 87), Interval(52, 58), Interval(71, 85), Interval(39, 39), Interval(93, 105),
         Interval(93, 93), Interval(63, 83), Interval(88, 98), Interval(81, 101), Interval(32, 40),
         Interval(11, 11), Interval(75, 81), Interval(67, 73), Interval(69, 71), Interval(60, 64)],
        # Job 11
        [Interval(81, 87), Interval(12, 16), Interval(33, 43), Interval(35, 37), Interval(59, 77),
         Interval(15, 17), Interval(84, 100), Interval(37, 45), Interval(4, 4), Interval(43, 51),
         Interval(49, 51), Interval(80, 96), Interval(81, 103), Interval(29, 29), Interval(23, 23),
         Interval(17, 21), Interval(10, 10), Interval(8, 10), Interval(22, 26), Interval(71, 77)],
        # Job 12
        [Interval(89, 97), Interval(7, 9), Interval(32, 38), Interval(10, 12), Interval(76, 88),
         Interval(2, 2), Interval(40, 42), Interval(33, 35), Interval(21, 23), Interval(98, 98),
         Interval(69, 75), Interval(59, 75), Interval(87, 109), Interval(17, 21), Interval(16, 16),
         Interval(7, 7), Interval(70, 94), Interval(63, 71), Interval(22, 26), Interval(51, 55)],
        # Job 13
        [Interval(77, 91), Interval(6, 6), Interval(63, 83), Interval(93, 105), Interval(68, 70),
         Interval(69, 85), Interval(25, 25), Interval(39, 39), Interval(25, 29), Interval(8, 8),
         Interval(65, 69), Interval(35, 41), Interval(53, 71), Interval(7, 9), Interval(34, 36),
         Interval(39, 49), Interval(42, 48), Interval(52, 60), Interval(46, 46), Interval(31, 39)],
        # Job 14
        [Interval(26, 26), Interval(72, 94), Interval(13, 13), Interval(32, 42), Interval(67, 75),
         Interval(22, 26), Interval(18, 22), Interval(42, 48), Interval(33, 33), Interval(41, 55),
         Interval(75, 75), Interval(15, 15), Interval(29, 29), Interval(13, 17), Interval(38, 50),
         Interval(52, 58), Interval(1, 1), Interval(20, 22), Interval(59, 75), Interval(24, 30)],
        # Job 15
        [Interval(92, 104), Interval(22, 22), Interval(94, 100), Interval(9, 9), Interval(52, 58),
         Interval(88, 92), Interval(51, 51), Interval(26, 34), Interval(45, 51), Interval(43, 51),
         Interval(45, 51), Interval(73, 83), Interval(19, 21), Interval(14, 14), Interval(18, 24),
         Interval(93, 101), Interval(66, 72), Interval(22, 28), Interval(49, 61), Interval(51, 53)],
        # Job 16
        [Interval(42, 46), Interval(47, 55), Interval(7, 7), Interval(52, 66), Interval(48, 48),
         Interval(83, 89), Interval(29, 31), Interval(92, 106), Interval(48, 54), Interval(47, 47),
         Interval(1, 1), Interval(14, 18), Interval(68, 82), Interval(29, 29), Interval(60, 68),
         Interval(61, 69), Interval(85, 103), Interval(78, 88), Interval(52, 70), Interval(36, 36)],
        # Job 17
        [Interval(23, 23), Interval(22, 26), Interval(51, 69), Interval(56, 62), Interval(69, 85),
         Interval(41, 45), Interval(18, 22), Interval(93, 105), Interval(24, 32), Interval(61, 69),
         Interval(78, 92), Interval(19, 25), Interval(93, 95), Interval(56, 68), Interval(21, 27),
         Interval(50, 62), Interval(65, 85), Interval(10, 12), Interval(41, 55), Interval(23, 29)],
        # Job 18
        [Interval(77, 99), Interval(62, 62), Interval(67, 83), Interval(79, 87), Interval(68, 74),
         Interval(29, 35), Interval(6, 6), Interval(83, 95), Interval(44, 44), Interval(27, 33),
         Interval(10, 10), Interval(32, 38), Interval(68, 88), Interval(34, 46), Interval(46, 50),
         Interval(76, 88), Interval(71, 83), Interval(68, 78), Interval(18, 20), Interval(74, 98)],
        # Job 19
        [Interval(88, 96), Interval(72, 80), Interval(49, 57), Interval(79, 91), Interval(42, 50),
         Interval(41, 43), Interval(30, 38), Interval(74, 96), Interval(47, 59), Interval(20, 20),
         Interval(22, 26), Interval(15, 15), Interval(25, 27), Interval(11, 11), Interval(25, 31),
         Interval(90, 102), Interval(44, 54), Interval(6, 8), Interval(29, 37), Interval(80, 84)],
        # Job 20
        [Interval(27, 35), Interval(10, 10), Interval(18, 20), Interval(75, 91), Interval(10, 10),
         Interval(77, 77), Interval(91, 99), Interval(53, 61), Interval(46, 52), Interval(66, 68),
         Interval(29, 39), Interval(21, 21), Interval(24, 30), Interval(42, 44), Interval(51, 61),
         Interval(86, 100), Interval(41, 53), Interval(80, 80), Interval(24, 32), Interval(77, 79)],
        # Job 21
        [Interval(47, 63), Interval(41, 51), Interval(32, 34), Interval(44, 48), Interval(46, 54),
         Interval(22, 26), Interval(63, 69), Interval(29, 31), Interval(85, 91), Interval(24, 28),
         Interval(77, 81), Interval(28, 36), Interval(65, 69), Interval(21, 27), Interval(19, 21),
         Interval(65, 69), Interval(4, 4), Interval(7, 9), Interval(4, 4), Interval(30, 32)],
        # Job 22
        [Interval(13, 17), Interval(27, 33), Interval(82, 110), Interval(43, 57), Interval(64, 82),
         Interval(42, 42), Interval(50, 62), Interval(63, 71), Interval(14, 18), Interval(32, 42),
         Interval(28, 28), Interval(12, 16), Interval(12, 12), Interval(16, 18), Interval(12, 12),
         Interval(89, 89), Interval(79, 101), Interval(81, 103), Interval(83, 101), Interval(41, 43)],
        # Job 23
        [Interval(85, 111), Interval(2, 2), Interval(61, 61), Interval(9, 9), Interval(44, 52),
         Interval(63, 75), Interval(64, 66), Interval(7, 9), Interval(79, 85), Interval(58, 70),
         Interval(56, 66), Interval(5, 5), Interval(21, 21), Interval(90, 104), Interval(55, 71),
         Interval(74, 96), Interval(16, 20), Interval(34, 44), Interval(84, 98), Interval(60, 68)],
        # Job 24
        [Interval(70, 70), Interval(48, 54), Interval(79, 99), Interval(68, 84), Interval(70, 84),
         Interval(6, 6), Interval(22, 22), Interval(28, 30), Interval(5, 5), Interval(33, 39),
         Interval(53, 55), Interval(30, 32), Interval(6, 6), Interval(79, 95), Interval(76, 92),
         Interval(3, 3), Interval(5, 5), Interval(81, 95), Interval(30, 40), Interval(84, 94)],
        # Job 25
        [Interval(50, 62), Interval(71, 89), Interval(14, 14), Interval(28, 28), Interval(12, 16),
         Interval(6, 6), Interval(6, 6), Interval(68, 90), Interval(83, 85), Interval(23, 23),
         Interval(65, 87), Interval(33, 43), Interval(26, 30), Interval(93, 103), Interval(96, 100),
         Interval(36, 40), Interval(57, 57), Interval(24, 30), Interval(54, 70), Interval(88, 100)],
        # Job 26
        [Interval(90, 94), Interval(26, 26), Interval(22, 26), Interval(16, 20), Interval(27, 33),
         Interval(11, 11), Interval(54, 70), Interval(36, 40), Interval(52, 52), Interval(3, 3),
         Interval(74, 98), Interval(17, 17), Interval(2, 2), Interval(46, 54), Interval(84, 90),
         Interval(10, 10), Interval(34, 40), Interval(40, 44), Interval(28, 32), Interval(5, 5)],
        # Job 27
        [Interval(43, 53), Interval(80, 98), Interval(98, 100), Interval(46, 52), Interval(52, 56),
         Interval(53, 61), Interval(31, 33), Interval(79, 93), Interval(68, 82), Interval(61, 67),
         Interval(92, 106), Interval(51, 69), Interval(63, 79), Interval(48, 56), Interval(71, 77),
         Interval(17, 19), Interval(12, 14), Interval(53, 65), Interval(23, 29), Interval(55, 63)],
        # Job 28
        [Interval(25, 27), Interval(34, 42), Interval(89, 107), Interval(27, 31), Interval(28, 30),
         Interval(50, 56), Interval(49, 51), Interval(6, 8), Interval(72, 90), Interval(67, 89),
         Interval(85, 85), Interval(24, 28), Interval(27, 27), Interval(48, 56), Interval(6, 8),
         Interval(93, 95), Interval(74, 98), Interval(47, 61), Interval(47, 55), Interval(17, 17)],
        # Job 29
        [Interval(92, 98), Interval(23, 27), Interval(62, 80), Interval(15, 17), Interval(58, 70),
         Interval(22, 24), Interval(71, 83), Interval(29, 29), Interval(89, 91), Interval(54, 56),
         Interval(75, 91), Interval(16, 20), Interval(39, 45), Interval(72, 84), Interval(33, 33),
         Interval(12, 12), Interval(28, 28), Interval(85, 109), Interval(57, 65), Interval(7, 7)],
        # Job 30
        [Interval(1, 1), Interval(51, 57), Interval(38, 46), Interval(78, 78), Interval(15, 15),
         Interval(69, 73), Interval(68, 70), Interval(9, 11), Interval(67, 67), Interval(24, 30),
         Interval(82, 82), Interval(51, 67), Interval(85, 101), Interval(76, 98), Interval(52, 58),
         Interval(54, 68), Interval(61, 79), Interval(57, 59), Interval(75, 97), Interval(7, 7)],
        # Job 31
        [Interval(36, 48), Interval(70, 72), Interval(84, 104), Interval(71, 75), Interval(54, 62),
         Interval(20, 24), Interval(36, 48), Interval(12, 14), Interval(54, 58), Interval(67, 81),
         Interval(12, 12), Interval(23, 29), Interval(68, 72), Interval(85, 97), Interval(66, 70),
         Interval(1, 1), Interval(2, 2), Interval(11, 13), Interval(78, 104), Interval(50, 56)],
        # Job 32
        [Interval(60, 74), Interval(2, 2), Interval(60, 76), Interval(86, 92), Interval(4, 4),
         Interval(75, 91), Interval(54, 72), Interval(57, 59), Interval(46, 46), Interval(53, 71),
         Interval(91, 107), Interval(78, 102), Interval(80, 102), Interval(9, 9), Interval(80, 86),
         Interval(15, 15), Interval(76, 90), Interval(41, 53), Interval(90, 100), Interval(39, 45)],
        # Job 33
        [Interval(81, 93), Interval(25, 29), Interval(6, 8), Interval(30, 36), Interval(89, 95),
         Interval(49, 55), Interval(78, 86), Interval(25, 33), Interval(77, 99), Interval(20, 22),
         Interval(41, 49), Interval(55, 67), Interval(33, 35), Interval(47, 59), Interval(25, 27),
         Interval(22, 24), Interval(68, 70), Interval(63, 83), Interval(77, 97), Interval(53, 53)],
        # Job 34
        [Interval(45, 47), Interval(48, 54), Interval(56, 58), Interval(86, 90), Interval(66, 76),
         Interval(10, 10), Interval(8, 10), Interval(43, 47), Interval(82, 98), Interval(15, 17),
         Interval(53, 57), Interval(82, 100), Interval(57, 73), Interval(31, 41), Interval(19, 19),
         Interval(69, 71), Interval(80, 104), Interval(15, 17), Interval(65, 87), Interval(1, 1)],
        # Job 35
        [Interval(40, 46), Interval(40, 52), Interval(60, 66), Interval(53, 71), Interval(64, 80),
         Interval(12, 12), Interval(87, 109), Interval(49, 57), Interval(52, 62), Interval(67, 67),
         Interval(39, 51), Interval(78, 102), Interval(79, 87), Interval(32, 40), Interval(54, 54),
         Interval(83, 87), Interval(25, 33), Interval(6, 6), Interval(36, 36), Interval(29, 35)],
        # Job 36
        [Interval(28, 28), Interval(62, 68), Interval(7, 7), Interval(47, 53), Interval(1, 1),
         Interval(53, 69), Interval(49, 63), Interval(19, 23), Interval(38, 40), Interval(54, 60),
         Interval(37, 49), Interval(33, 35), Interval(53, 61), Interval(37, 41), Interval(21, 23),
         Interval(71, 89), Interval(86, 90), Interval(64, 68), Interval(89, 91), Interval(19, 21)],
        # Job 37
        [Interval(10, 10), Interval(2, 2), Interval(11, 11), Interval(82, 82), Interval(48, 64),
         Interval(74, 82), Interval(73, 77), Interval(40, 40), Interval(29, 39), Interval(37, 47),
         Interval(51, 51), Interval(17, 17), Interval(53, 71), Interval(29, 35), Interval(75, 101),
         Interval(67, 73), Interval(47, 53), Interval(78, 78), Interval(36, 42), Interval(89, 107)],
        # Job 38
        [Interval(7, 9), Interval(24, 28), Interval(10, 12), Interval(27, 31), Interval(93, 105),
         Interval(9, 9), Interval(51, 65), Interval(51, 69), Interval(45, 59), Interval(31, 41),
         Interval(13, 15), Interval(40, 54), Interval(67, 73), Interval(10, 10), Interval(1, 1),
         Interval(66, 66), Interval(47, 55), Interval(95, 97), Interval(37, 45), Interval(68, 78)],
        # Job 39
        [Interval(74, 76), Interval(83, 95), Interval(81, 103), Interval(16, 16), Interval(47, 57),
         Interval(88, 108), Interval(20, 22), Interval(49, 51), Interval(61, 61), Interval(22, 22),
         Interval(78, 78), Interval(44, 58), Interval(68, 72), Interval(40, 42), Interval(39, 39),
         Interval(17, 21), Interval(89, 93), Interval(53, 71), Interval(40, 52), Interval(37, 41)],
        # Job 40
        [Interval(50, 54), Interval(83, 99), Interval(22, 26), Interval(2, 2), Interval(38, 48),
         Interval(35, 39), Interval(11, 11), Interval(54, 56), Interval(49, 53), Interval(27, 27),
         Interval(26, 30), Interval(90, 92), Interval(43, 47), Interval(67, 89), Interval(26, 32),
         Interval(59, 73), Interval(81, 93), Interval(83, 89), Interval(14, 18), Interval(18, 22)],
        # Job 41
        [Interval(2, 2), Interval(26, 28), Interval(76, 84), Interval(10, 12), Interval(17, 21),
         Interval(55, 65), Interval(52, 64), Interval(14, 18), Interval(32, 36), Interval(62, 74),
         Interval(79, 99), Interval(73, 93), Interval(5, 5), Interval(41, 45), Interval(62, 78),
         Interval(9, 11), Interval(56, 74), Interval(70, 70), Interval(12, 12), Interval(21, 27)],
        # Job 42
        [Interval(90, 102), Interval(74, 98), Interval(47, 49), Interval(73, 75), Interval(10, 10),
         Interval(4, 4), Interval(51, 59), Interval(47, 59), Interval(50, 62), Interval(1, 1),
         Interval(50, 54), Interval(50, 54), Interval(78, 94), Interval(6, 6), Interval(61, 69),
         Interval(50, 66), Interval(71, 89), Interval(90, 102), Interval(38, 38), Interval(93, 95)],
        # Job 43
        [Interval(63, 73), Interval(23, 23), Interval(46, 54), Interval(71, 89), Interval(80, 86),
         Interval(67, 75), Interval(30, 36), Interval(46, 50), Interval(24, 32), Interval(56, 64),
         Interval(67, 85), Interval(16, 20), Interval(32, 32), Interval(56, 74), Interval(32, 34),
         Interval(96, 100), Interval(25, 31), Interval(87, 97), Interval(85, 105), Interval(11, 11)],
        # Job 44
        [Interval(64, 84), Interval(75, 83), Interval(35, 45), Interval(50, 56), Interval(24, 24),
         Interval(26, 34), Interval(45, 59), Interval(23, 29), Interval(84, 96), Interval(50, 56),
         Interval(46, 54), Interval(85, 97), Interval(62, 78), Interval(83, 97), Interval(30, 32),
         Interval(34, 36), Interval(59, 73), Interval(84, 96), Interval(1, 1), Interval(19, 23)],
        # Job 45
        [Interval(45, 45), Interval(16, 18), Interval(69, 93), Interval(85, 109), Interval(76, 86),
         Interval(59, 75), Interval(82, 82), Interval(22, 26), Interval(26, 28), Interval(50, 54),
         Interval(59, 59), Interval(48, 62), Interval(67, 81), Interval(23, 27), Interval(54, 62),
         Interval(62, 62), Interval(28, 30), Interval(88, 88), Interval(90, 104), Interval(80, 80)],
        # Job 46
        [Interval(1, 1), Interval(22, 26), Interval(11, 11), Interval(78, 98), Interval(68, 86),
         Interval(55, 73), Interval(23, 31), Interval(13, 13), Interval(47, 57), Interval(48, 50),
         Interval(18, 20), Interval(56, 68), Interval(10, 10), Interval(42, 42), Interval(89, 105),
         Interval(44, 54), Interval(73, 79), Interval(58, 60), Interval(36, 36), Interval(37, 49)],
        # Job 47
        [Interval(90, 94), Interval(76, 88), Interval(18, 24), Interval(67, 73), Interval(83, 95),
         Interval(23, 29), Interval(23, 25), Interval(1, 1), Interval(20, 24), Interval(11, 13),
         Interval(6, 6), Interval(31, 37), Interval(83, 93), Interval(28, 28), Interval(54, 54),
         Interval(8, 8), Interval(72, 76), Interval(39, 43), Interval(1, 1), Interval(74, 74)],
        # Job 48
        [Interval(25, 33), Interval(7, 7), Interval(69, 87), Interval(84, 96), Interval(68, 88),
         Interval(89, 99), Interval(7, 7), Interval(52, 54), Interval(7, 9), Interval(79, 105),
         Interval(18, 18), Interval(52, 66), Interval(57, 61), Interval(92, 100), Interval(49, 55),
         Interval(64, 74), Interval(64, 64), Interval(66, 86), Interval(75, 89), Interval(36, 36)],
        # Job 49
        [Interval(17, 19), Interval(60, 68), Interval(75, 97), Interval(71, 93), Interval(6, 6),
         Interval(2, 2), Interval(72, 92), Interval(40, 52), Interval(20, 24), Interval(13, 13),
         Interval(89, 95), Interval(37, 39), Interval(62, 82), Interval(39, 51), Interval(60, 72),
         Interval(48, 48), Interval(9, 11), Interval(90, 98), Interval(74, 92), Interval(5, 5)],
        # Job 50
        [Interval(23, 31), Interval(30, 30), Interval(94, 104), Interval(70, 74), Interval(16, 18),
         Interval(66, 72), Interval(57, 61), Interval(3, 3), Interval(91, 95), Interval(4, 4),
         Interval(28, 32), Interval(17, 19), Interval(33, 39), Interval(62, 68), Interval(92, 94),
         Interval(34, 40), Interval(9, 11), Interval(45, 45), Interval(12, 16), Interval(84, 112)],
        # Job 51
        [Interval(9, 9), Interval(66, 66), Interval(32, 34), Interval(30, 40), Interval(25, 25),
         Interval(41, 47), Interval(13, 13), Interval(7, 9), Interval(43, 51), Interval(80, 80),
         Interval(91, 107), Interval(23, 23), Interval(59, 59), Interval(2, 2), Interval(77, 101),
         Interval(14, 18), Interval(28, 32), Interval(42, 48), Interval(3, 3), Interval(51, 59)],
        # Job 52
        [Interval(68, 80), Interval(6, 8), Interval(3, 3), Interval(91, 101), Interval(9, 9),
         Interval(38, 50), Interval(14, 16), Interval(14, 18), Interval(94, 102), Interval(18, 20),
         Interval(8, 8), Interval(1, 1), Interval(78, 96), Interval(8, 10), Interval(45, 51),
         Interval(76, 76), Interval(26, 26), Interval(57, 69), Interval(46, 58), Interval(11, 13)],
        # Job 53
        [Interval(80, 100), Interval(39, 39), Interval(54, 62), Interval(27, 33), Interval(35, 35),
         Interval(70, 90), Interval(62, 76), Interval(7, 7), Interval(69, 71), Interval(48, 56),
         Interval(81, 95), Interval(49, 63), Interval(8, 8), Interval(12, 12), Interval(4, 4),
         Interval(46, 50), Interval(50, 64), Interval(33, 35), Interval(68, 72), Interval(12, 14)],
        # Job 54
        [Interval(91, 91), Interval(37, 41), Interval(82, 90), Interval(45, 49), Interval(54, 68),
         Interval(18, 20), Interval(68, 76), Interval(62, 64), Interval(42, 46), Interval(85, 105),
         Interval(50, 54), Interval(55, 67), Interval(6, 8), Interval(91, 97), Interval(77, 77),
         Interval(52, 64), Interval(11, 11), Interval(20, 22), Interval(51, 57), Interval(74, 86)],
        # Job 55
        [Interval(12, 16), Interval(55, 69), Interval(12, 14), Interval(73, 95), Interval(13, 17),
         Interval(19, 19), Interval(61, 79), Interval(28, 36), Interval(56, 58), Interval(38, 38),
         Interval(77, 103), Interval(33, 41), Interval(29, 33), Interval(64, 64), Interval(19, 21),
         Interval(12, 12), Interval(9, 9), Interval(73, 77), Interval(82, 98), Interval(15, 15)],
        # Job 56
        [Interval(44, 52), Interval(13, 13), Interval(5, 5), Interval(13, 13), Interval(18, 20),
         Interval(76, 98), Interval(70, 90), Interval(6, 6), Interval(54, 54), Interval(39, 43),
         Interval(55, 57), Interval(10, 10), Interval(64, 64), Interval(25, 27), Interval(33, 33),
         Interval(10, 12), Interval(20, 20), Interval(29, 35), Interval(21, 27), Interval(26, 28)],
        # Job 57
        [Interval(62, 68), Interval(85, 93), Interval(39, 39), Interval(67, 87), Interval(16, 20),
         Interval(42, 42), Interval(39, 51), Interval(75, 91), Interval(53, 55), Interval(59, 67),
         Interval(80, 84), Interval(45, 55), Interval(8, 10), Interval(72, 72), Interval(45, 47),
         Interval(48, 54), Interval(34, 38), Interval(24, 30), Interval(8, 10), Interval(42, 54)],
        # Job 58
        [Interval(33, 35), Interval(82, 88), Interval(2, 2), Interval(27, 31), Interval(16, 18),
         Interval(52, 68), Interval(69, 69), Interval(55, 55), Interval(29, 39), Interval(12, 12),
         Interval(15, 19), Interval(55, 65), Interval(1, 1), Interval(59, 67), Interval(61, 63),
         Interval(12, 16), Interval(71, 81), Interval(2, 2), Interval(77, 93), Interval(8, 10)],
        # Job 59
        [Interval(13, 13), Interval(39, 49), Interval(96, 100), Interval(16, 16), Interval(62, 64),
         Interval(31, 31), Interval(67, 79), Interval(65, 85), Interval(27, 35), Interval(43, 49),
         Interval(75, 95), Interval(78, 80), Interval(59, 75), Interval(6, 6), Interval(22, 28),
         Interval(36, 44), Interval(36, 42), Interval(16, 16), Interval(52, 68), Interval(56, 72)],
        # Job 60
        [Interval(20, 26), Interval(94, 94), Interval(53, 57), Interval(24, 26), Interval(86, 100),
         Interval(26, 34), Interval(95, 95), Interval(55, 57), Interval(1, 1), Interval(3, 3),
         Interval(77, 77), Interval(1, 1), Interval(48, 56), Interval(51, 53), Interval(21, 21),
         Interval(5, 5), Interval(1, 1), Interval(9, 9), Interval(20, 26), Interval(70, 86)],
        # Job 61
        [Interval(9, 11), Interval(67, 69), Interval(49, 63), Interval(65, 79), Interval(57, 69),
         Interval(77, 83), Interval(82, 100), Interval(80, 80), Interval(22, 22), Interval(70, 70),
         Interval(35, 43), Interval(38, 38), Interval(52, 62), Interval(79, 79), Interval(54, 66),
         Interval(19, 19), Interval(85, 105), Interval(33, 37), Interval(40, 42), Interval(3, 3)],
        # Job 62
        [Interval(51, 59), Interval(49, 51), Interval(2, 2), Interval(65, 73), Interval(43, 45),
         Interval(18, 20), Interval(63, 77), Interval(71, 71), Interval(48, 58), Interval(95, 101),
         Interval(63, 67), Interval(4, 4), Interval(45, 47), Interval(93, 95), Interval(47, 49),
         Interval(79, 93), Interval(6, 6), Interval(29, 39), Interval(83, 111), Interval(41, 49)],
        # Job 63
        [Interval(77, 93), Interval(34, 42), Interval(26, 28), Interval(83, 103), Interval(77, 85),
         Interval(15, 19), Interval(12, 16), Interval(74, 82), Interval(83, 95), Interval(78, 102),
         Interval(90, 104), Interval(92, 102), Interval(12, 12), Interval(26, 30), Interval(62, 82),
         Interval(91, 95), Interval(16, 20), Interval(82, 98), Interval(51, 55), Interval(21, 25)],
        # Job 64
        [Interval(71, 95), Interval(10, 12), Interval(93, 95), Interval(41, 47), Interval(69, 91),
         Interval(83, 105), Interval(23, 25), Interval(59, 71), Interval(19, 25), Interval(65, 83),
         Interval(54, 70), Interval(53, 63), Interval(84, 88), Interval(48, 50), Interval(92, 96),
         Interval(29, 29), Interval(67, 83), Interval(13, 13), Interval(26, 26), Interval(79, 85)],
        # Job 65
        [Interval(29, 33), Interval(76, 76), Interval(9, 9), Interval(15, 17), Interval(25, 31),
         Interval(80, 96), Interval(96, 98), Interval(39, 47), Interval(14, 14), Interval(85, 93),
         Interval(37, 39), Interval(65, 67), Interval(61, 63), Interval(7, 9), Interval(36, 46),
         Interval(79, 83), Interval(38, 38), Interval(15, 17), Interval(26, 26), Interval(14, 18)],
        # Job 66
        [Interval(45, 57), Interval(1, 1), Interval(79, 81), Interval(62, 64), Interval(1, 1),
         Interval(57, 65), Interval(91, 105), Interval(58, 58), Interval(40, 54), Interval(13, 17),
         Interval(79, 87), Interval(16, 16), Interval(50, 50), Interval(34, 38), Interval(13, 13),
         Interval(44, 48), Interval(85, 109), Interval(80, 94), Interval(3, 3), Interval(48, 52)],
        # Job 67
        [Interval(87, 109), Interval(59, 71), Interval(19, 25), Interval(27, 35), Interval(36, 40),
         Interval(45, 45), Interval(66, 78), Interval(71, 73), Interval(34, 40), Interval(54, 72),
         Interval(33, 41), Interval(45, 55), Interval(6, 6), Interval(30, 30), Interval(10, 12),
         Interval(33, 35), Interval(40, 52), Interval(33, 35), Interval(35, 39), Interval(74, 90)],
        # Job 68
        [Interval(30, 32), Interval(19, 19), Interval(26, 34), Interval(79, 81), Interval(21, 27),
         Interval(64, 84), Interval(61, 73), Interval(36, 42), Interval(33, 37), Interval(71, 87),
         Interval(42, 42), Interval(24, 24), Interval(41, 49), Interval(5, 5), Interval(12, 14),
         Interval(44, 44), Interval(82, 104), Interval(31, 35), Interval(30, 38), Interval(26, 30)],
        # Job 69
        [Interval(19, 19), Interval(4, 4), Interval(45, 59), Interval(82, 82), Interval(36, 48),
         Interval(63, 79), Interval(17, 21), Interval(40, 54), Interval(17, 17), Interval(66, 68),
         Interval(38, 38), Interval(20, 26), Interval(74, 84), Interval(82, 108), Interval(21, 21),
         Interval(52, 60), Interval(19, 19), Interval(52, 52), Interval(25, 25), Interval(61, 75)],
        # Job 70
        [Interval(58, 58), Interval(32, 42), Interval(44, 48), Interval(4, 4), Interval(70, 76),
         Interval(79, 93), Interval(8, 8), Interval(51, 51), Interval(41, 51), Interval(34, 42),
         Interval(32, 34), Interval(29, 39), Interval(85, 93), Interval(82, 98), Interval(73, 73),
         Interval(78, 84), Interval(32, 42), Interval(44, 56), Interval(77, 83), Interval(55, 71)],
        # Job 71
        [Interval(67, 81), Interval(23, 29), Interval(66, 84), Interval(37, 43), Interval(25, 33),
         Interval(75, 83), Interval(74, 92), Interval(36, 44), Interval(30, 40), Interval(52, 54),
         Interval(54, 60), Interval(99, 99), Interval(57, 57), Interval(83, 105), Interval(92, 106),
         Interval(52, 54), Interval(85, 101), Interval(65, 85), Interval(26, 32), Interval(79, 79)],
        # Job 72
        [Interval(34, 44), Interval(20, 22), Interval(51, 51), Interval(84, 100), Interval(88, 96),
         Interval(35, 37), Interval(71, 75), Interval(49, 57), Interval(57, 67), Interval(92, 102),
         Interval(55, 69), Interval(17, 17), Interval(68, 92), Interval(27, 31), Interval(78, 94),
         Interval(77, 101), Interval(26, 26), Interval(25, 33), Interval(9, 9), Interval(80, 86)],
        # Job 73
        [Interval(81, 97), Interval(86, 90), Interval(8, 10), Interval(56, 70), Interval(61, 67),
         Interval(79, 91), Interval(92, 98), Interval(74, 100), Interval(39, 49), Interval(13, 17),
         Interval(21, 25), Interval(10, 10), Interval(83, 103), Interval(63, 71), Interval(60, 78),
         Interval(12, 14), Interval(30, 40), Interval(61, 81), Interval(50, 52), Interval(84, 96)],
        # Job 74
        [Interval(49, 57), Interval(64, 80), Interval(43, 55), Interval(10, 12), Interval(46, 58),
         Interval(53, 69), Interval(36, 36), Interval(99, 99), Interval(48, 50), Interval(71, 95),
         Interval(9, 11), Interval(32, 32), Interval(35, 43), Interval(37, 41), Interval(78, 94),
         Interval(12, 14), Interval(49, 59), Interval(81, 101), Interval(6, 6), Interval(47, 55)],
        # Job 75
        [Interval(72, 82), Interval(57, 61), Interval(79, 87), Interval(49, 51), Interval(77, 99),
         Interval(7, 9), Interval(9, 9), Interval(57, 59), Interval(40, 50), Interval(22, 28),
         Interval(10, 12), Interval(34, 34), Interval(61, 75), Interval(30, 40), Interval(25, 27),
         Interval(41, 55), Interval(1, 1), Interval(48, 48), Interval(12, 12), Interval(53, 59)],
        # Job 76
        [Interval(22, 26), Interval(53, 67), Interval(18, 22), Interval(16, 16), Interval(64, 66),
         Interval(61, 71), Interval(45, 49), Interval(37, 49), Interval(57, 69), Interval(8, 10),
         Interval(12, 16), Interval(67, 73), Interval(41, 51), Interval(31, 33), Interval(51, 57),
         Interval(16, 18), Interval(80, 90), Interval(6, 6), Interval(12, 12), Interval(10, 12)],
        # Job 77
        [Interval(82, 96), Interval(17, 21), Interval(22, 28), Interval(53, 71), Interval(65, 79),
         Interval(20, 22), Interval(31, 33), Interval(53, 59), Interval(52, 70), Interval(23, 23),
         Interval(33, 33), Interval(60, 72), Interval(64, 66), Interval(10, 10), Interval(23, 31),
         Interval(38, 40), Interval(41, 51), Interval(27, 35), Interval(20, 26), Interval(23, 25)],
        # Job 78
        [Interval(14, 16), Interval(86, 112), Interval(13, 15), Interval(31, 35), Interval(71, 91),
         Interval(39, 39), Interval(43, 55), Interval(90, 102), Interval(30, 32), Interval(56, 68),
         Interval(34, 46), Interval(50, 58), Interval(53, 53), Interval(78, 104), Interval(83, 91),
         Interval(36, 36), Interval(72, 86), Interval(25, 29), Interval(2, 2), Interval(32, 36)],
        # Job 79
        [Interval(35, 47), Interval(13, 17), Interval(26, 28), Interval(90, 90), Interval(90, 92),
         Interval(2, 2), Interval(68, 70), Interval(89, 89), Interval(26, 34), Interval(66, 68),
         Interval(35, 39), Interval(21, 23), Interval(70, 88), Interval(67, 89), Interval(64, 82),
         Interval(70, 72), Interval(61, 73), Interval(46, 50), Interval(9, 11), Interval(46, 62)],
        # Job 80
        [Interval(58, 64), Interval(2, 2), Interval(25, 29), Interval(17, 23), Interval(75, 75),
         Interval(2, 2), Interval(58, 58), Interval(34, 38), Interval(49, 59), Interval(42, 50),
         Interval(85, 85), Interval(23, 31), Interval(55, 71), Interval(40, 44), Interval(80, 96),
         Interval(69, 81), Interval(27, 33), Interval(41, 51), Interval(18, 20), Interval(12, 12)],
        # Job 81
        [Interval(19, 19), Interval(51, 67), Interval(69, 77), Interval(86, 94), Interval(17, 23),
         Interval(27, 27), Interval(32, 40), Interval(15, 17), Interval(53, 53), Interval(64, 72),
         Interval(10, 10), Interval(55, 63), Interval(75, 91), Interval(21, 23), Interval(6, 6),
         Interval(83, 99), Interval(20, 24), Interval(69, 79), Interval(92, 106), Interval(60, 62)],
        # Job 82
        [Interval(85, 109), Interval(81, 89), Interval(28, 30), Interval(18, 22), Interval(85, 113),
         Interval(27, 31), Interval(48, 50), Interval(74, 98), Interval(82, 110), Interval(72, 94),
         Interval(12, 16), Interval(94, 96), Interval(15, 19), Interval(42, 48), Interval(56, 74),
         Interval(43, 53), Interval(60, 68), Interval(8, 10), Interval(26, 26), Interval(35, 37)],
        # Job 83
        [Interval(54, 64), Interval(49, 59), Interval(75, 79), Interval(88, 110), Interval(86, 94),
         Interval(55, 67), Interval(64, 66), Interval(50, 66), Interval(36, 48), Interval(81, 91),
         Interval(59, 69), Interval(3, 3), Interval(49, 61), Interval(69, 89), Interval(80, 96),
         Interval(12, 14), Interval(57, 69), Interval(62, 70), Interval(77, 89), Interval(77, 93)],
        # Job 84
        [Interval(86, 98), Interval(28, 30), Interval(55, 69), Interval(78, 84), Interval(70, 92),
         Interval(85, 109), Interval(90, 102), Interval(63, 69), Interval(71, 91), Interval(74, 76),
         Interval(93, 93), Interval(48, 54), Interval(67, 79), Interval(70, 82), Interval(30, 36),
         Interval(33, 35), Interval(86, 104), Interval(4, 4), Interval(55, 63), Interval(68, 70)],
        # Job 85
        [Interval(18, 18), Interval(51, 67), Interval(13, 17), Interval(52, 60), Interval(82, 88),
         Interval(31, 33), Interval(62, 74), Interval(66, 74), Interval(23, 25), Interval(48, 58),
         Interval(12, 12), Interval(67, 71), Interval(35, 35), Interval(77, 101), Interval(6, 6),
         Interval(35, 47), Interval(78, 96), Interval(41, 41), Interval(85, 85), Interval(48, 54)],
        # Job 86
        [Interval(4, 4), Interval(65, 75), Interval(76, 92), Interval(79, 81), Interval(17, 17),
         Interval(38, 48), Interval(50, 50), Interval(15, 19), Interval(50, 50), Interval(63, 69),
         Interval(22, 26), Interval(15, 15), Interval(83, 97), Interval(82, 84), Interval(40, 50),
         Interval(14, 16), Interval(68, 76), Interval(25, 27), Interval(84, 94), Interval(74, 92)],
        # Job 87
        [Interval(13, 13), Interval(51, 53), Interval(77, 99), Interval(51, 57), Interval(44, 56),
         Interval(56, 62), Interval(48, 54), Interval(31, 41), Interval(82, 92), Interval(88, 108),
         Interval(24, 28), Interval(56, 56), Interval(86, 92), Interval(37, 39), Interval(48, 48),
         Interval(58, 58), Interval(3, 3), Interval(67, 77), Interval(9, 11), Interval(69, 93)],
        # Job 88
        [Interval(63, 63), Interval(25, 33), Interval(55, 73), Interval(49, 51), Interval(10, 12),
         Interval(36, 40), Interval(18, 20), Interval(7, 7), Interval(52, 66), Interval(39, 41),
         Interval(51, 61), Interval(5, 5), Interval(55, 63), Interval(80, 86), Interval(44, 48),
         Interval(38, 44), Interval(84, 96), Interval(4, 4), Interval(24, 24), Interval(32, 36)],
        # Job 89
        [Interval(9, 9), Interval(82, 82), Interval(65, 73), Interval(14, 14), Interval(68, 86),
         Interval(39, 39), Interval(25, 29), Interval(90, 106), Interval(7, 9), Interval(46, 60),
         Interval(14, 16), Interval(1, 1), Interval(65, 71), Interval(55, 57), Interval(66, 78),
         Interval(60, 62), Interval(43, 55), Interval(34, 36), Interval(59, 75), Interval(18, 24)],
        # Job 90
        [Interval(78, 90), Interval(35, 47), Interval(74, 82), Interval(52, 54), Interval(82, 82),
         Interval(28, 36), Interval(48, 54), Interval(26, 28), Interval(54, 58), Interval(4, 4),
         Interval(19, 19), Interval(40, 42), Interval(71, 89), Interval(31, 35), Interval(69, 73),
         Interval(17, 19), Interval(13, 13), Interval(3, 3), Interval(39, 47), Interval(83, 107)],
        # Job 91
        [Interval(66, 70), Interval(52, 66), Interval(64, 70), Interval(23, 25), Interval(2, 2),
         Interval(62, 76), Interval(42, 48), Interval(75, 95), Interval(44, 58), Interval(40, 52),
         Interval(81, 91), Interval(11, 11), Interval(2, 2), Interval(84, 110), Interval(46, 60),
         Interval(43, 45), Interval(62, 66), Interval(29, 37), Interval(29, 35), Interval(48, 58)],
        # Job 92
        [Interval(21, 27), Interval(86, 108), Interval(11, 11), Interval(68, 70), Interval(6, 6),
         Interval(12, 12), Interval(81, 87), Interval(29, 35), Interval(1, 1), Interval(84, 96),
         Interval(30, 34), Interval(84, 112), Interval(71, 87), Interval(34, 38), Interval(51, 61),
         Interval(1, 1), Interval(17, 17), Interval(79, 89), Interval(72, 88), Interval(59, 69)],
        # Job 93
        [Interval(47, 47), Interval(60, 68), Interval(15, 17), Interval(64, 64), Interval(68, 70),
         Interval(15, 17), Interval(44, 46), Interval(56, 68), Interval(15, 17), Interval(5, 5),
         Interval(26, 26), Interval(69, 71), Interval(48, 48), Interval(54, 62), Interval(67, 83),
         Interval(12, 14), Interval(11, 11), Interval(47, 47), Interval(43, 57), Interval(27, 31)],
        # Job 94
        [Interval(66, 78), Interval(46, 56), Interval(14, 18), Interval(29, 35), Interval(43, 43),
         Interval(56, 66), Interval(11, 11), Interval(1, 1), Interval(71, 77), Interval(15, 19),
         Interval(15, 15), Interval(72, 72), Interval(84, 90), Interval(76, 86), Interval(26, 26),
         Interval(26, 26), Interval(63, 85), Interval(30, 30), Interval(68, 90), Interval(40, 40)],
        # Job 95
        [Interval(54, 64), Interval(69, 69), Interval(96, 100), Interval(54, 66), Interval(66, 80),
         Interval(37, 37), Interval(32, 38), Interval(42, 52), Interval(15, 19), Interval(91, 95),
         Interval(83, 83), Interval(26, 28), Interval(91, 99), Interval(75, 79), Interval(61, 73),
         Interval(29, 31), Interval(69, 87), Interval(26, 26), Interval(41, 49), Interval(47, 63)],
        # Job 96
        [Interval(41, 43), Interval(90, 96), Interval(85, 91), Interval(81, 97), Interval(27, 35),
         Interval(87, 91), Interval(51, 67), Interval(81, 91), Interval(24, 32), Interval(21, 25),
         Interval(4, 4), Interval(71, 73), Interval(40, 46), Interval(27, 29), Interval(46, 58),
         Interval(17, 19), Interval(58, 62), Interval(86, 96), Interval(77, 95), Interval(6, 6)],
        # Job 97
        [Interval(82, 86), Interval(7, 9), Interval(75, 93), Interval(65, 69), Interval(75, 93),
         Interval(10, 12), Interval(76, 102), Interval(34, 42), Interval(11, 13), Interval(68, 80),
         Interval(12, 16), Interval(49, 51), Interval(77, 89), Interval(40, 44), Interval(75, 79),
         Interval(76, 100), Interval(57, 59), Interval(51, 65), Interval(8, 8), Interval(17, 17)],
        # Job 98
        [Interval(26, 30), Interval(14, 16), Interval(85, 109), Interval(29, 33), Interval(15, 15),
         Interval(33, 37), Interval(8, 10), Interval(54, 64), Interval(48, 52), Interval(95, 101),
         Interval(76, 96), Interval(6, 6), Interval(48, 50), Interval(24, 24), Interval(82, 96),
         Interval(50, 62), Interval(76, 94), Interval(12, 16), Interval(67, 89), Interval(20, 20)],
        # Job 99
        [Interval(46, 56), Interval(23, 27), Interval(53, 59), Interval(61, 73), Interval(49, 53),
         Interval(42, 46), Interval(80, 80), Interval(63, 69), Interval(23, 23), Interval(74, 74),
         Interval(12, 12), Interval(47, 57), Interval(12, 14), Interval(4, 4), Interval(36, 36),
         Interval(64, 74), Interval(5, 5), Interval(20, 22), Interval(52, 62), Interval(73, 85)],
    ],
    'name': 'INT__TAI100_20_05.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai100_20_05_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI100_20_05.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI100_20_05.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI100_20_05_F_15_01_INTERVAL_DATA
