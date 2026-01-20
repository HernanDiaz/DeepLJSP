"""
Problema INT__TAI50_20_04.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI50_20_04_F_15_01_INTERVAL_DATA = {
    'num_jobs': 50,
    'num_machines': 20,
    'problem_id': 'int__tai50_20_04.F.15_01_interval',
    'sequences': [
        [9, 6, 3, 2, 7, 1, 15, 17, 0, 18, 4, 11, 5, 13, 19, 10, 8, 16, 12, 14],
        [2, 6, 13, 14, 8, 18, 7, 11, 9, 19, 1, 15, 17, 5, 12, 16, 0, 4, 10, 3],
        [10, 11, 4, 19, 9, 12, 18, 17, 2, 16, 7, 3, 13, 6, 15, 5, 14, 0, 1, 8],
        [9, 0, 13, 2, 3, 7, 4, 6, 16, 10, 17, 15, 8, 12, 19, 18, 5, 1, 11, 14],
        [11, 9, 5, 6, 10, 19, 17, 1, 15, 16, 14, 4, 2, 0, 12, 18, 7, 13, 3, 8],
        [4, 8, 9, 3, 15, 19, 12, 17, 0, 13, 6, 10, 5, 14, 11, 2, 18, 7, 16, 1],
        [4, 2, 10, 19, 1, 16, 15, 8, 0, 5, 7, 18, 9, 17, 12, 14, 3, 13, 11, 6],
        [10, 9, 2, 7, 5, 11, 3, 18, 12, 13, 8, 4, 19, 16, 15, 6, 14, 1, 17, 0],
        [16, 4, 14, 18, 6, 19, 11, 15, 8, 17, 12, 0, 1, 9, 2, 10, 3, 7, 5, 13],
        [12, 6, 2, 11, 3, 5, 15, 7, 10, 1, 18, 8, 0, 19, 4, 17, 16, 9, 14, 13],
        [5, 18, 12, 10, 17, 14, 6, 7, 8, 16, 3, 1, 13, 4, 9, 11, 19, 0, 2, 15],
        [16, 14, 3, 2, 7, 10, 1, 13, 11, 19, 0, 9, 4, 5, 6, 18, 17, 8, 12, 15],
        [6, 0, 9, 5, 14, 18, 3, 8, 11, 2, 4, 16, 12, 19, 13, 15, 17, 7, 1, 10],
        [1, 10, 14, 7, 0, 6, 5, 18, 12, 2, 13, 15, 16, 11, 9, 17, 4, 19, 3, 8],
        [8, 3, 19, 13, 18, 5, 16, 6, 11, 7, 10, 2, 0, 12, 17, 14, 15, 4, 1, 9],
        [9, 6, 4, 0, 18, 14, 2, 19, 3, 5, 17, 7, 13, 1, 16, 11, 8, 12, 10, 15],
        [15, 10, 4, 11, 0, 16, 5, 7, 2, 18, 13, 19, 1, 3, 12, 14, 6, 9, 8, 17],
        [11, 6, 1, 9, 15, 0, 16, 10, 8, 3, 13, 5, 7, 17, 18, 12, 2, 4, 19, 14],
        [17, 16, 0, 14, 6, 13, 18, 7, 4, 19, 1, 3, 8, 15, 12, 11, 2, 9, 5, 10],
        [5, 3, 18, 0, 7, 2, 11, 6, 8, 4, 1, 14, 16, 9, 12, 15, 10, 17, 19, 13],
        [19, 13, 12, 2, 11, 18, 17, 15, 6, 16, 10, 9, 7, 1, 3, 4, 14, 8, 0, 5],
        [14, 6, 7, 1, 13, 11, 2, 3, 12, 4, 0, 8, 16, 17, 5, 10, 19, 18, 9, 15],
        [15, 12, 5, 9, 1, 13, 14, 7, 4, 6, 11, 0, 3, 16, 17, 19, 10, 2, 8, 18],
        [14, 3, 0, 18, 19, 8, 4, 9, 13, 11, 12, 10, 6, 1, 7, 15, 17, 2, 16, 5],
        [18, 16, 10, 1, 4, 2, 19, 9, 8, 12, 0, 5, 13, 6, 17, 7, 3, 11, 15, 14],
        [5, 17, 10, 4, 0, 9, 18, 8, 11, 3, 16, 15, 19, 7, 14, 12, 13, 1, 6, 2],
        [9, 18, 19, 4, 0, 8, 17, 12, 13, 10, 16, 14, 1, 6, 2, 11, 3, 7, 15, 5],
        [16, 0, 12, 8, 1, 13, 10, 3, 19, 6, 9, 18, 4, 2, 7, 15, 5, 17, 14, 11],
        [4, 12, 14, 7, 18, 17, 0, 6, 1, 9, 8, 11, 19, 3, 10, 13, 2, 16, 5, 15],
        [4, 3, 8, 1, 17, 9, 14, 11, 5, 15, 10, 16, 18, 13, 2, 0, 6, 19, 7, 12],
        [6, 7, 11, 12, 5, 19, 9, 18, 10, 1, 8, 17, 3, 0, 13, 14, 4, 2, 16, 15],
        [18, 15, 17, 12, 16, 19, 10, 8, 14, 9, 3, 1, 6, 11, 2, 0, 7, 5, 13, 4],
        [3, 16, 19, 13, 11, 9, 12, 4, 5, 15, 2, 10, 14, 8, 0, 17, 6, 7, 1, 18],
        [5, 2, 13, 17, 16, 12, 11, 8, 9, 1, 3, 10, 15, 19, 14, 18, 7, 6, 4, 0],
        [2, 14, 7, 0, 11, 18, 6, 10, 16, 4, 9, 19, 12, 1, 15, 13, 8, 3, 17, 5],
        [9, 18, 17, 11, 15, 16, 6, 19, 1, 2, 10, 5, 14, 12, 13, 4, 3, 8, 7, 0],
        [4, 14, 18, 7, 6, 13, 5, 9, 0, 3, 11, 12, 2, 17, 1, 10, 15, 19, 16, 8],
        [5, 8, 17, 9, 10, 16, 13, 7, 2, 6, 18, 19, 15, 0, 14, 4, 12, 11, 1, 3],
        [18, 8, 9, 3, 16, 10, 11, 4, 17, 0, 12, 1, 6, 15, 7, 19, 2, 14, 13, 5],
        [1, 11, 15, 7, 16, 4, 3, 0, 13, 10, 6, 9, 14, 5, 2, 8, 17, 12, 19, 18],
        [11, 6, 13, 9, 7, 0, 15, 16, 8, 4, 12, 5, 14, 10, 1, 2, 18, 17, 3, 19],
        [13, 15, 3, 18, 14, 1, 11, 16, 8, 7, 9, 0, 4, 6, 12, 17, 2, 10, 19, 5],
        [12, 3, 9, 5, 13, 19, 4, 17, 18, 6, 14, 11, 1, 8, 7, 16, 15, 2, 0, 10],
        [5, 4, 17, 9, 3, 16, 10, 2, 0, 13, 14, 11, 12, 6, 1, 7, 18, 15, 8, 19],
        [8, 18, 16, 19, 4, 10, 13, 3, 14, 15, 2, 5, 6, 17, 1, 11, 9, 0, 7, 12],
        [14, 1, 5, 17, 15, 6, 12, 10, 3, 7, 9, 18, 11, 4, 13, 8, 16, 0, 19, 2],
        [15, 10, 9, 3, 2, 8, 12, 19, 17, 0, 13, 4, 16, 6, 1, 5, 14, 7, 18, 11],
        [10, 1, 3, 7, 14, 0, 5, 11, 15, 12, 4, 17, 16, 6, 13, 9, 19, 8, 18, 2],
        [12, 17, 18, 2, 11, 9, 10, 0, 15, 5, 19, 7, 8, 16, 6, 13, 3, 1, 14, 4],
        [0, 7, 9, 18, 19, 14, 6, 8, 1, 4, 17, 12, 10, 13, 16, 2, 5, 11, 3, 15],
    ],
    'durations': [
        # Job 0
        [Interval(54, 70), Interval(3, 3), Interval(77, 77), Interval(40, 50), Interval(37, 47),
         Interval(74, 80), Interval(41, 43), Interval(68, 88), Interval(17, 23), Interval(78, 84),
         Interval(37, 41), Interval(82, 100), Interval(12, 14), Interval(46, 60), Interval(28, 32),
         Interval(90, 100), Interval(70, 94), Interval(62, 78), Interval(37, 37), Interval(47, 63)],
        # Job 1
        [Interval(50, 62), Interval(79, 101), Interval(18, 24), Interval(43, 43), Interval(11, 13),
         Interval(80, 108), Interval(69, 93), Interval(50, 66), Interval(19, 21), Interval(82, 84),
         Interval(36, 46), Interval(81, 87), Interval(14, 18), Interval(6, 6), Interval(55, 73),
         Interval(61, 65), Interval(16, 16), Interval(12, 12), Interval(89, 97), Interval(35, 43)],
        # Job 2
        [Interval(88, 102), Interval(14, 16), Interval(48, 54), Interval(46, 60), Interval(64, 70),
         Interval(46, 60), Interval(24, 28), Interval(35, 45), Interval(13, 13), Interval(34, 44),
         Interval(53, 65), Interval(89, 91), Interval(43, 47), Interval(34, 38), Interval(33, 33),
         Interval(67, 85), Interval(13, 13), Interval(72, 72), Interval(39, 45), Interval(50, 62)],
        # Job 3
        [Interval(50, 52), Interval(71, 93), Interval(62, 64), Interval(63, 69), Interval(18, 24),
         Interval(57, 75), Interval(64, 80), Interval(33, 37), Interval(63, 85), Interval(51, 69),
         Interval(84, 100), Interval(26, 30), Interval(77, 101), Interval(54, 62), Interval(33, 43),
         Interval(13, 15), Interval(84, 94), Interval(15, 19), Interval(84, 92), Interval(13, 15)],
        # Job 4
        [Interval(22, 28), Interval(33, 43), Interval(10, 10), Interval(64, 78), Interval(68, 92),
         Interval(36, 46), Interval(74, 78), Interval(88, 96), Interval(84, 88), Interval(32, 34),
         Interval(40, 44), Interval(80, 100), Interval(17, 19), Interval(15, 19), Interval(79, 103),
         Interval(24, 24), Interval(89, 103), Interval(76, 88), Interval(73, 81), Interval(75, 91)],
        # Job 5
        [Interval(47, 49), Interval(21, 21), Interval(69, 73), Interval(89, 99), Interval(55, 73),
         Interval(65, 69), Interval(18, 24), Interval(2, 2), Interval(51, 65), Interval(37, 39),
         Interval(11, 13), Interval(10, 12), Interval(54, 72), Interval(26, 28), Interval(87, 97),
         Interval(60, 68), Interval(8, 10), Interval(48, 52), Interval(52, 58), Interval(13, 17)],
        # Job 6
        [Interval(31, 35), Interval(95, 103), Interval(42, 56), Interval(63, 69), Interval(68, 86),
         Interval(81, 95), Interval(41, 43), Interval(7, 9), Interval(59, 69), Interval(2, 2),
         Interval(78, 94), Interval(68, 76), Interval(24, 28), Interval(79, 93), Interval(49, 53),
         Interval(1, 1), Interval(39, 41), Interval(29, 37), Interval(63, 85), Interval(6, 6)],
        # Job 7
        [Interval(44, 46), Interval(80, 86), Interval(50, 58), Interval(19, 19), Interval(61, 79),
         Interval(14, 18), Interval(69, 79), Interval(23, 31), Interval(72, 96), Interval(12, 14),
         Interval(6, 6), Interval(97, 97), Interval(40, 54), Interval(82, 92), Interval(28, 34),
         Interval(34, 34), Interval(32, 42), Interval(67, 85), Interval(30, 32), Interval(34, 40)],
        # Job 8
        [Interval(57, 67), Interval(83, 109), Interval(7, 7), Interval(72, 96), Interval(68, 72),
         Interval(28, 34), Interval(32, 38), Interval(34, 40), Interval(88, 110), Interval(55, 73),
         Interval(50, 56), Interval(37, 41), Interval(63, 71), Interval(18, 22), Interval(14, 16),
         Interval(51, 55), Interval(83, 83), Interval(22, 28), Interval(61, 69), Interval(74, 82)],
        # Job 9
        [Interval(93, 99), Interval(24, 24), Interval(85, 91), Interval(61, 61), Interval(10, 10),
         Interval(73, 81), Interval(42, 50), Interval(47, 51), Interval(81, 101), Interval(41, 41),
         Interval(32, 42), Interval(63, 75), Interval(37, 37), Interval(73, 97), Interval(13, 15),
         Interval(29, 39), Interval(72, 94), Interval(26, 34), Interval(33, 41), Interval(4, 4)],
        # Job 10
        [Interval(27, 31), Interval(39, 49), Interval(51, 59), Interval(48, 54), Interval(45, 53),
         Interval(39, 47), Interval(1, 1), Interval(28, 36), Interval(88, 110), Interval(47, 51),
         Interval(80, 88), Interval(48, 58), Interval(54, 60), Interval(38, 42), Interval(10, 10),
         Interval(54, 62), Interval(71, 85), Interval(26, 28), Interval(34, 34), Interval(28, 36)],
        # Job 11
        [Interval(5, 5), Interval(86, 108), Interval(32, 42), Interval(57, 69), Interval(59, 73),
         Interval(34, 46), Interval(94, 96), Interval(44, 58), Interval(7, 9), Interval(31, 39),
         Interval(63, 63), Interval(16, 18), Interval(80, 96), Interval(13, 17), Interval(31, 35),
         Interval(10, 12), Interval(10, 10), Interval(74, 94), Interval(50, 60), Interval(25, 31)],
        # Job 12
        [Interval(19, 21), Interval(7, 7), Interval(22, 24), Interval(22, 26), Interval(10, 12),
         Interval(33, 43), Interval(53, 59), Interval(72, 74), Interval(20, 24), Interval(25, 33),
         Interval(11, 13), Interval(80, 92), Interval(1, 1), Interval(20, 26), Interval(6, 6),
         Interval(45, 45), Interval(61, 79), Interval(25, 25), Interval(1, 1), Interval(69, 89)],
        # Job 13
        [Interval(57, 59), Interval(53, 71), Interval(49, 61), Interval(73, 85), Interval(48, 62),
         Interval(26, 28), Interval(77, 77), Interval(12, 14), Interval(51, 55), Interval(30, 32),
         Interval(10, 12), Interval(71, 91), Interval(6, 8), Interval(94, 94), Interval(11, 11),
         Interval(75, 93), Interval(5, 5), Interval(65, 69), Interval(19, 19), Interval(23, 25)],
        # Job 14
        [Interval(64, 84), Interval(24, 28), Interval(79, 101), Interval(64, 82), Interval(24, 32),
         Interval(16, 16), Interval(30, 30), Interval(67, 71), Interval(42, 44), Interval(46, 50),
         Interval(61, 73), Interval(81, 101), Interval(3, 3), Interval(1, 1), Interval(89, 97),
         Interval(49, 55), Interval(39, 43), Interval(27, 35), Interval(46, 62), Interval(51, 63)],
        # Job 15
        [Interval(58, 58), Interval(1, 1), Interval(87, 97), Interval(83, 83), Interval(92, 106),
         Interval(62, 66), Interval(7, 7), Interval(19, 25), Interval(28, 30), Interval(43, 53),
         Interval(64, 76), Interval(59, 79), Interval(56, 64), Interval(45, 57), Interval(52, 66),
         Interval(18, 20), Interval(22, 28), Interval(65, 69), Interval(63, 71), Interval(65, 77)],
        # Job 16
        [Interval(5, 5), Interval(45, 47), Interval(19, 19), Interval(59, 75), Interval(39, 43),
         Interval(8, 8), Interval(44, 58), Interval(10, 12), Interval(65, 69), Interval(66, 70),
         Interval(43, 49), Interval(15, 17), Interval(18, 18), Interval(12, 12), Interval(11, 11),
         Interval(10, 12), Interval(66, 68), Interval(2, 2), Interval(5, 5), Interval(87, 111)],
        # Job 17
        [Interval(47, 47), Interval(31, 39), Interval(56, 58), Interval(59, 79), Interval(91, 107),
         Interval(15, 17), Interval(79, 103), Interval(36, 36), Interval(13, 15), Interval(50, 66),
         Interval(10, 10), Interval(80, 102), Interval(61, 67), Interval(43, 45), Interval(78, 80),
         Interval(62, 70), Interval(30, 32), Interval(10, 10), Interval(48, 64), Interval(7, 7)],
        # Job 18
        [Interval(43, 47), Interval(3, 3), Interval(54, 60), Interval(42, 46), Interval(29, 39),
         Interval(27, 27), Interval(73, 75), Interval(78, 98), Interval(31, 33), Interval(4, 4),
         Interval(93, 103), Interval(22, 28), Interval(6, 8), Interval(65, 81), Interval(45, 47),
         Interval(12, 16), Interval(57, 75), Interval(80, 94), Interval(53, 57), Interval(6, 6)],
        # Job 19
        [Interval(66, 66), Interval(28, 28), Interval(4, 4), Interval(66, 72), Interval(38, 50),
         Interval(51, 65), Interval(74, 98), Interval(59, 69), Interval(14, 18), Interval(17, 21),
         Interval(9, 9), Interval(23, 27), Interval(26, 26), Interval(55, 73), Interval(44, 46),
         Interval(10, 10), Interval(83, 107), Interval(86, 112), Interval(46, 46), Interval(68, 90)],
        # Job 20
        [Interval(30, 30), Interval(8, 10), Interval(37, 37), Interval(83, 87), Interval(60, 78),
         Interval(19, 25), Interval(23, 23), Interval(84, 110), Interval(47, 53), Interval(31, 41),
         Interval(11, 13), Interval(10, 10), Interval(41, 45), Interval(1, 1), Interval(32, 34),
         Interval(6, 8), Interval(14, 16), Interval(39, 51), Interval(28, 28), Interval(3, 3)],
        # Job 21
        [Interval(44, 44), Interval(54, 64), Interval(85, 99), Interval(27, 35), Interval(67, 71),
         Interval(53, 53), Interval(55, 71), Interval(92, 96), Interval(71, 77), Interval(47, 59),
         Interval(67, 67), Interval(21, 27), Interval(9, 9), Interval(31, 31), Interval(78, 90),
         Interval(45, 55), Interval(18, 20), Interval(70, 86), Interval(3, 3), Interval(35, 43)],
        # Job 22
        [Interval(46, 46), Interval(11, 11), Interval(56, 62), Interval(27, 27), Interval(75, 83),
         Interval(76, 96), Interval(49, 53), Interval(43, 51), Interval(19, 25), Interval(14, 18),
         Interval(21, 27), Interval(75, 85), Interval(5, 5), Interval(56, 58), Interval(73, 85),
         Interval(42, 42), Interval(46, 46), Interval(99, 99), Interval(42, 56), Interval(47, 61)],
        # Job 23
        [Interval(17, 19), Interval(33, 41), Interval(18, 18), Interval(75, 77), Interval(30, 30),
         Interval(79, 97), Interval(69, 69), Interval(17, 21), Interval(27, 31), Interval(38, 44),
         Interval(58, 58), Interval(7, 9), Interval(32, 42), Interval(16, 18), Interval(23, 23),
         Interval(83, 105), Interval(79, 105), Interval(1, 1), Interval(79, 79), Interval(32, 36)],
        # Job 24
        [Interval(26, 32), Interval(83, 87), Interval(90, 92), Interval(37, 49), Interval(56, 74),
         Interval(6, 6), Interval(60, 78), Interval(4, 4), Interval(80, 108), Interval(63, 81),
         Interval(67, 85), Interval(83, 83), Interval(20, 22), Interval(42, 48), Interval(9, 11),
         Interval(72, 96), Interval(48, 52), Interval(65, 83), Interval(38, 40), Interval(53, 57)],
        # Job 25
        [Interval(58, 76), Interval(65, 87), Interval(83, 99), Interval(60, 78), Interval(13, 13),
         Interval(71, 73), Interval(84, 112), Interval(15, 17), Interval(70, 88), Interval(36, 40),
         Interval(74, 78), Interval(63, 77), Interval(30, 30), Interval(83, 87), Interval(90, 96),
         Interval(34, 44), Interval(3, 3), Interval(36, 42), Interval(81, 95), Interval(76, 98)],
        # Job 26
        [Interval(78, 102), Interval(75, 81), Interval(54, 68), Interval(57, 65), Interval(33, 35),
         Interval(4, 4), Interval(46, 58), Interval(52, 66), Interval(18, 22), Interval(25, 33),
         Interval(6, 6), Interval(55, 65), Interval(93, 93), Interval(82, 108), Interval(53, 57),
         Interval(12, 12), Interval(82, 102), Interval(21, 23), Interval(2, 2), Interval(86, 96)],
        # Job 27
        [Interval(58, 68), Interval(73, 97), Interval(75, 77), Interval(68, 76), Interval(36, 44),
         Interval(40, 44), Interval(4, 4), Interval(65, 67), Interval(63, 63), Interval(75, 87),
         Interval(8, 8), Interval(53, 69), Interval(32, 34), Interval(84, 112), Interval(93, 95),
         Interval(89, 107), Interval(30, 40), Interval(80, 100), Interval(57, 61), Interval(23, 31)],
        # Job 28
        [Interval(85, 105), Interval(5, 5), Interval(87, 95), Interval(1, 1), Interval(51, 53),
         Interval(75, 99), Interval(50, 62), Interval(78, 88), Interval(48, 60), Interval(13, 17),
         Interval(55, 55), Interval(10, 10), Interval(19, 21), Interval(63, 83), Interval(58, 60),
         Interval(27, 33), Interval(12, 16), Interval(6, 6), Interval(43, 53), Interval(26, 30)],
        # Job 29
        [Interval(3, 3), Interval(83, 103), Interval(12, 12), Interval(63, 69), Interval(19, 19),
         Interval(82, 88), Interval(64, 68), Interval(94, 98), Interval(68, 80), Interval(68, 78),
         Interval(18, 24), Interval(54, 70), Interval(83, 99), Interval(95, 99), Interval(56, 66),
         Interval(59, 65), Interval(92, 98), Interval(12, 14), Interval(31, 35), Interval(58, 66)],
        # Job 30
        [Interval(53, 55), Interval(65, 71), Interval(39, 49), Interval(4, 4), Interval(58, 66),
         Interval(77, 95), Interval(80, 90), Interval(37, 47), Interval(55, 55), Interval(67, 71),
         Interval(60, 74), Interval(71, 71), Interval(70, 88), Interval(60, 72), Interval(1, 1),
         Interval(12, 12), Interval(57, 75), Interval(81, 107), Interval(37, 45), Interval(38, 48)],
        # Job 31
        [Interval(23, 23), Interval(22, 28), Interval(18, 24), Interval(13, 17), Interval(61, 67),
         Interval(6, 6), Interval(83, 109), Interval(63, 73), Interval(55, 61), Interval(73, 77),
         Interval(66, 66), Interval(52, 62), Interval(79, 91), Interval(53, 59), Interval(22, 26),
         Interval(31, 37), Interval(64, 64), Interval(1, 1), Interval(72, 92), Interval(70, 72)],
        # Job 32
        [Interval(42, 42), Interval(92, 102), Interval(64, 66), Interval(47, 55), Interval(1, 1),
         Interval(15, 17), Interval(74, 74), Interval(50, 58), Interval(79, 95), Interval(38, 38),
         Interval(45, 51), Interval(48, 60), Interval(40, 48), Interval(50, 52), Interval(48, 48),
         Interval(72, 76), Interval(78, 86), Interval(52, 66), Interval(46, 46), Interval(55, 65)],
        # Job 33
        [Interval(52, 68), Interval(44, 56), Interval(83, 89), Interval(6, 8), Interval(10, 10),
         Interval(11, 13), Interval(45, 55), Interval(67, 67), Interval(65, 65), Interval(38, 44),
         Interval(41, 53), Interval(59, 59), Interval(40, 46), Interval(1, 1), Interval(84, 110),
         Interval(63, 71), Interval(69, 93), Interval(34, 34), Interval(23, 31), Interval(34, 44)],
        # Job 34
        [Interval(6, 8), Interval(48, 56), Interval(76, 86), Interval(51, 65), Interval(4, 4),
         Interval(53, 53), Interval(80, 92), Interval(30, 34), Interval(48, 60), Interval(34, 42),
         Interval(69, 73), Interval(39, 47), Interval(50, 66), Interval(52, 60), Interval(54, 72),
         Interval(63, 83), Interval(54, 54), Interval(51, 61), Interval(32, 36), Interval(31, 39)],
        # Job 35
        [Interval(89, 109), Interval(29, 33), Interval(90, 90), Interval(61, 73), Interval(63, 83),
         Interval(68, 80), Interval(69, 69), Interval(25, 33), Interval(83, 101), Interval(78, 94),
         Interval(82, 98), Interval(67, 77), Interval(5, 5), Interval(19, 23), Interval(10, 12),
         Interval(3, 3), Interval(3, 3), Interval(27, 31), Interval(25, 29), Interval(37, 41)],
        # Job 36
        [Interval(66, 84), Interval(71, 71), Interval(76, 102), Interval(30, 32), Interval(39, 39),
         Interval(67, 73), Interval(5, 5), Interval(58, 62), Interval(13, 13), Interval(32, 32),
         Interval(19, 25), Interval(1, 1), Interval(52, 60), Interval(49, 57), Interval(80, 88),
         Interval(45, 49), Interval(91, 91), Interval(80, 90), Interval(14, 14), Interval(10, 10)],
        # Job 37
        [Interval(55, 57), Interval(80, 108), Interval(41, 53), Interval(78, 84), Interval(20, 22),
         Interval(82, 86), Interval(88, 108), Interval(5, 5), Interval(68, 84), Interval(6, 6),
         Interval(55, 69), Interval(40, 40), Interval(54, 62), Interval(17, 19), Interval(95, 99),
         Interval(81, 97), Interval(18, 18), Interval(44, 52), Interval(38, 50), Interval(48, 48)],
        # Job 38
        [Interval(43, 47), Interval(50, 60), Interval(13, 13), Interval(13, 17), Interval(93, 99),
         Interval(17, 21), Interval(17, 19), Interval(5, 5), Interval(60, 64), Interval(70, 82),
         Interval(59, 63), Interval(13, 15), Interval(19, 25), Interval(20, 26), Interval(3, 3),
         Interval(70, 90), Interval(84, 100), Interval(74, 98), Interval(74, 100), Interval(23, 23)],
        # Job 39
        [Interval(10, 10), Interval(61, 79), Interval(5, 5), Interval(34, 42), Interval(38, 46),
         Interval(63, 65), Interval(96, 102), Interval(24, 32), Interval(27, 33), Interval(70, 94),
         Interval(92, 92), Interval(62, 66), Interval(32, 40), Interval(49, 63), Interval(11, 11),
         Interval(73, 83), Interval(2, 2), Interval(18, 18), Interval(28, 36), Interval(51, 57)],
        # Job 40
        [Interval(83, 93), Interval(80, 84), Interval(27, 27), Interval(51, 55), Interval(39, 45),
         Interval(46, 60), Interval(6, 6), Interval(74, 86), Interval(48, 62), Interval(95, 95),
         Interval(79, 87), Interval(63, 69), Interval(11, 11), Interval(67, 71), Interval(76, 102),
         Interval(78, 80), Interval(48, 52), Interval(7, 7), Interval(30, 32), Interval(45, 47)],
        # Job 41
        [Interval(30, 30), Interval(6, 6), Interval(56, 72), Interval(29, 37), Interval(36, 46),
         Interval(33, 37), Interval(87, 97), Interval(65, 65), Interval(52, 56), Interval(60, 76),
         Interval(48, 56), Interval(13, 13), Interval(6, 6), Interval(31, 41), Interval(67, 83),
         Interval(57, 61), Interval(37, 45), Interval(89, 105), Interval(21, 27), Interval(75, 79)],
        # Job 42
        [Interval(64, 76), Interval(43, 49), Interval(31, 33), Interval(34, 34), Interval(57, 77),
         Interval(9, 11), Interval(30, 34), Interval(32, 32), Interval(5, 5), Interval(4, 4),
         Interval(41, 41), Interval(13, 13), Interval(23, 25), Interval(13, 13), Interval(14, 14),
         Interval(83, 87), Interval(34, 38), Interval(18, 18), Interval(1, 1), Interval(20, 26)],
        # Job 43
        [Interval(40, 46), Interval(31, 35), Interval(14, 18), Interval(82, 100), Interval(74, 100),
         Interval(5, 5), Interval(73, 75), Interval(41, 45), Interval(78, 84), Interval(22, 24),
         Interval(46, 62), Interval(79, 87), Interval(5, 5), Interval(64, 72), Interval(41, 49),
         Interval(80, 90), Interval(7, 7), Interval(38, 50), Interval(80, 100), Interval(85, 109)],
        # Job 44
        [Interval(64, 64), Interval(84, 112), Interval(44, 50), Interval(15, 17), Interval(66, 86),
         Interval(43, 57), Interval(52, 70), Interval(61, 63), Interval(80, 96), Interval(33, 41),
         Interval(84, 94), Interval(18, 18), Interval(34, 42), Interval(10, 10), Interval(1, 1),
         Interval(34, 38), Interval(10, 10), Interval(41, 41), Interval(50, 54), Interval(48, 62)],
        # Job 45
        [Interval(74, 82), Interval(82, 96), Interval(71, 81), Interval(48, 52), Interval(88, 90),
         Interval(62, 74), Interval(44, 52), Interval(1, 1), Interval(68, 86), Interval(92, 106),
         Interval(43, 49), Interval(47, 53), Interval(76, 86), Interval(16, 20), Interval(55, 65),
         Interval(59, 71), Interval(32, 42), Interval(7, 9), Interval(41, 53), Interval(31, 31)],
        # Job 46
        [Interval(52, 60), Interval(62, 68), Interval(13, 17), Interval(12, 14), Interval(37, 43),
         Interval(40, 52), Interval(63, 85), Interval(32, 36), Interval(1, 1), Interval(56, 56),
         Interval(2, 2), Interval(91, 101), Interval(12, 12), Interval(15, 19), Interval(18, 22),
         Interval(18, 20), Interval(45, 47), Interval(91, 103), Interval(74, 76), Interval(69, 77)],
        # Job 47
        [Interval(10, 12), Interval(77, 95), Interval(80, 80), Interval(8, 8), Interval(64, 80),
         Interval(13, 17), Interval(8, 8), Interval(66, 88), Interval(22, 26), Interval(71, 85),
         Interval(47, 59), Interval(28, 30), Interval(12, 14), Interval(64, 68), Interval(57, 71),
         Interval(56, 60), Interval(17, 21), Interval(18, 18), Interval(45, 45), Interval(5, 5)],
        # Job 48
        [Interval(96, 98), Interval(73, 73), Interval(12, 14), Interval(32, 36), Interval(5, 5),
         Interval(82, 86), Interval(60, 60), Interval(19, 25), Interval(37, 43), Interval(3, 3),
         Interval(8, 8), Interval(59, 69), Interval(23, 23), Interval(64, 68), Interval(3, 3),
         Interval(31, 39), Interval(59, 63), Interval(7, 7), Interval(28, 36), Interval(38, 50)],
        # Job 49
        [Interval(31, 35), Interval(16, 16), Interval(52, 52), Interval(67, 77), Interval(50, 58),
         Interval(60, 74), Interval(61, 81), Interval(39, 43), Interval(55, 55), Interval(29, 35),
         Interval(37, 45), Interval(24, 30), Interval(48, 60), Interval(63, 81), Interval(1, 1),
         Interval(12, 16), Interval(5, 5), Interval(12, 14), Interval(73, 97), Interval(20, 20)],
    ],
    'name': 'INT__TAI50_20_04.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai50_20_04_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI50_20_04.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI50_20_04.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI50_20_04_F_15_01_INTERVAL_DATA
