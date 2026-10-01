# -*- coding: utf-8 -*-
"""Cifras de la seccion 6.5 (E6 version 2): presupuesto en segundos.

Cuatro conjuntos, los cuatro paneles de la figura: las 12 clasicas (30
corridas de 900 s, e6c_clasicas.py) y las clases 15x15, 30x15 y 50x15 de
Taillard (3 corridas, horizontes de 900, 1800 y 3600 s, e6t_clases.py).
Todo con la solucion en curso de cada corrida (e6_tabla.incumbente),
media sobre las corridas de cada instancia y despues sobre instancias.

  - RE de cada metodo en 1, 10 y 100 s y al final del horizonte;
  - cruces: desde que instante de la rejilla una curva queda por debajo
    de otra HASTA EL FINAL (no la primera vez que la toca);
  - desde cuando el genetico sin sembrar iguala a la pasada unica;
  - contrastes al final (Wilcoxon pareado de dos colas, exacto, la
    instancia como unidad; |r| biserial de rangos);
  - el genetico frente al sembrado en varios instantes, y en las 42
    instancias juntas al final;
  - el coste por schedule de cada metodo, del ultimo punto de cada
    corrida (con seis procesos a la vez, la carga del experimento);
  - en las clasicas, el RE del genetico a 2^19 schedules y el instante en
    que alcanza la media publicada del genetico original.

    python scripts/e6_v2_resumen.py

Salida NUEVA: benchmarks/e6_v2/resumen.json
"""
import json
import os
import sys

import numpy as np
from scipy.stats import wilcoxon

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_e6c_figure as fc                      # noqa: E402
import make_e6_tamanos_figure as ft               # noqa: E402
from e6_tabla import incumbente                   # noqa: E402

SALIDA = "benchmarks/e6_v2/resumen.json"
BUSQUEDA = ("regla_bon", "ga", "ga_sembrado", "azar")
INSTANTES_SEMILLA = (1, 3, 10, 30, 100, 300, 1000)


def conjuntos():
    ec = fc.modulo_clasicas()
    dc, dt = fc.carga(), ft.carga()
    yield "clasicas", dc, list(ec.FILES), 900.0
    for clase, h in (("15_15", 900.0), ("30_15", 1800.0), ("50_15", 3600.0)):
        yield clase, dt, [f"int__tai{clase}_{k:02d}" for k in range(1, 11)], h


def por_instancia(d, m, insts, t):
    out = []
    for i in insts:
        w = [incumbente(p, t) for p in d[m][i].values()]
        w = [x for x in w if not np.isnan(x)]
        out.append(np.mean(w) if w else np.nan)
    return np.array(out)


def contraste(a, b):
    """Wilcoxon de dos colas de a frente a b, por instancia."""
    dif = a - b
    rk = np.argsort(np.argsort(np.abs(dif))) + 1
    wp, wn = rk[dif > 0].sum(), rk[dif < 0].sum()
    return {"p": float(wilcoxon(a, b).pvalue), "a_mejor": int((a < b).sum()),
            "n": int(len(a)), "r": float(abs(wp - wn) / (wp + wn)),
            "media_a": float(a.mean()), "media_b": float(b.mean())}


def cruce(d, insts, a, b, rejilla, nivel_b=None):
    """Primer t de la rejilla desde el que la media de a queda por debajo
    de la de b (o del nivel fijo nivel_b) en todos los t posteriores."""
    debajo = []
    for t in rejilla:
        ma = por_instancia(d, a, insts, t).mean()
        mb = nivel_b if nivel_b is not None else por_instancia(d, b, insts, t).mean()
        debajo.append(ma < mb)
    if not debajo[-1]:
        return None
    k = len(debajo) - 1
    while k > 0 and debajo[k - 1]:
        k -= 1
    return float(rejilla[k])


def main():
    res, A, B = {}, [], []
    for nombre, d, insts, h in conjuntos():
        fin = h - 1.0
        rejilla = np.logspace(-2, np.log10(fin), 300)
        r = {"instancias": len(insts), "horizonte": h,
             "corridas": {m: int(sum(len(d[m][i]) for i in insts))
                          for m in BUSQUEDA}}
        r["re"] = {str(t): {m: float(por_instancia(d, m, insts, float(t)).mean())
                            for m in BUSQUEDA}
                   for t in (1, 10, 100)}
        r["re"]["final"] = {m: float(por_instancia(d, m, insts, fin).mean())
                            for m in BUSQUEDA}
        pasada = float(np.mean([d["regla"][i][0][0][1] for i in insts]))
        r["pasada"] = {"regla": pasada, "gt_mwkr": float(np.mean(
            [d["gt_mwkr"][i][0][0][1] for i in insts]))}
        r["cruce"] = {
            "sembrado_bon": cruce(d, insts, "ga_sembrado", "regla_bon", rejilla),
            "ga_bon": cruce(d, insts, "ga", "regla_bon", rejilla),
            "ga_pasada": cruce(d, insts, "ga", None, rejilla, nivel_b=pasada)}
        fa = {m: por_instancia(d, m, insts, fin) for m in BUSQUEDA}
        r["final"] = {"sembrado_bon": contraste(fa["ga_sembrado"], fa["regla_bon"]),
                      "ga_bon": contraste(fa["ga"], fa["regla_bon"]),
                      "sembrado_ga": contraste(fa["ga_sembrado"], fa["ga"])}
        r["semilla"] = {}
        for t in INSTANTES_SEMILLA + (fin,):
            if t > fin:
                continue
            clave = "final" if t == fin else str(t)
            r["semilla"][clave] = contraste(
                por_instancia(d, "ga_sembrado", insts, float(t)),
                por_instancia(d, "ga", insts, float(t)))
        A += list(fa["ga_sembrado"])
        B += list(fa["ga"])
        # ms por schedule: el ultimo punto de cada corrida
        r["ms_schedule"] = {}
        for m in ("regla_bon", "ga", "ga_sembrado"):
            v = [seg / p * 1000 for i in insts for pts in d[m][i].values()
                 for p, _, seg in pts[-1:]]
            r["ms_schedule"][m] = float(np.mean(v))
        if nombre == "clasicas":
            ec = fc.modulo_clasicas()
            pub = {k: float(np.mean([ec.PUB_AVG[i][k] for i in insts]))
                   for k in ("GA", "ESABC")}
            r["publicado"] = pub
            r["ga_2_19"] = float(np.mean([np.mean([dict((p, re) for p, re, _ in pts)
                                                   [2 ** 19] for pts in d["ga"][i].values()])
                                          for i in insts]))
            r["cruce"]["ga_publicado"] = cruce(d, insts, "ga", None, rejilla,
                                               nivel_b=pub["GA"])
        res[nombre] = r
        print(nombre, json.dumps(r["cruce"]), {k: round(v["p"], 4)
                                                 for k, v in r["final"].items()})
    res["semilla_42"] = contraste(np.array(A), np.array(B))
    print("42:", res["semilla_42"])
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    json.dump(res, open(SALIDA, "w", encoding="utf-8"), indent=1)
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
