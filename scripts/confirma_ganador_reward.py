# -*- coding: utf-8 -*-
"""Confirmación pre-registrada del ganador de la campaña de pesos.

Protocolo de tuning/PLAN_reward.md, calcado de confirm_elite22.py:

- Lee el ganador del log de irace (la primera fila del bloque final
  "Best configurations as commandlines").
- Entrena SOLO al ganador: TA11-14, 1000 eps/instancia, bloques con
  transferencia, 3 semillas (2, 3, 4), hiperparámetros default; los
  pesos entran por DEEPLJSP_REWARD_WEIGHTS (bypass del reajuste).
- Evalúa ganador y default con el MISMO evaluador batcheado
  (best-of-64, semilla de muestreo fija) sobre TA15-20 → pareado.
- Regla pre-registrada: adoptar solo si mejora significativa
  (Wilcoxon pareado sobre los 18 pares, p<0.05). "Muy cercano" =
  no significativo = los pesos a mano quedan validados.

    python scripts/confirma_ganador_reward.py

Salida NUEVA: tuning/confirm_reward.log (via run_confirm_reward.bat).
No toca ningún checkpoint existente.
"""

import os
import re
import sys

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
sys.path.insert(0, ".")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import torch
torch.set_num_threads(2)

TRAIN_IDS = ["int__tai20_15_01", "int__tai20_15_02",
             "int__tai20_15_03", "int__tai20_15_04"]
EVAL_IDS = [f"int__tai20_15_{i:02d}" for i in range(5, 11)]  # TA15-20
SEEDS = [2, 3, 4]
EPISODES = 1000
N_EVAL = 64
CLAVES = ["rwmakespan", "rwidle", "rwcritical", "rwbalance",
          "rwprogress", "rwlocal"]
NOMBRES = ["makespan", "idle", "critical", "balance", "progress", "local"]


def lee_ganador():
    t = open("tuning/irace_reward.log", encoding="utf-8",
             errors="replace").read()
    i = t.rindex("Best configurations as commandlines")
    linea = next(l for l in t[i:].splitlines()[1:] if l.strip()
                 and l.strip()[0].isdigit())
    vals = dict(re.findall(r"--(rw-[a-z]+) ([\d.]+)", linea))
    ident = linea.split()[0]
    pesos = {n: float(vals[f"rw-{n}"]) for n in NOMBRES}
    return ident, pesos


def main():
    ident, pesos = lee_ganador()
    os.environ["DEEPLJSP_REWARD_WEIGHTS"] = ",".join(
        f"{k}={v}" for k, v in pesos.items())
    print(f"=== CONFIRMACIÓN ganadora #{ident} vs default "
          f"(4x{EPISODES} eps, {len(SEEDS)} semillas) ===")
    print("pesos:", os.environ["DEEPLJSP_REWARD_WEIGHTS"], flush=True)

    # los imports tocan el entorno DESPUÉS de fijar la variable
    from jobshop_rl.agents_v2 import AgentV2
    from jobshop_rl.agents_v2.batched_eval import evaluate_policy_batched
    from jobshop_rl.agents_v2.batched_train import train_batched
    from jobshop_rl.agents_v2.state_encoder import StateEncoder
    from jobshop_rl.data import PROBLEM_REGISTRY
    from jobshop_rl.data.literature_bounds import lb_for_problem_name
    from jobshop_rl.experiments.factory import EnvironmentFactory
    from jobshop_rl.models.interval import Interval
    from jobshop_rl.utils.seed_utils import set_random_seed

    def entrena(seed):
        agent = None
        for pid in TRAIN_IDS:
            env = EnvironmentFactory.create_from_problem(
                PROBLEM_REGISTRY[pid](), "adaptive", seed=seed)
            if agent is None:
                set_random_seed(seed)
                agent = AgentV2(env, seed=seed)
            else:
                prev = agent.network.state_dict()
                agent = AgentV2(env, seed=seed)
                agent.network.load_state_dict(prev)
            train_batched(agent, episodes=EPISODES, device="cuda")
        agent.save_checkpoint(f"models/v2_rewardwin_1000ep_seed{seed}.pt")
        return agent

    def carga_default(seed):
        env = EnvironmentFactory.create_from_problem(
            PROBLEM_REGISTRY[EVAL_IDS[0]](), "adaptive", seed=1)
        agent = AgentV2(env, seed=seed)
        agent.load_checkpoint(
            f"models/v2_final_deepsets_1000ep_seed{seed}.pt")
        return agent

    def eval_dev(agent, con_pesos):
        # la evaluacion es identica para ambos brazos: makespan
        # componente a componente, sin que la variable de pesos influya
        # (el reward no interviene en inferencia), pero se limpia por
        # higiene al evaluar el default
        if not con_pesos:
            os.environ.pop("DEEPLJSP_REWARD_WEIGHTS", None)
        else:
            os.environ["DEEPLJSP_REWARD_WEIGHTS"] = ",".join(
                f"{k}={v}" for k, v in pesos.items())
        out = {}
        for pid in EVAL_IDS:
            env = EnvironmentFactory.create_from_problem(
                PROBLEM_REGISTRY[pid](), "adaptive", seed=1)
            agent.env = env
            agent.encoder = StateEncoder(env)
            _, sched, _, _ = evaluate_policy_batched(agent, N_EVAL,
                                                     device="cuda", seed=1)
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

    gan, defr = {p: [] for p in EVAL_IDS}, {p: [] for p in EVAL_IDS}
    for seed in SEEDS:
        print(f"\n[seed {seed}] entrenando ganadora #{ident} ...", flush=True)
        a = entrena(seed)
        rg = eval_dev(a, True)
        for p, v in rg.items():
            gan[p].append(v)
        print(f"[seed {seed}] ganadora dev RE: "
              + " ".join(f"{v:.1f}" for v in rg.values())
              + f"  media={sum(rg.values())/6:.2f}", flush=True)
        d = carga_default(seed)
        rd = eval_dev(d, False)
        for p, v in rd.items():
            defr[p].append(v)
        print(f"[seed {seed}] default  dev RE: "
              + " ".join(f"{v:.1f}" for v in rd.values())
              + f"  media={sum(rd.values())/6:.2f}", flush=True)

    print("\n=== RESULTADO (pareado por instancia y semilla) ===")
    pares = [(gan[p][i] - defr[p][i]) for p in EVAL_IDS
             for i in range(len(SEEDS))]
    mg = sum(v for p in EVAL_IDS for v in gan[p]) / len(pares)
    md = sum(v for p in EVAL_IDS for v in defr[p]) / len(pares)
    mejor = sum(1 for d in pares if d < 0)
    print(f"MEDIA  {mg:.2f}  {md:.2f}  {mg - md:+.2f}")
    print(f"mejor en {mejor} de {len(pares)} pares")
    try:
        from scipy import stats
        p = stats.wilcoxon(pares)[1]
        print(f"Wilcoxon pareado: p={p:.4f}")
        if mg < md and p < 0.05:
            print("VEREDICTO: la ganadora mejora significativamente -> "
                  "regla 2 del plan (reentrenar el aparato)")
        else:
            print("VEREDICTO: sin mejora significativa -> regla 1 del plan "
                  "(los pesos a mano quedan validados)")
    except ImportError:
        print("(sin scipy: veredicto manual)")


if __name__ == "__main__":
    main()
