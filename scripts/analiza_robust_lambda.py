# -*- coding: utf-8 -*-
"""Que compra el objetivo robusto: RE frente a ancho del intervalo.

Del deposito de rollouts (scripts/eval_robust_lambda.py) se reconstruyen
DOS mejores-de-64 por (brazo, semilla, instancia): el que elige por cota
superior, que es el criterio del paper, y el que elige por el valor
robusto up + (up - lo), que es el criterio con el que el brazo lam1 fue
entrenado. Para cada uno se mide la RE del punto medio y el ancho
relativo (up - lo)/mid, que es la magnitud que lambda pretende encoger.

    python scripts/analiza_robust_lambda.py
"""
import collections
import csv
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ENTRADA = "benchmarks/robust_lambda/rollouts.csv"
LAM = 1.0


def carga():
    d = collections.defaultdict(list)
    lbs = {}
    with open(ENTRADA, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            k = (r["arm"], int(r["seed"]), r["instance"])
            d[k].append((float(r["lower"]), float(r["upper"])))
            lbs[r["instance"]] = float(r["lb"])
    return d, lbs


def mejor(rollouts, criterio):
    if criterio == "upper":
        return min(rollouts, key=lambda t: (t[1], t[0]))
    return min(rollouts, key=lambda t: t[1] + LAM * (t[1] - t[0]))


def main():
    d, lbs = carga()
    print(f"{len(d)} combinaciones (brazo, semilla, instancia), "
          f"{len(next(iter(d.values())))} rollouts cada una\n")

    res = {}
    for criterio in ("upper", "robust"):
        for brazo in ("base", "lam1"):
            filas = [(k, mejor(v, criterio)) for k, v in d.items()
                     if k[0] == brazo]
            re = [((lo + up) / 2 - lbs[k[2]]) / lbs[k[2]] * 100
                  for k, (lo, up) in filas]
            anc = [(up - lo) / ((lo + up) / 2) * 100 for _, (lo, up) in filas]
            res[(criterio, brazo)] = {k: (lo, up) for k, (lo, up) in filas}
            print(f"seleccion por {criterio:6s} | {brazo:4s}: "
                  f"RE {sum(re)/len(re):6.2f}%   "
                  f"ancho relativo {sum(anc)/len(anc):6.2f}%   (n={len(re)})")
        print()

    # el contraste que importa: mismo criterio de seleccion, distinto
    # entrenamiento. Emparejado por (semilla, instancia), 18 pares.
    for criterio in ("upper", "robust"):
        a, b = res[(criterio, "base")], res[(criterio, "lam1")]
        pares = sorted(k[1:] for k in a)
        d_re, d_anc = [], []
        for s, inst in pares:
            (lo0, up0), (lo1, up1) = a[("base", s, inst)], b[("lam1", s, inst)]
            m0, m1 = (lo0 + up0) / 2, (lo1 + up1) / 2
            d_re.append((m1 - m0) / lbs[inst] * 100)
            d_anc.append((up1 - lo1) / m1 * 100 - (up0 - lo0) / m0 * 100)
        print(f"pareado, seleccion por {criterio}: lam1 - base sobre "
              f"{len(pares)} pares")
        print(f"   RE     {sum(d_re)/len(d_re):+6.2f} puntos "
              f"(peor en {sum(x > 0 for x in d_re)}/{len(d_re)})")
        print(f"   ancho  {sum(d_anc)/len(d_anc):+6.2f} puntos "
              f"(mas estrecho en {sum(x < 0 for x in d_anc)}/{len(d_anc)})")
        try:
            from scipy import stats
            print(f"   Wilcoxon RE     p={stats.wilcoxon(d_re)[1]:.3g}")
            print(f"   Wilcoxon ancho  p={stats.wilcoxon(d_anc)[1]:.3g}")
        except ImportError:
            print("   (sin scipy)")
        print()


if __name__ == "__main__":
    main()
