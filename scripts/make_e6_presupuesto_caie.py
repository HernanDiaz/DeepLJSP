# -*- coding: utf-8 -*-
"""Figura de 6.5 (paper_caie): RE frente a segundos por instancia.

Cuatro paneles con el mismo criterio que el resto de E6 version 2 (la
solucion en curso de cada corrida, e6_tabla.incumbente; media sobre las
corridas de cada instancia y despues sobre las instancias):

  (a) las 12 clasicas, 30 corridas de 900 s (e6c_clasicas.py), con los
      resultados publicados del genetico y de ESABC como referencia;
  (b)-(d) las clases 15x15, 30x15 y 50x15 de Taillard, 3 corridas con
      horizontes de 900, 1800 y 3600 s (e6t_clases.py).

Las dos pasadas unicas van como lineas horizontales con su marcador a la
derecha.

    python scripts/make_e6_presupuesto_caie.py

Escribe paper_caie/figures/fig_budget.pdf
"""
import os
import sys

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt                    # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_e6c_figure as fc                      # noqa: E402
import make_e6_tamanos_figure as ft               # noqa: E402

SALIDA = "paper_caie/figures/fig_budget.pdf"
plt.rcParams.update({"font.size": 8.0, "figure.facecolor": "white",
                     "font.family": "sans-serif", "font.sans-serif": ["Arial"],
                     "mathtext.fontset": "custom", "mathtext.rm": "Arial",
                     "mathtext.it": "Arial:italic", "mathtext.bf": "Arial:bold",
                     "pdf.fonttype": 42})


def main():
    ec = fc.modulo_clasicas()
    dc, dt = fc.carga(), ft.carga()
    paneles = [("(a) 12 classical instances", dc, list(ec.FILES), 900.0)]
    for t, clase, h in (("(b) Taillard 15$\\times$15", "15_15", 900.0),
                        ("(c) Taillard 30$\\times$15", "30_15", 1800.0),
                        ("(d) Taillard 50$\\times$15", "50_15", 3600.0)):
        paneles.append((t, dt, [f"int__tai{clase}_{k:02d}"
                                for k in range(1, 11)], h))
    fig, axes = plt.subplots(2, 2, figsize=(4.98, 3.9), sharey=True)
    for ax, (titulo, d, insts, h) in zip(axes.flat, paneles):
        rejilla = np.logspace(-2, np.log10(h - 1.0), 200)
        for m, col, ls, etq in ft.CURVAS:
            ax.plot(*ft.curva(d, m, insts, rejilla), ls, color=col, lw=1.3,
                    label=etq)
        x = h * 2.6
        for m, col, mk, etq in ft.PUNTOS:
            nivel = float(np.mean([d[m][i][0][0][1] for i in insts]))
            ax.axhline(nivel, color=col, lw=0.6, ls=(0, (4, 3)), zorder=1)
            ax.plot([x], [nivel], mk, color=col, ms=4.5, zorder=5,
                    clip_on=False, label=etq)
        if d is dc:
            for clave, etq in (("GA", "GA (published)"),
                               ("ESABC", "ESABC (published)")):
                v = float(np.mean([ec.PUB_AVG[i][clave] for i in insts]))
                ax.axhline(v, color="0.15", lw=0.7, ls=":", zorder=1)
                ax.text(0.012, v * 1.04, etq, fontsize=6.5, va="bottom",
                        color="0.15")
        ax.set_xscale("log")
        ax.set_xlim(0.01, h * 4.5)
        ax.set_yscale("log")
        ax.set_ylim(4.5, 120)
        ax.set_yticks([5, 7, 10, 15, 20, 30, 50, 100])
        ax.set_yticklabels(["5", "7", "10", "15", "20", "30", "50", "100"])
        ax.minorticks_off()
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(alpha=0.25, linestyle=":", linewidth=0.6)
        ax.set_title(titulo, loc="left", fontsize=8, pad=3)
    for ax in axes[1]:
        ax.set_xlabel("seconds per instance")
    for ax in axes[:, 0]:
        ax.set_ylabel("RE (%)")
    h, l = axes[0, 0].get_legend_handles_labels()
    orden = [4, 5, 0, 1, 2, 3]
    fig.legend([h[i] for i in orden], [l[i] for i in orden], loc="lower center",
               ncol=2, frameon=False, fontsize=7, bbox_to_anchor=(0.5, -0.09),
               handlelength=2.4)
    fig.tight_layout(h_pad=1.0, w_pad=0.8)
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    fig.savefig(SALIDA, bbox_inches="tight")
    plt.close(fig)
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
