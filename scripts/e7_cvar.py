# -*- coding: utf-8 -*-
"""E7: la cola de la distribucion del makespan ejecutado (VaR y CVaR).

eps-barra (Eq. eps del articulo) es una desviacion MEDIA entre el makespan
ejecutado y el predicho. Un planificador que teme a los retrasos mira la
cola: que pasa en el 5 % de ejecuciones peores. Calamita et al. (2025)
miden el riesgo de un schedule fijo con el value-at-risk y el
conditional value-at-risk de su makespan; aqui se calculan los dos sobre
las mismas realizaciones Monte Carlo de E1.

Dos medidas de cola por (metodo, instancia), con alfa = 0.95:

  - cola del makespan: CVaR_alfa(C^ex), expresado como RE sobre la
    cota LB, comparable con la columna RE del articulo: mide el
    makespan de las peores ejecuciones, calidad y robustez juntas;
  - cola del exceso sobre la prediccion: CVaR_alfa(C^ex - E[C]), en
    unidades de tiempo: la contrapartida de cola, y de un solo lado,
    de la desviacion absoluta de E1.

El CVaR es la media de las ceil((1-alfa) K) realizaciones mayores (50
de 1000). Las realizaciones se regeneran con las semillas de
robustness_epsilon.py (numeros aleatorios comunes entre metodos), y el
script comprueba que reproduce el eps-barra y la desviacion absoluta de
benchmarks/e1_robustez/<ley>.csv celda a celda: si no, aborta, porque
eso querria decir que las reglas o las semillas no son las de E1.

Las reglas robustas representativas se eligen como en
cadena_pendientes.py: la de menor ancho relativo de su brazo.

    python scripts/e7_cvar.py

Salida NUEVA: benchmarks/e7_cvar/{por_instancia.csv, resumen.json}
"""
import csv
import json
import math
import os
import re
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")
sys.path.insert(0, "stochastic_experiment")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from cadena_pendientes import mejor_por_ancho                     # noqa: E402
from efecto import biserial                                       # noqa: E402
from robustness_epsilon import (heuristic_sequence, instance_arrays,  # noqa: E402
                                muestrea, predicted_midpoint)
from decode_vec import decode_mc                                  # noqa: E402
from jobshop_rl.data import PROBLEM_REGISTRY                      # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory     # noqa: E402
from jobshop_rl.heuristics.gp_rule import GPRuleHeuristic         # noqa: E402
from jobshop_rl.heuristics.strategies import ESTHeuristic, GTHeuristic  # noqa: E402

ALFA = 0.95
K = 1000
LEYES = ["uniform", "triangular", "pessimistic"]   # el caso peor es una
                                                   # sola realizacion
DIR = "benchmarks/e7_cvar"
E1 = "benchmarks/e1_robustez"
ORDEN = ["GP", "GP-nowidth", "GP-rob1", "GP-rob1-nw", "GP-rob4",
         "GT-MWKR", "EST"]
# los contrastes de E1, en el mismo orden
PARES = [("GP", "GP-nowidth"), ("GP-rob1", "GP"), ("GP-rob1", "GP-rob1-nw"),
         ("GP-rob4", "GP"), ("GP", "GT-MWKR"), ("GP", "EST"),
         ("GP-rob4", "GT-MWKR")]


def cola(x, alfa=ALFA):
    """(VaR, CVaR) empiricos de la muestra x al nivel alfa."""
    x = np.sort(np.asarray(x))
    k = int(math.ceil((1.0 - alfa) * len(x)))
    return float(x[-k]), float(x[-k:].mean())


def metodos():
    _, r1 = mejor_por_ancho("benchmarks/tuned/robust/width_seed*.json")
    _, r2 = mejor_por_ancho("benchmarks/tuned/robust/nowidth_seed*.json")
    _, r4 = mejor_por_ancho("benchmarks/tuned/lambda/lam4p0_seed*.json")
    print(f"reglas robustas: {r1}, {r2}, {r4}")

    def gp(f):
        return GPRuleHeuristic(json.load(open(f, encoding="utf-8"))["tree"])
    # el orden de construccion no importa: la semilla se reinicia por
    # metodo (numeros comunes), como en robustness_epsilon.py
    return {"GP": gp("benchmarks/reevo_fixedfit/gp_tuned_seed1.json"),
            "EST": ESTHeuristic(),
            "GT-MWKR": GTHeuristic(tiebreak="mwkr"),
            "GP-nowidth": gp("benchmarks/tuned/ablation/nowidth_seed25.json"),
            "GP-rob1": gp(r1), "GP-rob1-nw": gp(r2), "GP-rob4": gp(r4)}, \
        {"GP-rob1": r1, "GP-rob1-nw": r2, "GP-rob4": r4}


def referencia_e1(ley):
    """{(metodo, instancia): (eps_x1000, abs_dev)} a anchura nominal."""
    ruta = os.path.join(E1, f"{ley}.csv")
    assert os.path.exists(ruta), f"falta {ruta}"
    ref = {}
    for r in csv.DictReader(open(ruta, encoding="utf-8")):
        if float(r["width"]) == 1.0:
            ref[(r["method"], r["instance"])] = (float(r["eps_bar"]),
                                                 float(r["abs_dev"]))
    return ref


def pareado(x, y):
    x, y = np.asarray(x), np.asarray(y)
    dif = x - y
    w = stats.wilcoxon(x, y, method="exact", zero_method="wilcox")
    n = int(np.sum(np.abs(dif) > 1e-12))
    mu = n * (n + 1) / 4.0
    sd = (n * (n + 1) * (2 * n + 1) / 24.0) ** 0.5
    z = (float(w.statistic) - mu) / sd
    z = abs(z) if dif.mean() > 0 else -abs(z)
    return {"d": float(dif.mean()), "p": float(w.pvalue), "z": z,
            "rb": biserial(list(x), list(y)),
            "menor": int(np.sum(dif < 0)), "n": len(dif)}


def main():
    os.makedirs(DIR, exist_ok=True)
    mets, elegidas = metodos()
    todas = [p for p in sorted(PROBLEM_REGISTRY)
             if re.match(r"int__tai\d+_\d+_\d+$", p)]

    filas = []
    for ley in LEYES:
        ref = referencia_e1(ley)
        peor = 0.0
        for i, pid in enumerate(todas):
            lb = lb_for_problem_name(pid)
            if lb is None:
                continue
            lo, up, mseq = instance_arrays(pid)
            env = EnvironmentFactory.create_from_problem(
                PROBLEM_REGISTRY[pid](), "basic", seed=0)
            for m, h in mets.items():
                seq = heuristic_sequence(env, h)
                # la misma semilla que robustness_epsilon.py a anchura
                # nominal (wi = 0)
                rng = np.random.default_rng(1000 * i + 0)
                e_mid = predicted_midpoint(seq, lo, up, mseq)
                dur = muestrea(lo, up, K, rng, ley)
                cmax = np.asarray(decode_mc(seq, dur, mseq, K))
                eps = float(np.mean(np.abs(cmax - e_mid) / e_mid)) * 1000
                adev = float(np.mean(np.abs(cmax - e_mid)))
                e_ref, a_ref = ref[(m, pid)]
                peor = max(peor, abs(eps - e_ref), abs(adev - a_ref))
                var_c, cvar_c = cola(cmax)
                var_x, cvar_x = cola(cmax - e_mid)
                filas.append({"law": ley, "instance": pid, "method": m,
                              "lb": lb, "e_mid": e_mid,
                              "mean_cmax": float(cmax.mean()),
                              "var95_cmax": var_c, "cvar95_cmax": cvar_c,
                              "var95_over": var_x, "cvar95_over": cvar_x,
                              "re_mid": 100 * (e_mid - lb) / lb,
                              "re_cvar": 100 * (cvar_c - lb) / lb,
                              "eps_bar": eps, "abs_dev": adev})
            print(".", end="", flush=True)
        print(f"\n{ley}: mayor diferencia con E1 = {peor:.2e}")
        # las cifras de E1 van con cuatro decimales en el csv
        assert peor < 1e-3, f"{ley}: no reproduce E1 ({peor})"

    with open(os.path.join(DIR, "por_instancia.csv"), "w", newline="",
              encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=list(filas[0]))
        w.writeheader()
        for r in filas:
            w.writerow({k: (f"{v:.4f}" if isinstance(v, float) else v)
                        for k, v in r.items()})

    res = {"alfa": ALFA, "K": K, "reglas": elegidas, "leyes": {}}
    for ley in LEYES:
        d = {}
        for r in filas:
            if r["law"] == ley:
                d.setdefault(r["method"], {})[r["instance"]] = r
        insts = sorted(d["GP"])
        tabla = {}
        print(f"\n== {ley} ({len(insts)} instancias) ==")
        print(f"  {'metodo':<11} {'RE mid':>7} {'RE cvar':>8} "
              f"{'VaR exc':>8} {'CVaR exc':>9} {'abs':>7}")
        for m in ORDEN:
            v = {k: float(np.mean([d[m][i][k] for i in insts]))
                 for k in ("re_mid", "re_cvar", "var95_over", "cvar95_over",
                           "abs_dev", "e_mid", "cvar95_cmax")}
            tabla[m] = v
            print(f"  {m:<11} {v['re_mid']:7.2f} {v['re_cvar']:8.2f} "
                  f"{v['var95_over']:8.2f} {v['cvar95_over']:9.2f} "
                  f"{v['abs_dev']:7.2f}")
        contr = {}
        for x, y in PARES:
            c = {k: pareado([d[x][i][k] for i in insts],
                            [d[y][i][k] for i in insts])
                 for k in ("cvar95_over", "re_cvar")}
            contr[f"{x} vs {y}"] = c
            print(f"  {x + ' vs ' + y:<22} exc d={c['cvar95_over']['d']:+7.2f}"
                  f" z={c['cvar95_over']['z']:+6.2f}"
                  f" r={c['cvar95_over']['rb']:.2f}"
                  f" | cola RE d={c['re_cvar']['d']:+6.2f}"
                  f" z={c['re_cvar']['z']:+6.2f}"
                  f" r={c['re_cvar']['rb']:.2f}"
                  f" ({c['re_cvar']['menor']}/{c['re_cvar']['n']})")
        res["leyes"][ley] = {"metodos": tabla, "contrastes": contr,
                             "n_instancias": len(insts)}

    json.dump(res, open(os.path.join(DIR, "resumen.json"), "w",
                        encoding="utf-8"), indent=1)
    print(f"\nescrito {DIR}/resumen.json")


if __name__ == "__main__":
    main()
