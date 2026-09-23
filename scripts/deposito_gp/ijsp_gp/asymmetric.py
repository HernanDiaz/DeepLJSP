"""
Right-skewed interval versions of the 70 Taillard instances.

The crisp duration of every operation is recovered as the midpoint of its
symmetric interval, which the symmetric generation scheme preserves
exactly, and the asymmetric bounds are drawn around it as

    p - round(p * U[0, 0.05])   and   p + round(p * U[0, 0.25]),

so that a duration may fall slightly below its nominal value and
considerably above it. Machine routes are unchanged. Instance k of the
sorted list uses the generator seed 40500 + k, so the benchmark is
reproducible file by file.

Usage from the ``code/`` directory:

    python -m ijsp_gp.asymmetric --source ../instances/interval_taillard \
        --out asymmetric_taillard
"""

import argparse
import os
from typing import Dict, List, Tuple

import numpy as np

from .instances import load_instance
from .interval import Interval

DELTA_LOW, DELTA_UP = 0.05, 0.25
SEED_BASE = 40500


def crisp_value(d) -> int:
    """The crisp duration behind a symmetric interval: its exact midpoint."""
    if isinstance(d, Interval):
        p = (d.lower + d.upper) / 2
        if abs(p - round(p)) > 1e-9:
            raise ValueError(f"midpoint is not an integer: {d}")
        return int(round(p))
    return int(d)


def skew(p: int, rng) -> Tuple[int, int]:
    lo = p - int(round(p * rng.uniform(0, DELTA_LOW)))
    up = p + int(round(p * rng.uniform(0, DELTA_UP)))
    return max(1, lo), max(1, up)


def asymmetric_version(problem: Dict, seed: int) -> List[List[Tuple[int, int]]]:
    rng = np.random.default_rng(seed)
    return [[skew(crisp_value(d), rng) for d in row]
            for row in problem["durations"]]


def asymmetric_name(symmetric_name: str) -> str:
    """int__tai20_15_01 -> int__atai20_15_01"""
    return symmetric_name.replace("int__tai", "int__atai", 1)


def write_instance(path: str, name: str, problem: Dict,
                   durations: List[List[Tuple[int, int]]]) -> None:
    n, m = problem["num_jobs"], problem["num_machines"]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"# {name}  {n} jobs  {m} machines\n")
        f.write(f"{n} {m}\n")
        for row in problem["sequences"]:
            f.write(" ".join(str(x) for x in row) + "\n")
        for row in durations:
            f.write(" ".join(f"({lo},{up})" for lo, up in row) + "\n")


def generate(source_dir: str, out_dir: str) -> List[str]:
    """Write the asymmetric version of every instance in ``source_dir``."""
    os.makedirs(out_dir, exist_ok=True)
    names = sorted(os.path.splitext(fn)[0] for fn in os.listdir(source_dir)
                   if fn.startswith("int__tai") and fn.endswith(".txt"))
    written = []
    for k, name in enumerate(names):
        problem = load_instance(os.path.join(source_dir, name + ".txt"), name)
        new_name = asymmetric_name(name)
        write_instance(os.path.join(out_dir, new_name + ".txt"), new_name,
                       problem, asymmetric_version(problem, SEED_BASE + k))
        written.append(new_name)
    return written


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--source", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    written = generate(args.source, args.out)
    print(f"{len(written)} asymmetric instances written to {args.out}")


if __name__ == "__main__":
    main()
