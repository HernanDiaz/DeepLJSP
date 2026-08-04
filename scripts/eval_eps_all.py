# -*- coding: utf-8 -*-
"""Robustez ejecucional de TODOS los metodos, con semilla reproducible.

Dos motivos para no limitarse a extender eval_eps_policy.py:

1. Aquel siembra las realizaciones con abs(hash(pid)), y el hash de las
   cadenas en Python esta aleatorizado POR PROCESO salvo que se fije
   PYTHONHASHSEED, que su lanzador no fija. Dentro de una tirada las
   realizaciones son comunes a todos los metodos, que es lo que el
   contraste pareado necesita; pero aquel barrido se relanzo a mitad,
   de modo que las instancias calculadas antes y despues del corte NO
   comparten realizaciones, y una instancia partida por el corte
   tendria metodos con realizaciones distintas. Aqui la semilla sale de
   crc32 del identificador, que es estable entre procesos y maquinas.

2. Falta el brazo robusto lambda=1 de 7.5. Es la pregunta que 7.6 deja
   servida: los tres metodos mas fieles no optimizan el ancho, y ese
   brazo si lo hace. Si su eps-barra mejora, la maquinaria intervalar
   deja de ser inerte para la magnitud que le corresponde.

Se recalcula todo en un unico proceso, de modo que el CSV nuevo es
internamente pareado. No se toca benchmarks/eval_eps_policy.csv.

    python scripts/eval_eps_all.py

Salida NUEVA: benchmarks/eval_eps_all.csv (reanudable por filas; la
semilla es funcion de la instancia, asi que reanudar no rompe nada).
"""
import csv
import glob
import importlib.util
import json
import os
import sys
import zlib

import numpy as np

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import torch                                                   # noqa: E402

from jobshop_rl.agents_v2 import AgentV2                       # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.heuristics.gp_rule import GPRuleHeuristic      # noqa: E402
from jobshop_rl.heuristics.strategies import (                 # noqa: E402
    ESTHeuristic, GTHeuristic, MORHeuristic)

spec = importlib.util.spec_from_file_location(
    "reps", "scripts/robustness_epsilon.py")
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)

INSTANCIAS = [
    "int__tai20_15_05", "int__tai20_15_06", "int__tai20_15_07",
    "int__tai20_15_08", "int__tai20_15_09", "int__tai20_15_10",
    "int__tai15_15_01", "int__tai15_15_02", "int__tai15_15_05",
    "int__tai20_20_01", "int__tai20_20_05", "int__tai30_15_01",
    "int__tai30_20_01", "int__tai50_15_01", "int__tai50_20_01",
]
CKPTS = [f"models/v2_final_deepsets_1000ep_seed{s}.pt" for s in (2, 3, 4)]
LAM1 = "outputs/bench_v2-robust-lam1__*_seed{s}/INT__TAI20_15_04.F.15_01_INTERVAL_model.pt"
K = 1000
N_BO = 64
SALIDA = "benchmarks/eval_eps_all.csv"


def semilla(pid):
    """Estable entre procesos, al contrario que hash() de una cadena."""
    return zlib.crc32(pid.encode("utf-8")) % (2 ** 31)


def secuencia_politica(env, agent, muestrear, semilla_torch):
    torch.manual_seed(semilla_torch)
    state = env.reset()
    seq, done = [], False
    while not done and state["eligible_ops"]:
        salida = agent.select_action(state, training=muestrear)
        a = salida[0] if isinstance(salida, tuple) else salida
        a = min(int(a), len(state["eligible_ops"]) - 1)
        seq.append(state["eligible_ops"][a] + 1)
        state, _, done, _ = env.step(a)
    return seq


def mejor_de_n(env, agent, lo, up, mseq, n, robusto=False):
    """Greedy + (n-1) muestras. El brazo robusto se queda con la mejor
    por su PROPIO objetivo, up + (up-lo): elegir por otra cosa seria
    incoherente con como fue entrenado (misma razon que en 7.5)."""
    mejor, mejor_clave = None, None
    for i in range(n):
        seq = secuencia_politica(env, agent, muestrear=(i > 0),
                                 semilla_torch=1000 + i)
        clo, cup = R.predicted_interval(seq, lo, up, mseq)
        clave = (2 * cup - clo,) if robusto else (cup, clo)
        if mejor_clave is None or clave < mejor_clave:
            mejor, mejor_clave = seq, clave
    return mejor


def checkpoints_lam1():
    out = []
    for s in (2, 3, 4):
        g = glob.glob(LAM1.format(s=s))
        if g:
            out.append((f"lam1-seed{s}", g[0]))
    return out


def main():
    hechas = set()
    if os.path.exists(SALIDA):
        with open(SALIDA, encoding="utf-8") as f:
            hechas = {(r["instance"], r["method"]) for r in csv.DictReader(f)}
    nuevo = not os.path.exists(SALIDA) or os.path.getsize(SALIDA) == 0
    out = open(SALIDA, "a", encoding="utf-8", newline="")
    w = csv.writer(out)
    if nuevo:
        w.writerow(["instance", "method", "eps", "e_mid", "coverage",
                    "c_lo", "c_up", "width_rel"])

    lam = checkpoints_lam1()
    print(f"{len(lam)} checkpoints del brazo lambda=1", flush=True)

    for pid in INSTANCIAS:
        lo, up, mseq = R.instance_arrays(pid)
        rng = np.random.default_rng(semilla(pid))
        dur = R.sample_durations(lo, up, K, rng)

        metodos = {}
        env = EnvironmentFactory.create_from_problem_id(pid, "adaptive",
                                                        seed=1)
        _gp = json.load(open("benchmarks/reevo_fixedfit/gp_tuned_seed1.json",
                             encoding="utf-8"))["tree"]
        for nombre, h in [("MOR", MORHeuristic()), ("EST", ESTHeuristic()),
                          ("GT-MWKR", GTHeuristic(tiebreak="mwkr")),
                          ("GP", GPRuleHeuristic(_gp))]:
            metodos[nombre] = R.heuristic_sequence(env, h)
        for ck in CKPTS:
            et = os.path.basename(ck).replace(
                "v2_final_deepsets_1000ep_", "").replace(".pt", "")
            agent = AgentV2(env, seed=1, attention_layers=0)
            agent.load_checkpoint(ck)
            metodos[f"policy-greedy-{et}"] = secuencia_politica(
                env, agent, muestrear=False, semilla_torch=0)
            metodos[f"policy-bo{N_BO}-{et}"] = mejor_de_n(
                env, agent, lo, up, mseq, N_BO)
        for et, ck in lam:
            agent = AgentV2(env, seed=1, attention_layers=0)
            agent.load_checkpoint(ck)
            metodos[f"{et}-greedy"] = secuencia_politica(
                env, agent, muestrear=False, semilla_torch=0)
            metodos[f"{et}-bo{N_BO}"] = mejor_de_n(
                env, agent, lo, up, mseq, N_BO, robusto=True)

        for nombre, seq in metodos.items():
            if (pid, nombre) in hechas:
                continue
            clo, cup = R.predicted_interval(seq, lo, up, mseq)
            e_mid = (clo + cup) / 2.0
            cmax = R.decode_mc(seq, dur, mseq, K)
            eps = float(np.mean(np.abs(cmax - e_mid) / e_mid))
            cov = float(np.mean((cmax >= clo) & (cmax <= cup)))
            w.writerow([pid, nombre, f"{eps:.6f}", f"{e_mid:.1f}",
                        f"{cov:.4f}", f"{clo:.1f}", f"{cup:.1f}",
                        f"{(cup - clo) / e_mid * 100:.4f}"])
            out.flush()
            print(f"{pid} {nombre}: eps={eps * 1000:.2f}e-3 "
                  f"ancho={(cup - clo) / e_mid * 100:.2f}%", flush=True)
    out.close()
    print("hecho")


if __name__ == "__main__":
    main()
