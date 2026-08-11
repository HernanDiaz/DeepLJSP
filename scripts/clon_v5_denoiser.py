# -*- coding: utf-8 -*-
"""Clon v5: el denoiser — entrenar sobre estados de REPARACION.

La matriz v4/v4b/v4c/v4d dejo tres hechos: la profundidad de
destruccion es la palanca grande (cola->completa: 16.2->13.7), el
muestreador no lo es (13.73 ~ 13.89 desde politicas separadas por un
punto), y ninguna politica construida transfiere su calidad a las
continuaciones porque NUNCA VIO estados de reparacion — covariate
shift en inferencia, el espejo del que la v1 sufrio en entrenamiento.

La v5 entrena exactamente esa distribucion: estados que el arnes
ruin & recreate visita. Cada par de entrenamiento es

  incumbente PROPIO (rollout de la politica actual)
  -> prefijo tras destruir d ~ U[15, T] decisiones (d=T: reinicio)
  -> completacion experta: el resto valido de una solucion TSN2
     (resto_experto), etiquetando las decisiones con opcion real

Guardas heredadas: warm start rotatorio desde los CLONES v3 (el mejor
despliegue conocido, bo64 12.76), ancla KL contra el warm start (no
degradar la construccion mientras se aprende a reparar), premio de
entropia, seleccion de ronda por la METRICA DE DESPLIEGUE del
denoiser — la reparacion en desarrollo con el arnes v4 (d completo,
presupuesto 64xT, semillas fijas) — y restauracion si nada mejora.

Exito prerregistrado (DIARIO_CLON.md): reparacion dev < 12.76 (bo64
de los clones) y < 13.73/13.89 (reparacion ciega).

Salida NUEVA: benchmarks/clon_v5/. No toca nada existente.

    python scripts/clon_v5_denoiser.py                  # 3 semillas
    python scripts/clon_v5_denoiser.py --seeds 1 --rondas 2 \
        --pares 6 --presupuesto-eval 16                 # humo
"""
import argparse
import csv
import glob
import os
import sys
import time
from collections import Counter

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
from jobshop_rl.models.interval import final_makespan          # noqa: E402

TS_DIR = r"E:/PycharmProjects/DeepLJSP/T2N2/results/phaseB_TS/N2_tuned"
TRAIN = [f"int__tai20_15_{i:02d}" for i in range(1, 5)]      # TA11-14
DEV = [f"int__tai20_15_{i:02d}" for i in range(5, 11)]       # TA15-20
WARM = {1: "benchmarks/clon_v3/clon_v3_seed1.pt",
        2: "benchmarks/clon_v3/clon_v3_seed2.pt",
        3: "benchmarks/clon_v3/clon_v3_seed3.pt"}
M = 15
RUNS_TRAIN = 24              # runs TSN2 por instancia (split de la v2)
DMIN = 15
SALIDA = "benchmarks/clon_v5"


def lee_ts(pid, rng):
    corto = pid.replace("int__", "")
    f = glob.glob(f"{TS_DIR}/*{corto}*_Sols.csv")
    assert f, f"sin fichero TS para {pid}"
    out = []
    for fila in list(csv.reader(open(f[0], encoding="utf-8",
                                     errors="replace"),
                                delimiter=";"))[1:]:
        out.append([int(x) // M + 1 for x in fila[1].split()])
    idx = rng.permutation(len(out))
    return [out[i] for i in idx[:RUNS_TRAIN]]     # mismo espiritu de split


def resto_experto(seq, hechas):
    quedan = Counter(hechas)
    out = []
    for j in seq:
        if quedan.get(j, 0):
            quedan[j] -= 1
        else:
            out.append(j)
    return out


def _paso(env, state, a):
    state, _, done, _ = env.step(a)
    return state, done


def rollout(env, red, enc, muestrear, semilla, devolver_seq=False):
    torch.manual_seed(semilla)
    state = env.reset()
    seq = []
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
        if done:
            break
    mk = final_makespan(env.job_completion_time)
    r = ((float(mk.lower) + float(mk.upper)) / 2, float(mk.upper),
         float(mk.lower))
    return (r, seq) if devolver_seq else r


def re_pct(mid, pid):
    lb = lb_for_problem_name(pid)
    return (mid - lb) / lb * 100


def lote_tensor(lote):
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
    return (torch.tensor(ops), torch.tensor(gls), torch.tensor(mask),
            torch.tensor(y))


# ------------------------------------------------- datos de reparacion
def pares_reparacion(red, ts_sols, pid, sem, ronda, n_pares, rng, log):
    """Estados del arnes de reparacion etiquetados por el experto.

    Incumbentes propios frescos de la politica ACTUAL (la distribucion
    real del arnes), prefijo tras d ~ U[DMIN, T], completacion con el
    resto valido de una solucion TSN2 al azar."""
    env = EnvironmentFactory.create_from_problem_id(pid, "adaptive",
                                                    seed=1)
    enc = AgentV2(env, seed=1, attention_layers=0).encoder
    incumbentes, claves = [], []
    for i in range(4):
        (mid, up, lo), seq = rollout(env, red, enc, i > 0,
                                     400000 * sem + 2000 * ronda + i,
                                     devolver_seq=True)
        incumbentes.append(seq)
        claves.append((up, lo))
    mejor_inc = incumbentes[claves.index(min(claves))]
    T = len(incumbentes[0])
    muestras = 0
    out = []
    for p in range(n_pares):
        inc = incumbentes[int(rng.integers(len(incumbentes)))]
        d = int(rng.integers(DMIN, T + 1))
        prefijo = inc[:T - d]
        # v5.1: completaciones mixtas 50/50. La CE experta pura movio
        # demasiada masa (colapso de H en un solo paso de ronda, 3/3
        # semillas); la mitad de los pares completa ahora con el MEJOR
        # incumbente PROPIO — el ancla en distribucion que el dataset
        # mixto de la v2 demostro estabilizadora — y la otra mitad
        # conserva la señal de denoising del experto TSN2.
        if p % 2 == 0:
            experto = ts_sols[int(rng.integers(len(ts_sols)))]
        else:
            experto = mejor_inc
        state = env.reset()
        hechas = Counter()
        ok = True
        for job in prefijo:
            eleg = state["eligible_ops"]
            try:
                a = eleg.index(job - 1)
            except ValueError:
                ok = False
                break
            hechas[job] += 1
            state, done = _paso(env, state, a)
        if not ok:
            continue
        for job in resto_experto(experto, hechas):
            eleg = state["eligible_ops"]
            if not eleg:
                break
            try:
                a = eleg.index(job - 1)
            except ValueError:
                break
            if len(eleg) > 1:
                op, gl = enc.encode(state)
                out.append((op.astype(np.float32),
                            gl.astype(np.float32), a))
                muestras += 1
            state, done = _paso(env, state, a)
    log(f"    {pid}: {muestras} decisiones de reparacion")
    return out


# ---------------------------------------------- evaluacion del denoiser
def eval_reparacion(red, presupuesto, dmax=299):
    """El arnes v4 sobre desarrollo con semillas fijas: greedy inicial,
    luego R&R a presupuesto*T pasos. Devuelve (RE reparacion, RE bo16
    de control de construccion)."""
    rep, bo16 = [], []
    for k, pid in enumerate(DEV):
        env = EnvironmentFactory.create_from_problem_id(pid, "adaptive",
                                                        seed=1)
        enc = AgentV2(env, seed=1, attention_layers=0).encoder
        rng = np.random.default_rng(900 + k)
        (mid, up, lo), seq = rollout(env, red, enc, False, 0,
                                     devolver_seq=True)
        inc_clave, inc_mid, inc_seq = (up, lo), mid, seq
        T = len(seq)
        # control barato de construccion: prefijo bo16 de las semillas
        # de evaluacion de siempre
        mejor, clave = mid, inc_clave
        for i in range(1, 16):
            c_mid, c_up, c_lo = rollout(env, red, enc, True, 1000 + i)
            if (c_up, c_lo) < clave:
                mejor, clave = c_mid, (c_up, c_lo)
        bo16.append(re_pct(mejor, pid))
        # el control bo16 es diagnostico y NO consume presupuesto: el
        # despliegue medido es greedy + reparacion hasta presupuesto*T,
        # identico al arnes v4
        pasos, it = T, 0
        tope = presupuesto * T
        while pasos < tope:
            d = int(rng.integers(DMIN, min(dmax, T - 1) + 1))
            prefijo = inc_seq[:T - d]
            torch.manual_seed(700000 + 1000 * k + it)
            state = env.reset()
            seq2 = []
            for job in prefijo:
                a = state["eligible_ops"].index(job - 1)
                seq2.append(job)
                state, done = _paso(env, state, a)
                pasos += 1
            while state["eligible_ops"]:
                op, gl = enc.encode(state)
                with torch.no_grad():
                    logits, _ = red(
                        torch.tensor(op[None], dtype=torch.float32),
                        torch.tensor(gl[None], dtype=torch.float32))
                lg = logits[0, :len(state["eligible_ops"])]
                a = int(torch.distributions.Categorical(
                    logits=lg).sample())
                seq2.append(state["eligible_ops"][a] + 1)
                state, done = _paso(env, state, a)
                pasos += 1
                if done:
                    break
            mk = final_makespan(env.job_completion_time)
            c = (float(mk.upper), float(mk.lower))
            if c < inc_clave:
                inc_clave = c
                inc_mid = (float(mk.lower) + float(mk.upper)) / 2
                inc_seq = seq2
            it += 1
        rep.append(re_pct(inc_mid, pid))
    n = len(DEV)
    return sum(rep) / n, sum(bo16) / n


def una_semilla(sem, rondas, epocas, n_pares, lr, ent_coef, kl_coef,
                paciencia, presupuesto_eval, log):
    torch.manual_seed(sem)
    rng = np.random.default_rng(sem)
    red = PolicyValueNetV2()
    warm = WARM[(sem - 1) % 3 + 1]
    red.load_state_dict(torch.load(warm, map_location="cpu",
                                   weights_only=True)["network"])
    red0 = PolicyValueNetV2()
    red0.load_state_dict(torch.load(warm, map_location="cpu",
                                    weights_only=True)["network"])
    red0.eval()
    for q in red0.parameters():
        q.requires_grad_(False)
    log(f"[semilla {sem}] warm start desde {os.path.basename(warm)}")
    t0 = time.time()
    rep0, bo16_0 = eval_reparacion(red, presupuesto_eval)
    log(f"[semilla {sem}] antes: reparacion {rep0:.2f}% "
        f"bo16 {bo16_0:.2f}% ({time.time() - t0:.0f} s)")
    ts = {pid: lee_ts(pid, rng) for pid in TRAIN}

    opt = torch.optim.Adam(red.parameters(), lr=lr)
    mejor_rep, mejor_estado, sin_mejora = rep0, None, 0
    log(f"  [linea base a batir: reparacion={rep0:.2f}; listones "
        f"prerregistrados: 12.76 (bo64 clones) y 13.73 (R&R ciego)]")
    for ronda in range(rondas):
        t0 = time.time()
        red.eval()
        train = []
        for pid in TRAIN:
            train.extend(pares_reparacion(red, ts[pid], pid, sem, ronda,
                                          n_pares, rng, log))
        idx = np.arange(len(train))
        red.train()
        ent_media, n_lotes = 0.0, 0
        for _ in range(epocas):
            rng.shuffle(idx)
            for ini in range(0, len(idx), 256):
                ops, gls, mask, y = lote_tensor(
                    [train[i] for i in idx[ini:ini + 256]])
                logits, _ = red(ops, gls, mask)
                logp = F.log_softmax(logits.masked_fill(~mask, -1e9),
                                     dim=1)
                ent = -(logp.exp() * logp).masked_fill(
                    ~mask, 0.0).sum(1).mean()
                with torch.no_grad():
                    logits0, _ = red0(ops, gls, mask)
                    logp0 = F.log_softmax(
                        logits0.masked_fill(~mask, -1e9), dim=1)
                kl = (logp0.exp() * (logp0 - logp)).masked_fill(
                    ~mask, 0.0).sum(1).mean()
                perdida = (F.cross_entropy(logits, y) - ent_coef * ent
                           + kl_coef * kl)
                opt.zero_grad()
                perdida.backward()
                opt.step()
                ent_media += float(ent.detach())
                n_lotes += 1
        red.eval()
        rep_r, bo16_r = eval_reparacion(red, presupuesto_eval)
        marca = ""
        if rep_r < mejor_rep:
            mejor_rep, sin_mejora = rep_r, 0
            mejor_estado = {k: v.clone()
                            for k, v in red.state_dict().items()}
            marca = " *"
        else:
            sin_mejora += 1
        log(f"  ronda {ronda:>2}: {len(train)} dec. "
            f"H={ent_media / max(n_lotes, 1):.3f} | "
            f"dev reparacion={rep_r:.2f} bo16={bo16_r:.2f}{marca} "
            f"({time.time() - t0:.0f} s)")
        if sin_mejora >= paciencia:
            log(f"  parada temprana en la ronda {ronda}")
            break
    if mejor_estado:
        red.load_state_dict(mejor_estado)
    else:
        red.load_state_dict(torch.load(warm, map_location="cpu",
                                       weights_only=True)["network"])
        log("  ninguna ronda mejoro la linea base: RESTAURADO el "
            "warm start")
    rep1, bo16_1 = eval_reparacion(red, presupuesto_eval)
    log(f"[semilla {sem}] DESPUES: reparacion {rep1:.2f}% "
        f"bo16 {bo16_1:.2f}%")
    torch.save({"network": red.state_dict()},
               os.path.join(SALIDA, f"clon_v5_seed{sem}.pt"))
    return {"semilla": sem, "rep_antes": rep0, "bo16_antes": bo16_0,
            "rep_despues": rep1, "bo16_despues": bo16_1}


def main():
    global SALIDA
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--rondas", type=int, default=8)
    ap.add_argument("--epocas", type=int, default=3)
    ap.add_argument("--pares", type=int, default=24)
    ap.add_argument("--lr", type=float, default=5e-5)
    ap.add_argument("--ent", type=float, default=0.01)
    ap.add_argument("--kl", type=float, default=0.5)
    ap.add_argument("--paciencia", type=int, default=4)
    ap.add_argument("--presupuesto-eval", type=int, default=64)
    ap.add_argument("--salida", type=str, default=SALIDA)
    args = ap.parse_args()
    SALIDA = args.salida
    os.makedirs(SALIDA, exist_ok=True)
    reg = open(os.path.join(SALIDA, "log.txt"), "a", encoding="utf-8")

    def log(m):
        print(m, flush=True)
        reg.write(m + "\n")
        reg.flush()

    log(f"\n=== clon v5 denoiser ({args.seeds} semillas, {args.rondas} "
        f"rondas x {args.epocas} epocas, pares={args.pares}, "
        f"lr={args.lr}, ent={args.ent}, kl={args.kl}, "
        f"paciencia={args.paciencia}, eval={args.presupuesto_eval}xT, "
        f"salida={SALIDA}) ===")
    filas = []
    for sem in range(1, args.seeds + 1):
        filas.append(una_semilla(sem, args.rondas, args.epocas,
                                 args.pares, args.lr, args.ent, args.kl,
                                 args.paciencia, args.presupuesto_eval,
                                 log))
    with open(os.path.join(SALIDA, "resultados.csv"), "w",
              encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    log("\n=== RESUMEN ===")
    for c in ("rep_antes", "rep_despues", "bo16_antes", "bo16_despues"):
        log(f"  {c:>13}: {sum(f[c] for f in filas) / len(filas):.2f}%")
    log("  listones: bo64 clones 12.76; R&R ciego (PPO, d completo) "
        "13.73; bo64 PPO 13.86; experto TS ~3.66")


if __name__ == "__main__":
    main()
