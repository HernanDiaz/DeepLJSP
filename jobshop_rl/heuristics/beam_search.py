"""
Beam search constructivo sobre el árbol de despacho con conflict sets de G&T.

Mantiene un haz de W schedules parciales; en cada nivel expande cada nodo por
su conflict set (Giffler-Thompson: candidatas de la máquina de la operación
que antes terminaría), evalúa cada hijo con una cota inferior interval-aware
del makespan completable y poda a los W mejores (comparación lexicográfica
por upper). Referencia clásica: filtered beam search para scheduling
(Sabuncuoglu & Bayiz, 1999); aquí en versión interval-aware.

Coste aproximado: W x (tamaño medio del conflict set) despachos completos.

RESULTADO NEGATIVO DOCUMENTADO (2026-07-06): guiado solo por esta cota
inferior, el beam rinde PEOR que el G&T greedy y empeora con la anchura
(TA5: RE 48.4% con W=10, 62.1% con W=30, vs ~27% del GT-MWKR greedy) — la
cota apenas discrimina entre hermanos y desorienta la poda. La versión
fuerte de la literatura (filtered beam search, Sabuncuoglu & Bayiz 1999)
puntúa los candidatos con PROBES (completar cada hijo con un rollout
greedy), con coste O(T) por candidato — pendiente si se necesita un
baseline constructivo determinista más fuerte que GT-MWKR.
"""

from copy import deepcopy
from typing import List, Tuple

from jobshop_rl.models.interval import Interval


def _up(x) -> float:
    return float(x.upper) if isinstance(x, Interval) else float(x)


def _lo(x) -> float:
    return float(x.lower) if isinstance(x, Interval) else float(x)


def _completion_bound(env) -> Tuple[float, float]:
    """
    Cota inferior del makespan completable del estado actual (lexicográfica
    (upper, lower)): máximo entre el makespan parcial, la carga restante de
    cada máquina sumada a su completion, y el trabajo restante de cada job
    sumado a su completion.
    """
    nj, nm = env.num_jobs, env.num_machines
    best_up = max(_up(c) for c in env.machine_completion_time) if nm else 0.0
    best_lo = max(_lo(c) for c in env.machine_completion_time) if nm else 0.0

    machine_load_up = [0.0] * nm
    machine_load_lo = [0.0] * nm
    for j in range(nj):
        k0 = env.job_status[j]
        rem_up = 0.0
        rem_lo = 0.0
        for k in range(k0, nm):
            d = env.durations[j][k]
            m = env.sequences[j][k]
            machine_load_up[m] += _up(d)
            machine_load_lo[m] += _lo(d)
            rem_up += _up(d)
            rem_lo += _lo(d)
        job_bound_up = _up(env.job_completion_time[j]) + rem_up
        job_bound_lo = _lo(env.job_completion_time[j]) + rem_lo
        if job_bound_up > best_up or (job_bound_up == best_up and job_bound_lo > best_lo):
            best_up, best_lo = job_bound_up, max(best_lo, job_bound_lo)

    for m in range(nm):
        mb_up = _up(env.machine_completion_time[m]) + machine_load_up[m]
        mb_lo = _lo(env.machine_completion_time[m]) + machine_load_lo[m]
        if mb_up > best_up or (mb_up == best_up and mb_lo > best_lo):
            best_up, best_lo = mb_up, max(best_lo, mb_lo)

    return best_up, best_lo


def _gt_conflict_set(env) -> List[int]:
    """Índices (en eligible_ops) del conflict set de Giffler-Thompson."""
    eligible = env.eligible_ops
    completions = []
    starts = []
    machines = []
    for j in eligible:
        k = env.job_status[j]
        m = env.sequences[j][k]
        d = env.durations[j][k]
        s_up = max(_up(env.job_completion_time[j]), _up(env.machine_completion_time[m]))
        s_lo = max(_lo(env.job_completion_time[j]), _lo(env.machine_completion_time[m]))
        starts.append((s_up, s_lo))
        completions.append((s_up + _up(d), s_lo + _lo(d)))
        machines.append(m)

    c = min(range(len(eligible)), key=lambda i: completions[i])
    return [i for i in range(len(eligible))
            if machines[i] == machines[c] and starts[i] < completions[c]] or [c]


def beam_search(env, width: int = 10):
    """
    Ejecuta beam search sobre una copia del entorno.

    Returns:
        (makespan_interval, permutation_1based): mejor solución del haz final.
    """
    total_ops = env.num_jobs * env.num_machines
    root = deepcopy(env)
    root.reset()
    beam = [(root, [])]  # (env, permutación parcial 1-based)

    for _ in range(total_ops):
        candidates = []
        for node_env, perm in beam:
            for idx in _gt_conflict_set(node_env):
                job = node_env.eligible_ops[idx]
                child = deepcopy(node_env)
                child.step(idx)
                score = _completion_bound(child)
                candidates.append((score, child, perm + [job + 1]))
        candidates.sort(key=lambda c: c[0])
        beam = [(c[1], c[2]) for c in candidates[:width]]

    best_env, best_perm = min(
        beam, key=lambda n: (_up(max(n[0].job_completion_time)),
                             _lo(max(n[0].job_completion_time))))
    return max(best_env.job_completion_time), best_perm
