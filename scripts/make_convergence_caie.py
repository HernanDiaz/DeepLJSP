# -*- coding: utf-8 -*-
"""Figura de convergencia del articulo de C&IE, en estilo de revista.

La de paper_gp/make_figures.py (que sigue siendo la de paper_gp) pintaba
las 30 curvas casi transparentes y la media gruesa en ambar con halo, en
tipografia sin serifa: se leia como un grafico de divulgacion. Aqui:

  - tipografia Arial, la que Elsevier pide en las figuras, como el resto
    (fonttype 42 la incrusta como TrueType, sin Type 3);
  - la mediana en trazo fino, el rango intercuartilico sombreado y el
    rango completo en gris claro: la distribucion de las 30 evoluciones
    sin dibujar treinta lineas;
  - dibujada a su tamano final (0.8 \\linewidth), sin reescalado.

Lee paper_caie/figures/convergence_data.json (mejor RE de entrenamiento
por generacion y semilla, extraido de los logs de la campana).

    python scripts/make_convergence_caie.py

Escribe paper_caie/figures/fig_convergence.pdf
"""
import json
import os

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt                    # noqa: E402

DATOS = "paper_caie/figures/convergence_data.json"
SALIDA = "paper_caie/figures/fig_convergence.pdf"

plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial"],
    "font.size": 8.0, "legend.fontsize": 7.5, "pdf.fonttype": 42,
    "figure.facecolor": "white",
})


def main():
    curvas = json.load(open(DATOS, encoding="utf-8"))
    L = min(len(v) for v in curvas.values())
    Y = np.array([v[:L] for v in curvas.values()])
    g = np.arange(L)
    q0, q1, q2, q3, q4 = np.percentile(Y, [0, 25, 50, 75, 100], axis=0)

    fig, ax = plt.subplots(figsize=(4.0, 2.25))
    ax.fill_between(g, q0, q4, color="0.88", lw=0, label="Range")
    ax.fill_between(g, q1, q3, color="0.66", lw=0, label="Interquartile range")
    ax.plot(g, q2, color="black", lw=1.0, label="Median")
    ax.set_xlim(0, L - 1)
    ax.set_ylim(10, 42)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Best training RE (%)")
    ax.legend(frameon=False, loc="upper right", handlelength=1.8)
    fig.tight_layout(pad=0.3)
    fig.savefig(SALIDA)
    plt.close(fig)
    print(f"escrito {SALIDA}: {len(curvas)} evoluciones, {L} generaciones")


if __name__ == "__main__":
    main()
