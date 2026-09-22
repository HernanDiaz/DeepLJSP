"""aTA 15x15 #05 con intervalos asimetricos (protocolo A.05_25).

Generado por scripts/e4_genera_asimetricas.py a partir de la version
simetrica: el valor crisp es el punto medio de aquella, y sobre el se
sortea p_lo = p - round(p*U[0,0.05]) y p_up = p + round(p*U[0,0.25]).
Las rutas de maquina son las mismas.
"""

from jobshop_rl.models.interval import Interval


INT__ATAI15_15_05_A_05_25_INTERVAL_DATA = {
    'num_jobs': 15,
    'num_machines': 15,
    'problem_id': 'int__atai15_15_05',
    'name': 'aTA 15x15 #05',
    'has_intervals': True,
    'description': 'aTA 15x15 #05 asimetrica A.05_25',
    'sequences': [[12, 1, 4, 9, 13, 0, 11, 8, 3, 5, 6, 14, 10, 2, 7], [5, 1, 14, 10, 13, 9, 6, 12, 8, 2, 7, 0, 3, 4, 11], [6, 3, 10, 7, 13, 4, 5, 9, 8, 2, 0, 1, 11, 14, 12], [10, 7, 5, 0, 9, 13, 2, 8, 1, 14, 11, 3, 12, 6, 4], [6, 12, 14, 1, 7, 5, 11, 0, 2, 3, 8, 13, 4, 9, 10], [4, 7, 6, 0, 8, 13, 12, 14, 3, 2, 5, 9, 10, 1, 11], [10, 11, 6, 9, 0, 2, 1, 8, 12, 7, 5, 3, 13, 14, 4], [3, 10, 5, 6, 8, 4, 0, 14, 2, 7, 9, 11, 12, 1, 13], [1, 2, 6, 7, 10, 12, 14, 8, 0, 3, 13, 5, 4, 9, 11], [12, 7, 6, 14, 3, 4, 0, 13, 10, 8, 11, 9, 5, 2, 1], [4, 3, 8, 14, 2, 13, 5, 6, 10, 12, 7, 11, 1, 9, 0], [6, 12, 7, 5, 2, 4, 13, 11, 8, 0, 10, 3, 1, 9, 14], [12, 13, 8, 7, 1, 6, 0, 5, 9, 10, 4, 2, 14, 3, 11], [12, 1, 4, 8, 6, 10, 7, 3, 0, 5, 13, 2, 9, 14, 11], [7, 5, 0, 10, 2, 3, 9, 6, 11, 8, 1, 4, 14, 12, 13]],
    'durations': [
        [Interval(39, 48), Interval(92, 102), Interval(56, 62), Interval(92, 103), Interval(75, 88), Interval(74, 84), Interval(22, 28), Interval(63, 73), Interval(65, 69), Interval(16, 19), Interval(69, 75), Interval(51, 56), Interval(82, 86), Interval(95, 100), Interval(23, 30)],
        [Interval(2, 2), Interval(85, 110), Interval(96, 99), Interval(51, 61), Interval(65, 73), Interval(13, 13), Interval(37, 42), Interval(34, 38), Interval(56, 60), Interval(37, 45), Interval(91, 105), Interval(37, 41), Interval(66, 84), Interval(92, 117), Interval(71, 86)],
        [Interval(87, 95), Interval(44, 57), Interval(14, 15), Interval(83, 92), Interval(30, 34), Interval(78, 81), Interval(61, 63), Interval(36, 39), Interval(53, 56), Interval(1, 1), Interval(93, 115), Interval(15, 16), Interval(2, 2), Interval(50, 59), Interval(93, 118)],
        [Interval(19, 22), Interval(15, 18), Interval(40, 46), Interval(8, 9), Interval(72, 75), Interval(14, 17), Interval(75, 88), Interval(24, 27), Interval(76, 84), Interval(82, 96), Interval(59, 70), Interval(68, 73), Interval(79, 85), Interval(16, 17), Interval(92, 116)],
        [Interval(66, 73), Interval(68, 72), Interval(3, 3), Interval(66, 69), Interval(90, 109), Interval(36, 40), Interval(72, 89), Interval(20, 21), Interval(84, 90), Interval(75, 97), Interval(49, 55), Interval(48, 52), Interval(21, 21), Interval(29, 32), Interval(62, 75)],
        [Interval(13, 16), Interval(1, 1), Interval(28, 32), Interval(72, 84), Interval(6, 6), Interval(31, 37), Interval(97, 111), Interval(49, 53), Interval(82, 83), Interval(2, 2), Interval(82, 86), Interval(32, 36), Interval(32, 36), Interval(96, 99), Interval(58, 67)],
        [Interval(21, 22), Interval(78, 98), Interval(98, 110), Interval(67, 74), Interval(78, 82), Interval(68, 71), Interval(45, 48), Interval(94, 102), Interval(55, 63), Interval(75, 92), Interval(52, 61), Interval(10, 10), Interval(89, 98), Interval(1, 1), Interval(31, 36)],
        [Interval(29, 29), Interval(81, 101), Interval(86, 102), Interval(10, 12), Interval(29, 34), Interval(36, 43), Interval(37, 40), Interval(47, 48), Interval(15, 19), Interval(63, 66), Interval(88, 112), Interval(72, 81), Interval(87, 101), Interval(45, 53), Interval(45, 52)],
        [Interval(36, 38), Interval(9, 11), Interval(47, 52), Interval(22, 25), Interval(1, 1), Interval(75, 92), Interval(37, 42), Interval(15, 17), Interval(9, 10), Interval(41, 49), Interval(34, 36), Interval(81, 96), Interval(8, 9), Interval(58, 68), Interval(59, 72)],
        [Interval(1, 1), Interval(72, 87), Interval(45, 48), Interval(45, 49), Interval(10, 12), Interval(36, 38), Interval(58, 62), Interval(80, 99), Interval(25, 28), Interval(10, 12), Interval(37, 42), Interval(77, 82), Interval(74, 77), Interval(49, 60), Interval(49, 59)],
        [Interval(22, 22), Interval(48, 59), Interval(33, 39), Interval(2, 2), Interval(23, 30), Interval(3, 4), Interval(70, 87), Interval(65, 76), Interval(21, 23), Interval(59, 75), Interval(67, 85), Interval(92, 106), Interval(42, 48), Interval(38, 41), Interval(48, 56)],
        [Interval(80, 88), Interval(44, 50), Interval(21, 22), Interval(23, 27), Interval(84, 104), Interval(18, 23), Interval(63, 66), Interval(51, 54), Interval(22, 27), Interval(49, 53), Interval(11, 13), Interval(70, 89), Interval(73, 78), Interval(16, 17), Interval(71, 86)],
        [Interval(21, 25), Interval(76, 92), Interval(29, 35), Interval(32, 34), Interval(21, 24), Interval(22, 27), Interval(81, 104), Interval(89, 111), Interval(14, 17), Interval(12, 13), Interval(65, 70), Interval(58, 70), Interval(45, 51), Interval(31, 35), Interval(86, 105)],
        [Interval(28, 34), Interval(91, 113), Interval(50, 57), Interval(58, 64), Interval(32, 40), Interval(12, 14), Interval(71, 87), Interval(96, 100), Interval(73, 75), Interval(11, 13), Interval(82, 96), Interval(3, 4), Interval(86, 99), Interval(55, 66), Interval(6, 7)],
        [Interval(92, 94), Interval(17, 22), Interval(53, 60), Interval(40, 49), Interval(67, 73), Interval(29, 29), Interval(42, 49), Interval(50, 62), Interval(73, 81), Interval(67, 75), Interval(40, 44), Interval(47, 59), Interval(1, 1), Interval(26, 29), Interval(12, 14)],
    ],
}
