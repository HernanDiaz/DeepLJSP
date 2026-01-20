"""
Problema INT__TAI100_20_07.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI100_20_07_F_15_01_INTERVAL_DATA = {
    'num_jobs': 100,
    'num_machines': 20,
    'problem_id': 'int__tai100_20_07.F.15_01_interval',
    'sequences': [
        [3, 10, 16, 19, 7, 1, 12, 2, 15, 5, 0, 17, 9, 13, 14, 18, 6, 8, 11, 4],
        [2, 18, 9, 16, 14, 0, 3, 6, 5, 4, 15, 12, 8, 1, 10, 17, 11, 19, 7, 13],
        [7, 2, 11, 14, 0, 12, 13, 3, 8, 1, 18, 16, 5, 17, 15, 9, 4, 10, 19, 6],
        [1, 18, 12, 6, 8, 5, 19, 11, 9, 3, 2, 13, 17, 4, 10, 0, 15, 14, 7, 16],
        [6, 12, 8, 10, 11, 19, 2, 3, 4, 18, 16, 5, 0, 15, 13, 17, 7, 9, 1, 14],
        [4, 7, 17, 5, 16, 15, 12, 11, 0, 6, 19, 2, 3, 18, 1, 9, 14, 10, 13, 8],
        [3, 16, 19, 6, 10, 17, 4, 15, 1, 0, 9, 8, 2, 12, 5, 18, 7, 14, 11, 13],
        [12, 19, 5, 4, 8, 15, 9, 2, 16, 10, 1, 13, 7, 11, 17, 14, 18, 3, 6, 0],
        [3, 4, 13, 8, 19, 18, 14, 5, 12, 15, 10, 1, 9, 6, 11, 0, 17, 16, 7, 2],
        [13, 18, 19, 17, 16, 9, 6, 14, 8, 0, 12, 1, 11, 10, 15, 3, 4, 2, 5, 7],
        [19, 4, 17, 3, 15, 18, 11, 0, 10, 7, 6, 14, 12, 5, 8, 16, 2, 13, 9, 1],
        [2, 10, 13, 8, 11, 12, 9, 4, 16, 6, 15, 1, 14, 19, 0, 5, 3, 7, 17, 18],
        [7, 17, 11, 4, 2, 12, 15, 9, 18, 16, 8, 14, 10, 5, 19, 0, 6, 1, 13, 3],
        [11, 1, 6, 2, 7, 17, 10, 5, 16, 4, 13, 19, 3, 8, 0, 15, 18, 12, 14, 9],
        [18, 7, 11, 3, 9, 1, 12, 4, 13, 5, 14, 17, 8, 2, 15, 6, 0, 16, 10, 19],
        [4, 1, 6, 18, 0, 13, 3, 7, 15, 5, 8, 11, 12, 10, 2, 19, 17, 9, 16, 14],
        [11, 4, 10, 5, 14, 8, 6, 0, 9, 2, 15, 19, 13, 3, 1, 17, 7, 18, 16, 12],
        [17, 3, 1, 15, 13, 6, 12, 19, 7, 16, 11, 10, 0, 4, 2, 18, 5, 14, 8, 9],
        [14, 15, 12, 19, 17, 18, 10, 1, 6, 13, 3, 9, 4, 0, 11, 16, 7, 2, 8, 5],
        [5, 2, 4, 10, 19, 0, 3, 18, 1, 7, 16, 12, 11, 14, 9, 15, 17, 13, 8, 6],
        [18, 1, 14, 11, 19, 16, 9, 17, 3, 15, 0, 13, 10, 7, 12, 5, 6, 4, 2, 8],
        [10, 2, 19, 6, 0, 15, 18, 5, 13, 14, 12, 17, 7, 11, 1, 16, 4, 9, 8, 3],
        [4, 14, 17, 16, 15, 3, 5, 7, 11, 19, 18, 9, 13, 12, 2, 0, 6, 8, 10, 1],
        [12, 8, 3, 14, 18, 19, 15, 6, 11, 13, 16, 0, 1, 10, 5, 2, 17, 7, 9, 4],
        [8, 16, 17, 12, 1, 14, 2, 6, 7, 3, 10, 18, 13, 0, 5, 19, 15, 11, 9, 4],
        [8, 13, 9, 0, 10, 19, 4, 18, 17, 7, 2, 15, 12, 11, 3, 1, 5, 14, 6, 16],
        [2, 1, 19, 15, 8, 11, 5, 16, 7, 12, 0, 18, 17, 13, 10, 9, 14, 3, 6, 4],
        [13, 4, 18, 11, 12, 15, 3, 14, 5, 8, 10, 9, 0, 16, 6, 1, 17, 19, 2, 7],
        [19, 16, 17, 18, 12, 3, 6, 8, 15, 9, 7, 4, 1, 13, 5, 2, 11, 14, 0, 10],
        [7, 5, 13, 12, 9, 19, 1, 0, 14, 10, 17, 8, 6, 15, 2, 3, 11, 16, 4, 18],
        [18, 1, 8, 5, 13, 12, 7, 11, 19, 4, 10, 2, 16, 3, 14, 0, 6, 17, 9, 15],
        [8, 12, 17, 7, 11, 14, 10, 1, 5, 18, 0, 9, 15, 13, 3, 6, 19, 16, 2, 4],
        [15, 13, 14, 2, 10, 9, 12, 19, 0, 5, 8, 17, 1, 16, 18, 3, 11, 4, 7, 6],
        [18, 7, 5, 15, 12, 6, 4, 0, 13, 11, 17, 9, 8, 16, 3, 10, 19, 1, 2, 14],
        [19, 4, 7, 17, 14, 3, 12, 8, 6, 18, 9, 10, 2, 11, 1, 16, 0, 13, 5, 15],
        [11, 4, 7, 2, 15, 3, 0, 8, 12, 10, 5, 16, 19, 6, 13, 18, 17, 1, 14, 9],
        [17, 5, 11, 10, 3, 18, 6, 0, 15, 13, 16, 14, 19, 9, 12, 7, 4, 8, 2, 1],
        [4, 8, 18, 13, 3, 7, 15, 6, 0, 16, 19, 12, 9, 11, 17, 10, 5, 2, 1, 14],
        [3, 8, 6, 11, 12, 15, 4, 17, 13, 0, 16, 1, 10, 14, 19, 7, 18, 9, 5, 2],
        [10, 8, 12, 3, 1, 7, 15, 13, 16, 18, 2, 11, 17, 0, 6, 4, 14, 19, 5, 9],
        [0, 17, 18, 7, 10, 2, 1, 16, 13, 6, 5, 11, 14, 8, 4, 19, 3, 9, 15, 12],
        [3, 2, 4, 11, 16, 8, 12, 9, 15, 13, 14, 19, 5, 7, 6, 1, 17, 10, 0, 18],
        [6, 8, 7, 5, 10, 17, 12, 1, 9, 14, 13, 16, 15, 19, 4, 11, 3, 0, 18, 2],
        [2, 12, 16, 11, 0, 14, 4, 18, 8, 7, 5, 13, 10, 3, 9, 6, 19, 1, 17, 15],
        [17, 18, 6, 7, 0, 3, 15, 8, 1, 10, 9, 11, 14, 2, 5, 19, 16, 12, 4, 13],
        [12, 9, 8, 17, 2, 5, 14, 13, 10, 19, 18, 1, 3, 4, 11, 0, 6, 15, 16, 7],
        [6, 2, 13, 7, 16, 9, 4, 11, 12, 14, 15, 8, 19, 10, 18, 17, 5, 1, 0, 3],
        [0, 10, 12, 13, 6, 3, 15, 4, 16, 14, 9, 11, 2, 18, 1, 5, 7, 8, 17, 19],
        [3, 17, 15, 13, 19, 7, 12, 11, 6, 18, 8, 4, 0, 5, 16, 9, 14, 1, 2, 10],
        [16, 18, 10, 5, 4, 8, 15, 14, 3, 19, 0, 6, 9, 17, 12, 7, 2, 11, 1, 13],
        [10, 7, 13, 8, 6, 5, 16, 2, 18, 9, 3, 0, 1, 15, 12, 11, 19, 17, 4, 14],
        [1, 10, 7, 4, 19, 3, 5, 9, 13, 6, 15, 11, 17, 14, 2, 18, 16, 0, 8, 12],
        [14, 8, 5, 16, 0, 19, 9, 15, 18, 10, 4, 1, 17, 3, 11, 7, 12, 2, 6, 13],
        [15, 2, 8, 18, 13, 0, 6, 9, 17, 4, 3, 12, 10, 19, 14, 16, 11, 5, 1, 7],
        [0, 12, 15, 1, 10, 3, 4, 7, 9, 6, 19, 14, 17, 13, 2, 18, 5, 8, 16, 11],
        [9, 13, 15, 6, 17, 10, 8, 16, 1, 2, 4, 0, 19, 3, 5, 7, 11, 14, 12, 18],
        [4, 1, 2, 5, 18, 0, 7, 8, 14, 16, 13, 6, 11, 12, 3, 9, 15, 17, 10, 19],
        [4, 13, 17, 5, 10, 3, 2, 6, 14, 0, 16, 12, 9, 8, 15, 19, 7, 11, 1, 18],
        [4, 1, 3, 15, 6, 18, 9, 7, 19, 5, 10, 14, 2, 16, 13, 0, 8, 11, 17, 12],
        [13, 0, 19, 2, 5, 3, 6, 16, 12, 11, 17, 10, 9, 15, 8, 7, 14, 18, 1, 4],
        [0, 5, 14, 11, 1, 4, 12, 10, 15, 19, 8, 16, 2, 3, 18, 17, 13, 9, 6, 7],
        [8, 11, 6, 12, 18, 4, 16, 13, 0, 1, 19, 17, 3, 5, 2, 7, 9, 10, 15, 14],
        [6, 2, 0, 4, 14, 1, 18, 3, 9, 5, 11, 13, 12, 19, 7, 16, 15, 8, 10, 17],
        [1, 13, 19, 2, 18, 5, 7, 3, 8, 12, 15, 6, 4, 14, 16, 9, 11, 0, 10, 17],
        [2, 0, 1, 12, 7, 3, 8, 16, 14, 11, 19, 9, 4, 5, 6, 10, 15, 17, 18, 13],
        [0, 15, 3, 11, 17, 9, 16, 10, 12, 4, 7, 8, 18, 1, 14, 2, 13, 5, 19, 6],
        [10, 13, 6, 14, 2, 17, 15, 5, 18, 8, 9, 3, 4, 16, 11, 7, 1, 19, 12, 0],
        [14, 10, 17, 12, 5, 4, 7, 11, 13, 8, 0, 2, 16, 15, 18, 9, 19, 3, 6, 1],
        [17, 6, 12, 0, 16, 5, 9, 4, 7, 13, 11, 15, 18, 8, 1, 2, 3, 10, 19, 14],
        [9, 0, 6, 14, 2, 3, 12, 7, 5, 16, 19, 1, 10, 8, 18, 11, 13, 17, 4, 15],
        [19, 15, 12, 17, 18, 14, 13, 4, 1, 0, 6, 2, 9, 8, 11, 7, 16, 3, 5, 10],
        [11, 13, 10, 9, 2, 8, 5, 4, 6, 18, 17, 14, 7, 12, 16, 19, 3, 15, 0, 1],
        [8, 0, 12, 10, 9, 13, 1, 3, 4, 17, 19, 18, 15, 11, 6, 5, 14, 7, 2, 16],
        [19, 8, 5, 18, 2, 14, 3, 15, 12, 4, 16, 0, 11, 13, 7, 1, 9, 6, 10, 17],
        [11, 16, 7, 14, 15, 19, 1, 13, 2, 17, 9, 3, 6, 4, 10, 0, 5, 8, 18, 12],
        [11, 3, 14, 0, 17, 4, 15, 13, 2, 8, 18, 1, 12, 19, 5, 10, 16, 9, 6, 7],
        [13, 4, 18, 11, 15, 0, 16, 3, 19, 17, 1, 8, 14, 5, 12, 6, 9, 2, 10, 7],
        [7, 13, 4, 19, 0, 8, 15, 5, 1, 18, 16, 3, 11, 9, 12, 10, 17, 14, 2, 6],
        [8, 11, 7, 18, 4, 0, 6, 9, 5, 13, 17, 10, 15, 12, 16, 2, 14, 19, 3, 1],
        [15, 3, 8, 11, 17, 16, 9, 14, 6, 10, 1, 4, 18, 12, 13, 0, 7, 19, 2, 5],
        [5, 7, 11, 18, 10, 1, 16, 13, 4, 9, 6, 14, 8, 19, 0, 12, 2, 3, 15, 17],
        [11, 9, 6, 8, 18, 7, 1, 4, 17, 10, 3, 15, 12, 19, 16, 2, 13, 5, 14, 0],
        [10, 3, 4, 15, 16, 1, 2, 14, 7, 11, 19, 13, 0, 12, 6, 17, 18, 8, 5, 9],
        [17, 5, 11, 2, 13, 0, 7, 12, 6, 9, 4, 8, 14, 16, 1, 18, 19, 15, 10, 3],
        [4, 5, 0, 18, 9, 16, 19, 3, 1, 2, 17, 6, 8, 13, 10, 11, 12, 14, 7, 15],
        [10, 13, 5, 0, 7, 16, 4, 19, 9, 2, 11, 17, 14, 15, 18, 3, 8, 1, 6, 12],
        [0, 4, 6, 3, 15, 5, 2, 10, 11, 14, 13, 17, 16, 8, 9, 18, 19, 1, 7, 12],
        [15, 12, 19, 13, 11, 18, 4, 16, 5, 17, 2, 8, 7, 14, 0, 9, 10, 6, 1, 3],
        [6, 5, 15, 2, 9, 4, 1, 19, 17, 10, 0, 11, 12, 14, 7, 8, 16, 3, 18, 13],
        [18, 7, 4, 17, 16, 9, 8, 3, 12, 14, 6, 19, 2, 15, 10, 0, 1, 5, 13, 11],
        [10, 9, 5, 1, 14, 19, 0, 18, 3, 7, 16, 6, 4, 2, 12, 13, 15, 8, 11, 17],
        [17, 15, 16, 4, 13, 1, 9, 10, 11, 19, 0, 5, 14, 8, 12, 7, 2, 3, 18, 6],
        [19, 11, 13, 6, 4, 18, 1, 12, 17, 9, 3, 14, 0, 8, 10, 7, 5, 16, 15, 2],
        [7, 8, 1, 15, 14, 5, 3, 11, 2, 19, 4, 6, 18, 12, 16, 17, 9, 10, 13, 0],
        [5, 7, 4, 16, 2, 19, 18, 10, 0, 1, 11, 8, 17, 13, 14, 12, 9, 3, 6, 15],
        [9, 5, 18, 16, 7, 15, 8, 0, 3, 6, 12, 1, 10, 14, 13, 19, 17, 4, 11, 2],
        [15, 8, 9, 17, 1, 14, 3, 12, 5, 16, 6, 11, 10, 4, 13, 18, 7, 2, 0, 19],
        [12, 0, 10, 11, 2, 9, 7, 5, 16, 13, 6, 15, 3, 8, 14, 19, 18, 1, 17, 4],
        [14, 15, 8, 16, 5, 11, 12, 0, 9, 3, 18, 17, 13, 6, 4, 19, 1, 10, 7, 2],
        [7, 18, 0, 14, 12, 17, 8, 10, 16, 4, 19, 13, 2, 15, 6, 3, 1, 9, 11, 5],
    ],
    'durations': [
        # Job 0
        [Interval(1, 1), Interval(29, 35), Interval(14, 16), Interval(15, 15), Interval(67, 77),
         Interval(36, 46), Interval(42, 56), Interval(17, 17), Interval(11, 13), Interval(34, 44),
         Interval(60, 72), Interval(58, 70), Interval(10, 10), Interval(21, 27), Interval(58, 62),
         Interval(69, 83), Interval(67, 77), Interval(44, 50), Interval(85, 113), Interval(79, 105)],
        # Job 1
        [Interval(25, 31), Interval(60, 64), Interval(62, 66), Interval(95, 95), Interval(84, 104),
         Interval(85, 87), Interval(84, 90), Interval(11, 11), Interval(42, 50), Interval(63, 65),
         Interval(74, 98), Interval(69, 83), Interval(10, 12), Interval(29, 35), Interval(44, 44),
         Interval(30, 32), Interval(72, 82), Interval(88, 110), Interval(14, 18), Interval(97, 97)],
        # Job 2
        [Interval(71, 85), Interval(25, 31), Interval(2, 2), Interval(3, 3), Interval(83, 93),
         Interval(63, 75), Interval(34, 34), Interval(89, 109), Interval(33, 33), Interval(60, 80),
         Interval(17, 19), Interval(22, 22), Interval(37, 45), Interval(20, 20), Interval(20, 22),
         Interval(40, 48), Interval(65, 67), Interval(18, 18), Interval(64, 82), Interval(77, 83)],
        # Job 3
        [Interval(19, 21), Interval(21, 23), Interval(74, 78), Interval(40, 46), Interval(51, 69),
         Interval(87, 95), Interval(75, 101), Interval(26, 26), Interval(11, 13), Interval(7, 9),
         Interval(60, 70), Interval(37, 41), Interval(45, 53), Interval(71, 95), Interval(27, 33),
         Interval(74, 82), Interval(19, 23), Interval(84, 108), Interval(6, 6), Interval(51, 61)],
        # Job 4
        [Interval(49, 63), Interval(49, 55), Interval(73, 73), Interval(19, 21), Interval(65, 87),
         Interval(69, 77), Interval(18, 24), Interval(18, 24), Interval(39, 41), Interval(61, 77),
         Interval(19, 19), Interval(92, 94), Interval(79, 105), Interval(66, 82), Interval(77, 99),
         Interval(72, 76), Interval(88, 102), Interval(43, 43), Interval(44, 56), Interval(69, 85)],
        # Job 5
        [Interval(78, 80), Interval(53, 61), Interval(61, 79), Interval(31, 37), Interval(28, 28),
         Interval(28, 28), Interval(82, 86), Interval(39, 41), Interval(6, 6), Interval(52, 54),
         Interval(36, 48), Interval(88, 110), Interval(7, 7), Interval(17, 19), Interval(21, 25),
         Interval(12, 12), Interval(83, 91), Interval(79, 93), Interval(13, 13), Interval(64, 68)],
        # Job 6
        [Interval(63, 71), Interval(2, 2), Interval(67, 71), Interval(85, 89), Interval(52, 60),
         Interval(20, 24), Interval(23, 25), Interval(60, 74), Interval(51, 69), Interval(7, 7),
         Interval(2, 2), Interval(62, 80), Interval(58, 68), Interval(62, 64), Interval(95, 103),
         Interval(69, 89), Interval(73, 95), Interval(7, 7), Interval(94, 100), Interval(75, 93)],
        # Job 7
        [Interval(17, 21), Interval(86, 110), Interval(65, 65), Interval(54, 58), Interval(20, 22),
         Interval(70, 92), Interval(87, 95), Interval(52, 52), Interval(74, 98), Interval(60, 68),
         Interval(2, 2), Interval(6, 6), Interval(81, 81), Interval(77, 85), Interval(5, 5),
         Interval(77, 91), Interval(80, 96), Interval(64, 76), Interval(66, 86), Interval(71, 73)],
        # Job 8
        [Interval(63, 83), Interval(71, 75), Interval(24, 24), Interval(24, 28), Interval(20, 24),
         Interval(47, 59), Interval(87, 101), Interval(75, 87), Interval(24, 26), Interval(49, 65),
         Interval(44, 50), Interval(86, 86), Interval(79, 79), Interval(86, 98), Interval(44, 46),
         Interval(15, 19), Interval(3, 3), Interval(11, 13), Interval(60, 60), Interval(54, 66)],
        # Job 9
        [Interval(58, 74), Interval(64, 78), Interval(66, 72), Interval(73, 81), Interval(86, 104),
         Interval(29, 31), Interval(41, 49), Interval(45, 47), Interval(31, 39), Interval(33, 33),
         Interval(95, 95), Interval(18, 22), Interval(26, 34), Interval(43, 57), Interval(87, 97),
         Interval(91, 103), Interval(99, 99), Interval(2, 2), Interval(2, 2), Interval(22, 26)],
        # Job 10
        [Interval(87, 95), Interval(78, 92), Interval(16, 16), Interval(80, 102), Interval(38, 42),
         Interval(57, 61), Interval(60, 68), Interval(29, 31), Interval(56, 68), Interval(94, 94),
         Interval(63, 71), Interval(75, 75), Interval(19, 25), Interval(44, 48), Interval(86, 108),
         Interval(35, 45), Interval(9, 9), Interval(37, 39), Interval(7, 7), Interval(93, 95)],
        # Job 11
        [Interval(95, 103), Interval(79, 85), Interval(82, 106), Interval(17, 23), Interval(40, 42),
         Interval(75, 95), Interval(19, 23), Interval(72, 88), Interval(48, 58), Interval(46, 54),
         Interval(72, 74), Interval(34, 40), Interval(78, 100), Interval(60, 60), Interval(30, 30),
         Interval(5, 5), Interval(9, 11), Interval(12, 12), Interval(34, 46), Interval(27, 31)],
        # Job 12
        [Interval(33, 35), Interval(26, 28), Interval(64, 86), Interval(68, 80), Interval(70, 94),
         Interval(8, 10), Interval(73, 77), Interval(85, 89), Interval(75, 87), Interval(12, 12),
         Interval(12, 12), Interval(23, 29), Interval(16, 20), Interval(78, 100), Interval(84, 84),
         Interval(85, 89), Interval(12, 16), Interval(88, 98), Interval(18, 22), Interval(78, 84)],
        # Job 13
        [Interval(86, 100), Interval(41, 55), Interval(57, 65), Interval(57, 57), Interval(79, 99),
         Interval(61, 63), Interval(51, 51), Interval(83, 95), Interval(40, 46), Interval(9, 9),
         Interval(67, 79), Interval(21, 27), Interval(15, 19), Interval(71, 75), Interval(11, 13),
         Interval(70, 82), Interval(67, 77), Interval(11, 11), Interval(30, 38), Interval(75, 75)],
        # Job 14
        [Interval(6, 8), Interval(60, 64), Interval(2, 2), Interval(24, 32), Interval(69, 77),
         Interval(52, 62), Interval(46, 56), Interval(69, 81), Interval(85, 87), Interval(22, 28),
         Interval(98, 98), Interval(61, 65), Interval(41, 41), Interval(58, 70), Interval(21, 27),
         Interval(59, 65), Interval(37, 43), Interval(19, 23), Interval(30, 38), Interval(42, 46)],
        # Job 15
        [Interval(71, 71), Interval(43, 45), Interval(63, 69), Interval(87, 99), Interval(60, 62),
         Interval(66, 66), Interval(36, 48), Interval(48, 54), Interval(30, 34), Interval(49, 55),
         Interval(29, 33), Interval(28, 32), Interval(60, 66), Interval(26, 32), Interval(86, 94),
         Interval(72, 78), Interval(80, 108), Interval(8, 10), Interval(39, 41), Interval(21, 23)],
        # Job 16
        [Interval(13, 15), Interval(44, 48), Interval(9, 11), Interval(52, 52), Interval(7, 7),
         Interval(1, 1), Interval(13, 13), Interval(71, 83), Interval(35, 39), Interval(63, 63),
         Interval(33, 41), Interval(54, 64), Interval(33, 33), Interval(28, 32), Interval(74, 82),
         Interval(35, 41), Interval(73, 81), Interval(11, 13), Interval(46, 46), Interval(33, 33)],
        # Job 17
        [Interval(65, 79), Interval(61, 81), Interval(80, 88), Interval(9, 11), Interval(90, 100),
         Interval(22, 26), Interval(17, 19), Interval(48, 64), Interval(3, 3), Interval(46, 52),
         Interval(70, 84), Interval(17, 21), Interval(69, 71), Interval(22, 26), Interval(44, 56),
         Interval(17, 21), Interval(51, 69), Interval(40, 50), Interval(66, 88), Interval(6, 6)],
        # Job 18
        [Interval(10, 12), Interval(17, 23), Interval(12, 12), Interval(54, 68), Interval(95, 103),
         Interval(28, 30), Interval(34, 42), Interval(71, 81), Interval(48, 48), Interval(51, 61),
         Interval(92, 104), Interval(73, 87), Interval(45, 59), Interval(26, 34), Interval(22, 24),
         Interval(55, 63), Interval(61, 71), Interval(4, 4), Interval(40, 46), Interval(24, 28)],
        # Job 19
        [Interval(68, 92), Interval(68, 74), Interval(48, 52), Interval(63, 75), Interval(25, 29),
         Interval(49, 59), Interval(4, 4), Interval(58, 62), Interval(83, 103), Interval(1, 1),
         Interval(65, 87), Interval(10, 12), Interval(87, 89), Interval(77, 97), Interval(41, 43),
         Interval(70, 76), Interval(83, 91), Interval(36, 44), Interval(14, 16), Interval(64, 80)],
        # Job 20
        [Interval(72, 86), Interval(4, 4), Interval(7, 9), Interval(64, 66), Interval(63, 81),
         Interval(70, 70), Interval(64, 74), Interval(89, 109), Interval(1, 1), Interval(73, 73),
         Interval(57, 57), Interval(50, 54), Interval(74, 86), Interval(80, 90), Interval(57, 59),
         Interval(7, 9), Interval(31, 31), Interval(83, 99), Interval(86, 92), Interval(54, 66)],
        # Job 21
        [Interval(81, 95), Interval(35, 43), Interval(70, 70), Interval(57, 73), Interval(77, 79),
         Interval(8, 10), Interval(58, 72), Interval(52, 56), Interval(90, 102), Interval(13, 15),
         Interval(43, 49), Interval(49, 53), Interval(62, 66), Interval(53, 57), Interval(52, 60),
         Interval(6, 6), Interval(2, 2), Interval(15, 15), Interval(46, 60), Interval(20, 20)],
        # Job 22
        [Interval(50, 64), Interval(37, 41), Interval(76, 80), Interval(61, 81), Interval(88, 94),
         Interval(49, 65), Interval(65, 81), Interval(31, 41), Interval(70, 92), Interval(80, 104),
         Interval(59, 59), Interval(7, 9), Interval(23, 25), Interval(41, 55), Interval(76, 100),
         Interval(68, 70), Interval(42, 56), Interval(51, 59), Interval(7, 7), Interval(79, 85)],
        # Job 23
        [Interval(31, 31), Interval(49, 63), Interval(85, 109), Interval(88, 108), Interval(18, 18),
         Interval(48, 62), Interval(69, 69), Interval(33, 33), Interval(67, 79), Interval(4, 4),
         Interval(40, 48), Interval(95, 99), Interval(65, 87), Interval(21, 21), Interval(36, 42),
         Interval(68, 78), Interval(82, 88), Interval(28, 32), Interval(57, 73), Interval(13, 17)],
        # Job 24
        [Interval(2, 2), Interval(65, 87), Interval(81, 107), Interval(57, 67), Interval(26, 30),
         Interval(91, 91), Interval(35, 39), Interval(55, 69), Interval(44, 54), Interval(31, 37),
         Interval(71, 71), Interval(62, 68), Interval(52, 60), Interval(77, 79), Interval(10, 10),
         Interval(47, 57), Interval(39, 47), Interval(85, 99), Interval(29, 39), Interval(55, 61)],
        # Job 25
        [Interval(25, 31), Interval(71, 87), Interval(39, 41), Interval(44, 44), Interval(29, 37),
         Interval(2, 2), Interval(73, 97), Interval(53, 53), Interval(19, 19), Interval(61, 81),
         Interval(14, 18), Interval(8, 8), Interval(36, 40), Interval(51, 53), Interval(92, 104),
         Interval(30, 30), Interval(13, 17), Interval(5, 5), Interval(14, 18), Interval(82, 94)],
        # Job 26
        [Interval(87, 91), Interval(36, 36), Interval(2, 2), Interval(37, 47), Interval(64, 84),
         Interval(81, 97), Interval(66, 72), Interval(12, 14), Interval(13, 15), Interval(82, 84),
         Interval(40, 52), Interval(75, 81), Interval(64, 74), Interval(46, 50), Interval(62, 66),
         Interval(59, 69), Interval(2, 2), Interval(32, 36), Interval(35, 41), Interval(35, 45)],
        # Job 27
        [Interval(27, 33), Interval(91, 93), Interval(45, 51), Interval(90, 96), Interval(68, 80),
         Interval(68, 74), Interval(78, 92), Interval(23, 27), Interval(94, 102), Interval(66, 76),
         Interval(1, 1), Interval(72, 94), Interval(7, 9), Interval(68, 78), Interval(42, 46),
         Interval(24, 28), Interval(35, 41), Interval(61, 75), Interval(8, 10), Interval(59, 67)],
        # Job 28
        [Interval(42, 48), Interval(69, 85), Interval(10, 12), Interval(46, 52), Interval(53, 55),
         Interval(88, 98), Interval(42, 42), Interval(39, 47), Interval(51, 63), Interval(15, 19),
         Interval(61, 61), Interval(8, 10), Interval(65, 65), Interval(30, 34), Interval(24, 32),
         Interval(53, 53), Interval(54, 72), Interval(15, 19), Interval(61, 71), Interval(65, 67)],
        # Job 29
        [Interval(55, 59), Interval(4, 4), Interval(27, 33), Interval(29, 37), Interval(93, 105),
         Interval(4, 4), Interval(46, 56), Interval(39, 45), Interval(70, 82), Interval(44, 44),
         Interval(16, 16), Interval(89, 91), Interval(80, 98), Interval(80, 102), Interval(57, 65),
         Interval(75, 87), Interval(85, 87), Interval(86, 98), Interval(7, 7), Interval(6, 8)],
        # Job 30
        [Interval(31, 35), Interval(54, 62), Interval(21, 23), Interval(20, 24), Interval(63, 63),
         Interval(7, 7), Interval(22, 22), Interval(76, 80), Interval(72, 96), Interval(94, 96),
         Interval(75, 91), Interval(7, 7), Interval(57, 75), Interval(32, 38), Interval(8, 10),
         Interval(28, 30), Interval(38, 48), Interval(76, 100), Interval(92, 98), Interval(6, 8)],
        # Job 31
        [Interval(87, 89), Interval(45, 59), Interval(18, 18), Interval(41, 51), Interval(8, 8),
         Interval(5, 5), Interval(70, 82), Interval(18, 22), Interval(17, 21), Interval(61, 81),
         Interval(29, 31), Interval(20, 24), Interval(57, 57), Interval(47, 59), Interval(89, 93),
         Interval(63, 73), Interval(8, 8), Interval(43, 51), Interval(69, 93), Interval(31, 35)],
        # Job 32
        [Interval(43, 53), Interval(47, 59), Interval(33, 35), Interval(55, 67), Interval(20, 26),
         Interval(11, 11), Interval(5, 5), Interval(81, 81), Interval(26, 34), Interval(23, 27),
         Interval(12, 14), Interval(60, 76), Interval(9, 9), Interval(37, 39), Interval(6, 6),
         Interval(99, 99), Interval(17, 19), Interval(17, 21), Interval(51, 55), Interval(75, 87)],
        # Job 33
        [Interval(47, 53), Interval(3, 3), Interval(56, 66), Interval(76, 100), Interval(89, 107),
         Interval(54, 58), Interval(86, 98), Interval(82, 92), Interval(29, 39), Interval(25, 33),
         Interval(84, 94), Interval(72, 88), Interval(86, 106), Interval(25, 27), Interval(36, 46),
         Interval(93, 101), Interval(64, 68), Interval(49, 49), Interval(17, 21), Interval(30, 36)],
        # Job 34
        [Interval(59, 59), Interval(65, 67), Interval(25, 27), Interval(8, 8), Interval(40, 42),
         Interval(59, 67), Interval(69, 69), Interval(58, 70), Interval(55, 61), Interval(2, 2),
         Interval(84, 100), Interval(25, 27), Interval(13, 13), Interval(36, 44), Interval(77, 99),
         Interval(29, 39), Interval(8, 8), Interval(44, 46), Interval(81, 107), Interval(67, 77)],
        # Job 35
        [Interval(40, 52), Interval(88, 102), Interval(31, 41), Interval(25, 27), Interval(69, 89),
         Interval(67, 85), Interval(37, 37), Interval(65, 81), Interval(37, 45), Interval(85, 103),
         Interval(82, 82), Interval(31, 41), Interval(41, 55), Interval(91, 101), Interval(65, 81),
         Interval(79, 79), Interval(30, 30), Interval(13, 17), Interval(87, 87), Interval(30, 38)],
        # Job 36
        [Interval(30, 30), Interval(16, 18), Interval(88, 100), Interval(77, 87), Interval(38, 50),
         Interval(69, 87), Interval(87, 107), Interval(95, 103), Interval(77, 87), Interval(74, 100),
         Interval(55, 57), Interval(80, 94), Interval(39, 45), Interval(50, 54), Interval(77, 97),
         Interval(15, 15), Interval(1, 1), Interval(2, 2), Interval(87, 93), Interval(70, 72)],
        # Job 37
        [Interval(38, 42), Interval(13, 13), Interval(6, 6), Interval(41, 45), Interval(46, 46),
         Interval(73, 95), Interval(63, 69), Interval(14, 14), Interval(66, 66), Interval(14, 18),
         Interval(83, 105), Interval(63, 63), Interval(16, 16), Interval(31, 41), Interval(35, 45),
         Interval(42, 56), Interval(51, 55), Interval(32, 36), Interval(60, 60), Interval(7, 9)],
        # Job 38
        [Interval(1, 1), Interval(36, 44), Interval(53, 65), Interval(76, 90), Interval(59, 79),
         Interval(71, 81), Interval(36, 40), Interval(44, 48), Interval(58, 72), Interval(56, 74),
         Interval(52, 70), Interval(63, 83), Interval(2, 2), Interval(58, 68), Interval(17, 23),
         Interval(71, 77), Interval(45, 45), Interval(40, 40), Interval(70, 82), Interval(70, 70)],
        # Job 39
        [Interval(34, 40), Interval(4, 4), Interval(31, 35), Interval(79, 81), Interval(38, 44),
         Interval(65, 83), Interval(67, 67), Interval(24, 30), Interval(74, 92), Interval(2, 2),
         Interval(49, 55), Interval(52, 54), Interval(59, 59), Interval(27, 27), Interval(15, 15),
         Interval(38, 50), Interval(44, 46), Interval(17, 17), Interval(54, 56), Interval(52, 66)],
        # Job 40
        [Interval(10, 10), Interval(8, 10), Interval(17, 21), Interval(56, 64), Interval(84, 92),
         Interval(80, 96), Interval(27, 31), Interval(53, 67), Interval(46, 50), Interval(83, 87),
         Interval(87, 91), Interval(45, 49), Interval(98, 98), Interval(15, 17), Interval(9, 9),
         Interval(93, 103), Interval(45, 59), Interval(86, 104), Interval(44, 54), Interval(89, 103)],
        # Job 41
        [Interval(74, 80), Interval(84, 108), Interval(64, 76), Interval(19, 19), Interval(38, 42),
         Interval(89, 105), Interval(11, 13), Interval(58, 68), Interval(74, 90), Interval(6, 8),
         Interval(71, 81), Interval(85, 101), Interval(77, 95), Interval(72, 92), Interval(44, 48),
         Interval(17, 21), Interval(43, 51), Interval(77, 103), Interval(45, 45), Interval(11, 11)],
        # Job 42
        [Interval(58, 76), Interval(40, 44), Interval(15, 19), Interval(54, 56), Interval(59, 59),
         Interval(48, 52), Interval(54, 62), Interval(77, 101), Interval(81, 99), Interval(47, 51),
         Interval(83, 89), Interval(18, 22), Interval(38, 44), Interval(17, 21), Interval(48, 58),
         Interval(88, 100), Interval(85, 89), Interval(63, 63), Interval(50, 56), Interval(21, 21)],
        # Job 43
        [Interval(18, 22), Interval(62, 78), Interval(19, 21), Interval(67, 75), Interval(35, 43),
         Interval(33, 37), Interval(17, 21), Interval(84, 96), Interval(53, 67), Interval(21, 27),
         Interval(76, 78), Interval(51, 67), Interval(52, 58), Interval(17, 17), Interval(32, 38),
         Interval(73, 81), Interval(84, 102), Interval(31, 35), Interval(51, 69), Interval(15, 17)],
        # Job 44
        [Interval(47, 59), Interval(43, 49), Interval(12, 12), Interval(18, 24), Interval(17, 23),
         Interval(19, 25), Interval(25, 29), Interval(36, 40), Interval(39, 47), Interval(62, 70),
         Interval(34, 42), Interval(91, 105), Interval(53, 57), Interval(40, 42), Interval(88, 110),
         Interval(16, 18), Interval(83, 99), Interval(73, 73), Interval(23, 25), Interval(51, 67)],
        # Job 45
        [Interval(5, 5), Interval(72, 92), Interval(31, 33), Interval(25, 31), Interval(43, 43),
         Interval(46, 54), Interval(83, 87), Interval(56, 60), Interval(13, 13), Interval(44, 56),
         Interval(18, 22), Interval(46, 56), Interval(16, 18), Interval(54, 54), Interval(15, 17),
         Interval(20, 20), Interval(91, 105), Interval(45, 45), Interval(79, 95), Interval(54, 58)],
        # Job 46
        [Interval(65, 83), Interval(7, 9), Interval(17, 23), Interval(55, 71), Interval(93, 93),
         Interval(20, 24), Interval(85, 89), Interval(63, 69), Interval(8, 10), Interval(4, 4),
         Interval(7, 7), Interval(30, 30), Interval(84, 100), Interval(33, 39), Interval(65, 71),
         Interval(77, 79), Interval(6, 6), Interval(48, 48), Interval(73, 97), Interval(26, 26)],
        # Job 47
        [Interval(41, 47), Interval(4, 4), Interval(14, 18), Interval(69, 75), Interval(66, 74),
         Interval(46, 58), Interval(82, 88), Interval(71, 87), Interval(68, 90), Interval(70, 82),
         Interval(60, 68), Interval(70, 72), Interval(83, 83), Interval(36, 38), Interval(81, 87),
         Interval(11, 11), Interval(22, 22), Interval(24, 32), Interval(2, 2), Interval(55, 59)],
        # Job 48
        [Interval(77, 95), Interval(42, 48), Interval(12, 14), Interval(3, 3), Interval(23, 25),
         Interval(46, 48), Interval(30, 30), Interval(18, 20), Interval(15, 19), Interval(24, 26),
         Interval(81, 103), Interval(73, 77), Interval(92, 100), Interval(23, 25), Interval(15, 17),
         Interval(73, 75), Interval(58, 76), Interval(64, 76), Interval(42, 42), Interval(83, 97)],
        # Job 49
        [Interval(44, 50), Interval(6, 6), Interval(17, 21), Interval(33, 43), Interval(11, 13),
         Interval(80, 106), Interval(49, 61), Interval(59, 67), Interval(40, 42), Interval(14, 14),
         Interval(3, 3), Interval(10, 12), Interval(65, 87), Interval(29, 35), Interval(83, 83),
         Interval(29, 37), Interval(2, 2), Interval(73, 79), Interval(65, 81), Interval(23, 31)],
        # Job 50
        [Interval(58, 58), Interval(2, 2), Interval(73, 81), Interval(70, 74), Interval(90, 106),
         Interval(58, 62), Interval(37, 39), Interval(43, 45), Interval(62, 72), Interval(1, 1),
         Interval(52, 62), Interval(44, 52), Interval(35, 39), Interval(88, 90), Interval(74, 88),
         Interval(70, 88), Interval(81, 81), Interval(29, 37), Interval(19, 25), Interval(32, 34)],
        # Job 51
        [Interval(26, 26), Interval(14, 16), Interval(15, 19), Interval(9, 9), Interval(85, 97),
         Interval(39, 41), Interval(17, 19), Interval(6, 6), Interval(45, 53), Interval(90, 90),
         Interval(10, 12), Interval(68, 68), Interval(26, 26), Interval(57, 77), Interval(12, 16),
         Interval(86, 102), Interval(79, 91), Interval(90, 102), Interval(10, 12), Interval(86, 108)],
        # Job 52
        [Interval(14, 16), Interval(3, 3), Interval(51, 51), Interval(13, 17), Interval(63, 75),
         Interval(11, 13), Interval(22, 24), Interval(31, 35), Interval(65, 67), Interval(22, 26),
         Interval(40, 48), Interval(73, 83), Interval(48, 48), Interval(50, 50), Interval(80, 98),
         Interval(6, 6), Interval(52, 64), Interval(18, 22), Interval(5, 5), Interval(61, 77)],
        # Job 53
        [Interval(61, 63), Interval(49, 55), Interval(18, 20), Interval(92, 92), Interval(35, 45),
         Interval(1, 1), Interval(87, 107), Interval(53, 59), Interval(73, 75), Interval(42, 50),
         Interval(31, 35), Interval(30, 36), Interval(27, 29), Interval(82, 86), Interval(49, 53),
         Interval(22, 28), Interval(58, 60), Interval(87, 93), Interval(33, 43), Interval(59, 59)],
        # Job 54
        [Interval(61, 67), Interval(36, 38), Interval(2, 2), Interval(9, 9), Interval(6, 6),
         Interval(30, 38), Interval(1, 1), Interval(39, 45), Interval(87, 97), Interval(60, 62),
         Interval(46, 50), Interval(54, 68), Interval(60, 64), Interval(10, 12), Interval(69, 87),
         Interval(28, 30), Interval(40, 40), Interval(13, 17), Interval(59, 63), Interval(38, 40)],
        # Job 55
        [Interval(76, 86), Interval(8, 10), Interval(4, 4), Interval(59, 75), Interval(31, 39),
         Interval(80, 98), Interval(6, 8), Interval(1, 1), Interval(47, 63), Interval(3, 3),
         Interval(11, 11), Interval(30, 40), Interval(58, 74), Interval(19, 19), Interval(28, 28),
         Interval(59, 79), Interval(20, 24), Interval(3, 3), Interval(39, 45), Interval(56, 56)],
        # Job 56
        [Interval(86, 96), Interval(26, 26), Interval(5, 5), Interval(93, 103), Interval(10, 10),
         Interval(66, 78), Interval(75, 81), Interval(74, 88), Interval(11, 11), Interval(51, 51),
         Interval(57, 69), Interval(70, 90), Interval(25, 33), Interval(63, 63), Interval(63, 69),
         Interval(78, 82), Interval(3, 3), Interval(67, 69), Interval(50, 50), Interval(16, 16)],
        # Job 57
        [Interval(95, 95), Interval(38, 48), Interval(70, 70), Interval(11, 13), Interval(64, 82),
         Interval(10, 10), Interval(83, 93), Interval(81, 89), Interval(43, 43), Interval(50, 64),
         Interval(63, 77), Interval(15, 15), Interval(12, 14), Interval(49, 59), Interval(93, 99),
         Interval(93, 105), Interval(18, 18), Interval(58, 70), Interval(75, 95), Interval(53, 53)],
        # Job 58
        [Interval(47, 49), Interval(15, 17), Interval(52, 60), Interval(8, 10), Interval(57, 75),
         Interval(73, 93), Interval(25, 27), Interval(38, 42), Interval(26, 30), Interval(68, 78),
         Interval(69, 89), Interval(47, 47), Interval(81, 83), Interval(51, 67), Interval(62, 66),
         Interval(32, 42), Interval(73, 85), Interval(25, 29), Interval(6, 6), Interval(97, 101)],
        # Job 59
        [Interval(87, 111), Interval(31, 35), Interval(77, 93), Interval(24, 30), Interval(89, 97),
         Interval(3, 3), Interval(50, 62), Interval(11, 11), Interval(77, 85), Interval(41, 43),
         Interval(10, 10), Interval(67, 79), Interval(23, 31), Interval(52, 66), Interval(17, 19),
         Interval(1, 1), Interval(55, 69), Interval(54, 56), Interval(52, 66), Interval(51, 69)],
        # Job 60
        [Interval(6, 6), Interval(60, 74), Interval(38, 46), Interval(38, 40), Interval(12, 16),
         Interval(34, 44), Interval(43, 55), Interval(12, 12), Interval(88, 94), Interval(64, 70),
         Interval(84, 98), Interval(60, 78), Interval(38, 38), Interval(13, 13), Interval(40, 40),
         Interval(36, 42), Interval(4, 4), Interval(53, 57), Interval(2, 2), Interval(83, 87)],
        # Job 61
        [Interval(79, 87), Interval(13, 17), Interval(16, 20), Interval(8, 10), Interval(86, 88),
         Interval(58, 74), Interval(22, 26), Interval(2, 2), Interval(81, 99), Interval(52, 56),
         Interval(25, 31), Interval(87, 87), Interval(49, 51), Interval(76, 76), Interval(53, 65),
         Interval(28, 28), Interval(48, 58), Interval(79, 79), Interval(8, 10), Interval(31, 31)],
        # Job 62
        [Interval(64, 78), Interval(86, 98), Interval(38, 38), Interval(6, 6), Interval(80, 92),
         Interval(17, 17), Interval(21, 23), Interval(86, 90), Interval(73, 87), Interval(4, 4),
         Interval(12, 14), Interval(82, 82), Interval(39, 49), Interval(69, 73), Interval(7, 7),
         Interval(35, 37), Interval(43, 43), Interval(10, 10), Interval(59, 71), Interval(18, 24)],
        # Job 63
        [Interval(42, 56), Interval(46, 54), Interval(54, 66), Interval(55, 71), Interval(50, 52),
         Interval(55, 69), Interval(4, 4), Interval(82, 90), Interval(23, 31), Interval(29, 35),
         Interval(31, 33), Interval(62, 70), Interval(4, 4), Interval(4, 4), Interval(20, 26),
         Interval(92, 106), Interval(94, 104), Interval(73, 83), Interval(2, 2), Interval(35, 41)],
        # Job 64
        [Interval(40, 54), Interval(75, 77), Interval(6, 8), Interval(56, 68), Interval(31, 33),
         Interval(59, 69), Interval(24, 32), Interval(41, 49), Interval(65, 65), Interval(84, 98),
         Interval(31, 41), Interval(39, 49), Interval(75, 85), Interval(5, 5), Interval(6, 8),
         Interval(17, 23), Interval(47, 61), Interval(75, 99), Interval(77, 93), Interval(5, 5)],
        # Job 65
        [Interval(2, 2), Interval(76, 80), Interval(76, 80), Interval(38, 40), Interval(93, 95),
         Interval(84, 104), Interval(83, 83), Interval(45, 47), Interval(94, 100), Interval(18, 20),
         Interval(64, 64), Interval(92, 100), Interval(20, 24), Interval(42, 52), Interval(30, 34),
         Interval(70, 72), Interval(84, 102), Interval(89, 95), Interval(13, 13), Interval(9, 9)],
        # Job 66
        [Interval(50, 52), Interval(47, 49), Interval(52, 68), Interval(88, 110), Interval(52, 54),
         Interval(35, 35), Interval(18, 20), Interval(76, 80), Interval(58, 72), Interval(64, 80),
         Interval(71, 73), Interval(59, 61), Interval(86, 98), Interval(14, 16), Interval(61, 61),
         Interval(25, 33), Interval(87, 111), Interval(70, 78), Interval(53, 53), Interval(11, 11)],
        # Job 67
        [Interval(39, 43), Interval(54, 54), Interval(17, 17), Interval(80, 102), Interval(44, 52),
         Interval(77, 83), Interval(84, 106), Interval(76, 92), Interval(12, 14), Interval(80, 102),
         Interval(41, 47), Interval(80, 82), Interval(68, 80), Interval(44, 44), Interval(30, 34),
         Interval(8, 10), Interval(4, 4), Interval(12, 14), Interval(54, 66), Interval(83, 83)],
        # Job 68
        [Interval(12, 14), Interval(4, 4), Interval(23, 23), Interval(73, 95), Interval(40, 42),
         Interval(69, 77), Interval(70, 84), Interval(22, 24), Interval(16, 16), Interval(48, 64),
         Interval(19, 19), Interval(55, 71), Interval(62, 82), Interval(32, 38), Interval(57, 67),
         Interval(43, 47), Interval(45, 55), Interval(89, 89), Interval(37, 39), Interval(68, 84)],
        # Job 69
        [Interval(15, 19), Interval(98, 98), Interval(19, 25), Interval(79, 93), Interval(29, 35),
         Interval(85, 99), Interval(2, 2), Interval(26, 28), Interval(45, 59), Interval(41, 41),
         Interval(10, 12), Interval(41, 51), Interval(86, 108), Interval(39, 51), Interval(89, 95),
         Interval(54, 56), Interval(57, 59), Interval(84, 106), Interval(55, 61), Interval(17, 23)],
        # Job 70
        [Interval(52, 52), Interval(84, 96), Interval(37, 37), Interval(63, 63), Interval(25, 25),
         Interval(2, 2), Interval(45, 55), Interval(53, 53), Interval(57, 77), Interval(20, 22),
         Interval(82, 90), Interval(83, 97), Interval(30, 32), Interval(59, 59), Interval(40, 50),
         Interval(5, 5), Interval(66, 84), Interval(90, 96), Interval(24, 32), Interval(8, 8)],
        # Job 71
        [Interval(16, 18), Interval(89, 91), Interval(77, 83), Interval(79, 101), Interval(63, 81),
         Interval(30, 32), Interval(6, 6), Interval(75, 95), Interval(27, 33), Interval(52, 68),
         Interval(61, 77), Interval(84, 98), Interval(23, 31), Interval(28, 30), Interval(19, 23),
         Interval(32, 40), Interval(12, 14), Interval(73, 75), Interval(56, 64), Interval(11, 11)],
        # Job 72
        [Interval(73, 75), Interval(70, 90), Interval(87, 99), Interval(88, 94), Interval(54, 66),
         Interval(7, 9), Interval(85, 107), Interval(61, 61), Interval(63, 83), Interval(25, 29),
         Interval(62, 62), Interval(71, 85), Interval(43, 47), Interval(74, 80), Interval(60, 64),
         Interval(77, 89), Interval(23, 27), Interval(67, 75), Interval(10, 12), Interval(57, 59)],
        # Job 73
        [Interval(84, 112), Interval(30, 34), Interval(87, 107), Interval(23, 29), Interval(16, 16),
         Interval(57, 73), Interval(16, 16), Interval(93, 101), Interval(5, 5), Interval(4, 4),
         Interval(87, 103), Interval(10, 10), Interval(75, 101), Interval(31, 39), Interval(74, 80),
         Interval(34, 38), Interval(43, 45), Interval(65, 87), Interval(66, 84), Interval(12, 16)],
        # Job 74
        [Interval(4, 4), Interval(43, 51), Interval(68, 74), Interval(29, 35), Interval(19, 21),
         Interval(47, 61), Interval(78, 96), Interval(52, 66), Interval(5, 5), Interval(9, 11),
         Interval(42, 44), Interval(13, 13), Interval(22, 26), Interval(7, 9), Interval(24, 30),
         Interval(29, 37), Interval(49, 63), Interval(12, 14), Interval(33, 33), Interval(35, 35)],
        # Job 75
        [Interval(17, 17), Interval(17, 21), Interval(64, 78), Interval(90, 92), Interval(20, 26),
         Interval(24, 26), Interval(41, 49), Interval(61, 77), Interval(78, 94), Interval(81, 101),
         Interval(86, 104), Interval(34, 38), Interval(9, 9), Interval(24, 26), Interval(47, 49),
         Interval(87, 111), Interval(74, 100), Interval(50, 54), Interval(19, 19), Interval(60, 74)],
        # Job 76
        [Interval(63, 81), Interval(16, 20), Interval(89, 93), Interval(62, 76), Interval(12, 14),
         Interval(41, 45), Interval(68, 92), Interval(63, 63), Interval(40, 42), Interval(78, 86),
         Interval(18, 22), Interval(28, 34), Interval(76, 90), Interval(53, 57), Interval(87, 91),
         Interval(5, 5), Interval(63, 73), Interval(36, 40), Interval(69, 93), Interval(37, 45)],
        # Job 77
        [Interval(49, 57), Interval(55, 71), Interval(33, 37), Interval(62, 76), Interval(30, 32),
         Interval(37, 41), Interval(19, 23), Interval(91, 103), Interval(31, 31), Interval(10, 12),
         Interval(70, 82), Interval(25, 33), Interval(77, 99), Interval(58, 78), Interval(86, 106),
         Interval(74, 84), Interval(35, 39), Interval(9, 9), Interval(68, 92), Interval(85, 91)],
        # Job 78
        [Interval(99, 99), Interval(7, 9), Interval(83, 85), Interval(70, 70), Interval(39, 51),
         Interval(88, 94), Interval(9, 11), Interval(83, 111), Interval(80, 108), Interval(68, 78),
         Interval(31, 35), Interval(17, 23), Interval(72, 84), Interval(39, 47), Interval(30, 38),
         Interval(92, 92), Interval(34, 44), Interval(34, 38), Interval(48, 50), Interval(66, 80)],
        # Job 79
        [Interval(17, 21), Interval(15, 17), Interval(68, 70), Interval(82, 110), Interval(41, 45),
         Interval(8, 8), Interval(64, 76), Interval(8, 10), Interval(17, 19), Interval(35, 47),
         Interval(78, 100), Interval(38, 42), Interval(88, 88), Interval(88, 90), Interval(66, 68),
         Interval(58, 58), Interval(34, 44), Interval(44, 44), Interval(31, 35), Interval(17, 17)],
        # Job 80
        [Interval(31, 39), Interval(65, 87), Interval(17, 21), Interval(56, 58), Interval(74, 90),
         Interval(94, 104), Interval(10, 12), Interval(34, 44), Interval(30, 32), Interval(24, 26),
         Interval(57, 73), Interval(2, 2), Interval(77, 77), Interval(70, 70), Interval(64, 72),
         Interval(23, 27), Interval(67, 81), Interval(46, 46), Interval(27, 35), Interval(27, 35)],
        # Job 81
        [Interval(43, 47), Interval(55, 67), Interval(50, 58), Interval(65, 79), Interval(31, 39),
         Interval(63, 73), Interval(89, 89), Interval(19, 19), Interval(59, 79), Interval(10, 10),
         Interval(70, 78), Interval(48, 64), Interval(64, 64), Interval(10, 12), Interval(12, 12),
         Interval(42, 42), Interval(86, 98), Interval(82, 82), Interval(55, 65), Interval(18, 20)],
        # Job 82
        [Interval(22, 24), Interval(67, 79), Interval(24, 28), Interval(4, 4), Interval(24, 26),
         Interval(6, 6), Interval(31, 35), Interval(29, 29), Interval(10, 12), Interval(78, 86),
         Interval(28, 30), Interval(48, 58), Interval(71, 95), Interval(56, 66), Interval(26, 26),
         Interval(68, 90), Interval(83, 111), Interval(82, 104), Interval(28, 36), Interval(61, 61)],
        # Job 83
        [Interval(62, 76), Interval(79, 93), Interval(37, 49), Interval(10, 12), Interval(24, 26),
         Interval(67, 85), Interval(57, 57), Interval(33, 35), Interval(58, 70), Interval(31, 35),
         Interval(66, 70), Interval(79, 101), Interval(60, 66), Interval(35, 41), Interval(43, 45),
         Interval(45, 59), Interval(8, 10), Interval(50, 56), Interval(6, 8), Interval(69, 85)],
        # Job 84
        [Interval(47, 61), Interval(57, 67), Interval(36, 48), Interval(57, 69), Interval(82, 92),
         Interval(91, 105), Interval(84, 104), Interval(65, 75), Interval(25, 27), Interval(12, 16),
         Interval(4, 4), Interval(82, 88), Interval(38, 50), Interval(62, 80), Interval(20, 22),
         Interval(36, 38), Interval(26, 34), Interval(46, 46), Interval(2, 2), Interval(76, 76)],
        # Job 85
        [Interval(13, 13), Interval(6, 8), Interval(18, 20), Interval(4, 4), Interval(35, 43),
         Interval(55, 59), Interval(47, 57), Interval(91, 105), Interval(27, 27), Interval(54, 54),
         Interval(67, 87), Interval(73, 91), Interval(62, 70), Interval(92, 100), Interval(41, 45),
         Interval(72, 84), Interval(3, 3), Interval(12, 12), Interval(57, 65), Interval(60, 74)],
        # Job 86
        [Interval(51, 51), Interval(48, 50), Interval(75, 77), Interval(26, 34), Interval(18, 24),
         Interval(88, 108), Interval(22, 22), Interval(64, 64), Interval(42, 48), Interval(13, 15),
         Interval(1, 1), Interval(72, 86), Interval(68, 70), Interval(14, 14), Interval(62, 80),
         Interval(77, 77), Interval(66, 82), Interval(65, 65), Interval(54, 60), Interval(58, 68)],
        # Job 87
        [Interval(16, 16), Interval(8, 10), Interval(30, 30), Interval(55, 69), Interval(22, 24),
         Interval(44, 50), Interval(30, 32), Interval(21, 23), Interval(49, 61), Interval(99, 99),
         Interval(49, 51), Interval(37, 47), Interval(17, 19), Interval(43, 55), Interval(68, 76),
         Interval(53, 59), Interval(46, 62), Interval(89, 101), Interval(62, 76), Interval(86, 100)],
        # Job 88
        [Interval(34, 34), Interval(87, 93), Interval(83, 89), Interval(45, 45), Interval(5, 5),
         Interval(98, 100), Interval(74, 84), Interval(84, 106), Interval(81, 109), Interval(82, 82),
         Interval(83, 107), Interval(37, 49), Interval(33, 35), Interval(86, 104), Interval(49, 55),
         Interval(43, 49), Interval(64, 68), Interval(12, 14), Interval(42, 44), Interval(43, 51)],
        # Job 89
        [Interval(66, 78), Interval(3, 3), Interval(72, 78), Interval(31, 33), Interval(47, 55),
         Interval(53, 61), Interval(60, 64), Interval(48, 54), Interval(2, 2), Interval(97, 99),
         Interval(63, 63), Interval(57, 63), Interval(90, 96), Interval(49, 63), Interval(53, 53),
         Interval(83, 97), Interval(86, 100), Interval(41, 53), Interval(68, 88), Interval(28, 34)],
        # Job 90
        [Interval(13, 13), Interval(85, 89), Interval(24, 28), Interval(72, 74), Interval(33, 41),
         Interval(64, 66), Interval(30, 38), Interval(67, 87), Interval(43, 49), Interval(29, 37),
         Interval(74, 82), Interval(50, 52), Interval(5, 5), Interval(73, 73), Interval(36, 46),
         Interval(67, 75), Interval(70, 78), Interval(42, 46), Interval(47, 49), Interval(51, 53)],
        # Job 91
        [Interval(18, 22), Interval(37, 43), Interval(27, 29), Interval(53, 63), Interval(32, 32),
         Interval(66, 80), Interval(66, 86), Interval(81, 87), Interval(27, 35), Interval(36, 40),
         Interval(86, 98), Interval(12, 14), Interval(39, 45), Interval(67, 85), Interval(46, 62),
         Interval(4, 4), Interval(65, 87), Interval(7, 7), Interval(37, 43), Interval(24, 32)],
        # Job 92
        [Interval(32, 42), Interval(77, 81), Interval(68, 72), Interval(42, 56), Interval(36, 44),
         Interval(23, 27), Interval(45, 57), Interval(59, 73), Interval(27, 27), Interval(93, 95),
         Interval(36, 38), Interval(34, 36), Interval(25, 31), Interval(79, 91), Interval(79, 89),
         Interval(32, 42), Interval(42, 52), Interval(51, 55), Interval(74, 90), Interval(84, 88)],
        # Job 93
        [Interval(82, 94), Interval(87, 107), Interval(91, 107), Interval(81, 81), Interval(45, 51),
         Interval(3, 3), Interval(60, 74), Interval(62, 62), Interval(40, 42), Interval(50, 56),
         Interval(67, 69), Interval(64, 76), Interval(44, 52), Interval(96, 100), Interval(36, 36),
         Interval(29, 29), Interval(36, 40), Interval(1, 1), Interval(12, 14), Interval(74, 92)],
        # Job 94
        [Interval(26, 26), Interval(81, 83), Interval(50, 66), Interval(12, 14), Interval(84, 100),
         Interval(31, 39), Interval(47, 63), Interval(77, 99), Interval(32, 32), Interval(69, 81),
         Interval(81, 89), Interval(94, 102), Interval(10, 12), Interval(38, 40), Interval(74, 74),
         Interval(59, 63), Interval(54, 60), Interval(59, 59), Interval(62, 64), Interval(46, 60)],
        # Job 95
        [Interval(69, 71), Interval(24, 32), Interval(97, 97), Interval(73, 89), Interval(54, 54),
         Interval(59, 61), Interval(64, 78), Interval(14, 16), Interval(87, 87), Interval(23, 27),
         Interval(85, 103), Interval(34, 44), Interval(20, 20), Interval(74, 74), Interval(47, 51),
         Interval(79, 85), Interval(46, 48), Interval(56, 68), Interval(5, 5), Interval(23, 25)],
        # Job 96
        [Interval(6, 6), Interval(7, 9), Interval(52, 52), Interval(37, 45), Interval(29, 37),
         Interval(50, 54), Interval(27, 29), Interval(59, 63), Interval(79, 93), Interval(76, 100),
         Interval(65, 67), Interval(12, 14), Interval(60, 68), Interval(82, 106), Interval(9, 11),
         Interval(9, 9), Interval(74, 84), Interval(54, 58), Interval(11, 13), Interval(69, 79)],
        # Job 97
        [Interval(68, 72), Interval(94, 104), Interval(89, 109), Interval(25, 25), Interval(6, 8),
         Interval(38, 48), Interval(85, 91), Interval(67, 83), Interval(63, 85), Interval(38, 50),
         Interval(39, 49), Interval(72, 88), Interval(38, 44), Interval(64, 84), Interval(56, 58),
         Interval(78, 90), Interval(19, 19), Interval(26, 28), Interval(22, 28), Interval(77, 79)],
        # Job 98
        [Interval(57, 71), Interval(83, 93), Interval(44, 46), Interval(51, 57), Interval(42, 50),
         Interval(47, 59), Interval(7, 7), Interval(94, 98), Interval(35, 39), Interval(82, 102),
         Interval(10, 12), Interval(36, 40), Interval(67, 71), Interval(82, 104), Interval(89, 91),
         Interval(28, 28), Interval(45, 53), Interval(70, 86), Interval(85, 107), Interval(40, 50)],
        # Job 99
        [Interval(37, 49), Interval(86, 86), Interval(13, 17), Interval(1, 1), Interval(46, 56),
         Interval(7, 7), Interval(86, 104), Interval(77, 83), Interval(91, 103), Interval(3, 3),
         Interval(74, 74), Interval(93, 101), Interval(70, 70), Interval(88, 90), Interval(61, 67),
         Interval(86, 108), Interval(36, 44), Interval(32, 32), Interval(49, 55), Interval(61, 67)],
    ],
    'name': 'INT__TAI100_20_07.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai100_20_07_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI100_20_07.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI100_20_07.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI100_20_07_F_15_01_INTERVAL_DATA
