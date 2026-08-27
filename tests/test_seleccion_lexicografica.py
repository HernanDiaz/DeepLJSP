# -*- coding: utf-8 -*-
"""La retencion del best-of-N sigue la Eq. (3) del paper.

Regresion de la revision del 2026-08-26: evaluate_policy retenia por el
extremo superior solo y rompia los empates por orden de aparicion, no
por el extremo inferior. Estas pruebas fijan la semantica.
"""
import os
import sys

sys.path.insert(0, ".")

from jobshop_rl.agents_v2.agent import AgentV2          # noqa: E402
from jobshop_rl.models.interval import (                # noqa: E402
    Interval, final_makespan)


class _EnvFalso:
    def __init__(self, comps):
        self.job_completion_time = comps


def _clave(comps):
    agente = AgentV2.__new__(AgentV2)
    agente.env = _EnvFalso(comps)
    m = final_makespan(comps)
    escalar = float(m.upper) if isinstance(m, Interval) else float(m)
    return AgentV2._clave_retencion(agente, escalar)


def test_makespan_componente_a_componente():
    """El makespan agrega los dos extremos por separado."""
    comps = [Interval(40, 100), Interval(90, 95)]
    m = final_makespan(comps)
    assert (float(m.lower), float(m.upper)) == (90.0, 100.0)
    # el max lexicografico de Python daria el intervalo de UN trabajo
    assert float(max(comps).lower) == 40.0


def test_empate_del_superior_lo_decide_el_inferior():
    """Eq. (3): a^U = b^U -> gana el de menor a^L."""
    os.environ.pop("DEEPLJSP_V2_LAMBDA", None)
    ancho = _clave([Interval(40, 100), Interval(90, 95)])   # [90, 100]
    estrecho = _clave([Interval(70, 100), Interval(95, 98)])  # [95, 100]
    assert ancho[0] == estrecho[0] == 100.0
    assert ancho < estrecho


def test_el_superior_manda_sobre_el_inferior():
    """Sin empate, decide el peor caso aunque el inferior diga lo otro."""
    os.environ.pop("DEEPLJSP_V2_LAMBDA", None)
    mejor = _clave([Interval(10, 90)])
    peor = _clave([Interval(80, 100)])
    assert mejor < peor


def test_el_brazo_robusto_ordena_por_su_objetivo():
    """Con lambda>0 la clave es el f_lambda escalar, no la tupla."""
    os.environ["DEEPLJSP_V2_LAMBDA"] = "1"
    try:
        k = _clave([Interval(90, 100)])
        assert len(k) == 1
    finally:
        os.environ.pop("DEEPLJSP_V2_LAMBDA", None)


def test_la_bandera_de_compatibilidad_restituye_la_semantica_vieja():
    """DEEPLJSP_V2_LEGACY_TRACKING=1 vuelve al max lexicografico.

    Las tiradas robustas depositadas se entrenaron con esa semantica.
    El extremo superior coincide en ambas, de modo que ningun brazo
    lambda=0 depende de la bandera; lo que cambia es el inferior, y con
    el el f_lambda que decide que bloque transfiere sus pesos.
    """
    comps = [Interval(40, 100), Interval(90, 95)]
    agente = AgentV2.__new__(AgentV2)
    agente.env = _EnvFalso(comps)

    os.environ["DEEPLJSP_V2_LAMBDA"] = "1"
    try:
        os.environ.pop("DEEPLJSP_V2_LEGACY_TRACKING", None)
        correcto = AgentV2._episode_makespan(agente)
        os.environ["DEEPLJSP_V2_LEGACY_TRACKING"] = "1"
        historico = AgentV2._episode_makespan(agente)
    finally:
        os.environ.pop("DEEPLJSP_V2_LAMBDA", None)
        os.environ.pop("DEEPLJSP_V2_LEGACY_TRACKING", None)

    # componentwise da [90, 100] -> 100 + 1*(100-90) = 110
    assert correcto == 110.0
    # el max lexicografico da [40, 100] -> 100 + 1*(100-40) = 160
    assert historico == 160.0
    assert historico > correcto


def test_la_bandera_no_afecta_a_lambda_cero():
    """Con lambda=0 solo cuenta el extremo superior, igual en las dos."""
    comps = [Interval(40, 100), Interval(90, 95)]
    agente = AgentV2.__new__(AgentV2)
    agente.env = _EnvFalso(comps)
    os.environ.pop("DEEPLJSP_V2_LAMBDA", None)
    try:
        os.environ.pop("DEEPLJSP_V2_LEGACY_TRACKING", None)
        a = AgentV2._episode_makespan(agente)
        os.environ["DEEPLJSP_V2_LEGACY_TRACKING"] = "1"
        b = AgentV2._episode_makespan(agente)
    finally:
        os.environ.pop("DEEPLJSP_V2_LEGACY_TRACKING", None)
    assert a == b == 100.0
