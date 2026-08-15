# -*- coding: utf-8 -*-
"""Evalua CUALQUIER brazo sobre las seis instancias de validacion.

Unifica bajo un solo evaluador todos los numeros del conjunto de
validacion. Hasta ahora convivian dos procedencias: la evaluacion que
cada tirada de entrenamiento hace al terminar, de la que salen las
tablas de 6.1 y las ablaciones, y este evaluador independiente, del que
sale la campana de treinta semillas. El protocolo es el mismo (una
pasada greedy mas N-1 muestreadas) pero el flujo de aleatorios difiere,
y sobre las mismas diez semillas dan 13.82 y 13.57: la diferencia es
ruido de un estadistico de minimo, no un error, pero mezclarlas en una
misma afirmacion seria indefendible.

El numero de capas de atencion se deduce del propio punto de control,
para que el brazo con atencion cargue en su arquitectura y no en la
base.

    python scripts/eval_val_brazos.py --tags v2-full-300ep,v2-full-300ep-ext
    python scripts/eval_val_brazos.py --tags v2-attn-1000ep --bo 64
"""
import argparse
import csv
import glob
import os
import re
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import torch                                                   # noqa: E402
torch.set_num_threads(1)

from jobshop_rl.agents_v2 import AgentV2                       # noqa: E402
from jobshop_rl.agents_v2.networks import PolicyValueNetV2     # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.models.interval import final_makespan          # noqa: E402

VAL = [f"int__tai20_15_{k:02d}" for k in range(5, 11)]
# Las sesenta que no entraron ni en entrenamiento ni en validacion: todo
# el benchmark menos la clase 20x15. Sirven para dar potencia a las
# ablaciones, que sobre seis instancias se quedan en la frontera.
TEST60 = [f"int__{c}_{k:02d}"
          for c in ("tai15_15", "tai20_20", "tai30_15", "tai30_20",
                    "tai50_15", "tai50_20")
          for k in range(1, 11)]
# A 64 muestras las 60 costarian 89 h de CPU; cinco por clase bajan a
# 45 h y conservan el equilibrio entre clases, que es lo que importa
# porque los efectos cambian de signo entre ellas
TEST30 = [p for p in TEST60 if int(p[-2:]) <= 5]
CONJUNTOS = {"val": VAL, "test60": TEST60, "test30": TEST30}


def capas_atencion(estado):
    """Cuantos bloques de atencion lleva el punto de control."""
    idx = {int(m.group(1)) for k in estado
           for m in [re.match(r"attention\.(\d+)\.", k)] if m}
    return max(idx) + 1 if idx else 0


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
    # el best-of-N ordena por el criterio lexicografico de la Eq. (3),
    # extremo superior y luego inferior, no por el punto medio
    return ((float(mk.lower) + float(mk.upper)) / 2,
            float(mk.upper), float(mk.lower))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tags", required=True,
                    help="tags del brazo separados por comas; el brazo y "
                         "su extension son el mismo brazo")
    ap.add_argument("--bo", type=int, default=64)
    ap.add_argument("--salida", default="")
    ap.add_argument("--brazo", default="",
                    help="nombre del brazo en el CSV; por defecto el "
                         "primer tag. Sirve para que un brazo troceado "
                         "en varios carriles se agregue como uno solo")
    ap.add_argument("--semillas", default="",
                    help="subconjunto de semillas, p.ej. 2,5,8; vacio = "
                         "todas las del tag. Sirve para equilibrar "
                         "carriles cuando un brazo tiene 3 y otro 7")
    ap.add_argument("--conjunto", default="val",
                    choices=list(CONJUNTOS),
                    help="val = las seis de validacion; test60 = las "
                         "sesenta que no entraron en nada")
    ap.add_argument("--worstcase-only", action="store_true",
                    help="colapsa cada intervalo a su peor caso en el "
                         "encoder, como el brazo sin anchuras. SIN esto, "
                         "sus pesos reciben anchuras que nunca vieron al "
                         "entrenar y la ablacion mide otra cosa")
    args = ap.parse_args()
    if args.worstcase_only:
        os.environ["DEEPLJSP_V2_WORSTCASE_ONLY"] = "1"

    brazo = args.brazo or args.tags.split(",")[0]
    salida = args.salida or f"benchmarks/ext30/val_{brazo}_bo{args.bo}.csv"
    os.makedirs(os.path.dirname(salida), exist_ok=True)
    ya = set()
    if os.path.exists(salida):
        ya = {(r["arm"], r["seed"], r["instance"])
              for r in csv.DictReader(open(salida, encoding="utf-8"))}
    nuevo = not os.path.exists(salida)
    f = open(salida, "a", encoding="utf-8", newline="")
    w = csv.writer(f)
    if nuevo:
        w.writerow(["arm", "seed", "instance", "attn", "re_greedy", "re_bo"])
        f.flush()

    dirs = []
    for tag in args.tags.split(","):
        dirs += sorted(glob.glob(f"outputs/bench_{tag}__*_seed*"))
    if not dirs:
        raise SystemExit(f"sin directorios para {args.tags}")

    sel = {s.strip() for s in args.semillas.split(",")} if args.semillas \
        else None
    for d in dirs:
        sem = d.split("_seed")[-1]
        if sel and sem not in sel:
            continue
        ruta = os.path.join(d, "best_model.pt")
        if not os.path.exists(ruta):
            print(f"  aviso: {d} sin best_model.pt")
            continue
        ck = torch.load(ruta, map_location="cpu", weights_only=False)
        estado = ck["network"] if "network" in ck else ck
        nat = capas_atencion(estado)
        red = PolicyValueNetV2(num_attention_layers=nat)
        red.load_state_dict(estado)
        red.eval()
        t0 = time.time()
        for pid in CONJUNTOS[args.conjunto]:
            if (brazo, sem, pid) in ya:
                continue
            env = EnvironmentFactory.create_from_problem_id(
                pid, "adaptive", seed=1)
            enc = AgentV2(env, seed=1, attention_layers=nat).encoder
            lb = lb_for_problem_name(pid)
            g, g_up, g_lo = rollout(env, red, enc, False, 0)
            mejor, clave = g, (g_up, g_lo)
            for i in range(1, args.bo):
                mid, up, lo = rollout(env, red, enc, True, 1000 + i)
                if (up, lo) < clave:
                    mejor, clave = mid, (up, lo)
            w.writerow([brazo, sem, pid, nat,
                        f"{(g - lb) / lb * 100:.4f}",
                        f"{(mejor - lb) / lb * 100:.4f}"])
            f.flush()
        print(f"[{brazo} semilla {sem}, {nat} capas de atencion] "
              f"{time.time() - t0:.0f} s", flush=True)
    f.close()
    print("listo:", salida)


if __name__ == "__main__":
    main()
