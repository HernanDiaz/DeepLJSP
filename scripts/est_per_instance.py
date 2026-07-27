"""RE por instancia de EST, la mejor de las reglas simples (42.3% frente al
45.5% de MOR), para la tabla del apendice.

constructive_per_instance.csv solo trae MOR, G&T-MWKR y GP; este script anade
EST en un fichero aparte, sin tocar el anterior.

Salida: benchmarks/est_per_instance.csv
Uso: python scripts/est_per_instance.py
"""

import csv
import os
import re
import sys

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data import PROBLEM_REGISTRY                       # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory      # noqa: E402
from jobshop_rl.heuristics.strategies import ESTHeuristic          # noqa: E402
from jobshop_rl.models.interval import Interval, final_makespan    # noqa: E402

OUT = "benchmarks/est_per_instance.csv"
BASE = {(15, 15): 0, (20, 15): 10, (20, 20): 20, (30, 15): 30,
        (30, 20): 40, (50, 15): 50, (50, 20): 60}


def ta_index(inst):
    m = re.search(r"tai(\d+)_(\d+)_(\d+)", inst)
    return BASE[(int(m.group(1)), int(m.group(2)))] + int(m.group(3))


def main():
    if os.path.exists(OUT):
        sys.exit(f"{OUT} ya existe; borralo a mano si quieres recalcularlo")

    insts = sorted(p for p in PROBLEM_REGISTRY
                   if re.match(r"int__tai\d+_\d+_\d+$", p))
    h = ESTHeuristic()
    rows = []
    for pid in insts:
        lb = lb_for_problem_name(pid)
        if lb is None:
            continue
        env = EnvironmentFactory.create_from_problem(
            PROBLEM_REGISTRY[pid](), "basic", seed=0)
        st = env.reset()
        done = False
        while not done and st["eligible_ops"]:
            f = env.get_features(st)
            a = min(h.select_action(st["eligible_ops"], f),
                    len(st["eligible_ops"]) - 1)
            st, _, done, _ = env.step(a)
        m = final_makespan(env.job_completion_time)
        mid = m.midpoint if isinstance(m, Interval) else float(m)
        rows.append({"ta": f"TA{ta_index(pid)}", "instance": pid,
                     "lb": lb, "est_re": round((mid - lb) / lb * 100, 4)})
        print(".", end="", flush=True)
    print()

    rows.sort(key=lambda r: int(r["ta"][2:]))
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["ta", "instance", "lb", "est_re"])
        w.writeheader()
        w.writerows(rows)
    mu = sum(r["est_re"] for r in rows) / len(rows)
    print(f"{len(rows)} instancias -> {OUT}   RE medio {mu:.1f}")


if __name__ == "__main__":
    main()
