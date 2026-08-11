"""
Problema INT__SINT20_15_04.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Generado con el protocolo F.15_01 del paper (delta ~ U[0, 0.15],
intervalo simetrico, semilla fija) sobre la instancia crisp sint20_15_04 de
Demirkol, Mehta y Uzsoy (1998).
"""

from jobshop_rl.models.interval import Interval


INT__SINT20_15_04_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__sint20_15_04.F.15_01_interval',
    'sequences': [
        [9, 4, 12, 7, 11, 8, 6, 13, 0, 5, 10, 2, 1, 3, 14],
        [13, 6, 10, 5, 1, 2, 12, 0, 14, 4, 7, 11, 9, 8, 3],
        [13, 8, 5, 3, 1, 7, 4, 12, 2, 10, 0, 11, 14, 9, 6],
        [9, 14, 3, 1, 6, 11, 7, 2, 12, 0, 10, 5, 13, 8, 4],
        [14, 9, 12, 4, 1, 10, 7, 0, 5, 6, 13, 3, 8, 11, 2],
        [13, 5, 14, 9, 7, 1, 11, 0, 12, 3, 4, 6, 10, 8, 2],
        [3, 2, 4, 6, 14, 5, 1, 7, 13, 0, 10, 11, 9, 12, 8],
        [8, 14, 13, 0, 10, 7, 2, 3, 6, 11, 12, 4, 5, 1, 9],
        [5, 10, 9, 6, 14, 1, 3, 0, 2, 4, 8, 12, 13, 7, 11],
        [7, 9, 6, 8, 0, 4, 13, 11, 3, 14, 2, 12, 5, 10, 1],
        [6, 0, 9, 2, 8, 13, 1, 10, 4, 12, 11, 14, 7, 3, 5],
        [7, 1, 11, 0, 12, 14, 9, 13, 4, 6, 3, 8, 10, 5, 2],
        [13, 3, 10, 14, 5, 9, 0, 1, 2, 12, 7, 6, 8, 11, 4],
        [8, 12, 2, 7, 6, 3, 9, 11, 13, 5, 0, 10, 14, 4, 1],
        [4, 14, 3, 11, 13, 7, 2, 9, 1, 8, 5, 10, 0, 6, 12],
        [13, 9, 1, 7, 14, 10, 2, 12, 6, 11, 0, 5, 3, 4, 8],
        [0, 2, 5, 13, 1, 11, 3, 10, 12, 6, 4, 14, 8, 7, 9],
        [9, 12, 8, 2, 3, 13, 10, 14, 6, 7, 0, 4, 1, 11, 5],
        [8, 11, 3, 13, 2, 1, 0, 10, 9, 12, 6, 5, 4, 7, 14],
        [9, 1, 0, 14, 2, 10, 3, 7, 11, 13, 8, 5, 4, 6, 12],
    ],
    'durations': [
        [Interval(81, 85), Interval(33, 35), Interval(91, 93), Interval(73, 79), Interval(40, 44), Interval(5, 5), Interval(21, 23), Interval(66, 86), Interval(78, 86), Interval(46, 52), Interval(53, 63), Interval(63, 85), Interval(8, 10), Interval(56, 72), Interval(22, 28)],
        [Interval(29, 37), Interval(61, 61), Interval(49, 53), Interval(25, 31), Interval(89, 99), Interval(4, 4), Interval(9, 9), Interval(80, 80), Interval(5, 5), Interval(31, 35), Interval(95, 101), Interval(78, 98), Interval(72, 80), Interval(81, 99), Interval(51, 53)],
        [Interval(66, 84), Interval(39, 41), Interval(42, 52), Interval(36, 42), Interval(27, 31), Interval(89, 91), Interval(53, 57), Interval(4, 4), Interval(71, 85), Interval(73, 85), Interval(6, 8), Interval(16, 20), Interval(69, 81), Interval(62, 76), Interval(80, 104)],
        [Interval(22, 28), Interval(50, 50), Interval(21, 23), Interval(35, 37), Interval(54, 60), Interval(29, 29), Interval(9, 9), Interval(80, 90), Interval(24, 28), Interval(70, 82), Interval(2, 2), Interval(23, 25), Interval(40, 50), Interval(64, 82), Interval(40, 52)],
        [Interval(85, 111), Interval(12, 14), Interval(28, 28), Interval(68, 78), Interval(83, 101), Interval(56, 66), Interval(13, 15), Interval(56, 70), Interval(46, 54), Interval(72, 90), Interval(18, 20), Interval(45, 45), Interval(42, 48), Interval(11, 13), Interval(15, 15)],
        [Interval(37, 45), Interval(64, 74), Interval(73, 97), Interval(88, 110), Interval(87, 107), Interval(64, 72), Interval(31, 37), Interval(71, 93), Interval(62, 74), Interval(13, 17), Interval(65, 81), Interval(17, 21), Interval(39, 41), Interval(58, 68), Interval(55, 61)],
        [Interval(10, 12), Interval(25, 33), Interval(49, 55), Interval(27, 35), Interval(36, 46), Interval(78, 90), Interval(42, 52), Interval(5, 5), Interval(63, 63), Interval(86, 112), Interval(65, 83), Interval(28, 28), Interval(19, 21), Interval(18, 22), Interval(81, 99)],
        [Interval(10, 10), Interval(33, 43), Interval(87, 99), Interval(43, 49), Interval(3, 3), Interval(52, 66), Interval(18, 24), Interval(22, 26), Interval(45, 59), Interval(4, 4), Interval(44, 50), Interval(29, 37), Interval(11, 13), Interval(31, 31), Interval(50, 62)],
        [Interval(46, 48), Interval(80, 90), Interval(70, 90), Interval(47, 55), Interval(23, 29), Interval(66, 68), Interval(50, 56), Interval(16, 16), Interval(84, 106), Interval(75, 89), Interval(53, 71), Interval(59, 67), Interval(44, 54), Interval(40, 50), Interval(3, 3)],
        [Interval(22, 26), Interval(18, 22), Interval(26, 34), Interval(74, 96), Interval(50, 58), Interval(35, 45), Interval(60, 72), Interval(39, 45), Interval(26, 30), Interval(41, 51), Interval(31, 39), Interval(86, 100), Interval(34, 36), Interval(73, 81), Interval(71, 91)],
        [Interval(6, 8), Interval(62, 74), Interval(65, 69), Interval(50, 62), Interval(72, 96), Interval(54, 56), Interval(81, 103), Interval(62, 76), Interval(3, 3), Interval(23, 27), Interval(92, 94), Interval(58, 68), Interval(87, 93), Interval(4, 4), Interval(24, 24)],
        [Interval(9, 11), Interval(67, 69), Interval(26, 30), Interval(46, 60), Interval(34, 36), Interval(2, 2), Interval(30, 38), Interval(74, 94), Interval(52, 70), Interval(49, 57), Interval(50, 52), Interval(20, 24), Interval(76, 94), Interval(6, 8), Interval(34, 40)],
        [Interval(61, 63), Interval(66, 72), Interval(17, 21), Interval(69, 89), Interval(39, 45), Interval(51, 55), Interval(25, 29), Interval(65, 69), Interval(33, 43), Interval(36, 40), Interval(61, 75), Interval(73, 77), Interval(72, 94), Interval(21, 25), Interval(91, 107)],
        [Interval(79, 93), Interval(41, 47), Interval(32, 42), Interval(82, 98), Interval(45, 49), Interval(13, 17), Interval(64, 70), Interval(63, 77), Interval(42, 46), Interval(35, 37), Interval(31, 39), Interval(87, 97), Interval(56, 58), Interval(60, 72), Interval(17, 19)],
        [Interval(32, 34), Interval(36, 46), Interval(49, 59), Interval(54, 62), Interval(57, 73), Interval(89, 107), Interval(1, 1), Interval(57, 57), Interval(17, 21), Interval(8, 8), Interval(35, 45), Interval(34, 36), Interval(47, 63), Interval(28, 36), Interval(49, 51)],
        [Interval(14, 14), Interval(42, 52), Interval(2, 2), Interval(7, 9), Interval(85, 109), Interval(18, 20), Interval(51, 67), Interval(4, 4), Interval(52, 56), Interval(41, 49), Interval(53, 67), Interval(31, 41), Interval(39, 41), Interval(43, 47), Interval(35, 47)],
        [Interval(71, 95), Interval(39, 45), Interval(4, 4), Interval(16, 18), Interval(82, 94), Interval(93, 99), Interval(64, 68), Interval(51, 59), Interval(34, 42), Interval(32, 38), Interval(21, 23), Interval(68, 72), Interval(57, 59), Interval(6, 6), Interval(84, 86)],
        [Interval(56, 74), Interval(13, 13), Interval(93, 95), Interval(77, 87), Interval(21, 25), Interval(42, 54), Interval(55, 57), Interval(78, 102), Interval(26, 28), Interval(28, 34), Interval(45, 47), Interval(81, 91), Interval(87, 99), Interval(61, 65), Interval(53, 69)],
        [Interval(25, 27), Interval(92, 102), Interval(38, 50), Interval(27, 29), Interval(8, 10), Interval(26, 26), Interval(86, 90), Interval(81, 85), Interval(91, 99), Interval(88, 104), Interval(33, 37), Interval(78, 80), Interval(44, 56), Interval(87, 93), Interval(22, 26)],
        [Interval(75, 95), Interval(28, 36), Interval(26, 32), Interval(6, 6), Interval(52, 62), Interval(40, 52), Interval(11, 13), Interval(11, 11), Interval(4, 4), Interval(37, 41), Interval(75, 91), Interval(38, 42), Interval(51, 55), Interval(26, 32), Interval(62, 70)],
    ],
    'name': 'int__sint20_15_04.F.15_01_interval',
    'has_intervals': True,
    'description': 'DMU sint20_15_04 ensanchada F.15_01',
}
