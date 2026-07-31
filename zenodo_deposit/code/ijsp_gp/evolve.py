"""
Genetic-programming evolution of dispatching rules.

Fitness is the mean RE of one deterministic constructive pass over the
training instances; selection by tournament, subtree crossover and subtree
mutation, generational replacement with elitism, and a node cap on tree size.

Objectives:

* ``midpoint``: RE of the expected makespan (the paper's main objective).
* ``robust``: upper bound plus ``lam`` times the interval width, both
  normalized by the reference bound (the width-penalizing objective).

Example (a full evolution with the configuration used in the paper)::

    python -m ijsp_gp.evolve --pop 100 --gens 50 --seed 1 \
        --tournament 7 --crossover 0.7695 --maxtree 30 --elitism 2 \
        --train ../instances/interval_taillard \
        --train-ids int__tai20_15_01,int__tai20_15_02,int__tai20_15_03,int__tai20_15_04 \
        --out rule_seed1.json
"""

import argparse
import json
import random
import sys
import time

from .env import make_env
from .instances import lb_for_instance_name, load_dir
from .interval import Interval
from .rules import (GPRuleHeuristic, TERMINALS, crossover, mutate,
                    random_tree, tree_size, tree_str)


def rollout_re(env, heuristic, lb, fitness="midpoint", lam=0.0) -> float:
    state = env.reset()
    done = False
    while not done and state["eligible_ops"]:
        f = env.get_features(state)
        a = min(heuristic.select_action(state["eligible_ops"], f),
                len(state["eligible_ops"]) - 1)
        state, _, done, _ = env.step(a)
    from .interval import final_makespan
    m = final_makespan(env.job_completion_time)
    if isinstance(m, Interval):
        lo, up = float(m.lower), float(m.upper)
    else:
        lo = up = float(m)
    if fitness == "robust":
        val = up + lam * (up - lo)
    else:
        val = (lo + up) / 2.0
    return (val - lb) / lb * 100


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pop", type=int, default=100)
    parser.add_argument("--gens", type=int, default=50)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--tournament", type=int, default=7)
    parser.add_argument("--crossover", type=float, default=0.7695,
                        help="crossover probability (1-crossover = mutation)")
    parser.add_argument("--maxtree", type=int, default=30,
                        help="node cap on tree size (bloat control)")
    parser.add_argument("--elitism", type=int, default=2)
    parser.add_argument("--no-width", action="store_true",
                        help="exclude the interval-width terminals "
                             "(PTW, ESTW, WKRW) from the terminal set")
    parser.add_argument("--fitness", choices=["midpoint", "robust"],
                        default="midpoint")
    parser.add_argument("--lam", type=float, default=1.0,
                        help="width weight of the robust objective")
    parser.add_argument("--train", required=True,
                        help="directory with the training instance files")
    parser.add_argument("--train-ids", default="",
                        help="comma-separated instance names inside --train "
                             "(default: all instances in the directory)")
    parser.add_argument("--out", default="gp_rule_best.json")
    args = parser.parse_args()

    problems = load_dir(args.train)
    ids = [p.strip() for p in args.train_ids.split(",") if p.strip()] \
        or sorted(problems)
    rng = random.Random(args.seed)
    train = [(pid, make_env(problems[pid], seed=args.seed),
              lb_for_instance_name(pid)) for pid in ids]

    WIDTH = {"PTW", "ESTW", "WKRW"}
    terminals = [t for t in TERMINALS if t not in WIDTH] if args.no_width \
        else list(TERMINALS)

    def fitness(tree) -> float:
        if tree_size(tree) > args.maxtree:
            return float("inf")
        h = GPRuleHeuristic(tree)
        return sum(rollout_re(env, h, lb, args.fitness, args.lam)
                   for _, env, lb in train) / len(train)

    # initial population: ramped half-and-half plus two seeded classic rules
    population = [random_tree(rng, depth=rng.choice([2, 3, 4]),
                              full=rng.random() < 0.5, terminals=terminals)
                  for _ in range(args.pop - 2)]
    population.append("PT")            # SPT
    population.append(("neg", "WKR"))  # MWKR

    start = time.time()
    scored = sorted(((fitness(t), t) for t in population), key=lambda x: x[0])
    print(f"gen  0 | best={scored[0][0]:.2f}% | "
          f"mean={sum(s for s, _ in scored)/len(scored):.1f}% "
          f"| {time.time()-start:.0f}s", flush=True, file=sys.stderr)

    for gen in range(1, args.gens + 1):
        elite = [t for _, t in scored[:args.elitism]]
        children = list(elite)
        while len(children) < args.pop:
            def pick():
                return min(rng.sample(scored, args.tournament),
                           key=lambda x: x[0])[1]
            if rng.random() < args.crossover:
                child = crossover(rng, pick(), pick())
            else:
                child = mutate(rng, pick(), terminals=terminals)
            children.append(child)
        scored = sorted(((fitness(t), t) for t in children),
                        key=lambda x: x[0])
        print(f"gen {gen:>2} | best={scored[0][0]:.2f}% | "
              f"mean={sum(s for s, _ in scored)/len(scored):.1f}% "
              f"| best rule: {tree_str(scored[0][1])} "
              f"| {time.time()-start:.0f}s", flush=True, file=sys.stderr)

    best_fit, best_tree = scored[0]
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({"fitness_re": best_fit, "rule": tree_str(best_tree),
                   "tree": best_tree, "pop": args.pop, "gens": args.gens,
                   "seed": args.seed, "train_ids": ",".join(ids)}, f, indent=2)
    print(f"\nBest rule ({best_fit:.2f}% training RE): {tree_str(best_tree)}")
    print(f"Saved to {args.out}")


if __name__ == "__main__":
    main()
