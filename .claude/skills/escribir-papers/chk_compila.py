# -*- coding: utf-8 -*-
"""Resumen del main.log + palabras del abstract (ejecutar en paper/)."""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
t = open("main.log", encoding="utf-8", errors="replace").read()
err = re.findall(r"^! .*", t, re.M)
und = re.findall(r"Citation .([\w]+). .* undefined", t)
print("errores:", err[:4] if err else "ninguno")
print("Overfull:", len(re.findall(r"Overfull \\hbox", t)))
print("paginas:", re.findall(r"Output written.*?\((\d+) page", t))
print("citas rotas:", sorted(set(und)) or "no")
m = re.search(r"\\abstract\{(.*?)\}\s*\\keywords",
              open("main.tex", encoding="utf-8").read(), re.S)
print("palabras del abstract:",
      len(re.sub(r"[\\${}%~]", " ", m.group(1)).split()))
