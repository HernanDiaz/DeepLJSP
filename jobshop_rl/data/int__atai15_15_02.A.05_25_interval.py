"""aTA 15x15 #02 con intervalos asimetricos (protocolo A.05_25).

Generado por scripts/e4_genera_asimetricas.py a partir de la version
simetrica: el valor crisp es el punto medio de aquella, y sobre el se
sortea p_lo = p - round(p*U[0,0.05]) y p_up = p + round(p*U[0,0.25]).
Las rutas de maquina son las mismas.
"""

from jobshop_rl.models.interval import Interval


INT__ATAI15_15_02_A_05_25_INTERVAL_DATA = {
    'num_jobs': 15,
    'num_machines': 15,
    'problem_id': 'int__atai15_15_02',
    'name': 'aTA 15x15 #02',
    'has_intervals': True,
    'description': 'aTA 15x15 #02 asimetrica A.05_25',
    'sequences': [[9, 14, 4, 13, 10, 3, 7, 8, 0, 5, 1, 2, 12, 6, 11], [10, 8, 11, 14, 3, 13, 9, 7, 4, 2, 6, 1, 5, 12, 0], [7, 0, 6, 5, 14, 13, 2, 11, 4, 12, 1, 9, 3, 10, 8], [9, 11, 14, 0, 1, 8, 5, 10, 12, 4, 13, 3, 6, 7, 2], [11, 4, 13, 3, 8, 1, 10, 12, 2, 14, 6, 7, 0, 9, 5], [5, 2, 1, 10, 0, 4, 8, 14, 6, 3, 9, 7, 11, 12, 13], [5, 10, 13, 0, 9, 8, 1, 11, 14, 7, 12, 2, 6, 4, 3], [12, 0, 9, 3, 13, 6, 5, 7, 2, 14, 11, 8, 10, 1, 4], [11, 10, 5, 13, 1, 9, 8, 7, 3, 6, 0, 2, 14, 12, 4], [2, 14, 3, 10, 6, 1, 0, 13, 11, 4, 5, 8, 7, 12, 9], [11, 14, 13, 5, 4, 9, 1, 6, 12, 0, 2, 8, 10, 3, 7], [12, 3, 10, 8, 4, 7, 13, 11, 14, 1, 2, 0, 5, 6, 9], [8, 13, 5, 0, 11, 9, 4, 12, 1, 10, 6, 2, 7, 14, 3], [2, 5, 4, 3, 9, 1, 11, 13, 7, 6, 10, 14, 0, 8, 12], [1, 10, 4, 2, 0, 7, 6, 9, 11, 12, 5, 14, 3, 13, 8]],
    'durations': [
        [Interval(83, 87), Interval(59, 66), Interval(10, 12), Interval(56, 66), Interval(63, 71), Interval(91, 99), Interval(69, 72), Interval(25, 28), Interval(97, 108), Interval(48, 51), Interval(42, 50), Interval(8, 9), Interval(86, 95), Interval(20, 22), Interval(69, 84)],
        [Interval(68, 71), Interval(27, 35), Interval(37, 40), Interval(34, 38), Interval(88, 104), Interval(35, 41), Interval(36, 39), Interval(27, 33), Interval(61, 75), Interval(83, 87), Interval(64, 70), Interval(11, 12), Interval(20, 20), Interval(82, 91), Interval(23, 27)],
        [Interval(33, 37), Interval(67, 82), Interval(93, 119), Interval(87, 106), Interval(81, 97), Interval(80, 96), Interval(58, 65), Interval(88, 109), Interval(19, 24), Interval(61, 68), Interval(21, 23), Interval(78, 86), Interval(38, 40), Interval(39, 42), Interval(79, 88)],
        [Interval(13, 16), Interval(14, 15), Interval(70, 85), Interval(86, 101), Interval(24, 25), Interval(16, 18), Interval(75, 89), Interval(68, 72), Interval(52, 58), Interval(67, 80), Interval(73, 82), Interval(88, 110), Interval(57, 62), Interval(7, 9), Interval(4, 4)],
        [Interval(91, 111), Interval(51, 62), Interval(63, 75), Interval(13, 15), Interval(19, 21), Interval(40, 49), Interval(71, 78), Interval(59, 73), Interval(19, 20), Interval(59, 68), Interval(83, 99), Interval(97, 118), Interval(72, 82), Interval(92, 99), Interval(18, 23)],
        [Interval(62, 69), Interval(60, 68), Interval(90, 115), Interval(16, 18), Interval(10, 11), Interval(69, 85), Interval(88, 108), Interval(68, 81), Interval(57, 67), Interval(40, 45), Interval(45, 51), Interval(61, 70), Interval(74, 86), Interval(81, 97), Interval(61, 65)],
        [Interval(49, 52), Interval(66, 68), Interval(86, 105), Interval(34, 39), Interval(43, 47), Interval(5, 6), Interval(8, 8), Interval(25, 31), Interval(70, 77), Interval(52, 63), Interval(78, 82), Interval(89, 96), Interval(60, 63), Interval(82, 89), Interval(68, 70)],
        [Interval(58, 65), Interval(64, 78), Interval(90, 93), Interval(42, 52), Interval(60, 65), Interval(87, 95), Interval(21, 23), Interval(1, 1), Interval(92, 102), Interval(18, 21), Interval(57, 70), Interval(12, 13), Interval(40, 51), Interval(11, 13), Interval(92, 104)],
        [Interval(89, 105), Interval(45, 52), Interval(51, 64), Interval(36, 38), Interval(89, 99), Interval(86, 101), Interval(61, 67), Interval(40, 47), Interval(68, 74), Interval(13, 15), Interval(16, 19), Interval(81, 96), Interval(48, 59), Interval(23, 28), Interval(23, 28)],
        [Interval(5, 6), Interval(34, 43), Interval(21, 25), Interval(14, 17), Interval(63, 80), Interval(3, 3), Interval(6, 6), Interval(95, 110), Interval(62, 79), Interval(63, 69), Interval(75, 77), Interval(93, 103), Interval(17, 21), Interval(60, 72), Interval(36, 41)],
        [Interval(35, 40), Interval(42, 43), Interval(61, 71), Interval(66, 82), Interval(73, 79), Interval(27, 33), Interval(51, 55), Interval(38, 45), Interval(40, 50), Interval(24, 29), Interval(9, 10), Interval(32, 37), Interval(50, 52), Interval(40, 44), Interval(98, 102)],
        [Interval(22, 26), Interval(31, 33), Interval(35, 35), Interval(10, 11), Interval(28, 31), Interval(67, 69), Interval(19, 23), Interval(8, 9), Interval(57, 59), Interval(61, 67), Interval(38, 47), Interval(32, 34), Interval(8, 10), Interval(32, 35), Interval(87, 93)],
        [Interval(27, 32), Interval(30, 37), Interval(3, 3), Interval(28, 32), Interval(65, 70), Interval(57, 64), Interval(24, 25), Interval(45, 49), Interval(79, 96), Interval(8, 10), Interval(43, 47), Interval(41, 47), Interval(2, 2), Interval(22, 25), Interval(51, 58)],
        [Interval(10, 13), Interval(91, 98), Interval(26, 30), Interval(58, 66), Interval(60, 74), Interval(22, 23), Interval(23, 28), Interval(7, 8), Interval(74, 82), Interval(61, 77), Interval(57, 63), Interval(95, 120), Interval(35, 39), Interval(52, 62), Interval(69, 83)],
        [Interval(35, 39), Interval(95, 121), Interval(37, 45), Interval(23, 29), Interval(81, 95), Interval(46, 57), Interval(69, 72), Interval(1, 1), Interval(89, 91), Interval(81, 103), Interval(68, 83), Interval(41, 51), Interval(19, 21), Interval(29, 35), Interval(30, 35)],
    ],
}
