# -*- coding: utf-8 -*-
"""Figura del caso ilustrativo para paper_caie: la regla, sin anchura,
SPT y MWKR.

Cuatro paneles del mismo 3x3 con el mismo eje de tiempo: (a) la regla
destacada, Ec. (4); (b) la misma regla con el termino de anchura a cero,
con la operacion que separa las dos trazas senalada en ambas; (c) SPT y
(d) MWKR, cada una ejecutada por su cuenta desde el schedule vacio. Asi
se ven los huecos que dejan las dos clasicas, que el texto de 7.2 cita.

El Gantt intervalar y la paleta son los de make_e3_figure.py (la figura
de paper_gp, que no se toca): cada operacion es un poligono cuyo lado
superior va de s^L a c^L y el inferior de s^U a c^U.

Lee benchmarks/e3_caso/caso.json, que produce e3_caso_ilustrativo.py.

    python scripts/make_e3_figure_caie.py

Escribe paper_caie/figures/fig_case.pdf
"""
import json
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt                    # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_e3_figure import panel                   # noqa: E402

ENTRADA = "benchmarks/e3_caso/caso.json"
SALIDA = "paper_caie/figures/fig_case.pdf"
plt.rcParams.update({"font.size": 8.0, "figure.facecolor": "white",
                     "font.family": "sans-serif", "font.sans-serif": ["Arial"],
                     "mathtext.fontset": "custom", "mathtext.rm": "Arial",
                     "mathtext.it": "Arial:italic", "mathtext.bf": "Arial:bold",
                     "pdf.fonttype": 42})


def main():
    d = json.load(open(ENTRADA, encoding="utf-8"))
    k = d["decision"]
    j_gp, j_b0 = d["elige"]["gp"], d["elige"]["b0"]
    op_gp = d["op_idx"][d["elegibles"].index(j_gp)]
    op_b0 = d["op_idx"][d["elegibles"].index(j_b0)]
    # sitio a la derecha para la etiqueta del makespan mayor
    xmax = max(v[1] for v in d["makespan"].values()) + 62
    paneles = [
        ("gp", (j_gp, op_gp),
         f"(a) evolved rule, Eq. (4): decision {k + 1} dispatches "
         f"$o_{{{j_gp + 1}{op_gp + 1}}}$"),
        ("b0", (j_b0, op_b0),
         f"(b) width term removed ($\\beta = 0$): decision {k + 1} "
         f"dispatches $o_{{{j_b0 + 1}{op_b0 + 1}}}$"),
        ("spt", None, "(c) SPT, run on its own"),
        ("mwkr", None, "(d) MWKR, run on its own"),
    ]
    # 360 pt de \linewidth = 4.98 in: se dibuja al tamano al que se imprime
    fig, axes = plt.subplots(4, 1, figsize=(4.98, 5.2), sharex=True)
    for ax, (m, marcada, titulo) in zip(axes, paneles):
        panel(ax, d["schedules"][m], d["makespan"][m], marcada, titulo,
              xmax, d["num_machines"])
    axes[-1].set_xlabel("time")
    fig.tight_layout(h_pad=0.8)
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    fig.savefig(SALIDA, bbox_inches="tight")
    plt.close(fig)
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
