# -*- coding: utf-8 -*-
"""Prepara los ficheros del envio a Applied Soft Computing.

ASOC revisa con anonimato simple: el manuscrito lleva autor, afiliacion,
agradecimientos y el enlace al deposito, y no hay portada aparte. Pide el
fuente editable (un PDF no vale como fuente), los highlights en un fichero
editable con "highlights" en el nombre y un graphical abstract obligatorio.

    python paper_asoc/make_graphical_abstract.py
    python paper_asoc/build_envio.py

Deja en paper_asoc/envio/:
    manuscript.pdf          el articulo compilado desde el paquete de fuentes
    manuscript_source.zip   main.tex, main.bbl, refs.bib, figuras y el .aux
                            del suplementario que leen las referencias S-
    supplementary.pdf       el material suplementario
    highlights.txt          los cinco puntos, editables
    graphical_abstract.tif  y su version vectorial .pdf
    cover_letter.pdf

El manuscrito se compila DENTRO de una copia del paquete de fuentes, en un
directorio limpio: si al zip le falta algo, el envio aborta aqui y no en el
Editorial Manager.
"""
import io
import os
import re
import shutil
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ENVIO = os.path.join(HERE, "envio")
TMP = os.path.join(HERE, "_envio")

FUENTES = ["main.tex", "main.bbl", "refs.bib", "supplementary.aux"]


def tex(d, nombre, veces=1):
    r = None
    for _ in range(veces):
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode",
                            nombre + ".tex"], cwd=d, capture_output=True,
                           text=True, encoding="utf-8", errors="replace")
    return r


def figuras_usadas(t):
    """Las figuras que main.tex incluye de verdad, para no subir de mas."""
    usadas = set(re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", t))
    usadas |= set(re.findall(r"\\input\{(figures/[^}]+)\}", t))
    rutas = []
    for u in sorted(usadas):
        for ext in ("", ".pdf", ".tex", ".png"):
            if os.path.exists(os.path.join(HERE, u + ext)):
                rutas.append(u + ext)
                break
        else:
            sys.exit(f"falta la figura {u}")
    return rutas


def main():
    for a in ("main.aux", "main.bbl", "supplementary.aux"):
        assert os.path.exists(os.path.join(HERE, a)), \
            f"falta {a}: compilar supplementary.tex, main.tex y bibtex antes"
    t = io.open(os.path.join(HERE, "main.tex"), encoding="utf-8").read()
    for rastro in ("revcolor", "\\rev{", "\\todo{"):
        assert rastro not in t.replace("\\newcommand{\\todo}", ""), \
            f"queda una marca de revision: {rastro}"

    shutil.rmtree(TMP, ignore_errors=True)
    shutil.rmtree(ENVIO, ignore_errors=True)
    os.makedirs(ENVIO)

    # paquete de fuentes
    figs = figuras_usadas(t)
    zp = os.path.join(ENVIO, "manuscript_source.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in FUENTES + figs:
            z.write(os.path.join(HERE, f), f)
    print(f"manuscript_source.zip  {len(FUENTES)} fuentes y {len(figs)} figuras")

    # el manuscrito, compilado desde el zip en un directorio limpio. Cuatro
    # pasadas: con tres, si la paginacion cambia, puede salir sin bibliografia
    d = os.path.join(TMP, "manuscrito")
    os.makedirs(d)
    with zipfile.ZipFile(zp) as z:
        z.extractall(d)
    r = tex(d, "main", 4)
    pdf = os.path.join(d, "main.pdf")
    if not os.path.exists(pdf):
        sys.exit("\n".join(l for l in r.stdout.splitlines()
                           if l.startswith("!"))[:2000])
    log = io.open(os.path.join(d, "main.log"), encoding="utf-8",
                  errors="replace").read()
    pags = re.search(r"Output written on main\.pdf \((\d+) pages", log)
    indef = len(re.findall(r"(Citation|Reference) `[^']+' .*undefined", log))
    shutil.copy2(pdf, os.path.join(ENVIO, "manuscript.pdf"))
    print(f"manuscript.pdf         {pags.group(1)} paginas, "
          f"overfull={log.count('Overfull')}, sin resolver={indef}")
    if indef:
        sys.exit("hay citas o referencias sin resolver en el manuscrito")
    # una \citet con un estilo numerico sin nombres no da aviso en el log:
    # sale "(author?) [n]" en el PDF. Se busca en el texto
    txt = subprocess.run(["pdftotext", pdf, "-"], capture_output=True
                         ).stdout.decode("utf-8", errors="replace")
    for rastro in ("(author?)", "??"):
        if rastro in txt:
            sys.exit(f"el manuscrito contiene '{rastro}'")

    # suplementario: sus referencias al articulo salen de main.aux
    d = os.path.join(TMP, "suplementario")
    os.makedirs(d)
    for f in ("supplementary.tex", "main.aux"):
        shutil.copy2(os.path.join(HERE, f), d)
    shutil.copytree(os.path.join(HERE, "figures"), os.path.join(d, "figures"))
    tex(d, "supplementary", 3)
    shutil.copy2(os.path.join(d, "supplementary.pdf"),
                 os.path.join(ENVIO, "supplementary.pdf"))
    print("supplementary.pdf")

    # highlights en texto plano: editables, como pide la revista
    hl = io.open(os.path.join(HERE, "highlights.tex"), encoding="utf-8").read()
    items = hl.split("\\begin{itemize}")[1].split("\\end{itemize}")[0]
    items = [" ".join(i.split()) for i in items.split("\\item")[1:]]
    items = [i.replace("$20\\times15$", "20x15").replace("$", "") for i in items]
    assert all("\\" not in i for i in items), items
    assert 3 <= len(items) <= 5 and max(map(len, items)) <= 85, items
    io.open(os.path.join(ENVIO, "highlights.txt"), "w", encoding="utf-8",
            newline="\r\n").write("Highlights\n\n" +
                                  "\n".join("- " + i for i in items) + "\n")
    print(f"highlights.txt         {len(items)} puntos, "
          f"el mas largo de {max(map(len, items))} caracteres")

    for f in ("graphical_abstract.tif", "graphical_abstract.pdf"):
        origen = os.path.join(HERE, f)
        assert os.path.exists(origen), \
            "falta el graphical abstract: make_graphical_abstract.py"
        shutil.copy2(origen, ENVIO)
    print("graphical_abstract.tif y .pdf")

    d = os.path.join(TMP, "carta")
    os.makedirs(d)
    shutil.copy2(os.path.join(HERE, "cover_letter.tex"), d)
    tex(d, "cover_letter", 2)
    shutil.copy2(os.path.join(d, "cover_letter.pdf"),
                 os.path.join(ENVIO, "cover_letter.pdf"))
    print("cover_letter.pdf")

    # ninguna fuente Type 3: produccion las rechaza
    for f in ("manuscript.pdf", "supplementary.pdf",
              "graphical_abstract.pdf"):
        r = subprocess.run(["pdffonts", os.path.join(ENVIO, f)],
                           capture_output=True, text=True)
        if "Type 3" in r.stdout:
            sys.exit(f"{f} lleva fuentes Type 3")
    print("\nsin fuentes Type 3")


if __name__ == "__main__":
    main()
