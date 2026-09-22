"""aTA 15x15 #09 con intervalos asimetricos (protocolo A.05_25).

Generado por scripts/e4_genera_asimetricas.py a partir de la version
simetrica: el valor crisp es el punto medio de aquella, y sobre el se
sortea p_lo = p - round(p*U[0,0.05]) y p_up = p + round(p*U[0,0.25]).
Las rutas de maquina son las mismas.
"""

from jobshop_rl.models.interval import Interval


INT__ATAI15_15_09_A_05_25_INTERVAL_DATA = {
    'num_jobs': 15,
    'num_machines': 15,
    'problem_id': 'int__atai15_15_09',
    'name': 'aTA 15x15 #09',
    'has_intervals': True,
    'description': 'aTA 15x15 #09 asimetrica A.05_25',
    'sequences': [[3, 13, 11, 4, 2, 9, 10, 6, 12, 7, 5, 14, 8, 1, 0], [13, 9, 14, 0, 4, 5, 6, 11, 1, 7, 8, 12, 10, 3, 2], [1, 14, 13, 8, 10, 4, 0, 12, 5, 2, 11, 6, 9, 7, 3], [14, 5, 4, 3, 10, 7, 1, 11, 13, 6, 9, 12, 2, 8, 0], [14, 1, 13, 6, 12, 4, 5, 2, 9, 0, 3, 7, 11, 8, 10], [9, 11, 14, 10, 13, 7, 8, 2, 1, 0, 12, 5, 4, 6, 3], [3, 7, 11, 8, 4, 9, 1, 12, 10, 6, 0, 14, 5, 2, 13], [14, 13, 5, 0, 9, 8, 2, 3, 1, 11, 6, 10, 4, 7, 12], [3, 2, 0, 11, 1, 4, 5, 13, 7, 12, 9, 10, 8, 6, 14], [14, 9, 11, 13, 1, 5, 3, 4, 0, 12, 6, 2, 8, 10, 7], [14, 12, 2, 5, 4, 1, 13, 0, 8, 10, 7, 11, 3, 6, 9], [4, 13, 3, 1, 11, 8, 9, 7, 0, 2, 6, 10, 5, 12, 14], [11, 9, 1, 8, 12, 14, 2, 10, 7, 0, 13, 6, 3, 5, 4], [1, 4, 5, 6, 11, 3, 9, 10, 8, 2, 7, 13, 14, 12, 0], [13, 2, 4, 12, 7, 3, 8, 0, 11, 14, 9, 6, 1, 5, 10]],
    'durations': [
        [Interval(90, 105), Interval(14, 15), Interval(44, 54), Interval(25, 26), Interval(87, 92), Interval(52, 57), Interval(7, 8), Interval(75, 82), Interval(90, 102), Interval(8, 8), Interval(19, 22), Interval(54, 58), Interval(68, 71), Interval(63, 69), Interval(95, 117)],
        [Interval(32, 34), Interval(1, 1), Interval(39, 44), Interval(72, 87), Interval(41, 50), Interval(70, 73), Interval(96, 97), Interval(77, 85), Interval(84, 104), Interval(77, 80), Interval(87, 99), Interval(88, 95), Interval(49, 55), Interval(82, 98), Interval(3, 3)],
        [Interval(88, 94), Interval(97, 122), Interval(80, 87), Interval(45, 49), Interval(77, 79), Interval(66, 78), Interval(93, 108), Interval(40, 49), Interval(39, 49), Interval(11, 14), Interval(1, 1), Interval(69, 73), Interval(26, 33), Interval(77, 91), Interval(96, 122)],
        [Interval(49, 58), Interval(1, 1), Interval(21, 22), Interval(71, 79), Interval(45, 56), Interval(20, 24), Interval(60, 63), Interval(33, 40), Interval(79, 92), Interval(55, 66), Interval(67, 70), Interval(23, 26), Interval(56, 62), Interval(43, 46), Interval(54, 68)],
        [Interval(15, 16), Interval(15, 17), Interval(15, 17), Interval(77, 91), Interval(8, 8), Interval(70, 81), Interval(84, 91), Interval(51, 53), Interval(76, 88), Interval(60, 70), Interval(93, 107), Interval(84, 94), Interval(44, 54), Interval(79, 94), Interval(18, 22)],
        [Interval(76, 98), Interval(63, 74), Interval(94, 102), Interval(9, 9), Interval(85, 103), Interval(89, 95), Interval(11, 14), Interval(64, 69), Interval(53, 58), Interval(67, 72), Interval(34, 39), Interval(13, 14), Interval(3, 3), Interval(52, 67), Interval(59, 72)],
        [Interval(41, 42), Interval(37, 40), Interval(40, 49), Interval(9, 11), Interval(36, 45), Interval(25, 28), Interval(75, 78), Interval(74, 95), Interval(16, 17), Interval(38, 42), Interval(30, 35), Interval(77, 89), Interval(33, 35), Interval(92, 110), Interval(28, 34)],
        [Interval(92, 98), Interval(24, 28), Interval(48, 59), Interval(66, 72), Interval(52, 60), Interval(19, 21), Interval(51, 57), Interval(28, 31), Interval(50, 55), Interval(33, 36), Interval(36, 46), Interval(18, 19), Interval(41, 49), Interval(45, 54), Interval(94, 99)],
        [Interval(70, 74), Interval(65, 81), Interval(3, 3), Interval(94, 121), Interval(67, 69), Interval(8, 9), Interval(15, 18), Interval(84, 95), Interval(71, 79), Interval(20, 21), Interval(88, 108), Interval(58, 71), Interval(65, 83), Interval(60, 66), Interval(39, 50)],
        [Interval(29, 35), Interval(43, 43), Interval(80, 81), Interval(62, 79), Interval(14, 16), Interval(6, 7), Interval(35, 37), Interval(88, 92), Interval(71, 83), Interval(50, 62), Interval(63, 70), Interval(31, 35), Interval(16, 17), Interval(61, 66), Interval(7, 9)],
        [Interval(18, 18), Interval(88, 90), Interval(53, 63), Interval(24, 30), Interval(70, 75), Interval(92, 108), Interval(85, 100), Interval(66, 81), Interval(85, 94), Interval(82, 102), Interval(57, 60), Interval(35, 40), Interval(78, 81), Interval(41, 53), Interval(82, 92)],
        [Interval(50, 61), Interval(64, 76), Interval(85, 101), Interval(55, 63), Interval(24, 30), Interval(70, 75), Interval(18, 19), Interval(4, 5), Interval(68, 74), Interval(40, 49), Interval(27, 29), Interval(36, 43), Interval(41, 48), Interval(81, 96), Interval(83, 98)],
        [Interval(2, 2), Interval(39, 45), Interval(13, 16), Interval(75, 80), Interval(30, 35), Interval(63, 81), Interval(69, 86), Interval(64, 68), Interval(92, 99), Interval(44, 52), Interval(28, 35), Interval(47, 55), Interval(92, 98), Interval(48, 58), Interval(37, 42)],
        [Interval(79, 99), Interval(87, 99), Interval(34, 42), Interval(50, 53), Interval(73, 86), Interval(14, 15), Interval(31, 36), Interval(86, 100), Interval(85, 101), Interval(54, 66), Interval(48, 61), Interval(23, 28), Interval(18, 21), Interval(38, 42), Interval(92, 112)],
        [Interval(72, 82), Interval(44, 48), Interval(72, 81), Interval(70, 79), Interval(65, 70), Interval(6, 7), Interval(15, 18), Interval(23, 29), Interval(24, 29), Interval(44, 46), Interval(4, 4), Interval(21, 26), Interval(98, 108), Interval(10, 12), Interval(81, 95)],
    ],
}
