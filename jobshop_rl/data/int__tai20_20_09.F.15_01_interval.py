"""
Problema INT__TAI20_20_09.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI20_20_09_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 20,
    'problem_id': 'int__tai20_20_09.F.15_01_interval',
    'sequences': [
        [10, 9, 16, 18, 17, 5, 14, 2, 13, 19, 12, 3, 8, 4, 1, 15, 0, 6, 11, 7],
        [4, 19, 5, 6, 2, 7, 16, 12, 9, 11, 8, 13, 14, 3, 1, 15, 18, 17, 0, 10],
        [10, 3, 14, 0, 16, 1, 2, 5, 7, 15, 17, 13, 19, 4, 11, 12, 9, 18, 8, 6],
        [1, 8, 17, 11, 0, 10, 12, 5, 13, 4, 6, 3, 15, 7, 16, 14, 9, 2, 19, 18],
        [13, 16, 18, 10, 15, 4, 14, 5, 19, 2, 17, 0, 6, 7, 3, 1, 9, 12, 11, 8],
        [5, 7, 15, 19, 17, 4, 12, 2, 3, 18, 8, 13, 0, 9, 14, 10, 11, 6, 1, 16],
        [10, 3, 12, 8, 9, 16, 19, 6, 13, 11, 17, 0, 14, 18, 1, 4, 15, 5, 7, 2],
        [4, 14, 18, 3, 16, 7, 9, 10, 17, 11, 15, 0, 5, 6, 19, 13, 12, 1, 8, 2],
        [8, 4, 7, 5, 9, 19, 3, 0, 13, 14, 11, 17, 16, 10, 1, 2, 12, 6, 18, 15],
        [11, 19, 12, 4, 18, 6, 8, 13, 15, 2, 0, 1, 3, 17, 16, 10, 5, 9, 7, 14],
        [0, 17, 1, 18, 13, 12, 6, 7, 2, 5, 15, 10, 11, 9, 19, 16, 4, 14, 3, 8],
        [0, 10, 5, 8, 2, 1, 15, 7, 18, 3, 12, 13, 9, 17, 19, 11, 16, 6, 14, 4],
        [16, 13, 4, 19, 18, 6, 10, 5, 9, 17, 1, 12, 14, 8, 15, 11, 3, 0, 7, 2],
        [17, 13, 4, 12, 7, 0, 11, 3, 2, 8, 16, 18, 1, 6, 14, 15, 10, 19, 5, 9],
        [12, 10, 16, 5, 9, 0, 6, 18, 1, 2, 15, 11, 14, 3, 8, 7, 13, 19, 17, 4],
        [7, 1, 4, 13, 16, 12, 9, 3, 14, 18, 0, 10, 5, 17, 8, 2, 19, 6, 15, 11],
        [14, 8, 18, 17, 15, 19, 3, 12, 16, 0, 2, 1, 13, 5, 10, 11, 9, 7, 6, 4],
        [8, 9, 15, 7, 5, 1, 0, 18, 14, 2, 6, 12, 17, 4, 10, 19, 11, 13, 16, 3],
        [16, 4, 15, 14, 8, 7, 18, 19, 12, 5, 6, 9, 1, 2, 13, 3, 0, 11, 17, 10],
        [4, 8, 2, 14, 15, 6, 13, 17, 12, 9, 7, 5, 3, 1, 0, 11, 19, 10, 18, 16],
    ],
    'durations': [
        # Job 0
        [Interval(73, 95), Interval(41, 49), Interval(52, 54), Interval(42, 54), Interval(8, 10),
         Interval(9, 9), Interval(37, 41), Interval(73, 85), Interval(74, 92), Interval(44, 56),
         Interval(24, 24), Interval(46, 52), Interval(73, 89), Interval(5, 5), Interval(61, 79),
         Interval(82, 96), Interval(83, 99), Interval(25, 25), Interval(74, 86), Interval(36, 36)],
        # Job 1
        [Interval(68, 82), Interval(42, 54), Interval(6, 6), Interval(32, 32), Interval(62, 74),
         Interval(21, 25), Interval(38, 50), Interval(19, 23), Interval(37, 47), Interval(13, 13),
         Interval(73, 75), Interval(30, 32), Interval(59, 65), Interval(87, 95), Interval(64, 66),
         Interval(64, 68), Interval(24, 28), Interval(88, 104), Interval(89, 105), Interval(48, 54)],
        # Job 2
        [Interval(47, 51), Interval(23, 29), Interval(33, 37), Interval(60, 68), Interval(48, 62),
         Interval(69, 87), Interval(71, 73), Interval(76, 90), Interval(57, 61), Interval(15, 17),
         Interval(90, 94), Interval(65, 71), Interval(57, 71), Interval(4, 4), Interval(71, 81),
         Interval(79, 85), Interval(61, 79), Interval(67, 83), Interval(58, 72), Interval(27, 35)],
        # Job 3
        [Interval(49, 61), Interval(50, 66), Interval(36, 38), Interval(30, 34), Interval(31, 31),
         Interval(65, 65), Interval(63, 67), Interval(80, 90), Interval(50, 50), Interval(88, 100),
         Interval(37, 37), Interval(18, 22), Interval(81, 107), Interval(18, 22), Interval(30, 32),
         Interval(30, 30), Interval(45, 53), Interval(8, 8), Interval(22, 22), Interval(45, 49)],
        # Job 4
        [Interval(81, 81), Interval(59, 77), Interval(2, 2), Interval(64, 74), Interval(37, 39),
         Interval(7, 7), Interval(80, 82), Interval(70, 88), Interval(76, 76), Interval(92, 96),
         Interval(63, 67), Interval(11, 11), Interval(91, 105), Interval(38, 38), Interval(90, 100),
         Interval(91, 95), Interval(9, 9), Interval(20, 22), Interval(16, 18), Interval(71, 87)],
        # Job 5
        [Interval(60, 68), Interval(7, 7), Interval(92, 96), Interval(29, 29), Interval(76, 78),
         Interval(72, 78), Interval(46, 54), Interval(78, 78), Interval(57, 57), Interval(29, 29),
         Interval(65, 67), Interval(84, 102), Interval(69, 79), Interval(67, 79), Interval(73, 87),
         Interval(8, 8), Interval(26, 26), Interval(85, 89), Interval(59, 79), Interval(78, 92)],
        # Job 6
        [Interval(44, 54), Interval(52, 66), Interval(87, 95), Interval(51, 67), Interval(24, 26),
         Interval(40, 48), Interval(45, 55), Interval(37, 45), Interval(29, 37), Interval(83, 95),
         Interval(73, 85), Interval(3, 3), Interval(54, 54), Interval(79, 85), Interval(54, 72),
         Interval(30, 32), Interval(14, 16), Interval(2, 2), Interval(61, 73), Interval(61, 81)],
        # Job 7
        [Interval(4, 4), Interval(19, 21), Interval(23, 23), Interval(30, 36), Interval(60, 70),
         Interval(42, 46), Interval(56, 58), Interval(20, 20), Interval(81, 105), Interval(22, 24),
         Interval(17, 19), Interval(8, 8), Interval(66, 78), Interval(53, 55), Interval(16, 20),
         Interval(85, 101), Interval(43, 43), Interval(16, 20), Interval(55, 57), Interval(21, 21)],
        # Job 8
        [Interval(58, 58), Interval(25, 25), Interval(34, 34), Interval(87, 91), Interval(50, 58),
         Interval(81, 97), Interval(11, 13), Interval(51, 51), Interval(71, 77), Interval(76, 80),
         Interval(4, 4), Interval(69, 75), Interval(75, 87), Interval(81, 103), Interval(60, 78),
         Interval(35, 35), Interval(25, 25), Interval(35, 35), Interval(9, 11), Interval(30, 36)],
        # Job 9
        [Interval(30, 36), Interval(77, 91), Interval(65, 85), Interval(62, 70), Interval(46, 52),
         Interval(67, 87), Interval(87, 87), Interval(44, 44), Interval(35, 39), Interval(61, 73),
         Interval(30, 36), Interval(65, 85), Interval(62, 68), Interval(40, 48), Interval(59, 73),
         Interval(43, 47), Interval(86, 100), Interval(88, 108), Interval(20, 24), Interval(66, 68)],
        # Job 10
        [Interval(17, 17), Interval(26, 26), Interval(54, 54), Interval(23, 27), Interval(79, 105),
         Interval(33, 35), Interval(43, 51), Interval(71, 89), Interval(23, 25), Interval(83, 101),
         Interval(64, 86), Interval(60, 76), Interval(76, 92), Interval(69, 75), Interval(79, 89),
         Interval(92, 96), Interval(66, 72), Interval(91, 101), Interval(34, 34), Interval(29, 29)],
        # Job 11
        [Interval(65, 67), Interval(75, 83), Interval(73, 75), Interval(66, 68), Interval(72, 72),
         Interval(22, 22), Interval(45, 55), Interval(27, 33), Interval(43, 51), Interval(70, 80),
         Interval(41, 45), Interval(40, 48), Interval(70, 72), Interval(55, 67), Interval(47, 61),
         Interval(87, 111), Interval(11, 11), Interval(84, 110), Interval(73, 77), Interval(72, 90)],
        # Job 12
        [Interval(32, 38), Interval(68, 82), Interval(95, 103), Interval(66, 78), Interval(86, 98),
         Interval(83, 97), Interval(26, 26), Interval(83, 99), Interval(63, 77), Interval(82, 82),
         Interval(12, 14), Interval(40, 50), Interval(71, 93), Interval(53, 63), Interval(34, 42),
         Interval(18, 20), Interval(58, 74), Interval(23, 23), Interval(49, 49), Interval(18, 20)],
        # Job 13
        [Interval(81, 83), Interval(65, 83), Interval(39, 41), Interval(29, 37), Interval(9, 9),
         Interval(33, 33), Interval(25, 27), Interval(40, 48), Interval(16, 20), Interval(67, 79),
         Interval(37, 45), Interval(87, 105), Interval(39, 39), Interval(88, 94), Interval(86, 92),
         Interval(11, 11), Interval(1, 1), Interval(2, 2), Interval(63, 75), Interval(10, 10)],
        # Job 14
        [Interval(23, 27), Interval(29, 35), Interval(40, 42), Interval(14, 14), Interval(62, 72),
         Interval(24, 26), Interval(90, 98), Interval(84, 94), Interval(19, 23), Interval(92, 104),
         Interval(81, 103), Interval(62, 82), Interval(52, 62), Interval(4, 4), Interval(1, 1),
         Interval(2, 2), Interval(82, 86), Interval(87, 95), Interval(41, 43), Interval(84, 86)],
        # Job 15
        [Interval(27, 31), Interval(96, 100), Interval(41, 41), Interval(79, 95), Interval(51, 53),
         Interval(9, 9), Interval(20, 24), Interval(2, 2), Interval(77, 81), Interval(73, 73),
         Interval(15, 17), Interval(20, 24), Interval(91, 103), Interval(12, 14), Interval(19, 19),
         Interval(12, 14), Interval(46, 54), Interval(43, 43), Interval(88, 94), Interval(34, 34)],
        # Job 16
        [Interval(88, 94), Interval(39, 43), Interval(42, 52), Interval(57, 65), Interval(61, 71),
         Interval(28, 34), Interval(87, 97), Interval(42, 42), Interval(19, 19), Interval(87, 109),
         Interval(35, 37), Interval(28, 30), Interval(8, 8), Interval(22, 28), Interval(5, 5),
         Interval(86, 94), Interval(59, 65), Interval(62, 64), Interval(16, 18), Interval(21, 25)],
        # Job 17
        [Interval(68, 70), Interval(77, 79), Interval(57, 65), Interval(51, 53), Interval(38, 42),
         Interval(70, 72), Interval(40, 40), Interval(55, 67), Interval(87, 99), Interval(36, 38),
         Interval(29, 35), Interval(47, 49), Interval(6, 8), Interval(36, 38), Interval(65, 73),
         Interval(4, 4), Interval(75, 83), Interval(71, 91), Interval(10, 10), Interval(67, 83)],
        # Job 18
        [Interval(86, 94), Interval(16, 16), Interval(63, 73), Interval(32, 32), Interval(91, 101),
         Interval(7, 7), Interval(37, 47), Interval(46, 58), Interval(34, 42), Interval(62, 74),
         Interval(68, 76), Interval(73, 83), Interval(9, 11), Interval(54, 68), Interval(37, 43),
         Interval(31, 31), Interval(72, 90), Interval(68, 70), Interval(76, 92), Interval(26, 28)],
        # Job 19
        [Interval(83, 99), Interval(16, 18), Interval(71, 79), Interval(7, 7), Interval(44, 44),
         Interval(9, 11), Interval(30, 34), Interval(73, 83), Interval(9, 9), Interval(65, 73),
         Interval(42, 48), Interval(83, 91), Interval(77, 103), Interval(47, 53), Interval(38, 46),
         Interval(2, 2), Interval(19, 23), Interval(57, 67), Interval(90, 96), Interval(84, 92)],
    ],
    'name': 'INT__TAI20_20_09.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai20_20_09_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI20_20_09.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI20_20_09.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI20_20_09_F_15_01_INTERVAL_DATA
