"""aTA 15x15 #07 con intervalos asimetricos (protocolo A.05_25).

Generado por scripts/e4_genera_asimetricas.py a partir de la version
simetrica: el valor crisp es el punto medio de aquella, y sobre el se
sortea p_lo = p - round(p*U[0,0.05]) y p_up = p + round(p*U[0,0.25]).
Las rutas de maquina son las mismas.
"""

from jobshop_rl.models.interval import Interval


INT__ATAI15_15_07_A_05_25_INTERVAL_DATA = {
    'num_jobs': 15,
    'num_machines': 15,
    'problem_id': 'int__atai15_15_07',
    'name': 'aTA 15x15 #07',
    'has_intervals': True,
    'description': 'aTA 15x15 #07 asimetrica A.05_25',
    'sequences': [[13, 12, 7, 0, 5, 11, 9, 10, 1, 2, 3, 14, 4, 6, 8], [2, 1, 8, 14, 13, 0, 5, 11, 9, 12, 10, 7, 3, 4, 6], [0, 3, 1, 7, 4, 8, 14, 5, 6, 2, 13, 12, 9, 10, 11], [9, 11, 0, 7, 12, 14, 6, 1, 13, 10, 4, 5, 3, 2, 8], [8, 13, 5, 10, 9, 14, 12, 2, 3, 0, 6, 11, 7, 4, 1], [12, 13, 14, 9, 5, 1, 6, 7, 0, 3, 8, 10, 4, 11, 2], [9, 0, 5, 4, 12, 14, 6, 1, 3, 8, 13, 11, 2, 10, 7], [12, 1, 9, 14, 6, 10, 2, 7, 4, 11, 13, 5, 3, 8, 0], [6, 5, 12, 4, 1, 14, 9, 0, 7, 8, 10, 13, 2, 11, 3], [8, 3, 5, 4, 1, 10, 7, 9, 13, 2, 0, 11, 6, 12, 14], [4, 2, 1, 0, 14, 10, 9, 6, 11, 12, 3, 8, 7, 13, 5], [8, 3, 13, 14, 2, 11, 5, 4, 9, 12, 10, 7, 1, 0, 6], [7, 1, 10, 4, 0, 8, 12, 6, 13, 2, 3, 9, 11, 14, 5], [8, 11, 3, 7, 1, 12, 6, 4, 10, 13, 2, 5, 14, 9, 0], [5, 13, 14, 6, 9, 11, 7, 2, 12, 8, 3, 4, 10, 1, 0]],
    'durations': [
        [Interval(49, 53), Interval(18, 23), Interval(6, 7), Interval(19, 21), Interval(1, 1), Interval(25, 32), Interval(87, 105), Interval(43, 54), Interval(27, 30), Interval(17, 22), Interval(50, 51), Interval(78, 89), Interval(10, 12), Interval(50, 58), Interval(39, 46)],
        [Interval(42, 53), Interval(82, 89), Interval(2, 2), Interval(77, 78), Interval(83, 104), Interval(85, 92), Interval(59, 65), Interval(19, 23), Interval(55, 61), Interval(12, 14), Interval(66, 83), Interval(34, 38), Interval(55, 63), Interval(34, 37), Interval(82, 90)],
        [Interval(60, 74), Interval(69, 81), Interval(72, 81), Interval(61, 65), Interval(93, 116), Interval(29, 31), Interval(24, 26), Interval(33, 36), Interval(87, 103), Interval(81, 95), Interval(87, 112), Interval(25, 32), Interval(98, 106), Interval(62, 73), Interval(31, 36)],
        [Interval(10, 12), Interval(15, 15), Interval(90, 105), Interval(76, 93), Interval(75, 93), Interval(59, 71), Interval(1, 1), Interval(46, 54), Interval(22, 24), Interval(27, 29), Interval(21, 22), Interval(16, 20), Interval(44, 52), Interval(95, 112), Interval(11, 13)],
        [Interval(81, 95), Interval(49, 62), Interval(67, 84), Interval(76, 85), Interval(7, 8), Interval(27, 33), Interval(96, 117), Interval(52, 58), Interval(29, 34), Interval(79, 99), Interval(58, 70), Interval(88, 103), Interval(79, 88), Interval(53, 54), Interval(34, 40)],
        [Interval(3, 3), Interval(31, 39), Interval(97, 122), Interval(94, 106), Interval(74, 92), Interval(38, 48), Interval(40, 42), Interval(10, 11), Interval(9, 11), Interval(92, 104), Interval(7, 8), Interval(48, 59), Interval(20, 22), Interval(44, 46), Interval(56, 73)],
        [Interval(27, 29), Interval(91, 111), Interval(4, 5), Interval(50, 59), Interval(66, 79), Interval(5, 6), Interval(17, 22), Interval(50, 63), Interval(46, 55), Interval(20, 24), Interval(49, 56), Interval(62, 75), Interval(92, 100), Interval(81, 94), Interval(88, 96)],
        [Interval(25, 27), Interval(78, 92), Interval(56, 67), Interval(15, 17), Interval(66, 68), Interval(48, 57), Interval(63, 75), Interval(87, 96), Interval(54, 70), Interval(82, 98), Interval(55, 64), Interval(15, 17), Interval(33, 37), Interval(96, 119), Interval(61, 63)],
        [Interval(79, 84), Interval(30, 31), Interval(22, 25), Interval(15, 19), Interval(84, 88), Interval(48, 52), Interval(56, 65), Interval(62, 74), Interval(29, 32), Interval(97, 101), Interval(47, 48), Interval(36, 37), Interval(87, 92), Interval(59, 76), Interval(57, 63)],
        [Interval(27, 31), Interval(24, 28), Interval(67, 80), Interval(65, 73), Interval(59, 64), Interval(57, 64), Interval(93, 105), Interval(31, 36), Interval(14, 17), Interval(24, 27), Interval(82, 85), Interval(95, 108), Interval(53, 66), Interval(64, 72), Interval(30, 36)],
        [Interval(19, 21), Interval(96, 117), Interval(13, 14), Interval(86, 99), Interval(25, 31), Interval(72, 78), Interval(90, 95), Interval(84, 91), Interval(68, 76), Interval(40, 47), Interval(16, 20), Interval(52, 57), Interval(62, 72), Interval(1, 1), Interval(91, 99)],
        [Interval(57, 70), Interval(22, 27), Interval(46, 52), Interval(10, 12), Interval(1, 1), Interval(21, 23), Interval(3, 4), Interval(81, 88), Interval(92, 98), Interval(57, 61), Interval(76, 88), Interval(72, 75), Interval(57, 61), Interval(41, 43), Interval(61, 66)],
        [Interval(69, 82), Interval(78, 88), Interval(12, 13), Interval(54, 56), Interval(22, 27), Interval(8, 9), Interval(89, 104), Interval(26, 29), Interval(16, 17), Interval(37, 42), Interval(26, 31), Interval(49, 59), Interval(41, 49), Interval(77, 88), Interval(92, 106)],
        [Interval(69, 79), Interval(76, 87), Interval(29, 33), Interval(89, 106), Interval(46, 54), Interval(45, 49), Interval(41, 50), Interval(74, 82), Interval(89, 99), Interval(28, 36), Interval(8, 10), Interval(92, 94), Interval(16, 19), Interval(59, 72), Interval(6, 7)],
        [Interval(89, 90), Interval(43, 46), Interval(40, 44), Interval(31, 37), Interval(10, 11), Interval(83, 100), Interval(16, 17), Interval(22, 26), Interval(89, 93), Interval(44, 49), Interval(34, 41), Interval(17, 20), Interval(89, 95), Interval(44, 53), Interval(91, 100)],
    ],
}
