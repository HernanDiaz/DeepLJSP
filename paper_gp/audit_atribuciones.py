# -*- coding: utf-8 -*-
"""Cosas que el paper NOMBRA o USA sin citarlas.

No propone lecturas: busca en el manuscrito los nombres de benchmarks,
herramientas y familias de instancias, y comprueba que haya una cita cerca de
la mencion. Es atribucion, no relleno; y con que la entrada exista en refs.bib
no basta, porque el acronimo del texto no suele estar en el titulo (GRASP
frente a 'Greedy randomized adaptive search procedures').

Uso: python paper_gp/audit_atribuciones.py
"""

import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
VENTANA = 260          # caracteres alrededor de la mencion donde vale la cita

tex = open(os.path.join(HERE, "main.tex"), encoding="utf-8").read()

# (que usa el paper, como aparece en el tex, hace falta cita?)
COSAS = [
    ("Taillard (benchmark)", r"Taillard", True),
    ("irace (herramienta)", r"\birace\b", True),
    ("Fisher y Thompson (FT10/FT20)", r"\bFT10\b", True),
    ("Lawrence (familia La)", r"instances of the La\s*\n?family", True),
    ("Adams-Balas-Zawack (ABZ)", r"ABZ7--9", True),
    ("Giffler y Thompson", r"Giffler and\s*\n?Thompson", True),
    ("GRASP", r"GRASP", True),
    ("Wilcoxon", r"Wilcoxon", False),
    ("Monte Carlo", r"Monte Carlo", False),
]

print(f"{'usa el paper':<32}{'menciones':>10}{'con cita cerca':>16}")
mal = 0
for nombre, pat, obligatoria in COSAS:
    pos = [m.start() for m in re.finditer(pat, tex)]
    if not pos:
        print(f"{nombre:<32}{'0':>10}{'':>16}  (no aparece)")
        continue
    con = sum(1 for p in pos
              if re.search(r"\\cite\{", tex[max(0, p - VENTANA):p + VENTANA]))
    marca = ""
    if obligatoria and con == 0:
        marca = "  <-- SIN ATRIBUIR"
        mal += 1
    elif not obligatoria and con == 0:
        marca = "  (opcional)"
    print(f"{nombre:<32}{len(pos):>10}{con:>16}{marca}")

claves = set(re.findall(r"@\w+\{([^,]+),",
                        open(os.path.join(HERE, "refs.bib"),
                             encoding="utf-8").read()))
print(f"\n{len(claves)} referencias en refs.bib")
if mal:
    print(f"FALLA: {mal} atribucion(es) obligatoria(s) sin cita cerca.")
else:
    print("OK: todo lo que el paper usa por su nombre lleva cita.")
sys.exit(1 if mal else 0)
