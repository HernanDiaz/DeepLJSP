"""
Recalcula el makespan guardado de los pools con la convención CORRECTA
(componente a componente), dejando las SECUENCIAS intactas.

Motivo: los pools se generaron con el makespan final lexicográfico-por-upper
del entorno (max(job_completion_time)), que da el lower del trabajo de mayor
upper — un lower demasiado bajo. La convención correcta (= EvaluationIJSP_
Makespan y el entorno ya arreglado) es componente a componente:
    makespan = [ max_j lower_j , max_j upper_j ]
El UPPER es idéntico en ambas (no cambia ningún ranking); solo se corrige el
LOWER en el 0-24% de soluciones donde el trabajo de mayor upper no es el de
mayor lower.

Proceso: (1) informe del estado actual (cuántas cuadran), (2) reescritura con
el lower corregido, (3) verificación de que ahora cuadra el 100%.
Idempotente: reejecutar sobre pools ya corregidos da 100% sin cambios.
"""

import glob
import os
import sys

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data import PROBLEM_REGISTRY
from jobshop_rl.models.interval import Interval


def instance_bounds(pid):
    """dur_lo[j][k], dur_up[j][k], machine_seq[j][k] de la instancia intervalo."""
    prob = PROBLEM_REGISTRY[pid]()
    durs, mseq = prob["durations"], prob["sequences"]
    lo = [[int(d.lower) if isinstance(d, Interval) else int(d) for d in row]
          for row in durs]
    up = [[int(d.upper) if isinstance(d, Interval) else int(d) for d in row]
          for row in durs]
    return lo, up, mseq


def decode_component(seq, dlo, dup, mseq):
    """Makespan componente a componente (int). Devuelve (lo, up)."""
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
    return max(jlo), max(jup)


def main():
    pools = sorted(glob.glob("seeds/*_pool.csv"))
    print(f"{len(pools)} pools\n")

    # instancias en juego (cachear bounds)
    cache = {}
    total_lines = up_bad = lo_diff = 0
    per_gen_diff = {}

    # ---- Pase 1: informe del estado ACTUAL + reescritura ----
    for path in pools:
        base = os.path.basename(path)
        pid = base.split("_")[0] if base.startswith("ft10") else \
            "_".join(base.split("_")[:2]) if base.startswith("int__") else None
        # nombre de instancia = todo antes de _<generador>_pool.csv
        for g in ("graspmor", "gtmwkr", "graspmix", "gp", "v2"):
            suf = f"_{g}_pool.csv"
            if base.endswith(suf):
                pid = base[:-len(suf)]
                gen = g
                break
        else:
            continue
        if pid not in cache:
            cache[pid] = instance_bounds(pid)
        dlo, dup, mseq = cache[pid]

        out_lines = []
        for line in open(path, encoding="utf-8"):
            line = line.rstrip("\n")
            if ";" not in line:
                out_lines.append(line)
                continue
            perm_s, iv = line.split(";")
            seq = [int(x) for x in perm_s.split()]
            s_lo, s_up = (int(x) for x in iv.strip("[] ").split(","))
            c_lo, c_up = decode_component(seq, dlo, dup, mseq)
            total_lines += 1
            if c_up != s_up:
                up_bad += 1        # NO deberia pasar (upper es invariante)
            if c_lo != s_lo:
                lo_diff += 1
                per_gen_diff[gen] = per_gen_diff.get(gen, 0) + 1
            out_lines.append(f"{perm_s};[{c_lo}, {c_up}]")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(out_lines) + "\n")

    print("=== ESTADO ANTES (convención vieja lex-por-upper en los pools) ===")
    print(f"  líneas totales: {total_lines}")
    print(f"  UPPER discrepante: {up_bad}  (debe ser 0 — el upper es invariante)")
    print(f"  LOWER corregido:  {lo_diff}  ({100*lo_diff/total_lines:.1f}% de las soluciones)")
    for g, n in sorted(per_gen_diff.items()):
        print(f"      {g}: {n} lowers corregidos")

    # ---- Pase 2: VERIFICACIÓN de consistencia (ahora debe ser 100%) ----
    print("\n=== VERIFICACIÓN tras reescritura (test de consistencia) ===")
    checked = ok = 0
    for path in pools:
        base = os.path.basename(path)
        for g in ("graspmor", "gtmwkr", "graspmix", "gp", "v2"):
            suf = f"_{g}_pool.csv"
            if base.endswith(suf):
                pid = base[:-len(suf)]
                break
        else:
            continue
        dlo, dup, mseq = cache[pid]
        for line in open(path, encoding="utf-8"):
            if ";" not in line:
                continue
            perm_s, iv = line.strip().split(";")
            seq = [int(x) for x in perm_s.split()]
            s_lo, s_up = (int(x) for x in iv.strip("[] ").split(","))
            c_lo, c_up = decode_component(seq, dlo, dup, mseq)
            checked += 1
            if c_lo == s_lo and c_up == s_up:
                ok += 1
    print(f"  {ok}/{checked} líneas reproducen EXACTAMENTE el [lo,up] guardado "
          f"con el decodificador componente-a-componente")
    print("  ✓ CONSISTENCIA 100%" if ok == checked
          else f"  ✗ FALLAN {checked-ok}")


if __name__ == "__main__":
    main()
