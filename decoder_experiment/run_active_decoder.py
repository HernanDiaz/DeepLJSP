"""
EXPERIMENTO: ¿mejora el RE al decodificar las semillas con un SGS ACTIVO por
inserción en vez del semiactivo?

Re-decodifica las mismas secuencias de los pools con el decodificador activo
(crisp) y compara el RE crisp activo vs el RE crisp semiactivo (baseline). Se
mide, por generador y clase:
  - RE semiactivo vs activo (mejor individuo y media del pool).
  - Mejora media (puntos de RE) y % de soluciones que mejoran.
  - ¿se conserva la escalera / el ranking (Spearman)?

Aislado en decoder_experiment/. Aritmética crisp (gap-fitting inequívoco);
la versión intervalo queda como extensión.

Salida: benchmarks/active_decoder.csv + tabla por clase.
"""

import glob
import os
import re
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "decoder_experiment")
sys.path.insert(0, "transfer_experiment")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from active_decode import decode_active            # noqa: E402
from decode import decode_crisp                    # noqa: E402  (semiactivo)
from jobshop_rl.data import PROBLEM_REGISTRY        # noqa: E402
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
    path = f"seeds/{pid}_{gen}_pool.csv"
    if not os.path.exists(path):
        return None
    semi, act = [], []
    for line in open(path, encoding="utf-8"):
        if ";" not in line:
            continue
        seq = [int(x) for x in line.split(";")[0].split()]
        semi.append((decode_crisp(seq, durs, mseq) - lb) / lb * 100)
        act.append((decode_active(seq, durs, mseq) - lb) / lb * 100)
    n_better = sum(1 for a, s in zip(act, semi) if a < s - 1e-9)
    return {
        "semi_best": min(semi), "semi_mean": sum(semi) / len(semi),
        "act_best": min(act), "act_mean": sum(act) / len(act),
        "improve_mean": sum(s - a for s, a in zip(semi, act)) / len(semi),
        "pct_better": 100.0 * n_better / len(semi),
        "spearman": spearman(semi, act),
    }


def main():
    instances = sorted({os.path.basename(f).split("_v2_pool")[0]
                        for f in glob.glob("seeds/*_v2_pool.csv")})
    rows = []
    for pid in instances:
        crisp_pid = pid.replace("int__", "")
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
            for k in ("semi_best", "semi_mean", "act_best", "act_mean",
                      "improve_mean", "pct_better", "spearman"):
                rec[f"{g}_{k}"] = r[k] if r else float("nan")
        rows.append(rec)
        print(".", end="", flush=True)
    print()

    keys = ("semi_best", "semi_mean", "act_best", "act_mean",
            "improve_mean", "pct_better", "spearman")
    os.makedirs("benchmarks", exist_ok=True)
    with open("benchmarks/active_decoder.csv", "w", encoding="utf-8") as f:
        f.write("instance,cls," + ",".join(f"{g}_{k}" for g in GEN for k in keys) + "\n")
        for r in rows:
            f.write(f"{r['instance']},{r['cls']}," + ",".join(
                f"{r[f'{g}_{k}']:.3f}" for g in GEN for k in keys) + "\n")

    def avg(k):
        v = [r[k] for r in rows if r[k] == r[k]]
        return sum(v) / len(v) if v else float("nan")

    print("\n=== MEJOR individuo: RE semiactivo -> activo (global) ===")
    for g in GEN:
        print(f"  {g:<10}: {avg(f'{g}_semi_best'):5.1f}%  ->  "
              f"{avg(f'{g}_act_best'):5.1f}%   (Δ {avg(f'{g}_semi_best')-avg(f'{g}_act_best'):+.2f})")

    print("\n=== Mejora media del pool (pts de RE) y % de soluciones que mejoran ===")
    print(f"{'generador':<10}{'Δ media pool':>14}{'% mejoran':>12}{'Spearman':>11}")
    for g in GEN:
        print(f"{g:<10}{avg(f'{g}_improve_mean'):>13.2f} {avg(f'{g}_pct_better'):>11.1f}%"
              f"{avg(f'{g}_spearman'):>11.3f}")

    print("\n=== Mejora del MEJOR individuo por clase (Δ RE, v2) ===")
    for c in CLASSES:
        cr = [r for r in rows if r["cls"] == c]
        sb = sum(r["v2_semi_best"] for r in cr) / len(cr)
        ab = sum(r["v2_act_best"] for r in cr) / len(cr)
        print(f"  {c:<7} semi {sb:5.1f}% -> activo {ab:5.1f}%  (Δ {sb-ab:+.2f})")
    print("\nCSV: benchmarks/active_decoder.csv")


if __name__ == "__main__":
    main()
