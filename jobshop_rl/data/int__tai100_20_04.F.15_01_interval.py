"""
Problema INT__TAI100_20_04.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI100_20_04_F_15_01_INTERVAL_DATA = {
    'num_jobs': 100,
    'num_machines': 20,
    'problem_id': 'int__tai100_20_04.F.15_01_interval',
    'sequences': [
        [17, 16, 7, 0, 2, 5, 13, 15, 9, 10, 3, 1, 19, 12, 14, 6, 4, 11, 18, 8],
        [12, 3, 19, 13, 2, 7, 16, 17, 6, 14, 9, 5, 1, 0, 18, 4, 10, 8, 15, 11],
        [17, 0, 18, 10, 2, 1, 6, 4, 14, 8, 12, 15, 13, 3, 16, 5, 11, 7, 19, 9],
        [8, 14, 7, 0, 13, 12, 2, 10, 3, 9, 1, 17, 11, 16, 4, 19, 15, 6, 5, 18],
        [13, 0, 7, 16, 6, 12, 2, 4, 5, 11, 18, 14, 10, 1, 19, 8, 3, 9, 17, 15],
        [11, 1, 18, 6, 17, 16, 0, 19, 7, 10, 3, 2, 5, 13, 4, 9, 14, 12, 8, 15],
        [19, 2, 4, 11, 18, 14, 16, 10, 5, 3, 13, 0, 7, 6, 12, 15, 17, 1, 9, 8],
        [4, 17, 19, 11, 13, 16, 0, 10, 18, 7, 5, 9, 6, 12, 15, 14, 8, 2, 1, 3],
        [12, 3, 11, 7, 9, 17, 19, 15, 4, 18, 0, 14, 1, 8, 2, 5, 13, 10, 6, 16],
        [11, 0, 15, 14, 8, 17, 12, 16, 9, 18, 1, 7, 2, 19, 6, 10, 13, 4, 5, 3],
        [6, 8, 12, 15, 16, 4, 19, 2, 18, 11, 0, 10, 14, 3, 9, 7, 17, 5, 13, 1],
        [9, 1, 3, 14, 13, 7, 8, 17, 19, 12, 4, 18, 5, 2, 11, 6, 10, 16, 0, 15],
        [18, 1, 9, 3, 4, 0, 14, 2, 15, 8, 16, 10, 13, 17, 5, 7, 11, 19, 12, 6],
        [9, 12, 10, 14, 13, 17, 18, 4, 11, 3, 6, 1, 15, 7, 19, 0, 16, 5, 2, 8],
        [3, 8, 9, 10, 5, 2, 19, 0, 16, 6, 17, 11, 15, 4, 1, 7, 18, 12, 13, 14],
        [7, 16, 10, 8, 13, 3, 0, 5, 11, 17, 9, 15, 4, 1, 6, 12, 2, 19, 18, 14],
        [0, 18, 9, 6, 7, 3, 2, 11, 16, 4, 14, 17, 19, 5, 10, 8, 13, 15, 12, 1],
        [16, 9, 15, 5, 0, 7, 8, 18, 13, 2, 17, 19, 10, 4, 14, 12, 6, 11, 1, 3],
        [8, 10, 14, 7, 0, 19, 3, 9, 15, 5, 12, 13, 18, 16, 17, 2, 6, 11, 4, 1],
        [12, 9, 5, 1, 10, 18, 2, 7, 8, 11, 14, 4, 15, 17, 3, 13, 16, 19, 0, 6],
        [7, 15, 8, 17, 6, 14, 19, 18, 5, 9, 12, 2, 0, 4, 1, 3, 13, 11, 10, 16],
        [4, 10, 2, 13, 11, 18, 6, 19, 16, 8, 15, 14, 12, 17, 9, 5, 1, 3, 7, 0],
        [13, 9, 16, 17, 4, 10, 5, 19, 3, 14, 0, 6, 8, 12, 7, 2, 11, 18, 1, 15],
        [3, 16, 13, 1, 6, 7, 12, 9, 17, 11, 18, 14, 19, 4, 8, 2, 0, 15, 5, 10],
        [2, 3, 13, 10, 15, 14, 12, 1, 17, 4, 7, 11, 0, 18, 6, 16, 9, 8, 19, 5],
        [12, 19, 18, 1, 14, 16, 0, 10, 4, 5, 3, 9, 13, 8, 7, 11, 2, 6, 17, 15],
        [9, 11, 14, 16, 13, 0, 12, 10, 4, 2, 15, 5, 17, 19, 6, 1, 7, 3, 18, 8],
        [17, 6, 16, 7, 19, 12, 0, 18, 13, 2, 1, 11, 8, 14, 5, 3, 9, 15, 10, 4],
        [12, 11, 6, 5, 7, 19, 2, 17, 3, 15, 9, 13, 14, 8, 10, 16, 1, 0, 18, 4],
        [7, 12, 10, 13, 5, 11, 8, 0, 3, 1, 19, 9, 6, 2, 14, 15, 18, 4, 16, 17],
        [3, 12, 9, 10, 2, 0, 1, 6, 17, 15, 4, 11, 13, 16, 18, 8, 19, 7, 14, 5],
        [16, 18, 10, 17, 19, 8, 15, 7, 11, 6, 14, 4, 2, 12, 1, 9, 5, 13, 0, 3],
        [14, 18, 1, 17, 8, 12, 13, 15, 5, 3, 9, 7, 6, 10, 2, 19, 0, 16, 4, 11],
        [0, 8, 2, 12, 15, 16, 7, 1, 4, 9, 5, 11, 13, 6, 18, 14, 19, 17, 10, 3],
        [12, 11, 5, 8, 2, 16, 9, 4, 15, 10, 7, 1, 13, 6, 14, 18, 0, 19, 17, 3],
        [12, 19, 10, 11, 17, 4, 5, 18, 14, 0, 16, 9, 1, 7, 15, 6, 8, 3, 13, 2],
        [13, 3, 11, 16, 4, 8, 17, 0, 6, 2, 7, 10, 5, 9, 15, 1, 12, 14, 19, 18],
        [10, 13, 19, 8, 0, 9, 7, 15, 18, 17, 4, 1, 12, 3, 11, 14, 5, 6, 16, 2],
        [19, 8, 10, 3, 7, 15, 14, 5, 0, 11, 2, 9, 17, 1, 12, 16, 6, 18, 4, 13],
        [2, 15, 4, 0, 13, 10, 19, 18, 12, 9, 7, 5, 14, 1, 8, 17, 11, 16, 6, 3],
        [14, 8, 17, 15, 11, 1, 5, 10, 6, 9, 19, 7, 2, 4, 18, 13, 16, 3, 0, 12],
        [4, 3, 5, 6, 9, 18, 19, 2, 11, 15, 17, 0, 8, 16, 12, 1, 13, 14, 10, 7],
        [12, 8, 17, 19, 10, 13, 5, 14, 7, 6, 1, 2, 18, 3, 15, 11, 9, 0, 4, 16],
        [18, 4, 0, 8, 13, 6, 3, 2, 9, 17, 1, 11, 15, 12, 16, 10, 5, 7, 19, 14],
        [10, 13, 7, 0, 15, 6, 11, 8, 14, 2, 5, 3, 9, 16, 1, 4, 19, 18, 17, 12],
        [12, 5, 14, 18, 8, 0, 7, 2, 10, 16, 9, 6, 1, 17, 11, 4, 15, 19, 3, 13],
        [5, 2, 11, 18, 12, 15, 0, 3, 17, 19, 13, 9, 7, 6, 16, 10, 14, 1, 4, 8],
        [3, 1, 10, 9, 2, 15, 13, 12, 5, 0, 7, 19, 11, 17, 4, 8, 18, 14, 6, 16],
        [8, 3, 18, 9, 15, 0, 13, 10, 11, 19, 14, 16, 7, 2, 1, 12, 4, 6, 17, 5],
        [17, 2, 10, 9, 14, 16, 6, 1, 15, 8, 13, 7, 5, 11, 0, 4, 12, 18, 19, 3],
        [10, 9, 12, 5, 7, 4, 19, 0, 14, 11, 2, 6, 1, 3, 15, 16, 13, 18, 8, 17],
        [5, 9, 14, 3, 12, 17, 4, 11, 2, 19, 6, 15, 10, 0, 18, 7, 1, 8, 16, 13],
        [2, 13, 15, 4, 10, 5, 9, 0, 17, 11, 7, 18, 3, 16, 8, 14, 19, 6, 12, 1],
        [18, 6, 5, 19, 7, 16, 13, 4, 15, 14, 10, 8, 12, 17, 0, 11, 2, 9, 3, 1],
        [7, 1, 2, 17, 16, 10, 9, 6, 5, 15, 12, 8, 14, 3, 0, 19, 13, 11, 4, 18],
        [14, 8, 10, 15, 17, 4, 9, 7, 1, 3, 19, 0, 13, 2, 16, 5, 11, 6, 12, 18],
        [18, 4, 5, 2, 11, 17, 19, 14, 16, 15, 1, 7, 13, 9, 3, 10, 8, 0, 12, 6],
        [13, 14, 0, 8, 19, 15, 16, 6, 17, 4, 18, 10, 9, 5, 2, 11, 12, 3, 1, 7],
        [11, 15, 19, 8, 6, 12, 3, 18, 13, 4, 10, 14, 5, 9, 7, 17, 2, 16, 1, 0],
        [1, 10, 4, 13, 14, 9, 7, 19, 3, 17, 0, 8, 18, 11, 2, 5, 15, 6, 16, 12],
        [18, 2, 4, 3, 5, 19, 16, 10, 6, 17, 8, 13, 12, 0, 1, 9, 15, 14, 11, 7],
        [18, 7, 10, 11, 6, 16, 5, 9, 13, 4, 1, 19, 3, 14, 15, 17, 0, 8, 2, 12],
        [9, 1, 10, 0, 11, 8, 19, 7, 15, 6, 12, 13, 16, 4, 17, 18, 2, 14, 3, 5],
        [5, 9, 10, 7, 0, 4, 15, 13, 16, 2, 19, 3, 12, 11, 18, 14, 1, 8, 17, 6],
        [10, 3, 15, 17, 2, 6, 14, 19, 12, 8, 16, 13, 0, 11, 4, 1, 5, 9, 18, 7],
        [1, 0, 7, 19, 16, 17, 5, 8, 18, 15, 12, 3, 11, 4, 10, 13, 6, 14, 2, 9],
        [16, 2, 8, 5, 14, 9, 1, 4, 12, 10, 15, 13, 17, 7, 3, 19, 0, 6, 18, 11],
        [18, 12, 1, 3, 14, 2, 11, 10, 0, 13, 15, 8, 7, 5, 9, 19, 16, 6, 4, 17],
        [12, 10, 19, 2, 9, 16, 6, 17, 7, 15, 3, 4, 5, 1, 14, 11, 18, 0, 13, 8],
        [12, 9, 8, 6, 7, 0, 1, 11, 10, 18, 3, 14, 13, 17, 16, 5, 15, 2, 19, 4],
        [13, 9, 8, 11, 10, 15, 0, 18, 1, 5, 7, 4, 17, 2, 12, 16, 14, 6, 19, 3],
        [2, 12, 6, 4, 19, 7, 10, 1, 16, 17, 18, 3, 15, 11, 13, 8, 9, 0, 14, 5],
        [17, 11, 3, 15, 5, 13, 16, 9, 14, 10, 6, 2, 0, 19, 12, 8, 4, 18, 7, 1],
        [19, 6, 3, 5, 16, 14, 10, 4, 1, 11, 7, 9, 12, 17, 15, 18, 8, 13, 0, 2],
        [14, 6, 4, 0, 2, 12, 10, 8, 15, 7, 3, 16, 19, 1, 17, 9, 13, 5, 11, 18],
        [2, 1, 6, 7, 18, 16, 15, 14, 4, 11, 8, 9, 19, 0, 10, 13, 3, 5, 17, 12],
        [3, 11, 15, 19, 7, 2, 17, 18, 8, 4, 14, 1, 6, 10, 13, 9, 16, 0, 12, 5],
        [9, 19, 8, 10, 17, 6, 4, 15, 13, 1, 14, 16, 11, 18, 5, 0, 7, 12, 3, 2],
        [7, 2, 1, 3, 11, 15, 0, 9, 14, 10, 13, 16, 17, 6, 19, 12, 5, 18, 4, 8],
        [17, 13, 9, 2, 3, 8, 5, 10, 15, 16, 6, 4, 1, 7, 19, 11, 0, 18, 14, 12],
        [2, 13, 14, 10, 15, 18, 1, 11, 16, 19, 8, 12, 7, 0, 3, 5, 6, 9, 17, 4],
        [0, 17, 5, 9, 2, 8, 4, 15, 7, 14, 3, 12, 6, 1, 10, 13, 16, 11, 18, 19],
        [8, 11, 0, 15, 13, 14, 4, 7, 19, 12, 1, 3, 9, 10, 17, 2, 18, 16, 5, 6],
        [7, 8, 18, 12, 6, 14, 13, 16, 3, 10, 15, 5, 9, 1, 2, 11, 19, 17, 4, 0],
        [16, 15, 18, 11, 2, 14, 8, 4, 1, 9, 19, 3, 10, 7, 6, 13, 17, 0, 5, 12],
        [16, 11, 19, 18, 12, 0, 7, 4, 6, 13, 10, 15, 8, 1, 2, 5, 3, 14, 9, 17],
        [7, 15, 5, 2, 6, 13, 18, 0, 3, 12, 8, 9, 10, 17, 1, 14, 4, 16, 11, 19],
        [2, 17, 9, 8, 5, 4, 12, 1, 18, 11, 0, 15, 16, 14, 10, 3, 7, 19, 13, 6],
        [16, 19, 0, 2, 14, 5, 9, 12, 18, 13, 3, 10, 17, 15, 7, 6, 11, 8, 1, 4],
        [14, 17, 16, 18, 0, 6, 13, 9, 3, 4, 19, 10, 1, 15, 2, 8, 11, 12, 7, 5],
        [6, 15, 17, 11, 1, 16, 5, 9, 13, 10, 4, 2, 8, 12, 7, 14, 3, 19, 0, 18],
        [8, 19, 15, 18, 16, 14, 7, 17, 3, 5, 13, 2, 1, 9, 0, 6, 10, 11, 4, 12],
        [19, 8, 13, 0, 18, 16, 15, 5, 11, 6, 9, 12, 4, 2, 7, 3, 10, 17, 1, 14],
        [19, 13, 17, 0, 16, 14, 9, 12, 18, 10, 5, 4, 2, 15, 8, 7, 11, 1, 3, 6],
        [17, 4, 15, 3, 16, 18, 8, 9, 10, 11, 14, 1, 6, 13, 0, 5, 19, 12, 2, 7],
        [5, 9, 15, 19, 16, 1, 3, 0, 12, 6, 11, 17, 13, 10, 18, 7, 2, 8, 14, 4],
        [6, 3, 16, 12, 15, 4, 11, 8, 5, 10, 18, 2, 14, 9, 17, 19, 7, 1, 0, 13],
        [13, 18, 15, 2, 12, 19, 14, 10, 6, 0, 1, 9, 17, 11, 7, 5, 3, 8, 4, 16],
        [11, 0, 4, 10, 7, 17, 16, 14, 2, 3, 5, 15, 12, 18, 8, 9, 6, 13, 19, 1],
        [9, 19, 1, 15, 18, 12, 2, 13, 11, 16, 7, 14, 10, 17, 4, 6, 0, 8, 3, 5],
    ],
    'durations': [
        # Job 0
        [Interval(15, 19), Interval(23, 27), Interval(63, 67), Interval(29, 33), Interval(71, 89),
         Interval(55, 73), Interval(29, 31), Interval(31, 41), Interval(86, 112), Interval(15, 17),
         Interval(29, 35), Interval(3, 3), Interval(27, 29), Interval(68, 90), Interval(1, 1),
         Interval(48, 52), Interval(85, 103), Interval(29, 33), Interval(81, 93), Interval(80, 108)],
        # Job 1
        [Interval(61, 81), Interval(77, 95), Interval(16, 16), Interval(76, 82), Interval(92, 92),
         Interval(71, 87), Interval(62, 64), Interval(10, 10), Interval(45, 49), Interval(58, 70),
         Interval(55, 57), Interval(4, 4), Interval(74, 100), Interval(15, 17), Interval(39, 47),
         Interval(64, 76), Interval(15, 15), Interval(26, 28), Interval(93, 105), Interval(33, 41)],
        # Job 2
        [Interval(71, 91), Interval(32, 32), Interval(69, 83), Interval(71, 89), Interval(18, 20),
         Interval(6, 6), Interval(34, 40), Interval(59, 59), Interval(7, 9), Interval(3, 3),
         Interval(40, 42), Interval(68, 90), Interval(7, 9), Interval(80, 86), Interval(62, 74),
         Interval(52, 54), Interval(28, 30), Interval(55, 67), Interval(24, 24), Interval(53, 53)],
        # Job 3
        [Interval(68, 88), Interval(95, 103), Interval(93, 101), Interval(19, 21), Interval(3, 3),
         Interval(1, 1), Interval(95, 99), Interval(86, 98), Interval(37, 49), Interval(11, 11),
         Interval(22, 28), Interval(30, 32), Interval(87, 109), Interval(63, 83), Interval(35, 41),
         Interval(66, 76), Interval(63, 75), Interval(61, 81), Interval(66, 80), Interval(2, 2)],
        # Job 4
        [Interval(86, 96), Interval(83, 97), Interval(85, 109), Interval(22, 26), Interval(7, 9),
         Interval(68, 76), Interval(54, 54), Interval(64, 70), Interval(54, 72), Interval(37, 41),
         Interval(66, 86), Interval(11, 13), Interval(1, 1), Interval(7, 7), Interval(41, 51),
         Interval(14, 14), Interval(54, 54), Interval(57, 75), Interval(49, 61), Interval(37, 47)],
        # Job 5
        [Interval(65, 69), Interval(12, 14), Interval(74, 74), Interval(34, 42), Interval(9, 11),
         Interval(66, 68), Interval(6, 6), Interval(47, 53), Interval(63, 81), Interval(86, 100),
         Interval(25, 25), Interval(72, 72), Interval(65, 67), Interval(69, 73), Interval(18, 18),
         Interval(66, 88), Interval(24, 30), Interval(19, 21), Interval(92, 102), Interval(16, 18)],
        # Job 6
        [Interval(82, 86), Interval(19, 19), Interval(6, 8), Interval(38, 42), Interval(71, 75),
         Interval(83, 95), Interval(82, 88), Interval(76, 80), Interval(27, 31), Interval(81, 97),
         Interval(9, 9), Interval(79, 97), Interval(37, 49), Interval(49, 55), Interval(31, 41),
         Interval(41, 47), Interval(76, 78), Interval(42, 46), Interval(72, 92), Interval(79, 101)],
        # Job 7
        [Interval(25, 29), Interval(85, 91), Interval(53, 65), Interval(70, 88), Interval(86, 110),
         Interval(66, 66), Interval(9, 9), Interval(1, 1), Interval(33, 37), Interval(59, 79),
         Interval(28, 30), Interval(67, 67), Interval(51, 69), Interval(40, 46), Interval(21, 21),
         Interval(19, 19), Interval(70, 82), Interval(50, 60), Interval(71, 83), Interval(13, 17)],
        # Job 8
        [Interval(43, 45), Interval(37, 49), Interval(65, 69), Interval(41, 41), Interval(81, 99),
         Interval(64, 78), Interval(33, 43), Interval(37, 41), Interval(72, 82), Interval(17, 19),
         Interval(11, 13), Interval(16, 18), Interval(10, 10), Interval(77, 77), Interval(46, 52),
         Interval(25, 25), Interval(74, 96), Interval(28, 32), Interval(14, 14), Interval(83, 101)],
        # Job 9
        [Interval(50, 64), Interval(37, 45), Interval(49, 53), Interval(39, 43), Interval(16, 18),
         Interval(87, 95), Interval(74, 90), Interval(66, 70), Interval(67, 85), Interval(13, 13),
         Interval(93, 93), Interval(11, 13), Interval(78, 102), Interval(50, 66), Interval(49, 55),
         Interval(78, 88), Interval(68, 68), Interval(3, 3), Interval(10, 12), Interval(38, 42)],
        # Job 10
        [Interval(58, 68), Interval(57, 61), Interval(16, 20), Interval(94, 104), Interval(75, 81),
         Interval(5, 5), Interval(14, 16), Interval(68, 74), Interval(54, 64), Interval(21, 21),
         Interval(55, 61), Interval(29, 29), Interval(51, 67), Interval(93, 103), Interval(2, 2),
         Interval(16, 20), Interval(76, 98), Interval(54, 56), Interval(79, 87), Interval(82, 88)],
        # Job 11
        [Interval(53, 55), Interval(55, 59), Interval(49, 53), Interval(22, 28), Interval(50, 64),
         Interval(45, 47), Interval(82, 104), Interval(53, 63), Interval(18, 22), Interval(4, 4),
         Interval(18, 20), Interval(83, 99), Interval(25, 25), Interval(80, 96), Interval(82, 106),
         Interval(52, 52), Interval(23, 23), Interval(4, 4), Interval(24, 30), Interval(62, 70)],
        # Job 12
        [Interval(63, 83), Interval(78, 90), Interval(82, 88), Interval(48, 52), Interval(52, 70),
         Interval(37, 43), Interval(81, 105), Interval(16, 18), Interval(83, 89), Interval(19, 19),
         Interval(46, 52), Interval(98, 98), Interval(71, 77), Interval(6, 6), Interval(24, 30),
         Interval(81, 101), Interval(51, 65), Interval(59, 59), Interval(22, 22), Interval(13, 17)],
        # Job 13
        [Interval(11, 11), Interval(50, 62), Interval(38, 40), Interval(18, 22), Interval(68, 90),
         Interval(52, 58), Interval(18, 18), Interval(35, 45), Interval(73, 75), Interval(91, 91),
         Interval(89, 101), Interval(61, 69), Interval(13, 13), Interval(24, 28), Interval(34, 46),
         Interval(78, 100), Interval(24, 26), Interval(29, 37), Interval(3, 3), Interval(19, 23)],
        # Job 14
        [Interval(47, 55), Interval(37, 37), Interval(43, 55), Interval(20, 20), Interval(46, 58),
         Interval(55, 59), Interval(15, 19), Interval(40, 44), Interval(45, 55), Interval(66, 82),
         Interval(31, 35), Interval(38, 38), Interval(14, 18), Interval(21, 21), Interval(34, 36),
         Interval(85, 85), Interval(6, 8), Interval(57, 75), Interval(64, 72), Interval(62, 70)],
        # Job 15
        [Interval(42, 52), Interval(24, 30), Interval(81, 91), Interval(19, 19), Interval(9, 9),
         Interval(22, 24), Interval(60, 68), Interval(32, 32), Interval(24, 24), Interval(12, 16),
         Interval(44, 50), Interval(74, 88), Interval(43, 47), Interval(79, 89), Interval(10, 10),
         Interval(24, 26), Interval(65, 83), Interval(78, 84), Interval(94, 102), Interval(68, 90)],
        # Job 16
        [Interval(83, 105), Interval(45, 47), Interval(60, 66), Interval(58, 70), Interval(69, 75),
         Interval(62, 78), Interval(86, 86), Interval(10, 10), Interval(11, 11), Interval(92, 106),
         Interval(88, 98), Interval(90, 90), Interval(4, 4), Interval(66, 84), Interval(78, 96),
         Interval(35, 35), Interval(43, 49), Interval(25, 29), Interval(85, 103), Interval(78, 88)],
        # Job 17
        [Interval(46, 60), Interval(33, 33), Interval(56, 56), Interval(17, 21), Interval(43, 57),
         Interval(78, 86), Interval(18, 22), Interval(47, 51), Interval(66, 80), Interval(20, 22),
         Interval(24, 32), Interval(38, 42), Interval(45, 53), Interval(72, 94), Interval(81, 83),
         Interval(14, 18), Interval(85, 109), Interval(77, 95), Interval(40, 52), Interval(40, 50)],
        # Job 18
        [Interval(23, 29), Interval(25, 33), Interval(31, 39), Interval(31, 31), Interval(63, 79),
         Interval(75, 81), Interval(36, 40), Interval(10, 12), Interval(25, 27), Interval(12, 12),
         Interval(63, 75), Interval(60, 68), Interval(1, 1), Interval(87, 105), Interval(31, 41),
         Interval(80, 106), Interval(50, 54), Interval(28, 32), Interval(20, 24), Interval(23, 27)],
        # Job 19
        [Interval(11, 13), Interval(84, 112), Interval(14, 14), Interval(36, 40), Interval(85, 103),
         Interval(71, 83), Interval(48, 56), Interval(91, 99), Interval(18, 22), Interval(66, 88),
         Interval(37, 47), Interval(28, 28), Interval(62, 76), Interval(86, 90), Interval(28, 30),
         Interval(18, 18), Interval(85, 105), Interval(68, 78), Interval(14, 18), Interval(31, 37)],
        # Job 20
        [Interval(19, 25), Interval(5, 5), Interval(31, 31), Interval(22, 28), Interval(8, 8),
         Interval(35, 41), Interval(15, 19), Interval(17, 17), Interval(13, 13), Interval(57, 61),
         Interval(33, 39), Interval(83, 93), Interval(56, 58), Interval(17, 21), Interval(56, 58),
         Interval(59, 71), Interval(85, 91), Interval(21, 25), Interval(48, 56), Interval(35, 45)],
        # Job 21
        [Interval(19, 19), Interval(29, 39), Interval(49, 49), Interval(40, 52), Interval(2, 2),
         Interval(40, 50), Interval(79, 85), Interval(7, 7), Interval(6, 8), Interval(46, 54),
         Interval(77, 85), Interval(1, 1), Interval(95, 103), Interval(88, 94), Interval(50, 58),
         Interval(4, 4), Interval(85, 89), Interval(25, 33), Interval(61, 65), Interval(40, 50)],
        # Job 22
        [Interval(34, 38), Interval(37, 39), Interval(80, 106), Interval(26, 28), Interval(24, 32),
         Interval(71, 91), Interval(2, 2), Interval(57, 75), Interval(24, 32), Interval(40, 52),
         Interval(96, 96), Interval(49, 61), Interval(94, 104), Interval(77, 103), Interval(5, 5),
         Interval(32, 42), Interval(18, 18), Interval(47, 63), Interval(73, 83), Interval(50, 56)],
        # Job 23
        [Interval(86, 92), Interval(93, 93), Interval(35, 45), Interval(67, 85), Interval(26, 32),
         Interval(59, 63), Interval(12, 14), Interval(95, 95), Interval(28, 28), Interval(3, 3),
         Interval(81, 97), Interval(25, 31), Interval(13, 13), Interval(54, 72), Interval(31, 33),
         Interval(46, 54), Interval(22, 26), Interval(61, 65), Interval(70, 82), Interval(40, 54)],
        # Job 24
        [Interval(38, 50), Interval(41, 55), Interval(28, 36), Interval(56, 66), Interval(80, 90),
         Interval(34, 34), Interval(20, 22), Interval(46, 58), Interval(59, 73), Interval(42, 52),
         Interval(30, 30), Interval(46, 52), Interval(81, 95), Interval(94, 96), Interval(89, 99),
         Interval(54, 64), Interval(70, 84), Interval(5, 5), Interval(73, 85), Interval(23, 31)],
        # Job 25
        [Interval(18, 20), Interval(57, 71), Interval(24, 30), Interval(29, 31), Interval(27, 27),
         Interval(49, 65), Interval(82, 110), Interval(36, 36), Interval(8, 8), Interval(66, 88),
         Interval(51, 67), Interval(34, 38), Interval(13, 13), Interval(94, 98), Interval(83, 93),
         Interval(47, 47), Interval(71, 89), Interval(28, 36), Interval(40, 46), Interval(91, 95)],
        # Job 26
        [Interval(73, 73), Interval(67, 83), Interval(32, 42), Interval(64, 76), Interval(86, 94),
         Interval(29, 39), Interval(83, 91), Interval(6, 6), Interval(58, 60), Interval(68, 90),
         Interval(11, 11), Interval(46, 54), Interval(45, 47), Interval(12, 12), Interval(35, 41),
         Interval(52, 58), Interval(14, 16), Interval(16, 20), Interval(72, 88), Interval(97, 99)],
        # Job 27
        [Interval(66, 74), Interval(87, 93), Interval(82, 96), Interval(4, 4), Interval(74, 80),
         Interval(29, 33), Interval(39, 47), Interval(83, 91), Interval(49, 55), Interval(54, 72),
         Interval(66, 84), Interval(19, 23), Interval(29, 31), Interval(63, 73), Interval(75, 87),
         Interval(80, 98), Interval(59, 77), Interval(41, 47), Interval(59, 67), Interval(46, 56)],
        # Job 28
        [Interval(63, 77), Interval(9, 9), Interval(51, 53), Interval(52, 58), Interval(91, 93),
         Interval(55, 65), Interval(35, 43), Interval(12, 14), Interval(68, 68), Interval(65, 79),
         Interval(79, 81), Interval(42, 48), Interval(24, 32), Interval(69, 69), Interval(41, 55),
         Interval(25, 33), Interval(39, 45), Interval(54, 56), Interval(43, 45), Interval(78, 98)],
        # Job 29
        [Interval(80, 102), Interval(26, 30), Interval(62, 74), Interval(46, 52), Interval(86, 102),
         Interval(86, 86), Interval(43, 43), Interval(43, 43), Interval(67, 83), Interval(86, 110),
         Interval(82, 94), Interval(62, 72), Interval(62, 64), Interval(32, 36), Interval(61, 61),
         Interval(74, 96), Interval(30, 34), Interval(90, 102), Interval(43, 47), Interval(46, 56)],
        # Job 30
        [Interval(90, 90), Interval(96, 98), Interval(52, 54), Interval(9, 9), Interval(54, 72),
         Interval(91, 93), Interval(16, 20), Interval(68, 68), Interval(47, 63), Interval(9, 11),
         Interval(69, 87), Interval(32, 36), Interval(51, 63), Interval(12, 14), Interval(62, 66),
         Interval(51, 67), Interval(56, 56), Interval(65, 87), Interval(41, 41), Interval(50, 62)],
        # Job 31
        [Interval(9, 9), Interval(41, 47), Interval(53, 65), Interval(52, 70), Interval(6, 6),
         Interval(57, 75), Interval(54, 58), Interval(37, 45), Interval(96, 98), Interval(35, 47),
         Interval(1, 1), Interval(21, 21), Interval(40, 46), Interval(74, 78), Interval(18, 22),
         Interval(63, 83), Interval(82, 94), Interval(88, 108), Interval(50, 62), Interval(26, 26)],
        # Job 32
        [Interval(82, 98), Interval(51, 69), Interval(40, 40), Interval(78, 78), Interval(45, 59),
         Interval(9, 11), Interval(43, 57), Interval(53, 69), Interval(93, 97), Interval(27, 29),
         Interval(38, 38), Interval(22, 26), Interval(45, 57), Interval(91, 101), Interval(84, 96),
         Interval(17, 19), Interval(71, 83), Interval(10, 12), Interval(39, 47), Interval(90, 96)],
        # Job 33
        [Interval(44, 50), Interval(29, 31), Interval(12, 14), Interval(55, 71), Interval(88, 98),
         Interval(38, 46), Interval(29, 35), Interval(12, 12), Interval(59, 73), Interval(90, 98),
         Interval(85, 93), Interval(25, 25), Interval(14, 18), Interval(85, 107), Interval(86, 88),
         Interval(39, 39), Interval(54, 62), Interval(8, 8), Interval(2, 2), Interval(17, 17)],
        # Job 34
        [Interval(47, 53), Interval(62, 62), Interval(82, 100), Interval(24, 26), Interval(18, 20),
         Interval(68, 78), Interval(94, 102), Interval(57, 69), Interval(83, 107), Interval(49, 65),
         Interval(65, 69), Interval(7, 7), Interval(66, 86), Interval(74, 84), Interval(77, 103),
         Interval(69, 81), Interval(36, 48), Interval(63, 69), Interval(78, 102), Interval(36, 46)],
        # Job 35
        [Interval(18, 18), Interval(88, 110), Interval(81, 97), Interval(39, 47), Interval(49, 49),
         Interval(7, 9), Interval(38, 50), Interval(32, 34), Interval(81, 101), Interval(39, 39),
         Interval(35, 37), Interval(63, 81), Interval(27, 27), Interval(62, 78), Interval(66, 66),
         Interval(78, 86), Interval(88, 100), Interval(43, 49), Interval(16, 20), Interval(86, 110)],
        # Job 36
        [Interval(41, 49), Interval(13, 13), Interval(25, 27), Interval(12, 16), Interval(29, 29),
         Interval(83, 97), Interval(56, 64), Interval(80, 88), Interval(74, 92), Interval(40, 42),
         Interval(7, 7), Interval(24, 24), Interval(70, 76), Interval(57, 59), Interval(87, 95),
         Interval(47, 47), Interval(71, 93), Interval(76, 86), Interval(65, 69), Interval(15, 15)],
        # Job 37
        [Interval(46, 58), Interval(70, 88), Interval(18, 18), Interval(3, 3), Interval(28, 30),
         Interval(76, 100), Interval(87, 107), Interval(47, 63), Interval(53, 57), Interval(14, 16),
         Interval(87, 87), Interval(16, 18), Interval(39, 47), Interval(52, 64), Interval(63, 75),
         Interval(57, 75), Interval(29, 33), Interval(41, 45), Interval(8, 8), Interval(2, 2)],
        # Job 38
        [Interval(76, 98), Interval(44, 58), Interval(56, 74), Interval(5, 5), Interval(29, 39),
         Interval(54, 62), Interval(8, 10), Interval(10, 10), Interval(30, 30), Interval(87, 87),
         Interval(57, 67), Interval(88, 90), Interval(71, 85), Interval(34, 40), Interval(93, 95),
         Interval(37, 43), Interval(44, 56), Interval(83, 83), Interval(67, 81), Interval(74, 92)],
        # Job 39
        [Interval(33, 37), Interval(33, 35), Interval(44, 44), Interval(65, 65), Interval(37, 37),
         Interval(5, 5), Interval(44, 58), Interval(26, 26), Interval(63, 67), Interval(16, 16),
         Interval(79, 101), Interval(39, 41), Interval(65, 87), Interval(46, 62), Interval(68, 76),
         Interval(26, 28), Interval(34, 40), Interval(69, 81), Interval(69, 85), Interval(85, 93)],
        # Job 40
        [Interval(15, 15), Interval(1, 1), Interval(42, 44), Interval(7, 7), Interval(64, 64),
         Interval(46, 54), Interval(26, 26), Interval(28, 30), Interval(12, 14), Interval(69, 83),
         Interval(8, 10), Interval(5, 5), Interval(79, 91), Interval(19, 19), Interval(20, 26),
         Interval(86, 104), Interval(74, 78), Interval(66, 72), Interval(44, 52), Interval(23, 29)],
        # Job 41
        [Interval(77, 91), Interval(38, 46), Interval(86, 112), Interval(24, 26), Interval(69, 81),
         Interval(83, 103), Interval(67, 85), Interval(54, 58), Interval(20, 26), Interval(80, 94),
         Interval(7, 9), Interval(2, 2), Interval(60, 60), Interval(78, 80), Interval(26, 34),
         Interval(15, 17), Interval(52, 70), Interval(16, 16), Interval(1, 1), Interval(31, 31)],
        # Job 42
        [Interval(86, 94), Interval(38, 44), Interval(17, 23), Interval(45, 55), Interval(36, 40),
         Interval(73, 79), Interval(61, 75), Interval(62, 70), Interval(73, 95), Interval(69, 85),
         Interval(28, 32), Interval(54, 56), Interval(50, 50), Interval(37, 43), Interval(98, 100),
         Interval(5, 5), Interval(25, 29), Interval(9, 11), Interval(31, 33), Interval(23, 25)],
        # Job 43
        [Interval(30, 36), Interval(75, 83), Interval(48, 62), Interval(65, 73), Interval(47, 59),
         Interval(44, 56), Interval(80, 82), Interval(24, 32), Interval(86, 96), Interval(54, 56),
         Interval(46, 54), Interval(28, 30), Interval(24, 30), Interval(9, 9), Interval(52, 70),
         Interval(26, 28), Interval(32, 40), Interval(40, 46), Interval(5, 5), Interval(55, 57)],
        # Job 44
        [Interval(63, 81), Interval(31, 41), Interval(23, 31), Interval(15, 17), Interval(47, 53),
         Interval(75, 89), Interval(8, 8), Interval(71, 87), Interval(74, 86), Interval(22, 22),
         Interval(61, 65), Interval(54, 68), Interval(24, 26), Interval(56, 66), Interval(71, 71),
         Interval(87, 99), Interval(38, 50), Interval(57, 73), Interval(68, 76), Interval(78, 98)],
        # Job 45
        [Interval(7, 7), Interval(17, 19), Interval(58, 60), Interval(42, 46), Interval(63, 65),
         Interval(82, 106), Interval(50, 60), Interval(18, 22), Interval(10, 12), Interval(77, 77),
         Interval(3, 3), Interval(25, 27), Interval(8, 8), Interval(19, 23), Interval(73, 73),
         Interval(73, 87), Interval(85, 93), Interval(47, 59), Interval(17, 21), Interval(81, 109)],
        # Job 46
        [Interval(31, 39), Interval(7, 7), Interval(88, 108), Interval(65, 67), Interval(15, 17),
         Interval(80, 98), Interval(6, 6), Interval(23, 25), Interval(18, 18), Interval(36, 42),
         Interval(47, 57), Interval(47, 51), Interval(52, 52), Interval(26, 26), Interval(10, 12),
         Interval(72, 74), Interval(85, 97), Interval(60, 78), Interval(95, 103), Interval(74, 84)],
        # Job 47
        [Interval(57, 73), Interval(23, 25), Interval(77, 97), Interval(73, 97), Interval(61, 71),
         Interval(93, 105), Interval(5, 5), Interval(29, 29), Interval(98, 98), Interval(17, 17),
         Interval(4, 4), Interval(47, 49), Interval(43, 47), Interval(26, 26), Interval(69, 91),
         Interval(5, 5), Interval(54, 58), Interval(47, 59), Interval(71, 81), Interval(35, 47)],
        # Job 48
        [Interval(37, 41), Interval(33, 35), Interval(46, 48), Interval(54, 66), Interval(18, 24),
         Interval(11, 11), Interval(41, 51), Interval(14, 14), Interval(57, 61), Interval(48, 54),
         Interval(6, 8), Interval(58, 58), Interval(43, 55), Interval(52, 62), Interval(71, 71),
         Interval(53, 61), Interval(44, 50), Interval(1, 1), Interval(74, 96), Interval(62, 82)],
        # Job 49
        [Interval(82, 104), Interval(75, 101), Interval(22, 26), Interval(30, 34), Interval(18, 18),
         Interval(43, 45), Interval(41, 55), Interval(16, 20), Interval(72, 88), Interval(67, 67),
         Interval(9, 11), Interval(9, 9), Interval(14, 18), Interval(30, 40), Interval(16, 16),
         Interval(10, 10), Interval(28, 30), Interval(65, 77), Interval(85, 93), Interval(84, 90)],
        # Job 50
        [Interval(35, 37), Interval(27, 31), Interval(32, 38), Interval(72, 84), Interval(16, 18),
         Interval(7, 7), Interval(35, 41), Interval(44, 56), Interval(6, 6), Interval(15, 15),
         Interval(12, 16), Interval(26, 34), Interval(35, 37), Interval(18, 18), Interval(56, 62),
         Interval(54, 72), Interval(91, 93), Interval(25, 27), Interval(45, 47), Interval(21, 25)],
        # Job 51
        [Interval(82, 98), Interval(11, 11), Interval(80, 94), Interval(34, 34), Interval(20, 20),
         Interval(1, 1), Interval(49, 65), Interval(26, 34), Interval(18, 20), Interval(23, 27),
         Interval(21, 23), Interval(30, 34), Interval(77, 95), Interval(30, 32), Interval(4, 4),
         Interval(54, 54), Interval(28, 36), Interval(16, 18), Interval(21, 27), Interval(64, 70)],
        # Job 52
        [Interval(85, 97), Interval(60, 62), Interval(48, 58), Interval(1, 1), Interval(60, 74),
         Interval(50, 56), Interval(86, 86), Interval(8, 8), Interval(11, 13), Interval(45, 57),
         Interval(81, 99), Interval(65, 81), Interval(43, 45), Interval(12, 12), Interval(83, 101),
         Interval(58, 58), Interval(50, 64), Interval(56, 70), Interval(77, 87), Interval(67, 69)],
        # Job 53
        [Interval(70, 84), Interval(44, 52), Interval(64, 80), Interval(86, 92), Interval(35, 37),
         Interval(22, 24), Interval(34, 44), Interval(44, 46), Interval(38, 40), Interval(74, 96),
         Interval(54, 54), Interval(66, 72), Interval(42, 46), Interval(88, 96), Interval(76, 96),
         Interval(39, 45), Interval(79, 87), Interval(84, 86), Interval(22, 24), Interval(52, 64)],
        # Job 54
        [Interval(15, 15), Interval(5, 5), Interval(60, 74), Interval(8, 10), Interval(7, 7),
         Interval(81, 81), Interval(4, 4), Interval(77, 95), Interval(72, 76), Interval(47, 51),
         Interval(25, 27), Interval(8, 10), Interval(23, 31), Interval(30, 36), Interval(46, 56),
         Interval(83, 107), Interval(28, 36), Interval(24, 24), Interval(27, 35), Interval(50, 66)],
        # Job 55
        [Interval(29, 31), Interval(90, 90), Interval(23, 31), Interval(15, 19), Interval(80, 90),
         Interval(27, 27), Interval(87, 97), Interval(11, 11), Interval(14, 16), Interval(59, 63),
         Interval(17, 19), Interval(33, 35), Interval(87, 105), Interval(53, 59), Interval(34, 34),
         Interval(40, 48), Interval(28, 36), Interval(1, 1), Interval(14, 18), Interval(55, 55)],
        # Job 56
        [Interval(20, 22), Interval(92, 98), Interval(79, 83), Interval(1, 1), Interval(65, 65),
         Interval(66, 72), Interval(24, 24), Interval(41, 53), Interval(92, 92), Interval(23, 27),
         Interval(19, 25), Interval(58, 62), Interval(59, 65), Interval(92, 102), Interval(78, 78),
         Interval(55, 71), Interval(16, 20), Interval(35, 35), Interval(69, 91), Interval(50, 60)],
        # Job 57
        [Interval(93, 99), Interval(25, 29), Interval(65, 67), Interval(47, 57), Interval(14, 18),
         Interval(20, 20), Interval(24, 24), Interval(55, 63), Interval(70, 80), Interval(58, 70),
         Interval(23, 29), Interval(77, 99), Interval(55, 59), Interval(65, 71), Interval(55, 65),
         Interval(11, 13), Interval(47, 61), Interval(99, 99), Interval(51, 51), Interval(61, 81)],
        # Job 58
        [Interval(77, 81), Interval(6, 6), Interval(35, 47), Interval(7, 9), Interval(87, 99),
         Interval(45, 47), Interval(61, 77), Interval(76, 86), Interval(55, 67), Interval(39, 49),
         Interval(2, 2), Interval(66, 72), Interval(64, 80), Interval(21, 21), Interval(53, 57),
         Interval(68, 70), Interval(13, 13), Interval(63, 75), Interval(69, 91), Interval(79, 103)],
        # Job 59
        [Interval(76, 88), Interval(88, 110), Interval(90, 94), Interval(47, 59), Interval(5, 5),
         Interval(29, 37), Interval(53, 65), Interval(29, 35), Interval(89, 97), Interval(12, 14),
         Interval(56, 72), Interval(17, 21), Interval(96, 96), Interval(12, 12), Interval(63, 69),
         Interval(4, 4), Interval(77, 89), Interval(57, 73), Interval(3, 3), Interval(79, 79)],
        # Job 60
        [Interval(16, 16), Interval(62, 62), Interval(1, 1), Interval(38, 44), Interval(81, 87),
         Interval(60, 62), Interval(30, 32), Interval(54, 72), Interval(9, 11), Interval(9, 11),
         Interval(14, 14), Interval(65, 85), Interval(13, 15), Interval(57, 69), Interval(52, 54),
         Interval(55, 67), Interval(41, 41), Interval(7, 7), Interval(57, 57), Interval(13, 17)],
        # Job 61
        [Interval(5, 5), Interval(83, 83), Interval(23, 27), Interval(37, 37), Interval(73, 89),
         Interval(42, 42), Interval(18, 22), Interval(21, 23), Interval(49, 51), Interval(37, 43),
         Interval(76, 78), Interval(72, 80), Interval(57, 59), Interval(80, 96), Interval(70, 84),
         Interval(69, 69), Interval(56, 70), Interval(54, 58), Interval(48, 50), Interval(40, 42)],
        # Job 62
        [Interval(43, 43), Interval(16, 16), Interval(1, 1), Interval(51, 61), Interval(33, 43),
         Interval(35, 47), Interval(71, 85), Interval(73, 89), Interval(5, 5), Interval(41, 51),
         Interval(10, 10), Interval(6, 6), Interval(28, 34), Interval(42, 46), Interval(19, 25),
         Interval(69, 87), Interval(88, 98), Interval(39, 45), Interval(18, 24), Interval(40, 46)],
        # Job 63
        [Interval(26, 28), Interval(25, 27), Interval(30, 34), Interval(17, 23), Interval(20, 20),
         Interval(5, 5), Interval(38, 48), Interval(57, 69), Interval(22, 24), Interval(27, 31),
         Interval(39, 51), Interval(72, 86), Interval(68, 68), Interval(67, 79), Interval(1, 1),
         Interval(9, 11), Interval(54, 68), Interval(53, 59), Interval(85, 105), Interval(31, 41)],
        # Job 64
        [Interval(77, 99), Interval(18, 24), Interval(78, 94), Interval(90, 94), Interval(87, 91),
         Interval(30, 30), Interval(44, 44), Interval(23, 27), Interval(99, 99), Interval(88, 94),
         Interval(20, 22), Interval(42, 48), Interval(82, 82), Interval(39, 43), Interval(70, 82),
         Interval(30, 36), Interval(70, 84), Interval(48, 50), Interval(57, 69), Interval(36, 38)],
        # Job 65
        [Interval(32, 34), Interval(53, 55), Interval(77, 81), Interval(55, 57), Interval(47, 61),
         Interval(66, 84), Interval(77, 81), Interval(99, 99), Interval(35, 41), Interval(13, 13),
         Interval(2, 2), Interval(47, 59), Interval(79, 99), Interval(81, 83), Interval(52, 54),
         Interval(31, 35), Interval(40, 46), Interval(73, 73), Interval(22, 28), Interval(12, 16)],
        # Job 66
        [Interval(7, 7), Interval(43, 43), Interval(70, 70), Interval(21, 23), Interval(54, 54),
         Interval(78, 84), Interval(39, 49), Interval(87, 101), Interval(92, 98), Interval(26, 32),
         Interval(12, 16), Interval(44, 56), Interval(86, 110), Interval(17, 19), Interval(50, 50),
         Interval(88, 104), Interval(73, 75), Interval(61, 71), Interval(33, 43), Interval(43, 55)],
        # Job 67
        [Interval(72, 86), Interval(40, 40), Interval(64, 78), Interval(38, 40), Interval(12, 14),
         Interval(19, 19), Interval(1, 1), Interval(77, 87), Interval(53, 63), Interval(25, 27),
         Interval(43, 45), Interval(16, 20), Interval(93, 95), Interval(7, 9), Interval(58, 78),
         Interval(83, 97), Interval(36, 42), Interval(44, 50), Interval(39, 47), Interval(80, 80)],
        # Job 68
        [Interval(79, 85), Interval(1, 1), Interval(68, 84), Interval(20, 24), Interval(17, 17),
         Interval(13, 17), Interval(59, 69), Interval(63, 79), Interval(20, 24), Interval(76, 82),
         Interval(76, 102), Interval(80, 80), Interval(6, 8), Interval(69, 87), Interval(77, 97),
         Interval(76, 100), Interval(21, 23), Interval(58, 60), Interval(74, 76), Interval(21, 27)],
        # Job 69
        [Interval(53, 59), Interval(81, 105), Interval(62, 64), Interval(22, 24), Interval(31, 31),
         Interval(89, 91), Interval(46, 46), Interval(74, 92), Interval(21, 21), Interval(4, 4),
         Interval(46, 60), Interval(94, 104), Interval(62, 68), Interval(91, 107), Interval(56, 60),
         Interval(5, 5), Interval(33, 33), Interval(15, 19), Interval(23, 29), Interval(7, 7)],
        # Job 70
        [Interval(30, 40), Interval(42, 46), Interval(9, 11), Interval(5, 5), Interval(40, 40),
         Interval(64, 68), Interval(12, 14), Interval(17, 23), Interval(24, 26), Interval(83, 107),
         Interval(80, 96), Interval(28, 36), Interval(40, 50), Interval(10, 12), Interval(17, 23),
         Interval(58, 64), Interval(32, 40), Interval(41, 49), Interval(5, 5), Interval(48, 64)],
        # Job 71
        [Interval(41, 41), Interval(6, 6), Interval(72, 82), Interval(69, 69), Interval(82, 84),
         Interval(15, 19), Interval(21, 23), Interval(31, 33), Interval(53, 63), Interval(55, 71),
         Interval(53, 65), Interval(31, 31), Interval(80, 108), Interval(84, 96), Interval(20, 20),
         Interval(75, 91), Interval(14, 14), Interval(64, 70), Interval(60, 64), Interval(57, 67)],
        # Job 72
        [Interval(33, 39), Interval(77, 85), Interval(62, 78), Interval(20, 20), Interval(51, 69),
         Interval(20, 24), Interval(7, 9), Interval(27, 35), Interval(52, 54), Interval(58, 76),
         Interval(65, 67), Interval(72, 78), Interval(20, 24), Interval(30, 30), Interval(40, 54),
         Interval(61, 77), Interval(65, 71), Interval(72, 82), Interval(10, 10), Interval(4, 4)],
        # Job 73
        [Interval(18, 24), Interval(86, 108), Interval(61, 81), Interval(12, 14), Interval(81, 89),
         Interval(85, 105), Interval(25, 29), Interval(9, 11), Interval(22, 26), Interval(38, 48),
         Interval(69, 93), Interval(86, 90), Interval(68, 76), Interval(5, 5), Interval(47, 55),
         Interval(66, 84), Interval(39, 49), Interval(43, 55), Interval(38, 48), Interval(23, 29)],
        # Job 74
        [Interval(68, 70), Interval(93, 93), Interval(65, 67), Interval(11, 13), Interval(73, 89),
         Interval(93, 95), Interval(54, 68), Interval(53, 59), Interval(51, 61), Interval(55, 69),
         Interval(23, 27), Interval(2, 2), Interval(5, 5), Interval(77, 97), Interval(68, 82),
         Interval(13, 15), Interval(14, 14), Interval(43, 47), Interval(30, 30), Interval(7, 9)],
        # Job 75
        [Interval(68, 92), Interval(20, 22), Interval(93, 95), Interval(77, 95), Interval(47, 61),
         Interval(62, 78), Interval(82, 84), Interval(35, 43), Interval(46, 62), Interval(73, 79),
         Interval(43, 57), Interval(18, 18), Interval(15, 15), Interval(4, 4), Interval(32, 36),
         Interval(11, 13), Interval(8, 10), Interval(43, 51), Interval(30, 32), Interval(64, 66)],
        # Job 76
        [Interval(71, 83), Interval(82, 92), Interval(83, 111), Interval(82, 98), Interval(23, 27),
         Interval(67, 87), Interval(84, 92), Interval(68, 84), Interval(67, 71), Interval(14, 16),
         Interval(44, 54), Interval(25, 29), Interval(74, 76), Interval(78, 102), Interval(30, 34),
         Interval(23, 29), Interval(59, 75), Interval(70, 94), Interval(53, 65), Interval(67, 77)],
        # Job 77
        [Interval(80, 90), Interval(38, 42), Interval(41, 55), Interval(62, 66), Interval(8, 8),
         Interval(72, 86), Interval(95, 97), Interval(70, 70), Interval(22, 28), Interval(29, 31),
         Interval(67, 83), Interval(74, 98), Interval(62, 82), Interval(46, 52), Interval(69, 79),
         Interval(48, 62), Interval(80, 94), Interval(31, 37), Interval(86, 110), Interval(46, 46)],
        # Job 78
        [Interval(75, 99), Interval(70, 80), Interval(53, 57), Interval(30, 38), Interval(53, 71),
         Interval(29, 33), Interval(53, 53), Interval(12, 14), Interval(61, 65), Interval(14, 14),
         Interval(18, 22), Interval(11, 13), Interval(13, 15), Interval(41, 55), Interval(4, 4),
         Interval(56, 72), Interval(16, 18), Interval(5, 5), Interval(85, 85), Interval(41, 41)],
        # Job 79
        [Interval(54, 56), Interval(74, 74), Interval(13, 17), Interval(39, 39), Interval(60, 68),
         Interval(68, 74), Interval(16, 20), Interval(51, 69), Interval(24, 32), Interval(80, 84),
         Interval(85, 101), Interval(64, 72), Interval(67, 83), Interval(48, 64), Interval(9, 9),
         Interval(9, 9), Interval(17, 23), Interval(61, 61), Interval(78, 78), Interval(5, 5)],
        # Job 80
        [Interval(22, 24), Interval(60, 72), Interval(23, 27), Interval(2, 2), Interval(13, 13),
         Interval(63, 81), Interval(44, 58), Interval(76, 86), Interval(43, 51), Interval(6, 6),
         Interval(39, 45), Interval(40, 48), Interval(78, 98), Interval(34, 38), Interval(93, 93),
         Interval(20, 22), Interval(6, 6), Interval(53, 71), Interval(17, 19), Interval(36, 40)],
        # Job 81
        [Interval(73, 95), Interval(1, 1), Interval(70, 70), Interval(56, 70), Interval(65, 75),
         Interval(22, 22), Interval(92, 104), Interval(4, 4), Interval(85, 85), Interval(27, 31),
         Interval(73, 89), Interval(25, 27), Interval(44, 54), Interval(56, 68), Interval(46, 52),
         Interval(62, 70), Interval(40, 42), Interval(27, 35), Interval(49, 53), Interval(22, 24)],
        # Job 82
        [Interval(8, 10), Interval(17, 23), Interval(55, 65), Interval(22, 22), Interval(25, 33),
         Interval(76, 102), Interval(31, 41), Interval(44, 58), Interval(96, 98), Interval(35, 43),
         Interval(54, 62), Interval(43, 57), Interval(43, 53), Interval(88, 100), Interval(31, 39),
         Interval(95, 95), Interval(36, 38), Interval(72, 86), Interval(65, 77), Interval(12, 12)],
        # Job 83
        [Interval(69, 87), Interval(91, 99), Interval(38, 46), Interval(59, 61), Interval(54, 70),
         Interval(86, 112), Interval(29, 33), Interval(87, 101), Interval(70, 86), Interval(23, 31),
         Interval(21, 25), Interval(51, 69), Interval(9, 11), Interval(75, 85), Interval(77, 89),
         Interval(48, 60), Interval(89, 103), Interval(15, 15), Interval(45, 55), Interval(62, 66)],
        # Job 84
        [Interval(28, 36), Interval(52, 66), Interval(87, 99), Interval(91, 99), Interval(53, 69),
         Interval(19, 19), Interval(46, 46), Interval(70, 80), Interval(63, 75), Interval(70, 82),
         Interval(85, 107), Interval(48, 52), Interval(9, 11), Interval(64, 74), Interval(10, 10),
         Interval(98, 98), Interval(51, 69), Interval(1, 1), Interval(72, 90), Interval(74, 84)],
        # Job 85
        [Interval(22, 24), Interval(61, 67), Interval(64, 76), Interval(33, 37), Interval(6, 6),
         Interval(8, 8), Interval(87, 107), Interval(7, 7), Interval(54, 58), Interval(91, 93),
         Interval(10, 12), Interval(43, 57), Interval(35, 43), Interval(72, 72), Interval(25, 25),
         Interval(79, 91), Interval(4, 4), Interval(55, 63), Interval(2, 2), Interval(24, 30)],
        # Job 86
        [Interval(46, 46), Interval(89, 91), Interval(78, 100), Interval(66, 66), Interval(77, 97),
         Interval(35, 35), Interval(78, 88), Interval(83, 97), Interval(93, 93), Interval(49, 59),
         Interval(10, 10), Interval(19, 25), Interval(17, 19), Interval(91, 103), Interval(18, 20),
         Interval(89, 99), Interval(53, 67), Interval(90, 90), Interval(81, 85), Interval(36, 46)],
        # Job 87
        [Interval(51, 57), Interval(47, 59), Interval(4, 4), Interval(51, 57), Interval(69, 77),
         Interval(16, 20), Interval(25, 27), Interval(52, 64), Interval(41, 47), Interval(1, 1),
         Interval(49, 49), Interval(92, 98), Interval(88, 94), Interval(38, 38), Interval(92, 94),
         Interval(27, 31), Interval(62, 78), Interval(12, 16), Interval(6, 6), Interval(51, 51)],
        # Job 88
        [Interval(50, 64), Interval(4, 4), Interval(18, 24), Interval(5, 5), Interval(63, 65),
         Interval(64, 78), Interval(62, 72), Interval(23, 25), Interval(38, 40), Interval(64, 82),
         Interval(94, 102), Interval(11, 13), Interval(31, 37), Interval(19, 21), Interval(30, 32),
         Interval(11, 13), Interval(37, 43), Interval(73, 77), Interval(21, 23), Interval(65, 65)],
        # Job 89
        [Interval(63, 63), Interval(79, 87), Interval(28, 30), Interval(74, 94), Interval(25, 25),
         Interval(11, 13), Interval(74, 88), Interval(78, 100), Interval(38, 50), Interval(21, 25),
         Interval(64, 68), Interval(31, 31), Interval(26, 32), Interval(63, 65), Interval(58, 76),
         Interval(55, 57), Interval(30, 38), Interval(84, 110), Interval(25, 29), Interval(62, 80)],
        # Job 90
        [Interval(94, 104), Interval(28, 28), Interval(73, 73), Interval(9, 11), Interval(80, 90),
         Interval(53, 59), Interval(54, 58), Interval(10, 10), Interval(29, 31), Interval(73, 91),
         Interval(2, 2), Interval(42, 48), Interval(16, 16), Interval(33, 39), Interval(88, 90),
         Interval(24, 30), Interval(29, 39), Interval(82, 88), Interval(14, 18), Interval(71, 79)],
        # Job 91
        [Interval(50, 56), Interval(30, 36), Interval(15, 17), Interval(71, 91), Interval(46, 62),
         Interval(13, 17), Interval(63, 71), Interval(43, 49), Interval(85, 111), Interval(62, 82),
         Interval(63, 67), Interval(41, 43), Interval(12, 14), Interval(36, 44), Interval(51, 61),
         Interval(38, 48), Interval(50, 64), Interval(55, 57), Interval(76, 78), Interval(92, 96)],
        # Job 92
        [Interval(37, 39), Interval(74, 92), Interval(51, 59), Interval(75, 85), Interval(40, 54),
         Interval(25, 31), Interval(78, 86), Interval(74, 90), Interval(45, 47), Interval(83, 95),
         Interval(20, 24), Interval(63, 75), Interval(44, 44), Interval(78, 90), Interval(63, 77),
         Interval(32, 32), Interval(21, 21), Interval(52, 58), Interval(51, 53), Interval(12, 14)],
        # Job 93
        [Interval(37, 43), Interval(54, 56), Interval(53, 55), Interval(73, 73), Interval(87, 101),
         Interval(71, 89), Interval(54, 68), Interval(73, 75), Interval(91, 93), Interval(20, 26),
         Interval(17, 19), Interval(37, 45), Interval(42, 50), Interval(81, 107), Interval(65, 81),
         Interval(31, 31), Interval(31, 35), Interval(34, 36), Interval(31, 33), Interval(13, 17)],
        # Job 94
        [Interval(69, 73), Interval(20, 20), Interval(37, 39), Interval(68, 76), Interval(45, 45),
         Interval(74, 76), Interval(24, 32), Interval(30, 30), Interval(45, 59), Interval(57, 57),
         Interval(24, 28), Interval(77, 77), Interval(71, 73), Interval(39, 47), Interval(56, 68),
         Interval(7, 7), Interval(38, 44), Interval(19, 23), Interval(50, 66), Interval(21, 21)],
        # Job 95
        [Interval(18, 18), Interval(53, 59), Interval(70, 76), Interval(17, 17), Interval(28, 34),
         Interval(47, 51), Interval(41, 53), Interval(66, 66), Interval(16, 18), Interval(64, 86),
         Interval(24, 26), Interval(37, 39), Interval(42, 44), Interval(87, 103), Interval(4, 4),
         Interval(62, 80), Interval(26, 26), Interval(5, 5), Interval(23, 29), Interval(26, 30)],
        # Job 96
        [Interval(29, 37), Interval(56, 68), Interval(47, 49), Interval(20, 22), Interval(77, 81),
         Interval(42, 54), Interval(87, 99), Interval(28, 30), Interval(94, 104), Interval(88, 108),
         Interval(91, 95), Interval(32, 40), Interval(44, 54), Interval(41, 43), Interval(20, 24),
         Interval(54, 72), Interval(37, 49), Interval(24, 30), Interval(9, 11), Interval(3, 3)],
        # Job 97
        [Interval(79, 91), Interval(4, 4), Interval(35, 47), Interval(8, 8), Interval(72, 84),
         Interval(84, 92), Interval(80, 84), Interval(47, 59), Interval(25, 25), Interval(70, 90),
         Interval(31, 33), Interval(28, 28), Interval(71, 79), Interval(28, 34), Interval(17, 21),
         Interval(11, 11), Interval(4, 4), Interval(90, 94), Interval(29, 33), Interval(1, 1)],
        # Job 98
        [Interval(85, 107), Interval(22, 26), Interval(45, 49), Interval(34, 36), Interval(32, 40),
         Interval(82, 84), Interval(97, 101), Interval(20, 24), Interval(82, 100), Interval(1, 1),
         Interval(38, 48), Interval(30, 36), Interval(83, 111), Interval(50, 50), Interval(36, 46),
         Interval(70, 86), Interval(87, 97), Interval(84, 100), Interval(39, 41), Interval(43, 47)],
        # Job 99
        [Interval(97, 97), Interval(59, 65), Interval(35, 35), Interval(42, 42), Interval(49, 53),
         Interval(12, 16), Interval(59, 69), Interval(10, 10), Interval(88, 102), Interval(7, 7),
         Interval(35, 41), Interval(10, 12), Interval(31, 39), Interval(25, 25), Interval(75, 79),
         Interval(80, 84), Interval(69, 89), Interval(69, 93), Interval(15, 19), Interval(31, 35)],
    ],
    'name': 'INT__TAI100_20_04.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai100_20_04_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI100_20_04.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI100_20_04.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI100_20_04_F_15_01_INTERVAL_DATA
