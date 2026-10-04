# -*- coding: utf-8 -*-
"""Contrastes entre brazos de evoluciones con Mann-Whitney (no pareado).

Dos brazos que difieren en el conjunto de terminales, la fitness o el
banco no comparten nada mas que el numero de semilla: con otro conjunto
de terminales la poblacion inicial ya es distinta, y la correlacion entre
las reglas de la misma semilla es nula. Emparejar por semilla no esta
justificado, asi que aqui cada brazo es una muestra independiente de
reglas (cada una promediada sobre las instancias) y se contrastan con
Mann-Whitney de dos colas:

  - z de la aproximacion normal (con correccion de empates), NEGATIVO
    cuando el primer brazo nombrado tiene los valores menores;
  - p de scipy (asintotico con correccion de continuidad);
  - |r| biserial de rangos, |2 U1 / (n1 n2) - 1|, que vale 1 cuando los
    dos brazos no se solapan;
  - Holm dentro de cada familia de contrastes.

Familias: la ablacion de 7.4 (seis), la robustez por brazo de S2 (tres) y
los brazos asimetricos de S4 (nueve).

    python scripts/brazos_mw.py

Salida NUEVA: benchmarks/brazos_mw.json
"""
import csv
import json

import numpy as np
from scipy.stats import mannwhitneyu, rankdata

SALIDA = "benchmarks/brazos_mw.json"


def mw(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    n1, n2 = len(x), len(y)
    u1 = mannwhitneyu(x, y, alternative="two-sided").statistic
    p = float(mannwhitneyu(x, y, alternative="two-sided").pvalue)
    r = rankdata(np.concatenate([x, y]))
    _, t = np.unique(r, return_counts=True)
    n = n1 + n2
    sigma = np.sqrt(n1 * n2 / 12 * ((n + 1) - (t ** 3 - t).sum() / (n * (n - 1))))
    z = float((u1 - n1 * n2 / 2) / sigma)
    return {"z": z, "p": p, "r": float(abs(2 * u1 / (n1 * n2) - 1)),
            "media_a": float(x.mean()), "media_b": float(y.mean()),
            "n_a": n1, "n_b": n2,
            "separados": bool(x.max() < y.min() or y.max() < x.min())}


def holm(fam):
    claves = sorted(fam, key=lambda k: fam[k]["p"])
    m, previo = len(claves), 0.0
    for i, k in enumerate(claves):
        previo = max(previo, min(1.0, (m - i) * fam[k]["p"]))
        fam[k]["p_holm"] = previo
    return fam


def main():
    out = {}
    # 7.4: ablacion de terminales y control del punto medio (30 por brazo)
    d = {}
    for r in csv.DictReader(open("benchmarks/ablation_por_regla.csv", encoding="utf-8")):
        d.setdefault((r["objetivo"], r["terminales"]), []).append(
            (float(r["re"]), float(r["ancho"])))
    d[("crisp", "nowidth")] = [(float(r["re"]), float(r["ancho"])) for r in csv.DictReader(
        open("benchmarks/midpoint_control_por_regla.csv", encoding="utf-8"))]
    fam = {}
    for et, a, b in (("makespan", ("makespan", "full"), ("makespan", "nowidth")),
                     ("robust", ("robust", "full"), ("robust", "nowidth")),
                     ("crisp", ("crisp", "nowidth"), ("makespan", "nowidth"))):
        assert len(d[a]) == len(d[b]) == 30
        for k, med in ((0, "re"), (1, "ancho")):
            fam[f"{et}/{med}"] = mw([v[k] for v in d[a]], [v[k] for v in d[b]])
    out["ablacion"] = holm(fam)

    # S2: robustez por brazo, las 30 reglas de cada uno
    e = {}
    for r in csv.DictReader(open("benchmarks/eps_por_regla.csv", encoding="utf-8")):
        e.setdefault(r["arm"], []).append(float(r["eps_bar_x1000"]))
    out["eps_brazo"] = holm({
        "full vs nowidth": mw(e["full"], e["nowidth"]),
        "rob-full vs rob-nowidth": mw(e["rob-full"], e["rob-nowidth"]),
        "rob-full vs full": mw(e["rob-full"], e["full"])})

    # S4: brazos asimetricos (15 por brazo), los nueve contrastes de la tabla
    A = json.load(open("benchmarks/e4_asimetrico/resumen.json", encoding="utf-8"))
    ps = A["ramas"]
    fam = {}
    for par in ("full vs nowidth", "rob1 vs rob1_nowidth", "rob1 vs full"):
        a, b = par.split(" vs ")
        for med in ("re", "anchura", "abs"):
            x = [v[med] for v in ps[a]["por_semilla"].values()]
            y = [v[med] for v in ps[b]["por_semilla"].values()]
            assert len(x) == len(y) == 15
            fam[f"{par}/{med}"] = mw(x, y)
    out["asimetrico"] = holm(fam)

    json.dump(out, open(SALIDA, "w", encoding="utf-8"), indent=1)
    for f, v in out.items():
        print(f"== {f}")
        for k, c in v.items():
            print(f"  {k:30s} z={c['z']:+.2f}  p={c['p']:.4f}  holm={c['p_holm']:.4f}"
                  f"  |r|={c['r']:.2f}  {c['media_a']:.2f} vs {c['media_b']:.2f}"
                  f"{'  SEPARADOS' if c['separados'] else ''}")
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
