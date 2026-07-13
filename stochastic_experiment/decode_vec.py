"""
Decodificador semiactivo VECTORIZADO para evaluación Monte Carlo.

Las duraciones se muestrean una vez por instancia (K escenarios, uniforme en
[lo,up]) como arrays de numpy de longitud K -> una sola decodificación evalúa
la secuencia sobre los K escenarios a la vez (números aleatorios comunes: la
misma nube de escenarios para todas las secuencias de la instancia, para una
comparación pareada de baja varianza).
"""

import numpy as np


def sample_durations(lo, up, K, rng):
    """dur[j][k] = array (K,) uniforme en [lo[j][k], up[j][k]]."""
    return [[rng.uniform(lo[j][k], up[j][k], K) for k in range(len(lo[j]))]
            for j in range(len(lo))]


def decode_mc(seq, dur, machine_seq, K):
    """Devuelve array (K,) de makespans de la secuencia sobre los K escenarios."""
    nj = len(dur)
    nm = len(machine_seq[0])
    job_end = [np.zeros(K) for _ in range(nj)]
    mach_end = [np.zeros(K) for _ in range(nm)]
    op_idx = [0] * nj
    for j1 in seq:
        j = j1 - 1
        k = op_idx[j]
        m = machine_seq[j][k]
        start = np.maximum(job_end[j], mach_end[m])
        end = start + dur[j][k]
        job_end[j] = end
        mach_end[m] = end
        op_idx[j] = k + 1
    return np.maximum.reduce(job_end)   # max sobre trabajos, por escenario


def expected_and_cvar(mk_samples, alpha=0.95):
    """(makespan esperado, CVaR-alpha = media del peor (1-alpha) de la cola)."""
    exp = float(mk_samples.mean())
    thr = np.quantile(mk_samples, alpha)
    tail = mk_samples[mk_samples >= thr]
    cvar = float(tail.mean()) if tail.size else float(mk_samples.max())
    return exp, cvar
