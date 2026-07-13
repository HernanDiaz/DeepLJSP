"""
EXPERIMENTO DE TRANSFERENCIA A FUZZY (triangular) — Mitad A.

TFN por operación = (lower_intervalo, valor_crisp, upper_intervalo): soporte =
el intervalo, modal = el valor crisp (Taillard original). Es el TFN natural
del intervalo con su valor más probable en el centro — sin spread arbitrario.

Re-decodifica los pools de intervalo bajo aritmética fuzzy (suma/max de TFNs)
y mide el RE del valor esperado E[C]=(A+2B+C)/4 vs el LB crisp. Reporta la
escalera, el precio de robustez (fuzzy vs intervalo) y la correlación de
rankings intervalo->fuzzy.

Salida: benchmarks/fuzzy_transfer.csv + tabla por clase.
"""

import glob
import os
import re
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "transfer_experiment")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from decode import decode_tfn, _tfn_expected  # noqa: E402
from jobshop_rl.data import PROBLEM_REGISTRY  # noqa: E402
from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402
from jobshop_rl.models.interval import Interval  # noqa: E402

GEN = ["graspmor", "gtmwkr", "gp", "v2"]
CLASSES = ["15_15", "20_15", "20_20", "30_15", "30_20", "50_15", "50_20"]


def spearman(xs, ys):
    n = len(xs)
    rx = {v: i for i, v in enumerate(sorted(range(n), key=lambda k: xs[k]))}
    ry = {v: i for i, v in enumerate(sorted(range(n), key=lambda k: ys[k]))}
    d2 = sum((rx[k] - ry[k]) ** 2 for k in range(n))
    return 1 - 6 * d2 / (n * (n * n - 1))


def build_tfn(int_durs, crisp_durs):
    """TFN[j][k] = (lo_intervalo, valor_crisp, up_intervalo)."""
    tfn = []
    for j, row in enumerate(int_durs):
        tr = []
        for k, d in enumerate(row):
            lo = float(d.lower) if isinstance(d, Interval) else float(d)
            up = float(d.upper) if isinstance(d, Interval) else float(d)
            b = float(crisp_durs[j][k])
            tr.append((lo, b, up))
        tfn.append(tr)
    return tfn


def process(pid, gen, tfn, mseq, lb):
    path = f"seeds/{pid}_{gen}_pool.csv"
    if not os.path.exists(path):
        return None
    fuzzy_re, interval_mid_re = [], []
    for line in open(path, encoding="utf-8"):
        if ";" not in line:
            continue
        perm_s, interval_s = line.strip().split(";")
        seq = [int(x) for x in perm_s.split()]
        lo, up = (float(x) for x in interval_s.strip("[] ").split(","))
        interval_mid_re.append(((lo + up) / 2 - lb) / lb * 100)
        mk = decode_tfn(seq, tfn, mseq)
        fuzzy_re.append((_tfn_expected(mk) - lb) / lb * 100)
    return (min(fuzzy_re), sum(fuzzy_re) / len(fuzzy_re),
            interval_mid_re, fuzzy_re)


def main():
    instances = sorted({os.path.basename(f).split("_v2_pool")[0]
                        for f in glob.glob("seeds/*_v2_pool.csv")})
    rows = []
    for pid in instances:
        crisp_pid = pid.replace("int__", "")
        if not crisp_pid.startswith("tai") or crisp_pid not in PROBLEM_REGISTRY:
            continue
        int_durs = PROBLEM_REGISTRY[pid]()["durations"]
        crisp = PROBLEM_REGISTRY[crisp_pid]()
        tfn = build_tfn(int_durs, crisp["durations"])
        mseq = crisp["sequences"]
        lb = lb_for_problem_name(pid)
        if lb is None:
            continue
        m = re.search(r"tai(\d+_\d+)", pid)
        rec = {"instance": pid, "cls": m.group(1) if m else "ft10"}
        for g in GEN:
            r = process(pid, g, tfn, mseq, lb)
            if r:
                fb, fm, imid, flist = r
                rec[f"{g}_fuzzy_best"] = fb
                rec[f"{g}_fuzzy_mean"] = fm
                rec[f"{g}_int_mean"] = sum(imid) / len(imid)
                rec[f"{g}_spearman"] = spearman(imid, flist)
            else:
                for k in ("fuzzy_best", "fuzzy_mean", "int_mean", "spearman"):
                    rec[f"{g}_{k}"] = float("nan")
        rows.append(rec)
        print(".", end="", flush=True)
    print()

    os.makedirs("benchmarks", exist_ok=True)
    with open("benchmarks/fuzzy_transfer.csv", "w", encoding="utf-8") as f:
        cols = ["instance", "cls"] + [f"{g}_{k}" for g in GEN for k in
                ("fuzzy_best", "fuzzy_mean", "int_mean", "spearman")]
        f.write(",".join(cols) + "\n")
        for r in rows:
            f.write(",".join([r["instance"], r["cls"]] +
                    [f"{r[f'{g}_{k}']:.3f}" for g in GEN for k in
                     ("fuzzy_best", "fuzzy_mean", "int_mean", "spearman")]) + "\n")

    def avg(rs, key):
        v = [r[key] for r in rs if r[key] == r[key]]
        return sum(v) / len(v) if v else float("nan")

    print("\n=== ESCALERA FUZZY: RE del MEJOR (E[C]) por clase (%) ===")
    hdr = f"{'clase':<7}" + "".join(f"{g[:8]:>10}" for g in GEN)
    print(hdr)
    allr = []
    for c in CLASSES:
        cr = [r for r in rows if r["cls"] == c]; allr += cr
        print(f"{c:<7}" + "".join(f"{avg(cr, f'{g}_fuzzy_best'):>9.1f}%" for g in GEN))
    print(f"{'GLOBAL':<7}" + "".join(f"{avg(allr, f'{g}_fuzzy_best'):>9.1f}%" for g in GEN))

    print("\n=== PRECIO DE ROBUSTEZ: RE fuzzy - RE intervalo (media pool) ===")
    print(f"{'clase':<7}" + "".join(f"{g[:8]:>10}" for g in GEN))
    for c in CLASSES:
        cr = [r for r in rows if r["cls"] == c]
        print(f"{c:<7}" + "".join(
            f"{avg(cr, f'{g}_fuzzy_mean')-avg(cr, f'{g}_int_mean'):>+9.2f} " for g in GEN))
    print(f"{'GLOBAL':<7}" + "".join(
        f"{avg(allr, f'{g}_fuzzy_mean')-avg(allr, f'{g}_int_mean'):>+9.2f} " for g in GEN))

    print("\n=== CORRELACION ranking intervalo->fuzzy (Spearman medio) ===")
    print(f"{'clase':<7}" + "".join(f"{g[:8]:>10}" for g in GEN))
    for c in CLASSES:
        cr = [r for r in rows if r["cls"] == c]
        print(f"{c:<7}" + "".join(f"{avg(cr, f'{g}_spearman'):>10.3f}" for g in GEN))
    print(f"{'GLOBAL':<7}" + "".join(f"{avg(allr, f'{g}_spearman'):>10.3f}" for g in GEN))
    print("\nCSV: benchmarks/fuzzy_transfer.csv")


if __name__ == "__main__":
    main()
