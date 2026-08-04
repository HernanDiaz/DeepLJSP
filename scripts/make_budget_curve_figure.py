# -*- coding: utf-8 -*-
"""Curva de presupuesto de inferencia: RE frente al numero de rollouts.

El paper solo tenia dos puntos de la politica (greedy y 1024 muestras) y
el lector no podia saber si el 1024 era necesario o si con 16 ya se
alcanzaba a la regla GP. Aqui se reconstruye el mejor-de-N para cualquier
N a partir de los rollouts individuales guardados por
eval_budget_curve.py, sin volver a evaluar nada.

El reparto del presupuesto imita el protocolo desplegado: B rollouts se
reparten lo mas uniformemente posible entre los tres checkpoints, y el
mejor global se toma al agregar. Como el reparto concreto y las muestras
elegidas son aleatorios, cada B se estima con R remuestreos SIN
reemplazo del deposito de 341 muestras por checkpoint; se dibuja la
media y la banda del 10 al 90 por ciento.

    python scripts/make_budget_curve_figure.py

Escribe paper/figures/fig_budget.pdf y deja en la salida estandar los
cruces con las referencias, que son lo que cita el texto.
"""
import collections
import csv
import sys

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

plt.rcParams.update({
    "font.family": "serif", "font.size": 9, "pdf.fonttype": 42,
    "axes.grid": True, "grid.alpha": 0.3, "grid.linewidth": 0.5,
})

CURVA = "benchmarks/eval_budget_curve.csv"
GP_DESTACADA = "benchmarks/reevo_fixedfit/summary.csv"
EST = "benchmarks/est_per_instance.csv"
SALIDA = "paper/figures/fig_budget.pdf"
N_POR_CKPT = 341          # muestras por checkpoint sin contar el greedy
R = 300                   # remuestreos por presupuesto
PRESUPUESTOS = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192,
                256, 384, 512, 768, 1023]


def lee_depositos():
    """{instancia: {'lb':, 'greedy': [3], 'pools': [3 x 341]}}."""
    filas = collections.defaultdict(lambda: collections.defaultdict(list))
    lbs, greedy = {}, collections.defaultdict(dict)
    with open(CURVA, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            inst, ck = r["instance"], r["checkpoint"]
            lbs[inst] = float(r["lb"])
            if int(r["sample_idx"]) == 0:
                greedy[inst][ck] = float(r["mid_comp"])
            else:
                filas[inst][ck].append(float(r["mid_comp"]))
    out = {}
    for inst, porck in filas.items():
        cks = sorted(porck)
        if len(cks) != 3 or any(len(porck[c]) < N_POR_CKPT for c in cks):
            continue          # par a medias: el barrido sigue corriendo
        out[inst] = {
            "lb": lbs[inst],
            "greedy": [greedy[inst][c] for c in cks],
            "pools": np.array([porck[c][:N_POR_CKPT] for c in cks]),
        }
    return out


def curva(dep, rng):
    """RE media sobre las instancias para cada presupuesto: (R, |B|)."""
    re = np.zeros((R, len(PRESUPUESTOS)))
    for datos in dep.values():
        pools, lb = datos["pools"], datos["lb"]
        for j, b in enumerate(PRESUPUESTOS):
            q, resto = divmod(b, 3)
            for r in range(R):
                cuenta = [q] * 3
                for c in rng.choice(3, resto, replace=False):
                    cuenta[c] += 1
                mejor = np.inf
                for c in range(3):
                    if cuenta[c]:
                        idx = rng.choice(N_POR_CKPT, cuenta[c], replace=False)
                        mejor = min(mejor, pools[c, idx].min())
                re[r, j] += (mejor - lb) / lb * 100
    return re / len(dep)


def referencias(instancias):
    """RE media de la regla DESTACADA y de EST sobre estas instancias.

    OJO con la fuente del GP. constructive_per_instance.csv tiene una
    columna GP_re que NO es la regla destacada: es gp_seed1, de otra
    campana, y da 18.59 sobre las 70 en vez de 17.71. Todo el paper lee
    la destacada de reevo_fixedfit/summary.csv filtrando gp_tuned_seed1,
    y esta figura tiene que leer lo mismo o su linea de referencia
    contradiria a la Tabla 9 sin que nadie lo note.
    """
    ta = {}
    with open(EST, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ta[r["instance"]] = (r["ta"], float(r["est_re"]))
    gp = {}
    with open(GP_DESTACADA, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["method"] == "gp_tuned_seed1":
                gp[r["instance"]] = float(r["re"])
    est_v = [ta[i][1] for i in instancias if i in ta]
    gp_v = [gp[i] for i in instancias if i in gp]
    return (float(np.mean(gp_v)) if gp_v else None,
            float(np.mean(est_v)) if est_v else None,
            len(gp_v), len(est_v))


def cruce(xs, ys, umbral):
    """Primer presupuesto cuya RE media baja del umbral."""
    for x, y in zip(xs, ys):
        if y <= umbral:
            return x
    return None


def main():
    dep = lee_depositos()
    if not dep:
        sys.exit("ABORTA: ningun par completo todavia")
    instancias = sorted(dep)
    print(f"{len(instancias)} instancias con las tres semillas completas")

    rng = np.random.RandomState(20260803)
    re = curva(dep, rng)
    media = re.mean(axis=0)
    p10, p90 = np.percentile(re, 10, axis=0), np.percentile(re, 90, axis=0)
    greedy = float(np.mean([(min(d["greedy"]) - d["lb"]) / d["lb"] * 100
                            for d in dep.values()]))
    gp, est, n_gp, n_est = referencias(instancias)
    print(f"referencias sobre el mismo conjunto: GP {gp:.2f}% (n={n_gp}), "
          f"EST {est:.2f}% (n={n_est}), greedy de 3 semillas {greedy:.2f}%")
    for b, m in zip(PRESUPUESTOS, media):
        print(f"  B={b:5d}  RE={m:6.2f}%")
    print(f"cruza EST    con B={cruce(PRESUPUESTOS, media, est)}")
    print(f"cruza GP     con B={cruce(PRESUPUESTOS, media, gp)}")
    print(f"cruza greedy con B={cruce(PRESUPUESTOS, media, greedy)}")
    if len(instancias) < 70:
        print(f"AVISO: solo {len(instancias)}/70 instancias. Las que faltan "
              "son las grandes, donde la politica es mas debil: estos "
              "numeros son optimistas y la figura NO debe entrar al paper "
              "hasta que el barrido termine.")

    fig, ax = plt.subplots(figsize=(3.4, 2.6))
    ax.fill_between(PRESUPUESTOS, p10, p90, color="#1f77b4", alpha=0.18,
                    linewidth=0)
    ax.plot(PRESUPUESTOS, media, color="#1f77b4", linewidth=1.6,
            label="policy, best of $B$")
    # EST queda en el 42 por ciento: dibujarla aplastaria todo lo demas,
    # asi que el pie la nombra y el eje se reserva para la zona util.
    ax.axhline(gp, color="#d62728", linestyle="--", linewidth=1.1,
               label=f"GP rule ({gp:.1f}%)")
    # el greedy se agrega como la curva, quedandose con el mejor de los
    # tres checkpoints; el 19.4 de 6.4 es la MEDIA de las tres semillas,
    # otra cosa, y la etiqueta lo dice para que no se confundan
    ax.axhline(greedy, color="#2ca02c", linestyle=":", linewidth=1.1,
               label=f"greedy, best of 3 seeds ({greedy:.1f}%)")
    ax.set_xscale("log", base=2)
    ax.set_xlabel("inference budget $B$ (rollouts)")
    ax.set_ylabel("mean RE (%)")
    ax.set_xticks([1, 4, 16, 64, 256, 1024])
    ax.set_xticklabels(["1", "4", "16", "64", "256", "1024"])
    ax.legend(frameon=False, fontsize=7.5, loc="upper right")
    fig.tight_layout(pad=0.3)
    fig.savefig(SALIDA)
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
