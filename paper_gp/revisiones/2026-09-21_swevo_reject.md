# Swarm and Evolutionary Computation — rechazo (2026-09-21)

Ms. No. SWEVO-D-26-02115. *Genetic Programming Hyper-Heuristics for the
Job Shop Scheduling Problem with Interval Durations: Robustness-Aware
Interpretable Rules that Generalize Across Instance Sizes.*

Decisión del editor jefe: **rechazo**. Tres revisiones. Se transcriben
literalmente.

---

## Carta del editor

> Thank you for submitting your manuscript to Swarm and Evolutionary
> Computation. I regret to inform you that your manuscript does not reach
> the required quality standard of this journal and we must therefore
> reject it. Please refer to the comments listed at the end of this letter
> for details of why I reached this decision.

---

## Reviewer #1

This manuscript investigates the Interval Job Shop Scheduling Problem
(IJSP), where processing times are known only within intervals. The author
proposed a Genetic Programming (GP) hyper-heuristic to automatically design
priority dispatching rules. The terminal set is specifically enriched with
interval-aware attributes (both worst-case values and interval widths). The
evolved rules are deployed in a single constructive pass. Extensive
experiments were conducted to show the effectiveness of the proposed
method. Generally speaking, the idea of evolving interpretable,
robustness-aware rules for interval scheduling is interesting and the
resulting simplified rule (SLACK2 + 2PT − WKR − WKRW − 1) provides
reasonable practical interpretability. However, I have several concerns
regarding the experimental design, the consistency of the theoretical
claims, and the presentation of results. The comments are as follows:

1. The GP hyper-heuristic is trained exclusively on only four instances
   (TA11-TA14). While the authors justify this by demonstrating cross-size
   generalization. It remains unclear whether the performance of the
   featured rule is a result of general scheduling logic or an artifact of
   the specific numerical features of these four instances. So, the author
   should conduct a sensitivity analysis by training on alternative sets of
   four 20×15 instance or provide a cross-validation study across different
   training splits to demonstrate that the evolved rule's performance is
   stable regardless of which small subset is used for training.
2. The core advantage of Interval Scheduling is its "distribution-free"
   nature, which does not rely on any probability assumptions. However, in
   Section 7.4, the author introduced a Monte Carlo sampling procedure
   assuming a Uniform distribution over the intervals. So, the authors
   should explicitly clarify that the Uniform sampling is used exclusively
   as a post-hoc external oracle for measurement and does not influence the
   evolution or the core IJSP formulation.
3. The manuscript emphasized that the GP hyper-heuristic outperforms
   constructive baselines. However, the results in Table 6 show that
   specialized metaheuristics (e.g., ESABC) achieve a relative error of
   5.5%. This gap indicates that the evolved rule, while fast, is far from
   being a competitive solver for optimality. So, the authors should provide
   a deeper investigation into the underlying reasons for this performance
   gap. Additionally, the conclusions should be rephrased to more clearly
   frame this contribution as a "high-quality, interpretable fast-decision
   baseline" rather than a general solution to the IJSP.
4. The author should include a dedicated illustrative small-scale case
   study. This example should explicitly compare the evolved rule against
   classic baselines such as SPT and MWKR to show how their priority scores
   differ, and visually trace how the width terminal tilts the decision
   toward resolving uncertainty earlier. Such an illustration would bridge
   the gap between the mathematical expression and real-world scheduling
   practice.

---

## Reviewer #2

This paper introduces the first genetic programming (GP) hyper-heuristic
for the interval job shop scheduling problem (IJSP): priority rules are
evolved over an interval-aware terminal set (exposing both worst-case
values and interval widths), with fitness computed by interval arithmetic,
and deployed in a single constructive pass. Ablations show that
interval-width terminals do not improve expected makespan, but are decisive
for executional robustness (narrower predicted intervals, lower ε̄
deviation). GP hyper-heuristics for automated dispatching-rule design is a
classic evolutionary-computation topic; this paper extends it to interval
uncertainty, and engages SWEVO-relevant themes of interpretability,
robustness, and generalization.

### Strengths

1. Rigorous statistical methodology: 30 independent evolutions, paired
   Wilcoxon signed-rank tests (with z statistics, exact two-sided p-values,
   effect sizes |r|), and Holm correction; effect sizes are properly
   reported.
2. Honest problem framing: the authors explicitly report the negative
   result that interval awareness does not help expected makespan, and
   convert it into positive evidence for robustness; they also explicitly
   acknowledge that evolved rules cannot compete with per-instance
   search-based ABC metaheuristics and that GP-1024 is not faster than
   them. Such honesty is commendable.
3. Interpretability analysis: the featured rule simplifies to SLACK² + 2PT
   − WKR − WKRW − 1 with a per-term scheduling interpretation;
   terminal-usage statistics over 30 rules and weight-sensitivity sweeps
   (multi-modal landscape) are valuable.

### Major Comments

Contribution 3 in the title highlights "robustness-awareness," but
experiments show that the interval width feature has no statistical gain
under the default expected completion time objective, and only plays a role
under a robust customized objective that sacrifices expected completion
time. The authors need to supplement the actionable options for
decision-makers to choose the tradeoff coefficient λ and the applicable
boundaries of the interval feature's value, and rewrite Contribution 3 to
be consistent with experimental evidence.

The 70 Taillard examples only compare against the constructive baseline,
and the GA/ABC metaheuristics are only compared against 12 classic
examples, resulting in inconsistencies in programming languages,
computational budgets, and evaluation processes.

The model was trained using only four 20×15 examples, TA11-TA14, without
explaining the rationale for this subset and lacking a sensitivity analysis
of the training set size on generalization ability. A major overhaul must
include training set size sensitivity experiments to verify the reliability
of the "zero-shot generalization" conclusion.

The Python implementation of GP-1024 with multiple random sampling takes
37-134 seconds to run, which is not faster than metaheuristics. However,
the abstract and contributions section can mislead readers into believing
it is an efficient alternative. A major overhaul needs to clearly define
GP-best-of-N as merely an auxiliary tool for benchmarking sampling
algorithms, clarifying its connection to GRASP and multi-starting-point
search. Simultaneously, descriptions in the abstract that easily imply its
high efficiency advantage should be revised.

The benefits of interval awareness are built upon the goal of sacrificing
expected completion time. Under the default objective, GP rules
significantly lag behind iterative metaheuristics. Simply proposing the
first GP metaheuristic for IJSP is insufficient to meet the journal
publication threshold. The authors need to fully demonstrate, under what
scenarios, optimization objectives, and computational budgets, that this
method possesses quantifiable and clear advantages compared to existing
algorithms. The abstract, innovations, and conclusions should be rewritten
based on the demonstration results, and should not be limited to
comparisons with constructive scheduling rules.

---

## Reviewer #3

This paper investigates the interval job-shop scheduling problem (IJSP) and
proposes a genetic-programming hyper-heuristic to automatically evolve
dispatching rules. Interval-aware terminals are designed to generate
interpretable scheduling rules, followed by extensive numerical experiments
and ablation studies. but suffers from critical weaknesses regarding
algorithmic novelty, experimental fairness, mechanistic understanding and
conclusion generalizability. In its current form, it does not satisfy
journal publication criteria.

1. The featured rule is selected on all 70 instances, including the 60 test
   instances, which introduces test-set selection bias. Please select the
   rule using only the development set and report the mean standard
   deviation of the 30 rules as the primary result.
2. The robustness measure is normalized by E[Cmax], while the robust rule
   has a much higher RE; part of the reported improvement stems from the
   denominator effect and relies on the uniform-sampling assumption. Please
   report the absolute deviation, compare methods at similar RE levels, and
   add sensitivity experiments under non-uniform and worst-case
   realizations.
3. The interval handling of the baselines is not clearly described,
   interval-aware lexicographic baselines are missing, and the decoder
   difference between GP and G&T is not isolated. Please clarify the
   interval comparison rules used by each baseline, add explicit
   interval-aware baselines, and evaluate GP under the G&T decoder.
4. All instances are generated with symmetric intervals, and no rules are
   re-evolved under different interval widths or asymmetric intervals; the
   contribution of the width terminals may depend on this generation
   scheme. Please add experiments with asymmetric intervals to verify
   whether the robustness improvements are stable.
5. GP-best-of-1024 takes seconds, while GA and fEABC require only seconds;
   the comparison is not made under an equal computational budget, and the
   current wording understates this cost difference. Please report results
   under different budget settings or add a matched-budget comparison.
   *(El texto recibido viene con las cifras perdidas en los dos huecos.)*
6. The abstract states that interval information is of no value for the
   makespan objective, but this conclusion only holds under the current
   setting; moreover, the width terminals are heavily used, and weight
   optimization yields better performance. Please qualify the claim as
   "under the current setting" and soften the corresponding statement in
   the abstract.
