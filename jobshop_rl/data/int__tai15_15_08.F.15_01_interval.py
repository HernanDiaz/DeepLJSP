"""
Problema INT__TAI15_15_08.F.15_01_INTERVAL con incertidumbre en tiempos de procesamiento.

Esta versión utiliza duraciones con intervalos personalizados
para demostrar el manejo de incertidumbre.

Formato: Cada duración es un intervalo [lower, upper]
Algunas operaciones tienen incertidumbre (lower < upper)
Otras son determinísticas (lower = upper)
"""

from jobshop_rl.models.interval import Interval


INT__TAI15_15_08_F_15_01_INTERVAL_DATA = {
    'num_jobs': 15,
    'num_machines': 15,
    'problem_id': 'int__tai15_15_08.F.15_01_interval',
    'sequences': [
        [3, 6, 7, 13, 4, 1, 12, 10, 8, 14, 0, 9, 5, 2, 11],
        [2, 12, 1, 13, 3, 4, 8, 14, 0, 10, 7, 5, 9, 11, 6],
        [8, 14, 3, 0, 10, 5, 9, 13, 2, 11, 6, 4, 7, 1, 12],
        [5, 13, 11, 4, 14, 2, 9, 8, 10, 3, 6, 7, 1, 0, 12],
        [13, 5, 2, 14, 1, 8, 4, 3, 11, 6, 7, 12, 9, 0, 10],
        [14, 11, 2, 5, 8, 10, 0, 4, 9, 7, 13, 3, 1, 6, 12],
        [8, 12, 5, 10, 7, 11, 2, 13, 0, 14, 6, 9, 1, 4, 3],
        [9, 7, 12, 3, 6, 2, 10, 13, 1, 8, 14, 4, 0, 5, 11],
        [0, 4, 5, 1, 11, 7, 6, 2, 14, 13, 8, 9, 3, 10, 12],
        [8, 11, 7, 1, 14, 13, 12, 4, 6, 9, 10, 0, 5, 2, 3],
        [12, 4, 5, 13, 6, 0, 1, 7, 9, 8, 11, 10, 14, 2, 3],
        [3, 14, 4, 13, 5, 9, 8, 0, 7, 12, 6, 1, 10, 11, 2],
        [10, 8, 4, 1, 2, 0, 7, 14, 12, 13, 9, 6, 3, 11, 5],
        [6, 2, 0, 14, 1, 4, 12, 3, 10, 7, 8, 9, 5, 13, 11],
        [10, 2, 9, 13, 5, 0, 6, 7, 1, 14, 11, 4, 12, 3, 8],
    ],
    'durations': [
        # Job 0
        [Interval(82, 84), Interval(1, 1), Interval(95, 97), Interval(46, 62), Interval(29, 31),
         Interval(74, 86), Interval(70, 92), Interval(9, 9), Interval(45, 53), Interval(32, 32),
         Interval(17, 21), Interval(81, 103), Interval(62, 68), Interval(75, 101), Interval(64, 64)],
        # Job 1
        [Interval(4, 4), Interval(61, 75), Interval(71, 87), Interval(21, 21), Interval(77, 91),
         Interval(80, 104), Interval(62, 70), Interval(51, 51), Interval(71, 95), Interval(92, 100),
         Interval(60, 76), Interval(35, 41), Interval(36, 40), Interval(92, 106), Interval(68, 84)],
        # Job 2
        [Interval(40, 52), Interval(56, 58), Interval(60, 72), Interval(67, 83), Interval(80, 96),
         Interval(51, 65), Interval(49, 63), Interval(32, 38), Interval(55, 63), Interval(74, 90),
         Interval(23, 25), Interval(92, 100), Interval(21, 27), Interval(47, 63), Interval(71, 89)],
        # Job 3
        [Interval(29, 39), Interval(67, 71), Interval(46, 60), Interval(90, 106), Interval(7, 9),
         Interval(74, 88), Interval(80, 82), Interval(35, 41), Interval(36, 42), Interval(3, 3),
         Interval(59, 59), Interval(81, 81), Interval(28, 32), Interval(71, 81), Interval(70, 72)],
        # Job 4
        [Interval(79, 91), Interval(68, 92), Interval(34, 38), Interval(54, 60), Interval(95, 97),
         Interval(30, 38), Interval(14, 14), Interval(3, 3), Interval(78, 102), Interval(90, 108),
         Interval(9, 9), Interval(37, 47), Interval(84, 106), Interval(27, 27), Interval(24, 30)],
        # Job 5
        [Interval(24, 32), Interval(10, 12), Interval(57, 75), Interval(2, 2), Interval(32, 38),
         Interval(59, 79), Interval(59, 63), Interval(78, 90), Interval(71, 75), Interval(48, 64),
         Interval(94, 102), Interval(79, 83), Interval(72, 72), Interval(81, 103), Interval(23, 23)],
        # Job 6
        [Interval(19, 23), Interval(5, 5), Interval(83, 107), Interval(5, 5), Interval(19, 25),
         Interval(14, 18), Interval(67, 87), Interval(79, 91), Interval(66, 86), Interval(42, 50),
         Interval(36, 36), Interval(89, 89), Interval(99, 99), Interval(38, 50), Interval(37, 37)],
        # Job 7
        [Interval(44, 54), Interval(80, 80), Interval(58, 64), Interval(74, 100), Interval(39, 43),
         Interval(6, 6), Interval(81, 85), Interval(77, 81), Interval(42, 46), Interval(83, 83),
         Interval(9, 9), Interval(74, 94), Interval(90, 108), Interval(36, 40), Interval(62, 74)],
        # Job 8
        [Interval(77, 77), Interval(44, 58), Interval(62, 74), Interval(65, 73), Interval(6, 6),
         Interval(24, 28), Interval(85, 113), Interval(6, 6), Interval(30, 38), Interval(24, 30),
         Interval(51, 51), Interval(82, 82), Interval(5, 5), Interval(80, 100), Interval(1, 1)],
        # Job 9
        [Interval(74, 96), Interval(57, 71), Interval(50, 60), Interval(69, 83), Interval(80, 98),
         Interval(67, 69), Interval(29, 39), Interval(14, 14), Interval(50, 54), Interval(31, 35),
         Interval(87, 95), Interval(4, 4), Interval(16, 20), Interval(86, 104), Interval(65, 87)],
        # Job 10
        [Interval(34, 46), Interval(7, 9), Interval(36, 36), Interval(5, 5), Interval(1, 1),
         Interval(50, 52), Interval(29, 37), Interval(79, 81), Interval(87, 93), Interval(70, 80),
         Interval(41, 53), Interval(56, 74), Interval(41, 43), Interval(15, 17), Interval(11, 11)],
        # Job 11
        [Interval(36, 40), Interval(80, 86), Interval(44, 52), Interval(73, 75), Interval(15, 15),
         Interval(9, 11), Interval(76, 102), Interval(35, 47), Interval(93, 101), Interval(86, 108),
         Interval(16, 16), Interval(46, 48), Interval(19, 23), Interval(89, 101), Interval(18, 22)],
        # Job 12
        [Interval(83, 95), Interval(19, 25), Interval(11, 11), Interval(13, 17), Interval(35, 39),
         Interval(61, 69), Interval(25, 31), Interval(37, 41), Interval(84, 92), Interval(12, 16),
         Interval(26, 30), Interval(6, 6), Interval(22, 26), Interval(4, 4), Interval(21, 25)],
        # Job 13
        [Interval(14, 14), Interval(60, 72), Interval(4, 4), Interval(52, 64), Interval(7, 7),
         Interval(6, 6), Interval(5, 5), Interval(46, 50), Interval(46, 62), Interval(52, 66),
         Interval(2, 2), Interval(1, 1), Interval(4, 4), Interval(81, 83), Interval(67, 83)],
        # Job 14
        [Interval(21, 27), Interval(63, 69), Interval(4, 4), Interval(20, 20), Interval(78, 80),
         Interval(46, 54), Interval(20, 26), Interval(14, 16), Interval(12, 16), Interval(89, 93),
         Interval(77, 95), Interval(83, 109), Interval(56, 70), Interval(16, 16), Interval(3, 3)],
    ],
    'name': 'INT__TAI15_15_08.F.15_01_INTERVAL',
    'has_intervals': True,
    'description': 'Benchmark problem with custom interval processing times'
}


def get_int__tai15_15_08_f_15_01_interval_problem():
    """
    Obtiene los datos del problema INT__TAI15_15_08.F.15_01_INTERVAL con intervalos.
    
    Returns:
        Diccionario con los datos del problema INT__TAI15_15_08.F.15_01_INTERVAL con incertidumbre
    """
    return INT__TAI15_15_08_F_15_01_INTERVAL_DATA
