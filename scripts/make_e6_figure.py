# -*- coding: utf-8 -*-
"""Figura de E6: calidad frente a presupuesto, en las dos monedas.

Panel (a), evaluaciones de schedule, que es la moneda independiente de
la implementacion y la que pide la revision. Panel (b), segundos de esta
implementacion, donde la regla paga por calcular nueve atributos por
elegible en cada decision y el genetico no paga nada por decodificar una
permutacion ya fijada.

Ninguna curva se prolonga mas alla de su ultimo punto medido.

Lee benchmarks/e6_presupuesto/resumen.json, que produce e6_analiza.py.

    python scripts/make_e6_figure.py

Escribe paper_gp/figures/fig_budget.pdf
"""
import json
import os
import sys

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt                    # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ENTRADA = "benchmarks/e6_presupuesto/resumen.json"
SALIDA = "paper_gp/figures/fig_budget.pdf"

AZUL, AMBAR, GRIS, TEAL = "#1f5fa8", "#d68910", "#5d6d7e", "#0e8a7d"
GRANATE = "#8e2f4a"
ESTILO = {
    "azar":        (GRIS, ":", "random permutations"),
    "ga":          (GRANATE, "-", "genetic algorithm"),
    "ga_sembrado": (TEAL, "-", "GA seeded with the rule"),
    "regla_bon":   (AMBAR, "-", "evolved rule, best-of-$N$"),
}
LINEAS = {"regla": (AZUL, "evolved rule, one pass"),
          "gt_mwkr": ("0.35", "G&T-MWKR, one pass")}
plt.rcParams.update({"font.size": 8.0, "figure.facecolor": "white",
                     "pdf.fonttype": 42})


def main():
    d = json.load(open(ENTRADA, encoding="utf-8"))
    fig, axes = plt.subplots(1, 2, figsize=(4.98, 2.25))

    # --- (a) evaluaciones ---------------------------------------------
    ax = axes[0]
    for m, (col, ls, etq) in ESTILO.items():
        if m not in d["por_evaluaciones"]:
            continue
        fila = {int(k): v for k, v in d["por_evaluaciones"][m].items()}
        x = sorted(fila)
        ax.plot(x, [fila[k] for k in x], ls, color=col, lw=1.3, label=etq)
    for m, (col, etq) in LINEAS.items():
        if m in d["por_evaluaciones"]:
            ax.axhline(float(d["por_evaluaciones"][m]["1"]), color=col,
                       lw=1.0, ls="--", label=etq)
    ax.set_xscale("log")
    ax.set_xlabel("schedule evaluations")
    ax.set_ylabel("RE (%)")
    ax.set_title("(a)", loc="left", fontsize=8, pad=3)

    # --- (b) reloj ------------------------------------------------------
    ax = axes[1]
    t = np.array(d["rejilla_reloj"], dtype=float)
    for m, (col, ls, etq) in ESTILO.items():
        if m not in d["por_reloj"]:
            continue
        y = np.array(d["por_reloj"][m], dtype=float)
        ok = ~np.isnan(y)
        ax.plot(t[ok], y[ok], ls, color=col, lw=1.3)
    for m, (col, _) in LINEAS.items():
        if m in d["por_evaluaciones"]:
            ax.axhline(float(d["por_evaluaciones"][m]["1"]), color=col,
                       lw=1.0, ls="--")
    ax.set_xscale("log")
    # la rejilla del reloj llega a un milisegundo, pero ningun metodo
    # mide ahi: el eje se ajusta a donde hay datos
    hay = [t[i] for m in d["por_reloj"]
           for i, y in enumerate(d["por_reloj"][m]) if not np.isnan(y)]
    if hay:
        ax.set_xlim(min(hay) / 2, max(hay) * 2)
    ax.set_xlabel("seconds per instance")
    ax.set_title("(b)", loc="left", fontsize=8, pad=3)

    tope = float(d["por_evaluaciones"]["regla"]["1"]) * 3.2
    for ax in axes:
        ax.set_ylim(0, tope)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(alpha=0.25, linestyle=":", linewidth=0.6)
    axes[1].set_yticklabels([])

    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=3, frameon=False,
               fontsize=7, bbox_to_anchor=(0.5, -0.16))
    fig.tight_layout(w_pad=1.0)
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    fig.savefig(SALIDA, bbox_inches="tight")
    plt.close(fig)
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
