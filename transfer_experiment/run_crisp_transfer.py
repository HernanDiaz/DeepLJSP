"""
EXPERIMENTO DE TRANSFERENCIA A CRISP (Mitad A — transferencia de semillas).

Pregunta: las secuencias optimizadas para INTERVALO (que minimizan el peor
caso), ¿siguen siendo buenas cuando se evalúan bajo aritmética CRISP (valor
puntual)?

Método: re-decodifica los pools de intervalo (v2, gp, gtmwkr, graspmor) bajo
duraciones crisp (= punto medio, el Taillard original) y calcula el RE crisp
vs el LB crisp de Taillard. Se compara:
  - La ESCALERA crisp (¿se mantiene v2/gp < heurísticos?).
  - El PRECIO DE LA ROBUSTEZ: RE crisp vs RE intervalo (E[Cmax]) del mismo
    pool — cuánto cuesta haber optimizado el peor caso.
  - CORRELACIÓN de rankings intervalo->crisp (Spearman) dentro del pool: ¿la
    mejor solución en intervalo sigue siendo de las mejores en crisp?

Salida: benchmarks/crisp_transfer.csv + tabla por clase.
"""

import glob
import os
import re
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "transfer_experiment")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from decode import decode_crisp  # noqa: E402
from jobshop_rl.data import PROBLEM_REGISTRY  # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402

GEN = ["graspmor", "gtmwkr", "gp", "v2"]
CLASSES = ["15_15", "20_15", "20_20", "30_15", "30_20", "50_15", "50_20"]


def spearman(xs, ys):
    n = len(xs)
    rx = {v: i for i, v in enumerate(sorted(range(n), key=lambda k: xs[k]))}
    ry = {v: i for i, v in enumerate(sorted(range(n), key=lambda k: ys[k]))}
    d2 = sum((rx[k] - ry[k]) ** 2 for k in range(n))
    return 1 - 6 * d2 / (n * (n * n - 1))


def process(pid, gen, durs, mseq, lb):
    """Devuelve (crisp_best_RE, crisp_mean_RE, interval_mid_RE list, crisp list)."""
    path = f"seeds/{pid}_{gen}_pool.csv"
    if not os.path.exists(path):
        return None
    crisp_re, interval_mid_re = [], []
    for line in open(path, encoding="utf-8"):
        if ";" not in line:
            continue
        perm_s, interval_s = line.strip().split(";")
        seq = [int(x) for x in perm_s.split()]
        lo, up = (float(x) for x in interval_s.strip("[] ").split(","))
        interval_mid_re.append(((lo + up) / 2 - lb) / lb * 100)
        mk = decode_crisp(seq, durs, mseq)
        crisp_re.append((mk - lb) / lb * 100)
    return (min(crisp_re), sum(crisp_re) / len(crisp_re),
            interval_mid_re, crisp_re)


def main():
    instances = sorted({os.path.basename(f).split("_v2_pool")[0]
                        for f in glob.glob("seeds/*_v2_pool.csv")})
    rows = []
    for pid in instances:
        crisp_pid = pid.replace("int__", "")
        # solo Taillard: el crisp es taiJ_M_XX (misma instancia, midpoints).
        # ft10_interval se salta (su crisp es 'ft10', mapeo distinto).
        if not crisp_pid.startswith("tai") or crisp_pid not in PROBLEM_REGISTRY:
            continue
        prob = PROBLEM_REGISTRY[crisp_pid]()
        durs, mseq = prob["durations"], prob["sequences"]
        lb = lb_for_problem_name(pid)
        if lb is None:
            continue
        m = re.search(r"tai(\d+_\d+)", pid)
        rec = {"instance": pid, "cls": m.group(1) if m else "ft10"}
        for g in GEN:
            r = process(pid, g, durs, mseq, lb)
            if r:
                cbest, cmean, imid, clist = r
                rec[f"{g}_crisp_best"] = cbest
                rec[f"{g}_crisp_mean"] = cmean
                rec[f"{g}_int_mean"] = sum(imid) / len(imid)
                rec[f"{g}_spearman"] = spearman(imid, clist)
            else:
                for k in ("crisp_best", "crisp_mean", "int_mean", "spearman"):
                    rec[f"{g}_{k}"] = float("nan")
        rows.append(rec)
        print(".", end="", flush=True)
    print()

    os.makedirs("benchmarks", exist_ok=True)
    with open("benchmarks/crisp_transfer.csv", "w", encoding="utf-8") as f:
        cols = ["instance", "cls"] + [f"{g}_{k}" for g in GEN for k in
                ("crisp_best", "crisp_mean", "int_mean", "spearman")]
        f.write(",".join(cols) + "\n")
        for r in rows:
            f.write(",".join([r["instance"], r["cls"]] +
                    [f"{r[f'{g}_{k}']:.3f}" for g in GEN for k in
                     ("crisp_best", "crisp_mean", "int_mean", "spearman")]) + "\n")

    def avg(rs, key):
        v = [r[key] for r in rs if r[key] == r[key]]
        return sum(v) / len(v) if v else float("nan")

    print("\n=== ESCALERA CRISP: RE del MEJOR individuo (%) por clase ===")
    print("(¿se mantiene el orden v2/gp < heuristicos bajo evaluacion crisp?)")
    hdr = f"{'clase':<7}" + "".join(f"{g[:8]:>10}" for g in GEN)
    print(hdr)
    allr = []
    for c in CLASSES:
        cr = [r for r in rows if r["cls"] == c]; allr += cr
        print(f"{c:<7}" + "".join(f"{avg(cr, f'{g}_crisp_best'):>9.1f}%" for g in GEN))
    print(f"{'GLOBAL':<7}" + "".join(f"{avg(allr, f'{g}_crisp_best'):>9.1f}%" for g in GEN))

    print("\n=== PRECIO DE LA ROBUSTEZ: RE crisp - RE intervalo (media pool) ===")
    print("(positivo = optimizar peor caso cuesta calidad puntual crisp)")
    print(f"{'clase':<7}" + "".join(f"{g[:8]:>10}" for g in GEN))
    for c in CLASSES:
        cr = [r for r in rows if r["cls"] == c]
        print(f"{c:<7}" + "".join(
            f"{avg(cr, f'{g}_crisp_mean')-avg(cr, f'{g}_int_mean'):>+9.2f} " for g in GEN))
    print(f"{'GLOBAL':<7}" + "".join(
        f"{avg(allr, f'{g}_crisp_mean')-avg(allr, f'{g}_int_mean'):>+9.2f} " for g in GEN))

    print("\n=== CORRELACION ranking intervalo->crisp (Spearman medio) ===")
    print("(1 = la mejor en intervalo sigue siendo la mejor en crisp)")
    print(f"{'clase':<7}" + "".join(f"{g[:8]:>10}" for g in GEN))
    for c in CLASSES:
        cr = [r for r in rows if r["cls"] == c]
        print(f"{c:<7}" + "".join(f"{avg(cr, f'{g}_spearman'):>10.3f}" for g in GEN))
    print(f"{'GLOBAL':<7}" + "".join(f"{avg(allr, f'{g}_spearman'):>10.3f}" for g in GEN))
    print("\nCSV: benchmarks/crisp_transfer.csv")


if __name__ == "__main__":
    main()
