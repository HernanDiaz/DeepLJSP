# -*- coding: utf-8 -*-
"""E6 en las doce clasicas: calidad frente a presupuesto, hasta la
convergencia.

La figura del presupuesto sobre las 70 Taillard acaba donde se cruzan
las curvas. En las doce clasicas los metodos son mas rapidos (instancias
de 10x5 a 20x15) y hay resultados publicados con los que comparar, asi
que aqui corren mucho mas alla del cruce, para ver como convergen:

  - la regla destacada en una pasada, y G&T-MWKR, como referencia;
  - el mejor-de-N de la regla, el genetico y el genetico sembrado con la
    regla, 30 corridas por instancia (el protocolo de los resultados
    publicados, medias de 30), paradas por tiempo a LIMITE segundos;
  - las permutaciones al azar, una corrida (son el suelo de referencia).

La prueba de convergencia (e6c_piloto_clasicas.py) fijo el horizonte:
a 900 s dos de las tres instancias de prueba estaban estancadas y la
mayor aun mejoraba despacio.

Seis procesos a la vez, la carga del resto de E6. Cada corrida se anota
en cuanto termina y al arrancar se saltan las hechas, asi que se puede
reanudar.

    python scripts/e6c_clasicas.py

Salida NUEVA: benchmarks/e6_clasicas/curvas.csv
"""
import csv
import importlib.util
import os
import random
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

sys.path.insert(0, ".")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("OMP_NUM_THREADS", "1")

DIR = "benchmarks/e6_clasicas"
SALIDA = os.path.join(DIR, "curvas.csv")
INSTANCIAS = "zenodo_caie/instances/interval_classical"
LIMITE = 900.0
CORRIDAS = 30
PUNTOS = [2 ** k for k in range(0, 31)]
PROCESOS = 6


def modulo_clasicas():
    spec = importlib.util.spec_from_file_location(
        "ec12", os.path.join("scripts", "eval_classic12.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def corre(trabajo):
    nombre, metodo, semilla = trabajo
    from e6_extension2 import bon_por_tiempo
    from e6_presupuesto import ARBOL
    from tiempos_fast import gt
    from jobshop_rl.heuristics.fast_sim import Instancia, despacha, prioridad_de
    from jobshop_rl.heuristics.ga_interval import azar, evoluciona
    ec = modulo_clasicas()
    inst = Instancia(ec.load_instance(os.path.join(INSTANCIAS, ec.FILES[nombre]),
                                      nombre))
    lb = ec.LB[nombre]
    pol = prioridad_de(ARBOL)
    if metodo in ("regla", "gt_mwkr"):
        t0 = time.time()
        cm = despacha(inst, pol if metodo == "regla" else gt("mwkr"))
        c = {1: (cm, time.time() - t0)}
    elif metodo == "regla_bon":
        c = bon_por_tiempo(inst, pol, semilla, LIMITE)
    elif metodo == "azar":
        c, _ = azar(inst, PUNTOS[-1], random.Random(semilla), list(PUNTOS),
                    limite_s=LIMITE)
    else:
        siembra = (despacha(inst, pol, orden=True)[1]
                   if metodo == "ga_sembrado" else None)
        c, _ = evoluciona(inst, PUNTOS[-1], random.Random(semilla),
                          siembra=siembra, puntos=list(PUNTOS),
                          limite_s=LIMITE)
    return [(metodo, semilla, nombre, p,
             ((cm[0] + cm[1]) / 2 - lb) / lb * 100, seg)
            for p, (cm, seg) in sorted(c.items())]


def main():
    ec = modulo_clasicas()
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
    for s in range(1, CORRIDAS + 1):          # semilla a semilla: las
        for n in ec.FILES:                     # primeras corridas de todas
            for m in ("ga", "ga_sembrado", "regla_bon"):   # llegan antes
                trabajos.append((n, m, s))
    for n in ec.FILES:
        trabajos.append((n, "azar", 1))
        trabajos.append((n, "regla", 0))
        trabajos.append((n, "gt_mwkr", 0))
    trabajos = [t for t in trabajos if t not in hechos]
    print(f"{len(trabajos)} corridas pendientes", flush=True)
    with ProcessPoolExecutor(max_workers=PROCESOS) as ex:
        futuros = {ex.submit(corre, t): t for t in trabajos}
        for k, fu in enumerate(as_completed(futuros), 1):
            for fila in fu.result():
                m, s, n, p, re_, seg = fila
                w.writerow([m, s, n, p, f"{re_:.4f}", f"{seg:.4f}"])
            f.flush()
            print(f"  {k}/{len(trabajos)} {futuros[fu]}", flush=True)
    f.close()
    print("experimento hecho", flush=True)


if __name__ == "__main__":
    main()
