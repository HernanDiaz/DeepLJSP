"""Figura resumen: transferencia intervalo -> crisp y -> fuzzy (dos paneles)."""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "benchmarks/figures"
os.makedirs(OUT, exist_ok=True)
COL = {"gp": "#d68910", "v2": "#1f5fa8"}
LAB = {"gp": "GP-ε", "v2": "v2 (RL)"}

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
for ax, (csvf, ykey, titulo) in zip(axes, [
        ("benchmarks/crisp_transfer.csv", "crisp_mean", "→ CRISP"),
        ("benchmarks/fuzzy_transfer.csv", "fuzzy_mean", "→ FUZZY (E[C])")]):
    rows = list(csv.DictReader(open(csvf, encoding="utf-8")))
    for g in ("gp", "v2"):
        xs = [float(r[f"{g}_int_mean"]) for r in rows]
        ys = [float(r[f"{g}_{ykey}"]) for r in rows]
        ax.scatter(xs, ys, s=40, color=COL[g], alpha=0.7,
                   edgecolor="white", linewidth=0.5, label=LAB[g])
    lims = [8, 42]
    ax.plot(lims, lims, "--", color="gray", linewidth=1.2, label="y = x")
    ax.set_xlim(lims); ax.set_ylim(lims); ax.set_aspect("equal")
    ax.set_xlabel("RE bajo evaluación INTERVALO (%)")
    ax.set_ylabel("RE bajo la evaluación destino (%)")
    ax.set_title(f"Transferencia {titulo}")
    ax.grid(alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=9)
fig.suptitle("Las semillas de intervalo transfieren sin pérdida a crisp y a "
             "fuzzy\n(puntos sobre la diagonal · Spearman intervalo→destino "
             "≈ 0.995–0.998)", fontsize=12)
fig.tight_layout()
fig.savefig(f"{OUT}/fig_transfer_summary.pdf")
fig.savefig(f"{OUT}/fig_transfer_summary.png", dpi=150)
print(f"generada {OUT}/fig_transfer_summary.png")
