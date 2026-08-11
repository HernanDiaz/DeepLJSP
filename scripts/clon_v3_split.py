# -*- coding: utf-8 -*-
"""Clon v3-split: el experimento de atribucion seleccion vs mejora.

Los tests limpios (DMU y Taillard sinteticas) mostraron que la
"mejora" de la v3 (-1.10, 3/3) no sobrevive fuera de las seis
instancias que ELIGIERON las rondas: sesgo de seleccion del tamaño
exacto que predice el minimo de ~8 rondas ruidosas (sd ~0.7).

Este experimento repite el bucle v3 con la unica correccion que
importa: SELECCION y REPORTE separados.

  SEL  = TA15-17            elige la mejor ronda (bo64)
  REP  = TA18-20 + sint01-10  solo se mide; jamas decide nada

Ambas curvas se registran por ronda. Si la ganancia reaparece en REP,
la auto-mejora es real con protocolo corregido; si solo aparece en
SEL, la atribucion queda demostrada experimentalmente.

Salida NUEVA: benchmarks/clon_v3_split/. No toca nada existente.
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
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.models.interval import final_makespan          # noqa: E402

TRAIN = [f"int__tai20_15_{i:02d}" for i in range(1, 5)]      # TA11-14
SEL = [f"int__tai20_15_{i:02d}" for i in range(5, 8)]        # TA15-17
REP = ([f"int__tai20_15_{i:02d}" for i in range(8, 11)]      # TA18-20
       + [f"int__sint20_15_{k:02d}" for k in range(1, 11)])  # sinteticas
WARM = {1: "models/v2_final_deepsets_1000ep_seed2.pt",
        2: "models/v2_final_deepsets_1000ep_seed3.pt",
        3: "models/v2_final_deepsets_1000ep_seed4.pt"}
N_BO = 64
SALIDA = "benchmarks/clon_v3_split"


def _paso(env, state, a):
    state, _, done, _ = env.step(a)
    return state, done


def replay(env, enc, seq):
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
            muestras.append((op.astype(np.float32),
                             gl.astype(np.float32), a))
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


def bo64_mid(red, pid):
    """best-of-64 (mid del mejor bajo la clave lex) con semillas fijas."""
    env = EnvironmentFactory.create_from_problem_id(pid, "adaptive",
                                                    seed=1)
    enc = AgentV2(env, seed=1, attention_layers=0).encoder
    mejor, clave = None, None
    for i in range(N_BO):
        mid, up, lo = rollout(env, red, enc, i > 0, 1000 + i)
        if clave is None or (up, lo) < clave:
            mejor, clave = mid, (up, lo)
    return mejor


def evalua(red, pids):
    """Media del bo64 mid NORMALIZADO por instancia: mid / mid_warm.
    Se fija la referencia warm en la primera llamada por semilla."""
    return {pid: bo64_mid(red, pid) for pid in pids}


def muestrea_ronda(red, sem, ronda, n, top, elite, log):
    train, sel_re = [], []
    for pid in TRAIN:
        env = EnvironmentFactory.create_from_problem_id(pid, "adaptive",
                                                        seed=1)
        enc = AgentV2(env, seed=1, attention_layers=0).encoder
        cand = []
        for i in range(n):
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
        for _, mid, seq in escogidas:
            r = replay(env, enc, seq)
            if r:
                train.extend(r)
            sel_re.append(mid)
    return train


def una_semilla(sem, rondas, epocas, n, top, lr, ent_coef, kl_coef,
                paciencia, log):
    torch.manual_seed(sem)
    rng = np.random.default_rng(sem)
    red = PolicyValueNetV2()
    warm = WARM[(sem - 1) % 3 + 1]
    red.load_state_dict(torch.load(warm, map_location="cpu",
                                   weights_only=True)["network"])
    log(f"[semilla {sem}] warm start desde {os.path.basename(warm)}")
    t0 = time.time()
    base_sel = evalua(red, SEL)
    base_rep = evalua(red, REP)
    log(f"[semilla {sem}] linea base medida ({time.time() - t0:.0f} s)")

    def indice(vals, base):
        """media del ratio mid/mid_base x100 (100 = warm start)."""
        return 100 * sum(vals[p] / base[p] for p in vals) / len(vals)

    opt = torch.optim.Adam(red.parameters(), lr=lr)
    elite = {}
    mejor_sel, mejor_estado, mejor_ronda, sin_mejora = 100.0, None, -1, 0
    curva = []
    for ronda in range(rondas):
        t0 = time.time()
        red.eval()
        train = muestrea_ronda(red, sem, ronda, n, top, elite, log)
        ref = PolicyValueNetV2()
        ref.load_state_dict(red.state_dict())
        ref.eval()
        for q in ref.parameters():
            q.requires_grad_(False)
        idx = np.arange(len(train))
        red.train()
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
                    logits0, _ = ref(ops, gls, mask)
                    logp0 = F.log_softmax(
                        logits0.masked_fill(~mask, -1e9), dim=1)
                kl = (logp0.exp() * (logp0 - logp)).masked_fill(
                    ~mask, 0.0).sum(1).mean()
                perdida = (F.cross_entropy(logits, y) - ent_coef * ent
                           + kl_coef * kl)
                opt.zero_grad()
                perdida.backward()
                opt.step()
        red.eval()
        i_sel = indice(evalua(red, SEL), base_sel)
        i_rep = indice(evalua(red, REP), base_rep)
        marca = ""
        if i_sel < mejor_sel:
            mejor_sel, sin_mejora, mejor_ronda = i_sel, 0, ronda
            mejor_estado = {k: v.clone()
                            for k, v in red.state_dict().items()}
            marca = " *"
        else:
            sin_mejora += 1
        curva.append({"semilla": sem, "ronda": ronda,
                      "indice_sel": i_sel, "indice_rep": i_rep})
        log(f"  ronda {ronda:>2}: SEL={i_sel:.2f} REP={i_rep:.2f}"
            f"{marca} ({time.time() - t0:.0f} s)")
        if sin_mejora >= paciencia:
            log(f"  parada temprana en la ronda {ronda}")
            break
    if mejor_estado:
        red.load_state_dict(mejor_estado)
    else:
        red.load_state_dict(torch.load(warm, map_location="cpu",
                                       weights_only=True)["network"])
        log("  ninguna ronda mejoro SEL: RESTAURADO el warm start")
    fin_sel = indice(evalua(red, SEL), base_sel)
    fin_rep = indice(evalua(red, REP), base_rep)
    log(f"[semilla {sem}] DESPUES (ronda {mejor_ronda}): "
        f"SEL={fin_sel:.2f} REP={fin_rep:.2f}  (100 = warm start)")
    torch.save({"network": red.state_dict()},
               os.path.join(SALIDA, f"clon_v3split_seed{sem}.pt"))
    return ({"semilla": sem, "ronda_elegida": mejor_ronda,
             "sel_final": fin_sel, "rep_final": fin_rep}, curva)


def main():
    global SALIDA
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
    ap.add_argument("--salida", type=str, default=SALIDA)
    args = ap.parse_args()
    SALIDA = args.salida
    os.makedirs(SALIDA, exist_ok=True)
    reg = open(os.path.join(SALIDA, "log.txt"), "a", encoding="utf-8")

    def log(m):
        print(m, flush=True)
        reg.write(m + "\n")
        reg.flush()

    log(f"\n=== clon v3-split ({args.seeds} semillas, {args.rondas} "
        f"rondas, sel=TA15-17, rep=TA18-20+sint01-10, salida={SALIDA}) "
        f"===")
    filas, curvas = [], []
    for sem in range(1, args.seeds + 1):
        fila, curva = una_semilla(sem, args.rondas, args.epocas, args.n,
                                  args.top, args.lr, args.ent, args.kl,
                                  args.paciencia, log)
        filas.append(fila)
        curvas.extend(curva)
    for nombre, datos in (("resultados.csv", filas),
                          ("curvas.csv", curvas)):
        with open(os.path.join(SALIDA, nombre), "w", encoding="utf-8",
                  newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(datos[0]))
            w.writeheader()
            w.writerows(datos)
    log("\n=== RESUMEN (indice bo64, 100 = warm start) ===")
    for c in ("sel_final", "rep_final"):
        log(f"  {c}: {sum(f[c] for f in filas) / len(filas):.2f}")
    log("  atribucion: si SEL<100 y REP~100, la ganancia es seleccion; "
        "si ambos <100, la auto-mejora es real")


if __name__ == "__main__":
    main()
