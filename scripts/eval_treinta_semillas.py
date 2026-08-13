# -*- coding: utf-8 -*-
"""Evaluador unico de la campana de 30 semillas del brazo principal.

Cubre las tres tiradas del mismo brazo (julio 2-4, ext-c 5-11, ext30
12-31) con un solo protocolo: greedy determinista y best-of-N con
semillas de evaluacion 1000+i, identicas para todas las semillas de
entrenamiento. Dos conjuntos:

    --conjunto val   TA15-TA20 (int__tai20_15_05..10), para seleccionar
                     el campeon sobre validacion (nunca sobre las 70)
    --conjunto 70    las 70 de test, para el campeon y para la media

Salidas en benchmarks/ext30/ (carpeta nueva de esta campana),
reanudables fila a fila. --clases permite trocear un bo grande del
campeon en varios procesos.

    python scripts/eval_treinta_semillas.py --conjunto val --bo 64 --semillas 12,13
    python scripts/eval_treinta_semillas.py --conjunto 70 --bo 1024 --semillas 7 --clases tai15_15,tai20_15
"""
import argparse
import csv
import glob
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

CLASES_70 = [("tai15_15", 10), ("tai20_15", 10), ("tai20_20", 10),
             ("tai30_15", 10), ("tai30_20", 10), ("tai50_15", 10),
             ("tai50_20", 10)]


def ruta_semilla(s):
    """Checkpoint best_model.pt de la semilla s, tirada que corresponda."""
    if 2 <= s <= 4:
        return (f"outputs/bench_v2-full-1000ep__012ecd2__"
                f"20260703_174122_seed{s}/best_model.pt")
    if 5 <= s <= 11:
        return (f"outputs/bench_v2-full-1000ep-ext-c__6de2c20__"
                f"20260803_071159_seed{s}/best_model.pt")
    rutas = glob.glob(f"outputs/bench_v2-full-1000ep-ext30-*__*"
                      f"_seed{s}/best_model.pt")
    if len(rutas) != 1:
        raise SystemExit(f"semilla {s}: {len(rutas)} checkpoints ({rutas})")
    return rutas[0]


def instancias(conjunto, filtro, pids=None):
    """Instancias del conjunto, con filtro por clase o lista explicita.

    La lista explicita existe para trocear un bo grande a mano: el coste
    por instancia va de 41 s en 15x15 a 408 s en 50x20 al mismo numero
    de muestras, asi que repartir por numero de instancias deja carriles
    parados esperando al que lleva las grandes.
    """
    if pids:
        return list(pids)
    if conjunto == "val":
        out = [f"int__tai20_15_{k:02d}" for k in range(5, 11)]
    else:
        out = [f"int__{clase}_{k:02d}" for clase, n in CLASES_70
               for k in range(1, n + 1)]
    if filtro:
        out = [p for p in out if p.split("__")[1].rsplit("_", 1)[0] in filtro]
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
    ap = argparse.ArgumentParser()
    ap.add_argument("--conjunto", choices=["val", "70"], required=True)
    ap.add_argument("--bo", type=int, default=64)
    ap.add_argument("--semillas", type=str, required=True,
                    help="p.ej. 12,13,14")
    ap.add_argument("--clases", type=str, default="",
                    help="filtro de clases, p.ej. tai15_15,tai20_15")
    ap.add_argument("--salida", type=str, default="")
    args = ap.parse_args()
    sel = [int(x) for x in args.semillas.split(",")]
    filtro = set(args.clases.split(",")) if args.clases else None
    salida = args.salida or (f"benchmarks/ext30/eval_{args.conjunto}"
                             f"_bo{args.bo}.csv")
    os.makedirs(os.path.dirname(salida), exist_ok=True)
    ya = set()
    if os.path.exists(salida):
        ya = {(r["seed"], r["instance"])
              for r in csv.DictReader(open(salida, encoding="utf-8"))}
    nuevo = not os.path.exists(salida)
    f = open(salida, "a", encoding="utf-8", newline="")
    w = csv.writer(f)
    if nuevo:
        w.writerow(["seed", "instance", "cls", "re_greedy", "re_bo"])
        f.flush()
    pids = instancias(args.conjunto, filtro)
    for sem in sel:
        red = PolicyValueNetV2()
        ck = torch.load(ruta_semilla(sem), map_location="cpu",
                        weights_only=False)
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
            w.writerow([sem, pid, pid.split("__")[1].rsplit("_", 1)[0],
                        f"{(g_mid - lb) / lb * 100:.4f}",
                        f"{(mejor - lb) / lb * 100:.4f}"])
            f.flush()
        print(f"[semilla {sem}] {time.time() - t0:.0f} s", flush=True)
    f.close()
    print("listo:", salida)


if __name__ == "__main__":
    main()
