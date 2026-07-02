"""
Compara dos ejecuciones del benchmark y dice si la nueva versión es mejor o peor.

Uso:
    python scripts/compare_benchmarks.py benchmarks/baseline__abc123__*.json benchmarks/mi-cambio__def456__*.json

Interpretación:
- El makespan del RL se compara por problema con media +/- desviación entre
  semillas. Diferencias medias por debajo del ~3% con pocas semillas son ruido.
- Las heurísticas deterministas (SPT, LPT, MOR, MWKR) deben ser IDÉNTICAS
  entre versiones: si cambian, se cambió la semántica del entorno, no el
  aprendizaje del agente.
"""

import argparse
import glob
import json
import math
import sys

# La consola de Windows usa cp1252 por defecto; evitar crashes por caracteres
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Heurísticas que deben dar exactamente el mismo resultado entre versiones
DETERMINISTIC_ANCHORS = ("SPT", "LPT", "MOR", "MWKR")

# Umbral (%) por debajo del cual una diferencia media se considera ruido
NOISE_THRESHOLD_PCT = 3.0


def load(path):
    """Carga un JSON de benchmark; admite comodines (usa el más reciente)."""
    matches = sorted(glob.glob(path))
    if not matches:
        raise FileNotFoundError(f"No se encontró: {path}")
    with open(matches[-1], encoding="utf-8") as f:
        return json.load(f)


def mean(values):
    return sum(values) / len(values)


def std(values):
    if len(values) < 2:
        return 0.0
    m = mean(values)
    return math.sqrt(sum((v - m) ** 2 for v in values) / (len(values) - 1))


def collect_rl_makespans(result):
    """Devuelve {problema: [makespan por semilla]}"""
    per_problem = {}
    for seed_data in result["seeds"].values():
        for problem, metrics in seed_data["problems"].items():
            per_problem.setdefault(problem, []).append(metrics["rl_makespan"])
    return per_problem


def collect_anchors(result):
    """Devuelve {problema: {heurística: valor}} usando la primera semilla."""
    first_seed = next(iter(result["seeds"].values()))
    anchors = {}
    for problem, metrics in first_seed["problems"].items():
        heuristics = metrics.get("heuristics", {})
        anchors[problem] = {h: heuristics[h] for h in DETERMINISTIC_ANCHORS if h in heuristics}
    return anchors


def main():
    parser = argparse.ArgumentParser(description="Compara dos benchmarks")
    parser.add_argument("baseline", help="JSON del benchmark de referencia (versión A)")
    parser.add_argument("candidate", help="JSON del benchmark a evaluar (versión B)")
    args = parser.parse_args()

    a = load(args.baseline)
    b = load(args.candidate)

    print(f"A (referencia): {a['tag']} @ {a['commit']} ({a['branch']}) — {len(a['seeds'])} semillas, {a['config']['episodes']} episodios")
    print(f"B (candidato):  {b['tag']} @ {b['commit']} ({b['branch']}) — {len(b['seeds'])} semillas, {b['config']['episodes']} episodios")
    if a["config"]["episodes"] != b["config"]["episodes"] or a["config"]["seeds"] != b["config"]["seeds"]:
        print("AVISO: las configuraciones difieren (episodios/semillas) — la comparación no es equitativa.")
    print()

    # ------- Comparación del agente RL -------
    rl_a = collect_rl_makespans(a)
    rl_b = collect_rl_makespans(b)
    common = [p for p in rl_a if p in rl_b]
    if not common:
        print("No hay problemas comunes entre los dos benchmarks.")
        return

    print(f"{'Problema':<42} {'A: media+-std':>16} {'B: media+-std':>16} {'Dif.%':>8}  Veredicto")
    print("-" * 100)

    diffs = []
    for problem in common:
        ma, sa = mean(rl_a[problem]), std(rl_a[problem])
        mb, sb = mean(rl_b[problem]), std(rl_b[problem])
        diff_pct = (mb - ma) / ma * 100
        diffs.append(diff_pct)

        if abs(diff_pct) < NOISE_THRESHOLD_PCT:
            verdict = "~ ruido"
        elif diff_pct < 0:
            verdict = "MEJOR"
        else:
            verdict = "PEOR"

        print(f"{problem:<42} {ma:>10.1f}+-{sa:<4.1f} {mb:>10.1f}+-{sb:<4.1f} {diff_pct:>+7.2f}%  {verdict}")

    avg_diff = mean(diffs)
    better = sum(1 for d in diffs if d < -NOISE_THRESHOLD_PCT)
    worse = sum(1 for d in diffs if d > NOISE_THRESHOLD_PCT)
    print("-" * 100)
    print(f"Diferencia media: {avg_diff:+.2f}% (negativo = B mejor) | "
          f"mejor en {better}, peor en {worse}, ruido en {len(diffs) - better - worse} de {len(diffs)} problemas")

    if better > worse and avg_diff < -NOISE_THRESHOLD_PCT:
        print("VEREDICTO GLOBAL: B es MEJOR que A")
    elif worse > better and avg_diff > NOISE_THRESHOLD_PCT:
        print("VEREDICTO GLOBAL: B es PEOR que A")
    else:
        print("VEREDICTO GLOBAL: sin diferencia clara (dentro del ruido)")

    # ------- Chequeo de anclas deterministas -------
    anchors_a = collect_anchors(a)
    anchors_b = collect_anchors(b)
    mismatches = []
    for problem in common:
        for h in DETERMINISTIC_ANCHORS:
            va = anchors_a.get(problem, {}).get(h)
            vb = anchors_b.get(problem, {}).get(h)
            if va is not None and vb is not None and abs(va - vb) > 1e-6:
                mismatches.append((problem, h, va, vb))

    print()
    if mismatches:
        print("ATENCIÓN — las heurísticas deterministas cambiaron entre versiones.")
        print("Esto significa que cambió la SEMÁNTICA del entorno (no el aprendizaje):")
        for problem, h, va, vb in mismatches:
            print(f"  {problem} / {h}: {va:.1f} -> {vb:.1f}")
    else:
        print("Anclas deterministas (SPT/LPT/MOR/MWKR): idénticas — el entorno no cambió de semántica.")


if __name__ == "__main__":
    main()
