# 1. Summary of the contribution

The manuscript presents a size-invariant PPO hyper-heuristic for interval-valued job-shop scheduling. Processing times are represented as closed intervals, schedules are constructed through interval arithmetic, and solutions are ranked lexicographically by worst-case makespan and then by the lower endpoint. The policy uses a Deep Sets representation of currently schedulable operations, combining 16 operation-level and 12 global features so that one network can operate on different instance sizes. Training proceeds through four Taillard instances, with transfer between instance blocks, and the final policy is selected from 30 independent training runs using a separate validation set.

The experimental study compares the learned policy with 30 genetic-programming dispatching rules and several literature baselines. It evaluates greedy and best-of-\(N\) inference, cross-size generalization, architectural and interval-information ablations, budget–quality curves, and execution under sampled processing times. The principal empirical result is that the policy is weaker than the featured GP rule with one deterministic rollout but overtakes it when both methods receive matched schedule-construction budgets.

The submission is unusually transparent about several unfavorable findings: equal schedule counts do not imply equal wall-clock cost, the GP rule was selected more favorably than the policy in one comparison, cross-instance training blocks are compared using raw makespan, and a robust-objective tracking inconsistency is acknowledged. Most central computations are supported by deposited CSV/JSON records. However, the executable package still has important inconsistencies in evaluator semantics and artifact selection, and the advertised verification/reproduction path is not yet self-contained.

# 2. Significance and novelty assessment for EAAI’s audience

The work addresses a relevant EAAI problem: using a learned, reusable constructive policy for a combinatorial optimization problem with epistemic or bounded processing-time uncertainty. The combination of interval scheduling, a permutation- and size-invariant neural policy, sequential transfer across training instances, and a controlled comparison with GP hyper-heuristics is technically interesting. In particular, exposing the complete inference-budget curve is more informative than reporting only a single best-of-\(N\) point.

The strongest novelty is not PPO or Deep Sets individually, but their integration with interval-valued JSSP semantics and a systematic DRL-versus-GP comparison under a shared schedule builder. The claim of being the first such treatment should remain qualified as “to the best of our knowledge,” because adjacent literature exists on DRL for classical and stochastic JSSP, while the boundary between interval, robust, and stochastic scheduling is not always consistently named.

The contribution is potentially significant for EAAI, but the most convincing claim is presently sample efficiency under the authors’ defined constructive-rollout budget. It is not computational efficiency: the manuscript correctly reports that a GP rollout is substantially cheaper. The work should therefore avoid any broader implication that the learned policy is uniformly superior to GP.

# 3. Technical soundness

## 3.a Reward definition

**Verified.** The six-component reward in Section 4.1 matches the implementation in `jobshop_rl/rewards/strategies/adaptive.py:25-70,88-107`:

\[
r=w_mr_m+w_pr_p+w_ir_i+w_lr_l+w_cr_c+w_br_b.
\]

The implemented components agree with the manuscript:

- The terminal component uses the componentwise worst-case makespan and returns \(-C_{\max}^{U}/s_m\), with \(s_m=\max(100,LB^U/10)\); see `jobshop_rl/rewards/components/makespan.py:32-45,85-113`.
- Progress gives \(1/(nm)\) on each nonterminal step; see `progress.py:24-39`.
- Idle time uses the upper endpoint of the start interval minus the machine’s lower completion endpoint, normalized by twice the mean midpoint duration with a floor; see `idle_time.py:30-44,62-103`.
- Local improvement uses projected deterioration relative to the current upper makespan, with twice the penalty for deterioration and the stated makespan-dependent scale; see `local_improvement.py:61-106`.
- Criticality is remaining upper processing work divided by \(W^U/(2n)\), subject to the stated floor; see `criticality.py:30-44,62-99`.
- Balance uses the standard deviation of current upper machine completions, normalized by \(1.5\) times the standard deviation of total upper machine loads; see `balance.py:31-45,63-84`.

The experiment path supplies the nominal vector \((1,.15,.05,.15,.05,.30)\) in `jobshop_rl/main.py:246-260`. The generic strategy constructor has a different default terminal balance of `.40`, but that default is overridden by the experiment configuration. The conditional adaptations in `adaptive.py:56-70` also match Section 4.1. For TA11–TA14, the deposited verification establishes that only the balance reduction fires, giving \((1,.15,.05,.10,.05,.30)\). The manuscript correctly notes that the relevant scale floors and terminal bonus are inactive for the reported training instances.

The configured `gamma=1` is also correct for AgentV2. Although `jobshop_rl/main.py` retains obsolete AgentV1 values, `AgentFactory` constructs AgentV2 with its own defaults, including \(\gamma=1\), in `jobshop_rl/experiments/factory.py:157-198` and `jobshop_rl/agents_v2/agent.py:28-50`. This stale dual configuration is a reproducibility hazard, but the reported run used the claimed value.

## 3.b Interval makespan and lexicographic ranking

**Verified.** Interval addition and componentwise maximum implement Equations (1)–(2) in `jobshop_rl/models/interval.py:86-102,128-171`. Relational operators rank intervals lexicographically by \((U,L)\), as stated in Equation (3), at `interval.py:207-246`.

The environment computes operation starts using componentwise maximum and updates job and machine completion intervals accordingly; see `jobshop_rl/environment/job_shop_env.py:215-289`. Final makespan information is obtained through the componentwise `Interval.max`, not by selecting one job interval, at `job_shop_env.py:297-304` and `interval.py:407-422`.

Thus the scheduling semantics used by the standalone experiments are internally consistent: componentwise maxima define the feasible completion envelope, while complete schedules are ordered first by upper and then lower makespan. One minor exception is visualization code at `job_shop_env.py:493-494`, which uses Python’s lexicographic `max` and can therefore display the lower endpoint of the upper-critical job rather than the componentwise lower makespan.

## 3.c Size-invariant architecture

**Verified.** `jobshop_rl/agents_v2/state_encoder.py:17-18,39-159` constructs exactly 16 operation features and 12 global features. Their definitions, endpoint choices, and normalizations correspond to Tables 1–2.

`jobshop_rl/agents_v2/networks.py:17-33,62-112` implements the stated four MLP blocks:

1. operation encoder \(16\rightarrow128\rightarrow128\);
2. context encoder \(268\rightarrow128\rightarrow128\), where \(268=128+128+12\) from mean pooling, max pooling, and global features;
3. policy head \(256\rightarrow128\rightarrow1\);
4. value head \(128\rightarrow128\rightarrow1\).

Padding masks are applied to both pooling and action logits. The resulting counts are 18,944, 51,200, 33,281, and 16,897 parameters, totaling 120,322, exactly as printed. `paper/verify_numbers.py:891-960` independently instantiates the network and checks this count. The architecture is genuinely independent of the number of jobs and machines.

## 3.d Training protocol and deployed artifact

The main training logic matches the description in Section 5.4. `jobshop_rl/experiments/batch_experimenter.py:123-149` creates a fresh agent and optimizer for each instance block, reinitializes it with the same seed, and transfers network weights from the best prior block. At `batch_experimenter.py:192-198`, “best” is determined by the smallest raw episode makespan across blocks. This explains the reported nonmonotone transfer, including TA14 sometimes starting from TA12 rather than TA13.

The statistic called the best episode includes both sampled training episodes and the additional greedy evaluation performed every ten episodes; see `jobshop_rl/agents_v2/agent.py:171-190`. This should be stated explicitly.

The checkpoint stored as `best_model.pt` is the network at the end of the selected block, not the snapshot at the best individual episode: `batch_experimenter.py:220-221` calls `save_checkpoint`, which serializes the current network at `agent.py:259-266`. This agrees with the manuscript’s definition of the deployed artifact.

However, the built-in test path uses a different artifact. `batch_experimenter.py:300-308` preferentially loads `best_model_state`, which is the in-episode snapshot saved at `agent.py:157-165`. Therefore, `best_model.pt`, the standalone evaluators, and `BatchExperimenter.evaluate_test_problems` do not all evaluate the same defined artifact. The headline CSVs appear to come from the standalone evaluators and hence use the claimed final-block checkpoint, but the package API is inconsistent.

## 3.e Best-of-\(N\) inference

**Verified for the headline standalone experiments.** Both `scripts/eval_val_brazos.py:66-84,159-167` and `scripts/eval_treinta_semillas.py:82-98,145-153` execute one greedy rollout followed by \(N-1\) sampled rollouts, compute componentwise final endpoints, and retain the lexicographic minimum \((U,L)\). Reported relative error is then based on the retained interval midpoint.

The generic AgentV2 evaluator is not equivalent. `jobshop_rl/agents_v2/agent.py:121-135,216-230` reduces every schedule to a scalar upper endpoint when \(\lambda=0\); `evaluate_policy` therefore ignores the lower endpoint when upper endpoints tie. This contradicts Equation (3) and the stated deployed rule. The paper reports seven tied-upper pools among 300 interval-ablation pools, so this is not a purely theoretical edge case.

The standalone scripts rescue the headline results, but a reader using the package’s advertised `evaluate_policy` interface will not reproduce the exact inference criterion.

## 3.f Statistical convention

**Verified.** The analysis scripts average seeds within instance before paired testing:

- `scripts/ablaciones_unificadas.py:60-65`;
- `scripts/ablaciones_treinta_bo64.py:55-61`;
- `scripts/ablaciones_sesenta.py:44-50`;
- `scripts/analiza_lambda_diez.py:55-69,94-105`;
- `scripts/enfrenta_gp_treinta.py:77-88`.

They then apply two-sided Wilcoxon signed-rank tests across instances, using exact computation, and construct Student-\(t\) intervals over the instance-level differences. Independent recalculation of selected contrasts agreed with the recorded \(p\)-values. The unit of inference is therefore the instance, not an individual seed or rollout.

The manuscript explicitly states that no multiplicity adjustment is applied (`paper/main.tex:935-975`). That is transparent, but several narrative claims rely on marginal \(p\)-values among many related ablations and budget comparisons. These should be presented as exploratory unless primary hypothesis families are identified.

## 3.g Budget-curve reconstruction

**Verified.** `scripts/eval_curva_intervalo.py:1-20,53-84` evaluates ten runs on all 70 instances, storing one greedy schedule and 341 sampled schedules per run–instance pair. This gives the stated \(342\times10\times70=239{,}400\) schedules.

`scripts/analiza_curva_intervalo.py:33-36,40-50,79-100` reconstructs each budget \(B\) as the fixed greedy rollout plus \(B-1\) samples drawn without replacement from the stored stochastic pool. It uses the lexicographic \((U,L)\) key and repeats the subsampling 200 times. Thus it implements an empirical reconstruction of the deployed protocol, rather than the earlier midpoint-retention variant. The recorded crossings at \(B=2\) and \(B=6\), the \(B=64\) mean of approximately 15.34%, and the \(B=341\) mean of approximately 14.19% follow from that reconstruction.

The method is sound for estimating the budget curve from a finite rollout pool. The paper should nevertheless report Monte Carlo uncertainty from the 200 reconstructions and explain why the plotted maximum is 341 rather than the full stored budget of 342.

## 3.h Numerical spot checks

I traced the following printed quantities:

1. **Featured GP, one pass over 70 instances: 17.71%.**  
   `paper/verify_numbers.py:1791-1797` reads `benchmarks/reevo_fixedfit/summary.csv`, filters `gp_tuned_seed1`, verifies all 70 instances, and averages their relative errors. This is a direct primary-CSV check.

2. **Validation champion: seed 5, mean BO64 RE 12.77% (unrounded 12.7668%).**  
   `scripts/elige_campeon.py:26-74` reads the `benchmarks/ext30/eval_val_bo64*.csv` files, ranks all 30 seeds, and writes `campeon.json`. `paper/verify_numbers.py:2082-2116` checks seed 5 and the 30-entry ranking.

3. **Selected-policy BO64 versus GP BO64: 15.02% versus 15.88%, \(p=0.020\).**  
   `paper/verify_numbers.py:1840-1862` checks these values in `benchmarks/ext30/enfrentamiento70.json`. That JSON is generated by `scripts/enfrenta_gp_treinta.py` from the per-instance policy campaign CSVs and `fair_gp_eps.csv`.

4. **Budget curve: 15.34% at \(B=64\) and 14.19% at \(B=341\).**  
   The raw `benchmarks/curva_intervalo/curva_*.csv` files are aggregated by `scripts/analiza_curva_intervalo.py:40-102`. `paper/verify_numbers.py:3138-3155` checks the resulting summary.

5. **Midpoint-training ablation: approximately +0.432 percentage points, \(p=0.044907\).**  
   `scripts/ablaciones_treinta_bo64.py:45-61` derives the contrast from the per-seed `benchmarks/ext30/c64_*.csv` files after averaging seeds within instance. The resulting values are checked through `benchmarks/ext30/ablaciones_treinta_bo64.json` in `paper/verify_numbers.py:2470-2495`.

These checks support the printed results, but they also reveal that `verify_numbers.py` often verifies a derived JSON rather than rebuilding it from the primary CSVs.

# 4. Experimental design and fairness of the DRL-vs-GP comparison

The comparison is strong in several respects:

- Both methods use the same interval instances, schedule builder, objective, and reporting convention.
- At each inference budget, both receive the same number of complete schedule constructions.
- The 30 GP rules are deposited, and the policy study includes 30 independently trained artifacts.
- The manuscript reports both a selected-artifact comparison and, where affordable, a 30-versus-30 comparison.
- Policy selection uses TA15–TA20 validation instances rather than the 60-instance held-out test set.

The schedule-count budget is reasonable for studying constructive sample efficiency, but it is not a computationally matched budget. A GP rollout is reported to be approximately 7–11 times cheaper, so equal rollout counts favor the policy in time and energy. The manuscript acknowledges this and should consistently describe the result as sample-budget superiority.

The randomization mechanisms are also not equivalent: the policy samples from a categorical action distribution, whereas GP obtains alternative schedules through its perturbation mechanism. Equal numbers of completed schedules are auditable, but not algorithm-neutral.

Artifact selection is partially asymmetric. The policy champion is chosen on the six validation instances, whereas the featured GP rule was originally selected over the full 70-instance suite. The manuscript commendably reports that validation-only GP selection would choose the same rule and provides the 30-rule/30-policy one-pass comparison. Nevertheless, BO64 and BO1024 headline results remain selected-artifact comparisons rather than distributions across all 30 artifacts.

Training budgets are not matched: the policy and GP use different optimization procedures, tuning paths, and wall-clock budgets. This does not invalidate the stated inference comparison, but it precludes claims about overall learning efficiency. The paper generally respects this boundary.

# 5. Reproducibility

A technically competent reader could re-evaluate the supplied checkpoints after studying the scripts, because the repository contains benchmark instances, checkpoints, logs, standalone evaluators, primary campaign records, and the 30 GP rules. The deposited intermediate results are sufficiently rich to audit many claims.

A clean retraining and re-evaluation is not presently turnkey:

- There is no root README, dependency lock file, `requirements.txt`, `pyproject.toml`, Conda environment, or equivalent installation specification.
- `jobshop_rl/main.py:272-274` defaults to AgentV1. The correct architecture requires `DEEPLJSP_AGENT=v2`; only `scripts/run_benchmark.py:141-150` guards against the wrong setting.
- Many evaluation scripts contain hard-coded historical output directory names, timestamps, checkpoint mappings, and campaign tags.
- No single documented command regenerates the champion selection, all aggregate JSON files, all tables, all figures, and the final verification result.
- The current `paper/verify_numbers.py` run reports **792 successful checks, one failure, and six checks pending source material**. The failed check is the development-history assertion at `verify_numbers.py:830-835`; `RESEARCH_IDEAS.md` is also absent at `verify_numbers.py:839-844`. The script merely prints the failure count at `verify_numbers.py:3643-3644` and does not return a failing exit status.
- The verifier frequently reads derived summaries, for example `enfrentamiento70.json` at `verify_numbers.py:1841-1862`, ablation JSONs at `2470-2478`, and `curva_intervalo.json` at `3138-3153`. It therefore does not literally recompute every printed number from primary data.
- `paper/make_figures.py:36-66,84-99,150-168` hard-codes several plotted values. Its main routine at `make_figures.py:648-658` does not generate `fig_budget.pdf`; that figure requires the separate `scripts/make_budget_curve_figure.py`.

These are repairable packaging problems rather than evidence that the deposited numbers are fabricated, but they fall short of the reproducibility standard implied by the manuscript’s data-availability statement.

# 6. Presentation

The manuscript is generally well written and technically candid. The interval definitions, architecture, training protocol, and distinction between sample and time budgets are explained clearly. Tables provide both aggregate and class-level information, and the budget curve is particularly useful.

The paper is nevertheless dense for a 36-page single-column article. Some implementation-history details, rejected exploratory variants, and secondary validation results could move to the supplement. The central claims would be easier to identify if each experimental section ended with one concise conclusion and its precise scope.

Terminology should be tightened around the midpoint. The midpoint of a componentwise interval makespan is a nominal interval summary; even under independent uniform operation times, it is not generally \(E[C_{\max}]\), because the maximum is nonlinear. The manuscript acknowledges the proxy in `paper/main.tex:479-493`, but later uses “expected makespan” and “calibration” language more strongly. Either estimate the actual expectation from simulations or consistently call the quantity the interval midpoint/nominal makespan.

The English is publication quality, with only occasional long sentences and overly defensive implementation commentary. Figure captions should identify whether uncertainty bands represent seeds, instances, or Monte Carlo reconstructions. The “what the policy attends to” wording should be changed where the analysis is permutation importance rather than inspection of learned attention weights.

# 7. MAJOR issues

1. **The package has inconsistent definitions of best-of-\(N\) selection and of the deployed artifact.**  
   **Where:** `jobshop_rl/agents_v2/agent.py:121-135,216-230`; `jobshop_rl/experiments/batch_experimenter.py:300-313`; Section 5.4 and Equation (3).  
   **Why it matters:** `evaluate_policy` minimizes only \(U\) and ignores the lower-endpoint tie-break. The built-in batch evaluator also loads the best-episode snapshot, whereas `best_model.pt` and the paper define the deployed artifact as the end state of the selected block. Thus two reasonable entry points can evaluate different schedules and different networks.  
   **Resolution:** Make the evaluator return and compare a common objective key, at least \((U,L)\) for the main experiment. Make all evaluation paths load the same explicitly named deployed checkpoint. Add regression tests containing equal-upper/different-lower schedules, and confirm whether any reported results change.

2. **The robust-objective tracker does not compute the componentwise interval makespan.**  
   **Where:** `jobshop_rl/agents_v2/agent.py:121-135`; manuscript discussion at `paper/main.tex:1802-1810`.  
   **Why it matters:** Python’s `max(self.env.job_completion_time)` chooses one job interval lexicographically. Its lower endpoint need not equal \(\max_j C_{j,L}\). Therefore \(U+\lambda(U-L)\) is incorrect for model/block tracking when \(\lambda>0\), even though the reward and standalone evaluation use the correct componentwise interval. This can alter block transfer and final artifact selection, directly confounding the conclusion that robust retraining has little effect. Disclosure is welcome but does not repair the experiment.  
   **Resolution:** Track `env.final_makespan()` or `Interval.max(...)`, rerun the robust arms, and report whether block choices, selected checkpoints, and frontier conclusions remain unchanged.

3. **The advertised numerical and figure verification pipeline is not a clean reconstruction from primary data.**  
   **Where:** `paper/verify_numbers.py:830-844,1841-1862,2470-2478,3138-3153,3643-3644`; `paper/make_figures.py:36-66,84-99,150-168,648-658`.  
   **Why it matters:** The verifier currently reports one failure and six pending sources, exits without signaling failure, and often checks derived JSON summaries rather than recomputing them. Several figures contain hard-coded values, and the budget figure is omitted from the advertised figure script. This weakens a major strength claimed by the submission.  
   **Resolution:** Provide one documented command that starts from primary CSV/JSON records, rebuilds every intermediate aggregate, table, and figure, and terminates nonzero on any failed check. Remove development-history checks from the release verifier or ship their sources.

4. **The release lacks the executable documentation and environment specification required for independent retraining.**  
   **Where:** repository root; `jobshop_rl/main.py:272-274`; `scripts/run_benchmark.py:141-150`; hard-coded paths in the evaluation scripts.  
   **Why it matters:** A naïve invocation selects AgentV1, and there is no authoritative environment manifest or end-to-end guide. Successful reproduction currently depends on reverse-engineering environment variables and historical output paths.  
   **Resolution:** Add a root README, pinned dependencies, exact training/evaluation commands, random-seed conventions, checkpoint-selection instructions, expected runtimes/hardware, and portable path/config arguments. The documented smoke test should verify that AgentV2, \(\gamma=1\), the reported reward weights, and lexicographic evaluation are active.

5. **Confirmatory and exploratory statistical claims are not sufficiently separated.**  
   **Where:** statistical convention in `paper/main.tex:935-975` and the numerous contrasts in Sections 6–7.  
   **Why it matters:** Seeds are handled correctly, but many related Wilcoxon tests are interpreted individually without multiplicity control. Conclusions supported by \(p\)-values near .05 are fragile under any reasonable family-wise treatment.  
   **Resolution:** Identify a small set of prespecified primary contrasts and apply an appropriate correction within clearly defined families, or explicitly label the remaining tests exploratory and temper “significant” wording. Report effect sizes and instance-level differences as the primary evidence.

# 8. MINOR issues

1. Clarify in Section 5.4 that the block-selection statistic includes periodic greedy evaluations as well as sampled training episodes (`agent.py:171-190`).

2. Remove or clearly mark obsolete AgentV1 hyperparameters in `jobshop_rl/main.py`; presently they appear to configure AgentV2 even though the factory ignores them.

3. Replace the visualization-time lexicographic `max` in `job_shop_env.py:493-494` with the same componentwise final-makespan routine used by evaluation.

4. Report Monte Carlo uncertainty for the budget-curve reconstruction and explain the \(B=341\) endpoint despite storing 342 rollouts.

5. Consistently call the interval midpoint a “midpoint” or “nominal estimate,” not an expected makespan, unless an expectation under an explicit duration distribution is actually computed.

6. Describe Student-\(t\) intervals over only six validation instances as descriptive; they should not convey stronger uncertainty quantification than the sample permits.

7. Clearly label best-to-worst seed bands as ranges rather than confidence intervals.

8. Rename “what the policy attends to” to “permutation importance” unless actual attention weights or attribution scores are analyzed.

9. Replace hard-coded campaign timestamps and output-directory maps in evaluation scripts with command-line or configuration-file arguments.

10. Translate user-facing Spanish error messages and historical comments in the released scripts, or document them, to improve accessibility.

11. Add automated tests for interval addition, componentwise maximum, lexicographic tie-breaking, reward component scales, feature dimensions, parameter count, and checkpoint-selection semantics.

12. The raw cross-instance transfer criterion is correctly disclosed, but its dependence on instance scale and block order deserves a short sensitivity analysis or a stronger limitation statement.

# 9. Overall recommendation

**Major revision.**

The principal interval arithmetic, reward, Deep Sets architecture, parameter count, statistical unit, standalone best-of-\(N\) protocol, and most printed numerical results are technically consistent with the manuscript. The experimental comparison is thoughtful and unusually transparent about its limits. I therefore do not see grounds for rejection on the basis of the central reported results.

However, the generic evaluator does not implement the stated lexicographic criterion, the built-in batch evaluator can deploy a different network snapshot, and robust-objective model tracking uses an incorrect lower makespan endpoint. In addition, the current verification script does not pass cleanly or reconstruct all results from primary records, and the repository lacks a portable retraining specification. These issues materially affect technical reproducibility and, for the robust-objective experiment, possibly the scientific conclusion. They should be corrected and the affected results revalidated before publication.