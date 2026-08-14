# -*- coding: utf-8 -*-
"""Regenera las filas de la tabla por instancia del apendice.

El apendice quedo con el protocolo anterior: la politica como media de
las tres semillas desplegadas y el best-of-1024 repartido entre esos
tres puntos de control. La Tabla 8 reporta ahora el artefacto que cada
estudio selecciona, asi que el apendice debe dar el mismo: la tirada
elegida sobre validacion, a una pasada y a 1024 muestras.

Reescribe SOLO el bloque de filas entre \\midrule y \\bottomrule de
tab:perinstance; el resto del fichero no se toca. Las 350 celdas las
vuelve a comprobar paper/verify_numbers.py despues.

    python scripts/regenera_apendice.py
"""
import csv
import glob
import json
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TEX = "paper/main.tex"
TA_BASE = {"15_15": 0, "20_15": 10, "20_20": 20, "30_15": 30,
           "30_20": 40, "50_15": 50, "50_20": 60}


def ta_de(n):
    m = re.search(r"tai(\d+_\d+)_(\d+)", n.lower())
    return f"TA{TA_BASE[m.group(1)] + int(m.group(2))}"


def main():
    campeon = json.load(open("benchmarks/ext30/campeon.json",
                             encoding="utf-8"))["campeon"]

    lb, gt = {}, {}
    for l in open("benchmarks/constructive_per_instance.csv",
                  encoding="utf-8").read().splitlines()[1:]:
        c = l.split(",")
        lb[c[0]], gt[c[0]] = int(float(c[2])), float(c[5])
    est = {l.split(",")[0]: float(l.split(",")[3]) for l in
           open("benchmarks/est_per_instance.csv",
                encoding="utf-8").read().splitlines()[1:]}
    gp = {}
    for r in csv.DictReader(open("benchmarks/reevo_fixedfit/summary.csv",
                                 encoding="utf-8")):
        if r["method"] == "gp_tuned_seed1":
            gp[ta_de(r["instance"])] = float(r["re"])

    pol = {}
    for r in csv.DictReader(open("benchmarks/eval70_diez_semillas.csv",
                                 encoding="utf-8")):
        if int(r["seed"]) == campeon:
            pol[ta_de(r["instance"])] = float(r["re_greedy"])
    for f in sorted(glob.glob("benchmarks/ext30/eval70_greedy_*.csv")):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            if int(r["seed"]) == campeon:
                pol[ta_de(r["instance"])] = float(r["re_greedy"])

    bo = {}
    for f in sorted(glob.glob("benchmarks/ext30/camp_bo1024_*.csv")):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            bo[ta_de(r["instance"])] = float(r["re_bo"])

    tas = [f"TA{i}" for i in range(1, 71)]
    faltan = [t for t in tas if not all(t in d for d in (lb, est, gt, gp,
                                                         pol, bo))]
    if faltan:
        raise SystemExit(f"faltan datos para {faltan[:5]}")

    filas = []
    for i in range(35):
        izq, der = tas[i], tas[i + 35]
        def celdas(t):
            return (f"{t} & {lb[t]} & {est[t]:.1f} & {gt[t]:.1f} & "
                    f"{gp[t]:.1f} & {pol[t]:.1f} & {bo[t]:.1f}")
        filas.append(f"{celdas(izq)} & {celdas(der)} \\\\")
    bloque = "\n".join(filas)

    txt = open(TEX, encoding="utf-8").read()
    ini = txt.index("\\label{tab:perinstance}")
    a = txt.index("\\midrule", ini) + len("\\midrule")
    b = txt.index("\\bottomrule", a)
    nuevo = txt[:a] + "\n" + bloque + "\n" + txt[b:]
    open(TEX, "w", encoding="utf-8", newline="").write(nuevo)
    print(f"  reescritas 35 lineas (70 instancias) con la tirada "
          f"{campeon}, elegida sobre validacion")
    print(f"  media a una pasada {sum(pol.values())/70:.2f}, "
          f"a 1024 muestras {sum(bo.values())/70:.2f}")


if __name__ == "__main__":
    main()
