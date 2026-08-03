# -*- coding: utf-8 -*-
"""El resumen del brazo robusto, separando entrenamiento de seleccion.

El brazo lambda=1 se puede leer de dos maneras y dan respuestas
distintas, asi que conviene tener las dos en la misma tabla:

  (a) Como PAQUETE desplegado. Es como lo evalua la propia tirada:
      _episode_makespan respeta lambda, de modo que el best-of-64 del
      brazo lambda elige por up + (up-lo) mientras el brazo base elige
      por up. Entrenamiento y seleccion cambian a la vez.

  (b) Con la SELECCION FIJADA. Del deposito de rollouts se reconstruye
      el mejor-de-64 de ambos brazos bajo el mismo criterio, de modo
      que lo unico que difiere son los pesos.

La diferencia entre (a) y (b) es lo que responde a la pregunta: si el
estrechamiento sobrevive a (b), lo produjo el entrenamiento; si no, lo
produjo el criterio con que se elige la muestra.

    python scripts/resumen_lambda.py   -> benchmarks/robust_lambda/resumen.csv
"""
import csv
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SALIDA = "benchmarks/robust_lambda/resumen.csv"


def main():
    print("== (a) paquete desplegado: protocolo del paper ==")
    a = subprocess.run([sys.executable, "-X", "utf8",
                        "scripts/analiza_lam1_protocolo_paper.py"],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    print("\n".join(l for l in a.stdout.splitlines()
                    if "INFO" not in l and "Total de problemas" not in l))

    print("\n== (b) seleccion fijada: mismo deposito de rollouts ==")
    b = subprocess.run([sys.executable, "-X", "utf8",
                        "scripts/analiza_robust_lambda.py"],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    print(b.stdout)

    with open(SALIDA, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["fuente", "linea"])
        for etiqueta, r in (("paquete", a), ("seleccion_fijada", b)):
            for linea in r.stdout.splitlines():
                if linea.strip() and "INFO" not in linea:
                    w.writerow([etiqueta, linea.rstrip()])
    print(f"\nescrito {SALIDA}")


if __name__ == "__main__":
    main()
