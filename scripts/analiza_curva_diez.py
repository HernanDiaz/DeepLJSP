# -*- coding: utf-8 -*-
"""La curva de presupuesto a diez tiradas, por tirada.

El deposito de 2026-08 guardaba tres tiradas y el mejor-de-B se
reconstruia repartiendo el presupuesto entre sus tres checkpoints, un
artefacto del barrido bo1024 original: por eso aquella curva solo
podia usarse por su forma. Con las diez tiradas del brazo principal
(342 rollouts por tirada e instancia) la reconstruccion pasa a ser la
del protocolo que el paper despliega: UNA politica gasta sus B
muestras, y la curva es la media sobre las diez tiradas.

Por tirada e instancia: el indice 0 es la pasada greedy y los 341
restantes las muestreadas. Para cada B se toma el mejor de B extraidos
sin reemplazo del pool de 341, promediado sobre repeticiones; el
greedy se reporta aparte. La banda de la figura es la dispersion
ENTRE TIRADAS, que es la que interesa (que compra una muestra mas en
una politica cualquiera), no el ruido del remuestreo.

Salida NUEVA: benchmarks/curva_diez/curva_diez.json

    python scripts/analiza_curva_diez.py
"""
import collections
import csv
import glob
import json
import os
import statistics
import sys

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SALIDA = "benchmarks/curva_diez/curva_diez.json"
N_POOL = 341
REPES = 200
PRESUPUESTOS = [1, 2, 3, 4, 6, 8, 12, 16, 32, 64, 128, 256, 341]
GP_UNA_PASADA = 17.71      # regla destacada, Tabla 7


def carga():
    """{(tirada, instancia): [mid...]} con el greedy aparte."""
    pools = collections.defaultdict(dict)
    lbs = {}
    ficheros = (["benchmarks/eval_budget_curve.csv"]
                + sorted(glob.glob("benchmarks/curva_diez/curva_*.csv")))
    for ruta in ficheros:
        if ruta.endswith("curva_diez.json"):
            continue
        for r in csv.DictReader(open(ruta, encoding="utf-8")):
            k = (r["checkpoint"], r["instance"])
            pools[k][int(r["sample_idx"])] = float(r["mid_comp"])
            lbs[r["instance"]] = float(r["lb"])
    return pools, lbs


def main():
    pools, lbs = carga()
    tiradas = sorted({k[0] for k in pools})
    print(f"tiradas: {len(tiradas)} -> {', '.join(tiradas)}")
    completas = [t for t in tiradas
                 if sum(1 for k in pools if k[0] == t) == 70
                 and all(len(v) >= 342 for k, v in pools.items()
                         if k[0] == t)]
    print(f"completas (70 instancias x 342 rollouts): {len(completas)}")

    rng = np.random.RandomState(20260818)
    # RE por (tirada, B) promediando las 70 instancias
    curva = collections.defaultdict(dict)
    greedy = {}
    for t in completas:
        gr = []
        for (tt, inst), v in pools.items():
            if tt != t:
                continue
            lb = lbs[inst]
            gr.append((v[0] - lb) / lb * 100)
        greedy[t] = statistics.mean(gr)
        for B in PRESUPUESTOS:
            acc = []
            for (tt, inst), v in pools.items():
                if tt != t:
                    continue
                lb = lbs[inst]
                muestras = np.array([v[i] for i in range(1, N_POOL + 1)])
                if B >= N_POOL:
                    mejor = muestras.min()
                    acc.append((mejor - lb) / lb * 100)
                    continue
                tot = 0.0
                for _ in range(REPES):
                    ix = rng.choice(N_POOL, B, replace=False)
                    tot += (muestras[ix].min() - lb) / lb * 100
                acc.append(tot / REPES)
            curva[t][B] = statistics.mean(acc)

    res = {"tiradas": completas, "presupuestos": PRESUPUESTOS,
           "greedy_por_tirada": {t: round(g, 4)
                                 for t, g in sorted(greedy.items())},
           "greedy_media": round(statistics.mean(greedy.values()), 4),
           "por_presupuesto": {}}
    print(f"\n  greedy: {res['greedy_media']:.2f} "
          f"(rango {min(greedy.values()):.2f}-{max(greedy.values()):.2f})")
    print(f"\n  {'B':>4}  {'RE medio':>8}  {'mejor':>7}  {'peor':>7}")
    for B in PRESUPUESTOS:
        vals = [curva[t][B] for t in completas]
        res["por_presupuesto"][str(B)] = {
            "media": round(statistics.mean(vals), 4),
            "sd": round(statistics.stdev(vals), 4),
            "mejor": round(min(vals), 4),
            "peor": round(max(vals), 4)}
        print(f"  {B:>4}  {statistics.mean(vals):8.2f}  "
              f"{min(vals):7.2f}  {max(vals):7.2f}")

    # los cruces que cita 7.2
    med = {B: res["por_presupuesto"][str(B)]["media"] for B in PRESUPUESTOS}
    cruce_gp = next((B for B in PRESUPUESTOS if med[B] < GP_UNA_PASADA),
                    None)
    cruce_gr = next((B for B in PRESUPUESTOS
                     if med[B] < res["greedy_media"]), None)
    res["cruce_gp"] = cruce_gp
    res["cruce_greedy"] = cruce_gr
    print(f"\n  adelanta a la regla ({GP_UNA_PASADA}) en B={cruce_gp}")
    print(f"  adelanta a su greedy ({res['greedy_media']:.2f}) en "
          f"B={cruce_gr}")

    # retorno por duplicacion en la cola
    oct_ = [(32, 64), (64, 128), (128, 256)]
    res["ganancia_por_duplicacion"] = {
        f"{a}->{b}": round(med[a] - med[b], 4) for a, b in oct_}
    print("\n  ganancia por duplicacion:",
          {k: v for k, v in res["ganancia_por_duplicacion"].items()})

    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    json.dump(res, open(SALIDA, "w", encoding="utf-8"), indent=2)
    print(f"\n  escrito {SALIDA}")


if __name__ == "__main__":
    main()
