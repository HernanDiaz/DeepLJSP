"""
Problema INT__TAI100_20_09.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI100_20_09_F_15_01_INTERVAL_DATA = {
    'num_jobs': 100,
    'num_machines': 20,
    'problem_id': 'int__tai100_20_09.F.15_01_interval',
    'sequences': [
        [16, 18, 5, 13, 12, 9, 10, 0, 17, 4, 2, 11, 8, 6, 7, 15, 3, 14, 19, 1],
        [6, 9, 17, 10, 1, 7, 11, 13, 0, 5, 14, 4, 8, 3, 12, 18, 19, 2, 15, 16],
        [3, 13, 8, 18, 9, 2, 15, 16, 4, 1, 14, 10, 12, 6, 17, 19, 0, 7, 5, 11],
        [10, 4, 13, 18, 19, 12, 9, 17, 3, 7, 8, 6, 14, 2, 11, 1, 15, 16, 0, 5],
        [3, 19, 9, 4, 18, 15, 2, 10, 16, 17, 0, 6, 1, 5, 11, 7, 8, 12, 14, 13],
        [1, 7, 13, 16, 17, 5, 8, 4, 12, 19, 6, 3, 18, 0, 11, 14, 2, 10, 15, 9],
        [10, 6, 14, 19, 16, 4, 12, 17, 3, 8, 1, 15, 13, 18, 9, 2, 7, 5, 11, 0],
        [1, 14, 13, 12, 19, 7, 15, 16, 17, 0, 10, 11, 6, 2, 8, 4, 18, 3, 9, 5],
        [9, 5, 11, 16, 3, 18, 8, 7, 17, 4, 10, 2, 19, 6, 1, 0, 13, 12, 15, 14],
        [10, 5, 6, 12, 1, 4, 7, 11, 13, 19, 2, 3, 17, 15, 14, 8, 9, 18, 16, 0],
        [18, 4, 16, 2, 19, 8, 12, 0, 3, 10, 1, 9, 13, 17, 15, 6, 11, 7, 5, 14],
        [15, 11, 8, 17, 12, 2, 0, 5, 3, 19, 16, 14, 9, 10, 6, 1, 7, 4, 13, 18],
        [19, 8, 13, 12, 1, 5, 14, 15, 16, 3, 0, 4, 10, 2, 18, 11, 17, 9, 6, 7],
        [4, 6, 9, 15, 1, 12, 0, 14, 10, 18, 17, 13, 2, 8, 16, 3, 11, 7, 5, 19],
        [18, 19, 13, 8, 14, 17, 0, 9, 10, 16, 2, 5, 4, 15, 7, 3, 11, 12, 1, 6],
        [5, 16, 1, 18, 0, 13, 6, 12, 4, 15, 9, 14, 3, 17, 8, 10, 19, 11, 7, 2],
        [14, 17, 19, 5, 10, 1, 4, 2, 11, 6, 7, 8, 15, 12, 0, 13, 3, 9, 16, 18],
        [1, 5, 6, 17, 12, 8, 19, 14, 9, 4, 11, 13, 15, 16, 10, 7, 18, 3, 0, 2],
        [6, 9, 4, 16, 3, 15, 11, 5, 10, 7, 2, 0, 17, 8, 18, 13, 1, 19, 12, 14],
        [10, 12, 3, 6, 14, 2, 17, 11, 5, 9, 8, 7, 15, 4, 18, 0, 19, 1, 16, 13],
        [9, 11, 15, 2, 17, 10, 4, 14, 18, 6, 8, 3, 16, 7, 13, 1, 19, 0, 12, 5],
        [3, 17, 19, 8, 12, 11, 1, 6, 14, 7, 0, 18, 2, 15, 10, 4, 16, 9, 13, 5],
        [8, 15, 18, 10, 13, 7, 3, 16, 0, 14, 1, 2, 4, 17, 11, 5, 12, 9, 19, 6],
        [11, 0, 6, 1, 7, 9, 10, 14, 12, 15, 13, 8, 19, 5, 2, 4, 18, 17, 3, 16],
        [10, 2, 13, 11, 9, 4, 3, 5, 18, 19, 6, 1, 15, 8, 17, 0, 12, 16, 14, 7],
        [18, 1, 9, 3, 12, 6, 10, 13, 17, 5, 0, 4, 11, 2, 15, 16, 7, 19, 8, 14],
        [12, 16, 2, 8, 9, 19, 6, 0, 3, 7, 14, 10, 1, 15, 5, 11, 17, 18, 13, 4],
        [1, 4, 8, 15, 2, 14, 6, 18, 13, 12, 10, 16, 0, 9, 7, 3, 17, 19, 5, 11],
        [12, 16, 17, 1, 4, 11, 0, 15, 9, 3, 8, 5, 13, 10, 2, 19, 6, 18, 14, 7],
        [6, 10, 2, 18, 5, 3, 13, 11, 4, 7, 17, 12, 19, 8, 9, 0, 1, 16, 14, 15],
        [17, 8, 16, 4, 14, 11, 13, 7, 12, 3, 10, 1, 9, 15, 2, 5, 6, 0, 19, 18],
        [3, 5, 4, 1, 15, 16, 17, 12, 7, 14, 11, 13, 18, 10, 19, 6, 0, 9, 8, 2],
        [11, 3, 17, 16, 10, 1, 14, 18, 0, 4, 13, 5, 12, 8, 7, 6, 2, 15, 9, 19],
        [11, 3, 8, 9, 2, 15, 0, 12, 7, 14, 13, 4, 10, 17, 6, 16, 18, 1, 5, 19],
        [6, 15, 14, 19, 13, 1, 17, 3, 16, 12, 2, 10, 8, 18, 0, 4, 9, 7, 11, 5],
        [1, 14, 16, 8, 2, 3, 6, 18, 12, 5, 10, 7, 19, 4, 13, 0, 17, 11, 15, 9],
        [11, 6, 15, 4, 3, 2, 16, 19, 12, 5, 18, 14, 7, 1, 8, 13, 10, 17, 0, 9],
        [16, 14, 9, 12, 6, 2, 5, 1, 11, 8, 3, 15, 13, 18, 19, 10, 4, 17, 7, 0],
        [0, 7, 6, 13, 16, 5, 15, 12, 14, 4, 8, 3, 9, 19, 2, 18, 1, 10, 11, 17],
        [5, 3, 2, 0, 13, 4, 16, 6, 9, 10, 7, 15, 8, 19, 18, 12, 14, 11, 17, 1],
        [14, 13, 3, 10, 4, 5, 19, 15, 16, 9, 7, 0, 1, 12, 18, 8, 2, 17, 6, 11],
        [14, 19, 5, 11, 7, 3, 9, 1, 4, 2, 15, 6, 12, 17, 0, 13, 18, 8, 10, 16],
        [11, 7, 19, 4, 3, 13, 17, 16, 14, 2, 1, 12, 8, 5, 6, 0, 9, 15, 10, 18],
        [4, 15, 8, 19, 1, 13, 18, 2, 17, 0, 5, 11, 6, 3, 7, 14, 16, 9, 12, 10],
        [12, 8, 13, 11, 1, 17, 19, 14, 0, 4, 7, 6, 10, 9, 3, 15, 5, 18, 16, 2],
        [18, 1, 19, 2, 5, 8, 17, 4, 11, 9, 14, 12, 7, 0, 16, 6, 13, 3, 15, 10],
        [12, 10, 1, 3, 15, 13, 2, 8, 9, 11, 18, 19, 5, 7, 4, 16, 17, 0, 6, 14],
        [7, 6, 12, 10, 8, 14, 9, 1, 16, 5, 0, 11, 3, 4, 19, 17, 13, 18, 15, 2],
        [8, 5, 18, 17, 7, 15, 1, 10, 14, 13, 3, 6, 12, 19, 16, 0, 4, 11, 9, 2],
        [5, 13, 4, 19, 7, 12, 10, 2, 9, 14, 17, 1, 11, 15, 6, 16, 18, 3, 0, 8],
        [7, 11, 13, 19, 9, 6, 2, 4, 14, 12, 18, 17, 3, 0, 16, 10, 15, 8, 5, 1],
        [5, 2, 4, 18, 7, 14, 13, 16, 8, 19, 17, 15, 11, 9, 12, 3, 1, 10, 0, 6],
        [7, 10, 19, 13, 9, 12, 16, 1, 5, 14, 6, 18, 17, 8, 2, 0, 3, 11, 15, 4],
        [0, 1, 3, 18, 14, 10, 5, 9, 4, 6, 12, 11, 15, 8, 7, 13, 17, 19, 16, 2],
        [7, 4, 12, 17, 19, 13, 1, 6, 3, 10, 0, 5, 15, 2, 8, 14, 16, 11, 9, 18],
        [5, 16, 13, 8, 18, 3, 15, 12, 17, 14, 1, 7, 9, 10, 4, 6, 19, 11, 0, 2],
        [17, 7, 14, 12, 3, 9, 5, 8, 0, 10, 11, 1, 6, 16, 4, 15, 13, 19, 2, 18],
        [5, 14, 7, 9, 10, 12, 15, 19, 18, 13, 8, 1, 0, 17, 6, 4, 2, 3, 16, 11],
        [1, 9, 8, 11, 13, 5, 3, 7, 6, 14, 17, 18, 10, 16, 0, 12, 15, 2, 19, 4],
        [19, 16, 10, 17, 14, 13, 4, 3, 5, 6, 2, 8, 11, 15, 9, 1, 7, 0, 18, 12],
        [16, 14, 6, 17, 9, 4, 3, 5, 2, 15, 11, 7, 18, 12, 1, 8, 0, 13, 10, 19],
        [7, 15, 3, 12, 9, 17, 13, 10, 11, 1, 14, 16, 6, 0, 2, 19, 5, 8, 4, 18],
        [19, 10, 4, 9, 13, 5, 16, 12, 2, 1, 17, 7, 3, 15, 18, 11, 14, 8, 0, 6],
        [1, 10, 3, 17, 11, 0, 5, 6, 15, 9, 16, 2, 14, 18, 4, 7, 12, 8, 19, 13],
        [12, 11, 13, 7, 4, 17, 15, 6, 9, 18, 14, 1, 16, 19, 5, 0, 2, 3, 8, 10],
        [19, 0, 16, 10, 13, 18, 4, 14, 17, 11, 15, 7, 2, 8, 9, 1, 12, 6, 5, 3],
        [9, 10, 8, 6, 3, 19, 7, 1, 18, 17, 13, 0, 14, 11, 2, 16, 12, 4, 15, 5],
        [13, 4, 2, 19, 3, 9, 8, 12, 14, 18, 10, 0, 5, 11, 17, 16, 1, 7, 6, 15],
        [0, 16, 7, 3, 13, 18, 17, 10, 15, 14, 12, 6, 9, 4, 19, 1, 5, 8, 2, 11],
        [19, 0, 5, 16, 6, 18, 13, 11, 2, 15, 12, 4, 3, 10, 1, 7, 14, 9, 8, 17],
        [6, 1, 3, 19, 12, 16, 10, 4, 7, 15, 8, 18, 5, 13, 9, 17, 11, 14, 2, 0],
        [4, 9, 8, 14, 5, 0, 10, 1, 2, 6, 7, 19, 18, 12, 17, 15, 11, 3, 13, 16],
        [4, 1, 6, 10, 13, 12, 19, 0, 3, 5, 14, 15, 8, 11, 7, 18, 2, 9, 17, 16],
        [6, 10, 5, 0, 18, 9, 19, 16, 8, 15, 11, 3, 14, 1, 2, 4, 13, 12, 17, 7],
        [9, 0, 13, 16, 8, 15, 4, 1, 6, 14, 19, 18, 17, 2, 12, 10, 3, 5, 7, 11],
        [18, 14, 3, 8, 6, 0, 12, 9, 16, 11, 19, 10, 7, 4, 13, 15, 17, 2, 1, 5],
        [15, 18, 14, 4, 6, 13, 8, 17, 9, 1, 16, 7, 0, 12, 3, 10, 5, 11, 2, 19],
        [1, 10, 0, 12, 9, 6, 13, 8, 2, 11, 19, 14, 4, 3, 15, 7, 18, 17, 16, 5],
        [0, 4, 15, 10, 1, 5, 8, 16, 19, 2, 14, 11, 9, 18, 13, 3, 12, 17, 7, 6],
        [10, 5, 17, 3, 4, 7, 13, 16, 0, 19, 14, 2, 6, 1, 11, 9, 15, 12, 18, 8],
        [5, 6, 18, 13, 11, 9, 10, 14, 2, 7, 1, 0, 17, 4, 8, 15, 19, 16, 12, 3],
        [18, 9, 6, 12, 10, 3, 13, 1, 7, 14, 17, 0, 11, 4, 19, 16, 8, 15, 2, 5],
        [0, 10, 17, 12, 14, 3, 1, 16, 7, 4, 9, 11, 18, 6, 13, 19, 2, 5, 15, 8],
        [14, 12, 3, 11, 10, 16, 1, 2, 0, 5, 17, 8, 6, 19, 7, 15, 9, 4, 13, 18],
        [3, 14, 11, 13, 8, 18, 7, 0, 19, 4, 16, 9, 15, 10, 2, 12, 17, 5, 6, 1],
        [8, 4, 17, 15, 0, 11, 13, 6, 12, 3, 2, 7, 5, 1, 9, 16, 18, 19, 14, 10],
        [3, 18, 19, 7, 15, 2, 14, 12, 10, 5, 0, 17, 13, 8, 4, 9, 11, 16, 6, 1],
        [1, 3, 18, 7, 16, 0, 9, 13, 12, 6, 4, 11, 8, 14, 2, 19, 5, 17, 10, 15],
        [0, 11, 16, 14, 4, 1, 7, 5, 2, 17, 10, 15, 18, 8, 3, 19, 12, 9, 6, 13],
        [16, 18, 11, 3, 17, 5, 4, 19, 15, 13, 7, 0, 14, 1, 8, 6, 12, 2, 9, 10],
        [16, 8, 15, 6, 11, 13, 5, 9, 12, 10, 3, 0, 18, 1, 17, 19, 14, 2, 7, 4],
        [19, 0, 3, 14, 11, 10, 9, 4, 16, 8, 12, 7, 13, 2, 6, 18, 17, 5, 15, 1],
        [12, 16, 8, 0, 5, 4, 10, 13, 2, 19, 14, 18, 11, 15, 6, 3, 1, 17, 9, 7],
        [4, 1, 16, 13, 10, 14, 12, 7, 8, 11, 15, 17, 9, 3, 0, 6, 19, 5, 2, 18],
        [3, 0, 17, 6, 5, 12, 13, 18, 19, 14, 4, 9, 2, 7, 16, 11, 1, 10, 15, 8],
        [2, 19, 9, 14, 3, 1, 0, 16, 6, 7, 15, 17, 11, 13, 18, 12, 4, 5, 8, 10],
        [16, 18, 7, 17, 1, 10, 8, 12, 2, 11, 0, 14, 9, 4, 5, 6, 15, 13, 3, 19],
        [13, 15, 9, 12, 7, 0, 16, 19, 2, 1, 8, 10, 11, 6, 18, 4, 14, 3, 17, 5],
        [9, 5, 14, 7, 3, 4, 19, 16, 17, 12, 6, 1, 11, 13, 8, 10, 15, 2, 0, 18],
        [11, 4, 8, 12, 3, 2, 10, 13, 16, 18, 17, 0, 1, 9, 5, 15, 19, 6, 14, 7],
    ],
    'durations': [
        # Job 0
        [Interval(73, 93), Interval(43, 49), Interval(61, 65), Interval(18, 20), Interval(25, 31),
         Interval(75, 99), Interval(88, 94), Interval(52, 70), Interval(12, 16), Interval(76, 92),
         Interval(8, 10), Interval(87, 95), Interval(21, 27), Interval(27, 29), Interval(54, 66),
         Interval(24, 28), Interval(11, 11), Interval(6, 6), Interval(4, 4), Interval(82, 110)],
        # Job 1
        [Interval(60, 80), Interval(64, 80), Interval(44, 46), Interval(48, 52), Interval(1, 1),
         Interval(46, 46), Interval(60, 74), Interval(43, 43), Interval(73, 77), Interval(43, 45),
         Interval(56, 68), Interval(89, 93), Interval(85, 113), Interval(87, 105), Interval(30, 38),
         Interval(54, 66), Interval(96, 96), Interval(19, 19), Interval(10, 10), Interval(47, 57)],
        # Job 2
        [Interval(83, 105), Interval(42, 42), Interval(74, 90), Interval(35, 43), Interval(32, 34),
         Interval(44, 52), Interval(42, 42), Interval(29, 35), Interval(68, 70), Interval(80, 106),
         Interval(60, 70), Interval(72, 76), Interval(43, 51), Interval(3, 3), Interval(30, 32),
         Interval(52, 58), Interval(73, 89), Interval(89, 93), Interval(71, 71), Interval(58, 74)],
        # Job 3
        [Interval(47, 51), Interval(19, 21), Interval(36, 38), Interval(93, 97), Interval(23, 25),
         Interval(6, 6), Interval(56, 74), Interval(33, 35), Interval(54, 72), Interval(49, 51),
         Interval(11, 13), Interval(55, 73), Interval(52, 60), Interval(29, 33), Interval(34, 40),
         Interval(80, 106), Interval(80, 98), Interval(30, 34), Interval(88, 104), Interval(41, 53)],
        # Job 4
        [Interval(32, 38), Interval(13, 17), Interval(62, 70), Interval(89, 89), Interval(69, 75),
         Interval(40, 54), Interval(55, 61), Interval(29, 39), Interval(54, 68), Interval(49, 51),
         Interval(15, 19), Interval(30, 32), Interval(79, 81), Interval(72, 96), Interval(12, 14),
         Interval(38, 48), Interval(93, 99), Interval(68, 78), Interval(37, 37), Interval(86, 108)],
        # Job 5
        [Interval(50, 62), Interval(63, 65), Interval(14, 16), Interval(68, 88), Interval(32, 38),
         Interval(70, 72), Interval(85, 85), Interval(62, 64), Interval(35, 37), Interval(88, 94),
         Interval(41, 55), Interval(23, 29), Interval(13, 15), Interval(52, 58), Interval(5, 5),
         Interval(57, 67), Interval(56, 58), Interval(90, 98), Interval(49, 57), Interval(6, 6)],
        # Job 6
        [Interval(92, 102), Interval(18, 18), Interval(12, 12), Interval(63, 67), Interval(75, 79),
         Interval(63, 75), Interval(24, 30), Interval(73, 83), Interval(30, 38), Interval(51, 67),
         Interval(2, 2), Interval(21, 23), Interval(67, 87), Interval(47, 55), Interval(6, 6),
         Interval(25, 25), Interval(6, 6), Interval(47, 51), Interval(6, 8), Interval(85, 109)],
        # Job 7
        [Interval(78, 88), Interval(26, 28), Interval(30, 38), Interval(87, 109), Interval(36, 46),
         Interval(43, 43), Interval(21, 23), Interval(4, 4), Interval(43, 47), Interval(17, 21),
         Interval(42, 46), Interval(62, 62), Interval(68, 90), Interval(12, 12), Interval(31, 31),
         Interval(57, 63), Interval(31, 37), Interval(85, 101), Interval(87, 103), Interval(1, 1)],
        # Job 8
        [Interval(34, 44), Interval(73, 75), Interval(80, 108), Interval(66, 70), Interval(77, 77),
         Interval(9, 11), Interval(26, 32), Interval(52, 68), Interval(13, 13), Interval(36, 40),
         Interval(42, 46), Interval(56, 72), Interval(57, 65), Interval(95, 95), Interval(73, 73),
         Interval(35, 39), Interval(36, 38), Interval(2, 2), Interval(12, 14), Interval(30, 34)],
        # Job 9
        [Interval(12, 12), Interval(54, 66), Interval(38, 48), Interval(11, 13), Interval(38, 42),
         Interval(74, 82), Interval(60, 72), Interval(24, 26), Interval(69, 83), Interval(27, 29),
         Interval(60, 76), Interval(59, 59), Interval(10, 10), Interval(69, 85), Interval(75, 99),
         Interval(80, 106), Interval(43, 47), Interval(42, 46), Interval(95, 95), Interval(21, 25)],
        # Job 10
        [Interval(53, 57), Interval(56, 66), Interval(60, 64), Interval(43, 55), Interval(59, 65),
         Interval(91, 97), Interval(2, 2), Interval(87, 99), Interval(33, 37), Interval(74, 90),
         Interval(63, 63), Interval(24, 26), Interval(84, 84), Interval(52, 70), Interval(57, 63),
         Interval(84, 106), Interval(37, 47), Interval(19, 19), Interval(1, 1), Interval(95, 103)],
        # Job 11
        [Interval(13, 13), Interval(54, 56), Interval(30, 32), Interval(33, 35), Interval(61, 79),
         Interval(83, 107), Interval(84, 88), Interval(29, 37), Interval(58, 70), Interval(9, 11),
         Interval(88, 106), Interval(10, 12), Interval(78, 80), Interval(49, 57), Interval(76, 98),
         Interval(5, 5), Interval(96, 98), Interval(78, 78), Interval(73, 91), Interval(54, 62)],
        # Job 12
        [Interval(58, 78), Interval(23, 27), Interval(8, 8), Interval(46, 50), Interval(74, 98),
         Interval(24, 28), Interval(57, 75), Interval(89, 103), Interval(26, 28), Interval(75, 79),
         Interval(19, 21), Interval(5, 5), Interval(10, 10), Interval(62, 66), Interval(59, 73),
         Interval(51, 63), Interval(65, 83), Interval(96, 96), Interval(11, 11), Interval(71, 95)],
        # Job 13
        [Interval(31, 35), Interval(39, 49), Interval(20, 22), Interval(29, 33), Interval(11, 13),
         Interval(18, 20), Interval(84, 86), Interval(14, 18), Interval(78, 80), Interval(98, 98),
         Interval(19, 21), Interval(17, 19), Interval(20, 22), Interval(71, 83), Interval(16, 20),
         Interval(40, 50), Interval(56, 60), Interval(43, 55), Interval(87, 101), Interval(81, 95)],
        # Job 14
        [Interval(71, 71), Interval(32, 40), Interval(83, 83), Interval(42, 54), Interval(22, 24),
         Interval(73, 95), Interval(17, 19), Interval(86, 104), Interval(24, 28), Interval(87, 101),
         Interval(60, 60), Interval(24, 32), Interval(81, 81), Interval(69, 73), Interval(75, 75),
         Interval(57, 69), Interval(34, 46), Interval(62, 68), Interval(32, 36), Interval(86, 108)],
        # Job 15
        [Interval(12, 14), Interval(47, 53), Interval(15, 15), Interval(83, 87), Interval(22, 24),
         Interval(54, 60), Interval(91, 95), Interval(84, 84), Interval(64, 84), Interval(52, 58),
         Interval(86, 102), Interval(13, 13), Interval(93, 105), Interval(10, 10), Interval(57, 61),
         Interval(53, 67), Interval(91, 99), Interval(73, 79), Interval(59, 79), Interval(12, 16)],
        # Job 16
        [Interval(43, 45), Interval(61, 67), Interval(26, 32), Interval(66, 72), Interval(85, 107),
         Interval(23, 23), Interval(26, 28), Interval(4, 4), Interval(13, 13), Interval(7, 9),
         Interval(56, 62), Interval(29, 29), Interval(3, 3), Interval(70, 88), Interval(13, 15),
         Interval(45, 45), Interval(55, 63), Interval(80, 90), Interval(2, 2), Interval(68, 82)],
        # Job 17
        [Interval(38, 42), Interval(29, 37), Interval(11, 11), Interval(61, 61), Interval(14, 18),
         Interval(73, 97), Interval(90, 100), Interval(74, 92), Interval(78, 86), Interval(84, 104),
         Interval(35, 39), Interval(43, 57), Interval(57, 65), Interval(75, 89), Interval(31, 41),
         Interval(6, 6), Interval(14, 14), Interval(2, 2), Interval(89, 109), Interval(68, 88)],
        # Job 18
        [Interval(65, 81), Interval(41, 55), Interval(7, 9), Interval(29, 39), Interval(70, 90),
         Interval(59, 75), Interval(47, 47), Interval(12, 14), Interval(95, 103), Interval(10, 10),
         Interval(28, 34), Interval(61, 69), Interval(64, 66), Interval(24, 28), Interval(3, 3),
         Interval(44, 50), Interval(62, 74), Interval(10, 12), Interval(11, 13), Interval(41, 45)],
        # Job 19
        [Interval(59, 69), Interval(42, 48), Interval(17, 19), Interval(22, 26), Interval(8, 10),
         Interval(38, 40), Interval(93, 103), Interval(47, 55), Interval(26, 30), Interval(17, 19),
         Interval(33, 35), Interval(2, 2), Interval(16, 20), Interval(21, 27), Interval(72, 92),
         Interval(36, 36), Interval(43, 53), Interval(50, 52), Interval(2, 2), Interval(83, 89)],
        # Job 20
        [Interval(65, 71), Interval(65, 79), Interval(50, 58), Interval(26, 32), Interval(77, 93),
         Interval(10, 12), Interval(35, 37), Interval(31, 39), Interval(8, 8), Interval(43, 51),
         Interval(63, 77), Interval(56, 56), Interval(32, 32), Interval(93, 101), Interval(25, 29),
         Interval(31, 33), Interval(76, 78), Interval(44, 56), Interval(15, 15), Interval(58, 70)],
        # Job 21
        [Interval(55, 59), Interval(4, 4), Interval(79, 95), Interval(42, 48), Interval(64, 80),
         Interval(84, 84), Interval(56, 72), Interval(13, 13), Interval(29, 37), Interval(82, 104),
         Interval(19, 21), Interval(29, 33), Interval(63, 75), Interval(88, 104), Interval(56, 62),
         Interval(84, 90), Interval(79, 85), Interval(84, 98), Interval(89, 93), Interval(13, 17)],
        # Job 22
        [Interval(39, 41), Interval(86, 110), Interval(89, 101), Interval(93, 99), Interval(24, 32),
         Interval(88, 94), Interval(56, 74), Interval(28, 34), Interval(11, 13), Interval(22, 28),
         Interval(10, 12), Interval(11, 11), Interval(61, 77), Interval(73, 81), Interval(45, 59),
         Interval(15, 19), Interval(44, 44), Interval(36, 48), Interval(71, 81), Interval(84, 94)],
        # Job 23
        [Interval(83, 89), Interval(26, 26), Interval(67, 87), Interval(52, 66), Interval(48, 60),
         Interval(17, 17), Interval(8, 10), Interval(37, 37), Interval(29, 29), Interval(34, 40),
         Interval(38, 46), Interval(26, 26), Interval(72, 96), Interval(95, 101), Interval(49, 57),
         Interval(46, 54), Interval(73, 77), Interval(34, 40), Interval(81, 105), Interval(51, 69)],
        # Job 24
        [Interval(42, 56), Interval(58, 76), Interval(32, 38), Interval(60, 68), Interval(10, 10),
         Interval(16, 18), Interval(1, 1), Interval(6, 6), Interval(73, 91), Interval(67, 83),
         Interval(29, 35), Interval(41, 41), Interval(25, 27), Interval(86, 100), Interval(73, 75),
         Interval(85, 95), Interval(30, 36), Interval(32, 38), Interval(92, 106), Interval(43, 57)],
        # Job 25
        [Interval(33, 37), Interval(63, 79), Interval(51, 63), Interval(45, 47), Interval(11, 11),
         Interval(38, 50), Interval(74, 98), Interval(53, 53), Interval(4, 4), Interval(1, 1),
         Interval(22, 22), Interval(2, 2), Interval(34, 46), Interval(70, 94), Interval(56, 64),
         Interval(87, 95), Interval(3, 3), Interval(44, 46), Interval(75, 83), Interval(72, 72)],
        # Job 26
        [Interval(49, 61), Interval(49, 63), Interval(90, 102), Interval(29, 29), Interval(28, 28),
         Interval(7, 9), Interval(25, 33), Interval(24, 28), Interval(75, 81), Interval(23, 31),
         Interval(28, 30), Interval(81, 83), Interval(27, 35), Interval(56, 60), Interval(1, 1),
         Interval(77, 89), Interval(53, 57), Interval(78, 84), Interval(26, 30), Interval(93, 105)],
        # Job 27
        [Interval(65, 77), Interval(37, 47), Interval(21, 25), Interval(55, 55), Interval(56, 62),
         Interval(93, 101), Interval(80, 92), Interval(19, 21), Interval(79, 93), Interval(30, 34),
         Interval(55, 59), Interval(59, 67), Interval(16, 20), Interval(83, 107), Interval(36, 42),
         Interval(86, 94), Interval(3, 3), Interval(34, 40), Interval(80, 94), Interval(77, 93)],
        # Job 28
        [Interval(52, 68), Interval(41, 47), Interval(72, 82), Interval(20, 24), Interval(68, 82),
         Interval(4, 4), Interval(6, 6), Interval(64, 72), Interval(6, 6), Interval(19, 19),
         Interval(77, 87), Interval(93, 97), Interval(33, 39), Interval(43, 53), Interval(6, 8),
         Interval(88, 88), Interval(49, 59), Interval(2, 2), Interval(74, 76), Interval(12, 14)],
        # Job 29
        [Interval(6, 8), Interval(77, 77), Interval(66, 88), Interval(12, 14), Interval(89, 105),
         Interval(22, 22), Interval(21, 21), Interval(78, 98), Interval(79, 101), Interval(89, 101),
         Interval(10, 12), Interval(28, 32), Interval(56, 66), Interval(11, 11), Interval(39, 39),
         Interval(47, 49), Interval(79, 97), Interval(51, 65), Interval(22, 24), Interval(82, 96)],
        # Job 30
        [Interval(56, 56), Interval(61, 69), Interval(5, 5), Interval(89, 89), Interval(87, 111),
         Interval(56, 64), Interval(69, 77), Interval(53, 59), Interval(61, 75), Interval(63, 63),
         Interval(48, 48), Interval(68, 72), Interval(50, 52), Interval(6, 8), Interval(8, 8),
         Interval(6, 8), Interval(43, 43), Interval(16, 20), Interval(17, 19), Interval(71, 91)],
        # Job 31
        [Interval(50, 54), Interval(13, 17), Interval(65, 85), Interval(64, 68), Interval(80, 104),
         Interval(65, 67), Interval(14, 18), Interval(95, 97), Interval(65, 79), Interval(34, 36),
         Interval(24, 28), Interval(19, 23), Interval(59, 79), Interval(74, 98), Interval(15, 15),
         Interval(54, 66), Interval(6, 6), Interval(61, 61), Interval(2, 2), Interval(7, 9)],
        # Job 32
        [Interval(90, 94), Interval(78, 90), Interval(16, 16), Interval(25, 29), Interval(66, 88),
         Interval(76, 88), Interval(60, 74), Interval(65, 83), Interval(78, 84), Interval(84, 100),
         Interval(64, 86), Interval(91, 93), Interval(50, 50), Interval(71, 95), Interval(39, 47),
         Interval(36, 48), Interval(43, 55), Interval(50, 52), Interval(35, 37), Interval(89, 89)],
        # Job 33
        [Interval(39, 45), Interval(86, 108), Interval(2, 2), Interval(66, 74), Interval(55, 63),
         Interval(53, 61), Interval(28, 32), Interval(20, 26), Interval(44, 54), Interval(19, 21),
         Interval(63, 73), Interval(10, 10), Interval(52, 70), Interval(74, 94), Interval(14, 16),
         Interval(52, 64), Interval(25, 31), Interval(58, 64), Interval(59, 75), Interval(10, 10)],
        # Job 34
        [Interval(28, 30), Interval(57, 57), Interval(23, 29), Interval(71, 87), Interval(70, 72),
         Interval(15, 15), Interval(43, 49), Interval(73, 75), Interval(6, 6), Interval(95, 99),
         Interval(48, 54), Interval(3, 3), Interval(63, 63), Interval(72, 86), Interval(80, 90),
         Interval(79, 93), Interval(40, 46), Interval(21, 23), Interval(1, 1), Interval(35, 43)],
        # Job 35
        [Interval(71, 93), Interval(30, 40), Interval(20, 20), Interval(48, 50), Interval(84, 110),
         Interval(14, 16), Interval(29, 39), Interval(85, 99), Interval(20, 26), Interval(57, 63),
         Interval(12, 14), Interval(46, 58), Interval(38, 38), Interval(30, 38), Interval(62, 74),
         Interval(88, 106), Interval(1, 1), Interval(18, 18), Interval(63, 83), Interval(62, 82)],
        # Job 36
        [Interval(4, 4), Interval(82, 90), Interval(2, 2), Interval(21, 27), Interval(42, 42),
         Interval(69, 71), Interval(48, 62), Interval(45, 45), Interval(44, 54), Interval(96, 96),
         Interval(74, 82), Interval(68, 78), Interval(1, 1), Interval(45, 51), Interval(15, 19),
         Interval(47, 59), Interval(13, 17), Interval(46, 50), Interval(81, 91), Interval(4, 4)],
        # Job 37
        [Interval(74, 100), Interval(39, 41), Interval(51, 59), Interval(7, 7), Interval(32, 34),
         Interval(39, 49), Interval(76, 80), Interval(21, 21), Interval(48, 48), Interval(87, 97),
         Interval(59, 61), Interval(66, 72), Interval(32, 32), Interval(64, 86), Interval(84, 94),
         Interval(70, 74), Interval(62, 62), Interval(6, 8), Interval(44, 56), Interval(22, 22)],
        # Job 38
        [Interval(72, 76), Interval(45, 59), Interval(73, 91), Interval(22, 28), Interval(23, 25),
         Interval(87, 99), Interval(74, 74), Interval(53, 63), Interval(75, 91), Interval(2, 2),
         Interval(11, 13), Interval(70, 82), Interval(83, 111), Interval(1, 1), Interval(11, 11),
         Interval(27, 31), Interval(55, 59), Interval(36, 46), Interval(25, 33), Interval(67, 89)],
        # Job 39
        [Interval(28, 36), Interval(76, 90), Interval(68, 92), Interval(85, 93), Interval(98, 100),
         Interval(25, 25), Interval(5, 5), Interval(27, 31), Interval(76, 78), Interval(37, 45),
         Interval(6, 6), Interval(71, 83), Interval(70, 72), Interval(20, 22), Interval(12, 16),
         Interval(73, 73), Interval(55, 67), Interval(24, 28), Interval(51, 57), Interval(97, 101)],
        # Job 40
        [Interval(19, 19), Interval(40, 40), Interval(68, 68), Interval(4, 4), Interval(86, 112),
         Interval(70, 74), Interval(18, 18), Interval(45, 45), Interval(29, 37), Interval(40, 42),
         Interval(33, 43), Interval(64, 86), Interval(57, 65), Interval(8, 8), Interval(66, 80),
         Interval(74, 86), Interval(65, 81), Interval(61, 67), Interval(32, 34), Interval(14, 14)],
        # Job 41
        [Interval(74, 80), Interval(61, 61), Interval(19, 23), Interval(81, 83), Interval(73, 81),
         Interval(21, 27), Interval(87, 105), Interval(31, 39), Interval(11, 11), Interval(22, 24),
         Interval(67, 87), Interval(79, 93), Interval(8, 8), Interval(5, 5), Interval(41, 45),
         Interval(11, 13), Interval(29, 39), Interval(29, 33), Interval(40, 48), Interval(13, 17)],
        # Job 42
        [Interval(48, 54), Interval(58, 68), Interval(17, 21), Interval(12, 16), Interval(5, 5),
         Interval(48, 52), Interval(16, 20), Interval(4, 4), Interval(77, 91), Interval(43, 57),
         Interval(41, 41), Interval(39, 39), Interval(86, 110), Interval(63, 71), Interval(27, 35),
         Interval(58, 60), Interval(68, 70), Interval(87, 95), Interval(62, 72), Interval(29, 39)],
        # Job 43
        [Interval(83, 101), Interval(54, 60), Interval(70, 76), Interval(72, 88), Interval(53, 61),
         Interval(66, 88), Interval(74, 92), Interval(91, 103), Interval(46, 48), Interval(94, 96),
         Interval(78, 90), Interval(9, 9), Interval(52, 60), Interval(46, 56), Interval(31, 33),
         Interval(11, 11), Interval(59, 75), Interval(44, 48), Interval(44, 56), Interval(65, 73)],
        # Job 44
        [Interval(35, 45), Interval(1, 1), Interval(45, 57), Interval(33, 33), Interval(64, 86),
         Interval(60, 66), Interval(61, 63), Interval(49, 59), Interval(34, 38), Interval(15, 19),
         Interval(55, 63), Interval(83, 109), Interval(65, 71), Interval(39, 49), Interval(53, 61),
         Interval(87, 91), Interval(44, 56), Interval(8, 10), Interval(10, 12), Interval(10, 10)],
        # Job 45
        [Interval(42, 48), Interval(91, 107), Interval(86, 98), Interval(7, 9), Interval(71, 83),
         Interval(15, 15), Interval(77, 83), Interval(12, 14), Interval(47, 53), Interval(28, 32),
         Interval(66, 66), Interval(9, 9), Interval(66, 88), Interval(64, 80), Interval(25, 27),
         Interval(85, 107), Interval(85, 85), Interval(54, 62), Interval(42, 44), Interval(40, 44)],
        # Job 46
        [Interval(56, 56), Interval(24, 32), Interval(74, 88), Interval(18, 22), Interval(11, 13),
         Interval(14, 14), Interval(45, 49), Interval(83, 83), Interval(59, 69), Interval(44, 44),
         Interval(38, 46), Interval(65, 71), Interval(84, 106), Interval(15, 19), Interval(47, 63),
         Interval(54, 70), Interval(69, 69), Interval(64, 78), Interval(91, 95), Interval(12, 12)],
        # Job 47
        [Interval(15, 19), Interval(25, 27), Interval(97, 99), Interval(45, 53), Interval(71, 85),
         Interval(35, 37), Interval(86, 88), Interval(95, 97), Interval(28, 36), Interval(23, 23),
         Interval(52, 60), Interval(73, 95), Interval(20, 22), Interval(65, 73), Interval(86, 110),
         Interval(9, 9), Interval(67, 83), Interval(67, 89), Interval(30, 34), Interval(54, 60)],
        # Job 48
        [Interval(33, 33), Interval(82, 82), Interval(67, 71), Interval(31, 33), Interval(58, 64),
         Interval(49, 49), Interval(53, 69), Interval(95, 101), Interval(72, 90), Interval(57, 65),
         Interval(17, 21), Interval(60, 66), Interval(45, 47), Interval(80, 82), Interval(20, 24),
         Interval(68, 92), Interval(42, 44), Interval(17, 23), Interval(55, 59), Interval(30, 32)],
        # Job 49
        [Interval(91, 103), Interval(60, 70), Interval(82, 84), Interval(53, 69), Interval(32, 38),
         Interval(85, 85), Interval(91, 105), Interval(52, 60), Interval(18, 24), Interval(83, 109),
         Interval(17, 23), Interval(68, 90), Interval(62, 78), Interval(36, 40), Interval(30, 32),
         Interval(56, 58), Interval(29, 37), Interval(71, 95), Interval(52, 64), Interval(29, 29)],
        # Job 50
        [Interval(32, 42), Interval(22, 24), Interval(29, 35), Interval(81, 107), Interval(85, 87),
         Interval(42, 46), Interval(6, 6), Interval(59, 63), Interval(20, 24), Interval(15, 15),
         Interval(41, 43), Interval(65, 69), Interval(34, 38), Interval(75, 91), Interval(48, 56),
         Interval(47, 51), Interval(5, 5), Interval(84, 86), Interval(58, 68), Interval(53, 67)],
        # Job 51
        [Interval(98, 100), Interval(82, 108), Interval(57, 75), Interval(59, 63), Interval(5, 5),
         Interval(6, 6), Interval(57, 57), Interval(3, 3), Interval(35, 39), Interval(74, 100),
         Interval(27, 27), Interval(11, 11), Interval(27, 29), Interval(56, 66), Interval(85, 101),
         Interval(74, 74), Interval(5, 5), Interval(39, 45), Interval(45, 45), Interval(51, 51)],
        # Job 52
        [Interval(16, 20), Interval(38, 50), Interval(4, 4), Interval(60, 70), Interval(76, 88),
         Interval(91, 103), Interval(26, 30), Interval(55, 69), Interval(34, 38), Interval(96, 96),
         Interval(65, 87), Interval(54, 64), Interval(45, 57), Interval(16, 16), Interval(83, 95),
         Interval(38, 40), Interval(49, 61), Interval(9, 11), Interval(23, 25), Interval(62, 62)],
        # Job 53
        [Interval(78, 78), Interval(7, 9), Interval(8, 10), Interval(4, 4), Interval(43, 53),
         Interval(42, 54), Interval(76, 78), Interval(61, 69), Interval(64, 78), Interval(4, 4),
         Interval(18, 18), Interval(82, 104), Interval(63, 77), Interval(38, 44), Interval(27, 27),
         Interval(77, 93), Interval(57, 67), Interval(17, 23), Interval(26, 28), Interval(88, 92)],
        # Job 54
        [Interval(55, 59), Interval(1, 1), Interval(12, 16), Interval(11, 11), Interval(37, 39),
         Interval(64, 84), Interval(6, 6), Interval(72, 72), Interval(15, 17), Interval(11, 11),
         Interval(24, 26), Interval(5, 5), Interval(76, 96), Interval(77, 89), Interval(5, 5),
         Interval(39, 43), Interval(52, 52), Interval(37, 41), Interval(71, 89), Interval(71, 77)],
        # Job 55
        [Interval(69, 83), Interval(41, 53), Interval(32, 34), Interval(31, 31), Interval(54, 68),
         Interval(76, 80), Interval(26, 28), Interval(64, 72), Interval(31, 37), Interval(87, 111),
         Interval(40, 48), Interval(57, 71), Interval(12, 14), Interval(39, 51), Interval(54, 56),
         Interval(17, 21), Interval(86, 112), Interval(33, 35), Interval(84, 84), Interval(63, 85)],
        # Job 56
        [Interval(34, 42), Interval(74, 84), Interval(6, 6), Interval(8, 8), Interval(12, 12),
         Interval(71, 73), Interval(4, 4), Interval(4, 4), Interval(8, 8), Interval(53, 57),
         Interval(21, 25), Interval(74, 80), Interval(48, 56), Interval(52, 58), Interval(54, 54),
         Interval(27, 33), Interval(74, 94), Interval(69, 89), Interval(66, 66), Interval(20, 22)],
        # Job 57
        [Interval(58, 60), Interval(31, 31), Interval(83, 83), Interval(55, 59), Interval(67, 67),
         Interval(15, 19), Interval(70, 70), Interval(21, 25), Interval(12, 16), Interval(52, 56),
         Interval(10, 10), Interval(23, 25), Interval(79, 79), Interval(58, 76), Interval(69, 85),
         Interval(89, 91), Interval(6, 8), Interval(85, 103), Interval(33, 35), Interval(65, 73)],
        # Job 58
        [Interval(35, 37), Interval(6, 8), Interval(23, 31), Interval(16, 16), Interval(16, 16),
         Interval(10, 10), Interval(56, 64), Interval(70, 86), Interval(69, 91), Interval(6, 8),
         Interval(36, 38), Interval(73, 79), Interval(29, 33), Interval(33, 39), Interval(23, 29),
         Interval(63, 63), Interval(77, 79), Interval(67, 89), Interval(89, 95), Interval(40, 52)],
        # Job 59
        [Interval(66, 76), Interval(56, 64), Interval(73, 75), Interval(25, 33), Interval(25, 29),
         Interval(52, 62), Interval(73, 93), Interval(5, 5), Interval(12, 12), Interval(60, 76),
         Interval(94, 98), Interval(24, 26), Interval(49, 51), Interval(83, 87), Interval(21, 25),
         Interval(1, 1), Interval(67, 87), Interval(64, 84), Interval(20, 22), Interval(30, 36)],
        # Job 60
        [Interval(24, 24), Interval(18, 24), Interval(80, 108), Interval(4, 4), Interval(3, 3),
         Interval(4, 4), Interval(50, 62), Interval(21, 25), Interval(67, 73), Interval(37, 47),
         Interval(59, 77), Interval(86, 110), Interval(48, 48), Interval(46, 50), Interval(9, 9),
         Interval(91, 105), Interval(56, 72), Interval(69, 69), Interval(55, 57), Interval(84, 84)],
        # Job 61
        [Interval(92, 106), Interval(51, 53), Interval(51, 53), Interval(69, 75), Interval(81, 109),
         Interval(9, 11), Interval(87, 101), Interval(50, 52), Interval(67, 87), Interval(12, 14),
         Interval(74, 90), Interval(59, 63), Interval(61, 75), Interval(39, 39), Interval(59, 61),
         Interval(43, 43), Interval(84, 104), Interval(28, 28), Interval(33, 39), Interval(77, 77)],
        # Job 62
        [Interval(4, 4), Interval(41, 49), Interval(11, 11), Interval(14, 18), Interval(92, 104),
         Interval(92, 96), Interval(18, 22), Interval(97, 101), Interval(84, 94), Interval(62, 64),
         Interval(32, 38), Interval(65, 79), Interval(88, 88), Interval(20, 24), Interval(70, 74),
         Interval(69, 73), Interval(67, 71), Interval(50, 50), Interval(76, 78), Interval(36, 44)],
        # Job 63
        [Interval(58, 76), Interval(77, 103), Interval(42, 50), Interval(9, 11), Interval(17, 21),
         Interval(24, 24), Interval(32, 40), Interval(36, 40), Interval(64, 82), Interval(65, 83),
         Interval(32, 34), Interval(16, 18), Interval(8, 10), Interval(14, 16), Interval(90, 100),
         Interval(31, 35), Interval(43, 49), Interval(73, 97), Interval(34, 34), Interval(46, 56)],
        # Job 64
        [Interval(8, 10), Interval(8, 8), Interval(90, 104), Interval(55, 73), Interval(58, 70),
         Interval(95, 97), Interval(31, 35), Interval(23, 29), Interval(77, 99), Interval(63, 71),
         Interval(18, 22), Interval(16, 20), Interval(59, 75), Interval(44, 58), Interval(70, 84),
         Interval(42, 44), Interval(75, 79), Interval(81, 85), Interval(9, 9), Interval(18, 22)],
        # Job 65
        [Interval(43, 43), Interval(21, 21), Interval(49, 53), Interval(33, 37), Interval(11, 11),
         Interval(29, 31), Interval(82, 96), Interval(43, 53), Interval(64, 76), Interval(61, 63),
         Interval(50, 62), Interval(91, 97), Interval(12, 12), Interval(25, 25), Interval(81, 85),
         Interval(21, 21), Interval(80, 102), Interval(70, 90), Interval(42, 44), Interval(75, 75)],
        # Job 66
        [Interval(12, 14), Interval(34, 36), Interval(38, 48), Interval(70, 90), Interval(52, 54),
         Interval(11, 11), Interval(91, 103), Interval(27, 31), Interval(83, 83), Interval(6, 6),
         Interval(63, 83), Interval(9, 11), Interval(52, 58), Interval(32, 32), Interval(49, 49),
         Interval(48, 52), Interval(22, 22), Interval(83, 89), Interval(17, 23), Interval(75, 87)],
        # Job 67
        [Interval(53, 57), Interval(19, 25), Interval(82, 100), Interval(56, 70), Interval(13, 17),
         Interval(5, 5), Interval(89, 103), Interval(53, 53), Interval(62, 74), Interval(5, 5),
         Interval(59, 59), Interval(17, 19), Interval(74, 100), Interval(67, 85), Interval(18, 20),
         Interval(92, 92), Interval(16, 20), Interval(17, 17), Interval(17, 23), Interval(28, 30)],
        # Job 68
        [Interval(8, 8), Interval(2, 2), Interval(29, 35), Interval(12, 12), Interval(54, 56),
         Interval(23, 31), Interval(9, 9), Interval(52, 68), Interval(38, 50), Interval(79, 93),
         Interval(61, 71), Interval(49, 55), Interval(31, 39), Interval(21, 21), Interval(74, 78),
         Interval(45, 55), Interval(52, 64), Interval(25, 25), Interval(23, 29), Interval(20, 24)],
        # Job 69
        [Interval(16, 20), Interval(86, 102), Interval(80, 86), Interval(44, 58), Interval(91, 91),
         Interval(64, 84), Interval(8, 10), Interval(26, 32), Interval(81, 105), Interval(72, 78),
         Interval(61, 63), Interval(46, 46), Interval(60, 76), Interval(72, 82), Interval(29, 39),
         Interval(64, 66), Interval(68, 78), Interval(73, 73), Interval(40, 40), Interval(44, 44)],
        # Job 70
        [Interval(48, 58), Interval(17, 17), Interval(48, 64), Interval(36, 40), Interval(60, 66),
         Interval(60, 70), Interval(37, 39), Interval(65, 65), Interval(43, 53), Interval(53, 65),
         Interval(39, 41), Interval(29, 37), Interval(15, 15), Interval(78, 94), Interval(66, 66),
         Interval(37, 39), Interval(83, 107), Interval(70, 90), Interval(45, 49), Interval(9, 11)],
        # Job 71
        [Interval(36, 44), Interval(59, 77), Interval(47, 59), Interval(63, 75), Interval(19, 25),
         Interval(92, 102), Interval(44, 54), Interval(64, 78), Interval(71, 93), Interval(77, 79),
         Interval(3, 3), Interval(16, 18), Interval(20, 20), Interval(52, 52), Interval(7, 9),
         Interval(5, 5), Interval(92, 106), Interval(62, 66), Interval(77, 93), Interval(53, 69)],
        # Job 72
        [Interval(83, 105), Interval(12, 12), Interval(33, 43), Interval(63, 73), Interval(48, 48),
         Interval(30, 36), Interval(8, 8), Interval(40, 44), Interval(78, 84), Interval(50, 58),
         Interval(61, 73), Interval(60, 66), Interval(40, 50), Interval(44, 44), Interval(10, 12),
         Interval(44, 52), Interval(23, 27), Interval(23, 29), Interval(55, 57), Interval(41, 55)],
        # Job 73
        [Interval(58, 60), Interval(37, 39), Interval(76, 90), Interval(42, 44), Interval(7, 9),
         Interval(26, 32), Interval(54, 58), Interval(50, 58), Interval(33, 35), Interval(35, 47),
         Interval(45, 57), Interval(76, 102), Interval(76, 90), Interval(13, 13), Interval(54, 68),
         Interval(13, 13), Interval(29, 37), Interval(5, 5), Interval(32, 40), Interval(9, 11)],
        # Job 74
        [Interval(80, 108), Interval(41, 43), Interval(51, 57), Interval(38, 44), Interval(69, 87),
         Interval(71, 89), Interval(47, 59), Interval(86, 110), Interval(9, 11), Interval(85, 87),
         Interval(19, 19), Interval(71, 73), Interval(21, 27), Interval(87, 105), Interval(6, 6),
         Interval(14, 14), Interval(24, 30), Interval(18, 20), Interval(18, 20), Interval(78, 98)],
        # Job 75
        [Interval(57, 69), Interval(30, 38), Interval(60, 72), Interval(75, 85), Interval(59, 63),
         Interval(12, 12), Interval(30, 30), Interval(27, 35), Interval(34, 46), Interval(89, 99),
         Interval(91, 93), Interval(79, 99), Interval(51, 65), Interval(43, 55), Interval(29, 29),
         Interval(83, 103), Interval(1, 1), Interval(48, 64), Interval(48, 52), Interval(85, 113)],
        # Job 76
        [Interval(97, 97), Interval(70, 74), Interval(26, 28), Interval(34, 42), Interval(64, 80),
         Interval(82, 98), Interval(88, 94), Interval(50, 52), Interval(8, 10), Interval(13, 15),
         Interval(57, 77), Interval(59, 71), Interval(4, 4), Interval(12, 14), Interval(73, 95),
         Interval(1, 1), Interval(19, 21), Interval(66, 80), Interval(12, 12), Interval(59, 65)],
        # Job 77
        [Interval(74, 90), Interval(79, 89), Interval(45, 45), Interval(40, 52), Interval(5, 5),
         Interval(23, 27), Interval(27, 35), Interval(53, 67), Interval(11, 13), Interval(29, 35),
         Interval(20, 22), Interval(47, 53), Interval(72, 82), Interval(31, 41), Interval(83, 89),
         Interval(34, 34), Interval(10, 12), Interval(12, 12), Interval(60, 60), Interval(1, 1)],
        # Job 78
        [Interval(35, 47), Interval(21, 23), Interval(18, 22), Interval(65, 87), Interval(39, 51),
         Interval(56, 64), Interval(91, 103), Interval(71, 93), Interval(31, 35), Interval(54, 64),
         Interval(42, 54), Interval(58, 58), Interval(82, 108), Interval(42, 48), Interval(21, 21),
         Interval(77, 93), Interval(71, 93), Interval(46, 54), Interval(18, 18), Interval(18, 24)],
        # Job 79
        [Interval(20, 22), Interval(66, 66), Interval(28, 34), Interval(14, 16), Interval(88, 96),
         Interval(10, 12), Interval(30, 38), Interval(44, 48), Interval(28, 28), Interval(95, 97),
         Interval(71, 73), Interval(79, 79), Interval(75, 95), Interval(77, 79), Interval(29, 33),
         Interval(73, 79), Interval(22, 28), Interval(2, 2), Interval(17, 23), Interval(58, 76)],
        # Job 80
        [Interval(75, 79), Interval(36, 42), Interval(67, 75), Interval(74, 92), Interval(60, 80),
         Interval(44, 50), Interval(30, 34), Interval(10, 12), Interval(26, 26), Interval(1, 1),
         Interval(75, 75), Interval(16, 18), Interval(70, 84), Interval(89, 107), Interval(5, 5),
         Interval(10, 10), Interval(10, 12), Interval(29, 37), Interval(69, 77), Interval(61, 73)],
        # Job 81
        [Interval(15, 17), Interval(36, 42), Interval(26, 32), Interval(25, 29), Interval(70, 70),
         Interval(50, 54), Interval(10, 12), Interval(25, 27), Interval(59, 65), Interval(17, 21),
         Interval(98, 100), Interval(34, 42), Interval(89, 101), Interval(13, 13), Interval(3, 3),
         Interval(41, 47), Interval(30, 30), Interval(43, 49), Interval(66, 78), Interval(84, 94)],
        # Job 82
        [Interval(59, 71), Interval(87, 107), Interval(22, 24), Interval(36, 40), Interval(56, 58),
         Interval(64, 82), Interval(32, 34), Interval(11, 11), Interval(8, 10), Interval(82, 110),
         Interval(4, 4), Interval(72, 84), Interval(38, 38), Interval(46, 62), Interval(54, 72),
         Interval(86, 110), Interval(75, 97), Interval(58, 58), Interval(44, 54), Interval(88, 104)],
        # Job 83
        [Interval(82, 108), Interval(78, 94), Interval(55, 61), Interval(41, 51), Interval(51, 51),
         Interval(97, 101), Interval(54, 64), Interval(4, 4), Interval(31, 35), Interval(6, 6),
         Interval(49, 51), Interval(43, 55), Interval(59, 65), Interval(63, 75), Interval(36, 38),
         Interval(57, 73), Interval(11, 13), Interval(52, 60), Interval(81, 95), Interval(74, 90)],
        # Job 84
        [Interval(53, 69), Interval(49, 57), Interval(29, 37), Interval(5, 5), Interval(35, 41),
         Interval(59, 67), Interval(32, 38), Interval(66, 82), Interval(52, 60), Interval(52, 56),
         Interval(66, 80), Interval(17, 17), Interval(53, 69), Interval(43, 55), Interval(4, 4),
         Interval(71, 81), Interval(11, 11), Interval(56, 72), Interval(70, 70), Interval(50, 50)],
        # Job 85
        [Interval(16, 18), Interval(32, 38), Interval(67, 79), Interval(25, 31), Interval(77, 85),
         Interval(17, 19), Interval(88, 102), Interval(26, 26), Interval(93, 93), Interval(28, 36),
         Interval(3, 3), Interval(35, 43), Interval(13, 13), Interval(93, 101), Interval(89, 99),
         Interval(49, 57), Interval(11, 11), Interval(74, 86), Interval(27, 33), Interval(28, 28)],
        # Job 86
        [Interval(1, 1), Interval(95, 101), Interval(32, 32), Interval(48, 64), Interval(34, 44),
         Interval(26, 32), Interval(33, 33), Interval(82, 82), Interval(53, 61), Interval(16, 18),
         Interval(36, 42), Interval(76, 78), Interval(73, 73), Interval(11, 13), Interval(91, 91),
         Interval(59, 75), Interval(72, 72), Interval(89, 99), Interval(13, 15), Interval(73, 73)],
        # Job 87
        [Interval(33, 39), Interval(47, 49), Interval(59, 73), Interval(22, 24), Interval(49, 55),
         Interval(87, 97), Interval(85, 95), Interval(1, 1), Interval(1, 1), Interval(35, 43),
         Interval(49, 49), Interval(25, 25), Interval(4, 4), Interval(14, 18), Interval(70, 78),
         Interval(32, 40), Interval(49, 53), Interval(57, 65), Interval(14, 18), Interval(53, 59)],
        # Job 88
        [Interval(80, 100), Interval(19, 23), Interval(99, 99), Interval(28, 30), Interval(47, 51),
         Interval(13, 13), Interval(93, 95), Interval(25, 27), Interval(17, 23), Interval(63, 83),
         Interval(21, 21), Interval(24, 32), Interval(46, 62), Interval(3, 3), Interval(95, 99),
         Interval(39, 47), Interval(45, 51), Interval(51, 59), Interval(19, 21), Interval(61, 79)],
        # Job 89
        [Interval(62, 66), Interval(6, 6), Interval(66, 78), Interval(68, 80), Interval(24, 26),
         Interval(41, 45), Interval(7, 9), Interval(19, 21), Interval(78, 82), Interval(84, 94),
         Interval(6, 6), Interval(44, 44), Interval(2, 2), Interval(6, 6), Interval(54, 54),
         Interval(49, 53), Interval(40, 42), Interval(87, 109), Interval(90, 90), Interval(87, 101)],
        # Job 90
        [Interval(84, 98), Interval(52, 66), Interval(23, 31), Interval(59, 71), Interval(44, 46),
         Interval(22, 22), Interval(88, 106), Interval(53, 53), Interval(63, 81), Interval(46, 48),
         Interval(87, 109), Interval(42, 56), Interval(71, 81), Interval(75, 97), Interval(78, 86),
         Interval(51, 53), Interval(62, 62), Interval(42, 54), Interval(35, 39), Interval(24, 26)],
        # Job 91
        [Interval(93, 101), Interval(27, 29), Interval(84, 90), Interval(50, 62), Interval(90, 102),
         Interval(14, 14), Interval(72, 84), Interval(5, 5), Interval(29, 29), Interval(12, 16),
         Interval(64, 82), Interval(50, 54), Interval(2, 2), Interval(29, 39), Interval(18, 20),
         Interval(15, 17), Interval(19, 23), Interval(73, 85), Interval(63, 79), Interval(6, 6)],
        # Job 92
        [Interval(80, 106), Interval(12, 16), Interval(77, 87), Interval(75, 87), Interval(48, 62),
         Interval(46, 62), Interval(50, 52), Interval(59, 63), Interval(19, 25), Interval(25, 31),
         Interval(3, 3), Interval(32, 38), Interval(19, 25), Interval(41, 51), Interval(79, 81),
         Interval(65, 67), Interval(90, 94), Interval(2, 2), Interval(17, 17), Interval(54, 68)],
        # Job 93
        [Interval(50, 56), Interval(2, 2), Interval(48, 54), Interval(56, 74), Interval(67, 83),
         Interval(13, 15), Interval(12, 14), Interval(50, 52), Interval(17, 19), Interval(71, 87),
         Interval(23, 27), Interval(52, 52), Interval(46, 52), Interval(39, 47), Interval(49, 49),
         Interval(81, 85), Interval(34, 38), Interval(53, 55), Interval(39, 47), Interval(66, 78)],
        # Job 94
        [Interval(1, 1), Interval(32, 32), Interval(65, 67), Interval(52, 52), Interval(84, 96),
         Interval(7, 9), Interval(30, 36), Interval(71, 73), Interval(79, 81), Interval(34, 46),
         Interval(35, 41), Interval(89, 107), Interval(64, 78), Interval(85, 111), Interval(12, 16),
         Interval(35, 35), Interval(21, 25), Interval(21, 23), Interval(22, 24), Interval(81, 105)],
        # Job 95
        [Interval(48, 50), Interval(16, 16), Interval(82, 88), Interval(9, 9), Interval(61, 61),
         Interval(21, 21), Interval(74, 98), Interval(14, 14), Interval(70, 92), Interval(59, 59),
         Interval(31, 37), Interval(59, 59), Interval(19, 19), Interval(77, 93), Interval(26, 32),
         Interval(67, 67), Interval(43, 49), Interval(81, 99), Interval(36, 48), Interval(23, 23)],
        # Job 96
        [Interval(25, 25), Interval(80, 88), Interval(4, 4), Interval(51, 55), Interval(89, 93),
         Interval(1, 1), Interval(24, 28), Interval(18, 20), Interval(86, 110), Interval(97, 97),
         Interval(5, 5), Interval(22, 26), Interval(65, 87), Interval(27, 29), Interval(18, 18),
         Interval(78, 84), Interval(64, 76), Interval(73, 95), Interval(11, 11), Interval(57, 75)],
        # Job 97
        [Interval(5, 5), Interval(6, 6), Interval(76, 86), Interval(43, 55), Interval(27, 33),
         Interval(75, 79), Interval(41, 47), Interval(2, 2), Interval(71, 75), Interval(69, 87),
         Interval(14, 16), Interval(37, 39), Interval(37, 41), Interval(78, 98), Interval(71, 73),
         Interval(61, 77), Interval(27, 33), Interval(6, 6), Interval(45, 47), Interval(6, 8)],
        # Job 98
        [Interval(35, 47), Interval(12, 16), Interval(75, 95), Interval(1, 1), Interval(62, 76),
         Interval(8, 10), Interval(37, 49), Interval(86, 90), Interval(41, 47), Interval(81, 89),
         Interval(78, 82), Interval(44, 56), Interval(3, 3), Interval(31, 31), Interval(65, 83),
         Interval(83, 93), Interval(84, 86), Interval(3, 3), Interval(68, 76), Interval(77, 93)],
        # Job 99
        [Interval(68, 88), Interval(47, 53), Interval(75, 77), Interval(45, 51), Interval(34, 42),
         Interval(76, 92), Interval(20, 22), Interval(55, 59), Interval(64, 80), Interval(8, 8),
         Interval(54, 56), Interval(52, 60), Interval(21, 25), Interval(4, 4), Interval(51, 63),
         Interval(50, 62), Interval(50, 66), Interval(27, 27), Interval(59, 73), Interval(10, 12)],
    ],
    'name': 'INT__TAI100_20_09.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai100_20_09_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI100_20_09.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI100_20_09.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI100_20_09_F_15_01_INTERVAL_DATA
