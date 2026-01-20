"""
Problema INT__TAI30_20_06.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI30_20_06_F_15_01_INTERVAL_DATA = {
    'num_jobs': 30,
    'num_machines': 20,
    'problem_id': 'int__tai30_20_06.F.15_01_interval',
    'sequences': [
        [19, 12, 14, 10, 15, 7, 11, 17, 1, 5, 8, 0, 18, 2, 3, 4, 9, 13, 6, 16],
        [10, 5, 11, 8, 16, 6, 19, 15, 0, 13, 1, 17, 3, 7, 18, 4, 2, 14, 9, 12],
        [15, 19, 10, 5, 6, 7, 3, 9, 1, 16, 17, 11, 14, 12, 4, 18, 2, 8, 13, 0],
        [13, 9, 14, 18, 1, 11, 19, 2, 3, 4, 10, 5, 12, 17, 6, 8, 16, 0, 15, 7],
        [3, 2, 10, 8, 1, 4, 5, 15, 12, 11, 13, 7, 0, 16, 17, 9, 6, 19, 14, 18],
        [19, 11, 6, 9, 7, 18, 13, 14, 15, 0, 16, 8, 12, 3, 10, 1, 5, 17, 2, 4],
        [15, 10, 5, 9, 19, 0, 8, 18, 12, 13, 6, 4, 17, 14, 7, 2, 1, 16, 3, 11],
        [19, 5, 14, 3, 4, 12, 15, 13, 6, 18, 7, 9, 11, 1, 16, 10, 17, 0, 2, 8],
        [12, 5, 19, 10, 8, 11, 0, 17, 4, 6, 13, 9, 16, 3, 2, 14, 7, 15, 1, 18],
        [9, 15, 12, 5, 3, 13, 19, 8, 16, 4, 18, 17, 7, 2, 6, 0, 10, 1, 14, 11],
        [1, 19, 18, 10, 6, 2, 15, 14, 7, 17, 11, 13, 5, 12, 16, 4, 0, 9, 3, 8],
        [11, 19, 2, 17, 14, 7, 15, 4, 5, 0, 1, 8, 3, 10, 13, 16, 12, 6, 9, 18],
        [6, 5, 3, 11, 13, 14, 9, 12, 8, 0, 19, 1, 2, 18, 4, 7, 15, 17, 10, 16],
        [2, 6, 4, 12, 17, 16, 0, 10, 7, 3, 5, 18, 1, 8, 9, 19, 15, 11, 14, 13],
        [9, 5, 1, 7, 11, 0, 8, 12, 2, 19, 10, 6, 4, 15, 13, 18, 14, 16, 3, 17],
        [14, 11, 5, 10, 4, 3, 1, 13, 7, 15, 2, 17, 0, 19, 18, 8, 9, 6, 16, 12],
        [2, 12, 5, 13, 17, 4, 14, 7, 6, 11, 19, 0, 16, 10, 15, 3, 9, 18, 1, 8],
        [5, 4, 2, 15, 10, 3, 14, 7, 19, 0, 11, 17, 8, 12, 16, 9, 1, 13, 6, 18],
        [4, 9, 13, 5, 8, 6, 7, 17, 0, 12, 1, 3, 16, 15, 19, 10, 2, 11, 18, 14],
        [14, 3, 16, 10, 6, 2, 5, 0, 13, 12, 9, 7, 8, 19, 18, 1, 17, 15, 11, 4],
        [17, 13, 16, 15, 5, 4, 3, 11, 0, 7, 10, 2, 12, 14, 1, 8, 19, 18, 9, 6],
        [2, 9, 17, 4, 7, 5, 0, 18, 19, 13, 11, 1, 8, 15, 16, 12, 10, 6, 14, 3],
        [12, 4, 18, 1, 19, 5, 14, 8, 0, 10, 15, 6, 17, 2, 11, 16, 3, 13, 9, 7],
        [13, 6, 11, 5, 17, 16, 19, 10, 0, 4, 3, 1, 9, 18, 2, 14, 7, 8, 15, 12],
        [14, 9, 13, 11, 2, 5, 6, 17, 8, 4, 12, 0, 15, 1, 18, 19, 3, 7, 16, 10],
        [9, 18, 6, 8, 1, 4, 16, 7, 12, 10, 13, 17, 5, 2, 0, 11, 19, 15, 14, 3],
        [2, 19, 15, 8, 14, 3, 4, 1, 6, 11, 17, 12, 13, 5, 9, 16, 18, 7, 10, 0],
        [19, 1, 17, 6, 13, 2, 12, 8, 0, 9, 11, 3, 10, 4, 15, 7, 16, 18, 5, 14],
        [17, 14, 6, 5, 18, 16, 13, 0, 19, 9, 2, 7, 10, 8, 4, 1, 12, 15, 3, 11],
        [19, 7, 8, 0, 4, 3, 18, 9, 5, 2, 12, 11, 13, 17, 15, 6, 14, 10, 1, 16],
    ],
    'durations': [
        # Job 0
        [Interval(46, 52), Interval(87, 95), Interval(1, 1), Interval(34, 40), Interval(32, 32),
         Interval(68, 70), Interval(53, 59), Interval(58, 72), Interval(40, 50), Interval(57, 75),
         Interval(16, 18), Interval(70, 74), Interval(36, 40), Interval(57, 71), Interval(19, 21),
         Interval(61, 75), Interval(71, 71), Interval(46, 56), Interval(17, 17), Interval(25, 27)],
        # Job 1
        [Interval(51, 67), Interval(40, 46), Interval(85, 95), Interval(47, 55), Interval(91, 101),
         Interval(60, 64), Interval(33, 37), Interval(6, 6), Interval(50, 58), Interval(75, 87),
         Interval(3, 3), Interval(79, 81), Interval(82, 106), Interval(34, 44), Interval(36, 38),
         Interval(20, 22), Interval(50, 54), Interval(48, 54), Interval(33, 39), Interval(83, 95)],
        # Job 2
        [Interval(50, 64), Interval(90, 90), Interval(29, 39), Interval(36, 38), Interval(53, 67),
         Interval(48, 54), Interval(24, 30), Interval(28, 30), Interval(50, 56), Interval(20, 20),
         Interval(42, 48), Interval(15, 17), Interval(2, 2), Interval(21, 27), Interval(33, 35),
         Interval(17, 19), Interval(2, 2), Interval(72, 78), Interval(69, 87), Interval(41, 51)],
        # Job 3
        [Interval(29, 37), Interval(15, 15), Interval(66, 70), Interval(19, 19), Interval(40, 46),
         Interval(7, 7), Interval(2, 2), Interval(17, 21), Interval(13, 17), Interval(51, 65),
         Interval(73, 87), Interval(47, 49), Interval(49, 49), Interval(71, 93), Interval(61, 65),
         Interval(24, 28), Interval(4, 4), Interval(38, 38), Interval(62, 62), Interval(36, 46)],
        # Job 4
        [Interval(80, 84), Interval(61, 65), Interval(65, 79), Interval(42, 52), Interval(53, 59),
         Interval(89, 89), Interval(65, 77), Interval(81, 101), Interval(66, 84), Interval(92, 94),
         Interval(57, 61), Interval(54, 62), Interval(19, 21), Interval(77, 91), Interval(62, 64),
         Interval(44, 56), Interval(41, 55), Interval(80, 90), Interval(36, 42), Interval(40, 50)],
        # Job 5
        [Interval(54, 58), Interval(31, 33), Interval(32, 36), Interval(30, 30), Interval(38, 42),
         Interval(64, 70), Interval(30, 30), Interval(48, 50), Interval(17, 17), Interval(15, 19),
         Interval(14, 16), Interval(54, 62), Interval(43, 51), Interval(14, 16), Interval(20, 22),
         Interval(70, 78), Interval(76, 94), Interval(7, 7), Interval(37, 45), Interval(77, 81)],
        # Job 6
        [Interval(5, 5), Interval(73, 79), Interval(48, 48), Interval(53, 63), Interval(22, 24),
         Interval(39, 49), Interval(56, 70), Interval(52, 60), Interval(52, 66), Interval(68, 76),
         Interval(33, 35), Interval(74, 90), Interval(76, 96), Interval(43, 43), Interval(63, 77),
         Interval(36, 46), Interval(96, 98), Interval(56, 58), Interval(38, 38), Interval(22, 26)],
        # Job 7
        [Interval(51, 67), Interval(30, 38), Interval(65, 67), Interval(18, 22), Interval(12, 14),
         Interval(86, 90), Interval(88, 102), Interval(6, 6), Interval(61, 75), Interval(35, 47),
         Interval(50, 52), Interval(18, 22), Interval(72, 88), Interval(1, 1), Interval(38, 48),
         Interval(6, 6), Interval(34, 40), Interval(34, 34), Interval(66, 78), Interval(57, 67)],
        # Job 8
        [Interval(55, 55), Interval(59, 59), Interval(48, 58), Interval(65, 83), Interval(70, 84),
         Interval(69, 75), Interval(68, 84), Interval(95, 95), Interval(64, 68), Interval(2, 2),
         Interval(23, 29), Interval(52, 54), Interval(37, 45), Interval(28, 28), Interval(24, 28),
         Interval(63, 75), Interval(66, 82), Interval(54, 66), Interval(70, 88), Interval(5, 5)],
        # Job 9
        [Interval(57, 69), Interval(82, 106), Interval(82, 90), Interval(92, 102), Interval(90, 98),
         Interval(79, 85), Interval(87, 89), Interval(25, 25), Interval(10, 10), Interval(67, 77),
         Interval(37, 41), Interval(48, 50), Interval(5, 5), Interval(35, 41), Interval(84, 86),
         Interval(38, 46), Interval(83, 95), Interval(19, 25), Interval(30, 38), Interval(17, 19)],
        # Job 10
        [Interval(55, 69), Interval(64, 66), Interval(22, 28), Interval(66, 82), Interval(44, 52),
         Interval(63, 83), Interval(87, 97), Interval(59, 79), Interval(2, 2), Interval(17, 17),
         Interval(73, 85), Interval(70, 92), Interval(51, 59), Interval(37, 37), Interval(71, 87),
         Interval(83, 107), Interval(94, 94), Interval(28, 34), Interval(16, 16), Interval(39, 49)],
        # Job 11
        [Interval(47, 59), Interval(14, 14), Interval(69, 85), Interval(91, 93), Interval(30, 34),
         Interval(46, 48), Interval(81, 105), Interval(39, 43), Interval(6, 6), Interval(69, 73),
         Interval(61, 77), Interval(69, 71), Interval(89, 103), Interval(10, 12), Interval(36, 42),
         Interval(10, 10), Interval(15, 15), Interval(35, 43), Interval(92, 104), Interval(26, 32)],
        # Job 12
        [Interval(25, 25), Interval(76, 84), Interval(38, 38), Interval(40, 48), Interval(72, 84),
         Interval(34, 44), Interval(29, 29), Interval(37, 43), Interval(5, 5), Interval(44, 50),
         Interval(56, 66), Interval(44, 50), Interval(63, 63), Interval(77, 83), Interval(40, 52),
         Interval(76, 76), Interval(15, 15), Interval(54, 54), Interval(19, 23), Interval(23, 27)],
        # Job 13
        [Interval(53, 53), Interval(96, 102), Interval(44, 44), Interval(51, 57), Interval(84, 94),
         Interval(69, 81), Interval(25, 27), Interval(55, 61), Interval(30, 30), Interval(15, 19),
         Interval(3, 3), Interval(17, 17), Interval(13, 15), Interval(1, 1), Interval(57, 63),
         Interval(49, 49), Interval(72, 80), Interval(82, 84), Interval(9, 9), Interval(29, 35)],
        # Job 14
        [Interval(20, 24), Interval(10, 10), Interval(93, 95), Interval(54, 54), Interval(84, 98),
         Interval(85, 113), Interval(90, 92), Interval(8, 8), Interval(39, 39), Interval(52, 66),
         Interval(3, 3), Interval(50, 60), Interval(27, 31), Interval(35, 39), Interval(6, 6),
         Interval(64, 64), Interval(75, 87), Interval(80, 88), Interval(29, 29), Interval(83, 107)],
        # Job 15
        [Interval(66, 78), Interval(63, 71), Interval(25, 33), Interval(52, 62), Interval(9, 9),
         Interval(35, 45), Interval(68, 88), Interval(97, 101), Interval(50, 56), Interval(66, 66),
         Interval(81, 89), Interval(28, 34), Interval(37, 47), Interval(73, 93), Interval(44, 48),
         Interval(25, 29), Interval(43, 51), Interval(60, 60), Interval(59, 75), Interval(44, 50)],
        # Job 16
        [Interval(39, 51), Interval(44, 44), Interval(72, 94), Interval(8, 8), Interval(60, 60),
         Interval(2, 2), Interval(9, 11), Interval(3, 3), Interval(28, 30), Interval(9, 9),
         Interval(36, 38), Interval(27, 31), Interval(21, 23), Interval(90, 104), Interval(6, 6),
         Interval(37, 45), Interval(78, 84), Interval(66, 82), Interval(54, 70), Interval(90, 100)],
        # Job 17
        [Interval(79, 105), Interval(35, 39), Interval(30, 34), Interval(25, 31), Interval(26, 32),
         Interval(56, 68), Interval(87, 99), Interval(26, 34), Interval(85, 99), Interval(41, 49),
         Interval(33, 37), Interval(69, 85), Interval(41, 51), Interval(43, 51), Interval(44, 48),
         Interval(72, 90), Interval(40, 46), Interval(43, 43), Interval(28, 32), Interval(18, 18)],
        # Job 18
        [Interval(45, 53), Interval(82, 90), Interval(19, 21), Interval(80, 100), Interval(4, 4),
         Interval(42, 46), Interval(70, 74), Interval(22, 22), Interval(83, 97), Interval(1, 1),
         Interval(30, 30), Interval(70, 72), Interval(74, 80), Interval(55, 69), Interval(45, 51),
         Interval(24, 26), Interval(88, 90), Interval(6, 6), Interval(91, 99), Interval(39, 49)],
        # Job 19
        [Interval(55, 69), Interval(63, 63), Interval(89, 95), Interval(15, 17), Interval(18, 22),
         Interval(68, 70), Interval(59, 71), Interval(79, 83), Interval(19, 23), Interval(50, 58),
         Interval(94, 100), Interval(77, 81), Interval(37, 37), Interval(94, 100), Interval(81, 105),
         Interval(55, 55), Interval(62, 78), Interval(57, 63), Interval(35, 37), Interval(52, 62)],
        # Job 20
        [Interval(75, 77), Interval(50, 58), Interval(74, 78), Interval(32, 40), Interval(83, 103),
         Interval(61, 73), Interval(33, 37), Interval(37, 37), Interval(41, 47), Interval(80, 96),
         Interval(3, 3), Interval(19, 25), Interval(65, 81), Interval(59, 71), Interval(25, 27),
         Interval(3, 3), Interval(91, 107), Interval(73, 83), Interval(36, 40), Interval(29, 31)],
        # Job 21
        [Interval(73, 81), Interval(75, 89), Interval(64, 68), Interval(73, 77), Interval(81, 109),
         Interval(66, 78), Interval(75, 77), Interval(45, 59), Interval(65, 79), Interval(4, 4),
         Interval(65, 75), Interval(74, 78), Interval(55, 67), Interval(88, 88), Interval(34, 44),
         Interval(35, 37), Interval(80, 96), Interval(68, 70), Interval(52, 64), Interval(13, 15)],
        # Job 22
        [Interval(64, 66), Interval(8, 8), Interval(83, 97), Interval(57, 57), Interval(66, 80),
         Interval(2, 2), Interval(56, 68), Interval(47, 49), Interval(74, 78), Interval(75, 99),
         Interval(47, 59), Interval(21, 25), Interval(69, 83), Interval(73, 75), Interval(86, 112),
         Interval(34, 34), Interval(66, 76), Interval(24, 30), Interval(76, 98), Interval(44, 48)],
        # Job 23
        [Interval(66, 86), Interval(54, 54), Interval(66, 84), Interval(69, 69), Interval(40, 48),
         Interval(26, 26), Interval(61, 65), Interval(70, 80), Interval(70, 86), Interval(76, 80),
         Interval(35, 43), Interval(7, 7), Interval(71, 75), Interval(26, 28), Interval(51, 59),
         Interval(20, 26), Interval(50, 60), Interval(29, 29), Interval(56, 56), Interval(34, 38)],
        # Job 24
        [Interval(16, 18), Interval(42, 42), Interval(50, 62), Interval(81, 87), Interval(41, 47),
         Interval(73, 75), Interval(57, 67), Interval(52, 58), Interval(50, 60), Interval(31, 31),
         Interval(70, 72), Interval(11, 11), Interval(15, 17), Interval(26, 32), Interval(44, 56),
         Interval(67, 77), Interval(62, 66), Interval(39, 45), Interval(25, 31), Interval(67, 73)],
        # Job 25
        [Interval(69, 83), Interval(55, 57), Interval(70, 86), Interval(2, 2), Interval(6, 6),
         Interval(62, 80), Interval(19, 19), Interval(64, 74), Interval(27, 33), Interval(79, 95),
         Interval(50, 64), Interval(32, 34), Interval(84, 90), Interval(65, 71), Interval(21, 27),
         Interval(29, 33), Interval(54, 58), Interval(5, 5), Interval(18, 20), Interval(73, 91)],
        # Job 26
        [Interval(55, 73), Interval(31, 41), Interval(17, 21), Interval(79, 101), Interval(64, 66),
         Interval(79, 81), Interval(25, 27), Interval(2, 2), Interval(46, 58), Interval(72, 72),
         Interval(17, 17), Interval(27, 31), Interval(58, 62), Interval(14, 18), Interval(6, 6),
         Interval(81, 101), Interval(73, 85), Interval(37, 49), Interval(89, 109), Interval(24, 28)],
        # Job 27
        [Interval(79, 85), Interval(71, 89), Interval(53, 67), Interval(93, 93), Interval(53, 55),
         Interval(23, 25), Interval(79, 95), Interval(58, 68), Interval(52, 66), Interval(85, 85),
         Interval(13, 13), Interval(29, 35), Interval(84, 102), Interval(33, 33), Interval(15, 15),
         Interval(42, 54), Interval(63, 81), Interval(21, 25), Interval(97, 97), Interval(73, 79)],
        # Job 28
        [Interval(58, 64), Interval(6, 6), Interval(85, 89), Interval(72, 76), Interval(61, 73),
         Interval(40, 48), Interval(60, 66), Interval(12, 12), Interval(73, 89), Interval(60, 62),
         Interval(24, 28), Interval(21, 25), Interval(66, 86), Interval(83, 103), Interval(88, 106),
         Interval(73, 77), Interval(73, 79), Interval(41, 51), Interval(65, 67), Interval(53, 55)],
        # Job 29
        [Interval(70, 84), Interval(6, 6), Interval(55, 69), Interval(20, 24), Interval(70, 92),
         Interval(40, 48), Interval(28, 28), Interval(88, 106), Interval(16, 16), Interval(7, 7),
         Interval(34, 34), Interval(3, 3), Interval(93, 93), Interval(12, 12), Interval(32, 38),
         Interval(77, 99), Interval(9, 9), Interval(88, 98), Interval(75, 99), Interval(50, 52)],
    ],
    'name': 'INT__TAI30_20_06.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai30_20_06_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI30_20_06.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI30_20_06.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI30_20_06_F_15_01_INTERVAL_DATA
