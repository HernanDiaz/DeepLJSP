# -*- coding: utf-8 -*-
"""Prepara paper_eswa/envio/: el envio doblemente anonimo a ESWA.

Expert Systems with Applications (Elsevier) revisa a doble ciego: la
title page con la identidad y el manuscrito anonimo van en ficheros
separados, y ni el manuscrito ni el suplementario pueden llevar nombres,
afiliaciones ni agradecimientos. Adaptado de scripts/prepara_envio_eaai.py.

Deja en paper_eswa/envio/:
    manuscript.tex / .pdf   ANONIMO: main.tex sin los bloques
                            %<<IDENTIDAD ... %IDENTIDAD>>, con el .bbl
                            embebido y las rutas de figura aplanadas
    supplementary.tex / .pdf  el suplementario (ya anonimo de fabrica)
    las figuras PDF que usan los dos
    title_page.pdf          el unico fichero con identidad
    highlights.txt / .pdf   los cinco puntos, editables
    cover_letter.pdf

Hay que haber compilado antes main.tex y supplementary.tex con bibtex en
paper_eswa/ (compila.bat). Aborta si la copia anonima conserva algun
rastro de identidad fuera de las referencias, o si el PDF lleva citas
sin resolver.

    python paper_eswa/build_envio.py
"""
import glob
import io
import os
import re
import shutil
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ENVIO = os.path.join(HERE, "envio")
ID_RE = re.compile(r"%<<IDENTIDAD.*?%IDENTIDAD>>\n?", re.S)
# cadenas que identifican de verdad. Solo pueden aparecer dentro de la
# bibliografia: las autocitas en tercera persona son normales
RASTROS = ("diazhernan", "Oviedo", "uniovi", "Gil Ruiz", "Europea",
           "\\author", "\\ead{", "\\address", "Acknowledg", "PID2022",
           "CRediT")


def lee(nombre):
    return io.open(os.path.join(HERE, nombre), encoding="utf-8").read()


def compila(tex, veces=2):
    for _ in range(veces):
        subprocess.run(["pdflatex", "-interaction=nonstopmode", tex],
                       cwd=ENVIO, capture_output=True, text=True,
                       errors="replace")
    log = io.open(os.path.join(ENVIO, tex.replace(".tex", ".log")),
                  encoding="utf-8", errors="replace").read()
    m = re.search(r"Output written on .*\((\d+) pages?", log)
    assert m, f"{tex}: sin PDF"
    return int(m.group(1)), log


def main():
    for a in ("main.bbl", "supplementary.bbl"):
        assert os.path.exists(os.path.join(HERE, a)), \
            f"falta {a}: compilar con bibtex antes (compila.bat)"
    shutil.rmtree(ENVIO, ignore_errors=True)
    os.makedirs(ENVIO)

    # --- manuscrito anonimo y suplementario, con el bbl embebido ---
    for f, bbl, anon in (("main.tex", "main.bbl", True),
                         ("supplementary.tex", "supplementary.bbl", False)):
        t = lee(f)
        if anon:
            n_id = len(ID_RE.findall(t))
            assert n_id == 2, f"{f}: {n_id} bloques IDENTIDAD (esperaba 2)"
            t = ID_RE.sub("", t)
        t = t.replace("{figures/", "{")
        t = t.replace("\\bibliographystyle{elsarticle-harv}\n", "")
        t = t.replace("\\bibliography{refs}", lee(bbl))
        assert "\\bibliography{refs}" not in t and "thebibliography" in t
        cuerpo = t[:t.index("\\begin{thebibliography}")]
        for rastro in RASTROS:
            assert rastro not in cuerpo, f"{f}: rastro de identidad {rastro}"
        destino = "manuscript.tex" if anon else f
        io.open(os.path.join(ENVIO, destino), "w", encoding="utf-8",
                newline="").write(t)

    # --- figuras referenciadas ---
    tex = lee("main.tex") + lee("supplementary.tex")
    usadas = set(re.findall(r"includegraphics(?:\[[^]]*\])?\{figures/"
                            r"([^}]+)\}", tex))
    for u in usadas:
        shutil.copy2(os.path.join(HERE, "figures", u), ENVIO)

    # --- fuentes que se compilan tal cual ---
    for f in ("title_page.tex", "highlights.tex", "cover_letter.tex"):
        shutil.copy2(os.path.join(HERE, f), ENVIO)

    # --- compilaciones ---
    pags, log = compila("manuscript.tex", 3)
    indef = re.findall(r"(Citation|Reference) `[^']+' .*undefined", log)
    assert not indef, f"manuscrito con citas o referencias sin resolver"
    txt = subprocess.run(["pdftotext", os.path.join(ENVIO, "manuscript.pdf"),
                          "-"], capture_output=True).stdout.decode(
                              "utf-8", errors="replace")
    for rastro in ("(author?)", "??"):
        assert rastro not in txt, f"el manuscrito contiene '{rastro}'"
    p_sup, _ = compila("supplementary.tex", 3)
    compila("title_page.tex")
    compila("highlights.tex")
    compila("cover_letter.tex")

    # highlights en texto plano: editables, como pide la revista
    hl = re.findall(r"\\item (.+)", lee("highlights.tex"))
    hl = [h.strip() for h in hl]
    assert 3 <= len(hl) <= 5 and max(map(len, hl)) <= 85, hl
    io.open(os.path.join(ENVIO, "highlights.txt"), "w", encoding="utf-8",
            newline="\r\n").write("Highlights\n\n"
                                  + "\n".join("- " + h for h in hl) + "\n")

    # ninguna fuente Type 3
    for f in ("manuscript.pdf", "supplementary.pdf"):
        r = subprocess.run(["pdffonts", os.path.join(ENVIO, f)],
                           capture_output=True, text=True)
        assert "Type 3" not in r.stdout, f"{f} lleva fuentes Type 3"

    for aux in (glob.glob(os.path.join(ENVIO, "*.aux"))
                + glob.glob(os.path.join(ENVIO, "*.log"))
                + glob.glob(os.path.join(ENVIO, "*.out"))
                + glob.glob(os.path.join(ENVIO, "*.spl"))):
        os.remove(aux)
    print(f"paper_eswa/envio/: manuscrito anonimo ({pags} pags), "
          f"suplementario ({p_sup} pags), title page, highlights "
          f"({len(hl)}), carta, {len(usadas)} figuras; sin Type 3")


if __name__ == "__main__":
    main()
