# 1. Summary of the contribution

The manuscript presents a constructive PPO policy for the interval job shop scheduling problem (IJSP). At each dispatching step, the policy scores the next eligible operation of every unfinished job. Its observation consists of 16 dimensionless candidate features and 12 global features. A shared candidate encoder, permutation-invariant mean/max pooling, a global context network, and separate policy/value heads allow one network to process different numbers of jobs and machines. The policy is trained on four \(20\times15\) interval Taillard instances and evaluated without retraining on the full 70-instance benchmark and twelve intervalized classical JSP instances.

The empirical contribution is a comparison with a GP hyper-heuristic under a common scheduling harness and matched numbers of constructed schedules. The paper reports results at one, 64, and 1024 rollouts; examines cross-size and cross-family transfer; analyzes feature importance and attention; and studies whether interval width matters through input, training-data, and width-penalized-objective ablations. A further analysis measures executional deviation under sampled duration realizations. The submission is unusually rich in checkpoints, per-run records, rollout deposits, analysis scripts, and a numerical verification script.

# 2. Significance and novelty assessment for EAAI's audience

The problem is appropriate for *Engineering Applications of Artificial Intelligence*: it combines an established engineering scheduling problem, epistemic duration uncertainty, learned constructive heuristics, and deployment-cost considerations. The most valuable aspect is not a novel reinforcement-learning algorithm—the architecture is a competent application of Deep Sets and PPO—but the attempted controlled comparison between neural and symbolic learned dispatching policies, together with the investigation of where uncertainty enters their decisions.

The size-independent representation and broad zero-shot size evaluation are practically relevant. The manuscript also deserves credit for distinguishing inference sample count from wall-clock cost and for reporting negative results concerning attention and tuning. However, novelty should be framed primarily as the first carefully evaluated DRL application to this particular interval formulation and as an empirical DRL-versus-GP comparison. Deep Sets, PPO, sampled decoding, and the individual state/reward components are incremental in themselves.

At present, the significance is compromised by a material mismatch between the reward described in the manuscript and the reward passed by the training entry point that produced the named campaign artifacts. There is also a protocol mismatch in the best-of-\(N\) budget-curve analysis. These are not cosmetic reproducibility defects: they affect the stated method and some mechanistic conclusions.

# 3. Technical soundness

## 3.1 Reward formulation

The implementation does contain the six components stated in Section 4.1:

- terminal makespan;
- progress;
- idle time;
- local improvement;
- remaining-job criticality;
- machine-completion balance.

Their weighted sum is implemented by `AdaptiveRewardStrategy.calculate_reward` (`jobshop_rl/rewards/strategies/adaptive.py:72-81`), with the weights applied inside the components. The component formulas mostly match the manuscript:

- `MakespanRewardComponent` uses the upper endpoint by default and \(C^U+\lambda(C^U-C^L)\) for the robust arm (`makespan.py:46-59,77-113`).
- Idle time is conditionally computed using lexicographic predecessor comparison, and interval subtraction makes its upper endpoint \(s^U-c^L_\mu\) (`idle_time.py:78-103`; `interval.py:115-125`).
- Local deterioration is multiplied by two (`local_improvement.py:91-106`).
- Criticality uses upper remaining work (`criticality.py:77-99`).
- Balance uses the standard deviation of positive upper completion times (`balance.py:74-86`).

The scale floors described as dormant are present: `max(100,LB/10)` for terminal/local makespan, `max(10,2\bar p)` for idle time, `max(50,W^U/(2n))` for criticality, and `max(10,1.5\sigma(L^U))` for balance. For the benchmark sizes, the verifier reports these floors as non-binding.

There is, however, a major reward-configuration discrepancy. Section 4.1, lines 621-701, describes effective weights approximately

\[
(1.0,\;0.24,\;0.10,\;0.10,\;0.26,\;0.15)
\]

for makespan, idle, criticality, balance, progress, and local improvement. `AdaptiveConfigGenerator.generate_reward_config` can indeed generate these values (`jobshop_rl/utils/problem_analyzer.py:436-471`). But the actual batch entry point explicitly supplies a different vector:

```text
makespan 1.0, idle 0.15, critical 0.05,
balance 0.15, progress 0.05, local 0.30
```

at `jobshop_rl/main.py:251-260`. Because explicit nonempty parameters bypass the generator (`jobshop_rl/experiments/factory.py:121-143`), and `AdaptiveRewardStrategy._adapt_weights` subsequently changes balance to 0.10, the effective weights produced by this training route on TA11–TA14 are:

```text
(1.0, 0.15, 0.05, 0.10, 0.05, 0.30).
```

I instantiated all four training environments and obtained exactly that vector for each. The campaign directories encode commits such as `012ecd2`, `6de2c20`, and `871154c`; inspection of those revisions shows the same explicit vector in the batch route. Thus the verifier’s check at `paper/verify_numbers.py:2026-2035` verifies the generator in isolation, not the configuration used to produce the checkpoints.

Two smaller formula discrepancies also exist:

- `ProgressRewardComponent` returns zero on the terminal transition (`progress.py:31-37`). Its episode sum is therefore \((nm-1)/(nm)\), not one as stated at paper lines 635-640.
- `LocalImprovementRewardComponent` returns zero on the first transition because its previous makespan is initially `None` (`local_improvement.py:75-105`). The paper’s equation does not state this initialization convention.

Moreover, with \(\gamma=1\) and a fixed \(nm\)-step horizon, the constant progress return is action-independent. It may assist value fitting, but it cannot by itself prefer one complete processing order over another. Calling it policy-shaping progress should therefore be qualified.

The PPO discount factor is correctly \(1.0\): it is the default in `AgentV2` and `PPOTrainerV2` (`agent.py:28-50`; `ppo_trainer.py:44-59`), and the V2 factory leaves that default unchanged (`experiments/factory.py:173-198`).

## 3.2 Interval arithmetic and lexicographic criterion

Equations (1)–(3) are correctly represented in the main environment:

- Interval addition is componentwise (`interval.py:86-102`).
- `Interval.max` computes \([\max L,\max U]\), not a lexicographic maximum (`interval.py:128-171`).
- Interval comparisons use the tuple \((U,L)\) (`interval.py:207-246`).
- Environment start times use `Interval.max` (`job_shop_env.py:244-251`).
- Partial and final makespans use componentwise aggregation (`job_shop_env.py:277-300`; `interval.py:407-422`).

The standalone evaluators also compute the componentwise final makespan and retain rollouts using `(upper, lower)` (`scripts/eval_val_brazos.py:80-85,159-167`; `scripts/eval_treinta_semillas.py:96-98,145-153`). This part of the headline evaluation is sound.

One robust-arm defect remains. `AgentV2._episode_makespan` uses Python’s built-in `max` over interval job completions (`agent.py:121-135`). That selects the interval belonging to the job with the largest lexicographic endpoint rather than the componentwise final interval. Its upper endpoint is still correct, so the default \(\lambda=0\) arm is unaffected, but its lower endpoint—and hence \(C^U+\lambda(C^U-C^L)\)—can be wrong when \(\lambda>0\). The robust training/model-selection path should use `final_makespan`.

The notation \(E[\mathbf C_{\max}]=(C^L_{\max}+C^U_{\max})/2\) in Eq. (4) should also be reconsidered. Under an interval-only model this is the interval midpoint, not a mathematical expectation. Even under independent uniform operation durations, the expectation of a maximum is generally not the midpoint of the endpoint makespans. The computations remain usable as the field’s midpoint proxy, but “expected makespan” and “calibration” overstate its probabilistic meaning.

## 3.3 Size-invariant architecture

The architecture claims are verified.

- The encoder declares 16 operation features and 12 global features (`state_encoder.py:17-18`) and produces arrays of those dimensions (`state_encoder.py:98-159`).
- Temporal features are normalized by the internal worst-case lower bound (`state_encoder.py:44-49`).
- The network applies the same \(16\to128\to128\) encoder to every eligible operation, pools by masked mean and max, concatenates the resulting 256 values with 12 global values, and feeds the 268-dimensional vector through the context network (`networks.py:62-76,93-111`).
- The policy head reads each candidate embedding and the common context; the value head reads only the context.
- Padding is excluded from both pooling operations.
- With no attention blocks, the parameter count is exactly 120,322, agreeing with Table 3 and `paper/verify_numbers.py:903`.

The architecture is permutation-equivariant at the candidate-scoring level and permutation-invariant in its pooled context, with no parameter dimension tied to \(n\) or \(m\). The empirical zero-shot size claim is therefore architecturally credible.

## 3.4 Training protocol and deployed artifact

The unusual block-transfer rule in Section 5.4 is implemented as reported. `BatchExperimenter` trains one instance at a time, creates a new agent for each later block, and copies weights from the block with the smallest raw best makespan (`batch_experimenter.py:110-149,192-197`). It saves the current network at the end of every block and serializes `best_agent` as `best_model.pt` (`batch_experimenter.py:157-169,220-224`). `AgentV2.save_checkpoint` serializes the current network, not `best_model_state` (`agent.py:259-266`). Thus the paper is correct that the deployed checkpoint is the end-of-block network rather than the weights stored when the best individual episode was observed.

There is nevertheless an inconsistent secondary evaluation path: `BatchExperimenter.evaluate_on_test_set` preferentially restores `agent.best_model_state` (`batch_experimenter.py:299-308`). Therefore, running the main batch command and reading its immediate `test_results.csv` evaluates the best-episode snapshot, whereas loading `best_model.pt` in the standalone evaluators evaluates the stated end-of-block artifact. The manuscript’s main tables now use the latter, but the package exposes two different meanings of “evaluate the trained agent.” This should be removed or explicitly separated.

Creating each new environment and V2 agent also reseeds the global generators with the same training seed (`job_shop_env.py:62-64`; `agent.py:35`). Consequently, every block restarts the random-number streams rather than continuing one stream across the curriculum. This is reproducible but should be disclosed because the seed controls more than merely the run-level initialization.

## 3.5 Best-of-\(N\) inference

The two requested standalone evaluators implement the stated deployed protocol: one greedy rollout, \(N-1\) categorical samples, and lexicographic selection. They seed sampled rollout \(i\) with `1000+i`, identically across training artifacts. The reported primary one/64/1024 results are therefore reproducible from those files and checkpoints.

The budget-ablation analysis in Section 7.2 does not implement the same protocol. `scripts/eval_curva_diez.py:53-75,103-116` records only the componentwise midpoint of each rollout, discarding both endpoints. `scripts/analiza_curva_diez.py:81-97` then:

1. excludes the stored greedy rollout from each best-of-\(B\) pool;
2. samples \(B\) stochastic rollouts from the 341 sampled ones; and
3. retains the smallest midpoint, not the lexicographically smallest \((U,L)\).

Thus the claims that the deployed policy overtakes greedy at \(B=3\), overtakes GP at \(B=8\), and gains specified amounts per doubling are measurements of a different decoder. This is particularly important because a lexicographically preferable schedule can have a worse midpoint; two such cases are visible even in the 70 champion best-of-64 records. The raw budget deposits cannot repair the analysis because they do not retain lower and upper endpoints.

## 3.6 Statistical convention

The requested ablation scripts follow the stated convention:

- `ablaciones_unificadas.py:60-65`;
- `ablaciones_treinta_bo64.py:55-61`;
- `ablaciones_sesenta.py:44-50`; and
- `analiza_lambda_diez.py:61-69,94-105`

first average training seeds within each instance and then apply a two-sided `wilcoxon(..., method="exact")` to instance-level differences. The central DRL-versus-GP script likewise uses the instance as the unit (`scripts/enfrenta_gp_treinta.py:77-88,102-130`).

The statement that this convention governs *every* reported test is nonetheless false for the reward-weight confirmation in the supplementary material. `scripts/confirma_ganador_reward.py:150-160` creates 18 instance-seed differences and runs Wilcoxon directly on them, rather than averaging three seeds within each of six instances. It also transfers from the immediately preceding block (`lines 79-91`), not from the best block so far, so this confirmation does not reproduce the main training protocol. The supplementary claim at lines 86-105 that the reward campaign failed to improve the deployed weights is therefore not supported under the paper’s own statistical and training conventions.

The reported confidence intervals are ordinary \(t\)-intervals over instance differences, while significance is assessed nonparametrically. This is acceptable if stated explicitly, but the manuscript currently does not name the interval construction.

## 3.7 Numerical spot checks

I ran `paper/verify_numbers.py` and independently recomputed selected values from the benchmark CSV/JSON records:

1. The selected policy’s best-of-64 mean over 70 instances is **15.0226%**, from the 70 rows of `benchmarks/ext30/camp_bo64_*.csv`; this matches Table 7’s 15.0 and `paper/verify_numbers.py:1845,2171`.
2. The selected GP rule’s best-of-64 mean is **15.8845%**, from `benchmarks/fair_gp_eps.csv`; this matches Table 7’s 15.9 and the same verifier check.
3. Across the 30 policy runs, validation best-of-64 is **13.9181% ± 0.6000**, with champion seed 5 at **12.7668%**, from `benchmarks/ext30/eval_val_bo64*.csv`; this matches Section 6.1 and `paper/verify_numbers.py:2104-2123`.
4. For \(\lambda=1\), the common rollout deposits give width **13.0500% → 12.1788%**, with RE increasing by **1.1506 points** and exact \(p=0.03125\), matching Section 7.4 and `paper/verify_numbers.py:2831-2842`.
5. `benchmarks/tiempos_inferencia.csv` gives **66.1/64 = 1.0328 s** per \(20\times15\) policy sample and **408.4/64 = 6.3813 s** per \(50\times20\) sample, matching Table 9 and `paper/verify_numbers.py:3239`.

These spot checks support the printed numerical summaries. However, the advertised verification pass is not self-contained: after hundreds of checks it terminates with `FileNotFoundError` at `paper/verify_numbers.py:2324` because `paper/main.aux` is not supplied. Before terminating, it also emits a legacy failed check concerning “thirteen rejected modifications.” It therefore does not currently provide a clean all-numbers verification pass.

# 4. Experimental design and fairness of the DRL-vs-GP comparison

The evaluation side is substantially fair and unusually transparent:

- Both methods use the same instances and interval environment.
- Both output processing orders evaluated through the same componentwise schedule builder.
- Both retain schedules under the same lexicographic criterion.
- The compared inference budgets count constructed schedules.
- The paper explicitly states that schedule count is not wall-clock parity and measures the neural policy as approximately 7–11 times more expensive per sample.
- The asymmetric artifact-selection rules are disclosed, and the authors show that validation selection would choose the same GP rule.
- Thirty-artifact means are reported for the deterministic comparison, reducing dependence on the two selected representatives.

What is not matched should remain prominent:

- Training budgets and algorithms differ substantially: approximately 16 policy-hours versus 4.4 GP-hours for 30 artifacts.
- The supplied GP evolution code optimizes midpoint RE by default (`scripts/evolve_gp_rule.py:45-64,83-86`), whereas the policy’s terminal reward optimizes the upper endpoint. The shared criterion principally applies to schedule retention/evaluation, not to training.
- Neural sampling follows the learned categorical distribution, while GP sampling uses fixed \(\epsilon=0.1\) random dispatch. Equal schedule counts do not imply equal exploration strength.
- Sampled 64/1024 comparisons concern selected artifacts, whereas the full thirty-versus-thirty comparison is supplied only for deterministic inference.
- Published GA/ESABC/fEABC values are useful external yardsticks but are not matched-harness competitors.

These limitations do not make the comparison invalid; most are already acknowledged. It should be described consistently as matched evaluation opportunity under a schedule-count budget, not as end-to-end parity.

# 5. Reproducibility

Checkpoint re-evaluation is feasible. The instances, 128 output directories with checkpoints, 30 GP rules, primary benchmark records, and standalone evaluators are present. The evaluator logic is readable, deterministic, and produced the checked summary values.

Full reproduction from training is not yet adequately packaged:

- There is no README, requirements file, lockfile, environment specification, or single documented command sequence.
- The nominal batch entry point uses reward weights different from the manuscript.
- The immediate batch evaluator and standalone evaluator load different network states.
- Several scripts contain hard-coded paths to the author’s original `E:` workspace; for example `scripts/analiza_irace_reward.py:11`.
- `scripts/run_benchmark.py:45-48` contains a stale claim that zero-shot cross-size evaluation is impossible.
- `paper/verify_numbers.py` requires an omitted `.aux` file and crashes instead of reporting a final pass.
- No script in the supplied tree appears to generate `benchmarks/fair_gp_eps.csv`, although it is the primary source for the sampled GP rows in the main comparison.
- The budget-curve deposit omits endpoints needed to reproduce the stated lexicographic decoder.
- The exported `models/` directory contains only seeds 2–4 rather than the selected seed-5 artifact, although the latter can be recovered from `outputs/`.

A knowledgeable reader can reconstruct much of the workflow, but not by following a complete, documented, internally consistent reproduction recipe.

# 6. Presentation

The manuscript is generally well written. The problem formulation, separation of training/validation/unseen instances, interpretation of computational budgets, and limitations are clearer than in most learning-based scheduling submissions. Tables provide per-class and per-instance detail, and the architecture figure is supported by an exact layer table. The negative findings and post-hoc discovery of the curriculum rule are reported candidly.

The paper is nevertheless long and occasionally repeats conclusions across Results, Analysis, Limitations, and Conclusions. The distinction among “upper-endpoint objective,” “midpoint reporting metric,” “lexicographic selection,” and Monte Carlo execution should be summarized once in a compact table or schematic. This would prevent the current slippage between midpoint and expectation.

The source is still prepared for a different journal: `paper/main.tex:1-3` explicitly identifies the Springer Nature/JIM template rather than an Elsevier/EAAI format. The supplementary source similarly refers to fixed table numbers from that template. This is editorial rather than scientific, but it should be corrected before resubmission.

# 7. MAJOR issues

1. **The manuscript describes the wrong reward weights for the reported training campaigns.**  
   **Where:** Section 4.1, especially paper lines 621-701; `jobshop_rl/main.py:251-260`; `experiments/factory.py:121-143`; `rewards/strategies/adaptive.py:34-53`.  
   **Why it matters:** The reward is a central methodological contribution, and the uncertainty and tuning analyses are interpreted in terms of its components. The campaign route produces \((1,.15,.05,.10,.05,.30)\), not approximately \((1,.24,.10,.10,.26,.15)\). The verifier checks an unused generator path.  
   **Resolution:** Establish from archived commands/configurations exactly which vector trained every reported checkpoint; record that configuration with each artifact; revise Section 4.1 accordingly; and rerun any reward-tuning or mechanistic claim whose baseline was misidentified. Alternatively, retrain the headline arm under the stated reward.

2. **The best-of-\(N\) budget ablation does not use the deployed selection rule.**  
   **Where:** Section 7.2 and Figure 6; `scripts/eval_curva_diez.py:53-75,103-116`; `scripts/analiza_curva_diez.py:81-97`.  
   **Why it matters:** The analysis minimizes midpoint over sampled-only pools, while Section 5.4 defines one greedy plus \(N-1\) samples retained by \((U,L)\). Therefore the crossings at \(B=3\) and \(B=8\), and the marginal gains per doubling, do not characterize the deployed decoder.  
   **Resolution:** Regenerate the deposits with lower and upper endpoints, reconstruct exactly one greedy plus \(B-1\) samples, retain by \((U,L)\), and revise the figure and associated claims.

3. **The reward-weight tuning confirmation violates both the stated statistical unit and the main block-transfer protocol.**  
   **Where:** Supplementary material lines 86-105; `scripts/confirma_ganador_reward.py:79-91,150-160`; main paper lines 935-947 and 1043-1069.  
   **Why it matters:** The reported \(p=0.21\) is based on 18 instance-seed observations rather than six seed-averaged instance observations, and the tuned arm transfers from the immediately preceding block rather than the best block so far. This does not test the claimed configuration under the paper’s protocol.  
   **Resolution:** Repeat or reanalyze the confirmation with matched block transfer, identical artifact definition, and seeds averaged within instance before the exact Wilcoxon test.

4. **The robust objective uses an incorrect lower endpoint in an important training/model-selection path.**  
   **Where:** Eq. (8), Section 7.4; `jobshop_rl/agents_v2/agent.py:121-135`; contrast with `models/interval.py:407-422`.  
   **Why it matters:** Built-in `max` selects one job-completion interval, whereas final makespan requires componentwise maxima. The default upper-only arm is safe, but width-penalized \(f_\lambda\) can be wrong.  
   **Resolution:** Replace the built-in maximum with `final_makespan`, audit which robust checkpoints or selections were affected, and repeat affected training or artifact-selection stages.

5. **The public workflow evaluates two different deployed artifacts depending on entry point.**  
   **Where:** Section 5.4, lines 1061-1069; `batch_experimenter.py:299-308`; `agent.py:259-266`; standalone evaluators.  
   **Why it matters:** `best_model.pt` contains end-of-block weights, while `evaluate_on_test_set` restores the best-episode snapshot. A reader following the main batch pipeline will not evaluate the artifact the paper defines.  
   **Resolution:** Make artifact identity explicit in the API and filenames, remove the implicit restoration, and supply a single end-to-end reproduction command for each reported table.

6. **The “expected makespan” terminology lacks probabilistic justification.**  
   **Where:** Eq. (4), Sections 3, 6, 7.4, and 7.5.  
   **Why it matters:** The midpoint of a makespan interval is not generally \(E[C_{\max}]\). This affects the interpretation of relative error, width trade-offs, and “calibration,” although not the underlying arithmetic.  
   **Resolution:** Rename it the midpoint makespan or midpoint proxy throughout, or provide a probabilistic derivation justifying the expectation notation for the adopted uncertainty model.

7. **The reproduction package is not self-contained despite the strong data-availability claim.**  
   **Where:** Data Availability, paper lines 2066-2070; `paper/verify_numbers.py:2324`; absence of README/environment files; missing producer for `benchmarks/fair_gp_eps.csv`.  
   **Why it matters:** Independent checkpoint evaluation is possible, but clean retraining and end-to-end regeneration are not. The advertised verifier crashes and cannot certify its own final status.  
   **Resolution:** Add an environment/lockfile, top-level reproduction guide, archived commands and environment variables for every arm, a producer for every primary CSV, checksum/provenance metadata, and a verifier that exits successfully without omitted build intermediates.

# 8. MINOR issues

1. In Section 4.1, state explicitly that progress is omitted on the terminal transition and that local improvement is zero on the first transition, or change the code to match the equations.

2. Clarify that the constant progress term cannot alter complete-schedule ordering when \(\gamma=1\) and the horizon is fixed.

3. State that the random streams are reseeded at the start of every training block, not merely once per run.

4. Name the method used for the reported 95% confidence intervals; the scripts use parametric \(t\)-intervals over instance differences.

5. Provide a producer script or exact command for `benchmarks/fair_gp_eps.csv`; currently it is read but apparently never generated by the supplied scripts.

6. Correct the stale cross-size comment at `scripts/run_benchmark.py:45-48`, which contradicts the V2 architecture and the paper’s main result.

7. Export the selected seed-5 checkpoint under `models/` with an unambiguous filename, rather than requiring readers to locate it through campaign-specific `outputs/` paths.

8. In the supplementary material, lines 45-46 introduce “two configuration studies” but the text subsequently reports three campaigns.

9. The abstract’s claim that the policy improves on every hand-crafted rule on all 70 instances refers to the selected artifact. Adding “the validation-selected policy” would avoid implying that all 30 runs possess this property.

10. Update the manuscript and supplementary material from the Springer Nature/JIM class and comments to the Elsevier/EAAI submission format.

11. Remove author-side notes such as the pending generative-AI declaration comment at `paper/main.tex:2072-2074` from the archival source, after resolving the journal’s policy.

12. Reduce repetition in Sections 6–8 and add a compact summary distinguishing training objective, inference ranking, reporting metric, and executional metric.

# 9. Overall recommendation

**Major revision.**

The core empirical records are substantial and many headline numbers are independently traceable. The interval environment, size-invariant network, parameter count, standalone lexicographic evaluator, and main instance-level statistical analyses are largely sound. The paper also addresses a relevant EAAI problem and offers a potentially valuable DRL-versus-GP study.

Nevertheless, the reward specified as the method is not the reward configured by the campaign training route, the budget ablation analyzes a different decoder from the one claimed, and the reward-tuning confirmation violates the paper’s statistical and transfer conventions. Together with the robust-objective endpoint bug and incomplete reproduction workflow, these issues prevent acceptance in the current form. They appear repairable because the primary artifacts and records are extensive, but the revision must first establish an exact provenance chain from training command to checkpoint to evaluation record and then revise or rerun every affected claim.