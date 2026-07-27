"""
Evalúa las reglas GP sobre las 12 instancias clásicas del grupo (Selectos:
FT10/20, La21-40, ABZ7-9 en versión intervalo F0.15) y las posiciona frente a
los números PUBLICADOS de GA (IPMU'20), ABC_E3, fEABC y ESABC.

LBs del makespan esperado: los best-known reportados en Díaz et al. (2022),
tal como los reproduce la Tabla 2 del paper del fEABC (Natural Computing 2023).
Misma métrica RE = (E[Cmax]-LB)/LB*100.

Métodos propios: regla GP (mejor de la campaña de 30), MOR y GT-MWKR
deterministas, y GP-eps best-of-{64,1024}.

Salida: benchmarks/classic12.csv + tabla comparativa.
"""

import argparse
import json
import random
import re
import sys

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.experiments.factory import EnvironmentFactory
from jobshop_rl.heuristics.gp_rule import GPRuleHeuristic
from jobshop_rl.heuristics.strategies import MORHeuristic, GTHeuristic
from jobshop_rl.models.interval import Interval, final_makespan

DIR = r"E:\Experimentos\Selectos"
FILES = {
    "FT10": "F0.15.0.ft10_10.txt", "FT20": "F0.15.0.ft20_05.txt",
    "La21": "F0.15.0.la21_04.txt", "La24": "F0.15.0.la24_03.txt",
    "La25": "F0.15.0.la25_04.txt", "La27": "F0.15.0.la27_09.txt",
    "La29": "F0.15.0.la29_03.txt", "La38": "F0.15.0.la38_06.txt",
    "La40": "F0.15.0.la40_05.txt", "ABZ7": "F0.15.0.abz7_06.txt",
    "ABZ8": "F0.15.0.abz8_05.txt", "ABZ9": "F0.15.0.abz9_10.txt",
}
# LB del E[Cmax] (Diaz et al. 2022; Tabla 2 del fEABC)
LB = {"ABZ7": 656, "ABZ8": 645, "ABZ9": 661, "FT10": 930, "FT20": 1165,
      "La21": 1046, "La24": 935, "La25": 977, "La27": 1235, "La29": 1152,
      "La38": 1196, "La40": 1222}
# RE medio publicado (30 runs): GA (IPMU'20 via fEABC T2), ABC_E3, fEABC, ESABC
PUB_AVG = {
    "ABZ7": {"GA": 12.5, "ABCE3": 7.3, "fEABC": 6.6, "ESABC": 6.7},
    "ABZ8": {"GA": 18.5, "ABCE3": 12.1, "fEABC": 11.1, "ESABC": 10.9},
    "ABZ9": {"GA": 18.0, "ABCE3": 13.1, "fEABC": 11.6, "ESABC": 11.2},
    "FT10": {"GA": 5.2, "ABCE3": 4.1, "fEABC": 3.5, "ESABC": 3.0},
    "FT20": {"GA": 4.4, "ABCE3": 1.7, "fEABC": 1.8, "ESABC": 1.8},
    "La21": {"GA": 5.0, "ABCE3": 5.0, "fEABC": 4.2, "ESABC": 4.0},
    "La24": {"GA": 6.3, "ABCE3": 5.1, "fEABC": 4.9, "ESABC": 5.0},
    "La25": {"GA": 5.1, "ABCE3": 3.9, "fEABC": 3.4, "ESABC": 2.7},
    "La27": {"GA": 10.2, "ABCE3": 4.7, "fEABC": 4.6, "ESABC": 4.1},
    "La29": {"GA": 14.2, "ABCE3": 8.6, "fEABC": 7.4, "ESABC": 7.0},
    "La38": {"GA": 9.2, "ABCE3": 6.9, "fEABC": 6.1, "ESABC": 5.8},
    "La40": {"GA": 8.7, "ABCE3": 4.2, "fEABC": 4.6, "ESABC": 4.1},
}


def load_instance(path, name):
    lines = [ln.strip() for ln in open(path, encoding="utf-8", errors="replace")
             if ln.strip()]
    if "NUMERO DE TRABAJOS" in lines:          # formato FT (con cabeceras)
        i = lines.index("NUMERO DE TRABAJOS"); n = int(lines[i + 1])
        i = lines.index("NUMERO DE RECURSOS"); m = int(lines[i + 1])
        i = lines.index("SECUENCIA DE MAQUINAS")
        seq_lines = lines[i + 1:i + 1 + n]
        i = lines.index("DURACIONES")
        dur_lines = lines[i + 1:i + 1 + n]
    else:                                       # formato LA/ABZ (posicional)
        n = int(lines[0]); m = int(lines[1])
        seq_lines = lines[2:2 + n]
        dur_lines = lines[2 + n:2 + 2 * n]
    seqs = [[int(x) for x in ln.split()] for ln in seq_lines]
    durs = []
    for ln in dur_lines:
        row = [Interval(int(lo), int(up))
               for lo, up in re.findall(r"\((\d+),\s*(\d+)\)", ln)]
        durs.append(row)
    assert all(len(s) == m for s in seqs) and all(len(d) == m for d in durs), \
        f"{name}: shape mismatch"
    return {"num_jobs": n, "num_machines": m, "problem_id": name,
            "sequences": seqs, "durations": durs}


def rollout(env, h, rng=None, eps=0.0):
    st = env.reset()
    done = False
    while not done and st["eligible_ops"]:
        if rng is not None and rng.random() < eps:
            a = rng.randrange(len(st["eligible_ops"]))
        else:
            f = env.get_features(st)
            a = min(h.select_action(st["eligible_ops"], f),
                    len(st["eligible_ops"]) - 1)
        st, _, done, _ = env.step(a)
    m = final_makespan(env.job_completion_time)
    if isinstance(m, Interval):
        return float(m.lower), float(m.upper)
    return float(m), float(m)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rule",
                    default="benchmarks/reevo_fixedfit/gp_tuned_seed1.json",
                    help="regla destacada a evaluar")
    ap.add_argument("--out", default="benchmarks/classic12_tuned.csv",
                    help="salida; no se sobrescribe la de campanas previas")
    args = ap.parse_args()
    print(f"regla: {args.rule}", flush=True)

    gp = GPRuleHeuristic(json.load(open(args.rule, encoding="utf-8"))["tree"])
    mor, gt = MORHeuristic(), GTHeuristic(tiebreak="mwkr")

    rows = []
    for name, fname in FILES.items():
        prob = load_instance(f"{DIR}\\{fname}", name)
        lb = LB[name]

        def re_of(lo, up):
            return ((lo + up) / 2 - lb) / lb * 100

        env = EnvironmentFactory.create_from_problem(prob, "basic", seed=0)
        r_gp = re_of(*rollout(env, gp))
        env = EnvironmentFactory.create_from_problem(prob, "basic", seed=0)
        r_mor = re_of(*rollout(env, mor))
        env = EnvironmentFactory.create_from_problem(prob, "basic", seed=0)
        r_gt = re_of(*rollout(env, gt))

        # GP-eps best-of-N (seleccion lex por upper; RE por midpoint)
        rng = random.Random(1)
        best64 = best1024 = None
        for k in range(1024):
            env = EnvironmentFactory.create_from_problem(prob, "basic", seed=0)
            lo, up = rollout(env, gp, rng=(None if k == 0 else rng), eps=0.1)
            key = (up, lo)
            if best1024 is None or key < best1024[0]:
                best1024 = (key, re_of(lo, up))
            if k < 64 and (best64 is None or key < best64[0]):
                best64 = (key, re_of(lo, up))
        rows.append({"inst": name, "gp": r_gp, "mor": r_mor, "gt": r_gt,
                     "gp64": best64[1], "gp1024": best1024[1],
                     **PUB_AVG[name]})
        print(f"{name}: GP {r_gp:.1f} | bo1024 {best1024[1]:.1f}", flush=True)

    with open(args.out, "w", encoding="utf-8") as f:
        cols = ["inst", "mor", "gt", "gp", "gp64", "gp1024",
                "GA", "ABCE3", "fEABC", "ESABC"]
        f.write(",".join(cols) + "\n")
        for r in rows:
            f.write(",".join([r["inst"]] + [f"{r[c]:.2f}" for c in cols[1:]]) + "\n")

    print("\n=== 12 clasicas: RE (%) — propios vs publicados (avg 30 runs) ===")
    hdr = f"{'inst':<6}{'MOR':>7}{'GT':>7}{'GP':>7}{'GPe64':>8}{'GPe1024':>9}" \
          f"{'GA':>7}{'ABCE3':>8}{'fEABC':>8}{'ESABC':>8}"
    print(hdr)
    for r in rows:
        print(f"{r['inst']:<6}{r['mor']:>7.1f}{r['gt']:>7.1f}{r['gp']:>7.1f}"
              f"{r['gp64']:>8.1f}{r['gp1024']:>9.1f}{r['GA']:>7.1f}"
              f"{r['ABCE3']:>8.1f}{r['fEABC']:>8.1f}{r['ESABC']:>8.1f}")
    n = len(rows)
    print(f"{'MEDIA':<6}" + "".join(
        f"{sum(r[c] for r in rows)/n:>{w}.1f}"
        for c, w in [("mor", 7), ("gt", 7), ("gp", 7), ("gp64", 8),
                     ("gp1024", 9), ("GA", 7), ("ABCE3", 8),
                     ("fEABC", 8), ("ESABC", 8)]))
    print(f"\nCSV: {args.out}")


if __name__ == "__main__":
    main()
