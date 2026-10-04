"""
Equivalence test: the code in this deposit reproduces the deposited results.

Rules, instances and runs are re-derived from scratch with the ijsp_gp
package and compared against the result files shipped in ``results/``.
One or more results of every experiment of the article are re-derived:

 1. Per-rule RE and width on the 70 interval Taillard instances, against
    ``ablation_por_regla.csv`` and ``midpoint_control_por_regla.csv``.
 2. The featured rule on the 12 classical instances (``classic12_tuned.csv``).
 3. The featured rule's Monte Carlo eps_bar, K=1000 (``eps_por_regla.csv``).
 4. The G&T-MWKR baseline reproduces its reported mean RE (29.5).
 5. A smoke evolution runs end to end.
 6. The asymmetric benchmark is regenerated from the symmetric one and
    matches the deposited files, operation by operation.
 7. Rules of the training-set campaigns, on the 60 instances outside the
    training class (``training_sets/summary.json``).
 8. A rule of the asymmetric campaign, on the 70 asymmetric instances
    (``asymmetric/summary.json``).
 9. The featured rule as tie-break inside the Giffler-Thompson conflict
    set, and G&T-MWKR, on the fast simulator
    (``decoder_and_conventions.json``).
10. The budget curves of one instance: the rule, its sampled variant, the
    genetic algorithm, the seeded genetic algorithm and random search, on
    the schedule-construction axis (``budget/size_classes_curves.csv``).
11. The worked example and the census of 800 random 3x3 instances
    (``worked_example.json``).
12. The featured rule's conditional value-at-risk of the overrun beyond
    the predicted makespan, instance by instance
    (``tail_risk/per_instance.csv``).
13. The compiled rule of the budget comparison gives exactly the schedules
    of the reference dispatcher, deterministic and sampled.

Run from the ``code/`` directory:  python test_equivalence.py
"""

import csv
import filecmp
import json
import os
import random
import subprocess
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from ijsp_gp import (eps_bar_of_rule, evaluate_rule, lb_for_instance_name,
                     load_dir, load_rule)
from ijsp_gp.asymmetric import generate
from ijsp_gp.compiled_rule import compile_rule
from ijsp_gp.env import make_env
from ijsp_gp.ga import GRID, evolve, random_search
from ijsp_gp.heuristics import GTHeuristic, MWKRHeuristic, SPTHeuristic
from ijsp_gp.interval import Interval
from ijsp_gp.robustness import overrun_cvar_of_rule
from ijsp_gp.rules import GPRuleHeuristic
from ijsp_gp.simulate import (Instance, better, dispatch, gt_mwkr,
                              gt_policy, gt_tree, policy_from_tree)

PASS = FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f"  OK    {label} {detail}")
    else:
        FAIL += 1
        print(f"  FAIL  {label} {detail}")


def results(*parts):
    return os.path.join(ROOT, "results", *parts)


def load_json(*parts):
    with open(results(*parts), encoding="utf-8") as f:
        return json.load(f)


def rule_tree(rel):
    with open(os.path.join(ROOT, "rules", rel), encoding="utf-8") as f:
        return json.load(f)["tree"]


def re_of(cm, lb):
    return ((cm[0] + cm[1]) / 2 - lb) / lb * 100


def main():
    print("loading the 70 interval Taillard instances...")
    taillard = load_dir(os.path.join(ROOT, "instances", "interval_taillard"))
    assert len(taillard) == 70, f"expected 70 instances, got {len(taillard)}"

    # ------------------------------------------------------------------
    # 1. per-rule RE and width against the deposited CSVs
    # ------------------------------------------------------------------
    ablation = {}
    with open(results("ablation_por_regla.csv"), encoding="utf-8") as f:
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

    with open(results("midpoint_control_por_regla.csv"),
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
    with open(results("classic12_tuned.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            got = per_inst[row["inst"]]
            exp = float(row["gp"])
            check(f"classical {row['inst']}", abs(got - exp) <= 0.05 + 1e-9,
                  f"({got:.2f} vs {exp})")

    # ------------------------------------------------------------------
    # 3. Monte Carlo eps_bar of the featured rule
    # ------------------------------------------------------------------
    print("\n3. eps_bar of the featured rule (K=1000, ~1 minute)")
    with open(results("eps_por_regla.csv"), encoding="utf-8") as f:
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

    # ------------------------------------------------------------------
    # 6. the asymmetric benchmark, regenerated
    # ------------------------------------------------------------------
    print("\n6. asymmetric benchmark regenerated from the symmetric one")
    deposited = os.path.join(ROOT, "instances", "asymmetric_taillard")
    with tempfile.TemporaryDirectory() as tmp:
        written = generate(os.path.join(ROOT, "instances",
                                        "interval_taillard"), tmp)
        same = [n for n in written
                if filecmp.cmp(os.path.join(tmp, n + ".txt"),
                               os.path.join(deposited, n + ".txt"),
                               shallow=False)]
    check("asymmetric instances identical to the deposited ones",
          len(written) == 70 and len(same) == 70,
          f"({len(same)} of {len(written)})")

    # ------------------------------------------------------------------
    # 7. training-set campaigns on the 60 instances outside the 20x15 class
    # ------------------------------------------------------------------
    print("\n7. training-set campaigns, 60 instances outside the 20x15 class")
    outside = {k: v for k, v in taillard.items()
               if not k.startswith("int__tai20_15_")}
    ts = load_json("training_sets", "summary.json")["campanas"]
    for folder, key in (("TA11-TA12", "dos"), ("TA11-TA18", "ocho")):
        heuristic = load_rule(os.path.join(ROOT, "rules", "training_sets",
                                           folder, "seed1.json"))
        re_mean, _, _ = evaluate_rule(heuristic, outside)
        exp = ts[key]["por_semilla"]["1"]
        check(f"training set {folder}, seed 1: RE",
              round(re_mean, 4) == round(exp, 4),
              f"({re_mean:.4f} vs {exp:.4f})")

    # ------------------------------------------------------------------
    # 8. asymmetric campaign on the 70 asymmetric instances
    # ------------------------------------------------------------------
    print("\n8. asymmetric campaign, 70 asymmetric instances")
    asym = load_dir(deposited)
    assert len(asym) == 70, f"expected 70 instances, got {len(asym)}"
    arms = load_json("asymmetric", "summary.json")["ramas"]
    heuristic = load_rule(os.path.join(ROOT, "rules", "asymmetric",
                                       "robust_lambda1_full", "seed1.json"))
    re_mean, width_mean, _ = evaluate_rule(heuristic, asym)
    exp = arms["rob1"]["por_semilla"]["1"]
    check("asymmetric robust lambda=1, seed 1: RE",
          round(re_mean, 4) == round(exp["re"], 4),
          f"({re_mean:.4f} vs {exp['re']:.4f})")
    check("asymmetric robust lambda=1, seed 1: width",
          round(width_mean, 4) == round(exp["anchura"], 4),
          f"({width_mean:.4f} vs {exp['anchura']:.4f})")

    # ------------------------------------------------------------------
    # 9. decoder: the featured rule inside the conflict set
    # ------------------------------------------------------------------
    print("\n9. the featured rule inside the Giffler-Thompson conflict set")
    dec = load_json("decoder_and_conventions.json")["decodificador"]
    tree = rule_tree("main_arm/gp_tuned_seed1.json")
    names = sorted(taillard)
    insts = {n: Instance(taillard[n]) for n in names}
    lbs = {n: lb_for_instance_name(n) for n in names}

    def mean_re(policy):
        return float(np.mean([re_of(dispatch(insts[n], policy), lbs[n])
                              for n in names]))

    got = mean_re(gt_policy(gt_tree(tree)))
    exp = dec["gp_en_gt"]["destacada"]
    check("featured rule in the conflict set: RE",
          round(got, 4) == round(exp, 4), f"({got:.4f} vs {exp:.4f})")
    got = mean_re(gt_policy(gt_mwkr))
    exp = dec["gt_mwkr"]["media"]
    check("G&T-MWKR on the fast simulator: RE",
          round(got, 4) == round(exp, 4), f"({got:.4f} vs {exp:.4f})")
    got = mean_re(policy_from_tree(tree))
    exp = dec["gp_semiactivo"]["destacada"]
    check("featured rule, semi-active, on the fast simulator: RE",
          round(got, 4) == round(exp, 4), f"({got:.4f} vs {exp:.4f})")

    # ------------------------------------------------------------------
    # 10. budget curves of one instance, on the construction axis
    # ------------------------------------------------------------------
    print("\n10. budget curves of int__tai15_15_01, up to 4096 constructions")
    target = "int__tai15_15_01"
    curves = {}
    with open(results("budget", "size_classes_curves.csv"),
              encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["instancia"] == target:
                curves[(row["metodo"], int(row["semilla"]),
                        int(row["presupuesto"]))] = float(row["re"])
    inst, lb = insts[target], lbs[target]
    points = [p for p in GRID if p <= 4096]
    policy = policy_from_tree(tree)

    got = re_of(dispatch(inst, policy), lb)
    check("rule, one pass", round(got, 4) == curves[("regla", 0, 1)],
          f"({got:.4f})")

    cm0, perm = dispatch(inst, policy, return_order=True)
    rng, best, k, ok = random.Random(1), cm0, 1, True
    for p in [q for q in points if q <= 64]:
        while k < p:
            cm = dispatch(inst, policy, eps=0.1, rng=rng)
            k += 1
            if better(cm, best):
                best = cm
        ok &= round(re_of(best, lb), 4) == curves[("regla_bon", 1, p)]
    check("rule, best-of-N up to 64", ok)

    for label, key, run in (
            ("genetic algorithm", "ga",
             lambda: evolve(inst, points[-1], random.Random(1),
                            checkpoints=list(points))),
            ("seeded genetic algorithm", "ga_sembrado",
             lambda: evolve(inst, points[-1], random.Random(1),
                            seed_perm=perm, checkpoints=list(points))),
            ("random search", "azar",
             lambda: random_search(inst, points[-1], random.Random(1),
                                   list(points)))):
        curve, _ = run()
        bad = [p for p in points
               if round(re_of(curve[p][0], lb), 4) != curves[(key, 1, p)]]
        check(f"{label}, {len(points)} budget points", not bad,
              f"(mismatch at {bad})" if bad else "")

    # ------------------------------------------------------------------
    # 11. the worked example and its census
    # ------------------------------------------------------------------
    print("\n11. worked example and census of 800 random 3x3 instances")
    case = load_json("worked_example.json")

    def small_instance(seed, n_jobs=3, n_mach=3):
        r = np.random.default_rng(seed)
        seqs = [[int(x) for x in r.permutation(n_mach)]
                for _ in range(n_jobs)]
        durs = []
        for _ in range(n_jobs):
            row = []
            for _ in range(n_mach):
                p = int(r.integers(8, 31))
                d = int(r.integers(0, int(0.15 * p) + 1))
                row.append(Interval(p - d, p + d))
            durs.append(row)
        return {"num_jobs": n_jobs, "num_machines": n_mach,
                "problem_id": f"e3_{seed}", "sequences": seqs,
                "durations": durs}

    def traced(problem, heuristic):
        env = make_env(problem, seed=0)
        state, done, trace = env.reset(), False, []
        while not done and state["eligible_ops"]:
            f = env.get_features(state)
            a = min(heuristic.select_action(state["eligible_ops"], f),
                    len(state["eligible_ops"]) - 1)
            trace.append((tuple(state["eligible_ops"]), a))
            state, _, done, _ = env.step(a)
        c = env.job_completion_time
        lo = max(x.lower if isinstance(x, Interval) else x for x in c)
        up = max(x.upper if isinstance(x, Interval) else x for x in c)
        return trace, (lo, up)

    def divergences(t1, t2):
        d = []
        for k in range(min(len(t1), len(t2))):
            if t1[k][0] != t2[k][0]:
                break
            if t1[k][1] != t2[k][1]:
                d.append(k)
        return d

    beta0 = ["sub", ["sub", ["mul", "SLACK", "SLACK"],
                     ["sub", "WKR", ["add", "PT", "PT"]]], "ONE"]
    full_h, beta0_h = GPRuleHeuristic(tree), GPRuleHeuristic(beta0)

    problem = small_instance(300)
    for label, h, key in (("evolved rule", full_h, "gp"),
                          ("width term removed", beta0_h, "b0"),
                          ("SPT", SPTHeuristic(), "spt"),
                          ("MWKR", MWKRHeuristic(), "mwkr")):
        _, cm = traced(problem, h)
        exp = tuple(case["makespan"][key])
        check(f"worked example, {label}", tuple(cm) == exp,
              f"({list(cm)} vs {list(exp)})")

    census = {"n": 800, "igual": 0, "divergen": 0, "mejora": 0,
              "empeora": 0, "empata": 0}
    for seed in range(800):
        problem = small_instance(seed)
        t1, c1 = traced(problem, full_h)
        t2, c2 = traced(problem, beta0_h)
        if not divergences(t1, t2):
            census["igual"] += 1
            continue
        census["divergen"] += 1
        if better(c1, c2):
            census["mejora"] += 1
        elif better(c2, c1):
            census["empeora"] += 1
        else:
            census["empata"] += 1
    exp = {k: case["censo"][k] for k in census}
    check("census of 800 instances", census == exp,
          f"({census} vs {exp})")

    # ------------------------------------------------------------------
    # 12. tail risk: CVaR of the overrun of the featured rule
    # ------------------------------------------------------------------
    print("\n12. CVaR_0.95 of the overrun of the featured rule "
          "(K=1000, ~1 minute)")
    with open(results("tail_risk", "per_instance.csv"),
              encoding="utf-8") as f:
        exp_cvar = {row["instance"]: float(row["cvar95_over"])
                    for row in csv.DictReader(f)
                    if row["law"] == "uniform" and row["method"] == "GP"}
    # the tail-risk experiment seeded its realizations as the realization-
    # law one did, ten positions further on (see executed_makespans)
    got_cvar = overrun_cvar_of_rule(featured, taillard, K=1000,
                                    seed_offset=10)
    worst = max(abs(round(got_cvar[n], 4) - exp_cvar[n]) for n in exp_cvar)
    check("CVaR of the overrun, 70 instances",
          len(exp_cvar) == 70 and worst < 1e-3,
          f"(largest difference {worst:.1e})")

    # ------------------------------------------------------------------
    # 13. the compiled rule against the reference dispatcher
    # ------------------------------------------------------------------
    print("\n13. the compiled rule of the budget comparison")
    ok = True
    for rel in ("main_arm/gp_tuned_seed1.json", "main_arm/gp_tuned_seed2.json",
                "robust_lambda1_full/width_seed13.json"):
        tr = rule_tree(rel)
        fast, ref = compile_rule(tr), policy_from_tree(tr)
        for n in ("int__tai15_15_01", "int__tai30_20_05", "int__tai50_15_01"):
            ok &= fast(insts[n], return_order=True) == dispatch(
                insts[n], ref, return_order=True)
            r1, r2 = random.Random(7), random.Random(7)
            for _ in range(5):
                ok &= (fast(insts[n], return_order=True, eps=0.1, rng=r1)
                       == dispatch(insts[n], ref, return_order=True, eps=0.1,
                                   rng=r2))
            ok &= r1.getstate() == r2.getstate()
    check("same schedules, one pass and sampled, 3 rules x 3 instances", ok)

    print(f"\n{PASS} passed, {FAIL} failed")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
