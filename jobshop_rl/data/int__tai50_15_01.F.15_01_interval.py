"""
Problema INT__TAI50_15_01.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI50_15_01_F_15_01_INTERVAL_DATA = {
    'num_jobs': 50,
    'num_machines': 15,
    'problem_id': 'int__tai50_15_01.F.15_01_interval',
    'sequences': [
        [9, 10, 3, 8, 5, 7, 4, 0, 12, 1, 13, 6, 11, 2, 14],
        [1, 7, 8, 2, 9, 14, 12, 4, 3, 11, 13, 0, 5, 10, 6],
        [2, 13, 11, 4, 14, 8, 10, 3, 6, 5, 7, 1, 9, 12, 0],
        [10, 12, 7, 1, 5, 14, 4, 9, 2, 3, 8, 0, 11, 13, 6],
        [5, 3, 7, 0, 9, 6, 11, 10, 12, 4, 14, 2, 1, 8, 13],
        [3, 0, 6, 2, 4, 1, 5, 14, 10, 13, 11, 9, 7, 8, 12],
        [13, 10, 9, 8, 1, 6, 14, 0, 12, 11, 7, 2, 3, 5, 4],
        [14, 11, 10, 13, 12, 6, 4, 0, 7, 5, 2, 1, 3, 8, 9],
        [7, 2, 8, 10, 1, 14, 5, 4, 0, 12, 3, 9, 6, 13, 11],
        [12, 5, 4, 7, 3, 1, 11, 8, 14, 6, 9, 2, 10, 0, 13],
        [9, 11, 8, 5, 4, 6, 2, 12, 14, 1, 10, 7, 0, 3, 13],
        [3, 9, 7, 5, 4, 10, 2, 8, 14, 11, 12, 6, 13, 0, 1],
        [8, 4, 12, 3, 2, 9, 10, 6, 0, 13, 14, 1, 5, 7, 11],
        [14, 3, 8, 11, 5, 7, 12, 10, 2, 0, 13, 6, 1, 9, 4],
        [1, 4, 14, 3, 10, 6, 5, 2, 11, 0, 8, 7, 9, 13, 12],
        [4, 8, 11, 2, 13, 0, 7, 12, 6, 3, 9, 1, 5, 10, 14],
        [10, 12, 1, 4, 8, 7, 14, 9, 2, 0, 13, 6, 11, 5, 3],
        [13, 11, 9, 12, 0, 1, 10, 4, 6, 14, 7, 8, 3, 2, 5],
        [10, 2, 14, 1, 7, 13, 4, 9, 5, 3, 8, 0, 11, 6, 12],
        [0, 11, 2, 10, 6, 3, 4, 5, 12, 8, 7, 14, 9, 1, 13],
        [1, 4, 8, 2, 3, 7, 12, 13, 9, 14, 0, 5, 11, 6, 10],
        [7, 12, 9, 5, 1, 2, 14, 10, 6, 4, 8, 3, 0, 13, 11],
        [2, 0, 10, 7, 3, 14, 11, 1, 5, 12, 8, 6, 4, 9, 13],
        [9, 4, 14, 1, 3, 2, 8, 0, 6, 10, 7, 5, 11, 12, 13],
        [0, 8, 2, 10, 13, 3, 12, 1, 7, 4, 9, 5, 6, 14, 11],
        [13, 14, 7, 6, 11, 12, 0, 1, 10, 8, 4, 3, 9, 5, 2],
        [7, 11, 0, 6, 2, 8, 14, 5, 4, 12, 13, 1, 9, 3, 10],
        [9, 7, 6, 5, 10, 1, 14, 11, 12, 0, 4, 3, 8, 2, 13],
        [2, 3, 8, 1, 12, 13, 7, 11, 5, 0, 9, 10, 4, 14, 6],
        [8, 4, 12, 11, 3, 7, 0, 10, 6, 1, 14, 2, 5, 9, 13],
        [8, 1, 4, 6, 7, 14, 3, 10, 5, 12, 0, 13, 11, 9, 2],
        [7, 13, 0, 8, 9, 1, 10, 12, 5, 3, 4, 11, 2, 6, 14],
        [10, 8, 14, 2, 12, 0, 3, 5, 1, 9, 11, 7, 13, 4, 6],
        [1, 2, 5, 9, 7, 4, 0, 3, 14, 12, 13, 10, 6, 11, 8],
        [11, 2, 4, 14, 6, 5, 7, 12, 9, 3, 8, 0, 10, 13, 1],
        [14, 8, 5, 7, 10, 13, 1, 0, 9, 4, 3, 2, 6, 12, 11],
        [13, 7, 12, 11, 8, 3, 9, 2, 1, 5, 14, 6, 0, 10, 4],
        [0, 14, 5, 2, 4, 10, 9, 6, 3, 11, 12, 8, 13, 7, 1],
        [9, 7, 0, 6, 4, 8, 1, 3, 12, 10, 5, 13, 11, 14, 2],
        [14, 10, 6, 5, 0, 4, 8, 12, 9, 2, 7, 1, 11, 3, 13],
        [3, 11, 4, 14, 5, 8, 6, 2, 9, 10, 7, 13, 1, 0, 12],
        [3, 0, 10, 2, 12, 7, 4, 8, 6, 14, 11, 9, 1, 13, 5],
        [14, 2, 6, 5, 1, 3, 11, 13, 8, 12, 9, 4, 10, 0, 7],
        [10, 6, 14, 11, 7, 13, 1, 9, 8, 0, 4, 12, 2, 3, 5],
        [5, 2, 12, 7, 9, 11, 0, 1, 3, 10, 6, 8, 4, 14, 13],
        [9, 11, 1, 7, 0, 14, 8, 5, 10, 6, 2, 13, 3, 4, 12],
        [7, 10, 9, 3, 13, 4, 12, 5, 8, 14, 1, 6, 2, 0, 11],
        [4, 11, 13, 14, 5, 7, 2, 9, 12, 1, 0, 10, 3, 8, 6],
        [11, 10, 8, 3, 6, 9, 12, 7, 4, 1, 0, 2, 5, 13, 14],
        [9, 6, 4, 2, 14, 3, 8, 11, 10, 13, 5, 7, 1, 0, 12],
    ],
    'durations': [
        # Job 0
        [Interval(12, 16), Interval(79, 79), Interval(6, 6), Interval(30, 40), Interval(37, 47),
         Interval(61, 67), Interval(50, 52), Interval(58, 76), Interval(12, 14), Interval(9, 9),
         Interval(44, 48), Interval(75, 93), Interval(54, 66), Interval(9, 11), Interval(31, 37)],
        # Job 1
        [Interval(43, 47), Interval(36, 48), Interval(84, 106), Interval(95, 99), Interval(37, 49),
         Interval(36, 44), Interval(22, 28), Interval(19, 25), Interval(56, 58), Interval(13, 17),
         Interval(51, 67), Interval(29, 37), Interval(71, 95), Interval(69, 75), Interval(27, 27)],
        # Job 2
        [Interval(13, 17), Interval(88, 96), Interval(73, 91), Interval(65, 87), Interval(83, 91),
         Interval(92, 94), Interval(30, 30), Interval(92, 100), Interval(19, 23), Interval(71, 81),
         Interval(56, 66), Interval(58, 66), Interval(6, 8), Interval(20, 22), Interval(33, 43)],
        # Job 3
        [Interval(33, 39), Interval(85, 107), Interval(72, 82), Interval(85, 109), Interval(24, 28),
         Interval(13, 13), Interval(86, 94), Interval(56, 64), Interval(90, 92), Interval(76, 96),
         Interval(72, 76), Interval(64, 64), Interval(39, 45), Interval(84, 102), Interval(1, 1)],
        # Job 4
        [Interval(27, 27), Interval(52, 70), Interval(86, 88), Interval(2, 2), Interval(29, 31),
         Interval(41, 53), Interval(50, 66), Interval(5, 5), Interval(73, 93), Interval(68, 76),
         Interval(61, 81), Interval(45, 59), Interval(44, 52), Interval(50, 58), Interval(23, 31)],
        # Job 5
        [Interval(41, 47), Interval(58, 74), Interval(1, 1), Interval(12, 12), Interval(20, 22),
         Interval(22, 26), Interval(19, 19), Interval(6, 6), Interval(29, 33), Interval(44, 56),
         Interval(73, 95), Interval(32, 36), Interval(54, 64), Interval(55, 73), Interval(47, 59)],
        # Job 6
        [Interval(50, 52), Interval(46, 50), Interval(38, 40), Interval(72, 78), Interval(13, 13),
         Interval(83, 105), Interval(5, 5), Interval(70, 76), Interval(34, 42), Interval(24, 32),
         Interval(77, 77), Interval(37, 43), Interval(42, 48), Interval(84, 94), Interval(80, 98)],
        # Job 7
        [Interval(5, 5), Interval(34, 36), Interval(87, 87), Interval(47, 49), Interval(24, 26),
         Interval(4, 4), Interval(66, 86), Interval(22, 22), Interval(80, 104), Interval(68, 86),
         Interval(84, 88), Interval(30, 40), Interval(38, 48), Interval(64, 86), Interval(59, 63)],
        # Job 8
        [Interval(46, 52), Interval(39, 43), Interval(73, 87), Interval(25, 27), Interval(17, 19),
         Interval(27, 33), Interval(40, 46), Interval(48, 52), Interval(23, 29), Interval(22, 24),
         Interval(19, 25), Interval(65, 75), Interval(43, 45), Interval(49, 57), Interval(38, 44)],
        # Job 9
        [Interval(37, 45), Interval(3, 3), Interval(5, 5), Interval(28, 32), Interval(85, 101),
         Interval(70, 82), Interval(82, 90), Interval(19, 21), Interval(62, 82), Interval(57, 75),
         Interval(79, 83), Interval(36, 38), Interval(34, 40), Interval(46, 50), Interval(12, 16)],
        # Job 10
        [Interval(23, 31), Interval(8, 8), Interval(59, 77), Interval(1, 1), Interval(65, 87),
         Interval(10, 12), Interval(45, 45), Interval(68, 92), Interval(23, 25), Interval(77, 97),
         Interval(48, 48), Interval(39, 51), Interval(74, 94), Interval(33, 35), Interval(6, 8)],
        # Job 11
        [Interval(74, 86), Interval(4, 4), Interval(73, 95), Interval(5, 5), Interval(52, 52),
         Interval(64, 86), Interval(4, 4), Interval(90, 96), Interval(30, 36), Interval(31, 37),
         Interval(70, 84), Interval(49, 61), Interval(40, 54), Interval(77, 89), Interval(58, 64)],
        # Job 12
        [Interval(60, 66), Interval(61, 73), Interval(26, 30), Interval(89, 99), Interval(58, 58),
         Interval(47, 63), Interval(23, 25), Interval(93, 103), Interval(89, 93), Interval(90, 92),
         Interval(17, 17), Interval(37, 37), Interval(38, 42), Interval(11, 11), Interval(17, 19)],
        # Job 13
        [Interval(41, 45), Interval(6, 8), Interval(3, 3), Interval(67, 67), Interval(30, 40),
         Interval(36, 42), Interval(81, 81), Interval(85, 113), Interval(65, 75), Interval(24, 32),
         Interval(68, 88), Interval(76, 100), Interval(71, 89), Interval(38, 44), Interval(59, 77)],
        # Job 14
        [Interval(44, 50), Interval(16, 18), Interval(82, 98), Interval(43, 51), Interval(6, 6),
         Interval(74, 98), Interval(22, 26), Interval(54, 60), Interval(17, 19), Interval(67, 81),
         Interval(61, 67), Interval(6, 6), Interval(5, 5), Interval(90, 102), Interval(49, 55)],
        # Job 15
        [Interval(50, 58), Interval(45, 53), Interval(64, 70), Interval(51, 51), Interval(17, 21),
         Interval(59, 73), Interval(45, 57), Interval(48, 58), Interval(4, 4), Interval(85, 105),
         Interval(24, 32), Interval(45, 45), Interval(23, 31), Interval(2, 2), Interval(59, 77)],
        # Job 16
        [Interval(41, 51), Interval(50, 50), Interval(67, 81), Interval(59, 71), Interval(57, 71),
         Interval(14, 16), Interval(65, 83), Interval(90, 90), Interval(15, 19), Interval(89, 107),
         Interval(25, 31), Interval(17, 19), Interval(56, 56), Interval(76, 84), Interval(48, 56)],
        # Job 17
        [Interval(47, 55), Interval(31, 41), Interval(92, 104), Interval(8, 8), Interval(73, 87),
         Interval(68, 86), Interval(53, 69), Interval(88, 102), Interval(59, 79), Interval(13, 13),
         Interval(29, 39), Interval(43, 45), Interval(15, 19), Interval(1, 1), Interval(37, 37)],
        # Job 18
        [Interval(64, 86), Interval(6, 6), Interval(14, 18), Interval(56, 66), Interval(40, 50),
         Interval(55, 59), Interval(25, 25), Interval(12, 16), Interval(30, 32), Interval(12, 12),
         Interval(2, 2), Interval(39, 49), Interval(86, 110), Interval(43, 51), Interval(7, 7)],
        # Job 19
        [Interval(46, 52), Interval(63, 79), Interval(33, 35), Interval(5, 5), Interval(89, 91),
         Interval(49, 53), Interval(16, 20), Interval(61, 71), Interval(49, 63), Interval(43, 55),
         Interval(33, 43), Interval(44, 44), Interval(21, 21), Interval(72, 76), Interval(45, 49)],
        # Job 20
        [Interval(78, 84), Interval(4, 4), Interval(26, 32), Interval(85, 107), Interval(75, 81),
         Interval(74, 86), Interval(62, 68), Interval(52, 70), Interval(72, 96), Interval(24, 28),
         Interval(36, 36), Interval(63, 71), Interval(60, 60), Interval(15, 17), Interval(64, 70)],
        # Job 21
        [Interval(33, 33), Interval(47, 59), Interval(49, 53), Interval(6, 6), Interval(85, 105),
         Interval(83, 99), Interval(10, 12), Interval(20, 22), Interval(67, 85), Interval(28, 36),
         Interval(51, 61), Interval(67, 87), Interval(40, 42), Interval(78, 86), Interval(17, 19)],
        # Job 22
        [Interval(46, 48), Interval(18, 18), Interval(70, 90), Interval(78, 86), Interval(20, 22),
         Interval(21, 27), Interval(58, 76), Interval(66, 70), Interval(79, 83), Interval(45, 53),
         Interval(36, 42), Interval(29, 29), Interval(20, 20), Interval(79, 79), Interval(34, 42)],
        # Job 23
        [Interval(81, 83), Interval(61, 79), Interval(56, 56), Interval(59, 73), Interval(16, 16),
         Interval(53, 71), Interval(25, 29), Interval(6, 6), Interval(1, 1), Interval(82, 94),
         Interval(39, 51), Interval(27, 27), Interval(8, 8), Interval(75, 99), Interval(40, 42)],
        # Job 24
        [Interval(68, 88), Interval(20, 22), Interval(85, 89), Interval(87, 89), Interval(31, 35),
         Interval(14, 16), Interval(63, 73), Interval(32, 42), Interval(32, 34), Interval(29, 31),
         Interval(45, 51), Interval(27, 31), Interval(14, 18), Interval(41, 41), Interval(30, 30)],
        # Job 25
        [Interval(65, 81), Interval(82, 90), Interval(18, 20), Interval(85, 113), Interval(68, 88),
         Interval(67, 85), Interval(8, 8), Interval(39, 51), Interval(82, 110), Interval(40, 46),
         Interval(46, 48), Interval(8, 8), Interval(25, 25), Interval(54, 60), Interval(78, 104)],
        # Job 26
        [Interval(6, 6), Interval(78, 100), Interval(44, 58), Interval(49, 57), Interval(75, 97),
         Interval(56, 72), Interval(55, 57), Interval(73, 89), Interval(6, 6), Interval(53, 53),
         Interval(53, 71), Interval(51, 53), Interval(49, 53), Interval(58, 74), Interval(19, 25)],
        # Job 27
        [Interval(86, 88), Interval(83, 109), Interval(25, 25), Interval(57, 75), Interval(92, 92),
         Interval(43, 45), Interval(59, 77), Interval(43, 57), Interval(23, 23), Interval(39, 51),
         Interval(68, 76), Interval(82, 104), Interval(8, 10), Interval(13, 13), Interval(83, 91)],
        # Job 28
        [Interval(91, 99), Interval(14, 18), Interval(60, 68), Interval(62, 82), Interval(32, 32),
         Interval(4, 4), Interval(51, 51), Interval(48, 56), Interval(32, 38), Interval(67, 87),
         Interval(38, 40), Interval(72, 72), Interval(57, 73), Interval(45, 47), Interval(65, 69)],
        # Job 29
        [Interval(55, 69), Interval(30, 30), Interval(86, 112), Interval(67, 67), Interval(77, 77),
         Interval(8, 10), Interval(50, 62), Interval(70, 78), Interval(77, 95), Interval(55, 71),
         Interval(81, 81), Interval(80, 84), Interval(67, 75), Interval(62, 62), Interval(53, 59)],
        # Job 30
        [Interval(6, 6), Interval(86, 110), Interval(46, 50), Interval(3, 3), Interval(41, 49),
         Interval(76, 94), Interval(27, 35), Interval(37, 49), Interval(13, 15), Interval(69, 71),
         Interval(15, 17), Interval(86, 88), Interval(25, 25), Interval(62, 62), Interval(74, 98)],
        # Job 31
        [Interval(80, 104), Interval(92, 104), Interval(80, 102), Interval(30, 30), Interval(35, 35),
         Interval(29, 29), Interval(71, 89), Interval(99, 99), Interval(22, 28), Interval(50, 56),
         Interval(46, 52), Interval(97, 97), Interval(30, 38), Interval(84, 112), Interval(12, 14)],
        # Job 32
        [Interval(34, 34), Interval(59, 73), Interval(71, 95), Interval(78, 78), Interval(10, 10),
         Interval(84, 106), Interval(63, 65), Interval(43, 43), Interval(56, 74), Interval(32, 42),
         Interval(64, 82), Interval(29, 37), Interval(39, 51), Interval(5, 5), Interval(16, 20)],
        # Job 33
        [Interval(11, 11), Interval(20, 22), Interval(39, 45), Interval(61, 79), Interval(37, 49),
         Interval(46, 50), Interval(52, 64), Interval(52, 56), Interval(9, 9), Interval(15, 19),
         Interval(63, 83), Interval(38, 46), Interval(16, 20), Interval(74, 78), Interval(29, 29)],
        # Job 34
        [Interval(79, 105), Interval(80, 98), Interval(24, 32), Interval(8, 8), Interval(13, 13),
         Interval(83, 101), Interval(13, 13), Interval(44, 46), Interval(46, 48), Interval(31, 41),
         Interval(41, 47), Interval(61, 73), Interval(22, 28), Interval(67, 87), Interval(41, 45)],
        # Job 35
        [Interval(78, 98), Interval(34, 38), Interval(13, 13), Interval(57, 73), Interval(8, 10),
         Interval(41, 49), Interval(78, 100), Interval(72, 86), Interval(99, 99), Interval(81, 107),
         Interval(36, 38), Interval(73, 79), Interval(88, 110), Interval(36, 40), Interval(75, 83)],
        # Job 36
        [Interval(30, 34), Interval(56, 74), Interval(85, 87), Interval(42, 46), Interval(2, 2),
         Interval(49, 61), Interval(63, 69), Interval(49, 51), Interval(31, 31), Interval(62, 70),
         Interval(85, 91), Interval(9, 11), Interval(44, 48), Interval(48, 64), Interval(36, 36)],
        # Job 37
        [Interval(50, 60), Interval(67, 89), Interval(49, 61), Interval(60, 64), Interval(56, 74),
         Interval(87, 107), Interval(9, 9), Interval(46, 48), Interval(49, 63), Interval(82, 102),
         Interval(20, 22), Interval(59, 73), Interval(35, 45), Interval(20, 20), Interval(90, 104)],
        # Job 38
        [Interval(77, 85), Interval(37, 49), Interval(71, 73), Interval(63, 79), Interval(5, 5),
         Interval(50, 62), Interval(76, 92), Interval(49, 57), Interval(88, 108), Interval(74, 78),
         Interval(14, 16), Interval(84, 84), Interval(47, 49), Interval(63, 67), Interval(19, 19)],
        # Job 39
        [Interval(92, 106), Interval(22, 24), Interval(12, 16), Interval(3, 3), Interval(22, 28),
         Interval(86, 104), Interval(52, 54), Interval(20, 24), Interval(30, 32), Interval(3, 3),
         Interval(83, 89), Interval(34, 46), Interval(62, 70), Interval(75, 85), Interval(19, 19)],
        # Job 40
        [Interval(8, 8), Interval(33, 41), Interval(84, 96), Interval(88, 108), Interval(16, 18),
         Interval(77, 99), Interval(35, 35), Interval(51, 53), Interval(1, 1), Interval(90, 108),
         Interval(36, 36), Interval(25, 33), Interval(70, 84), Interval(18, 18), Interval(47, 63)],
        # Job 41
        [Interval(66, 86), Interval(30, 36), Interval(33, 41), Interval(79, 83), Interval(61, 81),
         Interval(49, 65), Interval(76, 100), Interval(28, 30), Interval(35, 47), Interval(6, 8),
         Interval(41, 45), Interval(7, 7), Interval(32, 32), Interval(14, 16), Interval(15, 17)],
        # Job 42
        [Interval(21, 23), Interval(35, 41), Interval(19, 23), Interval(25, 25), Interval(8, 10),
         Interval(49, 51), Interval(51, 51), Interval(79, 87), Interval(72, 74), Interval(77, 93),
         Interval(49, 57), Interval(21, 21), Interval(11, 13), Interval(9, 11), Interval(34, 34)],
        # Job 43
        [Interval(83, 95), Interval(76, 92), Interval(85, 103), Interval(80, 84), Interval(42, 42),
         Interval(26, 26), Interval(16, 16), Interval(34, 46), Interval(54, 56), Interval(14, 16),
         Interval(27, 35), Interval(65, 81), Interval(91, 99), Interval(34, 44), Interval(11, 11)],
        # Job 44
        [Interval(47, 57), Interval(63, 79), Interval(75, 75), Interval(11, 11), Interval(71, 83),
         Interval(66, 84), Interval(68, 68), Interval(51, 59), Interval(78, 102), Interval(20, 22),
         Interval(53, 71), Interval(23, 23), Interval(81, 109), Interval(7, 9), Interval(60, 72)],
        # Job 45
        [Interval(84, 98), Interval(42, 48), Interval(39, 49), Interval(23, 23), Interval(43, 51),
         Interval(56, 64), Interval(32, 40), Interval(72, 90), Interval(24, 24), Interval(54, 66),
         Interval(53, 71), Interval(13, 13), Interval(75, 101), Interval(33, 43), Interval(46, 46)],
        # Job 46
        [Interval(83, 97), Interval(81, 93), Interval(43, 55), Interval(69, 85), Interval(30, 34),
         Interval(28, 28), Interval(73, 87), Interval(52, 70), Interval(69, 81), Interval(23, 23),
         Interval(5, 5), Interval(37, 49), Interval(28, 34), Interval(72, 88), Interval(62, 74)],
        # Job 47
        [Interval(86, 98), Interval(61, 73), Interval(71, 85), Interval(37, 41), Interval(67, 81),
         Interval(45, 49), Interval(49, 63), Interval(81, 81), Interval(44, 58), Interval(82, 88),
         Interval(12, 12), Interval(24, 26), Interval(62, 66), Interval(67, 73), Interval(49, 49)],
        # Job 48
        [Interval(65, 81), Interval(68, 78), Interval(54, 64), Interval(44, 50), Interval(34, 38),
         Interval(81, 81), Interval(55, 61), Interval(37, 39), Interval(32, 34), Interval(19, 19),
         Interval(13, 17), Interval(85, 109), Interval(24, 26), Interval(63, 71), Interval(87, 91)],
        # Job 49
        [Interval(8, 10), Interval(52, 64), Interval(57, 71), Interval(46, 46), Interval(2, 2),
         Interval(23, 25), Interval(61, 75), Interval(4, 4), Interval(54, 56), Interval(86, 104),
         Interval(95, 101), Interval(53, 61), Interval(54, 72), Interval(31, 31), Interval(30, 32)],
    ],
    'name': 'INT__TAI50_15_01.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai50_15_01_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI50_15_01.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI50_15_01.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI50_15_01_F_15_01_INTERVAL_DATA
