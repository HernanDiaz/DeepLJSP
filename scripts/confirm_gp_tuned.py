"""
Confirmación pre-registrada del GP tuneado (config ganadora de irace #15)
vs el GP con configuración por defecto.

Evoluciona reglas con la config ganadora (TA11-14 × 3 semillas, mismo
pop/gens que la default) y evalúa cada regla sobre las 70 Taillard. Compara
el RE global con el 18.5% del GP default (semilla 1, la mejor de las 3
convencionales). Regla de adopción para el paper_gp: adoptar la config
tuneada solo si mejora de forma clara; en otro caso, "GP robusto a sus
hiperparámetros".

Hilos limitados (GP CPU-bound; evita sobresuscripción).
"""

import json
import os
import random
import sys

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
sys.path.insert(0, ".")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data import PROBLEM_REGISTRY
from jobshop_rl.data.literature_bounds import lb_for_problem_name
from jobshop_rl.experiments.factory import EnvironmentFactory
from jobshop_rl.heuristics.gp_rule import (
    GPRuleHeuristic, crossover, mutate, random_tree, tree_size, tree_str,
)
from jobshop_rl.models.interval import Interval

TRAIN_IDS = ["int__tai20_15_01", "int__tai20_15_02",
             "int__tai20_15_03", "int__tai20_15_04"]
CLASSES = ["15_15", "20_15", "20_20", "30_15", "30_20", "50_15", "50_20"]
SEEDS = [1, 2, 3]
POP, GENS = 100, 50
# Config ganadora irace #15
TOURNAMENT, CROSSOVER, MAXTREE, ELITISM = 7, 0.7695, 30, 2


def rollout_re(env, h, lb):
    state = env.reset()
    done = False
    while not done and state["eligible_ops"]:
        f = env.get_features(state)
        a = min(h.select_action(state["eligible_ops"], f),
                len(state["eligible_ops"]) - 1)
        state, _, done, _ = env.step(a)
    m = max(env.job_completion_time)
    mid = m.midpoint if isinstance(m, Interval) else float(m)
    return (mid - lb) / lb * 100


def evolve(seed):
    rng = random.Random(seed)
    train = [(EnvironmentFactory.create_from_problem(
                  PROBLEM_REGISTRY[p](), "basic", seed=seed),
              lb_for_problem_name(p)) for p in TRAIN_IDS]

    def fitness(t):
        if tree_size(t) > MAXTREE:
            return float("inf")
        h = GPRuleHeuristic(t)
        return sum(rollout_re(e, h, lb) for e, lb in train) / len(train)

    pop = [random_tree(rng, depth=rng.choice([2, 3, 4]), full=rng.random() < 0.5)
           for _ in range(POP - 2)]
    pop += ["PT", ("neg", "WKR")]
    scored = sorted(((fitness(t), t) for t in pop), key=lambda x: x[0])
    for _ in range(GENS):
        children = [t for _, t in scored[:ELITISM]]
        while len(children) < POP:
            def pick():
                return min(rng.sample(scored, TOURNAMENT), key=lambda x: x[0])[1]
            children.append(crossover(rng, pick(), pick())
                            if rng.random() < CROSSOVER else mutate(rng, pick()))
        scored = sorted(((fitness(t), t) for t in children), key=lambda x: x[0])
    return scored[0]


def eval_70(tree):
    h = GPRuleHeuristic(tree)
    per_class, allv = {}, []
    for cls in CLASSES:
        vals = []
        for i in range(1, 11):
            pid = f"int__tai{cls}_{i:02d}"
            env = EnvironmentFactory.create_from_problem(
                PROBLEM_REGISTRY[pid](), "basic", seed=1)
            vals.append(rollout_re(env, h, lb_for_problem_name(pid)))
        per_class[cls] = sum(vals) / len(vals)
        allv.extend(vals)
    return per_class, sum(allv) / len(allv)


def main():
    print("=== CONFIRMACIÓN GP TUNEADO (irace #15) vs DEFAULT ===", flush=True)
    print(f"config: tournament {TOURNAMENT}, crossover {CROSSOVER}, "
          f"maxtree {MAXTREE}, elitism {ELITISM}\n", flush=True)
    results = {}
    for s in SEEDS:
        fit, tree = evolve(s)
        pc, glob = eval_70(tree)
        results[s] = (fit, glob, pc, tree_size(tree))
        json.dump({"fitness_re": fit, "rule": tree_str(tree), "tree": tree,
                   "global_re_70": glob, "seed": s,
                   "config": "irace15_t7_c0.77_m30_e2"},
                  open(f"benchmarks/gp_tuned_seed{s}.json", "w"), indent=2)
        print(f"[seed {s}] train fit={fit:.2f}% | GLOBAL 70 = {glob:.2f}% | "
              f"tree {tree_size(tree)} nodos", flush=True)

    print("\n=== RESUMEN (RE global sobre 70 instancias) ===", flush=True)
    best = min(results.items(), key=lambda kv: kv[1][1])
    for s, (fit, glob, pc, sz) in results.items():
        print(f"  tuned seed {s}: {glob:.2f}%", flush=True)
    print(f"\n  GP tuneado mejor:  {best[1][1]:.2f}%  (semilla {best[0]})",
          flush=True)
    print(f"  GP default (ref):  18.50%", flush=True)
    delta = best[1][1] - 18.5
    print(f"  Δ = {delta:+.2f} puntos", flush=True)
    print(f"  VEREDICTO: {'ADOPTAR config tuneada' if delta < -0.3 else 'GP ROBUSTO a sus knobs (mantener default)'}",
          flush=True)


if __name__ == "__main__":
    main()
