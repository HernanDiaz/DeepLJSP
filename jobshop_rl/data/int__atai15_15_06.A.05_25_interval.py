"""aTA 15x15 #06 con intervalos asimetricos (protocolo A.05_25).

Generado por scripts/e4_genera_asimetricas.py a partir de la version
simetrica: el valor crisp es el punto medio de aquella, y sobre el se
sortea p_lo = p - round(p*U[0,0.05]) y p_up = p + round(p*U[0,0.25]).
Las rutas de maquina son las mismas.
"""

from jobshop_rl.models.interval import Interval


INT__ATAI15_15_06_A_05_25_INTERVAL_DATA = {
    'num_jobs': 15,
    'num_machines': 15,
    'problem_id': 'int__atai15_15_06',
    'name': 'aTA 15x15 #06',
    'has_intervals': True,
    'description': 'aTA 15x15 #06 asimetrica A.05_25',
    'sequences': [[7, 12, 5, 8, 3, 14, 13, 9, 0, 1, 4, 2, 6, 11, 10], [8, 0, 5, 13, 6, 1, 4, 2, 3, 11, 10, 12, 9, 14, 7], [6, 8, 7, 1, 9, 5, 12, 4, 0, 2, 14, 11, 3, 13, 10], [12, 0, 14, 7, 13, 1, 6, 8, 11, 2, 3, 9, 5, 10, 4], [8, 2, 12, 11, 10, 9, 4, 3, 14, 5, 0, 7, 6, 13, 1], [13, 8, 6, 11, 14, 9, 12, 7, 0, 1, 10, 2, 5, 3, 4], [4, 1, 2, 13, 7, 6, 0, 8, 12, 14, 10, 9, 5, 3, 11], [4, 10, 14, 3, 6, 13, 11, 9, 0, 5, 1, 12, 8, 7, 2], [7, 1, 5, 4, 14, 8, 0, 9, 12, 3, 10, 2, 13, 11, 6], [3, 6, 13, 4, 5, 10, 2, 8, 12, 11, 9, 7, 14, 1, 0], [1, 4, 7, 2, 14, 10, 12, 13, 6, 5, 9, 0, 3, 8, 11], [0, 7, 14, 13, 8, 3, 6, 9, 5, 12, 10, 4, 1, 2, 11], [14, 10, 0, 8, 12, 13, 4, 11, 1, 3, 6, 5, 2, 9, 7], [13, 4, 8, 6, 5, 2, 9, 0, 11, 12, 1, 3, 14, 7, 10], [14, 2, 6, 4, 3, 11, 1, 5, 7, 0, 8, 10, 9, 12, 13]],
    'durations': [
        [Interval(95, 116), Interval(22, 27), Interval(68, 72), Interval(25, 30), Interval(27, 33), Interval(16, 16), Interval(26, 28), Interval(69, 83), Interval(18, 20), Interval(55, 65), Interval(43, 51), Interval(5, 6), Interval(12, 13), Interval(87, 108), Interval(63, 74)],
        [Interval(31, 38), Interval(79, 94), Interval(93, 119), Interval(75, 88), Interval(54, 68), Interval(45, 46), Interval(60, 63), Interval(71, 76), Interval(22, 28), Interval(42, 50), Interval(91, 114), Interval(19, 20), Interval(5, 6), Interval(70, 85), Interval(69, 77)],
        [Interval(60, 66), Interval(90, 116), Interval(62, 63), Interval(77, 97), Interval(10, 11), Interval(64, 76), Interval(26, 30), Interval(90, 94), Interval(23, 27), Interval(25, 30), Interval(8, 8), Interval(67, 71), Interval(29, 35), Interval(64, 68), Interval(96, 102)],
        [Interval(78, 87), Interval(86, 89), Interval(65, 73), Interval(23, 28), Interval(53, 66), Interval(16, 19), Interval(68, 78), Interval(31, 39), Interval(72, 82), Interval(3, 4), Interval(2, 2), Interval(70, 78), Interval(4, 4), Interval(67, 67), Interval(27, 28)],
        [Interval(45, 53), Interval(93, 99), Interval(11, 12), Interval(39, 43), Interval(88, 106), Interval(2, 2), Interval(95, 113), Interval(10, 10), Interval(42, 46), Interval(63, 69), Interval(26, 29), Interval(55, 66), Interval(71, 89), Interval(83, 94), Interval(78, 93)],
        [Interval(5, 6), Interval(87, 103), Interval(88, 93), Interval(83, 105), Interval(65, 71), Interval(36, 41), Interval(65, 70), Interval(88, 109), Interval(89, 109), Interval(26, 30), Interval(12, 13), Interval(7, 8), Interval(94, 105), Interval(66, 73), Interval(13, 14)],
        [Interval(88, 100), Interval(32, 38), Interval(76, 80), Interval(74, 86), Interval(88, 99), Interval(66, 79), Interval(78, 94), Interval(90, 103), Interval(11, 13), Interval(5, 6), Interval(83, 94), Interval(40, 45), Interval(4, 5), Interval(2, 2), Interval(69, 77)],
        [Interval(77, 90), Interval(23, 29), Interval(41, 50), Interval(80, 96), Interval(44, 51), Interval(28, 36), Interval(3, 3), Interval(41, 43), Interval(5, 5), Interval(44, 46), Interval(80, 87), Interval(59, 72), Interval(58, 64), Interval(76, 87), Interval(42, 46)],
        [Interval(19, 23), Interval(53, 63), Interval(19, 21), Interval(71, 87), Interval(63, 73), Interval(36, 41), Interval(55, 57), Interval(61, 73), Interval(39, 49), Interval(72, 87), Interval(53, 64), Interval(83, 94), Interval(53, 62), Interval(59, 63), Interval(6, 6)],
        [Interval(26, 28), Interval(57, 71), Interval(6, 6), Interval(88, 104), Interval(6, 6), Interval(37, 46), Interval(61, 71), Interval(34, 40), Interval(24, 26), Interval(58, 62), Interval(76, 92), Interval(29, 33), Interval(1, 1), Interval(7, 8), Interval(69, 81)],
        [Interval(4, 4), Interval(50, 62), Interval(6, 6), Interval(10, 11), Interval(51, 53), Interval(85, 108), Interval(38, 38), Interval(37, 41), Interval(34, 36), Interval(43, 50), Interval(99, 123), Interval(87, 109), Interval(50, 60), Interval(15, 17), Interval(95, 123)],
        [Interval(28, 35), Interval(11, 12), Interval(74, 86), Interval(50, 57), Interval(35, 43), Interval(57, 73), Interval(44, 45), Interval(38, 48), Interval(63, 71), Interval(47, 56), Interval(39, 47), Interval(33, 39), Interval(77, 98), Interval(37, 43), Interval(28, 34)],
        [Interval(30, 32), Interval(32, 34), Interval(38, 41), Interval(25, 26), Interval(38, 42), Interval(84, 89), Interval(37, 43), Interval(61, 73), Interval(15, 15), Interval(41, 43), Interval(89, 103), Interval(63, 66), Interval(15, 19), Interval(79, 87), Interval(93, 97)],
        [Interval(9, 11), Interval(21, 23), Interval(8, 9), Interval(53, 63), Interval(77, 92), Interval(75, 76), Interval(77, 84), Interval(58, 65), Interval(66, 68), Interval(95, 121), Interval(23, 26), Interval(23, 28), Interval(91, 96), Interval(90, 112), Interval(22, 25)],
        [Interval(78, 100), Interval(29, 35), Interval(66, 79), Interval(56, 60), Interval(44, 51), Interval(28, 30), Interval(48, 58), Interval(28, 29), Interval(63, 76), Interval(61, 74), Interval(79, 88), Interval(22, 27), Interval(93, 108), Interval(53, 57), Interval(46, 49)],
    ],
}
