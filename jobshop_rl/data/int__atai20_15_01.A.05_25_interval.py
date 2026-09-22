"""aTA 20x15 #01 con intervalos asimetricos (protocolo A.05_25).

Generado por scripts/e4_genera_asimetricas.py a partir de la version
simetrica: el valor crisp es el punto medio de aquella, y sobre el se
sortea p_lo = p - round(p*U[0,0.05]) y p_up = p + round(p*U[0,0.25]).
Las rutas de maquina son las mismas.
"""

from jobshop_rl.models.interval import Interval


INT__ATAI20_15_01_A_05_25_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__atai20_15_01',
    'name': 'aTA 20x15 #01',
    'has_intervals': True,
    'description': 'aTA 20x15 #01 asimetrica A.05_25',
    'sequences': [[3, 11, 14, 1, 10, 2, 4, 7, 0, 12, 5, 9, 6, 13, 8], [5, 0, 3, 8, 4, 1, 12, 14, 6, 7, 10, 2, 9, 13, 11], [2, 3, 14, 0, 9, 12, 5, 4, 7, 10, 8, 11, 13, 1, 6], [8, 10, 1, 13, 3, 4, 14, 9, 2, 5, 11, 7, 0, 6, 12], [14, 8, 1, 2, 10, 9, 12, 4, 6, 5, 0, 13, 3, 11, 7], [3, 10, 1, 5, 6, 0, 8, 7, 11, 13, 2, 14, 12, 9, 4], [2, 10, 1, 12, 8, 0, 7, 6, 14, 13, 4, 3, 5, 9, 11], [1, 0, 2, 4, 7, 13, 11, 3, 12, 5, 6, 14, 9, 8, 10], [4, 5, 9, 10, 7, 6, 2, 1, 12, 3, 13, 0, 8, 14, 11], [1, 4, 3, 10, 14, 0, 6, 13, 11, 8, 5, 12, 7, 9, 2], [3, 10, 1, 0, 9, 8, 14, 6, 4, 7, 2, 12, 5, 11, 13], [2, 7, 6, 8, 3, 5, 14, 4, 1, 0, 9, 10, 13, 11, 12], [0, 7, 14, 8, 12, 10, 9, 3, 6, 1, 4, 2, 11, 13, 5], [12, 3, 9, 4, 1, 0, 10, 6, 5, 2, 14, 13, 7, 8, 11], [3, 14, 6, 5, 13, 9, 1, 0, 12, 7, 2, 4, 10, 8, 11], [5, 14, 6, 12, 8, 2, 4, 9, 11, 13, 3, 1, 7, 0, 10], [3, 7, 10, 14, 0, 8, 1, 11, 5, 13, 4, 12, 6, 9, 2], [10, 8, 2, 11, 13, 6, 14, 3, 9, 7, 4, 5, 12, 0, 1], [3, 2, 12, 13, 1, 6, 14, 5, 4, 8, 9, 11, 0, 10, 7], [11, 14, 5, 6, 10, 9, 13, 1, 4, 8, 0, 3, 12, 2, 7]],
    'durations': [
        [Interval(24, 30), Interval(72, 86), Interval(72, 89), Interval(75, 92), Interval(38, 38), Interval(59, 74), Interval(37, 38), Interval(57, 71), Interval(13, 17), Interval(13, 16), Interval(45, 48), Interval(30, 37), Interval(55, 66), Interval(89, 106), Interval(3, 4)],
        [Interval(64, 73), Interval(5, 5), Interval(11, 13), Interval(11, 13), Interval(39, 49), Interval(33, 35), Interval(76, 85), Interval(41, 51), Interval(34, 35), Interval(93, 107), Interval(22, 23), Interval(53, 63), Interval(21, 26), Interval(28, 31), Interval(16, 17)],
        [Interval(22, 26), Interval(95, 99), Interval(8, 8), Interval(34, 36), Interval(58, 70), Interval(31, 35), Interval(13, 16), Interval(45, 52), Interval(51, 58), Interval(21, 23), Interval(18, 18), Interval(19, 21), Interval(62, 67), Interval(29, 35), Interval(67, 79)],
        [Interval(94, 122), Interval(41, 52), Interval(2, 2), Interval(34, 41), Interval(11, 12), Interval(91, 99), Interval(87, 103), Interval(96, 109), Interval(21, 22), Interval(56, 68), Interval(17, 19), Interval(43, 48), Interval(26, 32), Interval(18, 19), Interval(22, 26)],
        [Interval(48, 61), Interval(5, 5), Interval(58, 69), Interval(70, 77), Interval(45, 50), Interval(39, 41), Interval(80, 94), Interval(35, 38), Interval(11, 14), Interval(2, 2), Interval(39, 42), Interval(41, 44), Interval(50, 59), Interval(64, 81), Interval(34, 37)],
        [Interval(47, 52), Interval(56, 71), Interval(5, 6), Interval(2, 2), Interval(58, 67), Interval(61, 76), Interval(86, 95), Interval(3, 3), Interval(51, 54), Interval(25, 28), Interval(33, 37), Interval(39, 43), Interval(45, 54), Interval(61, 76), Interval(52, 57)],
        [Interval(38, 41), Interval(42, 48), Interval(48, 54), Interval(70, 88), Interval(45, 52), Interval(97, 115), Interval(66, 77), Interval(33, 35), Interval(6, 7), Interval(91, 107), Interval(64, 77), Interval(52, 55), Interval(29, 34), Interval(29, 32), Interval(59, 72)],
        [Interval(56, 69), Interval(3, 3), Interval(82, 91), Interval(6, 6), Interval(46, 47), Interval(47, 58), Interval(5, 6), Interval(78, 96), Interval(17, 22), Interval(71, 80), Interval(47, 59), Interval(78, 80), Interval(61, 72), Interval(64, 69), Interval(75, 93)],
        [Interval(62, 66), Interval(52, 56), Interval(80, 88), Interval(15, 17), Interval(31, 37), Interval(50, 60), Interval(95, 97), Interval(66, 74), Interval(79, 95), Interval(89, 98), Interval(68, 84), Interval(83, 91), Interval(21, 26), Interval(71, 76), Interval(62, 65)],
        [Interval(67, 81), Interval(71, 88), Interval(51, 65), Interval(94, 101), Interval(13, 16), Interval(78, 91), Interval(24, 26), Interval(14, 17), Interval(31, 37), Interval(38, 47), Interval(65, 70), Interval(58, 68), Interval(18, 18), Interval(76, 79), Interval(50, 58)],
        [Interval(18, 20), Interval(6, 7), Interval(92, 107), Interval(51, 65), Interval(35, 39), Interval(98, 114), Interval(38, 41), Interval(18, 20), Interval(14, 17), Interval(89, 99), Interval(61, 68), Interval(81, 92), Interval(87, 93), Interval(47, 57), Interval(79, 95)],
        [Interval(42, 54), Interval(75, 82), Interval(11, 14), Interval(13, 16), Interval(71, 84), Interval(58, 61), Interval(68, 73), Interval(74, 87), Interval(29, 33), Interval(89, 104), Interval(26, 28), Interval(29, 37), Interval(83, 100), Interval(89, 97), Interval(89, 94)],
        [Interval(37, 40), Interval(53, 66), Interval(12, 16), Interval(28, 31), Interval(52, 66), Interval(68, 80), Interval(25, 29), Interval(7, 7), Interval(53, 64), Interval(48, 57), Interval(22, 24), Interval(45, 55), Interval(48, 50), Interval(92, 112), Interval(16, 19)],
        [Interval(56, 62), Interval(14, 16), Interval(8, 8), Interval(13, 14), Interval(94, 119), Interval(52, 56), Interval(76, 88), Interval(24, 25), Interval(90, 94), Interval(87, 92), Interval(68, 79), Interval(86, 108), Interval(42, 50), Interval(72, 85), Interval(94, 108)],
        [Interval(92, 100), Interval(90, 95), Interval(17, 19), Interval(28, 35), Interval(27, 28), Interval(38, 48), Interval(53, 56), Interval(81, 91), Interval(49, 57), Interval(15, 18), Interval(94, 103), Interval(47, 54), Interval(52, 60), Interval(77, 79), Interval(37, 40)],
        [Interval(46, 55), Interval(33, 40), Interval(41, 48), Interval(27, 35), Interval(11, 13), Interval(11, 11), Interval(29, 31), Interval(14, 17), Interval(10, 12), Interval(4, 4), Interval(20, 23), Interval(89, 105), Interval(19, 22), Interval(59, 70), Interval(27, 29)],
        [Interval(68, 85), Interval(80, 83), Interval(64, 64), Interval(40, 45), Interval(26, 28), Interval(81, 101), Interval(26, 29), Interval(43, 53), Interval(53, 70), Interval(17, 20), Interval(18, 20), Interval(19, 24), Interval(95, 114), Interval(43, 44), Interval(67, 80)],
        [Interval(84, 87), Interval(25, 29), Interval(86, 109), Interval(58, 74), Interval(91, 118), Interval(22, 28), Interval(85, 95), Interval(87, 94), Interval(48, 58), Interval(83, 95), Interval(12, 14), Interval(50, 60), Interval(3, 3), Interval(44, 49), Interval(19, 22)],
        [Interval(41, 46), Interval(54, 67), Interval(18, 22), Interval(70, 79), Interval(68, 73), Interval(28, 33), Interval(19, 23), Interval(22, 27), Interval(58, 67), Interval(36, 38), Interval(84, 88), Interval(13, 15), Interval(70, 85), Interval(29, 32), Interval(44, 46)],
        [Interval(7, 8), Interval(97, 101), Interval(4, 5), Interval(21, 23), Interval(72, 80), Interval(44, 52), Interval(62, 66), Interval(95, 97), Interval(63, 66), Interval(14, 16), Interval(38, 48), Interval(22, 23), Interval(75, 98), Interval(34, 35), Interval(8, 8)],
    ],
}
