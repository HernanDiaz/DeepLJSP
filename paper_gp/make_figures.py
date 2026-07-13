# -*- coding: utf-8 -*-
"""Figuras del paper GP -> paper_gp/figures/*.pdf (+ datos parseados en JSON).

Fig 1: convergencia de la evolución (mejor fitness por generación, 3 semillas)
Fig 2: escalera de métodos constructivos (RE global, 70 instancias)
Fig 3: curva best-of-N (GP-eps vs política RL del companion)
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
# Fig 1 — convergencia (parsea los logs de las 3 evoluciones default)
# ---------------------------------------------------------------------------
TASKS = ("C:/Users/herdi/AppData/Local/Temp/claude/E--PycharmProjects-DeepLJSP/"
         "ea0e876f-5656-4d1f-ba9c-624faf5d79d5/tasks")
LOGS = {1: "bvikfgwj2.output", 2: "b5iwcgzqu.output", 3: "b2i1pta8a.output"}

curves = {}
pat = re.compile(r"gen\s+(\d+)\s*\|\s*mejor=([\d.]+)%")
for seed, fname in LOGS.items():
    path = os.path.join(TASKS, fname)
    if not os.path.exists(path):
        continue
    text = open(path, encoding="utf-8", errors="replace").read()
    # los logs vienen con saltos de línea intercalados: quitar antes de parsear
    gens = {}
    for m in pat.finditer(text.replace("\n", " ")):
        gens[int(m.group(1))] = float(m.group(2))
    if gens:
        curves[seed] = [gens[g] for g in sorted(gens)]

if curves:
    json.dump(curves, open(os.path.join(FIGS, "convergence_data.json"), "w"),
              indent=1)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    for (seed, ys), c in zip(sorted(curves.items()), [AZUL, AMBAR, TEAL]):
        ax.plot(range(len(ys)), ys, color=c, linewidth=1.8,
                label=f"seed {seed}")
    ax.set_xlabel("generation")
    ax.set_ylabel("best training RE (%)")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "fig_convergence.pdf"))
    plt.close(fig)
    print(f"fig_convergence: semillas {sorted(curves)} "
          f"({[len(v) for _, v in sorted(curves.items())]} gens)")
else:
    print("AVISO: no hay datos de convergencia (logs no encontrados)")

# ---------------------------------------------------------------------------
# Fig 2 — escalera de constructivos
# ---------------------------------------------------------------------------
metodos = [
    ("MOR (best fixed rule)", 45.4, GRIS),
    ("G&T + MWKR", 29.4, GRIS),
    ("GP rule (default config)", 18.5, AMBAR),
    ("GP rule (tuned config)", 17.7, AMBAR),
    ("DRL policy, best-of-1024", 12.7, AZUL),
    ("Tabu search (30 runs, minutes)", 3.9, TEAL),
]
fig, ax = plt.subplots(figsize=(6.4, 3.4))
ys = range(len(metodos))[::-1]
for y, (nombre, v, c) in zip(ys, metodos):
    ax.barh(y, v, height=0.6, color=c)
    ax.text(v + 0.6, y, f"{v:.1f}%", va="center", fontsize=10,
            fontweight="bold")
ax.set_yticks(list(ys))
ax.set_yticklabels([m[0] for m in metodos], fontsize=10)
ax.set_xlabel("mean RE (%) over the 70 instances — lower is better")
ax.set_xlim(0, 52)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(FIGS, "fig_ladder.pdf"))
plt.close(fig)
print("fig_ladder ok")

# ---------------------------------------------------------------------------
# Fig 3 — best-of-N
# ---------------------------------------------------------------------------
n_gp = [1, 16, 64, 256, 1024]
re_gp = [18.5, 17.1, 15.9, 14.9, 14.1]
fig, ax = plt.subplots(figsize=(6.4, 3.8))
ax.plot(n_gp, re_gp, "-o", color=AMBAR, linewidth=2,
        label="GP-$\\varepsilon$ (uniform noise)")
ax.plot([1, 1024], [19.4, 12.7], "--s", color=AZUL, linewidth=2,
        label="DRL policy (learned distribution)")
ax.set_xscale("log", base=2)
ax.set_xticks(n_gp)
ax.set_xticklabels([str(n) for n in n_gp])
ax.set_xlabel("N sampled solutions per instance (best-of-N)")
ax.set_ylabel("mean RE (%) — 70 instances")
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(os.path.join(FIGS, "fig_bestofN.pdf"))
plt.close(fig)
print("fig_bestofN ok")
