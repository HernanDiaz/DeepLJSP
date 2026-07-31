# -*- coding: utf-8 -*-
"""Genera las dos tablas comparativas del paper DRL (espejo de las del GP).

Tabla A -- las 70 Taillard por clase: reglas (EST/MOR/G&T-MWKR), politica
(greedy y best-of-1024) y las referencias publicadas (fEABC y TS, medias
de 30 runs del suplemento).

Tabla B -- las 12 clasicas: EST/MOR/G&T, politica best-of-64 (media y
mejor de los 3 checkpoints) y las metaheuristicas publicadas (GA, ABC_E3,
fEABC, ESABC).

Escribe paper/tables_generated.tex para revision; no toca main.tex.
Si falta una fuente (evaluaciones aun corriendo) deja la columna como
guiones y lo dice.

    python scripts/make_comparison_tables.py
"""
import csv
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CLASES = ["15_15", "20_15", "20_20", "30_15", "30_20", "50_15", "50_20"]
TA_BASE = {c: 10 * i for i, c in enumerate(CLASES)}


def ta_de(nombre):
    m = re.search(r"tai(\d+_\d+)_(\d+)", nombre.lower())
    return TA_BASE[m.group(1)] + int(m.group(2))  # 1..70


def clase_de(num):
    return CLASES[(num - 1) // 10]


def medias_por_clase(por_ta):
    """{clase: media} + 'all' desde {num_ta: valor}."""
    grupos = defaultdict(list)
    for num, v in por_ta.items():
        grupos[clase_de(num)].append(v)
    out = {c: sum(v) / len(v) for c, v in grupos.items()}
    out["all"] = sum(por_ta.values()) / len(por_ta)
    return out


def fila(nombre, valores, negrita=False):
    fmt = "\\textbf{%.1f}" if negrita else "%.1f"
    celdas = [fmt % valores[c] if c in valores else "--"
              for c in CLASES + ["all"]]
    return f"{nombre} & " + " & ".join(celdas) + " \\\\"


def main():
    lineas = ["% Generado por scripts/make_comparison_tables.py -- revisar",
              "% antes de integrar en main.tex", ""]

    # ---------------- Tabla A: las 70 por clase --------------------------
    ab = {}
    for r in csv.DictReader(open("benchmarks/all_baselines.csv",
                                 encoding="utf-8")):
        ab[r["method"]] = {c: float(r[c]) for c in CLASES}
        ab[r["method"]]["all"] = float(r["all"])

    greedy = defaultdict(list)
    for r in csv.DictReader(open("benchmarks/fair_v2_greedy.csv",
                                 encoding="utf-8")):
        greedy[ta_de(r["instance"])].append(float(r["re_mid"]))
    greedy_ta = {k: sum(v) / len(v) for k, v in greedy.items()}

    bo1024 = None
    if os.path.exists("benchmarks/eval_fair_bo1024.csv"):
        mejor = defaultdict(list)
        for r in csv.DictReader(open("benchmarks/eval_fair_bo1024.csv",
                                     encoding="utf-8")):
            mejor[ta_de(r["instance"])].append(float(r["re_comp"]))
        if len(mejor) == 70:
            bo1024 = {k: min(v) for k, v in mejor.items()}
        else:
            print(f"bo1024 incompleto ({len(mejor)}/70): columna en guiones")

    pub = {}
    exec(re.search(r"(FEABC_BEST.*?)(?=\n# |\ndef |\Z)",
                   open("scripts/compare_pools_published.py",
                        encoding="utf-8").read(), re.S).group(1), {}, pub)
    feabc = {i + 1: v for i, v in enumerate(pub["FEABC_AVG"])}
    ts = {i + 1: v for i, v in enumerate(pub["TS_AVG"])}

    lineas += [
        "\\begin{table}[t]",
        "\\centering\\small",
        "\\caption{Mean RE (\\%) per size class over the 70 interval",
        "Taillard instances. Constructive methods are a single",
        "deterministic pass unless stated; fEABC and TS are 30-run",
        "averages on dedicated hardware (different computational class).}",
        "\\label{tab:seventy}",
        "\\begin{tabular}{lcccccccc}",
        "\\toprule",
        "Method & " + " & ".join(
            f"${c.replace('_', '{\\times}')}$" for c in CLASES)
        + " & All \\\\",
        "\\midrule",
        fila("EST", ab["EST"]),
        fila("MOR", ab["MOR"]),
        fila("G\\&T-MWKR", ab["G&T-MWKR"]),
        fila("Policy (greedy)", medias_por_clase(greedy_ta)),
        fila("Policy (best-of-1024)",
             medias_por_clase(bo1024) if bo1024 else {}, negrita=True),
        "\\midrule",
        fila("fEABC (30 runs)", medias_por_clase(feabc)),
        fila("TS (30 runs)", medias_por_clase(ts)),
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{table}",
        "",
    ]

    # ---------------- Tabla B: las 12 clasicas ---------------------------
    clas = {r["inst"]: r for r in csv.DictReader(
        open("benchmarks/classic12_tuned.csv", encoding="utf-8"))}
    est = {r["inst"]: float(r["est_re"]) for r in csv.DictReader(
        open("benchmarks/classic12_est.csv", encoding="utf-8"))}

    pol = defaultdict(list)
    if os.path.exists("benchmarks/eval_classic12_policy.csv"):
        for r in csv.DictReader(open("benchmarks/eval_classic12_policy.csv",
                                     encoding="utf-8")):
            pol[r["name"]].append(float(r["re"]))
    if len(pol) < 12:
        print(f"classics de la politica incompletos ({len(pol)}/12)")

    lineas += [
        "\\begin{table}[t]",
        "\\centering\\small",
        "\\caption{RE (\\%) on the 12 classical interval instances",
        "(cross-family zero-shot: the policy never saw these families).",
        "Published metaheuristics are 30-run averages; reference bounds",
        "are the best-known expected-makespan values, a different scale",
        "from Taillard's crisp bounds.}",
        "\\label{tab:classics}",
        "\\begin{tabular}{lccccccccc}",
        "\\toprule",
        "Inst. & EST & MOR & G\\&T & Policy & Policy$^{b}$ & GA &"
        " ABC$_{E3}$ & fEABC & ESABC \\\\",
        "\\midrule",
    ]
    for inst in clas:
        p_mean = f"{sum(pol[inst]) / len(pol[inst]):.1f}" if pol.get(inst) \
            else "--"
        p_best = f"{min(pol[inst]):.1f}" if pol.get(inst) else "--"
        c = clas[inst]
        lineas.append(
            f"{inst} & {est[inst]:.1f} & {float(c['mor']):.1f} & "
            f"{float(c['gt']):.1f} & {p_mean} & {p_best} & "
            f"{float(c['GA']):.1f} & {float(c['ABCE3']):.1f} & "
            f"{float(c['fEABC']):.1f} & {float(c['ESABC']):.1f} \\\\")
    lineas += [
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{table}",
        "",
        "% Policy: media de los 3 checkpoints, best-of-64.",
        "% Policy^b: mejor de los 3 checkpoints.",
    ]

    open("paper/tables_generated.tex", "w", encoding="utf-8",
         newline="\n").write("\n".join(lineas))
    print("escrito paper/tables_generated.tex")


if __name__ == "__main__":
    main()
