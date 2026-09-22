# -*- coding: utf-8 -*-
"""E6, calibracion externa: el genetico de este repositorio contra el
genetico PUBLICADO, en las doce clasicas.

Es el unico punto de contraste externo que existe. Si el genetico de
aqui queda muy por debajo del publicado sobre las mismas instancias y la
misma metrica, entonces el punto de cruce que E6 reporte estaria inflado
a favor de la regla, y el articulo tiene que decirlo. Si queda cerca, la
comparacion a presupuesto igualado mide metodos y no implementaciones.

El presupuesto se barre en decodificaciones, que es la moneda
independiente de la implementacion.

    python scripts/e6_calibra_clasicas.py --presupuesto 200000

Salida NUEVA: benchmarks/e6_presupuesto/calibracion_clasicas.json
"""
import argparse
import importlib.util
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

from jobshop_rl.heuristics.fast_sim import (                   # noqa: E402
    Instancia, despacha, prioridad_de)
from jobshop_rl.heuristics.ga_interval import evoluciona       # noqa: E402

DIR = "benchmarks/e6_presupuesto"
SALIDA = os.path.join(DIR, "calibracion_clasicas.json")
# la regla destacada del articulo, tal como se evoluciono
ARBOL = ("sub", ("sub", ("mul", "SLACK", "SLACK"),
                 ("sub", "WKR", ("add", "PT", "PT"))),
         ("add", "WKRW", "ONE"))


def modulo_clasicas():
    """Reutiliza el cargador y las tablas publicadas de eval_classic12."""
    spec = importlib.util.spec_from_file_location(
        "ec12", os.path.join("scripts", "eval_classic12.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--presupuesto", type=int, default=200000)
    ap.add_argument("--semillas", type=int, default=3)
    args = ap.parse_args()
    puntos = [p for p in (1000, 10000, 50000, 100000, 200000, 500000)
              if p <= args.presupuesto]

    ec = modulo_clasicas()
    os.makedirs(DIR, exist_ok=True)
    pol = prioridad_de(ARBOL)

    filas, res = {}, {"presupuesto": args.presupuesto, "puntos": puntos,
                      "semillas": args.semillas, "instancias": {}}
    print(f"{'inst':<6} {'LB':>6} {'regla':>7} " +
          " ".join(f"{p // 1000:>6}k" for p in puntos) +
          f" {'GA pub':>7} {'ESABC':>7}")
    for nombre, fich in ec.FILES.items():
        datos = ec.load_instance(os.path.join(ec.DIR, fich), nombre)
        inst = Instancia(datos)
        lb = ec.LB[nombre]

        def re_(cm):
            return ((cm[0] + cm[1]) / 2 - lb) / lb * 100

        regla = re_(despacha(inst, pol))
        por_punto = {p: [] for p in puntos}
        t0 = time.time()
        for s in range(1, args.semillas + 1):
            c, _ = evoluciona(inst, args.presupuesto, random.Random(s),
                              puntos=list(puntos))
            for p in puntos:
                por_punto[p].append(re_(c[p]))
        fila = {"lb": lb, "regla": regla,
                "ga": {str(p): float(np.mean(v))
                       for p, v in por_punto.items()},
                "ga_sd": {str(p): float(np.std(v, ddof=1)) if len(v) > 1
                          else 0.0 for p, v in por_punto.items()},
                "pub": ec.PUB_AVG[nombre], "segundos": time.time() - t0}
        res["instancias"][nombre] = fila
        filas[nombre] = fila
        print(f"{nombre:<6} {lb:>6} {regla:>7.1f} " +
              " ".join(f"{np.mean(por_punto[p]):7.1f}" for p in puntos) +
              f" {ec.PUB_AVG[nombre]['GA']:>7.1f}"
              f" {ec.PUB_AVG[nombre]['ESABC']:>7.1f}", flush=True)

    def media(f):
        return float(np.mean([f(v) for v in filas.values()]))

    res["medias"] = {
        "regla": media(lambda v: v["regla"]),
        "ga": {str(p): media(lambda v: v["ga"][str(p)]) for p in puntos},
        "ga_publicado": media(lambda v: v["pub"]["GA"]),
        "esabc_publicado": media(lambda v: v["pub"]["ESABC"])}
    print(f"\n{'MEDIA':<6} {'':>6} {res['medias']['regla']:>7.1f} " +
          " ".join(f"{res['medias']['ga'][str(p)]:7.1f}" for p in puntos) +
          f" {res['medias']['ga_publicado']:>7.1f}"
          f" {res['medias']['esabc_publicado']:>7.1f}")

    fin = res["medias"]["ga"][str(puntos[-1])]
    pub = res["medias"]["ga_publicado"]
    res["veredicto"] = ("el genetico de aqui alcanza al publicado"
                        if fin <= pub else
                        f"queda {fin - pub:.1f} puntos por encima del publicado")
    print(f"\nveredicto: {res['veredicto']}")
    json.dump(res, open(SALIDA, "w", encoding="utf-8"), indent=1)
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
