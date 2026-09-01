# -*- coding: utf-8 -*-
"""Contraste a nivel de ARTEFACTO en B=64 sobre las setenta Taillard.

El contraste muestreado del paper enfrentaba un checkpoint contra una
regla, de modo que el Wilcoxon media variacion entre instancias y no
entre artefactos. Aqui se enfrentan las familias enteras al mismo
presupuesto:

  - politica: los diez artefactos del deposito de la curva
    (benchmarks/curva_intervalo), cada uno con 342 rollouts por
    instancia de los que se gasta la pasada greedy mas 63 muestras.
  - regla: las treinta del brazo principal
    (benchmarks/gp_treinta_bo64), cada una con su propio pool de 64.

Cada artefacto gasta su presupuesto UNA vez, como haria uno
desplegado, de modo que los dos lados llevan el mismo ruido de
realizacion. Como sensibilidad se recalcula el lado de la politica
como media de 200 subconjuntos, que quita ese ruido de un solo lado y
sirve para comprobar que la conclusion no depende del sorteo.

Convencion estadistica del paper: se promedia dentro de la familia por
instancia y la instancia es la unidad; Wilcoxon exacto de dos colas.

    python scripts/analiza_artefactos_bo64.py

Salida NUEVA: benchmarks/gp_treinta_bo64/contraste_bo64.json
"""
import collections
import csv
import glob
import json
import os
import sys

import numpy as np
from scipy import stats

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GP = sorted(glob.glob("benchmarks/gp_treinta_bo64/pool_*.csv"))
POL = sorted(glob.glob("benchmarks/curva_intervalo/curva_*.csv"))
SALIDA = "benchmarks/gp_treinta_bo64/contraste_bo64.json"
B = 64
R = 200


def re_mid(par, lb):
    return ((par[0] + par[1]) / 2 - lb) / lb * 100


def mejor(pares):
    """El de menor (U, L), el criterio de la Ec. (3)."""
    return min(pares, key=lambda p: (p[1], p[0]))


def carga_gp():
    pools = collections.defaultdict(dict)
    lbs = {}
    for ruta in GP:
        for r in csv.DictReader(open(ruta, encoding="utf-8")):
            k = (int(r["rule_seed"]), r["instance"])
            pools[k][int(r["sample_idx"])] = (float(r["lo"]), float(r["up"]))
            lbs[r["instance"]] = float(r["lb"])
    fuera = {k: len(v) for k, v in pools.items() if len(v) != B}
    assert not fuera, f"pools incompletos: {list(fuera)[:3]}"
    out = {}
    for (sem, inst), v in pools.items():
        out[(sem, inst)] = re_mid(mejor([v[i] for i in range(B)]),
                                  lbs[inst])
    return out, lbs


def carga_politica():
    pools = collections.defaultdict(dict)
    lbs = {}
    for ruta in POL:
        for r in csv.DictReader(open(ruta, encoding="utf-8")):
            k = (r["checkpoint"], r["instance"])
            pools[k][int(r["sample_idx"])] = (float(r["lo"]), float(r["up"]))
            lbs[r["instance"]] = float(r["lb"])
    una, mc = {}, {}
    rng = np.random.RandomState(20260901)
    for (ck, inst), v in pools.items():
        n = len(v) - 1                      # muestras sin la greedy
        # una realizacion: la greedy mas las 63 primeras muestras
        una[(ck, inst)] = re_mid(
            mejor([v[0]] + [v[i] for i in range(1, B)]), lbs[inst])
        # sensibilidad: media de 200 subconjuntos de 63
        acc = []
        for _ in range(R):
            ix = rng.choice(n, B - 1, replace=False)
            acc.append(re_mid(
                mejor([v[0]] + [v[int(i) + 1] for i in ix]), lbs[inst]))
        mc[(ck, inst)] = float(np.mean(acc))
    return una, mc, lbs


def contrasta(pol, gp, instancias, etiqueta):
    """Promedia dentro de familia por instancia; la instancia es la
    unidad; Wilcoxon exacto."""
    a = np.array([np.mean([v for (c, i), v in pol.items() if i == inst])
                  for inst in instancias])
    b = np.array([np.mean([v for (s, i), v in gp.items() if i == inst])
                  for inst in instancias])
    d = a - b
    w = stats.wilcoxon(a, b, method="exact", zero_method="wilcox")
    print(f"\n== {etiqueta} ==")
    print(f"  politica {a.mean():7.3f}   regla {b.mean():7.3f}   "
          f"dif {d.mean():+.3f}")
    print(f"  la politica es mejor en {int((d < 0).sum())}/{len(d)} "
          f"instancias, p={w.pvalue:.4f}")
    return {"politica": float(a.mean()), "regla": float(b.mean()),
            "dif": float(d.mean()), "mejor_en": int((d < 0).sum()),
            "n": len(d), "p": float(w.pvalue)}


def main():
    gp, lbs = carga_gp()
    una, mc, _ = carga_politica()
    instancias = sorted({i for _, i in gp})
    assert len(instancias) == 70, f"{len(instancias)} instancias"
    n_gp = len({s for s, _ in gp})
    n_pol = len({c for c, _ in una})
    print(f"{n_pol} artefactos de politica contra {n_gp} reglas, "
          f"{len(instancias)} instancias, B={B}")

    res = {"n_politica": n_pol, "n_regla": n_gp, "B": B}
    res["realizacion"] = contrasta(una, gp, instancias,
                                   "una realizacion por artefacto")
    res["montecarlo"] = contrasta(mc, gp, instancias,
                                  f"politica como media de {R} subconjuntos")

    # dispersion entre artefactos: la media de cada uno sobre las 70
    por_pol = sorted(np.mean([v for (c, i), v in una.items() if c == ck])
                     for ck in {c for c, _ in una})
    por_gp = sorted(np.mean([v for (s, i), v in gp.items() if s == sem])
                    for sem in {s for s, _ in gp})
    res["artefactos"] = {"politica": [float(x) for x in por_pol],
                         "regla": [float(x) for x in por_gp]}
    print(f"\n  politica por artefacto: {por_pol[0]:.2f} a "
          f"{por_pol[-1]:.2f}  (mediana {np.median(por_pol):.2f})")
    print(f"  regla por artefacto:    {por_gp[0]:.2f} a "
          f"{por_gp[-1]:.2f}  (mediana {np.median(por_gp):.2f})")
    solapan = por_pol[0] <= por_gp[-1] and por_gp[0] <= por_pol[-1]
    print(f"  los rangos {'se solapan' if solapan else 'NO se solapan'}")
    res["solapan"] = bool(solapan)

    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    json.dump(res, open(SALIDA, "w", encoding="utf-8"), indent=1)
    print(f"\nescrito {SALIDA}")


if __name__ == "__main__":
    main()
