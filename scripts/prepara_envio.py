# -*- coding: utf-8 -*-
"""Prepara envio_revista/: lo que se sube al sistema de la revista.

Journal of Intelligent Manufacturing (Springer). Copia el PDF del
manuscrito, el material suplementario y las fuentes LaTeX completas
(tex, bib, bbl, clase, bst, sty y figuras), que el sistema pide para
manuscritos LaTeX. Idempotente: relanzar tras cada recompilacion.

    python scripts/prepara_envio.py
"""
import glob
import os
import shutil
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DESTINO = "envio_revista"


def copia(origen, destino):
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    shutil.copy2(origen, destino)


def main():
    os.makedirs(DESTINO, exist_ok=True)
    copia("paper/main.pdf", os.path.join(DESTINO, "manuscript.pdf"))
    copia("paper/supplementary.pdf",
          os.path.join(DESTINO, "supplementary_material.pdf"))
    fuentes = ["main.tex", "supplementary.tex", "refs.bib", "main.bbl",
               "supplementary.bbl", "sn-jnl.cls", "sn-apacite.bst",
               "cuted.sty", "stfloats.sty"]
    for f in fuentes:
        copia(os.path.join("paper", f),
              os.path.join(DESTINO, "fuente", f))
    for f in glob.glob("paper/figures/*.pdf"):
        copia(f, os.path.join(DESTINO, "fuente", "figures",
                              os.path.basename(f)))
    print(f"envio_revista/ actualizado "
          f"({len(fuentes) + 2} ficheros + figuras)")


if __name__ == "__main__":
    main()
