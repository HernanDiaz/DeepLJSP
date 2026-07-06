"""
Compara los pools v2 (best-of-1024 constructivo) con los resultados
publicados por instancia (suplemento Diaz et al.: fEABC y TS-N2, Best/Avg
RE% de 30 runs) sobre las 70 Taillard.

Lee benchmarks/pools_analysis.csv (generado por analyze_pools.py).
"""

import csv
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# RE(%) publicados por instancia TA1..TA70 (suplemento del usuario)
FEABC_BEST = [4.71,2.65,3.65,4.38,3.19,3.39,2.81,2.55,4.47,3.14,
              6.26,4.46,6.26,3.75,5.94,7.02,5.75,9.40,8.52,4.97,
              6.52,8.65,10.01,5.14,9.27,10.50,8.57,6.46,7.99,9.75,
              6.01,10.68,9.40,8.23,1.47,7.94,8.16,8.52,6.13,11.18,
              17.58,14.15,16.06,11.88,6.99,13.00,16.55,11.90,11.08,16.56,
              5.51,4.03,3.66,0.63,6.01,3.25,1.63,3.08,5.63,4.43,
              6.76,9.41,7.64,6.94,8.42,6.80,6.50,6.66,5.08,8.43]
FEABC_AVG = [6.73,4.20,5.63,6.99,4.89,5.61,4.86,5.41,8.25,6.16,
             9.37,5.99,8.88,5.02,8.53,8.98,8.72,11.79,11.36,8.09,
             8.07,10.53,11.56,7.47,10.97,13.05,10.42,8.21,10.21,12.22,
             8.78,13.07,11.71,9.63,3.25,9.63,9.70,10.65,8.35,13.42,
             20.55,17.45,18.13,14.41,9.45,15.91,20.44,13.90,13.19,20.36,
             7.20,5.93,5.40,2.96,8.44,5.04,3.61,4.94,7.50,6.07,
             8.84,11.74,9.19,8.36,9.98,8.56,8.95,8.01,6.59,9.91]
TS_BEST = [1.26,0.24,1.35,0.34,1.06,1.29,0.61,1.15,2.35,0.24,
           2.76,1.57,2.38,0.45,2.43,1.95,1.92,3.70,1.99,2.15,
           2.38,4.16,4.45,1.43,5.10,6.66,3.93,2.18,4.36,5.99,
           1.02,4.17,3.75,3.39,0.00,1.29,2.88,3.17,1.45,4.18,
           9.68,6.58,5.67,4.72,2.70,6.87,9.91,6.15,5.00,9.22,
           0.00,0.00,0.04,0.00,0.34,0.11,0.00,0.69,0.45,0.11,
           0.47,3.66,0.45,0.59,1.19,1.20,1.08,0.29,0.00,1.59]
TS_AVG = [1.85,1.65,2.34,1.31,2.22,1.97,1.77,2.37,2.73,2.23,
          4.11,2.21,3.91,1.82,3.96,3.28,3.14,5.23,4.54,3.54,
          3.75,5.88,5.80,2.86,6.50,8.02,5.08,3.27,5.10,7.13,
          1.97,5.32,4.61,4.73,0.26,2.82,3.85,4.35,2.67,6.17,
          12.12,8.36,8.72,6.86,4.17,8.69,11.53,7.87,6.49,11.43,
          0.02,0.10,0.04,0.02,0.87,0.27,0.03,0.69,0.75,0.41,
          1.83,5.02,1.69,1.44,2.12,2.05,2.30,1.10,0.12,2.53]

CLASSES = [("15x15", 0), ("20x15", 10), ("20x20", 20), ("30x15", 30),
           ("30x20", 40), ("50x15", 50), ("50x20", 60)]

# Leer análisis de pools
v2_best = {}
with open("benchmarks/pools_analysis.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row["ta"].startswith("TA"):
            v2_best[int(row["ta"][2:])] = float(row["v2_best_re"])

print(f"{'Clase':<7} {'v2 best-1024':>12} {'fEABC best':>10} {'fEABC avg':>10} "
      f"{'TS-N2 best':>10} {'TS-N2 avg':>10}")
print("-" * 65)
gap_feabc_avg = []
for name, off in CLASSES:
    idx = range(off, off + 10)
    v2 = sum(v2_best[i + 1] for i in idx) / 10
    fb = sum(FEABC_BEST[i] for i in idx) / 10
    fa = sum(FEABC_AVG[i] for i in idx) / 10
    tb = sum(TS_BEST[i] for i in idx) / 10
    ta = sum(TS_AVG[i] for i in idx) / 10
    gap_feabc_avg.append(v2 - fa)
    print(f"{name:<7} {v2:>11.1f}% {fb:>9.2f}% {fa:>9.2f}% {tb:>9.2f}% {ta:>9.2f}%")

# Conteos por instancia
wins_fa = sum(1 for i in range(70) if v2_best[i + 1] < FEABC_AVG[i])
wins_fb = sum(1 for i in range(70) if v2_best[i + 1] < FEABC_BEST[i])
close_fa = sum(1 for i in range(70) if v2_best[i + 1] < FEABC_AVG[i] + 2.0)

print("-" * 65)
print(f"v2 best-of-1024 mejor que fEABC Avg: {wins_fa}/70 instancias")
print(f"v2 best-of-1024 mejor que fEABC Best: {wins_fb}/70 instancias")
print(f"v2 a menos de 2 puntos del fEABC Avg: {close_fa}/70 instancias")
print(f"Gap medio v2-best vs fEABC-avg por clase: "
      f"{', '.join(f'{g:+.1f}' for g in gap_feabc_avg)}")
