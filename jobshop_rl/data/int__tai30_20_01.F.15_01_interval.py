"""
Problema INT__TAI30_20_01.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI30_20_01_F_15_01_INTERVAL_DATA = {
    'num_jobs': 30,
    'num_machines': 20,
    'problem_id': 'int__tai30_20_01.F.15_01_interval',
    'sequences': [
        [5, 13, 3, 15, 19, 9, 10, 6, 12, 4, 2, 14, 8, 7, 16, 11, 0, 17, 18, 1],
        [13, 2, 15, 12, 4, 9, 3, 7, 5, 0, 8, 14, 6, 19, 1, 10, 18, 17, 16, 11],
        [8, 5, 2, 18, 17, 14, 0, 4, 11, 3, 16, 7, 6, 1, 12, 15, 10, 19, 13, 9],
        [13, 8, 0, 11, 3, 14, 7, 4, 18, 6, 19, 5, 2, 9, 10, 15, 17, 1, 12, 16],
        [8, 6, 2, 13, 16, 11, 15, 12, 9, 4, 19, 17, 5, 3, 7, 1, 10, 18, 14, 0],
        [1, 13, 10, 0, 2, 12, 19, 5, 17, 16, 18, 4, 15, 8, 7, 6, 14, 11, 3, 9],
        [2, 3, 16, 17, 10, 15, 13, 12, 9, 19, 8, 0, 18, 11, 14, 1, 5, 7, 4, 6],
        [12, 10, 17, 4, 3, 11, 2, 19, 8, 9, 13, 14, 7, 18, 15, 6, 16, 1, 5, 0],
        [10, 14, 3, 0, 7, 17, 19, 2, 11, 16, 6, 4, 18, 1, 13, 5, 12, 15, 8, 9],
        [0, 2, 3, 9, 8, 12, 16, 13, 4, 10, 6, 19, 15, 1, 5, 17, 7, 14, 18, 11],
        [1, 4, 0, 10, 15, 11, 16, 9, 19, 13, 14, 8, 6, 17, 18, 12, 2, 7, 3, 5],
        [6, 5, 9, 10, 0, 2, 3, 12, 11, 7, 13, 8, 19, 14, 16, 4, 17, 1, 18, 15],
        [13, 19, 11, 5, 2, 15, 14, 4, 3, 6, 10, 1, 12, 18, 9, 7, 16, 17, 8, 0],
        [10, 3, 4, 9, 17, 8, 0, 19, 2, 11, 12, 1, 18, 15, 5, 16, 6, 14, 13, 7],
        [4, 14, 8, 15, 11, 9, 10, 1, 17, 16, 5, 18, 6, 13, 19, 12, 7, 3, 2, 0],
        [4, 9, 18, 19, 3, 17, 15, 16, 5, 8, 11, 14, 0, 2, 1, 12, 6, 10, 13, 7],
        [17, 10, 13, 19, 0, 12, 14, 18, 2, 5, 11, 16, 7, 4, 8, 1, 15, 6, 9, 3],
        [19, 13, 9, 3, 6, 17, 7, 16, 5, 14, 15, 18, 0, 2, 1, 12, 8, 11, 10, 4],
        [9, 11, 17, 13, 3, 1, 10, 16, 0, 5, 7, 6, 4, 2, 18, 15, 14, 19, 8, 12],
        [17, 8, 13, 7, 4, 0, 6, 9, 16, 18, 11, 5, 10, 12, 2, 19, 15, 14, 3, 1],
        [17, 2, 7, 16, 6, 12, 14, 9, 3, 18, 0, 4, 5, 8, 1, 19, 10, 11, 15, 13],
        [0, 7, 16, 12, 3, 6, 19, 2, 10, 9, 18, 8, 13, 5, 11, 4, 15, 1, 17, 14],
        [10, 18, 4, 5, 12, 6, 9, 1, 11, 13, 8, 7, 17, 0, 2, 14, 19, 15, 16, 3],
        [14, 0, 5, 11, 9, 19, 10, 15, 2, 3, 4, 18, 17, 13, 12, 7, 6, 1, 16, 8],
        [11, 6, 18, 14, 16, 0, 17, 10, 9, 2, 7, 4, 19, 5, 8, 1, 12, 15, 13, 3],
        [18, 13, 10, 12, 1, 9, 0, 7, 2, 5, 16, 6, 17, 8, 14, 3, 4, 11, 19, 15],
        [14, 2, 19, 10, 11, 16, 9, 7, 15, 1, 5, 13, 4, 8, 18, 0, 3, 12, 6, 17],
        [0, 18, 8, 9, 12, 17, 16, 19, 15, 11, 2, 13, 3, 10, 5, 7, 6, 4, 1, 14],
        [18, 11, 9, 14, 4, 0, 16, 3, 8, 6, 13, 15, 7, 2, 10, 12, 19, 17, 5, 1],
        [16, 3, 9, 6, 2, 18, 11, 1, 4, 0, 5, 7, 12, 15, 8, 14, 13, 19, 10, 17],
    ],
    'durations': [
        # Job 0
        [Interval(59, 59), Interval(67, 77), Interval(81, 103), Interval(30, 40), Interval(17, 17),
         Interval(42, 54), Interval(51, 63), Interval(17, 19), Interval(47, 63), Interval(47, 55),
         Interval(8, 8), Interval(63, 73), Interval(85, 95), Interval(37, 41), Interval(73, 85),
         Interval(38, 42), Interval(59, 73), Interval(55, 55), Interval(59, 65), Interval(60, 72)],
        # Job 1
        [Interval(38, 46), Interval(59, 61), Interval(49, 55), Interval(14, 14), Interval(79, 87),
         Interval(87, 103), Interval(32, 40), Interval(25, 31), Interval(4, 4), Interval(28, 34),
         Interval(13, 15), Interval(23, 23), Interval(63, 79), Interval(88, 102), Interval(69, 69),
         Interval(17, 17), Interval(12, 14), Interval(23, 23), Interval(73, 83), Interval(44, 58)],
        # Job 2
        [Interval(81, 105), Interval(12, 12), Interval(32, 36), Interval(29, 35), Interval(52, 66),
         Interval(66, 80), Interval(41, 51), Interval(25, 25), Interval(76, 88), Interval(85, 95),
         Interval(69, 71), Interval(24, 30), Interval(71, 93), Interval(85, 85), Interval(35, 45),
         Interval(31, 39), Interval(58, 64), Interval(80, 104), Interval(97, 99), Interval(51, 55)],
        # Job 3
        [Interval(29, 33), Interval(95, 95), Interval(36, 36), Interval(55, 67), Interval(87, 97),
         Interval(24, 24), Interval(63, 77), Interval(14, 16), Interval(67, 85), Interval(46, 54),
         Interval(17, 19), Interval(28, 32), Interval(80, 106), Interval(58, 66), Interval(72, 94),
         Interval(16, 16), Interval(71, 79), Interval(26, 32), Interval(33, 37), Interval(28, 34)],
        # Job 4
        [Interval(26, 28), Interval(9, 11), Interval(91, 95), Interval(25, 27), Interval(63, 65),
         Interval(69, 71), Interval(15, 17), Interval(43, 53), Interval(42, 50), Interval(36, 38),
         Interval(78, 100), Interval(77, 89), Interval(65, 77), Interval(69, 75), Interval(44, 46),
         Interval(67, 79), Interval(91, 103), Interval(12, 12), Interval(50, 64), Interval(58, 66)],
        # Job 5
        [Interval(9, 9), Interval(16, 16), Interval(75, 75), Interval(20, 22), Interval(44, 54),
         Interval(83, 111), Interval(5, 5), Interval(19, 21), Interval(23, 29), Interval(50, 50),
         Interval(24, 28), Interval(20, 20), Interval(7, 9), Interval(91, 101), Interval(50, 50),
         Interval(79, 89), Interval(7, 7), Interval(49, 55), Interval(65, 81), Interval(40, 46)],
        # Job 6
        [Interval(19, 21), Interval(70, 82), Interval(3, 3), Interval(44, 46), Interval(50, 56),
         Interval(6, 6), Interval(78, 88), Interval(68, 86), Interval(19, 23), Interval(49, 55),
         Interval(28, 36), Interval(26, 28), Interval(84, 102), Interval(72, 90), Interval(69, 87),
         Interval(6, 6), Interval(90, 96), Interval(60, 60), Interval(12, 12), Interval(32, 38)],
        # Job 7
        [Interval(36, 46), Interval(57, 61), Interval(33, 41), Interval(82, 96), Interval(84, 90),
         Interval(28, 36), Interval(94, 102), Interval(24, 24), Interval(27, 33), Interval(84, 84),
         Interval(49, 49), Interval(80, 88), Interval(38, 50), Interval(16, 16), Interval(40, 46),
         Interval(57, 73), Interval(42, 46), Interval(73, 93), Interval(62, 80), Interval(67, 75)],
        # Job 8
        [Interval(43, 49), Interval(34, 38), Interval(59, 61), Interval(59, 59), Interval(51, 55),
         Interval(55, 61), Interval(8, 8), Interval(33, 33), Interval(69, 71), Interval(91, 95),
         Interval(35, 41), Interval(5, 5), Interval(67, 83), Interval(21, 25), Interval(95, 101),
         Interval(82, 98), Interval(18, 18), Interval(56, 68), Interval(4, 4), Interval(55, 57)],
        # Job 9
        [Interval(25, 29), Interval(27, 35), Interval(42, 48), Interval(49, 65), Interval(74, 84),
         Interval(13, 15), Interval(76, 88), Interval(87, 105), Interval(4, 4), Interval(17, 17),
         Interval(40, 52), Interval(3, 3), Interval(7, 7), Interval(39, 45), Interval(24, 24),
         Interval(80, 92), Interval(66, 68), Interval(68, 90), Interval(43, 43), Interval(17, 17)],
        # Job 10
        [Interval(62, 82), Interval(51, 57), Interval(51, 51), Interval(77, 97), Interval(49, 55),
         Interval(4, 4), Interval(33, 37), Interval(62, 62), Interval(15, 15), Interval(39, 51),
         Interval(75, 93), Interval(64, 66), Interval(82, 88), Interval(47, 51), Interval(91, 105),
         Interval(5, 5), Interval(74, 88), Interval(7, 9), Interval(64, 80), Interval(32, 34)],
        # Job 11
        [Interval(30, 32), Interval(85, 87), Interval(41, 51), Interval(3, 3), Interval(61, 65),
         Interval(52, 64), Interval(70, 92), Interval(7, 7), Interval(48, 60), Interval(39, 39),
         Interval(45, 47), Interval(85, 99), Interval(87, 105), Interval(54, 60), Interval(38, 42),
         Interval(45, 53), Interval(55, 59), Interval(80, 92), Interval(18, 22), Interval(85, 97)],
        # Job 12
        [Interval(31, 39), Interval(5, 5), Interval(39, 47), Interval(74, 94), Interval(71, 83),
         Interval(18, 22), Interval(81, 87), Interval(67, 73), Interval(68, 90), Interval(46, 58),
         Interval(90, 94), Interval(30, 38), Interval(38, 40), Interval(30, 30), Interval(58, 72),
         Interval(10, 12), Interval(83, 93), Interval(31, 33), Interval(69, 91), Interval(2, 2)],
        # Job 13
        [Interval(58, 60), Interval(33, 39), Interval(70, 74), Interval(43, 49), Interval(42, 54),
         Interval(69, 75), Interval(70, 82), Interval(45, 51), Interval(60, 78), Interval(56, 68),
         Interval(29, 31), Interval(42, 54), Interval(7, 7), Interval(88, 90), Interval(35, 39),
         Interval(43, 55), Interval(28, 32), Interval(49, 55), Interval(1, 1), Interval(54, 58)],
        # Job 14
        [Interval(17, 19), Interval(34, 36), Interval(53, 69), Interval(20, 26), Interval(42, 50),
         Interval(12, 12), Interval(38, 38), Interval(55, 63), Interval(49, 51), Interval(75, 75),
         Interval(53, 67), Interval(53, 61), Interval(61, 65), Interval(89, 89), Interval(65, 77),
         Interval(45, 59), Interval(74, 92), Interval(77, 95), Interval(80, 82), Interval(98, 98)],
        # Job 15
        [Interval(30, 36), Interval(13, 15), Interval(18, 20), Interval(78, 90), Interval(63, 75),
         Interval(54, 64), Interval(2, 2), Interval(81, 85), Interval(12, 12), Interval(20, 22),
         Interval(70, 76), Interval(74, 92), Interval(23, 29), Interval(83, 105), Interval(62, 68),
         Interval(98, 98), Interval(72, 94), Interval(42, 48), Interval(39, 41), Interval(84, 94)],
        # Job 16
        [Interval(56, 70), Interval(65, 79), Interval(71, 89), Interval(2, 2), Interval(88, 100),
         Interval(11, 11), Interval(24, 26), Interval(10, 10), Interval(78, 102), Interval(68, 78),
         Interval(19, 21), Interval(88, 96), Interval(10, 12), Interval(73, 97), Interval(56, 70),
         Interval(92, 102), Interval(38, 38), Interval(12, 14), Interval(38, 46), Interval(56, 62)],
        # Job 17
        [Interval(86, 104), Interval(4, 4), Interval(85, 105), Interval(6, 6), Interval(66, 68),
         Interval(27, 33), Interval(80, 96), Interval(24, 28), Interval(56, 58), Interval(56, 66),
         Interval(9, 9), Interval(34, 36), Interval(23, 23), Interval(44, 50), Interval(45, 47),
         Interval(89, 103), Interval(18, 20), Interval(50, 58), Interval(66, 84), Interval(11, 11)],
        # Job 18
        [Interval(62, 66), Interval(72, 86), Interval(82, 92), Interval(90, 92), Interval(2, 2),
         Interval(57, 65), Interval(31, 31), Interval(79, 91), Interval(52, 54), Interval(74, 80),
         Interval(24, 26), Interval(81, 107), Interval(43, 43), Interval(12, 14), Interval(37, 43),
         Interval(55, 63), Interval(3, 3), Interval(80, 80), Interval(7, 7), Interval(89, 107)],
        # Job 19
        [Interval(56, 56), Interval(11, 13), Interval(67, 81), Interval(41, 43), Interval(87, 109),
         Interval(65, 85), Interval(17, 19), Interval(94, 102), Interval(20, 20), Interval(69, 75),
         Interval(32, 36), Interval(71, 77), Interval(10, 10), Interval(97, 99), Interval(11, 13),
         Interval(94, 96), Interval(29, 37), Interval(62, 76), Interval(84, 102), Interval(81, 81)],
        # Job 20
        [Interval(67, 79), Interval(38, 38), Interval(25, 25), Interval(80, 104), Interval(37, 39),
         Interval(84, 98), Interval(88, 102), Interval(2, 2), Interval(74, 84), Interval(38, 44),
         Interval(3, 3), Interval(97, 101), Interval(76, 90), Interval(16, 20), Interval(11, 13),
         Interval(68, 74), Interval(4, 4), Interval(66, 66), Interval(18, 22), Interval(50, 56)],
        # Job 21
        [Interval(61, 61), Interval(21, 27), Interval(23, 25), Interval(22, 22), Interval(76, 94),
         Interval(50, 62), Interval(85, 111), Interval(5, 5), Interval(28, 30), Interval(63, 83),
         Interval(27, 27), Interval(89, 109), Interval(4, 4), Interval(89, 109), Interval(55, 71),
         Interval(25, 25), Interval(54, 68), Interval(47, 55), Interval(78, 90), Interval(26, 34)],
        # Job 22
        [Interval(5, 5), Interval(16, 18), Interval(36, 44), Interval(85, 91), Interval(27, 33),
         Interval(3, 3), Interval(1, 1), Interval(91, 101), Interval(8, 10), Interval(91, 97),
         Interval(68, 70), Interval(69, 75), Interval(80, 100), Interval(13, 15), Interval(36, 46),
         Interval(45, 55), Interval(60, 78), Interval(37, 39), Interval(12, 12), Interval(1, 1)],
        # Job 23
        [Interval(50, 60), Interval(17, 21), Interval(53, 69), Interval(55, 67), Interval(94, 100),
         Interval(68, 84), Interval(34, 42), Interval(63, 75), Interval(21, 27), Interval(58, 66),
         Interval(21, 27), Interval(85, 103), Interval(3, 3), Interval(5, 5), Interval(72, 96),
         Interval(40, 46), Interval(65, 81), Interval(73, 79), Interval(41, 53), Interval(89, 93)],
        # Job 24
        [Interval(74, 96), Interval(89, 107), Interval(68, 68), Interval(53, 61), Interval(59, 67),
         Interval(51, 65), Interval(68, 80), Interval(49, 55), Interval(59, 59), Interval(45, 49),
         Interval(71, 75), Interval(73, 85), Interval(42, 54), Interval(33, 43), Interval(88, 88),
         Interval(81, 89), Interval(4, 4), Interval(43, 45), Interval(37, 37), Interval(64, 86)],
        # Job 25
        [Interval(39, 49), Interval(30, 34), Interval(34, 42), Interval(89, 97), Interval(38, 42),
         Interval(54, 58), Interval(78, 82), Interval(83, 97), Interval(64, 84), Interval(80, 84),
         Interval(56, 62), Interval(82, 100), Interval(39, 41), Interval(26, 26), Interval(69, 79),
         Interval(7, 7), Interval(49, 49), Interval(79, 97), Interval(59, 61), Interval(33, 37)],
        # Job 26
        [Interval(74, 76), Interval(70, 76), Interval(12, 14), Interval(4, 4), Interval(77, 77),
         Interval(5, 5), Interval(55, 59), Interval(85, 111), Interval(56, 64), Interval(95, 103),
         Interval(12, 12), Interval(13, 15), Interval(25, 25), Interval(75, 97), Interval(12, 14),
         Interval(80, 106), Interval(37, 45), Interval(1, 1), Interval(46, 60), Interval(49, 59)],
        # Job 27
        [Interval(29, 37), Interval(72, 78), Interval(88, 106), Interval(31, 31), Interval(74, 94),
         Interval(44, 54), Interval(48, 54), Interval(26, 34), Interval(55, 69), Interval(67, 67),
         Interval(76, 92), Interval(40, 50), Interval(42, 54), Interval(58, 66), Interval(63, 65),
         Interval(82, 92), Interval(13, 15), Interval(68, 84), Interval(39, 45), Interval(67, 75)],
        # Job 28
        [Interval(66, 82), Interval(90, 106), Interval(11, 11), Interval(85, 107), Interval(37, 41),
         Interval(30, 32), Interval(50, 58), Interval(43, 55), Interval(47, 55), Interval(38, 42),
         Interval(20, 22), Interval(17, 21), Interval(42, 46), Interval(73, 79), Interval(60, 68),
         Interval(40, 46), Interval(8, 10), Interval(30, 30), Interval(58, 74), Interval(16, 18)],
        # Job 29
        [Interval(29, 33), Interval(75, 79), Interval(92, 92), Interval(24, 30), Interval(63, 79),
         Interval(81, 83), Interval(32, 40), Interval(33, 33), Interval(48, 48), Interval(84, 98),
         Interval(48, 50), Interval(36, 42), Interval(88, 94), Interval(46, 48), Interval(72, 76),
         Interval(15, 19), Interval(60, 64), Interval(26, 30), Interval(87, 95), Interval(51, 65)],
    ],
    'name': 'INT__TAI30_20_01.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai30_20_01_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI30_20_01.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI30_20_01.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI30_20_01_F_15_01_INTERVAL_DATA
