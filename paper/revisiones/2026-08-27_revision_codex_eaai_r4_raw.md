# 1. Summary of the contribution

The manuscript proposes a constructive PPO policy for the interval job shop scheduling problem. At each step, the policy selects the next eligible job operation, while the environment constructs a semiactive schedule using componentwise interval arithmetic. The state consists of 16 dimensionless features per eligible operation and 12 global features. A shared candidate encoder, permutation-invariant mean/max pooling, and policy/value heads yield a network whose parameter dimensions do not depend on the numbers of jobs or machines.

The experimental contribution is broader than the architecture itself. Thirty DRL training runs are compared with thirty evolved GP dispatching rules, using common benchmark instances and a shared evaluation harness. The paper studies one-pass and sampled best-of-\(N\) decoding, cross-size and cross-family generalization, feature importance, self-attention, interval-information ablations, width-penalizing objectives, computational cost, and execution under sampled realizations. The central empirical conclusion is that the GP rule is stronger for one deterministic construction, whereas the policy benefits more from sampling and overtakes it at larger inference budgets.

# 2. Significance and novelty assessment for EAAI’s audience

The application is well aligned with EAAI: it combines a real engineering optimization problem, uncertainty representation, neural combinatorial optimization, and a comparison with an established AI-based hyper-heuristic paradigm. The systematic treatment of inference budget is particularly valuable. Many DRL scheduling papers compare methods at poorly aligned computational effort; here, the authors at least match the number of constructed schedules and explicitly price the remaining wall-clock asymmetry.

The claimed first application of DRL to the IJSP appears plausible from the manuscript’s literature review, although this priority claim should remain qualified as “to the best of our knowledge.” Deep Sets, PPO, and sampled decoding are not individually novel. The novelty lies in their integration for interval scheduling, the detailed code-level account of the implemented training protocol, and the DRL–GP comparison. Subject to the inferential and reproducibility issues below, the work could make a useful application-oriented contribution.

# 3. Technical soundness

## a. Reward implementation

The six-component reward in Section 4.1 is substantially faithful to the implementation.

- `MakespanRewardComponent` uses the componentwise final makespan and its upper endpoint, with scale `max(100, LB/10)` (`jobshop_rl/rewards/components/makespan.py:32–45, 77–113`). The floor and the below-5% terminal bonus are disclosed in the manuscript as dormant on the reported instances.
- Progress is \(1/(nm)\) on nonterminal steps and zero on the terminal step (`progress.py:24–39`), as stated.
- The idle penalty selects the job predecessor using lexicographic interval comparison and obtains \(s^U-c_\mu^L\) as the upper endpoint of interval subtraction (`idle_time.py:78–103`).
- Local improvement uses changes in the upper endpoint and doubles deteriorations (`local_improvement.py:72–106`).
- Criticality sums the upper endpoints of the remaining operations (`criticality.py:73–99`).
- Balance uses the standard deviation of positive machine-completion upper endpoints, scaled by 1.5 times the standard deviation of total worst-case machine loads (`balance.py:31–45, 74–86`).

The actual batch entry point supplies nominal weights \((1,.15,.05,.15,.05,.30)\) (`jobshop_rl/main.py:251–260`). The adaptive layer lowers the balance weight to .10 on TA11–TA14 (`jobshop_rl/rewards/strategies/adaptive.py:56–70`), producing the effective vector reported in the paper. The alternative weight generator is bypassed on this route. AgentV2 sets \(\gamma=1\) (`jobshop_rl/agents_v2/agent.py:28–50`; `ppo_trainer.py:46–77`), even though obsolete V1-oriented parameters in `main.py` still show 0.99.

I therefore find Section 4.1 accurate for the main campaign.

## b. Interval arithmetic and lexicographic ranking

The core interval semantics are correct.

- Addition is componentwise and `Interval.max` computes \([\max L,\max U]\) (`jobshop_rl/models/interval.py:86–171`).
- Interval comparison is lexicographic on `(upper, lower)` (`interval.py:207–246`).
- `final_makespan` correctly applies componentwise aggregation across job completions (`interval.py:407–422`).
- Environment transitions use `Interval.max` for the job and machine predecessors (`jobshop_rl/environment/job_shop_env.py:245–263`) and report the final componentwise makespan (`job_shop_env.py:278–303`).
- Main-arm best-of-\(N\) retention uses `(upper, lower)` (`jobshop_rl/agents_v2/agent.py:140–153`).

These points agree with Eqs. 1–3 and avoid the common error of using Python’s built-in `max` as a makespan aggregator.

## c. Size-invariant architecture

The implementation supports the architectural claims.

- The encoder dimensions are exactly 16 per candidate and 12 global (`jobshop_rl/agents_v2/state_encoder.py:17–18`), and the feature definitions match Tables 1 and 2 (`state_encoder.py:69–159`).
- The network has the four stated trainable MLP blocks: candidate encoder, context MLP, policy head, and value head (`jobshop_rl/agents_v2/networks.py:62–76`).
- Mean and masked maximum pooling are implemented correctly (`networks.py:93–105`).
- The policy head receives the candidate embedding and context, while the value head receives context alone (`networks.py:107–112`).
- The parameter count is 120,322, including biases and LayerNorm parameters.

The overall policy is permutation-equivariant with respect to candidate order, while its pooled context is permutation-invariant. The manuscript body explains this correctly; the abstract’s phrase “encoder is permutation-invariant” is slightly imprecise.

## d. Training blocks, transfer, and deployed artifact

The unusual training protocol is accurately disclosed for the main arm.

`BatchExperimenter` creates a new agent for each block, loads weights from the currently best block, and resets the optimizer (`jobshop_rl/experiments/batch_experimenter.py:114–149`). Blocks are compared using raw `best_makespan`, even though they correspond to different instances (`batch_experimenter.py:182–197`). The checkpoint saved for each block contains the network at the end of that block, not the best-episode snapshot (`batch_experimenter.py:157–169`; `jobshop_rl/agents_v2/agent.py:280–287`). The supplied summaries confirm that TA14 is the lowest-raw-makespan block in all thirty main runs and that TA14 starts from TA12 rather than TA13 in 26 runs, as stated in Section 5.4.

There is, however, a second evaluation convention inside the batch pipeline: `evaluate_on_test_set` preferentially loads `best_model_state`, i.e. the within-block best-episode snapshot (`batch_experimenter.py:299–313`). The paper’s results instead use standalone evaluation of the serialized end-of-block checkpoint. README lines 58–62 acknowledge this, but it remains an important reproducibility trap.

A code–paper mismatch exists for the robust \(\lambda>0\) arms. Section 7.3, lines 1804–1815, states that the historical training key used the lower endpoint from the lexicographically largest job completion rather than the componentwise lower endpoint. The current `AgentV2._episode_makespan` instead calls the corrected `final_makespan` (`agent.py:121–138`). Thus the released code does not exactly recreate the training semantics of the reported robust runs.

## e. Best-of-\(N\) inference

The standalone evaluators implement the stated protocol:

- one deterministic greedy rollout;
- \(N-1\) categorical samples;
- retention by `(upper, lower)`;
- reporting by the midpoint.

This is explicit in `scripts/eval_val_brazos.py:66–84, 159–167` and `scripts/eval_treinta_semillas.py:82–98, 145–153`. Fixed evaluation seeds give common random numbers across trained policies. I found no mismatch in this part.

## f. Statistical convention

The analysis scripts generally implement the stated convention correctly. In the ablation scripts, common training seeds are identified, results are averaged over seeds within each instance, and the Wilcoxon test is then applied to instance differences; see, for example, `scripts/ablaciones_unificadas.py:55–74`, `ablaciones_treinta_bo64.py:54–78`, and `analiza_lambda_diez.py:90–105`. They request `method="exact"` and use two-sided tests by default.

The more serious problem is not the implementation of the test but the set of instances submitted to the headline tests. Section 5.1 defines TA11–TA14 as training and TA15–TA20 as validation (`paper/main.tex:945–954`), and the policy is selected on TA15–TA20 (`main.tex:1114–1118`). Nevertheless, the significance tests in Section 6.2 use all seventy instances, including those ten non-test instances (`main.tex:1337–1348`).

Using the supplied primary records, I repeated the selected-artifact comparisons on the sixty genuinely unseen Taillard instances:

| Budget | Policy RE | GP RE | Exact Wilcoxon \(p\) |
|---:|---:|---:|---:|
| 1 | 18.676 | 17.894 | 0.034 |
| 64 | 15.401 | 15.884 | 0.261 |
| 1024 | 13.585 | 14.079 | 0.230 |

Thus the statement that the learners “differ significantly at every budget” does not hold on the unseen Taillard test set. At sampled budgets the policy retains a lower mean, but the paired differences are not significant. This is a central inferential issue.

## g. Budget-curve reconstruction

The revised budget-curve scripts do implement the deployed decoding rule. `eval_curva_intervalo.py` stores one greedy rollout plus 341 sampled rollouts with both endpoints. `analiza_curva_intervalo.py:79–103` reconstructs budget \(B\) as the greedy rollout plus \(B-1\) samples drawn without replacement and retains the minimum by `(upper, lower)`. This corrects the older midpoint-only reconstruction described in its header.

The resulting curve—19.47% greedy, 15.34% at \(B=64\), 14.19% at \(B=341\), and crossing the GP one-pass level at \(B=6\)—is internally consistent. The Monte Carlo subsampling uses 200 repetitions, so intermediate points are estimates rather than exact enumeration; this is acceptable but should be stated in the figure caption.

Raw regeneration is not currently self-contained: `eval_curva_intervalo.py:45–59` looks for the final TA14 block checkpoint, whereas the reviewed `outputs/` extracts contain `best_model.pt` but not those per-block checkpoint filenames.

## h. Numerical spot checks

`paper/verify_numbers.py` completed with 803 successful checks, zero failures, and four checks marked pending because their external source files were absent. I additionally traced the following numbers to primary benchmark records:

- GP one-pass mean: 17.7142%, from the 70 `gp_tuned_seed1` rows in `benchmarks/reevo_fixedfit/summary.csv`.
- Selected policy at 64 rollouts: 15.0226%, from the 70 rows across `benchmarks/ext30/camp_bo64_1.csv` through `_6.csv`.
- GP at 64 rollouts: 15.8845%, from `benchmarks/fair_gp_eps.csv`.
- Midpoint-training ablation on thirty unseen instances: \(+0.4323\) RE points and exact \(p=0.04491\), reconstructed from the `benchmarks/ext30/c64_*.csv` files after averaging the ten seeds by instance.
- Policy execution deviation at best-of-64: \(5.4812\times10^{-3}\), from the three policy seeds in the 1,190-row `benchmarks/eval_eps_all70.csv`.

These agree with the corresponding checks around `paper/verify_numbers.py:1791–1862, 2496–2583, 3428–3466`.

# 4. Experimental design and fairness of the DRL–GP comparison

The evaluation side is unusually well controlled. Both methods use the same interval instances, lower bounds, schedule builder, componentwise makespan calculation, lexicographic retention key, numbers of constructed schedules, and—where execution is studied—the same duration realizations. One pass means deterministic decoding for both; sampled GP uses the companion study’s \(\epsilon\)-greedy rule, while the policy samples its categorical distribution.

Several quantities are deliberately not matched:

- wall-clock inference cost: the policy is approximately 7–11 times more expensive per schedule;
- training cost: roughly 16 versus 4.4 aggregate hours;
- training algorithm and budget;
- training objective: the policy’s terminal reward optimizes the upper endpoint, whereas `scripts/evolve_gp_rule.py:45–64` defaults to midpoint RE, and the main GP campaign does not override that default (`scripts/rerun_evolutions_fixedfit.py:52–59`);
- artifact selection: the policy is validation-selected, while the highlighted GP artifact was originally selected on the seventy instances, although the authors report that validation selection yields the same rule;
- artifact replication at sampled budgets: all thirty artifacts are compared only at one pass; the 64- and 1024-sample headline contrasts use one selected artifact per family.

The manuscript acknowledges the unmatched training budgets, wall-clock costs, and selection asymmetry. It should also state the different training objectives explicitly and avoid interpreting selected-artifact tests as evidence about the complete distributions of trained artifacts.

# 5. Reproducibility

Numerical auditability is excellent: primary CSV/JSON records are extensive, figures and tables can be regenerated, and the verifier is much stronger than is typical for this literature. The main-arm training route can also be identified from the code, provided the reader sets `DEEPLJSP_AGENT=v2`.

Exact end-to-end reproduction is nevertheless incomplete in the reviewed package:

- `README.md:82–84` points to `zenodo_drl/code/requirements.txt`, but that directory and any root dependency lock file are absent.
- `README.md:74–77` points to `paper/compila.bat`, also absent.
- `scripts/eval_treinta_semillas.py:47–59` hard-codes campaign timestamps and commit identifiers rather than accepting checkpoint paths.
- Several raw-evaluation scripts require per-block checkpoint files that are not present in the supplied `outputs/` extracts.
- I found no script that directly regenerates `benchmarks/fair_gp_eps.csv`, the primary 64/1024-sample GP record.
- A normal `pytest -q` invocation aborts during collection because `scripts/test_batched_train.py:32` interprets pytest’s `-q` as an integer. Running `pytest -q tests` gives 195 passes and 9 failures. Some failures are stale tests that contradict the now-documented behavior, but a published regression suite should still be green.
- The default package entry point selects AgentV1 unless an environment variable is set. README lines 15–19 warn about this, but making the paper’s agent an explicit CLI choice would be safer.

A reader can verify the printed results and rerun substantial portions of the evaluation, but cannot currently reproduce every primary record from clean commands and the supplied artifacts.

# 6. Presentation

The manuscript is technically literate, candid about implementation provenance, and generally written in strong English. The problem definition, reward decomposition, feature tables, architecture table, and discussion of what is and is not matched are clearer than in most DRL scheduling papers. Figures and tables are information-dense but useful.

At 36 single-column pages plus supplementary material, it is long. Some interpretive discussion—particularly repeated explanations of where interval width enters—could be compressed. The paper should also distinguish more consistently among “the selected policy,” “the selected GP rule,” and the broader DRL/GP artifact families. The current wording occasionally promotes selected-pair findings into conclusions about paradigms.

# 7. MAJOR issues

1. **The headline significance claim uses training and validation instances as test units.**  
   **Where:** Sections 5.1 and 6.2; `paper/main.tex:945–954, 1114–1118, 1337–1348`; abstract lines 87–93.  
   **Why it matters:** The policy was trained on four and selected on six of the ten \(20\times15\) instances included in the 70-instance test. On the sixty genuinely unseen instances, the sampled-budget differences are not significant (\(p=0.261\) at 64 and \(p=0.230\) at 1024). Therefore “significant at every budget” is not supported as an unseen-instance conclusion.  
   **Resolution:** Make the sixty unseen instances the primary Taillard test, report their effect sizes and tests, and treat the \(20\times15\) training/validation class descriptively. Revise the abstract and conclusions accordingly.

2. **The DRL–GP conclusion overgeneralizes selected-artifact results and leaves a material objective mismatch implicit.**  
   **Where:** Abstract lines 74–98; contribution 2 (`main.tex:209–220`); Sections 6.2 and 8; `scripts/evolve_gp_rule.py:45–64`; `scripts/rerun_evolutions_fixedfit.py:52–59`.  
   **Why it matters:** At sampled budgets the comparison is one policy against one rule, not thirty against thirty. Moreover, the policy is trained primarily against worst-case makespan, while the highlighted GP rules are evolved against midpoint RE. This is a comparison of two deployed systems, but it does not isolate model family.  
   **Resolution:** Either evaluate the thirty artifacts per family at the sampled budgets, or restrict the claims explicitly to the selected artifacts. Add a clear table of matched and unmatched training choices, including the objective, and ideally provide a GP control evolved against the policy’s upper-endpoint objective.

3. **The released robust-training code does not reproduce the implementation described for the reported robust arms.**  
   **Where:** Section 7.3, `main.tex:1804–1815`, versus `jobshop_rl/agents_v2/agent.py:121–138`.  
   **Why it matters:** The manuscript says the reported \(\lambda>0\) runs used a historically incorrect lower endpoint in the block-selection key; the current code uses corrected componentwise aggregation. Retraining from the release may therefore follow a different transfer path and produce different robust-arm weights. This affects one of the paper’s stated contributions.  
   **Resolution:** Archive the exact historical implementation or add an explicit compatibility option, record the code version in every checkpoint, and provide a test demonstrating which semantics reproduce the deposited runs. Alternatively, retrain the robust arms with the corrected code.

4. **The claimed reproducibility is stronger than the executable package currently supports.**  
   **Where:** Data-availability statement (`main.tex:2123–2128`), README lines 58–84, `eval_curva_intervalo.py:45–59`, and the test failures described above.  
   **Why it matters:** Numerical verification succeeds, but several primary campaigns cannot be regenerated because scripts reference absent per-block checkpoints or hard-coded run paths; the dependency and compilation files named by README are absent; the GP sampling record lacks a direct generator; and the test suite is not green.  
   **Resolution:** Supply a pinned environment file, an end-to-end reproduction manifest mapping every table/figure to commands and inputs, all required checkpoints, a generator for `fair_gp_eps.csv`, checkpoint-path CLI options, and a passing documented test command.

# 8. MINOR issues

1. In the abstract, replace “encoder is permutation-invariant” with wording that distinguishes the equivariant candidate encoder/policy from the invariant pooled context.

2. Use “interval midpoint” consistently instead of notation such as \(\mathbb{E}[C_{\max}]\), which suggests a probabilistic expectation despite the manuscript’s correct disclaimer that no distribution is assumed.

3. The \(p=0.045\) midpoint-training ablation is one of several related contrasts and would not be robust to many reasonable multiplicity adjustments. It should be described as borderline/exploratory rather than as a firm dichotomy.

4. State in the budget-curve caption that intermediate budget values are Monte Carlo expectations over 200 subsets, not exact enumeration (`scripts/analiza_curva_intervalo.py:34–36, 91–100`).

5. Replace the raw-best-makespan transfer rule with an instance-normalized criterion in future work. The present rule is faithfully disclosed, but its dependence on instance time scale is avoidable and complicates interpretation.

6. Reconcile or remove stale tests whose expectations contradict the documented terminal bonus and doubled local-deterioration penalty (`tests/test_rewards_intervals.py:63, 90, 229`).

7. The permutation-importance study uses only three training seeds and the validation instances. Its findings should remain explicitly diagnostic rather than inferential.

# 9. Overall recommendation

**Major revision.**

The core environment, reward, interval arithmetic, Deep Sets architecture, best-of-\(N\) decoder, and numerical records are technically credible and unusually well audited. The work is potentially publishable and relevant to EAAI. However, the principal claim of statistically significant DRL–GP separation at every budget is not supported on the sixty unseen Taillard instances, and the sampled-budget evidence concerns selected artifacts rather than the thirty-artifact families advertised in the contribution. Exact retraining of the robust arm and several raw evaluations is also not possible from the current executable package. These issues require substantial reanalysis, claim revision, and reproducibility repairs, but not a wholesale redesign of the proposed method.