"""
Deterministic evaluation of a dispatching rule on a set of instances.

For each instance, one semi-active constructive pass; reported per instance:

* RE (%): relative error of the expected makespan, the midpoint of the
  interval makespan, against the instance's crisp reference bound.
* width (%): relative width of the predicted makespan interval.

The interval makespan is component-wise: [max of lower completion bounds,
max of upper completion bounds] over the jobs.
"""

from typing import Dict, List, Tuple

from .env import make_env
from .heuristics import HeuristicStrategy
from .instances import lb_for_instance_name
from .interval import Interval


def rollout(problem: Dict, heuristic: HeuristicStrategy):
    """One constructive pass; returns (makespan_lower, makespan_upper, env)."""
    env = make_env(problem, seed=0)
    state = env.reset()
    done = False
    while not done and state["eligible_ops"]:
        features = env.get_features(state)
        action = min(heuristic.select_action(state["eligible_ops"], features),
                     len(state["eligible_ops"]) - 1)
        state, _, done, _ = env.step(action)
    completions = env.job_completion_time
    lo = max(c.lower if isinstance(c, Interval) else c for c in completions)
    up = max(c.upper if isinstance(c, Interval) else c for c in completions)
    return lo, up, env


def evaluate_rule(heuristic: HeuristicStrategy,
                  problems: Dict[str, Dict]) -> Tuple[float, float, List[Dict]]:
    """Evaluate a heuristic on a dict of instances.

    Returns (mean RE, mean relative width, per-instance rows)."""
    rows = []
    for name in sorted(problems):
        problem = problems[name]
        lb = lb_for_instance_name(name)
        if lb is None:
            raise ValueError(f"no reference bound for instance {name}")
        lo, up, _ = rollout(problem, heuristic)
        re_pct = ((lo + up) / 2 - lb) / lb * 100
        width_pct = (up - lo) / ((up + lo) / 2) * 100
        rows.append({"instance": name, "re": re_pct, "width": width_pct,
                     "makespan_lower": lo, "makespan_upper": up})
    n = len(rows)
    return (sum(r["re"] for r in rows) / n,
            sum(r["width"] for r in rows) / n, rows)


def main():
    import argparse
    import glob

    from .instances import load_dir
    from .rules import load_rule

    ap = argparse.ArgumentParser(
        description="Evaluate rule JSON files on an instance directory.")
    ap.add_argument("--rules", required=True,
                    help="glob pattern of rule JSON files")
    ap.add_argument("--instances", required=True,
                    help="directory with instance files")
    args = ap.parse_args()

    problems = load_dir(args.instances)
    print(f"{len(problems)} instances")
    for path in sorted(glob.glob(args.rules)):
        heuristic = load_rule(path)
        re_mean, width_mean, _ = evaluate_rule(heuristic, problems)
        print(f"{path}: RE {re_mean:.4f}%  width {width_mean:.4f}%")


if __name__ == "__main__":
    main()
