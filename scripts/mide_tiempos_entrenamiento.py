# -*- coding: utf-8 -*-
"""Deriva el coste de pared de entrenar los treinta artefactos.

Politica: cada carpeta de entrenamiento registra su comienzo en el mtime
de global_training_log.csv (se escribe al arrancar) y su final en el de
best_model.pt (se escribe al terminar el entrenamiento, antes del test
embebido). La diferencia es el wall-clock de la semilla, con hasta tres
entrenamientos concurrentes en la maquina de la Tabla 3.

GP: la campana de re-evolucion de 2026-07-25 (mismo codigo y
configuracion que DiazGP2026: poblacion 100, 50 generaciones) corrio las
treinta evoluciones en tres carriles. Los mtimes de gp_tuned_seed*.json
marcan el final de cada una; el periodo entre lotes de tres estima el
wall-clock por evolucion en identicas condiciones de concurrencia.

Escribe benchmarks/tiempos/tiempos_entrenamiento.json.
"""
import json
import os
import statistics
from glob import glob

RAIZ = os.path.join(os.path.dirname(__file__), "..")
SALIDA = os.path.join(RAIZ, "benchmarks", "tiempos")

# --- politica: las treinta semillas del brazo principal -----------------
duraciones = {}
for d in sorted(glob(os.path.join(RAIZ, "outputs", "bench_v2-full-1000ep*"))):
    ini = os.path.join(d, "global_training_log.csv")
    fin = os.path.join(d, "best_model.pt")
    if not (os.path.exists(ini) and os.path.exists(fin)):
        continue
    semilla = os.path.basename(d).rsplit("_seed", 1)[1]
    duraciones[int(semilla)] = (os.path.getmtime(fin)
                                - os.path.getmtime(ini)) / 60.0
assert len(duraciones) == 30, f"esperaba 30 semillas, hay {len(duraciones)}"
mins = sorted(duraciones.values())

# --- GP: la re-evolucion de las treinta reglas --------------------------
fines = sorted(os.path.getmtime(f) for f in
               glob(os.path.join(RAIZ, "benchmarks", "reevo_fixedfit",
                                 "gp_tuned_seed*.json")))
assert len(fines) == 30, f"esperaba 30 evoluciones, hay {len(fines)}"
# t[2] cierra el primer lote de tres; quedan nueve lotes hasta t[29].
# Cada lote son tres evoluciones concurrentes, luego el periodo del lote
# es el wall-clock de una evolucion a tres carriles.
evo_min = (fines[29] - fines[2]) / 9 / 60.0

res = {
    "politica": {
        "por_semilla_min": {str(k): round(v, 1)
                            for k, v in sorted(duraciones.items())},
        "mediana_min": round(statistics.median(mins), 1),
        "min_min": round(mins[0], 1),
        "max_min": round(mins[-1], 1),
        "total_h_tres_carriles": round(sum(mins) / 3 / 60.0, 2),
    },
    "gp": {
        "evolucion_min": round(evo_min, 1),
        "total_h_tres_carriles": round(evo_min * 30 / 3 / 60.0, 2),
        "campana": "benchmarks/reevo_fixedfit, 2026-07-25",
    },
    "nota": "wall-clock por timestamps de ficheros; tres procesos "
            "concurrentes en ambas campanas",
}
os.makedirs(SALIDA, exist_ok=True)
ruta = os.path.join(SALIDA, "tiempos_entrenamiento.json")
with open(ruta, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2, ensure_ascii=False)
print(json.dumps({k: v for k, v in res.items() if k != "nota"},
                 indent=2, default=str)[:600])
print("escrito", ruta)
