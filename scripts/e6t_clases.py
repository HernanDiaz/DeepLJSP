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

Cada corrida guarda al pararse su estado completo en ESTADOS (poblacion,
generacion a medias, generador, mejor, reloj). Si despues hace falta
un horizonte mayor para una clase, se pasa con --horizonte y las
corridas de esa clase CONTINUAN desde su estado en lugar de empezar de
cero; la curva resultante es la de una corrida seguida hasta el nuevo
horizonte (tests/test_reanuda.py). Cada fila del CSV lleva el horizonte
de la corrida que la produjo, y quien lee se queda, por corrida, con
las del horizonte mayor.

    python scripts/e6t_clases.py
    python scripts/e6t_clases.py --horizonte 50_15=7200

Version 2: la regla compilada (fast_regla) y el genetico con el
decodificador y el cruce optimizados, que dan los mismos schedules
mas deprisa (tests/test_fast_regla.py, tests/test_ga_optimizado.py).
Las curvas de la version 1 quedan en curvas_v1.csv.

Salida NUEVA: benchmarks/e6_tamanos/curvas.csv y benchmarks/e6_tamanos/estados/
"""
import argparse
import csv
import gzip
import os
import pickle
import random
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

sys.path.insert(0, ".")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("OMP_NUM_THREADS", "1")

DIR = "benchmarks/e6_tamanos"
SALIDA = os.path.join(DIR, "curvas.csv")
ESTADOS = os.path.join(DIR, "estados")
HORIZONTE = {"15_15": 900.0, "30_15": 1800.0, "50_15": 3600.0}
SEMILLAS = (1, 2, 3)
# la mejor solucion se anota en cada 2^(k/4) schedules, cuatro puntos
# por duplicacion, para que el eje de segundos no vaya a escalones largos
PUNTOS = sorted({round(2 ** (k / 4)) for k in range(0, 121)})
PROCESOS = 6
UNA_PASADA = ("regla", "gt_mwkr")


def fichero_estado(pid, metodo, semilla):
    return os.path.join(ESTADOS, f"{pid}__{metodo}__{semilla}.pkl.gz")


def lee_estado(pid, metodo, semilla):
    f = fichero_estado(pid, metodo, semilla)
    if not os.path.exists(f):
        return None
    with gzip.open(f, "rb") as g:
        return pickle.load(g)


def guarda_estado(pid, metodo, semilla, estado):
    f = fichero_estado(pid, metodo, semilla)
    tmp = f + ".tmp"
    with gzip.open(tmp, "wb", compresslevel=1) as g:
        pickle.dump(estado, g, protocol=pickle.HIGHEST_PROTOCOL)
    os.replace(tmp, f)                  # nunca queda un estado a medias


def corre(trabajo):
    pid, metodo, semilla, limite = trabajo
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
    if metodo in UNA_PASADA:
        t0 = time.time()
        cm = desp(inst) if metodo == "regla" else despacha(inst, gt("mwkr"))
        c = {1: (cm, time.time() - t0)}
    else:
        previo = lee_estado(pid, metodo, semilla)
        if metodo == "regla_bon":
            c, est = mejor_de_n(inst, desp, semilla, limite, eps=EPS, puntos=PUNTOS,
                                estado=previo, con_estado=True)
        elif metodo == "azar":
            c, _, est = azar(inst, PUNTOS[-1], random.Random(semilla),
                             list(PUNTOS), limite_s=limite, estado=previo,
                             con_estado=True)
        else:
            siembra = (desp(inst, orden=True)[1]
                       if metodo == "ga_sembrado" and previo is None else None)
            c, _, est = evoluciona(inst, PUNTOS[-1], random.Random(semilla),
                                   siembra=siembra, puntos=list(PUNTOS),
                                   limite_s=limite, estado=previo,
                                   con_estado=True)
        guarda_estado(pid, metodo, semilla, est)
    return [(metodo, semilla, pid, p, ((cm[0] + cm[1]) / 2 - lb) / lb * 100,
             seg, limite) for p, (cm, seg) in sorted(c.items())]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--horizonte", action="append", default=[],
                    help="clase=segundos, p. ej. 50_15=7200; repetible")
    args = ap.parse_args()
    horizonte = dict(HORIZONTE)
    for h in args.horizonte:
        clase, seg = h.split("=")
        assert clase in horizonte, f"clase desconocida: {clase}"
        assert float(seg) >= HORIZONTE[clase], "el horizonte solo se alarga"
        horizonte[clase] = float(seg)
    print("horizontes:", horizonte, flush=True)

    os.makedirs(ESTADOS, exist_ok=True)
    hechos = set()
    if os.path.exists(SALIDA):
        for r in csv.DictReader(open(SALIDA, encoding="utf-8")):
            hechos.add((r["instancia"], r["metodo"], int(r["semilla"]),
                        float(r["horizonte"])))
    nuevo = not os.path.exists(SALIDA)
    f = open(SALIDA, "a", newline="", encoding="utf-8")
    w = csv.writer(f)
    if nuevo:
        w.writerow(["metodo", "semilla", "instancia", "presupuesto", "re",
                    "segundos", "horizonte"])
        f.flush()
    trabajos = []
    # las corridas largas primero, para que no quede una cola de una sola
    for clase in ("50_15", "30_15", "15_15"):
        insts = [f"int__tai{clase}_{k:02d}" for k in range(1, 11)]
        h = horizonte[clase]
        for s in SEMILLAS:
            for pid in insts:
                for m in ("ga", "ga_sembrado", "regla_bon"):
                    trabajos.append((pid, m, s, h))
        for pid in insts:
            trabajos.append((pid, "azar", 1, h))
            # la pasada unica no depende del horizonte: horizonte 0
            trabajos += [(pid, m, 0, 0.0) for m in UNA_PASADA]
    trabajos = [t for t in trabajos if t not in hechos]
    print(f"{len(trabajos)} corridas pendientes", flush=True)
    with ProcessPoolExecutor(max_workers=PROCESOS) as ex:
        futuros = {ex.submit(corre, t): t for t in trabajos}
        for k, fu in enumerate(as_completed(futuros), 1):
            for m, s, pid, p, re_, seg, h in fu.result():
                w.writerow([m, s, pid, p, f"{re_:.4f}", f"{seg:.4f}", f"{h:.0f}"])
            f.flush()
            print(f"  {k}/{len(trabajos)} {futuros[fu]}", flush=True)
    f.close()
    print("experimento hecho", flush=True)


if __name__ == "__main__":
    main()
