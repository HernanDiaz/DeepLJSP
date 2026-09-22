"""aTA 20x15 #07 con intervalos asimetricos (protocolo A.05_25).

Generado por scripts/e4_genera_asimetricas.py a partir de la version
simetrica: el valor crisp es el punto medio de aquella, y sobre el se
sortea p_lo = p - round(p*U[0,0.05]) y p_up = p + round(p*U[0,0.25]).
Las rutas de maquina son las mismas.
"""

from jobshop_rl.models.interval import Interval


INT__ATAI20_15_07_A_05_25_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__atai20_15_07',
    'name': 'aTA 20x15 #07',
    'has_intervals': True,
    'description': 'aTA 20x15 #07 asimetrica A.05_25',
    'sequences': [[6, 8, 11, 0, 14, 13, 9, 5, 3, 12, 10, 2, 7, 4, 1], [0, 9, 1, 6, 5, 13, 11, 8, 3, 4, 12, 14, 7, 2, 10], [8, 3, 9, 1, 0, 10, 5, 14, 12, 13, 6, 2, 7, 11, 4], [5, 1, 7, 10, 0, 2, 13, 11, 14, 3, 6, 9, 8, 12, 4], [2, 9, 6, 7, 0, 8, 13, 5, 10, 3, 12, 4, 14, 1, 11], [5, 3, 9, 2, 1, 4, 10, 8, 13, 0, 11, 12, 6, 14, 7], [8, 7, 12, 9, 6, 14, 4, 11, 5, 1, 3, 13, 10, 0, 2], [13, 7, 6, 11, 2, 0, 14, 4, 3, 1, 10, 8, 9, 12, 5], [1, 14, 0, 10, 11, 8, 7, 5, 9, 3, 4, 6, 12, 2, 13], [13, 1, 3, 14, 5, 9, 2, 0, 11, 7, 12, 4, 10, 6, 8], [10, 5, 9, 13, 6, 8, 11, 4, 14, 0, 7, 2, 12, 1, 3], [13, 9, 14, 10, 3, 7, 2, 5, 6, 11, 8, 1, 0, 12, 4], [5, 9, 7, 8, 10, 13, 2, 6, 1, 0, 12, 11, 3, 4, 14], [9, 11, 6, 7, 2, 8, 14, 3, 0, 12, 4, 13, 5, 1, 10], [10, 2, 1, 5, 0, 3, 14, 11, 4, 8, 9, 7, 12, 6, 13], [12, 14, 0, 2, 10, 5, 13, 3, 7, 11, 1, 9, 6, 8, 4], [8, 6, 12, 4, 13, 10, 5, 7, 9, 0, 1, 14, 3, 2, 11], [14, 5, 12, 4, 1, 13, 6, 2, 8, 7, 10, 11, 9, 3, 0], [7, 2, 6, 3, 8, 14, 5, 9, 4, 13, 0, 11, 12, 1, 10], [10, 7, 13, 4, 5, 3, 6, 1, 8, 0, 12, 11, 9, 14, 2]],
    'durations': [
        [Interval(40, 41), Interval(55, 63), Interval(94, 109), Interval(31, 37), Interval(70, 81), Interval(31, 31), Interval(54, 55), Interval(36, 42), Interval(91, 94), Interval(71, 85), Interval(77, 83), Interval(39, 44), Interval(3, 3), Interval(85, 89), Interval(28, 31)],
        [Interval(20, 21), Interval(55, 70), Interval(66, 73), Interval(48, 60), Interval(33, 44), Interval(56, 64), Interval(89, 104), Interval(51, 53), Interval(96, 119), Interval(94, 99), Interval(90, 105), Interval(32, 39), Interval(54, 56), Interval(70, 77), Interval(79, 97)],
        [Interval(94, 108), Interval(5, 6), Interval(93, 108), Interval(84, 94), Interval(31, 33), Interval(5, 5), Interval(15, 17), Interval(19, 23), Interval(72, 79), Interval(50, 53), Interval(22, 26), Interval(61, 69), Interval(86, 107), Interval(64, 69), Interval(23, 29)],
        [Interval(77, 87), Interval(57, 66), Interval(40, 42), Interval(33, 39), Interval(91, 113), Interval(61, 66), Interval(8, 9), Interval(74, 88), Interval(58, 68), Interval(40, 52), Interval(36, 42), Interval(3, 4), Interval(69, 83), Interval(78, 81), Interval(34, 41)],
        [Interval(70, 87), Interval(63, 78), Interval(25, 27), Interval(58, 70), Interval(54, 64), Interval(67, 79), Interval(85, 102), Interval(82, 107), Interval(43, 44), Interval(7, 7), Interval(35, 40), Interval(85, 92), Interval(94, 114), Interval(91, 96), Interval(97, 111)],
        [Interval(80, 83), Interval(69, 76), Interval(51, 55), Interval(71, 80), Interval(56, 71), Interval(67, 77), Interval(49, 56), Interval(36, 45), Interval(87, 92), Interval(21, 26), Interval(9, 11), Interval(96, 110), Interval(29, 31), Interval(92, 102), Interval(43, 44)],
        [Interval(68, 73), Interval(62, 68), Interval(64, 77), Interval(14, 18), Interval(37, 47), Interval(92, 115), Interval(92, 110), Interval(66, 72), Interval(5, 5), Interval(60, 69), Interval(63, 66), Interval(65, 84), Interval(2, 2), Interval(30, 36), Interval(17, 20)],
        [Interval(7, 7), Interval(10, 12), Interval(65, 67), Interval(61, 65), Interval(91, 104), Interval(87, 102), Interval(83, 89), Interval(79, 94), Interval(31, 39), Interval(59, 75), Interval(5, 5), Interval(21, 22), Interval(5, 6), Interval(48, 59), Interval(36, 38)],
        [Interval(9, 9), Interval(30, 35), Interval(75, 93), Interval(47, 54), Interval(24, 24), Interval(67, 77), Interval(65, 79), Interval(36, 41), Interval(80, 99), Interval(66, 71), Interval(62, 69), Interval(4, 5), Interval(60, 77), Interval(52, 53), Interval(64, 68)],
        [Interval(65, 71), Interval(71, 89), Interval(84, 96), Interval(27, 29), Interval(41, 49), Interval(13, 16), Interval(17, 21), Interval(73, 76), Interval(69, 85), Interval(19, 24), Interval(96, 102), Interval(72, 90), Interval(64, 75), Interval(8, 10), Interval(13, 15)],
        [Interval(82, 99), Interval(30, 35), Interval(76, 83), Interval(62, 75), Interval(17, 18), Interval(71, 80), Interval(63, 70), Interval(69, 80), Interval(28, 28), Interval(12, 15), Interval(17, 20), Interval(55, 64), Interval(17, 17), Interval(41, 47), Interval(58, 64)],
        [Interval(84, 102), Interval(35, 38), Interval(83, 107), Interval(27, 32), Interval(22, 26), Interval(69, 84), Interval(48, 52), Interval(78, 82), Interval(30, 33), Interval(17, 19), Interval(55, 65), Interval(53, 57), Interval(79, 90), Interval(4, 4), Interval(63, 79)],
        [Interval(6, 7), Interval(60, 72), Interval(76, 82), Interval(78, 84), Interval(59, 65), Interval(16, 20), Interval(41, 50), Interval(18, 21), Interval(53, 62), Interval(16, 17), Interval(66, 78), Interval(20, 23), Interval(66, 80), Interval(48, 52), Interval(4, 4)],
        [Interval(33, 39), Interval(85, 99), Interval(23, 28), Interval(67, 77), Interval(12, 15), Interval(57, 67), Interval(49, 53), Interval(56, 63), Interval(82, 104), Interval(15, 18), Interval(54, 58), Interval(80, 86), Interval(60, 73), Interval(5, 5), Interval(36, 39)],
        [Interval(70, 83), Interval(19, 22), Interval(93, 119), Interval(9, 9), Interval(81, 106), Interval(87, 96), Interval(3, 3), Interval(66, 73), Interval(50, 64), Interval(28, 31), Interval(28, 36), Interval(22, 27), Interval(10, 11), Interval(9, 11), Interval(62, 74)],
        [Interval(22, 28), Interval(33, 42), Interval(73, 88), Interval(33, 40), Interval(84, 97), Interval(40, 47), Interval(70, 78), Interval(15, 16), Interval(49, 57), Interval(90, 94), Interval(1, 1), Interval(41, 43), Interval(7, 8), Interval(61, 67), Interval(7, 7)],
        [Interval(18, 19), Interval(60, 75), Interval(96, 97), Interval(48, 58), Interval(4, 5), Interval(69, 71), Interval(65, 83), Interval(50, 62), Interval(42, 50), Interval(39, 42), Interval(31, 39), Interval(89, 113), Interval(11, 11), Interval(45, 53), Interval(99, 119)],
        [Interval(1, 1), Interval(92, 99), Interval(44, 55), Interval(12, 14), Interval(11, 13), Interval(81, 84), Interval(54, 70), Interval(38, 45), Interval(80, 102), Interval(42, 46), Interval(75, 80), Interval(21, 25), Interval(23, 29), Interval(46, 55), Interval(42, 49)],
        [Interval(97, 110), Interval(37, 45), Interval(91, 94), Interval(72, 80), Interval(75, 79), Interval(70, 77), Interval(46, 57), Interval(31, 32), Interval(80, 98), Interval(81, 102), Interval(61, 75), Interval(91, 114), Interval(57, 73), Interval(26, 26), Interval(13, 17)],
        [Interval(77, 88), Interval(51, 61), Interval(71, 73), Interval(9, 9), Interval(87, 97), Interval(29, 37), Interval(34, 36), Interval(33, 42), Interval(50, 55), Interval(85, 109), Interval(96, 113), Interval(33, 40), Interval(73, 77), Interval(66, 80), Interval(30, 33)],
    ],
}
