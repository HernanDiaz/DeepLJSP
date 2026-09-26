# -*- coding: utf-8 -*-
"""Figura del presupuesto en las doce clasicas (e6c_clasicas.py).

Mismo estilo que la de las 70 Taillard (make_e6_figure_caie.py): RE
frente a schedules construidos (a) y frente a segundos (b), la media
sobre las doce instancias de la media de las corridas de cada una. En el
eje de segundos se toma la solucion en curso de cada corrida
(e6_tabla.incumbente). Ademas, como lineas de referencia, la pasada unica
de la regla y de G&T-MWKR, y los resultados publicados del genetico y de
ESABC (medias de 30 corridas, C++, cada uno con su propia parada).

    python scripts/make_e6c_figure.py [--salida fichero.pdf]
"""
import argparse
import collections
import csv
import importlib.util
import os
import sys

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt                    # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e6_tabla import incumbente                    # noqa: E402

CURVAS_CSV = "benchmarks/e6_clasicas/curvas.csv"
AZUL, AMBAR, GRIS, TEAL = "#1f5fa8", "#d68910", "#5d6d7e", "#0e8a7d"
GRANATE = "#8e2f4a"
CURVAS = [
    ("regla_bon", AMBAR, "-", "evolved rule, best-of-$N$"),
    ("ga", GRANATE, "-", "genetic algorithm (our implementation)"),
    ("ga_sembrado", TEAL, "--", "genetic algorithm seeded with the rule"),
    ("azar", GRIS, ":", "random permutations"),
]
plt.rcParams.update({"font.size": 8.0, "figure.facecolor": "white",
                     "font.family": "sans-serif", "font.sans-serif": ["Arial"],
                     "mathtext.fontset": "custom", "mathtext.rm": "Arial",
                     "mathtext.it": "Arial:italic", "mathtext.bf": "Arial:bold",
                     "pdf.fonttype": 42})


def modulo_clasicas():
    spec = importlib.util.spec_from_file_location(
        "ec12", os.path.join("scripts", "eval_classic12.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def carga():
    d = collections.defaultdict(lambda: collections.defaultdict(
        lambda: collections.defaultdict(list)))
    for r in csv.DictReader(open(CURVAS_CSV, encoding="utf-8")):
        d[r["metodo"]][r["instancia"]][int(r["semilla"])].append(
            (int(r["presupuesto"]), float(r["re"]), float(r["segundos"])))
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default="paper_caie/figures/fig_budget_classical.pdf")
    args = ap.parse_args()
    ec = modulo_clasicas()
    insts = list(ec.FILES)
    d = carga()
    corridas = {m: min(len(d[m][i]) for i in insts) if all(d[m][i] for i in insts)
                else 0 for m, *_ in CURVAS}
    print("corridas completas por instancia:", corridas)

    def en_presupuesto(m, b):
        v = []
        for i in insts:
            w = [re for s in d[m][i] for (p, re, _) in d[m][i][s] if p == b]
            if not w:
                return None
            v.append(np.mean(w))
        return float(np.mean(v))

    def en_tiempo(m, t):
        v = []
        for i in insts:
            w = [incumbente(d[m][i][s], t) for s in d[m][i]]
            w = [x for x in w if not np.isnan(x)]
            if not w:
                return None
            v.append(np.mean(w))
        return float(np.mean(v))

    # las dos pasadas unicas: del csv si ya estan, si no se calculan
    from e6c_clasicas import corre
    pasada = {}
    for m in ("regla", "gt_mwkr"):
        if all(d[m][i] for i in insts):
            pasada[m] = float(np.mean([d[m][i][0][0][1] for i in insts]))
        else:
            pasada[m] = float(np.mean([corre((i, m, 0))[0][4] for i in insts]))
    publ = {"GA (published)": np.mean([ec.PUB_AVG[i]["GA"] for i in insts]),
            "ESABC (published)": np.mean([ec.PUB_AVG[i]["ESABC"] for i in insts])}
    print("pasadas:", pasada, "publicados:", publ)

    rejilla = np.logspace(-3, np.log10(900), 90)
    fig, axes = plt.subplots(1, 2, figsize=(5.0, 2.45), sharey=True)
    for k, ax in enumerate(axes):
        for m, col, ls, etq in CURVAS:
            if not corridas[m]:
                continue
            if k == 0:
                pts = [(2 ** e, en_presupuesto(m, 2 ** e)) for e in range(31)]
            else:
                pts = [(t, en_tiempo(m, float(t))) for t in rejilla]
            pts = [(x, y) for x, y in pts if y is not None]
            ax.plot(*zip(*pts), ls, color=col, lw=1.4, label=etq)
        for (m, col, mk, etq) in (("regla", AZUL, "D", "evolved rule, one pass"),
                                  ("gt_mwkr", "0.35", "s", "G&T-MWKR, one pass")):
            ax.axhline(pasada[m], color=col, lw=0.6, ls=(0, (4, 3)), zorder=1)
        for etq, v in publ.items():
            ax.axhline(v, color="black", lw=0.6, ls=":", zorder=1)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_ylim(3, 140)
        ax.set_yticks([3, 5, 10, 20, 30, 50, 100])
        ax.set_yticklabels(["3", "5", "10", "20", "30", "50", "100"])
        ax.minorticks_off()
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(alpha=0.25, linestyle=":", linewidth=0.6)
    axes[0].set_xlabel("schedules constructed")
    axes[0].set_ylabel("RE (%)")
    axes[0].set_title("(a) budget in schedules", loc="left", fontsize=8, pad=3)
    axes[1].set_xlabel("seconds per instance")
    axes[1].set_title("(b) budget in seconds", loc="left", fontsize=8, pad=3)
    for ax in axes:
        x = ax.get_xlim()[1] * 1.3
        for (m, col, mk, etq) in (("regla", AZUL, "D", "evolved rule, one pass"),
                                  ("gt_mwkr", "0.35", "s", "G&T-MWKR, one pass")):
            ax.plot([x], [pasada[m]], mk, color=col, ms=5, clip_on=False,
                    label=etq)
        for etq, v in publ.items():
            ax.text(ax.get_xlim()[0] * 1.3, v * 0.93, etq, fontsize=6.5,
                    va="top")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=2, frameon=False, fontsize=7,
               bbox_to_anchor=(0.5, -0.2), handlelength=2.4)
    fig.tight_layout(w_pad=1.2)
    fig.savefig(args.salida, bbox_inches="tight")
    print(f"escrito {args.salida}")


if __name__ == "__main__":
    main()
