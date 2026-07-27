# -*- coding: utf-8 -*-
"""Regenera el cuerpo de tab:perinstance (apendice) dentro de main.tex.

Columnas: LB y G&T-MWKR de benchmarks/constructive_per_instance.csv, EST de
benchmarks/est_per_instance.csv, y GP de benchmarks/reevo_fixedfit/summary.csv
para la REGLA DESTACADA, de modo que el apendice y el cuerpo del paper
reporten siempre la misma regla.

Se muestra EST y no MOR porque EST es la mejor de las reglas simples
(42.3% frente a 45.5%), que es la comparacion que hace el texto de 6.3.

Reescribe solo las filas entre \\midrule y \\bottomrule, en el sitio, para no
depender de un \\input externo (un fichero con CRLF rompe la tabular).

Uso: python paper_gp/make_perinstance_table.py [--rule gp_tuned_seed1]
"""

import argparse
import csv
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TEX = os.path.join(HERE, "main.tex")
PERINST = os.path.join(REPO, "benchmarks/constructive_per_instance.csv")
ESTCSV = os.path.join(REPO, "benchmarks/est_per_instance.csv")
SUMMARY = os.path.join(REPO, "benchmarks/reevo_fixedfit/summary.csv")

# summary.csv usa int__taiJ_M_KK; el CSV por instancia usa TA01..TA70. El
# indice global de Taillard por clase:
BASE = {(15, 15): 0, (20, 15): 10, (20, 20): 20, (30, 15): 30,
        (30, 20): 40, (50, 15): 50, (50, 20): 60}


def ta_index(inst):
    m = re.search(r"tai(\d+)_(\d+)_(\d+)", inst)
    return BASE[(int(m.group(1)), int(m.group(2)))] + int(m.group(3))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rule", default="gp_tuned_seed1")
    args = ap.parse_args()

    gp = {}
    for r in csv.DictReader(open(SUMMARY, encoding="utf-8")):
        if r["method"] == args.rule:
            gp[ta_index(r["instance"])] = float(r["re"])
    if len(gp) != 70:
        sys.exit(f"{args.rule}: {len(gp)} instancias en summary.csv, se esperaban 70")

    base = {int(r["ta"][2:]): r for r in
            csv.DictReader(open(PERINST, encoding="utf-8"))}
    if len(base) != 70:
        sys.exit(f"{PERINST}: {len(base)} filas, se esperaban 70")

    est = {int(r["ta"][2:]): float(r["est_re"]) for r in
           csv.DictReader(open(ESTCSV, encoding="utf-8"))}
    if len(est) != 70:
        sys.exit(f"{ESTCSV}: {len(est)} filas, se esperaban 70")

    # los dos CSV se generaron por separado: el LB tiene que coincidir
    for i, r in base.items():
        lb_a = int(float(r["lb"]))
        lb_b = int(float(next(x["lb"] for x in
                              csv.DictReader(open(ESTCSV, encoding="utf-8"))
                              if int(x["ta"][2:]) == i)))
        if lb_a != lb_b:
            sys.exit(f"TA{i}: LB discrepante entre los dos CSV "
                     f"({lb_a} vs {lb_b})")

    def cell(i):
        r = base[i]
        return (f"TA{i} & {int(float(r['lb']))} & {est[i]:.1f} & "
                f"{float(r['GT-MWKR_re']):.1f} & {gp[i]:.1f}")

    rows = [f"{cell(i)} & {cell(i + 35)} \\\\" for i in range(1, 36)]

    tex = open(TEX, encoding="utf-8").read()
    lab = tex.index("\\label{tab:perinstance}")
    a = tex.index("\\midrule", lab) + len("\\midrule")
    b = tex.index("\\bottomrule", a)
    tex = tex[:a] + "\n" + "\n".join(rows) + "\n" + tex[b:]
    open(TEX, "w", encoding="utf-8", newline="\n").write(tex)
    print(f"tab:perinstance regenerada con {args.rule} "
          f"(RE medio {sum(gp.values())/70:.2f})")


if __name__ == "__main__":
    main()
