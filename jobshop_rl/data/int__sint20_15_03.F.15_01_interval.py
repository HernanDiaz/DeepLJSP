"""
Problema INT__SINT20_15_03.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Generado con el protocolo F.15_01 del paper (delta ~ U[0, 0.15],
intervalo simetrico, semilla fija) sobre la instancia crisp sint20_15_03 de
Demirkol, Mehta y Uzsoy (1998).
"""

from jobshop_rl.models.interval import Interval


INT__SINT20_15_03_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__sint20_15_03.F.15_01_interval',
    'sequences': [
        [5, 4, 1, 9, 12, 14, 0, 3, 2, 8, 6, 10, 13, 7, 11],
        [14, 8, 5, 13, 9, 3, 6, 2, 1, 12, 0, 11, 4, 7, 10],
        [0, 14, 13, 5, 11, 2, 12, 3, 8, 7, 1, 9, 10, 4, 6],
        [3, 2, 4, 0, 6, 11, 5, 10, 9, 14, 1, 13, 12, 8, 7],
        [4, 14, 8, 3, 11, 13, 10, 12, 7, 1, 5, 6, 9, 0, 2],
        [6, 7, 5, 3, 11, 10, 4, 1, 0, 9, 12, 8, 14, 13, 2],
        [14, 4, 1, 8, 2, 13, 6, 3, 0, 11, 10, 7, 12, 5, 9],
        [6, 13, 7, 10, 9, 2, 3, 14, 4, 8, 1, 12, 0, 5, 11],
        [6, 9, 10, 4, 0, 14, 7, 13, 8, 3, 2, 11, 12, 1, 5],
        [12, 10, 7, 4, 8, 14, 1, 3, 9, 2, 0, 5, 11, 6, 13],
        [12, 8, 7, 4, 1, 9, 6, 2, 14, 5, 13, 0, 11, 10, 3],
        [13, 3, 12, 4, 5, 9, 10, 8, 7, 14, 11, 6, 2, 1, 0],
        [1, 9, 13, 14, 2, 6, 0, 4, 12, 11, 7, 10, 3, 8, 5],
        [7, 9, 8, 6, 11, 14, 3, 1, 4, 12, 10, 5, 2, 13, 0],
        [12, 6, 7, 3, 5, 14, 4, 11, 0, 13, 2, 1, 10, 8, 9],
        [5, 3, 4, 10, 9, 14, 0, 8, 12, 13, 7, 1, 11, 2, 6],
        [3, 8, 12, 2, 10, 11, 6, 7, 13, 1, 9, 5, 14, 0, 4],
        [9, 11, 12, 0, 10, 6, 2, 8, 3, 14, 5, 13, 1, 7, 4],
        [14, 5, 9, 6, 7, 1, 3, 11, 4, 13, 10, 8, 12, 0, 2],
        [2, 10, 7, 8, 6, 13, 5, 1, 0, 11, 3, 9, 4, 14, 12],
    ],
    'durations': [
        [Interval(66, 76), Interval(51, 67), Interval(31, 31), Interval(54, 68), Interval(79, 83), Interval(42, 44), Interval(12, 14), Interval(10, 12), Interval(13, 15), Interval(49, 57), Interval(21, 23), Interval(67, 71), Interval(82, 90), Interval(2, 2), Interval(20, 24)],
        [Interval(52, 68), Interval(18, 18), Interval(56, 64), Interval(61, 65), Interval(88, 100), Interval(16, 20), Interval(61, 63), Interval(82, 104), Interval(16, 18), Interval(68, 90), Interval(1, 1), Interval(83, 85), Interval(63, 75), Interval(18, 18), Interval(55, 63)],
        [Interval(17, 21), Interval(43, 55), Interval(33, 41), Interval(49, 51), Interval(7, 7), Interval(50, 56), Interval(9, 9), Interval(73, 89), Interval(73, 85), Interval(39, 43), Interval(24, 26), Interval(20, 22), Interval(55, 57), Interval(23, 29), Interval(79, 89)],
        [Interval(58, 74), Interval(89, 97), Interval(27, 29), Interval(70, 76), Interval(4, 4), Interval(78, 90), Interval(71, 73), Interval(26, 30), Interval(9, 9), Interval(29, 31), Interval(52, 58), Interval(50, 54), Interval(42, 48), Interval(71, 81), Interval(15, 19)],
        [Interval(43, 57), Interval(88, 98), Interval(78, 84), Interval(74, 86), Interval(64, 70), Interval(48, 54), Interval(83, 103), Interval(85, 93), Interval(41, 45), Interval(50, 56), Interval(6, 6), Interval(53, 67), Interval(36, 48), Interval(37, 45), Interval(53, 67)],
        [Interval(13, 17), Interval(2, 2), Interval(51, 53), Interval(82, 106), Interval(19, 23), Interval(34, 44), Interval(86, 102), Interval(16, 18), Interval(4, 4), Interval(74, 94), Interval(81, 99), Interval(40, 50), Interval(64, 64), Interval(24, 24), Interval(33, 37)],
        [Interval(62, 62), Interval(12, 14), Interval(85, 109), Interval(45, 53), Interval(31, 33), Interval(63, 65), Interval(60, 60), Interval(4, 4), Interval(30, 30), Interval(70, 80), Interval(74, 76), Interval(35, 43), Interval(31, 41), Interval(12, 14), Interval(22, 24)],
        [Interval(39, 47), Interval(56, 70), Interval(82, 86), Interval(12, 14), Interval(93, 95), Interval(89, 99), Interval(42, 48), Interval(77, 77), Interval(43, 49), Interval(15, 15), Interval(73, 97), Interval(85, 91), Interval(46, 58), Interval(49, 51), Interval(75, 81)],
        [Interval(68, 82), Interval(2, 2), Interval(68, 78), Interval(2, 2), Interval(89, 99), Interval(30, 40), Interval(38, 50), Interval(76, 78), Interval(60, 64), Interval(55, 63), Interval(44, 58), Interval(61, 77), Interval(34, 46), Interval(25, 31), Interval(21, 21)],
        [Interval(27, 33), Interval(59, 63), Interval(2, 2), Interval(2, 2), Interval(32, 32), Interval(38, 48), Interval(39, 51), Interval(24, 32), Interval(35, 45), Interval(86, 102), Interval(66, 74), Interval(2, 2), Interval(33, 43), Interval(16, 20), Interval(98, 100)],
        [Interval(44, 46), Interval(31, 37), Interval(28, 36), Interval(13, 17), Interval(36, 40), Interval(55, 69), Interval(8, 8), Interval(29, 35), Interval(38, 48), Interval(81, 99), Interval(45, 51), Interval(4, 4), Interval(15, 19), Interval(15, 19), Interval(44, 50)],
        [Interval(28, 34), Interval(10, 12), Interval(72, 74), Interval(6, 6), Interval(64, 86), Interval(36, 38), Interval(37, 39), Interval(58, 76), Interval(93, 101), Interval(27, 31), Interval(62, 72), Interval(39, 47), Interval(41, 55), Interval(26, 34), Interval(61, 61)],
        [Interval(71, 71), Interval(30, 32), Interval(47, 59), Interval(82, 104), Interval(20, 26), Interval(6, 6), Interval(70, 80), Interval(49, 65), Interval(53, 67), Interval(23, 25), Interval(58, 66), Interval(10, 12), Interval(61, 75), Interval(80, 86), Interval(28, 34)],
        [Interval(50, 58), Interval(49, 63), Interval(71, 77), Interval(60, 62), Interval(76, 100), Interval(11, 13), Interval(6, 8), Interval(20, 22), Interval(74, 96), Interval(36, 40), Interval(9, 11), Interval(59, 75), Interval(29, 37), Interval(79, 87), Interval(62, 82)],
        [Interval(44, 56), Interval(2, 2), Interval(68, 84), Interval(5, 5), Interval(74, 76), Interval(61, 73), Interval(43, 47), Interval(86, 100), Interval(19, 21), Interval(9, 9), Interval(61, 75), Interval(88, 108), Interval(17, 21), Interval(83, 111), Interval(67, 71)],
        [Interval(71, 73), Interval(94, 96), Interval(21, 21), Interval(42, 48), Interval(86, 88), Interval(45, 45), Interval(40, 54), Interval(82, 84), Interval(39, 39), Interval(49, 57), Interval(84, 90), Interval(49, 49), Interval(14, 16), Interval(29, 37), Interval(49, 61)],
        [Interval(20, 26), Interval(48, 60), Interval(1, 1), Interval(67, 83), Interval(25, 27), Interval(6, 6), Interval(29, 35), Interval(73, 89), Interval(78, 82), Interval(73, 85), Interval(22, 26), Interval(72, 90), Interval(90, 100), Interval(8, 10), Interval(74, 98)],
        [Interval(49, 61), Interval(28, 36), Interval(96, 100), Interval(89, 101), Interval(84, 112), Interval(13, 17), Interval(72, 78), Interval(86, 106), Interval(27, 35), Interval(6, 6), Interval(54, 58), Interval(32, 38), Interval(40, 48), Interval(61, 81), Interval(44, 52)],
        [Interval(1, 1), Interval(72, 74), Interval(55, 67), Interval(49, 61), Interval(21, 25), Interval(17, 17), Interval(77, 93), Interval(25, 29), Interval(41, 55), Interval(46, 50), Interval(7, 9), Interval(23, 29), Interval(81, 83), Interval(31, 37), Interval(40, 54)],
        [Interval(9, 9), Interval(21, 23), Interval(80, 96), Interval(13, 15), Interval(9, 9), Interval(65, 75), Interval(97, 97), Interval(58, 78), Interval(40, 42), Interval(20, 26), Interval(75, 97), Interval(37, 37), Interval(53, 57), Interval(3, 3), Interval(14, 16)],
    ],
    'name': 'int__sint20_15_03.F.15_01_interval',
    'has_intervals': True,
    'description': 'DMU sint20_15_03 ensanchada F.15_01',
}
