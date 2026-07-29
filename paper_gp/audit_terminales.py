# -*- coding: utf-8 -*-
"""Como esta marcado cada nombre de terminal a lo largo del manuscrito.

Interesa saber si el mismo nombre (PT, WKR, ...) se compone unas veces con
\\mathit, otras con \\textit y otras en redonda, porque entonces el lector ve
tres cosas distintas para una sola.
"""
import collections
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TERMS = ["PTW", "PT", "ESTW", "EST", "WKRW", "WKR", "NOR", "SLACK", "ONE"]
lines = open("paper_gp/main.tex", encoding="utf-8").read().split("\n")

MARCA = re.compile(
    r"\\(mathit|textit|emph|mathrm|texttt)\{\s*(" + "|".join(TERMS) + r")\s*\}")

cnt = collections.Counter()
donde = collections.defaultdict(list)
for i, ln in enumerate(lines, 1):
    if ln.lstrip().startswith("%"):
        continue
    for m in MARCA.finditer(ln):
        cnt[(m.group(2), "\\" + m.group(1))] += 1
        donde[(m.group(2), "\\" + m.group(1))].append(i)

print(f"{'terminal':<8}{'marca':<10}{'n':<5}lineas")
for (k, mk), n in sorted(cnt.items()):
    ls = donde[(k, mk)]
    print(f"{k:<8}{mk:<10}{n:<5}{ls[:8]}")

print("\n=== por terminal: cuantas marcas distintas ===")
por = collections.defaultdict(set)
for (k, mk) in cnt:
    por[k].add(mk)
for k in TERMS:
    if por[k]:
        aviso = "  <-- MEZCLA" if len(por[k]) > 1 else ""
        print(f"{k:<8}{sorted(por[k])}{aviso}")
