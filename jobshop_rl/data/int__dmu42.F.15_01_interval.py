"""
Problema INT__DMU42.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Generado con el protocolo F.15_01 del paper (delta ~ U[0, 0.15],
intervalo simetrico, semilla fija) sobre la instancia crisp dmu42 de
Demirkol, Mehta y Uzsoy (1998).
"""

from jobshop_rl.models.interval import Interval


INT__DMU42_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__dmu42.F.15_01_interval',
    'sequences': [
        [2, 5, 4, 0, 1, 3, 6, 13, 7, 11, 9, 10, 14, 8, 12],
        [5, 6, 4, 0, 3, 1, 2, 7, 8, 9, 12, 13, 14, 10, 11],
        [2, 4, 1, 6, 0, 5, 3, 10, 12, 14, 11, 9, 7, 8, 13],
        [3, 5, 2, 0, 1, 6, 4, 9, 14, 13, 8, 11, 7, 12, 10],
        [6, 4, 0, 5, 2, 1, 3, 7, 8, 14, 9, 10, 13, 12, 11],
        [2, 0, 3, 5, 1, 6, 4, 7, 11, 13, 12, 8, 10, 14, 9],
        [2, 6, 5, 4, 1, 3, 0, 11, 10, 13, 14, 9, 8, 7, 12],
        [3, 0, 1, 2, 4, 5, 6, 11, 9, 10, 8, 13, 12, 14, 7],
        [2, 1, 4, 0, 3, 6, 5, 7, 8, 9, 10, 11, 12, 13, 14],
        [3, 5, 2, 1, 6, 0, 4, 11, 7, 14, 12, 8, 10, 13, 9],
        [0, 1, 3, 2, 4, 5, 6, 11, 10, 7, 12, 14, 9, 13, 8],
        [5, 6, 2, 1, 0, 3, 4, 13, 7, 14, 8, 10, 9, 12, 11],
        [5, 2, 3, 4, 0, 1, 6, 11, 14, 9, 12, 10, 13, 7, 8],
        [4, 2, 1, 0, 3, 6, 5, 11, 9, 10, 14, 12, 8, 13, 7],
        [4, 3, 2, 6, 5, 1, 0, 8, 10, 9, 11, 14, 13, 12, 7],
        [5, 1, 2, 6, 0, 3, 4, 12, 8, 9, 14, 10, 11, 13, 7],
        [3, 1, 2, 4, 0, 5, 6, 14, 11, 10, 13, 7, 12, 8, 9],
        [5, 2, 3, 1, 4, 6, 0, 8, 11, 9, 7, 12, 13, 10, 14],
        [2, 4, 5, 0, 1, 6, 3, 9, 10, 11, 8, 7, 13, 14, 12],
        [4, 2, 0, 5, 6, 1, 3, 7, 9, 10, 8, 14, 13, 12, 11],
    ],
    'durations': [
        [Interval(37, 39), Interval(63, 63), Interval(102, 116), Interval(151, 151), Interval(180, 200), Interval(23, 27), Interval(177, 199), Interval(65, 67), Interval(59, 63), Interval(120, 134), Interval(138, 184), Interval(10, 10), Interval(167, 173), Interval(79, 81), Interval(123, 133)],
        [Interval(46, 50), Interval(152, 202), Interval(72, 72), Interval(33, 35), Interval(85, 107), Interval(159, 183), Interval(143, 183), Interval(114, 132), Interval(181, 219), Interval(78, 84), Interval(64, 76), Interval(165, 201), Interval(86, 110), Interval(94, 108), Interval(167, 219)],
        [Interval(59, 73), Interval(123, 147), Interval(9, 9), Interval(45, 49), Interval(29, 37), Interval(11, 13), Interval(133, 153), Interval(15, 19), Interval(80, 102), Interval(119, 151), Interval(62, 72), Interval(64, 78), Interval(141, 151), Interval(35, 47), Interval(12, 14)],
        [Interval(156, 166), Interval(161, 173), Interval(147, 173), Interval(99, 117), Interval(131, 163), Interval(79, 89), Interval(129, 161), Interval(78, 104), Interval(24, 26), Interval(83, 97), Interval(70, 78), Interval(85, 101), Interval(167, 171), Interval(88, 104), Interval(140, 148)],
        [Interval(112, 138), Interval(46, 58), Interval(44, 44), Interval(185, 199), Interval(79, 79), Interval(156, 210), Interval(84, 108), Interval(45, 55), Interval(62, 70), Interval(35, 47), Interval(141, 179), Interval(79, 97), Interval(73, 97), Interval(19, 23), Interval(154, 178)],
        [Interval(29, 33), Interval(181, 201), Interval(27, 33), Interval(107, 133), Interval(7, 9), Interval(34, 44), Interval(108, 132), Interval(137, 161), Interval(119, 153), Interval(122, 150), Interval(171, 189), Interval(27, 33), Interval(18, 20), Interval(170, 224), Interval(72, 94)],
        [Interval(83, 95), Interval(47, 61), Interval(161, 171), Interval(144, 176), Interval(155, 189), Interval(55, 61), Interval(175, 175), Interval(172, 188), Interval(156, 194), Interval(39, 51), Interval(167, 201), Interval(5, 5), Interval(57, 67), Interval(85, 93), Interval(145, 159)],
        [Interval(182, 204), Interval(167, 223), Interval(25, 31), Interval(78, 90), Interval(90, 120), Interval(86, 88), Interval(13, 17), Interval(1, 1), Interval(145, 195), Interval(92, 120), Interval(176, 208), Interval(34, 40), Interval(176, 182), Interval(166, 224), Interval(169, 191)],
        [Interval(122, 150), Interval(87, 117), Interval(38, 48), Interval(138, 162), Interval(98, 100), Interval(44, 44), Interval(101, 129), Interval(27, 31), Interval(144, 160), Interval(17, 19), Interval(94, 96), Interval(166, 172), Interval(5, 5), Interval(141, 187), Interval(40, 52)],
        [Interval(163, 183), Interval(137, 181), Interval(10, 12), Interval(152, 152), Interval(44, 56), Interval(82, 100), Interval(20, 22), Interval(96, 118), Interval(113, 117), Interval(110, 146), Interval(165, 203), Interval(159, 183), Interval(151, 197), Interval(70, 90), Interval(151, 165)],
        [Interval(163, 207), Interval(131, 149), Interval(57, 61), Interval(161, 217), Interval(68, 90), Interval(110, 136), Interval(99, 123), Interval(129, 173), Interval(39, 49), Interval(109, 135), Interval(84, 94), Interval(16, 20), Interval(29, 31), Interval(182, 194), Interval(148, 162)],
        [Interval(170, 198), Interval(136, 148), Interval(43, 57), Interval(105, 111), Interval(83, 107), Interval(170, 196), Interval(13, 15), Interval(105, 121), Interval(76, 100), Interval(102, 124), Interval(171, 223), Interval(166, 220), Interval(45, 59), Interval(80, 88), Interval(134, 156)],
        [Interval(138, 154), Interval(134, 152), Interval(64, 64), Interval(73, 97), Interval(186, 186), Interval(19, 25), Interval(153, 203), Interval(56, 58), Interval(173, 189), Interval(110, 120), Interval(50, 64), Interval(72, 94), Interval(58, 64), Interval(101, 107), Interval(159, 167)],
        [Interval(137, 163), Interval(106, 136), Interval(105, 123), Interval(15, 17), Interval(165, 173), Interval(140, 154), Interval(14, 16), Interval(157, 161), Interval(55, 63), Interval(89, 99), Interval(67, 85), Interval(67, 85), Interval(158, 192), Interval(152, 154), Interval(145, 189)],
        [Interval(48, 62), Interval(106, 142), Interval(105, 111), Interval(119, 155), Interval(94, 116), Interval(18, 18), Interval(74, 88), Interval(132, 140), Interval(178, 222), Interval(161, 177), Interval(127, 149), Interval(165, 177), Interval(8, 10), Interval(65, 73), Interval(62, 64)],
        [Interval(57, 67), Interval(183, 203), Interval(45, 57), Interval(123, 141), Interval(29, 39), Interval(139, 159), Interval(52, 70), Interval(47, 53), Interval(29, 33), Interval(80, 80), Interval(64, 76), Interval(52, 56), Interval(143, 189), Interval(181, 215), Interval(75, 79)],
        [Interval(58, 76), Interval(66, 84), Interval(104, 104), Interval(28, 36), Interval(118, 152), Interval(65, 83), Interval(57, 65), Interval(102, 128), Interval(37, 41), Interval(14, 16), Interval(131, 141), Interval(169, 227), Interval(1, 1), Interval(142, 188), Interval(33, 43)],
        [Interval(62, 74), Interval(26, 34), Interval(6, 6), Interval(73, 85), Interval(68, 80), Interval(68, 88), Interval(49, 63), Interval(63, 69), Interval(86, 112), Interval(127, 147), Interval(160, 196), Interval(192, 204), Interval(156, 194), Interval(83, 111), Interval(155, 205)],
        [Interval(77, 89), Interval(13, 13), Interval(53, 61), Interval(159, 201), Interval(30, 30), Interval(76, 102), Interval(63, 85), Interval(76, 80), Interval(157, 181), Interval(120, 122), Interval(179, 219), Interval(89, 103), Interval(24, 30), Interval(48, 60), Interval(141, 171)],
        [Interval(62, 82), Interval(130, 134), Interval(21, 21), Interval(91, 105), Interval(101, 107), Interval(27, 33), Interval(31, 39), Interval(191, 199), Interval(38, 42), Interval(183, 213), Interval(148, 150), Interval(15, 15), Interval(34, 36), Interval(126, 136), Interval(104, 116)],
    ],
    'name': 'int__dmu42.F.15_01_interval',
    'has_intervals': True,
    'description': 'DMU dmu42 ensanchada F.15_01',
}
