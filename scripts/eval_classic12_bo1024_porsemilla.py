# -*- coding: utf-8 -*-
"""La politica a 1024 muestras POR SEMILLA sobre las 12 clasicas.

eval_classic12_bo1024.py reparte 342 muestras entre los tres
checkpoints y agrega, que es el protocolo del bo1024 de las Taillard:
1026 muestras en total. Sirve para el texto, pero no para la figura de
la escalera, porque alli el peldano de GP es "una regla con 1024
muestras, promediado sobre cual de las 30 te toque". Enfrentar eso con
un numero que usa TRES redes empareja el presupuesto en muestras y lo
desempareja en modelos.

Aqui cada checkpoint recibe sus 1024 muestras y se promedia sobre las
tres semillas, que es el analogo exacto: una tirada de cada metodo, al
mismo presupuesto.

Salida NUEVA: benchmarks/eval_classic12_bo1024_porsemilla.csv

    python scripts/eval_classic12_bo1024_porsemilla.py
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

N = 1024
SALIDA = "benchmarks/eval_classic12_bo1024_porsemilla.csv"


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
            _, schedule, _, _ = agent.evaluate_policy(n_samples=N)
            mid = mid_componentwise(schedule)
            re_pct = (mid - LB[name]) / LB[name] * 100
            w.writerow([name, clave[1], LB[name], N, f"{mid:.1f}",
                        f"{re_pct:.4f}", f"{time.time() - t0:.0f}"])
            out.flush()
            print(f"{name} {clave[1]}: RE={re_pct:.2f}%", flush=True)
    out.close()
    print("hecho")


if __name__ == "__main__":
    main()
