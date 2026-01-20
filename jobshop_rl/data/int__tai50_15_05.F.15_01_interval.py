"""
Problema INT__TAI50_15_05.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI50_15_05_F_15_01_INTERVAL_DATA = {
    'num_jobs': 50,
    'num_machines': 15,
    'problem_id': 'int__tai50_15_05.F.15_01_interval',
    'sequences': [
        [5, 0, 2, 14, 12, 4, 7, 13, 1, 10, 11, 6, 9, 3, 8],
        [7, 2, 1, 8, 12, 9, 3, 11, 13, 14, 0, 6, 4, 10, 5],
        [4, 6, 5, 13, 0, 7, 14, 11, 9, 10, 12, 3, 8, 1, 2],
        [9, 13, 3, 11, 14, 12, 6, 1, 0, 4, 10, 5, 2, 7, 8],
        [11, 8, 1, 9, 2, 5, 6, 12, 7, 13, 3, 10, 0, 14, 4],
        [9, 3, 4, 7, 11, 2, 13, 5, 8, 12, 6, 10, 14, 0, 1],
        [1, 2, 3, 5, 13, 10, 6, 0, 8, 4, 12, 11, 7, 9, 14],
        [1, 14, 10, 12, 4, 8, 7, 13, 6, 2, 9, 3, 5, 11, 0],
        [6, 13, 2, 4, 12, 14, 3, 5, 10, 9, 11, 0, 1, 7, 8],
        [11, 13, 0, 10, 6, 9, 1, 2, 14, 3, 5, 8, 7, 4, 12],
        [9, 10, 5, 12, 7, 0, 14, 6, 1, 2, 11, 4, 8, 13, 3],
        [12, 5, 1, 13, 2, 8, 6, 4, 7, 10, 0, 3, 14, 11, 9],
        [4, 1, 8, 10, 5, 12, 6, 13, 7, 3, 9, 0, 14, 2, 11],
        [13, 12, 2, 5, 11, 7, 9, 14, 6, 0, 8, 10, 1, 3, 4],
        [11, 7, 14, 2, 12, 6, 4, 0, 9, 10, 1, 13, 5, 3, 8],
        [14, 5, 9, 11, 3, 0, 12, 1, 4, 6, 10, 8, 7, 13, 2],
        [0, 9, 2, 5, 13, 4, 1, 14, 6, 3, 10, 12, 8, 7, 11],
        [11, 6, 0, 5, 10, 12, 2, 14, 13, 1, 7, 8, 9, 3, 4],
        [7, 10, 4, 0, 12, 14, 11, 9, 5, 3, 2, 13, 1, 8, 6],
        [4, 9, 12, 10, 14, 3, 7, 11, 2, 0, 8, 1, 6, 13, 5],
        [3, 10, 14, 5, 6, 7, 1, 2, 4, 13, 12, 9, 8, 11, 0],
        [10, 12, 13, 2, 1, 0, 5, 6, 11, 8, 9, 3, 7, 14, 4],
        [5, 2, 0, 13, 1, 6, 4, 9, 8, 11, 10, 3, 14, 7, 12],
        [11, 4, 6, 10, 12, 8, 2, 7, 9, 14, 1, 0, 13, 3, 5],
        [11, 14, 9, 13, 2, 0, 4, 1, 8, 10, 12, 6, 5, 7, 3],
        [14, 0, 8, 1, 11, 12, 13, 2, 9, 4, 7, 6, 3, 10, 5],
        [3, 1, 12, 11, 4, 7, 6, 10, 9, 2, 13, 5, 14, 8, 0],
        [12, 14, 10, 0, 5, 13, 1, 11, 4, 3, 6, 8, 2, 9, 7],
        [4, 10, 13, 6, 0, 11, 7, 9, 14, 12, 8, 1, 3, 2, 5],
        [3, 5, 2, 9, 13, 11, 12, 6, 10, 4, 8, 0, 14, 1, 7],
        [1, 6, 7, 5, 11, 3, 12, 9, 2, 10, 13, 4, 14, 0, 8],
        [5, 4, 10, 9, 0, 6, 3, 1, 7, 13, 12, 11, 14, 8, 2],
        [11, 13, 6, 5, 1, 8, 14, 0, 3, 12, 4, 9, 7, 10, 2],
        [11, 9, 2, 1, 12, 0, 8, 13, 10, 5, 14, 6, 4, 7, 3],
        [12, 8, 6, 4, 14, 13, 0, 9, 1, 3, 7, 5, 10, 11, 2],
        [0, 4, 12, 6, 14, 10, 5, 7, 3, 13, 1, 2, 9, 8, 11],
        [6, 11, 13, 5, 2, 12, 0, 4, 1, 10, 8, 3, 7, 9, 14],
        [5, 6, 11, 0, 2, 12, 4, 8, 7, 9, 13, 10, 14, 3, 1],
        [2, 6, 13, 7, 5, 0, 9, 4, 14, 10, 1, 12, 8, 11, 3],
        [7, 2, 8, 9, 0, 6, 4, 1, 11, 14, 10, 3, 5, 13, 12],
        [7, 11, 14, 12, 4, 13, 5, 8, 2, 10, 3, 9, 1, 6, 0],
        [9, 7, 12, 4, 10, 1, 8, 13, 14, 3, 0, 2, 11, 6, 5],
        [8, 14, 9, 10, 7, 6, 4, 12, 1, 2, 11, 0, 3, 5, 13],
        [14, 7, 9, 5, 10, 6, 4, 12, 2, 13, 8, 0, 1, 11, 3],
        [14, 8, 13, 4, 9, 7, 10, 0, 12, 1, 5, 2, 3, 6, 11],
        [8, 11, 1, 4, 9, 14, 0, 3, 5, 12, 10, 7, 6, 2, 13],
        [10, 11, 13, 3, 9, 4, 2, 12, 6, 14, 5, 8, 1, 7, 0],
        [14, 12, 6, 10, 4, 1, 13, 11, 2, 5, 7, 8, 3, 0, 9],
        [0, 14, 9, 1, 4, 11, 3, 13, 6, 2, 10, 8, 12, 7, 5],
        [11, 3, 0, 13, 8, 14, 2, 7, 10, 12, 5, 6, 9, 4, 1],
    ],
    'durations': [
        # Job 0
        [Interval(22, 28), Interval(10, 10), Interval(35, 45), Interval(44, 56), Interval(43, 47),
         Interval(88, 94), Interval(6, 6), Interval(34, 46), Interval(17, 21), Interval(85, 91),
         Interval(82, 92), Interval(60, 74), Interval(30, 38), Interval(1, 1), Interval(23, 29)],
        # Job 1
        [Interval(49, 57), Interval(79, 87), Interval(45, 59), Interval(82, 102), Interval(90, 94),
         Interval(7, 9), Interval(67, 83), Interval(49, 63), Interval(35, 45), Interval(7, 7),
         Interval(18, 22), Interval(72, 96), Interval(55, 73), Interval(6, 8), Interval(22, 24)],
        # Job 2
        [Interval(98, 100), Interval(46, 56), Interval(83, 89), Interval(48, 58), Interval(74, 98),
         Interval(29, 31), Interval(86, 88), Interval(8, 8), Interval(51, 55), Interval(35, 43),
         Interval(21, 23), Interval(51, 59), Interval(60, 68), Interval(28, 36), Interval(62, 66)],
        # Job 3
        [Interval(58, 78), Interval(18, 20), Interval(12, 14), Interval(10, 10), Interval(56, 72),
         Interval(45, 55), Interval(4, 4), Interval(28, 28), Interval(66, 72), Interval(64, 72),
         Interval(37, 37), Interval(69, 87), Interval(40, 42), Interval(51, 51), Interval(31, 37)],
        # Job 4
        [Interval(21, 25), Interval(49, 51), Interval(22, 28), Interval(37, 37), Interval(89, 97),
         Interval(65, 83), Interval(40, 54), Interval(44, 56), Interval(38, 42), Interval(70, 94),
         Interval(25, 33), Interval(83, 99), Interval(74, 84), Interval(34, 46), Interval(18, 20)],
        # Job 5
        [Interval(67, 87), Interval(18, 20), Interval(42, 46), Interval(71, 87), Interval(76, 82),
         Interval(31, 35), Interval(11, 13), Interval(11, 13), Interval(14, 16), Interval(29, 35),
         Interval(55, 73), Interval(23, 29), Interval(88, 92), Interval(47, 51), Interval(66, 68)],
        # Job 6
        [Interval(27, 29), Interval(81, 87), Interval(84, 106), Interval(27, 29), Interval(83, 103),
         Interval(58, 76), Interval(75, 75), Interval(7, 9), Interval(52, 60), Interval(75, 83),
         Interval(24, 30), Interval(18, 18), Interval(45, 45), Interval(20, 20), Interval(42, 46)],
        # Job 7
        [Interval(2, 2), Interval(51, 69), Interval(12, 12), Interval(30, 40), Interval(40, 50),
         Interval(39, 41), Interval(21, 27), Interval(79, 101), Interval(1, 1), Interval(18, 24),
         Interval(73, 77), Interval(75, 83), Interval(86, 96), Interval(30, 34), Interval(39, 43)],
        # Job 8
        [Interval(57, 65), Interval(27, 33), Interval(76, 86), Interval(67, 73), Interval(70, 94),
         Interval(24, 26), Interval(8, 10), Interval(27, 31), Interval(26, 28), Interval(27, 31),
         Interval(62, 74), Interval(58, 70), Interval(22, 24), Interval(47, 55), Interval(47, 55)],
        # Job 9
        [Interval(83, 91), Interval(91, 97), Interval(78, 104), Interval(12, 16), Interval(15, 15),
         Interval(37, 39), Interval(80, 92), Interval(16, 16), Interval(39, 49), Interval(54, 72),
         Interval(58, 66), Interval(75, 99), Interval(66, 88), Interval(28, 34), Interval(19, 19)],
        # Job 10
        [Interval(55, 73), Interval(76, 84), Interval(82, 102), Interval(99, 99), Interval(1, 1),
         Interval(26, 34), Interval(18, 24), Interval(74, 78), Interval(60, 70), Interval(12, 14),
         Interval(31, 41), Interval(2, 2), Interval(76, 78), Interval(12, 14), Interval(66, 70)],
        # Job 11
        [Interval(25, 31), Interval(49, 57), Interval(58, 70), Interval(22, 26), Interval(44, 58),
         Interval(76, 88), Interval(94, 104), Interval(20, 22), Interval(62, 74), Interval(38, 44),
         Interval(13, 15), Interval(9, 9), Interval(78, 104), Interval(54, 60), Interval(5, 5)],
        # Job 12
        [Interval(48, 54), Interval(91, 95), Interval(76, 78), Interval(59, 63), Interval(22, 22),
         Interval(73, 81), Interval(52, 58), Interval(88, 104), Interval(72, 80), Interval(24, 30),
         Interval(12, 12), Interval(54, 72), Interval(77, 91), Interval(46, 46), Interval(12, 16)],
        # Job 13
        [Interval(48, 54), Interval(30, 40), Interval(56, 72), Interval(69, 89), Interval(13, 17),
         Interval(76, 88), Interval(51, 65), Interval(67, 77), Interval(56, 64), Interval(91, 107),
         Interval(43, 51), Interval(38, 50), Interval(17, 21), Interval(94, 104), Interval(82, 90)],
        # Job 14
        [Interval(44, 54), Interval(20, 22), Interval(35, 39), Interval(23, 25), Interval(89, 103),
         Interval(30, 34), Interval(90, 98), Interval(37, 37), Interval(24, 32), Interval(27, 33),
         Interval(36, 46), Interval(60, 72), Interval(11, 13), Interval(67, 89), Interval(81, 83)],
        # Job 15
        [Interval(23, 31), Interval(55, 71), Interval(31, 39), Interval(52, 52), Interval(65, 77),
         Interval(56, 68), Interval(18, 22), Interval(15, 17), Interval(57, 71), Interval(80, 80),
         Interval(50, 64), Interval(31, 37), Interval(66, 82), Interval(13, 13), Interval(79, 81)],
        # Job 16
        [Interval(69, 75), Interval(89, 107), Interval(46, 54), Interval(39, 51), Interval(69, 77),
         Interval(80, 84), Interval(3, 3), Interval(49, 57), Interval(4, 4), Interval(76, 96),
         Interval(46, 62), Interval(71, 81), Interval(47, 63), Interval(38, 38), Interval(46, 60)],
        # Job 17
        [Interval(22, 22), Interval(26, 34), Interval(17, 17), Interval(46, 60), Interval(45, 55),
         Interval(79, 93), Interval(16, 20), Interval(1, 1), Interval(34, 36), Interval(93, 93),
         Interval(77, 103), Interval(5, 5), Interval(85, 91), Interval(11, 11), Interval(58, 72)],
        # Job 18
        [Interval(24, 32), Interval(4, 4), Interval(10, 12), Interval(87, 87), Interval(58, 66),
         Interval(53, 65), Interval(35, 37), Interval(57, 57), Interval(33, 35), Interval(5, 5),
         Interval(66, 86), Interval(76, 90), Interval(80, 102), Interval(41, 51), Interval(55, 73)],
        # Job 19
        [Interval(67, 67), Interval(20, 20), Interval(92, 98), Interval(50, 54), Interval(36, 38),
         Interval(80, 96), Interval(59, 73), Interval(83, 91), Interval(72, 82), Interval(37, 39),
         Interval(48, 64), Interval(67, 89), Interval(49, 61), Interval(28, 28), Interval(52, 58)],
        # Job 20
        [Interval(6, 6), Interval(19, 19), Interval(60, 70), Interval(5, 5), Interval(65, 71),
         Interval(26, 26), Interval(81, 105), Interval(44, 48), Interval(44, 54), Interval(21, 25),
         Interval(71, 95), Interval(57, 65), Interval(77, 99), Interval(59, 77), Interval(56, 68)],
        # Job 21
        [Interval(45, 59), Interval(25, 25), Interval(32, 34), Interval(13, 15), Interval(28, 30),
         Interval(59, 63), Interval(15, 19), Interval(78, 86), Interval(19, 19), Interval(32, 42),
         Interval(67, 87), Interval(40, 42), Interval(46, 48), Interval(42, 48), Interval(47, 55)],
        # Job 22
        [Interval(66, 70), Interval(23, 23), Interval(18, 18), Interval(59, 71), Interval(87, 91),
         Interval(9, 11), Interval(98, 98), Interval(54, 68), Interval(37, 39), Interval(55, 73),
         Interval(83, 99), Interval(34, 38), Interval(57, 75), Interval(32, 32), Interval(23, 25)],
        # Job 23
        [Interval(75, 97), Interval(87, 93), Interval(39, 49), Interval(57, 63), Interval(22, 22),
         Interval(82, 84), Interval(88, 100), Interval(13, 15), Interval(74, 86), Interval(40, 52),
         Interval(19, 21), Interval(13, 13), Interval(37, 41), Interval(63, 71), Interval(15, 19)],
        # Job 24
        [Interval(4, 4), Interval(21, 21), Interval(58, 60), Interval(44, 56), Interval(71, 79),
         Interval(39, 43), Interval(68, 90), Interval(31, 41), Interval(47, 61), Interval(71, 73),
         Interval(80, 108), Interval(40, 52), Interval(17, 19), Interval(78, 84), Interval(45, 45)],
        # Job 25
        [Interval(76, 78), Interval(92, 102), Interval(52, 70), Interval(53, 69), Interval(80, 106),
         Interval(89, 105), Interval(75, 97), Interval(13, 17), Interval(72, 74), Interval(25, 31),
         Interval(1, 1), Interval(80, 80), Interval(76, 102), Interval(51, 53), Interval(29, 31)],
        # Job 26
        [Interval(13, 17), Interval(23, 31), Interval(35, 35), Interval(40, 54), Interval(79, 79),
         Interval(23, 29), Interval(72, 72), Interval(87, 91), Interval(30, 40), Interval(45, 59),
         Interval(17, 17), Interval(79, 105), Interval(5, 5), Interval(19, 21), Interval(43, 55)],
        # Job 27
        [Interval(3, 3), Interval(82, 104), Interval(54, 58), Interval(79, 85), Interval(56, 60),
         Interval(58, 72), Interval(77, 87), Interval(5, 5), Interval(5, 5), Interval(79, 105),
         Interval(30, 30), Interval(35, 35), Interval(16, 18), Interval(4, 4), Interval(72, 84)],
        # Job 28
        [Interval(26, 34), Interval(54, 56), Interval(85, 85), Interval(44, 56), Interval(29, 29),
         Interval(74, 80), Interval(59, 75), Interval(55, 55), Interval(39, 51), Interval(6, 6),
         Interval(48, 48), Interval(46, 46), Interval(8, 10), Interval(28, 34), Interval(39, 43)],
        # Job 29
        [Interval(21, 25), Interval(59, 75), Interval(33, 33), Interval(26, 28), Interval(74, 82),
         Interval(64, 64), Interval(5, 5), Interval(15, 17), Interval(6, 6), Interval(39, 49),
         Interval(42, 44), Interval(45, 53), Interval(11, 13), Interval(15, 19), Interval(74, 96)],
        # Job 30
        [Interval(47, 53), Interval(55, 57), Interval(73, 87), Interval(54, 54), Interval(8, 8),
         Interval(70, 70), Interval(71, 95), Interval(16, 20), Interval(29, 33), Interval(4, 4),
         Interval(79, 101), Interval(86, 88), Interval(1, 1), Interval(5, 5), Interval(60, 62)],
        # Job 31
        [Interval(22, 22), Interval(13, 17), Interval(4, 4), Interval(40, 40), Interval(60, 78),
         Interval(92, 104), Interval(41, 47), Interval(77, 77), Interval(21, 25), Interval(12, 16),
         Interval(88, 104), Interval(90, 90), Interval(80, 100), Interval(67, 89), Interval(71, 71)],
        # Job 32
        [Interval(88, 100), Interval(27, 33), Interval(50, 52), Interval(85, 87), Interval(59, 79),
         Interval(45, 59), Interval(10, 12), Interval(25, 33), Interval(32, 42), Interval(62, 78),
         Interval(34, 34), Interval(13, 13), Interval(10, 10), Interval(53, 69), Interval(41, 55)],
        # Job 33
        [Interval(7, 7), Interval(65, 83), Interval(14, 14), Interval(63, 67), Interval(17, 21),
         Interval(15, 19), Interval(4, 4), Interval(5, 5), Interval(24, 30), Interval(81, 105),
         Interval(88, 94), Interval(9, 9), Interval(59, 79), Interval(32, 38), Interval(5, 5)],
        # Job 34
        [Interval(35, 45), Interval(83, 95), Interval(71, 75), Interval(83, 101), Interval(58, 58),
         Interval(67, 69), Interval(94, 100), Interval(80, 108), Interval(71, 83), Interval(40, 46),
         Interval(46, 58), Interval(7, 9), Interval(39, 43), Interval(18, 24), Interval(52, 60)],
        # Job 35
        [Interval(69, 73), Interval(37, 49), Interval(10, 12), Interval(59, 71), Interval(10, 12),
         Interval(14, 16), Interval(46, 46), Interval(68, 88), Interval(3, 3), Interval(26, 28),
         Interval(32, 34), Interval(77, 97), Interval(92, 102), Interval(56, 62), Interval(34, 40)],
        # Job 36
        [Interval(58, 78), Interval(95, 97), Interval(28, 32), Interval(75, 93), Interval(2, 2),
         Interval(78, 84), Interval(56, 58), Interval(7, 7), Interval(65, 75), Interval(38, 40),
         Interval(54, 70), Interval(90, 98), Interval(82, 110), Interval(38, 38), Interval(42, 50)],
        # Job 37
        [Interval(82, 110), Interval(30, 38), Interval(69, 73), Interval(76, 100), Interval(9, 11),
         Interval(95, 103), Interval(47, 49), Interval(50, 64), Interval(28, 34), Interval(88, 98),
         Interval(30, 36), Interval(75, 93), Interval(28, 28), Interval(30, 34), Interval(68, 76)],
        # Job 38
        [Interval(82, 110), Interval(15, 15), Interval(28, 34), Interval(83, 103), Interval(19, 23),
         Interval(36, 44), Interval(89, 109), Interval(58, 62), Interval(60, 66), Interval(95, 95),
         Interval(44, 46), Interval(32, 34), Interval(81, 85), Interval(10, 12), Interval(70, 80)],
        # Job 39
        [Interval(40, 54), Interval(62, 80), Interval(34, 40), Interval(58, 60), Interval(67, 77),
         Interval(61, 67), Interval(59, 63), Interval(45, 59), Interval(19, 21), Interval(13, 13),
         Interval(11, 11), Interval(25, 27), Interval(25, 31), Interval(85, 97), Interval(24, 30)],
        # Job 40
        [Interval(29, 33), Interval(67, 85), Interval(4, 4), Interval(35, 35), Interval(18, 18),
         Interval(45, 55), Interval(16, 16), Interval(46, 58), Interval(78, 92), Interval(43, 43),
         Interval(38, 50), Interval(18, 24), Interval(66, 78), Interval(22, 26), Interval(12, 12)],
        # Job 41
        [Interval(61, 81), Interval(26, 34), Interval(51, 65), Interval(68, 74), Interval(75, 99),
         Interval(68, 80), Interval(32, 34), Interval(26, 26), Interval(3, 3), Interval(75, 75),
         Interval(78, 96), Interval(13, 15), Interval(32, 34), Interval(47, 57), Interval(35, 41)],
        # Job 42
        [Interval(42, 42), Interval(35, 43), Interval(8, 8), Interval(26, 26), Interval(25, 27),
         Interval(9, 9), Interval(1, 1), Interval(75, 91), Interval(79, 91), Interval(11, 11),
         Interval(75, 87), Interval(66, 78), Interval(86, 88), Interval(38, 44), Interval(40, 48)],
        # Job 43
        [Interval(66, 80), Interval(58, 60), Interval(4, 4), Interval(25, 25), Interval(66, 70),
         Interval(3, 3), Interval(69, 75), Interval(60, 78), Interval(49, 51), Interval(57, 67),
         Interval(19, 25), Interval(68, 86), Interval(1, 1), Interval(4, 4), Interval(90, 98)],
        # Job 44
        [Interval(51, 67), Interval(43, 47), Interval(35, 43), Interval(57, 71), Interval(35, 35),
         Interval(42, 42), Interval(15, 17), Interval(77, 99), Interval(9, 9), Interval(81, 95),
         Interval(74, 96), Interval(51, 57), Interval(54, 72), Interval(21, 21), Interval(65, 87)],
        # Job 45
        [Interval(57, 75), Interval(21, 25), Interval(26, 30), Interval(12, 12), Interval(19, 25),
         Interval(65, 65), Interval(8, 10), Interval(25, 29), Interval(23, 27), Interval(67, 83),
         Interval(82, 88), Interval(18, 20), Interval(35, 47), Interval(19, 21), Interval(22, 28)],
        # Job 46
        [Interval(24, 32), Interval(96, 96), Interval(34, 40), Interval(54, 62), Interval(83, 105),
         Interval(36, 44), Interval(39, 45), Interval(41, 41), Interval(18, 22), Interval(68, 92),
         Interval(27, 31), Interval(12, 12), Interval(70, 92), Interval(7, 9), Interval(25, 31)],
        # Job 47
        [Interval(76, 90), Interval(16, 18), Interval(24, 28), Interval(71, 85), Interval(88, 102),
         Interval(41, 49), Interval(15, 17), Interval(47, 59), Interval(12, 12), Interval(43, 57),
         Interval(6, 6), Interval(84, 90), Interval(44, 44), Interval(5, 5), Interval(61, 65)],
        # Job 48
        [Interval(13, 13), Interval(81, 89), Interval(49, 49), Interval(65, 81), Interval(45, 51),
         Interval(40, 48), Interval(80, 88), Interval(81, 89), Interval(1, 1), Interval(12, 12),
         Interval(3, 3), Interval(37, 41), Interval(72, 78), Interval(70, 76), Interval(44, 46)],
        # Job 49
        [Interval(3, 3), Interval(13, 17), Interval(35, 45), Interval(74, 80), Interval(41, 45),
         Interval(89, 93), Interval(46, 56), Interval(15, 19), Interval(63, 79), Interval(33, 33),
         Interval(77, 89), Interval(55, 67), Interval(67, 69), Interval(13, 15), Interval(94, 100)],
    ],
    'name': 'INT__TAI50_15_05.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai50_15_05_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI50_15_05.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI50_15_05.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI50_15_05_F_15_01_INTERVAL_DATA
