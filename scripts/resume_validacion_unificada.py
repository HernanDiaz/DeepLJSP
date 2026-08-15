# -*- coding: utf-8 -*-
"""Reune el conjunto de validacion bajo un solo evaluador.

Hasta ahora la Tabla 7, la figura de escalado y las tres ablaciones
salian de la evaluacion que cada tirada de entrenamiento hace al
terminar, imposible de reproducir sin repetir el entrenamiento. Estos
CSV vienen de scripts/eval_val_brazos.py sobre los puntos de control
guardados: mismo protocolo (una pasada greedy y N-1 muestreadas,
ordenadas por el criterio lexicografico) y un unico flujo de aleatorios
para todos los brazos.

El brazo principal a 1000 episodios son las treinta semillas de la
campana, que ya se evaluaron asi para elegir la politica.

Salida NUEVA: benchmarks/ext30/validacion_unificada.json

    python scripts/resume_validacion_unificada.py
"""
import collections
import csv
import glob
import json
import os
import statistics
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SALIDA = "benchmarks/ext30/validacion_unificada.json"
VAL = [f"int__tai20_15_{k:02d}" for k in range(5, 11)]
ESPERADAS = {"v2-full-100ep": 10, "v2-full-300ep": 10,
             "v2-full-1000ep": 30, "v2-attn-300ep": 3,
             "v2-attn-1000ep": 10, "v2-nowidth-1000ep": 10,
             "v2-midpoint-1000ep": 10}


def main():
    brazos = collections.defaultdict(lambda: collections.defaultdict(dict))
    for f in sorted(glob.glob("benchmarks/ext30/val_*.csv")):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            brazos[r["arm"]][int(r["seed"])][r["instance"]] = (
                float(r["re_greedy"]), float(r["re_bo"]))
    # el brazo principal a 1000 episodios: las 30 de la campana
    for f in sorted(glob.glob("benchmarks/ext30/eval_val_bo64*.csv")):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            brazos["v2-full-1000ep"][int(r["seed"])][r["instance"]] = (
                float(r["re_greedy"]), float(r["re_bo"]))

    def resume(sem):
        """Estadisticos de un conjunto de semillas ya filtrado."""
        bo = {s: statistics.mean(v[i][1] for i in VAL)
              for s, v in sem.items()}
        gr = {s: statistics.mean(v[i][0] for i in VAL)
              for s, v in sem.items()}
        return {
            "n": len(sem),
            "bo64": round(statistics.mean(bo.values()), 4),
            "sd": round(statistics.stdev(bo.values()), 4),
            "mejor": round(min(bo.values()), 4),
            "peor": round(max(bo.values()), 4),
            "greedy": round(statistics.mean(gr.values()), 4),
            "por_instancia": {
                i: round(statistics.mean(v[i][1] for v in sem.values()), 4)
                for i in VAL},
            # el mejor por instancia es la mejor TIRADA en esa instancia,
            # nunca el mejor rollout dentro de una tirada: el best-of-N ya
            # esta agregado en re_bo
            "mejor_por_instancia": {
                i: round(min(v[i][1] for v in sem.values()), 4)
                for i in VAL},
            "por_semilla": {str(s): round(v, 4)
                            for s, v in sorted(bo.items())}}

    out, incompletos = {}, []
    print(f"  {'brazo':<22} {'n':>3}  {'bo64':>6} {'sd':>5}  "
          f"{'mejor':>6} {'greedy':>7}")
    for arm in ESPERADAS:
        sem = {s: v for s, v in brazos.get(arm, {}).items()
               if all(i in v for i in VAL)}
        if len(sem) != ESPERADAS[arm]:
            incompletos.append(f"{arm}: {len(sem)}/{ESPERADAS[arm]}")
        if not sem:
            continue
        out[arm] = resume(sem)
        print(f"  {arm:<22} {len(sem):>3}  {out[arm]['bo64']:6.2f} "
              f"{out[arm]['sd']:5.2f}  {out[arm]['mejor']:6.2f} "
              f"{out[arm]['greedy']:7.2f}")
        # la escalera de presupuesto se lee pareada: los brazos de 100 y
        # 300 episodios solo tienen diez semillas, asi que el de 1000
        # publica ademas su vista sobre esas mismas diez
        if arm == "v2-full-1000ep":
            diez = {s: v for s, v in sem.items() if 2 <= s <= 11}
            out[arm + "-diez"] = resume(diez)
            d = out[arm + "-diez"]
            print(f"  {arm + ' (10 sem.)':<22} {d['n']:>3}  {d['bo64']:6.2f} "
                  f"{d['sd']:5.2f}  {d['mejor']:6.2f} {d['greedy']:7.2f}")
    if incompletos:
        print(f"\n  AVISO brazos incompletos: {incompletos}")
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    json.dump(out, open(SALIDA, "w", encoding="utf-8"), indent=2)
    print(f"\n  escrito {SALIDA}")


if __name__ == "__main__":
    main()
