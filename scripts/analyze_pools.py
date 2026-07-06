"""
Análisis de los pools de soluciones: RE mejor y medio por instancia.

Para cada instancia con pool en seeds/, calcula el RE (por E[C_max], LB crisp
de literatura) del mejor individuo y de la media del pool, para el generador
v2 y el baseline graspmor. Escribe benchmarks/pools_analysis.csv y muestra la
tabla por pantalla con resumen por clase de tamaño.
"""

import glob
import os
import re
import sys

sys.path.insert(0, ".")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data.literature_bounds import lb_for_problem_name, ta_name  # noqa: E402

FT10_LB = 930  # óptimo crisp conocido de ft10


def pool_stats(path):
    mids = []
    for line in open(path, encoding="utf-8"):
        lo, up = (float(x) for x in line.strip().split(";")[1].strip("[] ").split(","))
        mids.append((lo + up) / 2.0)
    return min(mids), sum(mids) / len(mids)


def instance_lb(pid):
    if pid.startswith("ft10"):
        return FT10_LB, "FT10"
    lb = lb_for_problem_name(pid)
    m = re.search(r"tai(\d+)_(\d+)_(\d+)", pid)
    ta = ta_name(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return lb, ta


def main():
    instances = sorted({os.path.basename(f).split("_v2_pool")[0]
                        for f in glob.glob("seeds/*_v2_pool.csv")})

    rows = []
    for pid in instances:
        lb, label = instance_lb(pid)
        v2_best, v2_mean = pool_stats(f"seeds/{pid}_v2_pool.csv")
        try:
            g_best, g_mean = pool_stats(f"seeds/{pid}_graspmor_pool.csv")
        except FileNotFoundError:
            g_best = g_mean = float("nan")
        rows.append({
            "instance": pid, "ta": label, "lb": lb,
            "v2_best_re": (v2_best - lb) / lb * 100,
            "v2_mean_re": (v2_mean - lb) / lb * 100,
            "mor_best_re": (g_best - lb) / lb * 100,
            "mor_mean_re": (g_mean - lb) / lb * 100,
        })

    # CSV
    os.makedirs("benchmarks", exist_ok=True)
    with open("benchmarks/pools_analysis.csv", "w", encoding="utf-8") as f:
        f.write("instance,ta,lb,v2_best_re,v2_mean_re,graspmor_best_re,graspmor_mean_re\n")
        for r in rows:
            f.write(f"{r['instance']},{r['ta']},{r['lb']},"
                    f"{r['v2_best_re']:.2f},{r['v2_mean_re']:.2f},"
                    f"{r['mor_best_re']:.2f},{r['mor_mean_re']:.2f}\n")

    # Tabla por pantalla
    print(f"{'Inst.':<6} {'LB':>6} | {'v2 best':>8} {'v2 medio':>9} | {'MORe best':>9} {'MORe medio':>10}")
    print("-" * 60)
    current_class = None
    class_rows = []

    def flush_class(name, cr):
        if not cr:
            return
        vb = sum(x['v2_best_re'] for x in cr) / len(cr)
        vm = sum(x['v2_mean_re'] for x in cr) / len(cr)
        gb = sum(x['mor_best_re'] for x in cr) / len(cr)
        print(f"{'  * ' + name + ' medias':<13} | {vb:>7.1f}% {vm:>8.1f}% | {gb:>8.1f}%")
        print("-" * 60)

    for r in rows:
        m = re.search(r"tai(\d+_\d+)", r["instance"])
        cls = m.group(1) if m else "clasica"
        if cls != current_class:
            flush_class(current_class or "", class_rows)
            current_class, class_rows = cls, []
        class_rows.append(r)
        print(f"{r['ta']:<6} {r['lb']:>6} | {r['v2_best_re']:>7.1f}% {r['v2_mean_re']:>8.1f}% "
              f"| {r['mor_best_re']:>8.1f}% {r['mor_mean_re']:>9.1f}%")
    flush_class(current_class, class_rows)

    n_win = sum(1 for r in rows if r['v2_mean_re'] < r['mor_best_re'])
    print(f"\nInstancias donde la MEDIA del pool v2 bate al MEJOR del pool MOR+e: {n_win}/{len(rows)}")
    print("CSV: benchmarks/pools_analysis.csv")


if __name__ == "__main__":
    main()
