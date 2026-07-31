# -*- coding: utf-8 -*-
"""Evaluaciones best-of-N cuyos numeros llegaron al paper DRL sin registro.

Tres tareas, cada una con su CSV NUEVO bajo benchmarks/ (no se toca nada
existente; si el CSV ya tiene una fila, se salta: reanudable):

    python scripts/eval_pending_bo.py crosssize   -> eval_crosssize_bo64.csv
    python scripts/eval_pending_bo.py multisize   -> eval_multisize_bo64.csv
    python scripts/eval_pending_bo.py bo1024      -> eval_fair_bo1024.csv

El makespan del mejor schedule se recompone COMPONENTE A COMPONENTE
([max lowers, max uppers]) sobre las tareas, la Eq. 2 del paper; se
guarda tambien el punto medio del final lexicografico para poder
comparar con los numeros antiguos.
"""
import csv
import os
import sys
import time

sys.path.insert(0, ".")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.agents_v2 import AgentV2                       # noqa: E402
from jobshop_rl.data import PROBLEM_REGISTRY                   # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402

CROSS_INSTANCIAS = [
    "int__tai15_15_01", "int__tai15_15_02", "int__tai15_15_05",
    "int__tai20_20_01", "int__tai20_20_05", "int__tai30_15_01",
    "int__tai30_20_01", "int__tai50_15_01", "int__tai50_20_01",
]
MULTI_INSTANCIAS = [
    "int__tai15_15_05", "int__tai20_20_05", "int__tai30_15_01",
    "int__tai30_20_01", "int__tai50_20_01",
]
CKPTS_FINALES = [f"models/v2_final_deepsets_1000ep_seed{s}.pt"
                 for s in (2, 3, 4)]


def mids_del_schedule(schedule):
    """(mid componentwise, mid lexicografico) del schedule devuelto."""
    lo_max, up_max, lex = 0.0, 0.0, (0.0, 0.0)
    for t in schedule:
        e = t.get("end")
        if hasattr(e, "lower"):
            lo, up = float(e.lower), float(e.upper)
        elif isinstance(e, dict):
            lo, up = float(e["lower"]), float(e["upper"])
        else:
            lo = up = float(e)
        lo_max, up_max = max(lo_max, lo), max(up_max, up)
        if up > lex[1] or (up == lex[1] and lo > lex[0]):
            lex = (lo, up)
    return (lo_max + up_max) / 2.0, (lex[0] + lex[1]) / 2.0


def evalua(ckpt, instancia, n_samples):
    problem = PROBLEM_REGISTRY[instancia]()
    env = EnvironmentFactory.create_from_problem(problem, "adaptive", seed=1)
    agent = AgentV2(env, seed=1, attention_layers=0)
    agent.load_checkpoint(ckpt)
    t0 = time.time()
    _, schedule, _, _ = agent.evaluate_policy(n_samples=n_samples)
    mid_comp, mid_lex = mids_del_schedule(schedule)
    return mid_comp, mid_lex, time.time() - t0


def corre(salida, trabajos, n_samples):
    """trabajos: lista de (checkpoint, instancia). Append reanudable."""
    hechas = set()
    if os.path.exists(salida):
        with open(salida, encoding="utf-8") as f:
            hechas = {(r["checkpoint"], r["instance"])
                      for r in csv.DictReader(f)}
    nuevo = not os.path.exists(salida)
    with open(salida, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if nuevo:
            w.writerow(["checkpoint", "instance", "lb", "n_samples",
                        "mid_comp", "mid_lex", "re_comp", "re_lex",
                        "seconds"])
        for ckpt, inst in trabajos:
            clave = (os.path.basename(ckpt), inst)
            if clave in hechas:
                print(f"  ya hecha: {clave}", flush=True)
                continue
            lb = lb_for_problem_name(inst)
            mid_c, mid_l, secs = evalua(ckpt, inst, n_samples)
            w.writerow([clave[0], inst, lb, n_samples,
                        f"{mid_c:.1f}", f"{mid_l:.1f}",
                        f"{(mid_c - lb) / lb * 100:.4f}",
                        f"{(mid_l - lb) / lb * 100:.4f}", f"{secs:.0f}"])
            f.flush()
            print(f"  {clave[0]} {inst}: RE_comp="
                  f"{(mid_c - lb) / lb * 100:.2f}% ({secs:.0f}s)", flush=True)


def main():
    tarea = sys.argv[1] if len(sys.argv) > 1 else ""
    if tarea == "crosssize":
        trabajos = [(c, i) for i in CROSS_INSTANCIAS for c in CKPTS_FINALES]
        corre("benchmarks/eval_crosssize_bo64.csv", trabajos, 64)
    elif tarea == "multisize":
        ckpts = [f"benchmarks/v2-multisize{sufijo}_seed{s}_model.pt"
                 for sufijo in ("", "-12k") for s in (2, 3, 4)]
        trabajos = [(c, i) for i in MULTI_INSTANCIAS for c in ckpts]
        corre("benchmarks/eval_multisize_bo64.csv", trabajos, 64)
    elif tarea == "bo1024":
        # protocolo del borrador: el pool mezcla las tres semillas; aqui
        # 342+341+341 muestras por instancia, el mejor global se decide
        # al agregar (columna mid_comp minima por instancia)
        # las 70 del benchmark: interval Taillard CON cota de literatura
        # (el registro tambien tiene las 100x20, fuera del benchmark)
        universo = sorted(k for k in PROBLEM_REGISTRY
                          if k.startswith("int__tai")
                          and not k.startswith("int__tai100")
                          and lb_for_problem_name(k) is not None)
        assert len(universo) == 70, f"esperaba 70, hay {len(universo)}"
        trabajos = [(c, i) for i in universo for c in CKPTS_FINALES]
        corre("benchmarks/eval_fair_bo1024.csv", trabajos, 342)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
