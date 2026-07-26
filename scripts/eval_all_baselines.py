"""
Evalua TODAS las reglas de despacho implementadas sobre las 70 instancias
Taillard de intervalo, para la tabla de baselines del paper (hasta ahora solo
se reportaba MOR, la mejor).

Reglas fijas: SPT, LPT, MOR, MWKR, EST, CR (critical ratio).
Generador activo de Giffler & Thompson con desempate SPT y MWKR.
Referencia: la mejor regla GP evolucionada (seed27).

Salida: benchmarks/all_baselines.csv + tabla por clase y global.
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

CLASSES = ["15_15", "20_15", "20_20", "30_15", "30_20", "50_15", "50_20"]


def rollout_re(env, h, lb):
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


def stats(v):
    n = len(v); mu = sum(v) / n
    sd = (sum((x - mu) ** 2 for x in v) / (n - 1)) ** 0.5 if n > 1 else 0.0
    return mu, sd


def main():
    methods = [
        ("SPT", SPTHeuristic()),
        ("LPT", LPTHeuristic()),
        ("EST", ESTHeuristic()),
        ("CR", CRHeuristic()),
        ("MWKR", MWKRHeuristic()),
        ("MOR", MORHeuristic()),
        ("G&T-SPT", GTHeuristic(tiebreak="spt")),
        ("G&T-MWKR", GTHeuristic(tiebreak="mwkr")),
        ("GP (best)", GPRuleHeuristic(json.load(open(
            "benchmarks/reevo_fixedfit/gp_rule_seed27.json",
            encoding="utf-8"))["tree"])),
    ]
    instances = [p for p in sorted(PROBLEM_REGISTRY)
                 if re.match(r"int__tai\d+_\d+_\d+$", p)]

    rows = []
    for name, h in methods:
        per_cls = {c: [] for c in CLASSES}
        allv = []
        for pid in instances:
            lb = lb_for_problem_name(pid)
            if lb is None:
                continue
            env = EnvironmentFactory.create_from_problem(
                PROBLEM_REGISTRY[pid](), "basic", seed=0)
            v = rollout_re(env, h, lb)
            per_cls[re.search(r"tai(\d+_\d+)", pid).group(1)].append(v)
            allv.append(v)
        rows.append((name, per_cls, allv))
        print(f"{name}: {sum(allv)/len(allv):.1f}%", flush=True)

    with open("benchmarks/all_baselines.csv", "w", encoding="utf-8") as f:
        f.write("method," + ",".join(CLASSES) + ",all,sd\n")
        for name, per_cls, allv in rows:
            mu, sd = stats(allv)
            f.write(f"{name}," + ",".join(
                f"{sum(per_cls[c])/len(per_cls[c]):.2f}" for c in CLASSES)
                + f",{mu:.2f},{sd:.2f}\n")

    print("\n=== RE (%) por clase, un pase constructivo determinista ===")
    hdr = f"{'method':<11}" + "".join(f"{c:>8}" for c in CLASSES) + f"{'ALL':>8}"
    print(hdr)
    for name, per_cls, allv in rows:
        line = f"{name:<11}" + "".join(
            f"{sum(per_cls[c])/len(per_cls[c]):>8.1f}" for c in CLASSES)
        print(line + f"{sum(allv)/len(allv):>8.1f}")
    print("\nCSV: benchmarks/all_baselines.csv")


if __name__ == "__main__":
    main()
