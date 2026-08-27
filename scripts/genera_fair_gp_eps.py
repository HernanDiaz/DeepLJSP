# -*- coding: utf-8 -*-
"""Regenera la evaluacion muestreada de la regla GP destacada.

benchmarks/fair_gp_eps.csv es fuente primaria de las filas GP de la
tabla de las 70 y del enfrentamiento, y venia del arnes del estudio
companero de GP, sin productor en este arbol: la revision del
2026-08-27 lo senalo. Este script reimplementa su protocolo aqui.

Protocolo, el mismo que el paper describe para el brazo GP muestreado:
por instancia, 1024 rollouts de la regla destacada con el dispatching
epsilon-greedy de su estudio (epsilon=0.1); best_at_N es el minimo
sobre los N primeros bajo el criterio lexicografico de la Eq. (3), y
la columna mean promedia los 1024. El RE se reporta en punto medio.

ATENCION a la procedencia: la semilla del muestreo original no viaja
con el fichero depositado, asi que esta reimplementacion reproduce el
protocolo y la distribucion, no la realizacion exacta. Por eso escribe
en una ruta NUEVA y no toca el registro que el paper usa.

    python scripts/genera_fair_gp_eps.py --instancias 3   (prueba)
    python scripts/genera_fair_gp_eps.py                  (las 70)

Salida NUEVA: benchmarks/fair_gp_eps_regen.csv (reanudable)
"""
import argparse
import csv
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, ".")
os.environ.setdefault("OMP_NUM_THREADS", "1")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data import PROBLEM_REGISTRY                   # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.heuristics.gp_rule import (                    # noqa: E402
    eval_tree, terminal_arrays)
from jobshop_rl.models.interval import Interval, final_makespan  # noqa: E402

REGLA = "benchmarks/reevo_fixedfit/gp_tuned_seed1.json"
SALIDA = "benchmarks/fair_gp_eps_regen.csv"
N_POOL = 1024
EPSILON = 0.1
CORTES = (1, 16, 64, 256, 1024)
CLASES = ("tai15_15", "tai20_15", "tai20_20", "tai30_15", "tai30_20",
          "tai50_15", "tai50_20")


def instancias():
    return sorted(p for p in PROBLEM_REGISTRY
                  if any(p.startswith(f"int__{c}_") for c in CLASES))


def clase_de(pid):
    return pid.replace("int__tai", "").rsplit("_", 1)[0]


def rollout(env, tree, rng):
    """Un rollout epsilon-greedy; devuelve (lower, upper) del makespan."""
    state = env.reset()
    done = False
    while not done and state["eligible_ops"]:
        f = env.get_features(state)
        if len(f) and rng.random() < EPSILON:
            idx = int(rng.integers(len(state["eligible_ops"])))
        else:
            idx = int(np.argmin(eval_tree(tree, terminal_arrays(f))))
        idx = min(idx, len(state["eligible_ops"]) - 1)
        state, _, done, _ = env.step(idx)
    m = final_makespan(env.job_completion_time)
    if isinstance(m, Interval):
        return float(m.lower), float(m.upper)
    return float(m), float(m)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instancias", type=int, default=0,
                    help="solo las N primeras (prueba); 0 = todas")
    args = ap.parse_args()

    tree = json.load(open(REGLA, encoding="utf-8"))["tree"]
    pids = instancias()
    if args.instancias:
        pids = pids[:args.instancias]

    hechas = set()
    if os.path.exists(SALIDA):
        for r in csv.DictReader(open(SALIDA, encoding="utf-8")):
            hechas.add(r["instance"])
    nuevo = not os.path.exists(SALIDA) or os.path.getsize(SALIDA) == 0
    out = open(SALIDA, "a", encoding="utf-8", newline="")
    w = csv.writer(out)
    if nuevo:
        w.writerow(["instance", "cls"]
                   + [f"best_at_{n}" for n in CORTES] + ["mean"])

    for pid in pids:
        if pid in hechas:
            continue
        env = EnvironmentFactory.create_from_problem_id(pid, "adaptive",
                                                        seed=1)
        rng = np.random.default_rng(abs(hash(pid)) % (2 ** 31))
        lb = lb_for_problem_name(pid)
        t0 = time.time()
        pool = [rollout(env, tree, rng) for _ in range(N_POOL)]
        re_de = lambda p: ((p[0] + p[1]) / 2 - lb) / lb * 100
        fila = [pid, clase_de(pid)]
        for n in CORTES:
            mejor = min(pool[:n], key=lambda p: (p[1], p[0]))
            fila.append(f"{re_de(mejor):.4f}")
        fila.append(f"{sum(re_de(p) for p in pool) / len(pool):.4f}")
        w.writerow(fila)
        out.flush()
        print(f"  {pid}: best@1024={fila[-2]} mean={fila[-1]} "
              f"({time.time() - t0:.0f}s)", flush=True)
    out.close()
    print("hecho")


if __name__ == "__main__":
    main()
