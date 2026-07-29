"""Tiempo de un pase constructivo sobre las 12 instancias clasicas.

La afirmacion de 6.4 sobre el coste de un pase 'en instancias de este tamano'
se referia a las clasicas, pero solo se habian cronometrado las Taillard, que
son mayores. Esto mide las que la frase menciona.

Salida: benchmarks/timing_classic12.csv
"""

import argparse
import csv
import json
import os
import re
import sys
import time

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
REPEATS = 20      # instancias pequenas: mas repeticiones para estabilizar


def load(path, name):
    lines = [ln.strip() for ln in open(path, encoding="utf-8",
                                       errors="replace") if ln.strip()]
    if "NUMERO DE TRABAJOS" in lines:
        n = int(lines[lines.index("NUMERO DE TRABAJOS") + 1])
        m = int(lines[lines.index("NUMERO DE RECURSOS") + 1])
        i = lines.index("SECUENCIA DE MAQUINAS"); sq = lines[i + 1:i + 1 + n]
        i = lines.index("DURACIONES"); du = lines[i + 1:i + 1 + n]
    else:
        n, m = int(lines[0]), int(lines[1])
        sq = lines[2:2 + n]; du = lines[2 + n:2 + 2 * n]
    return {"num_jobs": n, "num_machines": m, "problem_id": name,
            "sequences": [[int(x) for x in ln.split()] for ln in sq],
            "durations": [[Interval(int(a), int(b)) for a, b in
                           re.findall(r"\((\d+),\s*(\d+)\)", ln)]
                          for ln in du]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rule",
                    default="benchmarks/reevo_fixedfit/gp_tuned_seed1.json")
    ap.add_argument("--out", default="benchmarks/timing_classic12.csv")
    args = ap.parse_args()
    if os.path.exists(args.out):
        sys.exit(f"{args.out} ya existe; borralo a mano para recalcular")

    h = GPRuleHeuristic(json.load(open(args.rule, encoding="utf-8"))["tree"])
    rows = []
    for name, f in FILES.items():
        prob = load(f"{DIR}\\{f}", name)
        t0 = time.perf_counter()
        for _ in range(REPEATS):
            env = EnvironmentFactory.create_from_problem(prob, "basic", seed=0)
            st = env.reset(); done = False
            while not done and st["eligible_ops"]:
                fe = env.get_features(st)
                a = min(h.select_action(st["eligible_ops"], fe),
                        len(st["eligible_ops"]) - 1)
                st, _, done, _ = env.step(a)
            final_makespan(env.job_completion_time)
        ms = (time.perf_counter() - t0) / REPEATS * 1000
        rows.append({"inst": name,
                     "size": f"{prob['num_jobs']}x{prob['num_machines']}",
                     "mean_ms": round(ms, 1)})
        print(f"{name:<6}{rows[-1]['size']:>8}{ms:>9.0f} ms", flush=True)

    with open(args.out, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["inst", "size", "mean_ms"])
        w.writeheader(); w.writerows(rows)

    v = [r["mean_ms"] for r in rows]
    print(f"\nmedia {sum(v)/len(v):.0f} ms, rango {min(v):.0f}-{max(v):.0f} ms"
          f"  -> {args.out}")


if __name__ == "__main__":
    main()
