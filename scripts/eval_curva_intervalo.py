# -*- coding: utf-8 -*-
"""Deposito de la curva de presupuesto con los extremos del intervalo.

Reejecucion de la campana de la curva (2026-08-17) guardando el
makespan componentwise completo de cada rollout, no solo su punto
medio: la revision del 2026-08-25 (R2-2) mostro que sin los extremos
el analisis no puede reproducir el decodificador desplegado de 5.4
(greedy incluido en el pool y seleccion por (U, L)). Cubre las DIEZ
semillas 2-11 del brazo principal: las 2-4 (campana base) y las 5-11
(ext-c), de modo que el deposito nuevo es autonomo y
benchmarks/curva_diez/ y benchmarks/eval_budget_curve.csv quedan
intactos como registro.

Por (tirada, instancia): 342 rollouts, el 0 greedy y el resto
muestreados, mismas semillas de entorno/agente que la campana
original. Cada carril escribe su fichero y es reanudable.

    python scripts/eval_curva_intervalo.py --carril 0 --de 6

Salida NUEVA: benchmarks/curva_intervalo/curva_<carril>.csv
"""
import argparse
import csv
import glob
import os
import sys
import time

sys.path.insert(0, ".")
os.environ.pop("DEEPLJSP_V2_LAMBDA", None)
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.agents_v2 import AgentV2                       # noqa: E402
from jobshop_rl.data import PROBLEM_REGISTRY                   # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.models.interval import Interval, final_makespan  # noqa: E402

N_MUESTRAS = 342
SEMILLAS = list(range(2, 12))
ULTIMA = "INT__TAI20_15_04.F.15_01_INTERVAL_model.pt"
TAGS = ("v2-full-1000ep", "v2-full-1000ep-ext-c")
CLASES = ("tai15_15", "tai20_15", "tai20_20", "tai30_15", "tai30_20",
          "tai50_15", "tai50_20")
INSTANCIAS = sorted(p for p in PROBLEM_REGISTRY
                    if any(p.startswith(f"int__{c}_") for c in CLASES))


def checkpoint_de(semilla):
    for tag in TAGS:
        for d in glob.glob(f"outputs/bench_{tag}__*_seed{semilla}"):
            p = os.path.join(d, ULTIMA)
            if os.path.exists(p):
                return p
    return None


def makespan_extremos(env):
    m = final_makespan(env.job_completion_time)
    if isinstance(m, Interval):
        return float(m.lower), float(m.upper)
    return float(m), float(m)


def rollouts(ckpt, instancia, n):
    problem = PROBLEM_REGISTRY[instancia]()
    env = EnvironmentFactory.create_from_problem(problem, "adaptive", seed=1)
    agent = AgentV2(env, seed=1, attention_layers=0)
    agent.load_checkpoint(ckpt)
    out = []
    for i in range(n):
        state = env.reset()
        done = False
        while not done and state["eligible_ops"]:
            salida = agent.select_action(state, training=(i > 0))
            a = salida[0] if isinstance(salida, tuple) else salida
            state, _, done, _ = env.step(
                min(int(a), len(state["eligible_ops"]) - 1))
        out.append(makespan_extremos(env))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--carril", type=int, required=True)
    ap.add_argument("--de", type=int, default=6)
    args = ap.parse_args()
    salida = f"benchmarks/curva_intervalo/curva_{args.carril}.csv"
    os.makedirs(os.path.dirname(salida), exist_ok=True)

    assert len(INSTANCIAS) == 70, f"{len(INSTANCIAS)} instancias"
    unidades = [(s, inst) for s in SEMILLAS for inst in INSTANCIAS]
    unidades = [u for k, u in enumerate(unidades)
                if k % args.de == args.carril]
    print(f"carril {args.carril}: {len(unidades)} pares (semilla, "
          f"instancia)")

    hechos = {}
    if os.path.exists(salida):
        for r in csv.DictReader(open(salida, encoding="utf-8")):
            k = (r["checkpoint"], r["instance"])
            hechos[k] = hechos.get(k, 0) + 1

    nuevo = not os.path.exists(salida) or os.path.getsize(salida) == 0
    f = open(salida, "a", encoding="utf-8", newline="")
    w = csv.writer(f)
    if nuevo:
        w.writerow(["checkpoint", "instance", "lb", "sample_idx",
                    "lo", "up"])
    for s, inst in unidades:
        etiqueta = f"seed{s}"
        if hechos.get((etiqueta, inst), 0) >= N_MUESTRAS:
            continue
        ckpt = checkpoint_de(s)
        if ckpt is None:
            print(f"  AVISO: sin checkpoint para semilla {s}")
            continue
        lb = lb_for_problem_name(inst)
        t0 = time.time()
        for i, (lo, up) in enumerate(rollouts(ckpt, inst, N_MUESTRAS)):
            w.writerow([etiqueta, inst, lb, i, f"{lo:.1f}", f"{up:.1f}"])
        f.flush()
        print(f"  seed{s} {inst}: {N_MUESTRAS} en "
              f"{time.time() - t0:.0f}s", flush=True)
    f.close()
    print("carril hecho")


if __name__ == "__main__":
    main()
