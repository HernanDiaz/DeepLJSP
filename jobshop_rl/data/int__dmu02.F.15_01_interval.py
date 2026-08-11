"""
Problema INT__DMU02.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Generado con el protocolo F.15_01 del paper (delta ~ U[0, 0.15],
intervalo simetrico, semilla fija) sobre la instancia crisp dmu02 de
Demirkol, Mehta y Uzsoy (1998).
"""

from jobshop_rl.models.interval import Interval


INT__DMU02_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__dmu02.F.15_01_interval',
    'sequences': [
        [3, 9, 10, 4, 1, 12, 2, 11, 0, 8, 5, 14, 7, 6, 13],
        [13, 11, 2, 1, 6, 0, 10, 4, 3, 14, 7, 8, 12, 5, 9],
        [4, 6, 8, 14, 5, 11, 7, 10, 3, 1, 9, 12, 2, 0, 13],
        [10, 11, 14, 9, 2, 4, 6, 13, 3, 7, 12, 8, 5, 1, 0],
        [8, 14, 5, 4, 11, 9, 7, 13, 1, 3, 0, 2, 10, 12, 6],
        [1, 2, 6, 10, 14, 3, 9, 7, 5, 8, 4, 13, 0, 11, 12],
        [11, 1, 4, 5, 7, 9, 3, 13, 10, 0, 14, 2, 12, 8, 6],
        [9, 11, 3, 0, 12, 8, 7, 4, 13, 5, 1, 10, 2, 6, 14],
        [3, 9, 7, 2, 5, 14, 13, 6, 11, 10, 0, 4, 1, 12, 8],
        [14, 13, 12, 8, 6, 10, 9, 5, 4, 2, 0, 1, 3, 7, 11],
        [1, 4, 11, 7, 12, 13, 14, 8, 0, 9, 3, 2, 5, 10, 6],
        [4, 14, 3, 8, 13, 6, 5, 1, 0, 11, 9, 10, 12, 7, 2],
        [0, 14, 7, 8, 11, 5, 2, 9, 13, 1, 10, 4, 3, 6, 12],
        [8, 4, 7, 9, 14, 2, 12, 10, 13, 0, 5, 1, 11, 3, 6],
        [14, 2, 10, 12, 6, 11, 1, 0, 8, 13, 5, 7, 3, 9, 4],
        [13, 14, 9, 1, 8, 4, 2, 6, 5, 0, 10, 11, 12, 7, 3],
        [1, 9, 2, 10, 0, 8, 5, 7, 13, 11, 3, 4, 6, 14, 12],
        [2, 7, 8, 11, 0, 9, 1, 6, 3, 4, 12, 10, 5, 14, 13],
        [0, 12, 11, 1, 13, 9, 3, 6, 7, 4, 14, 8, 10, 2, 5],
        [14, 2, 11, 13, 0, 10, 4, 1, 5, 6, 12, 3, 8, 7, 9],
    ],
    'durations': [
        [Interval(59, 69), Interval(22, 26), Interval(49, 53), Interval(109, 119), Interval(68, 92), Interval(97, 123), Interval(56, 70), Interval(128, 144), Interval(49, 57), Interval(179, 185), Interval(131, 137), Interval(116, 134), Interval(53, 71), Interval(51, 65), Interval(173, 181)],
        [Interval(45, 59), Interval(165, 211), Interval(74, 82), Interval(80, 106), Interval(95, 125), Interval(44, 52), Interval(158, 184), Interval(10, 12), Interval(100, 126), Interval(134, 154), Interval(93, 99), Interval(164, 200), Interval(58, 68), Interval(135, 169), Interval(96, 118)],
        [Interval(74, 98), Interval(29, 29), Interval(170, 204), Interval(74, 80), Interval(34, 44), Interval(138, 150), Interval(93, 103), Interval(99, 117), Interval(47, 49), Interval(39, 41), Interval(143, 181), Interval(88, 90), Interval(34, 38), Interval(105, 109), Interval(46, 60)],
        [Interval(46, 50), Interval(25, 31), Interval(61, 81), Interval(112, 112), Interval(127, 153), Interval(10, 12), Interval(99, 111), Interval(24, 24), Interval(68, 90), Interval(184, 198), Interval(83, 85), Interval(32, 32), Interval(89, 109), Interval(45, 47), Interval(140, 140)],
        [Interval(153, 163), Interval(12, 14), Interval(115, 137), Interval(45, 49), Interval(12, 14), Interval(149, 195), Interval(32, 34), Interval(156, 178), Interval(112, 116), Interval(20, 26), Interval(153, 195), Interval(69, 87), Interval(138, 184), Interval(183, 187), Interval(129, 159)],
        [Interval(28, 30), Interval(155, 169), Interval(184, 208), Interval(28, 30), Interval(42, 42), Interval(8, 8), Interval(165, 185), Interval(124, 158), Interval(35, 39), Interval(24, 24), Interval(131, 167), Interval(10, 12), Interval(34, 44), Interval(28, 34), Interval(21, 27)],
        [Interval(83, 105), Interval(21, 23), Interval(66, 76), Interval(82, 102), Interval(73, 83), Interval(51, 57), Interval(16, 18), Interval(134, 178), Interval(56, 58), Interval(8, 8), Interval(10, 10), Interval(119, 149), Interval(125, 143), Interval(42, 44), Interval(54, 70)],
        [Interval(128, 164), Interval(94, 96), Interval(146, 190), Interval(163, 195), Interval(176, 186), Interval(97, 119), Interval(117, 121), Interval(122, 130), Interval(121, 139), Interval(114, 126), Interval(173, 191), Interval(109, 143), Interval(160, 190), Interval(118, 144), Interval(178, 184)],
        [Interval(147, 169), Interval(10, 12), Interval(93, 119), Interval(70, 84), Interval(25, 31), Interval(123, 163), Interval(173, 221), Interval(133, 155), Interval(71, 93), Interval(117, 123), Interval(112, 146), Interval(46, 62), Interval(84, 98), Interval(67, 89), Interval(71, 79)],
        [Interval(179, 191), Interval(94, 104), Interval(138, 180), Interval(67, 75), Interval(108, 112), Interval(73, 95), Interval(144, 150), Interval(143, 161), Interval(98, 124), Interval(47, 51), Interval(153, 163), Interval(115, 139), Interval(45, 57), Interval(83, 85), Interval(63, 77)],
        [Interval(115, 149), Interval(172, 188), Interval(45, 53), Interval(65, 65), Interval(181, 215), Interval(131, 135), Interval(141, 165), Interval(48, 50), Interval(146, 192), Interval(13, 15), Interval(64, 72), Interval(59, 71), Interval(7, 7), Interval(118, 158), Interval(67, 67)],
        [Interval(23, 31), Interval(177, 191), Interval(90, 94), Interval(76, 100), Interval(127, 135), Interval(101, 111), Interval(55, 71), Interval(10, 10), Interval(67, 77), Interval(21, 23), Interval(12, 12), Interval(158, 162), Interval(149, 159), Interval(87, 105), Interval(75, 87)],
        [Interval(119, 121), Interval(153, 183), Interval(167, 191), Interval(10, 12), Interval(133, 179), Interval(150, 176), Interval(5, 5), Interval(116, 152), Interval(83, 85), Interval(89, 113), Interval(51, 55), Interval(19, 23), Interval(16, 16), Interval(123, 163), Interval(22, 28)],
        [Interval(142, 186), Interval(95, 123), Interval(141, 179), Interval(165, 205), Interval(12, 12), Interval(180, 206), Interval(74, 94), Interval(177, 203), Interval(146, 156), Interval(171, 175), Interval(157, 209), Interval(4, 4), Interval(184, 212), Interval(169, 189), Interval(53, 69)],
        [Interval(73, 81), Interval(149, 179), Interval(108, 130), Interval(12, 14), Interval(177, 199), Interval(162, 200), Interval(63, 71), Interval(51, 59), Interval(77, 99), Interval(110, 138), Interval(73, 73), Interval(164, 218), Interval(177, 211), Interval(87, 111), Interval(167, 171)],
        [Interval(159, 193), Interval(81, 93), Interval(133, 133), Interval(6, 6), Interval(135, 149), Interval(152, 182), Interval(79, 91), Interval(51, 63), Interval(55, 65), Interval(130, 156), Interval(105, 129), Interval(158, 170), Interval(142, 160), Interval(40, 50), Interval(157, 199)],
        [Interval(157, 209), Interval(4, 4), Interval(21, 21), Interval(166, 210), Interval(173, 187), Interval(78, 86), Interval(118, 158), Interval(20, 24), Interval(116, 132), Interval(107, 111), Interval(49, 65), Interval(7, 9), Interval(91, 119), Interval(136, 164), Interval(28, 30)],
        [Interval(44, 44), Interval(90, 118), Interval(66, 88), Interval(7, 9), Interval(5, 5), Interval(19, 25), Interval(60, 68), Interval(149, 185), Interval(84, 108), Interval(24, 30), Interval(125, 157), Interval(6, 6), Interval(100, 126), Interval(49, 59), Interval(23, 29)],
        [Interval(141, 149), Interval(34, 38), Interval(139, 173), Interval(65, 77), Interval(33, 41), Interval(134, 160), Interval(78, 92), Interval(59, 59), Interval(132, 160), Interval(28, 34), Interval(121, 131), Interval(118, 158), Interval(152, 156), Interval(127, 157), Interval(95, 97)],
        [Interval(168, 216), Interval(127, 165), Interval(159, 175), Interval(45, 55), Interval(168, 192), Interval(169, 173), Interval(93, 95), Interval(163, 167), Interval(25, 29), Interval(32, 42), Interval(71, 89), Interval(173, 215), Interval(118, 150), Interval(46, 60), Interval(13, 15)],
    ],
    'name': 'int__dmu02.F.15_01_interval',
    'has_intervals': True,
    'description': 'DMU dmu02 ensanchada F.15_01',
}
