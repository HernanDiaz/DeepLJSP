"""
Comparativa de calidad de los pools de siembra por generador.

Para cada instancia con pools en seeds/, calcula el RE (por E[C_max] = punto
medio del intervalo, vs LB crisp de literatura) del MEJOR individuo y de la
MEDIA del pool, para los cuatro generadores de la escalera:
    graspmor (MOR+eps) < gtmwkr (G&T+eps) < gp (regla GP tuneada+eps) < v2 (RL)

Salida: benchmarks/generators_comparison.csv + tabla por clase y global.
Reanudable/tolerante: los generadores sin pool para una instancia se omiten
(NaN), así funciona aunque la generación aún no haya terminado.
"""

import glob
import os
import re
import sys

sys.path.insert(0, ".")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data.literature_bounds import lb_for_problem_name, ta_name  # noqa

FT10_LB = 930
GENERATORS = ["graspmor", "gtmwkr", "gp", "v2"]  # orden de peor a mejor esperado


def pool_stats(path):
    """(best_mid, mean_mid) del pool, por punto medio del intervalo."""
    mids = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or ";" not in line:
            continue
        lo, up = (float(x) for x in line.split(";")[1].strip("[] ").split(","))
        mids.append((lo + up) / 2.0)
    if not mids:
        return None
    return min(mids), sum(mids) / len(mids)


def instance_lb(pid):
    if pid.startswith("ft10"):
        return FT10_LB, "FT10"
    lb = lb_for_problem_name(pid)
    m = re.search(r"tai(\d+)_(\d+)_(\d+)", pid)
    return lb, ta_name(int(m.group(1)), int(m.group(2)), int(m.group(3)))


def main():
    instances = sorted({os.path.basename(f).split("_v2_pool")[0]
                        for f in glob.glob("seeds/*_v2_pool.csv")})
    rows = []
    for pid in instances:
        lb, label = instance_lb(pid)
        m = re.search(r"tai(\d+_\d+)", pid)
        cls = m.group(1) if m else "ft10"
        rec = {"instance": pid, "ta": label, "lb": lb, "cls": cls}
        for g in GENERATORS:
            st = None
            path = f"seeds/{pid}_{g}_pool.csv"
            if os.path.exists(path):
                st = pool_stats(path)
            if st:
                rec[f"{g}_best"] = (st[0] - lb) / lb * 100
                rec[f"{g}_mean"] = (st[1] - lb) / lb * 100
            else:
                rec[f"{g}_best"] = rec[f"{g}_mean"] = float("nan")
        rows.append(rec)

    os.makedirs("benchmarks", exist_ok=True)
    with open("benchmarks/generators_comparison.csv", "w", encoding="utf-8") as f:
        cols = ["instance", "ta", "lb"] + [f"{g}_{s}" for g in GENERATORS
                                           for s in ("best", "mean")]
        f.write(",".join(cols) + "\n")
        for r in rows:
            f.write(",".join([r["instance"], r["ta"], str(r["lb"])] +
                             [f"{r[f'{g}_{s}']:.2f}" for g in GENERATORS
                              for s in ("best", "mean")]) + "\n")

    # --- tabla resumen por clase (medias sobre las instancias de la clase) ---
    def avg(cr, key):
        vals = [x[key] for x in cr if x[key] == x[key]]  # descarta NaN
        return sum(vals) / len(vals) if vals else float("nan")

    classes = sorted({r["cls"] for r in rows},
                     key=lambda c: (len(c), c))
    hdr = f"{'Clase':<8}" + "".join(f"{g[:8]:>10}" for g in GENERATORS)
    print("=== RE MEDIO del pool (%) por clase ===")
    print(hdr); print("-" * len(hdr))
    glob_rows = []
    for cls in classes:
        cr = [r for r in rows if r["cls"] == cls]
        glob_rows += cr
        print(f"{cls:<8}" + "".join(f"{avg(cr, f'{g}_mean'):>9.1f}%"
                                    for g in GENERATORS))
    print("-" * len(hdr))
    print(f"{'GLOBAL':<8}" + "".join(f"{avg(glob_rows, f'{g}_mean'):>9.1f}%"
                                     for g in GENERATORS))

    print("\n=== RE del MEJOR individuo del pool (%) por clase ===")
    print(hdr); print("-" * len(hdr))
    for cls in classes:
        cr = [r for r in rows if r["cls"] == cls]
        print(f"{cls:<8}" + "".join(f"{avg(cr, f'{g}_best'):>9.1f}%"
                                    for g in GENERATORS))
    print("-" * len(hdr))
    print(f"{'GLOBAL':<8}" + "".join(f"{avg(glob_rows, f'{g}_best'):>9.1f}%"
                                     for g in GENERATORS))

    # --- dominancia: en cuántas instancias cada generador es el mejor ---
    print("\n=== Dominancia (generador con mejor MEDIA de pool por instancia) ===")
    wins = {g: 0 for g in GENERATORS}
    complete = 0
    for r in rows:
        means = {g: r[f"{g}_mean"] for g in GENERATORS if r[f"{g}_mean"] == r[f"{g}_mean"]}
        if len(means) == len(GENERATORS):
            complete += 1
            wins[min(means, key=means.get)] += 1
    for g in GENERATORS:
        print(f"  {g:<10}: {wins[g]}/{complete} instancias (con los 4 pools)")
    print("\nCSV: benchmarks/generators_comparison.csv")


if __name__ == "__main__":
    main()
