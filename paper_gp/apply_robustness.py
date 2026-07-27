# -*- coding: utf-8 -*-
"""Vuelca la eps-robustez de la campana tuneada en tab:robustness y en 7.3.

Lee benchmarks/robustness_tuned.csv, que scripts/robustness_epsilon.py escribe
en UNA sola ejecucion con los cuatro metodos. Eso resuelve el problema que
tenia la seccion: la tabla salia de robustness_eps.csv y la figura de
robustness_ablation.csv, que eran reglas GP distintas.

Anade ademas la fila GP-nowidth a la tabla (la figura ya la mostraba) y el
Wilcoxon pareado sobre las 70 instancias, que no habia.

Uso: python paper_gp/apply_robustness.py [--dry]
"""

import argparse
import csv
import os
import sys
from collections import defaultdict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CSV = os.path.join(REPO, "benchmarks/robustness_tuned.csv")
TEX = os.path.join(HERE, "main.tex")

ORDER = ["GP", "GP-nowidth", "GT-MWKR", "MOR"]
SHOWN = {"GP": "GP rule", "GP-nowidth": "GP rule, ablated (no widths)",
         "GT-MWKR": "G\\&T-MWKR", "MOR": "MOR"}


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

    eps = defaultdict(lambda: defaultdict(dict))   # metodo -> anchura -> inst
    wid = defaultdict(dict)
    for r in csv.DictReader(open(CSV, encoding="utf-8")):
        eps[r["method"]][r["width"]][r["instance"]] = float(r["eps_bar"])
        if r["rel_width"]:
            wid[r["method"]][r["instance"]] = float(r["rel_width"])

    missing = [m for m in ORDER if m not in eps]
    if missing:
        sys.exit(f"faltan metodos en el CSV: {missing}")

    def mean(d):
        return sum(d.values()) / len(d)

    print(f"{'metodo':<14}{'ancho':>8}{'+0%':>8}{'+20%':>8}{'+40%':>8}")
    stats = {}
    for m in ORDER:
        w = mean(wid[m])
        e = [mean(eps[m][k]) for k in ("1.0", "1.2", "1.4")]
        stats[m] = (w, e)
        print(f"{m:<14}{w:>8.1f}" + "".join(f"{x:>8.1f}" for x in e))

    insts = sorted(eps["GP"]["1.0"])
    tests = {}
    for m in ORDER[1:]:
        z, n = wilcoxon([eps["GP"]["1.0"][i] - eps[m]["1.0"][i] for i in insts])
        tests[m] = (z, n)
        print(f"  Wilcoxon GP vs {m:<12} z={z:.2f} (n={n})")

    if args.dry:
        return

    t = open(TEX, encoding="utf-8").read()

    def sub(old, new):
        nonlocal t
        if old not in t:
            sys.exit("NO ENCONTRADO en main.tex:\n" + old[:120])
        t = t.replace(old, new, 1)

    def row(m, bold=False):
        w, e = stats[m]
        cells = [f"{w:.1f}"] + [f"{x:.1f}" for x in e]
        if bold:
            cells = [f"\\textbf{{{c}}}" for c in cells]
        return f"{SHOWN[m]} & " + " & ".join(cells) + " \\\\"

    sub("""GP rule & \\textbf{12.6} & \\textbf{5.8} & \\textbf{6.8} & \\textbf{7.7} \\\\
G\\&T-MWKR & 13.8 & 6.3 & 7.5 & 8.6 \\\\
MOR & 14.4 & 6.5 & 7.7 & 8.9 \\\\""",
        "\n".join([row("GP", bold=True), row("GP-nowidth"),
                   row("GT-MWKR"), row("MOR")]))

    open(TEX, "w", encoding="utf-8", newline="\n").write(t)
    print("\ntab:robustness actualizada (4 filas, una sola ejecucion)")
    print("pendiente a mano: las cifras que 7.3 cita en prosa y el pie de"
          " fig:robustness, con los z de arriba")


if __name__ == "__main__":
    main()
