"""
PILOTO: ¿los terminales de anchura pagan cuando el OBJETIVO premia la robustez?

La ablacion anterior (fitness = makespan midpoint) mostro que la anchura no
aporta -- pero era esperable: el objetivo no premiaba la incertidumbre. Aqui
el fitness es ROBUSTO (upper + lam*ancho), asi que la anchura SI deberia
importar. Test decisivo: evolucionar con y sin terminales de anchura bajo el
fitness robusto y comparar la robustez de las reglas resultantes.

  - robust+width   : fitness robusto, terminales completos
  - robust+nowidth : fitness robusto, sin PTW/ESTW/WKRW

Hipotesis: si la anchura lleva informacion accionable, robust+width producira
schedules con intervalo de makespan mas estrecho (y mejor eps-barra) que
robust+nowidth, y ablarla dolera.

Piloto de 5 seeds/brazo (concept check antes de comprometer 30).
Fase 1: 10 evoluciones (3 en paralelo). Fase 2: evaluar cada regla en las 70
instancias -> ancho relativo del intervalo de makespan + RE midpoint. Anatomia.

Uso: python scripts/pilot_robust_fitness.py  [--lam 1.0] [--seeds 5]
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

OUT = "benchmarks/pilot_robust"
LOG = "logs/pilot_robust"
PY = sys.executable


def build_jobs(seeds, lam):
    common = ["--fitness", "robust", "--lam", str(lam)]
    jobs = []
    for s in range(1, seeds + 1):
        jobs.append((f"robwidth_seed{s}", ["--seed", str(s)] + common))
        jobs.append((f"robnowidth_seed{s}",
                     ["--seed", str(s), "--no-width"] + common))
    return jobs


def run_one(name, extra):
    out_json = f"{OUT}/{name}.json"
    cmd = [PY, "scripts/evolve_gp_rule.py", "--out", out_json] + extra
    t0 = time.time()
    with open(f"{LOG}/{name}.log", "w", encoding="utf-8") as lf:
        r = subprocess.run(cmd, stdout=lf, stderr=subprocess.STDOUT)
    ok = r.returncode == 0 and os.path.exists(out_json)
    print(f"[fase 1] {name}: {'OK' if ok else 'FALLO'} "
          f"({(time.time()-t0)/60:.0f} min)", flush=True)
    return name, ok


def evaluate():
    from jobshop_rl.data import PROBLEM_REGISTRY
    from jobshop_rl.data.literature_bounds import lb_for_problem_name
    from jobshop_rl.experiments.factory import EnvironmentFactory
    from jobshop_rl.heuristics.gp_rule import GPRuleHeuristic
    from jobshop_rl.models.interval import Interval

    insts = [p for p in sorted(PROBLEM_REGISTRY)
             if re.match(r"int__tai\d+_\d+_\d+$", p)]

    def eval_rule(tree):
        h = GPRuleHeuristic(tree)
        res, widths = [], []
        for pid in insts:
            lb = lb_for_problem_name(pid)
            env = EnvironmentFactory.create_from_problem(
                PROBLEM_REGISTRY[pid](), "basic", seed=0)
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

    def arm(prefix):
        re_l, w_l = [], []
        for p in sorted(glob.glob(f"{OUT}/{prefix}_seed*.json")):
            re_v, w_v = eval_rule(json.load(open(p, encoding="utf-8"))["tree"])
            re_l.append(re_v); w_l.append(w_v)
            print(".", end="", flush=True)
        print()
        return re_l, w_l

    def st(v):
        n = len(v); mu = sum(v) / n
        sd = (sum((x - mu) ** 2 for x in v) / (n - 1)) ** 0.5 if n > 1 else 0
        return mu, sd

    rw_re, rw_w = arm("robwidth")
    rn_re, rn_w = arm("robnowidth")

    print("\n=== PILOTO fitness robusto: width vs no-width ===")
    print(f"{'brazo':<16}{'RE midpoint':>16}{'ancho interv. %':>18}")
    print(f"{'robust+width':<16}{f'{st(rw_re)[0]:.2f} ± {st(rw_re)[1]:.2f}':>16}"
          f"{f'{st(rw_w)[0]:.2f} ± {st(rw_w)[1]:.2f}':>18}")
    print(f"{'robust+nowidth':<16}{f'{st(rn_re)[0]:.2f} ± {st(rn_re)[1]:.2f}':>16}"
          f"{f'{st(rn_w)[0]:.2f} ± {st(rn_w)[1]:.2f}':>18}")
    dw = st(rn_w)[0] - st(rw_w)[0]
    print(f"\nDelta ancho (nowidth - width): {dw:+.3f} pts")
    print("  >0 => quitar la anchura ENSANCHA el intervalo => los terminales")
    print("        de anchura SI ayudan bajo objetivo robusto (novedad recuperada)")
    print("  <=0 => la anchura no ayuda ni con objetivo robusto")

    with open(f"{OUT}/VEREDICTO_PILOTO.md", "w", encoding="utf-8") as f:
        f.write(f"# Piloto fitness robusto (upper + lam*ancho), 5 seeds/brazo\n\n"
                f"| brazo | RE midpoint | ancho intervalo (%) |\n|---|---|---|\n"
                f"| robust+width | {st(rw_re)[0]:.2f}±{st(rw_re)[1]:.2f} | "
                f"{st(rw_w)[0]:.2f}±{st(rw_w)[1]:.2f} |\n"
                f"| robust+nowidth | {st(rn_re)[0]:.2f}±{st(rn_re)[1]:.2f} | "
                f"{st(rn_w)[0]:.2f}±{st(rn_w)[1]:.2f} |\n\n"
                f"Delta ancho (nowidth-width) = {dw:+.3f} pts. "
                f">0 => la anchura ayuda bajo objetivo robusto.\n")
    print(f"\nVEREDICTO_PILOTO.md en {OUT}/")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lam", type=float, default=1.0)
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True); os.makedirs(LOG, exist_ok=True)
    jobs = build_jobs(args.seeds, args.lam)
    if args.dry:
        for n, e in jobs:
            print("DRY:", n, " ".join(e))
        return
    print(f"[fase 1] {len(jobs)} evoluciones (lam={args.lam}), 3 en paralelo "
          f"({time.ctime()})", flush=True)
    with ThreadPoolExecutor(max_workers=3) as ex:
        list(ex.map(lambda j: run_one(*j), jobs))
    print(f"[fase 2] evaluacion 70 instancias ({time.ctime()})", flush=True)
    evaluate()


if __name__ == "__main__":
    main()
