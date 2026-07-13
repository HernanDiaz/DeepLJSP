"""
EXPERIMENTO DE TRANSFERENCIA A ESTOCÁSTICO (Monte Carlo, uniforme en [lo,up]).

A diferencia de crisp/fuzzy (casos particulares del intervalo, transferencia
sin pérdida ya demostrada), el estocástico es un modelo DISTINTO: el intervalo
minimiza el peor caso; aquí medimos dos objetivos que pueden divergir de él:
  - ESPERADO  (riesgo-neutral): media del makespan sobre K escenarios.
  - CVaR-95   (riesgo-averso):  media del peor 5% de escenarios.

Hipótesis: las semillas de intervalo (peor-caso-óptimas) deberían transferir
MEJOR al CVaR (riesgo-averso) que al esperado (riesgo-neutral). Lo medimos con
la correlación de rankings intervalo->esperado vs intervalo->CVaR.

Salida: benchmarks/stochastic_transfer.csv + tabla por clase.
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

from decode_vec import sample_durations, decode_mc, expected_and_cvar  # noqa
from jobshop_rl.data import PROBLEM_REGISTRY  # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.models.interval import Interval  # noqa: E402

GEN = ["graspmor", "gtmwkr", "gp", "v2"]
CLASSES = ["15_15", "20_15", "20_20", "30_15", "30_20", "50_15", "50_20"]
K = 300   # escenarios Monte Carlo por instancia


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
    exp_re, cvar_re, int_up = [], [], []
    for line in open(path, encoding="utf-8"):
        if ";" not in line:
            continue
        perm_s, interval_s = line.strip().split(";")
        seq = [int(x) for x in perm_s.split()]
        up_val = float(interval_s.strip("[] ").split(",")[1])
        int_up.append(up_val)
        mk = decode_mc(seq, dur, mseq, K)
        e, c = expected_and_cvar(mk)
        exp_re.append((e - lb) / lb * 100)
        cvar_re.append((c - lb) / lb * 100)
    return exp_re, cvar_re, int_up


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
        rng = np.random.default_rng(12345)          # comun a todas las secuencias
        dur = sample_durations(lo, up, K, rng)       # K escenarios de la instancia
        m = re.search(r"tai(\d+_\d+)", pid)
        rec = {"instance": pid, "cls": m.group(1) if m else "ft10"}
        for g in GEN:
            r = process(pid, g, dur, mseq, lb)
            if r:
                exp_re, cvar_re, iup = r
                rec[f"{g}_exp_best"] = min(exp_re)
                rec[f"{g}_exp_mean"] = sum(exp_re) / len(exp_re)
                rec[f"{g}_cvar_best"] = min(cvar_re)
                rec[f"{g}_cvar_mean"] = sum(cvar_re) / len(cvar_re)
                rec[f"{g}_sp_exp"] = spearman(iup, exp_re)   # intervalo->esperado
                rec[f"{g}_sp_cvar"] = spearman(iup, cvar_re)  # intervalo->CVaR
            else:
                for k in ("exp_best", "exp_mean", "cvar_best", "cvar_mean",
                          "sp_exp", "sp_cvar"):
                    rec[f"{g}_{k}"] = float("nan")
        rows.append(rec)
        print(".", end="", flush=True)
    print()

    os.makedirs("benchmarks", exist_ok=True)
    keys = ("exp_best", "exp_mean", "cvar_best", "cvar_mean", "sp_exp", "sp_cvar")
    with open("benchmarks/stochastic_transfer.csv", "w", encoding="utf-8") as f:
        f.write("instance,cls," + ",".join(f"{g}_{k}" for g in GEN for k in keys) + "\n")
        for r in rows:
            f.write(f"{r['instance']},{r['cls']}," + ",".join(
                f"{r[f'{g}_{k}']:.3f}" for g in GEN for k in keys) + "\n")

    def avg(rs, key):
        v = [r[key] for r in rs if r[key] == r[key]]
        return sum(v) / len(v) if v else float("nan")

    def table(title, key):
        print(f"\n=== {title} ===")
        hdr = f"{'clase':<7}" + "".join(f"{g[:8]:>10}" for g in GEN)
        print(hdr)
        allr = []
        for c in CLASSES:
            cr = [r for r in rows if r["cls"] == c]; allr += cr
            print(f"{c:<7}" + "".join(f"{avg(cr, f'{g}_{key}'):>9.2f} " for g in GEN))
        print(f"{'GLOBAL':<7}" + "".join(f"{avg(allr, f'{g}_{key}'):>9.2f} " for g in GEN))

    table("ESPERADO: RE del MEJOR individuo (%)", "exp_best")
    table("CVaR-95: RE del MEJOR individuo (%)", "cvar_best")
    table("CORRELACION intervalo->ESPERADO (Spearman, riesgo-neutral)", "sp_exp")
    table("CORRELACION intervalo->CVaR-95 (Spearman, riesgo-averso)", "sp_cvar")
    # global de las dos correlaciones para la comparacion directa
    e = avg(rows, "v2_sp_exp"); c = avg(rows, "v2_sp_cvar")
    print(f"\n[v2] Spearman global: intervalo->esperado={e:.3f} vs "
          f"intervalo->CVaR={c:.3f}  (mayor = mejor alineado)")
    print("CSV: benchmarks/stochastic_transfer.csv")


if __name__ == "__main__":
    main()
