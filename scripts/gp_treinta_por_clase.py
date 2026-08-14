# -*- coding: utf-8 -*-
"""Media por clase de las 30 evoluciones publicadas del GP, a una pasada.

La tabla por tamanos comparaba la media de las semillas de la politica
contra la regla DESTACADA del estudio del GP, que es la mejor de sus 30
evoluciones seleccionada sobre estas mismas 70 instancias. Para que las
dos lecturas sean simetricas hace falta tambien la media de las 30
evoluciones desglosada por clase, que sale del mismo deposito publicado
(benchmarks/reevo_fixedfit/summary.csv, familia gp_tuned) del que ya
salia el 18.99 agregado que el paper cita.

No se evalua nada nuevo: se agregan por clase los mismos numeros.

Salida NUEVA: benchmarks/ext30/gp30_por_clase.json

    python scripts/gp_treinta_por_clase.py
"""
import collections
import csv
import json
import os
import statistics
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FUENTE = "benchmarks/reevo_fixedfit/summary.csv"
SALIDA = "benchmarks/ext30/gp30_por_clase.json"
FAMILIA = "gp_tuned"
CLASES = ["tai15_15", "tai20_15", "tai20_20", "tai30_15", "tai30_20",
          "tai50_15", "tai50_20"]


def main():
    metodos = collections.defaultdict(dict)
    for r in csv.DictReader(open(FUENTE, encoding="utf-8")):
        metodos[r["method"]][r["instance"]] = float(r["re"])
    miembros = [m for m in metodos if m.rsplit("_seed", 1)[0] == FAMILIA]
    if len(miembros) != 30:
        raise SystemExit(f"se esperaban 30 evoluciones, hay {len(miembros)}")

    por_clase, por_regla = {}, {}
    for c in CLASES:
        pids = [f"int__{c}_{k:02d}" for k in range(1, 11)]
        medias = [statistics.mean(metodos[m][p] for p in pids)
                  for m in miembros]
        por_clase[c] = statistics.mean(medias)
    for m in miembros:
        por_regla[m] = statistics.mean(metodos[m].values())

    mejor = min(por_regla, key=por_regla.get)
    global_ = statistics.mean(por_regla.values())
    print(f"  {len(miembros)} evoluciones, {len(metodos[miembros[0]])} "
          f"instancias cada una")
    print("\n  clase        media de las 30")
    for c in CLASES:
        print(f"    {c:<10} {por_clase[c]:5.1f}")
    print(f"\n  media global {global_:.2f}   sd "
          f"{statistics.stdev(por_regla.values()):.2f}")
    print(f"  mejor sobre test: {por_regla[mejor]:.2f} ({mejor})")

    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    json.dump({"n": len(miembros),
               "media_global": round(global_, 4),
               "sd": round(statistics.stdev(por_regla.values()), 4),
               "mejor_en_test": round(por_regla[mejor], 4),
               "por_clase": {c: round(v, 4) for c, v in por_clase.items()}},
              open(SALIDA, "w", encoding="utf-8"), indent=2)
    print(f"\n  escrito {SALIDA}")


if __name__ == "__main__":
    main()
