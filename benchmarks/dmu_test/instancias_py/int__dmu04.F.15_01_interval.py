"""
Problema INT__DMU04.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Generado con el protocolo F.15_01 del paper (delta ~ U[0, 0.15],
intervalo simetrico, semilla fija) sobre la instancia crisp dmu04 de
Demirkol, Mehta y Uzsoy (1998).
"""

from jobshop_rl.models.interval import Interval


INT__DMU04_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__dmu04.F.15_01_interval',
    'sequences': [
        [8, 10, 3, 2, 4, 0, 12, 7, 11, 13, 5, 1, 9, 6, 14],
        [14, 2, 8, 7, 9, 11, 4, 0, 12, 13, 10, 1, 5, 3, 6],
        [2, 12, 7, 8, 1, 10, 6, 5, 0, 9, 13, 11, 4, 3, 14],
        [5, 6, 2, 11, 7, 1, 3, 4, 14, 13, 8, 9, 0, 12, 10],
        [6, 10, 11, 4, 9, 5, 14, 8, 2, 3, 7, 12, 0, 1, 13],
        [0, 10, 13, 12, 11, 1, 3, 2, 5, 7, 6, 4, 8, 9, 14],
        [3, 0, 2, 8, 14, 5, 13, 10, 7, 11, 4, 9, 1, 6, 12],
        [11, 9, 1, 0, 5, 10, 12, 8, 13, 4, 7, 3, 6, 2, 14],
        [11, 8, 7, 2, 6, 3, 14, 0, 5, 13, 12, 4, 10, 9, 1],
        [5, 3, 12, 6, 14, 7, 1, 0, 8, 13, 4, 10, 2, 9, 11],
        [3, 12, 7, 9, 6, 11, 1, 5, 14, 13, 8, 10, 4, 0, 2],
        [12, 10, 0, 14, 9, 11, 5, 3, 13, 7, 1, 8, 6, 2, 4],
        [8, 7, 5, 2, 1, 9, 4, 13, 12, 10, 3, 14, 0, 6, 11],
        [3, 10, 13, 9, 2, 6, 4, 14, 12, 8, 0, 5, 11, 7, 1],
        [7, 6, 2, 13, 10, 11, 8, 5, 3, 0, 12, 1, 4, 14, 9],
        [10, 1, 13, 2, 14, 5, 3, 9, 11, 0, 12, 6, 4, 7, 8],
        [11, 2, 14, 7, 9, 8, 0, 4, 3, 5, 1, 6, 10, 13, 12],
        [0, 1, 2, 13, 8, 6, 10, 5, 9, 14, 4, 7, 12, 11, 3],
        [6, 9, 4, 1, 12, 5, 10, 14, 3, 2, 7, 8, 0, 13, 11],
        [9, 1, 10, 5, 3, 14, 13, 4, 0, 6, 7, 8, 11, 12, 2],
    ],
    'durations': [
        [Interval(179, 191), Interval(31, 37), Interval(93, 107), Interval(41, 51), Interval(93, 119), Interval(60, 74), Interval(72, 78), Interval(81, 105), Interval(47, 47), Interval(64, 76), Interval(180, 204), Interval(115, 153), Interval(73, 97), Interval(145, 153), Interval(42, 46)],
        [Interval(114, 138), Interval(57, 63), Interval(111, 113), Interval(129, 133), Interval(163, 207), Interval(84, 90), Interval(1, 1), Interval(174, 222), Interval(24, 32), Interval(136, 178), Interval(173, 215), Interval(56, 62), Interval(47, 61), Interval(2, 2), Interval(133, 179)],
        [Interval(18, 22), Interval(119, 159), Interval(147, 195), Interval(169, 227), Interval(18, 18), Interval(150, 188), Interval(129, 151), Interval(195, 201), Interval(109, 135), Interval(56, 64), Interval(107, 115), Interval(162, 218), Interval(99, 101), Interval(85, 93), Interval(17, 17)],
        [Interval(54, 72), Interval(31, 41), Interval(36, 46), Interval(180, 200), Interval(93, 113), Interval(122, 138), Interval(89, 101), Interval(149, 199), Interval(121, 133), Interval(154, 204), Interval(153, 161), Interval(106, 134), Interval(125, 139), Interval(188, 202), Interval(73, 81)],
        [Interval(50, 60), Interval(58, 60), Interval(17, 19), Interval(27, 29), Interval(112, 124), Interval(87, 91), Interval(104, 112), Interval(72, 90), Interval(84, 112), Interval(180, 184), Interval(8, 10), Interval(185, 207), Interval(114, 154), Interval(105, 117), Interval(41, 51)],
        [Interval(189, 191), Interval(2, 2), Interval(87, 93), Interval(17, 21), Interval(28, 30), Interval(14, 18), Interval(61, 81), Interval(130, 154), Interval(82, 98), Interval(21, 25), Interval(189, 189), Interval(97, 119), Interval(38, 44), Interval(35, 39), Interval(92, 104)],
        [Interval(128, 146), Interval(157, 191), Interval(113, 145), Interval(13, 15), Interval(51, 55), Interval(10, 12), Interval(120, 162), Interval(34, 38), Interval(64, 80), Interval(158, 164), Interval(183, 215), Interval(151, 159), Interval(98, 102), Interval(131, 145), Interval(144, 186)],
        [Interval(172, 204), Interval(92, 120), Interval(72, 86), Interval(53, 55), Interval(73, 81), Interval(141, 147), Interval(144, 160), Interval(96, 128), Interval(139, 159), Interval(190, 204), Interval(36, 44), Interval(64, 84), Interval(134, 144), Interval(79, 85), Interval(5, 5)],
        [Interval(58, 74), Interval(90, 96), Interval(92, 114), Interval(60, 74), Interval(114, 136), Interval(21, 27), Interval(134, 170), Interval(184, 188), Interval(7, 7), Interval(94, 118), Interval(140, 148), Interval(48, 50), Interval(120, 142), Interval(33, 37), Interval(176, 184)],
        [Interval(12, 14), Interval(51, 53), Interval(156, 190), Interval(119, 143), Interval(17, 21), Interval(63, 63), Interval(133, 133), Interval(17, 21), Interval(17, 17), Interval(101, 131), Interval(146, 150), Interval(90, 102), Interval(73, 87), Interval(163, 183), Interval(53, 65)],
        [Interval(182, 194), Interval(13, 13), Interval(52, 68), Interval(83, 87), Interval(181, 195), Interval(40, 42), Interval(46, 48), Interval(16, 20), Interval(35, 41), Interval(114, 154), Interval(3, 3), Interval(110, 120), Interval(96, 98), Interval(75, 77), Interval(70, 86)],
        [Interval(80, 106), Interval(197, 201), Interval(53, 53), Interval(140, 188), Interval(177, 197), Interval(90, 112), Interval(54, 68), Interval(49, 55), Interval(115, 123), Interval(156, 176), Interval(41, 55), Interval(26, 32), Interval(51, 67), Interval(92, 104), Interval(12, 14)],
        [Interval(13, 15), Interval(170, 202), Interval(134, 180), Interval(47, 57), Interval(34, 34), Interval(91, 107), Interval(85, 99), Interval(45, 53), Interval(89, 101), Interval(89, 113), Interval(165, 185), Interval(189, 195), Interval(104, 104), Interval(47, 57), Interval(67, 73)],
        [Interval(150, 174), Interval(40, 46), Interval(113, 145), Interval(81, 91), Interval(103, 129), Interval(79, 103), Interval(33, 41), Interval(68, 82), Interval(104, 108), Interval(77, 95), Interval(36, 36), Interval(116, 128), Interval(160, 178), Interval(177, 197), Interval(164, 178)],
        [Interval(120, 132), Interval(111, 129), Interval(67, 87), Interval(114, 152), Interval(168, 214), Interval(151, 195), Interval(161, 175), Interval(164, 168), Interval(171, 179), Interval(148, 164), Interval(26, 26), Interval(129, 165), Interval(131, 141), Interval(60, 72), Interval(45, 51)],
        [Interval(58, 72), Interval(40, 44), Interval(62, 70), Interval(129, 173), Interval(112, 122), Interval(70, 76), Interval(136, 184), Interval(147, 175), Interval(23, 23), Interval(61, 79), Interval(158, 178), Interval(68, 82), Interval(132, 168), Interval(89, 91), Interval(144, 192)],
        [Interval(52, 52), Interval(176, 206), Interval(112, 150), Interval(59, 67), Interval(124, 166), Interval(174, 194), Interval(171, 223), Interval(23, 25), Interval(186, 192), Interval(25, 29), Interval(54, 60), Interval(84, 90), Interval(43, 51), Interval(160, 176), Interval(132, 166)],
        [Interval(69, 75), Interval(43, 51), Interval(96, 122), Interval(8, 10), Interval(31, 41), Interval(79, 91), Interval(68, 84), Interval(94, 108), Interval(178, 190), Interval(109, 131), Interval(121, 133), Interval(117, 141), Interval(87, 115), Interval(5, 5), Interval(164, 196)],
        [Interval(72, 94), Interval(168, 176), Interval(22, 28), Interval(94, 114), Interval(110, 130), Interval(140, 150), Interval(163, 201), Interval(49, 61), Interval(42, 54), Interval(190, 204), Interval(160, 192), Interval(160, 190), Interval(37, 47), Interval(17, 19), Interval(50, 58)],
        [Interval(8, 10), Interval(82, 90), Interval(79, 83), Interval(133, 155), Interval(25, 33), Interval(160, 206), Interval(33, 41), Interval(185, 213), Interval(68, 90), Interval(159, 171), Interval(39, 51), Interval(24, 26), Interval(13, 15), Interval(155, 195), Interval(168, 214)],
    ],
    'name': 'int__dmu04.F.15_01_interval',
    'has_intervals': True,
    'description': 'DMU dmu04 ensanchada F.15_01',
}
