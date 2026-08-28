"""
Guardrail del makespan de intervalo: la agregación FINAL sobre las
terminaciones de trabajo debe ser COMPONENTE A COMPONENTE
([max_j lower_j, max_j upper_j]), NO el `max()` lexicográfico-por-upper
(que devuelve el intervalo del trabajo de mayor upper y por tanto un lower
demasiado bajo).

Este test falla si alguien vuelve a usar `max(job_completion_time)` para el
makespan de intervalo en cualquiera de las rutas cubiertas (helper, entorno,
decodificador de transfer). Es la red que impide reintroducir el bug.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jobshop_rl.models.interval import Interval, final_makespan  # noqa: E402


def test_helper_is_componentwise_not_lexicographic():
    # b tiene el mayor upper; a tiene el mayor lower. Son trabajos distintos.
    a = Interval(15, 18)   # mayor lower
    b = Interval(5, 20)    # mayor upper
    fm = final_makespan([a, b])
    assert (fm.lower, fm.upper) == (15, 20), fm      # [max lower, max upper]

    # El max() lexicográfico elegiría b (mayor upper) y daría lower=5: MAL.
    lex = max([a, b])
    assert lex is b and lex.lower == 5
    assert fm.lower != lex.lower                     # el helper NO hace eso


def test_helper_matches_bruteforce_componentwise():
    comps = [Interval(3, 7), Interval(9, 9), Interval(1, 12), Interval(8, 10)]
    fm = final_makespan(comps)
    assert fm.lower == max(c.lower for c in comps)
    assert fm.upper == max(c.upper for c in comps)


def test_helper_scalar_passthrough():
    # Problemas crisp: terminaciones escalares -> makespan escalar.
    assert final_makespan([3.0, 9.0, 1.0]) == 9.0


def test_env_reports_componentwise_makespan():
    """El entorno debe reportar el makespan componente a componente."""
    from jobshop_rl.data import PROBLEM_REGISTRY
    from jobshop_rl.experiments.factory import EnvironmentFactory

    pid = next((p for p in PROBLEM_REGISTRY
                if p.startswith("int__tai15_15")), None)
    if pid is None:
        return  # sin instancias de intervalo disponibles: nada que comprobar

    env = EnvironmentFactory.create_from_problem(
        PROBLEM_REGISTRY[pid](), "basic", seed=0)
    state = env.reset()
    done = False
    info = {}
    while not done:
        state, _, done, info = env.step(0)   # despacha siempre el 1er elegible

    mk = info["makespan"]
    comps = env.job_completion_time
    exp_lo = max(c.lower if isinstance(c, Interval) else c for c in comps)
    exp_up = max(c.upper if isinstance(c, Interval) else c for c in comps)
    assert isinstance(mk, Interval)
    assert mk.lower == exp_lo, (mk, exp_lo)
    assert mk.upper == exp_up, (mk, exp_up)


def test_transfer_decoder_matches_env():
    """decode_interval (transfer) reproduce el makespan del entorno."""
    from jobshop_rl.data import PROBLEM_REGISTRY
    from jobshop_rl.experiments.factory import EnvironmentFactory
    # transfer_experiment/ es material de trabajo y no viaja en el
    # paquete publicado: alli este test se salta en vez de fallar
    _dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "transfer_experiment")
    if not os.path.exists(os.path.join(_dir, "decode.py")):
        import pytest
        pytest.skip("transfer_experiment/ no forma parte del paquete")
    sys.path.insert(0, _dir)
    from decode import decode_interval  # noqa: E402

    pid = next((p for p in PROBLEM_REGISTRY
                if p.startswith("int__tai15_15")), None)
    if pid is None:
        return

    prob = PROBLEM_REGISTRY[pid]()
    env = EnvironmentFactory.create_from_problem(prob, "basic", seed=0)
    state = env.reset()
    done = False
    info = {}
    perm = []
    while not done:
        # reconstruye la permutación 1-based despachada
        job = env.eligible_ops[0]
        perm.append(job + 1)
        state, _, done, info = env.step(0)

    mk_env = info["makespan"]
    mk_dec = decode_interval(perm, prob["durations"], prob["sequences"])
    assert mk_dec.lower == mk_env.lower, (mk_dec, mk_env)
    assert mk_dec.upper == mk_env.upper, (mk_dec, mk_env)


if __name__ == "__main__":
    test_helper_is_componentwise_not_lexicographic()
    test_helper_matches_bruteforce_componentwise()
    test_helper_scalar_passthrough()
    test_env_reports_componentwise_makespan()
    test_transfer_decoder_matches_env()
    print("OK: todos los tests de agregación de makespan pasan")
