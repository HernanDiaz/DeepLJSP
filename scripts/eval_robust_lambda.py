# -*- coding: utf-8 -*-
"""El brazo de objetivo robusto (lambda=1) frente al objetivo normal.

7.5 cierra diciendo que la maquinaria de intervalos es inerte PARA EL
MAKESPAN ESPERADO, y deja abierto si un objetivo que premiara un
intervalo estrecho cambiaria la respuesta. v2-robust-lam1 entrena con
   up + lambda (up - lo),   lambda = 1
que es el analogo del f_lambda del estudio companero. Este script mide
lo que hace falta para contestar: no solo la RE, tambien el ANCHO del
intervalo que produce cada politica, que es la magnitud que lambda
pretende encoger.

Se guarda CADA rollout con sus dos extremos, no el mejor: asi el
mejor-de-N por cota superior y el mejor-de-N por valor robusto se
reconstruyen despues del mismo deposito, y la comparacion no depende de
haber elegido el criterio de seleccion antes de mirar.

    python scripts/eval_robust_lambda.py

Escribe benchmarks/robust_lambda/rollouts.csv (reanudable, append).
"""
import csv
import os
import sys
import time

sys.path.insert(0, ".")

# la evaluacion NO debe ver lambda: el objetivo entra por el entrenamiento,
# y aqui se mide con la metrica del paper. Si quedara puesta del lanzador,
# _episode_makespan devolveria el valor robusto y contaminaria la medida.
os.environ.pop("DEEPLJSP_V2_LAMBDA", None)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.agents_v2 import AgentV2                       # noqa: E402
from jobshop_rl.data import PROBLEM_REGISTRY                   # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.models.interval import Interval, final_makespan  # noqa: E402

DESARROLLO = [f"int__tai20_15_{k:02d}" for k in range(5, 11)]   # TA15-TA20
N_MUESTRAS = 64                 # el best-of-64 con que el paper compara
SALIDA = "benchmarks/robust_lambda/rollouts.csv"

BASE = "outputs/bench_v2-full-1000ep__*_seed{s}"
LAM1 = "outputs/bench_v2-robust-lam1__6f5e62e__20260803_101120_seed{s}"
ULTIMA = "INT__TAI20_15_04.F.15_01_INTERVAL_model.pt"   # el checkpoint
# final del brazo es el de la ultima instancia entrenada, no best_model.pt
# (verificado por md5 contra models/v2_final_deepsets_1000ep_seed2.pt)


def checkpoints():
    """[(brazo, semilla, ruta)] de los dos brazos, tres semillas cada uno."""
    import glob
    out = []
    for brazo, patron in (("lam1", LAM1), ("base", BASE)):
        for s in (2, 3, 4):
            if brazo == "base":
                ruta = f"models/v2_final_deepsets_1000ep_seed{s}.pt"
            else:
                dirs = glob.glob(patron.format(s=s))
                if not dirs:
                    print(f"  AVISO: sin directorio para {brazo} semilla {s}")
                    continue
                ruta = os.path.join(dirs[0], ULTIMA)
            if os.path.exists(ruta):
                out.append((brazo, s, ruta))
            else:
                print(f"  AVISO: falta {ruta}")
    return out


def extremos(env):
    """(lower, upper) del makespan componente a componente, Eq. 2."""
    m = final_makespan(env.job_completion_time)
    if isinstance(m, Interval):
        return float(m.lower), float(m.upper)
    return float(m), float(m)


def rollouts(ruta, instancia, n):
    problem = PROBLEM_REGISTRY[instancia]()
    env = EnvironmentFactory.create_from_problem(problem, "adaptive", seed=1)
    agent = AgentV2(env, seed=1, attention_layers=0)
    agent.load_checkpoint(ruta)
    out = []
    for i in range(n):
        state = env.reset()
        done = False
        while not done and state["eligible_ops"]:
            salida = agent.select_action(state, training=(i > 0))
            a = salida[0] if isinstance(salida, tuple) else salida
            state, _, done, _ = env.step(
                min(int(a), len(state["eligible_ops"]) - 1))
        out.append(extremos(env))
    return out


def main():
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    hechos = {}
    if os.path.exists(SALIDA):
        with open(SALIDA, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                k = (r["arm"], r["seed"], r["instance"])
                hechos[k] = hechos.get(k, 0) + 1

    nuevo = not os.path.exists(SALIDA) or os.path.getsize(SALIDA) == 0
    f = open(SALIDA, "a", encoding="utf-8", newline="")
    w = csv.writer(f)
    if nuevo:
        w.writerow(["arm", "seed", "instance", "lb", "sample_idx",
                    "lower", "upper"])

    for brazo, s, ruta in checkpoints():
        for instancia in DESARROLLO:
            if hechos.get((brazo, str(s), instancia), 0) >= N_MUESTRAS:
                continue
            lb = lb_for_problem_name(instancia)
            t0 = time.time()
            for i, (lo, up) in enumerate(rollouts(ruta, instancia,
                                                  N_MUESTRAS)):
                w.writerow([brazo, s, instancia, lb, i,
                            f"{lo:.1f}", f"{up:.1f}"])
            f.flush()
            print(f"  {brazo} s{s} {instancia}: {N_MUESTRAS} rollouts en "
                  f"{time.time() - t0:.0f}s", flush=True)
    f.close()
    print("hecho")


if __name__ == "__main__":
    main()
