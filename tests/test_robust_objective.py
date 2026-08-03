# -*- coding: utf-8 -*-
"""El objetivo robusto: la anchura entra en lo que se optimiza.

Sin DEEPLJSP_V2_LAMBDA el valor a minimizar es el peor caso puro, como
siempre. Con lambda>0 pasa a ser up + lambda*(up-lo), el analogo del
f_lambda del estudio companion, y la recompensa terminal lo refleja.
Es la unica via por la que la anchura del intervalo llega al objetivo.
"""
import importlib

import pytest

from jobshop_rl.models.interval import Interval


def _componente(monkeypatch, lam):
    if lam is None:
        monkeypatch.delenv("DEEPLJSP_V2_LAMBDA", raising=False)
    else:
        monkeypatch.setenv("DEEPLJSP_V2_LAMBDA", str(lam))
    import jobshop_rl.rewards.components.makespan as mk
    importlib.reload(mk)
    return mk.MakespanRewardComponent(weight=1.0)


def test_sin_lambda_es_el_peor_caso(monkeypatch):
    c = _componente(monkeypatch, None)
    assert c._robust_value(Interval(90, 110)) == pytest.approx(110.0)


def test_lambda_penaliza_la_anchura(monkeypatch):
    c = _componente(monkeypatch, 1.0)
    # up=110, lo=90 -> 110 + 1.0 * 20
    assert c._robust_value(Interval(90, 110)) == pytest.approx(130.0)
    c4 = _componente(monkeypatch, 4.0)
    assert c4._robust_value(Interval(90, 110)) == pytest.approx(190.0)


def test_a_igual_peor_caso_gana_el_mas_estrecho(monkeypatch):
    """El punto del objetivo: dos schedules con el mismo peor caso dejan
    de ser indiferentes en cuanto lambda>0."""
    c0 = _componente(monkeypatch, None)
    ancho = Interval(80, 110)
    estrecho = Interval(105, 110)
    assert c0._robust_value(ancho) == c0._robust_value(estrecho)
    c1 = _componente(monkeypatch, 1.0)
    assert c1._robust_value(estrecho) < c1._robust_value(ancho)


def test_un_escalar_no_se_penaliza(monkeypatch):
    c = _componente(monkeypatch, 2.0)
    assert c._robust_value(1234.0) == pytest.approx(1234.0)
