# -*- coding: utf-8 -*-
"""La politica a 1024 muestras sobre las 12 clasicas.

classic12_tuned.csv trae gp1024 desde hace tiempo: la regla evolucionada
aleatorizada con epsilon-greedy a 1024 muestras da 11.31%, mejor que el
best-of-64 de la politica (12.35%). Sin medir la politica al mismo
presupuesto, la escalera se corta justo donde la comparacion deja de
estar decidida, asi que aqui se mide.

Protocolo IDENTICO al bo1024 de las Taillard (scripts/eval_pending_bo.py):
342 muestras por checkpoint, y el mejor global se decide al agregar los
tres, de modo que el presupuesto total sea 1026 y no 3x1024.

Salida NUEVA: benchmarks/eval_classic12_bo1024.csv (reanudable).

    python scripts/eval_classic12_bo1024.py
"""
import csv
import os
import sys
import time

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.agents_v2 import AgentV2                       # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from scripts.eval_classic12_policy import (CKPTS, FILES, LB,   # noqa: E402
                                           load_instance, localiza,
                                           mid_componentwise)

N_POR_CKPT = 342
SALIDA = "benchmarks/eval_classic12_bo1024.csv"


def main():
    hechas = set()
    if os.path.exists(SALIDA):
        with open(SALIDA, encoding="utf-8") as f:
            hechas = {(r["name"], r["checkpoint"])
                      for r in csv.DictReader(f)}
    nuevo = not os.path.exists(SALIDA) or os.path.getsize(SALIDA) == 0
    out = open(SALIDA, "a", encoding="utf-8", newline="")
    w = csv.writer(out)
    if nuevo:
        w.writerow(["name", "checkpoint", "lb", "n_samples", "mid", "re",
                    "seconds"])

    for name, fichero in FILES.items():
        problema = load_instance(localiza(fichero), name)
        for ck in CKPTS:
            clave = (name, os.path.basename(ck))
            if clave in hechas:
                continue
            env = EnvironmentFactory.create_from_problem(
                problema, "adaptive", seed=1, problem_id=name)
            agent = AgentV2(env, seed=1, attention_layers=0)
            agent.load_checkpoint(ck)
            t0 = time.time()
            _, schedule, _, _ = agent.evaluate_policy(n_samples=N_POR_CKPT)
            mid = mid_componentwise(schedule)
            re_pct = (mid - LB[name]) / LB[name] * 100
            secs = time.time() - t0
            w.writerow([name, clave[1], LB[name], N_POR_CKPT, f"{mid:.1f}",
                        f"{re_pct:.4f}", f"{secs:.0f}"])
            out.flush()
            print(f"{name} {clave[1]}: RE={re_pct:.2f}% ({secs:.0f}s)",
                  flush=True)
    out.close()
    print("hecho")


if __name__ == "__main__":
    main()
