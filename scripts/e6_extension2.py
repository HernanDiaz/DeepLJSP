# -*- coding: utf-8 -*-
"""E6, segunda extension: completar la tabla 7 y la figura del presupuesto.

La primera extension (e6_extension.py) alargo solo las dos curvas de las
que dependian los cruces: el genetico hasta 2^20 y el mejor-de-N hasta
2^13. Esta alarga las demas para que la tabla no tenga huecos que solo
se deben a donde se paro cada metodo:

  - el genetico sembrado con la regla, hasta 2^20, dos semillas;
  - las permutaciones al azar, hasta 2^20, una semilla, como en E6;
  - el mejor-de-N, hasta 160 s por instancia en lugar de hasta un N
    fijo, para que la columna de 150 s tenga valor: en schedules no
    puede llegar a 2^17 (cada muestra cuesta lo que decenas de
    decodificaciones del genetico), y ahi la tabla seguira con guion.

Mismas semillas que E6, asi que en los presupuestos comunes el RE
coincide; e6_tabla.carga_completa() lo comprueba al unir.

    python scripts/e6_extension2.py --carril 0 --de 6

Salida NUEVA: benchmarks/e6_presupuesto/curva_ext2_carril<k>.csv
"""
import argparse
import csv
import os
import random
import sys
import time

sys.path.insert(0, ".")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("OMP_NUM_THREADS", "1")

from e6_presupuesto import ARBOL, DIR, EPS, setenta               # noqa: E402
from jobshop_rl.data import PROBLEM_REGISTRY                      # noqa: E402
from jobshop_rl.data.literature_bounds import (                   # noqa: E402
    lb_for_problem_name)
from jobshop_rl.heuristics.fast_sim import (                      # noqa: E402
    Instancia, despacha, mejor, prioridad_de)
from jobshop_rl.heuristics.ga_interval import azar, evoluciona    # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PUNTOS = [2 ** k for k in range(0, 21)]            # hasta 2^20
SEGUNDOS_BON = 160.0


def bon_por_tiempo(inst, pol, semilla, limite):
    """El mejor-de-N de e6_presupuesto.curva_regla_bon, con la misma
    semilla, pero parado por tiempo: anota cada potencia de dos y el
    ultimo punto."""
    rng = random.Random(semilla)
    t0 = time.time()
    mejor_cm = despacha(inst, pol)                 # muestra 0: determinista
    curva, k = {1: (mejor_cm, time.time() - t0)}, 1
    while time.time() - t0 < limite:
        cm = despacha(inst, pol, eps=EPS, rng=rng)
        k += 1
        if mejor(cm, mejor_cm):
            mejor_cm = cm
        if k & (k - 1) == 0:
            curva[k] = (mejor_cm, time.time() - t0)
    curva[k] = (mejor_cm, time.time() - t0)
    return curva


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--carril", type=int, required=True)
    ap.add_argument("--de", type=int, default=6)
    ap.add_argument("--semillas", type=int, default=2)
    args = ap.parse_args()

    insts = setenta()
    mias = [p for k, p in enumerate(insts) if k % args.de == args.carril]
    salida = os.path.join(DIR, f"curva_ext2_carril{args.carril}.csv")
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
    # el mejor-de-N solo se repite donde la primera extension no llego a
    # SEGUNDOS_BON; donde llego, ya cubre la columna y llega mas lejos en N
    fin_ext = {}
    import glob
    for g in glob.glob(os.path.join(DIR, "curva_ext_carril*.csv")):
        for r in csv.DictReader(open(g, encoding="utf-8")):
            if r["metodo"] == "regla_bon":
                k = (r["instancia"], int(r["semilla"]))
                fin_ext[k] = max(fin_ext.get(k, 0.0), float(r["segundos"]))
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

        _, perm = despacha(inst, pol, orden=True)
        for s in range(1, args.semillas + 1):
            if ("ga_sembrado", s, pid) not in hechos:
                c, _ = evoluciona(inst, PUNTOS[-1], random.Random(s),
                                  siembra=perm, puntos=list(PUNTOS))
                anota("ga_sembrado", s, c)
            if s == 1 and ("azar", s, pid) not in hechos:
                c, _ = azar(inst, PUNTOS[-1], random.Random(s), list(PUNTOS))
                anota("azar", s, c)
            if (("regla_bon", s, pid) not in hechos
                    and fin_ext.get((pid, s), 0.0) < SEGUNDOS_BON):
                anota("regla_bon", s,
                      bon_por_tiempo(inst, pol, s, SEGUNDOS_BON))
            print(f"  {pid} semilla {s} hecha", flush=True)
    f.close()
    print("carril hecho", flush=True)


if __name__ == "__main__":
    main()
