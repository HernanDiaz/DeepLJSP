"""
Tiempo medio de construccion de un schedule, por metodo, sobre las 70
instancias. Se cronometra el pase constructivo completo (todas las decisiones
de despacho de una instancia), repitiendolo REPEATS veces por instancia.

Nota: los valores absolutos dependen de la maquina, de su carga y de que la
implementacion es Python de investigacion; lo informativo es la comparacion
relativa entre metodos, todos medidos en la misma pasada.
"""

import argparse
import json
import random
import re
import sys
import time

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data import PROBLEM_REGISTRY
from jobshop_rl.data.literature_bounds import lb_for_problem_name
from jobshop_rl.experiments.factory import EnvironmentFactory
from jobshop_rl.heuristics.gp_rule import GPRuleHeuristic
from jobshop_rl.heuristics.strategies import (
    SPTHeuristic, LPTHeuristic, MORHeuristic, MWKRHeuristic,
    ESTHeuristic, CRHeuristic, GTHeuristic,
)

REPEATS = 5


def build_once(env, h, rnd=None):
    st = env.reset()
    done = False
    while not done and st["eligible_ops"]:
        if rnd is not None:
            a = rnd.randrange(len(st["eligible_ops"]))
        else:
            f = env.get_features(st)
            a = min(h.select_action(st["eligible_ops"], f),
                    len(st["eligible_ops"]) - 1)
        st, _, done, _ = env.step(a)


def main():
    # la regla destacada de la campana tuneada; se parametriza para que no
    # quede fijada a la de una campana anterior
    ap = argparse.ArgumentParser()
    ap.add_argument("--rule",
                    default="benchmarks/reevo_fixedfit/gp_tuned_seed1.json")
    ap.add_argument("--out", default="benchmarks/timing_tuned.csv")
    args = ap.parse_args()

    gp = GPRuleHeuristic(json.load(open(args.rule, encoding="utf-8"))["tree"])
    methods = [("SPT", SPTHeuristic()), ("LPT", LPTHeuristic()),
               ("EST", ESTHeuristic()), ("CR", CRHeuristic()),
               ("MWKR", MWKRHeuristic()), ("MOR", MORHeuristic()),
               ("G&T-SPT", GTHeuristic(tiebreak="spt")),
               ("G&T-MWKR", GTHeuristic(tiebreak="mwkr")),
               ("GP rule", gp), ("Random", None)]
    insts = [p for p in sorted(PROBLEM_REGISTRY)
             if re.match(r"int__tai\d+_\d+_\d+$", p)
             and lb_for_problem_name(p) is not None]

    ms = {n: [] for n, _ in methods}
    for pid in insts:
        prob = PROBLEM_REGISTRY[pid]()
        for name, h in methods:
            env = EnvironmentFactory.create_from_problem(prob, "basic", seed=0)
            rnd = random.Random(0) if name == "Random" else None
            t0 = time.perf_counter()
            for _ in range(REPEATS):
                build_once(env, h, rnd)
            ms[name].append((time.perf_counter() - t0) / REPEATS * 1000)
        print(".", end="", flush=True)
    print()

    print(f"\n=== Tiempo por schedule (ms), media sobre {len(insts)} instancias ===")
    print(f"{'metodo':<11}{'media':>9}{'min':>9}{'max':>9}")
    for name, _ in methods:
        v = ms[name]
        print(f"{name:<11}{sum(v)/len(v):>9.0f}{min(v):>9.0f}{max(v):>9.0f}")
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("method,mean_ms,min_ms,max_ms\n")
        for name, _ in methods:
            v = ms[name]
            f.write(f"{name},{sum(v)/len(v):.1f},{min(v):.1f},{max(v):.1f}\n")
    print(f"\nCSV: {args.out}")


if __name__ == "__main__":
    main()
