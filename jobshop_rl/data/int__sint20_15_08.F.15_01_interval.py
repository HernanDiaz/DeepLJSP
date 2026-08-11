"""
Problema INT__SINT20_15_08.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Generado con el protocolo F.15_01 del paper (delta ~ U[0, 0.15],
intervalo simetrico, semilla fija) sobre la instancia crisp sint20_15_08 de
Demirkol, Mehta y Uzsoy (1998).
"""

from jobshop_rl.models.interval import Interval


INT__SINT20_15_08_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__sint20_15_08.F.15_01_interval',
    'sequences': [
        [8, 6, 5, 7, 12, 2, 3, 10, 14, 4, 0, 9, 13, 1, 11],
        [1, 8, 3, 10, 11, 6, 5, 7, 14, 0, 13, 4, 2, 9, 12],
        [7, 6, 14, 12, 5, 4, 11, 0, 3, 2, 9, 10, 8, 13, 1],
        [2, 13, 14, 8, 10, 9, 7, 1, 0, 3, 5, 6, 11, 12, 4],
        [11, 10, 6, 2, 13, 12, 0, 14, 1, 7, 5, 4, 3, 8, 9],
        [1, 7, 14, 0, 13, 5, 9, 4, 8, 10, 11, 12, 3, 2, 6],
        [4, 8, 5, 12, 11, 9, 6, 0, 7, 3, 2, 14, 1, 13, 10],
        [4, 12, 5, 10, 13, 11, 1, 9, 6, 8, 3, 14, 7, 2, 0],
        [2, 0, 12, 10, 9, 8, 3, 4, 13, 7, 1, 14, 11, 6, 5],
        [13, 5, 2, 6, 3, 14, 10, 12, 4, 7, 11, 8, 0, 9, 1],
        [5, 10, 13, 9, 11, 1, 0, 14, 12, 8, 3, 2, 4, 6, 7],
        [3, 13, 14, 2, 5, 10, 8, 1, 4, 6, 11, 0, 9, 12, 7],
        [5, 9, 12, 7, 11, 0, 1, 6, 3, 13, 2, 4, 8, 14, 10],
        [12, 1, 14, 2, 5, 9, 0, 3, 6, 7, 10, 13, 4, 8, 11],
        [2, 3, 0, 5, 8, 12, 11, 6, 14, 10, 4, 13, 7, 1, 9],
        [11, 12, 2, 1, 7, 6, 5, 14, 8, 0, 13, 9, 4, 3, 10],
        [2, 3, 0, 10, 5, 13, 6, 4, 11, 8, 7, 14, 1, 12, 9],
        [0, 8, 2, 13, 10, 4, 5, 11, 9, 7, 3, 12, 1, 14, 6],
        [5, 13, 9, 0, 3, 14, 1, 7, 2, 8, 6, 12, 10, 4, 11],
        [2, 10, 13, 1, 9, 8, 6, 14, 3, 11, 4, 0, 7, 5, 12],
    ],
    'durations': [
        [Interval(56, 58), Interval(79, 81), Interval(88, 90), Interval(68, 92), Interval(56, 64), Interval(12, 16), Interval(48, 62), Interval(44, 48), Interval(24, 32), Interval(68, 90), Interval(88, 88), Interval(55, 67), Interval(33, 33), Interval(18, 20), Interval(41, 45)],
        [Interval(29, 37), Interval(6, 8), Interval(6, 6), Interval(52, 62), Interval(44, 48), Interval(58, 78), Interval(2, 2), Interval(50, 60), Interval(32, 42), Interval(77, 81), Interval(61, 77), Interval(6, 8), Interval(35, 43), Interval(46, 46), Interval(51, 63)],
        [Interval(86, 94), Interval(46, 46), Interval(8, 10), Interval(38, 48), Interval(70, 82), Interval(22, 26), Interval(18, 22), Interval(81, 85), Interval(60, 74), Interval(47, 49), Interval(31, 35), Interval(71, 73), Interval(28, 32), Interval(94, 98), Interval(72, 86)],
        [Interval(75, 101), Interval(46, 56), Interval(76, 86), Interval(51, 53), Interval(11, 13), Interval(37, 47), Interval(54, 72), Interval(23, 23), Interval(23, 25), Interval(30, 36), Interval(21, 23), Interval(97, 99), Interval(70, 86), Interval(55, 61), Interval(81, 109)],
        [Interval(24, 26), Interval(6, 6), Interval(75, 95), Interval(77, 89), Interval(14, 14), Interval(80, 86), Interval(46, 62), Interval(23, 27), Interval(44, 46), Interval(20, 24), Interval(42, 54), Interval(3, 3), Interval(72, 76), Interval(6, 6), Interval(5, 5)],
        [Interval(38, 44), Interval(49, 49), Interval(1, 1), Interval(20, 24), Interval(63, 65), Interval(33, 35), Interval(85, 105), Interval(43, 49), Interval(63, 73), Interval(5, 5), Interval(76, 86), Interval(85, 89), Interval(29, 31), Interval(83, 91), Interval(64, 86)],
        [Interval(74, 90), Interval(47, 49), Interval(9, 11), Interval(25, 31), Interval(93, 99), Interval(56, 60), Interval(14, 18), Interval(4, 4), Interval(31, 37), Interval(54, 66), Interval(5, 5), Interval(43, 55), Interval(86, 106), Interval(28, 32), Interval(16, 16)],
        [Interval(67, 73), Interval(76, 86), Interval(28, 30), Interval(75, 77), Interval(60, 60), Interval(29, 37), Interval(44, 56), Interval(25, 31), Interval(85, 105), Interval(28, 32), Interval(6, 6), Interval(98, 98), Interval(69, 69), Interval(84, 112), Interval(36, 48)],
        [Interval(51, 65), Interval(82, 90), Interval(56, 62), Interval(41, 49), Interval(21, 27), Interval(18, 24), Interval(87, 89), Interval(24, 26), Interval(76, 80), Interval(29, 37), Interval(78, 98), Interval(44, 54), Interval(40, 54), Interval(29, 37), Interval(79, 101)],
        [Interval(24, 24), Interval(4, 4), Interval(90, 92), Interval(17, 19), Interval(12, 16), Interval(65, 73), Interval(27, 33), Interval(74, 88), Interval(72, 74), Interval(69, 83), Interval(93, 95), Interval(91, 103), Interval(9, 11), Interval(67, 67), Interval(83, 99)],
        [Interval(15, 17), Interval(65, 87), Interval(2, 2), Interval(24, 30), Interval(60, 80), Interval(76, 102), Interval(34, 44), Interval(73, 97), Interval(90, 96), Interval(48, 50), Interval(43, 45), Interval(57, 77), Interval(33, 39), Interval(62, 76), Interval(86, 104)],
        [Interval(1, 1), Interval(12, 12), Interval(75, 99), Interval(10, 10), Interval(46, 60), Interval(25, 33), Interval(12, 14), Interval(14, 14), Interval(49, 65), Interval(12, 14), Interval(48, 52), Interval(70, 84), Interval(80, 100), Interval(30, 38), Interval(14, 16)],
        [Interval(54, 58), Interval(20, 24), Interval(8, 10), Interval(84, 88), Interval(30, 34), Interval(76, 78), Interval(90, 92), Interval(89, 97), Interval(11, 13), Interval(54, 54), Interval(25, 29), Interval(49, 57), Interval(69, 89), Interval(62, 78), Interval(36, 46)],
        [Interval(58, 66), Interval(7, 9), Interval(46, 54), Interval(78, 94), Interval(54, 54), Interval(37, 43), Interval(80, 90), Interval(2, 2), Interval(93, 97), Interval(90, 96), Interval(12, 14), Interval(69, 71), Interval(20, 22), Interval(65, 71), Interval(74, 84)],
        [Interval(73, 75), Interval(60, 62), Interval(1, 1), Interval(48, 56), Interval(83, 97), Interval(8, 10), Interval(8, 10), Interval(24, 28), Interval(37, 47), Interval(64, 72), Interval(58, 64), Interval(86, 106), Interval(57, 75), Interval(29, 35), Interval(81, 105)],
        [Interval(95, 103), Interval(42, 46), Interval(90, 108), Interval(37, 39), Interval(15, 17), Interval(52, 68), Interval(26, 30), Interval(23, 29), Interval(87, 91), Interval(41, 49), Interval(76, 76), Interval(2, 2), Interval(34, 44), Interval(91, 105), Interval(30, 36)],
        [Interval(7, 7), Interval(29, 33), Interval(83, 93), Interval(24, 24), Interval(87, 97), Interval(46, 56), Interval(34, 40), Interval(1, 1), Interval(20, 24), Interval(47, 59), Interval(8, 8), Interval(10, 10), Interval(13, 15), Interval(58, 58), Interval(89, 105)],
        [Interval(69, 77), Interval(2, 2), Interval(37, 39), Interval(26, 32), Interval(6, 6), Interval(58, 66), Interval(65, 83), Interval(37, 47), Interval(43, 47), Interval(81, 87), Interval(52, 58), Interval(7, 9), Interval(79, 93), Interval(63, 77), Interval(85, 101)],
        [Interval(38, 44), Interval(14, 16), Interval(74, 86), Interval(64, 66), Interval(90, 98), Interval(6, 6), Interval(97, 99), Interval(64, 64), Interval(16, 18), Interval(12, 14), Interval(46, 48), Interval(96, 98), Interval(12, 12), Interval(57, 75), Interval(16, 18)],
        [Interval(12, 12), Interval(27, 31), Interval(29, 29), Interval(26, 28), Interval(78, 84), Interval(29, 35), Interval(76, 84), Interval(14, 16), Interval(22, 24), Interval(58, 76), Interval(39, 49), Interval(53, 65), Interval(76, 82), Interval(49, 57), Interval(68, 74)],
    ],
    'name': 'int__sint20_15_08.F.15_01_interval',
    'has_intervals': True,
    'description': 'DMU sint20_15_08 ensanchada F.15_01',
}
