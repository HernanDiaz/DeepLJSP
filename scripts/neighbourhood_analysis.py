"""Tamano y neutralidad del vecindario de busqueda local sobre una regla GP.

Sustituye un simbolo (terminal u operador de igual aridad) en cada posicion y
cuenta cuantos vecinos producen EL MISMO schedule. La neutralidad decide que
metodo de busqueda local sirve: con mesetas grandes un hill climbing se atasca
y hace falta algo que fuerce movimiento, como tabu.

Material para el segundo paper; ver paper_gp/IDEAS_SEGUNDO_PAPER.md
"""
import json
import re
import sys

import numpy as np

sys.path.insert(0, ".")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data import PROBLEM_REGISTRY                       # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory      # noqa: E402
from jobshop_rl.heuristics.gp_rule import (                        # noqa: E402
    TERMINALS, FUNCTIONS, GPRuleHeuristic)

TREE = json.load(open("benchmarks/reevo_fixedfit/gp_tuned_seed1.json",
                      encoding="utf-8"))["tree"]
TRAIN = ["int__tai20_15_01", "int__tai20_15_02",
         "int__tai20_15_03", "int__tai20_15_04"]


def nodos(t, path=()):
    """Devuelve (path, nodo) de todos los nodos."""
    out = [(path, t)]
    if not isinstance(t, str):
        for i, c in enumerate(t[1:], 1):
            out += nodos(c, path + (i,))
    return out


def reemplaza(t, path, nuevo):
    if not path:
        return nuevo
    t = list(t)
    t[path[0]] = reemplaza(t[path[0]], path[1:], nuevo)
    return tuple(t) if isinstance(t, tuple) else t


def secuencia(tree, pid):
    h = GPRuleHeuristic(tree)
    env = EnvironmentFactory.create_from_problem(
        PROBLEM_REGISTRY[pid](), "basic", seed=0)
    st = env.reset(); done = False; seq = []
    while not done and st["eligible_ops"]:
        f = env.get_features(st)
        a = min(h.select_action(st["eligible_ops"], f),
                len(st["eligible_ops"]) - 1)
        seq.append(env.eligible_ops[a])
        st, _, done, _ = env.step(a)
    return tuple(seq)


todos = nodos(TREE)
hojas = [(p, n) for p, n in todos if isinstance(n, str)]
funcs = [(p, n) for p, n in todos if not isinstance(n, str)]
bin_ = [f for f in FUNCTIONS if FUNCTIONS[f] == 2]
un_ = [f for f in FUNCTIONS if FUNCTIONS[f] == 1]

print(f"regla destacada: {len(todos)} nodos, {len(hojas)} hojas, "
      f"{len(funcs)} funciones")

vecinos = []
for p, n in hojas:                       # sustitucion de terminal
    for t in TERMINALS:
        if t != n:
            vecinos.append(reemplaza(TREE, p, t))
for p, n in funcs:                       # sustitucion de operador de igual aridad
    alt = bin_ if FUNCTIONS[n[0]] == 2 else un_
    for f in alt:
        if f != n[0]:
            vecinos.append(reemplaza(TREE, p, tuple([f] + list(n[1:]))))

print(f"vecinos por sustitucion de un simbolo: {len(vecinos)}")

base = {pid: secuencia(TREE, pid) for pid in TRAIN}
neutros = 0
for v in vecinos:
    try:
        if all(secuencia(v, pid) == base[pid] for pid in TRAIN):
            neutros += 1
    except Exception:
        pass
print(f"vecinos NEUTROS (mismo schedule en las 4 de entrenamiento): "
      f"{neutros}/{len(vecinos)} = {100*neutros/len(vecinos):.0f}%")
