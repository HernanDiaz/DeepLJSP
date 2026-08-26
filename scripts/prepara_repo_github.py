# -*- coding: utf-8 -*-
"""Prepara github_drl/: el repositorio publico del proyecto DRL.

Solo el codigo de este proyecto: el paquete jobshop_rl y los scripts
de entrenamiento, evaluacion y analisis del paper DRL. Quedan fuera
las lineas de otros proyectos (evolucion GP y sus analisis por regla,
clones, siembra de poblaciones, DMU e instancias sinteticas) y el
utillaje interno del repo de trabajo. Se conserva el evaluador de
reglas GP (jobshop_rl/heuristics/gp_rule.py) porque los scripts de
comparacion del paper lo necesitan para reproducir las tablas 7 y 8.

No toca el codigo vivo: todo son copias a una carpeta nueva. No
inicializa git: eso lo hace el autor. Al final escanea el resultado y
ABORTA si alguna mencion de IA se cuela.

    python scripts/prepara_repo_github.py
"""
import glob
import os
import re
import shutil
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DESTINO = "github_drl"

# scripts de OTROS proyectos que conviven en scripts/
EXCLUIR = {
    # evolucion GP y analisis por regla (proyecto del paper de GP)
    "evolve_gp_rule", "rerun_evolutions_fixedfit", "confirm_gp_tuned",
    "audit_paper_gp_numbers", "pilot_robust_fitness", "lambda_sweep",
    "lambda_per_rule", "lambda_nowidth_per_rule", "ablation_per_rule",
    "rule_anatomy", "time_gp_arm", "neighbourhood_analysis",
    "midpoint_control", "midpoint_control_eval", "coefficient_sweep",
    "tuned_campaign", "check_domination", "audit_bestofn_pools",
    # clones y prototipos de imitacion
    "eval_sint", "proto_imitacion", "proto_imitacion_ts",
    "genera_tai_sinteticas",
    # siembra de poblaciones
    "analyze_pools", "gen_missing_pools", "pool_diversity",
    "pool_robustness", "compare_generators", "plot_generators",
    # lineas futuras y utillaje del repo de trabajo
    "eval_dmu", "genera_dmu_intervalar", "cadena_pendientes",
    "prepara_zenodo_drl", "prepara_repo_github",
}
PREFIJOS_EXCLUIR = ("clon_",)


def copia(origen, destino):
    if os.path.isfile(destino) and \
            os.path.getsize(destino) == os.path.getsize(origen):
        return 0
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    shutil.copy2(origen, destino)
    return 1


def main():
    os.makedirs(DESTINO, exist_ok=True)
    n = 0
    for f in glob.glob("jobshop_rl/**/*.py", recursive=True):
        if "__pycache__" not in f:
            n += copia(f, os.path.join(DESTINO, f))
    for f in glob.glob("scripts/*.py"):
        base = os.path.splitext(os.path.basename(f))[0]
        if base in EXCLUIR or base.startswith(PREFIJOS_EXCLUIR):
            continue
        n += copia(f, os.path.join(DESTINO, f))
    for f in ("paper/make_figures.py", "paper/verify_numbers.py"):
        n += copia(f, os.path.join(DESTINO, "paper_tools",
                                   os.path.basename(f)))
    print(f"{n} ficheros de codigo copiados")

    # el escaner: ninguna mencion de IA puede viajar en el paquete.
    # Excepcion unica: el titulo de la seccion de declaracion que EAAI
    # exige en el manuscrito ("Declaration of generative AI..."), que
    # el verificador comprueba literalmente; esa linea es terminologia
    # de la revista, no un rastro de herramienta
    patron = re.compile(r"claude|anthropic|copilot|chatgpt|co-authored|"
                        r"generative ai|ai-generated|llm", re.I)
    permitida = re.compile(r"declaration of generative ai", re.I)
    malos = []
    for f in glob.glob(os.path.join(DESTINO, "**", "*"), recursive=True):
        if not os.path.isfile(f) or os.path.basename(f) == "escaneo.txt":
            continue
        try:
            texto = open(f, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        lineas = texto.splitlines()
        for m in patron.finditer(texto):
            linea = texto[:m.start()].count("\n") + 1
            if permitida.search(lineas[linea - 1]):
                continue
            malos.append(f"{f}:{linea}: {m.group(0)}")
    if malos:
        print("ABORTADO: menciones encontradas:")
        for x in malos[:20]:
            print(" ", x)
        sys.exit(1)
    print("escaneo de menciones: limpio")


if __name__ == "__main__":
    main()
