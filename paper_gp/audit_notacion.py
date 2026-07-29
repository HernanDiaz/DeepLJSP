# -*- coding: utf-8 -*-
"""Inventario de notacion de main.tex.

Extrae los segmentos matematicos y los tokeniza, para poder revisar a mano
(a) que cada simbolo tenga una sola lectura y (b) donde aparece por primera
vez, que es donde tiene que estar definido. No juzga: solo lista con numero
de linea, el juicio es mio despues.
"""
import re
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SRC = "paper_gp/main.tex"
lines = open(SRC, encoding="utf-8").read().split("\n")

# fuera comentarios (respetando \%), conservando el numero de linea
clean = []
for i, ln in enumerate(lines, 1):
    ln = re.sub(r"(?<!\\)%.*$", "", ln)
    clean.append((i, ln))

texto = "\n".join(ln for _, ln in clean)


def linea_de(pos):
    return texto.count("\n", 0, pos) + 1


# --- segmentos matematicos -------------------------------------------------
segs = []  # (linea, contenido)
for m in re.finditer(r"(?<!\\)\$([^$]+)\$", texto):
    segs.append((linea_de(m.start()), m.group(1)))
for env in ("equation", "align", "equation\\*", "align\\*", "gather"):
    for m in re.finditer(r"\\begin\{%s\}(.*?)\\end\{%s\}" % (env, env),
                         texto, re.S):
        segs.append((linea_de(m.start()), m.group(1)))

print(f"{len(segs)} segmentos matematicos\n")

# --- tokens ---------------------------------------------------------------
TOK = re.compile(r"""
    \\(?:mathit|mathrm|mathcal|mathbf|mathbb|text|textit|mathsf)\{[^{}]*\}
  | \\(?:bar|hat|tilde|underline|overline|widetilde|widebar)\{[^{}]*\}
  | \\[A-Za-z]+
  | [A-Za-z]
""", re.X)

IGNORA = {
    # estructura, no notacion
    "\\label", "\\ref", "\\eqref", "\\quad", "\\qquad", "\\left", "\\right",
    "\\big", "\\Big", "\\bigl", "\\bigr", "\\begin", "\\end", "\\\\",
    "\\times", "\\cdot", "\\le", "\\leq", "\\ge", "\\geq", "\\neq", "\\in",
    "\\notin", "\\subset", "\\subseteq", "\\cup", "\\cap", "\\to", "\\mapsto",
    "\\approx", "\\sim", "\\pm", "\\mp", "\\dots", "\\ldots", "\\cdots",
    "\\forall", "\\exists", "\\land", "\\lor", "\\neg", "\\emptyset",
    "\\frac", "\\dfrac", "\\sqrt", "\\sum", "\\prod", "\\int", "\\lim",
    "\\max", "\\min", "\\argmin", "\\argmax", "\\log", "\\exp", "\\infty",
    "\\nonumber", "\\notag", "\\quad", "\\;", "\\,", "\\:", "\\!",
    "\\lfloor", "\\rfloor", "\\lceil", "\\rceil", "\\langle", "\\rangle",
    "\\colon", "\\mid", "\\setminus", "\\circ", "\\ast", "\\star",
    "\\displaystyle", "\\limits", "\\nolimits", "\\mathopen", "\\mathclose",
    "\\hspace", "\\vspace", "\\phantom", "\\text",
}

usos = defaultdict(list)
for ln, seg in segs:
    for m in TOK.finditer(seg):
        t = m.group(0)
        if t in IGNORA:
            continue
        usos[t].append(ln)

print("=== tokens por primera aparicion ===")
for t, ls in sorted(usos.items(), key=lambda kv: (min(kv[1]), kv[0])):
    ls_ord = sorted(set(ls))
    resto = "" if len(ls_ord) == 1 else f"  ... x{len(ls)} hasta L{ls_ord[-1]}"
    print(f"L{min(ls):>5}  {t:<28} n={len(ls):<4}{resto}")
