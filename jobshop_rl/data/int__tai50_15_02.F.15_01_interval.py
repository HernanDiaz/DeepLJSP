"""
Problema INT__TAI50_15_02.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI50_15_02_F_15_01_INTERVAL_DATA = {
    'num_jobs': 50,
    'num_machines': 15,
    'problem_id': 'int__tai50_15_02.F.15_01_interval',
    'sequences': [
        [1, 12, 2, 6, 10, 0, 11, 9, 4, 7, 5, 13, 14, 3, 8],
        [7, 1, 0, 11, 4, 9, 10, 2, 5, 6, 13, 12, 8, 3, 14],
        [9, 3, 5, 10, 8, 6, 12, 4, 7, 0, 13, 14, 11, 2, 1],
        [10, 7, 3, 12, 8, 0, 5, 6, 11, 1, 14, 9, 2, 4, 13],
        [11, 0, 9, 3, 7, 13, 8, 6, 5, 1, 2, 12, 14, 10, 4],
        [2, 4, 14, 7, 1, 8, 0, 6, 5, 10, 13, 3, 9, 12, 11],
        [4, 3, 7, 10, 9, 8, 2, 13, 14, 11, 1, 6, 5, 0, 12],
        [13, 14, 2, 12, 5, 8, 10, 4, 0, 3, 7, 11, 1, 9, 6],
        [14, 6, 1, 3, 0, 7, 4, 9, 10, 8, 12, 2, 11, 13, 5],
        [4, 3, 7, 6, 0, 8, 10, 1, 11, 12, 13, 9, 5, 14, 2],
        [1, 3, 14, 8, 2, 5, 9, 6, 12, 0, 7, 10, 11, 4, 13],
        [12, 2, 4, 6, 11, 9, 3, 7, 8, 5, 10, 14, 1, 13, 0],
        [6, 14, 2, 11, 0, 3, 12, 5, 1, 8, 13, 9, 7, 10, 4],
        [5, 11, 4, 0, 9, 10, 14, 12, 3, 7, 1, 8, 2, 13, 6],
        [8, 3, 14, 12, 9, 10, 4, 5, 13, 7, 2, 11, 1, 6, 0],
        [11, 4, 13, 0, 14, 5, 9, 10, 12, 6, 3, 2, 8, 1, 7],
        [14, 0, 5, 4, 10, 1, 8, 9, 12, 11, 3, 13, 7, 6, 2],
        [14, 13, 1, 9, 8, 12, 6, 10, 0, 11, 7, 4, 3, 2, 5],
        [10, 0, 12, 4, 7, 1, 6, 5, 3, 2, 9, 8, 11, 13, 14],
        [2, 8, 10, 0, 11, 14, 6, 1, 4, 7, 13, 12, 5, 3, 9],
        [3, 14, 11, 7, 0, 9, 12, 13, 4, 8, 1, 10, 5, 6, 2],
        [9, 8, 7, 1, 0, 3, 6, 14, 2, 4, 5, 10, 13, 11, 12],
        [10, 14, 6, 9, 13, 5, 7, 0, 12, 11, 8, 2, 3, 1, 4],
        [12, 2, 0, 5, 13, 9, 6, 14, 1, 8, 3, 7, 4, 10, 11],
        [4, 1, 14, 7, 6, 2, 10, 0, 11, 5, 13, 3, 8, 12, 9],
        [0, 14, 11, 4, 6, 1, 10, 8, 3, 13, 9, 12, 7, 2, 5],
        [4, 3, 0, 10, 6, 9, 5, 14, 7, 1, 12, 2, 11, 13, 8],
        [7, 9, 2, 4, 14, 10, 8, 1, 3, 13, 11, 0, 5, 12, 6],
        [6, 10, 11, 14, 9, 0, 1, 2, 7, 8, 5, 3, 12, 4, 13],
        [8, 12, 14, 7, 11, 0, 10, 13, 2, 6, 3, 9, 5, 4, 1],
        [9, 5, 12, 7, 14, 1, 0, 6, 3, 4, 2, 8, 13, 10, 11],
        [4, 5, 10, 1, 0, 2, 8, 9, 14, 12, 6, 13, 11, 3, 7],
        [9, 7, 0, 10, 13, 14, 8, 12, 1, 2, 4, 6, 11, 3, 5],
        [1, 8, 0, 12, 5, 11, 2, 4, 7, 14, 9, 6, 10, 3, 13],
        [14, 8, 5, 9, 6, 0, 13, 3, 2, 12, 7, 4, 1, 11, 10],
        [5, 12, 8, 14, 0, 1, 10, 3, 9, 4, 7, 2, 13, 6, 11],
        [4, 0, 11, 14, 5, 1, 6, 7, 9, 12, 8, 3, 10, 2, 13],
        [7, 2, 10, 14, 6, 3, 8, 0, 1, 13, 4, 12, 5, 11, 9],
        [8, 6, 5, 2, 7, 3, 0, 13, 14, 9, 1, 10, 12, 11, 4],
        [2, 11, 14, 0, 6, 7, 13, 5, 12, 8, 10, 1, 4, 9, 3],
        [9, 12, 7, 8, 11, 14, 5, 10, 13, 1, 2, 0, 4, 6, 3],
        [12, 10, 0, 13, 4, 8, 3, 1, 7, 9, 6, 14, 11, 2, 5],
        [14, 7, 8, 4, 6, 13, 5, 9, 3, 0, 1, 2, 12, 10, 11],
        [14, 6, 3, 11, 1, 2, 10, 5, 8, 9, 12, 7, 4, 13, 0],
        [12, 3, 0, 11, 4, 2, 7, 1, 6, 10, 8, 5, 13, 14, 9],
        [2, 7, 0, 4, 5, 10, 13, 1, 11, 3, 9, 12, 8, 14, 6],
        [6, 3, 0, 8, 10, 9, 4, 7, 2, 13, 14, 11, 1, 12, 5],
        [8, 2, 5, 10, 6, 7, 0, 11, 1, 9, 4, 14, 3, 13, 12],
        [5, 11, 3, 12, 7, 6, 2, 0, 13, 9, 14, 1, 4, 10, 8],
        [3, 11, 5, 6, 1, 2, 10, 8, 13, 14, 12, 9, 4, 0, 7],
    ],
    'durations': [
        # Job 0
        [Interval(15, 19), Interval(55, 55), Interval(54, 70), Interval(65, 83), Interval(37, 39),
         Interval(43, 45), Interval(25, 33), Interval(41, 53), Interval(90, 98), Interval(36, 40),
         Interval(58, 70), Interval(67, 83), Interval(51, 69), Interval(72, 84), Interval(10, 10)],
        # Job 1
        [Interval(16, 20), Interval(53, 65), Interval(85, 89), Interval(34, 46), Interval(48, 58),
         Interval(33, 43), Interval(39, 49), Interval(38, 38), Interval(6, 8), Interval(8, 10),
         Interval(82, 110), Interval(57, 77), Interval(55, 61), Interval(28, 28), Interval(57, 71)],
        # Job 2
        [Interval(40, 44), Interval(10, 12), Interval(80, 106), Interval(69, 75), Interval(58, 58),
         Interval(48, 50), Interval(44, 48), Interval(19, 23), Interval(87, 99), Interval(47, 55),
         Interval(13, 13), Interval(62, 82), Interval(75, 81), Interval(37, 49), Interval(50, 60)],
        # Job 3
        [Interval(83, 103), Interval(44, 50), Interval(71, 93), Interval(58, 70), Interval(38, 38),
         Interval(23, 25), Interval(16, 18), Interval(7, 7), Interval(43, 55), Interval(4, 4),
         Interval(67, 71), Interval(39, 39), Interval(23, 27), Interval(77, 93), Interval(51, 53)],
        # Job 4
        [Interval(41, 55), Interval(79, 81), Interval(46, 50), Interval(3, 3), Interval(6, 8),
         Interval(59, 79), Interval(47, 59), Interval(44, 48), Interval(1, 1), Interval(45, 59),
         Interval(32, 42), Interval(23, 27), Interval(79, 89), Interval(74, 96), Interval(13, 15)],
        # Job 5
        [Interval(43, 55), Interval(40, 44), Interval(59, 65), Interval(77, 95), Interval(14, 14),
         Interval(24, 26), Interval(55, 69), Interval(55, 71), Interval(81, 91), Interval(6, 8),
         Interval(71, 95), Interval(74, 94), Interval(53, 55), Interval(22, 24), Interval(16, 16)],
        # Job 6
        [Interval(54, 58), Interval(76, 82), Interval(86, 108), Interval(32, 36), Interval(3, 3),
         Interval(73, 93), Interval(34, 44), Interval(44, 44), Interval(40, 46), Interval(92, 104),
         Interval(93, 105), Interval(2, 2), Interval(42, 52), Interval(95, 99), Interval(8, 8)],
        # Job 7
        [Interval(60, 62), Interval(80, 88), Interval(83, 109), Interval(62, 66), Interval(50, 66),
         Interval(57, 71), Interval(14, 14), Interval(34, 46), Interval(82, 106), Interval(12, 14),
         Interval(24, 24), Interval(61, 67), Interval(59, 67), Interval(54, 62), Interval(70, 78)],
        # Job 8
        [Interval(87, 99), Interval(4, 4), Interval(25, 31), Interval(40, 46), Interval(88, 96),
         Interval(47, 63), Interval(83, 91), Interval(17, 21), Interval(21, 25), Interval(22, 24),
         Interval(92, 106), Interval(82, 96), Interval(38, 46), Interval(67, 75), Interval(87, 105)],
        # Job 9
        [Interval(52, 60), Interval(30, 32), Interval(70, 74), Interval(75, 101), Interval(6, 6),
         Interval(43, 57), Interval(65, 67), Interval(90, 96), Interval(24, 28), Interval(17, 17),
         Interval(54, 70), Interval(4, 4), Interval(12, 14), Interval(43, 49), Interval(30, 40)],
        # Job 10
        [Interval(6, 8), Interval(71, 91), Interval(97, 97), Interval(45, 59), Interval(88, 98),
         Interval(25, 31), Interval(74, 74), Interval(15, 19), Interval(42, 54), Interval(44, 46),
         Interval(47, 55), Interval(60, 70), Interval(64, 84), Interval(2, 2), Interval(10, 10)],
        # Job 11
        [Interval(73, 97), Interval(82, 88), Interval(84, 102), Interval(32, 38), Interval(46, 56),
         Interval(6, 6), Interval(81, 101), Interval(85, 113), Interval(9, 9), Interval(36, 40),
         Interval(3, 3), Interval(14, 16), Interval(36, 42), Interval(51, 59), Interval(33, 37)],
        # Job 12
        [Interval(14, 14), Interval(24, 32), Interval(46, 52), Interval(50, 56), Interval(91, 97),
         Interval(7, 7), Interval(14, 14), Interval(29, 29), Interval(29, 31), Interval(44, 50),
         Interval(46, 54), Interval(51, 57), Interval(23, 27), Interval(89, 91), Interval(73, 95)],
        # Job 13
        [Interval(15, 17), Interval(43, 43), Interval(70, 94), Interval(2, 2), Interval(80, 92),
         Interval(61, 79), Interval(42, 56), Interval(23, 29), Interval(56, 70), Interval(32, 36),
         Interval(76, 96), Interval(1, 1), Interval(25, 27), Interval(8, 8), Interval(10, 12)],
        # Job 14
        [Interval(82, 98), Interval(17, 21), Interval(48, 60), Interval(26, 28), Interval(36, 40),
         Interval(52, 62), Interval(65, 71), Interval(66, 74), Interval(71, 81), Interval(28, 32),
         Interval(50, 60), Interval(94, 102), Interval(9, 9), Interval(49, 65), Interval(71, 91)],
        # Job 15
        [Interval(21, 27), Interval(86, 104), Interval(81, 101), Interval(49, 65), Interval(70, 72),
         Interval(61, 81), Interval(73, 95), Interval(43, 55), Interval(94, 94), Interval(67, 81),
         Interval(17, 19), Interval(20, 24), Interval(31, 35), Interval(65, 81), Interval(81, 81)],
        # Job 16
        [Interval(76, 96), Interval(5, 5), Interval(85, 103), Interval(1, 1), Interval(60, 76),
         Interval(47, 53), Interval(53, 53), Interval(14, 14), Interval(75, 89), Interval(73, 87),
         Interval(36, 48), Interval(1, 1), Interval(68, 76), Interval(47, 49), Interval(59, 69)],
        # Job 17
        [Interval(17, 21), Interval(39, 51), Interval(47, 53), Interval(12, 16), Interval(3, 3),
         Interval(81, 83), Interval(4, 4), Interval(48, 62), Interval(92, 96), Interval(66, 86),
         Interval(63, 65), Interval(59, 79), Interval(29, 35), Interval(18, 22), Interval(42, 54)],
        # Job 18
        [Interval(51, 55), Interval(33, 33), Interval(77, 103), Interval(13, 13), Interval(70, 76),
         Interval(43, 53), Interval(46, 58), Interval(52, 62), Interval(71, 71), Interval(13, 13),
         Interval(49, 61), Interval(92, 98), Interval(49, 49), Interval(31, 33), Interval(7, 9)],
        # Job 19
        [Interval(66, 78), Interval(1, 1), Interval(7, 9), Interval(55, 71), Interval(6, 8),
         Interval(5, 5), Interval(30, 30), Interval(70, 72), Interval(72, 76), Interval(76, 82),
         Interval(35, 37), Interval(65, 77), Interval(28, 34), Interval(76, 82), Interval(40, 46)],
        # Job 20
        [Interval(89, 97), Interval(82, 110), Interval(80, 106), Interval(79, 97), Interval(4, 4),
         Interval(12, 12), Interval(32, 36), Interval(11, 11), Interval(16, 18), Interval(19, 21),
         Interval(74, 74), Interval(61, 79), Interval(13, 13), Interval(47, 57), Interval(76, 90)],
        # Job 21
        [Interval(74, 100), Interval(37, 41), Interval(74, 94), Interval(60, 78), Interval(59, 71),
         Interval(17, 21), Interval(79, 85), Interval(46, 50), Interval(79, 95), Interval(84, 90),
         Interval(1, 1), Interval(56, 60), Interval(79, 101), Interval(21, 23), Interval(77, 85)],
        # Job 22
        [Interval(49, 65), Interval(15, 19), Interval(56, 60), Interval(26, 28), Interval(44, 52),
         Interval(35, 41), Interval(75, 79), Interval(91, 93), Interval(11, 11), Interval(19, 23),
         Interval(69, 71), Interval(60, 78), Interval(47, 47), Interval(81, 101), Interval(68, 72)],
        # Job 23
        [Interval(79, 105), Interval(16, 18), Interval(6, 6), Interval(55, 61), Interval(40, 54),
         Interval(90, 90), Interval(31, 35), Interval(22, 28), Interval(21, 23), Interval(85, 109),
         Interval(38, 42), Interval(62, 64), Interval(94, 96), Interval(16, 18), Interval(19, 21)],
        # Job 24
        [Interval(81, 93), Interval(68, 92), Interval(3, 3), Interval(92, 102), Interval(50, 56),
         Interval(36, 40), Interval(26, 30), Interval(27, 35), Interval(46, 48), Interval(4, 4),
         Interval(46, 46), Interval(10, 12), Interval(66, 74), Interval(51, 57), Interval(38, 50)],
        # Job 25
        [Interval(71, 93), Interval(44, 56), Interval(59, 61), Interval(13, 17), Interval(57, 75),
         Interval(51, 59), Interval(25, 25), Interval(44, 44), Interval(93, 95), Interval(70, 76),
         Interval(67, 89), Interval(84, 108), Interval(19, 25), Interval(17, 19), Interval(4, 4)],
        # Job 26
        [Interval(79, 103), Interval(9, 11), Interval(86, 88), Interval(59, 71), Interval(12, 12),
         Interval(63, 83), Interval(17, 17), Interval(6, 6), Interval(82, 88), Interval(25, 33),
         Interval(47, 61), Interval(71, 73), Interval(37, 49), Interval(48, 48), Interval(25, 33)],
        # Job 27
        [Interval(48, 48), Interval(40, 42), Interval(38, 50), Interval(86, 112), Interval(14, 14),
         Interval(8, 10), Interval(20, 22), Interval(61, 79), Interval(76, 98), Interval(64, 68),
         Interval(36, 38), Interval(78, 86), Interval(26, 32), Interval(53, 59), Interval(9, 11)],
        # Job 28
        [Interval(28, 28), Interval(64, 64), Interval(79, 95), Interval(47, 55), Interval(46, 58),
         Interval(83, 87), Interval(85, 85), Interval(52, 66), Interval(43, 45), Interval(77, 83),
         Interval(45, 57), Interval(11, 11), Interval(55, 71), Interval(68, 68), Interval(85, 85)],
        # Job 29
        [Interval(30, 34), Interval(34, 42), Interval(85, 95), Interval(16, 20), Interval(8, 10),
         Interval(33, 33), Interval(42, 44), Interval(56, 62), Interval(52, 52), Interval(86, 96),
         Interval(50, 64), Interval(37, 39), Interval(14, 16), Interval(16, 20), Interval(69, 89)],
        # Job 30
        [Interval(12, 16), Interval(30, 32), Interval(94, 98), Interval(87, 103), Interval(82, 84),
         Interval(68, 68), Interval(7, 7), Interval(78, 104), Interval(42, 56), Interval(30, 34),
         Interval(82, 104), Interval(87, 89), Interval(11, 11), Interval(2, 2), Interval(2, 2)],
        # Job 31
        [Interval(22, 22), Interval(35, 43), Interval(25, 25), Interval(22, 28), Interval(79, 89),
         Interval(46, 52), Interval(68, 68), Interval(16, 20), Interval(17, 23), Interval(6, 8),
         Interval(93, 93), Interval(83, 103), Interval(55, 73), Interval(56, 56), Interval(57, 65)],
        # Job 32
        [Interval(85, 107), Interval(13, 13), Interval(58, 58), Interval(17, 23), Interval(5, 5),
         Interval(23, 29), Interval(23, 29), Interval(6, 6), Interval(17, 23), Interval(4, 4),
         Interval(51, 69), Interval(33, 41), Interval(2, 2), Interval(45, 45), Interval(50, 54)],
        # Job 33
        [Interval(46, 52), Interval(31, 41), Interval(22, 28), Interval(27, 29), Interval(41, 51),
         Interval(22, 24), Interval(34, 36), Interval(7, 9), Interval(57, 77), Interval(41, 49),
         Interval(40, 52), Interval(13, 13), Interval(4, 4), Interval(16, 16), Interval(6, 6)],
        # Job 34
        [Interval(11, 13), Interval(76, 92), Interval(54, 70), Interval(74, 84), Interval(95, 101),
         Interval(40, 48), Interval(25, 25), Interval(25, 25), Interval(28, 30), Interval(15, 19),
         Interval(11, 13), Interval(36, 42), Interval(51, 65), Interval(22, 28), Interval(55, 59)],
        # Job 35
        [Interval(3, 3), Interval(38, 48), Interval(4, 4), Interval(81, 93), Interval(63, 65),
         Interval(31, 41), Interval(70, 90), Interval(20, 24), Interval(17, 23), Interval(54, 64),
         Interval(26, 26), Interval(39, 51), Interval(38, 40), Interval(95, 103), Interval(64, 80)],
        # Job 36
        [Interval(37, 41), Interval(46, 50), Interval(50, 60), Interval(64, 86), Interval(64, 64),
         Interval(21, 23), Interval(39, 47), Interval(87, 95), Interval(7, 7), Interval(66, 66),
         Interval(21, 23), Interval(42, 44), Interval(52, 66), Interval(37, 39), Interval(68, 92)],
        # Job 37
        [Interval(50, 50), Interval(68, 82), Interval(43, 57), Interval(61, 75), Interval(32, 34),
         Interval(86, 112), Interval(29, 35), Interval(44, 48), Interval(10, 10), Interval(70, 92),
         Interval(83, 103), Interval(28, 30), Interval(12, 14), Interval(88, 108), Interval(13, 13)],
        # Job 38
        [Interval(56, 64), Interval(13, 15), Interval(46, 62), Interval(11, 11), Interval(87, 109),
         Interval(4, 4), Interval(50, 62), Interval(16, 18), Interval(17, 19), Interval(25, 31),
         Interval(82, 88), Interval(54, 60), Interval(82, 82), Interval(96, 102), Interval(4, 4)],
        # Job 39
        [Interval(76, 82), Interval(89, 93), Interval(21, 25), Interval(20, 22), Interval(78, 104),
         Interval(46, 58), Interval(44, 52), Interval(1, 1), Interval(23, 23), Interval(81, 95),
         Interval(6, 6), Interval(70, 76), Interval(12, 12), Interval(1, 1), Interval(3, 3)],
        # Job 40
        [Interval(31, 41), Interval(38, 42), Interval(37, 41), Interval(14, 14), Interval(76, 84),
         Interval(21, 27), Interval(46, 52), Interval(24, 30), Interval(84, 94), Interval(4, 4),
         Interval(60, 76), Interval(76, 78), Interval(95, 101), Interval(13, 15), Interval(74, 74)],
        # Job 41
        [Interval(53, 69), Interval(44, 52), Interval(55, 57), Interval(7, 9), Interval(66, 86),
         Interval(23, 27), Interval(38, 48), Interval(66, 68), Interval(9, 11), Interval(80, 104),
         Interval(58, 76), Interval(32, 34), Interval(44, 58), Interval(42, 48), Interval(93, 103)],
        # Job 42
        [Interval(44, 46), Interval(38, 38), Interval(72, 86), Interval(32, 38), Interval(23, 25),
         Interval(1, 1), Interval(46, 56), Interval(81, 95), Interval(94, 94), Interval(81, 101),
         Interval(47, 49), Interval(2, 2), Interval(49, 49), Interval(8, 8), Interval(84, 88)],
        # Job 43
        [Interval(40, 48), Interval(6, 6), Interval(29, 33), Interval(49, 49), Interval(10, 12),
         Interval(40, 48), Interval(97, 99), Interval(75, 87), Interval(38, 46), Interval(89, 107),
         Interval(75, 79), Interval(9, 9), Interval(53, 57), Interval(28, 30), Interval(8, 10)],
        # Job 44
        [Interval(46, 48), Interval(80, 94), Interval(44, 56), Interval(35, 45), Interval(82, 88),
         Interval(74, 98), Interval(18, 18), Interval(43, 53), Interval(81, 101), Interval(94, 94),
         Interval(98, 98), Interval(80, 92), Interval(49, 63), Interval(75, 75), Interval(43, 49)],
        # Job 45
        [Interval(38, 50), Interval(50, 56), Interval(86, 112), Interval(95, 95), Interval(28, 36),
         Interval(29, 37), Interval(61, 75), Interval(20, 24), Interval(46, 52), Interval(84, 108),
         Interval(8, 8), Interval(80, 94), Interval(73, 83), Interval(6, 6), Interval(55, 69)],
        # Job 46
        [Interval(77, 95), Interval(94, 100), Interval(15, 17), Interval(29, 37), Interval(44, 50),
         Interval(80, 106), Interval(10, 12), Interval(82, 82), Interval(6, 8), Interval(17, 19),
         Interval(26, 32), Interval(15, 19), Interval(52, 60), Interval(80, 80), Interval(75, 89)],
        # Job 47
        [Interval(15, 19), Interval(8, 10), Interval(17, 17), Interval(57, 73), Interval(79, 97),
         Interval(33, 41), Interval(49, 57), Interval(37, 43), Interval(32, 38), Interval(22, 26),
         Interval(66, 76), Interval(48, 56), Interval(29, 31), Interval(71, 91), Interval(2, 2)],
        # Job 48
        [Interval(65, 65), Interval(77, 103), Interval(37, 39), Interval(95, 99), Interval(92, 100),
         Interval(14, 14), Interval(81, 89), Interval(73, 73), Interval(84, 106), Interval(81, 93),
         Interval(9, 11), Interval(17, 19), Interval(16, 18), Interval(4, 4), Interval(58, 58)],
        # Job 49
        [Interval(65, 73), Interval(61, 67), Interval(73, 81), Interval(3, 3), Interval(73, 77),
         Interval(85, 113), Interval(65, 83), Interval(54, 58), Interval(27, 31), Interval(94, 98),
         Interval(75, 91), Interval(58, 70), Interval(17, 21), Interval(18, 18), Interval(36, 40)],
    ],
    'name': 'INT__TAI50_15_02.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai50_15_02_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI50_15_02.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI50_15_02.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI50_15_02_F_15_01_INTERVAL_DATA
