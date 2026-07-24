"""
RE-EVOLUCIÓN con el fitness corregido (makespan componente a componente).

Contexto: las 6 evoluciones del paper_gp (3 default + 3 tuned) usaron como
fitness el midpoint bajo la convención vieja (lex-por-upper). Tras el fix,
evolve_gp_rule.py ya usa final_makespan. Este driver re-evoluciona los 6
seeds con el fitness corregido para verificar que las reglas resultantes son
equivalentes (y blindar el paper): si lo son, se mantienen las reglas
publicadas con su reevaluación corregida; si alguna mejora claramente, se
adopta.

Fases (auto-contenido, pensado para correr de noche):
  1. 6 evoluciones (pop 100, gens 50), máx. 3 procesos en paralelo
     (CPU-bound, 4 núcleos físicos; hilos BLAS ya limitados a 1 por proceso).
     Salidas en benchmarks/reevo_fixedfit/ (NO pisa los JSON publicados).
  2. Evaluación de cada regla nueva: rollout determinista en las 70 Taillard
     con el evaluador corregido -> summary.csv + VEREDICTO.md.

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
DEFAULT_CFG = []                                    # defaults del script
TUNED_CFG = ["--tournament", "7", "--crossover", "0.7695",
             "--maxtree", "30", "--elitism", "2"]   # ganadora irace #15
JOBS = ([("gp_rule_seed%d" % s, ["--seed", str(s)] + DEFAULT_CFG)
         for s in (1, 2, 3)] +
        [("gp_tuned_seed%d" % s, ["--seed", str(s)] + TUNED_CFG)
         for s in (1, 2, 3)])

# Referencia: reglas publicadas reevaluadas con la convención corregida
# (benchmarks/audit_gp_numbers.csv, 2026-07-24).
REF = {"gp_rule_seed1": 18.59, "gp_rule_seed2": 19.50, "gp_rule_seed3": 19.54,
       "gp_tuned_seed1": 18.49, "gp_tuned_seed2": 19.98, "gp_tuned_seed3": 17.71}


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

    lines = ["# Veredicto re-evolución con fitness corregido", "",
             "| Regla | Publicada (reevaluada) | Re-evolucionada | Δ |",
             "|---|---|---|---|"]
    for name, _ in JOBS:
        new = avg(name)
        ref = REF.get(name, float("nan"))
        lines.append(f"| {name} | {ref:.2f} | {new:.2f} | {new-ref:+.2f} |")
    news_d = [avg(f"gp_rule_seed{s}") for s in (1, 2, 3)]
    news_t = [avg(f"gp_tuned_seed{s}") for s in (1, 2, 3)]
    lines += ["",
              f"Default: best-of-3 {min(news_d):.2f} (ref 18.59), "
              f"media {sum(news_d)/3:.2f} (ref 19.21)",
              f"Tuned:   best-of-3 {min(news_t):.2f} (ref 17.71), "
              f"media {sum(news_t)/3:.2f} (ref 18.73)",
              "",
              "Regla de decisión (pre-registrada): si |Δ| del best-of-3 <= el",
              "spread entre seeds (~2 pts), las reglas publicadas se MANTIENEN",
              "(el fix no afecta materialmente a la evolución) y el paper usa",
              "su reevaluación corregida. Solo si la re-evolución mejora el",
              "best-of-3 en más de 2 pts se considera adoptar las nuevas."]
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
    print(f"[fase 1] 6 evoluciones, 3 en paralelo ({time.ctime()})", flush=True)
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
