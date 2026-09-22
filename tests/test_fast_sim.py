# -*- coding: utf-8 -*-
"""El simulador rapido tiene que dar EXACTAMENTE lo que da el entorno.

Si estos tests pasan, la comparacion a presupuesto igualado de E6 mide
metodos y no implementaciones. Si alguna vez dejan de pasar, cualquier
cifra de E6 queda invalidada, asi que se comprueban las dos vias: la
regla de prioridad operacion a operacion, y la permutacion que esa misma
regla produce, decodificada por el otro camino.
"""
import os
import re
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jobshop_rl.data import PROBLEM_REGISTRY                   # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.heuristics.fast_sim import (                   # noqa: E402
    Instancia, compila, decodifica, despacha, prioridad_de)
from jobshop_rl.heuristics.gp_rule import (                    # noqa: E402
    eval_tree, terminal_arrays)
from jobshop_rl.models.interval import Interval                # noqa: E402

# la regla destacada del articulo, tal como se evoluciono
ARBOL = ("sub", ("sub", ("mul", "SLACK", "SLACK"),
                 ("sub", "WKR", ("add", "PT", "PT"))),
         ("add", "WKRW", "ONE"))
CASOS = ["int__tai15_15_01", "int__tai20_15_01", "int__tai20_20_03",
         "int__tai30_20_05", "int__tai50_20_02"]


def _entorno(pid, arbol):
    env = EnvironmentFactory.create_from_problem(
        PROBLEM_REGISTRY[pid](), "basic", seed=0)
    st, done, orden = env.reset(), False, []
    while not done and st["eligible_ops"]:
        f = env.get_features(st)
        a = int(np.argmin(np.asarray(eval_tree(arbol, terminal_arrays(f)))))
        orden.append(int(st["eligible_ops"][a]))
        st, _, done, _ = env.step(a)
    c = env.job_completion_time
    lo = max(x.lower if isinstance(x, Interval) else x for x in c)
    up = max(x.upper if isinstance(x, Interval) else x for x in c)
    return (lo, up), orden


def _prioridad(arbol):
    return prioridad_de(arbol)


def test_compila_coincide_con_eval_tree():
    """La evaluacion sin numpy da el mismo numero que la de numpy."""
    rng = np.random.default_rng(0)
    from jobshop_rl.heuristics.gp_rule import TERMINALS
    arboles = [ARBOL,
               ("div", "WKR", ("add", "PT", "ONE")),
               ("max", ("min", "SLACK", "PTW"), ("neg", "ESTW")),
               ("mul", ("sub", "EST", "WKRW"), "NOR")]
    for arbol in arboles:
        for k in (1, 2, 7, 20):
            lst = {t: list(rng.uniform(0, 50, k)) for t in TERMINALS}
            arr = {t: np.asarray(v) for t, v in lst.items()}
            a = compila(arbol)(lst)
            b = eval_tree(arbol, arr)
            assert np.array_equal(np.asarray(a), np.asarray(b)), arbol


@pytest.mark.parametrize("pid", CASOS)
def test_despacho_igual_que_el_entorno(pid):
    esperado, orden_env = _entorno(pid, ARBOL)
    inst = Instancia(PROBLEM_REGISTRY[pid]())
    obtenido, orden = despacha(inst, _prioridad(ARBOL), orden=True)
    assert orden == orden_env, f"{pid}: otra secuencia de despacho"
    assert obtenido == esperado, f"{pid}: {obtenido} contra {esperado}"


@pytest.mark.parametrize("pid", CASOS)
def test_decodifica_la_misma_permutacion(pid):
    inst = Instancia(PROBLEM_REGISTRY[pid]())
    cm, perm = despacha(inst, _prioridad(ARBOL), orden=True)
    assert decodifica(inst, perm) == cm, f"{pid}: el decodificador difiere"


def test_la_permutacion_es_valida():
    """Cada trabajo aparece exactamente m veces."""
    inst = Instancia(PROBLEM_REGISTRY["int__tai20_15_01"]())
    _, perm = despacha(inst, _prioridad(ARBOL), orden=True)
    for j in range(inst.n):
        assert perm.count(j) == inst.m
