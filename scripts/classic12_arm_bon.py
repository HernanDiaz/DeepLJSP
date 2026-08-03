# -*- coding: utf-8 -*-
"""Las 30 reglas del brazo GP a los TRES presupuestos sobre las 12 clasicas.

classic12_arm.py corrio las 30 reglas a una pasada, y eval_classic12.py
corrio la destacada a una pasada, 64 y 1024. Falta el producto: las 30
a los tres presupuestos, que es lo que hace falta para que la columna
GP de tab:classics pueda dar media [mejor] igual que la de la politica,
en vez de una sola regla.

No se reimplementa nada: se invoca eval_classic12.py una vez por regla
con su propio --out, de modo que el calculo es literalmente el mismo que
produjo las cifras publicadas y ningun CSV anterior se toca.

    python scripts/classic12_arm_bon.py

Deja benchmarks/classic12_arm_bon/<regla>.csv y, al final, agrega.
"""
import glob
import os
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REGLAS = "benchmarks/reevo_fixedfit/gp_tuned_seed*.json"
DESTINO = "benchmarks/classic12_arm_bon"


def main():
    os.makedirs(DESTINO, exist_ok=True)
    reglas = sorted(glob.glob(REGLAS),
                    key=lambda p: int(''.join(c for c in os.path.basename(p)
                                              if c.isdigit())))
    print(f"{len(reglas)} reglas")
    for i, r in enumerate(reglas, 1):
        nombre = os.path.splitext(os.path.basename(r))[0]
        salida = os.path.join(DESTINO, f"{nombre}.csv")
        if os.path.exists(salida) and os.path.getsize(salida) > 0:
            continue
        t0 = time.time()
        p = subprocess.run(
            [sys.executable, "-X", "utf8", "scripts/eval_classic12.py",
             "--rule", r, "--out", salida],
            capture_output=True, text=True, encoding="utf-8",
            errors="replace")
        if p.returncode != 0:
            print(f"  FALLO {nombre}:\n{p.stdout[-500:]}\n{p.stderr[-500:]}")
            continue
        print(f"  [{i}/{len(reglas)}] {nombre} en {time.time()-t0:.0f}s",
              flush=True)
    print("hecho")


if __name__ == "__main__":
    main()
