"""
Ejecuta un benchmark reproducible para comparar versiones del código.

Cada ejecución lanza el pipeline batch real (python -m jobshop_rl.main) una vez
por semilla, recoge las métricas de test_results.csv y guarda un JSON en
benchmarks/ etiquetado con el commit actual. Los resultados se comparan luego
con scripts/compare_benchmarks.py.

Uso:
    python scripts/run_benchmark.py --tier quick --tag mi-cambio
    python scripts/run_benchmark.py --tier full --tag baseline

Niveles:
    quick: 1 problema de entrenamiento, 2 de evaluación, 30 episodios, 1 semilla (~10 min)
    full:  el experimento estándar (4 train 20x15, 6 eval 20x15),
           100 episodios, 3 semillas (~horas)
"""

import argparse
import ast
import datetime
import json
import os
import subprocess
import sys
import time

import pandas as pd

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BENCHMARKS_DIR = os.path.join(REPO_ROOT, "benchmarks")

TIERS = {
    "quick": {
        "train": ["int__tai20_15_01"],
        "eval": ["int__tai20_15_05", "int__tai20_15_06"],
        "episodes": 30,
        "seeds": [2],
    },
    "full": {
        "train": ["int__tai20_15_01", "int__tai20_15_02", "int__tai20_15_03", "int__tai20_15_04"],
        "eval": [
            "int__tai20_15_05", "int__tai20_15_06", "int__tai20_15_07",
            "int__tai20_15_08", "int__tai20_15_09", "int__tai20_15_10",
            # NOTA: la evaluación zero-shot en otros tamaños (p.ej. 15x15) no es
            # posible hoy: la entrada de la red de valor depende de num_jobs y
            # num_machines, así que los pesos no cargan entre tamaños distintos.
            # Requeriría una representación de estado independiente del tamaño.
        ],
        "episodes": 100,
        "seeds": [2, 3, 4],
    },
    # Control del punto medio (espejo del control del paper del GP): las
    # instancias crisp SON el escenario del punto medio de sus versiones
    # intervalares (perturbacion simetrica), asi que entrenar en crisp y
    # evaluar en intervalo mide que aporta entrenar con intervalos.
    "midpoint": {
        "train": ["tai20_15_01", "tai20_15_02", "tai20_15_03", "tai20_15_04"],
        "eval": [
            "int__tai20_15_05", "int__tai20_15_06", "int__tai20_15_07",
            "int__tai20_15_08", "int__tai20_15_09", "int__tai20_15_10",
        ],
        "episodes": 1000,
        "seeds": [2, 3, 4],
    },
}


def get_git_info():
    """Devuelve (commit_corto, branch, dirty) del repositorio."""
    def run(cmd):
        return subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT).stdout.strip()

    commit = run(["git", "rev-parse", "--short", "HEAD"])
    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    dirty = bool(run(["git", "status", "--porcelain"]))
    return commit, branch, dirty


def run_seed(tier_config, seed, episodes, output_name):
    """Lanza una ejecución batch completa para una semilla y devuelve sus métricas."""
    # Coma final si hay un solo problema: las versiones antiguas del código
    # solo cargan problemas por ID cuando la lista contiene una coma
    train_arg = ",".join(tier_config["train"])
    if len(tier_config["train"]) == 1:
        train_arg += ","

    cmd = [
        sys.executable, "-m", "jobshop_rl.main",
        "--mode", "batch",
        "--train-problem", train_arg,
        "--eval-problem", ",".join(tier_config["eval"]),
        # Usar el flag nativo del modo batch: --episodes tiene default 300 y
        # main.py no distingue "300 explícito" del default (lo ignoraría)
        "--episodes-per-problem", str(episodes),
        "--reward", "adaptive",
        "--output-dir", output_name,
        "--use-ortools",
        "--seed", str(seed),
    ]

    print(f"  Semilla {seed}: {' '.join(cmd[2:])}")
    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT)
    wall_time = time.time() - start

    if result.returncode != 0:
        print(result.stdout[-3000:])
        print(result.stderr[-3000:])
        raise RuntimeError(f"La ejecución con semilla {seed} falló (código {result.returncode})")

    # Leer métricas del CSV de resultados de test
    csv_path = os.path.join(REPO_ROOT, "outputs", output_name, "test_results.csv")
    df = pd.read_csv(csv_path)

    problems = {}
    for _, row in df.iterrows():
        entry = {
            "rl_makespan": float(row["makespan"]),
            "lower_bound": float(row["lower_bound"]) if pd.notna(row.get("lower_bound")) else None,
        }
        if entry["lower_bound"]:
            entry["gap_vs_lb_pct"] = round(
                (entry["rl_makespan"] - entry["lower_bound"]) / entry["lower_bound"] * 100, 2)

        # Heurísticas (anclas deterministas + Random muestreado)
        heuristics = row.get("heuristic_results")
        if isinstance(heuristics, str):
            try:
                entry["heuristics"] = {k: float(v) for k, v in ast.literal_eval(heuristics).items()}
            except (ValueError, SyntaxError):
                pass
        elif isinstance(heuristics, dict):
            entry["heuristics"] = {k: float(v) for k, v in heuristics.items()}

        problems[row["problem"]] = entry

    return {"wall_time_s": round(wall_time, 1), "problems": problems}


def main():
    parser = argparse.ArgumentParser(description="Ejecuta el benchmark del proyecto")
    parser.add_argument("--tier", choices=list(TIERS.keys()), default="quick")
    parser.add_argument("--tag", required=True, help="Nombre para identificar esta ejecución (p.ej. 'baseline', 'fix-entropia')")
    parser.add_argument("--episodes", type=int, default=None, help="Sobrescribe los episodios del tier (para pruebas del propio script)")
    parser.add_argument("--seeds", type=str, default=None, help="Sobrescribe las semillas, separadas por comas (p.ej. '2,3')")
    args = parser.parse_args()

    tier_config = TIERS[args.tier]
    episodes = args.episodes or tier_config["episodes"]
    seeds = [int(s) for s in args.seeds.split(",")] if args.seeds else tier_config["seeds"]

    commit, branch, dirty = get_git_info()
    if dirty:
        print("AVISO: el repositorio tiene cambios sin commitear — el resultado no será "
              "reproducible desde el commit registrado.")

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_id = f"{args.tag}__{commit}__{timestamp}"
    print(f"Benchmark '{args.tier}' | tag={args.tag} | commit={commit} ({branch}{'+dirty' if dirty else ''})")
    print(f"Entrenamiento: {tier_config['train']}")
    print(f"Evaluación:    {tier_config['eval']}")
    print(f"Episodios: {episodes} | Semillas: {seeds}\n")

    results = {
        "tag": args.tag,
        "tier": args.tier,
        "commit": commit,
        "branch": branch,
        "dirty": dirty,
        "date": datetime.datetime.now().isoformat(),
        "config": {
            "train": tier_config["train"],
            "eval": tier_config["eval"],
            "episodes": episodes,
            "seeds": seeds,
        },
        "seeds": {},
    }

    total_start = time.time()
    for seed in seeds:
        output_name = f"bench_{run_id}_seed{seed}"
        results["seeds"][str(seed)] = run_seed(tier_config, seed, episodes, output_name)
        elapsed = results["seeds"][str(seed)]["wall_time_s"]
        print(f"  Semilla {seed} completada en {elapsed:.0f}s")

    results["total_wall_time_s"] = round(time.time() - total_start, 1)

    os.makedirs(BENCHMARKS_DIR, exist_ok=True)
    out_path = os.path.join(BENCHMARKS_DIR, f"{run_id}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nBenchmark completado en {results['total_wall_time_s']:.0f}s")
    print(f"Resultados guardados en: {os.path.relpath(out_path, REPO_ROOT)}")
    print("Compara dos ejecuciones con: python scripts/compare_benchmarks.py <A.json> <B.json>")


if __name__ == "__main__":
    main()
