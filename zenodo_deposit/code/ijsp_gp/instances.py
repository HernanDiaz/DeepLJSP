"""
Instance loading and reference bounds.

Two on-disk formats are supported, matching the files shipped in
``instances/``:

* Plain format (Taillard-derived sets)::

    # optional comment lines
    n m
    n rows with the machine sequence of each job
    n rows with durations: ``(lo,up)`` pairs for interval instances,
    plain integers for crisp instances

* Legacy format (classical set), with Spanish section headers
  (``NUMERO DE TRABAJOS`` etc.), kept verbatim from the original files.

Reference bounds: Taillard's published lower bounds for the Taillard-derived
instances; best-known bounds of the expected makespan for the classical set.
"""

import os
import re
from typing import Dict, Optional

from .interval import Interval

# ----------------------------------------------------------------------
# Taillard lower bounds (Taillard, 1993), indexed TA1..TA70
# ----------------------------------------------------------------------

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

_SIZE_OFFSET = {
    (15, 15): 0, (20, 15): 10, (20, 20): 20, (30, 15): 30,
    (30, 20): 40, (50, 15): 50, (50, 20): 60,
}

# Best-known lower bounds of the expected makespan for the classical set
CLASSICAL_LB = {
    "ABZ7": 656, "ABZ8": 645, "ABZ9": 661, "FT10": 930, "FT20": 1165,
    "La21": 1046, "La24": 935, "La25": 977, "La27": 1235, "La29": 1152,
    "La38": 1196, "La40": 1222,
}

# Mapping from the classical set's original file names to instance names
CLASSICAL_FILES = {
    "F0.15.0.ft10_10.txt": "FT10", "F0.15.0.ft20_05.txt": "FT20",
    "F0.15.0.la21_04.txt": "La21", "F0.15.0.la24_03.txt": "La24",
    "F0.15.0.la25_04.txt": "La25", "F0.15.0.la27_09.txt": "La27",
    "F0.15.0.la29_03.txt": "La29", "F0.15.0.la38_06.txt": "La38",
    "F0.15.0.la40_05.txt": "La40", "F0.15.0.abz7_06.txt": "ABZ7",
    "F0.15.0.abz8_05.txt": "ABZ8", "F0.15.0.abz9_10.txt": "ABZ9",
}


def ta_name(num_jobs: int, num_machines: int, index: int) -> str:
    offset = _SIZE_OFFSET[(num_jobs, num_machines)]
    return f"TA{offset + index}"


def lb_for_instance_name(name: str) -> Optional[int]:
    """Taillard LB for names like 'int__tai20_15_05' or 'tai20_15_05';
    classical LB for names like 'FT10'; None otherwise."""
    if name in CLASSICAL_LB:
        return CLASSICAL_LB[name]
    m = re.search(r"tai(\d+)_(\d+)_(\d+)", name.lower())
    if not m:
        return None
    nj, nm, idx = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if (nj, nm) not in _SIZE_OFFSET:
        return None
    return TAILLARD_LB[ta_name(nj, nm, idx)]


def load_instance(path: str, name: Optional[str] = None) -> Dict:
    """Load one instance file (either supported format)."""
    lines = [ln.strip() for ln in open(path, encoding="utf-8",
                                       errors="replace") if ln.strip()]
    lines = [ln for ln in lines if not ln.startswith("#")]
    if "NUMERO DE TRABAJOS" in lines:
        i = lines.index("NUMERO DE TRABAJOS"); n = int(lines[i + 1])
        i = lines.index("NUMERO DE RECURSOS"); m = int(lines[i + 1])
        i = lines.index("SECUENCIA DE MAQUINAS"); sq = lines[i + 1:i + 1 + n]
        i = lines.index("DURACIONES"); du = lines[i + 1:i + 1 + n]
    else:
        header = lines[0].split()
        if len(header) >= 2:
            # 'n m' on one line (the Taillard-derived exports)
            n, m = int(header[0]), int(header[1])
            sq = lines[1:1 + n]
            du = lines[1 + n:1 + 2 * n]
        else:
            # n and m on separate lines (part of the classical set)
            n = int(lines[0])
            m = int(lines[1])
            sq = lines[2:2 + n]
            du = lines[2 + n:2 + 2 * n]
    durations = []
    for ln in du:
        pairs = re.findall(r"\((\d+),\s*(\d+)\)", ln)
        if pairs:
            durations.append([Interval(int(a), int(b)) for a, b in pairs])
        else:
            durations.append([int(x) for x in ln.split()])
    stem = name or os.path.splitext(os.path.basename(path))[0]
    if stem in CLASSICAL_FILES.values():
        pass
    elif os.path.basename(path) in CLASSICAL_FILES:
        stem = CLASSICAL_FILES[os.path.basename(path)]
    return {"num_jobs": n, "num_machines": m, "problem_id": stem,
            "sequences": [[int(x) for x in ln.split()] for ln in sq],
            "durations": durations}


def load_dir(directory: str) -> Dict[str, Dict]:
    """Load every instance file in a directory, keyed by instance name."""
    out = {}
    for fn in sorted(os.listdir(directory)):
        if not fn.endswith(".txt"):
            continue
        name = CLASSICAL_FILES.get(fn, os.path.splitext(fn)[0])
        out[name] = load_instance(os.path.join(directory, fn), name)
    return out
