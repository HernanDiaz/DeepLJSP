"""
Executional robustness by Monte Carlo simulation.

For a schedule built by a rule with a fixed processing order, K realizations
of the durations are drawn uniformly and independently within their intervals
and the fixed order is executed under each realization (vectorized decoder).
The reported measure is the mean relative deviation of the executed makespan
from the predicted expected makespan:

    eps_bar = mean_k |Cmax_ex_k - E[Cmax]| / E[Cmax]

Since version 2.0 the same realizations also give tail measures: the
value-at-risk and conditional value-at-risk, at level alpha = 0.95, of
the overrun Cmax_ex - E[Cmax] and of the executed makespan itself.

Common random numbers: the scenario cloud of each instance is seeded by the
instance's position in the sorted instance list, so every method sees the
same realizations and comparisons are paired.
"""

from typing import Dict, List

import numpy as np

from .env import make_env
from .heuristics import HeuristicStrategy
from .interval import Interval

K_DEFAULT = 1000


def sample_durations(lo, up, K, rng):
    """dur[j][k] = array (K,) uniform in [lo[j][k], up[j][k]]."""
    return [[rng.uniform(lo[j][k], up[j][k], K) for k in range(len(lo[j]))]
            for j in range(len(lo))]


def decode_mc(seq, dur, machine_seq, K):
    """Array (K,) of makespans of the sequence over the K scenarios."""
    nj = len(dur)
    nm = len(machine_seq[0])
    job_end = [np.zeros(K) for _ in range(nj)]
    mach_end = [np.zeros(K) for _ in range(nm)]
    op_idx = [0] * nj
    for j1 in seq:
        j = j1 - 1
        k = op_idx[j]
        m = machine_seq[j][k]
        start = np.maximum(job_end[j], mach_end[m])
        end = start + dur[j][k]
        job_end[j] = end
        mach_end[m] = end
        op_idx[j] = k + 1
    return np.maximum.reduce(job_end)


def _bounds(problem: Dict):
    durs = problem["durations"]
    lo = [[float(d.lower) if isinstance(d, Interval) else float(d) for d in r]
          for r in durs]
    up = [[float(d.upper) if isinstance(d, Interval) else float(d) for d in r]
          for r in durs]
    return lo, up


def executed_makespans(heuristic: HeuristicStrategy,
                       problems: Dict[str, Dict],
                       K: int = K_DEFAULT,
                       seed_offset: int = 0):
    """{instance: (E[Cmax], array (K,) of executed makespans)}.

    Instances are processed in sorted-name order; the RNG of instance i is
    seeded with 1000*(i + seed_offset), so every method sees the same
    realizations. With the default offset this reproduces the arm-level
    measurement (eps_por_regla.csv). The realization-law and tail-risk
    experiments indexed a list that also held the ten 100x20 Taillard
    instances, which sort first and, having no reference bound, were
    skipped: they are reproduced with seed_offset=10."""
    names: List[str] = sorted(problems)
    out = {}
    for i, name in enumerate(names):
        problem = problems[name]
        lo, up = _bounds(problem)
        mseq = problem["sequences"]
        env = make_env(problem, seed=0)
        state = env.reset()
        done = False
        seq = []
        while not done and state["eligible_ops"]:
            f = env.get_features(state)
            a = min(heuristic.select_action(state["eligible_ops"], f),
                    len(state["eligible_ops"]) - 1)
            seq.append(env.eligible_ops[a] + 1)
            state, _, done, _ = env.step(a)
        c = env.job_completion_time
        e_mid = (max(x.lower if isinstance(x, Interval) else x for x in c) +
                 max(x.upper if isinstance(x, Interval) else x for x in c)) / 2
        rng = np.random.default_rng(1000 * (i + seed_offset))
        dur = sample_durations(lo, up, K, rng)
        out[name] = (e_mid, decode_mc(seq, dur, mseq, K))
    return out


def eps_bar_of_rule(heuristic: HeuristicStrategy,
                    problems: Dict[str, Dict],
                    K: int = K_DEFAULT) -> float:
    """Mean eps_bar of the heuristic over a dict of instances."""
    vals = [float(np.mean(np.abs(cmax - e_mid) / e_mid))
            for e_mid, cmax in executed_makespans(heuristic, problems,
                                                  K).values()]
    return sum(vals) / len(vals)


def tail(x, alpha: float = 0.95):
    """Empirical (VaR, CVaR) of the sample x at level alpha: the
    ceil((1 - alpha) K)-th largest value and the mean of the
    ceil((1 - alpha) K) largest ones."""
    x = np.sort(np.asarray(x))
    k = int(np.ceil((1.0 - alpha) * len(x)))
    return float(x[-k]), float(x[-k:].mean())


def overrun_cvar_of_rule(heuristic: HeuristicStrategy,
                         problems: Dict[str, Dict],
                         K: int = K_DEFAULT,
                         alpha: float = 0.95,
                         seed_offset: int = 0) -> Dict[str, float]:
    """{instance: CVaR_alpha of Cmax_ex - E[Cmax]}, in time units: the mean
    overrun of the executed makespan beyond its prediction over the
    (1 - alpha) worst realizations."""
    return {name: tail(cmax - e_mid, alpha)[1]
            for name, (e_mid, cmax) in executed_makespans(
                heuristic, problems, K, seed_offset).items()}
