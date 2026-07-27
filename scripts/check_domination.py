"""
Comprueba, instancia a instancia, en cuantas de las 70 la mejor regla GP gana
a CADA baseline. Necesario para poder afirmar (o no) que domina a todas las
reglas probadas, no solo a las dos usadas en los tests.
"""

import json
import re
import sys

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
from jobshop_rl.models.interval import Interval, final_makespan

RULE = "benchmarks/reevo_fixedfit/gp_rule_seed27.json"


def re_of(env, h, lb):
    st = env.reset()
    done = False
    while not done and st["eligible_ops"]:
        f = env.get_features(st)
        a = min(h.select_action(st["eligible_ops"], f),
                len(st["eligible_ops"]) - 1)
        st, _, done, _ = env.step(a)
    m = final_makespan(env.job_completion_time)
    mid = m.midpoint if isinstance(m, Interval) else float(m)
    return (mid - lb) / lb * 100


def main():
    gp = GPRuleHeuristic(json.load(open(RULE, encoding="utf-8"))["tree"])
    base = [("SPT", SPTHeuristic()), ("LPT", LPTHeuristic()),
            ("EST", ESTHeuristic()), ("CR", CRHeuristic()),
            ("MWKR", MWKRHeuristic()), ("MOR", MORHeuristic()),
            ("G&T-SPT", GTHeuristic(tiebreak="spt")),
            ("G&T-MWKR", GTHeuristic(tiebreak="mwkr"))]
    insts = [p for p in sorted(PROBLEM_REGISTRY)
             if re.match(r"int__tai\d+_\d+_\d+$", p)]

    wins = {n: 0 for n, _ in base}
    closest = {n: (1e9, None) for n, _ in base}   # menor margen a favor del GP
    total = 0
    for pid in insts:
        lb = lb_for_problem_name(pid)
        if lb is None:
            continue
        total += 1
        env = EnvironmentFactory.create_from_problem(
            PROBLEM_REGISTRY[pid](), "basic", seed=0)
        g = re_of(env, gp, lb)
        for name, h in base:
            env = EnvironmentFactory.create_from_problem(
                PROBLEM_REGISTRY[pid](), "basic", seed=0)
            b = re_of(env, h, lb)
            if g < b:
                wins[name] += 1
            if b - g < closest[name][0]:
                closest[name] = (b - g, pid)
        print(".", end="", flush=True)
    print()

    print(f"\n=== La mejor regla GP frente a cada baseline ({total} instancias) ===")
    print(f"{'baseline':<10}{'gana en':>10}{'margen minimo (pts)':>22}  instancia")
    for name, _ in base:
        d, pid = closest[name]
        print(f"{name:<10}{f'{wins[name]}/{total}':>10}{d:>22.2f}  {pid}")
    allwin = all(wins[n] == total for n, _ in base)
    print(f"\n=> {'DOMINA a todas en TODAS las instancias' if allwin else 'NO domina en todas'}")


if __name__ == "__main__":
    main()
