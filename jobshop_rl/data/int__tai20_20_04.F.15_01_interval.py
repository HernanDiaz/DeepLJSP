"""
Problema INT__TAI20_20_04.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI20_20_04_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 20,
    'problem_id': 'int__tai20_20_04.F.15_01_interval',
    'sequences': [
        [1, 18, 4, 15, 16, 19, 0, 10, 5, 14, 13, 7, 8, 6, 2, 11, 3, 9, 12, 17],
        [4, 2, 3, 14, 1, 0, 13, 17, 18, 16, 5, 10, 9, 15, 19, 11, 8, 6, 7, 12],
        [1, 16, 8, 18, 13, 14, 6, 0, 9, 15, 19, 3, 12, 5, 4, 11, 10, 7, 2, 17],
        [19, 3, 4, 9, 1, 2, 18, 8, 6, 16, 13, 14, 12, 5, 7, 11, 15, 10, 17, 0],
        [15, 12, 1, 10, 0, 19, 11, 13, 2, 14, 17, 6, 16, 3, 7, 4, 8, 9, 18, 5],
        [3, 7, 9, 0, 5, 6, 14, 16, 4, 2, 19, 12, 13, 18, 1, 11, 17, 10, 8, 15],
        [17, 3, 11, 9, 4, 13, 16, 8, 0, 18, 1, 19, 10, 5, 6, 15, 14, 12, 7, 2],
        [17, 13, 16, 4, 11, 7, 12, 6, 8, 10, 2, 18, 0, 9, 15, 1, 3, 5, 14, 19],
        [0, 11, 1, 18, 2, 13, 9, 7, 8, 15, 16, 12, 14, 10, 6, 17, 3, 5, 4, 19],
        [9, 3, 6, 12, 0, 13, 2, 1, 17, 16, 18, 19, 4, 11, 14, 7, 15, 5, 8, 10],
        [12, 10, 16, 9, 18, 7, 8, 0, 6, 3, 15, 1, 5, 4, 17, 14, 13, 19, 11, 2],
        [6, 18, 8, 4, 7, 17, 0, 14, 11, 19, 3, 10, 9, 16, 12, 5, 1, 13, 2, 15],
        [17, 4, 16, 12, 19, 1, 2, 18, 11, 3, 10, 6, 5, 7, 9, 0, 8, 13, 15, 14],
        [14, 11, 1, 9, 12, 7, 10, 19, 2, 17, 13, 16, 8, 15, 5, 3, 18, 0, 6, 4],
        [4, 10, 19, 18, 16, 11, 5, 15, 1, 7, 2, 14, 13, 3, 17, 0, 12, 6, 9, 8],
        [2, 3, 7, 18, 14, 6, 12, 0, 9, 13, 4, 16, 10, 5, 19, 11, 17, 15, 8, 1],
        [3, 2, 15, 9, 18, 11, 7, 17, 16, 8, 19, 13, 0, 6, 4, 10, 14, 1, 5, 12],
        [4, 10, 8, 1, 12, 18, 17, 15, 11, 19, 3, 14, 13, 7, 2, 9, 5, 6, 0, 16],
        [13, 15, 5, 14, 3, 18, 17, 10, 2, 19, 6, 12, 11, 16, 7, 0, 4, 1, 9, 8],
        [3, 13, 18, 8, 11, 9, 17, 12, 16, 0, 2, 14, 19, 7, 10, 1, 15, 4, 6, 5],
    ],
    'durations': [
        # Job 0
        [Interval(28, 32), Interval(74, 86), Interval(32, 36), Interval(90, 94), Interval(25, 33),
         Interval(93, 99), Interval(25, 25), Interval(46, 52), Interval(65, 69), Interval(48, 58),
         Interval(19, 21), Interval(46, 58), Interval(27, 31), Interval(48, 54), Interval(35, 35),
         Interval(35, 41), Interval(17, 19), Interval(42, 44), Interval(45, 47), Interval(87, 109)],
        # Job 1
        [Interval(72, 74), Interval(64, 72), Interval(3, 3), Interval(91, 105), Interval(65, 71),
         Interval(8, 8), Interval(15, 15), Interval(76, 100), Interval(62, 82), Interval(18, 22),
         Interval(89, 89), Interval(56, 62), Interval(67, 69), Interval(62, 64), Interval(40, 42),
         Interval(27, 33), Interval(41, 45), Interval(70, 90), Interval(58, 70), Interval(13, 15)],
        # Job 2
        [Interval(6, 6), Interval(31, 41), Interval(83, 93), Interval(71, 71), Interval(46, 56),
         Interval(56, 70), Interval(32, 32), Interval(15, 17), Interval(61, 65), Interval(7, 7),
         Interval(16, 20), Interval(86, 94), Interval(50, 60), Interval(23, 27), Interval(71, 73),
         Interval(88, 96), Interval(84, 92), Interval(60, 78), Interval(87, 91), Interval(73, 93)],
        # Job 3
        [Interval(55, 61), Interval(31, 39), Interval(74, 84), Interval(43, 43), Interval(82, 90),
         Interval(47, 53), Interval(59, 69), Interval(79, 97), Interval(55, 59), Interval(24, 26),
         Interval(65, 81), Interval(18, 18), Interval(4, 4), Interval(60, 78), Interval(36, 44),
         Interval(25, 31), Interval(33, 41), Interval(40, 44), Interval(80, 84), Interval(77, 89)],
        # Job 4
        [Interval(2, 2), Interval(35, 47), Interval(12, 14), Interval(66, 84), Interval(28, 34),
         Interval(61, 71), Interval(65, 79), Interval(65, 67), Interval(84, 108), Interval(43, 47),
         Interval(26, 32), Interval(48, 50), Interval(91, 101), Interval(48, 52), Interval(34, 42),
         Interval(69, 91), Interval(83, 97), Interval(36, 36), Interval(44, 56), Interval(65, 87)],
        # Job 5
        [Interval(14, 16), Interval(31, 31), Interval(76, 102), Interval(77, 97), Interval(54, 56),
         Interval(47, 51), Interval(20, 26), Interval(17, 21), Interval(35, 41), Interval(85, 101),
         Interval(74, 76), Interval(45, 45), Interval(65, 85), Interval(71, 73), Interval(63, 67),
         Interval(6, 6), Interval(16, 16), Interval(24, 24), Interval(23, 25), Interval(39, 49)],
        # Job 6
        [Interval(4, 4), Interval(20, 24), Interval(95, 103), Interval(9, 11), Interval(78, 92),
         Interval(79, 79), Interval(2, 2), Interval(48, 60), Interval(75, 85), Interval(2, 2),
         Interval(51, 65), Interval(32, 34), Interval(83, 101), Interval(81, 105), Interval(86, 102),
         Interval(30, 38), Interval(32, 40), Interval(43, 53), Interval(51, 57), Interval(12, 12)],
        # Job 7
        [Interval(18, 20), Interval(2, 2), Interval(7, 7), Interval(57, 63), Interval(35, 37),
         Interval(11, 11), Interval(97, 97), Interval(54, 60), Interval(68, 74), Interval(52, 68),
         Interval(19, 21), Interval(65, 71), Interval(50, 56), Interval(54, 54), Interval(54, 64),
         Interval(15, 17), Interval(58, 62), Interval(60, 76), Interval(60, 70), Interval(40, 44)],
        # Job 8
        [Interval(57, 57), Interval(16, 16), Interval(87, 97), Interval(85, 113), Interval(81, 83),
         Interval(83, 99), Interval(12, 12), Interval(17, 21), Interval(51, 67), Interval(41, 45),
         Interval(18, 22), Interval(74, 94), Interval(23, 25), Interval(75, 85), Interval(60, 60),
         Interval(78, 86), Interval(61, 63), Interval(31, 33), Interval(26, 32), Interval(18, 22)],
        # Job 9
        [Interval(74, 78), Interval(76, 80), Interval(78, 78), Interval(37, 47), Interval(3, 3),
         Interval(29, 31), Interval(7, 7), Interval(71, 93), Interval(58, 66), Interval(13, 13),
         Interval(81, 87), Interval(19, 25), Interval(73, 83), Interval(72, 88), Interval(50, 66),
         Interval(52, 54), Interval(6, 6), Interval(73, 97), Interval(23, 23), Interval(86, 112)],
        # Job 10
        [Interval(73, 93), Interval(9, 9), Interval(66, 78), Interval(86, 90), Interval(81, 87),
         Interval(86, 88), Interval(74, 82), Interval(62, 68), Interval(20, 26), Interval(7, 7),
         Interval(30, 40), Interval(82, 106), Interval(33, 33), Interval(10, 10), Interval(6, 6),
         Interval(82, 88), Interval(80, 96), Interval(18, 18), Interval(82, 106), Interval(84, 100)],
        # Job 11
        [Interval(26, 30), Interval(31, 35), Interval(80, 106), Interval(11, 11), Interval(23, 27),
         Interval(65, 69), Interval(43, 45), Interval(28, 28), Interval(60, 78), Interval(67, 67),
         Interval(8, 10), Interval(78, 86), Interval(42, 44), Interval(48, 58), Interval(47, 49),
         Interval(38, 40), Interval(45, 59), Interval(75, 75), Interval(77, 85), Interval(43, 45)],
        # Job 12
        [Interval(22, 26), Interval(38, 50), Interval(53, 63), Interval(65, 81), Interval(27, 33),
         Interval(24, 26), Interval(20, 22), Interval(14, 14), Interval(6, 6), Interval(36, 46),
         Interval(17, 21), Interval(19, 23), Interval(35, 37), Interval(63, 81), Interval(83, 109),
         Interval(29, 35), Interval(5, 5), Interval(43, 49), Interval(61, 61), Interval(71, 93)],
        # Job 13
        [Interval(85, 97), Interval(41, 43), Interval(89, 105), Interval(63, 67), Interval(74, 82),
         Interval(35, 45), Interval(88, 98), Interval(61, 67), Interval(8, 8), Interval(49, 63),
         Interval(10, 10), Interval(83, 103), Interval(24, 32), Interval(68, 86), Interval(78, 96),
         Interval(26, 26), Interval(33, 33), Interval(16, 18), Interval(2, 2), Interval(31, 39)],
        # Job 14
        [Interval(14, 16), Interval(45, 45), Interval(96, 96), Interval(11, 11), Interval(87, 103),
         Interval(35, 43), Interval(19, 25), Interval(69, 77), Interval(76, 82), Interval(56, 72),
         Interval(73, 85), Interval(76, 100), Interval(60, 70), Interval(24, 24), Interval(38, 38),
         Interval(17, 17), Interval(3, 3), Interval(63, 83), Interval(59, 59), Interval(90, 94)],
        # Job 15
        [Interval(3, 3), Interval(26, 30), Interval(17, 17), Interval(61, 81), Interval(78, 104),
         Interval(16, 18), Interval(66, 72), Interval(66, 72), Interval(49, 53), Interval(35, 45),
         Interval(88, 98), Interval(82, 82), Interval(42, 52), Interval(42, 42), Interval(51, 67),
         Interval(7, 7), Interval(43, 43), Interval(82, 84), Interval(44, 46), Interval(74, 92)],
        # Job 16
        [Interval(60, 74), Interval(9, 9), Interval(37, 37), Interval(56, 68), Interval(82, 82),
         Interval(63, 75), Interval(29, 39), Interval(35, 43), Interval(13, 17), Interval(73, 95),
         Interval(29, 35), Interval(69, 75), Interval(67, 69), Interval(88, 102), Interval(63, 77),
         Interval(76, 84), Interval(68, 88), Interval(73, 87), Interval(29, 31), Interval(40, 48)],
        # Job 17
        [Interval(12, 14), Interval(95, 97), Interval(24, 28), Interval(4, 4), Interval(88, 90),
         Interval(85, 111), Interval(72, 94), Interval(8, 8), Interval(70, 70), Interval(63, 73),
         Interval(34, 40), Interval(20, 20), Interval(35, 35), Interval(96, 102), Interval(25, 29),
         Interval(12, 12), Interval(73, 73), Interval(86, 98), Interval(94, 102), Interval(71, 79)],
        # Job 18
        [Interval(71, 79), Interval(1, 1), Interval(35, 35), Interval(72, 74), Interval(32, 38),
         Interval(6, 6), Interval(37, 39), Interval(30, 38), Interval(62, 78), Interval(49, 53),
         Interval(16, 16), Interval(67, 89), Interval(57, 59), Interval(9, 9), Interval(97, 97),
         Interval(53, 57), Interval(33, 43), Interval(61, 69), Interval(1, 1), Interval(8, 8)],
        # Job 19
        [Interval(25, 29), Interval(34, 38), Interval(46, 54), Interval(20, 22), Interval(32, 32),
         Interval(6, 6), Interval(34, 34), Interval(73, 95), Interval(45, 55), Interval(38, 40),
         Interval(4, 4), Interval(83, 105), Interval(43, 55), Interval(19, 21), Interval(86, 110),
         Interval(56, 72), Interval(40, 42), Interval(29, 29), Interval(4, 4), Interval(90, 90)],
    ],
    'name': 'INT__TAI20_20_04.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai20_20_04_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI20_20_04.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI20_20_04.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI20_20_04_F_15_01_INTERVAL_DATA
