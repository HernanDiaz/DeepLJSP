"""
Problema INT__DMU01.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Generado con el protocolo F.15_01 del paper (delta ~ U[0, 0.15],
intervalo simetrico, semilla fija) sobre la instancia crisp dmu01 de
Demirkol, Mehta y Uzsoy (1998).
"""

from jobshop_rl.models.interval import Interval


INT__DMU01_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__dmu01.F.15_01_interval',
    'sequences': [
        [0, 13, 6, 11, 12, 5, 2, 1, 3, 10, 7, 4, 14, 8, 9],
        [14, 7, 3, 2, 11, 1, 12, 0, 4, 9, 10, 13, 8, 6, 5],
        [11, 5, 9, 4, 13, 12, 6, 7, 10, 0, 2, 8, 14, 3, 1],
        [13, 1, 4, 0, 5, 8, 3, 14, 2, 11, 6, 9, 12, 7, 10],
        [5, 9, 10, 12, 11, 1, 3, 0, 4, 14, 2, 6, 13, 8, 7],
        [5, 0, 2, 14, 12, 13, 11, 7, 1, 6, 4, 9, 3, 8, 10],
        [6, 1, 3, 12, 11, 10, 2, 9, 4, 13, 0, 7, 8, 14, 5],
        [13, 0, 14, 9, 7, 11, 8, 3, 12, 5, 6, 2, 4, 10, 1],
        [13, 8, 6, 4, 14, 12, 10, 5, 0, 1, 9, 11, 3, 7, 2],
        [1, 5, 9, 8, 12, 3, 11, 7, 6, 10, 2, 4, 0, 13, 14],
        [2, 1, 13, 6, 7, 14, 5, 0, 12, 11, 9, 8, 4, 3, 10],
        [3, 6, 4, 13, 14, 5, 9, 0, 1, 11, 12, 2, 7, 10, 8],
        [9, 12, 8, 5, 2, 10, 4, 3, 6, 1, 14, 13, 7, 11, 0],
        [5, 3, 11, 8, 12, 0, 9, 14, 13, 4, 7, 1, 2, 6, 10],
        [10, 11, 6, 8, 14, 12, 7, 13, 0, 2, 9, 5, 1, 4, 3],
        [11, 9, 14, 3, 7, 4, 10, 0, 1, 6, 13, 5, 2, 8, 12],
        [1, 11, 3, 9, 14, 12, 7, 10, 4, 6, 2, 13, 8, 5, 0],
        [8, 0, 14, 11, 9, 1, 12, 7, 3, 13, 4, 6, 2, 5, 10],
        [11, 3, 0, 4, 12, 13, 5, 9, 1, 6, 10, 7, 2, 14, 8],
        [1, 10, 4, 2, 11, 5, 9, 0, 7, 13, 8, 12, 6, 3, 14],
    ],
    'durations': [
        [Interval(148, 172), Interval(5, 5), Interval(127, 151), Interval(96, 102), Interval(9, 9), Interval(93, 103), Interval(24, 32), Interval(96, 118), Interval(191, 201), Interval(141, 189), Interval(105, 123), Interval(6, 8), Interval(34, 34), Interval(131, 135), Interval(68, 84)],
        [Interval(93, 117), Interval(151, 169), Interval(19, 19), Interval(184, 194), Interval(24, 26), Interval(94, 96), Interval(13, 17), Interval(118, 126), Interval(145, 185), Interval(2, 2), Interval(58, 74), Interval(98, 124), Interval(47, 55), Interval(77, 89), Interval(157, 209)],
        [Interval(54, 68), Interval(10, 12), Interval(119, 141), Interval(140, 154), Interval(92, 120), Interval(1, 1), Interval(139, 143), Interval(129, 143), Interval(29, 37), Interval(12, 14), Interval(13, 17), Interval(9, 11), Interval(55, 69), Interval(4, 4), Interval(132, 152)],
        [Interval(111, 123), Interval(10, 12), Interval(156, 168), Interval(174, 210), Interval(34, 36), Interval(166, 178), Interval(4, 4), Interval(173, 213), Interval(122, 160), Interval(138, 140), Interval(61, 63), Interval(11, 13), Interval(1, 1), Interval(124, 146), Interval(24, 26)],
        [Interval(47, 59), Interval(87, 91), Interval(156, 180), Interval(40, 42), Interval(112, 130), Interval(163, 199), Interval(37, 49), Interval(116, 120), Interval(57, 65), Interval(189, 197), Interval(108, 140), Interval(155, 197), Interval(28, 28), Interval(107, 143), Interval(126, 146)],
        [Interval(130, 174), Interval(102, 128), Interval(110, 134), Interval(5, 5), Interval(46, 46), Interval(139, 149), Interval(26, 32), Interval(175, 177), Interval(105, 125), Interval(16, 20), Interval(21, 25), Interval(23, 29), Interval(167, 183), Interval(103, 117), Interval(68, 82)],
        [Interval(47, 53), Interval(55, 69), Interval(184, 188), Interval(51, 63), Interval(140, 172), Interval(31, 33), Interval(118, 150), Interval(130, 152), Interval(176, 202), Interval(101, 135), Interval(89, 115), Interval(3, 3), Interval(169, 185), Interval(37, 49), Interval(40, 42)],
        [Interval(32, 38), Interval(146, 196), Interval(144, 176), Interval(28, 36), Interval(5, 5), Interval(141, 167), Interval(179, 211), Interval(111, 115), Interval(138, 186), Interval(146, 158), Interval(120, 160), Interval(62, 82), Interval(16, 16), Interval(98, 110), Interval(163, 179)],
        [Interval(62, 74), Interval(47, 61), Interval(107, 125), Interval(8, 10), Interval(93, 105), Interval(140, 170), Interval(19, 25), Interval(130, 140), Interval(64, 70), Interval(158, 172), Interval(96, 104), Interval(44, 50), Interval(45, 47), Interval(51, 59), Interval(12, 12)],
        [Interval(123, 147), Interval(103, 107), Interval(43, 55), Interval(4, 4), Interval(171, 181), Interval(47, 57), Interval(121, 135), Interval(174, 202), Interval(156, 184), Interval(168, 172), Interval(145, 193), Interval(61, 63), Interval(114, 126), Interval(27, 29), Interval(65, 75)],
        [Interval(92, 94), Interval(165, 179), Interval(121, 127), Interval(69, 75), Interval(178, 200), Interval(114, 130), Interval(36, 40), Interval(115, 125), Interval(109, 119), Interval(50, 52), Interval(73, 81), Interval(62, 68), Interval(153, 199), Interval(170, 172), Interval(148, 190)],
        [Interval(105, 139), Interval(19, 23), Interval(6, 6), Interval(174, 204), Interval(71, 79), Interval(5, 5), Interval(156, 204), Interval(146, 174), Interval(14, 14), Interval(63, 83), Interval(39, 51), Interval(58, 64), Interval(139, 157), Interval(93, 99), Interval(177, 211)],
        [Interval(94, 94), Interval(193, 203), Interval(86, 114), Interval(176, 212), Interval(123, 131), Interval(86, 104), Interval(39, 47), Interval(51, 53), Interval(151, 181), Interval(27, 35), Interval(99, 101), Interval(93, 115), Interval(143, 189), Interval(132, 146), Interval(123, 163)],
        [Interval(4, 4), Interval(69, 87), Interval(175, 223), Interval(105, 133), Interval(147, 187), Interval(47, 61), Interval(37, 39), Interval(110, 118), Interval(10, 10), Interval(108, 122), Interval(87, 115), Interval(104, 104), Interval(52, 70), Interval(75, 75), Interval(156, 194)],
        [Interval(18, 18), Interval(111, 119), Interval(159, 173), Interval(36, 46), Interval(113, 135), Interval(94, 108), Interval(35, 41), Interval(25, 33), Interval(80, 102), Interval(104, 132), Interval(34, 46), Interval(52, 58), Interval(76, 88), Interval(89, 89), Interval(85, 115)],
        [Interval(2, 2), Interval(92, 122), Interval(87, 111), Interval(136, 168), Interval(48, 54), Interval(12, 14), Interval(104, 120), Interval(93, 99), Interval(135, 165), Interval(93, 101), Interval(62, 72), Interval(56, 58), Interval(44, 46), Interval(15, 19), Interval(171, 197)],
        [Interval(157, 195), Interval(15, 15), Interval(89, 95), Interval(9, 9), Interval(70, 84), Interval(4, 4), Interval(72, 94), Interval(172, 218), Interval(134, 178), Interval(89, 115), Interval(80, 102), Interval(61, 69), Interval(17, 21), Interval(140, 186), Interval(88, 98)],
        [Interval(33, 43), Interval(29, 35), Interval(72, 88), Interval(101, 117), Interval(63, 79), Interval(98, 102), Interval(130, 148), Interval(49, 55), Interval(143, 183), Interval(39, 41), Interval(5, 5), Interval(24, 32), Interval(103, 107), Interval(162, 210), Interval(167, 205)],
        [Interval(1, 1), Interval(71, 75), Interval(95, 117), Interval(79, 81), Interval(143, 157), Interval(5, 5), Interval(71, 71), Interval(143, 147), Interval(121, 155), Interval(148, 148), Interval(168, 168), Interval(57, 63), Interval(95, 119), Interval(164, 164), Interval(175, 181)],
        [Interval(12, 16), Interval(5, 5), Interval(104, 126), Interval(61, 79), Interval(103, 121), Interval(74, 78), Interval(19, 21), Interval(102, 106), Interval(155, 179), Interval(51, 65), Interval(187, 199), Interval(28, 32), Interval(117, 147), Interval(6, 6), Interval(18, 20)],
    ],
    'name': 'int__dmu01.F.15_01_interval',
    'has_intervals': True,
    'description': 'DMU dmu01 ensanchada F.15_01',
}
