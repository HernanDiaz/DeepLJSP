# -*- coding: utf-8 -*-
"""Cuanto cambia retener por el upper solo en vez de por (U, L).

La revision del 2026-08-26 senalo que AgentV2.evaluate_policy retenia
el mejor rollout por el extremo superior y rompia los empates por
orden de aparicion, no por el extremo inferior de la Eq. (3). El
defecto se corrigio; este script mide lo que habria cambiado, sobre el
deposito de la curva de presupuesto, que guarda los dos extremos de
239.400 rollouts.

    python scripts/mide_clave_retencion.py

Salida NUEVA: benchmarks/curva_intervalo/clave_retencion.json
"""
import csv, glob, collections, statistics
import numpy as np

pools = collections.defaultdict(dict)
lbs = {}
for ruta in sorted(glob.glob("benchmarks/curva_intervalo/curva_*.csv")):
    for r in csv.DictReader(open(ruta, encoding="utf-8")):
        pools[(r["checkpoint"], r["instance"])][int(r["sample_idx"])] = (
            float(r["lo"]), float(r["up"]))
        lbs[r["instance"]] = float(r["lb"])

rng = np.random.RandomState(11)
B = 64
REP = 40
dif, empates, unidades = [], 0, 0
for (ck, inst), v in pools.items():
    lb = lbs[inst]
    g = v[0]
    muestras = [v[i] for i in range(1, 342)]
    d_lex, d_up = [], []
    for _ in range(REP):
        ix = rng.choice(341, B - 1, replace=False)
        pool = [g] + [muestras[i] for i in ix]
        lex = min(pool, key=lambda p: (p[1], p[0]))
        # evaluate_policy: minimiza upper; en empate gana el primero visto
        mejor_up = None
        for p in pool:
            if mejor_up is None or p[1] < mejor_up[1]:
                mejor_up = p
        if lex != mejor_up:
            empates += 1
        d_lex.append(((lex[0] + lex[1]) / 2 - lb) / lb * 100)
        d_up.append(((mejor_up[0] + mejor_up[1]) / 2 - lb) / lb * 100)
    dif.append(statistics.mean(d_up) - statistics.mean(d_lex))
    unidades += REP

import json, os
res = {"presupuesto": B, "repeticiones": REP,
       "unidades": len(dif), "sorteos": unidades,
       "sorteos_que_difieren": empates,
       "pct_que_difieren": round(empates / unidades * 100, 4),
       "delta_re_medio": round(statistics.mean(dif), 4),
       "delta_re_max": round(max(dif), 4)}
os.makedirs("benchmarks/curva_intervalo", exist_ok=True)
json.dump(res, open("benchmarks/curva_intervalo/clave_retencion.json",
                    "w", encoding="utf-8"), indent=1)
print(f"unidades (instancia x tirada): {len(dif)}, sorteos: {unidades}")
print(f"sorteos donde la eleccion DIFIERE: {empates} ({empates/unidades*100:.2f}%)")
print(f"RE: upper-solo menos lex = {statistics.mean(dif):+.4f} puntos de media")
print(f"   maximo por unidad: {max(dif):+.4f}, minimo: {min(dif):+.4f}")
