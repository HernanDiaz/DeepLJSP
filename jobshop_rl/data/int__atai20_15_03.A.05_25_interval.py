"""aTA 20x15 #03 con intervalos asimetricos (protocolo A.05_25).

Generado por scripts/e4_genera_asimetricas.py a partir de la version
simetrica: el valor crisp es el punto medio de aquella, y sobre el se
sortea p_lo = p - round(p*U[0,0.05]) y p_up = p + round(p*U[0,0.25]).
Las rutas de maquina son las mismas.
"""

from jobshop_rl.models.interval import Interval


INT__ATAI20_15_03_A_05_25_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__atai20_15_03',
    'name': 'aTA 20x15 #03',
    'has_intervals': True,
    'description': 'aTA 20x15 #03 asimetrica A.05_25',
    'sequences': [[12, 11, 8, 9, 7, 13, 0, 10, 2, 4, 5, 6, 3, 14, 1], [2, 5, 0, 10, 4, 1, 13, 11, 3, 14, 6, 8, 9, 12, 7], [3, 2, 6, 9, 5, 12, 0, 13, 7, 10, 14, 1, 4, 8, 11], [9, 14, 5, 7, 13, 10, 12, 2, 3, 8, 1, 6, 11, 0, 4], [3, 8, 6, 1, 13, 0, 9, 5, 14, 2, 12, 7, 4, 11, 10], [3, 8, 13, 11, 12, 1, 4, 14, 6, 5, 9, 0, 7, 10, 2], [11, 2, 0, 6, 4, 1, 5, 12, 9, 7, 3, 8, 13, 10, 14], [12, 3, 4, 11, 8, 1, 5, 0, 13, 6, 10, 9, 2, 14, 7], [5, 8, 7, 0, 12, 13, 1, 6, 4, 14, 10, 9, 3, 2, 11], [6, 3, 9, 8, 2, 1, 12, 7, 5, 14, 0, 4, 11, 13, 10], [6, 0, 4, 14, 8, 13, 12, 11, 10, 1, 9, 7, 5, 3, 2], [0, 6, 4, 3, 8, 2, 11, 1, 9, 5, 13, 12, 10, 14, 7], [2, 9, 5, 12, 3, 14, 4, 13, 11, 7, 1, 10, 8, 6, 0], [11, 7, 10, 4, 8, 14, 6, 3, 9, 5, 1, 13, 2, 12, 0], [8, 13, 10, 12, 0, 9, 2, 6, 11, 1, 3, 14, 5, 7, 4], [14, 7, 11, 6, 10, 9, 2, 0, 1, 12, 8, 3, 4, 13, 5], [8, 13, 7, 9, 11, 12, 5, 4, 2, 3, 14, 6, 0, 10, 1], [8, 14, 5, 11, 1, 0, 7, 3, 12, 2, 9, 10, 13, 6, 4], [8, 6, 1, 11, 7, 12, 14, 10, 0, 9, 3, 4, 5, 13, 2], [13, 1, 4, 0, 5, 7, 3, 6, 12, 8, 11, 2, 10, 14, 9]],
    'durations': [
        [Interval(88, 106), Interval(16, 21), Interval(4, 4), Interval(61, 79), Interval(65, 74), Interval(29, 32), Interval(84, 108), Interval(78, 81), Interval(91, 102), Interval(14, 15), Interval(16, 21), Interval(22, 26), Interval(1, 1), Interval(82, 102), Interval(41, 45)],
        [Interval(74, 83), Interval(75, 92), Interval(9, 11), Interval(75, 83), Interval(24, 24), Interval(8, 10), Interval(62, 68), Interval(6, 6), Interval(12, 13), Interval(13, 13), Interval(71, 79), Interval(75, 86), Interval(94, 101), Interval(8, 9), Interval(6, 7)],
        [Interval(89, 102), Interval(3, 3), Interval(12, 13), Interval(27, 33), Interval(56, 65), Interval(63, 76), Interval(97, 121), Interval(31, 37), Interval(7, 7), Interval(76, 93), Interval(95, 108), Interval(29, 37), Interval(53, 56), Interval(22, 23), Interval(85, 90)],
        [Interval(19, 21), Interval(43, 51), Interval(65, 81), Interval(23, 24), Interval(30, 34), Interval(30, 30), Interval(47, 51), Interval(31, 33), Interval(75, 84), Interval(30, 35), Interval(3, 3), Interval(25, 27), Interval(9, 10), Interval(2, 2), Interval(21, 23)],
        [Interval(82, 87), Interval(60, 68), Interval(35, 38), Interval(42, 48), Interval(36, 40), Interval(15, 18), Interval(95, 112), Interval(83, 88), Interval(49, 60), Interval(26, 28), Interval(12, 14), Interval(74, 82), Interval(40, 46), Interval(2, 2), Interval(94, 101)],
        [Interval(82, 85), Interval(53, 62), Interval(2, 2), Interval(64, 73), Interval(50, 62), Interval(95, 121), Interval(77, 97), Interval(8, 8), Interval(22, 24), Interval(58, 66), Interval(91, 115), Interval(51, 61), Interval(83, 99), Interval(64, 67), Interval(13, 15)],
        [Interval(62, 67), Interval(92, 108), Interval(4, 5), Interval(12, 15), Interval(95, 115), Interval(25, 30), Interval(31, 37), Interval(19, 24), Interval(93, 101), Interval(27, 31), Interval(61, 75), Interval(2, 2), Interval(22, 23), Interval(14, 17), Interval(61, 67)],
        [Interval(55, 61), Interval(95, 101), Interval(54, 65), Interval(27, 28), Interval(1, 1), Interval(95, 115), Interval(27, 30), Interval(38, 41), Interval(40, 47), Interval(89, 97), Interval(76, 86), Interval(62, 72), Interval(62, 64), Interval(79, 89), Interval(6, 7)],
        [Interval(61, 70), Interval(98, 114), Interval(63, 73), Interval(36, 40), Interval(87, 92), Interval(94, 96), Interval(85, 106), Interval(13, 15), Interval(70, 74), Interval(27, 31), Interval(56, 62), Interval(97, 117), Interval(11, 11), Interval(8, 9), Interval(92, 112)],
        [Interval(17, 20), Interval(68, 82), Interval(77, 88), Interval(32, 36), Interval(83, 104), Interval(80, 86), Interval(44, 49), Interval(14, 16), Interval(84, 103), Interval(2, 2), Interval(59, 73), Interval(72, 82), Interval(27, 32), Interval(63, 65), Interval(65, 72)],
        [Interval(46, 51), Interval(42, 49), Interval(60, 69), Interval(17, 18), Interval(64, 75), Interval(5, 6), Interval(93, 101), Interval(46, 51), Interval(9, 11), Interval(19, 22), Interval(10, 11), Interval(11, 13), Interval(84, 95), Interval(90, 96), Interval(63, 75)],
        [Interval(65, 70), Interval(89, 94), Interval(8, 8), Interval(35, 38), Interval(97, 109), Interval(87, 100), Interval(16, 16), Interval(85, 109), Interval(17, 17), Interval(98, 108), Interval(85, 88), Interval(8, 10), Interval(39, 49), Interval(33, 37), Interval(36, 39)],
        [Interval(97, 111), Interval(2, 2), Interval(21, 22), Interval(12, 14), Interval(13, 14), Interval(60, 72), Interval(29, 32), Interval(43, 51), Interval(25, 27), Interval(53, 69), Interval(10, 12), Interval(44, 44), Interval(25, 27), Interval(38, 45), Interval(63, 67)],
        [Interval(34, 39), Interval(59, 73), Interval(51, 60), Interval(81, 104), Interval(30, 33), Interval(2, 2), Interval(49, 52), Interval(68, 77), Interval(63, 79), Interval(53, 64), Interval(44, 52), Interval(36, 38), Interval(86, 98), Interval(67, 71), Interval(36, 44)],
        [Interval(70, 78), Interval(39, 44), Interval(16, 17), Interval(20, 22), Interval(50, 50), Interval(10, 11), Interval(45, 46), Interval(2, 2), Interval(47, 54), Interval(16, 18), Interval(56, 71), Interval(35, 41), Interval(12, 14), Interval(29, 34), Interval(78, 102)],
        [Interval(74, 90), Interval(40, 43), Interval(21, 26), Interval(88, 93), Interval(46, 51), Interval(6, 6), Interval(87, 95), Interval(74, 82), Interval(76, 92), Interval(49, 53), Interval(49, 55), Interval(79, 87), Interval(69, 85), Interval(65, 68), Interval(19, 21)],
        [Interval(47, 59), Interval(5, 6), Interval(57, 70), Interval(40, 49), Interval(72, 82), Interval(69, 84), Interval(82, 86), Interval(47, 50), Interval(24, 26), Interval(82, 94), Interval(75, 83), Interval(25, 31), Interval(51, 63), Interval(31, 34), Interval(15, 17)],
        [Interval(11, 12), Interval(18, 22), Interval(6, 7), Interval(57, 67), Interval(82, 85), Interval(61, 79), Interval(83, 91), Interval(21, 26), Interval(50, 63), Interval(49, 60), Interval(29, 32), Interval(54, 60), Interval(30, 35), Interval(24, 27), Interval(31, 38)],
        [Interval(79, 96), Interval(40, 52), Interval(11, 11), Interval(62, 64), Interval(43, 54), Interval(87, 92), Interval(8, 9), Interval(35, 43), Interval(69, 82), Interval(66, 68), Interval(72, 77), Interval(55, 62), Interval(42, 53), Interval(85, 97), Interval(34, 38)],
        [Interval(19, 19), Interval(51, 56), Interval(79, 91), Interval(89, 91), Interval(21, 23), Interval(32, 37), Interval(54, 69), Interval(86, 101), Interval(49, 56), Interval(27, 31), Interval(15, 17), Interval(26, 29), Interval(72, 88), Interval(81, 98), Interval(78, 80)],
    ],
}
