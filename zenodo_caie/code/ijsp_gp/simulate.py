"""
Fast interval simulator shared by the rule, the sampled rule and the GA.

The budget comparison of the paper measures every method on one decoder
and one evaluator. This module is that decoder, written without building
the feature matrix at each decision: it dispatches with a priority rule
and it decodes a permutation with repetition of jobs, and both paths
produce exactly the semi-active schedule of ``env.py``.

Conventions, identical to ``env.py``:
  * eligible operations are listed in increasing job order;
  * WKR and NOR exclude the operation being scheduled;
  * SLACK is measured against the smallest upper earliest start among the
    eligible operations;
  * the makespan is component-wise, [max of lower, max of upper];
  * priority ties go to the first eligible operation, as with argmin.
"""

from typing import Callable, Dict, List, Tuple

from .interval import Interval

TERMINALS = ["PT", "PTW", "EST", "ESTW", "WKR", "WKRW", "NOR", "SLACK",
             "ONE"]


class Instance:
    """An instance unfolded into flat lists, ready to iterate over."""

    __slots__ = ("n", "m", "seq", "lo", "up", "suf_up", "suf_w", "ops")

    def __init__(self, problem: Dict):
        self.n = int(problem["num_jobs"])
        self.m = int(problem["num_machines"])
        self.seq = [[int(x) for x in row] for row in problem["sequences"]]
        self.lo, self.up = [], []
        for row in problem["durations"]:
            a, b = [], []
            for d in row:
                if isinstance(d, Interval):
                    a.append(float(d.lower))
                    b.append(float(d.upper))
                else:
                    a.append(float(d))
                    b.append(float(d))
            self.lo.append(a)
            self.up.append(b)
        # work remaining AFTER each operation, as suffix sums
        self.suf_up, self.suf_w = [], []
        for j in range(self.n):
            s, w = [0.0] * (self.m + 1), [0.0] * (self.m + 1)
            for k in range(self.m - 1, -1, -1):
                s[k] = s[k + 1] + self.up[j][k]
                w[k] = w[k + 1] + (self.up[j][k] - self.lo[j][k])
            self.suf_up.append(s)
            self.suf_w.append(w)
        # per job, its operations as (machine, lower, upper): all that the
        # permutation decoder reads
        self.ops = [[(self.seq[j][k], self.lo[j][k], self.up[j][k])
                     for k in range(self.m)] for j in range(self.n)]


def better(a: Tuple[float, float], b: Tuple[float, float]) -> bool:
    """Lexicographic ranking of the paper: upper bound first, then lower.
    True if interval makespan ``a`` is preferable to ``b``."""
    return a[1] < b[1] or (a[1] == b[1] and a[0] < b[0])


def decode(inst: Instance, perm: List[int]) -> Tuple[float, float]:
    """Decode a permutation with repetition of jobs.

    The k-th occurrence of job j is its k-th operation, so reading the list
    from left to right respects every job order without checks: one
    iterator per job over its operations is enough. The same sums and
    comparisons, in the same order, as dispatching with a rule."""
    n, m = inst.n, inst.m
    jc_lo, jc_up = [0.0] * n, [0.0] * n
    mc_lo, mc_up = [0.0] * m, [0.0] * m
    nxt = [iter(o) for o in inst.ops]
    for j in perm:
        q, d_lo, d_up = next(nxt[j])
        a, x = jc_lo[j], mc_lo[q]
        jc_lo[j] = mc_lo[q] = (a if a > x else x) + d_lo
        a, x = jc_up[j], mc_up[q]
        jc_up[j] = mc_up[q] = (a if a > x else x) + d_up
    return max(jc_lo), max(jc_up)


def dispatch(inst: Instance, priority: Callable[[Dict], int],
             return_order: bool = False, eps: float = 0.0, rng=None):
    """Build a schedule by dispatching with a priority rule.

    ``priority(terms)`` receives one list per terminal, one entry per
    eligible operation in eligible order, and returns the index to
    dispatch. The extra keys ``_MACHINE`` and ``_EST_LO`` are not terminals
    of the evolved rules; they let an external policy, such as the
    Giffler-Thompson conflict set, be built on the same decoder.

    With ``eps > 0`` an eligible operation is chosen uniformly at random
    with that probability: the GRASP-style randomization of GP-best-of-N.
    With ``return_order=True`` the permutation built is also returned.
    """
    n, m, seq, lo, up = inst.n, inst.m, inst.seq, inst.lo, inst.up
    suf_up, suf_w = inst.suf_up, inst.suf_w
    jc_lo, jc_up = [0.0] * n, [0.0] * n
    mc_lo, mc_up = [0.0] * m, [0.0] * m
    op = [0] * n
    perm = []
    for _ in range(n * m):
        elig = [j for j in range(n) if op[j] < m]
        if eps > 0.0 and rng.random() < eps:
            # a random choice needs no terminals
            i = rng.randrange(len(elig))
            j = elig[i]
            k = op[j]
            q = seq[j][k]
            a = jc_lo[j] if jc_lo[j] > mc_lo[q] else mc_lo[q]
            b = jc_up[j] if jc_up[j] > mc_up[q] else mc_up[q]
            jc_lo[j] = mc_lo[q] = a + lo[j][k]
            jc_up[j] = mc_up[q] = b + up[j][k]
            op[j] = k + 1
            perm.append(j)
            continue
        est_lo, est_up, pt, ptw = [], [], [], []
        wkr, wkrw, nor, mach = [], [], [], []
        for j in elig:
            k = op[j]
            q = seq[j][k]
            mach.append(q)
            a = jc_lo[j] if jc_lo[j] > mc_lo[q] else mc_lo[q]
            b = jc_up[j] if jc_up[j] > mc_up[q] else mc_up[q]
            est_lo.append(a)
            est_up.append(b)
            pt.append(up[j][k])
            ptw.append(up[j][k] - lo[j][k])
            wkr.append(suf_up[j][k + 1])
            wkrw.append(suf_w[j][k + 1])
            nor.append(float(m - k - 1))
        base = min(est_up)
        terms = {"PT": pt, "PTW": ptw, "EST": est_up,
                 "ESTW": [b - a for a, b in zip(est_lo, est_up)],
                 "WKR": wkr, "WKRW": wkrw, "NOR": nor,
                 "SLACK": [b - base for b in est_up],
                 "ONE": [1.0] * len(elig),
                 "_MACHINE": mach, "_EST_LO": est_lo}
        i = priority(terms)
        j = elig[i]
        k = op[j]
        q = seq[j][k]
        jc_lo[j] = mc_lo[q] = est_lo[i] + lo[j][k]
        jc_up[j] = mc_up[q] = est_up[i] + up[j][k]
        op[j] = k + 1
        perm.append(j)
    cm = (max(jc_lo), max(jc_up))
    return (cm, perm) if return_order else cm


def compile_tree(tree) -> Callable[[Dict], List[float]]:
    """Compile an expression tree into a function over Python lists.

    The arithmetic is operation by operation that of ``rules.eval_tree``,
    protected division included, so both give identical values; on
    eligible sets of a few dozen operations lists are much faster than
    NumPy arrays."""
    if isinstance(tree, str):
        key = tree
        return lambda t: t[key]
    op = tree[0]
    if op == "neg":
        f = compile_tree(tree[1])
        return lambda t: [-x for x in f(t)]
    f, g = compile_tree(tree[1]), compile_tree(tree[2])
    if op == "add":
        return lambda t: [x + y for x, y in zip(f(t), g(t))]
    if op == "sub":
        return lambda t: [x - y for x, y in zip(f(t), g(t))]
    if op == "mul":
        return lambda t: [x * y for x, y in zip(f(t), g(t))]
    if op == "div":
        return lambda t: [x / (y if abs(y) > 1e-9 else 1.0)
                          for x, y in zip(f(t), g(t))]
    if op == "min":
        return lambda t: [x if x < y else y for x, y in zip(f(t), g(t))]
    if op == "max":
        return lambda t: [x if x > y else y for x, y in zip(f(t), g(t))]
    raise ValueError(op)


def policy_from_tree(tree) -> Callable[[Dict], int]:
    """The dispatching policy of an evolved rule: the lowest value wins,
    ties to the first eligible operation."""
    f = compile_tree(tree)

    def policy(terms):
        v = f(terms)
        best_i, best_v = 0, v[0]
        for i in range(1, len(v)):
            if v[i] < best_v:
                best_i, best_v = i, v[i]
        return best_i
    return policy


def gt_policy(tie_break: Callable[[Dict, List[int]], int]):
    """Giffler-Thompson on this decoder: the operation of minimum upper
    completion, its machine's conflict set, and ``tie_break`` inside it.
    ``tie_break(terms, candidates)`` returns one of the candidate indices."""
    def policy(terms):
        fin = [e + p for e, p in zip(terms["EST"], terms["PT"])]
        c = min(range(len(fin)), key=lambda i: fin[i])
        mach = terms["_MACHINE"]
        cand = [i for i in range(len(fin))
                if mach[i] == mach[c] and terms["EST"][i] < fin[c]]
        if not cand:
            cand = [c]
        return tie_break(terms, cand)
    return policy


def gt_mwkr(terms, cand):
    """MWKR tie-break inside the conflict set."""
    return max(cand, key=lambda i: terms["WKR"][i])


def gt_tree(tree):
    """An evolved rule as the tie-break inside the conflict set."""
    f = compile_tree(tree)

    def tie_break(terms, cand):
        v = f(terms)
        return min(cand, key=lambda i: v[i])
    return tie_break
