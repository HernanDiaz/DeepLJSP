"""
BARRIDO DE LAMBDA: la frontera calidad-predictibilidad del fitness robusto.

El fitness robusto minimiza  upper + lambda*(upper-lower), normalizado por LB.
Con lambda=1 ya sabemos (campana 30x2) que los terminales de anchura producen
intervalos significativamente mas estrechos, a cambio de ~0.9 pts de RE. Este
barrido caracteriza el TRADE-OFF completo: al crecer lambda, cuanto ancho se
gana y cuanto makespan esperado se paga.

Solo el brazo CON anchura: el brazo sin anchura es la referencia plana
(~12.4% de ancho haga lo que haga el objetivo, ya medido bajo midpoint y
lambda=1). lambda=1 se reutiliza de la campana anterior.

Salida: benchmarks/lambda_sweep/ + tabla con (lambda -> RE, ancho) y figura
paper_gp/figures/fig_lambda.pdf con la frontera.

Uso: python scripts/lambda_sweep.py [--seeds 10] [--dry]
"""

import argparse
import glob
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT = "benchmarks/lambda_sweep"
LOG = "logs/lambda_sweep"
PY = sys.executable
LAMBDAS = [0.5, 2.0, 4.0]          # lambda=1 ya esta en benchmarks/pilot_robust


def tag(lam):
    return str(lam).replace(".", "p")


def run_one(name, extra):
    out_json = f"{OUT}/{name}.json"
    if os.path.exists(out_json):
        print(f"[evo] {name}: ya existe, salto", flush=True)
        return
    t0 = time.time()
    with open(f"{LOG}/{name}.log", "w", encoding="utf-8") as lf:
        r = subprocess.run([PY, "scripts/evolve_gp_rule.py", "--out", out_json]
                           + extra, stdout=lf, stderr=subprocess.STDOUT)
    ok = r.returncode == 0 and os.path.exists(out_json)
    print(f"[evo] {name}: {'OK' if ok else 'FALLO'} "
          f"({(time.time()-t0)/60:.0f} min)", flush=True)


def evaluate_rule(tree, insts, PROBLEM_REGISTRY, lb_for, factory,
                  GPRuleHeuristic, Interval):
    h = GPRuleHeuristic(tree)
    res, widths = [], []
    for pid in insts:
        lb = lb_for(pid)
        if lb is None:
            continue
        env = factory.create_from_problem(PROBLEM_REGISTRY[pid](), "basic",
                                          seed=0)
        st = env.reset(); done = False
        while not done and st["eligible_ops"]:
            f = env.get_features(st)
            a = min(h.select_action(st["eligible_ops"], f),
                    len(st["eligible_ops"]) - 1)
            st, _, done, _ = env.step(a)
        comps = env.job_completion_time
        lo = max(c.lower if isinstance(c, Interval) else c for c in comps)
        up = max(c.upper if isinstance(c, Interval) else c for c in comps)
        res.append(((lo + up) / 2 - lb) / lb * 100)
        widths.append((up - lo) / ((up + lo) / 2) * 100)
    return sum(res) / len(res), sum(widths) / len(widths)


def st(v):
    n = len(v); mu = sum(v) / n
    sd = (sum((x - mu) ** 2 for x in v) / (n - 1)) ** 0.5 if n > 1 else 0.0
    return mu, sd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--eval-only", action="store_true")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True); os.makedirs(LOG, exist_ok=True)

    jobs = [(f"rob_lam{tag(l)}_seed{s}",
             ["--seed", str(s), "--fitness", "robust", "--lam", str(l)])
            for l in LAMBDAS for s in range(1, args.seeds + 1)]
    if args.dry:
        for n, e in jobs:
            print("DRY:", n, " ".join(e))
        return

    if not args.eval_only:
        print(f"[fase 1] {len(jobs)} evoluciones, 3 en paralelo ({time.ctime()})",
              flush=True)
        with ThreadPoolExecutor(max_workers=3) as ex:
            list(ex.map(lambda j: run_one(*j), jobs))

    # ---- evaluacion ----
    from jobshop_rl.data import PROBLEM_REGISTRY
    from jobshop_rl.data.literature_bounds import lb_for_problem_name
    from jobshop_rl.experiments.factory import EnvironmentFactory
    from jobshop_rl.heuristics.gp_rule import GPRuleHeuristic
    from jobshop_rl.models.interval import Interval

    insts = [p for p in sorted(PROBLEM_REGISTRY)
             if re.match(r"int__tai\d+_\d+_\d+$", p)]

    def arm(pattern):
        res, wid = [], []
        for p in sorted(glob.glob(pattern)):
            r, w = evaluate_rule(json.load(open(p, encoding="utf-8"))["tree"],
                                 insts, PROBLEM_REGISTRY, lb_for_problem_name,
                                 EnvironmentFactory, GPRuleHeuristic, Interval)
            res.append(r); wid.append(w)
            print(".", end="", flush=True)
        print()
        return res, wid

    rows = []
    for lam in LAMBDAS:
        r, w = arm(f"{OUT}/rob_lam{tag(lam)}_seed*.json")
        if r:
            rows.append((lam, st(r), st(w), len(r)))
    # lambda=1 desde la campana previa
    r1, w1 = arm("benchmarks/pilot_robust/robwidth_seed*.json")
    if r1:
        rows.append((1.0, st(r1), st(w1), len(r1)))
    rows.sort()

    print("\n=== Frontera calidad-predictibilidad (brazo CON anchura) ===")
    print(f"{'lambda':>8}{'n':>5}{'RE (%)':>18}{'ancho (%)':>18}")
    for lam, (mr, sr), (mw, sw), n in rows:
        print(f"{lam:>8.1f}{n:>5}{f'{mr:.2f} ± {sr:.2f}':>18}"
              f"{f'{mw:.2f} ± {sw:.2f}':>18}")

    with open(f"{OUT}/lambda_sweep.csv", "w", encoding="utf-8") as f:
        f.write("lambda,n,re_mean,re_sd,width_mean,width_sd\n")
        for lam, (mr, sr), (mw, sw), n in rows:
            f.write(f"{lam},{n},{mr:.4f},{sr:.4f},{mw:.4f},{sw:.4f}\n")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6.0, 3.6))
        xs = [r[2][0] for r in rows]; ys = [r[1][0] for r in rows]
        xe = [r[2][1] for r in rows]; ye = [r[1][1] for r in rows]
        ax.errorbar(xs, ys, xerr=xe, yerr=ye, fmt="-o", color="#d68910",
                    linewidth=1.8, capsize=3)
        for (lam, (mr, _), (mw, _), _) in rows:
            ax.annotate(f"$\\lambda$={lam:g}", (mw, mr),
                        textcoords="offset points", xytext=(6, 5), fontsize=9)
        ax.set_xlabel("relative width of the makespan interval (%)")
        ax.set_ylabel("mean RE (%)")
        ax.spines[["top", "right"]].set_visible(False)
        fig.tight_layout()
        fig.savefig("paper_gp/figures/fig_lambda.pdf")
        plt.close(fig)
        print("fig_lambda ok")
    except Exception as e:
        print("figura no generada:", e)
    print(f"\nCSV: {OUT}/lambda_sweep.csv")


if __name__ == "__main__":
    main()
