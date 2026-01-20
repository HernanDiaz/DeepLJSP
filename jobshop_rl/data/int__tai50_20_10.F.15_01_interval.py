"""
Problema INT__TAI50_20_10.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI50_20_10_F_15_01_INTERVAL_DATA = {
    'num_jobs': 50,
    'num_machines': 20,
    'problem_id': 'int__tai50_20_10.F.15_01_interval',
    'sequences': [
        [10, 1, 2, 7, 17, 4, 3, 18, 0, 14, 6, 19, 15, 16, 13, 12, 5, 11, 9, 8],
        [11, 3, 7, 18, 12, 5, 13, 6, 4, 14, 10, 2, 1, 16, 19, 0, 15, 9, 8, 17],
        [14, 19, 5, 11, 16, 12, 1, 8, 6, 4, 2, 9, 18, 10, 17, 0, 13, 3, 7, 15],
        [10, 16, 15, 2, 14, 1, 11, 7, 5, 18, 12, 0, 4, 8, 17, 6, 9, 3, 19, 13],
        [19, 8, 4, 14, 12, 13, 2, 9, 3, 0, 1, 10, 17, 6, 18, 11, 16, 7, 5, 15],
        [0, 9, 11, 18, 3, 15, 2, 17, 10, 8, 13, 12, 14, 4, 5, 1, 6, 16, 7, 19],
        [0, 8, 12, 5, 11, 16, 7, 2, 15, 3, 10, 18, 6, 13, 14, 19, 17, 1, 4, 9],
        [10, 15, 19, 17, 6, 1, 14, 0, 16, 7, 4, 18, 13, 3, 2, 12, 11, 9, 8, 5],
        [11, 6, 7, 1, 17, 9, 12, 18, 0, 8, 4, 15, 14, 5, 3, 10, 19, 16, 2, 13],
        [13, 18, 8, 14, 11, 16, 10, 15, 0, 9, 1, 4, 19, 7, 3, 2, 5, 12, 17, 6],
        [18, 8, 14, 2, 5, 1, 6, 13, 0, 17, 15, 3, 16, 11, 10, 19, 7, 4, 9, 12],
        [6, 18, 16, 12, 0, 17, 1, 11, 15, 7, 4, 2, 10, 8, 19, 13, 14, 5, 9, 3],
        [19, 13, 18, 11, 6, 3, 5, 14, 16, 4, 7, 15, 10, 17, 12, 8, 1, 9, 0, 2],
        [1, 15, 17, 14, 10, 13, 4, 9, 0, 18, 11, 12, 16, 19, 8, 2, 7, 5, 6, 3],
        [5, 15, 3, 14, 0, 4, 12, 1, 9, 6, 8, 11, 10, 17, 2, 19, 7, 13, 18, 16],
        [13, 19, 18, 12, 11, 14, 17, 1, 2, 6, 0, 15, 7, 10, 3, 9, 5, 8, 4, 16],
        [16, 5, 14, 7, 17, 0, 3, 1, 6, 2, 12, 8, 9, 11, 13, 19, 10, 4, 18, 15],
        [15, 1, 11, 17, 19, 0, 8, 18, 2, 6, 14, 16, 9, 5, 7, 3, 12, 4, 10, 13],
        [5, 1, 17, 3, 18, 10, 12, 19, 7, 15, 0, 2, 6, 11, 9, 14, 8, 13, 4, 16],
        [12, 19, 6, 13, 11, 5, 14, 8, 7, 2, 18, 0, 4, 17, 1, 15, 10, 9, 16, 3],
        [12, 13, 11, 0, 10, 15, 8, 7, 3, 9, 5, 14, 18, 1, 6, 19, 17, 4, 16, 2],
        [12, 18, 13, 6, 2, 14, 7, 10, 3, 17, 19, 15, 8, 11, 1, 0, 9, 4, 16, 5],
        [9, 14, 5, 17, 7, 10, 16, 1, 8, 6, 11, 12, 2, 0, 4, 19, 3, 15, 18, 13],
        [6, 19, 14, 13, 11, 8, 5, 4, 12, 2, 9, 0, 10, 16, 18, 17, 7, 1, 3, 15],
        [4, 2, 11, 12, 14, 8, 17, 0, 9, 18, 19, 3, 5, 13, 16, 6, 1, 10, 15, 7],
        [8, 9, 17, 2, 19, 14, 13, 4, 0, 11, 15, 6, 5, 3, 1, 16, 7, 12, 18, 10],
        [16, 12, 2, 0, 1, 3, 13, 4, 14, 9, 5, 11, 15, 8, 19, 17, 18, 6, 10, 7],
        [19, 14, 2, 16, 17, 5, 8, 12, 6, 3, 13, 10, 7, 11, 9, 1, 0, 15, 4, 18],
        [17, 18, 7, 1, 3, 9, 6, 16, 14, 12, 11, 0, 5, 2, 4, 8, 13, 15, 19, 10],
        [4, 9, 13, 6, 5, 8, 2, 16, 7, 0, 12, 11, 18, 17, 19, 1, 3, 14, 10, 15],
        [4, 6, 9, 11, 8, 10, 13, 7, 5, 2, 0, 3, 14, 12, 19, 1, 16, 17, 18, 15],
        [6, 0, 4, 12, 19, 11, 2, 16, 1, 17, 8, 15, 18, 14, 9, 7, 5, 10, 3, 13],
        [9, 14, 2, 18, 15, 8, 17, 0, 5, 16, 11, 4, 10, 13, 3, 6, 7, 12, 19, 1],
        [2, 9, 7, 6, 14, 17, 11, 12, 18, 8, 1, 10, 4, 16, 13, 15, 19, 5, 0, 3],
        [7, 18, 0, 10, 17, 2, 12, 4, 3, 19, 8, 13, 1, 11, 14, 6, 9, 16, 15, 5],
        [1, 16, 17, 8, 9, 11, 3, 2, 6, 7, 18, 5, 19, 15, 4, 12, 14, 10, 0, 13],
        [3, 10, 14, 19, 12, 11, 0, 4, 8, 13, 7, 9, 15, 1, 16, 5, 17, 6, 2, 18],
        [15, 1, 8, 5, 17, 2, 11, 18, 16, 19, 12, 6, 3, 14, 10, 9, 4, 13, 7, 0],
        [5, 2, 13, 14, 15, 10, 16, 8, 19, 17, 1, 0, 7, 4, 6, 12, 11, 9, 18, 3],
        [15, 0, 7, 16, 9, 19, 5, 12, 2, 1, 17, 13, 18, 6, 3, 10, 8, 11, 4, 14],
        [15, 6, 3, 2, 8, 18, 5, 19, 11, 9, 0, 13, 16, 1, 17, 10, 14, 12, 4, 7],
        [10, 12, 19, 18, 8, 2, 1, 0, 6, 4, 5, 16, 15, 14, 13, 9, 7, 17, 3, 11],
        [11, 16, 17, 1, 0, 9, 4, 3, 6, 10, 18, 14, 7, 5, 8, 12, 15, 2, 13, 19],
        [4, 13, 17, 6, 8, 19, 12, 0, 5, 16, 1, 10, 7, 9, 18, 2, 3, 15, 14, 11],
        [6, 18, 10, 19, 2, 0, 15, 11, 4, 12, 8, 1, 7, 14, 17, 9, 5, 3, 16, 13],
        [7, 19, 0, 1, 3, 13, 17, 2, 8, 14, 4, 16, 12, 5, 9, 10, 11, 6, 18, 15],
        [2, 18, 19, 0, 14, 11, 13, 4, 7, 5, 15, 12, 17, 10, 9, 3, 1, 8, 16, 6],
        [2, 12, 17, 18, 16, 5, 6, 8, 15, 9, 19, 13, 10, 7, 4, 3, 11, 14, 0, 1],
        [10, 7, 16, 5, 12, 0, 14, 3, 1, 11, 13, 18, 15, 17, 9, 4, 19, 8, 2, 6],
        [14, 8, 12, 11, 19, 17, 3, 10, 2, 9, 0, 13, 16, 18, 5, 7, 6, 1, 15, 4],
    ],
    'durations': [
        # Job 0
        [Interval(17, 23), Interval(22, 22), Interval(33, 43), Interval(30, 36), Interval(23, 25),
         Interval(70, 74), Interval(65, 85), Interval(53, 69), Interval(2, 2), Interval(17, 17),
         Interval(63, 71), Interval(45, 55), Interval(59, 71), Interval(66, 88), Interval(60, 70),
         Interval(33, 37), Interval(58, 78), Interval(68, 84), Interval(96, 100), Interval(69, 93)],
        # Job 1
        [Interval(66, 80), Interval(76, 96), Interval(23, 29), Interval(42, 42), Interval(45, 55),
         Interval(12, 14), Interval(79, 105), Interval(13, 17), Interval(73, 81), Interval(73, 75),
         Interval(43, 53), Interval(52, 56), Interval(42, 50), Interval(51, 69), Interval(80, 86),
         Interval(78, 78), Interval(1, 1), Interval(89, 93), Interval(32, 34), Interval(53, 67)],
        # Job 2
        [Interval(62, 72), Interval(58, 68), Interval(51, 57), Interval(56, 74), Interval(28, 30),
         Interval(44, 58), Interval(68, 80), Interval(14, 18), Interval(11, 11), Interval(85, 109),
         Interval(78, 96), Interval(65, 67), Interval(4, 4), Interval(10, 10), Interval(49, 55),
         Interval(84, 86), Interval(52, 68), Interval(63, 65), Interval(40, 40), Interval(45, 53)],
        # Job 3
        [Interval(28, 34), Interval(72, 74), Interval(2, 2), Interval(4, 4), Interval(75, 99),
         Interval(80, 82), Interval(86, 94), Interval(82, 102), Interval(23, 31), Interval(45, 57),
         Interval(4, 4), Interval(40, 44), Interval(18, 24), Interval(66, 88), Interval(65, 77),
         Interval(5, 5), Interval(72, 82), Interval(70, 92), Interval(37, 41), Interval(28, 36)],
        # Job 4
        [Interval(17, 19), Interval(13, 13), Interval(79, 99), Interval(43, 47), Interval(55, 63),
         Interval(80, 100), Interval(75, 97), Interval(67, 75), Interval(5, 5), Interval(49, 59),
         Interval(36, 48), Interval(52, 68), Interval(32, 32), Interval(15, 17), Interval(84, 88),
         Interval(67, 73), Interval(7, 7), Interval(14, 18), Interval(77, 85), Interval(4, 4)],
        # Job 5
        [Interval(52, 66), Interval(47, 63), Interval(3, 3), Interval(43, 43), Interval(24, 28),
         Interval(18, 20), Interval(54, 60), Interval(68, 82), Interval(34, 36), Interval(40, 40),
         Interval(17, 17), Interval(3, 3), Interval(91, 101), Interval(71, 93), Interval(26, 26),
         Interval(20, 26), Interval(86, 108), Interval(23, 23), Interval(56, 74), Interval(24, 32)],
        # Job 6
        [Interval(72, 94), Interval(78, 84), Interval(18, 20), Interval(51, 57), Interval(79, 93),
         Interval(89, 99), Interval(46, 52), Interval(34, 42), Interval(36, 40), Interval(32, 34),
         Interval(80, 106), Interval(60, 66), Interval(45, 57), Interval(42, 48), Interval(66, 70),
         Interval(4, 4), Interval(27, 31), Interval(49, 57), Interval(77, 93), Interval(20, 22)],
        # Job 7
        [Interval(42, 50), Interval(7, 9), Interval(5, 5), Interval(28, 30), Interval(31, 33),
         Interval(29, 39), Interval(3, 3), Interval(9, 11), Interval(44, 46), Interval(68, 72),
         Interval(71, 83), Interval(1, 1), Interval(60, 64), Interval(69, 89), Interval(43, 57),
         Interval(2, 2), Interval(17, 19), Interval(77, 101), Interval(74, 98), Interval(18, 24)],
        # Job 8
        [Interval(17, 17), Interval(40, 54), Interval(7, 7), Interval(17, 23), Interval(9, 9),
         Interval(80, 104), Interval(20, 26), Interval(74, 78), Interval(65, 77), Interval(18, 22),
         Interval(18, 24), Interval(71, 73), Interval(61, 81), Interval(89, 95), Interval(83, 101),
         Interval(16, 18), Interval(8, 10), Interval(34, 42), Interval(20, 26), Interval(32, 36)],
        # Job 9
        [Interval(6, 6), Interval(70, 78), Interval(28, 30), Interval(90, 108), Interval(74, 86),
         Interval(26, 28), Interval(43, 43), Interval(31, 41), Interval(29, 33), Interval(60, 66),
         Interval(33, 35), Interval(26, 26), Interval(95, 101), Interval(47, 47), Interval(65, 73),
         Interval(5, 5), Interval(52, 58), Interval(20, 24), Interval(14, 16), Interval(17, 21)],
        # Job 10
        [Interval(77, 77), Interval(11, 13), Interval(88, 104), Interval(84, 84), Interval(19, 25),
         Interval(15, 17), Interval(52, 66), Interval(81, 107), Interval(59, 79), Interval(60, 76),
         Interval(75, 87), Interval(12, 14), Interval(42, 48), Interval(57, 65), Interval(25, 29),
         Interval(24, 28), Interval(11, 13), Interval(77, 95), Interval(78, 86), Interval(81, 89)],
        # Job 11
        [Interval(24, 30), Interval(77, 85), Interval(2, 2), Interval(27, 31), Interval(57, 65),
         Interval(2, 2), Interval(37, 43), Interval(71, 85), Interval(62, 68), Interval(68, 68),
         Interval(34, 44), Interval(60, 76), Interval(34, 44), Interval(57, 69), Interval(53, 65),
         Interval(68, 90), Interval(95, 97), Interval(10, 12), Interval(66, 86), Interval(42, 54)],
        # Job 12
        [Interval(95, 95), Interval(57, 67), Interval(9, 11), Interval(61, 75), Interval(38, 46),
         Interval(54, 68), Interval(73, 73), Interval(45, 57), Interval(74, 88), Interval(67, 83),
         Interval(35, 39), Interval(95, 97), Interval(62, 68), Interval(41, 49), Interval(40, 48),
         Interval(37, 49), Interval(18, 20), Interval(43, 45), Interval(86, 102), Interval(49, 63)],
        # Job 13
        [Interval(20, 26), Interval(65, 75), Interval(21, 27), Interval(4, 4), Interval(85, 87),
         Interval(78, 102), Interval(84, 88), Interval(72, 94), Interval(74, 76), Interval(40, 52),
         Interval(83, 101), Interval(86, 102), Interval(20, 26), Interval(28, 30), Interval(6, 6),
         Interval(3, 3), Interval(33, 33), Interval(11, 13), Interval(49, 53), Interval(15, 15)],
        # Job 14
        [Interval(6, 8), Interval(48, 62), Interval(24, 28), Interval(30, 30), Interval(75, 83),
         Interval(52, 64), Interval(83, 89), Interval(70, 70), Interval(65, 71), Interval(86, 110),
         Interval(24, 28), Interval(28, 36), Interval(86, 110), Interval(30, 40), Interval(37, 37),
         Interval(13, 13), Interval(82, 88), Interval(82, 88), Interval(14, 14), Interval(31, 37)],
        # Job 15
        [Interval(18, 24), Interval(65, 71), Interval(1, 1), Interval(71, 81), Interval(42, 46),
         Interval(4, 4), Interval(41, 55), Interval(34, 44), Interval(66, 80), Interval(81, 81),
         Interval(48, 52), Interval(97, 97), Interval(38, 44), Interval(76, 82), Interval(10, 10),
         Interval(64, 82), Interval(34, 38), Interval(25, 31), Interval(59, 69), Interval(27, 35)],
        # Job 16
        [Interval(71, 81), Interval(48, 62), Interval(36, 46), Interval(42, 50), Interval(69, 91),
         Interval(96, 102), Interval(94, 104), Interval(54, 64), Interval(14, 14), Interval(84, 88),
         Interval(61, 77), Interval(23, 25), Interval(52, 56), Interval(29, 39), Interval(28, 36),
         Interval(94, 102), Interval(72, 76), Interval(62, 72), Interval(22, 26), Interval(55, 57)],
        # Job 17
        [Interval(14, 14), Interval(32, 32), Interval(69, 85), Interval(80, 82), Interval(30, 40),
         Interval(38, 38), Interval(34, 42), Interval(37, 39), Interval(52, 70), Interval(79, 95),
         Interval(66, 74), Interval(68, 90), Interval(25, 25), Interval(43, 49), Interval(76, 100),
         Interval(18, 18), Interval(66, 86), Interval(93, 103), Interval(73, 77), Interval(23, 23)],
        # Job 18
        [Interval(57, 65), Interval(87, 97), Interval(6, 6), Interval(54, 62), Interval(23, 29),
         Interval(25, 27), Interval(34, 38), Interval(84, 94), Interval(9, 9), Interval(30, 40),
         Interval(53, 55), Interval(5, 5), Interval(71, 73), Interval(81, 101), Interval(4, 4),
         Interval(58, 64), Interval(71, 79), Interval(36, 48), Interval(74, 96), Interval(40, 50)],
        # Job 19
        [Interval(45, 47), Interval(76, 102), Interval(42, 56), Interval(80, 92), Interval(14, 14),
         Interval(62, 62), Interval(53, 53), Interval(56, 62), Interval(23, 31), Interval(76, 96),
         Interval(9, 11), Interval(80, 94), Interval(86, 112), Interval(4, 4), Interval(74, 94),
         Interval(61, 63), Interval(67, 81), Interval(30, 30), Interval(58, 78), Interval(84, 88)],
        # Job 20
        [Interval(1, 1), Interval(3, 3), Interval(81, 87), Interval(69, 87), Interval(36, 48),
         Interval(72, 74), Interval(85, 111), Interval(91, 91), Interval(60, 80), Interval(53, 53),
         Interval(56, 58), Interval(31, 41), Interval(66, 86), Interval(4, 4), Interval(75, 77),
         Interval(19, 25), Interval(66, 74), Interval(58, 76), Interval(6, 6), Interval(14, 18)],
        # Job 21
        [Interval(77, 83), Interval(87, 95), Interval(23, 25), Interval(32, 40), Interval(42, 46),
         Interval(69, 93), Interval(77, 79), Interval(65, 65), Interval(2, 2), Interval(83, 99),
         Interval(57, 67), Interval(35, 47), Interval(39, 41), Interval(95, 97), Interval(56, 72),
         Interval(5, 5), Interval(80, 82), Interval(69, 73), Interval(28, 34), Interval(71, 71)],
        # Job 22
        [Interval(3, 3), Interval(59, 77), Interval(55, 55), Interval(13, 13), Interval(77, 89),
         Interval(12, 14), Interval(12, 12), Interval(87, 109), Interval(76, 96), Interval(10, 10),
         Interval(68, 72), Interval(56, 62), Interval(89, 89), Interval(70, 78), Interval(73, 93),
         Interval(29, 31), Interval(51, 61), Interval(88, 110), Interval(59, 77), Interval(58, 76)],
        # Job 23
        [Interval(33, 37), Interval(73, 75), Interval(55, 63), Interval(17, 17), Interval(56, 56),
         Interval(64, 64), Interval(57, 77), Interval(67, 87), Interval(79, 89), Interval(9, 11),
         Interval(35, 35), Interval(78, 80), Interval(12, 12), Interval(82, 100), Interval(36, 36),
         Interval(74, 94), Interval(1, 1), Interval(38, 44), Interval(91, 105), Interval(81, 81)],
        # Job 24
        [Interval(29, 35), Interval(9, 11), Interval(36, 42), Interval(58, 58), Interval(21, 27),
         Interval(48, 64), Interval(83, 83), Interval(72, 82), Interval(69, 87), Interval(97, 101),
         Interval(94, 96), Interval(57, 77), Interval(69, 93), Interval(13, 17), Interval(5, 5),
         Interval(30, 40), Interval(9, 11), Interval(21, 27), Interval(97, 97), Interval(42, 46)],
        # Job 25
        [Interval(51, 59), Interval(36, 46), Interval(85, 113), Interval(26, 28), Interval(83, 105),
         Interval(12, 12), Interval(32, 34), Interval(3, 3), Interval(62, 80), Interval(5, 5),
         Interval(75, 101), Interval(23, 27), Interval(58, 74), Interval(78, 82), Interval(39, 39),
         Interval(77, 103), Interval(72, 86), Interval(49, 63), Interval(56, 64), Interval(5, 5)],
        # Job 26
        [Interval(67, 71), Interval(37, 45), Interval(25, 25), Interval(80, 84), Interval(31, 33),
         Interval(60, 80), Interval(35, 41), Interval(20, 24), Interval(83, 107), Interval(85, 111),
         Interval(6, 6), Interval(61, 67), Interval(46, 58), Interval(43, 49), Interval(69, 73),
         Interval(35, 47), Interval(35, 45), Interval(32, 38), Interval(19, 25), Interval(31, 35)],
        # Job 27
        [Interval(14, 14), Interval(33, 43), Interval(31, 33), Interval(37, 39), Interval(57, 71),
         Interval(64, 70), Interval(13, 13), Interval(67, 81), Interval(63, 85), Interval(66, 68),
         Interval(37, 41), Interval(48, 58), Interval(53, 57), Interval(15, 15), Interval(93, 93),
         Interval(35, 39), Interval(7, 7), Interval(46, 60), Interval(52, 56), Interval(34, 44)],
        # Job 28
        [Interval(83, 85), Interval(70, 84), Interval(6, 6), Interval(39, 51), Interval(81, 101),
         Interval(75, 79), Interval(11, 13), Interval(86, 106), Interval(23, 25), Interval(89, 91),
         Interval(47, 61), Interval(46, 58), Interval(46, 52), Interval(87, 107), Interval(71, 89),
         Interval(84, 84), Interval(41, 47), Interval(35, 39), Interval(68, 90), Interval(5, 5)],
        # Job 29
        [Interval(68, 70), Interval(25, 31), Interval(29, 35), Interval(61, 75), Interval(54, 64),
         Interval(21, 25), Interval(83, 89), Interval(51, 57), Interval(41, 41), Interval(77, 83),
         Interval(55, 59), Interval(44, 46), Interval(18, 20), Interval(36, 40), Interval(76, 102),
         Interval(18, 24), Interval(5, 5), Interval(58, 70), Interval(64, 66), Interval(15, 17)],
        # Job 30
        [Interval(55, 59), Interval(46, 48), Interval(1, 1), Interval(68, 90), Interval(9, 9),
         Interval(62, 70), Interval(82, 86), Interval(20, 22), Interval(31, 39), Interval(90, 104),
         Interval(74, 92), Interval(43, 47), Interval(16, 20), Interval(21, 21), Interval(19, 19),
         Interval(34, 40), Interval(93, 93), Interval(73, 93), Interval(42, 50), Interval(53, 55)],
        # Job 31
        [Interval(40, 52), Interval(11, 13), Interval(40, 48), Interval(67, 83), Interval(32, 32),
         Interval(13, 17), Interval(42, 56), Interval(4, 4), Interval(25, 33), Interval(72, 80),
         Interval(56, 74), Interval(36, 42), Interval(70, 76), Interval(52, 56), Interval(63, 63),
         Interval(71, 85), Interval(17, 19), Interval(87, 95), Interval(3, 3), Interval(84, 102)],
        # Job 32
        [Interval(91, 105), Interval(7, 7), Interval(41, 53), Interval(55, 57), Interval(37, 37),
         Interval(3, 3), Interval(16, 18), Interval(92, 96), Interval(8, 10), Interval(18, 20),
         Interval(91, 91), Interval(54, 62), Interval(7, 9), Interval(32, 32), Interval(56, 64),
         Interval(5, 5), Interval(58, 70), Interval(3, 3), Interval(51, 61), Interval(96, 100)],
        # Job 33
        [Interval(93, 93), Interval(61, 65), Interval(38, 42), Interval(76, 100), Interval(20, 20),
         Interval(10, 12), Interval(14, 18), Interval(49, 61), Interval(59, 63), Interval(69, 93),
         Interval(17, 17), Interval(14, 18), Interval(40, 50), Interval(46, 46), Interval(85, 85),
         Interval(82, 96), Interval(1, 1), Interval(19, 25), Interval(59, 59), Interval(51, 59)],
        # Job 34
        [Interval(65, 87), Interval(81, 91), Interval(71, 95), Interval(26, 26), Interval(4, 4),
         Interval(52, 70), Interval(62, 82), Interval(73, 89), Interval(41, 47), Interval(45, 51),
         Interval(15, 19), Interval(72, 72), Interval(13, 15), Interval(43, 49), Interval(41, 51),
         Interval(71, 89), Interval(72, 76), Interval(10, 12), Interval(49, 65), Interval(2, 2)],
        # Job 35
        [Interval(13, 13), Interval(42, 56), Interval(65, 87), Interval(41, 41), Interval(3, 3),
         Interval(12, 14), Interval(89, 101), Interval(87, 109), Interval(26, 32), Interval(45, 51),
         Interval(60, 60), Interval(61, 73), Interval(24, 32), Interval(59, 69), Interval(36, 36),
         Interval(40, 54), Interval(71, 85), Interval(75, 91), Interval(30, 34), Interval(82, 94)],
        # Job 36
        [Interval(53, 63), Interval(67, 81), Interval(38, 44), Interval(68, 82), Interval(43, 47),
         Interval(17, 21), Interval(51, 51), Interval(34, 44), Interval(91, 97), Interval(41, 41),
         Interval(60, 64), Interval(72, 78), Interval(34, 38), Interval(5, 5), Interval(80, 80),
         Interval(41, 53), Interval(34, 38), Interval(21, 25), Interval(6, 6), Interval(3, 3)],
        # Job 37
        [Interval(87, 97), Interval(61, 67), Interval(1, 1), Interval(65, 65), Interval(2, 2),
         Interval(82, 92), Interval(43, 47), Interval(70, 76), Interval(30, 30), Interval(57, 77),
         Interval(60, 76), Interval(32, 34), Interval(33, 37), Interval(64, 66), Interval(45, 55),
         Interval(84, 102), Interval(32, 40), Interval(18, 18), Interval(37, 41), Interval(49, 59)],
        # Job 38
        [Interval(39, 41), Interval(10, 12), Interval(8, 8), Interval(27, 31), Interval(23, 29),
         Interval(65, 65), Interval(25, 27), Interval(16, 18), Interval(52, 52), Interval(22, 26),
         Interval(84, 90), Interval(59, 75), Interval(80, 96), Interval(81, 85), Interval(33, 39),
         Interval(29, 31), Interval(90, 104), Interval(17, 21), Interval(85, 109), Interval(60, 76)],
        # Job 39
        [Interval(58, 70), Interval(52, 70), Interval(51, 67), Interval(64, 66), Interval(91, 95),
         Interval(70, 90), Interval(74, 92), Interval(5, 5), Interval(45, 55), Interval(41, 43),
         Interval(48, 50), Interval(59, 79), Interval(77, 95), Interval(12, 16), Interval(84, 84),
         Interval(40, 42), Interval(27, 35), Interval(59, 75), Interval(86, 90), Interval(19, 21)],
        # Job 40
        [Interval(44, 46), Interval(19, 25), Interval(2, 2), Interval(78, 88), Interval(58, 64),
         Interval(54, 56), Interval(83, 87), Interval(69, 75), Interval(35, 39), Interval(48, 64),
         Interval(68, 78), Interval(57, 73), Interval(19, 19), Interval(40, 44), Interval(49, 53),
         Interval(83, 93), Interval(2, 2), Interval(1, 1), Interval(1, 1), Interval(29, 31)],
        # Job 41
        [Interval(63, 85), Interval(28, 28), Interval(83, 91), Interval(89, 93), Interval(66, 70),
         Interval(26, 28), Interval(41, 43), Interval(87, 111), Interval(6, 8), Interval(20, 26),
         Interval(26, 28), Interval(15, 17), Interval(86, 86), Interval(59, 63), Interval(25, 31),
         Interval(57, 67), Interval(82, 92), Interval(62, 82), Interval(83, 103), Interval(64, 70)],
        # Job 42
        [Interval(70, 84), Interval(18, 22), Interval(46, 60), Interval(51, 53), Interval(13, 15),
         Interval(52, 62), Interval(2, 2), Interval(74, 82), Interval(63, 63), Interval(11, 13),
         Interval(9, 11), Interval(1, 1), Interval(55, 63), Interval(1, 1), Interval(66, 68),
         Interval(52, 54), Interval(72, 80), Interval(16, 18), Interval(75, 85), Interval(12, 12)],
        # Job 43
        [Interval(72, 76), Interval(80, 92), Interval(75, 81), Interval(47, 63), Interval(70, 80),
         Interval(35, 39), Interval(31, 41), Interval(44, 54), Interval(43, 57), Interval(92, 94),
         Interval(50, 54), Interval(74, 80), Interval(77, 89), Interval(25, 33), Interval(80, 88),
         Interval(56, 64), Interval(84, 100), Interval(57, 65), Interval(31, 31), Interval(3, 3)],
        # Job 44
        [Interval(65, 87), Interval(24, 28), Interval(33, 43), Interval(61, 61), Interval(57, 77),
         Interval(57, 63), Interval(36, 44), Interval(6, 8), Interval(17, 23), Interval(6, 8),
         Interval(95, 99), Interval(69, 83), Interval(16, 20), Interval(78, 88), Interval(39, 39),
         Interval(58, 70), Interval(42, 44), Interval(37, 41), Interval(76, 82), Interval(79, 79)],
        # Job 45
        [Interval(58, 64), Interval(65, 81), Interval(86, 96), Interval(39, 45), Interval(65, 75),
         Interval(70, 76), Interval(34, 34), Interval(74, 88), Interval(18, 20), Interval(57, 71),
         Interval(50, 58), Interval(88, 104), Interval(83, 95), Interval(3, 3), Interval(52, 58),
         Interval(80, 108), Interval(85, 101), Interval(22, 26), Interval(9, 11), Interval(87, 111)],
        # Job 46
        [Interval(65, 81), Interval(10, 10), Interval(6, 6), Interval(63, 71), Interval(21, 23),
         Interval(44, 56), Interval(4, 4), Interval(26, 32), Interval(32, 36), Interval(13, 17),
         Interval(40, 52), Interval(30, 34), Interval(66, 66), Interval(27, 29), Interval(67, 67),
         Interval(55, 71), Interval(55, 65), Interval(37, 41), Interval(63, 67), Interval(18, 20)],
        # Job 47
        [Interval(92, 96), Interval(73, 81), Interval(32, 40), Interval(87, 107), Interval(38, 38),
         Interval(8, 8), Interval(63, 79), Interval(74, 92), Interval(41, 45), Interval(74, 98),
         Interval(30, 36), Interval(85, 103), Interval(26, 34), Interval(32, 34), Interval(76, 102),
         Interval(36, 38), Interval(1, 1), Interval(31, 39), Interval(90, 98), Interval(28, 36)],
        # Job 48
        [Interval(24, 24), Interval(67, 67), Interval(61, 61), Interval(41, 41), Interval(17, 19),
         Interval(4, 4), Interval(85, 97), Interval(72, 74), Interval(33, 33), Interval(85, 107),
         Interval(55, 63), Interval(61, 65), Interval(36, 44), Interval(5, 5), Interval(10, 10),
         Interval(44, 46), Interval(24, 30), Interval(51, 55), Interval(24, 24), Interval(69, 93)],
        # Job 49
        [Interval(27, 35), Interval(92, 106), Interval(14, 14), Interval(63, 65), Interval(83, 95),
         Interval(40, 46), Interval(84, 102), Interval(28, 36), Interval(31, 33), Interval(26, 26),
         Interval(20, 24), Interval(31, 35), Interval(80, 98), Interval(36, 46), Interval(35, 45),
         Interval(74, 100), Interval(23, 29), Interval(84, 112), Interval(53, 53), Interval(84, 112)],
    ],
    'name': 'INT__TAI50_20_10.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai50_20_10_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI50_20_10.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI50_20_10.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI50_20_10_F_15_01_INTERVAL_DATA
