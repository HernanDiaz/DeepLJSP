# Genetic Programming Dispatching Rules for the Interval Job Shop: Data and Code

Companion deposit of the article *Genetic Programming Hyper-Heuristics for
the Job Shop Scheduling Problem with Interval Durations* (Hernán Díaz,
University of Oviedo). It contains every benchmark instance, every evolved
rule, the primary result files behind each table and figure of the article,
and a self-contained Python package that reproduces them.

Version 2.0 adds the material of the revised article: a right-skewed
version of the 70 Taillard instances; the rules evolved on five other
training sets and on the asymmetric instances; a fast simulator shared
by all methods of the budget comparison, the genetic algorithm of that
comparison and the compiled form of the evolved rule it uses; and the
results of the experiments on training-set sensitivity (kept here,
although the final article does not report it), asymmetric intervals, alternative realization laws, interval conventions and
decoders, the worked example, quality against computational budget, and
the tail risk (value-at-risk and conditional value-at-risk) of the
executed makespan.

## Contents

```
instances/
  interval_taillard/    the 70 interval Taillard instances (TA1-TA70)
  asymmetric_taillard/  their right-skewed versions (new in 2.0)
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
  training_sets/        150 rules, 30 per training set (new in 2.0)
  asymmetric/           60 rules, 15 per arm, on asymmetric intervals (new)
results/                the primary files behind the article's numbers
  irace/                scenario, parameter space and log of the configuration study
supplementary_material.pdf  the supplementary material of the article
code/
  ijsp_gp/              self-contained Python package (see below)
  test_equivalence.py   re-derives deposited results from scratch
  requirements.txt      numpy is the only dependency
```

In total the deposit holds 430 evolved rules: the 220 of version 1.0 and
the 210 of the campaigns added in version 2.0.

## Instance formats

Taillard-derived files: an optional `#` comment line, then `n m`, then `n`
rows with the machine sequence of each job, then `n` rows of durations,
written as `(lo,up)` pairs for interval instances and plain integers for
crisp instances. The classical files are kept verbatim in their original
formats (both are parsed by `ijsp_gp.instances.load_instance`). File names
of the classical set encode the generation parameters (`F0.15.0` = symmetric
±15% intervals around the original crisp durations).

The asymmetric instances (`int__ataiNN_MM_KK`) are generated from the
symmetric ones by `ijsp_gp.asymmetric`: the crisp duration is the midpoint
of the symmetric interval, and the bounds are `p - round(p*U[0,0.05])` and
`p + round(p*U[0,0.25])`, with a fixed seed per instance. Machine routes and
reference bounds are those of the symmetric version.

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
(`robustness.py`, which since 2.0 also returns the executed makespans
and their tail measures). Version 2.0 adds a fast simulator that dispatches with a
rule or decodes a permutation on the same semi-active scheme
(`simulate.py`), the genetic algorithm of the budget comparison (`ga.py`),
the evolved rule compiled into a single function and its sampled variant
stopped by time (`compiled_rule.py`), which are the implementations used
in that comparison, and the generator of the asymmetric instances
(`asymmetric.py`).

Quick start:

```
cd code
pip install -r requirements.txt
python test_equivalence.py
```

The test re-derives at least one result of every experiment of the
article: rules from several arms on the 70 interval instances and on the
12 classical ones, the Monte Carlo robustness of the featured rule, the
G&T-MWKR baseline, a small evolution end to end, the asymmetric instances
file by file, rules of the training-set and asymmetric campaigns, the
featured rule inside the Giffler-Thompson conflict set, the budget curves
of one instance for five methods, the worked example with its census
of 800 random instances, the conditional value-at-risk of the
featured rule instance by instance, and the compiled rule against the
reference dispatcher. Every recomputed figure is compared against the
deposited files, most of them to four decimals. It takes a few minutes.

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

Run the genetic algorithm on one instance for 30 seconds and print its
budget curve:

```
python -m ijsp_gp.ga --instance ../instances/interval_taillard/int__tai15_15_01.txt \
    --seconds 30 --seed 1
```

Regenerate the asymmetric instances:

```
python -m ijsp_gp.asymmetric --source ../instances/interval_taillard \
    --out asymmetric_taillard
```

## Map from the article to the result files

| Article element                                   | File in results/ |
|---------------------------------------------------|------------------|
| Main-arm per-instance RE                          | summary.csv |
| Evolution of the best rule (training, validation, test RE; size; widths) | evolution_best_rules.json |
| Selection of the featured rule on the development set | featured_rule_selection.json |
| Constructive baselines (RE column)                | all_baselines.csv |
| Per-instance RE (Supplementary Table S4)          | per_instance_baselines.csv; summary.csv, method gp_tuned_seed1 |
| Configuration study with irace (Section 5.3, Table 4) | irace/ |
| Timing (all times in the article)                 | timing.json |
| Generalization to the classical instances         | classic12_tuned.csv |
| Configuration of the genetic algorithm            | budget/ga_calibration_training.json |
| Quality against budget (Section 6.5, Figure 4, Supplementary Table S5) | budget/classical_curves.csv, budget/size_classes_curves.csv, budget/summary.json |
| Speed of the compiled rule                        | budget/compiled_rule_speed.json |
| Terminal usage and rule sizes                     | rule_anatomy.csv |
| Coefficient sensitivity sweep                     | coefficient_sweep.csv |
| Worked example and census                         | worked_example.json |
| Interval conventions and decoders                 | decoder_and_conventions.json |
| Terminal ablation and midpoint control            | ablation_por_regla.csv, midpoint_control_por_regla.csv |
| Contrasts between arms (Mann-Whitney, Holm)       | arm_contrasts.json |
| Lambda sweep, full arm                            | lambda_sweep_tuned.csv, lambda_por_regla.csv |
| Lambda sweep, no-width arm                        | lambda_nowidth_por_regla_completo.csv |
| Robustness table (per instance)                   | robustness_seis.csv |
| Representative rules of the robustness table      | representative_rules.json |
| Arm-level robustness                              | eps_por_regla.csv |
| Absolute deviation and other realization laws     | realization_laws/*.csv, realization_laws/summary.json |
| Tail risk (VaR and CVaR at 0.95)                  | tail_risk/per_instance.csv, tail_risk/summary.json |
| Sensitivity to the training set                   | training_sets/summary.json |
| Asymmetric intervals                              | asymmetric/summary.json, asymmetric/generation.json |

Some field names in the result files are in Spanish, as written by the
experiment scripts: `metodo` (method), `semilla` (seed), `instancia`
(instance), `presupuesto` (budget, in schedule constructions), `segundos`
(seconds), `horizonte` (time limit of the run), `ramas` (arms), `campanas`
(campaigns), `por_semilla` (per seed), `media` (mean), `anchura` / `ancho`
(relative width), `abs` (absolute deviation), `contrastes` (paired
contrasts), `destacada` (the featured rule), `censo` (census), `cruce`
(the budget from which one method stays below another), `semilla` (seed;
in `budget/summary.json`, the seeded against the unseeded genetic
algorithm). In the budget curves the methods are `regla` (the evolved
rule, one pass), `regla_bon` (its sampled best-of-N variant), `gt_mwkr`,
`azar` (random permutations), `ga` and `ga_sembrado` (the genetic
algorithm seeded with the rule's permutation). Every run is stopped by
time and records its incumbent solution each time the number of schedule
constructions grows by a factor of 2^(1/4), plus a final point:
`budget/classical_curves.csv` holds 30 runs of 900 s per instance and
method on the 12 classical instances, and `budget/size_classes_curves.csv`
3 runs per instance on the Taillard classes 15x15, 30x15 and 50x15, with
time limits of 900, 1800 and 3600 s (column `horizonte`).
`timing.json` holds the times of the baseline table, one constructive
pass per method on the 70 Taillard instances, with the evolved rules
compiled as in `compiled_rule.py` and every baseline written in the same
way (same schedules as the reference dispatchers), measured in six
simultaneous copies (`metodos`: methods; `brazo`: the 30 rules of the
main arm, `destacada` the featured one); `timing_tuned.csv` and
`timing_gp_arm.csv` are the version 1.0 times, measured on the slower
learning environment and no longer used. In
`tail_risk/per_instance.csv`, `law` is the realization law, `over` the
overrun `Cmax_ex - E[Cmax]`, `cvar95_*` and `var95_*` the conditional
value-at-risk and value-at-risk at 0.95, `re_cvar` the CVaR of the
executed makespan expressed as RE over the reference bound; `leyes`
(laws) and `reglas` (rules) in `summary.json`.

## Licenses

* Code (`code/`): MIT License, see `code/LICENSE`.
* Data (`instances/`, `rules/`, `results/`): Creative Commons Attribution
  4.0 International (CC BY 4.0), see `LICENSE-DATA`.

## Funding

Supported by the Spanish Ministry of Science, Innovation and Universities
(MCIN/AEI/10.13039/501100011033) under grant PID2022-141746OB-I00.
