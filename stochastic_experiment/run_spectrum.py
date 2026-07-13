"""
ESPECTRO DE RIESGO COMPLETO (extiende run_stochastic.py sin sobreescribirlo).

Para cada secuencia y sus K makespans Monte Carlo, tres resúmenes de optimista
a pesimista:
  - OPTIMISTA: media del mejor 5% (riesgo-buscador; diagnóstico, no criterio real)
  - ESPERADO:  media de todos (riesgo-neutral)
  - CVaR-95:   media del peor 5% (riesgo-averso)

Mide la correlación del ranking del INTERVALO con cada objetivo. Predicción:
crece monótona con lo pesimista del objetivo (optimista < esperado < CVaR),
porque el intervalo optimiza el peor caso (upper). Bonus: el ranking por el
LOWER del intervalo debería alinearse con la cola optimista — los dos bordes
del intervalo son los dos extremos del riesgo.

Salida: benchmarks/stochastic_spectrum.csv + tabla + figura.
"""

import glob
import os
import re
import sys

import numpy as np

sys.path.insert(0, ".")
sys.path.insert(0, "stochastic_experiment")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from decode_vec import sample_durations, decode_mc  # noqa: E402
from jobshop_rl.data import PROBLEM_REGISTRY  # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.models.interval import Interval  # noqa: E402

GEN = ["graspmor", "gtmwkr", "gp", "v2"]
CLASSES = ["15_15", "20_15", "20_20", "30_15", "30_20", "50_15", "50_20"]
K = 300


def spearman(xs, ys):
    n = len(xs)
    rx = {v: i for i, v in enumerate(sorted(range(n), key=lambda k: xs[k]))}
    ry = {v: i for i, v in enumerate(sorted(range(n), key=lambda k: ys[k]))}
    d2 = sum((rx[k] - ry[k]) ** 2 for k in range(n))
    return 1 - 6 * d2 / (n * (n * n - 1))


def bounds(int_durs):
    lo = [[float(d.lower) if isinstance(d, Interval) else float(d) for d in row]
          for row in int_durs]
    up = [[float(d.upper) if isinstance(d, Interval) else float(d) for d in row]
          for row in int_durs]
    return lo, up


def process(pid, gen, dur, mseq, lb):
    path = f"seeds/{pid}_{gen}_pool.csv"
    if not os.path.exists(path):
        return None
    opt, exp, cvar, i_up, i_lo = [], [], [], [], []
    for line in open(path, encoding="utf-8"):
        if ";" not in line:
            continue
        perm_s, iv = line.strip().split(";")
        seq = [int(x) for x in perm_s.split()]
        lo_v, up_v = (float(x) for x in iv.strip("[] ").split(","))
        i_lo.append(lo_v); i_up.append(up_v)
        mk = decode_mc(seq, dur, mseq, K)
        q05, q95 = np.quantile(mk, 0.05), np.quantile(mk, 0.95)
        opt.append((float(mk[mk <= q05].mean()) - lb) / lb * 100)
        exp.append((float(mk.mean()) - lb) / lb * 100)
        cvar.append((float(mk[mk >= q95].mean()) - lb) / lb * 100)
    return {
        "opt_best": min(opt), "exp_best": min(exp), "cvar_best": min(cvar),
        # correlaciones del ranking por UPPER del intervalo con cada objetivo
        "sp_up_opt": spearman(i_up, opt),
        "sp_up_exp": spearman(i_up, exp),
        "sp_up_cvar": spearman(i_up, cvar),
        # bonus: ranking por LOWER del intervalo vs la cola optimista
        "sp_lo_opt": spearman(i_lo, opt),
    }


def main():
    instances = sorted({os.path.basename(f).split("_v2_pool")[0]
                        for f in glob.glob("seeds/*_v2_pool.csv")})
    rows = []
    for pid in instances:
        crisp_pid = pid.replace("int__", "")
        if not crisp_pid.startswith("tai") or crisp_pid not in PROBLEM_REGISTRY:
            continue
        int_durs = PROBLEM_REGISTRY[pid]()["durations"]
        mseq = PROBLEM_REGISTRY[crisp_pid]()["sequences"]
        lb = lb_for_problem_name(pid)
        if lb is None:
            continue
        lo, up = bounds(int_durs)
        rng = np.random.default_rng(12345)
        dur = sample_durations(lo, up, K, rng)
        m = re.search(r"tai(\d+_\d+)", pid)
        rec = {"instance": pid, "cls": m.group(1) if m else "ft10"}
        for g in GEN:
            r = process(pid, g, dur, mseq, lb)
            for k in ("opt_best", "exp_best", "cvar_best", "sp_up_opt",
                      "sp_up_exp", "sp_up_cvar", "sp_lo_opt"):
                rec[f"{g}_{k}"] = r[k] if r else float("nan")
        rows.append(rec)
        print(".", end="", flush=True)
    print()

    keys = ("opt_best", "exp_best", "cvar_best", "sp_up_opt", "sp_up_exp",
            "sp_up_cvar", "sp_lo_opt")
    os.makedirs("benchmarks", exist_ok=True)
    with open("benchmarks/stochastic_spectrum.csv", "w", encoding="utf-8") as f:
        f.write("instance,cls," + ",".join(f"{g}_{k}" for g in GEN for k in keys) + "\n")
        for r in rows:
            f.write(f"{r['instance']},{r['cls']}," + ",".join(
                f"{r[f'{g}_{k}']:.4f}" for g in GEN for k in keys) + "\n")

    def avg(k):
        v = [r[k] for r in rows if r[k] == r[k]]
        return sum(v) / len(v) if v else float("nan")

    print("\n=== ESPECTRO: correlación intervalo(upper) → objetivo (Spearman global) ===")
    print("(predicción: crece de optimista a CVaR)")
    print(f"{'generador':<10}{'optimista':>11}{'esperado':>11}{'CVaR-95':>11}")
    for g in GEN:
        print(f"{g:<10}{avg(f'{g}_sp_up_opt'):>11.3f}{avg(f'{g}_sp_up_exp'):>11.3f}"
              f"{avg(f'{g}_sp_up_cvar'):>11.3f}")

    print("\n=== BONUS: los dos bordes del intervalo ↔ las dos colas ===")
    for g in ("gp", "v2"):
        print(f"  {g}: upper→CVaR={avg(f'{g}_sp_up_cvar'):.3f}  |  "
              f"lower→optimista={avg(f'{g}_sp_lo_opt'):.3f}  "
              f"(vs upper→optimista={avg(f'{g}_sp_up_opt'):.3f})")

    print("\n=== RE del MEJOR individuo por objetivo (v2/gp global) ===")
    for g in ("gp", "v2"):
        print(f"  {g}: optimista={avg(f'{g}_opt_best'):.1f}%  "
              f"esperado={avg(f'{g}_exp_best'):.1f}%  "
              f"CVaR={avg(f'{g}_cvar_best'):.1f}%")

    # figura del gradiente monotono
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    COL = {"gp": "#d68910", "v2": "#1f5fa8"}
    LAB = {"gp": "GP-ε", "v2": "v2 (RL)"}
    fig, ax = plt.subplots(figsize=(7, 5))
    xt = ["optimista\n(mejor 5%)", "esperado\n(media)", "CVaR-95\n(peor 5%)"]
    for g in ("gp", "v2"):
        ys = [avg(f"{g}_sp_up_opt"), avg(f"{g}_sp_up_exp"), avg(f"{g}_sp_up_cvar")]
        ax.plot(range(3), ys, "-o", color=COL[g], linewidth=2.2,
                markersize=9, label=LAB[g])
    ax.set_xticks(range(3)); ax.set_xticklabels(xt)
    ax.set_ylabel("Spearman  ranking intervalo(peor caso) → objetivo")
    ax.set_xlabel("← riesgo-buscador          riesgo-averso →")
    ax.set_title("El alineamiento de las semillas de intervalo crece\n"
                 "monótonamente con la aversión al riesgo", fontsize=12)
    ax.legend(frameon=False)
    ax.grid(alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig("benchmarks/figures/fig_risk_spectrum.pdf")
    fig.savefig("benchmarks/figures/fig_risk_spectrum.png", dpi=150)
    print("\nfigura: benchmarks/figures/fig_risk_spectrum.png")
    print("CSV: benchmarks/stochastic_spectrum.csv")


if __name__ == "__main__":
    main()
