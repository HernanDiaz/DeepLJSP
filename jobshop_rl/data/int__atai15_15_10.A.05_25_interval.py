"""aTA 15x15 #10 con intervalos asimetricos (protocolo A.05_25).

Generado por scripts/e4_genera_asimetricas.py a partir de la version
simetrica: el valor crisp es el punto medio de aquella, y sobre el se
sortea p_lo = p - round(p*U[0,0.05]) y p_up = p + round(p*U[0,0.25]).
Las rutas de maquina son las mismas.
"""

from jobshop_rl.models.interval import Interval


INT__ATAI15_15_10_A_05_25_INTERVAL_DATA = {
    'num_jobs': 15,
    'num_machines': 15,
    'problem_id': 'int__atai15_15_10',
    'name': 'aTA 15x15 #10',
    'has_intervals': True,
    'description': 'aTA 15x15 #10 asimetrica A.05_25',
    'sequences': [[8, 2, 7, 14, 12, 0, 4, 3, 13, 5, 9, 10, 6, 1, 11], [2, 8, 6, 4, 11, 0, 9, 7, 5, 3, 1, 10, 13, 14, 12], [5, 11, 8, 14, 12, 1, 4, 9, 10, 6, 13, 0, 2, 3, 7], [9, 13, 8, 6, 12, 5, 10, 2, 1, 0, 14, 11, 3, 4, 7], [8, 10, 3, 13, 14, 5, 4, 0, 12, 11, 9, 6, 2, 1, 7], [7, 2, 9, 5, 10, 4, 3, 1, 11, 8, 6, 14, 13, 0, 12], [2, 10, 1, 12, 14, 3, 0, 4, 9, 5, 11, 13, 7, 8, 6], [13, 6, 11, 12, 8, 7, 14, 5, 3, 4, 0, 10, 2, 1, 9], [8, 4, 6, 7, 0, 11, 13, 12, 2, 3, 10, 1, 5, 14, 9], [2, 6, 12, 9, 8, 11, 1, 3, 13, 4, 10, 5, 0, 7, 14], [0, 9, 4, 8, 10, 2, 11, 12, 14, 6, 3, 7, 5, 1, 13], [8, 1, 12, 5, 7, 10, 9, 4, 11, 6, 13, 2, 14, 0, 3], [13, 14, 2, 9, 7, 8, 12, 4, 10, 6, 1, 0, 5, 11, 3], [1, 0, 12, 2, 13, 8, 3, 14, 4, 7, 6, 9, 11, 10, 5], [3, 13, 2, 5, 9, 6, 7, 4, 8, 0, 12, 10, 14, 1, 11]],
    'durations': [
        [Interval(34, 35), Interval(76, 88), Interval(78, 80), Interval(63, 81), Interval(53, 57), Interval(14, 16), Interval(90, 114), Interval(69, 72), Interval(14, 14), Interval(86, 94), Interval(94, 114), Interval(47, 51), Interval(35, 40), Interval(81, 94), Interval(1, 1)],
        [Interval(80, 92), Interval(40, 48), Interval(21, 26), Interval(28, 32), Interval(52, 53), Interval(69, 73), Interval(16, 18), Interval(89, 95), Interval(53, 58), Interval(63, 68), Interval(11, 15), Interval(82, 94), Interval(62, 69), Interval(44, 56), Interval(30, 30)],
        [Interval(57, 62), Interval(41, 46), Interval(69, 73), Interval(2, 2), Interval(50, 60), Interval(36, 44), Interval(82, 95), Interval(78, 98), Interval(60, 72), Interval(56, 68), Interval(65, 78), Interval(23, 25), Interval(97, 116), Interval(91, 103), Interval(67, 86)],
        [Interval(13, 15), Interval(58, 63), Interval(33, 39), Interval(6, 7), Interval(25, 31), Interval(57, 69), Interval(1, 1), Interval(43, 54), Interval(94, 110), Interval(29, 35), Interval(93, 99), Interval(89, 115), Interval(48, 57), Interval(50, 52), Interval(15, 18)],
        [Interval(92, 97), Interval(37, 49), Interval(73, 89), Interval(96, 99), Interval(2, 2), Interval(36, 40), Interval(66, 84), Interval(31, 36), Interval(95, 112), Interval(61, 70), Interval(4, 5), Interval(10, 12), Interval(48, 52), Interval(92, 102), Interval(76, 81)],
        [Interval(73, 84), Interval(28, 33), Interval(41, 53), Interval(45, 53), Interval(55, 71), Interval(85, 101), Interval(33, 40), Interval(13, 14), Interval(7, 8), Interval(49, 52), Interval(23, 28), Interval(38, 47), Interval(20, 22), Interval(96, 102), Interval(70, 89)],
        [Interval(3, 3), Interval(77, 82), Interval(66, 79), Interval(93, 113), Interval(87, 98), Interval(31, 34), Interval(50, 60), Interval(61, 70), Interval(83, 97), Interval(2, 2), Interval(88, 91), Interval(63, 66), Interval(15, 17), Interval(17, 21), Interval(25, 29)],
        [Interval(22, 25), Interval(29, 32), Interval(21, 24), Interval(53, 62), Interval(67, 69), Interval(63, 75), Interval(87, 108), Interval(92, 116), Interval(5, 6), Interval(37, 40), Interval(5, 6), Interval(41, 43), Interval(16, 19), Interval(54, 63), Interval(44, 56)],
        [Interval(43, 50), Interval(58, 66), Interval(83, 99), Interval(60, 63), Interval(49, 51), Interval(55, 60), Interval(3, 3), Interval(39, 50), Interval(25, 32), Interval(18, 21), Interval(14, 16), Interval(17, 20), Interval(71, 74), Interval(34, 43), Interval(58, 67)],
        [Interval(26, 32), Interval(14, 15), Interval(76, 84), Interval(24, 28), Interval(55, 58), Interval(67, 78), Interval(56, 74), Interval(19, 20), Interval(28, 31), Interval(32, 34), Interval(85, 90), Interval(29, 31), Interval(90, 111), Interval(11, 13), Interval(11, 12)],
        [Interval(67, 71), Interval(93, 106), Interval(48, 62), Interval(2, 2), Interval(82, 91), Interval(18, 22), Interval(28, 33), Interval(36, 41), Interval(56, 72), Interval(31, 38), Interval(37, 41), Interval(96, 102), Interval(87, 108), Interval(48, 50), Interval(67, 82)],
        [Interval(60, 71), Interval(7, 8), Interval(80, 84), Interval(79, 92), Interval(56, 68), Interval(80, 96), Interval(16, 19), Interval(1, 1), Interval(67, 74), Interval(7, 7), Interval(3, 3), Interval(80, 90), Interval(8, 9), Interval(12, 15), Interval(90, 106)],
        [Interval(92, 104), Interval(80, 98), Interval(4, 5), Interval(75, 92), Interval(9, 11), Interval(78, 88), Interval(74, 85), Interval(5, 6), Interval(49, 59), Interval(8, 9), Interval(44, 54), Interval(4, 4), Interval(57, 69), Interval(93, 98), Interval(74, 76)],
        [Interval(32, 38), Interval(86, 89), Interval(31, 34), Interval(66, 83), Interval(31, 39), Interval(10, 12), Interval(43, 48), Interval(73, 76), Interval(78, 86), Interval(49, 53), Interval(54, 63), Interval(96, 107), Interval(44, 53), Interval(83, 84), Interval(21, 27)],
        [Interval(11, 14), Interval(35, 41), Interval(64, 76), Interval(17, 21), Interval(42, 45), Interval(44, 48), Interval(63, 79), Interval(70, 89), Interval(92, 112), Interval(28, 33), Interval(85, 88), Interval(94, 109), Interval(90, 114), Interval(66, 80), Interval(56, 60)],
    ],
}
