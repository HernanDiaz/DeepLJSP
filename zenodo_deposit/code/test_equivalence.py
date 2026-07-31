"""
Equivalence test: the code in this deposit reproduces the deposited results.

Selected rules are re-evaluated from scratch with the ijsp_gp package and the
outcome is compared against the result CSV files shipped in ``results/``:

1. Per-rule RE and width on the 70 interval Taillard instances, against
   ``ablation_por_regla.csv`` (three rules from different arms) and
   ``midpoint_control_por_regla.csv`` (one rule), exact to the CSVs' four
   decimals.
2. The featured rule on the 12 classical instances, against the ``gp``
   column of ``classic12_tuned.csv``.
3. The featured rule's Monte Carlo eps_bar (K=1000, paired scenario seeds)
   against ``eps_por_regla.csv``, exact to four decimals.
4. The G&T-MWKR baseline reproduces its reported mean RE (29.5).
5. A smoke evolution (small population, two generations) runs end to end.

Run from the ``code/`` directory:  python test_equivalence.py
"""

import csv
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from ijsp_gp import evaluate_rule, eps_bar_of_rule, load_dir, load_rule
from ijsp_gp.heuristics import GTHeuristic

PASS = FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f"  OK    {label} {detail}")
    else:
        FAIL += 1
        print(f"  FAIL  {label} {detail}")


def main():
    print("loading the 70 interval Taillard instances...")
    taillard = load_dir(os.path.join(ROOT, "instances", "interval_taillard"))
    assert len(taillard) == 70, f"expected 70 instances, got {len(taillard)}"

    # ------------------------------------------------------------------
    # 1. per-rule RE and width against the deposited CSVs
    # ------------------------------------------------------------------
    ablation = {}
    with open(os.path.join(ROOT, "results", "ablation_por_regla.csv"),
              encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ablation[(row["objetivo"], row["terminales"],
                      row["seed"])] = (float(row["re"]), float(row["ancho"]))

    CASES = [
        ("main_arm/gp_tuned_seed1.json", ("makespan", "full", "1")),
        ("ablation_nowidth/nowidth_seed1.json", ("makespan", "nowidth", "1")),
        ("robust_lambda1_full/width_seed13.json", ("robust", "full", "13")),
    ]
    print("\n1. per-rule RE and width on the 70 interval instances")
    for rel, key in CASES:
        heuristic = load_rule(os.path.join(ROOT, "rules", rel))
        re_mean, width_mean, _ = evaluate_rule(heuristic, taillard)
        exp_re, exp_w = ablation[key]
        check(f"{rel}: RE", round(re_mean, 4) == exp_re,
              f"({re_mean:.4f} vs {exp_re})")
        check(f"{rel}: width", round(width_mean, 4) == exp_w,
              f"({width_mean:.4f} vs {exp_w})")

    with open(os.path.join(ROOT, "results",
                           "midpoint_control_por_regla.csv"),
              encoding="utf-8") as f:
        mid = {row["seed"]: (float(row["re"]), float(row["ancho"]))
               for row in csv.DictReader(f)}
    heuristic = load_rule(os.path.join(ROOT, "rules",
                                       "midpoint_control/mid_seed1.json"))
    re_mean, width_mean, _ = evaluate_rule(heuristic, taillard)
    check("midpoint_control/mid_seed1.json: RE",
          round(re_mean, 4) == mid["1"][0], f"({re_mean:.4f} vs {mid['1'][0]})")
    check("midpoint_control/mid_seed1.json: width",
          round(width_mean, 4) == mid["1"][1],
          f"({width_mean:.4f} vs {mid['1'][1]})")

    # ------------------------------------------------------------------
    # 2. featured rule on the 12 classical instances
    # ------------------------------------------------------------------
    print("\n2. featured rule on the 12 classical instances")
    classical = load_dir(os.path.join(ROOT, "instances",
                                      "interval_classical"))
    assert len(classical) == 12, f"expected 12 instances, got {len(classical)}"
    featured = load_rule(os.path.join(ROOT, "rules",
                                      "main_arm/gp_tuned_seed1.json"))
    _, _, rows = evaluate_rule(featured, classical)
    per_inst = {r["instance"]: r["re"] for r in rows}
    with open(os.path.join(ROOT, "results", "classic12_tuned.csv"),
              encoding="utf-8") as f:
        for row in csv.DictReader(f):
            got = per_inst[row["inst"]]
            exp = float(row["gp"])
            check(f"classical {row['inst']}", abs(got - exp) <= 0.05 + 1e-9,
                  f"({got:.2f} vs {exp})")

    # ------------------------------------------------------------------
    # 3. Monte Carlo eps_bar of the featured rule
    # ------------------------------------------------------------------
    print("\n3. eps_bar of the featured rule (K=1000, ~1 minute)")
    with open(os.path.join(ROOT, "results", "eps_por_regla.csv"),
              encoding="utf-8") as f:
        eps_rows = {(row["arm"], row["rule"]): float(row["eps_bar_x1000"])
                    for row in csv.DictReader(f)}
    exp_eps = eps_rows[("full", "gp_tuned_seed1.json")]
    got_eps = 1000 * eps_bar_of_rule(featured, taillard, K=1000)
    check("eps_bar featured", round(got_eps, 4) == exp_eps,
          f"({got_eps:.4f} vs {exp_eps})")

    # ------------------------------------------------------------------
    # 4. baseline sanity: G&T-MWKR mean RE
    # ------------------------------------------------------------------
    print("\n4. G&T-MWKR baseline")
    re_mean, _, _ = evaluate_rule(GTHeuristic(tiebreak="mwkr"), taillard)
    check("G&T-MWKR mean RE rounds to 29.5", round(re_mean, 1) == 29.5,
          f"({re_mean:.4f})")

    # ------------------------------------------------------------------
    # 5. smoke evolution
    # ------------------------------------------------------------------
    print("\n5. smoke evolution (pop 10, 2 generations, crisp training set)")
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "smoke_rule.json")
        result = subprocess.run(
            [sys.executable, "-m", "ijsp_gp.evolve",
             "--pop", "10", "--gens", "2", "--seed", "99",
             "--train", os.path.join(ROOT, "instances", "crisp_taillard"),
             "--out", out],
            cwd=HERE, capture_output=True, text=True)
        check("evolution completes", result.returncode == 0,
              result.stderr.strip().splitlines()[-1] if result.stderr else "")
        check("rule file written", os.path.exists(out))

    print(f"\n{PASS} passed, {FAIL} failed")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
