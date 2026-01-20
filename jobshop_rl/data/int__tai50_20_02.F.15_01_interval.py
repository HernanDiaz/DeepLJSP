"""
Problema INT__TAI50_20_02.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI50_20_02_F_15_01_INTERVAL_DATA = {
    'num_jobs': 50,
    'num_machines': 20,
    'problem_id': 'int__tai50_20_02.F.15_01_interval',
    'sequences': [
        [18, 12, 17, 4, 5, 11, 10, 8, 9, 13, 15, 1, 16, 7, 14, 19, 0, 6, 3, 2],
        [13, 7, 2, 6, 5, 8, 12, 0, 9, 15, 1, 19, 18, 10, 4, 11, 14, 16, 17, 3],
        [10, 7, 1, 15, 18, 2, 14, 9, 11, 5, 19, 3, 8, 13, 6, 16, 17, 4, 12, 0],
        [10, 12, 18, 2, 9, 13, 8, 5, 4, 19, 3, 6, 0, 14, 16, 15, 1, 7, 11, 17],
        [2, 7, 14, 19, 1, 5, 0, 15, 6, 4, 16, 17, 8, 3, 11, 13, 18, 10, 12, 9],
        [6, 19, 17, 10, 3, 15, 2, 13, 11, 1, 18, 0, 8, 16, 9, 5, 12, 7, 14, 4],
        [0, 2, 4, 10, 3, 7, 13, 15, 12, 18, 17, 14, 11, 8, 19, 16, 1, 6, 9, 5],
        [16, 0, 10, 6, 4, 7, 9, 13, 19, 5, 2, 17, 12, 18, 11, 3, 8, 14, 1, 15],
        [19, 8, 4, 9, 18, 7, 10, 6, 11, 1, 2, 15, 16, 5, 0, 3, 17, 12, 14, 13],
        [1, 17, 3, 5, 11, 4, 9, 18, 19, 16, 14, 6, 8, 0, 10, 15, 12, 7, 2, 13],
        [19, 3, 18, 7, 13, 16, 10, 11, 0, 1, 12, 15, 8, 6, 9, 4, 2, 14, 17, 5],
        [12, 4, 8, 1, 11, 16, 5, 13, 0, 9, 19, 10, 15, 17, 2, 18, 6, 14, 7, 3],
        [18, 6, 3, 4, 14, 0, 11, 5, 10, 1, 12, 9, 13, 15, 17, 2, 19, 8, 16, 7],
        [10, 7, 1, 19, 9, 0, 6, 3, 16, 12, 14, 4, 5, 15, 17, 18, 13, 8, 2, 11],
        [2, 15, 1, 19, 9, 10, 16, 7, 3, 12, 8, 18, 11, 0, 14, 4, 13, 17, 6, 5],
        [1, 9, 4, 16, 2, 11, 7, 3, 0, 5, 15, 8, 14, 10, 6, 17, 13, 18, 12, 19],
        [10, 2, 1, 17, 8, 0, 9, 16, 14, 4, 12, 7, 6, 11, 15, 5, 18, 13, 19, 3],
        [8, 11, 19, 12, 15, 9, 10, 14, 2, 18, 17, 16, 7, 6, 13, 4, 1, 3, 0, 5],
        [10, 19, 18, 5, 14, 0, 1, 11, 13, 15, 9, 16, 4, 12, 6, 7, 3, 8, 17, 2],
        [6, 10, 5, 9, 11, 7, 13, 1, 17, 4, 15, 12, 14, 18, 2, 16, 19, 0, 8, 3],
        [10, 15, 12, 7, 2, 11, 8, 5, 14, 1, 9, 18, 16, 19, 3, 4, 6, 13, 0, 17],
        [19, 13, 9, 2, 6, 7, 15, 10, 11, 8, 17, 4, 1, 18, 3, 14, 0, 5, 12, 16],
        [12, 8, 18, 2, 1, 11, 6, 19, 7, 16, 3, 14, 4, 9, 17, 13, 5, 15, 10, 0],
        [18, 5, 10, 14, 2, 4, 9, 17, 8, 19, 12, 6, 1, 11, 3, 16, 0, 13, 7, 15],
        [11, 19, 15, 17, 3, 16, 0, 7, 10, 1, 6, 13, 18, 2, 14, 5, 8, 12, 9, 4],
        [4, 1, 12, 7, 10, 11, 9, 19, 6, 2, 18, 17, 14, 0, 5, 16, 8, 13, 3, 15],
        [18, 2, 8, 3, 11, 0, 14, 12, 4, 9, 17, 5, 6, 10, 19, 13, 7, 15, 16, 1],
        [16, 17, 13, 1, 5, 7, 14, 10, 0, 19, 6, 2, 8, 9, 12, 15, 18, 3, 11, 4],
        [4, 1, 10, 6, 8, 9, 2, 12, 7, 17, 11, 0, 14, 13, 19, 16, 3, 5, 15, 18],
        [9, 17, 7, 8, 2, 11, 14, 13, 3, 15, 10, 19, 18, 1, 6, 4, 16, 12, 0, 5],
        [2, 12, 11, 8, 18, 17, 7, 6, 5, 1, 9, 13, 19, 14, 16, 10, 3, 0, 4, 15],
        [16, 4, 1, 17, 7, 11, 18, 0, 14, 9, 8, 6, 10, 13, 15, 12, 5, 19, 2, 3],
        [17, 7, 14, 9, 4, 13, 2, 10, 8, 15, 11, 6, 3, 5, 0, 12, 16, 18, 19, 1],
        [6, 1, 12, 18, 7, 19, 5, 10, 11, 16, 0, 9, 14, 15, 13, 3, 2, 8, 4, 17],
        [5, 18, 19, 17, 14, 4, 0, 8, 10, 2, 12, 16, 9, 6, 7, 1, 13, 11, 15, 3],
        [15, 14, 9, 8, 16, 2, 18, 17, 19, 12, 7, 3, 1, 11, 4, 0, 10, 6, 13, 5],
        [16, 15, 19, 14, 18, 3, 2, 10, 5, 8, 7, 13, 6, 17, 0, 4, 12, 1, 11, 9],
        [1, 2, 12, 11, 15, 19, 0, 10, 17, 16, 18, 9, 6, 5, 7, 4, 3, 8, 14, 13],
        [9, 19, 2, 6, 11, 3, 15, 16, 4, 13, 7, 12, 8, 14, 0, 18, 1, 10, 17, 5],
        [12, 16, 3, 5, 0, 9, 2, 1, 11, 8, 10, 18, 4, 6, 14, 7, 15, 13, 19, 17],
        [11, 19, 3, 17, 7, 18, 14, 5, 16, 4, 8, 6, 12, 9, 13, 15, 2, 1, 0, 10],
        [6, 1, 8, 11, 19, 2, 5, 14, 3, 12, 7, 0, 9, 4, 17, 18, 16, 13, 15, 10],
        [7, 12, 17, 19, 6, 11, 15, 10, 9, 3, 5, 18, 8, 13, 2, 1, 0, 16, 14, 4],
        [16, 11, 14, 8, 4, 5, 3, 15, 2, 0, 17, 9, 18, 6, 19, 1, 7, 13, 10, 12],
        [16, 3, 9, 17, 14, 0, 6, 5, 8, 4, 19, 12, 2, 1, 13, 7, 10, 18, 15, 11],
        [11, 3, 8, 9, 2, 14, 17, 0, 18, 15, 10, 7, 19, 6, 4, 12, 16, 1, 13, 5],
        [7, 9, 2, 11, 12, 1, 6, 3, 16, 13, 14, 10, 17, 15, 0, 8, 19, 4, 18, 5],
        [13, 17, 1, 3, 2, 15, 12, 5, 10, 11, 6, 14, 18, 0, 8, 4, 16, 19, 9, 7],
        [5, 10, 16, 15, 9, 11, 12, 17, 7, 1, 8, 4, 0, 14, 3, 2, 6, 13, 19, 18],
        [1, 7, 9, 13, 2, 12, 6, 0, 18, 19, 10, 4, 17, 11, 5, 3, 8, 15, 14, 16],
    ],
    'durations': [
        # Job 0
        [Interval(46, 62), Interval(96, 96), Interval(84, 108), Interval(55, 69), Interval(68, 74),
         Interval(41, 43), Interval(54, 70), Interval(82, 104), Interval(94, 102), Interval(10, 10),
         Interval(48, 60), Interval(12, 14), Interval(32, 42), Interval(56, 66), Interval(88, 96),
         Interval(77, 103), Interval(53, 65), Interval(63, 65), Interval(82, 110), Interval(58, 70)],
        # Job 1
        [Interval(74, 94), Interval(82, 104), Interval(22, 22), Interval(6, 8), Interval(71, 95),
         Interval(48, 64), Interval(80, 108), Interval(50, 54), Interval(6, 6), Interval(84, 86),
         Interval(34, 42), Interval(79, 85), Interval(3, 3), Interval(84, 104), Interval(28, 36),
         Interval(17, 17), Interval(66, 66), Interval(78, 80), Interval(9, 9), Interval(30, 38)],
        # Job 2
        [Interval(62, 72), Interval(64, 74), Interval(5, 5), Interval(13, 15), Interval(46, 60),
         Interval(12, 12), Interval(15, 19), Interval(86, 100), Interval(25, 31), Interval(53, 61),
         Interval(8, 10), Interval(70, 86), Interval(19, 19), Interval(59, 65), Interval(47, 53),
         Interval(84, 86), Interval(3, 3), Interval(50, 64), Interval(93, 97), Interval(74, 76)],
        # Job 3
        [Interval(91, 107), Interval(14, 18), Interval(82, 86), Interval(44, 58), Interval(83, 85),
         Interval(17, 19), Interval(18, 24), Interval(46, 62), Interval(7, 9), Interval(36, 40),
         Interval(68, 92), Interval(4, 4), Interval(69, 93), Interval(24, 28), Interval(45, 51),
         Interval(44, 58), Interval(87, 99), Interval(66, 86), Interval(31, 33), Interval(47, 53)],
        # Job 4
        [Interval(8, 10), Interval(5, 5), Interval(2, 2), Interval(68, 74), Interval(56, 64),
         Interval(87, 109), Interval(3, 3), Interval(23, 29), Interval(56, 64), Interval(52, 62),
         Interval(47, 63), Interval(41, 53), Interval(44, 46), Interval(45, 49), Interval(77, 81),
         Interval(56, 60), Interval(95, 103), Interval(80, 100), Interval(20, 22), Interval(69, 87)],
        # Job 5
        [Interval(78, 102), Interval(92, 92), Interval(89, 103), Interval(41, 47), Interval(83, 93),
         Interval(72, 86), Interval(76, 80), Interval(3, 3), Interval(17, 17), Interval(11, 11),
         Interval(32, 36), Interval(13, 17), Interval(45, 47), Interval(40, 54), Interval(79, 101),
         Interval(57, 59), Interval(81, 109), Interval(29, 37), Interval(49, 65), Interval(88, 94)],
        # Job 6
        [Interval(24, 26), Interval(93, 105), Interval(16, 18), Interval(61, 67), Interval(78, 88),
         Interval(55, 69), Interval(43, 49), Interval(20, 22), Interval(84, 112), Interval(48, 52),
         Interval(49, 63), Interval(53, 61), Interval(4, 4), Interval(64, 68), Interval(51, 59),
         Interval(3, 3), Interval(13, 15), Interval(9, 11), Interval(23, 25), Interval(85, 101)],
        # Job 7
        [Interval(86, 102), Interval(18, 18), Interval(68, 72), Interval(79, 105), Interval(29, 39),
         Interval(29, 29), Interval(63, 67), Interval(18, 20), Interval(82, 88), Interval(48, 62),
         Interval(38, 50), Interval(81, 93), Interval(51, 67), Interval(29, 39), Interval(76, 96),
         Interval(72, 72), Interval(24, 32), Interval(59, 65), Interval(19, 25), Interval(35, 35)],
        # Job 8
        [Interval(76, 100), Interval(9, 11), Interval(39, 41), Interval(88, 104), Interval(43, 49),
         Interval(42, 54), Interval(73, 75), Interval(70, 94), Interval(88, 94), Interval(41, 49),
         Interval(79, 91), Interval(48, 58), Interval(68, 84), Interval(29, 37), Interval(62, 72),
         Interval(60, 66), Interval(42, 46), Interval(74, 90), Interval(47, 55), Interval(45, 49)],
        # Job 9
        [Interval(45, 45), Interval(14, 18), Interval(59, 67), Interval(15, 17), Interval(84, 88),
         Interval(73, 75), Interval(56, 60), Interval(39, 39), Interval(47, 53), Interval(27, 29),
         Interval(46, 54), Interval(64, 72), Interval(35, 43), Interval(6, 6), Interval(35, 35),
         Interval(6, 6), Interval(12, 14), Interval(24, 28), Interval(15, 15), Interval(48, 64)],
        # Job 10
        [Interval(23, 25), Interval(72, 94), Interval(46, 60), Interval(51, 69), Interval(59, 75),
         Interval(73, 83), Interval(17, 21), Interval(48, 54), Interval(13, 15), Interval(44, 52),
         Interval(52, 62), Interval(45, 59), Interval(82, 102), Interval(47, 51), Interval(70, 78),
         Interval(74, 90), Interval(31, 33), Interval(59, 67), Interval(85, 97), Interval(63, 73)],
        # Job 11
        [Interval(6, 8), Interval(74, 80), Interval(96, 98), Interval(84, 112), Interval(17, 23),
         Interval(49, 63), Interval(60, 72), Interval(51, 63), Interval(46, 62), Interval(58, 58),
         Interval(17, 23), Interval(26, 34), Interval(68, 86), Interval(68, 68), Interval(58, 68),
         Interval(6, 6), Interval(57, 69), Interval(60, 74), Interval(21, 25), Interval(23, 29)],
        # Job 12
        [Interval(76, 76), Interval(71, 91), Interval(30, 36), Interval(31, 39), Interval(80, 90),
         Interval(29, 29), Interval(10, 10), Interval(48, 56), Interval(10, 12), Interval(18, 24),
         Interval(1, 1), Interval(90, 102), Interval(44, 46), Interval(29, 33), Interval(38, 48),
         Interval(10, 12), Interval(44, 50), Interval(35, 47), Interval(69, 69), Interval(46, 60)],
        # Job 13
        [Interval(3, 3), Interval(51, 53), Interval(3, 3), Interval(74, 96), Interval(34, 34),
         Interval(23, 29), Interval(67, 83), Interval(85, 99), Interval(73, 93), Interval(8, 8),
         Interval(79, 79), Interval(59, 79), Interval(56, 60), Interval(64, 70), Interval(1, 1),
         Interval(71, 87), Interval(56, 72), Interval(45, 53), Interval(57, 57), Interval(4, 4)],
        # Job 14
        [Interval(28, 32), Interval(17, 21), Interval(30, 32), Interval(44, 44), Interval(2, 2),
         Interval(17, 17), Interval(71, 93), Interval(13, 15), Interval(72, 92), Interval(83, 107),
         Interval(22, 28), Interval(67, 67), Interval(74, 76), Interval(40, 42), Interval(89, 95),
         Interval(3, 3), Interval(6, 6), Interval(21, 23), Interval(31, 37), Interval(17, 23)],
        # Job 15
        [Interval(16, 16), Interval(58, 66), Interval(47, 51), Interval(8, 10), Interval(39, 51),
         Interval(37, 45), Interval(23, 23), Interval(41, 45), Interval(35, 35), Interval(39, 45),
         Interval(85, 91), Interval(19, 19), Interval(3, 3), Interval(7, 9), Interval(91, 101),
         Interval(24, 30), Interval(28, 32), Interval(32, 42), Interval(18, 20), Interval(24, 32)],
        # Job 16
        [Interval(17, 21), Interval(58, 70), Interval(65, 85), Interval(20, 20), Interval(94, 104),
         Interval(77, 93), Interval(54, 58), Interval(95, 101), Interval(31, 39), Interval(67, 73),
         Interval(42, 46), Interval(14, 18), Interval(22, 28), Interval(6, 6), Interval(10, 10),
         Interval(23, 23), Interval(7, 9), Interval(89, 107), Interval(25, 25), Interval(98, 100)],
        # Job 17
        [Interval(1, 1), Interval(24, 24), Interval(39, 47), Interval(5, 5), Interval(31, 31),
         Interval(47, 61), Interval(1, 1), Interval(47, 47), Interval(59, 75), Interval(60, 64),
         Interval(21, 27), Interval(33, 39), Interval(88, 100), Interval(14, 18), Interval(8, 8),
         Interval(52, 60), Interval(14, 18), Interval(18, 18), Interval(43, 55), Interval(65, 73)],
        # Job 18
        [Interval(95, 99), Interval(88, 90), Interval(67, 75), Interval(82, 92), Interval(73, 83),
         Interval(73, 97), Interval(17, 19), Interval(18, 20), Interval(19, 21), Interval(90, 102),
         Interval(43, 57), Interval(65, 67), Interval(53, 53), Interval(62, 78), Interval(46, 50),
         Interval(19, 21), Interval(35, 47), Interval(81, 105), Interval(80, 102), Interval(50, 52)],
        # Job 19
        [Interval(77, 103), Interval(25, 33), Interval(23, 27), Interval(66, 70), Interval(18, 18),
         Interval(47, 47), Interval(78, 86), Interval(30, 40), Interval(24, 32), Interval(8, 10),
         Interval(42, 48), Interval(52, 68), Interval(56, 72), Interval(32, 32), Interval(15, 17),
         Interval(26, 26), Interval(40, 54), Interval(32, 34), Interval(85, 93), Interval(35, 43)],
        # Job 20
        [Interval(69, 89), Interval(61, 63), Interval(22, 28), Interval(47, 47), Interval(4, 4),
         Interval(12, 16), Interval(41, 41), Interval(8, 8), Interval(79, 103), Interval(60, 80),
         Interval(27, 27), Interval(77, 103), Interval(69, 77), Interval(52, 66), Interval(18, 24),
         Interval(64, 70), Interval(74, 80), Interval(53, 57), Interval(48, 60), Interval(39, 43)],
        # Job 21
        [Interval(34, 44), Interval(63, 65), Interval(55, 55), Interval(74, 88), Interval(6, 6),
         Interval(68, 78), Interval(15, 19), Interval(43, 45), Interval(27, 27), Interval(50, 64),
         Interval(15, 15), Interval(32, 34), Interval(14, 18), Interval(38, 38), Interval(1, 1),
         Interval(53, 69), Interval(11, 11), Interval(56, 56), Interval(60, 70), Interval(42, 52)],
        # Job 22
        [Interval(45, 51), Interval(50, 62), Interval(6, 8), Interval(34, 34), Interval(57, 61),
         Interval(61, 69), Interval(1, 1), Interval(65, 65), Interval(8, 8), Interval(17, 21),
         Interval(30, 32), Interval(52, 62), Interval(59, 75), Interval(50, 64), Interval(81, 107),
         Interval(31, 33), Interval(48, 50), Interval(29, 33), Interval(72, 72), Interval(68, 68)],
        # Job 23
        [Interval(65, 65), Interval(10, 12), Interval(71, 93), Interval(47, 53), Interval(35, 43),
         Interval(55, 57), Interval(58, 58), Interval(59, 59), Interval(5, 5), Interval(30, 36),
         Interval(81, 81), Interval(82, 104), Interval(43, 49), Interval(22, 24), Interval(80, 80),
         Interval(22, 26), Interval(12, 14), Interval(9, 11), Interval(36, 36), Interval(38, 48)],
        # Job 24
        [Interval(51, 69), Interval(32, 32), Interval(35, 39), Interval(12, 14), Interval(55, 57),
         Interval(6, 6), Interval(74, 74), Interval(71, 95), Interval(43, 57), Interval(52, 68),
         Interval(11, 13), Interval(78, 102), Interval(52, 66), Interval(32, 32), Interval(69, 75),
         Interval(71, 81), Interval(76, 98), Interval(22, 28), Interval(22, 24), Interval(57, 71)],
        # Job 25
        [Interval(23, 25), Interval(76, 80), Interval(39, 49), Interval(5, 5), Interval(74, 100),
         Interval(54, 66), Interval(47, 59), Interval(18, 18), Interval(90, 92), Interval(57, 77),
         Interval(54, 64), Interval(71, 91), Interval(8, 8), Interval(16, 16), Interval(84, 104),
         Interval(93, 95), Interval(46, 48), Interval(26, 26), Interval(63, 83), Interval(64, 74)],
        # Job 26
        [Interval(7, 9), Interval(64, 84), Interval(81, 105), Interval(9, 9), Interval(73, 91),
         Interval(81, 93), Interval(39, 41), Interval(6, 6), Interval(61, 79), Interval(73, 93),
         Interval(78, 94), Interval(79, 101), Interval(70, 84), Interval(13, 13), Interval(56, 74),
         Interval(20, 22), Interval(79, 87), Interval(52, 64), Interval(90, 100), Interval(46, 50)],
        # Job 27
        [Interval(6, 8), Interval(80, 106), Interval(74, 76), Interval(77, 87), Interval(30, 38),
         Interval(27, 29), Interval(8, 8), Interval(32, 32), Interval(59, 67), Interval(5, 5),
         Interval(26, 28), Interval(78, 102), Interval(31, 33), Interval(13, 17), Interval(52, 52),
         Interval(57, 69), Interval(10, 12), Interval(86, 106), Interval(25, 25), Interval(19, 25)],
        # Job 28
        [Interval(66, 80), Interval(70, 76), Interval(33, 33), Interval(64, 82), Interval(17, 21),
         Interval(45, 51), Interval(6, 8), Interval(66, 82), Interval(77, 77), Interval(45, 51),
         Interval(5, 5), Interval(45, 49), Interval(33, 43), Interval(72, 74), Interval(74, 92),
         Interval(22, 26), Interval(72, 88), Interval(73, 87), Interval(36, 46), Interval(26, 26)],
        # Job 29
        [Interval(48, 52), Interval(34, 34), Interval(92, 98), Interval(43, 45), Interval(31, 31),
         Interval(74, 86), Interval(55, 63), Interval(46, 60), Interval(21, 27), Interval(17, 19),
         Interval(36, 38), Interval(67, 77), Interval(69, 75), Interval(71, 75), Interval(6, 6),
         Interval(74, 98), Interval(16, 18), Interval(13, 13), Interval(87, 91), Interval(23, 25)],
        # Job 30
        [Interval(84, 106), Interval(92, 106), Interval(31, 39), Interval(52, 58), Interval(59, 75),
         Interval(54, 54), Interval(15, 15), Interval(23, 27), Interval(2, 2), Interval(60, 60),
         Interval(31, 39), Interval(13, 15), Interval(14, 14), Interval(32, 42), Interval(71, 93),
         Interval(34, 40), Interval(42, 52), Interval(28, 28), Interval(32, 42), Interval(18, 24)],
        # Job 31
        [Interval(21, 27), Interval(22, 24), Interval(58, 78), Interval(12, 14), Interval(93, 103),
         Interval(65, 69), Interval(58, 58), Interval(73, 89), Interval(57, 67), Interval(11, 11),
         Interval(90, 108), Interval(69, 81), Interval(41, 41), Interval(20, 26), Interval(13, 13),
         Interval(35, 35), Interval(69, 77), Interval(35, 35), Interval(65, 77), Interval(26, 30)],
        # Job 32
        [Interval(87, 87), Interval(36, 42), Interval(60, 72), Interval(67, 67), Interval(85, 97),
         Interval(64, 78), Interval(43, 53), Interval(17, 17), Interval(12, 12), Interval(92, 98),
         Interval(82, 90), Interval(62, 80), Interval(19, 19), Interval(45, 53), Interval(55, 71),
         Interval(59, 73), Interval(67, 71), Interval(63, 83), Interval(83, 91), Interval(7, 9)],
        # Job 33
        [Interval(61, 77), Interval(3, 3), Interval(11, 11), Interval(76, 76), Interval(53, 61),
         Interval(48, 62), Interval(36, 36), Interval(88, 102), Interval(54, 72), Interval(74, 82),
         Interval(62, 82), Interval(28, 28), Interval(46, 60), Interval(9, 11), Interval(78, 94),
         Interval(12, 14), Interval(50, 56), Interval(12, 16), Interval(4, 4), Interval(52, 52)],
        # Job 34
        [Interval(62, 72), Interval(55, 63), Interval(75, 93), Interval(45, 55), Interval(88, 94),
         Interval(85, 101), Interval(46, 60), Interval(52, 60), Interval(26, 34), Interval(84, 112),
         Interval(53, 53), Interval(68, 80), Interval(56, 64), Interval(41, 51), Interval(51, 63),
         Interval(22, 24), Interval(27, 27), Interval(45, 53), Interval(46, 62), Interval(43, 51)],
        # Job 35
        [Interval(99, 99), Interval(71, 93), Interval(3, 3), Interval(55, 67), Interval(83, 101),
         Interval(61, 73), Interval(62, 70), Interval(74, 88), Interval(56, 68), Interval(38, 44),
         Interval(70, 84), Interval(9, 9), Interval(49, 63), Interval(80, 80), Interval(77, 103),
         Interval(66, 70), Interval(80, 82), Interval(56, 60), Interval(83, 89), Interval(56, 62)],
        # Job 36
        [Interval(76, 76), Interval(68, 86), Interval(22, 24), Interval(27, 31), Interval(24, 26),
         Interval(42, 46), Interval(15, 15), Interval(16, 18), Interval(92, 100), Interval(61, 67),
         Interval(70, 72), Interval(19, 25), Interval(76, 98), Interval(70, 76), Interval(68, 76),
         Interval(8, 8), Interval(60, 74), Interval(83, 101), Interval(54, 68), Interval(97, 97)],
        # Job 37
        [Interval(86, 98), Interval(42, 52), Interval(93, 97), Interval(50, 60), Interval(76, 80),
         Interval(54, 62), Interval(31, 41), Interval(1, 1), Interval(23, 23), Interval(67, 75),
         Interval(42, 52), Interval(76, 76), Interval(30, 38), Interval(92, 98), Interval(22, 28),
         Interval(4, 4), Interval(83, 99), Interval(22, 22), Interval(47, 55), Interval(52, 54)],
        # Job 38
        [Interval(53, 61), Interval(52, 70), Interval(35, 43), Interval(19, 25), Interval(54, 66),
         Interval(77, 103), Interval(46, 62), Interval(2, 2), Interval(81, 85), Interval(72, 74),
         Interval(32, 40), Interval(60, 76), Interval(89, 109), Interval(67, 69), Interval(59, 63),
         Interval(66, 86), Interval(79, 97), Interval(13, 17), Interval(96, 96), Interval(77, 83)],
        # Job 39
        [Interval(6, 6), Interval(52, 66), Interval(87, 111), Interval(30, 30), Interval(68, 78),
         Interval(55, 57), Interval(35, 43), Interval(9, 9), Interval(76, 84), Interval(85, 89),
         Interval(72, 76), Interval(6, 6), Interval(53, 57), Interval(37, 41), Interval(34, 44),
         Interval(39, 45), Interval(68, 88), Interval(37, 37), Interval(63, 69), Interval(35, 39)],
        # Job 40
        [Interval(11, 11), Interval(80, 86), Interval(71, 95), Interval(85, 89), Interval(33, 35),
         Interval(44, 46), Interval(75, 81), Interval(13, 13), Interval(58, 60), Interval(82, 104),
         Interval(14, 18), Interval(75, 95), Interval(72, 80), Interval(51, 57), Interval(91, 91),
         Interval(90, 96), Interval(12, 14), Interval(52, 60), Interval(10, 10), Interval(85, 113)],
        # Job 41
        [Interval(24, 28), Interval(43, 47), Interval(72, 88), Interval(41, 47), Interval(8, 10),
         Interval(27, 29), Interval(64, 76), Interval(87, 103), Interval(38, 42), Interval(20, 20),
         Interval(54, 72), Interval(40, 48), Interval(58, 68), Interval(72, 74), Interval(58, 60),
         Interval(77, 87), Interval(38, 44), Interval(82, 92), Interval(88, 90), Interval(28, 30)],
        # Job 42
        [Interval(60, 68), Interval(85, 93), Interval(53, 71), Interval(28, 32), Interval(13, 13),
         Interval(56, 72), Interval(38, 46), Interval(34, 44), Interval(88, 90), Interval(85, 93),
         Interval(55, 59), Interval(58, 66), Interval(86, 112), Interval(52, 58), Interval(37, 43),
         Interval(86, 102), Interval(24, 26), Interval(34, 34), Interval(4, 4), Interval(56, 74)],
        # Job 43
        [Interval(52, 64), Interval(87, 111), Interval(16, 16), Interval(40, 52), Interval(68, 76),
         Interval(36, 44), Interval(42, 54), Interval(13, 17), Interval(12, 16), Interval(15, 15),
         Interval(36, 42), Interval(15, 19), Interval(49, 55), Interval(43, 43), Interval(8, 10),
         Interval(71, 75), Interval(6, 6), Interval(61, 69), Interval(56, 60), Interval(13, 13)],
        # Job 44
        [Interval(19, 19), Interval(64, 80), Interval(75, 85), Interval(44, 52), Interval(74, 84),
         Interval(68, 74), Interval(29, 29), Interval(13, 15), Interval(18, 20), Interval(24, 30),
         Interval(85, 99), Interval(89, 105), Interval(92, 106), Interval(70, 78), Interval(59, 79),
         Interval(18, 22), Interval(36, 44), Interval(35, 47), Interval(83, 107), Interval(35, 43)],
        # Job 45
        [Interval(62, 64), Interval(24, 26), Interval(71, 77), Interval(34, 46), Interval(12, 16),
         Interval(91, 105), Interval(23, 29), Interval(47, 63), Interval(9, 9), Interval(92, 92),
         Interval(64, 70), Interval(99, 99), Interval(42, 54), Interval(18, 22), Interval(82, 92),
         Interval(53, 57), Interval(61, 69), Interval(65, 67), Interval(10, 10), Interval(4, 4)],
        # Job 46
        [Interval(2, 2), Interval(80, 98), Interval(89, 109), Interval(89, 89), Interval(71, 75),
         Interval(11, 13), Interval(70, 86), Interval(55, 59), Interval(33, 43), Interval(16, 18),
         Interval(58, 70), Interval(70, 90), Interval(45, 49), Interval(65, 87), Interval(95, 103),
         Interval(64, 80), Interval(30, 32), Interval(45, 59), Interval(48, 50), Interval(76, 76)],
        # Job 47
        [Interval(45, 45), Interval(22, 22), Interval(10, 12), Interval(93, 105), Interval(64, 66),
         Interval(96, 96), Interval(84, 106), Interval(43, 51), Interval(8, 8), Interval(52, 62),
         Interval(58, 62), Interval(37, 39), Interval(64, 78), Interval(68, 72), Interval(95, 101),
         Interval(49, 65), Interval(4, 4), Interval(27, 35), Interval(68, 78), Interval(56, 56)],
        # Job 48
        [Interval(28, 28), Interval(25, 27), Interval(43, 51), Interval(69, 85), Interval(76, 102),
         Interval(78, 86), Interval(94, 94), Interval(37, 45), Interval(81, 97), Interval(66, 82),
         Interval(84, 106), Interval(39, 49), Interval(51, 69), Interval(76, 100), Interval(52, 70),
         Interval(98, 100), Interval(31, 41), Interval(46, 52), Interval(36, 46), Interval(1, 1)],
        # Job 49
        [Interval(16, 16), Interval(61, 81), Interval(48, 50), Interval(25, 25), Interval(54, 70),
         Interval(96, 100), Interval(62, 64), Interval(78, 80), Interval(28, 30), Interval(75, 89),
         Interval(81, 87), Interval(76, 76), Interval(76, 94), Interval(18, 18), Interval(67, 89),
         Interval(18, 18), Interval(84, 90), Interval(65, 65), Interval(9, 11), Interval(73, 83)],
    ],
    'name': 'INT__TAI50_20_02.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai50_20_02_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI50_20_02.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI50_20_02.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI50_20_02_F_15_01_INTERVAL_DATA
