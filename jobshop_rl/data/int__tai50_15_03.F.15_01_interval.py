"""
Problema INT__TAI50_15_03.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI50_15_03_F_15_01_INTERVAL_DATA = {
    'num_jobs': 50,
    'num_machines': 15,
    'problem_id': 'int__tai50_15_03.F.15_01_interval',
    'sequences': [
        [14, 2, 5, 1, 3, 7, 10, 4, 11, 8, 0, 9, 6, 13, 12],
        [1, 0, 5, 2, 4, 7, 3, 10, 13, 14, 12, 11, 6, 8, 9],
        [13, 14, 1, 4, 8, 7, 0, 6, 9, 2, 10, 12, 5, 3, 11],
        [9, 10, 3, 4, 12, 6, 1, 14, 0, 7, 13, 11, 5, 2, 8],
        [1, 2, 0, 3, 8, 13, 4, 7, 14, 12, 11, 10, 9, 5, 6],
        [8, 9, 2, 1, 7, 3, 14, 10, 11, 5, 12, 0, 4, 13, 6],
        [10, 14, 7, 11, 4, 3, 2, 13, 5, 8, 9, 0, 1, 6, 12],
        [12, 14, 10, 2, 1, 9, 6, 11, 13, 0, 5, 7, 3, 4, 8],
        [3, 12, 11, 8, 7, 0, 13, 2, 4, 9, 1, 10, 6, 14, 5],
        [10, 4, 6, 13, 8, 0, 14, 2, 9, 3, 1, 12, 7, 11, 5],
        [13, 4, 7, 5, 8, 3, 6, 2, 9, 11, 0, 12, 1, 10, 14],
        [4, 2, 6, 5, 1, 13, 3, 0, 14, 8, 10, 9, 12, 7, 11],
        [0, 13, 4, 11, 5, 12, 10, 3, 9, 6, 2, 14, 7, 8, 1],
        [0, 13, 3, 1, 8, 6, 12, 2, 14, 5, 11, 4, 9, 10, 7],
        [11, 0, 3, 8, 9, 5, 1, 4, 7, 13, 6, 2, 14, 12, 10],
        [11, 9, 3, 10, 5, 7, 2, 12, 0, 8, 13, 4, 6, 1, 14],
        [5, 0, 7, 6, 2, 12, 13, 11, 9, 3, 1, 8, 10, 4, 14],
        [5, 7, 12, 6, 8, 0, 1, 14, 2, 4, 13, 9, 10, 11, 3],
        [4, 8, 2, 11, 9, 3, 5, 7, 13, 10, 12, 1, 6, 14, 0],
        [10, 12, 3, 5, 1, 11, 6, 8, 14, 4, 7, 2, 9, 0, 13],
        [11, 13, 1, 6, 4, 10, 9, 7, 5, 12, 3, 2, 0, 8, 14],
        [7, 9, 14, 0, 5, 3, 13, 12, 1, 6, 2, 4, 8, 10, 11],
        [12, 0, 14, 1, 7, 9, 8, 2, 4, 5, 6, 10, 13, 3, 11],
        [8, 9, 11, 5, 10, 12, 13, 7, 1, 0, 2, 4, 3, 6, 14],
        [6, 14, 12, 1, 0, 7, 11, 10, 8, 13, 2, 5, 3, 9, 4],
        [9, 5, 13, 12, 8, 1, 3, 2, 14, 0, 11, 10, 6, 7, 4],
        [0, 6, 3, 10, 5, 4, 9, 12, 1, 14, 7, 2, 11, 13, 8],
        [5, 9, 12, 14, 10, 2, 7, 0, 6, 4, 1, 13, 11, 3, 8],
        [4, 0, 5, 11, 10, 12, 9, 7, 13, 3, 8, 2, 14, 1, 6],
        [13, 12, 3, 10, 2, 4, 7, 5, 14, 0, 8, 11, 1, 6, 9],
        [11, 14, 5, 7, 12, 6, 10, 13, 9, 2, 8, 1, 3, 0, 4],
        [1, 6, 5, 0, 11, 12, 2, 9, 4, 10, 7, 14, 13, 8, 3],
        [5, 9, 6, 14, 4, 0, 3, 11, 1, 13, 2, 7, 8, 12, 10],
        [6, 3, 13, 2, 4, 14, 0, 12, 10, 5, 1, 9, 11, 7, 8],
        [13, 9, 11, 4, 3, 0, 7, 1, 2, 14, 5, 8, 6, 10, 12],
        [8, 3, 5, 6, 2, 12, 4, 10, 7, 1, 13, 14, 0, 11, 9],
        [2, 8, 7, 4, 3, 6, 12, 5, 13, 10, 14, 9, 1, 0, 11],
        [10, 14, 13, 6, 11, 0, 1, 3, 12, 8, 7, 2, 4, 9, 5],
        [1, 8, 13, 12, 11, 7, 0, 2, 6, 3, 4, 9, 5, 10, 14],
        [7, 2, 0, 8, 5, 11, 6, 9, 12, 10, 1, 13, 14, 4, 3],
        [4, 1, 14, 6, 13, 9, 8, 12, 3, 5, 0, 10, 11, 2, 7],
        [13, 5, 6, 9, 0, 10, 4, 8, 12, 11, 1, 14, 7, 3, 2],
        [4, 7, 3, 5, 1, 10, 2, 9, 8, 13, 6, 12, 11, 14, 0],
        [9, 1, 10, 12, 8, 13, 0, 3, 2, 11, 14, 4, 5, 6, 7],
        [0, 2, 12, 10, 14, 3, 8, 9, 1, 4, 7, 5, 13, 6, 11],
        [10, 7, 14, 13, 4, 1, 12, 0, 11, 6, 2, 5, 3, 8, 9],
        [14, 7, 0, 13, 10, 11, 5, 1, 8, 3, 2, 6, 4, 12, 9],
        [9, 7, 8, 13, 10, 2, 3, 6, 4, 12, 0, 5, 1, 11, 14],
        [12, 7, 8, 14, 10, 0, 13, 4, 6, 9, 11, 5, 1, 2, 3],
        [13, 14, 6, 9, 0, 3, 8, 5, 11, 12, 10, 2, 7, 1, 4],
    ],
    'durations': [
        # Job 0
        [Interval(59, 77), Interval(21, 21), Interval(6, 8), Interval(17, 21), Interval(79, 87),
         Interval(72, 76), Interval(11, 13), Interval(60, 78), Interval(38, 40), Interval(9, 9),
         Interval(57, 69), Interval(60, 74), Interval(50, 66), Interval(34, 40), Interval(14, 16)],
        # Job 1
        [Interval(53, 71), Interval(74, 92), Interval(32, 32), Interval(48, 64), Interval(55, 67),
         Interval(58, 76), Interval(8, 10), Interval(50, 50), Interval(79, 97), Interval(85, 113),
         Interval(43, 57), Interval(74, 98), Interval(40, 44), Interval(69, 71), Interval(27, 33)],
        # Job 2
        [Interval(19, 21), Interval(36, 44), Interval(24, 32), Interval(49, 53), Interval(23, 23),
         Interval(34, 34), Interval(10, 10), Interval(63, 79), Interval(38, 44), Interval(13, 15),
         Interval(58, 66), Interval(35, 47), Interval(14, 14), Interval(62, 82), Interval(44, 52)],
        # Job 3
        [Interval(41, 53), Interval(30, 34), Interval(87, 111), Interval(46, 56), Interval(84, 86),
         Interval(47, 51), Interval(30, 34), Interval(88, 90), Interval(66, 84), Interval(24, 24),
         Interval(8, 8), Interval(45, 53), Interval(78, 94), Interval(95, 99), Interval(75, 97)],
        # Job 4
        [Interval(12, 12), Interval(62, 68), Interval(3, 3), Interval(79, 99), Interval(23, 29),
         Interval(59, 75), Interval(23, 25), Interval(21, 27), Interval(4, 4), Interval(37, 49),
         Interval(31, 35), Interval(49, 55), Interval(34, 46), Interval(79, 89), Interval(86, 112)],
        # Job 5
        [Interval(73, 81), Interval(1, 1), Interval(76, 86), Interval(54, 68), Interval(49, 53),
         Interval(13, 15), Interval(69, 87), Interval(60, 78), Interval(89, 101), Interval(17, 19),
         Interval(13, 17), Interval(58, 74), Interval(72, 76), Interval(80, 88), Interval(1, 1)],
        # Job 6
        [Interval(23, 23), Interval(56, 60), Interval(32, 34), Interval(46, 58), Interval(25, 27),
         Interval(11, 13), Interval(84, 110), Interval(78, 78), Interval(47, 55), Interval(76, 88),
         Interval(5, 5), Interval(70, 78), Interval(11, 13), Interval(25, 25), Interval(40, 40)],
        # Job 7
        [Interval(66, 70), Interval(63, 69), Interval(12, 16), Interval(92, 98), Interval(17, 21),
         Interval(86, 108), Interval(57, 59), Interval(46, 62), Interval(64, 84), Interval(5, 5),
         Interval(72, 94), Interval(89, 95), Interval(8, 8), Interval(90, 102), Interval(73, 87)],
        # Job 8
        [Interval(85, 93), Interval(71, 81), Interval(66, 82), Interval(72, 82), Interval(57, 61),
         Interval(34, 44), Interval(35, 37), Interval(35, 43), Interval(42, 48), Interval(33, 35),
         Interval(44, 52), Interval(66, 78), Interval(63, 77), Interval(70, 80), Interval(38, 46)],
        # Job 9
        [Interval(35, 41), Interval(41, 45), Interval(9, 9), Interval(25, 33), Interval(70, 94),
         Interval(4, 4), Interval(41, 43), Interval(69, 73), Interval(85, 99), Interval(26, 28),
         Interval(39, 49), Interval(67, 87), Interval(52, 58), Interval(80, 104), Interval(77, 103)],
        # Job 10
        [Interval(6, 8), Interval(57, 57), Interval(17, 23), Interval(37, 41), Interval(54, 68),
         Interval(10, 10), Interval(81, 105), Interval(30, 38), Interval(83, 87), Interval(57, 67),
         Interval(27, 31), Interval(4, 4), Interval(45, 57), Interval(61, 63), Interval(40, 54)],
        # Job 11
        [Interval(63, 67), Interval(51, 63), Interval(70, 82), Interval(81, 97), Interval(8, 10),
         Interval(52, 70), Interval(60, 68), Interval(2, 2), Interval(81, 89), Interval(79, 89),
         Interval(24, 30), Interval(65, 75), Interval(5, 5), Interval(56, 62), Interval(69, 69)],
        # Job 12
        [Interval(31, 41), Interval(31, 35), Interval(75, 83), Interval(8, 8), Interval(84, 86),
         Interval(74, 78), Interval(92, 92), Interval(5, 5), Interval(22, 24), Interval(66, 74),
         Interval(22, 26), Interval(1, 1), Interval(37, 41), Interval(1, 1), Interval(64, 78)],
        # Job 13
        [Interval(44, 44), Interval(41, 55), Interval(54, 64), Interval(56, 56), Interval(66, 88),
         Interval(12, 12), Interval(76, 98), Interval(35, 47), Interval(77, 101), Interval(22, 26),
         Interval(23, 25), Interval(51, 65), Interval(52, 60), Interval(16, 18), Interval(31, 35)],
        # Job 14
        [Interval(48, 56), Interval(17, 23), Interval(51, 63), Interval(91, 101), Interval(12, 12),
         Interval(36, 44), Interval(57, 63), Interval(7, 7), Interval(32, 36), Interval(85, 97),
         Interval(19, 23), Interval(42, 46), Interval(79, 79), Interval(46, 62), Interval(31, 39)],
        # Job 15
        [Interval(11, 13), Interval(22, 26), Interval(13, 17), Interval(57, 75), Interval(61, 63),
         Interval(4, 4), Interval(32, 42), Interval(29, 37), Interval(68, 86), Interval(67, 67),
         Interval(69, 83), Interval(37, 45), Interval(69, 85), Interval(47, 55), Interval(71, 91)],
        # Job 16
        [Interval(63, 63), Interval(52, 68), Interval(45, 53), Interval(68, 84), Interval(70, 80),
         Interval(65, 65), Interval(25, 27), Interval(67, 81), Interval(10, 12), Interval(38, 50),
         Interval(63, 71), Interval(92, 96), Interval(82, 98), Interval(54, 70), Interval(75, 97)],
        # Job 17
        [Interval(29, 33), Interval(6, 6), Interval(53, 71), Interval(80, 82), Interval(63, 81),
         Interval(20, 20), Interval(16, 20), Interval(77, 79), Interval(3, 3), Interval(85, 111),
         Interval(84, 104), Interval(20, 24), Interval(4, 4), Interval(58, 72), Interval(69, 75)],
        # Job 18
        [Interval(21, 21), Interval(38, 50), Interval(84, 90), Interval(30, 32), Interval(81, 101),
         Interval(27, 35), Interval(73, 89), Interval(10, 10), Interval(29, 33), Interval(22, 26),
         Interval(37, 39), Interval(89, 91), Interval(18, 18), Interval(2, 2), Interval(1, 1)],
        # Job 19
        [Interval(27, 35), Interval(70, 82), Interval(54, 70), Interval(1, 1), Interval(58, 74),
         Interval(31, 41), Interval(36, 36), Interval(54, 56), Interval(22, 22), Interval(83, 89),
         Interval(71, 77), Interval(7, 9), Interval(53, 65), Interval(36, 38), Interval(35, 39)],
        # Job 20
        [Interval(4, 4), Interval(68, 74), Interval(34, 44), Interval(14, 18), Interval(30, 36),
         Interval(26, 26), Interval(43, 47), Interval(87, 87), Interval(39, 45), Interval(11, 11),
         Interval(18, 18), Interval(10, 12), Interval(16, 18), Interval(68, 84), Interval(47, 55)],
        # Job 21
        [Interval(29, 39), Interval(36, 40), Interval(65, 83), Interval(47, 61), Interval(54, 66),
         Interval(79, 103), Interval(78, 84), Interval(87, 97), Interval(41, 49), Interval(50, 52),
         Interval(20, 20), Interval(63, 79), Interval(13, 15), Interval(13, 13), Interval(50, 66)],
        # Job 22
        [Interval(57, 75), Interval(13, 13), Interval(21, 21), Interval(85, 99), Interval(3, 3),
         Interval(3, 3), Interval(71, 85), Interval(46, 48), Interval(46, 46), Interval(52, 52),
         Interval(78, 96), Interval(85, 89), Interval(54, 70), Interval(70, 70), Interval(80, 100)],
        # Job 23
        [Interval(83, 87), Interval(15, 19), Interval(79, 93), Interval(90, 102), Interval(47, 63),
         Interval(74, 74), Interval(17, 19), Interval(70, 92), Interval(54, 58), Interval(3, 3),
         Interval(27, 35), Interval(14, 16), Interval(90, 94), Interval(47, 47), Interval(3, 3)],
        # Job 24
        [Interval(87, 99), Interval(32, 34), Interval(69, 79), Interval(77, 103), Interval(50, 54),
         Interval(35, 39), Interval(40, 44), Interval(26, 30), Interval(71, 95), Interval(81, 83),
         Interval(71, 73), Interval(12, 14), Interval(9, 9), Interval(50, 54), Interval(18, 24)],
        # Job 25
        [Interval(10, 12), Interval(53, 69), Interval(46, 48), Interval(10, 12), Interval(35, 47),
         Interval(6, 8), Interval(30, 32), Interval(51, 51), Interval(2, 2), Interval(80, 82),
         Interval(43, 47), Interval(23, 31), Interval(46, 58), Interval(75, 101), Interval(56, 66)],
        # Job 26
        [Interval(85, 111), Interval(46, 58), Interval(41, 41), Interval(5, 5), Interval(18, 22),
         Interval(97, 97), Interval(41, 55), Interval(23, 23), Interval(33, 35), Interval(24, 32),
         Interval(65, 85), Interval(21, 21), Interval(51, 69), Interval(86, 86), Interval(29, 39)],
        # Job 27
        [Interval(55, 55), Interval(97, 101), Interval(43, 55), Interval(38, 50), Interval(28, 28),
         Interval(32, 42), Interval(12, 12), Interval(60, 78), Interval(76, 96), Interval(71, 77),
         Interval(43, 47), Interval(91, 99), Interval(86, 108), Interval(73, 83), Interval(1, 1)],
        # Job 28
        [Interval(80, 106), Interval(41, 43), Interval(25, 25), Interval(31, 37), Interval(55, 63),
         Interval(9, 11), Interval(43, 45), Interval(38, 38), Interval(70, 90), Interval(29, 29),
         Interval(66, 70), Interval(63, 79), Interval(27, 27), Interval(21, 27), Interval(46, 46)],
        # Job 29
        [Interval(29, 29), Interval(15, 17), Interval(70, 86), Interval(31, 33), Interval(27, 33),
         Interval(64, 80), Interval(91, 91), Interval(75, 79), Interval(5, 5), Interval(85, 95),
         Interval(24, 24), Interval(6, 6), Interval(66, 74), Interval(47, 61), Interval(50, 54)],
        # Job 30
        [Interval(35, 41), Interval(60, 76), Interval(46, 58), Interval(69, 89), Interval(5, 5),
         Interval(44, 50), Interval(42, 42), Interval(4, 4), Interval(61, 71), Interval(47, 47),
         Interval(71, 71), Interval(79, 79), Interval(15, 19), Interval(56, 72), Interval(50, 56)],
        # Job 31
        [Interval(45, 57), Interval(89, 91), Interval(61, 63), Interval(97, 97), Interval(69, 85),
         Interval(30, 30), Interval(15, 19), Interval(13, 13), Interval(61, 69), Interval(60, 60),
         Interval(80, 100), Interval(12, 14), Interval(72, 84), Interval(82, 82), Interval(68, 86)],
        # Job 32
        [Interval(19, 25), Interval(38, 38), Interval(88, 100), Interval(9, 11), Interval(63, 65),
         Interval(22, 22), Interval(78, 104), Interval(60, 80), Interval(19, 25), Interval(46, 62),
         Interval(71, 93), Interval(43, 55), Interval(30, 30), Interval(59, 65), Interval(62, 70)],
        # Job 33
        [Interval(77, 99), Interval(68, 90), Interval(9, 9), Interval(16, 20), Interval(52, 56),
         Interval(20, 20), Interval(52, 66), Interval(21, 27), Interval(47, 57), Interval(61, 79),
         Interval(16, 16), Interval(32, 32), Interval(51, 69), Interval(72, 86), Interval(81, 103)],
        # Job 34
        [Interval(41, 47), Interval(7, 7), Interval(70, 86), Interval(84, 86), Interval(13, 13),
         Interval(3, 3), Interval(56, 60), Interval(53, 71), Interval(55, 63), Interval(73, 85),
         Interval(27, 35), Interval(38, 50), Interval(12, 12), Interval(70, 88), Interval(6, 6)],
        # Job 35
        [Interval(67, 77), Interval(68, 72), Interval(84, 110), Interval(22, 28), Interval(7, 9),
         Interval(87, 111), Interval(60, 70), Interval(2, 2), Interval(92, 92), Interval(3, 3),
         Interval(52, 70), Interval(92, 98), Interval(40, 44), Interval(73, 91), Interval(57, 63)],
        # Job 36
        [Interval(14, 16), Interval(78, 92), Interval(2, 2), Interval(4, 4), Interval(59, 79),
         Interval(42, 42), Interval(69, 77), Interval(66, 80), Interval(27, 29), Interval(16, 16),
         Interval(37, 37), Interval(55, 63), Interval(45, 47), Interval(56, 72), Interval(39, 43)],
        # Job 37
        [Interval(47, 63), Interval(87, 89), Interval(63, 75), Interval(48, 64), Interval(43, 53),
         Interval(17, 17), Interval(2, 2), Interval(57, 75), Interval(63, 77), Interval(55, 59),
         Interval(66, 68), Interval(33, 43), Interval(40, 50), Interval(13, 15), Interval(84, 104)],
        # Job 38
        [Interval(53, 65), Interval(99, 99), Interval(90, 104), Interval(13, 15), Interval(3, 3),
         Interval(23, 29), Interval(6, 6), Interval(46, 48), Interval(31, 39), Interval(63, 79),
         Interval(44, 54), Interval(83, 99), Interval(34, 42), Interval(72, 76), Interval(40, 44)],
        # Job 39
        [Interval(41, 41), Interval(39, 41), Interval(95, 101), Interval(49, 51), Interval(50, 58),
         Interval(13, 15), Interval(55, 73), Interval(47, 61), Interval(77, 91), Interval(26, 26),
         Interval(52, 60), Interval(66, 72), Interval(93, 99), Interval(6, 6), Interval(36, 48)],
        # Job 40
        [Interval(83, 93), Interval(40, 46), Interval(39, 41), Interval(46, 50), Interval(41, 51),
         Interval(65, 75), Interval(7, 9), Interval(34, 38), Interval(14, 18), Interval(84, 86),
         Interval(80, 84), Interval(45, 55), Interval(74, 74), Interval(24, 32), Interval(79, 95)],
        # Job 41
        [Interval(6, 6), Interval(47, 49), Interval(60, 80), Interval(85, 111), Interval(18, 20),
         Interval(22, 26), Interval(37, 37), Interval(33, 43), Interval(74, 96), Interval(86, 112),
         Interval(19, 21), Interval(65, 87), Interval(86, 102), Interval(86, 94), Interval(14, 14)],
        # Job 42
        [Interval(56, 56), Interval(13, 15), Interval(56, 66), Interval(32, 36), Interval(23, 27),
         Interval(65, 75), Interval(50, 50), Interval(13, 17), Interval(6, 6), Interval(76, 78),
         Interval(37, 37), Interval(8, 8), Interval(62, 64), Interval(34, 40), Interval(23, 27)],
        # Job 43
        [Interval(95, 95), Interval(31, 37), Interval(59, 71), Interval(87, 89), Interval(40, 46),
         Interval(38, 46), Interval(27, 33), Interval(61, 63), Interval(86, 86), Interval(51, 53),
         Interval(58, 64), Interval(14, 18), Interval(47, 49), Interval(57, 67), Interval(47, 59)],
        # Job 44
        [Interval(39, 49), Interval(89, 95), Interval(4, 4), Interval(51, 67), Interval(3, 3),
         Interval(33, 35), Interval(7, 9), Interval(70, 86), Interval(22, 22), Interval(98, 98),
         Interval(8, 10), Interval(55, 71), Interval(83, 85), Interval(50, 58), Interval(46, 60)],
        # Job 45
        [Interval(86, 96), Interval(12, 16), Interval(88, 88), Interval(46, 62), Interval(25, 33),
         Interval(60, 72), Interval(44, 52), Interval(54, 62), Interval(37, 47), Interval(26, 26),
         Interval(7, 9), Interval(7, 7), Interval(88, 110), Interval(21, 25), Interval(72, 76)],
        # Job 46
        [Interval(61, 73), Interval(66, 88), Interval(30, 34), Interval(83, 111), Interval(61, 81),
         Interval(47, 47), Interval(61, 73), Interval(92, 104), Interval(38, 48), Interval(56, 68),
         Interval(78, 90), Interval(44, 44), Interval(2, 2), Interval(55, 65), Interval(40, 52)],
        # Job 47
        [Interval(25, 29), Interval(72, 72), Interval(54, 70), Interval(6, 8), Interval(68, 84),
         Interval(3, 3), Interval(28, 32), Interval(35, 39), Interval(8, 10), Interval(12, 14),
         Interval(67, 77), Interval(91, 107), Interval(15, 17), Interval(15, 19), Interval(40, 40)],
        # Job 48
        [Interval(45, 59), Interval(94, 100), Interval(25, 25), Interval(88, 96), Interval(52, 56),
         Interval(52, 58), Interval(51, 51), Interval(82, 102), Interval(37, 43), Interval(48, 56),
         Interval(59, 65), Interval(40, 44), Interval(1, 1), Interval(56, 56), Interval(9, 9)],
        # Job 49
        [Interval(61, 67), Interval(79, 87), Interval(31, 31), Interval(40, 54), Interval(17, 21),
         Interval(59, 65), Interval(11, 11), Interval(43, 45), Interval(49, 61), Interval(54, 66),
         Interval(74, 94), Interval(64, 64), Interval(77, 89), Interval(6, 8), Interval(10, 10)],
    ],
    'name': 'INT__TAI50_15_03.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai50_15_03_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI50_15_03.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI50_15_03.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI50_15_03_F_15_01_INTERVAL_DATA
