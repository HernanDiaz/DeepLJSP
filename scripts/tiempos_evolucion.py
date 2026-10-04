# -*- coding: utf-8 -*-
"""Tiempo de cada una de las 30 evoluciones del brazo principal (6.1).

Lo lee de los logs de logs/reevo/gp_tuned_seed*.log, que anotan al final
de cada generacion el tiempo transcurrido desde el arranque; el de la
generacion 50 es lo que tarda la evolucion entera.

    python scripts/tiempos_evolucion.py

Salida NUEVA: benchmarks/tiempos_evolucion.json
"""
import glob
import json
import re
import statistics

SALIDA = "benchmarks/tiempos_evolucion.json"


def main():
    seg = {}
    for f in sorted(glob.glob("logs/reevo/gp_tuned_seed*.log")):
        s = open(f, encoding="utf-8", errors="replace").read()
        g = re.findall(r"^gen\s+50 \|.*\| (\d+)s\s*$", s, re.M)
        assert g, f"{f}: sin generacion 50"
        seg[re.search(r"seed(\d+)", f).group(1)] = int(g[-1])
    assert len(seg) == 30, len(seg)
    v = list(seg.values())
    out = {"generaciones": 50, "segundos_por_semilla": seg,
           "mediana_min": statistics.median(v) / 60,
           "min_min": min(v) / 60, "max_min": max(v) / 60}
    json.dump(out, open(SALIDA, "w", encoding="utf-8"), indent=1)
    print(f"mediana {out['mediana_min']:.1f} min, de {out['min_min']:.1f} "
          f"a {out['max_min']:.1f}; escrito {SALIDA}")


if __name__ == "__main__":
    main()
