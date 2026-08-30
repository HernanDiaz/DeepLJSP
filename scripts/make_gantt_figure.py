# -*- coding: utf-8 -*-
"""Figura del schedule semiactivo con duraciones intervalares.

La seccion del problema explicaba solo en prosa que un procesamiento
fijado bajo duraciones intervalares no da UN schedule sino una familia
de ellos, acotada por dos esquinas: la que toma todas las duraciones
en su extremo inferior y la que las toma en el superior. Por monotonia
de la recursion, cualquier realizacion cae entre las dos, y el
makespan agrega los dos extremos por separado.

La figura dibuja esas dos esquinas para el mismo orden de despacho,
construidas con el MISMO entorno que el resto del paper.

    python scripts/make_gantt_figure.py

Escribe paper/figures/fig_gantt.pdf
"""
import sys

import matplotlib

sys.path.insert(0, ".")
matplotlib.use("Agg")
import matplotlib.pyplot as plt                            # noqa: E402
from matplotlib.patches import Patch                       # noqa: E402

from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.models.interval import (                    # noqa: E402
    Interval, final_makespan)

plt.rcParams.update({"font.family": "serif", "font.size": 10,
                     "pdf.fonttype": 42})

SALIDA = "paper/figures/fig_gantt.pdf"
SEQ = [[0, 1, 2], [1, 0, 2], [2, 1, 0]]
DUR = [[Interval(3, 5), Interval(2, 4), Interval(4, 6)],
       [Interval(4, 6), Interval(3, 4), Interval(2, 5)],
       [Interval(3, 4), Interval(5, 7), Interval(2, 3)]]
ORDEN = [0, 1, 2, 0, 1, 2, 0, 1, 2]
COLOR = ["#4C72B0", "#DD8452", "#55A868"]


def extremos(v):
    if isinstance(v, Interval):
        return float(v.lower), float(v.upper)
    return float(v), float(v)


def construye():
    problema = {"num_jobs": 3, "num_machines": 3, "sequences": SEQ,
                "durations": DUR, "problem_id": "ejemplo3x3"}
    env = EnvironmentFactory.create_from_problem(problema, "basic", seed=0)
    env.reset()
    for trabajo in ORDEN:
        elegibles = list(env.eligible_ops)
        env.step(elegibles.index(trabajo))
    mk = final_makespan(env.job_completion_time)
    return env.schedule_history, extremos(mk)


def main():
    sched, (c_lo, c_up) = construye()

    fig, ax = plt.subplots(figsize=(6.53, 2.9))
    # cada maquina ocupa dos carriles: la esquina inferior arriba y la
    # superior debajo, para leerlas apiladas
    alto, sep = 0.30, 0.34
    for op in sched:
        s_lo, s_up = extremos(op["start"])
        e_lo, e_up = extremos(op["end"])
        y = op["machine"]
        col = COLOR[op["job"]]
        etiqueta = f"$O_{{{op['job'] + 1}{op['operation'] + 1}}}$"
        for base, ini, fin, alfa in ((y - sep / 2, s_lo, e_lo, 0.45),
                                     (y + sep / 2, s_up, e_up, 1.0)):
            ax.broken_barh([(ini, fin - ini)], (base - alto / 2, alto),
                           facecolors=col, alpha=alfa, edgecolor="white",
                           linewidth=0.7)
            if fin - ini >= 2.2:
                ax.text((ini + fin) / 2, base, etiqueta, ha="center",
                        va="center", fontsize=8, color="white")

    ax.axvline(c_lo, color="0.30", linestyle="--", linewidth=1.0)
    ax.axvline(c_up, color="0.15", linestyle="-", linewidth=1.2)
    ax.annotate("", xy=(c_lo, -0.92), xytext=(c_up, -0.92),
                arrowprops=dict(arrowstyle="<->", color="0.25", lw=0.9))
    ax.text((c_lo + c_up) / 2, -1.04,
            f"$\\mathbf{{C}}_{{\\max}}=[{c_lo:.0f},\\,{c_up:.0f}]$",
            ha="center", va="bottom", fontsize=9.5)

    ax.set_yticks(range(3))
    ax.set_yticklabels([f"$M_{i + 1}$" for i in range(3)])
    ax.set_ylim(-1.15, 2.62)
    ax.set_xlim(0, c_up + 0.5)
    ax.set_xlabel("time")
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.3, linestyle=":", linewidth=0.6)
    leyenda = [Patch(facecolor="0.45", alpha=0.45,
                     label="all durations at their lower endpoint"),
               Patch(facecolor="0.25",
                     label="all durations at their upper endpoint")]
    ax.legend(handles=leyenda, frameon=False, fontsize=8.5, ncol=2,
              loc="upper center", bbox_to_anchor=(0.5, 1.24))
    fig.tight_layout()
    fig.savefig(SALIDA, bbox_inches="tight")
    plt.close(fig)
    print(f"makespan componentwise: [{c_lo:.0f}, {c_up:.0f}]")
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
