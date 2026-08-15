# -*- coding: utf-8 -*-
"""Las ablaciones sobre las 60 instancias no vistas, a una pasada.

Sobre las seis de validacion los dos efectos de interes se quedaban en
la frontera (p=0.094 y p=0.063): con seis instancias el test no tiene
potencia para separarlos. Aqui la unidad sigue siendo la instancia,
pero hay sesenta, ninguna vista por ningun brazo, y la evaluacion es
determinista, asi que la diferencia no arrastra ruido de muestreo.

Salida NUEVA: benchmarks/ext30/ablaciones_sesenta.json

    python scripts/ablaciones_sesenta.py
"""
import collections
import csv
import glob
import json
import math
import os
import statistics
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from scipy import stats                                        # noqa: E402

SALIDA = "benchmarks/ext30/ablaciones_sesenta.json"
PARES = [("v2-nowidth-1000ep", "las anchuras como entrada"),
         ("v2-midpoint-1000ep", "los intervalos como datos")]


def main():
    d = collections.defaultdict(lambda: collections.defaultdict(dict))
    for f in sorted(glob.glob("benchmarks/ext30/t60_*.csv")):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            d[r["arm"]][int(r["seed"])][r["instance"]] = float(r["re_greedy"])
    base = d["v2-full-1000ep"]
    inst = sorted({i for v in base.values() for i in v})
    print(f"  {len(inst)} instancias, {len(base)} semillas en el brazo base")

    res = {}
    for arm, etq in PARES:
        sem = sorted(set(d[arm]) & set(base))
        a = {i: statistics.mean(d[arm][s][i] for s in sem) for i in inst}
        b = {i: statistics.mean(base[s][i] for s in sem) for i in inst}
        dif = [a[i] - b[i] for i in inst]
        md, sd = statistics.mean(dif), statistics.stdev(dif)
        semi = stats.t.ppf(0.975, len(dif) - 1) * sd / math.sqrt(len(dif))
        p = float(stats.wilcoxon(dif).pvalue)
        peor = sum(1 for x in dif if x > 0)
        print(f"\n  {etq} ({arm}, {len(sem)} semillas)")
        print(f"    base {statistics.mean(b.values()):.2f}   "
              f"brazo {statistics.mean(a.values()):.2f}   "
              f"diferencia {md:+.2f} [{md - semi:+.2f}, {md + semi:+.2f}]")
        print(f"    peor en {peor}/{len(inst)} instancias   p={p:.2g}")
        res[arm] = {"n_instancias": len(inst), "n_semillas": len(sem),
                    "base": round(statistics.mean(b.values()), 4),
                    "brazo": round(statistics.mean(a.values()), 4),
                    "dif": round(md, 4),
                    "ic95": [round(md - semi, 4), round(md + semi, 4)],
                    "peor_en": peor, "p": p}
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    json.dump(res, open(SALIDA, "w", encoding="utf-8"), indent=2)
    print(f"\n  escrito {SALIDA}")


if __name__ == "__main__":
    main()
