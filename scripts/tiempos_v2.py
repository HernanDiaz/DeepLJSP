# -*- coding: utf-8 -*-
"""Tiempos de la tabla de baselines (6.2) con las implementaciones de E6 v2.

La regla evolucionada se mide compilada (fast_regla) y cada baseline con
su despachador optimizado (fast_baselines), escritos con el mismo
cuidado y con exactamente los mismos schedules que las versiones de
scripts/tiempos_fast.py (tests/test_fast_regla.py y
tests/test_fast_baselines.py). Asi la columna de tiempos compara reglas,
no implementaciones.

Protocolo de tiempos_fast.py: seis copias a la vez (la carga con que
corrio E6), REPS pasadas por instancia, media sobre las 70 Taillard y
despues sobre las copias. Antes de cronometrar, cada metodo reproduce su
RE de la tabla; si no, se aborta.

  - los ocho baselines y el despachador aleatorio;
  - la regla destacada simplificada, Ec. (besttree), y tal como se
    evoluciono (gp_tuned_seed1);
  - la media de las 30 reglas del brazo principal.

    python scripts/tiempos_v2.py

Salida NUEVA: benchmarks/tiempos_v2.json
"""
import csv
import glob
import json
import os
import random
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, ".")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("OMP_NUM_THREADS", "1")

SALIDA = "benchmarks/tiempos_v2.json"
REPS = 5
COPIAS = 6


def mide(copia):
    from e6_presupuesto import ARBOL, setenta
    from jobshop_rl.data import PROBLEM_REGISTRY
    from jobshop_rl.data.literature_bounds import lb_for_problem_name
    from jobshop_rl.heuristics.fast_baselines import METODOS, despachador
    from jobshop_rl.heuristics.fast_regla import despachador as compila
    from jobshop_rl.heuristics.fast_sim import Instancia
    insts = setenta()
    datos = {p: Instancia(PROBLEM_REGISTRY[p]()) for p in insts}
    lbs = {p: lb_for_problem_name(p) for p in insts}

    def re_medio(d):
        return float(np.mean([((cm[0] + cm[1]) / 2 - lbs[p]) / lbs[p] * 100
                              for p in insts for cm in [d(datos[p])]]))

    def ms(d, **kw):
        v = []
        for p in insts:
            t0 = time.perf_counter()
            for _ in range(REPS):
                d(datos[p], **kw)
            v.append((time.perf_counter() - t0) / REPS * 1000)
        return float(np.mean(v))

    res = {}
    for metodo in METODOS:
        d = despachador(metodo)
        res[metodo] = {"re": re_medio(d), "ms": ms(d)}
    gp = compila(ARBOL)
    res["GP simplificada"] = {"re": re_medio(gp), "ms": ms(gp)}
    rng = random.Random(copia)
    res["Random"] = {"ms": ms(gp, eps=1.0, rng=rng)}
    reglas = sorted(glob.glob("benchmarks/reevo_fixedfit/gp_tuned_seed*.json"))
    assert len(reglas) == 30
    por_regla = []
    for f in reglas:
        d = compila(json.load(open(f, encoding="utf-8"))["tree"])
        por_regla.append({"regla": os.path.basename(f), "re": re_medio(d),
                          "ms": ms(d)})
    res["brazo"] = por_regla
    return res


def main():
    with ProcessPoolExecutor(max_workers=COPIAS) as ex:
        copias = list(ex.map(mide, range(COPIAS)))
    ref = {r["method"]: float(r["all"]) for r in csv.DictReader(
        open("benchmarks/all_baselines.csv", encoding="utf-8-sig"))}
    out = {"copias": COPIAS, "reps": REPS, "metodos": {}}
    for m in copias[0]:
        if m == "brazo":
            continue
        v = [c[m]["ms"] for c in copias]
        fila = {"ms_media": float(np.mean(v)), "ms_copias": v}
        if "re" in copias[0][m]:
            fila["re"] = copias[0][m]["re"]
            assert len({round(c[m]["re"], 6) for c in copias}) == 1, m
            if m in ref:
                assert abs(fila["re"] - ref[m]) < 0.01, (m, fila["re"], ref[m])
        out["metodos"][m] = fila
    assert abs(out["metodos"]["GP simplificada"]["re"] - 17.7142) < 0.001
    brazo_ms = [float(np.mean([c["brazo"][k]["ms"] for c in copias]))
                for k in range(30)]
    brazo_re = [copias[0]["brazo"][k]["re"] for k in range(30)]
    assert abs(np.mean(brazo_re) - 18.99) < 0.005, np.mean(brazo_re)
    assert copias[0]["brazo"][0]["regla"] == "gp_tuned_seed1.json"
    out["brazo"] = {"ms_por_regla": brazo_ms, "re_por_regla": brazo_re,
                    "ms_media": float(np.mean(brazo_ms)),
                    "re_media": float(np.mean(brazo_re)),
                    "ms_destacada_arbol": brazo_ms[0],
                    "re_destacada": brazo_re[0]}
    json.dump(out, open(SALIDA, "w", encoding="utf-8"), indent=1)
    for m, f in out["metodos"].items():
        print(f"{m:<16} {f['ms_media']:7.2f} ms  RE {f.get('re', float('nan')):7.2f}")
    print(f"{'GP media de 30':<16} {out['brazo']['ms_media']:7.2f} ms")
    print(f"{'GP destacada':<16} {out['brazo']['ms_destacada_arbol']:7.2f} ms")
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
