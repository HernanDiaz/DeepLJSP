# -*- coding: utf-8 -*-
"""Contrasta las cifras clave de main.tex contra los ficheros de datos.

No comprueba la redaccion, solo que cada numero que el paper afirma aparezca
igual en su fuente. Pensado para pasarlo antes de enviar: si una campana se
rehace y alguna cifra se queda atras, aqui salta.

Uso: python paper_gp/verify_numbers.py
"""

import csv
import os
import re
import sys
from collections import defaultdict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TEX = open(os.path.join(HERE, "main.tex"), encoding="utf-8").read()
# las celdas destacadas van en \textbf{}: se desenvuelven para poder buscar la
# cifra tal cual, sin que el resaltado haga fallar la comprobacion
TEX = re.sub(r"\\textbf\{([^{}]*)\}", r"\1", TEX)

ok = bad = 0
# version con los espacios colapsados: una afirmacion en prosa puede quedar
# partida por el salto de linea, y entonces la busqueda literal falla aunque el
# paper este bien. Comparar tambien asi hace las comprobaciones inmunes al
# reflujo del texto.
TEX_1L = re.sub(r"\s+", " ", TEX)


def check(label, expected, source):
    """expected: cadena que debe aparecer en el tex, ignorando el reflujo."""
    global ok, bad
    if expected in TEX or re.sub(r"\s+", " ", expected) in TEX_1L:
        ok += 1
        print(f"  OK    {label:<46} {expected}")
    else:
        bad += 1
        print(f"  FALLA {label:<46} esperaba '{expected}' de {source}")


def stats(v):
    n = len(v)
    mu = sum(v) / n
    sd = (sum((x - mu) ** 2 for x in v) / (n - 1)) ** 0.5 if n > 1 else 0.0
    return mu, sd


# ---- brazo principal, desde summary.csv --------------------------------
per = defaultdict(dict)
for r in csv.DictReader(open(os.path.join(
        REPO, "benchmarks/reevo_fixedfit/summary.csv"), encoding="utf-8")):
    per[r["method"]][r["instance"]] = float(r["re"])

tuned = {k: v for k, v in per.items() if k.startswith("gp_tuned_seed")}
means = {k: sum(v.values()) / len(v) for k, v in tuned.items()}
mu, sd = stats(list(means.values()))
best = min(means, key=means.get)

print("\n== brazo principal (summary.csv) ==")
check("media de 30 sobre las 70", f"{mu:.2f} \\pm {sd:.2f}", "summary.csv")
check("mejor regla", f"{means[best]:.2f}", "summary.csv")
bv = list(tuned[best].values())
check("sd de la mejor entre instancias", f"{stats(bv)[1]:.2f}", "summary.csv")

# ---- ablacion y barrido, desde RESULTADOS.md ---------------------------
res = os.path.join(REPO, "benchmarks/tuned/RESULTADOS.md")
if os.path.exists(res):
    txt = open(res, encoding="utf-8").read()
    print("\n== ablacion y barrido (RESULTADOS.md) ==")
    for name, label in (("full (tuned)", "makespan full"),
                        ("no-width (tuned)", "makespan no-width"),
                        ("robust+width", "robusto con anchura"),
                        ("robust+nowidth", "robusto sin anchura")):
        m = re.search(r"\|\s*" + re.escape(name) + r"\s*\|\s*\d+\s*\|\s*"
                      r"([\d.]+) ± ([\d.]+)\s*\|\s*([\d.]+) ± ([\d.]+)", txt)
        if m:
            check(f"{label}: RE", f"{m.group(1)} \\pm {m.group(2)}", "RESULTADOS.md")
            check(f"{label}: ancho", f"{m.group(3)} \\pm {m.group(4)}", "RESULTADOS.md")
    for pat, label in ((r"RE z=(-?[\d.]+)", "Wilcoxon RE makespan"),
                       (r"ancho z=(-?[\d.]+)", "Wilcoxon ancho makespan")):
        m = re.search(pat, txt)
        if m:
            check(label, f"z={float(m.group(1)):.2f}", "RESULTADOS.md")

# ---- barrido de lambda, citado en prosa en 7.2 -------------------------
sw = os.path.join(REPO, "benchmarks/lambda_sweep/lambda_sweep_tuned.csv")
if os.path.exists(sw):
    print("\n== barrido de lambda (lambda_sweep_tuned.csv) ==")
    for r in csv.DictReader(open(sw, encoding="utf-8")):
        lam = float(r["lambda"])
        if lam in (0.5, 4.0):        # los dos extremos son los que cita 7.2
            check(f"lambda={lam:g}: RE",
                  f"{float(r['re_mean']):.2f} \\pm {float(r['re_sd']):.2f}",
                  "lambda_sweep_tuned.csv")
            check(f"lambda={lam:g}: ancho",
                  f"{float(r['width_mean']):.2f} \\pm "
                  f"{float(r['width_sd']):.2f}", "lambda_sweep_tuned.csv")

# ---- robustez, desde robustness_seis.csv -------------------------------
rob = os.path.join(REPO, "benchmarks/robustness_seis.csv")
if os.path.exists(rob):
    eps = defaultdict(lambda: defaultdict(list))
    wid = defaultdict(list)
    for r in csv.DictReader(open(rob, encoding="utf-8")):
        eps[r["method"]][r["width"]].append(float(r["eps_bar"]))
        if r["rel_width"]:
            wid[r["method"]].append(float(r["rel_width"]))
    print("\n== robustez (robustness_seis.csv) ==")
    for m in ("GP", "GP-nowidth", "GP-rob1", "GP-rob1-nw", "GP-rob4",
              "GT-MWKR", "EST"):
        w = sum(wid[m]) / len(wid[m])
        e = [sum(eps[m][k]) / len(eps[m][k]) for k in ("1.0", "1.2", "1.4")]
        check(f"{m}: ancho", f"{w:.2f}", "robustness_seis.csv")
        check(f"{m}: eps +0/+20/+40",
              " & ".join(f"{x:.2f}" for x in e),
              "robustness_seis.csv")

# ---- columna RE de tab:robustness, desde los CSV por regla -------------
apr = os.path.join(REPO, "benchmarks/ablation_por_regla.csv")
lpr = os.path.join(REPO, "benchmarks/lambda_por_regla.csv")
if os.path.exists(apr):
    porregla = {(r["objetivo"], r["terminales"], r["seed"]): float(r["re"])
                for r in csv.DictReader(open(apr, encoding="utf-8"))}
    print("\n== RE de tab:robustness (ablation_por_regla.csv) ==")
    for key, label in ((("makespan", "full", "1"), "GP makespan"),
                       (("makespan", "nowidth", "25"), "GP makespan sin anchura"),
                       (("robust", "full", "13"), "GP robusto l=1"),
                       (("robust", "nowidth", "8"), "GP robusto l=1 sin anchura")):
        check(f"RE {label}", f"{porregla[key]:.2f}", "ablation_por_regla.csv")
if os.path.exists(lpr):
    lam4 = {r["seed"]: float(r["re"])
            for r in csv.DictReader(open(lpr, encoding="utf-8"))
            if r["lam"] == "4.0"}
    check("RE GP robusto l=4", f"{lam4['10']:.2f}", "lambda_por_regla.csv")

# ---- 12 clasicas -------------------------------------------------------
cl = os.path.join(REPO, "benchmarks/classic12_tuned.csv")
if os.path.exists(cl):
    rows = list(csv.DictReader(open(cl, encoding="utf-8")))
    print("\n== 12 clasicas (classic12_tuned.csv) ==")
    for c, label in (("gp", "pase unico"), ("gp64", "best-of-64"),
                     ("gp1024", "best-of-1024")):
        m = sum(float(r[c]) for r in rows) / len(rows)
        check(f"media {label}", f"{m:.1f}", "classic12_tuned.csv")
    for r in rows[:3]:
        check(f"{r['inst']}: fila completa",
              f"{float(r['gp']):.1f} & {float(r['gp64']):.1f} & "
              f"{float(r['gp1024']):.1f}", "classic12_tuned.csv")

# ---- lo que 5.3 afirma de las elites, contra el log de irace -----------
# el paper describe el conjunto elite en prosa; se comprueba contra el log en
# vez de fiarse de la memoria, que es como llego a decir que las cuatro
# coincidian en torneo 7 cuando una tiene 4.
ir = os.path.join(REPO, "tuning/gp/irace_gp.log")
if os.path.exists(ir):
    log = open(ir, encoding="utf-8", errors="replace").read()
    blq = log.rsplit("# Best configurations as commandlines", 1)
    elites = re.findall(r"--tournament (\S+) --crossover (\S+) "
                        r"--maxtree (\S+) --elitism (\S+)", blq[-1])
    if elites:
        print("\n== elites de irace (tuning/gp/irace_gp.log) ==")
        tor = [e[0] for e in elites]
        cro = [float(e[1]) for e in elites]
        cap = sorted({e[2] for e in elites}, key=int)
        check("numero de elites", str(len(elites)), ir)
        check("elites con torneo 7", str(tor.count("7")), ir)
        check("banda de crossover",
              f"${min(cro):.2f}$--${max(cro):.2f}$", ir)
        check("caps que sobreviven",
              "$" + "$, $".join(cap[:-1]) + "$ and $" + cap[-1] + "$", ir)
        # la ganadora es la primera del bloque y tiene que ser la que imprime
        # tab:irace, celda a celda dentro del bloque de esa tabla
        w = elites[0]
        blq_tab = TEX[TEX.index("\\label{tab:irace}"):]
        blq_tab = blq_tab[:blq_tab.index("\\end{tabular}")]
        for fila, val in (("Tournament size", w[0]),
                          ("Crossover prob.", f"{float(w[1]):.2f}"),
                          ("Tree-size cap", w[2]),
                          ("Elitism", w[3])):
            linea = next((l for l in blq_tab.split("\n")
                          if l.startswith(fila)), "")
            marca = f"& ${val}$"
            if marca in linea:
                ok += 1
                print(f"  OK    {'ganadora irace: ' + fila:<46} {val}")
            else:
                bad += 1
                print(f"  FALLA {'ganadora irace: ' + fila:<46} "
                      f"esperaba '{marca}' de {ir}")

# ---- barrido de lambda SIN anchuras, citado en 7.2 ---------------------
# el CSV _completo sustituye al parcial (40/40 evoluciones); el parcial se
# conserva en el repositorio pero ya no es la fuente de ninguna cifra
nwl = os.path.join(REPO, "benchmarks/lambda_nowidth_por_regla_completo.csv")
if os.path.exists(nwl):
    porlam = defaultdict(list)
    for r in csv.DictReader(open(nwl, encoding="utf-8")):
        porlam[r["lam"]].append(float(r["ancho"]))
    print("\n== barrido sin anchuras (lambda_nowidth_por_regla_completo) ==")
    for lam in sorted(porlam):
        mu, sd = stats(porlam[lam])
        check(f"lambda={lam} sin anchuras: ancho",
              f"{mu:.2f} \\pm {sd:.2f}", "lambda_nowidth_por_regla_completo")

# ---- los cuatro tests de tab:ablation, desde los datos por regla -------
# RESULTADOS.md solo recoge los dos del objetivo de makespan, asi que el test
# de RE bajo el objetivo robusto no estaba comprobado por nadie. Se recalcula
# aqui desde el CSV por regla, que es la fuente primaria.
abl = os.path.join(REPO, "benchmarks/ablation_por_regla.csv")
if os.path.exists(abl):
    try:
        from scipy.stats import wilcoxon
    except ImportError:
        wilcoxon = None
    if wilcoxon is not None:
        def rank_biserial(x, y):
            """|r| = |W+ - W-|/(W+ + W-) sobre diferencias no nulas."""
            d = [a - b for a, b in zip(x, y) if a != b]
            orden = sorted(range(len(d)), key=lambda i: abs(d[i]))
            ranks, i = {}, 0
            while i < len(d):
                j = i
                while j + 1 < len(d) and abs(d[orden[j + 1]]) == abs(d[orden[i]]):
                    j += 1
                for k in range(i, j + 1):
                    ranks[orden[k]] = (i + j) / 2 + 1
                i = j + 1
            wp = sum(ranks[i] for i in range(len(d)) if d[i] > 0)
            wn = sum(ranks[i] for i in range(len(d)) if d[i] < 0)
            return abs(wp - wn) / (wp + wn)

        por = defaultdict(dict)
        for r in csv.DictReader(open(abl, encoding="utf-8")):
            por[(r["objetivo"], r["terminales"])][r["seed"]] = (
                float(r["re"]), float(r["ancho"]))
        print("\n== tests de tab:ablation (ablation_por_regla.csv) ==")
        for obj in ("makespan", "robust"):
            for i, que in ((0, "RE"), (1, "ancho")):
                a, b = por[(obj, "full")], por[(obj, "nowidth")]
                com = sorted(set(a) & set(b), key=int)
                x = [a[s][i] for s in com]
                y = [b[s][i] for s in com]
                st, p = wilcoxon(x, y, method="exact")
                n = len(com)
                z = (st - n * (n + 1) / 4) / (n * (n + 1) * (2 * n + 1) / 24) ** 0.5
                # la tabla lleva el signo del sentido del efecto: negativo si el
                # brazo con anchuras sale peor en esa medida
                z = z if sum(x) / n > sum(y) / n else -z
                if p >= 0.05:
                    check(f"{obj}/{que}: no significativo", f"z={z:.2f}", abl)
                else:
                    tramo = ("p<0.001" if p < 0.001 else
                             "p<0.01" if p < 0.01 else "p<0.05")
                    check(f"{obj}/{que}: test", f"z={z:.2f}$, ${tramo}", abl)
                    if que == "ancho":     # los |r| que la prosa de 7.2 cita
                        check(f"{obj}/{que}: efecto",
                              f"|r|={rank_biserial(x, y):.2f}", abl)

        # los |r| de eps-barra que cita 7.3, desde robustness_seis.csv
        rob = os.path.join(REPO, "benchmarks/robustness_seis.csv")
        if os.path.exists(rob):
            eps1 = defaultdict(dict)
            for r in csv.DictReader(open(rob, encoding="utf-8")):
                if r["width"] == "1.0":
                    eps1[r["method"]][r["instance"]] = float(r["eps_bar"])
            print("\n== efectos de eps-barra (robustness_seis.csv) ==")
            for a, b, label in (("GP", "GP-rob1", "GP vs robusto"),
                                ("GP-rob1", "GP-rob1-nw", "robusto vs ablacion"),
                                ("GP", "GT-MWKR", "GP vs G&T-MWKR")):
                com = sorted(set(eps1[a]) & set(eps1[b]))
                check(f"eps {label}: efecto",
                      f"|r|={rank_biserial([eps1[a][i] for i in com], [eps1[b][i] for i in com]):.2f}",
                      rob)

# ---- el minimo local de alpha=4 que cita 7.1 ---------------------------
cs = os.path.join(REPO, "benchmarks/coefficient_sweep.csv")
if os.path.exists(cs):
    alfa = sorted((float(r["value"]), float(r["re"]))
                  for r in csv.DictReader(open(cs, encoding="utf-8"))
                  if r["coef"] == "alpha_PT")
    vals = dict(alfa)
    print("\n== barrido de coeficientes (coefficient_sweep.csv) ==")
    # 7.1 afirma que un descenso local desde alpha=4 se atasca en un minimo
    # secundario a 0.6 puntos del global: comprobar que 4.0 ES minimo local
    # y que la distancia formateada es la que el texto imprime
    es_min = vals[4.0] < vals[3.75] and vals[4.0] < vals[4.25]
    if es_min:
        ok += 1
        print("  OK    alpha=4.0 es minimo local del barrido")
    else:
        bad += 1
        print("  FALLA alpha=4.0 ya no es minimo local; reescribir 7.1")
    glob = min(re_ for _, re_ in alfa)
    check("distancia del minimo secundario",
          f"{vals[4.0] - glob:.1f}$ points", cs)

# ---- control del punto medio, citado en 7.2 y tab:ablation -------------
mpc = os.path.join(REPO, "benchmarks/midpoint_control_por_regla.csv")
if os.path.exists(mpc):
    res, anc = [], []
    for r in csv.DictReader(open(mpc, encoding="utf-8")):
        res.append(float(r["re"]))
        anc.append(float(r["ancho"]))
    print("\n== control del punto medio (midpoint_control_por_regla.csv) ==")
    mu, sd = stats(res)
    check("control: RE", f"{mu:.2f} \\pm {sd:.2f}", mpc)
    mu, sd = stats(anc)
    check("control: ancho", f"{mu:.2f} \\pm {sd:.2f}", mpc)

# ---- eps-barra a nivel de brazo, citado en 7.3 -------------------------
epr = os.path.join(REPO, "benchmarks/eps_por_regla.csv")
if os.path.exists(epr):
    braz = defaultdict(list)
    for r in csv.DictReader(open(epr, encoding="utf-8")):
        braz[r["arm"]].append(float(r["eps_bar_x1000"]))
    print("\n== eps-barra por brazo (eps_por_regla.csv) ==")
    for a in ("full", "nowidth", "rob-full", "rob-nowidth"):
        mu, sd = stats(braz[a])
        check(f"brazo {a}: eps", f"{mu:.2f} \\pm {sd:.2f}", epr)

# ---- columna Time de tab:baselines -------------------------------------
# esta columna no estaba comprobada, y por eso sobrevivio una celda medida en
# otra tirada y con deriva de maquina. Todos los tiempos que el paper imprime
# tienen que venir de timing_tuned.csv, que es una sola tirada.
tim = os.path.join(REPO, "benchmarks/timing_tuned.csv")
if os.path.exists(tim):
    ms = {r["method"]: float(r["mean_ms"])
          for r in csv.DictReader(open(tim, encoding="utf-8"))}
    print("\n== tiempos de tab:baselines (timing_tuned.csv) ==")
    for m in ("LPT", "SPT", "CR", "Random", "G&T-SPT", "MWKR", "MOR", "EST",
              "G&T-MWKR", "GP rule"):
        check(f"{m}: s por pase", f"{ms[m] / 1000:.2f}", "timing_tuned.csv")
    # la dispersion que el texto afirma entre las tres filas comparables
    tres = [ms[m] for m in ("MOR", "GP rule", "G&T-MWKR")]
    check("dispersion MOR/GP/G&T-MWKR",
          f"{(max(tres) / min(tres) - 1) * 100:.0f}\\%", "timing_tuned.csv")

    # la celda 'GP rule (mean of 30)': por decision del autor el paper no
    # lleva nota, asi que la metodologia queda AQUI. Media del bloque limpio
    # de timing_gp_arm.csv (semillas 1 y 10-17, las 9 primeras en orden de
    # medicion, antes del escalon del 23% de deriva de maquina), calibrada a
    # la tirada de la columna por la regla compartida (seed1 en ambas).
    tga = os.path.join(REPO, "benchmarks/timing_gp_arm.csv")
    if os.path.exists(tga):
        arm = {r["rule"]: float(r["mean_ms"])
               for r in csv.DictReader(open(tga, encoding="utf-8"))}
        limpio = [arm[f"gp_tuned_seed{s}"]
                  for s in (1, 10, 11, 12, 13, 14, 15, 16, 17)]
        cal = (sum(limpio) / len(limpio)) * ms["GP rule"] / arm["gp_tuned_seed1"]
        check("GP rule (mean of 30): s por pase, calibrado",
              f"{cal / 1000:.2f}", tga)

# ---- apendice ----------------------------------------------------------
print("\n== apendice ==")
blk = TEX[TEX.index("\\label{tab:perinstance}"):]
blk = blk[blk.index("\\midrule"):blk.index("\\bottomrule")]
n_rows = len(re.findall(r"TA\d+ & \d+ &", blk))
print(f"  {'OK' if n_rows == 70 else 'FALLA'}    filas de la tabla por instancia: {n_rows}/70")
if n_rows != 70:
    bad += 1
else:
    ok += 1

print(f"\n{ok} comprobaciones correctas, {bad} fallos")
sys.exit(1 if bad else 0)
