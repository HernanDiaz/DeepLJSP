"""
Problema INT__TAI30_15_06.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI30_15_06_F_15_01_INTERVAL_DATA = {
    'num_jobs': 30,
    'num_machines': 15,
    'problem_id': 'int__tai30_15_06.F.15_01_interval',
    'sequences': [
        [2, 13, 9, 1, 4, 0, 14, 12, 6, 11, 5, 7, 3, 8, 10],
        [3, 11, 14, 1, 5, 0, 8, 10, 2, 4, 6, 9, 12, 13, 7],
        [2, 8, 6, 5, 4, 7, 0, 14, 11, 1, 10, 12, 3, 13, 9],
        [6, 0, 8, 7, 4, 9, 2, 14, 12, 10, 11, 1, 3, 5, 13],
        [12, 3, 5, 0, 10, 11, 13, 6, 7, 4, 8, 2, 1, 14, 9],
        [11, 1, 3, 0, 5, 8, 7, 10, 4, 2, 6, 9, 12, 14, 13],
        [10, 1, 11, 5, 9, 4, 13, 3, 7, 0, 8, 6, 14, 12, 2],
        [12, 1, 4, 5, 13, 9, 2, 14, 7, 3, 11, 8, 6, 10, 0],
        [10, 14, 11, 9, 4, 0, 3, 2, 6, 8, 5, 13, 7, 1, 12],
        [14, 2, 3, 1, 5, 9, 10, 4, 11, 0, 8, 7, 6, 13, 12],
        [7, 6, 12, 1, 2, 11, 3, 14, 4, 13, 5, 0, 8, 9, 10],
        [14, 3, 13, 0, 7, 12, 6, 1, 11, 10, 2, 8, 9, 4, 5],
        [3, 11, 13, 8, 2, 1, 10, 14, 4, 9, 12, 5, 6, 0, 7],
        [8, 0, 13, 1, 6, 14, 10, 4, 5, 11, 2, 9, 7, 12, 3],
        [5, 12, 4, 6, 14, 8, 3, 7, 13, 9, 1, 10, 2, 11, 0],
        [2, 5, 12, 11, 1, 4, 7, 14, 0, 9, 8, 6, 3, 13, 10],
        [10, 3, 1, 4, 7, 5, 2, 0, 14, 12, 8, 6, 13, 9, 11],
        [2, 6, 13, 4, 3, 8, 7, 5, 14, 10, 9, 12, 1, 11, 0],
        [2, 0, 6, 11, 5, 12, 7, 14, 13, 4, 3, 1, 10, 8, 9],
        [6, 5, 2, 3, 0, 7, 10, 1, 14, 4, 8, 13, 9, 11, 12],
        [5, 13, 2, 14, 11, 0, 6, 4, 1, 9, 7, 10, 12, 3, 8],
        [12, 6, 0, 14, 9, 10, 5, 4, 7, 3, 8, 13, 11, 1, 2],
        [1, 5, 10, 4, 12, 3, 0, 7, 8, 14, 9, 13, 11, 2, 6],
        [13, 3, 8, 2, 14, 6, 10, 7, 9, 1, 4, 0, 5, 11, 12],
        [8, 1, 3, 12, 0, 2, 4, 6, 14, 9, 13, 11, 5, 7, 10],
        [2, 0, 7, 5, 11, 8, 13, 1, 14, 9, 4, 10, 6, 12, 3],
        [7, 6, 9, 11, 10, 13, 12, 0, 5, 1, 4, 3, 8, 2, 14],
        [7, 0, 14, 10, 3, 2, 11, 5, 12, 1, 6, 4, 8, 13, 9],
        [10, 14, 5, 1, 6, 4, 13, 8, 2, 11, 0, 9, 12, 3, 7],
        [13, 1, 2, 0, 6, 12, 10, 7, 9, 5, 3, 11, 4, 8, 14],
    ],
    'durations': [
        # Job 0
        [Interval(82, 110), Interval(79, 93), Interval(71, 79), Interval(3, 3), Interval(97, 97),
         Interval(76, 100), Interval(81, 95), Interval(62, 70), Interval(14, 18), Interval(57, 69),
         Interval(72, 74), Interval(3, 3), Interval(56, 70), Interval(91, 91), Interval(29, 37)],
        # Job 1
        [Interval(18, 24), Interval(33, 33), Interval(36, 40), Interval(80, 108), Interval(75, 83),
         Interval(31, 41), Interval(46, 54), Interval(77, 89), Interval(4, 4), Interval(78, 88),
         Interval(7, 7), Interval(24, 28), Interval(76, 98), Interval(13, 17), Interval(80, 100)],
        # Job 2
        [Interval(88, 88), Interval(37, 37), Interval(87, 101), Interval(56, 74), Interval(22, 26),
         Interval(83, 89), Interval(88, 104), Interval(80, 108), Interval(70, 92), Interval(2, 2),
         Interval(81, 105), Interval(5, 5), Interval(21, 25), Interval(39, 51), Interval(11, 11)],
        # Job 3
        [Interval(62, 62), Interval(57, 65), Interval(37, 37), Interval(1, 1), Interval(9, 11),
         Interval(20, 22), Interval(83, 93), Interval(24, 24), Interval(60, 62), Interval(41, 43),
         Interval(49, 59), Interval(86, 98), Interval(4, 4), Interval(35, 41), Interval(8, 10)],
        # Job 4
        [Interval(49, 55), Interval(83, 91), Interval(36, 38), Interval(23, 31), Interval(75, 77),
         Interval(69, 69), Interval(69, 83), Interval(65, 83), Interval(77, 95), Interval(45, 47),
         Interval(72, 96), Interval(46, 50), Interval(16, 16), Interval(78, 104), Interval(27, 29)],
        # Job 5
        [Interval(32, 38), Interval(51, 55), Interval(41, 51), Interval(97, 101), Interval(17, 17),
         Interval(77, 79), Interval(72, 96), Interval(77, 99), Interval(53, 67), Interval(49, 57),
         Interval(25, 29), Interval(31, 35), Interval(76, 100), Interval(64, 86), Interval(12, 14)],
        # Job 6
        [Interval(70, 88), Interval(70, 74), Interval(22, 28), Interval(52, 52), Interval(22, 26),
         Interval(89, 107), Interval(4, 4), Interval(87, 111), Interval(15, 19), Interval(50, 54),
         Interval(82, 88), Interval(48, 48), Interval(82, 88), Interval(96, 102), Interval(65, 79)],
        # Job 7
        [Interval(68, 86), Interval(75, 85), Interval(41, 47), Interval(71, 75), Interval(42, 50),
         Interval(54, 66), Interval(25, 25), Interval(61, 73), Interval(17, 19), Interval(16, 18),
         Interval(4, 4), Interval(67, 79), Interval(31, 33), Interval(64, 70), Interval(6, 6)],
        # Job 8
        [Interval(49, 53), Interval(25, 27), Interval(28, 30), Interval(51, 63), Interval(50, 58),
         Interval(15, 17), Interval(40, 42), Interval(2, 2), Interval(13, 17), Interval(88, 88),
         Interval(45, 49), Interval(10, 10), Interval(2, 2), Interval(64, 86), Interval(16, 16)],
        # Job 9
        [Interval(27, 27), Interval(1, 1), Interval(87, 89), Interval(41, 47), Interval(17, 17),
         Interval(18, 22), Interval(48, 52), Interval(39, 41), Interval(39, 41), Interval(63, 67),
         Interval(10, 10), Interval(49, 51), Interval(10, 12), Interval(34, 38), Interval(72, 90)],
        # Job 10
        [Interval(6, 6), Interval(36, 36), Interval(59, 75), Interval(68, 78), Interval(26, 34),
         Interval(85, 109), Interval(57, 67), Interval(10, 12), Interval(71, 89), Interval(24, 26),
         Interval(59, 61), Interval(36, 48), Interval(41, 43), Interval(36, 44), Interval(51, 59)],
        # Job 11
        [Interval(57, 61), Interval(85, 87), Interval(85, 93), Interval(8, 8), Interval(4, 4),
         Interval(15, 17), Interval(63, 71), Interval(43, 43), Interval(63, 85), Interval(95, 99),
         Interval(3, 3), Interval(11, 13), Interval(51, 59), Interval(3, 3), Interval(25, 33)],
        # Job 12
        [Interval(21, 23), Interval(82, 94), Interval(34, 44), Interval(81, 101), Interval(22, 28),
         Interval(23, 23), Interval(37, 39), Interval(14, 14), Interval(67, 77), Interval(82, 92),
         Interval(69, 87), Interval(36, 48), Interval(3, 3), Interval(27, 35), Interval(73, 93)],
        # Job 13
        [Interval(74, 74), Interval(62, 76), Interval(58, 60), Interval(74, 74), Interval(56, 66),
         Interval(81, 85), Interval(77, 87), Interval(38, 48), Interval(42, 42), Interval(41, 45),
         Interval(18, 22), Interval(51, 51), Interval(6, 8), Interval(5, 5), Interval(7, 7)],
        # Job 14
        [Interval(74, 76), Interval(64, 78), Interval(44, 46), Interval(84, 100), Interval(9, 9),
         Interval(47, 49), Interval(18, 22), Interval(24, 32), Interval(23, 27), Interval(13, 15),
         Interval(52, 70), Interval(37, 41), Interval(60, 70), Interval(26, 30), Interval(44, 54)],
        # Job 15
        [Interval(81, 107), Interval(11, 13), Interval(32, 34), Interval(33, 37), Interval(57, 57),
         Interval(32, 34), Interval(19, 25), Interval(42, 52), Interval(76, 98), Interval(45, 49),
         Interval(56, 66), Interval(37, 47), Interval(83, 85), Interval(11, 13), Interval(50, 66)],
        # Job 16
        [Interval(70, 72), Interval(32, 38), Interval(60, 80), Interval(65, 69), Interval(86, 86),
         Interval(37, 47), Interval(69, 75), Interval(51, 53), Interval(63, 83), Interval(38, 50),
         Interval(86, 106), Interval(40, 44), Interval(96, 96), Interval(3, 3), Interval(84, 104)],
        # Job 17
        [Interval(63, 77), Interval(28, 32), Interval(44, 52), Interval(54, 60), Interval(58, 74),
         Interval(84, 106), Interval(83, 107), Interval(17, 17), Interval(57, 71), Interval(70, 70),
         Interval(6, 6), Interval(99, 99), Interval(62, 64), Interval(32, 34), Interval(25, 29)],
        # Job 18
        [Interval(77, 83), Interval(89, 97), Interval(14, 16), Interval(78, 94), Interval(31, 35),
         Interval(61, 69), Interval(42, 46), Interval(22, 22), Interval(79, 93), Interval(82, 104),
         Interval(79, 105), Interval(85, 91), Interval(62, 68), Interval(34, 44), Interval(13, 15)],
        # Job 19
        [Interval(87, 95), Interval(39, 45), Interval(12, 16), Interval(15, 19), Interval(44, 56),
         Interval(16, 16), Interval(2, 2), Interval(35, 37), Interval(44, 50), Interval(10, 12),
         Interval(32, 36), Interval(27, 31), Interval(66, 76), Interval(67, 89), Interval(51, 59)],
        # Job 20
        [Interval(65, 87), Interval(57, 77), Interval(34, 36), Interval(87, 99), Interval(13, 13),
         Interval(52, 64), Interval(22, 26), Interval(9, 11), Interval(6, 6), Interval(42, 56),
         Interval(36, 44), Interval(60, 62), Interval(63, 81), Interval(87, 107), Interval(15, 19)],
        # Job 21
        [Interval(89, 89), Interval(78, 94), Interval(42, 48), Interval(56, 62), Interval(16, 16),
         Interval(50, 54), Interval(37, 41), Interval(77, 89), Interval(11, 11), Interval(49, 63),
         Interval(28, 32), Interval(57, 63), Interval(79, 81), Interval(37, 49), Interval(4, 4)],
        # Job 22
        [Interval(46, 52), Interval(38, 50), Interval(3, 3), Interval(65, 81), Interval(45, 53),
         Interval(62, 64), Interval(17, 23), Interval(61, 75), Interval(39, 41), Interval(34, 40),
         Interval(16, 18), Interval(57, 75), Interval(80, 104), Interval(71, 93), Interval(5, 5)],
        # Job 23
        [Interval(68, 70), Interval(52, 62), Interval(31, 37), Interval(64, 70), Interval(64, 82),
         Interval(56, 64), Interval(81, 105), Interval(1, 1), Interval(40, 46), Interval(64, 70),
         Interval(78, 92), Interval(79, 81), Interval(79, 81), Interval(72, 90), Interval(93, 103)],
        # Job 24
        [Interval(49, 61), Interval(26, 28), Interval(44, 56), Interval(95, 97), Interval(42, 42),
         Interval(75, 77), Interval(29, 37), Interval(82, 82), Interval(72, 92), Interval(87, 87),
         Interval(91, 95), Interval(41, 43), Interval(18, 22), Interval(94, 100), Interval(14, 16)],
        # Job 25
        [Interval(7, 9), Interval(73, 85), Interval(22, 26), Interval(19, 19), Interval(64, 82),
         Interval(77, 87), Interval(47, 47), Interval(89, 91), Interval(95, 99), Interval(86, 100),
         Interval(62, 76), Interval(46, 48), Interval(65, 71), Interval(39, 49), Interval(48, 60)],
        # Job 26
        [Interval(47, 57), Interval(11, 11), Interval(97, 99), Interval(40, 48), Interval(12, 16),
         Interval(36, 40), Interval(57, 57), Interval(45, 55), Interval(37, 43), Interval(77, 101),
         Interval(2, 2), Interval(67, 79), Interval(17, 21), Interval(37, 43), Interval(91, 101)],
        # Job 27
        [Interval(5, 5), Interval(49, 55), Interval(43, 47), Interval(15, 19), Interval(80, 108),
         Interval(40, 48), Interval(9, 9), Interval(16, 20), Interval(35, 39), Interval(84, 84),
         Interval(25, 31), Interval(71, 85), Interval(27, 29), Interval(67, 69), Interval(63, 65)],
        # Job 28
        [Interval(21, 25), Interval(63, 63), Interval(56, 58), Interval(52, 62), Interval(19, 25),
         Interval(67, 75), Interval(67, 71), Interval(14, 16), Interval(19, 19), Interval(77, 99),
         Interval(25, 25), Interval(76, 90), Interval(55, 69), Interval(48, 60), Interval(64, 72)],
        # Job 29
        [Interval(43, 51), Interval(88, 104), Interval(10, 12), Interval(99, 99), Interval(26, 30),
         Interval(7, 9), Interval(47, 53), Interval(18, 18), Interval(95, 99), Interval(10, 10),
         Interval(49, 59), Interval(46, 54), Interval(61, 73), Interval(16, 16), Interval(77, 81)],
    ],
    'name': 'INT__TAI30_15_06.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai30_15_06_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI30_15_06.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI30_15_06.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI30_15_06_F_15_01_INTERVAL_DATA
