"""
Problema INT__DMU45.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Generado con el protocolo F.15_01 del paper (delta ~ U[0, 0.15],
intervalo simetrico, semilla fija) sobre la instancia crisp dmu45 de
Demirkol, Mehta y Uzsoy (1998).
"""

from jobshop_rl.models.interval import Interval


INT__DMU45_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__dmu45.F.15_01_interval',
    'sequences': [
        [6, 5, 0, 3, 1, 2, 4, 13, 10, 14, 8, 9, 11, 12, 7],
        [6, 1, 3, 0, 2, 4, 5, 7, 11, 12, 9, 13, 10, 8, 14],
        [0, 2, 4, 1, 3, 5, 6, 9, 7, 10, 11, 12, 8, 13, 14],
        [0, 1, 4, 2, 5, 3, 6, 13, 12, 10, 11, 7, 14, 8, 9],
        [4, 2, 1, 6, 0, 3, 5, 10, 8, 14, 11, 9, 13, 12, 7],
        [3, 6, 4, 2, 0, 5, 1, 8, 9, 11, 13, 10, 12, 7, 14],
        [6, 3, 0, 2, 1, 5, 4, 14, 7, 10, 13, 9, 12, 8, 11],
        [1, 2, 5, 0, 6, 4, 3, 8, 13, 7, 12, 9, 10, 14, 11],
        [6, 2, 5, 0, 1, 4, 3, 9, 8, 14, 7, 11, 13, 12, 10],
        [2, 0, 5, 6, 3, 1, 4, 10, 13, 8, 7, 11, 14, 12, 9],
        [2, 1, 6, 0, 5, 4, 3, 14, 8, 13, 10, 11, 12, 7, 9],
        [5, 1, 6, 4, 3, 0, 2, 14, 13, 7, 11, 9, 10, 12, 8],
        [2, 0, 3, 5, 4, 1, 6, 8, 11, 9, 13, 7, 12, 10, 14],
        [1, 2, 4, 3, 5, 0, 6, 12, 9, 13, 11, 8, 7, 10, 14],
        [6, 2, 3, 4, 5, 0, 1, 7, 9, 8, 10, 11, 13, 14, 12],
        [1, 6, 0, 3, 4, 2, 5, 9, 8, 14, 13, 10, 12, 11, 7],
        [0, 2, 3, 1, 6, 4, 5, 11, 14, 9, 10, 7, 12, 13, 8],
        [3, 6, 1, 4, 2, 0, 5, 12, 13, 9, 14, 10, 7, 11, 8],
        [6, 0, 5, 1, 3, 4, 2, 11, 13, 14, 7, 9, 12, 10, 8],
        [5, 6, 3, 0, 4, 2, 1, 13, 9, 14, 11, 8, 10, 12, 7],
    ],
    'durations': [
        [Interval(105, 105), Interval(14, 18), Interval(43, 53), Interval(103, 125), Interval(46, 62), Interval(79, 101), Interval(147, 171), Interval(132, 134), Interval(57, 73), Interval(135, 171), Interval(127, 165), Interval(25, 31), Interval(14, 16), Interval(35, 47), Interval(139, 143)],
        [Interval(25, 33), Interval(79, 85), Interval(38, 42), Interval(40, 50), Interval(140, 162), Interval(99, 107), Interval(21, 27), Interval(102, 132), Interval(50, 60), Interval(179, 191), Interval(24, 26), Interval(110, 128), Interval(153, 183), Interval(54, 62), Interval(3, 3)],
        [Interval(23, 29), Interval(163, 217), Interval(35, 45), Interval(135, 135), Interval(112, 128), Interval(4, 4), Interval(116, 136), Interval(31, 41), Interval(109, 145), Interval(94, 104), Interval(91, 107), Interval(57, 67), Interval(171, 177), Interval(142, 168), Interval(135, 151)],
        [Interval(139, 141), Interval(20, 22), Interval(67, 81), Interval(167, 221), Interval(9, 9), Interval(156, 190), Interval(154, 184), Interval(110, 146), Interval(180, 186), Interval(87, 99), Interval(121, 123), Interval(88, 94), Interval(51, 61), Interval(16, 20), Interval(45, 59)],
        [Interval(31, 35), Interval(169, 223), Interval(143, 177), Interval(6, 6), Interval(21, 23), Interval(147, 181), Interval(107, 143), Interval(130, 170), Interval(17, 21), Interval(66, 80), Interval(36, 44), Interval(94, 116), Interval(39, 39), Interval(81, 105), Interval(94, 116)],
        [Interval(88, 90), Interval(165, 183), Interval(67, 83), Interval(33, 37), Interval(114, 122), Interval(105, 129), Interval(29, 37), Interval(35, 45), Interval(85, 109), Interval(76, 88), Interval(103, 123), Interval(121, 139), Interval(129, 131), Interval(95, 103), Interval(5, 5)],
        [Interval(125, 157), Interval(127, 155), Interval(11, 11), Interval(13, 17), Interval(73, 85), Interval(72, 84), Interval(123, 145), Interval(35, 47), Interval(154, 206), Interval(112, 148), Interval(115, 153), Interval(160, 214), Interval(117, 145), Interval(36, 44), Interval(61, 67)],
        [Interval(8, 10), Interval(92, 104), Interval(149, 195), Interval(94, 108), Interval(2, 2), Interval(66, 82), Interval(124, 146), Interval(28, 36), Interval(167, 185), Interval(168, 180), Interval(95, 95), Interval(101, 109), Interval(33, 39), Interval(153, 177), Interval(173, 207)],
        [Interval(133, 179), Interval(131, 139), Interval(90, 100), Interval(151, 171), Interval(98, 122), Interval(174, 218), Interval(33, 33), Interval(182, 194), Interval(42, 48), Interval(146, 172), Interval(129, 145), Interval(28, 34), Interval(103, 121), Interval(78, 88), Interval(78, 100)],
        [Interval(27, 33), Interval(157, 175), Interval(91, 107), Interval(147, 183), Interval(57, 61), Interval(144, 158), Interval(116, 128), Interval(122, 134), Interval(187, 199), Interval(36, 40), Interval(118, 118), Interval(121, 151), Interval(118, 136), Interval(148, 160), Interval(73, 91)],
        [Interval(64, 70), Interval(142, 166), Interval(114, 136), Interval(50, 64), Interval(22, 26), Interval(20, 22), Interval(10, 12), Interval(75, 83), Interval(128, 156), Interval(26, 32), Interval(176, 196), Interval(95, 119), Interval(56, 58), Interval(191, 193), Interval(179, 215)],
        [Interval(107, 129), Interval(46, 62), Interval(69, 79), Interval(91, 97), Interval(121, 125), Interval(80, 96), Interval(178, 186), Interval(32, 38), Interval(118, 122), Interval(184, 196), Interval(153, 165), Interval(87, 97), Interval(31, 37), Interval(69, 91), Interval(88, 114)],
        [Interval(13, 17), Interval(107, 109), Interval(159, 167), Interval(102, 134), Interval(100, 114), Interval(28, 32), Interval(119, 133), Interval(174, 204), Interval(6, 8), Interval(125, 137), Interval(117, 127), Interval(153, 193), Interval(165, 181), Interval(122, 142), Interval(7, 9)],
        [Interval(116, 138), Interval(134, 168), Interval(1, 1), Interval(102, 130), Interval(144, 172), Interval(126, 170), Interval(112, 150), Interval(34, 38), Interval(190, 198), Interval(90, 94), Interval(22, 24), Interval(168, 186), Interval(59, 71), Interval(150, 180), Interval(160, 204)],
        [Interval(110, 140), Interval(5, 5), Interval(29, 33), Interval(45, 55), Interval(160, 188), Interval(83, 105), Interval(93, 103), Interval(36, 40), Interval(24, 28), Interval(150, 174), Interval(5, 5), Interval(78, 96), Interval(92, 110), Interval(139, 143), Interval(10, 12)],
        [Interval(169, 227), Interval(62, 68), Interval(163, 183), Interval(156, 182), Interval(45, 47), Interval(159, 169), Interval(148, 154), Interval(12, 16), Interval(142, 158), Interval(98, 118), Interval(111, 135), Interval(66, 68), Interval(13, 15), Interval(149, 183), Interval(107, 125)],
        [Interval(157, 191), Interval(145, 185), Interval(180, 180), Interval(106, 124), Interval(170, 200), Interval(97, 103), Interval(114, 130), Interval(36, 40), Interval(108, 116), Interval(86, 100), Interval(123, 151), Interval(63, 85), Interval(29, 39), Interval(45, 55), Interval(41, 43)],
        [Interval(89, 101), Interval(13, 17), Interval(12, 14), Interval(100, 106), Interval(41, 43), Interval(174, 200), Interval(181, 195), Interval(131, 155), Interval(84, 90), Interval(180, 184), Interval(21, 21), Interval(143, 187), Interval(63, 75), Interval(4, 4), Interval(53, 57)],
        [Interval(12, 14), Interval(118, 150), Interval(154, 200), Interval(38, 42), Interval(117, 147), Interval(1, 1), Interval(42, 42), Interval(30, 40), Interval(61, 69), Interval(80, 104), Interval(109, 133), Interval(108, 114), Interval(89, 99), Interval(24, 30), Interval(131, 143)],
        [Interval(95, 127), Interval(154, 180), Interval(109, 125), Interval(3, 3), Interval(75, 77), Interval(101, 119), Interval(70, 88), Interval(136, 148), Interval(176, 224), Interval(31, 35), Interval(129, 167), Interval(81, 99), Interval(74, 90), Interval(139, 187), Interval(24, 26)],
    ],
    'name': 'int__dmu45.F.15_01_interval',
    'has_intervals': True,
    'description': 'DMU dmu45 ensanchada F.15_01',
}
