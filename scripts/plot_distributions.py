"""
Distribuciones de RE de los pools v2 vs GP-eps, por clase de tamaño.

Box plot pareado: para cada clase, la distribución de los RE (1024 soluciones
x 10 instancias) de v2 y de GP lado a lado. El box muestra cuartiles, el
whisker llega al MEJOR (min) y al peor (max), y un diamante marca la MEDIA.
Así se ven mejor/media/varianza de un vistazo.

Salida: benchmarks/figures/fig_distributions.pdf/.png
"""

import os
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa

OUT = "benchmarks/figures"
os.makedirs(OUT, exist_ok=True)
CLASSES = ["15_15", "20_15", "20_20", "30_15", "30_20", "50_15", "50_20"]
AZUL, AMBAR = "#1f5fa8", "#d68910"


def pool_res(pid, gen):
    path = f"seeds/{pid}_{gen}_pool.csv"
    if not os.path.exists(path):
        return []
    lb = lb_for_problem_name(pid)
    out = []
    for line in open(path, encoding="utf-8"):
        if ";" not in line:
            continue
        lo, up = (float(x) for x in line.split(";")[1].strip("[] \n").split(","))
        out.append(((lo + up) / 2 - lb) / lb * 100)
    return out


# recolecta RE por clase y generador (todas las instancias de la clase juntas)
data = {g: {} for g in ("v2", "gp")}
for cls in CLASSES:
    for g in ("v2", "gp"):
        vals = []
        for i in range(1, 11):
            vals += pool_res(f"int__tai{cls}_{i:02d}", g)
        data[g][cls] = vals

fig, ax = plt.subplots(figsize=(12, 6))
width = 0.36
positions_v2 = np.arange(len(CLASSES)) - width / 2 - 0.02
positions_gp = np.arange(len(CLASSES)) + width / 2 + 0.02


def box(pos, cls_data, color):
    bp = ax.boxplot([cls_data[c] for c in CLASSES], positions=pos,
                    widths=width, whis=(0, 100), patch_artist=True,
                    showmeans=True, meanprops=dict(marker="D",
                    markerfacecolor="white", markeredgecolor=color,
                    markersize=7),
                    medianprops=dict(color="white", linewidth=1.5),
                    flierprops=dict(marker="", markersize=0))
    for b in bp["boxes"]:
        b.set(facecolor=color, alpha=0.75, edgecolor=color)
    for w in bp["whiskers"] + bp["caps"]:
        w.set(color=color, linewidth=1.2)
    return bp


box(positions_v2, data["v2"], AZUL)
box(positions_gp, data["gp"], AMBAR)

ax.set_xticks(range(len(CLASSES)))
ax.set_xticklabels([c.replace("_", "×") for c in CLASSES])
ax.set_xlabel("instance size class")
ax.set_ylabel("solution RE (%) — lower is better")
ax.set_title("Pool solution distributions: v2 (blue) vs GP-ε (amber)\n"
             "box = quartiles · whiskers = best↓/worst↑ · ◇ = mean",
             fontsize=13)
ax.grid(axis="y", alpha=0.25)
ax.spines[["top", "right"]].set_visible(False)

from matplotlib.patches import Patch
ax.legend(handles=[Patch(facecolor=AZUL, alpha=0.75, label="v2 (RL)"),
                   Patch(facecolor=AMBAR, alpha=0.75, label="GP-ε")],
          frameon=False, loc="upper left")

fig.tight_layout()
fig.savefig(f"{OUT}/fig_distributions.pdf")
fig.savefig(f"{OUT}/fig_distributions.png", dpi=150)
plt.close(fig)
print(f"generada {OUT}/fig_distributions.png")

# resumen numérico por clase
print(f"\n{'clase':<7} {'v2 best':>8} {'v2 med':>7} {'v2 σ':>6} | "
      f"{'gp best':>8} {'gp med':>7} {'gp σ':>6}")
for c in CLASSES:
    v, g = np.array(data["v2"][c]), np.array(data["gp"][c])
    print(f"{c:<7} {v.min():>7.1f} {v.mean():>7.1f} {v.std():>6.1f} | "
          f"{g.min():>7.1f} {g.mean():>7.1f} {g.std():>6.1f}")
