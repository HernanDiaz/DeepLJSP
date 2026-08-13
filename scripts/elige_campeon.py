# -*- coding: utf-8 -*-
"""Elige el campeon de las 30 semillas SOBRE VALIDACION, nunca sobre test.

El estudio del GP destaca la mejor de sus 30 evoluciones seleccionandola
sobre las mismas 70 instancias en las que luego la reporta. Copiar ese
protocolo importaria su sesgo. Aqui el campeon se elige por RE medio
best-of-64 en TA15-TA20, las seis instancias de validacion, que no
reciben gradientes y que ya cargaban todas las decisiones de diseno;
las 70 quedan intactas para la comparacion.

Lee todos los CSV de validacion de benchmarks/ext30/ y escribe el
ranking completo mas el campeon.

    python scripts/elige_campeon.py
"""
import csv
import glob
import json
import os
import statistics
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PATRON = "benchmarks/ext30/eval_val_bo64*.csv"
SALIDA = "benchmarks/ext30/campeon.json"
VAL = [f"int__tai20_15_{k:02d}" for k in range(5, 11)]


def main():
    por_semilla = {}
    for ruta in sorted(glob.glob(PATRON)):
        for r in csv.DictReader(open(ruta, encoding="utf-8")):
            por_semilla.setdefault(int(r["seed"]), {})[r["instance"]] = (
                float(r["re_greedy"]), float(r["re_bo"]))

    completas = {s: v for s, v in por_semilla.items()
                 if all(i in v for i in VAL)}
    incompletas = sorted(set(por_semilla) - set(completas))
    if incompletas:
        print(f"AVISO: semillas sin las 6 instancias: {incompletas}")

    filas = []
    for s, v in completas.items():
        bo = [v[i][1] for i in VAL]
        gr = [v[i][0] for i in VAL]
        filas.append((sum(bo) / 6, sum(gr) / 6, s))
    filas.sort()

    print(f"\n  {len(filas)} semillas con validacion completa")
    print("\n  puesto  semilla   bo64    greedy")
    for k, (bo, gr, s) in enumerate(filas, 1):
        marca = "  <-- campeon" if k == 1 else ""
        print(f"  {k:>5}     {s:>3}    {bo:6.2f}   {gr:6.2f}{marca}")

    bo_todas = [f[0] for f in filas]
    print(f"\n  media de las {len(filas)}: {statistics.mean(bo_todas):.2f}"
          f"   sd {statistics.stdev(bo_todas):.2f}")
    print(f"  mejor {filas[0][0]:.2f} (semilla {filas[0][2]}), "
          f"peor {filas[-1][0]:.2f} (semilla {filas[-1][2]})")

    campeon = filas[0][2]
    ya = {2: "eval_fair_bo1024.csv (julio)", 3: "eval_fair_bo1024.csv",
          4: "eval_fair_bo1024.csv"}
    if campeon in ya:
        print(f"\n  El campeon es una de las tres desplegadas: su bo1024 "
              f"sobre las 70 ya existe en {ya[campeon]}.")
    else:
        print(f"\n  El campeon ({campeon}) no tiene bo1024 sobre las 70: "
              f"hay que calcularlo.")

    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    json.dump({"campeon": campeon,
               "criterio": "RE medio best-of-64 sobre TA15-TA20",
               "n_semillas": len(filas),
               "media": round(statistics.mean(bo_todas), 4),
               "sd": round(statistics.stdev(bo_todas), 4),
               "ranking": [{"puesto": k, "semilla": s, "bo64": round(bo, 4),
                            "greedy": round(gr, 4)}
                           for k, (bo, gr, s) in enumerate(filas, 1)]},
              open(SALIDA, "w", encoding="utf-8"), indent=2)
    print(f"\n  escrito {SALIDA}")


if __name__ == "__main__":
    main()
