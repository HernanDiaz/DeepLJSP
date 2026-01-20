"""
Problema INT__TAI30_20_07.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI30_20_07_F_15_01_INTERVAL_DATA = {
    'num_jobs': 30,
    'num_machines': 20,
    'problem_id': 'int__tai30_20_07.F.15_01_interval',
    'sequences': [
        [11, 19, 16, 7, 12, 1, 10, 8, 6, 18, 2, 13, 17, 14, 0, 3, 15, 4, 5, 9],
        [4, 19, 8, 17, 0, 5, 1, 6, 11, 12, 10, 13, 2, 3, 15, 18, 16, 7, 14, 9],
        [19, 10, 14, 11, 3, 2, 13, 1, 0, 12, 9, 18, 4, 5, 16, 17, 7, 6, 8, 15],
        [2, 15, 6, 19, 17, 14, 12, 13, 1, 11, 5, 4, 9, 16, 18, 10, 8, 7, 0, 3],
        [17, 8, 10, 16, 19, 4, 2, 6, 0, 3, 9, 12, 11, 7, 1, 15, 14, 13, 18, 5],
        [5, 6, 13, 10, 19, 16, 9, 8, 15, 12, 4, 7, 14, 11, 17, 3, 18, 2, 0, 1],
        [2, 19, 4, 8, 9, 6, 7, 5, 11, 1, 13, 14, 17, 18, 10, 3, 12, 16, 0, 15],
        [16, 7, 1, 6, 5, 12, 4, 10, 14, 15, 8, 18, 0, 3, 9, 11, 17, 13, 19, 2],
        [12, 0, 2, 4, 1, 6, 14, 16, 19, 3, 17, 5, 11, 8, 9, 10, 13, 15, 7, 18],
        [6, 17, 13, 19, 16, 18, 11, 10, 3, 2, 14, 8, 5, 7, 15, 9, 12, 4, 0, 1],
        [12, 18, 11, 7, 17, 10, 6, 9, 3, 19, 14, 1, 4, 15, 0, 2, 13, 5, 8, 16],
        [0, 18, 11, 3, 15, 10, 5, 4, 7, 13, 8, 19, 17, 2, 14, 1, 6, 16, 9, 12],
        [3, 4, 7, 6, 5, 15, 8, 13, 17, 12, 9, 10, 18, 2, 14, 0, 11, 1, 19, 16],
        [5, 12, 14, 6, 3, 10, 13, 7, 8, 17, 15, 18, 4, 0, 1, 16, 9, 11, 2, 19],
        [7, 4, 10, 13, 11, 16, 18, 12, 8, 15, 19, 1, 0, 17, 2, 3, 9, 14, 6, 5],
        [0, 17, 4, 15, 11, 3, 14, 13, 10, 7, 8, 1, 9, 16, 5, 18, 12, 6, 19, 2],
        [19, 1, 11, 17, 5, 18, 7, 10, 12, 2, 0, 3, 4, 13, 6, 8, 16, 9, 15, 14],
        [3, 12, 1, 15, 7, 6, 8, 9, 13, 16, 19, 10, 4, 17, 5, 18, 14, 2, 0, 11],
        [11, 10, 15, 12, 7, 19, 9, 4, 8, 2, 1, 5, 6, 3, 17, 13, 0, 16, 18, 14],
        [0, 13, 9, 5, 15, 14, 17, 6, 11, 7, 12, 2, 10, 16, 1, 19, 4, 8, 18, 3],
        [14, 2, 13, 16, 9, 19, 7, 6, 18, 15, 4, 17, 0, 12, 5, 3, 11, 8, 10, 1],
        [16, 9, 17, 8, 6, 4, 19, 18, 7, 2, 14, 15, 12, 5, 10, 13, 3, 0, 11, 1],
        [5, 19, 2, 16, 10, 6, 13, 4, 11, 1, 3, 17, 9, 8, 15, 7, 18, 12, 14, 0],
        [4, 0, 10, 2, 1, 8, 18, 5, 13, 7, 19, 14, 6, 15, 17, 16, 12, 11, 9, 3],
        [6, 5, 10, 11, 3, 7, 0, 8, 15, 9, 17, 4, 2, 19, 16, 12, 13, 18, 1, 14],
        [18, 9, 0, 11, 14, 4, 1, 5, 19, 12, 17, 10, 6, 3, 13, 2, 15, 7, 8, 16],
        [17, 0, 16, 4, 18, 1, 8, 5, 15, 2, 3, 7, 19, 12, 11, 14, 13, 9, 10, 6],
        [4, 17, 13, 2, 15, 7, 10, 1, 9, 16, 11, 6, 8, 18, 12, 0, 3, 14, 5, 19],
        [6, 18, 5, 2, 3, 17, 19, 1, 14, 9, 12, 0, 15, 10, 4, 13, 16, 11, 8, 7],
        [10, 11, 17, 3, 6, 7, 5, 12, 14, 1, 9, 18, 15, 0, 13, 19, 2, 4, 16, 8],
    ],
    'durations': [
        # Job 0
        [Interval(60, 72), Interval(36, 40), Interval(15, 15), Interval(7, 7), Interval(89, 97),
         Interval(51, 63), Interval(85, 99), Interval(53, 59), Interval(87, 99), Interval(57, 63),
         Interval(36, 44), Interval(64, 84), Interval(56, 62), Interval(69, 75), Interval(19, 23),
         Interval(23, 25), Interval(23, 25), Interval(57, 57), Interval(74, 74), Interval(66, 72)],
        # Job 1
        [Interval(86, 90), Interval(64, 76), Interval(39, 45), Interval(13, 15), Interval(66, 66),
         Interval(8, 8), Interval(28, 36), Interval(66, 88), Interval(11, 11), Interval(30, 30),
         Interval(43, 53), Interval(96, 98), Interval(82, 96), Interval(78, 86), Interval(81, 81),
         Interval(79, 99), Interval(71, 81), Interval(83, 91), Interval(41, 47), Interval(26, 26)],
        # Job 2
        [Interval(52, 54), Interval(81, 83), Interval(35, 39), Interval(82, 88), Interval(29, 33),
         Interval(74, 88), Interval(21, 27), Interval(67, 67), Interval(3, 3), Interval(12, 12),
         Interval(8, 8), Interval(64, 80), Interval(77, 97), Interval(68, 70), Interval(18, 20),
         Interval(31, 39), Interval(86, 108), Interval(46, 46), Interval(67, 79), Interval(12, 12)],
        # Job 3
        [Interval(30, 32), Interval(44, 56), Interval(72, 76), Interval(12, 12), Interval(48, 56),
         Interval(83, 95), Interval(67, 67), Interval(46, 58), Interval(21, 21), Interval(10, 12),
         Interval(29, 33), Interval(62, 76), Interval(31, 39), Interval(92, 106), Interval(23, 25),
         Interval(82, 104), Interval(82, 92), Interval(15, 15), Interval(19, 21), Interval(57, 75)],
        # Job 4
        [Interval(14, 14), Interval(79, 101), Interval(13, 15), Interval(61, 75), Interval(6, 6),
         Interval(77, 81), Interval(14, 14), Interval(15, 15), Interval(16, 18), Interval(66, 70),
         Interval(18, 20), Interval(43, 49), Interval(68, 76), Interval(31, 35), Interval(18, 22),
         Interval(12, 12), Interval(52, 60), Interval(86, 108), Interval(26, 26), Interval(32, 40)],
        # Job 5
        [Interval(67, 75), Interval(83, 107), Interval(2, 2), Interval(79, 83), Interval(84, 102),
         Interval(18, 24), Interval(84, 112), Interval(61, 67), Interval(29, 31), Interval(37, 43),
         Interval(61, 73), Interval(59, 71), Interval(16, 16), Interval(29, 37), Interval(46, 56),
         Interval(46, 52), Interval(62, 74), Interval(83, 95), Interval(90, 94), Interval(31, 39)],
        # Job 6
        [Interval(27, 29), Interval(31, 35), Interval(78, 84), Interval(91, 97), Interval(10, 12),
         Interval(53, 69), Interval(32, 40), Interval(29, 37), Interval(87, 97), Interval(73, 93),
         Interval(14, 14), Interval(87, 107), Interval(35, 37), Interval(58, 64), Interval(67, 77),
         Interval(64, 66), Interval(24, 28), Interval(13, 15), Interval(4, 4), Interval(71, 89)],
        # Job 7
        [Interval(63, 77), Interval(86, 106), Interval(34, 36), Interval(11, 11), Interval(99, 99),
         Interval(71, 95), Interval(39, 39), Interval(41, 45), Interval(86, 88), Interval(18, 20),
         Interval(13, 15), Interval(40, 52), Interval(81, 101), Interval(15, 19), Interval(31, 33),
         Interval(32, 32), Interval(35, 41), Interval(41, 51), Interval(93, 99), Interval(20, 24)],
        # Job 8
        [Interval(65, 73), Interval(34, 38), Interval(8, 8), Interval(19, 23), Interval(2, 2),
         Interval(31, 33), Interval(65, 85), Interval(70, 92), Interval(43, 51), Interval(61, 67),
         Interval(77, 83), Interval(71, 79), Interval(45, 53), Interval(41, 41), Interval(78, 86),
         Interval(22, 28), Interval(85, 93), Interval(29, 37), Interval(27, 31), Interval(45, 49)],
        # Job 9
        [Interval(9, 9), Interval(33, 39), Interval(20, 24), Interval(56, 62), Interval(30, 34),
         Interval(32, 34), Interval(64, 80), Interval(25, 29), Interval(41, 49), Interval(17, 21),
         Interval(45, 53), Interval(31, 39), Interval(56, 58), Interval(81, 93), Interval(56, 62),
         Interval(47, 51), Interval(76, 90), Interval(51, 53), Interval(60, 72), Interval(60, 62)],
        # Job 10
        [Interval(22, 26), Interval(50, 56), Interval(56, 66), Interval(31, 31), Interval(13, 15),
         Interval(18, 20), Interval(26, 26), Interval(84, 98), Interval(48, 58), Interval(37, 45),
         Interval(69, 85), Interval(65, 67), Interval(74, 88), Interval(32, 32), Interval(26, 32),
         Interval(77, 89), Interval(13, 13), Interval(29, 33), Interval(6, 6), Interval(19, 23)],
        # Job 11
        [Interval(41, 49), Interval(86, 92), Interval(27, 31), Interval(7, 7), Interval(41, 53),
         Interval(42, 52), Interval(24, 26), Interval(43, 47), Interval(60, 60), Interval(26, 30),
         Interval(74, 92), Interval(66, 70), Interval(11, 13), Interval(35, 39), Interval(61, 77),
         Interval(40, 52), Interval(43, 51), Interval(84, 98), Interval(20, 20), Interval(40, 50)],
        # Job 12
        [Interval(21, 25), Interval(55, 55), Interval(59, 61), Interval(45, 59), Interval(15, 19),
         Interval(68, 82), Interval(50, 58), Interval(66, 86), Interval(33, 37), Interval(56, 66),
         Interval(50, 52), Interval(74, 94), Interval(35, 41), Interval(89, 99), Interval(26, 34),
         Interval(14, 14), Interval(68, 88), Interval(27, 31), Interval(86, 112), Interval(83, 93)],
        # Job 13
        [Interval(13, 15), Interval(22, 22), Interval(91, 107), Interval(51, 67), Interval(76, 102),
         Interval(44, 44), Interval(91, 105), Interval(56, 56), Interval(19, 25), Interval(29, 37),
         Interval(41, 41), Interval(40, 52), Interval(57, 73), Interval(77, 93), Interval(33, 43),
         Interval(3, 3), Interval(19, 19), Interval(36, 42), Interval(5, 5), Interval(64, 80)],
        # Job 14
        [Interval(11, 13), Interval(25, 29), Interval(8, 8), Interval(13, 13), Interval(24, 28),
         Interval(32, 38), Interval(30, 36), Interval(46, 52), Interval(26, 32), Interval(37, 41),
         Interval(35, 39), Interval(1, 1), Interval(72, 76), Interval(21, 23), Interval(35, 41),
         Interval(31, 31), Interval(6, 6), Interval(93, 103), Interval(74, 98), Interval(69, 69)],
        # Job 15
        [Interval(68, 76), Interval(72, 76), Interval(6, 6), Interval(52, 64), Interval(26, 28),
         Interval(21, 21), Interval(19, 19), Interval(94, 100), Interval(8, 8), Interval(66, 74),
         Interval(48, 50), Interval(25, 25), Interval(39, 39), Interval(82, 108), Interval(71, 71),
         Interval(75, 87), Interval(83, 93), Interval(11, 11), Interval(89, 97), Interval(61, 81)],
        # Job 16
        [Interval(11, 11), Interval(74, 90), Interval(82, 82), Interval(71, 89), Interval(65, 83),
         Interval(58, 62), Interval(43, 43), Interval(73, 77), Interval(4, 4), Interval(59, 69),
         Interval(45, 59), Interval(69, 77), Interval(73, 81), Interval(73, 87), Interval(81, 97),
         Interval(62, 70), Interval(26, 30), Interval(62, 62), Interval(79, 85), Interval(41, 43)],
        # Job 17
        [Interval(11, 11), Interval(16, 16), Interval(11, 13), Interval(70, 74), Interval(31, 39),
         Interval(77, 89), Interval(69, 77), Interval(41, 41), Interval(21, 25), Interval(56, 70),
         Interval(16, 16), Interval(37, 37), Interval(27, 29), Interval(82, 94), Interval(70, 80),
         Interval(45, 57), Interval(22, 24), Interval(40, 40), Interval(4, 4), Interval(69, 87)],
        # Job 18
        [Interval(51, 55), Interval(30, 30), Interval(73, 97), Interval(8, 8), Interval(58, 76),
         Interval(31, 39), Interval(56, 60), Interval(26, 32), Interval(52, 56), Interval(16, 16),
         Interval(58, 58), Interval(68, 78), Interval(14, 16), Interval(80, 84), Interval(75, 77),
         Interval(81, 95), Interval(63, 79), Interval(55, 59), Interval(54, 72), Interval(12, 14)],
        # Job 19
        [Interval(30, 38), Interval(16, 18), Interval(32, 40), Interval(93, 99), Interval(76, 92),
         Interval(79, 89), Interval(28, 30), Interval(50, 62), Interval(75, 91), Interval(83, 85),
         Interval(45, 59), Interval(33, 41), Interval(40, 42), Interval(90, 96), Interval(70, 88),
         Interval(84, 102), Interval(34, 40), Interval(1, 1), Interval(44, 46), Interval(30, 36)],
        # Job 20
        [Interval(19, 19), Interval(73, 85), Interval(38, 48), Interval(38, 48), Interval(62, 66),
         Interval(2, 2), Interval(13, 15), Interval(57, 59), Interval(42, 52), Interval(22, 24),
         Interval(92, 94), Interval(18, 20), Interval(57, 57), Interval(69, 85), Interval(31, 33),
         Interval(58, 64), Interval(25, 29), Interval(22, 28), Interval(52, 52), Interval(52, 54)],
        # Job 21
        [Interval(3, 3), Interval(1, 1), Interval(73, 73), Interval(78, 84), Interval(76, 100),
         Interval(49, 63), Interval(52, 64), Interval(14, 14), Interval(77, 99), Interval(58, 78),
         Interval(16, 16), Interval(77, 79), Interval(44, 52), Interval(27, 33), Interval(63, 73),
         Interval(5, 5), Interval(47, 47), Interval(25, 31), Interval(68, 74), Interval(17, 21)],
        # Job 22
        [Interval(37, 41), Interval(65, 79), Interval(35, 39), Interval(32, 34), Interval(50, 56),
         Interval(84, 106), Interval(7, 9), Interval(13, 13), Interval(20, 26), Interval(40, 40),
         Interval(15, 15), Interval(6, 6), Interval(25, 25), Interval(1, 1), Interval(19, 25),
         Interval(30, 30), Interval(10, 10), Interval(6, 8), Interval(54, 64), Interval(14, 14)],
        # Job 23
        [Interval(35, 39), Interval(94, 102), Interval(76, 86), Interval(66, 80), Interval(52, 64),
         Interval(25, 29), Interval(21, 23), Interval(37, 41), Interval(85, 111), Interval(32, 38),
         Interval(88, 108), Interval(67, 79), Interval(25, 25), Interval(71, 75), Interval(68, 76),
         Interval(75, 83), Interval(48, 60), Interval(83, 105), Interval(27, 27), Interval(27, 33)],
        # Job 24
        [Interval(46, 52), Interval(60, 66), Interval(94, 100), Interval(77, 97), Interval(76, 96),
         Interval(71, 91), Interval(13, 17), Interval(91, 93), Interval(64, 82), Interval(66, 86),
         Interval(48, 58), Interval(75, 75), Interval(83, 103), Interval(70, 70), Interval(32, 38),
         Interval(13, 13), Interval(82, 88), Interval(81, 109), Interval(39, 39), Interval(49, 65)],
        # Job 25
        [Interval(33, 35), Interval(41, 43), Interval(62, 64), Interval(68, 78), Interval(6, 6),
         Interval(61, 81), Interval(72, 80), Interval(78, 94), Interval(96, 98), Interval(15, 17),
         Interval(52, 56), Interval(39, 49), Interval(44, 54), Interval(91, 97), Interval(82, 102),
         Interval(24, 24), Interval(28, 34), Interval(66, 78), Interval(35, 35), Interval(45, 47)],
        # Job 26
        [Interval(4, 4), Interval(69, 75), Interval(27, 33), Interval(43, 51), Interval(77, 89),
         Interval(22, 24), Interval(76, 100), Interval(65, 79), Interval(71, 81), Interval(4, 4),
         Interval(10, 10), Interval(87, 91), Interval(66, 84), Interval(75, 75), Interval(24, 24),
         Interval(59, 67), Interval(72, 80), Interval(71, 83), Interval(36, 36), Interval(81, 95)],
        # Job 27
        [Interval(77, 83), Interval(67, 69), Interval(59, 71), Interval(14, 16), Interval(35, 37),
         Interval(34, 34), Interval(93, 95), Interval(7, 7), Interval(93, 105), Interval(41, 47),
         Interval(66, 78), Interval(12, 12), Interval(30, 36), Interval(72, 82), Interval(24, 24),
         Interval(54, 60), Interval(67, 69), Interval(1, 1), Interval(3, 3), Interval(6, 6)],
        # Job 28
        [Interval(79, 101), Interval(3, 3), Interval(65, 75), Interval(5, 5), Interval(72, 72),
         Interval(54, 66), Interval(32, 32), Interval(83, 99), Interval(40, 44), Interval(54, 54),
         Interval(17, 19), Interval(62, 64), Interval(50, 58), Interval(75, 91), Interval(83, 101),
         Interval(50, 64), Interval(94, 98), Interval(11, 11), Interval(91, 105), Interval(41, 53)],
        # Job 29
        [Interval(68, 86), Interval(32, 34), Interval(57, 75), Interval(60, 76), Interval(91, 107),
         Interval(43, 51), Interval(50, 54), Interval(79, 97), Interval(4, 4), Interval(63, 79),
         Interval(20, 20), Interval(26, 32), Interval(74, 90), Interval(11, 11), Interval(16, 16),
         Interval(53, 61), Interval(4, 4), Interval(16, 20), Interval(27, 31), Interval(59, 77)],
    ],
    'name': 'INT__TAI30_20_07.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai30_20_07_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI30_20_07.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI30_20_07.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI30_20_07_F_15_01_INTERVAL_DATA
