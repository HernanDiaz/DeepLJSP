# -*- coding: utf-8 -*-
"""Monta la version 2.0 del deposito de Zenodo del paper de GP.

La 1.0 (zenodo_deposit/, publicada el 2026-07-31, DOI de concepto
10.5281/zenodo.21716972) se monto a mano y no se toca. La 2.0 parte de
ella y anade lo que la revision genero:

  - instances/asymmetric_taillard/: el banco asimetrico de E4;
  - rules/training_sets/ (E2, 150) y rules/asymmetric/ (E4, 60);
  - results/: E0, E1, E2, E3, E4, E5, E6 y la tabla de baselines;
  - code/ijsp_gp/: simulador comun, genetico y generador asimetrico,
    y el test de equivalencia ampliado con una comprobacion por
    experimento nuevo.

El paquete sigue siendo autocontenido: no importa nada de jobshop_rl.
El zip no lleva __pycache__ (la 1.0 si los llevo) ni la hoja de
metadatos, que es para rellenar el formulario y no se publica.

    python scripts/prepara_zenodo_gp.py

Salida NUEVA: zenodo_caie/ (carpeta de trabajo, zip y hoja de metadatos)
"""
import csv
import glob
import io
import os
import re
import shutil
import sys
import zipfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

V1 = "zenodo_deposit"
SRC = "scripts/deposito_gp"
DEST = "zenodo_caie"
ZIP = os.path.join(DEST, "ijsp_gp_dataset.zip")
NO_PUBLICAR = {"ZENODO_METADATA.md", "ijsp_gp_dataset.zip"}

# E2: nombre de campana -> carpeta con el conjunto de entrenamiento
CAMPANAS = {"cuatro_b": "TA15-TA18", "cuatro_c": "TA17-TA20",
            "cuatro_d": "TA12-TA14-TA16-TA18", "dos": "TA11-TA12",
            "ocho": "TA11-TA18"}
# E4: rama -> carpeta
RAMAS = {"full": "makespan_full", "nowidth": "makespan_nowidth",
         "rob1": "robust_lambda1_full",
         "rob1_nowidth": "robust_lambda1_nowidth"}


def ignora(_, nombres):
    return [n for n in nombres
            if n == "__pycache__" or n.endswith(".pyc") or n in NO_PUBLICAR]


def copia(origen, destino):
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    shutil.copy2(origen, destino)


def main():
    assert os.path.isdir(V1), f"falta la version 1.0 en {V1}"
    if os.path.isdir(DEST):
        shutil.rmtree(DEST)
    os.makedirs(DEST)

    # --- 1. la base: la version 1.0, sin caches ni metadatos -------------
    for p in ("instances", "rules", "results", "code"):
        shutil.copytree(os.path.join(V1, p), os.path.join(DEST, p),
                        ignore=ignora)
    copia(os.path.join(V1, "LICENSE-DATA"), os.path.join(DEST, "LICENSE-DATA"))

    # --- 2. codigo y README nuevos --------------------------------------
    for f in glob.glob(os.path.join(SRC, "ijsp_gp", "*.py")):
        copia(f, os.path.join(DEST, "code", "ijsp_gp", os.path.basename(f)))
    copia(os.path.join(SRC, "test_equivalence.py"),
          os.path.join(DEST, "code", "test_equivalence.py"))
    copia(os.path.join(SRC, "README.md"), os.path.join(DEST, "README.md"))

    # --- 3. el banco asimetrico, con el escritor del propio paquete ------
    sys.path.insert(0, ".")
    import contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        from jobshop_rl.data import PROBLEM_REGISTRY
    sys.path.insert(0, os.path.join(DEST, "code"))
    from ijsp_gp.asymmetric import write_instance

    salida = os.path.join(DEST, "instances", "asymmetric_taillard")
    os.makedirs(salida)
    clases = {(15, 15), (20, 15), (20, 20), (30, 15), (30, 20),
              (50, 15), (50, 20)}
    n_asim = 0
    for pid in sorted(PROBLEM_REGISTRY):
        m = re.fullmatch(r"int__atai(\d+)_(\d+)_(\d+)", pid)
        if not m or (int(m[1]), int(m[2])) not in clases:
            continue
        datos = PROBLEM_REGISTRY[pid]()
        durs = [[(int(d.lower), int(d.upper)) for d in fila]
                for fila in datos["durations"]]
        write_instance(os.path.join(salida, pid + ".txt"), pid, datos, durs)
        n_asim += 1
    assert n_asim == 70, f"{n_asim} instancias asimetricas"

    # --- 4. reglas nuevas ------------------------------------------------
    n_reglas = 0
    for camp, carpeta in CAMPANAS.items():
        for f in glob.glob(f"benchmarks/e2_entrenamiento/{camp}/seed*.json"):
            copia(f, os.path.join(DEST, "rules", "training_sets", carpeta,
                                  os.path.basename(f)))
            n_reglas += 1
    for rama, carpeta in RAMAS.items():
        for f in glob.glob(f"benchmarks/e4_asimetrico/{rama}/seed*.json"):
            copia(f, os.path.join(DEST, "rules", "asymmetric", carpeta,
                                  os.path.basename(f)))
            n_reglas += 1
    assert n_reglas == 210, f"{n_reglas} reglas nuevas, esperaba 210"

    # --- 5. resultados nuevos --------------------------------------------
    R = os.path.join(DEST, "results")
    copia("benchmarks/reevo_fixedfit/e0_seleccion.json",
          os.path.join(R, "featured_rule_selection.json"))
    for f in glob.glob("benchmarks/e1_robustez/*.csv"):
        copia(f, os.path.join(R, "realization_laws", os.path.basename(f)))
    copia("benchmarks/e1_robustez/resumen.json",
          os.path.join(R, "realization_laws", "summary.json"))
    copia("benchmarks/e2_entrenamiento/resumen.json",
          os.path.join(R, "training_sets", "summary.json"))
    copia("benchmarks/e3_caso/caso.json", os.path.join(R, "worked_example.json"))
    copia("benchmarks/e4_asimetrico/resumen.json",
          os.path.join(R, "asymmetric", "summary.json"))
    copia("benchmarks/e4_asimetrico/resumen_generacion.json",
          os.path.join(R, "asymmetric", "generation.json"))
    copia("benchmarks/e5_decodificador/resumen.json",
          os.path.join(R, "decoder_and_conventions.json"))
    copia("benchmarks/e6_presupuesto/resumen.json",
          os.path.join(R, "budget", "summary.json"))
    copia("benchmarks/e6_presupuesto/calibracion.json",
          os.path.join(R, "budget", "ga_calibration_training.json"))
    copia("benchmarks/e6_presupuesto/calibracion_clasicas.json",
          os.path.join(R, "budget", "ga_calibration_classical.json"))

    # las curvas de los seis carriles, en un solo fichero
    filas, cab = [], None
    for f in sorted(glob.glob("benchmarks/e6_presupuesto/curva_carril*.csv")):
        with open(f, encoding="utf-8") as h:
            lector = csv.reader(h)
            c = next(lector)
            assert cab in (None, c), "cabeceras distintas entre carriles"
            cab = c
            filas.extend(lector)
    filas.sort(key=lambda r: (r[2], r[0], int(r[1]), int(r[3])))
    with open(os.path.join(R, "budget", "curves.csv"), "w", newline="",
              encoding="utf-8") as h:
        w = csv.writer(h)
        w.writerow(cab)
        w.writerows(filas)
    insts = {r[2] for r in filas}
    assert len(insts) == 70, f"curvas de {len(insts)} instancias"

    # la tabla de baselines, sin la fila 'GP (best)', que es de una
    # campana anterior: las filas GP del articulo salen de summary.csv
    with open("benchmarks/all_baselines.csv", encoding="utf-8") as h:
        base = [r for r in csv.reader(h)]
    with open(os.path.join(R, "all_baselines.csv"), "w", newline="",
              encoding="utf-8") as h:
        csv.writer(h).writerows(r for r in base if r[0] != "GP (best)")

    # --- 6. hoja de metadatos, fuera del zip ------------------------------
    copia(os.path.join(SRC, "ZENODO_METADATA.md"),
          os.path.join(DEST, "ZENODO_METADATA.md"))

    # --- 7. el zip ---------------------------------------------------------
    n = 0
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for raiz, dirs, ficheros in os.walk(DEST):
            dirs[:] = sorted(d for d in dirs if d != "__pycache__")
            for f in sorted(ficheros):
                if f in NO_PUBLICAR or f.endswith(".pyc"):
                    continue
                ruta = os.path.join(raiz, f)
                z.write(ruta, os.path.relpath(ruta, DEST).replace(os.sep, "/"))
                n += 1

    # --- 8. comprobaciones de lo que se va a publicar ------------------------
    with zipfile.ZipFile(ZIP) as z:
        nombres = z.namelist()
    assert not any("__pycache__" in x or x.endswith(".pyc") for x in nombres)
    assert not any("METADATA" in x for x in nombres)
    codigo = [x for x in nombres if x.startswith("code/") and x.endswith(".py")]
    with zipfile.ZipFile(ZIP) as z:
        for x in codigo:
            fuente = z.read(x).decode("utf-8")
            assert "jobshop_rl" not in fuente, f"{x} depende del repositorio"
    reglas = [x for x in nombres if x.startswith("rules/") and x.endswith(".json")]
    print(f"{n} ficheros en {ZIP} ({os.path.getsize(ZIP) / 2**20:.1f} MiB)")
    print(f"  reglas: {len(reglas)}")
    print(f"  instancias asimetricas: {n_asim}")
    print(f"  codigo: {len(codigo)} modulos, ninguno depende del repositorio")


if __name__ == "__main__":
    main()
