"""
Problema INT__TAI50_15_04.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI50_15_04_F_15_01_INTERVAL_DATA = {
    'num_jobs': 50,
    'num_machines': 15,
    'problem_id': 'int__tai50_15_04.F.15_01_interval',
    'sequences': [
        [11, 14, 9, 1, 5, 13, 6, 8, 10, 7, 4, 12, 0, 2, 3],
        [12, 11, 10, 4, 6, 14, 2, 0, 5, 3, 1, 13, 9, 8, 7],
        [4, 0, 13, 14, 7, 9, 12, 11, 10, 2, 6, 1, 5, 3, 8],
        [4, 12, 14, 3, 8, 9, 0, 6, 1, 7, 11, 13, 2, 10, 5],
        [10, 4, 5, 14, 9, 12, 6, 13, 0, 3, 8, 2, 11, 1, 7],
        [8, 0, 12, 1, 7, 4, 5, 3, 2, 14, 10, 9, 13, 6, 11],
        [9, 4, 13, 2, 14, 10, 12, 6, 1, 11, 5, 8, 7, 0, 3],
        [9, 4, 12, 11, 6, 7, 0, 2, 10, 3, 14, 13, 1, 8, 5],
        [8, 12, 3, 5, 7, 14, 1, 11, 10, 4, 0, 9, 6, 13, 2],
        [8, 11, 9, 13, 3, 12, 5, 7, 10, 2, 1, 14, 6, 4, 0],
        [4, 9, 2, 10, 12, 6, 8, 0, 13, 5, 11, 14, 7, 1, 3],
        [10, 6, 5, 4, 12, 3, 9, 13, 14, 8, 2, 7, 11, 1, 0],
        [5, 9, 0, 12, 8, 10, 13, 11, 3, 7, 14, 6, 1, 4, 2],
        [4, 5, 12, 2, 6, 14, 0, 7, 1, 11, 13, 10, 8, 9, 3],
        [14, 10, 8, 5, 4, 9, 7, 13, 3, 1, 2, 6, 11, 12, 0],
        [8, 12, 11, 7, 10, 2, 3, 6, 4, 1, 9, 5, 13, 14, 0],
        [1, 4, 5, 6, 9, 13, 3, 7, 2, 14, 11, 0, 10, 12, 8],
        [12, 8, 3, 10, 9, 1, 7, 6, 2, 4, 0, 13, 5, 14, 11],
        [5, 12, 1, 2, 3, 0, 7, 13, 6, 11, 4, 8, 10, 9, 14],
        [12, 1, 8, 11, 2, 7, 6, 10, 4, 13, 14, 9, 5, 3, 0],
        [3, 9, 8, 0, 11, 1, 14, 10, 4, 13, 5, 2, 12, 7, 6],
        [11, 1, 9, 4, 3, 8, 12, 0, 6, 7, 14, 10, 13, 2, 5],
        [1, 7, 6, 5, 9, 14, 2, 4, 3, 0, 13, 12, 11, 8, 10],
        [2, 14, 9, 13, 7, 8, 6, 5, 4, 0, 12, 11, 3, 1, 10],
        [9, 4, 12, 1, 6, 10, 8, 7, 2, 11, 13, 14, 3, 0, 5],
        [4, 1, 9, 0, 8, 2, 14, 3, 5, 6, 7, 13, 11, 12, 10],
        [7, 8, 6, 4, 13, 1, 5, 14, 2, 10, 12, 0, 3, 9, 11],
        [5, 12, 10, 9, 1, 4, 13, 11, 14, 2, 7, 0, 3, 8, 6],
        [1, 13, 0, 5, 4, 6, 8, 11, 14, 12, 9, 10, 7, 3, 2],
        [3, 6, 10, 5, 7, 8, 9, 0, 14, 1, 12, 2, 11, 13, 4],
        [4, 8, 6, 9, 3, 2, 0, 5, 13, 7, 1, 12, 10, 14, 11],
        [4, 0, 12, 6, 1, 3, 14, 11, 7, 2, 5, 8, 10, 13, 9],
        [7, 10, 1, 14, 6, 11, 8, 4, 12, 5, 0, 13, 2, 9, 3],
        [12, 13, 1, 10, 7, 2, 9, 14, 4, 11, 5, 3, 6, 0, 8],
        [0, 2, 10, 1, 12, 4, 5, 11, 9, 3, 8, 7, 6, 13, 14],
        [0, 10, 13, 12, 6, 1, 8, 2, 3, 14, 9, 4, 7, 5, 11],
        [12, 2, 10, 4, 9, 6, 0, 1, 7, 13, 11, 8, 3, 14, 5],
        [3, 1, 12, 5, 6, 2, 8, 14, 0, 11, 7, 10, 13, 9, 4],
        [11, 6, 14, 5, 4, 3, 1, 0, 7, 12, 2, 13, 8, 10, 9],
        [3, 2, 10, 9, 1, 5, 13, 8, 7, 4, 6, 0, 11, 12, 14],
        [6, 2, 9, 7, 13, 8, 1, 11, 12, 5, 10, 3, 14, 4, 0],
        [2, 4, 7, 14, 11, 8, 9, 13, 0, 1, 5, 12, 10, 3, 6],
        [10, 12, 7, 11, 0, 14, 2, 1, 4, 6, 13, 5, 8, 3, 9],
        [0, 9, 11, 1, 14, 4, 3, 7, 2, 5, 12, 10, 8, 13, 6],
        [10, 0, 12, 9, 5, 4, 7, 2, 8, 13, 1, 6, 11, 14, 3],
        [2, 8, 6, 5, 7, 11, 3, 14, 10, 1, 0, 4, 9, 13, 12],
        [2, 5, 3, 13, 0, 10, 12, 14, 6, 7, 1, 8, 9, 4, 11],
        [2, 5, 14, 1, 7, 13, 12, 10, 3, 6, 9, 8, 11, 4, 0],
        [12, 1, 8, 3, 10, 4, 5, 11, 6, 14, 7, 9, 2, 13, 0],
        [5, 2, 14, 10, 11, 3, 6, 1, 9, 8, 12, 7, 0, 13, 4],
    ],
    'durations': [
        # Job 0
        [Interval(20, 26), Interval(58, 58), Interval(52, 68), Interval(38, 48), Interval(17, 17),
         Interval(66, 70), Interval(36, 48), Interval(47, 59), Interval(18, 18), Interval(40, 44),
         Interval(86, 106), Interval(17, 21), Interval(43, 57), Interval(57, 67), Interval(92, 102)],
        # Job 1
        [Interval(25, 33), Interval(55, 69), Interval(55, 57), Interval(29, 37), Interval(65, 79),
         Interval(70, 90), Interval(56, 72), Interval(79, 81), Interval(4, 4), Interval(36, 44),
         Interval(75, 101), Interval(67, 89), Interval(81, 109), Interval(29, 31), Interval(21, 21)],
        # Job 2
        [Interval(30, 38), Interval(58, 62), Interval(70, 86), Interval(47, 63), Interval(39, 43),
         Interval(3, 3), Interval(98, 100), Interval(32, 32), Interval(82, 90), Interval(24, 28),
         Interval(83, 95), Interval(4, 4), Interval(45, 53), Interval(40, 44), Interval(67, 89)],
        # Job 3
        [Interval(84, 90), Interval(3, 3), Interval(23, 31), Interval(63, 75), Interval(7, 9),
         Interval(26, 30), Interval(35, 45), Interval(66, 80), Interval(2, 2), Interval(70, 72),
         Interval(48, 52), Interval(89, 101), Interval(14, 14), Interval(57, 73), Interval(62, 64)],
        # Job 4
        [Interval(46, 46), Interval(37, 43), Interval(39, 47), Interval(47, 49), Interval(24, 32),
         Interval(15, 15), Interval(56, 62), Interval(51, 65), Interval(29, 39), Interval(51, 63),
         Interval(28, 30), Interval(39, 51), Interval(38, 50), Interval(25, 29), Interval(56, 64)],
        # Job 5
        [Interval(58, 76), Interval(29, 33), Interval(7, 9), Interval(20, 22), Interval(17, 19),
         Interval(41, 51), Interval(61, 67), Interval(25, 29), Interval(33, 41), Interval(82, 108),
         Interval(70, 80), Interval(18, 20), Interval(33, 43), Interval(80, 102), Interval(24, 24)],
        # Job 6
        [Interval(32, 34), Interval(45, 47), Interval(57, 61), Interval(68, 74), Interval(17, 21),
         Interval(72, 80), Interval(54, 68), Interval(28, 36), Interval(29, 29), Interval(24, 28),
         Interval(29, 33), Interval(25, 29), Interval(64, 78), Interval(44, 46), Interval(42, 42)],
        # Job 7
        [Interval(64, 66), Interval(26, 28), Interval(53, 71), Interval(72, 76), Interval(2, 2),
         Interval(64, 82), Interval(35, 45), Interval(35, 37), Interval(84, 112), Interval(6, 6),
         Interval(43, 55), Interval(59, 79), Interval(49, 51), Interval(55, 61), Interval(49, 55)],
        # Job 8
        [Interval(86, 102), Interval(69, 75), Interval(45, 51), Interval(21, 25), Interval(91, 103),
         Interval(83, 91), Interval(63, 83), Interval(24, 26), Interval(4, 4), Interval(35, 45),
         Interval(55, 65), Interval(11, 11), Interval(12, 14), Interval(61, 71), Interval(27, 33)],
        # Job 9
        [Interval(65, 73), Interval(49, 59), Interval(13, 15), Interval(58, 64), Interval(12, 12),
         Interval(64, 86), Interval(22, 28), Interval(40, 42), Interval(92, 100), Interval(21, 25),
         Interval(25, 27), Interval(59, 77), Interval(80, 104), Interval(70, 80), Interval(12, 14)],
        # Job 10
        [Interval(48, 64), Interval(38, 48), Interval(10, 10), Interval(57, 77), Interval(94, 104),
         Interval(44, 56), Interval(87, 87), Interval(4, 4), Interval(24, 32), Interval(25, 31),
         Interval(4, 4), Interval(55, 57), Interval(50, 60), Interval(77, 89), Interval(52, 66)],
        # Job 11
        [Interval(46, 46), Interval(63, 85), Interval(12, 12), Interval(86, 106), Interval(69, 81),
         Interval(15, 17), Interval(80, 100), Interval(75, 101), Interval(12, 12), Interval(77, 85),
         Interval(8, 8), Interval(25, 31), Interval(83, 97), Interval(19, 21), Interval(40, 40)],
        # Job 12
        [Interval(31, 41), Interval(82, 92), Interval(91, 101), Interval(22, 22), Interval(90, 92),
         Interval(37, 39), Interval(92, 92), Interval(15, 17), Interval(27, 29), Interval(42, 50),
         Interval(70, 78), Interval(31, 39), Interval(15, 15), Interval(52, 70), Interval(46, 54)],
        # Job 13
        [Interval(70, 70), Interval(45, 59), Interval(5, 5), Interval(45, 51), Interval(51, 65),
         Interval(44, 58), Interval(28, 36), Interval(53, 65), Interval(83, 95), Interval(62, 80),
         Interval(55, 63), Interval(11, 11), Interval(72, 86), Interval(29, 33), Interval(6, 6)],
        # Job 14
        [Interval(80, 108), Interval(33, 41), Interval(48, 52), Interval(83, 93), Interval(79, 95),
         Interval(61, 67), Interval(8, 8), Interval(16, 18), Interval(84, 96), Interval(13, 15),
         Interval(54, 58), Interval(25, 25), Interval(36, 48), Interval(16, 20), Interval(5, 5)],
        # Job 15
        [Interval(58, 74), Interval(55, 67), Interval(65, 79), Interval(22, 28), Interval(32, 32),
         Interval(40, 52), Interval(34, 44), Interval(81, 103), Interval(33, 33), Interval(49, 59),
         Interval(53, 63), Interval(25, 31), Interval(72, 84), Interval(54, 68), Interval(79, 79)],
        # Job 16
        [Interval(85, 109), Interval(31, 37), Interval(42, 52), Interval(67, 75), Interval(83, 85),
         Interval(75, 81), Interval(56, 68), Interval(90, 106), Interval(56, 72), Interval(83, 95),
         Interval(54, 56), Interval(85, 101), Interval(76, 96), Interval(80, 104), Interval(87, 101)],
        # Job 17
        [Interval(62, 82), Interval(40, 40), Interval(49, 63), Interval(31, 31), Interval(8, 10),
         Interval(13, 13), Interval(53, 71), Interval(55, 69), Interval(51, 59), Interval(2, 2),
         Interval(26, 32), Interval(64, 70), Interval(92, 92), Interval(27, 35), Interval(49, 53)],
        # Job 18
        [Interval(34, 36), Interval(35, 45), Interval(28, 36), Interval(37, 45), Interval(64, 64),
         Interval(86, 96), Interval(2, 2), Interval(8, 10), Interval(46, 50), Interval(76, 76),
         Interval(43, 47), Interval(11, 13), Interval(72, 84), Interval(7, 9), Interval(78, 100)],
        # Job 19
        [Interval(46, 60), Interval(93, 93), Interval(78, 80), Interval(92, 98), Interval(19, 19),
         Interval(28, 30), Interval(79, 93), Interval(57, 71), Interval(4, 4), Interval(63, 67),
         Interval(74, 86), Interval(39, 43), Interval(78, 104), Interval(33, 43), Interval(48, 60)],
        # Job 20
        [Interval(75, 75), Interval(70, 78), Interval(38, 38), Interval(92, 106), Interval(43, 45),
         Interval(58, 58), Interval(76, 100), Interval(32, 34), Interval(6, 8), Interval(39, 47),
         Interval(49, 65), Interval(40, 46), Interval(6, 6), Interval(13, 17), Interval(19, 25)],
        # Job 21
        [Interval(77, 93), Interval(39, 51), Interval(3, 3), Interval(15, 15), Interval(48, 52),
         Interval(24, 28), Interval(89, 95), Interval(60, 64), Interval(5, 5), Interval(68, 86),
         Interval(91, 101), Interval(57, 61), Interval(41, 55), Interval(11, 13), Interval(42, 44)],
        # Job 22
        [Interval(25, 25), Interval(13, 15), Interval(31, 37), Interval(33, 33), Interval(18, 18),
         Interval(89, 89), Interval(44, 54), Interval(72, 74), Interval(77, 101), Interval(68, 68),
         Interval(64, 80), Interval(96, 102), Interval(42, 56), Interval(67, 79), Interval(58, 66)],
        # Job 23
        [Interval(8, 10), Interval(39, 39), Interval(58, 66), Interval(68, 88), Interval(10, 10),
         Interval(87, 111), Interval(51, 57), Interval(53, 55), Interval(28, 28), Interval(21, 23),
         Interval(85, 95), Interval(8, 8), Interval(45, 59), Interval(48, 52), Interval(10, 10)],
        # Job 24
        [Interval(83, 93), Interval(85, 95), Interval(57, 75), Interval(10, 10), Interval(75, 77),
         Interval(61, 77), Interval(89, 99), Interval(54, 60), Interval(27, 35), Interval(2, 2),
         Interval(51, 67), Interval(16, 20), Interval(1, 1), Interval(68, 70), Interval(84, 112)],
        # Job 25
        [Interval(71, 95), Interval(23, 27), Interval(36, 38), Interval(24, 24), Interval(48, 48),
         Interval(52, 58), Interval(57, 75), Interval(29, 39), Interval(32, 42), Interval(73, 87),
         Interval(17, 23), Interval(68, 86), Interval(26, 26), Interval(66, 78), Interval(31, 31)],
        # Job 26
        [Interval(19, 25), Interval(30, 32), Interval(43, 47), Interval(11, 13), Interval(75, 99),
         Interval(17, 17), Interval(53, 71), Interval(14, 14), Interval(78, 104), Interval(7, 7),
         Interval(81, 85), Interval(51, 65), Interval(75, 99), Interval(30, 30), Interval(84, 110)],
        # Job 27
        [Interval(34, 38), Interval(59, 77), Interval(9, 11), Interval(16, 16), Interval(66, 72),
         Interval(75, 81), Interval(41, 51), Interval(29, 33), Interval(60, 80), Interval(91, 95),
         Interval(95, 97), Interval(31, 35), Interval(42, 48), Interval(70, 92), Interval(76, 80)],
        # Job 28
        [Interval(13, 13), Interval(18, 24), Interval(14, 14), Interval(72, 78), Interval(77, 99),
         Interval(14, 14), Interval(24, 32), Interval(81, 81), Interval(16, 16), Interval(76, 88),
         Interval(84, 104), Interval(52, 58), Interval(57, 71), Interval(69, 87), Interval(23, 23)],
        # Job 29
        [Interval(89, 95), Interval(12, 12), Interval(46, 46), Interval(2, 2), Interval(5, 5),
         Interval(52, 58), Interval(67, 85), Interval(4, 4), Interval(5, 5), Interval(43, 45),
         Interval(36, 44), Interval(85, 107), Interval(54, 70), Interval(31, 41), Interval(24, 26)],
        # Job 30
        [Interval(17, 17), Interval(79, 93), Interval(36, 36), Interval(10, 10), Interval(94, 94),
         Interval(56, 74), Interval(4, 4), Interval(34, 46), Interval(3, 3), Interval(12, 12),
         Interval(65, 83), Interval(98, 100), Interval(5, 5), Interval(67, 69), Interval(38, 38)],
        # Job 31
        [Interval(47, 57), Interval(44, 44), Interval(63, 81), Interval(23, 25), Interval(86, 98),
         Interval(88, 88), Interval(6, 8), Interval(80, 106), Interval(11, 13), Interval(63, 63),
         Interval(63, 79), Interval(75, 101), Interval(75, 75), Interval(17, 19), Interval(34, 42)],
        # Job 32
        [Interval(36, 38), Interval(64, 64), Interval(64, 86), Interval(34, 46), Interval(12, 16),
         Interval(43, 57), Interval(17, 23), Interval(20, 26), Interval(32, 32), Interval(17, 19),
         Interval(27, 31), Interval(55, 71), Interval(78, 104), Interval(62, 66), Interval(27, 33)],
        # Job 33
        [Interval(66, 72), Interval(15, 15), Interval(34, 44), Interval(20, 26), Interval(46, 56),
         Interval(56, 72), Interval(53, 55), Interval(29, 29), Interval(78, 104), Interval(15, 17),
         Interval(83, 107), Interval(14, 16), Interval(20, 20), Interval(22, 26), Interval(6, 6)],
        # Job 34
        [Interval(10, 10), Interval(47, 49), Interval(61, 65), Interval(70, 94), Interval(43, 51),
         Interval(51, 61), Interval(7, 9), Interval(49, 63), Interval(26, 28), Interval(73, 91),
         Interval(11, 11), Interval(10, 10), Interval(58, 76), Interval(78, 100), Interval(17, 19)],
        # Job 35
        [Interval(43, 55), Interval(10, 12), Interval(50, 50), Interval(22, 28), Interval(34, 36),
         Interval(73, 79), Interval(68, 84), Interval(1, 1), Interval(33, 37), Interval(65, 73),
         Interval(18, 20), Interval(4, 4), Interval(23, 29), Interval(47, 47), Interval(11, 11)],
        # Job 36
        [Interval(9, 11), Interval(15, 15), Interval(81, 83), Interval(50, 50), Interval(46, 52),
         Interval(54, 58), Interval(54, 70), Interval(55, 59), Interval(73, 97), Interval(26, 26),
         Interval(16, 18), Interval(31, 41), Interval(75, 93), Interval(8, 8), Interval(58, 78)],
        # Job 37
        [Interval(23, 27), Interval(19, 19), Interval(66, 68), Interval(24, 32), Interval(78, 98),
         Interval(64, 72), Interval(26, 32), Interval(56, 70), Interval(8, 8), Interval(5, 5),
         Interval(5, 5), Interval(44, 50), Interval(6, 6), Interval(2, 2), Interval(92, 102)],
        # Job 38
        [Interval(25, 33), Interval(61, 63), Interval(17, 23), Interval(50, 62), Interval(58, 70),
         Interval(75, 89), Interval(18, 22), Interval(11, 11), Interval(62, 68), Interval(66, 66),
         Interval(44, 46), Interval(56, 60), Interval(82, 86), Interval(68, 78), Interval(65, 75)],
        # Job 39
        [Interval(45, 59), Interval(58, 74), Interval(8, 10), Interval(81, 85), Interval(20, 24),
         Interval(74, 80), Interval(58, 62), Interval(24, 32), Interval(29, 33), Interval(12, 12),
         Interval(85, 89), Interval(81, 89), Interval(7, 9), Interval(82, 94), Interval(66, 82)],
        # Job 40
        [Interval(36, 40), Interval(31, 39), Interval(29, 29), Interval(65, 69), Interval(75, 91),
         Interval(57, 57), Interval(52, 68), Interval(4, 4), Interval(12, 14), Interval(50, 52),
         Interval(16, 20), Interval(75, 99), Interval(17, 19), Interval(77, 97), Interval(37, 37)],
        # Job 41
        [Interval(51, 69), Interval(18, 24), Interval(85, 111), Interval(73, 81), Interval(57, 75),
         Interval(75, 87), Interval(8, 8), Interval(52, 56), Interval(62, 62), Interval(37, 45),
         Interval(33, 39), Interval(70, 76), Interval(45, 55), Interval(1, 1), Interval(3, 3)],
        # Job 42
        [Interval(16, 18), Interval(23, 23), Interval(39, 49), Interval(61, 63), Interval(43, 43),
         Interval(48, 52), Interval(51, 53), Interval(17, 19), Interval(25, 29), Interval(16, 16),
         Interval(86, 100), Interval(88, 106), Interval(46, 46), Interval(74, 86), Interval(81, 99)],
        # Job 43
        [Interval(85, 103), Interval(39, 41), Interval(46, 46), Interval(18, 18), Interval(38, 40),
         Interval(48, 62), Interval(51, 53), Interval(17, 19), Interval(41, 51), Interval(5, 5),
         Interval(23, 29), Interval(38, 40), Interval(42, 56), Interval(90, 98), Interval(84, 102)],
        # Job 44
        [Interval(50, 62), Interval(44, 44), Interval(91, 91), Interval(58, 68), Interval(46, 58),
         Interval(54, 54), Interval(29, 33), Interval(86, 112), Interval(40, 44), Interval(6, 6),
         Interval(1, 1), Interval(81, 107), Interval(32, 32), Interval(80, 106), Interval(84, 110)],
        # Job 45
        [Interval(32, 38), Interval(25, 29), Interval(50, 58), Interval(59, 75), Interval(72, 72),
         Interval(90, 104), Interval(74, 84), Interval(12, 14), Interval(15, 19), Interval(54, 58),
         Interval(57, 69), Interval(85, 111), Interval(14, 16), Interval(16, 20), Interval(3, 3)],
        # Job 46
        [Interval(17, 23), Interval(47, 47), Interval(70, 82), Interval(54, 62), Interval(37, 47),
         Interval(68, 84), Interval(36, 40), Interval(7, 7), Interval(4, 4), Interval(23, 27),
         Interval(52, 70), Interval(3, 3), Interval(57, 67), Interval(8, 8), Interval(86, 112)],
        # Job 47
        [Interval(64, 78), Interval(84, 104), Interval(22, 26), Interval(69, 79), Interval(70, 84),
         Interval(82, 98), Interval(64, 74), Interval(42, 50), Interval(60, 66), Interval(71, 91),
         Interval(33, 33), Interval(60, 80), Interval(39, 41), Interval(90, 92), Interval(21, 23)],
        # Job 48
        [Interval(24, 26), Interval(57, 63), Interval(40, 40), Interval(72, 92), Interval(1, 1),
         Interval(83, 95), Interval(1, 1), Interval(12, 14), Interval(59, 65), Interval(91, 101),
         Interval(10, 10), Interval(78, 88), Interval(31, 33), Interval(52, 58), Interval(85, 89)],
        # Job 49
        [Interval(27, 35), Interval(59, 75), Interval(56, 60), Interval(44, 50), Interval(36, 38),
         Interval(47, 57), Interval(80, 98), Interval(14, 18), Interval(36, 36), Interval(74, 86),
         Interval(72, 88), Interval(85, 89), Interval(22, 26), Interval(39, 41), Interval(86, 102)],
    ],
    'name': 'INT__TAI50_15_04.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai50_15_04_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI50_15_04.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI50_15_04.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI50_15_04_F_15_01_INTERVAL_DATA
