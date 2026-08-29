# -*- coding: utf-8 -*-
"""Depositos de rollouts de los brazos robustos reentrenados.

Mismo protocolo que eval_robust_lambda.py y eval_lambda_sweep_rollouts
.py: 64 rollouts por (brazo, semilla, instancia) sobre TA15-TA20 con
los dos extremos de cada makespan, evaluacion sin lambda a la vista.
Cubre los cinco brazos en sus tags de extension. Cada carril escribe
su propio fichero (reanudable); el analisis los funde con los dos
depositos originales, que no se tocan.

    python scripts/eval_lambda_fix_rollouts.py --carril 0 --de 6

Salida NUEVA: benchmarks/robust_lambda_fix/rollouts_<carril>.csv
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
from jobshop_rl.data.literature_bounds import (                # noqa: E402
    lb_for_problem_name)
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.models.interval import Interval, final_makespan  # noqa: E402

DESARROLLO = [f"int__tai20_15_{k:02d}" for k in range(5, 11)]
N_MUESTRAS = 64
ULTIMA = "INT__TAI20_15_04.F.15_01_INTERVAL_model.pt"
SEMILLAS = list(range(2, 12))
BRAZOS = [("lam0p5", ["v2-robust-lam0p5-fix"]),
          ("lam1", ["v2-robust-lam1-fix"]),
          ("lam2", ["v2-robust-lam2-fix"]),
          ("lam4", ["v2-robust-lam4-fix"])]


def checkpoints():
    out = []
    for arm, tags in BRAZOS:
        for s in SEMILLAS:
            rutas = []
            for tag in tags:
                for d in glob.glob(f"outputs/bench_{tag}__*_seed{s}"):
                    p = os.path.join(d, ULTIMA)
                    if os.path.exists(p) and os.path.exists(
                            os.path.join(d, "best_model.pt")):
                        rutas.append(p)
            if rutas:
                out.append((arm, s, sorted(rutas)[-1]))
            else:
                print(f"  AVISO: sin checkpoint para {arm} semilla {s}")
    return out


def extremos(env):
    m = final_makespan(env.job_completion_time)
    if isinstance(m, Interval):
        return float(m.lower), float(m.upper)
    return float(m), float(m)


def rollouts(ruta, instancia, n):
    problem = PROBLEM_REGISTRY[instancia]()
    env = EnvironmentFactory.create_from_problem(problem, "adaptive", seed=1)
    agent = AgentV2(env, seed=1, attention_layers=0)
    agent.load_checkpoint(ruta)
    out = []
    for i in range(n):
        state = env.reset()
        done = False
        while not done and state["eligible_ops"]:
            salida = agent.select_action(state, training=(i > 0))
            a = salida[0] if isinstance(salida, tuple) else salida
            state, _, done, _ = env.step(
                min(int(a), len(state["eligible_ops"]) - 1))
        out.append(extremos(env))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--carril", type=int, required=True)
    ap.add_argument("--de", type=int, default=6)
    args = ap.parse_args()
    salida = f"benchmarks/robust_lambda_fix/rollouts_{args.carril}.csv"
    os.makedirs(os.path.dirname(salida), exist_ok=True)

    unidades = [(a, s, r) for k, (a, s, r) in enumerate(checkpoints())
                if k % args.de == args.carril]
    print(f"carril {args.carril}: {len(unidades)} unidades (brazo, semilla)")

    hechos = {}
    if os.path.exists(salida):
        for r in csv.DictReader(open(salida, encoding="utf-8")):
            k = (r["arm"], r["seed"], r["instance"])
            hechos[k] = hechos.get(k, 0) + 1

    nuevo = not os.path.exists(salida) or os.path.getsize(salida) == 0
    f = open(salida, "a", encoding="utf-8", newline="")
    w = csv.writer(f)
    if nuevo:
        w.writerow(["arm", "seed", "instance", "lb", "sample_idx",
                    "lower", "upper"])
    for brazo, s, ruta in unidades:
        for instancia in DESARROLLO:
            if hechos.get((brazo, str(s), instancia), 0) >= N_MUESTRAS:
                continue
            lb = lb_for_problem_name(instancia)
            t0 = time.time()
            for i, (lo, up) in enumerate(rollouts(ruta, instancia,
                                                  N_MUESTRAS)):
                w.writerow([brazo, s, instancia, lb, i,
                            f"{lo:.1f}", f"{up:.1f}"])
            f.flush()
            print(f"  {brazo} s{s} {instancia}: {N_MUESTRAS} en "
                  f"{time.time() - t0:.0f}s", flush=True)
    f.close()
    print("carril hecho")


if __name__ == "__main__":
    main()
