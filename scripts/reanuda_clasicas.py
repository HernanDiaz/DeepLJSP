# -*- coding: utf-8 -*-
"""Prepara una reanudacion CORRECTA del bo1024 de las clasicas.

El evaluador salta lo ya hecho leyendo SU PROPIO fichero de salida. Una
reanudacion que escriba en un fichero nuevo empieza con ese registro
vacio y recalcula todo desde el principio, que es lo que ocurrio el
2026-08-14: nueve horas duplicando semillas ya medidas mientras las que
faltaban seguian sin tocarse.

Aqui se fusionan todos los CSV existentes en un maestro deduplicado, se
siembra con el cada carril, y se reparten SOLO las semillas incompletas.
Cada carril arranca sabiendo lo que ya existe y escribe unicamente lo
que falta.

    python scripts/reanuda_clasicas.py
"""
import csv
import glob
import os
import collections
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DIR = "benchmarks/ext30"
CAMPO = ["name", "seed", "lb", "n_samples", "mid", "re", "seconds"]
# carriles: seis de un hilo exprimen mas la maquina que tres, porque el
# coste es Python recorriendo el entorno y no la red
N = int(sys.argv[1]) if len(sys.argv) > 1 else 3


def main():
    filas = {}
    for f in sorted(glob.glob(f"{DIR}/classic12_bo1024_*.csv")):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            filas[(r["name"], int(r["seed"]))] = r
    por_semilla = collections.Counter(s for _, s in filas)
    pendientes = sorted(set(range(2, 32)) - {s for s, n in por_semilla.items()
                                             if n == 12})
    print(f"  {len(filas)} filas unicas; pendientes: {pendientes}")

    maestro = f"{DIR}/classic12_bo1024_maestro.csv"
    with open(maestro, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPO)
        w.writeheader()
        for k in sorted(filas, key=lambda t: (t[1], t[0])):
            w.writerow(filas[k])
    print(f"  maestro deduplicado: {maestro}")

    destino = r"E:\PycharmProjects\DeepLJSP\logs"
    for i in range(N):
        trozo = pendientes[i::N]
        salida = f"{DIR}/classic12_bo1024_f{i+1}.csv"
        # el carril arranca CON todo lo conocido, para que lo salte
        with open(salida, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=CAMPO)
            w.writeheader()
            for k in sorted(filas, key=lambda t: (t[1], t[0])):
                w.writerow(filas[k])
        txt = ("@echo off\r\n"
               f"rem Cierre del bo1024 de las clasicas, carril {i+1}.\r\n"
               "rem El fichero de salida se siembra con lo ya medido, para\r\n"
               "rem que el evaluador lo salte en vez de repetirlo.\r\n"
               "cd /d E:\\PycharmProjects\\DeepLJSP\r\n"
               "set OMP_NUM_THREADS=1\r\n"
               "set MKL_NUM_THREADS=1\r\n"
               "start \"clas\" /low /b /wait venv\\Scripts\\python.exe -X utf8 "
               "scripts\\eval_classic12_treinta.py --n 1024 "
               f"--semillas {','.join(map(str, trozo))} "
               f"--salida {salida.replace('/', chr(92))} "
               f">> logs\\clas30_f{i+1}.log 2>&1\r\n"
               f"echo CLAS30 F{i+1} COMPLETA > logs\\clas30_f{i+1}_done.txt\r\n")
        open(os.path.join(destino, f"lanza_clas30_f{i+1}.bat"), "w",
             encoding="ascii").write(txt)
        print(f"  carril {i+1}: semillas {trozo}")


if __name__ == "__main__":
    main()
