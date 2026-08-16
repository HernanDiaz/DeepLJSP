# -*- coding: utf-8 -*-
"""Prueba de autocontencion del deposito zenodo_drl.

Recorre las rutas de datos que paper/verify_numbers.py consulta
(literales y globs) y comprueba que cada una existe dentro del paquete
bajo su mapeo: benchmarks/ y tuning/ viven en records/, outputs/ en
training_runs/ (con la carpeta de la tirada como primer nivel). Lo que
falte se lista; si todo esta, el deposito puede sostener por si solo
cada numero del paper.

    python scripts/comprueba_zenodo_drl.py
"""
import glob
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PAQUETE = "zenodo_drl"


def destino_de(ruta):
    if ruta.startswith(("benchmarks/", "tuning/")):
        return os.path.join(PAQUETE, "records", ruta)
    if ruta.startswith("outputs/"):
        return os.path.join(PAQUETE, "training_runs",
                            os.path.relpath(ruta, "outputs"))
    return None


def main():
    ver = open("paper/verify_numbers.py", encoding="utf-8").read()
    literales = set(re.findall(
        r'"((?:benchmarks|tuning|outputs)/[^"*]+?\.\w+)"', ver))
    patrones = set(re.findall(
        r'"((?:benchmarks|tuning|outputs)/[^"]*\*[^"]*)"', ver))
    # los globs con f-string (outputs/bench_{tag}...) no se capturan:
    # se cubren con el patron generico de tiradas
    patrones.add("outputs/bench_*/plots/test/*_schedule.json")
    patrones.add("outputs/bench_*/best_model.pt")

    rutas = {r for r in literales if os.path.exists(r)}
    for p in patrones:
        rutas |= set(glob.glob(p))
    # las tiradas en curso (sin best_model.pt) no cuentan: el paquete
    # solo promete tiradas completas
    rutas = {r for r in rutas
             if not (r.replace("\\", "/").startswith("outputs/")
                     and not os.path.exists(os.path.join(
                         "outputs",
                         r.replace("\\", "/").split("/")[1],
                         "best_model.pt")))}

    faltan = []
    for r in sorted(rutas):
        d = destino_de(r.replace("\\", "/"))
        if d and not os.path.exists(d):
            faltan.append(r)
    print(f"{len(rutas)} rutas de datos consultadas por el verificador")
    if faltan:
        print(f"FALTAN {len(faltan)} en el paquete:")
        for r in faltan[:25]:
            print("  ", r)
        sys.exit(1)
    print("autocontenido: el paquete cubre todas las rutas")


if __name__ == "__main__":
    main()
