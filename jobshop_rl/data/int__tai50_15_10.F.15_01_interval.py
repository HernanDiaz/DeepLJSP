"""
Problema INT__TAI50_15_10.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI50_15_10_F_15_01_INTERVAL_DATA = {
    'num_jobs': 50,
    'num_machines': 15,
    'problem_id': 'int__tai50_15_10.F.15_01_interval',
    'sequences': [
        [2, 10, 12, 8, 9, 0, 14, 13, 6, 7, 4, 11, 3, 5, 1],
        [3, 1, 10, 12, 0, 2, 9, 8, 13, 11, 6, 14, 5, 4, 7],
        [8, 0, 2, 1, 3, 7, 13, 6, 4, 10, 12, 11, 5, 9, 14],
        [10, 4, 1, 6, 12, 3, 5, 11, 14, 2, 13, 9, 8, 0, 7],
        [2, 1, 14, 8, 11, 13, 12, 6, 5, 3, 7, 4, 9, 0, 10],
        [11, 12, 9, 7, 14, 6, 2, 1, 4, 0, 3, 8, 10, 13, 5],
        [0, 8, 12, 1, 5, 4, 7, 14, 10, 2, 11, 9, 13, 3, 6],
        [3, 7, 13, 9, 12, 8, 10, 11, 4, 2, 0, 5, 1, 6, 14],
        [13, 12, 9, 6, 3, 14, 2, 8, 10, 11, 4, 1, 5, 7, 0],
        [9, 10, 8, 12, 13, 11, 1, 5, 2, 7, 14, 6, 3, 0, 4],
        [7, 3, 2, 8, 6, 10, 5, 1, 13, 0, 12, 11, 14, 4, 9],
        [8, 12, 1, 2, 14, 4, 10, 5, 6, 9, 0, 13, 11, 7, 3],
        [9, 13, 3, 14, 5, 2, 11, 0, 6, 8, 4, 12, 10, 7, 1],
        [12, 3, 5, 8, 7, 13, 6, 1, 14, 0, 11, 2, 4, 10, 9],
        [6, 4, 1, 5, 3, 9, 0, 7, 14, 11, 10, 8, 13, 12, 2],
        [1, 8, 0, 9, 10, 13, 7, 5, 4, 6, 14, 11, 12, 3, 2],
        [7, 13, 1, 9, 6, 10, 2, 8, 12, 4, 11, 14, 5, 3, 0],
        [13, 3, 2, 4, 0, 8, 12, 11, 7, 6, 10, 1, 14, 9, 5],
        [4, 9, 1, 6, 0, 5, 13, 2, 12, 3, 10, 14, 7, 8, 11],
        [0, 3, 2, 13, 12, 10, 5, 14, 1, 6, 11, 8, 9, 4, 7],
        [4, 1, 13, 9, 10, 0, 7, 8, 14, 6, 3, 11, 5, 12, 2],
        [12, 6, 10, 0, 5, 3, 13, 1, 11, 8, 14, 9, 2, 7, 4],
        [9, 6, 3, 0, 12, 2, 5, 7, 8, 13, 14, 4, 10, 11, 1],
        [0, 3, 8, 13, 11, 12, 14, 7, 9, 6, 10, 1, 2, 4, 5],
        [2, 5, 0, 12, 13, 9, 3, 11, 10, 8, 4, 7, 6, 1, 14],
        [13, 2, 4, 6, 12, 9, 7, 1, 11, 3, 8, 14, 5, 10, 0],
        [0, 11, 8, 4, 7, 6, 13, 1, 5, 3, 9, 10, 2, 14, 12],
        [10, 5, 0, 9, 1, 13, 3, 7, 4, 6, 12, 8, 14, 11, 2],
        [1, 8, 4, 10, 13, 3, 12, 0, 14, 9, 6, 11, 7, 2, 5],
        [8, 13, 6, 3, 1, 7, 9, 0, 12, 14, 2, 4, 10, 5, 11],
        [4, 3, 12, 1, 13, 0, 6, 8, 14, 2, 7, 9, 11, 10, 5],
        [0, 8, 1, 7, 14, 5, 4, 10, 9, 12, 6, 2, 13, 3, 11],
        [3, 6, 12, 11, 0, 2, 5, 1, 14, 8, 13, 4, 9, 10, 7],
        [5, 4, 14, 7, 0, 8, 13, 2, 12, 9, 1, 6, 11, 10, 3],
        [6, 9, 12, 11, 2, 1, 8, 5, 14, 10, 4, 7, 13, 3, 0],
        [10, 2, 4, 0, 14, 12, 13, 1, 8, 5, 9, 6, 7, 11, 3],
        [11, 4, 8, 6, 2, 7, 14, 12, 5, 3, 0, 1, 9, 13, 10],
        [14, 7, 2, 11, 0, 4, 9, 8, 5, 6, 10, 3, 13, 12, 1],
        [0, 14, 11, 4, 2, 6, 5, 13, 12, 1, 10, 7, 8, 9, 3],
        [2, 5, 13, 8, 11, 12, 6, 4, 9, 10, 14, 7, 0, 1, 3],
        [1, 9, 4, 5, 2, 0, 13, 7, 6, 11, 3, 12, 8, 10, 14],
        [6, 4, 11, 8, 10, 7, 5, 13, 3, 1, 12, 2, 9, 14, 0],
        [12, 2, 6, 5, 14, 10, 8, 0, 9, 7, 1, 4, 11, 13, 3],
        [14, 9, 5, 1, 0, 3, 6, 7, 2, 13, 12, 10, 11, 4, 8],
        [9, 4, 1, 14, 7, 6, 0, 10, 12, 5, 13, 8, 11, 3, 2],
        [2, 5, 8, 12, 0, 10, 6, 9, 4, 3, 1, 7, 14, 13, 11],
        [10, 3, 9, 14, 13, 5, 2, 0, 4, 6, 12, 7, 11, 8, 1],
        [7, 10, 9, 14, 5, 12, 8, 11, 3, 2, 13, 0, 6, 4, 1],
        [7, 0, 2, 3, 11, 14, 5, 12, 4, 9, 1, 13, 8, 10, 6],
        [9, 2, 6, 8, 7, 12, 0, 3, 14, 13, 10, 11, 1, 5, 4],
    ],
    'durations': [
        # Job 0
        [Interval(66, 86), Interval(34, 34), Interval(24, 32), Interval(7, 9), Interval(10, 10),
         Interval(72, 76), Interval(80, 104), Interval(26, 34), Interval(10, 10), Interval(78, 86),
         Interval(41, 49), Interval(66, 82), Interval(21, 27), Interval(80, 94), Interval(36, 40)],
        # Job 1
        [Interval(77, 103), Interval(49, 61), Interval(16, 16), Interval(66, 88), Interval(78, 94),
         Interval(73, 93), Interval(23, 29), Interval(91, 93), Interval(21, 25), Interval(43, 57),
         Interval(63, 85), Interval(69, 93), Interval(14, 16), Interval(14, 14), Interval(28, 34)],
        # Job 2
        [Interval(34, 36), Interval(50, 62), Interval(28, 36), Interval(62, 66), Interval(70, 70),
         Interval(77, 79), Interval(22, 24), Interval(41, 51), Interval(8, 8), Interval(69, 81),
         Interval(43, 47), Interval(5, 5), Interval(6, 8), Interval(60, 64), Interval(63, 83)],
        # Job 3
        [Interval(68, 80), Interval(12, 14), Interval(73, 83), Interval(77, 99), Interval(29, 35),
         Interval(26, 26), Interval(8, 8), Interval(2, 2), Interval(25, 29), Interval(29, 29),
         Interval(54, 70), Interval(47, 49), Interval(25, 25), Interval(72, 84), Interval(7, 9)],
        # Job 4
        [Interval(93, 97), Interval(59, 77), Interval(64, 66), Interval(89, 97), Interval(60, 76),
         Interval(64, 86), Interval(48, 60), Interval(2, 2), Interval(57, 63), Interval(85, 113),
         Interval(12, 14), Interval(3, 3), Interval(61, 71), Interval(53, 61), Interval(52, 68)],
        # Job 5
        [Interval(40, 46), Interval(73, 95), Interval(7, 7), Interval(66, 74), Interval(38, 48),
         Interval(36, 38), Interval(39, 45), Interval(82, 102), Interval(61, 79), Interval(85, 97),
         Interval(27, 33), Interval(5, 5), Interval(49, 65), Interval(62, 78), Interval(78, 82)],
        # Job 6
        [Interval(79, 87), Interval(95, 99), Interval(12, 12), Interval(19, 19), Interval(44, 56),
         Interval(17, 19), Interval(36, 46), Interval(57, 75), Interval(24, 24), Interval(91, 105),
         Interval(11, 11), Interval(20, 22), Interval(26, 32), Interval(6, 6), Interval(84, 88)],
        # Job 7
        [Interval(86, 86), Interval(4, 4), Interval(92, 96), Interval(49, 55), Interval(19, 25),
         Interval(74, 78), Interval(70, 92), Interval(41, 53), Interval(90, 94), Interval(81, 109),
         Interval(13, 17), Interval(29, 37), Interval(82, 88), Interval(36, 40), Interval(51, 57)],
        # Job 8
        [Interval(73, 87), Interval(53, 59), Interval(51, 57), Interval(77, 97), Interval(21, 23),
         Interval(89, 97), Interval(31, 41), Interval(79, 87), Interval(87, 111), Interval(25, 29),
         Interval(15, 15), Interval(6, 8), Interval(63, 75), Interval(70, 84), Interval(47, 53)],
        # Job 9
        [Interval(39, 47), Interval(45, 53), Interval(13, 13), Interval(26, 28), Interval(80, 108),
         Interval(78, 104), Interval(77, 81), Interval(77, 83), Interval(12, 14), Interval(78, 84),
         Interval(29, 39), Interval(17, 21), Interval(63, 71), Interval(3, 3), Interval(58, 76)],
        # Job 10
        [Interval(54, 72), Interval(49, 63), Interval(77, 77), Interval(15, 19), Interval(16, 18),
         Interval(45, 57), Interval(3, 3), Interval(9, 9), Interval(6, 8), Interval(56, 70),
         Interval(84, 90), Interval(61, 71), Interval(85, 99), Interval(56, 72), Interval(59, 61)],
        # Job 11
        [Interval(29, 37), Interval(83, 89), Interval(31, 39), Interval(64, 74), Interval(29, 35),
         Interval(77, 95), Interval(23, 29), Interval(91, 105), Interval(90, 100), Interval(30, 32),
         Interval(10, 12), Interval(76, 88), Interval(81, 89), Interval(71, 71), Interval(52, 70)],
        # Job 12
        [Interval(76, 86), Interval(81, 91), Interval(1, 1), Interval(18, 18), Interval(16, 16),
         Interval(91, 97), Interval(84, 84), Interval(11, 11), Interval(17, 19), Interval(37, 45),
         Interval(68, 76), Interval(13, 17), Interval(50, 50), Interval(69, 89), Interval(71, 83)],
        # Job 13
        [Interval(67, 67), Interval(35, 47), Interval(92, 106), Interval(25, 33), Interval(54, 70),
         Interval(69, 91), Interval(35, 43), Interval(1, 1), Interval(20, 22), Interval(33, 43),
         Interval(63, 73), Interval(82, 94), Interval(80, 96), Interval(87, 103), Interval(2, 2)],
        # Job 14
        [Interval(65, 87), Interval(71, 89), Interval(40, 44), Interval(62, 68), Interval(4, 4),
         Interval(56, 68), Interval(48, 52), Interval(88, 98), Interval(69, 79), Interval(71, 81),
         Interval(9, 11), Interval(73, 79), Interval(55, 55), Interval(81, 109), Interval(83, 105)],
        # Job 15
        [Interval(66, 86), Interval(36, 44), Interval(86, 106), Interval(76, 102), Interval(22, 22),
         Interval(1, 1), Interval(19, 25), Interval(43, 55), Interval(11, 13), Interval(27, 27),
         Interval(16, 18), Interval(31, 37), Interval(43, 53), Interval(26, 30), Interval(29, 35)],
        # Job 16
        [Interval(90, 90), Interval(44, 56), Interval(30, 36), Interval(48, 58), Interval(20, 22),
         Interval(35, 35), Interval(11, 11), Interval(49, 57), Interval(40, 48), Interval(51, 65),
         Interval(71, 81), Interval(32, 32), Interval(57, 67), Interval(52, 68), Interval(20, 26)],
        # Job 17
        [Interval(89, 103), Interval(12, 16), Interval(67, 67), Interval(32, 42), Interval(7, 7),
         Interval(20, 26), Interval(75, 77), Interval(71, 93), Interval(46, 56), Interval(63, 73),
         Interval(51, 65), Interval(63, 69), Interval(13, 13), Interval(34, 46), Interval(42, 44)],
        # Job 18
        [Interval(31, 33), Interval(85, 105), Interval(61, 79), Interval(24, 30), Interval(79, 79),
         Interval(35, 39), Interval(88, 108), Interval(83, 89), Interval(84, 86), Interval(51, 55),
         Interval(22, 28), Interval(81, 95), Interval(28, 36), Interval(27, 35), Interval(23, 29)],
        # Job 19
        [Interval(18, 18), Interval(31, 31), Interval(94, 100), Interval(91, 97), Interval(71, 77),
         Interval(67, 79), Interval(35, 45), Interval(33, 35), Interval(82, 94), Interval(50, 54),
         Interval(41, 55), Interval(62, 82), Interval(45, 55), Interval(20, 20), Interval(6, 6)],
        # Job 20
        [Interval(81, 89), Interval(90, 90), Interval(80, 94), Interval(55, 59), Interval(87, 87),
         Interval(10, 12), Interval(91, 101), Interval(62, 76), Interval(70, 84), Interval(82, 108),
         Interval(56, 64), Interval(33, 41), Interval(76, 98), Interval(75, 91), Interval(34, 46)],
        # Job 21
        [Interval(74, 78), Interval(1, 1), Interval(44, 48), Interval(28, 34), Interval(21, 21),
         Interval(55, 59), Interval(61, 77), Interval(91, 101), Interval(81, 89), Interval(34, 46),
         Interval(26, 34), Interval(4, 4), Interval(59, 63), Interval(43, 45), Interval(27, 31)],
        # Job 22
        [Interval(30, 36), Interval(47, 49), Interval(71, 71), Interval(27, 27), Interval(60, 74),
         Interval(11, 11), Interval(20, 26), Interval(97, 97), Interval(63, 79), Interval(23, 23),
         Interval(46, 62), Interval(83, 99), Interval(52, 58), Interval(11, 13), Interval(62, 62)],
        # Job 23
        [Interval(61, 69), Interval(17, 21), Interval(6, 6), Interval(44, 46), Interval(82, 106),
         Interval(4, 4), Interval(44, 48), Interval(51, 53), Interval(92, 94), Interval(13, 15),
         Interval(47, 51), Interval(65, 75), Interval(1, 1), Interval(3, 3), Interval(20, 26)],
        # Job 24
        [Interval(13, 15), Interval(3, 3), Interval(32, 36), Interval(13, 13), Interval(44, 48),
         Interval(68, 90), Interval(81, 83), Interval(75, 77), Interval(12, 16), Interval(6, 6),
         Interval(26, 28), Interval(32, 36), Interval(56, 74), Interval(44, 58), Interval(75, 95)],
        # Job 25
        [Interval(8, 8), Interval(35, 47), Interval(63, 85), Interval(8, 10), Interval(41, 43),
         Interval(98, 98), Interval(64, 66), Interval(89, 99), Interval(21, 27), Interval(73, 93),
         Interval(18, 24), Interval(69, 81), Interval(23, 29), Interval(26, 34), Interval(66, 68)],
        # Job 26
        [Interval(78, 94), Interval(96, 96), Interval(51, 69), Interval(6, 6), Interval(76, 80),
         Interval(83, 91), Interval(5, 5), Interval(23, 29), Interval(41, 55), Interval(80, 82),
         Interval(55, 73), Interval(20, 20), Interval(38, 50), Interval(91, 91), Interval(12, 12)],
        # Job 27
        [Interval(65, 85), Interval(21, 27), Interval(27, 27), Interval(12, 16), Interval(31, 35),
         Interval(15, 19), Interval(82, 104), Interval(5, 5), Interval(5, 5), Interval(85, 93),
         Interval(51, 55), Interval(63, 69), Interval(76, 94), Interval(48, 54), Interval(82, 110)],
        # Job 28
        [Interval(31, 31), Interval(63, 63), Interval(19, 23), Interval(34, 40), Interval(59, 77),
         Interval(76, 80), Interval(48, 48), Interval(58, 74), Interval(85, 87), Interval(18, 18),
         Interval(68, 86), Interval(22, 22), Interval(27, 35), Interval(87, 87), Interval(18, 18)],
        # Job 29
        [Interval(21, 25), Interval(23, 27), Interval(21, 23), Interval(35, 45), Interval(5, 5),
         Interval(8, 10), Interval(29, 29), Interval(50, 52), Interval(57, 65), Interval(84, 84),
         Interval(47, 53), Interval(4, 4), Interval(76, 98), Interval(35, 37), Interval(29, 33)],
        # Job 30
        [Interval(14, 18), Interval(70, 92), Interval(16, 20), Interval(69, 77), Interval(26, 26),
         Interval(18, 20), Interval(54, 54), Interval(44, 44), Interval(92, 92), Interval(7, 9),
         Interval(6, 6), Interval(77, 101), Interval(2, 2), Interval(44, 48), Interval(18, 24)],
        # Job 31
        [Interval(56, 58), Interval(48, 48), Interval(31, 31), Interval(51, 63), Interval(11, 11),
         Interval(70, 88), Interval(64, 72), Interval(92, 106), Interval(44, 44), Interval(63, 79),
         Interval(51, 67), Interval(12, 14), Interval(10, 10), Interval(42, 54), Interval(28, 36)],
        # Job 32
        [Interval(42, 42), Interval(32, 36), Interval(83, 103), Interval(62, 64), Interval(13, 13),
         Interval(33, 43), Interval(80, 106), Interval(29, 39), Interval(57, 75), Interval(53, 71),
         Interval(35, 43), Interval(68, 68), Interval(41, 45), Interval(67, 77), Interval(32, 42)],
        # Job 33
        [Interval(74, 98), Interval(11, 11), Interval(30, 36), Interval(81, 89), Interval(9, 9),
         Interval(29, 37), Interval(68, 92), Interval(84, 100), Interval(52, 66), Interval(21, 21),
         Interval(64, 66), Interval(17, 21), Interval(87, 105), Interval(15, 19), Interval(31, 35)],
        # Job 34
        [Interval(43, 45), Interval(39, 47), Interval(77, 79), Interval(35, 37), Interval(8, 8),
         Interval(11, 13), Interval(4, 4), Interval(7, 9), Interval(2, 2), Interval(72, 84),
         Interval(38, 48), Interval(23, 31), Interval(9, 9), Interval(14, 18), Interval(16, 18)],
        # Job 35
        [Interval(79, 83), Interval(28, 36), Interval(34, 42), Interval(75, 91), Interval(28, 36),
         Interval(67, 81), Interval(76, 76), Interval(6, 6), Interval(15, 19), Interval(27, 29),
         Interval(73, 79), Interval(59, 73), Interval(18, 20), Interval(26, 28), Interval(70, 84)],
        # Job 36
        [Interval(42, 56), Interval(73, 75), Interval(33, 37), Interval(10, 12), Interval(78, 84),
         Interval(71, 73), Interval(76, 76), Interval(46, 52), Interval(65, 69), Interval(25, 33),
         Interval(50, 54), Interval(29, 37), Interval(71, 73), Interval(49, 59), Interval(17, 21)],
        # Job 37
        [Interval(86, 106), Interval(71, 75), Interval(34, 44), Interval(62, 76), Interval(40, 44),
         Interval(76, 78), Interval(83, 107), Interval(5, 5), Interval(33, 41), Interval(53, 59),
         Interval(19, 23), Interval(58, 72), Interval(5, 5), Interval(40, 40), Interval(8, 8)],
        # Job 38
        [Interval(11, 11), Interval(38, 50), Interval(32, 32), Interval(38, 48), Interval(9, 11),
         Interval(5, 5), Interval(56, 68), Interval(14, 16), Interval(82, 102), Interval(77, 81),
         Interval(29, 31), Interval(29, 29), Interval(21, 21), Interval(56, 60), Interval(29, 29)],
        # Job 39
        [Interval(20, 24), Interval(77, 89), Interval(47, 63), Interval(83, 107), Interval(38, 46),
         Interval(41, 43), Interval(57, 67), Interval(12, 12), Interval(79, 85), Interval(45, 59),
         Interval(39, 43), Interval(37, 43), Interval(84, 88), Interval(27, 29), Interval(42, 54)],
        # Job 40
        [Interval(60, 68), Interval(61, 75), Interval(13, 15), Interval(62, 78), Interval(62, 64),
         Interval(32, 34), Interval(74, 90), Interval(55, 55), Interval(15, 19), Interval(47, 55),
         Interval(94, 98), Interval(23, 31), Interval(69, 89), Interval(57, 69), Interval(25, 31)],
        # Job 41
        [Interval(87, 91), Interval(68, 92), Interval(85, 111), Interval(47, 61), Interval(71, 79),
         Interval(84, 110), Interval(37, 43), Interval(59, 65), Interval(95, 101), Interval(38, 38),
         Interval(63, 77), Interval(36, 42), Interval(22, 24), Interval(11, 13), Interval(87, 101)],
        # Job 42
        [Interval(21, 21), Interval(7, 9), Interval(79, 81), Interval(2, 2), Interval(65, 67),
         Interval(32, 34), Interval(22, 22), Interval(19, 23), Interval(65, 75), Interval(14, 14),
         Interval(30, 34), Interval(64, 76), Interval(78, 78), Interval(43, 49), Interval(34, 42)],
        # Job 43
        [Interval(16, 18), Interval(22, 22), Interval(57, 57), Interval(58, 62), Interval(65, 71),
         Interval(75, 97), Interval(31, 31), Interval(15, 17), Interval(66, 84), Interval(58, 72),
         Interval(45, 47), Interval(48, 64), Interval(72, 78), Interval(89, 109), Interval(6, 6)],
        # Job 44
        [Interval(4, 4), Interval(67, 83), Interval(8, 8), Interval(35, 35), Interval(62, 72),
         Interval(77, 99), Interval(40, 40), Interval(83, 97), Interval(8, 10), Interval(94, 104),
         Interval(80, 106), Interval(39, 39), Interval(51, 67), Interval(77, 103), Interval(62, 76)],
        # Job 45
        [Interval(31, 37), Interval(57, 65), Interval(77, 99), Interval(54, 54), Interval(88, 102),
         Interval(21, 23), Interval(42, 52), Interval(81, 101), Interval(52, 54), Interval(6, 8),
         Interval(81, 107), Interval(13, 15), Interval(60, 80), Interval(34, 46), Interval(31, 31)],
        # Job 46
        [Interval(26, 30), Interval(84, 96), Interval(5, 5), Interval(76, 94), Interval(75, 91),
         Interval(6, 6), Interval(64, 74), Interval(6, 6), Interval(57, 57), Interval(79, 95),
         Interval(80, 106), Interval(69, 81), Interval(70, 70), Interval(75, 97), Interval(61, 75)],
        # Job 47
        [Interval(23, 27), Interval(40, 48), Interval(50, 58), Interval(86, 102), Interval(32, 38),
         Interval(58, 66), Interval(58, 68), Interval(49, 53), Interval(52, 66), Interval(68, 68),
         Interval(73, 97), Interval(47, 49), Interval(63, 65), Interval(38, 42), Interval(72, 78)],
        # Job 48
        [Interval(28, 30), Interval(42, 42), Interval(50, 62), Interval(87, 101), Interval(8, 10),
         Interval(30, 32), Interval(76, 84), Interval(52, 52), Interval(50, 56), Interval(79, 85),
         Interval(8, 8), Interval(32, 32), Interval(80, 108), Interval(82, 106), Interval(31, 33)],
        # Job 49
        [Interval(37, 41), Interval(12, 12), Interval(30, 38), Interval(22, 26), Interval(36, 46),
         Interval(85, 85), Interval(69, 79), Interval(42, 50), Interval(30, 30), Interval(81, 97),
         Interval(2, 2), Interval(85, 89), Interval(53, 61), Interval(72, 96), Interval(34, 34)],
    ],
    'name': 'INT__TAI50_15_10.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai50_15_10_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI50_15_10.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI50_15_10.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI50_15_10_F_15_01_INTERVAL_DATA
