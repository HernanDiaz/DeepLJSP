"""
Target-runner para la configuración de hiperparámetros del AgentV2 (irace).

Entrena el agente con la configuración dada a fidelidad reducida (TA11+TA12,
300 episodios por instancia, bloques secuenciales con transferencia como el
pipeline estándar) y evalúa best-of-16 en TA15-17. Imprime UNA línea final
con el coste (RE medio por E[Cmax], menor = mejor), que es lo que irace lee.

Uso (los nombres de flag coinciden con parameters.txt de irace):
  python scripts/train_eval_config.py --seed 3 --lr 3e-4 --entropy 0.01 \
      --clip 0.2 --kepochs 4 --minibatch 256 --update-every 4 \
      --gae 0.95 --hidden 128
"""

import argparse
import os
import sys

sys.path.insert(0, ".")

# Limitar hilos ANTES de importar torch: con varios workers de irace en
# paralelo, el intra-op parallelism por defecto de torch (= n. de logicos)
# sobresuscribe la CPU (4 nucleos fisicos aqui) y llega a congelar la
# maquina. 2 hilos/worker deja holgura al SO y a los entornos Python.
os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
import torch
torch.set_num_threads(2)

from jobshop_rl.agents_v2 import AgentV2
from jobshop_rl.agents_v2.state_encoder import StateEncoder
from jobshop_rl.data import PROBLEM_REGISTRY
from jobshop_rl.data.literature_bounds import lb_for_problem_name
from jobshop_rl.experiments.factory import EnvironmentFactory
from jobshop_rl.models.interval import Interval
from jobshop_rl.utils.seed_utils import set_random_seed

TRAIN_IDS = ["int__tai20_15_01", "int__tai20_15_02"]
EVAL_IDS = ["int__tai20_15_05", "int__tai20_15_06", "int__tai20_15_07"]
EPISODES_PER_INSTANCE = 300
N_EVAL_SAMPLES = 16


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--lr", type=float, default=3e-4)
    parser.add_argument("--entropy", type=float, default=0.01)
    parser.add_argument("--clip", type=float, default=0.2)
    parser.add_argument("--kepochs", type=int, default=4)
    parser.add_argument("--minibatch", type=int, default=256)
    parser.add_argument("--update-every", type=int, default=4)
    parser.add_argument("--gae", type=float, default=0.95)
    parser.add_argument("--hidden", type=int, default=128)
    parser.add_argument("--attention", type=int, default=0,
                        help="capas de atención (campaña de la variante attention)")
    parser.add_argument("--heads", type=int, default=4)
    parser.add_argument("--episodes", type=int, default=EPISODES_PER_INSTANCE)
    parser.add_argument("--train-ids", type=str, default=",".join(TRAIN_IDS))
    parser.add_argument("--eval-samples", type=int, default=N_EVAL_SAMPLES)
    parser.add_argument("--batched", action="store_true",
                        help="rutas vectorizadas (batched_train/batched_eval); "
                             "por defecto, caminos secuenciales originales")
    parser.add_argument("--device", type=str, default=None,
                        help="cpu|cuda para las rutas batcheadas (None = auto)")
    # Campana de pesos del reward: si se dan, se exporta
    # DEEPLJSP_REWARD_WEIGHTS y la factoria usa estos seis valores fijos
    # en lugar del generador (y sin el reajuste por instancia)
    for _rw in ("rw-makespan", "rw-idle", "rw-critical", "rw-balance",
                "rw-progress", "rw-local"):
        parser.add_argument(f"--{_rw}", type=float, default=None)
    args = parser.parse_args()

    _rws = {k: getattr(args, f"rw_{k}") for k in
            ("makespan", "idle", "critical", "balance", "progress", "local")}
    if any(v is not None for v in _rws.values()):
        if any(v is None for v in _rws.values()):
            parser.error("los seis --rw-* van juntos o ninguno")
        os.environ["DEEPLJSP_REWARD_WEIGHTS"] = ",".join(
            f"{k}={v}" for k, v in _rws.items())

    train_ids = [p.strip() for p in args.train_ids.split(",") if p.strip()]

    set_random_seed(args.seed)

    def make_agent(env):
        return AgentV2(
            env, seed=args.seed, lr=args.lr, entropy_coef=args.entropy,
            eps_clip=args.clip, K_epochs=args.kepochs,
            minibatch_size=args.minibatch,
            update_every_episodes=args.update_every,
            gae_lambda=args.gae, hidden_dim=args.hidden,
            attention_layers=args.attention, attention_heads=args.heads,
        )

    # Entrenamiento por bloques con transferencia de pesos (como el pipeline)
    agent = None
    for pid in train_ids:
        env = EnvironmentFactory.create_from_problem(
            PROBLEM_REGISTRY[pid](), "adaptive", seed=args.seed)
        if agent is None:
            agent = make_agent(env)
        else:
            prev_state = agent.network.state_dict()
            agent = make_agent(env)
            agent.network.load_state_dict(prev_state)
        if args.batched:
            from jobshop_rl.agents_v2.batched_train import train_batched
            train_batched(agent, episodes=args.episodes, device=args.device)
        else:
            agent.train(episodes=args.episodes)

    # Evaluación best-of-N en el conjunto de desarrollo reducido
    res = []
    for pid in EVAL_IDS:
        env = EnvironmentFactory.create_from_problem(
            PROBLEM_REGISTRY[pid](), "adaptive", seed=args.seed)
        agent.env = env
        agent.encoder = StateEncoder(env)
        if args.batched:
            from jobshop_rl.agents_v2.batched_eval import evaluate_policy_batched
            _, schedule, _, _ = evaluate_policy_batched(
                agent, args.eval_samples, device=args.device)
        else:
            _, schedule, _, _ = agent.evaluate_policy(n_samples=args.eval_samples)
        best = None
        for t in schedule:
            end = t.get("end")
            if isinstance(end, Interval):
                mid, up = end.midpoint, float(end.upper)
            else:
                mid, up = float(end), float(end)
            if best is None or up > best[1]:
                best = (mid, up)
        lb = lb_for_problem_name(pid)
        res.append((best[0] - lb) / lb * 100)

    # Última línea = coste para irace
    print(f"{sum(res) / len(res):.4f}")


if __name__ == "__main__":
    main()
