# -*- coding: utf-8 -*-
"""Importancia por permutacion de las 16 features de operacion.

El analogo (humilde) de la anatomia de la regla del paper del GP: la red
no se puede leer, pero si se puede medir que mira. Para cada feature se
permuta su columna entre las operaciones elegibles en CADA decision de
un rollout greedy y se mide la degradacion del RE frente al rollout
intacto; una feature cuya permutacion no cuesta nada no esta informando
la decision.

Salida NUEVA: benchmarks/feature_importance.csv.

    python scripts/feature_importance.py
"""
import csv
import os
import sys

import numpy as np

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

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
SALIDA = "benchmarks/feature_importance.csv"

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
    se.StateEncoder.encode = _encode_permutado

    # base: sin permutar
    _estado["col"] = None
    base = {(pid, ck): rollout_greedy(pid, ck)
            for pid in INSTANCIAS for ck in CKPTS}
    re_base = float(np.mean(list(base.values())))
    print(f"RE base (greedy, sin permutar): {re_base:.2f}%", flush=True)

    out = open(SALIDA, "w", encoding="utf-8", newline="")
    w = csv.writer(out)
    w.writerow(["feature_idx", "feature", "re_base", "re_permutado",
                "delta_puntos"])
    for col, nombre in enumerate(NOMBRES):
        _estado["col"] = col
        _estado["rng"] = np.random.default_rng(97 + col)
        _estado["llamadas"] = 0
        res = [rollout_greedy(pid, ck)
               for pid in INSTANCIAS for ck in CKPTS]
        if _estado["llamadas"] == 0:
            sys.exit("ABORTA: el parche del encoder no se esta ejecutando")
        re_perm = float(np.mean(res))
        w.writerow([col, nombre, f"{re_base:.4f}", f"{re_perm:.4f}",
                    f"{re_perm - re_base:.4f}"])
        out.flush()
        print(f"  {col:>2} {nombre:<18} RE={re_perm:.2f}%  "
              f"delta={re_perm - re_base:+.2f}", flush=True)
    out.close()


if __name__ == "__main__":
    main()
