"""
Exporta pools de soluciones para sembrar la población inicial del TS.

Formato de salida (un CSV por instancia, una solución por línea):
    j1 j2 j3 ... jN;[lower, upper]
donde j1..jN es la permutación con repetición de trabajos (1-based): cada
aparición k-ésima del trabajo j significa "k-ésima operación del trabajo j",
en el orden en que fueron programadas. Tras ';' va el intervalo de makespan
del schedule semiactivo correspondiente.

Generadores:
  --generator v2     muestreos de la política aprendida (reparte el pool entre
                     los checkpoints pasados con --checkpoints)
  --generator grasp  despacho aleatorizado (regla al azar por individuo entre
                     SPT/LPT/MOR/MWKR/EST + ruido epsilon-greedy por paso)

Uso:
  python scripts/export_v2_seeds.py --instance int__tai15_15_05 --n 1024 \
      --generator v2 --checkpoints ckptA.pt,ckptB.pt,ckptC.pt --out seeds/
  python scripts/export_v2_seeds.py --instance int__tai15_15_05 --n 1024 \
      --generator grasp --epsilon 0.1 --out seeds/
"""

import argparse
import os
import random
import sys
import time

sys.path.insert(0, ".")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.agents_v2 import AgentV2  # noqa: E402
from jobshop_rl.data import PROBLEM_REGISTRY  # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.heuristics.strategies import (  # noqa: E402
    SPTHeuristic, LPTHeuristic, MORHeuristic, MWKRHeuristic, GTHeuristic,
)
from jobshop_rl.models.interval import Interval, final_makespan  # noqa: E402
from jobshop_rl.utils.seed_utils import set_random_seed  # noqa: E402


def _makespan_str(env) -> str:
    # Agregacion componente a componente (NO max() lexicografico): asi el lower
    # guardado es la cota real, no el lower del trabajo de mayor upper.
    m = final_makespan(env.job_completion_time)
    if isinstance(m, Interval):
        return f"[{int(m.lower)}, {int(m.upper)}]"
    return f"[{int(m)}, {int(m)}]"


def rollout_v2(agent, env):
    """Un muestreo de la política; devuelve (permutación 1-based, makespan)."""
    state = env.reset()
    permutation = []
    done = False
    while not done:
        action_idx, _, _ = agent.select_action(state, training=True)
        if action_idx is None:
            break
        permutation.append(state["eligible_ops"][action_idx] + 1)
        state, _, done, _ = env.step(action_idx)
    return permutation, _makespan_str(env)


def rollout_grasp(env, rules, epsilon, rng):
    """
    Despacho aleatorizado: regla fija por individuo + ruido epsilon por paso.
    Si la regla lleva ruido interno (GTHeuristic con epsilon>0), no se aplica
    ruido externo — la aleatorización ocurre dentro del conflict set.
    """
    rule = rng.choice(rules)
    internal_noise = getattr(rule, "epsilon", 0.0) > 0
    state = env.reset()
    permutation = []
    done = False
    while not done:
        eligible = state["eligible_ops"]
        if not eligible:
            break
        if not internal_noise and rng.random() < epsilon:
            action_idx = rng.randrange(len(eligible))
        else:
            features = env.get_features(state)
            action_idx = min(rule.select_action(eligible, features), len(eligible) - 1)
        permutation.append(eligible[action_idx] + 1)
        state, _, done, _ = env.step(action_idx)
    return permutation, _makespan_str(env)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance", required=True)
    parser.add_argument("--n", type=int, default=1024)
    parser.add_argument("--generator", choices=["v2", "grasp"], default="v2")
    parser.add_argument("--checkpoints", type=str, default="",
                        help="rutas .pt separadas por comas (generator=v2)")
    parser.add_argument("--attention", type=int, default=0)
    parser.add_argument("--epsilon", type=float, default=0.1)
    parser.add_argument("--rules", type=str, default="spt,lpt,mor,mwkr",
                        help="reglas para el generador grasp, separadas por comas")
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--gp-json", type=str,
                        default="benchmarks/gp_tuned_seed3.json",
                        help="regla GP para --rules gp (JSON con 'tree')")
    parser.add_argument("--suffix", type=str, default="",
                        help="sufijo del nombre del pool (p.ej. 'gp' -> _gp_pool.csv)")
    parser.add_argument("--out", type=str, default="seeds")
    args = parser.parse_args()

    set_random_seed(args.seed)
    rng = random.Random(args.seed)

    problem = PROBLEM_REGISTRY[args.instance]()
    env = EnvironmentFactory.create_from_problem(problem, "adaptive", seed=args.seed)

    os.makedirs(args.out, exist_ok=True)
    tag = args.suffix if args.suffix else args.generator
    out_path = os.path.join(args.out, f"{args.instance}_{tag}_pool.csv")

    start = time.time()
    lines = []

    if args.generator == "v2":
        checkpoints = [c.strip() for c in args.checkpoints.split(",") if c.strip()]
        if not checkpoints:
            raise SystemExit("--checkpoints es obligatorio con --generator v2")
        per_ckpt = [args.n // len(checkpoints)] * len(checkpoints)
        per_ckpt[0] += args.n - sum(per_ckpt)
        for ckpt, count in zip(checkpoints, per_ckpt):
            agent = AgentV2(env, seed=args.seed, attention_layers=args.attention)
            agent.load_checkpoint(ckpt)
            for _ in range(count):
                perm, mk = rollout_v2(agent, env)
                lines.append(" ".join(map(str, perm)) + ";" + mk)
    else:
        def _gp_rule():
            # regla GP evolucionada (drop-in determinista; el ruido epsilon
            # externo del grasp la aleatoriza, espejo del protocolo GP-eps)
            import json
            from jobshop_rl.heuristics.gp_rule import GPRuleHeuristic

            def to_tuple(t):
                return tuple(to_tuple(x) for x in t) if isinstance(t, list) else t
            data = json.load(open(args.gp_json, encoding="utf-8"))
            return GPRuleHeuristic(to_tuple(data["tree"]))

        rule_map = {"spt": SPTHeuristic, "lpt": LPTHeuristic,
                    "mor": MORHeuristic, "mwkr": MWKRHeuristic,
                    # G&T aleatorizado: ruido interno al conflict set
                    "gtmwkr": lambda: GTHeuristic("mwkr", epsilon=args.epsilon, rng=rng),
                    "gp": _gp_rule}
        rules = []
        for r in args.rules.split(","):
            r = r.strip().lower()
            if r:
                factory = rule_map[r]
                rules.append(factory() if callable(factory) else factory)
        for _ in range(args.n):
            perm, mk = rollout_grasp(env, rules, args.epsilon, rng)
            lines.append(" ".join(map(str, perm)) + ";" + mk)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    # resumen de calidad del pool (por upper del intervalo)
    uppers = [int(l.split(";")[1].split(",")[1].strip(" ]")) for l in lines]
    print(f"{out_path}: {len(lines)} soluciones en {time.time()-start:.0f}s | "
          f"makespan upper: mejor={min(uppers)}, mediana={sorted(uppers)[len(uppers)//2]}, "
          f"peor={max(uppers)}")


if __name__ == "__main__":
    main()
