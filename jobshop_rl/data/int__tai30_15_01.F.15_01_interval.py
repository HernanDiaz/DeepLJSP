"""
Problema INT__TAI30_15_01.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI30_15_01_F_15_01_INTERVAL_DATA = {
    'num_jobs': 30,
    'num_machines': 15,
    'problem_id': 'int__tai30_15_01.F.15_01_interval',
    'sequences': [
        [3, 10, 14, 1, 5, 8, 4, 11, 13, 12, 2, 9, 7, 0, 6],
        [6, 4, 2, 3, 14, 5, 7, 13, 9, 0, 11, 12, 8, 10, 1],
        [4, 2, 10, 5, 12, 13, 3, 11, 9, 7, 8, 6, 14, 1, 0],
        [0, 13, 4, 1, 14, 9, 12, 3, 8, 5, 2, 6, 10, 7, 11],
        [6, 1, 10, 4, 8, 5, 2, 9, 7, 0, 13, 11, 3, 14, 12],
        [5, 6, 12, 3, 0, 4, 2, 8, 1, 13, 11, 9, 14, 7, 10],
        [11, 13, 1, 6, 4, 12, 14, 0, 10, 8, 5, 7, 2, 9, 3],
        [5, 2, 1, 4, 9, 13, 8, 10, 11, 3, 7, 0, 6, 12, 14],
        [7, 13, 12, 5, 10, 9, 0, 11, 8, 4, 2, 1, 14, 6, 3],
        [6, 7, 14, 1, 9, 11, 3, 5, 10, 2, 8, 0, 13, 12, 4],
        [10, 0, 3, 4, 5, 11, 7, 12, 13, 14, 8, 1, 6, 2, 9],
        [5, 0, 9, 11, 12, 6, 10, 14, 8, 4, 7, 3, 13, 1, 2],
        [8, 0, 7, 4, 3, 1, 13, 5, 6, 12, 11, 9, 2, 14, 10],
        [4, 9, 13, 12, 6, 2, 7, 1, 11, 10, 8, 14, 0, 5, 3],
        [7, 14, 11, 2, 10, 12, 1, 3, 13, 9, 4, 8, 5, 0, 6],
        [13, 12, 4, 11, 1, 0, 10, 6, 5, 9, 2, 7, 3, 14, 8],
        [0, 7, 12, 14, 3, 2, 8, 11, 13, 9, 4, 1, 5, 6, 10],
        [5, 6, 7, 4, 12, 9, 11, 3, 10, 8, 1, 0, 2, 14, 13],
        [12, 4, 3, 13, 11, 6, 5, 0, 10, 1, 2, 9, 7, 8, 14],
        [0, 7, 3, 11, 10, 1, 8, 12, 5, 6, 2, 14, 9, 13, 4],
        [14, 5, 7, 1, 10, 6, 9, 3, 12, 0, 11, 13, 4, 2, 8],
        [12, 11, 6, 8, 13, 10, 1, 7, 14, 9, 4, 3, 2, 0, 5],
        [8, 9, 11, 3, 4, 13, 10, 2, 0, 12, 5, 6, 7, 1, 14],
        [12, 8, 6, 9, 11, 5, 2, 7, 14, 0, 4, 1, 3, 13, 10],
        [14, 11, 8, 4, 10, 5, 3, 2, 6, 9, 12, 13, 0, 1, 7],
        [7, 14, 4, 0, 12, 10, 8, 5, 3, 1, 6, 9, 2, 11, 13],
        [11, 12, 4, 14, 13, 1, 5, 8, 0, 7, 10, 9, 2, 6, 3],
        [14, 8, 7, 1, 0, 6, 9, 12, 5, 10, 4, 13, 11, 2, 3],
        [8, 7, 10, 14, 5, 12, 9, 2, 11, 1, 3, 0, 13, 6, 4],
        [2, 12, 13, 3, 0, 14, 6, 5, 10, 11, 8, 9, 1, 7, 4],
    ],
    'durations': [
        # Job 0
        [Interval(85, 113), Interval(40, 46), Interval(6, 6), Interval(93, 105), Interval(23, 23),
         Interval(85, 111), Interval(77, 91), Interval(23, 25), Interval(27, 33), Interval(48, 58),
         Interval(34, 34), Interval(84, 106), Interval(50, 50), Interval(41, 55), Interval(34, 42)],
        # Job 1
        [Interval(19, 19), Interval(23, 25), Interval(56, 74), Interval(15, 17), Interval(80, 108),
         Interval(8, 10), Interval(56, 64), Interval(31, 33), Interval(58, 60), Interval(76, 94),
         Interval(8, 10), Interval(32, 40), Interval(20, 24), Interval(25, 25), Interval(5, 5)],
        # Job 2
        [Interval(54, 54), Interval(58, 66), Interval(80, 106), Interval(70, 86), Interval(57, 61),
         Interval(65, 77), Interval(42, 56), Interval(77, 99), Interval(34, 46), Interval(12, 14),
         Interval(15, 19), Interval(83, 93), Interval(47, 47), Interval(28, 32), Interval(56, 56)],
        # Job 3
        [Interval(51, 69), Interval(15, 17), Interval(75, 83), Interval(84, 84), Interval(82, 86),
         Interval(41, 43), Interval(54, 64), Interval(13, 15), Interval(68, 80), Interval(55, 65),
         Interval(92, 104), Interval(17, 17), Interval(40, 44), Interval(27, 35), Interval(19, 19)],
        # Job 4
        [Interval(49, 49), Interval(47, 57), Interval(41, 51), Interval(45, 55), Interval(1, 1),
         Interval(14, 14), Interval(2, 2), Interval(48, 64), Interval(61, 67), Interval(51, 51),
         Interval(64, 86), Interval(27, 29), Interval(8, 10), Interval(36, 38), Interval(6, 6)],
        # Job 5
        [Interval(52, 66), Interval(64, 66), Interval(81, 89), Interval(40, 40), Interval(20, 26),
         Interval(35, 43), Interval(88, 110), Interval(43, 49), Interval(16, 18), Interval(88, 100),
         Interval(6, 6), Interval(58, 76), Interval(59, 79), Interval(74, 98), Interval(7, 9)],
        # Job 6
        [Interval(10, 10), Interval(6, 8), Interval(22, 22), Interval(33, 39), Interval(28, 34),
         Interval(65, 85), Interval(49, 65), Interval(47, 51), Interval(42, 46), Interval(21, 21),
         Interval(74, 80), Interval(68, 72), Interval(58, 70), Interval(41, 51), Interval(65, 73)],
        # Job 7
        [Interval(49, 57), Interval(72, 76), Interval(84, 102), Interval(24, 28), Interval(53, 55),
         Interval(82, 96), Interval(75, 89), Interval(61, 71), Interval(34, 40), Interval(60, 66),
         Interval(68, 74), Interval(17, 17), Interval(54, 62), Interval(4, 4), Interval(45, 47)],
        # Job 8
        [Interval(68, 84), Interval(68, 76), Interval(39, 45), Interval(17, 17), Interval(24, 30),
         Interval(56, 56), Interval(75, 81), Interval(5, 5), Interval(71, 73), Interval(17, 21),
         Interval(89, 91), Interval(46, 46), Interval(43, 43), Interval(51, 61), Interval(17, 17)],
        # Job 9
        [Interval(17, 19), Interval(75, 83), Interval(90, 96), Interval(69, 73), Interval(46, 50),
         Interval(23, 23), Interval(20, 20), Interval(82, 98), Interval(88, 100), Interval(77, 97),
         Interval(6, 6), Interval(36, 36), Interval(75, 93), Interval(23, 27), Interval(73, 93)],
        # Job 10
        [Interval(46, 58), Interval(56, 66), Interval(42, 48), Interval(53, 67), Interval(14, 16),
         Interval(72, 76), Interval(42, 56), Interval(26, 26), Interval(84, 104), Interval(50, 58),
         Interval(1, 1), Interval(56, 60), Interval(56, 56), Interval(52, 56), Interval(72, 72)],
        # Job 11
        [Interval(59, 67), Interval(69, 77), Interval(82, 82), Interval(72, 96), Interval(15, 15),
         Interval(47, 61), Interval(49, 55), Interval(46, 58), Interval(34, 38), Interval(20, 22),
         Interval(39, 51), Interval(36, 46), Interval(18, 24), Interval(96, 98), Interval(48, 52)],
        # Job 12
        [Interval(88, 92), Interval(83, 97), Interval(73, 81), Interval(30, 36), Interval(27, 35),
         Interval(23, 29), Interval(12, 16), Interval(75, 75), Interval(82, 102), Interval(69, 71),
         Interval(55, 55), Interval(51, 61), Interval(38, 40), Interval(46, 52), Interval(21, 25)],
        # Job 13
        [Interval(87, 87), Interval(45, 49), Interval(52, 64), Interval(34, 34), Interval(27, 31),
         Interval(83, 83), Interval(24, 24), Interval(43, 53), Interval(94, 100), Interval(81, 97),
         Interval(80, 88), Interval(80, 84), Interval(48, 58), Interval(87, 111), Interval(9, 11)],
        # Job 14
        [Interval(33, 37), Interval(28, 36), Interval(28, 32), Interval(86, 100), Interval(54, 62),
         Interval(25, 31), Interval(76, 100), Interval(14, 18), Interval(93, 103), Interval(4, 4),
         Interval(78, 86), Interval(97, 99), Interval(25, 27), Interval(25, 33), Interval(70, 84)],
        # Job 15
        [Interval(16, 20), Interval(88, 96), Interval(57, 67), Interval(52, 66), Interval(3, 3),
         Interval(93, 95), Interval(30, 38), Interval(48, 64), Interval(24, 24), Interval(17, 19),
         Interval(57, 75), Interval(52, 54), Interval(30, 30), Interval(36, 46), Interval(10, 10)],
        # Job 16
        [Interval(2, 2), Interval(26, 26), Interval(15, 19), Interval(16, 20), Interval(54, 66),
         Interval(37, 41), Interval(23, 23), Interval(85, 105), Interval(72, 90), Interval(51, 61),
         Interval(31, 37), Interval(8, 8), Interval(41, 53), Interval(64, 80), Interval(49, 63)],
        # Job 17
        [Interval(6, 6), Interval(79, 79), Interval(58, 72), Interval(58, 58), Interval(94, 94),
         Interval(44, 46), Interval(76, 84), Interval(3, 3), Interval(27, 31), Interval(77, 83),
         Interval(26, 28), Interval(56, 64), Interval(85, 103), Interval(13, 15), Interval(72, 80)],
        # Job 18
        [Interval(30, 32), Interval(78, 80), Interval(80, 94), Interval(70, 88), Interval(49, 65),
         Interval(46, 50), Interval(32, 34), Interval(36, 48), Interval(87, 99), Interval(82, 90),
         Interval(50, 58), Interval(28, 36), Interval(7, 9), Interval(14, 18), Interval(60, 66)],
        # Job 19
        [Interval(92, 100), Interval(1, 1), Interval(71, 79), Interval(37, 47), Interval(43, 47),
         Interval(47, 55), Interval(9, 11), Interval(50, 66), Interval(66, 76), Interval(80, 104),
         Interval(20, 26), Interval(18, 18), Interval(59, 67), Interval(26, 28), Interval(57, 69)],
        # Job 20
        [Interval(77, 91), Interval(73, 91), Interval(14, 18), Interval(55, 67), Interval(43, 43),
         Interval(65, 85), Interval(25, 31), Interval(13, 17), Interval(19, 19), Interval(85, 101),
         Interval(21, 23), Interval(1, 1), Interval(58, 66), Interval(9, 9), Interval(5, 5)],
        # Job 21
        [Interval(44, 48), Interval(27, 31), Interval(46, 54), Interval(12, 12), Interval(64, 80),
         Interval(17, 19), Interval(76, 82), Interval(73, 73), Interval(20, 26), Interval(1, 1),
         Interval(55, 61), Interval(1, 1), Interval(83, 107), Interval(22, 28), Interval(65, 77)],
        # Job 22
        [Interval(10, 10), Interval(34, 44), Interval(44, 54), Interval(55, 57), Interval(65, 77),
         Interval(37, 43), Interval(78, 102), Interval(24, 32), Interval(77, 101), Interval(42, 42),
         Interval(8, 10), Interval(85, 99), Interval(50, 54), Interval(6, 6), Interval(17, 23)],
        # Job 23
        [Interval(65, 75), Interval(54, 72), Interval(63, 73), Interval(92, 102), Interval(79, 93),
         Interval(80, 82), Interval(38, 38), Interval(6, 8), Interval(51, 55), Interval(42, 54),
         Interval(41, 45), Interval(53, 65), Interval(87, 89), Interval(29, 29), Interval(86, 88)],
        # Job 24
        [Interval(71, 91), Interval(97, 97), Interval(58, 72), Interval(60, 60), Interval(15, 15),
         Interval(29, 29), Interval(8, 10), Interval(77, 83), Interval(74, 82), Interval(73, 97),
         Interval(87, 103), Interval(76, 94), Interval(91, 91), Interval(24, 32), Interval(87, 97)],
        # Job 25
        [Interval(39, 39), Interval(6, 6), Interval(59, 59), Interval(34, 34), Interval(31, 37),
         Interval(29, 35), Interval(12, 12), Interval(7, 7), Interval(31, 39), Interval(4, 4),
         Interval(48, 58), Interval(61, 77), Interval(87, 91), Interval(3, 3), Interval(40, 40)],
        # Job 26
        [Interval(88, 108), Interval(73, 97), Interval(48, 54), Interval(9, 9), Interval(22, 26),
         Interval(7, 7), Interval(51, 67), Interval(90, 106), Interval(43, 57), Interval(91, 105),
         Interval(61, 67), Interval(29, 33), Interval(29, 33), Interval(26, 32), Interval(1, 1)],
        # Job 27
        [Interval(51, 67), Interval(62, 74), Interval(3, 3), Interval(8, 8), Interval(2, 2),
         Interval(8, 10), Interval(65, 73), Interval(14, 14), Interval(66, 78), Interval(77, 91),
         Interval(67, 71), Interval(54, 54), Interval(45, 45), Interval(53, 65), Interval(7, 7)],
        # Job 28
        [Interval(90, 94), Interval(19, 23), Interval(46, 60), Interval(60, 68), Interval(57, 61),
         Interval(72, 86), Interval(52, 52), Interval(12, 16), Interval(60, 62), Interval(79, 93),
         Interval(72, 92), Interval(87, 109), Interval(79, 87), Interval(22, 26), Interval(79, 95)],
        # Job 29
        [Interval(46, 56), Interval(70, 70), Interval(86, 102), Interval(68, 92), Interval(33, 37),
         Interval(56, 56), Interval(8, 8), Interval(94, 94), Interval(10, 12), Interval(3, 3),
         Interval(55, 65), Interval(67, 79), Interval(26, 26), Interval(21, 21), Interval(40, 50)],
    ],
    'name': 'INT__TAI30_15_01.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai30_15_01_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI30_15_01.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI30_15_01.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI30_15_01_F_15_01_INTERVAL_DATA
