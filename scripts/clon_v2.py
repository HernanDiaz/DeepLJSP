# -*- coding: utf-8 -*-
"""Clon v2: imitacion de TSN2 con warm start y dataset mixto.

Implementa el diseño de RESEARCH_IMITACION.md (2026-08-10), que ataca
los dos fallos medidos en los pilotos:

  v0 (auto-clon):  profesor incoherente  -> se cambia el experto a TSN2
  v1 (clon TS):    covariate shift       -> warm start + dataset mixto

Dataset 50/25/25:
  A) replay puro de las soluciones TSN2                    (la autopista)
  B) replay con PREFIJO CORROMPIDO: k decisiones al azar y
     luego el RESTO del orden experto, etiquetando solo lo
     posterior al desvio                            (volver al carril)
  C) estados de rollouts propios etiquetados por auto-
     seleccion: N muestras de la politica actual, se
     conserva la mejor bajo la Eq. (3) y se replaya  (la distribucion
                                                     de despliegue)

(B) es factible sin proyeccion porque en la codificacion de
permutacion con repeticion, si el prefijo ya ejecuto c_j operaciones
del trabajo j, el resto valido del orden experto es su secuencia sin
las primeras c_j apariciones de j: sigue respetando las precedencias.

Validacion por SECUENCIAS enteras (no por decisiones sueltas, que
serian casi duplicados). Varias semillas de clon.

Salida NUEVA: benchmarks/clon_v2/. No toca nada existente.

    python scripts/clon_v2.py                  # 3 semillas, por defecto
    python scripts/clon_v2.py --seeds 1 --epocas 10   # prueba rapida
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
# warm start rotatorio: el clon `sem` parte del checkpoint desplegado
# seed(sem+1); tres puntos de partida reales, mejora pareada por maestro
WARM = {1: "models/v2_final_deepsets_1000ep_seed2.pt",
        2: "models/v2_final_deepsets_1000ep_seed3.pt",
        3: "models/v2_final_deepsets_1000ep_seed4.pt"}
M = 15                       # maquinas de la clase 20x15
RUNS_TRAIN, RUNS_VAL = 24, 6         # split por secuencias, de las 30
N_CORRUPTAS = 24             # secuencias con prefijo corrompido por instancia
N_AUTOSEL = 64               # muestras por auto-seleccion (fase C)
TOP_AUTOSEL = 8              # cuantas de esas se replayan
N_BO = 64
N_BO_SEL = 16          # presupuesto barato para elegir epoca
SALIDA = "benchmarks/clon_v2"


# ----------------------------------------------------------------- datos
def lee_ts(pid):
    corto = pid.replace("int__", "")
    f = glob.glob(f"{TS_DIR}/*{corto}*_Sols.csv")
    assert f, f"sin fichero TS para {pid}"
    out = []
    for fila in list(csv.reader(open(f[0], encoding="utf-8",
                                     errors="replace"),
                                delimiter=";"))[1:]:
        jobs = [int(x) // M + 1 for x in fila[1].split()]
        lo, up = eval(fila[2])
        out.append((jobs, (lo + up) / 2))
    return out


def resto_experto(seq, hechas):
    """Orden experto restante tras haber ejecutado `hechas` (Counter de
    trabajos). Quita las primeras c_j apariciones de cada trabajo j."""
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


def replay(env, enc, seq, desde=0):
    """Reproduce `seq` y devuelve (muestras desde el paso `desde`, mid).
    None si la secuencia es inconsistente con el entorno."""
    state = env.reset()
    muestras = []
    for t, job in enumerate(seq):
        eleg = state["eligible_ops"]
        if not eleg:
            break
        try:
            a = eleg.index(job - 1)
        except ValueError:
            return None
        if t >= desde and len(eleg) > 1:
            op, gl = enc.encode(state)
            muestras.append((op.astype(np.float32), gl.astype(np.float32),
                             a))
        state, done = _paso(env, state, a)
    mk = final_makespan(env.job_completion_time)
    return muestras, (float(mk.lower) + float(mk.upper)) / 2


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


def construye_dataset(red, rng, sem, log):
    """(train, val) como listas de (op, gl, accion)."""
    train, val = [], []
    for pid in TRAIN:
        env = EnvironmentFactory.create_from_problem_id(pid, "adaptive",
                                                        seed=1)
        enc = AgentV2(env, seed=1, attention_layers=0).encoder
        sols = lee_ts(pid)
        idx = rng.permutation(len(sols))
        tr = [sols[i] for i in idx[:RUNS_TRAIN]]
        va = [sols[i] for i in idx[RUNS_TRAIN:RUNS_TRAIN + RUNS_VAL]]

        # (A) replay puro
        na = 0
        for seq, _ in tr:
            r = replay(env, enc, seq)
            if r:
                train.extend(r[0])
                na += len(r[0])
        for seq, _ in va:
            r = replay(env, enc, seq)
            if r:
                val.extend(r[0])

        # (B) prefijo corrompido: k ~ U[5,60] decisiones al azar en el
        # MISMO entorno que luego etiqueta (nada de reconstruir el
        # prefijo en otro: en semiactivo el ORDEN de despacho fija las
        # secuencias de maquina, y una reconstruccion canonica
        # colapsaria corrupciones distintas al mismo estado)
        nb = 0
        for _ in range(N_CORRUPTAS):
            seq, _ = tr[int(rng.integers(len(tr)))]
            k = int(rng.integers(5, 61))
            state = env.reset()
            hechas = Counter()
            for _ in range(k):
                eleg = state["eligible_ops"]
                if not eleg:
                    break
                a = int(rng.integers(len(eleg)))
                hechas[eleg[a] + 1] += 1
                state, done = _paso(env, state, a)
                if done:
                    break
            for job in resto_experto(seq, hechas):
                eleg = state["eligible_ops"]
                if not eleg:
                    break
                try:
                    a = eleg.index(job - 1)
                except ValueError:
                    break
                if len(eleg) > 1:
                    op, gl = enc.encode(state)
                    train.append((op.astype(np.float32),
                                  gl.astype(np.float32), a))
                    nb += 1
                state, done = _paso(env, state, a)

        # (C) auto-seleccion sobre la distribucion propia: de N muestras
        # se replayan las TOP_AUTOSEL mejores bajo la Eq. (3). Una sola
        # aportaba el 2% del dataset; ocho lo dejan en el ~15% sin caer
        # en el error de la v0, donde el experto ERAN colas afortunadas
        cand = []
        for i in range(N_AUTOSEL):
            (mid, up, lo), seq = rollout(env, red, enc, i > 0,
                                         5000 + 1000 * sem + i,
                                         devolver_seq=True)
            cand.append(((up, lo), seq))
        cand.sort(key=lambda t: t[0])
        nc = 0
        for _, seq in cand[:TOP_AUTOSEL]:
            r = replay(env, enc, seq)
            if r:
                train.extend(r[0])
                nc += len(r[0])
        log(f"  {pid}: A={na} B={nb} C={nc} decisiones")
    return train, val


# ------------------------------------------------------------ entreno
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


def evalua_ce(red, datos, lote=512):
    tot, ac, n = 0.0, 0, 0
    with torch.no_grad():
        for i in range(0, len(datos), lote):
            ops, gls, mask, y = lote_tensor(datos[i:i + lote])
            logits, _ = red(ops, gls, mask)
            tot += float(F.cross_entropy(logits, y, reduction="sum"))
            ac += int((logits.argmax(1) == y).sum())
            n += len(y)
    return tot / n, ac / n


def re_pct(mid, pid):
    lb = lb_for_problem_name(pid)
    return (mid - lb) / lb * 100


def evalua_dev(red, n_bo=N_BO):
    g, b = [], []
    for pid in DEV:
        env = EnvironmentFactory.create_from_problem_id(pid, "adaptive",
                                                        seed=1)
        enc = AgentV2(env, seed=1, attention_layers=0).encoder
        g.append(re_pct(rollout(env, red, enc, False, 0)[0], pid))
        mejor, clave = None, None
        for i in range(n_bo):
            mid, up, lo = rollout(env, red, enc, i > 0, 1000 + i)
            if clave is None or (up, lo) < clave:
                mejor, clave = mid, (up, lo)
        b.append(re_pct(mejor, pid))
    return sum(g) / len(g), sum(b) / len(b)


def una_semilla(sem, epocas, lr, ent_coef, kl_coef, log):
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
    g0, b0f = evalua_dev(red)
    _, b0 = evalua_dev(red, N_BO_SEL)
    log(f"[semilla {sem}] antes de imitar: greedy {g0:.2f}% "
        f"bo{N_BO} {b0f:.2f}% bo{N_BO_SEL} {b0:.2f}%")

    t0 = time.time()
    train, val = construye_dataset(red, rng, sem, log)
    log(f"[semilla {sem}] dataset: {len(train)} train / {len(val)} val "
        f"({time.time() - t0:.0f} s)")

    # El humo mostro el riesgo: una epoca de CE pura a lr de
    # entrenamiento ya hundia el best-of-N (13.90 -> 17.80). La CE
    # empuja hacia imitacion determinista y colapsa la entropia que el
    # muestreo explota. Tres correcciones: lr de ajuste fino, premio de
    # entropia, y seleccion de epoca por la METRICA DE DESPLIEGUE
    # (best-of-16 en desarrollo) en vez de por la CE de validacion, que
    # mide fidelidad al experto y no calidad de la distribucion.
    opt = torch.optim.Adam(red.parameters(), lr=lr)
    idx = np.arange(len(train))
    mejor_bo, mejor_estado, sin_mejora = b0, None, 0
    log(f"  [linea base a batir: bo{N_BO_SEL}={b0:.2f}]")
    for ep in range(epocas):
        rng.shuffle(idx)
        red.train()
        ent_media, n_lotes = 0.0, 0
        for ini in range(0, len(idx), 256):
            ops, gls, mask, y = lote_tensor([train[i]
                                             for i in idx[ini:ini + 256]])
            logits, _ = red(ops, gls, mask)
            logp = F.log_softmax(logits.masked_fill(~mask, -1e9), dim=1)
            ent = -(logp.exp() * logp).masked_fill(~mask, 0.0).sum(1).mean()
            # ancla: KL(p0 || p) contra la politica del warm start; le
            # impide anular acciones que la original valoraba, que es
            # exactamente lo que el humo vio morir (bo16 -> greedy en
            # una epoca)
            with torch.no_grad():
                logits0, _ = red0(ops, gls, mask)
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
        ce_t, ac_t = evalua_ce(red, train[:4000])
        ce_v, ac_v = evalua_ce(red, val)
        g_e, b_e = evalua_dev(red, N_BO_SEL)
        marca = ""
        if b_e < mejor_bo:
            mejor_bo, sin_mejora = b_e, 0
            mejor_estado = {k: v.clone() for k, v in red.state_dict().items()}
            marca = " *"
        else:
            sin_mejora += 1
        log(f"  ep {ep:>3}: train CE={ce_t:.4f} ac={ac_t:.3f} "
            f"H={ent_media / max(n_lotes, 1):.3f} | "
            f"val CE={ce_v:.4f} ac={ac_v:.3f} | dev greedy={g_e:.2f} "
            f"bo{N_BO_SEL}={b_e:.2f}{marca}")
        if sin_mejora >= 4:
            log(f"  parada temprana en la epoca {ep}")
            break
    if mejor_estado:
        red.load_state_dict(mejor_estado)
    else:
        red.load_state_dict(torch.load(warm, map_location="cpu",
                                       weights_only=True)["network"])
        log("  ninguna epoca mejoro la linea base: RESTAURADO el "
            "warm start")
    g1, b1 = evalua_dev(red)
    log(f"[semilla {sem}] DESPUES: greedy {g1:.2f}% bo{N_BO} {b1:.2f}%")
    torch.save({"network": red.state_dict()},
               os.path.join(SALIDA, f"clon_v2_seed{sem}.pt"))
    return {"semilla": sem, "greedy_antes": g0, "bo64_antes": b0f,
            "greedy_despues": g1, "bo64_despues": b1,
            "mejor_bo_sel": mejor_bo, "n_train": len(train), "n_val": len(val)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--epocas", type=int, default=30)
    ap.add_argument("--lr", type=float, default=5e-5)
    ap.add_argument("--ent", type=float, default=0.01)
    ap.add_argument("--kl", type=float, default=0.5)
    args = ap.parse_args()
    os.makedirs(SALIDA, exist_ok=True)
    reg = open(os.path.join(SALIDA, "log.txt"), "a", encoding="utf-8")

    def log(m):
        print(m, flush=True)
        reg.write(m + "\n")
        reg.flush()

    log(f"\n=== clon v2 ({args.seeds} semillas, {args.epocas} epocas, "
        f"lr={args.lr}, ent={args.ent}, kl={args.kl}) ===")
    filas = []
    for sem in range(1, args.seeds + 1):
        filas.append(una_semilla(sem, args.epocas, args.lr, args.ent, args.kl, log))
    with open(os.path.join(SALIDA, "resultados.csv"), "w",
              encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    log("\n=== RESUMEN ===")
    for c in ("greedy_antes", "greedy_despues", "bo64_antes",
              "bo64_despues"):
        log(f"  {c:>16}: {sum(f[c] for f in filas) / len(filas):.2f}%")
    log("  referencias: politica RL greedy 18.25 / bo64 13.4; "
        "clon v0 bo64 13.94; clon v1-TS bo64 20.42; experto TS ~3.6")


if __name__ == "__main__":
    main()
