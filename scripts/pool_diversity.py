"""
Diversidad de los pools de siembra por generador.

Para sembrar una población, además de la calidad importa la variedad: un pool
de clones acelera la convergencia prematura. Tres métricas por pool:

  1. unicidad   = fracción de permutaciones DISTINTAS (1 = sin duplicados)
  2. sigma_RE   = desviación típica del RE dentro del pool (dispersión de
                  CALIDAD; alta = mezcla de buenas y malas)
  3. dist_estr  = distancia estructural media entre pares (fracción de
                  posiciones en las que dos secuencias de despacho difieren;
                  0 = idénticas, ~1 = muy distintas). Muestreada por pares.

Salida: benchmarks/pool_diversity.csv + tabla por clase.
"""

import glob
import os
import random
import re
import sys

sys.path.insert(0, ".")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data.literature_bounds import lb_for_problem_name, ta_name  # noqa

FT10_LB = 930
GENERATORS = ["graspmor", "gtmwkr", "gp", "v2"]
N_PAIRS = 400  # pares muestreados para la distancia estructural
rng = random.Random(0)


def read_pool(path):
    perms, mids = [], []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or ";" not in line:
            continue
        perm, interval = line.split(";")
        lo, up = (float(x) for x in interval.strip("[] ").split(","))
        perms.append(perm.strip())
        mids.append((lo + up) / 2.0)
    return perms, mids


def struct_dist(perms):
    """Distancia estructural media (desacuerdo posicional) entre pares."""
    n = len(perms)
    if n < 2:
        return float("nan")
    tot = 0.0
    for _ in range(N_PAIRS):
        a, b = rng.randrange(n), rng.randrange(n)
        if a == b:
            b = (b + 1) % n
        pa, pb = perms[a].split(), perms[b].split()
        L = min(len(pa), len(pb))
        if L == 0:
            continue
        diff = sum(1 for i in range(L) if pa[i] != pb[i])
        tot += diff / L
    return tot / N_PAIRS


def diversity(path, lb):
    perms, mids = read_pool(path)
    if not perms:
        return None
    n = len(perms)
    uniq = len(set(perms)) / n
    res = [(m - lb) / lb * 100 for m in mids]
    mean = sum(res) / n
    sigma = (sum((x - mean) ** 2 for x in res) / n) ** 0.5
    return uniq, sigma, struct_dist(perms)


def instance_lb(pid):
    if pid.startswith("ft10"):
        return FT10_LB
    return lb_for_problem_name(pid)


def main():
    instances = sorted({os.path.basename(f).split("_v2_pool")[0]
                        for f in glob.glob("seeds/*_v2_pool.csv")})
    rows = []
    for pid in instances:
        lb = instance_lb(pid)
        m = re.search(r"tai(\d+_\d+)", pid)
        rec = {"instance": pid, "cls": m.group(1) if m else "ft10"}
        for g in GENERATORS:
            path = f"seeds/{pid}_{g}_pool.csv"
            d = diversity(path, lb) if os.path.exists(path) else None
            rec[g] = d if d else (float("nan"),) * 3
        rows.append(rec)

    os.makedirs("benchmarks", exist_ok=True)
    with open("benchmarks/pool_diversity.csv", "w", encoding="utf-8") as f:
        f.write("instance," + ",".join(f"{g}_{s}" for g in GENERATORS
                for s in ("uniq", "sigmaRE", "structdist")) + "\n")
        for r in rows:
            f.write(r["instance"] + "," + ",".join(
                f"{r[g][k]:.4f}" for g in GENERATORS for k in range(3)) + "\n")

    def avg(rs, g, k):
        vals = [r[g][k] for r in rs if r[g][k] == r[g][k]]
        return sum(vals) / len(vals) if vals else float("nan")

    for k, (nombre, unidad) in enumerate([
            ("UNICIDAD (fracción de perms distintas; 1 = sin duplicados)", ""),
            ("SIGMA_RE (dispersión de calidad dentro del pool, en puntos)", ""),
            ("DIST. ESTRUCTURAL (desacuerdo posicional medio entre pares)", "")]):
        print(f"\n=== {nombre} ===")
        hdr = f"{'Clase':<8}" + "".join(f"{g[:8]:>10}" for g in GENERATORS)
        print(hdr); print("-" * len(hdr))
        classes = sorted({r["cls"] for r in rows}, key=lambda c: (len(c), c))
        allr = []
        for cls in classes:
            cr = [r for r in rows if r["cls"] == cls]
            allr += cr
            print(f"{cls:<8}" + "".join(f"{avg(cr, g, k):>10.3f}"
                                        for g in GENERATORS))
        print("-" * len(hdr))
        print(f"{'GLOBAL':<8}" + "".join(f"{avg(allr, g, k):>10.3f}"
                                         for g in GENERATORS))
    print("\nCSV: benchmarks/pool_diversity.csv")


if __name__ == "__main__":
    main()
