# -*- coding: utf-8 -*-
"""'Both curves have a single broad minimum': lo tienen?

Las evaluaciones son deterministas (un rollout por instancia, 70 instancias),
asi que la rugosidad que se vea no es ruido de repeticion: es la forma real de
la curva.
"""
import collections
import csv
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

d = collections.defaultdict(list)
for r in csv.DictReader(open("benchmarks/coefficient_sweep.csv", encoding="utf-8")):
    d[r["coef"]].append((float(r["value"]), float(r["re"])))

for coef, pts in d.items():
    pts.sort()
    xs = [x for x, _ in pts]
    ys = [y for _, y in pts]
    gi = ys.index(min(ys))
    print(f"\n=== {coef} ===")
    print(f"minimo global: {coef}={xs[gi]} con RE={ys[gi]:.4f}")
    locales = [(xs[i], ys[i]) for i in range(1, len(ys) - 1)
               if ys[i] < ys[i - 1] and ys[i] < ys[i + 1]]
    print(f"minimos locales interiores ({len(locales)}): "
          + ", ".join(f"{x}->{y:.2f}" for x, y in locales))
    # cuantas veces cambia el sentido de la pendiente
    signos = [1 if ys[i + 1] > ys[i] else -1 for i in range(len(ys) - 1)]
    cambios = sum(1 for i in range(1, len(signos)) if signos[i] != signos[i - 1])
    print(f"cambios de pendiente: {cambios} sobre {len(signos)} tramos")
    if len(locales) > 1:
        seg = sorted(locales, key=lambda t: t[1])[1]
        print(f"  el 2o minimo local esta en {seg[0]} con {seg[1]:.2f}, "
              f"a {seg[1] - min(ys):.2f} puntos del global")
        print("  -> NO es 'un solo minimo'")
