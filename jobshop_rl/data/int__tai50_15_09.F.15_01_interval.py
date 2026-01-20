"""
Problema INT__TAI50_15_09.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI50_15_09_F_15_01_INTERVAL_DATA = {
    'num_jobs': 50,
    'num_machines': 15,
    'problem_id': 'int__tai50_15_09.F.15_01_interval',
    'sequences': [
        [10, 4, 0, 6, 2, 3, 12, 1, 5, 11, 8, 7, 14, 13, 9],
        [14, 5, 2, 6, 3, 7, 9, 8, 0, 1, 13, 10, 12, 11, 4],
        [11, 14, 2, 5, 7, 13, 12, 0, 3, 9, 10, 4, 6, 1, 8],
        [6, 3, 4, 9, 2, 0, 12, 7, 5, 11, 10, 13, 1, 8, 14],
        [1, 10, 0, 9, 5, 4, 7, 12, 11, 3, 13, 14, 6, 8, 2],
        [2, 0, 8, 4, 12, 9, 6, 14, 13, 5, 3, 1, 7, 10, 11],
        [0, 11, 2, 13, 8, 4, 10, 12, 14, 7, 1, 6, 3, 5, 9],
        [3, 2, 4, 10, 6, 12, 5, 13, 8, 9, 14, 11, 0, 1, 7],
        [12, 10, 1, 4, 7, 9, 6, 2, 3, 11, 14, 5, 13, 0, 8],
        [12, 5, 14, 7, 10, 9, 6, 4, 3, 8, 11, 2, 13, 0, 1],
        [10, 5, 14, 3, 2, 13, 7, 4, 9, 12, 11, 6, 8, 0, 1],
        [5, 0, 14, 10, 9, 6, 11, 12, 8, 2, 1, 13, 7, 3, 4],
        [1, 12, 3, 5, 0, 8, 11, 9, 2, 4, 13, 14, 7, 6, 10],
        [8, 11, 10, 6, 5, 0, 4, 1, 14, 7, 12, 2, 3, 13, 9],
        [6, 7, 1, 2, 10, 14, 12, 8, 9, 0, 13, 4, 3, 5, 11],
        [1, 8, 10, 4, 6, 7, 13, 14, 12, 5, 3, 0, 2, 9, 11],
        [1, 0, 8, 3, 12, 2, 6, 4, 14, 11, 10, 13, 7, 9, 5],
        [2, 7, 14, 4, 9, 10, 3, 5, 6, 13, 12, 11, 8, 1, 0],
        [6, 4, 1, 12, 0, 14, 3, 8, 2, 7, 13, 10, 11, 5, 9],
        [8, 0, 14, 3, 7, 6, 1, 13, 5, 11, 12, 2, 9, 4, 10],
        [11, 13, 7, 14, 1, 12, 4, 5, 3, 9, 8, 10, 0, 2, 6],
        [12, 4, 1, 13, 6, 0, 5, 8, 3, 10, 11, 14, 7, 2, 9],
        [2, 9, 10, 7, 11, 4, 8, 0, 5, 3, 6, 12, 13, 14, 1],
        [5, 9, 3, 1, 2, 12, 0, 7, 14, 4, 10, 11, 6, 13, 8],
        [5, 12, 4, 11, 9, 14, 8, 1, 3, 2, 10, 0, 7, 6, 13],
        [14, 10, 2, 3, 0, 9, 11, 12, 7, 6, 1, 5, 13, 8, 4],
        [14, 2, 9, 1, 7, 5, 8, 3, 4, 12, 0, 6, 11, 13, 10],
        [8, 14, 11, 7, 6, 9, 12, 10, 0, 4, 1, 5, 3, 13, 2],
        [2, 12, 4, 13, 14, 6, 9, 3, 5, 1, 0, 8, 7, 11, 10],
        [13, 3, 1, 6, 10, 11, 9, 14, 0, 7, 5, 12, 4, 2, 8],
        [3, 1, 11, 6, 12, 7, 10, 14, 5, 13, 8, 0, 2, 4, 9],
        [0, 2, 4, 13, 5, 10, 3, 11, 7, 1, 14, 9, 12, 6, 8],
        [9, 10, 12, 5, 6, 14, 2, 0, 7, 3, 4, 1, 13, 11, 8],
        [4, 8, 0, 11, 2, 9, 7, 12, 1, 10, 3, 5, 13, 14, 6],
        [2, 14, 1, 11, 0, 6, 4, 3, 10, 5, 12, 7, 9, 8, 13],
        [2, 6, 9, 4, 1, 0, 14, 7, 3, 8, 13, 10, 5, 12, 11],
        [7, 3, 8, 13, 9, 10, 11, 4, 5, 1, 14, 2, 6, 12, 0],
        [9, 7, 3, 6, 4, 8, 1, 11, 14, 13, 12, 5, 0, 2, 10],
        [2, 10, 0, 5, 1, 3, 14, 4, 12, 13, 8, 7, 6, 11, 9],
        [4, 14, 13, 0, 5, 2, 10, 7, 9, 1, 11, 12, 3, 8, 6],
        [14, 3, 1, 13, 5, 6, 8, 4, 0, 9, 2, 10, 12, 7, 11],
        [1, 9, 5, 12, 7, 0, 11, 3, 14, 6, 10, 2, 4, 8, 13],
        [2, 10, 1, 11, 6, 13, 12, 7, 3, 8, 5, 14, 9, 4, 0],
        [7, 12, 14, 11, 9, 1, 5, 13, 3, 8, 4, 6, 2, 10, 0],
        [4, 0, 2, 5, 11, 13, 10, 14, 6, 8, 9, 7, 3, 12, 1],
        [9, 7, 6, 10, 13, 1, 8, 5, 11, 14, 12, 0, 3, 4, 2],
        [7, 5, 9, 14, 4, 2, 1, 0, 12, 13, 6, 10, 8, 11, 3],
        [11, 1, 0, 4, 9, 2, 3, 10, 5, 6, 13, 14, 12, 8, 7],
        [7, 8, 4, 14, 5, 2, 10, 0, 12, 6, 13, 9, 11, 1, 3],
        [11, 6, 9, 13, 7, 2, 0, 3, 12, 4, 14, 5, 10, 1, 8],
    ],
    'durations': [
        # Job 0
        [Interval(40, 52), Interval(43, 43), Interval(22, 28), Interval(88, 110), Interval(86, 94),
         Interval(21, 21), Interval(23, 31), Interval(15, 19), Interval(16, 16), Interval(83, 93),
         Interval(58, 70), Interval(8, 10), Interval(43, 57), Interval(51, 59), Interval(21, 23)],
        # Job 1
        [Interval(8, 10), Interval(35, 43), Interval(57, 59), Interval(14, 18), Interval(88, 108),
         Interval(51, 65), Interval(71, 91), Interval(51, 51), Interval(9, 11), Interval(27, 35),
         Interval(42, 56), Interval(56, 74), Interval(46, 50), Interval(61, 63), Interval(46, 56)],
        # Job 2
        [Interval(52, 56), Interval(42, 50), Interval(82, 110), Interval(44, 48), Interval(16, 16),
         Interval(17, 17), Interval(69, 75), Interval(46, 56), Interval(31, 35), Interval(84, 98),
         Interval(17, 19), Interval(73, 95), Interval(84, 90), Interval(27, 35), Interval(47, 55)],
        # Job 3
        [Interval(3, 3), Interval(83, 105), Interval(85, 97), Interval(2, 2), Interval(44, 56),
         Interval(80, 98), Interval(77, 79), Interval(5, 5), Interval(29, 31), Interval(10, 10),
         Interval(22, 22), Interval(67, 85), Interval(49, 51), Interval(45, 45), Interval(26, 30)],
        # Job 4
        [Interval(5, 5), Interval(48, 58), Interval(56, 58), Interval(12, 16), Interval(89, 91),
         Interval(8, 8), Interval(46, 58), Interval(65, 87), Interval(53, 65), Interval(14, 16),
         Interval(34, 44), Interval(34, 46), Interval(49, 59), Interval(53, 61), Interval(45, 59)],
        # Job 5
        [Interval(29, 33), Interval(2, 2), Interval(49, 63), Interval(61, 67), Interval(52, 58),
         Interval(86, 106), Interval(6, 6), Interval(35, 37), Interval(27, 31), Interval(50, 64),
         Interval(75, 97), Interval(65, 73), Interval(49, 59), Interval(65, 87), Interval(78, 100)],
        # Job 6
        [Interval(38, 40), Interval(7, 7), Interval(32, 32), Interval(71, 77), Interval(86, 94),
         Interval(59, 73), Interval(72, 80), Interval(47, 59), Interval(40, 52), Interval(27, 27),
         Interval(77, 89), Interval(46, 52), Interval(68, 76), Interval(20, 24), Interval(52, 54)],
        # Job 7
        [Interval(83, 83), Interval(18, 18), Interval(82, 90), Interval(77, 101), Interval(90, 96),
         Interval(54, 72), Interval(30, 38), Interval(95, 99), Interval(72, 96), Interval(53, 69),
         Interval(28, 36), Interval(47, 49), Interval(22, 24), Interval(76, 86), Interval(56, 66)],
        # Job 8
        [Interval(31, 33), Interval(11, 11), Interval(16, 20), Interval(51, 57), Interval(92, 100),
         Interval(57, 77), Interval(70, 76), Interval(53, 69), Interval(14, 16), Interval(65, 69),
         Interval(31, 37), Interval(34, 40), Interval(59, 71), Interval(41, 47), Interval(29, 35)],
        # Job 9
        [Interval(73, 85), Interval(22, 24), Interval(49, 53), Interval(51, 69), Interval(8, 10),
         Interval(53, 55), Interval(82, 88), Interval(81, 95), Interval(80, 86), Interval(48, 62),
         Interval(75, 99), Interval(87, 99), Interval(69, 91), Interval(62, 82), Interval(5, 5)],
        # Job 10
        [Interval(47, 61), Interval(54, 54), Interval(46, 62), Interval(56, 62), Interval(43, 55),
         Interval(68, 68), Interval(48, 64), Interval(8, 10), Interval(23, 23), Interval(53, 63),
         Interval(81, 95), Interval(71, 93), Interval(10, 10), Interval(74, 100), Interval(52, 56)],
        # Job 11
        [Interval(65, 79), Interval(78, 90), Interval(26, 32), Interval(53, 65), Interval(51, 69),
         Interval(91, 105), Interval(39, 43), Interval(82, 92), Interval(24, 30), Interval(29, 33),
         Interval(75, 83), Interval(69, 69), Interval(55, 73), Interval(81, 91), Interval(73, 81)],
        # Job 12
        [Interval(69, 73), Interval(61, 61), Interval(32, 34), Interval(55, 55), Interval(78, 88),
         Interval(9, 9), Interval(79, 95), Interval(18, 20), Interval(44, 54), Interval(68, 68),
         Interval(4, 4), Interval(21, 27), Interval(37, 45), Interval(49, 49), Interval(66, 88)],
        # Job 13
        [Interval(34, 38), Interval(20, 26), Interval(31, 41), Interval(35, 47), Interval(50, 62),
         Interval(63, 73), Interval(71, 91), Interval(46, 52), Interval(42, 48), Interval(61, 73),
         Interval(81, 97), Interval(51, 69), Interval(1, 1), Interval(52, 64), Interval(27, 29)],
        # Job 14
        [Interval(41, 45), Interval(69, 83), Interval(40, 44), Interval(56, 62), Interval(47, 53),
         Interval(3, 3), Interval(25, 27), Interval(37, 45), Interval(63, 69), Interval(52, 52),
         Interval(7, 9), Interval(30, 36), Interval(35, 45), Interval(36, 42), Interval(45, 55)],
        # Job 15
        [Interval(56, 74), Interval(30, 30), Interval(42, 56), Interval(12, 16), Interval(57, 71),
         Interval(34, 34), Interval(32, 38), Interval(60, 72), Interval(14, 18), Interval(41, 49),
         Interval(32, 40), Interval(80, 80), Interval(5, 5), Interval(2, 2), Interval(55, 71)],
        # Job 16
        [Interval(49, 57), Interval(6, 8), Interval(32, 36), Interval(53, 53), Interval(41, 45),
         Interval(78, 92), Interval(8, 10), Interval(56, 72), Interval(86, 98), Interval(64, 66),
         Interval(14, 16), Interval(1, 1), Interval(6, 6), Interval(83, 107), Interval(71, 93)],
        # Job 17
        [Interval(11, 11), Interval(3, 3), Interval(29, 37), Interval(62, 62), Interval(61, 79),
         Interval(6, 6), Interval(3, 3), Interval(35, 35), Interval(50, 64), Interval(75, 77),
         Interval(33, 43), Interval(25, 31), Interval(72, 84), Interval(6, 8), Interval(17, 17)],
        # Job 18
        [Interval(40, 40), Interval(47, 63), Interval(20, 22), Interval(11, 11), Interval(52, 64),
         Interval(7, 9), Interval(35, 41), Interval(19, 19), Interval(24, 26), Interval(49, 61),
         Interval(38, 40), Interval(91, 93), Interval(29, 31), Interval(82, 106), Interval(36, 42)],
        # Job 19
        [Interval(29, 39), Interval(16, 20), Interval(85, 113), Interval(28, 28), Interval(2, 2),
         Interval(40, 42), Interval(34, 36), Interval(6, 6), Interval(68, 72), Interval(4, 4),
         Interval(92, 98), Interval(54, 64), Interval(6, 8), Interval(84, 92), Interval(66, 76)],
        # Job 20
        [Interval(38, 40), Interval(41, 55), Interval(23, 31), Interval(24, 30), Interval(23, 23),
         Interval(76, 84), Interval(35, 35), Interval(62, 72), Interval(21, 23), Interval(85, 85),
         Interval(61, 79), Interval(34, 38), Interval(38, 48), Interval(73, 87), Interval(51, 69)],
        # Job 21
        [Interval(14, 16), Interval(19, 25), Interval(82, 104), Interval(77, 93), Interval(8, 10),
         Interval(37, 39), Interval(93, 103), Interval(23, 27), Interval(62, 66), Interval(44, 46),
         Interval(85, 107), Interval(34, 38), Interval(36, 38), Interval(40, 52), Interval(77, 101)],
        # Job 22
        [Interval(22, 24), Interval(20, 20), Interval(43, 49), Interval(83, 99), Interval(44, 46),
         Interval(67, 67), Interval(6, 6), Interval(69, 69), Interval(74, 90), Interval(75, 77),
         Interval(5, 5), Interval(62, 80), Interval(82, 82), Interval(62, 78), Interval(70, 74)],
        # Job 23
        [Interval(31, 41), Interval(85, 101), Interval(22, 24), Interval(12, 14), Interval(80, 80),
         Interval(41, 47), Interval(82, 108), Interval(78, 84), Interval(39, 49), Interval(42, 46),
         Interval(83, 87), Interval(57, 59), Interval(58, 66), Interval(17, 19), Interval(87, 101)],
        # Job 24
        [Interval(51, 69), Interval(64, 72), Interval(80, 88), Interval(33, 37), Interval(87, 97),
         Interval(53, 71), Interval(92, 96), Interval(88, 90), Interval(1, 1), Interval(42, 54),
         Interval(34, 38), Interval(33, 37), Interval(24, 32), Interval(32, 42), Interval(36, 46)],
        # Job 25
        [Interval(61, 63), Interval(30, 40), Interval(53, 71), Interval(14, 16), Interval(8, 8),
         Interval(18, 18), Interval(21, 21), Interval(27, 29), Interval(62, 82), Interval(57, 73),
         Interval(70, 94), Interval(15, 17), Interval(34, 46), Interval(82, 104), Interval(41, 41)],
        # Job 26
        [Interval(11, 13), Interval(14, 14), Interval(46, 60), Interval(20, 20), Interval(95, 103),
         Interval(26, 34), Interval(41, 55), Interval(9, 9), Interval(44, 58), Interval(12, 12),
         Interval(51, 69), Interval(51, 51), Interval(78, 82), Interval(70, 92), Interval(8, 10)],
        # Job 27
        [Interval(60, 62), Interval(53, 71), Interval(31, 35), Interval(53, 69), Interval(64, 82),
         Interval(3, 3), Interval(1, 1), Interval(19, 19), Interval(77, 83), Interval(38, 42),
         Interval(14, 18), Interval(22, 24), Interval(6, 8), Interval(81, 83), Interval(4, 4)],
        # Job 28
        [Interval(12, 12), Interval(70, 82), Interval(87, 103), Interval(55, 71), Interval(51, 53),
         Interval(60, 60), Interval(76, 96), Interval(66, 68), Interval(25, 27), Interval(22, 28),
         Interval(85, 85), Interval(11, 13), Interval(86, 86), Interval(92, 92), Interval(68, 78)],
        # Job 29
        [Interval(51, 63), Interval(53, 59), Interval(42, 52), Interval(86, 110), Interval(55, 55),
         Interval(3, 3), Interval(28, 30), Interval(31, 35), Interval(24, 24), Interval(87, 97),
         Interval(45, 57), Interval(64, 68), Interval(35, 41), Interval(17, 21), Interval(52, 66)],
        # Job 30
        [Interval(11, 13), Interval(51, 57), Interval(72, 74), Interval(31, 35), Interval(23, 23),
         Interval(74, 76), Interval(69, 69), Interval(80, 106), Interval(56, 72), Interval(44, 48),
         Interval(39, 49), Interval(80, 82), Interval(1, 1), Interval(77, 79), Interval(98, 98)],
        # Job 31
        [Interval(20, 24), Interval(95, 95), Interval(24, 32), Interval(8, 8), Interval(55, 63),
         Interval(63, 63), Interval(77, 97), Interval(72, 96), Interval(20, 24), Interval(43, 43),
         Interval(76, 94), Interval(85, 113), Interval(9, 9), Interval(11, 11), Interval(70, 88)],
        # Job 32
        [Interval(2, 2), Interval(20, 20), Interval(49, 49), Interval(28, 36), Interval(42, 56),
         Interval(15, 19), Interval(61, 81), Interval(69, 89), Interval(22, 28), Interval(78, 78),
         Interval(32, 34), Interval(19, 21), Interval(74, 94), Interval(51, 69), Interval(65, 69)],
        # Job 33
        [Interval(11, 13), Interval(43, 47), Interval(78, 84), Interval(25, 33), Interval(35, 47),
         Interval(79, 95), Interval(50, 64), Interval(66, 70), Interval(78, 80), Interval(83, 111),
         Interval(15, 17), Interval(53, 69), Interval(59, 67), Interval(25, 25), Interval(46, 56)],
        # Job 34
        [Interval(41, 41), Interval(33, 33), Interval(77, 83), Interval(65, 87), Interval(68, 80),
         Interval(3, 3), Interval(50, 60), Interval(28, 36), Interval(17, 23), Interval(74, 80),
         Interval(53, 67), Interval(58, 66), Interval(68, 72), Interval(59, 77), Interval(80, 102)],
        # Job 35
        [Interval(87, 105), Interval(12, 14), Interval(67, 79), Interval(16, 16), Interval(6, 6),
         Interval(20, 26), Interval(85, 91), Interval(69, 75), Interval(33, 41), Interval(32, 34),
         Interval(93, 103), Interval(13, 15), Interval(69, 93), Interval(83, 85), Interval(89, 101)],
        # Job 36
        [Interval(75, 93), Interval(45, 49), Interval(17, 17), Interval(38, 38), Interval(11, 11),
         Interval(32, 34), Interval(42, 56), Interval(9, 9), Interval(44, 58), Interval(26, 26),
         Interval(90, 108), Interval(16, 20), Interval(36, 46), Interval(27, 29), Interval(6, 8)],
        # Job 37
        [Interval(1, 1), Interval(12, 16), Interval(33, 35), Interval(48, 50), Interval(10, 12),
         Interval(69, 87), Interval(8, 8), Interval(7, 9), Interval(61, 75), Interval(38, 38),
         Interval(67, 77), Interval(66, 74), Interval(28, 36), Interval(80, 82), Interval(77, 95)],
        # Job 38
        [Interval(83, 103), Interval(31, 37), Interval(6, 6), Interval(91, 107), Interval(4, 4),
         Interval(26, 32), Interval(24, 24), Interval(80, 88), Interval(53, 53), Interval(17, 17),
         Interval(48, 52), Interval(52, 54), Interval(22, 26), Interval(55, 63), Interval(53, 71)],
        # Job 39
        [Interval(58, 76), Interval(68, 82), Interval(87, 91), Interval(75, 89), Interval(38, 40),
         Interval(79, 85), Interval(30, 40), Interval(55, 61), Interval(59, 67), Interval(4, 4),
         Interval(63, 65), Interval(8, 8), Interval(27, 33), Interval(50, 56), Interval(66, 82)],
        # Job 40
        [Interval(42, 46), Interval(15, 19), Interval(26, 26), Interval(71, 75), Interval(31, 37),
         Interval(38, 38), Interval(40, 50), Interval(65, 77), Interval(16, 16), Interval(82, 110),
         Interval(75, 97), Interval(27, 33), Interval(41, 51), Interval(26, 26), Interval(6, 8)],
        # Job 41
        [Interval(39, 51), Interval(14, 18), Interval(91, 101), Interval(58, 78), Interval(44, 52),
         Interval(29, 31), Interval(77, 81), Interval(90, 90), Interval(76, 92), Interval(44, 52),
         Interval(75, 83), Interval(13, 15), Interval(39, 45), Interval(82, 82), Interval(23, 29)],
        # Job 42
        [Interval(1, 1), Interval(61, 63), Interval(45, 45), Interval(3, 3), Interval(7, 7),
         Interval(15, 15), Interval(20, 24), Interval(66, 76), Interval(19, 19), Interval(80, 94),
         Interval(50, 60), Interval(12, 12), Interval(47, 53), Interval(9, 11), Interval(33, 39)],
        # Job 43
        [Interval(69, 73), Interval(3, 3), Interval(61, 61), Interval(33, 35), Interval(57, 63),
         Interval(63, 81), Interval(34, 34), Interval(31, 35), Interval(60, 78), Interval(32, 40),
         Interval(85, 91), Interval(1, 1), Interval(3, 3), Interval(85, 111), Interval(86, 94)],
        # Job 44
        [Interval(75, 93), Interval(45, 55), Interval(74, 74), Interval(16, 16), Interval(80, 92),
         Interval(28, 36), Interval(2, 2), Interval(22, 22), Interval(20, 24), Interval(63, 83),
         Interval(15, 17), Interval(7, 9), Interval(64, 64), Interval(60, 80), Interval(71, 95)],
        # Job 45
        [Interval(52, 62), Interval(20, 24), Interval(40, 46), Interval(2, 2), Interval(9, 11),
         Interval(37, 37), Interval(43, 49), Interval(83, 95), Interval(28, 34), Interval(24, 30),
         Interval(46, 48), Interval(77, 93), Interval(74, 98), Interval(75, 87), Interval(33, 43)],
        # Job 46
        [Interval(34, 44), Interval(14, 14), Interval(59, 69), Interval(81, 93), Interval(30, 38),
         Interval(30, 36), Interval(35, 39), Interval(78, 78), Interval(77, 91), Interval(23, 31),
         Interval(43, 49), Interval(93, 93), Interval(65, 85), Interval(63, 77), Interval(8, 10)],
        # Job 47
        [Interval(23, 27), Interval(78, 90), Interval(14, 16), Interval(54, 64), Interval(79, 91),
         Interval(49, 57), Interval(28, 30), Interval(62, 78), Interval(50, 50), Interval(80, 106),
         Interval(23, 23), Interval(96, 100), Interval(2, 2), Interval(17, 17), Interval(83, 91)],
        # Job 48
        [Interval(11, 11), Interval(7, 7), Interval(62, 78), Interval(18, 20), Interval(12, 14),
         Interval(22, 24), Interval(89, 99), Interval(2, 2), Interval(55, 55), Interval(88, 98),
         Interval(74, 80), Interval(88, 96), Interval(38, 40), Interval(29, 37), Interval(66, 84)],
        # Job 49
        [Interval(28, 30), Interval(56, 64), Interval(27, 27), Interval(51, 63), Interval(71, 87),
         Interval(59, 75), Interval(66, 66), Interval(21, 23), Interval(24, 30), Interval(20, 20),
         Interval(5, 5), Interval(39, 47), Interval(77, 81), Interval(8, 10), Interval(73, 97)],
    ],
    'name': 'INT__TAI50_15_09.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai50_15_09_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI50_15_09.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI50_15_09.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI50_15_09_F_15_01_INTERVAL_DATA
