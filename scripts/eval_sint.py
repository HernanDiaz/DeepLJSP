# -*- coding: utf-8 -*-
"""Evaluacion pareada PPO vs clones v3 en las Taillard sinteticas.

Sin cotas: la pregunta es el PAR (warm start -> clon) sobre cada
instancia no vista de la misma familia. Se reporta el makespan medio
(mid) de greedy/bo16/bo64 y la diferencia porcentual pareada
(v3 - ppo)/ppo por instancia, con Wilcoxon sobre los 30 pares.

Salida NUEVA: benchmarks/sint_test/eval_neural.csv.
"""
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
from jobshop_rl.agents_v2.networks import PolicyValueNetV2     # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.models.interval import final_makespan          # noqa: E402

PARES = [("ppo-seed2", "models/v2_final_deepsets_1000ep_seed2.pt",
          "v3-seed1", "benchmarks/clon_v3/clon_v3_seed1.pt"),
         ("ppo-seed3", "models/v2_final_deepsets_1000ep_seed3.pt",
          "v3-seed2", "benchmarks/clon_v3/clon_v3_seed2.pt"),
         ("ppo-seed4", "models/v2_final_deepsets_1000ep_seed4.pt",
          "v3-seed3", "benchmarks/clon_v3/clon_v3_seed3.pt")]
PIDS = [f"int__sint20_15_{k:02d}" for k in range(1, 11)]
N_BO = 64
SALIDA = "benchmarks/sint_test/eval_neural.csv"


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


def evalua(red, pid):
    env = EnvironmentFactory.create_from_problem_id(pid, "adaptive",
                                                    seed=1)
    enc = AgentV2(env, seed=1, attention_layers=0).encoder
    g_mid, g_up, g_lo = rollout(env, red, enc, False, 0)
    mejor, clave = g_mid, (g_up, g_lo)
    m16 = None
    for i in range(1, N_BO):
        mid, up, lo = rollout(env, red, enc, True, 1000 + i)
        if (up, lo) < clave:
            mejor, clave = mid, (up, lo)
        if i == 15:
            m16 = mejor
    return g_mid, m16, mejor


def main():
    os.makedirs("benchmarks/sint_test", exist_ok=True)
    filas = []
    for nom_p, ruta_p, nom_c, ruta_c in PARES:
        redes = {}
        for nom, ruta in ((nom_p, ruta_p), (nom_c, ruta_c)):
            r = PolicyValueNetV2()
            r.load_state_dict(torch.load(ruta, map_location="cpu",
                                         weights_only=True)["network"])
            r.eval()
            redes[nom] = r
        t0 = time.time()
        for pid in PIDS:
            fila = {"par": f"{nom_p}->{nom_c}", "instancia": pid}
            for nom in (nom_p, nom_c):
                g, b16, b64 = evalua(redes[nom], pid)
                pref = "ppo" if nom.startswith("ppo") else "v3"
                fila[f"{pref}_greedy"], fila[f"{pref}_bo16"], \
                    fila[f"{pref}_bo64"] = g, b16, b64
            fila["dif_bo64_pct"] = ((fila["v3_bo64"] - fila["ppo_bo64"])
                                    / fila["ppo_bo64"] * 100)
            filas.append(fila)
            print(f"  {fila['par']} {pid}: ppo {fila['ppo_bo64']:.1f} "
                  f"v3 {fila['v3_bo64']:.1f} "
                  f"({fila['dif_bo64_pct']:+.2f}%)", flush=True)
        print(f"[{nom_p}->{nom_c}] {time.time() - t0:.0f} s", flush=True)
    with open(SALIDA, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)

    difs = [f["dif_bo64_pct"] for f in filas]
    gana = sum(1 for d in difs if d < 0)
    print("\n=== RESUMEN bo64 pareado (30 pares) ===")
    print(f"  v3 mejor en {gana}/{len(difs)} | dif media "
          f"{sum(difs) / len(difs):+.2f}%")
    from scipy.stats import wilcoxon
    print(f"  Wilcoxon: p={wilcoxon(difs).pvalue:.4f}")


if __name__ == "__main__":
    main()
