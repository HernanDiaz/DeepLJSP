# -*- coding: utf-8 -*-
"""E0: reselecciona la regla destacada SOLO sobre el conjunto de desarrollo.

La revision r3 del envio a SWEVO senala que la regla destacada se eligio
mirando las setenta instancias, entre ellas las sesenta reservadas. El
paper lo declara, pero declararlo no lo arregla.

Este script comprueba si la seleccion sobre TA15--TA20, que es el
conjunto de desarrollo y nunca contribuye al fitness, devuelve la misma
regla. Si la devuelve, la contaminacion se elimina redefiniendo la regla
destacada sin tocar ninguna cifra del articulo.

Calcula ademas la media y la desviacion de las treinta reglas, que es lo
que el revisor pide como resultado principal.

    python scripts/e0_seleccion_desarrollo.py

Salida NUEVA: benchmarks/reevo_fixedfit/e0_seleccion.json
"""
import collections
import csv
import json
import os
import re
import sys

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FUENTE = "benchmarks/reevo_fixedfit/summary.csv"
SALIDA = "benchmarks/reevo_fixedfit/e0_seleccion.json"
DESARROLLO = {f"int__tai20_15_{k:02d}" for k in range(5, 11)}   # TA15-TA20
ENTRENA = {f"int__tai20_15_{k:02d}" for k in range(1, 5)}       # TA11-TA14


def main():
    por = collections.defaultdict(dict)
    for r in csv.DictReader(open(FUENTE, encoding="utf-8")):
        m = re.fullmatch(r"gp_tuned_seed(\d+)", r["method"])
        if m:
            por[int(m.group(1))][r["instance"]] = float(r["re"])

    semillas = sorted(por)
    assert len(semillas) == 30, f"{len(semillas)} reglas"
    instancias = sorted(por[semillas[0]])
    assert len(instancias) == 70, f"{len(instancias)} instancias"

    no_vistas = [i for i in instancias
                 if i not in DESARROLLO and i not in ENTRENA]
    print(f"{len(semillas)} reglas, {len(instancias)} instancias "
          f"({len(DESARROLLO)} de desarrollo, {len(no_vistas)} reservadas)")

    def media(sem, conj):
        return float(np.mean([por[sem][i] for i in conj]))

    todas = {s: media(s, instancias) for s in semillas}
    desa = {s: media(s, sorted(DESARROLLO)) for s in semillas}
    resto = {s: media(s, no_vistas) for s in semillas}

    g_todas = min(todas, key=todas.get)
    g_desa = min(desa, key=desa.get)

    orden_d = sorted(semillas, key=desa.get)
    orden_t = sorted(semillas, key=todas.get)

    print(f"\nganadora sobre las 70        : seed{g_todas}  "
          f"({todas[g_todas]:.4f}%)")
    print(f"ganadora sobre desarrollo    : seed{g_desa}  "
          f"({desa[g_desa]:.4f}% en desarrollo, "
          f"{todas[g_desa]:.4f}% en las 70)")
    print(f"coinciden: {'SI' if g_todas == g_desa else 'NO'}")

    print(f"\nsegunda en desarrollo        : seed{orden_d[1]}  "
          f"({desa[orden_d[1]]:.4f}%)")
    print(f"segunda sobre las 70         : seed{orden_t[1]}  "
          f"({todas[orden_t[1]]:.4f}%)")

    v = np.array([todas[s] for s in semillas])
    vr = np.array([resto[s] for s in semillas])
    print(f"\nlas 30 sobre las 70          : {v.mean():.4f} +- {v.std(ddof=1):.4f}"
          f"  (min {v.min():.4f}, max {v.max():.4f})")
    print(f"las 30 sobre las 60 reservadas: {vr.mean():.4f} +- "
          f"{vr.std(ddof=1):.4f}")

    res = {
        "n_reglas": len(semillas),
        "ganadora_70": g_todas, "ganadora_desarrollo": g_desa,
        "coinciden": g_todas == g_desa,
        "re_ganadora_70_sobre_70": todas[g_todas],
        "re_ganadora_desarrollo_sobre_70": todas[g_desa],
        "re_ganadora_desarrollo_sobre_desarrollo": desa[g_desa],
        "ranking_desarrollo": [{"seed": s, "re_desarrollo": desa[s],
                                "re_70": todas[s]} for s in orden_d],
        "treinta_sobre_70": {"media": float(v.mean()),
                             "sd": float(v.std(ddof=1)),
                             "min": float(v.min()), "max": float(v.max())},
        "treinta_sobre_60": {"media": float(vr.mean()),
                             "sd": float(vr.std(ddof=1))},
    }
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    json.dump(res, open(SALIDA, "w", encoding="utf-8"), indent=1)
    print(f"\nescrito {SALIDA}")


if __name__ == "__main__":
    main()
