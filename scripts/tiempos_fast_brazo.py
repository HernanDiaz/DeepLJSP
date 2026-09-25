# -*- coding: utf-8 -*-
"""Tiempo de una pasada de las 30 reglas del brazo principal, con el
simulador rapido, para la fila 'GP rule (mean of 30)' de la tabla de
baselines. Se lanza en seis copias a la vez, como tiempos_fast.py, y
comprueba que la media de RE de las 30 es la del articulo (18.99).

    python scripts/tiempos_fast_brazo.py --out benchmarks/tiempos_brazo_0.json

Salida NUEVA: benchmarks/tiempos_brazo_<k>.json
"""
import argparse
import glob
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, ".")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from e6_presupuesto import setenta                                 # noqa: E402
from jobshop_rl.data import PROBLEM_REGISTRY                       # noqa: E402
from jobshop_rl.data.literature_bounds import (                    # noqa: E402
    lb_for_problem_name)
from jobshop_rl.heuristics.fast_sim import (                       # noqa: E402
    Instancia, despacha, prioridad_de)

REPS = 5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    insts = setenta()
    datos = {p: Instancia(PROBLEM_REGISTRY[p]()) for p in insts}
    lbs = {p: lb_for_problem_name(p) for p in insts}
    reglas = sorted(glob.glob("benchmarks/reevo_fixedfit/gp_tuned_seed*.json"))
    assert len(reglas) == 30, len(reglas)
    res, ms_reglas = [], []
    for f in reglas:
        pol = prioridad_de(json.load(open(f, encoding="utf-8"))["tree"])
        re_ = np.mean([((cm[0] + cm[1]) / 2 - lbs[p]) / lbs[p] * 100
                       for p in insts for cm in [despacha(datos[p], pol)]])
        res.append(float(re_))
        ms = []
        for p in insts:
            t0 = time.perf_counter()
            for _ in range(REPS):
                despacha(datos[p], pol)
            ms.append((time.perf_counter() - t0) / REPS * 1000)
        ms_reglas.append(float(np.mean(ms)))
        print(f"{os.path.basename(f)}: RE {re_:.2f}  {np.mean(ms):.1f} ms",
              flush=True)
    assert abs(np.mean(res) - 18.99) < 0.005, np.mean(res)
    json.dump({"re_media": float(np.mean(res)), "ms_por_regla": ms_reglas,
               "ms_media": float(np.mean(ms_reglas))},
              open(args.out, "w", encoding="utf-8"), indent=1)
    print(f"escrito {args.out}")


if __name__ == "__main__":
    main()
