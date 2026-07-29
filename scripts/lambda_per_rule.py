"""RE y ancho POR REGLA de los brazos del barrido de lambda.

ablation_por_regla.csv cubre el 2x2 (makespan/robusto x con/sin anchura), pero
no los lambda intermedios. Esto completa 0.5, 2 y 4 para poder dibujar como se
recorre la frontera al crecer lambda, no solo sus medias.

Salida: benchmarks/lambda_por_regla.csv
"""

import argparse
import csv
import glob
import json
import os
import re
import sys

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data import PROBLEM_REGISTRY                       # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory      # noqa: E402
from jobshop_rl.heuristics.gp_rule import GPRuleHeuristic          # noqa: E402
from jobshop_rl.models.interval import Interval                    # noqa: E402

BRAZOS = [("0.5", "benchmarks/tuned/lambda/lam0p5_seed*.json"),
          ("2.0", "benchmarks/tuned/lambda/lam2p0_seed*.json"),
          ("4.0", "benchmarks/tuned/lambda/lam4p0_seed*.json")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="benchmarks/lambda_por_regla.csv")
    a = ap.parse_args()
    if os.path.exists(a.out):
        sys.exit(f"{a.out} ya existe; borralo a mano para recalcular")

    insts = [p for p in sorted(PROBLEM_REGISTRY)
             if re.match(r"int__tai\d+_\d+_\d+$", p)
             and lb_for_problem_name(p) is not None]

    filas = []
    for lam, pat in BRAZOS:
        for f in sorted(glob.glob(pat)):
            d = json.load(open(f, encoding="utf-8"))
            h = GPRuleHeuristic(d["tree"])
            res, wid = [], []
            for pid in insts:
                lb = lb_for_problem_name(pid)
                env = EnvironmentFactory.create_from_problem(
                    PROBLEM_REGISTRY[pid](), "basic", seed=0)
                st = env.reset(); done = False
                while not done and st["eligible_ops"]:
                    fe = env.get_features(st)
                    k = min(h.select_action(st["eligible_ops"], fe),
                            len(st["eligible_ops"]) - 1)
                    st, _, done, _ = env.step(k)
                c = env.job_completion_time
                lo = max(x.lower if isinstance(x, Interval) else x for x in c)
                up = max(x.upper if isinstance(x, Interval) else x for x in c)
                res.append(((lo + up) / 2 - lb) / lb * 100)
                wid.append((up - lo) / ((up + lo) / 2) * 100)
            filas.append({"lam": lam, "seed": d["seed"],
                          "re": round(sum(res) / len(res), 4),
                          "ancho": round(sum(wid) / len(wid), 4)})
            print(".", end="", flush=True)
        print(f" lambda={lam}", flush=True)

    with open(a.out, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["lam", "seed", "re", "ancho"])
        w.writeheader(); w.writerows(filas)
    print(f"\n{len(filas)} reglas -> {a.out}")


if __name__ == "__main__":
    main()
