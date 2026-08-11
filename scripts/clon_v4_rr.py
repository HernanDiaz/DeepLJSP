# -*- coding: utf-8 -*-
"""v4, linea base: ruin & recreate con la politica constructiva.

La via del denoising empieza aqui. Antes de aprender un operador de
reparacion hay que medir que rinde la reparacion SIN aprender: destruir
la cola de una buena solucion y dejar que la politica desplegada la
reconstruya muestreando. Es la maquinaria de la fase B de la v2
(prefijo + resto valido) usada en inferencia, y convierte el
constructor en un mejorador iterativo sin entrenar nada. Si un denoiser
aprendido no bate esta linea base, no ha aprendido nada.

Pregunta medida: a PRESUPUESTO IGUAL de inferencia, ¿reconstruir
iterativamente supera a muestrear desde cero (best-of-64)?

Protocolo por (politica, instancia):
  greedy      una pasada argmax                       (el incumbente 0)
  bo64        64 muestras desde cero, semillas 1000+i (la referencia,
              recalculada aqui para el par exacto)
  R&R         mientras queden pasos: d ~ U[dmin,dmax] decisiones
              destruidas de la cola, replay del prefijo, reconstruccion
              muestreada, aceptar si mejora la clave (C^U, C^L) de la
              Eq. (3)

Contabilidad conservadora: el presupuesto de R&R se mide en pasos de
entorno e INCLUYE los replays de prefijo, que no usan la red; los
forwards de politica se registran aparte. Si R&R gana pagando tambien
los replays, la conclusion no depende de la contabilidad.

Salida NUEVA: benchmarks/clon_v4_rr/. No toca nada existente.

    python scripts/clon_v4_rr.py                    # 3 politicas x dev
    python scripts/clon_v4_rr.py --seeds 1 --instancias 2 --bo 8 \
                                 --presupuesto 8    # humo
"""
import argparse
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
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.models.interval import final_makespan          # noqa: E402

DEV = [f"int__tai20_15_{i:02d}" for i in range(5, 11)]       # TA15-20
POLITICAS = {1: "models/v2_final_deepsets_1000ep_seed2.pt",
             2: "models/v2_final_deepsets_1000ep_seed3.pt",
             3: "models/v2_final_deepsets_1000ep_seed4.pt"}
SALIDA = "benchmarks/clon_v4_rr"    # sobreescribible con --salida


def _paso(env, state, a):
    state, _, done, _ = env.step(a)
    return state, done


def _clave_y_mid(env):
    mk = final_makespan(env.job_completion_time)
    up, lo = float(mk.upper), float(mk.lower)
    return (up, lo), (lo + up) / 2


def reconstruye(env, red, enc, prefijo, semilla):
    """Replay de `prefijo` (trabajos 1-based) y reconstruccion muestreada
    del resto. Devuelve (clave, mid, seq, pasos_env, forwards)."""
    torch.manual_seed(semilla)
    state = env.reset()
    seq, pasos, fwd = [], 0, 0
    for job in prefijo:
        a = state["eligible_ops"].index(job - 1)   # valido por construccion
        seq.append(job)
        state, done = _paso(env, state, a)
        pasos += 1
    while state["eligible_ops"]:
        op, gl = enc.encode(state)
        with torch.no_grad():
            logits, _ = red(torch.tensor(op[None], dtype=torch.float32),
                            torch.tensor(gl[None], dtype=torch.float32))
        lg = logits[0, :len(state["eligible_ops"])]
        a = int(torch.distributions.Categorical(logits=lg).sample())
        fwd += 1
        seq.append(state["eligible_ops"][a] + 1)
        state, done = _paso(env, state, a)
        pasos += 1
        if done:
            break
    clave, mid = _clave_y_mid(env)
    return clave, mid, seq, pasos, fwd


def rollout(env, red, enc, muestrear, semilla):
    """Pasada completa desde cero; misma convencion que el clon v3."""
    torch.manual_seed(semilla)
    state = env.reset()
    seq, pasos = [], 0
    while state["eligible_ops"]:
        op, gl = enc.encode(state)
        with torch.no_grad():
            logits, _ = red(torch.tensor(op[None], dtype=torch.float32),
                            torch.tensor(gl[None], dtype=torch.float32))
        lg = logits[0, :len(state["eligible_ops"])]
        a = (int(torch.distributions.Categorical(logits=lg).sample())
             if muestrear else int(lg.argmax()))
        seq.append(state["eligible_ops"][a] + 1)
        state, done = _paso(env, state, a)
        pasos += 1
        if done:
            break
    clave, mid = _clave_y_mid(env)
    return clave, mid, seq, pasos


def re_pct(mid, pid):
    lb = lb_for_problem_name(pid)
    return (mid - lb) / lb * 100


def un_par(polsem, red, pid, inst_idx, presupuesto, n_bo, dmin, dmax,
           rng, log):
    env = EnvironmentFactory.create_from_problem_id(pid, "adaptive", seed=1)
    enc = AgentV2(env, seed=1, attention_layers=0).encoder

    # incumbente 0: el greedy
    inc_clave, inc_mid, inc_seq, T = rollout(env, red, enc, False, 0)
    re_greedy = re_pct(inc_mid, pid)

    # la referencia bo64, con las semillas de evaluacion de siempre
    mejor, clave = inc_mid, inc_clave
    for i in range(1, n_bo):
        c, mid, _, _ = rollout(env, red, enc, True, 1000 + i)
        if c < clave:
            mejor, clave = mid, c
    re_bo = re_pct(mejor, pid)

    # R&R a presupuesto igual (presupuesto * T pasos de entorno,
    # descontando el greedy inicial que ya esta pagado)
    tope = presupuesto * T
    pasos_tot, fwd_tot, it, acept = T, 0, 0, 0
    sem_base = 300000 * polsem + 500 * inst_idx
    while pasos_tot < tope:
        d = int(rng.integers(dmin, min(dmax, T - 1) + 1))
        prefijo = inc_seq[:T - d]
        c, mid, seq, pasos, fwd = reconstruye(env, red, enc, prefijo,
                                              sem_base + it)
        pasos_tot += pasos
        fwd_tot += fwd
        it += 1
        if c < inc_clave:
            inc_clave, inc_mid, inc_seq = c, mid, seq
            acept += 1
    re_rr = re_pct(inc_mid, pid)
    log(f"    {pid}: greedy {re_greedy:.2f} bo{n_bo} {re_bo:.2f} "
        f"R&R {re_rr:.2f} ({it} it, {acept} aceptadas, "
        f"{fwd_tot} forwards vs {n_bo * T} del bo)")
    return {"politica": polsem, "instancia": pid, "T": T,
            "re_greedy": re_greedy, "re_bo": re_bo, "re_rr": re_rr,
            "iteraciones": it, "aceptadas": acept,
            "pasos_env": pasos_tot, "forwards": fwd_tot}


def main():
    global SALIDA
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--instancias", type=int, default=len(DEV))
    ap.add_argument("--presupuesto", type=int, default=64,
                    help="pasos de entorno permitidos, en multiplos de T")
    ap.add_argument("--bo", type=int, default=64)
    ap.add_argument("--dmin", type=int, default=15)
    ap.add_argument("--dmax", type=int, default=150)
    ap.add_argument("--salida", type=str, default=SALIDA)
    ap.add_argument("--modelos", type=str, default="",
                    help="tres rutas .pt separadas por coma; por defecto "
                         "las politicas PPO desplegadas")
    args = ap.parse_args()
    SALIDA = args.salida
    if args.modelos:
        rutas = args.modelos.split(",")
        assert len(rutas) == args.seeds, "una ruta por politica"
        for i, r in enumerate(rutas, 1):
            assert os.path.exists(r), f"no existe {r}"
            POLITICAS[i] = r
    os.makedirs(SALIDA, exist_ok=True)
    reg = open(os.path.join(SALIDA, "log.txt"), "a", encoding="utf-8")

    def log(m):
        print(m, flush=True)
        reg.write(m + "\n")
        reg.flush()

    log(f"\n=== v4 ruin&recreate ({args.seeds} politicas x "
        f"{args.instancias} instancias, presupuesto {args.presupuesto}xT, "
        f"bo{args.bo}, d U[{args.dmin},{args.dmax}]) ===")
    filas = []
    for polsem in range(1, args.seeds + 1):
        red = PolicyValueNetV2()
        red.load_state_dict(torch.load(POLITICAS[polsem],
                                       map_location="cpu",
                                       weights_only=True)["network"])
        red.eval()
        log(f"  [politica {polsem}: "
            f"{os.path.basename(POLITICAS[polsem])}]")
        rng = np.random.default_rng(polsem)
        t0 = time.time()
        for k, pid in enumerate(DEV[:args.instancias]):
            filas.append(un_par(polsem, red, pid, k, args.presupuesto,
                                args.bo, args.dmin, args.dmax, rng, log))
        log(f"  [politica {polsem}: {time.time() - t0:.0f} s]")
    with open(os.path.join(SALIDA, "resultados.csv"), "w",
              encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)

    log("\n=== RESUMEN ===")
    for c in ("re_greedy", "re_bo", "re_rr"):
        log(f"  {c:>9}: {sum(f[c] for f in filas) / len(filas):.2f}%")
    dif = [f["re_rr"] - f["re_bo"] for f in filas]
    gana = sum(1 for x in dif if x < 0)
    log(f"  R&R mejor que bo{args.bo} en {gana}/{len(dif)} pares "
        f"(dif media {sum(dif) / len(dif):+.2f})")
    if len(dif) >= 10:
        from scipy.stats import wilcoxon
        log(f"  Wilcoxon pareado R&R vs bo: p={wilcoxon(dif).pvalue:.4f}")
    log("  referencias: politica RL bo64 13.4; clon v0 13.94; "
        "experto TS ~3.66")


if __name__ == "__main__":
    main()
