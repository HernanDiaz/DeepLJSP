# -*- coding: utf-8 -*-
"""La ablacion worst-case-only del encoder: espejo del brazo no-width del GP.

Con DEEPLJSP_V2_WORSTCASE_ONLY=1 cada intervalo colapsa a su peor caso:
las features de anchura (columnas 2 y 5, y la incertidumbre pendiente
global) deben ser exactamente cero, los pares (lo, up) deben coincidir, y
las dimensiones no cambian. Sin la variable, una instancia intervalar
debe producir anchuras positivas — el guardia contra un encoder que
estuviera ciego de serie.
"""
import importlib
import os

import numpy as np
import pytest

from jobshop_rl.experiments.factory import EnvironmentFactory


def _encode_inicial(monkeypatch, worstcase):
    if worstcase:
        monkeypatch.setenv("DEEPLJSP_V2_WORSTCASE_ONLY", "1")
    else:
        monkeypatch.delenv("DEEPLJSP_V2_WORSTCASE_ONLY", raising=False)
    import jobshop_rl.agents_v2.state_encoder as se
    importlib.reload(se)
    env = EnvironmentFactory.create_from_problem_id(
        "int__tai15_15_01", "adaptive", seed=1)
    state = env.reset()
    enc = se.StateEncoder(env)
    return enc.encode(state)


def test_worstcase_anula_las_anchuras(monkeypatch):
    op, gl = _encode_inicial(monkeypatch, worstcase=True)
    assert op.shape[1] == 16 and gl.shape == (12,)
    # anchuras relativas de duracion (col 2) y de earliest start (col 5)
    assert np.allclose(op[:, 2], 0.0)
    assert np.allclose(op[:, 5], 0.0)
    # los pares (lo, up) coinciden: duracion, est, trabajo restante
    assert np.allclose(op[:, 0], op[:, 1])
    assert np.allclose(op[:, 3], op[:, 4])
    assert np.allclose(op[:, 6], op[:, 7])
    # incertidumbre pendiente global
    assert gl[10] == pytest.approx(0.0)


def test_sin_flag_hay_anchura(monkeypatch):
    op, gl = _encode_inicial(monkeypatch, worstcase=False)
    assert float(np.max(op[:, 2])) > 0.0
    assert float(gl[10]) > 0.0
