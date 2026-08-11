# -*- coding: utf-8 -*-
"""Clon v5.3: auto-imitacion sobre REPARACIONES propias aceptadas.

Las v5.0/5.1/5.2 dejaron un hecho triple: la CE hacia completaciones
EXPERTAS daña el despliegue en la primera epoca a cualquier lr, ancla
y curriculo probados — el conflicto esta en las etiquetas ajenas, no
en el orden de presentacion. La v3 dejo el hecho espejo: las
etiquetas PROPIAS seleccionadas mejoran el despliegue 3/3.

La v5.3 aplica la receta de la v3 a los estados de reparacion: el
arnes ruin & recreate genera reconstrucciones y ACEPTA las que
mejoran el incumbente bajo la Eq. (3); esas reconstrucciones
aceptadas — estados y acciones muestreados por la propia politica —
son las etiquetas. On-distribution por construccion. El incumbente
por instancia PERSISTE entre rondas (trinquete, como la elite v3).

Guardas: warm start desde los clones v3, ancla KL 0.5 contra el warm
start, premio de entropia, seleccion de ronda por la reparacion en
desarrollo (arnes v4, semillas fijas), restauracion si nada mejora.

Exito prerregistrado: reparacion dev < 12.76 (bo64 clones) y
< 13.73/13.89 (reparacion ciega).

Salida NUEVA: benchmarks/clon_v5p3/. No toca nada existente.

    python scripts/clon_v5_selfrepair.py                # 3 semillas
    python scripts/clon_v5_selfrepair.py --seeds 1 --rondas 2 \
        --iteraciones 8 --presupuesto-eval 24           # humo
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
WARM = {1: "benchmarks/clon_v3/clon_v3_seed1.pt",
        2: "benchmarks/clon_v3/clon_v3_seed2.pt",
        3: "benchmarks/clon_v3/clon_v3_seed3.pt"}
DMIN = 15
SALIDA = "benchmarks/clon_v5p3"


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


def reparaciones_propias(red, pid, inc, sem, ronda, n_iter, rng, log):
    """n_iter iteraciones de R&R sobre el incumbente persistente.
    Devuelve (muestras de las reconstrucciones ACEPTADAS, incumbente
    actualizado, aceptadas)."""
    env = EnvironmentFactory.create_from_problem_id(pid, "adaptive",
                                                    seed=1)
    enc = AgentV2(env, seed=1, attention_layers=0).encoder
    if inc is None:
        (mid, up, lo), seq = rollout(env, red, enc, False, 0,
                                     devolver_seq=True)
        inc = {"clave": (up, lo), "mid": mid, "seq": seq}
    T = len(inc["seq"])
    out, acept = [], 0
    for it in range(n_iter):
        d = int(rng.integers(DMIN, T))
        prefijo = inc["seq"][:T - d]
        torch.manual_seed(600000 * sem + 3000 * ronda + it)
        state = env.reset()
        seq2, cand = [], []
        for job in prefijo:
            a = state["eligible_ops"].index(job - 1)
            seq2.append(job)
            state, done = _paso(env, state, a)
        while state["eligible_ops"]:
            op, gl = enc.encode(state)
            with torch.no_grad():
                logits, _ = red(
                    torch.tensor(op[None], dtype=torch.float32),
                    torch.tensor(gl[None], dtype=torch.float32))
            lg = logits[0, :len(state["eligible_ops"])]
            a = int(torch.distributions.Categorical(logits=lg).sample())
            if len(state["eligible_ops"]) > 1:
                cand.append((op.astype(np.float32),
                             gl.astype(np.float32), a))
            seq2.append(state["eligible_ops"][a] + 1)
            state, done = _paso(env, state, a)
            if done:
                break
        mk = final_makespan(env.job_completion_time)
        clave = (float(mk.upper), float(mk.lower))
        if clave < inc["clave"]:
            inc = {"clave": clave,
                   "mid": (float(mk.lower) + float(mk.upper)) / 2,
                   "seq": seq2}
            out.extend(cand)
            acept += 1
    log(f"    {pid}: {acept}/{n_iter} aceptadas, {len(out)} decisiones "
        f"(incumbente {re_pct(inc['mid'], pid):.2f}%)")
    return out, inc, acept


def eval_reparacion(red, presupuesto, dmax=299):
    """Identica a la v5: greedy + R&R a presupuesto*T con semillas
    fijas; bo16 como control de construccion fuera del presupuesto."""
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
        mejor, clave = mid, inc_clave
        for i in range(1, 16):
            c_mid, c_up, c_lo = rollout(env, red, enc, True, 1000 + i)
            if (c_up, c_lo) < clave:
                mejor, clave = c_mid, (c_up, c_lo)
        bo16.append(re_pct(mejor, pid))
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


def una_semilla(sem, rondas, epocas, n_iter, lr, ent_coef, kl_coef,
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

    opt = torch.optim.Adam(red.parameters(), lr=lr)
    incumbentes = {pid: None for pid in TRAIN}
    mejor_rep, mejor_estado, sin_mejora = rep0, None, 0
    log(f"  [linea base a batir: reparacion={rep0:.2f}; listones "
        f"prerregistrados: 12.76 y 13.73/13.89]")
    for ronda in range(rondas):
        t0 = time.time()
        red.eval()
        train, acept_tot = [], 0
        for pid in TRAIN:
            m, incumbentes[pid], ac = reparaciones_propias(
                red, pid, incumbentes[pid], sem, ronda, n_iter, rng, log)
            train.extend(m)
            acept_tot += ac
        if not train:
            log(f"  ronda {ronda:>2}: sin aceptaciones, sin "
                f"entrenamiento ({time.time() - t0:.0f} s)")
            sin_mejora += 1
            if sin_mejora >= paciencia:
                log(f"  parada temprana en la ronda {ronda}")
                break
            continue
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
        log(f"  ronda {ronda:>2}: {acept_tot} acept. {len(train)} dec. "
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
               os.path.join(SALIDA, f"clon_v5p3_seed{sem}.pt"))
    return {"semilla": sem, "rep_antes": rep0, "bo16_antes": bo16_0,
            "rep_despues": rep1, "bo16_despues": bo16_1}


def main():
    global SALIDA
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--rondas", type=int, default=12)
    ap.add_argument("--epocas", type=int, default=3)
    ap.add_argument("--iteraciones", type=int, default=48)
    ap.add_argument("--lr", type=float, default=5e-5)
    ap.add_argument("--ent", type=float, default=0.01)
    ap.add_argument("--kl", type=float, default=0.5)
    ap.add_argument("--paciencia", type=int, default=6)
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

    log(f"\n=== clon v5.3 self-repair ({args.seeds} semillas, "
        f"{args.rondas} rondas x {args.epocas} epocas, "
        f"iter={args.iteraciones}, lr={args.lr}, ent={args.ent}, "
        f"kl={args.kl}, paciencia={args.paciencia}, "
        f"eval={args.presupuesto_eval}xT, salida={SALIDA}) ===")
    filas = []
    for sem in range(1, args.seeds + 1):
        filas.append(una_semilla(sem, args.rondas, args.epocas,
                                 args.iteraciones, args.lr, args.ent,
                                 args.kl, args.paciencia,
                                 args.presupuesto_eval, log))
    with open(os.path.join(SALIDA, "resultados.csv"), "w",
              encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    log("\n=== RESUMEN ===")
    for c in ("rep_antes", "rep_despues", "bo16_antes", "bo16_despues"):
        log(f"  {c:>13}: {sum(f[c] for f in filas) / len(filas):.2f}%")
    log("  listones: bo64 clones 12.76; R&R ciego 13.73/13.89; "
        "experto TS ~3.66")


if __name__ == "__main__":
    main()
