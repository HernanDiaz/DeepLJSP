# -*- coding: utf-8 -*-
"""E6: lee las curvas de presupuesto y dice donde se cruza cada metodo.

Dos ejes, porque una evaluacion no cuesta lo mismo en todos los metodos:

  - EVALUACIONES DE SCHEDULE, la moneda que no depende de la
    implementacion, que es la que pide la revision;
  - SEGUNDOS de esta implementacion, donde despachar con una regla sale
    caro porque calcula nueve atributos por elegible en cada decision.

En el eje del reloj los metodos no comparten rejilla, asi que se
interpola por instancia: el RE de un metodo en el segundo t es el mejor
que habia conseguido hasta t, que es una funcion escalonada bien
definida porque el mejor-hasta-ahora no sube. Se promedia despues.

    python scripts/e6_analiza.py

Salida NUEVA: benchmarks/e6_presupuesto/resumen.json
"""
import collections
import csv
import glob
import json
import os
import sys

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DIR = "benchmarks/e6_presupuesto"
SALIDA = os.path.join(DIR, "resumen.json")
ORDEN = ["regla", "gt_mwkr", "regla_bon", "azar", "ga", "ga_sembrado"]
ETIQUETA = {"regla": "evolved rule, one pass",
            "gt_mwkr": "G&T-MWKR, one pass",
            "regla_bon": "evolved rule, best-of-N",
            "azar": "random permutations",
            "ga": "genetic algorithm",
            "ga_sembrado": "GA seeded with the rule"}
# rejilla de reloj: de un milisegundo a cinco minutos por instancia
REJILLA = np.logspace(-3, np.log10(300), 60)


def carga():
    """{metodo: {instancia: {semilla: [(presupuesto, re, segundos)]}}}"""
    d = collections.defaultdict(
        lambda: collections.defaultdict(lambda: collections.defaultdict(list)))
    for f in sorted(glob.glob(os.path.join(DIR, "curva_carril*.csv"))):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            d[r["metodo"]][r["instancia"]][int(r["semilla"])].append(
                (int(r["presupuesto"]), float(r["re"]), float(r["segundos"])))
    return d


def escalon(puntos, t):
    """El mejor RE alcanzado hasta el segundo t.

    NaN antes del primer punto medido y tambien DESPUES del ultimo: la
    curva de un metodo termina donde termina su presupuesto, y
    prolongarla plana haria creer que sigue ahi cuando en realidad no se
    midio. Esto importa para el mejor-de-N de la regla, cuyo presupuesto
    en evaluaciones es mil veces menor que el del genetico.
    """
    if not puntos or t > max(seg for _, _, seg in puntos):
        return float("nan")
    vistos = [re for _, re, seg in puntos if seg <= t]
    return min(vistos) if vistos else float("nan")


def main():
    d = carga()
    if not d:
        sys.exit(f"no hay curvas en {DIR}: lanza e6_presupuesto.py primero")
    insts = sorted(set(d["ga"]) if "ga" in d else set())
    print(f"{len(insts)} instancias\n")

    res = {"n_instancias": len(insts), "por_evaluaciones": {},
           "por_reloj": {}, "rejilla_reloj": list(REJILLA)}

    # --- eje de evaluaciones ------------------------------------------
    print("RE medio por numero de evaluaciones de schedule")
    presupuestos = sorted({p for m in d for i in d[m] for s in d[m][i]
                           for p, _, _ in d[m][i][s]})
    muestra = [p for p in presupuestos if p in
               (1, 64, 1024, 4096, 16384, 65536, 131072)]
    print(f"  {'metodo':<26} " + " ".join(f"{p:>8}" for p in muestra))
    for m in ORDEN:
        if m not in d:
            continue
        fila = {}
        for p in presupuestos:
            v = []
            for i in insts:
                por_semilla = [re for s in d[m][i]
                               for q, re, _ in d[m][i][s] if q == p]
                if por_semilla:
                    v.append(np.mean(por_semilla))
            if len(v) == len(insts):
                fila[p] = float(np.mean(v))
        res["por_evaluaciones"][m] = {str(k): v for k, v in fila.items()}
        print(f"  {ETIQUETA[m]:<26} " +
              " ".join(f"{fila[p]:8.2f}" if p in fila else f"{'':>8}"
                       for p in muestra))

    # --- eje del reloj --------------------------------------------------
    print("\nRE medio por segundos de esta implementacion")
    for m in ORDEN:
        if m not in d:
            continue
        curva = []
        for t in REJILLA:
            v = []
            for i in insts:
                por_semilla = [escalon(d[m][i][s], t) for s in d[m][i]]
                por_semilla = [x for x in por_semilla if not np.isnan(x)]
                if por_semilla:
                    v.append(np.mean(por_semilla))
            curva.append(float(np.mean(v)) if len(v) == len(insts)
                         else float("nan"))
        res["por_reloj"][m] = curva

    # --- los cruces, que es lo que el articulo tiene que decir ----------
    base = res["por_evaluaciones"]["regla"]["1"]
    print(f"\n  la regla en una pasada: {base:.2f}")
    res["regla_una_pasada"] = base
    res["cruces"] = {}
    for m in ("azar", "ga", "ga_sembrado", "regla_bon"):
        if m not in res["por_evaluaciones"]:
            continue
        fila = {int(k): v for k, v in res["por_evaluaciones"][m].items()}
        cruce = next((p for p in sorted(fila) if fila[p] < base), None)
        res["cruces"][m] = cruce
        print(f"  {ETIQUETA[m]:<26} la iguala en "
              + (f"{cruce} evaluaciones" if cruce else "ningun presupuesto"))

    # el cruce que importa en reloj: cuando el genetico alcanza al
    # mejor-de-N de la regla, que es el metodo que mas rinde por segundo
    if "regla_bon" in res["por_reloj"] and "ga" in res["por_reloj"]:
        bon = np.array(res["por_reloj"]["regla_bon"], dtype=float)
        ga = np.array(res["por_reloj"]["ga"], dtype=float)
        val = ~(np.isnan(bon) | np.isnan(ga))
        cruce = None
        for k in np.where(val)[0]:
            if ga[k] < bon[k]:
                cruce = float(REJILLA[k])
                break
        res["cruce_reloj_ga_vs_bon"] = cruce
        print(f"\n  en reloj, el genetico alcanza al mejor-de-N de la regla "
              + (f"a los {cruce:.1f} s por instancia" if cruce
                 else "en ningun punto de la rejilla"))

    json.dump(res, open(SALIDA, "w", encoding="utf-8"), indent=1)
    print(f"\nescrito {SALIDA}")


if __name__ == "__main__":
    main()
