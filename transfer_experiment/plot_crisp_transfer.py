"""Figura de la transferencia a crisp: RE intervalo vs RE crisp por instancia."""
import csv
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "benchmarks/figures"
os.makedirs(OUT, exist_ok=True)
rows = list(csv.DictReader(open("benchmarks/crisp_transfer.csv", encoding="utf-8")))

fig, ax = plt.subplots(figsize=(6.5, 6.5))
COL = {"gp": "#d68910", "v2": "#1f5fa8"}
LAB = {"gp": "GP-ε", "v2": "v2 (RL)"}
for g in ("gp", "v2"):
    xs = [float(r[f"{g}_int_mean"]) for r in rows]  # RE intervalo (media pool)
    ys = [float(r[f"{g}_crisp_mean"]) for r in rows]  # RE crisp (media pool)
    ax.scatter(xs, ys, s=45, color=COL[g], alpha=0.7, edgecolor="white",
               linewidth=0.5, label=LAB[g])
lims = [8, 42]
ax.plot(lims, lims, "--", color="gray", linewidth=1.3, label="y = x (sin pérdida)")
ax.set_xlim(lims); ax.set_ylim(lims)
ax.set_xlabel("RE bajo evaluación INTERVALO (E[Cmax], %)")
ax.set_ylabel("RE bajo evaluación CRISP (%)")
ax.set_title("Transferencia intervalo → crisp (media del pool por instancia)\n"
             "puntos sobre la diagonal = la calidad se conserva", fontsize=12)
ax.legend(frameon=False)
ax.grid(alpha=0.25)
ax.spines[["top", "right"]].set_visible(False)
ax.set_aspect("equal")
fig.tight_layout()
fig.savefig(f"{OUT}/fig_crisp_transfer.pdf")
fig.savefig(f"{OUT}/fig_crisp_transfer.png", dpi=150)
print(f"generada {OUT}/fig_crisp_transfer.png")
