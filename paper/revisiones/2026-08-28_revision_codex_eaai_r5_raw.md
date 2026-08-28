# Referee Report

## 1. Summary of the contribution

This paper develops a deep reinforcement learning method for the interval job-shop scheduling problem, where every processing time is represented by an interval. A PPO policy constructs semiactive schedules one operation at a time. Its state representation combines 16 normalized operation features with 12 global features, while a Deep Sets architecture provides a fixed-size representation regardless of the number of jobs, machines, or eligible operations. The training reward combines terminal makespan, progress, idleness, local projected makespan, criticality, and load-balance terms.

The experimental study emphasizes size generalization and inference-budget effects. Thirty policy runs trained on four \(20\times15\) instances are evaluated on interval Taillard instances from \(15\times15\) to \(50\times20\), as well as twelve classical instances. The principal comparison is against thirty genetic-programming dispatching rules. The study matches the number of constructed schedules at inference—one deterministic construction plus sampled constructions—and shows a budget-dependent ordering: the selected GP rule leads in one pass, the methods are similar around 64 constructions, and the policy leads at 1024 on the full 70-instance aggregate, although not consistently on the largest size classes.

A further contribution is the analysis of interval information and robustness. The paper studies feature and objective ablations, reconstructs performance as a function of sampling budget, and separates the effects of retraining and sample selection under a width-penalized objective. The supplied records and verification program make the numerical content unusually auditable.

## 2. Significance and novelty assessment for EAAI’s audience

The work is relevant to EAAI because it combines an industrially meaningful scheduling problem, uncertainty-aware modeling, learned constructive heuristics, and a comparatively careful empirical comparison with genetic-programming hyper-heuristics. The size-invariant representation and the direct analysis of where interval information affects the learned system are particularly useful to scheduling and hyper-heuristic researchers.

The algorithmic ingredients—PPO, Deep Sets, normalized handcrafted features, and sampled decoding—are not individually novel. The novelty lies in their integration for interval JSSP, the scale-transfer study, the matched inference-budget comparison with GP, and the mechanistic analysis of width-aware selection. I therefore judge the application-level novelty as moderate to high for EAAI, provided the remaining validity and reproducibility issues are resolved.

The practical scope is appropriately bounded. The policy searches only semiactive schedules, uses symmetric \(\pm15\%\) uncertainty, is relatively expensive at high sampling budgets, and does not outperform specialized per-instance metaheuristics. The manuscript generally acknowledges these limitations and does not claim otherwise.

## 3. Technical soundness

### a. Reward implementation

I verified the six components in Section 4.1 against `jobshop_rl/rewards/`:

| Component | Paper | Implementation |
|---|---:|---|
| Terminal makespan | weight 1.00; \(-C_{\max}^U/(\mathrm{LB}/10)\) | `components/makespan.py:32-59,85-113` |
| Progress | weight 0.05; \(1/(nm)\), except terminal | `components/progress.py:31-39` |
| Idleness | weight 0.15; \(-(s^U-c_\mu^L)/(2\bar p)\) when the job predecessor determines the start | `components/idle_time.py:73-103` |
| Local projected makespan | weight 0.30; upper-endpoint change, factor two on deterioration | `components/local_improvement.py:72-104` |
| Criticality | weight 0.05; remaining upper job work divided by \(W^U/(2n)\) | `components/criticality.py:73-99` |
| Load balance | effective weight 0.10; upper completion-time standard deviation over used machines | `components/balance.py:74-86` |

The entry point supplies the nominal vector explicitly, including balance weight 0.15; the adaptive layer then lowers balance to 0.10 when machine-load dispersion exceeds its threshold (`rewards/strategies/adaptive.py:60-70`). I instantiated the environments for TA11–TA14 and confirmed that this is the only adjustment firing, and that it fires for all four. Explicit tuning weights bypass that adjustment, as stated.

The implementation also contains the scale floors and terminal bonus described as dormant in Section 4.1. The observed training-instance scales exceed their floors, and the verifier found no training episode activating the bonus.

The effective PPO discount is indeed \(\gamma=1\): it is the default in `agents_v2/agent.py:29`, and the V2 factory does not override it. However, `jobshop_rl/main.py:265` still contains a dead \(\gamma=0.99\) setting inherited from the older agent path. This does not change the reported V2 experiments, but it is confusing and should be removed or explicitly overridden.

One substantive clarification is needed for the “local improvement” term. Since every scheduled operation can only increase or preserve the maximum machine-completion upper endpoint, \(M_t^U<M_{t-1}^U\) cannot occur. Thus the positive “improvement” branch in `local_improvement.py:94-101` is unreachable: every nonzero change receives the factor two. With \(\gamma=1\), the accumulated changes also largely telescope. The formula matches the paper, but the interpretation as rewarding improvements and penalizing deteriorations asymmetrically is misleading.

### b. Interval makespan and lexicographic criterion

Equations (1)–(3) match the implementation.

- The environment computes each start as the componentwise maximum of the job and machine completion intervals and then adds the duration interval (`environment/job_shop_env.py:245-263`).
- `Interval.max` independently maximizes lower and upper endpoints (`models/interval.py:128-171`).
- `final_makespan` therefore returns
  \[
  [\max_j C_j^L,\max_j C_j^U],
  \]
  as required by Eq. (2) (`models/interval.py:407-422`).
- Interval comparisons use the tuple \((\text{upper},\text{lower})\), matching Eq. (3) (`models/interval.py:207-246`).
- The environment reports the componentwise makespan at completion (`environment/job_shop_env.py:278-303`), and default best-of-\(N\) retention explicitly uses \((C_{\max}^U,C_{\max}^L)\) (`agents_v2/agent.py:150-163`).

The historical robust-arm tracking exception is separate and discussed under Major Issue 1.

### c. Size-invariant architecture

The architecture claims are accurate.

- `state_encoder.py:17-18` fixes the operation and global dimensions at 16 and 12.
- The feature construction in `state_encoder.py:55-159` matches the two feature tables in Section 4.2, including interval endpoints and widths, remaining work, machine congestion, slack, completion summaries, progress, load statistics, and uncertainty summaries.
- `networks.py:64-76` defines the four claimed MLP blocks: the shared operation encoder, pooled-context encoder, policy head with an operation embedding skip, and value head.
- `networks.py:93-111` applies the shared encoder, masked mean and maximum pooling, global context, and per-candidate policy scoring.

Independent parameter counting gives:

- operation encoder: 18,944;
- context encoder: 51,200;
- policy head: 33,281;
- value head: 16,897;
- total: 120,322.

This agrees exactly with Section 4.3 and `paper/verify_numbers.py`.

### d. Training protocol and deployed artifact

Section 5.4 accurately describes an unusual but important implementation detail. In `experiments/batch_experimenter.py:101-224`, each new instance block starts from the policy of the block with the lowest raw best-episode makespan so far. The comparison is made in raw time units even across different instances (`batch_experimenter.py:193-197`). The next block receives those policy weights (`batch_experimenter.py:141-144`).

At the end of each block, the current network is serialized. Although `AgentV2` tracks `best_model_state` during episodes (`agents_v2/agent.py:186-190`), `save_checkpoint` serializes the network as it stands at the end of the block, not that best-episode snapshot (`agents_v2/agent.py:290-297`). Consequently, `best_model.pt` is the end-of-best-block network, exactly as the paper now states.

I inspected the thirty principal training summaries. Every run has four blocks, TA14 is the raw-best block in all thirty, and the deployed artifact is therefore the final TA14 checkpoint. The reported observation that TA12, rather than TA13, supplies the starting weights for TA14 in 26 of 30 runs is also reproduced by the records. The seed is reapplied indirectly through environment construction at every block; the behavior is correct but should be made explicit in the experiment driver rather than relying on a global side effect.

### e. Best-of-\(N\) evaluation

The standalone evaluators implement the declared inference protocol:

- `scripts/eval_val_brazos.py:66-84,141-167` loads `best_model.pt`, performs one greedy rollout followed by \(N-1\) sampled rollouts, and retains the minimum \((C_{\max}^U,C_{\max}^L)\).
- `scripts/eval_treinta_semillas.py:47-59,82-98,145-153` maps all thirty seeds to their corresponding output directories and applies the same protocol.
- The midpoint is used only to compute reported RE after lexicographic selection.

Thus the standalone evaluation is consistent with Section 5.4 and Eq. (3). The sampled rollout seeds are held common across artifacts, which is a sensible variance-reduction convention.

### f. Statistical convention

The analysis scripts implement the convention stated in Section 5.2:

- seeds are first averaged within each instance;
- the paired instance-level differences are then tested;
- SciPy’s two-sided exact Wilcoxon test is requested explicitly.

Examples are `ablaciones_sesenta.py:44-50`, `ablaciones_treinta_bo64.py:55-61`, `ablaciones_unificadas.py:56-65`, `analiza_lambda_diez.py:61-69,94-105`, and `enfrenta_gp_treinta.py:77-88`. I found no zero differences or tied absolute differences in the headline 70-instance selected-pair contrasts, so the exact calculation is well defined there.

The paper openly states that no multiplicity correction is applied. That is acceptable for clearly labeled individual hypotheses, but the many related ablation and subgroup claims would benefit from effect sizes, paired confidence intervals, and a multiplicity sensitivity analysis. In the six-instance validation tests, \(p=0.03125\) simply corresponds to all six differences having the same sign; this should be interpreted accordingly.

### g. Budget-curve reconstruction

The policy-side reconstruction now implements the deployed protocol correctly.

`scripts/eval_curva_intervalo.py` stores both endpoints for 342 rollouts per policy–instance pair: one greedy plus 341 sampled. It loads the final TA14 checkpoint (`eval_curva_intervalo.py:45`), which is the deployed checkpoint because TA14 is the best block for all relevant runs. For \(B>1\), `analiza_curva_intervalo.py:82-103` combines the greedy solution with \(B-1\) sampled schedules and retains the lexicographic minimum. It repeats random subset selection 200 times (`analiza_curva_intervalo.py:34-35,93-101`) and then averages over the ten policy artifacts.

This is materially different from an older midpoint-only reconstruction, but the manuscript and current figure use the corrected interval-aware data.

The GP curve uses the same number of retained schedules and the same lexicographic decoder, but not the same Monte Carlo reconstruction: `make_budget_curve_figure.py:145-162` uses one nested prefix from one stochastic pool for the single selected rule. The consequences are discussed under Major Issue 2.

### h. Provenance of the DRL-versus-GP comparison

The following artifact mapping could be reconstructed:

| Result | Policy artifact and data | GP artifact and data | Same artifact across budgets? |
|---|---|---|---|
| Table 7, selected pair | Seed-5 `best_model.pt` under `outputs/bench_v2-full-1000ep-ext-c__6de2c20__20260803_071159_seed5/`. \(B=1\): `benchmarks/eval70_diez_semillas.csv`; \(B=64,1024\): `benchmarks/ext30/camp_bo64_*.csv` and `camp_bo1024_*.csv` | `rules/gp_main_arm/gp_tuned_seed1.json`, duplicated in the benchmark records. \(B=1\): `benchmarks/reevo_fixedfit/summary.csv`; sampled budgets: `benchmarks/gp_destacada/gp_destacada_presupuestos.csv`, derived from `pool_*.csv` | Yes on both sides |
| Figure 7 budget curve | Final TA14 checkpoints for policy seeds 2–11; `benchmarks/curva_intervalo/curva_*.csv` | The same seed-1 GP rule; `benchmarks/gp_destacada/pool_*.csv` | Yes: the same ten policies and same one GP rule for every \(B\) |
| Table 8 classical comparison | Thirty policy checkpoints, seeds 2–31; `benchmarks/ext30/classic12_bo{1,64,1024}_*.csv` | Thirty rules; `benchmarks/classic12_arm_bon/gp_tuned_seed*.csv` | Yes: the same sets of thirty artifacts |
| One-pass 30-versus-30 comparison | Greedy records for policy seeds 2–31 combined by `enfrenta_gp_treinta.py` | `gp_tuned_seed1` through `gp_tuned_seed30` in `summary.csv` | Not a budget curve; all thirty artifacts are included |

For Table 8, the ordinary entries are means over the same thirty artifacts at every budget. The bracketed entries are per-instance minima over those thirty artifacts. They are therefore symmetric across methods but constitute a virtual per-instance oracle; no single policy or rule attains the complete bracketed row.

The selected-policy artifact was chosen on the six validation instances at \(B=64\). The selected GP rule was originally featured based on all seventy instances, although selecting it on the same six validation instances returns the same rule. This makes the realized comparison unaffected, but the ex ante selection protocols are not identical.

### i. Numerical spot checks

Running `paper/verify_numbers.py` produced:

> 825 checks passed, 0 failed, 4 pending source checks.

The four pending items concern absent source/package artifacts rather than numerical contradictions. I additionally traced the following printed values:

1. **G&T-MWKR, all 70 instances: 29.5%**  
   `paper/verify_numbers.py:135-136` reads the corresponding rows of `benchmarks/all_baselines.csv`; the unrounded mean is 29.48%.

2. **Selected GP, one pass: 17.71%**  
   `paper/verify_numbers.py:1792-1797` filters seed 1 in `benchmarks/reevo_fixedfit/summary.csv`; the recomputed mean is 17.7142%.

3. **Selected policy, \(B=64\): 15.02%**  
   The verifier combines the seed-5 campaign records in `benchmarks/ext30/camp_bo64_*.csv`; the 70-instance mean is 15.0226%.

4. **Selected policy, \(B=1024\): 13.25%**  
   The analogous `camp_bo1024_*.csv` records yield 13.2475%.

5. **Width-aware \(\lambda=1\) arm: 12.18% relative width and 15.11% RE**  
   `paper/verify_numbers.py:2987-3009` recomputes these from the rollout deposits under `benchmarks/robust_lambda/`; the underlying means are 12.1788% and 15.1093%.

I found no discrepancy among the checked values.

## 4. Experimental design and fairness of the DRL-versus-GP comparison

The comparison is stronger than most DRL-versus-heuristic studies in several respects. Both methods use the same interval instances, schedule builder, interval arithmetic, lexicographic retention criterion, and number of constructed schedules. Both receive one deterministic construction plus \(B-1\) stochastic constructions. The sampled comparisons therefore match schedule-count budgets rather than giving the policy sampling unavailable to the rule.

The comparison nevertheless matches inference counts, not computational effort. The two stochastic generators differ inherently: the policy samples its categorical action distribution, whereas the GP rule uses \(\epsilon\)-greedy randomization. Their per-schedule costs also differ, and 1024 policy samples are expensive. The manuscript provides timing information and does not conceal this distinction.

Training is not budget-matched. The thirty policy and thirty GP artifacts follow their respective studies’ training procedures, with approximately 4.4 versus 16 hours reported in Table 6. The paper correctly describes this as accounting rather than parity. Consequently, the results support statements about the supplied trained systems under matched inference budgets, not about sample efficiency under equal total compute.

Selection is mildly asymmetric: the policy champion is selected on validation, while the GP study’s featured rule was selected over the 70-instance set. The same GP rule is selected by validation, so no numerical advantage arises in this particular data set, but a future comparison should specify a common selection protocol prospectively.

The strongest conclusions should be stratified by size. On the sixty instances unseen by both families, neither sampled comparison is significant overall. The policy’s large-budget advantage is concentrated below \(50\times15\), while GP remains better on the two largest classes. The manuscript reports this clearly. Likewise, comparisons with fEABC are useful for positioning but are not shared-harness or matched-compute comparisons.

## 5. Reproducibility

The submission is exceptionally strong as a numerical audit package. Primary CSV/JSON records are extensive, the thirty main checkpoints are present under `outputs/`, all thirty GP rules are supplied, and the verifier checks hundreds of manuscript values. The headline training path is guarded against accidentally running the obsolete agent. Within the supplied Python environment, the verifier and analysis scripts execute.

A clean external reproduction is not yet possible from the workspace as delivered:

- `README.md:91-93` points to `zenodo_drl/code/requirements.txt`, but `zenodo_drl/` and any root-level dependency lock are absent.
- `README.md:83-87` instructs the reader to run `paper/compila.bat`, which is also absent.
- The classical-instance evaluators contain author-machine paths. In particular, `scripts/eval_classic12.py:31,119` hard-codes `E:\Experimentos\Selectos`; `eval_classic12_policy.py:39-51` searches an absent `zenodo_deposit/` directory and then the same external path, despite the instances being present under `instances/interval_classical/`.
- Running `pytest -q tests` yielded 205 passing tests and one failure: `tests/test_makespan_aggregation.py` imports the absent `transfer_experiment/decode.py`. Running `pytest -q` at repository root additionally fails during collection because `scripts/test_batched_train.py` interprets pytest’s `-q` argument as an integer.
- Artifact-to-result provenance is reconstructible, but it is spread across scripts and filename conventions. The selected checkpoint is not among the three convenience exports in `models/`; it is available only under `outputs/`.

Thus a reader can audit the supplied results and probably retrain the headline model after reconstructing the environment, but cannot presently execute the full workflow from a clean checkout using only the documented commands.

## 6. Presentation

The manuscript is technically careful and generally well written. Equations, algorithmic conventions, feature tables, and captions are unusually explicit. The rendered 37-page PDF is clean: I found no clipping, overlap, or illegible figures. The budget, frontier, robustness, and architecture figures are visually effective.

The main presentation weakness is density. Table 8 is readable but small and information-heavy, and several paragraphs combine result, qualification, provenance, and interpretation in long sentences. Some post-hoc implementation disclosures are essential but interrupt the narrative; a compact “implementation audit and artifact semantics” subsection could consolidate them.

The English is strong. Some source-code comments and script documentation remain primarily in Spanish, which is not a scientific validity issue but reduces accessibility for international readers.

## 7. MAJOR issues

1. **The width-aware retraining conclusions rely on runs whose inter-block transfer criterion did not implement the stated \(f_\lambda\).**  
   **Where:** Section 7.3, especially `paper/main.tex:1834-1845,1863-1886`; `jobshop_rl/agents_v2/agent.py:130-148`; `README.md:33-40`.  
   **What:** The deposited \(\lambda>0\) runs used the lower endpoint of the lexicographically largest job completion rather than \(\max_j C_j^L\). The manuscript says this “does not reach the figures” because evaluation loads the final block and recomputes the componentwise makespan. That is not sufficient: the erroneous key decides which earlier block supplies the weights for subsequent blocks, so it can alter the final-block initialization and final learned weights. The code comments explicitly acknowledge that corrected retraining may follow a different transfer chain and end with different weights.  
   **Why it matters:** The conclusion that retraining does not move the policy and that the width–makespan frontier arises “entirely at selection time” is precisely a conclusion about the learned weights. It is not securely supported by runs whose weight-transfer path was selected using a different objective. This does not affect the default \(\lambda=0\) results.  
   **Resolution:** Retrain all \(\lambda>0\) arms with the corrected componentwise key, recompute the common-deposit analysis and Figure 9, and revise the conclusion if needed. At minimum, report corrected-versus-legacy transfer chains and demonstrate empirically that the final results are insensitive to the bug.

2. **The precise budget-curve crossing is estimated asymmetrically and is more certain in the prose than the data support.**  
   **Where:** Section 7.2 and Figure 7, particularly `paper/main.tex:1630-1665`; `scripts/analiza_curva_intervalo.py:82-103`; `scripts/make_budget_curve_figure.py:145-162`.  
   **What:** Each policy point averages 200 random subsets for each of ten trained artifacts, with a band over artifacts. The GP point uses a single nested prefix from one stochastic pool for one selected rule, without repeated subsets, independent pools, or an uncertainty band.  
   **Why it matters:** The claims that the policy draws level specifically at \(B=96\), is only 0.13 points behind at \(B=64\), and remains within 0.05 points thereafter involve differences small enough to be sensitive to the single GP random stream. The schedule-count protocol is matched, but Monte Carlo precision is not.  
   **Resolution:** Generate multiple independent GP pools or apply the same repeated-subset reconstruction to a sufficiently large GP pool, quantify uncertainty for both curves, and report a distribution or interval for the crossing budget. Otherwise, restrict the claim to the coarser conclusion that parity occurs somewhere between the tested budget regimes.

3. **The supplied package is auditable but not self-contained or cleanly executable.**  
   **Where:** `README.md:83-93`; `scripts/eval_classic12.py:31,119`; `scripts/eval_classic12_policy.py:39-51`; `tests/test_makespan_aggregation.py:79`; `scripts/test_batched_train.py`.  
   **What:** The documented dependency file and compilation script are missing; classical evaluators depend on author-specific paths; and the test suite does not pass from the documented repository root.  
   **Why it matters:** Table 8 and parts of the end-to-end reproduction cannot be regenerated by a reader from the supplied workspace, despite the data-availability claim in Section “Data availability.”  
   **Resolution:** Include a pinned environment specification, repair all paths to use the provided `instances/interval_classical/`, supply a single scripted table/figure reproduction workflow, include or remove the missing transfer test dependency, and make `pytest` pass from repository root in a clean checkout.

## 8. MINOR issues

1. Rename or clarify the “local improvement” reward in Section 4.1. Its positive branch is unreachable because projected upper makespan is monotone; all nonzero changes use \(\kappa=2\).

2. Remove the dead \(\gamma=0.99\) setting from `jobshop_rl/main.py:265` or pass \(\gamma=1\) explicitly through the V2 factory. The effective implementation is correct, but the current configuration is easy to misread.

3. Explicitly label the bracketed Table 8 entries as a per-instance oracle over thirty artifacts. They are symmetric and useful descriptively, but they are not the performance of any deployable policy or rule.

4. Supplement the many Wilcoxon \(p\)-values with paired effect sizes and confidence intervals, and provide a multiple-testing sensitivity analysis. This is particularly important for the sequences of six-instance tests where the minimum nonzero two-sided exact \(p\)-value is 0.03125.

5. Record checkpoint paths or hashes and GP rule hashes directly in evaluation CSV metadata. Current provenance can be reconstructed, but only by following filename conventions across several scripts.

6. The raw-time transfer rule in Section 5.4 is faithfully disclosed but poorly motivated because values from different instances are incomparable. A small comparison against normalized gap-based transfer would help determine whether this historical convention materially affects the result.

7. Move runnable benchmark scripts named `test_*.py` out of pytest’s collection path, or make their argument parsing conditional on direct execution.

8. Consider moving detailed per-instance classical results and some provenance discussion to the supplementary material to reduce the density of the main manuscript.

## 9. Overall recommendation

**Major revision.**

The main interval arithmetic, reward, architecture, training-artifact semantics, best-of-\(N\) evaluator, statistical aggregation, and printed numerical results are internally consistent. The study is significant for EAAI, unusually transparent, and substantially stronger than a typical DRL scheduling submission in its numerical auditability.

However, the historical componentwise-makespan bug directly weakens the central causal conclusion of the width-aware retraining study; the precise policy–GP budget crossing lacks symmetric Monte Carlo support; and the delivered code package is not yet self-contained. These issues are important but repairable. Corrected robust-arm runs, a symmetric budget-curve analysis, and a clean executable release would make the paper a strong candidate for publication.