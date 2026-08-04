# -*- coding: utf-8 -*-
"""Best-of-64 de las 70 instancias, reconstruido del deposito de rollouts.

tab:crosssize mostraba nueve instancias escogidas (las _01 de cada
clase mas TA2 y TA5) sin decir por que esas nueve. No hace falta
evaluar nada nuevo: eval_budget_curve.py guardo 342 rollouts por
checkpoint de las 70, y el protocolo de esa tabla -- por checkpoint, un
greedy mas 63 muestreados, el mejor por cota superior, luego media
[mejor] sobre las tres semillas -- se reconstruye tomando los 64
primeros de cada deposito.

Validado contra eval_crosssize_bo64.csv sobre las ocho instancias
comunes que la curva tenia completas: seis identicas, desvio maximo
0.25 puntos (mismo flujo de numeros aleatorios, la semilla del agente
es fija).

    python scripts/bo64_desde_curva.py -> benchmarks/bo64_70.csv
"""
import collections
import csv
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CURVA = "benchmarks/eval_budget_curve.csv"
SALIDA = "benchmarks/bo64_70.csv"
CLASE = {(15, 15): 0, (20, 15): 1, (20, 20): 2, (30, 15): 3,
         (30, 20): 4, (50, 15): 5, (50, 20): 6}
N = 64


def ta_de(n):
    m = re.search(r"tai(\d+)_(\d+)_(\d+)", n.lower())
    a, b, k = int(m.group(1)), int(m.group(2)), int(m.group(3))
    return f"TA{CLASE[(a, b)] * 10 + k}", f"{a}x{b}"


def main():
    pool = collections.defaultdict(list)
    lbs = {}
    for r in csv.DictReader(open(CURVA, encoding="utf-8")):
        pool[(r["instance"], r["checkpoint"])].append(
            (int(r["sample_idx"]), float(r["mid_comp"])))
        lbs[r["instance"]] = float(r["lb"])

    por_inst = collections.defaultdict(dict)
    for (inst, ck), v in pool.items():
        primeros = [m for _, m in sorted(v)[:N]]
        por_inst[inst][ck] = (min(primeros) - lbs[inst]) / lbs[inst] * 100

    completas = {i: d for i, d in por_inst.items() if len(d) == 3}
    assert len(completas) == 70, f"esperaba 70, hay {len(completas)}"

    with open(SALIDA, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ta", "instance", "cls", "lb", "re_mean", "re_best"])
        for inst in sorted(completas):
            ta, cls = ta_de(inst)
            v = list(completas[inst].values())
            w.writerow([ta, inst, cls, f"{lbs[inst]:.0f}",
                        f"{sum(v) / 3:.4f}", f"{min(v):.4f}"])
    print(f"escrito {SALIDA}: 70 instancias")

    # el resumen por clase, que es lo que va a la tabla
    por_clase = collections.defaultdict(list)
    for inst, d in completas.items():
        _, cls = ta_de(inst)
        por_clase[cls].append((sum(d.values()) / 3, min(d.values())))
    print(f"\n{'clase':8s} {'media':>7s} {'mejor':>7s}")
    for cls in ("15x15", "20x15", "20x20", "30x15", "30x20", "50x15",
                "50x20"):
        v = por_clase[cls]
        print(f"{cls:8s} {sum(a for a, _ in v) / 10:7.1f} "
              f"{sum(b for _, b in v) / 10:7.1f}")
    todo = [x for v in por_clase.values() for x in v]
    print(f"{'todas':8s} {sum(a for a, _ in todo) / 70:7.1f} "
          f"{sum(b for _, b in todo) / 70:7.1f}")


if __name__ == "__main__":
    main()
