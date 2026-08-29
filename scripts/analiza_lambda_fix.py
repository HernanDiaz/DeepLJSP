# -*- coding: utf-8 -*-
"""La frontera de lambda a DIEZ semillas, con sus tres lecturas.

Funde los depositos originales (rollouts.csv: base y lam1 a semillas
2-4; rollouts_sweep.csv: lam0p5/2/4 a 2-4) con los de la ampliacion
(rollouts_ext_*.csv: los cinco brazos a 5-11) y reconstruye, por
(brazo, semilla, instancia), el mejor-de-64 bajo:

  * seleccion PROPIA: el f_lambda del brazo -- el paquete desplegado.
  * seleccion FIJA: la cota superior para todos -- lo que cambie solo
    puede venir de los pesos.
  * RERANK: los depositos del brazo BASE re-rankeados por el f_lambda
    de cada brazo -- la frontera sin reentrenar nada.

La unidad del test es la instancia: las semillas se promedian antes
del Wilcoxon exacto bilateral (6 instancias de desarrollo).

Salida NUEVA: benchmarks/robust_lambda/frontera_diez.json

    python scripts/analiza_lambda_diez.py
"""
import collections
import csv
import glob
import json
import statistics
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from scipy import stats                                        # noqa: E402

# los brazos lambda>0 salen del deposito de las tiradas con la clave
# componente a componente; el brazo base es el mismo de siempre, que
# no depende de lambda y por tanto no cambia
FICHEROS = (["benchmarks/robust_lambda/rollouts.csv",
             "benchmarks/robust_lambda/rollouts_sweep.csv"]
            + sorted(glob.glob("benchmarks/robust_lambda/rollouts_ext_*.csv"))
            + sorted(glob.glob(
                "benchmarks/robust_lambda_fix/rollouts_*.csv")))
LAMBDAS = {"base": 0.0, "lam0p5": 0.5, "lam1": 1.0, "lam2": 2.0,
           "lam4": 4.0}
ORDEN = ["base", "lam0p5", "lam1", "lam2", "lam4"]
SALIDA = "benchmarks/robust_lambda_fix/frontera_fix.json"


def carga():
    d = collections.defaultdict(list)
    lbs = {}
    for ruta in FICHEROS:
        nuevo = "robust_lambda_fix" in ruta.replace("\\", "/")
        for r in csv.DictReader(open(ruta, encoding="utf-8")):
            # base solo del deposito viejo; lambda>0 solo del nuevo
            if (r["arm"] == "base") == nuevo:
                continue
            k = (r["arm"], int(r["seed"]), r["instance"])
            d[k].append((float(r["lower"]), float(r["upper"])))
            lbs[r["instance"]] = float(r["lb"])
    # los CSV reanudables pueden traer bloques repetidos: cada pool son
    # los 64 primeros
    return {k: v[:64] for k, v in d.items()}, lbs


def mejor(rollouts, lam):
    if lam == 0.0:
        return min(rollouts, key=lambda t: (t[1], t[0]))
    return min(rollouts, key=lambda t: t[1] + lam * (t[1] - t[0]))


def por_instancia(sel, lbs):
    """Media sobre semillas por instancia: RE del punto medio y ancho."""
    re_i, anc_i = collections.defaultdict(list), collections.defaultdict(list)
    for (arm, s, inst), (lo, up) in sel.items():
        mid = (lo + up) / 2
        re_i[inst].append((mid - lbs[inst]) / lbs[inst] * 100)
        anc_i[inst].append((up - lo) / mid * 100)
    return ({i: statistics.mean(v) for i, v in re_i.items()},
            {i: statistics.mean(v) for i, v in anc_i.items()})


def main():
    d, lbs = carga()
    por_brazo = collections.Counter(k[0] for k in d)
    print("pools por brazo:", dict(por_brazo))
    res = {"pools_por_brazo": dict(por_brazo), "modos": {}}

    selecciones = {}
    for modo in ("propia", "fija", "rerank"):
        res["modos"][modo] = {}
        for brazo in ORDEN:
            lam = LAMBDAS[brazo] if modo in ("propia", "rerank") else 0.0
            if modo == "rerank":
                filas = {("base", k[1], k[2]): mejor(v, lam)
                         for k, v in d.items() if k[0] == "base"}
            else:
                filas = {k: mejor(v, lam) for k, v in d.items()
                         if k[0] == brazo}
            selecciones[(modo, brazo)] = filas
            re_i, anc_i = por_instancia(filas, lbs)
            entrada = {"re": round(statistics.mean(re_i.values()), 4),
                       "ancho": round(statistics.mean(anc_i.values()), 4),
                       "n_pools": len(filas)}
            # contraste pareado contra base por instancia
            if brazo != "base":
                ref = selecciones[(modo, "base")]
                re0, anc0 = por_instancia(ref, lbs)
                d_re = [re_i[i] - re0[i] for i in sorted(re_i)]
                d_anc = [anc_i[i] - anc0[i] for i in sorted(anc_i)]
                entrada.update({
                    "d_re": round(statistics.mean(d_re), 4),
                    "d_ancho": round(statistics.mean(d_anc), 4),
                    "estrecho_en": sum(1 for x in d_anc if x < 0),
                    "p_re": float(stats.wilcoxon(d_re, method="exact").pvalue),
                    "p_ancho": float(stats.wilcoxon(d_anc, method="exact").pvalue)})
            res["modos"][modo][brazo] = entrada
            extra = ""
            if brazo != "base":
                extra = (f"  dRE {entrada['d_re']:+6.2f} "
                         f"(p={entrada['p_re']:.3f})  "
                         f"dancho {entrada['d_ancho']:+6.2f} "
                         f"(p={entrada['p_ancho']:.3f})  "
                         f"estrecho {entrada['estrecho_en']}/6")
            print(f"  {modo:6s} {brazo:6s}: RE {entrada['re']:6.2f}  "
                  f"ancho {entrada['ancho']:6.2f}  n={entrada['n_pools']}"
                  + extra)
        print()

    json.dump(res, open(SALIDA, "w", encoding="utf-8"), indent=2)
    print("escrito", SALIDA)


if __name__ == "__main__":
    main()
