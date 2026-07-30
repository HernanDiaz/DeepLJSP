# -*- coding: utf-8 -*-
"""Frontera calidad-predictibilidad, reglas y medias -> fig_lambda.pdf.

Fusion de las antiguas fig_lambda (curvas de medias frente a lambda) y
fig_arms (las reglas individuales en el espacio RE-anchura): eran el mismo
espacio con los ejes traspuestos, y tras anadir la segunda curva el solape
era casi total. Una sola figura lleva ahora los dos mensajes:

  * capa de puntos (tenue): cada regla evolucionada, evaluada en las 70
    instancias. Color por conjunto de terminales (ambar = completo, gris =
    sin anchuras); relleno por objetivo (hueco = makespan, relleno = robusto,
    cualquier lambda). Sostiene las afirmaciones a nivel de regla: ninguna
    ablacionada baja de 12.05% de anchura y solo el brazo robusto completo
    llega a 9.24%.
  * capa de curvas (solida): la media de cada brazo en cada lambda del
    barrido. Sostiene la frontera y su ausencia en el brazo ablacionado.

La dispersion la ensena la propia nube, asi que las barras de error
desaparecen: eran redundantes y en lambda=4 competian visualmente con todo.

make_arms_fig.py y fig_arms.pdf se conservan en el repositorio pero el paper
ya no los incluye. No recalcula nada: solo lee CSVs.
"""

import csv
import os
import sys
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CSV_FULL = os.path.join(REPO, "benchmarks/lambda_sweep/lambda_sweep_tuned.csv")
CSV_LPR = os.path.join(REPO, "benchmarks/lambda_por_regla.csv")
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


# --- puntos: cada regla, clasificada por (terminales, objetivo) -----------
# (ancho, re) por categoria; 'mk' = objetivo makespan, 'rob' = robusto
pts = defaultdict(list)
for r in csv.DictReader(open(CSV_2X2, encoding="utf-8")):
    term = "full" if r["terminales"] == "full" else "nw"
    obj = "mk" if r["objetivo"] == "makespan" else "rob"
    pts[(term, obj)].append((float(r["ancho"]), float(r["re"])))
for r in csv.DictReader(open(CSV_LPR, encoding="utf-8")):
    pts[("full", "rob")].append((float(r["ancho"]), float(r["re"])))
for r in csv.DictReader(open(CSV_NW, encoding="utf-8")):
    pts[("nw", "rob")].append((float(r["ancho"]), float(r["re"])))

# --- curvas: medias por brazo y lambda ------------------------------------
full = sorted((float(r["lambda"]), float(r["re_mean"]), float(r["width_mean"]))
              for r in csv.DictReader(open(CSV_FULL, encoding="utf-8")))

acc = defaultdict(lambda: ([], []))
for r in csv.DictReader(open(CSV_NW, encoding="utf-8")):
    acc[float(r["lam"])][0].append(float(r["re"]))
    acc[float(r["lam"])][1].append(float(r["ancho"]))
for r in csv.DictReader(open(CSV_2X2, encoding="utf-8")):
    if r["objetivo"] == "robust" and r["terminales"] == "nowidth":
        acc[1.0][0].append(float(r["re"]))
        acc[1.0][1].append(float(r["ancho"]))
nw = [(lam, stats(acc[lam][0])[0], stats(acc[lam][1])[0])
      for lam in sorted(acc)]

fig, ax = plt.subplots(figsize=(3.99, 2.62))

# capa 1: la nube de reglas, tenue y detras
ESTILO = {("full", "mk"): dict(marker="o", mfc="none", mec=AMBAR),
          ("full", "rob"): dict(marker="o", mfc=AMBAR, mec=AMBAR),
          ("nw", "mk"): dict(marker="s", mfc="none", mec=GRIS),
          ("nw", "rob"): dict(marker="s", mfc=GRIS, mec=GRIS)}
for k, ps in pts.items():
    ax.plot([w for w, _ in ps], [re for _, re in ps], ls="none",
            ms=2.6, mew=0.7, alpha=0.4, zorder=2, **ESTILO[k])

# capa 2: las medias por lambda, solidas y delante
ax.plot([w for _, _, w in full], [re for _, re, _ in full], "-o",
        color=AMBAR, linewidth=1.8, markersize=4.5, zorder=4)
ax.plot([w for _, _, w in nw], [re for _, re, _ in nw], "-s",
        color=GRIS, linewidth=1.6, markersize=4, zorder=4)

# etiquetas de lambda solo sobre la curva ambar: los cinco puntos de la gris
# caen en 0.13 puntos de ancho y etiquetarlos seria rotular cinco veces el
# mismo sitio; que la gris no se mueve lo dice el pie
OFF = {0.5: (-33, -8), 1.0: (9, -1), 2.0: (5, 7), 4.0: (8, 2)}
for lam, re_m, w_m in full:
    ax.annotate(f"$\\lambda$={lam:g}", (w_m, re_m), textcoords="offset points",
                xytext=OFF.get(lam, (8, 4)), fontsize=7.5, zorder=5)

ax.set_xlabel("relative width of the makespan interval (%)")
ax.set_ylabel("mean RE (%)")
leyenda = [
    Line2D([], [], color=AMBAR, marker="o", ms=4.5, lw=1.8,
           label="with width terminals (mean per $\\lambda$)"),
    Line2D([], [], color=GRIS, marker="s", ms=4, lw=1.6,
           label="without width terminals (mean per $\\lambda$)"),
    Line2D([], [], ls="none", marker="o", mfc="none", mec="black", ms=3,
           label="single rule, makespan objective"),
    Line2D([], [], ls="none", marker="o", mfc="black", mec="black", ms=3,
           label="single rule, robust objective"),
]
ax.legend(handles=leyenda, fontsize=6.8, frameon=False, loc="upper left",
          handlelength=1.6, labelspacing=0.35)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(OUT)
plt.close(fig)
n_pts = sum(len(v) for v in pts.values())
print(f"fig_lambda ok: {n_pts} reglas + curvas de {len(full)} y {len(nw)} "
      f"medias -> {OUT}")
