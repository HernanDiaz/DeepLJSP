"""
Problema INT__TAI50_20_05.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI50_20_05_F_15_01_INTERVAL_DATA = {
    'num_jobs': 50,
    'num_machines': 20,
    'problem_id': 'int__tai50_20_05.F.15_01_interval',
    'sequences': [
        [7, 15, 11, 5, 9, 16, 0, 8, 1, 4, 14, 18, 13, 10, 3, 19, 6, 2, 17, 12],
        [15, 0, 2, 5, 12, 17, 10, 4, 11, 1, 18, 3, 9, 14, 19, 8, 6, 16, 7, 13],
        [15, 11, 8, 17, 3, 7, 12, 13, 2, 16, 4, 19, 9, 14, 0, 5, 1, 18, 10, 6],
        [6, 16, 1, 7, 11, 5, 14, 4, 17, 2, 19, 3, 18, 10, 9, 0, 13, 15, 8, 12],
        [13, 8, 2, 0, 19, 11, 9, 10, 7, 1, 17, 12, 6, 14, 16, 4, 15, 18, 5, 3],
        [9, 5, 14, 17, 12, 11, 3, 0, 13, 10, 18, 1, 8, 7, 16, 15, 19, 6, 2, 4],
        [15, 12, 4, 2, 14, 5, 16, 18, 11, 8, 7, 10, 13, 17, 0, 19, 1, 6, 3, 9],
        [10, 0, 18, 1, 16, 7, 8, 3, 13, 6, 15, 9, 19, 11, 14, 12, 2, 4, 5, 17],
        [7, 14, 0, 6, 12, 1, 11, 19, 8, 5, 3, 18, 2, 10, 13, 16, 4, 9, 15, 17],
        [0, 7, 5, 8, 14, 1, 4, 15, 12, 2, 3, 9, 10, 6, 18, 11, 16, 19, 13, 17],
        [6, 10, 14, 7, 11, 0, 19, 15, 4, 9, 5, 16, 8, 2, 1, 3, 18, 13, 17, 12],
        [12, 4, 1, 15, 19, 16, 17, 11, 6, 2, 13, 8, 18, 3, 0, 5, 14, 7, 10, 9],
        [1, 5, 10, 4, 9, 2, 16, 19, 7, 14, 3, 11, 17, 12, 13, 8, 15, 18, 0, 6],
        [18, 2, 7, 17, 14, 15, 4, 3, 11, 19, 9, 5, 12, 6, 8, 1, 16, 10, 0, 13],
        [5, 15, 11, 14, 12, 13, 18, 9, 19, 2, 16, 6, 4, 3, 1, 0, 7, 8, 17, 10],
        [16, 19, 0, 12, 18, 15, 1, 7, 14, 9, 11, 13, 5, 2, 4, 17, 6, 8, 10, 3],
        [10, 19, 16, 7, 6, 4, 15, 3, 13, 11, 8, 17, 18, 1, 14, 2, 9, 5, 0, 12],
        [1, 3, 17, 18, 5, 11, 14, 9, 16, 12, 19, 13, 2, 4, 0, 6, 8, 7, 10, 15],
        [8, 11, 15, 2, 3, 10, 18, 6, 5, 17, 12, 19, 7, 16, 9, 1, 0, 4, 14, 13],
        [10, 18, 8, 13, 15, 19, 4, 9, 6, 16, 0, 5, 2, 17, 1, 12, 11, 7, 14, 3],
        [13, 12, 7, 6, 15, 16, 11, 2, 9, 19, 18, 17, 14, 5, 0, 1, 4, 3, 8, 10],
        [12, 2, 1, 5, 3, 14, 8, 17, 10, 13, 9, 11, 19, 18, 7, 4, 6, 0, 15, 16],
        [18, 5, 17, 1, 12, 14, 7, 10, 6, 19, 4, 9, 0, 16, 11, 15, 3, 8, 13, 2],
        [19, 15, 4, 7, 8, 9, 6, 0, 10, 3, 18, 13, 1, 17, 16, 2, 11, 14, 12, 5],
        [5, 15, 16, 9, 17, 1, 7, 13, 6, 0, 18, 11, 12, 4, 10, 19, 14, 3, 8, 2],
        [17, 8, 5, 0, 13, 16, 2, 1, 19, 18, 14, 4, 3, 12, 15, 7, 10, 6, 9, 11],
        [12, 14, 19, 2, 5, 9, 17, 7, 3, 0, 18, 1, 13, 16, 8, 10, 11, 4, 6, 15],
        [5, 3, 10, 1, 14, 11, 16, 12, 0, 4, 19, 17, 6, 7, 13, 8, 2, 18, 9, 15],
        [3, 6, 13, 18, 2, 19, 5, 15, 11, 1, 14, 17, 10, 4, 16, 8, 9, 0, 7, 12],
        [14, 11, 0, 12, 17, 1, 19, 7, 15, 13, 18, 4, 3, 2, 8, 10, 9, 5, 6, 16],
        [7, 6, 19, 12, 4, 0, 8, 14, 9, 10, 1, 15, 11, 17, 5, 18, 2, 3, 13, 16],
        [6, 14, 5, 0, 3, 17, 12, 16, 9, 2, 13, 1, 8, 4, 7, 11, 19, 15, 18, 10],
        [16, 8, 4, 1, 13, 0, 11, 17, 12, 3, 15, 19, 18, 14, 6, 2, 9, 7, 5, 10],
        [9, 0, 16, 10, 19, 3, 4, 5, 12, 6, 17, 1, 2, 7, 11, 18, 15, 14, 8, 13],
        [9, 5, 1, 8, 2, 0, 11, 14, 19, 4, 7, 18, 10, 15, 12, 17, 13, 16, 6, 3],
        [10, 11, 14, 7, 13, 15, 9, 5, 1, 2, 4, 16, 3, 19, 8, 18, 0, 17, 12, 6],
        [12, 16, 9, 3, 13, 18, 1, 5, 10, 7, 17, 2, 8, 4, 11, 0, 15, 6, 19, 14],
        [0, 18, 16, 9, 13, 1, 10, 7, 3, 5, 12, 2, 6, 4, 19, 15, 11, 8, 17, 14],
        [3, 11, 18, 12, 15, 17, 0, 19, 4, 13, 16, 7, 9, 2, 6, 14, 10, 5, 8, 1],
        [13, 6, 16, 10, 1, 9, 0, 7, 18, 8, 3, 11, 15, 5, 2, 14, 17, 12, 4, 19],
        [3, 6, 12, 15, 14, 7, 10, 13, 17, 16, 1, 2, 4, 0, 8, 18, 5, 11, 9, 19],
        [6, 2, 19, 5, 12, 9, 10, 11, 16, 17, 13, 0, 1, 18, 4, 14, 8, 3, 7, 15],
        [3, 19, 18, 10, 4, 5, 0, 17, 9, 13, 16, 1, 12, 8, 7, 6, 14, 15, 2, 11],
        [8, 16, 9, 7, 10, 15, 3, 4, 18, 17, 6, 19, 2, 14, 1, 5, 12, 13, 0, 11],
        [9, 4, 7, 12, 6, 13, 15, 17, 1, 5, 11, 2, 14, 3, 19, 8, 0, 10, 18, 16],
        [4, 1, 7, 19, 17, 0, 9, 18, 16, 10, 3, 12, 2, 14, 6, 15, 13, 11, 5, 8],
        [15, 2, 19, 14, 16, 9, 1, 13, 10, 18, 17, 5, 0, 4, 11, 7, 3, 8, 12, 6],
        [16, 14, 10, 12, 13, 7, 8, 9, 18, 17, 5, 4, 19, 11, 2, 0, 6, 3, 1, 15],
        [11, 14, 0, 6, 2, 9, 15, 5, 12, 10, 16, 3, 7, 4, 19, 18, 13, 17, 8, 1],
        [13, 7, 11, 0, 1, 19, 9, 17, 8, 12, 18, 2, 14, 16, 3, 4, 15, 10, 6, 5],
    ],
    'durations': [
        # Job 0
        [Interval(28, 36), Interval(13, 13), Interval(28, 36), Interval(45, 57), Interval(71, 77),
         Interval(71, 75), Interval(42, 54), Interval(12, 14), Interval(6, 6), Interval(57, 61),
         Interval(32, 34), Interval(16, 20), Interval(77, 93), Interval(12, 14), Interval(53, 61),
         Interval(78, 86), Interval(61, 81), Interval(29, 35), Interval(74, 76), Interval(43, 57)],
        # Job 1
        [Interval(6, 6), Interval(58, 70), Interval(29, 39), Interval(52, 68), Interval(49, 49),
         Interval(3, 3), Interval(53, 65), Interval(40, 54), Interval(13, 17), Interval(66, 88),
         Interval(23, 25), Interval(77, 79), Interval(64, 78), Interval(19, 19), Interval(59, 71),
         Interval(75, 101), Interval(22, 24), Interval(2, 2), Interval(32, 32), Interval(5, 5)],
        # Job 2
        [Interval(68, 70), Interval(25, 27), Interval(27, 33), Interval(84, 96), Interval(40, 46),
         Interval(16, 18), Interval(20, 26), Interval(60, 64), Interval(15, 19), Interval(4, 4),
         Interval(17, 19), Interval(62, 78), Interval(18, 20), Interval(13, 17), Interval(15, 19),
         Interval(83, 85), Interval(51, 57), Interval(16, 18), Interval(55, 55), Interval(71, 91)],
        # Job 3
        [Interval(23, 23), Interval(7, 7), Interval(45, 53), Interval(84, 104), Interval(73, 77),
         Interval(48, 64), Interval(91, 93), Interval(55, 61), Interval(29, 35), Interval(75, 101),
         Interval(35, 43), Interval(56, 62), Interval(12, 14), Interval(12, 16), Interval(45, 53),
         Interval(50, 56), Interval(16, 20), Interval(13, 13), Interval(49, 63), Interval(33, 37)],
        # Job 4
        [Interval(11, 11), Interval(53, 65), Interval(74, 80), Interval(19, 21), Interval(53, 67),
         Interval(29, 37), Interval(15, 17), Interval(12, 14), Interval(62, 82), Interval(31, 39),
         Interval(35, 37), Interval(88, 96), Interval(31, 31), Interval(88, 96), Interval(51, 55),
         Interval(79, 99), Interval(67, 73), Interval(18, 24), Interval(32, 42), Interval(12, 12)],
        # Job 5
        [Interval(64, 74), Interval(51, 59), Interval(22, 24), Interval(73, 89), Interval(42, 44),
         Interval(62, 62), Interval(17, 17), Interval(90, 100), Interval(34, 44), Interval(28, 30),
         Interval(18, 24), Interval(84, 106), Interval(61, 63), Interval(35, 47), Interval(64, 84),
         Interval(64, 86), Interval(7, 7), Interval(94, 104), Interval(55, 61), Interval(7, 9)],
        # Job 6
        [Interval(11, 11), Interval(79, 89), Interval(15, 19), Interval(81, 93), Interval(43, 47),
         Interval(58, 78), Interval(10, 10), Interval(9, 11), Interval(13, 15), Interval(83, 89),
         Interval(83, 97), Interval(86, 102), Interval(8, 10), Interval(71, 81), Interval(68, 82),
         Interval(57, 67), Interval(58, 64), Interval(22, 24), Interval(82, 110), Interval(85, 113)],
        # Job 7
        [Interval(86, 90), Interval(81, 87), Interval(38, 44), Interval(78, 84), Interval(4, 4),
         Interval(6, 6), Interval(63, 81), Interval(85, 111), Interval(66, 74), Interval(23, 31),
         Interval(8, 10), Interval(40, 50), Interval(51, 51), Interval(72, 96), Interval(87, 97),
         Interval(36, 46), Interval(20, 20), Interval(17, 21), Interval(55, 69), Interval(28, 30)],
        # Job 8
        [Interval(48, 56), Interval(23, 27), Interval(6, 6), Interval(79, 103), Interval(12, 12),
         Interval(68, 90), Interval(25, 27), Interval(71, 89), Interval(6, 6), Interval(15, 17),
         Interval(76, 92), Interval(30, 36), Interval(12, 14), Interval(60, 68), Interval(58, 64),
         Interval(39, 43), Interval(70, 84), Interval(29, 33), Interval(70, 78), Interval(67, 67)],
        # Job 9
        [Interval(51, 69), Interval(89, 101), Interval(19, 21), Interval(96, 102), Interval(30, 30),
         Interval(47, 49), Interval(11, 11), Interval(52, 58), Interval(7, 7), Interval(50, 60),
         Interval(16, 18), Interval(71, 87), Interval(18, 18), Interval(51, 67), Interval(20, 24),
         Interval(26, 26), Interval(30, 40), Interval(1, 1), Interval(24, 26), Interval(35, 45)],
        # Job 10
        [Interval(18, 24), Interval(12, 16), Interval(56, 70), Interval(59, 67), Interval(78, 100),
         Interval(18, 20), Interval(78, 90), Interval(78, 92), Interval(24, 28), Interval(67, 89),
         Interval(48, 58), Interval(93, 103), Interval(22, 24), Interval(76, 92), Interval(51, 55),
         Interval(44, 50), Interval(2, 2), Interval(91, 105), Interval(54, 62), Interval(57, 67)],
        # Job 11
        [Interval(17, 17), Interval(52, 52), Interval(11, 13), Interval(53, 67), Interval(18, 24),
         Interval(9, 11), Interval(16, 20), Interval(26, 34), Interval(57, 57), Interval(56, 74),
         Interval(27, 35), Interval(16, 20), Interval(95, 95), Interval(80, 96), Interval(37, 45),
         Interval(83, 101), Interval(69, 81), Interval(16, 20), Interval(87, 87), Interval(49, 63)],
        # Job 12
        [Interval(33, 39), Interval(6, 6), Interval(83, 103), Interval(54, 60), Interval(28, 28),
         Interval(9, 9), Interval(85, 101), Interval(17, 19), Interval(33, 43), Interval(50, 56),
         Interval(86, 90), Interval(91, 107), Interval(10, 12), Interval(75, 97), Interval(70, 80),
         Interval(74, 100), Interval(16, 16), Interval(25, 33), Interval(9, 9), Interval(47, 59)],
        # Job 13
        [Interval(69, 71), Interval(51, 67), Interval(30, 36), Interval(7, 9), Interval(70, 90),
         Interval(8, 8), Interval(58, 58), Interval(84, 110), Interval(92, 100), Interval(45, 49),
         Interval(32, 40), Interval(25, 33), Interval(1, 1), Interval(12, 14), Interval(17, 17),
         Interval(32, 36), Interval(30, 38), Interval(33, 35), Interval(65, 65), Interval(7, 7)],
        # Job 14
        [Interval(54, 70), Interval(31, 35), Interval(40, 50), Interval(4, 4), Interval(17, 23),
         Interval(12, 16), Interval(24, 24), Interval(82, 86), Interval(56, 60), Interval(87, 93),
         Interval(92, 98), Interval(42, 50), Interval(53, 67), Interval(11, 11), Interval(27, 31),
         Interval(38, 40), Interval(21, 27), Interval(19, 25), Interval(84, 102), Interval(58, 58)],
        # Job 15
        [Interval(29, 31), Interval(49, 49), Interval(86, 100), Interval(79, 85), Interval(67, 67),
         Interval(22, 28), Interval(60, 66), Interval(89, 109), Interval(5, 5), Interval(85, 101),
         Interval(62, 82), Interval(13, 13), Interval(15, 19), Interval(64, 82), Interval(5, 5),
         Interval(36, 42), Interval(17, 23), Interval(26, 28), Interval(48, 52), Interval(61, 73)],
        # Job 16
        [Interval(96, 102), Interval(22, 22), Interval(83, 105), Interval(67, 73), Interval(66, 72),
         Interval(35, 47), Interval(40, 52), Interval(85, 91), Interval(85, 89), Interval(10, 12),
         Interval(50, 60), Interval(50, 52), Interval(56, 56), Interval(32, 32), Interval(26, 32),
         Interval(6, 6), Interval(95, 99), Interval(47, 61), Interval(92, 92), Interval(75, 93)],
        # Job 17
        [Interval(89, 95), Interval(25, 33), Interval(53, 63), Interval(85, 97), Interval(16, 20),
         Interval(15, 15), Interval(21, 23), Interval(69, 89), Interval(18, 18), Interval(83, 107),
         Interval(13, 15), Interval(65, 67), Interval(47, 47), Interval(66, 74), Interval(85, 95),
         Interval(56, 64), Interval(68, 90), Interval(6, 6), Interval(57, 63), Interval(54, 60)],
        # Job 18
        [Interval(8, 8), Interval(60, 68), Interval(83, 111), Interval(20, 20), Interval(17, 17),
         Interval(2, 2), Interval(58, 72), Interval(87, 97), Interval(28, 30), Interval(23, 31),
         Interval(53, 71), Interval(43, 55), Interval(93, 97), Interval(5, 5), Interval(80, 106),
         Interval(33, 43), Interval(76, 88), Interval(40, 42), Interval(43, 43), Interval(16, 16)],
        # Job 19
        [Interval(14, 16), Interval(10, 12), Interval(29, 37), Interval(71, 95), Interval(72, 84),
         Interval(28, 36), Interval(17, 21), Interval(51, 53), Interval(78, 94), Interval(20, 20),
         Interval(7, 9), Interval(22, 22), Interval(40, 44), Interval(70, 90), Interval(53, 69),
         Interval(75, 77), Interval(13, 17), Interval(86, 86), Interval(13, 17), Interval(73, 73)],
        # Job 20
        [Interval(47, 49), Interval(24, 32), Interval(32, 42), Interval(12, 12), Interval(52, 70),
         Interval(83, 95), Interval(27, 35), Interval(79, 101), Interval(88, 96), Interval(50, 54),
         Interval(95, 103), Interval(46, 56), Interval(45, 51), Interval(84, 112), Interval(97, 101),
         Interval(47, 47), Interval(90, 106), Interval(16, 18), Interval(28, 36), Interval(68, 72)],
        # Job 21
        [Interval(78, 78), Interval(28, 36), Interval(65, 67), Interval(33, 35), Interval(51, 65),
         Interval(6, 6), Interval(93, 93), Interval(17, 21), Interval(97, 97), Interval(42, 42),
         Interval(25, 29), Interval(20, 24), Interval(15, 17), Interval(82, 102), Interval(36, 46),
         Interval(87, 87), Interval(31, 33), Interval(46, 52), Interval(1, 1), Interval(10, 10)],
        # Job 22
        [Interval(94, 104), Interval(50, 64), Interval(74, 80), Interval(44, 52), Interval(30, 36),
         Interval(52, 66), Interval(44, 58), Interval(86, 96), Interval(74, 76), Interval(22, 26),
         Interval(15, 15), Interval(16, 16), Interval(56, 56), Interval(68, 92), Interval(36, 48),
         Interval(65, 73), Interval(65, 81), Interval(85, 87), Interval(84, 86), Interval(58, 58)],
        # Job 23
        [Interval(65, 79), Interval(61, 61), Interval(23, 29), Interval(58, 66), Interval(14, 16),
         Interval(44, 44), Interval(3, 3), Interval(6, 8), Interval(67, 89), Interval(51, 61),
         Interval(90, 90), Interval(75, 93), Interval(29, 39), Interval(13, 13), Interval(89, 101),
         Interval(54, 68), Interval(51, 53), Interval(76, 76), Interval(19, 25), Interval(35, 47)],
        # Job 24
        [Interval(21, 27), Interval(14, 18), Interval(12, 14), Interval(77, 99), Interval(92, 92),
         Interval(16, 18), Interval(25, 29), Interval(20, 26), Interval(9, 11), Interval(85, 91),
         Interval(78, 98), Interval(41, 45), Interval(68, 72), Interval(64, 84), Interval(72, 96),
         Interval(5, 5), Interval(33, 39), Interval(62, 80), Interval(66, 70), Interval(68, 70)],
        # Job 25
        [Interval(50, 66), Interval(63, 77), Interval(23, 29), Interval(56, 62), Interval(19, 19),
         Interval(78, 96), Interval(55, 55), Interval(12, 12), Interval(48, 50), Interval(35, 47),
         Interval(80, 94), Interval(48, 56), Interval(74, 96), Interval(34, 44), Interval(37, 39),
         Interval(18, 24), Interval(46, 52), Interval(16, 16), Interval(7, 9), Interval(75, 95)],
        # Job 26
        [Interval(43, 53), Interval(35, 45), Interval(60, 70), Interval(92, 92), Interval(10, 12),
         Interval(28, 30), Interval(65, 71), Interval(62, 78), Interval(20, 22), Interval(47, 51),
         Interval(38, 46), Interval(57, 77), Interval(40, 40), Interval(6, 6), Interval(37, 41),
         Interval(26, 32), Interval(39, 43), Interval(81, 83), Interval(93, 93), Interval(18, 20)],
        # Job 27
        [Interval(52, 56), Interval(58, 74), Interval(18, 18), Interval(46, 62), Interval(84, 86),
         Interval(38, 46), Interval(30, 40), Interval(49, 61), Interval(56, 60), Interval(29, 37),
         Interval(47, 57), Interval(27, 29), Interval(31, 31), Interval(85, 109), Interval(45, 57),
         Interval(13, 15), Interval(89, 109), Interval(45, 55), Interval(14, 14), Interval(29, 33)],
        # Job 28
        [Interval(73, 81), Interval(10, 12), Interval(60, 62), Interval(39, 49), Interval(18, 22),
         Interval(36, 42), Interval(19, 23), Interval(71, 89), Interval(3, 3), Interval(43, 45),
         Interval(13, 13), Interval(73, 73), Interval(93, 99), Interval(67, 71), Interval(5, 5),
         Interval(2, 2), Interval(72, 74), Interval(68, 80), Interval(28, 32), Interval(36, 48)],
        # Job 29
        [Interval(82, 104), Interval(78, 92), Interval(71, 75), Interval(70, 82), Interval(32, 34),
         Interval(90, 96), Interval(84, 112), Interval(79, 89), Interval(78, 88), Interval(53, 55),
         Interval(14, 16), Interval(15, 19), Interval(31, 35), Interval(73, 91), Interval(49, 55),
         Interval(64, 80), Interval(37, 37), Interval(92, 98), Interval(41, 49), Interval(50, 50)],
        # Job 30
        [Interval(72, 92), Interval(43, 51), Interval(92, 94), Interval(35, 47), Interval(20, 26),
         Interval(89, 107), Interval(11, 13), Interval(51, 53), Interval(67, 89), Interval(10, 12),
         Interval(2, 2), Interval(22, 28), Interval(2, 2), Interval(37, 41), Interval(68, 90),
         Interval(88, 104), Interval(32, 34), Interval(78, 84), Interval(74, 74), Interval(36, 44)],
        # Job 31
        [Interval(61, 71), Interval(34, 38), Interval(11, 13), Interval(81, 95), Interval(83, 83),
         Interval(4, 4), Interval(74, 94), Interval(67, 69), Interval(27, 27), Interval(62, 68),
         Interval(88, 92), Interval(67, 79), Interval(1, 1), Interval(41, 47), Interval(27, 27),
         Interval(89, 103), Interval(67, 79), Interval(12, 12), Interval(25, 29), Interval(20, 24)],
        # Job 32
        [Interval(1, 1), Interval(37, 45), Interval(52, 54), Interval(29, 29), Interval(73, 77),
         Interval(17, 17), Interval(46, 60), Interval(82, 84), Interval(57, 67), Interval(82, 104),
         Interval(5, 5), Interval(83, 105), Interval(24, 26), Interval(56, 74), Interval(65, 71),
         Interval(40, 48), Interval(14, 18), Interval(48, 48), Interval(58, 58), Interval(6, 8)],
        # Job 33
        [Interval(8, 10), Interval(15, 15), Interval(39, 45), Interval(28, 36), Interval(48, 54),
         Interval(63, 85), Interval(58, 58), Interval(23, 29), Interval(44, 58), Interval(23, 27),
         Interval(8, 10), Interval(49, 55), Interval(76, 98), Interval(23, 23), Interval(65, 75),
         Interval(54, 62), Interval(12, 16), Interval(44, 54), Interval(50, 52), Interval(49, 59)],
        # Job 34
        [Interval(73, 97), Interval(13, 15), Interval(7, 9), Interval(7, 9), Interval(50, 50),
         Interval(86, 102), Interval(11, 11), Interval(77, 97), Interval(40, 48), Interval(33, 37),
         Interval(69, 69), Interval(57, 67), Interval(30, 40), Interval(51, 59), Interval(77, 77),
         Interval(80, 104), Interval(80, 98), Interval(18, 22), Interval(60, 70), Interval(13, 13)],
        # Job 35
        [Interval(73, 87), Interval(72, 86), Interval(30, 34), Interval(32, 38), Interval(64, 70),
         Interval(39, 49), Interval(37, 37), Interval(6, 8), Interval(90, 96), Interval(72, 74),
         Interval(6, 6), Interval(74, 80), Interval(74, 80), Interval(80, 88), Interval(12, 12),
         Interval(42, 54), Interval(48, 54), Interval(67, 79), Interval(84, 94), Interval(26, 28)],
        # Job 36
        [Interval(65, 65), Interval(1, 1), Interval(27, 31), Interval(57, 63), Interval(52, 58),
         Interval(46, 48), Interval(59, 79), Interval(77, 99), Interval(59, 65), Interval(21, 23),
         Interval(43, 45), Interval(3, 3), Interval(50, 62), Interval(67, 83), Interval(70, 90),
         Interval(1, 1), Interval(65, 65), Interval(71, 81), Interval(4, 4), Interval(60, 72)],
        # Job 37
        [Interval(3, 3), Interval(6, 6), Interval(60, 62), Interval(56, 68), Interval(53, 55),
         Interval(78, 92), Interval(23, 29), Interval(4, 4), Interval(27, 27), Interval(51, 57),
         Interval(76, 92), Interval(3, 3), Interval(2, 2), Interval(12, 12), Interval(39, 49),
         Interval(86, 92), Interval(72, 90), Interval(15, 17), Interval(77, 81), Interval(62, 74)],
        # Job 38
        [Interval(15, 15), Interval(31, 37), Interval(60, 80), Interval(79, 101), Interval(41, 53),
         Interval(65, 79), Interval(22, 28), Interval(49, 65), Interval(20, 20), Interval(78, 82),
         Interval(77, 99), Interval(39, 49), Interval(70, 86), Interval(78, 80), Interval(52, 54),
         Interval(36, 48), Interval(58, 70), Interval(72, 96), Interval(15, 15), Interval(41, 43)],
        # Job 39
        [Interval(25, 33), Interval(47, 61), Interval(11, 11), Interval(87, 99), Interval(2, 2),
         Interval(84, 88), Interval(71, 91), Interval(22, 24), Interval(94, 104), Interval(48, 50),
         Interval(96, 100), Interval(75, 81), Interval(13, 15), Interval(22, 28), Interval(68, 80),
         Interval(82, 106), Interval(91, 91), Interval(31, 33), Interval(5, 5), Interval(66, 72)],
        # Job 40
        [Interval(22, 24), Interval(90, 98), Interval(52, 70), Interval(39, 39), Interval(8, 8),
         Interval(70, 72), Interval(90, 96), Interval(70, 74), Interval(54, 56), Interval(83, 107),
         Interval(11, 13), Interval(52, 68), Interval(77, 87), Interval(44, 48), Interval(82, 82),
         Interval(7, 7), Interval(49, 61), Interval(35, 41), Interval(81, 91), Interval(30, 40)],
        # Job 41
        [Interval(40, 50), Interval(54, 58), Interval(9, 11), Interval(45, 53), Interval(67, 87),
         Interval(42, 44), Interval(7, 9), Interval(61, 71), Interval(30, 32), Interval(74, 74),
         Interval(80, 106), Interval(44, 54), Interval(53, 61), Interval(23, 23), Interval(26, 26),
         Interval(92, 102), Interval(88, 100), Interval(67, 75), Interval(23, 23), Interval(94, 100)],
        # Job 42
        [Interval(52, 60), Interval(86, 94), Interval(61, 81), Interval(47, 53), Interval(27, 31),
         Interval(55, 71), Interval(1, 1), Interval(62, 76), Interval(83, 111), Interval(84, 86),
         Interval(40, 44), Interval(19, 21), Interval(19, 21), Interval(3, 3), Interval(37, 49),
         Interval(82, 90), Interval(91, 103), Interval(20, 24), Interval(49, 55), Interval(21, 21)],
        # Job 43
        [Interval(70, 92), Interval(11, 13), Interval(62, 80), Interval(39, 39), Interval(85, 113),
         Interval(66, 74), Interval(32, 38), Interval(73, 95), Interval(19, 25), Interval(40, 54),
         Interval(63, 65), Interval(89, 107), Interval(6, 8), Interval(12, 12), Interval(74, 76),
         Interval(58, 70), Interval(83, 89), Interval(25, 29), Interval(37, 39), Interval(10, 10)],
        # Job 44
        [Interval(34, 36), Interval(6, 6), Interval(80, 102), Interval(15, 17), Interval(43, 49),
         Interval(74, 84), Interval(53, 57), Interval(95, 97), Interval(79, 93), Interval(42, 48),
         Interval(38, 48), Interval(5, 5), Interval(88, 102), Interval(13, 15), Interval(28, 32),
         Interval(4, 4), Interval(36, 40), Interval(78, 104), Interval(8, 10), Interval(40, 48)],
        # Job 45
        [Interval(17, 23), Interval(57, 73), Interval(16, 20), Interval(21, 21), Interval(13, 13),
         Interval(71, 77), Interval(38, 50), Interval(35, 43), Interval(90, 104), Interval(21, 27),
         Interval(29, 37), Interval(13, 15), Interval(43, 43), Interval(16, 18), Interval(80, 80),
         Interval(64, 82), Interval(36, 42), Interval(6, 6), Interval(13, 15), Interval(42, 44)],
        # Job 46
        [Interval(57, 65), Interval(81, 85), Interval(44, 48), Interval(64, 78), Interval(23, 27),
         Interval(8, 8), Interval(79, 83), Interval(52, 68), Interval(12, 16), Interval(29, 31),
         Interval(9, 11), Interval(1, 1), Interval(55, 67), Interval(48, 58), Interval(17, 23),
         Interval(19, 19), Interval(13, 17), Interval(12, 12), Interval(9, 11), Interval(34, 36)],
        # Job 47
        [Interval(31, 41), Interval(8, 8), Interval(78, 78), Interval(32, 32), Interval(93, 93),
         Interval(28, 34), Interval(11, 11), Interval(40, 42), Interval(12, 12), Interval(9, 11),
         Interval(45, 53), Interval(19, 19), Interval(91, 107), Interval(71, 75), Interval(91, 99),
         Interval(34, 42), Interval(80, 86), Interval(11, 11), Interval(22, 28), Interval(32, 42)],
        # Job 48
        [Interval(34, 40), Interval(90, 90), Interval(79, 81), Interval(25, 27), Interval(39, 45),
         Interval(30, 38), Interval(57, 77), Interval(56, 62), Interval(81, 81), Interval(66, 82),
         Interval(16, 18), Interval(37, 45), Interval(24, 30), Interval(63, 81), Interval(32, 42),
         Interval(71, 93), Interval(67, 89), Interval(75, 77), Interval(51, 67), Interval(13, 15)],
        # Job 49
        [Interval(41, 53), Interval(1, 1), Interval(10, 10), Interval(76, 100), Interval(37, 39),
         Interval(80, 86), Interval(73, 93), Interval(97, 101), Interval(1, 1), Interval(28, 28),
         Interval(60, 62), Interval(59, 65), Interval(70, 82), Interval(42, 44), Interval(29, 29),
         Interval(74, 92), Interval(94, 100), Interval(51, 69), Interval(28, 30), Interval(71, 75)],
    ],
    'name': 'INT__TAI50_20_05.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai50_20_05_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI50_20_05.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI50_20_05.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI50_20_05_F_15_01_INTERVAL_DATA
