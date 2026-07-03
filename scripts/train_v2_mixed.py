"""
Entrenamiento mixto del AgentV2: muestreo de instancia por episodio.

Régimen nativo del diseño (AGENTS_V2_DESIGN.md): un único agente y optimizador
entrenan sobre las 4 instancias de entrenamiento intercaladas al azar, sin
bloques secuenciales ni reinicios de Adam entre problemas — posible gracias a
la invarianza al tamaño. Mismo presupuesto total que el pipeline por bloques
(400 episodios) para comparación justa.

Uso:
    python scripts/train_v2_mixed.py [--episodes 400] [--seed 2] [--tag mixed]
"""

import argparse
import json
import random
import sys
import time

sys.path.insert(0, ".")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.agents_v2 import AgentV2  # noqa: E402
from jobshop_rl.agents_v2.state_encoder import StateEncoder  # noqa: E402
from jobshop_rl.data import PROBLEM_REGISTRY  # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.utils.seed_utils import set_random_seed  # noqa: E402

TRAIN_IDS = ["int__tai20_15_01", "int__tai20_15_02", "int__tai20_15_03", "int__tai20_15_04"]
EVAL_IDS = [f"int__tai20_15_{i:02d}" for i in range(5, 11)]
N_SAMPLES = 64
UPDATE_EVERY = 4


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=400)
    parser.add_argument("--seed", type=int, default=2)
    parser.add_argument("--tag", type=str, default="v2-mixed")
    args = parser.parse_args()

    set_random_seed(args.seed)
    rng = random.Random(args.seed)

    train_envs = [EnvironmentFactory.create_from_problem(PROBLEM_REGISTRY[pid](), "adaptive", seed=args.seed)
                  for pid in TRAIN_IDS]
    encoders = [StateEncoder(env) for env in train_envs]

    agent = AgentV2(train_envs[0], seed=args.seed)

    start = time.time()
    for ep in range(1, args.episodes + 1):
        idx = rng.randrange(len(train_envs))
        # Cambiar de instancia = cambiar env y su encoder; el agente, la red
        # y el optimizador son los mismos durante todo el entrenamiento
        agent.env = train_envs[idx]
        agent.encoder = encoders[idx]

        makespan, total_reward = agent._run_episode(sample=True, store=True)
        agent.total_episodes += 1
        agent.training_makespan_history.append(makespan)
        agent.episode_rewards.append(total_reward)

        if ep % UPDATE_EVERY == 0:
            losses = agent.trainer.update(agent.buffer)
            agent.training_losses["policy"].append(losses["policy_loss"])
            agent.training_losses["value"].append(losses["value_loss"])

        if ep % 50 == 0:
            recent = agent.training_makespan_history[-50:]
            print(f"ep {ep:>4} | media últimos 50 = {sum(recent)/len(recent):.0f} "
                  f"| loss_v = {agent.training_losses['value'][-1]:.2f} "
                  f"| {time.time()-start:.0f}s", flush=True)

    if len(agent.buffer) > 0:
        agent.trainer.update(agent.buffer)

    train_time = time.time() - start
    print(f"\nEntrenamiento mixto: {args.episodes} episodios en {train_time:.0f}s")

    # Evaluación en los 6 problemas de test (best-of-N, igual que el pipeline)
    results = {}
    print(f"\n{'Instancia':<18} {'LB lit.':>7} {'makespan (up)':>13} {'RE (up)':>8}")
    print("-" * 52)
    for pid in EVAL_IDS:
        env = EnvironmentFactory.create_from_problem(PROBLEM_REGISTRY[pid](), "adaptive", seed=args.seed)
        agent.env = env
        agent.encoder = StateEncoder(env)
        mk, _, _, _ = agent.evaluate_policy(n_samples=N_SAMPLES)
        lb = lb_for_problem_name(pid)
        results[pid] = {"rl_makespan": mk, "lower_bound_lit": lb}
        print(f"{pid:<18} {lb:>7} {mk:>13.0f} {(mk-lb)/lb*100:>7.1f}%")

    out = {
        "tag": args.tag,
        "seed": args.seed,
        "episodes": args.episodes,
        "train_time_s": round(train_time, 1),
        "regime": "mixed-instance-sampling",
        "results": results,
    }
    path = f"benchmarks/{args.tag}_seed{args.seed}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    ckpt = f"benchmarks/{args.tag}_seed{args.seed}_model.pt"
    agent.save_checkpoint(ckpt)
    print(f"\nResultados: {path} | checkpoint: {ckpt}")


if __name__ == "__main__":
    main()
