# Revisión externa simulada, ronda 1

- **Fecha:** 13 de agosto de 2026
- **Manuscrito revisado:** `paper/main.pdf`, estado del commit `c238153`
  (41 páginas; tablas 8 y 9 todavía con la comparación asimétrica
  mejor-de-30 contra mejor-de-3, antes de la campaña de 30 semillas)
- **Prompt empleado:** `paper/prompt_revision_externa.md`
- **Revisor:** modelo externo, papel de revisor de *Journal of
  Intelligent Manufacturing*
- **Recomendación emitida:** Major revision. Confianza 5/5.

## Estado de las respuestas (13 de agosto de 2026)

Resueltas en el texto, cada una verificada antes contra los datos o el
código: mayores 3, 4, 5 (en lo que no exige medir), 6, 8, 9, 10 y 11;
menores 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 15 y 16.

La mayor 2, la pseudorreplicación, se resolvió rehaciendo el análisis
con la instancia como unidad (`scripts/reanalisis_por_instancia.py`,
commit b522a24). Las cuatro conclusiones sobreviven; los p-valores
suben y tres de ellos aterrizan en 0.031, que es el mínimo que admiten
seis instancias, y el texto lo dice.

Un hallazgo colateral que la revisión no vio y que apareció al
comprobar sus objeciones: un retorno de carro dentro de un `\ref` en la
sección 2 imprimía `ef{sec:arch}` en el PDF. Corregido, con
comprobación añadida al verificador.

Pendientes y su motivo:

- **Mayor 1 (simetría de la comparación con GP).** En curso: campaña de
  30 semillas del brazo principal, para comparar mejor de 30 contra
  mejor de 30. Su exigencia de que GP no se seleccione sobre las 70 no
  puede cumplirse, porque esa selección pertenece a un estudio ya
  publicado; se declara y se contrapone nuestra selección en
  validación.
- **Mayor 5 (coste en tiempo del brazo GP).** Requiere medir con la
  máquina libre, que ahora entrena. Encolado.
- **Mayor 7 y 12 (esquema de incertidumbre estrecho, relevancia
  industrial).** Atendidas parcialmente acotando afirmaciones; lo que
  queda son decisiones de alcance del trabajo.
- **Menores 10, 14, 17, 18, 19 y 20.** Editoriales o dependientes del
  DOI del preprint.

---

## 1. Summary of the submission

The manuscript proposes a constructive deep-reinforcement-learning policy
for the interval job shop scheduling problem (IJSP), with the stated goal
of amortizing the computational cost of per-instance metaheuristic search.
The policy uses dimensionless interval-derived features, a Deep Sets
encoder, and a PPO-trained policy/value network whose parameter count is
independent of the number of jobs and machines. Training is performed on
four $20\times15$ interval Taillard instances, with six additional
instances of the same size used for validation and the remaining Taillard
instances reserved from training and validation. The main experiments
compare the policy with classical dispatching rules, a previously
published genetic-programming (GP) dispatching rule, and published
per-instance metaheuristics, while additional experiments study
inference-budget scaling, self-attention, interval features, reward
objectives, and executional robustness. The headline result is that the
policy improves substantially over hand-crafted dispatching rules and, at
sufficiently large sampling budgets, can outperform the selected GP rule,
while remaining inferior to the strongest per-instance metaheuristic. The
manuscript further argues that interval width is largely irrelevant to the
learned decision function because the primary optimization criterion
depends only on upper endpoints, although training on interval rather than
midpoint data provides a measurable benefit. The manuscript therefore
establishes an interesting empirical result for this particular benchmark,
but several central claims about comparative superiority, statistical
significance, zero-shot generalization, and the practical value of the
proposed policy are not supported strongly enough by the current
experimental protocol.

## 2. Assessment

The paper establishes that a relatively small permutation-invariant PPO
policy can construct schedules for the particular symmetric-interval
Taillard benchmark and that, under the authors' inference protocol, it
substantially outperforms several classical dispatching rules and can
outperform the selected GP rule when both are allowed many stochastic
samples. It also provides useful evidence that the upper endpoints
dominate the stated optimization objective and that selection among
stochastic policy rollouts, rather than a change in the learned
representation, accounts for much of the reported width–makespan
trade-off. However, the paper does not yet establish a fair superiority
claim over the GP approach, nor does it provide statistically valid
evidence for several of its ablation claims because independent training
seeds are treated as if they were independent observations when the
underlying scheduling instances are repeated. The strongest "zero-shot"
claim is also overstated because one of the seven size classes contains
the training and validation instances. The manuscript's comparison with
published metaheuristics is appropriately described as a reference rather
than a head-to-head comparison, but the computational and statistical
comparison between the proposed method and constructive alternatives is
central enough that the GP asymmetry cannot remain merely acknowledged in
a footnote-like discussion. These issues are methodological rather than
cosmetic; they could be addressed by restructuring the evaluation and
statistical analysis, but doing so would require substantial additional
experiments and therefore constitutes a major-revision-level problem.

## 3. Major issues

### 1. The GP comparison is not a symmetric comparison of learned methods

Claim/passage — Section 4.2, "Baselines":

> The learned-symbolic baseline is the dispatching rule evolved by genetic
> programming for this same benchmark by \citet{DiazGP2026}, compared
> budget by budget in Section~\ref{sec:positioning}.

Results — Section 5.2:

> the $17.7\%$ rule is the best of 30 independent evolutions, selected on
> these same 70 instances, while the $19.4\%$ is a mean over the policy's
> three seeds.

This is the most important fairness problem in the manuscript. The
featured GP rule is the best artifact selected from 30 independent
evolutions using the same 70 instances on which its performance is
subsequently reported, whereas the neural policy is represented by the
mean of three training seeds. This is a classic selection/evaluation
asymmetry. The authors correctly acknowledge it, but acknowledging an
invalid or asymmetric comparison does not make the resulting superiority
claim valid.

The asymmetry is particularly consequential because the paper's main
conclusion about the two learning paradigms depends on it:

> the rule is better at a single pass, and the policy overtakes it when
> both draw $1024$ samples (Conclusions).

At one pass, the comparison is between a selected best-of-30 GP artifact
and a mean over three neural seeds. At 1024 samples, the comparison is
again between the selected GP artifact and the neural-policy aggregate.
Equalizing the number of inference rollouts does not equalize the upstream
selection procedure.

**What is required:** the authors should rerun the GP-vs-DRL comparison
under a genuinely symmetric protocol. At minimum:

1. Define a training/development set and a held-out test set for the GP
   evolution.
2. Do not select the GP rule using the final 70-instance test set.
3. Report the distribution of performance over independent GP evolutions,
   rather than only the selected best artifact.
4. Train multiple independent DRL policies under the same corresponding
   development protocol.
5. Evaluate both families on an untouched test set.
6. Report both mean performance and a clearly defined selection statistic,
   preferably with identical numbers of independent training artifacts or
   a pre-specified selection rule.
7. Retain the 1-pass/64/1024 inference-budget comparison, but explicitly
   separate training selection budget from inference budget.

The current comparison can remain as a comparison against the published GP
artifact, but it should not be used to support a claim that one learning
paradigm is superior to the other.

### 2. Several statistical tests pseudoreplicate training seeds

Claim/passage — Section 6.3, attention ablation:

> Across the eighteen instance--seed pairs it is $1.03$ points of RE
> inferior at $300$ episodes...

and:

> at $1000$ episodes the deficit is $1.06$ points over the sixty
> instance--seed pairs... ($p<0.001$).

The same issue occurs in the interval ablations:

> Ten seeds retrained from scratch reach $13.86\%$ mean RE against the
> ten-seed baseline's $13.82\%$... (Wilcoxon signed-rank, $p=0.93$).

and:

> the gap is $0.63$ points... ($p=0.045$).

The independent experimental unit for generalization to instances is the
instance, not the pair (instance, seed). Ten independently trained
policies evaluated on the same six instances do not produce 60 independent
observations. The seed variation is useful for quantifying training
stochasticity, but it cannot simply multiply the sample size for a paired
statistical test on instance-level generalization.

Consequently, the $p$-values reported for the attention and interval
ablations are overly optimistic if they were calculated over all
instance-seed pairs as implied by the manuscript. The manuscript itself
later recognizes this limitation:

> The $\lambda$-sweep arms and the rollout-deposit controls ... are run
> over three training seeds and compared pairwise on them...

but this does not resolve the problem for the previously reported tests.

**What is required:** redo the inferential analysis using the instance as
the independent unit. For example, aggregate the seed results per instance
before applying a paired test, or use an appropriate
hierarchical/mixed-effects model that explicitly separates instance and
seed variance. Report effect sizes and confidence intervals in addition to
$p$-values. For the six-instance validation set, the very small effective
sample size should be made explicit; exact Wilcoxon tests may be
appropriate, but the authors should not manufacture statistical power by
treating repeated seeds as independent instances.

This affects at least the attention ablation, the width-input ablation,
the midpoint-training ablation, and potentially the robust-objective
comparisons.

### 3. The "zero-shot on all seven size classes" claim is overstated

Claim — Abstract:

> surpasses every such rule zero-shot on all seven size classes of the
> 70-instance benchmark.

Section 5.2:

> The size-invariant design allows direct evaluation of the
> $20{\times}15$-trained network on any class. Evaluation is zero-shot...

But the $20\times15$ class contains TA11--TA14 as training instances and
TA15--TA20 as validation instances:

> the final model is trained on four, TA11--TA14 of the $20{\times}15$
> class. Six more of the same class, TA15--TA20, form the validation
> set...

Therefore the $20\times15$ size class itself was not unseen. The model was
trained on four instances from that class and repeatedly evaluated on six
others during design and configuration. Calling the complete seven-class
evaluation "zero-shot" is technically inaccurate.

There is a legitimate and interesting claim here: the model transfers to
unseen instances of the training size and to six completely unseen size
classes. That should be stated instead.

**What is required:** replace "zero-shot on all seven size classes" with a
precise distinction between:

- unseen instances within the training size class;
- completely unseen size classes;
- the 60-instance held-out Taillard test set.

If the authors want to claim zero-shot generalization to the entire
benchmark, they need an experimental protocol in which the whole benchmark
is excluded from model selection, which is incompatible with the current
validation procedure.

### 4. The abstract contains a direct internal inconsistency concerning the best hand-crafted rule

The abstract states:

> it attains $13.8\%$ mean relative error ... compared with ${\approx}46\%$
> for the best hand-crafted dispatching rule

However, Table 2 reports G&T-MWKR at 27.9% on the six validation
instances, whereas the approximately 46% figure corresponds to plain rules
such as MOR/EST. The paper itself later distinguishes these:

> 13.8% versus $27.9\%$ for G&T-MWKR and ${\approx}46\%$ for the best
> plain rule.

Thus "best hand-crafted dispatching rule" in the abstract is incorrect.
G&T-MWKR is a hand-crafted dispatching-rule-based constructive method and
is substantially stronger.

This is not merely wording: the abstract currently exaggerates the
apparent improvement by comparing against a weaker baseline than the
strongest hand-crafted baseline used in the paper.

**What is required:** correct the abstract and any other occurrence of
"best hand-crafted rule" when it refers to approximately 46%. If the
intended distinction is "best plain priority rule excluding
Giffler--Thompson," state that explicitly.

### 5. The comparison between GP and policy does not fully equalize inference cost

The manuscript repeatedly frames the comparison as matched inference
budgets:

> With $1024$ samples each, the GP rule ... provides for this purpose, the
> ordering reverses...

Equal numbers of rollouts do not necessarily imply equal inference budgets
in computational terms. The DRL policy requires neural forward passes and
the GP rule evaluates an evolved expression. More importantly, the GP's
stochastic mechanism is an $\epsilon$-greedy dispatching procedure
imported from another study, whereas the policy samples from a learned
categorical distribution.

The paper gives wall-clock cost for policy rollouts:

> a sampled rollout requires $1.03$ s on a $20{\times}15$ instance and
> $6.4$ s on a $50{\times}20$ one...

but does not provide corresponding GP timing. Consequently, the practical
statement that the methods are compared at matched inference budgets is
only true in number of rollouts, not in computational budget.

**What is required:** report per-rollout wall-clock time and total
wall-clock time for GP and DRL on the same hardware and implementation
harness. Add a comparison at matched computational time as well as matched
rollout count. If the GP implementation cannot be reproduced on the same
machine, report that limitation explicitly and avoid describing the
comparison as fully budget-matched.

### 6. The training protocol is vulnerable to instance-order effects and is insufficiently specified

The paper states:

> Training on a set of instances proceeds in blocks, one instance at a
> time, with the weights carried over from each block to the next.

This is effectively a curriculum/order-dependent training procedure. With
only four training instances, the order in which TA11--TA14 are presented
can materially affect the final parameters. Random seeds do not
necessarily address this if the instance order is fixed.

The paper does not specify whether the order of the four training
instances is randomized between seeds, whether each instance receives
exactly the same number of updates, or whether the training-budget
experiments restart independently from scratch for each budget.

**What is required:** state the exact training-instance order and whether
it is randomized. Report a sensitivity experiment over multiple instance
permutations, or randomize the order within training and repeat the
experiment. Clarify precisely how the 100/300/1000 episode budgets are
generated and whether models at different budgets share training
trajectories.

### 7. The strongest generalization claim is based on a very narrow uncertainty distribution

The benchmark uses:

> each crisp duration replaced by an integer interval symmetric around it,
> with half-width drawn uniformly up to $15\%$ of the original value

The manuscript correctly acknowledges asymmetric and heterogeneous
uncertainty as a limitation:

> asymmetric intervals, and distributions in which the uncertainty varies
> sharply from one operation to another, would separate the worst-case and
> expected-value criteria far more than they do here, and no policy was
> trained under them.

This limitation is particularly important because much of the paper's
interpretation of "interval awareness" follows directly from the special
symmetric construction. The claim that interval widths are inert is
mathematically valid for the specific primary objective defined here, but
it should not be generalized to interval scheduling more broadly. In more
general uncertainty structures, width, asymmetry, or dependence could
become decision-relevant under alternative objectives.

**What is required:** either substantially narrow the claims throughout
the abstract/introduction/conclusions, or add experiments with at least
asymmetric interval widths and heterogeneous uncertainty magnitudes. The
former is the minimum requirement; the latter would materially strengthen
the paper.

### 8. The claim of "size invariance" exceeds what is demonstrated experimentally

The manuscript states:

> one parameter set covers any instance size (Abstract)

and describes the architecture as:

> no dimension of which depends on $n$ or $m$.

The latter is an architectural fact. The former is an empirical
generalization claim. The experiments cover seven Taillard size classes,
with maximum size $50\times20$, plus the listed classical instances. This
does not establish that the policy is generally invariant to arbitrary
instance sizes.

Moreover, the feature definitions contain explicit size-dependent
normalizations such as $k/m$ and $|\mathcal E|/n$, and the empirical
transfer is confined to a relatively narrow family of classical JSP
structures.

**What is required:** distinguish clearly between size-agnostic
architecture and empirically demonstrated size generalization. The latter
should be stated as "generalizes across the tested Taillard sizes" rather
than "covers any instance size." If size invariance is intended as a
central scientific contribution, an additional extrapolation experiment
outside the observed size range would be appropriate.

### 9. The benchmark contains only one uncertainty-generation mechanism, making the robustness conclusions narrow

The policy is trained and evaluated on the same $\pm15\%$ symmetric
interval construction. The classical benchmark is generated using the same
scheme:

> generated with the same symmetric scheme ... reserved for the
> cross-family evaluation.

Consequently, the second benchmark is independent in job-shop instance
family but not independent in uncertainty-generation mechanism. Calling it
a broad "cross-family generalization test" is therefore reasonable only
for the crisp-instance family, not for uncertainty structure.

**What is required:** make this distinction explicit and avoid implying
that the method has been tested under independent uncertainty regimes. A
stronger revision would include at least one uncertainty-generation
mechanism not derived by applying symmetric perturbations to a crisp
benchmark.

### 10. The paper's executional-robustness analysis does not establish deployment reliability in a manufacturing sense

The manuscript defines execution by independently uniform draws inside
each interval:

> durations drawn independently and uniformly within their intervals.

This is a legitimate Monte Carlo experiment, but the conclusion uses
broader deployment language:

> supporting deployment where schedules must be fast and dependable.

The interval model deliberately makes no distributional assumption, while
the execution experiment introduces a uniform independent distribution.
This is fine for an illustrative experiment, but it does not establish
real-world execution reliability. In manufacturing, processing-time
uncertainty can be correlated, biased, time-varying, machine-dependent, or
non-uniform.

**What is required:** restrict the claim to "under the assumed
independent-uniform realization model." Alternatively, test multiple
realization distributions, including biased and correlated scenarios, and
report whether the ranking persists.

### 11. The practical comparison with fEABC is incomplete and risks an apples-to-oranges interpretation

The paper reports:

> fEABC (30 runs) ... 9.4%

while explicitly stating that these are published results rather than
reruns:

> Their figures are quoted from those papers, not re-run here.

This is acceptable as historical context, but the paper repeatedly uses
the resulting ranking to characterize its practical position. The methods
have different hardware, implementation, stopping conditions, run counts,
and potentially implementation details. The paper itself calls the
comparison a "reference yardstick," which is appropriate.

However, the conclusion says:

> The per-instance metaheuristics retain the lead in solution quality
> ($9.4\%$ mean RE for fEABC against $13.0\%$ for the policy at its
> largest budget)

without sufficiently emphasizing that this is not a controlled experiment.

**What is required:** consistently label these as published reference
results and do not use them to support claims of computational superiority
or practical speed superiority. If the authors want to compare solution
quality only, that is defensible; if they want to compare the quality/time
trade-off, the metaheuristics must be rerun under a common computational
protocol.

### 12. The contribution is not yet sufficiently connected to intelligent manufacturing practice

The paper is technically a scheduling-method paper, but its industrial
relevance is mostly asserted through generic statements about uncertain
processing times and deployment speed. There is no manufacturing-specific
scenario, decision latency requirement, machine environment,
production-control integration, or demonstration of how a plant operator
would use the predicted interval.

For a *Journal of Intelligent Manufacturing* submission, the paper needs a
clearer answer to what operational decision the method improves beyond
benchmark RE.

**What is required:** either add a concrete manufacturing
interpretation—e.g., how interval predictions are obtained, when the
policy would be invoked, what latency is acceptable, and how a
practitioner would choose between the default and width-penalizing
objective—or reduce the manufacturing claims and position the paper
explicitly as an intelligent scheduling methodology evaluated on standard
benchmarks.

## 4. Minor issues

1. **Abstract terminology.** Replace "best hand-crafted dispatching rule"
   at approximately 46% with "best plain dispatching rule" or report the
   actual G&T-MWKR value of 27.9%.
2. **"Zero-shot" should be used consistently.** The $20\times15$ class was
   seen during training; only the individual validation/test instances
   within that class are unseen.
3. **Best vs mean values.** Several tables report `mean [best]`. The
   distinction is useful, but the paper should consistently identify
   whether "best" means best seed, best rollout, or best independent run.
4. **Table 2 caption.** The standard deviation column is described as
   "standard deviation across the ten per-seed means over the six
   instances." This is unusual and should be defined mathematically.
5. **Statistical reporting.** Report confidence intervals/effect sizes
   alongside $p$-values rather than relying almost exclusively on
   significance testing.
6. **Multiple comparisons.** Numerous ablations and pairwise tests are
   reported without discussion of multiplicity. Either pre-specify primary
   tests or state that the reported $p$-values are exploratory.
7. **Reward specification.** The load-balance scale is described as "a
   scale set to the dispersion expected for the instance" without a
   precise formula. This is insufficient for reproduction.
8. **Division by interval midpoints.** The feature definitions should
   state how zero midpoints are handled, even if the benchmark cannot
   produce them.
9. **Feature definition ambiguity.** "remaining job work interval of the
   job after $o$" should be made explicit about whether the current
   operation itself is excluded.
10. **Attention parameter count.** The paper should explain how the stated
    132,480 parameters per attention block were calculated, since this is
    central to the computational-cost argument.
11. **Wall-clock methodology.** State whether reported times include
    schedule evaluation, environment transition, Python overhead, and
    sampling but exclude model-loading time.
12. **Training hardware wording.** The manuscript says every number was
    produced on CPU but subsequently states that the GPU was used for the
    tuning campaign. This should be phrased as "all reported
    training/evaluation results except the specified batched tuning
    experiments."
13. **Operating system.** Windows 10 and the precise library versions are
    useful for reproducibility, but CPU thread settings and BLAS
    implementation are also relevant to the reported timing.
14. **Figures should expose uncertainty.** Where distributions over
    instances are shown, numerical sample sizes and whether the displayed
    values are instance-level or seed-level should be explicit in the
    captions.
15. The statement "any permutation-invariant function ... admits this
    form" is mathematically stronger than necessary and potentially
    misleading in the finite-width implementation. It would be clearer to
    distinguish the Deep Sets representation theorem from the capacity of
    the particular finite MLP used.
16. "The strongest constructive baseline available" is too categorical
    unless the authors can substantiate the completeness of the literature
    search.
17. **Related-work positioning.** The manuscript would benefit from a
    table explicitly comparing the proposed method with representative
    deterministic JSP-DRL, stochastic JSP-DRL, fuzzy JSP, GP
    hyper-heuristics, and IJSP metaheuristics in terms of uncertainty
    model, architecture, training regime, inference budget, and
    generalization protocol.
18. **Data/code availability.** The statement says code and experiment
    records "will be deposited openly upon submission" but leaves a TODO
    for the DOI. For a reproducibility-oriented paper, the final
    submission should provide a persistent identifier rather than a future
    commitment.
19. **English.** The prose is generally understandable, but some sentences
    are unnecessarily argumentative, particularly those explaining why
    particular findings "therefore" establish mechanisms. These should be
    softened where the evidence is observational.
20. **Conclusions.** The conclusion currently mixes established results,
    interpretation, and proposed future experiments. The distinction
    should be made more explicit.

## 5. Questions to the authors

1. Was the GP rule selected using the same 70 Taillard instances on which
   its final performance is reported, including the test instances
   TA21--TA70?
2. For the GP study, what exactly constitutes one "sample" at inference
   time, and what is its wall-clock cost relative to one DRL rollout?
3. Were the four training instances always presented in the order TA11,
   TA12, TA13, TA14? If so, was sensitivity to that order tested?
4. For the 100-, 300-, and 1000-episode experiments, were separate models
   trained from scratch, or are they checkpoints of the same training
   trajectories?
5. How exactly was the final PPO checkpoint selected? Was checkpoint
   selection ever influenced by validation performance, directly or
   indirectly?
6. In the ten-seed experiments, what are the actual independent random
   seeds, and were environment randomness, network initialization, PPO
   minibatch ordering, and sampling all controlled by them?
7. Were the Wilcoxon tests on 60 or 18 instance-seed pairs actually
   computed treating all pairs as independent observations? If so, the
   statistical analysis needs to be redone.
8. For the GP rule, why are 30 evolved artifacts available for the
   classical benchmark but only one featured rule used in the Taillard
   comparison? Can the complete distribution of GP runs be supplied?
9. For the 1024-sample GP comparison, are the $\epsilon$-greedy parameters
   exactly those optimized in the GP study, or were they re-tuned for this
   comparison?
10. Are all methods evaluated using exactly the same interval arithmetic
    and schedule-construction implementation, or are the published
    GP/metaheuristic results produced by separate implementations?
11. What is the exact definition of the load-balance scale
    $s_{\mathrm{ba}}$ described as being "set to the dispersion expected
    for the instance"?
12. How was the $15\%$ interval-generation scheme rounded to integer
    endpoints, particularly for small processing times?
13. Does the "zero-shot" 64-sample result on the $20\times15$ class
    include TA11--TA14, which were used for training, or only TA15--TA20?
14. Were any of the 70 instances used to select the particular
    benchmark-wide GP artifact after the authors had access to the DRL
    results?
15. Were the classical benchmark instances used only after all
    architecture/reward/hyperparameter decisions had been frozen?
16. For the executional-robustness experiment, why was the
    independent-uniform distribution selected, and were other realization
    distributions tested?
17. Are the 1000 Monte Carlo realizations used solely for the executional
    metric and completely independent of all model training and selection?
18. Can the complete experiment records referred to in the
    data-availability statement be made available at review time rather
    than only "upon submission"?

## 6. Recommendation

**Major revision.**

The paper contains a substantial experimental study, but the GP comparison
is not currently a fair comparison of the two learning paradigms, and
several reported significance tests appear to use pseudoreplicated
instance-seed observations. These are blocking issues; the
zero-shot/generalization claims and the abstract's baseline statement also
require correction, and the manuscript needs a clearer separation between
controlled evidence and claims inferred from published metaheuristic
results.

## 7. Confidence

**5/5.** I am highly confident in the assessment of the scheduling
formulation, experimental-design issues, comparison fairness, statistical
independence, and reproducibility; my least confident judgments concern
the completeness of the related-work coverage and whether the
implementation details of the cited GP and metaheuristic studies introduce
additional differences that cannot be determined from this manuscript
alone.
