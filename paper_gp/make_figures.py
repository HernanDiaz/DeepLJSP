# -*- coding: utf-8 -*-
"""Figuras del paper GP -> paper_gp/figures/*.pdf (+ datos parseados en JSON).

Fig 1: convergencia de la evolución (mejor fitness por generación, 30 semillas)
Fig 2 (eliminada): la curva best-of-N pertenecia al experimento de siembra,
       que es material del tercer paper (paper_seeding/).
"""

import json
import os
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.join(HERE, "figures")
os.makedirs(FIGS, exist_ok=True)

plt.rcParams.update({"font.size": 11, "figure.facecolor": "white"})

AZUL, AMBAR, GRIS, TEAL = "#1f5fa8", "#d68910", "#5d6d7e", "#0e8a7d"

# ---------------------------------------------------------------------------
# Fig 1 — convergencia (30 evoluciones default de la campaña reevo_fixedfit)
# ---------------------------------------------------------------------------
import glob as _glob
REPO = os.path.dirname(HERE)
LOGDIR = os.path.join(REPO, "logs", "reevo")

curves = {}
pat = re.compile(r"gen\s+(\d+)\s*\|\s*mejor=([\d.]+)%")
for path in sorted(_glob.glob(os.path.join(LOGDIR, "gp_tuned_seed*.log"))):
    seed = int(re.search(r"seed(\d+)", path).group(1))
    text = open(path, encoding="utf-8", errors="replace").read()
    gens = {}
    for m in pat.finditer(text.replace("\n", " ")):
        gens[int(m.group(1))] = float(m.group(2))
    if gens:
        curves[seed] = [gens[g] for g in sorted(gens)]

if curves:
    json.dump(curves, open(os.path.join(FIGS, "convergence_data.json"), "w"),
              indent=1)
    L = min(len(v) for v in curves.values())
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    # curvas individuales muy tenues: son contexto, no el mensaje
    for i, (seed, ys) in enumerate(sorted(curves.items())):
        ax.plot(range(L), ys[:L], color="#9aa5b1", linewidth=0.45, alpha=0.22,
                zorder=1, label="individual runs" if i == 0 else None)
    mean = [sum(curves[s][g] for s in curves) / len(curves) for g in range(L)]
    # halo blanco bajo la media para que destaque sobre el haz de curvas
    ax.plot(range(L), mean, color="white", linewidth=4.0, solid_capstyle="round",
            zorder=2)
    ax.plot(range(L), mean, color=AMBAR, linewidth=2.4, solid_capstyle="round",
            zorder=3, label=f"mean of {len(curves)} runs")
    ax.set_xlabel("generation")
    ax.set_ylabel("best training RE (%)")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "fig_convergence.pdf"))
    plt.close(fig)
    print(f"fig_convergence: {len(curves)} semillas, {L} gens")
else:
    print("AVISO: no hay datos de convergencia (logs no encontrados)")
