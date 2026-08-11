"""
Problema INT__DMU05.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Generado con el protocolo F.15_01 del paper (delta ~ U[0, 0.15],
intervalo simetrico, semilla fija) sobre la instancia crisp dmu05 de
Demirkol, Mehta y Uzsoy (1998).
"""

from jobshop_rl.models.interval import Interval


INT__DMU05_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__dmu05.F.15_01_interval',
    'sequences': [
        [8, 13, 6, 10, 4, 7, 14, 11, 3, 9, 0, 2, 1, 12, 5],
        [5, 3, 1, 4, 0, 11, 7, 6, 9, 12, 10, 13, 8, 2, 14],
        [2, 3, 5, 6, 9, 10, 4, 12, 11, 8, 14, 0, 1, 13, 7],
        [11, 10, 13, 5, 4, 2, 12, 6, 8, 3, 7, 14, 0, 1, 9],
        [10, 1, 11, 6, 12, 5, 4, 0, 2, 3, 13, 7, 14, 9, 8],
        [5, 8, 13, 11, 4, 14, 3, 7, 6, 9, 2, 10, 0, 1, 12],
        [7, 5, 10, 8, 2, 4, 12, 14, 11, 3, 6, 13, 9, 0, 1],
        [10, 13, 11, 8, 4, 6, 1, 7, 0, 12, 9, 14, 3, 5, 2],
        [0, 9, 14, 11, 1, 12, 3, 13, 4, 2, 5, 8, 10, 6, 7],
        [4, 0, 3, 12, 7, 8, 13, 9, 1, 10, 2, 6, 14, 11, 5],
        [6, 3, 0, 14, 5, 2, 12, 1, 11, 13, 7, 10, 8, 9, 4],
        [13, 4, 1, 9, 11, 10, 2, 8, 12, 0, 7, 3, 14, 6, 5],
        [0, 7, 11, 10, 3, 12, 13, 14, 2, 8, 6, 1, 4, 5, 9],
        [13, 2, 10, 7, 12, 1, 5, 14, 6, 9, 8, 4, 3, 11, 0],
        [3, 4, 2, 13, 8, 0, 5, 12, 11, 6, 10, 7, 9, 14, 1],
        [11, 0, 1, 12, 5, 4, 7, 6, 13, 9, 3, 14, 2, 10, 8],
        [11, 13, 5, 10, 12, 0, 3, 7, 14, 9, 8, 2, 6, 4, 1],
        [7, 9, 2, 10, 12, 5, 4, 13, 1, 11, 14, 6, 0, 8, 3],
        [5, 14, 10, 8, 13, 11, 12, 4, 0, 9, 3, 6, 2, 1, 7],
        [1, 13, 4, 14, 7, 6, 8, 0, 10, 9, 5, 12, 11, 3, 2],
    ],
    'durations': [
        [Interval(85, 111), Interval(129, 169), Interval(31, 41), Interval(158, 180), Interval(117, 155), Interval(38, 44), Interval(17, 21), Interval(195, 203), Interval(170, 192), Interval(83, 107), Interval(39, 49), Interval(127, 159), Interval(160, 204), Interval(151, 165), Interval(50, 56)],
        [Interval(170, 218), Interval(150, 194), Interval(64, 84), Interval(74, 96), Interval(85, 103), Interval(77, 95), Interval(190, 192), Interval(183, 187), Interval(57, 67), Interval(80, 108), Interval(162, 162), Interval(34, 46), Interval(132, 152), Interval(71, 79), Interval(122, 136)],
        [Interval(60, 80), Interval(33, 33), Interval(112, 116), Interval(154, 204), Interval(127, 135), Interval(52, 56), Interval(112, 144), Interval(27, 29), Interval(103, 109), Interval(156, 204), Interval(45, 51), Interval(93, 119), Interval(131, 137), Interval(106, 106), Interval(85, 85)],
        [Interval(29, 39), Interval(92, 110), Interval(105, 111), Interval(158, 206), Interval(112, 146), Interval(87, 91), Interval(80, 88), Interval(66, 70), Interval(33, 35), Interval(146, 196), Interval(176, 190), Interval(164, 174), Interval(14, 18), Interval(110, 144), Interval(30, 32)],
        [Interval(188, 206), Interval(166, 186), Interval(38, 40), Interval(184, 200), Interval(79, 101), Interval(29, 31), Interval(4, 4), Interval(48, 54), Interval(132, 172), Interval(161, 185), Interval(175, 213), Interval(34, 44), Interval(57, 63), Interval(108, 128), Interval(12, 16)],
        [Interval(82, 86), Interval(22, 22), Interval(18, 22), Interval(50, 52), Interval(124, 166), Interval(80, 92), Interval(156, 162), Interval(42, 56), Interval(191, 195), Interval(41, 45), Interval(175, 181), Interval(142, 178), Interval(17, 19), Interval(105, 117), Interval(185, 201)],
        [Interval(38, 46), Interval(155, 181), Interval(68, 72), Interval(76, 96), Interval(35, 47), Interval(49, 63), Interval(181, 207), Interval(106, 108), Interval(159, 161), Interval(158, 206), Interval(136, 150), Interval(159, 161), Interval(137, 153), Interval(53, 71), Interval(1, 1)],
        [Interval(73, 87), Interval(74, 78), Interval(15, 17), Interval(192, 192), Interval(86, 114), Interval(72, 94), Interval(163, 209), Interval(51, 59), Interval(112, 132), Interval(84, 90), Interval(53, 65), Interval(137, 171), Interval(181, 219), Interval(94, 96), Interval(17, 19)],
        [Interval(72, 76), Interval(93, 105), Interval(41, 49), Interval(86, 96), Interval(142, 164), Interval(189, 209), Interval(31, 39), Interval(110, 132), Interval(123, 133), Interval(171, 215), Interval(114, 136), Interval(128, 154), Interval(71, 83), Interval(147, 151), Interval(194, 200)],
        [Interval(1, 1), Interval(10, 12), Interval(143, 173), Interval(135, 135), Interval(171, 221), Interval(103, 111), Interval(68, 84), Interval(6, 6), Interval(53, 61), Interval(80, 106), Interval(88, 104), Interval(166, 194), Interval(6, 8), Interval(132, 148), Interval(54, 68)],
        [Interval(82, 98), Interval(185, 193), Interval(3, 3), Interval(112, 144), Interval(120, 126), Interval(168, 188), Interval(103, 129), Interval(127, 165), Interval(86, 102), Interval(182, 210), Interval(97, 117), Interval(127, 145), Interval(36, 46), Interval(22, 28), Interval(161, 167)],
        [Interval(72, 92), Interval(60, 62), Interval(50, 54), Interval(125, 157), Interval(59, 71), Interval(89, 99), Interval(46, 50), Interval(117, 139), Interval(132, 160), Interval(90, 90), Interval(45, 49), Interval(143, 165), Interval(45, 53), Interval(152, 202), Interval(39, 45)],
        [Interval(133, 159), Interval(25, 33), Interval(5, 5), Interval(167, 171), Interval(166, 218), Interval(52, 60), Interval(87, 117), Interval(104, 138), Interval(100, 132), Interval(41, 49), Interval(32, 34), Interval(170, 170), Interval(187, 197), Interval(136, 182), Interval(141, 149)],
        [Interval(123, 137), Interval(31, 35), Interval(178, 222), Interval(119, 139), Interval(90, 116), Interval(169, 177), Interval(73, 73), Interval(114, 124), Interval(40, 52), Interval(19, 25), Interval(157, 159), Interval(21, 25), Interval(24, 24), Interval(120, 124), Interval(184, 194)],
        [Interval(9, 11), Interval(192, 206), Interval(135, 163), Interval(67, 73), Interval(67, 85), Interval(139, 171), Interval(2, 2), Interval(68, 90), Interval(95, 109), Interval(149, 177), Interval(156, 166), Interval(109, 143), Interval(62, 76), Interval(29, 37), Interval(193, 199)],
        [Interval(33, 39), Interval(49, 55), Interval(118, 122), Interval(79, 97), Interval(72, 90), Interval(1, 1), Interval(3, 3), Interval(10, 12), Interval(78, 98), Interval(7, 7), Interval(134, 138), Interval(152, 178), Interval(37, 41), Interval(18, 24), Interval(130, 134)],
        [Interval(158, 202), Interval(73, 81), Interval(80, 108), Interval(19, 23), Interval(126, 142), Interval(134, 160), Interval(166, 168), Interval(174, 200), Interval(52, 54), Interval(35, 43), Interval(25, 31), Interval(131, 147), Interval(43, 57), Interval(46, 54), Interval(53, 61)],
        [Interval(172, 198), Interval(100, 104), Interval(121, 133), Interval(96, 124), Interval(172, 224), Interval(60, 72), Interval(161, 205), Interval(101, 101), Interval(23, 27), Interval(14, 16), Interval(105, 111), Interval(50, 64), Interval(28, 36), Interval(41, 45), Interval(39, 47)],
        [Interval(31, 35), Interval(73, 87), Interval(90, 116), Interval(123, 153), Interval(123, 159), Interval(4, 4), Interval(123, 131), Interval(178, 204), Interval(155, 205), Interval(103, 111), Interval(17, 21), Interval(30, 38), Interval(57, 65), Interval(172, 214), Interval(133, 157)],
        [Interval(40, 42), Interval(145, 191), Interval(154, 194), Interval(1, 1), Interval(123, 137), Interval(106, 142), Interval(25, 31), Interval(74, 90), Interval(118, 136), Interval(127, 151), Interval(148, 156), Interval(140, 152), Interval(28, 32), Interval(12, 12), Interval(63, 77)],
    ],
    'name': 'int__dmu05.F.15_01_interval',
    'has_intervals': True,
    'description': 'DMU dmu05 ensanchada F.15_01',
}
