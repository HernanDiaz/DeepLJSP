"""aTA 20x15 #09 con intervalos asimetricos (protocolo A.05_25).

Generado por scripts/e4_genera_asimetricas.py a partir de la version
simetrica: el valor crisp es el punto medio de aquella, y sobre el se
sortea p_lo = p - round(p*U[0,0.05]) y p_up = p + round(p*U[0,0.25]).
Las rutas de maquina son las mismas.
"""

from jobshop_rl.models.interval import Interval


INT__ATAI20_15_09_A_05_25_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__atai20_15_09',
    'name': 'aTA 20x15 #09',
    'has_intervals': True,
    'description': 'aTA 20x15 #09 asimetrica A.05_25',
    'sequences': [[8, 1, 10, 7, 9, 5, 6, 3, 2, 13, 4, 0, 14, 11, 12], [1, 9, 4, 5, 0, 11, 6, 7, 12, 2, 14, 8, 13, 10, 3], [6, 2, 8, 9, 3, 5, 4, 12, 11, 7, 10, 13, 0, 14, 1], [4, 9, 1, 2, 13, 3, 6, 0, 12, 5, 10, 7, 8, 11, 14], [6, 7, 9, 13, 11, 1, 5, 0, 12, 3, 14, 2, 4, 8, 10], [2, 12, 6, 13, 8, 4, 1, 14, 5, 9, 10, 0, 3, 7, 11], [13, 2, 12, 5, 11, 6, 8, 4, 10, 7, 1, 0, 3, 9, 14], [9, 8, 14, 7, 3, 10, 1, 12, 4, 13, 11, 6, 5, 0, 2], [14, 3, 6, 8, 12, 9, 4, 5, 1, 7, 0, 10, 2, 11, 13], [11, 4, 14, 8, 13, 10, 9, 0, 5, 6, 2, 12, 3, 1, 7], [6, 2, 8, 0, 3, 5, 7, 10, 14, 9, 11, 13, 4, 1, 12], [9, 1, 14, 0, 13, 2, 7, 8, 5, 11, 4, 10, 6, 3, 12], [8, 11, 12, 3, 7, 13, 6, 1, 14, 5, 9, 2, 4, 0, 10], [8, 12, 7, 11, 3, 14, 6, 10, 5, 1, 2, 9, 0, 4, 13], [10, 13, 12, 8, 3, 11, 5, 14, 0, 4, 2, 6, 1, 9, 7], [8, 6, 10, 14, 1, 11, 3, 5, 12, 9, 2, 4, 0, 7, 13], [13, 2, 8, 14, 7, 0, 9, 6, 3, 11, 10, 5, 12, 1, 4], [0, 13, 12, 6, 7, 2, 11, 14, 8, 3, 4, 10, 1, 5, 9], [9, 6, 2, 12, 0, 8, 11, 4, 5, 1, 7, 3, 14, 10, 13], [2, 8, 6, 12, 14, 10, 13, 5, 0, 7, 11, 9, 3, 4, 1]],
    'durations': [
        [Interval(77, 87), Interval(22, 23), Interval(87, 93), Interval(45, 47), Interval(41, 43), Interval(57, 64), Interval(12, 13), Interval(90, 102), Interval(39, 46), Interval(67, 86), Interval(71, 83), Interval(13, 16), Interval(47, 53), Interval(93, 104), Interval(62, 65)],
        [Interval(85, 100), Interval(56, 68), Interval(44, 54), Interval(1, 1), Interval(72, 84), Interval(3, 4), Interval(87, 111), Interval(76, 82), Interval(28, 36), Interval(17, 20), Interval(12, 14), Interval(59, 64), Interval(88, 113), Interval(34, 38), Interval(24, 24)],
        [Interval(56, 57), Interval(6, 7), Interval(72, 90), Interval(35, 40), Interval(56, 70), Interval(25, 27), Interval(90, 96), Interval(21, 25), Interval(45, 52), Interval(88, 95), Interval(46, 56), Interval(2, 2), Interval(57, 64), Interval(65, 78), Interval(54, 67)],
        [Interval(73, 89), Interval(38, 46), Interval(1, 1), Interval(36, 46), Interval(52, 57), Interval(83, 85), Interval(50, 57), Interval(38, 40), Interval(64, 73), Interval(80, 90), Interval(42, 54), Interval(67, 83), Interval(24, 29), Interval(27, 31), Interval(12, 13)],
        [Interval(14, 17), Interval(71, 81), Interval(24, 28), Interval(68, 73), Interval(8, 9), Interval(94, 117), Interval(14, 16), Interval(13, 15), Interval(31, 34), Interval(74, 86), Interval(13, 15), Interval(89, 100), Interval(38, 48), Interval(57, 68), Interval(45, 50)],
        [Interval(90, 99), Interval(2, 2), Interval(68, 73), Interval(22, 26), Interval(38, 44), Interval(32, 34), Interval(35, 42), Interval(31, 35), Interval(50, 60), Interval(31, 37), Interval(10, 12), Interval(62, 69), Interval(82, 90), Interval(16, 19), Interval(1, 1)],
        [Interval(15, 18), Interval(95, 106), Interval(20, 26), Interval(10, 10), Interval(34, 41), Interval(74, 92), Interval(28, 36), Interval(62, 72), Interval(33, 42), Interval(25, 26), Interval(85, 100), Interval(29, 33), Interval(50, 59), Interval(41, 50), Interval(43, 53)],
        [Interval(14, 16), Interval(20, 23), Interval(85, 103), Interval(2, 2), Interval(18, 24), Interval(75, 83), Interval(91, 114), Interval(81, 96), Interval(53, 56), Interval(59, 75), Interval(6, 7), Interval(13, 16), Interval(83, 105), Interval(86, 93), Interval(43, 51)],
        [Interval(8, 9), Interval(56, 62), Interval(67, 81), Interval(16, 17), Interval(95, 106), Interval(32, 37), Interval(14, 17), Interval(45, 48), Interval(21, 23), Interval(76, 96), Interval(63, 79), Interval(28, 32), Interval(72, 85), Interval(10, 12), Interval(47, 57)],
        [Interval(52, 64), Interval(84, 103), Interval(53, 63), Interval(26, 28), Interval(81, 97), Interval(6, 6), Interval(97, 108), Interval(50, 58), Interval(27, 34), Interval(63, 70), Interval(92, 105), Interval(52, 57), Interval(83, 103), Interval(68, 78), Interval(45, 52)],
        [Interval(43, 52), Interval(18, 22), Interval(31, 36), Interval(34, 39), Interval(18, 20), Interval(58, 63), Interval(96, 109), Interval(13, 14), Interval(47, 50), Interval(35, 39), Interval(78, 83), Interval(13, 15), Interval(66, 81), Interval(15, 19), Interval(22, 25)],
        [Interval(12, 14), Interval(66, 80), Interval(35, 41), Interval(71, 78), Interval(89, 106), Interval(65, 73), Interval(28, 31), Interval(12, 16), Interval(17, 19), Interval(66, 77), Interval(47, 60), Interval(50, 64), Interval(50, 62), Interval(60, 66), Interval(10, 11)],
        [Interval(75, 79), Interval(75, 93), Interval(73, 87), Interval(40, 48), Interval(55, 68), Interval(22, 28), Interval(6, 7), Interval(31, 33), Interval(5, 5), Interval(15, 20), Interval(70, 79), Interval(39, 51), Interval(46, 48), Interval(64, 73), Interval(37, 39)],
        [Interval(93, 111), Interval(57, 64), Interval(56, 63), Interval(91, 114), Interval(20, 22), Interval(88, 102), Interval(13, 14), Interval(78, 102), Interval(6, 7), Interval(61, 73), Interval(50, 57), Interval(43, 48), Interval(4, 4), Interval(28, 35), Interval(20, 23)],
        [Interval(96, 102), Interval(63, 72), Interval(61, 63), Interval(60, 70), Interval(70, 74), Interval(9, 11), Interval(10, 11), Interval(91, 103), Interval(90, 113), Interval(75, 83), Interval(45, 55), Interval(39, 46), Interval(24, 29), Interval(93, 97), Interval(56, 61)],
        [Interval(32, 35), Interval(17, 18), Interval(92, 109), Interval(77, 81), Interval(84, 99), Interval(3, 3), Interval(69, 85), Interval(17, 22), Interval(29, 36), Interval(32, 38), Interval(89, 115), Interval(10, 10), Interval(83, 92), Interval(55, 67), Interval(44, 50)],
        [Interval(67, 79), Interval(81, 98), Interval(59, 76), Interval(76, 77), Interval(40, 48), Interval(13, 14), Interval(8, 9), Interval(84, 99), Interval(3, 3), Interval(65, 74), Interval(39, 48), Interval(11, 13), Interval(31, 38), Interval(69, 80), Interval(85, 104)],
        [Interval(20, 22), Interval(74, 87), Interval(74, 95), Interval(74, 85), Interval(59, 76), Interval(78, 98), Interval(75, 92), Interval(40, 43), Interval(6, 7), Interval(85, 99), Interval(51, 53), Interval(49, 56), Interval(28, 32), Interval(62, 73), Interval(18, 22)],
        [Interval(86, 93), Interval(16, 17), Interval(96, 112), Interval(26, 30), Interval(57, 69), Interval(59, 65), Interval(69, 77), Interval(93, 111), Interval(81, 102), Interval(78, 88), Interval(94, 109), Interval(86, 110), Interval(10, 11), Interval(8, 9), Interval(41, 49)],
        [Interval(24, 26), Interval(16, 19), Interval(19, 20), Interval(64, 83), Interval(83, 102), Interval(73, 91), Interval(48, 51), Interval(43, 46), Interval(94, 111), Interval(27, 34), Interval(66, 74), Interval(33, 37), Interval(24, 30), Interval(93, 106), Interval(19, 23)],
    ],
}
