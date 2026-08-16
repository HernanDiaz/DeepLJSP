# Deep Reinforcement Learning for the Interval Job Shop: Checkpoints, Records and Code

Companion deposit of the article *Deep Reinforcement Learning for the
Interval Job Shop Scheduling Problem: A Comparison with Genetic
Programming Hyper-Heuristics across Inference Budgets* (Hernán Díaz
Rodríguez, University of Oviedo). It contains the trained checkpoints,
the primary result files behind every table and figure of the article,
accepted and rejected experiment records alike, and the code that
produced and verifies them.

The benchmark instances and the thirty evolved GP rules the article
compares against are published in the companion GP deposit
(doi:10.5281/zenodo.21716972) and are not duplicated here.

## Contents

```
records/
  benchmarks/           primary CSV/JSON files of every campaign cited
                        by the article, quarantined files included
                        (CUARENTENA_* prefix marks data withdrawn for
                        cause, kept for the record)
  tuning/               irace campaign states and scenarios (Section 5.3)
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
- `v2-robust-lam*`: the width-penalizing arms of Section 7.3
  (PENDIENTE: the extension of the lambda sweep to ten seeds trains as
  this skeleton is written; its runs, deposits and reanalysis JSONs
  will be added before the deposit is published).

## Code repository

The code is also maintained at https://github.com/HernanDiaz/ijsp-drl.

## License and citation

Code under MIT; data under CC BY 4.0 (LICENSE files at the root).
Please cite the article and this deposit.

Version note: v1 of this deposit precedes the ten-seed extension of
the lambda sweep; its runs, deposits and reanalysis files are added
in v2. The concept DOI always resolves to the latest version.
