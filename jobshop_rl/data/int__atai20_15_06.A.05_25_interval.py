"""aTA 20x15 #06 con intervalos asimetricos (protocolo A.05_25).

Generado por scripts/e4_genera_asimetricas.py a partir de la version
simetrica: el valor crisp es el punto medio de aquella, y sobre el se
sortea p_lo = p - round(p*U[0,0.05]) y p_up = p + round(p*U[0,0.25]).
Las rutas de maquina son las mismas.
"""

from jobshop_rl.models.interval import Interval


INT__ATAI20_15_06_A_05_25_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__atai20_15_06',
    'name': 'aTA 20x15 #06',
    'has_intervals': True,
    'description': 'aTA 20x15 #06 asimetrica A.05_25',
    'sequences': [[2, 11, 0, 13, 1, 8, 9, 6, 4, 7, 12, 3, 14, 5, 10], [5, 8, 9, 3, 1, 13, 11, 0, 14, 7, 4, 12, 10, 6, 2], [5, 2, 8, 14, 13, 1, 6, 9, 12, 4, 11, 0, 7, 3, 10], [8, 10, 4, 0, 3, 11, 13, 6, 1, 5, 2, 9, 12, 14, 7], [8, 11, 1, 0, 5, 13, 2, 14, 10, 12, 9, 3, 4, 6, 7], [11, 3, 13, 9, 14, 1, 0, 7, 4, 5, 10, 12, 6, 2, 8], [13, 3, 11, 10, 5, 12, 0, 4, 14, 6, 7, 8, 9, 2, 1], [5, 8, 6, 7, 2, 3, 10, 4, 1, 14, 11, 9, 13, 0, 12], [12, 8, 9, 7, 3, 6, 11, 13, 10, 0, 2, 5, 1, 4, 14], [5, 14, 11, 4, 10, 8, 9, 2, 13, 12, 7, 1, 0, 3, 6], [10, 9, 1, 12, 2, 7, 3, 4, 0, 5, 6, 8, 13, 14, 11], [9, 7, 5, 6, 0, 14, 1, 3, 8, 11, 2, 12, 10, 13, 4], [2, 13, 12, 3, 9, 1, 5, 10, 11, 6, 0, 7, 8, 14, 4], [3, 0, 9, 13, 8, 2, 6, 1, 10, 12, 7, 14, 4, 5, 11], [6, 5, 0, 13, 8, 14, 2, 7, 12, 4, 10, 3, 1, 9, 11], [6, 8, 0, 7, 4, 1, 11, 10, 13, 14, 12, 2, 9, 3, 5], [13, 2, 1, 8, 3, 12, 6, 14, 11, 9, 5, 7, 4, 10, 0], [13, 7, 5, 11, 4, 6, 10, 14, 2, 9, 0, 3, 8, 12, 1], [9, 2, 10, 11, 7, 1, 14, 3, 6, 8, 5, 4, 12, 0, 13], [13, 4, 11, 12, 7, 0, 5, 1, 8, 14, 9, 2, 3, 10, 6]],
    'durations': [
        [Interval(73, 90), Interval(17, 18), Interval(57, 68), Interval(26, 28), Interval(87, 92), Interval(77, 79), Interval(62, 65), Interval(85, 105), Interval(72, 85), Interval(33, 36), Interval(57, 70), Interval(90, 97), Interval(63, 76), Interval(66, 81), Interval(27, 33)],
        [Interval(5, 6), Interval(77, 97), Interval(69, 88), Interval(41, 52), Interval(69, 72), Interval(20, 24), Interval(85, 93), Interval(85, 105), Interval(46, 55), Interval(61, 69), Interval(35, 42), Interval(84, 97), Interval(47, 56), Interval(97, 116), Interval(23, 24)],
        [Interval(2, 2), Interval(65, 80), Interval(27, 32), Interval(97, 115), Interval(63, 80), Interval(40, 50), Interval(46, 57), Interval(22, 24), Interval(90, 106), Interval(25, 27), Interval(87, 98), Interval(3, 3), Interval(37, 40), Interval(72, 76), Interval(74, 79)],
        [Interval(92, 116), Interval(79, 90), Interval(19, 21), Interval(35, 39), Interval(85, 97), Interval(6, 7), Interval(9, 9), Interval(18, 19), Interval(31, 34), Interval(37, 44), Interval(55, 61), Interval(3, 3), Interval(15, 18), Interval(11, 14), Interval(43, 51)],
        [Interval(70, 78), Interval(70, 77), Interval(16, 17), Interval(40, 47), Interval(70, 73), Interval(87, 94), Interval(41, 45), Interval(56, 68), Interval(37, 42), Interval(21, 22), Interval(21, 24), Interval(77, 79), Interval(64, 70), Interval(44, 52), Interval(50, 64)],
        [Interval(19, 22), Interval(12, 14), Interval(84, 102), Interval(22, 25), Interval(40, 50), Interval(28, 30), Interval(6, 7), Interval(4, 4), Interval(76, 99), Interval(74, 92), Interval(20, 25), Interval(26, 29), Interval(16, 18), Interval(54, 61), Interval(59, 63)],
        [Interval(93, 108), Interval(38, 40), Interval(79, 101), Interval(14, 18), Interval(21, 27), Interval(29, 33), Interval(63, 70), Interval(92, 99), Interval(65, 72), Interval(59, 63), Interval(37, 39), Interval(10, 12), Interval(46, 56), Interval(67, 72), Interval(73, 86)],
        [Interval(27, 30), Interval(3, 4), Interval(69, 72), Interval(57, 67), Interval(90, 111), Interval(57, 60), Interval(97, 102), Interval(74, 82), Interval(9, 10), Interval(55, 60), Interval(20, 23), Interval(71, 86), Interval(19, 20), Interval(71, 92), Interval(19, 22)],
        [Interval(7, 8), Interval(36, 40), Interval(62, 65), Interval(69, 83), Interval(13, 15), Interval(56, 66), Interval(52, 56), Interval(57, 70), Interval(2, 2), Interval(91, 115), Interval(87, 97), Interval(6, 7), Interval(63, 74), Interval(75, 84), Interval(60, 73)],
        [Interval(82, 105), Interval(44, 52), Interval(74, 78), Interval(34, 36), Interval(32, 39), Interval(92, 117), Interval(49, 62), Interval(19, 21), Interval(4, 4), Interval(28, 33), Interval(59, 64), Interval(70, 81), Interval(87, 112), Interval(50, 56), Interval(64, 81)],
        [Interval(86, 110), Interval(11, 14), Interval(34, 43), Interval(83, 105), Interval(14, 14), Interval(82, 104), Interval(12, 14), Interval(20, 25), Interval(23, 28), Interval(35, 44), Interval(12, 14), Interval(88, 105), Interval(96, 100), Interval(33, 41), Interval(75, 89)],
        [Interval(30, 32), Interval(85, 90), Interval(88, 102), Interval(3, 3), Interval(97, 115), Interval(70, 73), Interval(71, 81), Interval(16, 20), Interval(14, 15), Interval(94, 119), Interval(71, 72), Interval(19, 23), Interval(64, 76), Interval(87, 103), Interval(2, 2)],
        [Interval(61, 71), Interval(84, 95), Interval(71, 86), Interval(74, 89), Interval(84, 92), Interval(31, 37), Interval(31, 32), Interval(48, 52), Interval(25, 29), Interval(80, 93), Interval(76, 83), Interval(33, 34), Interval(58, 70), Interval(73, 86), Interval(76, 91)],
        [Interval(9, 10), Interval(58, 74), Interval(90, 111), Interval(68, 74), Interval(38, 46), Interval(62, 66), Interval(93, 106), Interval(66, 76), Interval(73, 87), Interval(40, 42), Interval(58, 62), Interval(67, 71), Interval(11, 11), Interval(23, 28), Interval(25, 27)],
        [Interval(84, 87), Interval(77, 87), Interval(20, 25), Interval(50, 51), Interval(69, 80), Interval(66, 70), Interval(89, 109), Interval(69, 72), Interval(64, 75), Interval(50, 60), Interval(43, 55), Interval(5, 6), Interval(70, 86), Interval(66, 70), Interval(25, 27)],
        [Interval(36, 46), Interval(26, 31), Interval(22, 27), Interval(25, 30), Interval(2, 2), Interval(35, 41), Interval(20, 22), Interval(62, 67), Interval(59, 63), Interval(26, 28), Interval(34, 36), Interval(49, 51), Interval(43, 47), Interval(79, 94), Interval(19, 23)],
        [Interval(5, 6), Interval(56, 67), Interval(67, 75), Interval(91, 103), Interval(44, 50), Interval(36, 39), Interval(88, 91), Interval(42, 45), Interval(48, 59), Interval(22, 28), Interval(62, 67), Interval(76, 93), Interval(47, 48), Interval(86, 102), Interval(7, 8)],
        [Interval(28, 29), Interval(61, 67), Interval(23, 23), Interval(42, 51), Interval(31, 39), Interval(63, 70), Interval(89, 109), Interval(78, 82), Interval(48, 50), Interval(3, 3), Interval(82, 101), Interval(19, 22), Interval(60, 75), Interval(74, 83), Interval(84, 97)],
        [Interval(65, 79), Interval(46, 53), Interval(47, 50), Interval(55, 59), Interval(84, 104), Interval(61, 74), Interval(47, 60), Interval(69, 82), Interval(83, 100), Interval(89, 100), Interval(1, 1), Interval(63, 65), Interval(83, 89), Interval(29, 34), Interval(86, 111)],
        [Interval(79, 88), Interval(14, 16), Interval(40, 42), Interval(71, 79), Interval(21, 26), Interval(90, 97), Interval(6, 7), Interval(78, 101), Interval(18, 20), Interval(60, 70), Interval(62, 65), Interval(82, 97), Interval(24, 28), Interval(68, 79), Interval(10, 10)],
    ],
}
