# -*- coding: utf-8 -*-
"""E3: el caso ilustrativo pequeno que pide la revision r1.4.

Se busca una instancia pequena, generada con el MISMO esquema del
articulo (delta uniforme en [0, 0.15 p] alrededor de una duracion base),
en la que:

  - la regla destacada, Ec. (4), despache distinto que SPT y que MWKR;
  - la regla destacada despache distinto que ella misma SIN el termino de
    anchura (beta = 0), y termine con un makespan mejor en las dos
    componentes;
  - la divergencia con beta = 0 ocurra en UNA sola decision, para poder
    senalarla.

El makespan es el intervalo componente a componente, y la comparacion
entre dos schedules usa el criterio lexicografico del articulo.

    python scripts/e3_caso_ilustrativo.py --buscar
    python scripts/e3_caso_ilustrativo.py --caso 12345

Salida NUEVA: benchmarks/e3_caso/caso.json
"""
import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, ".")
os.environ.setdefault("OMP_NUM_THREADS", "1")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.experiments.factory import EnvironmentFactory   # noqa: E402
from jobshop_rl.heuristics.gp_rule import terminal_arrays       # noqa: E402
from jobshop_rl.heuristics.strategies import (                  # noqa: E402
    MWKRHeuristic, SPTHeuristic)
from jobshop_rl.models.interval import Interval                 # noqa: E402

DIR = "benchmarks/e3_caso"
SALIDA = os.path.join(DIR, "caso.json")


# ----------------------------------------------------------------------
# la regla destacada, Ec. (4): SLACK^2 + 2 PT - WKR - beta WKRW - 1
# ----------------------------------------------------------------------
def puntuaciones(features, beta=1.0):
    t = terminal_arrays(features)
    return (t["SLACK"] ** 2 + 2 * t["PT"] - t["WKR"]
            - beta * t["WKRW"] - 1.0)


def instancia(seed, n_jobs, n_maq, base=(8, 30)):
    """Una instancia pequena con el esquema de generacion del articulo."""
    rng = np.random.default_rng(seed)
    secuencias = [list(rng.permutation(n_maq)) for _ in range(n_jobs)]
    duraciones = []
    for _ in range(n_jobs):
        fila = []
        for _ in range(n_maq):
            p = int(rng.integers(base[0], base[1] + 1))
            d = int(rng.integers(0, int(0.15 * p) + 1))
            fila.append(Interval(p - d, p + d))
        duraciones.append(fila)
    return {"num_jobs": n_jobs, "num_machines": n_maq,
            "problem_id": f"e3_{n_jobs}x{n_maq}_s{seed}",
            "sequences": [[int(m) for m in s] for s in secuencias],
            "durations": duraciones, "has_intervals": True}


def rueda(prob, politica):
    """Despacha la instancia entera. Devuelve traza, schedule y makespan."""
    env = EnvironmentFactory.create_from_problem(prob, "basic", seed=0)
    st, traza = env.reset(), []
    done = False
    while not done and st["eligible_ops"]:
        f = env.get_features(st)
        a = politica(st, f)
        traza.append((tuple(st["eligible_ops"]), int(a)))
        st, _, done, _ = env.step(a)
    # Interval.max colapsa a escalar si el resultado es degenerado
    cm = Interval.max(*env.job_completion_time)
    par = ((cm.lower, cm.upper) if isinstance(cm, Interval) else (cm, cm))
    return traza, env.schedule_history, par


def pol_gp(beta):
    return lambda st, f: int(np.argmin(puntuaciones(f, beta)))


def pol_spt(st, f):
    return SPTHeuristic().select_action(st["eligible_ops"], f)


def pol_mwkr(st, f):
    return MWKRHeuristic().select_action(st["eligible_ops"], f)


def mejor(a, b):
    """Criterio lexicografico del articulo: primero el upper, luego el lower."""
    return a[1] < b[1] or (a[1] == b[1] and a[0] < b[0])


def divergencias(t1, t2):
    """Indices en que dos trazas eligen distinto, mientras van a la par."""
    d = []
    for k in range(min(len(t1), len(t2))):
        if t1[k][0] != t2[k][0]:
            break
        if t1[k][1] != t2[k][1]:
            d.append(k)
    return d


def busca(n_jobs, n_maq, hasta):
    """Censo del efecto del termino de anchura, y el primer caso limpio.

    El criterio no mira a SPT ni a MWKR: solo pide que quitar el termino
    de anchura cambie UNA decision y que el makespan empeore al quitarlo.
    Lo que hagan las dos clasicas en ese caso es entonces un hallazgo, no
    una condicion de la busqueda.
    """
    censo = {"n": hasta, "igual": 0, "divergen": 0, "una": 0,
             "mejora": 0, "empeora": 0, "empata": 0,
             "mejora_una": 0, "empeora_una": 0}
    primero = (None, None, None)
    for seed in range(hasta):
        prob = instancia(seed, n_jobs, n_maq)
        tg, _, cg = rueda(prob, pol_gp(1.0))
        tb, _, cb = rueda(prob, pol_gp(0.0))
        d = divergencias(tg, tb)
        if not d:
            censo["igual"] += 1
            continue
        censo["divergen"] += 1
        una = len(d) == 1
        censo["una"] += una
        if mejor(cg, cb):
            censo["mejora"] += 1
            censo["mejora_una"] += una
            if una and primero[1] is None:
                primero = (seed, prob, d[0])
        elif mejor(cb, cg):
            censo["empeora"] += 1
            censo["empeora_una"] += una
        else:
            censo["empata"] += 1
    return primero + (censo,)


def informa(prob, k, censo=None):
    """Imprime la decision k y los cuatro schedules, y deja el json."""
    tg, sg, cg = rueda(prob, pol_gp(1.0))
    tb, sb, cb = rueda(prob, pol_gp(0.0))
    _, ss, cs = rueda(prob, pol_spt)
    _, sm, cm = rueda(prob, pol_mwkr)

    env = EnvironmentFactory.create_from_problem(prob, "basic", seed=0)
    st = env.reset()
    for j in range(k):
        st, _, _, _ = env.step(tg[j][1])
    f = env.get_features(st)
    t = terminal_arrays(f)
    s1, s0 = puntuaciones(f, 1.0), puntuaciones(f, 0.0)
    elig = list(st["eligible_ops"])
    op = [int(st["job_status"][j]) for j in elig]

    print(f"instancia {prob['problem_id']}: "
          f"{prob['num_jobs']}x{prob['num_machines']}\n")
    for j in range(prob["num_jobs"]):
        d = " ".join(f"M{m}[{int(x.lower):2d},{int(x.upper):2d}]"
                     for m, x in zip(prob["sequences"][j],
                                     prob["durations"][j]))
        print(f"  J{j + 1}: {d}")

    print(f"\ndecision {k + 1}, elegibles {['J%d' % (j + 1) for j in elig]}")
    print(f"  {'op':<6} {'PT':>10} {'WKR':>12} {'WKRW':>6} {'SLACK':>6} "
          f"{'Ec.(4)':>9} {'b=0':>9}")
    for i, j in enumerate(elig):
        lo = f.tolist()[i][3]
        print(f"  J{j + 1}o{op[i] + 1:<3} "
              f"[{int(lo):2d},{int(t['PT'][i]):2d}]".ljust(18)
              + f"{int(t['WKR'][i]):>7d} {int(t['WKRW'][i]):>6d} "
                f"{int(t['SLACK'][i]):>6d} {s1[i]:>9.0f} {s0[i]:>9.0f}")
    print(f"\n  Ec.(4) despacha J{elig[int(np.argmin(s1))] + 1}, "
          f"beta=0 J{elig[int(np.argmin(s0))] + 1}, "
          f"SPT J{elig[pol_spt(st, f)] + 1}, "
          f"MWKR J{elig[pol_mwkr(st, f)] + 1}")
    print(f"\n  makespan: Ec.(4) [{cg[0]},{cg[1]}]  beta=0 [{cb[0]},{cb[1]}]"
          f"  SPT [{cs[0]},{cs[1]}]  MWKR [{cm[0]},{cm[1]}]")

    def par(v):
        """start y end llegan como Interval, o como float si son degenerados."""
        return ((v.lower, v.upper) if isinstance(v, Interval)
                else (float(v), float(v)))

    def plano(h):
        out = []
        for x in h:
            s, c = par(x["start"]), par(x["end"])
            out.append({"job": int(x["job"]), "op": int(x["operation"]),
                        "machine": int(x["machine"]),
                        "s_lo": s[0], "s_up": s[1],
                        "c_lo": c[0], "c_up": c[1]})
        return out

    os.makedirs(DIR, exist_ok=True)
    json.dump({
        "problem_id": prob["problem_id"],
        "num_jobs": prob["num_jobs"], "num_machines": prob["num_machines"],
        "sequences": prob["sequences"],
        "durations": [[[int(x.lower), int(x.upper)] for x in fila]
                      for fila in prob["durations"]],
        "decision": k,
        "elegibles": [int(j) for j in elig], "op_idx": op,
        "terminales": {kk: [float(v) for v in t[kk]]
                       for kk in ("PT", "PTW", "WKR", "WKRW", "SLACK")},
        "pt_lo": [float(r[3]) for r in f.tolist()],
        "score_b1": [float(v) for v in s1],
        "score_b0": [float(v) for v in s0],
        "elige": {"gp": int(elig[int(np.argmin(s1))]),
                  "b0": int(elig[int(np.argmin(s0))]),
                  "spt": int(elig[pol_spt(st, f)]),
                  "mwkr": int(elig[pol_mwkr(st, f)])},
        "makespan": {"gp": list(cg), "b0": list(cb),
                     "spt": list(cs), "mwkr": list(cm)},
        "schedules": {"gp": plano(sg), "b0": plano(sb),
                      "spt": plano(ss), "mwkr": plano(sm)},
        "censo": censo,
    }, open(SALIDA, "w", encoding="utf-8"), indent=1)
    print(f"\nescrito {SALIDA}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--caso", type=int, default=None)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--maquinas", type=int, default=4)
    ap.add_argument("--hasta", type=int, default=4000)
    args = ap.parse_args()

    if args.caso is not None:
        prob = instancia(args.caso, args.jobs, args.maquinas)
        tg, _, _ = rueda(prob, pol_gp(1.0))
        tb, _, _ = rueda(prob, pol_gp(0.0))
        informa(prob, divergencias(tg, tb)[0])
        return

    seed, prob, k, censo = busca(args.jobs, args.maquinas, args.hasta)
    print(f"{censo['n']} instancias {args.jobs}x{args.maquinas}")
    print(f"  misma traza sin el termino de anchura  {censo['igual']}")
    print(f"  divergen                               {censo['divergen']}"
          f"  (en una sola decision: {censo['una']})")
    print(f"    la anchura mejora                    {censo['mejora']}"
          f"  (de una sola: {censo['mejora_una']})")
    print(f"    la anchura empeora                   {censo['empeora']}"
          f"  (de una sola: {censo['empeora_una']})")
    print(f"    empatan                              {censo['empata']}\n")
    if prob is None:
        sys.exit(f"sin caso en {args.hasta} semillas")
    print(f"caso: semilla {seed}\n")
    informa(prob, k, censo)


if __name__ == "__main__":
    main()
