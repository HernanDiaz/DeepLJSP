# -*- coding: utf-8 -*-
"""Frontera calidad-predictibilidad del fitness robusto -> fig_lambda.pdf.

Lee benchmarks/lambda_sweep/lambda_sweep.csv (no recalcula nada), de modo que
la figura puede regenerarse al instante cuando cambien los datos. La linea
discontinua marca el brazo evolucionado SIN terminales de anchura, que es la
referencia plana del argumento.
"""

import csv
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CSV = os.path.join(REPO, "benchmarks/lambda_sweep/lambda_sweep.csv")
OUT = os.path.join(HERE, "figures/fig_lambda.pdf")

AMBAR, GRIS = "#d68910", "#5d6d7e"
NOWIDTH = 12.42          # ancho del brazo sin terminales de anchura

rows = sorted((float(r["lambda"]), float(r["re_mean"]), float(r["re_sd"]),
               float(r["width_mean"]), float(r["width_sd"]))
              for r in csv.DictReader(open(CSV, encoding="utf-8")))

fig, ax = plt.subplots(figsize=(6.2, 3.8))

# referencia plana: el brazo sin terminales de anchura
ax.axvline(NOWIDTH, color=GRIS, linestyle="--", linewidth=1.2, zorder=1)
ymax = max(r[1] + r[2] for r in rows)
ax.text(NOWIDTH - 0.04, ymax, "without width terminals", fontsize=8,
        color=GRIS, ha="right", va="top")

# barras de error tenues para que no tapen la frontera
ax.errorbar([r[3] for r in rows], [r[1] for r in rows],
            xerr=[r[4] for r in rows], yerr=[r[2] for r in rows],
            fmt="none", ecolor=AMBAR, elinewidth=0.9, capsize=2.5,
            alpha=0.45, zorder=2)
ax.plot([r[3] for r in rows], [r[1] for r in rows], "-o", color=AMBAR,
        linewidth=1.8, markersize=5, zorder=3)

# etiquetas escalonadas: los tres lambda pequenos caen muy juntos
OFF = {0.5: (9, -9), 1.0: (10, 1), 2.0: (7, 8), 4.0: (9, 2)}
for lam, re_m, _, w_m, _ in rows:
    ax.annotate(f"$\\lambda$={lam:g}", (w_m, re_m), textcoords="offset points",
                xytext=OFF.get(lam, (8, 4)), fontsize=9, zorder=4)
ax.set_xlabel("relative width of the makespan interval (%)")
ax.set_ylabel("mean RE (%)")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(OUT)
plt.close(fig)
print(f"fig_lambda ok ({len(rows)} puntos) -> {OUT}")
