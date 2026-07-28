# -*- coding: utf-8 -*-
"""Scatter de dominacion por instancia: la regla destacada contra el mejor
baseline (G&T-MWKR), 70 puntos coloreados por clase de tamano, con la
diagonal de igualdad. Visualiza el resultado 70/70 de 6.3.

Lee summary.csv y constructive_per_instance.csv (nada se recalcula).
"""

import csv
import os
import re
import sys
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(HERE, "figures/fig_dominance.pdf")
RULE = "gp_tuned_seed1"

plt.rcParams.update({"font.size": 11, "figure.facecolor": "white"})

BASE = {(15, 15): 0, (20, 15): 10, (20, 20): 20, (30, 15): 30,
        (30, 20): 40, (50, 15): 50, (50, 20): 60}
CLASSES = ["15x15", "20x15", "20x20", "30x15", "30x20", "50x15", "50x20"]
# 7 colores distinguibles, ordenados de claro a oscuro con el tamano
COLORS = ["#c7a740", "#d68910", "#b0632c", "#0e8a7d", "#2e6f95",
          "#5d6d7e", "#31394d"]


def ta_index(inst):
    m = re.search(r"tai(\d+)_(\d+)_(\d+)", inst)
    return BASE[(int(m.group(1)), int(m.group(2)))] + int(m.group(3))


gp = {}
cls = {}
for r in csv.DictReader(open(os.path.join(
        REPO, "benchmarks/reevo_fixedfit/summary.csv"), encoding="utf-8")):
    if r["method"] == RULE:
        i = ta_index(r["instance"])
        gp[i] = float(r["re"])
        cls[i] = r["cls"].replace("_", "x")

gt = {int(r["ta"][2:]): float(r["GT-MWKR_re"]) for r in
      csv.DictReader(open(os.path.join(
          REPO, "benchmarks/constructive_per_instance.csv"),
          encoding="utf-8"))}
assert len(gp) == len(gt) == 70

fig, ax = plt.subplots(figsize=(5.0, 5.0))
lim = (5, 50)

# mitad inferior sombreada: la region donde la regla evolucionada gana
ax.fill_between(lim, lim, (lim[0], lim[0]), color="#d68910", alpha=0.06,
                zorder=0)
ax.plot(lim, lim, color="#5d6d7e", linewidth=1.0, linestyle="--", zorder=1)
ax.text(46.5, 47.5, "equal RE", fontsize=9, color="#5d6d7e",
        ha="right", rotation=45, rotation_mode="anchor")

by_class = defaultdict(list)
for i in gp:
    by_class[cls[i]].append((gt[i], gp[i]))
for c, col in zip(CLASSES, COLORS):
    pts = by_class[c]
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=26,
               color=col, alpha=0.85, linewidths=0.4, edgecolors="white",
               label="$" + c.replace("x", "{\\times}") + "$", zorder=3)

ax.set_xlim(lim); ax.set_ylim(lim)
ax.set_aspect("equal")
ax.set_xlabel("G&T-MWKR, RE per instance (%)")
ax.set_ylabel("evolved rule, RE per instance (%)")
ax.legend(loc="upper left", fontsize=9, frameon=False, handletextpad=0.2,
          borderaxespad=0.4, labelspacing=0.35)
ax.spines[["top", "right"]].set_visible(False)

fig.tight_layout()
fig.savefig(OUT)
plt.close(fig)

wins = sum(1 for i in gp if gp[i] < gt[i])
worst = min(gp, key=lambda i: gt[i] - gp[i])
print(f"fig_dominance ok: {wins}/70 bajo la diagonal, margen minimo "
      f"{gt[worst]-gp[worst]:.2f} (TA{worst}) -> {OUT}")
