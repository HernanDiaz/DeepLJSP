# -*- coding: utf-8 -*-
"""Compila el paper SIN las marcas de revision.

El azul de \\rev{} sirve para que nosotros veamos que ha cambiado. En un
envio a una revista distinta no vale: esos revisores no han visto la
version anterior, y el color solo delataria que hubo una.

Deja main_limpio.pdf junto al marcado, sin tocar main.tex.

    python paper_gp/build_limpio.py
"""
import io
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(HERE, "_limpio")
SALIDA = os.path.join(HERE, "main_limpio.pdf")


def main():
    t = io.open(os.path.join(HERE, "main.tex"), encoding="utf-8").read()
    marcado = r"\newcommand{\rev}[1]{\textcolor{revcolor}{#1}}"
    assert t.count(marcado) == 1, "la orden \\rev ya no esta donde estaba"
    t = t.replace(marcado, r"\newcommand{\rev}[1]{#1}")
    # el color de grupo dentro de las tablas nuevas tambien sobra
    t = t.replace("\\color{revcolor}\n", "")

    quedan = len(re.findall(r"\\textcolor\{revcolor\}", t))
    assert quedan == 0, f"quedan {quedan} marcas de color sueltas"

    os.makedirs(TMP, exist_ok=True)
    io.open(os.path.join(TMP, "main.tex"), "w", encoding="utf-8",
            newline="").write(t)
    for nombre in ("main.bbl", "figures"):
        origen = os.path.join(HERE, nombre)
        destino = os.path.join(TMP, nombre)
        if os.path.isdir(origen):
            shutil.copytree(origen, destino, dirs_exist_ok=True)
        elif os.path.exists(origen):
            shutil.copy2(origen, destino)

    for _ in range(2):
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode",
                            "-halt-on-error", "main.tex"],
                           cwd=TMP, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("\n".join(l for l in r.stdout.splitlines()
                           if l.startswith("!"))[:2000])
    shutil.copy2(os.path.join(TMP, "main.pdf"), SALIDA)
    log = io.open(os.path.join(TMP, "main.log"), encoding="utf-8",
                  errors="replace").read()
    print(f"escrito {SALIDA}")
    for aviso in ("Overfull", "undefined"):
        n = log.count(aviso)
        print(f"  {aviso}: {n}")


if __name__ == "__main__":
    main()
