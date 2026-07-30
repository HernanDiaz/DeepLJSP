"""
Calcula la eps-robustez media de cada brazo de la ablacion, para completar
tab:ablation con las tres medidas (RE, ancho de intervalo y eps-robustez).

Para cada regla: se despacha una vez por instancia, se predice E[Cmax] y se
estima eps-barra por Monte Carlo con K realizaciones uniformes de las
duraciones (Eq. eps del paper). Se reporta media +- sd entre las reglas del
brazo, junto al Wilcoxon pareado full vs no-width sobre las semillas comunes.

Uso (tras la campana tuneada):
  python scripts/eval_ablation_robustness.py \
      --arm "full=benchmarks/reevo_fixedfit/gp_tuned_seed*.json" \
      --arm "nowidth=benchmarks/tuned/ablation/nowidth_seed*.json" \
      --arm "rob-full=benchmarks/tuned/robust/width_seed*.json" \
      --arm "rob-nowidth=benchmarks/tuned/robust/nowidth_seed*.json"
"""

import argparse
import glob
import json
import re
import sys

import numpy as np

sys.path.insert(0, ".")
sys.path.insert(0, "stochastic_experiment")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from decode_vec import sample_durations, decode_mc            # noqa: E402
from jobshop_rl.data import PROBLEM_REGISTRY                   # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.heuristics.gp_rule import GPRuleHeuristic      # noqa: E402
from jobshop_rl.models.interval import Interval                # noqa: E402

K = 1000


def instance_data(pid):
    prob = PROBLEM_REGISTRY[pid]()
    durs, mseq = prob["durations"], prob["sequences"]
    lo = [[float(d.lower) if isinstance(d, Interval) else float(d) for d in r]
          for r in durs]
    up = [[float(d.upper) if isinstance(d, Interval) else float(d) for d in r]
          for r in durs]
    return prob, lo, up, mseq


def eps_bar_of_rule(tree, insts, cache):
    h = GPRuleHeuristic(tree)
    vals = []
    for i, pid in enumerate(insts):
        prob, lo, up, mseq = cache[pid]
        env = EnvironmentFactory.create_from_problem(prob, "basic", seed=0)
        st = env.reset(); done = False; seq = []
        while not done and st["eligible_ops"]:
            f = env.get_features(st)
            a = min(h.select_action(st["eligible_ops"], f),
                    len(st["eligible_ops"]) - 1)
            seq.append(env.eligible_ops[a] + 1)
            st, _, done, _ = env.step(a)
        c = env.job_completion_time
        e_mid = (max(x.lower if isinstance(x, Interval) else x for x in c) +
                 max(x.upper if isinstance(x, Interval) else x for x in c)) / 2
        rng = np.random.default_rng(1000 * i)      # numeros comunes por instancia
        dur = sample_durations(lo, up, K, rng)
        cmax = decode_mc(seq, dur, mseq, K)
        vals.append(float(np.mean(np.abs(cmax - e_mid) / e_mid)))
    return sum(vals) / len(vals)


def wilcoxon(pairs):
    d = [a - b for a, b in pairs if abs(a - b) > 1e-12]
    n = len(d)
    if n < 6:
        return float("nan"), n
    r = sorted(d, key=abs); rk = {}; i = 0
    while i < n:
        j = i
        while j + 1 < n and abs(abs(r[j + 1]) - abs(r[i])) < 1e-12:
            j += 1
        rr = (i + j) / 2 + 1
        for k in range(i, j + 1):
            rk[id(r[k])] = rr
        i = j + 1
    wp = sum(rk[id(x)] for x in r if x > 0)
    mu = n * (n + 1) / 4; sd = (n * (n + 1) * (2 * n + 1) / 24) ** 0.5
    return (wp - mu) / sd, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", action="append", required=True,
                    help="nombre=patron_glob")
    ap.add_argument("--out", default=None,
                    help="CSV por regla (arm,rule,eps_bar_x1000); no "
                         "sobrescribe si existe")
    args = ap.parse_args()
    if args.out and __import__("os").path.exists(args.out):
        sys.exit(f"{args.out} ya existe; borralo a mano para recalcular")

    insts = [p for p in sorted(PROBLEM_REGISTRY)
             if re.match(r"int__tai\d+_\d+_\d+$", p)
             and lb_for_problem_name(p) is not None]
    cache = {pid: instance_data(pid) for pid in insts}

    out = {}
    filas = []            # (brazo, fichero, eps) para el CSV por regla
    for spec in args.arm:
        name, pattern = spec.split("=", 1)
        vals = []
        for p in sorted(glob.glob(pattern)):
            e = eps_bar_of_rule(
                json.load(open(p, encoding="utf-8"))["tree"], insts, cache)
            vals.append(e)
            filas.append((name, __import__("os").path.basename(p),
                          round(1000 * e, 4)))
            print(".", end="", flush=True)
        print(f" {name}: {len(vals)} reglas", flush=True)
        out[name] = vals

    if args.out:
        import csv as _csv
        with open(args.out, "w", encoding="utf-8", newline="") as fh:
            w = _csv.writer(fh)
            w.writerow(["arm", "rule", "eps_bar_x1000"])
            w.writerows(filas)
        print(f"\nCSV por regla -> {args.out}", flush=True)

    print(f"\n=== eps-robustez (x10^3), media +- sd entre reglas del brazo ===")
    for name, v in out.items():
        n = len(v); mu = sum(v) / n
        sd = (sum((x - mu) ** 2 for x in v) / (n - 1)) ** 0.5 if n > 1 else 0.0
        print(f"  {name:<14}: {1000*mu:.2f} ± {1000*sd:.2f}   (n={n})")

    for a, b in (("nowidth", "full"), ("rob-nowidth", "rob-full")):
        if a in out and b in out and len(out[a]) == len(out[b]):
            z, n = wilcoxon(list(zip(out[a], out[b])))
            print(f"  Wilcoxon {a} vs {b}: z={z:.2f} (n={n})")


if __name__ == "__main__":
    main()
