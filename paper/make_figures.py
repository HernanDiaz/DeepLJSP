"""
Genera las figuras del paper desde los datos de benchmarks/ y seeds/.

Los agregados de RE provienen de los benchmarks versionados (ver comentarios
por figura con el JSON de origen); las distribuciones de pools se leen
directamente de seeds/. Salida: paper/figures/*.pdf
"""

import os
import re
import sys

sys.path.insert(0, ".")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TA_BASE = {"15_15": 0, "20_15": 10, "20_20": 20, "30_15": 30,
           "30_20": 40, "50_15": 50, "50_20": 60}

FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# fonttype 42 (TrueType): por defecto matplotlib incrusta el texto de los
# PDF como Type 3 (mapa de bits), que produccion de Springer rechaza
plt.rcParams.update({"font.size": 10, "figure.dpi": 150,
                     "pdf.fonttype": 42, "ps.fonttype": 42})


# ----------------------------------------------------------------------
# Fig 1: curva de escalado (episodios vs RE medio en TA15-20)
# Origen: v2-full__d15a325, v2-full-300ep__e323b1a, v2-full-1000ep__012ecd2,
#         v2-attn-300ep__dfb324e, v2-attn-1000ep__9c35115 (re_report.py)
# ----------------------------------------------------------------------
def fig_scaling():
    episodes = [100, 300, 1000]
    # diez semillas por punto; la banda es el rango entre la mejor y la
    # peor tirada, que es lo que colapsa con el presupuesto
    # cifras del evaluador independiente (validacion_unificada.json), las
    # mismas diez semillas en los tres presupuestos
    ds_mean = [30.6, 17.3, 13.6]
    ds_best = [21.1, 14.5, 12.8]
    ds_worst = [39.2, 19.9, 14.0]
    # la variante de atencion NO se dibuja aqui: tiene tres semillas y
    # esta curva ya tiene diez, asi que ponerlas juntas invitaria a una
    # comparacion no pareada. Su contraste vive en tab:insize-attn.

    fig, ax = plt.subplots(figsize=(4.57, 3.05))
    ax.fill_between(episodes, ds_best, ds_worst, color="seagreen",
                    alpha=0.15, linewidth=0,
                    label="best-to-worst seed range")
    ax.plot(episodes, ds_mean, "o-", color="seagreen", label="Deep Sets (mean of 10 seeds)")
    ax.plot(episodes, ds_best, "o--", color="seagreen", alpha=0.6, label="Deep Sets (best seed)")

    # G&T-MWKR y no MOR: el limite superior debe ser la MEJOR referencia
    # constructiva, no la mas comoda. 27.9 es su media en TA15-TA20;
    # sobre las 70 da 29.5. La inferior sigue siendo fEABC porque GA solo
    # esta publicado sobre las 12 clasicas, no sobre Taillard.
    ax.axhline(27.9, color="gray", linestyle=":", linewidth=1.2)
    # sin escapar el &: matplotlib no pasa por LaTeX y lo imprimiria literal
    ax.text(1000, 28.4, "G&T-MWKR", va="bottom", ha="right", fontsize=9,
            color="gray")
    ax.axhline(9.6, color="indianred", linestyle=":", linewidth=1.2)
    ax.text(1000, 10.1, "fEABC", va="bottom", ha="right", fontsize=9,
            color="indianred")

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
    v2 = [13.1, 9.7, 10.5, 13.2, 15.0, 15.8, 25.9, 15.3, 16.8]
    mor = [29.7, 34.8, 50.7, 40.8, 53.2, 34.4, 53.5, 38.2, 48.7]

    x = range(len(labels))
    width = 0.38
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar([i - width / 2 for i in x], v2, width, color="seagreen", label="Policy (zero-shot, mean of 3 seeds)")
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




# ----------------------------------------------------------------------
# Fig: enfrentamiento por instancia contra el mejor baseline constructivo
# Origen: constructive_per_instance.csv (G&T-MWKR), fair_v2_greedy.csv y
#         eval_fair_bo1024.csv. Cada punto es una de las 70 instancias;
#         por debajo de la diagonal gana la politica.
# ----------------------------------------------------------------------
def fig_headtohead():
    """Politica frente al GP a presupuestos emparejados.

    Panel izquierdo: una pasada contra una pasada (regla destacada del
    companion frente a la politica greedy). Panel derecho: 1024 muestras
    contra 1024 (regla aleatorizada del companion frente a best-of-1024).
    Comparar una pasada con 1024 muestras estaria sesgado.
    """
    import csv
    from collections import defaultdict

    def _ta(nombre):
        m = re.search(r"tai(\d+_\d+)_(\d+)", nombre.lower())
        return "TA%d" % (TA_BASE[m.group(1)] + int(m.group(2)))

    gp1 = {_ta(r["instance"]): float(r["re"]) for r in
           csv.DictReader(open("benchmarks/reevo_fixedfit/summary.csv",
                               encoding="utf-8"))
           if r["method"] == "gp_tuned_seed1"}
    gp1024 = {_ta(r["instance"]): float(r["best_at_1024"]) for r in
              csv.DictReader(open("benchmarks/gp_destacada/gp_destacada_presupuestos.csv",
                                  encoding="utf-8"))}
    gre = defaultdict(list)
    for r in csv.DictReader(open("benchmarks/fair_v2_greedy.csv",
                                 encoding="utf-8")):
        gre[_ta(r["instance"])].append(float(r["re_mid"]))
    gre = {k: sum(v) / len(v) for k, v in gre.items()}
    bo = defaultdict(list)
    for r in csv.DictReader(open("benchmarks/eval_fair_bo1024.csv",
                                 encoding="utf-8")):
        bo[_ta(r["instance"])].append(float(r["re_comp"]))
    bo = {k: min(v) for k, v in bo.items()}

    paneles = [
        ("One constructive pass", gp1, gre, "steelblue", "o"),
        ("Best of 1024 samples", gp1024, bo, "seagreen", "^"),
    ]
    tas = sorted(gp1, key=lambda s: int(s[2:]))
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.3))
    for ax, (titulo, x, y, color, marca) in zip(axes, paneles):
        lim = [0, max(max(x.values()), max(y.values())) * 1.08]
        ax.plot(lim, lim, color="gray", linewidth=1, linestyle="--", zorder=1)
        ax.fill_between(lim, 0, lim, color=color, alpha=0.07, zorder=0)
        ax.scatter([x[k] for k in tas], [y[k] for k in tas], s=24,
                   color=color, marker=marca, alpha=0.85, zorder=3)
        gana = sum(y[k] < x[k] for k in tas)
        ax.set_xlim(lim); ax.set_ylim(lim); ax.set_aspect("equal")
        ax.set_title(titulo, fontsize=10)
        ax.set_xlabel("GP rule: RE (%)")
        ax.text(0.96, 0.07, "policy wins %d/70" % gana,
                transform=ax.transAxes, ha="right", fontsize=11,
                color=color)
        ax.grid(alpha=0.3, linestyle="--")
    axes[0].set_ylabel("DRL policy: RE (%)")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_headtohead.pdf"))
    plt.close(fig)


# ----------------------------------------------------------------------
# Fig: importancia por permutacion de las 16 features de operacion
# Origen: feature_importance.csv
# ----------------------------------------------------------------------
def fig_importance():
    import csv

    ETIQUETAS = {
        "holgura": "slack", "pos_restante": "job position (remaining)",
        "rem_up": "remaining work (upper)", "dur_up": "duration (upper)",
        "pos_hecha": "job position (done)",
        "rem_lo": "remaining work (lower)",
        "hueco_potencial": "potential idle gap",
        "dur_lo": "duration (lower)", "est_lo": "earliest start (lower)",
        "est_width_rel": "earliest start width", "est_up": "earliest start (upper)",
        "carga_maquina": "machine load", "congestion": "machine congestion",
        "makespan_maquina": "machine makespan", "dur_width_rel": "duration width",
        "makespan_job": "job makespan",
    }
    # cinco permutaciones por feature: media y desviacion tipica. El
    # fichero de una sola extraccion se conserva pero ya no se dibuja
    import statistics as _st
    por_feat = {}
    for r in csv.DictReader(open("benchmarks/feature_importance_rep.csv",
                                 encoding="utf-8")):
        por_feat.setdefault(r["feature"], []).append(
            float(r["delta_puntos"]))
    filas = [{"feature": f, "media": _st.mean(v), "sd": _st.stdev(v)}
             for f, v in por_feat.items()]
    filas.sort(key=lambda r: r["media"])
    nombres = [ETIQUETAS.get(r["feature"], r["feature"]) for r in filas]
    valores = [r["media"] for r in filas]
    errores = [r["sd"] for r in filas]
    # las dos features de anchura, resaltadas: son las que no aportan
    colores = ["indianred" if r["feature"].endswith("width_rel")
               else "steelblue" for r in filas]

    fig, ax = plt.subplots(figsize=(6.53, 3.9))
    y = range(len(nombres))
    ax.barh(list(y), valores, color=colores, height=0.7,
            xerr=errores, error_kw={"ecolor": "0.3", "elinewidth": 0.9,
                                    "capsize": 2})
    ax.set_yticks(list(y))
    ax.set_yticklabels(nombres, fontsize=8.5)
    # las barras de anchura son demasiado cortas para que el color se vea:
    # el resaltado va en la etiqueta
    for etiqueta, fila in zip(ax.get_yticklabels(), filas):
        if fila["feature"].endswith("width_rel"):
            etiqueta.set_color("indianred")
            etiqueta.set_fontweight("bold")
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("$\\Delta$ mean RE when the feature is permuted (points)")
    for i, (v, e) in enumerate(zip(valores, errores)):
        ax.text(v + e + 1.0, i, "%+.1f" % v, va="center",
                ha="left", fontsize=8)
    ax.set_xlim(min(valores) - 6, max(valores) + 9)
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_importance.pdf"),
                bbox_inches="tight")
    plt.close(fig)


# ----------------------------------------------------------------------
# Fig: robustez ejecucional eps-barra por metodo (x1000)
# Origen: eval_eps_policy.csv (K=1000, numeros aleatorios comunes)
# ----------------------------------------------------------------------
def fig_eps():
    import csv
    from collections import defaultdict

    # eval_eps_all70.csv: el benchmark completo, los 17 metodos de 7.5
    # con las mismas realizaciones sembradas por instancia
    por = defaultdict(dict)
    for r in csv.DictReader(open("benchmarks/eval_eps_all70.csv",
                                 encoding="utf-8")):
        m = r["method"]
        if m.startswith("lam1-") and m.endswith("-bo64"):
            g = "Policy $f_\\lambda$\n(best-of-64)"
        elif m.startswith("lam1-"):
            continue                      # el greedy robusto no aporta
        elif m.startswith("policy-bo64"):
            g = "Policy\n(best-of-64)"
        elif m.startswith("policy-greedy"):
            g = "Policy\n(greedy)"
        elif m == "GP-bo64":
            g = "GP\n(best-of-64)"
        elif m == "GP":
            g = "GP\n(one pass)"
        else:
            g = m
        por[g].setdefault(r["instance"], []).append(float(r["eps"]) * 1000)
    med = {g: {i: sum(v) / len(v) for i, v in d.items()}
           for g, d in por.items()}

    orden = ["MOR", "GT-MWKR", "EST", "GP\n(one pass)",
             "GP\n(best-of-64)", "Policy\n(greedy)",
             "Policy\n(best-of-64)", "Policy $f_\\lambda$\n(best-of-64)"]
    # los rotulos del eje son mas cortos que las claves de los datos:
    # ocho categorias en 6.53 pulgadas dejan ~50pt por hueco y
    # "(best-of-64)" a 8.5pt mide mas que eso, asi que se solapaban
    rotulos = ["MOR", "GT-MWKR", "EST", "GP\n(1)", "GP\n(64)",
               "Policy\n(greedy)", "Policy\n(64)",
               "Policy $f_\\lambda$\n(64)"]
    fig, ax = plt.subplots(figsize=(6.53, 2.78))
    datos = [list(med[g].values()) for g in orden]
    bp = ax.boxplot(datos, positions=list(range(len(orden))), widths=0.52,
                    whis=1.5, showfliers=False, patch_artist=True,
                    medianprops={"color": "black", "linewidth": 1.2})
    for parche, g in zip(bp["boxes"], orden):
        parche.set_facecolor("#D8EFD8" if "Policy" in g else "#D5E5F0")
        parche.set_edgecolor("0.35")
    # la media va rotulada ENCIMA de su bigote y centrada en la
    # categoria: a la derecha del diamante invadia la caja siguiente,
    # que empieza a 0.74 del centro
    topes = [bp["caps"][2 * k + 1].get_ydata()[0]
             for k in range(len(orden))]
    for k, (g, vals) in enumerate(zip(orden, datos)):
        m = sum(vals) / len(vals)
        color = "seagreen" if "Policy" in g else "steelblue"
        ax.scatter([k], [m], marker="D", s=26, color=color, zorder=4)
        ax.text(k, topes[k] + 0.12, "%.2f" % m, va="bottom", ha="center",
                fontsize=8.5, color=color)
    ax.set_ylim(top=max(topes) + 0.75)
    ax.set_xticks(range(len(orden)))
    ax.set_xticklabels(rotulos, fontsize=8.5)
    ax.set_ylabel("$\\bar\\varepsilon \\times 10^{3}$")
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    ax.set_xlim(-0.55, len(orden) - 0.25)
    fig.savefig(os.path.join(FIG_DIR, "fig_eps.pdf"), bbox_inches="tight")
    plt.close(fig)


# ----------------------------------------------------------------------
# Fig: distribucion del RE por clase de tamano sobre las 70 instancias
# Origen: constructive_per_instance.csv, fair_v2_greedy.csv,
#         eval_fair_bo1024.csv
# ----------------------------------------------------------------------
def fig_byclass():
    import csv
    from collections import defaultdict
    import numpy as np

    CL = ["15_15", "20_15", "20_20", "30_15", "30_20", "50_15", "50_20"]

    def _n(nombre):
        m = re.search(r"tai(\d+_\d+)_(\d+)", nombre.lower())
        return TA_BASE[m.group(1)] + int(m.group(2))

    def _n2(nombre):
        m = re.search(r"tai(\d+_\d+)_(\d+)", nombre.lower())
        return TA_BASE[m.group(1)] + int(m.group(2))

    gp = {_n2(r["instance"]): float(r["re"]) for r in
          csv.DictReader(open("benchmarks/reevo_fixedfit/summary.csv",
                              encoding="utf-8"))
          if r["method"] == "gp_tuned_seed1"}
    gp1024 = {_n2(r["instance"]): float(r["best_at_1024"]) for r in
              csv.DictReader(open("benchmarks/gp_destacada/gp_destacada_presupuestos.csv",
                                  encoding="utf-8"))}
    gre = defaultdict(list)
    for r in csv.DictReader(open("benchmarks/fair_v2_greedy.csv",
                                 encoding="utf-8")):
        gre[_n(r["instance"])].append(float(r["re_mid"]))
    gre = {k: sum(v) / len(v) for k, v in gre.items()}
    bo = defaultdict(list)
    for r in csv.DictReader(open("benchmarks/eval_fair_bo1024.csv",
                                 encoding="utf-8")):
        bo[_n(r["instance"])].append(float(r["re_comp"]))
    bo = {k: min(v) for k, v in bo.items()}

    # emparejadas por presupuesto: los dos aprendices a una pasada y a
    # 1024 muestras (G&T-MWKR salio de la figura: su sitio es la tabla)
    # los rotulos son los de tab:seventy: GP rule y Policy, un pase o
    # 1024 muestras. Decir "greedy" aqui y "1 pass" en la tabla
    # obligaba al lector a traducir entre figura y tabla
    series = [("GP rule, 1 pass", gp, "#b39ddb"),
              ("Policy, 1 pass", gre, "sandybrown"),
              ("GP rule, 1024 samples", gp1024, "mediumpurple"),
              ("Policy, 1024 samples", bo, "seagreen")]
    # Caja con los puntos superpuestos: los cuartiles y bigotes resumen,
    # y con n=10 por clase ningun punto queda escondido.
    fig, ax = plt.subplots(figsize=(6.53, 3.02))
    ancho = 0.21
    rng = np.random.default_rng(11)
    for k, (nombre, datos, color) in enumerate(series):
        for i in range(len(CL)):
            vals = [datos[j] for j in range(i * 10 + 1, i * 10 + 11)]
            x = i + (k - 1.5) * ancho
            bp = ax.boxplot([vals], positions=[x], widths=ancho * 0.82,
                            patch_artist=True, showfliers=False,
                            medianprops=dict(color="black", linewidth=1.6),
                            boxprops=dict(facecolor=color, alpha=0.55,
                                          edgecolor=color, linewidth=1.4),
                            whiskerprops=dict(color=color, linewidth=1.3),
                            capprops=dict(color=color, linewidth=1.3))
            ax.scatter(rng.normal(x, 0.022, len(vals)), vals, s=8,
                       color=color, alpha=0.75, linewidth=0, zorder=3)
        ax.plot([], [], color=color, linewidth=6, alpha=0.75, label=nombre)
    ax.set_xlim(-0.6, len(CL) - 0.4)
    ax.set_xticks(range(len(CL)))
    ax.set_xticklabels([c.replace("_", r"$\times$") for c in CL])
    # la clase de entrenamiento y validacion, marcada
    ax.axvspan(0.5, 1.5, color="gray", alpha=0.10, zorder=0)
    ax.text(1, ax.get_ylim()[1] * 0.97, "train + validation", ha="center",
            va="top", fontsize=8, color="dimgray")
    ax.set_xlabel("Instance size class")
    ax.set_ylabel("RE (%)")
    # la leyenda no debe ser mas ancha que los ejes: si sobresale, el
    # recorte la incluye y los ejes encogen al escalar a \linewidth
    ax.legend(frameon=False, fontsize=9, ncol=4, loc="lower center",
              bbox_to_anchor=(0.5, 1.01), columnspacing=1.1,
              handlelength=1.3, handletextpad=0.5)
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    fig.tight_layout()
    # recortar al contenido: sin esto el PDF conserva margenes blancos
    # y, colocado a \linewidth, los ejes quedan mas estrechos que la caja
    fig.savefig(os.path.join(FIG_DIR, "fig_byclass.pdf"),
                bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


# ----------------------------------------------------------------------
# Fig: escalera de clases computacionales en las 12 clasicas
# Origen: classic12_est.csv, classic12_tuned.csv,
#         eval_classic12_policy.csv
# ----------------------------------------------------------------------
def fig_ladder():
    import csv
    from collections import defaultdict

    clas = {r["inst"]: r for r in csv.DictReader(
        open("benchmarks/classic12_tuned.csv", encoding="utf-8"))}
    est = {r["inst"]: float(r["est_re"]) for r in csv.DictReader(
        open("benchmarks/classic12_est.csv", encoding="utf-8"))}
    # las TREINTA semillas de la campana de 2026-08-15, a los tres
    # presupuestos, para que la escalera enfrente 30 contra 30 en cada
    # peldano y no tres contra treinta
    import glob as _g
    campana = defaultdict(lambda: defaultdict(list))
    for f in _g.glob("benchmarks/ext30/classic12_bo*_*.csv"):
        if "maestro" in f:
            continue
        for r in csv.DictReader(open(f, encoding="utf-8")):
            campana[int(r["n_samples"])][r["name"]].append(
                (int(r["seed"]), float(r["re"])))

    def por_presupuesto(n):
        """{instancia: [RE por semilla]} deduplicado por semilla."""
        return {i: [v for _, v in dict(vs).items()]
                for i, vs in campana[n].items()}

    pol = por_presupuesto(64)

    def media(d):
        return sum(d) / len(d)

    # la politica greedy, para que la clase de una pasada tenga las dos
    # familias al mismo presupuesto (antes se comparaba su best-of-64
    # contra la regla a una pasada, y ambas iban en la misma clase)
    gre = por_presupuesto(1)
    # A 1024 la figura usa el fichero POR SEMILLA: cada checkpoint con sus
    # propias 1024 muestras, promediado sobre los tres. El otro fichero
    # reparte 342 entre los tres y agrega, que empareja el presupuesto en
    # muestras pero no en modelos -- una tirada de GP es UNA regla.
    bo1024 = por_presupuesto(1024)

    def media(d):
        return sum(d) / len(d)

    # las 30 reglas del brazo, para poder enfrentar media contra media en
    # vez de una regla seleccionada contra la media de tres semillas
    import glob
    arm = {}
    for f in glob.glob("benchmarks/classic12_arm_bon/*.csv"):
        arm[os.path.basename(f)] = {
            r["inst"]: (float(r["gp"]), float(r["gp64"]), float(r["gp1024"]))
            for r in csv.DictReader(open(f, encoding="utf-8"))}

    def gp_media(k):
        return media([media([arm[r][i][k] for r in arm]) for i in clas])

    filas = [
        ("MOR", media([float(c["mor"]) for c in clas.values()]), "constructive"),
        ("EST", media(list(est.values())), "constructive"),
        ("G&T-MWKR", media([float(c["gt"]) for c in clas.values()]),
         "constructive"),
        ("GP rules (mean of 30)", gp_media(0), "learned1"),
        ("Policy, 1 pass", media([media(v) for v in gre.values()]),
         "learned1"),
        ("GP rules, $\\epsilon$-greedy@64", gp_media(1), "learned64"),
        ("Policy, best-of-64", media([media(v) for v in pol.values()]),
         "learned64"),
        ("GP rules, $\\epsilon$-greedy@1024", gp_media(2), "learned1024"),
        ("Policy, best-of-1024",
         media([media(v) for v in bo1024.values()]), "learned1024"),
        ("GA", media([float(c["GA"]) for c in clas.values()]), "search"),
        ("ABC$_{E3}$", media([float(c["ABCE3"]) for c in clas.values()]),
         "search"),
        ("fEABC", media([float(c["fEABC"]) for c in clas.values()]), "search"),
        ("ESABC", media([float(c["ESABC"]) for c in clas.values()]), "search"),
    ]
    filas.sort(key=lambda r: -r[1])
    COLOR = {"constructive": "steelblue", "learned1": "seagreen",
             "learned64": "mediumaquamarine", "learned1024": "#bfe6d4",
             "search": "indianred"}
    ETIQ = {"constructive": "hand-crafted, one pass",
            "learned1": "learned, one pass",
            "learned64": "learned, 64 samples",
            "learned1024": "learned, 1024 samples",
            "search": "per-instance search, 30 runs"}

    fig, ax = plt.subplots(figsize=(5.09, 3.58))
    vistos = set()
    for k, (nombre, valor, clase) in enumerate(filas):
        etiqueta = ETIQ[clase] if clase not in vistos else None
        vistos.add(clase)
        ax.barh(k, valor, color=COLOR[clase], alpha=0.8, height=0.66,
                label=etiqueta)
        ax.text(valor + 0.7, k, "%.1f" % valor, va="center", fontsize=8.5)
    ax.set_yticks(range(len(filas)))
    ax.set_yticklabels([f[0] for f in filas], fontsize=8.5)
    # las tres filas de la politica en negrita: es el metodo del paper y
    # conviene que se distinga de un vistazo entre trece barras
    for etiqueta, (nombre, _, _) in zip(ax.get_yticklabels(), filas):
        if nombre.startswith("Policy"):
            etiqueta.set_fontweight("bold")
    ax.invert_yaxis()
    ax.set_xlabel("Mean RE (%) over the 12 classical instances")
    ax.set_xlim(0, max(f[1] for f in filas) * 1.14)
    ax.legend(frameon=False, fontsize=8.5, loc="lower right")
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_ladder.pdf"))
    plt.close(fig)


# ----------------------------------------------------------------------
# Fig: frontera ancho-makespan del barrido de lambda (7.5)
# Origen: benchmarks/robust_lambda/rollouts.csv + rollouts_sweep.csv
# (90 pools de 64 rollouts con extremos inferior y superior)
# ----------------------------------------------------------------------
def fig_frontier():
    import csv
    from collections import defaultdict

    import glob as _gl
    pools = defaultdict(list)
    lbs = {}
    # los tres juegos de depositos: originales (semillas 2-4) y la
    # ampliacion a diez (5-11), cinco brazos
    for f in (["benchmarks/robust_lambda/rollouts.csv",
               "benchmarks/robust_lambda/rollouts_sweep.csv"]
              + sorted(_gl.glob(
                  "benchmarks/robust_lambda/rollouts_ext_*.csv"))):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            pools[(r["arm"], r["seed"], r["instance"])].append(
                (float(r["lower"]), float(r["upper"])))
            lbs[r["instance"]] = float(r["lb"])
    pools = {k: v[:64] for k, v in pools.items()}   # rollouts.csv se relee

    def sel(v, lam):
        # lam=None: el criterio lexicografico de la Eq. (3)
        if lam is None:
            return min(v, key=lambda t: (t[1], t[0]))
        return min(v, key=lambda t: t[1] + lam * (t[1] - t[0]))

    def punto(brazo, lam):
        ws, res = [], []
        for (a, _s, inst), v in pools.items():
            if a != brazo:
                continue
            lo, up = sel(v, lam)
            mid = (lo + up) / 2
            ws.append((up - lo) / mid * 100)
            res.append((mid - lbs[inst]) / lbs[inst] * 100)
        return sum(ws) / len(ws), sum(res) / len(res)

    BRAZOS = [("base", None, "0"), ("lam0p5", 0.5, "0.5"),
              ("lam1", 1.0, "1"), ("lam2", 2.0, "2"), ("lam4", 4.0, "4")]
    despl = [punto(b, lam) for b, lam, _ in BRAZOS]
    libre = [punto("base", lam) for _, lam, _ in BRAZOS]
    fija = [punto(b, None) for b, _, _ in BRAZOS]

    fig, ax = plt.subplots(figsize=(4.31, 3.03))
    ax.plot([w for w, _ in despl], [r for _, r in despl], "o-",
            color="steelblue", label="retrained at $\\lambda$, deployed",
            zorder=3)
    ax.plot([w for w, _ in libre], [r for _, r in libre], "s--",
            markerfacecolor="none", color="indianred",
            label="default weights, re-ranked by $f_\\lambda$", zorder=2)
    ax.scatter([w for w, _ in fija], [r for _, r in fija], marker="^",
               color="0.45",
               label="retrained arms, common criterion", zorder=2)
    for (w, r), (_, _, et) in zip(despl, BRAZOS):
        ax.annotate(f"$\\lambda{{=}}{et}$", (w, r), fontsize=8.5,
                    xytext=(4, 4), textcoords="offset points")
    ax.set_xlabel("mean relative width of the selected schedule (%)")
    ax.set_ylabel("mean RE (%)")
    ax.grid(alpha=0.3, linestyle="--")
    ax.legend(fontsize=8.5, loc="upper right")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_frontier.pdf"))
    plt.close(fig)
    print("frontera:", " ".join(f"({w:.2f},{r:.2f})" for w, r in despl))
    print("libre   :", " ".join(f"({w:.2f},{r:.2f})" for w, r in libre))
    print("fija    :", " ".join(f"({w:.2f},{r:.2f})" for w, r in fija))


if __name__ == "__main__":
    fig_scaling()
    fig_crosssize()
    fig_pools()
    fig_ablation()
    fig_headtohead()
    fig_importance()
    fig_eps()
    fig_byclass()
    fig_ladder()
    fig_frontier()
    print("Figuras generadas en", FIG_DIR)
