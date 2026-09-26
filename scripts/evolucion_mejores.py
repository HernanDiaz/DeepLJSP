# -*- coding: utf-8 -*-
"""La mejor regla de cada generacion de las 30 evoluciones del brazo
principal, reconstruida desde los logs y evaluada fuera del entrenamiento.

Los logs de la campana (logs/reevo/gp_tuned_seed*.log) guardan, por
generacion, el mejor RE de entrenamiento y la expresion de la mejor
regla, escrita por gp_rule.tree_str: una notacion con todos los
parentesis, que aqui se vuelve a convertir en arbol. Se comprueba que el
arbol de la ultima generacion es el guardado en el JSON de la regla y
que su RE de entrenamiento, recalculado, es el del log.

Despues cada arbol distinto se evalua con el simulador rapido en las 70
instancias Taillard, y se guarda el RE por particion: entrenamiento
(TA11-TA14), validacion (TA15-TA20) y prueba (las otras 60).

    python scripts/evolucion_mejores.py            # extrae y evalua
    python scripts/evolucion_mejores.py --sin-evaluar

Salida NUEVA: benchmarks/evolucion_mejores.json
"""
import argparse
import glob
import json
import os
import re
import sys

import numpy as np

sys.path.insert(0, ".")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SALIDA = "benchmarks/evolucion_mejores.json"
LINEA = re.compile(r"gen\s+(\d+)\s*\|\s*mejor=([\d.]+)%.*?mejor regla:\s*(.+?)\s*\|\s*\d+s")
BIN = {"+": "add", "-": "sub", "*": "mul", "/": "div"}


def analiza(s):
    """Arbol de gp_rule a partir de su tree_str."""
    pos = 0

    def expr():
        nonlocal pos
        if s[pos] == "(":
            pos += 1
            if s[pos] == "-":                      # (-X): negacion
                pos += 1
                a = expr()
                assert s[pos] == ")", s[pos:pos + 20]
                pos += 1
                return ("neg", a)
            a = expr()
            assert s[pos] == " " and s[pos + 2] == " ", s[pos:pos + 20]
            op = BIN[s[pos + 1]]
            pos += 3
            b = expr()
            assert s[pos] == ")", s[pos:pos + 20]
            pos += 1
            return (op, a, b)
        m = re.match(r"[A-Za-z]+", s[pos:])
        nombre = m.group(0)
        pos += len(nombre)
        if pos < len(s) and s[pos] == "(":         # min(a, b) / max(a, b)
            pos += 1
            a = expr()
            assert s[pos:pos + 2] == ", ", s[pos:pos + 20]
            pos += 2
            b = expr()
            assert s[pos] == ")", s[pos:pos + 20]
            pos += 1
            return (nombre, a, b)
        return nombre

    t = expr()
    assert pos == len(s), s[pos:]
    return t


def como_tupla(t):
    return t if isinstance(t, str) else tuple([t[0]] + [como_tupla(c) for c in t[1:]])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sin-evaluar", action="store_true")
    args = ap.parse_args()
    from jobshop_rl.heuristics.gp_rule import TERMINALS, tree_size, tree_str
    ANCHO = {"PTW", "ESTW", "WKRW"}

    res = {"semillas": {}}
    arboles = {}
    for f in sorted(glob.glob("logs/reevo/gp_tuned_seed*.log"),
                    key=lambda x: int(re.search(r"seed(\d+)", x).group(1))):
        s = int(re.search(r"seed(\d+)", f).group(1))
        filas = {}
        for m in LINEA.finditer(open(f, encoding="utf-8", errors="replace").read()):
            g, re_, ex = int(m.group(1)), float(m.group(2)), m.group(3)
            t = analiza(ex)
            assert tree_str(t) == ex, (s, g)
            arboles[ex] = t
            hojas = [n for n in _nodos(t) if n in TERMINALS]
            filas[g] = {"re_log": re_, "expr": ex, "size": tree_size(t),
                        "ancho": sum(h in ANCHO for h in hojas) / len(hojas)}
        # la generacion 0 solo imprime su RE, sin la regla
        assert sorted(filas) == list(range(1, 51)), (s, sorted(filas)[:3])
        guardado = json.load(open(f"benchmarks/reevo_fixedfit/gp_tuned_seed{s}.json",
                                  encoding="utf-8"))["tree"]
        assert como_tupla(guardado) == como_tupla(analiza(filas[50]["expr"])), s
        res["semillas"][s] = filas
    print(f"{len(res['semillas'])} evoluciones, {len(arboles)} reglas distintas")

    if not args.sin_evaluar:
        from e6_presupuesto import setenta
        from jobshop_rl.data import PROBLEM_REGISTRY
        from jobshop_rl.data.literature_bounds import lb_for_problem_name
        from jobshop_rl.heuristics.fast_sim import (Instancia, despacha,
                                                    prioridad_de)
        insts = setenta()
        datos = {p: Instancia(PROBLEM_REGISTRY[p]()) for p in insts}
        lbs = {p: lb_for_problem_name(p) for p in insts}
        ent = [f"int__tai20_15_{k:02d}" for k in (1, 2, 3, 4)]
        val = [f"int__tai20_15_{k:02d}" for k in range(5, 11)]
        pru = [p for p in insts if p not in ent and p not in val]
        assert len(pru) == 60
        ev = {}
        for k, (ex, t) in enumerate(sorted(arboles.items())):
            pol = prioridad_de(t)
            r = {p: ((cm[0] + cm[1]) / 2 - lbs[p]) / lbs[p] * 100
                 for p in insts for cm in [despacha(datos[p], pol)]}
            ev[ex] = {"ent": float(np.mean([r[p] for p in ent])),
                      "val": float(np.mean([r[p] for p in val])),
                      "pru": float(np.mean([r[p] for p in pru]))}
            if k % 50 == 0:
                print(f"  {k}/{len(arboles)}", flush=True)
        # el RE de entrenamiento recalculado es el del log
        peor = 0.0
        for filas in res["semillas"].values():
            for fila in filas.values():
                fila.update(ev[fila["expr"]])
                peor = max(peor, abs(fila["ent"] - fila["re_log"]))
        print(f"mayor diferencia con el RE del log: {peor:.3f}")
        assert peor < 0.01, peor
    json.dump(res, open(SALIDA, "w", encoding="utf-8"))
    print(f"escrito {SALIDA}")


def _nodos(t):
    if isinstance(t, str):
        yield t
        return
    yield t[0]
    for c in t[1:]:
        yield from _nodos(c)


if __name__ == "__main__":
    main()
