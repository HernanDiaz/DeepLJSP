# -*- coding: utf-8 -*-
"""Figura del caso ilustrativo E3: que hace el termino de anchura.

Dos paneles del mismo 3x3: arriba la regla destacada, Ec. (4); abajo la
misma regla con el termino de anchura a cero. Las dos trazas coinciden
salvo en una decision, que la figura senala.

Convencion del Gantt intervalar, la misma que el resto de la linea: cada
operacion es un poligono cuyo lado superior va de s^L a c^L y cuyo lado
inferior va de s^U a c^U, de modo que el borde de arriba es el schedule
que resulta si toda duracion toma su extremo inferior y el de abajo el
que resulta si toma el superior.

Lee benchmarks/e3_caso/caso.json, que produce e3_caso_ilustrativo.py.

    python scripts/make_e3_figure.py

Escribe paper_gp/figures/fig_case.pdf
"""
import json
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt                    # noqa: E402
from matplotlib.patches import Polygon             # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ENTRADA = "benchmarks/e3_caso/caso.json"
SALIDA = "paper_gp/figures/fig_case.pdf"

# la paleta del resto de las figuras del paper
AZUL, AMBAR, TEAL = "#1f5fa8", "#d68910", "#0e8a7d"
COLOR = [AZUL, AMBAR, TEAL]
ALTO = 0.46
# 8 pt es el tamano efectivo: la figura se genera al ancho al que se
# imprime (360 pt de \linewidth = 4.98 in), asi que LaTeX no la encoge
plt.rcParams.update({"font.size": 8.0, "figure.facecolor": "white",
                     "pdf.fonttype": 42})


def perfil(s_lo, s_up, c_lo, c_up, base):
    """Vertices del poligono. El eje y va invertido: el suelo es el mayor."""
    suelo, techo = base + ALTO / 2, base - ALTO / 2
    return [(s_lo, techo), (c_lo, techo), (c_up, suelo), (s_up, suelo)]


def panel(ax, sched, cmax, marcada, titulo, xmax, n_maq):
    for op in sched:
        es_la = (op["job"], op["op"]) == marcada
        ax.add_patch(Polygon(
            perfil(op["s_lo"], op["s_up"], op["c_lo"], op["c_up"],
                   op["machine"]),
            closed=True, facecolor=COLOR[op["job"]],
            alpha=0.95 if es_la else 0.72,
            edgecolor="0.10" if es_la else COLOR[op["job"]],
            linewidth=1.6 if es_la else 0.9, zorder=3 if es_la else 2))
        ax.text((op["s_lo"] + op["s_up"] + op["c_lo"] + op["c_up"]) / 4,
                op["machine"],
                f"$o_{{{op['job'] + 1}{op['op'] + 1}}}$",
                ha="center", va="center", fontsize=7, color="white",
                zorder=4)

    ax.axvline(cmax[0], color="0.35", linestyle="--", linewidth=0.9,
               zorder=1)
    ax.axvline(cmax[1], color="0.15", linestyle="-", linewidth=1.1,
               zorder=1)
    ax.text(cmax[1] + 3.5, -0.62,
            f"$\\mathbf{{C}}_{{\\max}} = [{cmax[0]:.0f},\\,{cmax[1]:.0f}]$",
            ha="left", va="center", fontsize=8)
    ax.set_title(titulo, loc="left", fontsize=8, pad=3)
    ax.set_yticks(range(n_maq))
    ax.set_yticklabels([str(i + 1) for i in range(n_maq)])
    ax.set_ylabel("machine")
    ax.set_ylim(-1.0, n_maq - 0.45)
    ax.set_xlim(0, xmax)
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.3, linestyle=":", linewidth=0.6)
    ax.spines[["top", "right"]].set_visible(False)


def main():
    d = json.load(open(ENTRADA, encoding="utf-8"))
    k = d["decision"]
    # la operacion que separa las dos trazas, en cada panel
    j_gp, j_b0 = d["elige"]["gp"], d["elige"]["b0"]
    op_gp = d["op_idx"][d["elegibles"].index(j_gp)]
    op_b0 = d["op_idx"][d["elegibles"].index(j_b0)]

    xmax = max(d["makespan"]["gp"][1], d["makespan"]["b0"][1]) * 1.30
    fig, axes = plt.subplots(2, 1, figsize=(4.98, 2.95), sharex=True)
    panel(axes[0], d["schedules"]["gp"], d["makespan"]["gp"],
          (j_gp, op_gp),
          f"(a) evolved rule, Eq. (4): decision {k + 1} dispatches "
          f"$o_{{{j_gp + 1}{op_gp + 1}}}$", xmax, d["num_machines"])
    panel(axes[1], d["schedules"]["b0"], d["makespan"]["b0"],
          (j_b0, op_b0),
          f"(b) width term removed ($\\beta = 0$): decision {k + 1} "
          f"dispatches $o_{{{j_b0 + 1}{op_b0 + 1}}}$", xmax,
          d["num_machines"])
    axes[1].set_xlabel("time")
    fig.tight_layout(h_pad=0.9)
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    fig.savefig(SALIDA, bbox_inches="tight")
    plt.close(fig)
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
