# -*- coding: utf-8 -*-
"""Promedia las seis copias simultaneas de tiempos_fast.py.

Las seis se lanzan a la vez para medir con la misma carga que E6, que
corrio en seis carriles; el tiempo de cada metodo es la media de las
seis. Comprueba ademas que las seis dan el mismo RE.

    python scripts/tiempos_fast_promedia.py

Salida NUEVA: benchmarks/tiempos_fast.json
"""
import glob
import json
import sys

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

COPIAS = sorted(glob.glob("benchmarks/tiempos_fast_[0-9].json"))
assert len(COPIAS) == 6, COPIAS
R = [json.load(open(f, encoding="utf-8")) for f in COPIAS]

res = {"copias": len(R), "taillard": {}, "clasicas": {}}
for m in R[0]["taillard"]:
    v = [r["taillard"][m]["ms_media"] for r in R]
    fila = {"ms_media": float(np.mean(v)), "ms_copias": v}
    if "re" in R[0]["taillard"][m]:
        res_ = {r["taillard"][m]["re"] for r in R}
        assert len(res_) == 1, (m, res_)
        fila["re"] = R[0]["taillard"][m]["re"]
    res["taillard"][m] = fila
    print(f"{m:10} {fila['ms_media']:7.1f} ms  (copias {min(v):.1f}-{max(v):.1f})")
for n in R[0]["clasicas"]:
    una = float(np.mean([r["clasicas"][n]["una_s"] for r in R]))
    bon = float(np.mean([r["clasicas"][n]["bon1024_s"] for r in R]))
    res["clasicas"][n] = {"una_s": una, "bon1024_s": bon}
    print(f"{n:5} una {una * 1000:6.1f} ms  mejor-de-1024 {bon:6.2f} s")
u = [c["una_s"] for c in res["clasicas"].values()]
b = [c["bon1024_s"] for c in res["clasicas"].values()]
res["resumen_clasicas"] = {"una_min": min(u), "una_max": max(u),
                           "una_media": float(np.mean(u)),
                           "bon_min": min(b), "bon_max": max(b),
                           "bon_media": float(np.mean(b))}
print(res["resumen_clasicas"])

# las 30 reglas del brazo principal tal como se evolucionaron
# (tiempos_fast_brazo.py, tambien en seis copias); la destacada es la
# semilla 1, cuyo arbol sin simplificar es mas caro que ARBOL
B = [json.load(open(f, encoding="utf-8"))
     for f in sorted(glob.glob("benchmarks/tiempos_brazo_[0-9].json"))]
assert len(B) == 6, len(B)
reglas = sorted(glob.glob("benchmarks/reevo_fixedfit/gp_tuned_seed*.json"))
i1 = [f.replace("\\", "/").split("/")[-1] for f in reglas].index(
    "gp_tuned_seed1.json")
res["brazo"] = {"re_media": B[0]["re_media"],
                "ms_media": float(np.mean([b["ms_media"] for b in B])),
                "ms_destacada_arbol": float(np.mean(
                    [b["ms_por_regla"][i1] for b in B]))}
print(res["brazo"])
json.dump(res, open("benchmarks/tiempos_fast.json", "w", encoding="utf-8"),
          indent=1)
print("escrito benchmarks/tiempos_fast.json")
