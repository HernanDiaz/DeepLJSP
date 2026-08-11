# -*- coding: utf-8 -*-
"""Evaluacion en el test DMU de los checkpoints CONGELADOS.

Las diez DMU 20x15 ensanchadas (F.15_01) son instancias que ningun
modelo ni protocolo de seleccion ha visto: el test limpio que faltaba.
Se evaluan tal cual, sin re-seleccion, los seis checkpoints de la
clase 20x15:

  ppo-seedN   politicas PPO desplegadas (seeds 2,3,4)
  v3-seedN    clones de auto-mejora (benchmarks/clon_v3)

greedy y best-of-64 con las semillas de evaluacion de siempre
(1000+i). RE respecto a las cotas de literatura (cotas.csv; seis
instancias con optimo exacto). El RPD respecto al best-known de TSN2
se añade cuando termine su campaña.

Salida NUEVA: benchmarks/dmu_test/eval_neural.csv. No toca nada.
"""
import csv
import os
import sys
import time

import numpy as np

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import torch                                                   # noqa: E402
torch.set_num_threads(2)

from jobshop_rl.agents_v2 import AgentV2                       # noqa: E402
from jobshop_rl.agents_v2.networks import PolicyValueNetV2     # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.models.interval import final_makespan          # noqa: E402

MODELOS = {
    "ppo-seed2": "models/v2_final_deepsets_1000ep_seed2.pt",
    "ppo-seed3": "models/v2_final_deepsets_1000ep_seed3.pt",
    "ppo-seed4": "models/v2_final_deepsets_1000ep_seed4.pt",
    "v3-seed1": "benchmarks/clon_v3/clon_v3_seed1.pt",
    "v3-seed2": "benchmarks/clon_v3/clon_v3_seed2.pt",
    "v3-seed3": "benchmarks/clon_v3/clon_v3_seed3.pt",
}
N_BO = 64
SALIDA = "benchmarks/dmu_test/eval_neural.csv"


def lee_cotas():
    out = {}
    for r in csv.DictReader(open("benchmarks/dmu_test/cotas.csv")):
        out["int__" + r["instance"]] = (int(r["lb"]), r["status"])
    return out


def rollout(env, red, enc, muestrear, semilla):
    torch.manual_seed(semilla)
    state = env.reset()
    while state["eligible_ops"]:
        op, gl = enc.encode(state)
        with torch.no_grad():
            logits, _ = red(torch.tensor(op[None], dtype=torch.float32),
                            torch.tensor(gl[None], dtype=torch.float32))
        lg = logits[0, :len(state["eligible_ops"])]
        a = (int(torch.distributions.Categorical(logits=lg).sample())
             if muestrear else int(lg.argmax()))
        state, _, done, _ = env.step(a)
        if done:
            break
    mk = final_makespan(env.job_completion_time)
    return ((float(mk.lower) + float(mk.upper)) / 2, float(mk.upper),
            float(mk.lower))


def main():
    cotas = lee_cotas()
    pids = sorted(cotas)
    filas = []
    for nombre, ruta in MODELOS.items():
        red = PolicyValueNetV2()
        red.load_state_dict(torch.load(ruta, map_location="cpu",
                                       weights_only=True)["network"])
        red.eval()
        t0 = time.time()
        for pid in pids:
            env = EnvironmentFactory.create_from_problem_id(
                pid, "adaptive", seed=1)
            enc = AgentV2(env, seed=1, attention_layers=0).encoder
            lb, status = cotas[pid]
            g_mid, g_up, g_lo = rollout(env, red, enc, False, 0)
            mejor_mid, clave = g_mid, (g_up, g_lo)
            m16_mid = None
            for i in range(1, N_BO):
                mid, up, lo = rollout(env, red, enc, True, 1000 + i)
                if (up, lo) < clave:
                    mejor_mid, clave = mid, (up, lo)
                if i == 15:
                    m16_mid = mejor_mid
            filas.append({
                "modelo": nombre, "instancia": pid, "lb": lb,
                "status": status,
                "re_greedy": (g_mid - lb) / lb * 100,
                "re_bo16": (m16_mid - lb) / lb * 100,
                "re_bo64": (mejor_mid - lb) / lb * 100,
            })
            print(f"  {nombre} {pid}: greedy "
                  f"{filas[-1]['re_greedy']:.2f}% bo64 "
                  f"{filas[-1]['re_bo64']:.2f}%", flush=True)
        print(f"[{nombre}] {time.time() - t0:.0f} s", flush=True)
    with open(SALIDA, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)

    print("\n=== RESUMEN (RE medio sobre 10 DMU) ===")
    for nombre in MODELOS:
        sel = [x for x in filas if x["modelo"] == nombre]
        for m in ("re_greedy", "re_bo16", "re_bo64"):
            v = sum(x[m] for x in sel) / len(sel)
            print(f"  {nombre:>9} {m}: {v:.2f}%")


if __name__ == "__main__":
    main()
