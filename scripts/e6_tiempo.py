# -*- coding: utf-8 -*-
"""E6 en las 70 Taillard, de una vez: todos los metodos parados por tiempo.

Sustituye a E6 y a sus tres extensiones (e6_extension*.py), que
alargaron las curvas por capas con presupuestos distintos. Aqui cada
corrida se para a LIMITE segundos por instancia y anota el mejor
makespan en cada potencia de dos de schedules y al final, asi que de
las mismas corridas salen los dos ejes de la tabla y la figura del
presupuesto:

  - el genetico, el genetico sembrado con la regla y el mejor-de-N de la
    regla, semillas 1 y 2, las de E6;
  - las permutaciones al azar, semilla 1;
  - la regla en una pasada, y G&T-MWKR, como referencia.

La regla va compilada (fast_regla) y el genetico con el decodificador y
el cruce optimizados: dan los mismos schedules que la implementacion
anterior con las mismas semillas (tests/test_fast_regla.py,
tests/test_ga_optimizado.py), asi que en el eje de schedules las curvas
coinciden con las de E6 y solo cambia el de segundos.

Seis procesos a la vez; cada corrida se anota al terminar y al arrancar
se saltan las hechas.

    python scripts/e6_tiempo.py

Salida NUEVA: benchmarks/e6_tiempo/curvas.csv
"""
import csv
import os
import random
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed

sys.path.insert(0, ".")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("OMP_NUM_THREADS", "1")

DIR = "benchmarks/e6_tiempo"
SALIDA = os.path.join(DIR, "curvas.csv")
LIMITE = 800.0
SEMILLAS = (1, 2)
PUNTOS = [2 ** k for k in range(0, 31)]
PROCESOS = 6


def corre(trabajo):
    import time
    pid, metodo, semilla = trabajo
    from e6_presupuesto import ARBOL, EPS
    from tiempos_fast import gt
    from jobshop_rl.data import PROBLEM_REGISTRY
    from jobshop_rl.data.literature_bounds import lb_for_problem_name
    from jobshop_rl.heuristics.fast_regla import despachador, mejor_de_n
    from jobshop_rl.heuristics.fast_sim import Instancia, despacha
    from jobshop_rl.heuristics.ga_interval import azar, evoluciona
    inst = Instancia(PROBLEM_REGISTRY[pid]())
    lb = lb_for_problem_name(pid)
    desp = despachador(ARBOL)
    if metodo in ("regla", "gt_mwkr"):
        t0 = time.time()
        cm = desp(inst) if metodo == "regla" else despacha(inst, gt("mwkr"))
        c = {1: (cm, time.time() - t0)}
    elif metodo == "regla_bon":
        c = mejor_de_n(inst, desp, semilla, LIMITE, eps=EPS)
    elif metodo == "azar":
        c, _ = azar(inst, PUNTOS[-1], random.Random(semilla), list(PUNTOS),
                    limite_s=LIMITE)
    else:
        siembra = (desp(inst, orden=True)[1]
                   if metodo == "ga_sembrado" else None)
        c, _ = evoluciona(inst, PUNTOS[-1], random.Random(semilla),
                          siembra=siembra, puntos=list(PUNTOS),
                          limite_s=LIMITE)
    return [(metodo, semilla, pid, p, ((cm[0] + cm[1]) / 2 - lb) / lb * 100, seg)
            for p, (cm, seg) in sorted(c.items())]


def main():
    from e6_presupuesto import setenta
    insts = setenta()
    assert len(insts) == 70, len(insts)
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
    for s in SEMILLAS:                  # semilla a semilla: la primera
        for pid in insts:               # corrida de todas llega antes
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
