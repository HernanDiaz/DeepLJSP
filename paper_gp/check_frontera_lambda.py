# -*- coding: utf-8 -*-
"""Traza el brazo ablacionado una frontera propia al crecer lambda?

Compara el barrido con anchuras (lambda_por_regla.csv, mas los dos brazos del
2x2) con el barrido sin anchuras recien evaluado. Si lambda mueve el ancho solo
cuando los terminales estan, entonces el fitness que penaliza la anchura actua
NECESARIAMENTE a traves de ellos, que es la hipotesis H2.
"""
import collections
import csv
import statistics as st
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def carga(path, key="lam"):
    d = collections.defaultdict(list)
    for r in csv.DictReader(open(path, encoding="utf-8")):
        d[r[key]].append((float(r["re"]), float(r["ancho"])))
    return d


con = carga("benchmarks/lambda_por_regla.csv")
sin = carga("benchmarks/lambda_nowidth_por_regla.csv")

# los dos puntos del 2x2, para situar lambda=1
abl = collections.defaultdict(list)
for r in csv.DictReader(open("benchmarks/ablation_por_regla.csv", encoding="utf-8")):
    abl[(r["objetivo"], r["terminales"])].append((float(r["re"]),
                                                  float(r["ancho"])))


def linea(etq, vs, n_completo=10):
    re_ = [x for x, _ in vs]
    an = [y for _, y in vs]
    aviso = "" if len(vs) >= n_completo else f"  (parcial {len(vs)}/{n_completo})"
    return (f"  {etq:<26} n={len(vs):<3} "
            f"RE {st.mean(re_):6.2f} +- {st.stdev(re_):4.2f}   "
            f"ancho {st.mean(an):6.2f} +- {st.stdev(an):4.2f}{aviso}")


print("CON los terminales de anchura")
print(linea("makespan (punto medio)", abl[("makespan", "full")], 30))
for lam in ("0.5", "2.0", "4.0"):
    if lam in con:
        print(linea(f"robusto lambda={lam}", con[lam]))
print(linea("robusto lambda=1", abl[("robust", "full")], 30))

print("\nSIN los terminales de anchura")
print(linea("makespan (punto medio)", abl[("makespan", "nowidth")], 30))
for lam in ("0.0", "0.5", "2.0"):
    if lam in sin:
        print(linea(f"robusto lambda={lam}", sin[lam]))
print(linea("robusto lambda=1", abl[("robust", "nowidth")], 30))

anchos_sin = [st.mean([y for _, y in sin[l]]) for l in ("0.0", "0.5", "2.0")
              if l in sin]
anchos_con = [st.mean([y for _, y in con[l]]) for l in ("0.5", "2.0", "4.0")
              if l in con]
print(f"\nrecorrido del ancho al crecer lambda")
print(f"  sin anchuras (lambda 0 -> 2):   {min(anchos_sin):.2f} a "
      f"{max(anchos_sin):.2f}   ({max(anchos_sin) - min(anchos_sin):.2f} puntos)")
print(f"  con anchuras (lambda 0.5 -> 4): {min(anchos_con):.2f} a "
      f"{max(anchos_con):.2f}   ({max(anchos_con) - min(anchos_con):.2f} puntos)")
