"""
Problema INT__DMU41.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Generado con el protocolo F.15_01 del paper (delta ~ U[0, 0.15],
intervalo simetrico, semilla fija) sobre la instancia crisp dmu41 de
Demirkol, Mehta y Uzsoy (1998).
"""

from jobshop_rl.models.interval import Interval


INT__DMU41_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__dmu41.F.15_01_interval',
    'sequences': [
        [4, 2, 1, 5, 3, 0, 6, 11, 10, 12, 8, 7, 13, 9, 14],
        [2, 0, 4, 1, 6, 3, 5, 7, 13, 9, 11, 8, 12, 10, 14],
        [0, 2, 4, 5, 1, 3, 6, 14, 7, 13, 12, 8, 9, 10, 11],
        [4, 2, 6, 5, 3, 0, 1, 14, 12, 9, 11, 10, 8, 13, 7],
        [4, 2, 1, 3, 6, 5, 0, 11, 8, 10, 14, 7, 9, 13, 12],
        [3, 0, 6, 5, 4, 2, 1, 10, 7, 14, 8, 13, 9, 11, 12],
        [0, 1, 5, 3, 2, 6, 4, 8, 7, 14, 11, 12, 9, 10, 13],
        [2, 3, 6, 5, 4, 1, 0, 10, 8, 13, 12, 11, 14, 9, 7],
        [6, 4, 0, 3, 2, 1, 5, 9, 8, 14, 7, 13, 10, 11, 12],
        [0, 1, 4, 2, 5, 3, 6, 10, 7, 13, 11, 9, 8, 12, 14],
        [5, 6, 0, 1, 2, 3, 4, 8, 7, 12, 13, 10, 9, 11, 14],
        [1, 6, 5, 0, 4, 2, 3, 9, 13, 12, 8, 7, 11, 10, 14],
        [6, 3, 2, 0, 5, 1, 4, 7, 14, 11, 8, 12, 13, 10, 9],
        [6, 3, 4, 0, 2, 5, 1, 14, 11, 8, 10, 7, 9, 12, 13],
        [3, 1, 5, 4, 2, 0, 6, 9, 12, 14, 8, 13, 7, 10, 11],
        [5, 3, 1, 0, 2, 4, 6, 10, 12, 9, 8, 11, 14, 7, 13],
        [6, 5, 1, 4, 2, 0, 3, 9, 7, 12, 11, 8, 13, 14, 10],
        [3, 6, 1, 0, 4, 5, 2, 12, 14, 7, 8, 9, 13, 11, 10],
        [4, 6, 3, 1, 5, 0, 2, 13, 9, 11, 8, 14, 10, 7, 12],
        [4, 3, 2, 1, 0, 6, 5, 11, 10, 7, 12, 13, 8, 14, 9],
    ],
    'durations': [
        [Interval(90, 98), Interval(7, 9), Interval(43, 51), Interval(185, 205), Interval(4, 4), Interval(79, 81), Interval(171, 209), Interval(69, 81), Interval(41, 55), Interval(107, 111), Interval(151, 185), Interval(149, 181), Interval(169, 181), Interval(24, 28), Interval(193, 199)],
        [Interval(49, 55), Interval(145, 157), Interval(93, 113), Interval(167, 197), Interval(98, 106), Interval(126, 162), Interval(121, 155), Interval(106, 112), Interval(138, 160), Interval(49, 55), Interval(119, 157), Interval(157, 179), Interval(23, 31), Interval(9, 11), Interval(168, 216)],
        [Interval(176, 186), Interval(145, 149), Interval(5, 5), Interval(39, 47), Interval(136, 166), Interval(39, 51), Interval(52, 62), Interval(68, 72), Interval(155, 173), Interval(97, 115), Interval(12, 14), Interval(14, 16), Interval(102, 130), Interval(156, 170), Interval(63, 75)],
        [Interval(107, 139), Interval(42, 44), Interval(107, 109), Interval(54, 62), Interval(173, 199), Interval(89, 105), Interval(165, 195), Interval(168, 218), Interval(166, 224), Interval(166, 198), Interval(60, 60), Interval(54, 68), Interval(98, 124), Interval(86, 114), Interval(138, 152)],
        [Interval(79, 103), Interval(87, 89), Interval(189, 201), Interval(20, 24), Interval(51, 65), Interval(153, 183), Interval(72, 74), Interval(135, 165), Interval(111, 145), Interval(102, 112), Interval(60, 62), Interval(30, 30), Interval(115, 137), Interval(139, 155), Interval(65, 87)],
        [Interval(19, 25), Interval(80, 94), Interval(144, 174), Interval(120, 130), Interval(149, 177), Interval(5, 5), Interval(30, 32), Interval(25, 27), Interval(3, 3), Interval(42, 50), Interval(88, 88), Interval(153, 197), Interval(95, 125), Interval(19, 19), Interval(12, 14)],
        [Interval(190, 196), Interval(155, 189), Interval(90, 98), Interval(33, 41), Interval(87, 89), Interval(135, 137), Interval(146, 164), Interval(27, 33), Interval(142, 158), Interval(115, 149), Interval(108, 140), Interval(169, 173), Interval(42, 48), Interval(53, 67), Interval(165, 187)],
        [Interval(89, 109), Interval(76, 86), Interval(122, 142), Interval(129, 131), Interval(63, 75), Interval(2, 2), Interval(129, 143), Interval(121, 125), Interval(23, 29), Interval(152, 188), Interval(112, 134), Interval(7, 7), Interval(103, 107), Interval(11, 11), Interval(158, 172)],
        [Interval(16, 16), Interval(148, 180), Interval(31, 33), Interval(148, 196), Interval(46, 56), Interval(121, 127), Interval(80, 84), Interval(126, 144), Interval(113, 149), Interval(110, 140), Interval(189, 199), Interval(5, 5), Interval(154, 182), Interval(124, 158), Interval(112, 126)],
        [Interval(79, 81), Interval(177, 199), Interval(103, 105), Interval(151, 155), Interval(6, 6), Interval(34, 42), Interval(15, 19), Interval(106, 112), Interval(171, 215), Interval(77, 99), Interval(112, 134), Interval(6, 8), Interval(101, 127), Interval(10, 12), Interval(44, 46)],
        [Interval(109, 147), Interval(183, 187), Interval(47, 57), Interval(27, 29), Interval(167, 191), Interval(189, 211), Interval(164, 176), Interval(120, 154), Interval(15, 19), Interval(83, 105), Interval(51, 67), Interval(75, 93), Interval(69, 85), Interval(122, 148), Interval(13, 13)],
        [Interval(171, 221), Interval(2, 2), Interval(87, 115), Interval(36, 38), Interval(5, 5), Interval(1, 1), Interval(177, 183), Interval(139, 145), Interval(44, 46), Interval(129, 143), Interval(106, 118), Interval(144, 162), Interval(173, 177), Interval(153, 175), Interval(177, 221)],
        [Interval(48, 50), Interval(39, 49), Interval(140, 154), Interval(107, 127), Interval(30, 36), Interval(180, 206), Interval(62, 78), Interval(41, 51), Interval(24, 24), Interval(142, 158), Interval(5, 5), Interval(3, 3), Interval(120, 148), Interval(98, 114), Interval(110, 146)],
        [Interval(84, 104), Interval(103, 109), Interval(143, 157), Interval(75, 85), Interval(139, 149), Interval(187, 189), Interval(25, 27), Interval(189, 203), Interval(20, 26), Interval(6, 8), Interval(169, 173), Interval(175, 195), Interval(67, 69), Interval(68, 88), Interval(151, 151)],
        [Interval(61, 75), Interval(53, 61), Interval(78, 94), Interval(173, 227), Interval(136, 168), Interval(54, 70), Interval(76, 92), Interval(17, 21), Interval(157, 173), Interval(139, 175), Interval(18, 20), Interval(71, 85), Interval(180, 198), Interval(59, 67), Interval(15, 19)],
        [Interval(148, 156), Interval(98, 100), Interval(111, 111), Interval(54, 58), Interval(18, 22), Interval(36, 40), Interval(156, 188), Interval(48, 62), Interval(78, 100), Interval(139, 151), Interval(154, 192), Interval(184, 214), Interval(137, 143), Interval(66, 68), Interval(136, 144)],
        [Interval(26, 28), Interval(45, 47), Interval(84, 90), Interval(38, 44), Interval(81, 89), Interval(84, 90), Interval(6, 8), Interval(131, 143), Interval(29, 31), Interval(64, 78), Interval(58, 74), Interval(160, 196), Interval(54, 72), Interval(20, 22), Interval(59, 59)],
        [Interval(89, 105), Interval(121, 159), Interval(13, 15), Interval(83, 89), Interval(49, 55), Interval(61, 81), Interval(111, 111), Interval(145, 147), Interval(30, 36), Interval(20, 22), Interval(118, 152), Interval(37, 43), Interval(118, 144), Interval(120, 126), Interval(20, 24)],
        [Interval(14, 18), Interval(87, 109), Interval(6, 8), Interval(164, 190), Interval(168, 194), Interval(103, 133), Interval(96, 100), Interval(66, 76), Interval(69, 73), Interval(145, 171), Interval(8, 8), Interval(173, 217), Interval(95, 103), Interval(36, 38), Interval(122, 144)],
        [Interval(98, 116), Interval(183, 195), Interval(110, 128), Interval(2, 2), Interval(157, 185), Interval(16, 20), Interval(20, 22), Interval(8, 10), Interval(113, 135), Interval(78, 102), Interval(119, 155), Interval(11, 13), Interval(74, 92), Interval(46, 54), Interval(88, 100)],
    ],
    'name': 'int__dmu41.F.15_01_interval',
    'has_intervals': True,
    'description': 'DMU dmu41 ensanchada F.15_01',
}
