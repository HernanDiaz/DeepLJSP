# -*- coding: utf-8 -*-
"""Robustez ejecucional eps-barra de la politica DRL frente a los baselines.

Para cada instancia se muestrean K=1000 realizaciones de las duraciones
(numeros aleatorios comunes: las MISMAS realizaciones para todos los
metodos) y se mide eps-barra = media de |C_ex - E[Cmax]| / E[Cmax], mas
la cobertura del intervalo predicho, reutilizando la maquinaria de
scripts/robustness_epsilon.py.

Metodos: politica greedy y best-of-64 (cada checkpoint final), y los
baselines deterministas MOR, EST y G&T-MWKR. Salida NUEVA:
benchmarks/eval_eps_policy.csv (reanudable por filas).

    python scripts/eval_eps_policy.py
"""
import csv
import importlib.util
import json
import os
import sys

import numpy as np

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import torch                                                   # noqa: E402

from jobshop_rl.agents_v2 import AgentV2                       # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.heuristics.gp_rule import GPRuleHeuristic      # noqa: E402
from jobshop_rl.heuristics.strategies import (                 # noqa: E402
    ESTHeuristic, GTHeuristic, MORHeuristic)

spec = importlib.util.spec_from_file_location(
    "reps", "scripts/robustness_epsilon.py")
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)

INSTANCIAS = [
    # desarrollo (20x15)
    "int__tai20_15_05", "int__tai20_15_06", "int__tai20_15_07",
    "int__tai20_15_08", "int__tai20_15_09", "int__tai20_15_10",
    # zero-shot (las de tab:crosssize)
    "int__tai15_15_01", "int__tai15_15_02", "int__tai15_15_05",
    "int__tai20_20_01", "int__tai20_20_05", "int__tai30_15_01",
    "int__tai30_20_01", "int__tai50_15_01", "int__tai50_20_01",
]
CKPTS = [f"models/v2_final_deepsets_1000ep_seed{s}.pt" for s in (2, 3, 4)]
K = 1000
N_BO = 64
SALIDA = "benchmarks/eval_eps_policy.csv"


def secuencia_politica(env, agent, muestrear, semilla_torch):
    """Orden de proceso (jobs 1-based) de un rollout de la politica."""
    torch.manual_seed(semilla_torch)
    state = env.reset()
    seq, done = [], False
    while not done and state["eligible_ops"]:
        salida = agent.select_action(state, training=muestrear)
        a = salida[0] if isinstance(salida, tuple) else salida
        a = min(int(a), len(state["eligible_ops"]) - 1)
        seq.append(state["eligible_ops"][a] + 1)
        state, _, done, _ = env.step(a)
    return seq


def mejor_de_n(env, agent, lo, up, mseq, n):
    """Greedy + (n-1) muestras; se queda la mejor por ranking lexicografico
    (upper primero) del intervalo predicho componentwise."""
    mejor, mejor_clave = None, None
    for i in range(n):
        seq = secuencia_politica(env, agent, muestrear=(i > 0),
                                 semilla_torch=1000 + i)
        clo, cup = R.predicted_interval(seq, lo, up, mseq)
        clave = (cup, clo)
        if mejor_clave is None or clave < mejor_clave:
            mejor, mejor_clave = seq, clave
    return mejor


def main():
    hechas = set()
    if os.path.exists(SALIDA):
        with open(SALIDA, encoding="utf-8") as f:
            hechas = {(r["instance"], r["method"]) for r in csv.DictReader(f)}
    nuevo = not os.path.exists(SALIDA)
    out = open(SALIDA, "a", encoding="utf-8", newline="")
    w = csv.writer(out)
    if nuevo:
        w.writerow(["instance", "method", "eps", "e_mid", "coverage",
                    "c_lo", "c_up"])

    for pid in INSTANCIAS:
        lo, up, mseq = R.instance_arrays(pid)
        # numeros aleatorios comunes: mismas realizaciones para todos
        rng = np.random.default_rng(abs(hash(pid)) % (2 ** 31))
        dur = R.sample_durations(lo, up, K, rng)

        metodos = {}
        env = EnvironmentFactory.create_from_problem_id(pid, "adaptive",
                                                        seed=1)
        # la regla destacada del companion, evaluada con LOS MISMOS
        # numeros aleatorios que todo lo demas (el CSV del GP uso otras
        # semillas de escenario, asi que no estaria pareado)
        _gp = json.load(open("benchmarks/reevo_fixedfit/gp_tuned_seed1.json",
                             encoding="utf-8"))["tree"]
        for nombre, h in [("MOR", MORHeuristic()), ("EST", ESTHeuristic()),
                          ("GT-MWKR", GTHeuristic(tiebreak="mwkr")),
                          ("GP", GPRuleHeuristic(_gp))]:
            metodos[nombre] = R.heuristic_sequence(env, h)
        for ck in CKPTS:
            etiqueta = os.path.basename(ck).replace(
                "v2_final_deepsets_1000ep_", "").replace(".pt", "")
            agent = AgentV2(env, seed=1, attention_layers=0)
            agent.load_checkpoint(ck)
            metodos[f"policy-greedy-{etiqueta}"] = secuencia_politica(
                env, agent, muestrear=False, semilla_torch=0)
            metodos[f"policy-bo{N_BO}-{etiqueta}"] = mejor_de_n(
                env, agent, lo, up, mseq, N_BO)

        for nombre, seq in metodos.items():
            if (pid, nombre) in hechas:
                continue
            clo, cup = R.predicted_interval(seq, lo, up, mseq)
            e_mid = (clo + cup) / 2.0
            cmax = R.decode_mc(seq, dur, mseq, K)
            eps = float(np.mean(np.abs(cmax - e_mid) / e_mid))
            cov = float(np.mean((cmax >= clo) & (cmax <= cup)))
            w.writerow([pid, nombre, f"{eps:.6f}", f"{e_mid:.1f}",
                        f"{cov:.4f}", f"{clo:.1f}", f"{cup:.1f}"])
            out.flush()
            print(f"{pid} {nombre}: eps={eps * 100:.2f}% cov={cov:.2f}",
                  flush=True)
    out.close()


if __name__ == "__main__":
    main()
