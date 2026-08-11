"""
Problema INT__SINT20_15_01.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Generado con el protocolo F.15_01 del paper (delta ~ U[0, 0.15],
intervalo simetrico, semilla fija) sobre la instancia crisp sint20_15_01 de
Demirkol, Mehta y Uzsoy (1998).
"""

from jobshop_rl.models.interval import Interval


INT__SINT20_15_01_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 15,
    'problem_id': 'int__sint20_15_01.F.15_01_interval',
    'sequences': [
        [9, 5, 11, 4, 3, 8, 2, 12, 13, 0, 14, 7, 10, 1, 6],
        [2, 9, 6, 10, 13, 7, 1, 14, 11, 3, 8, 12, 5, 0, 4],
        [9, 3, 4, 14, 5, 11, 0, 2, 6, 13, 1, 12, 10, 8, 7],
        [13, 11, 4, 9, 0, 10, 3, 2, 7, 8, 14, 1, 12, 5, 6],
        [0, 7, 8, 13, 14, 4, 9, 3, 10, 11, 2, 1, 6, 5, 12],
        [13, 3, 14, 7, 1, 11, 5, 10, 9, 4, 8, 6, 0, 2, 12],
        [4, 2, 14, 0, 13, 8, 9, 10, 6, 11, 3, 7, 1, 5, 12],
        [12, 10, 5, 3, 7, 8, 14, 11, 6, 9, 4, 1, 0, 13, 2],
        [0, 14, 6, 4, 2, 3, 1, 10, 7, 11, 8, 9, 12, 13, 5],
        [14, 1, 5, 8, 13, 4, 11, 7, 3, 10, 0, 2, 6, 12, 9],
        [3, 11, 9, 14, 13, 1, 0, 8, 5, 7, 12, 2, 4, 6, 10],
        [11, 6, 8, 0, 9, 7, 5, 1, 12, 14, 10, 3, 2, 13, 4],
        [13, 12, 11, 2, 10, 7, 0, 1, 9, 8, 4, 5, 3, 6, 14],
        [12, 1, 11, 4, 9, 14, 6, 5, 10, 13, 8, 3, 0, 2, 7],
        [8, 13, 12, 6, 2, 9, 5, 1, 3, 4, 10, 7, 0, 11, 14],
        [1, 0, 3, 4, 5, 14, 8, 13, 11, 10, 9, 6, 2, 7, 12],
        [12, 14, 7, 9, 0, 11, 3, 4, 8, 2, 5, 13, 10, 1, 6],
        [7, 14, 5, 13, 9, 6, 10, 2, 4, 12, 11, 1, 0, 8, 3],
        [13, 6, 2, 8, 11, 3, 14, 1, 0, 7, 10, 12, 5, 4, 9],
        [0, 2, 6, 4, 14, 9, 13, 7, 11, 5, 12, 3, 8, 10, 1],
    ],
    'durations': [
        [Interval(49, 55), Interval(26, 32), Interval(43, 57), Interval(19, 25), Interval(50, 58), Interval(66, 82), Interval(56, 74), Interval(13, 13), Interval(69, 81), Interval(14, 16), Interval(24, 30), Interval(83, 95), Interval(30, 36), Interval(18, 22), Interval(39, 41)],
        [Interval(51, 63), Interval(64, 80), Interval(82, 96), Interval(71, 83), Interval(55, 57), Interval(7, 7), Interval(27, 35), Interval(37, 45), Interval(64, 78), Interval(13, 15), Interval(86, 112), Interval(85, 87), Interval(47, 53), Interval(23, 27), Interval(21, 23)],
        [Interval(11, 11), Interval(3, 3), Interval(14, 18), Interval(36, 40), Interval(18, 18), Interval(36, 40), Interval(67, 75), Interval(22, 28), Interval(27, 29), Interval(4, 4), Interval(61, 71), Interval(23, 29), Interval(2, 2), Interval(63, 73), Interval(92, 102)],
        [Interval(29, 37), Interval(6, 8), Interval(15, 15), Interval(51, 53), Interval(14, 16), Interval(56, 64), Interval(3, 3), Interval(69, 93), Interval(74, 84), Interval(53, 59), Interval(40, 54), Interval(64, 74), Interval(44, 48), Interval(69, 79), Interval(78, 100)],
        [Interval(20, 20), Interval(15, 19), Interval(54, 60), Interval(81, 107), Interval(32, 36), Interval(80, 104), Interval(17, 21), Interval(30, 32), Interval(59, 75), Interval(39, 45), Interval(69, 91), Interval(26, 28), Interval(81, 81), Interval(39, 51), Interval(41, 47)],
        [Interval(74, 82), Interval(10, 10), Interval(9, 9), Interval(26, 34), Interval(24, 28), Interval(16, 18), Interval(33, 35), Interval(28, 36), Interval(35, 39), Interval(55, 71), Interval(64, 72), Interval(30, 38), Interval(10, 12), Interval(26, 30), Interval(28, 30)],
        [Interval(47, 55), Interval(39, 47), Interval(87, 91), Interval(9, 11), Interval(25, 27), Interval(37, 37), Interval(71, 87), Interval(72, 82), Interval(35, 37), Interval(49, 57), Interval(25, 27), Interval(4, 4), Interval(4, 4), Interval(9, 11), Interval(72, 96)],
        [Interval(5, 5), Interval(53, 67), Interval(13, 15), Interval(41, 55), Interval(6, 6), Interval(48, 50), Interval(18, 20), Interval(40, 50), Interval(26, 28), Interval(48, 54), Interval(84, 108), Interval(85, 89), Interval(50, 62), Interval(35, 37), Interval(6, 6)],
        [Interval(41, 43), Interval(70, 80), Interval(32, 36), Interval(91, 107), Interval(4, 4), Interval(97, 99), Interval(53, 63), Interval(52, 62), Interval(10, 10), Interval(44, 46), Interval(27, 33), Interval(60, 64), Interval(74, 88), Interval(85, 85), Interval(47, 53)],
        [Interval(55, 59), Interval(57, 75), Interval(19, 19), Interval(67, 79), Interval(43, 55), Interval(80, 104), Interval(34, 38), Interval(12, 14), Interval(29, 31), Interval(77, 103), Interval(81, 85), Interval(25, 27), Interval(23, 23), Interval(43, 45), Interval(61, 67)],
        [Interval(48, 60), Interval(77, 93), Interval(12, 16), Interval(38, 40), Interval(41, 55), Interval(11, 13), Interval(37, 43), Interval(5, 5), Interval(28, 34), Interval(14, 18), Interval(34, 44), Interval(48, 56), Interval(25, 33), Interval(36, 42), Interval(41, 49)],
        [Interval(18, 22), Interval(61, 77), Interval(81, 107), Interval(37, 43), Interval(24, 26), Interval(35, 45), Interval(9, 11), Interval(43, 53), Interval(71, 91), Interval(6, 6), Interval(62, 72), Interval(24, 30), Interval(86, 110), Interval(19, 25), Interval(45, 47)],
        [Interval(80, 82), Interval(11, 13), Interval(70, 72), Interval(60, 78), Interval(25, 25), Interval(50, 58), Interval(26, 34), Interval(8, 10), Interval(79, 97), Interval(11, 13), Interval(40, 54), Interval(25, 25), Interval(79, 105), Interval(64, 70), Interval(2, 2)],
        [Interval(69, 75), Interval(73, 87), Interval(45, 57), Interval(54, 54), Interval(13, 17), Interval(36, 44), Interval(75, 79), Interval(3, 3), Interval(59, 59), Interval(28, 36), Interval(98, 98), Interval(78, 88), Interval(41, 51), Interval(5, 5), Interval(73, 91)],
        [Interval(16, 20), Interval(31, 39), Interval(20, 22), Interval(41, 53), Interval(29, 37), Interval(31, 33), Interval(92, 96), Interval(33, 41), Interval(83, 99), Interval(82, 106), Interval(38, 48), Interval(31, 31), Interval(40, 50), Interval(75, 101), Interval(72, 80)],
        [Interval(6, 6), Interval(76, 92), Interval(8, 8), Interval(36, 44), Interval(26, 28), Interval(57, 77), Interval(54, 66), Interval(80, 92), Interval(19, 21), Interval(8, 10), Interval(52, 54), Interval(34, 36), Interval(14, 16), Interval(40, 40), Interval(67, 89)],
        [Interval(19, 21), Interval(39, 45), Interval(62, 82), Interval(55, 67), Interval(79, 105), Interval(2, 2), Interval(14, 18), Interval(14, 16), Interval(25, 27), Interval(66, 66), Interval(38, 46), Interval(43, 53), Interval(75, 83), Interval(76, 98), Interval(47, 63)],
        [Interval(74, 78), Interval(84, 92), Interval(36, 38), Interval(14, 16), Interval(67, 71), Interval(31, 35), Interval(92, 100), Interval(81, 93), Interval(57, 65), Interval(67, 67), Interval(33, 35), Interval(49, 59), Interval(61, 69), Interval(82, 84), Interval(80, 96)],
        [Interval(76, 76), Interval(59, 69), Interval(36, 48), Interval(54, 58), Interval(58, 74), Interval(56, 62), Interval(14, 18), Interval(92, 94), Interval(9, 11), Interval(72, 80), Interval(28, 34), Interval(29, 37), Interval(79, 101), Interval(41, 53), Interval(36, 36)],
        [Interval(22, 26), Interval(60, 60), Interval(28, 36), Interval(95, 97), Interval(54, 62), Interval(29, 31), Interval(11, 13), Interval(58, 72), Interval(35, 43), Interval(49, 55), Interval(9, 9), Interval(15, 15), Interval(34, 38), Interval(72, 82), Interval(21, 25)],
    ],
    'name': 'int__sint20_15_01.F.15_01_interval',
    'has_intervals': True,
    'description': 'DMU sint20_15_01 ensanchada F.15_01',
}
