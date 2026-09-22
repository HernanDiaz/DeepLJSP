"""aTA 20x15 #08 con intervalos asimetricos (protocolo A.05_25).

Generado por scripts/e4_genera_asimetricas.py a partir de la version
simetrica: el valor crisp es el punto medio de aquella, y sobre el se
sortea p_lo = p - round(p*U[0,0.05]) y p_up = p + round(p*U[0,0.25]).
Las rutas de maquina son las mismas.
"""

from jobshop_rl.models.interval import Interval


INT__ATAI20_15_08_A_05_25_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__atai20_15_08',
    'name': 'aTA 20x15 #08',
    'has_intervals': True,
    'description': 'aTA 20x15 #08 asimetrica A.05_25',
    'sequences': [[1, 6, 10, 14, 7, 5, 13, 4, 3, 8, 0, 9, 12, 2, 11], [0, 9, 3, 2, 8, 5, 14, 12, 6, 11, 10, 7, 4, 1, 13], [1, 6, 2, 11, 3, 4, 10, 9, 12, 8, 7, 5, 0, 14, 13], [12, 14, 8, 9, 5, 3, 0, 1, 13, 10, 6, 11, 4, 7, 2], [14, 10, 8, 6, 0, 4, 5, 9, 11, 3, 7, 13, 1, 12, 2], [8, 2, 9, 12, 3, 0, 13, 14, 5, 11, 7, 1, 4, 6, 10], [5, 3, 8, 7, 0, 12, 4, 2, 14, 6, 10, 11, 9, 1, 13], [5, 8, 12, 1, 7, 4, 2, 9, 6, 14, 13, 0, 3, 10, 11], [14, 8, 7, 12, 6, 10, 0, 1, 11, 9, 5, 4, 2, 3, 13], [0, 14, 2, 5, 10, 4, 9, 7, 11, 6, 3, 13, 1, 12, 8], [1, 3, 11, 0, 9, 5, 2, 14, 6, 7, 8, 12, 13, 10, 4], [12, 8, 3, 10, 2, 0, 7, 9, 14, 5, 4, 1, 11, 13, 6], [1, 6, 14, 2, 11, 4, 8, 3, 13, 10, 0, 9, 12, 7, 5], [1, 4, 9, 3, 11, 14, 8, 0, 13, 10, 2, 6, 5, 7, 12], [2, 7, 3, 1, 8, 4, 14, 11, 12, 5, 10, 0, 13, 6, 9], [10, 2, 4, 6, 1, 9, 7, 12, 3, 11, 13, 14, 5, 8, 0], [2, 0, 5, 14, 4, 6, 11, 10, 8, 7, 13, 1, 3, 9, 12], [3, 0, 11, 14, 5, 10, 4, 13, 9, 6, 8, 1, 7, 2, 12], [1, 0, 7, 5, 9, 8, 14, 13, 2, 10, 4, 3, 12, 11, 6], [1, 12, 14, 4, 7, 9, 8, 3, 6, 0, 10, 2, 11, 13, 5]],
    'durations': [
        [Interval(68, 83), Interval(6, 7), Interval(29, 33), Interval(55, 59), Interval(13, 17), Interval(33, 33), Interval(64, 75), Interval(14, 16), Interval(7, 8), Interval(55, 68), Interval(53, 57), Interval(17, 20), Interval(60, 75), Interval(44, 50), Interval(88, 103)],
        [Interval(29, 36), Interval(52, 56), Interval(19, 21), Interval(1, 1), Interval(93, 100), Interval(79, 88), Interval(62, 64), Interval(60, 65), Interval(10, 11), Interval(14, 18), Interval(69, 78), Interval(75, 83), Interval(78, 96), Interval(83, 89), Interval(93, 113)],
        [Interval(41, 45), Interval(59, 70), Interval(6, 6), Interval(59, 70), Interval(24, 30), Interval(69, 77), Interval(77, 88), Interval(11, 14), Interval(34, 36), Interval(37, 43), Interval(58, 71), Interval(87, 92), Interval(74, 87), Interval(1, 1), Interval(58, 69)],
        [Interval(73, 94), Interval(83, 84), Interval(71, 72), Interval(17, 18), Interval(26, 31), Interval(85, 98), Interval(82, 98), Interval(70, 78), Interval(86, 98), Interval(26, 27), Interval(13, 16), Interval(95, 121), Interval(3, 3), Interval(56, 64), Interval(64, 73)],
        [Interval(37, 46), Interval(57, 69), Interval(77, 92), Interval(24, 30), Interval(50, 52), Interval(73, 92), Interval(6, 7), Interval(12, 13), Interval(25, 31), Interval(14, 16), Interval(34, 41), Interval(37, 43), Interval(54, 58), Interval(32, 35), Interval(40, 46)],
        [Interval(75, 94), Interval(87, 101), Interval(58, 61), Interval(18, 23), Interval(83, 89), Interval(85, 90), Interval(60, 67), Interval(51, 62), Interval(17, 22), Interval(28, 36), Interval(2, 2), Interval(13, 15), Interval(1, 1), Interval(25, 30), Interval(52, 61)],
        [Interval(19, 21), Interval(82, 96), Interval(68, 82), Interval(21, 25), Interval(4, 5), Interval(65, 68), Interval(67, 81), Interval(87, 89), Interval(79, 88), Interval(53, 67), Interval(10, 13), Interval(19, 23), Interval(39, 42), Interval(68, 81), Interval(37, 43)],
        [Interval(37, 41), Interval(94, 117), Interval(11, 12), Interval(3, 3), Interval(32, 40), Interval(41, 48), Interval(18, 22), Interval(86, 104), Interval(55, 68), Interval(81, 86), Interval(76, 93), Interval(96, 102), Interval(2, 2), Interval(76, 89), Interval(1, 1)],
        [Interval(24, 27), Interval(65, 66), Interval(87, 94), Interval(56, 66), Interval(74, 89), Interval(46, 59), Interval(38, 40), Interval(19, 20), Interval(38, 47), Interval(40, 43), Interval(42, 46), Interval(96, 106), Interval(22, 28), Interval(73, 87), Interval(37, 47)],
        [Interval(95, 97), Interval(66, 68), Interval(54, 56), Interval(28, 33), Interval(23, 24), Interval(9, 9), Interval(71, 84), Interval(45, 50), Interval(85, 100), Interval(97, 101), Interval(73, 91), Interval(12, 15), Interval(68, 88), Interval(64, 73), Interval(24, 26)],
        [Interval(3, 3), Interval(39, 45), Interval(77, 83), Interval(71, 84), Interval(64, 69), Interval(92, 99), Interval(74, 82), Interval(16, 17), Interval(11, 13), Interval(64, 75), Interval(51, 62), Interval(19, 20), Interval(24, 29), Interval(71, 88), Interval(86, 98)],
        [Interval(13, 15), Interval(58, 69), Interval(91, 99), Interval(78, 93), Interval(45, 51), Interval(15, 19), Interval(65, 77), Interval(67, 82), Interval(63, 79), Interval(83, 87), Interval(85, 87), Interval(26, 27), Interval(26, 28), Interval(56, 66), Interval(1, 1)],
        [Interval(63, 76), Interval(1, 1), Interval(29, 32), Interval(65, 69), Interval(31, 33), Interval(33, 37), Interval(8, 9), Interval(26, 32), Interval(92, 117), Interval(93, 100), Interval(62, 66), Interval(41, 49), Interval(58, 63), Interval(54, 59), Interval(7, 7)],
        [Interval(3, 3), Interval(7, 7), Interval(40, 42), Interval(89, 99), Interval(55, 67), Interval(73, 93), Interval(24, 27), Interval(21, 23), Interval(29, 32), Interval(80, 88), Interval(1, 1), Interval(57, 70), Interval(52, 63), Interval(85, 97), Interval(18, 22)],
        [Interval(65, 75), Interval(85, 109), Interval(46, 49), Interval(76, 90), Interval(37, 39), Interval(77, 78), Interval(16, 16), Interval(39, 41), Interval(90, 114), Interval(36, 46), Interval(24, 26), Interval(50, 52), Interval(14, 15), Interval(94, 118), Interval(59, 66)],
        [Interval(33, 33), Interval(22, 23), Interval(7, 8), Interval(59, 64), Interval(73, 88), Interval(53, 55), Interval(2, 2), Interval(21, 23), Interval(31, 36), Interval(15, 16), Interval(77, 85), Interval(79, 88), Interval(66, 81), Interval(40, 46), Interval(18, 20)],
        [Interval(58, 75), Interval(26, 27), Interval(64, 71), Interval(82, 102), Interval(34, 38), Interval(15, 17), Interval(59, 74), Interval(72, 85), Interval(3, 3), Interval(79, 96), Interval(37, 42), Interval(67, 85), Interval(6, 7), Interval(70, 75), Interval(64, 66)],
        [Interval(92, 106), Interval(6, 7), Interval(52, 63), Interval(21, 26), Interval(34, 41), Interval(76, 82), Interval(16, 19), Interval(70, 73), Interval(28, 32), Interval(25, 29), Interval(51, 56), Interval(57, 61), Interval(54, 66), Interval(31, 37), Interval(73, 91)],
        [Interval(41, 50), Interval(79, 98), Interval(83, 102), Interval(24, 30), Interval(70, 80), Interval(88, 95), Interval(8, 9), Interval(59, 69), Interval(78, 98), Interval(87, 99), Interval(11, 12), Interval(71, 79), Interval(58, 70), Interval(47, 55), Interval(80, 92)],
        [Interval(51, 57), Interval(3, 3), Interval(57, 68), Interval(65, 81), Interval(84, 105), Interval(40, 49), Interval(22, 25), Interval(72, 77), Interval(96, 107), Interval(91, 93), Interval(48, 54), Interval(42, 50), Interval(79, 92), Interval(60, 70), Interval(26, 30)],
    ],
}
