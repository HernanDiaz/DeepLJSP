# -*- coding: utf-8 -*-
"""El enfrentamiento DRL-GP sobre instancias NO VISTAS, por tamano.

La revision del 2026-08-27 senalo que el contraste agregado de 6.2 corre
sobre las 70 Taillard, diez de las cuales (TA11-TA20, la clase 20x15)
son las de entrenamiento y validacion de AMBAS familias. Este script
recomputa los contrastes sobre las 60 restantes y los separa por
regimen de tamano, porque el agregado de las 60 esconde una
cancelacion: la politica gana con claridad hasta 30x20 y pierde con
claridad en 50xN.

    python scripts/enfrenta_no_vistas.py

Salida NUEVA: benchmarks/ext30/no_vistas.json
"""
import csv
import importlib.util
import json
import os
import statistics
import sys

sys.path.insert(0, ".")

from scipy import stats                                    # noqa: E402

SALIDA = "benchmarks/ext30/no_vistas.json"
CLASES = ["15x15", "20x15", "20x20", "30x15", "30x20", "50x15", "50x20"]


def _modulo():
    spec = importlib.util.spec_from_file_location(
        "eg", "scripts/enfrenta_gp_treinta.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def clase(ta):
    return CLASES[(int(ta[2:]) - 1) // 10]


def contrasta(a, b, tas):
    d = [a[t] - b[t] for t in tas]
    return {"n": len(tas),
            "media_politica": round(statistics.mean(a[t] for t in tas), 4),
            "media_gp": round(statistics.mean(b[t] for t in tas), 4),
            "dif_media": round(statistics.mean(d), 4),
            "gana_politica": sum(1 for x in d if x < 0),
            "p": float(stats.wilcoxon(d, method="exact").pvalue)}


def main():
    eg = _modulo()
    pol, gp = eg.politica_por_instancia(), eg.gp_por_instancia()
    todas = sorted(set(pol) & set(gp), key=lambda t: int(t[2:]))
    if len(todas) != 70:
        raise SystemExit(f"faltan instancias: {len(todas)}")

    pol_med = {t: statistics.mean(pol[t].values()) for t in todas}
    gp_med = {t: statistics.mean(gp[t].values()) for t in todas}
    camp = {"1": {t: pol[t][5] for t in todas}}
    for etq in ("bo64", "bo1024"):
        camp[etq] = eg.campeon_por_instancia(etq)
    gp_bon = {}
    for r in csv.DictReader(open("benchmarks/gp_destacada/gp_destacada_presupuestos.csv",
                                 encoding="utf-8")):
        gp_bon[eg.ta_de(r["instance"])] = {
            "bo64": float(r["best_at_64"]),
            "bo1024": float(r["best_at_1024"])}
    gp_dest = {"1": {t: gp[t][1] for t in todas},
               "bo64": {t: gp_bon[t]["bo64"] for t in todas},
               "bo1024": {t: gp_bon[t]["bo1024"] for t in todas}}

    grupos = {
        "sesenta_no_vistas": [t for t in todas if clase(t) != "20x15"],
        "hasta_30x20": [t for t in todas
                        if clase(t) not in ("20x15", "50x15", "50x20")],
        "cincuenta_xN": [t for t in todas
                         if clase(t) in ("50x15", "50x20")],
    }

    res = {}
    for nombre, tas in grupos.items():
        res[nombre] = {
            "1pass_medias30": contrasta(pol_med, gp_med, tas),
            "1pass_elegido": contrasta(camp["1"], gp_dest["1"], tas),
            "bo64_elegido": contrasta(camp["bo64"], gp_dest["bo64"], tas),
            "bo1024_elegido": contrasta(camp["bo1024"],
                                        gp_dest["bo1024"], tas)}
        print(f"{nombre} (n={len(tas)}):")
        for k, v in res[nombre].items():
            print(f"   {k:16s} {v['media_politica']:6.2f} vs "
                  f"{v['media_gp']:6.2f}  dif {v['dif_media']:+5.2f}  "
                  f"gana {v['gana_politica']}/{v['n']}  p={v['p']:.4f}")
        print()

    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    json.dump(res, open(SALIDA, "w", encoding="utf-8"), indent=2)
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
