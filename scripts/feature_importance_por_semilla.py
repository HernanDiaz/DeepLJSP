# -*- coding: utf-8 -*-
"""La misma importancia por permutacion, pero SIN promediar las semillas.

feature_importance.py agrega los 18 rollouts (6 instancias x 3 semillas)
en un solo delta por feature, asi que no permite saber si las tres redes
miran lo mismo o si el orden sale de promediar tres cosas distintas.
Aqui se guarda un delta por (feature, semilla), con las seis instancias
promediadas dentro de cada semilla.

    python scripts/feature_importance_por_semilla.py

Salida NUEVA: benchmarks/feature_importance_por_semilla.csv (no toca el
fichero agregado).
"""
import csv
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
INSTANCIAS = [f"int__tai20_15_{k:02d}" for k in range(5, 11)]
SEMILLAS = (2, 3, 4)
SALIDA = "benchmarks/feature_importance_por_semilla.csv"

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
        state, _, done, _ = env.step(
            min(int(a), len(state["eligible_ops"]) - 1))
    m = final_makespan(env.job_completion_time)
    mid = (float(m.lower) + float(m.upper)) / 2 if isinstance(m, Interval) \
        else float(m)
    lb = lb_for_problem_name(pid)
    return (mid - lb) / lb * 100


def main():
    se.StateEncoder.encode = _encode_permutado
    ck = {s: f"models/v2_final_deepsets_1000ep_seed{s}.pt" for s in SEMILLAS}

    _estado["col"] = None
    base = {s: float(np.mean([rollout_greedy(p, ck[s]) for p in INSTANCIAS]))
            for s in SEMILLAS}
    for s in SEMILLAS:
        print(f"base semilla {s}: {base[s]:.2f}%", flush=True)

    f = open(SALIDA, "w", encoding="utf-8", newline="")
    w = csv.writer(f)
    w.writerow(["feature_idx", "feature", "semilla", "re_base",
                "re_permutado", "delta_puntos"])
    for col, nombre in enumerate(NOMBRES):
        deltas = []
        for s in SEMILLAS:
            _estado["col"] = col
            _estado["rng"] = np.random.default_rng(97 + col)
            _estado["llamadas"] = 0
            re_perm = float(np.mean([rollout_greedy(p, ck[s])
                                     for p in INSTANCIAS]))
            if _estado["llamadas"] == 0:
                sys.exit("ABORTA: el parche del encoder no se ejecuta")
            d = re_perm - base[s]
            deltas.append(d)
            w.writerow([col, nombre, s, f"{base[s]:.4f}", f"{re_perm:.4f}",
                        f"{d:.4f}"])
        f.flush()
        print(f"  {col:>2} {nombre:<18} "
              + "  ".join(f"s{s}={d:+.1f}" for s, d in zip(SEMILLAS, deltas)),
              flush=True)
    f.close()
    print("hecho")


if __name__ == "__main__":
    main()
