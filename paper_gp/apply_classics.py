# -*- coding: utf-8 -*-
"""Vuelca benchmarks/classic12_tuned.csv en tab:classics y recalcula el
Wilcoxon GP-eps(1024) contra el GA publicado.

La comparacion con el GA es la afirmacion mas expuesta de la seccion, asi que
el script la RECALCULA en vez de dar por bueno el z anterior, e imprime en
claro si sigue siendo no significativa.

Uso: python paper_gp/apply_classics.py [--dry]
"""

import argparse
import csv
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CSV = os.path.join(REPO, "benchmarks/classic12_tuned.csv")
TEX = os.path.join(HERE, "main.tex")
LB = {"ABZ7": 656, "ABZ8": 645, "ABZ9": 661, "FT10": 930, "FT20": 1165,
      "La21": 1046, "La24": 935, "La25": 977, "La27": 1235, "La29": 1152,
      "La38": 1196, "La40": 1222}
ORDER = ["FT10", "FT20", "La21", "La24", "La25", "La27", "La29", "La38",
         "La40", "ABZ7", "ABZ8", "ABZ9"]


def wilcoxon(d):
    d = [x for x in d if abs(x) > 1e-12]
    n = len(d)
    if n < 6:
        return float("nan"), n
    r = sorted(d, key=abs)
    rk = {}
    i = 0
    while i < n:
        j = i
        while j + 1 < n and abs(abs(r[j + 1]) - abs(r[i])) < 1e-12:
            j += 1
        rr = (i + j) / 2 + 1
        for k in range(i, j + 1):
            rk[id(r[k])] = rr
        i = j + 1
    wp = sum(rk[id(x)] for x in r if x > 0)
    mu = n * (n + 1) / 4
    sd = (n * (n + 1) * (2 * n + 1) / 24) ** 0.5
    return (wp - mu) / sd, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()
    if not os.path.exists(CSV):
        sys.exit(f"todavia no existe {CSV}")

    rows = {r["inst"]: r for r in csv.DictReader(open(CSV, encoding="utf-8"))}
    missing = [i for i in ORDER if i not in rows]
    if missing:
        sys.exit(f"faltan instancias: {missing}")

    def mean(c):
        return sum(float(rows[i][c]) for i in ORDER) / len(ORDER)

    print(f"{'inst':<7}{'GP':>7}{'GPe64':>8}{'GPe1024':>9}{'GA':>7}")
    for i in ORDER:
        r = rows[i]
        print(f"{i:<7}{float(r['gp']):>7.1f}{float(r['gp64']):>8.1f}"
              f"{float(r['gp1024']):>9.1f}{float(r['GA']):>7.1f}")
    for c in ("gp", "gp64", "gp1024", "GA"):
        print(f"  media {c:<8}{mean(c):.2f}")

    z, n = wilcoxon([float(rows[i]["gp1024"]) - float(rows[i]["GA"])
                     for i in ORDER])
    sig = abs(z) > 1.96
    print(f"\nWilcoxon GP-eps(1024) vs GA: z={z:.2f} (n={n})  -> "
          + ("DIFERENCIA SIGNIFICATIVA" if sig else "no significativa"))
    if sig:
        peor = mean("gp1024") > mean("GA")
        print("  ATENCION: la afirmacion 'matches the published average of a"
              f" genetic algorithm' YA NO SE SOSTIENE (GP-eps es "
              f"{'peor' if peor else 'mejor'}).")

    if args.dry:
        return

    tex = open(TEX, encoding="utf-8").read()
    body = []
    for i in ORDER:
        r = rows[i]
        body.append(f"{i} & {LB[i]} & & {float(r['gp']):.1f} & "
                    f"{float(r['gp64']):.1f} & {float(r['gp1024']):.1f} & "
                    f"{float(r['GA']):.1f} & {float(r['ABCE3']):.1f} & "
                    f"{float(r['fEABC']):.1f} & {float(r['ESABC']):.1f} \\\\")
    body.append("\\midrule")
    body.append("Mean & & & " + " & ".join(
        f"{mean(c):.1f}" for c in ("gp", "gp64", "gp1024", "GA", "ABCE3",
                                   "fEABC", "ESABC")) + " \\\\")

    lab = tex.index("\\label{tab:classics}")
    a = tex.index("\\midrule", lab) + len("\\midrule")
    b = tex.index("\\bottomrule", a)
    tex = tex[:a] + "\n" + "\n".join(body) + "\n" + tex[b:]
    open(TEX, "w", encoding="utf-8", newline="\n").write(tex)
    print("\ntab:classics actualizada")
    print("pendiente a mano: el texto de 6.4 cita 13.9 / 11.9 / 9.9 y el z"
          " del GA; revisalo con las cifras de arriba")


if __name__ == "__main__":
    main()
