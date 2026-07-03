"""
Informe RE(%) de una ejecución del benchmark, con los LB crisp de la literatura.

RE(%) = (E[C_max] − LB)/LB × 100, con E[C_max] = punto medio del intervalo de
makespan (convención del campo IJSP) reconstruido de los schedules guardados.
También reporta la variante conservadora por peor caso.

Uso:
    python scripts/re_report.py "benchmarks/v2-full__*.json"
"""

import glob
import json
import sys

sys.path.insert(0, ".")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data.literature_bounds import lb_for_problem_name, ta_name  # noqa: E402


def makespan_bounds(schedule_json_path):
    """(lower, upper) del makespan = end con máximo lexicográfico."""
    tasks = json.load(open(schedule_json_path))
    best = None
    for t in tasks:
        end = t["end"]
        lo, up = (end["lower"], end["upper"]) if isinstance(end, dict) else (float(end), float(end))
        if best is None or up > best[1] or (up == best[1] and lo > best[0]):
            best = (lo, up)
    return best


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    matches = sorted(glob.glob(sys.argv[1]))
    if not matches:
        raise FileNotFoundError(sys.argv[1])
    result = json.load(open(matches[-1], encoding="utf-8"))
    tag, commit = result["tag"], result["commit"]

    # Reconstruir midpoints de los schedules por semilla
    run_dirs = sorted(glob.glob(f"outputs/bench_{tag}__{commit}__*_seed*"))
    if not run_dirs:
        raise FileNotFoundError(f"No hay directorios outputs/bench_{tag}__{commit}__*_seed*")

    problems = sorted(next(iter(result["seeds"].values()))["problems"].keys())

    print(f"Benchmark: {tag} @ {commit} ({len(result['seeds'])} semillas)")
    print(f"{'Inst.':<6} {'LB lit.':>7} {'E[Cmax] media':>13} {'E[Cmax] mejor':>13} "
          f"{'RE media':>9} {'RE mejor':>9} {'RE peor-caso media':>18}")
    print("-" * 82)

    re_means, re_bests = [], []
    for prob in problems:
        lb = lb_for_problem_name(prob)
        if lb is None:
            print(f"{prob:<6} sin LB de literatura, omitida")
            continue
        mids, uppers = [], []
        for d in run_dirs:
            lo, up = makespan_bounds(f"{d}/plots/test/{prob}_schedule.json")
            mids.append((lo + up) / 2.0)
            uppers.append(up)
        m_mean, m_best = sum(mids) / len(mids), min(mids)
        u_mean = sum(uppers) / len(uppers)
        re_mean = (m_mean - lb) / lb * 100
        re_best = (m_best - lb) / lb * 100
        re_upper = (u_mean - lb) / lb * 100
        re_means.append(re_mean)
        re_bests.append(re_best)
        import re as _re
        m = _re.search(r"tai(\d+)_(\d+)_(\d+)", prob.lower())
        ta = ta_name(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        print(f"{ta:<6} {lb:>7} {m_mean:>13.0f} {m_best:>13.0f} "
              f"{re_mean:>8.1f}% {re_best:>8.1f}% {re_upper:>17.1f}%")

    if re_means:
        print("-" * 82)
        print(f"RE medio: {sum(re_means)/len(re_means):.1f}% (media semillas) | "
              f"{sum(re_bests)/len(re_bests):.1f}% (mejor semilla)")


if __name__ == "__main__":
    main()
