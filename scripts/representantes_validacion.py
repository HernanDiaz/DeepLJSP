# -*- coding: utf-8 -*-
"""Representantes de cada brazo elegidos en validacion (TA15-TA20).

La Tabla 9 de paper_caie representa los brazos robustos por su regla mas
estrecha en validacion y los ablados por su mejor regla en las 70
instancias. Este script recalcula, para cada brazo, que semilla sale con
cada criterio, y lo guarda en benchmarks/representantes_validacion.json
para que verify_numbers.py compruebe que los representantes del
experimento de robustez (logs/lanza_e1.bat) son los que dice el texto.
"""
import glob, json, os, re, sys
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
os.chdir(RAIZ)
from jobshop_rl.data import PROBLEM_REGISTRY as R
from jobshop_rl.data.literature_bounds import lb_for_problem_name
from jobshop_rl.heuristics.fast_regla import despachador
from jobshop_rl.heuristics.fast_sim import Instancia

IDS = sorted(x for x in R if x.startswith("int__tai") and "100_20" not in x)
assert len(IDS) == 70
VAL = [f"int__tai20_15_{k:02d}" for k in range(5, 11)]
INST = {p: (Instancia(R[p]()), lb_for_problem_name(p)) for p in IDS}
# brazo: (patron de reglas, criterio, semilla usada en el experimento E1)
BRAZOS = {
    "makespan-nowidth": ("benchmarks/tuned/ablation/nowidth_seed*.json", "re", 25),
    "robust1-full": ("benchmarks/tuned/robust/width_seed*.json", "w", 13),
    "robust1-nowidth": ("benchmarks/tuned/robust/nowidth_seed*.json", "w", 8),
    "lam4": ("benchmarks/tuned/lambda/lam4p0_seed*.json", "w", 10),
}


def mide(desp, ps):
    re_, w = 0.0, 0.0
    for p in ps:
        i, lb = INST[p]
        lo, up = desp(i)
        mid = (lo + up) / 2
        re_ += (mid - lb) / lb * 100
        w += (up - lo) / mid * 100
    return re_ / len(ps), w / len(ps)


salida = {}
for nombre, (pat, crit, usada) in BRAZOS.items():
    filas = {}
    for f in glob.glob(pat):
        s = int(re.search(r"seed(\d+)", f).group(1))
        d = despachador(json.load(open(f, encoding="utf-8"))["tree"])
        filas[s] = {"val": mide(d, VAL), "todas": mide(d, IDS)}
    k = 0 if crit == "re" else 1
    salida[nombre] = {
        "criterio": crit, "semilla_usada": usada, "n": len(filas),
        "elegida_validacion": min(filas, key=lambda s: filas[s]["val"][k]),
        "elegida_70": min(filas, key=lambda s: filas[s]["todas"][k]),
    }
    print(nombre, salida[nombre])
json.dump(salida, open("benchmarks/representantes_validacion.json", "w"), indent=1)
