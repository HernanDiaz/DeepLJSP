"""
Evaluación zero-shot cross-size del AgentV2 — lo que el v1 no podía hacer.

Carga un checkpoint del v2 entrenado en 20x15 y lo evalúa (best-of-64) sobre
instancias de otros tamaños, comparando con MOR y con el LB de la literatura.

Uso:
    python scripts/eval_v2_crosssize.py <checkpoint.pt> [instancias...]

Por defecto evalúa 3 instancias de 15x15 y 3 de 30x15.
"""

import sys
import time

sys.path.insert(0, ".")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.agents_v2 import AgentV2  # noqa: E402
from jobshop_rl.data import PROBLEM_REGISTRY  # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.heuristics.strategies import MORHeuristic  # noqa: E402
from jobshop_rl.models.interval import Interval  # noqa: E402

DEFAULT_INSTANCES = [
    "int__tai15_15_01", "int__tai15_15_02", "int__tai15_15_03",
    "int__tai30_15_01", "int__tai30_15_02", "int__tai30_15_03",
]
N_SAMPLES = 64


def _mid_up(value):
    if isinstance(value, Interval):
        return value.midpoint, float(value.upper)
    return float(value), float(value)


def run_mor(env):
    heuristic = MORHeuristic()
    state = env.reset()
    done = False
    while not done and state["eligible_ops"]:
        features = env.get_features(state)
        a = min(heuristic.select_action(state["eligible_ops"], features),
                len(state["eligible_ops"]) - 1)
        state, _, done, _ = env.step(a)
    return _mid_up(max(env.job_completion_time))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    checkpoint = sys.argv[1]
    instances = sys.argv[2:] or DEFAULT_INSTANCES

    print(f"Checkpoint: {checkpoint} | best-of-{N_SAMPLES}")
    print(f"{'Instancia':<18} {'LB lit.':>7} {'v2 E[Cmax]':>10} {'v2 RE':>7} "
          f"{'MOR E[Cmax]':>11} {'MOR RE':>7} {'t(s)':>6}")
    print("-" * 74)

    for pid in instances:
        problem = PROBLEM_REGISTRY[pid]()
        lb = lb_for_problem_name(pid)

        env = EnvironmentFactory.create_from_problem(problem, "adaptive", seed=1)
        agent = AgentV2(env, seed=1)
        agent.load_checkpoint(checkpoint)

        start = time.time()
        mk_up, schedule, _, _ = agent.evaluate_policy(n_samples=N_SAMPLES)
        elapsed = time.time() - start
        # midpoint del mejor schedule: reconstruir del estado final no es
        # posible aquí (el env quedó en el último muestreo); usar el schedule
        best = None
        for t in schedule:
            end = t.get("end")
            e_mid, e_up = _mid_up(end)
            if best is None or e_up > best[1]:
                best = (e_mid, e_up)
        v2_mid = best[0] if best else float("inf")

        mor_mid, _ = run_mor(env)

        v2_re = (v2_mid - lb) / lb * 100 if lb else float("nan")
        mor_re = (mor_mid - lb) / lb * 100 if lb else float("nan")
        print(f"{pid:<18} {lb:>7} {v2_mid:>10.0f} {v2_re:>6.1f}% "
              f"{mor_mid:>11.0f} {mor_re:>6.1f}% {elapsed:>6.0f}")


if __name__ == "__main__":
    main()
