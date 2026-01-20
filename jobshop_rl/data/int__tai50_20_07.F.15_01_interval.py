"""
Problema INT__TAI50_20_07.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI50_20_07_F_15_01_INTERVAL_DATA = {
    'num_jobs': 50,
    'num_machines': 20,
    'problem_id': 'int__tai50_20_07.F.15_01_interval',
    'sequences': [
        [15, 2, 17, 11, 3, 19, 5, 14, 7, 10, 18, 1, 12, 9, 13, 4, 6, 16, 0, 8],
        [10, 18, 14, 1, 9, 6, 5, 16, 11, 19, 0, 4, 3, 2, 15, 17, 7, 13, 8, 12],
        [16, 12, 8, 3, 6, 9, 18, 19, 4, 10, 13, 11, 5, 14, 15, 1, 0, 17, 2, 7],
        [8, 12, 6, 19, 4, 5, 14, 2, 11, 16, 18, 10, 0, 17, 9, 13, 1, 7, 15, 3],
        [18, 16, 17, 3, 8, 14, 15, 5, 1, 9, 19, 13, 11, 0, 2, 6, 4, 12, 10, 7],
        [7, 3, 12, 16, 10, 18, 6, 4, 9, 19, 15, 11, 0, 17, 2, 5, 14, 13, 8, 1],
        [18, 19, 7, 5, 10, 16, 15, 6, 13, 17, 1, 2, 14, 12, 3, 9, 4, 8, 11, 0],
        [15, 13, 8, 19, 6, 11, 3, 0, 18, 9, 16, 1, 2, 12, 7, 4, 14, 10, 5, 17],
        [1, 0, 18, 6, 17, 16, 5, 13, 10, 15, 9, 19, 4, 12, 14, 2, 3, 8, 7, 11],
        [18, 2, 17, 0, 5, 1, 13, 9, 10, 11, 7, 6, 12, 14, 3, 15, 8, 16, 4, 19],
        [10, 1, 5, 3, 19, 2, 4, 18, 15, 13, 6, 12, 9, 0, 7, 8, 11, 14, 17, 16],
        [11, 14, 6, 2, 9, 4, 0, 1, 8, 7, 18, 13, 19, 15, 16, 17, 3, 5, 12, 10],
        [16, 0, 13, 11, 2, 8, 5, 9, 4, 7, 15, 14, 18, 10, 12, 19, 3, 6, 1, 17],
        [7, 0, 13, 5, 14, 9, 3, 15, 4, 8, 11, 12, 19, 17, 16, 2, 1, 6, 10, 18],
        [3, 11, 10, 6, 8, 5, 17, 9, 14, 12, 2, 16, 18, 7, 1, 15, 19, 4, 13, 0],
        [13, 14, 17, 11, 16, 5, 2, 3, 6, 1, 18, 9, 15, 12, 0, 4, 19, 8, 10, 7],
        [8, 13, 10, 7, 9, 12, 2, 14, 6, 18, 11, 1, 4, 19, 17, 3, 0, 16, 5, 15],
        [7, 16, 2, 6, 3, 5, 1, 0, 9, 13, 14, 12, 18, 4, 10, 11, 15, 19, 17, 8],
        [17, 7, 1, 16, 18, 9, 10, 11, 6, 2, 15, 5, 3, 19, 14, 12, 4, 13, 8, 0],
        [12, 6, 16, 11, 8, 14, 0, 19, 1, 2, 10, 3, 18, 17, 7, 9, 13, 5, 15, 4],
        [13, 3, 7, 1, 6, 19, 16, 11, 14, 17, 2, 18, 4, 10, 8, 15, 0, 5, 9, 12],
        [1, 12, 18, 5, 19, 2, 14, 17, 10, 3, 9, 4, 13, 11, 0, 6, 15, 7, 8, 16],
        [6, 4, 8, 11, 17, 13, 5, 12, 1, 9, 15, 10, 2, 0, 19, 3, 16, 18, 14, 7],
        [4, 7, 5, 19, 12, 9, 15, 1, 17, 6, 16, 18, 14, 0, 13, 3, 10, 11, 2, 8],
        [10, 2, 0, 13, 4, 16, 12, 1, 7, 15, 5, 9, 3, 6, 18, 14, 17, 8, 11, 19],
        [11, 14, 7, 16, 3, 10, 6, 13, 4, 2, 0, 15, 5, 18, 1, 9, 17, 8, 12, 19],
        [4, 16, 8, 3, 0, 17, 5, 12, 2, 7, 9, 18, 14, 10, 13, 19, 11, 6, 1, 15],
        [16, 5, 7, 10, 8, 17, 14, 0, 13, 18, 15, 12, 1, 6, 11, 19, 2, 4, 9, 3],
        [12, 8, 7, 17, 2, 4, 9, 18, 1, 5, 10, 13, 11, 19, 0, 15, 14, 16, 6, 3],
        [15, 3, 16, 19, 6, 11, 8, 0, 12, 5, 9, 4, 18, 1, 7, 13, 2, 10, 17, 14],
        [13, 9, 1, 0, 8, 11, 5, 10, 17, 18, 16, 2, 14, 19, 4, 3, 7, 6, 12, 15],
        [11, 16, 4, 17, 18, 6, 3, 13, 12, 19, 14, 15, 1, 7, 0, 5, 9, 10, 8, 2],
        [1, 3, 9, 0, 5, 17, 8, 7, 13, 11, 18, 10, 16, 4, 6, 2, 12, 19, 15, 14],
        [15, 0, 10, 4, 2, 8, 6, 12, 13, 7, 18, 3, 16, 11, 14, 5, 19, 17, 1, 9],
        [7, 3, 13, 1, 12, 2, 9, 15, 8, 14, 6, 10, 11, 4, 0, 18, 5, 16, 17, 19],
        [18, 6, 3, 9, 10, 13, 12, 5, 7, 19, 15, 1, 8, 17, 11, 4, 0, 14, 2, 16],
        [15, 13, 4, 0, 2, 10, 3, 8, 19, 9, 17, 11, 18, 6, 1, 7, 5, 16, 12, 14],
        [7, 19, 18, 16, 8, 12, 4, 6, 0, 14, 9, 2, 15, 5, 3, 1, 13, 10, 11, 17],
        [17, 7, 19, 16, 2, 13, 18, 11, 0, 1, 3, 10, 15, 6, 9, 4, 8, 12, 14, 5],
        [9, 18, 2, 4, 1, 10, 17, 5, 0, 8, 3, 15, 12, 6, 16, 11, 19, 7, 14, 13],
        [7, 18, 1, 9, 5, 13, 16, 11, 19, 14, 2, 15, 3, 17, 8, 12, 6, 4, 0, 10],
        [5, 4, 10, 16, 7, 1, 2, 11, 0, 13, 8, 14, 6, 19, 3, 18, 9, 17, 15, 12],
        [2, 13, 10, 6, 1, 15, 18, 7, 12, 19, 11, 3, 5, 16, 0, 14, 8, 17, 4, 9],
        [2, 13, 17, 0, 19, 7, 12, 6, 10, 3, 1, 18, 4, 11, 16, 8, 14, 5, 15, 9],
        [7, 5, 14, 16, 1, 17, 15, 6, 8, 12, 4, 18, 2, 11, 19, 10, 0, 9, 13, 3],
        [11, 16, 2, 7, 19, 3, 14, 4, 6, 8, 5, 17, 10, 15, 12, 13, 9, 1, 0, 18],
        [2, 15, 4, 18, 3, 12, 6, 9, 19, 8, 5, 0, 13, 10, 7, 11, 14, 16, 17, 1],
        [18, 17, 19, 1, 3, 14, 13, 15, 8, 0, 5, 7, 10, 12, 4, 11, 9, 6, 2, 16],
        [17, 4, 6, 16, 15, 11, 12, 8, 10, 1, 2, 3, 7, 13, 14, 5, 0, 9, 18, 19],
        [7, 15, 6, 3, 12, 9, 8, 0, 2, 18, 17, 11, 10, 16, 5, 4, 13, 14, 1, 19],
    ],
    'durations': [
        # Job 0
        [Interval(32, 42), Interval(64, 64), Interval(13, 17), Interval(46, 58), Interval(68, 74),
         Interval(37, 39), Interval(47, 59), Interval(61, 79), Interval(73, 79), Interval(72, 80),
         Interval(55, 67), Interval(9, 11), Interval(44, 58), Interval(55, 63), Interval(12, 12),
         Interval(63, 85), Interval(54, 68), Interval(51, 53), Interval(58, 78), Interval(17, 21)],
        # Job 1
        [Interval(69, 89), Interval(62, 80), Interval(32, 32), Interval(16, 20), Interval(8, 10),
         Interval(85, 113), Interval(73, 97), Interval(89, 99), Interval(41, 41), Interval(1, 1),
         Interval(16, 20), Interval(94, 102), Interval(2, 2), Interval(42, 52), Interval(49, 65),
         Interval(42, 46), Interval(25, 25), Interval(47, 49), Interval(12, 12), Interval(22, 26)],
        # Job 2
        [Interval(47, 53), Interval(51, 59), Interval(24, 26), Interval(21, 27), Interval(42, 44),
         Interval(55, 73), Interval(37, 43), Interval(33, 41), Interval(28, 32), Interval(62, 80),
         Interval(58, 70), Interval(13, 13), Interval(32, 34), Interval(25, 27), Interval(42, 42),
         Interval(56, 72), Interval(54, 56), Interval(75, 77), Interval(16, 18), Interval(7, 9)],
        # Job 3
        [Interval(31, 31), Interval(19, 25), Interval(38, 38), Interval(9, 9), Interval(74, 94),
         Interval(58, 78), Interval(31, 39), Interval(89, 99), Interval(68, 90), Interval(68, 90),
         Interval(36, 44), Interval(37, 41), Interval(8, 10), Interval(34, 38), Interval(71, 93),
         Interval(37, 41), Interval(32, 34), Interval(38, 48), Interval(83, 89), Interval(69, 79)],
        # Job 4
        [Interval(15, 19), Interval(64, 82), Interval(52, 58), Interval(27, 33), Interval(24, 32),
         Interval(31, 39), Interval(71, 73), Interval(29, 31), Interval(49, 51), Interval(3, 3),
         Interval(80, 88), Interval(69, 75), Interval(4, 4), Interval(65, 81), Interval(51, 57),
         Interval(13, 17), Interval(55, 73), Interval(43, 43), Interval(9, 11), Interval(74, 86)],
        # Job 5
        [Interval(52, 58), Interval(12, 14), Interval(63, 65), Interval(94, 94), Interval(87, 91),
         Interval(20, 22), Interval(27, 35), Interval(80, 84), Interval(46, 62), Interval(14, 18),
         Interval(8, 8), Interval(85, 113), Interval(61, 79), Interval(19, 25), Interval(86, 92),
         Interval(62, 68), Interval(53, 59), Interval(85, 99), Interval(14, 16), Interval(72, 82)],
        # Job 6
        [Interval(36, 46), Interval(4, 4), Interval(39, 45), Interval(77, 85), Interval(70, 94),
         Interval(54, 58), Interval(70, 88), Interval(90, 104), Interval(45, 49), Interval(84, 98),
         Interval(44, 52), Interval(78, 94), Interval(26, 30), Interval(73, 87), Interval(82, 96),
         Interval(87, 95), Interval(43, 45), Interval(57, 77), Interval(57, 77), Interval(52, 54)],
        # Job 7
        [Interval(26, 28), Interval(89, 103), Interval(42, 44), Interval(20, 26), Interval(43, 57),
         Interval(73, 83), Interval(40, 52), Interval(12, 14), Interval(47, 61), Interval(20, 20),
         Interval(32, 42), Interval(21, 23), Interval(12, 14), Interval(53, 53), Interval(4, 4),
         Interval(46, 60), Interval(6, 8), Interval(52, 54), Interval(51, 61), Interval(4, 4)],
        # Job 8
        [Interval(26, 30), Interval(72, 94), Interval(62, 64), Interval(65, 87), Interval(2, 2),
         Interval(11, 11), Interval(14, 18), Interval(51, 59), Interval(71, 85), Interval(49, 61),
         Interval(66, 88), Interval(30, 34), Interval(26, 28), Interval(44, 48), Interval(16, 18),
         Interval(42, 48), Interval(38, 42), Interval(94, 94), Interval(9, 11), Interval(12, 12)],
        # Job 9
        [Interval(56, 62), Interval(79, 83), Interval(84, 86), Interval(84, 90), Interval(37, 37),
         Interval(29, 31), Interval(31, 33), Interval(9, 11), Interval(68, 76), Interval(89, 109),
         Interval(23, 23), Interval(28, 36), Interval(25, 29), Interval(32, 32), Interval(66, 88),
         Interval(6, 6), Interval(56, 64), Interval(74, 96), Interval(69, 89), Interval(57, 75)],
        # Job 10
        [Interval(79, 99), Interval(8, 8), Interval(75, 95), Interval(46, 52), Interval(50, 58),
         Interval(12, 14), Interval(30, 34), Interval(29, 37), Interval(48, 58), Interval(72, 80),
         Interval(79, 87), Interval(68, 82), Interval(28, 30), Interval(75, 83), Interval(61, 69),
         Interval(47, 53), Interval(34, 40), Interval(18, 18), Interval(36, 36), Interval(40, 52)],
        # Job 11
        [Interval(45, 57), Interval(5, 5), Interval(6, 6), Interval(56, 72), Interval(30, 36),
         Interval(12, 16), Interval(36, 48), Interval(12, 12), Interval(79, 105), Interval(59, 77),
         Interval(83, 105), Interval(29, 29), Interval(81, 97), Interval(36, 44), Interval(9, 11),
         Interval(39, 47), Interval(7, 9), Interval(82, 82), Interval(77, 99), Interval(79, 93)],
        # Job 12
        [Interval(6, 8), Interval(80, 90), Interval(12, 12), Interval(54, 58), Interval(55, 67),
         Interval(6, 6), Interval(71, 83), Interval(56, 72), Interval(37, 43), Interval(13, 13),
         Interval(79, 93), Interval(34, 42), Interval(77, 101), Interval(91, 105), Interval(36, 48),
         Interval(92, 94), Interval(75, 97), Interval(95, 99), Interval(29, 37), Interval(22, 22)],
        # Job 13
        [Interval(75, 97), Interval(41, 49), Interval(91, 107), Interval(70, 90), Interval(8, 8),
         Interval(76, 76), Interval(36, 48), Interval(14, 14), Interval(77, 85), Interval(76, 94),
         Interval(77, 99), Interval(15, 17), Interval(48, 48), Interval(22, 24), Interval(24, 30),
         Interval(47, 51), Interval(42, 42), Interval(5, 5), Interval(59, 63), Interval(23, 29)],
        # Job 14
        [Interval(33, 39), Interval(52, 68), Interval(70, 90), Interval(29, 39), Interval(30, 30),
         Interval(52, 54), Interval(88, 94), Interval(2, 2), Interval(86, 92), Interval(30, 32),
         Interval(55, 67), Interval(31, 39), Interval(66, 72), Interval(26, 30), Interval(16, 16),
         Interval(60, 80), Interval(75, 101), Interval(1, 1), Interval(87, 107), Interval(33, 33)],
        # Job 15
        [Interval(46, 50), Interval(21, 21), Interval(59, 69), Interval(48, 52), Interval(79, 79),
         Interval(23, 29), Interval(19, 21), Interval(10, 12), Interval(15, 17), Interval(3, 3),
         Interval(52, 70), Interval(27, 31), Interval(85, 109), Interval(58, 74), Interval(89, 107),
         Interval(44, 58), Interval(52, 56), Interval(48, 52), Interval(87, 105), Interval(32, 34)],
        # Job 16
        [Interval(59, 63), Interval(14, 18), Interval(29, 31), Interval(29, 31), Interval(83, 109),
         Interval(30, 40), Interval(19, 21), Interval(61, 65), Interval(56, 66), Interval(14, 16),
         Interval(44, 46), Interval(63, 63), Interval(66, 66), Interval(55, 67), Interval(69, 71),
         Interval(65, 85), Interval(89, 89), Interval(87, 107), Interval(17, 17), Interval(51, 69)],
        # Job 17
        [Interval(71, 85), Interval(38, 44), Interval(8, 10), Interval(8, 8), Interval(25, 27),
         Interval(60, 78), Interval(53, 57), Interval(26, 34), Interval(7, 7), Interval(27, 27),
         Interval(58, 60), Interval(31, 35), Interval(17, 19), Interval(72, 82), Interval(49, 65),
         Interval(85, 95), Interval(23, 25), Interval(39, 43), Interval(6, 6), Interval(67, 75)],
        # Job 18
        [Interval(52, 70), Interval(27, 27), Interval(46, 46), Interval(27, 33), Interval(44, 48),
         Interval(14, 16), Interval(21, 27), Interval(86, 112), Interval(39, 49), Interval(1, 1),
         Interval(16, 16), Interval(10, 12), Interval(13, 17), Interval(35, 41), Interval(52, 56),
         Interval(13, 13), Interval(72, 74), Interval(65, 71), Interval(73, 97), Interval(47, 61)],
        # Job 19
        [Interval(12, 16), Interval(31, 35), Interval(57, 73), Interval(85, 109), Interval(73, 75),
         Interval(50, 60), Interval(18, 18), Interval(65, 87), Interval(72, 76), Interval(67, 73),
         Interval(69, 87), Interval(13, 17), Interval(40, 40), Interval(19, 25), Interval(56, 56),
         Interval(58, 78), Interval(31, 31), Interval(52, 54), Interval(17, 21), Interval(77, 101)],
        # Job 20
        [Interval(60, 62), Interval(84, 110), Interval(86, 98), Interval(56, 72), Interval(78, 100),
         Interval(49, 53), Interval(65, 71), Interval(79, 87), Interval(19, 23), Interval(5, 5),
         Interval(5, 5), Interval(80, 90), Interval(57, 77), Interval(92, 96), Interval(96, 98),
         Interval(65, 77), Interval(36, 42), Interval(51, 65), Interval(29, 31), Interval(82, 82)],
        # Job 21
        [Interval(72, 92), Interval(20, 20), Interval(79, 85), Interval(12, 16), Interval(71, 71),
         Interval(79, 103), Interval(61, 61), Interval(19, 19), Interval(62, 72), Interval(70, 86),
         Interval(50, 56), Interval(50, 62), Interval(35, 45), Interval(51, 51), Interval(45, 47),
         Interval(89, 101), Interval(38, 38), Interval(12, 12), Interval(8, 10), Interval(87, 93)],
        # Job 22
        [Interval(89, 105), Interval(80, 100), Interval(29, 39), Interval(86, 112), Interval(27, 29),
         Interval(83, 85), Interval(60, 70), Interval(57, 57), Interval(29, 29), Interval(87, 87),
         Interval(12, 14), Interval(20, 26), Interval(48, 54), Interval(77, 99), Interval(36, 36),
         Interval(7, 7), Interval(34, 34), Interval(16, 20), Interval(59, 59), Interval(84, 108)],
        # Job 23
        [Interval(18, 20), Interval(79, 91), Interval(91, 91), Interval(27, 33), Interval(59, 79),
         Interval(2, 2), Interval(88, 104), Interval(21, 21), Interval(72, 90), Interval(28, 36),
         Interval(79, 79), Interval(43, 49), Interval(82, 102), Interval(86, 90), Interval(3, 3),
         Interval(20, 20), Interval(46, 60), Interval(18, 24), Interval(50, 64), Interval(17, 23)],
        # Job 24
        [Interval(8, 10), Interval(5, 5), Interval(44, 56), Interval(26, 26), Interval(64, 70),
         Interval(60, 68), Interval(29, 39), Interval(63, 83), Interval(28, 30), Interval(50, 62),
         Interval(7, 7), Interval(68, 72), Interval(47, 61), Interval(40, 54), Interval(74, 90),
         Interval(26, 34), Interval(17, 17), Interval(91, 93), Interval(2, 2), Interval(20, 26)],
        # Job 25
        [Interval(37, 45), Interval(70, 88), Interval(68, 76), Interval(86, 90), Interval(1, 1),
         Interval(58, 70), Interval(98, 100), Interval(32, 32), Interval(53, 57), Interval(68, 92),
         Interval(26, 30), Interval(80, 94), Interval(57, 73), Interval(31, 41), Interval(69, 75),
         Interval(5, 5), Interval(12, 14), Interval(52, 60), Interval(32, 32), Interval(63, 81)],
        # Job 26
        [Interval(49, 63), Interval(77, 93), Interval(46, 58), Interval(59, 69), Interval(60, 60),
         Interval(70, 92), Interval(43, 45), Interval(41, 45), Interval(8, 10), Interval(4, 4),
         Interval(58, 64), Interval(23, 25), Interval(57, 67), Interval(48, 64), Interval(17, 17),
         Interval(9, 9), Interval(26, 32), Interval(43, 47), Interval(62, 64), Interval(7, 7)],
        # Job 27
        [Interval(60, 68), Interval(66, 70), Interval(81, 107), Interval(44, 48), Interval(14, 18),
         Interval(10, 10), Interval(73, 89), Interval(17, 21), Interval(81, 101), Interval(73, 77),
         Interval(82, 108), Interval(19, 23), Interval(48, 52), Interval(81, 83), Interval(2, 2),
         Interval(64, 82), Interval(49, 61), Interval(88, 98), Interval(35, 43), Interval(31, 39)],
        # Job 28
        [Interval(69, 69), Interval(61, 69), Interval(24, 26), Interval(44, 58), Interval(28, 28),
         Interval(67, 85), Interval(1, 1), Interval(3, 3), Interval(6, 6), Interval(66, 82),
         Interval(10, 12), Interval(54, 64), Interval(81, 101), Interval(10, 10), Interval(33, 37),
         Interval(8, 8), Interval(26, 28), Interval(34, 36), Interval(28, 28), Interval(90, 104)],
        # Job 29
        [Interval(38, 44), Interval(39, 51), Interval(47, 59), Interval(12, 14), Interval(90, 94),
         Interval(52, 60), Interval(40, 44), Interval(47, 49), Interval(57, 77), Interval(91, 103),
         Interval(75, 85), Interval(56, 58), Interval(76, 84), Interval(9, 11), Interval(84, 96),
         Interval(24, 28), Interval(64, 72), Interval(31, 39), Interval(83, 85), Interval(96, 102)],
        # Job 30
        [Interval(39, 47), Interval(68, 68), Interval(24, 32), Interval(69, 83), Interval(32, 32),
         Interval(17, 23), Interval(77, 101), Interval(25, 31), Interval(41, 51), Interval(17, 17),
         Interval(35, 47), Interval(28, 36), Interval(32, 42), Interval(31, 33), Interval(41, 55),
         Interval(43, 51), Interval(31, 33), Interval(2, 2), Interval(26, 26), Interval(37, 37)],
        # Job 31
        [Interval(75, 91), Interval(7, 9), Interval(5, 5), Interval(23, 25), Interval(62, 76),
         Interval(64, 74), Interval(93, 93), Interval(47, 61), Interval(89, 91), Interval(15, 15),
         Interval(60, 66), Interval(70, 72), Interval(76, 92), Interval(72, 84), Interval(62, 62),
         Interval(78, 90), Interval(90, 108), Interval(81, 83), Interval(28, 32), Interval(46, 56)],
        # Job 32
        [Interval(62, 76), Interval(63, 65), Interval(75, 75), Interval(23, 23), Interval(89, 97),
         Interval(41, 55), Interval(11, 11), Interval(17, 19), Interval(78, 100), Interval(85, 107),
         Interval(68, 72), Interval(86, 112), Interval(50, 54), Interval(63, 77), Interval(21, 25),
         Interval(85, 85), Interval(50, 50), Interval(75, 87), Interval(15, 19), Interval(5, 5)],
        # Job 33
        [Interval(86, 88), Interval(51, 59), Interval(41, 55), Interval(80, 90), Interval(15, 19),
         Interval(79, 79), Interval(63, 83), Interval(17, 21), Interval(20, 24), Interval(34, 40),
         Interval(12, 12), Interval(17, 21), Interval(9, 9), Interval(5, 5), Interval(4, 4),
         Interval(79, 91), Interval(82, 94), Interval(41, 51), Interval(9, 11), Interval(4, 4)],
        # Job 34
        [Interval(83, 89), Interval(33, 39), Interval(78, 102), Interval(59, 67), Interval(41, 55),
         Interval(4, 4), Interval(13, 17), Interval(15, 15), Interval(14, 16), Interval(37, 41),
         Interval(65, 81), Interval(80, 98), Interval(54, 62), Interval(80, 80), Interval(65, 77),
         Interval(46, 62), Interval(23, 27), Interval(41, 41), Interval(73, 95), Interval(66, 80)],
        # Job 35
        [Interval(38, 46), Interval(44, 52), Interval(82, 94), Interval(65, 77), Interval(61, 75),
         Interval(24, 26), Interval(31, 35), Interval(84, 92), Interval(55, 69), Interval(51, 51),
         Interval(42, 56), Interval(74, 78), Interval(22, 22), Interval(45, 49), Interval(61, 65),
         Interval(58, 64), Interval(16, 16), Interval(9, 11), Interval(87, 101), Interval(43, 51)],
        # Job 36
        [Interval(31, 33), Interval(39, 43), Interval(99, 99), Interval(45, 51), Interval(79, 85),
         Interval(50, 54), Interval(45, 47), Interval(57, 77), Interval(55, 71), Interval(16, 16),
         Interval(23, 25), Interval(32, 32), Interval(79, 97), Interval(66, 82), Interval(12, 14),
         Interval(24, 24), Interval(76, 88), Interval(25, 31), Interval(72, 76), Interval(13, 15)],
        # Job 37
        [Interval(55, 57), Interval(55, 65), Interval(60, 80), Interval(93, 93), Interval(21, 23),
         Interval(56, 68), Interval(50, 50), Interval(2, 2), Interval(13, 17), Interval(96, 102),
         Interval(17, 23), Interval(41, 49), Interval(6, 6), Interval(79, 83), Interval(12, 14),
         Interval(50, 52), Interval(11, 13), Interval(11, 13), Interval(48, 62), Interval(31, 39)],
        # Job 38
        [Interval(42, 50), Interval(11, 13), Interval(79, 105), Interval(23, 23), Interval(97, 101),
         Interval(10, 12), Interval(89, 109), Interval(79, 97), Interval(22, 22), Interval(18, 18),
         Interval(25, 33), Interval(48, 58), Interval(48, 64), Interval(56, 56), Interval(42, 44),
         Interval(47, 59), Interval(9, 11), Interval(40, 42), Interval(57, 65), Interval(12, 12)],
        # Job 39
        [Interval(43, 55), Interval(45, 51), Interval(24, 26), Interval(39, 41), Interval(20, 20),
         Interval(10, 10), Interval(89, 103), Interval(7, 9), Interval(44, 52), Interval(79, 103),
         Interval(88, 88), Interval(29, 31), Interval(86, 94), Interval(50, 56), Interval(24, 26),
         Interval(28, 36), Interval(42, 44), Interval(48, 52), Interval(3, 3), Interval(4, 4)],
        # Job 40
        [Interval(88, 92), Interval(41, 43), Interval(20, 20), Interval(12, 12), Interval(53, 69),
         Interval(77, 101), Interval(2, 2), Interval(50, 64), Interval(25, 27), Interval(73, 81),
         Interval(32, 32), Interval(40, 42), Interval(79, 99), Interval(42, 48), Interval(52, 58),
         Interval(32, 42), Interval(59, 73), Interval(11, 11), Interval(1, 1), Interval(50, 60)],
        # Job 41
        [Interval(20, 24), Interval(34, 44), Interval(26, 26), Interval(78, 92), Interval(56, 66),
         Interval(51, 57), Interval(27, 27), Interval(22, 28), Interval(28, 34), Interval(43, 51),
         Interval(53, 55), Interval(16, 16), Interval(73, 81), Interval(27, 31), Interval(67, 75),
         Interval(24, 24), Interval(84, 88), Interval(63, 73), Interval(20, 22), Interval(34, 46)],
        # Job 42
        [Interval(59, 67), Interval(24, 26), Interval(17, 21), Interval(88, 106), Interval(52, 70),
         Interval(70, 72), Interval(73, 79), Interval(50, 54), Interval(17, 19), Interval(23, 31),
         Interval(92, 102), Interval(69, 79), Interval(15, 17), Interval(10, 10), Interval(72, 72),
         Interval(52, 70), Interval(43, 53), Interval(84, 108), Interval(82, 84), Interval(84, 112)],
        # Job 43
        [Interval(13, 15), Interval(21, 25), Interval(70, 92), Interval(46, 60), Interval(71, 95),
         Interval(91, 95), Interval(78, 94), Interval(40, 50), Interval(67, 75), Interval(9, 9),
         Interval(84, 104), Interval(88, 94), Interval(85, 95), Interval(33, 35), Interval(75, 75),
         Interval(1, 1), Interval(70, 76), Interval(73, 93), Interval(71, 79), Interval(63, 73)],
        # Job 44
        [Interval(17, 19), Interval(62, 66), Interval(22, 22), Interval(31, 35), Interval(8, 10),
         Interval(51, 63), Interval(39, 45), Interval(1, 1), Interval(8, 10), Interval(42, 48),
         Interval(19, 21), Interval(21, 27), Interval(62, 74), Interval(78, 94), Interval(52, 66),
         Interval(79, 101), Interval(50, 62), Interval(40, 42), Interval(37, 41), Interval(41, 45)],
        # Job 45
        [Interval(39, 51), Interval(59, 75), Interval(42, 48), Interval(16, 20), Interval(59, 79),
         Interval(25, 27), Interval(38, 38), Interval(1, 1), Interval(68, 74), Interval(64, 64),
         Interval(25, 33), Interval(71, 83), Interval(47, 53), Interval(22, 24), Interval(23, 25),
         Interval(66, 68), Interval(75, 85), Interval(80, 98), Interval(86, 106), Interval(21, 21)],
        # Job 46
        [Interval(38, 40), Interval(40, 50), Interval(53, 67), Interval(63, 67), Interval(57, 77),
         Interval(83, 99), Interval(90, 108), Interval(84, 108), Interval(3, 3), Interval(11, 11),
         Interval(1, 1), Interval(12, 16), Interval(90, 98), Interval(8, 10), Interval(13, 13),
         Interval(70, 94), Interval(8, 8), Interval(58, 58), Interval(13, 13), Interval(76, 76)],
        # Job 47
        [Interval(52, 62), Interval(47, 53), Interval(54, 56), Interval(54, 54), Interval(41, 51),
         Interval(48, 56), Interval(43, 45), Interval(3, 3), Interval(65, 77), Interval(78, 82),
         Interval(7, 7), Interval(59, 73), Interval(24, 26), Interval(5, 5), Interval(43, 45),
         Interval(38, 50), Interval(66, 86), Interval(77, 89), Interval(38, 38), Interval(93, 95)],
        # Job 48
        [Interval(64, 74), Interval(30, 34), Interval(42, 52), Interval(52, 70), Interval(67, 75),
         Interval(39, 39), Interval(50, 62), Interval(63, 75), Interval(29, 35), Interval(53, 67),
         Interval(19, 25), Interval(58, 78), Interval(16, 20), Interval(8, 10), Interval(75, 77),
         Interval(38, 50), Interval(37, 41), Interval(19, 25), Interval(16, 16), Interval(82, 108)],
        # Job 49
        [Interval(47, 49), Interval(89, 95), Interval(54, 70), Interval(47, 49), Interval(92, 94),
         Interval(27, 27), Interval(76, 84), Interval(44, 52), Interval(82, 88), Interval(62, 62),
         Interval(22, 26), Interval(65, 69), Interval(75, 101), Interval(28, 30), Interval(5, 5),
         Interval(3, 3), Interval(75, 79), Interval(47, 47), Interval(12, 14), Interval(56, 64)],
    ],
    'name': 'INT__TAI50_20_07.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai50_20_07_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI50_20_07.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI50_20_07.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI50_20_07_F_15_01_INTERVAL_DATA
