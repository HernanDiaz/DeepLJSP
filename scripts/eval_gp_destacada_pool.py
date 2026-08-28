# -*- coding: utf-8 -*-
"""Deposito muestreado de la regla GP destacada, con extremos.

El brazo GP muestreado debe salir de la MISMA regla que el paper
destaca y bajo el MISMO protocolo que la politica despliega, y debe
poder regenerarse entero desde este paquete. Este script lo produce:

- Regla: la destacada, benchmarks/reevo_fixedfit/gp_tuned_seed1.json,
  cuya pasada determinista sobre las 70 reproduce exactamente el
  $17.71\%$ que el paper imprime.
- Protocolo: el de 5.4, espejo del de la politica. El rollout 0 es la
  pasada determinista de la regla; los demas son epsilon-greedy con
  epsilon=0.1, el dispatching aleatorizado que el estudio de GP
  provee. El mejor-de-B se retiene por el criterio de la Eq. (3).
- Salida: los DOS extremos de cada rollout, para que cualquier
  presupuesto y cualquier criterio de retencion se recompute despues
  sin volver a evaluar, como ya se hizo con la curva de presupuesto.

Reanudable por (instancia): relanzar continua donde iba.

    python scripts/eval_gp_destacada_pool.py --carril 0 --de 6

Salida NUEVA: benchmarks/gp_destacada/pool_<carril>.csv
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
os.environ.setdefault("MKL_NUM_THREADS", "1")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data import PROBLEM_REGISTRY                   # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.heuristics.gp_rule import (                    # noqa: E402
    eval_tree, terminal_arrays)
from jobshop_rl.models.interval import Interval, final_makespan  # noqa: E402

REGLA = "benchmarks/reevo_fixedfit/gp_tuned_seed1.json"
N_POOL = 1024
EPSILON = 0.1
CLASES = ("tai15_15", "tai20_15", "tai20_20", "tai30_15", "tai30_20",
          "tai50_15", "tai50_20")
INSTANCIAS = sorted(p for p in PROBLEM_REGISTRY
                    if any(p.startswith(f"int__{c}_") for c in CLASES))


def rollout(env, tree, rng, determinista):
    """Un rollout; el determinista no consulta el generador."""
    state = env.reset()
    done = False
    while not done and state["eligible_ops"]:
        f = env.get_features(state)
        if not determinista and len(f) and rng.random() < EPSILON:
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
    ap.add_argument("--carril", type=int, required=True)
    ap.add_argument("--de", type=int, default=6)
    args = ap.parse_args()

    assert len(INSTANCIAS) == 70, f"{len(INSTANCIAS)} instancias"
    salida = f"benchmarks/gp_destacada/pool_{args.carril}.csv"
    os.makedirs(os.path.dirname(salida), exist_ok=True)
    tree = json.load(open(REGLA, encoding="utf-8"))["tree"]

    mias = [p for k, p in enumerate(INSTANCIAS) if k % args.de == args.carril]
    print(f"carril {args.carril}: {len(mias)} instancias")

    hechas = {}
    if os.path.exists(salida):
        for r in csv.DictReader(open(salida, encoding="utf-8")):
            hechas[r["instance"]] = hechas.get(r["instance"], 0) + 1

    nuevo = not os.path.exists(salida) or os.path.getsize(salida) == 0
    f = open(salida, "a", encoding="utf-8", newline="")
    w = csv.writer(f)
    if nuevo:
        w.writerow(["instance", "lb", "sample_idx", "lo", "up"])

    for pid in mias:
        if hechas.get(pid, 0) >= N_POOL:
            continue
        env = EnvironmentFactory.create_from_problem_id(pid, "adaptive",
                                                        seed=1)
        # semilla del muestreo fijada por la instancia, como en el
        # protocolo de la politica
        rng = np.random.default_rng(
            abs(int.from_bytes(pid.encode(), "little")) % (2 ** 31))
        lb = lb_for_problem_name(pid)
        t0 = time.time()
        for i in range(N_POOL):
            lo, up = rollout(env, tree, rng, determinista=(i == 0))
            w.writerow([pid, lb, i, f"{lo:.1f}", f"{up:.1f}"])
        f.flush()
        print(f"  {pid}: {N_POOL} rollouts en {time.time() - t0:.0f}s",
              flush=True)
    f.close()
    print("carril hecho")


if __name__ == "__main__":
    main()
