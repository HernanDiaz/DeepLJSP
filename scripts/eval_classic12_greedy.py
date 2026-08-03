# -*- coding: utf-8 -*-
"""La politica a UNA pasada sobre las 12 clasicas, para poder comparar.

La tabla y la figura de las clasicas enfrentaban el best-of-64 de la
politica con la regla evolucionada a una pasada, y encima las agrupaban
en la misma clase computacional. Para arreglarlo hacen falta las dos
esquinas que faltaban: la regla a 64 muestras, que ya estaba calculada
en classic12_tuned.csv (columnas gp64 y gp1024), y la politica a una
pasada greedy, que es lo que calcula este script.

Reutiliza el cargador y las cotas de eval_classic12_policy.py; lo unico
que cambia es n_samples=1, es decir un unico rollout determinista.

Salida NUEVA: benchmarks/eval_classic12_greedy.csv (reanudable).

    python scripts/eval_classic12_greedy.py
"""
import csv
import os
import sys

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.agents_v2 import AgentV2                       # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from scripts.eval_classic12_policy import (CKPTS, FILES, LB,   # noqa: E402
                                           load_instance, localiza,
                                           mid_componentwise)

SALIDA = "benchmarks/eval_classic12_greedy.csv"


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
        w.writerow(["name", "checkpoint", "lb", "mid", "re"])

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
            # n_samples=1 -> solo el rollout greedy (i=0 no muestrea)
            _, schedule, _, _ = agent.evaluate_policy(n_samples=1)
            mid = mid_componentwise(schedule)
            re_pct = (mid - LB[name]) / LB[name] * 100
            w.writerow([name, clave[1], LB[name], f"{mid:.1f}",
                        f"{re_pct:.4f}"])
            out.flush()
            print(f"{name} {clave[1]}: RE={re_pct:.2f}%", flush=True)
    out.close()


if __name__ == "__main__":
    main()
