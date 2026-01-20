"""
Problema INT__TAI30_15_03.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI30_15_03_F_15_01_INTERVAL_DATA = {
    'num_jobs': 30,
    'num_machines': 15,
    'problem_id': 'int__tai30_15_03.F.15_01_interval',
    'sequences': [
        [10, 11, 9, 8, 1, 7, 6, 2, 5, 13, 4, 14, 0, 12, 3],
        [12, 8, 14, 3, 1, 7, 13, 6, 10, 5, 4, 2, 9, 11, 0],
        [12, 0, 3, 13, 14, 10, 2, 6, 9, 1, 11, 4, 5, 7, 8],
        [14, 3, 7, 2, 6, 5, 10, 8, 11, 1, 0, 9, 13, 12, 4],
        [6, 5, 7, 4, 9, 3, 13, 10, 1, 0, 14, 11, 8, 12, 2],
        [7, 11, 12, 9, 8, 2, 3, 5, 4, 1, 10, 0, 6, 13, 14],
        [11, 12, 1, 7, 14, 6, 3, 5, 8, 9, 13, 4, 10, 0, 2],
        [3, 9, 11, 14, 2, 13, 12, 10, 6, 7, 0, 1, 4, 5, 8],
        [9, 2, 3, 13, 10, 14, 12, 1, 7, 0, 6, 8, 11, 4, 5],
        [0, 7, 3, 14, 4, 8, 13, 2, 1, 9, 12, 5, 6, 10, 11],
        [2, 12, 0, 4, 14, 10, 8, 13, 7, 3, 6, 9, 5, 1, 11],
        [5, 2, 8, 6, 4, 12, 9, 1, 10, 0, 14, 7, 13, 11, 3],
        [14, 5, 0, 3, 7, 1, 4, 8, 2, 12, 11, 13, 9, 10, 6],
        [5, 2, 14, 6, 12, 4, 10, 9, 3, 8, 13, 7, 1, 0, 11],
        [4, 9, 0, 6, 1, 10, 13, 3, 2, 12, 5, 11, 7, 8, 14],
        [2, 5, 12, 4, 1, 7, 6, 14, 3, 8, 13, 10, 9, 0, 11],
        [6, 10, 1, 8, 12, 2, 11, 9, 14, 5, 0, 7, 13, 3, 4],
        [2, 0, 4, 10, 3, 5, 7, 12, 14, 13, 11, 9, 8, 1, 6],
        [5, 6, 8, 0, 10, 11, 13, 14, 7, 2, 12, 1, 4, 9, 3],
        [13, 8, 11, 7, 9, 10, 3, 14, 4, 12, 1, 6, 2, 5, 0],
        [1, 6, 14, 3, 12, 10, 7, 13, 5, 0, 4, 11, 9, 2, 8],
        [7, 11, 0, 10, 1, 2, 5, 4, 3, 9, 14, 8, 6, 12, 13],
        [6, 7, 12, 13, 11, 3, 8, 1, 10, 9, 0, 5, 2, 14, 4],
        [4, 6, 1, 10, 12, 9, 14, 7, 11, 0, 5, 3, 13, 8, 2],
        [7, 2, 10, 9, 5, 3, 1, 13, 11, 8, 4, 14, 12, 6, 0],
        [3, 4, 12, 0, 7, 11, 10, 2, 13, 5, 8, 6, 14, 9, 1],
        [11, 12, 0, 13, 6, 2, 1, 9, 5, 7, 3, 10, 4, 14, 8],
        [0, 9, 8, 12, 3, 14, 10, 7, 2, 1, 6, 11, 4, 5, 13],
        [4, 2, 7, 11, 6, 3, 1, 10, 8, 9, 13, 0, 12, 14, 5],
        [14, 6, 2, 8, 10, 4, 11, 13, 12, 7, 3, 5, 1, 0, 9],
    ],
    'durations': [
        # Job 0
        [Interval(31, 41), Interval(30, 34), Interval(38, 42), Interval(47, 47), Interval(75, 99),
         Interval(50, 60), Interval(72, 82), Interval(24, 30), Interval(80, 98), Interval(71, 73),
         Interval(83, 103), Interval(15, 15), Interval(84, 112), Interval(84, 106), Interval(32, 32)],
        # Job 1
        [Interval(7, 7), Interval(36, 48), Interval(80, 88), Interval(65, 87), Interval(40, 48),
         Interval(62, 70), Interval(44, 50), Interval(70, 74), Interval(22, 26), Interval(59, 77),
         Interval(5, 5), Interval(31, 39), Interval(12, 14), Interval(55, 55), Interval(73, 73)],
        # Job 2
        [Interval(55, 63), Interval(6, 8), Interval(76, 94), Interval(55, 59), Interval(90, 106),
         Interval(61, 81), Interval(53, 69), Interval(85, 111), Interval(3, 3), Interval(55, 67),
         Interval(11, 13), Interval(42, 46), Interval(7, 7), Interval(26, 30), Interval(3, 3)],
        # Job 3
        [Interval(16, 16), Interval(3, 3), Interval(83, 111), Interval(25, 29), Interval(92, 102),
         Interval(93, 93), Interval(19, 19), Interval(9, 9), Interval(64, 76), Interval(18, 20),
         Interval(85, 99), Interval(25, 29), Interval(72, 80), Interval(1, 1), Interval(4, 4)],
        # Job 4
        [Interval(68, 74), Interval(51, 55), Interval(31, 41), Interval(63, 63), Interval(16, 16),
         Interval(32, 38), Interval(24, 30), Interval(32, 40), Interval(76, 82), Interval(79, 105),
         Interval(22, 24), Interval(60, 60), Interval(42, 56), Interval(49, 55), Interval(18, 20)],
        # Job 5
        [Interval(46, 50), Interval(77, 99), Interval(66, 70), Interval(6, 6), Interval(60, 66),
         Interval(25, 25), Interval(24, 32), Interval(58, 76), Interval(55, 69), Interval(49, 57),
         Interval(47, 55), Interval(61, 69), Interval(84, 110), Interval(13, 17), Interval(68, 90)],
        # Job 6
        [Interval(43, 55), Interval(64, 66), Interval(23, 29), Interval(72, 72), Interval(55, 65),
         Interval(14, 16), Interval(61, 79), Interval(23, 29), Interval(68, 74), Interval(46, 50),
         Interval(79, 79), Interval(52, 56), Interval(95, 101), Interval(73, 89), Interval(38, 48)],
        # Job 7
        [Interval(33, 37), Interval(26, 30), Interval(85, 91), Interval(52, 64), Interval(79, 95),
         Interval(18, 18), Interval(5, 5), Interval(68, 80), Interval(39, 47), Interval(26, 30),
         Interval(75, 89), Interval(32, 36), Interval(27, 29), Interval(94, 102), Interval(68, 78)],
        # Job 8
        [Interval(80, 86), Interval(83, 103), Interval(81, 91), Interval(58, 66), Interval(18, 18),
         Interval(63, 77), Interval(67, 67), Interval(63, 69), Interval(14, 14), Interval(53, 71),
         Interval(46, 48), Interval(51, 51), Interval(89, 91), Interval(2, 2), Interval(90, 106)],
        # Job 9
        [Interval(28, 28), Interval(86, 102), Interval(6, 6), Interval(63, 69), Interval(77, 81),
         Interval(69, 73), Interval(34, 36), Interval(56, 58), Interval(68, 70), Interval(69, 81),
         Interval(79, 89), Interval(42, 52), Interval(21, 21), Interval(59, 73), Interval(61, 71)],
        # Job 10
        [Interval(17, 23), Interval(54, 70), Interval(34, 40), Interval(66, 76), Interval(17, 21),
         Interval(60, 66), Interval(88, 92), Interval(68, 90), Interval(85, 89), Interval(36, 44),
         Interval(85, 99), Interval(15, 15), Interval(5, 5), Interval(75, 77), Interval(43, 47)],
        # Job 11
        [Interval(71, 71), Interval(56, 62), Interval(93, 105), Interval(70, 70), Interval(23, 31),
         Interval(53, 55), Interval(72, 92), Interval(58, 66), Interval(6, 8), Interval(5, 5),
         Interval(12, 12), Interval(84, 96), Interval(80, 104), Interval(74, 92), Interval(61, 81)],
        # Job 12
        [Interval(90, 90), Interval(76, 82), Interval(47, 49), Interval(61, 71), Interval(81, 91),
         Interval(77, 97), Interval(3, 3), Interval(42, 56), Interval(73, 95), Interval(86, 110),
         Interval(46, 46), Interval(52, 64), Interval(73, 75), Interval(11, 11), Interval(19, 23)],
        # Job 13
        [Interval(55, 57), Interval(46, 52), Interval(83, 103), Interval(11, 11), Interval(5, 5),
         Interval(31, 33), Interval(17, 21), Interval(95, 97), Interval(6, 8), Interval(80, 80),
         Interval(94, 98), Interval(15, 19), Interval(22, 22), Interval(41, 49), Interval(80, 88)],
        # Job 14
        [Interval(91, 95), Interval(16, 20), Interval(22, 28), Interval(64, 74), Interval(62, 68),
         Interval(34, 46), Interval(79, 91), Interval(18, 20), Interval(82, 94), Interval(70, 86),
         Interval(30, 40), Interval(46, 60), Interval(44, 48), Interval(70, 76), Interval(16, 16)],
        # Job 15
        [Interval(34, 38), Interval(16, 20), Interval(33, 39), Interval(30, 38), Interval(61, 67),
         Interval(73, 87), Interval(76, 98), Interval(40, 40), Interval(35, 43), Interval(54, 72),
         Interval(42, 42), Interval(68, 80), Interval(29, 39), Interval(85, 89), Interval(49, 49)],
        # Job 16
        [Interval(74, 94), Interval(76, 82), Interval(61, 65), Interval(13, 17), Interval(63, 83),
         Interval(1, 1), Interval(52, 64), Interval(26, 28), Interval(67, 67), Interval(73, 89),
         Interval(16, 20), Interval(32, 38), Interval(48, 56), Interval(32, 36), Interval(83, 107)],
        # Job 17
        [Interval(57, 71), Interval(42, 54), Interval(82, 82), Interval(1, 1), Interval(10, 12),
         Interval(19, 19), Interval(27, 27), Interval(91, 95), Interval(40, 44), Interval(78, 88),
         Interval(12, 12), Interval(35, 39), Interval(52, 58), Interval(60, 72), Interval(39, 45)],
        # Job 18
        [Interval(73, 81), Interval(13, 13), Interval(55, 55), Interval(14, 16), Interval(64, 80),
         Interval(17, 23), Interval(68, 74), Interval(43, 47), Interval(34, 44), Interval(57, 65),
         Interval(70, 76), Interval(86, 100), Interval(29, 39), Interval(54, 70), Interval(59, 73)],
        # Job 19
        [Interval(65, 71), Interval(15, 15), Interval(91, 103), Interval(75, 95), Interval(76, 86),
         Interval(49, 57), Interval(45, 53), Interval(60, 80), Interval(89, 103), Interval(56, 74),
         Interval(62, 82), Interval(73, 79), Interval(66, 76), Interval(79, 83), Interval(69, 85)],
        # Job 20
        [Interval(56, 68), Interval(75, 93), Interval(51, 65), Interval(33, 39), Interval(62, 64),
         Interval(60, 78), Interval(9, 11), Interval(45, 57), Interval(34, 34), Interval(24, 30),
         Interval(18, 20), Interval(92, 104), Interval(21, 21), Interval(15, 17), Interval(22, 24)],
        # Job 21
        [Interval(55, 65), Interval(17, 17), Interval(78, 100), Interval(80, 94), Interval(50, 54),
         Interval(79, 81), Interval(15, 19), Interval(29, 31), Interval(71, 93), Interval(44, 56),
         Interval(49, 57), Interval(76, 80), Interval(60, 78), Interval(69, 85), Interval(66, 68)],
        # Job 22
        [Interval(51, 61), Interval(37, 43), Interval(28, 36), Interval(32, 42), Interval(32, 42),
         Interval(12, 12), Interval(10, 12), Interval(33, 39), Interval(82, 88), Interval(78, 100),
         Interval(79, 91), Interval(28, 36), Interval(62, 70), Interval(93, 103), Interval(73, 85)],
        # Job 23
        [Interval(32, 32), Interval(55, 57), Interval(20, 24), Interval(90, 100), Interval(49, 61),
         Interval(19, 21), Interval(41, 51), Interval(8, 8), Interval(67, 69), Interval(49, 49),
         Interval(76, 96), Interval(92, 92), Interval(22, 28), Interval(24, 24), Interval(13, 13)],
        # Job 24
        [Interval(52, 54), Interval(1, 1), Interval(85, 99), Interval(63, 67), Interval(10, 10),
         Interval(79, 105), Interval(85, 99), Interval(43, 53), Interval(39, 39), Interval(46, 60),
         Interval(46, 52), Interval(26, 26), Interval(75, 75), Interval(83, 85), Interval(2, 2)],
        # Job 25
        [Interval(13, 15), Interval(60, 74), Interval(82, 86), Interval(30, 32), Interval(54, 68),
         Interval(57, 69), Interval(22, 26), Interval(50, 52), Interval(22, 22), Interval(30, 36),
         Interval(46, 62), Interval(8, 8), Interval(38, 38), Interval(6, 8), Interval(62, 72)],
        # Job 26
        [Interval(59, 77), Interval(9, 11), Interval(47, 63), Interval(28, 32), Interval(25, 27),
         Interval(16, 18), Interval(4, 4), Interval(92, 104), Interval(49, 61), Interval(39, 51),
         Interval(24, 30), Interval(72, 80), Interval(84, 108), Interval(62, 68), Interval(60, 60)],
        # Job 27
        [Interval(8, 10), Interval(22, 26), Interval(21, 23), Interval(40, 40), Interval(47, 47),
         Interval(66, 80), Interval(71, 73), Interval(69, 71), Interval(61, 71), Interval(17, 21),
         Interval(3, 3), Interval(91, 103), Interval(95, 101), Interval(77, 93), Interval(51, 51)],
        # Job 28
        [Interval(47, 61), Interval(19, 19), Interval(66, 78), Interval(34, 42), Interval(16, 20),
         Interval(80, 88), Interval(66, 76), Interval(73, 87), Interval(42, 50), Interval(25, 25),
         Interval(27, 31), Interval(49, 65), Interval(86, 98), Interval(41, 41), Interval(73, 77)],
        # Job 29
        [Interval(16, 16), Interval(72, 86), Interval(49, 57), Interval(89, 107), Interval(8, 8),
         Interval(20, 20), Interval(2, 2), Interval(57, 71), Interval(54, 68), Interval(68, 88),
         Interval(79, 103), Interval(34, 36), Interval(53, 57), Interval(82, 102), Interval(76, 80)],
    ],
    'name': 'INT__TAI30_15_03.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai30_15_03_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI30_15_03.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI30_15_03.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI30_15_03_F_15_01_INTERVAL_DATA
