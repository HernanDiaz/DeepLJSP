"""aTA 20x15 #02 con intervalos asimetricos (protocolo A.05_25).

Generado por scripts/e4_genera_asimetricas.py a partir de la version
simetrica: el valor crisp es el punto medio de aquella, y sobre el se
sortea p_lo = p - round(p*U[0,0.05]) y p_up = p + round(p*U[0,0.25]).
Las rutas de maquina son las mismas.
"""

from jobshop_rl.models.interval import Interval


INT__ATAI20_15_02_A_05_25_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__atai20_15_02',
    'name': 'aTA 20x15 #02',
    'has_intervals': True,
    'description': 'aTA 20x15 #02 asimetrica A.05_25',
    'sequences': [[2, 5, 1, 8, 3, 4, 14, 7, 10, 13, 11, 9, 12, 6, 0], [14, 8, 12, 4, 11, 3, 6, 9, 0, 10, 1, 13, 2, 7, 5], [7, 12, 1, 8, 2, 10, 3, 11, 13, 14, 5, 6, 0, 9, 4], [1, 8, 5, 11, 7, 6, 3, 2, 4, 9, 12, 13, 0, 14, 10], [8, 4, 12, 1, 3, 14, 2, 9, 13, 6, 5, 10, 11, 7, 0], [2, 14, 10, 7, 3, 0, 1, 13, 9, 6, 11, 12, 4, 5, 8], [0, 4, 13, 1, 8, 10, 11, 6, 9, 2, 5, 12, 7, 3, 14], [12, 2, 11, 9, 8, 10, 13, 4, 5, 14, 6, 3, 1, 7, 0], [7, 3, 4, 5, 13, 0, 11, 10, 9, 1, 8, 6, 12, 14, 2], [7, 14, 12, 6, 5, 9, 10, 0, 3, 4, 2, 1, 8, 13, 11], [0, 9, 13, 7, 6, 3, 11, 8, 10, 4, 2, 1, 14, 12, 5], [14, 10, 3, 12, 5, 7, 4, 6, 1, 2, 0, 13, 9, 11, 8], [11, 10, 5, 1, 3, 13, 9, 7, 8, 14, 0, 2, 6, 12, 4], [7, 6, 13, 10, 3, 1, 5, 11, 4, 8, 0, 12, 9, 2, 14], [2, 4, 14, 5, 0, 7, 10, 12, 1, 9, 3, 8, 6, 13, 11], [5, 14, 12, 7, 3, 13, 0, 9, 10, 6, 1, 2, 8, 4, 11], [14, 8, 1, 10, 11, 12, 7, 0, 3, 2, 9, 13, 5, 6, 4], [5, 2, 10, 3, 12, 4, 6, 11, 0, 13, 8, 14, 7, 1, 9], [0, 9, 10, 4, 2, 6, 13, 1, 3, 14, 7, 8, 5, 12, 11], [2, 12, 9, 8, 4, 6, 10, 14, 7, 5, 1, 11, 3, 0, 13]],
    'durations': [
        [Interval(53, 63), Interval(65, 66), Interval(46, 52), Interval(58, 63), Interval(8, 8), Interval(20, 21), Interval(63, 75), Interval(7, 7), Interval(76, 80), Interval(5, 6), Interval(58, 72), Interval(8, 9), Interval(87, 96), Interval(11, 12), Interval(78, 92)],
        [Interval(84, 99), Interval(74, 86), Interval(39, 41), Interval(75, 87), Interval(9, 10), Interval(23, 26), Interval(79, 95), Interval(49, 60), Interval(46, 54), Interval(47, 49), Interval(66, 73), Interval(50, 61), Interval(15, 18), Interval(5, 6), Interval(79, 94)],
        [Interval(81, 102), Interval(94, 105), Interval(25, 32), Interval(68, 77), Interval(31, 37), Interval(31, 36), Interval(20, 21), Interval(38, 39), Interval(40, 52), Interval(32, 35), Interval(70, 72), Interval(83, 89), Interval(23, 28), Interval(54, 57), Interval(54, 60)],
        [Interval(59, 75), Interval(81, 87), Interval(14, 17), Interval(35, 39), Interval(21, 23), Interval(20, 23), Interval(3, 4), Interval(11, 14), Interval(79, 102), Interval(89, 97), Interval(50, 58), Interval(82, 101), Interval(74, 83), Interval(3, 3), Interval(86, 98)],
        [Interval(80, 100), Interval(33, 35), Interval(15, 17), Interval(35, 37), Interval(93, 119), Interval(95, 101), Interval(81, 95), Interval(24, 27), Interval(58, 65), Interval(85, 105), Interval(11, 14), Interval(13, 16), Interval(26, 30), Interval(87, 93), Interval(83, 104)],
        [Interval(49, 59), Interval(20, 21), Interval(88, 101), Interval(96, 100), Interval(94, 100), Interval(40, 51), Interval(7, 8), Interval(66, 73), Interval(76, 86), Interval(44, 53), Interval(73, 79), Interval(88, 95), Interval(86, 106), Interval(1, 1), Interval(54, 57)],
        [Interval(34, 35), Interval(70, 85), Interval(45, 49), Interval(33, 41), Interval(76, 92), Interval(65, 81), Interval(85, 101), Interval(27, 33), Interval(2, 2), Interval(98, 123), Interval(9, 10), Interval(18, 18), Interval(27, 29), Interval(33, 40), Interval(88, 96)],
        [Interval(74, 93), Interval(57, 68), Interval(37, 40), Interval(28, 30), Interval(78, 85), Interval(96, 98), Interval(94, 103), Interval(90, 104), Interval(82, 88), Interval(66, 72), Interval(1, 1), Interval(85, 101), Interval(31, 38), Interval(64, 70), Interval(20, 24)],
        [Interval(16, 19), Interval(11, 14), Interval(18, 19), Interval(89, 112), Interval(57, 57), Interval(91, 113), Interval(16, 21), Interval(33, 40), Interval(59, 72), Interval(49, 53), Interval(35, 41), Interval(36, 42), Interval(60, 74), Interval(72, 75), Interval(24, 25)],
        [Interval(79, 83), Interval(81, 89), Interval(83, 92), Interval(43, 50), Interval(95, 120), Interval(62, 68), Interval(67, 73), Interval(56, 67), Interval(63, 72), Interval(86, 110), Interval(40, 52), Interval(76, 81), Interval(42, 53), Interval(75, 94), Interval(36, 41)],
        [Interval(53, 61), Interval(64, 73), Interval(8, 9), Interval(47, 57), Interval(81, 85), Interval(15, 16), Interval(91, 106), Interval(90, 105), Interval(56, 57), Interval(16, 16), Interval(62, 80), Interval(12, 13), Interval(62, 75), Interval(62, 65), Interval(52, 62)],
        [Interval(20, 25), Interval(70, 78), Interval(41, 50), Interval(28, 35), Interval(81, 99), Interval(5, 6), Interval(16, 19), Interval(73, 92), Interval(65, 81), Interval(46, 47), Interval(64, 83), Interval(82, 91), Interval(45, 54), Interval(28, 31), Interval(26, 26)],
        [Interval(92, 101), Interval(41, 49), Interval(47, 57), Interval(53, 65), Interval(57, 70), Interval(8, 9), Interval(40, 43), Interval(13, 15), Interval(35, 40), Interval(9, 9), Interval(73, 80), Interval(16, 16), Interval(48, 50), Interval(67, 79), Interval(43, 53)],
        [Interval(68, 81), Interval(89, 99), Interval(16, 17), Interval(18, 22), Interval(43, 48), Interval(46, 50), Interval(30, 34), Interval(29, 29), Interval(27, 33), Interval(83, 94), Interval(68, 88), Interval(91, 95), Interval(19, 20), Interval(11, 12), Interval(84, 107)],
        [Interval(40, 44), Interval(23, 25), Interval(80, 89), Interval(48, 55), Interval(24, 30), Interval(73, 75), Interval(34, 41), Interval(80, 99), Interval(69, 72), Interval(51, 64), Interval(5, 5), Interval(41, 50), Interval(8, 9), Interval(33, 37), Interval(93, 109)],
        [Interval(61, 76), Interval(4, 4), Interval(82, 103), Interval(51, 63), Interval(60, 71), Interval(52, 60), Interval(16, 16), Interval(17, 22), Interval(5, 5), Interval(42, 44), Interval(23, 27), Interval(87, 91), Interval(64, 70), Interval(76, 87), Interval(41, 43)],
        [Interval(17, 20), Interval(37, 42), Interval(54, 62), Interval(67, 79), Interval(55, 60), Interval(23, 28), Interval(93, 101), Interval(12, 13), Interval(94, 118), Interval(26, 30), Interval(53, 56), Interval(34, 43), Interval(41, 46), Interval(64, 80), Interval(23, 29)],
        [Interval(78, 94), Interval(6, 7), Interval(87, 102), Interval(66, 77), Interval(16, 18), Interval(55, 59), Interval(78, 93), Interval(96, 119), Interval(12, 14), Interval(19, 19), Interval(87, 91), Interval(3, 3), Interval(35, 38), Interval(65, 74), Interval(73, 79)],
        [Interval(38, 39), Interval(73, 80), Interval(46, 56), Interval(21, 24), Interval(79, 88), Interval(96, 114), Interval(34, 43), Interval(43, 50), Interval(72, 91), Interval(88, 97), Interval(97, 122), Interval(53, 58), Interval(87, 105), Interval(76, 98), Interval(46, 48)],
        [Interval(33, 41), Interval(55, 59), Interval(25, 27), Interval(62, 72), Interval(82, 83), Interval(37, 41), Interval(89, 104), Interval(32, 34), Interval(49, 59), Interval(61, 72), Interval(38, 43), Interval(61, 65), Interval(88, 100), Interval(13, 15), Interval(42, 47)],
    ],
}
