# -*- coding: utf-8 -*-
"""Boxplots de eps-robustez por metodo y nivel de incertidumbre.

Lee benchmarks/robustness_ablation.csv (no recalcula el Monte Carlo), igual
que make_lambda_fig.py, de modo que la figura se regenera al instante cuando
cambien los datos.

Se dibuja al ancho REAL de impresion (\\linewidth = 360pt = 4.98in): la version
anterior se generaba a 9in y LaTeX la reducia al 55%, con lo que las etiquetas
de metodo acababan imprimiendose a ~4pt. Los tres niveles de incertidumbre van
en un solo eje agrupados, y los metodos pasan a la leyenda, que es lo que
libera el espacio para que las fuentes sean legibles.
"""

import csv
import os
import sys
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CSV = os.path.join(REPO, "benchmarks/robustness_ablation.csv")
OUT = os.path.join(HERE, "figures/fig_robustness_box.pdf")

plt.rcParams.update({"font.size": 11, "figure.facecolor": "white"})

COL = {"GP": "#d68910", "MOR": "#5d6d7e",
       "GT-MWKR": "#0e8a7d", "GP-nowidth": "#a04000"}
METHODS = ["GP", "MOR", "GT-MWKR", "GP-nowidth"]
WIDTHS = ["1.0", "1.2", "1.4"]

data = defaultdict(list)
for r in csv.DictReader(open(CSV, encoding="utf-8")):
    # el CSV ya guarda eps_bar escalado x10^3 (robustness_epsilon.py:174)
    data[(r["method"], r["width"])].append(float(r["eps_bar"]))

fig, ax = plt.subplots(figsize=(4.98, 3.0))

off = [-0.27, -0.09, 0.09, 0.27]
for m, o in zip(METHODS, off):
    pos = [g + o for g in range(len(WIDTHS))]
    bp = ax.boxplot([data[(m, w)] for w in WIDTHS], positions=pos,
                    widths=0.16, patch_artist=True, showfliers=False,
                    medianprops=dict(color="black", linewidth=0.9))
    for patch in bp["boxes"]:
        patch.set_facecolor(COL[m]); patch.set_alpha(0.75)
        patch.set_linewidth(0.8)

ax.set_xticks(range(len(WIDTHS)))
ax.set_xticklabels([f"+{round((float(w)-1)*100)}%" for w in WIDTHS])
ax.set_xlabel("interval width")
ax.set_ylabel(r"$\bar{\varepsilon}$ ($\times 10^{3}$)")
ax.set_xlim(-0.5, len(WIDTHS) - 0.5)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(handles=[Patch(facecolor=COL[m], alpha=0.75, label=m)
                   for m in METHODS],
          ncol=4, fontsize=8.5, frameon=False, loc="upper center",
          bbox_to_anchor=(0.5, 1.16), columnspacing=1.1, handlelength=1.3)

fig.tight_layout()
fig.savefig(OUT)
plt.close(fig)
n = len(data[("GP", "1.0")])
print(f"fig_robustness_box ok ({len(METHODS)} metodos x {len(WIDTHS)} anchuras,"
      f" n={n}) -> {OUT}")
