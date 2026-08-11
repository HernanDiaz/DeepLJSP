"""
Problema INT__DMU03.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Generado con el protocolo F.15_01 del paper (delta ~ U[0, 0.15],
intervalo simetrico, semilla fija) sobre la instancia crisp dmu03 de
Demirkol, Mehta y Uzsoy (1998).
"""

from jobshop_rl.models.interval import Interval


INT__DMU03_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__dmu03.F.15_01_interval',
    'sequences': [
        [11, 12, 2, 3, 8, 0, 9, 6, 14, 5, 13, 1, 10, 4, 7],
        [14, 0, 8, 6, 2, 10, 7, 11, 4, 9, 13, 12, 5, 1, 3],
        [13, 3, 4, 11, 0, 10, 12, 2, 14, 5, 1, 6, 9, 8, 7],
        [13, 5, 3, 8, 12, 14, 2, 0, 6, 1, 4, 7, 9, 11, 10],
        [1, 11, 10, 8, 4, 9, 5, 12, 3, 0, 14, 13, 6, 7, 2],
        [6, 3, 5, 8, 1, 9, 0, 14, 13, 10, 12, 11, 4, 7, 2],
        [13, 11, 12, 14, 7, 2, 8, 6, 0, 9, 1, 10, 5, 3, 4],
        [6, 4, 12, 10, 5, 3, 1, 9, 13, 2, 11, 0, 8, 7, 14],
        [7, 11, 6, 5, 0, 8, 2, 9, 12, 4, 14, 10, 1, 13, 3],
        [14, 7, 4, 9, 6, 0, 13, 8, 3, 10, 2, 1, 12, 11, 5],
        [4, 3, 12, 8, 6, 0, 2, 7, 9, 5, 13, 11, 1, 10, 14],
        [4, 0, 7, 14, 1, 11, 5, 10, 2, 6, 8, 13, 3, 12, 9],
        [7, 6, 2, 9, 1, 8, 4, 11, 13, 5, 14, 12, 3, 0, 10],
        [14, 2, 10, 13, 0, 3, 1, 11, 6, 9, 4, 8, 7, 5, 12],
        [7, 4, 5, 2, 1, 12, 13, 8, 3, 9, 10, 6, 11, 0, 14],
        [7, 5, 3, 6, 11, 0, 8, 2, 13, 14, 12, 1, 4, 9, 10],
        [8, 7, 0, 14, 2, 10, 11, 13, 6, 9, 12, 3, 1, 4, 5],
        [4, 14, 13, 0, 12, 2, 8, 6, 11, 5, 7, 3, 1, 10, 9],
        [7, 1, 14, 3, 8, 12, 13, 5, 6, 9, 11, 2, 4, 0, 10],
        [12, 8, 3, 7, 11, 4, 13, 1, 0, 9, 10, 6, 2, 5, 14],
    ],
    'durations': [
        [Interval(75, 93), Interval(102, 136), Interval(123, 133), Interval(135, 153), Interval(158, 196), Interval(138, 164), Interval(118, 158), Interval(16, 16), Interval(194, 196), Interval(84, 102), Interval(101, 113), Interval(22, 22), Interval(135, 139), Interval(92, 100), Interval(20, 22)],
        [Interval(87, 103), Interval(81, 101), Interval(148, 158), Interval(97, 121), Interval(156, 208), Interval(42, 52), Interval(86, 110), Interval(50, 58), Interval(140, 178), Interval(120, 126), Interval(5, 5), Interval(5, 5), Interval(122, 160), Interval(77, 81), Interval(146, 174)],
        [Interval(83, 99), Interval(60, 64), Interval(157, 189), Interval(67, 67), Interval(130, 142), Interval(139, 141), Interval(105, 125), Interval(175, 191), Interval(159, 213), Interval(6, 6), Interval(188, 192), Interval(151, 195), Interval(126, 152), Interval(28, 28), Interval(161, 205)],
        [Interval(114, 124), Interval(178, 198), Interval(38, 48), Interval(17, 19), Interval(21, 25), Interval(50, 66), Interval(125, 147), Interval(47, 61), Interval(171, 217), Interval(33, 37), Interval(40, 40), Interval(30, 34), Interval(176, 192), Interval(99, 125), Interval(160, 212)],
        [Interval(185, 213), Interval(13, 13), Interval(58, 68), Interval(57, 59), Interval(55, 55), Interval(72, 92), Interval(21, 23), Interval(158, 208), Interval(38, 48), Interval(134, 180), Interval(25, 25), Interval(53, 67), Interval(149, 151), Interval(11, 13), Interval(115, 115)],
        [Interval(107, 119), Interval(98, 120), Interval(166, 204), Interval(57, 61), Interval(3, 3), Interval(23, 25), Interval(67, 75), Interval(84, 112), Interval(32, 32), Interval(96, 108), Interval(18, 20), Interval(19, 21), Interval(101, 123), Interval(13, 15), Interval(34, 44)],
        [Interval(166, 222), Interval(131, 135), Interval(107, 127), Interval(12, 14), Interval(107, 115), Interval(115, 137), Interval(86, 116), Interval(37, 39), Interval(175, 193), Interval(124, 146), Interval(89, 109), Interval(83, 101), Interval(140, 152), Interval(38, 50), Interval(151, 165)],
        [Interval(99, 107), Interval(83, 103), Interval(21, 21), Interval(129, 167), Interval(61, 71), Interval(26, 32), Interval(11, 11), Interval(4, 4), Interval(25, 31), Interval(80, 106), Interval(186, 198), Interval(58, 76), Interval(93, 99), Interval(14, 18), Interval(61, 67)],
        [Interval(116, 132), Interval(168, 202), Interval(134, 172), Interval(135, 151), Interval(26, 34), Interval(27, 27), Interval(67, 71), Interval(112, 148), Interval(53, 53), Interval(175, 203), Interval(75, 97), Interval(68, 88), Interval(134, 176), Interval(83, 91), Interval(103, 125)],
        [Interval(156, 180), Interval(5, 5), Interval(17, 17), Interval(179, 193), Interval(117, 149), Interval(30, 40), Interval(92, 110), Interval(162, 182), Interval(55, 57), Interval(108, 144), Interval(72, 78), Interval(84, 102), Interval(59, 75), Interval(103, 115), Interval(112, 142)],
        [Interval(79, 101), Interval(188, 210), Interval(178, 192), Interval(91, 97), Interval(34, 46), Interval(83, 101), Interval(146, 146), Interval(79, 101), Interval(115, 147), Interval(56, 58), Interval(117, 153), Interval(173, 207), Interval(167, 217), Interval(51, 61), Interval(90, 116)],
        [Interval(44, 46), Interval(45, 45), Interval(139, 175), Interval(12, 14), Interval(113, 139), Interval(38, 50), Interval(141, 163), Interval(126, 170), Interval(116, 128), Interval(153, 163), Interval(140, 156), Interval(95, 111), Interval(68, 70), Interval(90, 96), Interval(178, 206)],
        [Interval(94, 120), Interval(131, 143), Interval(12, 16), Interval(97, 129), Interval(138, 138), Interval(181, 183), Interval(164, 194), Interval(96, 118), Interval(107, 129), Interval(154, 190), Interval(150, 164), Interval(165, 191), Interval(121, 133), Interval(32, 36), Interval(72, 92)],
        [Interval(9, 9), Interval(141, 185), Interval(92, 116), Interval(19, 21), Interval(19, 23), Interval(47, 49), Interval(118, 144), Interval(8, 10), Interval(108, 142), Interval(86, 116), Interval(93, 119), Interval(169, 221), Interval(143, 179), Interval(69, 79), Interval(110, 120)],
        [Interval(180, 194), Interval(47, 63), Interval(70, 82), Interval(48, 64), Interval(55, 63), Interval(10, 12), Interval(66, 82), Interval(2, 2), Interval(177, 211), Interval(12, 14), Interval(99, 109), Interval(144, 150), Interval(144, 188), Interval(30, 38), Interval(101, 135)],
        [Interval(41, 49), Interval(145, 195), Interval(129, 141), Interval(71, 73), Interval(56, 56), Interval(129, 163), Interval(164, 216), Interval(49, 65), Interval(143, 153), Interval(39, 39), Interval(145, 181), Interval(13, 15), Interval(148, 188), Interval(96, 106), Interval(97, 101)],
        [Interval(97, 111), Interval(67, 83), Interval(158, 208), Interval(143, 161), Interval(151, 181), Interval(10, 10), Interval(106, 138), Interval(31, 33), Interval(88, 100), Interval(145, 177), Interval(147, 153), Interval(1, 1), Interval(90, 106), Interval(106, 120), Interval(24, 28)],
        [Interval(39, 45), Interval(61, 63), Interval(85, 87), Interval(101, 135), Interval(123, 133), Interval(152, 154), Interval(116, 152), Interval(144, 168), Interval(75, 85), Interval(96, 114), Interval(15, 17), Interval(160, 212), Interval(77, 91), Interval(40, 44), Interval(112, 146)],
        [Interval(139, 181), Interval(116, 122), Interval(80, 106), Interval(21, 23), Interval(166, 170), Interval(132, 144), Interval(155, 169), Interval(59, 71), Interval(48, 64), Interval(164, 178), Interval(17, 23), Interval(7, 9), Interval(134, 140), Interval(169, 217), Interval(88, 96)],
        [Interval(160, 210), Interval(17, 21), Interval(10, 12), Interval(83, 91), Interval(162, 180), Interval(14, 14), Interval(63, 67), Interval(57, 65), Interval(31, 37), Interval(84, 102), Interval(133, 175), Interval(64, 70), Interval(14, 14), Interval(123, 149), Interval(25, 29)],
    ],
    'name': 'int__dmu03.F.15_01_interval',
    'has_intervals': True,
    'description': 'DMU dmu03 ensanchada F.15_01',
}
