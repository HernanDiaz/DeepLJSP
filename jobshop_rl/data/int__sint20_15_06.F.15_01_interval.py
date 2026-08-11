"""
Problema INT__SINT20_15_06.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Generado con el protocolo F.15_01 del paper (delta ~ U[0, 0.15],
intervalo simetrico, semilla fija) sobre la instancia crisp sint20_15_06 de
Demirkol, Mehta y Uzsoy (1998).
"""

from jobshop_rl.models.interval import Interval


INT__SINT20_15_06_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__sint20_15_06.F.15_01_interval',
    'sequences': [
        [11, 5, 10, 14, 1, 0, 6, 12, 13, 8, 4, 9, 7, 2, 3],
        [4, 8, 14, 1, 10, 12, 13, 5, 2, 0, 11, 9, 6, 7, 3],
        [0, 4, 9, 1, 6, 13, 11, 12, 2, 14, 8, 7, 5, 3, 10],
        [1, 12, 2, 5, 0, 4, 6, 3, 7, 8, 9, 13, 14, 11, 10],
        [5, 10, 4, 2, 3, 14, 1, 12, 0, 6, 13, 11, 8, 7, 9],
        [4, 7, 13, 5, 9, 10, 8, 2, 14, 11, 12, 3, 6, 0, 1],
        [5, 9, 2, 10, 1, 3, 8, 13, 6, 12, 0, 11, 7, 4, 14],
        [7, 6, 10, 9, 0, 5, 12, 14, 13, 8, 4, 11, 2, 3, 1],
        [14, 4, 1, 8, 6, 9, 5, 3, 10, 13, 2, 12, 0, 11, 7],
        [8, 4, 11, 5, 0, 7, 3, 13, 6, 1, 14, 9, 2, 10, 12],
        [8, 11, 1, 0, 5, 14, 6, 12, 9, 13, 3, 7, 10, 2, 4],
        [13, 14, 11, 7, 3, 0, 10, 8, 6, 12, 9, 4, 5, 2, 1],
        [5, 14, 3, 7, 13, 10, 8, 0, 9, 6, 2, 1, 12, 11, 4],
        [7, 2, 1, 9, 6, 0, 11, 10, 5, 3, 13, 14, 8, 12, 4],
        [14, 12, 8, 1, 4, 13, 2, 0, 11, 3, 7, 9, 10, 5, 6],
        [8, 1, 6, 7, 2, 11, 10, 4, 9, 14, 12, 5, 0, 3, 13],
        [10, 4, 2, 13, 8, 7, 0, 11, 3, 1, 6, 12, 5, 14, 9],
        [2, 1, 13, 11, 3, 14, 4, 10, 7, 5, 9, 0, 12, 6, 8],
        [2, 11, 14, 0, 5, 4, 9, 3, 7, 8, 1, 12, 10, 13, 6],
        [10, 7, 1, 3, 6, 5, 0, 13, 11, 9, 2, 12, 8, 14, 4],
    ],
    'durations': [
        [Interval(86, 98), Interval(3, 3), Interval(5, 5), Interval(20, 22), Interval(7, 7), Interval(6, 8), Interval(27, 29), Interval(12, 14), Interval(38, 50), Interval(57, 77), Interval(63, 81), Interval(45, 57), Interval(55, 55), Interval(61, 67), Interval(39, 51)],
        [Interval(50, 54), Interval(76, 100), Interval(49, 59), Interval(48, 56), Interval(84, 94), Interval(61, 61), Interval(13, 17), Interval(29, 37), Interval(27, 33), Interval(73, 91), Interval(73, 73), Interval(42, 50), Interval(87, 99), Interval(65, 77), Interval(78, 80)],
        [Interval(62, 82), Interval(92, 102), Interval(28, 36), Interval(63, 85), Interval(77, 85), Interval(58, 78), Interval(55, 73), Interval(30, 32), Interval(37, 41), Interval(16, 18), Interval(4, 4), Interval(60, 66), Interval(43, 43), Interval(70, 80), Interval(88, 96)],
        [Interval(34, 38), Interval(45, 51), Interval(14, 14), Interval(4, 4), Interval(72, 84), Interval(6, 8), Interval(57, 63), Interval(48, 62), Interval(60, 78), Interval(41, 45), Interval(70, 78), Interval(25, 29), Interval(69, 71), Interval(33, 39), Interval(42, 42)],
        [Interval(45, 51), Interval(58, 68), Interval(50, 56), Interval(58, 58), Interval(37, 39), Interval(32, 42), Interval(27, 33), Interval(81, 107), Interval(61, 71), Interval(95, 103), Interval(60, 64), Interval(76, 94), Interval(25, 29), Interval(22, 26), Interval(89, 95)],
        [Interval(90, 102), Interval(83, 87), Interval(39, 41), Interval(40, 46), Interval(53, 63), Interval(65, 79), Interval(4, 4), Interval(53, 63), Interval(33, 41), Interval(22, 26), Interval(22, 22), Interval(61, 77), Interval(16, 16), Interval(31, 31), Interval(15, 15)],
        [Interval(53, 71), Interval(13, 15), Interval(19, 25), Interval(64, 84), Interval(62, 74), Interval(23, 31), Interval(44, 46), Interval(77, 79), Interval(4, 4), Interval(88, 106), Interval(25, 29), Interval(36, 38), Interval(11, 11), Interval(59, 65), Interval(30, 40)],
        [Interval(40, 42), Interval(40, 50), Interval(89, 105), Interval(80, 96), Interval(95, 101), Interval(57, 71), Interval(12, 14), Interval(62, 64), Interval(68, 92), Interval(24, 26), Interval(18, 22), Interval(4, 4), Interval(37, 45), Interval(65, 75), Interval(38, 42)],
        [Interval(69, 85), Interval(36, 44), Interval(77, 79), Interval(20, 20), Interval(75, 85), Interval(41, 51), Interval(59, 65), Interval(77, 99), Interval(16, 18), Interval(23, 29), Interval(53, 57), Interval(82, 90), Interval(84, 88), Interval(64, 70), Interval(23, 23)],
        [Interval(57, 59), Interval(14, 18), Interval(64, 72), Interval(42, 52), Interval(53, 71), Interval(24, 30), Interval(66, 74), Interval(52, 68), Interval(27, 29), Interval(53, 57), Interval(9, 11), Interval(56, 64), Interval(75, 79), Interval(34, 42), Interval(2, 2)],
        [Interval(25, 33), Interval(16, 18), Interval(12, 14), Interval(51, 53), Interval(91, 99), Interval(29, 37), Interval(31, 35), Interval(75, 89), Interval(2, 2), Interval(40, 48), Interval(3, 3), Interval(45, 59), Interval(33, 35), Interval(17, 19), Interval(31, 37)],
        [Interval(42, 46), Interval(53, 71), Interval(15, 17), Interval(43, 55), Interval(96, 98), Interval(40, 52), Interval(34, 42), Interval(78, 90), Interval(66, 74), Interval(1, 1), Interval(10, 10), Interval(60, 74), Interval(80, 82), Interval(12, 14), Interval(68, 72)],
        [Interval(32, 32), Interval(72, 82), Interval(55, 59), Interval(43, 45), Interval(12, 14), Interval(2, 2), Interval(51, 59), Interval(56, 68), Interval(68, 82), Interval(97, 99), Interval(15, 17), Interval(40, 50), Interval(37, 41), Interval(60, 66), Interval(61, 71)],
        [Interval(17, 17), Interval(78, 98), Interval(83, 101), Interval(35, 41), Interval(43, 51), Interval(56, 70), Interval(63, 83), Interval(14, 16), Interval(41, 45), Interval(35, 47), Interval(17, 21), Interval(15, 17), Interval(67, 71), Interval(55, 73), Interval(26, 28)],
        [Interval(68, 70), Interval(77, 89), Interval(17, 23), Interval(12, 14), Interval(46, 48), Interval(49, 61), Interval(66, 86), Interval(36, 44), Interval(22, 22), Interval(74, 86), Interval(9, 11), Interval(77, 77), Interval(39, 43), Interval(20, 22), Interval(87, 103)],
        [Interval(3, 3), Interval(21, 25), Interval(71, 73), Interval(75, 79), Interval(36, 46), Interval(30, 32), Interval(14, 14), Interval(25, 29), Interval(8, 8), Interval(83, 109), Interval(11, 13), Interval(32, 42), Interval(41, 45), Interval(88, 92), Interval(10, 12)],
        [Interval(68, 92), Interval(57, 59), Interval(49, 59), Interval(76, 90), Interval(11, 13), Interval(27, 31), Interval(88, 96), Interval(85, 87), Interval(70, 76), Interval(72, 88), Interval(17, 17), Interval(56, 60), Interval(1, 1), Interval(38, 42), Interval(91, 95)],
        [Interval(58, 72), Interval(69, 81), Interval(38, 44), Interval(33, 39), Interval(14, 18), Interval(85, 113), Interval(19, 23), Interval(13, 15), Interval(55, 71), Interval(79, 91), Interval(9, 11), Interval(46, 48), Interval(73, 79), Interval(29, 33), Interval(34, 46)],
        [Interval(6, 6), Interval(14, 14), Interval(51, 61), Interval(28, 36), Interval(12, 12), Interval(34, 34), Interval(85, 99), Interval(8, 10), Interval(20, 20), Interval(41, 53), Interval(81, 87), Interval(2, 2), Interval(97, 99), Interval(55, 67), Interval(11, 11)],
        [Interval(75, 95), Interval(25, 33), Interval(36, 36), Interval(28, 36), Interval(65, 79), Interval(55, 59), Interval(69, 87), Interval(56, 66), Interval(16, 18), Interval(70, 78), Interval(42, 52), Interval(76, 86), Interval(66, 78), Interval(73, 87), Interval(70, 80)],
    ],
    'name': 'int__sint20_15_06.F.15_01_interval',
    'has_intervals': True,
    'description': 'DMU sint20_15_06 ensanchada F.15_01',
}
