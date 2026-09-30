# -*- coding: utf-8 -*-
"""Figura del presupuesto en segundos por clase de tamano (Taillard).

Un panel por clase del experimento e6t_clases.py: 15x15, 30x15 y 50x15,
las tres con 15 maquinas, cada una con su horizonte. En cada panel, para
cada metodo, el RE de la solucion en curso de cada corrida
(e6_tabla.incumbente), promediado sobre las corridas de cada instancia
y despues sobre las instancias de la clase. La regla y G&T-MWKR en una
pasada van como lineas de referencia con su marcador a la derecha.

Una clase sin datos todavia deja su panel vacio, con un aviso.

    python scripts/make_e6_tamanos_figure.py [--salida fichero.pdf]
"""
import argparse
import collections
import csv
import os
import sys

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt                    # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e6_tabla import incumbente                    # noqa: E402

CURVAS_CSV = "benchmarks/e6_tamanos/curvas.csv"
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
CLASES = [("(a) 15$\\times$15", "15_15"), ("(b) 30$\\times$15", "30_15"),
          ("(c) 50$\\times$15", "50_15")]
plt.rcParams.update({"font.size": 8.0, "figure.facecolor": "white",
                     "font.family": "sans-serif", "font.sans-serif": ["Arial"],
                     "mathtext.fontset": "custom", "mathtext.rm": "Arial",
                     "mathtext.it": "Arial:italic", "mathtext.bf": "Arial:bold",
                     "pdf.fonttype": 42})


def carga(fichero=CURVAS_CSV):
    """d[metodo][instancia][semilla] = [(presupuesto, re, segundos)],
    y de cada corrida solo las filas de su horizonte mayor: una corrida
    alargada desde su estado sustituye a la corta."""
    filas = collections.defaultdict(list)
    for r in csv.DictReader(open(fichero, encoding="utf-8")):
        filas[(r["metodo"], r["instancia"], int(r["semilla"]))].append(
            (float(r["horizonte"]), int(r["presupuesto"]), float(r["re"]),
             float(r["segundos"])))
    d = collections.defaultdict(lambda: collections.defaultdict(dict))
    for (m, i, s), v in filas.items():
        h = max(x[0] for x in v)
        d[m][i][s] = sorted((p, re, seg) for hh, p, re, seg in v if hh == h)
    return d


def curva(d, m, insts, rejilla):
    """Media sobre instancias de la media sobre corridas, en cada t de la
    rejilla donde todas las instancias tienen al menos una corrida."""
    xs, ys = [], []
    for t in rejilla:
        v = []
        for i in insts:
            w = [incumbente(p, t) for p in d[m][i].values()]
            w = [x for x in w if not np.isnan(x)]
            if not w:
                break
            v.append(np.mean(w))
        else:
            xs.append(t)
            ys.append(np.mean(v))
    return xs, ys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default="paper_caie/figures/fig_budget_sizes.pdf")
    args = ap.parse_args()
    d = carga()
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.5), sharey=True)
    for ax, (titulo, clase) in zip(axes, CLASES):
        insts = [f"int__tai{clase}_{k:02d}" for k in range(1, 11)]
        hay = [i for i in insts if all(d[m][i] for m in ("ga", "ga_sembrado",
                                                          "regla_bon"))]
        horiz = max((seg for m in ("ga", "regla_bon") for i in hay
                     for p in d[m][i].values() for _, _, seg in p[-1:]),
                    default=1.0)
        corridas = {m: sum(len(d[m][i]) for i in hay) for m, *_ in CURVAS}
        print(f"{clase}: {len(hay)} instancias, corridas {corridas}")
        ax.set_title(titulo, loc="left", fontsize=8, pad=3)
        if not hay:
            ax.text(0.5, 0.5, "pending", transform=ax.transAxes,
                    ha="center", color="0.5")
        rejilla = np.logspace(-2, np.log10(horiz), 160)
        for m, col, ls, etq in CURVAS:
            if hay and all(d[m][i] for i in hay):
                ax.plot(*curva(d, m, hay, rejilla), ls, color=col, lw=1.3,
                        label=etq)
            else:
                ax.plot([], [], ls, color=col, lw=1.3, label=etq)
        for m, col, mk, etq in PUNTOS:
            if hay and all(d[m][i] for i in hay):
                nivel = float(np.mean([d[m][i][0][0][1] for i in hay]))
                ax.axhline(nivel, color=col, lw=0.6, ls=(0, (4, 3)), zorder=1)
                ax.plot([horiz * 2.2], [nivel], mk, color=col, ms=4.5,
                        zorder=5, clip_on=False, label=etq)
            else:
                ax.plot([], [], mk, color=col, ms=4.5, label=etq)
        ax.set_xscale("log")
        ax.set_xlim(0.01, horiz * 3.5)
        ax.set_yscale("log")
        ax.set_ylim(5, 140)
        ax.set_yticks([5, 7, 10, 15, 20, 30, 50, 100])
        ax.set_yticklabels(["5", "7", "10", "15", "20", "30", "50", "100"])
        ax.minorticks_off()
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(alpha=0.25, linestyle=":", linewidth=0.6)
        ax.set_xlabel("seconds per instance")
    axes[0].set_ylabel("RE (%)")
    h, l = axes[0].get_legend_handles_labels()
    orden = [4, 5, 0, 1, 2, 3]
    fig.legend([h[i] for i in orden], [l[i] for i in orden], loc="lower center",
               ncol=3, frameon=False, fontsize=7, bbox_to_anchor=(0.5, -0.13),
               handlelength=2.4)
    fig.tight_layout(w_pad=0.8)
    fig.savefig(args.salida, bbox_inches="tight")
    print(f"escrito {args.salida}")


if __name__ == "__main__":
    main()
