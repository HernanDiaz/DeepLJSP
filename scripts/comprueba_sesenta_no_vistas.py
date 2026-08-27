# -*- coding: utf-8 -*-
"""El enfrentamiento DRL-GP restringido a las 60 instancias no vistas.

La revision del 2026-08-27 senalo que el contraste de 6.2 corre sobre
las 70 Taillard, diez de las cuales (TA11-TA20, la clase 20x15) son
las de entrenamiento y validacion de AMBAS familias. Este script
recomputa los mismos contrastes excluyendolas, para separar lo que se
sostiene fuera de la distribucion de entrenamiento de lo que no.

    python scripts/comprueba_sesenta_no_vistas.py
"""
import sys, statistics
sys.path.insert(0, ".")
sys.argv = ["x"]
from scipy import stats
import importlib.util
spec = importlib.util.spec_from_file_location(
    "eg", "scripts/enfrenta_gp_treinta.py")
eg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(eg)

pol = eg.politica_por_instancia()
gp = eg.gp_por_instancia()
todas = sorted(set(pol) & set(gp), key=lambda t: int(t[2:]))
vistas = {f"TA{k}" for k in range(11, 21)}
sesenta = [t for t in todas if t not in vistas]
print(f"70 -> {len(sesenta)} no vistas (excluidas TA11-TA20)\n")

pol_med = {t: statistics.mean(pol[t].values()) for t in todas}
gp_med = {t: statistics.mean(gp[t].values()) for t in todas}
camp = {"1": {t: pol[t][5] for t in todas}}
for etq in ("bo64", "bo1024"):
    v = eg.campeon_por_instancia(etq)
    if len(v) == 70:
        camp[etq] = v
import csv
gp_bon = {}
for r in csv.DictReader(open("benchmarks/fair_gp_eps.csv", encoding="utf-8")):
    gp_bon[eg.ta_de(r["instance"])] = {"bo64": float(r["best_at_64"]),
                                       "bo1024": float(r["best_at_1024"])}
gp_dest = {"1": {t: gp[t][1] for t in todas},
           "bo64": {t: gp_bon[t]["bo64"] for t in todas},
           "bo1024": {t: gp_bon[t]["bo1024"] for t in todas}}


def prueba(nombre, a, b, tas):
    d = [a[t] - b[t] for t in tas]
    p = float(stats.wilcoxon(d, method="exact").pvalue)
    gana = sum(1 for x in d if x < 0)
    print(f"  {nombre:<32} {statistics.mean(a[t] for t in tas):6.2f} vs "
          f"{statistics.mean(b[t] for t in tas):6.2f}  "
          f"gana {gana}/{len(tas)}  p={p:.4f}")


for etiqueta, tas in (("LAS 70 (lo que imprime el paper)", todas),
                      ("LAS 60 NO VISTAS", sesenta)):
    print(etiqueta + ":")
    prueba("1 pasada: 30 pol vs 30 GP", pol_med, gp_med, tas)
    prueba("1 pasada: campeon vs destacada", camp["1"], gp_dest["1"], tas)
    prueba("64: campeon vs destacada", camp["bo64"], gp_dest["bo64"], tas)
    prueba("1024: campeon vs destacada", camp["bo1024"], gp_dest["bo1024"], tas)
    print()
