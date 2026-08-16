# -*- coding: utf-8 -*-
"""Prepara drl-jim/: lo que se sube al sistema de la revista.

Journal of Intelligent Manufacturing (Springer). Todo en un unico
directorio plano, como pide el sistema de envio: PDF del manuscrito,
material suplementario, fuentes LaTeX (tex, bib, bbl, clase, bst,
sty) y las figuras al mismo nivel. Como las figuras pierden su
subcarpeta, las rutas figures/ de los .tex se reescriben EN LA COPIA;
los originales de paper/ no se tocan. Idempotente: relanzar tras cada
recompilacion.

    python scripts/prepara_envio.py
"""
import glob
import os
import shutil
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DESTINO = "drl-jim"


def copia(origen, destino):
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    shutil.copy2(origen, destino)


def main():
    os.makedirs(DESTINO, exist_ok=True)
    copia("paper/main.pdf", os.path.join(DESTINO, "manuscript.pdf"))
    copia("paper/supplementary.pdf",
          os.path.join(DESTINO, "supplementary_material.pdf"))
    planos = ["refs.bib", "main.bbl", "supplementary.bbl", "sn-jnl.cls",
              "sn-apacite.bst", "cuted.sty", "stfloats.sty"]
    for f in planos:
        copia(os.path.join("paper", f), os.path.join(DESTINO, f))
    # los .tex viajan con las rutas de figura aplanadas
    for f in ("main.tex", "supplementary.tex"):
        t = open(os.path.join("paper", f), encoding="utf-8").read()
        t = t.replace("{figures/", "{")
        with open(os.path.join(DESTINO, f), "w", encoding="utf-8",
                  newline="") as out:
            out.write(t)
    # solo las figuras que los .tex referencian; las huerfanas de
    # versiones anteriores no viajan
    import re
    tex = (open("paper/main.tex", encoding="utf-8").read()
           + open("paper/supplementary.tex", encoding="utf-8").read())
    usadas = set(re.findall(r"includegraphics(?:\[[^]]*\])?\{figures/"
                            r"([^}]+)\}", tex))
    n_fig = 0
    for f in glob.glob("paper/figures/*.pdf"):
        if os.path.basename(f) in usadas:
            copia(f, os.path.join(DESTINO, os.path.basename(f)))
            n_fig += 1
    print(f"drl-jim/ actualizado, plano: {len(planos) + 4} ficheros "
          f"+ {n_fig} figuras")


if __name__ == "__main__":
    main()
