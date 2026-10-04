"""
Genetic algorithm for the interval job shop, on a permutation with
repetition of jobs.

This is the per-instance search method of the paper's budget comparison
(Section 6.5). It follows the design of the genetic algorithm published
for the IJSP (permutation with repetition, job-based order crossover,
tournament selection, elitism, lexicographic ranking of interval
makespans) and runs on the same decoder and evaluator as the evolved
rules (``simulate.py``). A run stops after a number of schedule
constructions or after a time limit, and records its incumbent solution
at the requested numbers of constructions; with the article's grid,
every time that number grows by a factor of 2^(1/4).

Usage from the ``code/`` directory:

    python -m ijsp_gp.ga --instance ../instances/interval_taillard/int__tai15_15_01.txt \\
        --seconds 30 --seed 1
"""

import argparse
import random
import time
from typing import List, Optional

from .simulate import Instance, better, decode

# the article's recording grid: every 2^(1/4)-fold increase, up to 2^30
GRID = sorted({round(2 ** (k / 4)) for k in range(0, 121)})


def random_permutation(inst: Instance, rng: random.Random) -> List[int]:
    perm = [j for j in range(inst.n) for _ in range(inst.m)]
    rng.shuffle(perm)
    return perm


def job_order_crossover(p1: List[int], p2: List[int], n: int,
                        rng: random.Random) -> List[int]:
    """A random subset of jobs keeps its positions from the first parent;
    the remaining positions are filled in the order of the second."""
    keep = [rng.random() < 0.5 for _ in range(n)]
    rest = iter([j for j in p2 if not keep[j]])
    return [j if keep[j] else next(rest) for j in p1]


def swap_mutation(perm: List[int], rng: random.Random) -> None:
    """Swap two positions: any permutation with repetition is feasible, so
    no repair is needed."""
    i, j = rng.randrange(len(perm)), rng.randrange(len(perm))
    perm[i], perm[j] = perm[j], perm[i]


def evolve(inst: Instance, budget: int, rng: random.Random, pop: int = 250,
           tournament: int = 3, p_crossover: float = 0.9,
           p_mutation: float = 0.2, elite: int = 2,
           seed_perm: Optional[List[int]] = None,
           checkpoints: Optional[List[int]] = None,
           time_limit: Optional[float] = None):
    """Run the GA until ``budget`` schedule constructions or, if given,
    ``time_limit`` seconds.

    Returns ({constructions: (incumbent makespan, seconds)}, incumbent
    makespan). One run yields the whole quality-budget curve at the
    requested ``checkpoints``. Stopped by time, the curve ends at the last
    checkpoint reached plus a final point at the constructions made.
    ``seed_perm`` places one given permutation, such as the one an
    evolved rule builds, in the initial population.
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

    def exhausted():
        return used >= budget or (
            time_limit is not None and time.time() - t0 >= time_limit)

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
        if exhausted():
            break

    while not exhausted():
        scored.sort(key=lambda x: (x[0][1], x[0][0]))
        new = scored[:elite]
        while len(new) < pop and not exhausted():
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

    if time_limit is not None:       # stopped by time: the last real point
        curve[used] = (best_cm, time.time() - t0)
        return curve, best_cm
    for p in points:                 # if the budget ended first
        curve[p] = (best_cm, time.time() - t0)
    return curve, best_cm


def random_search(inst: Instance, budget: int, rng: random.Random,
                  checkpoints: Optional[List[int]] = None,
                  time_limit: Optional[float] = None):
    """Uniformly sampled permutations on the same decoder: the floor any
    search method is measured against. Stops like ``evolve``."""
    points = sorted(checkpoints or [budget])
    t0 = time.time()
    curve, best_cm = {}, None
    for k in range(1, budget + 1):
        cm = decode(inst, random_permutation(inst, rng))
        if best_cm is None or better(cm, best_cm):
            best_cm = cm
        while points and k >= points[0]:
            curve[points.pop(0)] = (best_cm, time.time() - t0)
        if time_limit is not None and time.time() - t0 >= time_limit:
            curve[k] = (best_cm, time.time() - t0)
            return curve, best_cm
    for p in points:
        curve[p] = (best_cm, time.time() - t0)
    return curve, best_cm


def main():
    from .instances import lb_for_instance_name, load_instance
    import os

    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--instance", required=True)
    ap.add_argument("--seconds", type=float, default=30.0,
                    help="time limit per run")
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()

    name = os.path.splitext(os.path.basename(args.instance))[0]
    inst = Instance(load_instance(args.instance, name))
    lb = lb_for_instance_name(name)
    curve, _ = evolve(inst, GRID[-1], random.Random(args.seed),
                      checkpoints=list(GRID), time_limit=args.seconds)
    for p in sorted(curve):
        if p & (p - 1) and p != max(curve):
            continue                 # print powers of two and the last point
        (lo, up), sec = curve[p]
        re_pct = ((lo + up) / 2 - lb) / lb * 100 if lb else float("nan")
        print(f"{p:>9} constructions  [{lo:.0f}, {up:.0f}]  "
              f"RE {re_pct:6.2f}  {sec:7.2f} s")


if __name__ == "__main__":
    main()
