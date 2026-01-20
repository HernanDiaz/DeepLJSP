"""
Problema INT__TAI50_15_08.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI50_15_08_F_15_01_INTERVAL_DATA = {
    'num_jobs': 50,
    'num_machines': 15,
    'problem_id': 'int__tai50_15_08.F.15_01_interval',
    'sequences': [
        [11, 1, 2, 8, 5, 13, 10, 14, 4, 12, 9, 6, 3, 7, 0],
        [1, 0, 3, 9, 5, 4, 10, 13, 2, 6, 7, 12, 8, 11, 14],
        [9, 7, 4, 0, 2, 1, 8, 10, 3, 5, 12, 14, 11, 6, 13],
        [0, 12, 3, 11, 10, 2, 13, 7, 14, 6, 8, 4, 9, 5, 1],
        [3, 1, 9, 5, 10, 8, 2, 0, 13, 7, 4, 6, 14, 11, 12],
        [5, 4, 10, 8, 3, 13, 1, 9, 6, 2, 11, 14, 0, 12, 7],
        [11, 3, 9, 2, 4, 13, 7, 6, 10, 0, 14, 12, 8, 1, 5],
        [7, 9, 0, 12, 13, 1, 3, 14, 4, 5, 11, 6, 2, 10, 8],
        [14, 11, 2, 12, 13, 4, 5, 9, 7, 6, 10, 0, 8, 1, 3],
        [12, 1, 14, 10, 11, 2, 8, 3, 13, 9, 7, 0, 5, 6, 4],
        [5, 14, 2, 12, 7, 3, 6, 10, 1, 11, 9, 4, 8, 13, 0],
        [7, 11, 1, 4, 6, 2, 8, 9, 13, 10, 5, 14, 0, 12, 3],
        [8, 1, 3, 10, 11, 7, 6, 0, 13, 2, 14, 4, 12, 5, 9],
        [11, 6, 12, 13, 4, 1, 0, 9, 8, 5, 10, 2, 3, 7, 14],
        [8, 4, 3, 13, 1, 2, 12, 6, 9, 0, 14, 5, 11, 7, 10],
        [8, 2, 5, 3, 4, 12, 14, 1, 9, 10, 6, 13, 0, 7, 11],
        [0, 10, 4, 7, 6, 14, 11, 9, 2, 5, 1, 13, 12, 8, 3],
        [1, 8, 6, 2, 9, 4, 13, 11, 10, 3, 14, 7, 5, 0, 12],
        [12, 5, 11, 2, 7, 3, 14, 1, 8, 4, 13, 9, 6, 10, 0],
        [14, 8, 4, 5, 0, 2, 11, 9, 1, 6, 13, 10, 3, 7, 12],
        [3, 4, 13, 11, 7, 12, 6, 9, 14, 5, 8, 1, 0, 10, 2],
        [7, 8, 14, 5, 2, 0, 1, 9, 10, 12, 6, 4, 13, 3, 11],
        [6, 11, 14, 7, 12, 9, 8, 0, 1, 2, 4, 13, 3, 10, 5],
        [9, 2, 3, 14, 8, 1, 10, 4, 13, 11, 6, 5, 7, 12, 0],
        [2, 11, 1, 9, 0, 4, 12, 5, 8, 6, 7, 13, 3, 10, 14],
        [1, 11, 8, 0, 12, 3, 10, 14, 7, 13, 2, 4, 6, 5, 9],
        [5, 3, 11, 12, 14, 2, 10, 8, 13, 6, 9, 0, 4, 1, 7],
        [7, 8, 2, 5, 13, 4, 9, 6, 14, 10, 12, 0, 3, 11, 1],
        [2, 0, 11, 5, 7, 12, 10, 13, 9, 6, 1, 8, 4, 3, 14],
        [7, 11, 9, 0, 6, 8, 4, 12, 2, 3, 14, 5, 1, 13, 10],
        [14, 2, 8, 10, 7, 4, 3, 1, 9, 0, 11, 5, 13, 12, 6],
        [6, 8, 7, 11, 4, 2, 3, 1, 10, 13, 9, 5, 0, 14, 12],
        [13, 2, 1, 14, 6, 0, 12, 11, 4, 10, 5, 7, 3, 9, 8],
        [0, 3, 14, 7, 9, 2, 10, 4, 11, 6, 8, 1, 5, 12, 13],
        [4, 3, 11, 13, 7, 5, 0, 8, 6, 12, 2, 1, 14, 10, 9],
        [7, 13, 4, 8, 12, 14, 10, 11, 0, 5, 2, 9, 1, 3, 6],
        [12, 10, 4, 1, 8, 5, 9, 2, 11, 0, 14, 6, 3, 7, 13],
        [0, 5, 4, 14, 13, 1, 2, 10, 9, 8, 12, 6, 11, 7, 3],
        [2, 11, 9, 1, 7, 14, 0, 5, 12, 3, 6, 13, 4, 8, 10],
        [12, 3, 10, 6, 9, 0, 2, 11, 7, 14, 8, 4, 1, 13, 5],
        [5, 10, 12, 0, 8, 7, 6, 9, 11, 1, 2, 4, 14, 3, 13],
        [6, 13, 7, 9, 3, 1, 14, 4, 11, 12, 2, 10, 5, 8, 0],
        [4, 8, 9, 7, 6, 2, 5, 13, 3, 11, 10, 0, 14, 12, 1],
        [1, 7, 8, 2, 12, 9, 11, 4, 14, 10, 3, 6, 5, 0, 13],
        [7, 4, 8, 10, 3, 13, 2, 12, 0, 1, 9, 14, 5, 6, 11],
        [2, 14, 12, 7, 4, 13, 5, 9, 0, 3, 1, 8, 10, 6, 11],
        [7, 2, 11, 13, 8, 10, 4, 12, 9, 0, 3, 5, 14, 1, 6],
        [9, 14, 1, 2, 12, 11, 4, 7, 5, 10, 0, 3, 6, 13, 8],
        [12, 0, 10, 4, 8, 9, 7, 11, 3, 2, 5, 1, 14, 6, 13],
        [11, 3, 5, 10, 1, 6, 14, 13, 12, 0, 4, 2, 8, 9, 7],
    ],
    'durations': [
        # Job 0
        [Interval(75, 97), Interval(13, 13), Interval(57, 73), Interval(17, 23), Interval(73, 79),
         Interval(79, 85), Interval(36, 48), Interval(9, 11), Interval(48, 52), Interval(28, 30),
         Interval(27, 33), Interval(48, 58), Interval(45, 59), Interval(18, 20), Interval(23, 25)],
        # Job 1
        [Interval(17, 21), Interval(68, 84), Interval(76, 78), Interval(63, 83), Interval(68, 84),
         Interval(76, 98), Interval(53, 69), Interval(51, 51), Interval(54, 68), Interval(85, 113),
         Interval(33, 43), Interval(84, 112), Interval(32, 36), Interval(34, 34), Interval(39, 49)],
        # Job 2
        [Interval(28, 30), Interval(71, 89), Interval(54, 72), Interval(15, 15), Interval(75, 75),
         Interval(27, 27), Interval(94, 102), Interval(34, 42), Interval(53, 61), Interval(74, 86),
         Interval(53, 59), Interval(46, 62), Interval(53, 57), Interval(30, 40), Interval(14, 16)],
        # Job 3
        [Interval(64, 80), Interval(68, 78), Interval(58, 76), Interval(52, 64), Interval(14, 14),
         Interval(56, 62), Interval(6, 6), Interval(66, 74), Interval(87, 89), Interval(58, 74),
         Interval(64, 66), Interval(95, 97), Interval(87, 103), Interval(50, 62), Interval(16, 16)],
        # Job 4
        [Interval(18, 24), Interval(77, 79), Interval(3, 3), Interval(72, 80), Interval(9, 11),
         Interval(40, 52), Interval(87, 109), Interval(12, 12), Interval(47, 63), Interval(79, 105),
         Interval(38, 46), Interval(64, 72), Interval(58, 76), Interval(70, 80), Interval(84, 110)],
        # Job 5
        [Interval(29, 31), Interval(19, 21), Interval(71, 89), Interval(16, 16), Interval(71, 81),
         Interval(40, 50), Interval(84, 110), Interval(66, 74), Interval(49, 59), Interval(33, 43),
         Interval(67, 85), Interval(82, 86), Interval(52, 58), Interval(91, 95), Interval(64, 70)],
        # Job 6
        [Interval(78, 84), Interval(47, 59), Interval(35, 39), Interval(74, 94), Interval(29, 37),
         Interval(69, 69), Interval(48, 56), Interval(11, 11), Interval(2, 2), Interval(7, 7),
         Interval(72, 86), Interval(35, 37), Interval(78, 78), Interval(90, 94), Interval(18, 20)],
        # Job 7
        [Interval(24, 32), Interval(76, 80), Interval(53, 71), Interval(15, 19), Interval(37, 39),
         Interval(57, 75), Interval(59, 77), Interval(6, 6), Interval(51, 69), Interval(90, 96),
         Interval(44, 50), Interval(59, 67), Interval(24, 28), Interval(55, 61), Interval(43, 49)],
        # Job 8
        [Interval(17, 21), Interval(4, 4), Interval(62, 70), Interval(49, 53), Interval(52, 70),
         Interval(16, 16), Interval(64, 80), Interval(18, 22), Interval(82, 88), Interval(88, 102),
         Interval(34, 40), Interval(19, 23), Interval(88, 100), Interval(58, 70), Interval(7, 9)],
        # Job 9
        [Interval(43, 47), Interval(81, 87), Interval(45, 59), Interval(43, 57), Interval(75, 79),
         Interval(37, 39), Interval(55, 65), Interval(2, 2), Interval(48, 52), Interval(57, 73),
         Interval(62, 80), Interval(63, 71), Interval(82, 108), Interval(61, 81), Interval(21, 27)],
        # Job 10
        [Interval(32, 32), Interval(6, 6), Interval(36, 48), Interval(70, 78), Interval(49, 63),
         Interval(38, 38), Interval(47, 63), Interval(74, 94), Interval(93, 99), Interval(79, 93),
         Interval(43, 51), Interval(33, 43), Interval(4, 4), Interval(71, 73), Interval(78, 104)],
        # Job 11
        [Interval(78, 84), Interval(44, 54), Interval(37, 43), Interval(52, 62), Interval(14, 18),
         Interval(6, 8), Interval(13, 13), Interval(17, 19), Interval(91, 101), Interval(76, 92),
         Interval(49, 57), Interval(67, 73), Interval(94, 94), Interval(63, 85), Interval(84, 94)],
        # Job 12
        [Interval(67, 75), Interval(64, 68), Interval(45, 45), Interval(26, 28), Interval(79, 79),
         Interval(71, 79), Interval(67, 75), Interval(80, 96), Interval(13, 15), Interval(32, 40),
         Interval(87, 89), Interval(20, 26), Interval(48, 56), Interval(74, 74), Interval(67, 89)],
        # Job 13
        [Interval(43, 49), Interval(60, 78), Interval(21, 27), Interval(17, 23), Interval(33, 41),
         Interval(50, 56), Interval(72, 92), Interval(32, 36), Interval(50, 58), Interval(43, 51),
         Interval(12, 14), Interval(24, 32), Interval(70, 86), Interval(40, 44), Interval(82, 90)],
        # Job 14
        [Interval(42, 50), Interval(84, 92), Interval(35, 39), Interval(70, 80), Interval(52, 60),
         Interval(70, 84), Interval(20, 22), Interval(8, 8), Interval(45, 59), Interval(47, 59),
         Interval(11, 13), Interval(73, 89), Interval(65, 79), Interval(68, 90), Interval(97, 99)],
        # Job 15
        [Interval(11, 13), Interval(9, 11), Interval(87, 109), Interval(15, 15), Interval(50, 60),
         Interval(44, 52), Interval(82, 100), Interval(10, 12), Interval(25, 31), Interval(42, 42),
         Interval(12, 14), Interval(78, 92), Interval(13, 17), Interval(20, 22), Interval(24, 24)],
        # Job 16
        [Interval(42, 46), Interval(42, 50), Interval(73, 85), Interval(12, 14), Interval(45, 51),
         Interval(76, 80), Interval(61, 73), Interval(64, 80), Interval(75, 99), Interval(60, 68),
         Interval(18, 24), Interval(58, 58), Interval(65, 85), Interval(84, 88), Interval(9, 11)],
        # Job 17
        [Interval(32, 32), Interval(63, 83), Interval(63, 77), Interval(28, 32), Interval(81, 101),
         Interval(60, 66), Interval(33, 33), Interval(33, 43), Interval(41, 43), Interval(78, 86),
         Interval(63, 79), Interval(61, 79), Interval(71, 85), Interval(15, 15), Interval(75, 85)],
        # Job 18
        [Interval(6, 6), Interval(24, 30), Interval(76, 82), Interval(59, 59), Interval(74, 80),
         Interval(87, 111), Interval(25, 29), Interval(23, 29), Interval(53, 69), Interval(10, 12),
         Interval(20, 20), Interval(65, 67), Interval(93, 99), Interval(53, 57), Interval(46, 50)],
        # Job 19
        [Interval(52, 62), Interval(41, 53), Interval(81, 87), Interval(78, 90), Interval(88, 96),
         Interval(4, 4), Interval(53, 71), Interval(20, 26), Interval(50, 62), Interval(99, 99),
         Interval(64, 72), Interval(5, 5), Interval(31, 31), Interval(77, 89), Interval(30, 32)],
        # Job 20
        [Interval(24, 24), Interval(37, 49), Interval(46, 50), Interval(71, 87), Interval(36, 44),
         Interval(49, 65), Interval(84, 96), Interval(73, 93), Interval(7, 9), Interval(90, 108),
         Interval(25, 33), Interval(8, 8), Interval(38, 42), Interval(58, 70), Interval(55, 59)],
        # Job 21
        [Interval(75, 79), Interval(47, 59), Interval(1, 1), Interval(94, 104), Interval(38, 40),
         Interval(70, 92), Interval(50, 66), Interval(90, 98), Interval(40, 42), Interval(86, 100),
         Interval(55, 67), Interval(24, 24), Interval(32, 32), Interval(31, 31), Interval(43, 53)],
        # Job 22
        [Interval(41, 43), Interval(34, 44), Interval(60, 60), Interval(36, 46), Interval(39, 41),
         Interval(39, 51), Interval(13, 15), Interval(25, 29), Interval(7, 9), Interval(29, 29),
         Interval(83, 95), Interval(80, 104), Interval(71, 77), Interval(85, 109), Interval(15, 17)],
        # Job 23
        [Interval(14, 14), Interval(28, 28), Interval(10, 10), Interval(6, 6), Interval(26, 28),
         Interval(53, 61), Interval(46, 62), Interval(59, 65), Interval(54, 60), Interval(93, 103),
         Interval(30, 34), Interval(28, 36), Interval(21, 21), Interval(60, 62), Interval(59, 73)],
        # Job 24
        [Interval(6, 6), Interval(13, 13), Interval(32, 34), Interval(75, 101), Interval(80, 104),
         Interval(17, 23), Interval(77, 81), Interval(54, 72), Interval(25, 33), Interval(90, 104),
         Interval(64, 68), Interval(59, 59), Interval(2, 2), Interval(82, 84), Interval(19, 21)],
        # Job 25
        [Interval(31, 41), Interval(30, 40), Interval(60, 80), Interval(31, 37), Interval(52, 68),
         Interval(55, 71), Interval(89, 91), Interval(85, 103), Interval(56, 56), Interval(23, 31),
         Interval(48, 50), Interval(89, 97), Interval(23, 31), Interval(34, 44), Interval(44, 44)],
        # Job 26
        [Interval(17, 21), Interval(13, 13), Interval(46, 62), Interval(69, 69), Interval(55, 57),
         Interval(28, 36), Interval(69, 91), Interval(30, 30), Interval(42, 56), Interval(69, 79),
         Interval(69, 89), Interval(22, 28), Interval(66, 72), Interval(9, 9), Interval(49, 53)],
        # Job 27
        [Interval(33, 41), Interval(87, 97), Interval(51, 67), Interval(11, 11), Interval(41, 41),
         Interval(62, 74), Interval(3, 3), Interval(6, 6), Interval(3, 3), Interval(50, 58),
         Interval(86, 110), Interval(80, 84), Interval(21, 21), Interval(53, 69), Interval(93, 97)],
        # Job 28
        [Interval(76, 82), Interval(13, 17), Interval(44, 44), Interval(79, 103), Interval(93, 93),
         Interval(38, 38), Interval(83, 97), Interval(19, 23), Interval(40, 44), Interval(35, 45),
         Interval(13, 17), Interval(24, 24), Interval(94, 100), Interval(32, 36), Interval(27, 27)],
        # Job 29
        [Interval(70, 78), Interval(61, 77), Interval(78, 84), Interval(6, 8), Interval(63, 79),
         Interval(6, 6), Interval(28, 36), Interval(13, 17), Interval(27, 29), Interval(6, 6),
         Interval(52, 54), Interval(68, 78), Interval(65, 65), Interval(29, 29), Interval(37, 37)],
        # Job 30
        [Interval(39, 51), Interval(75, 99), Interval(25, 29), Interval(67, 85), Interval(63, 65),
         Interval(35, 35), Interval(4, 4), Interval(57, 57), Interval(39, 47), Interval(98, 98),
         Interval(54, 70), Interval(46, 52), Interval(41, 47), Interval(75, 75), Interval(34, 42)],
        # Job 31
        [Interval(80, 106), Interval(72, 84), Interval(92, 92), Interval(39, 49), Interval(17, 23),
         Interval(83, 83), Interval(48, 54), Interval(60, 76), Interval(89, 93), Interval(7, 7),
         Interval(83, 111), Interval(59, 79), Interval(85, 109), Interval(80, 108), Interval(50, 66)],
        # Job 32
        [Interval(70, 90), Interval(80, 80), Interval(21, 23), Interval(48, 54), Interval(62, 80),
         Interval(22, 28), Interval(13, 13), Interval(6, 8), Interval(84, 92), Interval(26, 26),
         Interval(73, 93), Interval(63, 83), Interval(67, 79), Interval(34, 44), Interval(57, 59)],
        # Job 33
        [Interval(76, 78), Interval(17, 21), Interval(8, 10), Interval(52, 68), Interval(18, 20),
         Interval(85, 89), Interval(54, 66), Interval(48, 48), Interval(84, 88), Interval(49, 51),
         Interval(6, 8), Interval(18, 20), Interval(13, 15), Interval(46, 58), Interval(84, 110)],
        # Job 34
        [Interval(4, 4), Interval(82, 90), Interval(50, 62), Interval(80, 92), Interval(48, 50),
         Interval(14, 18), Interval(41, 51), Interval(85, 101), Interval(76, 98), Interval(36, 42),
         Interval(22, 22), Interval(1, 1), Interval(61, 81), Interval(4, 4), Interval(81, 87)],
        # Job 35
        [Interval(38, 40), Interval(75, 93), Interval(93, 103), Interval(90, 100), Interval(20, 24),
         Interval(41, 55), Interval(28, 28), Interval(25, 29), Interval(19, 23), Interval(53, 57),
         Interval(79, 81), Interval(10, 10), Interval(83, 95), Interval(84, 90), Interval(66, 86)],
        # Job 36
        [Interval(66, 72), Interval(68, 92), Interval(58, 60), Interval(89, 107), Interval(65, 87),
         Interval(11, 13), Interval(4, 4), Interval(56, 60), Interval(21, 27), Interval(77, 95),
         Interval(43, 47), Interval(88, 90), Interval(15, 19), Interval(27, 33), Interval(76, 86)],
        # Job 37
        [Interval(20, 24), Interval(5, 5), Interval(25, 31), Interval(18, 18), Interval(43, 49),
         Interval(83, 93), Interval(9, 11), Interval(89, 91), Interval(71, 89), Interval(48, 58),
         Interval(37, 45), Interval(90, 106), Interval(25, 31), Interval(12, 12), Interval(24, 26)],
        # Job 38
        [Interval(93, 93), Interval(19, 19), Interval(80, 86), Interval(57, 59), Interval(56, 66),
         Interval(7, 7), Interval(75, 101), Interval(15, 19), Interval(74, 88), Interval(67, 71),
         Interval(70, 82), Interval(12, 12), Interval(69, 73), Interval(52, 70), Interval(26, 30)],
        # Job 39
        [Interval(20, 22), Interval(20, 20), Interval(84, 94), Interval(34, 42), Interval(85, 97),
         Interval(44, 54), Interval(40, 44), Interval(23, 29), Interval(88, 90), Interval(78, 82),
         Interval(9, 11), Interval(15, 15), Interval(43, 55), Interval(41, 49), Interval(58, 60)],
        # Job 40
        [Interval(74, 98), Interval(2, 2), Interval(17, 23), Interval(16, 18), Interval(43, 53),
         Interval(45, 47), Interval(6, 6), Interval(37, 49), Interval(14, 18), Interval(44, 58),
         Interval(70, 78), Interval(69, 93), Interval(68, 80), Interval(61, 67), Interval(15, 15)],
        # Job 41
        [Interval(47, 47), Interval(89, 107), Interval(30, 34), Interval(33, 37), Interval(73, 89),
         Interval(89, 103), Interval(42, 42), Interval(13, 17), Interval(35, 35), Interval(91, 93),
         Interval(52, 58), Interval(96, 100), Interval(55, 67), Interval(68, 80), Interval(30, 30)],
        # Job 42
        [Interval(41, 47), Interval(7, 9), Interval(53, 53), Interval(42, 48), Interval(64, 78),
         Interval(59, 71), Interval(85, 89), Interval(4, 4), Interval(35, 35), Interval(9, 9),
         Interval(29, 31), Interval(49, 63), Interval(66, 68), Interval(63, 73), Interval(79, 101)],
        # Job 43
        [Interval(55, 69), Interval(30, 32), Interval(12, 16), Interval(41, 45), Interval(19, 23),
         Interval(52, 64), Interval(82, 82), Interval(85, 85), Interval(81, 95), Interval(29, 37),
         Interval(39, 39), Interval(65, 75), Interval(54, 72), Interval(77, 87), Interval(49, 65)],
        # Job 44
        [Interval(71, 71), Interval(85, 113), Interval(67, 89), Interval(75, 91), Interval(81, 95),
         Interval(9, 9), Interval(44, 56), Interval(38, 38), Interval(70, 82), Interval(79, 91),
         Interval(86, 108), Interval(17, 21), Interval(66, 70), Interval(46, 56), Interval(22, 28)],
        # Job 45
        [Interval(3, 3), Interval(53, 61), Interval(64, 86), Interval(81, 109), Interval(6, 6),
         Interval(31, 31), Interval(73, 85), Interval(81, 91), Interval(84, 106), Interval(78, 96),
         Interval(62, 70), Interval(35, 35), Interval(62, 74), Interval(15, 19), Interval(17, 19)],
        # Job 46
        [Interval(68, 68), Interval(62, 80), Interval(76, 92), Interval(58, 70), Interval(49, 57),
         Interval(62, 72), Interval(40, 48), Interval(1, 1), Interval(57, 69), Interval(25, 29),
         Interval(9, 11), Interval(20, 22), Interval(44, 56), Interval(13, 13), Interval(65, 87)],
        # Job 47
        [Interval(54, 58), Interval(76, 78), Interval(38, 42), Interval(79, 85), Interval(71, 79),
         Interval(92, 92), Interval(15, 19), Interval(67, 77), Interval(9, 11), Interval(12, 12),
         Interval(46, 50), Interval(5, 5), Interval(3, 3), Interval(13, 13), Interval(31, 35)],
        # Job 48
        [Interval(24, 26), Interval(82, 90), Interval(32, 32), Interval(27, 35), Interval(12, 16),
         Interval(56, 60), Interval(29, 33), Interval(61, 63), Interval(37, 45), Interval(49, 61),
         Interval(39, 49), Interval(13, 13), Interval(50, 56), Interval(30, 36), Interval(62, 64)],
        # Job 49
        [Interval(7, 9), Interval(92, 98), Interval(41, 47), Interval(33, 43), Interval(6, 6),
         Interval(95, 95), Interval(82, 92), Interval(42, 52), Interval(42, 42), Interval(65, 79),
         Interval(90, 96), Interval(82, 102), Interval(35, 41), Interval(95, 101), Interval(50, 60)],
    ],
    'name': 'INT__TAI50_15_08.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai50_15_08_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI50_15_08.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI50_15_08.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI50_15_08_F_15_01_INTERVAL_DATA
