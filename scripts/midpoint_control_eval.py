"""Evalua las 30 reglas del control del punto medio sobre las 70 intervalares.

Contrapartida de lambda_nowidth_per_rule.py para el control: las reglas se
evolucionaron sobre las instancias CRISP (escenario del punto medio) y aqui se
despliegan sobre el benchmark intervalar con el mismo decodificador que todo lo
demas. RE y ancho relativo por regla.

El brazo de comparacion es el ablacionado entrenado sobre intervalos
(mismas semillas 1-30, mismos terminales sin anchura): la unica diferencia
entre ambos es la aritmetica del fitness durante la evolucion.

Salida: benchmarks/midpoint_control_por_regla.csv (no sobrescribe)
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pattern",
                    default="benchmarks/midpoint_control/mid_seed*.json")
    ap.add_argument("--out",
                    default="benchmarks/midpoint_control_por_regla.csv")
    a = ap.parse_args()
    if os.path.exists(a.out):
        sys.exit(f"{a.out} ya existe; borralo a mano para recalcular")

    insts = [p for p in sorted(PROBLEM_REGISTRY)
             if re.match(r"int__tai\d+_\d+_\d+$", p)
             and lb_for_problem_name(p) is not None]
    print(f"{len(insts)} instancias intervalares", flush=True)

    filas = []
    for f in sorted(glob.glob(a.pattern),
                    key=lambda p: int(re.search(r"seed(\d+)", p).group(1))):
        d = json.load(open(f, encoding="utf-8"))
        h = GPRuleHeuristic(d["tree"])
        res, wid = [], []
        for pid in insts:
            lb = lb_for_problem_name(pid)
            env = EnvironmentFactory.create_from_problem(
                PROBLEM_REGISTRY[pid](), "basic", seed=0)
            st = env.reset()
            done = False
            while not done and st["eligible_ops"]:
                fe = env.get_features(st)
                k = min(h.select_action(st["eligible_ops"], fe),
                        len(st["eligible_ops"]) - 1)
                st, _, done, _ = env.step(k)
            c = env.job_completion_time
            # makespan componente a componente, nunca max lexicografico
            lo = max(x.lower if isinstance(x, Interval) else x for x in c)
            up = max(x.upper if isinstance(x, Interval) else x for x in c)
            res.append(((lo + up) / 2 - lb) / lb * 100)
            wid.append((up - lo) / ((up + lo) / 2) * 100)
        filas.append({"seed": d["seed"],
                      "re": round(sum(res) / len(res), 4),
                      "ancho": round(sum(wid) / len(wid), 4)})
        print(".", end="", flush=True)

    with open(a.out, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["seed", "re", "ancho"])
        w.writeheader()
        w.writerows(filas)
    print(f"\n{len(filas)} reglas -> {a.out}")


if __name__ == "__main__":
    main()
