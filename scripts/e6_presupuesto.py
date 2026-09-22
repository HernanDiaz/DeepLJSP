# -*- coding: utf-8 -*-
"""E6: calidad frente a presupuesto, todo en la misma implementacion.

La revision r2 y la r3.5 objetan que el articulo compara la regla
evolucionada con metaheuristicas publicadas en otro lenguaje y con otro
presupuesto, y piden una comparacion a presupuesto igualado. Aqui se
mide todo con el mismo decodificador (jobshop_rl/heuristics/fast_sim.py,
contrastado contra el entorno en tests/test_fast_sim.py), el mismo
evaluador y el mismo lenguaje, sobre las setenta.

Dos monedas, porque no son intercambiables y el articulo tiene que decir
las dos:

  - EVALUACIONES DE SCHEDULE, que no dependen de la implementacion y son
    lo que la revision pide literalmente;
  - SEGUNDOS de esta implementacion, porque una evaluacion no cuesta lo
    mismo en todos los metodos: despachar con una regla calcula nueve
    atributos por elegible en cada decision, y decodificar una
    permutacion ya fijada no calcula ninguno.

Metodos: la regla destacada en una pasada; la regla aleatorizada
mejor-de-N; G&T-MWKR; permutaciones al azar; el genetico; y el genetico
sembrado con la permutacion de la regla.

Reanudable por (carril, metodo, semilla, instancia).

    python scripts/e6_presupuesto.py --carril 0 --de 6

Salida NUEVA: benchmarks/e6_presupuesto/curva_carril<k>.csv
"""
import argparse
import csv
import os
import random
import re
import sys
import time

sys.path.insert(0, ".")
os.environ.setdefault("OMP_NUM_THREADS", "1")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data import PROBLEM_REGISTRY                   # noqa: E402
from jobshop_rl.data.literature_bounds import (                # noqa: E402
    lb_for_problem_name)
from jobshop_rl.heuristics.fast_sim import (                   # noqa: E402
    Instancia, despacha, mejor, prioridad_de)
from jobshop_rl.heuristics.ga_interval import (                # noqa: E402
    azar, evoluciona)

DIR = "benchmarks/e6_presupuesto"
CLASES = {(15, 15), (20, 15), (20, 20), (30, 15), (30, 20),
          (50, 15), (50, 20)}
ARBOL = ("sub", ("sub", ("mul", "SLACK", "SLACK"),
                 ("sub", "WKR", ("add", "PT", "PT"))),
         ("add", "WKRW", "ONE"))
# hasta 2^17: es, en segundos de esta implementacion, el orden del
# mejor-de-1024 de la regla, que es el presupuesto mayor del articulo
PUNTOS_BUSQUEDA = [2 ** k for k in range(0, 18)]
PUNTOS_REGLA = [2 ** k for k in range(0, 11)]      # hasta 1024
EPS = 0.1                                          # el del articulo


def setenta():
    out = []
    for p in PROBLEM_REGISTRY:
        m = re.fullmatch(r"int__tai(\d+)_(\d+)_(\d+)", p)
        if m and (int(m.group(1)), int(m.group(2))) in CLASES:
            out.append(p)
    return sorted(out)


def gt_mwkr(terms):
    """Giffler y Thompson con desempate MWKR, sobre el mismo decodificador.

    Operacion de fin minimo, conflict set de su maquina, y dentro de el
    el trabajo con mas pendiente. Los extremos superiores son el convenio
    lexicografico del articulo. Que esto reproduzca el 29.5 publicado en
    la tabla de baselines es la comprobacion de que el decodificador
    comun no cambia ninguna baseline.
    """
    fin = [e + p for e, p in zip(terms["EST"], terms["PT"])]
    c = min(range(len(fin)), key=lambda i: fin[i])
    maq = terms["_MAQ"]
    cand = [i for i in range(len(fin))
            if maq[i] == maq[c] and terms["EST"][i] < fin[c]]
    if not cand:
        cand = [c]
    return max(cand, key=lambda i: terms["WKR"][i])


def curva_regla_bon(inst, pol, semilla, puntos):
    rng = random.Random(semilla)
    cm0 = despacha(inst, pol)                      # muestra 0: determinista
    curva, mejor_cm, k = {}, cm0, 1
    pend = sorted(puntos)
    while pend and 1 >= pend[0]:
        curva[pend.pop(0)] = mejor_cm
    while pend:
        cm = despacha(inst, pol, eps=EPS, rng=rng)
        k += 1
        if mejor(cm, mejor_cm):
            mejor_cm = cm
        while pend and k >= pend[0]:
            curva[pend.pop(0)] = mejor_cm
    return curva


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--carril", type=int, required=True)
    ap.add_argument("--de", type=int, default=6)
    ap.add_argument("--semillas", type=int, default=2)
    args = ap.parse_args()

    insts = setenta()
    mias = [p for k, p in enumerate(insts) if k % args.de == args.carril]
    os.makedirs(DIR, exist_ok=True)
    salida = os.path.join(DIR, f"curva_carril{args.carril}.csv")
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

        def re_(cm):
            return ((cm[0] + cm[1]) / 2 - lb) / lb * 100

        def anota(metodo, semilla, curva, segundos):
            for p, cm in sorted(curva.items()):
                w.writerow([metodo, semilla, pid, p, f"{re_(cm):.4f}",
                            f"{segundos:.3f}"])
            f.flush()

        # deterministas: una sola evaluacion, y su coste real
        for metodo, politica in (("regla", pol), ("gt_mwkr", gt_mwkr)):
            if (metodo, 0, pid) in hechos:
                continue
            t = time.time()
            cm = despacha(inst, politica)
            anota(metodo, 0, {1: cm}, time.time() - t)

        _, perm = despacha(inst, pol, orden=True)

        for s in range(1, args.semillas + 1):
            if ("regla_bon", s, pid) not in hechos:
                t = time.time()
                c = curva_regla_bon(inst, pol, s, PUNTOS_REGLA)
                anota("regla_bon", s, c, time.time() - t)
            if ("azar", s, pid) not in hechos and s == 1:
                t = time.time()
                c, _ = azar(inst, PUNTOS_BUSQUEDA[-1], random.Random(s),
                            list(PUNTOS_BUSQUEDA))
                anota("azar", s, c, time.time() - t)
            if ("ga", s, pid) not in hechos:
                t = time.time()
                c, _ = evoluciona(inst, PUNTOS_BUSQUEDA[-1],
                                  random.Random(s),
                                  puntos=list(PUNTOS_BUSQUEDA))
                anota("ga", s, c, time.time() - t)
            if ("ga_sembrado", s, pid) not in hechos:
                t = time.time()
                c, _ = evoluciona(inst, PUNTOS_BUSQUEDA[-1],
                                  random.Random(s), siembra=perm,
                                  puntos=list(PUNTOS_BUSQUEDA))
                anota("ga_sembrado", s, c, time.time() - t)
            print(f"  {pid} semilla {s} hecha", flush=True)
    f.close()
    print("carril hecho", flush=True)


if __name__ == "__main__":
    main()
