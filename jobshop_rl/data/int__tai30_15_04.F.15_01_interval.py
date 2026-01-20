"""
Problema INT__TAI30_15_04.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI30_15_04_F_15_01_INTERVAL_DATA = {
    'num_jobs': 30,
    'num_machines': 15,
    'problem_id': 'int__tai30_15_04.F.15_01_interval',
    'sequences': [
        [7, 0, 12, 5, 11, 10, 8, 2, 13, 6, 4, 3, 1, 14, 9],
        [7, 11, 6, 10, 3, 1, 4, 2, 14, 8, 12, 13, 9, 5, 0],
        [1, 2, 8, 5, 4, 10, 12, 14, 13, 6, 7, 9, 11, 0, 3],
        [7, 5, 2, 10, 1, 3, 13, 6, 8, 12, 4, 14, 11, 9, 0],
        [13, 12, 0, 9, 3, 5, 10, 14, 4, 8, 1, 6, 11, 7, 2],
        [8, 6, 4, 3, 5, 11, 0, 12, 9, 1, 13, 2, 14, 7, 10],
        [3, 9, 5, 13, 8, 14, 12, 10, 2, 0, 1, 6, 7, 4, 11],
        [6, 8, 14, 3, 10, 11, 12, 4, 7, 1, 9, 13, 2, 5, 0],
        [12, 8, 3, 0, 14, 6, 11, 10, 13, 1, 7, 5, 9, 2, 4],
        [14, 12, 10, 11, 3, 5, 8, 2, 9, 13, 0, 4, 7, 1, 6],
        [11, 13, 7, 9, 12, 14, 2, 5, 8, 6, 10, 3, 4, 1, 0],
        [9, 10, 11, 4, 13, 8, 1, 2, 14, 0, 5, 12, 6, 3, 7],
        [9, 3, 6, 4, 10, 8, 12, 5, 1, 14, 11, 13, 0, 2, 7],
        [13, 7, 5, 14, 0, 6, 12, 9, 11, 3, 2, 1, 4, 10, 8],
        [10, 2, 9, 5, 3, 14, 13, 1, 4, 0, 7, 12, 11, 8, 6],
        [1, 4, 3, 9, 14, 0, 5, 7, 2, 11, 8, 10, 12, 6, 13],
        [13, 3, 5, 9, 7, 1, 4, 10, 6, 11, 0, 14, 12, 2, 8],
        [14, 0, 1, 9, 7, 11, 10, 13, 6, 12, 2, 5, 4, 3, 8],
        [7, 5, 11, 14, 8, 13, 3, 6, 9, 4, 1, 2, 10, 0, 12],
        [5, 1, 8, 2, 6, 9, 12, 7, 4, 10, 13, 3, 14, 0, 11],
        [8, 5, 1, 11, 10, 6, 7, 4, 12, 13, 0, 9, 3, 14, 2],
        [9, 2, 5, 4, 0, 8, 14, 10, 3, 1, 6, 11, 13, 7, 12],
        [14, 1, 0, 12, 10, 13, 6, 3, 8, 11, 5, 4, 2, 9, 7],
        [10, 12, 1, 7, 5, 8, 11, 9, 14, 3, 2, 6, 4, 0, 13],
        [13, 2, 1, 5, 4, 8, 14, 0, 11, 10, 7, 12, 6, 3, 9],
        [1, 13, 10, 0, 12, 11, 4, 3, 7, 9, 8, 5, 14, 6, 2],
        [5, 7, 10, 14, 12, 11, 2, 0, 9, 13, 4, 6, 1, 3, 8],
        [11, 10, 9, 7, 8, 1, 3, 6, 2, 12, 0, 14, 13, 4, 5],
        [2, 8, 0, 10, 1, 13, 5, 12, 3, 11, 4, 7, 14, 6, 9],
        [1, 8, 5, 3, 6, 13, 11, 0, 4, 9, 10, 12, 2, 7, 14],
    ],
    'durations': [
        # Job 0
        [Interval(6, 8), Interval(10, 12), Interval(32, 36), Interval(56, 56), Interval(12, 16),
         Interval(31, 35), Interval(89, 101), Interval(57, 71), Interval(11, 13), Interval(22, 22),
         Interval(77, 97), Interval(32, 32), Interval(46, 62), Interval(5, 5), Interval(48, 62)],
        # Job 1
        [Interval(57, 57), Interval(11, 11), Interval(29, 37), Interval(53, 59), Interval(8, 10),
         Interval(65, 77), Interval(92, 106), Interval(30, 32), Interval(51, 53), Interval(30, 36),
         Interval(84, 108), Interval(42, 50), Interval(1, 1), Interval(43, 53), Interval(55, 55)],
        # Job 2
        [Interval(90, 90), Interval(53, 61), Interval(68, 92), Interval(7, 9), Interval(35, 37),
         Interval(6, 8), Interval(35, 47), Interval(27, 35), Interval(27, 35), Interval(43, 53),
         Interval(58, 78), Interval(18, 20), Interval(25, 25), Interval(36, 40), Interval(88, 88)],
        # Job 3
        [Interval(74, 100), Interval(23, 25), Interval(1, 1), Interval(47, 51), Interval(63, 63),
         Interval(27, 27), Interval(96, 100), Interval(20, 24), Interval(33, 37), Interval(17, 19),
         Interval(6, 8), Interval(52, 58), Interval(53, 57), Interval(83, 91), Interval(25, 33)],
        # Job 4
        [Interval(33, 33), Interval(36, 36), Interval(68, 82), Interval(15, 19), Interval(7, 9),
         Interval(53, 57), Interval(46, 60), Interval(30, 32), Interval(95, 95), Interval(27, 35),
         Interval(63, 71), Interval(72, 88), Interval(83, 91), Interval(5, 5), Interval(51, 65)],
        # Job 5
        [Interval(73, 77), Interval(24, 26), Interval(75, 77), Interval(62, 82), Interval(69, 87),
         Interval(19, 25), Interval(75, 87), Interval(34, 40), Interval(25, 29), Interval(74, 96),
         Interval(61, 81), Interval(14, 18), Interval(76, 96), Interval(76, 80), Interval(12, 16)],
        # Job 6
        [Interval(90, 90), Interval(50, 58), Interval(89, 107), Interval(9, 11), Interval(64, 86),
         Interval(4, 4), Interval(23, 25), Interval(10, 10), Interval(7, 7), Interval(15, 15),
         Interval(42, 44), Interval(81, 99), Interval(71, 91), Interval(46, 52), Interval(81, 95)],
        # Job 7
        [Interval(93, 99), Interval(73, 89), Interval(84, 100), Interval(30, 32), Interval(8, 10),
         Interval(60, 70), Interval(32, 38), Interval(90, 106), Interval(81, 89), Interval(36, 38),
         Interval(41, 45), Interval(89, 103), Interval(88, 94), Interval(1, 1), Interval(32, 40)],
        # Job 8
        [Interval(37, 43), Interval(42, 48), Interval(92, 96), Interval(19, 23), Interval(87, 87),
         Interval(65, 71), Interval(34, 36), Interval(54, 72), Interval(37, 37), Interval(53, 53),
         Interval(97, 99), Interval(86, 102), Interval(6, 6), Interval(25, 25), Interval(66, 78)],
        # Job 9
        [Interval(33, 37), Interval(53, 57), Interval(26, 26), Interval(94, 102), Interval(23, 23),
         Interval(64, 66), Interval(80, 96), Interval(67, 75), Interval(31, 39), Interval(59, 59),
         Interval(75, 93), Interval(29, 33), Interval(67, 85), Interval(12, 14), Interval(82, 96)],
        # Job 10
        [Interval(71, 83), Interval(30, 38), Interval(57, 63), Interval(74, 78), Interval(50, 66),
         Interval(62, 64), Interval(2, 2), Interval(40, 48), Interval(84, 98), Interval(41, 43),
         Interval(53, 53), Interval(43, 47), Interval(45, 45), Interval(56, 62), Interval(93, 105)],
        # Job 11
        [Interval(6, 6), Interval(56, 56), Interval(40, 54), Interval(93, 97), Interval(31, 41),
         Interval(59, 67), Interval(75, 95), Interval(44, 50), Interval(56, 64), Interval(30, 40),
         Interval(73, 91), Interval(77, 103), Interval(30, 30), Interval(73, 79), Interval(92, 96)],
        # Job 12
        [Interval(54, 62), Interval(2, 2), Interval(65, 73), Interval(17, 21), Interval(55, 73),
         Interval(23, 31), Interval(15, 19), Interval(33, 33), Interval(43, 53), Interval(80, 82),
         Interval(86, 86), Interval(26, 30), Interval(91, 97), Interval(67, 75), Interval(3, 3)],
        # Job 13
        [Interval(83, 103), Interval(40, 40), Interval(90, 100), Interval(32, 40), Interval(38, 38),
         Interval(43, 51), Interval(24, 24), Interval(95, 99), Interval(10, 12), Interval(53, 57),
         Interval(6, 8), Interval(65, 71), Interval(3, 3), Interval(43, 45), Interval(42, 52)],
        # Job 14
        [Interval(69, 89), Interval(31, 35), Interval(62, 68), Interval(49, 65), Interval(51, 59),
         Interval(72, 84), Interval(29, 33), Interval(54, 66), Interval(69, 89), Interval(22, 28),
         Interval(72, 80), Interval(91, 101), Interval(5, 5), Interval(5, 5), Interval(38, 38)],
        # Job 15
        [Interval(71, 79), Interval(25, 33), Interval(70, 84), Interval(44, 56), Interval(30, 32),
         Interval(46, 54), Interval(5, 5), Interval(22, 28), Interval(69, 71), Interval(34, 42),
         Interval(78, 104), Interval(70, 72), Interval(78, 90), Interval(68, 92), Interval(74, 78)],
        # Job 16
        [Interval(64, 64), Interval(75, 95), Interval(92, 100), Interval(11, 11), Interval(63, 83),
         Interval(35, 47), Interval(45, 55), Interval(26, 28), Interval(40, 40), Interval(48, 60),
         Interval(57, 69), Interval(67, 81), Interval(77, 91), Interval(72, 80), Interval(51, 65)],
        # Job 17
        [Interval(59, 73), Interval(65, 85), Interval(54, 54), Interval(4, 4), Interval(14, 18),
         Interval(6, 6), Interval(89, 89), Interval(29, 29), Interval(3, 3), Interval(10, 10),
         Interval(89, 97), Interval(50, 56), Interval(8, 8), Interval(56, 62), Interval(21, 23)],
        # Job 18
        [Interval(16, 18), Interval(70, 82), Interval(79, 89), Interval(43, 47), Interval(70, 70),
         Interval(5, 5), Interval(51, 59), Interval(6, 8), Interval(23, 29), Interval(57, 61),
         Interval(2, 2), Interval(18, 18), Interval(57, 75), Interval(54, 62), Interval(94, 104)],
        # Job 19
        [Interval(53, 61), Interval(73, 95), Interval(44, 56), Interval(47, 61), Interval(88, 96),
         Interval(33, 35), Interval(55, 61), Interval(45, 57), Interval(32, 36), Interval(55, 65),
         Interval(39, 45), Interval(57, 75), Interval(17, 19), Interval(10, 12), Interval(51, 67)],
        # Job 20
        [Interval(82, 88), Interval(29, 33), Interval(28, 30), Interval(16, 20), Interval(42, 50),
         Interval(26, 32), Interval(42, 56), Interval(34, 40), Interval(42, 42), Interval(16, 20),
         Interval(69, 85), Interval(59, 75), Interval(61, 61), Interval(42, 50), Interval(85, 97)],
        # Job 21
        [Interval(2, 2), Interval(62, 70), Interval(73, 77), Interval(79, 87), Interval(59, 67),
         Interval(57, 67), Interval(70, 72), Interval(17, 23), Interval(39, 45), Interval(57, 61),
         Interval(4, 4), Interval(67, 67), Interval(81, 109), Interval(72, 80), Interval(69, 91)],
        # Job 22
        [Interval(41, 51), Interval(76, 90), Interval(7, 7), Interval(32, 42), Interval(54, 66),
         Interval(75, 77), Interval(6, 6), Interval(77, 91), Interval(76, 88), Interval(81, 107),
         Interval(31, 41), Interval(69, 89), Interval(46, 46), Interval(81, 99), Interval(87, 101)],
        # Job 23
        [Interval(8, 8), Interval(52, 68), Interval(92, 106), Interval(61, 79), Interval(21, 23),
         Interval(87, 95), Interval(62, 74), Interval(86, 88), Interval(11, 11), Interval(46, 56),
         Interval(63, 69), Interval(17, 21), Interval(27, 29), Interval(41, 53), Interval(66, 66)],
        # Job 24
        [Interval(90, 92), Interval(2, 2), Interval(39, 39), Interval(11, 13), Interval(11, 11),
         Interval(15, 19), Interval(86, 86), Interval(67, 69), Interval(86, 90), Interval(80, 92),
         Interval(76, 80), Interval(71, 79), Interval(74, 98), Interval(5, 5), Interval(73, 85)],
        # Job 25
        [Interval(16, 20), Interval(90, 90), Interval(79, 103), Interval(20, 22), Interval(45, 45),
         Interval(31, 31), Interval(65, 67), Interval(45, 53), Interval(85, 105), Interval(11, 11),
         Interval(55, 59), Interval(28, 34), Interval(32, 40), Interval(51, 63), Interval(86, 90)],
        # Job 26
        [Interval(55, 57), Interval(16, 20), Interval(39, 51), Interval(9, 9), Interval(4, 4),
         Interval(2, 2), Interval(96, 96), Interval(54, 66), Interval(42, 48), Interval(49, 65),
         Interval(5, 5), Interval(45, 53), Interval(77, 103), Interval(29, 33), Interval(92, 102)],
        # Job 27
        [Interval(89, 101), Interval(90, 102), Interval(36, 46), Interval(64, 86), Interval(55, 67),
         Interval(62, 68), Interval(17, 21), Interval(36, 40), Interval(78, 78), Interval(78, 92),
         Interval(27, 31), Interval(63, 67), Interval(76, 78), Interval(66, 68), Interval(75, 93)],
        # Job 28
        [Interval(64, 64), Interval(61, 63), Interval(48, 56), Interval(18, 24), Interval(77, 87),
         Interval(26, 28), Interval(84, 102), Interval(64, 66), Interval(29, 35), Interval(46, 48),
         Interval(61, 71), Interval(35, 43), Interval(40, 50), Interval(74, 82), Interval(24, 28)],
        # Job 29
        [Interval(20, 24), Interval(47, 57), Interval(36, 36), Interval(29, 33), Interval(35, 47),
         Interval(86, 98), Interval(97, 99), Interval(66, 70), Interval(57, 57), Interval(29, 35),
         Interval(75, 89), Interval(36, 42), Interval(80, 86), Interval(47, 49), Interval(76, 94)],
    ],
    'name': 'INT__TAI30_15_04.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai30_15_04_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI30_15_04.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI30_15_04.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI30_15_04_F_15_01_INTERVAL_DATA
