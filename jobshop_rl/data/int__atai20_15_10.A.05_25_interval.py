"""aTA 20x15 #10 con intervalos asimetricos (protocolo A.05_25).

Generado por scripts/e4_genera_asimetricas.py a partir de la version
simetrica: el valor crisp es el punto medio de aquella, y sobre el se
sortea p_lo = p - round(p*U[0,0.05]) y p_up = p + round(p*U[0,0.25]).
Las rutas de maquina son las mismas.
"""

from jobshop_rl.models.interval import Interval


INT__ATAI20_15_10_A_05_25_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__atai20_15_10',
    'name': 'aTA 20x15 #10',
    'has_intervals': True,
    'description': 'aTA 20x15 #10 asimetrica A.05_25',
    'sequences': [[7, 0, 12, 4, 1, 9, 2, 11, 10, 14, 5, 6, 13, 3, 8], [4, 8, 7, 3, 9, 13, 12, 0, 11, 10, 1, 6, 5, 14, 2], [1, 4, 7, 13, 3, 8, 10, 5, 12, 14, 9, 6, 2, 0, 11], [5, 11, 9, 12, 7, 1, 6, 13, 8, 2, 0, 14, 3, 4, 10], [4, 11, 12, 1, 0, 9, 6, 13, 2, 14, 5, 10, 3, 8, 7], [2, 6, 3, 8, 14, 0, 4, 10, 11, 1, 7, 13, 12, 5, 9], [4, 14, 5, 10, 8, 7, 6, 1, 0, 12, 9, 13, 11, 3, 2], [7, 10, 11, 14, 3, 2, 4, 5, 1, 12, 9, 6, 13, 0, 8], [14, 11, 0, 13, 3, 2, 1, 8, 5, 7, 4, 12, 6, 10, 9], [0, 5, 12, 1, 13, 10, 9, 4, 2, 8, 14, 11, 7, 6, 3], [4, 3, 8, 12, 9, 11, 2, 14, 5, 7, 13, 6, 10, 1, 0], [9, 6, 1, 0, 14, 7, 13, 12, 2, 11, 5, 8, 10, 3, 4], [4, 3, 0, 14, 13, 9, 7, 2, 11, 8, 10, 1, 6, 12, 5], [12, 10, 3, 6, 4, 5, 0, 7, 2, 8, 13, 11, 14, 9, 1], [14, 7, 5, 8, 11, 0, 2, 13, 12, 4, 6, 1, 10, 9, 3], [6, 14, 12, 2, 7, 5, 8, 13, 11, 9, 0, 3, 4, 1, 10], [9, 5, 14, 10, 12, 1, 4, 13, 0, 11, 3, 2, 7, 6, 8], [9, 12, 4, 14, 11, 8, 0, 7, 5, 3, 1, 10, 6, 13, 2], [12, 2, 3, 14, 5, 1, 6, 11, 13, 9, 7, 10, 8, 0, 4], [3, 12, 10, 5, 14, 0, 9, 8, 13, 6, 11, 1, 7, 2, 4]],
    'durations': [
        [Interval(81, 87), Interval(57, 59), Interval(70, 81), Interval(26, 30), Interval(96, 113), Interval(35, 40), Interval(12, 15), Interval(29, 31), Interval(87, 97), Interval(90, 111), Interval(45, 45), Interval(27, 32), Interval(70, 80), Interval(73, 85), Interval(44, 52)],
        [Interval(28, 36), Interval(21, 24), Interval(46, 52), Interval(74, 85), Interval(91, 111), Interval(14, 16), Interval(4, 4), Interval(78, 97), Interval(14, 15), Interval(34, 37), Interval(76, 87), Interval(33, 34), Interval(56, 64), Interval(22, 25), Interval(55, 61)],
        [Interval(72, 87), Interval(36, 44), Interval(48, 57), Interval(25, 30), Interval(47, 52), Interval(59, 62), Interval(15, 16), Interval(66, 73), Interval(86, 96), Interval(38, 44), Interval(8, 9), Interval(72, 81), Interval(62, 66), Interval(90, 108), Interval(90, 102)],
        [Interval(1, 1), Interval(35, 43), Interval(22, 23), Interval(93, 99), Interval(74, 89), Interval(49, 51), Interval(39, 43), Interval(58, 75), Interval(40, 47), Interval(7, 7), Interval(55, 66), Interval(69, 83), Interval(38, 45), Interval(75, 77), Interval(7, 8)],
        [Interval(12, 16), Interval(15, 17), Interval(16, 21), Interval(14, 17), Interval(65, 82), Interval(92, 104), Interval(17, 22), Interval(50, 64), Interval(51, 53), Interval(16, 17), Interval(32, 37), Interval(59, 61), Interval(46, 52), Interval(64, 69), Interval(38, 47)],
        [Interval(53, 58), Interval(78, 92), Interval(83, 101), Interval(35, 37), Interval(54, 58), Interval(69, 90), Interval(16, 20), Interval(44, 49), Interval(35, 41), Interval(87, 95), Interval(76, 91), Interval(81, 105), Interval(16, 17), Interval(79, 90), Interval(88, 94)],
        [Interval(4, 4), Interval(59, 72), Interval(32, 36), Interval(60, 73), Interval(84, 94), Interval(29, 36), Interval(39, 41), Interval(67, 69), Interval(42, 52), Interval(30, 34), Interval(79, 85), Interval(38, 42), Interval(67, 75), Interval(64, 82), Interval(30, 35)],
        [Interval(28, 34), Interval(29, 36), Interval(68, 86), Interval(26, 31), Interval(54, 69), Interval(46, 49), Interval(53, 54), Interval(62, 75), Interval(93, 106), Interval(24, 29), Interval(68, 81), Interval(21, 24), Interval(17, 20), Interval(38, 42), Interval(12, 14)],
        [Interval(12, 15), Interval(72, 76), Interval(35, 38), Interval(67, 84), Interval(12, 14), Interval(78, 81), Interval(94, 116), Interval(68, 74), Interval(49, 62), Interval(14, 17), Interval(70, 88), Interval(27, 28), Interval(34, 39), Interval(58, 70), Interval(33, 38)],
        [Interval(59, 68), Interval(48, 51), Interval(71, 80), Interval(87, 112), Interval(58, 72), Interval(84, 100), Interval(3, 4), Interval(59, 64), Interval(58, 74), Interval(93, 95), Interval(87, 103), Interval(34, 36), Interval(25, 32), Interval(4, 5), Interval(26, 28)],
        [Interval(85, 101), Interval(87, 100), Interval(92, 115), Interval(31, 34), Interval(18, 21), Interval(71, 74), Interval(9, 10), Interval(19, 23), Interval(92, 116), Interval(56, 59), Interval(35, 38), Interval(62, 68), Interval(13, 15), Interval(16, 18), Interval(1, 1)],
        [Interval(70, 80), Interval(47, 53), Interval(94, 108), Interval(7, 8), Interval(62, 77), Interval(47, 54), Interval(24, 27), Interval(45, 54), Interval(70, 86), Interval(70, 78), Interval(19, 21), Interval(96, 116), Interval(39, 44), Interval(15, 17), Interval(78, 82)],
        [Interval(44, 52), Interval(9, 11), Interval(94, 120), Interval(59, 66), Interval(73, 85), Interval(78, 96), Interval(68, 78), Interval(19, 20), Interval(85, 107), Interval(15, 18), Interval(22, 28), Interval(46, 55), Interval(31, 33), Interval(6, 7), Interval(69, 71)],
        [Interval(74, 86), Interval(44, 48), Interval(95, 106), Interval(1, 1), Interval(52, 65), Interval(57, 65), Interval(82, 91), Interval(94, 103), Interval(75, 93), Interval(12, 13), Interval(87, 103), Interval(96, 110), Interval(96, 100), Interval(11, 13), Interval(26, 33)],
        [Interval(70, 88), Interval(69, 74), Interval(13, 16), Interval(31, 32), Interval(18, 22), Interval(55, 66), Interval(17, 17), Interval(91, 102), Interval(55, 68), Interval(73, 76), Interval(31, 35), Interval(7, 8), Interval(78, 89), Interval(10, 12), Interval(88, 112)],
        [Interval(39, 47), Interval(85, 107), Interval(11, 13), Interval(79, 85), Interval(7, 8), Interval(77, 87), Interval(23, 29), Interval(9, 10), Interval(56, 65), Interval(41, 44), Interval(67, 68), Interval(26, 29), Interval(19, 24), Interval(19, 23), Interval(67, 77)],
        [Interval(74, 95), Interval(87, 89), Interval(64, 77), Interval(14, 15), Interval(11, 11), Interval(14, 14), Interval(98, 120), Interval(81, 99), Interval(77, 91), Interval(3, 3), Interval(44, 55), Interval(47, 57), Interval(39, 46), Interval(81, 93), Interval(27, 27)],
        [Interval(55, 56), Interval(69, 74), Interval(5, 6), Interval(83, 86), Interval(16, 19), Interval(4, 5), Interval(19, 22), Interval(14, 17), Interval(60, 75), Interval(8, 9), Interval(89, 96), Interval(32, 38), Interval(60, 74), Interval(68, 76), Interval(28, 33)],
        [Interval(89, 105), Interval(24, 29), Interval(8, 9), Interval(84, 94), Interval(22, 27), Interval(78, 84), Interval(22, 24), Interval(96, 110), Interval(24, 29), Interval(93, 104), Interval(94, 116), Interval(17, 20), Interval(46, 54), Interval(65, 75), Interval(46, 51)],
        [Interval(5, 6), Interval(76, 93), Interval(74, 92), Interval(59, 62), Interval(12, 14), Interval(55, 67), Interval(61, 68), Interval(36, 41), Interval(53, 57), Interval(68, 84), Interval(76, 84), Interval(35, 36), Interval(86, 90), Interval(47, 50), Interval(94, 99)],
    ],
}
