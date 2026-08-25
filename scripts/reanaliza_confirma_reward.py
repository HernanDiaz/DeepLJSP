# -*- coding: utf-8 -*-
"""Reanaliza la confirmacion del ganador de irace bajo la convencion 5.1.

La revision del 2026-08-25 (R2-3) senalo que el p=0.21 de la
confirmacion corre el Wilcoxon sobre los 18 pares instancia x semilla
(la regla de adopcion pre-registrada en tuning/PLAN_reward.md), no
sobre las 6 medias por instancia que usa el resto del paper. Los seis
checkpoints de la confirmacion estan en models/ y la evaluacion es
determinista (best-of-64, semilla de muestreo fija), asi que aqui se
reevaluan ambos brazos con el protocolo identico de
confirma_ganador_reward.py y se calculan los dos estadisticos: el
pre-registrado (18 pares, sanity check contra el log) y el conforme a
la convencion (6 medias por instancia, Wilcoxon exacto).

    python scripts/reanaliza_confirma_reward.py

Salida NUEVA: benchmarks/confirm_reward/reanalisis.json
No toca ningun checkpoint ni registro existente.
"""
import json
import os
import sys

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
os.environ.pop("DEEPLJSP_REWARD_WEIGHTS", None)
os.environ.pop("DEEPLJSP_V2_LAMBDA", None)
sys.path.insert(0, ".")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import torch  # noqa: E402
torch.set_num_threads(2)

from jobshop_rl.agents_v2 import AgentV2                       # noqa: E402
from jobshop_rl.agents_v2.batched_eval import evaluate_policy_batched  # noqa: E402
from jobshop_rl.agents_v2.state_encoder import StateEncoder    # noqa: E402
from jobshop_rl.data import PROBLEM_REGISTRY                   # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.models.interval import Interval                # noqa: E402

EVAL_IDS = [f"int__tai20_15_{i:02d}" for i in range(5, 11)]  # TA15-20
SEEDS = [2, 3, 4]
N_EVAL = 64
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
BRAZOS = {"ganadora": "models/v2_rewardwin_1000ep_seed{s}.pt",
          "default": "models/v2_final_deepsets_1000ep_seed{s}.pt"}


def eval_dev(ckpt):
    env = EnvironmentFactory.create_from_problem(
        PROBLEM_REGISTRY[EVAL_IDS[0]](), "adaptive", seed=1)
    agent = AgentV2(env, seed=1)
    agent.load_checkpoint(ckpt)
    out = {}
    for pid in EVAL_IDS:
        env = EnvironmentFactory.create_from_problem(
            PROBLEM_REGISTRY[pid](), "adaptive", seed=1)
        agent.env = env
        agent.encoder = StateEncoder(env)
        _, sched, _, _ = evaluate_policy_batched(agent, N_EVAL,
                                                 device=DEVICE, seed=1)
        max_lo = max_up = None
        for t in sched:
            end = t.get("end")
            lo = float(end.lower) if isinstance(end, Interval) else float(end)
            up = float(end.upper) if isinstance(end, Interval) else float(end)
            max_lo = lo if max_lo is None else max(max_lo, lo)
            max_up = up if max_up is None else max(max_up, up)
        lb = lb_for_problem_name(pid)
        out[pid] = ((max_lo + max_up) / 2 - lb) / lb * 100
    return out


def main():
    from scipy import stats
    res = {b: {p: [] for p in EVAL_IDS} for b in BRAZOS}
    for brazo, patron in BRAZOS.items():
        for s in SEEDS:
            ckpt = patron.format(s=s)
            r = eval_dev(ckpt)
            for p, v in r.items():
                res[brazo][p].append(v)
            print(f"[{brazo} seed {s}] "
                  + " ".join(f"{r[p]:.2f}" for p in EVAL_IDS)
                  + f"  media={sum(r.values()) / 6:.4f}", flush=True)

    gan, defr = res["ganadora"], res["default"]
    pares18 = [gan[p][i] - defr[p][i] for p in EVAL_IDS
               for i in range(len(SEEDS))]
    mg = sum(v for p in EVAL_IDS for v in gan[p]) / 18
    md = sum(v for p in EVAL_IDS for v in defr[p]) / 18
    p18 = float(stats.wilcoxon(pares18)[1])
    print(f"\n18 pares (regla pre-registrada): medias {mg:.2f} vs "
          f"{md:.2f}, Wilcoxon p={p18:.4f}")

    medias_g = [sum(gan[p]) / len(SEEDS) for p in EVAL_IDS]
    medias_d = [sum(defr[p]) / len(SEEDS) for p in EVAL_IDS]
    pares6 = [g - d for g, d in zip(medias_g, medias_d)]
    p6 = float(stats.wilcoxon(pares6, method="exact")[1])
    print("6 medias por instancia (convencion 5.1): "
          + " ".join(f"{d:+.3f}" for d in pares6)
          + f", Wilcoxon exacto p={p6:.4f}")

    os.makedirs("benchmarks/confirm_reward", exist_ok=True)
    with open("benchmarks/confirm_reward/reanalisis.json", "w",
              encoding="utf-8") as f:
        json.dump({"instancias": EVAL_IDS, "semillas": SEEDS,
                   "n_eval": N_EVAL,
                   "re": {b: {p: [round(v, 4) for v in res[b][p]]
                              for p in EVAL_IDS} for b in BRAZOS},
                   "media_ganadora_18": round(mg, 4),
                   "media_default_18": round(md, 4),
                   "p_18pares_preregistrado": round(p18, 4),
                   "d_por_instancia": [round(d, 4) for d in pares6],
                   "p_6medias_exacto": round(p6, 4)}, f, indent=1)
    print("guardado: benchmarks/confirm_reward/reanalisis.json")


if __name__ == "__main__":
    main()
