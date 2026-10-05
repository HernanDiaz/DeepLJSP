# -*- coding: utf-8 -*-
"""Prepara los tres ficheros del envio a Computers & Industrial Engineering.

C&IE revisa a doble ciego, de modo que la portada con los datos del autor
y el manuscrito anonimo van como ficheros SEPARADOS, y el manuscrito no
puede llevar nombres, afiliaciones ni agradecimientos. Tampoco puede
llevar el enlace al deposito, que identifica igual que una firma.

Se genera todo desde main.tex, asi que no hay una segunda copia del
articulo que se pueda quedar atras.

    python paper_caie/build_envio.py

Deja en paper_caie/envio/:
    manuscript.pdf   anonimo, sin marcas de revision
    supplementary.pdf  el material suplementario, tambien anonimo
    title_page.pdf   titulo, autor, afiliacion, agradecimientos
    highlights.pdf   los cinco puntos

El articulo y el suplementario se citan entre si con xr-hyper, que lee
el .aux del otro documento: se copian los de paper_caie, asi que hay que
haber compilado los dos alli antes (la numeracion no cambia al anonimizar).
"""
import io
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENVIO = os.path.join(HERE, "envio")
TMP = os.path.join(HERE, "_envio")

PORTADA = r"""\documentclass[11pt]{article}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[a4paper,margin=2.5cm]{geometry}
\usepackage{hyperref}
\pagestyle{empty}
\begin{document}
\begin{center}
{\large\bfseries %(titulo)s}
\end{center}

\vspace{1em}
\noindent\textbf{Author.} Hern\'an D\'iaz Rodr\'iguez

\noindent Department of Computing, University of Oviedo,
Campus de Gij\'on, 33204 Gij\'on, Spain

\vspace{1em}
\noindent\textbf{Corresponding author.} Hern\'an D\'iaz Rodr\'iguez,
Department of Computing, University of Oviedo, Campus de Gij\'on,
Edificio Departamental Oeste, 33204 Gij\'on, Asturias, Spain.
\ Email: \href{mailto:diazhernan@uniovi.es}{diazhernan@uniovi.es}

\vspace{1em}
\noindent\textbf{CRediT authorship contribution statement.}
\textbf{Hern\'an D\'iaz}: Conceptualization, Methodology, Software,
Validation, Formal analysis, Investigation, Resources, Data curation,
Writing -- original draft, Writing -- review \& editing, Visualization.

\vspace{1em}
\noindent\textbf{Acknowledgements.}
This work was supported by the Spanish Ministry of Science, Innovation
and Universities (MCIN/AEI/10.13039/501100011033) under grant
PID2022-141746OB-I00.

\vspace{1em}
\noindent\textbf{Declaration of competing interest.}
The author declares that there are no known competing financial
interests or personal relationships that could have appeared to
influence the work reported in this paper.

\end{document}
"""

# lo que sustituye al enlace del deposito mientras dure el anonimato
DATOS_ANON = r"""\section*{Data availability}
The GP hyper-heuristic is implemented from scratch in pure
Python/NumPy, with no evolutionary-computation dependencies; evolved
rules are stored as plain JSON expression trees and evaluated as drop-in
dispatching strategies by the same environment used by every baseline.
All benchmark instances, the evolved rules of every experimental arm,
the primary result files behind each table and figure, and a
self-contained implementation that re-derives the deposited results from
scratch are openly available in a public repository. The link is
withheld here because it would identify the author, and is provided to
the editor on request and in the published version.
"""


def titulo(t):
    m = re.search(r"\\title\{(.+?)\}\s*\n\s*\n", t, re.S)
    if not m:
        m = re.search(r"\\title\{(.+?)\}", t, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip()


def anonimiza(t):
    """Quita del manuscrito todo lo que identifique al autor."""
    fuera = [
        (r"\\author\{[^}]*\}\s*\n", "autor"),
        (r"\\ead\{[^}]*\}\s*\n", "correo"),
        (r"\\affiliation\{.*?\n            country=\{[^}]*\}\}\s*\n",
         "afiliacion"),
    ]
    for pat, etq in fuera:
        t, n = re.subn(pat, "", t, flags=re.S)
        assert n == 1, f"no se pudo quitar: {etq} ({n} coincidencias)"

    # los tres bloques del cierre que llevan nombre o financiacion
    for cab in ("CRediT authorship contribution statement",
                "Acknowledgements", "Declaration of competing interest"):
        pat = r"\\section\*\{" + re.escape(cab) + r"\}.*?(?=\\section\*|\\bibliographystyle)"
        t, n = re.subn(pat, "", t, flags=re.S)
        assert n == 1, f"no se pudo quitar la seccion: {cab}"

    # el deposito, que identifica igual que una firma
    # el reemplazo va como funcion: si no, re interpreta los \s y \b del
    # LaTeX como escapes de plantilla
    pat = r"\\section\*\{Data availability\}.*?(?=\\bibliographystyle)"
    t, n = re.subn(pat, lambda _: DATOS_ANON + "\n", t, flags=re.S)
    assert n == 1, "no se pudo anonimizar Data availability"

    return t


def limpia(t):
    """Comprueba que no quedan marcas de revision.

    En paper_caie el fuente ya no las lleva: es un envio nuevo, sin
    version anterior que marcar. Si alguna vuelve a aparecer, se aborta
    en vez de enviarla.
    """
    for rastro in ("revcolor", "\\rev{"):
        assert rastro not in t, f"queda una marca de revision: {rastro}"
    return t


def compila(nombre, fuente, salida, con_bibtex=False, tex_nombre="main",
            aux=()):
    d = os.path.join(TMP, nombre)
    os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, tex_nombre + ".tex"), "w", encoding="utf-8",
            newline="").write(fuente)
    for extra in ("refs.bib", "figures") + tuple(aux):
        origen = os.path.join(HERE, extra)
        destino = os.path.join(d, extra)
        if os.path.isdir(origen):
            shutil.copytree(origen, destino, dirs_exist_ok=True)
        elif os.path.exists(origen):
            shutil.copy2(origen, destino)

    def tex():
        return subprocess.run(["pdflatex", "-interaction=nonstopmode",
                               tex_nombre + ".tex"], cwd=d,
                              capture_output=True, text=True)

    tex()
    if con_bibtex:
        subprocess.run(["bibtex", tex_nombre], cwd=d, capture_output=True,
                       text=True)
    tex()
    r = tex()
    pdf = os.path.join(d, tex_nombre + ".pdf")
    if not os.path.exists(pdf):
        sys.exit("\n".join(l for l in r.stdout.splitlines()
                           if l.startswith("!"))[:2000])
    shutil.copy2(pdf, salida)
    log = io.open(os.path.join(d, tex_nombre + ".log"), encoding="utf-8",
                  errors="replace").read()
    return log


def main():
    t = io.open(os.path.join(HERE, "main.tex"), encoding="utf-8").read()
    os.makedirs(ENVIO, exist_ok=True)

    tit = titulo(t)
    compila("portada", PORTADA % {"titulo": tit},
            os.path.join(ENVIO, "title_page.pdf"))
    print("title_page.pdf")

    man = anonimiza(limpia(t))
    for a in ("main.aux", "supplementary.aux"):
        assert os.path.exists(os.path.join(HERE, a)), \
            f"falta {a}: compilar main.tex y supplementary.tex antes"
    log = compila("manuscrito", man,
                  os.path.join(ENVIO, "manuscript.pdf"), con_bibtex=True,
                  aux=("supplementary.aux",))
    print(f"manuscript.pdf   overfull={log.count('Overfull')} "
          f"undefined={log.count('undefined')}")

    su = limpia(io.open(os.path.join(HERE, "supplementary.tex"),
                        encoding="utf-8").read())
    log = compila("suplementario", su,
                  os.path.join(ENVIO, "supplementary.pdf"),
                  tex_nombre="supplementary", aux=("main.aux",))
    print(f"supplementary.pdf overfull={log.count('Overfull')} "
          f"undefined={log.count('undefined')}")

    hl = io.open(os.path.join(HERE, "highlights.tex"),
                 encoding="utf-8").read()
    compila("highlights", hl, os.path.join(ENVIO, "highlights.pdf"))
    print("highlights.pdf")

    # ultima red: que el manuscrito no lleve ni una palabra delatora
    # pdftotext escribe la codificacion de la consola, no utf-8: se lee
    # en bytes y se decodifica a la brava
    texto = ""
    for pdf in ("manuscript.pdf", "supplementary.pdf"):
        bruto = subprocess.run(["pdftotext", os.path.join(ENVIO, pdf), "-"],
                               capture_output=True).stdout
        texto += bruto.decode("utf-8", errors="replace")
    # cadenas que identifican de verdad. Ojo con palabras corrientes:
    # una palabra como "acknowledgement" puede salir en la prosa y no delata a
    # nadie, asi que se busca el encabezado y no la palabra.
    delatoras = ["Hern", "Oviedo", "uniovi", "Gij", "zenodo", "PID2022",
                 "MCIN/AEI", "Acknowledgements", "CRediT",
                 "competing interest"]
    malas = [d for d in delatoras if d.lower() in texto.lower()]
    if malas:
        sys.exit(f"EL MANUSCRITO NO ES ANONIMO: aparece {malas}")
    print("\nni el manuscrito ni el suplementario identifican al autor")


if __name__ == "__main__":
    main()
