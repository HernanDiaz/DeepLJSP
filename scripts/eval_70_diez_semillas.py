# -*- coding: utf-8 -*-
"""Evalua las 70 instancias con las SIETE semillas de la ampliacion.

Las tres semillas desplegadas (2,3,4) ya tienen deposito sobre las 70
(benchmarks/fair_v2_greedy.csv y eval_fair_bo*.csv). Las siete de la
ampliacion a diez semillas solo se evaluaron en la clase de
entrenamiento. Este script cierra esa asimetria: mismo protocolo,
mismas semillas de evaluacion (1000+i), greedy y best-of-64.

Salida NUEVA: benchmarks/eval70_diez_semillas.csv (una fila por
(semilla, instancia), reanudable: se saltan las ya hechas).

    python scripts/eval_70_diez_semillas.py --bo 64
    python scripts/eval_70_diez_semillas.py --bo 1 --solo-greedy
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
from jobshop_rl.agents_v2.networks import PolicyValueNetV2     # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.models.interval import final_makespan          # noqa: E402

SEMILLAS = {s: f"outputs/bench_v2-full-1000ep-ext-c__6de2c20__"
               f"20260803_071159_seed{s}/best_model.pt"
            for s in range(5, 12)}
CLASES = [("tai15_15", 10), ("tai20_15", 10), ("tai20_20", 10),
          ("tai30_15", 10), ("tai30_20", 10), ("tai50_15", 10),
          ("tai50_20", 10)]
SALIDA = "benchmarks/eval70_diez_semillas.csv"


def instancias():
    out = []
    for clase, n in CLASES:
        for k in range(1, n + 1):
            out.append(f"int__{clase}_{k:02d}")
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


def hechas():
    if not os.path.exists(SALIDA):
        return set()
    return {(r["seed"], r["instance"])
            for r in csv.DictReader(open(SALIDA, encoding="utf-8"))}


def main():
    global SALIDA
    ap = argparse.ArgumentParser()
    ap.add_argument("--bo", type=int, default=64)
    ap.add_argument("--semillas", type=str, default="",
                    help="subconjunto, p.ej. 5,6,7; vacio = todas")
    ap.add_argument("--salida", type=str, default=SALIDA)
    args = ap.parse_args()
    SALIDA = args.salida
    sel = ({int(x) for x in args.semillas.split(",")}
           if args.semillas else set(SEMILLAS))
    ya = hechas()
    nuevo = not os.path.exists(SALIDA)
    f = open(SALIDA, "a", encoding="utf-8", newline="")
    w = csv.writer(f)
    if nuevo:
        w.writerow(["seed", "instance", "cls", "re_greedy", "re_bo"])
        f.flush()
    pids = instancias()
    for sem, ruta in SEMILLAS.items():
        if sem not in sel:
            continue
        red = PolicyValueNetV2()
        ck = torch.load(ruta, map_location="cpu", weights_only=False)
        red.load_state_dict(ck["network"] if "network" in ck else ck)
        red.eval()
        t0 = time.time()
        for pid in pids:
            if (str(sem), pid) in ya:
                continue
            env = EnvironmentFactory.create_from_problem_id(
                pid, "adaptive", seed=1)
            enc = AgentV2(env, seed=1, attention_layers=0).encoder
            lb = lb_for_problem_name(pid)
            g_mid, g_up, g_lo = rollout(env, red, enc, False, 0)
            mejor, clave = g_mid, (g_up, g_lo)
            for i in range(1, args.bo):
                mid, up, lo = rollout(env, red, enc, True, 1000 + i)
                if (up, lo) < clave:
                    mejor, clave = mid, (up, lo)
            w.writerow([sem, pid, pid.split("_", 2)[1] + "_"
                        + pid.split("_")[2],
                        f"{(g_mid - lb) / lb * 100:.4f}",
                        f"{(mejor - lb) / lb * 100:.4f}"])
            f.flush()
        print(f"[semilla {sem}] {time.time() - t0:.0f} s", flush=True)
    f.close()
    print("listo:", SALIDA)


if __name__ == "__main__":
    main()
