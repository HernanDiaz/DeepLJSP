# -*- coding: utf-8 -*-
"""El 0.41 s de 'GP rule (mean of 30)': es una propiedad de las reglas o de
la maquina mientras se median?

Las filas del CSV estan en orden alfabetico de nombre de regla, que es el orden
en que se midieron. Si el tiempo depende de la regla, no debe haber estructura
en ese orden. Si depende de la carga de la maquina, si.
"""
import csv
import statistics as st
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

rows = list(csv.DictReader(open("benchmarks/timing_gp_arm.csv", encoding="utf-8")))
v = [(r["rule"], float(r["mean_ms"])) for r in rows]

print("orden de medicion (alfabetico, como se ejecuto):")
for i, (name, ms) in enumerate(v, 1):
    marca = " <<<" if i == 10 else ""
    print(f"  {i:>2}. {name:<20} {ms:>7.1f} ms{marca}")

a = [ms for _, ms in v[:9]]
b = [ms for _, ms in v[9:]]
print(f"\nprimeras 9 medidas:  media {st.mean(a):.1f} ms, sd {st.pdev(a) if hasattr(st,'pdev') else st.pstdev(a):.1f}")
print(f"medidas 10 a 30:     media {st.mean(b):.1f} ms, sd {st.pstdev(b):.1f}")
print(f"salto entre bloques: {(st.mean(b)/st.mean(a)-1)*100:.1f}%")
print(f"\nmedia global (la que fue al paper): {st.mean([ms for _, ms in v]):.1f} ms")
print("\nel corte cae exactamente en la 10a medida, que es donde el orden")
print("alfabetico pasa de seed17 a seed18: es deriva de la maquina, no de")
print("las reglas, cuyos tamanos van de 20 a 30 nodos y no pueden producir")
print("un escalon limpio del 24% con dispersion interna de ~6 ms.")
