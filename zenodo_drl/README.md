# Deep Reinforcement Learning for the Interval Job Shop: Checkpoints, Records and Code

Companion deposit of the article *Deep Reinforcement Learning for the
Interval Job Shop Scheduling Problem: A Comparison with Genetic
Programming Hyper-Heuristics across Inference Budgets* (Hernán Díaz
Rodríguez, University of Oviedo; Jesús Gil Ruiz, Universidad Europea
de Madrid). It contains the trained checkpoints,
the primary result files behind every table and figure of the article,
accepted and rejected experiment records alike, and the code that
produced and verifies them.

The thirty evolved GP rules the article compares against are
published in the companion GP deposit (doi:10.5281/zenodo.21716972);
from v3 on, the thirty rule files of the main arm are also mirrored
here under `rules/gp_main_arm/` so the shared evaluation can be rerun
from this deposit alone.

## Contents

```
instances/
  interval_taillard/    the 70 interval Taillard instances (TA1-TA70)
  interval_classical/   the 12 classical interval instances
  crisp_taillard/       crisp counterparts of the training instances
records/
  benchmarks/           primary CSV/JSON files of every campaign cited
                        by the article, quarantined files included
                        (CUARENTENA_* prefix marks data withdrawn for
                        cause, kept for the record)
  tuning/               irace campaign states, scenarios and the
                        target-runner scripts they invoke (Section 5.3)
rules/
  gp_main_arm/          the thirty GP rules of the shared evaluation
                        (mirrored from doi:10.5281/zenodo.21716972)
training_runs/
  bench_<arm>__<git>__<stamp>_seed<k>/
                        one folder per training run: final checkpoint
                        (best_model.pt), training logs, and the
                        schedules of the embedded evaluation
supplementary_material.pdf
                        the article's supplementary material (irace
                        campaigns, self-attention variant,
                        per-instance results)
code/
  jobshop_rl/           the training and evaluation package
  scripts/              evaluation, analysis and campaign scripts
  models/               exported checkpoints referenced by scripts
  paper/make_figures.py     regenerates every figure from records/
  paper/verify_numbers.py   recomputes every number the article prints
                            from the primary files in this deposit
  requirements.txt      pinned versions (Table 4 of the article)
```

## Reproducing the article's numbers

`code/paper/verify_numbers.py` re-derives each figure and statistic the
article prints from the files in `records/` and `training_runs/`, one
named check per claim. Run it from a checkout whose layout mirrors this
deposit (or adjust the base paths at the top of the script).

## Reproducing training

Training runs from `code/` with the pinned requirements. The entry
point is `scripts/run_benchmark.py`; the size-invariant agent the
article uses is selected with the environment variable
`DEEPLJSP_AGENT=v2`. One representative command per arm (Windows
syntax; on Linux replace `set` with `export`):

```
:: main arm (Section 5.4), thirty seeds in total
set DEEPLJSP_AGENT=v2
python scripts/run_benchmark.py --tier full --tag v2-full-1000ep --episodes 1000 --seeds 2,3,4,5,6

:: training-budget ladder (Table 6)
python scripts/run_benchmark.py --tier full --tag v2-full-100ep  --episodes 100  --seeds 2,3,4,5,6
python scripts/run_benchmark.py --tier full --tag v2-full-300ep  --episodes 300  --seeds 2,3,4,5,6

:: no-width ablation (Section 7.3): the encoder collapses each
:: interval to its worst case
set DEEPLJSP_V2_WORSTCASE_ONLY=1
python scripts/run_benchmark.py --tier full --tag v2-nowidth-1000ep --episodes 1000 --seeds 2,3,4

:: midpoint control (Section 7.3): crisp midpoint instances
python scripts/run_benchmark.py --tier midpoint --tag v2-midpoint-1000ep --episodes 1000 --seeds 2,3,4

:: width-penalized arms (Section 7.3), one value per run
set DEEPLJSP_V2_LAMBDA=0.5
python scripts/run_benchmark.py --tier full --tag v2-robust-lam0p5-fix --episodes 1000 --seeds 2,3,4
```

Two conventions of the trainer, both described in Section 5.4 of the
article, matter for reproduction: each block starts from the weights
of the best block so far, judged by the lowest best-episode makespan
in raw time units, and the serialized artifact of a run is the
network as it stands at the end of that best block (`best_model.pt`),
not the weights of the best individual episode. One caveat: the
`test_results.csv` that the batch pipeline writes at the end of a run
comes from `evaluate_on_test_set`, which restores the best-episode
snapshot instead; every table of the article uses the standalone
evaluators on `best_model.pt`, and so should any reproduction.

Two provenance notes. The reward weights the batch entry point
supplies are the ones Section 4.1 of the article prints (the
generator in `utils/problem_analyzer.py` is bypassed and unused). The
sampled GP arm is regenerated here rather than imported: the featured
rule of `rules/gp_main_arm/`, whose deterministic pass reproduces the
article's one-pass figure exactly, run under the deployed protocol of
Section 5.4 by `code/scripts/eval_gp_destacada_pool.py`, which writes
both endpoints of 1024 rollouts per instance to
`records/benchmarks/gp_destacada/`;
`code/scripts/analiza_gp_destacada.py` reads the budgets off them.
The deployed champion of the article (main arm, seed 5) is exported
as `code/models/v2_full_1000ep_seed5_deployed.pt`, byte-identical to
`best_model.pt` of its run folder.

## Arms and campaigns

- `v2-full-1000ep` (+ `-ext`, `-ext30-*`): the thirty training runs of
  the main arm. The policy the article reports is the run with the
  lowest mean validation RE (seed 5).
- `v2-full-100ep`, `v2-full-300ep` (+ `-ext`): the training-budget
  ladder of Table 6.
- `v2-nowidth-1000ep*`, `v2-midpoint-1000ep*`: the interval ablations
  of Section 7.3, ten seeds each.
- `v2-attn-300ep`, `v2-attn-1000ep*`: the self-attention variant
  (supplementary material).
- `v2-robust-lam*-fix`: the width-penalizing arms of Section 7.3,
  ten seeds each at lambda 0.5, 1, 2 and 4, and the runs the article
  reports. The `v2-robust-lam*` and `v2-robust-lam*-ext` folders are
  an earlier sweep of the same arms, kept as a record and not used by
  any reported figure.

## License and citation

Code under MIT; data under CC BY 4.0 (LICENSE files at the root).
Please cite the article and this deposit.

Version note: v1 preceded the ten-seed extension of the lambda sweep
and the ten-run budget-curve deposit; both are included from v2 on.
v3 adds the exported checkpoints under `code/models/`, the irace
target-runner scripts and the mirrored GP rules; the per-rollout
deposits behind the budget curve (`records/benchmarks/curva_intervalo/`),
the sampled GP arm (`gp_destacada/`, both endpoints of 1024 rollouts
per instance) and the width-penalizing arms (`robust_lambda_fix/`);
the forty `v2-robust-lam*-fix` training runs; and this reproduction
section.
The concept DOI always resolves to the latest version.
