# -*- coding: utf-8 -*-
"""Las 12 clasicas: 30 semillas contra 30 evoluciones, a tres presupuestos.

A diferencia de las Taillard, el estudio del GP publica aqui sus treinta
reglas a los tres presupuestos (benchmarks/classic12_arm_bon/, columnas
gp, gp64 y gp1024), asi que la simetria admite las dos lecturas en las
tres columnas: media de treinta contra media de treinta, y artefacto
seleccionado contra artefacto seleccionado.

El campeon es el mismo que en las Taillard, la semilla elegida sobre
las seis instancias de validacion; la regla destacada es la mejor de
las treinta sobre estas doce, que es como su estudio la selecciona.

Salida NUEVA: benchmarks/ext30/resumen_clasicas30.json

    python scripts/resume_clasicas_treinta.py
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

SALIDA = "benchmarks/ext30/resumen_clasicas30.json"
INST = ["FT10", "FT20", "La21", "La24", "La25", "La27", "La29", "La38",
        "La40", "ABZ7", "ABZ8", "ABZ9"]


def politica():
    """{presupuesto: {instancia: {semilla: RE}}}."""
    out = collections.defaultdict(lambda: collections.defaultdict(dict))
    for f in sorted(glob.glob("benchmarks/ext30/classic12_bo*_*.csv")):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            out[int(r["n_samples"])][r["name"]][int(r["seed"])] = float(
                r["re"])
    return out


def gp():
    """{presupuesto: {instancia: {regla: RE}}}, deposito publicado."""
    col = {1: "gp", 64: "gp64", 1024: "gp1024"}
    out = collections.defaultdict(lambda: collections.defaultdict(dict))
    for f in sorted(glob.glob("benchmarks/classic12_arm_bon/*.csv")):
        regla = os.path.splitext(os.path.basename(f))[0]
        for r in csv.DictReader(open(f, encoding="utf-8")):
            for n, c in col.items():
                out[n][r["inst"]][regla] = float(r[c])
    return out


def resumen(datos, n, campeon=None):
    """Las tres lecturas de la tabla, por instancia y en global.

    media   promedio sobre los artefactos de la familia
    mejor   minimo POR INSTANCIA sobre esos artefactos, que es lo que
            la tabla imprime entre corchetes; no lo alcanza ninguna
            tirada individual, es un mejor virtual, y solo es
            comparable si ambos lados se seleccionan sobre el mismo
            numero de tiradas
    sel     un artefacto real: el campeon en la politica, elegido sobre
            validacion, y la mejor regla sobre estas doce en el GP,
            que es como su estudio la selecciona
    """
    d = datos[n]
    completas = [i for i in INST if i in d]
    if len(completas) < 12:
        return None
    n_art = {len(d[i]) for i in completas}
    if len(n_art) != 1:
        return None
    media = {i: statistics.mean(d[i].values()) for i in completas}
    mejor = {i: min(d[i].values()) for i in completas}
    if campeon is not None:
        sel = {i: d[i][campeon] for i in completas}
        etq = f"campeon (semilla {campeon}, elegido en validacion)"
    else:
        art = list(next(iter(d.values())))
        _m = min(art, key=lambda a: statistics.mean(d[i][a]
                                                    for i in completas))
        sel = {i: d[i][_m] for i in completas}
        etq = f"mejor de {len(art)} sobre estas 12 ({_m})"
    # dispersion ENTRE artefactos: cada uno da su media sobre las 12 y
    # se mide como se separan. 6.3 explicaba el corchete del GP por su
    # mayor dispersion, asi que la afirmacion hay que recomprobarla
    art = list(next(iter(d.values())))
    por_art = [statistics.mean(d[i][a] for i in completas) for a in art]
    return {"n_artefactos": n_art.pop(), "etiqueta_sel": etq,
            "sd_entre_artefactos": round(statistics.stdev(por_art), 4),
            "media_global": round(statistics.mean(media.values()), 4),
            "mejor_global": round(statistics.mean(mejor.values()), 4),
            "sel_global": round(statistics.mean(sel.values()), 4),
            "media": {i: round(media[i], 4) for i in completas},
            "mejor": {i: round(mejor[i], 4) for i in completas},
            "sel": {i: round(sel[i], 4) for i in completas}}


def main():
    pol, g = politica(), gp()
    campeon = json.load(open("benchmarks/ext30/campeon.json",
                             encoding="utf-8"))["campeon"]
    out = {"campeon": campeon, "presupuestos": {}}
    print(f"  campeon: semilla {campeon}\n")
    print(f"  {'presup.':<9} {'GP med':>7} {'POL med':>8} | "
          f"{'GP mej':>7} {'POL mej':>8} | {'GP sel':>7} {'POL camp':>9}")
    for n in (1, 64, 1024):
        rp, rg = resumen(pol, n, campeon), resumen(g, n)
        if rp is None:
            print(f"  {n:<9} politica incompleta, aun en curso")
            continue
        out["presupuestos"][str(n)] = {"politica": rp, "gp": rg}
        print(f"  {n:<9} {rg['media_global']:7.2f} {rp['media_global']:8.2f}"
              f" | {rg['mejor_global']:7.2f} {rp['mejor_global']:8.2f}"
              f" | {rg['sel_global']:7.2f} {rp['sel_global']:9.2f}"
              f" | sd {rg['sd_entre_artefactos']:.2f} vs "
              f"{rp['sd_entre_artefactos']:.2f}")
    print(f"\n  semillas de politica: "
          f"{ {k: v['politica']['n_artefactos'] for k, v in out['presupuestos'].items()} }")
    print(f"  reglas de GP: "
          f"{ {k: v['gp']['n_artefactos'] for k, v in out['presupuestos'].items()} }")
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    json.dump(out, open(SALIDA, "w", encoding="utf-8"), indent=2)
    print(f"\n  escrito {SALIDA}")


if __name__ == "__main__":
    main()
