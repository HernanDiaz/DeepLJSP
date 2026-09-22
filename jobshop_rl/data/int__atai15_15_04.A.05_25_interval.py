"""aTA 15x15 #04 con intervalos asimetricos (protocolo A.05_25).

Generado por scripts/e4_genera_asimetricas.py a partir de la version
simetrica: el valor crisp es el punto medio de aquella, y sobre el se
sortea p_lo = p - round(p*U[0,0.05]) y p_up = p + round(p*U[0,0.25]).
Las rutas de maquina son las mismas.
"""

from jobshop_rl.models.interval import Interval


INT__ATAI15_15_04_A_05_25_INTERVAL_DATA = {
    'num_jobs': 15,
    'num_machines': 15,
    'problem_id': 'int__atai15_15_04',
    'name': 'aTA 15x15 #04',
    'has_intervals': True,
    'description': 'aTA 15x15 #04 asimetrica A.05_25',
    'sequences': [[3, 7, 6, 14, 9, 8, 5, 4, 10, 1, 0, 12, 11, 2, 13], [1, 11, 0, 5, 8, 13, 3, 10, 9, 2, 12, 6, 4, 7, 14], [7, 3, 8, 11, 0, 4, 9, 13, 1, 10, 6, 5, 14, 12, 2], [6, 11, 5, 13, 3, 2, 1, 4, 9, 12, 8, 0, 14, 7, 10], [1, 11, 6, 5, 8, 7, 12, 9, 2, 14, 13, 3, 0, 4, 10], [11, 2, 12, 1, 14, 0, 6, 9, 3, 13, 7, 10, 4, 5, 8], [14, 7, 11, 0, 12, 8, 9, 10, 3, 13, 4, 1, 2, 6, 5], [7, 4, 13, 5, 14, 11, 2, 12, 6, 1, 0, 10, 9, 3, 8], [7, 4, 14, 10, 3, 0, 13, 8, 1, 2, 6, 12, 11, 9, 5], [2, 12, 10, 3, 6, 5, 14, 9, 13, 4, 0, 11, 7, 8, 1], [11, 9, 3, 7, 6, 4, 0, 2, 5, 1, 10, 8, 13, 12, 14], [0, 4, 1, 9, 2, 11, 13, 10, 7, 6, 8, 12, 14, 3, 5], [6, 0, 4, 10, 2, 14, 9, 13, 11, 12, 1, 8, 5, 3, 7], [5, 10, 13, 2, 7, 4, 8, 6, 9, 0, 12, 11, 1, 14, 3], [11, 2, 0, 4, 14, 5, 9, 10, 6, 12, 8, 1, 7, 3, 13]],
    'durations': [
        [Interval(70, 85), Interval(50, 60), Interval(41, 47), Interval(30, 33), Interval(59, 63), Interval(45, 48), Interval(87, 98), Interval(33, 39), Interval(27, 30), Interval(84, 103), Interval(67, 86), Interval(55, 60), Interval(68, 75), Interval(48, 61), Interval(24, 28)],
        [Interval(19, 22), Interval(75, 85), Interval(76, 88), Interval(47, 49), Interval(39, 46), Interval(66, 78), Interval(42, 53), Interval(62, 79), Interval(83, 99), Interval(60, 70), Interval(29, 31), Interval(54, 60), Interval(19, 21), Interval(89, 97), Interval(65, 84)],
        [Interval(92, 111), Interval(7, 8), Interval(2, 2), Interval(91, 115), Interval(60, 72), Interval(82, 95), Interval(73, 91), Interval(36, 43), Interval(8, 9), Interval(85, 92), Interval(7, 9), Interval(42, 52), Interval(2, 2), Interval(72, 83), Interval(87, 112)],
        [Interval(57, 70), Interval(64, 83), Interval(83, 90), Interval(33, 35), Interval(19, 20), Interval(19, 22), Interval(91, 96), Interval(39, 45), Interval(96, 102), Interval(93, 117), Interval(24, 26), Interval(39, 43), Interval(73, 84), Interval(86, 101), Interval(74, 85)],
        [Interval(44, 49), Interval(59, 67), Interval(8, 9), Interval(28, 34), Interval(32, 32), Interval(41, 47), Interval(25, 29), Interval(4, 5), Interval(68, 80), Interval(78, 82), Interval(89, 116), Interval(27, 28), Interval(29, 37), Interval(17, 18), Interval(41, 53)],
        [Interval(83, 97), Interval(56, 63), Interval(44, 56), Interval(93, 94), Interval(63, 79), Interval(83, 101), Interval(40, 47), Interval(4, 5), Interval(15, 17), Interval(15, 16), Interval(52, 67), Interval(38, 42), Interval(76, 78), Interval(54, 68), Interval(31, 38)],
        [Interval(65, 80), Interval(89, 109), Interval(16, 20), Interval(46, 59), Interval(77, 87), Interval(65, 72), Interval(59, 68), Interval(21, 23), Interval(71, 86), Interval(46, 58), Interval(37, 42), Interval(7, 8), Interval(11, 12), Interval(22, 26), Interval(61, 65)],
        [Interval(12, 13), Interval(21, 22), Interval(59, 64), Interval(41, 46), Interval(21, 23), Interval(81, 99), Interval(60, 74), Interval(50, 54), Interval(25, 28), Interval(51, 54), Interval(52, 58), Interval(54, 59), Interval(28, 33), Interval(80, 83), Interval(30, 36)],
        [Interval(48, 53), Interval(28, 28), Interval(67, 72), Interval(25, 29), Interval(65, 74), Interval(4, 5), Interval(18, 21), Interval(89, 108), Interval(23, 29), Interval(54, 61), Interval(57, 71), Interval(46, 51), Interval(83, 99), Interval(82, 96), Interval(92, 111)],
        [Interval(35, 43), Interval(33, 37), Interval(64, 80), Interval(62, 71), Interval(29, 35), Interval(40, 42), Interval(51, 62), Interval(72, 89), Interval(42, 48), Interval(13, 14), Interval(41, 49), Interval(6, 6), Interval(32, 33), Interval(91, 95), Interval(36, 39)],
        [Interval(59, 64), Interval(9, 11), Interval(88, 104), Interval(37, 40), Interval(28, 30), Interval(23, 26), Interval(13, 15), Interval(59, 72), Interval(44, 54), Interval(92, 97), Interval(83, 103), Interval(71, 82), Interval(18, 22), Interval(78, 96), Interval(11, 12)],
        [Interval(74, 75), Interval(61, 64), Interval(41, 54), Interval(25, 31), Interval(93, 103), Interval(62, 72), Interval(39, 43), Interval(59, 63), Interval(61, 66), Interval(75, 93), Interval(41, 42), Interval(8, 9), Interval(20, 25), Interval(11, 12), Interval(68, 74)],
        [Interval(9, 11), Interval(21, 24), Interval(9, 10), Interval(8, 9), Interval(51, 64), Interval(31, 34), Interval(88, 111), Interval(75, 79), Interval(2, 2), Interval(62, 67), Interval(62, 67), Interval(94, 105), Interval(42, 44), Interval(12, 12), Interval(41, 46)],
        [Interval(66, 68), Interval(7, 7), Interval(87, 93), Interval(50, 56), Interval(85, 99), Interval(4, 5), Interval(1, 1), Interval(54, 66), Interval(80, 83), Interval(46, 57), Interval(35, 41), Interval(8, 9), Interval(88, 97), Interval(39, 42), Interval(11, 12)],
        [Interval(42, 51), Interval(24, 27), Interval(24, 28), Interval(14, 14), Interval(33, 42), Interval(55, 62), Interval(29, 35), Interval(63, 68), Interval(4, 5), Interval(14, 16), Interval(68, 72), Interval(91, 107), Interval(21, 26), Interval(58, 73), Interval(60, 74)],
    ],
}
