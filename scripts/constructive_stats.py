"""
Comparación de métodos CONSTRUCTIVOS con rigor estadístico y de runtime.

Por instancia (70 Taillard intervalo): RE (E[C_max] vs LB crisp) y tiempo de
construcción de cada método determinista (MOR, G&T-MWKR, regla GP). Añade:
  - media±(sd entre instancias) de RE y tiempo por método,
  - Wilcoxon signed-rank pareado GP-vs-baseline sobre el RE por instancia,
  - tabla por instancia para el apéndice (benchmarks/constructive_per_instance.csv).

Los métodos son deterministas -> un rollout por instancia. El tiempo se mide
promediando REPEATS construcciones (milisegundos), para respaldar la
afirmación de "coste negligible" con números.

Uso: python scripts/constructive_stats.py [--rule benchmarks/gp_rule_seed1.json]
"""

import argparse
import json
import re
import sys
import time

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data import PROBLEM_REGISTRY                       # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name, ta_name  # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory     # noqa: E402
from jobshop_rl.heuristics.gp_rule import GPRuleHeuristic          # noqa: E402
from jobshop_rl.heuristics.strategies import MORHeuristic, GTHeuristic  # noqa: E402
from jobshop_rl.models.interval import Interval, final_makespan    # noqa: E402

REPEATS = 20   # repeticiones para cronometrar la construcción


def rollout_re_timed(env, heuristic, lb):
    """(RE por midpoint, tiempo medio de construcción en ms)."""
    # cronometrar REPEATS construcciones
    t0 = time.perf_counter()
    for _ in range(REPEATS):
        state = env.reset()
        done = False
        while not done and state["eligible_ops"]:
            f = env.get_features(state)
            a = min(heuristic.select_action(state["eligible_ops"], f),
                    len(state["eligible_ops"]) - 1)
            state, _, done, _ = env.step(a)
    ms = (time.perf_counter() - t0) / REPEATS * 1000.0
    m = final_makespan(env.job_completion_time)
    mid = m.midpoint if isinstance(m, Interval) else float(m)
    return (mid - lb) / lb * 100.0, ms


def stats(v):
    n = len(v); mu = sum(v) / n
    sd = (sum((x - mu) ** 2 for x in v) / (n - 1)) ** 0.5 if n > 1 else 0.0
    return mu, sd


def wilcoxon(pairs):
    """Wilcoxon signed-rank pareado (aprox. normal). -> (W+, z, n_efectivo)."""
    diffs = [a - b for a, b in pairs if abs(a - b) > 1e-12]
    n = len(diffs)
    if n < 6:
        return float("nan"), float("nan"), n
    ranked = sorted(diffs, key=lambda d: abs(d))
    ranks = {}; i = 0
    while i < n:
        j = i
        while j + 1 < n and abs(abs(ranked[j + 1]) - abs(ranked[i])) < 1e-12:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[id(ranked[k])] = r
        i = j + 1
    w = sum(ranks[id(d)] for d in ranked if d > 0)
    mu = n * (n + 1) / 4
    sd = (n * (n + 1) * (2 * n + 1) / 24) ** 0.5
    return w, (w - mu) / sd if sd else float("nan"), n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rule", default="benchmarks/gp_rule_seed1.json")
    args = ap.parse_args()
    gp = GPRuleHeuristic(json.load(open(args.rule))["tree"])
    methods = {"MOR": MORHeuristic(), "GT-MWKR": GTHeuristic(tiebreak="mwkr"),
               "GP": gp}

    instances = [p for p in sorted(PROBLEM_REGISTRY)
                 if re.match(r"int__tai\d+_\d+_\d+$", p)]
    rows = []
    for pid in instances:
        lb = lb_for_problem_name(pid)
        if lb is None:
            continue
        m = re.search(r"tai(\d+)_(\d+)_(\d+)", pid)
        rec = {"instance": pid, "ta": ta_name(*(int(g) for g in m.groups())),
               "cls": f"{m.group(1)}_{m.group(2)}", "lb": lb}
        for name, h in methods.items():
            env = EnvironmentFactory.create_from_problem(
                PROBLEM_REGISTRY[pid](), "basic", seed=0)
            re_v, ms = rollout_re_timed(env, h, lb)
            rec[f"{name}_re"] = re_v
            rec[f"{name}_ms"] = ms
        rows.append(rec)
        print(".", end="", flush=True)
    print()

    # Tabla por instancia (apéndice)
    with open("benchmarks/constructive_per_instance.csv", "w", encoding="utf-8") as f:
        cols = ["ta", "cls", "lb"] + [f"{m}_{s}" for m in methods
                                      for s in ("re", "ms")]
        f.write(",".join(cols) + "\n")
        for r in rows:
            f.write(",".join([r["ta"], r["cls"], str(r["lb"])] +
                             [f"{r[f'{m}_{s}']:.3f}" for m in methods
                              for s in ("re", "ms")]) + "\n")

    # Resumen global
    print("\n=== RE y tiempo de construcción (media±sd entre 70 instancias) ===")
    print(f"{'método':<10}{'RE (%)':>16}{'tiempo (ms)':>16}")
    for name in methods:
        mu_re, sd_re = stats([r[f"{name}_re"] for r in rows])
        mu_ms, sd_ms = stats([r[f"{name}_ms"] for r in rows])
        print(f"{name:<10}{f'{mu_re:.2f} ± {sd_re:.2f}':>16}"
              f"{f'{mu_ms:.2f} ± {sd_ms:.2f}':>16}")

    print("\n=== Wilcoxon signed-rank pareado sobre el RE por instancia ===")
    for base in ("MOR", "GT-MWKR"):
        pairs = [(r["GP_re"], r[f"{base}_re"]) for r in rows]
        w, z, n = wilcoxon(pairs)
        wins = sum(1 for a, b in pairs if a < b)
        print(f"  GP vs {base:<8}: GP mejor en {wins}/{len(pairs)} | "
              f"W+={w:.0f}, z={z:.2f}  "
              f"({'significativo' if abs(z) > 1.96 else 'no sig.'} al 5%)")

    print("\nTabla por instancia: benchmarks/constructive_per_instance.csv")


if __name__ == "__main__":
    main()
