"""
Evoluciona una regla de despacho por programación genética (hiper-heurística)
sobre las instancias de entrenamiento del proyecto.

Fitness = RE medio (E[Cmax] vs LB crisp) del despacho determinista con la
regla sobre las instancias de entrenamiento. Selección por torneo, cruce de
subárboles, mutación, elitismo. Sin dependencias externas.

Uso (smoke test):
  python scripts/evolve_gp_rule.py --pop 16 --gens 4 --train-ids int__tai20_15_01,int__tai20_15_02

Uso (evolución completa):
  python scripts/evolve_gp_rule.py --pop 100 --gens 50 --seed 1
"""

import argparse
import json
import os
import random
import sys
import time

# GP es CPU-bound (numpy sobre vectores diminutos): con varios workers de
# irace en paralelo, limitar los hilos de BLAS evita sobresuscripción.
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

sys.path.insert(0, ".")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data import PROBLEM_REGISTRY
from jobshop_rl.data.literature_bounds import lb_for_problem_name
from jobshop_rl.experiments.factory import EnvironmentFactory
from jobshop_rl.heuristics.gp_rule import (
    GPRuleHeuristic, crossover, mutate, random_tree, tree_size, tree_str,
)
from jobshop_rl.models.interval import Interval, final_makespan

DEFAULT_TRAIN = "int__tai20_15_01,int__tai20_15_02,int__tai20_15_03,int__tai20_15_04"


def rollout_re(env, heuristic, lb) -> float:
    state = env.reset()
    done = False
    while not done and state["eligible_ops"]:
        f = env.get_features(state)
        a = min(heuristic.select_action(state["eligible_ops"], f),
                len(state["eligible_ops"]) - 1)
        state, _, done, _ = env.step(a)
    m = final_makespan(env.job_completion_time)
    mid = m.midpoint if isinstance(m, Interval) else float(m)
    return (mid - lb) / lb * 100


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pop", type=int, default=100)
    parser.add_argument("--gens", type=int, default=50)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--tournament", type=int, default=4)
    parser.add_argument("--crossover", type=float, default=0.8,
                        help="prob. de cruce (1-crossover = prob. de mutación)")
    parser.add_argument("--maxtree", type=int, default=40,
                        help="cap de nodos del árbol (control de bloat)")
    parser.add_argument("--elitism", type=int, default=2,
                        help="n. de mejores que pasan intactos por generación")
    parser.add_argument("--no-width", action="store_true",
                        help="ABLACIÓN: excluye los terminales de anchura de "
                             "intervalo (PTW, ESTW, WKRW) del conjunto. Mide "
                             "cuánto aporta la información de incertidumbre.")
    parser.add_argument("--train-ids", type=str, default=DEFAULT_TRAIN)
    parser.add_argument("--eval-ids", type=str, default="",
                        help="si se da: tras evolucionar, evalúa la mejor regla "
                             "en estas instancias e imprime el RE medio como "
                             "última línea (coste para irace); no guarda JSON")
    parser.add_argument("--out", type=str, default="benchmarks/gp_rule_best.json")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    train = [(pid, EnvironmentFactory.create_from_problem(
                  PROBLEM_REGISTRY[pid](), "basic", seed=args.seed),
              lb_for_problem_name(pid))
             for pid in (p.strip() for p in args.train_ids.split(",")) if pid]

    # Conjunto de terminales (ablación --no-width: sin PTW/ESTW/WKRW).
    from jobshop_rl.heuristics.gp_rule import TERMINALS
    WIDTH = {"PTW", "ESTW", "WKRW"}
    terminals = [t for t in TERMINALS if t not in WIDTH] if args.no_width \
        else list(TERMINALS)

    def fitness(tree) -> float:
        if tree_size(tree) > args.maxtree:
            return float("inf")
        h = GPRuleHeuristic(tree)
        return sum(rollout_re(env, h, lb) for _, env, lb in train) / len(train)

    # Población inicial: ramped half-and-half + las reglas clásicas como semillas
    population = [random_tree(rng, depth=rng.choice([2, 3, 4]),
                              full=rng.random() < 0.5, terminals=terminals)
                  for _ in range(args.pop - 2)]
    population.append("PT")     # SPT
    population.append(("neg", "WKR"))  # MWKR

    # Progreso a stderr: así en modo --eval-ids el stdout queda limpio para
    # que irace lea el coste como última (y única relevante) línea.
    start = time.time()
    scored = sorted(((fitness(t), t) for t in population), key=lambda x: x[0])
    print(f"gen  0 | mejor={scored[0][0]:.2f}% | media={sum(s for s, _ in scored)/len(scored):.1f}% "
          f"| {time.time()-start:.0f}s", flush=True, file=sys.stderr)

    for gen in range(1, args.gens + 1):
        elite = [t for _, t in scored[:args.elitism]]
        children = list(elite)
        while len(children) < args.pop:
            def pick():
                return min(rng.sample(scored, args.tournament), key=lambda x: x[0])[1]
            if rng.random() < args.crossover:
                child = crossover(rng, pick(), pick())
            else:
                child = mutate(rng, pick(), terminals=terminals)
            children.append(child)
        scored = sorted(((fitness(t), t) for t in children), key=lambda x: x[0])
        print(f"gen {gen:>2} | mejor={scored[0][0]:.2f}% | "
              f"media={sum(s for s, _ in scored)/len(scored):.1f}% "
              f"| mejor regla: {tree_str(scored[0][1])} | {time.time()-start:.0f}s",
              flush=True, file=sys.stderr)

    best_fit, best_tree = scored[0]

    # Modo tuning (irace): evaluar la mejor regla en el conjunto de validación
    # e imprimir el RE medio como coste. NO se guarda JSON (es una corrida más
    # del racing, no un artefacto final).
    eval_ids = [p.strip() for p in args.eval_ids.split(",") if p.strip()]
    if eval_ids:
        h = GPRuleHeuristic(best_tree)
        re_val = []
        for pid in eval_ids:
            env = EnvironmentFactory.create_from_problem(
                PROBLEM_REGISTRY[pid](), "basic", seed=args.seed)
            re_val.append(rollout_re(env, h, lb_for_problem_name(pid)))
        print(f"{sum(re_val) / len(re_val):.4f}")
        return

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({"fitness_re": best_fit, "rule": tree_str(best_tree),
                   "tree": best_tree, "pop": args.pop, "gens": args.gens,
                   "seed": args.seed, "train_ids": args.train_ids}, f, indent=2)
    print(f"\nMejor regla ({best_fit:.2f}% RE en entrenamiento): {tree_str(best_tree)}")
    print(f"Guardada en {args.out}")


if __name__ == "__main__":
    main()
