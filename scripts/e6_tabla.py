# -*- coding: utf-8 -*-
"""E6: la tabla de la comparacion a igual presupuesto, en las dos monedas.

La figura de E6 da las curvas enteras; el articulo necesita ademas una
tabla que se pueda leer sin ella, sobre el MISMO banco que la figura
(las 70 Taillard): el RE de cada metodo a unos pocos presupuestos fijos
en schedules construidos y a unos pocos tiempos fijos por instancia, y
los contrastes pareados por instancia en los tiempos que el texto cita.

Reutiliza la carga y el escalon de e6_analiza.py, de modo que los
valores coinciden con los de la figura: en el eje del reloj, el RE de
un metodo en el segundo t es el mejor que llevaba hasta t, promediado
sobre sus corridas, y un tiempo solo cuenta si las 70 instancias lo
alcanzaron (ninguna curva se prolonga mas alla de lo medido).

    python scripts/e6_tabla.py

Salida NUEVA: benchmarks/e6_presupuesto/tabla.json
"""
import json
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e6_analiza import carga, escalon                            # noqa: E402
from efecto import biserial                                      # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SALIDA = "benchmarks/e6_presupuesto/tabla.json"
METODOS = ["regla", "gt_mwkr", "regla_bon", "ga", "ga_sembrado", "azar"]
PRESUPUESTOS = [1, 1024, 8192, 131072, 1048576]
TIEMPOS = [5.0, 20.0, 50.0, 150.0, 800.0]
# los contrastes que el texto cita, en segundos
CONTRASTES = [("regla", "ga", 20.0), ("regla", "ga", 50.0),
              ("regla_bon", "ga", 50.0), ("ga_sembrado", "ga", 20.0),
              ("regla_bon", "ga", 150.0), ("ga_sembrado", "regla_bon", 150.0),
              ("regla_bon", "ga", 800.0), ("ga_sembrado", "regla_bon", 800.0)]


def carga_completa():
    """Las curvas de E6 con las de la extension (e6_extension.py) en lugar
    de las originales para el genetico y el mejor-de-N, alli donde la
    extension ya ha corrido. Las semillas son las mismas, asi que en los
    presupuestos comunes el RE tiene que coincidir: si no, se aborta."""
    import csv
    import glob
    d = carga()
    # primero la extension 1 y luego la 2 (e6_extension2.py); una curva
    # sustituye a la que habia solo si llega al menos igual de lejos
    for patron in ("curva_ext_carril*.csv", "curva_ext2_carril*.csv",
                   "curva_ext3_carril*.csv"):
        ext = {}
        for f in sorted(glob.glob(os.path.join(
                "benchmarks/e6_presupuesto", patron))):
            for r in csv.DictReader(open(f, encoding="utf-8")):
                ext.setdefault((r["metodo"], r["instancia"],
                                int(r["semilla"])), []).append(
                    (int(r["presupuesto"]), float(r["re"]),
                     float(r["segundos"])))
        for (m, i, s), puntos in ext.items():
            viejo = {p: re for p, re, _ in d[m][i].get(s, [])}
            for p, re, _ in puntos:
                if p in viejo:
                    assert abs(viejo[p] - re) < 1e-3, (m, i, s, p, viejo[p], re)
            if not viejo or max(p for p, _, _ in puntos) >= max(viejo):
                d[m][i][s] = sorted(puntos)
    return d


def por_instancia_presupuesto(d, m, b, insts):
    """RE por instancia al presupuesto b, media sobre corridas; None si
    el metodo no llego a b en alguna instancia."""
    out = []
    for i in insts:
        v = [re for s in d[m][i] for (p, re, _) in d[m][i][s] if p == b]
        if not v:
            return None
        out.append(float(np.mean(v)))
    return out


def por_instancia_tiempo(d, m, t, insts):
    """RE por instancia en el segundo t. La regla de una pasada no mejora
    despues de terminar: su valor vale para todo t posterior a su tiempo."""
    out = []
    for i in insts:
        if m in ("regla", "gt_mwkr"):
            (p, re, seg), = d[m][i][0]
            if seg > t:
                return None
            out.append(re)
            continue
        v = [escalon(d[m][i][s], t) for s in d[m][i]]
        v = [x for x in v if not np.isnan(x)]
        if not v:
            return None
        out.append(float(np.mean(v)))
    return out


def contraste(x, y):
    x, y = np.asarray(x), np.asarray(y)
    dif = x - y
    w = stats.wilcoxon(x, y, method="exact", zero_method="wilcox")
    n = int(np.sum(np.abs(dif) > 1e-12))
    z = (w.statistic - n * (n + 1) / 4) / (n * (n + 1) * (2 * n + 1) / 24) ** 0.5
    z = abs(z) if dif.mean() > 0 else -abs(z)
    return {"d": float(dif.mean()), "p": float(w.pvalue), "z": float(z),
            "rb": biserial(list(x), list(y)), "menor": int(np.sum(dif < 0)),
            "n": len(dif)}


def main():
    d = carga_completa()
    insts = sorted(d["ga"])
    assert len(insts) == 70, len(insts)
    res = {"presupuestos": PRESUPUESTOS, "tiempos": TIEMPOS,
           "por_presupuesto": {}, "por_tiempo": {}, "contrastes": {},
           "corridas": {m: len(next(iter(d[m].values()))) for m in METODOS},
           "segundos_una_pasada": {}}

    for m in ("regla", "gt_mwkr"):
        segs = [d[m][i][0][0][2] for i in insts]
        res["segundos_una_pasada"][m] = {"media": float(np.mean(segs)),
                                         "max": float(np.max(segs))}

    print(f"{'':12}" + "".join(f"{b:>9}" for b in PRESUPUESTOS)
          + " |" + "".join(f"{t:>8}s" for t in TIEMPOS))
    for m in METODOS:
        fila_b, fila_t = {}, {}
        for b in PRESUPUESTOS:
            v = por_instancia_presupuesto(d, m, b, insts)
            if v is not None:
                fila_b[str(b)] = float(np.mean(v))
        for t in TIEMPOS:
            v = por_instancia_tiempo(d, m, t, insts)
            if v is not None:
                fila_t[str(t)] = float(np.mean(v))
        res["por_presupuesto"][m] = fila_b
        res["por_tiempo"][m] = fila_t
        print(f"{m:12}"
              + "".join(f"{fila_b[str(b)]:9.2f}" if str(b) in fila_b
                        else f"{'-':>9}" for b in PRESUPUESTOS) + " |"
              + "".join(f"{fila_t[str(t)]:9.2f}" if str(t) in fila_t
                        else f"{'-':>9}" for t in TIEMPOS))

    print()
    for a, b, t in CONTRASTES:
        c = contraste(por_instancia_tiempo(d, a, t, insts),
                      por_instancia_tiempo(d, b, t, insts))
        res["contrastes"][f"{a} vs {b} a {t}s"] = c
        print(f"  {a} vs {b} a {t:g} s: d={c['d']:+.2f} z={c['z']:+.2f} "
              f"p={c['p']:.1e} r={c['rb']:.2f} menor en {c['menor']}/70")
    # donde el sembrado alcanza al mejor-de-N en segundos, en una rejilla
    # fina: el primer tiempo en que su media queda por debajo
    cruce = None
    for s in np.logspace(0, np.log10(TIEMPOS[-1]), 120):
        a = por_instancia_tiempo(d, "ga_sembrado", float(s), insts)
        b = por_instancia_tiempo(d, "regla_bon", float(s), insts)
        if a and b and np.mean(a) < np.mean(b):
            cruce = float(s)
            break
    res["cruce_sembrado_bon_s"] = cruce
    print(f"\n  el sembrado alcanza al mejor-de-N a los {cruce} s")
    print(f"\n  una pasada: {res['segundos_una_pasada']}")
    print(f"  corridas por instancia: {res['corridas']}")
    json.dump(res, open(SALIDA, "w", encoding="utf-8"), indent=1)
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
