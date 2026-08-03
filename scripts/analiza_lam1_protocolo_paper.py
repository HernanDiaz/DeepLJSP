# -*- coding: utf-8 -*-
"""El brazo lambda=1 bajo el MISMO protocolo que las otras ablaciones.

7.5 compara no-width y punto-medio contra el brazo principal leyendo los
schedules que cada tirada guardo en plots/test/, no relanzando una
evaluacion nueva. Este script hace lo mismo con v2-robust-lam1, de modo
que su RE sea directamente comparable con el 13.44 del brazo principal,
y ademas extrae de esos mismos schedules el ANCHO relativo del intervalo
final, que es la magnitud que lambda pretende encoger y que nunca se
habia medido para ningun brazo.

    python scripts/analiza_lam1_protocolo_paper.py
"""
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, ".")

from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402

BRAZOS = [("principal", "v2-full-1000ep"), ("no-width", "v2-nowidth-1000ep-b"),
          ("punto medio", "v2-midpoint-1000ep-b"),
          ("lambda=1", "v2-robust-lam1")]


def ta_de(nombre):
    m = re.search(r"tai(\d+)_(\d+)_(\d+)", nombre.lower())
    if not m:
        return None
    n, mm, k = int(m.group(1)), int(m.group(2)), int(m.group(3))
    clase = {(15, 15): 0, (20, 15): 1, (20, 20): 2, (30, 15): 3,
             (30, 20): 4, (50, 15): 5, (50, 20): 6}[(n, mm)]
    return f"TA{clase * 10 + k}"


def extremos(path):
    """(lower, upper) del makespan componente a componente, Eq. 2."""
    lo_max = up_max = 0.0
    for t in json.load(open(path)):
        e = t["end"]
        lo, up = (e["lower"], e["upper"]) if isinstance(e, dict) else (e, e)
        lo_max, up_max = max(lo_max, lo), max(up_max, up)
    return lo_max, up_max


def por_par(tag):
    """{(TA, semilla): (re, ancho relativo %)}."""
    out = {}
    for d in sorted(glob.glob(f"outputs/bench_{tag}__*_seed*")):
        s = d.split("_seed")[-1]
        for p in glob.glob(os.path.join(d, "plots", "test", "*_schedule.json")):
            ta = ta_de(os.path.basename(p))
            lo, up = extremos(p)
            mid = (lo + up) / 2
            lb = lb_for_problem_name(f"int__tai20_15_{int(ta[2:]) - 10:02d}")
            out[(ta, s)] = ((mid - lb) / lb * 100, (up - lo) / mid * 100)
    return out


def main():
    datos = {n: por_par(t) for n, t in BRAZOS}
    base = datos["principal"]
    print(f"{'brazo':12s} {'pares':>6s} {'RE':>8s} {'ancho':>8s}")
    for n, _ in BRAZOS:
        d = datos[n]
        if not d:
            print(f"{n:12s}  SIN DIRECTORIOS")
            continue
        re_m = sum(v[0] for v in d.values()) / len(d)
        an_m = sum(v[1] for v in d.values()) / len(d)
        print(f"{n:12s} {len(d):6d} {re_m:7.2f}% {an_m:7.2f}%")

    print("\npareado contra el brazo principal (mismos TA y semilla):")
    for n, _ in BRAZOS[1:]:
        d = datos[n]
        if not d:
            continue
        com = sorted(set(base) & set(d))
        if not com:
            print(f"  {n}: sin pares en comun "
                  f"(semillas {sorted({k[1] for k in d})})")
            continue
        dre = [d[k][0] - base[k][0] for k in com]
        dan = [d[k][1] - base[k][1] for k in com]
        print(f"  {n} ({len(com)} pares): RE {sum(dre)/len(dre):+.2f} pts, "
              f"ancho {sum(dan)/len(dan):+.2f} pts "
              f"(mas estrecho en {sum(x < 0 for x in dan)}/{len(dan)})")
        try:
            from scipy import stats
            print(f"      Wilcoxon  RE p={stats.wilcoxon(dre)[1]:.3g}   "
                  f"ancho p={stats.wilcoxon(dan)[1]:.3g}")
        except ImportError:
            pass


if __name__ == "__main__":
    main()
