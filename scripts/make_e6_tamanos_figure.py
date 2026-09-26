# -*- coding: utf-8 -*-
"""Figura del presupuesto en segundos por tamano de instancia (Taillard).

La media de las 70 instancias mezcla cruces que ocurren a tiempos muy
distintos segun el tamano. Aqui un panel por grupo: pequenas (15x15,
20x15, 20x20), medianas (30x15, 30x20) y grandes (50x15, 50x20), con las
mismas curvas y el mismo criterio que la figura del presupuesto (la
solucion en curso de cada corrida, e6_tabla.incumbente).

    python scripts/make_e6_tamanos_figure.py [--salida fichero.pdf]
"""
import argparse
import os
import sys

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt                    # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e6_tabla import carga_completa, por_instancia_tiempo    # noqa: E402

AZUL, AMBAR, GRIS, TEAL = "#1f5fa8", "#d68910", "#5d6d7e", "#0e8a7d"
GRANATE = "#8e2f4a"
CURVAS = [
    ("regla_bon", AMBAR, "-", "evolved rule, best-of-$N$"),
    ("ga", GRANATE, "-", "genetic algorithm (our implementation)"),
    ("ga_sembrado", TEAL, "--", "genetic algorithm seeded with the rule"),
    ("azar", GRIS, ":", "random permutations"),
]
PUNTOS = [("regla", AZUL, "D", "evolved rule, one pass"),
          ("gt_mwkr", "0.35", "s", "G&T-MWKR, one pass")]
GRUPOS = [("(a) small: 15$\\times$15 to 20$\\times$20", ("15_15", "20_15", "20_20")),
          ("(b) medium: 30$\\times$15, 30$\\times$20", ("30_15", "30_20")),
          ("(c) large: 50$\\times$15, 50$\\times$20", ("50_15", "50_20"))]
plt.rcParams.update({"font.size": 8.0, "figure.facecolor": "white",
                     "font.family": "sans-serif", "font.sans-serif": ["Arial"],
                     "mathtext.fontset": "custom", "mathtext.rm": "Arial",
                     "mathtext.it": "Arial:italic", "mathtext.bf": "Arial:bold",
                     "pdf.fonttype": 42})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default="paper_caie/figures/fig_budget_sizes.pdf")
    args = ap.parse_args()
    d = carga_completa()
    todas = sorted(d["ga"])
    rejilla = sorted(set(np.logspace(-2, np.log10(800), 90)) | {800.0})
    fig, axes = plt.subplots(1, 3, figsize=(5.0, 2.3), sharey=True)
    for ax, (titulo, clases) in zip(axes, GRUPOS):
        ins = [i for i in todas if any(c in i for c in clases)]
        for m, col, ls, etq in CURVAS:
            pts = [(t, por_instancia_tiempo(d, m, float(t), ins)) for t in rejilla]
            pts = [(t, np.mean(v)) for t, v in pts if v]
            ax.plot(*zip(*pts), ls, color=col, lw=1.3, label=etq)
        for m, col, mk, etq in PUNTOS:
            nivel = float(np.mean([d[m][i][0][0][1] for i in ins]))
            ax.axhline(nivel, color=col, lw=0.6, ls=(0, (4, 3)), zorder=1)
        ax.set_xscale("log")
        ax.set_xlim(0.01, 3000)
        ax.set_xticks([0.1, 1, 10, 100, 800])
        ax.set_xticklabels(["0.1", "1", "10", "100", "800"])
        ax.set_yscale("log")
        ax.set_ylim(8, 140)
        ax.set_yticks([10, 15, 20, 30, 50, 100])
        ax.set_yticklabels(["10", "15", "20", "30", "50", "100"])
        ax.minorticks_off()
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(alpha=0.25, linestyle=":", linewidth=0.6)
        ax.set_title(titulo, loc="left", fontsize=7.5, pad=3)
        ax.set_xlabel("seconds per instance")
        x = ax.get_xlim()[1] / 1.5
        for m, col, mk, etq in PUNTOS:
            nivel = float(np.mean([d[m][i][0][0][1] for i in ins]))
            ax.plot([x], [nivel], mk, color=col, ms=4.5, zorder=5,
                    clip_on=False, label=etq)
    axes[0].set_ylabel("RE (%)")
    h, l = axes[0].get_legend_handles_labels()
    orden = [4, 5, 0, 1, 2, 3]
    fig.legend([h[i] for i in orden], [l[i] for i in orden], loc="lower center",
               ncol=2, frameon=False, fontsize=7, bbox_to_anchor=(0.5, -0.22),
               handlelength=2.4)
    fig.tight_layout(w_pad=0.8)
    fig.savefig(args.salida, bbox_inches="tight")
    print(f"escrito {args.salida}")


if __name__ == "__main__":
    main()
