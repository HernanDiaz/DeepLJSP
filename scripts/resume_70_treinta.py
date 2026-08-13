# -*- coding: utf-8 -*-
"""Resume las 30 semillas sobre las 70 instancias a una pasada.

Fusiona las tres procedencias del greedy, que son comparables entre si
porque el greedy es determinista (argmax en cada decision, sin
muestreo): las semillas 2-4 de benchmarks/fair_v2_greedy.csv, las 5-11
de benchmarks/eval70_diez_semillas.csv y las 12-31 de los tres CSV de
benchmarks/ext30/. Devuelve las dos lecturas simetricas frente al
estudio del GP: la media de las 30 tiradas y el campeon, este ultimo
elegido sobre validacion y no sobre estas 70.

Salida NUEVA: benchmarks/ext30/resumen70_una_pasada.json

    python scripts/resume_70_treinta.py
"""
import csv
import glob
import json
import os
import statistics
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SALIDA = "benchmarks/ext30/resumen70_una_pasada.json"
# lo publicado por el estudio del GP sobre estas mismas 70
GP_MEDIA_30 = 18.99      # media de las 30 evoluciones, una pasada
GP_DESTACADA = 17.71     # la regla destacada, mejor de 30 sobre TEST


def lee(ruta, col_semilla, col_re, col_inst):
    out = {}
    if not os.path.exists(ruta):
        return out
    for r in csv.DictReader(open(ruta, encoding="utf-8")):
        out.setdefault(int(r[col_semilla]), {})[r[col_inst]] = float(r[col_re])
    return out


def main():
    por_semilla = {}

    # semillas 2-4: deposito de julio, con la semilla en el checkpoint
    # (v2_final_deepsets_1000ep_seedN.pt) y el RE en re_mid
    for r in csv.DictReader(open("benchmarks/fair_v2_greedy.csv",
                                 encoding="utf-8")):
        s = int(r["checkpoint"].split("seed")[1].split(".")[0])
        por_semilla.setdefault(s, {})[r["instance"]] = float(r["re_mid"])
    # semillas 5-11
    for s, v in lee("benchmarks/eval70_diez_semillas.csv",
                    "seed", "re_greedy", "instance").items():
        por_semilla.setdefault(s, {}).update(v)
    # semillas 12-31
    for ruta in sorted(glob.glob("benchmarks/ext30/eval70_greedy_*.csv")):
        for s, v in lee(ruta, "seed", "re_greedy", "instance").items():
            por_semilla.setdefault(s, {}).update(v)

    completas = {s: v for s, v in por_semilla.items() if len(v) == 70}
    faltan = {s: len(v) for s, v in por_semilla.items() if len(v) != 70}
    if faltan:
        print(f"AVISO: semillas incompletas {faltan}")

    medias = {s: statistics.mean(v.values()) for s, v in completas.items()}
    campeon = json.load(open("benchmarks/ext30/campeon.json",
                             encoding="utf-8"))["campeon"]

    vals = sorted(medias.values())
    print(f"\n  {len(medias)} semillas completas sobre las 70")
    print(f"  media de las {len(medias)}: {statistics.mean(vals):.2f}"
          f"   sd {statistics.stdev(vals):.2f}")
    print(f"  mejor sobre TEST {min(vals):.2f}, peor {max(vals):.2f}")
    print(f"  campeon (semilla {campeon}, elegido en validacion): "
          f"{medias[campeon]:.2f}")
    orden = sorted(medias, key=lambda s: medias[s])
    print(f"  el campeon ocupa el puesto {orden.index(campeon) + 1} "
          f"de {len(orden)} sobre test")

    print("\n  frente al estudio del GP, a una pasada:")
    print(f"    media 30 evoluciones {GP_MEDIA_30:.2f}  contra  "
          f"media 30 semillas {statistics.mean(vals):.2f}   "
          f"(diferencia {statistics.mean(vals) - GP_MEDIA_30:+.2f})")
    print(f"    regla destacada      {GP_DESTACADA:.2f}  contra  "
          f"campeon {medias[campeon]:.2f}   "
          f"(diferencia {medias[campeon] - GP_DESTACADA:+.2f})")

    # desglose por clase, para la fila de la tabla por tamanos
    clases = ["tai15_15", "tai20_15", "tai20_20", "tai30_15", "tai30_20",
              "tai50_15", "tai50_20"]
    por_clase_media, por_clase_camp = {}, {}
    for c in clases:
        pids = [f"int__{c}_{k:02d}" for k in range(1, 11)]
        por_clase_media[c] = statistics.mean(
            statistics.mean(completas[s][p] for p in pids)
            for s in completas)
        por_clase_camp[c] = statistics.mean(completas[campeon][p]
                                            for p in pids)
    print("\n  por clase (media de las 30 / campeon):")
    for c in clases:
        print(f"    {c:<10} {por_clase_media[c]:5.1f} / "
              f"{por_clase_camp[c]:5.1f}")

    # el campeon a los presupuestos muestreados, si sus carriles ya han
    # escrito: 70 instancias repartidas en seis CSV por coste
    camp_bo = {}
    for etq, bo in (("bo64", 64), ("bo1024", 1024)):
        v = {}
        for ruta in sorted(glob.glob(f"benchmarks/ext30/camp_{etq}_*.csv")):
            for r in csv.DictReader(open(ruta, encoding="utf-8")):
                v[r["instance"]] = float(r["re_bo"])
        if len(v) == 70:
            camp_bo[etq] = {
                "global": round(statistics.mean(v.values()), 4),
                "por_clase": {c: round(statistics.mean(
                    v[f"int__{c}_{k:02d}"] for k in range(1, 11)), 4)
                    for c in clases}}
            print(f"\n  campeon a {bo} muestras sobre las 70: "
                  f"{camp_bo[etq]['global']:.2f}")
        elif v:
            print(f"\n  campeon a {bo} muestras: {len(v)}/70 instancias, "
                  f"aun en curso")

    json.dump({"campeon_muestreado": camp_bo,
               "por_clase_media_30": {c: round(v, 4)
                                      for c, v in por_clase_media.items()},
               "por_clase_campeon": {c: round(v, 4)
                                     for c, v in por_clase_camp.items()},
               "n": len(medias), "campeon": campeon,
               "media_30": round(statistics.mean(vals), 4),
               "sd_30": round(statistics.stdev(vals), 4),
               "mejor_en_test": round(min(vals), 4),
               "peor_en_test": round(max(vals), 4),
               "campeon_re": round(medias[campeon], 4),
               "puesto_campeon_en_test": orden.index(campeon) + 1,
               "gp_media_30": GP_MEDIA_30, "gp_destacada": GP_DESTACADA,
               "por_semilla": {str(s): round(m, 4)
                               for s, m in sorted(medias.items())}},
              open(SALIDA, "w", encoding="utf-8"), indent=2)
    print(f"\n  escrito {SALIDA}")


if __name__ == "__main__":
    main()
