"""Sensibilidad de la regla destacada a sus dos coeficientes.

La regla simplificada es  SLACK^2 + 2*PT - WKR - 1*WKRW - 1  (identidad
verificada contra el arbol en las 37.250 decisiones del benchmark). Se barre
cada coeficiente dejando el otro en su valor evolucionado:

    alpha: peso de PT    (evolucionado: 2)
    beta : peso de WKRW  (evolucionado: 1; beta=0 = ablacion en despliegue)

y se evalua RE medio sobre las 70 instancias. Analogo a la Fig. 13 de
Gil-Gala et al. (2025), que barre la constante numerica de la regla final.

Salida: benchmarks/coefficient_sweep.csv
"""

import csv
import os
import re
import sys

import numpy as np

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data import PROBLEM_REGISTRY                       # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory      # noqa: E402
from jobshop_rl.heuristics.gp_rule import terminal_arrays          # noqa: E402
from jobshop_rl.models.interval import Interval, final_makespan    # noqa: E402

OUT = "benchmarks/coefficient_sweep.csv"
INSTS = [p for p in sorted(PROBLEM_REGISTRY)
         if re.match(r"int__tai\d+_\d+_\d+$", p)
         and lb_for_problem_name(p) is not None]


def re_of(alpha, beta):
    vals = []
    for pid in INSTS:
        lb = lb_for_problem_name(pid)
        env = EnvironmentFactory.create_from_problem(
            PROBLEM_REGISTRY[pid](), "basic", seed=0)
        st = env.reset(); done = False
        while not done and st["eligible_ops"]:
            t = terminal_arrays(env.get_features(st))
            pri = (t["SLACK"] ** 2 + alpha * t["PT"] - t["WKR"]
                   - beta * t["WKRW"])
            a = int(np.argmin(pri))
            st, _, done, _ = env.step(a)
        m = final_makespan(env.job_completion_time)
        mid = m.midpoint if isinstance(m, Interval) else float(m)
        vals.append((mid - lb) / lb * 100)
    return sum(vals) / len(vals)


def main():
    if os.path.exists(OUT):
        sys.exit(f"{OUT} ya existe; borralo a mano para recalcular")

    rows = []
    # alpha: peso de PT, evolucionado 2 (beta fijo en 1)
    for a in [x / 4 for x in range(0, 21)]:          # 0 .. 5
        r = re_of(a, 1.0)
        rows.append({"coef": "alpha_PT", "value": a, "re": round(r, 4)})
        print(f"alpha={a:<5} RE={r:.2f}", flush=True)
    # beta: peso de WKRW, evolucionado 1 (alpha fijo en 2); beta=0 lo apaga
    for b in [x / 4 for x in range(-4, 13)]:         # -1 .. 3
        r = re_of(2.0, b)
        rows.append({"coef": "beta_WKRW", "value": b, "re": round(r, 4)})
        print(f"beta={b:<5} RE={r:.2f}", flush=True)

    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["coef", "value", "re"])
        w.writeheader(); w.writerows(rows)
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
