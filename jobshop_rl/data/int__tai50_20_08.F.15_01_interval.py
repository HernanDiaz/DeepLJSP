"""
Problema INT__TAI50_20_08.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI50_20_08_F_15_01_INTERVAL_DATA = {
    'num_jobs': 50,
    'num_machines': 20,
    'problem_id': 'int__tai50_20_08.F.15_01_interval',
    'sequences': [
        [4, 3, 18, 17, 12, 13, 14, 6, 7, 11, 1, 5, 16, 8, 9, 15, 10, 0, 19, 2],
        [13, 5, 14, 18, 1, 19, 11, 6, 3, 7, 2, 8, 4, 10, 15, 12, 17, 9, 0, 16],
        [5, 3, 18, 15, 11, 19, 12, 1, 6, 17, 4, 13, 14, 0, 9, 8, 10, 7, 2, 16],
        [13, 9, 6, 0, 7, 8, 1, 3, 15, 10, 5, 18, 2, 16, 4, 19, 11, 12, 17, 14],
        [1, 11, 19, 18, 0, 8, 4, 7, 5, 2, 6, 13, 15, 16, 9, 17, 10, 14, 12, 3],
        [5, 9, 6, 13, 8, 17, 10, 19, 18, 4, 14, 11, 3, 12, 2, 16, 15, 1, 0, 7],
        [8, 0, 4, 15, 2, 14, 18, 16, 11, 17, 6, 7, 5, 3, 13, 9, 10, 1, 19, 12],
        [5, 13, 1, 6, 17, 8, 0, 7, 10, 16, 15, 12, 2, 19, 14, 18, 11, 9, 4, 3],
        [16, 15, 18, 2, 14, 0, 12, 6, 3, 11, 9, 17, 19, 13, 5, 8, 7, 1, 4, 10],
        [18, 12, 9, 5, 11, 6, 19, 14, 1, 4, 17, 16, 3, 8, 13, 15, 10, 2, 7, 0],
        [2, 3, 13, 0, 9, 7, 19, 17, 8, 1, 14, 18, 6, 16, 5, 15, 12, 10, 4, 11],
        [7, 14, 16, 5, 19, 8, 1, 3, 11, 0, 17, 15, 2, 9, 18, 13, 10, 12, 6, 4],
        [10, 17, 11, 9, 19, 1, 15, 4, 18, 14, 7, 16, 12, 2, 5, 0, 13, 8, 6, 3],
        [8, 2, 17, 19, 10, 14, 13, 16, 12, 11, 6, 18, 3, 9, 5, 0, 4, 7, 1, 15],
        [10, 11, 7, 18, 17, 14, 16, 1, 9, 8, 2, 12, 3, 19, 15, 5, 4, 0, 13, 6],
        [5, 11, 9, 18, 12, 8, 2, 14, 1, 15, 7, 6, 16, 0, 4, 10, 19, 17, 3, 13],
        [12, 7, 16, 5, 6, 15, 17, 0, 13, 8, 19, 10, 2, 4, 18, 14, 9, 3, 1, 11],
        [9, 4, 17, 14, 10, 0, 18, 2, 13, 16, 6, 19, 12, 8, 3, 7, 11, 1, 15, 5],
        [5, 13, 1, 14, 0, 6, 19, 3, 7, 10, 9, 4, 11, 18, 17, 2, 15, 16, 8, 12],
        [4, 0, 13, 2, 1, 3, 15, 12, 11, 6, 9, 18, 5, 8, 19, 16, 17, 14, 7, 10],
        [10, 1, 15, 17, 9, 6, 18, 4, 19, 7, 13, 5, 3, 11, 0, 14, 8, 12, 2, 16],
        [10, 11, 13, 7, 4, 17, 3, 9, 19, 14, 6, 2, 15, 16, 12, 18, 8, 5, 1, 0],
        [7, 4, 5, 12, 9, 13, 3, 17, 11, 16, 8, 19, 10, 14, 18, 6, 15, 0, 2, 1],
        [18, 6, 19, 9, 17, 10, 14, 15, 16, 0, 11, 5, 13, 7, 2, 3, 12, 1, 8, 4],
        [6, 15, 7, 14, 5, 8, 2, 9, 17, 11, 19, 12, 10, 1, 18, 16, 13, 3, 0, 4],
        [9, 4, 7, 18, 5, 1, 13, 10, 15, 3, 2, 19, 12, 11, 17, 14, 0, 6, 16, 8],
        [16, 19, 13, 18, 1, 3, 9, 8, 12, 11, 10, 0, 15, 7, 2, 5, 4, 6, 17, 14],
        [7, 4, 17, 12, 15, 1, 3, 5, 11, 14, 8, 13, 19, 10, 18, 6, 9, 16, 2, 0],
        [16, 8, 12, 19, 18, 7, 4, 13, 6, 14, 17, 3, 10, 1, 9, 11, 0, 2, 15, 5],
        [14, 4, 12, 19, 17, 9, 18, 8, 5, 13, 6, 2, 10, 15, 1, 11, 3, 0, 7, 16],
        [15, 8, 17, 9, 19, 18, 10, 0, 5, 7, 6, 13, 12, 3, 4, 11, 1, 14, 16, 2],
        [16, 9, 12, 13, 6, 5, 11, 18, 17, 4, 10, 0, 3, 15, 1, 7, 8, 14, 19, 2],
        [16, 10, 7, 15, 9, 3, 14, 5, 1, 11, 12, 18, 2, 19, 4, 0, 17, 6, 8, 13],
        [10, 6, 18, 14, 2, 7, 17, 8, 5, 1, 4, 15, 12, 3, 11, 13, 9, 0, 19, 16],
        [16, 3, 2, 11, 7, 14, 9, 15, 1, 6, 10, 18, 0, 19, 5, 13, 8, 17, 12, 4],
        [4, 13, 3, 15, 19, 10, 18, 11, 14, 16, 1, 2, 9, 6, 5, 7, 8, 12, 17, 0],
        [4, 3, 18, 2, 0, 17, 14, 8, 15, 13, 9, 16, 1, 5, 19, 11, 10, 7, 12, 6],
        [12, 14, 5, 2, 3, 9, 7, 11, 13, 10, 4, 18, 0, 15, 1, 16, 8, 17, 19, 6],
        [13, 0, 11, 8, 18, 17, 10, 19, 16, 15, 6, 1, 5, 4, 14, 2, 12, 9, 3, 7],
        [3, 0, 13, 8, 5, 1, 7, 4, 17, 11, 10, 12, 2, 19, 16, 9, 14, 6, 15, 18],
        [7, 19, 15, 5, 3, 1, 12, 11, 4, 0, 8, 16, 17, 2, 10, 18, 9, 6, 14, 13],
        [9, 19, 8, 3, 17, 10, 16, 13, 11, 14, 0, 15, 1, 12, 7, 4, 2, 6, 18, 5],
        [19, 13, 11, 6, 2, 12, 7, 14, 0, 15, 8, 17, 16, 18, 1, 3, 5, 9, 10, 4],
        [8, 10, 17, 16, 18, 9, 15, 1, 5, 6, 2, 3, 7, 0, 19, 12, 11, 13, 4, 14],
        [11, 8, 10, 7, 0, 15, 5, 17, 19, 18, 16, 2, 3, 14, 6, 9, 1, 13, 4, 12],
        [11, 14, 13, 1, 9, 5, 7, 18, 4, 2, 19, 15, 0, 17, 12, 6, 16, 10, 3, 8],
        [6, 15, 19, 16, 5, 12, 11, 4, 0, 2, 3, 8, 10, 7, 1, 17, 14, 18, 9, 13],
        [12, 15, 14, 3, 1, 2, 9, 11, 16, 6, 10, 17, 8, 18, 4, 13, 0, 5, 19, 7],
        [6, 9, 10, 11, 12, 18, 0, 4, 1, 2, 13, 8, 16, 7, 3, 14, 5, 19, 15, 17],
        [3, 2, 8, 19, 15, 13, 6, 4, 14, 16, 10, 5, 17, 7, 11, 18, 1, 9, 12, 0],
    ],
    'durations': [
        # Job 0
        [Interval(7, 9), Interval(41, 41), Interval(4, 4), Interval(46, 58), Interval(41, 53),
         Interval(64, 70), Interval(63, 67), Interval(16, 20), Interval(64, 82), Interval(10, 10),
         Interval(66, 74), Interval(60, 72), Interval(58, 70), Interval(46, 60), Interval(31, 37),
         Interval(27, 29), Interval(63, 85), Interval(35, 45), Interval(8, 8), Interval(26, 34)],
        # Job 1
        [Interval(33, 41), Interval(80, 102), Interval(85, 109), Interval(6, 6), Interval(48, 48),
         Interval(81, 99), Interval(28, 36), Interval(11, 13), Interval(80, 106), Interval(14, 16),
         Interval(33, 33), Interval(5, 5), Interval(2, 2), Interval(10, 12), Interval(92, 100),
         Interval(14, 18), Interval(70, 94), Interval(47, 51), Interval(48, 48), Interval(80, 82)],
        # Job 2
        [Interval(11, 11), Interval(62, 78), Interval(4, 4), Interval(86, 98), Interval(17, 19),
         Interval(39, 43), Interval(66, 88), Interval(5, 5), Interval(47, 51), Interval(80, 108),
         Interval(30, 34), Interval(59, 75), Interval(2, 2), Interval(15, 17), Interval(18, 24),
         Interval(62, 76), Interval(88, 90), Interval(31, 33), Interval(6, 6), Interval(31, 35)],
        # Job 3
        [Interval(86, 88), Interval(3, 3), Interval(72, 92), Interval(43, 45), Interval(16, 16),
         Interval(49, 59), Interval(8, 10), Interval(48, 50), Interval(24, 32), Interval(69, 71),
         Interval(81, 89), Interval(30, 38), Interval(46, 60), Interval(33, 41), Interval(56, 62),
         Interval(57, 75), Interval(35, 47), Interval(88, 104), Interval(79, 89), Interval(47, 61)],
        # Job 4
        [Interval(1, 1), Interval(29, 33), Interval(64, 82), Interval(33, 37), Interval(76, 86),
         Interval(75, 93), Interval(33, 35), Interval(50, 56), Interval(65, 81), Interval(26, 34),
         Interval(59, 67), Interval(69, 83), Interval(53, 71), Interval(12, 16), Interval(30, 30),
         Interval(30, 32), Interval(87, 91), Interval(27, 29), Interval(88, 96), Interval(3, 3)],
        # Job 5
        [Interval(57, 71), Interval(44, 48), Interval(71, 91), Interval(33, 43), Interval(46, 46),
         Interval(64, 74), Interval(10, 10), Interval(25, 29), Interval(33, 39), Interval(92, 96),
         Interval(53, 53), Interval(31, 31), Interval(14, 16), Interval(51, 67), Interval(30, 32),
         Interval(6, 6), Interval(1, 1), Interval(24, 32), Interval(38, 48), Interval(90, 94)],
        # Job 6
        [Interval(23, 31), Interval(68, 88), Interval(9, 11), Interval(19, 19), Interval(84, 94),
         Interval(86, 96), Interval(39, 45), Interval(13, 13), Interval(70, 80), Interval(2, 2),
         Interval(32, 40), Interval(13, 15), Interval(57, 61), Interval(12, 16), Interval(9, 9),
         Interval(30, 38), Interval(3, 3), Interval(79, 91), Interval(43, 45), Interval(87, 101)],
        # Job 7
        [Interval(7, 9), Interval(82, 98), Interval(36, 40), Interval(21, 25), Interval(63, 75),
         Interval(33, 35), Interval(13, 13), Interval(53, 71), Interval(33, 43), Interval(72, 76),
         Interval(65, 69), Interval(42, 48), Interval(60, 64), Interval(28, 36), Interval(75, 97),
         Interval(56, 62), Interval(73, 95), Interval(57, 75), Interval(33, 41), Interval(52, 52)],
        # Job 8
        [Interval(39, 51), Interval(29, 31), Interval(20, 26), Interval(7, 7), Interval(80, 104),
         Interval(64, 80), Interval(33, 35), Interval(58, 68), Interval(63, 73), Interval(31, 41),
         Interval(74, 76), Interval(9, 11), Interval(26, 28), Interval(80, 98), Interval(29, 33),
         Interval(80, 96), Interval(41, 51), Interval(31, 41), Interval(66, 76), Interval(22, 24)],
        # Job 9
        [Interval(68, 76), Interval(33, 39), Interval(5, 5), Interval(91, 105), Interval(36, 40),
         Interval(99, 99), Interval(79, 105), Interval(87, 97), Interval(60, 66), Interval(20, 20),
         Interval(42, 42), Interval(75, 79), Interval(71, 71), Interval(3, 3), Interval(75, 85),
         Interval(90, 100), Interval(77, 91), Interval(31, 33), Interval(29, 35), Interval(66, 66)],
        # Job 10
        [Interval(54, 72), Interval(14, 16), Interval(66, 66), Interval(14, 18), Interval(48, 54),
         Interval(23, 29), Interval(21, 27), Interval(68, 88), Interval(48, 60), Interval(62, 70),
         Interval(45, 57), Interval(28, 32), Interval(35, 39), Interval(66, 78), Interval(70, 84),
         Interval(10, 12), Interval(30, 36), Interval(29, 31), Interval(34, 38), Interval(22, 26)],
        # Job 11
        [Interval(74, 82), Interval(71, 79), Interval(33, 37), Interval(10, 10), Interval(74, 88),
         Interval(1, 1), Interval(27, 29), Interval(58, 58), Interval(68, 92), Interval(54, 68),
         Interval(46, 58), Interval(67, 81), Interval(15, 19), Interval(10, 12), Interval(63, 65),
         Interval(59, 79), Interval(23, 31), Interval(81, 103), Interval(79, 79), Interval(81, 97)],
        # Job 12
        [Interval(23, 27), Interval(17, 21), Interval(49, 57), Interval(32, 40), Interval(53, 53),
         Interval(23, 31), Interval(7, 9), Interval(21, 25), Interval(81, 91), Interval(31, 31),
         Interval(2, 2), Interval(91, 99), Interval(49, 57), Interval(27, 31), Interval(30, 40),
         Interval(26, 30), Interval(1, 1), Interval(70, 72), Interval(52, 62), Interval(49, 63)],
        # Job 13
        [Interval(10, 12), Interval(52, 60), Interval(55, 73), Interval(45, 45), Interval(83, 109),
         Interval(92, 96), Interval(42, 54), Interval(78, 80), Interval(41, 55), Interval(52, 64),
         Interval(30, 34), Interval(51, 65), Interval(13, 13), Interval(95, 95), Interval(34, 44),
         Interval(20, 22), Interval(18, 18), Interval(74, 92), Interval(40, 50), Interval(63, 75)],
        # Job 14
        [Interval(88, 88), Interval(24, 26), Interval(8, 10), Interval(80, 86), Interval(12, 12),
         Interval(76, 82), Interval(35, 47), Interval(82, 96), Interval(82, 104), Interval(41, 51),
         Interval(21, 27), Interval(41, 41), Interval(58, 60), Interval(54, 58), Interval(19, 19),
         Interval(12, 12), Interval(31, 37), Interval(70, 90), Interval(78, 84), Interval(48, 54)],
        # Job 15
        [Interval(21, 23), Interval(42, 56), Interval(63, 83), Interval(53, 65), Interval(48, 48),
         Interval(72, 80), Interval(78, 78), Interval(64, 74), Interval(64, 68), Interval(27, 27),
         Interval(64, 82), Interval(44, 48), Interval(37, 47), Interval(49, 57), Interval(53, 71),
         Interval(37, 41), Interval(13, 17), Interval(4, 4), Interval(66, 86), Interval(48, 58)],
        # Job 16
        [Interval(83, 109), Interval(88, 94), Interval(67, 75), Interval(54, 66), Interval(58, 62),
         Interval(58, 62), Interval(39, 49), Interval(17, 19), Interval(78, 86), Interval(78, 102),
         Interval(67, 87), Interval(90, 96), Interval(24, 24), Interval(6, 6), Interval(71, 83),
         Interval(51, 61), Interval(80, 84), Interval(15, 15), Interval(85, 85), Interval(37, 45)],
        # Job 17
        [Interval(4, 4), Interval(8, 8), Interval(9, 11), Interval(4, 4), Interval(23, 23),
         Interval(15, 19), Interval(32, 34), Interval(43, 57), Interval(22, 26), Interval(12, 12),
         Interval(25, 33), Interval(65, 65), Interval(40, 46), Interval(59, 77), Interval(64, 68),
         Interval(71, 93), Interval(21, 23), Interval(87, 91), Interval(57, 59), Interval(24, 26)],
        # Job 18
        [Interval(4, 4), Interval(13, 15), Interval(58, 66), Interval(37, 49), Interval(47, 51),
         Interval(17, 19), Interval(86, 96), Interval(78, 88), Interval(46, 60), Interval(35, 35),
         Interval(78, 80), Interval(55, 69), Interval(40, 44), Interval(16, 18), Interval(53, 71),
         Interval(34, 44), Interval(67, 85), Interval(42, 44), Interval(8, 10), Interval(34, 44)],
        # Job 19
        [Interval(1, 1), Interval(91, 105), Interval(75, 79), Interval(28, 28), Interval(3, 3),
         Interval(8, 8), Interval(41, 45), Interval(46, 60), Interval(4, 4), Interval(70, 90),
         Interval(69, 93), Interval(90, 106), Interval(53, 69), Interval(80, 102), Interval(32, 32),
         Interval(59, 71), Interval(52, 52), Interval(25, 33), Interval(48, 50), Interval(1, 1)],
        # Job 20
        [Interval(38, 42), Interval(78, 100), Interval(57, 73), Interval(30, 30), Interval(20, 26),
         Interval(47, 47), Interval(83, 111), Interval(28, 28), Interval(3, 3), Interval(5, 5),
         Interval(4, 4), Interval(83, 87), Interval(29, 39), Interval(21, 27), Interval(86, 88),
         Interval(54, 72), Interval(51, 57), Interval(47, 61), Interval(23, 31), Interval(91, 99)],
        # Job 21
        [Interval(48, 52), Interval(23, 25), Interval(33, 41), Interval(93, 105), Interval(12, 16),
         Interval(97, 101), Interval(25, 25), Interval(59, 69), Interval(68, 78), Interval(56, 72),
         Interval(24, 24), Interval(86, 86), Interval(9, 11), Interval(75, 77), Interval(54, 58),
         Interval(71, 91), Interval(62, 62), Interval(42, 56), Interval(19, 19), Interval(78, 78)],
        # Job 22
        [Interval(68, 78), Interval(68, 84), Interval(30, 32), Interval(4, 4), Interval(9, 11),
         Interval(21, 27), Interval(67, 67), Interval(55, 59), Interval(24, 26), Interval(72, 72),
         Interval(29, 31), Interval(27, 35), Interval(76, 82), Interval(12, 14), Interval(36, 46),
         Interval(74, 96), Interval(69, 89), Interval(58, 64), Interval(45, 45), Interval(3, 3)],
        # Job 23
        [Interval(67, 77), Interval(49, 49), Interval(50, 50), Interval(95, 95), Interval(69, 93),
         Interval(69, 91), Interval(47, 53), Interval(36, 46), Interval(47, 49), Interval(67, 69),
         Interval(15, 15), Interval(26, 32), Interval(68, 68), Interval(73, 93), Interval(68, 76),
         Interval(24, 26), Interval(56, 56), Interval(17, 21), Interval(68, 92), Interval(55, 65)],
        # Job 24
        [Interval(68, 68), Interval(27, 33), Interval(33, 43), Interval(23, 23), Interval(5, 5),
         Interval(61, 69), Interval(1, 1), Interval(16, 20), Interval(60, 62), Interval(51, 51),
         Interval(38, 50), Interval(55, 73), Interval(86, 110), Interval(85, 113), Interval(55, 73),
         Interval(76, 98), Interval(90, 90), Interval(63, 69), Interval(92, 106), Interval(6, 8)],
        # Job 25
        [Interval(80, 108), Interval(58, 62), Interval(17, 21), Interval(38, 42), Interval(45, 47),
         Interval(6, 8), Interval(6, 8), Interval(78, 94), Interval(28, 36), Interval(3, 3),
         Interval(25, 25), Interval(88, 90), Interval(51, 67), Interval(62, 76), Interval(78, 100),
         Interval(61, 69), Interval(9, 9), Interval(69, 85), Interval(35, 35), Interval(41, 43)],
        # Job 26
        [Interval(90, 96), Interval(71, 95), Interval(73, 85), Interval(33, 39), Interval(13, 17),
         Interval(38, 50), Interval(43, 47), Interval(10, 12), Interval(44, 50), Interval(2, 2),
         Interval(82, 86), Interval(45, 57), Interval(23, 29), Interval(56, 68), Interval(47, 61),
         Interval(65, 77), Interval(86, 86), Interval(55, 73), Interval(59, 63), Interval(37, 39)],
        # Job 27
        [Interval(78, 98), Interval(35, 39), Interval(35, 39), Interval(33, 39), Interval(51, 67),
         Interval(14, 14), Interval(84, 94), Interval(84, 102), Interval(6, 6), Interval(45, 49),
         Interval(44, 44), Interval(1, 1), Interval(82, 82), Interval(78, 90), Interval(49, 51),
         Interval(18, 24), Interval(4, 4), Interval(19, 21), Interval(84, 112), Interval(37, 37)],
        # Job 28
        [Interval(59, 71), Interval(4, 4), Interval(84, 112), Interval(26, 32), Interval(22, 22),
         Interval(1, 1), Interval(60, 80), Interval(80, 98), Interval(70, 76), Interval(5, 5),
         Interval(15, 15), Interval(29, 37), Interval(20, 26), Interval(60, 66), Interval(18, 22),
         Interval(25, 31), Interval(31, 31), Interval(58, 66), Interval(85, 95), Interval(46, 60)],
        # Job 29
        [Interval(5, 5), Interval(50, 52), Interval(80, 100), Interval(81, 101), Interval(22, 26),
         Interval(90, 106), Interval(28, 34), Interval(87, 93), Interval(3, 3), Interval(53, 59),
         Interval(5, 5), Interval(41, 41), Interval(73, 77), Interval(55, 59), Interval(48, 50),
         Interval(69, 81), Interval(1, 1), Interval(62, 70), Interval(56, 74), Interval(51, 65)],
        # Job 30
        [Interval(78, 92), Interval(42, 44), Interval(87, 103), Interval(40, 44), Interval(49, 51),
         Interval(28, 36), Interval(35, 39), Interval(8, 8), Interval(67, 69), Interval(78, 86),
         Interval(69, 87), Interval(11, 11), Interval(41, 49), Interval(30, 34), Interval(58, 74),
         Interval(41, 41), Interval(52, 54), Interval(82, 100), Interval(65, 65), Interval(77, 99)],
        # Job 31
        [Interval(79, 95), Interval(16, 16), Interval(37, 49), Interval(75, 97), Interval(61, 73),
         Interval(73, 91), Interval(69, 71), Interval(56, 74), Interval(48, 64), Interval(46, 60),
         Interval(21, 23), Interval(15, 19), Interval(86, 102), Interval(58, 64), Interval(67, 71),
         Interval(73, 73), Interval(30, 36), Interval(64, 74), Interval(34, 38), Interval(58, 70)],
        # Job 32
        [Interval(79, 91), Interval(6, 6), Interval(31, 31), Interval(20, 26), Interval(33, 33),
         Interval(4, 4), Interval(68, 70), Interval(58, 64), Interval(49, 51), Interval(24, 30),
         Interval(23, 27), Interval(10, 10), Interval(24, 28), Interval(24, 28), Interval(42, 42),
         Interval(9, 9), Interval(65, 79), Interval(27, 33), Interval(89, 93), Interval(83, 83)],
        # Job 33
        [Interval(43, 45), Interval(74, 80), Interval(44, 58), Interval(48, 50), Interval(34, 40),
         Interval(17, 23), Interval(61, 77), Interval(91, 99), Interval(72, 96), Interval(41, 45),
         Interval(77, 95), Interval(77, 95), Interval(57, 57), Interval(29, 29), Interval(65, 75),
         Interval(82, 106), Interval(38, 38), Interval(36, 42), Interval(52, 70), Interval(57, 63)],
        # Job 34
        [Interval(32, 42), Interval(22, 22), Interval(48, 64), Interval(75, 101), Interval(86, 104),
         Interval(18, 20), Interval(86, 98), Interval(56, 72), Interval(25, 25), Interval(64, 74),
         Interval(35, 39), Interval(8, 10), Interval(73, 91), Interval(65, 69), Interval(82, 98),
         Interval(45, 59), Interval(60, 68), Interval(22, 28), Interval(53, 71), Interval(39, 39)],
        # Job 35
        [Interval(62, 74), Interval(34, 38), Interval(76, 94), Interval(33, 41), Interval(62, 70),
         Interval(31, 31), Interval(32, 38), Interval(83, 111), Interval(70, 82), Interval(22, 22),
         Interval(39, 51), Interval(72, 88), Interval(81, 99), Interval(44, 52), Interval(5, 5),
         Interval(52, 60), Interval(46, 54), Interval(60, 72), Interval(50, 58), Interval(49, 57)],
        # Job 36
        [Interval(82, 90), Interval(18, 24), Interval(36, 36), Interval(36, 48), Interval(65, 69),
         Interval(38, 38), Interval(27, 29), Interval(56, 60), Interval(39, 43), Interval(1, 1),
         Interval(67, 67), Interval(40, 50), Interval(24, 26), Interval(17, 19), Interval(12, 12),
         Interval(67, 75), Interval(49, 49), Interval(26, 30), Interval(20, 22), Interval(50, 54)],
        # Job 37
        [Interval(91, 95), Interval(83, 111), Interval(31, 39), Interval(68, 74), Interval(58, 66),
         Interval(48, 50), Interval(73, 89), Interval(54, 66), Interval(57, 71), Interval(50, 50),
         Interval(31, 35), Interval(36, 42), Interval(7, 7), Interval(40, 48), Interval(52, 54),
         Interval(18, 22), Interval(82, 110), Interval(49, 49), Interval(22, 24), Interval(63, 77)],
        # Job 38
        [Interval(15, 15), Interval(20, 24), Interval(39, 41), Interval(11, 13), Interval(18, 20),
         Interval(5, 5), Interval(31, 33), Interval(78, 92), Interval(47, 49), Interval(43, 49),
         Interval(84, 110), Interval(4, 4), Interval(85, 109), Interval(84, 106), Interval(82, 98),
         Interval(2, 2), Interval(59, 79), Interval(81, 109), Interval(67, 69), Interval(18, 18)],
        # Job 39
        [Interval(46, 58), Interval(51, 63), Interval(60, 74), Interval(66, 68), Interval(88, 94),
         Interval(71, 93), Interval(77, 95), Interval(25, 33), Interval(8, 8), Interval(34, 36),
         Interval(57, 73), Interval(12, 14), Interval(90, 94), Interval(26, 30), Interval(75, 79),
         Interval(87, 111), Interval(28, 32), Interval(15, 17), Interval(31, 31), Interval(34, 36)],
        # Job 40
        [Interval(81, 89), Interval(23, 25), Interval(51, 69), Interval(55, 65), Interval(77, 101),
         Interval(99, 99), Interval(84, 92), Interval(14, 16), Interval(43, 47), Interval(58, 62),
         Interval(33, 43), Interval(43, 45), Interval(37, 39), Interval(4, 4), Interval(93, 97),
         Interval(26, 28), Interval(26, 28), Interval(15, 15), Interval(66, 86), Interval(46, 60)],
        # Job 41
        [Interval(13, 17), Interval(61, 67), Interval(27, 31), Interval(72, 72), Interval(94, 102),
         Interval(65, 81), Interval(26, 30), Interval(24, 26), Interval(30, 40), Interval(51, 63),
         Interval(25, 27), Interval(35, 41), Interval(39, 45), Interval(17, 21), Interval(73, 77),
         Interval(2, 2), Interval(79, 93), Interval(43, 49), Interval(80, 88), Interval(5, 5)],
        # Job 42
        [Interval(57, 57), Interval(4, 4), Interval(71, 95), Interval(12, 14), Interval(74, 86),
         Interval(44, 46), Interval(6, 6), Interval(46, 46), Interval(60, 66), Interval(88, 100),
         Interval(51, 57), Interval(68, 70), Interval(67, 71), Interval(40, 46), Interval(59, 65),
         Interval(6, 6), Interval(13, 17), Interval(33, 37), Interval(58, 66), Interval(39, 49)],
        # Job 43
        [Interval(52, 62), Interval(57, 77), Interval(79, 81), Interval(77, 83), Interval(59, 63),
         Interval(78, 90), Interval(78, 102), Interval(60, 66), Interval(25, 27), Interval(90, 106),
         Interval(88, 100), Interval(92, 92), Interval(73, 95), Interval(14, 18), Interval(21, 27),
         Interval(66, 68), Interval(40, 54), Interval(33, 37), Interval(72, 86), Interval(87, 111)],
        # Job 44
        [Interval(54, 72), Interval(39, 51), Interval(48, 50), Interval(35, 41), Interval(29, 35),
         Interval(82, 92), Interval(41, 41), Interval(30, 36), Interval(18, 18), Interval(38, 42),
         Interval(48, 52), Interval(83, 85), Interval(35, 37), Interval(87, 111), Interval(73, 81),
         Interval(15, 17), Interval(49, 55), Interval(19, 21), Interval(59, 61), Interval(61, 71)],
        # Job 45
        [Interval(1, 1), Interval(22, 26), Interval(33, 41), Interval(50, 58), Interval(36, 42),
         Interval(47, 53), Interval(36, 40), Interval(68, 90), Interval(80, 96), Interval(32, 38),
         Interval(51, 65), Interval(67, 87), Interval(38, 48), Interval(96, 100), Interval(49, 55),
         Interval(70, 76), Interval(39, 51), Interval(40, 50), Interval(78, 90), Interval(69, 91)],
        # Job 46
        [Interval(23, 29), Interval(9, 9), Interval(92, 92), Interval(67, 73), Interval(87, 87),
         Interval(29, 37), Interval(13, 15), Interval(79, 87), Interval(33, 35), Interval(92, 104),
         Interval(5, 5), Interval(97, 101), Interval(88, 98), Interval(84, 104), Interval(38, 48),
         Interval(36, 36), Interval(26, 26), Interval(10, 12), Interval(25, 31), Interval(16, 16)],
        # Job 47
        [Interval(17, 21), Interval(53, 63), Interval(27, 33), Interval(64, 80), Interval(38, 40),
         Interval(23, 31), Interval(18, 18), Interval(39, 49), Interval(19, 21), Interval(74, 100),
         Interval(80, 84), Interval(51, 51), Interval(77, 79), Interval(20, 20), Interval(18, 20),
         Interval(34, 38), Interval(41, 43), Interval(75, 75), Interval(75, 95), Interval(88, 102)],
        # Job 48
        [Interval(40, 42), Interval(42, 50), Interval(79, 83), Interval(17, 17), Interval(23, 27),
         Interval(77, 83), Interval(40, 42), Interval(25, 33), Interval(86, 112), Interval(13, 15),
         Interval(28, 28), Interval(25, 25), Interval(54, 62), Interval(22, 26), Interval(53, 65),
         Interval(39, 51), Interval(16, 18), Interval(53, 53), Interval(14, 18), Interval(79, 93)],
        # Job 49
        [Interval(27, 33), Interval(3, 3), Interval(25, 31), Interval(81, 103), Interval(74, 100),
         Interval(24, 32), Interval(26, 34), Interval(68, 70), Interval(17, 23), Interval(87, 101),
         Interval(85, 109), Interval(88, 94), Interval(5, 5), Interval(14, 18), Interval(85, 91),
         Interval(46, 48), Interval(58, 74), Interval(66, 68), Interval(15, 15), Interval(29, 29)],
    ],
    'name': 'INT__TAI50_20_08.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai50_20_08_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI50_20_08.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI50_20_08.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI50_20_08_F_15_01_INTERVAL_DATA
