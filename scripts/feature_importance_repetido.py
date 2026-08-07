# -*- coding: utf-8 -*-
"""Importancia por permutacion con VARIAS extracciones por feature.

feature_importance.py mide una sola permutacion por rollout, asi que
sus magnitudes llevan el ruido de esa unica extraccion: el orden de
las features es estable entre semillas, pero los numeros no. Aqui se
repite R veces la permutacion de cada columna, con una semilla distinta
cada vez, y se reporta la media de las R degradaciones y su desviacion
tipica, que es lo que el paper deberia citar.

El rollout base (sin permutar) es determinista y se calcula una vez.

Salida NUEVA: benchmarks/feature_importance_rep.csv (una fila por
feature y repeticion, mas el resumen por feature en el log). No toca
benchmarks/feature_importance.csv ni ningun checkpoint.

    python scripts/feature_importance_repetido.py        # R=5
    DEEPLJSP_FI_REPS=10 python scripts/feature_importance_repetido.py
"""
import csv
import os
import sys

import numpy as np

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import torch                                                  # noqa: E402
torch.set_num_threads(2)

from jobshop_rl.agents_v2 import AgentV2                       # noqa: E402
import jobshop_rl.agents_v2.state_encoder as se                # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.models.interval import Interval, final_makespan  # noqa: E402

NOMBRES = [
    "dur_lo", "dur_up", "dur_width_rel", "est_lo", "est_up",
    "est_width_rel", "rem_lo", "rem_up", "pos_restante", "pos_hecha",
    "carga_maquina", "hueco_potencial", "congestion", "holgura",
    "makespan_maquina", "makespan_job",
]
INSTANCIAS = [
    "int__tai20_15_05", "int__tai20_15_06", "int__tai20_15_07",
    "int__tai20_15_08", "int__tai20_15_09", "int__tai20_15_10",
]
CKPTS = [f"models/v2_final_deepsets_1000ep_seed{s}.pt" for s in (2, 3, 4)]
SALIDA = "benchmarks/feature_importance_rep.csv"
REPS = int(os.environ.get("DEEPLJSP_FI_REPS", "5"))

_encode_original = se.StateEncoder.encode
_estado = {"col": None, "rng": None, "llamadas": 0}


def _encode_permutado(self, state):
    op, gl = _encode_original(self, state)
    if _estado["col"] is not None and op.shape[0] > 1:
        _estado["llamadas"] += 1
        op = op.copy()
        op[:, _estado["col"]] = _estado["rng"].permutation(
            op[:, _estado["col"]])
    return op, gl


def rollout_greedy(pid, ckpt):
    env = EnvironmentFactory.create_from_problem_id(pid, "adaptive", seed=1)
    agent = AgentV2(env, seed=1, attention_layers=0)
    agent.load_checkpoint(ckpt)
    state = env.reset()
    done = False
    while not done and state["eligible_ops"]:
        salida = agent.select_action(state, training=False)
        a = salida[0] if isinstance(salida, tuple) else salida
        a = min(int(a), len(state["eligible_ops"]) - 1)
        state, _, done, _ = env.step(a)
    m = final_makespan(env.job_completion_time)
    mid = (float(m.lower) + float(m.upper)) / 2 if isinstance(m, Interval) \
        else float(m)
    lb = lb_for_problem_name(pid)
    return (mid - lb) / lb * 100


def main():
    if os.path.exists(SALIDA):
        sys.exit(f"ABORTA: {SALIDA} ya existe; no se sobrescribe nada")
    se.StateEncoder.encode = _encode_permutado

    _estado["col"] = None
    base = [rollout_greedy(pid, ck) for pid in INSTANCIAS for ck in CKPTS]
    re_base = float(np.mean(base))
    print(f"RE base (greedy, sin permutar): {re_base:.2f}%  "
          f"sobre {len(base)} rollouts", flush=True)
    print(f"{REPS} permutaciones por feature\n", flush=True)

    out = open(SALIDA, "w", encoding="utf-8", newline="")
    w = csv.writer(out)
    w.writerow(["feature_idx", "feature", "repeticion", "semilla",
                "re_base", "re_permutado", "delta_puntos"])
    resumen = {}
    for col, nombre in enumerate(NOMBRES):
        deltas = []
        for r in range(REPS):
            semilla = 9700 + col * 100 + r
            _estado["col"] = col
            _estado["rng"] = np.random.default_rng(semilla)
            _estado["llamadas"] = 0
            res = [rollout_greedy(pid, ck)
                   for pid in INSTANCIAS for ck in CKPTS]
            if _estado["llamadas"] == 0:
                sys.exit("ABORTA: el parche del encoder no se ejecuta")
            re_perm = float(np.mean(res))
            deltas.append(re_perm - re_base)
            w.writerow([col, nombre, r, semilla, f"{re_base:.4f}",
                        f"{re_perm:.4f}", f"{re_perm - re_base:.4f}"])
            out.flush()
        m, s = float(np.mean(deltas)), float(np.std(deltas, ddof=1))
        resumen[nombre] = (m, s)
        print(f"  {col:>2} {nombre:<18} delta={m:+7.2f}  sd={s:5.2f}  "
              f"[{min(deltas):+.2f}, {max(deltas):+.2f}]", flush=True)
    out.close()

    print("\n=== orden por importancia media ===", flush=True)
    for i, (nom, (m, s)) in enumerate(
            sorted(resumen.items(), key=lambda kv: -kv[1][0]), 1):
        print(f"  {i:>2}. {nom:<18} {m:+7.2f} +- {s:.2f}", flush=True)


if __name__ == "__main__":
    main()
