"""
Problema INT__TAI20_20_02.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI20_20_02_F_15_01_INTERVAL_DATA = {
    'num_jobs': 20,
    'num_machines': 20,
    'problem_id': 'int__tai20_20_02.F.15_01_interval',
    'sequences': [
        [3, 2, 19, 11, 10, 13, 16, 15, 1, 0, 12, 17, 18, 9, 5, 7, 14, 4, 8, 6],
        [14, 12, 4, 17, 7, 2, 10, 15, 8, 9, 3, 6, 16, 13, 11, 1, 0, 5, 19, 18],
        [18, 17, 0, 13, 7, 1, 11, 19, 5, 3, 2, 16, 15, 4, 8, 14, 9, 12, 10, 6],
        [17, 10, 8, 12, 5, 16, 14, 11, 6, 1, 9, 4, 19, 0, 18, 15, 3, 2, 13, 7],
        [8, 12, 1, 10, 13, 15, 5, 17, 9, 7, 18, 3, 4, 0, 2, 14, 19, 11, 16, 6],
        [6, 0, 9, 16, 14, 18, 17, 10, 2, 13, 11, 7, 19, 1, 8, 3, 4, 15, 12, 5],
        [12, 1, 6, 14, 11, 15, 3, 10, 9, 19, 5, 17, 2, 4, 8, 18, 7, 0, 13, 16],
        [5, 12, 19, 1, 8, 13, 18, 9, 10, 2, 17, 3, 15, 6, 16, 7, 0, 4, 11, 14],
        [2, 8, 3, 10, 16, 15, 0, 17, 7, 13, 5, 14, 12, 9, 19, 6, 18, 11, 4, 1],
        [17, 2, 7, 19, 11, 16, 13, 10, 15, 1, 5, 6, 8, 9, 3, 12, 18, 14, 0, 4],
        [7, 12, 8, 11, 16, 15, 4, 3, 14, 9, 19, 2, 13, 17, 6, 1, 10, 18, 5, 0],
        [4, 17, 11, 16, 15, 18, 14, 19, 6, 7, 5, 10, 13, 0, 3, 9, 2, 8, 1, 12],
        [8, 16, 12, 2, 5, 15, 10, 17, 7, 13, 4, 1, 0, 3, 19, 9, 18, 14, 11, 6],
        [1, 8, 18, 11, 17, 9, 10, 16, 19, 5, 12, 4, 3, 6, 7, 2, 14, 0, 13, 15],
        [13, 7, 4, 0, 19, 2, 14, 3, 11, 17, 16, 10, 1, 9, 12, 6, 15, 8, 5, 18],
        [15, 0, 18, 16, 8, 4, 5, 14, 7, 17, 1, 3, 10, 19, 6, 2, 13, 12, 9, 11],
        [3, 11, 2, 9, 15, 1, 10, 7, 19, 5, 8, 13, 17, 6, 0, 16, 14, 12, 18, 4],
        [17, 6, 11, 5, 16, 4, 12, 9, 18, 0, 10, 14, 7, 3, 15, 1, 8, 19, 2, 13],
        [5, 6, 8, 12, 2, 9, 16, 13, 18, 1, 7, 17, 0, 15, 19, 3, 11, 4, 14, 10],
        [3, 15, 10, 4, 18, 1, 16, 9, 12, 7, 11, 0, 2, 19, 13, 14, 17, 5, 6, 8],
    ],
    'durations': [
        # Job 0
        [Interval(94, 94), Interval(60, 62), Interval(12, 12), Interval(63, 73), Interval(35, 45),
         Interval(73, 95), Interval(30, 30), Interval(14, 18), Interval(34, 34), Interval(89, 95),
         Interval(48, 58), Interval(50, 60), Interval(56, 66), Interval(60, 74), Interval(28, 32),
         Interval(80, 96), Interval(11, 13), Interval(20, 20), Interval(16, 16), Interval(49, 53)],
        # Job 1
        [Interval(21, 23), Interval(73, 77), Interval(26, 32), Interval(80, 94), Interval(44, 50),
         Interval(44, 52), Interval(19, 23), Interval(44, 48), Interval(70, 84), Interval(33, 37),
         Interval(10, 10), Interval(87, 97), Interval(8, 10), Interval(70, 80), Interval(37, 43),
         Interval(86, 92), Interval(82, 90), Interval(31, 35), Interval(2, 2), Interval(1, 1)],
        # Job 2
        [Interval(32, 32), Interval(8, 8), Interval(98, 100), Interval(13, 15), Interval(36, 46),
         Interval(48, 58), Interval(85, 109), Interval(19, 19), Interval(37, 41), Interval(18, 22),
         Interval(86, 96), Interval(49, 59), Interval(84, 110), Interval(71, 87), Interval(20, 22),
         Interval(21, 23), Interval(82, 104), Interval(67, 67), Interval(16, 18), Interval(78, 90)],
        # Job 3
        [Interval(12, 14), Interval(39, 47), Interval(85, 109), Interval(40, 42), Interval(4, 4),
         Interval(32, 38), Interval(6, 6), Interval(83, 103), Interval(29, 35), Interval(31, 39),
         Interval(2, 2), Interval(49, 59), Interval(75, 79), Interval(8, 10), Interval(88, 106),
         Interval(10, 10), Interval(45, 45), Interval(75, 87), Interval(66, 86), Interval(36, 38)],
        # Job 4
        [Interval(23, 29), Interval(67, 73), Interval(29, 37), Interval(51, 65), Interval(34, 42),
         Interval(70, 84), Interval(75, 97), Interval(51, 55), Interval(44, 50), Interval(19, 21),
         Interval(65, 77), Interval(61, 77), Interval(91, 99), Interval(4, 4), Interval(21, 25),
         Interval(77, 101), Interval(76, 98), Interval(20, 20), Interval(64, 70), Interval(61, 69)],
        # Job 5
        [Interval(76, 96), Interval(65, 81), Interval(85, 101), Interval(24, 28), Interval(92, 104),
         Interval(36, 38), Interval(58, 76), Interval(77, 97), Interval(33, 33), Interval(6, 6),
         Interval(64, 72), Interval(15, 17), Interval(12, 12), Interval(5, 5), Interval(30, 36),
         Interval(82, 92), Interval(91, 101), Interval(43, 49), Interval(85, 89), Interval(80, 98)],
        # Job 6
        [Interval(3, 3), Interval(32, 36), Interval(2, 2), Interval(82, 110), Interval(61, 73),
         Interval(37, 37), Interval(28, 32), Interval(47, 53), Interval(81, 87), Interval(26, 28),
         Interval(36, 38), Interval(83, 95), Interval(80, 104), Interval(60, 76), Interval(19, 21),
         Interval(71, 89), Interval(66, 86), Interval(64, 84), Interval(10, 12), Interval(38, 38)],
        # Job 7
        [Interval(56, 64), Interval(85, 109), Interval(41, 43), Interval(63, 83), Interval(25, 31),
         Interval(66, 72), Interval(77, 103), Interval(41, 47), Interval(27, 27), Interval(48, 60),
         Interval(23, 25), Interval(33, 39), Interval(82, 82), Interval(13, 13), Interval(31, 35),
         Interval(78, 82), Interval(40, 48), Interval(87, 111), Interval(69, 91), Interval(76, 88)],
        # Job 8
        [Interval(79, 79), Interval(54, 70), Interval(28, 34), Interval(24, 30), Interval(66, 78),
         Interval(12, 12), Interval(4, 4), Interval(4, 4), Interval(11, 11), Interval(33, 37),
         Interval(72, 94), Interval(54, 60), Interval(18, 20), Interval(77, 83), Interval(20, 20),
         Interval(15, 17), Interval(93, 99), Interval(23, 25), Interval(61, 67), Interval(87, 99)],
        # Job 9
        [Interval(56, 66), Interval(81, 91), Interval(41, 51), Interval(56, 60), Interval(2, 2),
         Interval(18, 20), Interval(46, 46), Interval(43, 57), Interval(69, 89), Interval(78, 90),
         Interval(13, 15), Interval(14, 18), Interval(70, 82), Interval(80, 98), Interval(77, 93),
         Interval(80, 92), Interval(53, 67), Interval(40, 48), Interval(25, 31), Interval(55, 71)],
        # Job 10
        [Interval(9, 11), Interval(44, 44), Interval(24, 28), Interval(58, 64), Interval(82, 102),
         Interval(30, 30), Interval(19, 19), Interval(24, 30), Interval(22, 22), Interval(76, 96),
         Interval(20, 24), Interval(54, 70), Interval(74, 76), Interval(10, 10), Interval(76, 80),
         Interval(3, 3), Interval(96, 98), Interval(85, 91), Interval(10, 10), Interval(44, 48)],
        # Job 11
        [Interval(20, 22), Interval(50, 52), Interval(3, 3), Interval(85, 103), Interval(72, 92),
         Interval(24, 28), Interval(83, 83), Interval(53, 61), Interval(86, 86), Interval(60, 62),
         Interval(76, 84), Interval(78, 84), Interval(23, 27), Interval(5, 5), Interval(67, 83),
         Interval(37, 39), Interval(15, 17), Interval(20, 20), Interval(47, 53), Interval(50, 54)],
        # Job 12
        [Interval(15, 19), Interval(77, 95), Interval(6, 6), Interval(49, 49), Interval(69, 79),
         Interval(74, 90), Interval(74, 98), Interval(26, 26), Interval(72, 88), Interval(40, 52),
         Interval(83, 105), Interval(7, 7), Interval(24, 30), Interval(24, 28), Interval(93, 101),
         Interval(13, 15), Interval(27, 27), Interval(3, 3), Interval(12, 12), Interval(73, 91)],
        # Job 13
        [Interval(43, 49), Interval(19, 23), Interval(1, 1), Interval(93, 105), Interval(74, 92),
         Interval(22, 22), Interval(2, 2), Interval(37, 47), Interval(55, 67), Interval(77, 81),
         Interval(17, 17), Interval(63, 71), Interval(59, 63), Interval(66, 78), Interval(48, 50),
         Interval(85, 97), Interval(33, 43), Interval(27, 29), Interval(34, 34), Interval(14, 14)],
        # Job 14
        [Interval(47, 53), Interval(46, 52), Interval(39, 41), Interval(57, 69), Interval(5, 5),
         Interval(74, 86), Interval(69, 71), Interval(3, 3), Interval(58, 66), Interval(37, 49),
         Interval(52, 64), Interval(38, 40), Interval(51, 53), Interval(65, 71), Interval(63, 79),
         Interval(84, 88), Interval(57, 65), Interval(50, 56), Interval(1, 1), Interval(95, 99)],
        # Job 15
        [Interval(53, 53), Interval(47, 55), Interval(23, 27), Interval(15, 17), Interval(88, 94),
         Interval(84, 102), Interval(35, 39), Interval(61, 61), Interval(37, 45), Interval(48, 50),
         Interval(20, 20), Interval(23, 25), Interval(54, 62), Interval(8, 8), Interval(64, 80),
         Interval(28, 32), Interval(14, 16), Interval(85, 87), Interval(27, 35), Interval(35, 45)],
        # Job 16
        [Interval(63, 81), Interval(72, 82), Interval(32, 36), Interval(45, 45), Interval(78, 88),
         Interval(74, 96), Interval(17, 21), Interval(5, 5), Interval(71, 83), Interval(65, 85),
         Interval(53, 69), Interval(81, 97), Interval(77, 77), Interval(42, 46), Interval(32, 32),
         Interval(86, 86), Interval(38, 42), Interval(21, 25), Interval(35, 35), Interval(57, 57)],
        # Job 17
        [Interval(33, 33), Interval(16, 16), Interval(56, 64), Interval(70, 70), Interval(64, 70),
         Interval(33, 41), Interval(42, 42), Interval(24, 24), Interval(72, 78), Interval(1, 1),
         Interval(20, 24), Interval(32, 32), Interval(19, 23), Interval(3, 3), Interval(68, 70),
         Interval(66, 88), Interval(49, 57), Interval(64, 64), Interval(33, 35), Interval(14, 16)],
        # Job 18
        [Interval(58, 58), Interval(54, 56), Interval(63, 73), Interval(5, 5), Interval(20, 20),
         Interval(83, 93), Interval(79, 103), Interval(71, 87), Interval(51, 59), Interval(15, 17),
         Interval(50, 56), Interval(74, 94), Interval(1, 1), Interval(60, 72), Interval(14, 14),
         Interval(79, 87), Interval(1, 1), Interval(84, 108), Interval(51, 57), Interval(29, 31)],
        # Job 19
        [Interval(71, 89), Interval(80, 82), Interval(8, 10), Interval(43, 55), Interval(29, 35),
         Interval(19, 19), Interval(81, 103), Interval(62, 68), Interval(81, 95), Interval(63, 65),
         Interval(4, 4), Interval(65, 71), Interval(74, 84), Interval(20, 22), Interval(82, 86),
         Interval(86, 98), Interval(58, 74), Interval(45, 57), Interval(72, 94), Interval(93, 99)],
    ],
    'name': 'INT__TAI20_20_02.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai20_20_02_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI20_20_02.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI20_20_02.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI20_20_02_F_15_01_INTERVAL_DATA
