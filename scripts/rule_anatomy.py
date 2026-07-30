"""
Anatomía e interpretabilidad de las reglas GP evolucionadas.

Sobre un conjunto de reglas (JSON con árbol): frecuencia de uso de cada
terminal (¿explotan la anchura del intervalo?), distribución del tamaño de
árbol (bloat / legibilidad), y profundidad. Es el análisis que SSHE/Gil-Gala
hacen su bandera. Salida: tabla por consola + benchmarks/rule_anatomy.csv +
figura de frecuencia de terminales.

Uso:
  python scripts/rule_anatomy.py benchmarks/gp_rule_seed*.json
  python scripts/rule_anatomy.py benchmarks/reevo_fixedfit/gp_rule_seed*.json
"""

import glob
import json
import os
import sys

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.heuristics.gp_rule import TERMINALS, tree_size  # noqa: E402

WIDTH_TERMS = {"PTW", "ESTW", "WKRW"}


def walk(tree):
    """Genera todos los nodos (str terminal u operador str) del árbol."""
    if isinstance(tree, str):
        yield tree
    else:
        yield tree[0]
        for child in tree[1:]:
            yield from walk(child)


def depth(tree):
    if isinstance(tree, str):
        return 1
    return 1 + max(depth(c) for c in tree[1:])


def main():
    patterns = sys.argv[1:] or ["benchmarks/gp_rule_seed*.json"]
    paths = sorted(p for pat in patterns for p in glob.glob(pat))
    if not paths:
        print("sin reglas"); return

    term_count = {t: 0 for t in TERMINALS}
    rules_using_width = 0
    sizes, depths = [], []
    rows = []
    for path in paths:
        tree = json.load(open(path, encoding="utf-8"))["tree"]
        nodes = list(walk(tree))
        terms = [n for n in nodes if n in TERMINALS]
        for t in terms:
            term_count[t] += 1
        uses_w = any(t in WIDTH_TERMS for t in terms)
        rules_using_width += int(uses_w)
        sz, dp = tree_size(tree), depth(tree)
        sizes.append(sz); depths.append(dp)
        rows.append({"rule": os.path.basename(path), "size": sz, "depth": dp,
                     "n_terminals": len(terms),
                     "width_terms": sum(1 for t in terms if t in WIDTH_TERMS)})

    n = len(paths)
    total_terms = sum(term_count.values())
    print(f"=== Anatomía de {n} reglas ===")
    print(f"tamaño de árbol: media {sum(sizes)/n:.1f}, min {min(sizes)}, "
          f"max {max(sizes)}")
    print(f"profundidad: media {sum(depths)/n:.1f}, min {min(depths)}, "
          f"max {max(depths)}")
    print(f"reglas que usan >=1 terminal de anchura: {rules_using_width}/{n} "
          f"({100*rules_using_width/n:.0f}%)")
    print("\nfrecuencia de terminales (share del total de terminales):")
    for t in sorted(TERMINALS, key=lambda x: -term_count[x]):
        share = 100 * term_count[t] / total_terms if total_terms else 0
        tag = " [width]" if t in WIDTH_TERMS else ""
        print(f"  {t:<6} {term_count[t]:>4}  ({share:4.1f}%){tag}")
    w_share = 100 * sum(term_count[t] for t in WIDTH_TERMS) / total_terms
    print(f"\nshare total de terminales de ANCHURA: {w_share:.1f}%")

    os.makedirs("benchmarks", exist_ok=True)
    with open("benchmarks/rule_anatomy.csv", "w", encoding="utf-8") as f:
        f.write("rule,size,depth,n_terminals,width_terms\n")
        for r in rows:
            f.write(f"{r['rule']},{r['size']},{r['depth']},"
                    f"{r['n_terminals']},{r['width_terms']}\n")

    _figure(term_count, total_terms)
    print("\nCSV: benchmarks/rule_anatomy.csv")


def _figure(term_count, total_terms):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # mismo esquema que el resto de las figuras del paper: la figura se genera
    # al ancho al que se imprime, asi que 8 pt es lo que llega al papel. Antes
    # no se fijaba y el defecto de 10 acababa imprimiendose a 6.2 pt.
    plt.rcParams.update({"font.size": 8.0, "figure.facecolor": "white"})

    os.makedirs("paper_gp/figures", exist_ok=True)
    order = sorted(TERMINALS, key=lambda x: -term_count[x])
    shares = [100 * term_count[t] / total_terms if total_terms else 0
              for t in order]
    colors = ["#d68910" if t in WIDTH_TERMS else "#5d6d7e" for t in order]
    fig, ax = plt.subplots(figsize=(3.99, 2.12))
    ax.bar(range(len(order)), shares, color=colors)
    ax.set_xticks(range(len(order)))
    # a 8 pt y con el lienzo al ancho impreso, ESTW y WKRW se tocaban
    ax.set_xticklabels(order, rotation=30, ha="right")
    ax.set_ylabel("share of terminals (%)")
    ax.spines[["top", "right"]].set_visible(False)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color="#d68910", label="interval width"),
                       Patch(color="#5d6d7e", label="other")],
              frameon=False, fontsize=7.5)
    fig.tight_layout()
    fig.savefig("paper_gp/figures/fig_terminals.pdf")
    plt.close(fig)
    print("fig_terminals ok")


if __name__ == "__main__":
    main()
