"""Control del punto medio: evolucionar sobre las instancias CRISP y
desplegar sobre las intervalares.

El experimento que decide si la aritmetica de intervalos en el fitness aporta
algo. La instancia crisp es exactamente el escenario del punto medio de su
version intervalar (seccion 5.1 del paper), asi que evolucionar sobre ella es
evolucionar 'sin intervalos' manteniendo todo lo demas.

Diseno, y por que asi:

  * Terminales SIN anchura (--no-width). Sobre una instancia crisp los
    terminales de anchura valen 0 identicamente: dejarlos seria meter
    constantes degeneradas en el entrenamiento que al desplegar sobre
    intervalos despiertan con valores nunca vistos, un confundido que un
    revisor senalaria. Con --no-width el brazo de comparacion es el brazo
    ablacionado entrenado sobre intervalos (18.66 +- 1.08 de RE), y lo UNICO
    que difiere entre ambos es la aritmetica del fitness: escalar sobre el
    punto medio aqui, intervalar alli.

  * No es redundante con ese brazo ablacionado, porque los dos objetivos son
    genuinamente distintos: el brazo intervalar optimiza el punto medio del
    intervalo de makespan, (max_j c_lo_j + max_j c_up_j)/2, dos maximos que
    pueden alcanzarse en trabajos DISTINTOS; este control optimiza el makespan
    del escenario del punto medio, max_j (c_lo_j + c_up_j)/2, un solo maximo.
    max no conmuta con tomar puntos medios.

  * Mismas semillas 1-30 y misma configuracion de irace que todos los brazos
    (torneo 7, cruce 0.7695, cap 30, elitismo 2, pop 100, 50 generaciones).

  * Despliegue: las reglas resultantes se evaluan con ablation_per_rule.py o
    equivalente sobre las 70 intervalares, con el MISMO decodificador; la
    regla es un arbol sobre terminales sin anchura, asi que se aplica a
    intervalos sin cambio alguno.

Salida: benchmarks/midpoint_control/mid_seed<N>.json (no sobreescribe nada).
Reanudable: los seeds ya presentes se saltan.

Uso: python scripts/midpoint_control.py [--seeds 1-30] [--dry]
"""

import argparse
import os
import subprocess
import sys
import time

PY = sys.executable
OUTDIR = "benchmarks/midpoint_control"
LOGDIR = "logs/midpoint_control"
TRAIN = "tai20_15_01,tai20_15_02,tai20_15_03,tai20_15_04"
TUNED = ["--tournament", "7", "--crossover", "0.7695",
         "--maxtree", "30", "--elitism", "2"]

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="1-30")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    lo, hi = (int(x) for x in a.seeds.split("-"))
    os.makedirs(OUTDIR, exist_ok=True)
    os.makedirs(LOGDIR, exist_ok=True)

    pendientes = [s for s in range(lo, hi + 1)
                  if not os.path.exists(f"{OUTDIR}/mid_seed{s}.json")]
    print(f"{len(pendientes)} evoluciones pendientes de {hi - lo + 1}",
          flush=True)
    for s in pendientes:
        out = f"{OUTDIR}/mid_seed{s}.json"
        cmd = [PY, "scripts/evolve_gp_rule.py", "--out", out,
               "--seed", str(s), "--no-width", "--fitness", "midpoint",
               "--train-ids", TRAIN] + TUNED
        if a.dry:
            print(" ".join(cmd))
            continue
        t0 = time.time()
        with open(f"{LOGDIR}/mid_seed{s}.log", "w", encoding="utf-8") as f:
            subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
        ok = os.path.exists(out)
        print(f"  seed {s}: {'OK' if ok else 'FALLO'} "
              f"({(time.time() - t0) / 60:.1f} min)", flush=True)
    print("control del punto medio: completo", flush=True)


if __name__ == "__main__":
    main()
