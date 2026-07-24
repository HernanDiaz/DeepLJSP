"""
Robustez epsilon-barra de los schedules (firma metodológica del grupo).

Replica la epsilon-robustness de Díaz et al. (IPMU 2020, eqs. 17-18): para un
schedule con orden de proceso fijo y makespan de intervalo predicho C_max, con
E[C_max] = midpoint, se mide sobre K realizaciones (duraciones ~ U[lo,up]):

    eps_barra = (1/K) sum_k |C^k_max - E[C_max]| / E[C_max]

C^k_max = makespan CRISP ejecutando el orden fijo con la realización k. Menor
eps_barra = predicción a-priori más fiable = schedule más robusto.

Análisis de sensibilidad a la incertidumbre (fEABC, tabla 4): se repite con las
anchuras de intervalo ampliadas +0/+20/+40% simétricamente respecto al midpoint
(si el lower saliera negativo se recorta a 0), evaluando el MISMO orden.

Compara por método: la regla GP interval-aware, la ablación no-width (si existe),
y los baselines MOR y GT-MWKR. Salida: benchmarks/robustness_eps.csv + figuras
(boxplots por método/anchura, histogramas estilo fEABC Fig 3).

Uso:
  python scripts/robustness_epsilon.py --rule benchmarks/gp_rule_seed1.json
  python scripts/robustness_epsilon.py --rule ... --nowidth benchmarks/reevo_fixedfit/gp_nowidth_seed1.json
"""

import argparse
import json
import os
import re
import sys

import numpy as np

sys.path.insert(0, ".")
sys.path.insert(0, "stochastic_experiment")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from decode_vec import sample_durations, decode_mc          # noqa: E402
from jobshop_rl.data import PROBLEM_REGISTRY                 # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory     # noqa: E402
from jobshop_rl.heuristics.gp_rule import GPRuleHeuristic         # noqa: E402
from jobshop_rl.heuristics.strategies import MORHeuristic, GTHeuristic  # noqa: E402
from jobshop_rl.models.interval import Interval               # noqa: E402

WIDTHS = [1.0, 1.2, 1.4]     # +0%, +20%, +40%
K = 1000


def instance_arrays(pid):
    """lo[j][k], up[j][k] (float) y machine_seq[j][k] de la instancia."""
    prob = PROBLEM_REGISTRY[pid]()
    durs, mseq = prob["durations"], prob["sequences"]
    lo = [[float(d.lower) if isinstance(d, Interval) else float(d) for d in row]
          for row in durs]
    up = [[float(d.upper) if isinstance(d, Interval) else float(d) for d in row]
          for row in durs]
    return lo, up, mseq


def widen(lo, up, w):
    """Amplía anchuras al factor w manteniendo el midpoint (lower recortado a 0)."""
    nlo, nup = [], []
    for rlo, rup in zip(lo, up):
        a, b = [], []
        for x, y in zip(rlo, rup):
            mid = (x + y) / 2.0
            half = (y - x) / 2.0 * w
            a.append(max(0.0, mid - half))
            b.append(mid + half)
        nlo.append(a); nup.append(b)
    return nlo, nup


def predicted_interval(seq, lo, up, mseq):
    """Makespan de intervalo predicho [C_lo, C_up] (componente a componente)."""
    nj = len(lo); nm = len(mseq[0])
    jlo = [0.0] * nj; jup = [0.0] * nj
    mlo = [0.0] * nm; mup = [0.0] * nm
    oi = [0] * nj
    for j1 in seq:
        j = j1 - 1; k = oi[j]; m = mseq[j][k]
        slo = max(jlo[j], mlo[m]); sup = max(jup[j], mup[m])
        elo = slo + lo[j][k]; eup = sup + up[j][k]
        jlo[j] = elo; jup[j] = eup; mlo[m] = elo; mup[m] = eup
        oi[j] = k + 1
    return max(jlo), max(jup)


def predicted_midpoint(seq, lo, up, mseq):
    """E[C_max] = midpoint del makespan de intervalo."""
    clo, cup = predicted_interval(seq, lo, up, mseq)
    return (clo + cup) / 2.0


def heuristic_sequence(env, heuristic):
    """Ejecuta la heurística y devuelve el orden de proceso (jobs 1-based)."""
    state = env.reset()
    seq = []
    done = False
    while not done and state["eligible_ops"]:
        f = env.get_features(state)
        idx = min(heuristic.select_action(state["eligible_ops"], f),
                  len(state["eligible_ops"]) - 1)
        seq.append(env.eligible_ops[idx] + 1)   # job 1-based
        state, _, done, _ = env.step(idx)
    return seq


def eps_bar(seq, lo, up, mseq, rng):
    """eps-barra sobre K realizaciones uniformes de [lo,up]."""
    e_mid = predicted_midpoint(seq, lo, up, mseq)
    dur = sample_durations(lo, up, K, rng)
    cmax = decode_mc(seq, dur, mseq, K)           # array (K,)
    return float(np.mean(np.abs(cmax - e_mid) / e_mid)), e_mid, cmax


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rule", default="benchmarks/gp_rule_seed1.json",
                    help="regla GP interval-aware (JSON)")
    ap.add_argument("--nowidth", default="",
                    help="regla ablación no-width (JSON), opcional")
    ap.add_argument("--hist-instance", default="int__tai20_20_02",
                    help="instancia para los histogramas estilo fEABC Fig 3")
    ap.add_argument("--out", default="benchmarks/robustness_eps.csv")
    args = ap.parse_args()

    methods = {"GP": GPRuleHeuristic(json.load(open(args.rule))["tree"]),
               "MOR": MORHeuristic(),
               "GT-MWKR": GTHeuristic(tiebreak="mwkr")}
    if args.nowidth and os.path.exists(args.nowidth):
        methods["GP-nowidth"] = GPRuleHeuristic(
            json.load(open(args.nowidth))["tree"])

    instances = [p for p in sorted(PROBLEM_REGISTRY)
                 if re.match(r"int__tai\d+_\d+_\d+$", p)]

    rows = []
    hist = {}
    for i, pid in enumerate(instances):
        if lb_for_problem_name(pid) is None:
            continue
        lo0, up0, mseq = instance_arrays(pid)
        cls = re.search(r"tai(\d+_\d+)", pid).group(1)
        env = EnvironmentFactory.create_from_problem(
            PROBLEM_REGISTRY[pid](), "basic", seed=0)
        seqs = {name: heuristic_sequence(env, h) for name, h in methods.items()}
        for name, seq in seqs.items():
            # Ancho relativo del intervalo de makespan predicho (a-priori, nominal):
            # rel_width = (C_up - C_lo) / midpoint * 100. Más estrecho = mejor.
            clo, cup = predicted_interval(seq, lo0, up0, mseq)
            rel_width = (cup - clo) / ((clo + cup) / 2.0) * 100.0
            for wi, w in enumerate(WIDTHS):
                lo, up = widen(lo0, up0, w) if w != 1.0 else (lo0, up0)
                # semilla determinista por (instancia, anchura): reproducible y
                # con números comunes entre métodos (misma nube por instancia).
                rng = np.random.default_rng(1000 * i + wi)
                eb, e_mid, cmax = eps_bar(seq, lo, up, mseq, rng)
                rows.append({"instance": pid, "cls": cls, "method": name,
                             "width": w, "eps_bar": eb,
                             "rel_width": rel_width if w == 1.0 else float("nan")})
                if pid == args.hist_instance:
                    hist[(name, w)] = (cmax, e_mid)
        print(".", end="", flush=True)
    print()

    with open(args.out, "w", encoding="utf-8") as f:
        f.write("instance,cls,method,width,eps_bar,rel_width\n")
        for r in rows:
            rw = f"{r['rel_width']:.4f}" if r["rel_width"] == r["rel_width"] else ""
            f.write(f"{r['instance']},{r['cls']},{r['method']},"
                    f"{r['width']:.1f},{r['eps_bar']*1000:.4f},{rw}\n")

    # Resumen: eps-barra media (x1000) por método y anchura
    print("\n=== eps-barra media (x1000) por método y anchura ===")
    print(f"{'método':<12}" + "".join(f"{f'+{round((w-1)*100)}%':>10}" for w in WIDTHS))
    for name in methods:
        line = f"{name:<12}"
        for w in WIDTHS:
            vals = [r["eps_bar"] for r in rows
                    if r["method"] == name and r["width"] == w]
            line += f"{1000*sum(vals)/len(vals):>10.2f}"
        print(line)

    # Resumen: ancho relativo del intervalo de makespan predicho (%, nominal)
    print("\n=== ancho relativo del intervalo de makespan (%, más estrecho=mejor) ===")
    for name in methods:
        vals = [r["rel_width"] for r in rows if r["method"] == name
                and r["width"] == 1.0 and r["rel_width"] == r["rel_width"]]
        print(f"  {name:<12}: {sum(vals)/len(vals):.2f}%")

    _figures(rows, hist, methods)
    print(f"\nCSV: {args.out}")


def _figures(rows, hist, methods):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    os.makedirs("paper_gp/figures", exist_ok=True)
    COL = {"GP": "#d68910", "GP-nowidth": "#a04000",
           "MOR": "#5d6d7e", "GT-MWKR": "#0e8a7d"}

    # Fig A: boxplots de eps-barra por método, un panel por anchura
    fig, axes = plt.subplots(1, len(WIDTHS), figsize=(9, 3.4), sharey=True)
    for ax, w in zip(axes, WIDTHS):
        data = [[r["eps_bar"] * 1000 for r in rows
                 if r["method"] == m and r["width"] == w] for m in methods]
        bp = ax.boxplot(data, tick_labels=list(methods), patch_artist=True,
                        widths=0.6, showfliers=False)
        for patch, m in zip(bp["boxes"], methods):
            patch.set_facecolor(COL.get(m, "#888")); patch.set_alpha(0.75)
        ax.set_title(f"+{round((w-1)*100)}% width", fontsize=10)
        ax.tick_params(axis="x", rotation=30, labelsize=8)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel(r"$\bar{\varepsilon}$ ($\times 10^{3}$)")
    fig.tight_layout()
    fig.savefig("paper_gp/figures/fig_robustness_box.pdf")
    plt.close(fig)
    print("fig_robustness_box ok")

    # Fig B: histogramas de C^k_max (instancia elegida), GP vs MOR, +0/+40%
    if hist:
        pairs = [(m, w) for m in ("GP", "MOR") for w in (1.0, 1.4)
                 if (m, w) in hist]
        if pairs:
            fig, axes = plt.subplots(len(pairs) // 2, 2, figsize=(8, 5),
                                     squeeze=False)
            for ax, (m, w) in zip(axes.ravel(), pairs):
                cmax, e_mid = hist[(m, w)]
                ax.hist(cmax, bins=40, color=COL.get(m, "#888"), alpha=0.8)
                ax.axvline(e_mid, color="red", lw=1.5)
                ax.set_title(f"{m}, +{round((w-1)*100)}%", fontsize=10)
                ax.spines[["top", "right"]].set_visible(False)
            fig.supxlabel(r"executed makespan $C^{ex}_{max}$")
            fig.tight_layout()
            fig.savefig("paper_gp/figures/fig_robustness_hist.pdf")
            plt.close(fig)
            print("fig_robustness_hist ok")


if __name__ == "__main__":
    main()
