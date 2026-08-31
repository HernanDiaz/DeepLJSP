# -*- coding: utf-8 -*-
"""Figura del schedule semiactivo con duraciones intervalares.

La seccion del problema explicaba solo en prosa que los inicios y
finales de cada operacion son intervalos. La figura los dibuja con la
convencion habitual del Gantt intervalar: cada operacion es un
poligono cuyo flanco izquierdo asciende desde el suelo en s^L hasta el
techo en s^U, y cuyo flanco derecho desciende desde el techo en e^L
hasta el suelo en e^U. La meseta superior es el tramo en que la
operacion ocupa la maquina con certeza; los flancos, la holgura con
que puede empezar y acabar.

Se construye con el MISMO entorno que el resto del paper, de modo que
lo dibujado es lo que el codigo calcula.

    python scripts/make_gantt_figure.py

Escribe paper/figures/fig_gantt.pdf
"""
import sys

import matplotlib

sys.path.insert(0, ".")
matplotlib.use("Agg")
import matplotlib.pyplot as plt                            # noqa: E402
from matplotlib.patches import Polygon                     # noqa: E402

from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.models.interval import (                    # noqa: E402
    Interval, final_makespan)

plt.rcParams.update({"font.family": "serif", "font.size": 8,
                     "pdf.fonttype": 42})

SALIDA = "paper/figures/fig_gantt.pdf"
SEQ = [[0, 1, 2], [1, 0, 2], [2, 1, 0]]
# Duraciones intervalares estrechas frente a la duracion, como en
# el benchmark. Estan elegidas para que los dos extremos del
# makespan vengan de trabajos distintos: el trabajo 2 acaba en
# [26,34] y el 3 en [25,35], de modo que el maximo del extremo
# inferior y el del superior no son el mismo trabajo y el maximo
# componente a componente de la Ec. (2) no es el fin de ninguna
# operacion concreta.
DUR = [[Interval(5, 7), Interval(5, 7), Interval(6, 8)],
       [Interval(7, 9), Interval(9, 13), Interval(8, 10)],
       [Interval(11, 15), Interval(5, 7), Interval(8, 12)]]
ORDEN = [0, 1, 2, 0, 1, 2, 0, 1, 2]
COLOR = ["#4C72B0", "#DD8452", "#55A868"]
ALTO = 0.40
EJEMPLO_FIN = []


def extremos(v):
    if isinstance(v, Interval):
        return float(v.lower), float(v.upper)
    return float(v), float(v)


def perfil(s_lo, s_up, e_lo, e_up, base):
    """Vertices del poligono de una operacion.

    El lado superior va de s^L a e^L y el inferior de s^U a e^U,
    de modo que el borde de arriba es el schedule que resulta si
    toda duracion toma su extremo inferior y el de abajo el que
    resulta si toma el superior. Los dos flancos descienden. El
    eje y se dibuja invertido, asi que el suelo de la barra es la
    coordenada mayor.
    """
    suelo, techo = base + ALTO / 2, base - ALTO / 2
    return [(s_lo, techo), (e_lo, techo), (e_up, suelo),
            (s_up, suelo)]

def construye():
    problema = {"num_jobs": 3, "num_machines": 3, "sequences": SEQ,
                "durations": DUR, "problem_id": "ejemplo3x3"}
    env = EnvironmentFactory.create_from_problem(problema, "basic", seed=0)
    env.reset()
    for trabajo in ORDEN:
        env.step(list(env.eligible_ops).index(trabajo))
    global EJEMPLO_FIN
    EJEMPLO_FIN = list(env.job_completion_time)
    return env.schedule_history, extremos(final_makespan(
        env.job_completion_time))


def main():
    sched, (c_lo, c_up) = construye()

    fig, ax = plt.subplots(figsize=(6.53, 1.95))
    for op in sched:
        s_lo, s_up = extremos(op["start"])
        e_lo, e_up = extremos(op["end"])
        y = op["machine"]
        col = COLOR[op["job"]]
        ax.add_patch(Polygon(perfil(s_lo, s_up, e_lo, e_up, y),
                             closed=True, facecolor=col, alpha=0.75,
                             edgecolor=col, linewidth=1.0,
                             zorder=2))
        ax.text((s_lo + s_up + e_lo + e_up) / 4, y,
                f"$o_{{{op['job'] + 1}{op['operation'] + 1}}}$",
                ha="center", va="center", fontsize=7, color="white",
                zorder=3)

    ax.axvline(c_lo, color="0.30", linestyle="--", linewidth=1.0,
               zorder=1)
    ax.axvline(c_up, color="0.15", linestyle="-", linewidth=1.2,
               zorder=1)
    ax.annotate("", xy=(c_lo, -0.62), xytext=(c_up, -0.62),
                arrowprops=dict(arrowstyle="<->", color="0.25", lw=0.9))
    ax.text((c_lo + c_up) / 2, -0.68,
            f"$\\mathbf{{C}}_{{\\max}}=[{c_lo:.0f},\\,{c_up:.0f}]$",
            ha="center", va="bottom", fontsize=8)

    ax.set_yticks(range(3))
    ax.set_yticklabels([f"$M_{i + 1}$" for i in range(3)])
    ax.set_ylim(-1.05, 2.45)
    ax.set_xlim(0, c_up + 0.5)
    ax.set_xlabel("time")
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.3, linestyle=":", linewidth=0.6)
    fig.tight_layout()
    fig.savefig(SALIDA, bbox_inches="tight")
    plt.close(fig)
    print(f"makespan componentwise: [{c_lo:.0f}, {c_up:.0f}]")
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
