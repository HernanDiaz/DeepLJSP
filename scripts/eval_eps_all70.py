# -*- coding: utf-8 -*-
"""Robustez ejecucional de 7.5 sobre las 70 instancias del benchmark.

La seccion 7.5 sostiene sus contrastes sobre quince instancias fijadas
a priori; esto repite la medicion completa sobre las setenta, con el
mismo protocolo y el MISMO conjunto de metodos que la Figura 9:

  MOR, EST, GT-MWKR, GP (una pasada), GP best-of-64 (eps-greedy 0.1),
  politica greedy y best-of-64 (semillas 2-4), y el brazo robusto
  lambda=1 greedy y best-of-64 (semillas 2-4).

Realizaciones con semilla crc32 del identificador de instancia, como
eval_eps_all.csv: en las quince compartidas los numeros reproducen
exactamente. El muestreo eps-greedy del GP usa semilla(pid)+7, la
misma que eval_eps_gp_bo64.csv, por la misma razon.

Salida NUEVA: benchmarks/eval_eps_all70.csv (reanudable por filas).
No toca ningun CSV anterior.

    python scripts/eval_eps_all70.py
"""
import csv
import glob
import importlib.util
import json
import os
import sys
import time
import zlib

import numpy as np

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import torch                                                   # noqa: E402
torch.set_num_threads(2)

from jobshop_rl.agents_v2 import AgentV2                       # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.heuristics.gp_rule import (                    # noqa: E402
    GPRuleHeuristic, eval_tree, terminal_arrays)
from jobshop_rl.heuristics.strategies import (                 # noqa: E402
    ESTHeuristic, GTHeuristic, MORHeuristic)

spec = importlib.util.spec_from_file_location(
    "reps", "scripts/robustness_epsilon.py")
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)

INSTANCIAS = [f"int__tai{n}_{m}_{i:02d}"
              for n, m in [(15, 15), (20, 15), (20, 20), (30, 15),
                           (30, 20), (50, 15), (50, 20)]
              for i in range(1, 11)]
CKPTS = [f"models/v2_final_deepsets_1000ep_seed{s}.pt" for s in (2, 3, 4)]
LAM1 = ("outputs/bench_v2-robust-lam1__*_seed{s}/"
        "INT__TAI20_15_04.F.15_01_INTERVAL_model.pt")
K = 1000
N_BO = 64
EPS_GP = 0.1
SALIDA = "benchmarks/eval_eps_all70.csv"


def semilla(pid):
    return zlib.crc32(pid.encode("utf-8")) % (2 ** 31)


def secuencia_politica(env, agent, muestrear, semilla_torch):
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


def mejor_de_n(env, agent, lo, up, mseq, n, robusto=False):
    mejor, mejor_clave = None, None
    for i in range(n):
        seq = secuencia_politica(env, agent, muestrear=(i > 0),
                                 semilla_torch=1000 + i)
        clo, cup = R.predicted_interval(seq, lo, up, mseq)
        clave = (2 * cup - clo,) if robusto else (cup, clo)
        if mejor_clave is None or clave < mejor_clave:
            mejor, mejor_clave = seq, clave
    return mejor


def secuencia_gp_eps(env, tree, rng):
    state = env.reset()
    seq, done = [], False
    while not done and state["eligible_ops"]:
        f = env.get_features(state)
        if len(f) and rng.random() < EPS_GP:
            idx = int(rng.integers(len(state["eligible_ops"])))
        else:
            pri = eval_tree(tree, terminal_arrays(f))
            idx = int(np.argmin(pri))
        idx = min(idx, len(state["eligible_ops"]) - 1)
        seq.append(env.eligible_ops[idx] + 1)
        state, _, done, _ = env.step(idx)
    return seq


def gp_mejor_de_n(env, tree, lo, up, mseq, rng):
    mejor, mejor_clave = None, None
    for i in range(N_BO):
        if i == 0:
            seq = R.heuristic_sequence(env, GPRuleHeuristic(tree))
        else:
            seq = secuencia_gp_eps(env, tree, rng)
        clo, cup = R.predicted_interval(seq, lo, up, mseq)
        clave = (cup, clo)
        if mejor_clave is None or clave < mejor_clave:
            mejor, mejor_clave = seq, clave
    return mejor


def checkpoints_lam1():
    out = []
    for s in (2, 3, 4):
        g = glob.glob(LAM1.format(s=s))
        if g:
            out.append((f"lam1-seed{s}", g[0]))
    return out


def main():
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

    lam = checkpoints_lam1()
    tree = json.load(open("benchmarks/reevo_fixedfit/gp_tuned_seed1.json",
                          encoding="utf-8"))["tree"]
    print(f"{len(lam)} checkpoints lambda=1; {len(INSTANCIAS)} instancias",
          flush=True)

    for pid in INSTANCIAS:
        t0 = time.time()
        lo, up, mseq = R.instance_arrays(pid)
        rng = np.random.default_rng(semilla(pid))
        dur = R.sample_durations(lo, up, K, rng)

        metodos = {}
        env = EnvironmentFactory.create_from_problem_id(pid, "adaptive",
                                                        seed=1)
        for nombre, h in [("MOR", MORHeuristic()), ("EST", ESTHeuristic()),
                          ("GT-MWKR", GTHeuristic(tiebreak="mwkr")),
                          ("GP", GPRuleHeuristic(tree))]:
            if (pid, nombre) not in hechas:
                metodos[nombre] = R.heuristic_sequence(env, h)
        if (pid, f"GP-bo{N_BO}") not in hechas:
            metodos[f"GP-bo{N_BO}"] = gp_mejor_de_n(
                env, tree, lo, up, mseq,
                np.random.default_rng(semilla(pid) + 7))
        for ck in CKPTS:
            et = os.path.basename(ck).replace(
                "v2_final_deepsets_1000ep_", "").replace(".pt", "")
            if ((pid, f"policy-greedy-{et}") in hechas
                    and (pid, f"policy-bo{N_BO}-{et}") in hechas):
                continue
            agent = AgentV2(env, seed=1, attention_layers=0)
            agent.load_checkpoint(ck)
            metodos[f"policy-greedy-{et}"] = secuencia_politica(
                env, agent, muestrear=False, semilla_torch=0)
            metodos[f"policy-bo{N_BO}-{et}"] = mejor_de_n(
                env, agent, lo, up, mseq, N_BO)
        for et, ck in lam:
            if ((pid, f"{et}-greedy") in hechas
                    and (pid, f"{et}-bo{N_BO}") in hechas):
                continue
            agent = AgentV2(env, seed=1, attention_layers=0)
            agent.load_checkpoint(ck)
            metodos[f"{et}-greedy"] = secuencia_politica(
                env, agent, muestrear=False, semilla_torch=0)
            metodos[f"{et}-bo{N_BO}"] = mejor_de_n(
                env, agent, lo, up, mseq, N_BO, robusto=True)

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
        print(f"{pid}: {len(metodos)} metodos en "
              f"{time.time() - t0:.0f} s", flush=True)
    out.close()
    print("hecho")


if __name__ == "__main__":
    main()
