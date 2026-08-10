# -*- coding: utf-8 -*-
"""Clon v3: bucle de auto-mejora (estilo SLIM, Corsini et al. 2024).

Diagnostico de la v2 que motiva este diseño: la CE hacia un experto
EXTERNO (TSN2) afila el argmax pero mueve la masa de probabilidad fuera
de la region que el best-of-N explota, aun con la entropia intacta. El
valor de la distribucion RL no es su entropia sino DONDE pone la masa.

El bucle ataca eso directamente: las etiquetas salen siempre de la
PROPIA distribucion (sin covariate shift ni masa ajena), y mejoran
ronda a ronda:

  ronda r:  muestrear N rollouts por instancia con la politica actual
            -> conservar las TOP_K mejores bajo la Eq. (3)  (+ la elite
               historica de la instancia, un trinquete que impide
               regresion de las etiquetas)
            -> replay a (estado, accion) y unas pocas epocas de CE
            -> evaluar en desarrollo; seleccion de ronda por bo16

Guardas heredadas de la v2: warm start rotatorio desde los checkpoints
PPO desplegados, ancla KL (aqui contra la politica al INICIO de cada
ronda, no contra el warm start: region de confianza que permite deriva
acumulada pero controla el colapso por ronda), premio de entropia,
seleccion por la metrica de despliegue y restauracion del warm start si
ninguna ronda mejora la linea base.

La ronda 0 sin iterar es exactamente la v0 (destilacion one-shot, que
empataba con PPO: bo64 13.94 vs 13.4). La apuesta medible es que
iterar con re-muestreo fresco supere el 13.4.

Salida NUEVA: benchmarks/clon_v3/. No toca nada existente.

    python scripts/clon_v3.py                     # 3 semillas, defecto
    python scripts/clon_v3.py --seeds 1 --rondas 2 --n 16 --top 2 \
                              --epocas 1          # humo
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
import torch.nn.functional as F                                # noqa: E402
torch.set_num_threads(2)

from jobshop_rl.agents_v2 import AgentV2                       # noqa: E402
from jobshop_rl.agents_v2.networks import PolicyValueNetV2     # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.models.interval import final_makespan          # noqa: E402

TRAIN = [f"int__tai20_15_{i:02d}" for i in range(1, 5)]      # TA11-14
DEV = [f"int__tai20_15_{i:02d}" for i in range(5, 11)]       # TA15-20
WARM = {1: "models/v2_final_deepsets_1000ep_seed2.pt",
        2: "models/v2_final_deepsets_1000ep_seed3.pt",
        3: "models/v2_final_deepsets_1000ep_seed4.pt"}
N_BO = 64
N_BO_SEL = 16          # presupuesto barato para elegir ronda
SALIDA = "benchmarks/clon_v3"


def _paso(env, state, a):
    state, _, done, _ = env.step(a)
    return state, done


def replay(env, enc, seq):
    """Reproduce `seq` (trabajos 1-based) y devuelve las muestras
    (op, gl, accion) de los estados con mas de una opcion."""
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
        if len(eleg) > 1:
            op, gl = enc.encode(state)
            muestras.append((op.astype(np.float32), gl.astype(np.float32),
                             a))
        state, done = _paso(env, state, a)
    return muestras


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


def re_pct(mid, pid):
    lb = lb_for_problem_name(pid)
    return (mid - lb) / lb * 100


def evalua_dev(red, n_bo=N_BO):
    """Una sola pasada de n_bo muestras por instancia; devuelve
    (greedy, best-of-16, best-of-n_bo).

    El best-of-16 sale del PREFIJO de las mismas semillas, asi que las
    dos curvas son el mismo experimento a dos presupuestos y cuestan
    una sola evaluacion. El humo dejo claro por que hacen falta las
    dos: la ronda que mejoraba a 16 muestras empeoraba a 64 (15.10
    frente a 14.24), de modo que elegir por el presupuesto barato
    optimiza un proxy sesgado del despliegue."""
    g, b16, b64 = [], [], []
    for pid in DEV:
        env = EnvironmentFactory.create_from_problem_id(pid, "adaptive",
                                                        seed=1)
        enc = AgentV2(env, seed=1, attention_layers=0).encoder
        g.append(re_pct(rollout(env, red, enc, False, 0)[0], pid))
        mejor, clave = None, None
        m16, c16 = None, None
        for i in range(n_bo):
            mid, up, lo = rollout(env, red, enc, i > 0, 1000 + i)
            if clave is None or (up, lo) < clave:
                mejor, clave = mid, (up, lo)
            if i == N_BO_SEL - 1:
                m16, c16 = mejor, clave
        b16.append(re_pct(m16 if m16 is not None else mejor, pid))
        b64.append(re_pct(mejor, pid))
    n = len(DEV)
    return sum(g) / n, sum(b16) / n, sum(b64) / n


def muestrea_ronda(red, sem, ronda, n, top, elite, log):
    """Etiquetas de la ronda: TOP mejores de n muestras frescas por
    instancia de entrenamiento, mas la elite historica. Actualiza la
    elite in situ y devuelve (dataset, RE media de lo seleccionado)."""
    train, sel_re = [], []
    for pid in TRAIN:
        env = EnvironmentFactory.create_from_problem_id(pid, "adaptive",
                                                        seed=1)
        enc = AgentV2(env, seed=1, attention_layers=0).encoder
        cand = []
        for i in range(n):
            # i=0 es el argmax; el resto muestrea con semilla propia por
            # (semilla, ronda, muestra) para que cada ronda vea colas
            # frescas de la distribucion ya desplazada
            (mid, up, lo), seq = rollout(
                env, red, enc, i > 0,
                100000 * sem + 1000 * ronda + i, devolver_seq=True)
            cand.append(((up, lo), mid, seq))
        cand.sort(key=lambda t: t[0])
        if elite.get(pid) is None or cand[0][0] < elite[pid][0]:
            elite[pid] = (cand[0][0], cand[0][1], cand[0][2])
        escogidas = cand[:top]
        claves = {tuple(s) for _, _, s in escogidas}
        if tuple(elite[pid][2]) not in claves:
            escogidas = escogidas[:top - 1] + [elite[pid]]
        nd = 0
        for _, mid, seq in escogidas:
            r = replay(env, enc, seq)
            if r:
                train.extend(r)
                nd += len(r)
            sel_re.append(re_pct(mid, pid))
        log(f"    {pid}: mejor {re_pct(cand[0][1], pid):.2f}% "
            f"elite {re_pct(elite[pid][1], pid):.2f}% "
            f"({nd} decisiones)")
    return train, sum(sel_re) / len(sel_re)


def una_semilla(sem, rondas, epocas, n, top, lr, ent_coef, kl_coef,
                paciencia, log):
    torch.manual_seed(sem)
    rng = np.random.default_rng(sem)
    red = PolicyValueNetV2()
    warm = WARM[(sem - 1) % 3 + 1]
    red.load_state_dict(torch.load(warm, map_location="cpu",
                                   weights_only=True)["network"])
    log(f"[semilla {sem}] warm start desde {os.path.basename(warm)}")
    g0, b16_0, b0 = evalua_dev(red)
    log(f"[semilla {sem}] antes: greedy {g0:.2f}% bo{N_BO_SEL} "
        f"{b16_0:.2f}% bo{N_BO} {b0:.2f}%")

    opt = torch.optim.Adam(red.parameters(), lr=lr)
    elite = {}
    mejor_bo, mejor_estado, sin_mejora = b0, None, 0
    log(f"  [linea base a batir: bo{N_BO}={b0:.2f}]")
    for ronda in range(rondas):
        t0 = time.time()
        red.eval()
        train, re_sel = muestrea_ronda(red, sem, ronda, n, top, elite, log)
        # region de confianza de la ronda: el ancla KL apunta a la
        # politica con la que se muestreo ESTA ronda, no al warm start;
        # la deriva acumulada queda libre, el colapso por ronda no
        ref = PolicyValueNetV2()
        ref.load_state_dict(red.state_dict())
        ref.eval()
        for q in ref.parameters():
            q.requires_grad_(False)
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
                ent = -(logp.exp() * logp).masked_fill(~mask,
                                                       0.0).sum(1).mean()
                with torch.no_grad():
                    logits0, _ = ref(ops, gls, mask)
                    logp0 = F.log_softmax(logits0.masked_fill(~mask, -1e9),
                                          dim=1)
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
        g_r, b16_r, b_r = evalua_dev(red)
        marca = ""
        if b_r < mejor_bo:
            mejor_bo, sin_mejora = b_r, 0
            mejor_estado = {k: v.clone()
                            for k, v in red.state_dict().items()}
            marca = " *"
        else:
            sin_mejora += 1
        log(f"  ronda {ronda:>2}: sel RE={re_sel:.2f}% "
            f"({len(train)} dec.) H={ent_media / max(n_lotes, 1):.3f} | "
            f"dev greedy={g_r:.2f} bo{N_BO_SEL}={b16_r:.2f} "
            f"bo{N_BO}={b_r:.2f}{marca} ({time.time() - t0:.0f} s)")
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
    g1, b16_1, b1 = evalua_dev(red)
    log(f"[semilla {sem}] DESPUES: greedy {g1:.2f}% bo{N_BO_SEL} "
        f"{b16_1:.2f}% bo{N_BO} {b1:.2f}%")
    torch.save({"network": red.state_dict()},
               os.path.join(SALIDA, f"clon_v3_seed{sem}.pt"))
    elite_re = sum(re_pct(m, p) for p, (_, m, _) in elite.items()) / len(elite)
    return {"semilla": sem, "greedy_antes": g0, "bo16_antes": b16_0,
            "bo64_antes": b0, "greedy_despues": g1, "bo16_despues": b16_1,
            "bo64_despues": b1, "elite_re_train": elite_re}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--rondas", type=int, default=10)
    ap.add_argument("--epocas", type=int, default=3)
    ap.add_argument("--n", type=int, default=64)
    ap.add_argument("--top", type=int, default=4)
    ap.add_argument("--lr", type=float, default=5e-5)
    ap.add_argument("--ent", type=float, default=0.01)
    ap.add_argument("--kl", type=float, default=0.5)
    ap.add_argument("--paciencia", type=int, default=4)
    args = ap.parse_args()
    os.makedirs(SALIDA, exist_ok=True)
    reg = open(os.path.join(SALIDA, "log.txt"), "a", encoding="utf-8")

    def log(m):
        print(m, flush=True)
        reg.write(m + "\n")
        reg.flush()

    log(f"\n=== clon v3 ({args.seeds} semillas, {args.rondas} rondas x "
        f"{args.epocas} epocas, n={args.n}, top={args.top}, lr={args.lr}, "
        f"ent={args.ent}, kl={args.kl}, paciencia={args.paciencia}) ===")
    filas = []
    for sem in range(1, args.seeds + 1):
        filas.append(una_semilla(sem, args.rondas, args.epocas, args.n,
                                 args.top, args.lr, args.ent, args.kl,
                                 args.paciencia, log))
    with open(os.path.join(SALIDA, "resultados.csv"), "w",
              encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    log("\n=== RESUMEN ===")
    for c in ("greedy_antes", "greedy_despues", "bo16_antes",
              "bo16_despues", "bo64_antes", "bo64_despues",
              "elite_re_train"):
        log(f"  {c:>16}: {sum(f[c] for f in filas) / len(filas):.2f}%")
    log("  referencias: politica RL greedy 18.25 / bo64 13.4; "
        "clon v0 bo64 13.94; clon v2 nulo protegido; experto TS ~3.6")


if __name__ == "__main__":
    main()
