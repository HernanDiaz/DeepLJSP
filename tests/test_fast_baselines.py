# -*- coding: utf-8 -*-
"""Los baselines optimizados tienen que dar EXACTAMENTE lo de tiempos_fast.

Mismo makespan y misma secuencia de despacho, en una pasada y con
eps > 0 (con el generador en el mismo estado), que las politicas de
scripts/tiempos_fast.py sobre fast_sim.despacha; y la media de RE de cada
uno sobre las 70 Taillard es la de benchmarks/all_baselines.csv.
"""
import csv
import os
import random
import sys

import numpy as np
import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

from jobshop_rl.data import PROBLEM_REGISTRY                   # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.heuristics.fast_baselines import (             # noqa: E402
    METODOS, despachador)
from jobshop_rl.heuristics.fast_sim import Instancia, despacha  # noqa: E402

import tiempos_fast as tf                                       # noqa: E402

REFERENCIA = {"SPT": tf.spt, "LPT": tf.lpt, "EST": tf.est, "MWKR": tf.mwkr,
              "MOR": tf.mor, "CR": tf.cr, "G&T-SPT": tf.gt("spt"),
              "G&T-MWKR": tf.gt("mwkr")}
CASOS = ["int__tai15_15_01", "int__tai20_20_03", "int__tai30_15_07",
         "int__tai50_20_02"]


@pytest.fixture(scope="module")
def instancias():
    return {pid: Instancia(PROBLEM_REGISTRY[pid]()) for pid in CASOS}


def test_estan_los_ocho():
    assert set(METODOS) == set(REFERENCIA)


@pytest.mark.parametrize("metodo", sorted(REFERENCIA))
def test_misma_pasada(metodo, instancias):
    rapido = despachador(metodo)
    for pid, inst in instancias.items():
        assert rapido(inst, orden=True) == despacha(
            inst, REFERENCIA[metodo], orden=True), pid


@pytest.mark.parametrize("metodo", sorted(REFERENCIA))
def test_mismas_muestras(metodo, instancias):
    rapido = despachador(metodo)
    for pid, inst in instancias.items():
        r1, r2 = random.Random(3), random.Random(3)
        for _ in range(4):
            assert rapido(inst, orden=True, eps=0.3, rng=r1) == despacha(
                inst, REFERENCIA[metodo], orden=True, eps=0.3, rng=r2), pid
        assert r1.getstate() == r2.getstate()


def test_reproducen_la_tabla():
    """La media de RE de cada baseline en las 70 es la de la tabla."""
    sys.path.insert(0, os.path.join(RAIZ, "scripts"))
    from e6_presupuesto import setenta
    ref = {r["method"]: float(r["all"]) for r in csv.DictReader(
        open(os.path.join(RAIZ, "benchmarks/all_baselines.csv"),
             encoding="utf-8-sig"))}
    insts = setenta()
    datos = {p: Instancia(PROBLEM_REGISTRY[p]()) for p in insts}
    for metodo in METODOS:
        d = despachador(metodo)
        v = np.mean([tf.re_(d(datos[p]), lb_for_problem_name(p)) for p in insts])
        assert abs(v - ref[metodo]) < 0.01, (metodo, v, ref[metodo])
