# -*- coding: utf-8 -*-
"""Resumen de una compilacion de LaTeX: errores, desbordes, paginas,
citas rotas y palabras del resumen.

Se ejecuta en el directorio del manuscrito. Por defecto mira main.log y
main.tex; con un argumento, usa ese nombre base.

    python chk_compila.py            # main
    python chk_compila.py articulo   # articulo.log y articulo.tex
"""
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

base = sys.argv[1] if len(sys.argv) > 1 else "main"

log = f"{base}.log"
if not os.path.exists(log):
    sys.exit(f"no encuentro {log}: compila primero")
t = open(log, encoding="utf-8", errors="replace").read()

err = re.findall(r"^! .*", t, re.M)
und = re.findall(r"Citation .([\w:.-]+). .* undefined", t)
ref = re.findall(r"Reference .([\w:.-]+). .* undefined", t)

print("errores:", err[:4] if err else "ninguno")
print("Overfull:", len(re.findall(r"Overfull \\hbox", t)))
print("paginas:", re.findall(r"Output written.*?\((\d+) page", t))
print("citas rotas:", sorted(set(und)) or "no")
print("referencias rotas:", sorted(set(ref)) or "no")

# el resumen: las plantillas lo escriben de dos formas distintas
tex = f"{base}.tex"
if not os.path.exists(tex):
    sys.exit(0)
fuente = open(tex, encoding="utf-8", errors="replace").read()
m = (re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", fuente, re.S)
     or re.search(r"\\abstract\{(.*?)\}\s*\\keywords", fuente, re.S))
if not m:
    print("palabras del resumen: no localizo el bloque")
    sys.exit(0)
plano = re.sub(r"\\[a-zA-Z]+\*?", " ", m.group(1))
plano = re.sub(r"[${}%~\\]", " ", plano)
print("palabras del resumen:",
      len([w for w in plano.split() if any(c.isalnum() for c in w)]))
