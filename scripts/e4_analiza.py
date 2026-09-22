# -*- coding: utf-8 -*-
"""E4: si el valor de las anchuras depende del esquema simetrico.

La revision r3.4 objeta que todas las instancias del articulo llevan
intervalos simetricos, de modo que la contribucion de los terminales de
anchura podria ser un artefacto del generador. La campana de
e4_campana.py repite los cuatro brazos del articulo --- makespan y
robusto lambda=1, cada uno con el conjunto completo de terminales y con
la ablacion sin anchuras --- sobre el banco asimetrico.

Se mide lo mismo que el articulo mide en el banco simetrico:

  - RE sobre las setenta asimetricas, que NO es comparable en nivel con
    el del banco simetrico, porque el sesgo a la derecha sube el
    makespan esperado y la cota inferior crisp no se mueve; lo
    comparable es el contraste entre brazos DENTRO del banco;
  - la anchura relativa del intervalo de makespan predicho;
  - la desviacion de la ejecucion, absoluta y normalizada, por Monte
    Carlo sobre el orden ya fijado.

    python scripts/e4_analiza.py

Salida NUEVA: benchmarks/e4_asimetrico/resumen.json
"""
import glob
import json
import os
import re
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, ".")
os.environ.setdefault("OMP_NUM_THREADS", "1")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data import PROBLEM_REGISTRY                   # noqa: E402
from jobshop_rl.data.literature_bounds import (                # noqa: E402
    lb_for_problem_name)
from jobshop_rl.heuristics.fast_sim import (                   # noqa: E402
    Instancia, despacha, prioridad_de)

DIR = "benchmarks/e4_asimetrico"
SALIDA = os.path.join(DIR, "resumen.json")
RAMAS = ["full", "nowidth", "rob1", "rob1_nowidth"]
ETIQUETA = {"full": "makespan, full", "nowidth": "makespan, sin anchura",
            "rob1": "robusto l=1, full",
            "rob1_nowidth": "robusto l=1, sin anchura"}
CLASES = {(15, 15), (20, 15), (20, 20), (30, 15), (30, 20),
          (50, 15), (50, 20)}
K = 400                       # realizaciones por instancia


def asimetricas():
    out = []
    for p in PROBLEM_REGISTRY:
        m = re.fullmatch(r"int__atai(\d+)_(\d+)_(\d+)", p)
        if m and (int(m.group(1)), int(m.group(2))) in CLASES:
            out.append(p)
    return sorted(out)


def ejecuta(inst, perm, dur):
    """Decodifica `perm` con duraciones crisp `dur[j][k]`: el makespan
    que sale al ejecutar el mismo orden bajo una realizacion."""
    n, m, seq = inst.n, inst.m, inst.seq
    jc, mc, op = [0.0] * n, [0.0] * m, [0] * n
    for j in perm:
        k = op[j]
        q = seq[j][k]
        s = jc[j] if jc[j] > mc[q] else mc[q]
        jc[j] = mc[q] = s + dur[j][k]
        op[j] = k + 1
    return max(jc)


def mide(arbol, insts, rng):
    """RE, anchura relativa y desviacion de la ejecucion, por instancia."""
    pol = prioridad_de(arbol)
    re_, anc, absd, eps = [], [], [], []
    for pid, inst, lb in insts:
        (lo, up), perm = despacha(inst, pol, orden=True)
        mid = (lo + up) / 2
        re_.append((mid - lb) / lb * 100)
        anc.append((up - lo) / mid * 100)
        # el orden esta fijado; solo cambian las duraciones realizadas
        d = [[rng.uniform(inst.lo[j][k], inst.up[j][k], K)
              for k in range(inst.m)] for j in range(inst.n)]
        ex = np.array([ejecuta(inst, perm,
                               [[d[j][k][t] for k in range(inst.m)]
                                for j in range(inst.n)])
                       for t in range(K)])
        absd.append(float(np.mean(np.abs(ex - mid))))
        eps.append(float(np.mean(np.abs(ex - mid)) / mid * 1000))
    return (np.array(re_), np.array(anc), np.array(absd), np.array(eps))


def main():
    ids = asimetricas()
    assert len(ids) == 70, len(ids)
    insts = [(p, Instancia(PROBLEM_REGISTRY[p]()), lb_for_problem_name(p))
             for p in ids]
    print(f"{len(insts)} instancias asimetricas, {K} realizaciones\n")

    res = {"n_instancias": len(insts), "K": K, "ramas": {}}
    por_rama = {}
    for rama in RAMAS:
        fich = sorted(glob.glob(os.path.join(DIR, rama, "seed*.json")))
        if not fich:
            continue
        filas = {}
        for f in fich:
            s = int(re.search(r"seed(\d+)", os.path.basename(f)).group(1))
            arbol = json.load(open(f, encoding="utf-8"))["tree"]
            rng = np.random.default_rng(4000 + s)
            r, a, ab, e = mide(arbol, insts, rng)
            filas[s] = {"re": float(r.mean()), "anchura": float(a.mean()),
                        "abs": float(ab.mean()), "eps": float(e.mean())}
            print(f"  {rama} seed{s}: RE {r.mean():.2f} anchura "
                  f"{a.mean():.2f} |D| {ab.mean():.2f}", flush=True)
        por_rama[rama] = filas
        v = {k: np.array([filas[s][k] for s in sorted(filas)])
             for k in ("re", "anchura", "abs", "eps")}
        res["ramas"][rama] = {
            "n": len(filas),
            **{k: {"media": float(v[k].mean()),
                   "sd": float(v[k].std(ddof=1))} for k in v},
            "por_semilla": filas}

    print(f"\n  {'rama':<26} {'n':>3} {'RE':>14} {'anchura':>14} "
          f"{'|Delta|':>14}")
    for rama in RAMAS:
        if rama not in res["ramas"]:
            continue
        r = res["ramas"][rama]
        print(f"  {ETIQUETA[rama]:<26} {r['n']:>3} "
              + " ".join(f"{r[k]['media']:8.2f}+-{r[k]['sd']:4.2f}"
                         for k in ("re", "anchura", "abs")))

    # los dos contrastes que sostienen la contribucion, pareados por
    # semilla: la anchura dentro de cada objetivo
    res["contrastes"] = {}
    for a, b, etq in (("full", "nowidth", "makespan: anchura o no"),
                      ("rob1", "rob1_nowidth", "robusto: anchura o no"),
                      ("rob1", "full", "robusto contra makespan")):
        if a not in por_rama or b not in por_rama:
            continue
        com = sorted(set(por_rama[a]) & set(por_rama[b]))
        d = {}
        for k in ("re", "anchura", "abs"):
            x = np.array([por_rama[a][s][k] for s in com])
            y = np.array([por_rama[b][s][k] for s in com])
            w = stats.wilcoxon(x, y, method="exact", zero_method="wilcox")
            n = int(np.sum(np.abs(x - y) > 1e-12))
            mu = n * (n + 1) / 4.0
            sd = (n * (n + 1) * (2 * n + 1) / 24.0) ** 0.5
            z = (float(w.statistic) - mu) / sd if sd > 0 else 0.0
            z = abs(z) if (x - y).mean() > 0 else -abs(z)
            d[k] = {"d": float((x - y).mean()), "p": float(w.pvalue),
                    "z": float(z), "r": float(abs(z) / n ** 0.5)}
        res["contrastes"][f"{a} vs {b}"] = d
        print(f"\n  {etq} (n={len(com)})")
        for k in ("re", "anchura", "abs"):
            print(f"    {k:<8} d={d[k]['d']:+7.2f}  z={d[k]['z']:+6.2f}  "
                  f"p={d[k]['p']:.4f}  |r|={d[k]['r']:.2f}")

    # Holm sobre la familia entera: tres contrastes por tres medidas. Sin
    # ella, dos diferencias de RE al filo de 0.03 pareceria que dicen algo
    todos = [(v[k]["p"], f"{par}/{k}")
             for par, v in res["contrastes"].items() for k in v]
    todos.sort()
    prev, ajust = 0.0, {}
    for i, (pv, etq) in enumerate(todos):
        prev = max(prev, min(1.0, pv * (len(todos) - i)))
        ajust[etq] = prev
    for par, v in res["contrastes"].items():
        for k in v:
            v[k]["p_holm"] = ajust[f"{par}/{k}"]
    print(f"\n  Holm sobre los {len(todos)} contrastes")
    for pv, etq in todos:
        marca = "  <-- sobrevive" if ajust[etq] < 0.05 else ""
        print(f"    {etq:<34} p={pv:.4f}  Holm={ajust[etq]:.4f}{marca}")

    json.dump(res, open(SALIDA, "w", encoding="utf-8"), indent=1)
    print(f"\nescrito {SALIDA}")


if __name__ == "__main__":
    main()
