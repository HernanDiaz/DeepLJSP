"""
Problema INT__TAI50_20_06.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI50_20_06_F_15_01_INTERVAL_DATA = {
    'num_jobs': 50,
    'num_machines': 20,
    'problem_id': 'int__tai50_20_06.F.15_01_interval',
    'sequences': [
        [10, 5, 2, 17, 14, 19, 1, 4, 8, 16, 11, 3, 0, 6, 7, 12, 13, 18, 15, 9],
        [5, 13, 4, 3, 19, 18, 16, 2, 0, 10, 11, 7, 1, 15, 12, 14, 9, 8, 17, 6],
        [10, 15, 19, 9, 16, 12, 7, 17, 8, 1, 18, 13, 6, 5, 4, 0, 14, 11, 2, 3],
        [12, 10, 8, 4, 15, 18, 11, 16, 6, 9, 0, 1, 19, 5, 3, 17, 2, 14, 7, 13],
        [5, 15, 6, 7, 3, 17, 9, 11, 1, 18, 12, 13, 4, 19, 0, 10, 14, 8, 2, 16],
        [17, 9, 8, 14, 10, 16, 13, 12, 11, 15, 2, 3, 5, 0, 1, 4, 6, 7, 18, 19],
        [15, 19, 18, 12, 2, 3, 5, 0, 14, 4, 8, 1, 7, 17, 10, 9, 11, 13, 16, 6],
        [6, 5, 16, 4, 13, 1, 9, 7, 14, 11, 0, 3, 2, 10, 18, 15, 19, 17, 8, 12],
        [17, 1, 3, 6, 0, 9, 12, 19, 16, 7, 8, 4, 2, 13, 5, 18, 15, 11, 14, 10],
        [12, 17, 5, 16, 7, 1, 8, 0, 19, 6, 3, 14, 2, 10, 15, 4, 18, 13, 9, 11],
        [2, 18, 0, 19, 10, 17, 1, 8, 7, 16, 15, 14, 5, 4, 6, 13, 3, 12, 11, 9],
        [7, 2, 12, 0, 16, 14, 3, 15, 17, 5, 19, 4, 10, 8, 18, 1, 13, 9, 11, 6],
        [17, 0, 12, 4, 5, 1, 10, 8, 11, 15, 3, 16, 7, 6, 19, 13, 9, 14, 18, 2],
        [9, 15, 4, 3, 18, 1, 16, 14, 13, 5, 19, 0, 8, 7, 10, 12, 17, 11, 2, 6],
        [8, 5, 3, 19, 1, 2, 17, 13, 6, 10, 12, 15, 11, 0, 9, 14, 4, 7, 16, 18],
        [1, 15, 8, 13, 4, 12, 17, 19, 6, 9, 0, 2, 18, 14, 11, 5, 3, 16, 10, 7],
        [14, 9, 18, 6, 17, 10, 19, 16, 4, 5, 12, 15, 0, 13, 1, 11, 3, 8, 7, 2],
        [8, 17, 5, 13, 9, 14, 7, 18, 0, 10, 1, 2, 15, 16, 6, 11, 3, 12, 4, 19],
        [14, 6, 8, 13, 16, 0, 2, 3, 9, 18, 15, 10, 11, 4, 5, 19, 1, 7, 12, 17],
        [14, 8, 2, 7, 19, 5, 16, 6, 1, 13, 18, 11, 0, 4, 15, 12, 10, 9, 3, 17],
        [9, 5, 19, 3, 11, 4, 12, 2, 8, 1, 13, 6, 0, 18, 10, 17, 14, 15, 16, 7],
        [18, 12, 0, 8, 2, 1, 16, 15, 13, 14, 11, 4, 7, 5, 9, 3, 10, 17, 6, 19],
        [19, 15, 0, 7, 12, 4, 3, 6, 10, 17, 14, 16, 8, 2, 9, 13, 18, 11, 1, 5],
        [17, 9, 10, 8, 11, 16, 19, 12, 14, 6, 1, 15, 0, 7, 4, 2, 3, 5, 13, 18],
        [1, 17, 5, 18, 2, 7, 16, 11, 15, 4, 0, 10, 8, 3, 12, 19, 14, 13, 9, 6],
        [0, 17, 9, 15, 16, 1, 6, 3, 12, 10, 8, 5, 13, 2, 19, 7, 4, 11, 14, 18],
        [4, 12, 2, 1, 17, 14, 6, 15, 0, 9, 5, 11, 7, 18, 3, 10, 16, 13, 8, 19],
        [1, 6, 13, 19, 18, 11, 17, 7, 10, 15, 4, 3, 9, 0, 16, 12, 8, 2, 14, 5],
        [2, 4, 16, 12, 14, 15, 9, 8, 19, 10, 13, 0, 1, 11, 5, 6, 7, 17, 3, 18],
        [15, 4, 6, 13, 14, 19, 5, 1, 17, 16, 12, 11, 10, 18, 8, 2, 0, 3, 7, 9],
        [8, 2, 15, 12, 10, 3, 18, 13, 9, 0, 5, 7, 19, 16, 17, 1, 11, 4, 6, 14],
        [19, 8, 10, 16, 18, 6, 14, 13, 11, 9, 2, 7, 3, 4, 0, 1, 5, 15, 17, 12],
        [15, 9, 16, 10, 18, 13, 11, 14, 6, 3, 1, 4, 8, 19, 17, 7, 0, 2, 5, 12],
        [1, 12, 17, 2, 9, 10, 15, 19, 4, 16, 18, 11, 7, 8, 13, 0, 14, 5, 3, 6],
        [6, 19, 2, 17, 15, 12, 14, 16, 4, 7, 1, 11, 5, 13, 9, 0, 18, 3, 8, 10],
        [3, 0, 6, 2, 12, 16, 5, 8, 18, 1, 13, 9, 11, 14, 19, 10, 17, 7, 15, 4],
        [14, 7, 3, 6, 9, 8, 16, 1, 15, 2, 17, 13, 5, 12, 19, 10, 18, 11, 4, 0],
        [18, 13, 19, 2, 10, 6, 4, 14, 15, 9, 7, 16, 1, 0, 12, 5, 11, 17, 8, 3],
        [12, 1, 10, 3, 0, 13, 2, 18, 15, 16, 9, 8, 4, 7, 19, 5, 11, 14, 6, 17],
        [7, 12, 2, 13, 6, 4, 17, 0, 15, 19, 16, 3, 1, 5, 14, 11, 10, 18, 8, 9],
        [2, 18, 5, 12, 0, 6, 19, 9, 1, 15, 13, 14, 3, 16, 8, 17, 11, 10, 4, 7],
        [4, 2, 8, 11, 3, 14, 19, 10, 9, 18, 6, 1, 5, 13, 17, 0, 15, 16, 7, 12],
        [3, 16, 14, 15, 12, 19, 18, 6, 7, 5, 10, 2, 4, 0, 11, 1, 13, 17, 8, 9],
        [14, 3, 9, 16, 4, 17, 6, 10, 0, 18, 1, 15, 5, 12, 11, 2, 7, 19, 13, 8],
        [9, 12, 1, 14, 15, 7, 8, 2, 6, 10, 18, 3, 19, 11, 17, 13, 4, 16, 5, 0],
        [0, 19, 12, 15, 13, 7, 17, 6, 5, 18, 9, 2, 14, 3, 16, 11, 1, 8, 4, 10],
        [14, 11, 6, 8, 7, 12, 5, 4, 19, 18, 15, 16, 2, 0, 10, 13, 17, 9, 3, 1],
        [12, 11, 13, 19, 9, 18, 5, 6, 2, 15, 14, 0, 8, 1, 3, 7, 16, 17, 10, 4],
        [6, 1, 9, 5, 15, 11, 10, 7, 0, 12, 2, 8, 14, 17, 13, 3, 16, 18, 19, 4],
        [2, 13, 8, 10, 18, 4, 6, 7, 5, 11, 16, 3, 17, 19, 0, 14, 15, 12, 1, 9],
    ],
    'durations': [
        # Job 0
        [Interval(65, 85), Interval(50, 50), Interval(4, 4), Interval(29, 39), Interval(32, 40),
         Interval(66, 72), Interval(51, 53), Interval(38, 50), Interval(37, 47), Interval(12, 12),
         Interval(47, 53), Interval(11, 13), Interval(64, 78), Interval(76, 102), Interval(29, 33),
         Interval(13, 15), Interval(12, 14), Interval(48, 58), Interval(42, 44), Interval(37, 49)],
        # Job 1
        [Interval(24, 30), Interval(16, 20), Interval(61, 79), Interval(83, 85), Interval(7, 9),
         Interval(53, 71), Interval(78, 104), Interval(21, 27), Interval(89, 99), Interval(97, 99),
         Interval(70, 86), Interval(86, 94), Interval(1, 1), Interval(22, 26), Interval(82, 110),
         Interval(59, 63), Interval(89, 91), Interval(66, 68), Interval(7, 7), Interval(64, 80)],
        # Job 2
        [Interval(52, 60), Interval(78, 90), Interval(89, 101), Interval(28, 36), Interval(8, 8),
         Interval(37, 49), Interval(34, 40), Interval(22, 28), Interval(10, 10), Interval(74, 96),
         Interval(70, 86), Interval(75, 77), Interval(89, 99), Interval(56, 64), Interval(37, 37),
         Interval(60, 76), Interval(11, 11), Interval(66, 66), Interval(61, 71), Interval(75, 91)],
        # Job 3
        [Interval(64, 66), Interval(82, 108), Interval(65, 67), Interval(4, 4), Interval(32, 36),
         Interval(48, 62), Interval(30, 40), Interval(29, 35), Interval(74, 82), Interval(45, 59),
         Interval(9, 11), Interval(53, 63), Interval(9, 9), Interval(64, 82), Interval(17, 19),
         Interval(46, 58), Interval(54, 60), Interval(56, 62), Interval(24, 30), Interval(85, 93)],
        # Job 4
        [Interval(29, 33), Interval(71, 91), Interval(39, 51), Interval(20, 22), Interval(67, 81),
         Interval(6, 8), Interval(38, 48), Interval(34, 36), Interval(22, 24), Interval(62, 64),
         Interval(12, 12), Interval(88, 96), Interval(69, 87), Interval(9, 9), Interval(27, 33),
         Interval(19, 25), Interval(19, 19), Interval(65, 75), Interval(4, 4), Interval(16, 18)],
        # Job 5
        [Interval(50, 56), Interval(46, 56), Interval(34, 36), Interval(11, 11), Interval(54, 56),
         Interval(17, 19), Interval(77, 101), Interval(88, 94), Interval(14, 18), Interval(72, 92),
         Interval(82, 86), Interval(4, 4), Interval(2, 2), Interval(81, 109), Interval(15, 19),
         Interval(80, 104), Interval(78, 84), Interval(21, 23), Interval(7, 7), Interval(54, 62)],
        # Job 6
        [Interval(88, 96), Interval(44, 50), Interval(9, 11), Interval(44, 50), Interval(4, 4),
         Interval(72, 78), Interval(35, 47), Interval(49, 53), Interval(2, 2), Interval(65, 81),
         Interval(48, 56), Interval(37, 39), Interval(41, 47), Interval(21, 25), Interval(28, 34),
         Interval(84, 96), Interval(82, 98), Interval(74, 88), Interval(72, 78), Interval(81, 87)],
        # Job 7
        [Interval(27, 35), Interval(17, 23), Interval(32, 32), Interval(52, 56), Interval(9, 11),
         Interval(93, 99), Interval(6, 6), Interval(71, 91), Interval(64, 82), Interval(70, 80),
         Interval(82, 108), Interval(69, 93), Interval(28, 34), Interval(81, 81), Interval(77, 103),
         Interval(32, 34), Interval(57, 71), Interval(96, 96), Interval(18, 24), Interval(1, 1)],
        # Job 8
        [Interval(59, 75), Interval(59, 63), Interval(17, 19), Interval(75, 87), Interval(67, 87),
         Interval(35, 35), Interval(11, 13), Interval(27, 29), Interval(73, 91), Interval(9, 11),
         Interval(64, 78), Interval(83, 105), Interval(44, 58), Interval(50, 58), Interval(24, 26),
         Interval(35, 39), Interval(31, 37), Interval(2, 2), Interval(66, 76), Interval(57, 63)],
        # Job 9
        [Interval(29, 29), Interval(67, 89), Interval(31, 35), Interval(51, 57), Interval(20, 20),
         Interval(74, 76), Interval(85, 91), Interval(35, 35), Interval(66, 74), Interval(33, 37),
         Interval(49, 57), Interval(34, 38), Interval(73, 91), Interval(26, 26), Interval(21, 27),
         Interval(26, 30), Interval(10, 10), Interval(84, 112), Interval(80, 92), Interval(2, 2)],
        # Job 10
        [Interval(26, 34), Interval(2, 2), Interval(83, 109), Interval(57, 75), Interval(3, 3),
         Interval(72, 90), Interval(4, 4), Interval(50, 56), Interval(11, 13), Interval(34, 38),
         Interval(57, 65), Interval(71, 85), Interval(23, 27), Interval(64, 86), Interval(39, 49),
         Interval(12, 12), Interval(77, 85), Interval(21, 25), Interval(39, 43), Interval(82, 92)],
        # Job 11
        [Interval(91, 105), Interval(44, 50), Interval(78, 92), Interval(86, 94), Interval(74, 74),
         Interval(80, 108), Interval(21, 27), Interval(16, 20), Interval(7, 9), Interval(80, 100),
         Interval(47, 63), Interval(66, 68), Interval(45, 59), Interval(3, 3), Interval(24, 32),
         Interval(26, 32), Interval(73, 73), Interval(88, 104), Interval(52, 62), Interval(49, 61)],
        # Job 12
        [Interval(17, 19), Interval(64, 80), Interval(88, 88), Interval(51, 65), Interval(5, 5),
         Interval(74, 88), Interval(83, 103), Interval(89, 101), Interval(36, 36), Interval(49, 53),
         Interval(49, 57), Interval(56, 66), Interval(63, 81), Interval(59, 67), Interval(35, 37),
         Interval(44, 52), Interval(84, 108), Interval(80, 104), Interval(20, 22), Interval(52, 70)],
        # Job 13
        [Interval(55, 55), Interval(39, 51), Interval(89, 93), Interval(21, 27), Interval(76, 78),
         Interval(61, 81), Interval(11, 13), Interval(84, 98), Interval(60, 76), Interval(53, 57),
         Interval(88, 88), Interval(65, 87), Interval(86, 92), Interval(14, 14), Interval(82, 102),
         Interval(56, 72), Interval(60, 72), Interval(13, 13), Interval(45, 51), Interval(51, 63)],
        # Job 14
        [Interval(89, 95), Interval(18, 18), Interval(54, 58), Interval(60, 78), Interval(79, 93),
         Interval(20, 26), Interval(29, 37), Interval(74, 98), Interval(52, 52), Interval(70, 72),
         Interval(94, 100), Interval(9, 9), Interval(16, 16), Interval(35, 41), Interval(61, 77),
         Interval(33, 35), Interval(40, 46), Interval(1, 1), Interval(68, 74), Interval(72, 96)],
        # Job 15
        [Interval(51, 67), Interval(45, 55), Interval(11, 11), Interval(20, 22), Interval(47, 47),
         Interval(48, 56), Interval(75, 81), Interval(72, 72), Interval(75, 97), Interval(27, 29),
         Interval(72, 90), Interval(5, 5), Interval(27, 31), Interval(31, 41), Interval(7, 7),
         Interval(59, 77), Interval(24, 32), Interval(88, 106), Interval(42, 56), Interval(90, 96)],
        # Job 16
        [Interval(32, 36), Interval(18, 22), Interval(31, 33), Interval(87, 93), Interval(52, 66),
         Interval(51, 55), Interval(88, 96), Interval(1, 1), Interval(7, 9), Interval(9, 11),
         Interval(10, 10), Interval(25, 25), Interval(7, 9), Interval(49, 57), Interval(25, 25),
         Interval(79, 79), Interval(85, 85), Interval(25, 31), Interval(10, 10), Interval(29, 37)],
        # Job 17
        [Interval(37, 37), Interval(46, 56), Interval(77, 81), Interval(6, 6), Interval(24, 32),
         Interval(36, 44), Interval(18, 20), Interval(51, 69), Interval(14, 14), Interval(12, 12),
         Interval(27, 35), Interval(24, 26), Interval(13, 17), Interval(80, 88), Interval(81, 85),
         Interval(84, 86), Interval(81, 93), Interval(32, 36), Interval(39, 45), Interval(79, 105)],
        # Job 18
        [Interval(23, 25), Interval(3, 3), Interval(12, 12), Interval(37, 41), Interval(5, 5),
         Interval(26, 30), Interval(44, 58), Interval(67, 69), Interval(36, 36), Interval(6, 6),
         Interval(11, 13), Interval(51, 57), Interval(58, 64), Interval(10, 12), Interval(86, 112),
         Interval(35, 43), Interval(52, 54), Interval(3, 3), Interval(29, 37), Interval(41, 55)],
        # Job 19
        [Interval(35, 41), Interval(78, 84), Interval(84, 84), Interval(12, 12), Interval(34, 38),
         Interval(82, 110), Interval(58, 76), Interval(40, 52), Interval(83, 97), Interval(68, 88),
         Interval(19, 25), Interval(82, 84), Interval(77, 93), Interval(97, 97), Interval(43, 57),
         Interval(76, 80), Interval(87, 95), Interval(73, 93), Interval(42, 56), Interval(31, 31)],
        # Job 20
        [Interval(9, 11), Interval(42, 42), Interval(25, 33), Interval(1, 1), Interval(88, 88),
         Interval(7, 7), Interval(10, 12), Interval(35, 47), Interval(51, 51), Interval(34, 46),
         Interval(84, 96), Interval(17, 23), Interval(37, 47), Interval(38, 42), Interval(24, 26),
         Interval(30, 32), Interval(7, 9), Interval(81, 91), Interval(72, 96), Interval(25, 25)],
        # Job 21
        [Interval(12, 12), Interval(64, 76), Interval(86, 100), Interval(67, 87), Interval(18, 18),
         Interval(13, 13), Interval(61, 79), Interval(35, 35), Interval(93, 101), Interval(44, 56),
         Interval(32, 32), Interval(76, 100), Interval(98, 98), Interval(37, 37), Interval(76, 88),
         Interval(48, 58), Interval(20, 22), Interval(83, 103), Interval(52, 68), Interval(93, 93)],
        # Job 22
        [Interval(14, 14), Interval(80, 90), Interval(21, 21), Interval(24, 26), Interval(64, 80),
         Interval(37, 39), Interval(39, 47), Interval(60, 76), Interval(33, 43), Interval(16, 20),
         Interval(33, 37), Interval(48, 50), Interval(91, 107), Interval(48, 48), Interval(86, 88),
         Interval(11, 11), Interval(14, 18), Interval(83, 109), Interval(34, 38), Interval(74, 94)],
        # Job 23
        [Interval(6, 6), Interval(23, 23), Interval(96, 98), Interval(72, 72), Interval(29, 35),
         Interval(77, 77), Interval(31, 39), Interval(58, 66), Interval(14, 16), Interval(72, 72),
         Interval(43, 53), Interval(29, 39), Interval(47, 55), Interval(24, 24), Interval(63, 79),
         Interval(16, 20), Interval(5, 5), Interval(37, 37), Interval(52, 60), Interval(12, 14)],
        # Job 24
        [Interval(10, 10), Interval(38, 38), Interval(69, 93), Interval(66, 88), Interval(72, 94),
         Interval(34, 46), Interval(37, 49), Interval(57, 71), Interval(91, 91), Interval(1, 1),
         Interval(46, 50), Interval(74, 86), Interval(13, 17), Interval(18, 24), Interval(26, 28),
         Interval(14, 18), Interval(57, 63), Interval(44, 46), Interval(57, 73), Interval(75, 101)],
        # Job 25
        [Interval(18, 22), Interval(4, 4), Interval(69, 89), Interval(84, 90), Interval(27, 27),
         Interval(72, 96), Interval(18, 22), Interval(41, 51), Interval(85, 97), Interval(9, 9),
         Interval(22, 26), Interval(97, 99), Interval(28, 28), Interval(2, 2), Interval(74, 78),
         Interval(19, 25), Interval(81, 95), Interval(61, 73), Interval(28, 36), Interval(32, 42)],
        # Job 26
        [Interval(22, 24), Interval(6, 8), Interval(58, 66), Interval(48, 50), Interval(85, 111),
         Interval(53, 69), Interval(54, 64), Interval(34, 42), Interval(12, 14), Interval(5, 5),
         Interval(75, 75), Interval(64, 84), Interval(63, 67), Interval(63, 69), Interval(53, 67),
         Interval(13, 15), Interval(75, 83), Interval(41, 49), Interval(40, 54), Interval(51, 51)],
        # Job 27
        [Interval(22, 24), Interval(41, 49), Interval(92, 100), Interval(35, 35), Interval(37, 37),
         Interval(32, 36), Interval(28, 30), Interval(11, 13), Interval(85, 93), Interval(59, 79),
         Interval(73, 75), Interval(47, 57), Interval(84, 112), Interval(15, 19), Interval(83, 89),
         Interval(65, 87), Interval(86, 106), Interval(63, 69), Interval(85, 87), Interval(32, 42)],
        # Job 28
        [Interval(65, 83), Interval(94, 104), Interval(8, 10), Interval(8, 10), Interval(74, 74),
         Interval(77, 89), Interval(3, 3), Interval(91, 101), Interval(38, 50), Interval(23, 23),
         Interval(3, 3), Interval(16, 20), Interval(3, 3), Interval(40, 50), Interval(35, 41),
         Interval(22, 26), Interval(81, 101), Interval(35, 37), Interval(21, 23), Interval(15, 15)],
        # Job 29
        [Interval(33, 35), Interval(22, 24), Interval(67, 69), Interval(10, 12), Interval(50, 56),
         Interval(66, 88), Interval(62, 80), Interval(59, 71), Interval(75, 79), Interval(44, 52),
         Interval(41, 45), Interval(44, 46), Interval(71, 95), Interval(7, 7), Interval(87, 99),
         Interval(64, 66), Interval(79, 87), Interval(7, 9), Interval(5, 5), Interval(69, 79)],
        # Job 30
        [Interval(36, 44), Interval(14, 16), Interval(26, 34), Interval(89, 91), Interval(60, 64),
         Interval(14, 16), Interval(13, 13), Interval(3, 3), Interval(43, 55), Interval(82, 98),
         Interval(54, 56), Interval(56, 74), Interval(74, 96), Interval(79, 95), Interval(22, 26),
         Interval(60, 62), Interval(43, 57), Interval(41, 55), Interval(67, 87), Interval(20, 22)],
        # Job 31
        [Interval(36, 48), Interval(84, 98), Interval(67, 73), Interval(8, 8), Interval(45, 45),
         Interval(22, 26), Interval(58, 68), Interval(82, 90), Interval(15, 17), Interval(63, 73),
         Interval(57, 57), Interval(16, 20), Interval(59, 61), Interval(80, 82), Interval(3, 3),
         Interval(16, 18), Interval(67, 69), Interval(88, 106), Interval(39, 45), Interval(54, 54)],
        # Job 32
        [Interval(80, 94), Interval(86, 104), Interval(25, 25), Interval(57, 65), Interval(8, 10),
         Interval(27, 33), Interval(82, 86), Interval(21, 21), Interval(85, 91), Interval(79, 87),
         Interval(63, 81), Interval(85, 87), Interval(18, 22), Interval(64, 82), Interval(35, 43),
         Interval(69, 73), Interval(45, 59), Interval(36, 38), Interval(65, 79), Interval(35, 45)],
        # Job 33
        [Interval(46, 46), Interval(45, 45), Interval(80, 94), Interval(39, 49), Interval(27, 27),
         Interval(41, 47), Interval(17, 21), Interval(48, 54), Interval(71, 95), Interval(2, 2),
         Interval(21, 21), Interval(12, 14), Interval(43, 57), Interval(16, 18), Interval(87, 103),
         Interval(78, 88), Interval(29, 37), Interval(29, 29), Interval(85, 99), Interval(58, 66)],
        # Job 34
        [Interval(20, 24), Interval(65, 81), Interval(34, 36), Interval(4, 4), Interval(20, 24),
         Interval(86, 112), Interval(92, 106), Interval(56, 74), Interval(46, 62), Interval(72, 72),
         Interval(54, 64), Interval(92, 104), Interval(39, 49), Interval(17, 21), Interval(22, 24),
         Interval(95, 95), Interval(79, 95), Interval(59, 79), Interval(63, 73), Interval(57, 57)],
        # Job 35
        [Interval(17, 23), Interval(72, 86), Interval(85, 105), Interval(6, 6), Interval(35, 41),
         Interval(34, 38), Interval(34, 40), Interval(19, 23), Interval(58, 66), Interval(44, 52),
         Interval(74, 82), Interval(16, 20), Interval(70, 70), Interval(67, 89), Interval(1, 1),
         Interval(21, 21), Interval(84, 86), Interval(38, 40), Interval(33, 35), Interval(93, 103)],
        # Job 36
        [Interval(56, 56), Interval(53, 67), Interval(31, 35), Interval(73, 87), Interval(64, 72),
         Interval(57, 63), Interval(41, 41), Interval(77, 87), Interval(17, 17), Interval(85, 93),
         Interval(58, 60), Interval(61, 81), Interval(43, 55), Interval(72, 78), Interval(43, 47),
         Interval(22, 22), Interval(54, 66), Interval(75, 91), Interval(63, 79), Interval(22, 22)],
        # Job 37
        [Interval(67, 77), Interval(65, 79), Interval(11, 11), Interval(14, 16), Interval(70, 74),
         Interval(60, 70), Interval(48, 64), Interval(77, 77), Interval(64, 72), Interval(16, 18),
         Interval(59, 59), Interval(15, 19), Interval(66, 70), Interval(61, 77), Interval(65, 77),
         Interval(58, 62), Interval(36, 42), Interval(41, 43), Interval(72, 84), Interval(53, 71)],
        # Job 38
        [Interval(11, 13), Interval(24, 30), Interval(15, 17), Interval(20, 26), Interval(11, 13),
         Interval(72, 76), Interval(71, 73), Interval(42, 54), Interval(31, 39), Interval(48, 58),
         Interval(9, 9), Interval(78, 82), Interval(58, 78), Interval(13, 17), Interval(53, 71),
         Interval(23, 23), Interval(14, 14), Interval(78, 100), Interval(11, 13), Interval(66, 68)],
        # Job 39
        [Interval(69, 79), Interval(52, 54), Interval(67, 85), Interval(91, 103), Interval(67, 75),
         Interval(79, 83), Interval(28, 28), Interval(67, 73), Interval(62, 72), Interval(23, 29),
         Interval(90, 104), Interval(10, 12), Interval(77, 77), Interval(54, 58), Interval(59, 65),
         Interval(39, 43), Interval(48, 52), Interval(34, 46), Interval(35, 35), Interval(76, 82)],
        # Job 40
        [Interval(74, 76), Interval(3, 3), Interval(31, 33), Interval(10, 10), Interval(91, 95),
         Interval(2, 2), Interval(55, 71), Interval(4, 4), Interval(4, 4), Interval(16, 20),
         Interval(75, 95), Interval(27, 29), Interval(52, 58), Interval(80, 80), Interval(57, 61),
         Interval(66, 82), Interval(47, 55), Interval(69, 79), Interval(17, 23), Interval(41, 51)],
        # Job 41
        [Interval(31, 33), Interval(70, 84), Interval(45, 53), Interval(66, 86), Interval(6, 6),
         Interval(90, 96), Interval(52, 62), Interval(10, 12), Interval(65, 73), Interval(35, 35),
         Interval(51, 67), Interval(18, 22), Interval(20, 24), Interval(13, 13), Interval(35, 35),
         Interval(94, 104), Interval(89, 101), Interval(94, 104), Interval(73, 75), Interval(93, 99)],
        # Job 42
        [Interval(51, 59), Interval(37, 39), Interval(68, 92), Interval(24, 26), Interval(69, 77),
         Interval(49, 63), Interval(78, 96), Interval(14, 18), Interval(2, 2), Interval(79, 81),
         Interval(41, 45), Interval(48, 52), Interval(63, 73), Interval(11, 13), Interval(18, 20),
         Interval(24, 26), Interval(16, 18), Interval(49, 55), Interval(31, 31), Interval(27, 35)],
        # Job 43
        [Interval(48, 58), Interval(60, 78), Interval(57, 57), Interval(84, 112), Interval(45, 51),
         Interval(24, 28), Interval(26, 34), Interval(17, 23), Interval(63, 85), Interval(46, 48),
         Interval(90, 108), Interval(69, 87), Interval(91, 103), Interval(92, 96), Interval(72, 88),
         Interval(72, 76), Interval(40, 44), Interval(2, 2), Interval(44, 48), Interval(32, 32)],
        # Job 44
        [Interval(52, 56), Interval(12, 16), Interval(91, 101), Interval(36, 42), Interval(1, 1),
         Interval(92, 104), Interval(42, 44), Interval(57, 57), Interval(27, 31), Interval(70, 82),
         Interval(32, 40), Interval(54, 62), Interval(86, 100), Interval(16, 18), Interval(36, 40),
         Interval(69, 93), Interval(68, 80), Interval(18, 22), Interval(34, 44), Interval(86, 110)],
        # Job 45
        [Interval(71, 89), Interval(92, 96), Interval(65, 73), Interval(66, 72), Interval(47, 61),
         Interval(27, 33), Interval(80, 92), Interval(69, 91), Interval(6, 6), Interval(62, 82),
         Interval(61, 69), Interval(45, 45), Interval(85, 93), Interval(67, 67), Interval(6, 6),
         Interval(24, 32), Interval(70, 82), Interval(27, 29), Interval(28, 30), Interval(26, 30)],
        # Job 46
        [Interval(1, 1), Interval(73, 75), Interval(8, 8), Interval(86, 106), Interval(18, 22),
         Interval(7, 7), Interval(26, 26), Interval(22, 28), Interval(16, 20), Interval(81, 87),
         Interval(25, 33), Interval(84, 100), Interval(17, 19), Interval(34, 42), Interval(89, 97),
         Interval(7, 9), Interval(31, 33), Interval(59, 75), Interval(77, 85), Interval(15, 19)],
        # Job 47
        [Interval(36, 36), Interval(41, 41), Interval(72, 72), Interval(31, 31), Interval(25, 31),
         Interval(49, 55), Interval(14, 14), Interval(59, 59), Interval(86, 108), Interval(66, 76),
         Interval(89, 95), Interval(46, 54), Interval(4, 4), Interval(93, 99), Interval(6, 6),
         Interval(95, 103), Interval(1, 1), Interval(63, 77), Interval(56, 60), Interval(90, 94)],
        # Job 48
        [Interval(21, 27), Interval(70, 92), Interval(78, 90), Interval(57, 57), Interval(58, 60),
         Interval(87, 101), Interval(29, 33), Interval(88, 108), Interval(32, 42), Interval(61, 67),
         Interval(69, 69), Interval(50, 62), Interval(65, 77), Interval(21, 25), Interval(27, 33),
         Interval(85, 109), Interval(74, 98), Interval(25, 33), Interval(14, 18), Interval(74, 76)],
        # Job 49
        [Interval(29, 37), Interval(75, 87), Interval(51, 65), Interval(78, 84), Interval(2, 2),
         Interval(22, 28), Interval(17, 17), Interval(1, 1), Interval(70, 74), Interval(29, 37),
         Interval(18, 18), Interval(22, 22), Interval(44, 44), Interval(27, 29), Interval(63, 75),
         Interval(89, 95), Interval(90, 90), Interval(38, 48), Interval(51, 55), Interval(65, 87)],
    ],
    'name': 'INT__TAI50_20_06.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai50_20_06_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI50_20_06.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI50_20_06.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI50_20_06_F_15_01_INTERVAL_DATA
