# -*- coding: utf-8 -*-
"""Genera las DMU 20x15 intervalares con el protocolo F.15_01 del paper.

Protocolo (verificado sobre tai20_15_01.F.15_01.txt, que lo
autodocumenta en sus comentarios finales):
  - intervalo simetrico alrededor del valor crisp: (p-h, p+h)
  - semiancho h = round(p * delta) con delta ~ U[0, 0.15], acotado
    para que h/p <= 0.15
  - 300/300 operaciones simetricas; delta max 0.1500; media 6.97%;
    ~19% de operaciones deterministas (h=0 por redondeo en p pequeños)

Entrada:  benchmarks/dmu_test/crudas/dmu*.txt   (formato estandar
          "n m" + lineas de pares maquina-duracion en orden de proceso)
Salida:   benchmarks/dmu_test/instancias_txt/dmuNN.F.15_01.txt
          (formato del solver FuzzyFW, cabeceras en español)
          benchmarks/dmu_test/instancias_py/int__dmuNN.F.15_01_interval.py
          (formato DeepLJSP)
          benchmarks/dmu_test/cotas.csv  (LB/UB de literatura, bks.json
          de ScheduleOpt, 2026-06)

Semillas fijas por instancia: reproducible. No toca nada existente.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, ".")

CRUDAS = "benchmarks/dmu_test/crudas"
OUT_TXT = "benchmarks/dmu_test/instancias_txt"
OUT_PY = "benchmarks/dmu_test/instancias_py"
INSTANCIAS = ["dmu01", "dmu02", "dmu03", "dmu04", "dmu05",
              "dmu41", "dmu42", "dmu43", "dmu44", "dmu45"]
DELTA_MAX = 0.15


def lee_dmu(ruta):
    with open(ruta) as f:
        toks = f.read().split()
    n, m = int(toks[0]), int(toks[1])
    vals = [int(t) for t in toks[2:]]
    assert len(vals) == n * m * 2, (len(vals), n, m)
    seqs, durs = [], []
    k = 0
    for _ in range(n):
        fila_m, fila_p = [], []
        for _ in range(m):
            fila_m.append(vals[k])
            fila_p.append(vals[k + 1])
            k += 2
        seqs.append(fila_m)
        durs.append(fila_p)
    return n, m, seqs, durs


def ensancha(durs, rng):
    out = []
    for fila in durs:
        fila_iv = []
        for p in fila:
            delta = float(rng.uniform(0.0, DELTA_MAX))
            h = min(int(round(p * delta)), int(np.floor(DELTA_MAX * p)))
            fila_iv.append((p - h, p + h))
        out.append(fila_iv)
    return out


def escribe_txt(ruta, n, m, seqs, ivs):
    hw = [(up - lo) / 2 for fila in ivs for lo, up in fila]
    mids = [(up + lo) / 2 for fila in ivs for lo, up in fila]
    deltas = [h / mid for h, mid in zip(hw, mids) if mid > 0]
    prom = 100 * sum(deltas) / len(deltas)
    dmax = 100 * max(deltas)
    with open(ruta, "w", newline="\n") as f:
        f.write("NUMERO DE TRABAJOS\n%d\n" % n)
        f.write("NUMERO DE RECURSOS\n%d\n" % m)
        f.write("SECUENCIA DE MAQUINAS\n")
        for fila in seqs:
            f.write(" ".join(str(x) for x in fila) + " \n")
        f.write("DURACIONES\n")
        for fila in ivs:
            f.write(" ".join("(%d, %d)" % iv for iv in fila) + " \n")
        f.write("TIEMPOS MAXIMOS DE FIN\n")
        f.write(" ".join(["(10000, 10000)"] * n) + " \n")
        f.write("// Desviacion Izda: min(0%%), max(%.0f%%), "
                "promedio(%.5f%%)\n" % (dmax, prom))
        f.write("// Desviacion Dcha: min(0%%), max(%.0f%%), "
                "promedio(%.5f%%)\n" % (dmax, prom))


def escribe_py(ruta, nombre, n, m, seqs, ivs):
    pid = "int__%s.F.15_01_interval" % nombre
    var = "INT__%s_F_15_01_INTERVAL_DATA" % nombre.upper()
    with open(ruta, "w", newline="\n") as f:
        f.write('"""\nProblema %s con incertidumbre en tiempos de '
                "procesamiento.\n\nGenerado con el protocolo F.15_01 del "
                "paper (delta ~ U[0, 0.15],\nintervalo simetrico, "
                "semilla fija) sobre la instancia crisp %s de\nDemirkol, "
                'Mehta y Uzsoy (1998).\n"""\n\n' % (pid.upper(), nombre))
        f.write("from jobshop_rl.models.interval import Interval\n\n\n")
        f.write("%s = {\n" % var)
        f.write("    'num_jobs': %d,\n" % n)
        f.write("    'num_machines': %d,\n" % m)
        f.write("    'problem_id': '%s',\n" % pid)
        f.write("    'sequences': [\n")
        for fila in seqs:
            f.write("        %r,\n" % (fila,))
        f.write("    ],\n")
        f.write("    'durations': [\n")
        for fila in ivs:
            f.write("        [" + ", ".join("Interval(%d, %d)" % iv
                                            for iv in fila) + "],\n")
        f.write("    ],\n")
        f.write("    'name': '%s',\n" % pid)
        f.write("    'has_intervals': True,\n")
        f.write("    'description': 'DMU %s ensanchada F.15_01',\n"
                % nombre)
        f.write("}\n")


def main():
    os.makedirs(OUT_TXT, exist_ok=True)
    os.makedirs(OUT_PY, exist_ok=True)
    cotas = {e["instance"]: (e["lower_bound"], e["upper_bound"],
                             e["status"])
             for e in json.load(open("benchmarks/dmu_test/bks.json"))
             if e.get("instance") in INSTANCIAS}
    with open("benchmarks/dmu_test/cotas.csv", "w", newline="\n") as f:
        f.write("instance,lb,ub,status\n")
        for nom in INSTANCIAS:
            lb, ub, st = cotas[nom]
            f.write("%s,%d,%d,%s\n" % (nom, lb, ub, st))
    for idx, nom in enumerate(INSTANCIAS):
        n, m, seqs, durs = lee_dmu(os.path.join(CRUDAS, nom + ".txt"))
        assert (n, m) == (20, 15), (nom, n, m)
        rng = np.random.default_rng(150100 + idx)   # F.15_01, por indice
        ivs = ensancha(durs, rng)
        escribe_txt(os.path.join(OUT_TXT, "%s.F.15_01.txt" % nom),
                    n, m, seqs, ivs)
        escribe_py(os.path.join(OUT_PY,
                                "int__%s.F.15_01_interval.py" % nom),
                   nom, n, m, seqs, ivs)
        hw = [(up - lo) for fila in ivs for lo, up in fila]
        print("%s: LB=%d UB=%d (%s) | ops sin ancho: %d/300" %
              (nom, *cotas[nom], sum(1 for h in hw if h == 0)))
    print("generadas %d instancias en %s y %s" %
          (len(INSTANCIAS), OUT_TXT, OUT_PY))


if __name__ == "__main__":
    main()
