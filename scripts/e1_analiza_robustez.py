# -*- coding: utf-8 -*-
"""E1: la robustez sin el efecto del denominador, y bajo otras realizaciones.

La revision r3 del envio a SWEVO objeta que eps-barra va normalizada por
E[Cmax] y que el brazo robusto tiene un RE mucho mas alto, de modo que
parte de la mejora reportada podria ser del denominador y no del
schedule. Objeta ademas que la medida descansa sobre un muestreo
uniforme que el modelo intervalar no asume.

Este script lee los depositos que produce robustness_epsilon.py con
--dist y responde a las dos cosas:

  - la desviacion ABSOLUTA junto a la normalizada, por metodo;
  - las dos bajo uniforme, triangular, sesgada al extremo alto y caso
    peor, para ver si el orden entre metodos sobrevive al modelo;
  - el contraste pareado por instancia, que es la unidad del articulo.

    python scripts/e1_analiza_robustez.py

Salida NUEVA: benchmarks/e1_robustez/resumen.json
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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from efecto import biserial                                    # noqa: E402

DIR = "benchmarks/e1_robustez"
SALIDA = os.path.join(DIR, "resumen.json")
ORDEN = ["GP", "GP-nowidth", "GP-rob1", "GP-rob1-nw", "GP-rob4",
         "GT-MWKR", "EST"]
# los contrastes que el articulo sostiene y que la objecion pone en duda
PARES = [("GP", "GP-nowidth"), ("GP-rob1", "GP"), ("GP-rob1", "GP-rob1-nw"),
         ("GP-rob4", "GP"), ("GP", "GT-MWKR"), ("GP", "EST"),
         # r3.2 pide ademas comparar a niveles de RE parecidos: el brazo
         # robusto lam=4 (28.27 de RE) y G&T-MWKR (29.50) estan casi
         # empatados en makespan esperado, asi que su contraste en
         # desviacion aisla la robustez de la calidad a priori
         ("GP-rob4", "GT-MWKR")]


def carga(ruta):
    """{metodo: {instancia: (eps_x1000, abs_dev, e_mid)}} a anchura nominal."""
    d = collections.defaultdict(dict)
    for r in csv.DictReader(open(ruta, encoding="utf-8")):
        if float(r["width"]) != 1.0:
            continue
        d[r["method"]][r["instance"]] = (float(r["eps_bar"]),
                                         float(r["abs_dev"]),
                                         float(r["e_mid"]))
    return d


def pareado(a, b, insts, k):
    x = np.array([a[i][k] for i in insts])
    y = np.array([b[i][k] for i in insts])
    dif = x - y
    if not np.any(np.abs(dif) > 1e-12):
        return 0.0, 1.0, 0.0, 0.0, 0.0
    w = stats.wilcoxon(x, y, method="exact", zero_method="wilcox")
    # z y tamano del efecto, en el formato que usa el articulo
    n = int(np.sum(np.abs(dif) > 1e-12))
    mu = n * (n + 1) / 4.0
    sd = (n * (n + 1) * (2 * n + 1) / 24.0) ** 0.5
    z = (float(w.statistic) - mu) / sd if sd > 0 else 0.0
    if dif.mean() > 0:
        z = abs(z)
    else:
        z = -abs(z)
    # el cuarto valor es |z|/sqrt(n), que se conserva por compatibilidad
    # con lo ya citado en paper_gp; el quinto es la biserial por rangos,
    # que es el |r| que define el articulo
    return (float(dif.mean()), float(w.pvalue), z, abs(z) / n ** 0.5,
            biserial(list(x), list(y)))


def main():
    ficheros = {os.path.basename(f)[:-4]: f
                for f in sorted(glob.glob(os.path.join(DIR, "*.csv")))}
    if not ficheros:
        sys.exit(f"no hay depositos en {DIR}: lanza robustness_epsilon.py "
                 f"con --dist primero")
    print(f"distribuciones: {', '.join(sorted(ficheros))}\n")

    res = {}
    for dist in sorted(ficheros):
        d = carga(ficheros[dist])
        metodos = [m for m in ORDEN if m in d]
        insts = sorted(set.intersection(*(set(d[m]) for m in metodos)))
        print(f"== {dist} ({len(insts)} instancias) ==")
        print(f"  {'metodo':<12} {'eps x1e3':>9} {'abs':>9} {'E[Cmax]':>9}")
        tabla = {}
        for m in metodos:
            e = np.mean([d[m][i][0] for i in insts])
            a = np.mean([d[m][i][1] for i in insts])
            c = np.mean([d[m][i][2] for i in insts])
            tabla[m] = {"eps": float(e), "abs": float(a), "e_mid": float(c)}
            print(f"  {m:<12} {e:9.2f} {a:9.2f} {c:9.1f}")

        print(f"\n  {'contraste':<26} {'d eps':>8} {'p':>8} "
              f"{'d abs':>9} {'p':>8}")
        contrastes = {}
        for x, y in PARES:
            if x not in d or y not in d:
                continue
            de, pe, ze, re_, rbe = pareado(d[x], d[y], insts, 0)
            da, pa, za, ra, rba = pareado(d[x], d[y], insts, 1)
            contrastes[f"{x} vs {y}"] = {"d_eps": de, "p_eps": pe,
                                         "d_abs": da, "p_abs": pa,
                                         "z_eps": ze, "r_eps": re_,
                                         "z_abs": za, "r_abs": ra,
                                         "rb_eps": rbe, "rb_abs": rba}
            aviso = "  <-- cambia de signo" if de * da < 0 else ""
            print(f"  {x + ' vs ' + y:<26} {de:8.2f} {pe:8.4f} "
                  f"{da:9.2f} {pa:8.4f}  z={za:+6.2f} r={ra:.2f}{aviso}")
        res[dist] = {"metodos": tabla, "contrastes": contrastes,
                     "n_instancias": len(insts)}
        print()

    json.dump(res, open(SALIDA, "w", encoding="utf-8"), indent=1)
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
