"""RE y ancho POR REGLA del barrido de lambda SIN los terminales de anchura.

Contrapartida de lambda_per_rule.py para el brazo ablacionado, cuyo barrido
(benchmarks/lambda_nowidth/) es el paso 2 de la cadena de pendientes. Sirve
para contrastar la afirmacion de 7.2 de que el brazo sin anchuras no traza una
frontera comparable: hasta ahora eso se sostenia con dos puntos (los objetivos
makespan y robusto lambda=1 del 2x2), no con un barrido.

Ojo con lambda=0: en f_lambda = Cmax_sup + lambda*(Cmax_sup - Cmax_inf) da el
peor caso puro, que NO es el punto medio que optimiza el brazo de makespan. Son
brazos distintos y no se deben mezclar.

Toma los lambda que esten completos y avisa de los que no, de modo que un
barrido a medias no se lea como uno terminado.

Salida: benchmarks/lambda_nowidth_por_regla.csv (no sobrescribe)
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

BRAZOS = [("0.0", "benchmarks/lambda_nowidth/nw_lam0p0_seed*.json"),
          ("0.5", "benchmarks/lambda_nowidth/nw_lam0p5_seed*.json"),
          ("2.0", "benchmarks/lambda_nowidth/nw_lam2p0_seed*.json"),
          ("4.0", "benchmarks/lambda_nowidth/nw_lam4p0_seed*.json")]
COMPLETO = 10  # semillas por lambda cuando el brazo termina


def evalua(tree, insts):
    """RE medio y ancho relativo medio de una regla sobre las instancias."""
    res, wid = [], []
    h = GPRuleHeuristic(tree)
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
        # makespan componente a componente: max de los inferiores y max de los
        # superiores por separado, nunca un max lexicografico sobre intervalos
        lo = max(x.lower if isinstance(x, Interval) else x for x in c)
        up = max(x.upper if isinstance(x, Interval) else x for x in c)
        res.append(((lo + up) / 2 - lb) / lb * 100)
        wid.append((up - lo) / ((up + lo) / 2) * 100)
    return sum(res) / len(res), sum(wid) / len(wid)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="benchmarks/lambda_nowidth_por_regla.csv")
    a = ap.parse_args()
    if os.path.exists(a.out):
        sys.exit(f"{a.out} ya existe; borralo a mano para recalcular")

    insts = [p for p in sorted(PROBLEM_REGISTRY)
             if re.match(r"int__tai\d+_\d+_\d+$", p)
             and lb_for_problem_name(p) is not None]
    print(f"{len(insts)} instancias", flush=True)

    filas, parciales = [], []
    for lam, pat in BRAZOS:
        fs = sorted(glob.glob(pat))
        if not fs:
            print(f"lambda={lam}: sin datos, se omite", flush=True)
            continue
        if len(fs) < COMPLETO:
            parciales.append((lam, len(fs)))
        for f in fs:
            d = json.load(open(f, encoding="utf-8"))
            re_, wid = evalua(d["tree"], insts)
            filas.append({"lam": lam, "seed": d["seed"],
                          "re": round(re_, 4), "ancho": round(wid, 4)})
            print(".", end="", flush=True)
        print(f" lambda={lam} ({len(fs)}/{COMPLETO})", flush=True)

    with open(a.out, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["lam", "seed", "re", "ancho"])
        w.writeheader()
        w.writerows(filas)
    print(f"\n{len(filas)} reglas -> {a.out}")
    for lam, n in parciales:
        print(f"AVISO: lambda={lam} esta a {n}/{COMPLETO} semillas; "
              f"no usar su media como si el brazo estuviera completo")


if __name__ == "__main__":
    main()
