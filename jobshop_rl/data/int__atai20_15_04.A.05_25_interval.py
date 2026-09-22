"""aTA 20x15 #04 con intervalos asimetricos (protocolo A.05_25).

Generado por scripts/e4_genera_asimetricas.py a partir de la version
simetrica: el valor crisp es el punto medio de aquella, y sobre el se
sortea p_lo = p - round(p*U[0,0.05]) y p_up = p + round(p*U[0,0.25]).
Las rutas de maquina son las mismas.
"""

from jobshop_rl.models.interval import Interval


INT__ATAI20_15_04_A_05_25_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__atai20_15_04',
    'name': 'aTA 20x15 #04',
    'has_intervals': True,
    'description': 'aTA 20x15 #04 asimetrica A.05_25',
    'sequences': [[8, 13, 3, 7, 10, 6, 14, 12, 9, 2, 0, 4, 5, 11, 1], [11, 4, 6, 3, 8, 9, 12, 5, 13, 0, 7, 10, 14, 2, 1], [14, 9, 4, 0, 2, 13, 6, 7, 11, 1, 3, 5, 10, 12, 8], [0, 12, 10, 1, 11, 14, 8, 5, 9, 13, 2, 6, 3, 4, 7], [2, 6, 4, 13, 8, 12, 3, 10, 9, 11, 0, 7, 1, 5, 14], [1, 4, 13, 7, 12, 8, 3, 0, 14, 5, 10, 11, 9, 6, 2], [6, 12, 3, 11, 0, 1, 7, 13, 4, 8, 5, 9, 14, 10, 2], [5, 7, 14, 11, 4, 3, 10, 0, 1, 6, 13, 12, 8, 9, 2], [3, 2, 6, 4, 11, 10, 0, 8, 14, 7, 13, 5, 1, 9, 12], [3, 11, 14, 10, 2, 4, 1, 13, 6, 9, 5, 8, 12, 7, 0], [9, 10, 6, 7, 4, 12, 5, 14, 13, 1, 8, 0, 2, 3, 11], [7, 5, 11, 14, 8, 0, 13, 12, 2, 9, 10, 1, 4, 3, 6], [11, 0, 6, 12, 5, 10, 13, 3, 4, 1, 9, 14, 2, 8, 7], [2, 9, 4, 6, 3, 7, 13, 5, 12, 10, 1, 11, 8, 14, 0], [6, 14, 5, 8, 13, 4, 1, 3, 0, 7, 12, 2, 10, 11, 9], [10, 14, 8, 7, 6, 5, 1, 13, 11, 2, 3, 9, 12, 0, 4], [5, 11, 1, 4, 7, 6, 14, 13, 8, 12, 3, 2, 0, 9, 10], [4, 14, 2, 6, 0, 11, 7, 13, 9, 1, 5, 3, 8, 10, 12], [7, 14, 10, 1, 5, 9, 2, 4, 0, 11, 13, 3, 6, 12, 8], [11, 13, 7, 8, 6, 0, 5, 4, 10, 1, 3, 2, 9, 12, 14]],
    'durations': [
        [Interval(54, 64), Interval(25, 27), Interval(16, 21), Interval(62, 66), Interval(9, 9), Interval(30, 35), Interval(72, 78), Interval(21, 26), Interval(42, 45), Interval(81, 89), Interval(68, 70), Interval(86, 95), Interval(85, 92), Interval(20, 23), Interval(30, 36)],
        [Interval(38, 49), Interval(19, 24), Interval(35, 37), Interval(77, 87), Interval(34, 42), Interval(65, 72), Interval(15, 15), Interval(55, 66), Interval(58, 68), Interval(71, 80), Interval(50, 65), Interval(13, 16), Interval(2, 2), Interval(15, 16), Interval(57, 67)],
        [Interval(5, 6), Interval(31, 37), Interval(54, 62), Interval(67, 78), Interval(47, 58), Interval(70, 80), Interval(91, 112), Interval(40, 44), Interval(13, 14), Interval(14, 15), Interval(49, 53), Interval(29, 30), Interval(48, 57), Interval(75, 88), Interval(80, 81)],
        [Interval(61, 78), Interval(63, 74), Interval(21, 22), Interval(21, 26), Interval(29, 33), Interval(10, 10), Interval(24, 25), Interval(60, 62), Interval(90, 94), Interval(24, 29), Interval(48, 50), Interval(51, 63), Interval(8, 9), Interval(29, 36), Interval(36, 43)],
        [Interval(4, 4), Interval(32, 35), Interval(10, 12), Interval(76, 95), Interval(44, 53), Interval(36, 43), Interval(87, 103), Interval(59, 70), Interval(58, 66), Interval(41, 50), Interval(47, 55), Interval(30, 32), Interval(21, 22), Interval(22, 24), Interval(15, 18)],
        [Interval(14, 17), Interval(10, 11), Interval(68, 73), Interval(91, 96), Interval(41, 42), Interval(28, 34), Interval(42, 47), Interval(22, 26), Interval(59, 63), Interval(56, 63), Interval(44, 49), Interval(93, 102), Interval(30, 35), Interval(26, 28), Interval(13, 13)],
        [Interval(50, 62), Interval(54, 64), Interval(23, 23), Interval(25, 28), Interval(49, 55), Interval(53, 60), Interval(9, 9), Interval(85, 108), Interval(20, 25), Interval(46, 55), Interval(53, 66), Interval(22, 24), Interval(46, 47), Interval(49, 60), Interval(86, 95)],
        [Interval(11, 13), Interval(41, 44), Interval(26, 27), Interval(30, 32), Interval(18, 19), Interval(58, 71), Interval(82, 95), Interval(33, 40), Interval(73, 75), Interval(19, 23), Interval(34, 40), Interval(91, 109), Interval(65, 81), Interval(83, 93), Interval(37, 41)],
        [Interval(9, 11), Interval(19, 24), Interval(11, 11), Interval(20, 24), Interval(11, 11), Interval(95, 104), Interval(92, 99), Interval(87, 110), Interval(92, 103), Interval(97, 121), Interval(28, 34), Interval(53, 66), Interval(85, 107), Interval(32, 42), Interval(60, 73)],
        [Interval(10, 12), Interval(56, 71), Interval(84, 95), Interval(83, 100), Interval(83, 108), Interval(18, 22), Interval(71, 87), Interval(64, 75), Interval(12, 14), Interval(22, 25), Interval(78, 98), Interval(5, 6), Interval(92, 115), Interval(6, 7), Interval(34, 36)],
        [Interval(45, 54), Interval(65, 75), Interval(58, 64), Interval(19, 23), Interval(14, 17), Interval(6, 6), Interval(20, 23), Interval(6, 6), Interval(46, 56), Interval(76, 86), Interval(31, 39), Interval(79, 98), Interval(7, 8), Interval(73, 92), Interval(52, 66)],
        [Interval(19, 22), Interval(96, 123), Interval(54, 63), Interval(75, 90), Interval(34, 37), Interval(26, 29), Interval(23, 25), Interval(85, 104), Interval(86, 102), Interval(25, 29), Interval(93, 122), Interval(1, 1), Interval(16, 17), Interval(32, 40), Interval(48, 55)],
        [Interval(33, 35), Interval(32, 38), Interval(64, 67), Interval(46, 52), Interval(46, 52), Interval(51, 53), Interval(32, 41), Interval(76, 92), Interval(38, 43), Interval(63, 81), Interval(58, 67), Interval(71, 79), Interval(14, 15), Interval(83, 89), Interval(13, 15)],
        [Interval(85, 104), Interval(82, 95), Interval(15, 17), Interval(66, 68), Interval(31, 33), Interval(82, 102), Interval(80, 81), Interval(79, 90), Interval(10, 11), Interval(12, 12), Interval(30, 33), Interval(37, 43), Interval(75, 85), Interval(43, 52), Interval(18, 19)],
        [Interval(59, 67), Interval(57, 59), Interval(16, 18), Interval(24, 27), Interval(54, 68), Interval(8, 8), Interval(41, 51), Interval(38, 41), Interval(28, 34), Interval(54, 64), Interval(36, 38), Interval(33, 42), Interval(39, 44), Interval(66, 73), Interval(51, 56)],
        [Interval(76, 88), Interval(86, 101), Interval(88, 96), Interval(12, 15), Interval(4, 5), Interval(31, 37), Interval(57, 61), Interval(60, 74), Interval(81, 99), Interval(47, 57), Interval(40, 42), Interval(35, 38), Interval(66, 73), Interval(27, 35), Interval(12, 12)],
        [Interval(1, 1), Interval(65, 76), Interval(93, 113), Interval(41, 48), Interval(83, 102), Interval(33, 36), Interval(82, 98), Interval(74, 84), Interval(92, 94), Interval(79, 83), Interval(64, 69), Interval(90, 94), Interval(46, 48), Interval(56, 65), Interval(61, 67)],
        [Interval(59, 73), Interval(49, 55), Interval(34, 37), Interval(89, 109), Interval(80, 99), Interval(55, 65), Interval(30, 34), Interval(49, 56), Interval(52, 54), Interval(11, 12), Interval(71, 81), Interval(8, 8), Interval(13, 14), Interval(12, 15), Interval(48, 57)],
        [Interval(19, 22), Interval(87, 100), Interval(65, 80), Interval(10, 11), Interval(74, 91), Interval(47, 57), Interval(72, 78), Interval(66, 68), Interval(37, 38), Interval(76, 96), Interval(92, 98), Interval(59, 74), Interval(37, 42), Interval(50, 52), Interval(58, 63)],
        [Interval(29, 35), Interval(71, 80), Interval(59, 75), Interval(19, 20), Interval(95, 117), Interval(94, 110), Interval(2, 2), Interval(39, 45), Interval(69, 85), Interval(88, 94), Interval(10, 12), Interval(59, 67), Interval(20, 24), Interval(39, 41), Interval(16, 20)],
    ],
}
