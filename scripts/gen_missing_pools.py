"""
Genera los pools de semillas que falten para un conjunto de clases y
generadores, saltando los que ya existen en seeds/. Reanudable: si se
interrumpe, relanzar y continúa donde iba.

Uso:
  python scripts/gen_missing_pools.py --classes 50_15,50_20 --generators gp
  python scripts/gen_missing_pools.py --classes 15_15,20_15 --generators gp,gtmwkr --ft10
"""

import argparse
import os
import subprocess
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
sys.path.insert(0, ".")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GEN_ARGS = {
    "gp": ["--generator", "grasp", "--rules", "gp", "--epsilon", "0.1",
           "--suffix", "gp"],
    "gtmwkr": ["--generator", "grasp", "--rules", "gtmwkr", "--epsilon", "0.1",
               "--suffix", "gtmwkr"],
    "graspmix": ["--generator", "grasp", "--rules", "spt,lpt,mor,mwkr",
                 "--epsilon", "0.1", "--suffix", "graspmix"],
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--classes", required=True,
                        help="clases separadas por comas, p.ej. 50_15,50_20")
    parser.add_argument("--generators", required=True,
                        help="gp,gtmwkr,graspmix (separados por comas)")
    parser.add_argument("--ft10", action="store_true",
                        help="incluir también ft10_interval")
    parser.add_argument("--n", type=int, default=1024)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()

    instances = []
    for cls in (c.strip() for c in args.classes.split(",") if c.strip()):
        instances += [f"int__tai{cls}_{i:02d}" for i in range(1, 11)]
    if args.ft10:
        instances.append("ft10_interval")

    gens = [g.strip() for g in args.generators.split(",") if g.strip()]
    pend = [(g, inst) for g in gens for inst in instances
            if not os.path.exists(os.path.join("seeds", f"{inst}_{g}_pool.csv"))]
    print(f"pendientes: {len(pend)} pools "
          f"({len(gens)} generadores x {len(instances)} instancias, "
          f"saltando existentes)", flush=True)

    t0 = time.time()
    for k, (g, inst) in enumerate(pend, 1):
        cmd = [sys.executable, "scripts/export_v2_seeds.py",
               "--instance", inst, "--n", str(args.n),
               "--seed", str(args.seed), "--out", "seeds"] + GEN_ARGS[g]
        r = subprocess.run(cmd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        ultima = (r.stdout.strip().splitlines() or ["(sin salida)"])[-1]
        estado = "OK" if r.returncode == 0 else f"FALLO rc={r.returncode}"
        print(f"[{k}/{len(pend)}] {g} {inst}: {estado} | {ultima} | "
              f"{(time.time()-t0)/60:.0f} min acumulados", flush=True)
        if r.returncode != 0:
            print(r.stderr[-500:], flush=True)

    print(f"\nHECHO: {len(pend)} pools en {(time.time()-t0)/3600:.1f} h",
          flush=True)


if __name__ == "__main__":
    main()
