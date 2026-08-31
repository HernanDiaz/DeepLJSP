# -*- coding: utf-8 -*-
"""Cuanto lleva la campana de las treinta reglas a presupuesto 64.

    python scripts/estado_gp30.py
"""
import collections
import csv
import glob
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OBJETIVO = 30 * 70          # pares (regla, instancia)
N_POOL = 64

hechos = collections.Counter()
for ruta in sorted(glob.glob("benchmarks/gp_treinta_bo64/pool_*.csv")):
    for r in csv.DictReader(open(ruta, encoding="utf-8")):
        hechos[(int(r["rule_seed"]), r["instance"])] += 1

completos = sum(1 for v in hechos.values() if v >= N_POOL)
print(f"pares completos: {completos}/{OBJETIVO} "
      f"({100 * completos / OBJETIVO:.1f}%)")
print(f"rollouts escritos: {sum(hechos.values())}/{OBJETIVO * N_POOL}")

por_regla = collections.Counter()
for (sem, _), v in hechos.items():
    if v >= N_POOL:
        por_regla[sem] += 1
listas = sum(1 for s in por_regla.values() if s == 70)
print(f"reglas con las 70 instancias: {listas}/30")

for ruta in sorted(glob.glob("logs/gp30_*.log")):
    n = sum(1 for _ in open(ruta, encoding="utf-8", errors="replace"))
    edad = ""
    if os.path.exists(ruta):
        import time
        edad = f", ultimo cambio hace {(time.time() - os.path.getmtime(ruta)) / 60:.0f} min"
    print(f"  {os.path.basename(ruta)}: {n} lineas{edad}")
