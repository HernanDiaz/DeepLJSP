# -*- coding: utf-8 -*-
"""E4: las setenta Taillard con intervalos ASIMETRICOS.

La revision r3.4 objeta que todas las instancias del articulo llevan
intervalos simetricos, de modo que el valor de los terminales de anchura
podria depender del esquema de generacion y no del problema.

Aqui se genera una variante asimetrica de las mismas setenta. El valor
crisp se recupera del punto medio, que el protocolo simetrico conserva
exacto, y sobre el se sortea

    p_lo = p - round(p * U[0, 0.05]),
    p_up = p + round(p * U[0, 0.25]),

sesgado a la derecha: adelantarse poco, retrasarse mucho, que es la
asimetria que tiene sentido en taller. La anchura ESPERADA total es
0.15 p, practicamente la del esquema simetrico (0.14 p), asi que lo que
cambia entre los dos bancos es la forma del intervalo y no su tamano, y
cualquier diferencia se puede atribuir a la asimetria.

Las rutas de maquina no se tocan, de modo que las cotas inferiores
crisp de Taillard siguen siendo validas y el RE es comparable.

    python scripts/e4_genera_asimetricas.py

Salida NUEVA: jobshop_rl/data/int__ataiNN_MM_KK.A.05_25_interval.py
              benchmarks/e4_asimetrico/resumen_generacion.json
"""
import json
import os
import re
import sys

import numpy as np

sys.path.insert(0, ".")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.data import PROBLEM_REGISTRY          # noqa: E402
from jobshop_rl.models.interval import Interval       # noqa: E402

DATA = "jobshop_rl/data"
DIR = "benchmarks/e4_asimetrico"
TAG = "A.05_25"
DELTA_LO, DELTA_UP = 0.05, 0.25

CABECERA = '''"""{nombre} con intervalos asimetricos (protocolo {tag}).

Generado por scripts/e4_genera_asimetricas.py a partir de la version
simetrica: el valor crisp es el punto medio de aquella, y sobre el se
sortea p_lo = p - round(p*U[0,{dlo}]) y p_up = p + round(p*U[0,{dup}]).
Las rutas de maquina son las mismas.
"""

from jobshop_rl.models.interval import Interval


{var} = {{
    'num_jobs': {n},
    'num_machines': {m},
    'problem_id': '{pid}',
    'name': '{nombre}',
    'has_intervals': True,
    'description': '{nombre} asimetrica {tag}',
    'sequences': {seqs},
    'durations': [
'''


# las siete clases del banco del articulo: la 100x20 existe en el repo
# pero no forma parte de las setenta
CLASES = {(15, 15), (20, 15), (20, 20), (30, 15), (30, 20),
          (50, 15), (50, 20)}


def simetricas():
    """Los ids de las setenta simetricas, en orden."""
    out = []
    for p in PROBLEM_REGISTRY:
        m = re.fullmatch(r"int__tai(\d+)_(\d+)_(\d+)", p)
        if m and (int(m.group(1)), int(m.group(2))) in CLASES:
            out.append(p)
    return sorted(out)


def crisp(dur):
    """El valor crisp de una duracion simetrica: su punto medio exacto."""
    if isinstance(dur, Interval):
        p = (dur.lower + dur.upper) / 2
        assert abs(p - round(p)) < 1e-9, f"punto medio no entero: {dur}"
        return int(round(p))
    return int(dur)


def asimetriza(p, rng):
    lo = p - int(round(p * rng.uniform(0, DELTA_LO)))
    up = p + int(round(p * rng.uniform(0, DELTA_UP)))
    return max(1, lo), max(1, up)


def escribe(pid_sim, datos, rng, stats):
    m = re.fullmatch(r"int__tai(\d+)_(\d+)_(\d+)", pid_sim)
    nj, nm, idx = m.groups()
    pid = f"int__atai{nj}_{nm}_{idx}"
    nombre = f"aTA {nj}x{nm} #{idx}"
    fichero = os.path.join(DATA, f"{pid}.{TAG}_interval.py")
    var = f"{pid.upper()}_{TAG.replace('.', '_')}_INTERVAL_DATA"

    filas = []
    for fila in datos["durations"]:
        nueva = []
        for d in fila:
            p = crisp(d)
            lo, up = asimetriza(p, rng)
            nueva.append((lo, up))
            stats["p"].append(p)
            stats["w"].append(up - lo)
            stats["sesgo"].append((up - p) - (p - lo))
        filas.append(nueva)

    with open(fichero, "w", encoding="utf-8") as f:
        f.write(CABECERA.format(
            nombre=nombre, tag=TAG, dlo=DELTA_LO, dup=DELTA_UP, var=var,
            n=datos["num_jobs"], m=datos["num_machines"], pid=pid,
            seqs=repr([[int(x) for x in s] for s in datos["sequences"]])))
        for fila in filas:
            f.write("        [" + ", ".join(
                f"Interval({lo}, {up})" for lo, up in fila) + "],\n")
        f.write("    ],\n}\n")
    return pid


def main():
    ids = simetricas()
    assert len(ids) == 70, f"{len(ids)} simetricas, esperaba 70"
    os.makedirs(DIR, exist_ok=True)
    stats = {"p": [], "w": [], "sesgo": []}
    hechos = []
    for k, pid_sim in enumerate(ids):
        # semilla fija por instancia: reproducible y sin solape entre ellas
        rng = np.random.default_rng(40500 + k)
        hechos.append(escribe(pid_sim, PROBLEM_REGISTRY[pid_sim](), rng,
                              stats))
        print(f"  {pid_sim} -> {hechos[-1]}")

    p = np.array(stats["p"], dtype=float)
    w = np.array(stats["w"], dtype=float)
    s = np.array(stats["sesgo"], dtype=float)
    res = {"n_instancias": len(hechos), "n_operaciones": len(p),
           "delta_lo": DELTA_LO, "delta_up": DELTA_UP,
           "anchura_media_rel": float((w / p).mean()),
           "sesgo_medio_rel": float((s / p).mean()),
           "deterministas": int((w == 0).sum()),
           "ids": hechos}
    json.dump(res, open(os.path.join(DIR, "resumen_generacion.json"), "w",
                        encoding="utf-8"), indent=1)
    print(f"\n{len(hechos)} instancias, {len(p)} operaciones")
    print(f"  anchura media  {100 * res['anchura_media_rel']:.2f}% de p")
    print(f"  sesgo medio    {100 * res['sesgo_medio_rel']:+.2f}% de p")
    print(f"  deterministas  {res['deterministas']}")
    print(f"\nescrito {DIR}/resumen_generacion.json")


if __name__ == "__main__":
    main()
