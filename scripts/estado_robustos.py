# -*- coding: utf-8 -*-
"""Cuantas tiradas del reentrenamiento robusto van hechas."""
import glob
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BRAZOS = ["v2-robust-lam0p5-fix", "v2-robust-lam1-fix",
          "v2-robust-lam2-fix", "v2-robust-lam4-fix"]
SEMILLAS = range(2, 12)

total = hechas = 0
for tag in BRAZOS:
    n = 0
    for s in SEMILLAS:
        total += 1
        if any(os.path.exists(os.path.join(d, "best_model.pt"))
               for d in glob.glob(f"outputs/bench_{tag}__*_seed{s}")):
            n += 1
    hechas += n
    print(f"  {tag:24s} {n:2d}/10")
print(f"\n  total {hechas}/{total}")
if os.path.exists("logs/PARAR_ROBFIX.txt"):
    print("  AVISO: PARAR_ROBFIX.txt presente; los carriles saldran al "
          "terminar su tirada")
vivos = 0
for f in glob.glob("logs/robfix_*.log"):
    pass
print(f"  marcadores de fin: {len(glob.glob('logs/robfix_*_done.txt'))}/6")
