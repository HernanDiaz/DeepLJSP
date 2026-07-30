# -*- coding: utf-8 -*-
"""Tamano EFECTIVO de la fuente de cada figura, tal como se imprime.

No basta con mirar el font.size del script: si una figura se genera a 6.4 in y
se incluye a 0.8\\linewidth (288 pt = 3.99 in), LaTeX la reduce y las letras se
imprimen encogidas en la misma proporcion. Los fontsize= fijados a mano en
leyendas y anotaciones se encogen igual.

  efectivo = font.size * (ancho impreso / ancho natural del PDF)

Con cada figura generada a su ancho impreso el factor es 1 y el efectivo es el
declarado. Este script comprueba que sigue siendo asi: es el tipo de cosa que
se degrada en cuanto alguien retoca un figsize.

Uso: python paper_gp/audit_fuentes_figuras.py
"""

import glob
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
LINEWIDTH_PT, PT_IN = 360.0, 72.27
TOLERANCIA = 0.15          # pt de desviacion admitida entre figuras

tex = open(os.path.join(HERE, "main.tex"), encoding="utf-8").read()

# ancho con el que main.tex incluye cada figura
inc = {}
for m in re.finditer(r"\\includegraphics\[width=([^\]]+)\]\{figures/([^}]+)\}",
                     tex):
    f = re.match(r"([\d.]*)\\linewidth", m.group(1).strip())
    inc[m.group(2)] = (m.group(1).strip(),
                       float(f.group(1)) if f and f.group(1) else 1.0)

# font.size de cada script generador, buscando el nombre del PDF en su fuente
fuentes = {}
for s in sorted(glob.glob(os.path.join(HERE, "make_*.py")) +
                glob.glob(os.path.join(REPO, "scripts", "*.py"))):
    src = open(s, encoding="utf-8").read()
    m = re.search(r'"font\.size"\s*:\s*([\d.]+)', src)
    for fich in inc:
        if fich in src and "savefig" in src:
            fuentes.setdefault(fich, (os.path.basename(s),
                                      float(m.group(1)) if m else None))

print(f"{'figura':<24}{'incluida':<14}{'nat':>6}{'impr':>7}{'font':>6}"
      f"{'efectivo':>10}  script")
efectivos, faltan = [], []
for fich, (spec, frac) in sorted(inc.items()):
    ruta = os.path.join(HERE, "figures", fich)
    if not os.path.exists(ruta):
        print(f"{fich:<24}  FALTA el PDF")
        faltan.append(fich)
        continue
    info = subprocess.run(["pdfinfo", ruta], capture_output=True,
                          text=True).stdout
    m = re.search(r"Page size:\s*([\d.]+) x ([\d.]+)", info)
    nat = float(m.group(1)) / PT_IN
    impr = LINEWIDTH_PT * frac / PT_IN
    script, size = fuentes.get(fich, ("?", None))
    if size is None:
        print(f"{fich:<24}{spec:<14}{nat:>6.2f}{impr:>7.2f}"
              f"{'?':>6}{'?':>10}  {script}")
        faltan.append(fich)
        continue
    efe = size * impr / nat
    efectivos.append((fich, efe))
    print(f"{fich:<24}{spec:<14}{nat:>6.2f}{impr:>7.2f}{size:>6.1f}"
          f"{efe:>10.2f}  {script}")

mal = 0
if efectivos:
    vals = [e for _, e in efectivos]
    print(f"\nefectivo: {min(vals):.2f} a {max(vals):.2f}, "
          f"dispersion {max(vals) / min(vals):.2f}x")
    if max(vals) - min(vals) > TOLERANCIA:
        mal += 1
        print(f"FALLA: mas de {TOLERANCIA} pt de diferencia entre figuras.")
        for f, e in sorted(efectivos, key=lambda t: -t[1]):
            print(f"  {f:<24} {e:.2f}")
    else:
        print("OK: todas dentro de tolerancia.")
if faltan:
    mal += 1
    print(f"FALLA: sin medir {faltan}")
sys.exit(1 if mal else 0)
