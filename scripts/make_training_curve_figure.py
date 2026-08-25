# -*- coding: utf-8 -*-
"""Figura de dinamica de entrenamiento del brazo principal (10 semillas).

Fuente: outputs/bench_v2-full-1000ep*/INT__*_training_log.csv, una fila
por episodio con el makespan del episodio y el mejor-hasta-ahora. El
entrenamiento procede por bloques (una instancia de entrenamiento cada
vez, TA11->TA14, pesos arrastrados), asi que el eje x concatena los
cuatro bloques de 1000 episodios. Todo en RE (%) del punto medio
contra la cota crisp publicada, como el resto del paper.

Salida: paper/figures/fig_training.pdf. No toca nada existente.
"""
import csv
import os
import sys

import numpy as np

sys.path.insert(0, ".")
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams.update({"font.family": "serif", "font.size": 8,
                            "pdf.fonttype": 42})
import matplotlib.pyplot as plt                                # noqa: E402

from jobshop_rl.data.literature_bounds import lb_for_problem_name  # noqa: E402

# Las semillas 2-4 (tiradas de julio) no registraron el log por
# episodio (cabecera sola): el registro se añadio despues. La curva
# usa las siete semillas de la extension, mismo brazo y protocolo.
SEMILLAS = {
    s: f"outputs/bench_v2-full-1000ep-ext-c__6de2c20__20260803_071159_seed{s}"
    for s in range(5, 12)
}
INSTANCIAS = [f"int__tai20_15_{i:02d}" for i in range(1, 5)]   # TA11-14
ETIQUETAS = ["TA11", "TA12", "TA13", "TA14"]
EP = 1000


def lee_semilla(directorio):
    """RE (%) del episodio y del mejor-hasta-ahora, bloques concatenados."""
    cur, mejor = [], []
    for pid in INSTANCIAS:
        lb = lb_for_problem_name(pid)
        nombre = pid.replace("int__", "INT__").upper() + ".F.15_01_INTERVAL"
        ruta = os.path.join(directorio, nombre + "_training_log.csv")
        filas = list(csv.DictReader(open(ruta)))
        assert len(filas) == EP, (ruta, len(filas))
        for r in filas:
            mid_c = (float(r["current_makespan_lower"])
                     + float(r["current_makespan_upper"])) / 2
            mid_b = (float(r["best_makespan_lower"])
                     + float(r["best_makespan_upper"])) / 2
            cur.append((mid_c - lb) / lb * 100)
            mejor.append((mid_b - lb) / lb * 100)
    return np.array(cur), np.array(mejor)


def suaviza(x, w=25):
    nucleo = np.ones(w) / w
    return np.convolve(x, nucleo, mode="same")


def main():
    curvas_c, curvas_b = [], []
    for sem, d in SEMILLAS.items():
        c, b = lee_semilla(d)
        curvas_c.append(c)
        curvas_b.append(b)
        print(f"semilla {sem}: RE final por bloque "
              f"{[round(float(b[k*EP-1]), 1) for k in range(1, 5)]}")
    C = np.vstack(curvas_c)     # (10, 4000) episodio
    B = np.vstack(curvas_b)     # (10, 4000) mejor-hasta-ahora

    x = np.arange(C.shape[1])
    fig, ax = plt.subplots(figsize=(4.8, 2.5))
    # episodio suavizado: media entre semillas, banda min-max
    Cs = np.vstack([suaviza(c) for c in C])
    ax.fill_between(x, Cs.min(0), Cs.max(0), color="#1f77b4", alpha=0.15,
                    linewidth=0)
    ax.plot(x, Cs.mean(0), color="#1f77b4", linewidth=0.9,
            label="episode RE (smoothed, seed range)")
    # mejor-hasta-ahora: media entre semillas
    ax.plot(x, B.mean(0), color="#d62728", linewidth=1.4,
            label="best-so-far RE (seed mean)")
    for k in range(1, 4):
        ax.axvline(k * EP, color="#999999", linewidth=0.6,
                   linestyle=(0, (2, 2)))
    for k, et in enumerate(ETIQUETAS):
        ax.text((k + 0.5) * EP, ax.get_ylim()[1] * 0.97, et,
                ha="center", va="top", fontsize=7, color="#555555")
    ax.set_xlabel("training episode (blocks of 1000 per instance, "
                  "weights carried over)")
    ax.set_ylabel("worst-case gap (%)")
    ax.set_xlim(0, 4 * EP)
    ax.legend(frameon=False, fontsize=7, loc="upper right",
              bbox_to_anchor=(1.0, 0.88))
    fig.tight_layout(pad=0.3)
    fig.savefig("paper/figures/fig_training.pdf")
    print("escrito paper/figures/fig_training.pdf")


if __name__ == "__main__":
    main()
