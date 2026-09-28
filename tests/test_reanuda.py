# -*- coding: utf-8 -*-
"""Una corrida parada y reanudada tiene que dar lo mismo que una seguida.

El experimento por clases guarda el estado de cada corrida al llegar a
su horizonte para poder alargarla despues sin empezar de cero. Eso solo
vale si continuar desde el estado recorre exactamente los mismos
schedules que una corrida sin interrumpir: aqui se comprueba parando
por presupuesto (sin depender del reloj) en los tres sitios donde puede
caer la parada del genetico --- a mitad de la poblacion inicial, a mitad
de una generacion y justo al cerrar una ---, y con el estado pasado por
pickle, que es como se guarda.
"""
import os
import pickle
import random
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jobshop_rl.data import PROBLEM_REGISTRY                   # noqa: E402
from jobshop_rl.heuristics import fast_regla                   # noqa: E402
from jobshop_rl.heuristics.fast_regla import despachador       # noqa: E402
from jobshop_rl.heuristics.fast_sim import Instancia           # noqa: E402
from jobshop_rl.heuristics.ga_interval import azar, evoluciona  # noqa: E402

ARBOL = ("sub", ("sub", ("mul", "SLACK", "SLACK"),
                 ("sub", "WKR", ("add", "PT", "PT"))),
         ("add", "WKRW", "ONE"))
PUNTOS = [2 ** k for k in range(0, 14)]
TOTAL = 6000
# pop 250 y elite 2: la poblacion inicial son 250 y cada generacion 248
# hijos, asi que 250 + 3 * 248 = 994 cierra una generacion
PARADAS = [100, 1000, 994]


@pytest.fixture(scope="module")
def inst():
    return Instancia(PROBLEM_REGISTRY["int__tai15_15_01"]())


def _cms(curva):
    return {p: cm for p, (cm, _) in curva.items()}


def _por_pickle(estado):
    return pickle.loads(pickle.dumps(estado))


@pytest.mark.parametrize("sembrado", [False, True])
@pytest.mark.parametrize("parada", PARADAS)
def test_genetico_reanudado_igual(inst, parada, sembrado):
    siembra = despachador(ARBOL)(inst, orden=True)[1] if sembrado else None
    seguida, m1 = evoluciona(inst, TOTAL, random.Random(1), siembra=siembra,
                             puntos=list(PUNTOS))
    _, _, est = evoluciona(inst, parada, random.Random(1), siembra=siembra,
                           puntos=list(PUNTOS), con_estado=True)
    assert est["usadas"] == parada
    otra, m2 = evoluciona(inst, TOTAL, random.Random(99),
                          estado=_por_pickle(est))
    assert _cms(otra) == _cms(seguida)
    assert m1 == m2


def test_genetico_reanudado_dos_veces(inst):
    seguida, _ = evoluciona(inst, TOTAL, random.Random(2), puntos=list(PUNTOS))
    _, _, e1 = evoluciona(inst, 700, random.Random(2), puntos=list(PUNTOS),
                          con_estado=True)
    _, _, e2 = evoluciona(inst, 2500, random.Random(0),
                          estado=_por_pickle(e1), con_estado=True)
    otra, _ = evoluciona(inst, TOTAL, random.Random(0), estado=_por_pickle(e2))
    assert _cms(otra) == _cms(seguida)


def test_azar_reanudado_igual(inst):
    seguida, m1 = azar(inst, 3000, random.Random(1), puntos=list(PUNTOS))
    _, _, est = azar(inst, 1000, random.Random(1), puntos=list(PUNTOS),
                     con_estado=True)
    otra, m2 = azar(inst, 3000, random.Random(5), estado=_por_pickle(est))
    assert _cms(otra) == _cms(seguida) and m1 == m2


def test_mejor_de_n_reanudado_igual(inst, monkeypatch):
    """Parado por tiempo con un reloj falso que avanza 1 por lectura: la
    corrida seguida y la reanudada recorren la misma serie de muestras,
    asi que coinciden en todas las potencias de dos que ambas alcanzan."""
    import time as _time
    desp = despachador(ARBOL)

    def reloj_falso():
        cuenta = iter(range(10 ** 7))
        return lambda: float(next(cuenta))

    monkeypatch.setattr(_time, "time", reloj_falso())
    seguida = fast_regla.mejor_de_n(inst, desp, 1, 600.0)
    monkeypatch.setattr(_time, "time", reloj_falso())
    _, est = fast_regla.mejor_de_n(inst, desp, 1, 200.0, con_estado=True)
    monkeypatch.setattr(_time, "time", reloj_falso())
    otra = fast_regla.mejor_de_n(inst, desp, 1, 600.0, estado=_por_pickle(est))
    comunes = [p for p in seguida if p in otra and p & (p - 1) == 0]
    assert len(comunes) >= 7
    assert all(seguida[p][0] == otra[p][0] for p in comunes)
    assert est["k"] > 64
