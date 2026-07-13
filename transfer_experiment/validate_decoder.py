"""
Valida el decodificador: decodifica secuencias de un pool bajo aritmética de
INTERVALO y comprueba que reproduce EXACTAMENTE el [lo,up] guardado en el
pool (el mismo chequeo de consistencia que exige el piloto TS). Si cuadra,
el decodificador crisp/fuzzy (mismo esqueleto) es de fiar.
"""

import os
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "transfer_experiment")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from decode import decode_interval  # noqa: E402
from jobshop_rl.data import PROBLEM_REGISTRY  # noqa: E402


def check(pid, gen, n=200):
    prob = PROBLEM_REGISTRY[pid]()
    durs, mseq = prob["durations"], prob["sequences"]
    path = f"seeds/{pid}_{gen}_pool.csv"
    ok = bad = 0
    first_bad = None
    for i, line in enumerate(open(path, encoding="utf-8")):
        if i >= n or ";" not in line:
            break
        perm_s, interval_s = line.strip().split(";")
        seq = [int(x) for x in perm_s.split()]
        lo_exp, up_exp = (int(x) for x in interval_s.strip("[] ").split(","))
        mk = decode_interval(seq, durs, mseq)
        if int(mk.lower) == lo_exp and int(mk.upper) == up_exp:
            ok += 1
        else:
            bad += 1
            if first_bad is None:
                first_bad = (i, (lo_exp, up_exp), (int(mk.lower), int(mk.upper)))
    return ok, bad, first_bad


if __name__ == "__main__":
    total_ok = total_bad = 0
    for pid in ["int__tai15_15_05", "int__tai30_20_04", "int__tai50_20_02"]:
        for gen in ["v2", "gp"]:
            if not os.path.exists(f"seeds/{pid}_{gen}_pool.csv"):
                continue
            ok, bad, fb = check(pid, gen)
            total_ok += ok
            total_bad += bad
            estado = "OK" if bad == 0 else f"FALLO {fb}"
            print(f"{pid} {gen}: {ok} correctas, {bad} incorrectas | {estado}")
    print(f"\nTOTAL: {total_ok} OK, {total_bad} incorrectas")
    print("Decodificador VALIDADO" if total_bad == 0
          else "REVISAR decodificador")
