"""Ancho del intervalo POR REGLA en los cuatro brazos del diseno 2x2 de 7.2.

La campana guardo solo las medias de brazo, asi que la interaccion del 2x2
(el objetivo robusto rinde mas cuando los terminales de anchura estan
disponibles) solo puede verse en las medias, no contrastarse. Con el ancho por
regla y semilla se puede hacer el test de diferencia-de-diferencias.

Salida: benchmarks/ablation_por_regla.csv con columnas
        objetivo, terminales, seed, re, ancho
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

BRAZOS = [
    ("makespan", "full", "benchmarks/reevo_fixedfit/gp_tuned_seed*.json"),
    ("makespan", "nowidth", "benchmarks/tuned/ablation/nowidth_seed*.json"),
    ("robust", "full", "benchmarks/tuned/robust/width_seed*.json"),
    ("robust", "nowidth", "benchmarks/tuned/robust/nowidth_seed*.json"),
]


def evalua(tree, insts):
    h = GPRuleHeuristic(tree)
    res, wid = [], []
    for pid in insts:
        lb = lb_for_problem_name(pid)
        env = EnvironmentFactory.create_from_problem(
            PROBLEM_REGISTRY[pid](), "basic", seed=0)
        st = env.reset(); done = False
        while not done and st["eligible_ops"]:
            f = env.get_features(st)
            a = min(h.select_action(st["eligible_ops"], f),
                    len(st["eligible_ops"]) - 1)
            st, _, done, _ = env.step(a)
        c = env.job_completion_time
        lo = max(x.lower if isinstance(x, Interval) else x for x in c)
        up = max(x.upper if isinstance(x, Interval) else x for x in c)
        res.append(((lo + up) / 2 - lb) / lb * 100)
        wid.append((up - lo) / ((up + lo) / 2) * 100)
    return sum(res) / len(res), sum(wid) / len(wid)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="benchmarks/ablation_por_regla.csv")
    a = ap.parse_args()
    if os.path.exists(a.out):
        sys.exit(f"{a.out} ya existe; borralo a mano para recalcular")

    insts = [p for p in sorted(PROBLEM_REGISTRY)
             if re.match(r"int__tai\d+_\d+_\d+$", p)
             and lb_for_problem_name(p) is not None]

    filas = []
    for obj, term, pat in BRAZOS:
        for f in sorted(glob.glob(pat)):
            d = json.load(open(f, encoding="utf-8"))
            r, w = evalua(d["tree"], insts)
            filas.append({"objetivo": obj, "terminales": term,
                          "seed": d["seed"], "re": round(r, 4),
                          "ancho": round(w, 4)})
            print(".", end="", flush=True)
        print(f" {obj}/{term}: {len([x for x in filas if x['objetivo']==obj and x['terminales']==term])}",
              flush=True)

    with open(a.out, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["objetivo", "terminales", "seed",
                                           "re", "ancho"])
        w.writeheader(); w.writerows(filas)
    print(f"\n{len(filas)} reglas -> {a.out}")


if __name__ == "__main__":
    main()
