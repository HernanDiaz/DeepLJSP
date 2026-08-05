# -*- coding: utf-8 -*-
"""Depositos de rollouts para los brazos del barrido de lambda.

El barrido (lam 0.5, 2, 4; tres semillas) ya esta entrenado. Sus
schedules guardados se seleccionaron con el objetivo propio de cada
brazo, asi que sirven para la frontera DESPLEGADA; pero el control que
separa entrenamiento de seleccion -- reconstruir el mejor-de-64 de cada
brazo bajo un criterio comun -- necesita los rollouts individuales con
sus dos extremos, como hizo eval_robust_lambda.py para lam=1.

Mismo protocolo que aquel: 64 rollouts por (brazo, semilla, instancia)
sobre TA15-TA20, guardando lower y upper de cada uno. base y lam1 ya
estan en benchmarks/robust_lambda/rollouts.csv; aqui van los tres
brazos nuevos a un fichero propio, sin tocar el anterior.

    python scripts/eval_lambda_sweep_rollouts.py

Salida NUEVA: benchmarks/robust_lambda/rollouts_sweep.csv (reanudable).
"""
import csv
import glob
import os
import sys
import time

sys.path.insert(0, ".")

# la evaluacion NO debe ver lambda: el objetivo entra por el
# entrenamiento, y aqui se registran los dos extremos de cada rollout
os.environ.pop("DEEPLJSP_V2_LAMBDA", None)

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
SALIDA = "benchmarks/robust_lambda/rollouts_sweep.csv"
ULTIMA = "INT__TAI20_15_04.F.15_01_INTERVAL_model.pt"
BRAZOS = [("lam0p5", "v2-robust-lam0p5"), ("lam2", "v2-robust-lam2"),
          ("lam4", "v2-robust-lam4")]


def checkpoints():
    out = []
    for arm, tag in BRAZOS:
        for s in (2, 3, 4):
            dirs = glob.glob(f"outputs/bench_{tag}__*_seed{s}")
            rutas = [os.path.join(d, ULTIMA) for d in dirs
                     if os.path.exists(os.path.join(d, ULTIMA))]
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
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    hechos = {}
    if os.path.exists(SALIDA):
        with open(SALIDA, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                k = (r["arm"], r["seed"], r["instance"])
                hechos[k] = hechos.get(k, 0) + 1

    nuevo = not os.path.exists(SALIDA) or os.path.getsize(SALIDA) == 0
    f = open(SALIDA, "a", encoding="utf-8", newline="")
    w = csv.writer(f)
    if nuevo:
        w.writerow(["arm", "seed", "instance", "lb", "sample_idx",
                    "lower", "upper"])

    for brazo, s, ruta in checkpoints():
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
    print("hecho")


if __name__ == "__main__":
    main()
