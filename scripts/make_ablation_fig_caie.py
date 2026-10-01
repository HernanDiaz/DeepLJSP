# -*- coding: utf-8 -*-
"""Figura de 7.4 (paper_caie): las ablaciones, semilla a semilla.

Las tres comparaciones de la tabla de ablaciones como diferencias
pareadas por semilla (30 por fila), en RE (a) y en anchura relativa del
intervalo de makespan previsto (b), sobre las 70 instancias:

  - objetivo de makespan: con terminales de anchura menos sin ellos;
  - objetivo robusto (lambda = 1): con menos sin;
  - control del punto medio: evolucionado en las instancias crisp con
    fitness escalar menos el brazo sin anchuras con fitness intervalar.

Negativo es mejor para la primera opcion de cada fila. El rombo es la
mediana; la etiqueta, el contraste de Wilcoxon pareado de la tabla.

Lee benchmarks/ablation_por_regla.csv y
benchmarks/midpoint_control_por_regla.csv.

    python scripts/make_ablation_fig_caie.py

Escribe paper_caie/figures/fig_ablation.pdf
"""
import csv
import os

import matplotlib
import numpy as np
from scipy.stats import wilcoxon

matplotlib.use("Agg")
import matplotlib.pyplot as plt                    # noqa: E402

SALIDA = "paper_caie/figures/fig_ablation.pdf"
plt.rcParams.update({"font.size": 8.0, "figure.facecolor": "white",
                     "font.family": "sans-serif", "font.sans-serif": ["Arial"],
                     "mathtext.fontset": "custom", "mathtext.rm": "Arial",
                     "mathtext.it": "Arial:italic", "mathtext.bf": "Arial:bold",
                     "pdf.fonttype": 42})
AMBAR, MARRON, GRIS = "#d68910", "#b0632c", "#5d6d7e"


def carga():
    d = {}
    for r in csv.DictReader(open("benchmarks/ablation_por_regla.csv",
                                 encoding="utf-8")):
        d.setdefault((r["objetivo"], r["terminales"]), {})[int(r["seed"])] = (
            float(r["re"]), float(r["ancho"]))
    for r in csv.DictReader(open("benchmarks/midpoint_control_por_regla.csv",
                                 encoding="utf-8")):
        d.setdefault(("crisp", "nowidth"), {})[int(r["seed"])] = (
            float(r["re"]), float(r["ancho"]))
    return d


def main():
    d = carga()
    filas = [  # etiqueta, primero, segundo, color
        ("makespan objective:\nwith $-$ without widths",
         ("makespan", "full"), ("makespan", "nowidth"), AMBAR),
        ("robust objective:\nwith $-$ without widths",
         ("robust", "full"), ("robust", "nowidth"), MARRON),
        ("midpoint control:\ncrisp $-$ interval fitness",
         ("crisp", "nowidth"), ("makespan", "nowidth"), GRIS),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(4.98, 2.1), sharey=True)
    rng = np.random.default_rng(0)
    for k, (titulo, eje) in enumerate((("(a) RE (points)", 0),
                                       ("(b) relative width (points)", 1))):
        ax = axes[k]
        for f, (etq, a, b, col) in enumerate(filas):
            semillas = sorted(set(d[a]) & set(d[b]))
            assert len(semillas) == 30, (a, b, len(semillas))
            x = np.array([d[a][s][eje] - d[b][s][eje] for s in semillas])
            y = len(filas) - 1 - f + rng.uniform(-0.18, 0.18, len(x))
            ax.plot(x, y, "o", ms=3.2, color=col, alpha=0.75, mew=0)
            ax.plot([np.median(x)], [len(filas) - 1 - f], "D", ms=5.5,
                    color="0.1", mfc="white", mew=1.1, zorder=4)
            p = wilcoxon([d[a][s][eje] for s in semillas],
                         [d[b][s][eje] for s in semillas]).pvalue
            txt = "n.s." if p >= 0.05 else ("$p<0.001$" if p < 0.001
                                            else f"$p={p:.3f}$")
            ax.text(1.0, len(filas) - 1 - f + 0.33, txt, fontsize=6.5,
                    ha="right", va="bottom", transform=ax.get_yaxis_transform())
        ax.axvline(0, color="0.3", lw=0.8, zorder=1)
        ax.set_title(titulo, loc="left", fontsize=8, pad=3)
        ax.set_ylim(-0.6, len(filas) - 0.25)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="x", alpha=0.25, linestyle=":", linewidth=0.6)
        ax.set_xlabel("paired difference")
    axes[0].set_yticks(range(len(filas)))
    axes[0].set_yticklabels([f[0] for f in filas][::-1], fontsize=7)
    fig.tight_layout(w_pad=1.2)
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    fig.savefig(SALIDA, bbox_inches="tight")
    plt.close(fig)
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
