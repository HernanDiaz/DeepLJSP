"""
Problema INT__TAI30_20_04.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI30_20_04_F_15_01_INTERVAL_DATA = {
    'num_jobs': 30,
    'num_machines': 20,
    'problem_id': 'int__tai30_20_04.F.15_01_interval',
    'sequences': [
        [5, 0, 6, 16, 2, 15, 19, 10, 12, 13, 4, 3, 9, 17, 18, 1, 7, 8, 14, 11],
        [17, 11, 16, 13, 1, 7, 4, 14, 10, 8, 2, 19, 3, 12, 6, 5, 0, 15, 9, 18],
        [15, 9, 18, 19, 1, 16, 17, 8, 0, 14, 13, 2, 7, 3, 12, 11, 5, 6, 10, 4],
        [13, 1, 19, 2, 10, 6, 8, 3, 0, 16, 9, 5, 14, 17, 15, 11, 12, 4, 18, 7],
        [13, 3, 2, 19, 1, 0, 15, 6, 18, 14, 5, 16, 17, 9, 11, 10, 12, 7, 4, 8],
        [6, 17, 14, 19, 7, 12, 3, 18, 5, 11, 8, 0, 1, 15, 16, 10, 13, 4, 2, 9],
        [0, 10, 15, 11, 17, 14, 5, 6, 8, 3, 9, 16, 12, 2, 1, 19, 18, 13, 7, 4],
        [9, 10, 8, 13, 16, 18, 15, 3, 6, 5, 1, 11, 14, 0, 7, 17, 2, 12, 4, 19],
        [4, 6, 19, 5, 2, 9, 16, 18, 7, 8, 12, 1, 15, 13, 17, 10, 0, 14, 3, 11],
        [17, 1, 12, 5, 2, 3, 8, 7, 6, 9, 19, 15, 14, 10, 4, 18, 11, 16, 13, 0],
        [17, 15, 11, 0, 7, 6, 5, 9, 4, 12, 10, 2, 14, 16, 19, 3, 13, 8, 1, 18],
        [13, 14, 2, 5, 0, 11, 16, 17, 15, 9, 18, 6, 19, 7, 12, 3, 4, 1, 10, 8],
        [3, 5, 13, 0, 14, 12, 11, 16, 2, 19, 8, 9, 15, 4, 7, 17, 6, 18, 10, 1],
        [15, 5, 18, 17, 6, 16, 13, 12, 3, 2, 9, 0, 1, 14, 8, 10, 11, 19, 4, 7],
        [10, 6, 19, 15, 4, 17, 8, 1, 12, 18, 0, 9, 3, 5, 13, 11, 2, 16, 7, 14],
        [3, 9, 16, 6, 7, 11, 14, 8, 18, 12, 5, 17, 19, 10, 2, 1, 0, 15, 13, 4],
        [13, 18, 5, 6, 8, 0, 4, 10, 7, 12, 1, 15, 3, 16, 19, 2, 11, 17, 9, 14],
        [5, 15, 1, 2, 19, 18, 12, 13, 16, 17, 14, 9, 0, 11, 10, 3, 8, 4, 6, 7],
        [8, 14, 6, 3, 11, 4, 12, 15, 1, 0, 17, 7, 5, 10, 19, 2, 18, 13, 16, 9],
        [10, 0, 14, 2, 16, 19, 17, 6, 3, 8, 12, 11, 7, 13, 15, 9, 1, 5, 4, 18],
        [17, 14, 1, 4, 7, 16, 0, 18, 19, 13, 15, 8, 2, 11, 10, 6, 3, 12, 9, 5],
        [14, 16, 17, 5, 4, 8, 10, 12, 3, 19, 2, 9, 18, 13, 15, 0, 7, 1, 6, 11],
        [1, 14, 2, 8, 13, 6, 12, 3, 5, 18, 17, 11, 10, 0, 7, 19, 15, 4, 16, 9],
        [7, 11, 3, 9, 8, 4, 18, 5, 14, 0, 10, 13, 1, 2, 15, 17, 19, 6, 12, 16],
        [19, 6, 9, 16, 17, 8, 14, 11, 7, 10, 18, 2, 3, 0, 1, 12, 4, 5, 15, 13],
        [2, 16, 17, 6, 3, 4, 11, 5, 18, 14, 15, 19, 0, 9, 7, 12, 13, 10, 1, 8],
        [13, 11, 16, 14, 6, 15, 1, 17, 0, 12, 5, 3, 2, 4, 7, 8, 10, 9, 18, 19],
        [10, 2, 6, 0, 19, 14, 7, 12, 18, 16, 5, 9, 15, 3, 11, 13, 1, 17, 4, 8],
        [15, 19, 11, 17, 18, 13, 4, 6, 8, 12, 3, 14, 1, 10, 16, 2, 5, 0, 7, 9],
        [0, 18, 19, 6, 11, 4, 5, 13, 2, 12, 17, 3, 1, 16, 8, 10, 9, 7, 14, 15],
    ],
    'durations': [
        # Job 0
        [Interval(45, 57), Interval(83, 103), Interval(47, 51), Interval(1, 1), Interval(51, 53),
         Interval(25, 27), Interval(70, 78), Interval(56, 62), Interval(38, 50), Interval(8, 8),
         Interval(79, 83), Interval(90, 100), Interval(64, 72), Interval(53, 61), Interval(49, 65),
         Interval(36, 44), Interval(16, 18), Interval(83, 101), Interval(85, 91), Interval(6, 6)],
        # Job 1
        [Interval(67, 83), Interval(20, 24), Interval(11, 11), Interval(46, 52), Interval(31, 31),
         Interval(30, 34), Interval(5, 5), Interval(50, 52), Interval(13, 15), Interval(38, 48),
         Interval(43, 43), Interval(24, 24), Interval(80, 86), Interval(62, 72), Interval(2, 2),
         Interval(40, 50), Interval(72, 78), Interval(32, 38), Interval(49, 51), Interval(95, 95)],
        # Job 2
        [Interval(76, 84), Interval(13, 13), Interval(35, 37), Interval(48, 54), Interval(58, 68),
         Interval(54, 62), Interval(30, 30), Interval(68, 82), Interval(71, 73), Interval(85, 99),
         Interval(13, 13), Interval(13, 13), Interval(84, 100), Interval(11, 13), Interval(68, 84),
         Interval(28, 30), Interval(57, 71), Interval(56, 60), Interval(25, 27), Interval(21, 21)],
        # Job 3
        [Interval(81, 101), Interval(93, 97), Interval(45, 57), Interval(65, 85), Interval(79, 99),
         Interval(56, 56), Interval(64, 84), Interval(53, 67), Interval(80, 92), Interval(64, 76),
         Interval(97, 97), Interval(11, 11), Interval(55, 67), Interval(59, 77), Interval(41, 45),
         Interval(5, 5), Interval(17, 17), Interval(18, 18), Interval(14, 14), Interval(91, 95)],
        # Job 4
        [Interval(35, 45), Interval(8, 10), Interval(74, 86), Interval(75, 89), Interval(64, 70),
         Interval(29, 37), Interval(79, 89), Interval(36, 42), Interval(47, 49), Interval(79, 99),
         Interval(90, 100), Interval(53, 67), Interval(4, 4), Interval(93, 105), Interval(88, 96),
         Interval(46, 58), Interval(72, 86), Interval(9, 9), Interval(87, 91), Interval(51, 57)],
        # Job 5
        [Interval(48, 62), Interval(63, 77), Interval(84, 106), Interval(57, 63), Interval(9, 9),
         Interval(78, 86), Interval(52, 52), Interval(29, 31), Interval(6, 6), Interval(24, 30),
         Interval(56, 58), Interval(89, 89), Interval(59, 67), Interval(26, 32), Interval(48, 62),
         Interval(35, 39), Interval(62, 70), Interval(15, 17), Interval(76, 98), Interval(59, 67)],
        # Job 6
        [Interval(42, 46), Interval(43, 51), Interval(89, 91), Interval(32, 38), Interval(75, 83),
         Interval(51, 63), Interval(56, 60), Interval(86, 110), Interval(62, 62), Interval(7, 9),
         Interval(27, 35), Interval(87, 101), Interval(45, 53), Interval(88, 92), Interval(10, 12),
         Interval(55, 71), Interval(22, 22), Interval(39, 49), Interval(90, 102), Interval(80, 92)],
        # Job 7
        [Interval(63, 63), Interval(69, 91), Interval(69, 75), Interval(79, 87), Interval(25, 25),
         Interval(54, 56), Interval(62, 74), Interval(37, 47), Interval(60, 80), Interval(63, 65),
         Interval(23, 25), Interval(7, 7), Interval(45, 45), Interval(12, 12), Interval(17, 17),
         Interval(8, 8), Interval(40, 42), Interval(86, 90), Interval(7, 7), Interval(78, 88)],
        # Job 8
        [Interval(68, 68), Interval(95, 103), Interval(36, 38), Interval(29, 37), Interval(71, 73),
         Interval(89, 107), Interval(90, 94), Interval(25, 31), Interval(13, 15), Interval(14, 18),
         Interval(90, 108), Interval(9, 9), Interval(84, 102), Interval(25, 25), Interval(8, 8),
         Interval(59, 69), Interval(4, 4), Interval(68, 80), Interval(34, 36), Interval(35, 39)],
        # Job 9
        [Interval(78, 80), Interval(31, 37), Interval(33, 39), Interval(72, 94), Interval(44, 52),
         Interval(23, 23), Interval(2, 2), Interval(5, 5), Interval(15, 17), Interval(73, 79),
         Interval(9, 11), Interval(94, 96), Interval(11, 13), Interval(85, 103), Interval(44, 48),
         Interval(51, 55), Interval(32, 38), Interval(72, 74), Interval(75, 81), Interval(50, 60)],
        # Job 10
        [Interval(27, 35), Interval(73, 77), Interval(10, 12), Interval(84, 100), Interval(46, 46),
         Interval(84, 84), Interval(37, 41), Interval(16, 18), Interval(78, 88), Interval(87, 87),
         Interval(76, 96), Interval(80, 106), Interval(64, 72), Interval(66, 68), Interval(81, 85),
         Interval(4, 4), Interval(88, 104), Interval(3, 3), Interval(7, 7), Interval(51, 51)],
        # Job 11
        [Interval(4, 4), Interval(47, 53), Interval(20, 20), Interval(64, 84), Interval(35, 39),
         Interval(83, 107), Interval(65, 65), Interval(83, 83), Interval(88, 108), Interval(25, 25),
         Interval(62, 66), Interval(88, 92), Interval(50, 52), Interval(55, 67), Interval(94, 100),
         Interval(68, 72), Interval(13, 15), Interval(12, 14), Interval(94, 104), Interval(75, 91)],
        # Job 12
        [Interval(37, 45), Interval(74, 88), Interval(80, 106), Interval(75, 81), Interval(47, 59),
         Interval(60, 72), Interval(37, 43), Interval(8, 8), Interval(54, 72), Interval(62, 70),
         Interval(2, 2), Interval(36, 36), Interval(22, 26), Interval(56, 66), Interval(69, 81),
         Interval(23, 31), Interval(65, 77), Interval(20, 26), Interval(16, 20), Interval(53, 67)],
        # Job 13
        [Interval(87, 87), Interval(26, 32), Interval(36, 36), Interval(2, 2), Interval(18, 18),
         Interval(2, 2), Interval(11, 11), Interval(41, 53), Interval(89, 99), Interval(86, 98),
         Interval(51, 65), Interval(85, 101), Interval(46, 48), Interval(84, 96), Interval(25, 31),
         Interval(48, 60), Interval(26, 30), Interval(80, 88), Interval(64, 72), Interval(4, 4)],
        # Job 14
        [Interval(23, 23), Interval(73, 75), Interval(83, 107), Interval(64, 64), Interval(20, 22),
         Interval(45, 47), Interval(75, 97), Interval(8, 8), Interval(51, 65), Interval(58, 70),
         Interval(91, 107), Interval(28, 30), Interval(41, 53), Interval(62, 66), Interval(6, 6),
         Interval(25, 25), Interval(57, 69), Interval(52, 66), Interval(83, 109), Interval(17, 21)],
        # Job 15
        [Interval(64, 86), Interval(72, 78), Interval(70, 82), Interval(81, 85), Interval(21, 23),
         Interval(98, 98), Interval(76, 94), Interval(70, 80), Interval(11, 11), Interval(57, 71),
         Interval(19, 23), Interval(90, 98), Interval(46, 46), Interval(62, 64), Interval(74, 82),
         Interval(33, 37), Interval(9, 9), Interval(16, 16), Interval(38, 40), Interval(27, 29)],
        # Job 16
        [Interval(50, 64), Interval(66, 66), Interval(43, 49), Interval(76, 92), Interval(15, 17),
         Interval(19, 19), Interval(1, 1), Interval(29, 29), Interval(57, 73), Interval(42, 42),
         Interval(87, 87), Interval(37, 39), Interval(80, 96), Interval(76, 90), Interval(76, 96),
         Interval(21, 21), Interval(34, 42), Interval(56, 66), Interval(29, 29), Interval(74, 74)],
        # Job 17
        [Interval(59, 73), Interval(70, 78), Interval(40, 46), Interval(49, 61), Interval(80, 92),
         Interval(61, 77), Interval(11, 11), Interval(11, 13), Interval(59, 63), Interval(48, 64),
         Interval(52, 60), Interval(69, 85), Interval(79, 81), Interval(15, 17), Interval(12, 14),
         Interval(12, 16), Interval(12, 16), Interval(88, 104), Interval(81, 95), Interval(18, 22)],
        # Job 18
        [Interval(45, 59), Interval(1, 1), Interval(82, 82), Interval(51, 63), Interval(16, 20),
         Interval(82, 106), Interval(41, 47), Interval(78, 84), Interval(22, 28), Interval(68, 82),
         Interval(26, 32), Interval(71, 77), Interval(9, 11), Interval(23, 25), Interval(61, 65),
         Interval(40, 44), Interval(59, 65), Interval(85, 111), Interval(61, 73), Interval(72, 72)],
        # Job 19
        [Interval(75, 87), Interval(89, 101), Interval(40, 52), Interval(6, 6), Interval(5, 5),
         Interval(18, 18), Interval(69, 89), Interval(39, 47), Interval(24, 32), Interval(25, 29),
         Interval(79, 89), Interval(74, 92), Interval(94, 104), Interval(59, 61), Interval(80, 92),
         Interval(20, 22), Interval(13, 13), Interval(26, 30), Interval(89, 93), Interval(19, 21)],
        # Job 20
        [Interval(61, 65), Interval(53, 59), Interval(22, 26), Interval(38, 48), Interval(30, 30),
         Interval(21, 23), Interval(30, 32), Interval(59, 69), Interval(51, 61), Interval(56, 68),
         Interval(25, 25), Interval(74, 96), Interval(12, 14), Interval(73, 79), Interval(59, 67),
         Interval(50, 52), Interval(79, 95), Interval(20, 22), Interval(61, 69), Interval(1, 1)],
        # Job 21
        [Interval(53, 55), Interval(1, 1), Interval(64, 78), Interval(74, 78), Interval(21, 25),
         Interval(78, 102), Interval(19, 19), Interval(91, 103), Interval(82, 86), Interval(27, 27),
         Interval(69, 71), Interval(36, 40), Interval(54, 70), Interval(94, 94), Interval(43, 51),
         Interval(20, 24), Interval(48, 56), Interval(19, 23), Interval(11, 11), Interval(89, 105)],
        # Job 22
        [Interval(87, 95), Interval(65, 69), Interval(11, 13), Interval(71, 79), Interval(38, 46),
         Interval(33, 43), Interval(62, 64), Interval(85, 99), Interval(38, 44), Interval(14, 14),
         Interval(25, 31), Interval(79, 89), Interval(39, 39), Interval(47, 51), Interval(20, 26),
         Interval(50, 66), Interval(8, 10), Interval(17, 21), Interval(16, 18), Interval(43, 49)],
        # Job 23
        [Interval(80, 98), Interval(39, 49), Interval(56, 66), Interval(63, 63), Interval(84, 106),
         Interval(64, 76), Interval(42, 56), Interval(86, 112), Interval(40, 48), Interval(67, 69),
         Interval(80, 92), Interval(74, 98), Interval(10, 12), Interval(12, 14), Interval(16, 18),
         Interval(82, 88), Interval(57, 67), Interval(69, 91), Interval(33, 41), Interval(2, 2)],
        # Job 24
        [Interval(37, 41), Interval(39, 45), Interval(17, 21), Interval(75, 87), Interval(43, 49),
         Interval(80, 94), Interval(7, 7), Interval(56, 60), Interval(27, 27), Interval(85, 109),
         Interval(49, 57), Interval(18, 24), Interval(60, 78), Interval(96, 98), Interval(61, 67),
         Interval(44, 50), Interval(10, 12), Interval(43, 43), Interval(63, 71), Interval(11, 11)],
        # Job 25
        [Interval(4, 4), Interval(12, 14), Interval(41, 47), Interval(24, 30), Interval(23, 23),
         Interval(23, 27), Interval(41, 47), Interval(35, 43), Interval(37, 39), Interval(29, 33),
         Interval(33, 43), Interval(86, 104), Interval(13, 13), Interval(18, 20), Interval(29, 29),
         Interval(33, 41), Interval(40, 48), Interval(66, 88), Interval(23, 25), Interval(39, 39)],
        # Job 26
        [Interval(54, 58), Interval(79, 103), Interval(36, 38), Interval(32, 40), Interval(82, 90),
         Interval(2, 2), Interval(38, 40), Interval(17, 21), Interval(88, 92), Interval(39, 47),
         Interval(72, 72), Interval(86, 88), Interval(35, 39), Interval(37, 41), Interval(84, 96),
         Interval(29, 37), Interval(70, 76), Interval(76, 100), Interval(33, 35), Interval(60, 72)],
        # Job 27
        [Interval(49, 63), Interval(29, 35), Interval(42, 54), Interval(6, 6), Interval(9, 9),
         Interval(51, 63), Interval(21, 21), Interval(50, 62), Interval(36, 38), Interval(73, 77),
         Interval(36, 44), Interval(82, 104), Interval(86, 108), Interval(5, 5), Interval(67, 67),
         Interval(23, 25), Interval(20, 20), Interval(14, 16), Interval(16, 16), Interval(21, 21)],
        # Job 28
        [Interval(28, 34), Interval(28, 32), Interval(81, 95), Interval(45, 45), Interval(37, 37),
         Interval(34, 42), Interval(3, 3), Interval(96, 98), Interval(38, 42), Interval(29, 29),
         Interval(22, 26), Interval(29, 31), Interval(28, 30), Interval(39, 51), Interval(47, 55),
         Interval(58, 58), Interval(77, 87), Interval(48, 54), Interval(82, 88), Interval(33, 41)],
        # Job 29
        [Interval(37, 39), Interval(72, 82), Interval(8, 8), Interval(46, 50), Interval(44, 48),
         Interval(81, 97), Interval(84, 108), Interval(47, 53), Interval(20, 22), Interval(38, 38),
         Interval(51, 63), Interval(23, 29), Interval(84, 110), Interval(65, 75), Interval(21, 25),
         Interval(17, 19), Interval(29, 37), Interval(30, 38), Interval(32, 38), Interval(67, 71)],
    ],
    'name': 'INT__TAI30_20_04.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai30_20_04_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI30_20_04.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI30_20_04.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI30_20_04_F_15_01_INTERVAL_DATA
