"""
Test de equivalencia estadística y velocidad del entrenamiento batcheado.

Entrena en TA11 (100 episodios) con el camino secuencial (agent.train) y
con train_batched (CPU y GPU), mismas semillas, y compara:
- wall-clock (speedup)
- best_makespan de entrenamiento y makespan greedy final (calidad)

Criterio: calidad comparable entre caminos (misma escala +-ruido de semilla;
el orden RNG difiere, no se espera bit-igualdad) y speedup > 1.5x.

Uso: python scripts/test_batched_train.py [episodios]
"""

import sys
import time

sys.path.insert(0, ".")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import torch

from jobshop_rl.agents_v2 import AgentV2
from jobshop_rl.agents_v2.batched_train import train_batched
from jobshop_rl.data import PROBLEM_REGISTRY
from jobshop_rl.experiments.factory import EnvironmentFactory
from jobshop_rl.utils.seed_utils import set_random_seed

PID = "int__tai20_15_01"
EPISODES = int(sys.argv[1]) if len(sys.argv) > 1 else 100
SEEDS = [2, 3]


def fresh_agent(seed):
    set_random_seed(seed)
    env = EnvironmentFactory.create_from_problem(
        PROBLEM_REGISTRY[PID](), "adaptive", seed=seed)
    return AgentV2(env, seed=seed)


def final_greedy(agent):
    mk, _, _, _ = agent.evaluate_policy(n_samples=1)
    return mk


def main():
    torch.set_num_threads(2)
    has_cuda = torch.cuda.is_available()
    arms = [("secuencial", None), ("batch-cpu", "cpu")]
    if has_cuda:
        arms.append(("batch-gpu", "cuda"))

    print(f"{PID} | {EPISODES} episodios | semillas {SEEDS} | CUDA: {has_cuda}\n")
    print(f"{'camino':<12} {'semilla':>7} {'t(s)':>7} {'best train':>11} "
          f"{'greedy final':>13}")
    print("-" * 56)

    times = {}
    for name, device in arms:
        for seed in SEEDS:
            agent = fresh_agent(seed)
            t0 = time.time()
            if device is None:
                agent.train(episodes=EPISODES)
            else:
                train_batched(agent, episodes=EPISODES, device=device)
            elapsed = time.time() - t0
            times.setdefault(name, []).append(elapsed)
            print(f"{name:<12} {seed:>7} {elapsed:>7.0f} "
                  f"{agent.best_makespan:>11.0f} {final_greedy(agent):>13.0f}",
                  flush=True)

    base = sum(times["secuencial"]) / len(times["secuencial"])
    print()
    for name in times:
        t = sum(times[name]) / len(times[name])
        print(f"{name}: {t:.0f}s medio -> speedup {base/t:.2f}x")


if __name__ == "__main__":
    main()
