# -*- coding: utf-8 -*-
"""Las 12 clasicas con las 30 semillas del brazo principal.

Extiende a 30 semillas las columnas de la politica en la tabla de las
clasicas, hoy calculadas con las tres desplegadas (media [mejor] de 3):
con 30 contra 30 los corchetes quedan en los mismos terminos que GP y
el parrafo de estadistica de orden del 6.3 deja de ser necesario.

Protocolo identico a eval_classic12_{greedy,policy,bo1024_porsemilla}:
mismo parser, mismos LB best-known del E[Cmax], evaluate_policy con
n_samples=N (N=1 es el rollout greedy). Checkpoints resueltos por
semilla como en eval_treinta_semillas.py.

Salida en benchmarks/ext30/ (reanudable por fila):

    python scripts/eval_classic12_treinta.py --n 64 --semillas 12,13
    python scripts/eval_classic12_treinta.py --n 1024 --semillas 7
"""
import argparse
import csv
import os
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import torch                                                   # noqa: E402
torch.set_num_threads(2)

from jobshop_rl.agents_v2 import AgentV2                       # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from scripts.eval_classic12_policy import (FILES, LB,          # noqa: E402
                                           load_instance, localiza,
                                           mid_componentwise)
from scripts.eval_treinta_semillas import ruta_semilla         # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True,
                    help="muestras por instancia: 1, 64 o 1024")
    ap.add_argument("--semillas", type=str, required=True)
    ap.add_argument("--salida", type=str, default="")
    args = ap.parse_args()
    sel = [int(x) for x in args.semillas.split(",")]
    salida = args.salida or f"benchmarks/ext30/classic12_bo{args.n}.csv"
    os.makedirs(os.path.dirname(salida), exist_ok=True)
    hechas = set()
    if os.path.exists(salida):
        hechas = {(r["name"], r["seed"])
                  for r in csv.DictReader(open(salida, encoding="utf-8"))}
    nuevo = not os.path.exists(salida)
    out = open(salida, "a", encoding="utf-8", newline="")
    w = csv.writer(out)
    if nuevo:
        w.writerow(["name", "seed", "lb", "n_samples", "mid", "re",
                    "seconds"])
        out.flush()
    for sem in sel:
        ck = ruta_semilla(sem)
        for name, fichero in FILES.items():
            if (name, str(sem)) in hechas:
                continue
            problema = load_instance(localiza(fichero), name)
            env = EnvironmentFactory.create_from_problem(
                problema, "adaptive", seed=1, problem_id=name)
            agent = AgentV2(env, seed=1, attention_layers=0)
            agent.load_checkpoint(ck)
            t0 = time.time()
            _, schedule, _, _ = agent.evaluate_policy(n_samples=args.n)
            mid = mid_componentwise(schedule)
            re_pct = (mid - LB[name]) / LB[name] * 100
            w.writerow([name, sem, LB[name], args.n, f"{mid:.1f}",
                        f"{re_pct:.4f}", f"{time.time() - t0:.0f}"])
            out.flush()
            print(f"{name} semilla {sem}: RE={re_pct:.2f}%", flush=True)
    out.close()
    print("listo:", salida)


if __name__ == "__main__":
    main()
