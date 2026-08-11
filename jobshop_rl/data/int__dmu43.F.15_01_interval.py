"""
Problema INT__DMU43.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Generado con el protocolo F.15_01 del paper (delta ~ U[0, 0.15],
intervalo simetrico, semilla fija) sobre la instancia crisp dmu43 de
Demirkol, Mehta y Uzsoy (1998).
"""

from jobshop_rl.models.interval import Interval


INT__DMU43_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__dmu43.F.15_01_interval',
    'sequences': [
        [1, 4, 5, 0, 6, 3, 2, 10, 13, 11, 7, 12, 14, 8, 9],
        [3, 0, 5, 4, 1, 6, 2, 12, 8, 7, 10, 13, 9, 14, 11],
        [6, 0, 5, 1, 2, 4, 3, 9, 10, 13, 8, 11, 7, 12, 14],
        [3, 2, 1, 6, 0, 4, 5, 14, 10, 9, 13, 11, 8, 12, 7],
        [3, 2, 6, 5, 0, 1, 4, 12, 11, 8, 10, 13, 7, 14, 9],
        [6, 4, 1, 3, 5, 0, 2, 8, 11, 12, 7, 9, 10, 14, 13],
        [3, 4, 1, 6, 0, 5, 2, 11, 14, 13, 12, 10, 9, 8, 7],
        [1, 6, 5, 2, 4, 3, 0, 11, 10, 7, 14, 13, 12, 8, 9],
        [6, 3, 0, 2, 1, 4, 5, 12, 7, 9, 11, 10, 14, 13, 8],
        [1, 6, 2, 3, 5, 0, 4, 10, 7, 11, 8, 13, 9, 12, 14],
        [1, 3, 4, 2, 0, 6, 5, 10, 11, 13, 12, 9, 14, 8, 7],
        [0, 3, 2, 4, 5, 6, 1, 9, 13, 11, 7, 10, 8, 14, 12],
        [5, 2, 6, 4, 1, 0, 3, 13, 14, 8, 11, 7, 9, 10, 12],
        [2, 5, 0, 1, 4, 3, 6, 14, 11, 12, 13, 8, 7, 9, 10],
        [6, 0, 3, 2, 5, 4, 1, 11, 14, 9, 8, 7, 13, 10, 12],
        [1, 6, 2, 3, 0, 4, 5, 11, 14, 8, 7, 9, 10, 13, 12],
        [1, 3, 4, 5, 6, 0, 2, 10, 11, 12, 7, 13, 14, 8, 9],
        [3, 0, 4, 5, 1, 6, 2, 11, 14, 13, 7, 8, 10, 9, 12],
        [4, 6, 5, 2, 1, 0, 3, 8, 11, 10, 12, 7, 14, 9, 13],
        [3, 2, 6, 5, 0, 4, 1, 12, 14, 8, 10, 13, 7, 9, 11],
    ],
    'durations': [
        [Interval(70, 94), Interval(135, 139), Interval(82, 104), Interval(138, 140), Interval(68, 76), Interval(52, 70), Interval(92, 96), Interval(161, 203), Interval(117, 151), Interval(57, 63), Interval(45, 51), Interval(49, 65), Interval(21, 25), Interval(60, 64), Interval(76, 88)],
        [Interval(12, 14), Interval(56, 66), Interval(61, 75), Interval(169, 203), Interval(162, 184), Interval(116, 126), Interval(120, 146), Interval(5, 5), Interval(175, 215), Interval(100, 100), Interval(46, 46), Interval(26, 30), Interval(27, 33), Interval(1, 1), Interval(22, 24)],
        [Interval(172, 186), Interval(160, 168), Interval(121, 125), Interval(149, 175), Interval(182, 208), Interval(132, 166), Interval(115, 137), Interval(53, 53), Interval(23, 23), Interval(59, 77), Interval(173, 197), Interval(158, 162), Interval(14, 18), Interval(127, 163), Interval(37, 45)],
        [Interval(72, 92), Interval(2, 2), Interval(75, 91), Interval(156, 190), Interval(86, 94), Interval(102, 128), Interval(143, 187), Interval(137, 165), Interval(114, 128), Interval(16, 18), Interval(78, 98), Interval(15, 19), Interval(101, 109), Interval(12, 16), Interval(38, 42)],
        [Interval(112, 124), Interval(70, 84), Interval(20, 22), Interval(128, 158), Interval(6, 6), Interval(154, 186), Interval(75, 85), Interval(102, 104), Interval(159, 161), Interval(140, 178), Interval(25, 31), Interval(150, 154), Interval(1, 1), Interval(64, 64), Interval(80, 108)],
        [Interval(9, 9), Interval(152, 166), Interval(111, 119), Interval(69, 83), Interval(25, 27), Interval(35, 47), Interval(34, 36), Interval(35, 35), Interval(107, 111), Interval(94, 116), Interval(131, 149), Interval(35, 47), Interval(22, 24), Interval(16, 16), Interval(179, 183)],
        [Interval(74, 84), Interval(50, 54), Interval(139, 141), Interval(198, 198), Interval(175, 207), Interval(113, 143), Interval(42, 44), Interval(9, 11), Interval(7, 7), Interval(160, 204), Interval(131, 133), Interval(98, 102), Interval(97, 97), Interval(164, 220), Interval(32, 38)],
        [Interval(23, 25), Interval(172, 172), Interval(59, 75), Interval(124, 156), Interval(44, 54), Interval(121, 133), Interval(6, 8), Interval(35, 45), Interval(39, 41), Interval(25, 31), Interval(93, 97), Interval(136, 140), Interval(165, 207), Interval(66, 86), Interval(124, 160)],
        [Interval(118, 134), Interval(141, 175), Interval(87, 105), Interval(22, 28), Interval(63, 67), Interval(93, 109), Interval(165, 171), Interval(92, 116), Interval(193, 207), Interval(39, 51), Interval(107, 131), Interval(122, 128), Interval(119, 125), Interval(128, 128), Interval(168, 196)],
        [Interval(22, 26), Interval(80, 88), Interval(74, 74), Interval(139, 153), Interval(163, 197), Interval(21, 27), Interval(170, 176), Interval(1, 1), Interval(117, 135), Interval(154, 208), Interval(42, 44), Interval(93, 119), Interval(76, 100), Interval(59, 77), Interval(47, 51)],
        [Interval(69, 77), Interval(135, 157), Interval(153, 185), Interval(155, 173), Interval(157, 165), Interval(72, 88), Interval(6, 8), Interval(166, 192), Interval(166, 206), Interval(46, 50), Interval(16, 18), Interval(39, 43), Interval(56, 66), Interval(74, 90), Interval(2, 2)],
        [Interval(189, 199), Interval(6, 8), Interval(109, 125), Interval(92, 104), Interval(143, 151), Interval(92, 94), Interval(128, 166), Interval(131, 145), Interval(15, 19), Interval(10, 12), Interval(101, 123), Interval(91, 101), Interval(161, 211), Interval(173, 207), Interval(151, 157)],
        [Interval(171, 213), Interval(98, 122), Interval(84, 88), Interval(38, 38), Interval(154, 196), Interval(50, 54), Interval(25, 33), Interval(163, 167), Interval(126, 142), Interval(93, 117), Interval(177, 203), Interval(7, 7), Interval(19, 23), Interval(106, 122), Interval(12, 12)],
        [Interval(76, 100), Interval(188, 188), Interval(98, 102), Interval(144, 172), Interval(146, 166), Interval(41, 43), Interval(17, 21), Interval(51, 65), Interval(192, 198), Interval(168, 172), Interval(21, 23), Interval(23, 29), Interval(106, 124), Interval(47, 63), Interval(5, 5)],
        [Interval(173, 199), Interval(67, 87), Interval(35, 37), Interval(147, 175), Interval(196, 202), Interval(31, 31), Interval(167, 199), Interval(173, 211), Interval(145, 151), Interval(59, 65), Interval(125, 139), Interval(115, 123), Interval(64, 72), Interval(180, 204), Interval(111, 147)],
        [Interval(163, 203), Interval(2, 2), Interval(3, 3), Interval(121, 129), Interval(77, 81), Interval(62, 74), Interval(143, 147), Interval(112, 122), Interval(123, 137), Interval(15, 15), Interval(24, 28), Interval(174, 204), Interval(150, 202), Interval(156, 160), Interval(162, 214)],
        [Interval(178, 196), Interval(69, 69), Interval(73, 91), Interval(46, 56), Interval(99, 107), Interval(175, 193), Interval(102, 116), Interval(139, 149), Interval(150, 176), Interval(102, 132), Interval(83, 95), Interval(34, 38), Interval(94, 108), Interval(114, 122), Interval(142, 182)],
        [Interval(16, 20), Interval(78, 98), Interval(150, 172), Interval(48, 50), Interval(130, 162), Interval(50, 60), Interval(176, 212), Interval(98, 132), Interval(170, 206), Interval(56, 58), Interval(103, 137), Interval(167, 219), Interval(89, 105), Interval(146, 190), Interval(136, 168)],
        [Interval(173, 219), Interval(9, 11), Interval(104, 126), Interval(120, 130), Interval(126, 168), Interval(22, 28), Interval(59, 75), Interval(161, 177), Interval(95, 119), Interval(6, 6), Interval(141, 179), Interval(120, 148), Interval(33, 37), Interval(70, 92), Interval(57, 63)],
        [Interval(24, 26), Interval(174, 208), Interval(83, 87), Interval(101, 135), Interval(181, 219), Interval(182, 214), Interval(77, 95), Interval(114, 132), Interval(136, 180), Interval(141, 177), Interval(9, 11), Interval(16, 18), Interval(43, 51), Interval(23, 29), Interval(52, 64)],
    ],
    'name': 'int__dmu43.F.15_01_interval',
    'has_intervals': True,
    'description': 'DMU dmu43 ensanchada F.15_01',
}
