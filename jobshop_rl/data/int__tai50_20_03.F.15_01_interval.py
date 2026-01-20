"""
Problema INT__TAI50_20_03.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI50_20_03_F_15_01_INTERVAL_DATA = {
    'num_jobs': 50,
    'num_machines': 20,
    'problem_id': 'int__tai50_20_03.F.15_01_interval',
    'sequences': [
        [0, 1, 11, 17, 10, 7, 5, 13, 3, 4, 19, 9, 12, 14, 15, 2, 16, 18, 8, 6],
        [3, 16, 5, 7, 10, 11, 14, 18, 13, 1, 8, 9, 19, 12, 0, 2, 15, 4, 17, 6],
        [6, 11, 7, 2, 4, 12, 14, 5, 0, 13, 10, 18, 19, 1, 8, 15, 9, 3, 16, 17],
        [13, 6, 19, 16, 2, 3, 10, 9, 7, 1, 0, 14, 12, 5, 18, 4, 8, 17, 15, 11],
        [8, 0, 13, 7, 10, 4, 16, 6, 1, 17, 15, 3, 2, 9, 19, 18, 5, 11, 14, 12],
        [7, 12, 0, 17, 3, 15, 4, 13, 14, 6, 16, 19, 10, 1, 18, 9, 11, 5, 8, 2],
        [15, 7, 1, 0, 18, 5, 19, 10, 12, 6, 17, 14, 3, 11, 13, 4, 16, 2, 9, 8],
        [19, 2, 16, 14, 5, 6, 15, 9, 17, 11, 10, 3, 12, 4, 0, 1, 7, 13, 8, 18],
        [13, 15, 12, 19, 4, 0, 3, 18, 10, 1, 17, 14, 5, 7, 6, 11, 8, 2, 16, 9],
        [5, 0, 6, 10, 1, 3, 2, 11, 18, 7, 4, 17, 9, 15, 16, 8, 13, 12, 19, 14],
        [4, 11, 9, 3, 1, 2, 5, 16, 10, 8, 7, 13, 18, 15, 17, 14, 6, 12, 0, 19],
        [11, 13, 1, 10, 0, 12, 3, 15, 5, 9, 19, 17, 4, 8, 14, 16, 6, 7, 18, 2],
        [7, 19, 14, 3, 16, 4, 11, 17, 5, 15, 10, 9, 0, 18, 6, 12, 1, 2, 13, 8],
        [9, 8, 10, 2, 7, 12, 5, 4, 17, 14, 3, 16, 18, 1, 15, 6, 19, 13, 11, 0],
        [14, 0, 1, 8, 2, 6, 3, 12, 9, 16, 4, 19, 5, 15, 13, 18, 11, 10, 7, 17],
        [16, 9, 19, 12, 6, 0, 17, 2, 13, 4, 7, 18, 5, 11, 8, 1, 3, 14, 15, 10],
        [15, 10, 11, 18, 14, 17, 5, 19, 12, 6, 16, 1, 7, 8, 3, 2, 4, 13, 9, 0],
        [6, 9, 18, 16, 12, 1, 2, 7, 19, 11, 4, 0, 3, 5, 10, 14, 17, 8, 15, 13],
        [18, 7, 12, 17, 19, 11, 5, 15, 3, 8, 0, 6, 16, 13, 1, 2, 9, 4, 10, 14],
        [13, 15, 12, 14, 5, 18, 11, 6, 3, 8, 2, 17, 4, 16, 0, 7, 10, 1, 9, 19],
        [17, 4, 2, 7, 1, 5, 15, 18, 0, 11, 10, 6, 19, 8, 14, 13, 9, 3, 12, 16],
        [8, 13, 1, 9, 2, 10, 14, 0, 3, 12, 16, 18, 5, 17, 7, 4, 19, 11, 6, 15],
        [16, 5, 11, 12, 17, 18, 8, 19, 3, 10, 13, 1, 4, 2, 9, 15, 6, 7, 0, 14],
        [13, 1, 11, 0, 16, 3, 7, 5, 14, 17, 19, 18, 10, 4, 6, 15, 9, 2, 12, 8],
        [19, 2, 14, 7, 3, 17, 6, 10, 15, 9, 0, 16, 1, 5, 18, 4, 13, 11, 12, 8],
        [11, 9, 5, 18, 16, 1, 2, 17, 8, 12, 10, 19, 15, 14, 3, 7, 0, 6, 13, 4],
        [13, 15, 11, 14, 12, 18, 1, 4, 9, 10, 16, 17, 3, 19, 7, 6, 0, 2, 5, 8],
        [7, 17, 16, 6, 14, 19, 18, 1, 2, 8, 5, 4, 10, 11, 9, 3, 15, 12, 0, 13],
        [18, 15, 16, 9, 6, 8, 17, 19, 1, 0, 11, 7, 14, 3, 12, 10, 4, 13, 5, 2],
        [9, 12, 4, 8, 6, 3, 11, 14, 7, 15, 1, 2, 10, 13, 17, 19, 16, 5, 18, 0],
        [15, 1, 17, 11, 7, 3, 18, 19, 4, 10, 13, 2, 5, 8, 6, 0, 12, 16, 14, 9],
        [14, 19, 17, 9, 18, 11, 1, 4, 16, 8, 5, 7, 0, 10, 2, 3, 13, 6, 15, 12],
        [9, 17, 12, 3, 11, 2, 15, 10, 0, 16, 14, 1, 5, 8, 19, 7, 4, 6, 13, 18],
        [5, 16, 2, 0, 8, 12, 11, 19, 15, 4, 6, 14, 7, 18, 17, 9, 1, 10, 13, 3],
        [14, 15, 3, 7, 11, 0, 12, 6, 1, 8, 13, 19, 2, 4, 5, 18, 17, 9, 10, 16],
        [13, 17, 18, 14, 10, 15, 5, 16, 1, 3, 9, 7, 11, 12, 0, 2, 4, 6, 19, 8],
        [17, 2, 19, 15, 18, 5, 9, 16, 13, 0, 1, 7, 3, 14, 12, 10, 6, 4, 8, 11],
        [11, 4, 5, 12, 3, 2, 6, 16, 0, 10, 1, 15, 19, 18, 8, 13, 7, 17, 9, 14],
        [19, 6, 4, 17, 2, 18, 3, 13, 12, 15, 14, 7, 10, 8, 9, 5, 11, 16, 1, 0],
        [8, 16, 15, 12, 18, 17, 4, 0, 11, 19, 14, 6, 5, 1, 13, 3, 9, 10, 7, 2],
        [10, 17, 13, 11, 6, 2, 9, 12, 15, 0, 7, 5, 14, 16, 18, 19, 1, 3, 8, 4],
        [0, 3, 14, 1, 9, 18, 5, 11, 8, 7, 6, 15, 16, 12, 17, 10, 19, 13, 2, 4],
        [8, 14, 16, 4, 11, 18, 12, 19, 2, 5, 9, 15, 7, 0, 6, 13, 17, 1, 10, 3],
        [6, 15, 7, 16, 14, 9, 3, 18, 11, 17, 0, 2, 1, 19, 10, 13, 5, 4, 12, 8],
        [9, 10, 11, 6, 4, 3, 12, 13, 5, 0, 18, 19, 14, 17, 2, 7, 16, 15, 8, 1],
        [5, 7, 17, 18, 8, 1, 12, 16, 19, 4, 10, 3, 0, 9, 15, 14, 2, 11, 13, 6],
        [13, 15, 10, 18, 14, 9, 7, 19, 5, 3, 16, 4, 17, 12, 8, 1, 2, 0, 11, 6],
        [7, 16, 5, 2, 9, 8, 15, 3, 19, 18, 13, 12, 4, 14, 17, 11, 0, 6, 1, 10],
        [12, 9, 6, 16, 3, 8, 15, 0, 11, 5, 10, 18, 17, 19, 13, 7, 14, 4, 2, 1],
        [15, 8, 5, 9, 13, 1, 6, 14, 18, 12, 3, 19, 16, 2, 17, 7, 0, 10, 11, 4],
    ],
    'durations': [
        # Job 0
        [Interval(30, 40), Interval(73, 73), Interval(49, 63), Interval(25, 31), Interval(77, 85),
         Interval(79, 85), Interval(5, 5), Interval(42, 54), Interval(31, 41), Interval(36, 38),
         Interval(9, 9), Interval(7, 9), Interval(8, 10), Interval(17, 23), Interval(72, 84),
         Interval(73, 81), Interval(27, 35), Interval(39, 49), Interval(9, 9), Interval(34, 46)],
        # Job 1
        [Interval(37, 45), Interval(23, 29), Interval(23, 31), Interval(31, 31), Interval(55, 69),
         Interval(17, 23), Interval(15, 19), Interval(47, 63), Interval(54, 60), Interval(21, 21),
         Interval(54, 68), Interval(61, 65), Interval(15, 19), Interval(12, 16), Interval(57, 61),
         Interval(90, 92), Interval(53, 55), Interval(61, 67), Interval(19, 23), Interval(44, 50)],
        # Job 2
        [Interval(4, 4), Interval(85, 99), Interval(71, 79), Interval(18, 24), Interval(20, 22),
         Interval(84, 112), Interval(30, 34), Interval(36, 46), Interval(27, 31), Interval(37, 47),
         Interval(64, 78), Interval(89, 91), Interval(66, 72), Interval(81, 93), Interval(70, 72),
         Interval(16, 20), Interval(40, 42), Interval(77, 79), Interval(55, 65), Interval(77, 93)],
        # Job 3
        [Interval(71, 73), Interval(18, 24), Interval(8, 8), Interval(52, 58), Interval(76, 96),
         Interval(15, 19), Interval(87, 109), Interval(67, 75), Interval(16, 20), Interval(74, 98),
         Interval(77, 91), Interval(82, 94), Interval(84, 110), Interval(70, 80), Interval(61, 79),
         Interval(64, 70), Interval(34, 38), Interval(10, 12), Interval(93, 101), Interval(51, 59)],
        # Job 4
        [Interval(78, 98), Interval(13, 17), Interval(27, 31), Interval(46, 56), Interval(70, 94),
         Interval(58, 74), Interval(26, 26), Interval(67, 73), Interval(7, 7), Interval(83, 91),
         Interval(78, 84), Interval(67, 85), Interval(42, 46), Interval(24, 30), Interval(76, 100),
         Interval(34, 34), Interval(65, 75), Interval(58, 66), Interval(42, 46), Interval(60, 74)],
        # Job 5
        [Interval(26, 26), Interval(24, 24), Interval(85, 89), Interval(45, 51), Interval(47, 63),
         Interval(66, 70), Interval(46, 62), Interval(73, 93), Interval(17, 17), Interval(43, 57),
         Interval(76, 98), Interval(16, 20), Interval(80, 86), Interval(31, 33), Interval(67, 75),
         Interval(66, 78), Interval(90, 100), Interval(37, 41), Interval(33, 41), Interval(20, 22)],
        # Job 6
        [Interval(76, 84), Interval(27, 35), Interval(19, 21), Interval(45, 57), Interval(30, 34),
         Interval(20, 22), Interval(11, 13), Interval(73, 85), Interval(1, 1), Interval(85, 101),
         Interval(75, 85), Interval(54, 66), Interval(16, 18), Interval(75, 81), Interval(84, 90),
         Interval(55, 73), Interval(40, 54), Interval(65, 67), Interval(62, 66), Interval(43, 51)],
        # Job 7
        [Interval(57, 61), Interval(9, 11), Interval(69, 91), Interval(43, 49), Interval(54, 70),
         Interval(34, 46), Interval(60, 76), Interval(26, 26), Interval(46, 62), Interval(47, 53),
         Interval(54, 68), Interval(77, 77), Interval(34, 46), Interval(83, 105), Interval(35, 37),
         Interval(61, 73), Interval(55, 63), Interval(48, 62), Interval(15, 15), Interval(61, 81)],
        # Job 8
        [Interval(35, 37), Interval(65, 79), Interval(49, 57), Interval(83, 99), Interval(58, 72),
         Interval(84, 112), Interval(56, 64), Interval(57, 63), Interval(59, 65), Interval(48, 56),
         Interval(36, 42), Interval(13, 13), Interval(44, 44), Interval(59, 79), Interval(3, 3),
         Interval(91, 103), Interval(62, 68), Interval(16, 16), Interval(57, 57), Interval(63, 67)],
        # Job 9
        [Interval(8, 8), Interval(94, 104), Interval(32, 36), Interval(39, 47), Interval(36, 40),
         Interval(44, 54), Interval(85, 87), Interval(79, 103), Interval(13, 15), Interval(87, 87),
         Interval(39, 51), Interval(12, 12), Interval(40, 50), Interval(12, 16), Interval(50, 66),
         Interval(24, 30), Interval(63, 73), Interval(5, 5), Interval(41, 53), Interval(57, 65)],
        # Job 10
        [Interval(74, 84), Interval(47, 55), Interval(37, 45), Interval(44, 58), Interval(36, 46),
         Interval(42, 46), Interval(47, 53), Interval(16, 18), Interval(25, 27), Interval(2, 2),
         Interval(15, 17), Interval(24, 26), Interval(36, 40), Interval(16, 18), Interval(85, 93),
         Interval(82, 84), Interval(51, 67), Interval(40, 50), Interval(32, 42), Interval(21, 25)],
        # Job 11
        [Interval(87, 107), Interval(77, 103), Interval(91, 93), Interval(3, 3), Interval(2, 2),
         Interval(8, 10), Interval(61, 79), Interval(13, 17), Interval(38, 38), Interval(44, 52),
         Interval(11, 13), Interval(9, 11), Interval(8, 10), Interval(67, 85), Interval(27, 27),
         Interval(7, 9), Interval(40, 48), Interval(72, 90), Interval(7, 7), Interval(79, 81)],
        # Job 12
        [Interval(43, 47), Interval(12, 14), Interval(46, 54), Interval(26, 34), Interval(80, 90),
         Interval(79, 83), Interval(30, 34), Interval(56, 72), Interval(10, 12), Interval(65, 75),
         Interval(1, 1), Interval(80, 106), Interval(54, 54), Interval(12, 14), Interval(30, 30),
         Interval(15, 19), Interval(16, 16), Interval(3, 3), Interval(2, 2), Interval(17, 21)],
        # Job 13
        [Interval(51, 63), Interval(74, 88), Interval(17, 21), Interval(44, 48), Interval(40, 40),
         Interval(34, 44), Interval(61, 65), Interval(88, 96), Interval(53, 67), Interval(7, 9),
         Interval(6, 8), Interval(39, 39), Interval(9, 9), Interval(48, 60), Interval(66, 70),
         Interval(21, 21), Interval(64, 68), Interval(46, 58), Interval(49, 59), Interval(18, 24)],
        # Job 14
        [Interval(58, 74), Interval(57, 75), Interval(48, 48), Interval(79, 83), Interval(29, 31),
         Interval(78, 84), Interval(45, 47), Interval(86, 104), Interval(19, 25), Interval(82, 88),
         Interval(53, 61), Interval(79, 87), Interval(41, 55), Interval(80, 108), Interval(10, 12),
         Interval(61, 61), Interval(87, 97), Interval(49, 49), Interval(77, 89), Interval(88, 94)],
        # Job 15
        [Interval(28, 28), Interval(12, 16), Interval(62, 68), Interval(15, 19), Interval(89, 105),
         Interval(49, 65), Interval(31, 35), Interval(84, 108), Interval(3, 3), Interval(28, 36),
         Interval(64, 76), Interval(68, 88), Interval(29, 31), Interval(64, 72), Interval(84, 100),
         Interval(47, 49), Interval(9, 9), Interval(66, 84), Interval(30, 32), Interval(72, 78)],
        # Job 16
        [Interval(22, 28), Interval(28, 36), Interval(11, 11), Interval(22, 22), Interval(67, 77),
         Interval(80, 96), Interval(49, 51), Interval(19, 19), Interval(34, 34), Interval(78, 96),
         Interval(79, 81), Interval(11, 13), Interval(26, 26), Interval(70, 86), Interval(61, 65),
         Interval(3, 3), Interval(83, 111), Interval(25, 29), Interval(24, 26), Interval(18, 24)],
        # Job 17
        [Interval(1, 1), Interval(39, 39), Interval(19, 21), Interval(53, 71), Interval(68, 74),
         Interval(36, 46), Interval(66, 74), Interval(8, 8), Interval(11, 11), Interval(62, 70),
         Interval(71, 79), Interval(62, 72), Interval(28, 36), Interval(70, 78), Interval(8, 8),
         Interval(42, 46), Interval(88, 100), Interval(52, 70), Interval(18, 18), Interval(98, 100)],
        # Job 18
        [Interval(49, 63), Interval(45, 49), Interval(11, 11), Interval(37, 49), Interval(49, 65),
         Interval(23, 31), Interval(3, 3), Interval(53, 55), Interval(34, 46), Interval(74, 98),
         Interval(37, 43), Interval(29, 31), Interval(55, 55), Interval(48, 48), Interval(35, 39),
         Interval(12, 16), Interval(43, 55), Interval(51, 67), Interval(14, 16), Interval(86, 112)],
        # Job 19
        [Interval(63, 81), Interval(11, 11), Interval(82, 98), Interval(18, 18), Interval(69, 93),
         Interval(43, 45), Interval(76, 82), Interval(68, 86), Interval(17, 23), Interval(85, 87),
         Interval(50, 66), Interval(44, 44), Interval(28, 36), Interval(33, 33), Interval(36, 38),
         Interval(80, 104), Interval(82, 108), Interval(76, 78), Interval(84, 110), Interval(8, 8)],
        # Job 20
        [Interval(8, 10), Interval(32, 42), Interval(7, 7), Interval(37, 39), Interval(10, 10),
         Interval(4, 4), Interval(67, 83), Interval(51, 57), Interval(2, 2), Interval(13, 17),
         Interval(93, 97), Interval(4, 4), Interval(37, 37), Interval(18, 20), Interval(52, 60),
         Interval(38, 50), Interval(58, 62), Interval(90, 90), Interval(41, 51), Interval(7, 7)],
        # Job 21
        [Interval(32, 34), Interval(51, 65), Interval(88, 88), Interval(42, 56), Interval(50, 50),
         Interval(3, 3), Interval(44, 44), Interval(7, 9), Interval(74, 90), Interval(68, 76),
         Interval(88, 110), Interval(44, 56), Interval(57, 57), Interval(19, 19), Interval(12, 12),
         Interval(84, 84), Interval(65, 73), Interval(12, 16), Interval(8, 8), Interval(9, 11)],
        # Job 22
        [Interval(33, 41), Interval(8, 10), Interval(79, 103), Interval(87, 97), Interval(17, 17),
         Interval(63, 73), Interval(34, 34), Interval(80, 82), Interval(26, 26), Interval(85, 113),
         Interval(63, 81), Interval(14, 16), Interval(82, 104), Interval(24, 24), Interval(2, 2),
         Interval(72, 74), Interval(34, 34), Interval(38, 46), Interval(12, 12), Interval(87, 111)],
        # Job 23
        [Interval(73, 83), Interval(91, 105), Interval(9, 9), Interval(13, 17), Interval(83, 111),
         Interval(79, 93), Interval(88, 88), Interval(19, 25), Interval(27, 35), Interval(59, 59),
         Interval(65, 75), Interval(37, 47), Interval(41, 43), Interval(65, 65), Interval(16, 20),
         Interval(43, 57), Interval(24, 32), Interval(49, 65), Interval(75, 99), Interval(50, 64)],
        # Job 24
        [Interval(51, 51), Interval(32, 36), Interval(90, 104), Interval(73, 93), Interval(13, 17),
         Interval(66, 70), Interval(77, 97), Interval(75, 81), Interval(55, 59), Interval(32, 42),
         Interval(52, 70), Interval(46, 56), Interval(81, 105), Interval(34, 36), Interval(56, 58),
         Interval(42, 56), Interval(38, 46), Interval(11, 13), Interval(71, 81), Interval(17, 17)],
        # Job 25
        [Interval(30, 36), Interval(65, 65), Interval(61, 63), Interval(11, 11), Interval(31, 41),
         Interval(4, 4), Interval(90, 104), Interval(20, 24), Interval(66, 86), Interval(15, 19),
         Interval(78, 86), Interval(6, 6), Interval(85, 107), Interval(35, 39), Interval(26, 26),
         Interval(77, 101), Interval(36, 46), Interval(52, 62), Interval(20, 26), Interval(8, 10)],
        # Job 26
        [Interval(6, 6), Interval(89, 89), Interval(52, 70), Interval(16, 16), Interval(40, 44),
         Interval(18, 22), Interval(29, 31), Interval(54, 60), Interval(61, 71), Interval(71, 95),
         Interval(7, 7), Interval(20, 22), Interval(86, 106), Interval(7, 7), Interval(31, 31),
         Interval(99, 99), Interval(13, 15), Interval(82, 88), Interval(50, 64), Interval(15, 15)],
        # Job 27
        [Interval(39, 51), Interval(78, 80), Interval(80, 96), Interval(50, 66), Interval(2, 2),
         Interval(12, 14), Interval(21, 21), Interval(7, 9), Interval(33, 41), Interval(68, 74),
         Interval(98, 100), Interval(43, 55), Interval(51, 63), Interval(90, 100), Interval(17, 21),
         Interval(66, 80), Interval(64, 64), Interval(60, 68), Interval(52, 58), Interval(73, 97)],
        # Job 28
        [Interval(50, 52), Interval(19, 25), Interval(10, 12), Interval(74, 90), Interval(82, 98),
         Interval(36, 46), Interval(85, 91), Interval(32, 34), Interval(91, 91), Interval(96, 102),
         Interval(67, 71), Interval(6, 6), Interval(33, 33), Interval(23, 27), Interval(29, 33),
         Interval(6, 8), Interval(34, 42), Interval(42, 50), Interval(40, 42), Interval(7, 9)],
        # Job 29
        [Interval(19, 21), Interval(93, 99), Interval(75, 101), Interval(46, 52), Interval(23, 25),
         Interval(87, 91), Interval(23, 25), Interval(59, 73), Interval(64, 74), Interval(38, 46),
         Interval(87, 97), Interval(54, 70), Interval(48, 48), Interval(92, 98), Interval(25, 31),
         Interval(43, 43), Interval(63, 79), Interval(8, 10), Interval(52, 54), Interval(27, 35)],
        # Job 30
        [Interval(38, 50), Interval(90, 108), Interval(44, 54), Interval(46, 48), Interval(51, 69),
         Interval(11, 13), Interval(19, 25), Interval(47, 51), Interval(34, 46), Interval(22, 26),
         Interval(49, 53), Interval(2, 2), Interval(61, 65), Interval(99, 99), Interval(68, 82),
         Interval(48, 56), Interval(56, 62), Interval(15, 17), Interval(22, 26), Interval(55, 55)],
        # Job 31
        [Interval(59, 75), Interval(72, 74), Interval(3, 3), Interval(71, 73), Interval(8, 8),
         Interval(69, 71), Interval(67, 79), Interval(55, 63), Interval(91, 91), Interval(64, 74),
         Interval(42, 50), Interval(31, 31), Interval(6, 6), Interval(33, 37), Interval(33, 41),
         Interval(84, 102), Interval(41, 43), Interval(89, 89), Interval(33, 35), Interval(24, 26)],
        # Job 32
        [Interval(27, 35), Interval(26, 26), Interval(6, 8), Interval(58, 76), Interval(22, 28),
         Interval(42, 44), Interval(20, 26), Interval(30, 32), Interval(25, 31), Interval(51, 63),
         Interval(42, 42), Interval(16, 16), Interval(9, 11), Interval(23, 29), Interval(50, 50),
         Interval(64, 74), Interval(30, 40), Interval(17, 19), Interval(16, 20), Interval(77, 77)],
        # Job 33
        [Interval(81, 109), Interval(9, 11), Interval(6, 8), Interval(81, 95), Interval(73, 83),
         Interval(54, 70), Interval(93, 93), Interval(21, 25), Interval(87, 101), Interval(20, 24),
         Interval(76, 94), Interval(71, 75), Interval(54, 64), Interval(11, 13), Interval(54, 62),
         Interval(80, 106), Interval(40, 54), Interval(73, 73), Interval(83, 97), Interval(17, 19)],
        # Job 34
        [Interval(73, 91), Interval(84, 102), Interval(10, 10), Interval(46, 46), Interval(12, 14),
         Interval(49, 65), Interval(28, 32), Interval(20, 20), Interval(62, 80), Interval(37, 45),
         Interval(31, 39), Interval(32, 38), Interval(49, 55), Interval(82, 98), Interval(17, 19),
         Interval(74, 86), Interval(27, 31), Interval(16, 18), Interval(65, 83), Interval(90, 90)],
        # Job 35
        [Interval(34, 44), Interval(7, 7), Interval(15, 15), Interval(47, 51), Interval(33, 35),
         Interval(48, 52), Interval(48, 48), Interval(68, 86), Interval(25, 27), Interval(25, 29),
         Interval(74, 82), Interval(36, 40), Interval(76, 76), Interval(38, 42), Interval(2, 2),
         Interval(38, 42), Interval(88, 96), Interval(72, 74), Interval(74, 98), Interval(6, 6)],
        # Job 36
        [Interval(41, 53), Interval(27, 29), Interval(20, 22), Interval(78, 82), Interval(42, 50),
         Interval(57, 69), Interval(67, 85), Interval(20, 20), Interval(5, 5), Interval(53, 61),
         Interval(8, 10), Interval(70, 72), Interval(31, 37), Interval(26, 28), Interval(80, 94),
         Interval(21, 27), Interval(63, 63), Interval(6, 6), Interval(63, 69), Interval(59, 71)],
        # Job 37
        [Interval(52, 52), Interval(23, 27), Interval(65, 69), Interval(47, 59), Interval(89, 105),
         Interval(8, 8), Interval(21, 25), Interval(82, 86), Interval(68, 80), Interval(64, 86),
         Interval(16, 20), Interval(47, 59), Interval(28, 34), Interval(57, 75), Interval(42, 56),
         Interval(50, 52), Interval(29, 29), Interval(46, 58), Interval(30, 38), Interval(40, 48)],
        # Job 38
        [Interval(39, 39), Interval(17, 17), Interval(41, 55), Interval(84, 102), Interval(83, 111),
         Interval(79, 79), Interval(84, 90), Interval(35, 45), Interval(2, 2), Interval(85, 109),
         Interval(46, 48), Interval(44, 50), Interval(44, 46), Interval(57, 73), Interval(27, 31),
         Interval(91, 101), Interval(8, 8), Interval(41, 43), Interval(71, 77), Interval(17, 19)],
        # Job 39
        [Interval(32, 42), Interval(77, 89), Interval(26, 34), Interval(92, 92), Interval(83, 91),
         Interval(49, 53), Interval(86, 96), Interval(38, 40), Interval(55, 73), Interval(64, 66),
         Interval(46, 50), Interval(67, 69), Interval(41, 43), Interval(10, 10), Interval(84, 88),
         Interval(84, 108), Interval(85, 111), Interval(30, 40), Interval(48, 54), Interval(45, 51)],
        # Job 40
        [Interval(98, 98), Interval(2, 2), Interval(58, 62), Interval(21, 25), Interval(48, 56),
         Interval(79, 89), Interval(33, 43), Interval(3, 3), Interval(1, 1), Interval(41, 51),
         Interval(42, 46), Interval(75, 91), Interval(63, 73), Interval(8, 10), Interval(31, 33),
         Interval(18, 20), Interval(61, 73), Interval(10, 10), Interval(12, 12), Interval(85, 113)],
        # Job 41
        [Interval(61, 75), Interval(35, 41), Interval(88, 92), Interval(38, 38), Interval(55, 61),
         Interval(9, 9), Interval(83, 93), Interval(62, 64), Interval(9, 9), Interval(33, 37),
         Interval(4, 4), Interval(13, 13), Interval(46, 62), Interval(88, 100), Interval(84, 94),
         Interval(69, 89), Interval(67, 81), Interval(27, 35), Interval(69, 71), Interval(93, 101)],
        # Job 42
        [Interval(87, 93), Interval(17, 19), Interval(79, 103), Interval(50, 54), Interval(48, 54),
         Interval(77, 91), Interval(50, 56), Interval(8, 8), Interval(78, 102), Interval(77, 97),
         Interval(28, 36), Interval(21, 21), Interval(57, 77), Interval(13, 13), Interval(54, 66),
         Interval(65, 85), Interval(33, 43), Interval(31, 41), Interval(19, 19), Interval(62, 74)],
        # Job 43
        [Interval(41, 51), Interval(63, 71), Interval(79, 81), Interval(56, 68), Interval(42, 44),
         Interval(61, 69), Interval(9, 9), Interval(31, 31), Interval(63, 69), Interval(37, 47),
         Interval(6, 6), Interval(41, 45), Interval(43, 51), Interval(9, 9), Interval(29, 31),
         Interval(6, 6), Interval(72, 74), Interval(18, 22), Interval(1, 1), Interval(11, 13)],
        # Job 44
        [Interval(67, 85), Interval(33, 39), Interval(84, 98), Interval(67, 77), Interval(57, 65),
         Interval(7, 9), Interval(72, 84), Interval(51, 61), Interval(21, 27), Interval(17, 23),
         Interval(11, 13), Interval(50, 52), Interval(57, 65), Interval(87, 95), Interval(15, 19),
         Interval(12, 14), Interval(69, 79), Interval(55, 71), Interval(8, 10), Interval(79, 89)],
        # Job 45
        [Interval(71, 71), Interval(11, 11), Interval(72, 72), Interval(34, 46), Interval(68, 78),
         Interval(9, 9), Interval(7, 7), Interval(82, 94), Interval(19, 19), Interval(14, 16),
         Interval(41, 49), Interval(48, 60), Interval(86, 86), Interval(37, 39), Interval(8, 10),
         Interval(6, 8), Interval(71, 77), Interval(68, 92), Interval(68, 82), Interval(72, 88)],
        # Job 46
        [Interval(34, 42), Interval(87, 95), Interval(62, 82), Interval(43, 45), Interval(28, 34),
         Interval(85, 93), Interval(4, 4), Interval(71, 95), Interval(56, 58), Interval(63, 63),
         Interval(70, 70), Interval(3, 3), Interval(12, 12), Interval(40, 48), Interval(78, 88),
         Interval(7, 7), Interval(32, 32), Interval(32, 40), Interval(24, 28), Interval(47, 51)],
        # Job 47
        [Interval(55, 65), Interval(86, 90), Interval(3, 3), Interval(4, 4), Interval(54, 58),
         Interval(1, 1), Interval(85, 105), Interval(30, 32), Interval(53, 55), Interval(17, 23),
         Interval(44, 58), Interval(81, 95), Interval(82, 82), Interval(67, 69), Interval(64, 74),
         Interval(14, 16), Interval(65, 79), Interval(3, 3), Interval(51, 67), Interval(41, 45)],
        # Job 48
        [Interval(92, 92), Interval(79, 97), Interval(36, 44), Interval(42, 52), Interval(71, 89),
         Interval(20, 26), Interval(6, 8), Interval(86, 110), Interval(2, 2), Interval(77, 103),
         Interval(73, 75), Interval(20, 26), Interval(87, 99), Interval(82, 106), Interval(40, 42),
         Interval(42, 56), Interval(2, 2), Interval(9, 9), Interval(80, 86), Interval(74, 94)],
        # Job 49
        [Interval(82, 86), Interval(67, 69), Interval(76, 78), Interval(51, 57), Interval(42, 48),
         Interval(68, 72), Interval(34, 34), Interval(57, 71), Interval(53, 57), Interval(57, 75),
         Interval(16, 16), Interval(11, 11), Interval(9, 9), Interval(70, 88), Interval(50, 58),
         Interval(23, 23), Interval(63, 63), Interval(1, 1), Interval(87, 95), Interval(45, 55)],
    ],
    'name': 'INT__TAI50_20_03.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai50_20_03_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI50_20_03.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI50_20_03.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI50_20_03_F_15_01_INTERVAL_DATA
