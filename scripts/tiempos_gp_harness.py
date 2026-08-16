# -*- coding: utf-8 -*-
"""Cronometra la regla GP destacada en el harness unificado, por clase.

Mismo diseno que benchmarks/tiempos_inferencia.csv, que midio la
politica sobre una instancia representativa por clase: la pasada
determinista suelta y la tanda best-of-64 completa (una greedy y 63
epsilon-greedy con eps=0.1, el despacho de su estudio), esta ultima
amortizada entre 64. Asi las dos familias quedan medidas en la misma
maquina, el mismo harness y las mismas instancias.

Salida NUEVA: benchmarks/tiempos_gp_harness/tiempos_gp.csv

    python scripts/tiempos_gp_harness.py
"""
import csv
import json
import os
import random
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data import PROBLEM_REGISTRY                       # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory      # noqa: E402
from jobshop_rl.heuristics.gp_rule import GPRuleHeuristic          # noqa: E402
from jobshop_rl.models.interval import Interval, final_makespan    # noqa: E402


def crea_env(pid):
    return EnvironmentFactory.create_from_problem(
        PROBLEM_REGISTRY[pid](), "basic", seed=0)

# las mismas instancias que midieron a la politica
INSTANCIAS = {"15x15": "int__tai15_15_01", "20x15": "int__tai20_15_05",
              "30x20": "int__tai30_20_01", "50x20": "int__tai50_20_01"}
REGLA = "benchmarks/reevo_fixedfit/gp_tuned_seed1.json"
SALIDA = "benchmarks/tiempos_gp_harness/tiempos_gp.csv"
REPES_GREEDY = 5
EPS = 0.1


def rollout(env, h, rng=None, eps=0.0):
    st = env.reset()
    done = False
    while not done and st["eligible_ops"]:
        if rng is not None and rng.random() < eps:
            a = rng.randrange(len(st["eligible_ops"]))
        else:
            f = env.get_features(st)
            a = min(h.select_action(st["eligible_ops"], f),
                    len(st["eligible_ops"]) - 1)
        st, _, done, _ = env.step(a)
    m = final_makespan(env.job_completion_time)
    if isinstance(m, Interval):
        return float(m.lower), float(m.upper)
    return float(m), float(m)


def main():
    gp = GPRuleHeuristic(json.load(open(REGLA, encoding="utf-8"))["tree"])
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    filas = []
    for clase, pid in INSTANCIAS.items():
        # calentamiento: primera construccion fuera de reloj
        env = crea_env(pid)
        rollout(env, gp)

        # pasada determinista suelta, media de varias repeticiones
        t0 = time.perf_counter()
        for _ in range(REPES_GREEDY):
            env = crea_env(pid)
            rollout(env, gp)
        det_s = (time.perf_counter() - t0) / REPES_GREEDY

        # tanda best-of-64: una determinista y 63 epsilon-greedy, con la
        # seleccion lexicografica incluida en el reloj, como en la tanda
        # de la politica
        rng = random.Random(1)
        t0 = time.perf_counter()
        mejor = None
        for k in range(64):
            env = crea_env(pid)
            lo, up = rollout(env, gp, rng=(None if k == 0 else rng), eps=EPS)
            if mejor is None or (up, lo) < mejor:
                mejor = (up, lo)
        bo64_s = time.perf_counter() - t0

        filas.append({"clase": clase, "instancia": pid,
                      "det_s": round(det_s, 3),
                      "bo64_s": round(bo64_s, 1),
                      "por_muestra_s": round(bo64_s / 64, 3)})
        print(f"  {clase}: det {det_s:.2f} s   bo64 {bo64_s:.1f} s "
              f"({bo64_s / 64:.2f} s/muestra)", flush=True)

    with open(SALIDA, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
