"""
Ablación rigurosa 30-vs-30: ¿los terminales de anchura reducen el ANCHO del
intervalo de makespan? Compara la distribución del ancho relativo (a-priori,
sin Monte Carlo) del brazo full vs no-width sobre las 70 instancias.
"""
import glob
import json
import re
import sys

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data import PROBLEM_REGISTRY
from jobshop_rl.experiments.factory import EnvironmentFactory
from jobshop_rl.heuristics.gp_rule import GPRuleHeuristic
from jobshop_rl.models.interval import Interval

INSTS = [p for p in sorted(PROBLEM_REGISTRY) if re.match(r"int__tai\d+_\d+_\d+$", p)]


def rel_width_of_rule(tree):
    h = GPRuleHeuristic(tree)
    ws = []
    for pid in INSTS:
        prob = PROBLEM_REGISTRY[pid]()
        env = EnvironmentFactory.create_from_problem(prob, "basic", seed=0)
        st = env.reset()
        done = False
        while not done and st["eligible_ops"]:
            f = env.get_features(st)
            a = min(h.select_action(st["eligible_ops"], f),
                    len(st["eligible_ops"]) - 1)
            st, _, done, _ = env.step(a)
        comps = env.job_completion_time
        lo = max(c.lower if isinstance(c, Interval) else c for c in comps)
        up = max(c.upper if isinstance(c, Interval) else c for c in comps)
        ws.append((up - lo) / ((up + lo) / 2) * 100)
    return sum(ws) / len(ws)


def arm(a):
    out = []
    for p in sorted(glob.glob(f"benchmarks/reevo_fixedfit/{a}_seed*.json")):
        out.append(rel_width_of_rule(json.load(open(p, encoding="utf-8"))["tree"]))
        print(".", end="", flush=True)
    print()
    return out


def st(v):
    n = len(v); mu = sum(v) / n
    sd = (sum((x - mu) ** 2 for x in v) / (n - 1)) ** 0.5
    return mu, sd, n


def mann_whitney_z(full, now):
    allv = sorted([(x, "f") for x in full] + [(x, "n") for x in now])
    ranks = {}; i = 0
    while i < len(allv):
        j = i
        while j + 1 < len(allv) and allv[j + 1][0] == allv[i][0]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[k] = r
        i = j + 1
    Rf = sum(ranks[k] for k, (x, g) in enumerate(allv) if g == "f")
    n1, n2 = len(full), len(now)
    U = Rf - n1 * (n1 + 1) / 2
    mu = n1 * n2 / 2; sd = (n1 * n2 * (n1 + n2 + 1) / 12) ** 0.5
    return (U - mu) / sd


def main():
    full = arm("gp_rule")
    now = arm("gp_nowidth")
    mf, sf, nf = st(full); mn, sn, nn = st(now)
    z = mann_whitney_z(full, now)
    print("\nANCHO RELATIVO del intervalo de makespan (media/70 inst., por regla):")
    print(f"  GP-full     (n={nf}): {mf:.2f} ± {sf:.2f} %")
    print(f"  GP-no-width (n={nn}): {mn:.2f} ± {sn:.2f} %")
    print(f"  Delta (no-width - full): {mn - mf:+.3f} pts")
    print(f"  Mann-Whitney U: z={z:.2f}  "
          f"({'SIGNIFICATIVO' if abs(z) > 1.96 else 'NO significativo'} al 5%)")


if __name__ == "__main__":
    main()
