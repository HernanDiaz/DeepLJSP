# -*- coding: utf-8 -*-
"""Las ablaciones bajo el evaluador unico, con la instancia como unidad.

Cada brazo se compara contra el principal EN SUS MISMAS SEMILLAS: el
principal tiene treinta y las ablaciones diez, y enfrentar diez contra
treinta reintroduciria la asimetria que el resto del paper acaba de
quitar. Las diferencias se promedian por instancia antes del test,
segun la convencion de la Seccion 5.1.

Salida NUEVA: benchmarks/ext30/ablaciones_unificadas.json

    python scripts/ablaciones_unificadas.py
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

SALIDA = "benchmarks/ext30/ablaciones_unificadas.json"
VAL = [f"int__tai20_15_{k:02d}" for k in range(5, 11)]
PARES = [("v2-attn-300ep", "v2-full-300ep", "atencion, 300 episodios"),
         ("v2-attn-1000ep", "v2-full-1000ep", "atencion, 1000 episodios"),
         ("v2-nowidth-1000ep", "v2-full-1000ep", "sin anchuras"),
         ("v2-midpoint-1000ep", "v2-full-1000ep", "punto medio")]


def carga():
    d = collections.defaultdict(lambda: collections.defaultdict(dict))
    for f in sorted(glob.glob("benchmarks/ext30/val_*.csv")):
        if "CUARENTENA" in f:
            continue
        for r in csv.DictReader(open(f, encoding="utf-8")):
            d[r["arm"]][int(r["seed"])][r["instance"]] = float(r["re_bo"])
    for f in sorted(glob.glob("benchmarks/ext30/eval_val_bo64*.csv")):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            d["v2-full-1000ep"][int(r["seed"])][r["instance"]] = float(
                r["re_bo"])
    return d


def main():
    d = carga()
    res = {}
    print(f"  {'ablacion':<26} {'base':>6} {'brazo':>6} {'dif':>6} "
          f"{'IC95':>16} {'peor':>6}    p")
    for arm, base, etq in PARES:
        sem = sorted(set(d[arm]) & set(d[base]))
        if not sem:
            print(f"  {etq}: sin semillas comunes")
            continue
        a = {i: statistics.mean(d[arm][s][i] for s in sem) for i in VAL}
        b = {i: statistics.mean(d[base][s][i] for s in sem) for i in VAL}
        dif = [a[i] - b[i] for i in VAL]
        md, sd = statistics.mean(dif), statistics.stdev(dif)
        semi = stats.t.ppf(0.975, 5) * sd / math.sqrt(6)
        p = float(stats.wilcoxon(dif, method="exact").pvalue)
        peor = sum(1 for x in dif if x > 0)
        print(f"  {etq:<26} {statistics.mean(b.values()):6.2f} "
              f"{statistics.mean(a.values()):6.2f} {md:+6.2f} "
              f"[{md - semi:+6.2f},{md + semi:+6.2f}] {peor:>3}/6  {p:.4f}")
        res[arm] = {"base": round(statistics.mean(b.values()), 4),
                    "brazo": round(statistics.mean(a.values()), 4),
                    "n_semillas": len(sem), "dif": round(md, 4),
                    "ic95": [round(md - semi, 4), round(md + semi, 4)],
                    "peor_en": peor, "p": p}
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    json.dump(res, open(SALIDA, "w", encoding="utf-8"), indent=2)
    print(f"\n  escrito {SALIDA}")


if __name__ == "__main__":
    main()
