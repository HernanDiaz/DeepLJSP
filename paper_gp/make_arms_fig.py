# -*- coding: utf-8 -*-
"""Los cuatro brazos de la ablacion en el plano RE-anchura -> fig_arms.pdf

Una regla, un punto: 120 en total. Muestra lo que una tabla de medias no
puede: los brazos SIN terminales de anchura ocupan una banda estrecha haga lo
que haga el objetivo, y solo el brazo robusto CON anchura se estira a lo largo
del intercambio.

El panel de la progresion de lambda se descarto: con 10 reglas por brazo los
minimos individuales no son monotonos (estadistico de orden), y las medias,
que si lo son, ya estan en fig_lambda. Lee benchmarks/ablation_por_regla.csv.
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
CSV = os.path.join(REPO, "benchmarks/ablation_por_regla.csv")
OUT = os.path.join(HERE, "figures/fig_arms.pdf")

# 8 pt es el tamano EFECTIVO porque la figura se genera al ancho al que
# se imprime: no hay reduccion de LaTeX que encoja las letras
plt.rcParams.update({"font.size": 8.0, "figure.facecolor": "white"})
AMBAR, GRIS = "#d68910", "#5d6d7e"

pts = defaultdict(list)
for r in csv.DictReader(open(CSV, encoding="utf-8")):
    pts[(r["objetivo"], r["terminales"])].append(
        (float(r["re"]), float(r["ancho"])))

fig, ax = plt.subplots(figsize=(3.59, 2.69))
SERIES = [(("makespan", "nowidth"), GRIS, "s", False, "makespan, no widths"),
          (("makespan", "full"), AMBAR, "o", False, "makespan, full terminals"),
          (("robust", "nowidth"), GRIS, "s", True,
           r"robust $\lambda{=}1$, no widths"),
          (("robust", "full"), AMBAR, "o", True,
           r"robust $\lambda{=}1$, full terminals")]
for key, col, mk, fill, lab in SERIES:
    xs = [p[0] for p in pts[key]]
    ys = [p[1] for p in pts[key]]
    ax.scatter(xs, ys, s=30, marker=mk, label=lab,
               color=col if fill else "none", edgecolor=col,
               linewidth=1.2, alpha=0.85 if fill else 1.0, zorder=3)

ax.set_xlabel("mean RE over the 70 instances (%)")
ax.set_ylabel("relative width of the makespan interval (%)")
ax.spines[["top", "right"]].set_visible(False)
ax.legend(fontsize=7.5, frameon=False, loc="lower left",
          handletextpad=0.3, labelspacing=0.4)

fig.tight_layout()
fig.savefig(OUT)
plt.close(fig)

for k in sorted(pts):
    v = pts[k]
    print(f"{k[0]:<9}{k[1]:<9} n={len(v):<3} "
          f"ancho {min(p[1] for p in v):.2f}-{max(p[1] for p in v):.2f}")
print(f"-> {OUT}")
