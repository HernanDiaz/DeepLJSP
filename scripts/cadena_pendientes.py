"""Encadena los tres experimentos pendientes del paper GP, en secuencia.

Secuencial y no en paralelo a proposito: comparten maquina y el paso 2 vuelve
a evolucionar, de modo que solaparlos alargaria los tres sin ganar nada. Cada
paso salta si su salida ya existe, asi que la cadena se puede reanudar.

  1. eps-robustez de 7.3 con seis metodos, incluida la comparacion CON vs SIN
     anchura bajo el objetivo ROBUSTO, que es la que prueba la contribucion, y
     con cobertura como tercera medida.
  2. barrido de lambda para el brazo SIN anchura, con lambda=0 (peor caso puro)
     como control que aisla el termino de anchura.
  3. reevaluacion de los cuatro brazos guardando el ancho POR REGLA, necesario
     para el test formal de la interaccion del diseno 2x2 de 7.2.

Uso: python scripts/cadena_pendientes.py [--dry]
"""

import argparse
import glob
import json
import os
import re
import subprocess
import sys
import time

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PY = sys.executable
LOG = "logs/cadena"
TUNED = ["--tournament", "7", "--crossover", "0.7695",
         "--maxtree", "30", "--elitism", "2"]


def log(msg):
    print(f"[{time.strftime('%H:%M')}] {msg}", flush=True)


def mejor_por_ancho(patron):
    """Mejor regla de un brazo robusto segun el ancho del intervalo, que es lo
    que su fitness optimiza; elegirla por RE seria juzgarla por otro criterio."""
    from jobshop_rl.data import PROBLEM_REGISTRY
    from jobshop_rl.data.literature_bounds import lb_for_problem_name
    from jobshop_rl.experiments.factory import EnvironmentFactory
    from jobshop_rl.heuristics.gp_rule import GPRuleHeuristic
    from jobshop_rl.models.interval import Interval

    insts = [p for p in sorted(PROBLEM_REGISTRY)
             if re.match(r"int__tai\d+_\d+_\d+$", p)
             and lb_for_problem_name(p) is not None]
    best = (1e9, None)
    for f in sorted(glob.glob(patron)):
        h = GPRuleHeuristic(json.load(open(f, encoding="utf-8"))["tree"])
        wid = []
        for pid in insts:
            env = EnvironmentFactory.create_from_problem(
                PROBLEM_REGISTRY[pid](), "basic", seed=0)
            st = env.reset(); done = False
            while not done and st["eligible_ops"]:
                fe = env.get_features(st)
                a = min(h.select_action(st["eligible_ops"], fe),
                        len(st["eligible_ops"]) - 1)
                st, _, done, _ = env.step(a)
            c = env.job_completion_time
            lo = max(x.lower if isinstance(x, Interval) else x for x in c)
            up = max(x.upper if isinstance(x, Interval) else x for x in c)
            wid.append((up - lo) / ((up + lo) / 2) * 100)
        w = sum(wid) / len(wid)
        if w < best[0]:
            best = (w, f)
    return best


def paso1():
    out = "benchmarks/robustness_seis.csv"
    if os.path.exists(out):
        log("paso 1: ya existe, salto"); return
    log("paso 1: eligiendo las mejores reglas de los brazos robustos")
    w1, r1 = mejor_por_ancho("benchmarks/tuned/robust/width_seed*.json")
    w2, r2 = mejor_por_ancho("benchmarks/tuned/robust/nowidth_seed*.json")
    w4, r4 = mejor_por_ancho("benchmarks/tuned/lambda/lam4p0_seed*.json")
    log(f"  robusto lam=1 con anchura : {os.path.basename(r1)} ({w1:.2f}%)")
    log(f"  robusto lam=1 sin anchura : {os.path.basename(r2)} ({w2:.2f}%)")
    log(f"  robusto lam=4 con anchura : {os.path.basename(r4)} ({w4:.2f}%)")
    cmd = [PY, "scripts/robustness_epsilon.py",
           "--rule", "benchmarks/reevo_fixedfit/gp_tuned_seed1.json",
           "--nowidth", "benchmarks/tuned/ablation/nowidth_seed25.json",
           "--extra", f"GP-rob1={r1}",
           "--extra", f"GP-rob1-nw={r2}",
           "--extra", f"GP-rob4={r4}",
           "--out", out]
    with open(f"{LOG}/paso1.log", "w", encoding="utf-8") as f:
        subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
    log(f"paso 1: {'OK' if os.path.exists(out) else 'FALLO'}")


def paso2():
    outdir = "benchmarks/lambda_nowidth"
    os.makedirs(outdir, exist_ok=True)
    jobs = [(l, s) for l in ("0.0", "0.5", "2.0", "4.0")
            for s in range(1, 11)]
    faltan = [(l, s) for l, s in jobs
              if not os.path.exists(f"{outdir}/nw_lam{l.replace('.','p')}_seed{s}.json")]
    if not faltan:
        log("paso 2: completo, salto"); return
    log(f"paso 2: barrido lambda sin anchura, {len(faltan)} evoluciones")
    for l, s in faltan:
        o = f"{outdir}/nw_lam{l.replace('.','p')}_seed{s}.json"
        cmd = [PY, "scripts/evolve_gp_rule.py", "--out", o, "--seed", str(s),
               "--fitness", "robust", "--lam", l, "--no-width"] + TUNED
        with open(f"{LOG}/nw_lam{l}_s{s}.log", "w", encoding="utf-8") as f:
            subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
        log(f"  lam={l} seed={s}: {'OK' if os.path.exists(o) else 'FALLO'}")


def paso3():
    out = "benchmarks/ablation_por_regla.csv"
    if os.path.exists(out):
        log("paso 3: ya existe, salto"); return
    log("paso 3: ancho por regla de los cuatro brazos del 2x2")
    cmd = [PY, "scripts/ablation_per_rule.py", "--out", out]
    with open(f"{LOG}/paso3.log", "w", encoding="utf-8") as f:
        subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
    log(f"paso 3: {'OK' if os.path.exists(out) else 'FALLO'}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    os.makedirs(LOG, exist_ok=True)
    if a.dry:
        print("1) eps-robustez seis metodos -> benchmarks/robustness_seis.csv")
        print("2) 40 evoluciones sin anchura -> benchmarks/lambda_nowidth/")
        print("3) ancho por regla 2x2       -> benchmarks/ablation_por_regla.csv")
        return
    t0 = time.time()
    paso1(); paso2(); paso3()
    log(f"cadena terminada en {(time.time()-t0)/3600:.1f} h")


if __name__ == "__main__":
    main()
