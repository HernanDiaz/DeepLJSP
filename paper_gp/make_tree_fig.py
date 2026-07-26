# -*- coding: utf-8 -*-
"""Genera el codigo TikZ del arbol de una regla evolucionada (JSON -> .tex).

Calcula el layout explicitamente (hojas equiespaciadas, padre centrado sobre
sus hijos) en vez de usar la sintaxis 'child' de TikZ, que espacia mal los
arboles profundos. Salida: paper_gp/figures/tree_seed27.tex (fragmento
tikzpicture, listo para \\input o para pegar).
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SYM = {"add": "$+$", "sub": "$-$", "mul": "$\\times$", "div": "$\\div$",
       "min": "min", "max": "max", "neg": "neg"}


def build(tree, out, depth=0, counter=[0]):
    """Devuelve (id, x) asignando x a las hojas por orden de aparicion."""
    nid = f"n{counter[0]}"; counter[0] += 1
    if isinstance(tree, str):
        x = build.leaf; build.leaf += 1
        out.append((nid, x, depth, tree, True))
        return nid, x
    kids = [build(c, out, depth + 1, counter) for c in tree[1:]]
    x = sum(k[1] for k in kids) / len(kids)
    out.append((nid, x, depth, SYM.get(tree[0], tree[0]), False))
    for kid_id, _ in kids:
        build.edges.append((nid, kid_id))
    return nid, x


def emit(path_json, path_out, xs=0.62, ys=0.86):
    tree = json.load(open(path_json, encoding="utf-8"))["tree"]
    nodes = []
    build.leaf = 0
    build.edges = []
    build(tree, nodes)

    L = [
        "\\begin{tikzpicture}[",
        "  op/.style={circle, draw, inner sep=0.6pt, minimum size=3.6mm,",
        "             font=\\scriptsize},",
        "  term/.style={rectangle, draw, rounded corners=1pt, inner sep=1.2pt,",
        "               font=\\tiny\\itshape, fill=black!5}]",
    ]
    for nid, x, d, label, is_leaf in nodes:
        style = "term" if is_leaf else "op"
        L.append(f"  \\node[{style}] ({nid}) at ({x * xs:.2f},{-d * ys:.2f}) "
                 f"{{{label}}};")
    for a, b in build.edges:
        L.append(f"  \\draw ({a}) -- ({b});")
    L.append("\\end{tikzpicture}")

    os.makedirs(os.path.dirname(path_out), exist_ok=True)
    with open(path_out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    w = max(n[1] for n in nodes) * xs
    h = max(n[2] for n in nodes) * ys
    print(f"{len(nodes)} nodos -> {path_out}  ({w:.1f}cm x {h:.1f}cm)")


if __name__ == "__main__":
    HERE = os.path.dirname(os.path.abspath(__file__))
    emit(os.path.join(os.path.dirname(HERE),
                      "benchmarks/reevo_fixedfit/gp_rule_seed27.json"),
         os.path.join(HERE, "figures/tree_seed27.tex"))
