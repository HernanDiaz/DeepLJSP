# -*- coding: utf-8 -*-
"""Figura de 7.4 (paper_caie): las ablaciones, brazo a brazo.

Las 30 reglas de cada brazo, cada una promediada sobre las 70 instancias,
en RE (a) y en anchura relativa del intervalo de makespan previsto (b).
Los brazos son muestras independientes (con otro conjunto de terminales
o otra fitness la evolucion no comparte nada con la de la misma
semilla), asi que no se dibujan diferencias por semilla: cada fila es un
brazo, el rombo su mediana, y la etiqueta el Mann-Whitney de
scripts/brazos_mw.py frente al brazo de referencia de su grupo.

Lee benchmarks/ablation_por_regla.csv,
benchmarks/midpoint_control_por_regla.csv y benchmarks/brazos_mw.json.

    python scripts/make_ablation_fig_caie.py

Escribe paper_caie/figures/fig_ablation.pdf
"""
import csv
import json
import os

import matplotlib
import numpy as np

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
        d.setdefault((r["objetivo"], r["terminales"]), []).append(
            (float(r["re"]), float(r["ancho"])))
    d[("crisp", "nowidth")] = [(float(r["re"]), float(r["ancho"])) for r in
                               csv.DictReader(open(
                                   "benchmarks/midpoint_control_por_regla.csv",
                                   encoding="utf-8"))]
    return d


def etiqueta(c):
    p = c["p_holm"]
    return "n.s." if c["p"] >= 0.05 else ("$p<0.001$" if c["p"] < 0.001
                                           else "$p<0.01$" if c["p"] < 0.01
                                           else "$p<0.05$")


def main():
    d = carga()
    T = json.load(open("benchmarks/brazos_mw.json", encoding="utf-8"))["ablacion"]
    # filas de arriba abajo: brazo, etiqueta, color, relleno, contraste
    filas = [
        (("makespan", "full"), "makespan objective, with widths", AMBAR, True, None),
        (("makespan", "nowidth"), "makespan objective, without widths", AMBAR, False,
         "makespan"),
        (("crisp", "nowidth"), "crisp midpoint control", GRIS, False, "crisp"),
        (("robust", "full"), "robust objective, with widths", MARRON, True, None),
        (("robust", "nowidth"), "robust objective, without widths", MARRON, False,
         "robust"),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(4.98, 2.5), sharey=True)
    rng = np.random.default_rng(0)
    ys = [4.4, 3.4, 2.4, 1.0, 0.0]
    for k, (titulo, med) in enumerate((("(a) RE (%)", "re"),
                                       ("(b) relative width (%)", "ancho"))):
        ax = axes[k]
        for (brazo, etq, col, lleno, con), y in zip(filas, ys):
            x = np.array([v[k] for v in d[brazo]])
            assert len(x) == 30
            ax.plot(x, y + rng.uniform(-0.2, 0.2, len(x)), "o", ms=3.0,
                    color=col, mfc=col if lleno else "white", mew=0.9,
                    alpha=0.85)
            ax.plot([np.median(x)], [y], "D", ms=5.5, color="0.1",
                    mfc="white", mew=1.1, zorder=4)
            if con is not None:
                ax.text(1.0, y + 0.3, etiqueta(T[f"{con}/{med}"]),
                        fontsize=6.5, ha="right", va="bottom",
                        transform=ax.get_yaxis_transform())
        ax.set_title(titulo, loc="left", fontsize=8, pad=3)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="x", alpha=0.25, linestyle=":", linewidth=0.6)
        ax.axhline(1.7, color="0.8", lw=0.6)
    axes[0].set_yticks(ys)
    axes[0].set_yticklabels([f[1] for f in filas], fontsize=7)
    axes[0].set_ylim(-0.6, 5.0)
    fig.tight_layout(w_pad=1.2)
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    fig.savefig(SALIDA, bbox_inches="tight")
    plt.close(fig)
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
