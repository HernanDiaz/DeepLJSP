# -*- coding: utf-8 -*-
"""El enfrentamiento con el GP, simetrico, sobre las 70 instancias.

Cada comparacion enfrenta treinta artefactos contra treinta, al mismo
presupuesto de inferencia y con la misma unidad muestral (la instancia,
Seccion 5.1):

  media contra media   las 30 evoluciones contra las 30 semillas, cada
                       lado promediado por instancia antes del test
  elegido contra elegido  la regla destacada del estudio del GP, mejor
                       de sus 30 sobre estas mismas 70, contra nuestro
                       campeon, mejor de 30 sobre validacion

Salida NUEVA: benchmarks/ext30/enfrentamiento70.json

    python scripts/enfrenta_gp_treinta.py
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

from scipy import stats                                        # noqa: E402

SALIDA = "benchmarks/ext30/enfrentamiento70.json"
TA_BASE = {"15_15": 0, "20_15": 10, "20_20": 20, "30_15": 30,
           "30_20": 40, "50_15": 50, "50_20": 60}


def ta_de(nombre):
    import re
    m = re.search(r"tai(\d+_\d+)_(\d+)", nombre.lower())
    return f"TA{TA_BASE[m.group(1)] + int(m.group(2))}"


def politica_por_instancia():
    """{TA: {semilla: RE}} a una pasada, de las tres procedencias."""
    out = collections.defaultdict(dict)
    for r in csv.DictReader(open("benchmarks/fair_v2_greedy.csv",
                                 encoding="utf-8")):
        s = int(r["checkpoint"].split("seed")[1].split(".")[0])
        out[ta_de(r["instance"])][s] = float(r["re_mid"])
    for r in csv.DictReader(open("benchmarks/eval70_diez_semillas.csv",
                                 encoding="utf-8")):
        out[ta_de(r["instance"])][int(r["seed"])] = float(r["re_greedy"])
    for f in sorted(glob.glob("benchmarks/ext30/eval70_greedy_*.csv")):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            out[ta_de(r["instance"])][int(r["seed"])] = float(r["re_greedy"])
    return out


def gp_por_instancia():
    """{TA: {evolucion: RE}} a una pasada, deposito publicado."""
    out = collections.defaultdict(dict)
    for r in csv.DictReader(open("benchmarks/reevo_fixedfit/summary.csv",
                                 encoding="utf-8")):
        fam, _, sem = r["method"].rpartition("_seed")
        if fam == "gp_tuned":
            out[ta_de(r["instance"])][int(sem)] = float(r["re"])
    return out


def campeon_por_instancia(etq):
    out = {}
    for f in sorted(glob.glob(f"benchmarks/ext30/camp_{etq}_*.csv")):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            out[ta_de(r["instance"])] = float(r["re_bo"])
    return out


def contrasta(nombre, a, b, tas):
    """a menos b instancia a instancia; a favor de a si negativo."""
    d = [a[t] - b[t] for t in tas]
    gana = sum(1 for x in d if x < 0)
    p = float(stats.wilcoxon(d, method="exact").pvalue)
    print(f"  {nombre:<34} {statistics.mean(a[t] for t in tas):6.2f} vs "
          f"{statistics.mean(b[t] for t in tas):6.2f}   gana en {gana}/70   "
          f"mediana {statistics.median(d):+.2f}   p={p:.2g}")
    return {"media_a": round(statistics.mean(a[t] for t in tas), 4),
            "media_b": round(statistics.mean(b[t] for t in tas), 4),
            "gana_a": gana, "mediana_dif": round(statistics.median(d), 4),
            "p": p}


def main():
    pol = politica_por_instancia()
    gp = gp_por_instancia()
    tas = sorted(set(pol) & set(gp), key=lambda t: int(t[2:]))
    if len(tas) != 70:
        raise SystemExit(f"faltan instancias: {len(tas)}")
    n_pol = {len(v) for v in pol.values()}
    n_gp = {len(v) for v in gp.values()}
    print(f"  70 instancias, {n_pol} semillas de politica, "
          f"{n_gp} evoluciones de GP\n")

    pol_med = {t: statistics.mean(pol[t].values()) for t in tas}
    gp_med = {t: statistics.mean(gp[t].values()) for t in tas}
    camp = {"1": {t: pol[t][5] for t in tas}}
    for etq in ("bo64", "bo1024"):
        v = campeon_por_instancia(etq)
        if len(v) == 70:
            camp[etq] = v

    gp_bon = {}
    for r in csv.DictReader(open("benchmarks/fair_gp_eps.csv",
                                 encoding="utf-8")):
        gp_bon[ta_de(r["instance"])] = {
            "bo64": float(r["best_at_64"]),
            "bo1024": float(r["best_at_1024"])}
    gp_dest = {"1": {t: gp[t][1] for t in tas}}
    for etq in ("bo64", "bo1024"):
        gp_dest[etq] = {t: gp_bon[t][etq] for t in tas}

    res = {}
    print("una pasada:")
    res["1pass_media"] = contrasta("media 30 pol vs media 30 GP",
                                   pol_med, gp_med, tas)
    res["1pass_elegido"] = contrasta("campeon vs regla destacada",
                                     camp["1"], gp_dest["1"], tas)
    for etq, nombre in (("bo64", "64 muestras"), ("bo1024", "1024 muestras")):
        if etq in camp:
            print(f"\n{nombre}:")
            res[f"{etq}_elegido"] = contrasta(
                "campeon vs regla destacada", camp[etq], gp_dest[etq], tas)

    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    json.dump(res, open(SALIDA, "w", encoding="utf-8"), indent=2)
    print(f"\n  escrito {SALIDA}")


if __name__ == "__main__":
    main()
