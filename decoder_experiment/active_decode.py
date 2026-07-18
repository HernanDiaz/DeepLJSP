"""
Decodificador ACTIVO por inserción (crisp), para comparar contra el semiactivo.

Semiactivo (lo que usan los pools): cada operación se coloca al FINAL de la
línea de su máquina.
Activo por inserción: cada operación se coloca en el HUECO más temprano de su
máquina que (a) empiece tras el fin de la op anterior de su trabajo y (b) sea
suficientemente largo. Puede colar operaciones en huecos previos -> makespan
<= semiactivo (todo óptimo es activo).

La secuencia se procesa en su orden dado (permutación con repetición de
trabajos, 1-based). Aritmética escalar (crisp).
"""


def _earliest_slot(intervals, release, dur):
    """Inicio más temprano s >= release tal que [s, s+dur] no solapa ninguna
    op ya programada en la máquina. intervals: lista ordenada de (inicio,fin)
    no solapados."""
    prev_end = 0.0
    for st, en in intervals:
        s = max(release, prev_end)
        if s + dur <= st:          # cabe en el hueco [prev_end, st]
            return s
        prev_end = en
    return max(release, prev_end)   # al final de la máquina (hueco abierto)


def decode_active(seq, durations, machine_seq):
    """Devuelve el makespan crisp del schedule ACTIVO por inserción."""
    nj = len(durations)
    nm = len(machine_seq[0])
    mach = [[] for _ in range(nm)]   # por máquina: (inicio,fin) ordenados
    job_end = [0.0] * nj
    op_idx = [0] * nj
    for j1 in seq:
        j = j1 - 1
        k = op_idx[j]
        m = machine_seq[j][k]
        d = durations[j][k]
        s = _earliest_slot(mach[m], job_end[j], d)
        e = s + d
        # insertar manteniendo orden por inicio
        lst = mach[m]
        lo, hi = 0, len(lst)
        while lo < hi:
            mid = (lo + hi) // 2
            if lst[mid][0] < s:
                lo = mid + 1
            else:
                hi = mid
        lst.insert(lo, (s, e))
        job_end[j] = e
        op_idx[j] = k + 1
    return max(job_end)
