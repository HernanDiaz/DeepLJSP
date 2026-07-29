"""Tiempo medio de un pase constructivo para las 30 reglas del brazo.

time_baselines.py cronometra una regla por metodo; aqui se cronometran las 30
reglas evolucionadas, para poder dar el tiempo de la fila 'mean of 30' de
tab:baselines con el mismo protocolo que el resto: 70 instancias, REPEATS
repeticiones cada una.

Salida: benchmarks/timing_gp_arm.csv (una fila por regla)
"""

import argparse
import csv
import glob
import json
import os
import re
import sys
import time

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data import PROBLEM_REGISTRY                       # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory      # noqa: E402
from jobshop_rl.heuristics.gp_rule import GPRuleHeuristic          # noqa: E402
from jobshop_rl.models.interval import final_makespan              # noqa: E402

REPEATS = 5      # mismo valor que time_baselines.py


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pattern",
                    default="benchmarks/reevo_fixedfit/gp_tuned_seed*.json")
    ap.add_argument("--out", default="benchmarks/timing_gp_arm.csv")
    args = ap.parse_args()
    if os.path.exists(args.out):
        sys.exit(f"{args.out} ya existe; borralo a mano para recalcular")

    insts = [p for p in sorted(PROBLEM_REGISTRY)
             if re.match(r"int__tai\d+_\d+_\d+$", p)
             and lb_for_problem_name(p) is not None]
    probs = {p: PROBLEM_REGISTRY[p]() for p in insts}

    rows = []
    for f in sorted(glob.glob(args.pattern)):
        h = GPRuleHeuristic(json.load(open(f, encoding="utf-8"))["tree"])
        per_inst = []
        for pid in insts:
            t0 = time.perf_counter()
            for _ in range(REPEATS):
                env = EnvironmentFactory.create_from_problem(
                    probs[pid], "basic", seed=0)
                st = env.reset(); done = False
                while not done and st["eligible_ops"]:
                    fe = env.get_features(st)
                    a = min(h.select_action(st["eligible_ops"], fe),
                            len(st["eligible_ops"]) - 1)
                    st, _, done, _ = env.step(a)
                final_makespan(env.job_completion_time)
            per_inst.append((time.perf_counter() - t0) / REPEATS * 1000)
        ms = sum(per_inst) / len(per_inst)
        rows.append({"rule": os.path.basename(f)[:-5], "mean_ms": round(ms, 1)})
        print(f"{rows[-1]['rule']}: {ms:.0f} ms", flush=True)

    with open(args.out, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["rule", "mean_ms"])
        w.writeheader(); w.writerows(rows)

    v = [r["mean_ms"] for r in rows]
    n = len(v); mu = sum(v) / n
    sd = (sum((x - mu) ** 2 for x in v) / (n - 1)) ** 0.5
    print(f"\n{n} reglas: {mu:.0f} ms de media (sd {sd:.0f}, "
          f"rango {min(v):.0f}-{max(v):.0f}) -> {args.out}")


if __name__ == "__main__":
    main()
