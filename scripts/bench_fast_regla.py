# -*- coding: utf-8 -*-
"""Cuanto gana la regla compilada (fast_regla) frente a fast_sim.despacha.

Mide, con la regla destacada del articulo, el coste por schedule de una
pasada y de una muestra del mejor-de-N (eps = 0.1), por las dos vias, en
las 12 clasicas y en la primera instancia de cada clase de Taillard.
Seis copias a la vez, como el resto de tiempos de E6; cada copia
comprueba ademas que las dos vias dan el mismo makespan.

Hay que correrlo con la maquina libre: si hay otro experimento en marcha
los tiempos no valen.

    python scripts/bench_fast_regla.py

Salida NUEVA: benchmarks/bench_fast_regla.json
"""
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

SALIDA = "benchmarks/bench_fast_regla.json"
COPIAS = 6
REPS = 40
EPS = 0.1
TAILLARD = [f"int__tai{c}_01" for c in
            ("15_15", "20_15", "20_20", "30_15", "30_20", "50_15", "50_20")]
CLASICAS = "zenodo_caie/instances/interval_classical"


def instancias():
    from jobshop_rl.data import PROBLEM_REGISTRY
    from jobshop_rl.heuristics.fast_sim import Instancia
    from time_classic12 import FILES, load
    d = {n: Instancia(load(os.path.join(CLASICAS, f), n)) for n, f in FILES.items()}
    d.update({p: Instancia(PROBLEM_REGISTRY[p]()) for p in TAILLARD})
    return d


def mide(copia):
    from e6_presupuesto import ARBOL
    from jobshop_rl.heuristics.fast_regla import despachador
    from jobshop_rl.heuristics.fast_sim import despacha, prioridad_de
    pol, rapido = prioridad_de(ARBOL), despachador(ARBOL)
    vias = {"actual": lambda inst, **kw: despacha(inst, pol, **kw),
            "compilada": rapido}
    res = {}
    for nombre, inst in instancias().items():
        fila = {}
        for via, f in vias.items():
            t0 = time.perf_counter()
            for _ in range(REPS):
                cm = f(inst)
            fila[f"una_{via}_ms"] = (time.perf_counter() - t0) / REPS * 1000
            fila[f"cm_{via}"] = cm
            rng = random.Random(copia)
            t0 = time.perf_counter()
            muestras = [f(inst, eps=EPS, rng=rng) for _ in range(REPS)]
            fila[f"bon_{via}_ms"] = (time.perf_counter() - t0) / REPS * 1000
            fila[f"muestras_{via}"] = muestras
        assert fila["cm_actual"] == fila["cm_compilada"], nombre
        assert fila["muestras_actual"] == fila["muestras_compilada"], nombre
        res[nombre] = {k: v for k, v in fila.items() if k.endswith("_ms")}
    return res


def main():
    with ProcessPoolExecutor(max_workers=COPIAS) as ex:
        copias = list(ex.map(mide, range(COPIAS)))
    out = {}
    print(f"{'instancia':<18}{'una: actual':>12}{'compilada':>11}{'x':>6}"
          f"{'muestra: actual':>17}{'compilada':>11}{'x':>6}")
    for nombre in copias[0]:
        m = {k: float(np.mean([c[nombre][k] for c in copias]))
             for k in copias[0][nombre]}
        m["x_una"] = m["una_actual_ms"] / m["una_compilada_ms"]
        m["x_bon"] = m["bon_actual_ms"] / m["bon_compilada_ms"]
        out[nombre] = m
        print(f"{nombre:<18}{m['una_actual_ms']:12.2f}{m['una_compilada_ms']:11.2f}"
              f"{m['x_una']:6.1f}{m['bon_actual_ms']:17.2f}"
              f"{m['bon_compilada_ms']:11.2f}{m['x_bon']:6.1f}")
    json.dump(out, open(SALIDA, "w", encoding="utf-8"), indent=1)
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
