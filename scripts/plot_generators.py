"""
Figuras de la comparativa de generadores de siembra (calidad + diversidad).
Lee benchmarks/generators_comparison.csv y pool_diversity.csv.

Salida: benchmarks/figures/
  fig_quality_diversity.pdf/.png  — scatter calidad vs diversidad estructural
  fig_class_quality.pdf/.png      — RE medio por clase (el cruce GP<->v2)
"""

import csv
import os
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, ".")
OUT = "benchmarks/figures"
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "figure.facecolor": "white"})

GEN = ["graspmor", "gtmwkr", "gp", "v2"]
LABEL = {"graspmor": "MOR-ε", "gtmwkr": "GT-ε", "gp": "GP-ε", "v2": "v2 (RL)"}
COLOR = {"graspmor": "#5d6d7e", "gtmwkr": "#0e8a7d",
         "gp": "#d68910", "v2": "#1f5fa8"}


def load(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


comp = load("benchmarks/generators_comparison.csv")
div = load("benchmarks/pool_diversity.csv")
divmap = {r["instance"]: r for r in div}


def mean(rows, key):
    vals = [float(r[key]) for r in rows if r[key] and r[key] == r[key]
            and r[key] != "nan"]
    return sum(vals) / len(vals) if vals else float("nan")


# --- Fig 1: calidad (x, menor mejor) vs diversidad estructural (y, mayor mejor)
fig, ax = plt.subplots(figsize=(7, 5))
for g in GEN:
    q = mean(comp, f"{g}_mean")
    d = mean([divmap[r["instance"]] for r in comp
              if r["instance"] in divmap], f"{g}_structdist")
    ax.scatter(q, d, s=280, color=COLOR[g], edgecolor="white",
               linewidth=1.5, zorder=3)
    ax.annotate(LABEL[g], (q, d), fontsize=13, fontweight="bold",
                xytext=(8, 8), textcoords="offset points")
ax.set_xlabel("mean pool RE (%) — lower is better  →  worse")
ax.invert_xaxis()  # mejor calidad a la derecha
ax.set_ylabel("structural diversity — higher is better")
ax.set_title("Seed generators: quality vs. diversity\n(top-right corner = "
             "high-quality AND diverse pools)", fontsize=13)
ax.grid(alpha=0.25, zorder=0)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(f"{OUT}/fig_quality_diversity.pdf")
fig.savefig(f"{OUT}/fig_quality_diversity.png", dpi=150)
plt.close(fig)

# --- Fig 2: RE medio por clase (muestra el cruce GP<->v2 en clases grandes)
CLASSES = ["15_15", "20_15", "20_20", "30_15", "30_20", "50_15", "50_20"]


def class_of(inst):
    m = re.search(r"tai(\d+_\d+)", inst)
    return m.group(1) if m else "ft10"


fig, ax = plt.subplots(figsize=(8.5, 4.6))
x = range(len(CLASSES))
for g in ("gtmwkr", "gp", "v2"):
    ys = [mean([r for r in comp if class_of(r["instance"]) == c],
               f"{g}_mean") for c in CLASSES]
    ax.plot(x, ys, "-o", color=COLOR[g], linewidth=2, markersize=7,
            label=LABEL[g])
ax.set_xticks(list(x))
ax.set_xticklabels([c.replace("_", "×") for c in CLASSES])
ax.set_xlabel("instance size class")
ax.set_ylabel("mean pool RE (%)")
ax.set_title("Pool quality by size class — GP-ε overtakes v2 on the "
             "large classes", fontsize=13)
ax.legend(frameon=False)
ax.grid(alpha=0.25)
ax.spines[["top", "right"]].set_visible(False)
# resaltar la zona de cruce
ax.axvspan(4.5, 6.5, color="#d68910", alpha=0.07)
fig.tight_layout()
fig.savefig(f"{OUT}/fig_class_quality.pdf")
fig.savefig(f"{OUT}/fig_class_quality.png", dpi=150)
plt.close(fig)

print("figuras en", OUT)
for f in sorted(os.listdir(OUT)):
    print(" -", f)
