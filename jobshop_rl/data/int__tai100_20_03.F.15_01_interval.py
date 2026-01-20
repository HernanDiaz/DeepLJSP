"""
Problema INT__TAI100_20_03.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI100_20_03_F_15_01_INTERVAL_DATA = {
    'num_jobs': 100,
    'num_machines': 20,
    'problem_id': 'int__tai100_20_03.F.15_01_interval',
    'sequences': [
        [14, 0, 15, 16, 6, 19, 4, 13, 1, 8, 17, 5, 10, 12, 11, 18, 9, 3, 7, 2],
        [2, 13, 19, 11, 16, 4, 6, 17, 5, 8, 10, 12, 15, 1, 0, 3, 7, 18, 14, 9],
        [10, 6, 2, 16, 7, 3, 13, 9, 14, 19, 4, 8, 17, 11, 0, 1, 18, 5, 15, 12],
        [12, 9, 18, 4, 19, 14, 3, 6, 13, 5, 1, 16, 17, 10, 2, 0, 7, 15, 8, 11],
        [16, 2, 8, 6, 14, 12, 0, 19, 3, 11, 7, 10, 18, 13, 5, 15, 17, 4, 1, 9],
        [19, 8, 1, 13, 17, 3, 10, 2, 9, 12, 7, 5, 15, 4, 14, 6, 16, 11, 0, 18],
        [17, 2, 14, 10, 0, 19, 7, 3, 18, 8, 13, 15, 6, 11, 4, 9, 5, 16, 12, 1],
        [6, 19, 12, 11, 13, 10, 8, 7, 9, 0, 4, 1, 3, 15, 16, 18, 5, 2, 14, 17],
        [14, 16, 6, 0, 19, 5, 9, 18, 2, 3, 17, 8, 10, 1, 12, 15, 11, 7, 13, 4],
        [13, 5, 16, 4, 6, 19, 15, 1, 9, 14, 7, 11, 8, 17, 2, 12, 0, 10, 3, 18],
        [10, 5, 1, 2, 6, 18, 9, 11, 8, 12, 3, 17, 13, 7, 14, 15, 4, 19, 0, 16],
        [7, 5, 17, 10, 3, 8, 14, 4, 13, 6, 16, 0, 12, 18, 2, 11, 19, 15, 1, 9],
        [19, 5, 3, 0, 8, 7, 2, 1, 9, 15, 17, 16, 10, 4, 18, 12, 14, 6, 11, 13],
        [19, 4, 16, 17, 7, 5, 2, 15, 9, 8, 1, 18, 6, 10, 0, 14, 12, 3, 11, 13],
        [3, 0, 8, 14, 5, 16, 19, 4, 2, 11, 12, 17, 9, 15, 13, 7, 1, 6, 18, 10],
        [5, 17, 2, 10, 6, 9, 15, 0, 11, 3, 4, 7, 8, 1, 19, 16, 13, 18, 14, 12],
        [10, 4, 15, 13, 9, 14, 1, 2, 3, 16, 0, 19, 11, 7, 8, 18, 17, 6, 5, 12],
        [2, 8, 7, 11, 0, 17, 4, 13, 19, 12, 3, 15, 16, 5, 10, 18, 9, 6, 14, 1],
        [19, 9, 3, 16, 10, 17, 12, 13, 2, 15, 6, 4, 8, 18, 5, 0, 7, 1, 11, 14],
        [2, 14, 15, 8, 4, 10, 0, 12, 1, 5, 17, 19, 13, 11, 7, 16, 6, 9, 18, 3],
        [4, 9, 17, 11, 5, 8, 16, 1, 19, 2, 18, 15, 7, 12, 14, 13, 10, 6, 3, 0],
        [0, 3, 13, 11, 5, 6, 14, 1, 18, 2, 19, 16, 15, 8, 4, 7, 12, 10, 9, 17],
        [16, 8, 2, 4, 17, 18, 7, 15, 14, 12, 6, 3, 19, 13, 10, 1, 0, 11, 9, 5],
        [2, 12, 14, 18, 11, 9, 19, 7, 6, 15, 5, 1, 4, 10, 16, 8, 13, 17, 3, 0],
        [10, 9, 16, 0, 1, 7, 19, 13, 14, 2, 3, 6, 12, 15, 4, 8, 17, 18, 5, 11],
        [15, 3, 5, 6, 18, 9, 10, 7, 14, 13, 17, 1, 4, 11, 16, 19, 0, 12, 2, 8],
        [15, 19, 8, 4, 11, 6, 17, 3, 12, 7, 16, 10, 13, 1, 2, 18, 5, 14, 0, 9],
        [6, 11, 13, 5, 18, 3, 0, 16, 7, 2, 17, 1, 15, 8, 4, 19, 9, 14, 10, 12],
        [1, 0, 16, 12, 7, 4, 18, 9, 15, 17, 10, 6, 19, 11, 3, 8, 14, 5, 13, 2],
        [2, 19, 11, 0, 18, 16, 13, 5, 7, 4, 8, 1, 14, 15, 6, 10, 3, 17, 9, 12],
        [0, 16, 1, 18, 10, 19, 3, 8, 9, 11, 2, 14, 15, 17, 5, 7, 6, 13, 4, 12],
        [13, 15, 1, 5, 14, 10, 6, 12, 4, 0, 8, 7, 11, 2, 19, 17, 9, 16, 3, 18],
        [9, 12, 10, 5, 16, 7, 6, 19, 8, 0, 13, 4, 1, 14, 17, 2, 11, 18, 3, 15],
        [17, 7, 16, 8, 18, 9, 5, 1, 19, 13, 4, 14, 10, 15, 0, 2, 3, 11, 6, 12],
        [4, 3, 18, 12, 9, 6, 11, 14, 10, 1, 7, 17, 8, 5, 16, 0, 19, 15, 13, 2],
        [19, 13, 9, 0, 14, 8, 12, 10, 5, 7, 16, 17, 15, 3, 11, 6, 4, 18, 2, 1],
        [19, 7, 9, 17, 13, 5, 2, 15, 3, 1, 14, 16, 18, 0, 10, 8, 6, 11, 4, 12],
        [7, 0, 17, 13, 12, 14, 1, 8, 6, 18, 2, 3, 9, 5, 10, 15, 19, 11, 4, 16],
        [9, 7, 8, 19, 12, 3, 1, 14, 18, 11, 16, 13, 4, 5, 17, 0, 2, 15, 6, 10],
        [6, 8, 18, 7, 16, 1, 5, 14, 3, 9, 19, 4, 11, 2, 17, 12, 15, 0, 10, 13],
        [19, 3, 2, 8, 5, 7, 14, 17, 0, 1, 13, 15, 12, 4, 9, 10, 18, 11, 16, 6],
        [3, 12, 4, 8, 10, 1, 16, 0, 9, 17, 14, 13, 19, 18, 15, 11, 6, 7, 2, 5],
        [13, 12, 0, 5, 8, 18, 7, 1, 3, 4, 16, 11, 10, 15, 9, 19, 17, 14, 2, 6],
        [4, 16, 3, 19, 7, 1, 0, 11, 5, 6, 10, 8, 17, 9, 13, 12, 2, 18, 15, 14],
        [4, 15, 16, 8, 9, 17, 5, 11, 18, 0, 14, 6, 10, 2, 3, 13, 12, 7, 19, 1],
        [15, 5, 16, 12, 1, 17, 0, 18, 10, 19, 8, 14, 11, 13, 2, 9, 4, 3, 7, 6],
        [5, 4, 15, 9, 2, 7, 19, 14, 8, 16, 11, 12, 0, 17, 6, 13, 3, 18, 1, 10],
        [3, 14, 5, 13, 15, 0, 4, 8, 19, 16, 7, 6, 17, 12, 1, 10, 11, 2, 9, 18],
        [2, 17, 7, 0, 14, 8, 1, 12, 18, 13, 10, 6, 15, 4, 3, 5, 9, 19, 16, 11],
        [18, 7, 14, 2, 1, 19, 6, 8, 11, 13, 10, 15, 3, 0, 12, 4, 17, 5, 9, 16],
        [2, 5, 8, 19, 7, 15, 4, 16, 13, 6, 12, 18, 17, 14, 0, 10, 11, 3, 9, 1],
        [5, 14, 18, 13, 15, 0, 12, 7, 8, 6, 1, 3, 2, 10, 9, 19, 11, 4, 16, 17],
        [10, 15, 9, 14, 11, 8, 7, 1, 3, 17, 18, 0, 5, 4, 16, 19, 2, 12, 13, 6],
        [13, 14, 9, 11, 19, 6, 4, 7, 5, 12, 0, 18, 17, 8, 2, 1, 16, 3, 10, 15],
        [11, 18, 19, 17, 14, 9, 4, 16, 8, 6, 0, 2, 7, 15, 12, 13, 5, 1, 10, 3],
        [18, 5, 4, 0, 14, 1, 12, 19, 3, 16, 11, 7, 17, 13, 8, 2, 9, 10, 15, 6],
        [5, 17, 14, 10, 8, 6, 18, 9, 0, 13, 1, 2, 19, 4, 7, 11, 16, 3, 12, 15],
        [9, 7, 13, 16, 3, 19, 14, 6, 5, 11, 1, 18, 4, 12, 8, 0, 2, 10, 15, 17],
        [1, 0, 5, 19, 10, 2, 7, 9, 8, 4, 18, 14, 17, 11, 12, 6, 16, 3, 15, 13],
        [3, 6, 1, 7, 9, 14, 10, 0, 5, 13, 19, 4, 12, 17, 8, 16, 2, 18, 11, 15],
        [10, 1, 8, 18, 4, 6, 13, 12, 7, 0, 9, 14, 3, 11, 16, 19, 2, 5, 15, 17],
        [17, 4, 16, 7, 10, 14, 19, 12, 8, 1, 15, 3, 13, 11, 0, 6, 2, 18, 9, 5],
        [14, 16, 19, 13, 10, 8, 0, 11, 4, 6, 2, 7, 3, 18, 17, 15, 9, 12, 1, 5],
        [2, 8, 19, 5, 12, 3, 11, 13, 9, 17, 7, 4, 6, 0, 15, 14, 16, 10, 1, 18],
        [14, 1, 12, 2, 0, 5, 9, 7, 17, 16, 10, 4, 8, 13, 11, 18, 15, 6, 19, 3],
        [1, 15, 18, 8, 16, 10, 14, 7, 12, 13, 2, 5, 9, 19, 0, 11, 6, 4, 3, 17],
        [1, 19, 5, 4, 15, 6, 14, 8, 12, 3, 18, 13, 11, 0, 2, 16, 10, 7, 17, 9],
        [4, 15, 17, 6, 16, 5, 10, 7, 18, 12, 19, 9, 14, 13, 0, 3, 8, 2, 11, 1],
        [2, 14, 5, 11, 12, 7, 16, 9, 13, 18, 19, 3, 8, 6, 4, 10, 17, 15, 1, 0],
        [6, 14, 8, 5, 11, 18, 2, 4, 1, 15, 13, 9, 3, 16, 19, 12, 7, 0, 17, 10],
        [18, 5, 0, 15, 3, 4, 1, 17, 9, 7, 14, 16, 8, 6, 11, 2, 12, 19, 13, 10],
        [0, 1, 3, 18, 13, 8, 17, 4, 2, 5, 16, 6, 7, 19, 9, 15, 12, 10, 11, 14],
        [19, 1, 3, 15, 8, 13, 14, 18, 11, 2, 12, 17, 16, 9, 4, 10, 5, 6, 0, 7],
        [5, 1, 9, 0, 16, 10, 7, 11, 18, 4, 15, 3, 14, 12, 8, 19, 2, 6, 17, 13],
        [6, 1, 19, 3, 9, 17, 10, 2, 12, 0, 15, 8, 11, 18, 7, 14, 13, 16, 5, 4],
        [0, 5, 4, 2, 3, 15, 10, 19, 11, 17, 13, 14, 16, 6, 8, 18, 9, 7, 12, 1],
        [1, 12, 7, 17, 10, 16, 4, 8, 6, 13, 14, 18, 5, 15, 0, 11, 3, 2, 9, 19],
        [8, 13, 3, 10, 6, 18, 19, 5, 4, 14, 15, 1, 11, 0, 7, 17, 2, 9, 16, 12],
        [12, 13, 15, 8, 10, 4, 1, 3, 0, 9, 7, 2, 16, 19, 11, 14, 5, 6, 18, 17],
        [9, 16, 8, 1, 12, 5, 15, 18, 7, 4, 3, 14, 2, 13, 10, 0, 11, 17, 19, 6],
        [4, 9, 16, 12, 19, 5, 15, 3, 0, 1, 17, 10, 18, 6, 2, 11, 7, 8, 13, 14],
        [10, 8, 14, 9, 2, 3, 4, 0, 18, 1, 16, 17, 6, 7, 15, 12, 5, 19, 13, 11],
        [2, 14, 1, 0, 5, 19, 15, 4, 7, 12, 3, 13, 10, 6, 9, 8, 17, 16, 11, 18],
        [9, 4, 19, 12, 18, 6, 14, 3, 8, 11, 13, 5, 16, 7, 15, 17, 10, 0, 1, 2],
        [12, 0, 10, 19, 14, 17, 18, 3, 5, 16, 6, 7, 8, 9, 2, 1, 4, 13, 15, 11],
        [9, 6, 0, 12, 3, 4, 19, 17, 5, 10, 14, 7, 1, 13, 2, 18, 8, 11, 15, 16],
        [18, 5, 13, 0, 10, 8, 16, 7, 12, 14, 17, 15, 11, 3, 6, 2, 1, 19, 4, 9],
        [17, 4, 18, 1, 7, 16, 13, 6, 19, 5, 14, 15, 10, 11, 12, 0, 3, 9, 8, 2],
        [3, 17, 5, 9, 19, 18, 0, 15, 8, 13, 11, 1, 12, 4, 2, 10, 16, 6, 14, 7],
        [7, 13, 10, 17, 14, 0, 2, 16, 18, 19, 3, 5, 11, 4, 9, 12, 15, 6, 8, 1],
        [1, 5, 0, 13, 4, 6, 3, 12, 7, 14, 16, 8, 11, 15, 17, 9, 2, 10, 18, 19],
        [13, 12, 3, 14, 5, 19, 16, 10, 2, 0, 15, 8, 6, 17, 7, 1, 4, 11, 18, 9],
        [16, 18, 11, 4, 8, 17, 3, 14, 7, 1, 13, 10, 0, 12, 2, 6, 9, 15, 19, 5],
        [12, 8, 4, 6, 0, 15, 19, 5, 9, 1, 3, 10, 2, 16, 18, 13, 7, 17, 11, 14],
        [17, 14, 6, 8, 11, 13, 19, 12, 7, 4, 16, 2, 15, 18, 3, 1, 0, 9, 10, 5],
        [14, 18, 13, 7, 4, 15, 3, 11, 19, 5, 10, 2, 1, 0, 16, 6, 8, 17, 12, 9],
        [7, 16, 5, 13, 18, 19, 11, 1, 4, 8, 3, 9, 15, 2, 0, 10, 12, 14, 6, 17],
        [17, 2, 8, 4, 19, 0, 14, 9, 18, 13, 5, 6, 12, 7, 3, 16, 11, 1, 15, 10],
        [10, 8, 19, 2, 11, 5, 15, 9, 4, 0, 12, 1, 17, 18, 3, 7, 13, 6, 14, 16],
        [13, 15, 4, 12, 1, 17, 18, 3, 2, 6, 7, 16, 11, 5, 14, 0, 8, 9, 10, 19],
    ],
    'durations': [
        # Job 0
        [Interval(50, 64), Interval(17, 19), Interval(42, 46), Interval(16, 18), Interval(59, 73),
         Interval(29, 39), Interval(80, 86), Interval(65, 87), Interval(57, 75), Interval(18, 22),
         Interval(85, 103), Interval(64, 70), Interval(65, 87), Interval(1, 1), Interval(81, 87),
         Interval(28, 34), Interval(72, 84), Interval(15, 17), Interval(13, 17), Interval(78, 104)],
        # Job 1
        [Interval(50, 62), Interval(89, 93), Interval(60, 64), Interval(32, 32), Interval(55, 67),
         Interval(48, 50), Interval(26, 28), Interval(91, 97), Interval(83, 101), Interval(27, 27),
         Interval(6, 8), Interval(90, 108), Interval(24, 28), Interval(72, 88), Interval(90, 90),
         Interval(59, 63), Interval(37, 43), Interval(66, 82), Interval(16, 20), Interval(38, 38)],
        # Job 2
        [Interval(23, 27), Interval(54, 68), Interval(5, 5), Interval(69, 77), Interval(8, 10),
         Interval(17, 17), Interval(23, 27), Interval(97, 101), Interval(19, 25), Interval(22, 26),
         Interval(89, 95), Interval(83, 99), Interval(19, 19), Interval(19, 21), Interval(31, 37),
         Interval(80, 84), Interval(90, 92), Interval(33, 43), Interval(84, 90), Interval(13, 13)],
        # Job 3
        [Interval(29, 31), Interval(49, 51), Interval(13, 13), Interval(66, 88), Interval(10, 10),
         Interval(79, 105), Interval(83, 87), Interval(75, 93), Interval(84, 112), Interval(23, 27),
         Interval(55, 63), Interval(63, 75), Interval(58, 78), Interval(43, 53), Interval(75, 83),
         Interval(83, 97), Interval(36, 46), Interval(54, 66), Interval(51, 65), Interval(69, 77)],
        # Job 4
        [Interval(70, 70), Interval(89, 97), Interval(62, 82), Interval(16, 18), Interval(2, 2),
         Interval(75, 99), Interval(17, 21), Interval(43, 45), Interval(34, 42), Interval(28, 30),
         Interval(62, 62), Interval(38, 50), Interval(16, 20), Interval(46, 58), Interval(61, 65),
         Interval(38, 44), Interval(99, 99), Interval(60, 76), Interval(38, 46), Interval(1, 1)],
        # Job 5
        [Interval(63, 65), Interval(61, 69), Interval(29, 39), Interval(67, 79), Interval(32, 32),
         Interval(17, 17), Interval(31, 31), Interval(77, 83), Interval(61, 65), Interval(12, 14),
         Interval(3, 3), Interval(30, 38), Interval(2, 2), Interval(56, 64), Interval(6, 6),
         Interval(89, 97), Interval(36, 42), Interval(31, 31), Interval(56, 60), Interval(6, 6)],
        # Job 6
        [Interval(83, 99), Interval(62, 68), Interval(22, 22), Interval(4, 4), Interval(68, 76),
         Interval(48, 52), Interval(83, 87), Interval(4, 4), Interval(6, 8), Interval(53, 63),
         Interval(89, 103), Interval(19, 23), Interval(53, 71), Interval(14, 16), Interval(69, 89),
         Interval(33, 39), Interval(57, 59), Interval(41, 45), Interval(18, 24), Interval(40, 50)],
        # Job 7
        [Interval(6, 6), Interval(3, 3), Interval(20, 22), Interval(1, 1), Interval(58, 62),
         Interval(29, 35), Interval(28, 34), Interval(38, 48), Interval(84, 86), Interval(57, 61),
         Interval(45, 51), Interval(10, 12), Interval(67, 73), Interval(21, 21), Interval(75, 101),
         Interval(86, 98), Interval(90, 90), Interval(4, 4), Interval(47, 51), Interval(38, 46)],
        # Job 8
        [Interval(81, 97), Interval(91, 107), Interval(73, 95), Interval(68, 70), Interval(30, 40),
         Interval(22, 22), Interval(42, 42), Interval(12, 14), Interval(5, 5), Interval(30, 36),
         Interval(13, 17), Interval(21, 23), Interval(15, 17), Interval(12, 12), Interval(19, 25),
         Interval(25, 27), Interval(52, 52), Interval(11, 11), Interval(37, 41), Interval(38, 40)],
        # Job 9
        [Interval(1, 1), Interval(58, 76), Interval(65, 75), Interval(74, 74), Interval(47, 57),
         Interval(30, 40), Interval(74, 92), Interval(2, 2), Interval(55, 59), Interval(23, 25),
         Interval(53, 63), Interval(75, 81), Interval(59, 71), Interval(43, 45), Interval(84, 106),
         Interval(5, 5), Interval(47, 47), Interval(69, 69), Interval(60, 72), Interval(33, 43)],
        # Job 10
        [Interval(56, 74), Interval(67, 75), Interval(32, 36), Interval(6, 6), Interval(88, 88),
         Interval(87, 105), Interval(77, 83), Interval(79, 95), Interval(54, 58), Interval(13, 17),
         Interval(59, 65), Interval(72, 78), Interval(57, 65), Interval(3, 3), Interval(53, 59),
         Interval(61, 73), Interval(6, 6), Interval(37, 37), Interval(32, 36), Interval(4, 4)],
        # Job 11
        [Interval(23, 23), Interval(37, 49), Interval(27, 29), Interval(69, 87), Interval(68, 86),
         Interval(54, 56), Interval(26, 28), Interval(77, 83), Interval(42, 42), Interval(49, 53),
         Interval(52, 56), Interval(8, 10), Interval(75, 95), Interval(91, 95), Interval(68, 86),
         Interval(28, 34), Interval(69, 83), Interval(39, 47), Interval(26, 32), Interval(8, 8)],
        # Job 12
        [Interval(50, 60), Interval(43, 55), Interval(22, 22), Interval(21, 21), Interval(51, 63),
         Interval(24, 26), Interval(2, 2), Interval(74, 100), Interval(68, 80), Interval(90, 98),
         Interval(7, 7), Interval(73, 97), Interval(43, 49), Interval(64, 86), Interval(84, 98),
         Interval(38, 40), Interval(21, 21), Interval(16, 18), Interval(66, 66), Interval(80, 86)],
        # Job 13
        [Interval(37, 47), Interval(7, 9), Interval(22, 28), Interval(42, 42), Interval(39, 39),
         Interval(11, 13), Interval(11, 11), Interval(65, 81), Interval(24, 26), Interval(58, 68),
         Interval(56, 74), Interval(54, 60), Interval(76, 78), Interval(44, 54), Interval(18, 18),
         Interval(1, 1), Interval(84, 84), Interval(54, 62), Interval(63, 71), Interval(8, 8)],
        # Job 14
        [Interval(28, 32), Interval(23, 29), Interval(31, 39), Interval(39, 41), Interval(29, 39),
         Interval(1, 1), Interval(81, 95), Interval(85, 99), Interval(53, 53), Interval(51, 65),
         Interval(32, 32), Interval(61, 79), Interval(11, 11), Interval(21, 27), Interval(61, 67),
         Interval(45, 55), Interval(61, 75), Interval(92, 106), Interval(38, 38), Interval(10, 12)],
        # Job 15
        [Interval(38, 38), Interval(90, 96), Interval(50, 50), Interval(62, 76), Interval(67, 89),
         Interval(59, 65), Interval(65, 75), Interval(40, 50), Interval(6, 8), Interval(82, 92),
         Interval(77, 77), Interval(85, 89), Interval(81, 91), Interval(62, 70), Interval(34, 36),
         Interval(42, 42), Interval(71, 93), Interval(52, 58), Interval(26, 30), Interval(22, 24)],
        # Job 16
        [Interval(77, 87), Interval(93, 105), Interval(94, 102), Interval(44, 56), Interval(47, 51),
         Interval(21, 23), Interval(8, 10), Interval(47, 57), Interval(21, 21), Interval(36, 40),
         Interval(46, 54), Interval(71, 77), Interval(51, 65), Interval(44, 44), Interval(5, 5),
         Interval(51, 55), Interval(58, 64), Interval(19, 23), Interval(84, 94), Interval(62, 62)],
        # Job 17
        [Interval(11, 13), Interval(54, 66), Interval(27, 27), Interval(69, 79), Interval(56, 64),
         Interval(7, 9), Interval(25, 27), Interval(3, 3), Interval(26, 34), Interval(6, 6),
         Interval(46, 46), Interval(63, 63), Interval(60, 74), Interval(15, 19), Interval(71, 79),
         Interval(51, 63), Interval(49, 53), Interval(47, 57), Interval(13, 13), Interval(74, 100)],
        # Job 18
        [Interval(64, 72), Interval(21, 25), Interval(6, 6), Interval(17, 23), Interval(73, 75),
         Interval(27, 33), Interval(12, 16), Interval(41, 51), Interval(42, 56), Interval(59, 75),
         Interval(29, 39), Interval(41, 53), Interval(73, 93), Interval(45, 45), Interval(38, 48),
         Interval(72, 78), Interval(39, 43), Interval(72, 90), Interval(75, 85), Interval(54, 56)],
        # Job 19
        [Interval(39, 47), Interval(16, 18), Interval(24, 28), Interval(5, 5), Interval(19, 25),
         Interval(44, 58), Interval(9, 9), Interval(56, 66), Interval(15, 17), Interval(86, 100),
         Interval(69, 83), Interval(29, 39), Interval(5, 5), Interval(29, 31), Interval(77, 85),
         Interval(33, 39), Interval(12, 14), Interval(21, 25), Interval(73, 79), Interval(28, 34)],
        # Job 20
        [Interval(22, 28), Interval(51, 63), Interval(50, 52), Interval(46, 56), Interval(22, 22),
         Interval(88, 94), Interval(31, 33), Interval(20, 24), Interval(7, 7), Interval(89, 109),
         Interval(55, 67), Interval(6, 8), Interval(65, 69), Interval(76, 98), Interval(95, 95),
         Interval(73, 85), Interval(17, 21), Interval(37, 37), Interval(92, 92), Interval(22, 24)],
        # Job 21
        [Interval(53, 61), Interval(22, 24), Interval(98, 100), Interval(40, 50), Interval(46, 48),
         Interval(54, 64), Interval(51, 55), Interval(62, 74), Interval(63, 73), Interval(48, 62),
         Interval(19, 19), Interval(66, 86), Interval(30, 30), Interval(74, 100), Interval(48, 62),
         Interval(74, 80), Interval(12, 12), Interval(36, 44), Interval(28, 32), Interval(72, 80)],
        # Job 22
        [Interval(92, 100), Interval(24, 26), Interval(77, 89), Interval(40, 42), Interval(65, 87),
         Interval(44, 46), Interval(20, 26), Interval(61, 69), Interval(71, 75), Interval(30, 40),
         Interval(4, 4), Interval(45, 49), Interval(51, 69), Interval(65, 83), Interval(80, 108),
         Interval(44, 58), Interval(43, 57), Interval(82, 82), Interval(75, 93), Interval(11, 11)],
        # Job 23
        [Interval(76, 102), Interval(66, 86), Interval(15, 15), Interval(58, 78), Interval(76, 86),
         Interval(76, 86), Interval(53, 57), Interval(56, 56), Interval(68, 88), Interval(41, 51),
         Interval(83, 101), Interval(15, 15), Interval(5, 5), Interval(11, 13), Interval(49, 49),
         Interval(60, 60), Interval(86, 102), Interval(11, 13), Interval(33, 33), Interval(40, 54)],
        # Job 24
        [Interval(54, 58), Interval(13, 15), Interval(74, 86), Interval(11, 11), Interval(46, 54),
         Interval(44, 58), Interval(72, 94), Interval(56, 74), Interval(75, 99), Interval(46, 54),
         Interval(74, 82), Interval(6, 6), Interval(18, 18), Interval(38, 42), Interval(38, 48),
         Interval(77, 97), Interval(67, 81), Interval(76, 76), Interval(69, 77), Interval(47, 55)],
        # Job 25
        [Interval(62, 64), Interval(52, 58), Interval(44, 54), Interval(47, 57), Interval(61, 71),
         Interval(23, 31), Interval(63, 69), Interval(1, 1), Interval(74, 92), Interval(21, 25),
         Interval(47, 51), Interval(95, 95), Interval(41, 55), Interval(23, 29), Interval(56, 56),
         Interval(20, 20), Interval(6, 8), Interval(6, 6), Interval(37, 49), Interval(49, 55)],
        # Job 26
        [Interval(28, 30), Interval(88, 92), Interval(78, 88), Interval(33, 33), Interval(81, 101),
         Interval(39, 51), Interval(67, 75), Interval(48, 50), Interval(90, 90), Interval(64, 80),
         Interval(69, 89), Interval(51, 61), Interval(62, 68), Interval(10, 12), Interval(70, 78),
         Interval(36, 36), Interval(65, 87), Interval(1, 1), Interval(2, 2), Interval(71, 77)],
        # Job 27
        [Interval(82, 96), Interval(18, 18), Interval(71, 75), Interval(42, 48), Interval(35, 39),
         Interval(41, 47), Interval(23, 27), Interval(78, 94), Interval(65, 67), Interval(18, 20),
         Interval(73, 79), Interval(29, 33), Interval(42, 46), Interval(11, 13), Interval(49, 59),
         Interval(70, 76), Interval(39, 45), Interval(1, 1), Interval(79, 103), Interval(27, 35)],
        # Job 28
        [Interval(68, 78), Interval(19, 19), Interval(90, 104), Interval(46, 54), Interval(66, 82),
         Interval(26, 34), Interval(4, 4), Interval(64, 74), Interval(41, 47), Interval(88, 108),
         Interval(18, 20), Interval(2, 2), Interval(85, 95), Interval(33, 35), Interval(44, 48),
         Interval(75, 77), Interval(74, 88), Interval(68, 84), Interval(34, 46), Interval(50, 50)],
        # Job 29
        [Interval(4, 4), Interval(54, 66), Interval(5, 5), Interval(19, 19), Interval(45, 53),
         Interval(23, 29), Interval(18, 18), Interval(82, 110), Interval(32, 42), Interval(51, 59),
         Interval(81, 85), Interval(70, 74), Interval(68, 84), Interval(34, 42), Interval(89, 101),
         Interval(89, 107), Interval(61, 69), Interval(68, 80), Interval(80, 80), Interval(96, 98)],
        # Job 30
        [Interval(16, 16), Interval(58, 70), Interval(17, 23), Interval(55, 61), Interval(92, 106),
         Interval(4, 4), Interval(9, 9), Interval(55, 63), Interval(29, 29), Interval(23, 29),
         Interval(22, 24), Interval(10, 10), Interval(14, 16), Interval(19, 23), Interval(19, 19),
         Interval(97, 99), Interval(75, 79), Interval(78, 82), Interval(65, 87), Interval(25, 25)],
        # Job 31
        [Interval(46, 56), Interval(33, 33), Interval(12, 16), Interval(57, 69), Interval(41, 51),
         Interval(6, 6), Interval(51, 55), Interval(24, 30), Interval(87, 111), Interval(84, 90),
         Interval(13, 17), Interval(76, 78), Interval(57, 75), Interval(3, 3), Interval(50, 52),
         Interval(3, 3), Interval(8, 10), Interval(33, 35), Interval(71, 83), Interval(48, 60)],
        # Job 32
        [Interval(57, 77), Interval(84, 112), Interval(55, 59), Interval(67, 81), Interval(47, 47),
         Interval(11, 13), Interval(90, 94), Interval(28, 32), Interval(44, 46), Interval(36, 42),
         Interval(31, 41), Interval(12, 12), Interval(77, 95), Interval(78, 98), Interval(15, 15),
         Interval(81, 97), Interval(82, 110), Interval(68, 70), Interval(43, 43), Interval(62, 82)],
        # Job 33
        [Interval(77, 91), Interval(57, 77), Interval(26, 34), Interval(68, 70), Interval(6, 6),
         Interval(84, 90), Interval(58, 58), Interval(34, 40), Interval(77, 97), Interval(12, 12),
         Interval(84, 96), Interval(36, 40), Interval(43, 51), Interval(86, 112), Interval(7, 9),
         Interval(29, 31), Interval(45, 51), Interval(29, 31), Interval(6, 8), Interval(86, 110)],
        # Job 34
        [Interval(87, 97), Interval(66, 82), Interval(7, 9), Interval(82, 90), Interval(32, 40),
         Interval(75, 81), Interval(6, 6), Interval(2, 2), Interval(40, 44), Interval(14, 14),
         Interval(62, 82), Interval(83, 105), Interval(82, 84), Interval(4, 4), Interval(49, 51),
         Interval(84, 96), Interval(79, 81), Interval(27, 27), Interval(42, 48), Interval(71, 71)],
        # Job 35
        [Interval(71, 85), Interval(39, 43), Interval(16, 18), Interval(80, 92), Interval(80, 86),
         Interval(64, 78), Interval(47, 61), Interval(69, 91), Interval(66, 70), Interval(16, 16),
         Interval(76, 100), Interval(37, 43), Interval(75, 101), Interval(10, 12), Interval(8, 10),
         Interval(51, 57), Interval(3, 3), Interval(21, 27), Interval(71, 91), Interval(18, 18)],
        # Job 36
        [Interval(64, 80), Interval(58, 70), Interval(61, 75), Interval(46, 46), Interval(25, 33),
         Interval(80, 104), Interval(70, 78), Interval(60, 76), Interval(12, 12), Interval(67, 69),
         Interval(75, 99), Interval(80, 80), Interval(72, 90), Interval(44, 44), Interval(72, 80),
         Interval(9, 9), Interval(25, 27), Interval(27, 35), Interval(33, 41), Interval(73, 91)],
        # Job 37
        [Interval(42, 46), Interval(50, 56), Interval(74, 98), Interval(66, 68), Interval(4, 4),
         Interval(13, 15), Interval(44, 50), Interval(19, 19), Interval(45, 55), Interval(67, 69),
         Interval(63, 67), Interval(22, 22), Interval(92, 102), Interval(11, 11), Interval(33, 35),
         Interval(75, 75), Interval(10, 12), Interval(13, 15), Interval(76, 80), Interval(80, 80)],
        # Job 38
        [Interval(55, 71), Interval(42, 54), Interval(63, 63), Interval(42, 44), Interval(8, 10),
         Interval(73, 91), Interval(12, 14), Interval(46, 50), Interval(3, 3), Interval(65, 73),
         Interval(47, 47), Interval(3, 3), Interval(51, 61), Interval(29, 35), Interval(36, 46),
         Interval(9, 11), Interval(41, 55), Interval(15, 17), Interval(92, 104), Interval(57, 61)],
        # Job 39
        [Interval(37, 47), Interval(79, 103), Interval(10, 12), Interval(32, 42), Interval(89, 105),
         Interval(34, 46), Interval(34, 36), Interval(95, 97), Interval(95, 95), Interval(24, 28),
         Interval(79, 81), Interval(55, 67), Interval(64, 74), Interval(16, 16), Interval(56, 62),
         Interval(57, 73), Interval(3, 3), Interval(5, 5), Interval(85, 85), Interval(43, 53)],
        # Job 40
        [Interval(3, 3), Interval(20, 24), Interval(12, 12), Interval(62, 64), Interval(20, 20),
         Interval(83, 83), Interval(56, 56), Interval(65, 87), Interval(46, 48), Interval(9, 9),
         Interval(42, 42), Interval(31, 39), Interval(23, 23), Interval(10, 12), Interval(17, 23),
         Interval(26, 30), Interval(49, 53), Interval(71, 85), Interval(32, 38), Interval(51, 63)],
        # Job 41
        [Interval(13, 13), Interval(74, 78), Interval(20, 20), Interval(65, 69), Interval(6, 6),
         Interval(19, 19), Interval(68, 80), Interval(1, 1), Interval(13, 13), Interval(46, 50),
         Interval(38, 50), Interval(11, 13), Interval(41, 51), Interval(87, 101), Interval(25, 27),
         Interval(38, 48), Interval(34, 40), Interval(71, 75), Interval(46, 50), Interval(27, 31)],
        # Job 42
        [Interval(22, 28), Interval(45, 53), Interval(46, 56), Interval(31, 41), Interval(47, 53),
         Interval(14, 16), Interval(59, 73), Interval(15, 19), Interval(41, 45), Interval(47, 59),
         Interval(3, 3), Interval(43, 51), Interval(11, 13), Interval(74, 74), Interval(8, 8),
         Interval(57, 73), Interval(27, 31), Interval(7, 9), Interval(18, 18), Interval(36, 36)],
        # Job 43
        [Interval(32, 34), Interval(13, 15), Interval(83, 107), Interval(43, 53), Interval(64, 72),
         Interval(23, 25), Interval(78, 96), Interval(40, 46), Interval(9, 11), Interval(35, 45),
         Interval(30, 34), Interval(42, 44), Interval(66, 66), Interval(39, 45), Interval(29, 29),
         Interval(18, 22), Interval(25, 31), Interval(38, 40), Interval(73, 81), Interval(36, 46)],
        # Job 44
        [Interval(70, 76), Interval(58, 74), Interval(63, 71), Interval(59, 75), Interval(63, 81),
         Interval(63, 63), Interval(69, 93), Interval(80, 88), Interval(7, 7), Interval(48, 56),
         Interval(9, 9), Interval(8, 10), Interval(33, 37), Interval(10, 12), Interval(35, 39),
         Interval(48, 62), Interval(89, 103), Interval(82, 86), Interval(85, 109), Interval(28, 36)],
        # Job 45
        [Interval(58, 76), Interval(26, 30), Interval(79, 91), Interval(53, 63), Interval(48, 54),
         Interval(36, 46), Interval(59, 69), Interval(39, 41), Interval(52, 56), Interval(28, 34),
         Interval(44, 50), Interval(15, 17), Interval(43, 43), Interval(55, 63), Interval(57, 77),
         Interval(29, 37), Interval(14, 16), Interval(81, 101), Interval(9, 9), Interval(48, 56)],
        # Job 46
        [Interval(28, 30), Interval(60, 64), Interval(23, 23), Interval(52, 68), Interval(62, 74),
         Interval(18, 22), Interval(18, 22), Interval(32, 32), Interval(48, 52), Interval(9, 9),
         Interval(20, 24), Interval(56, 56), Interval(85, 103), Interval(26, 28), Interval(36, 46),
         Interval(68, 86), Interval(17, 21), Interval(47, 61), Interval(87, 87), Interval(86, 106)],
        # Job 47
        [Interval(67, 71), Interval(63, 69), Interval(78, 94), Interval(41, 45), Interval(52, 52),
         Interval(36, 42), Interval(24, 30), Interval(60, 66), Interval(5, 5), Interval(69, 71),
         Interval(2, 2), Interval(10, 10), Interval(2, 2), Interval(12, 14), Interval(43, 45),
         Interval(86, 98), Interval(62, 80), Interval(14, 14), Interval(4, 4), Interval(33, 37)],
        # Job 48
        [Interval(57, 73), Interval(75, 81), Interval(24, 28), Interval(25, 33), Interval(70, 82),
         Interval(19, 21), Interval(63, 65), Interval(33, 33), Interval(88, 94), Interval(46, 48),
         Interval(85, 93), Interval(49, 49), Interval(43, 57), Interval(40, 42), Interval(54, 68),
         Interval(21, 23), Interval(86, 112), Interval(31, 33), Interval(12, 12), Interval(43, 43)],
        # Job 49
        [Interval(71, 85), Interval(72, 96), Interval(78, 84), Interval(54, 70), Interval(41, 43),
         Interval(11, 11), Interval(61, 69), Interval(77, 89), Interval(74, 76), Interval(11, 13),
         Interval(43, 49), Interval(46, 46), Interval(56, 66), Interval(92, 104), Interval(42, 56),
         Interval(30, 40), Interval(35, 43), Interval(23, 31), Interval(21, 25), Interval(52, 60)],
        # Job 50
        [Interval(47, 51), Interval(36, 38), Interval(32, 42), Interval(81, 109), Interval(82, 100),
         Interval(68, 68), Interval(7, 9), Interval(18, 18), Interval(48, 60), Interval(20, 26),
         Interval(93, 95), Interval(59, 65), Interval(64, 68), Interval(3, 3), Interval(19, 23),
         Interval(60, 64), Interval(70, 74), Interval(28, 28), Interval(85, 97), Interval(75, 91)],
        # Job 51
        [Interval(19, 23), Interval(70, 76), Interval(45, 45), Interval(20, 24), Interval(79, 99),
         Interval(4, 4), Interval(4, 4), Interval(1, 1), Interval(71, 71), Interval(38, 50),
         Interval(30, 40), Interval(95, 103), Interval(49, 49), Interval(18, 20), Interval(22, 28),
         Interval(76, 78), Interval(13, 15), Interval(87, 93), Interval(18, 20), Interval(78, 92)],
        # Job 52
        [Interval(76, 76), Interval(7, 9), Interval(68, 68), Interval(13, 13), Interval(85, 111),
         Interval(76, 100), Interval(46, 54), Interval(16, 18), Interval(68, 78), Interval(17, 19),
         Interval(20, 24), Interval(60, 66), Interval(73, 73), Interval(48, 64), Interval(56, 66),
         Interval(22, 28), Interval(68, 74), Interval(14, 16), Interval(49, 51), Interval(21, 25)],
        # Job 53
        [Interval(1, 1), Interval(89, 109), Interval(60, 68), Interval(51, 51), Interval(77, 77),
         Interval(11, 13), Interval(23, 29), Interval(24, 30), Interval(28, 34), Interval(23, 23),
         Interval(84, 96), Interval(59, 71), Interval(16, 16), Interval(80, 102), Interval(42, 52),
         Interval(33, 37), Interval(39, 39), Interval(8, 10), Interval(59, 69), Interval(81, 101)],
        # Job 54
        [Interval(5, 5), Interval(41, 43), Interval(3, 3), Interval(15, 15), Interval(71, 77),
         Interval(39, 51), Interval(33, 35), Interval(47, 51), Interval(40, 50), Interval(54, 54),
         Interval(82, 90), Interval(27, 29), Interval(6, 6), Interval(73, 81), Interval(67, 85),
         Interval(55, 63), Interval(60, 66), Interval(21, 21), Interval(48, 52), Interval(84, 102)],
        # Job 55
        [Interval(25, 27), Interval(85, 103), Interval(29, 37), Interval(20, 20), Interval(27, 27),
         Interval(74, 92), Interval(54, 56), Interval(89, 97), Interval(39, 43), Interval(57, 67),
         Interval(6, 6), Interval(29, 37), Interval(42, 52), Interval(75, 93), Interval(22, 28),
         Interval(5, 5), Interval(7, 9), Interval(14, 14), Interval(23, 29), Interval(83, 109)],
        # Job 56
        [Interval(87, 93), Interval(99, 99), Interval(17, 21), Interval(66, 82), Interval(14, 16),
         Interval(82, 82), Interval(52, 58), Interval(90, 92), Interval(51, 55), Interval(8, 8),
         Interval(18, 20), Interval(9, 9), Interval(54, 66), Interval(10, 10), Interval(5, 5),
         Interval(37, 37), Interval(86, 104), Interval(17, 21), Interval(55, 71), Interval(57, 57)],
        # Job 57
        [Interval(38, 42), Interval(19, 19), Interval(3, 3), Interval(43, 45), Interval(30, 30),
         Interval(80, 88), Interval(49, 49), Interval(19, 25), Interval(15, 15), Interval(84, 102),
         Interval(7, 9), Interval(86, 94), Interval(45, 51), Interval(83, 91), Interval(34, 34),
         Interval(36, 48), Interval(70, 86), Interval(75, 77), Interval(71, 93), Interval(6, 8)],
        # Job 58
        [Interval(46, 48), Interval(4, 4), Interval(33, 37), Interval(15, 15), Interval(29, 35),
         Interval(56, 72), Interval(75, 75), Interval(61, 65), Interval(91, 103), Interval(48, 54),
         Interval(59, 71), Interval(35, 47), Interval(41, 51), Interval(61, 67), Interval(20, 22),
         Interval(46, 54), Interval(3, 3), Interval(37, 43), Interval(30, 40), Interval(65, 65)],
        # Job 59
        [Interval(88, 90), Interval(20, 26), Interval(9, 9), Interval(6, 8), Interval(7, 9),
         Interval(72, 82), Interval(92, 96), Interval(72, 92), Interval(30, 34), Interval(84, 102),
         Interval(4, 4), Interval(65, 81), Interval(89, 99), Interval(59, 73), Interval(81, 83),
         Interval(27, 29), Interval(37, 39), Interval(43, 45), Interval(24, 28), Interval(5, 5)],
        # Job 60
        [Interval(26, 34), Interval(59, 77), Interval(64, 74), Interval(50, 64), Interval(80, 84),
         Interval(66, 84), Interval(9, 11), Interval(33, 41), Interval(32, 38), Interval(91, 99),
         Interval(76, 96), Interval(22, 28), Interval(54, 70), Interval(81, 81), Interval(72, 78),
         Interval(57, 61), Interval(89, 103), Interval(73, 95), Interval(81, 81), Interval(98, 100)],
        # Job 61
        [Interval(91, 91), Interval(56, 66), Interval(43, 45), Interval(11, 11), Interval(20, 22),
         Interval(12, 16), Interval(55, 69), Interval(15, 17), Interval(36, 36), Interval(45, 57),
         Interval(51, 61), Interval(69, 85), Interval(77, 81), Interval(48, 58), Interval(37, 37),
         Interval(47, 49), Interval(28, 28), Interval(55, 67), Interval(52, 52), Interval(65, 79)],
        # Job 62
        [Interval(51, 51), Interval(17, 19), Interval(9, 9), Interval(6, 6), Interval(48, 58),
         Interval(68, 76), Interval(47, 49), Interval(67, 77), Interval(63, 65), Interval(46, 52),
         Interval(56, 58), Interval(38, 46), Interval(72, 88), Interval(92, 92), Interval(8, 10),
         Interval(6, 6), Interval(81, 87), Interval(57, 59), Interval(48, 52), Interval(78, 80)],
        # Job 63
        [Interval(66, 68), Interval(15, 17), Interval(5, 5), Interval(26, 34), Interval(11, 13),
         Interval(10, 12), Interval(24, 28), Interval(65, 83), Interval(35, 37), Interval(20, 26),
         Interval(48, 52), Interval(12, 14), Interval(53, 65), Interval(35, 39), Interval(74, 84),
         Interval(59, 77), Interval(18, 22), Interval(63, 69), Interval(81, 93), Interval(48, 56)],
        # Job 64
        [Interval(45, 59), Interval(4, 4), Interval(6, 6), Interval(27, 27), Interval(31, 39),
         Interval(42, 50), Interval(78, 86), Interval(2, 2), Interval(55, 63), Interval(61, 81),
         Interval(76, 92), Interval(15, 15), Interval(37, 43), Interval(67, 87), Interval(69, 87),
         Interval(2, 2), Interval(59, 65), Interval(65, 79), Interval(69, 89), Interval(63, 79)],
        # Job 65
        [Interval(66, 86), Interval(23, 27), Interval(39, 41), Interval(15, 15), Interval(81, 85),
         Interval(39, 39), Interval(60, 72), Interval(79, 79), Interval(76, 80), Interval(29, 31),
         Interval(17, 19), Interval(29, 29), Interval(54, 58), Interval(25, 29), Interval(39, 49),
         Interval(71, 85), Interval(1, 1), Interval(68, 70), Interval(30, 38), Interval(18, 18)],
        # Job 66
        [Interval(49, 53), Interval(86, 92), Interval(97, 101), Interval(53, 55), Interval(87, 111),
         Interval(67, 85), Interval(11, 11), Interval(92, 92), Interval(4, 4), Interval(23, 27),
         Interval(65, 67), Interval(36, 46), Interval(82, 102), Interval(36, 36), Interval(54, 56),
         Interval(30, 34), Interval(43, 51), Interval(1, 1), Interval(45, 45), Interval(78, 104)],
        # Job 67
        [Interval(71, 91), Interval(83, 91), Interval(28, 28), Interval(15, 15), Interval(41, 45),
         Interval(4, 4), Interval(67, 67), Interval(12, 12), Interval(83, 107), Interval(4, 4),
         Interval(61, 71), Interval(57, 61), Interval(30, 38), Interval(8, 10), Interval(22, 28),
         Interval(2, 2), Interval(6, 6), Interval(76, 98), Interval(79, 91), Interval(35, 35)],
        # Job 68
        [Interval(6, 6), Interval(10, 12), Interval(50, 50), Interval(78, 90), Interval(53, 71),
         Interval(83, 105), Interval(2, 2), Interval(88, 106), Interval(52, 52), Interval(4, 4),
         Interval(83, 101), Interval(43, 45), Interval(44, 58), Interval(23, 23), Interval(75, 85),
         Interval(32, 38), Interval(16, 16), Interval(45, 47), Interval(5, 5), Interval(57, 77)],
        # Job 69
        [Interval(62, 62), Interval(84, 110), Interval(45, 59), Interval(91, 107), Interval(76, 90),
         Interval(50, 56), Interval(51, 63), Interval(8, 8), Interval(67, 71), Interval(33, 41),
         Interval(65, 79), Interval(95, 95), Interval(53, 69), Interval(70, 82), Interval(64, 80),
         Interval(49, 59), Interval(15, 15), Interval(78, 104), Interval(50, 50), Interval(31, 41)],
        # Job 70
        [Interval(38, 48), Interval(30, 36), Interval(21, 27), Interval(81, 87), Interval(29, 29),
         Interval(32, 32), Interval(27, 33), Interval(40, 44), Interval(68, 90), Interval(57, 59),
         Interval(43, 49), Interval(7, 7), Interval(88, 90), Interval(71, 71), Interval(82, 100),
         Interval(9, 9), Interval(60, 80), Interval(38, 42), Interval(32, 34), Interval(20, 24)],
        # Job 71
        [Interval(30, 32), Interval(23, 23), Interval(32, 40), Interval(33, 41), Interval(77, 83),
         Interval(6, 6), Interval(49, 65), Interval(82, 90), Interval(48, 56), Interval(1, 1),
         Interval(94, 96), Interval(65, 71), Interval(76, 98), Interval(16, 20), Interval(54, 58),
         Interval(24, 32), Interval(60, 72), Interval(77, 99), Interval(40, 50), Interval(18, 22)],
        # Job 72
        [Interval(59, 77), Interval(13, 15), Interval(38, 48), Interval(81, 99), Interval(38, 50),
         Interval(21, 21), Interval(26, 30), Interval(97, 97), Interval(97, 99), Interval(42, 54),
         Interval(88, 102), Interval(81, 87), Interval(63, 77), Interval(33, 43), Interval(82, 102),
         Interval(56, 56), Interval(47, 63), Interval(50, 56), Interval(15, 15), Interval(19, 23)],
        # Job 73
        [Interval(87, 95), Interval(54, 58), Interval(94, 100), Interval(43, 49), Interval(17, 19),
         Interval(61, 67), Interval(83, 105), Interval(98, 100), Interval(69, 93), Interval(57, 67),
         Interval(50, 62), Interval(46, 60), Interval(96, 100), Interval(28, 36), Interval(50, 52),
         Interval(23, 25), Interval(24, 28), Interval(79, 83), Interval(21, 27), Interval(24, 28)],
        # Job 74
        [Interval(95, 103), Interval(43, 49), Interval(21, 23), Interval(22, 28), Interval(11, 13),
         Interval(24, 32), Interval(26, 32), Interval(83, 91), Interval(32, 40), Interval(36, 40),
         Interval(37, 47), Interval(31, 39), Interval(26, 34), Interval(49, 65), Interval(83, 87),
         Interval(91, 103), Interval(2, 2), Interval(45, 53), Interval(73, 93), Interval(25, 31)],
        # Job 75
        [Interval(12, 14), Interval(82, 104), Interval(52, 66), Interval(3, 3), Interval(50, 52),
         Interval(74, 74), Interval(82, 86), Interval(71, 95), Interval(67, 81), Interval(88, 90),
         Interval(62, 78), Interval(43, 47), Interval(54, 64), Interval(48, 60), Interval(1, 1),
         Interval(54, 66), Interval(69, 87), Interval(54, 64), Interval(43, 49), Interval(88, 94)],
        # Job 76
        [Interval(45, 49), Interval(35, 35), Interval(22, 28), Interval(46, 62), Interval(48, 52),
         Interval(31, 31), Interval(65, 79), Interval(74, 94), Interval(61, 77), Interval(88, 92),
         Interval(49, 61), Interval(55, 73), Interval(85, 93), Interval(9, 11), Interval(51, 51),
         Interval(79, 83), Interval(55, 61), Interval(42, 52), Interval(32, 40), Interval(12, 14)],
        # Job 77
        [Interval(80, 84), Interval(82, 86), Interval(23, 27), Interval(15, 17), Interval(78, 104),
         Interval(71, 85), Interval(71, 85), Interval(41, 55), Interval(69, 75), Interval(42, 52),
         Interval(58, 62), Interval(34, 38), Interval(24, 30), Interval(40, 44), Interval(34, 34),
         Interval(30, 40), Interval(79, 91), Interval(29, 37), Interval(62, 78), Interval(49, 65)],
        # Job 78
        [Interval(4, 4), Interval(87, 107), Interval(55, 63), Interval(91, 101), Interval(29, 33),
         Interval(62, 82), Interval(45, 47), Interval(47, 47), Interval(51, 61), Interval(63, 65),
         Interval(51, 51), Interval(67, 87), Interval(71, 75), Interval(59, 75), Interval(69, 93),
         Interval(2, 2), Interval(67, 89), Interval(21, 23), Interval(45, 51), Interval(8, 10)],
        # Job 79
        [Interval(83, 97), Interval(19, 23), Interval(71, 91), Interval(42, 42), Interval(55, 71),
         Interval(92, 104), Interval(82, 86), Interval(26, 32), Interval(46, 62), Interval(84, 98),
         Interval(74, 76), Interval(77, 103), Interval(1, 1), Interval(85, 93), Interval(6, 6),
         Interval(42, 42), Interval(2, 2), Interval(11, 13), Interval(31, 35), Interval(63, 69)],
        # Job 80
        [Interval(69, 91), Interval(77, 99), Interval(54, 60), Interval(30, 30), Interval(93, 95),
         Interval(93, 97), Interval(58, 58), Interval(78, 100), Interval(46, 48), Interval(16, 18),
         Interval(23, 25), Interval(87, 109), Interval(53, 71), Interval(79, 103), Interval(48, 50),
         Interval(59, 71), Interval(32, 36), Interval(82, 100), Interval(80, 108), Interval(13, 13)],
        # Job 81
        [Interval(38, 44), Interval(82, 106), Interval(9, 9), Interval(95, 95), Interval(72, 82),
         Interval(78, 96), Interval(81, 99), Interval(86, 86), Interval(18, 24), Interval(12, 14),
         Interval(56, 64), Interval(33, 39), Interval(20, 24), Interval(64, 78), Interval(16, 20),
         Interval(14, 16), Interval(32, 32), Interval(14, 14), Interval(10, 12), Interval(50, 58)],
        # Job 82
        [Interval(45, 49), Interval(16, 20), Interval(93, 93), Interval(51, 63), Interval(69, 79),
         Interval(2, 2), Interval(58, 58), Interval(65, 73), Interval(10, 10), Interval(38, 44),
         Interval(72, 88), Interval(3, 3), Interval(68, 76), Interval(54, 66), Interval(30, 38),
         Interval(56, 64), Interval(32, 36), Interval(32, 32), Interval(29, 37), Interval(85, 93)],
        # Job 83
        [Interval(83, 93), Interval(28, 34), Interval(23, 31), Interval(81, 95), Interval(47, 49),
         Interval(23, 31), Interval(5, 5), Interval(42, 56), Interval(7, 9), Interval(58, 76),
         Interval(23, 23), Interval(43, 53), Interval(22, 26), Interval(77, 101), Interval(66, 80),
         Interval(72, 80), Interval(77, 97), Interval(55, 55), Interval(17, 17), Interval(57, 69)],
        # Job 84
        [Interval(9, 11), Interval(81, 85), Interval(76, 98), Interval(44, 48), Interval(28, 34),
         Interval(77, 81), Interval(24, 32), Interval(13, 17), Interval(29, 33), Interval(77, 89),
         Interval(38, 46), Interval(34, 46), Interval(39, 47), Interval(51, 69), Interval(5, 5),
         Interval(56, 68), Interval(45, 51), Interval(26, 30), Interval(12, 14), Interval(69, 79)],
        # Job 85
        [Interval(70, 76), Interval(69, 85), Interval(91, 97), Interval(14, 18), Interval(78, 100),
         Interval(45, 51), Interval(89, 97), Interval(22, 28), Interval(75, 77), Interval(4, 4),
         Interval(70, 70), Interval(62, 70), Interval(29, 33), Interval(58, 68), Interval(62, 78),
         Interval(87, 95), Interval(36, 42), Interval(62, 72), Interval(3, 3), Interval(5, 5)],
        # Job 86
        [Interval(61, 63), Interval(93, 93), Interval(33, 43), Interval(58, 72), Interval(75, 87),
         Interval(43, 47), Interval(53, 59), Interval(63, 75), Interval(73, 81), Interval(4, 4),
         Interval(8, 8), Interval(60, 72), Interval(16, 16), Interval(6, 6), Interval(74, 78),
         Interval(78, 80), Interval(21, 27), Interval(82, 110), Interval(71, 89), Interval(38, 38)],
        # Job 87
        [Interval(95, 95), Interval(25, 27), Interval(78, 90), Interval(87, 105), Interval(90, 92),
         Interval(63, 63), Interval(42, 54), Interval(39, 39), Interval(25, 31), Interval(48, 48),
         Interval(78, 88), Interval(68, 80), Interval(84, 84), Interval(2, 2), Interval(70, 82),
         Interval(45, 45), Interval(87, 109), Interval(66, 74), Interval(82, 94), Interval(64, 72)],
        # Job 88
        [Interval(10, 10), Interval(86, 106), Interval(66, 66), Interval(77, 81), Interval(83, 105),
         Interval(8, 8), Interval(17, 21), Interval(9, 9), Interval(8, 8), Interval(64, 84),
         Interval(1, 1), Interval(28, 32), Interval(83, 103), Interval(84, 98), Interval(11, 11),
         Interval(55, 59), Interval(73, 79), Interval(75, 75), Interval(86, 88), Interval(37, 43)],
        # Job 89
        [Interval(15, 19), Interval(84, 112), Interval(75, 75), Interval(50, 64), Interval(1, 1),
         Interval(52, 70), Interval(70, 74), Interval(74, 90), Interval(56, 64), Interval(81, 93),
         Interval(90, 98), Interval(43, 55), Interval(62, 66), Interval(76, 90), Interval(39, 45),
         Interval(61, 65), Interval(28, 30), Interval(62, 72), Interval(92, 106), Interval(74, 78)],
        # Job 90
        [Interval(6, 6), Interval(87, 97), Interval(9, 9), Interval(60, 60), Interval(23, 25),
         Interval(20, 20), Interval(69, 87), Interval(46, 46), Interval(15, 17), Interval(48, 56),
         Interval(68, 88), Interval(26, 34), Interval(3, 3), Interval(57, 69), Interval(13, 13),
         Interval(67, 69), Interval(67, 79), Interval(54, 56), Interval(82, 106), Interval(64, 66)],
        # Job 91
        [Interval(18, 24), Interval(81, 105), Interval(17, 19), Interval(29, 39), Interval(78, 86),
         Interval(50, 52), Interval(49, 49), Interval(61, 79), Interval(48, 54), Interval(55, 61),
         Interval(55, 59), Interval(78, 82), Interval(44, 46), Interval(61, 77), Interval(47, 53),
         Interval(91, 97), Interval(9, 11), Interval(2, 2), Interval(70, 72), Interval(36, 44)],
        # Job 92
        [Interval(15, 19), Interval(75, 81), Interval(49, 63), Interval(72, 80), Interval(34, 38),
         Interval(24, 28), Interval(80, 94), Interval(65, 83), Interval(30, 40), Interval(34, 44),
         Interval(31, 33), Interval(76, 88), Interval(73, 95), Interval(81, 109), Interval(40, 42),
         Interval(42, 44), Interval(43, 57), Interval(37, 45), Interval(42, 50), Interval(47, 59)],
        # Job 93
        [Interval(59, 75), Interval(61, 63), Interval(70, 72), Interval(12, 12), Interval(22, 24),
         Interval(72, 90), Interval(61, 69), Interval(37, 43), Interval(51, 67), Interval(59, 73),
         Interval(74, 82), Interval(19, 23), Interval(47, 49), Interval(65, 73), Interval(4, 4),
         Interval(85, 105), Interval(62, 74), Interval(36, 36), Interval(18, 20), Interval(46, 56)],
        # Job 94
        [Interval(96, 98), Interval(82, 86), Interval(82, 92), Interval(93, 97), Interval(24, 28),
         Interval(13, 15), Interval(71, 73), Interval(24, 24), Interval(86, 86), Interval(6, 6),
         Interval(42, 48), Interval(26, 32), Interval(17, 21), Interval(91, 93), Interval(79, 81),
         Interval(10, 12), Interval(48, 56), Interval(70, 84), Interval(80, 98), Interval(64, 86)],
        # Job 95
        [Interval(17, 23), Interval(84, 86), Interval(44, 52), Interval(67, 73), Interval(30, 32),
         Interval(12, 16), Interval(79, 83), Interval(21, 21), Interval(55, 59), Interval(92, 104),
         Interval(9, 9), Interval(23, 23), Interval(14, 18), Interval(45, 47), Interval(38, 50),
         Interval(16, 16), Interval(37, 45), Interval(17, 17), Interval(79, 81), Interval(12, 14)],
        # Job 96
        [Interval(61, 75), Interval(30, 30), Interval(79, 93), Interval(49, 59), Interval(69, 91),
         Interval(76, 80), Interval(16, 16), Interval(85, 93), Interval(68, 74), Interval(94, 100),
         Interval(73, 87), Interval(66, 72), Interval(34, 42), Interval(77, 77), Interval(3, 3),
         Interval(28, 32), Interval(52, 70), Interval(79, 85), Interval(85, 91), Interval(82, 88)],
        # Job 97
        [Interval(89, 105), Interval(40, 52), Interval(48, 50), Interval(66, 88), Interval(25, 29),
         Interval(84, 108), Interval(74, 90), Interval(62, 64), Interval(20, 22), Interval(81, 85),
         Interval(45, 57), Interval(72, 82), Interval(77, 83), Interval(83, 93), Interval(6, 8),
         Interval(95, 99), Interval(65, 81), Interval(52, 64), Interval(35, 37), Interval(2, 2)],
        # Job 98
        [Interval(40, 48), Interval(78, 104), Interval(2, 2), Interval(80, 108), Interval(71, 91),
         Interval(46, 56), Interval(81, 95), Interval(37, 49), Interval(20, 20), Interval(73, 85),
         Interval(45, 49), Interval(60, 64), Interval(58, 74), Interval(40, 42), Interval(21, 27),
         Interval(57, 63), Interval(12, 12), Interval(3, 3), Interval(73, 81), Interval(73, 89)],
        # Job 99
        [Interval(38, 48), Interval(61, 69), Interval(67, 69), Interval(57, 65), Interval(61, 77),
         Interval(24, 28), Interval(45, 49), Interval(84, 90), Interval(47, 59), Interval(80, 82),
         Interval(58, 60), Interval(75, 87), Interval(72, 88), Interval(56, 70), Interval(28, 34),
         Interval(18, 24), Interval(46, 46), Interval(3, 3), Interval(73, 91), Interval(57, 71)],
    ],
    'name': 'INT__TAI100_20_03.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai100_20_03_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI100_20_03.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI100_20_03.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI100_20_03_F_15_01_INTERVAL_DATA
