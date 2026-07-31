# -*- coding: utf-8 -*-
"""Tests pareados por instancia: politica frente a MOR y G&T-MWKR.

Wilcoxon de rangos con signo sobre los 70 pares de RE por instancia, con
la correlacion biserial de rangos de pares emparejados como tamano de
efecto -- el mismo aparato estadistico del paper del GP. Usa la politica
greedy (benchmarks/fair_v2_greedy.csv, media de los 3 checkpoints) y,
si benchmarks/eval_fair_bo1024.csv ya existe y esta completo, tambien el
best-of-1024 (mejor mid_comp por instancia entre los checkpoints).

    python scripts/stats_policy.py
"""
import csv
import os
import sys
from collections import defaultdict

from scipy import stats

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def carga_baselines():
    """{TA: (lb, MOR_re, GT_re)} y el mapa instancia->TA."""
    filas = {}
    for r in csv.DictReader(open("benchmarks/constructive_per_instance.csv",
                                 encoding="utf-8")):
        filas[r["ta"]] = (float(r["lb"]), float(r["MOR_re"]),
                          float(r["GT-MWKR_re"]))
    return filas


TA_BASE = {"15_15": 0, "20_15": 10, "20_20": 20, "30_15": 30,
           "30_20": 40, "50_15": 50, "50_20": 60}


def ta_de(nombre):
    import re as _re
    m = _re.search(r"tai(\d+_\d+)_(\d+)", nombre.lower())
    return f"TA{TA_BASE[m.group(1)] + int(m.group(2))}"


def politica_greedy():
    """{TA: RE medio de los 3 checkpoints (greedy)}."""
    acum = defaultdict(list)
    for r in csv.DictReader(open("benchmarks/fair_v2_greedy.csv",
                                 encoding="utf-8")):
        acum[ta_de(r["instance"])].append(float(r["re_mid"]))
    return {ta: sum(v) / len(v) for ta, v in acum.items()}


def politica_bo1024():
    p = "benchmarks/eval_fair_bo1024.csv"
    if not os.path.exists(p):
        return None
    mejor = defaultdict(list)
    for r in csv.DictReader(open(p, encoding="utf-8")):
        mejor[ta_de(r["instance"])].append(float(r["re_comp"]))
    if len(mejor) < 70:
        print(f"(bo1024 incompleto: {len(mejor)}/70 instancias; se omite)")
        return None
    return {ta: min(v) for ta, v in mejor.items()}


def test(nombre, politica, base_idx, baselines):
    pares = [(politica[ta], baselines[ta][base_idx])
             for ta in sorted(politica) if ta in baselines]
    d = [b - a for a, b in pares]          # positivo = la politica gana
    stat, p = stats.wilcoxon(d)
    n = len(d)
    rangos = stats.rankdata([abs(x) for x in d])
    w_pos = sum(r for r, x in zip(rangos, d) if x > 0)
    w_neg = sum(r for r, x in zip(rangos, d) if x < 0)
    rb = (w_pos - w_neg) / (w_pos + w_neg)
    gana = sum(x > 0 for x in d)
    print(f"  {nombre}: n={n}, gana {gana}/{n}, "
          f"mediana delta={sorted(d)[n // 2]:+.2f} pts, "
          f"W={stat:.0f}, p={p:.2e}, r_rb={rb:+.3f}")


def main():
    baselines = carga_baselines()
    print("== politica greedy (media de 3 checkpoints) ==")
    g = politica_greedy()
    test("vs MOR    ", g, 1, baselines)
    test("vs G&T-MWKR", g, 2, baselines)
    bo = politica_bo1024()
    if bo:
        print("== politica best-of-1024 (mejor por instancia) ==")
        test("vs MOR    ", bo, 1, baselines)
        test("vs G&T-MWKR", bo, 2, baselines)
        media = sum(bo.values()) / len(bo)
        print(f"  RE medio bo1024 sobre las 70: {media:.2f}%")


if __name__ == "__main__":
    main()
