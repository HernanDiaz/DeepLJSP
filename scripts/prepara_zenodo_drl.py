# -*- coding: utf-8 -*-
"""Esqueleto del deposito Zenodo del paper DRL.

Copia (nunca mueve) en zenodo_drl/ lo que la declaracion de
disponibilidad promete: codigo, registros de experimento aceptados y
rechazados, checkpoints finales y scripts de figuras. El criterio de
inclusion de registros es el propio verificador: todo fichero de datos
que paper/verify_numbers.py lee debe estar en el paquete, y con el se
copia su campana entera (la carpeta), incluidas las cuarentenas.

De outputs/ (2.5 GB) se extrae por tirada solo lo que el paper usa:
el checkpoint final, los logs de entrenamiento y los schedules JSON de
la evaluacion embebida (los PNG se regeneran y no viajan).

Idempotente: lo ya copiado con el mismo tamano se salta.

    python scripts/prepara_zenodo_drl.py
"""
import glob
import os
import re
import shutil
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DESTINO = "zenodo_drl"
# campanas del paper de GP que viven en este repo y NO van en este
# deposito (ya estan publicadas en el suyo). OJO: classic12_arm_bon NO
# se excluye, porque esas evaluaciones de las 30 reglas a tres
# presupuestos son de ESTE paper (tab:classics), no del suyo
EXCLUIR_BENCH = ("reevo_fixedfit", "pilot_robust", "lambda_sweep",
                 "clon_v2")
EXCLUIR_SCRIPTS_PREFIJO = ("clon_",)


def copia(origen, destino):
    if os.path.isfile(destino) and \
            os.path.getsize(destino) == os.path.getsize(origen):
        return 0
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    shutil.copy2(origen, destino)
    return 1


def main():
    os.makedirs(DESTINO, exist_ok=True)
    copiados, saltados = 0, 0

    # --- registros: las carpetas de benchmarks/ que el verificador lee ---
    ver = open("paper/verify_numbers.py", encoding="utf-8").read()
    rutas = set(re.findall(r'"(benchmarks/[^"*]+?\.\w+)"', ver))
    rutas |= set(re.findall(r'"(tuning/[^"*]+?\.\w+)"', ver))
    # y las lecturas por glob (classic12_arm_bon entre ellas)
    for patron in re.findall(r'"((?:benchmarks|tuning)/[^"]*\*[^"]*)"', ver):
        rutas |= set(glob.glob(patron))
    carpetas = set()
    for r in sorted(rutas):
        if not os.path.exists(r):
            continue
        d = os.path.dirname(r)
        carpetas.add(d if d not in ("benchmarks", "tuning") else None)
        n = copia(r, os.path.join(DESTINO, "records", r))
        copiados += n
        saltados += 1 - n
    # la campana entera de cada fichero citado, cuarentenas incluidas
    for c in sorted(x for x in carpetas if x):
        if any(e in c for e in EXCLUIR_BENCH):
            continue
        for f in glob.glob(os.path.join(c, "*")):
            if os.path.isfile(f):
                n = copia(f, os.path.join(DESTINO, "records", f))
                copiados += n
                saltados += 1 - n
    print(f"registros: {copiados} copiados, {saltados} ya estaban")

    # --- extractos de las tiradas de entrenamiento ---
    # solo tiradas COMPLETAS: una en curso no tiene best_model.pt y no
    # debe viajar a medias
    c2, s2 = 0, 0
    for d in sorted(glob.glob("outputs/bench_*")):
        if not os.path.exists(os.path.join(d, "best_model.pt")):
            continue
        nombre = os.path.basename(d)
        for patron in ("best_model.pt", "global_training_log.csv",
                       "training_summary.csv", "training_stats.txt",
                       "*_training_log.csv", "test_results.csv",
                       "plots/test/*_schedule.json"):
            for f in glob.glob(os.path.join(d, patron)):
                rel = os.path.relpath(f, d)
                n = copia(f, os.path.join(DESTINO, "training_runs",
                                          nombre, rel))
                c2 += n
                s2 += 1 - n
    print(f"tiradas: {c2} ficheros copiados, {s2} ya estaban")

    # --- codigo ---
    c3 = 0
    for f in glob.glob("jobshop_rl/**/*.py", recursive=True):
        if "__pycache__" in f:
            continue
        c3 += copia(f, os.path.join(DESTINO, "code", f))
    for f in glob.glob("scripts/*.py"):
        base = os.path.basename(f)
        if any(base.startswith(p) for p in EXCLUIR_SCRIPTS_PREFIJO):
            continue
        c3 += copia(f, os.path.join(DESTINO, "code", f))
    for f in ("paper/make_figures.py", "paper/verify_numbers.py"):
        c3 += copia(f, os.path.join(DESTINO, "code", f))
    print(f"codigo: {c3} ficheros")

    # --- las instancias del benchmark ---
    # el deposito es autocontenido desde 2026-08-18: la declaracion de
    # datos del paper promete instancias Y codigo aqui, sin remitir al
    # deposito del estudio GP
    c_inst = 0
    for f in glob.glob("zenodo_deposit/instances/**/*.txt", recursive=True):
        rel = os.path.relpath(f, "zenodo_deposit")
        c_inst += copia(f, os.path.join(DESTINO, rel))
    print(f"instancias: {c_inst} copiadas")

    # --- lo que la revision de 2026-08-25 echo en falta ---
    # los checkpoints exportados que referencian scripts y tests
    c_m = 0
    for f in glob.glob("models/*.pt"):
        c_m += copia(f, os.path.join(DESTINO, "code", f))
    # los target-runner de irace que tuning/scenario*.txt referencia;
    # solo esos: los lanzadores run_*.bat son utileria local
    for f in glob.glob("tuning/target_runner*.bat") + \
            glob.glob("tuning/*.txt"):
        c_m += copia(f, os.path.join(DESTINO, "records", f))
    # las 30 reglas GP del brazo principal: sin ellas la evaluacion
    # compartida no es reejecutable (siguen publicadas en su deposito;
    # aqui viajan como conveniencia CC-BY del mismo autor)
    for f in glob.glob("zenodo_deposit/rules/main_arm/*.json"):
        c_m += copia(f, os.path.join(DESTINO, "rules", "gp_main_arm",
                                     os.path.basename(f)))
    print(f"revision M7: {c_m} ficheros (modelos, irace, reglas GP)")

    # --- el material suplementario del articulo, en PDF ---
    try:
        import shutil as _sh
        destino_pdf = os.path.join(DESTINO, "supplementary_material.pdf")
        _sh.copy2("paper/supplementary.pdf", destino_pdf)
    except PermissionError:
        with open("paper/supplementary.pdf", "rb") as a, \
                open(destino_pdf, "wb") as b:
            b.write(a.read())
    print("suplementario: copiado")

    # --- requisitos, con las versiones de la tabla de entorno ---
    req = os.path.join(DESTINO, "code", "requirements.txt")
    if not os.path.exists(req):
        with open(req, "w", encoding="utf-8") as f:
            f.write("torch==2.9.1\nnumpy==2.3.5\nscipy==1.17.0\n"
                    "matplotlib==3.10.8\n")
    print("hecho: revisar README.md y completar tras el barrido")


if __name__ == "__main__":
    main()
