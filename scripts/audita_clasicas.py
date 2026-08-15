# -*- coding: utf-8 -*-
"""Audita la campana de las clasicas: cobertura, solapes y desperdicio.

Escrito despues de que una reanudacion mal hecha gastara nueve horas
recalculando semillas ya medidas (2026-08-14). Responde tres preguntas
que entonces nadie hizo a tiempo:

  cobertura  que pares (instancia, semilla) faltan todavia
  solape     que carriles estan calculando lo mismo a la vez
  reproceso  cuantas filas se han recalculado sin necesidad

Se puede ejecutar en cualquier momento; solo lee ficheros.

    python scripts/audita_clasicas.py
"""
import collections
import csv
import glob
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

INST = ["FT10", "FT20", "La21", "La24", "La25", "La27", "La29", "La38",
        "La40", "ABZ7", "ABZ8", "ABZ9"]
SEM = list(range(2, 32))


def main():
    # filas por fichero, para distinguir lo heredado de lo nuevo
    por_fichero, todas = {}, collections.defaultdict(list)
    for f in sorted(glob.glob("benchmarks/ext30/classic12_bo1024_*.csv")):
        if "maestro" in f:
            continue
        pares = []
        for r in csv.DictReader(open(f, encoding="utf-8")):
            k = (r["name"], int(r["seed"]))
            pares.append(k)
            todas[k].append(os.path.basename(f))
        por_fichero[os.path.basename(f)] = pares

    hechos = set(todas)
    faltan = [(i, s) for s in SEM for i in INST if (i, s) not in hechos]
    print(f"  cobertura: {len(hechos)}/360 pares; faltan {len(faltan)}")
    if faltan:
        por_sem = collections.Counter(s for _, s in faltan)
        print("    por semilla: " + ", ".join(
            f"{s}:{n}" for s, n in sorted(por_sem.items())))

    # reproceso: un par medido en mas de un fichero se calculo dos veces
    # (salvo los ficheros f*, sembrados a proposito con el maestro)
    repes = {k: v for k, v in todas.items()
             if len([x for x in v if not x.startswith("classic12_bo1024_f")])
             > 1}
    print(f"  reproceso historico: {len(repes)} pares medidos mas de una vez")

    # solape en curso: dos carriles f* con la misma semilla asignada
    asignadas = {}
    for bat in sorted(glob.glob("logs/lanza_clas30_f*.bat")):
        txt = open(bat, encoding="ascii", errors="replace").read()
        m = re.search(r"--semillas ([\d,]+)", txt)
        if m:
            asignadas[os.path.basename(bat)] = [int(x) for x in
                                                m.group(1).split(",")]
    vistas = collections.Counter(s for v in asignadas.values() for s in v)
    solapes = [s for s, n in vistas.items() if n > 1]
    print(f"  carriles activos: {len(asignadas)}; "
          f"semillas asignadas: {sorted(vistas)}")
    print(f"  solape entre carriles: "
          f"{'NINGUNO' if not solapes else solapes}")

    # Que lo asignado cubriera lo pendiente EN EL LANZAMIENTO, no ahora:
    # una semilla asignada que ya no falta puede haberla terminado este
    # mismo carril, que es lo normal segun avanza. La referencia correcta
    # es el maestro, que es la foto del momento en que se repartio.
    pend = sorted({s for _, s in faltan})
    maestro = "benchmarks/ext30/classic12_bo1024_maestro.csv"
    if os.path.exists(maestro):
        ini = collections.Counter(
            int(r["seed"]) for r in
            csv.DictReader(open(maestro, encoding="utf-8")))
        completas_ini = {s for s, n in ini.items() if n == 12}
    else:
        completas_ini = set()
    sobra = sorted(set(vistas) & completas_ini)
    corto = sorted(set(pend) - set(vistas))
    print(f"  semillas aun pendientes: {pend if pend else 'ninguna'}")
    if sobra:
        print(f"  AVISO: asignadas pese a estar completas al lanzar: {sobra}")
    if corto:
        print(f"  AVISO: nadie va a calcular: {corto}")
    if not sobra and not corto:
        print("  el reparto cubrio exactamente lo pendiente al lanzar")


if __name__ == "__main__":
    main()
