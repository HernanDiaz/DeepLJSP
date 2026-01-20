"""
Problema INT__TAI30_20_05.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI30_20_05_F_15_01_INTERVAL_DATA = {
    'num_jobs': 30,
    'num_machines': 20,
    'problem_id': 'int__tai30_20_05.F.15_01_interval',
    'sequences': [
        [11, 18, 19, 9, 1, 10, 3, 13, 7, 5, 15, 0, 4, 6, 8, 17, 16, 2, 14, 12],
        [8, 15, 18, 16, 6, 0, 2, 11, 13, 7, 10, 19, 9, 12, 3, 17, 14, 4, 5, 1],
        [17, 18, 2, 4, 14, 7, 10, 12, 13, 0, 19, 15, 5, 16, 1, 11, 9, 6, 8, 3],
        [2, 17, 4, 10, 9, 6, 12, 8, 5, 18, 3, 7, 16, 11, 19, 14, 15, 13, 1, 0],
        [4, 11, 18, 9, 2, 12, 16, 5, 7, 6, 8, 15, 3, 13, 14, 10, 0, 1, 19, 17],
        [4, 6, 16, 18, 14, 2, 7, 9, 1, 15, 10, 12, 5, 8, 19, 13, 17, 3, 0, 11],
        [19, 14, 11, 3, 6, 9, 15, 4, 2, 12, 17, 10, 13, 8, 0, 16, 7, 1, 5, 18],
        [6, 9, 17, 12, 16, 5, 0, 8, 1, 3, 14, 13, 7, 2, 4, 15, 18, 11, 10, 19],
        [10, 16, 17, 5, 15, 18, 14, 2, 0, 1, 4, 13, 7, 12, 9, 6, 8, 3, 19, 11],
        [6, 11, 15, 17, 14, 9, 7, 10, 16, 19, 8, 1, 4, 13, 5, 0, 3, 12, 18, 2],
        [10, 11, 7, 14, 5, 2, 19, 15, 1, 12, 8, 0, 16, 13, 9, 4, 17, 3, 18, 6],
        [19, 9, 0, 3, 14, 7, 13, 6, 11, 8, 15, 10, 4, 12, 1, 2, 18, 17, 5, 16],
        [6, 16, 10, 13, 9, 18, 14, 4, 1, 8, 17, 5, 2, 12, 3, 19, 0, 7, 15, 11],
        [4, 11, 5, 0, 15, 12, 13, 19, 14, 3, 16, 10, 9, 1, 18, 6, 17, 8, 7, 2],
        [1, 12, 3, 15, 11, 2, 5, 8, 16, 9, 17, 7, 4, 13, 6, 14, 0, 10, 19, 18],
        [19, 12, 7, 14, 13, 10, 2, 11, 3, 0, 16, 17, 9, 1, 18, 15, 8, 5, 6, 4],
        [16, 19, 12, 9, 3, 5, 6, 17, 13, 4, 8, 7, 1, 10, 14, 0, 11, 15, 2, 18],
        [7, 6, 0, 19, 9, 3, 16, 8, 11, 4, 12, 2, 13, 17, 18, 15, 1, 14, 5, 10],
        [12, 9, 19, 14, 7, 8, 0, 13, 16, 11, 6, 3, 1, 2, 4, 5, 10, 15, 18, 17],
        [1, 4, 18, 11, 0, 16, 12, 8, 13, 7, 2, 19, 3, 5, 9, 15, 17, 14, 10, 6],
        [10, 16, 3, 5, 4, 7, 11, 19, 15, 14, 9, 8, 6, 18, 12, 0, 1, 2, 13, 17],
        [5, 4, 7, 8, 0, 11, 1, 3, 17, 14, 16, 19, 15, 13, 10, 6, 12, 2, 9, 18],
        [13, 14, 16, 5, 0, 7, 18, 12, 1, 3, 19, 17, 11, 4, 2, 9, 15, 8, 6, 10],
        [14, 16, 19, 15, 7, 11, 4, 9, 10, 3, 18, 6, 13, 17, 2, 0, 5, 12, 1, 8],
        [8, 13, 6, 5, 1, 19, 14, 17, 9, 0, 12, 11, 3, 4, 7, 10, 15, 18, 16, 2],
        [0, 19, 12, 16, 10, 5, 14, 8, 7, 9, 18, 1, 11, 6, 17, 15, 13, 2, 4, 3],
        [12, 14, 11, 6, 0, 9, 3, 13, 4, 1, 18, 15, 8, 5, 2, 7, 10, 16, 17, 19],
        [18, 13, 7, 15, 1, 11, 0, 14, 2, 3, 8, 10, 6, 4, 12, 17, 5, 19, 16, 9],
        [11, 5, 7, 10, 8, 1, 2, 6, 14, 12, 17, 13, 0, 4, 16, 9, 3, 19, 15, 18],
        [0, 1, 19, 10, 16, 14, 5, 6, 12, 3, 7, 4, 18, 17, 9, 15, 2, 13, 11, 8],
    ],
    'durations': [
        # Job 0
        [Interval(37, 39), Interval(63, 67), Interval(79, 105), Interval(13, 13), Interval(53, 69),
         Interval(53, 59), Interval(92, 98), Interval(66, 88), Interval(40, 40), Interval(22, 24),
         Interval(82, 92), Interval(90, 102), Interval(90, 100), Interval(49, 53), Interval(98, 98),
         Interval(39, 49), Interval(10, 10), Interval(55, 59), Interval(43, 45), Interval(26, 30)],
        # Job 1
        [Interval(73, 89), Interval(36, 38), Interval(13, 13), Interval(45, 51), Interval(7, 7),
         Interval(77, 97), Interval(11, 13), Interval(23, 23), Interval(76, 90), Interval(69, 69),
         Interval(26, 26), Interval(60, 62), Interval(16, 16), Interval(57, 63), Interval(73, 85),
         Interval(45, 59), Interval(83, 85), Interval(86, 100), Interval(66, 80), Interval(83, 101)],
        # Job 2
        [Interval(66, 74), Interval(1, 1), Interval(67, 77), Interval(34, 38), Interval(65, 67),
         Interval(63, 67), Interval(56, 68), Interval(88, 108), Interval(21, 23), Interval(65, 65),
         Interval(25, 27), Interval(82, 96), Interval(11, 13), Interval(47, 57), Interval(73, 73),
         Interval(52, 52), Interval(26, 30), Interval(56, 64), Interval(10, 12), Interval(25, 27)],
        # Job 3
        [Interval(4, 4), Interval(26, 28), Interval(62, 68), Interval(39, 39), Interval(88, 98),
         Interval(11, 13), Interval(92, 92), Interval(85, 87), Interval(8, 10), Interval(85, 89),
         Interval(58, 72), Interval(71, 87), Interval(91, 93), Interval(40, 42), Interval(96, 98),
         Interval(43, 47), Interval(77, 91), Interval(88, 90), Interval(59, 69), Interval(33, 41)],
        # Job 4
        [Interval(58, 62), Interval(79, 99), Interval(15, 17), Interval(22, 26), Interval(46, 52),
         Interval(82, 104), Interval(69, 91), Interval(34, 36), Interval(60, 62), Interval(40, 52),
         Interval(36, 36), Interval(64, 72), Interval(20, 26), Interval(12, 14), Interval(47, 55),
         Interval(25, 25), Interval(71, 81), Interval(46, 46), Interval(98, 98), Interval(51, 65)],
        # Job 5
        [Interval(35, 35), Interval(17, 19), Interval(62, 82), Interval(83, 89), Interval(99, 99),
         Interval(46, 58), Interval(46, 50), Interval(84, 112), Interval(56, 60), Interval(7, 7),
         Interval(25, 27), Interval(15, 15), Interval(3, 3), Interval(36, 38), Interval(89, 95),
         Interval(9, 9), Interval(56, 70), Interval(19, 21), Interval(89, 93), Interval(80, 92)],
        # Job 6
        [Interval(49, 63), Interval(10, 10), Interval(54, 70), Interval(8, 8), Interval(49, 51),
         Interval(17, 21), Interval(47, 59), Interval(67, 71), Interval(64, 70), Interval(8, 8),
         Interval(10, 10), Interval(20, 24), Interval(39, 41), Interval(76, 94), Interval(38, 50),
         Interval(21, 23), Interval(1, 1), Interval(85, 95), Interval(46, 48), Interval(56, 62)],
        # Job 7
        [Interval(81, 83), Interval(72, 94), Interval(75, 75), Interval(83, 95), Interval(71, 73),
         Interval(37, 41), Interval(41, 53), Interval(37, 41), Interval(14, 16), Interval(1, 1),
         Interval(58, 70), Interval(59, 73), Interval(16, 18), Interval(61, 75), Interval(40, 46),
         Interval(54, 72), Interval(87, 105), Interval(34, 40), Interval(64, 64), Interval(34, 36)],
        # Job 8
        [Interval(53, 63), Interval(45, 51), Interval(17, 21), Interval(15, 19), Interval(31, 35),
         Interval(28, 30), Interval(43, 49), Interval(80, 82), Interval(10, 12), Interval(82, 94),
         Interval(56, 60), Interval(61, 79), Interval(89, 109), Interval(84, 108), Interval(89, 91),
         Interval(44, 48), Interval(68, 70), Interval(86, 98), Interval(4, 4), Interval(44, 46)],
        # Job 9
        [Interval(72, 76), Interval(76, 80), Interval(79, 79), Interval(42, 46), Interval(2, 2),
         Interval(62, 64), Interval(64, 72), Interval(51, 63), Interval(31, 35), Interval(88, 92),
         Interval(68, 70), Interval(87, 95), Interval(34, 36), Interval(70, 90), Interval(23, 29),
         Interval(38, 50), Interval(87, 95), Interval(25, 29), Interval(2, 2), Interval(53, 69)],
        # Job 10
        [Interval(52, 66), Interval(40, 52), Interval(78, 84), Interval(41, 43), Interval(50, 56),
         Interval(41, 47), Interval(20, 22), Interval(43, 47), Interval(84, 98), Interval(4, 4),
         Interval(74, 78), Interval(16, 20), Interval(67, 77), Interval(77, 79), Interval(19, 21),
         Interval(43, 45), Interval(52, 52), Interval(37, 37), Interval(63, 73), Interval(29, 37)],
        # Job 11
        [Interval(2, 2), Interval(63, 63), Interval(71, 93), Interval(34, 40), Interval(3, 3),
         Interval(48, 58), Interval(84, 94), Interval(29, 33), Interval(58, 68), Interval(6, 6),
         Interval(87, 109), Interval(2, 2), Interval(22, 24), Interval(33, 43), Interval(81, 93),
         Interval(82, 100), Interval(52, 68), Interval(48, 62), Interval(82, 104), Interval(34, 42)],
        # Job 12
        [Interval(71, 77), Interval(77, 93), Interval(55, 55), Interval(50, 54), Interval(84, 90),
         Interval(25, 25), Interval(80, 90), Interval(32, 34), Interval(39, 45), Interval(63, 67),
         Interval(51, 67), Interval(90, 92), Interval(85, 97), Interval(16, 16), Interval(30, 30),
         Interval(62, 62), Interval(61, 79), Interval(14, 14), Interval(31, 39), Interval(17, 21)],
        # Job 13
        [Interval(15, 17), Interval(22, 24), Interval(63, 77), Interval(41, 41), Interval(11, 13),
         Interval(98, 100), Interval(25, 27), Interval(38, 48), Interval(14, 14), Interval(79, 103),
         Interval(44, 56), Interval(71, 85), Interval(1, 1), Interval(2, 2), Interval(4, 4),
         Interval(73, 87), Interval(13, 15), Interval(58, 68), Interval(53, 57), Interval(13, 15)],
        # Job 14
        [Interval(74, 98), Interval(30, 34), Interval(51, 61), Interval(80, 82), Interval(50, 54),
         Interval(14, 14), Interval(7, 7), Interval(74, 74), Interval(31, 35), Interval(68, 70),
         Interval(23, 23), Interval(62, 74), Interval(40, 50), Interval(19, 19), Interval(36, 40),
         Interval(35, 35), Interval(19, 23), Interval(40, 44), Interval(80, 92), Interval(89, 107)],
        # Job 15
        [Interval(30, 36), Interval(47, 55), Interval(94, 98), Interval(5, 5), Interval(48, 64),
         Interval(83, 97), Interval(44, 56), Interval(41, 41), Interval(31, 37), Interval(83, 103),
         Interval(57, 65), Interval(64, 70), Interval(56, 64), Interval(28, 34), Interval(5, 5),
         Interval(37, 45), Interval(75, 95), Interval(53, 63), Interval(54, 60), Interval(10, 10)],
        # Job 16
        [Interval(23, 27), Interval(86, 98), Interval(16, 18), Interval(90, 98), Interval(65, 69),
         Interval(57, 63), Interval(63, 79), Interval(24, 32), Interval(69, 71), Interval(87, 107),
         Interval(52, 60), Interval(25, 33), Interval(52, 60), Interval(39, 43), Interval(52, 62),
         Interval(70, 70), Interval(23, 29), Interval(46, 54), Interval(2, 2), Interval(42, 46)],
        # Job 17
        [Interval(25, 29), Interval(44, 52), Interval(81, 89), Interval(16, 18), Interval(1, 1),
         Interval(74, 98), Interval(81, 95), Interval(38, 48), Interval(56, 60), Interval(75, 89),
         Interval(44, 58), Interval(57, 61), Interval(37, 39), Interval(86, 112), Interval(7, 7),
         Interval(45, 53), Interval(79, 97), Interval(56, 56), Interval(76, 84), Interval(1, 1)],
        # Job 18
        [Interval(53, 69), Interval(44, 52), Interval(89, 91), Interval(56, 62), Interval(71, 89),
         Interval(40, 48), Interval(26, 26), Interval(42, 46), Interval(75, 97), Interval(28, 34),
         Interval(70, 74), Interval(26, 32), Interval(67, 69), Interval(28, 30), Interval(44, 54),
         Interval(23, 23), Interval(56, 62), Interval(58, 64), Interval(64, 76), Interval(44, 54)],
        # Job 19
        [Interval(34, 40), Interval(41, 49), Interval(22, 26), Interval(78, 98), Interval(16, 20),
         Interval(30, 36), Interval(41, 43), Interval(4, 4), Interval(7, 7), Interval(59, 79),
         Interval(63, 73), Interval(36, 42), Interval(78, 96), Interval(60, 62), Interval(37, 47),
         Interval(15, 17), Interval(37, 49), Interval(75, 91), Interval(6, 6), Interval(33, 39)],
        # Job 20
        [Interval(89, 93), Interval(33, 37), Interval(9, 9), Interval(86, 110), Interval(47, 51),
         Interval(86, 106), Interval(62, 74), Interval(80, 82), Interval(10, 10), Interval(51, 65),
         Interval(20, 22), Interval(83, 97), Interval(24, 28), Interval(34, 38), Interval(86, 96),
         Interval(45, 59), Interval(9, 9), Interval(49, 49), Interval(14, 16), Interval(77, 83)],
        # Job 21
        [Interval(11, 11), Interval(71, 85), Interval(56, 62), Interval(46, 48), Interval(11, 11),
         Interval(23, 25), Interval(51, 59), Interval(81, 93), Interval(26, 30), Interval(2, 2),
         Interval(21, 25), Interval(37, 39), Interval(63, 79), Interval(67, 71), Interval(95, 99),
         Interval(73, 75), Interval(42, 44), Interval(54, 60), Interval(44, 44), Interval(22, 24)],
        # Job 22
        [Interval(13, 13), Interval(49, 59), Interval(18, 20), Interval(3, 3), Interval(4, 4),
         Interval(13, 13), Interval(72, 82), Interval(72, 76), Interval(2, 2), Interval(57, 75),
         Interval(76, 86), Interval(59, 61), Interval(38, 38), Interval(80, 100), Interval(58, 76),
         Interval(34, 34), Interval(24, 30), Interval(52, 62), Interval(71, 73), Interval(7, 7)],
        # Job 23
        [Interval(28, 30), Interval(62, 76), Interval(13, 13), Interval(90, 102), Interval(84, 96),
         Interval(22, 26), Interval(78, 102), Interval(3, 3), Interval(53, 61), Interval(74, 92),
         Interval(68, 88), Interval(4, 4), Interval(24, 24), Interval(62, 68), Interval(40, 48),
         Interval(20, 22), Interval(53, 59), Interval(69, 77), Interval(92, 94), Interval(93, 101)],
        # Job 24
        [Interval(48, 58), Interval(12, 14), Interval(17, 19), Interval(29, 37), Interval(76, 82),
         Interval(42, 48), Interval(17, 17), Interval(42, 52), Interval(43, 47), Interval(78, 80),
         Interval(7, 7), Interval(79, 99), Interval(49, 53), Interval(30, 34), Interval(26, 26),
         Interval(30, 34), Interval(42, 44), Interval(61, 63), Interval(30, 32), Interval(13, 15)],
        # Job 25
        [Interval(63, 63), Interval(56, 56), Interval(66, 70), Interval(48, 50), Interval(37, 43),
         Interval(45, 57), Interval(3, 3), Interval(81, 93), Interval(59, 67), Interval(48, 56),
         Interval(88, 102), Interval(49, 63), Interval(87, 107), Interval(28, 32), Interval(85, 113),
         Interval(34, 44), Interval(6, 6), Interval(65, 87), Interval(33, 35), Interval(70, 76)],
        # Job 26
        [Interval(61, 75), Interval(29, 33), Interval(58, 60), Interval(6, 6), Interval(27, 33),
         Interval(51, 65), Interval(63, 83), Interval(61, 63), Interval(70, 72), Interval(87, 105),
         Interval(23, 23), Interval(61, 81), Interval(18, 22), Interval(10, 12), Interval(49, 51),
         Interval(92, 92), Interval(56, 68), Interval(64, 70), Interval(10, 10), Interval(60, 70)],
        # Job 27
        [Interval(94, 102), Interval(79, 87), Interval(89, 89), Interval(60, 68), Interval(4, 4),
         Interval(25, 29), Interval(77, 81), Interval(23, 27), Interval(76, 80), Interval(34, 38),
         Interval(52, 52), Interval(35, 47), Interval(19, 23), Interval(57, 67), Interval(78, 78),
         Interval(87, 97), Interval(85, 99), Interval(88, 88), Interval(74, 86), Interval(63, 65)],
        # Job 28
        [Interval(77, 99), Interval(77, 79), Interval(9, 11), Interval(14, 14), Interval(8, 8),
         Interval(17, 19), Interval(9, 11), Interval(37, 37), Interval(49, 49), Interval(26, 28),
         Interval(86, 102), Interval(91, 99), Interval(37, 37), Interval(21, 25), Interval(14, 16),
         Interval(80, 94), Interval(51, 57), Interval(1, 1), Interval(66, 82), Interval(38, 42)],
        # Job 29
        [Interval(20, 22), Interval(3, 3), Interval(30, 34), Interval(47, 55), Interval(9, 9),
         Interval(67, 85), Interval(21, 25), Interval(67, 79), Interval(46, 60), Interval(75, 87),
         Interval(74, 74), Interval(88, 96), Interval(66, 72), Interval(54, 58), Interval(80, 106),
         Interval(51, 53), Interval(81, 85), Interval(1, 1), Interval(17, 17), Interval(44, 48)],
    ],
    'name': 'INT__TAI30_20_05.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai30_20_05_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI30_20_05.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI30_20_05.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI30_20_05_F_15_01_INTERVAL_DATA
