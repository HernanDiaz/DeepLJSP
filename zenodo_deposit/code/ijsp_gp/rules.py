"""
Genetic-programming dispatching rules: expression trees over interval-aware
attributes of the eligible operations. The operation with the LOWEST priority
value is dispatched.

Trees are nested tuples ("op", child, ...) with string terminals, exactly the
representation stored in the rule JSON files of this deposit.
"""

import random
from typing import List

import numpy as np

from .heuristics import HeuristicStrategy

# ----------------------------------------------------------------------
# Terminals: vectors of length n_eligible derived from the feature matrix
# (interval layout: [.., .., .., dur_lo, dur_up, est_lo, est_up,
#  rem_lo, rem_up, nor]; the 7-column scalar layout duplicates bounds)
# ----------------------------------------------------------------------

TERMINALS = ["PT", "PTW", "EST", "ESTW", "WKR", "WKRW", "NOR", "SLACK", "ONE"]


def terminal_arrays(features: np.ndarray) -> dict:
    f = np.asarray(features, dtype=np.float64)
    if f.shape[1] >= 10:  # interval layout
        dur_lo, dur_up = f[:, 3], f[:, 4]
        est_lo, est_up = f[:, 5], f[:, 6]
        rem_lo, rem_up = f[:, 7], f[:, 8]
        nor = f[:, 9]
    else:  # scalar layout (7)
        dur_lo = dur_up = f[:, 3]
        est_lo = est_up = f[:, 4]
        rem_lo = rem_up = f[:, 5]
        nor = f[:, 6]
    return {
        "PT": dur_up,                      # worst-case processing time
        "PTW": dur_up - dur_lo,            # duration width
        "EST": est_up,                     # worst-case earliest start
        "ESTW": est_up - est_lo,           # start width
        "WKR": rem_up,                     # worst-case work remaining
        "WKRW": rem_up - rem_lo,
        "NOR": nor,                        # operations remaining
        "SLACK": est_up - est_up.min(),    # slack against the earliest start
        "ONE": np.ones(len(f)),
    }


# ----------------------------------------------------------------------
# Trees
# ----------------------------------------------------------------------

FUNCTIONS = {"add": 2, "sub": 2, "mul": 2, "div": 2, "min": 2, "max": 2, "neg": 1}


def eval_tree(tree, terms: dict) -> np.ndarray:
    if isinstance(tree, str):
        return terms[tree]
    op = tree[0]
    if op == "neg":
        return -eval_tree(tree[1], terms)
    a = eval_tree(tree[1], terms)
    b = eval_tree(tree[2], terms)
    if op == "add":
        return a + b
    if op == "sub":
        return a - b
    if op == "mul":
        return a * b
    if op == "div":  # protected division
        return a / np.where(np.abs(b) > 1e-9, b, 1.0)
    if op == "min":
        return np.minimum(a, b)
    return np.maximum(a, b)


def tree_str(tree) -> str:
    if isinstance(tree, str):
        return tree
    op = tree[0]
    if op == "neg":
        return f"(-{tree_str(tree[1])})"
    sym = {"add": "+", "sub": "-", "mul": "*", "div": "/"}.get(op)
    if sym:
        return f"({tree_str(tree[1])} {sym} {tree_str(tree[2])})"
    return f"{op}({tree_str(tree[1])}, {tree_str(tree[2])})"


def tree_size(tree) -> int:
    if isinstance(tree, str):
        return 1
    return 1 + sum(tree_size(c) for c in tree[1:])


def random_tree(rng: random.Random, depth: int, full: bool, terminals=None):
    terminals = terminals if terminals is not None else TERMINALS
    if depth <= 0 or (not full and rng.random() < 0.3):
        return rng.choice(terminals)
    op = rng.choice(list(FUNCTIONS))
    arity = FUNCTIONS[op]
    return tuple([op] + [random_tree(rng, depth - 1, full, terminals)
                         for _ in range(arity)])


def _collect(tree, path=()):
    yield path, tree
    if not isinstance(tree, str):
        for i, child in enumerate(tree[1:], start=1):
            yield from _collect(child, path + (i,))


def _replace(tree, path, sub):
    if not path:
        return sub
    idx = path[0]
    parts = list(tree)
    parts[idx] = _replace(parts[idx], path[1:], sub)
    return tuple(parts)


def crossover(rng: random.Random, a, b):
    pa, _ = rng.choice(list(_collect(a)))
    _, sb = rng.choice(list(_collect(b)))
    return _replace(a, pa, sb)


def mutate(rng: random.Random, tree, depth: int = 3, terminals=None):
    path, _ = rng.choice(list(_collect(tree)))
    return _replace(tree, path, random_tree(rng, depth, full=False,
                                            terminals=terminals))


# ----------------------------------------------------------------------
# Drop-in heuristic wrapping an evolved rule
# ----------------------------------------------------------------------

class GPRuleHeuristic(HeuristicStrategy):
    """Dispatches the operation with the LOWEST priority under the tree."""

    def __init__(self, tree):
        self.tree = tree

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        if len(features) == 0:
            return 0
        priorities = eval_tree(self.tree, terminal_arrays(features))
        return int(np.argmin(priorities))


def load_rule(path: str) -> GPRuleHeuristic:
    """Load an evolved rule from one of the deposit's JSON files."""
    import json

    def as_tuple(node):
        if isinstance(node, list):
            return tuple(as_tuple(c) for c in node)
        return node

    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return GPRuleHeuristic(as_tuple(data["tree"]))
