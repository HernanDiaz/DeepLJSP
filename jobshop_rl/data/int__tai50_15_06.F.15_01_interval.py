"""
Problema INT__TAI50_15_06.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI50_15_06_F_15_01_INTERVAL_DATA = {
    'num_jobs': 50,
    'num_machines': 15,
    'problem_id': 'int__tai50_15_06.F.15_01_interval',
    'sequences': [
        [7, 8, 0, 14, 11, 6, 5, 9, 13, 1, 2, 12, 4, 10, 3],
        [14, 0, 6, 10, 1, 11, 2, 9, 8, 3, 4, 5, 12, 7, 13],
        [10, 6, 3, 11, 0, 5, 4, 1, 13, 2, 12, 14, 9, 7, 8],
        [11, 14, 3, 0, 12, 9, 10, 7, 5, 6, 2, 8, 4, 13, 1],
        [5, 7, 0, 3, 10, 1, 9, 11, 8, 12, 13, 14, 2, 6, 4],
        [6, 13, 1, 7, 10, 0, 11, 8, 9, 5, 12, 14, 4, 3, 2],
        [14, 8, 3, 9, 5, 0, 1, 6, 2, 7, 12, 10, 4, 13, 11],
        [8, 13, 0, 3, 10, 1, 2, 14, 11, 7, 5, 6, 12, 9, 4],
        [6, 10, 1, 11, 5, 4, 12, 9, 2, 8, 13, 14, 7, 0, 3],
        [4, 9, 6, 10, 8, 1, 7, 14, 13, 5, 2, 11, 12, 0, 3],
        [4, 1, 3, 7, 13, 5, 8, 10, 12, 0, 6, 14, 11, 2, 9],
        [9, 7, 10, 2, 6, 12, 8, 13, 14, 5, 1, 0, 3, 11, 4],
        [3, 2, 12, 4, 11, 7, 5, 1, 14, 10, 8, 9, 13, 6, 0],
        [13, 14, 1, 3, 2, 11, 9, 8, 6, 0, 12, 10, 7, 5, 4],
        [10, 3, 2, 11, 5, 9, 0, 12, 8, 13, 4, 7, 14, 1, 6],
        [2, 13, 14, 11, 1, 5, 3, 4, 8, 12, 10, 0, 6, 9, 7],
        [6, 11, 3, 10, 4, 2, 0, 14, 7, 13, 1, 12, 9, 8, 5],
        [6, 8, 10, 14, 1, 5, 3, 0, 9, 4, 12, 11, 13, 7, 2],
        [10, 1, 2, 5, 7, 12, 13, 11, 0, 9, 3, 8, 4, 14, 6],
        [12, 4, 11, 13, 9, 8, 7, 10, 0, 2, 3, 6, 5, 14, 1],
        [11, 6, 0, 12, 14, 7, 10, 5, 2, 4, 8, 13, 3, 9, 1],
        [14, 7, 9, 1, 4, 13, 5, 0, 2, 12, 10, 11, 6, 8, 3],
        [9, 5, 1, 14, 2, 3, 0, 11, 12, 10, 4, 8, 7, 13, 6],
        [9, 10, 3, 8, 0, 5, 6, 4, 12, 2, 14, 1, 7, 13, 11],
        [14, 8, 9, 5, 11, 0, 12, 13, 4, 7, 10, 1, 6, 3, 2],
        [6, 10, 7, 13, 12, 3, 2, 11, 5, 4, 1, 0, 8, 14, 9],
        [10, 11, 9, 13, 3, 7, 6, 12, 0, 14, 1, 4, 8, 5, 2],
        [5, 7, 3, 14, 13, 10, 8, 9, 1, 12, 2, 0, 4, 11, 6],
        [9, 10, 4, 14, 8, 6, 1, 2, 11, 12, 13, 0, 3, 7, 5],
        [10, 1, 4, 2, 3, 12, 5, 0, 9, 14, 8, 7, 6, 13, 11],
        [3, 9, 11, 5, 4, 2, 14, 0, 12, 1, 10, 13, 8, 7, 6],
        [6, 2, 12, 13, 4, 0, 10, 1, 5, 9, 14, 7, 8, 11, 3],
        [0, 14, 11, 5, 6, 7, 1, 3, 4, 9, 13, 10, 8, 2, 12],
        [13, 6, 4, 11, 9, 5, 2, 12, 14, 10, 0, 3, 7, 8, 1],
        [0, 1, 13, 2, 4, 7, 12, 3, 10, 8, 11, 6, 9, 5, 14],
        [7, 2, 4, 3, 6, 9, 11, 13, 10, 8, 1, 14, 5, 12, 0],
        [1, 12, 2, 5, 0, 7, 13, 10, 14, 4, 11, 6, 9, 8, 3],
        [14, 4, 9, 12, 2, 13, 7, 1, 5, 8, 11, 0, 3, 6, 10],
        [7, 10, 2, 13, 8, 0, 9, 12, 3, 6, 11, 4, 14, 5, 1],
        [5, 14, 4, 2, 9, 0, 7, 6, 12, 3, 13, 1, 10, 8, 11],
        [1, 13, 0, 14, 2, 12, 7, 9, 8, 4, 11, 10, 5, 6, 3],
        [11, 1, 0, 7, 6, 14, 12, 2, 5, 13, 8, 10, 4, 9, 3],
        [10, 8, 11, 9, 4, 5, 0, 12, 1, 14, 13, 2, 7, 3, 6],
        [12, 13, 9, 5, 1, 6, 3, 2, 0, 11, 8, 4, 7, 10, 14],
        [14, 8, 9, 13, 11, 10, 7, 3, 4, 2, 5, 0, 6, 12, 1],
        [9, 6, 12, 10, 2, 7, 1, 4, 0, 5, 11, 3, 13, 8, 14],
        [12, 2, 1, 9, 6, 14, 5, 8, 3, 13, 11, 0, 7, 10, 4],
        [10, 2, 11, 5, 9, 0, 4, 13, 7, 8, 14, 3, 1, 6, 12],
        [6, 5, 10, 9, 4, 12, 3, 14, 0, 2, 13, 8, 7, 11, 1],
        [8, 0, 14, 6, 4, 5, 10, 12, 9, 7, 13, 3, 11, 2, 1],
    ],
    'durations': [
        # Job 0
        [Interval(29, 39), Interval(91, 91), Interval(82, 104), Interval(78, 98), Interval(57, 61),
         Interval(64, 68), Interval(44, 56), Interval(47, 59), Interval(44, 46), Interval(1, 1),
         Interval(64, 72), Interval(69, 85), Interval(33, 41), Interval(52, 70), Interval(16, 18)],
        # Job 1
        [Interval(18, 20), Interval(63, 83), Interval(13, 17), Interval(71, 73), Interval(33, 43),
         Interval(47, 57), Interval(12, 16), Interval(60, 78), Interval(19, 19), Interval(26, 32),
         Interval(3, 3), Interval(41, 55), Interval(10, 12), Interval(46, 62), Interval(27, 29)],
        # Job 2
        [Interval(59, 59), Interval(26, 32), Interval(81, 87), Interval(4, 4), Interval(17, 21),
         Interval(30, 40), Interval(21, 23), Interval(50, 50), Interval(67, 69), Interval(27, 29),
         Interval(85, 107), Interval(22, 24), Interval(68, 80), Interval(85, 95), Interval(44, 58)],
        # Job 3
        [Interval(14, 14), Interval(74, 98), Interval(7, 9), Interval(76, 94), Interval(46, 52),
         Interval(49, 63), Interval(78, 96), Interval(2, 2), Interval(84, 86), Interval(57, 63),
         Interval(91, 103), Interval(51, 51), Interval(35, 43), Interval(33, 35), Interval(88, 90)],
        # Job 4
        [Interval(91, 107), Interval(5, 5), Interval(35, 43), Interval(38, 40), Interval(3, 3),
         Interval(64, 82), Interval(16, 16), Interval(59, 65), Interval(26, 32), Interval(58, 78),
         Interval(12, 16), Interval(36, 40), Interval(77, 103), Interval(48, 64), Interval(30, 34)],
        # Job 5
        [Interval(22, 24), Interval(73, 95), Interval(32, 36), Interval(67, 87), Interval(24, 26),
         Interval(42, 46), Interval(40, 50), Interval(14, 14), Interval(74, 84), Interval(80, 100),
         Interval(68, 88), Interval(53, 59), Interval(34, 40), Interval(52, 70), Interval(84, 108)],
        # Job 6
        [Interval(24, 24), Interval(14, 16), Interval(97, 101), Interval(47, 51), Interval(63, 69),
         Interval(88, 110), Interval(83, 91), Interval(10, 12), Interval(39, 51), Interval(84, 84),
         Interval(18, 22), Interval(9, 9), Interval(67, 75), Interval(45, 55), Interval(53, 55)],
        # Job 7
        [Interval(67, 67), Interval(11, 11), Interval(92, 102), Interval(54, 72), Interval(62, 66),
         Interval(29, 37), Interval(59, 73), Interval(4, 4), Interval(87, 91), Interval(51, 69),
         Interval(45, 57), Interval(12, 14), Interval(32, 34), Interval(45, 51), Interval(66, 74)],
        # Job 8
        [Interval(52, 60), Interval(63, 69), Interval(8, 8), Interval(82, 102), Interval(76, 86),
         Interval(90, 98), Interval(5, 5), Interval(18, 24), Interval(66, 72), Interval(53, 69),
         Interval(46, 54), Interval(95, 103), Interval(45, 53), Interval(24, 28), Interval(75, 91)],
        # Job 9
        [Interval(13, 15), Interval(35, 41), Interval(75, 89), Interval(95, 103), Interval(74, 80),
         Interval(15, 19), Interval(8, 10), Interval(21, 21), Interval(15, 15), Interval(40, 46),
         Interval(38, 40), Interval(34, 44), Interval(69, 91), Interval(18, 20), Interval(37, 49)],
        # Job 10
        [Interval(65, 87), Interval(83, 105), Interval(34, 34), Interval(39, 51), Interval(7, 7),
         Interval(73, 93), Interval(88, 88), Interval(40, 54), Interval(19, 25), Interval(87, 93),
         Interval(10, 12), Interval(6, 6), Interval(20, 24), Interval(34, 46), Interval(51, 51)],
        # Job 11
        [Interval(62, 82), Interval(63, 67), Interval(2, 2), Interval(34, 42), Interval(89, 103),
         Interval(9, 11), Interval(52, 64), Interval(56, 74), Interval(16, 18), Interval(71, 79),
         Interval(62, 68), Interval(72, 86), Interval(77, 89), Interval(43, 47), Interval(52, 52)],
        # Job 12
        [Interval(20, 26), Interval(33, 37), Interval(23, 25), Interval(65, 69), Interval(65, 65),
         Interval(18, 18), Interval(7, 7), Interval(64, 72), Interval(18, 20), Interval(58, 68),
         Interval(17, 19), Interval(71, 89), Interval(19, 19), Interval(20, 26), Interval(36, 42)],
        # Job 13
        [Interval(47, 47), Interval(60, 80), Interval(36, 40), Interval(12, 16), Interval(40, 52),
         Interval(41, 55), Interval(12, 16), Interval(42, 48), Interval(27, 35), Interval(33, 37),
         Interval(88, 102), Interval(68, 82), Interval(56, 66), Interval(38, 50), Interval(63, 79)],
        # Job 14
        [Interval(25, 27), Interval(13, 15), Interval(42, 50), Interval(1, 1), Interval(22, 24),
         Interval(47, 53), Interval(25, 29), Interval(76, 88), Interval(24, 28), Interval(7, 7),
         Interval(55, 55), Interval(19, 25), Interval(18, 24), Interval(74, 96), Interval(60, 72)],
        # Job 15
        [Interval(10, 12), Interval(72, 96), Interval(48, 48), Interval(42, 56), Interval(17, 21),
         Interval(87, 109), Interval(92, 92), Interval(38, 46), Interval(61, 73), Interval(51, 63),
         Interval(36, 44), Interval(69, 87), Interval(19, 19), Interval(46, 58), Interval(13, 15)],
        # Job 16
        [Interval(11, 13), Interval(67, 75), Interval(17, 17), Interval(64, 70), Interval(18, 22),
         Interval(37, 45), Interval(64, 84), Interval(90, 102), Interval(85, 89), Interval(18, 22),
         Interval(74, 94), Interval(67, 87), Interval(67, 77), Interval(78, 104), Interval(37, 37)],
        # Job 17
        [Interval(11, 13), Interval(12, 12), Interval(58, 74), Interval(2, 2), Interval(17, 17),
         Interval(29, 37), Interval(27, 33), Interval(9, 11), Interval(64, 80), Interval(6, 6),
         Interval(6, 6), Interval(39, 43), Interval(39, 39), Interval(61, 81), Interval(4, 4)],
        # Job 18
        [Interval(3, 3), Interval(86, 92), Interval(9, 9), Interval(22, 26), Interval(70, 90),
         Interval(6, 8), Interval(42, 42), Interval(80, 90), Interval(75, 93), Interval(86, 92),
         Interval(40, 40), Interval(40, 44), Interval(80, 104), Interval(84, 98), Interval(67, 87)],
        # Job 19
        [Interval(86, 110), Interval(71, 95), Interval(65, 65), Interval(92, 96), Interval(6, 6),
         Interval(93, 99), Interval(33, 35), Interval(7, 7), Interval(45, 53), Interval(22, 28),
         Interval(45, 49), Interval(8, 8), Interval(89, 97), Interval(57, 77), Interval(43, 57)],
        # Job 20
        [Interval(47, 57), Interval(57, 57), Interval(69, 77), Interval(45, 45), Interval(51, 59),
         Interval(61, 65), Interval(99, 99), Interval(17, 23), Interval(56, 62), Interval(80, 100),
         Interval(29, 33), Interval(20, 26), Interval(93, 105), Interval(81, 103), Interval(47, 59)],
        # Job 21
        [Interval(58, 70), Interval(4, 4), Interval(22, 28), Interval(51, 53), Interval(68, 76),
         Interval(37, 45), Interval(11, 11), Interval(96, 102), Interval(31, 39), Interval(73, 81),
         Interval(85, 93), Interval(85, 111), Interval(54, 72), Interval(57, 61), Interval(96, 102)],
        # Job 22
        [Interval(73, 87), Interval(85, 101), Interval(63, 65), Interval(13, 13), Interval(48, 48),
         Interval(42, 52), Interval(77, 79), Interval(52, 66), Interval(58, 58), Interval(65, 81),
         Interval(3, 3), Interval(27, 29), Interval(12, 14), Interval(66, 78), Interval(9, 9)],
        # Job 23
        [Interval(21, 27), Interval(95, 95), Interval(87, 99), Interval(41, 55), Interval(75, 81),
         Interval(56, 72), Interval(25, 27), Interval(84, 88), Interval(82, 84), Interval(38, 44),
         Interval(59, 65), Interval(50, 56), Interval(30, 40), Interval(80, 88), Interval(43, 47)],
        # Job 24
        [Interval(86, 96), Interval(81, 91), Interval(68, 90), Interval(5, 5), Interval(84, 86),
         Interval(29, 29), Interval(65, 81), Interval(9, 9), Interval(70, 78), Interval(59, 79),
         Interval(20, 26), Interval(70, 90), Interval(80, 84), Interval(29, 39), Interval(75, 101)],
        # Job 25
        [Interval(70, 82), Interval(75, 79), Interval(2, 2), Interval(28, 28), Interval(27, 27),
         Interval(26, 28), Interval(74, 100), Interval(29, 37), Interval(35, 47), Interval(91, 107),
         Interval(2, 2), Interval(38, 50), Interval(14, 18), Interval(82, 84), Interval(83, 99)],
        # Job 26
        [Interval(96, 96), Interval(23, 31), Interval(59, 63), Interval(40, 44), Interval(87, 111),
         Interval(66, 86), Interval(86, 88), Interval(31, 41), Interval(24, 24), Interval(18, 24),
         Interval(88, 88), Interval(42, 44), Interval(77, 101), Interval(68, 88), Interval(53, 53)],
        # Job 27
        [Interval(74, 98), Interval(68, 76), Interval(3, 3), Interval(80, 102), Interval(29, 37),
         Interval(1, 1), Interval(36, 38), Interval(38, 40), Interval(29, 31), Interval(70, 86),
         Interval(49, 55), Interval(45, 59), Interval(63, 65), Interval(87, 89), Interval(69, 81)],
        # Job 28
        [Interval(90, 106), Interval(46, 58), Interval(96, 102), Interval(11, 11), Interval(50, 64),
         Interval(39, 41), Interval(50, 54), Interval(66, 84), Interval(23, 23), Interval(42, 56),
         Interval(65, 65), Interval(1, 1), Interval(57, 57), Interval(52, 60), Interval(83, 101)],
        # Job 29
        [Interval(77, 87), Interval(30, 36), Interval(70, 90), Interval(23, 23), Interval(7, 7),
         Interval(46, 52), Interval(24, 24), Interval(47, 53), Interval(25, 33), Interval(37, 39),
         Interval(43, 51), Interval(3, 3), Interval(47, 59), Interval(78, 100), Interval(61, 79)],
        # Job 30
        [Interval(31, 33), Interval(61, 63), Interval(8, 10), Interval(87, 89), Interval(58, 58),
         Interval(70, 70), Interval(8, 10), Interval(58, 74), Interval(17, 19), Interval(35, 45),
         Interval(33, 33), Interval(54, 54), Interval(60, 60), Interval(83, 101), Interval(88, 88)],
        # Job 31
        [Interval(2, 2), Interval(5, 5), Interval(31, 39), Interval(61, 69), Interval(62, 72),
         Interval(58, 58), Interval(54, 68), Interval(62, 82), Interval(55, 65), Interval(84, 84),
         Interval(78, 98), Interval(20, 26), Interval(17, 17), Interval(66, 76), Interval(12, 14)],
        # Job 32
        [Interval(64, 66), Interval(56, 56), Interval(5, 5), Interval(80, 108), Interval(70, 94),
         Interval(66, 86), Interval(25, 33), Interval(1, 1), Interval(81, 105), Interval(59, 73),
         Interval(47, 47), Interval(31, 33), Interval(39, 45), Interval(65, 85), Interval(12, 14)],
        # Job 33
        [Interval(14, 14), Interval(76, 96), Interval(62, 68), Interval(40, 42), Interval(3, 3),
         Interval(9, 11), Interval(42, 56), Interval(24, 28), Interval(9, 11), Interval(84, 88),
         Interval(1, 1), Interval(32, 32), Interval(33, 43), Interval(43, 53), Interval(82, 104)],
        # Job 34
        [Interval(92, 104), Interval(21, 21), Interval(55, 67), Interval(61, 61), Interval(53, 55),
         Interval(69, 73), Interval(84, 112), Interval(36, 42), Interval(13, 15), Interval(33, 43),
         Interval(64, 84), Interval(2, 2), Interval(12, 12), Interval(83, 103), Interval(79, 91)],
        # Job 35
        [Interval(91, 95), Interval(1, 1), Interval(23, 29), Interval(50, 64), Interval(35, 41),
         Interval(70, 90), Interval(39, 47), Interval(64, 64), Interval(20, 26), Interval(85, 91),
         Interval(71, 77), Interval(5, 5), Interval(14, 18), Interval(48, 52), Interval(1, 1)],
        # Job 36
        [Interval(22, 24), Interval(50, 60), Interval(62, 82), Interval(57, 57), Interval(44, 48),
         Interval(15, 19), Interval(77, 83), Interval(44, 44), Interval(80, 80), Interval(51, 59),
         Interval(73, 77), Interval(60, 78), Interval(33, 35), Interval(38, 50), Interval(30, 30)],
        # Job 37
        [Interval(58, 70), Interval(80, 106), Interval(49, 61), Interval(76, 80), Interval(8, 10),
         Interval(22, 26), Interval(57, 61), Interval(71, 73), Interval(26, 34), Interval(44, 56),
         Interval(76, 86), Interval(6, 8), Interval(48, 58), Interval(69, 69), Interval(3, 3)],
        # Job 38
        [Interval(59, 67), Interval(38, 42), Interval(69, 93), Interval(33, 33), Interval(46, 58),
         Interval(77, 95), Interval(2, 2), Interval(39, 47), Interval(52, 62), Interval(32, 40),
         Interval(52, 54), Interval(17, 19), Interval(22, 22), Interval(89, 95), Interval(39, 41)],
        # Job 39
        [Interval(59, 61), Interval(73, 85), Interval(40, 46), Interval(71, 95), Interval(67, 85),
         Interval(72, 86), Interval(52, 54), Interval(67, 77), Interval(38, 42), Interval(36, 38),
         Interval(57, 75), Interval(3, 3), Interval(49, 55), Interval(31, 35), Interval(9, 9)],
        # Job 40
        [Interval(27, 29), Interval(62, 78), Interval(7, 7), Interval(46, 56), Interval(31, 35),
         Interval(50, 64), Interval(88, 90), Interval(58, 62), Interval(58, 70), Interval(36, 36),
         Interval(66, 84), Interval(45, 53), Interval(13, 13), Interval(31, 41), Interval(57, 73)],
        # Job 41
        [Interval(67, 81), Interval(87, 107), Interval(86, 90), Interval(23, 31), Interval(82, 108),
         Interval(86, 112), Interval(16, 18), Interval(27, 35), Interval(80, 94), Interval(32, 36),
         Interval(27, 29), Interval(16, 16), Interval(15, 17), Interval(86, 102), Interval(13, 15)],
        # Job 42
        [Interval(57, 69), Interval(43, 51), Interval(6, 6), Interval(43, 43), Interval(42, 54),
         Interval(64, 66), Interval(82, 84), Interval(93, 103), Interval(57, 59), Interval(54, 66),
         Interval(11, 13), Interval(48, 48), Interval(86, 100), Interval(70, 84), Interval(32, 32)],
        # Job 43
        [Interval(30, 34), Interval(84, 104), Interval(64, 78), Interval(3, 3), Interval(20, 20),
         Interval(45, 45), Interval(10, 10), Interval(43, 47), Interval(6, 6), Interval(50, 64),
         Interval(35, 35), Interval(70, 82), Interval(41, 51), Interval(77, 97), Interval(24, 26)],
        # Job 44
        [Interval(39, 51), Interval(61, 65), Interval(73, 91), Interval(21, 25), Interval(1, 1),
         Interval(13, 13), Interval(50, 50), Interval(59, 69), Interval(72, 92), Interval(55, 55),
         Interval(39, 45), Interval(12, 16), Interval(33, 37), Interval(13, 17), Interval(47, 47)],
        # Job 45
        [Interval(6, 6), Interval(6, 6), Interval(24, 32), Interval(83, 109), Interval(2, 2),
         Interval(77, 93), Interval(89, 105), Interval(84, 96), Interval(73, 93), Interval(76, 76),
         Interval(60, 70), Interval(43, 49), Interval(63, 79), Interval(37, 47), Interval(59, 63)],
        # Job 46
        [Interval(86, 104), Interval(46, 62), Interval(43, 49), Interval(29, 37), Interval(12, 14),
         Interval(71, 71), Interval(34, 40), Interval(56, 64), Interval(44, 56), Interval(27, 33),
         Interval(52, 60), Interval(10, 10), Interval(57, 67), Interval(65, 87), Interval(53, 61)],
        # Job 47
        [Interval(96, 96), Interval(56, 72), Interval(6, 6), Interval(81, 99), Interval(1, 1),
         Interval(89, 109), Interval(79, 93), Interval(25, 29), Interval(17, 19), Interval(51, 61),
         Interval(18, 20), Interval(67, 79), Interval(72, 80), Interval(72, 92), Interval(78, 78)],
        # Job 48
        [Interval(84, 112), Interval(67, 71), Interval(67, 69), Interval(43, 47), Interval(17, 17),
         Interval(28, 30), Interval(15, 15), Interval(71, 91), Interval(29, 33), Interval(72, 86),
         Interval(51, 57), Interval(48, 52), Interval(73, 73), Interval(2, 2), Interval(81, 91)],
        # Job 49
        [Interval(42, 46), Interval(74, 82), Interval(31, 31), Interval(7, 9), Interval(7, 9),
         Interval(15, 15), Interval(89, 101), Interval(81, 85), Interval(3, 3), Interval(27, 33),
         Interval(35, 43), Interval(81, 103), Interval(47, 47), Interval(46, 52), Interval(41, 49)],
    ],
    'name': 'INT__TAI50_15_06.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai50_15_06_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI50_15_06.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI50_15_06.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI50_15_06_F_15_01_INTERVAL_DATA
