# -*- coding: utf-8 -*-
"""Prototipo de imitacion: clonar las mejores soluciones de un pool.

La pregunta de diseno (conversacion 2026-08-09): ¿se puede entrenar por
via SUPERVISADA una politica que produzca de una pasada la calidad que
hoy cuesta muestrear? Aqui el experto son las mejores K soluciones del
pool v2 de cada instancia de entrenamiento (seeds/*.csv, 1024 por
instancia, secuencia + intervalo), pero el pipeline acepta cualquier
experto que entregue ordenes de proceso: las soluciones de TSN2
entrarian por el mismo camino.

Fases:
 1. replay: cada secuencia experta se reproduce en el entorno y cada
    decision se convierte en (features de candidatas, indice experto);
 2. entrenamiento: la MISMA red PolicyValueNetV2 (cabeza de valor sin
    usar), entropia cruzada, sin PPO, sin reward, sin pesos;
 3. evaluacion: greedy del clon en TA15-20 contra el greedy de los
    tres checkpoints maestros, y la calidad del experto imitado.

Salida NUEVA: benchmarks/proto_imitacion/ (dataset resumen, modelo,
resultados). No toca nada existente. Threads limitados a 2 para
convivir con la cola de entrenamiento en marcha.

    python scripts/proto_imitacion.py
"""
import csv
import glob
import json
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
import torch.nn.functional as F                                # noqa: E402
torch.set_num_threads(2)

from jobshop_rl.agents_v2 import AgentV2                       # noqa: E402
from jobshop_rl.agents_v2.networks import PolicyValueNetV2     # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.models.interval import Interval, final_makespan  # noqa: E402

TRAIN = [f"int__tai20_15_{i:02d}" for i in range(1, 5)]    # TA11-14
DEV = [f"int__tai20_15_{i:02d}" for i in range(5, 11)]     # TA15-20
CKPTS = [f"models/v2_final_deepsets_1000ep_seed{s}.pt" for s in (2, 3, 4)]
K_EXPERTO = 16          # mejores K del pool por instancia
EPOCAS = 40
LOTE = 256
LR = 1e-3
SEMILLA = 7
SALIDA = "benchmarks/proto_imitacion"


def lee_pool(pid):
    """[(seq jobs 1-based, lower, upper)] ordenado por (upper, lower)."""
    ruta = f"seeds/{pid}_v2_pool.csv"
    sols = []
    for linea in open(ruta, encoding="utf-8"):
        linea = linea.strip()
        if not linea:
            continue
        seq_txt, inter = linea.split(";")
        lo, up = json.loads(inter)
        sols.append(([int(x) for x in seq_txt.split()], float(lo),
                     float(up)))
    sols.sort(key=lambda t: (t[2], t[1]))
    return sols


def replay(env, encoder, seq):
    """Reproduce una secuencia experta y devuelve las decisiones."""
    state = env.reset()
    muestras = []
    for job in seq:
        eleg = state["eligible_ops"]
        if not eleg:
            break
        try:
            a = eleg.index(job - 1)
        except ValueError:
            return None                  # secuencia inconsistente
        op, gl = encoder.encode(state)
        if len(eleg) > 1:                # decisiones triviales no ensenan
            muestras.append((op.astype(np.float32),
                             gl.astype(np.float32), a))
        state, _, done, _ = env.step(a)
    m = final_makespan(env.job_completion_time)
    mid = ((float(m.lower) + float(m.upper)) / 2
           if isinstance(m, Interval) else float(m))
    return muestras, mid


def greedy(env, red, encoder):
    state = env.reset()
    while state["eligible_ops"]:
        op, gl = encoder.encode(state)
        with torch.no_grad():
            logits, _ = red(torch.tensor(op[None], dtype=torch.float32),
                            torch.tensor(gl[None], dtype=torch.float32))
        a = int(logits[0, :len(state["eligible_ops"])].argmax())
        state, _, done, _ = env.step(a)
        if done:
            break
    m = final_makespan(env.job_completion_time)
    return (float(m.lower) + float(m.upper)) / 2


def re_pct(mid, pid):
    lb = lb_for_problem_name(pid)
    return (mid - lb) / lb * 100


def main():
    os.makedirs(SALIDA, exist_ok=True)
    torch.manual_seed(SEMILLA)
    rng = np.random.default_rng(SEMILLA)

    # ---- fase 1: dataset por replay -------------------------------
    t0 = time.time()
    dataset, expertos = [], {}
    for pid in TRAIN:
        env = EnvironmentFactory.create_from_problem_id(pid, "adaptive",
                                                        seed=1)
        agente = AgentV2(env, seed=1, attention_layers=0)
        pool = lee_pool(pid)[:K_EXPERTO]
        res, rechazadas = [], 0
        for seq, lo, up in pool:
            r = replay(env, agente.encoder, seq)
            if r is None:
                rechazadas += 1
                continue
            muestras, mid = r
            dataset.extend(muestras)
            res.append(re_pct(mid, pid))
        expertos[pid] = sum(res) / len(res)
        print(f"{pid}: {len(pool) - rechazadas}/{len(pool)} secuencias, "
              f"RE experto medio {expertos[pid]:.2f}%", flush=True)
    print(f"dataset: {len(dataset)} decisiones "
          f"({time.time() - t0:.0f} s)", flush=True)

    # ---- fase 2: entrenamiento supervisado ------------------------
    red = PolicyValueNetV2()
    opt = torch.optim.Adam(red.parameters(), lr=LR)
    idx = np.arange(len(dataset))
    t0 = time.time()
    for ep in range(EPOCAS):
        rng.shuffle(idx)
        tot, aciertos, n = 0.0, 0, 0
        for ini in range(0, len(idx), LOTE):
            lote = [dataset[i] for i in idx[ini:ini + LOTE]]
            mx = max(op.shape[0] for op, _, _ in lote)
            B = len(lote)
            ops = np.zeros((B, mx, 16), dtype=np.float32)
            gls = np.zeros((B, 12), dtype=np.float32)
            mask = np.zeros((B, mx), dtype=bool)
            y = np.zeros(B, dtype=np.int64)
            for b, (op, gl, a) in enumerate(lote):
                ops[b, :op.shape[0]] = op
                gls[b] = gl
                mask[b, :op.shape[0]] = True
                y[b] = a
            logits, _ = red(torch.tensor(ops), torch.tensor(gls),
                            torch.tensor(mask))
            perdida = F.cross_entropy(logits, torch.tensor(y))
            opt.zero_grad()
            perdida.backward()
            opt.step()
            tot += float(perdida) * B
            aciertos += int((logits.argmax(1) == torch.tensor(y)).sum())
            n += B
        if ep % 5 == 0 or ep == EPOCAS - 1:
            print(f"  epoca {ep:>3}: CE={tot / n:.4f} "
                  f"acierto={aciertos / n:.3f}", flush=True)
    print(f"entrenamiento: {time.time() - t0:.0f} s", flush=True)
    torch.save({"network": red.state_dict()},
               os.path.join(SALIDA, "clon_v0.pt"))

    # ---- fase 3: evaluacion greedy en desarrollo ------------------
    filas = [["instancia", "clon_greedy", "maestro_greedy_medio",
              "experto_entrenado_re"]]
    print("\n== greedy en TA15-20 ==", flush=True)
    for pid in DEV:
        env = EnvironmentFactory.create_from_problem_id(pid, "adaptive",
                                                        seed=1)
        agente = AgentV2(env, seed=1, attention_layers=0)
        clon = re_pct(greedy(env, red, agente.encoder), pid)
        maestro = []
        for ck in CKPTS:
            agente.load_checkpoint(ck)
            torch.manual_seed(0)
            state = env.reset()
            while state["eligible_ops"]:
                salida = agente.select_action(state, training=False)
                a = salida[0] if isinstance(salida, tuple) else salida
                a = min(int(a), len(state["eligible_ops"]) - 1)
                state, _, done, _ = env.step(a)
                if done:
                    break
            m = final_makespan(env.job_completion_time)
            maestro.append(re_pct((float(m.lower) + float(m.upper)) / 2,
                                  pid))
        filas.append([pid, f"{clon:.2f}",
                      f"{sum(maestro) / 3:.2f}", ""])
        print(f"  {pid}: clon {clon:.2f}%  maestros "
              f"{sum(maestro) / 3:.2f}%", flush=True)
    m_c = sum(float(f[1]) for f in filas[1:]) / 6
    m_m = sum(float(f[2]) for f in filas[1:]) / 6
    print(f"\nMEDIAS dev: clon greedy {m_c:.2f}%  "
          f"maestros greedy {m_m:.2f}%", flush=True)
    print(f"experto imitado (train): "
          f"{sum(expertos.values()) / len(expertos):.2f}%", flush=True)
    with open(os.path.join(SALIDA, "resultados_v0.csv"), "w",
              encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(filas)


if __name__ == "__main__":
    main()
