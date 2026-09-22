# -*- coding: utf-8 -*-
"""E5: el decodificador y el trato que cada baseline da a los intervalos.

La revision r3.3 hace tres reproches: que no se dice como compara
intervalos cada baseline, que faltan baselines intervalares explicitas, y
que la diferencia entre la regla evolucionada y G&T mezcla dos cosas, la
regla y el decodificador.

Se responde a los tres midiendo:

  A. cada regla clasica bajo TRES convenios de comparacion de intervalos
     --- extremo inferior, punto medio y extremo superior --- de modo que
     ninguna quede penalizada por el convenio que el articulo eligio;
  B. la regla evolucionada bajo el decodificador de Giffler y Thompson,
     restringida al conflict set, que es el decodificador de la baseline
     mas fuerte;
  C. y, de paso, G&T con la regla evolucionada como desempate frente a
     G&T con SPT y con MWKR, que es la comparacion limpia entre reglas a
     decodificador igual.

Todo sobre las setenta, un paso determinista por instancia, el mismo
evaluador que el resto del articulo.

    python scripts/e5_decodificador_baselines.py

Salida NUEVA: benchmarks/e5_decodificador/resumen.json
"""
import glob
import json
import os
import re
import sys

import numpy as np

sys.path.insert(0, ".")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data import PROBLEM_REGISTRY                    # noqa: E402
from jobshop_rl.data.literature_bounds import (                 # noqa: E402
    lb_for_problem_name)
from jobshop_rl.experiments.factory import EnvironmentFactory   # noqa: E402
from jobshop_rl.heuristics.gp_rule import (                     # noqa: E402
    eval_tree, terminal_arrays)
from jobshop_rl.models.interval import Interval                 # noqa: E402

DIR = "benchmarks/e5_decodificador"
SALIDA = os.path.join(DIR, "resumen.json")
REGLAS = "benchmarks/reevo_fixedfit/gp_tuned_seed*.json"
CLASES = {(15, 15), (20, 15), (20, 20), (30, 15), (30, 20),
          (50, 15), (50, 20)}
# los tres convenios: con que numero se resume un intervalo para ordenar
CONVENIOS = {"lower": lambda lo, up: lo,
             "mid": lambda lo, up: (lo + up) / 2.0,
             "upper": lambda lo, up: up}


def setenta():
    out = []
    for p in PROBLEM_REGISTRY:
        m = re.fullmatch(r"int__tai(\d+)_(\d+)_(\d+)", p)
        if m and (int(m.group(1)), int(m.group(2))) in CLASES:
            out.append(p)
    return sorted(out)


# ----------------------------------------------------------------------
# columnas de la matriz de features, layout intervalar de 10
#   2 maquina | 3,4 duracion | 5,6 inicio mas temprano | 7,8 restante
#   9 operaciones restantes
# ----------------------------------------------------------------------
def resumen(f, a, b, conv):
    return np.array([CONVENIOS[conv](f[i][a], f[i][b])
                     for i in range(len(f))])


def clasica(nombre, conv):
    """Una regla clasica bajo un convenio dado. Devuelve el indice."""
    def politica(st, f):
        if nombre == "SPT":
            return int(np.argmin(resumen(f, 3, 4, conv)))
        if nombre == "LPT":
            return int(np.argmax(resumen(f, 3, 4, conv)))
        if nombre == "MWKR":
            return int(np.argmax(resumen(f, 7, 8, conv)))
        if nombre == "EST":
            return int(np.argmin(resumen(f, 5, 6, conv)))
        raise ValueError(nombre)
    return politica


def conflicto(f, conv):
    """El conflict set de Giffler y Thompson bajo un convenio."""
    ini = resumen(f, 5, 6, conv)
    dur = resumen(f, 3, 4, conv)
    fin = ini + dur
    c = int(np.argmin(fin))
    maq = np.array([int(f[i][2]) for i in range(len(f))])
    idx = np.where((maq == maq[c]) & (ini < fin[c]))[0]
    return idx if len(idx) else np.array([c])


def gt(desempate, conv="upper", arbol=None):
    """G&T: conflict set, y dentro de el un desempate."""
    def politica(st, f):
        cs = conflicto(f, conv)
        if len(cs) == 1:
            return int(cs[0])
        if desempate == "spt":
            return int(cs[int(np.argmin(resumen(f, 3, 4, conv)[cs]))])
        if desempate == "mwkr":
            return int(cs[int(np.argmax(resumen(f, 7, 8, conv)[cs]))])
        if desempate == "gp":
            v = eval_tree(arbol, terminal_arrays(f))
            return int(cs[int(np.argmin(np.asarray(v)[cs]))])
        raise ValueError(desempate)
    return politica


def gp_semiactivo(arbol):
    def politica(st, f):
        return int(np.argmin(np.asarray(
            eval_tree(arbol, terminal_arrays(f)))))
    return politica


def re_de(politica, insts):
    vals = []
    for pid in insts:
        env = EnvironmentFactory.create_from_problem(
            PROBLEM_REGISTRY[pid](), "basic", seed=0)
        st, done = env.reset(), False
        while not done and st["eligible_ops"]:
            f = env.get_features(st)
            a = min(politica(st, f), len(st["eligible_ops"]) - 1)
            st, _, done, _ = env.step(a)
        c = env.job_completion_time
        lo = max(x.lower if isinstance(x, Interval) else x for x in c)
        up = max(x.upper if isinstance(x, Interval) else x for x in c)
        lb = lb_for_problem_name(pid)
        vals.append(((lo + up) / 2 - lb) / lb * 100)
    return float(np.mean(vals)), vals


def main():
    insts = setenta()
    assert len(insts) == 70, len(insts)
    os.makedirs(DIR, exist_ok=True)
    res = {"n_instancias": len(insts), "convenios": {}, "decodificador": {}}

    print("A. reglas clasicas bajo los tres convenios de intervalo")
    print(f"  {'regla':<8} " + " ".join(f"{c:>9}" for c in CONVENIOS))
    for nombre in ("SPT", "LPT", "MWKR", "EST"):
        fila = {}
        for conv in CONVENIOS:
            fila[conv] = re_de(clasica(nombre, conv), insts)[0]
        res["convenios"][nombre] = fila
        print(f"  {nombre:<8} " + " ".join(f"{fila[c]:9.2f}" for c in CONVENIOS)
              + f"   mejor {min(fila, key=fila.get)}")

    print("\nB. decodificador: la misma regla en semiactivo y en G&T")
    arboles = {}
    for f in sorted(glob.glob(REGLAS)):
        s = int(re.search(r"seed(\d+)", os.path.basename(f)).group(1))
        arboles[s] = json.load(open(f, encoding="utf-8"))["tree"]
    assert len(arboles) == 30, len(arboles)

    for etq, hazlo in (("gp_semiactivo", gp_semiactivo),
                       ("gp_en_gt", lambda a: gt("gp", "upper", a))):
        por = {}
        for s, a in sorted(arboles.items()):
            por[s] = re_de(hazlo(a), insts)[0]
            print(f"  {etq} seed{s}: {por[s]:.2f}", flush=True)
        v = np.array([por[s] for s in sorted(por)])
        res["decodificador"][etq] = {
            "media": float(v.mean()), "sd": float(v.std(ddof=1)),
            "destacada": float(por[1]), "por_semilla": por}
        print(f"  {etq}: {v.mean():.2f} +- {v.std(ddof=1):.2f}, "
              f"destacada {por[1]:.2f}")

    print("\nC. G&T con los tres desempates, decodificador igual")
    for etq, pol in (("gt_spt", gt("spt")), ("gt_mwkr", gt("mwkr"))):
        m, _ = re_de(pol, insts)
        res["decodificador"][etq] = {"media": m}
        print(f"  {etq}: {m:.2f}")

    # el contraste pareado por instancia entre los dos decodificadores,
    # con la regla destacada, que es lo que aisla el decodificador
    from scipy import stats
    _, a = re_de(gp_semiactivo(arboles[1]), insts)
    _, b = re_de(gt("gp", "upper", arboles[1]), insts)
    w = stats.wilcoxon(a, b, method="exact", zero_method="wilcox")
    res["decodificador"]["contraste_destacada"] = {
        "d": float(np.mean(np.array(b) - np.array(a))),
        "p": float(w.pvalue)}
    print(f"\n  destacada, G&T menos semiactivo: "
          f"{np.mean(np.array(b) - np.array(a)):+.2f} (p={w.pvalue:.4f})")

    json.dump(res, open(SALIDA, "w", encoding="utf-8"), indent=1)
    print(f"\nescrito {SALIDA}")


if __name__ == "__main__":
    main()
