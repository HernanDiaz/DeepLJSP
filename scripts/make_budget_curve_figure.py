# -*- coding: utf-8 -*-
"""Curva de presupuesto de inferencia: RE frente al numero de rollouts.

El paper solo tenia dos puntos de la politica (greedy y 1024 muestras) y
el lector no podia saber si el 1024 era necesario o si con 16 ya se
alcanzaba a la regla GP. Aqui se reconstruye el mejor-de-N para cualquier
N a partir de los rollouts individuales guardados por
eval_budget_curve.py (tres tiradas) y eval_curva_diez.py (siete mas),
sin volver a evaluar nada.

Desde 2026-08-18 el reparto imita el protocolo DESPLEGADO de verdad:
una politica gasta sus B muestras. Cada tirada da su curva, extraida
sin reemplazo de su pool de 341, y la figura dibuja la media de las
diez con la banda entre la mejor y la peor: la dispersion que
afrontaria quien entrena una sola vez. El reparto anterior entre tres
checkpoints era un artefacto del barrido bo1024 original y prestaba a
la curva la diversidad de un comite que el despliegue no tiene.

    python scripts/make_budget_curve_figure.py

Escribe paper/figures/fig_budget.pdf y deja en la salida estandar los
cruces con las referencias, que son lo que cita el texto.
"""
import collections
import csv
import glob
import sys

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

plt.rcParams.update({
    "font.family": "serif", "font.size": 10, "pdf.fonttype": 42,
    "axes.grid": True, "grid.alpha": 0.3, "grid.linewidth": 0.5,
})

# deposito con extremos (2026-08-26): las diez tiradas, greedy
# incluido en el pool y seleccion por (U, L), el protocolo de 5.4
CURVAS = sorted(glob.glob("benchmarks/curva_intervalo/curva_*.csv"))
GP_DESTACADA = "benchmarks/reevo_fixedfit/summary.csv"
# el deposito muestreado de la MISMA regla publicada, con los dos
# extremos de sus 1024 rollouts por instancia: permite trazar su
# curva a presupuesto igualado en vez de una sola linea horizontal
GP_POOL = sorted(glob.glob("benchmarks/gp_destacada/pool_*.csv"))
EST = "benchmarks/est_per_instance.csv"
SALIDA = "paper/figures/fig_budget.pdf"
N_POOL = 341              # muestras por tirada sin contar el greedy
R = 200                   # remuestreos por presupuesto y tirada
PRESUPUESTOS = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192,
                256, 341]


def lee_depositos():
    """{tirada: {instancia: {'lb':, 'greedy':, 'pool': [341]}}}."""
    filas = collections.defaultdict(lambda: collections.defaultdict(list))
    lbs, greedy = {}, collections.defaultdict(dict)
    for ruta in CURVAS:
        for r in csv.DictReader(open(ruta, encoding="utf-8")):
            inst, ck = r["instance"], r["checkpoint"]
            lbs[inst] = float(r["lb"])
            par = (float(r["lo"]), float(r["up"]))
            if int(r["sample_idx"]) == 0:
                greedy[ck][inst] = par
            else:
                filas[ck][inst].append(par)
    out = {}
    for ck, porinst in filas.items():
        completo = {i: v for i, v in porinst.items() if len(v) >= N_POOL}
        if len(completo) != 70:
            print(f"  AVISO: {ck} con {len(completo)}/70 instancias, fuera")
            continue
        out[ck] = {}
        for i, v in completo.items():
            lo = np.array([x[0] for x in v[:N_POOL]])
            up = np.array([x[1] for x in v[:N_POOL]])
            g_lo, g_up = greedy[ck][i]
            out[ck][i] = {
                "lb": lbs[i],
                # clave lexicografica (U, L): los datos llevan un
                # decimal, asi que 1e6 preserva el orden sin colision
                "g_clave": g_up * 1e6 + g_lo,
                "g_mid": (g_lo + g_up) / 2,
                "clave": up * 1e6 + lo,
                "mid": (lo + up) / 2,
            }
    return out


def curva_de(tirada, rng):
    """RE media (punto medio) para cada presupuesto, con el
    decodificador desplegado: la pasada greedy mas B-1 muestras,
    retenidas por la clave lexicografica (U, L)."""
    re = np.zeros(len(PRESUPUESTOS))
    for datos in tirada.values():
        lb = datos["lb"]
        clave, mid = datos["clave"], datos["mid"]
        g_clave, g_mid = datos["g_clave"], datos["g_mid"]
        for j, b in enumerate(PRESUPUESTOS):
            if b == 1:
                re[j] += (g_mid - lb) / lb * 100
                continue
            tot = 0.0
            for _ in range(R):
                idx = rng.choice(N_POOL, b - 1, replace=False)
                k = clave[idx].argmin()
                if clave[idx][k] < g_clave:
                    m = mid[idx][k]
                else:
                    m = g_mid
                tot += (m - lb) / lb * 100
            re[j] += tot / R
    return re / len(tirada)


def referencias(instancias):
    """RE media de la regla DESTACADA y de EST sobre estas instancias.

    OJO con la fuente del GP: la unica valida es la regla PUBLICADA,
    reevo_fixedfit/summary.csv filtrando gp_tuned_seed1, cuya pasada
    determinista da 17.71 sobre las 70. La columna GP_re de
    constructive_per_instance.csv NO es esa regla y no debe usarse: si
    esta figura la leyera, su linea de referencia contradiria a la
    Tabla 7 sin que nadie lo note.
    """
    ta = {}
    for r in csv.DictReader(open(EST, encoding="utf-8")):
        ta[r["instance"]] = (r["ta"], float(r["est_re"]))
    gp = {}
    for r in csv.DictReader(open(GP_DESTACADA, encoding="utf-8")):
        if r["method"] == "gp_tuned_seed1":
            gp[r["instance"]] = float(r["re"])
    est_v = [ta[i][1] for i in instancias if i in ta]
    gp_v = [gp[i] for i in instancias if i in gp]
    return (float(np.mean(gp_v)) if gp_v else None,
            float(np.mean(est_v)) if est_v else None,
            len(gp_v), len(est_v))


def curva_gp(rng):
    """RE media de la regla para cada presupuesto, mismo decodificador
    y MISMO remuestreo que la curva de la politica.

    Tomar el prefijo del pool en vez de remuestrear daria un solo
    sorteo por presupuesto, con lo que la curva de la regla llevaria
    ruido que la de la politica no tiene y la comparacion entre ambas
    seria asimetrica en precision Monte Carlo. Se devuelve tambien la
    dispersion entre repeticiones, que es lo que acota hasta donde
    puede afinarse el cruce.
    """
    pools, lbs = collections.defaultdict(dict), {}
    for ruta in GP_POOL:
        for r in csv.DictReader(open(ruta, encoding="utf-8")):
            pools[r["instance"]][int(r["sample_idx"])] = (float(r["lo"]),
                                                          float(r["up"]))
            lbs[r["instance"]] = float(r["lb"])
    n_muestras = min(len(v) for v in pools.values()) - 1
    media, sd = [], []
    for b in PRESUPUESTOS:
        reps = []
        for _ in range(R if 1 < b < n_muestras else 1):
            acc = []
            for inst, v in pools.items():
                lb = lbs[inst]
                if b == 1:
                    m = v[0]
                elif b > n_muestras:
                    m = min([v[0]] + [v[i] for i in range(1, n_muestras + 1)],
                            key=lambda p: (p[1], p[0]))
                else:
                    ix = rng.choice(n_muestras, b - 1, replace=False)
                    m = min([v[0]] + [v[int(i) + 1] for i in ix],
                            key=lambda p: (p[1], p[0]))
                acc.append(((m[0] + m[1]) / 2 - lb) / lb * 100)
            reps.append(sum(acc) / len(acc))
        media.append(sum(reps) / len(reps))
        sd.append(float(np.std(reps)) if len(reps) > 1 else 0.0)
    return np.array(media), np.array(sd)


def cruce(xs, ys, umbral):
    """Primer presupuesto cuya RE media baja del umbral."""
    for x, y in zip(xs, ys):
        if y <= umbral:
            return x
    return None


def main():
    dep = lee_depositos()
    if len(dep) < 2:
        sys.exit("ABORTA: hacen falta varias tiradas completas")
    print(f"{len(dep)} tiradas completas de 70 instancias")

    rng = np.random.RandomState(20260818)
    curvas = np.array([curva_de(dep[ck], rng) for ck in sorted(dep)])
    media = curvas.mean(axis=0)
    mejor, peor = curvas.min(axis=0), curvas.max(axis=0)
    greedy = float(np.mean([
        np.mean([(d["g_mid"] - d["lb"]) / d["lb"] * 100
                 for d in dep[ck].values()]) for ck in dep]))
    instancias = sorted(next(iter(dep.values())))
    gp, est, n_gp, n_est = referencias(instancias)
    gp_curva, gp_sd = curva_gp(rng)
    print(f"referencias: GP {gp:.2f}% (n={n_gp}), EST {est:.2f}% "
          f"(n={n_est}), greedy medio de las tiradas {greedy:.2f}%")
    for b, m in zip(PRESUPUESTOS, media):
        print(f"  B={b:5d}  RE={m:6.2f}%")
    print(f"cruza EST    con B={cruce(PRESUPUESTOS, media, est)}")
    print(f"cruza GP     con B={cruce(PRESUPUESTOS, media, gp)}")
    print(f"cruza greedy con B={cruce(PRESUPUESTOS, media, greedy)}")
    print("")
    print("      B   politica     GP  sd_GP     dif")
    for b, m, g, s in zip(PRESUPUESTOS, media, gp_curva, gp_sd):
        print(f"  {b:5d} {m:8.2f} {g:7.2f} {s:6.3f} {m - g:+7.2f}")
    _alcanza = next((b for b, m, g in zip(PRESUPUESTOS, media, gp_curva)
                     if m <= g), None)
    print(f"  a presupuesto igualado, la politica alcanza a la regla "
          f"en B={_alcanza}")

    fig, ax = plt.subplots(figsize=(4.05, 3.1))
    ax.fill_between(PRESUPUESTOS, mejor, peor, color="#1f77b4", alpha=0.18,
                    linewidth=0)
    ax.plot(PRESUPUESTOS, media, color="#1f77b4", linewidth=1.6,
            label="policy, best of $B$ (mean of 10 runs)")
    # EST queda en el 42 por ciento: dibujarla aplastaria todo lo demas,
    # asi que el pie la nombra y el eje se reserva para la zona util.
    ax.plot(PRESUPUESTOS, gp_curva, color="#d62728", linewidth=1.6,
            linestyle="--", label="GP rule, best of $B$")
    ax.axhline(gp, color="#d62728", linestyle=":", linewidth=0.9,
               alpha=0.7, label=f"GP rule, one pass ({gp:.1f}%)")
    ax.axhline(greedy, color="#2ca02c", linestyle=":", linewidth=1.1,
               label=f"greedy pass ({greedy:.1f}%)")
    ax.set_xscale("log", base=2)
    ax.set_xlabel("inference budget $B$ (rollouts)")
    ax.set_ylabel("mean RE (%)")
    ax.set_xticks([1, 4, 16, 64, 256])
    ax.set_xticklabels(["1", "4", "16", "64", "256"])
    ax.legend(frameon=False, fontsize=7.5, loc="upper right")
    fig.tight_layout(pad=0.3)
    fig.savefig(SALIDA)
    print(f"escrito {SALIDA}")


if __name__ == "__main__":
    main()
