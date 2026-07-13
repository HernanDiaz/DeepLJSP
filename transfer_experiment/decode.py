"""
Decodificadores de secuencias (permutación con repetición de trabajos) a
schedules semiactivos, bajo distintas aritméticas de incertidumbre.

Una SECUENCIA es la lista 1-based de trabajos del formato de los pools: la
k-ésima aparición del trabajo j = k-ésima operación de j. El schedule
semiactivo arranca cada operación en max(fin de la op anterior del trabajo,
fin de la anterior en su máquina) y termina en inicio + duración.

- decode_crisp: duraciones enteras, max/suma normales -> makespan crisp.
- decode_interval: duraciones Interval, max/suma componente a componente ->
  makespan intervalo (para VALIDAR contra el [lo,up] guardado en el pool).
- decode_tfn: números triangulares (a,b,c), suma y max fuzzy -> makespan TFN.

Todos comparten el mismo esqueleto de despacho; solo cambia el tipo de
duración y las operaciones + y max.
"""

from jobshop_rl.models.interval import Interval


def _decode(seq, durations, machine_seq, zero, add, mx, key):
    """
    Esqueleto genérico. seq: lista 1-based de trabajos. durations[j][k]:
    duración de la k-ésima op del trabajo j. machine_seq[j][k]: máquina de esa
    op. zero: elemento neutro (t=0). add/mx: suma y máximo del tipo. key: para
    el max final del makespan (p.ej. lambda x: x.upper en intervalo).
    """
    nj = len(durations)
    nm = len(machine_seq[0])
    job_end = [zero] * nj           # fin de la última op programada de cada job
    mach_end = [zero] * nm          # fin de la última op programada de cada máquina
    op_idx = [0] * nj               # siguiente op de cada job
    for j1 in seq:
        j = j1 - 1
        k = op_idx[j]
        m = machine_seq[j][k]
        start = mx(job_end[j], mach_end[m])
        end = add(start, durations[j][k])
        job_end[j] = end
        mach_end[m] = end
        op_idx[j] = k + 1
    return max(job_end, key=key)


def decode_crisp(seq, durations, machine_seq):
    return _decode(seq, durations, machine_seq, 0,
                   lambda a, b: a + b, max, key=lambda x: x)


def _imax(a, b):
    return Interval(max(a.lower, b.lower), max(a.upper, b.upper))


def decode_interval(seq, durations, machine_seq):
    mk = _decode(seq, durations, machine_seq, Interval(0, 0),
                 lambda a, b: a + b, _imax, key=lambda x: x.upper)
    return mk


def _tadd(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def _tmax(a, b):
    # max fuzzy aproximado (componente a componente) — estándar en fuzzy JSP
    return (max(a[0], b[0]), max(a[1], b[1]), max(a[2], b[2]))


def _tfn_expected(t):
    """Valor esperado de un TFN (a,b,c): E = (a + 2b + c)/4 (defuzzificación
    estándar). Se usa para rankear el max final sobre trabajos."""
    return (t[0] + 2 * t[1] + t[2]) / 4


def decode_tfn(seq, durations, machine_seq):
    """durations[j][k] = (a,b,c) triangular. Devuelve makespan TFN, con el
    max final sobre trabajos rankeado por valor esperado."""
    return _decode(seq, durations, machine_seq, (0, 0, 0),
                   _tadd, _tmax, key=_tfn_expected)
