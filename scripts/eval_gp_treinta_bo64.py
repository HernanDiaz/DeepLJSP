# -*- coding: utf-8 -*-
"""Deposito muestreado de las TREINTA reglas GP a presupuesto 64.

El contraste muestreado de las setenta Taillard enfrentaba un
checkpoint contra una regla, de modo que el Wilcoxon medía variación
entre instancias y no entre artefactos: no sostiene por si solo una
afirmacion sobre paradigmas. El lado de la politica ya tiene diez
artefactos en benchmarks/curva_intervalo (342 rollouts por (tirada,
instancia), de los que el mejor-de-64 se lee sin evaluar nada). Este
script produce el lado que falta: las treinta reglas del brazo
principal, cada una con su propio pool de 64 rollouts por instancia.

- Reglas: benchmarks/reevo_fixedfit/gp_tuned_seed{1..30}.json, las
  mismas treinta que el estudio de GP publica.
- Protocolo: el de 5.4, espejo del de la politica. El rollout 0 es la
  pasada determinista de la regla; los 63 restantes son epsilon-greedy
  con epsilon=0.1, el dispatching aleatorizado del estudio de GP.
- Semilla del muestreo fijada por (regla, instancia): cada artefacto
  gasta su propio presupuesto, como haria uno desplegado, en vez de
  compartir sorteos con los demas.
- Salida: los DOS extremos de cada rollout, para que cualquier
  presupuesto <=64 y cualquier criterio de retencion se recompute
  despues sin volver a evaluar.

Reanudable por (regla, instancia): relanzar continua donde iba.

    python scripts/eval_gp_treinta_bo64.py --carril 0 --de 6

Salida NUEVA: benchmarks/gp_treinta_bo64/pool_<carril>.csv
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
from jobshop_rl.data.literature_bounds import (                # noqa: E402
    lb_for_problem_name)
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.heuristics.gp_rule import (                    # noqa: E402
    eval_tree, terminal_arrays)
from jobshop_rl.models.interval import (                       # noqa: E402
    Interval, final_makespan)

DIR_REGLAS = "benchmarks/reevo_fixedfit"
SEMILLAS = list(range(1, 31))
N_POOL = 64
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


def semilla_de(pid, sem):
    base = abs(int.from_bytes(pid.encode(), "little")) % (2 ** 31)
    return (base ^ (sem * 2654435761)) % (2 ** 31)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--carril", type=int, required=True)
    ap.add_argument("--de", type=int, default=6)
    args = ap.parse_args()

    assert len(INSTANCIAS) == 70, f"{len(INSTANCIAS)} instancias"
    salida = f"benchmarks/gp_treinta_bo64/pool_{args.carril}.csv"
    os.makedirs(os.path.dirname(salida), exist_ok=True)

    arboles = {}
    for sem in SEMILLAS:
        ruta = os.path.join(DIR_REGLAS, f"gp_tuned_seed{sem}.json")
        arboles[sem] = json.load(open(ruta, encoding="utf-8"))["tree"]

    # el carril reparte los pares (regla, instancia), no las instancias:
    # asi las clases grandes, que son las caras, se reparten parejo
    pares = [(sem, pid) for sem in SEMILLAS for pid in INSTANCIAS]
    mios = [p for k, p in enumerate(pares) if k % args.de == args.carril]
    print(f"carril {args.carril}: {len(mios)} pares (regla, instancia)",
          flush=True)

    hechos = {}
    if os.path.exists(salida):
        for r in csv.DictReader(open(salida, encoding="utf-8")):
            k = (int(r["rule_seed"]), r["instance"])
            hechos[k] = hechos.get(k, 0) + 1

    nuevo = not os.path.exists(salida) or os.path.getsize(salida) == 0
    f = open(salida, "a", encoding="utf-8", newline="")
    w = csv.writer(f)
    if nuevo:
        w.writerow(["rule_seed", "instance", "lb", "sample_idx", "lo", "up"])

    t_ini, hechas = time.time(), 0
    for sem, pid in mios:
        if hechos.get((sem, pid), 0) >= N_POOL:
            continue
        env = EnvironmentFactory.create_from_problem_id(pid, "adaptive",
                                                        seed=1)
        rng = np.random.default_rng(semilla_de(pid, sem))
        lb = lb_for_problem_name(pid)
        t0 = time.time()
        for i in range(N_POOL):
            lo, up = rollout(env, arboles[sem], rng, determinista=(i == 0))
            w.writerow([sem, pid, lb, i, f"{lo:.1f}", f"{up:.1f}"])
        f.flush()
        hechas += 1
        print(f"  seed{sem} {pid}: {N_POOL} rollouts en "
              f"{time.time() - t0:.0f}s  [{hechas}/{len(mios)}, "
              f"{(time.time() - t_ini) / 60:.0f} min]", flush=True)
    f.close()
    print("carril hecho", flush=True)


if __name__ == "__main__":
    main()
