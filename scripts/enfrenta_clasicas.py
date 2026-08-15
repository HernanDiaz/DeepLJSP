# -*- coding: utf-8 -*-
"""Contrastes pareados sobre las 12 clasicas, 30 artefactos por familia.

Misma convencion que el resto del paper: la instancia es la unidad, con
las tiradas promediadas antes del test, y Wilcoxon exacto bilateral.
Con doce instancias el p mas pequeno alcanzable es 0.00049.

Salida NUEVA: benchmarks/ext30/enfrentamiento_clasicas.json

    python scripts/enfrenta_clasicas.py
"""
import json
import os
import statistics
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from scipy import stats                                        # noqa: E402

INST = ["FT10", "FT20", "La21", "La24", "La25", "La27", "La29", "La38",
        "La40", "ABZ7", "ABZ8", "ABZ9"]
SALIDA = "benchmarks/ext30/enfrentamiento_clasicas.json"


def main():
    j = json.load(open("benchmarks/ext30/resumen_clasicas30.json",
                       encoding="utf-8"))
    res = {}
    print(f"  {'presupuesto':<12} {'lectura':<8} "
          f"{'GP':>6} {'POL':>6}  gana  mediana      p")
    for n in ("1", "64", "1024"):
        p = j["presupuestos"][n]
        for lect in ("media", "mejor"):
            a = [p["politica"][lect][i] for i in INST]
            b = [p["gp"][lect][i] for i in INST]
            d = [x - y for x, y in zip(a, b)]
            gana = sum(1 for x in d if x < 0)
            pv = float(stats.wilcoxon(d, method="exact").pvalue)
            print(f"  {n:<12} {lect:<8} {statistics.mean(b):6.2f} "
                  f"{statistics.mean(a):6.2f}  {gana:2d}/12  "
                  f"{statistics.median(d):+6.2f}  {pv:.4f}")
            res[f"{n}_{lect}"] = {
                "gp": round(statistics.mean(b), 4),
                "pol": round(statistics.mean(a), 4),
                "gana_pol": gana,
                "mediana": round(statistics.median(d), 4),
                "p": pv}
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    json.dump(res, open(SALIDA, "w", encoding="utf-8"), indent=2)
    print(f"\n  minimo p alcanzable con 12 instancias: "
          f"{2 / 2 ** 12:.5f}")
    print(f"  escrito {SALIDA}")


if __name__ == "__main__":
    main()
