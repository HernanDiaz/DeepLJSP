# -*- coding: utf-8 -*-
"""Figura de 7.6 (paper_caie): calidad prevista frente a fiabilidad.

Dos paneles con los siete metodos de la tabla de robustez, cada uno en
la media sobre las 70 instancias, ley uniforme y K = 1000 realizaciones:

  (a) RE de la prediccion frente a la desviacion media del makespan
      ejecutado respecto al previsto, |Delta|, en unidades de tiempo;
  (b) RE frente al exceso sobre la prediccion en el 5 % peor de las
      ejecuciones (CVaR 0.95 del exceso), en unidades de tiempo.

Las unidades de tiempo, y no el epsilon normalizado, porque al dividir
por E[Cmax] un metodo con peor makespan parece mas robusto de lo que es.
La linea une los brazos con terminales de anchura al subir lambda
(makespan, lambda = 1, lambda = 4).

Lee benchmarks/e7_cvar/por_instancia.csv (scripts/e7_cvar.py).

    python scripts/make_robustness_plane_caie.py

Escribe paper_caie/figures/fig_robustness_plane.pdf
"""
import collections
import csv
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt                    # noqa: E402

ENTRADA = "benchmarks/e7_cvar/por_instancia.csv"
SALIDA = "paper_caie/figures/fig_robustness_plane.pdf"
plt.rcParams.update({"font.size": 8.0, "figure.facecolor": "white",
                     "font.family": "sans-serif", "font.sans-serif": ["Arial"],
                     "mathtext.fontset": "custom", "mathtext.rm": "Arial",
                     "mathtext.it": "Arial:italic", "mathtext.bf": "Arial:bold",
                     "pdf.fonttype": 42})

# la paleta de fig_robustness_box, mas los dos brazos que alli no salen
METODOS = [  # clave, etiqueta, color, marcador, relleno
    ("GP", "GP, makespan", "#d68910", "o", True),
    ("GP-nowidth", "GP, makespan, no widths", "#d68910", "o", False),
    ("GP-rob1", "GP, robust $\\lambda{=}1$", "#b0632c", "s", True),
    ("GP-rob1-nw", "GP, robust $\\lambda{=}1$, no widths", "#c7a740", "s", False),
    ("GP-rob4", "GP, robust $\\lambda{=}4$", "#7a3e17", "^", True),
    ("GT-MWKR", "G&T-MWKR", "#0e8a7d", "D", True),
    ("EST", "EST", "#5d6d7e", "v", True),
]
EJES = [("abs_dev", "(a) mean deviation",
         "deviation $|\\Delta|$ (time units)"),
        ("cvar95_over", "(b) worst 5% of executions",
         "overrun, CVaR$_{0.95}$ (time units)")]


def main():
    filas = collections.defaultdict(list)
    for r in csv.DictReader(open(ENTRADA, encoding="utf-8")):
        if r["law"] == "uniform":
            filas[r["method"]].append(r)
    media = {m: {k: sum(float(x[k]) for x in v) / len(v)
                 for k in ("re_mid", "abs_dev", "cvar95_over")}
             for m, v in filas.items()}
    assert all(len(filas[m]) == 70 for m, *_ in METODOS)

    fig, axes = plt.subplots(1, 2, figsize=(4.98, 2.7))
    for ax, (clave, titulo, ylab) in zip(axes, EJES):
        # la senda de los brazos con anchuras al subir lambda
        senda = ["GP", "GP-rob1", "GP-rob4"]
        ax.plot([media[m]["re_mid"] for m in senda],
                [media[m][clave] for m in senda], "-", color="0.75",
                lw=1.0, zorder=1)
        for m, etq, col, mk, lleno in METODOS:
            ax.plot(media[m]["re_mid"], media[m][clave], mk, ms=6,
                    color=col, mfc=col if lleno else "white", mew=1.3,
                    zorder=3, label=etq)
        ax.set_title(titulo, loc="left", fontsize=8, pad=3)
        ax.set_xlabel("RE of the predicted makespan (%)")
        ax.set_ylabel(ylab)
        ax.set_xlim(14, 46)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(alpha=0.25, linestyle=":", linewidth=0.6)
    axes[0].set_ylim(9, 15.8)
    axes[1].set_ylim(24, 43)
    axes[1].set_yticks(range(25, 45, 5))
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=3, frameon=False, fontsize=7,
               bbox_to_anchor=(0.5, -0.17), handletextpad=0.3,
               columnspacing=1.0)
    fig.tight_layout(w_pad=1.5)
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    fig.savefig(SALIDA, bbox_inches="tight")
    plt.close(fig)
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
