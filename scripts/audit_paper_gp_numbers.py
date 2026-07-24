"""
AUDITORÍA post-fix del makespan para paper_gp: recalcula cada número del paper
que depende del midpoint y compara la convención VIEJA (lex-por-upper, la
usada cuando se generaron los números) con la NUEVA (componente a componente).

Cubre los números basados en rollout determinista:
  - Tabla gp70: RE por clase de las 3 reglas default (gp_rule_seed1..3)
  - Confirmación tuneada: gp_tuned_seed1..3 (17.67 / 18.68 en el paper)
  - Baselines: MOR (45.4) y GT-MWKR (29.4)

Método: un solo rollout por (regla, instancia); de env.job_completion_time se
derivan las DOS agregaciones -> delta exacto sin ambigüedad de seeds.

Salida: benchmarks/audit_gp_numbers.csv + resumen old/new por número del paper.
(Los números basados en pools —best-of-N, comparativa de generadores— se
auditan aparte re-ejecutando sus scripts sobre los pools corregidos.)
"""

import json
import re
import sys

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data import PROBLEM_REGISTRY
from jobshop_rl.data.literature_bounds import lb_for_problem_name
from jobshop_rl.experiments.factory import EnvironmentFactory
from jobshop_rl.heuristics.gp_rule import GPRuleHeuristic
from jobshop_rl.heuristics.strategies import MORHeuristic, GTHeuristic
from jobshop_rl.models.interval import Interval

INSTANCES = [p for p in sorted(PROBLEM_REGISTRY)
             if re.match(r"int__tai\d+_\d+_\d+$", p)]
CLASSES = ["15_15", "20_15", "20_20", "30_15", "30_20", "50_15", "50_20"]


def rollout_both(env, heuristic):
    """Un rollout determinista; devuelve (mid_viejo_lex, mid_nuevo_comp)."""
    state = env.reset()
    done = False
    while not done and state["eligible_ops"]:
        f = env.get_features(state)
        a = min(heuristic.select_action(state["eligible_ops"], f),
                len(state["eligible_ops"]) - 1)
        state, _, done, _ = env.step(a)
    comps = env.job_completion_time
    if isinstance(comps[0], Interval):
        old = max(comps)                       # lex por (upper, lower)
        old_mid = (old.lower + old.upper) / 2
        new_lo = max(c.lower for c in comps)   # componente a componente
        new_up = max(c.upper for c in comps)
        new_mid = (new_lo + new_up) / 2
        return old_mid, new_mid
    m = float(max(comps))
    return m, m


def load_rule(path):
    return GPRuleHeuristic(json.load(open(path, encoding="utf-8"))["tree"])


def main():
    methods = {
        "gp_seed1": lambda: load_rule("benchmarks/gp_rule_seed1.json"),
        "gp_seed2": lambda: load_rule("benchmarks/gp_rule_seed2.json"),
        "gp_seed3": lambda: load_rule("benchmarks/gp_rule_seed3.json"),
        "gp_tuned1": lambda: load_rule("benchmarks/gp_tuned_seed1.json"),
        "gp_tuned2": lambda: load_rule("benchmarks/gp_tuned_seed2.json"),
        "gp_tuned3": lambda: load_rule("benchmarks/gp_tuned_seed3.json"),
        "MOR": MORHeuristic,
        "GT-MWKR": lambda: GTHeuristic(tiebreak="mwkr"),
    }

    rows = []
    for name, mk in methods.items():
        h = mk()
        for pid in INSTANCES:
            lb = lb_for_problem_name(pid)
            if lb is None:
                continue
            env = EnvironmentFactory.create_from_problem(
                PROBLEM_REGISTRY[pid](), "basic", seed=0)
            old_mid, new_mid = rollout_both(env, h)
            cls = re.search(r"tai(\d+_\d+)", pid).group(1)
            rows.append({
                "method": name, "instance": pid, "cls": cls,
                "re_old": (old_mid - lb) / lb * 100,
                "re_new": (new_mid - lb) / lb * 100,
            })
        done_n = len([r for r in rows if r['method'] == name])
        print(f"{name}: {done_n} instancias", flush=True)

    with open("benchmarks/audit_gp_numbers.csv", "w", encoding="utf-8") as f:
        f.write("method,instance,cls,re_old,re_new\n")
        for r in rows:
            f.write(f"{r['method']},{r['instance']},{r['cls']},"
                    f"{r['re_old']:.4f},{r['re_new']:.4f}\n")

    def avg(meth, key, cls=None):
        v = [r[key] for r in rows if r["method"] == meth
             and (cls is None or r["cls"] == cls)]
        return sum(v) / len(v) if v else float("nan")

    print("\n=== GLOBAL (70 instancias): RE viejo -> nuevo (Δ) ===")
    for m in methods:
        o, n = avg(m, "re_old"), avg(m, "re_new")
        print(f"  {m:<10}: {o:6.2f}% -> {n:6.2f}%   (Δ {n-o:+.3f})")

    print("\n=== Por clase, reglas default (formato tabla gp70) ===")
    for m in ["gp_seed1", "gp_seed2", "gp_seed3"]:
        line_o = "  ".join(f"{avg(m, 're_old', c):5.1f}" for c in CLASSES)
        line_n = "  ".join(f"{avg(m, 're_new', c):5.1f}" for c in CLASSES)
        print(f"  {m} viejo: {line_o} | {avg(m, 're_old'):5.1f}")
        print(f"  {m} nuevo: {line_n} | {avg(m, 're_new'):5.1f}")

    print("\n=== Confirmación tuneada (paper: best 17.67, media 18.68) ===")
    news = [avg(f"gp_tuned{i}", "re_new") for i in (1, 2, 3)]
    olds = [avg(f"gp_tuned{i}", "re_old") for i in (1, 2, 3)]
    print(f"  viejo: best-of-3 {min(olds):.2f}  media {sum(olds)/3:.2f}")
    print(f"  nuevo: best-of-3 {min(news):.2f}  media {sum(news)/3:.2f}")
    news_d = [avg(f"gp_seed{i}", "re_new") for i in (1, 2, 3)]
    olds_d = [avg(f"gp_seed{i}", "re_old") for i in (1, 2, 3)]
    print(f"  default viejo: best {min(olds_d):.2f}  media {sum(olds_d)/3:.2f}")
    print(f"  default nuevo: best {min(news_d):.2f}  media {sum(news_d)/3:.2f}")

    print("\nCSV: benchmarks/audit_gp_numbers.csv")


if __name__ == "__main__":
    main()
