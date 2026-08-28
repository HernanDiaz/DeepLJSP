# -*- coding: utf-8 -*-
"""Presupuestos de la regla GP destacada, con el protocolo desplegado.

Del deposito de eval_gp_destacada_pool.py (los dos extremos de 1024
rollouts por instancia, el 0 determinista y el resto epsilon-greedy)
calcula el mejor-de-B con el criterio de la Eq. (3): la pasada
determinista mas B-1 muestras, retenidas por (U, L). Es el mismo
protocolo con el que se lee la politica, de modo que las dos familias
quedan bajo reglas identicas y regenerables desde este paquete.

    python scripts/analiza_gp_destacada.py

Salida NUEVA: benchmarks/gp_destacada/gp_destacada_presupuestos.csv
"""
import csv
import collections
import glob
import os
import sys


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SALIDA = "benchmarks/gp_destacada/gp_destacada_presupuestos.csv"
CORTES = (1, 16, 64, 256, 1024)


def main():
    pools, lbs = collections.defaultdict(dict), {}
    for ruta in sorted(glob.glob("benchmarks/gp_destacada/pool_*.csv")):
        for r in csv.DictReader(open(ruta, encoding="utf-8")):
            pools[r["instance"]][int(r["sample_idx"])] = (float(r["lo"]),
                                                          float(r["up"]))
            lbs[r["instance"]] = float(r["lb"])
    completas = {i: v for i, v in pools.items() if len(v) >= 1024}
    if len(completas) != 70:
        sys.exit(f"ABORTA: {len(completas)}/70 instancias completas")

    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    with open(SALIDA, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["instance", "lb"] + [f"best_at_{n}" for n in CORTES]
                   + ["mean"])
        medias = collections.defaultdict(list)
        for inst in sorted(completas):
            v, lb = completas[inst], lbs[inst]
            det = v[0]
            muestras = [v[i] for i in range(1, 1024)]
            re_de = lambda p: ((p[0] + p[1]) / 2 - lb) / lb * 100
            fila = [inst, lb]
            for n in CORTES:
                if n == 1:
                    val = re_de(det)
                elif n >= 1024:
                    pool = [det] + muestras
                    val = re_de(min(pool, key=lambda p: (p[1], p[0])))
                else:
                    # UNA ejecucion, como el brazo de la politica: la
                    # pasada determinista mas las n-1 primeras muestras
                    # del pool, sin promediar sorteos. La comparacion la
                    # sostienen los contrastes pareados por instancia
                    pool = [det] + muestras[:n - 1]
                    val = re_de(min(pool, key=lambda p: (p[1], p[0])))
                fila.append(f"{val:.4f}")
                medias[n].append(val)
            m = sum(re_de(p) for p in [det] + muestras) / 1024
            fila.append(f"{m:.4f}")
            medias["mean"].append(m)
            w.writerow(fila)
    print(f"{'presupuesto':>12s} {'RE medio':>9s}")
    for n in CORTES:
        print(f"{n:>12d} {sum(medias[n]) / 70:9.4f}")
    print(f"{'media pool':>12s} {sum(medias['mean']) / 70:9.4f}")
    print(f"\nescrito {SALIDA}")


if __name__ == "__main__":
    main()
