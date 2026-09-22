"""aTA 15x15 #08 con intervalos asimetricos (protocolo A.05_25).

Generado por scripts/e4_genera_asimetricas.py a partir de la version
simetrica: el valor crisp es el punto medio de aquella, y sobre el se
sortea p_lo = p - round(p*U[0,0.05]) y p_up = p + round(p*U[0,0.25]).
Las rutas de maquina son las mismas.
"""

from jobshop_rl.models.interval import Interval


INT__ATAI15_15_08_A_05_25_INTERVAL_DATA = {
    'num_jobs': 15,
    'num_machines': 15,
    'problem_id': 'int__atai15_15_08',
    'name': 'aTA 15x15 #08',
    'has_intervals': True,
    'description': 'aTA 15x15 #08 asimetrica A.05_25',
    'sequences': [[3, 6, 7, 13, 4, 1, 12, 10, 8, 14, 0, 9, 5, 2, 11], [2, 12, 1, 13, 3, 4, 8, 14, 0, 10, 7, 5, 9, 11, 6], [8, 14, 3, 0, 10, 5, 9, 13, 2, 11, 6, 4, 7, 1, 12], [5, 13, 11, 4, 14, 2, 9, 8, 10, 3, 6, 7, 1, 0, 12], [13, 5, 2, 14, 1, 8, 4, 3, 11, 6, 7, 12, 9, 0, 10], [14, 11, 2, 5, 8, 10, 0, 4, 9, 7, 13, 3, 1, 6, 12], [8, 12, 5, 10, 7, 11, 2, 13, 0, 14, 6, 9, 1, 4, 3], [9, 7, 12, 3, 6, 2, 10, 13, 1, 8, 14, 4, 0, 5, 11], [0, 4, 5, 1, 11, 7, 6, 2, 14, 13, 8, 9, 3, 10, 12], [8, 11, 7, 1, 14, 13, 12, 4, 6, 9, 10, 0, 5, 2, 3], [12, 4, 5, 13, 6, 0, 1, 7, 9, 8, 11, 10, 14, 2, 3], [3, 14, 4, 13, 5, 9, 8, 0, 7, 12, 6, 1, 10, 11, 2], [10, 8, 4, 1, 2, 0, 7, 14, 12, 13, 9, 6, 3, 11, 5], [6, 2, 0, 14, 1, 4, 12, 3, 10, 7, 8, 9, 5, 13, 11], [10, 2, 9, 13, 5, 0, 6, 7, 1, 14, 11, 4, 12, 3, 8]],
    'durations': [
        [Interval(80, 102), Interval(1, 1), Interval(96, 110), Interval(54, 66), Interval(29, 34), Interval(78, 85), Interval(81, 92), Interval(9, 11), Interval(47, 49), Interval(31, 35), Interval(19, 23), Interval(88, 102), Interval(65, 70), Interval(86, 90), Interval(61, 80)],
        [Interval(4, 5), Interval(68, 80), Interval(77, 94), Interval(21, 25), Interval(81, 92), Interval(91, 105), Interval(64, 73), Interval(49, 60), Interval(79, 103), Interval(93, 116), Interval(68, 75), Interval(38, 39), Interval(36, 38), Interval(99, 114), Interval(73, 77)],
        [Interval(44, 50), Interval(56, 70), Interval(63, 74), Interval(72, 92), Interval(85, 94), Interval(55, 66), Interval(53, 58), Interval(34, 39), Interval(57, 64), Interval(80, 101), Interval(23, 27), Interval(92, 97), Interval(23, 24), Interval(54, 68), Interval(80, 93)],
        [Interval(34, 39), Interval(66, 78), Interval(52, 62), Interval(94, 99), Interval(8, 9), Interval(77, 93), Interval(78, 97), Interval(37, 47), Interval(39, 41), Interval(3, 3), Interval(56, 73), Interval(79, 83), Interval(29, 37), Interval(74, 78), Interval(69, 83)],
        [Interval(84, 86), Interval(79, 88), Interval(35, 43), Interval(56, 65), Interval(93, 102), Interval(33, 40), Interval(14, 16), Interval(3, 4), Interval(87, 93), Interval(95, 120), Interval(9, 11), Interval(41, 47), Interval(92, 114), Interval(26, 31), Interval(27, 30)],
        [Interval(28, 29), Interval(11, 13), Interval(66, 75), Interval(2, 2), Interval(33, 41), Interval(69, 73), Interval(61, 68), Interval(82, 95), Interval(72, 75), Interval(55, 59), Interval(94, 118), Interval(78, 96), Interval(70, 85), Interval(88, 94), Interval(23, 26)],
        [Interval(21, 26), Interval(5, 6), Interval(94, 107), Interval(5, 5), Interval(22, 25), Interval(15, 18), Interval(75, 82), Interval(83, 103), Interval(73, 91), Interval(44, 57), Interval(34, 39), Interval(88, 99), Interval(94, 120), Interval(42, 46), Interval(35, 46)],
        [Interval(47, 60), Interval(79, 84), Interval(59, 62), Interval(84, 109), Interval(39, 49), Interval(6, 6), Interval(79, 102), Interval(77, 96), Interval(43, 49), Interval(79, 95), Interval(9, 10), Interval(80, 105), Interval(97, 100), Interval(36, 47), Interval(66, 82)],
        [Interval(74, 81), Interval(50, 62), Interval(65, 73), Interval(66, 84), Interval(6, 6), Interval(25, 26), Interval(98, 112), Interval(6, 6), Interval(34, 41), Interval(26, 30), Interval(49, 58), Interval(81, 92), Interval(5, 5), Interval(88, 91), Interval(1, 1)],
        [Interval(82, 88), Interval(62, 65), Interval(54, 65), Interval(73, 81), Interval(89, 99), Interval(66, 78), Interval(33, 35), Interval(13, 15), Interval(50, 59), Interval(33, 40), Interval(89, 103), Interval(4, 4), Interval(17, 19), Interval(94, 117), Interval(73, 80)],
        [Interval(39, 48), Interval(8, 10), Interval(34, 40), Interval(5, 6), Interval(1, 1), Interval(49, 62), Interval(32, 33), Interval(77, 86), Interval(86, 97), Interval(74, 85), Interval(45, 50), Interval(62, 69), Interval(41, 46), Interval(15, 17), Interval(11, 13)],
        [Interval(37, 45), Interval(81, 92), Interval(47, 51), Interval(73, 92), Interval(15, 15), Interval(10, 11), Interval(89, 93), Interval(40, 51), Interval(93, 110), Interval(96, 116), Interval(16, 19), Interval(47, 55), Interval(20, 22), Interval(92, 106), Interval(19, 25)],
        [Interval(88, 103), Interval(22, 25), Interval(11, 13), Interval(14, 17), Interval(37, 44), Interval(63, 76), Interval(28, 33), Interval(38, 48), Interval(87, 100), Interval(13, 15), Interval(27, 30), Interval(6, 7), Interval(23, 27), Interval(4, 5), Interval(22, 27)],
        [Interval(14, 15), Interval(64, 67), Interval(4, 4), Interval(57, 62), Interval(7, 8), Interval(6, 7), Interval(5, 6), Interval(47, 55), Interval(54, 62), Interval(56, 64), Interval(2, 2), Interval(1, 1), Interval(4, 5), Interval(81, 96), Interval(73, 93)],
        [Interval(24, 25), Interval(66, 79), Interval(4, 4), Interval(19, 23), Interval(79, 98), Interval(48, 60), Interval(23, 28), Interval(14, 16), Interval(14, 16), Interval(89, 99), Interval(82, 102), Interval(93, 110), Interval(61, 66), Interval(16, 17), Interval(3, 3)],
    ],
}
