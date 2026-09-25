# -*- coding: utf-8 -*-
"""Tiempos de todos los metodos con el simulador rapido de E6.

Los tiempos de la tabla de baselines (6.2) y de 6.4 se midieron con el
entorno general de jobshop_rl, que en cada decision construye la matriz
de atributos con objetos Interval, y la comparacion por presupuesto de
6.5 con jobshop_rl/heuristics/fast_sim.py, unas diez veces mas rapido.
Dos escalas de tiempo en el mismo articulo no tienen sentido: aqui se
miden todos con el simulador rapido.

Cada baseline se reimplementa como politica del simulador con la misma
semantica que jobshop_rl/heuristics/strategies.py: comparacion
lexicografica de intervalos (superior, luego inferior), empates al primer
elegible. Antes de cronometrar se comprueba que cada una reproduce el RE
de benchmarks/all_baselines.csv en las 70 instancias; si no, se aborta.

  - Taillard (tabla de baselines): una pasada de cada metodo, REPS
    repeticiones por instancia; el despachador aleatorio, REPS pasadas.
  - Clasicas (6.4): una pasada de la regla y su mejor-de-1024.

    python scripts/tiempos_fast.py

Salida NUEVA: benchmarks/tiempos_fast.json
"""
import csv
import json
import os
import random
import re
import sys
import time

import numpy as np

sys.path.insert(0, ".")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from e6_presupuesto import ARBOL, EPS, setenta                    # noqa: E402
from jobshop_rl.data import PROBLEM_REGISTRY                      # noqa: E402
from jobshop_rl.data.literature_bounds import (                   # noqa: E402
    lb_for_problem_name)
from jobshop_rl.heuristics.fast_sim import (                      # noqa: E402
    Instancia, despacha, mejor, prioridad_de)

SALIDA = "benchmarks/tiempos_fast.json"
REPS = 5


# ---- comparacion lexicografica, como strategies._lexicographic_compare
def _mejor_min(a, b):
    """a estrictamente preferible a b al minimizar (sup, luego inf)."""
    return a[0] < b[0] or (a[0] == b[0] and a[1] < b[1])


def _arg(claves, minimiza):
    """Indice del primer elegible optimo en orden lexicografico."""
    k = 0
    for i in range(1, len(claves)):
        a, b = claves[i], claves[k]
        if minimiza and _mejor_min(a, b):
            k = i
        elif not minimiza and _mejor_min(b, a):
            k = i
    return k


def _pt(t):
    return [(u, u - w) for u, w in zip(t["PT"], t["PTW"])]


def _wkr(t):
    return [(u, u - w) for u, w in zip(t["WKR"], t["WKRW"])]


def _est(t):
    return list(zip(t["EST"], t["_EST_LO"]))


def spt(t):
    return _arg(_pt(t), True)


def lpt(t):
    return _arg(_pt(t), False)


def est(t):
    return _arg(_est(t), True)


def mwkr(t):
    return _arg(_wkr(t), False)


def mor(t):
    return int(np.argmax(t["NOR"]))


def cr(t):
    return int(np.argmin([w / (n + 1e-10) for w, n in zip(t["WKR"], t["NOR"])]))


def gt(desempate):
    """Giffler y Thompson de strategies.GTHeuristic, con desempate SPT o
    MWKR dentro del conflict set, todo en orden lexicografico."""
    def politica(t):
        s = _est(t)
        p = _pt(t)
        fin = [(a[0] + b[0], a[1] + b[1]) for a, b in zip(s, p)]
        c = _arg(fin, True)
        maq = t["_MAQ"]
        conf = [i for i in range(len(s))
                if maq[i] == maq[c] and _mejor_min(s[i], fin[c])]
        if not conf:
            conf = [c]
        claves = p if desempate == "spt" else _wkr(t)
        mejor_i = conf[0]
        for i in conf[1:]:
            if desempate == "spt" and _mejor_min(claves[i], claves[mejor_i]):
                mejor_i = i
            if desempate == "mwkr" and _mejor_min(claves[mejor_i], claves[i]):
                mejor_i = i
        return mejor_i
    return politica


def re_(cm, lb):
    return ((cm[0] + cm[1]) / 2 - lb) / lb * 100


def main():
    import argparse
    ap = argparse.ArgumentParser()
    # seis copias a la vez reproducen la carga con que se midio E6
    ap.add_argument("--out", default=SALIDA)
    args = ap.parse_args()
    insts = setenta()
    datos = {p: Instancia(PROBLEM_REGISTRY[p]()) for p in insts}
    lbs = {p: lb_for_problem_name(p) for p in insts}
    gp = prioridad_de(ARBOL)
    metodos = [("SPT", spt), ("LPT", lpt), ("EST", est), ("CR", cr),
               ("MWKR", mwkr), ("MOR", mor), ("G&T-SPT", gt("spt")),
               ("G&T-MWKR", gt("mwkr")), ("GP rule", gp)]

    # 1. cada baseline reproduce su RE publicado
    ref = {r["method"]: float(r["all"]) for r in
           csv.DictReader(open("benchmarks/all_baselines.csv", encoding="utf-8-sig"))}
    ref["GP rule"] = 17.714164285714283
    res = {"taillard": {}, "clasicas": {}}
    for nombre, pol in metodos:
        v = np.mean([re_(despacha(datos[p], pol), lbs[p]) for p in insts])
        print(f"{nombre:<9} RE {v:8.2f}  (tabla {ref[nombre]:.2f})")
        assert abs(v - ref[nombre]) < 0.01, f"{nombre} no reproduce la tabla"
        res["taillard"][nombre] = {"re": float(v)}

    # 2. tiempos en Taillard
    for nombre, pol in metodos + [("Random", None)]:
        ms = []
        for p in insts:
            rng = random.Random(0)
            t0 = time.perf_counter()
            for _ in range(REPS):
                if pol is None:
                    despacha(datos[p], gp, eps=1.0, rng=rng)
                else:
                    despacha(datos[p], pol)
            ms.append((time.perf_counter() - t0) / REPS * 1000)
        res["taillard"].setdefault(nombre, {}).update(
            {"ms_media": float(np.mean(ms)), "ms_min": float(np.min(ms)),
             "ms_max": float(np.max(ms))})
        print(f"{nombre:<9} {np.mean(ms):8.1f} ms ({np.min(ms):.1f}-{np.max(ms):.1f})")

    # 3. clasicas: una pasada y el mejor-de-1024 de la regla
    sys.path.insert(0, "scripts")
    from time_classic12 import FILES, load
    # los ficheros de E:\Experimentos\Selectos, tal como van al deposito
    DIR = "zenodo_caie/instances/interval_classical"
    for nombre, fichero in FILES.items():
        inst = Instancia(load(os.path.join(DIR, fichero), nombre))
        t0 = time.perf_counter()
        for _ in range(20):
            despacha(inst, gp)
        una = (time.perf_counter() - t0) / 20
        rng = random.Random(1)
        t0 = time.perf_counter()
        mejor_cm = despacha(inst, gp)
        for _ in range(1023):
            cm = despacha(inst, gp, eps=EPS, rng=rng)
            if mejor(cm, mejor_cm):
                mejor_cm = cm
        bon = time.perf_counter() - t0
        res["clasicas"][nombre] = {"una_s": una, "bon1024_s": bon}
        print(f"{nombre:<5} una {una * 1000:6.1f} ms  mejor-de-1024 {bon:6.1f} s")

    json.dump(res, open(args.out, "w", encoding="utf-8"), indent=1)
    print(f"escrito {args.out}")


if __name__ == "__main__":
    main()
