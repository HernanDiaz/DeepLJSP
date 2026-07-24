"""
Hiper-heurística por programación genética: evoluciona reglas de despacho
como árboles de expresión sobre atributos interval-aware de las operaciones.

Línea de trabajo: Branke, Nguyen, Pickardt & Zhang (IEEE TEC 2016) —
"Automated Design of Production Scheduling Heuristics". Aquí en versión
mínima y autocontenida (sin dependencias externas): la regla asigna una
prioridad a cada operación elegible y se despacha la de MENOR prioridad.

Los terminales se calculan de la matriz de features estándar del entorno
(layout interval de 10 columnas), de modo que una regla evolucionada es un
drop-in de HeuristicStrategy sin acceso extra al entorno.

Módulo NUEVO: no modifica nada del código existente.
"""

import math
import random
from typing import List, Tuple

import numpy as np

from jobshop_rl.heuristics.strategies import HeuristicStrategy

# ----------------------------------------------------------------------
# Terminales: vectores (n_elegibles,) derivados de la matriz de features
# (layout interval: [.., .., .., dur_lo, dur_up, est_lo, est_up,
#  rem_lo, rem_up, nor]; para el layout escalar de 7 se duplican bounds)
# ----------------------------------------------------------------------

TERMINALS = ["PT", "PTW", "EST", "ESTW", "WKR", "WKRW", "NOR", "SLACK", "ONE"]


def terminal_arrays(features: np.ndarray) -> dict:
    f = np.asarray(features, dtype=np.float64)
    if f.shape[1] >= 10:  # layout interval
        dur_lo, dur_up = f[:, 3], f[:, 4]
        est_lo, est_up = f[:, 5], f[:, 6]
        rem_lo, rem_up = f[:, 7], f[:, 8]
        nor = f[:, 9]
    else:  # layout escalar (7)
        dur_lo = dur_up = f[:, 3]
        est_lo = est_up = f[:, 4]
        rem_lo = rem_up = f[:, 5]
        nor = f[:, 6]
    return {
        "PT": dur_up,                      # processing time (peor caso)
        "PTW": dur_up - dur_lo,            # anchura de la duración
        "EST": est_up,                     # earliest start (peor caso)
        "ESTW": est_up - est_lo,           # anchura del inicio
        "WKR": rem_up,                     # work remaining del job
        "WKRW": rem_up - rem_lo,
        "NOR": nor,                        # operaciones restantes
        "SLACK": est_up - est_up.min(),    # holgura frente a la más temprana
        "ONE": np.ones(len(f)),
    }


# ----------------------------------------------------------------------
# Árboles: tuplas anidadas ("op", hijo...) o terminales (str)
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
    if op == "div":  # división protegida
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
# Heurística drop-in con una regla evolucionada
# ----------------------------------------------------------------------

class GPRuleHeuristic(HeuristicStrategy):
    """Despacha la operación con MENOR prioridad según el árbol dado."""

    def __init__(self, tree):
        self.tree = tree

    def select_action(self, eligible_ops: List[int], features: np.ndarray) -> int:
        if len(features) == 0:
            return 0
        priorities = eval_tree(self.tree, terminal_arrays(features))
        return int(np.argmin(priorities))
