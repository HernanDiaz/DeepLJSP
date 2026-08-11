"""
Problema INT__SINT20_15_10.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Generado con el protocolo F.15_01 del paper (delta ~ U[0, 0.15],
intervalo simetrico, semilla fija) sobre la instancia crisp sint20_15_10 de
Demirkol, Mehta y Uzsoy (1998).
"""

from jobshop_rl.models.interval import Interval


INT__SINT20_15_10_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__sint20_15_10.F.15_01_interval',
    'sequences': [
        [0, 3, 5, 8, 10, 14, 13, 6, 9, 4, 7, 12, 11, 2, 1],
        [14, 9, 12, 13, 7, 3, 8, 10, 2, 5, 6, 11, 0, 4, 1],
        [1, 10, 0, 2, 13, 4, 11, 3, 12, 9, 14, 8, 5, 7, 6],
        [12, 9, 7, 14, 6, 13, 8, 10, 2, 1, 0, 3, 11, 5, 4],
        [10, 6, 13, 11, 0, 9, 4, 12, 7, 2, 1, 5, 3, 8, 14],
        [7, 9, 0, 3, 6, 2, 10, 11, 14, 8, 13, 1, 5, 4, 12],
        [10, 13, 3, 7, 9, 11, 0, 12, 2, 6, 14, 5, 4, 8, 1],
        [12, 8, 14, 11, 10, 4, 1, 5, 9, 0, 7, 6, 2, 13, 3],
        [7, 8, 9, 3, 11, 14, 10, 4, 1, 12, 6, 0, 5, 2, 13],
        [9, 8, 6, 2, 7, 10, 0, 3, 14, 13, 4, 11, 5, 12, 1],
        [1, 7, 0, 9, 13, 6, 5, 8, 10, 3, 11, 12, 4, 14, 2],
        [12, 14, 10, 3, 0, 9, 4, 1, 8, 11, 5, 7, 2, 13, 6],
        [5, 14, 9, 12, 13, 8, 1, 10, 11, 3, 2, 6, 7, 4, 0],
        [12, 11, 13, 4, 9, 1, 14, 6, 0, 10, 8, 3, 2, 5, 7],
        [6, 9, 8, 3, 13, 14, 10, 5, 7, 0, 11, 2, 4, 12, 1],
        [14, 2, 10, 12, 0, 13, 1, 6, 4, 11, 8, 3, 7, 9, 5],
        [5, 7, 9, 4, 8, 2, 11, 1, 12, 10, 14, 0, 13, 3, 6],
        [7, 11, 0, 1, 10, 12, 14, 6, 13, 9, 5, 8, 4, 3, 2],
        [4, 2, 0, 12, 9, 13, 11, 14, 3, 8, 6, 5, 1, 7, 10],
        [10, 8, 4, 13, 2, 5, 0, 9, 1, 14, 7, 3, 6, 12, 11],
    ],
    'durations': [
        [Interval(38, 48), Interval(79, 105), Interval(25, 29), Interval(78, 88), Interval(67, 73), Interval(28, 30), Interval(94, 102), Interval(81, 101), Interval(54, 58), Interval(97, 99), Interval(25, 31), Interval(20, 20), Interval(45, 55), Interval(1, 1), Interval(6, 8)],
        [Interval(61, 65), Interval(69, 77), Interval(75, 85), Interval(21, 21), Interval(38, 42), Interval(29, 29), Interval(32, 34), Interval(88, 90), Interval(30, 38), Interval(40, 42), Interval(48, 62), Interval(75, 85), Interval(42, 52), Interval(4, 4), Interval(16, 18)],
        [Interval(1, 1), Interval(35, 45), Interval(43, 53), Interval(24, 26), Interval(83, 85), Interval(86, 88), Interval(19, 21), Interval(43, 53), Interval(2, 2), Interval(13, 17), Interval(88, 102), Interval(69, 93), Interval(43, 55), Interval(25, 33), Interval(5, 5)],
        [Interval(77, 97), Interval(70, 88), Interval(26, 34), Interval(43, 49), Interval(87, 101), Interval(10, 12), Interval(39, 41), Interval(25, 27), Interval(49, 55), Interval(33, 35), Interval(87, 95), Interval(67, 67), Interval(46, 48), Interval(97, 99), Interval(84, 110)],
        [Interval(20, 26), Interval(4, 4), Interval(23, 25), Interval(27, 33), Interval(33, 35), Interval(53, 57), Interval(40, 48), Interval(12, 12), Interval(37, 39), Interval(41, 55), Interval(21, 27), Interval(41, 53), Interval(26, 30), Interval(16, 18), Interval(54, 68)],
        [Interval(79, 95), Interval(44, 50), Interval(44, 48), Interval(67, 69), Interval(2, 2), Interval(56, 66), Interval(86, 112), Interval(70, 76), Interval(29, 35), Interval(62, 82), Interval(63, 67), Interval(15, 17), Interval(30, 30), Interval(84, 104), Interval(38, 44)],
        [Interval(49, 59), Interval(56, 64), Interval(1, 1), Interval(3, 3), Interval(58, 64), Interval(22, 28), Interval(35, 47), Interval(53, 61), Interval(80, 86), Interval(37, 39), Interval(33, 41), Interval(39, 41), Interval(73, 79), Interval(47, 57), Interval(92, 102)],
        [Interval(9, 9), Interval(24, 32), Interval(76, 76), Interval(47, 55), Interval(44, 56), Interval(40, 52), Interval(73, 87), Interval(87, 111), Interval(1, 1), Interval(56, 74), Interval(11, 13), Interval(8, 10), Interval(84, 110), Interval(57, 67), Interval(38, 48)],
        [Interval(53, 57), Interval(76, 96), Interval(33, 39), Interval(49, 57), Interval(14, 18), Interval(21, 25), Interval(30, 34), Interval(84, 100), Interval(73, 83), Interval(1, 1), Interval(75, 83), Interval(89, 93), Interval(88, 88), Interval(64, 84), Interval(28, 30)],
        [Interval(83, 103), Interval(12, 14), Interval(18, 22), Interval(4, 4), Interval(69, 73), Interval(45, 57), Interval(42, 50), Interval(80, 94), Interval(57, 59), Interval(12, 14), Interval(40, 40), Interval(68, 84), Interval(10, 10), Interval(3, 3), Interval(5, 5)],
        [Interval(4, 4), Interval(84, 106), Interval(94, 104), Interval(25, 33), Interval(44, 54), Interval(35, 39), Interval(43, 47), Interval(47, 63), Interval(37, 47), Interval(14, 14), Interval(88, 96), Interval(58, 62), Interval(47, 47), Interval(43, 47), Interval(43, 45)],
        [Interval(86, 108), Interval(56, 72), Interval(39, 51), Interval(22, 26), Interval(21, 25), Interval(77, 97), Interval(72, 80), Interval(50, 60), Interval(3, 3), Interval(83, 103), Interval(37, 49), Interval(51, 59), Interval(87, 95), Interval(84, 100), Interval(80, 82)],
        [Interval(19, 21), Interval(46, 50), Interval(9, 11), Interval(90, 108), Interval(59, 65), Interval(19, 25), Interval(98, 100), Interval(67, 67), Interval(12, 12), Interval(16, 16), Interval(74, 78), Interval(45, 53), Interval(70, 84), Interval(64, 70), Interval(19, 23)],
        [Interval(70, 84), Interval(71, 79), Interval(11, 13), Interval(75, 93), Interval(44, 58), Interval(42, 52), Interval(95, 97), Interval(6, 8), Interval(54, 72), Interval(73, 77), Interval(90, 94), Interval(69, 85), Interval(83, 85), Interval(76, 88), Interval(3, 3)],
        [Interval(86, 98), Interval(10, 12), Interval(43, 49), Interval(42, 54), Interval(51, 61), Interval(75, 77), Interval(85, 113), Interval(13, 15), Interval(45, 51), Interval(92, 98), Interval(6, 6), Interval(55, 67), Interval(37, 43), Interval(63, 67), Interval(39, 45)],
        [Interval(33, 43), Interval(44, 54), Interval(45, 51), Interval(22, 28), Interval(55, 73), Interval(89, 103), Interval(86, 92), Interval(90, 96), Interval(12, 14), Interval(61, 75), Interval(75, 85), Interval(19, 21), Interval(85, 91), Interval(71, 91), Interval(44, 48)],
        [Interval(70, 92), Interval(82, 82), Interval(69, 91), Interval(28, 34), Interval(80, 100), Interval(35, 37), Interval(59, 69), Interval(68, 88), Interval(44, 46), Interval(68, 82), Interval(92, 106), Interval(28, 30), Interval(87, 103), Interval(10, 12), Interval(85, 91)],
        [Interval(27, 29), Interval(11, 11), Interval(30, 40), Interval(13, 15), Interval(22, 28), Interval(44, 48), Interval(81, 97), Interval(67, 69), Interval(1, 1), Interval(64, 74), Interval(66, 88), Interval(46, 62), Interval(15, 19), Interval(19, 19), Interval(54, 68)],
        [Interval(17, 19), Interval(20, 24), Interval(67, 67), Interval(10, 12), Interval(8, 8), Interval(11, 13), Interval(68, 74), Interval(14, 16), Interval(76, 84), Interval(57, 67), Interval(18, 18), Interval(16, 18), Interval(67, 87), Interval(24, 30), Interval(20, 22)],
        [Interval(14, 18), Interval(31, 35), Interval(12, 14), Interval(11, 13), Interval(47, 55), Interval(3, 3), Interval(82, 90), Interval(37, 47), Interval(68, 72), Interval(71, 91), Interval(60, 72), Interval(24, 30), Interval(27, 31), Interval(69, 87), Interval(38, 40)],
    ],
    'name': 'int__sint20_15_10.F.15_01_interval',
    'has_intervals': True,
    'description': 'DMU sint20_15_10 ensanchada F.15_01',
}
