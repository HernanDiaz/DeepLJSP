# -*- coding: utf-8 -*-
"""Robustez ejecucional del GP best-of-64: la fila que falta en fig:eps.

La Figura 9 muestra a la politica a dos presupuestos y a la regla GP
solo a una pasada, el unico sitio del paper sin paridad de presupuesto.
Aqui se mide la regla destacada con el dispatching epsilon-greedy de su
propio estudio (epsilon=0.1, el mismo protocolo que fair_gp_eps.csv):
64 rollouts por instancia (el determinista mas 63 muestreados), se
retiene el mejor bajo el criterio lexicografico de la Eq. (3), y ese
schedule pasa por las MISMAS 1000 realizaciones que eval_eps_all.csv
(semilla crc32 del identificador de instancia), de modo que la
comparacion con el resto de metodos queda pareada realizacion a
realizacion.

Salida NUEVA: benchmarks/eval_eps_gp_bo64.csv. No toca eval_eps_all.csv.

    python scripts/eval_eps_gp_bo64.py
"""
import csv
import importlib.util
import json
import os
import sys
import zlib

import numpy as np

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.heuristics.gp_rule import (                    # noqa: E402
    GPRuleHeuristic, eval_tree, terminal_arrays)

spec = importlib.util.spec_from_file_location(
    "reps", "scripts/robustness_epsilon.py")
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)

INSTANCIAS = [
    "int__tai20_15_05", "int__tai20_15_06", "int__tai20_15_07",
    "int__tai20_15_08", "int__tai20_15_09", "int__tai20_15_10",
    "int__tai15_15_01", "int__tai15_15_02", "int__tai15_15_05",
    "int__tai20_20_01", "int__tai20_20_05", "int__tai30_15_01",
    "int__tai30_20_01", "int__tai50_15_01", "int__tai50_20_01",
]
K = 1000
N_BO = 64
EPSILON = 0.1
SALIDA = "benchmarks/eval_eps_gp_bo64.csv"


def semilla(pid):
    return zlib.crc32(pid.encode("utf-8")) % (2 ** 31)


def secuencia_gp_eps(env, tree, rng):
    """Un rollout epsilon-greedy de la regla: con probabilidad epsilon
    elige uniforme entre las elegibles, si no el argmin del arbol."""
    state = env.reset()
    seq, done = [], False
    while not done and state["eligible_ops"]:
        f = env.get_features(state)
        if len(f) and rng.random() < EPSILON:
            idx = int(rng.integers(len(state["eligible_ops"])))
        else:
            pri = eval_tree(tree, terminal_arrays(f))
            idx = int(np.argmin(pri))
        idx = min(idx, len(state["eligible_ops"]) - 1)
        seq.append(env.eligible_ops[idx] + 1)
        state, _, done, _ = env.step(idx)
    return seq


def main():
    if os.path.exists(SALIDA):
        sys.exit(f"ABORTA: {SALIDA} ya existe; no se sobrescribe nada")
    tree = json.load(open("benchmarks/reevo_fixedfit/gp_tuned_seed1.json",
                          encoding="utf-8"))["tree"]
    out = open(SALIDA, "w", encoding="utf-8", newline="")
    w = csv.writer(out)
    w.writerow(["instance", "method", "eps", "e_mid", "coverage",
                "c_lo", "c_up", "width_rel"])
    for pid in INSTANCIAS:
        lo, up, mseq = R.instance_arrays(pid)
        env = EnvironmentFactory.create_from_problem_id(pid, "adaptive",
                                                        seed=1)
        # el muestreo del rollout tiene su propia semilla (funcion de la
        # instancia, como el protocolo de la politica); las realizaciones
        # de la ejecucion usan la MISMA semilla que eval_eps_all.csv
        rng_roll = np.random.default_rng(semilla(pid) + 7)
        mejor, mejor_clave = None, None
        for i in range(N_BO):
            if i == 0:
                seq = R.heuristic_sequence(env, GPRuleHeuristic(tree))
            else:
                seq = secuencia_gp_eps(env, tree, rng_roll)
            clo, cup = R.predicted_interval(seq, lo, up, mseq)
            clave = (cup, clo)                  # Eq. (3), lexicografico
            if mejor_clave is None or clave < mejor_clave:
                mejor, mejor_clave = seq, clave
        rng_mc = np.random.default_rng(semilla(pid))
        dur = R.sample_durations(lo, up, K, rng_mc)
        clo, cup = R.predicted_interval(mejor, lo, up, mseq)
        e_mid = (clo + cup) / 2.0
        cmax = R.decode_mc(mejor, dur, mseq, K)
        eps = float(np.mean(np.abs(cmax - e_mid) / e_mid))
        cov = float(np.mean((cmax >= clo) & (cmax <= cup)))
        w.writerow([pid, f"GP-bo{N_BO}", f"{eps:.6f}", f"{e_mid:.1f}",
                    f"{cov:.4f}", f"{clo:.1f}", f"{cup:.1f}",
                    f"{(cup - clo) / e_mid * 100:.4f}"])
        out.flush()
        print(f"{pid}: eps={eps * 1000:.2f}e-3 "
              f"ancho={(cup - clo) / e_mid * 100:.2f}%", flush=True)
    out.close()
    print("hecho")


if __name__ == "__main__":
    main()
