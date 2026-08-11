"""
Problema INT__SINT20_15_09.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Generado con el protocolo F.15_01 del paper (delta ~ U[0, 0.15],
intervalo simetrico, semilla fija) sobre la instancia crisp sint20_15_09 de
Demirkol, Mehta y Uzsoy (1998).
"""

from jobshop_rl.models.interval import Interval


INT__SINT20_15_09_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__sint20_15_09.F.15_01_interval',
    'sequences': [
        [9, 6, 4, 1, 11, 12, 2, 8, 7, 14, 10, 3, 0, 13, 5],
        [14, 5, 3, 1, 2, 4, 12, 13, 9, 8, 11, 0, 7, 6, 10],
        [8, 0, 6, 3, 5, 13, 1, 14, 2, 11, 7, 9, 4, 12, 10],
        [13, 2, 11, 3, 10, 0, 6, 14, 8, 4, 9, 7, 12, 1, 5],
        [11, 2, 4, 9, 10, 6, 8, 12, 1, 3, 5, 13, 0, 14, 7],
        [12, 8, 4, 6, 3, 2, 9, 5, 0, 7, 1, 10, 14, 11, 13],
        [1, 6, 3, 9, 5, 10, 7, 13, 14, 2, 4, 0, 12, 8, 11],
        [5, 14, 10, 2, 0, 13, 1, 7, 8, 9, 12, 6, 11, 3, 4],
        [13, 1, 0, 8, 12, 10, 2, 6, 9, 11, 5, 14, 7, 4, 3],
        [12, 4, 11, 6, 2, 10, 0, 5, 13, 9, 14, 3, 8, 1, 7],
        [5, 3, 13, 6, 0, 2, 10, 1, 4, 11, 14, 7, 8, 9, 12],
        [14, 9, 0, 7, 4, 3, 5, 1, 6, 13, 8, 2, 12, 11, 10],
        [12, 6, 9, 8, 11, 14, 0, 10, 2, 13, 3, 5, 7, 1, 4],
        [12, 14, 7, 9, 6, 10, 3, 4, 1, 8, 2, 0, 11, 5, 13],
        [5, 4, 12, 11, 1, 10, 9, 7, 2, 8, 6, 3, 0, 14, 13],
        [4, 1, 11, 8, 9, 7, 14, 0, 6, 12, 10, 5, 2, 13, 3],
        [12, 0, 9, 10, 5, 7, 3, 1, 6, 14, 11, 13, 2, 4, 8],
        [10, 1, 3, 2, 7, 14, 13, 11, 4, 12, 5, 8, 9, 0, 6],
        [5, 4, 0, 7, 2, 8, 1, 13, 12, 3, 6, 11, 10, 9, 14],
        [10, 4, 1, 13, 7, 8, 5, 2, 11, 6, 14, 3, 0, 9, 12],
    ],
    'durations': [
        [Interval(39, 49), Interval(80, 88), Interval(89, 97), Interval(69, 83), Interval(46, 58), Interval(11, 11), Interval(10, 12), Interval(59, 75), Interval(68, 70), Interval(56, 72), Interval(44, 52), Interval(18, 22), Interval(12, 14), Interval(50, 58), Interval(63, 77)],
        [Interval(60, 64), Interval(3, 3), Interval(72, 76), Interval(33, 37), Interval(15, 19), Interval(80, 92), Interval(62, 64), Interval(55, 63), Interval(48, 52), Interval(31, 35), Interval(56, 70), Interval(46, 50), Interval(19, 23), Interval(61, 69), Interval(29, 29)],
        [Interval(54, 56), Interval(27, 29), Interval(57, 61), Interval(18, 20), Interval(38, 42), Interval(30, 36), Interval(92, 98), Interval(13, 17), Interval(67, 71), Interval(76, 86), Interval(81, 93), Interval(64, 80), Interval(97, 99), Interval(66, 84), Interval(33, 35)],
        [Interval(74, 100), Interval(5, 5), Interval(77, 101), Interval(23, 25), Interval(89, 95), Interval(78, 102), Interval(49, 61), Interval(78, 104), Interval(26, 28), Interval(66, 72), Interval(4, 4), Interval(23, 27), Interval(17, 17), Interval(36, 36), Interval(75, 83)],
        [Interval(34, 38), Interval(40, 44), Interval(16, 20), Interval(41, 49), Interval(10, 10), Interval(68, 86), Interval(79, 81), Interval(83, 87), Interval(45, 51), Interval(59, 69), Interval(54, 68), Interval(82, 88), Interval(50, 66), Interval(13, 15), Interval(21, 27)],
        [Interval(18, 24), Interval(55, 71), Interval(90, 90), Interval(88, 94), Interval(60, 68), Interval(51, 55), Interval(24, 26), Interval(26, 30), Interval(56, 60), Interval(40, 52), Interval(40, 40), Interval(20, 24), Interval(47, 57), Interval(30, 40), Interval(68, 70)],
        [Interval(2, 2), Interval(50, 64), Interval(65, 73), Interval(40, 44), Interval(35, 45), Interval(55, 59), Interval(52, 62), Interval(48, 64), Interval(38, 46), Interval(49, 53), Interval(14, 18), Interval(29, 33), Interval(44, 58), Interval(62, 64), Interval(39, 41)],
        [Interval(67, 73), Interval(57, 61), Interval(20, 26), Interval(65, 83), Interval(59, 79), Interval(73, 89), Interval(81, 89), Interval(69, 81), Interval(88, 96), Interval(58, 68), Interval(63, 71), Interval(44, 48), Interval(95, 101), Interval(30, 38), Interval(82, 86)],
        [Interval(15, 15), Interval(97, 97), Interval(8, 8), Interval(17, 19), Interval(39, 41), Interval(11, 13), Interval(69, 83), Interval(37, 45), Interval(80, 82), Interval(34, 36), Interval(12, 16), Interval(19, 23), Interval(3, 3), Interval(46, 60), Interval(22, 24)],
        [Interval(17, 17), Interval(54, 64), Interval(60, 70), Interval(52, 70), Interval(63, 75), Interval(64, 86), Interval(55, 55), Interval(66, 84), Interval(14, 16), Interval(81, 91), Interval(33, 33), Interval(3, 3), Interval(25, 25), Interval(42, 48), Interval(9, 11)],
        [Interval(12, 16), Interval(51, 69), Interval(83, 85), Interval(4, 4), Interval(41, 49), Interval(84, 92), Interval(70, 78), Interval(75, 75), Interval(93, 95), Interval(40, 54), Interval(61, 71), Interval(57, 59), Interval(71, 79), Interval(52, 56), Interval(64, 70)],
        [Interval(77, 101), Interval(44, 48), Interval(92, 98), Interval(77, 103), Interval(60, 64), Interval(27, 27), Interval(50, 66), Interval(22, 22), Interval(56, 60), Interval(51, 61), Interval(26, 26), Interval(40, 46), Interval(27, 29), Interval(88, 102), Interval(72, 80)],
        [Interval(17, 19), Interval(46, 58), Interval(37, 45), Interval(12, 14), Interval(71, 81), Interval(18, 24), Interval(55, 71), Interval(63, 65), Interval(20, 22), Interval(57, 69), Interval(60, 80), Interval(78, 96), Interval(24, 28), Interval(47, 51), Interval(70, 74)],
        [Interval(26, 28), Interval(26, 28), Interval(43, 55), Interval(39, 51), Interval(74, 84), Interval(70, 76), Interval(19, 21), Interval(51, 63), Interval(24, 26), Interval(72, 92), Interval(91, 99), Interval(35, 41), Interval(35, 45), Interval(17, 21), Interval(35, 41)],
        [Interval(45, 55), Interval(67, 71), Interval(4, 4), Interval(53, 67), Interval(77, 91), Interval(47, 63), Interval(73, 79), Interval(2, 2), Interval(69, 87), Interval(29, 31), Interval(63, 71), Interval(86, 94), Interval(16, 18), Interval(36, 36), Interval(43, 49)],
        [Interval(28, 34), Interval(61, 67), Interval(2, 2), Interval(24, 30), Interval(19, 25), Interval(38, 44), Interval(23, 29), Interval(4, 4), Interval(3, 3), Interval(1, 1), Interval(19, 21), Interval(53, 55), Interval(8, 8), Interval(71, 79), Interval(80, 88)],
        [Interval(25, 27), Interval(85, 97), Interval(96, 96), Interval(48, 54), Interval(69, 81), Interval(86, 112), Interval(17, 21), Interval(4, 4), Interval(74, 88), Interval(72, 78), Interval(52, 64), Interval(11, 11), Interval(12, 14), Interval(26, 30), Interval(22, 24)],
        [Interval(11, 13), Interval(21, 21), Interval(78, 102), Interval(43, 51), Interval(13, 13), Interval(5, 5), Interval(65, 77), Interval(42, 52), Interval(51, 59), Interval(2, 2), Interval(42, 56), Interval(23, 29), Interval(30, 34), Interval(26, 28), Interval(25, 33)],
        [Interval(67, 83), Interval(84, 86), Interval(32, 36), Interval(62, 78), Interval(18, 24), Interval(25, 29), Interval(50, 56), Interval(83, 109), Interval(50, 54), Interval(62, 70), Interval(95, 103), Interval(32, 38), Interval(8, 10), Interval(38, 50), Interval(16, 16)],
        [Interval(64, 72), Interval(85, 113), Interval(11, 13), Interval(25, 31), Interval(70, 82), Interval(16, 20), Interval(10, 12), Interval(37, 37), Interval(52, 58), Interval(61, 69), Interval(91, 101), Interval(27, 35), Interval(58, 74), Interval(11, 13), Interval(80, 108)],
    ],
    'name': 'int__sint20_15_09.F.15_01_interval',
    'has_intervals': True,
    'description': 'DMU sint20_15_09 ensanchada F.15_01',
}
