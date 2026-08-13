# -*- coding: utf-8 -*-
"""Reanalisis de las ablaciones con la instancia como unidad muestral.

El paper contrasta los brazos con un Wilcoxon sobre los pares
(instancia, semilla): 60 pares con diez semillas sobre seis instancias.
Esos 60 no son independientes. Diez politicas entrenadas de forma
independiente y evaluadas sobre las MISMAS seis instancias aportan seis
observaciones independientes, no sesenta; la semilla mide la
estocasticidad del entrenamiento, no amplia la muestra de instancias.
La revision externa r1 lo senalo como un problema bloqueante y tiene
razon.

Este script recomputa cada contraste de las dos formas, agregando por
instancia antes del test, y anade tamano de efecto e intervalo de
confianza. No hay experimentos nuevos: lee los schedules ya guardados,
igual que paper/verify_numbers.py, y con el mismo makespan componente a
componente.

Salida NUEVA: benchmarks/reanalisis/ablaciones_por_instancia.csv

    python scripts/reanalisis_por_instancia.py
"""
import csv
import glob
import json
import math
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from scipy import stats                                        # noqa: E402

TA_BASE = {"15_15": 0, "20_15": 10, "20_20": 20, "30_15": 30,
           "30_20": 40, "50_15": 50, "50_20": 60}
SALIDA = "benchmarks/reanalisis/ablaciones_por_instancia.csv"

BASE_1000 = ("v2-full-1000ep", "v2-full-1000ep-ext-c")
COMPARACIONES = [
    ("atencion, 300 episodios",
     ("v2-full-300ep", "v2-full-300ep-ext"), ("v2-attn-300ep",)),
    ("atencion, 1000 episodios",
     BASE_1000, ("v2-attn-1000ep", "v2-attn-1000ep-ext")),
    ("sin anchuras, 1000 episodios",
     BASE_1000, ("v2-nowidth-1000ep-b", "v2-nowidth-1000ep-ext")),
    ("punto medio, 1000 episodios",
     BASE_1000, ("v2-midpoint-1000ep-b", "v2-midpoint-1000ep-ext")),
    ("robusto lambda=1, RE",
     ("v2-full-1000ep",), ("v2-robust-lam1",)),
]

LB = {}
for _l in open("benchmarks/constructive_per_instance.csv",
               encoding="utf-8").read().splitlines()[1:]:
    _c = _l.split(",")
    LB[_c[0]] = float(_c[2])


def ta_de(nombre):
    m = re.search(r"tai(\d+_\d+)_(\d+)", nombre.lower())
    return f"TA{TA_BASE[m.group(1)] + int(m.group(2))}"


def mid_componentwise(path):
    lo_max = up_max = 0.0
    for t in json.load(open(path)):
        e = t["end"]
        lo, up = (e["lower"], e["upper"]) if isinstance(e, dict) else (e, e)
        lo_max, up_max = max(lo_max, lo), max(up_max, up)
    return (lo_max + up_max) / 2.0


def por_par(tags):
    """{(TA, semilla): RE} de uno o varios tags del mismo brazo."""
    out = {}
    for tag in tags:
        for d in sorted(glob.glob(f"outputs/bench_{tag}__*_seed*")):
            s = d.split("_seed")[-1]
            for p in glob.glob(os.path.join(d, "plots", "test",
                                            "*_schedule.json")):
                ta = ta_de(os.path.basename(p))
                out[(ta, s)] = (mid_componentwise(p) - LB[ta]) / LB[ta] * 100
    return out


def media(v):
    return sum(v) / len(v)


def desv(v):
    if len(v) < 2:
        return float("nan")
    m = media(v)
    return math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))


def analiza(nombre, tags_base, tags_var):
    base, var = por_par(tags_base), por_par(tags_var)
    semillas = sorted({s for _, s in base} & {s for _, s in var}, key=int)
    instancias = sorted({t for t, _ in base} & {t for t, _ in var},
                        key=lambda x: int(x[2:]))
    if not semillas or not instancias:
        print(f"  {nombre}: sin datos emparejables")
        return None

    # --- lectura de hoy: todos los pares (instancia, semilla) juntos ---
    d_par = [var[(t, s)] - base[(t, s)]
             for t in instancias for s in semillas]
    p_par = stats.wilcoxon(d_par).pvalue

    # --- lectura correcta: la instancia es la unidad ------------------
    m_base = {t: media([base[(t, s)] for s in semillas]) for t in instancias}
    m_var = {t: media([var[(t, s)] for s in semillas]) for t in instancias}
    d_ins = [m_var[t] - m_base[t] for t in instancias]
    n = len(d_ins)
    p_ins = stats.wilcoxon(d_ins, method="exact").pvalue
    md, sd = media(d_ins), desv(d_ins)
    t_crit = stats.t.ppf(0.975, n - 1)
    semi = t_crit * sd / math.sqrt(n)
    d_cohen = md / sd if sd else float("nan")

    # --- de donde viene la varianza -----------------------------------
    sd_entre = desv(list(m_base.values()))
    sd_dentro = media([desv([base[(t, s)] for s in semillas])
                       for t in instancias])

    peor = sum(1 for x in d_ins if x > 0)
    print(f"\n  {nombre}")
    print(f"    semillas emparejadas: {len(semillas)}  "
          f"instancias: {n}")
    print(f"    diferencia media (variante - base): {md:+.2f} puntos "
          f"[IC95 {md - semi:+.2f}, {md + semi:+.2f}]")
    print(f"    d de Cohen sobre instancias: {d_cohen:+.2f}   "
          f"peor en {peor}/{n} instancias")
    print(f"    p por pares (lectura de hoy, n={len(d_par)}): "
          f"{p_par:.4f}")
    print(f"    p por instancia (n={n}, exacto):            {p_ins:.4f}"
          f"   {'sigue significativo' if p_ins < 0.05 else 'NO significativo'}")
    print(f"    sd entre instancias {sd_entre:.2f} frente a sd entre "
          f"semillas dentro de instancia {sd_dentro:.2f}")
    return {"comparacion": nombre, "semillas": len(semillas),
            "instancias": n, "dif_media": round(md, 3),
            "ic95_lo": round(md - semi, 3), "ic95_hi": round(md + semi, 3),
            "d_cohen": round(d_cohen, 3), "peor_en": peor,
            "n_pares": len(d_par), "p_pares": round(float(p_par), 5),
            "p_instancia": round(float(p_ins), 5),
            "sd_entre_instancias": round(sd_entre, 3),
            "sd_entre_semillas": round(sd_dentro, 3)}


def extremos(path):
    lo_max = up_max = 0.0
    for t in json.load(open(path)):
        e = t["end"]
        lo, up = (e["lower"], e["upper"]) if isinstance(e, dict) else (e, e)
        lo_max, up_max = max(lo_max, lo), max(up_max, up)
    return lo_max, up_max


def anchura_por_par(tags):
    """{(TA, semilla): ancho relativo %} desde los schedules."""
    out = {}
    for tag in tags:
        for d in sorted(glob.glob(f"outputs/bench_{tag}__*_seed*")):
            s = d.split("_seed")[-1]
            for p in glob.glob(os.path.join(d, "plots", "test",
                                            "*_schedule.json")):
                lo, up = extremos(p)
                mid = (lo + up) / 2
                out[(ta_de(os.path.basename(p)), s)] = (up - lo) / mid * 100
    return out


def analiza_anchura():
    """El brazo robusto lambda=1: la anchura predicha, misma unidad."""
    base = anchura_por_par(("v2-full-1000ep",))
    var = anchura_por_par(("v2-robust-lam1",))
    semillas = sorted({s for _, s in base} & {s for _, s in var}, key=int)
    instancias = sorted({t for t, _ in base} & {t for t, _ in var},
                        key=lambda x: int(x[2:]))
    d_par = [var[(t, s)] - base[(t, s)]
             for t in instancias for s in semillas]
    d_ins = [media([var[(t, s)] for s in semillas])
             - media([base[(t, s)] for s in semillas]) for t in instancias]
    n = len(d_ins)
    p_par = stats.wilcoxon(d_par).pvalue
    p_ins = stats.wilcoxon(d_ins, method="exact").pvalue
    md, sd = media(d_ins), desv(d_ins)
    semi = stats.t.ppf(0.975, n - 1) * sd / math.sqrt(n)
    mejor = sum(1 for x in d_ins if x < 0)
    print("\n  anchura predicha, lambda=1 frente al brazo por defecto")
    print(f"    semillas emparejadas: {len(semillas)}  instancias: {n}")
    print(f"    diferencia media: {md:+.2f} puntos de anchura "
          f"[IC95 {md - semi:+.2f}, {md + semi:+.2f}]")
    print(f"    mas estrecho en {mejor}/{n} instancias")
    print(f"    p por pares (lectura de hoy, n={len(d_par)}): {p_par:.4f}")
    print(f"    p por instancia (n={n}, exacto):            {p_ins:.4f}")
    return {"comparacion": "anchura predicha, lambda=1",
            "semillas": len(semillas), "instancias": n,
            "dif_media": round(md, 3), "ic95_lo": round(md - semi, 3),
            "ic95_hi": round(md + semi, 3),
            "d_cohen": round(md / sd, 3) if sd else "",
            "peor_en": n - mejor, "n_pares": len(d_par),
            "p_pares": round(float(p_par), 5),
            "p_instancia": round(float(p_ins), 5),
            "sd_entre_instancias": "", "sd_entre_semillas": ""}


def main():
    print("== ablaciones: pares (instancia, semilla) frente a instancia ==")
    filas = [f for f in (analiza(*c) for c in COMPARACIONES) if f]
    filas.append(analiza_anchura())
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    with open(SALIDA, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    print(f"\nescrito {SALIDA}")


if __name__ == "__main__":
    main()
