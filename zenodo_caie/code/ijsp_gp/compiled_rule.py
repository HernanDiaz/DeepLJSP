"""
An evolved rule compiled into a single Python function, and its sampled
variant stopped by time.

``simulate.dispatch`` with ``simulate.policy_from_tree`` computes all nine
terminals of every eligible operation at each step and evaluates the tree
node by node over lists. Here the tree is translated into source code and
a dispatcher is generated that

  * keeps, per job, the terminals of its next operation (PT, PTW, WKR,
    WKRW, NOR and the machine) and updates them only for the job just
    dispatched, since those of the other jobs do not change;
  * at each step computes the earliest starts of the eligible operations
    and the value of the tree, written as a single expression, with list
    comprehensions, and dispatches the first minimum;
  * computes only the terminals the tree reads.

The result is identical to ``dispatch(inst, policy_from_tree(tree))``: the
same floating-point operations in the same order (protected division
included), the same tie-breaking (the first eligible operation, as
``min`` and ``list.index`` scan) and the same use of the random generator
when ``eps > 0``, so the sampled rule draws the same schedules with the
same seed. ``test_equivalence.py`` checks it.

This is the implementation of the rule used in the budget comparison of
the article (Section 6.5).
"""

import random
import time
from typing import Iterable, Optional

from .simulate import TERMINALS, Instance, better

# each terminal for eligible job j; a and b are its lower and upper
# earliest start, and base the minimum of b over the eligible operations
_TERMINAL = {
    "PT": "pt_[j]",
    "PTW": "ptw_[j]",
    "EST": "b",
    "ESTW": "(b - a)",
    "WKR": "wkr_[j]",
    "WKRW": "wkrw_[j]",
    "NOR": "nor_[j]",
    "SLACK": "(b - base)",
    "ONE": "1.0",
}
# how a stored terminal is recomputed when job j moves to its operation k;
# the same computations as simulate.dispatch
_UPDATE = {
    "PT": "pt_[j] = up[j][k]",
    "PTW": "ptw_[j] = up[j][k] - lo[j][k]",
    "WKR": "wkr_[j] = suf_up[j][k + 1]",
    "WKRW": "wkrw_[j] = suf_w[j][k + 1]",
    "NOR": "nor_[j] = float(m - k - 1)",
}


def _terminals(tree, used):
    if isinstance(tree, str):
        used.add(tree)
    else:
        for child in tree[1:]:
            _terminals(child, used)
    return used


def _expression(tree, count):
    """The tree as a single Python expression. Nodes that read an operand
    twice (min, max, div) name it with := so it is evaluated once."""
    if isinstance(tree, str):
        return _TERMINAL[tree]
    op = tree[0]
    x = _expression(tree[1], count)
    if op == "neg":
        return f"(-{x})"
    y = _expression(tree[2], count)
    if op in ("add", "sub", "mul"):
        return f"({x} {dict(add='+', sub='-', mul='*')[op]} {y})"
    count[0] += 1
    u, w = f"_x{count[0]}", f"_y{count[0]}"
    if op == "div":
        # the protected division of the evolution: abs(y) > 1e-9, else 1.0
        return (f"({x} / ({w} if (({w} := {y}) > 1e-9 or {w} < -1e-9)"
                f" else 1.0))")
    if op == "min":
        return f"({u} if ({u} := {x}) < ({w} := {y}) else {w})"
    if op == "max":
        return f"({u} if ({u} := {x}) > ({w} := {y}) else {w})"
    raise ValueError(op)


def source(tree) -> str:
    """The source code of the dispatcher of a tree."""
    used = _terminals(tree, set())
    unknown = used - set(TERMINALS)
    if unknown:
        raise ValueError(f"unknown terminals: {sorted(unknown)}")
    stored = [t for t in TERMINALS if t in _UPDATE and t in used]
    expr = _expression(tree, [0])
    uses_a = "ESTW" in used
    uses_b = bool(used & {"EST", "ESTW", "SLACK"})

    src = [
        "def dispatch(inst, return_order=False, eps=0.0, rng=None):",
        "    n, m, seq, lo, up = inst.n, inst.m, inst.seq, inst.lo, inst.up",
        "    suf_up, suf_w = inst.suf_up, inst.suf_w",
        "    jc_lo, jc_up = [0.0] * n, [0.0] * n",
        "    mc_lo, mc_up = [0.0] * m, [0.0] * m",
        "    op = [0] * n",
        "    perm = []",
        "    elig = list(range(n))",
        "    mach_ = [seq[j][0] for j in range(n)]",
    ]
    for t in stored:
        src.append(f"    {t.lower()}_ = [0.0] * n")
    if stored:
        src += ["    k = 0",
                "    for j in range(n):"]
        src += ["        " + _UPDATE[t] for t in stored]
    src += [
        "    for _ in range(n * m):",
        "        if eps > 0.0 and rng.random() < eps:",
        "            i = rng.randrange(len(elig))",
        "        else:",
    ]
    loop_vars = ["j"]
    if uses_b:
        src.append("            bs = [jc_up[j] if jc_up[j] > mc_up[mach_[j]]"
                   " else mc_up[mach_[j]] for j in elig]")
        loop_vars.append("b")
    if uses_a:
        src.append("            as_ = [jc_lo[j] if jc_lo[j] > mc_lo[mach_[j]]"
                   " else mc_lo[mach_[j]] for j in elig]")
        loop_vars.append("a")
    if "SLACK" in used:
        src.append("            base = min(bs)")
    lists = {"j": "elig", "b": "bs", "a": "as_"}
    if len(loop_vars) == 1:
        loop = "for j in elig"
    else:
        loop = (f"for {', '.join(loop_vars)} in "
                f"zip({', '.join(lists[v] for v in loop_vars)})")
    src += [f"            vs = [{expr} {loop}]",
            "            i = vs.index(min(vs))"]
    src += [
        "        j = elig[i]",
        "        k = op[j]",
        "        q = mach_[j]",
        "        a = jc_lo[j] if jc_lo[j] > mc_lo[q] else mc_lo[q]",
        "        b = jc_up[j] if jc_up[j] > mc_up[q] else mc_up[q]",
        "        jc_lo[j] = mc_lo[q] = a + lo[j][k]",
        "        jc_up[j] = mc_up[q] = b + up[j][k]",
        "        k += 1",
        "        op[j] = k",
        "        perm.append(j)",
        "        if k == m:",
        "            del elig[i]",
        "        else:",
        "            mach_[j] = seq[j][k]",
    ]
    src += ["            " + _UPDATE[t] for t in stored]
    src += ["    cm = (max(jc_lo), max(jc_up))",
            "    return (cm, perm) if return_order else cm"]
    return "\n".join(src) + "\n"


def compile_rule(tree):
    """Compile a tree into dispatch(inst, return_order=False, eps=0.0,
    rng=None), with the signature and the result of
    simulate.dispatch(inst, policy_from_tree(tree), ...)."""
    namespace = {}
    exec(compile(source(tree), "<compiled rule>", "exec"), namespace)
    return namespace["dispatch"]


def best_of_n(inst: Instance, dispatcher, seed: int, time_limit: float,
              eps: float = 0.1, checkpoints: Optional[Iterable[int]] = None):
    """The sampled rule (GP-best-of-N) of a compiled rule, stopped by time.

    Sample 0 is the deterministic pass; the others dispatch, with
    probability ``eps``, a uniformly chosen eligible operation. The curve
    records the incumbent makespan (lexicographic ranking) at every power
    of two of samples, or at the given ``checkpoints``, and at the last
    sample, with the elapsed seconds."""
    rng = random.Random(seed)
    marks = set(checkpoints) if checkpoints is not None else None
    t0 = time.time()
    best_cm = dispatcher(inst)
    curve, k = {1: (best_cm, time.time() - t0)}, 1
    while time.time() - t0 < time_limit:
        cm = dispatcher(inst, eps=eps, rng=rng)
        k += 1
        if better(cm, best_cm):
            best_cm = cm
        if (k & (k - 1) == 0) if marks is None else (k in marks):
            curve[k] = (best_cm, time.time() - t0)
    curve[k] = (best_cm, time.time() - t0)
    return curve
