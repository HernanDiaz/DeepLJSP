# -*- coding: utf-8 -*-
"""Graphical abstract para Applied Soft Computing.

ASOC lo exige en el envio: 531 x 1328 px (alto x ancho) o proporcionalmente
mas, legible a 5 x 13 cm. Se dibuja a ese tamano final (13 cm de ancho, alto
en la proporcion 531/1328), asi que el cuerpo de letra del codigo es el que se
ve impreso.

Tres paneles: el problema (duraciones en intervalo), el metodo (la regla
destacada, Eq. besttree del articulo) y los resultados. Las cifras son las del
articulo; si cambian alli, hay que cambiarlas aqui.

    python paper_asoc/make_graphical_abstract.py

Deja graphical_abstract.pdf (vectorial) y graphical_abstract.tif
(2656 x 1062 px, el doble del minimo) junto a este fichero.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))

# la paleta de las figuras del articulo (paper_gp/make_figures.py)
AZUL, AMBAR, GRIS, TEAL = "#1f5fa8", "#d68910", "#5d6d7e", "#0e8a7d"
TINTA = "#1c2833"

# cifras del articulo: resumen, tabla de resultados y seccion de robustez
RE_REGLA = 17.71      # regla destacada, elegida en validacion
RE_MEDIA = 18.99      # media de las 30 reglas
RE_GT = 29.5          # G&T-MWKR, la mejor constructiva
MENOS_DESV = 34.5     # regla lambda=4 frente a G&T-MWKR, mismo makespan

plt.rcParams.update({"font.size": 6.0, "font.family": "DejaVu Sans",
                     "pdf.fonttype": 42, "figure.facecolor": "white"})

CM = 1 / 2.54
W = 13.0
H = W * 531 / 1328
fig = plt.figure(figsize=(W * CM, H * CM))

CUERPO = 5.6   # texto de los paneles: legible a 13 cm de ancho


def caja(x, y, w, h, titulo):
    ax = fig.add_axes([x, y, w, h])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.01, 0.01), 0.98, 0.98,
                                boxstyle="round,pad=0,rounding_size=0.04",
                                linewidth=0.8, edgecolor="#c5ccd3",
                                facecolor="#f7f9fb"))
    ax.text(0.5, 0.9, titulo, ha="center", va="center", fontsize=7,
            fontweight="bold", color=TINTA)
    return ax


def texto(ax, y, s, color=TINTA, size=CUERPO, **kw):
    ax.text(0.5, y, s, ha="center", va="center", fontsize=size, color=color,
            linespacing=1.25, **kw)


# --- panel 1: el problema ---------------------------------------------------
a1 = caja(0.01, 0.03, 0.30, 0.94, "Interval job shop")
texto(a1, 0.76, "durations known\nonly by their bounds")
ops = [  # maquina, inicio, minimo, maximo, color
    (0, 0.12, 0.20, 0.30, AZUL), (0, 0.46, 0.16, 0.24, AMBAR),
    (1, 0.12, 0.12, 0.20, AMBAR), (1, 0.36, 0.22, 0.32, TEAL),
    (2, 0.20, 0.18, 0.28, TEAL), (2, 0.54, 0.14, 0.22, AZUL),
]
for m, x0, lo, up, c in ops:
    y = 0.50 - m * 0.13
    a1.add_patch(Rectangle((x0, y), lo, 0.09, facecolor=c, edgecolor="none"))
    a1.add_patch(Rectangle((x0 + lo, y), up - lo, 0.09, facecolor=c,
                           alpha=0.3, edgecolor=c, linewidth=0.5,
                           hatch="////"))
for m in range(3):
    a1.text(0.09, 0.545 - m * 0.13, f"M{m + 1}", ha="right", va="center",
            fontsize=CUERPO, color=GRIS)
a1.add_patch(Rectangle((0.14, 0.165), 0.07, 0.05, facecolor=GRIS,
                       edgecolor="none"))
a1.text(0.23, 0.19, "lower bound", va="center", fontsize=CUERPO, color=GRIS)
a1.add_patch(Rectangle((0.14, 0.085), 0.07, 0.05, facecolor=GRIS, alpha=0.3,
                       edgecolor=GRIS, linewidth=0.5, hatch="////"))
a1.text(0.23, 0.11, "width", va="center", fontsize=CUERPO, color=GRIS)

# --- panel 2: el metodo ------------------------------------------------------
a2 = caja(0.345, 0.03, 0.30, 0.94, "GP hyper-heuristic")
texto(a2, 0.75, "evolves priority rules over\nworst-case values and widths")
a2.add_patch(FancyBboxPatch((0.05, 0.41), 0.90, 0.16,
                            boxstyle="round,pad=0,rounding_size=0.03",
                            facecolor="white", edgecolor=AZUL, linewidth=0.9))
texto(a2, 0.49, r"$\mathit{SLACK}^{2} + 2\,\mathit{PT} - \mathit{WKR}"
      r" - \mathit{WKRW} - 1$", color=AZUL, size=5.6)
texto(a2, 0.25, "one pass, milliseconds\ntrained on four 20$\\times$15 instances")
texto(a2, 0.08, "rule selected on validation", color=GRIS, style="italic")

# --- panel 3: los resultados -------------------------------------------------
a3 = caja(0.68, 0.03, 0.31, 0.94, "70 Taillard instances")
texto(a3, 0.77, "relative error, lower is better", color=GRIS)
bx = fig.add_axes([0.80, 0.42, 0.135, 0.29])
bx.set_facecolor("none")
nombres = ["selected rule", "mean of 30", "G&T-MWKR"]
vals = [RE_REGLA, RE_MEDIA, RE_GT]
cols = [AZUL, "#7fa6d3", GRIS]
bx.barh(range(3), vals, color=cols, height=0.62)
bx.set_yticks(range(3))
bx.set_yticklabels(nombres, fontsize=CUERPO)
bx.invert_yaxis()
bx.set_xlim(0, 36)
bx.set_xticks([])
for s in ("top", "right", "bottom"):
    bx.spines[s].set_visible(False)
bx.spines["left"].set_color("#9aa5b1")
bx.tick_params(axis="y", length=0, pad=2)
for i, v in enumerate(vals):
    bx.text(v + 0.8, i, f"{v:.2f}%" if i < 2 else f"{v:.1f}%",
            va="center", fontsize=CUERPO, color=TINTA)
texto(a3, 0.27, "zero-shot across all sizes")
texto(a3, 0.11, f"robust rule: {MENOS_DESV}% less deviation\n"
      "than G&T-MWKR, similar makespan", color=TEAL)

# flechas entre paneles
for x0, x1 in ((0.313, 0.343), (0.648, 0.678)):
    fig.patches.append(FancyArrowPatch((x0, 0.5), (x1, 0.5),
                                       transform=fig.transFigure,
                                       arrowstyle="-|>", mutation_scale=7,
                                       color=GRIS, linewidth=0.9))

fig.savefig(os.path.join(HERE, "graphical_abstract.pdf"))
fig.savefig(os.path.join(HERE, "graphical_abstract.tif"),
            dpi=2656 / (W * CM), pil_kwargs={"compression": "tiff_lzw"})
print("graphical_abstract.pdf y .tif")
