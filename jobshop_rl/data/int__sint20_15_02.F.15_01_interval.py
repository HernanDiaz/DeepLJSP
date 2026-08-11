"""
Problema INT__SINT20_15_02.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Generado con el protocolo F.15_01 del paper (delta ~ U[0, 0.15],
intervalo simetrico, semilla fija) sobre la instancia crisp sint20_15_02 de
Demirkol, Mehta y Uzsoy (1998).
"""

from jobshop_rl.models.interval import Interval


INT__SINT20_15_02_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__sint20_15_02.F.15_01_interval',
    'sequences': [
        [12, 4, 3, 0, 14, 7, 11, 13, 6, 8, 2, 1, 9, 10, 5],
        [7, 11, 9, 1, 6, 3, 12, 14, 2, 10, 8, 5, 13, 4, 0],
        [12, 5, 6, 3, 11, 4, 1, 10, 13, 14, 2, 9, 8, 7, 0],
        [11, 2, 8, 9, 14, 5, 12, 6, 13, 4, 10, 0, 7, 3, 1],
        [3, 9, 11, 0, 7, 6, 14, 2, 12, 13, 10, 4, 1, 8, 5],
        [11, 7, 6, 5, 9, 8, 0, 1, 12, 13, 2, 3, 14, 10, 4],
        [11, 12, 14, 6, 8, 0, 3, 7, 2, 4, 13, 10, 9, 5, 1],
        [13, 12, 5, 8, 7, 0, 10, 6, 1, 3, 11, 14, 4, 2, 9],
        [5, 2, 4, 7, 11, 12, 8, 0, 9, 13, 10, 3, 14, 6, 1],
        [4, 5, 14, 0, 2, 1, 6, 11, 8, 7, 9, 13, 3, 12, 10],
        [10, 7, 11, 8, 12, 0, 14, 4, 6, 9, 2, 13, 1, 5, 3],
        [6, 0, 4, 10, 7, 2, 8, 3, 14, 13, 11, 5, 12, 1, 9],
        [14, 5, 13, 3, 8, 4, 1, 7, 2, 0, 11, 12, 10, 6, 9],
        [13, 14, 12, 8, 11, 0, 6, 2, 10, 3, 4, 7, 5, 9, 1],
        [2, 9, 7, 0, 4, 3, 5, 1, 8, 12, 6, 14, 10, 13, 11],
        [6, 2, 13, 9, 10, 3, 5, 1, 0, 14, 4, 7, 12, 11, 8],
        [13, 1, 8, 11, 4, 0, 3, 5, 10, 14, 9, 2, 7, 6, 12],
        [2, 3, 6, 0, 14, 11, 7, 9, 1, 8, 5, 10, 13, 12, 4],
        [0, 6, 8, 3, 7, 10, 14, 11, 5, 1, 2, 9, 13, 4, 12],
        [1, 10, 12, 5, 8, 14, 9, 6, 4, 11, 13, 2, 0, 3, 7],
    ],
    'durations': [
        [Interval(12, 16), Interval(76, 88), Interval(36, 48), Interval(94, 100), Interval(63, 77), Interval(79, 99), Interval(37, 39), Interval(13, 17), Interval(41, 49), Interval(49, 65), Interval(54, 64), Interval(51, 67), Interval(9, 9), Interval(38, 50), Interval(88, 106)],
        [Interval(44, 44), Interval(39, 49), Interval(59, 61), Interval(29, 31), Interval(66, 86), Interval(40, 42), Interval(95, 99), Interval(75, 91), Interval(31, 33), Interval(22, 26), Interval(90, 96), Interval(14, 16), Interval(20, 22), Interval(55, 65), Interval(75, 79)],
        [Interval(59, 67), Interval(63, 73), Interval(84, 92), Interval(63, 83), Interval(63, 69), Interval(50, 52), Interval(86, 104), Interval(26, 28), Interval(69, 89), Interval(23, 27), Interval(1, 1), Interval(86, 88), Interval(74, 96), Interval(3, 3), Interval(49, 59)],
        [Interval(2, 2), Interval(52, 58), Interval(44, 52), Interval(73, 77), Interval(52, 64), Interval(43, 49), Interval(67, 89), Interval(43, 53), Interval(13, 13), Interval(53, 65), Interval(32, 34), Interval(6, 6), Interval(18, 20), Interval(81, 107), Interval(53, 57)],
        [Interval(31, 39), Interval(13, 17), Interval(67, 87), Interval(4, 4), Interval(54, 62), Interval(64, 82), Interval(1, 1), Interval(19, 19), Interval(54, 54), Interval(90, 108), Interval(20, 26), Interval(83, 101), Interval(7, 9), Interval(37, 41), Interval(5, 5)],
        [Interval(92, 106), Interval(71, 95), Interval(31, 39), Interval(52, 70), Interval(45, 49), Interval(86, 92), Interval(55, 55), Interval(51, 67), Interval(18, 22), Interval(61, 63), Interval(82, 104), Interval(58, 72), Interval(10, 12), Interval(11, 13), Interval(57, 75)],
        [Interval(46, 50), Interval(90, 108), Interval(55, 69), Interval(52, 68), Interval(8, 8), Interval(38, 44), Interval(60, 64), Interval(58, 66), Interval(2, 2), Interval(40, 42), Interval(73, 77), Interval(89, 105), Interval(68, 74), Interval(24, 32), Interval(31, 39)],
        [Interval(21, 25), Interval(75, 77), Interval(11, 11), Interval(83, 93), Interval(85, 85), Interval(36, 46), Interval(4, 4), Interval(79, 87), Interval(73, 83), Interval(84, 108), Interval(29, 31), Interval(40, 52), Interval(67, 89), Interval(52, 54), Interval(12, 14)],
        [Interval(13, 17), Interval(24, 30), Interval(16, 18), Interval(60, 74), Interval(43, 51), Interval(66, 80), Interval(74, 84), Interval(33, 37), Interval(8, 8), Interval(3, 3), Interval(30, 32), Interval(55, 55), Interval(9, 9), Interval(37, 41), Interval(83, 109)],
        [Interval(71, 85), Interval(12, 14), Interval(72, 86), Interval(32, 32), Interval(14, 16), Interval(19, 21), Interval(73, 89), Interval(86, 112), Interval(28, 36), Interval(38, 50), Interval(16, 16), Interval(52, 62), Interval(54, 66), Interval(50, 62), Interval(56, 68)],
        [Interval(42, 48), Interval(45, 49), Interval(89, 95), Interval(21, 27), Interval(32, 32), Interval(60, 78), Interval(28, 32), Interval(70, 94), Interval(26, 34), Interval(85, 107), Interval(18, 18), Interval(35, 37), Interval(85, 109), Interval(73, 93), Interval(81, 101)],
        [Interval(6, 6), Interval(51, 51), Interval(62, 80), Interval(69, 83), Interval(44, 46), Interval(8, 10), Interval(77, 97), Interval(11, 13), Interval(67, 73), Interval(47, 51), Interval(20, 20), Interval(79, 105), Interval(11, 13), Interval(60, 62), Interval(8, 10)],
        [Interval(41, 49), Interval(74, 98), Interval(15, 15), Interval(88, 90), Interval(37, 49), Interval(1, 1), Interval(56, 62), Interval(55, 63), Interval(15, 17), Interval(39, 49), Interval(51, 63), Interval(49, 53), Interval(62, 64), Interval(53, 69), Interval(59, 63)],
        [Interval(54, 60), Interval(22, 26), Interval(15, 15), Interval(10, 12), Interval(66, 78), Interval(84, 110), Interval(85, 113), Interval(19, 23), Interval(4, 4), Interval(43, 57), Interval(19, 25), Interval(48, 64), Interval(37, 45), Interval(51, 67), Interval(70, 90)],
        [Interval(34, 40), Interval(78, 90), Interval(7, 9), Interval(55, 57), Interval(27, 33), Interval(47, 61), Interval(82, 102), Interval(24, 26), Interval(56, 66), Interval(87, 109), Interval(17, 19), Interval(9, 9), Interval(27, 29), Interval(51, 57), Interval(57, 71)],
        [Interval(87, 95), Interval(15, 19), Interval(65, 71), Interval(49, 51), Interval(55, 63), Interval(49, 59), Interval(68, 90), Interval(79, 87), Interval(9, 9), Interval(1, 1), Interval(52, 60), Interval(10, 12), Interval(79, 97), Interval(59, 73), Interval(16, 16)],
        [Interval(62, 78), Interval(13, 17), Interval(12, 16), Interval(50, 58), Interval(89, 99), Interval(45, 57), Interval(81, 91), Interval(8, 10), Interval(46, 48), Interval(6, 8), Interval(12, 16), Interval(53, 53), Interval(7, 9), Interval(89, 105), Interval(24, 28)],
        [Interval(57, 77), Interval(89, 103), Interval(47, 51), Interval(94, 102), Interval(15, 19), Interval(68, 88), Interval(44, 52), Interval(64, 82), Interval(8, 10), Interval(22, 24), Interval(4, 4), Interval(37, 41), Interval(77, 83), Interval(24, 24), Interval(62, 74)],
        [Interval(69, 77), Interval(13, 13), Interval(47, 63), Interval(14, 14), Interval(73, 85), Interval(87, 107), Interval(14, 16), Interval(77, 91), Interval(14, 14), Interval(13, 17), Interval(32, 38), Interval(66, 76), Interval(4, 4), Interval(61, 65), Interval(57, 75)],
        [Interval(93, 105), Interval(43, 45), Interval(77, 81), Interval(80, 100), Interval(27, 35), Interval(42, 46), Interval(94, 102), Interval(6, 8), Interval(40, 42), Interval(3, 3), Interval(50, 66), Interval(32, 34), Interval(96, 98), Interval(79, 95), Interval(85, 85)],
    ],
    'name': 'int__sint20_15_02.F.15_01_interval',
    'has_intervals': True,
    'description': 'DMU sint20_15_02 ensanchada F.15_01',
}
