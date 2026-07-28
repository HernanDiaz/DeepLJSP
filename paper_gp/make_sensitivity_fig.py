# -*- coding: utf-8 -*-
"""Sensibilidad de la regla destacada a sus coeficientes -> fig_sensitivity.pdf

Dos paneles con eje y comun: RE medio sobre las 70 instancias al variar el
peso de PT (alpha, evolucionado 2) y el de WKRW (beta, evolucionado 1). Linea
vertical en el valor evolucionado; referencia horizontal en la media de las
30 evoluciones. Lee benchmarks/coefficient_sweep.csv, no recalcula nada.
"""

import csv
import os
import sys
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CSV = os.path.join(REPO, "benchmarks/coefficient_sweep.csv")
OUT = os.path.join(HERE, "figures/fig_sensitivity.pdf")

plt.rcParams.update({"font.size": 11, "figure.facecolor": "white"})
AMBAR, GRIS = "#d68910", "#5d6d7e"
MEAN30 = 18.99          # media de las 30 evoluciones (tab:gp70)

data = defaultdict(list)
for r in csv.DictReader(open(CSV, encoding="utf-8")):
    data[r["coef"]].append((float(r["value"]), float(r["re"])))

fig, axes = plt.subplots(1, 2, figsize=(6.4, 3.2), sharey=True)
PANELS = [("alpha_PT", r"weight $\alpha$ of $\mathit{PT}$", 2.0),
          ("beta_WKRW", r"weight $\beta$ of $\mathit{WKRW}$", 1.0)]

for ax, (key, label, evolved) in zip(axes, PANELS):
    pts = sorted(data[key])
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    ax.axhline(MEAN30, color=GRIS, linestyle=":", linewidth=1.0, zorder=1)
    ax.axvline(evolved, color=GRIS, linestyle="--", linewidth=1.0, zorder=1)
    ax.plot(xs, ys, "-o", color=AMBAR, linewidth=1.6, markersize=3.5,
            zorder=3)
    ax.set_xlabel(label)
    ax.spines[["top", "right"]].set_visible(False)

axes[0].set_ylabel("mean RE over the 70 instances (%)")
axes[0].text(2.1, MEAN30, " mean of 30 evolutions", fontsize=8, color=GRIS,
             va="bottom")
axes[1].annotate("evolved value", xy=(1.0, 0), xycoords=("data",
                 "axes fraction"), xytext=(4, 6), textcoords="offset points",
                 fontsize=8, color=GRIS)
axes[0].annotate("evolved value", xy=(2.0, 0), xycoords=("data",
                 "axes fraction"), xytext=(4, 6), textcoords="offset points",
                 fontsize=8, color=GRIS)

fig.tight_layout()
fig.savefig(OUT)
plt.close(fig)
for key, _, evolved in PANELS:
    pts = dict(sorted(data[key]))
    best = min(pts, key=pts.get)
    print(f"{key}: en el valor evolucionado {evolved} -> RE "
          f"{pts.get(evolved, float('nan')):.2f}; minimo del barrido "
          f"{pts[best]:.2f} en {best}")
print(f"-> {OUT}")
