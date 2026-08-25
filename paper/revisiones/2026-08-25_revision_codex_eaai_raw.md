# Referee Report

## 1. Summary of the contribution

The manuscript presents a constructive PPO policy for the interval job shop scheduling problem (IJSP). A schedule is built by choosing the next eligible operation at each step. The proposed policy uses 16 dimensionless per-operation features and 12 global features, a shared operation encoder, mean/max pooling over eligible operations, and separate policy and value heads. This Deep Sets construction makes the network applicable without architectural changes to different numbers of jobs and machines. Inference uses one greedy rollout plus sampled rollouts, retaining the best schedule according to a worst-case-first lexicographic ordering of interval makespans.

The experimental study trains 30 policies on four \(20\times15\) Taillard instances, selects one on six validation instances, and evaluates on the 70-instance interval Taillard benchmark and 12 interval versions of classical JSP instances. The policy is compared with hand-crafted dispatching rules, published metaheuristics, and a genetic-programming (GP) hyper-heuristic at matched numbers of constructed schedules. Further analyses cover training and inference budgets, self-attention, feature importance, interval-width ablations, a width-penalizing objective, and execution under sampled processing-time realizations.

The contribution is ambitious and unusually well documented at the result level. However, inspection of the training pipeline and reward implementation reveals discrepancies that affect the claimed training protocol and the central explanation of how interval information enters learning. These are not merely documentary defects: at least the training pipeline requires the principal experiments to be repeated.

## 2. Significance and novelty assessment for EAAI’s audience

The problem is relevant to EAAI: it combines uncertainty-aware scheduling, learning-based combinatorial optimization, and a direct comparison between neural and symbolic learned heuristics. The apparent first application of DRL to this particular interval-valued JSP formulation is a meaningful application contribution. The cross-size evaluation, explicit inference-budget curves, comparison with GP, and attempt to localize where uncertainty affects each paradigm are particularly valuable.

The individual ingredients—PPO, Deep Sets pooling, sampled decoding, permutation importance, and GP dispatching rules—are established. The novelty therefore lies primarily in their integration for IJSP and in the comparative experimental design. That is sufficient for EAAI if the implementation and causal interpretation are sound. At present, the empirical solution-quality results remain interesting, but the claimed four-instance curriculum and the mechanism asserted for interval-width information do not match the supplied code.

## 3. Technical soundness

### a. Reward in Section 4.1

Several elements are verified:

- Six reward components are instantiated in `jobshop_rl/rewards/strategies/adaptive.py:47-53` and summed at lines 72-81.
- The effective training-instance weights are \(1.0\), \(0.26\), approximately \(0.24\), \(0.15\), \(0.1\), and \(0.1\), consistent numerically with Section 4.1 (`paper/main.tex:619-680`). I obtained idle weights from 0.2365 to 0.2430 on TA11–TA14.
- \(\gamma=1\) is the AgentV2 default and is passed to the PPO trainer (`jobshop_rl/agents_v2/agent.py:28-49`; `ppo_trainer.py:46-54`).
- The terminal component uses the componentwise final makespan and its upper endpoint (`rewards/components/makespan.py:85-99`).
- Criticality and progress substantially match their printed formulas.

The principal discrepancy is the machine-idleness component. The paper defines

\[
-\max(0,s_o^U-c_\mu^U)/s_{\mathrm{id}}
\]

at `paper/main.tex:639-647`. The code instead chooses an entire interval with Python’s lexicographic `max`, subtracts the machine-completion interval, and takes the upper endpoint (`rewards/components/idle_time.py:78-103`). Interval subtraction is defined as

\[
[a,b]-[c,d]=[a-d,b-c]
\]

in `models/interval.py:115-126`. Consequently, when the job determines the start, the implemented penalty contains \(s_o^U-c_\mu^L\), not \(s_o^U-c_\mu^U\). It therefore depends directly and often strongly on the lower endpoint. In a deterministic action-0 trace of TA11, 240 of 300 idle rewards differed from the printed formula.

This contradicts the central statement that none of the six components reads a lower endpoint and that width can affect decisions only through lexicographic ties (`paper/main.tex:1630-1635`, also the third contribution at lines 206-218). The verifier misses this because it searches for explicit `.lower` accesses, whereas the dependency is encapsulated in `Interval.__sub__`. Thus the empirical ablation may still show that width features are unhelpful, but the manuscript’s claimed structural explanation is false for the implemented reward.

Additional discrepancies are:

- Load balance omits all machines whose current completion is zero (`rewards/components/balance.py:74-84`), whereas the paper takes the standard deviation across all \(m\) machines (`paper/main.tex:668-680`).
- The local-improvement component gives zero on the first step because no previous value is initialized (`local_improvement.py:72-104`), whereas the printed recurrence naturally has \(M_0=0\). Moreover, \(M_t\) is nondecreasing, so this component never rewards a genuine decrease; it is an incremental makespan penalty.
- A discontinuous terminal bonus is applied for gaps at or below 5% (`makespan.py:101-113`) but is absent from Section 4.1. The supplied verifier reports that it was inactive in recorded training episodes, so this did not affect those runs, but the implementation is not fully specified.
- Scale floors such as `max(100, LB/10)` and `max(10, ...)` appear in `makespan.py:32-44`, `idle_time.py:30-44`, `criticality.py:30-44`, and `balance.py:31-45`; they are omitted from the equations. They were inactive for the main training instances.
- The statement that all weights were fixed and carried unchanged (`paper/main.tex:683-685`) is inaccurate. `AdaptiveConfigGenerator.generate_reward_config` modifies idle and balance weights per instance (`utils/problem_analyzer.py:436-471`), followed by further adaptive logic in `adaptive.py:39-70`.

### b. Lexicographic ordering and componentwise interval makespan

The mathematical implementation of Eqs. (1)–(3) is otherwise correct:

- Componentwise interval addition is implemented at `models/interval.py:86-102`.
- `Interval.max` computes \([\max L,\max U]\), not a lexicographic selection (`models/interval.py:128-171`).
- Lexicographic comparison minimizes `(upper, lower)` (`models/interval.py:207-246`).
- The environment uses `Interval.max` for predecessor completion, current makespan, and final makespan (`environment/job_shop_env.py:244-258`, 277-300).
- `final_makespan` correctly aggregates job completions componentwise (`models/interval.py:407-422`).

However, AgentV2 does not consistently use this criterion. `_episode_makespan` uses Python `max` over job-completion intervals and returns only the upper endpoint for the default objective (`agents_v2/agent.py:121-135`). Therefore checkpoint tracking and the built-in evaluator ignore the lower-endpoint tiebreak (`agent.py:157-165`, 216-230). For \(\lambda>0\), this is more serious: the width is computed from the single job interval selected lexicographically, not from the componentwise final makespan, so checkpoint selection is inconsistent with Eq. (10).

### c. Size-invariant architecture

These claims are verified:

- The encoder produces exactly 16 operation features and 12 global features (`agents_v2/state_encoder.py:17-18`, 69-159), matching Tables 1 and 2.
- The shared operation MLP, mean/max pooling, context MLP, policy head, and value head match `paper/main.tex:780-870` (`agents_v2/networks.py:62-112`).
- Padding is masked correctly in both mean and max pooling.
- The four blocks have the stated shapes and parameter counts. The base network contains exactly 120,322 trainable parameters.
- No parameter dimension depends on \(n\) or \(m\), and the policy is permutation-equivariant over candidates while the context is permutation-invariant.

The architecture is technically sound and is one of the strongest parts of the submission.

### d. Best-of-\(N\) inference

The standalone evaluators implement the printed protocol correctly:

- `scripts/eval_val_brazos.py:66-84,159-167` and `scripts/eval_treinta_semillas.py:82-98,145-153` perform one greedy rollout and \(N-1\) sampled rollouts.
- They reset the Torch seed to `1000+i`, providing common sampling seeds across training runs.
- They compute componentwise makespans and select by `(upper, lower)`.
- They report midpoint-based RE for the selected schedule.

The built-in evaluator differs: `agents_v2/agent.py:223-230` and `agents_v2/batched_eval.py:115-120` retain schedules by upper endpoint alone. The manuscript appropriately says that the main validation ladder uses the standalone evaluator (`paper/main.tex:1146-1153`), but this distinction should be made explicit wherever embedded evaluation records are used.

More importantly, the claimed evaluation checkpoint is not what the standalone evaluator loads. `_track_best` stores `best_model_state` (`agent.py:157-165`), but `save_checkpoint` writes the current network, not that stored state (`agent.py:259-266`). `BatchExperimenter` calls this method to create `best_model.pt` (`experiments/batch_experimenter.py:220-224`), and the standalone evaluator loads that file (`eval_treinta_semillas.py:132-136`). Thus `best_model.pt` is the final network of the selected training block, not the weights that produced the best training schedule described at `paper/main.tex:1032-1036`.

### e. Statistical convention

The instance-as-unit convention is implemented in the principal ablation analyses: seeds are averaged within each instance before testing (`scripts/ablaciones_unificadas.py:56-65`, `ablaciones_treinta_bo64.py:55-61`, `analiza_lambda_diez.py:61-105`). This is correct and avoids pseudoreplication.

The assertion that all tests are *exact* Wilcoxon tests (`paper/main.tex:912-920`) is false for several headline comparisons. For example, `scripts/enfrenta_gp_treinta.py:77-88` and `ablaciones_sesenta.py:45-50` call `stats.wilcoxon` with its default `method="auto"`. Under the supplied SciPy version this becomes asymptotic for 60 or 70 observations. For the selected one-pass policy-versus-GP contrast, the reported value is the asymptotic \(p=0.02883096\); `method="exact"` gives \(p=0.02842337\). The conclusion is unchanged, but the convention and printed \(p\)-values must be corrected. Comparisons containing zeros or tied ranks require an explicitly defined permutation or asymptotic procedure rather than merely forcing SciPy’s nominal exact mode.

### f. Numerical spot checks

I independently traced the following printed values through `paper/verify_numbers.py` to the underlying campaign CSVs:

| Printed result | Primary records and recomputation | Status |
|---|---|---|
| Validation best-of-64 mean over 30 runs: 13.92 (`paper/main.tex:1151-1153`; verifier lines 417-420) | 180 rows from four `benchmarks/ext30/eval_val_bo64*.csv` files; mean of the 30 six-instance seed means = 13.91807 | Verified |
| Corresponding SD: 0.60 | Same 30 seed means; sample SD = 0.59997 | Verified |
| Selected policy, 70 instances, best-of-64: 15.02 (`paper/main.tex:1273-1275`; verifier lines 2171-2172) | 70 unique rows from six `benchmarks/ext30/camp_bo64_*.csv` files; mean = 15.02259 | Verified |
| Selected policy, best-of-1024: 13.25 | 70 unique rows from six `benchmarks/ext30/camp_bo1024_*.csv` files; mean = 13.24752 | Verified |
| Featured GP rule, one pass: 17.71 (`paper/main.tex:1271-1275`; verifier lines 1786-1792) | 70 `gp_tuned_seed1` rows in `benchmarks/reevo_fixedfit/summary.csv`; mean = 17.71417 | Verified |

The numerical records are internally consistent for these checks. However, `paper/verify_numbers.py` itself does not complete in the supplied package: it raises `FileNotFoundError` for `paper/main.log` at line 2208, after also flagging zero of the expected 13 rejected-experiment records and a missing `RESEARCH_IDEAS.md`.

## 4. Experimental design and fairness of the DRL-versus-GP comparison

The comparison has several important strengths. Both methods use the same interval instances, arithmetic, componentwise makespan, schedule builder, ranking criterion, and schedule-count budgets. The manuscript correctly distinguishes matched schedule counts from wall-clock parity (`paper/main.tex:1078-1090`) and reports the considerable per-schedule and training-time disadvantage of the neural policy. The published metaheuristics are properly treated as positioning references rather than budget-matched competitors.

Training is not matched, and the manuscript acknowledges this in the limitations (`paper/main.tex:1903-1912`). Likewise, the two sampling mechanisms differ—categorical sampling for the policy and \(\epsilon\)-greedy dispatching for GP—but that is a legitimate comparison of the deployed algorithms provided the number of schedules is the chosen budget.

The serious fairness problem is artifact selection. The policy is selected on TA15–TA20, independently of the 70-instance reported comparison (`paper/main.tex:1051-1055`). In contrast, the supplied GP analysis states that the featured GP rule is the best of 30 selected on those same 70 test instances (`scripts/gp_treinta_por_clase.py:4-10`; `scripts/enfrenta_gp_treinta.py:8-12`). The manuscript only says that each study contributes the artifact it selects (`paper/main.tex:1210-1215`), obscuring this asymmetry.

This selection favors GP in point estimates, so it does not provide an easy explanation for the policy’s sampled-budget lead. Nevertheless, test-set selection invalidates the formal interpretation of the subsequent Wilcoxon tests as out-of-sample family comparisons. The mean-over-30 one-pass comparison is selection-free and reassuring, but sampled-budget results are reported only for the selected GP artifact. A fair resolution would select the GP artifact on TA15–TA20 as well, or evaluate and average all 30 GP artifacts at each sampled budget before testing over instances.

## 5. Reproducibility

The submission contains unusually rich result material: benchmark instances, many primary CSVs, all 128 supplied policy checkpoints, training summaries, schedules, standalone evaluators, analysis scripts, figure scripts, and a broad numerical audit. Re-evaluating the main policies from the supplied `outputs/` checkpoints is feasible.

Retraining and complete regeneration are not presently reproducible from the package:

- There is no README, dependency manifest, lock file, installation procedure, or end-to-end reproduction command.
- The main AgentV2 path depends on environment variables such as `DEEPLJSP_AGENT=v2`; otherwise `jobshop_rl/main.py` defaults to v1. `scripts/run_benchmark.py:141-150` guards against this, but no user-facing documentation exists.
- No per-run experiment configuration files are supplied; the output directories contain checkpoints and summaries but not the effective environment-variable configuration.
- `tuning/scenario*.txt` references missing `target_runner*.bat` files.
- Several scripts and the supplied batched-evaluation test expect `models/v2_final_deepsets_1000ep_seed2.pt`, but no `models/` directory is included. `scripts/test_batched_eval.py` therefore fails immediately.
- Robust-objective evaluation scripts expect per-instance checkpoints that are absent from the extracts (`scripts/eval_robust_lambda.py:47-69`; `eval_lambda_sweep_rollouts.py:45-61`).
- The 30 GP rule expressions are not provided; only their result CSVs are present. Therefore the claimed shared-harness GP evaluation cannot be independently rerun.
- `paper/verify_numbers.py` requires absent LaTeX auxiliary files and does not finish.
- The data-availability claim that all accepted and rejected experiment records are supplied (`paper/main.tex:2013-2017`) conflicts with the verifier’s finding of no expected rejected records.

Most importantly, the retraining code does not implement the curriculum described in the paper. `BatchExperimenter` transfers weights from `best_agent` (`batch_experimenter.py:131-142`) but updates that object only when the new instance has a lower *raw makespan* than all earlier instances (`batch_experimenter.py:192-197`). Comparing raw makespans across different instances is not meaningful. Auditing the 30 main `training_summary.csv` files shows that in 26 runs TA13’s best makespan exceeds TA12’s, so TA13’s learned weights are discarded and TA14 starts from the TA12 network. Hence the final policies were not generally trained by carrying weights through TA11→TA12→TA13→TA14 as stated at `paper/main.tex:1020-1027`.

## 6. Presentation

The manuscript is well organized, technically literate, and written in strong English. The problem formulation, diagrams, feature tables, architecture table, limitations, and distinction between constructive methods and per-instance search are particularly clear. Reporting per-instance results in the supplement and separating validation from unseen instances are commendable.

The paper is nevertheless very long and dense for its contribution. Some of the mechanistic prose is more categorical than the evidence permits: “prove inert” (`paper/main.tex:212-215`) should be replaced by an effect-size and uncertainty statement, particularly once the reward’s lower-endpoint dependence is acknowledged.

Figure 2 also needs correction. Its generating script uses seven seeds, not ten (`scripts/make_training_curve_figure.py:28-34`), despite its module description claiming ten. More importantly, AgentV2 logs the worst-case upper makespan into both the lower and upper columns (`agents_v2/agent.py:76-90`), and the figure script treats their average as the expected makespan (`make_training_curve_figure.py:49-55`). The plotted quantity is therefore a worst-case gap, not the midpoint RE defined by Eq. (4).

## 7. MAJOR issues

1. **The claimed four-instance sequential curriculum is not implemented.**  
   **Where:** `paper/main.tex:1020-1027`; `jobshop_rl/experiments/batch_experimenter.py:131-142,192-197`.  
   **Why it matters:** In 26 of 30 main runs, TA13’s weights are discarded before TA14 because raw makespans from different instances are compared. The final policies therefore do not generally result from the stated TA11→TA14 sequence. This affects every main and ablation arm using the pipeline.  
   **Resolution:** Always transfer the network resulting from the immediately preceding block, separate curriculum transfer from checkpoint selection, and rerun the principal 30-policy campaign and all training-time ablations.

2. **Checkpoint selection and serialization contradict the manuscript.**  
   **Where:** `paper/main.tex:1032-1036`; `agents_v2/agent.py:157-165,259-266`; `batch_experimenter.py:220-224`; `scripts/eval_treinta_semillas.py:132-136`.  
   **Why it matters:** `best_model.pt` contains the current network, not `best_model_state`, yet headline standalone evaluations load it as the reported checkpoint. Tracking also minimizes only the upper endpoint, not the lexicographic criterion.  
   **Resolution:** Define whether the deployed artifact is the final policy or a selected checkpoint, serialize exactly that state, apply the stated ranking criterion, record its provenance, and repeat evaluation—and training if checkpoint selection is intended to influence transfer.

3. **The implemented idleness reward invalidates the central “no lower-endpoint channel” argument.**  
   **Where:** `paper/main.tex:639-647,1630-1635`; `rewards/components/idle_time.py:78-103`; `models/interval.py:115-126`.  
   **Why it matters:** The implemented reward contains the machine completion’s lower endpoint through interval subtraction. Consequently, the theoretical explanation supporting the width-feature conclusions and Q2 is false.  
   **Resolution:** Either implement the printed upper-endpoint formula and retrain, or specify and analyze the actual reward, withdraw the structural claim, and repeat the relevant ablations under a correctly defined reward.

4. **The width-penalizing objective is not used consistently for checkpoint ranking.**  
   **Where:** Eq. (10), `paper/main.tex:1700-1716`; `agents_v2/agent.py:121-135`; `models/interval.py:407-422`.  
   **Why it matters:** For \(\lambda>0\), checkpoint ranking computes width from one lexicographically selected job-completion interval rather than the componentwise interval makespan used by the reward and standalone analysis. This compromises the claim that optimization and selection use the same \(f_\lambda\).  
   **Resolution:** Use `final_makespan` everywhere, regenerate the robust checkpoints, and repeat the \(\lambda\)-frontier experiment.

5. **The selected GP artifact uses the reported test set for selection.**  
   **Where:** `paper/main.tex:1210-1215`; `scripts/gp_treinta_por_clase.py:4-10`; `scripts/enfrenta_gp_treinta.py:8-12`.  
   **Why it matters:** Selection and inferential testing use the same 70 instances for GP, while policy selection uses the validation set. The selected-artifact Wilcoxon tests are not clean out-of-sample family comparisons.  
   **Resolution:** Select both artifacts on the shared validation set, or compare all 30 artifacts per family at each inference budget before testing on the 70 instances.

6. **The stated exact-Wilcoxon convention is not implemented.**  
   **Where:** `paper/main.tex:912-920`; `scripts/enfrenta_gp_treinta.py:77-88`; `ablaciones_sesenta.py:45-50`.  
   **Why it matters:** Several reported \(p\)-values are asymptotic despite being described as exact. This is a methodological and reporting error, although my checks suggest it does not reverse the highlighted conclusions.  
   **Resolution:** Predefine the treatment of zeros and ties, use an exact sign-permutation procedure where feasible or label the asymptotic procedure accurately, and regenerate all reported \(p\)-values.

7. **The supplied artifact does not support the data-availability and end-to-end reproducibility claims.**  
   **Where:** `paper/main.tex:2013-2017`; `paper/verify_numbers.py:825-839,2208-2215`; missing README, dependency files, runners, model files, GP expressions, and configuration records.  
   **Why it matters:** A reader can inspect many results but cannot reliably recreate training, tuning, GP inference, robust evaluation, or the full numerical verification pass.  
   **Resolution:** Provide a documented, version-pinned archive with one-command verification, complete run configurations, all referenced scripts and artifacts, checkpoint hashes, GP trees, and a verifier that runs successfully from a clean checkout.

## 8. MINOR issues

1. Amend Section 4.1 to disclose the per-instance adaptive idle weight, scale floors, and dormant terminal bonus.

2. Make the load-balance formula agree with whether inactive machines are included (`balance.py:74-84` versus `paper/main.tex:668-680`).

3. Correct Figure 2 to state that seven seeds are plotted and use the componentwise midpoint if the axis is labelled RE under Eq. (4).

4. The universality statement about Deep Sets at `paper/main.tex:822-827` is too broad for this finite mean-plus-max architecture; distinguish the general representation theorem from the capacity of the implemented network.

5. Replace “at no budget do they tie” with “at each evaluated budget they differ significantly”; only a finite set of budgets was tested.

6. Add checkpoint path/hash, evaluation seed scheme, code revision, and arm configuration to every primary CSV. Current filenames and hard-coded routing functions carry too much provenance information implicitly.

7. Clarify that the “all seventy” aggregate includes four training and six validation instances; the dagger in Table 7 does this visually, but the abstract’s wording can be read as an entirely unseen test.

8. If no multiplicity adjustment is retained, describe the analyses as individually interpreted contrasts rather than asserting that they were all posed in advance unless a dated protocol is supplied.

## 9. Overall recommendation

**Reject.**

The architecture, interval propagation, standalone best-of-\(N\) evaluator, and spot-checked numerical aggregates are strong. Nevertheless, the actual training curriculum differs from the manuscript in 26 of 30 principal runs, the deployed checkpoint is not the checkpoint described, and the reward has a lower-endpoint dependency that invalidates a central mechanistic contribution. The GP selection and statistical-procedure discrepancies further weaken the formal comparison. Resolving these problems requires correcting the pipeline and repeating the main training and ablation campaigns, not only revising the exposition. A substantially revised and fully reproducible resubmission could be valuable to EAAI.
