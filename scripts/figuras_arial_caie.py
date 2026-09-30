# -*- coding: utf-8 -*-
"""Regenera las figuras de matplotlib del articulo de C&IE en Arial.

Elsevier pide en sus figuras Arial (o Helvetica), Courier, Symbol o
Times, o tipografias parecidas; las nuestras salian en DejaVu Sans, la de
matplotlib por defecto. Los scripts de figuras de paper_gp escriben en
paper_gp/figures, que no se toca, asi que aqui se ejecutan tal cual con
tres cambios alrededor, sin editarlos:

  - la tipografia por defecto pasa a Arial (sans-serif, 8 pt como antes);
  - todo savefig que apunte a paper_gp/figures se desvia a
    paper_caie/figures;
  - cualquier otra escritura de fichero se desvia a una carpeta temporal,
    para que ni paper_gp ni los resultados de benchmarks cambien.

Las dos figuras propias de C&IE (presupuesto y convergencia) se generan
con sus scripts, que ya escriben en paper_caie y toman la tipografia de
aqui.

    python scripts/figuras_arial_caie.py

Escribe paper_caie/figures/fig_*.pdf
"""
import builtins
import os
import runpy
import sys
import tempfile

import matplotlib

matplotlib.use("Agg")
import matplotlib.figure                                          # noqa: E402
import matplotlib.pyplot as plt                                   # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(REPO, "paper_caie", "figures")
TEMPORAL = tempfile.mkdtemp(prefix="figuras_caie_")

# (script, argumentos, figura que debe salir)
SCRIPTS = [
    ("paper_gp/make_lambda_fig.py", [], "fig_lambda.pdf"),
    ("paper_gp/make_sensitivity_fig.py", [], "fig_sensitivity.pdf"),
    ("paper_gp/make_robustness_fig.py", [], "fig_robustness_box.pdf"),
    # fig_case.pdf: scripts/make_e3_figure_caie.py, con SPT y MWKR, que
    # ya fija Arial y escribe en paper_caie/figures
    ("scripts/rule_anatomy.py",
     ["benchmarks/reevo_fixedfit/gp_tuned_seed*.json"], "fig_terminals.pdf"),
    ("scripts/make_convergence_caie.py", [], "fig_convergence.pdf"),
    # fig_budget.pdf: scripts/make_e6_figure_caie.py, que ya fija Arial y
    # se lanza aparte cuando las curvas de E6 estan completas
]

ARIAL = {"font.family": "sans-serif",
         "font.sans-serif": ["Arial"],
         "mathtext.fontset": "custom",
         "mathtext.rm": "Arial", "mathtext.it": "Arial:italic",
         "mathtext.bf": "Arial:bold", "pdf.fonttype": 42}

_savefig = matplotlib.figure.Figure.savefig
_open = builtins.open
escritas = []


def _a_caie(ruta):
    r = os.path.abspath(str(ruta))
    base = os.path.basename(r)
    if base.startswith("fig_") and r.lower().endswith(".pdf"):
        return os.path.join(DESTINO, base)
    return None


def savefig(self, fname, *a, **k):
    nuevo = _a_caie(fname)
    assert nuevo, f"figura fuera de lo previsto: {fname}"
    escritas.append(os.path.basename(nuevo))
    return _savefig(self, nuevo, *a, **k)


def abre(file, mode="r", *a, **k):
    if isinstance(file, (str, bytes, os.PathLike)) and any(
            c in mode for c in "wax"):
        r = os.path.abspath(os.fsdecode(file))
        if not r.startswith(DESTINO + os.sep):
            file = os.path.join(TEMPORAL, os.path.basename(r))
    return _open(file, mode, *a, **k)


def main():
    os.chdir(REPO)
    matplotlib.figure.Figure.savefig = savefig
    builtins.open = abre
    for script, args, figura in SCRIPTS:
        plt.rcdefaults()
        plt.rcParams.update(ARIAL)
        # los scripts llaman a rcParams.update con su tamano y fonttype,
        # que no tocan la familia; se reimpone por si alguno la fijara
        sys.argv = [script] + args
        antes = len(escritas)
        runpy.run_path(script, run_name="__main__")
        assert figura in escritas[antes:], f"{script} no escribio {figura}"
        plt.close("all")
    builtins.open = _open
    matplotlib.figure.Figure.savefig = _savefig
    print(f"figuras: {sorted(set(escritas))}; otras escrituras en {TEMPORAL}")


if __name__ == "__main__":
    main()
