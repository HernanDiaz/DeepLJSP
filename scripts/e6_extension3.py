# -*- coding: utf-8 -*-
"""E6, tercera extension: correr por TIEMPO hasta que las curvas se crucen.

Con las dos extensiones anteriores, en el eje de segundos de la figura
del presupuesto el genetico y el sembrado aun no cruzan con claridad al
mejor-de-N de la regla: la curva media se corta donde la primera de las
70 instancias agota su presupuesto (2^20 schedules en unos 180 s en las
pequenas). Aqui los tres metodos corren hasta LIMITE segundos por
instancia, sea cual sea el numero de schedules, con la semilla 1:

  - el genetico y el genetico sembrado, parados por tiempo
    (ga_interval.evoluciona con limite_s);
  - el mejor-de-N, parado por tiempo (e6_extension2.bon_por_tiempo).

Mismas semillas, asi que en los presupuestos comunes el RE coincide con
el de E6 y sus extensiones (e6_tabla.carga_completa lo comprueba, y se
queda con la curva que llega mas lejos).

    python scripts/e6_extension3.py --carril 0 --de 6

Salida NUEVA: benchmarks/e6_presupuesto/curva_ext3_carril<k>.csv
"""
import argparse
import csv
import os
import random
import sys

sys.path.insert(0, ".")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("OMP_NUM_THREADS", "1")

from e6_extension2 import bon_por_tiempo                          # noqa: E402
from e6_presupuesto import ARBOL, DIR, setenta                    # noqa: E402
from jobshop_rl.data import PROBLEM_REGISTRY                      # noqa: E402
from jobshop_rl.data.literature_bounds import (                   # noqa: E402
    lb_for_problem_name)
from jobshop_rl.heuristics.fast_sim import (                      # noqa: E402
    Instancia, despacha, prioridad_de)
from jobshop_rl.heuristics.ga_interval import evoluciona          # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LIMITE = 800.0
PUNTOS = [2 ** k for k in range(0, 27)]
SEMILLA = 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--carril", type=int, required=True)
    ap.add_argument("--de", type=int, default=6)
    args = ap.parse_args()

    insts = setenta()
    mias = [p for k, p in enumerate(insts) if k % args.de == args.carril]
    salida = os.path.join(DIR, f"curva_ext3_carril{args.carril}.csv")
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
    s = SEMILLA
    for pid in mias:
        inst = Instancia(PROBLEM_REGISTRY[pid]())
        lb = lb_for_problem_name(pid)

        def anota(metodo, curva):
            for p, (cm, seg) in sorted(curva.items()):
                re_ = ((cm[0] + cm[1]) / 2 - lb) / lb * 100
                w.writerow([metodo, s, pid, p, f"{re_:.4f}", f"{seg:.4f}"])
            f.flush()

        _, perm = despacha(inst, pol, orden=True)
        if ("ga", s, pid) not in hechos:
            c, _ = evoluciona(inst, PUNTOS[-1], random.Random(s),
                              puntos=list(PUNTOS), limite_s=LIMITE)
            anota("ga", c)
        if ("ga_sembrado", s, pid) not in hechos:
            c, _ = evoluciona(inst, PUNTOS[-1], random.Random(s), siembra=perm,
                              puntos=list(PUNTOS), limite_s=LIMITE)
            anota("ga_sembrado", c)
        if ("regla_bon", s, pid) not in hechos:
            anota("regla_bon", bon_por_tiempo(inst, pol, s, LIMITE))
        print(f"  {pid} hecha", flush=True)
    f.close()
    print("carril hecho", flush=True)


if __name__ == "__main__":
    main()
