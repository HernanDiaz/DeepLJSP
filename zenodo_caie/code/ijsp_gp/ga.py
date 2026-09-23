"""
Genetic algorithm for the interval job shop, on a permutation with
repetition of jobs.

This is the per-instance search method of the paper's budget comparison.
It follows the design of the genetic algorithm published for the IJSP
(permutation with repetition, job-based order crossover, tournament
selection, elitism, lexicographic ranking of interval makespans) and runs
on the same decoder and evaluator as the evolved rules (``simulate.py``).
Its cost is counted in schedule constructions, the implementation-
independent budget measure; the caller measures wall-clock time.

Usage from the ``code/`` directory:

    python -m ijsp_gp.ga --instance ../instances/interval_taillard/int__tai15_15_01.txt \
        --budget 131072 --seed 1
"""

import argparse
import random
import time
from typing import Dict, List, Optional, Tuple

from .simulate import Instance, better, decode


def random_permutation(inst: Instance, rng: random.Random) -> List[int]:
    perm = [j for j in range(inst.n) for _ in range(inst.m)]
    rng.shuffle(perm)
    return perm


def job_order_crossover(p1: List[int], p2: List[int], n: int,
                        rng: random.Random) -> List[int]:
    """A random subset of jobs keeps its positions from the first parent;
    the remaining positions are filled in the order of the second."""
    keep = {j for j in range(n) if rng.random() < 0.5}
    child = [j if j in keep else None for j in p1]
    rest = [j for j in p2 if j not in keep]
    k = 0
    for i, v in enumerate(child):
        if v is None:
            child[i] = rest[k]
            k += 1
    return child


def swap_mutation(perm: List[int], rng: random.Random) -> None:
    """Swap two positions; any permutation with repetition is feasible."""
    i, j = rng.randrange(len(perm)), rng.randrange(len(perm))
    perm[i], perm[j] = perm[j], perm[i]


def evolve(inst: Instance, budget: int, rng: random.Random, pop: int = 250,
           tournament: int = 3, p_crossover: float = 0.9,
           p_mutation: float = 0.2, elite: int = 2,
           seed_perm: Optional[List[int]] = None,
           checkpoints: Optional[List[int]] = None):
    """Run the GA until ``budget`` schedule constructions.

    Returns ({constructions: (best makespan so far, seconds)}, best
    makespan). One run yields the whole quality-budget curve at the
    requested ``checkpoints``. ``seed_perm`` places one given permutation,
    such as the one an evolved rule builds, in the initial population.
    """
    points = sorted(checkpoints or [budget])
    t0 = time.time()
    curve, used = {}, 0
    population = []
    if seed_perm is not None:
        population.append(list(seed_perm))
    while len(population) < pop:
        population.append(random_permutation(inst, rng))

    best_cm = None

    def record(cm):
        nonlocal best_cm, used
        used += 1
        if best_cm is None or better(cm, best_cm):
            best_cm = cm
        while points and used >= points[0]:
            curve[points.pop(0)] = (best_cm, time.time() - t0)

    scored = []
    for ind in population:
        cm = decode(inst, ind)
        record(cm)
        scored.append((cm, ind))
        if used >= budget:
            break

    while used < budget:
        scored.sort(key=lambda x: (x[0][1], x[0][0]))
        new = [s for s in scored[:elite]]
        while len(new) < pop and used < budget:
            a = min((scored[rng.randrange(len(scored))]
                     for _ in range(tournament)),
                    key=lambda x: (x[0][1], x[0][0]))
            b = min((scored[rng.randrange(len(scored))]
                     for _ in range(tournament)),
                    key=lambda x: (x[0][1], x[0][0]))
            child = (job_order_crossover(a[1], b[1], inst.n, rng)
                     if rng.random() < p_crossover else list(a[1]))
            if rng.random() < p_mutation:
                swap_mutation(child, rng)
            cm = decode(inst, child)
            record(cm)
            new.append((cm, child))
        scored = new

    for p in points:                 # if the budget ended first
        curve[p] = (best_cm, time.time() - t0)
    return curve, best_cm


def random_search(inst: Instance, budget: int, rng: random.Random,
                  checkpoints: Optional[List[int]] = None):
    """Uniformly sampled permutations on the same decoder: the floor any
    search method is measured against."""
    points = sorted(checkpoints or [budget])
    t0 = time.time()
    curve, best_cm = {}, None
    for k in range(1, budget + 1):
        cm = decode(inst, random_permutation(inst, rng))
        if best_cm is None or better(cm, best_cm):
            best_cm = cm
        while points and k >= points[0]:
            curve[points.pop(0)] = (best_cm, time.time() - t0)
    for p in points:
        curve[p] = (best_cm, time.time() - t0)
    return curve, best_cm


def main():
    from .instances import lb_for_instance_name, load_instance
    import os

    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--instance", required=True)
    ap.add_argument("--budget", type=int, default=131072)
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()

    name = os.path.splitext(os.path.basename(args.instance))[0]
    inst = Instance(load_instance(args.instance, name))
    lb = lb_for_instance_name(name)
    points = [2 ** k for k in range(0, 18) if 2 ** k <= args.budget]
    curve, _ = evolve(inst, args.budget, random.Random(args.seed),
                      checkpoints=points)
    for p in points:
        (lo, up), sec = curve[p]
        re_pct = ((lo + up) / 2 - lb) / lb * 100 if lb else float("nan")
        print(f"{p:>7} constructions  [{lo:.0f}, {up:.0f}]  "
              f"RE {re_pct:6.2f}  {sec:7.2f} s")


if __name__ == "__main__":
    main()
