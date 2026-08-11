"""
Problema INT__SINT20_15_05.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Generado con el protocolo F.15_01 del paper (delta ~ U[0, 0.15],
intervalo simetrico, semilla fija) sobre la instancia crisp sint20_15_05 de
Demirkol, Mehta y Uzsoy (1998).
"""

from jobshop_rl.models.interval import Interval


INT__SINT20_15_05_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__sint20_15_05.F.15_01_interval',
    'sequences': [
        [9, 13, 4, 0, 1, 8, 10, 5, 7, 2, 14, 6, 11, 12, 3],
        [10, 2, 3, 4, 14, 8, 5, 6, 0, 13, 9, 7, 12, 11, 1],
        [2, 6, 7, 13, 1, 4, 5, 11, 3, 8, 10, 9, 14, 0, 12],
        [14, 3, 2, 10, 8, 7, 1, 4, 13, 0, 11, 9, 5, 12, 6],
        [11, 0, 12, 3, 1, 8, 2, 9, 13, 7, 14, 5, 10, 4, 6],
        [1, 13, 4, 5, 7, 10, 11, 12, 0, 6, 2, 3, 8, 9, 14],
        [9, 10, 11, 1, 13, 3, 6, 4, 8, 5, 2, 7, 12, 0, 14],
        [10, 12, 0, 1, 11, 2, 5, 6, 13, 9, 8, 7, 3, 14, 4],
        [5, 9, 4, 6, 14, 1, 2, 7, 13, 3, 12, 0, 8, 11, 10],
        [11, 1, 4, 2, 14, 12, 7, 8, 3, 13, 5, 9, 0, 6, 10],
        [1, 13, 5, 11, 9, 2, 3, 10, 14, 12, 7, 4, 0, 6, 8],
        [11, 5, 1, 9, 6, 0, 10, 7, 14, 8, 13, 12, 2, 3, 4],
        [14, 4, 12, 3, 0, 8, 5, 9, 13, 1, 10, 6, 11, 7, 2],
        [14, 8, 0, 12, 13, 4, 9, 7, 5, 10, 1, 3, 2, 11, 6],
        [4, 0, 11, 10, 5, 3, 9, 8, 12, 6, 14, 13, 1, 2, 7],
        [13, 14, 4, 12, 5, 3, 0, 2, 7, 6, 1, 10, 8, 9, 11],
        [10, 8, 1, 4, 6, 12, 11, 2, 13, 7, 14, 5, 0, 3, 9],
        [12, 9, 6, 0, 4, 3, 5, 11, 2, 14, 8, 13, 1, 10, 7],
        [5, 7, 9, 12, 6, 13, 4, 2, 3, 8, 11, 10, 14, 0, 1],
        [11, 13, 1, 14, 6, 7, 9, 0, 3, 8, 5, 12, 4, 2, 10],
    ],
    'durations': [
        [Interval(25, 33), Interval(44, 46), Interval(67, 87), Interval(56, 66), Interval(80, 94), Interval(39, 47), Interval(38, 44), Interval(37, 49), Interval(16, 16), Interval(88, 90), Interval(75, 93), Interval(1, 1), Interval(53, 65), Interval(80, 88), Interval(10, 12)],
        [Interval(80, 106), Interval(44, 46), Interval(74, 78), Interval(88, 98), Interval(15, 15), Interval(4, 4), Interval(72, 84), Interval(32, 34), Interval(87, 107), Interval(64, 70), Interval(96, 98), Interval(57, 67), Interval(35, 45), Interval(28, 34), Interval(37, 37)],
        [Interval(35, 41), Interval(32, 40), Interval(71, 87), Interval(77, 95), Interval(29, 33), Interval(19, 21), Interval(83, 109), Interval(51, 59), Interval(41, 45), Interval(6, 6), Interval(94, 102), Interval(48, 50), Interval(84, 100), Interval(49, 55), Interval(42, 46)],
        [Interval(76, 80), Interval(35, 45), Interval(30, 32), Interval(62, 82), Interval(58, 64), Interval(1, 1), Interval(55, 67), Interval(40, 42), Interval(15, 17), Interval(62, 76), Interval(44, 58), Interval(12, 16), Interval(17, 23), Interval(7, 7), Interval(35, 37)],
        [Interval(46, 54), Interval(65, 67), Interval(44, 44), Interval(71, 91), Interval(68, 74), Interval(16, 16), Interval(59, 75), Interval(75, 97), Interval(59, 75), Interval(65, 73), Interval(88, 106), Interval(10, 12), Interval(51, 59), Interval(85, 103), Interval(28, 36)],
        [Interval(64, 80), Interval(75, 95), Interval(28, 30), Interval(81, 87), Interval(28, 36), Interval(44, 58), Interval(4, 4), Interval(47, 61), Interval(82, 108), Interval(35, 37), Interval(74, 88), Interval(16, 18), Interval(52, 70), Interval(32, 36), Interval(74, 76)],
        [Interval(32, 40), Interval(72, 86), Interval(34, 44), Interval(47, 47), Interval(85, 113), Interval(81, 85), Interval(41, 43), Interval(48, 58), Interval(7, 7), Interval(44, 48), Interval(34, 42), Interval(43, 45), Interval(50, 62), Interval(76, 100), Interval(10, 12)],
        [Interval(59, 65), Interval(43, 57), Interval(70, 72), Interval(24, 32), Interval(31, 37), Interval(56, 72), Interval(83, 97), Interval(38, 48), Interval(19, 21), Interval(8, 10), Interval(50, 54), Interval(11, 13), Interval(29, 37), Interval(54, 66), Interval(30, 38)],
        [Interval(81, 95), Interval(17, 17), Interval(81, 99), Interval(56, 72), Interval(11, 11), Interval(70, 80), Interval(12, 12), Interval(44, 56), Interval(78, 82), Interval(63, 81), Interval(12, 14), Interval(21, 27), Interval(31, 31), Interval(36, 38), Interval(89, 109)],
        [Interval(38, 44), Interval(94, 94), Interval(67, 87), Interval(41, 43), Interval(15, 19), Interval(31, 37), Interval(15, 19), Interval(70, 76), Interval(68, 80), Interval(80, 94), Interval(91, 95), Interval(71, 83), Interval(17, 21), Interval(83, 93), Interval(25, 27)],
        [Interval(40, 52), Interval(57, 57), Interval(21, 25), Interval(71, 79), Interval(12, 14), Interval(26, 30), Interval(34, 36), Interval(77, 79), Interval(45, 57), Interval(19, 25), Interval(80, 86), Interval(73, 77), Interval(36, 46), Interval(1, 1), Interval(21, 27)],
        [Interval(55, 63), Interval(39, 41), Interval(2, 2), Interval(45, 53), Interval(28, 30), Interval(11, 13), Interval(82, 88), Interval(64, 80), Interval(3, 3), Interval(66, 70), Interval(73, 91), Interval(17, 19), Interval(39, 47), Interval(63, 81), Interval(56, 64)],
        [Interval(18, 20), Interval(81, 107), Interval(56, 66), Interval(92, 94), Interval(69, 75), Interval(17, 21), Interval(29, 29), Interval(43, 57), Interval(45, 47), Interval(21, 21), Interval(60, 62), Interval(64, 82), Interval(25, 33), Interval(73, 87), Interval(79, 99)],
        [Interval(32, 38), Interval(85, 105), Interval(82, 86), Interval(53, 69), Interval(7, 7), Interval(22, 28), Interval(90, 100), Interval(85, 109), Interval(89, 101), Interval(10, 10), Interval(27, 35), Interval(77, 93), Interval(17, 21), Interval(14, 14), Interval(68, 74)],
        [Interval(7, 9), Interval(52, 64), Interval(45, 57), Interval(60, 72), Interval(51, 55), Interval(57, 65), Interval(8, 10), Interval(16, 16), Interval(53, 67), Interval(85, 95), Interval(51, 55), Interval(18, 20), Interval(44, 44), Interval(73, 83), Interval(30, 36)],
        [Interval(2, 2), Interval(37, 49), Interval(6, 8), Interval(34, 42), Interval(85, 97), Interval(70, 78), Interval(29, 31), Interval(71, 83), Interval(34, 36), Interval(74, 78), Interval(39, 41), Interval(4, 4), Interval(30, 40), Interval(75, 83), Interval(14, 16)],
        [Interval(89, 105), Interval(17, 19), Interval(46, 56), Interval(31, 35), Interval(89, 107), Interval(9, 9), Interval(29, 35), Interval(9, 11), Interval(37, 39), Interval(7, 9), Interval(48, 54), Interval(85, 109), Interval(9, 9), Interval(63, 69), Interval(78, 104)],
        [Interval(73, 79), Interval(63, 81), Interval(64, 76), Interval(28, 32), Interval(39, 43), Interval(11, 11), Interval(43, 57), Interval(41, 47), Interval(60, 76), Interval(85, 113), Interval(50, 64), Interval(22, 28), Interval(16, 18), Interval(64, 76), Interval(9, 11)],
        [Interval(14, 18), Interval(17, 19), Interval(17, 21), Interval(48, 52), Interval(41, 45), Interval(30, 36), Interval(18, 24), Interval(25, 25), Interval(49, 53), Interval(39, 49), Interval(33, 35), Interval(22, 22), Interval(54, 64), Interval(63, 71), Interval(5, 5)],
        [Interval(70, 74), Interval(52, 68), Interval(43, 45), Interval(21, 23), Interval(18, 24), Interval(6, 8), Interval(52, 58), Interval(21, 21), Interval(9, 9), Interval(50, 66), Interval(30, 34), Interval(84, 100), Interval(73, 83), Interval(29, 37), Interval(18, 20)],
    ],
    'name': 'int__sint20_15_05.F.15_01_interval',
    'has_intervals': True,
    'description': 'DMU sint20_15_05 ensanchada F.15_01',
}
