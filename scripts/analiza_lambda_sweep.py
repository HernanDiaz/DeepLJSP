# -*- coding: utf-8 -*-
"""La frontera de lambda con la seleccion separada del entrenamiento.

Del deposito de rollouts de cada brazo (base y lam1 en rollouts.csv;
lam0p5, lam2 y lam4 en rollouts_sweep.csv) se reconstruyen dos
mejores-de-64 por (brazo, semilla, instancia):

  * seleccion FIJA: elige por cota superior, el criterio del paper,
    identico para todos los brazos. Lo que cambie aqui solo puede
    venir del entrenamiento -- de la distribucion que la politica
    aprendio a proponer.
  * seleccion PROPIA: elige por el f_lambda del brazo (up + lam*(up-lo)).
    Es el paquete desplegado completo, entrenamiento mas criterio.

Para cada uno, RE del punto medio y ancho relativo (up-lo)/mid, en %,
sobre TA15-TA20 (desarrollo), pareado contra base por (semilla,
instancia): 18 pares por brazo.

    python scripts/analiza_lambda_sweep.py
"""
import collections
import csv
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FICHEROS = ["benchmarks/robust_lambda/rollouts.csv",
            "benchmarks/robust_lambda/rollouts_sweep.csv"]
LAMBDAS = {"base": 0.0, "lam0p5": 0.5, "lam1": 1.0, "lam2": 2.0,
           "lam4": 4.0}
ORDEN = ["base", "lam0p5", "lam1", "lam2", "lam4"]


def carga():
    d = collections.defaultdict(list)
    lbs = {}
    for ruta in FICHEROS:
        with open(ruta, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                k = (r["arm"], int(r["seed"]), r["instance"])
                d[k].append((float(r["lower"]), float(r["upper"])))
                lbs[r["instance"]] = float(r["lb"])
    return d, lbs


def mejor(rollouts, lam):
    if lam == 0.0:
        return min(rollouts, key=lambda t: (t[1], t[0]))
    return min(rollouts, key=lambda t: t[1] + lam * (t[1] - t[0]))


def metricas(pares_sel, lbs):
    re = [((lo + up) / 2 - lbs[k[2]]) / lbs[k[2]] * 100
          for k, (lo, up) in pares_sel]
    anc = [(up - lo) / ((lo + up) / 2) * 100 for _, (lo, up) in pares_sel]
    return sum(re) / len(re), sum(anc) / len(anc)


def main():
    d, lbs = carga()
    n_por_brazo = collections.Counter(k[0] for k in d)
    print("combinaciones por brazo:", dict(n_por_brazo), "\n")

    sel = {}   # (modo, brazo) -> {clave: (lo, up)}
    for modo in ("fija", "propia"):
        print(f"=== seleccion {modo} "
              f"({'cota superior para todos' if modo == 'fija' else 'f_lambda de cada brazo'}) ===")
        for brazo in ORDEN:
            lam = 0.0 if modo == "fija" else LAMBDAS[brazo]
            filas = [(k, mejor(v, lam)) for k, v in d.items()
                     if k[0] == brazo]
            sel[(modo, brazo)] = {k: v for k, v in filas}
            re, anc = metricas(filas, lbs)
            print(f"  {brazo:6s}: RE {re:6.2f}%   ancho rel {anc:6.2f}%   "
                  f"(n={len(filas)})")
        print()

    # contraste pareado contra base, mismo modo de seleccion
    try:
        from scipy import stats
    except ImportError:
        stats = None
    base_f = sel[("fija", "base")]
    base_p = sel[("propia", "base")]   # identico a fija (lam base = 0)
    for modo, ref in (("fija", base_f), ("propia", base_p)):
        print(f"=== pareado contra base, seleccion {modo} ===")
        for brazo in ORDEN[1:]:
            cur = sel[(modo, brazo)]
            d_re, d_anc = [], []
            for k, (lo1, up1) in sorted(cur.items()):
                k0 = ("base", k[1], k[2])
                lo0, up0 = ref[k0]
                m0, m1 = (lo0 + up0) / 2, (lo1 + up1) / 2
                d_re.append((m1 - m0) / lbs[k[2]] * 100)
                d_anc.append((up1 - lo1) / m1 * 100 - (up0 - lo0) / m0 * 100)
            linea = (f"  {brazo:6s}: dRE {sum(d_re)/len(d_re):+6.2f}   "
                     f"dancho {sum(d_anc)/len(d_anc):+6.2f}   "
                     f"(estrecho en {sum(x < 0 for x in d_anc)}/{len(d_anc)})")
            if stats is not None:
                linea += (f"   p_RE={stats.wilcoxon(d_re)[1]:.3g}"
                          f"   p_anc={stats.wilcoxon(d_anc)[1]:.3g}")
            print(linea)
        print()


if __name__ == "__main__":
    main()
