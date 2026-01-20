"""
Problema INT__TAI50_20_01.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI50_20_01_F_15_01_INTERVAL_DATA = {
    'num_jobs': 50,
    'num_machines': 20,
    'problem_id': 'int__tai50_20_01.F.15_01_interval',
    'sequences': [
        [8, 19, 17, 15, 1, 2, 10, 7, 13, 18, 5, 6, 3, 4, 14, 11, 16, 0, 9, 12],
        [12, 11, 3, 16, 1, 2, 9, 8, 18, 4, 0, 19, 17, 15, 5, 10, 13, 14, 6, 7],
        [8, 6, 15, 14, 3, 7, 19, 18, 1, 11, 4, 12, 17, 13, 0, 2, 9, 10, 16, 5],
        [12, 9, 5, 16, 0, 2, 13, 18, 6, 11, 1, 19, 8, 14, 7, 4, 15, 10, 3, 17],
        [1, 3, 13, 4, 18, 5, 6, 9, 7, 8, 15, 0, 14, 10, 12, 19, 16, 17, 2, 11],
        [16, 3, 4, 14, 1, 2, 10, 9, 5, 0, 18, 19, 8, 17, 12, 15, 13, 6, 7, 11],
        [19, 4, 15, 0, 12, 13, 1, 7, 18, 5, 9, 3, 16, 8, 11, 2, 6, 14, 10, 17],
        [9, 10, 8, 4, 14, 5, 15, 7, 18, 6, 13, 19, 17, 2, 16, 11, 0, 12, 3, 1],
        [9, 13, 15, 7, 18, 2, 11, 19, 1, 8, 0, 4, 3, 12, 6, 16, 14, 17, 10, 5],
        [6, 11, 17, 8, 16, 7, 0, 14, 4, 15, 2, 13, 18, 1, 9, 19, 10, 5, 3, 12],
        [13, 4, 7, 6, 15, 11, 10, 9, 3, 17, 16, 5, 12, 1, 8, 18, 14, 0, 19, 2],
        [3, 10, 14, 0, 7, 12, 9, 19, 11, 5, 18, 1, 13, 17, 2, 6, 4, 16, 15, 8],
        [0, 10, 2, 18, 14, 12, 13, 1, 3, 9, 17, 15, 19, 4, 5, 8, 16, 6, 7, 11],
        [6, 11, 9, 8, 15, 17, 0, 4, 14, 10, 12, 2, 13, 18, 5, 1, 16, 19, 3, 7],
        [1, 9, 16, 17, 15, 2, 5, 10, 8, 14, 7, 11, 13, 0, 19, 3, 4, 18, 12, 6],
        [11, 17, 5, 1, 12, 18, 10, 9, 2, 15, 16, 6, 7, 8, 14, 4, 0, 19, 13, 3],
        [3, 5, 13, 16, 14, 11, 17, 12, 7, 18, 15, 8, 2, 0, 9, 10, 4, 6, 19, 1],
        [16, 13, 8, 17, 5, 10, 18, 12, 1, 4, 14, 9, 6, 11, 3, 7, 15, 2, 0, 19],
        [4, 14, 15, 19, 17, 18, 1, 9, 8, 7, 6, 5, 0, 3, 16, 11, 10, 12, 13, 2],
        [9, 15, 13, 4, 14, 8, 3, 2, 5, 18, 7, 16, 6, 11, 10, 0, 17, 12, 19, 1],
        [18, 2, 17, 16, 10, 8, 12, 19, 14, 1, 6, 5, 0, 7, 11, 3, 4, 15, 13, 9],
        [8, 17, 11, 15, 3, 6, 16, 13, 12, 2, 19, 9, 14, 4, 18, 1, 7, 10, 5, 0],
        [11, 17, 10, 19, 12, 18, 16, 5, 15, 4, 1, 13, 2, 7, 0, 6, 14, 9, 3, 8],
        [18, 7, 15, 9, 3, 19, 16, 11, 5, 13, 17, 10, 12, 0, 1, 14, 2, 4, 6, 8],
        [4, 17, 6, 2, 18, 5, 12, 7, 0, 14, 11, 15, 1, 19, 16, 8, 3, 9, 13, 10],
        [6, 1, 15, 2, 18, 11, 7, 14, 10, 4, 0, 3, 9, 13, 12, 19, 17, 8, 5, 16],
        [15, 6, 18, 17, 0, 19, 1, 14, 16, 9, 13, 4, 5, 8, 2, 12, 11, 3, 7, 10],
        [9, 17, 10, 6, 3, 0, 12, 18, 16, 7, 14, 4, 13, 1, 8, 19, 11, 5, 2, 15],
        [13, 4, 17, 14, 5, 11, 8, 0, 9, 18, 12, 16, 2, 6, 15, 3, 10, 1, 19, 7],
        [2, 4, 10, 12, 17, 5, 7, 11, 16, 15, 3, 9, 0, 18, 19, 6, 1, 13, 8, 14],
        [9, 2, 15, 7, 11, 17, 14, 6, 12, 3, 19, 0, 10, 1, 13, 8, 16, 5, 4, 18],
        [17, 4, 19, 15, 0, 3, 6, 2, 12, 13, 1, 8, 16, 7, 5, 10, 14, 18, 9, 11],
        [13, 6, 4, 12, 5, 10, 11, 8, 2, 18, 9, 3, 14, 0, 17, 1, 15, 16, 19, 7],
        [15, 2, 3, 7, 13, 16, 12, 14, 8, 4, 5, 0, 17, 10, 6, 18, 9, 11, 19, 1],
        [15, 8, 10, 1, 18, 11, 0, 17, 4, 12, 3, 19, 5, 2, 14, 9, 16, 7, 6, 13],
        [4, 12, 3, 18, 10, 19, 17, 6, 2, 1, 0, 5, 7, 8, 11, 14, 9, 16, 13, 15],
        [16, 17, 9, 19, 7, 1, 6, 8, 3, 13, 15, 12, 11, 2, 14, 5, 18, 4, 0, 10],
        [12, 2, 0, 13, 4, 16, 7, 3, 18, 15, 5, 9, 6, 10, 11, 1, 19, 14, 17, 8],
        [15, 1, 2, 16, 12, 19, 0, 8, 9, 5, 7, 11, 18, 4, 10, 3, 13, 14, 6, 17],
        [7, 0, 12, 10, 1, 18, 8, 5, 19, 3, 11, 15, 2, 16, 13, 6, 17, 4, 9, 14],
        [11, 2, 10, 17, 7, 4, 6, 19, 16, 8, 9, 0, 1, 5, 12, 15, 13, 18, 14, 3],
        [15, 8, 7, 5, 19, 17, 18, 14, 6, 16, 3, 2, 10, 9, 13, 12, 0, 11, 4, 1],
        [4, 3, 12, 19, 7, 11, 15, 0, 14, 9, 10, 18, 13, 5, 2, 6, 8, 17, 16, 1],
        [2, 7, 4, 18, 17, 1, 5, 8, 13, 9, 15, 3, 12, 6, 11, 16, 0, 19, 14, 10],
        [13, 14, 1, 2, 16, 0, 11, 19, 6, 7, 5, 10, 15, 12, 17, 9, 4, 18, 3, 8],
        [0, 16, 3, 7, 2, 17, 19, 4, 12, 8, 5, 6, 14, 9, 18, 10, 13, 1, 11, 15],
        [6, 13, 12, 9, 2, 19, 14, 18, 4, 5, 10, 7, 15, 8, 3, 1, 0, 11, 16, 17],
        [8, 14, 7, 10, 9, 6, 0, 2, 16, 12, 13, 5, 19, 17, 4, 15, 3, 11, 18, 1],
        [3, 10, 7, 0, 1, 13, 18, 17, 8, 14, 16, 15, 11, 19, 5, 12, 4, 9, 6, 2],
        [15, 5, 18, 19, 17, 9, 12, 14, 1, 11, 2, 7, 10, 0, 4, 6, 16, 8, 3, 13],
    ],
    'durations': [
        # Job 0
        [Interval(41, 55), Interval(40, 40), Interval(47, 61), Interval(63, 79), Interval(50, 54),
         Interval(68, 72), Interval(35, 47), Interval(66, 86), Interval(50, 54), Interval(23, 25),
         Interval(5, 5), Interval(39, 47), Interval(61, 75), Interval(9, 11), Interval(45, 53),
         Interval(9, 9), Interval(69, 93), Interval(27, 33), Interval(91, 95), Interval(15, 19)],
        # Job 1
        [Interval(77, 93), Interval(16, 20), Interval(47, 61), Interval(42, 42), Interval(37, 45),
         Interval(61, 81), Interval(58, 78), Interval(70, 94), Interval(51, 57), Interval(49, 49),
         Interval(19, 23), Interval(1, 1), Interval(56, 60), Interval(1, 1), Interval(62, 76),
         Interval(50, 66), Interval(38, 42), Interval(59, 59), Interval(65, 67), Interval(28, 30)],
        # Job 2
        [Interval(30, 36), Interval(32, 36), Interval(71, 83), Interval(40, 44), Interval(82, 108),
         Interval(2, 2), Interval(68, 74), Interval(63, 83), Interval(18, 20), Interval(22, 28),
         Interval(42, 48), Interval(77, 99), Interval(17, 21), Interval(40, 40), Interval(40, 44),
         Interval(16, 18), Interval(80, 82), Interval(64, 80), Interval(68, 72), Interval(67, 67)],
        # Job 3
        [Interval(47, 55), Interval(37, 45), Interval(72, 76), Interval(84, 110), Interval(26, 26),
         Interval(4, 4), Interval(24, 26), Interval(11, 13), Interval(15, 19), Interval(67, 85),
         Interval(6, 6), Interval(75, 83), Interval(42, 56), Interval(34, 44), Interval(1, 1),
         Interval(25, 29), Interval(41, 47), Interval(65, 85), Interval(1, 1), Interval(17, 19)],
        # Job 4
        [Interval(19, 25), Interval(94, 104), Interval(7, 7), Interval(6, 8), Interval(69, 75),
         Interval(23, 25), Interval(17, 21), Interval(70, 92), Interval(22, 24), Interval(65, 79),
         Interval(43, 57), Interval(83, 107), Interval(31, 31), Interval(64, 70), Interval(66, 68),
         Interval(21, 23), Interval(12, 12), Interval(25, 31), Interval(65, 71), Interval(78, 98)],
        # Job 5
        [Interval(45, 59), Interval(51, 51), Interval(41, 47), Interval(36, 40), Interval(60, 68),
         Interval(10, 12), Interval(61, 63), Interval(20, 20), Interval(53, 55), Interval(14, 16),
         Interval(72, 94), Interval(77, 81), Interval(47, 63), Interval(42, 54), Interval(37, 39),
         Interval(32, 42), Interval(37, 47), Interval(70, 92), Interval(86, 92), Interval(57, 63)],
        # Job 6
        [Interval(77, 87), Interval(40, 46), Interval(54, 60), Interval(1, 1), Interval(83, 95),
         Interval(10, 12), Interval(38, 44), Interval(48, 52), Interval(58, 78), Interval(2, 2),
         Interval(4, 4), Interval(62, 68), Interval(17, 23), Interval(52, 60), Interval(45, 47),
         Interval(33, 39), Interval(31, 35), Interval(51, 61), Interval(13, 13), Interval(46, 54)],
        # Job 7
        [Interval(42, 48), Interval(11, 11), Interval(61, 65), Interval(51, 67), Interval(59, 79),
         Interval(38, 40), Interval(43, 45), Interval(56, 66), Interval(65, 69), Interval(63, 81),
         Interval(64, 84), Interval(56, 62), Interval(14, 18), Interval(23, 29), Interval(79, 101),
         Interval(66, 66), Interval(48, 64), Interval(44, 50), Interval(84, 106), Interval(39, 39)],
        # Job 8
        [Interval(80, 104), Interval(2, 2), Interval(78, 98), Interval(87, 93), Interval(42, 48),
         Interval(81, 95), Interval(78, 102), Interval(93, 95), Interval(29, 39), Interval(1, 1),
         Interval(78, 84), Interval(57, 71), Interval(65, 75), Interval(50, 60), Interval(6, 8),
         Interval(29, 37), Interval(20, 22), Interval(33, 37), Interval(59, 65), Interval(55, 67)],
        # Job 9
        [Interval(82, 96), Interval(20, 22), Interval(61, 61), Interval(16, 20), Interval(73, 81),
         Interval(19, 21), Interval(41, 43), Interval(59, 59), Interval(77, 81), Interval(12, 12),
         Interval(53, 59), Interval(13, 15), Interval(19, 23), Interval(41, 45), Interval(79, 99),
         Interval(31, 31), Interval(62, 80), Interval(84, 100), Interval(47, 47), Interval(61, 81)],
        # Job 10
        [Interval(57, 65), Interval(73, 95), Interval(3, 3), Interval(64, 82), Interval(30, 40),
         Interval(32, 40), Interval(74, 84), Interval(77, 99), Interval(50, 58), Interval(89, 103),
         Interval(20, 24), Interval(64, 76), Interval(9, 11), Interval(4, 4), Interval(68, 84),
         Interval(38, 42), Interval(81, 89), Interval(76, 92), Interval(89, 97), Interval(61, 69)],
        # Job 11
        [Interval(63, 73), Interval(67, 77), Interval(67, 81), Interval(93, 101), Interval(63, 63),
         Interval(29, 37), Interval(85, 107), Interval(4, 4), Interval(55, 71), Interval(28, 34),
         Interval(1, 1), Interval(88, 108), Interval(34, 44), Interval(64, 66), Interval(62, 82),
         Interval(17, 23), Interval(6, 8), Interval(63, 63), Interval(31, 35), Interval(24, 28)],
        # Job 12
        [Interval(37, 45), Interval(60, 70), Interval(30, 38), Interval(71, 71), Interval(17, 21),
         Interval(45, 53), Interval(77, 97), Interval(57, 65), Interval(78, 80), Interval(58, 64),
         Interval(26, 32), Interval(20, 24), Interval(64, 84), Interval(64, 72), Interval(59, 61),
         Interval(21, 25), Interval(72, 92), Interval(29, 37), Interval(87, 101), Interval(36, 48)],
        # Job 13
        [Interval(17, 17), Interval(34, 46), Interval(39, 41), Interval(24, 32), Interval(6, 6),
         Interval(61, 63), Interval(72, 94), Interval(85, 105), Interval(41, 47), Interval(81, 101),
         Interval(76, 82), Interval(39, 39), Interval(58, 78), Interval(76, 82), Interval(1, 1),
         Interval(19, 21), Interval(86, 106), Interval(54, 70), Interval(56, 68), Interval(70, 70)],
        # Job 14
        [Interval(37, 41), Interval(79, 99), Interval(36, 38), Interval(7, 7), Interval(81, 87),
         Interval(52, 68), Interval(56, 66), Interval(64, 82), Interval(56, 72), Interval(63, 83),
         Interval(3, 3), Interval(75, 75), Interval(3, 3), Interval(47, 49), Interval(72, 76),
         Interval(65, 69), Interval(38, 40), Interval(29, 35), Interval(61, 77), Interval(24, 26)],
        # Job 15
        [Interval(9, 9), Interval(79, 87), Interval(26, 34), Interval(3, 3), Interval(27, 35),
         Interval(84, 102), Interval(86, 86), Interval(47, 51), Interval(34, 34), Interval(84, 98),
         Interval(54, 58), Interval(80, 80), Interval(29, 37), Interval(73, 81), Interval(31, 39),
         Interval(58, 68), Interval(62, 82), Interval(43, 49), Interval(19, 25), Interval(64, 82)],
        # Job 16
        [Interval(19, 23), Interval(40, 52), Interval(32, 34), Interval(51, 57), Interval(20, 24),
         Interval(62, 66), Interval(20, 20), Interval(67, 85), Interval(73, 81), Interval(93, 101),
         Interval(24, 32), Interval(46, 62), Interval(78, 84), Interval(92, 98), Interval(74, 88),
         Interval(66, 78), Interval(78, 82), Interval(75, 75), Interval(18, 18), Interval(73, 89)],
        # Job 17
        [Interval(51, 53), Interval(26, 34), Interval(38, 38), Interval(62, 78), Interval(22, 22),
         Interval(13, 17), Interval(61, 71), Interval(25, 27), Interval(47, 63), Interval(34, 34),
         Interval(13, 13), Interval(56, 74), Interval(84, 90), Interval(33, 43), Interval(81, 89),
         Interval(87, 91), Interval(76, 78), Interval(21, 23), Interval(63, 71), Interval(41, 47)],
        # Job 18
        [Interval(54, 72), Interval(90, 100), Interval(17, 19), Interval(89, 99), Interval(69, 77),
         Interval(44, 58), Interval(35, 35), Interval(56, 58), Interval(34, 42), Interval(62, 68),
         Interval(66, 72), Interval(51, 69), Interval(78, 102), Interval(60, 76), Interval(32, 32),
         Interval(34, 46), Interval(10, 12), Interval(69, 81), Interval(94, 100), Interval(51, 51)],
        # Job 19
        [Interval(67, 69), Interval(35, 39), Interval(34, 44), Interval(12, 14), Interval(65, 87),
         Interval(71, 83), Interval(6, 6), Interval(6, 6), Interval(46, 60), Interval(36, 46),
         Interval(71, 73), Interval(65, 77), Interval(46, 46), Interval(21, 27), Interval(45, 47),
         Interval(48, 52), Interval(11, 13), Interval(34, 44), Interval(91, 93), Interval(46, 62)],
        # Job 20
        [Interval(93, 93), Interval(81, 109), Interval(8, 8), Interval(27, 27), Interval(47, 59),
         Interval(65, 85), Interval(3, 3), Interval(42, 42), Interval(5, 5), Interval(21, 27),
         Interval(69, 77), Interval(77, 99), Interval(50, 64), Interval(19, 21), Interval(95, 103),
         Interval(38, 40), Interval(66, 82), Interval(70, 80), Interval(38, 50), Interval(24, 24)],
        # Job 21
        [Interval(82, 84), Interval(13, 15), Interval(61, 71), Interval(84, 108), Interval(11, 11),
         Interval(36, 36), Interval(17, 23), Interval(5, 5), Interval(71, 73), Interval(37, 39),
         Interval(70, 88), Interval(10, 10), Interval(23, 31), Interval(27, 27), Interval(90, 90),
         Interval(7, 9), Interval(75, 91), Interval(10, 10), Interval(54, 68), Interval(61, 77)],
        # Job 22
        [Interval(22, 22), Interval(54, 58), Interval(51, 57), Interval(50, 50), Interval(48, 54),
         Interval(8, 10), Interval(15, 15), Interval(33, 39), Interval(17, 23), Interval(69, 89),
         Interval(44, 58), Interval(79, 89), Interval(40, 40), Interval(55, 63), Interval(48, 48),
         Interval(27, 27), Interval(65, 65), Interval(38, 50), Interval(34, 46), Interval(78, 88)],
        # Job 23
        [Interval(5, 5), Interval(66, 84), Interval(43, 43), Interval(17, 17), Interval(10, 10),
         Interval(83, 101), Interval(22, 22), Interval(32, 40), Interval(7, 7), Interval(66, 76),
         Interval(77, 77), Interval(62, 78), Interval(9, 11), Interval(22, 26), Interval(78, 78),
         Interval(68, 86), Interval(48, 64), Interval(42, 42), Interval(15, 17), Interval(42, 54)],
        # Job 24
        [Interval(36, 38), Interval(95, 97), Interval(69, 93), Interval(11, 13), Interval(80, 104),
         Interval(74, 98), Interval(54, 72), Interval(77, 99), Interval(28, 28), Interval(54, 60),
         Interval(54, 62), Interval(20, 26), Interval(4, 4), Interval(81, 109), Interval(77, 83),
         Interval(11, 13), Interval(78, 86), Interval(52, 54), Interval(5, 5), Interval(65, 85)],
        # Job 25
        [Interval(50, 66), Interval(54, 64), Interval(57, 73), Interval(76, 80), Interval(67, 69),
         Interval(43, 57), Interval(35, 41), Interval(85, 109), Interval(68, 76), Interval(91, 97),
         Interval(53, 65), Interval(42, 42), Interval(5, 5), Interval(19, 19), Interval(26, 28),
         Interval(46, 62), Interval(64, 74), Interval(2, 2), Interval(51, 61), Interval(45, 57)],
        # Job 26
        [Interval(4, 4), Interval(6, 8), Interval(35, 37), Interval(31, 39), Interval(74, 86),
         Interval(93, 97), Interval(45, 57), Interval(52, 66), Interval(85, 101), Interval(5, 5),
         Interval(53, 69), Interval(4, 4), Interval(39, 47), Interval(30, 30), Interval(81, 105),
         Interval(73, 79), Interval(40, 44), Interval(88, 110), Interval(29, 31), Interval(44, 48)],
        # Job 27
        [Interval(80, 96), Interval(64, 86), Interval(80, 82), Interval(38, 42), Interval(54, 68),
         Interval(90, 98), Interval(77, 79), Interval(24, 24), Interval(18, 20), Interval(43, 45),
         Interval(83, 109), Interval(22, 24), Interval(77, 103), Interval(93, 95), Interval(72, 88),
         Interval(83, 111), Interval(22, 26), Interval(43, 45), Interval(46, 62), Interval(47, 57)],
        # Job 28
        [Interval(5, 5), Interval(95, 103), Interval(59, 61), Interval(75, 99), Interval(57, 71),
         Interval(34, 38), Interval(70, 86), Interval(29, 35), Interval(4, 4), Interval(18, 18),
         Interval(25, 27), Interval(82, 92), Interval(63, 85), Interval(26, 26), Interval(80, 100),
         Interval(40, 50), Interval(32, 38), Interval(49, 59), Interval(24, 30), Interval(23, 23)],
        # Job 29
        [Interval(88, 98), Interval(95, 95), Interval(11, 11), Interval(14, 14), Interval(97, 101),
         Interval(80, 92), Interval(38, 44), Interval(23, 29), Interval(44, 56), Interval(67, 81),
         Interval(21, 21), Interval(6, 6), Interval(62, 72), Interval(83, 91), Interval(45, 47),
         Interval(72, 96), Interval(11, 11), Interval(83, 95), Interval(87, 91), Interval(63, 69)],
        # Job 30
        [Interval(44, 56), Interval(66, 76), Interval(64, 78), Interval(5, 5), Interval(56, 64),
         Interval(25, 33), Interval(17, 17), Interval(28, 30), Interval(89, 107), Interval(61, 61),
         Interval(76, 98), Interval(53, 63), Interval(6, 6), Interval(59, 61), Interval(72, 96),
         Interval(80, 104), Interval(21, 25), Interval(23, 27), Interval(23, 23), Interval(49, 65)],
        # Job 31
        [Interval(65, 85), Interval(52, 68), Interval(73, 81), Interval(41, 55), Interval(80, 94),
         Interval(50, 54), Interval(95, 101), Interval(8, 8), Interval(50, 60), Interval(89, 105),
         Interval(52, 58), Interval(61, 75), Interval(55, 63), Interval(90, 90), Interval(44, 56),
         Interval(97, 99), Interval(57, 57), Interval(41, 45), Interval(71, 73), Interval(32, 38)],
        # Job 32
        [Interval(43, 49), Interval(22, 22), Interval(10, 12), Interval(45, 53), Interval(34, 34),
         Interval(28, 32), Interval(71, 87), Interval(65, 79), Interval(75, 79), Interval(47, 47),
         Interval(53, 57), Interval(60, 66), Interval(51, 65), Interval(88, 90), Interval(66, 76),
         Interval(82, 106), Interval(84, 106), Interval(13, 13), Interval(84, 110), Interval(44, 48)],
        # Job 33
        [Interval(23, 27), Interval(87, 109), Interval(71, 71), Interval(68, 68), Interval(7, 9),
         Interval(64, 80), Interval(57, 57), Interval(36, 42), Interval(72, 94), Interval(16, 18),
         Interval(77, 103), Interval(31, 31), Interval(69, 93), Interval(6, 6), Interval(84, 110),
         Interval(89, 107), Interval(75, 89), Interval(77, 87), Interval(46, 58), Interval(82, 82)],
        # Job 34
        [Interval(39, 45), Interval(72, 82), Interval(63, 79), Interval(17, 21), Interval(77, 83),
         Interval(28, 34), Interval(57, 75), Interval(84, 96), Interval(16, 20), Interval(13, 17),
         Interval(76, 76), Interval(53, 63), Interval(86, 98), Interval(30, 38), Interval(60, 72),
         Interval(8, 8), Interval(65, 65), Interval(61, 73), Interval(72, 96), Interval(39, 45)],
        # Job 35
        [Interval(41, 41), Interval(36, 48), Interval(62, 76), Interval(73, 89), Interval(87, 103),
         Interval(15, 17), Interval(41, 49), Interval(47, 57), Interval(45, 51), Interval(32, 38),
         Interval(69, 75), Interval(70, 90), Interval(81, 81), Interval(4, 4), Interval(3, 3),
         Interval(4, 4), Interval(82, 110), Interval(52, 54), Interval(14, 14), Interval(77, 83)],
        # Job 36
        [Interval(6, 6), Interval(6, 6), Interval(12, 12), Interval(82, 90), Interval(26, 26),
         Interval(46, 58), Interval(65, 75), Interval(85, 101), Interval(77, 85), Interval(30, 32),
         Interval(89, 89), Interval(93, 105), Interval(95, 103), Interval(68, 74), Interval(72, 76),
         Interval(6, 8), Interval(38, 48), Interval(83, 89), Interval(1, 1), Interval(88, 98)],
        # Job 37
        [Interval(43, 45), Interval(48, 60), Interval(32, 40), Interval(35, 45), Interval(68, 68),
         Interval(46, 52), Interval(41, 49), Interval(57, 59), Interval(40, 48), Interval(63, 67),
         Interval(66, 78), Interval(56, 74), Interval(53, 53), Interval(45, 51), Interval(82, 98),
         Interval(98, 98), Interval(53, 67), Interval(69, 73), Interval(24, 30), Interval(44, 52)],
        # Job 38
        [Interval(9, 9), Interval(15, 17), Interval(55, 57), Interval(25, 29), Interval(43, 57),
         Interval(50, 64), Interval(48, 62), Interval(79, 95), Interval(38, 50), Interval(40, 54),
         Interval(29, 29), Interval(80, 84), Interval(70, 90), Interval(38, 48), Interval(67, 83),
         Interval(10, 10), Interval(68, 72), Interval(33, 43), Interval(25, 31), Interval(2, 2)],
        # Job 39
        [Interval(25, 33), Interval(91, 91), Interval(82, 88), Interval(45, 57), Interval(76, 96),
         Interval(34, 34), Interval(68, 78), Interval(12, 12), Interval(12, 16), Interval(48, 54),
         Interval(1, 1), Interval(36, 40), Interval(73, 75), Interval(90, 94), Interval(57, 63),
         Interval(40, 46), Interval(31, 41), Interval(21, 25), Interval(71, 93), Interval(30, 30)],
        # Job 40
        [Interval(20, 22), Interval(92, 102), Interval(4, 4), Interval(80, 90), Interval(20, 22),
         Interval(47, 63), Interval(34, 34), Interval(59, 65), Interval(77, 79), Interval(11, 11),
         Interval(33, 35), Interval(17, 17), Interval(3, 3), Interval(38, 48), Interval(33, 43),
         Interval(39, 49), Interval(43, 47), Interval(16, 18), Interval(3, 3), Interval(83, 83)],
        # Job 41
        [Interval(28, 30), Interval(6, 6), Interval(40, 50), Interval(14, 16), Interval(56, 64),
         Interval(25, 33), Interval(86, 108), Interval(87, 95), Interval(12, 14), Interval(7, 9),
         Interval(43, 57), Interval(45, 47), Interval(66, 78), Interval(79, 93), Interval(7, 7),
         Interval(30, 30), Interval(24, 32), Interval(12, 14), Interval(25, 29), Interval(41, 43)],
        # Job 42
        [Interval(38, 38), Interval(10, 10), Interval(87, 99), Interval(6, 6), Interval(68, 76),
         Interval(38, 38), Interval(71, 75), Interval(82, 94), Interval(42, 46), Interval(57, 75),
         Interval(74, 84), Interval(44, 50), Interval(53, 69), Interval(6, 6), Interval(58, 70),
         Interval(16, 20), Interval(2, 2), Interval(6, 6), Interval(90, 92), Interval(36, 38)],
        # Job 43
        [Interval(20, 22), Interval(19, 21), Interval(44, 58), Interval(91, 101), Interval(48, 54),
         Interval(38, 46), Interval(49, 55), Interval(37, 37), Interval(74, 96), Interval(16, 20),
         Interval(38, 50), Interval(60, 60), Interval(58, 78), Interval(3, 3), Interval(6, 6),
         Interval(19, 21), Interval(73, 89), Interval(84, 108), Interval(26, 34), Interval(8, 10)],
        # Job 44
        [Interval(16, 16), Interval(49, 59), Interval(47, 59), Interval(54, 60), Interval(46, 46),
         Interval(76, 92), Interval(1, 1), Interval(74, 78), Interval(25, 27), Interval(7, 7),
         Interval(69, 69), Interval(84, 92), Interval(25, 33), Interval(69, 77), Interval(30, 34),
         Interval(48, 54), Interval(4, 4), Interval(71, 77), Interval(74, 76), Interval(68, 82)],
        # Job 45
        [Interval(25, 29), Interval(48, 60), Interval(83, 97), Interval(23, 27), Interval(90, 104),
         Interval(64, 72), Interval(12, 16), Interval(49, 59), Interval(26, 32), Interval(12, 16),
         Interval(7, 9), Interval(1, 1), Interval(53, 67), Interval(13, 13), Interval(15, 17),
         Interval(39, 43), Interval(70, 92), Interval(31, 39), Interval(17, 19), Interval(69, 89)],
        # Job 46
        [Interval(48, 64), Interval(7, 7), Interval(31, 31), Interval(52, 58), Interval(85, 85),
         Interval(30, 40), Interval(76, 88), Interval(60, 66), Interval(34, 36), Interval(50, 58),
         Interval(51, 53), Interval(73, 81), Interval(73, 91), Interval(84, 104), Interval(81, 81),
         Interval(25, 25), Interval(21, 27), Interval(50, 62), Interval(22, 24), Interval(68, 90)],
        # Job 47
        [Interval(30, 36), Interval(45, 55), Interval(19, 25), Interval(67, 73), Interval(51, 67),
         Interval(49, 53), Interval(71, 89), Interval(80, 88), Interval(40, 54), Interval(86, 90),
         Interval(27, 27), Interval(18, 18), Interval(34, 34), Interval(42, 52), Interval(4, 4),
         Interval(38, 44), Interval(55, 57), Interval(42, 42), Interval(23, 29), Interval(61, 71)],
        # Job 48
        [Interval(30, 32), Interval(76, 90), Interval(9, 9), Interval(33, 35), Interval(55, 69),
         Interval(80, 86), Interval(59, 63), Interval(35, 47), Interval(51, 65), Interval(89, 103),
         Interval(87, 87), Interval(18, 18), Interval(52, 60), Interval(2, 2), Interval(87, 103),
         Interval(19, 23), Interval(44, 58), Interval(13, 13), Interval(31, 31), Interval(86, 106)],
        # Job 49
        [Interval(57, 67), Interval(85, 105), Interval(7, 9), Interval(3, 3), Interval(23, 31),
         Interval(17, 21), Interval(31, 41), Interval(83, 111), Interval(86, 88), Interval(53, 71),
         Interval(80, 92), Interval(18, 24), Interval(36, 38), Interval(10, 12), Interval(11, 11),
         Interval(65, 69), Interval(74, 94), Interval(34, 34), Interval(48, 48), Interval(96, 98)],
    ],
    'name': 'INT__TAI50_20_01.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai50_20_01_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI50_20_01.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI50_20_01.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI50_20_01_F_15_01_INTERVAL_DATA
