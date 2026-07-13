"""Figura del hallazgo estocástico: correlación intervalo->esperado vs ->CVaR."""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "benchmarks/figures"
os.makedirs(OUT, exist_ok=True)
rows = list(csv.DictReader(open("benchmarks/stochastic_transfer.csv", encoding="utf-8")))
COL = {"gp": "#d68910", "v2": "#1f5fa8"}
LAB = {"gp": "GP-ε", "v2": "v2 (RL)"}

fig, ax = plt.subplots(figsize=(6.8, 6.8))
above = 0
tot = 0
for g in ("gp", "v2"):
    xs = [float(r[f"{g}_sp_exp"]) for r in rows]
    ys = [float(r[f"{g}_sp_cvar"]) for r in rows]
    ax.scatter(xs, ys, s=45, color=COL[g], alpha=0.7,
               edgecolor="white", linewidth=0.5, label=LAB[g])
    above += sum(1 for a, b in zip(xs, ys) if b > a)
    tot += len(xs)
lims = [0.93, 1.001]
ax.plot(lims, lims, "--", color="gray", linewidth=1.3, label="y = x")
ax.set_xlim(lims); ax.set_ylim(lims); ax.set_aspect("equal")
ax.set_xlabel("Spearman  intervalo → makespan ESPERADO\n(riesgo-neutral)")
ax.set_ylabel("Spearman  intervalo → CVaR-95\n(riesgo-averso)")
ax.set_title("Las semillas de intervalo se alinean MEJOR con el objetivo\n"
             f"riesgo-averso (CVaR): {above}/{tot} instancias sobre la diagonal",
             fontsize=12)
ax.legend(frameon=False, loc="lower right")
ax.grid(alpha=0.25)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(f"{OUT}/fig_stochastic_risk.pdf")
fig.savefig(f"{OUT}/fig_stochastic_risk.png", dpi=150)
print(f"generada {OUT}/fig_stochastic_risk.png ({above}/{tot} sobre diagonal)")
