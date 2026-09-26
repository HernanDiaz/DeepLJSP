# -*- coding: utf-8 -*-
"""E6 por tamano de instancia: tres clases de Taillard, mas alla del cruce.

En la media de las 70 Taillard los cruces entre el genetico, el genetico
sembrado y el mejor-de-N de la regla ocurren a tiempos muy distintos
segun el tamano, y en las instancias grandes la figura acaba antes de
ver que pasa despues. Aqui una clase por panel, las tres con 15
maquinas para que solo cambie el numero de trabajos:

  15x15, 30x15 y 50x15, las 10 instancias de cada una,
  3 corridas (semillas 1-3) del genetico, el sembrado y el mejor-de-N,
  1 corrida de permutaciones al azar, y las dos pasadas unicas,

parados por tiempo con un horizonte por clase, mas de un orden de
magnitud despues del ultimo cruce observado en los datos de E6 (a 800 s,
el genetico cruza al mejor-de-N hacia los 50, 86 y 324 s).

Las semillas son las de E6: sus curvas coinciden con las de E6 en los
presupuestos comunes. Seis procesos a la vez; cada corrida se anota al
terminar y al arrancar se saltan las hechas.

    python scripts/e6t_clases.py

Salida NUEVA: benchmarks/e6_tamanos/curvas.csv
"""
import csv
import os
import random
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

sys.path.insert(0, ".")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("OMP_NUM_THREADS", "1")

DIR = "benchmarks/e6_tamanos"
SALIDA = os.path.join(DIR, "curvas.csv")
HORIZONTE = {"15_15": 900.0, "30_15": 1800.0, "50_15": 3600.0}
SEMILLAS = (1, 2, 3)
PUNTOS = [2 ** k for k in range(0, 31)]
PROCESOS = 6


def corre(trabajo):
    pid, metodo, semilla = trabajo
    from e6_extension2 import bon_por_tiempo
    from e6_presupuesto import ARBOL
    from tiempos_fast import gt
    from jobshop_rl.data import PROBLEM_REGISTRY
    from jobshop_rl.data.literature_bounds import lb_for_problem_name
    from jobshop_rl.heuristics.fast_sim import Instancia, despacha, prioridad_de
    from jobshop_rl.heuristics.ga_interval import azar, evoluciona
    inst = Instancia(PROBLEM_REGISTRY[pid]())
    lb = lb_for_problem_name(pid)
    limite = HORIZONTE[pid.split("tai")[1][:5]]
    pol = prioridad_de(ARBOL)
    if metodo in ("regla", "gt_mwkr"):
        t0 = time.time()
        cm = despacha(inst, pol if metodo == "regla" else gt("mwkr"))
        c = {1: (cm, time.time() - t0)}
    elif metodo == "regla_bon":
        c = bon_por_tiempo(inst, pol, semilla, limite)
    elif metodo == "azar":
        c, _ = azar(inst, PUNTOS[-1], random.Random(semilla), list(PUNTOS),
                    limite_s=limite)
    else:
        siembra = (despacha(inst, pol, orden=True)[1]
                   if metodo == "ga_sembrado" else None)
        c, _ = evoluciona(inst, PUNTOS[-1], random.Random(semilla),
                          siembra=siembra, puntos=list(PUNTOS),
                          limite_s=limite)
    return [(metodo, semilla, pid, p, ((cm[0] + cm[1]) / 2 - lb) / lb * 100, seg)
            for p, (cm, seg) in sorted(c.items())]


def main():
    os.makedirs(DIR, exist_ok=True)
    hechos = set()
    if os.path.exists(SALIDA):
        for r in csv.DictReader(open(SALIDA, encoding="utf-8")):
            hechos.add((r["instancia"], r["metodo"], int(r["semilla"])))
    nuevo = not os.path.exists(SALIDA)
    f = open(SALIDA, "a", newline="", encoding="utf-8")
    w = csv.writer(f)
    if nuevo:
        w.writerow(["metodo", "semilla", "instancia", "presupuesto", "re",
                    "segundos"])
        f.flush()
    trabajos = []
    # las corridas largas primero, para que no quede una cola de una sola
    for clase in ("50_15", "30_15", "15_15"):
        insts = [f"int__tai{clase}_{k:02d}" for k in range(1, 11)]
        for s in SEMILLAS:
            for pid in insts:
                for m in ("ga", "ga_sembrado", "regla_bon"):
                    trabajos.append((pid, m, s))
        for pid in insts:
            trabajos += [(pid, "azar", 1), (pid, "regla", 0), (pid, "gt_mwkr", 0)]
    trabajos = [t for t in trabajos if t not in hechos]
    print(f"{len(trabajos)} corridas pendientes", flush=True)
    with ProcessPoolExecutor(max_workers=PROCESOS) as ex:
        futuros = {ex.submit(corre, t): t for t in trabajos}
        for k, fu in enumerate(as_completed(futuros), 1):
            for m, s, pid, p, re_, seg in fu.result():
                w.writerow([m, s, pid, p, f"{re_:.4f}", f"{seg:.4f}"])
            f.flush()
            print(f"  {k}/{len(trabajos)} {futuros[fu]}", flush=True)
    f.close()
    print("experimento hecho", flush=True)


if __name__ == "__main__":
    main()
