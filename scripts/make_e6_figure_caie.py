# -*- coding: utf-8 -*-
"""Figura de E6 para el articulo de C&IE: calidad frente a presupuesto.

Rehace la de make_e6_figure.py (que sigue siendo la de paper_gp) para que
se lea sin el texto:

  - el eje (a) se llama como en el articulo, schedules construidos;
  - la regla de una pasada y G&T-MWKR son un punto, no una curva: se
    dibujan como una linea de referencia fina, para leer contra ella
    las demas curvas, con su marcador en el extremo derecho;
  - en (b) se marcan los tres tiempos de la tabla (1, 5 y 20 s);
  - la leyenda nombra el genetico como lo que es, nuestra
    implementacion.

Calcula las curvas desde las de E6 unidas a las de su extension, con
las funciones de e6_tabla.py, y lee tabla.json para los tiempos.

    python scripts/make_e6_figure_caie.py

Escribe paper_caie/figures/fig_budget.pdf
"""
import json
import os
import sys

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt                    # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TABLA = "benchmarks/e6_presupuesto/tabla.json"
SALIDA = "paper_caie/figures/fig_budget.pdf"

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
plt.rcParams.update({"font.size": 8.0, "figure.facecolor": "white",
                     "font.family": "sans-serif", "font.sans-serif": ["Arial"],
                     "mathtext.fontset": "custom", "mathtext.rm": "Arial",
                     "mathtext.it": "Arial:italic", "mathtext.bf": "Arial:bold",
                     "pdf.fonttype": 42})


def curvas():
    """Las curvas medias sobre las 70, en schedules y en segundos, desde
    las curvas de E6 unidas a las de su extension (e6_tabla.py)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from e6_tabla import (carga_completa, por_instancia_presupuesto,
                          por_instancia_tiempo)
    d = carga_completa()
    insts = sorted(d["ga"])
    rejilla = np.logspace(-2, 3, 90)
    ev, rl = {}, {}
    for m, *_ in CURVAS + PUNTOS:
        ev[m] = {}
        for k in range(0, 21):
            v = por_instancia_presupuesto(d, m, 2 ** k, insts)
            if v is not None:
                ev[m][2 ** k] = float(np.mean(v))
        xs, ys = [], []
        for t in rejilla:
            v = por_instancia_tiempo(d, m, float(t), insts)
            if v is not None:
                xs.append(float(t))
                ys.append(float(np.mean(v)))
        rl[m] = (xs, ys)
    return ev, rl


def main():
    tab = json.load(open(TABLA, encoding="utf-8"))
    ev, rl = curvas()
    fig, axes = plt.subplots(1, 2, figsize=(5.0, 2.45), sharey=True)

    for k, ax in enumerate(axes):
        for m, col, ls, etq in CURVAS:
            if k == 0:
                x = sorted(ev[m])
                y = [ev[m][b] for b in x]
            else:
                x, y = rl[m]
            ax.plot(x, y, ls, color=col, lw=1.4, label=etq)
        for m, col, mk, etq in PUNTOS:
            ax.axhline(ev[m][1], color=col, lw=0.6, ls=(0, (4, 3)), zorder=1)

    ax = axes[0]
    ax.set_xscale("log")
    ax.set_xlim(0.6, 5 * max(max(ev[m]) for m, *_ in CURVAS))
    ax.set_xlabel("schedules constructed")
    ax.set_ylabel("RE (%)")
    ax.set_title("(a) budget in schedules", loc="left", fontsize=8, pad=3)

    ax = axes[1]
    ax.set_xscale("log")
    ax.set_xlim(0.015, 4 * max(max(rl[m][0]) for m, *_ in CURVAS))
    for s in tab["tiempos"]:
        ax.axvline(s, color="0.75", lw=0.6, ls="-", zorder=0)
    ax.set_xlabel("seconds per instance")
    ax.set_title("(b) budget in seconds", loc="left", fontsize=8, pad=3)

    # las dos pasadas unicas, rotuladas con su marcador al extremo
    # derecho de su linea de referencia
    for ax in axes:
        x = ax.get_xlim()[1] / 1.5
        for m, col, mk, etq in PUNTOS:
            ax.plot([x], [ev[m][1]], mk, color=col, ms=5, zorder=5,
                    clip_on=False, label=etq)

    # escala logaritmica en RE: las permutaciones al azar viven por encima
    # del 60 % y la zona que interesa esta entre 13 y 30
    for ax in axes:
        ax.set_yscale("log")
        ax.set_ylim(10, 140)
        ax.set_yticks([10, 15, 20, 30, 50, 100])
        ax.set_yticklabels(["10", "15", "20", "30", "50", "100"])
        ax.minorticks_off()
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(alpha=0.25, linestyle=":", linewidth=0.6)

    h, l = axes[0].get_legend_handles_labels()
    orden = [4, 5, 0, 1, 2, 3]          # las dos pasadas, luego las curvas
    fig.legend([h[i] for i in orden], [l[i] for i in orden],
               loc="lower center", ncol=2, frameon=False, fontsize=7,
               bbox_to_anchor=(0.5, -0.2), handlelength=2.4)
    fig.tight_layout(w_pad=1.2)
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    fig.savefig(SALIDA, bbox_inches="tight")
    plt.close(fig)
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
