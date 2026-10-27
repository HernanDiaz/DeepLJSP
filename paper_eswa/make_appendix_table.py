# -*- coding: utf-8 -*-
"""Regenera el cuerpo de tab:perinstance (apendice) dentro de main.tex.

Columnas: LB y G&T-MWKR de constructive_per_instance.csv, EST de
est_per_instance.csv, GP (regla destacada del companion, publicada como
preprint) de reevo_fixedfit/summary.csv, y la politica en sus dos
presupuestos: greedy de fair_v2_greedy.csv (media de los tres
checkpoints) y best-of-1024 de eval_fair_bo1024.csv (mejor por
instancia).

Reescribe solo las filas entre \\midrule y \\bottomrule, en el sitio.

    python paper/make_appendix_table.py
"""
import csv
import os
import re
import sys
from collections import defaultdict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TEX = os.path.join(HERE, "main.tex")

BASE = {"15_15": 0, "20_15": 10, "20_20": 20, "30_15": 30,
        "30_20": 40, "50_15": 50, "50_20": 60}
REGLA_GP = "gp_tuned_seed1"      # la destacada del companion (17.71%)


def idx(inst):
    m = re.search(r"tai(\d+_\d+)_(\d+)", inst.lower())
    return BASE[m.group(1)] + int(m.group(2))


def _csv(nombre):
    return csv.DictReader(open(os.path.join(REPO, nombre), encoding="utf-8"))


def main():
    lb, gt = {}, {}
    for r in _csv("benchmarks/constructive_per_instance.csv"):
        n = int(r["ta"][2:])
        lb[n] = int(float(r["lb"]))
        gt[n] = float(r["GT-MWKR_re"])
    est = {int(r["ta"][2:]): float(r["est_re"])
           for r in _csv("benchmarks/est_per_instance.csv")}
    gp = {idx(r["instance"]): float(r["re"])
          for r in _csv("benchmarks/reevo_fixedfit/summary.csv")
          if r["method"] == REGLA_GP}

    gre = defaultdict(list)
    for r in _csv("benchmarks/fair_v2_greedy.csv"):
        gre[idx(r["instance"])].append(float(r["re_mid"]))
    gre = {k: sum(v) / len(v) for k, v in gre.items()}

    bo = defaultdict(list)
    for r in _csv("benchmarks/eval_fair_bo1024.csv"):
        bo[idx(r["instance"])].append(float(r["re_comp"]))
    bo = {k: min(v) for k, v in bo.items()}

    for nombre, d in [("LB", lb), ("EST", est), ("G&T", gt), ("GP", gp),
                      ("greedy", gre), ("bo1024", bo)]:
        if len(d) != 70:
            sys.exit(f"ABORTA: {nombre} tiene {len(d)} instancias, no 70")

    def celda(n):
        return (f"TA{n} & {lb[n]} & {est[n]:.1f} & {gt[n]:.1f} & "
                f"{gp[n]:.1f} & {gre[n]:.1f} & {bo[n]:.1f}")

    filas = [celda(n) + " & " + celda(n + 35) + r" \\" for n in range(1, 36)]
    cuerpo = "\n".join(filas)

    t = open(TEX, encoding="utf-8").read()
    i = t.index("\\label{tab:perinstance}")
    a = t.index("\\midrule", i) + len("\\midrule")
    b = t.index("\\bottomrule", a)
    t = t[:a] + "\n" + cuerpo + "\n" + t[b:]
    open(TEX, "w", encoding="utf-8", newline="\n").write(t)

    print(f"tab:perinstance regenerada, {len(filas)} filas")
    print(f"  medias: EST {sum(est.values()) / 70:.2f}  "
          f"G&T {sum(gt.values()) / 70:.2f}  GP {sum(gp.values()) / 70:.2f}  "
          f"greedy {sum(gre.values()) / 70:.2f}  "
          f"bo1024 {sum(bo.values()) / 70:.2f}")


if __name__ == "__main__":
    main()
