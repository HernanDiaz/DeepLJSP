"""
Executional robustness by Monte Carlo simulation.

For a schedule built by a rule with a fixed processing order, K realizations
of the durations are drawn uniformly and independently within their intervals
and the fixed order is executed under each realization (vectorized decoder).
The reported measure is the mean relative deviation of the executed makespan
from the predicted expected makespan:

    eps_bar = mean_k |Cmax_ex_k - E[Cmax]| / E[Cmax]

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


def eps_bar_of_rule(heuristic: HeuristicStrategy,
                    problems: Dict[str, Dict],
                    K: int = K_DEFAULT) -> float:
    """Mean eps_bar of the heuristic over a dict of instances.

    Instances are processed in sorted-name order; the RNG of instance i is
    seeded with 1000*i, reproducing the paired scenario clouds used in the
    reported experiments."""
    names: List[str] = sorted(problems)
    vals = []
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
        rng = np.random.default_rng(1000 * i)
        dur = sample_durations(lo, up, K, rng)
        cmax = decode_mc(seq, dur, mseq, K)
        vals.append(float(np.mean(np.abs(cmax - e_mid) / e_mid)))
    return sum(vals) / len(vals)
