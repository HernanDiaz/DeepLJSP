# -*- coding: utf-8 -*-
"""Curva de presupuesto de inferencia: RE frente al numero de muestras.

El barrido best-of-1024 solo guardo el mejor de cada tirada, asi que la
pregunta "que compra cada muestra adicional" solo tiene dos puntos
(greedy y 1024). Aqui se guarda el makespan de CADA rollout, de modo que
el mejor-de-N para cualquier N se reconstruye despues sin volver a
calcular, incluida la mezcla de los tres checkpoints del protocolo.

Formato largo: una fila por rollout (checkpoint, instancia, indice,
makespan componentwise). Reanudable: se salta cada par ya completo.

    python scripts/eval_budget_curve.py
"""
import csv
import os
import sys
import time

sys.path.insert(0, ".")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.agents_v2 import AgentV2                       # noqa: E402
from jobshop_rl.data import PROBLEM_REGISTRY                   # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.models.interval import Interval, final_makespan  # noqa: E402

CKPTS = [f"models/v2_final_deepsets_1000ep_seed{s}.pt" for s in (2, 3, 4)]
N_MUESTRAS = 342          # 3 x 342 ~ 1024, el protocolo del paper
SALIDA = "benchmarks/eval_budget_curve.csv"


def mid_componentwise(env):
    """E[Cmax] del estado final: [max lowers, max uppers], Eq. 2."""
    m = final_makespan(env.job_completion_time)
    if isinstance(m, Interval):
        return (float(m.lower) + float(m.upper)) / 2.0
    return float(m)


def rollouts(ckpt, instancia, n):
    """Devuelve los n makespan: el 0 es greedy, el resto muestreados."""
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
        out.append(mid_componentwise(env))
    return out


def main():
    hechos = {}
    if os.path.exists(SALIDA):
        with open(SALIDA, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                hechos[(r["checkpoint"], r["instance"])] = \
                    hechos.get((r["checkpoint"], r["instance"]), 0) + 1

    universo = sorted(k for k in PROBLEM_REGISTRY
                      if k.startswith("int__tai")
                      and not k.startswith("int__tai100")
                      and lb_for_problem_name(k) is not None)
    assert len(universo) == 70, f"esperaba 70, hay {len(universo)}"

    nuevo = not os.path.exists(SALIDA) or os.path.getsize(SALIDA) == 0
    f = open(SALIDA, "a", encoding="utf-8", newline="")
    w = csv.writer(f)
    if nuevo:
        w.writerow(["checkpoint", "instance", "lb", "sample_idx", "mid_comp"])

    for instancia in universo:
        lb = lb_for_problem_name(instancia)
        for ckpt in CKPTS:
            clave = (os.path.basename(ckpt), instancia)
            if hechos.get(clave, 0) >= N_MUESTRAS:
                continue
            t0 = time.time()
            for i, mid in enumerate(rollouts(ckpt, instancia, N_MUESTRAS)):
                w.writerow([clave[0], instancia, lb, i, f"{mid:.1f}"])
            f.flush()
            print(f"  {clave[0]} {instancia}: {N_MUESTRAS} rollouts en "
                  f"{time.time() - t0:.0f}s", flush=True)
    f.close()


if __name__ == "__main__":
    main()
