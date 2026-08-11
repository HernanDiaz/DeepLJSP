# -*- coding: utf-8 -*-
"""Taillard SINTETICAS 20x15 intervalares: la celda dentro-de-familia.

Diez instancias nuevas con el generador de Taillard (duraciones
enteras U[1,99], secuencia de maquinas = permutacion aleatoria por
trabajo) y el ensanchado F.15_01 del paper. Ningun modelo las ha
visto y ningun protocolo de seleccion las ha tocado: miden si la
ganancia v3 generaliza DENTRO de la familia Taillard, con
comparacion pareada (sin necesidad de cotas).

Salida (nada se sobreescribe):
  benchmarks/sint_test/instancias_txt/sint20_15_NN.F.15_01.txt
  jobshop_rl/data/int__sint20_15_NN.F.15_01_interval.py  (aditivo)
"""
import os
import sys

import numpy as np

sys.path.insert(0, ".")
from scripts.genera_dmu_intervalar import (ensancha, escribe_txt,   # noqa: E402
                                           escribe_py)

OUT_TXT = "benchmarks/sint_test/instancias_txt"
N_INST = 10
N, M = 20, 15


def main():
    os.makedirs(OUT_TXT, exist_ok=True)
    for k in range(1, N_INST + 1):
        rng = np.random.default_rng(770000 + k)
        seqs = [[int(x) for x in rng.permutation(M)] for _ in range(N)]
        durs = [[int(rng.integers(1, 100)) for _ in range(M)]
                for _ in range(N)]
        rng_w = np.random.default_rng(880000 + k)
        ivs = ensancha(durs, rng_w)
        nom = "sint20_15_%02d" % k
        escribe_txt(os.path.join(OUT_TXT, nom + ".F.15_01.txt"),
                    N, M, seqs, ivs)
        escribe_py(os.path.join("jobshop_rl/data",
                                "int__%s.F.15_01_interval.py" % nom),
                   nom, N, M, seqs, ivs)
        print(nom, "generada")
    print("listo:", N_INST, "instancias sinteticas")


if __name__ == "__main__":
    main()
