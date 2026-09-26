# -*- coding: utf-8 -*-
"""Figura de la evolucion del articulo de C&IE: tres paneles.

La figura de paper_gp solo daba la curva de convergencia del RE de
entrenamiento. Aqui, con la mejor regla de cada generacion de las 30
evoluciones (scripts/evolucion_mejores.py):

  (a) su RE en entrenamiento, validacion y prueba: si lo que gana la
      evolucion en las cuatro instancias de entrenamiento se traslada a
      las que no ve;
  (b) su tamano, con el tope de 30 nodos;
  (c) la proporcion de terminales de anchura entre sus hojas.

En cada panel, mediana (o media en (c)) y rango intercuartilico de las
30 evoluciones. Arial, como el resto de figuras; dibujada a su tamano
final (\\linewidth).

Lee paper_caie/figures/convergence_data.json (RE de entrenamiento, con la
generacion 0) y benchmarks/evolucion_mejores.json.

    python scripts/make_convergence_caie.py

Escribe paper_caie/figures/fig_convergence.pdf
"""
import json

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt                    # noqa: E402

CONV = "paper_caie/figures/convergence_data.json"
MEJORES = "benchmarks/evolucion_mejores.json"
SALIDA = "paper_caie/figures/fig_convergence.pdf"
TOPE = 30

AZUL, AMBAR, GRIS = "#1f5fa8", "#d68910", "#5d6d7e"
plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial"],
    "font.size": 8.0, "legend.fontsize": 7.0, "pdf.fonttype": 42,
    "figure.facecolor": "white",
})


def banda(ax, g, Y, color, ls, etq, centro="mediana"):
    q1, q3 = np.percentile(Y, [25, 75], axis=0)
    c = np.median(Y, axis=0) if centro == "mediana" else np.mean(Y, axis=0)
    ax.fill_between(g, q1, q3, color=color, alpha=0.18, lw=0)
    ax.plot(g, c, ls, color=color, lw=1.2, label=etq)


def main():
    conv = json.load(open(CONV, encoding="utf-8"))
    M = json.load(open(MEJORES, encoding="utf-8"))["semillas"]
    semillas = sorted(M, key=int)
    gens = list(range(1, 51))

    def matriz(clave):
        return np.array([[M[s][str(g)][clave] for g in gens] for s in semillas])

    fig, axes = plt.subplots(1, 3, figsize=(5.0, 1.95))

    # (a) calidad: entrenamiento desde la generacion 0, y fuera de el
    ax = axes[0]
    L = min(len(v) for v in conv.values())
    ent = np.array([v[:L] for v in conv.values()])
    banda(ax, np.arange(L), ent, "black", "-", "training")
    evaluado = "val" in M[semillas[0]]["1"]
    if evaluado:
        banda(ax, gens, matriz("val"), AMBAR, "--", "validation")
        banda(ax, gens, matriz("pru"), AZUL, ":", "test")
    ax.set_xlim(0, 50)
    ax.set_ylabel("RE of the best rule (%)")
    ax.legend(frameon=False, loc="upper right", handlelength=1.8)
    ax.set_title("(a) Quality", loc="left", fontsize=8, pad=3)

    # (b) tamano del arbol
    ax = axes[1]
    banda(ax, gens, matriz("size"), GRIS, "-", "median")
    ax.axhline(TOPE, color="black", lw=0.7, ls=(0, (4, 3)))
    ax.text(1, TOPE + 0.6, "size cap", ha="left", va="bottom", fontsize=7)
    ax.set_xlim(0, 50)
    ax.set_ylim(0, TOPE + 5)
    ax.set_ylabel("Nodes")
    ax.set_title("(b) Rule size", loc="left", fontsize=8, pad=3)

    # (c) terminales de anchura
    ax = axes[2]
    banda(ax, gens, 100 * matriz("ancho"), AMBAR, "-", "mean", centro="media")
    ax.set_xlim(0, 50)
    ax.set_ylim(0, None)
    ax.set_ylabel("Width terminals (% of leaves)")
    ax.set_title("(c) Interval widths", loc="left", fontsize=8, pad=3)

    for ax in axes:
        ax.set_xlabel("Generation")
        ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(pad=0.3, w_pad=0.8)
    fig.savefig(SALIDA)
    plt.close(fig)
    print(f"escrito {SALIDA} ({'con' if evaluado else 'sin'} validacion y prueba)")


if __name__ == "__main__":
    main()
