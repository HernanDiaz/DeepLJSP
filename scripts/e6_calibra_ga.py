# -*- coding: utf-8 -*-
"""E6, paso previo: comprobar que el genetico de referencia no es un
espantapajaros.

Toda la comparacion a presupuesto igualado carece de valor si la
metaheuristica contra la que se mide esta mal configurada. Aqui se
barren cuatro configuraciones a presupuesto alto y, sobre todo, se
contrasta el genetico contra la cifra PUBLICADA del genetico para el
IJSP en las doce instancias clasicas, que es el unico punto externo de
calibracion disponible.

Si el genetico de este repositorio queda muy por debajo de la cifra
publicada, cualquier conclusion de E6 sobre "el regimen en que la regla
gana" estaria inflada, y hay que decirlo o arreglarlo antes.

    python scripts/e6_calibra_ga.py

Salida NUEVA: benchmarks/e6_presupuesto/calibracion.json
"""
import json
import os
import random
import sys
import time

import numpy as np

sys.path.insert(0, ".")
os.environ.setdefault("OMP_NUM_THREADS", "1")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data import PROBLEM_REGISTRY                   # noqa: E402
from jobshop_rl.data.literature_bounds import (                # noqa: E402
    lb_for_problem_name)
from jobshop_rl.heuristics.fast_sim import Instancia           # noqa: E402
from jobshop_rl.heuristics.ga_interval import evoluciona       # noqa: E402

DIR = "benchmarks/e6_presupuesto"
SALIDA = os.path.join(DIR, "calibracion.json")
PRESUPUESTO = 200000
PUNTOS = [20000, 50000, 100000, 200000]
CONFIGS = [(100, 3, 0.2), (250, 3, 0.2), (100, 2, 0.5), (250, 5, 0.3)]
# las cuatro 20x15 de entrenamiento, que es donde el articulo mira
CALIBRA = [f"int__tai20_15_{k:02d}" for k in (1, 2, 3, 4)]


def re_de(cm, lb):
    return ((cm[0] + cm[1]) / 2 - lb) / lb * 100


def main():
    os.makedirs(DIR, exist_ok=True)
    res = {"presupuesto": PRESUPUESTO, "puntos": PUNTOS, "configs": {}}
    print(f"RE a {PRESUPUESTO} decodificaciones, media de "
          f"{len(CALIBRA)} instancias 20x15\n")
    print(f"  {'config':<18} " + " ".join(f"{p // 1000:>6}k" for p in PUNTOS))
    for pop, tor, pm in CONFIGS:
        por_punto = {p: [] for p in PUNTOS}
        t0 = time.time()
        for pid in CALIBRA:
            inst = Instancia(PROBLEM_REGISTRY[pid]())
            lb = lb_for_problem_name(pid)
            c, _ = evoluciona(inst, PRESUPUESTO, random.Random(1), pop=pop,
                              torneo=tor, p_muta=pm, puntos=list(PUNTOS))
            for p in PUNTOS:
                por_punto[p].append(re_de(c[p], lb))
        etq = f"pop{pop} tor{tor} pm{pm}"
        res["configs"][etq] = {str(p): float(np.mean(v))
                               for p, v in por_punto.items()}
        res["configs"][etq]["segundos"] = time.time() - t0
        print(f"  {etq:<18} " +
              " ".join(f"{np.mean(por_punto[p]):7.2f}" for p in PUNTOS))

    mejor = min(res["configs"],
                key=lambda k: res["configs"][k][str(PRESUPUESTO)])
    res["mejor"] = mejor
    print(f"\n  mejor configuracion: {mejor}")
    json.dump(res, open(SALIDA, "w", encoding="utf-8"), indent=1)
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
