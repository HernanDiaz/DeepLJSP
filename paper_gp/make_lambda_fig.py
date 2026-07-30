# -*- coding: utf-8 -*-
"""Frontera calidad-predictibilidad del fitness robusto -> fig_lambda.pdf.

Dos curvas, una por brazo:
  - CON terminales de anchura: benchmarks/lambda_sweep/lambda_sweep_tuned.csv
    (medias ya agregadas; lambda = 0.5, 1, 2, 4).
  - SIN terminales de anchura: se agrega aqui desde los CSV por regla,
    lambda_nowidth_por_regla_completo.csv (0, 0.5, 2, 4; n=10) mas el punto
    lambda=1 del 2x2 (ablation_por_regla.csv; n=30).

Hasta que termino el barrido ablacionado la figura llevaba una linea vertical
discontinua como referencia; con el barrido completo la referencia pasa a ser
una curva de verdad, y se VE que no es curva: el ancho del brazo sin anchuras
recorre 0.13 puntos entre lambda=0 y lambda=4 mientras el brazo completo
recorre 1.65. No recalcula nada costoso: solo lee CSVs.
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
CSV_FULL = os.path.join(REPO, "benchmarks/lambda_sweep/lambda_sweep_tuned.csv")
CSV_NW = os.path.join(REPO, "benchmarks/lambda_nowidth_por_regla_completo.csv")
CSV_2X2 = os.path.join(REPO, "benchmarks/ablation_por_regla.csv")
OUT = os.path.join(HERE, "figures/fig_lambda.pdf")

# 8 pt es el tamano EFECTIVO porque la figura se genera al ancho al que
# se imprime: no hay reduccion de LaTeX que encoja las letras
plt.rcParams.update({"font.size": 8.0, "figure.facecolor": "white"})

AMBAR, GRIS = "#d68910", "#5d6d7e"


def stats(v):
    n = len(v)
    mu = sum(v) / n
    sd = (sum((x - mu) ** 2 for x in v) / (n - 1)) ** 0.5 if n > 1 else 0.0
    return mu, sd


# --- brazo completo: medias ya agregadas ----------------------------------
full = sorted((float(r["lambda"]), float(r["re_mean"]), float(r["re_sd"]),
               float(r["width_mean"]), float(r["width_sd"]))
              for r in csv.DictReader(open(CSV_FULL, encoding="utf-8")))

# --- brazo sin anchuras: agregar por lambda desde los CSV por regla -------
acc = defaultdict(lambda: ([], []))
for r in csv.DictReader(open(CSV_NW, encoding="utf-8")):
    acc[float(r["lam"])][0].append(float(r["re"]))
    acc[float(r["lam"])][1].append(float(r["ancho"]))
for r in csv.DictReader(open(CSV_2X2, encoding="utf-8")):
    if r["objetivo"] == "robust" and r["terminales"] == "nowidth":
        acc[1.0][0].append(float(r["re"]))
        acc[1.0][1].append(float(r["ancho"]))

nw = []
for lam in sorted(acc):
    re_m, re_s = stats(acc[lam][0])
    w_m, w_s = stats(acc[lam][1])
    nw.append((lam, re_m, re_s, w_m, w_s, len(acc[lam][0])))

fig, ax = plt.subplots(figsize=(3.99, 2.37))

# dispersion en gris fino y detras, comun a ambas curvas
for rows, color in ((full, AMBAR), ([r[:5] for r in nw], GRIS)):
    ax.errorbar([r[3] for r in rows], [r[1] for r in rows],
                xerr=[r[4] for r in rows], yerr=[r[2] for r in rows],
                fmt="none", ecolor=GRIS, elinewidth=0.7, capsize=2,
                capthick=0.7, alpha=0.45, zorder=2)

ax.plot([r[3] for r in full], [r[1] for r in full], "-o", color=AMBAR,
        linewidth=1.8, markersize=5, zorder=3,
        label="with width terminals")
ax.plot([r[3] for r in nw], [r[1] for r in nw], "-s", color=GRIS,
        linewidth=1.4, markersize=4, zorder=3,
        label="without width terminals")

# etiquetas escalonadas; en el brazo ablacionado los cinco puntos caen en
# 0.13 puntos de ancho, asi que solo se rotulan los extremos
OFF = {0.5: (9, -9), 1.0: (10, 1), 2.0: (7, 8), 4.0: (9, 2)}
for lam, re_m, _, w_m, _ in full:
    ax.annotate(f"$\\lambda$={lam:g}", (w_m, re_m), textcoords="offset points",
                xytext=OFF.get(lam, (8, 4)), fontsize=7.5, zorder=4)
OFF_NW = {0.0: (6, -11), 4.0: (-2, 7)}
for lam, re_m, _, w_m, _, _ in nw:
    if lam in OFF_NW:
        ax.annotate(f"$\\lambda$={lam:g}", (w_m, re_m), color=GRIS,
                    textcoords="offset points", xytext=OFF_NW[lam],
                    fontsize=7.5, zorder=4)

ax.set_xlabel("relative width of the makespan interval (%)")
ax.set_ylabel("mean RE (%)")
ax.legend(fontsize=7.5, frameon=False, loc="upper left")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(OUT)
plt.close(fig)
rango_nw = max(r[3] for r in nw) - min(r[3] for r in nw)
rango_f = max(r[3] for r in full) - min(r[3] for r in full)
print(f"fig_lambda ok: brazo completo {len(full)} puntos (recorrido "
      f"{rango_f:.2f}), ablacionado {len(nw)} puntos (recorrido "
      f"{rango_nw:.2f}) -> {OUT}")
