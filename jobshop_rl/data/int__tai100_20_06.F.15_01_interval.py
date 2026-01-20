"""
Problema INT__TAI100_20_06.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI100_20_06_F_15_01_INTERVAL_DATA = {
    'num_jobs': 100,
    'num_machines': 20,
    'problem_id': 'int__tai100_20_06.F.15_01_interval',
    'sequences': [
        [9, 19, 7, 6, 2, 13, 11, 18, 16, 8, 14, 3, 1, 4, 5, 0, 15, 10, 12, 17],
        [3, 2, 6, 15, 16, 18, 8, 14, 10, 12, 13, 1, 17, 0, 5, 11, 7, 4, 9, 19],
        [12, 11, 13, 16, 7, 9, 3, 19, 10, 14, 2, 0, 18, 6, 1, 17, 15, 5, 4, 8],
        [12, 19, 5, 11, 14, 4, 13, 7, 6, 15, 18, 1, 0, 3, 17, 2, 10, 16, 8, 9],
        [12, 2, 10, 11, 8, 18, 17, 6, 5, 13, 9, 14, 4, 16, 19, 15, 3, 1, 0, 7],
        [12, 14, 18, 0, 9, 3, 15, 16, 2, 13, 17, 7, 11, 10, 5, 19, 8, 4, 1, 6],
        [2, 18, 8, 10, 17, 12, 19, 9, 7, 4, 11, 14, 1, 3, 0, 16, 13, 15, 6, 5],
        [5, 11, 0, 18, 16, 6, 3, 7, 13, 9, 10, 14, 19, 15, 12, 1, 17, 8, 4, 2],
        [8, 1, 7, 15, 17, 12, 14, 18, 16, 0, 3, 13, 9, 4, 19, 11, 10, 6, 5, 2],
        [11, 13, 0, 4, 8, 19, 14, 2, 17, 12, 18, 6, 3, 5, 10, 15, 16, 1, 7, 9],
        [0, 9, 2, 7, 4, 3, 15, 17, 6, 1, 10, 8, 19, 5, 16, 18, 11, 14, 12, 13],
        [16, 11, 6, 13, 17, 14, 2, 5, 1, 4, 8, 9, 15, 19, 3, 0, 18, 7, 12, 10],
        [11, 14, 18, 8, 1, 9, 5, 10, 2, 3, 16, 0, 4, 17, 13, 19, 6, 12, 15, 7],
        [3, 19, 14, 10, 16, 7, 0, 1, 12, 5, 11, 6, 18, 8, 4, 2, 15, 9, 13, 17],
        [6, 9, 11, 4, 14, 8, 10, 19, 5, 12, 18, 17, 3, 15, 0, 1, 16, 13, 7, 2],
        [6, 1, 5, 18, 13, 15, 9, 3, 7, 8, 16, 14, 10, 4, 17, 11, 12, 0, 19, 2],
        [12, 16, 2, 3, 0, 18, 9, 10, 19, 4, 13, 15, 6, 17, 7, 5, 11, 8, 1, 14],
        [6, 15, 0, 5, 2, 12, 19, 10, 3, 7, 13, 4, 11, 16, 8, 1, 18, 14, 9, 17],
        [4, 1, 15, 19, 0, 18, 16, 14, 12, 11, 3, 9, 10, 8, 2, 17, 6, 5, 7, 13],
        [12, 19, 13, 8, 10, 14, 17, 1, 7, 3, 4, 18, 5, 6, 2, 15, 0, 11, 16, 9],
        [15, 12, 11, 19, 3, 0, 14, 4, 1, 13, 18, 8, 17, 2, 7, 5, 16, 6, 10, 9],
        [4, 6, 5, 7, 1, 2, 13, 3, 9, 18, 16, 15, 12, 0, 11, 17, 10, 8, 14, 19],
        [19, 17, 18, 12, 5, 15, 0, 8, 4, 1, 6, 10, 13, 16, 14, 2, 7, 11, 9, 3],
        [16, 15, 18, 8, 1, 7, 17, 10, 0, 9, 12, 14, 11, 5, 13, 6, 3, 4, 2, 19],
        [12, 11, 1, 0, 8, 6, 15, 3, 17, 9, 7, 19, 13, 18, 14, 4, 16, 5, 10, 2],
        [9, 1, 19, 16, 7, 5, 17, 11, 8, 0, 2, 3, 18, 4, 12, 15, 10, 14, 13, 6],
        [10, 5, 15, 16, 2, 9, 4, 0, 8, 19, 14, 13, 1, 12, 17, 18, 11, 3, 7, 6],
        [8, 5, 9, 19, 2, 11, 18, 4, 3, 7, 12, 1, 6, 10, 14, 15, 16, 0, 17, 13],
        [4, 6, 12, 5, 9, 15, 0, 16, 11, 3, 7, 8, 17, 18, 13, 19, 2, 10, 14, 1],
        [16, 15, 10, 3, 5, 14, 12, 18, 13, 0, 1, 8, 19, 17, 7, 4, 2, 11, 6, 9],
        [11, 5, 3, 4, 0, 9, 16, 17, 13, 12, 18, 10, 2, 1, 14, 19, 7, 15, 8, 6],
        [15, 2, 11, 12, 5, 1, 10, 3, 7, 14, 18, 19, 13, 4, 17, 8, 6, 9, 0, 16],
        [16, 17, 13, 2, 1, 6, 14, 4, 18, 15, 19, 0, 12, 8, 9, 10, 5, 3, 11, 7],
        [14, 0, 17, 19, 18, 11, 4, 3, 12, 15, 10, 13, 16, 9, 7, 2, 1, 5, 6, 8],
        [16, 15, 14, 6, 4, 5, 1, 19, 0, 10, 2, 12, 17, 13, 8, 9, 3, 7, 11, 18],
        [14, 3, 5, 18, 6, 16, 1, 19, 10, 2, 12, 9, 0, 4, 17, 7, 13, 11, 15, 8],
        [10, 16, 7, 11, 14, 5, 13, 12, 17, 6, 9, 2, 3, 1, 8, 15, 18, 0, 19, 4],
        [5, 15, 13, 16, 18, 19, 8, 11, 4, 6, 3, 2, 0, 17, 1, 10, 12, 14, 9, 7],
        [13, 0, 11, 7, 18, 5, 6, 8, 14, 4, 9, 10, 19, 15, 1, 2, 3, 12, 17, 16],
        [5, 11, 13, 9, 17, 3, 14, 12, 19, 4, 16, 1, 15, 2, 18, 0, 10, 8, 7, 6],
        [1, 7, 15, 9, 19, 5, 17, 8, 2, 11, 3, 12, 6, 0, 14, 10, 16, 13, 18, 4],
        [12, 13, 6, 18, 8, 2, 14, 1, 16, 4, 7, 9, 0, 19, 5, 11, 10, 3, 17, 15],
        [5, 13, 9, 11, 10, 16, 4, 18, 0, 17, 8, 3, 14, 2, 7, 19, 12, 6, 15, 1],
        [10, 1, 17, 2, 19, 14, 0, 8, 15, 16, 3, 9, 18, 4, 12, 7, 6, 5, 11, 13],
        [19, 13, 3, 7, 10, 6, 9, 2, 14, 11, 17, 12, 4, 16, 5, 15, 18, 8, 0, 1],
        [16, 12, 14, 19, 9, 8, 15, 18, 0, 6, 2, 11, 13, 7, 4, 3, 1, 5, 17, 10],
        [4, 3, 10, 15, 11, 5, 0, 12, 14, 1, 2, 19, 16, 18, 8, 6, 7, 17, 9, 13],
        [1, 19, 5, 14, 12, 13, 18, 9, 7, 16, 0, 6, 10, 15, 17, 4, 11, 2, 8, 3],
        [4, 6, 3, 13, 1, 10, 2, 5, 18, 16, 17, 7, 15, 8, 9, 19, 0, 14, 11, 12],
        [19, 6, 0, 3, 5, 4, 12, 8, 2, 7, 17, 18, 9, 1, 10, 14, 13, 16, 15, 11],
        [9, 18, 12, 10, 1, 2, 13, 6, 8, 17, 7, 4, 11, 3, 0, 15, 19, 16, 14, 5],
        [11, 1, 2, 15, 13, 8, 4, 10, 16, 14, 12, 17, 18, 6, 5, 0, 3, 19, 7, 9],
        [16, 12, 10, 2, 6, 18, 9, 17, 0, 1, 15, 4, 19, 11, 7, 13, 8, 5, 14, 3],
        [13, 5, 8, 19, 9, 15, 1, 10, 4, 17, 18, 14, 2, 0, 7, 3, 16, 12, 11, 6],
        [14, 2, 3, 6, 12, 5, 16, 19, 4, 1, 9, 7, 0, 15, 11, 17, 18, 13, 10, 8],
        [2, 11, 0, 15, 19, 6, 4, 3, 17, 14, 9, 16, 18, 8, 1, 13, 5, 7, 10, 12],
        [6, 15, 9, 0, 14, 8, 13, 1, 4, 5, 17, 18, 12, 10, 19, 11, 2, 7, 16, 3],
        [13, 2, 12, 3, 5, 6, 17, 19, 8, 10, 16, 0, 15, 11, 18, 9, 7, 1, 4, 14],
        [19, 7, 15, 14, 10, 9, 4, 17, 13, 2, 8, 6, 11, 1, 18, 16, 3, 0, 12, 5],
        [12, 0, 17, 18, 6, 5, 11, 3, 2, 10, 15, 7, 9, 13, 8, 1, 4, 14, 19, 16],
        [3, 0, 14, 5, 4, 15, 2, 17, 12, 10, 16, 7, 6, 11, 8, 9, 19, 13, 18, 1],
        [7, 4, 15, 13, 11, 9, 1, 8, 6, 0, 12, 18, 19, 14, 3, 16, 10, 2, 17, 5],
        [7, 4, 1, 19, 6, 14, 13, 12, 0, 17, 11, 18, 5, 15, 10, 8, 9, 3, 16, 2],
        [1, 9, 5, 14, 17, 0, 3, 2, 18, 13, 4, 11, 12, 6, 8, 19, 7, 10, 16, 15],
        [1, 18, 12, 0, 5, 11, 9, 14, 2, 15, 8, 6, 3, 17, 10, 13, 7, 4, 19, 16],
        [8, 19, 18, 7, 4, 16, 6, 15, 9, 12, 1, 14, 17, 2, 10, 3, 0, 13, 11, 5],
        [7, 2, 1, 6, 11, 12, 14, 18, 9, 15, 3, 8, 17, 16, 19, 0, 13, 4, 5, 10],
        [16, 3, 5, 10, 15, 8, 6, 14, 13, 19, 18, 7, 17, 11, 2, 0, 4, 12, 1, 9],
        [5, 11, 1, 0, 16, 10, 6, 2, 7, 8, 12, 14, 18, 4, 15, 19, 17, 9, 13, 3],
        [8, 3, 2, 14, 0, 1, 16, 6, 11, 9, 4, 18, 19, 10, 5, 17, 13, 7, 12, 15],
        [2, 16, 9, 6, 19, 3, 0, 7, 12, 17, 18, 5, 14, 10, 4, 13, 15, 11, 1, 8],
        [11, 7, 15, 14, 2, 0, 1, 4, 12, 9, 3, 19, 16, 5, 17, 10, 13, 18, 8, 6],
        [15, 11, 8, 14, 3, 13, 18, 0, 4, 6, 1, 17, 19, 12, 9, 5, 2, 7, 16, 10],
        [6, 17, 5, 0, 7, 15, 18, 19, 1, 12, 2, 10, 4, 8, 3, 9, 14, 16, 13, 11],
        [16, 6, 17, 5, 11, 9, 13, 19, 1, 14, 2, 7, 8, 18, 0, 15, 4, 12, 10, 3],
        [3, 5, 17, 15, 6, 13, 12, 16, 14, 10, 0, 18, 1, 7, 8, 11, 4, 19, 2, 9],
        [12, 15, 19, 3, 10, 16, 2, 18, 11, 7, 9, 8, 17, 13, 0, 1, 4, 5, 14, 6],
        [5, 6, 12, 3, 4, 10, 15, 0, 17, 14, 19, 8, 7, 16, 9, 13, 1, 11, 2, 18],
        [1, 17, 18, 15, 0, 14, 5, 11, 8, 3, 16, 6, 2, 9, 13, 4, 12, 7, 10, 19],
        [8, 6, 1, 10, 5, 12, 0, 11, 2, 3, 4, 15, 17, 13, 19, 18, 7, 14, 9, 16],
        [0, 14, 18, 15, 5, 7, 12, 11, 10, 16, 6, 9, 19, 2, 3, 8, 17, 4, 13, 1],
        [10, 2, 18, 13, 11, 9, 14, 4, 15, 12, 19, 17, 1, 3, 6, 16, 0, 8, 7, 5],
        [10, 4, 7, 18, 8, 9, 17, 19, 1, 14, 16, 15, 11, 13, 5, 0, 2, 3, 12, 6],
        [0, 3, 1, 19, 15, 8, 16, 11, 13, 10, 5, 9, 6, 7, 17, 12, 14, 4, 18, 2],
        [10, 6, 8, 2, 7, 15, 13, 9, 18, 12, 16, 1, 17, 11, 14, 5, 4, 3, 19, 0],
        [18, 12, 6, 19, 15, 16, 1, 2, 7, 3, 17, 4, 0, 9, 11, 13, 14, 10, 8, 5],
        [9, 15, 8, 14, 0, 7, 3, 18, 4, 13, 2, 12, 6, 19, 5, 16, 11, 17, 10, 1],
        [16, 18, 15, 0, 6, 2, 12, 14, 3, 11, 9, 13, 7, 8, 5, 19, 10, 17, 4, 1],
        [9, 6, 12, 18, 15, 11, 17, 3, 7, 14, 10, 0, 4, 16, 19, 8, 1, 2, 13, 5],
        [16, 13, 17, 14, 12, 15, 18, 8, 19, 6, 2, 11, 5, 10, 0, 3, 4, 1, 9, 7],
        [16, 2, 14, 3, 19, 9, 6, 17, 15, 0, 7, 11, 5, 12, 18, 8, 10, 1, 13, 4],
        [13, 9, 1, 18, 7, 12, 19, 2, 11, 6, 17, 3, 16, 14, 15, 4, 8, 0, 5, 10],
        [3, 19, 9, 16, 14, 5, 4, 6, 15, 11, 1, 7, 8, 10, 2, 13, 0, 17, 18, 12],
        [11, 7, 15, 16, 3, 2, 12, 5, 17, 19, 14, 6, 9, 10, 8, 18, 0, 13, 1, 4],
        [8, 15, 13, 14, 18, 16, 19, 0, 7, 17, 12, 11, 4, 1, 3, 9, 6, 2, 5, 10],
        [17, 8, 2, 11, 9, 4, 10, 15, 5, 19, 0, 14, 6, 16, 18, 3, 7, 12, 1, 13],
        [0, 18, 12, 4, 8, 14, 5, 6, 16, 13, 2, 7, 9, 15, 17, 1, 3, 19, 11, 10],
        [9, 15, 14, 12, 7, 3, 5, 19, 0, 2, 1, 8, 4, 16, 6, 18, 10, 11, 13, 17],
        [19, 4, 10, 18, 1, 17, 0, 8, 5, 9, 14, 6, 12, 7, 2, 15, 3, 13, 16, 11],
        [4, 11, 9, 17, 0, 12, 14, 1, 19, 13, 2, 3, 15, 16, 6, 8, 10, 7, 5, 18],
    ],
    'durations': [
        # Job 0
        [Interval(47, 59), Interval(44, 52), Interval(17, 17), Interval(39, 45), Interval(63, 77),
         Interval(86, 112), Interval(22, 24), Interval(68, 90), Interval(36, 48), Interval(79, 97),
         Interval(21, 25), Interval(74, 80), Interval(51, 67), Interval(44, 46), Interval(76, 92),
         Interval(54, 62), Interval(44, 50), Interval(78, 104), Interval(25, 33), Interval(42, 54)],
        # Job 1
        [Interval(51, 53), Interval(71, 77), Interval(35, 35), Interval(3, 3), Interval(41, 49),
         Interval(36, 36), Interval(89, 95), Interval(19, 21), Interval(53, 63), Interval(14, 14),
         Interval(5, 5), Interval(80, 106), Interval(42, 50), Interval(32, 40), Interval(85, 103),
         Interval(76, 76), Interval(61, 65), Interval(89, 101), Interval(59, 73), Interval(43, 55)],
        # Job 2
        [Interval(42, 42), Interval(56, 68), Interval(74, 92), Interval(56, 62), Interval(55, 65),
         Interval(8, 8), Interval(13, 17), Interval(10, 10), Interval(1, 1), Interval(67, 89),
         Interval(25, 29), Interval(95, 101), Interval(32, 38), Interval(22, 22), Interval(76, 84),
         Interval(70, 84), Interval(84, 88), Interval(63, 63), Interval(38, 50), Interval(38, 40)],
        # Job 3
        [Interval(10, 10), Interval(6, 6), Interval(60, 64), Interval(66, 68), Interval(62, 70),
         Interval(33, 43), Interval(19, 21), Interval(65, 87), Interval(91, 97), Interval(59, 75),
         Interval(29, 39), Interval(55, 63), Interval(25, 29), Interval(56, 66), Interval(9, 11),
         Interval(60, 74), Interval(20, 22), Interval(83, 97), Interval(64, 82), Interval(13, 15)],
        # Job 4
        [Interval(15, 19), Interval(35, 39), Interval(21, 21), Interval(87, 95), Interval(6, 8),
         Interval(42, 46), Interval(19, 25), Interval(44, 56), Interval(31, 31), Interval(73, 91),
         Interval(51, 55), Interval(21, 21), Interval(76, 102), Interval(31, 39), Interval(42, 54),
         Interval(16, 16), Interval(65, 75), Interval(93, 93), Interval(36, 46), Interval(5, 5)],
        # Job 5
        [Interval(57, 69), Interval(67, 69), Interval(42, 48), Interval(35, 47), Interval(72, 84),
         Interval(73, 75), Interval(97, 97), Interval(14, 14), Interval(46, 50), Interval(52, 56),
         Interval(78, 104), Interval(82, 102), Interval(86, 96), Interval(61, 67), Interval(56, 66),
         Interval(6, 6), Interval(6, 6), Interval(59, 61), Interval(63, 67), Interval(67, 79)],
        # Job 6
        [Interval(86, 96), Interval(56, 60), Interval(70, 80), Interval(11, 11), Interval(7, 7),
         Interval(79, 93), Interval(64, 76), Interval(25, 27), Interval(48, 58), Interval(5, 5),
         Interval(69, 93), Interval(62, 70), Interval(49, 65), Interval(71, 83), Interval(87, 91),
         Interval(47, 51), Interval(3, 3), Interval(52, 66), Interval(82, 104), Interval(35, 39)],
        # Job 7
        [Interval(32, 34), Interval(87, 107), Interval(71, 91), Interval(31, 39), Interval(82, 84),
         Interval(27, 29), Interval(44, 50), Interval(29, 39), Interval(22, 24), Interval(96, 96),
         Interval(27, 35), Interval(88, 100), Interval(63, 63), Interval(20, 22), Interval(1, 1),
         Interval(51, 61), Interval(33, 39), Interval(46, 54), Interval(79, 103), Interval(86, 90)],
        # Job 8
        [Interval(32, 42), Interval(68, 72), Interval(38, 38), Interval(75, 93), Interval(23, 27),
         Interval(28, 36), Interval(67, 77), Interval(35, 39), Interval(22, 24), Interval(12, 16),
         Interval(41, 47), Interval(3, 3), Interval(25, 25), Interval(91, 91), Interval(90, 104),
         Interval(85, 91), Interval(56, 72), Interval(75, 87), Interval(65, 65), Interval(54, 64)],
        # Job 9
        [Interval(35, 45), Interval(21, 25), Interval(50, 54), Interval(37, 41), Interval(58, 70),
         Interval(9, 9), Interval(59, 71), Interval(22, 22), Interval(63, 79), Interval(51, 51),
         Interval(7, 7), Interval(6, 8), Interval(6, 8), Interval(29, 39), Interval(56, 62),
         Interval(2, 2), Interval(43, 47), Interval(41, 41), Interval(87, 105), Interval(19, 21)],
        # Job 10
        [Interval(44, 52), Interval(61, 65), Interval(41, 53), Interval(12, 12), Interval(54, 58),
         Interval(81, 91), Interval(82, 90), Interval(1, 1), Interval(18, 22), Interval(80, 80),
         Interval(77, 87), Interval(4, 4), Interval(8, 8), Interval(47, 63), Interval(81, 89),
         Interval(66, 84), Interval(19, 25), Interval(11, 11), Interval(44, 48), Interval(46, 50)],
        # Job 11
        [Interval(75, 77), Interval(54, 58), Interval(19, 19), Interval(6, 8), Interval(39, 49),
         Interval(88, 92), Interval(20, 26), Interval(11, 13), Interval(52, 62), Interval(90, 108),
         Interval(68, 82), Interval(22, 22), Interval(54, 64), Interval(84, 108), Interval(5, 5),
         Interval(67, 67), Interval(94, 94), Interval(58, 70), Interval(82, 94), Interval(66, 88)],
        # Job 12
        [Interval(80, 94), Interval(21, 23), Interval(14, 14), Interval(17, 21), Interval(91, 105),
         Interval(58, 78), Interval(43, 51), Interval(94, 100), Interval(10, 10), Interval(66, 76),
         Interval(66, 66), Interval(41, 43), Interval(18, 24), Interval(43, 55), Interval(76, 98),
         Interval(49, 49), Interval(53, 55), Interval(63, 85), Interval(87, 97), Interval(23, 27)],
        # Job 13
        [Interval(21, 23), Interval(59, 69), Interval(18, 24), Interval(42, 46), Interval(34, 34),
         Interval(38, 48), Interval(14, 14), Interval(73, 73), Interval(36, 40), Interval(54, 62),
         Interval(50, 54), Interval(24, 28), Interval(6, 6), Interval(48, 64), Interval(86, 110),
         Interval(2, 2), Interval(95, 101), Interval(43, 55), Interval(84, 98), Interval(60, 70)],
        # Job 14
        [Interval(58, 58), Interval(49, 63), Interval(73, 73), Interval(19, 25), Interval(63, 67),
         Interval(81, 107), Interval(93, 103), Interval(12, 14), Interval(23, 27), Interval(61, 71),
         Interval(35, 35), Interval(43, 57), Interval(8, 8), Interval(46, 48), Interval(33, 33),
         Interval(22, 26), Interval(46, 60), Interval(37, 41), Interval(40, 46), Interval(85, 107)],
        # Job 15
        [Interval(89, 109), Interval(68, 76), Interval(40, 40), Interval(86, 90), Interval(37, 41),
         Interval(25, 27), Interval(56, 58), Interval(81, 81), Interval(55, 71), Interval(67, 75),
         Interval(86, 100), Interval(56, 62), Interval(12, 12), Interval(66, 76), Interval(83, 91),
         Interval(46, 58), Interval(64, 70), Interval(26, 28), Interval(60, 80), Interval(81, 101)],
        # Job 16
        [Interval(62, 64), Interval(82, 92), Interval(66, 78), Interval(42, 46), Interval(17, 23),
         Interval(77, 77), Interval(46, 50), Interval(32, 36), Interval(57, 67), Interval(61, 67),
         Interval(26, 26), Interval(60, 76), Interval(83, 101), Interval(18, 18), Interval(48, 54),
         Interval(41, 45), Interval(14, 16), Interval(66, 74), Interval(20, 26), Interval(55, 57)],
        # Job 17
        [Interval(6, 6), Interval(39, 39), Interval(59, 71), Interval(40, 54), Interval(66, 72),
         Interval(15, 19), Interval(33, 37), Interval(84, 104), Interval(49, 55), Interval(50, 66),
         Interval(59, 67), Interval(57, 69), Interval(77, 101), Interval(56, 56), Interval(27, 33),
         Interval(21, 27), Interval(33, 41), Interval(3, 3), Interval(52, 70), Interval(11, 13)],
        # Job 18
        [Interval(68, 92), Interval(44, 56), Interval(31, 39), Interval(43, 43), Interval(86, 106),
         Interval(3, 3), Interval(77, 85), Interval(10, 10), Interval(12, 16), Interval(30, 34),
         Interval(53, 55), Interval(19, 23), Interval(54, 60), Interval(71, 85), Interval(49, 63),
         Interval(7, 9), Interval(57, 63), Interval(34, 40), Interval(43, 51), Interval(2, 2)],
        # Job 19
        [Interval(86, 100), Interval(42, 50), Interval(40, 54), Interval(13, 13), Interval(83, 91),
         Interval(54, 66), Interval(77, 89), Interval(63, 75), Interval(31, 33), Interval(11, 13),
         Interval(2, 2), Interval(77, 101), Interval(3, 3), Interval(11, 13), Interval(14, 14),
         Interval(89, 109), Interval(67, 71), Interval(12, 12), Interval(76, 82), Interval(65, 79)],
        # Job 20
        [Interval(93, 105), Interval(49, 61), Interval(40, 48), Interval(14, 18), Interval(48, 50),
         Interval(76, 96), Interval(40, 40), Interval(37, 43), Interval(37, 45), Interval(36, 36),
         Interval(93, 93), Interval(33, 35), Interval(81, 95), Interval(85, 95), Interval(98, 100),
         Interval(32, 42), Interval(53, 55), Interval(75, 89), Interval(4, 4), Interval(53, 57)],
        # Job 21
        [Interval(28, 34), Interval(24, 28), Interval(11, 13), Interval(48, 48), Interval(35, 47),
         Interval(2, 2), Interval(25, 25), Interval(15, 19), Interval(29, 35), Interval(74, 80),
         Interval(92, 104), Interval(2, 2), Interval(75, 89), Interval(85, 99), Interval(32, 34),
         Interval(51, 55), Interval(51, 55), Interval(26, 30), Interval(27, 27), Interval(74, 98)],
        # Job 22
        [Interval(83, 89), Interval(52, 66), Interval(37, 43), Interval(41, 43), Interval(40, 52),
         Interval(75, 81), Interval(12, 16), Interval(6, 8), Interval(42, 56), Interval(6, 6),
         Interval(24, 32), Interval(11, 13), Interval(73, 73), Interval(31, 39), Interval(61, 67),
         Interval(49, 65), Interval(67, 87), Interval(63, 65), Interval(54, 72), Interval(14, 16)],
        # Job 23
        [Interval(16, 18), Interval(57, 61), Interval(60, 60), Interval(32, 42), Interval(83, 107),
         Interval(70, 86), Interval(59, 63), Interval(39, 51), Interval(51, 51), Interval(67, 67),
         Interval(31, 37), Interval(41, 49), Interval(46, 48), Interval(74, 98), Interval(72, 76),
         Interval(5, 5), Interval(61, 73), Interval(73, 85), Interval(26, 28), Interval(8, 10)],
        # Job 24
        [Interval(61, 79), Interval(20, 26), Interval(25, 33), Interval(68, 88), Interval(50, 58),
         Interval(3, 3), Interval(25, 29), Interval(82, 82), Interval(28, 32), Interval(80, 100),
         Interval(24, 30), Interval(86, 104), Interval(8, 8), Interval(9, 9), Interval(54, 62),
         Interval(41, 41), Interval(24, 26), Interval(79, 95), Interval(32, 38), Interval(22, 26)],
        # Job 25
        [Interval(34, 44), Interval(59, 65), Interval(71, 89), Interval(66, 82), Interval(24, 26),
         Interval(43, 43), Interval(68, 90), Interval(45, 59), Interval(12, 12), Interval(6, 6),
         Interval(65, 69), Interval(40, 52), Interval(32, 42), Interval(13, 15), Interval(35, 39),
         Interval(2, 2), Interval(80, 84), Interval(12, 12), Interval(38, 38), Interval(8, 10)],
        # Job 26
        [Interval(73, 95), Interval(81, 93), Interval(39, 41), Interval(12, 12), Interval(8, 10),
         Interval(53, 71), Interval(24, 30), Interval(65, 71), Interval(21, 27), Interval(75, 83),
         Interval(52, 52), Interval(16, 20), Interval(55, 59), Interval(86, 100), Interval(59, 63),
         Interval(15, 15), Interval(56, 66), Interval(20, 22), Interval(86, 100), Interval(51, 63)],
        # Job 27
        [Interval(48, 60), Interval(88, 90), Interval(28, 32), Interval(4, 4), Interval(36, 38),
         Interval(67, 77), Interval(1, 1), Interval(10, 10), Interval(60, 70), Interval(74, 88),
         Interval(21, 23), Interval(16, 18), Interval(62, 82), Interval(36, 46), Interval(47, 55),
         Interval(40, 44), Interval(19, 23), Interval(36, 42), Interval(1, 1), Interval(53, 65)],
        # Job 28
        [Interval(57, 73), Interval(76, 88), Interval(11, 11), Interval(76, 94), Interval(7, 9),
         Interval(50, 56), Interval(87, 91), Interval(27, 31), Interval(59, 61), Interval(20, 24),
         Interval(42, 50), Interval(25, 33), Interval(22, 22), Interval(64, 78), Interval(35, 35),
         Interval(6, 6), Interval(20, 24), Interval(67, 87), Interval(69, 69), Interval(26, 34)],
        # Job 29
        [Interval(37, 49), Interval(32, 38), Interval(82, 86), Interval(66, 70), Interval(76, 94),
         Interval(3, 3), Interval(10, 12), Interval(13, 13), Interval(60, 72), Interval(69, 79),
         Interval(28, 32), Interval(54, 54), Interval(12, 12), Interval(92, 96), Interval(77, 93),
         Interval(75, 97), Interval(69, 79), Interval(16, 18), Interval(87, 89), Interval(6, 6)],
        # Job 30
        [Interval(76, 86), Interval(3, 3), Interval(69, 69), Interval(70, 92), Interval(49, 55),
         Interval(55, 63), Interval(83, 93), Interval(89, 109), Interval(63, 63), Interval(35, 35),
         Interval(47, 49), Interval(26, 26), Interval(38, 50), Interval(38, 38), Interval(29, 35),
         Interval(4, 4), Interval(80, 80), Interval(38, 50), Interval(78, 94), Interval(79, 101)],
        # Job 31
        [Interval(33, 37), Interval(12, 16), Interval(55, 71), Interval(25, 25), Interval(6, 8),
         Interval(22, 22), Interval(62, 82), Interval(38, 38), Interval(56, 70), Interval(77, 83),
         Interval(60, 70), Interval(75, 93), Interval(7, 9), Interval(16, 20), Interval(76, 82),
         Interval(38, 46), Interval(93, 95), Interval(77, 101), Interval(28, 30), Interval(37, 43)],
        # Job 32
        [Interval(95, 101), Interval(69, 83), Interval(74, 100), Interval(64, 74), Interval(59, 71),
         Interval(57, 71), Interval(56, 60), Interval(6, 8), Interval(16, 20), Interval(7, 7),
         Interval(9, 9), Interval(31, 41), Interval(44, 52), Interval(41, 55), Interval(73, 93),
         Interval(43, 43), Interval(34, 36), Interval(84, 84), Interval(30, 34), Interval(74, 94)],
        # Job 33
        [Interval(21, 23), Interval(88, 102), Interval(86, 98), Interval(87, 103), Interval(61, 79),
         Interval(76, 92), Interval(3, 3), Interval(54, 58), Interval(29, 33), Interval(10, 10),
         Interval(30, 40), Interval(41, 53), Interval(89, 99), Interval(55, 67), Interval(41, 49),
         Interval(45, 49), Interval(4, 4), Interval(1, 1), Interval(31, 39), Interval(51, 55)],
        # Job 34
        [Interval(1, 1), Interval(21, 23), Interval(46, 46), Interval(78, 104), Interval(70, 86),
         Interval(48, 48), Interval(32, 32), Interval(87, 99), Interval(28, 28), Interval(89, 93),
         Interval(15, 17), Interval(52, 52), Interval(43, 53), Interval(41, 45), Interval(10, 12),
         Interval(63, 73), Interval(42, 46), Interval(46, 56), Interval(10, 12), Interval(29, 37)],
        # Job 35
        [Interval(26, 26), Interval(64, 66), Interval(81, 105), Interval(8, 8), Interval(38, 50),
         Interval(91, 105), Interval(43, 57), Interval(34, 38), Interval(5, 5), Interval(59, 77),
         Interval(6, 6), Interval(43, 55), Interval(46, 46), Interval(48, 62), Interval(1, 1),
         Interval(85, 103), Interval(12, 14), Interval(39, 39), Interval(77, 103), Interval(34, 46)],
        # Job 36
        [Interval(60, 66), Interval(27, 33), Interval(24, 24), Interval(40, 42), Interval(84, 110),
         Interval(71, 71), Interval(82, 102), Interval(91, 91), Interval(21, 23), Interval(91, 103),
         Interval(46, 52), Interval(34, 46), Interval(33, 41), Interval(32, 40), Interval(22, 24),
         Interval(78, 88), Interval(46, 60), Interval(70, 72), Interval(59, 69), Interval(71, 81)],
        # Job 37
        [Interval(36, 38), Interval(53, 67), Interval(77, 81), Interval(25, 25), Interval(82, 84),
         Interval(20, 22), Interval(10, 10), Interval(75, 81), Interval(75, 75), Interval(8, 10),
         Interval(66, 74), Interval(35, 37), Interval(41, 41), Interval(7, 9), Interval(1, 1),
         Interval(17, 21), Interval(1, 1), Interval(6, 6), Interval(67, 67), Interval(45, 47)],
        # Job 38
        [Interval(5, 5), Interval(25, 33), Interval(68, 84), Interval(14, 18), Interval(77, 85),
         Interval(9, 9), Interval(94, 94), Interval(74, 90), Interval(64, 78), Interval(5, 5),
         Interval(3, 3), Interval(34, 42), Interval(23, 27), Interval(73, 97), Interval(43, 47),
         Interval(58, 66), Interval(29, 31), Interval(51, 65), Interval(9, 11), Interval(17, 23)],
        # Job 39
        [Interval(73, 97), Interval(91, 107), Interval(26, 34), Interval(22, 24), Interval(90, 92),
         Interval(32, 32), Interval(56, 66), Interval(42, 42), Interval(10, 12), Interval(52, 60),
         Interval(33, 33), Interval(28, 32), Interval(23, 31), Interval(19, 19), Interval(13, 15),
         Interval(72, 90), Interval(20, 22), Interval(55, 57), Interval(57, 57), Interval(68, 68)],
        # Job 40
        [Interval(4, 4), Interval(20, 20), Interval(32, 42), Interval(60, 64), Interval(76, 82),
         Interval(61, 63), Interval(62, 80), Interval(18, 18), Interval(70, 94), Interval(6, 8),
         Interval(40, 44), Interval(93, 101), Interval(9, 11), Interval(6, 6), Interval(23, 27),
         Interval(62, 78), Interval(26, 28), Interval(85, 89), Interval(68, 70), Interval(51, 55)],
        # Job 41
        [Interval(14, 14), Interval(18, 20), Interval(36, 36), Interval(50, 54), Interval(75, 101),
         Interval(60, 74), Interval(2, 2), Interval(27, 33), Interval(77, 89), Interval(83, 89),
         Interval(85, 109), Interval(30, 36), Interval(23, 23), Interval(5, 5), Interval(40, 44),
         Interval(71, 83), Interval(40, 54), Interval(53, 63), Interval(21, 25), Interval(38, 50)],
        # Job 42
        [Interval(76, 88), Interval(67, 79), Interval(81, 101), Interval(69, 87), Interval(52, 56),
         Interval(1, 1), Interval(26, 34), Interval(8, 10), Interval(32, 42), Interval(3, 3),
         Interval(71, 71), Interval(26, 26), Interval(86, 110), Interval(66, 74), Interval(30, 40),
         Interval(54, 56), Interval(71, 73), Interval(45, 49), Interval(33, 37), Interval(74, 96)],
        # Job 43
        [Interval(32, 40), Interval(13, 15), Interval(92, 100), Interval(55, 67), Interval(3, 3),
         Interval(28, 32), Interval(85, 111), Interval(67, 83), Interval(39, 43), Interval(78, 80),
         Interval(95, 97), Interval(68, 78), Interval(54, 54), Interval(66, 78), Interval(26, 32),
         Interval(6, 6), Interval(30, 32), Interval(31, 33), Interval(30, 38), Interval(48, 52)],
        # Job 44
        [Interval(82, 104), Interval(15, 17), Interval(85, 107), Interval(64, 82), Interval(93, 95),
         Interval(31, 41), Interval(28, 30), Interval(37, 39), Interval(57, 69), Interval(13, 15),
         Interval(6, 8), Interval(7, 7), Interval(48, 64), Interval(51, 57), Interval(6, 8),
         Interval(77, 89), Interval(33, 33), Interval(52, 68), Interval(76, 100), Interval(51, 65)],
        # Job 45
        [Interval(60, 68), Interval(11, 11), Interval(12, 14), Interval(4, 4), Interval(69, 79),
         Interval(21, 25), Interval(78, 90), Interval(60, 64), Interval(8, 8), Interval(37, 47),
         Interval(90, 102), Interval(24, 28), Interval(41, 41), Interval(2, 2), Interval(26, 30),
         Interval(12, 16), Interval(87, 111), Interval(13, 15), Interval(58, 72), Interval(80, 80)],
        # Job 46
        [Interval(9, 11), Interval(96, 102), Interval(19, 21), Interval(79, 81), Interval(52, 68),
         Interval(2, 2), Interval(90, 106), Interval(87, 107), Interval(1, 1), Interval(1, 1),
         Interval(55, 63), Interval(1, 1), Interval(26, 26), Interval(94, 104), Interval(89, 89),
         Interval(35, 41), Interval(15, 15), Interval(43, 51), Interval(71, 77), Interval(12, 16)],
        # Job 47
        [Interval(46, 58), Interval(43, 57), Interval(12, 14), Interval(73, 73), Interval(79, 97),
         Interval(65, 69), Interval(74, 82), Interval(74, 90), Interval(17, 19), Interval(86, 86),
         Interval(25, 29), Interval(31, 37), Interval(25, 27), Interval(30, 30), Interval(17, 17),
         Interval(2, 2), Interval(74, 100), Interval(83, 87), Interval(37, 43), Interval(67, 87)],
        # Job 48
        [Interval(67, 73), Interval(92, 104), Interval(20, 26), Interval(28, 30), Interval(78, 98),
         Interval(27, 35), Interval(6, 8), Interval(87, 97), Interval(3, 3), Interval(78, 82),
         Interval(18, 18), Interval(38, 40), Interval(55, 59), Interval(53, 59), Interval(8, 8),
         Interval(1, 1), Interval(69, 89), Interval(87, 93), Interval(65, 83), Interval(51, 59)],
        # Job 49
        [Interval(22, 28), Interval(28, 30), Interval(50, 52), Interval(82, 84), Interval(83, 99),
         Interval(80, 106), Interval(43, 45), Interval(14, 18), Interval(23, 23), Interval(7, 7),
         Interval(54, 60), Interval(52, 60), Interval(72, 72), Interval(36, 46), Interval(62, 74),
         Interval(25, 25), Interval(58, 68), Interval(40, 46), Interval(75, 99), Interval(46, 60)],
        # Job 50
        [Interval(31, 39), Interval(11, 13), Interval(79, 99), Interval(38, 44), Interval(67, 73),
         Interval(18, 18), Interval(60, 80), Interval(59, 79), Interval(5, 5), Interval(53, 65),
         Interval(30, 30), Interval(29, 39), Interval(22, 24), Interval(37, 47), Interval(39, 51),
         Interval(91, 93), Interval(87, 97), Interval(58, 62), Interval(90, 106), Interval(39, 43)],
        # Job 51
        [Interval(59, 63), Interval(4, 4), Interval(30, 30), Interval(47, 53), Interval(45, 55),
         Interval(36, 42), Interval(39, 43), Interval(15, 15), Interval(20, 24), Interval(48, 62),
         Interval(37, 37), Interval(6, 8), Interval(75, 101), Interval(56, 60), Interval(89, 91),
         Interval(61, 67), Interval(6, 8), Interval(23, 23), Interval(18, 20), Interval(36, 38)],
        # Job 52
        [Interval(4, 4), Interval(53, 61), Interval(1, 1), Interval(73, 87), Interval(21, 21),
         Interval(32, 38), Interval(32, 32), Interval(97, 99), Interval(68, 88), Interval(44, 56),
         Interval(73, 85), Interval(49, 57), Interval(37, 43), Interval(18, 20), Interval(23, 27),
         Interval(80, 88), Interval(91, 91), Interval(44, 58), Interval(87, 103), Interval(4, 4)],
        # Job 53
        [Interval(64, 82), Interval(88, 96), Interval(24, 26), Interval(40, 42), Interval(52, 64),
         Interval(32, 40), Interval(47, 53), Interval(89, 91), Interval(98, 98), Interval(35, 43),
         Interval(83, 105), Interval(57, 71), Interval(13, 17), Interval(29, 29), Interval(25, 29),
         Interval(80, 98), Interval(50, 50), Interval(23, 29), Interval(34, 42), Interval(11, 11)],
        # Job 54
        [Interval(81, 83), Interval(34, 40), Interval(91, 107), Interval(30, 38), Interval(91, 97),
         Interval(45, 47), Interval(71, 77), Interval(39, 51), Interval(76, 80), Interval(40, 42),
         Interval(51, 65), Interval(43, 43), Interval(68, 74), Interval(57, 61), Interval(24, 26),
         Interval(48, 62), Interval(78, 90), Interval(46, 50), Interval(83, 85), Interval(54, 60)],
        # Job 55
        [Interval(10, 12), Interval(51, 55), Interval(36, 42), Interval(71, 91), Interval(64, 68),
         Interval(99, 99), Interval(65, 81), Interval(74, 78), Interval(7, 7), Interval(86, 96),
         Interval(31, 35), Interval(41, 53), Interval(12, 16), Interval(46, 56), Interval(22, 28),
         Interval(4, 4), Interval(13, 17), Interval(26, 26), Interval(69, 89), Interval(61, 79)],
        # Job 56
        [Interval(77, 81), Interval(97, 97), Interval(8, 10), Interval(50, 62), Interval(47, 53),
         Interval(43, 43), Interval(52, 58), Interval(32, 32), Interval(86, 96), Interval(73, 77),
         Interval(75, 91), Interval(17, 17), Interval(50, 60), Interval(41, 45), Interval(80, 80),
         Interval(56, 68), Interval(52, 68), Interval(3, 3), Interval(49, 63), Interval(33, 33)],
        # Job 57
        [Interval(92, 102), Interval(39, 41), Interval(32, 32), Interval(7, 7), Interval(81, 89),
         Interval(60, 60), Interval(17, 21), Interval(13, 13), Interval(49, 59), Interval(54, 70),
         Interval(45, 49), Interval(11, 11), Interval(31, 33), Interval(49, 49), Interval(57, 73),
         Interval(62, 76), Interval(67, 67), Interval(83, 109), Interval(6, 8), Interval(69, 73)],
        # Job 58
        [Interval(7, 7), Interval(53, 55), Interval(17, 21), Interval(12, 16), Interval(68, 68),
         Interval(72, 76), Interval(1, 1), Interval(58, 66), Interval(50, 56), Interval(46, 56),
         Interval(30, 40), Interval(20, 26), Interval(84, 92), Interval(65, 71), Interval(49, 57),
         Interval(36, 42), Interval(57, 73), Interval(64, 64), Interval(92, 94), Interval(80, 106)],
        # Job 59
        [Interval(9, 9), Interval(24, 32), Interval(6, 6), Interval(68, 78), Interval(68, 78),
         Interval(70, 72), Interval(6, 8), Interval(53, 61), Interval(86, 104), Interval(83, 103),
         Interval(53, 59), Interval(59, 75), Interval(23, 23), Interval(29, 31), Interval(96, 100),
         Interval(37, 37), Interval(31, 37), Interval(23, 31), Interval(39, 51), Interval(58, 66)],
        # Job 60
        [Interval(29, 35), Interval(70, 72), Interval(41, 53), Interval(14, 18), Interval(45, 55),
         Interval(87, 105), Interval(30, 32), Interval(9, 11), Interval(55, 71), Interval(9, 11),
         Interval(74, 74), Interval(85, 91), Interval(31, 33), Interval(46, 54), Interval(81, 105),
         Interval(41, 41), Interval(54, 56), Interval(5, 5), Interval(69, 69), Interval(77, 89)],
        # Job 61
        [Interval(4, 4), Interval(8, 8), Interval(89, 93), Interval(51, 57), Interval(51, 67),
         Interval(46, 56), Interval(54, 62), Interval(54, 56), Interval(55, 71), Interval(3, 3),
         Interval(58, 70), Interval(34, 42), Interval(21, 21), Interval(7, 9), Interval(69, 69),
         Interval(91, 95), Interval(95, 95), Interval(55, 67), Interval(37, 37), Interval(67, 81)],
        # Job 62
        [Interval(86, 86), Interval(42, 50), Interval(70, 72), Interval(84, 104), Interval(79, 89),
         Interval(71, 73), Interval(47, 55), Interval(74, 76), Interval(44, 48), Interval(17, 17),
         Interval(32, 38), Interval(20, 24), Interval(43, 43), Interval(57, 71), Interval(4, 4),
         Interval(31, 33), Interval(22, 22), Interval(69, 73), Interval(26, 26), Interval(61, 63)],
        # Job 63
        [Interval(40, 48), Interval(48, 62), Interval(11, 13), Interval(35, 41), Interval(31, 39),
         Interval(6, 6), Interval(53, 69), Interval(90, 96), Interval(16, 20), Interval(59, 65),
         Interval(37, 47), Interval(20, 26), Interval(9, 9), Interval(67, 75), Interval(69, 89),
         Interval(78, 90), Interval(86, 94), Interval(62, 72), Interval(85, 99), Interval(41, 55)],
        # Job 64
        [Interval(77, 79), Interval(20, 24), Interval(7, 9), Interval(81, 89), Interval(85, 99),
         Interval(7, 9), Interval(41, 49), Interval(38, 38), Interval(18, 22), Interval(33, 43),
         Interval(65, 81), Interval(50, 56), Interval(40, 48), Interval(17, 21), Interval(66, 84),
         Interval(35, 47), Interval(64, 78), Interval(6, 6), Interval(82, 86), Interval(72, 76)],
        # Job 65
        [Interval(30, 30), Interval(41, 41), Interval(18, 22), Interval(49, 49), Interval(58, 62),
         Interval(57, 61), Interval(37, 43), Interval(72, 72), Interval(30, 32), Interval(24, 28),
         Interval(49, 61), Interval(3, 3), Interval(56, 66), Interval(56, 58), Interval(52, 64),
         Interval(84, 90), Interval(84, 92), Interval(39, 41), Interval(92, 96), Interval(77, 79)],
        # Job 66
        [Interval(7, 9), Interval(13, 17), Interval(65, 67), Interval(46, 46), Interval(20, 24),
         Interval(65, 67), Interval(12, 14), Interval(6, 8), Interval(30, 30), Interval(63, 65),
         Interval(51, 59), Interval(29, 33), Interval(96, 96), Interval(70, 94), Interval(52, 68),
         Interval(13, 15), Interval(63, 63), Interval(56, 56), Interval(68, 74), Interval(63, 63)],
        # Job 67
        [Interval(28, 30), Interval(9, 11), Interval(72, 84), Interval(45, 47), Interval(83, 105),
         Interval(87, 107), Interval(76, 94), Interval(76, 96), Interval(59, 67), Interval(50, 50),
         Interval(45, 53), Interval(27, 27), Interval(58, 68), Interval(69, 93), Interval(4, 4),
         Interval(71, 89), Interval(8, 10), Interval(95, 95), Interval(6, 6), Interval(74, 92)],
        # Job 68
        [Interval(61, 65), Interval(24, 32), Interval(36, 38), Interval(58, 66), Interval(51, 61),
         Interval(71, 75), Interval(53, 55), Interval(60, 80), Interval(53, 53), Interval(6, 8),
         Interval(30, 40), Interval(59, 69), Interval(20, 24), Interval(93, 103), Interval(37, 45),
         Interval(6, 6), Interval(88, 88), Interval(20, 20), Interval(5, 5), Interval(78, 94)],
        # Job 69
        [Interval(76, 92), Interval(84, 84), Interval(18, 24), Interval(32, 38), Interval(48, 60),
         Interval(90, 106), Interval(92, 98), Interval(46, 62), Interval(63, 63), Interval(52, 66),
         Interval(65, 83), Interval(80, 100), Interval(59, 77), Interval(95, 101), Interval(39, 39),
         Interval(82, 84), Interval(5, 5), Interval(17, 21), Interval(69, 79), Interval(63, 83)],
        # Job 70
        [Interval(1, 1), Interval(41, 41), Interval(29, 33), Interval(10, 10), Interval(98, 100),
         Interval(94, 94), Interval(8, 10), Interval(69, 69), Interval(47, 63), Interval(87, 97),
         Interval(16, 18), Interval(82, 96), Interval(71, 75), Interval(10, 10), Interval(88, 108),
         Interval(34, 42), Interval(13, 13), Interval(45, 59), Interval(46, 50), Interval(79, 95)],
        # Job 71
        [Interval(70, 70), Interval(38, 42), Interval(16, 20), Interval(36, 46), Interval(25, 27),
         Interval(57, 73), Interval(6, 8), Interval(49, 63), Interval(28, 36), Interval(34, 40),
         Interval(28, 36), Interval(46, 50), Interval(69, 85), Interval(24, 28), Interval(79, 103),
         Interval(5, 5), Interval(33, 33), Interval(69, 79), Interval(90, 90), Interval(96, 98)],
        # Job 72
        [Interval(1, 1), Interval(49, 61), Interval(74, 86), Interval(26, 28), Interval(53, 63),
         Interval(80, 104), Interval(16, 20), Interval(91, 91), Interval(20, 26), Interval(90, 102),
         Interval(86, 86), Interval(36, 44), Interval(17, 17), Interval(38, 40), Interval(48, 50),
         Interval(29, 33), Interval(55, 65), Interval(50, 56), Interval(65, 83), Interval(23, 23)],
        # Job 73
        [Interval(63, 83), Interval(18, 20), Interval(80, 98), Interval(78, 102), Interval(27, 27),
         Interval(73, 95), Interval(72, 74), Interval(29, 31), Interval(47, 55), Interval(33, 33),
         Interval(72, 96), Interval(19, 23), Interval(37, 39), Interval(27, 31), Interval(33, 35),
         Interval(11, 13), Interval(51, 63), Interval(40, 52), Interval(8, 10), Interval(8, 8)],
        # Job 74
        [Interval(58, 72), Interval(37, 41), Interval(13, 17), Interval(65, 79), Interval(57, 73),
         Interval(6, 6), Interval(85, 113), Interval(81, 85), Interval(61, 69), Interval(77, 91),
         Interval(75, 95), Interval(80, 100), Interval(20, 26), Interval(40, 50), Interval(64, 84),
         Interval(87, 89), Interval(26, 26), Interval(40, 42), Interval(52, 70), Interval(25, 31)],
        # Job 75
        [Interval(85, 87), Interval(53, 67), Interval(45, 51), Interval(7, 9), Interval(16, 20),
         Interval(13, 15), Interval(63, 79), Interval(37, 45), Interval(71, 81), Interval(55, 59),
         Interval(69, 75), Interval(23, 23), Interval(71, 91), Interval(43, 57), Interval(57, 63),
         Interval(15, 15), Interval(30, 36), Interval(47, 61), Interval(59, 75), Interval(79, 81)],
        # Job 76
        [Interval(23, 27), Interval(17, 21), Interval(84, 92), Interval(58, 78), Interval(40, 40),
         Interval(41, 43), Interval(57, 63), Interval(26, 32), Interval(77, 97), Interval(52, 62),
         Interval(75, 79), Interval(23, 23), Interval(84, 98), Interval(32, 36), Interval(82, 110),
         Interval(20, 24), Interval(77, 91), Interval(23, 29), Interval(63, 69), Interval(68, 84)],
        # Job 77
        [Interval(40, 42), Interval(22, 24), Interval(31, 37), Interval(29, 33), Interval(65, 65),
         Interval(37, 49), Interval(47, 55), Interval(30, 40), Interval(37, 47), Interval(48, 64),
         Interval(26, 32), Interval(74, 84), Interval(21, 23), Interval(62, 70), Interval(58, 78),
         Interval(31, 33), Interval(21, 21), Interval(74, 90), Interval(42, 42), Interval(66, 66)],
        # Job 78
        [Interval(25, 33), Interval(23, 25), Interval(43, 53), Interval(12, 14), Interval(80, 106),
         Interval(63, 73), Interval(16, 18), Interval(44, 58), Interval(45, 53), Interval(69, 83),
         Interval(35, 45), Interval(88, 88), Interval(74, 96), Interval(40, 46), Interval(54, 58),
         Interval(28, 34), Interval(67, 87), Interval(81, 95), Interval(53, 53), Interval(46, 60)],
        # Job 79
        [Interval(17, 17), Interval(18, 18), Interval(33, 39), Interval(1, 1), Interval(50, 58),
         Interval(19, 21), Interval(82, 108), Interval(17, 23), Interval(54, 60), Interval(42, 42),
         Interval(3, 3), Interval(54, 56), Interval(18, 18), Interval(39, 39), Interval(75, 95),
         Interval(28, 28), Interval(20, 22), Interval(47, 51), Interval(6, 8), Interval(84, 112)],
        # Job 80
        [Interval(77, 101), Interval(95, 99), Interval(60, 72), Interval(16, 18), Interval(2, 2),
         Interval(29, 35), Interval(80, 108), Interval(67, 75), Interval(81, 93), Interval(40, 50),
         Interval(45, 45), Interval(21, 21), Interval(85, 97), Interval(27, 33), Interval(30, 36),
         Interval(20, 20), Interval(84, 110), Interval(29, 39), Interval(14, 16), Interval(22, 26)],
        # Job 81
        [Interval(53, 61), Interval(80, 98), Interval(70, 86), Interval(20, 22), Interval(58, 58),
         Interval(75, 81), Interval(22, 28), Interval(48, 54), Interval(7, 7), Interval(1, 1),
         Interval(52, 70), Interval(92, 92), Interval(12, 14), Interval(68, 78), Interval(35, 35),
         Interval(43, 49), Interval(61, 61), Interval(4, 4), Interval(63, 73), Interval(3, 3)],
        # Job 82
        [Interval(70, 84), Interval(75, 83), Interval(55, 67), Interval(47, 57), Interval(69, 79),
         Interval(29, 33), Interval(69, 73), Interval(86, 110), Interval(4, 4), Interval(59, 65),
         Interval(42, 46), Interval(34, 42), Interval(22, 28), Interval(27, 31), Interval(39, 41),
         Interval(26, 34), Interval(56, 74), Interval(69, 89), Interval(50, 64), Interval(10, 10)],
        # Job 83
        [Interval(45, 55), Interval(87, 103), Interval(29, 37), Interval(30, 38), Interval(46, 52),
         Interval(22, 28), Interval(22, 22), Interval(85, 89), Interval(42, 50), Interval(12, 14),
         Interval(93, 99), Interval(87, 109), Interval(41, 45), Interval(72, 88), Interval(69, 71),
         Interval(6, 8), Interval(84, 110), Interval(18, 20), Interval(68, 80), Interval(42, 52)],
        # Job 84
        [Interval(72, 94), Interval(85, 101), Interval(77, 103), Interval(87, 105), Interval(70, 80),
         Interval(38, 44), Interval(61, 75), Interval(40, 46), Interval(74, 80), Interval(29, 35),
         Interval(73, 77), Interval(1, 1), Interval(24, 32), Interval(10, 12), Interval(84, 96),
         Interval(5, 5), Interval(4, 4), Interval(60, 66), Interval(69, 89), Interval(91, 93)],
        # Job 85
        [Interval(61, 61), Interval(61, 69), Interval(44, 52), Interval(2, 2), Interval(90, 106),
         Interval(39, 49), Interval(4, 4), Interval(48, 52), Interval(60, 72), Interval(90, 104),
         Interval(26, 26), Interval(85, 85), Interval(62, 80), Interval(47, 57), Interval(30, 34),
         Interval(94, 102), Interval(57, 63), Interval(81, 95), Interval(71, 79), Interval(40, 46)],
        # Job 86
        [Interval(87, 107), Interval(42, 42), Interval(75, 79), Interval(4, 4), Interval(79, 81),
         Interval(82, 108), Interval(15, 19), Interval(45, 55), Interval(32, 32), Interval(44, 44),
         Interval(87, 99), Interval(2, 2), Interval(5, 5), Interval(63, 73), Interval(71, 85),
         Interval(21, 21), Interval(70, 70), Interval(16, 20), Interval(49, 49), Interval(5, 5)],
        # Job 87
        [Interval(77, 95), Interval(18, 18), Interval(67, 75), Interval(18, 20), Interval(13, 13),
         Interval(66, 78), Interval(12, 12), Interval(57, 71), Interval(73, 83), Interval(35, 39),
         Interval(65, 73), Interval(13, 13), Interval(70, 86), Interval(60, 60), Interval(69, 73),
         Interval(56, 70), Interval(73, 81), Interval(36, 46), Interval(80, 88), Interval(67, 75)],
        # Job 88
        [Interval(15, 19), Interval(75, 85), Interval(86, 106), Interval(41, 47), Interval(2, 2),
         Interval(92, 92), Interval(31, 33), Interval(55, 59), Interval(74, 74), Interval(32, 32),
         Interval(45, 51), Interval(54, 68), Interval(40, 54), Interval(78, 78), Interval(70, 92),
         Interval(74, 98), Interval(29, 29), Interval(58, 70), Interval(45, 51), Interval(32, 36)],
        # Job 89
        [Interval(8, 8), Interval(69, 89), Interval(68, 74), Interval(80, 94), Interval(1, 1),
         Interval(56, 66), Interval(79, 85), Interval(7, 7), Interval(49, 57), Interval(65, 75),
         Interval(53, 55), Interval(59, 65), Interval(74, 76), Interval(13, 13), Interval(51, 55),
         Interval(52, 54), Interval(69, 87), Interval(97, 97), Interval(17, 19), Interval(36, 42)],
        # Job 90
        [Interval(61, 79), Interval(47, 63), Interval(83, 101), Interval(57, 61), Interval(61, 63),
         Interval(15, 17), Interval(4, 4), Interval(29, 29), Interval(16, 20), Interval(20, 20),
         Interval(49, 63), Interval(71, 93), Interval(31, 35), Interval(67, 87), Interval(61, 67),
         Interval(25, 25), Interval(75, 75), Interval(41, 51), Interval(51, 57), Interval(52, 58)],
        # Job 91
        [Interval(68, 74), Interval(67, 71), Interval(9, 9), Interval(82, 102), Interval(65, 73),
         Interval(88, 94), Interval(58, 68), Interval(3, 3), Interval(95, 97), Interval(8, 10),
         Interval(42, 54), Interval(28, 30), Interval(12, 16), Interval(14, 16), Interval(11, 11),
         Interval(2, 2), Interval(39, 47), Interval(48, 56), Interval(47, 61), Interval(82, 110)],
        # Job 92
        [Interval(62, 82), Interval(62, 68), Interval(17, 19), Interval(69, 91), Interval(47, 63),
         Interval(44, 46), Interval(33, 35), Interval(57, 77), Interval(54, 64), Interval(5, 5),
         Interval(35, 41), Interval(88, 110), Interval(80, 102), Interval(15, 15), Interval(42, 42),
         Interval(72, 76), Interval(23, 25), Interval(21, 25), Interval(10, 10), Interval(50, 56)],
        # Job 93
        [Interval(3, 3), Interval(15, 19), Interval(70, 86), Interval(69, 75), Interval(57, 69),
         Interval(90, 94), Interval(33, 37), Interval(56, 68), Interval(79, 93), Interval(5, 5),
         Interval(55, 55), Interval(72, 82), Interval(86, 104), Interval(49, 49), Interval(6, 6),
         Interval(57, 59), Interval(15, 17), Interval(76, 80), Interval(56, 68), Interval(67, 79)],
        # Job 94
        [Interval(38, 38), Interval(51, 51), Interval(28, 28), Interval(71, 81), Interval(34, 42),
         Interval(85, 107), Interval(90, 92), Interval(32, 32), Interval(77, 103), Interval(68, 78),
         Interval(51, 61), Interval(60, 74), Interval(4, 4), Interval(47, 63), Interval(68, 86),
         Interval(20, 20), Interval(40, 46), Interval(59, 65), Interval(76, 82), Interval(43, 55)],
        # Job 95
        [Interval(36, 38), Interval(71, 71), Interval(77, 83), Interval(31, 35), Interval(95, 95),
         Interval(40, 42), Interval(13, 17), Interval(66, 68), Interval(9, 11), Interval(94, 94),
         Interval(57, 69), Interval(97, 97), Interval(55, 57), Interval(38, 46), Interval(32, 38),
         Interval(63, 63), Interval(15, 17), Interval(83, 101), Interval(12, 14), Interval(86, 90)],
        # Job 96
        [Interval(14, 14), Interval(39, 43), Interval(79, 85), Interval(46, 48), Interval(45, 53),
         Interval(50, 54), Interval(56, 72), Interval(25, 25), Interval(11, 13), Interval(48, 64),
         Interval(45, 49), Interval(41, 43), Interval(74, 80), Interval(81, 97), Interval(80, 104),
         Interval(40, 42), Interval(64, 86), Interval(22, 24), Interval(35, 45), Interval(82, 100)],
        # Job 97
        [Interval(97, 101), Interval(49, 55), Interval(29, 31), Interval(24, 30), Interval(80, 92),
         Interval(28, 30), Interval(76, 84), Interval(70, 86), Interval(74, 78), Interval(12, 14),
         Interval(11, 13), Interval(22, 24), Interval(60, 72), Interval(26, 34), Interval(57, 75),
         Interval(46, 58), Interval(60, 74), Interval(39, 45), Interval(79, 103), Interval(82, 86)],
        # Job 98
        [Interval(87, 101), Interval(7, 7), Interval(39, 41), Interval(25, 33), Interval(85, 89),
         Interval(16, 20), Interval(78, 86), Interval(74, 76), Interval(30, 34), Interval(41, 49),
         Interval(17, 21), Interval(22, 24), Interval(68, 70), Interval(1, 1), Interval(86, 98),
         Interval(8, 10), Interval(26, 32), Interval(35, 39), Interval(8, 8), Interval(69, 87)],
        # Job 99
        [Interval(78, 80), Interval(39, 39), Interval(43, 49), Interval(85, 105), Interval(4, 4),
         Interval(49, 61), Interval(71, 89), Interval(68, 90), Interval(35, 35), Interval(10, 12),
         Interval(4, 4), Interval(22, 26), Interval(60, 66), Interval(13, 15), Interval(33, 35),
         Interval(13, 15), Interval(57, 57), Interval(56, 60), Interval(14, 14), Interval(60, 60)],
    ],
    'name': 'INT__TAI100_20_06.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai100_20_06_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI100_20_06.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI100_20_06.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI100_20_06_F_15_01_INTERVAL_DATA
