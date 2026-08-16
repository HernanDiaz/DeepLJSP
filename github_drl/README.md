# Deep Reinforcement Learning for the Interval Job Shop

Training and evaluation code for the article *Deep Reinforcement
Learning for the Interval Job Shop Scheduling Problem: A Comparison
with Genetic Programming Hyper-Heuristics across Inference Budgets*
(Hernán Díaz Rodríguez, University of Oviedo).

The policy is a size-invariant constructive dispatcher for the job
shop with interval processing times: dimensionless state features, a
Deep Sets encoder over the eligible-operation set, and PPO training.
One trained network applies to instances of any size.

## Layout

```
jobshop_rl/            the package
  agents_v2/           the policy and PPO trainer of the article
  data/                benchmark instance definitions
  environment/         the scheduling environment (interval semantics)
  heuristics/          dispatching-rule baselines and the evaluator of
                       evolved GP rules used in the comparison
  models/              interval arithmetic and schedule model
  rewards/             the shaped reward of Section 4.1
scripts/               training, evaluation and analysis entry points
paper_tools/
  make_figures.py      regenerates the article's figures
  verify_numbers.py    recomputes every number the article prints
```

## Install

```
python -m venv venv
venv/Scripts/pip install -r requirements.txt   # Windows
```

## Train and evaluate

Train the main arm (one seed) on the four training instances:

```
python scripts/run_benchmark.py --tier full --tag v2-full-1000ep --episodes 1000 --seeds 2
```

Evaluate a checkpoint on the validation set under the standalone
evaluator:

```
python scripts/eval_val_brazos.py --brazo v2-full-1000ep --semillas 2
```

## Data

Benchmark instances and the thirty evolved GP rules are published at
doi:10.5281/zenodo.21716972. The trained checkpoints and the primary
result files behind every table and figure of the article are in the
article's companion deposit (DOI in the article).

## License and citation

MIT (see LICENSE). If you use this code, please cite the article.
