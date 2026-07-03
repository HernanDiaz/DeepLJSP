"""
Límites inferiores crisp publicados (Taillard 1993) para las instancias IJSP.

Referencia estándar del campo: RE(%) = (E[C_max] − LB)/LB × 100, donde
E[C_max] es el punto medio del intervalo de makespan y LB es el límite
inferior del problema Taillard determinista original. Los LB son indicativos
para el setting de intervalos (no constituyen gap estricto de optimalidad).

Mapeo: tai{J}_{M}_{XX} del repositorio = TA(offset + XX) de Taillard, con
offsets por clase de tamaño: 15x15→TA1-10, 20x15→TA11-20, 20x20→TA21-30,
30x15→TA31-40, 30x20→TA41-50, 50x15→TA51-60, 50x20→TA61-70.
"""

# LB crisp por instancia TA (Taillard 1993, según el suplemento de Díaz et al.)
TAILLARD_LB = {
    # 15x15 (TA1-10)
    "TA1": 1231, "TA2": 1244, "TA3": 1218, "TA4": 1175, "TA5": 1224,
    "TA6": 1238, "TA7": 1227, "TA8": 1217, "TA9": 1274, "TA10": 1241,
    # 20x15 (TA11-20)
    "TA11": 1357, "TA12": 1367, "TA13": 1342, "TA14": 1345, "TA15": 1339,
    "TA16": 1360, "TA17": 1462, "TA18": 1377, "TA19": 1332, "TA20": 1348,
    # 20x20 (TA21-30)
    "TA21": 1642, "TA22": 1561, "TA23": 1518, "TA24": 1644, "TA25": 1558,
    "TA26": 1591, "TA27": 1652, "TA28": 1603, "TA29": 1583, "TA30": 1528,
    # 30x15 (TA31-40)
    "TA31": 1764, "TA32": 1774, "TA33": 1788, "TA34": 1828, "TA35": 2007,
    "TA36": 1819, "TA37": 1771, "TA38": 1673, "TA39": 1795, "TA40": 1651,
    # 30x20 (TA41-50)
    "TA41": 1906, "TA42": 1884, "TA43": 1809, "TA44": 1948, "TA45": 1997,
    "TA46": 1957, "TA47": 1807, "TA48": 1912, "TA49": 1931, "TA50": 1833,
    # 50x15 (TA51-60)
    "TA51": 2760, "TA52": 2756, "TA53": 2717, "TA54": 2839, "TA55": 2679,
    "TA56": 2781, "TA57": 2943, "TA58": 2885, "TA59": 2655, "TA60": 2723,
    # 50x20 (TA61-70)
    "TA61": 2868, "TA62": 2869, "TA63": 2755, "TA64": 2702, "TA65": 2725,
    "TA66": 2845, "TA67": 2825, "TA68": 2784, "TA69": 3071, "TA70": 2995,
}

# Offset TA por clase de tamaño (num_jobs, num_machines)
_SIZE_OFFSET = {
    (15, 15): 0, (20, 15): 10, (20, 20): 20, (30, 15): 30,
    (30, 20): 40, (50, 15): 50, (50, 20): 60,
}


def ta_name(num_jobs: int, num_machines: int, index: int) -> str:
    """Nombre TA de una instancia taiJ_M_XX (index = XX, 1-based)."""
    offset = _SIZE_OFFSET[(num_jobs, num_machines)]
    return f"TA{offset + index}"


def literature_lb(num_jobs: int, num_machines: int, index: int) -> int:
    """LB crisp publicado para la instancia taiJ_M_XX."""
    return TAILLARD_LB[ta_name(num_jobs, num_machines, index)]


def lb_for_problem_name(name: str):
    """
    LB para nombres del repo tipo 'INT__TAI20_15_05.F.15_01_INTERVAL' o
    'int__tai20_15_05'. Devuelve None si no es una instancia Taillard.
    """
    import re
    m = re.search(r"tai(\d+)_(\d+)_(\d+)", name.lower())
    if not m:
        return None
    nj, nm, idx = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if (nj, nm) not in _SIZE_OFFSET:
        return None
    return literature_lb(nj, nm, idx)
