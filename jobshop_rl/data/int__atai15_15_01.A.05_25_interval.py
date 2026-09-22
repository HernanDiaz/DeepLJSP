"""aTA 15x15 #01 con intervalos asimetricos (protocolo A.05_25).

Generado por scripts/e4_genera_asimetricas.py a partir de la version
simetrica: el valor crisp es el punto medio de aquella, y sobre el se
sortea p_lo = p - round(p*U[0,0.05]) y p_up = p + round(p*U[0,0.25]).
Las rutas de maquina son las mismas.
"""

from jobshop_rl.models.interval import Interval


INT__ATAI15_15_01_A_05_25_INTERVAL_DATA = {
    'num_jobs': 15,
    'num_machines': 15,
    'problem_id': 'int__atai15_15_01',
    'name': 'aTA 15x15 #01',
    'has_intervals': True,
    'description': 'aTA 15x15 #01 asimetrica A.05_25',
    'sequences': [[6, 12, 4, 7, 3, 2, 10, 11, 8, 14, 9, 13, 5, 0, 1], [4, 5, 7, 14, 13, 8, 11, 9, 6, 10, 0, 3, 12, 1, 2], [1, 8, 9, 12, 6, 11, 13, 5, 0, 2, 7, 10, 4, 3, 14], [5, 2, 9, 6, 10, 0, 13, 4, 7, 14, 11, 8, 12, 1, 3], [7, 8, 6, 10, 4, 9, 2, 14, 12, 5, 1, 13, 11, 0, 3], [5, 3, 12, 13, 11, 4, 14, 7, 2, 1, 10, 0, 9, 6, 8], [12, 3, 7, 8, 14, 6, 1, 11, 4, 5, 2, 10, 0, 13, 9], [11, 5, 0, 7, 12, 13, 14, 1, 2, 8, 4, 3, 9, 6, 10], [10, 11, 6, 14, 0, 1, 2, 5, 12, 4, 8, 7, 9, 13, 3], [6, 11, 9, 2, 8, 0, 13, 3, 10, 7, 1, 12, 14, 4, 5], [4, 7, 13, 0, 5, 12, 6, 8, 14, 10, 3, 1, 11, 9, 2], [2, 14, 0, 12, 6, 10, 7, 5, 8, 9, 13, 1, 3, 11, 4], [5, 8, 10, 2, 3, 6, 9, 0, 13, 4, 1, 11, 12, 7, 14], [8, 14, 4, 13, 5, 6, 9, 1, 12, 7, 11, 10, 3, 2, 0], [10, 8, 12, 6, 4, 1, 13, 14, 11, 0, 7, 3, 2, 9, 5]],
    'durations': [
        [Interval(92, 112), Interval(63, 72), Interval(10, 12), Interval(51, 55), Interval(26, 27), Interval(15, 18), Interval(65, 80), Interval(81, 87), Interval(10, 12), Interval(26, 30), Interval(90, 113), Interval(90, 115), Interval(93, 119), Interval(69, 83), Interval(79, 91)],
        [Interval(71, 81), Interval(30, 36), Interval(85, 94), Interval(50, 61), Interval(55, 71), Interval(76, 96), Interval(8, 9), Interval(7, 7), Interval(90, 96), Interval(78, 93), Interval(17, 21), Interval(49, 52), Interval(17, 18), Interval(97, 100), Interval(32, 39)],
        [Interval(4, 4), Interval(79, 84), Interval(39, 44), Interval(82, 106), Interval(48, 56), Interval(53, 67), Interval(20, 25), Interval(6, 6), Interval(53, 55), Interval(65, 68), Interval(80, 87), Interval(20, 24), Interval(37, 48), Interval(34, 35), Interval(66, 69)],
        [Interval(72, 82), Interval(22, 24), Interval(30, 37), Interval(30, 30), Interval(53, 65), Interval(91, 101), Interval(57, 64), Interval(91, 110), Interval(31, 34), Interval(90, 91), Interval(29, 30), Interval(54, 61), Interval(27, 31), Interval(91, 93), Interval(9, 10)],
        [Interval(78, 95), Interval(23, 27), Interval(20, 25), Interval(58, 60), Interval(35, 44), Interval(29, 35), Interval(94, 113), Interval(95, 102), Interval(77, 93), Interval(73, 79), Interval(89, 102), Interval(41, 44), Interval(52, 53), Interval(40, 52), Interval(95, 115)],
        [Interval(28, 32), Interval(60, 72), Interval(84, 102), Interval(68, 74), Interval(15, 16), Interval(30, 34), Interval(63, 71), Interval(80, 85), Interval(74, 85), Interval(25, 27), Interval(50, 52), Interval(83, 105), Interval(60, 73), Interval(14, 15), Interval(29, 33)],
        [Interval(17, 21), Interval(74, 78), Interval(19, 24), Interval(4, 4), Interval(88, 110), Interval(67, 73), Interval(19, 20), Interval(53, 67), Interval(83, 90), Interval(70, 80), Interval(42, 54), Interval(24, 25), Interval(36, 41), Interval(87, 88), Interval(64, 69)],
        [Interval(31, 33), Interval(51, 62), Interval(9, 11), Interval(49, 58), Interval(59, 74), Interval(34, 37), Interval(97, 114), Interval(60, 73), Interval(6, 7), Interval(60, 65), Interval(7, 8), Interval(78, 97), Interval(3, 3), Interval(57, 59), Interval(7, 8)],
        [Interval(82, 95), Interval(29, 34), Interval(94, 99), Interval(90, 103), Interval(13, 13), Interval(85, 106), Interval(79, 83), Interval(82, 100), Interval(77, 81), Interval(56, 59), Interval(84, 104), Interval(8, 8), Interval(63, 79), Interval(87, 95), Interval(14, 15)],
        [Interval(5, 5), Interval(56, 61), Interval(29, 31), Interval(58, 63), Interval(40, 47), Interval(17, 17), Interval(64, 75), Interval(85, 95), Interval(77, 80), Interval(87, 93), Interval(67, 78), Interval(44, 56), Interval(81, 86), Interval(6, 6), Interval(13, 15)],
        [Interval(88, 94), Interval(26, 31), Interval(1, 1), Interval(8, 9), Interval(90, 102), Interval(78, 92), Interval(88, 105), Interval(49, 52), Interval(31, 38), Interval(28, 32), Interval(90, 111), Interval(91, 115), Interval(6, 6), Interval(35, 44), Interval(73, 83)],
        [Interval(45, 55), Interval(41, 47), Interval(72, 88), Interval(8, 9), Interval(50, 58), Interval(3, 3), Interval(80, 103), Interval(33, 38), Interval(27, 29), Interval(57, 70), Interval(66, 72), Interval(45, 54), Interval(65, 70), Interval(58, 62), Interval(85, 94)],
        [Interval(63, 67), Interval(60, 62), Interval(95, 111), Interval(20, 22), Interval(30, 34), Interval(32, 38), Interval(33, 38), Interval(75, 89), Interval(50, 51), Interval(77, 92), Interval(47, 53), Interval(86, 106), Interval(74, 89), Interval(93, 98), Interval(44, 55)],
        [Interval(27, 29), Interval(21, 26), Interval(50, 61), Interval(73, 86), Interval(17, 19), Interval(85, 104), Interval(57, 62), Interval(55, 58), Interval(62, 71), Interval(17, 19), Interval(16, 19), Interval(29, 37), Interval(15, 18), Interval(7, 8), Interval(33, 37)],
        [Interval(57, 61), Interval(15, 19), Interval(42, 49), Interval(33, 34), Interval(36, 40), Interval(25, 27), Interval(65, 71), Interval(72, 83), Interval(5, 6), Interval(8, 9), Interval(12, 14), Interval(83, 102), Interval(79, 89), Interval(20, 24), Interval(96, 105)],
    ],
}
