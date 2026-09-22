# -*- coding: utf-8 -*-
"""E4: evoluciona sobre las asimetricas, con y sin terminales de anchura.

La revision r3.4 pregunta si el valor de los terminales de anchura
depende del esquema simetrico de generacion. La respuesta necesita las
dos ramas sobre el banco asimetrico de e4_genera_asimetricas.py: la
completa y la ablacion --no-width, treinta semillas cada una, con la
configuracion de irace del articulo y sin tocar nada mas.

El entrenamiento son las cuatro 20x15 asimetricas que corresponden a
TA11--TA14, de modo que el protocolo es el mismo que el del articulo
trasladado al banco nuevo.

Reanudable por (rama, semilla): relanzar continua donde iba.

    python scripts/e4_campana.py --carril 0 --de 6

Salida NUEVA: benchmarks/e4_asimetrico/<rama>/seed<N>.json
"""
import argparse
import os
import subprocess
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PY = os.path.join("venv", "Scripts", "python.exe")
DIR = "benchmarks/e4_asimetrico"
SEMILLAS = list(range(1, 31))
TRAIN = ",".join(f"int__atai20_15_{k:02d}" for k in (1, 2, 3, 4))
TUNED = ["--tournament", "7", "--crossover", "0.7695",
         "--maxtree", "30", "--elitism", "2"]
RAMAS = {"full": [], "nowidth": ["--no-width"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--carril", type=int, required=True)
    ap.add_argument("--de", type=int, default=6)
    args = ap.parse_args()

    tareas = [(r, s) for r in RAMAS for s in SEMILLAS]
    mias = [t for k, t in enumerate(tareas) if k % args.de == args.carril]
    print(f"carril {args.carril}: {len(mias)} evoluciones", flush=True)

    t0, hechas = time.time(), 0
    for rama, semilla in mias:
        out = os.path.join(DIR, rama, f"seed{semilla}.json")
        if os.path.exists(out):
            continue
        os.makedirs(os.path.dirname(out), exist_ok=True)
        cmd = ([PY, "-X", "utf8", "scripts/evolve_gp_rule.py",
                "--out", out, "--seed", str(semilla),
                "--train-ids", TRAIN] + TUNED + RAMAS[rama])
        t1 = time.time()
        os.makedirs("logs", exist_ok=True)
        log = os.path.join("logs", f"e4_{rama}_s{semilla}.log")
        with open(log, "w", encoding="utf-8") as f:
            subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
        hechas += 1
        estado = "OK" if os.path.exists(out) else "FALLO"
        print(f"  {rama} seed{semilla}: {estado} en "
              f"{time.time() - t1:.0f}s  [{hechas}/{len(mias)}, "
              f"{(time.time() - t0) / 60:.0f} min]", flush=True)
    print("carril hecho", flush=True)


if __name__ == "__main__":
    main()
