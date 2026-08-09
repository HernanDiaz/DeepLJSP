# -*- coding: utf-8 -*-
"""Prototipo de imitacion v1: el experto es TSN2.

Identico protocolo que proto_imitacion.py (v0) cambiando SOLO el
experto: las 30 soluciones de TSN2 por instancia de entrenamiento
(T2N2/results/phaseB_TS/N2_tuned, formato verificado por replay
exacto: id de operacion = trabajo*m + k, objetivo reproducido bit a
bit en nuestro entorno). El experto medio ronda el 3.6% de RE frente
al 13.0% del pool v2 que uso la v0, asi que la comparacion v0/v1
aisla el efecto de la calidad y coherencia del profesor.

Salida NUEVA: benchmarks/proto_imitacion/clon_v1_ts.pt y
resultados_v1_ts.csv. No toca nada existente.

    python scripts/proto_imitacion_ts.py
"""
import csv
import glob
import os
import re
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

TS_DIR = r"E:/PycharmProjects/DeepLJSP/T2N2/results/phaseB_TS/N2_tuned"
TRAIN = [f"int__tai20_15_{i:02d}" for i in range(1, 5)]
DEV = [f"int__tai20_15_{i:02d}" for i in range(5, 11)]
CKPTS = [f"models/v2_final_deepsets_1000ep_seed{s}.pt" for s in (2, 3, 4)]
M = 15                                # maquinas de la clase 20x15
EPOCAS = 40
LOTE = 256
LR = 1e-3
SEMILLA = 7
SALIDA = "benchmarks/proto_imitacion"


def lee_ts(pid):
    """[(secuencia de trabajos 1-based, mid)] de las 30 runs de TSN2."""
    corto = pid.replace("int__", "")
    f = glob.glob(f"{TS_DIR}/*{corto}*_Sols.csv")
    assert f, f"sin fichero TS para {pid}"
    out = []
    for fila in list(csv.reader(open(f[0], encoding="utf-8",
                                     errors="replace"),
                                delimiter=";"))[1:]:
        ids = [int(x) for x in fila[1].split()]
        jobs = [i // M + 1 for i in ids]
        lo, up = eval(fila[2])
        out.append((jobs, (lo + up) / 2))
    return out


def replay(env, encoder, seq):
    state = env.reset()
    muestras = []
    for job in seq:
        eleg = state["eligible_ops"]
        if not eleg:
            break
        try:
            a = eleg.index(job - 1)
        except ValueError:
            return None
        op, gl = encoder.encode(state)
        if len(eleg) > 1:
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

    t0 = time.time()
    dataset, expertos = [], {}
    for pid in TRAIN:
        env = EnvironmentFactory.create_from_problem_id(pid, "adaptive",
                                                        seed=1)
        agente = AgentV2(env, seed=1, attention_layers=0)
        res, rechazadas = [], 0
        for seq, mid_ts in lee_ts(pid):
            r = replay(env, agente.encoder, seq)
            if r is None:
                rechazadas += 1
                continue
            muestras, mid = r
            assert abs(mid - mid_ts) < 0.51, f"replay no reproduce en {pid}"
            dataset.extend(muestras)
            res.append(re_pct(mid, pid))
        expertos[pid] = sum(res) / len(res)
        print(f"{pid}: {len(res)}/{len(res) + rechazadas} runs, "
              f"RE experto medio {expertos[pid]:.2f}%", flush=True)
    print(f"dataset: {len(dataset)} decisiones "
          f"({time.time() - t0:.0f} s)", flush=True)

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
            tot += float(perdida.detach()) * B
            aciertos += int((logits.argmax(1) == torch.tensor(y)).sum())
            n += B
        if ep % 5 == 0 or ep == EPOCAS - 1:
            print(f"  epoca {ep:>3}: CE={tot / n:.4f} "
                  f"acierto={aciertos / n:.3f}", flush=True)
    print(f"entrenamiento: {time.time() - t0:.0f} s", flush=True)
    torch.save({"network": red.state_dict()},
               os.path.join(SALIDA, "clon_v1_ts.pt"))

    filas = [["instancia", "clon_ts_greedy", "maestro_rl_greedy_medio"]]
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
        filas.append([pid, f"{clon:.2f}", f"{sum(maestro) / 3:.2f}"])
        print(f"  {pid}: clon-TS {clon:.2f}%  politica RL "
              f"{sum(maestro) / 3:.2f}%", flush=True)
    m_c = sum(float(f[1]) for f in filas[1:]) / 6
    m_m = sum(float(f[2]) for f in filas[1:]) / 6
    print(f"\nMEDIAS dev: clon-TS greedy {m_c:.2f}%  "
          f"politica RL greedy {m_m:.2f}%  "
          f"(v0 auto-clon: 19.58%)", flush=True)
    print(f"experto TS imitado (train): "
          f"{sum(expertos.values()) / len(expertos):.2f}%", flush=True)
    with open(os.path.join(SALIDA, "resultados_v1_ts.csv"), "w",
              encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(filas)


if __name__ == "__main__":
    main()
