# -*- coding: utf-8 -*-
"""La regla compilada tiene que dar EXACTAMENTE lo que da fast_sim.

Si estos tests pasan, cambiar fast_sim.despacha por el despachador
compilado solo cambia el tiempo: el mismo makespan, la misma secuencia
de despacho y, con eps > 0, el mismo estado final del generador, asi que
el mejor-de-N produce los mismos schedules con la misma semilla.
"""
import glob
import json
import os
import random
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from jobshop_rl.data import PROBLEM_REGISTRY                   # noqa: E402
from jobshop_rl.heuristics.fast_regla import despachador       # noqa: E402
from jobshop_rl.heuristics.fast_sim import (                   # noqa: E402
    Instancia, despacha, prioridad_de)

# la regla destacada del articulo, tal como se evoluciono
ARBOL = ("sub", ("sub", ("mul", "SLACK", "SLACK"),
                 ("sub", "WKR", ("add", "PT", "PT"))),
         ("add", "WKRW", "ONE"))
# arboles que cubren todos los operadores y todos los terminales
SINTETICOS = [
    ("div", "WKR", ("add", "PT", "ONE")),
    ("max", ("min", "SLACK", "PTW"), ("neg", "ESTW")),
    ("mul", ("sub", "EST", "WKRW"), "NOR"),
    ("div", ("sub", "PT", "PT"), ("sub", "NOR", "NOR")),   # division por 0
    "EST",
    ("min", "NOR", "ONE"),                                 # empates masivos
]
EVOLUCIONADAS = [json.load(open(p, encoding="utf-8"))["tree"]
                 for p in sorted(glob.glob(os.path.join(
                     RAIZ, "benchmarks/reevo_fixedfit/gp_tuned_seed*.json")))]
CASOS = ["int__tai15_15_01", "int__tai20_15_01", "int__tai30_20_05"]


@pytest.fixture(scope="module")
def instancias():
    return {pid: Instancia(PROBLEM_REGISTRY[pid]()) for pid in CASOS}


def test_estan_las_30_reglas():
    assert len(EVOLUCIONADAS) == 30


@pytest.mark.parametrize("arbol", [ARBOL] + SINTETICOS + EVOLUCIONADAS)
def test_una_pasada_igual(arbol, instancias):
    rapido = despachador(arbol)
    for pid, inst in instancias.items():
        esperado = despacha(inst, prioridad_de(arbol), orden=True)
        assert rapido(inst, orden=True) == esperado, pid


@pytest.mark.parametrize("arbol", [ARBOL] + SINTETICOS + EVOLUCIONADAS[:5])
def test_mejor_de_n_igual(arbol, instancias):
    """Con eps > 0: mismas muestras y el generador en el mismo estado."""
    rapido = despachador(arbol)
    pol = prioridad_de(arbol)
    for pid, inst in instancias.items():
        r1, r2 = random.Random(7), random.Random(7)
        for _ in range(10):
            a = despacha(inst, pol, orden=True, eps=0.1, rng=r1)
            b = rapido(inst, orden=True, eps=0.1, rng=r2)
            assert a == b, pid
        assert r1.getstate() == r2.getstate(), pid


def test_mejor_de_n_misma_curva(instancias):
    """Parado por numero de muestras en lugar de por tiempo, el mejor-de-N
    compilado recorre las mismas muestras que el de e6_extension2."""
    import time as _time
    from jobshop_rl.heuristics import fast_regla
    sys.path.insert(0, os.path.join(RAIZ, "scripts"))
    from e6_extension2 import bon_por_tiempo
    inst = instancias["int__tai15_15_01"]
    # congelamos el reloj: time.time avanza 1 por llamada, asi los dos
    # paran tras el mismo numero de muestras
    for semilla in (1, 2):
        curvas = []
        for f, pol in ((fast_regla.mejor_de_n, despachador(ARBOL)),
                       (bon_por_tiempo, prioridad_de(ARBOL))):
            reloj = iter(range(10 ** 6))
            real = _time.time
            _time.time = lambda: float(next(reloj))
            try:
                c = f(inst, pol, semilla, 300.0)
            finally:
                _time.time = real
            curvas.append({p: cm for p, (cm, _) in c.items()})
        assert curvas[0] == curvas[1], semilla
