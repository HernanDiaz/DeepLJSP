# -*- coding: utf-8 -*-
"""Robustez ejecucional sobre las 70 instancias, no sobre quince.

7.6 sostiene su afirmacion -- la politica es de las mas fieles del
conjunto constructivo -- sobre quince instancias, mientras 6.4 usa las
setenta. Un revisor lo notara. Aqui se amplia a las 70 lo que 7.6
afirma de fondo: politica frente a reglas.

El brazo robusto NO entra: su contraste vive en eval_eps_all.csv sobre
las quince, y anadirlo aqui doblaria el coste (seis brazos de politica
en vez de tres) para refinar algo que ya esta medido. Las 50x20 son las
caras: ~4 s por rollout, 192 rollouts por instancia.

Semilla de las realizaciones por crc32 del identificador, estable entre
procesos, como en eval_eps_all.py.

    python scripts/eval_eps_70.py

Salida NUEVA: benchmarks/eval_eps_70.csv (reanudable por filas).
"""
import csv
import importlib.util
import json
import os
import sys
import time
import zlib

import numpy as np

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import torch                                                   # noqa: E402

from jobshop_rl.agents_v2 import AgentV2                       # noqa: E402
from jobshop_rl.data import PROBLEM_REGISTRY                   # noqa: E402
from jobshop_rl.data.literature_bounds import (                # noqa: E402
    lb_for_problem_name)
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.heuristics.gp_rule import GPRuleHeuristic      # noqa: E402
from jobshop_rl.heuristics.strategies import (                 # noqa: E402
    ESTHeuristic, GTHeuristic, MORHeuristic)

spec = importlib.util.spec_from_file_location(
    "reps", "scripts/robustness_epsilon.py")
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)

CKPTS = [f"models/v2_final_deepsets_1000ep_seed{s}.pt" for s in (2, 3, 4)]
K = 1000
N_BO = 64
SALIDA = "benchmarks/eval_eps_70.csv"


def semilla(pid):
    return zlib.crc32(pid.encode("utf-8")) % (2 ** 31)


def secuencia(env, agent, muestrear, semilla_torch):
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
    mejor, clave_mejor = None, None
    for i in range(n):
        seq = secuencia(env, agent, muestrear=(i > 0), semilla_torch=1000 + i)
        clo, cup = R.predicted_interval(seq, lo, up, mseq)
        clave = (cup, clo)
        if clave_mejor is None or clave < clave_mejor:
            mejor, clave_mejor = seq, clave
    return mejor


def main():
    universo = sorted(k for k in PROBLEM_REGISTRY
                      if k.startswith("int__tai")
                      and not k.startswith("int__tai100")
                      and lb_for_problem_name(k) is not None)
    assert len(universo) == 70, f"esperaba 70, hay {len(universo)}"

    hechas = set()
    if os.path.exists(SALIDA):
        with open(SALIDA, encoding="utf-8") as f:
            hechas = {(r["instance"], r["method"]) for r in csv.DictReader(f)}
    nuevo = not os.path.exists(SALIDA) or os.path.getsize(SALIDA) == 0
    out = open(SALIDA, "a", encoding="utf-8", newline="")
    w = csv.writer(out)
    if nuevo:
        w.writerow(["instance", "method", "eps", "e_mid", "coverage",
                    "c_lo", "c_up", "width_rel"])

    _gp = json.load(open("benchmarks/reevo_fixedfit/gp_tuned_seed1.json",
                         encoding="utf-8"))["tree"]
    for pid in universo:
        # si la instancia ya esta entera, ni se carga
        if sum(1 for i, _ in hechas if i == pid) >= 10:
            continue
        t0 = time.time()
        lo, up, mseq = R.instance_arrays(pid)
        dur = R.sample_durations(lo, up, K, np.random.default_rng(
            semilla(pid)))
        env = EnvironmentFactory.create_from_problem_id(pid, "adaptive",
                                                        seed=1)
        metodos = {}
        for nombre, h in [("MOR", MORHeuristic()), ("EST", ESTHeuristic()),
                          ("GT-MWKR", GTHeuristic(tiebreak="mwkr")),
                          ("GP", GPRuleHeuristic(_gp))]:
            metodos[nombre] = R.heuristic_sequence(env, h)
        for ck in CKPTS:
            et = os.path.basename(ck).replace(
                "v2_final_deepsets_1000ep_", "").replace(".pt", "")
            agent = AgentV2(env, seed=1, attention_layers=0)
            agent.load_checkpoint(ck)
            metodos[f"policy-greedy-{et}"] = secuencia(
                env, agent, muestrear=False, semilla_torch=0)
            metodos[f"policy-bo{N_BO}-{et}"] = mejor_de_n(
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
                        f"{cov:.4f}", f"{clo:.1f}", f"{cup:.1f}",
                        f"{(cup - clo) / e_mid * 100:.4f}"])
            out.flush()
        print(f"{pid}: {len(metodos)} metodos en {time.time() - t0:.0f}s",
              flush=True)
    out.close()
    print("hecho")


if __name__ == "__main__":
    main()
