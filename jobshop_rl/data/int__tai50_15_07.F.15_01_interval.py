"""
Problema INT__TAI50_15_07.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI50_15_07_F_15_01_INTERVAL_DATA = {
    'num_jobs': 50,
    'num_machines': 15,
    'problem_id': 'int__tai50_15_07.F.15_01_interval',
    'sequences': [
        [11, 3, 12, 0, 14, 9, 1, 6, 2, 13, 7, 4, 5, 8, 10],
        [2, 8, 14, 1, 0, 10, 6, 12, 7, 9, 3, 4, 11, 13, 5],
        [13, 0, 5, 6, 14, 11, 4, 3, 7, 9, 12, 8, 2, 10, 1],
        [13, 4, 9, 11, 1, 6, 12, 2, 10, 3, 0, 7, 14, 8, 5],
        [9, 3, 4, 7, 11, 0, 8, 10, 6, 5, 14, 12, 1, 2, 13],
        [2, 0, 5, 3, 12, 1, 4, 6, 9, 7, 8, 10, 14, 13, 11],
        [6, 1, 9, 2, 7, 10, 4, 11, 0, 13, 14, 12, 3, 5, 8],
        [2, 13, 14, 4, 3, 10, 7, 9, 6, 5, 1, 11, 12, 0, 8],
        [7, 14, 12, 2, 13, 8, 6, 0, 1, 5, 11, 9, 4, 3, 10],
        [10, 5, 7, 3, 12, 6, 2, 0, 13, 8, 14, 9, 11, 4, 1],
        [13, 4, 14, 6, 3, 2, 5, 8, 9, 12, 7, 0, 11, 10, 1],
        [9, 14, 7, 6, 11, 12, 4, 5, 10, 13, 3, 1, 8, 0, 2],
        [8, 10, 7, 11, 13, 1, 2, 3, 14, 12, 9, 4, 5, 6, 0],
        [5, 10, 2, 4, 7, 9, 12, 3, 13, 1, 14, 6, 8, 0, 11],
        [13, 1, 11, 7, 3, 8, 5, 4, 2, 6, 0, 14, 9, 12, 10],
        [3, 4, 7, 9, 8, 5, 11, 14, 12, 2, 6, 10, 0, 13, 1],
        [10, 3, 9, 14, 0, 7, 13, 12, 6, 11, 4, 8, 1, 2, 5],
        [9, 12, 13, 14, 6, 2, 4, 7, 0, 8, 11, 3, 10, 5, 1],
        [7, 3, 6, 12, 13, 14, 0, 5, 8, 1, 11, 2, 10, 9, 4],
        [3, 11, 12, 4, 6, 0, 13, 8, 5, 9, 7, 1, 10, 14, 2],
        [4, 2, 1, 3, 13, 10, 12, 8, 14, 5, 7, 6, 11, 0, 9],
        [7, 8, 5, 3, 13, 0, 10, 12, 11, 6, 2, 1, 4, 9, 14],
        [8, 13, 14, 5, 12, 11, 10, 9, 2, 3, 7, 0, 6, 1, 4],
        [0, 9, 1, 8, 6, 12, 5, 7, 4, 3, 2, 13, 10, 14, 11],
        [8, 5, 7, 2, 6, 11, 13, 4, 9, 0, 1, 14, 12, 10, 3],
        [10, 11, 3, 8, 2, 7, 14, 4, 1, 5, 0, 6, 9, 13, 12],
        [11, 0, 5, 8, 9, 4, 1, 6, 2, 3, 14, 10, 13, 12, 7],
        [11, 0, 8, 2, 1, 6, 13, 9, 14, 12, 10, 4, 5, 3, 7],
        [2, 12, 7, 4, 13, 8, 0, 9, 5, 11, 1, 3, 10, 6, 14],
        [8, 3, 6, 1, 12, 7, 11, 4, 9, 2, 10, 14, 13, 5, 0],
        [2, 6, 7, 13, 8, 3, 1, 10, 14, 11, 9, 5, 12, 4, 0],
        [13, 5, 2, 12, 1, 6, 4, 0, 3, 8, 7, 9, 11, 10, 14],
        [0, 13, 4, 10, 14, 7, 8, 1, 3, 9, 6, 5, 11, 12, 2],
        [4, 13, 10, 5, 8, 2, 1, 3, 6, 14, 12, 7, 11, 9, 0],
        [9, 13, 3, 5, 12, 14, 6, 1, 4, 10, 2, 7, 8, 11, 0],
        [12, 6, 11, 4, 1, 9, 8, 5, 0, 13, 2, 14, 10, 3, 7],
        [3, 10, 4, 13, 9, 7, 14, 12, 11, 8, 2, 1, 0, 5, 6],
        [13, 12, 1, 2, 8, 0, 7, 4, 10, 6, 9, 5, 3, 11, 14],
        [13, 8, 2, 7, 11, 12, 10, 9, 6, 4, 1, 0, 3, 5, 14],
        [6, 11, 3, 4, 8, 2, 10, 13, 7, 5, 9, 1, 14, 0, 12],
        [8, 2, 7, 13, 9, 3, 14, 12, 0, 1, 10, 6, 5, 11, 4],
        [6, 4, 8, 9, 2, 5, 13, 1, 12, 11, 14, 0, 7, 10, 3],
        [13, 9, 12, 3, 14, 5, 8, 7, 10, 4, 11, 0, 1, 2, 6],
        [7, 3, 10, 1, 8, 5, 0, 11, 9, 13, 2, 4, 14, 6, 12],
        [11, 13, 8, 1, 12, 4, 2, 10, 6, 9, 3, 14, 0, 7, 5],
        [1, 11, 10, 7, 5, 3, 14, 2, 13, 6, 4, 9, 0, 12, 8],
        [14, 11, 1, 8, 5, 13, 0, 9, 4, 12, 6, 10, 3, 2, 7],
        [10, 5, 7, 2, 11, 4, 3, 14, 9, 0, 12, 6, 1, 13, 8],
        [14, 12, 10, 6, 4, 13, 8, 7, 2, 11, 5, 3, 1, 0, 9],
        [12, 2, 10, 3, 4, 0, 13, 14, 7, 5, 6, 8, 1, 11, 9],
    ],
    'durations': [
        # Job 0
        [Interval(26, 34), Interval(16, 16), Interval(62, 80), Interval(27, 33), Interval(75, 81),
         Interval(45, 47), Interval(16, 20), Interval(28, 36), Interval(33, 35), Interval(83, 93),
         Interval(84, 104), Interval(77, 93), Interval(71, 95), Interval(28, 32), Interval(70, 76)],
        # Job 1
        [Interval(12, 16), Interval(46, 56), Interval(6, 6), Interval(33, 33), Interval(15, 19),
         Interval(20, 24), Interval(55, 71), Interval(62, 80), Interval(14, 14), Interval(78, 96),
         Interval(50, 66), Interval(32, 42), Interval(47, 63), Interval(70, 76), Interval(77, 79)],
        # Job 2
        [Interval(35, 43), Interval(25, 27), Interval(71, 87), Interval(9, 11), Interval(46, 50),
         Interval(48, 48), Interval(95, 99), Interval(21, 23), Interval(79, 99), Interval(1, 1),
         Interval(3, 3), Interval(41, 47), Interval(8, 10), Interval(73, 81), Interval(34, 46)],
        # Job 3
        [Interval(76, 82), Interval(57, 75), Interval(36, 42), Interval(54, 68), Interval(53, 61),
         Interval(84, 108), Interval(88, 108), Interval(54, 54), Interval(84, 92), Interval(20, 22),
         Interval(91, 93), Interval(3, 3), Interval(35, 43), Interval(21, 21), Interval(73, 73)],
        # Job 4
        [Interval(5, 5), Interval(60, 70), Interval(84, 102), Interval(88, 92), Interval(55, 73),
         Interval(30, 30), Interval(89, 97), Interval(78, 98), Interval(78, 104), Interval(41, 53),
         Interval(25, 27), Interval(68, 90), Interval(3, 3), Interval(66, 88), Interval(36, 42)],
        # Job 5
        [Interval(6, 6), Interval(57, 65), Interval(80, 104), Interval(21, 23), Interval(16, 20),
         Interval(50, 54), Interval(77, 87), Interval(43, 53), Interval(31, 33), Interval(68, 78),
         Interval(43, 55), Interval(14, 18), Interval(71, 81), Interval(50, 60), Interval(33, 43)],
        # Job 6
        [Interval(14, 18), Interval(29, 29), Interval(89, 97), Interval(87, 91), Interval(58, 64),
         Interval(45, 49), Interval(22, 28), Interval(36, 40), Interval(25, 31), Interval(40, 52),
         Interval(93, 93), Interval(63, 73), Interval(93, 105), Interval(39, 43), Interval(54, 64)],
        # Job 7
        [Interval(49, 51), Interval(77, 77), Interval(11, 11), Interval(75, 83), Interval(85, 111),
         Interval(64, 68), Interval(20, 26), Interval(13, 17), Interval(24, 24), Interval(35, 47),
         Interval(7, 9), Interval(49, 65), Interval(66, 70), Interval(49, 55), Interval(28, 32)],
        # Job 8
        [Interval(24, 28), Interval(34, 38), Interval(74, 84), Interval(82, 102), Interval(87, 99),
         Interval(11, 11), Interval(16, 20), Interval(68, 74), Interval(23, 29), Interval(88, 102),
         Interval(14, 14), Interval(80, 92), Interval(38, 44), Interval(3, 3), Interval(42, 52)],
        # Job 9
        [Interval(13, 15), Interval(15, 17), Interval(52, 60), Interval(71, 77), Interval(89, 95),
         Interval(29, 37), Interval(80, 106), Interval(66, 70), Interval(68, 72), Interval(35, 41),
         Interval(62, 66), Interval(69, 89), Interval(7, 9), Interval(65, 73), Interval(64, 84)],
        # Job 10
        [Interval(74, 100), Interval(65, 83), Interval(84, 84), Interval(67, 89), Interval(46, 52),
         Interval(40, 50), Interval(44, 44), Interval(46, 60), Interval(73, 93), Interval(27, 29),
         Interval(3, 3), Interval(44, 52), Interval(6, 6), Interval(48, 56), Interval(47, 59)],
        # Job 11
        [Interval(70, 72), Interval(8, 10), Interval(71, 75), Interval(81, 99), Interval(54, 62),
         Interval(15, 17), Interval(80, 100), Interval(46, 62), Interval(45, 51), Interval(61, 67),
         Interval(16, 18), Interval(57, 69), Interval(59, 69), Interval(93, 103), Interval(96, 96)],
        # Job 12
        [Interval(50, 66), Interval(44, 50), Interval(90, 100), Interval(33, 35), Interval(14, 14),
         Interval(11, 11), Interval(2, 2), Interval(52, 52), Interval(28, 30), Interval(62, 68),
         Interval(79, 93), Interval(57, 63), Interval(12, 14), Interval(5, 5), Interval(16, 16)],
        # Job 13
        [Interval(55, 73), Interval(27, 31), Interval(35, 35), Interval(6, 6), Interval(77, 103),
         Interval(39, 45), Interval(31, 41), Interval(25, 33), Interval(49, 65), Interval(35, 43),
         Interval(49, 55), Interval(34, 44), Interval(87, 99), Interval(20, 22), Interval(70, 84)],
        # Job 14
        [Interval(78, 92), Interval(84, 112), Interval(39, 49), Interval(81, 89), Interval(43, 47),
         Interval(58, 70), Interval(32, 34), Interval(46, 52), Interval(22, 24), Interval(78, 90),
         Interval(49, 57), Interval(17, 17), Interval(48, 48), Interval(27, 35), Interval(10, 12)],
        # Job 15
        [Interval(29, 37), Interval(80, 98), Interval(43, 53), Interval(17, 23), Interval(94, 96),
         Interval(49, 65), Interval(7, 9), Interval(17, 21), Interval(21, 21), Interval(33, 39),
         Interval(59, 71), Interval(33, 41), Interval(85, 101), Interval(4, 4), Interval(2, 2)],
        # Job 16
        [Interval(45, 57), Interval(57, 57), Interval(61, 77), Interval(67, 81), Interval(84, 106),
         Interval(74, 84), Interval(37, 37), Interval(78, 86), Interval(68, 82), Interval(18, 22),
         Interval(43, 55), Interval(36, 40), Interval(76, 80), Interval(89, 105), Interval(65, 81)],
        # Job 17
        [Interval(59, 77), Interval(85, 97), Interval(5, 5), Interval(43, 57), Interval(32, 32),
         Interval(41, 55), Interval(39, 39), Interval(70, 92), Interval(32, 32), Interval(58, 78),
         Interval(83, 101), Interval(68, 80), Interval(24, 30), Interval(57, 63), Interval(59, 59)],
        # Job 18
        [Interval(70, 94), Interval(61, 65), Interval(18, 18), Interval(29, 35), Interval(60, 78),
         Interval(74, 90), Interval(76, 76), Interval(37, 41), Interval(64, 80), Interval(87, 93),
         Interval(4, 4), Interval(54, 54), Interval(76, 82), Interval(70, 92), Interval(66, 78)],
        # Job 19
        [Interval(86, 110), Interval(85, 109), Interval(32, 42), Interval(95, 95), Interval(91, 95),
         Interval(54, 58), Interval(45, 47), Interval(82, 88), Interval(6, 8), Interval(69, 87),
         Interval(68, 74), Interval(64, 74), Interval(45, 49), Interval(35, 47), Interval(55, 73)],
        # Job 20
        [Interval(59, 71), Interval(64, 64), Interval(27, 29), Interval(46, 46), Interval(25, 29),
         Interval(51, 55), Interval(6, 6), Interval(71, 71), Interval(11, 13), Interval(14, 16),
         Interval(54, 68), Interval(81, 97), Interval(48, 64), Interval(33, 37), Interval(8, 10)],
        # Job 21
        [Interval(76, 96), Interval(78, 94), Interval(63, 81), Interval(13, 13), Interval(65, 73),
         Interval(36, 42), Interval(95, 101), Interval(27, 29), Interval(29, 35), Interval(61, 67),
         Interval(20, 22), Interval(75, 97), Interval(43, 57), Interval(8, 8), Interval(88, 92)],
        # Job 22
        [Interval(88, 104), Interval(75, 89), Interval(2, 2), Interval(4, 4), Interval(27, 27),
         Interval(43, 43), Interval(35, 35), Interval(66, 80), Interval(95, 99), Interval(18, 24),
         Interval(78, 78), Interval(85, 105), Interval(74, 78), Interval(63, 83), Interval(81, 97)],
        # Job 23
        [Interval(18, 20), Interval(15, 19), Interval(55, 55), Interval(50, 56), Interval(77, 101),
         Interval(39, 41), Interval(3, 3), Interval(3, 3), Interval(12, 16), Interval(38, 42),
         Interval(67, 71), Interval(50, 50), Interval(19, 21), Interval(39, 43), Interval(28, 32)],
        # Job 24
        [Interval(8, 10), Interval(71, 79), Interval(63, 71), Interval(4, 4), Interval(8, 8),
         Interval(66, 74), Interval(33, 43), Interval(1, 1), Interval(97, 101), Interval(49, 49),
         Interval(38, 48), Interval(70, 78), Interval(30, 32), Interval(8, 10), Interval(1, 1)],
        # Job 25
        [Interval(74, 96), Interval(79, 101), Interval(92, 96), Interval(13, 17), Interval(63, 83),
         Interval(46, 54), Interval(78, 84), Interval(26, 26), Interval(90, 92), Interval(10, 10),
         Interval(50, 66), Interval(28, 36), Interval(67, 89), Interval(1, 1), Interval(6, 8)],
        # Job 26
        [Interval(50, 66), Interval(83, 107), Interval(31, 31), Interval(90, 108), Interval(89, 89),
         Interval(79, 105), Interval(18, 18), Interval(40, 44), Interval(83, 107), Interval(6, 8),
         Interval(80, 82), Interval(40, 54), Interval(53, 53), Interval(80, 108), Interval(52, 52)],
        # Job 27
        [Interval(13, 13), Interval(50, 64), Interval(39, 51), Interval(70, 72), Interval(14, 18),
         Interval(84, 96), Interval(22, 28), Interval(46, 58), Interval(69, 75), Interval(11, 11),
         Interval(20, 22), Interval(24, 30), Interval(32, 36), Interval(76, 102), Interval(27, 27)],
        # Job 28
        [Interval(40, 40), Interval(40, 48), Interval(16, 18), Interval(82, 106), Interval(38, 40),
         Interval(49, 49), Interval(46, 58), Interval(17, 17), Interval(76, 82), Interval(39, 49),
         Interval(70, 70), Interval(1, 1), Interval(58, 76), Interval(1, 1), Interval(8, 8)],
        # Job 29
        [Interval(98, 98), Interval(35, 41), Interval(48, 58), Interval(93, 103), Interval(36, 46),
         Interval(55, 71), Interval(2, 2), Interval(68, 68), Interval(27, 29), Interval(71, 79),
         Interval(14, 14), Interval(20, 22), Interval(7, 9), Interval(63, 67), Interval(1, 1)],
        # Job 30
        [Interval(5, 5), Interval(36, 44), Interval(24, 30), Interval(82, 104), Interval(57, 73),
         Interval(88, 98), Interval(7, 7), Interval(36, 42), Interval(42, 42), Interval(8, 8),
         Interval(29, 29), Interval(23, 31), Interval(50, 64), Interval(16, 18), Interval(68, 86)],
        # Job 31
        [Interval(39, 39), Interval(18, 18), Interval(17, 17), Interval(84, 102), Interval(8, 8),
         Interval(50, 64), Interval(62, 70), Interval(71, 81), Interval(28, 28), Interval(19, 23),
         Interval(2, 2), Interval(70, 94), Interval(61, 71), Interval(77, 77), Interval(83, 105)],
        # Job 32
        [Interval(64, 86), Interval(13, 13), Interval(45, 51), Interval(12, 14), Interval(38, 40),
         Interval(16, 16), Interval(59, 79), Interval(34, 44), Interval(30, 40), Interval(64, 86),
         Interval(74, 96), Interval(48, 62), Interval(45, 45), Interval(52, 58), Interval(79, 91)],
        # Job 33
        [Interval(75, 95), Interval(70, 94), Interval(13, 13), Interval(79, 99), Interval(33, 35),
         Interval(10, 10), Interval(83, 107), Interval(33, 43), Interval(4, 4), Interval(9, 11),
         Interval(73, 95), Interval(85, 91), Interval(64, 66), Interval(22, 28), Interval(45, 55)],
        # Job 34
        [Interval(66, 84), Interval(69, 79), Interval(82, 86), Interval(64, 78), Interval(54, 54),
         Interval(52, 54), Interval(83, 89), Interval(10, 12), Interval(67, 77), Interval(25, 29),
         Interval(78, 100), Interval(52, 68), Interval(24, 26), Interval(15, 19), Interval(80, 92)],
        # Job 35
        [Interval(16, 16), Interval(58, 74), Interval(21, 27), Interval(6, 6), Interval(73, 89),
         Interval(23, 29), Interval(62, 74), Interval(41, 41), Interval(2, 2), Interval(75, 99),
         Interval(83, 89), Interval(68, 74), Interval(29, 35), Interval(32, 36), Interval(65, 73)],
        # Job 36
        [Interval(20, 24), Interval(14, 18), Interval(45, 45), Interval(53, 59), Interval(7, 9),
         Interval(59, 65), Interval(20, 20), Interval(84, 84), Interval(81, 93), Interval(57, 61),
         Interval(46, 60), Interval(78, 84), Interval(37, 49), Interval(3, 3), Interval(22, 22)],
        # Job 37
        [Interval(25, 31), Interval(20, 26), Interval(59, 73), Interval(26, 28), Interval(42, 56),
         Interval(42, 50), Interval(47, 51), Interval(63, 65), Interval(37, 49), Interval(11, 13),
         Interval(90, 100), Interval(34, 42), Interval(28, 34), Interval(49, 49), Interval(17, 19)],
        # Job 38
        [Interval(19, 21), Interval(19, 25), Interval(89, 91), Interval(75, 93), Interval(12, 16),
         Interval(33, 39), Interval(5, 5), Interval(73, 87), Interval(89, 109), Interval(90, 96),
         Interval(63, 71), Interval(58, 58), Interval(36, 38), Interval(13, 13), Interval(54, 56)],
        # Job 39
        [Interval(91, 105), Interval(82, 94), Interval(33, 43), Interval(83, 107), Interval(79, 95),
         Interval(67, 71), Interval(91, 107), Interval(82, 88), Interval(73, 77), Interval(34, 44),
         Interval(72, 82), Interval(53, 61), Interval(80, 84), Interval(91, 101), Interval(46, 58)],
        # Job 40
        [Interval(9, 9), Interval(80, 98), Interval(77, 87), Interval(71, 91), Interval(16, 16),
         Interval(39, 41), Interval(67, 81), Interval(27, 27), Interval(29, 37), Interval(30, 36),
         Interval(15, 15), Interval(67, 89), Interval(51, 65), Interval(72, 86), Interval(25, 31)],
        # Job 41
        [Interval(63, 65), Interval(79, 105), Interval(7, 9), Interval(41, 55), Interval(71, 79),
         Interval(25, 33), Interval(64, 74), Interval(32, 34), Interval(80, 86), Interval(19, 19),
         Interval(88, 106), Interval(68, 80), Interval(93, 103), Interval(3, 3), Interval(36, 42)],
        # Job 42
        [Interval(63, 73), Interval(87, 87), Interval(78, 98), Interval(71, 73), Interval(83, 85),
         Interval(25, 27), Interval(11, 11), Interval(86, 104), Interval(86, 102), Interval(90, 90),
         Interval(7, 9), Interval(16, 18), Interval(53, 53), Interval(86, 98), Interval(6, 6)],
        # Job 43
        [Interval(87, 107), Interval(87, 105), Interval(29, 29), Interval(68, 68), Interval(93, 99),
         Interval(66, 72), Interval(82, 108), Interval(89, 91), Interval(62, 72), Interval(47, 59),
         Interval(20, 26), Interval(18, 18), Interval(46, 62), Interval(47, 51), Interval(16, 20)],
        # Job 44
        [Interval(70, 86), Interval(44, 44), Interval(69, 69), Interval(23, 27), Interval(42, 54),
         Interval(77, 77), Interval(1, 1), Interval(65, 75), Interval(12, 16), Interval(24, 26),
         Interval(82, 108), Interval(25, 25), Interval(46, 60), Interval(55, 73), Interval(36, 42)],
        # Job 45
        [Interval(3, 3), Interval(73, 87), Interval(65, 75), Interval(52, 66), Interval(43, 43),
         Interval(50, 58), Interval(50, 58), Interval(53, 65), Interval(26, 32), Interval(60, 64),
         Interval(81, 97), Interval(3, 3), Interval(51, 67), Interval(74, 84), Interval(7, 9)],
        # Job 46
        [Interval(33, 43), Interval(15, 15), Interval(17, 19), Interval(71, 81), Interval(18, 24),
         Interval(74, 90), Interval(78, 90), Interval(53, 53), Interval(17, 19), Interval(63, 85),
         Interval(55, 63), Interval(61, 61), Interval(10, 12), Interval(53, 63), Interval(9, 11)],
        # Job 47
        [Interval(20, 24), Interval(7, 7), Interval(81, 97), Interval(36, 42), Interval(41, 47),
         Interval(37, 45), Interval(39, 43), Interval(73, 93), Interval(54, 54), Interval(74, 100),
         Interval(83, 89), Interval(7, 7), Interval(67, 73), Interval(53, 57), Interval(70, 76)],
        # Job 48
        [Interval(5, 5), Interval(59, 59), Interval(19, 25), Interval(55, 63), Interval(62, 74),
         Interval(94, 104), Interval(39, 43), Interval(27, 27), Interval(58, 66), Interval(77, 83),
         Interval(29, 31), Interval(36, 38), Interval(51, 69), Interval(67, 85), Interval(4, 4)],
        # Job 49
        [Interval(23, 25), Interval(89, 101), Interval(66, 68), Interval(77, 93), Interval(7, 9),
         Interval(13, 17), Interval(73, 73), Interval(49, 55), Interval(11, 13), Interval(38, 40),
         Interval(15, 17), Interval(60, 64), Interval(56, 66), Interval(8, 10), Interval(53, 53)],
    ],
    'name': 'INT__TAI50_15_07.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai50_15_07_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI50_15_07.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI50_15_07.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI50_15_07_F_15_01_INTERVAL_DATA
