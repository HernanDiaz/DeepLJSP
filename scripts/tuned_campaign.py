"""
CAMPANA COMPLETA CON LA CONFIGURACION GANADORA DE IRACE.

El paper pasa a reportar la configuracion tuneada (tournament 7, crossover
0.7695, maxtree 30, elitism 2) como principal. Todos los experimentos de
ANALISIS se habian ejecutado con la configuracion por defecto, asi que hay
que rehacerlos con la tuneada para que el paper sea coherente.

120 evoluciones nuevas (el brazo 'full+tuned' ya existe: gp_tuned_seed1..30):
  A) ablacion  : 30 x (tuned, --no-width)
  B) robusto   : 30 x (tuned, robust, lam=1, con anchura)
                 30 x (tuned, robust, lam=1, --no-width)
  C) barrido   : 10 x (tuned, robust, lam=0.5 / 2 / 4, con anchura)

NO se sobreescribe nada: todo va a benchmarks/tuned/{ablation,robust,lambda}/.
Reejecutable: los JSON ya existentes se saltan.

Fase 2: evalua cada regla (nueva y las 30 tuned ya existentes) en las 70
instancias, midiendo RE (midpoint) y anchura relativa del intervalo de
makespan, y escribe benchmarks/tuned/RESULTADOS.md con las comparaciones y
los tests de Wilcoxon.

Uso:  python scripts/tuned_campaign.py [--dry] [--eval-only]
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

PY = sys.executable
ROOT = "benchmarks/tuned"
LOG = "logs/tuned_campaign"
TUNED = ["--tournament", "7", "--crossover", "0.7695",
         "--maxtree", "30", "--elitism", "2"]
N = 30
LAMBDAS = [0.5, 2.0, 4.0]


def tag(x):
    return str(x).replace(".", "p")


def jobs():
    J = []
    for s in range(1, N + 1):
        J.append((f"{ROOT}/ablation/nowidth_seed{s}",
                  ["--seed", str(s), "--no-width"] + TUNED))
        J.append((f"{ROOT}/robust/width_seed{s}",
                  ["--seed", str(s), "--fitness", "robust", "--lam", "1.0"]
                  + TUNED))
        J.append((f"{ROOT}/robust/nowidth_seed{s}",
                  ["--seed", str(s), "--no-width", "--fitness", "robust",
                   "--lam", "1.0"] + TUNED))
    for lam in LAMBDAS:
        for s in range(1, 11):
            J.append((f"{ROOT}/lambda/lam{tag(lam)}_seed{s}",
                      ["--seed", str(s), "--fitness", "robust",
                       "--lam", str(lam)] + TUNED))
    return J


def run_one(stem, extra):
    out = stem + ".json"
    if os.path.exists(out):
        print(f"[evo] {os.path.basename(stem)}: ya existe", flush=True)
        return
    os.makedirs(os.path.dirname(out), exist_ok=True)
    t0 = time.time()
    logf = os.path.join(LOG, os.path.basename(stem) + ".log")
    with open(logf, "w", encoding="utf-8") as lf:
        r = subprocess.run([PY, "scripts/evolve_gp_rule.py", "--out", out]
                           + extra, stdout=lf, stderr=subprocess.STDOUT)
    ok = r.returncode == 0 and os.path.exists(out)
    print(f"[evo] {os.path.basename(stem)}: {'OK' if ok else 'FALLO'} "
          f"({(time.time() - t0) / 60:.0f} min)", flush=True)


# ----------------------------------------------------------------- evaluacion
def evaluate_all():
    from jobshop_rl.data import PROBLEM_REGISTRY
    from jobshop_rl.data.literature_bounds import lb_for_problem_name
    from jobshop_rl.experiments.factory import EnvironmentFactory
    from jobshop_rl.heuristics.gp_rule import GPRuleHeuristic, tree_size
    from jobshop_rl.models.interval import Interval

    insts = [p for p in sorted(PROBLEM_REGISTRY)
             if re.match(r"int__tai\d+_\d+_\d+$", p)]

    def eval_rule(path):
        tree = json.load(open(path, encoding="utf-8"))["tree"]
        h = GPRuleHeuristic(tree)
        res, wid = [], []
        for pid in insts:
            lb = lb_for_problem_name(pid)
            if lb is None:
                continue
            env = EnvironmentFactory.create_from_problem(
                PROBLEM_REGISTRY[pid](), "basic", seed=0)
            st = env.reset(); done = False
            while not done and st["eligible_ops"]:
                f = env.get_features(st)
                a = min(h.select_action(st["eligible_ops"], f),
                        len(st["eligible_ops"]) - 1)
                st, _, done, _ = env.step(a)
            c = env.job_completion_time
            lo = max(x.lower if isinstance(x, Interval) else x for x in c)
            up = max(x.upper if isinstance(x, Interval) else x for x in c)
            res.append(((lo + up) / 2 - lb) / lb * 100)
            wid.append((up - lo) / ((up + lo) / 2) * 100)
        return (sum(res) / len(res), sum(wid) / len(wid), tree_size(tree))

    def arm(pattern):
        out = {}
        for p in sorted(glob.glob(pattern)):
            out[os.path.basename(p)[:-5]] = eval_rule(p)
            print(".", end="", flush=True)
        print(f" [{len(out)}]", flush=True)
        return out

    print("[eval] full+tuned (existentes)", flush=True)
    full = arm("benchmarks/reevo_fixedfit/gp_tuned_seed*.json")
    print("[eval] ablacion no-width", flush=True)
    abl = arm(f"{ROOT}/ablation/nowidth_seed*.json")
    print("[eval] robusto con anchura", flush=True)
    rw = arm(f"{ROOT}/robust/width_seed*.json")
    print("[eval] robusto sin anchura", flush=True)
    rn = arm(f"{ROOT}/robust/nowidth_seed*.json")
    lam = {l: arm(f"{ROOT}/lambda/lam{tag(l)}_seed*.json") for l in LAMBDAS}

    def st(v):
        n = len(v); mu = sum(v) / n
        sd = (sum((x - mu) ** 2 for x in v) / (n - 1)) ** 0.5 if n > 1 else 0.0
        return mu, sd

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

    def col(d, k):   # k: 0=RE, 1=ancho, 2=nodos
        return [v[k] for v in d.values()]

    def paired(a, b, k):
        ka, kb = sorted(a), sorted(b)
        return [(a[x][k], b[y][k]) for x, y in zip(ka, kb)]

    L = ["# Campana con la configuracion ganadora de irace", "",
         "Config: tournament 7, crossover 0.7695, maxtree 30, elitism 2.",
         "Todas las cifras sobre las 70 instancias Taillard de intervalo.", ""]

    L += ["## Resultados principales (objetivo makespan)", "",
          "| brazo | n | RE (%) | ancho (%) | nodos |", "|---|---|---|---|---|"]
    for name, d in [("full (tuned)", full), ("no-width (tuned)", abl)]:
        if not d:
            continue
        r, w, s = (st(col(d, i)) for i in range(3))
        L.append(f"| {name} | {len(d)} | {r[0]:.2f} ± {r[1]:.2f} | "
                 f"{w[0]:.2f} ± {w[1]:.2f} | {s[0]:.1f} |")
    if full and abl:
        z, n = wilcoxon(paired(abl, full, 0))
        zw, _ = wilcoxon(paired(abl, full, 1))
        L += ["", f"Wilcoxon pareado no-width vs full: RE z={z:.2f}, "
                  f"ancho z={zw:.2f} (n={n})"]
        best = min(full, key=lambda k: full[k][0])
        L += ["", f"Mejor regla: {best} -> RE {full[best][0]:.2f}%, "
                  f"ancho {full[best][1]:.2f}%, {full[best][2]} nodos"]

    L += ["", "## Objetivo robusto (upper + lambda*ancho, lambda=1)", "",
          "| brazo | n | RE (%) | ancho (%) |", "|---|---|---|---|"]
    for name, d in [("robust+width", rw), ("robust+nowidth", rn)]:
        if not d:
            continue
        r, w = st(col(d, 0)), st(col(d, 1))
        L.append(f"| {name} | {len(d)} | {r[0]:.2f} ± {r[1]:.2f} | "
                 f"{w[0]:.2f} ± {w[1]:.2f} |")
    if rw and rn:
        z, n = wilcoxon(paired(rn, rw, 1))
        L += ["", f"Wilcoxon pareado sobre el ancho (nowidth - width): "
                  f"z={z:.2f} (n={n})"]

    L += ["", "## Frontera calidad-predictibilidad", "",
          "| lambda | n | RE (%) | ancho (%) |", "|---|---|---|---|"]
    rows = [(1.0, rw)] + [(l, lam[l]) for l in LAMBDAS]
    for l, d in sorted(rows):
        if not d:
            continue
        r, w = st(col(d, 0)), st(col(d, 1))
        L.append(f"| {l} | {len(d)} | {r[0]:.2f} ± {r[1]:.2f} | "
                 f"{w[0]:.2f} ± {w[1]:.2f} |")

    txt = "\n".join(L)
    with open(f"{ROOT}/RESULTADOS.md", "w", encoding="utf-8") as f:
        f.write(txt + "\n")
    print("\n" + txt, flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--eval-only", action="store_true")
    a = ap.parse_args()
    os.makedirs(LOG, exist_ok=True)
    J = jobs()
    if a.dry:
        for s, e in J:
            print("DRY:", s, " ".join(e))
        print(f"total: {len(J)}")
        return
    if not a.eval_only:
        print(f"[fase 1] {len(J)} evoluciones, 3 en paralelo ({time.ctime()})",
              flush=True)
        with ThreadPoolExecutor(max_workers=3) as ex:
            list(ex.map(lambda j: run_one(*j), J))
    print(f"[fase 2] evaluacion ({time.ctime()})", flush=True)
    evaluate_all()
    print(f"\nFIN ({time.ctime()})", flush=True)


if __name__ == "__main__":
    main()
