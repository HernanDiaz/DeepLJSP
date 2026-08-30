# -*- coding: utf-8 -*-
"""Figura de la particion de instancias.

El paper se apoya constantemente en que instancias vio cada familia y
cuales no, y hasta ahora eso solo estaba en prosa. La figura pone las
70 Taillard por clase de tamano, marcando las cuatro de entrenamiento
y las seis de validacion (ambas de la clase 20x15, y ambas compartidas
por las dos familias), y anade aparte las doce clasicas, que ninguna
de las dos vio ni para entrenar ni para seleccionar.

    python scripts/make_split_figure.py

Escribe paper/figures/fig_split.pdf
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt                            # noqa: E402
from matplotlib.patches import Patch, Rectangle            # noqa: E402

plt.rcParams.update({"font.family": "serif", "font.size": 10,
                     "pdf.fonttype": 42})

SALIDA = "paper/figures/fig_split.pdf"
CLASES = ["15$\\times$15", "20$\\times$15", "20$\\times$20",
          "30$\\times$15", "30$\\times$20", "50$\\times$15",
          "50$\\times$20"]
ENTRENA = set(range(11, 15))     # TA11-TA14
VALIDA = set(range(15, 21))      # TA15-TA20
C_ENTRENA, C_VALIDA, C_NO = "#B2453C", "#E2A03F", "#BFD3E6"


def main():
    fig, ax = plt.subplots(figsize=(6.53, 2.15))
    ancho, alto, hueco = 1.0, 0.62, 0.55

    for c in range(7):
        for k in range(10):
            ta = c * 10 + k + 1
            x = c * (10 * ancho + hueco) + k * ancho
            if ta in ENTRENA:
                col, borde = C_ENTRENA, "0.2"
            elif ta in VALIDA:
                col, borde = C_VALIDA, "0.2"
            else:
                col, borde = C_NO, "0.55"
            ax.add_patch(Rectangle((x, 0), ancho * 0.92, alto,
                                   facecolor=col, edgecolor=borde,
                                   linewidth=0.5))
        centro = c * (10 * ancho + hueco) + 5 * ancho - ancho * 0.04
        ax.text(centro, -0.22, CLASES[c], ha="center", va="top",
                fontsize=9)
        ax.text(centro, alto + 0.12, f"TA{c * 10 + 1}--TA{c * 10 + 10}",
                ha="center", va="bottom", fontsize=7.5, color="0.35")

    # las doce clasicas, aparte y a la misma escala
    x0 = 7 * (10 * ancho + hueco) + 1.4
    for k in range(12):
        ax.add_patch(Rectangle((x0 + k * ancho, 0), ancho * 0.92, alto,
                               facecolor=C_NO, edgecolor="0.55",
                               linewidth=0.5))
    ax.text(x0 + 6 * ancho - ancho * 0.04, -0.22, "12 classical",
            ha="center", va="top", fontsize=9)
    ax.text(x0 + 6 * ancho - ancho * 0.04, alto + 0.12,
            "FT, La, ABZ", ha="center", va="bottom", fontsize=7.5,
            color="0.35")

    ax.set_xlim(-0.6, x0 + 12 * ancho + 0.6)
    ax.set_ylim(-0.95, alto + 0.95)
    ax.axis("off")
    leyenda = [
        Patch(facecolor=C_ENTRENA, edgecolor="0.2",
              label="training (4)"),
        Patch(facecolor=C_VALIDA, edgecolor="0.2",
              label="validation / selection (6)"),
        Patch(facecolor=C_NO, edgecolor="0.55",
              label="never seen by either family (60 + 12)"),
    ]
    ax.legend(handles=leyenda, frameon=False, fontsize=8.5, ncol=3,
              loc="lower center", bbox_to_anchor=(0.5, -0.10))
    fig.tight_layout()
    fig.savefig(SALIDA, bbox_inches="tight")
    plt.close(fig)
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
