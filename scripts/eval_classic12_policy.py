# -*- coding: utf-8 -*-
"""Zero-shot de la politica DRL sobre las 12 instancias clasicas (F0.15).

La prueba de generalizacion cross-family del paper del GP, replicada para
la politica: FT10/FT20, siete La y ABZ7-9 en version intervalo, que no
comparten familia con las Taillard de entrenamiento. Best-of-64 con cada
checkpoint final; RE contra los LB best-known del E[Cmax] (Diaz et al.
2022, tabla 2 del fEABC) -- la MISMA referencia que usa el paper del GP
para esta tabla, distinta de las cotas crisp de Taillard.

Salida NUEVA: benchmarks/eval_classic12_policy.csv (reanudable).

    python scripts/eval_classic12_policy.py
"""
import csv
import os
import re
import sys

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from jobshop_rl.agents_v2 import AgentV2                       # noqa: E402
from jobshop_rl.experiments.factory import EnvironmentFactory  # noqa: E402
from jobshop_rl.models.interval import Interval                # noqa: E402

FILES = {
    "FT10": "F0.15.0.ft10_10.txt", "FT20": "F0.15.0.ft20_05.txt",
    "La21": "F0.15.0.la21_04.txt", "La24": "F0.15.0.la24_03.txt",
    "La25": "F0.15.0.la25_04.txt", "La27": "F0.15.0.la27_09.txt",
    "La29": "F0.15.0.la29_03.txt", "La38": "F0.15.0.la38_06.txt",
    "La40": "F0.15.0.la40_05.txt", "ABZ7": "F0.15.0.abz7_06.txt",
    "ABZ8": "F0.15.0.abz8_05.txt", "ABZ9": "F0.15.0.abz9_10.txt",
}
LB = {"ABZ7": 656, "ABZ8": 645, "ABZ9": 661, "FT10": 930, "FT20": 1165,
      "La21": 1046, "La24": 935, "La25": 977, "La27": 1235, "La29": 1152,
      "La38": 1196, "La40": 1222}
DIRS = [os.path.join("zenodo_deposit", "instances", "classical"),
        r"E:\Experimentos\Selectos"]
CKPTS = [f"models/v2_final_deepsets_1000ep_seed{s}.pt" for s in (2, 3, 4)]
N_BO = 64
SALIDA = "benchmarks/eval_classic12_policy.csv"


def localiza(fichero):
    for d in DIRS:
        p = os.path.join(d, fichero)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(fichero)


def load_instance(path, name):
    """El mismo parser doble-formato de scripts/eval_classic12.py."""
    lines = [ln.strip() for ln in open(path, encoding="utf-8",
                                       errors="replace") if ln.strip()]
    if "NUMERO DE TRABAJOS" in lines:            # formato FT (cabeceras)
        i = lines.index("NUMERO DE TRABAJOS"); n = int(lines[i + 1])
        i = lines.index("NUMERO DE RECURSOS"); m = int(lines[i + 1])
        i = lines.index("SECUENCIA DE MAQUINAS")
        seq_lines = lines[i + 1:i + 1 + n]
        i = lines.index("DURACIONES")
        dur_lines = lines[i + 1:i + 1 + n]
    else:                                         # formato LA/ABZ
        n = int(lines[0]); m = int(lines[1])
        seq_lines = lines[2:2 + n]
        dur_lines = lines[2 + n:2 + 2 * n]
    seqs = [[int(x) for x in ln.split()] for ln in seq_lines]
    durs = [[Interval(int(lo), int(up))
             for lo, up in re.findall(r"\((\d+),\s*(\d+)\)", ln)]
            for ln in dur_lines]
    assert all(len(s) == m for s in seqs) and all(len(d) == m for d in durs)
    return {"num_jobs": n, "num_machines": m, "problem_id": name,
            "sequences": seqs, "durations": durs}


def mid_componentwise(schedule):
    lo_max = up_max = 0.0
    for t in schedule:
        e = t.get("end")
        if hasattr(e, "lower"):
            lo, up = float(e.lower), float(e.upper)
        elif isinstance(e, dict):
            lo, up = float(e["lower"]), float(e["upper"])
        else:
            lo = up = float(e)
        lo_max, up_max = max(lo_max, lo), max(up_max, up)
    return (lo_max + up_max) / 2.0


def main():
    hechas = set()
    if os.path.exists(SALIDA):
        with open(SALIDA, encoding="utf-8") as f:
            hechas = {(r["name"], r["checkpoint"])
                      for r in csv.DictReader(f)}
    nuevo = not os.path.exists(SALIDA)
    out = open(SALIDA, "a", encoding="utf-8", newline="")
    w = csv.writer(out)
    if nuevo:
        w.writerow(["name", "checkpoint", "lb", "mid", "re"])

    for name, fichero in FILES.items():
        problema = load_instance(localiza(fichero), name)
        for ck in CKPTS:
            clave = (name, os.path.basename(ck))
            if clave in hechas:
                continue
            env = EnvironmentFactory.create_from_problem(
                problema, "adaptive", seed=1, problem_id=name)
            agent = AgentV2(env, seed=1, attention_layers=0)
            agent.load_checkpoint(ck)
            _, schedule, _, _ = agent.evaluate_policy(n_samples=N_BO)
            mid = mid_componentwise(schedule)
            re_pct = (mid - LB[name]) / LB[name] * 100
            w.writerow([name, clave[1], LB[name], f"{mid:.1f}",
                        f"{re_pct:.4f}"])
            out.flush()
            print(f"{name} {clave[1]}: RE={re_pct:.2f}%", flush=True)
    out.close()


if __name__ == "__main__":
    main()
