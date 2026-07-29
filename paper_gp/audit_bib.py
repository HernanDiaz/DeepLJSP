# -*- coding: utf-8 -*-
"""Auditoria de refs.bib y de su uso en main.tex.

Comprueba lo comprobable sin salir del repositorio: entradas citadas que no
existen, entradas que existen y no se citan, campos que faltan, y claves con
pinta de marcador provisional.
"""
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

tex = open("paper_gp/main.tex", encoding="utf-8").read()
bib = open("paper_gp/refs.bib", encoding="utf-8").read()

entradas = {}
for m in re.finditer(r"@(\w+)\{([^,]+),(.*?)\n\}", bib, re.S):
    entradas[m.group(2).strip()] = (m.group(1).lower(), m.group(3))

citadas = Counter()
for m in re.finditer(r"\\cite\{([^}]*)\}", tex):
    for k in m.group(1).split(","):
        citadas[k.strip()] += 1

print(f"{len(entradas)} entradas en refs.bib, {len(citadas)} claves citadas, "
      f"{sum(citadas.values())} citas en total\n")

faltan = [k for k in citadas if k not in entradas]
print(f"citadas y ausentes de refs.bib: {faltan or 'ninguna'}")
sobran = [k for k in entradas if k not in citadas]
print(f"en refs.bib y nunca citadas: {sobran or 'ninguna'}")

print("\n=== campos que faltan ===")
OBLIG = {"article": ["author", "title", "journal", "year"],
         "inproceedings": ["author", "title", "booktitle", "year"],
         "book": ["author", "title", "publisher", "year"],
         "incollection": ["author", "title", "booktitle", "year"],
         "misc": ["author", "title", "year"]}
for k in sorted(entradas):
    tipo, cuerpo = entradas[k]
    for campo in OBLIG.get(tipo, ["author", "title", "year"]):
        if not re.search(r"\b" + campo + r"\s*=", cuerpo):
            print(f"  {k} ({tipo}): sin '{campo}'")

print("\n=== claves con pinta de provisional ===")
for k in sorted(entradas):
    if not re.match(r"^[A-Z][A-Za-z]*\d{4}[A-Za-z0-9]*$", k):
        print(f"  {k}   (el resto sigue Autor+anyo)")

print("\n=== las mas citadas ===")
for k, n in citadas.most_common(6):
    tipo, cuerpo = entradas.get(k, ("?", ""))
    ano = re.search(r"year\s*=\s*\{?(\d{4})", cuerpo)
    print(f"  {n}x  {k:<24} {tipo:<14} {ano.group(1) if ano else '?'}")
