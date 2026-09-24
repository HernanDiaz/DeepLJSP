# -*- coding: utf-8 -*-
"""E6, extension: el genetico y el mejor-de-N, mas alla de donde paro E6.

En E6 el genetico corrio hasta 2^17 schedules y el mejor-de-N de la regla
hasta N = 1024. Con eso las curvas del genetico no llegan a cruzar las
de la regla: en segundos, las instancias pequenas agotan 2^17 hacia los
20 s y la curva media se corta ahi, por encima de la pasada unica. Esta
extension repite las dos curvas con las MISMAS semillas y presupuestos
mayores, hasta 2^20 el genetico y 2^13 el mejor-de-N, para ver donde se
cruzan en lugar de suponerlo.

Con las mismas semillas, los valores de RE hasta los presupuestos de E6
coinciden con los de E6 (el genetico y el muestreo solo usan su
random.Random); e6_tabla.py y la figura toman estas curvas en lugar de
las de E6 para estos dos metodos, y lo comprueban.

Reanudable por (metodo, semilla, instancia). Mismos carriles que E6.

    python scripts/e6_extension.py --carril 0 --de 6

Salida NUEVA: benchmarks/e6_presupuesto/curva_ext_carril<k>.csv
"""
import argparse
import csv
import os
import random
import sys

sys.path.insert(0, ".")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("OMP_NUM_THREADS", "1")

from e6_presupuesto import (ARBOL, DIR, curva_regla_bon,        # noqa: E402
                            setenta)
from jobshop_rl.data import PROBLEM_REGISTRY                    # noqa: E402
from jobshop_rl.data.literature_bounds import (                 # noqa: E402
    lb_for_problem_name)
from jobshop_rl.heuristics.fast_sim import (                    # noqa: E402
    Instancia, prioridad_de)
from jobshop_rl.heuristics.ga_interval import evoluciona        # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PUNTOS_GA = [2 ** k for k in range(0, 21)]         # hasta 2^20
PUNTOS_BON = [2 ** k for k in range(0, 14)]        # hasta 2^13


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--carril", type=int, required=True)
    ap.add_argument("--de", type=int, default=6)
    ap.add_argument("--semillas", type=int, default=2)
    args = ap.parse_args()

    insts = setenta()
    mias = [p for k, p in enumerate(insts) if k % args.de == args.carril]
    salida = os.path.join(DIR, f"curva_ext_carril{args.carril}.csv")
    hechos = set()
    if os.path.exists(salida):
        for r in csv.DictReader(open(salida, encoding="utf-8")):
            hechos.add((r["metodo"], int(r["semilla"]), r["instancia"]))
    f = open(salida, "a", newline="", encoding="utf-8")
    w = csv.writer(f)
    if not hechos:
        w.writerow(["metodo", "semilla", "instancia", "presupuesto",
                    "re", "segundos"])
    pol = prioridad_de(ARBOL)
    print(f"carril {args.carril}: {len(mias)} instancias", flush=True)

    for pid in mias:
        inst = Instancia(PROBLEM_REGISTRY[pid]())
        lb = lb_for_problem_name(pid)

        def anota(metodo, semilla, curva):
            for p, (cm, seg) in sorted(curva.items()):
                re_ = ((cm[0] + cm[1]) / 2 - lb) / lb * 100
                w.writerow([metodo, semilla, pid, p, f"{re_:.4f}",
                            f"{seg:.4f}"])
            f.flush()

        for s in range(1, args.semillas + 1):
            if ("ga", s, pid) not in hechos:
                c, _ = evoluciona(inst, PUNTOS_GA[-1], random.Random(s),
                                  puntos=list(PUNTOS_GA))
                anota("ga", s, c)
            if ("regla_bon", s, pid) not in hechos:
                anota("regla_bon", s,
                      curva_regla_bon(inst, pol, s, PUNTOS_BON))
            print(f"  {pid} semilla {s} hecha", flush=True)
    f.close()
    print("carril hecho", flush=True)


if __name__ == "__main__":
    main()
