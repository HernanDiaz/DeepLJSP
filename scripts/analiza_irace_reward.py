# -*- coding: utf-8 -*-
"""Que dice la campana de pesos, mas alla de quien gano.

Lo interesante no es la ganadora sino la dispersion entre las elites
supervivientes: si cuatro vectores muy distintos empatan, los pesos no
son identificables a esta fidelidad, y eso es el resultado.
"""
import re
import statistics as st

LOG = r"E:\PycharmProjects\DeepLJSP\tuning\irace_reward.log"
NOM = ["makespan", "idle", "critical", "balance", "progress", "local"]
ACTUAL = [1.0, 0.24, 0.10, 0.10, 0.26, 0.15]

texto = open(LOG, encoding="utf-8", errors="replace").read()
bloque = texto.split("# Best configurations (")[1]
elites = {}
for linea in bloque.splitlines():
    m = re.match(r"\s*(\d+)\s+((?:[\d.]+\s*){6})$", linea)
    if m:
        elites[int(m.group(1))] = [float(x) for x in m.group(2).split()]

print(f"{len(elites)} elites finales\n")
print(f"{'peso':<10} " + "  ".join(f"#{i:<5}" for i in elites)
      + "   min   max  rango   actual")
for j, n in enumerate(NOM):
    v = [c[j] for c in elites.values()]
    print(f"{n:<10} " + "  ".join(f"{x:.3f} " for x in v)
          + f"  {min(v):.2f}  {max(v):.2f}   {max(v)-min(v):.2f}"
          f"     {ACTUAL[j]:.2f}")

print("\ncoeficiente de variacion entre elites (sd/media):")
for j, n in enumerate(NOM):
    v = [c[j] for c in elites.values()]
    print(f"   {n:<10} {st.stdev(v)/st.mean(v):5.2f}")

print("\nordenacion de los seis pesos en cada elite:")
for i, c in elites.items():
    orden = [NOM[j] for j in sorted(range(6), key=lambda k: -c[k])]
    print(f"   #{i:<3} {' > '.join(orden)}")
print(f"   actual {' > '.join(NOM[j] for j in sorted(range(6), key=lambda k: -ACTUAL[k]))}")

# concordancia entre semillas en la ultima iteracion
ult = texto.rsplit("Iteration 5 of 5", 1)[-1]
kw = re.findall(r"\|\s*[-=x.:!]\s*\|.*?\|([-+][\d.]+)\|([\d.]+)\|", ult)
if kw:
    print("\nconcordancia entre semillas en la ultima carrera (Kendall W):")
    print("   " + " ".join(w for _, w in kw))
