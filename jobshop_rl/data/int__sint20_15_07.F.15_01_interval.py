"""
Problema INT__SINT20_15_07.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Generado con el protocolo F.15_01 del paper (delta ~ U[0, 0.15],
intervalo simetrico, semilla fija) sobre la instancia crisp sint20_15_07 de
Demirkol, Mehta y Uzsoy (1998).
"""

from jobshop_rl.models.interval import Interval


INT__SINT20_15_07_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__sint20_15_07.F.15_01_interval',
    'sequences': [
        [4, 2, 13, 1, 8, 6, 5, 12, 3, 9, 10, 11, 7, 0, 14],
        [10, 11, 6, 8, 4, 2, 1, 5, 13, 14, 3, 7, 0, 9, 12],
        [4, 11, 0, 5, 10, 2, 3, 13, 7, 8, 6, 12, 1, 9, 14],
        [14, 12, 6, 7, 11, 10, 1, 2, 9, 8, 0, 4, 3, 13, 5],
        [0, 3, 4, 7, 9, 12, 10, 1, 2, 13, 14, 11, 6, 5, 8],
        [2, 10, 7, 13, 0, 11, 8, 5, 6, 9, 14, 4, 12, 1, 3],
        [14, 4, 9, 5, 3, 0, 7, 10, 12, 11, 13, 1, 2, 8, 6],
        [9, 6, 4, 7, 10, 0, 2, 12, 5, 3, 1, 13, 14, 8, 11],
        [6, 8, 3, 7, 9, 2, 1, 11, 10, 12, 13, 14, 5, 4, 0],
        [7, 13, 11, 5, 8, 14, 10, 4, 12, 6, 2, 3, 1, 9, 0],
        [4, 3, 9, 1, 5, 14, 8, 10, 12, 11, 6, 2, 0, 13, 7],
        [2, 11, 1, 13, 8, 14, 7, 0, 6, 10, 3, 12, 4, 5, 9],
        [2, 10, 0, 5, 4, 11, 3, 14, 1, 9, 8, 7, 6, 12, 13],
        [13, 11, 2, 8, 9, 4, 1, 6, 5, 10, 14, 3, 0, 12, 7],
        [4, 9, 14, 11, 7, 6, 0, 5, 3, 10, 12, 1, 13, 2, 8],
        [6, 2, 4, 14, 3, 11, 9, 13, 8, 5, 0, 10, 12, 1, 7],
        [8, 13, 12, 5, 14, 9, 4, 1, 7, 0, 6, 10, 11, 2, 3],
        [0, 14, 12, 13, 11, 8, 2, 1, 10, 5, 3, 7, 4, 6, 9],
        [1, 5, 12, 6, 11, 13, 7, 3, 2, 10, 0, 14, 4, 9, 8],
        [5, 0, 6, 9, 1, 8, 7, 13, 12, 11, 10, 3, 4, 14, 2],
    ],
    'durations': [
        [Interval(63, 65), Interval(18, 24), Interval(85, 101), Interval(43, 49), Interval(89, 101), Interval(56, 64), Interval(9, 11), Interval(26, 32), Interval(87, 103), Interval(26, 32), Interval(52, 60), Interval(78, 86), Interval(43, 45), Interval(14, 18), Interval(30, 34)],
        [Interval(72, 76), Interval(33, 33), Interval(29, 35), Interval(46, 60), Interval(93, 95), Interval(60, 74), Interval(41, 49), Interval(67, 83), Interval(46, 52), Interval(92, 100), Interval(38, 48), Interval(37, 41), Interval(78, 92), Interval(77, 89), Interval(49, 63)],
        [Interval(59, 63), Interval(10, 10), Interval(78, 94), Interval(65, 67), Interval(70, 72), Interval(3, 3), Interval(75, 81), Interval(37, 41), Interval(5, 5), Interval(73, 85), Interval(40, 44), Interval(49, 59), Interval(66, 82), Interval(2, 2), Interval(58, 64)],
        [Interval(20, 26), Interval(60, 68), Interval(55, 61), Interval(48, 64), Interval(43, 45), Interval(65, 69), Interval(51, 63), Interval(59, 67), Interval(68, 82), Interval(10, 12), Interval(54, 68), Interval(55, 57), Interval(21, 25), Interval(94, 98), Interval(52, 56)],
        [Interval(57, 61), Interval(44, 54), Interval(48, 54), Interval(61, 67), Interval(83, 97), Interval(33, 43), Interval(45, 45), Interval(35, 41), Interval(9, 9), Interval(6, 8), Interval(9, 11), Interval(63, 73), Interval(34, 44), Interval(54, 66), Interval(7, 7)],
        [Interval(36, 44), Interval(49, 57), Interval(66, 68), Interval(21, 25), Interval(5, 5), Interval(41, 51), Interval(45, 53), Interval(78, 104), Interval(92, 106), Interval(71, 73), Interval(14, 16), Interval(54, 70), Interval(54, 58), Interval(76, 88), Interval(45, 49)],
        [Interval(44, 48), Interval(84, 96), Interval(9, 9), Interval(40, 52), Interval(76, 92), Interval(36, 38), Interval(37, 47), Interval(32, 40), Interval(80, 96), Interval(34, 38), Interval(11, 13), Interval(63, 67), Interval(12, 14), Interval(29, 35), Interval(64, 74)],
        [Interval(69, 85), Interval(78, 88), Interval(3, 3), Interval(22, 28), Interval(14, 16), Interval(42, 46), Interval(38, 46), Interval(2, 2), Interval(86, 96), Interval(75, 79), Interval(9, 11), Interval(89, 105), Interval(83, 105), Interval(6, 6), Interval(80, 82)],
        [Interval(78, 98), Interval(64, 76), Interval(63, 83), Interval(2, 2), Interval(45, 57), Interval(79, 87), Interval(6, 6), Interval(93, 95), Interval(73, 95), Interval(4, 4), Interval(24, 30), Interval(63, 77), Interval(79, 87), Interval(3, 3), Interval(6, 8)],
        [Interval(3, 3), Interval(81, 107), Interval(46, 52), Interval(2, 2), Interval(74, 96), Interval(15, 19), Interval(29, 37), Interval(46, 52), Interval(58, 60), Interval(19, 19), Interval(73, 87), Interval(43, 53), Interval(44, 54), Interval(24, 28), Interval(26, 28)],
        [Interval(18, 24), Interval(88, 94), Interval(49, 49), Interval(67, 83), Interval(89, 101), Interval(84, 96), Interval(66, 72), Interval(35, 41), Interval(7, 7), Interval(49, 49), Interval(6, 6), Interval(48, 58), Interval(28, 30), Interval(66, 78), Interval(23, 27)],
        [Interval(68, 88), Interval(15, 17), Interval(58, 66), Interval(76, 84), Interval(27, 27), Interval(44, 56), Interval(4, 4), Interval(65, 79), Interval(84, 86), Interval(81, 89), Interval(44, 52), Interval(75, 85), Interval(46, 58), Interval(49, 53), Interval(8, 8)],
        [Interval(46, 48), Interval(7, 7), Interval(25, 29), Interval(70, 82), Interval(36, 42), Interval(51, 55), Interval(6, 6), Interval(68, 84), Interval(18, 22), Interval(82, 90), Interval(11, 13), Interval(3, 3), Interval(8, 10), Interval(58, 72), Interval(20, 26)],
        [Interval(45, 51), Interval(83, 109), Interval(66, 72), Interval(1, 1), Interval(69, 71), Interval(91, 93), Interval(55, 67), Interval(23, 29), Interval(43, 51), Interval(27, 27), Interval(91, 103), Interval(90, 94), Interval(35, 39), Interval(86, 94), Interval(69, 75)],
        [Interval(39, 51), Interval(39, 41), Interval(51, 51), Interval(38, 46), Interval(59, 75), Interval(93, 93), Interval(15, 17), Interval(21, 25), Interval(50, 66), Interval(30, 30), Interval(34, 36), Interval(70, 80), Interval(40, 40), Interval(62, 76), Interval(43, 55)],
        [Interval(1, 1), Interval(21, 25), Interval(9, 11), Interval(1, 1), Interval(10, 12), Interval(33, 35), Interval(21, 27), Interval(7, 7), Interval(17, 21), Interval(54, 62), Interval(68, 72), Interval(57, 59), Interval(13, 17), Interval(83, 89), Interval(64, 86)],
        [Interval(48, 62), Interval(64, 78), Interval(17, 23), Interval(43, 49), Interval(57, 77), Interval(13, 13), Interval(48, 64), Interval(64, 76), Interval(33, 37), Interval(54, 62), Interval(46, 52), Interval(80, 82), Interval(37, 39), Interval(30, 34), Interval(61, 67)],
        [Interval(49, 63), Interval(47, 49), Interval(42, 56), Interval(6, 6), Interval(59, 73), Interval(83, 111), Interval(30, 32), Interval(66, 86), Interval(27, 33), Interval(87, 89), Interval(55, 59), Interval(15, 17), Interval(31, 37), Interval(74, 94), Interval(24, 32)],
        [Interval(27, 35), Interval(33, 41), Interval(23, 29), Interval(33, 43), Interval(83, 109), Interval(61, 67), Interval(67, 79), Interval(79, 85), Interval(42, 46), Interval(47, 59), Interval(88, 110), Interval(46, 46), Interval(41, 51), Interval(40, 52), Interval(43, 51)],
        [Interval(63, 71), Interval(7, 7), Interval(15, 17), Interval(49, 55), Interval(72, 74), Interval(19, 21), Interval(10, 10), Interval(2, 2), Interval(14, 18), Interval(85, 113), Interval(60, 74), Interval(95, 97), Interval(20, 20), Interval(42, 56), Interval(40, 52)],
    ],
    'name': 'int__sint20_15_07.F.15_01_interval',
    'has_intervals': True,
    'description': 'DMU sint20_15_07 ensanchada F.15_01',
}
