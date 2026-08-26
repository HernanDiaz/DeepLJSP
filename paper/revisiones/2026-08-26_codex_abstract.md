## Abstract

Production schedules must be committed when processing times are known only through bounds. We address interval job shop scheduling, for which leading methods repeat metaheuristic search for each instance. The artificial-intelligence contribution is a constructive deep reinforcement learning policy with dimensionless features and a permutation-invariant encoder, plus a controlled comparison with genetic programming hyper-heuristics and an analysis of how both use interval uncertainty; the engineering application is makespan-oriented production scheduling under bounded processing-time uncertainty. The size-invariant policy, trained on one size class, transfers without retraining. Thirty artifacts per family are evaluated together at matched schedule-count budgets. The selected policy outperforms every hand-crafted dispatching rule on all 70 benchmark instances, including six unseen size classes. Neither learned paradigm dominates: at one pass, the evolved rule achieves 17.71% mean relative error against the policy’s 18.49%; at 64 samples, the policy achieves 15.02% against 15.88%, retaining its lead at 1024. All three budget differences are statistically significant, although each policy rollout costs more. On 12 classical instances outside both training families, the policy has lower mean error at every budget, but not significantly at one pass. Ablations show that interval widths are inert as policy inputs under the default objective, whereas training on interval upper bounds improves sampled inference. When schedule width is penalized, the width–makespan trade-off arises from sample selection rather than measurably changed policy weights, unlike in the evolved rules. Thus the preferred learner depends on deployment budget and transfer regime, and both remain between hand-crafted dispatching and per-instance search. (249 words)

## What I changed and why

- Moved the engineering setting and the explicit artificial-intelligence/engineering distinction to the opening, satisfying the venue requirement more directly.
- Compressed the architecture description while retaining the dimensionless features, permutation invariance, size invariance, and zero-shot transfer.
- Replaced the rounded “0.8 points” comparison with the reported mean errors at one pass and 64 samples, while preserving the reversal at 1024.
- Added the higher per-rollout cost, preventing the sample-matched comparison from implying matched runtime.
- Qualified the classical-instance result: the policy leads in mean error at every budget, but the one-pass difference is not significant.
- Distinguished inert interval-width inputs from the measurable benefit of training on interval upper bounds during sampled inference.
- Reworded “weights unmoved” as “not measurably changed policy weights,” matching what the ablation establishes.
- Added the overall position between hand-crafted dispatching and per-instance search, which the current abstract omits.

## What I deliberately kept

- The contrast with per-instance metaheuristic search.
- The explicit identification of the artificial-intelligence contribution and engineering application.
- The controlled, thirty-artifact comparison at matched inference budgets.
- The result on all 70 benchmark instances and six unseen size classes.
- The central two-sided conclusion that the preferred learner changes with inference budget.
- The cross-family test on 12 classical instances.
- The contrast between sample-selection effects in the policy and representation-level effects in the evolved rules.

## Unsupported claims

The phrase “its weights unmoved” is stronger than the evidence. Retraining necessarily produces different numerical weights; the body establishes that the retrained policies are indistinguishable from the default policy under a common selection criterion, not that their weights literally remain unchanged. I found no other unsupported claim in the current abstract.