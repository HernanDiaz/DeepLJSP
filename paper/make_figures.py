"""
Genera las figuras del paper desde los datos de benchmarks/ y seeds/.

Los agregados de RE provienen de los benchmarks versionados (ver comentarios
por figura con el JSON de origen); las distribuciones de pools se leen
directamente de seeds/. Salida: paper/figures/*.pdf
"""

import os
import sys

sys.path.insert(0, ".")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(FIG_DIR, exist_ok=True)

plt.rcParams.update({"font.size": 11, "figure.dpi": 150})


# ----------------------------------------------------------------------
# Fig 1: curva de escalado (episodios vs RE medio en TA15-20)
# Origen: v2-full__d15a325, v2-full-300ep__e323b1a, v2-full-1000ep__012ecd2,
#         v2-attn-300ep__dfb324e, v2-attn-1000ep__9c35115 (re_report.py)
# ----------------------------------------------------------------------
def fig_scaling():
    episodes = [100, 300, 1000]
    ds_mean = [28.0, 16.4, 13.4]
    ds_best = [25.0, 15.5, 12.3]
    attn_mean = [17.5, 15.0]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(episodes, ds_mean, "o-", color="seagreen", label="Deep Sets (mean of 3 seeds)")
    ax.plot(episodes, ds_best, "o--", color="seagreen", alpha=0.6, label="Deep Sets (best seed)")
    ax.plot([300, 1000], attn_mean, "s-", color="steelblue", label="+ attention (mean)")

    ax.axhline(46.4, color="gray", linestyle=":", linewidth=1.2)
    ax.text(1000, 46.4, " MOR", va="center", fontsize=9, color="gray")
    ax.axhline(9.6, color="indianred", linestyle=":", linewidth=1.2)
    ax.text(1000, 9.6, " fEABC", va="center", fontsize=9, color="indianred")
    ax.axhline(3.9, color="darkred", linestyle=":", linewidth=1.2)
    ax.text(1000, 3.9, " TS-N$_2$", va="center", fontsize=9, color="darkred")

    ax.set_xscale("log")
    ax.set_xticks(episodes)
    ax.set_xticklabels(episodes)
    ax.set_xlabel("Training episodes per instance")
    ax.set_ylabel("Mean RE (%) on TA15–TA20")
    ax.legend(frameon=False)
    ax.grid(alpha=0.3, linestyle="--")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_scaling.pdf"))
    plt.close(fig)


# ----------------------------------------------------------------------
# Fig 2: generalización cross-size zero-shot (checkpoint 20x15, best-of-64)
# Origen: eval_v2_crosssize con checkpoint 1000ep (50x15 con checkpoint 300ep)
# ----------------------------------------------------------------------
def fig_crosssize():
    labels = ["TA1\n15×15", "TA2\n15×15", "TA5\n15×15", "TA21\n20×20", "TA25\n20×20",
              "TA31\n30×15", "TA41\n30×20", "TA51\n50×15", "TA61\n50×20"]
    v2 = [14.4, 7.0, 8.7, 9.6, 15.9, 13.9, 24.5, 25.0, 15.1]
    mor = [29.7, 34.8, 50.7, 40.8, 53.2, 34.4, 53.5, 38.2, 48.7]

    x = range(len(labels))
    width = 0.38
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar([i - width / 2 for i in x], v2, width, color="seagreen", label="v2 (zero-shot)")
    ax.bar([i + width / 2 for i in x], mor, width, color="steelblue", label="MOR")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("RE (%)")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_crosssize.pdf"))
    plt.close(fig)


# ----------------------------------------------------------------------
# Fig 3: distribución de calidad de los pools de siembra (piloto)
# Origen: seeds/*.csv (E[Cmax] de cada solución)
# ----------------------------------------------------------------------
def fig_pools():
    instances = [("int__tai15_15_05", "TA5", 1224),
                 ("int__tai20_20_02", "TA22", 1561),
                 ("int__tai30_20_04", "TA44", 1948)]
    gens = [("v2", "v2 policy", "seagreen"),
            ("graspmor", "MOR+$\\epsilon$", "steelblue"),
            ("graspmix", "mixed rules+$\\epsilon$", "sandybrown")]

    fig, axes = plt.subplots(1, 3, figsize=(10, 3.6), sharey=False)
    for ax, (pid, ta, lb) in zip(axes, instances):
        data, labels, colors = [], [], []
        for gen, glabel, color in gens:
            path = f"seeds/{pid}_{gen}_pool.csv"
            if not os.path.exists(path):
                continue
            res = []
            for line in open(path, encoding="utf-8"):
                lo, up = (float(x) for x in line.strip().split(";")[1].strip("[] ").split(","))
                res.append(((lo + up) / 2.0 - lb) / lb * 100)
            data.append(res)
            labels.append(glabel)
            colors.append(color)
        parts = ax.violinplot(data, showmedians=True)
        for body, color in zip(parts["bodies"], colors):
            body.set_facecolor(color)
            body.set_alpha(0.6)
        ax.set_xticks(range(1, len(labels) + 1))
        ax.set_xticklabels(labels, fontsize=8)
        ax.set_title(f"{ta}", fontsize=10)
        ax.grid(axis="y", alpha=0.3, linestyle="--")
    axes[0].set_ylabel("RE (%) of pool solutions")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_pools.pdf"))
    plt.close(fig)


# ----------------------------------------------------------------------
# Fig 4: ablaciones (in-size, TA15-20, 1000 eps)
# Origen: idea-16-full (v1), v2-full-1000ep, v2-attn-1000ep,
#         v2-multisize-12k (evaluación común 5 instancias, aquí solo nota)
# ----------------------------------------------------------------------
def fig_ablation():
    labels = ["MOR", "v1 (tuned,\nbest-of-64)", "v2 Deep Sets\n(1000 eps)",
              "v2 + attention\n(1000 eps)"]
    values = [46.4, 38.6, 13.4, 15.0]
    colors = ["steelblue", "gray", "seagreen", "mediumseagreen"]

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(labels, values, color=colors, edgecolor="black", linewidth=0.6)
    for bar, v in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, v, f"{v:.1f}",
                ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.axhline(9.6, color="indianred", linestyle=":", linewidth=1.2)
    ax.text(3.4, 9.6, " fEABC", va="bottom", fontsize=9, color="indianred")
    ax.axhline(3.9, color="darkred", linestyle=":", linewidth=1.2)
    ax.text(3.4, 3.9, " TS-N$_2$", va="bottom", fontsize=9, color="darkred")
    ax.set_ylabel("Mean RE (%) on TA15–TA20")
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_ablation.pdf"))
    plt.close(fig)


if __name__ == "__main__":
    fig_scaling()
    fig_crosssize()
    fig_pools()
    fig_ablation()
    print("Figuras generadas en", FIG_DIR)
