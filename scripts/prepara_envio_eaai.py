# -*- coding: utf-8 -*-
"""Prepara drl-eaai/: el envio doblemente anonimo a EAAI.

Engineering Applications of Artificial Intelligence (Elsevier,
Editorial Manager). Directorio plano con:

- manuscript.tex ANONIMO: paper/main.tex sin los bloques
  %<<IDENTIDAD ... %IDENTIDAD>>, con la bibliografia embebida (el
  .bbl sustituye a \\bibliography) y las rutas de figura aplanadas.
- supplementary.tex (ya anonimo de fabrica), mismo tratamiento.
- title_page.tex y highlights.tex: fuentes estaticas mantenidas a
  mano en drl-eaai/ (NO se regeneran aqui; solo se compilan).
- las figuras PDF referenciadas, al mismo nivel.
- PDFs de control compilados de manuscrito, title page y highlights.

Los originales de paper/ no se tocan. Idempotente: relanzar tras cada
recompilacion. Aborta si la copia anonima conserva algun rastro de
identidad fuera de las referencias.

    python scripts/prepara_envio_eaai.py
"""
import glob
import os
import re
import shutil
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DESTINO = "drl-eaai"
ID_RE = re.compile(r"%<<IDENTIDAD.*?%IDENTIDAD>>\n?", re.S)


def copia(origen, destino):
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    try:
        shutil.copy2(origen, destino)
    except PermissionError:
        with open(origen, "rb") as a, open(destino, "wb") as b:
            b.write(a.read())


def compila(tex):
    for _ in range(2):
        r = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex],
            cwd=DESTINO, capture_output=True, text=True,
            errors="replace")
    log = open(os.path.join(DESTINO, tex.replace(".tex", ".log")),
               encoding="utf-8", errors="replace").read()
    m = re.search(r"Output written on .*\((\d+) pages?", log)
    assert m, f"{tex}: sin PDF"
    return int(m.group(1))


def main():
    os.makedirs(DESTINO, exist_ok=True)

    # --- manuscrito anonimo y suplementario, con bbl embebido ---
    for f, bbl, anon in (("main.tex", "main.bbl", True),
                         ("supplementary.tex", "supplementary.bbl",
                          False)):
        t = open(os.path.join("paper", f), encoding="utf-8").read()
        if anon:
            n_id = len(ID_RE.findall(t))
            assert n_id == 2, f"{f}: {n_id} bloques IDENTIDAD (esperaba 2)"
            t = ID_RE.sub("", t)
        t = t.replace("{figures/", "{")
        cuerpo_bbl = open(os.path.join("paper", bbl),
                          encoding="utf-8").read()
        t = t.replace("\\bibliographystyle{elsarticle-harv}\n", "")
        t = t.replace("\\bibliography{refs}", cuerpo_bbl)
        assert "\\bibliography{refs}" not in t and "thebibliography" in t
        destino = "manuscript.tex" if anon else f
        # rastro de identidad: solo puede sobrevivir dentro de la
        # bibliografia (las autocitas en tercera persona son normales)
        cuerpo = t[:t.index("\\begin{thebibliography}")]
        for rastro in ("diazhernan", "Oviedo", "\\author", "\\ead{",
                       "\\address", "Acknowledg"):
            assert rastro not in cuerpo, f"{destino}: rastro {rastro}"
        with open(os.path.join(DESTINO, destino), "w",
                  encoding="utf-8", newline="") as out:
            out.write(t)

    # --- figuras referenciadas ---
    tex = (open("paper/main.tex", encoding="utf-8").read()
           + open("paper/supplementary.tex", encoding="utf-8").read())
    usadas = set(re.findall(r"includegraphics(?:\[[^]]*\])?\{figures/"
                            r"([^}]+)\}", tex))
    n_fig = 0
    for f in glob.glob("paper/figures/*.pdf"):
        if os.path.basename(f) in usadas:
            copia(f, os.path.join(DESTINO, os.path.basename(f)))
            n_fig += 1

    # --- compilaciones de control ---
    paginas = compila("manuscript.tex")
    assert paginas <= 50, f"manuscrito a {paginas} paginas (limite 50)"
    p_sup = compila("supplementary.tex")
    compila("title_page.tex")
    compila("highlights.tex")
    # limpiar auxiliares
    for aux in glob.glob(os.path.join(DESTINO, "*.aux")) + \
            glob.glob(os.path.join(DESTINO, "*.log")) + \
            glob.glob(os.path.join(DESTINO, "*.out")) + \
            glob.glob(os.path.join(DESTINO, "*.spl")):
        os.remove(aux)
    print(f"drl-eaai/ actualizado: manuscrito anonimo ({paginas} pags), "
          f"suplementario ({p_sup} pags), title page, highlights, "
          f"{n_fig} figuras")


if __name__ == "__main__":
    main()
