"""
CAMPAÑA DE 30+30 EVOLUCIONES con el fitness corregido (componente a comp.).

Doble objetivo:
  (a) Fitness corregido: las evoluciones del paper usaron el midpoint bajo
      la convención vieja (lex-por-upper); evolve_gp_rule.py ya está
      corregido.
  (b) Rigor estadístico: el estándar EC son 30 ejecuciones independientes
      con media±desviación (no 3). 30 seeds default + 30 tuned permiten
      además un test pareado (Wilcoxon signed-rank, mismos seeds) para la
      afirmación de tuning del paper.

Fases (auto-contenido, ~16 h evolución + ~3 h evaluación con 3 workers):
  1. 60 evoluciones (pop 100, gens 50), máx. 3 procesos en paralelo
     (CPU-bound, 4 núcleos físicos; hilos BLAS a 1 por proceso -> la
     máquina queda usable). Salidas en benchmarks/reevo_fixedfit/
     (NO pisa los JSON publicados).
  2. Evaluación de cada regla: rollout determinista en las 70 Taillard con
     el evaluador corregido -> summary.csv + VEREDICTO.md con media±std,
     mejor seed, y Wilcoxon pareado default-vs-tuned.

Uso:
  python scripts/rerun_evolutions_fixedfit.py          # todo
  python scripts/rerun_evolutions_fixedfit.py --dry    # solo listar comandos
"""

import csv
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

OUT_DIR = "benchmarks/reevo_fixedfit"
LOG_DIR = "logs/reevo"
PY = sys.executable

# (nombre, args extra de evolve_gp_rule.py)
N_SEEDS = 30                                        # estándar EC: 30 runs
DEFAULT_CFG = []                                    # defaults del script
TUNED_CFG = ["--tournament", "7", "--crossover", "0.7695",
             "--maxtree", "30", "--elitism", "2"]   # ganadora irace #15
JOBS = ([("gp_rule_seed%d" % s, ["--seed", str(s)] + DEFAULT_CFG)
         for s in range(1, N_SEEDS + 1)] +
        [("gp_tuned_seed%d" % s, ["--seed", str(s)] + TUNED_CFG)
         for s in range(1, N_SEEDS + 1)])


def run_one(name, extra):
    out_json = f"{OUT_DIR}/{name}.json"
    log = f"{LOG_DIR}/{name}.log"
    cmd = [PY, "scripts/evolve_gp_rule.py", "--out", out_json] + extra
    t0 = time.time()
    with open(log, "w", encoding="utf-8") as lf:
        r = subprocess.run(cmd, stdout=lf, stderr=subprocess.STDOUT,
                           cwd=".")
    mins = (time.time() - t0) / 60
    status = "OK" if r.returncode == 0 and os.path.exists(out_json) else "FALLO"
    print(f"[fase 1] {name}: {status} ({mins:.0f} min)", flush=True)
    return name, status


def evaluate_rules():
    from jobshop_rl.data import PROBLEM_REGISTRY
    from jobshop_rl.data.literature_bounds import lb_for_problem_name
    from jobshop_rl.experiments.factory import EnvironmentFactory
    from jobshop_rl.heuristics.gp_rule import GPRuleHeuristic
    from jobshop_rl.models.interval import Interval, final_makespan

    instances = [p for p in sorted(PROBLEM_REGISTRY)
                 if re.match(r"int__tai\d+_\d+_\d+$", p)]
    rows = []
    for name, _ in JOBS:
        path = f"{OUT_DIR}/{name}.json"
        if not os.path.exists(path):
            print(f"[fase 2] {name}: sin JSON, salto", flush=True)
            continue
        h = GPRuleHeuristic(json.load(open(path, encoding="utf-8"))["tree"])
        for pid in instances:
            lb = lb_for_problem_name(pid)
            if lb is None:
                continue
            env = EnvironmentFactory.create_from_problem(
                PROBLEM_REGISTRY[pid](), "basic", seed=0)
            state = env.reset()
            done = False
            while not done and state["eligible_ops"]:
                f = env.get_features(state)
                a = min(h.select_action(state["eligible_ops"], f),
                        len(state["eligible_ops"]) - 1)
                state, _, done, _ = env.step(a)
            m = final_makespan(env.job_completion_time)
            mid = m.midpoint if isinstance(m, Interval) else float(m)
            cls = re.search(r"tai(\d+_\d+)", pid).group(1)
            rows.append({"method": name, "instance": pid, "cls": cls,
                         "re": (mid - lb) / lb * 100})
        print(f"[fase 2] {name}: evaluada", flush=True)

    with open(f"{OUT_DIR}/summary.csv", "w", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["method", "instance", "cls", "re"])
        w.writeheader()
        w.writerows(rows)

    def avg(m):
        v = [r["re"] for r in rows if r["method"] == m]
        return sum(v) / len(v) if v else float("nan")

    def stats(vals):
        vals = [v for v in vals if v == v]
        n = len(vals)
        mu = sum(vals) / n
        sd = (sum((v - mu) ** 2 for v in vals) / (n - 1)) ** 0.5 if n > 1 else 0.0
        return mu, sd, min(vals), n

    def wilcoxon_signed(pairs):
        """Wilcoxon signed-rank pareado, aproximación normal. -> (W, z)."""
        diffs = [(a - b) for a, b in pairs if abs(a - b) > 1e-12]
        n = len(diffs)
        if n < 6:
            return float("nan"), float("nan")
        ranked = sorted(diffs, key=lambda d: abs(d))
        # rangos con empates promediados
        ranks = {}
        i = 0
        while i < n:
            j = i
            while j + 1 < n and abs(abs(ranked[j + 1]) - abs(ranked[i])) < 1e-12:
                j += 1
            r = (i + j) / 2 + 1
            for k in range(i, j + 1):
                ranks[id(ranked[k])] = r
            i = j + 1
        w_pos = sum(ranks[id(d)] for d in ranked if d > 0)
        mu_w = n * (n + 1) / 4
        sd_w = (n * (n + 1) * (2 * n + 1) / 24) ** 0.5
        z = (w_pos - mu_w) / sd_w if sd_w else float("nan")
        return w_pos, z

    seeds = range(1, N_SEEDS + 1)
    news_d = [avg(f"gp_rule_seed{s}") for s in seeds]
    news_t = [avg(f"gp_tuned_seed{s}") for s in seeds]
    mu_d, sd_d, best_d, n_d = stats(news_d)
    mu_t, sd_t, best_t, n_t = stats(news_t)
    pairs = [(d, t) for d, t in zip(news_d, news_t) if d == d and t == t]
    w, z = wilcoxon_signed(pairs)

    lines = ["# Veredicto campaña 30+30 con fitness corregido", "",
             f"| Config | n | media±std RE global | mejor seed |",
             "|---|---|---|---|",
             f"| default | {n_d} | {mu_d:.2f} ± {sd_d:.2f} | {best_d:.2f} |",
             f"| tuned (irace #15) | {n_t} | {mu_t:.2f} ± {sd_t:.2f} | {best_t:.2f} |",
             "",
             f"Wilcoxon signed-rank pareado (mismos seeds, n={len(pairs)}): "
             f"W+={w:.1f}, z={z:.2f} "
             f"(|z|>1.96 -> diferencia significativa al 5%)",
             "",
             "Referencia (3 seeds publicados, reevaluados con convención "
             "corregida): default best 18.59 / media 19.21; tuned best 17.71 "
             "/ media 18.73.",
             "",
             "Para el paper: reportar media±std sobre las 30 ejecuciones, el",
             "mejor individuo, y el test pareado para la afirmación de tuning.",
             "Los detalles por seed están en summary.csv."]
    text = "\n".join(lines)
    with open(f"{OUT_DIR}/VEREDICTO.md", "w", encoding="utf-8") as f:
        f.write(text + "\n")
    print("\n" + text, flush=True)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
    if "--dry" in sys.argv:
        for name, extra in JOBS:
            print("DRY:", " ".join(
                [PY, "scripts/evolve_gp_rule.py", "--out",
                 f"{OUT_DIR}/{name}.json"] + extra))
        return
    t0 = time.time()
    print(f"[fase 1] {len(JOBS)} evoluciones, 3 en paralelo ({time.ctime()})",
          flush=True)
    with ThreadPoolExecutor(max_workers=3) as ex:
        results = list(ex.map(lambda j: run_one(*j), JOBS))
    fails = [n for n, s in results if s != "OK"]
    if fails:
        print(f"[fase 1] FALLOS: {fails} — evalúo las que sí terminaron",
              flush=True)
    print(f"[fase 2] evaluación 70 instancias ({time.ctime()})", flush=True)
    evaluate_rules()
    print(f"\nTotal: {(time.time()-t0)/3600:.1f} h. "
          f"Resultados en {OUT_DIR}/ (VEREDICTO.md)", flush=True)


if __name__ == "__main__":
    main()
