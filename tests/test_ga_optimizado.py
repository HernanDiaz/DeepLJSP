# -*- coding: utf-8 -*-
"""El genetico optimizado tiene que dar EXACTAMENTE lo que daba antes.

La optimizacion del decodificador de permutaciones y del cruce JOX solo
puede cambiar el tiempo: con la misma semilla, el mismo hijo, el mismo
makespan y la misma curva de presupuesto que la version congelada en
tests/referencias/e6_v1.py.
"""
import os
import random
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jobshop_rl.data import PROBLEM_REGISTRY                   # noqa: E402
from jobshop_rl.heuristics import ga_interval as nuevo         # noqa: E402
from jobshop_rl.heuristics.fast_sim import (                   # noqa: E402
    Instancia, decodifica, despacha, prioridad_de)
from tests.referencias import e6_v1 as viejo                   # noqa: E402

ARBOL = ("sub", ("sub", ("mul", "SLACK", "SLACK"),
                 ("sub", "WKR", ("add", "PT", "PT"))),
         ("add", "WKRW", "ONE"))
CASOS = ["int__tai15_15_01", "int__tai30_20_05", "int__tai50_20_02"]
PUNTOS = [2 ** k for k in range(0, 13)]


@pytest.fixture(scope="module")
def instancias():
    return {pid: Instancia(PROBLEM_REGISTRY[pid]()) for pid in CASOS}


def test_decodifica_igual(instancias):
    for pid, inst in instancias.items():
        rng = random.Random(1)
        for _ in range(200):
            perm = viejo.aleatoria(inst, rng)
            assert decodifica(inst, perm) == viejo.decodifica(inst, perm), pid


def test_jox_igual(instancias):
    for pid, inst in instancias.items():
        rng = random.Random(2)
        padres = [viejo.aleatoria(inst, rng) for _ in range(101)]
        r1, r2 = random.Random(3), random.Random(3)
        for a, b in zip(padres, padres[1:]):
            assert nuevo.jox(a, b, inst.n, r1) == viejo.jox(a, b, inst.n, r2)
        assert r1.getstate() == r2.getstate(), pid


def _makespans(curva):
    return {p: cm for p, (cm, _) in curva.items()}


@pytest.mark.parametrize("sembrado", [False, True])
def test_evoluciona_igual(instancias, sembrado):
    for pid, inst in instancias.items():
        siembra = (despacha(inst, prioridad_de(ARBOL), orden=True)[1]
                   if sembrado else None)
        for semilla in (1, 2):
            a, ma = nuevo.evoluciona(inst, PUNTOS[-1], random.Random(semilla),
                                     siembra=siembra, puntos=list(PUNTOS))
            b, mb = viejo.evoluciona(inst, PUNTOS[-1], random.Random(semilla),
                                     siembra=siembra, puntos=list(PUNTOS))
            assert _makespans(a) == _makespans(b), (pid, semilla)
            assert ma == mb


def test_azar_igual(instancias):
    for pid, inst in instancias.items():
        a, ma = nuevo.azar(inst, 1024, random.Random(1), puntos=list(PUNTOS[:11]))
        b, mb = viejo.azar(inst, 1024, random.Random(1), puntos=list(PUNTOS[:11]))
        assert _makespans(a) == _makespans(b) and ma == mb, pid
