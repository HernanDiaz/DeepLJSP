"""Transferencia del BRAZO COMPLETO a las 12 instancias clasicas.

eval_classic12.py evalua una sola regla (la destacada) e incluye el
best-of-{64,1024}, que es caro. Este script hace lo complementario: el pase
determinista unico de las 30 reglas del brazo, para poder reportar la
transferencia con media +- sd igual que se hace sobre Taillard, en vez de
depender de una sola regla.

Importa: sobre las clasicas la regla destacada de la campana por defecto
(seed27) era la n1 de 30 de su brazo, asi que su cifra no era representativa
del metodo. Esta es la comprobacion que lo detecta.

Salida: benchmarks/classic12_arm.csv (una fila por regla e instancia)
Uso: python scripts/classic12_arm.py [--pattern ...] [--out ...]
"""

import argparse
import csv
import glob
import json
import os
import re
import sys

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.experiments.factory import EnvironmentFactory      # noqa: E402
from jobshop_rl.heuristics.gp_rule import GPRuleHeuristic          # noqa: E402
from jobshop_rl.models.interval import Interval, final_makespan    # noqa: E402

DIR = r"E:\Experimentos\Selectos"
FILES = {
    "FT10": "F0.15.0.ft10_10.txt", "FT20": "F0.15.0.ft20_05.txt",
    "La21": "F0.15.0.la21_04.txt", "La24": "F0.15.0.la24_03.txt",
    "La25": "F0.15.0.la25_04.txt", "La27": "F0.15.0.la27_09.txt",
    "La29": "F0.15.0.la29_03.txt", "La38": "F0.15.0.la38_06.txt",
    "La40": "F0.15.0.la40_05.txt", "ABZ7": "F0.15.0.abz7_06.txt",
    "ABZ8": "F0.15.0.abz8_05.txt", "ABZ9": "F0.15.0.abz9_10.txt",
}
LB = {"ABZ7": 656, "ABZ8": 645, "ABZ9": 661, "FT10": 930, "FT20": 1165,
      "La21": 1046, "La24": 935, "La25": 977, "La27": 1235, "La29": 1152,
      "La38": 1196, "La40": 1222}


def load(path, name):
    lines = [ln.strip() for ln in open(path, encoding="utf-8",
                                       errors="replace") if ln.strip()]
    if "NUMERO DE TRABAJOS" in lines:
        i = lines.index("NUMERO DE TRABAJOS"); n = int(lines[i + 1])
        i = lines.index("NUMERO DE RECURSOS"); m = int(lines[i + 1])
        i = lines.index("SECUENCIA DE MAQUINAS"); sq = lines[i + 1:i + 1 + n]
        i = lines.index("DURACIONES"); du = lines[i + 1:i + 1 + n]
    else:
        n = int(lines[0]); m = int(lines[1])
        sq = lines[2:2 + n]; du = lines[2 + n:2 + 2 * n]
    return {"num_jobs": n, "num_machines": m, "problem_id": name,
            "sequences": [[int(x) for x in ln.split()] for ln in sq],
            "durations": [[Interval(int(a), int(b)) for a, b in
                           re.findall(r"\((\d+),\s*(\d+)\)", ln)]
                          for ln in du]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pattern",
                    default="benchmarks/reevo_fixedfit/gp_tuned_seed*.json")
    ap.add_argument("--out", default="benchmarks/classic12_arm.csv")
    args = ap.parse_args()

    probs = {k: load(f"{DIR}\\{v}", k) for k, v in FILES.items()}
    files = sorted(glob.glob(args.pattern))
    if not files:
        sys.exit(f"sin reglas en {args.pattern}")

    rows = []
    for p in files:
        tree = json.load(open(p, encoding="utf-8"))["tree"]
        h = GPRuleHeuristic(tree)
        for name, prob in probs.items():
            env = EnvironmentFactory.create_from_problem(prob, "basic", seed=0)
            st = env.reset(); done = False
            while not done and st["eligible_ops"]:
                f = env.get_features(st)
                a = min(h.select_action(st["eligible_ops"], f),
                        len(st["eligible_ops"]) - 1)
                st, _, done, _ = env.step(a)
            m = final_makespan(env.job_completion_time)
            mid = m.midpoint if isinstance(m, Interval) else float(m)
            rows.append({"rule": os.path.basename(p)[:-5], "inst": name,
                         "re": round((mid - LB[name]) / LB[name] * 100, 4)})
        print(".", end="", flush=True)
    print()

    with open(args.out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["rule", "inst", "re"])
        w.writeheader(); w.writerows(rows)

    per = {}
    for r in rows:
        per.setdefault(r["rule"], []).append(r["re"])
    means = {k: sum(v) / len(v) for k, v in per.items()}
    n = len(means); mu = sum(means.values()) / n
    sd = (sum((x - mu) ** 2 for x in means.values()) / (n - 1)) ** 0.5
    best = min(means, key=means.get)
    print(f"{n} reglas x 12 instancias -> {args.out}")
    print(f"brazo: {mu:.2f} ± {sd:.2f}   mejor {means[best]:.2f} ({best})")


if __name__ == "__main__":
    main()
