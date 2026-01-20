"""
Problema INT__TAI50_20_09.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI50_20_09_F_15_01_INTERVAL_DATA = {
    'num_jobs': 50,
    'num_machines': 20,
    'problem_id': 'int__tai50_20_09.F.15_01_interval',
    'sequences': [
        [2, 6, 0, 18, 9, 12, 5, 10, 19, 16, 15, 7, 3, 13, 8, 1, 17, 14, 4, 11],
        [3, 0, 13, 12, 2, 18, 4, 11, 1, 16, 17, 10, 19, 5, 8, 15, 6, 9, 14, 7],
        [17, 7, 15, 2, 19, 0, 6, 1, 18, 13, 5, 11, 14, 3, 16, 4, 10, 12, 9, 8],
        [3, 5, 11, 15, 7, 12, 8, 17, 18, 6, 16, 14, 9, 0, 1, 19, 4, 2, 13, 10],
        [19, 17, 11, 14, 0, 6, 3, 1, 15, 10, 7, 13, 18, 2, 9, 8, 5, 16, 12, 4],
        [11, 16, 1, 14, 9, 7, 0, 6, 17, 5, 4, 8, 19, 2, 12, 18, 13, 10, 15, 3],
        [18, 12, 3, 19, 2, 15, 1, 4, 8, 9, 16, 17, 14, 10, 7, 5, 0, 11, 13, 6],
        [6, 19, 1, 0, 16, 7, 17, 10, 12, 15, 14, 11, 8, 4, 18, 13, 2, 9, 3, 5],
        [13, 12, 19, 17, 14, 15, 11, 1, 7, 2, 16, 10, 8, 4, 6, 3, 5, 9, 0, 18],
        [7, 18, 6, 13, 2, 16, 0, 3, 4, 15, 5, 11, 9, 1, 10, 19, 17, 12, 14, 8],
        [3, 8, 19, 4, 7, 1, 0, 14, 16, 12, 13, 11, 15, 10, 5, 6, 2, 9, 18, 17],
        [4, 18, 3, 12, 14, 13, 1, 16, 10, 9, 11, 15, 2, 19, 8, 7, 5, 0, 17, 6],
        [17, 3, 7, 5, 16, 11, 6, 19, 9, 0, 12, 15, 10, 13, 8, 14, 1, 4, 2, 18],
        [0, 13, 8, 14, 2, 11, 1, 16, 17, 7, 12, 9, 15, 5, 19, 4, 18, 6, 3, 10],
        [15, 11, 3, 1, 9, 13, 19, 8, 12, 7, 5, 14, 2, 17, 6, 18, 16, 10, 0, 4],
        [7, 14, 3, 6, 18, 12, 19, 9, 0, 1, 11, 16, 15, 5, 2, 4, 17, 10, 8, 13],
        [9, 15, 8, 13, 7, 17, 4, 2, 18, 14, 11, 12, 0, 5, 6, 3, 16, 1, 19, 10],
        [14, 3, 18, 7, 17, 5, 15, 0, 9, 19, 10, 4, 8, 11, 13, 6, 12, 1, 16, 2],
        [12, 6, 11, 17, 3, 18, 4, 14, 9, 1, 2, 16, 13, 0, 10, 5, 15, 7, 19, 8],
        [11, 5, 19, 0, 13, 3, 7, 16, 10, 6, 9, 15, 2, 4, 17, 14, 1, 12, 8, 18],
        [0, 9, 15, 3, 7, 1, 4, 19, 13, 5, 17, 14, 11, 6, 2, 18, 10, 12, 8, 16],
        [2, 15, 4, 17, 5, 10, 16, 18, 14, 3, 1, 0, 19, 12, 6, 11, 9, 13, 7, 8],
        [19, 15, 16, 6, 11, 3, 12, 18, 4, 17, 14, 9, 8, 0, 1, 7, 5, 2, 13, 10],
        [6, 18, 4, 5, 17, 16, 3, 7, 9, 1, 19, 12, 14, 8, 10, 13, 15, 11, 2, 0],
        [8, 5, 3, 12, 6, 7, 13, 19, 0, 10, 14, 11, 16, 17, 15, 2, 9, 4, 18, 1],
        [17, 12, 11, 19, 9, 5, 2, 6, 3, 16, 14, 1, 18, 10, 13, 15, 4, 7, 0, 8],
        [10, 16, 1, 12, 15, 6, 9, 0, 11, 7, 18, 19, 8, 4, 5, 17, 14, 13, 2, 3],
        [17, 13, 5, 11, 15, 16, 10, 12, 1, 14, 3, 9, 19, 8, 0, 6, 2, 4, 18, 7],
        [16, 13, 18, 7, 3, 2, 8, 17, 19, 5, 6, 9, 0, 4, 12, 1, 15, 11, 10, 14],
        [7, 6, 12, 9, 16, 0, 5, 18, 13, 2, 3, 10, 11, 15, 1, 4, 8, 17, 14, 19],
        [13, 10, 9, 16, 6, 0, 18, 19, 2, 3, 14, 5, 4, 15, 11, 12, 8, 17, 7, 1],
        [11, 17, 15, 1, 4, 6, 13, 3, 12, 2, 7, 14, 5, 8, 16, 19, 10, 9, 0, 18],
        [8, 10, 0, 7, 17, 2, 16, 5, 3, 9, 18, 11, 13, 19, 15, 12, 1, 4, 14, 6],
        [19, 17, 16, 3, 8, 6, 9, 10, 0, 5, 18, 4, 15, 7, 14, 12, 13, 11, 2, 1],
        [19, 14, 10, 15, 12, 0, 8, 17, 6, 9, 16, 11, 4, 7, 5, 13, 3, 2, 18, 1],
        [10, 6, 3, 4, 0, 11, 12, 1, 8, 7, 2, 17, 16, 5, 15, 18, 19, 14, 9, 13],
        [15, 11, 6, 12, 9, 18, 7, 5, 1, 0, 17, 19, 10, 8, 4, 3, 16, 2, 13, 14],
        [2, 11, 13, 10, 12, 3, 5, 1, 16, 14, 8, 18, 15, 6, 9, 4, 17, 0, 19, 7],
        [9, 17, 8, 14, 11, 0, 7, 6, 1, 19, 10, 12, 5, 15, 3, 4, 16, 18, 2, 13],
        [11, 17, 4, 18, 12, 19, 9, 16, 6, 8, 1, 0, 15, 5, 7, 3, 13, 14, 2, 10],
        [11, 6, 10, 5, 7, 2, 19, 9, 0, 8, 14, 3, 16, 13, 15, 12, 18, 1, 17, 4],
        [4, 5, 14, 12, 11, 8, 15, 7, 2, 16, 6, 19, 17, 18, 9, 0, 10, 1, 13, 3],
        [17, 6, 5, 8, 15, 19, 12, 14, 7, 11, 3, 18, 2, 10, 4, 16, 13, 9, 1, 0],
        [9, 6, 15, 5, 14, 10, 19, 2, 3, 16, 0, 17, 12, 13, 7, 18, 1, 8, 4, 11],
        [5, 2, 12, 8, 13, 11, 1, 3, 0, 15, 18, 16, 7, 9, 6, 17, 14, 19, 10, 4],
        [16, 14, 12, 7, 2, 5, 3, 13, 4, 10, 11, 17, 15, 6, 9, 0, 19, 8, 18, 1],
        [1, 14, 19, 12, 7, 8, 17, 10, 0, 3, 6, 2, 11, 13, 5, 15, 16, 18, 4, 9],
        [10, 9, 3, 12, 2, 8, 19, 0, 15, 17, 5, 16, 4, 6, 11, 13, 1, 14, 7, 18],
        [15, 3, 4, 10, 1, 16, 18, 5, 14, 8, 13, 6, 11, 17, 19, 12, 7, 0, 9, 2],
        [12, 6, 8, 11, 17, 1, 4, 15, 13, 5, 2, 14, 18, 16, 7, 9, 10, 0, 19, 3],
    ],
    'durations': [
        # Job 0
        [Interval(73, 95), Interval(26, 26), Interval(14, 18), Interval(12, 16), Interval(41, 45),
         Interval(27, 29), Interval(75, 97), Interval(81, 103), Interval(31, 33), Interval(69, 77),
         Interval(55, 67), Interval(12, 14), Interval(41, 55), Interval(65, 75), Interval(65, 71),
         Interval(48, 64), Interval(75, 93), Interval(23, 23), Interval(80, 108), Interval(27, 33)],
        # Job 1
        [Interval(67, 87), Interval(28, 36), Interval(54, 56), Interval(20, 24), Interval(71, 95),
         Interval(17, 21), Interval(42, 56), Interval(76, 84), Interval(27, 27), Interval(62, 76),
         Interval(44, 48), Interval(77, 95), Interval(44, 58), Interval(1, 1), Interval(84, 92),
         Interval(77, 77), Interval(96, 100), Interval(46, 50), Interval(22, 26), Interval(59, 67)],
        # Job 2
        [Interval(33, 39), Interval(64, 72), Interval(36, 48), Interval(44, 46), Interval(29, 39),
         Interval(67, 79), Interval(12, 16), Interval(76, 88), Interval(13, 17), Interval(31, 39),
         Interval(91, 93), Interval(10, 10), Interval(40, 46), Interval(18, 18), Interval(65, 81),
         Interval(67, 71), Interval(55, 55), Interval(58, 68), Interval(80, 98), Interval(96, 100)],
        # Job 3
        [Interval(36, 48), Interval(23, 23), Interval(28, 30), Interval(7, 9), Interval(80, 106),
         Interval(17, 21), Interval(61, 67), Interval(40, 54), Interval(17, 21), Interval(4, 4),
         Interval(77, 91), Interval(68, 76), Interval(2, 2), Interval(77, 101), Interval(72, 82),
         Interval(11, 13), Interval(88, 96), Interval(63, 71), Interval(34, 42), Interval(83, 91)],
        # Job 4
        [Interval(53, 61), Interval(59, 75), Interval(86, 112), Interval(9, 9), Interval(80, 98),
         Interval(50, 66), Interval(14, 18), Interval(34, 36), Interval(29, 31), Interval(57, 59),
         Interval(27, 29), Interval(67, 73), Interval(73, 91), Interval(29, 31), Interval(74, 94),
         Interval(5, 5), Interval(12, 14), Interval(3, 3), Interval(91, 91), Interval(7, 9)],
        # Job 5
        [Interval(32, 36), Interval(32, 36), Interval(29, 35), Interval(17, 17), Interval(49, 49),
         Interval(13, 13), Interval(4, 4), Interval(7, 7), Interval(33, 43), Interval(60, 64),
         Interval(40, 52), Interval(26, 32), Interval(85, 89), Interval(20, 26), Interval(39, 49),
         Interval(81, 105), Interval(15, 15), Interval(9, 9), Interval(53, 59), Interval(39, 45)],
        # Job 6
        [Interval(4, 4), Interval(68, 74), Interval(59, 67), Interval(17, 21), Interval(17, 19),
         Interval(46, 50), Interval(40, 54), Interval(48, 52), Interval(72, 92), Interval(87, 101),
         Interval(21, 23), Interval(6, 8), Interval(63, 75), Interval(61, 75), Interval(32, 36),
         Interval(68, 82), Interval(12, 14), Interval(53, 57), Interval(11, 11), Interval(51, 69)],
        # Job 7
        [Interval(38, 50), Interval(20, 20), Interval(83, 89), Interval(2, 2), Interval(83, 97),
         Interval(31, 33), Interval(47, 61), Interval(34, 46), Interval(37, 43), Interval(3, 3),
         Interval(17, 23), Interval(58, 78), Interval(74, 94), Interval(40, 40), Interval(78, 104),
         Interval(50, 56), Interval(68, 86), Interval(83, 83), Interval(84, 110), Interval(56, 70)],
        # Job 8
        [Interval(44, 46), Interval(66, 78), Interval(7, 9), Interval(53, 69), Interval(51, 51),
         Interval(82, 110), Interval(90, 98), Interval(88, 108), Interval(77, 89), Interval(43, 53),
         Interval(6, 6), Interval(20, 24), Interval(43, 57), Interval(23, 25), Interval(34, 38),
         Interval(20, 22), Interval(16, 18), Interval(44, 52), Interval(51, 57), Interval(21, 21)],
        # Job 9
        [Interval(21, 27), Interval(19, 21), Interval(87, 97), Interval(46, 48), Interval(98, 100),
         Interval(82, 88), Interval(20, 20), Interval(85, 95), Interval(1, 1), Interval(19, 21),
         Interval(33, 39), Interval(55, 61), Interval(2, 2), Interval(77, 95), Interval(42, 42),
         Interval(33, 43), Interval(63, 75), Interval(79, 79), Interval(37, 49), Interval(51, 59)],
        # Job 10
        [Interval(54, 70), Interval(18, 24), Interval(82, 108), Interval(48, 58), Interval(70, 80),
         Interval(79, 101), Interval(87, 101), Interval(40, 46), Interval(66, 78), Interval(35, 41),
         Interval(51, 69), Interval(27, 33), Interval(6, 6), Interval(71, 79), Interval(30, 32),
         Interval(79, 95), Interval(60, 66), Interval(23, 25), Interval(15, 17), Interval(43, 49)],
        # Job 11
        [Interval(5, 5), Interval(44, 52), Interval(84, 92), Interval(78, 78), Interval(72, 96),
         Interval(75, 95), Interval(1, 1), Interval(69, 89), Interval(86, 104), Interval(37, 47),
         Interval(18, 24), Interval(68, 70), Interval(76, 102), Interval(59, 77), Interval(49, 63),
         Interval(30, 30), Interval(88, 104), Interval(89, 107), Interval(67, 83), Interval(22, 26)],
        # Job 12
        [Interval(51, 65), Interval(49, 49), Interval(47, 59), Interval(78, 92), Interval(18, 22),
         Interval(14, 16), Interval(44, 44), Interval(93, 101), Interval(22, 26), Interval(11, 13),
         Interval(85, 111), Interval(50, 56), Interval(66, 68), Interval(9, 11), Interval(80, 102),
         Interval(40, 54), Interval(73, 83), Interval(5, 5), Interval(24, 32), Interval(5, 5)],
        # Job 13
        [Interval(55, 55), Interval(26, 34), Interval(67, 69), Interval(29, 39), Interval(3, 3),
         Interval(57, 59), Interval(16, 20), Interval(18, 22), Interval(31, 35), Interval(55, 69),
         Interval(67, 73), Interval(87, 87), Interval(47, 63), Interval(88, 94), Interval(2, 2),
         Interval(32, 34), Interval(20, 24), Interval(17, 23), Interval(24, 28), Interval(99, 99)],
        # Job 14
        [Interval(60, 68), Interval(78, 98), Interval(91, 97), Interval(34, 34), Interval(4, 4),
         Interval(75, 81), Interval(9, 11), Interval(61, 73), Interval(67, 87), Interval(47, 59),
         Interval(57, 77), Interval(91, 91), Interval(24, 24), Interval(29, 31), Interval(73, 79),
         Interval(68, 72), Interval(51, 61), Interval(79, 99), Interval(47, 51), Interval(69, 79)],
        # Job 15
        [Interval(91, 99), Interval(8, 10), Interval(25, 33), Interval(41, 49), Interval(64, 64),
         Interval(69, 77), Interval(62, 62), Interval(10, 12), Interval(30, 32), Interval(77, 77),
         Interval(53, 69), Interval(19, 21), Interval(48, 60), Interval(34, 40), Interval(15, 19),
         Interval(29, 33), Interval(28, 36), Interval(86, 110), Interval(18, 22), Interval(81, 107)],
        # Job 16
        [Interval(14, 14), Interval(85, 95), Interval(67, 79), Interval(81, 87), Interval(73, 77),
         Interval(78, 100), Interval(39, 43), Interval(57, 61), Interval(50, 66), Interval(38, 50),
         Interval(20, 22), Interval(59, 63), Interval(84, 98), Interval(23, 27), Interval(47, 49),
         Interval(12, 12), Interval(37, 37), Interval(72, 88), Interval(76, 78), Interval(45, 57)],
        # Job 17
        [Interval(47, 47), Interval(82, 102), Interval(11, 11), Interval(63, 83), Interval(4, 4),
         Interval(8, 10), Interval(89, 101), Interval(19, 25), Interval(32, 32), Interval(83, 95),
         Interval(55, 73), Interval(19, 19), Interval(60, 78), Interval(79, 87), Interval(89, 93),
         Interval(34, 34), Interval(75, 85), Interval(89, 99), Interval(87, 99), Interval(70, 94)],
        # Job 18
        [Interval(87, 97), Interval(75, 83), Interval(70, 78), Interval(2, 2), Interval(91, 103),
         Interval(58, 78), Interval(96, 100), Interval(77, 79), Interval(19, 25), Interval(39, 43),
         Interval(55, 61), Interval(85, 113), Interval(45, 59), Interval(59, 75), Interval(47, 49),
         Interval(29, 37), Interval(41, 55), Interval(54, 62), Interval(78, 84), Interval(39, 39)],
        # Job 19
        [Interval(20, 20), Interval(91, 101), Interval(55, 73), Interval(83, 107), Interval(6, 6),
         Interval(23, 29), Interval(36, 42), Interval(23, 29), Interval(81, 103), Interval(12, 12),
         Interval(59, 71), Interval(14, 14), Interval(61, 81), Interval(30, 32), Interval(93, 101),
         Interval(21, 27), Interval(74, 96), Interval(88, 90), Interval(10, 12), Interval(5, 5)],
        # Job 20
        [Interval(77, 77), Interval(70, 94), Interval(36, 36), Interval(51, 53), Interval(81, 107),
         Interval(75, 99), Interval(7, 7), Interval(56, 74), Interval(37, 43), Interval(53, 69),
         Interval(69, 89), Interval(2, 2), Interval(7, 7), Interval(68, 74), Interval(47, 51),
         Interval(16, 20), Interval(57, 65), Interval(59, 79), Interval(49, 51), Interval(84, 86)],
        # Job 21
        [Interval(58, 68), Interval(46, 54), Interval(76, 100), Interval(88, 92), Interval(35, 35),
         Interval(17, 23), Interval(68, 70), Interval(85, 91), Interval(38, 48), Interval(94, 94),
         Interval(44, 58), Interval(94, 94), Interval(12, 12), Interval(83, 97), Interval(32, 40),
         Interval(3, 3), Interval(94, 104), Interval(33, 41), Interval(7, 9), Interval(69, 69)],
        # Job 22
        [Interval(42, 44), Interval(62, 70), Interval(92, 92), Interval(58, 64), Interval(10, 12),
         Interval(51, 55), Interval(49, 59), Interval(48, 60), Interval(37, 47), Interval(75, 99),
         Interval(81, 91), Interval(34, 34), Interval(6, 8), Interval(60, 60), Interval(52, 52),
         Interval(96, 96), Interval(22, 28), Interval(48, 62), Interval(46, 52), Interval(49, 63)],
        # Job 23
        [Interval(11, 11), Interval(70, 72), Interval(60, 60), Interval(66, 80), Interval(91, 91),
         Interval(87, 111), Interval(21, 23), Interval(69, 79), Interval(80, 80), Interval(71, 87),
         Interval(83, 111), Interval(85, 101), Interval(85, 85), Interval(64, 80), Interval(82, 110),
         Interval(52, 52), Interval(65, 75), Interval(10, 12), Interval(93, 97), Interval(84, 86)],
        # Job 24
        [Interval(71, 95), Interval(34, 44), Interval(45, 57), Interval(42, 56), Interval(27, 35),
         Interval(16, 20), Interval(94, 94), Interval(84, 92), Interval(43, 49), Interval(86, 110),
         Interval(57, 75), Interval(7, 7), Interval(17, 23), Interval(51, 55), Interval(9, 9),
         Interval(6, 8), Interval(12, 16), Interval(77, 93), Interval(28, 36), Interval(85, 91)],
        # Job 25
        [Interval(97, 99), Interval(78, 104), Interval(71, 85), Interval(38, 48), Interval(52, 58),
         Interval(44, 46), Interval(53, 65), Interval(76, 78), Interval(31, 31), Interval(88, 94),
         Interval(51, 69), Interval(56, 66), Interval(57, 67), Interval(52, 66), Interval(77, 101),
         Interval(24, 26), Interval(16, 20), Interval(27, 31), Interval(48, 50), Interval(47, 59)],
        # Job 26
        [Interval(23, 29), Interval(45, 55), Interval(6, 8), Interval(71, 85), Interval(75, 75),
         Interval(3, 3), Interval(24, 32), Interval(19, 21), Interval(56, 60), Interval(84, 106),
         Interval(36, 40), Interval(55, 61), Interval(64, 76), Interval(64, 86), Interval(6, 6),
         Interval(26, 26), Interval(25, 27), Interval(48, 60), Interval(91, 99), Interval(12, 12)],
        # Job 27
        [Interval(81, 81), Interval(66, 76), Interval(22, 22), Interval(49, 63), Interval(17, 17),
         Interval(12, 16), Interval(64, 66), Interval(82, 98), Interval(25, 33), Interval(42, 52),
         Interval(8, 8), Interval(34, 44), Interval(8, 10), Interval(56, 60), Interval(94, 96),
         Interval(22, 28), Interval(1, 1), Interval(58, 72), Interval(42, 46), Interval(59, 73)],
        # Job 28
        [Interval(55, 69), Interval(79, 79), Interval(65, 75), Interval(41, 45), Interval(81, 109),
         Interval(42, 42), Interval(6, 6), Interval(78, 98), Interval(5, 5), Interval(11, 13),
         Interval(49, 59), Interval(17, 19), Interval(74, 92), Interval(26, 28), Interval(36, 40),
         Interval(49, 49), Interval(91, 97), Interval(92, 98), Interval(77, 79), Interval(53, 61)],
        # Job 29
        [Interval(17, 19), Interval(31, 41), Interval(61, 79), Interval(9, 11), Interval(25, 25),
         Interval(23, 27), Interval(69, 75), Interval(67, 71), Interval(13, 17), Interval(16, 18),
         Interval(29, 33), Interval(59, 61), Interval(66, 72), Interval(35, 43), Interval(50, 58),
         Interval(50, 62), Interval(80, 90), Interval(41, 53), Interval(40, 40), Interval(10, 10)],
        # Job 30
        [Interval(6, 8), Interval(14, 14), Interval(10, 12), Interval(30, 36), Interval(48, 50),
         Interval(70, 94), Interval(66, 86), Interval(10, 12), Interval(47, 57), Interval(20, 20),
         Interval(30, 40), Interval(64, 82), Interval(70, 92), Interval(40, 44), Interval(4, 4),
         Interval(23, 31), Interval(13, 15), Interval(70, 76), Interval(10, 10), Interval(25, 25)],
        # Job 31
        [Interval(49, 59), Interval(75, 87), Interval(50, 54), Interval(23, 27), Interval(72, 84),
         Interval(23, 23), Interval(34, 42), Interval(58, 60), Interval(22, 22), Interval(43, 47),
         Interval(65, 67), Interval(85, 103), Interval(53, 61), Interval(82, 82), Interval(47, 55),
         Interval(49, 59), Interval(25, 25), Interval(90, 104), Interval(49, 61), Interval(35, 41)],
        # Job 32
        [Interval(50, 52), Interval(21, 21), Interval(35, 37), Interval(91, 99), Interval(59, 77),
         Interval(89, 91), Interval(70, 82), Interval(74, 94), Interval(33, 41), Interval(37, 39),
         Interval(26, 34), Interval(21, 23), Interval(25, 31), Interval(80, 100), Interval(6, 6),
         Interval(91, 91), Interval(73, 73), Interval(86, 100), Interval(48, 62), Interval(38, 38)],
        # Job 33
        [Interval(72, 84), Interval(15, 19), Interval(39, 43), Interval(59, 79), Interval(94, 94),
         Interval(71, 95), Interval(21, 27), Interval(50, 60), Interval(57, 67), Interval(25, 29),
         Interval(21, 27), Interval(70, 70), Interval(46, 54), Interval(20, 22), Interval(46, 56),
         Interval(17, 21), Interval(20, 20), Interval(54, 64), Interval(39, 51), Interval(21, 23)],
        # Job 34
        [Interval(2, 2), Interval(73, 97), Interval(50, 66), Interval(47, 47), Interval(61, 71),
         Interval(76, 86), Interval(39, 49), Interval(37, 45), Interval(17, 19), Interval(85, 85),
         Interval(51, 61), Interval(2, 2), Interval(69, 93), Interval(1, 1), Interval(33, 39),
         Interval(51, 51), Interval(22, 28), Interval(10, 12), Interval(19, 23), Interval(1, 1)],
        # Job 35
        [Interval(79, 95), Interval(61, 69), Interval(10, 12), Interval(77, 93), Interval(35, 39),
         Interval(24, 28), Interval(85, 93), Interval(24, 30), Interval(10, 10), Interval(12, 14),
         Interval(60, 64), Interval(30, 30), Interval(23, 25), Interval(76, 82), Interval(93, 103),
         Interval(61, 61), Interval(58, 72), Interval(27, 31), Interval(25, 29), Interval(13, 15)],
        # Job 36
        [Interval(13, 15), Interval(47, 47), Interval(11, 11), Interval(28, 30), Interval(17, 19),
         Interval(38, 40), Interval(18, 24), Interval(70, 90), Interval(39, 43), Interval(58, 66),
         Interval(71, 73), Interval(44, 54), Interval(47, 57), Interval(73, 93), Interval(36, 36),
         Interval(29, 33), Interval(46, 56), Interval(56, 58), Interval(30, 36), Interval(46, 48)],
        # Job 37
        [Interval(8, 10), Interval(82, 110), Interval(42, 42), Interval(37, 41), Interval(6, 6),
         Interval(60, 74), Interval(59, 59), Interval(81, 101), Interval(78, 84), Interval(80, 100),
         Interval(6, 8), Interval(48, 50), Interval(88, 104), Interval(50, 52), Interval(35, 41),
         Interval(48, 64), Interval(41, 53), Interval(84, 106), Interval(21, 25), Interval(16, 20)],
        # Job 38
        [Interval(67, 89), Interval(94, 98), Interval(78, 80), Interval(31, 39), Interval(88, 108),
         Interval(9, 11), Interval(1, 1), Interval(80, 84), Interval(55, 57), Interval(27, 35),
         Interval(79, 97), Interval(45, 59), Interval(96, 96), Interval(73, 77), Interval(47, 61),
         Interval(11, 13), Interval(62, 64), Interval(41, 47), Interval(42, 44), Interval(17, 21)],
        # Job 39
        [Interval(33, 37), Interval(69, 77), Interval(39, 41), Interval(51, 53), Interval(88, 96),
         Interval(72, 82), Interval(49, 65), Interval(61, 71), Interval(31, 41), Interval(7, 7),
         Interval(6, 6), Interval(66, 72), Interval(80, 88), Interval(51, 57), Interval(51, 55),
         Interval(83, 111), Interval(38, 38), Interval(89, 97), Interval(28, 28), Interval(64, 68)],
        # Job 40
        [Interval(96, 102), Interval(86, 90), Interval(15, 19), Interval(29, 37), Interval(3, 3),
         Interval(51, 65), Interval(21, 23), Interval(71, 79), Interval(57, 57), Interval(5, 5),
         Interval(21, 23), Interval(10, 12), Interval(70, 82), Interval(88, 98), Interval(10, 12),
         Interval(56, 70), Interval(85, 93), Interval(87, 105), Interval(14, 16), Interval(51, 69)],
        # Job 41
        [Interval(47, 49), Interval(87, 105), Interval(12, 14), Interval(43, 47), Interval(77, 77),
         Interval(8, 10), Interval(54, 66), Interval(7, 9), Interval(85, 89), Interval(29, 29),
         Interval(53, 59), Interval(37, 41), Interval(77, 87), Interval(34, 34), Interval(20, 20),
         Interval(54, 62), Interval(39, 43), Interval(41, 55), Interval(53, 59), Interval(39, 43)],
        # Job 42
        [Interval(13, 17), Interval(70, 84), Interval(40, 54), Interval(60, 60), Interval(49, 53),
         Interval(49, 53), Interval(52, 60), Interval(26, 34), Interval(48, 52), Interval(37, 41),
         Interval(23, 27), Interval(85, 95), Interval(14, 14), Interval(57, 77), Interval(12, 14),
         Interval(36, 48), Interval(28, 28), Interval(31, 41), Interval(7, 7), Interval(2, 2)],
        # Job 43
        [Interval(11, 13), Interval(59, 77), Interval(78, 104), Interval(11, 13), Interval(71, 75),
         Interval(67, 81), Interval(67, 85), Interval(56, 62), Interval(59, 61), Interval(18, 22),
         Interval(80, 86), Interval(83, 93), Interval(24, 26), Interval(77, 77), Interval(62, 68),
         Interval(39, 49), Interval(29, 31), Interval(78, 90), Interval(26, 30), Interval(61, 65)],
        # Job 44
        [Interval(32, 32), Interval(10, 12), Interval(70, 82), Interval(24, 30), Interval(11, 13),
         Interval(62, 72), Interval(31, 35), Interval(16, 18), Interval(11, 13), Interval(53, 63),
         Interval(51, 61), Interval(27, 35), Interval(84, 108), Interval(79, 99), Interval(28, 28),
         Interval(31, 35), Interval(72, 78), Interval(87, 111), Interval(35, 45), Interval(69, 79)],
        # Job 45
        [Interval(78, 102), Interval(1, 1), Interval(58, 78), Interval(4, 4), Interval(89, 101),
         Interval(9, 9), Interval(58, 64), Interval(45, 45), Interval(55, 71), Interval(32, 38),
         Interval(77, 85), Interval(74, 80), Interval(9, 9), Interval(52, 54), Interval(42, 46),
         Interval(53, 65), Interval(86, 106), Interval(76, 76), Interval(91, 97), Interval(17, 23)],
        # Job 46
        [Interval(38, 48), Interval(76, 82), Interval(51, 69), Interval(89, 107), Interval(3, 3),
         Interval(4, 4), Interval(43, 53), Interval(64, 80), Interval(39, 43), Interval(77, 103),
         Interval(90, 98), Interval(10, 12), Interval(29, 31), Interval(9, 11), Interval(40, 42),
         Interval(79, 79), Interval(66, 66), Interval(11, 11), Interval(78, 96), Interval(64, 72)],
        # Job 47
        [Interval(89, 93), Interval(65, 65), Interval(70, 90), Interval(46, 54), Interval(64, 68),
         Interval(32, 38), Interval(68, 72), Interval(94, 102), Interval(71, 89), Interval(45, 49),
         Interval(9, 9), Interval(6, 8), Interval(58, 76), Interval(20, 24), Interval(95, 95),
         Interval(11, 11), Interval(52, 60), Interval(23, 27), Interval(57, 71), Interval(49, 65)],
        # Job 48
        [Interval(22, 24), Interval(75, 75), Interval(11, 13), Interval(47, 55), Interval(41, 49),
         Interval(21, 25), Interval(46, 58), Interval(66, 88), Interval(66, 86), Interval(41, 55),
         Interval(52, 52), Interval(46, 60), Interval(50, 56), Interval(16, 20), Interval(3, 3),
         Interval(18, 18), Interval(48, 64), Interval(95, 101), Interval(69, 73), Interval(22, 28)],
        # Job 49
        [Interval(63, 65), Interval(20, 20), Interval(88, 90), Interval(26, 28), Interval(5, 5),
         Interval(43, 51), Interval(89, 95), Interval(23, 23), Interval(70, 86), Interval(62, 66),
         Interval(66, 88), Interval(12, 12), Interval(48, 50), Interval(40, 40), Interval(3, 3),
         Interval(53, 67), Interval(50, 58), Interval(37, 37), Interval(15, 15), Interval(16, 16)],
    ],
    'name': 'INT__TAI50_20_09.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai50_20_09_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI50_20_09.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI50_20_09.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI50_20_09_F_15_01_INTERVAL_DATA
