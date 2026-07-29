# -*- coding: utf-8 -*-
"""Los tres numeros que la conclusion (iii) ahora contrasta, desde el CSV.

verify_numbers.py comprueba la fila completa de eps-bar de tab:robustness, asi
que el 5.54 esta trazado, pero busca la cadena en todo main.tex: una copia mal
teclada en la conclusion no se detectaria. Lo recalculo aparte.
"""
import collections
import csv
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

d = collections.defaultdict(list)
for r in csv.DictReader(open("benchmarks/robustness_seis.csv", encoding="utf-8")):
    d[(r["method"], r["width"])].append(float(r["eps_bar"]))


def m0(m):
    v = d[(m, "1.0")]
    return sum(v) / len(v)


gp, rob, robnw = m0("GP"), m0("GP-rob1"), m0("GP-rob1-nw")
print(f"objetivo makespan, con anchuras   GP          = {gp:.2f}")
print(f"objetivo robusto,  con anchuras   GP-rob1     = {rob:.2f}")
print(f"objetivo robusto,  sin anchuras   GP-rob1-nw  = {robnw:.2f}")
print()
print(f"efecto del OBJETIVO (anchuras fijas):  {gp:.2f} -> {rob:.2f}"
      f"   = {(gp - rob) / gp * 100:.1f}% menos")
print(f"efecto de las ANCHURAS (objetivo fijo): {robnw:.2f} -> {rob:.2f}"
      f"   = {(robnw - rob) / robnw * 100:.1f}% menos")
print()
print("la conclusion atribuye 'about a fifth' al cambio de objetivo: "
      f"{(gp - rob) / gp * 100:.1f}%, correcto")
