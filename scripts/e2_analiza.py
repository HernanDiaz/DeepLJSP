# -*- coding: utf-8 -*-
"""E2: que cambia al entrenar sobre otro subconjunto.

Cada campana de benchmarks/e2_entrenamiento/ evoluciono treinta reglas
sobre un subconjunto distinto de la clase 20x15. Todas se juzgan aqui
sobre las SESENTA instancias de las otras clases, que ningun subconjunto
toca, de modo que la superficie de comparacion es la misma para todas.

La referencia son las treinta reglas del articulo, entrenadas en
TA11--TA14, cuyos RE por instancia ya estan en
benchmarks/reevo_fixedfit/summary.csv.

Se reporta, por campana: media y desviacion del RE entre las treinta
reglas, el contraste pareado por semilla contra la referencia, y el uso
de terminales, que dice si lo que cambia es el rendimiento o la forma de
las reglas.

    python scripts/e2_analiza.py

Salida NUEVA: benchmarks/e2_entrenamiento/resumen.json
"""
import collections
import csv
import glob
import json
import os
import re
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, ".")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data import PROBLEM_REGISTRY                   # noqa: E402
from jobshop_rl.data.literature_bounds import (                # noqa: E402
    lb_for_problem_name)
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.heuristics.gp_rule import GPRuleHeuristic      # noqa: E402
from jobshop_rl.models.interval import Interval                # noqa: E402

DIR = "benchmarks/e2_entrenamiento"
SALIDA = os.path.join(DIR, "resumen.json")
REF = "benchmarks/reevo_fixedfit/summary.csv"
# las sesenta: todo menos la clase 20x15, que es donde entrena cualquier
# campana y por tanto la unica contaminada segun cual sea
NO_VISTAS = sorted(p for p in PROBLEM_REGISTRY
                   if re.match(r"int__tai\d+_\d+_\d+$", p)
                   and not p.startswith("int__tai20_15_")
                   and lb_for_problem_name(p) is not None)


def re_de_regla(tree, insts):
    h = GPRuleHeuristic(tree)
    vals = []
    for pid in insts:
        env = EnvironmentFactory.create_from_problem(
            PROBLEM_REGISTRY[pid](), "basic", seed=0)
        st = env.reset()
        done = False
        while not done and st["eligible_ops"]:
            f = env.get_features(st)
            a = min(h.select_action(st["eligible_ops"], f),
                    len(st["eligible_ops"]) - 1)
            st, _, done, _ = env.step(a)
        c = env.job_completion_time
        lo = max(x.lower if isinstance(x, Interval) else x for x in c)
        up = max(x.upper if isinstance(x, Interval) else x for x in c)
        lb = lb_for_problem_name(pid)
        vals.append(((lo + up) / 2 - lb) / lb * 100)
    return float(np.mean(vals))


def terminales(tree):
    """Cuenta de terminales de un arbol serializado."""
    txt = json.dumps(tree)
    return collections.Counter(re.findall(r'"([A-Z][A-Z0-9_]*)"', txt))


def referencia():
    por = collections.defaultdict(dict)
    for r in csv.DictReader(open(REF, encoding="utf-8")):
        m = re.fullmatch(r"gp_tuned_seed(\d+)", r["method"])
        if m and r["instance"] in set(NO_VISTAS):
            por[int(m.group(1))][r["instance"]] = float(r["re"])
    return {s: float(np.mean(list(v.values()))) for s, v in por.items()}


def main():
    print(f"{len(NO_VISTAS)} instancias no vistas por ninguna campana\n")
    ref = referencia()
    assert len(ref) == 30, f"{len(ref)} reglas de referencia"
    v_ref = np.array([ref[s] for s in sorted(ref)])
    print(f"  {'campana':<12} {'n':>3} {'RE medio':>9} {'sd':>6} "
          f"{'min':>7} {'max':>7} {'d vs ref':>9} {'p':>8}")
    print(f"  {'TA11-TA14':<12} {30:>3} {v_ref.mean():9.2f} "
          f"{v_ref.std(ddof=1):6.2f} {v_ref.min():7.2f} {v_ref.max():7.2f}")

    res = {"referencia": {"media": float(v_ref.mean()),
                          "sd": float(v_ref.std(ddof=1))}, "campanas": {}}
    usos = {"TA11-TA14": collections.Counter()}
    for f in sorted(glob.glob("benchmarks/reevo_fixedfit/gp_tuned_seed*.json")):
        usos["TA11-TA14"] += terminales(
            json.load(open(f, encoding="utf-8"))["tree"])

    for camp in sorted(d for d in os.listdir(DIR)
                       if os.path.isdir(os.path.join(DIR, d))):
        ficheros = sorted(glob.glob(os.path.join(DIR, camp, "seed*.json")))
        if not ficheros:
            continue
        vals, semillas, uso = {}, [], collections.Counter()
        for f in ficheros:
            s = int(re.search(r"seed(\d+)", os.path.basename(f)).group(1))
            tree = json.load(open(f, encoding="utf-8"))["tree"]
            vals[s] = re_de_regla(tree, NO_VISTAS)
            uso += terminales(tree)
            semillas.append(s)
        usos[camp] = uso
        v = np.array([vals[s] for s in sorted(vals)])
        # pareado por semilla: misma semilla, distinto conjunto
        comunes = sorted(set(vals) & set(ref))
        a = np.array([vals[s] for s in comunes])
        b = np.array([ref[s] for s in comunes])
        w = stats.wilcoxon(a, b, method="exact", zero_method="wilcox")
        print(f"  {camp:<12} {len(v):>3} {v.mean():9.2f} "
              f"{v.std(ddof=1):6.2f} {v.min():7.2f} {v.max():7.2f} "
              f"{(a - b).mean():+9.2f} {w.pvalue:8.4f}")
        res["campanas"][camp] = {
            "n": len(v), "media": float(v.mean()),
            "sd": float(v.std(ddof=1)), "min": float(v.min()),
            "max": float(v.max()), "d_vs_ref": float((a - b).mean()),
            "p": float(w.pvalue), "por_semilla": vals}

    print("\n  uso de terminales (fraccion del total, por campana)")
    claves = sorted({k for u in usos.values() for k in u},
                    key=lambda k: -usos["TA11-TA14"][k])[:8]
    print(f"  {'campana':<12} " + " ".join(f"{k:>7}" for k in claves))
    for camp, u in usos.items():
        tot = sum(u.values()) or 1
        print(f"  {camp:<12} " +
              " ".join(f"{100 * u[k] / tot:6.1f}%" for k in claves))
    res["terminales"] = {c: dict(u) for c, u in usos.items()}

    json.dump(res, open(SALIDA, "w", encoding="utf-8"), indent=1)
    print(f"\nescrito {SALIDA}")


if __name__ == "__main__":
    main()
