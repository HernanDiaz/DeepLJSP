# -*- coding: utf-8 -*-
"""Cronometra la inferencia: un rollout greedy y el best-of-64 por tamano.

El paper afirmaba tiempos de construccion sin haberlos medido nunca (era
de las pocas cifras sin comprobacion en verify_numbers.py). Esto los mide
sobre el checkpoint desplegado, con el mismo camino de codigo que las
evaluaciones del paper.

    python scripts/mide_tiempos_inferencia.py

Salida NUEVA: benchmarks/tiempos_inferencia.csv (no sobreescribe nada).
Registra la carga de la maquina en el momento de medir, porque si hay
otros trabajos en marcha las cifras son cotas superiores.
"""
import csv
import glob
import os
import sys
import time

sys.path.insert(0, ".")
os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.agents_v2 import AgentV2                       # noqa: E402
from jobshop_rl.data import PROBLEM_REGISTRY                   # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402

SALIDA = "benchmarks/tiempos_inferencia.csv"
ULTIMA = "INT__TAI20_15_04.F.15_01_INTERVAL_model.pt"
INSTANCIAS = [("15x15", "int__tai15_15_01"), ("20x15", "int__tai20_15_05"),
              ("30x20", "int__tai30_20_01"), ("50x20", "int__tai50_20_01")]
N = 64


def checkpoint():
    for d in sorted(glob.glob("outputs/bench_v2-full-1000ep__*_seed2")):
        p = os.path.join(d, ULTIMA)
        if os.path.exists(p):
            return p
    raise SystemExit("sin checkpoint desplegado")


def rollout(agent, env, greedy):
    state = env.reset()
    done = False
    pasos = 0
    while not done and state["eligible_ops"]:
        salida = agent.select_action(state, training=not greedy)
        a = salida[0] if isinstance(salida, tuple) else salida
        state, _, done, _ = env.step(
            min(int(a), len(state["eligible_ops"]) - 1))
        pasos += 1
    return pasos


def carga():
    try:
        import subprocess
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" |"
             " Where-Object {$_.CommandLine -match 'train_eval_config'} |"
             " Measure-Object).Count"],
            capture_output=True, text=True, timeout=60)
        return r.stdout.strip()
    except Exception:
        return "?"


def main():
    ruta = checkpoint()
    otros = carga()
    print(f"checkpoint: {ruta}")
    print(f"workers de irace activos al medir: {otros}\n")

    nuevo = not os.path.exists(SALIDA)
    f = open(SALIDA, "a", encoding="utf-8", newline="")
    w = csv.writer(f)
    if nuevo:
        w.writerow(["clase", "instancia", "pasos", "greedy_s", "bo64_s",
                    "ms_por_paso", "workers_irace"])

    for clase, inst in INSTANCIAS:
        problem = PROBLEM_REGISTRY[inst]()
        env = EnvironmentFactory.create_from_problem(problem, "adaptive",
                                                     seed=1)
        agent = AgentV2(env, seed=1, attention_layers=0)
        agent.load_checkpoint(ruta)

        rollout(agent, env, True)          # calentamiento, no se cronometra
        t0 = time.perf_counter()
        pasos = rollout(agent, env, True)
        t_greedy = time.perf_counter() - t0

        t0 = time.perf_counter()
        for i in range(N):
            rollout(agent, env, i == 0)
        t_bo = time.perf_counter() - t0

        ms = t_greedy / pasos * 1000
        print(f"  {clase:6s} {pasos:4d} pasos | greedy {t_greedy:6.2f}s | "
              f"best-of-{N} {t_bo:7.1f}s | {ms:.2f} ms/paso")
        w.writerow([clase, inst, pasos, f"{t_greedy:.3f}", f"{t_bo:.1f}",
                    f"{ms:.2f}", otros])
        f.flush()
    f.close()
    print("\nhecho")


if __name__ == "__main__":
    main()
