# Genetic Programming Dispatching Rules for the Interval Job Shop: Data and Code

Companion deposit of the article *Genetic Programming Hyper-Heuristics for
the Job Shop Scheduling Problem with Interval Durations: Robustness-Aware
Interpretable Rules that Generalize Across Instance Sizes* (Hernán Díaz,
University of Oviedo). It contains every benchmark instance, every evolved
rule, the primary result files behind each table and figure of the article,
and a self-contained Python package that reproduces them.

## Contents

```
instances/
  interval_taillard/    the 70 interval Taillard instances (TA1-TA70)
  crisp_taillard/       crisp counterparts of the four training instances
  interval_classical/   the 12 classical interval instances (FT, La, ABZ)
rules/
  main_arm/             30 rules, makespan objective, full terminal set
  ablation_nowidth/     30 rules, makespan objective, no width terminals
  robust_lambda1_full/  30 rules, robust objective (lambda=1), full set
  robust_lambda1_nowidth/  30 rules, robust objective, no width terminals
  lambda_sweep_full/    30 rules, robust objective, lambda in {0.5, 2, 4}
  lambda_sweep_nowidth/ 40 rules, same sweep plus lambda=0, no widths
  midpoint_control/     30 rules evolved on the crisp midpoint instances
results/                the primary CSV files behind the article's numbers
code/
  ijsp_gp/              self-contained Python package (see below)
  test_equivalence.py   reproduces deposited results from scratch
  requirements.txt      numpy is the only dependency
```

## Instance formats

Taillard-derived files: an optional `#` comment line, then `n m`, then `n`
rows with the machine sequence of each job, then `n` rows of durations,
written as `(lo,up)` pairs for interval instances and plain integers for
crisp instances. The classical files are kept verbatim in their original
formats (both are parsed by `ijsp_gp.instances.load_instance`). File names
of the classical set encode the generation parameters (`F0.15.0` = symmetric
±15% intervals around the original crisp durations).

Rule files are JSON: the expression tree (nested lists), its printable form,
the training fitness and the evolution parameters.

## The code

`ijsp_gp` implements: interval arithmetic with component-wise `max` and `+`
(`interval.py`), the semi-active decoder and the per-operation attribute
layout (`env.py`), the hand-crafted baselines including Giffler-Thompson
(`heuristics.py`), evolved-rule trees and their evaluation (`rules.py`),
instance loading and reference bounds (`instances.py`), deterministic
evaluation in RE and interval width (`evaluate.py`), the GP evolution
(`evolve.py`), and the Monte Carlo executional-robustness measure
(`robustness.py`).

Quick start:

```
cd code
pip install -r requirements.txt
python test_equivalence.py
```

The test re-evaluates rules from several arms on the 70 interval instances
and on the 12 classical instances, recomputes the Monte Carlo robustness of
the featured rule with the paired scenario seeds, checks the G&T-MWKR
baseline, and runs a small evolution end to end. Every recomputed figure is
compared against the deposited CSVs, most of them to four decimals.

Evaluate any rule set:

```
python -m ijsp_gp.evaluate --rules "../rules/main_arm/*.json" \
    --instances ../instances/interval_taillard
```

Evolve a new rule with the article's configuration:

```
python -m ijsp_gp.evolve --pop 100 --gens 50 --seed 1 \
    --tournament 7 --crossover 0.7695 --maxtree 30 --elitism 2 \
    --train ../instances/interval_taillard \
    --train-ids int__tai20_15_01,int__tai20_15_02,int__tai20_15_03,int__tai20_15_04 \
    --out my_rule.json
```

## Map from the article to the result files

| Article element                                   | File in results/ |
|---------------------------------------------------|------------------|
| Main-arm per-instance RE                          | summary.csv |
| Terminal ablation and midpoint control            | ablation_por_regla.csv, midpoint_control_por_regla.csv |
| Lambda sweep, full arm                            | lambda_sweep_tuned.csv, lambda_por_regla.csv |
| Lambda sweep, no-width arm                        | lambda_nowidth_por_regla_completo.csv |
| Robustness table (per instance)                   | robustness_seis.csv |
| Arm-level robustness                              | eps_por_regla.csv |
| Classical-instance transfer                       | classic12_tuned.csv |
| Coefficient sensitivity sweep                     | coefficient_sweep.csv |
| Terminal usage and rule sizes                     | rule_anatomy.csv |
| Timing                                            | timing_tuned.csv, timing_gp_arm.csv |

## Licenses

* Code (`code/`): MIT License, see `code/LICENSE`.
* Data (`instances/`, `rules/`, `results/`): Creative Commons Attribution
  4.0 International (CC BY 4.0), see `LICENSE-DATA`.

## Funding

Supported by the Spanish Ministry of Science, Innovation and Universities
(MCIN/AEI/10.13039/501100011033) under grant PID2022-141746OB-I00.
