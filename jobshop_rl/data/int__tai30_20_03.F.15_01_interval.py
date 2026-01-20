"""
Problema INT__TAI30_20_03.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI30_20_03_F_15_01_INTERVAL_DATA = {
    'num_jobs': 30,
    'num_machines': 20,
    'problem_id': 'int__tai30_20_03.F.15_01_interval',
    'sequences': [
        [3, 17, 14, 10, 5, 12, 18, 8, 15, 4, 1, 7, 9, 6, 16, 0, 13, 2, 11, 19],
        [8, 7, 12, 14, 1, 4, 17, 19, 9, 15, 0, 3, 2, 6, 11, 16, 10, 5, 18, 13],
        [18, 14, 1, 11, 0, 6, 12, 4, 15, 5, 13, 17, 9, 16, 8, 2, 19, 3, 7, 10],
        [15, 1, 4, 11, 3, 2, 17, 10, 14, 13, 16, 7, 18, 0, 12, 5, 8, 9, 6, 19],
        [5, 10, 15, 13, 16, 19, 18, 2, 4, 7, 8, 17, 11, 9, 14, 6, 3, 0, 12, 1],
        [9, 16, 1, 5, 6, 11, 13, 14, 2, 0, 4, 17, 15, 19, 10, 18, 8, 3, 7, 12],
        [2, 6, 7, 14, 4, 12, 15, 16, 13, 5, 1, 10, 0, 17, 9, 18, 3, 19, 8, 11],
        [8, 14, 13, 16, 10, 7, 2, 19, 0, 6, 5, 12, 4, 11, 1, 3, 18, 17, 9, 15],
        [3, 0, 14, 4, 15, 6, 8, 5, 17, 9, 13, 16, 1, 2, 12, 10, 18, 19, 7, 11],
        [1, 19, 0, 7, 2, 6, 10, 4, 17, 5, 12, 13, 14, 15, 18, 16, 3, 8, 9, 11],
        [9, 0, 1, 13, 3, 16, 14, 2, 5, 12, 7, 8, 19, 4, 18, 10, 11, 6, 15, 17],
        [1, 14, 4, 11, 2, 7, 3, 12, 16, 9, 13, 17, 18, 0, 10, 15, 5, 8, 6, 19],
        [0, 9, 10, 4, 2, 3, 7, 12, 11, 17, 14, 15, 13, 6, 8, 19, 18, 1, 16, 5],
        [17, 11, 5, 3, 14, 7, 1, 15, 10, 12, 13, 16, 2, 18, 19, 0, 9, 8, 4, 6],
        [3, 19, 4, 10, 2, 1, 11, 15, 0, 5, 14, 17, 8, 13, 12, 6, 7, 9, 18, 16],
        [9, 0, 6, 14, 3, 11, 8, 10, 2, 13, 15, 19, 4, 18, 17, 12, 1, 5, 7, 16],
        [17, 12, 18, 6, 14, 16, 13, 2, 9, 19, 7, 3, 8, 11, 0, 4, 1, 5, 15, 10],
        [3, 15, 0, 2, 4, 6, 9, 10, 14, 16, 11, 5, 17, 13, 18, 19, 8, 1, 12, 7],
        [0, 6, 17, 4, 1, 2, 18, 12, 11, 16, 10, 15, 3, 13, 8, 14, 19, 7, 9, 5],
        [6, 19, 3, 13, 18, 4, 7, 1, 9, 16, 8, 17, 10, 14, 2, 15, 11, 12, 5, 0],
        [8, 18, 7, 14, 0, 11, 4, 9, 13, 5, 3, 12, 17, 16, 2, 15, 19, 6, 10, 1],
        [15, 0, 8, 9, 13, 5, 3, 16, 10, 17, 1, 7, 14, 4, 18, 2, 12, 6, 19, 11],
        [14, 17, 19, 5, 16, 6, 4, 10, 15, 18, 12, 13, 8, 2, 7, 9, 1, 0, 11, 3],
        [19, 13, 2, 17, 9, 1, 4, 0, 3, 11, 10, 8, 18, 14, 16, 12, 15, 7, 5, 6],
        [6, 14, 15, 7, 4, 16, 11, 0, 1, 10, 17, 19, 13, 18, 3, 12, 8, 5, 2, 9],
        [8, 6, 4, 7, 15, 10, 18, 3, 13, 19, 14, 5, 0, 2, 11, 16, 17, 12, 9, 1],
        [4, 0, 5, 8, 9, 18, 14, 15, 10, 12, 13, 7, 11, 3, 16, 2, 6, 1, 19, 17],
        [18, 7, 3, 9, 14, 6, 0, 15, 8, 19, 11, 12, 13, 5, 10, 4, 1, 16, 2, 17],
        [3, 15, 11, 9, 16, 5, 12, 19, 13, 0, 17, 2, 8, 1, 6, 14, 18, 4, 7, 10],
        [7, 18, 16, 10, 4, 3, 11, 0, 17, 14, 2, 5, 9, 6, 19, 15, 13, 12, 8, 1],
    ],
    'durations': [
        # Job 0
        [Interval(80, 92), Interval(5, 5), Interval(21, 21), Interval(67, 67), Interval(78, 96),
         Interval(88, 92), Interval(21, 21), Interval(75, 99), Interval(77, 87), Interval(64, 72),
         Interval(22, 28), Interval(9, 11), Interval(55, 61), Interval(61, 69), Interval(20, 20),
         Interval(34, 34), Interval(11, 13), Interval(31, 39), Interval(60, 66), Interval(40, 42)],
        # Job 1
        [Interval(88, 94), Interval(76, 84), Interval(34, 42), Interval(75, 83), Interval(59, 73),
         Interval(6, 6), Interval(19, 23), Interval(83, 95), Interval(50, 50), Interval(82, 104),
         Interval(49, 55), Interval(33, 33), Interval(82, 82), Interval(47, 55), Interval(84, 96),
         Interval(55, 55), Interval(85, 113), Interval(65, 85), Interval(21, 23), Interval(54, 62)],
        # Job 2
        [Interval(54, 64), Interval(22, 22), Interval(10, 10), Interval(1, 1), Interval(73, 77),
         Interval(1, 1), Interval(30, 40), Interval(15, 15), Interval(38, 40), Interval(26, 30),
         Interval(27, 31), Interval(8, 8), Interval(58, 72), Interval(42, 48), Interval(5, 5),
         Interval(82, 98), Interval(17, 19), Interval(11, 11), Interval(35, 43), Interval(68, 72)],
        # Job 3
        [Interval(20, 20), Interval(36, 42), Interval(2, 2), Interval(29, 35), Interval(41, 47),
         Interval(78, 92), Interval(27, 33), Interval(66, 70), Interval(66, 68), Interval(57, 57),
         Interval(14, 14), Interval(69, 81), Interval(63, 79), Interval(37, 45), Interval(36, 36),
         Interval(30, 36), Interval(70, 74), Interval(28, 36), Interval(87, 97), Interval(17, 17)],
        # Job 4
        [Interval(80, 84), Interval(62, 80), Interval(53, 57), Interval(26, 30), Interval(71, 75),
         Interval(12, 12), Interval(18, 18), Interval(37, 45), Interval(67, 89), Interval(66, 76),
         Interval(26, 26), Interval(87, 107), Interval(23, 23), Interval(62, 68), Interval(52, 56),
         Interval(79, 97), Interval(87, 101), Interval(25, 31), Interval(22, 22), Interval(89, 101)],
        # Job 5
        [Interval(5, 5), Interval(27, 31), Interval(64, 82), Interval(65, 73), Interval(49, 53),
         Interval(69, 71), Interval(23, 25), Interval(78, 100), Interval(19, 23), Interval(83, 95),
         Interval(73, 93), Interval(13, 15), Interval(60, 62), Interval(12, 12), Interval(91, 103),
         Interval(54, 60), Interval(56, 66), Interval(56, 66), Interval(17, 21), Interval(3, 3)],
        # Job 6
        [Interval(37, 49), Interval(4, 4), Interval(29, 35), Interval(4, 4), Interval(83, 109),
         Interval(31, 37), Interval(20, 22), Interval(2, 2), Interval(33, 33), Interval(75, 79),
         Interval(59, 65), Interval(37, 41), Interval(81, 97), Interval(84, 96), Interval(86, 94),
         Interval(41, 43), Interval(16, 16), Interval(68, 78), Interval(67, 83), Interval(57, 57)],
        # Job 7
        [Interval(73, 83), Interval(62, 64), Interval(26, 26), Interval(45, 51), Interval(9, 9),
         Interval(24, 28), Interval(52, 58), Interval(80, 106), Interval(15, 15), Interval(84, 86),
         Interval(39, 39), Interval(81, 93), Interval(66, 66), Interval(53, 55), Interval(66, 70),
         Interval(30, 30), Interval(7, 7), Interval(45, 59), Interval(2, 2), Interval(27, 35)],
        # Job 8
        [Interval(53, 57), Interval(82, 92), Interval(9, 11), Interval(5, 5), Interval(43, 53),
         Interval(72, 84), Interval(78, 96), Interval(7, 9), Interval(61, 79), Interval(69, 69),
         Interval(52, 62), Interval(83, 87), Interval(52, 64), Interval(65, 83), Interval(86, 98),
         Interval(76, 78), Interval(50, 58), Interval(43, 43), Interval(25, 31), Interval(6, 6)],
        # Job 9
        [Interval(40, 44), Interval(68, 74), Interval(68, 68), Interval(66, 88), Interval(19, 19),
         Interval(12, 12), Interval(51, 67), Interval(70, 78), Interval(65, 77), Interval(20, 24),
         Interval(7, 7), Interval(49, 57), Interval(87, 111), Interval(71, 71), Interval(78, 98),
         Interval(79, 103), Interval(21, 23), Interval(42, 50), Interval(72, 88), Interval(52, 58)],
        # Job 10
        [Interval(67, 87), Interval(15, 19), Interval(74, 84), Interval(1, 1), Interval(64, 80),
         Interval(85, 91), Interval(36, 48), Interval(80, 86), Interval(81, 87), Interval(7, 9),
         Interval(39, 41), Interval(84, 98), Interval(63, 69), Interval(83, 87), Interval(38, 48),
         Interval(45, 57), Interval(86, 102), Interval(23, 23), Interval(75, 93), Interval(15, 15)],
        # Job 11
        [Interval(6, 6), Interval(40, 42), Interval(5, 5), Interval(86, 88), Interval(41, 51),
         Interval(67, 83), Interval(49, 49), Interval(6, 6), Interval(1, 1), Interval(50, 50),
         Interval(85, 91), Interval(57, 73), Interval(9, 11), Interval(88, 88), Interval(41, 51),
         Interval(29, 37), Interval(41, 53), Interval(72, 72), Interval(47, 49), Interval(11, 13)],
        # Job 12
        [Interval(54, 58), Interval(73, 77), Interval(47, 59), Interval(32, 36), Interval(71, 75),
         Interval(80, 86), Interval(68, 76), Interval(15, 15), Interval(24, 32), Interval(51, 53),
         Interval(47, 51), Interval(14, 16), Interval(76, 86), Interval(84, 92), Interval(10, 12),
         Interval(45, 59), Interval(45, 51), Interval(80, 96), Interval(16, 20), Interval(44, 48)],
        # Job 13
        [Interval(67, 69), Interval(36, 36), Interval(34, 34), Interval(11, 11), Interval(54, 72),
         Interval(30, 32), Interval(28, 32), Interval(54, 64), Interval(77, 93), Interval(55, 65),
         Interval(71, 85), Interval(79, 85), Interval(6, 6), Interval(78, 98), Interval(39, 47),
         Interval(58, 74), Interval(92, 94), Interval(77, 87), Interval(34, 44), Interval(16, 16)],
        # Job 14
        [Interval(55, 61), Interval(47, 49), Interval(84, 110), Interval(67, 67), Interval(3, 3),
         Interval(76, 94), Interval(34, 38), Interval(24, 24), Interval(2, 2), Interval(35, 39),
         Interval(70, 74), Interval(2, 2), Interval(23, 27), Interval(73, 75), Interval(41, 51),
         Interval(37, 49), Interval(61, 63), Interval(24, 30), Interval(72, 82), Interval(77, 87)],
        # Job 15
        [Interval(5, 5), Interval(85, 101), Interval(79, 79), Interval(35, 45), Interval(4, 4),
         Interval(79, 85), Interval(68, 78), Interval(68, 74), Interval(56, 66), Interval(64, 66),
         Interval(63, 85), Interval(2, 2), Interval(54, 60), Interval(67, 89), Interval(11, 13),
         Interval(1, 1), Interval(77, 89), Interval(10, 10), Interval(82, 88), Interval(46, 50)],
        # Job 16
        [Interval(72, 78), Interval(55, 71), Interval(16, 16), Interval(15, 15), Interval(42, 42),
         Interval(34, 34), Interval(24, 30), Interval(3, 3), Interval(79, 87), Interval(7, 7),
         Interval(11, 13), Interval(56, 70), Interval(84, 104), Interval(20, 20), Interval(31, 39),
         Interval(67, 83), Interval(45, 59), Interval(25, 25), Interval(93, 103), Interval(81, 85)],
        # Job 17
        [Interval(38, 40), Interval(57, 73), Interval(21, 21), Interval(34, 34), Interval(63, 69),
         Interval(26, 28), Interval(76, 86), Interval(30, 36), Interval(26, 32), Interval(84, 106),
         Interval(1, 1), Interval(55, 73), Interval(81, 83), Interval(60, 62), Interval(68, 80),
         Interval(46, 56), Interval(46, 50), Interval(91, 107), Interval(23, 23), Interval(52, 62)],
        # Job 18
        [Interval(81, 95), Interval(90, 96), Interval(11, 11), Interval(78, 102), Interval(24, 30),
         Interval(57, 69), Interval(20, 20), Interval(45, 57), Interval(33, 39), Interval(71, 81),
         Interval(26, 26), Interval(10, 10), Interval(66, 76), Interval(68, 80), Interval(31, 39),
         Interval(42, 54), Interval(12, 12), Interval(36, 36), Interval(24, 24), Interval(9, 11)],
        # Job 19
        [Interval(90, 96), Interval(52, 60), Interval(25, 31), Interval(52, 62), Interval(20, 22),
         Interval(54, 64), Interval(43, 53), Interval(6, 6), Interval(16, 16), Interval(84, 96),
         Interval(6, 6), Interval(46, 52), Interval(28, 36), Interval(81, 83), Interval(3, 3),
         Interval(4, 4), Interval(29, 33), Interval(25, 25), Interval(8, 8), Interval(27, 29)],
        # Job 20
        [Interval(64, 72), Interval(11, 11), Interval(92, 106), Interval(3, 3), Interval(77, 79),
         Interval(1, 1), Interval(37, 41), Interval(61, 69), Interval(19, 19), Interval(16, 16),
         Interval(11, 11), Interval(26, 26), Interval(10, 10), Interval(54, 54), Interval(2, 2),
         Interval(62, 76), Interval(87, 95), Interval(35, 43), Interval(1, 1), Interval(86, 96)],
        # Job 21
        [Interval(10, 10), Interval(22, 26), Interval(54, 56), Interval(69, 73), Interval(90, 108),
         Interval(81, 89), Interval(58, 58), Interval(17, 19), Interval(10, 12), Interval(84, 96),
         Interval(7, 7), Interval(81, 95), Interval(74, 76), Interval(92, 102), Interval(73, 77),
         Interval(11, 11), Interval(8, 8), Interval(6, 6), Interval(40, 50), Interval(75, 81)],
        # Job 22
        [Interval(68, 68), Interval(55, 59), Interval(14, 16), Interval(32, 40), Interval(27, 27),
         Interval(25, 27), Interval(60, 72), Interval(36, 40), Interval(94, 100), Interval(53, 57),
         Interval(63, 83), Interval(22, 24), Interval(59, 77), Interval(18, 20), Interval(78, 100),
         Interval(41, 51), Interval(33, 35), Interval(36, 42), Interval(20, 26), Interval(52, 68)],
        # Job 23
        [Interval(26, 30), Interval(20, 20), Interval(43, 45), Interval(71, 91), Interval(58, 66),
         Interval(60, 72), Interval(42, 46), Interval(50, 54), Interval(38, 42), Interval(85, 93),
         Interval(83, 101), Interval(26, 28), Interval(6, 6), Interval(75, 75), Interval(6, 6),
         Interval(90, 102), Interval(49, 51), Interval(67, 79), Interval(53, 67), Interval(29, 33)],
        # Job 24
        [Interval(81, 99), Interval(55, 55), Interval(36, 46), Interval(19, 21), Interval(44, 58),
         Interval(43, 45), Interval(65, 69), Interval(6, 6), Interval(76, 88), Interval(5, 5),
         Interval(10, 10), Interval(56, 70), Interval(75, 85), Interval(36, 42), Interval(20, 24),
         Interval(46, 50), Interval(22, 26), Interval(65, 67), Interval(41, 51), Interval(89, 93)],
        # Job 25
        [Interval(41, 41), Interval(4, 4), Interval(31, 37), Interval(62, 74), Interval(51, 65),
         Interval(67, 75), Interval(54, 60), Interval(73, 89), Interval(57, 67), Interval(80, 88),
         Interval(56, 58), Interval(21, 25), Interval(30, 32), Interval(52, 66), Interval(18, 18),
         Interval(68, 80), Interval(53, 67), Interval(37, 39), Interval(62, 78), Interval(47, 51)],
        # Job 26
        [Interval(48, 58), Interval(6, 6), Interval(73, 85), Interval(82, 86), Interval(3, 3),
         Interval(37, 45), Interval(27, 29), Interval(57, 65), Interval(38, 48), Interval(31, 41),
         Interval(60, 76), Interval(7, 9), Interval(34, 36), Interval(71, 75), Interval(75, 87),
         Interval(87, 99), Interval(1, 1), Interval(85, 103), Interval(87, 105), Interval(66, 80)],
        # Job 27
        [Interval(80, 104), Interval(94, 94), Interval(52, 56), Interval(17, 17), Interval(11, 11),
         Interval(40, 42), Interval(53, 57), Interval(14, 16), Interval(87, 87), Interval(80, 82),
         Interval(61, 63), Interval(75, 81), Interval(25, 31), Interval(8, 8), Interval(76, 78),
         Interval(77, 87), Interval(1, 1), Interval(67, 69), Interval(79, 89), Interval(51, 65)],
        # Job 28
        [Interval(74, 90), Interval(31, 31), Interval(11, 13), Interval(68, 88), Interval(80, 86),
         Interval(30, 36), Interval(39, 39), Interval(73, 83), Interval(33, 33), Interval(11, 11),
         Interval(83, 99), Interval(51, 57), Interval(23, 29), Interval(88, 92), Interval(66, 76),
         Interval(11, 13), Interval(26, 30), Interval(51, 63), Interval(91, 107), Interval(48, 50)],
        # Job 29
        [Interval(33, 41), Interval(17, 17), Interval(3, 3), Interval(57, 57), Interval(71, 71),
         Interval(72, 92), Interval(9, 9), Interval(28, 30), Interval(17, 17), Interval(88, 110),
         Interval(89, 103), Interval(94, 100), Interval(10, 10), Interval(25, 27), Interval(34, 38),
         Interval(31, 33), Interval(14, 14), Interval(31, 39), Interval(32, 36), Interval(8, 8)],
    ],
    'name': 'INT__TAI30_20_03.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai30_20_03_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI30_20_03.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI30_20_03.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI30_20_03_F_15_01_INTERVAL_DATA
