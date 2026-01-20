"""
Problema INT__TAI100_20_08.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI100_20_08_F_15_01_INTERVAL_DATA = {
    'num_jobs': 100,
    'num_machines': 20,
    'problem_id': 'int__tai100_20_08.F.15_01_interval',
    'sequences': [
        [10, 17, 18, 2, 0, 19, 15, 5, 4, 9, 14, 1, 13, 3, 7, 16, 8, 11, 12, 6],
        [6, 10, 0, 3, 17, 9, 19, 5, 4, 12, 14, 18, 7, 8, 15, 11, 13, 2, 16, 1],
        [5, 1, 15, 4, 13, 11, 9, 6, 19, 8, 0, 12, 10, 17, 16, 2, 18, 3, 14, 7],
        [10, 19, 14, 0, 2, 12, 13, 4, 11, 5, 8, 15, 7, 16, 1, 6, 9, 3, 18, 17],
        [12, 14, 16, 1, 11, 4, 7, 13, 15, 8, 18, 17, 9, 10, 2, 6, 19, 5, 0, 3],
        [13, 14, 10, 11, 1, 2, 15, 4, 3, 6, 17, 19, 18, 12, 16, 0, 8, 5, 9, 7],
        [1, 10, 16, 7, 3, 2, 12, 17, 5, 6, 18, 9, 15, 0, 11, 13, 8, 4, 14, 19],
        [9, 13, 10, 14, 4, 12, 2, 18, 0, 11, 7, 3, 19, 1, 17, 8, 16, 5, 6, 15],
        [2, 3, 6, 15, 13, 5, 11, 18, 4, 7, 0, 10, 9, 17, 12, 1, 14, 19, 8, 16],
        [0, 5, 15, 3, 18, 7, 14, 9, 16, 19, 2, 6, 11, 12, 13, 4, 1, 8, 10, 17],
        [14, 18, 13, 2, 8, 10, 19, 15, 9, 3, 1, 17, 5, 4, 16, 12, 6, 11, 7, 0],
        [11, 16, 15, 4, 9, 10, 7, 5, 2, 8, 13, 14, 12, 6, 19, 1, 0, 18, 3, 17],
        [8, 19, 5, 12, 10, 15, 3, 4, 13, 9, 17, 1, 16, 2, 14, 0, 6, 11, 18, 7],
        [5, 10, 14, 7, 3, 13, 16, 11, 15, 6, 17, 12, 4, 8, 1, 0, 9, 18, 19, 2],
        [2, 3, 15, 14, 19, 7, 11, 4, 16, 10, 17, 9, 12, 1, 5, 8, 0, 6, 18, 13],
        [18, 12, 9, 17, 14, 2, 3, 16, 15, 7, 13, 4, 0, 8, 11, 19, 1, 6, 5, 10],
        [16, 12, 4, 18, 3, 17, 7, 2, 13, 5, 9, 19, 14, 10, 0, 8, 11, 1, 6, 15],
        [6, 7, 8, 15, 2, 3, 11, 18, 0, 4, 9, 17, 19, 13, 12, 10, 16, 1, 14, 5],
        [8, 6, 17, 12, 15, 5, 0, 3, 16, 7, 9, 13, 10, 4, 14, 11, 1, 18, 19, 2],
        [9, 5, 0, 6, 3, 11, 13, 15, 1, 7, 14, 2, 17, 8, 16, 18, 12, 19, 4, 10],
        [15, 7, 6, 9, 18, 3, 0, 19, 16, 10, 12, 11, 4, 2, 8, 14, 17, 1, 13, 5],
        [9, 11, 10, 3, 13, 17, 2, 0, 12, 8, 1, 6, 4, 7, 19, 15, 16, 14, 18, 5],
        [9, 18, 14, 19, 0, 8, 11, 10, 12, 3, 7, 16, 17, 5, 15, 1, 6, 4, 2, 13],
        [0, 11, 2, 1, 12, 5, 14, 4, 16, 10, 17, 9, 3, 8, 13, 7, 15, 6, 19, 18],
        [9, 7, 0, 2, 1, 11, 3, 14, 19, 12, 13, 4, 17, 18, 10, 6, 5, 15, 8, 16],
        [16, 15, 18, 9, 8, 4, 13, 6, 12, 10, 11, 3, 5, 0, 1, 17, 19, 2, 14, 7],
        [19, 10, 5, 3, 2, 0, 13, 18, 8, 4, 6, 7, 15, 9, 17, 14, 16, 1, 11, 12],
        [3, 19, 16, 8, 4, 17, 11, 2, 10, 13, 7, 15, 1, 6, 0, 18, 5, 14, 9, 12],
        [4, 7, 16, 11, 9, 6, 14, 3, 18, 10, 19, 0, 13, 1, 2, 8, 15, 12, 5, 17],
        [10, 15, 14, 4, 8, 18, 3, 13, 17, 5, 12, 7, 6, 2, 9, 11, 19, 16, 1, 0],
        [15, 7, 4, 14, 1, 17, 0, 9, 18, 2, 10, 16, 8, 19, 11, 5, 12, 6, 13, 3],
        [17, 13, 8, 9, 10, 5, 19, 0, 14, 6, 2, 12, 11, 18, 16, 3, 15, 7, 1, 4],
        [9, 8, 7, 15, 1, 2, 18, 5, 4, 3, 19, 0, 6, 17, 14, 13, 11, 10, 12, 16],
        [10, 19, 1, 6, 4, 13, 12, 0, 11, 14, 5, 9, 2, 7, 3, 8, 18, 15, 17, 16],
        [8, 19, 4, 18, 12, 11, 14, 2, 10, 0, 16, 9, 1, 6, 5, 17, 7, 13, 15, 3],
        [19, 4, 11, 0, 16, 12, 18, 3, 15, 1, 14, 2, 6, 9, 10, 5, 7, 17, 13, 8],
        [19, 13, 4, 0, 9, 10, 3, 8, 14, 18, 1, 2, 15, 17, 12, 6, 5, 16, 7, 11],
        [5, 1, 12, 3, 0, 14, 7, 9, 18, 2, 19, 4, 6, 13, 17, 15, 8, 16, 11, 10],
        [10, 12, 0, 17, 16, 5, 9, 14, 19, 8, 6, 13, 4, 1, 15, 2, 7, 3, 11, 18],
        [8, 2, 18, 9, 6, 4, 11, 0, 5, 10, 17, 16, 3, 19, 7, 14, 13, 12, 1, 15],
        [5, 12, 19, 7, 9, 14, 15, 10, 0, 16, 13, 18, 3, 8, 17, 4, 6, 1, 11, 2],
        [4, 18, 7, 12, 17, 13, 19, 0, 9, 8, 3, 5, 2, 10, 6, 14, 15, 11, 1, 16],
        [19, 13, 6, 7, 9, 18, 15, 5, 16, 11, 0, 17, 1, 12, 3, 8, 2, 4, 10, 14],
        [0, 19, 14, 2, 13, 12, 3, 15, 17, 7, 4, 11, 9, 10, 1, 8, 6, 18, 16, 5],
        [2, 7, 10, 0, 12, 16, 1, 13, 9, 8, 19, 15, 14, 17, 4, 3, 6, 18, 11, 5],
        [7, 15, 11, 6, 18, 13, 2, 12, 10, 19, 17, 5, 16, 14, 4, 3, 9, 1, 8, 0],
        [11, 7, 19, 5, 1, 15, 13, 17, 2, 0, 9, 8, 6, 12, 3, 10, 16, 4, 18, 14],
        [12, 13, 2, 3, 15, 7, 11, 8, 0, 19, 5, 18, 1, 6, 16, 17, 4, 14, 9, 10],
        [15, 0, 2, 19, 13, 9, 14, 11, 4, 10, 7, 16, 8, 17, 5, 3, 18, 12, 1, 6],
        [4, 10, 9, 0, 5, 11, 14, 3, 13, 8, 17, 1, 18, 15, 12, 7, 6, 2, 19, 16],
        [3, 6, 5, 0, 15, 2, 13, 1, 11, 4, 19, 9, 18, 17, 16, 8, 10, 7, 12, 14],
        [7, 14, 16, 19, 11, 12, 15, 6, 8, 18, 5, 0, 4, 13, 17, 9, 10, 2, 1, 3],
        [7, 15, 8, 18, 13, 17, 14, 10, 19, 9, 1, 5, 2, 0, 4, 12, 6, 11, 16, 3],
        [7, 13, 4, 3, 0, 10, 12, 1, 16, 19, 6, 14, 2, 15, 8, 17, 5, 18, 11, 9],
        [18, 2, 14, 11, 6, 9, 5, 12, 1, 10, 13, 0, 4, 17, 3, 8, 7, 16, 19, 15],
        [10, 4, 9, 1, 19, 17, 18, 7, 12, 6, 15, 3, 2, 13, 16, 5, 0, 11, 14, 8],
        [9, 2, 5, 15, 12, 17, 18, 1, 8, 10, 11, 0, 4, 14, 19, 3, 6, 13, 16, 7],
        [3, 15, 9, 19, 11, 17, 10, 6, 8, 16, 4, 13, 2, 12, 14, 1, 5, 0, 7, 18],
        [19, 15, 18, 5, 17, 14, 16, 1, 9, 0, 6, 12, 3, 10, 13, 11, 7, 4, 8, 2],
        [11, 5, 12, 7, 4, 1, 17, 18, 8, 15, 10, 2, 9, 3, 14, 6, 0, 19, 16, 13],
        [15, 17, 18, 1, 3, 6, 19, 14, 16, 13, 9, 11, 0, 5, 4, 2, 12, 10, 7, 8],
        [5, 17, 2, 13, 4, 19, 18, 1, 12, 16, 10, 11, 8, 6, 7, 3, 0, 14, 9, 15],
        [12, 7, 16, 9, 6, 8, 18, 14, 5, 17, 4, 13, 19, 11, 10, 0, 2, 1, 15, 3],
        [19, 2, 7, 3, 8, 16, 9, 18, 1, 10, 11, 5, 12, 0, 6, 14, 13, 17, 4, 15],
        [5, 7, 3, 12, 14, 8, 1, 19, 17, 11, 9, 18, 2, 0, 10, 16, 4, 6, 13, 15],
        [12, 3, 0, 9, 15, 6, 8, 16, 17, 19, 7, 14, 10, 18, 11, 13, 5, 2, 1, 4],
        [16, 8, 18, 3, 13, 9, 10, 6, 4, 11, 5, 12, 17, 14, 7, 19, 0, 2, 15, 1],
        [13, 0, 3, 14, 6, 5, 8, 11, 4, 9, 12, 7, 18, 16, 17, 1, 10, 19, 2, 15],
        [14, 13, 18, 1, 11, 8, 2, 6, 15, 12, 5, 19, 17, 3, 16, 4, 9, 10, 7, 0],
        [19, 15, 5, 10, 12, 13, 0, 3, 6, 11, 16, 9, 17, 8, 1, 14, 2, 7, 4, 18],
        [15, 11, 12, 19, 1, 7, 13, 6, 17, 18, 10, 14, 0, 9, 16, 5, 8, 2, 3, 4],
        [4, 16, 9, 6, 13, 0, 7, 18, 10, 17, 8, 15, 19, 3, 2, 14, 5, 12, 11, 1],
        [3, 12, 4, 0, 10, 2, 7, 1, 17, 15, 6, 11, 19, 8, 5, 9, 13, 16, 14, 18],
        [8, 0, 16, 2, 19, 4, 5, 6, 15, 9, 7, 1, 12, 13, 17, 11, 3, 14, 10, 18],
        [10, 17, 18, 7, 3, 14, 5, 2, 0, 1, 6, 4, 19, 9, 8, 16, 15, 12, 11, 13],
        [5, 3, 2, 9, 1, 8, 11, 13, 0, 14, 10, 12, 16, 7, 4, 6, 18, 17, 15, 19],
        [13, 0, 14, 6, 11, 12, 5, 7, 18, 10, 9, 19, 17, 4, 16, 3, 1, 2, 15, 8],
        [8, 2, 6, 7, 19, 11, 9, 13, 10, 4, 14, 18, 3, 5, 15, 12, 1, 0, 17, 16],
        [5, 18, 14, 3, 0, 15, 11, 9, 6, 2, 1, 4, 8, 12, 17, 13, 10, 19, 7, 16],
        [6, 18, 15, 16, 9, 13, 1, 14, 3, 17, 19, 0, 12, 5, 8, 2, 4, 11, 10, 7],
        [0, 17, 6, 12, 11, 16, 18, 5, 9, 8, 13, 2, 3, 7, 15, 4, 14, 10, 1, 19],
        [16, 9, 2, 14, 1, 15, 17, 7, 3, 5, 4, 11, 6, 18, 8, 19, 10, 13, 12, 0],
        [4, 10, 0, 14, 2, 11, 1, 3, 12, 9, 18, 6, 15, 13, 7, 8, 19, 5, 17, 16],
        [17, 14, 10, 4, 9, 2, 3, 15, 11, 0, 16, 1, 5, 7, 13, 8, 6, 18, 19, 12],
        [17, 11, 0, 7, 13, 10, 4, 16, 15, 9, 1, 3, 5, 6, 12, 19, 18, 2, 8, 14],
        [3, 11, 10, 19, 7, 15, 6, 9, 17, 13, 16, 8, 2, 14, 4, 18, 1, 12, 5, 0],
        [15, 12, 18, 7, 13, 11, 2, 14, 5, 16, 3, 17, 9, 1, 6, 4, 0, 19, 10, 8],
        [13, 17, 14, 18, 5, 8, 16, 11, 3, 7, 15, 2, 9, 1, 12, 4, 0, 10, 19, 6],
        [7, 4, 3, 1, 18, 12, 2, 13, 9, 14, 8, 5, 6, 16, 11, 19, 0, 15, 17, 10],
        [2, 19, 11, 6, 17, 15, 0, 13, 7, 8, 10, 3, 12, 16, 4, 9, 5, 14, 1, 18],
        [8, 3, 17, 16, 1, 14, 2, 0, 4, 9, 7, 18, 13, 12, 10, 5, 6, 15, 19, 11],
        [17, 13, 7, 12, 18, 8, 14, 6, 3, 2, 16, 9, 11, 5, 10, 0, 19, 15, 1, 4],
        [15, 12, 5, 19, 11, 8, 6, 0, 16, 9, 14, 2, 10, 1, 3, 4, 17, 18, 7, 13],
        [11, 2, 6, 5, 19, 3, 18, 8, 0, 7, 10, 12, 15, 14, 1, 16, 4, 17, 13, 9],
        [1, 4, 16, 14, 13, 7, 9, 2, 8, 5, 3, 6, 15, 10, 11, 0, 12, 17, 18, 19],
        [5, 0, 3, 9, 2, 17, 19, 6, 14, 18, 10, 15, 4, 13, 8, 1, 7, 11, 12, 16],
        [12, 6, 3, 8, 16, 13, 0, 1, 18, 9, 11, 15, 5, 2, 4, 17, 10, 19, 14, 7],
        [9, 4, 10, 8, 14, 0, 12, 17, 18, 19, 11, 7, 13, 1, 16, 2, 5, 6, 15, 3],
        [2, 7, 15, 5, 9, 6, 8, 4, 12, 0, 3, 16, 11, 14, 19, 13, 18, 1, 10, 17],
        [1, 3, 12, 15, 8, 6, 13, 7, 5, 14, 18, 4, 9, 19, 11, 10, 2, 17, 16, 0],
    ],
    'durations': [
        # Job 0
        [Interval(56, 70), Interval(78, 90), Interval(3, 3), Interval(51, 55), Interval(1, 1),
         Interval(33, 37), Interval(18, 22), Interval(37, 49), Interval(42, 44), Interval(73, 97),
         Interval(20, 26), Interval(19, 23), Interval(9, 11), Interval(74, 80), Interval(71, 95),
         Interval(26, 28), Interval(32, 38), Interval(17, 19), Interval(41, 47), Interval(34, 44)],
        # Job 1
        [Interval(83, 111), Interval(42, 54), Interval(61, 65), Interval(73, 79), Interval(18, 18),
         Interval(8, 10), Interval(74, 76), Interval(35, 37), Interval(70, 74), Interval(72, 86),
         Interval(97, 101), Interval(80, 108), Interval(42, 50), Interval(14, 18), Interval(30, 36),
         Interval(42, 42), Interval(63, 67), Interval(92, 104), Interval(27, 33), Interval(44, 56)],
        # Job 2
        [Interval(64, 64), Interval(44, 52), Interval(83, 103), Interval(44, 50), Interval(74, 88),
         Interval(31, 31), Interval(48, 60), Interval(87, 91), Interval(19, 25), Interval(58, 68),
         Interval(56, 60), Interval(23, 27), Interval(62, 66), Interval(78, 86), Interval(55, 67),
         Interval(63, 65), Interval(38, 38), Interval(15, 19), Interval(26, 28), Interval(68, 72)],
        # Job 3
        [Interval(31, 33), Interval(71, 73), Interval(39, 45), Interval(71, 95), Interval(2, 2),
         Interval(32, 34), Interval(25, 33), Interval(87, 93), Interval(31, 39), Interval(78, 104),
         Interval(24, 28), Interval(79, 91), Interval(66, 78), Interval(17, 21), Interval(85, 105),
         Interval(5, 5), Interval(37, 41), Interval(69, 81), Interval(73, 93), Interval(64, 76)],
        # Job 4
        [Interval(79, 101), Interval(71, 81), Interval(27, 27), Interval(84, 92), Interval(51, 67),
         Interval(90, 100), Interval(44, 58), Interval(19, 25), Interval(78, 80), Interval(27, 33),
         Interval(10, 10), Interval(90, 92), Interval(63, 85), Interval(4, 4), Interval(32, 40),
         Interval(87, 109), Interval(52, 56), Interval(31, 35), Interval(2, 2), Interval(22, 22)],
        # Job 5
        [Interval(63, 79), Interval(89, 109), Interval(22, 22), Interval(60, 68), Interval(26, 34),
         Interval(10, 12), Interval(93, 95), Interval(14, 14), Interval(81, 85), Interval(45, 49),
         Interval(47, 49), Interval(39, 51), Interval(35, 43), Interval(7, 7), Interval(31, 33),
         Interval(2, 2), Interval(86, 100), Interval(39, 41), Interval(14, 14), Interval(44, 52)],
        # Job 6
        [Interval(76, 84), Interval(45, 47), Interval(4, 4), Interval(42, 48), Interval(62, 66),
         Interval(19, 19), Interval(78, 92), Interval(36, 42), Interval(73, 83), Interval(56, 68),
         Interval(59, 79), Interval(61, 69), Interval(71, 93), Interval(69, 81), Interval(39, 41),
         Interval(15, 15), Interval(59, 77), Interval(10, 12), Interval(42, 46), Interval(3, 3)],
        # Job 7
        [Interval(92, 98), Interval(80, 98), Interval(87, 109), Interval(66, 84), Interval(27, 27),
         Interval(71, 77), Interval(19, 21), Interval(49, 65), Interval(51, 55), Interval(94, 94),
         Interval(15, 19), Interval(73, 83), Interval(21, 21), Interval(95, 103), Interval(29, 33),
         Interval(91, 107), Interval(79, 93), Interval(17, 23), Interval(79, 81), Interval(74, 98)],
        # Job 8
        [Interval(21, 21), Interval(52, 52), Interval(50, 62), Interval(20, 24), Interval(17, 21),
         Interval(78, 90), Interval(89, 103), Interval(54, 60), Interval(27, 35), Interval(37, 41),
         Interval(13, 13), Interval(6, 6), Interval(58, 58), Interval(30, 34), Interval(40, 42),
         Interval(41, 53), Interval(12, 14), Interval(30, 30), Interval(40, 48), Interval(69, 91)],
        # Job 9
        [Interval(64, 78), Interval(30, 32), Interval(16, 18), Interval(48, 58), Interval(82, 88),
         Interval(44, 52), Interval(51, 53), Interval(30, 38), Interval(39, 39), Interval(84, 84),
         Interval(2, 2), Interval(28, 34), Interval(50, 64), Interval(54, 72), Interval(1, 1),
         Interval(54, 60), Interval(28, 32), Interval(61, 61), Interval(65, 79), Interval(17, 17)],
        # Job 10
        [Interval(13, 15), Interval(95, 101), Interval(39, 49), Interval(10, 10), Interval(51, 55),
         Interval(68, 76), Interval(62, 68), Interval(45, 53), Interval(21, 21), Interval(79, 89),
         Interval(94, 94), Interval(85, 113), Interval(58, 64), Interval(57, 71), Interval(26, 32),
         Interval(97, 99), Interval(53, 57), Interval(68, 74), Interval(43, 43), Interval(62, 66)],
        # Job 11
        [Interval(14, 14), Interval(65, 83), Interval(50, 64), Interval(79, 83), Interval(35, 45),
         Interval(6, 8), Interval(77, 93), Interval(29, 35), Interval(32, 38), Interval(34, 34),
         Interval(37, 45), Interval(70, 88), Interval(80, 80), Interval(1, 1), Interval(95, 95),
         Interval(23, 27), Interval(40, 46), Interval(17, 21), Interval(91, 105), Interval(46, 50)],
        # Job 12
        [Interval(40, 44), Interval(61, 81), Interval(8, 10), Interval(23, 29), Interval(3, 3),
         Interval(3, 3), Interval(29, 33), Interval(3, 3), Interval(39, 41), Interval(21, 21),
         Interval(64, 74), Interval(89, 89), Interval(90, 98), Interval(83, 105), Interval(53, 65),
         Interval(8, 10), Interval(71, 71), Interval(52, 54), Interval(39, 51), Interval(71, 79)],
        # Job 13
        [Interval(64, 80), Interval(83, 89), Interval(20, 24), Interval(61, 81), Interval(21, 23),
         Interval(8, 8), Interval(65, 81), Interval(15, 15), Interval(90, 90), Interval(37, 43),
         Interval(1, 1), Interval(4, 4), Interval(76, 86), Interval(10, 10), Interval(76, 90),
         Interval(28, 36), Interval(78, 100), Interval(4, 4), Interval(51, 55), Interval(33, 43)],
        # Job 14
        [Interval(48, 56), Interval(42, 48), Interval(43, 43), Interval(8, 10), Interval(90, 90),
         Interval(34, 46), Interval(25, 27), Interval(45, 59), Interval(21, 23), Interval(8, 10),
         Interval(30, 38), Interval(87, 101), Interval(69, 69), Interval(24, 32), Interval(29, 29),
         Interval(60, 64), Interval(63, 63), Interval(89, 109), Interval(83, 111), Interval(13, 15)],
        # Job 15
        [Interval(75, 87), Interval(45, 55), Interval(8, 10), Interval(25, 29), Interval(91, 91),
         Interval(52, 54), Interval(88, 98), Interval(60, 68), Interval(23, 23), Interval(42, 42),
         Interval(67, 87), Interval(47, 53), Interval(77, 91), Interval(13, 13), Interval(85, 95),
         Interval(78, 90), Interval(77, 85), Interval(53, 67), Interval(88, 96), Interval(69, 75)],
        # Job 16
        [Interval(74, 100), Interval(4, 4), Interval(50, 62), Interval(39, 41), Interval(52, 58),
         Interval(26, 32), Interval(30, 32), Interval(26, 32), Interval(39, 39), Interval(37, 39),
         Interval(89, 99), Interval(37, 43), Interval(83, 93), Interval(1, 1), Interval(3, 3),
         Interval(46, 46), Interval(32, 40), Interval(40, 48), Interval(91, 93), Interval(32, 36)],
        # Job 17
        [Interval(58, 66), Interval(86, 104), Interval(65, 73), Interval(25, 33), Interval(45, 45),
         Interval(77, 77), Interval(30, 38), Interval(51, 67), Interval(86, 94), Interval(74, 92),
         Interval(79, 87), Interval(65, 79), Interval(92, 104), Interval(46, 60), Interval(79, 89),
         Interval(85, 103), Interval(62, 80), Interval(49, 49), Interval(15, 19), Interval(24, 32)],
        # Job 18
        [Interval(59, 73), Interval(21, 27), Interval(66, 82), Interval(63, 83), Interval(68, 86),
         Interval(66, 84), Interval(66, 66), Interval(12, 16), Interval(20, 22), Interval(8, 8),
         Interval(1, 1), Interval(35, 43), Interval(71, 81), Interval(14, 14), Interval(64, 76),
         Interval(19, 21), Interval(18, 22), Interval(58, 74), Interval(20, 26), Interval(71, 77)],
        # Job 19
        [Interval(50, 58), Interval(32, 38), Interval(54, 62), Interval(66, 78), Interval(84, 112),
         Interval(60, 64), Interval(65, 71), Interval(79, 95), Interval(19, 23), Interval(61, 73),
         Interval(9, 9), Interval(11, 13), Interval(39, 51), Interval(32, 40), Interval(43, 43),
         Interval(3, 3), Interval(25, 31), Interval(24, 24), Interval(67, 73), Interval(43, 47)],
        # Job 20
        [Interval(70, 86), Interval(26, 30), Interval(53, 67), Interval(62, 76), Interval(76, 98),
         Interval(33, 35), Interval(61, 79), Interval(2, 2), Interval(83, 83), Interval(87, 101),
         Interval(20, 24), Interval(62, 62), Interval(37, 37), Interval(46, 50), Interval(18, 22),
         Interval(5, 5), Interval(13, 13), Interval(74, 76), Interval(35, 45), Interval(27, 27)],
        # Job 21
        [Interval(84, 100), Interval(75, 81), Interval(76, 92), Interval(90, 104), Interval(68, 86),
         Interval(84, 84), Interval(51, 65), Interval(84, 86), Interval(34, 46), Interval(49, 63),
         Interval(53, 57), Interval(59, 67), Interval(39, 47), Interval(33, 39), Interval(50, 54),
         Interval(42, 44), Interval(2, 2), Interval(9, 9), Interval(68, 80), Interval(78, 82)],
        # Job 22
        [Interval(46, 60), Interval(82, 88), Interval(70, 88), Interval(74, 84), Interval(26, 26),
         Interval(4, 4), Interval(17, 21), Interval(11, 11), Interval(10, 12), Interval(63, 79),
         Interval(6, 6), Interval(57, 77), Interval(23, 29), Interval(3, 3), Interval(9, 11),
         Interval(74, 74), Interval(53, 67), Interval(73, 81), Interval(29, 39), Interval(34, 46)],
        # Job 23
        [Interval(23, 23), Interval(29, 39), Interval(1, 1), Interval(78, 88), Interval(90, 100),
         Interval(19, 19), Interval(44, 44), Interval(35, 45), Interval(19, 25), Interval(52, 64),
         Interval(70, 74), Interval(16, 20), Interval(23, 23), Interval(16, 16), Interval(83, 99),
         Interval(34, 40), Interval(25, 25), Interval(4, 4), Interval(79, 105), Interval(87, 93)],
        # Job 24
        [Interval(85, 101), Interval(26, 30), Interval(47, 49), Interval(28, 32), Interval(78, 102),
         Interval(20, 26), Interval(63, 83), Interval(18, 24), Interval(27, 31), Interval(22, 24),
         Interval(44, 44), Interval(88, 100), Interval(25, 31), Interval(72, 90), Interval(48, 58),
         Interval(87, 87), Interval(64, 72), Interval(1, 1), Interval(36, 42), Interval(46, 46)],
        # Job 25
        [Interval(85, 95), Interval(53, 63), Interval(6, 8), Interval(80, 92), Interval(75, 101),
         Interval(61, 67), Interval(8, 10), Interval(70, 86), Interval(71, 77), Interval(42, 42),
         Interval(80, 106), Interval(13, 17), Interval(32, 32), Interval(75, 79), Interval(36, 48),
         Interval(23, 31), Interval(9, 9), Interval(3, 3), Interval(66, 72), Interval(16, 16)],
        # Job 26
        [Interval(42, 46), Interval(60, 60), Interval(19, 23), Interval(75, 99), Interval(61, 69),
         Interval(8, 8), Interval(65, 65), Interval(37, 47), Interval(27, 35), Interval(39, 47),
         Interval(48, 52), Interval(47, 61), Interval(39, 43), Interval(78, 80), Interval(68, 92),
         Interval(86, 92), Interval(17, 19), Interval(44, 46), Interval(55, 59), Interval(16, 18)],
        # Job 27
        [Interval(50, 56), Interval(82, 96), Interval(53, 65), Interval(61, 75), Interval(58, 58),
         Interval(55, 61), Interval(71, 77), Interval(43, 49), Interval(52, 56), Interval(70, 82),
         Interval(61, 71), Interval(3, 3), Interval(76, 82), Interval(70, 80), Interval(12, 14),
         Interval(75, 95), Interval(48, 56), Interval(26, 28), Interval(56, 66), Interval(2, 2)],
        # Job 28
        [Interval(68, 80), Interval(25, 31), Interval(25, 33), Interval(76, 88), Interval(3, 3),
         Interval(29, 33), Interval(66, 80), Interval(42, 52), Interval(15, 17), Interval(53, 55),
         Interval(59, 67), Interval(27, 27), Interval(10, 12), Interval(71, 87), Interval(35, 47),
         Interval(65, 65), Interval(69, 83), Interval(61, 61), Interval(40, 46), Interval(24, 32)],
        # Job 29
        [Interval(3, 3), Interval(18, 18), Interval(41, 55), Interval(17, 23), Interval(60, 70),
         Interval(41, 43), Interval(53, 57), Interval(35, 45), Interval(15, 19), Interval(12, 12),
         Interval(8, 10), Interval(30, 34), Interval(64, 76), Interval(26, 26), Interval(44, 44),
         Interval(33, 33), Interval(74, 90), Interval(6, 6), Interval(32, 42), Interval(3, 3)],
        # Job 30
        [Interval(73, 83), Interval(31, 35), Interval(60, 62), Interval(76, 86), Interval(18, 18),
         Interval(65, 85), Interval(15, 17), Interval(29, 33), Interval(23, 25), Interval(1, 1),
         Interval(32, 40), Interval(88, 88), Interval(56, 58), Interval(36, 38), Interval(7, 7),
         Interval(65, 87), Interval(40, 40), Interval(71, 87), Interval(67, 67), Interval(17, 21)],
        # Job 31
        [Interval(18, 22), Interval(32, 40), Interval(64, 70), Interval(57, 71), Interval(45, 57),
         Interval(55, 57), Interval(25, 33), Interval(15, 15), Interval(42, 56), Interval(71, 73),
         Interval(77, 97), Interval(74, 80), Interval(5, 5), Interval(72, 84), Interval(29, 35),
         Interval(16, 20), Interval(71, 95), Interval(51, 55), Interval(76, 92), Interval(15, 15)],
        # Job 32
        [Interval(48, 62), Interval(91, 97), Interval(73, 83), Interval(83, 87), Interval(19, 23),
         Interval(5, 5), Interval(15, 19), Interval(89, 103), Interval(17, 21), Interval(64, 80),
         Interval(2, 2), Interval(60, 64), Interval(17, 19), Interval(20, 26), Interval(63, 65),
         Interval(63, 63), Interval(77, 103), Interval(48, 56), Interval(8, 10), Interval(14, 18)],
        # Job 33
        [Interval(81, 83), Interval(20, 20), Interval(50, 50), Interval(19, 23), Interval(51, 63),
         Interval(9, 9), Interval(46, 52), Interval(5, 5), Interval(13, 15), Interval(65, 77),
         Interval(40, 54), Interval(32, 38), Interval(8, 8), Interval(86, 98), Interval(69, 77),
         Interval(57, 77), Interval(58, 74), Interval(88, 98), Interval(43, 53), Interval(59, 71)],
        # Job 34
        [Interval(78, 86), Interval(35, 45), Interval(14, 14), Interval(49, 53), Interval(85, 87),
         Interval(7, 9), Interval(23, 27), Interval(75, 77), Interval(40, 42), Interval(10, 10),
         Interval(59, 61), Interval(94, 98), Interval(63, 73), Interval(8, 8), Interval(72, 86),
         Interval(17, 19), Interval(68, 82), Interval(33, 37), Interval(30, 32), Interval(12, 16)],
        # Job 35
        [Interval(40, 50), Interval(2, 2), Interval(81, 107), Interval(4, 4), Interval(26, 28),
         Interval(71, 73), Interval(66, 86), Interval(58, 66), Interval(8, 10), Interval(13, 15),
         Interval(6, 8), Interval(65, 73), Interval(41, 55), Interval(70, 88), Interval(52, 52),
         Interval(4, 4), Interval(48, 62), Interval(68, 82), Interval(56, 68), Interval(93, 93)],
        # Job 36
        [Interval(12, 14), Interval(54, 72), Interval(71, 79), Interval(59, 75), Interval(26, 26),
         Interval(58, 60), Interval(70, 92), Interval(55, 55), Interval(59, 73), Interval(28, 28),
         Interval(47, 51), Interval(15, 17), Interval(65, 73), Interval(3, 3), Interval(12, 14),
         Interval(63, 81), Interval(68, 84), Interval(92, 100), Interval(59, 67), Interval(33, 43)],
        # Job 37
        [Interval(35, 37), Interval(77, 89), Interval(3, 3), Interval(10, 10), Interval(45, 49),
         Interval(58, 72), Interval(26, 26), Interval(60, 64), Interval(45, 45), Interval(52, 58),
         Interval(71, 75), Interval(29, 31), Interval(86, 86), Interval(46, 60), Interval(57, 63),
         Interval(40, 42), Interval(54, 54), Interval(29, 37), Interval(35, 45), Interval(20, 20)],
        # Job 38
        [Interval(59, 63), Interval(24, 32), Interval(48, 58), Interval(68, 90), Interval(59, 65),
         Interval(81, 93), Interval(44, 44), Interval(19, 23), Interval(20, 24), Interval(59, 75),
         Interval(7, 9), Interval(45, 59), Interval(41, 45), Interval(8, 8), Interval(80, 88),
         Interval(23, 29), Interval(75, 97), Interval(53, 71), Interval(10, 12), Interval(68, 80)],
        # Job 39
        [Interval(12, 16), Interval(1, 1), Interval(29, 31), Interval(74, 74), Interval(2, 2),
         Interval(87, 87), Interval(29, 33), Interval(83, 85), Interval(38, 46), Interval(10, 12),
         Interval(89, 91), Interval(39, 45), Interval(30, 38), Interval(14, 14), Interval(12, 14),
         Interval(67, 83), Interval(47, 53), Interval(60, 62), Interval(10, 10), Interval(76, 76)],
        # Job 40
        [Interval(22, 22), Interval(50, 66), Interval(37, 39), Interval(14, 14), Interval(94, 98),
         Interval(67, 85), Interval(26, 28), Interval(14, 18), Interval(59, 79), Interval(46, 52),
         Interval(34, 36), Interval(85, 101), Interval(44, 52), Interval(38, 48), Interval(59, 65),
         Interval(33, 35), Interval(43, 45), Interval(49, 53), Interval(86, 86), Interval(46, 54)],
        # Job 41
        [Interval(37, 37), Interval(46, 50), Interval(74, 100), Interval(71, 85), Interval(6, 6),
         Interval(69, 85), Interval(91, 105), Interval(63, 69), Interval(29, 37), Interval(67, 79),
         Interval(65, 69), Interval(28, 30), Interval(71, 83), Interval(81, 109), Interval(37, 43),
         Interval(21, 25), Interval(60, 78), Interval(1, 1), Interval(25, 29), Interval(7, 9)],
        # Job 42
        [Interval(57, 71), Interval(76, 98), Interval(48, 52), Interval(52, 68), Interval(46, 54),
         Interval(11, 13), Interval(33, 33), Interval(45, 45), Interval(14, 18), Interval(52, 58),
         Interval(75, 101), Interval(86, 90), Interval(25, 25), Interval(32, 34), Interval(14, 16),
         Interval(2, 2), Interval(38, 50), Interval(67, 83), Interval(58, 64), Interval(64, 70)],
        # Job 43
        [Interval(18, 22), Interval(88, 102), Interval(23, 31), Interval(61, 77), Interval(11, 11),
         Interval(23, 23), Interval(34, 34), Interval(8, 8), Interval(64, 64), Interval(58, 68),
         Interval(65, 81), Interval(56, 60), Interval(32, 34), Interval(23, 29), Interval(80, 88),
         Interval(4, 4), Interval(72, 92), Interval(33, 37), Interval(27, 33), Interval(45, 57)],
        # Job 44
        [Interval(42, 42), Interval(54, 72), Interval(65, 71), Interval(91, 95), Interval(42, 50),
         Interval(57, 63), Interval(36, 44), Interval(3, 3), Interval(68, 78), Interval(75, 99),
         Interval(50, 54), Interval(62, 78), Interval(33, 37), Interval(90, 94), Interval(17, 21),
         Interval(34, 46), Interval(42, 54), Interval(38, 44), Interval(65, 75), Interval(12, 14)],
        # Job 45
        [Interval(50, 56), Interval(49, 61), Interval(30, 34), Interval(58, 62), Interval(39, 41),
         Interval(14, 18), Interval(5, 5), Interval(50, 56), Interval(62, 74), Interval(43, 43),
         Interval(62, 72), Interval(51, 69), Interval(34, 42), Interval(22, 24), Interval(2, 2),
         Interval(59, 75), Interval(42, 42), Interval(23, 27), Interval(78, 82), Interval(1, 1)],
        # Job 46
        [Interval(81, 87), Interval(98, 100), Interval(68, 86), Interval(47, 55), Interval(21, 25),
         Interval(71, 83), Interval(73, 73), Interval(1, 1), Interval(62, 68), Interval(36, 36),
         Interval(81, 95), Interval(11, 11), Interval(73, 87), Interval(81, 89), Interval(45, 57),
         Interval(23, 29), Interval(5, 5), Interval(71, 95), Interval(17, 23), Interval(60, 60)],
        # Job 47
        [Interval(19, 23), Interval(12, 12), Interval(89, 99), Interval(7, 9), Interval(13, 15),
         Interval(34, 34), Interval(4, 4), Interval(53, 63), Interval(54, 66), Interval(49, 53),
         Interval(45, 45), Interval(94, 96), Interval(18, 24), Interval(90, 94), Interval(84, 96),
         Interval(67, 87), Interval(13, 13), Interval(48, 54), Interval(82, 106), Interval(32, 34)],
        # Job 48
        [Interval(67, 83), Interval(73, 97), Interval(75, 87), Interval(76, 86), Interval(90, 94),
         Interval(96, 96), Interval(83, 89), Interval(88, 94), Interval(92, 102), Interval(12, 12),
         Interval(13, 17), Interval(11, 11), Interval(75, 93), Interval(25, 29), Interval(29, 37),
         Interval(1, 1), Interval(82, 92), Interval(53, 57), Interval(32, 32), Interval(7, 9)],
        # Job 49
        [Interval(17, 23), Interval(69, 73), Interval(56, 72), Interval(82, 88), Interval(47, 51),
         Interval(6, 6), Interval(49, 55), Interval(79, 91), Interval(15, 15), Interval(41, 53),
         Interval(5, 5), Interval(21, 25), Interval(40, 40), Interval(43, 49), Interval(45, 51),
         Interval(75, 99), Interval(80, 104), Interval(47, 61), Interval(71, 95), Interval(2, 2)],
        # Job 50
        [Interval(66, 82), Interval(30, 34), Interval(15, 15), Interval(91, 95), Interval(12, 16),
         Interval(35, 47), Interval(87, 107), Interval(83, 83), Interval(25, 33), Interval(89, 97),
         Interval(27, 33), Interval(85, 111), Interval(15, 15), Interval(46, 50), Interval(30, 32),
         Interval(36, 44), Interval(35, 37), Interval(52, 54), Interval(26, 26), Interval(92, 106)],
        # Job 51
        [Interval(54, 64), Interval(61, 71), Interval(27, 29), Interval(26, 26), Interval(60, 70),
         Interval(84, 106), Interval(54, 54), Interval(20, 26), Interval(22, 28), Interval(3, 3),
         Interval(81, 87), Interval(72, 72), Interval(53, 59), Interval(80, 108), Interval(91, 93),
         Interval(14, 16), Interval(40, 42), Interval(25, 29), Interval(42, 50), Interval(52, 52)],
        # Job 52
        [Interval(91, 107), Interval(7, 7), Interval(33, 33), Interval(78, 102), Interval(71, 93),
         Interval(15, 17), Interval(75, 87), Interval(75, 85), Interval(69, 81), Interval(82, 102),
         Interval(88, 98), Interval(49, 49), Interval(12, 16), Interval(15, 17), Interval(43, 55),
         Interval(84, 92), Interval(48, 54), Interval(49, 51), Interval(10, 12), Interval(30, 38)],
        # Job 53
        [Interval(41, 45), Interval(35, 35), Interval(91, 91), Interval(81, 99), Interval(30, 38),
         Interval(63, 77), Interval(19, 25), Interval(26, 26), Interval(51, 59), Interval(31, 37),
         Interval(55, 55), Interval(30, 38), Interval(61, 75), Interval(93, 105), Interval(24, 24),
         Interval(36, 44), Interval(23, 27), Interval(53, 67), Interval(13, 13), Interval(80, 84)],
        # Job 54
        [Interval(65, 71), Interval(41, 55), Interval(62, 66), Interval(73, 79), Interval(13, 17),
         Interval(23, 23), Interval(59, 65), Interval(25, 27), Interval(37, 41), Interval(46, 58),
         Interval(6, 6), Interval(44, 50), Interval(37, 41), Interval(80, 82), Interval(45, 49),
         Interval(88, 108), Interval(24, 26), Interval(53, 63), Interval(59, 75), Interval(45, 47)],
        # Job 55
        [Interval(17, 17), Interval(31, 39), Interval(83, 87), Interval(15, 15), Interval(80, 90),
         Interval(43, 49), Interval(5, 5), Interval(65, 81), Interval(56, 70), Interval(87, 107),
         Interval(18, 24), Interval(29, 39), Interval(58, 60), Interval(2, 2), Interval(56, 72),
         Interval(76, 100), Interval(22, 22), Interval(17, 17), Interval(40, 54), Interval(69, 85)],
        # Job 56
        [Interval(76, 86), Interval(60, 60), Interval(16, 18), Interval(25, 25), Interval(44, 48),
         Interval(77, 83), Interval(14, 16), Interval(30, 32), Interval(54, 66), Interval(26, 30),
         Interval(41, 41), Interval(32, 38), Interval(17, 23), Interval(71, 91), Interval(40, 40),
         Interval(48, 54), Interval(14, 14), Interval(35, 37), Interval(30, 30), Interval(72, 78)],
        # Job 57
        [Interval(21, 21), Interval(82, 104), Interval(89, 89), Interval(14, 16), Interval(7, 9),
         Interval(88, 96), Interval(18, 20), Interval(18, 20), Interval(45, 45), Interval(40, 52),
         Interval(87, 107), Interval(6, 6), Interval(42, 42), Interval(52, 68), Interval(9, 11),
         Interval(36, 38), Interval(91, 103), Interval(2, 2), Interval(50, 52), Interval(50, 62)],
        # Job 58
        [Interval(52, 68), Interval(81, 83), Interval(92, 98), Interval(86, 98), Interval(2, 2),
         Interval(73, 83), Interval(78, 94), Interval(57, 75), Interval(81, 103), Interval(89, 97),
         Interval(38, 40), Interval(54, 62), Interval(53, 61), Interval(6, 6), Interval(16, 20),
         Interval(98, 98), Interval(52, 52), Interval(71, 95), Interval(35, 37), Interval(51, 69)],
        # Job 59
        [Interval(51, 59), Interval(87, 101), Interval(91, 95), Interval(57, 73), Interval(31, 35),
         Interval(20, 24), Interval(34, 42), Interval(43, 47), Interval(16, 20), Interval(7, 7),
         Interval(47, 51), Interval(79, 83), Interval(16, 16), Interval(2, 2), Interval(61, 73),
         Interval(7, 9), Interval(29, 39), Interval(46, 52), Interval(61, 77), Interval(35, 35)],
        # Job 60
        [Interval(25, 31), Interval(2, 2), Interval(67, 89), Interval(48, 60), Interval(13, 15),
         Interval(45, 49), Interval(62, 80), Interval(63, 81), Interval(45, 57), Interval(83, 83),
         Interval(23, 25), Interval(13, 13), Interval(10, 12), Interval(18, 24), Interval(71, 71),
         Interval(77, 79), Interval(68, 68), Interval(78, 90), Interval(46, 48), Interval(7, 7)],
        # Job 61
        [Interval(16, 18), Interval(73, 97), Interval(84, 104), Interval(88, 102), Interval(11, 11),
         Interval(51, 65), Interval(68, 82), Interval(63, 77), Interval(62, 66), Interval(14, 18),
         Interval(73, 73), Interval(22, 22), Interval(17, 17), Interval(41, 49), Interval(74, 74),
         Interval(75, 91), Interval(72, 72), Interval(12, 14), Interval(47, 47), Interval(71, 87)],
        # Job 62
        [Interval(39, 45), Interval(37, 37), Interval(67, 77), Interval(16, 16), Interval(50, 56),
         Interval(5, 5), Interval(61, 63), Interval(80, 96), Interval(32, 38), Interval(85, 85),
         Interval(52, 64), Interval(56, 60), Interval(7, 7), Interval(78, 84), Interval(87, 89),
         Interval(73, 75), Interval(68, 82), Interval(58, 76), Interval(61, 81), Interval(53, 63)],
        # Job 63
        [Interval(35, 43), Interval(5, 5), Interval(81, 103), Interval(66, 70), Interval(30, 38),
         Interval(87, 97), Interval(15, 19), Interval(30, 36), Interval(9, 9), Interval(51, 59),
         Interval(42, 56), Interval(45, 53), Interval(12, 12), Interval(23, 25), Interval(85, 99),
         Interval(60, 80), Interval(40, 42), Interval(33, 41), Interval(14, 16), Interval(21, 23)],
        # Job 64
        [Interval(69, 81), Interval(29, 39), Interval(62, 76), Interval(48, 48), Interval(6, 8),
         Interval(14, 18), Interval(24, 30), Interval(67, 75), Interval(10, 12), Interval(42, 54),
         Interval(3, 3), Interval(35, 43), Interval(85, 111), Interval(2, 2), Interval(36, 42),
         Interval(2, 2), Interval(11, 11), Interval(66, 70), Interval(73, 77), Interval(49, 49)],
        # Job 65
        [Interval(79, 97), Interval(16, 16), Interval(64, 68), Interval(33, 35), Interval(2, 2),
         Interval(5, 5), Interval(69, 77), Interval(25, 25), Interval(94, 102), Interval(53, 61),
         Interval(41, 51), Interval(83, 99), Interval(81, 83), Interval(46, 56), Interval(1, 1),
         Interval(40, 42), Interval(54, 60), Interval(65, 69), Interval(28, 28), Interval(66, 68)],
        # Job 66
        [Interval(33, 41), Interval(41, 51), Interval(1, 1), Interval(85, 89), Interval(55, 55),
         Interval(23, 27), Interval(42, 44), Interval(9, 11), Interval(24, 30), Interval(6, 6),
         Interval(89, 93), Interval(2, 2), Interval(49, 51), Interval(88, 100), Interval(1, 1),
         Interval(43, 51), Interval(79, 79), Interval(21, 27), Interval(56, 72), Interval(11, 11)],
        # Job 67
        [Interval(32, 32), Interval(24, 24), Interval(80, 88), Interval(13, 13), Interval(11, 11),
         Interval(86, 110), Interval(68, 80), Interval(81, 87), Interval(72, 92), Interval(89, 109),
         Interval(4, 4), Interval(87, 109), Interval(57, 73), Interval(7, 7), Interval(87, 89),
         Interval(23, 27), Interval(67, 69), Interval(86, 100), Interval(63, 83), Interval(29, 35)],
        # Job 68
        [Interval(38, 46), Interval(76, 76), Interval(39, 47), Interval(24, 24), Interval(80, 104),
         Interval(39, 41), Interval(34, 38), Interval(47, 57), Interval(57, 61), Interval(61, 65),
         Interval(13, 17), Interval(54, 54), Interval(61, 79), Interval(75, 97), Interval(44, 52),
         Interval(57, 67), Interval(19, 21), Interval(44, 54), Interval(15, 15), Interval(15, 15)],
        # Job 69
        [Interval(38, 46), Interval(28, 34), Interval(80, 80), Interval(38, 48), Interval(73, 87),
         Interval(21, 25), Interval(82, 96), Interval(57, 61), Interval(17, 21), Interval(54, 54),
         Interval(13, 17), Interval(16, 20), Interval(79, 99), Interval(40, 54), Interval(37, 39),
         Interval(21, 21), Interval(86, 88), Interval(59, 73), Interval(71, 81), Interval(53, 71)],
        # Job 70
        [Interval(53, 55), Interval(50, 56), Interval(19, 19), Interval(55, 55), Interval(83, 83),
         Interval(65, 79), Interval(13, 13), Interval(71, 95), Interval(51, 57), Interval(27, 29),
         Interval(20, 24), Interval(86, 92), Interval(13, 13), Interval(66, 80), Interval(21, 27),
         Interval(12, 12), Interval(70, 94), Interval(15, 15), Interval(71, 85), Interval(93, 95)],
        # Job 71
        [Interval(18, 18), Interval(3, 3), Interval(73, 95), Interval(78, 100), Interval(85, 93),
         Interval(65, 81), Interval(5, 5), Interval(52, 62), Interval(33, 43), Interval(8, 10),
         Interval(71, 83), Interval(15, 19), Interval(13, 15), Interval(29, 35), Interval(25, 31),
         Interval(13, 17), Interval(33, 33), Interval(45, 51), Interval(49, 49), Interval(40, 40)],
        # Job 72
        [Interval(42, 54), Interval(31, 35), Interval(77, 81), Interval(38, 46), Interval(22, 28),
         Interval(8, 10), Interval(25, 25), Interval(1, 1), Interval(43, 57), Interval(51, 59),
         Interval(96, 98), Interval(87, 105), Interval(18, 18), Interval(24, 26), Interval(24, 24),
         Interval(71, 83), Interval(22, 26), Interval(49, 55), Interval(33, 41), Interval(87, 89)],
        # Job 73
        [Interval(49, 65), Interval(46, 54), Interval(58, 70), Interval(77, 101), Interval(10, 10),
         Interval(69, 91), Interval(62, 64), Interval(6, 6), Interval(31, 33), Interval(31, 37),
         Interval(34, 34), Interval(58, 78), Interval(5, 5), Interval(68, 84), Interval(74, 80),
         Interval(80, 92), Interval(65, 69), Interval(65, 87), Interval(72, 90), Interval(44, 58)],
        # Job 74
        [Interval(68, 82), Interval(87, 95), Interval(87, 107), Interval(13, 15), Interval(54, 70),
         Interval(36, 44), Interval(38, 48), Interval(14, 18), Interval(91, 95), Interval(52, 58),
         Interval(4, 4), Interval(23, 27), Interval(25, 33), Interval(40, 50), Interval(73, 93),
         Interval(41, 51), Interval(27, 35), Interval(13, 13), Interval(57, 57), Interval(67, 69)],
        # Job 75
        [Interval(55, 73), Interval(68, 82), Interval(35, 35), Interval(63, 79), Interval(36, 40),
         Interval(49, 59), Interval(32, 40), Interval(64, 78), Interval(59, 73), Interval(66, 78),
         Interval(54, 62), Interval(20, 20), Interval(64, 70), Interval(68, 70), Interval(41, 51),
         Interval(58, 78), Interval(88, 98), Interval(39, 39), Interval(43, 53), Interval(67, 87)],
        # Job 76
        [Interval(52, 66), Interval(34, 34), Interval(6, 6), Interval(68, 84), Interval(12, 14),
         Interval(57, 61), Interval(81, 109), Interval(78, 78), Interval(64, 68), Interval(88, 96),
         Interval(80, 98), Interval(68, 86), Interval(60, 72), Interval(16, 16), Interval(7, 7),
         Interval(69, 81), Interval(92, 102), Interval(6, 8), Interval(74, 88), Interval(12, 14)],
        # Job 77
        [Interval(9, 11), Interval(36, 40), Interval(26, 32), Interval(37, 39), Interval(26, 28),
         Interval(7, 9), Interval(56, 62), Interval(60, 60), Interval(31, 41), Interval(80, 92),
         Interval(34, 44), Interval(17, 21), Interval(72, 96), Interval(45, 55), Interval(61, 69),
         Interval(55, 61), Interval(58, 66), Interval(61, 81), Interval(22, 22), Interval(6, 6)],
        # Job 78
        [Interval(6, 6), Interval(32, 32), Interval(35, 41), Interval(53, 53), Interval(59, 59),
         Interval(29, 37), Interval(5, 5), Interval(36, 38), Interval(76, 94), Interval(29, 37),
         Interval(40, 54), Interval(65, 75), Interval(6, 6), Interval(30, 34), Interval(75, 97),
         Interval(24, 28), Interval(33, 39), Interval(56, 72), Interval(78, 78), Interval(14, 18)],
        # Job 79
        [Interval(56, 64), Interval(4, 4), Interval(43, 45), Interval(12, 16), Interval(39, 51),
         Interval(77, 89), Interval(7, 7), Interval(64, 86), Interval(83, 89), Interval(88, 88),
         Interval(23, 27), Interval(78, 92), Interval(94, 104), Interval(69, 91), Interval(44, 56),
         Interval(86, 96), Interval(14, 14), Interval(86, 88), Interval(72, 74), Interval(72, 72)],
        # Job 80
        [Interval(81, 103), Interval(25, 25), Interval(87, 99), Interval(29, 31), Interval(8, 10),
         Interval(74, 98), Interval(69, 89), Interval(70, 72), Interval(5, 5), Interval(43, 51),
         Interval(58, 64), Interval(70, 86), Interval(65, 87), Interval(67, 75), Interval(92, 104),
         Interval(29, 39), Interval(23, 23), Interval(82, 82), Interval(50, 56), Interval(19, 23)],
        # Job 81
        [Interval(82, 100), Interval(81, 81), Interval(61, 79), Interval(31, 41), Interval(90, 102),
         Interval(21, 25), Interval(51, 59), Interval(84, 102), Interval(77, 95), Interval(14, 16),
         Interval(19, 19), Interval(18, 18), Interval(57, 75), Interval(41, 47), Interval(55, 61),
         Interval(53, 71), Interval(54, 54), Interval(70, 88), Interval(11, 11), Interval(49, 49)],
        # Job 82
        [Interval(58, 66), Interval(77, 77), Interval(8, 10), Interval(4, 4), Interval(72, 88),
         Interval(24, 26), Interval(15, 17), Interval(85, 105), Interval(28, 32), Interval(53, 61),
         Interval(39, 41), Interval(70, 92), Interval(3, 3), Interval(27, 29), Interval(43, 47),
         Interval(53, 65), Interval(80, 108), Interval(29, 33), Interval(89, 93), Interval(47, 63)],
        # Job 83
        [Interval(73, 97), Interval(20, 26), Interval(68, 88), Interval(68, 68), Interval(53, 65),
         Interval(8, 10), Interval(61, 81), Interval(83, 101), Interval(47, 53), Interval(34, 42),
         Interval(35, 35), Interval(31, 31), Interval(83, 99), Interval(52, 62), Interval(68, 72),
         Interval(53, 67), Interval(70, 76), Interval(36, 42), Interval(74, 78), Interval(52, 68)],
        # Job 84
        [Interval(52, 70), Interval(72, 82), Interval(20, 24), Interval(39, 47), Interval(58, 74),
         Interval(43, 51), Interval(46, 60), Interval(88, 106), Interval(86, 96), Interval(59, 69),
         Interval(84, 102), Interval(43, 49), Interval(19, 21), Interval(81, 99), Interval(56, 60),
         Interval(31, 41), Interval(86, 110), Interval(66, 74), Interval(47, 51), Interval(81, 103)],
        # Job 85
        [Interval(35, 35), Interval(56, 56), Interval(42, 48), Interval(14, 16), Interval(73, 85),
         Interval(59, 73), Interval(53, 57), Interval(1, 1), Interval(80, 98), Interval(27, 31),
         Interval(97, 99), Interval(31, 31), Interval(39, 51), Interval(46, 56), Interval(77, 89),
         Interval(7, 7), Interval(72, 80), Interval(5, 5), Interval(72, 84), Interval(73, 81)],
        # Job 86
        [Interval(8, 8), Interval(52, 64), Interval(24, 24), Interval(60, 64), Interval(76, 78),
         Interval(33, 43), Interval(8, 10), Interval(6, 6), Interval(79, 97), Interval(23, 23),
         Interval(9, 9), Interval(12, 12), Interval(9, 9), Interval(59, 71), Interval(67, 69),
         Interval(57, 57), Interval(33, 43), Interval(15, 15), Interval(87, 109), Interval(55, 55)],
        # Job 87
        [Interval(91, 101), Interval(26, 30), Interval(52, 52), Interval(84, 98), Interval(9, 9),
         Interval(13, 17), Interval(41, 47), Interval(65, 73), Interval(94, 104), Interval(14, 16),
         Interval(58, 72), Interval(9, 9), Interval(27, 27), Interval(49, 63), Interval(66, 74),
         Interval(35, 43), Interval(20, 22), Interval(56, 62), Interval(2, 2), Interval(13, 17)],
        # Job 88
        [Interval(92, 104), Interval(75, 93), Interval(41, 47), Interval(10, 10), Interval(81, 87),
         Interval(75, 81), Interval(19, 19), Interval(80, 80), Interval(26, 30), Interval(17, 21),
         Interval(50, 66), Interval(76, 76), Interval(43, 55), Interval(75, 101), Interval(41, 43),
         Interval(71, 85), Interval(73, 83), Interval(85, 97), Interval(80, 86), Interval(25, 33)],
        # Job 89
        [Interval(18, 18), Interval(37, 43), Interval(19, 23), Interval(8, 8), Interval(30, 32),
         Interval(52, 60), Interval(52, 60), Interval(76, 80), Interval(43, 47), Interval(31, 31),
         Interval(79, 79), Interval(45, 49), Interval(71, 75), Interval(59, 73), Interval(27, 27),
         Interval(91, 105), Interval(67, 79), Interval(69, 89), Interval(64, 84), Interval(7, 9)],
        # Job 90
        [Interval(91, 99), Interval(2, 2), Interval(40, 42), Interval(42, 50), Interval(19, 19),
         Interval(31, 39), Interval(40, 42), Interval(72, 92), Interval(67, 87), Interval(3, 3),
         Interval(49, 55), Interval(13, 17), Interval(12, 12), Interval(3, 3), Interval(30, 30),
         Interval(93, 93), Interval(84, 108), Interval(64, 72), Interval(70, 76), Interval(64, 70)],
        # Job 91
        [Interval(89, 95), Interval(58, 62), Interval(40, 50), Interval(61, 69), Interval(5, 5),
         Interval(79, 83), Interval(19, 23), Interval(2, 2), Interval(70, 72), Interval(51, 63),
         Interval(16, 20), Interval(2, 2), Interval(58, 62), Interval(36, 46), Interval(41, 45),
         Interval(34, 38), Interval(67, 83), Interval(50, 60), Interval(70, 88), Interval(33, 43)],
        # Job 92
        [Interval(30, 40), Interval(6, 6), Interval(5, 5), Interval(4, 4), Interval(37, 41),
         Interval(40, 46), Interval(66, 86), Interval(71, 95), Interval(37, 39), Interval(45, 49),
         Interval(3, 3), Interval(58, 78), Interval(53, 63), Interval(44, 54), Interval(88, 110),
         Interval(17, 23), Interval(9, 9), Interval(39, 39), Interval(11, 11), Interval(9, 9)],
        # Job 93
        [Interval(34, 42), Interval(52, 60), Interval(61, 69), Interval(46, 62), Interval(85, 105),
         Interval(6, 6), Interval(8, 8), Interval(48, 58), Interval(9, 9), Interval(41, 47),
         Interval(35, 43), Interval(17, 19), Interval(77, 77), Interval(6, 6), Interval(40, 46),
         Interval(24, 28), Interval(54, 54), Interval(63, 65), Interval(41, 45), Interval(70, 72)],
        # Job 94
        [Interval(68, 82), Interval(29, 33), Interval(50, 52), Interval(94, 96), Interval(50, 50),
         Interval(91, 105), Interval(71, 89), Interval(34, 42), Interval(97, 101), Interval(77, 79),
         Interval(71, 95), Interval(35, 41), Interval(4, 4), Interval(62, 74), Interval(40, 48),
         Interval(82, 108), Interval(68, 86), Interval(16, 16), Interval(82, 96), Interval(50, 54)],
        # Job 95
        [Interval(10, 10), Interval(35, 47), Interval(51, 53), Interval(96, 98), Interval(53, 57),
         Interval(47, 53), Interval(48, 48), Interval(85, 89), Interval(84, 110), Interval(1, 1),
         Interval(27, 27), Interval(59, 79), Interval(4, 4), Interval(75, 75), Interval(54, 64),
         Interval(50, 50), Interval(22, 22), Interval(66, 80), Interval(66, 80), Interval(57, 57)],
        # Job 96
        [Interval(7, 9), Interval(56, 68), Interval(21, 27), Interval(29, 29), Interval(87, 87),
         Interval(69, 75), Interval(33, 35), Interval(23, 23), Interval(32, 38), Interval(1, 1),
         Interval(4, 4), Interval(40, 44), Interval(79, 101), Interval(23, 23), Interval(23, 27),
         Interval(53, 71), Interval(45, 47), Interval(14, 14), Interval(76, 82), Interval(1, 1)],
        # Job 97
        [Interval(12, 14), Interval(83, 109), Interval(42, 44), Interval(79, 105), Interval(11, 11),
         Interval(82, 106), Interval(5, 5), Interval(30, 38), Interval(37, 39), Interval(63, 73),
         Interval(68, 72), Interval(58, 72), Interval(58, 66), Interval(9, 9), Interval(33, 37),
         Interval(84, 104), Interval(12, 12), Interval(27, 33), Interval(81, 101), Interval(61, 65)],
        # Job 98
        [Interval(30, 36), Interval(12, 16), Interval(68, 90), Interval(21, 27), Interval(10, 12),
         Interval(5, 5), Interval(20, 24), Interval(52, 70), Interval(27, 27), Interval(81, 95),
         Interval(4, 4), Interval(75, 81), Interval(60, 64), Interval(63, 81), Interval(55, 57),
         Interval(16, 20), Interval(59, 65), Interval(46, 48), Interval(25, 29), Interval(85, 103)],
        # Job 99
        [Interval(29, 39), Interval(6, 6), Interval(57, 65), Interval(59, 61), Interval(45, 51),
         Interval(2, 2), Interval(57, 71), Interval(24, 30), Interval(15, 17), Interval(69, 73),
         Interval(63, 79), Interval(46, 48), Interval(51, 53), Interval(68, 78), Interval(38, 46),
         Interval(88, 110), Interval(5, 5), Interval(64, 80), Interval(37, 49), Interval(27, 27)],
    ],
    'name': 'INT__TAI100_20_08.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai100_20_08_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI100_20_08.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI100_20_08.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI100_20_08_F_15_01_INTERVAL_DATA
