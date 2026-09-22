"""aTA 20x15 #05 con intervalos asimetricos (protocolo A.05_25).

Generado por scripts/e4_genera_asimetricas.py a partir de la version
simetrica: el valor crisp es el punto medio de aquella, y sobre el se
sortea p_lo = p - round(p*U[0,0.05]) y p_up = p + round(p*U[0,0.25]).
Las rutas de maquina son las mismas.
"""

from jobshop_rl.models.interval import Interval


INT__ATAI20_15_05_A_05_25_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__atai20_15_05',
    'name': 'aTA 20x15 #05',
    'has_intervals': True,
    'description': 'aTA 20x15 #05 asimetrica A.05_25',
    'sequences': [[7, 12, 6, 3, 8, 5, 0, 9, 1, 10, 2, 4, 13, 14, 11], [8, 3, 12, 5, 6, 9, 1, 14, 4, 2, 11, 0, 10, 13, 7], [1, 0, 8, 4, 11, 14, 12, 6, 13, 9, 2, 5, 7, 10, 3], [11, 13, 10, 0, 4, 7, 14, 5, 3, 2, 9, 1, 12, 8, 6], [14, 6, 2, 10, 11, 5, 12, 9, 3, 1, 13, 4, 0, 7, 8], [7, 5, 12, 13, 9, 11, 1, 4, 3, 6, 2, 8, 0, 14, 10], [14, 13, 8, 9, 1, 0, 11, 4, 2, 3, 10, 6, 7, 12, 5], [7, 13, 4, 11, 0, 10, 5, 2, 6, 1, 8, 12, 3, 9, 14], [5, 11, 4, 1, 12, 14, 13, 7, 8, 6, 9, 2, 0, 3, 10], [9, 4, 3, 8, 14, 5, 6, 13, 11, 10, 12, 7, 1, 2, 0], [11, 13, 6, 5, 10, 3, 12, 8, 2, 4, 9, 1, 0, 14, 7], [11, 1, 4, 7, 12, 3, 5, 10, 14, 2, 13, 0, 6, 9, 8], [1, 5, 7, 12, 13, 6, 11, 4, 8, 3, 14, 10, 0, 9, 2], [4, 10, 7, 8, 3, 13, 0, 14, 11, 12, 9, 6, 1, 2, 5], [8, 4, 11, 13, 1, 9, 0, 6, 12, 5, 2, 10, 3, 7, 14], [13, 8, 10, 5, 6, 14, 11, 7, 12, 0, 1, 4, 9, 2, 3], [5, 8, 13, 11, 9, 14, 10, 1, 12, 6, 4, 7, 3, 0, 2], [2, 9, 4, 0, 5, 7, 8, 10, 12, 11, 3, 13, 6, 1, 14], [1, 4, 8, 10, 6, 11, 9, 5, 13, 0, 7, 12, 3, 14, 2], [1, 10, 13, 12, 5, 4, 6, 14, 11, 7, 8, 2, 9, 0, 3]],
    'durations': [
        [Interval(15, 15), Interval(85, 95), Interval(49, 56), Interval(95, 116), Interval(40, 42), Interval(78, 91), Interval(43, 49), Interval(57, 67), Interval(85, 101), Interval(87, 93), Interval(47, 52), Interval(43, 44), Interval(41, 51), Interval(11, 13), Interval(73, 90)],
        [Interval(6, 6), Interval(44, 54), Interval(17, 20), Interval(4, 4), Interval(56, 68), Interval(43, 54), Interval(14, 19), Interval(40, 46), Interval(43, 51), Interval(76, 94), Interval(1, 1), Interval(32, 33), Interval(5, 6), Interval(90, 113), Interval(74, 82)],
        [Interval(77, 97), Interval(44, 46), Interval(59, 68), Interval(49, 60), Interval(25, 31), Interval(35, 41), Interval(89, 117), Interval(78, 92), Interval(48, 55), Interval(52, 62), Interval(4, 4), Interval(49, 60), Interval(79, 85), Interval(35, 42), Interval(75, 91)],
        [Interval(55, 64), Interval(34, 34), Interval(67, 75), Interval(18, 23), Interval(82, 96), Interval(67, 73), Interval(87, 104), Interval(38, 43), Interval(5, 5), Interval(87, 105), Interval(65, 73), Interval(3, 4), Interval(10, 11), Interval(27, 30), Interval(18, 18)],
        [Interval(74, 88), Interval(7, 8), Interval(81, 88), Interval(74, 76), Interval(38, 48), Interval(24, 29), Interval(10, 10), Interval(13, 15), Interval(42, 44), Interval(2, 2), Interval(60, 73), Interval(26, 31), Interval(11, 11), Interval(89, 93), Interval(39, 40)],
        [Interval(77, 80), Interval(87, 91), Interval(13, 15), Interval(89, 107), Interval(11, 13), Interval(60, 76), Interval(42, 44), Interval(3, 3), Interval(6, 7), Interval(35, 39), Interval(49, 54), Interval(94, 113), Interval(38, 46), Interval(58, 67), Interval(15, 16)],
        [Interval(81, 102), Interval(12, 13), Interval(46, 56), Interval(1, 1), Interval(74, 93), Interval(31, 33), Interval(1, 1), Interval(78, 94), Interval(51, 61), Interval(70, 79), Interval(77, 80), Interval(72, 91), Interval(7, 9), Interval(81, 91), Interval(30, 38)],
        [Interval(73, 82), Interval(13, 13), Interval(9, 11), Interval(11, 12), Interval(49, 52), Interval(14, 15), Interval(57, 62), Interval(80, 95), Interval(74, 87), Interval(79, 83), Interval(41, 42), Interval(80, 89), Interval(66, 81), Interval(61, 78), Interval(50, 56)],
        [Interval(39, 41), Interval(62, 65), Interval(87, 104), Interval(9, 10), Interval(95, 104), Interval(95, 107), Interval(26, 33), Interval(47, 52), Interval(17, 18), Interval(48, 49), Interval(49, 58), Interval(26, 27), Interval(51, 63), Interval(77, 94), Interval(77, 83)],
        [Interval(65, 78), Interval(86, 88), Interval(26, 31), Interval(45, 58), Interval(66, 81), Interval(74, 93), Interval(30, 35), Interval(24, 26), Interval(49, 61), Interval(82, 86), Interval(83, 105), Interval(12, 12), Interval(25, 28), Interval(78, 100), Interval(77, 85)],
        [Interval(92, 106), Interval(84, 89), Interval(71, 78), Interval(25, 26), Interval(59, 67), Interval(72, 80), Interval(3, 3), Interval(97, 111), Interval(68, 74), Interval(50, 60), Interval(71, 83), Interval(73, 78), Interval(27, 33), Interval(1, 1), Interval(50, 51)],
        [Interval(79, 81), Interval(13, 14), Interval(13, 15), Interval(27, 31), Interval(14, 16), Interval(5, 5), Interval(58, 59), Interval(31, 35), Interval(38, 39), Interval(64, 71), Interval(67, 84), Interval(83, 103), Interval(28, 31), Interval(90, 100), Interval(32, 34)],
        [Interval(83, 92), Interval(64, 71), Interval(17, 22), Interval(20, 22), Interval(4, 5), Interval(80, 100), Interval(22, 26), Interval(8, 10), Interval(90, 107), Interval(88, 109), Interval(24, 30), Interval(8, 10), Interval(66, 83), Interval(85, 94), Interval(45, 52)],
        [Interval(61, 67), Interval(17, 21), Interval(12, 13), Interval(41, 53), Interval(78, 86), Interval(63, 70), Interval(19, 22), Interval(53, 58), Interval(32, 38), Interval(48, 53), Interval(25, 30), Interval(10, 11), Interval(42, 47), Interval(29, 37), Interval(3, 3)],
        [Interval(95, 123), Interval(28, 35), Interval(49, 55), Interval(98, 103), Interval(51, 66), Interval(62, 80), Interval(22, 28), Interval(47, 55), Interval(89, 102), Interval(1, 1), Interval(83, 99), Interval(7, 9), Interval(65, 75), Interval(68, 80), Interval(88, 100)],
        [Interval(12, 15), Interval(19, 19), Interval(31, 33), Interval(93, 100), Interval(78, 97), Interval(42, 51), Interval(16, 20), Interval(56, 68), Interval(73, 95), Interval(1, 1), Interval(11, 13), Interval(24, 25), Interval(13, 15), Interval(60, 69), Interval(54, 56)],
        [Interval(43, 45), Interval(24, 26), Interval(82, 100), Interval(20, 24), Interval(6, 7), Interval(44, 46), Interval(49, 56), Interval(41, 51), Interval(66, 83), Interval(46, 52), Interval(24, 29), Interval(83, 107), Interval(6, 7), Interval(6, 6), Interval(29, 32)],
        [Interval(65, 77), Interval(91, 93), Interval(15, 19), Interval(77, 96), Interval(28, 36), Interval(70, 85), Interval(21, 22), Interval(40, 44), Interval(48, 53), Interval(35, 40), Interval(93, 101), Interval(80, 82), Interval(22, 24), Interval(74, 78), Interval(4, 4)],
        [Interval(49, 60), Interval(33, 41), Interval(10, 10), Interval(95, 100), Interval(72, 82), Interval(80, 87), Interval(65, 70), Interval(74, 93), Interval(14, 14), Interval(82, 101), Interval(12, 14), Interval(74, 78), Interval(59, 74), Interval(42, 53), Interval(58, 64)],
        [Interval(67, 79), Interval(54, 63), Interval(15, 19), Interval(85, 90), Interval(21, 25), Interval(21, 22), Interval(86, 98), Interval(16, 17), Interval(59, 71), Interval(81, 99), Interval(19, 24), Interval(32, 37), Interval(10, 13), Interval(66, 82), Interval(89, 104)],
    ],
}
