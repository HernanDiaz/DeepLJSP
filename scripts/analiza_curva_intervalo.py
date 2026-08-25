# -*- coding: utf-8 -*-
"""La curva de presupuesto bajo el decodificador desplegado de 5.4.

Sustituye a analiza_curva_diez.py tras la revision del 2026-08-25
(R2-2): aquella reconstruccion excluia la pasada greedy del pool y
retenia por punto medio minimo, es decir, media otro decodificador.
Con los extremos guardados por eval_curva_intervalo.py el mejor-de-B
se reconstruye exactamente como se despliega: la pasada greedy mas
B-1 muestras extraidas sin reemplazo del pool de 341, retenidas por
el criterio lexicografico (U, L) de Eq. (2), y el RE del retenido se
reporta en punto medio como todo el paper. Para B=1 el protocolo ES
la pasada greedy. Se calcula ademas, sobre los mismos pools, la
variante que retiene por punto medio, para cuantificar cuanto separa
a los dos decodificadores.

Salida NUEVA: benchmarks/curva_intervalo/curva_intervalo.json

    python scripts/analiza_curva_intervalo.py
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

SALIDA = "benchmarks/curva_intervalo/curva_intervalo.json"
N_POOL = 341
REPES = 200
PRESUPUESTOS = [1, 2, 3, 4, 6, 8, 12, 16, 32, 64, 128, 256, 341]
GP_UNA_PASADA = 17.71      # regla destacada, Tabla 7


def carga():
    """{(tirada, instancia): {idx: (lo, up)}} y las cotas."""
    pools = collections.defaultdict(dict)
    lbs = {}
    for ruta in sorted(glob.glob("benchmarks/curva_intervalo/curva_*.csv")):
        for r in csv.DictReader(open(ruta, encoding="utf-8")):
            k = (r["checkpoint"], r["instance"])
            pools[k][int(r["sample_idx"])] = (float(r["lo"]),
                                              float(r["up"]))
            lbs[r["instance"]] = float(r["lb"])
    return pools, lbs


def re_de(par, lb):
    lo, up = par
    return ((lo + up) / 2 - lb) / lb * 100


def main():
    pools, lbs = carga()
    tiradas = sorted({k[0] for k in pools})
    print(f"tiradas: {len(tiradas)} -> {', '.join(tiradas)}")
    completas = [t for t in tiradas
                 if sum(1 for k in pools if k[0] == t) == 70
                 and all(len(v) >= N_POOL + 1 for k, v in pools.items()
                         if k[0] == t)]
    print(f"completas (70 instancias x 342 rollouts): {len(completas)}")

    rng = np.random.RandomState(20260825)
    curva = collections.defaultdict(dict)      # lexicografica (U, L)
    curva_mid = collections.defaultdict(dict)  # control: punto medio
    greedy = {}
    for t in completas:
        gr = []
        for (tt, inst), v in pools.items():
            if tt != t:
                continue
            gr.append(re_de(v[0], lbs[inst]))
        greedy[t] = statistics.mean(gr)
        for B in PRESUPUESTOS:
            acc_lex, acc_mid = [], []
            for (tt, inst), v in pools.items():
                if tt != t:
                    continue
                lb = lbs[inst]
                g = v[0]
                muestras = [v[i] for i in range(1, N_POOL + 1)]
                if B == 1:
                    acc_lex.append(re_de(g, lb))
                    acc_mid.append(re_de(g, lb))
                    continue
                tot_lex = tot_mid = 0.0
                for _ in range(REPES):
                    ix = rng.choice(N_POOL, B - 1, replace=False)
                    pool = [g] + [muestras[i] for i in ix]
                    mejor_lex = min(pool, key=lambda p: (p[1], p[0]))
                    mejor_mid = min(pool, key=lambda p: p[0] + p[1])
                    tot_lex += re_de(mejor_lex, lb)
                    tot_mid += re_de(mejor_mid, lb)
                acc_lex.append(tot_lex / REPES)
                acc_mid.append(tot_mid / REPES)
            curva[t][B] = statistics.mean(acc_lex)
            curva_mid[t][B] = statistics.mean(acc_mid)

    res = {"tiradas": completas, "presupuestos": PRESUPUESTOS,
           "protocolo": "greedy + (B-1) muestras, retenido por (U, L)",
           "greedy_por_tirada": {t: round(g, 4)
                                 for t, g in sorted(greedy.items())},
           "greedy_media": round(statistics.mean(greedy.values()), 4),
           "por_presupuesto": {}, "por_presupuesto_mid": {}}
    print(f"\n  greedy: {res['greedy_media']:.2f}")
    print(f"\n  {'B':>4}  {'lex (U,L)':>9}  {'mid':>7}  {'dif':>6}")
    for B in PRESUPUESTOS:
        vals = [curva[t][B] for t in completas]
        vals_m = [curva_mid[t][B] for t in completas]
        res["por_presupuesto"][str(B)] = {
            "media": round(statistics.mean(vals), 4),
            "sd": round(statistics.stdev(vals), 4),
            "mejor": round(min(vals), 4),
            "peor": round(max(vals), 4)}
        res["por_presupuesto_mid"][str(B)] = {
            "media": round(statistics.mean(vals_m), 4)}
        print(f"  {B:>4}  {statistics.mean(vals):9.2f}  "
              f"{statistics.mean(vals_m):7.2f}  "
              f"{statistics.mean(vals) - statistics.mean(vals_m):+6.3f}")

    med = {B: res["por_presupuesto"][str(B)]["media"] for B in PRESUPUESTOS}
    cruce_gp = next((B for B in PRESUPUESTOS if med[B] < GP_UNA_PASADA),
                    None)
    cruce_gr = next((B for B in PRESUPUESTOS
                     if med[B] < res["greedy_media"]), None)
    res["cruce_gp"] = cruce_gp
    res["cruce_greedy"] = cruce_gr
    print(f"\n  baja de la regla ({GP_UNA_PASADA}) en B={cruce_gp}")
    print(f"  mejora a su greedy ({res['greedy_media']:.2f}) en "
          f"B={cruce_gr}")

    oct_ = [(32, 64), (64, 128), (128, 256)]
    res["ganancia_por_duplicacion"] = {
        f"{a}->{b}": round(med[a] - med[b], 4) for a, b in oct_}
    print("  ganancia por duplicacion:",
          res["ganancia_por_duplicacion"])

    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    json.dump(res, open(SALIDA, "w", encoding="utf-8"), indent=2)
    print(f"\n  escrito {SALIDA}")


if __name__ == "__main__":
    main()
