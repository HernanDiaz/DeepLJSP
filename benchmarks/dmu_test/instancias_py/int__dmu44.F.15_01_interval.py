"""
Problema INT__DMU44.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Generado con el protocolo F.15_01 del paper (delta ~ U[0, 0.15],
intervalo simetrico, semilla fija) sobre la instancia crisp dmu44 de
Demirkol, Mehta y Uzsoy (1998).
"""

from jobshop_rl.models.interval import Interval


INT__DMU44_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__dmu44.F.15_01_interval',
    'sequences': [
        [0, 5, 1, 3, 2, 6, 4, 7, 9, 11, 10, 14, 13, 8, 12],
        [2, 4, 3, 6, 1, 0, 5, 12, 14, 7, 10, 13, 9, 8, 11],
        [2, 5, 3, 6, 1, 4, 0, 13, 10, 8, 7, 14, 9, 12, 11],
        [6, 5, 0, 3, 1, 2, 4, 10, 7, 11, 14, 8, 12, 13, 9],
        [2, 3, 4, 6, 5, 0, 1, 8, 9, 11, 14, 13, 7, 10, 12],
        [1, 3, 4, 2, 6, 0, 5, 11, 13, 14, 8, 9, 10, 7, 12],
        [3, 0, 5, 1, 2, 4, 6, 10, 11, 8, 12, 13, 14, 7, 9],
        [5, 4, 6, 2, 0, 1, 3, 10, 13, 12, 11, 7, 14, 8, 9],
        [6, 2, 0, 3, 5, 1, 4, 11, 13, 10, 8, 9, 14, 12, 7],
        [3, 2, 4, 6, 0, 1, 5, 7, 10, 14, 8, 11, 12, 9, 13],
        [3, 1, 0, 6, 2, 5, 4, 13, 8, 9, 14, 12, 10, 7, 11],
        [1, 0, 6, 4, 5, 3, 2, 7, 10, 8, 9, 14, 12, 13, 11],
        [2, 3, 5, 6, 0, 4, 1, 10, 13, 9, 8, 14, 7, 11, 12],
        [0, 6, 5, 4, 3, 2, 1, 13, 12, 7, 9, 14, 10, 11, 8],
        [2, 5, 1, 4, 3, 6, 0, 11, 7, 10, 9, 14, 12, 8, 13],
        [0, 2, 1, 3, 6, 4, 5, 11, 10, 8, 12, 14, 13, 9, 7],
        [1, 2, 3, 5, 6, 4, 0, 8, 9, 12, 13, 7, 14, 10, 11],
        [6, 0, 5, 1, 2, 4, 3, 7, 9, 11, 12, 10, 14, 8, 13],
        [4, 5, 1, 0, 6, 3, 2, 9, 11, 10, 14, 12, 8, 7, 13],
        [6, 4, 1, 5, 2, 3, 0, 13, 7, 9, 14, 10, 12, 8, 11],
    ],
    'durations': [
        [Interval(128, 156), Interval(183, 213), Interval(121, 149), Interval(167, 173), Interval(11, 13), Interval(19, 23), Interval(115, 153), Interval(20, 22), Interval(32, 34), Interval(41, 53), Interval(127, 133), Interval(36, 48), Interval(90, 102), Interval(108, 134), Interval(158, 174)],
        [Interval(149, 157), Interval(38, 40), Interval(122, 136), Interval(134, 162), Interval(5, 5), Interval(127, 165), Interval(179, 203), Interval(154, 168), Interval(64, 84), Interval(148, 198), Interval(107, 119), Interval(126, 168), Interval(160, 184), Interval(130, 174), Interval(114, 136)],
        [Interval(63, 65), Interval(134, 140), Interval(90, 96), Interval(7, 9), Interval(166, 204), Interval(45, 57), Interval(103, 119), Interval(165, 219), Interval(151, 179), Interval(174, 190), Interval(77, 103), Interval(6, 6), Interval(99, 121), Interval(138, 182), Interval(16, 20)],
        [Interval(134, 172), Interval(192, 202), Interval(169, 213), Interval(103, 135), Interval(172, 210), Interval(23, 29), Interval(106, 136), Interval(125, 137), Interval(170, 188), Interval(39, 49), Interval(151, 175), Interval(79, 97), Interval(178, 192), Interval(35, 41), Interval(68, 86)],
        [Interval(100, 110), Interval(13, 17), Interval(109, 141), Interval(126, 138), Interval(114, 146), Interval(42, 52), Interval(146, 182), Interval(68, 72), Interval(44, 52), Interval(136, 182), Interval(95, 99), Interval(168, 176), Interval(188, 200), Interval(27, 35), Interval(74, 90)],
        [Interval(55, 69), Interval(114, 118), Interval(175, 189), Interval(80, 82), Interval(160, 192), Interval(77, 79), Interval(9, 11), Interval(23, 25), Interval(152, 162), Interval(57, 75), Interval(13, 13), Interval(135, 149), Interval(187, 191), Interval(118, 152), Interval(96, 100)],
        [Interval(28, 28), Interval(38, 50), Interval(173, 207), Interval(163, 197), Interval(125, 133), Interval(177, 185), Interval(29, 37), Interval(47, 55), Interval(52, 68), Interval(186, 200), Interval(68, 80), Interval(81, 95), Interval(101, 105), Interval(19, 25), Interval(91, 95)],
        [Interval(160, 194), Interval(44, 50), Interval(62, 82), Interval(33, 35), Interval(148, 156), Interval(131, 155), Interval(63, 63), Interval(143, 149), Interval(160, 206), Interval(2, 2), Interval(142, 190), Interval(126, 170), Interval(9, 11), Interval(152, 204), Interval(130, 168)],
        [Interval(150, 164), Interval(119, 159), Interval(48, 58), Interval(30, 38), Interval(40, 44), Interval(132, 168), Interval(107, 121), Interval(22, 24), Interval(160, 182), Interval(159, 195), Interval(138, 156), Interval(27, 27), Interval(107, 111), Interval(27, 35), Interval(70, 82)],
        [Interval(54, 72), Interval(178, 206), Interval(144, 188), Interval(35, 43), Interval(47, 53), Interval(43, 57), Interval(159, 199), Interval(103, 119), Interval(35, 35), Interval(127, 157), Interval(118, 154), Interval(55, 59), Interval(3, 3), Interval(12, 12), Interval(50, 60)],
        [Interval(156, 210), Interval(64, 72), Interval(36, 46), Interval(52, 60), Interval(157, 173), Interval(71, 77), Interval(50, 56), Interval(27, 35), Interval(70, 90), Interval(70, 84), Interval(153, 183), Interval(29, 37), Interval(92, 102), Interval(1, 1), Interval(106, 118)],
        [Interval(152, 162), Interval(188, 212), Interval(97, 129), Interval(99, 101), Interval(2, 2), Interval(154, 186), Interval(36, 46), Interval(134, 160), Interval(42, 54), Interval(56, 68), Interval(165, 171), Interval(33, 39), Interval(68, 86), Interval(74, 78), Interval(118, 124)],
        [Interval(121, 145), Interval(79, 91), Interval(84, 94), Interval(92, 104), Interval(54, 58), Interval(164, 196), Interval(13, 17), Interval(151, 181), Interval(139, 181), Interval(165, 181), Interval(194, 194), Interval(140, 164), Interval(135, 137), Interval(155, 179), Interval(171, 171)],
        [Interval(42, 56), Interval(58, 70), Interval(174, 174), Interval(20, 24), Interval(29, 35), Interval(150, 170), Interval(31, 39), Interval(188, 192), Interval(126, 148), Interval(154, 192), Interval(2, 2), Interval(123, 133), Interval(5, 5), Interval(46, 54), Interval(34, 44)],
        [Interval(112, 118), Interval(100, 112), Interval(17, 21), Interval(147, 155), Interval(65, 87), Interval(99, 105), Interval(177, 197), Interval(166, 192), Interval(176, 192), Interval(45, 53), Interval(63, 73), Interval(150, 176), Interval(127, 147), Interval(86, 102), Interval(48, 60)],
        [Interval(124, 130), Interval(164, 202), Interval(23, 29), Interval(10, 10), Interval(65, 81), Interval(55, 73), Interval(5, 5), Interval(42, 46), Interval(2, 2), Interval(43, 47), Interval(40, 52), Interval(180, 188), Interval(97, 97), Interval(198, 202), Interval(75, 97)],
        [Interval(79, 89), Interval(79, 95), Interval(157, 201), Interval(135, 149), Interval(12, 12), Interval(115, 137), Interval(150, 188), Interval(36, 42), Interval(155, 181), Interval(23, 25), Interval(135, 149), Interval(129, 137), Interval(131, 163), Interval(117, 125), Interval(178, 180)],
        [Interval(97, 99), Interval(67, 87), Interval(39, 43), Interval(97, 129), Interval(94, 100), Interval(126, 152), Interval(16, 18), Interval(167, 173), Interval(112, 120), Interval(57, 63), Interval(147, 183), Interval(155, 189), Interval(66, 88), Interval(47, 49), Interval(182, 210)],
        [Interval(31, 39), Interval(191, 199), Interval(3, 3), Interval(184, 198), Interval(51, 59), Interval(167, 211), Interval(5, 5), Interval(32, 34), Interval(115, 147), Interval(36, 42), Interval(145, 171), Interval(61, 77), Interval(99, 101), Interval(178, 220), Interval(162, 176)],
        [Interval(115, 147), Interval(134, 158), Interval(171, 179), Interval(22, 26), Interval(44, 56), Interval(133, 137), Interval(75, 81), Interval(64, 76), Interval(133, 171), Interval(93, 105), Interval(138, 166), Interval(63, 67), Interval(108, 140), Interval(82, 106), Interval(98, 102)],
    ],
    'name': 'int__dmu44.F.15_01_interval',
    'has_intervals': True,
    'description': 'DMU dmu44 ensanchada F.15_01',
}
