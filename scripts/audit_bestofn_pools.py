"""
AUDITORÍA best-of-N (paper_gp fig_bestofN / tab:matched) desde los pools.

Para cada pool GP y v2: decodifica cada línea y obtiene las DOS agregaciones
del makespan (vieja lex-por-upper y nueva componente a componente). Calcula
las curvas best-of-N (selección lexicográfica por (upper, lower), como en el
paper; RE por midpoint) bajo ambas convenciones -> delta exacto por convención
sobre la MISMA muestra.

Nota: los números publicados (18.5/17.1/15.9/14.9/14.1) provienen de otra
corrida de muestreo (fair_gp_eps, 2026-07-07); los pools son otra realización.
Este script separa los dos efectos: (a) convención vieja->nueva sobre muestra
idéntica (el efecto del fix), (b) corrida vieja vs pools (ruido de muestreo).
"""

import glob
import os
import re
import sys

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data import PROBLEM_REGISTRY
from jobshop_rl.data.literature_bounds import lb_for_problem_name
from jobshop_rl.models.interval import Interval

NS = [1, 16, 64, 256, 1024]


def instance_bounds(pid):
    prob = PROBLEM_REGISTRY[pid]()
    durs, mseq = prob["durations"], prob["sequences"]
    lo = [[int(d.lower) if isinstance(d, Interval) else int(d) for d in row]
          for row in durs]
    up = [[int(d.upper) if isinstance(d, Interval) else int(d) for d in row]
          for row in durs]
    return lo, up, mseq


def decode_both(seq, dlo, dup, mseq):
    """(old_lo, new_lo, up): lower lex-por-upper, lower componentwise, upper."""
    nj = len(dlo); nm = len(mseq[0])
    jlo = [0] * nj; jup = [0] * nj
    mlo = [0] * nm; mup = [0] * nm
    oi = [0] * nj
    for j1 in seq:
        j = j1 - 1; k = oi[j]; m = mseq[j][k]
        slo = jlo[j] if jlo[j] > mlo[m] else mlo[m]
        sup = jup[j] if jup[j] > mup[m] else mup[m]
        elo = slo + dlo[j][k]; eup = sup + dup[j][k]
        jlo[j] = elo; jup[j] = eup; mlo[m] = elo; mup[m] = eup
        oi[j] = k + 1
    # viejo: lower del trabajo de mayor (upper, lower); nuevo: max lowers
    bi = max(range(nj), key=lambda i: (jup[i], jlo[i]))
    return jlo[bi], max(jlo), max(jup)


def curves_for(gen):
    pools = sorted(glob.glob(f"seeds/*_{gen}_pool.csv"))
    acc_old = {n: [] for n in NS}
    acc_new = {n: [] for n in NS}
    for path in pools:
        pid = os.path.basename(path)[:-len(f"_{gen}_pool.csv")]
        if not re.match(r"int__tai\d+_\d+_\d+$", pid):
            continue
        lb = lb_for_problem_name(pid)
        if lb is None:
            continue
        dlo, dup, mseq = instance_bounds(pid)
        sols = []
        for line in open(path, encoding="utf-8"):
            if ";" not in line:
                continue
            seq = [int(x) for x in line.split(";")[0].split()]
            sols.append(decode_both(seq, dlo, dup, mseq))
        # prefijos best-of-N, selección lex (upper, lower) por convención
        for n in NS:
            pre = sols[:n]
            bo = min(pre, key=lambda s: (s[2], s[0]))   # convención vieja
            bn = min(pre, key=lambda s: (s[2], s[1]))   # convención nueva
            acc_old[n].append(((bo[0] + bo[2]) / 2 - lb) / lb * 100)
            acc_new[n].append(((bn[1] + bn[2]) / 2 - lb) / lb * 100)
        print(".", end="", flush=True)
    print()
    return acc_old, acc_new, len(acc_old[1])


def main():
    for gen in ("gp", "v2"):
        acc_old, acc_new, ninst = curves_for(gen)
        print(f"=== {gen} ({ninst} instancias): best-of-N, RE midpoint ===")
        print(f"  {'N':>6}{'viejo':>9}{'nuevo':>9}{'delta':>9}")
        for n in NS:
            o = sum(acc_old[n]) / ninst
            v = sum(acc_new[n]) / ninst
            print(f"  {n:>6}{o:>9.2f}{v:>9.2f}{v-o:>+9.3f}")
        print()


if __name__ == "__main__":
    main()
