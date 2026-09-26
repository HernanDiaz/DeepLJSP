# -*- coding: utf-8 -*-
"""Prueba de convergencia en las clasicas antes de lanzar el experimento
del presupuesto sobre ellas: una corrida larga de cada metodo en tres
instancias de tamanos distintos, para ver cuanto tardan en estancarse y
elegir el horizonte con datos.

Metodos: el genetico, el genetico sembrado con la regla y el mejor-de-N
de la regla, cada uno parado por tiempo (LIMITE s), semilla 1, anotando
el mejor RE en cada potencia de dos de schedules construidos. Se corren
seis a la vez, la carga con que se haria el experimento completo.

    python scripts/e6c_piloto_clasicas.py

Salida NUEVA: benchmarks/e6_clasicas/piloto.csv
"""
import csv
import importlib.util
import os
import random
import sys
from concurrent.futures import ProcessPoolExecutor

sys.path.insert(0, ".")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("OMP_NUM_THREADS", "1")

DIR = "benchmarks/e6_clasicas"
INSTANCIAS = "zenodo_caie/instances/interval_classical"
LIMITE = 1200.0
PUNTOS = [2 ** k for k in range(0, 31)]
PILOTO = ["FT10", "La29", "ABZ9"]
METODOS = ["ga", "ga_sembrado", "regla_bon"]


def modulo_clasicas():
    spec = importlib.util.spec_from_file_location(
        "ec12", os.path.join("scripts", "eval_classic12.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def corre(trabajo):
    nombre, metodo = trabajo
    from e6_extension2 import bon_por_tiempo
    from e6_presupuesto import ARBOL
    from jobshop_rl.heuristics.fast_sim import Instancia, despacha, prioridad_de
    from jobshop_rl.heuristics.ga_interval import evoluciona
    ec = modulo_clasicas()
    inst = Instancia(ec.load_instance(os.path.join(INSTANCIAS, ec.FILES[nombre]),
                                      nombre))
    lb = ec.LB[nombre]
    pol = prioridad_de(ARBOL)
    if metodo == "regla_bon":
        c = bon_por_tiempo(inst, pol, 1, LIMITE)
    else:
        siembra = despacha(inst, pol, orden=True)[1] if metodo == "ga_sembrado" else None
        c, _ = evoluciona(inst, PUNTOS[-1], random.Random(1), siembra=siembra,
                          puntos=list(PUNTOS), limite_s=LIMITE)
    return [(metodo, nombre, p, ((cm[0] + cm[1]) / 2 - lb) / lb * 100, seg)
            for p, (cm, seg) in sorted(c.items())]


def main():
    os.makedirs(DIR, exist_ok=True)
    trabajos = [(n, m) for n in PILOTO for m in METODOS]
    with ProcessPoolExecutor(max_workers=6) as ex:
        filas = [f for r in ex.map(corre, trabajos) for f in r]
    with open(os.path.join(DIR, "piloto.csv"), "w", newline="",
              encoding="utf-8") as h:
        w = csv.writer(h)
        w.writerow(["metodo", "instancia", "presupuesto", "re", "segundos"])
        for m, n, p, re_, seg in filas:
            w.writerow([m, n, p, f"{re_:.4f}", f"{seg:.4f}"])
    print(f"escrito {DIR}/piloto.csv")


if __name__ == "__main__":
    main()
