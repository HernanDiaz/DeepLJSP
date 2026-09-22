# -*- coding: utf-8 -*-
"""E2: sensibilidad de la regla al conjunto de entrenamiento.

Los tres revisores del envio a SWEVO piden lo mismo: el articulo evoluciona
sobre cuatro instancias 20x15 y no muestra que el resultado sobreviva a
otra eleccion, ni al tamano del conjunto.

Diseno. La clase 20x15 tiene diez instancias. Cada campana evoluciona
treinta reglas sobre un subconjunto distinto y todas se juzgan sobre las
SESENTA instancias de las otras clases, que ningun subconjunto toca: esa
es la superficie de comparacion limpia, y evita el problema de que
cualquier cuadrupla alternativa solape con el conjunto de desarrollo.

Dos ejes:
  - que cuatro: tres cuadruplas distintas de la original;
  - cuantas: dos y ocho instancias.

Reanudable por (campana, semilla): relanzar continua donde iba.

    python scripts/e2_sensibilidad_entrenamiento.py --carril 0 --de 6

Salida NUEVA: benchmarks/e2_entrenamiento/<campana>/seed<N>.json
"""
import argparse
import os
import subprocess
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PY = os.path.join("venv", "Scripts", "python.exe")
DIR = "benchmarks/e2_entrenamiento"
SEMILLAS = list(range(1, 31))
# la configuracion de irace del articulo, identica en todas las campanas:
# lo que varia es el conjunto de entrenamiento y nada mas
TUNED = ["--tournament", "7", "--crossover", "0.7695",
         "--maxtree", "30", "--elitism", "2"]


def ids(*n):
    return ",".join(f"int__tai20_15_{k:02d}" for k in n)


CAMPANAS = {
    # tres cuadruplas alternativas a la original (01-04)
    "cuatro_b": ids(5, 6, 7, 8),
    "cuatro_c": ids(7, 8, 9, 10),
    "cuatro_d": ids(2, 4, 6, 8),
    # y el tamano del conjunto
    "dos": ids(1, 2),
    "ocho": ids(1, 2, 3, 4, 5, 6, 7, 8),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--carril", type=int, required=True)
    ap.add_argument("--de", type=int, default=6)
    args = ap.parse_args()

    tareas = [(c, s) for c in CAMPANAS for s in SEMILLAS]
    mias = [t for k, t in enumerate(tareas) if k % args.de == args.carril]
    print(f"carril {args.carril}: {len(mias)} evoluciones", flush=True)

    t0, hechas = time.time(), 0
    for campana, semilla in mias:
        out = os.path.join(DIR, campana, f"seed{semilla}.json")
        if os.path.exists(out):
            continue
        os.makedirs(os.path.dirname(out), exist_ok=True)
        cmd = [PY, "-X", "utf8", "scripts/evolve_gp_rule.py",
               "--out", out, "--seed", str(semilla),
               "--train-ids", CAMPANAS[campana]] + TUNED
        t1 = time.time()
        log = os.path.join("logs", f"e2_{campana}_s{semilla}.log")
        os.makedirs("logs", exist_ok=True)
        with open(log, "w", encoding="utf-8") as f:
            subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
        hechas += 1
        estado = "OK" if os.path.exists(out) else "FALLO"
        print(f"  {campana} seed{semilla}: {estado} en "
              f"{time.time() - t1:.0f}s  [{hechas}/{len(mias)}, "
              f"{(time.time() - t0) / 60:.0f} min]", flush=True)
    print("carril hecho", flush=True)


if __name__ == "__main__":
    main()
