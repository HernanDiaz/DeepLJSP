"""
Robustez de las soluciones de los pools: anchura del intervalo de makespan.

Dos soluciones con el mismo E[Cmax] (punto medio) no son igual de robustas:
la de intervalo más ESTRECHO tiene el peor caso más cerca del mejor -> menos
incertidumbre en el resultado. Métrica: anchura relativa
    w = (upper - lower) / midpoint * 100   (% de incertidumbre)

Compara los 4 generadores por clase: anchura media del pool y anchura de la
MEJOR solución (la de menor upper, que es como se rankean).

Salida: benchmarks/figures/fig_robustness.pdf/.png + tabla.
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT = "benchmarks/figures"
os.makedirs(OUT, exist_ok=True)
CLASSES = ["15_15", "20_15", "20_20", "30_15", "30_20", "50_15", "50_20"]
GEN = ["graspmor", "gtmwkr", "gp", "v2"]
LABEL = {"graspmor": "MOR-ε", "gtmwkr": "GT-ε", "gp": "GP-ε", "v2": "v2 (RL)"}
COLOR = {"graspmor": "#5d6d7e", "gtmwkr": "#0e8a7d",
         "gp": "#d68910", "v2": "#1f5fa8"}


def widths(pid, gen):
    """(anchura relativa media del pool, anchura rel. del mejor por upper)."""
    path = f"seeds/{pid}_{gen}_pool.csv"
    if not os.path.exists(path):
        return None
    rels, best = [], None
    for line in open(path, encoding="utf-8"):
        if ";" not in line:
            continue
        lo, up = (float(x) for x in line.split(";")[1].strip("[] \n").split(","))
        mid = (lo + up) / 2
        rel = (up - lo) / mid * 100 if mid else 0.0
        rels.append(rel)
        if best is None or up < best[0]:
            best = (up, rel)
    return (sum(rels) / len(rels), best[1]) if rels else None


pool_w = {g: {c: [] for c in CLASSES} for g in GEN}
best_w = {g: {c: [] for c in CLASSES} for g in GEN}
for cls in CLASSES:
    for i in range(1, 11):
        pid = f"int__tai{cls}_{i:02d}"
        for g in GEN:
            r = widths(pid, g)
            if r:
                pool_w[g][cls].append(r[0])
                best_w[g][cls].append(r[1])


def cmean(d, g, c):
    return np.mean(d[g][c]) if d[g][c] else np.nan


# --- figura: anchura media del pool por clase, una línea por generador ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
x = np.arange(len(CLASSES))
for g in GEN:
    ax1.plot(x, [cmean(pool_w, g, c) for c in CLASSES], "-o",
             color=COLOR[g], linewidth=2, label=LABEL[g])
    ax2.plot(x, [cmean(best_w, g, c) for c in CLASSES], "-o",
             color=COLOR[g], linewidth=2, label=LABEL[g])
for ax, title in ((ax1, "anchura media del pool"),
                  (ax2, "anchura de la MEJOR solución")):
    ax.set_xticks(x)
    ax.set_xticklabels([c.replace("_", "×") for c in CLASSES], rotation=30)
    ax.set_xlabel("clase de tamaño")
    ax.set_ylabel("anchura relativa del intervalo (%)")
    ax.set_title(title)
    ax.grid(alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)
ax1.legend(frameon=False, fontsize=10)
fig.suptitle("Robustez de las soluciones: anchura del intervalo de makespan "
             "(menor = más robusto)", fontsize=13)
fig.tight_layout()
fig.savefig(f"{OUT}/fig_robustness.pdf")
fig.savefig(f"{OUT}/fig_robustness.png", dpi=150)
plt.close(fig)
print(f"generada {OUT}/fig_robustness.png\n")

# --- tabla ---
print("ANCHURA RELATIVA MEDIA DEL POOL (%)")
print(f"{'clase':<7}" + "".join(f"{LABEL[g]:>10}" for g in GEN))
allg = {g: [] for g in GEN}
for c in CLASSES:
    print(f"{c:<7}" + "".join(f"{cmean(pool_w, g, c):>9.1f}%" for g in GEN))
    for g in GEN:
        allg[g] += pool_w[g][c]
print(f"{'GLOBAL':<7}" + "".join(f"{np.mean(allg[g]):>9.1f}%" for g in GEN))

print("\nANCHURA RELATIVA DE LA MEJOR SOLUCIÓN (%)")
print(f"{'clase':<7}" + "".join(f"{LABEL[g]:>10}" for g in GEN))
allg = {g: [] for g in GEN}
for c in CLASSES:
    print(f"{c:<7}" + "".join(f"{cmean(best_w, g, c):>9.1f}%" for g in GEN))
    for g in GEN:
        allg[g] += best_w[g][c]
print(f"{'GLOBAL':<7}" + "".join(f"{np.mean(allg[g]):>9.1f}%" for g in GEN))
