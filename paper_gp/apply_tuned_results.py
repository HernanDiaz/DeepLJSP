# -*- coding: utf-8 -*-
"""Vuelca los resultados de la campana tuneada en el paper.

Lee benchmarks/tuned/RESULTADOS.md (lo escribe scripts/tuned_campaign.py al
terminar la fase 2) y actualiza:

  * tab:ablation           -- los cuatro brazos y los dos tests
  * el texto de 7.2        -- las cifras citadas en prosa
  * benchmarks/lambda_sweep/lambda_sweep_tuned.csv y fig:lambda

Cada sustitucion es una asercion: si el texto no esta como se espera, aborta
sin escribir en vez de dejar el paper a medias. No toca el CSV del barrido
anterior, que se conserva.

Uso:  python paper_gp/apply_tuned_results.py [--dry]
"""

import argparse
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
RES = os.path.join(REPO, "benchmarks/tuned/RESULTADOS.md")
TEX = os.path.join(HERE, "main.tex")
CSV = os.path.join(REPO, "benchmarks/lambda_sweep/lambda_sweep_tuned.csv")

NUM = r"([\d.]+) ± ([\d.]+)"


def parse():
    if not os.path.exists(RES):
        sys.exit(f"todavia no existe {RES}: la fase 2 no ha terminado")
    txt = open(RES, encoding="utf-8").read()
    d = {}

    def row(name):
        m = re.search(r"\|\s*" + re.escape(name) + r"\s*\|\s*(\d+)\s*\|\s*"
                      + NUM + r"\s*\|\s*" + NUM, txt)
        if not m:
            sys.exit(f"no encuentro la fila '{name}' en RESULTADOS.md")
        return dict(n=int(m.group(1)),
                    re=(float(m.group(2)), float(m.group(3))),
                    w=(float(m.group(4)), float(m.group(5))))

    for key, name in (("full", "full (tuned)"), ("nowidth", "no-width (tuned)"),
                      ("rob_w", "robust+width"), ("rob_nw", "robust+nowidth")):
        d[key] = row(name)

    m = re.search(r"Wilcoxon pareado no-width vs full: RE z=(-?[\d.]+), "
                  r"ancho z=(-?[\d.]+)", txt)
    if not m:
        sys.exit("no encuentro el Wilcoxon del objetivo makespan")
    d["z_re"], d["z_w"] = float(m.group(1)), float(m.group(2))

    m = re.search(r"Wilcoxon pareado sobre el ancho \(nowidth - width\): "
                  r"z=(-?[\d.]+)", txt)
    if not m:
        sys.exit("no encuentro el Wilcoxon del objetivo robusto")
    d["z_rob"] = float(m.group(1))

    d["lambda"] = []
    for m in re.finditer(r"\|\s*([\d.]+)\s*\|\s*(\d+)\s*\|\s*" + NUM
                         + r"\s*\|\s*" + NUM + r"\s*\|", txt):
        lam = float(m.group(1))
        if lam in (0.5, 1.0, 2.0, 4.0):
            d["lambda"].append((lam, int(m.group(2)),
                                float(m.group(3)), float(m.group(4)),
                                float(m.group(5)), float(m.group(6))))
    if len(d["lambda"]) != 4:
        sys.exit(f"esperaba 4 valores de lambda, encontre {len(d['lambda'])}")
    return d


def f(pair):
    return f"{pair[0]:.2f} \\pm {pair[1]:.2f}"


def verdict(z):
    """Celda de test a partir del |z| de la normal, en vez de dar por hecho
    el resultado: con la configuracion tuneada el ancho bajo objetivo makespan
    pasa de n.s. a significativo, y hardcodear 'n.s.' habria impreso una
    conclusion falsa junto a su propio z."""
    a = abs(z)
    if a > 3.29:
        return f"$z={z:.2f}$, $p<0.001$"
    if a > 2.58:
        return f"$z={z:.2f}$, $p<0.01$"
    if a > 1.96:
        return f"$z={z:.2f}$, $p<0.05$"
    return f"\\textit{{n.s.}} ($z={z:.2f}$)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()
    d = parse()

    for k in ("full", "nowidth", "rob_w", "rob_nw"):
        v = d[k]
        print(f"  {k:<8} n={v['n']:<3} RE {f(v['re'])}   ancho {f(v['w'])}")
    print(f"  z: makespan RE {d['z_re']}, ancho {d['z_w']}; "
          f"robusto ancho {d['z_rob']}")
    if args.dry:
        return

    t = open(TEX, encoding="utf-8").read()

    def sub(old, new):
        nonlocal t
        if old not in t:
            sys.exit("NO ENCONTRADO en main.tex:\n" + old[:120])
        t = t.replace(old, new, 1)

    # --- tab:ablation -----------------------------------------------------
    sub(""" & full & $18.68 \\pm 0.84$ & $12.38 \\pm 0.31$ \\\\
 & without widths & $18.39 \\pm 0.59$ & $12.38 \\pm 0.22$ \\\\
 & \\textit{test} & \\textit{n.s.} ($z=1.26$) & \\textit{n.s.} ($z=-0.12$) \\\\""",
        f""" & full & ${f(d['full']['re'])}$ & ${f(d['full']['w'])}$ \\\\
 & without widths & ${f(d['nowidth']['re'])}$ & ${f(d['nowidth']['w'])}$ \\\\
 & \\textit{{test}} & {verdict(d['z_re'])} & {verdict(d['z_w'])} \\\\""")

    sub(""" & full & $19.64 \\pm 1.28$ & $\\mathbf{12.01 \\pm 0.74}$ \\\\
 & without widths & $18.70 \\pm 0.89$ & $12.42 \\pm 0.21$ \\\\
 & \\textit{test} & --- & $z=2.73$, $p<0.01$ \\\\""",
        f""" & full & ${f(d['rob_w']['re'])}$ & $\\mathbf{{{f(d['rob_w']['w'])}}}$ \\\\
 & without widths & ${f(d['rob_nw']['re'])}$ & ${f(d['rob_nw']['w'])}$ \\\\
 & \\textit{{test}} & --- & {verdict(d['z_rob'])} \\\\""")

    # --- texto de 7.2 -----------------------------------------------------
    sub(f"""performance unchanged: $18.39 \\pm 0.59$ mean $\\RE$ over the 70 instances without
them versus $18.68 \\pm 0.84$ with them, a difference that is not
significant ($z=1.26$)""",
        f"""performance unchanged: ${f(d['nowidth']['re'])}$ mean $\\RE$ over the 70
instances without them versus ${f(d['full']['re'])}$ with them, a difference
that is not significant ($z={d['z_re']:.2f}$)""")

    sub("""($12.38 \\pm 0.31$ with the width terminals versus $12.38 \\pm 0.22$
without them)""",
        f"""(${f(d['full']['w'])}$ with the width terminals versus
${f(d['nowidth']['w'])}$ without them)""")

    sub(f"""them ($12.01 \\pm 0.74$ versus $12.42 \\pm 0.21$ relative width; paired
Wilcoxon $z=2.73$, $p<0.01$)""",
        f"""them (${f(d['rob_w']['w'])}$ versus ${f(d['rob_nw']['w'])}$ relative
width; paired Wilcoxon $z={d['z_rob']:.2f}$)""")

    sub("""paid for in expected makespan ($19.64$ versus $18.70$ $\\RE$)""",
        f"""paid for in expected makespan (${d['rob_w']['re'][0]:.2f}$ versus """
        f"""${d['rob_nw']['re'][0]:.2f}$ $\\RE$)""")

    open(TEX, "w", encoding="utf-8", newline="\n").write(t)
    print("tab:ablation y el texto de 7.2 actualizados")

    # --- barrido de lambda -> figura --------------------------------------
    with open(CSV, "w", encoding="utf-8", newline="") as fh:
        fh.write("lambda,n,re_mean,re_sd,width_mean,width_sd\n")
        for lam, n, rm, rs, wm, ws in sorted(d["lambda"]):
            fh.write(f"{lam},{n},{rm:.4f},{rs:.4f},{wm:.4f},{ws:.4f}\n")
    print(f"barrido -> {CSV}")
    print("  ahora: apunta make_lambda_fig.py a ese CSV, ajusta la linea de"
          " referencia al ancho del brazo no-width y regenera")


if __name__ == "__main__":
    main()
