"""
Confirmación pre-registrada: élite irace #22 vs default, a presupuesto de
operación completo.

- Entrena SOLO la #22 (la default ya existe en models/v2_final_deepsets_*).
- Protocolo idéntico al modelo final: TA11-14, 1000 eps/instancia, bloques
  secuenciales con transferencia de pesos, 3 semillas (2,3,4).
- Evalúa AMBAS configuraciones con el MISMO evaluador batcheado (best-of-64,
  seed de muestreo fija) sobre el dev completo TA15-20 → comparación pareada.
- Regla de adopción (pre-registrada): adoptar la #22 solo si mejora de forma
  clara — media de RE menor Y (mejor en >=3 instancias con 0 peores). En
  cualquier otro caso, la default se mantiene (resultado de robustez).

Hilos limitados (evita la sobresuscripción que congeló la máquina).
"""

import os
import sys

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
sys.path.insert(0, ".")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import torch
torch.set_num_threads(2)

from jobshop_rl.agents_v2 import AgentV2
from jobshop_rl.agents_v2.batched_eval import evaluate_policy_batched
from jobshop_rl.agents_v2.batched_train import train_batched
from jobshop_rl.agents_v2.state_encoder import StateEncoder
from jobshop_rl.data import PROBLEM_REGISTRY
from jobshop_rl.data.literature_bounds import lb_for_problem_name
from jobshop_rl.experiments.factory import EnvironmentFactory
from jobshop_rl.models.interval import Interval
from jobshop_rl.utils.seed_utils import set_random_seed

TRAIN_IDS = ["int__tai20_15_01", "int__tai20_15_02",
             "int__tai20_15_03", "int__tai20_15_04"]
EVAL_IDS = [f"int__tai20_15_{i:02d}" for i in range(5, 11)]  # TA15-20
SEEDS = [2, 3, 4]
EPISODES = 1000
N_EVAL = 64

ELITE = dict(lr=7e-4, entropy_coef=0.0063, eps_clip=0.1, K_epochs=8,
             gae_lambda=0.90, hidden_dim=256, minibatch_size=256,
             update_every_episodes=4)
DEFAULT = dict(lr=3e-4, entropy_coef=0.01, eps_clip=0.2, K_epochs=4,
               gae_lambda=0.95, hidden_dim=128, minibatch_size=256,
               update_every_episodes=4)


def train_elite(seed):
    agent = None
    for pid in TRAIN_IDS:
        env = EnvironmentFactory.create_from_problem(
            PROBLEM_REGISTRY[pid](), "adaptive", seed=seed)
        if agent is None:
            set_random_seed(seed)
            agent = AgentV2(env, seed=seed, **ELITE)
        else:
            prev = agent.network.state_dict()
            agent = AgentV2(env, seed=seed, **ELITE)
            agent.network.load_state_dict(prev)
        train_batched(agent, episodes=EPISODES, device="cuda")
    agent.save_checkpoint(f"models/v2_elite22_1000ep_seed{seed}.pt")
    return agent


def load_default(seed):
    env = EnvironmentFactory.create_from_problem(
        PROBLEM_REGISTRY[EVAL_IDS[0]](), "adaptive", seed=1)
    agent = AgentV2(env, seed=seed, **DEFAULT)
    agent.load_checkpoint(f"models/v2_final_deepsets_1000ep_seed{seed}.pt")
    return agent


def eval_dev(agent):
    """RE (punto medio) por instancia del dev, best-of-N batcheado."""
    out = {}
    for pid in EVAL_IDS:
        env = EnvironmentFactory.create_from_problem(
            PROBLEM_REGISTRY[pid](), "adaptive", seed=1)
        agent.env = env
        agent.encoder = StateEncoder(env)
        _, sched, _, _ = evaluate_policy_batched(agent, N_EVAL,
                                                 device="cuda", seed=1)
        best = None
        for t in sched:
            end = t.get("end")
            up = float(end.upper) if isinstance(end, Interval) else float(end)
            mid = end.midpoint if isinstance(end, Interval) else float(end)
            if best is None or up > best[1]:
                best = (mid, up)
        lb = lb_for_problem_name(pid)
        out[pid] = (best[0] - lb) / lb * 100
    return out


def main():
    print("=== CONFIRMACIÓN élite #22 vs default (1000 eps, 3 semillas) ===",
          flush=True)
    elite_res, default_res = {p: [] for p in EVAL_IDS}, {p: [] for p in EVAL_IDS}

    for seed in SEEDS:
        print(f"\n[seed {seed}] entrenando #22 ...", flush=True)
        a_elite = train_elite(seed)
        re_e = eval_dev(a_elite)
        for p, v in re_e.items():
            elite_res[p].append(v)
        print(f"[seed {seed}] #22 dev RE: "
              + " ".join(f"{v:.1f}" for v in re_e.values())
              + f"  media={sum(re_e.values())/len(re_e):.2f}", flush=True)

        a_def = load_default(seed)
        re_d = eval_dev(a_def)
        for p, v in re_d.items():
            default_res[p].append(v)
        print(f"[seed {seed}] def dev RE: "
              + " ".join(f"{v:.1f}" for v in re_d.values())
              + f"  media={sum(re_d.values())/len(re_d):.2f}", flush=True)

    # Agregado por instancia (media sobre semillas) y veredicto
    print("\n=== RESULTADO (media sobre 3 semillas, RE punto medio) ===",
          flush=True)
    print(f"{'Instancia':<20}{'#22':>8}{'default':>10}{'Δ':>8}", flush=True)
    e_means, d_means = [], []
    better = worse = 0
    for p in EVAL_IDS:
        e = sum(elite_res[p]) / len(elite_res[p])
        d = sum(default_res[p]) / len(default_res[p])
        e_means.append(e)
        d_means.append(d)
        delta = e - d
        if delta < -0.1:
            better += 1
        elif delta > 0.1:
            worse += 1
        print(f"{p:<20}{e:>8.2f}{d:>10.2f}{delta:>+8.2f}", flush=True)

    e_mean = sum(e_means) / len(e_means)
    d_mean = sum(d_means) / len(d_means)
    print("-" * 46, flush=True)
    print(f"{'MEDIA':<20}{e_mean:>8.2f}{d_mean:>10.2f}{e_mean-d_mean:>+8.2f}",
          flush=True)
    print(f"\n#22 mejor en {better} instancias, peor en {worse} "
          f"(de {len(EVAL_IDS)}).", flush=True)
    adopt = (e_mean < d_mean) and (better >= 3) and (worse == 0)
    print(f"VEREDICTO (regla pre-registrada): "
          f"{'ADOPTAR #22' if adopt else 'MANTENER default (robusta)'}",
          flush=True)


if __name__ == "__main__":
    main()
