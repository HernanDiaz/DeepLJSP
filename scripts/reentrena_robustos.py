# -*- coding: utf-8 -*-
"""Reentrena los brazos lambda>0 con la clave de bloque corregida.

La revision del 2026-08-28 (R5-1) objeta que las tiradas robustas
depositadas eligieron que bloque cedia sus pesos al siguiente con una
clave que agregaba el makespan lexicograficamente en vez de componente
a componente. La recompensa SI era correcta, pero la conclusion de 7.3
trata sobre los pesos, asi que conviene rehacerlas sin el defecto.

Etiquetas NUEVAS (sufijo -fix): no se sobrescribe ninguna tirada
depositada. Cada (brazo, semilla) es una unidad independiente y
completa; una tirada solo cuenta como hecha si dejo su best_model.pt.

PARADA Y REANUDACION
- Reanudable: relanzar salta las tiradas ya completas.
- Parada limpia: crear logs/PARAR_ROBFIX.txt y el carril termina la
  tirada en curso y sale sin empezar otra.
- Parada dura: matar el proceso. Se pierde solo la tirada en curso.
- Prioridad: la fija el lanzador (logs/lanza_robfix_<c>.bat), que
  acepta 'low' o 'normal' como argumento.

    python scripts/reentrena_robustos.py --carril 0 --de 6
"""
import argparse
import glob
import os
import subprocess
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BRAZOS = [("0.5", "v2-robust-lam0p5-fix"), ("1", "v2-robust-lam1-fix"),
          ("2", "v2-robust-lam2-fix"), ("4", "v2-robust-lam4-fix")]
SEMILLAS = list(range(2, 12))
EPISODIOS = 1000
PARAR = "logs/PARAR_ROBFIX.txt"


def hecha(tag, semilla):
    """Una tirada cuenta solo si dejo su checkpoint final."""
    for d in glob.glob(f"outputs/bench_{tag}__*_seed{semilla}"):
        if os.path.exists(os.path.join(d, "best_model.pt")):
            return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--carril", type=int, required=True)
    ap.add_argument("--de", type=int, default=6)
    args = ap.parse_args()

    unidades = [(lam, tag, s) for lam, tag in BRAZOS for s in SEMILLAS]
    mias = [u for k, u in enumerate(unidades) if k % args.de == args.carril]
    print(f"carril {args.carril}: {len(mias)} tiradas asignadas", flush=True)

    for lam, tag, semilla in mias:
        if os.path.exists(PARAR):
            print("PARAR_ROBFIX presente: salgo sin empezar otra tirada",
                  flush=True)
            return
        if hecha(tag, semilla):
            print(f"  ya hecha: {tag} semilla {semilla}", flush=True)
            continue
        entorno = dict(os.environ)
        entorno["DEEPLJSP_AGENT"] = "v2"
        entorno["DEEPLJSP_V2_LAMBDA"] = lam
        # explicitamente SIN la semantica historica: es el arreglo
        entorno.pop("DEEPLJSP_V2_LEGACY_TRACKING", None)
        entorno["OMP_NUM_THREADS"] = "2"
        entorno["MKL_NUM_THREADS"] = "2"
        t0 = time.time()
        print(f"  entrenando {tag} semilla {semilla} (lambda={lam})",
              flush=True)
        r = subprocess.run(
            [sys.executable, "-X", "utf8", "scripts/run_benchmark.py",
             "--tier", "full", "--tag", tag,
             "--episodes", str(EPISODIOS), "--seeds", str(semilla)],
            env=entorno)
        estado = "ok" if r.returncode == 0 else f"FALLO ({r.returncode})"
        print(f"  {tag} semilla {semilla}: {estado} en "
              f"{(time.time() - t0) / 60:.0f} min", flush=True)
    print("carril hecho", flush=True)


if __name__ == "__main__":
    main()
