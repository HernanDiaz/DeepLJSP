"""aTA 15x15 #03 con intervalos asimetricos (protocolo A.05_25).

Generado por scripts/e4_genera_asimetricas.py a partir de la version
simetrica: el valor crisp es el punto medio de aquella, y sobre el se
sortea p_lo = p - round(p*U[0,0.05]) y p_up = p + round(p*U[0,0.25]).
Las rutas de maquina son las mismas.
"""

from jobshop_rl.models.interval import Interval


INT__ATAI15_15_03_A_05_25_INTERVAL_DATA = {
    'num_jobs': 15,
    'num_machines': 15,
    'problem_id': 'int__atai15_15_03',
    'name': 'aTA 15x15 #03',
    'has_intervals': True,
    'description': 'aTA 15x15 #03 asimetrica A.05_25',
    'sequences': [[7, 11, 8, 3, 12, 1, 13, 0, 14, 6, 9, 4, 2, 10, 5], [12, 1, 11, 9, 6, 3, 2, 4, 5, 8, 13, 14, 10, 0, 7], [1, 2, 9, 0, 3, 5, 8, 4, 14, 10, 12, 13, 7, 6, 11], [13, 10, 6, 2, 14, 7, 4, 11, 0, 5, 9, 3, 8, 1, 12], [1, 8, 4, 14, 6, 5, 3, 2, 9, 10, 13, 7, 11, 0, 12], [5, 14, 2, 12, 10, 1, 11, 4, 6, 9, 0, 13, 8, 3, 7], [5, 2, 0, 1, 8, 14, 11, 10, 7, 9, 6, 12, 4, 13, 3], [4, 7, 10, 1, 9, 8, 2, 14, 11, 3, 5, 6, 13, 12, 0], [14, 11, 0, 9, 10, 5, 3, 12, 8, 13, 6, 1, 7, 2, 4], [9, 0, 3, 10, 12, 13, 5, 1, 6, 14, 8, 11, 2, 7, 4], [7, 2, 1, 12, 3, 14, 4, 6, 5, 9, 8, 13, 10, 0, 11], [0, 8, 14, 12, 9, 5, 6, 10, 7, 11, 3, 4, 1, 13, 2], [8, 12, 10, 11, 14, 3, 6, 1, 4, 5, 0, 9, 13, 2, 7], [13, 2, 11, 0, 14, 10, 3, 1, 12, 4, 5, 6, 7, 9, 8], [1, 13, 0, 11, 2, 10, 4, 8, 3, 5, 7, 6, 9, 12, 14]],
    'durations': [
        [Interval(66, 74), Interval(78, 82), Interval(79, 95), Interval(61, 63), Interval(76, 94), Interval(3, 3), Interval(38, 44), Interval(59, 71), Interval(52, 59), Interval(65, 80), Interval(85, 95), Interval(78, 89), Interval(3, 3), Interval(12, 12), Interval(87, 95)],
        [Interval(80, 99), Interval(51, 62), Interval(46, 47), Interval(15, 18), Interval(87, 102), Interval(73, 94), Interval(50, 59), Interval(18, 19), Interval(21, 26), Interval(81, 86), Interval(26, 27), Interval(29, 34), Interval(5, 6), Interval(88, 103), Interval(22, 26)],
        [Interval(59, 63), Interval(46, 57), Interval(88, 103), Interval(53, 61), Interval(38, 42), Interval(74, 89), Interval(69, 72), Interval(94, 116), Interval(19, 21), Interval(33, 39), Interval(44, 52), Interval(70, 76), Interval(89, 95), Interval(9, 11), Interval(20, 24)],
        [Interval(31, 40), Interval(81, 93), Interval(76, 100), Interval(29, 31), Interval(94, 107), Interval(30, 34), Interval(11, 13), Interval(25, 28), Interval(41, 41), Interval(55, 64), Interval(12, 14), Interval(10, 11), Interval(92, 97), Interval(3, 4), Interval(72, 77)],
        [Interval(35, 36), Interval(47, 52), Interval(10, 12), Interval(42, 45), Interval(67, 81), Interval(72, 76), Interval(18, 20), Interval(63, 74), Interval(37, 41), Interval(57, 63), Interval(31, 39), Interval(11, 13), Interval(70, 74), Interval(85, 104), Interval(12, 14)],
        [Interval(83, 101), Interval(31, 34), Interval(6, 7), Interval(13, 13), Interval(83, 91), Interval(93, 106), Interval(35, 43), Interval(76, 89), Interval(46, 47), Interval(29, 37), Interval(55, 68), Interval(61, 77), Interval(32, 36), Interval(50, 53), Interval(71, 81)],
        [Interval(28, 31), Interval(75, 84), Interval(21, 24), Interval(27, 33), Interval(17, 21), Interval(42, 45), Interval(14, 14), Interval(15, 16), Interval(15, 18), Interval(48, 51), Interval(71, 81), Interval(19, 23), Interval(99, 110), Interval(38, 44), Interval(62, 77)],
        [Interval(12, 15), Interval(73, 78), Interval(4, 5), Interval(3, 3), Interval(15, 19), Interval(59, 70), Interval(50, 61), Interval(38, 42), Interval(47, 56), Interval(24, 29), Interval(18, 21), Interval(53, 64), Interval(5, 5), Interval(68, 85), Interval(26, 31)],
        [Interval(68, 79), Interval(13, 16), Interval(32, 36), Interval(46, 48), Interval(86, 98), Interval(30, 32), Interval(97, 113), Interval(47, 55), Interval(24, 31), Interval(38, 42), Interval(92, 116), Interval(21, 23), Interval(59, 67), Interval(58, 61), Interval(16, 18)],
        [Interval(26, 31), Interval(4, 4), Interval(34, 40), Interval(78, 100), Interval(49, 59), Interval(45, 55), Interval(81, 102), Interval(45, 54), Interval(92, 97), Interval(68, 83), Interval(18, 19), Interval(22, 24), Interval(93, 106), Interval(72, 91), Interval(22, 25)],
        [Interval(35, 39), Interval(17, 21), Interval(78, 83), Interval(65, 74), Interval(46, 52), Interval(5, 5), Interval(50, 51), Interval(22, 24), Interval(82, 84), Interval(35, 43), Interval(92, 113), Interval(7, 7), Interval(52, 62), Interval(91, 109), Interval(37, 46)],
        [Interval(76, 82), Interval(57, 68), Interval(61, 71), Interval(42, 45), Interval(1, 1), Interval(55, 68), Interval(73, 90), Interval(47, 60), Interval(79, 91), Interval(25, 30), Interval(77, 93), Interval(9, 10), Interval(23, 26), Interval(23, 29), Interval(40, 52)],
        [Interval(37, 45), Interval(83, 92), Interval(37, 46), Interval(38, 44), Interval(80, 99), Interval(35, 44), Interval(11, 12), Interval(16, 19), Interval(97, 116), Interval(14, 17), Interval(55, 65), Interval(64, 74), Interval(57, 60), Interval(92, 100), Interval(17, 19)],
        [Interval(10, 12), Interval(84, 90), Interval(91, 111), Interval(60, 76), Interval(58, 66), Interval(60, 68), Interval(75, 87), Interval(89, 105), Interval(39, 43), Interval(76, 91), Interval(8, 10), Interval(27, 29), Interval(93, 104), Interval(67, 83), Interval(61, 73)],
        [Interval(72, 83), Interval(12, 15), Interval(14, 17), Interval(70, 88), Interval(3, 3), Interval(46, 58), Interval(80, 93), Interval(81, 103), Interval(51, 64), Interval(57, 63), Interval(91, 117), Interval(85, 90), Interval(87, 107), Interval(67, 80), Interval(74, 88)],
    ],
}
