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

# E0 (revision r3 de SWEVO): la regla destacada se elige sobre el
# conjunto de desarrollo, no sobre las setenta. Se recomprueba que
# el criterio no decide el resultado, que es lo que permite quitar
# la contaminacion sin mover ninguna cifra del articulo
import collections as _col
import csv as _csv
import re as _re
_DES = {f'int__tai20_15_{k:02d}' for k in range(5, 11)}
_por = _col.defaultdict(dict)
for _r in _csv.DictReader(open(os.path.join(
        REPO, 'benchmarks/reevo_fixedfit/summary.csv'),
        encoding='utf-8')):
    _m = _re.fullmatch(r'gp_tuned_seed(\d+)', _r['method'])
    if _m:
        _por[int(_m.group(1))][_r['instance']] = float(_r['re'])
_sem = sorted(_por)
_m70 = {_s: sum(_por[_s].values()) / len(_por[_s]) for _s in _sem}
_mde = {_s: sum(_por[_s][_i] for _i in _DES) / len(_DES)
        for _s in _sem}
_g70, _gde = min(_m70, key=_m70.get), min(_mde, key=_mde.get)
if len(_sem) == 30 and _g70 == _gde == 1:
    ok += 1
    print(f"  OK    {'destacada = ganadora de desarrollo (seed1)':<46} "
          f'desarrollo {_mde[_gde]:.2f}, 70 {_m70[_g70]:.2f}')
else:
    bad += 1
    print(f'  FALLA destacada: desarrollo seed{_gde}, 70 seed{_g70}')

# E1 (revision r3): la desviacion absoluta y las otras tres
# realizaciones. Las cifras salen del resumen que produce
# scripts/e1_analiza_robustez.py sobre benchmarks/e1_robustez/
_e1 = os.path.join(REPO, 'benchmarks/e1_robustez/resumen.json')
if not os.path.exists(_e1):
    print('\n== E1: sin benchmarks/e1_robustez/resumen.json ==')
else:
    import json as _json
    _R = _json.load(open(_e1, encoding='utf-8'))
    print('\n== E1: robustez absoluta y realizaciones ==')
    _u = _R['uniform']
    for _m, _et in (('GP', 'GP makespan'), ('GP-nowidth', 'sin anchura'),
                    ('GP-rob1', 'robusto lam=1'),
                    ('GP-rob1-nw', 'robusto lam=1 sin anchura'),
                    ('GP-rob4', 'robusto lam=4'),
                    ('GT-MWKR', 'G&T-MWKR'), ('EST', 'EST')):
        check(f'|Delta| de {_et}',
              f"{_u['metodos'][_m]['abs']:.2f}", 'e1_robustez/uniform')
    # el E[Cmax] de EST y de la regla, que el texto compara
    check('E[Cmax] de la regla',
          f"{_u['metodos']['GP']['e_mid']:.0f}", 'e1_robustez/uniform')
    check('E[Cmax] de EST',
          f"{_u['metodos']['EST']['e_mid']:.0f}", 'e1_robustez/uniform')
    # y los tres contrastes sobre la medida absoluta
    for _par, _et in (('GP vs EST', 'GP contra EST'),
                      ('GP vs GT-MWKR', 'GP contra G&T-MWKR'),
                      ('GP-rob1 vs GP', 'robusto contra makespan'),
                      ('GP-rob1 vs GP-rob1-nw', 'robusto contra su ablacion')):
        _c = _u['contrastes'][_par]
        check(f'z absoluto, {_et}', f"z=-{abs(_c['z_abs']):.2f}",
              'e1_robustez/uniform')
        check(f'|r| absoluto, {_et}', f"|r|={_c['r_abs']:.2f}",
              'e1_robustez/uniform')
    # las diferencias absolutas bajo las otras realizaciones
    for _d, _et in (('triangular', 'triangular'),
                    ('pessimistic', 'sesgada'),
                    ('worstcase', 'caso peor')):
        _v = abs(_R[_d]['contrastes']['GP-rob1 vs GP']['d_abs'])
        check(f'ventaja del robusto, {_et}', f'{_v:.2f}',
              f'e1_robustez/{_d}')
        check(f'|Delta| de la regla, {_et}',
              f"{_R[_d]['metodos']['GP']['abs']:.2f}",
              f'e1_robustez/{_d}')

# E2 (revision r1.1 y r2): sensibilidad al conjunto de entrenamiento.
# Las cifras salen de scripts/e2_analiza.py sobre
# benchmarks/e2_entrenamiento/. El nombre de cada campana en el json
# es el del script que las lanzo; aqui se mapea a las TA del paper.
_e2 = os.path.join(REPO, 'benchmarks/e2_entrenamiento/resumen.json')
if not os.path.exists(_e2):
    print('\n== E2: sin benchmarks/e2_entrenamiento/resumen.json ==')
else:
    import json as _json
    _S = _json.load(open(_e2, encoding='utf-8'))
    print('\n== E2: sensibilidad al conjunto de entrenamiento ==')
    _TA = {'cuatro_b': 'TA15--TA18', 'cuatro_c': 'TA17--TA20',
           'cuatro_d': 'TA12, 14, 16, 18', 'dos': 'TA11--TA12',
           'ocho': 'TA11--TA18'}
    check('referencia, media y sd',
          f"${_S['referencia']['media']:.2f} \\pm "
          f"{_S['referencia']['sd']:.2f}$", 'e2_entrenamiento')
    _medias = [_S['referencia']['media']]
    for _c, _v in sorted(_S['campanas'].items()):
        _medias.append(_v['media'])
        check(f'media y sd de {_TA[_c]}',
              f"${_v['media']:.2f} \\pm {_v['sd']:.2f}$",
              f'e2_entrenamiento/{_c}')
        check(f'mejor regla de {_TA[_c]}', f"{_v['min']:.2f}",
              f'e2_entrenamiento/{_c}')
        _sg = '+' if _v['d_vs_ref'] >= 0 else '-'
        check(f'diferencia de {_TA[_c]}',
              f"${_sg}{abs(_v['d_vs_ref']):.2f}$",
              f'e2_entrenamiento/{_c}')
        check(f'p de {_TA[_c]}', f"{_v['p']:.3f}",
              f'e2_entrenamiento/{_c}')
    # el rango de medias y el minimo de Holm, que el texto afirma
    check('rango de las seis medias',
          f'${max(_medias) - min(_medias):.2f}$ points', 'e2, derivado')
    check('media menor', f'${min(_medias):.2f}\\%$', 'e2, derivado')
    check('media mayor', f'${max(_medias):.2f}\\%$', 'e2, derivado')
    _ps = sorted(_v['p'] for _v in _S['campanas'].values())
    _m, _prev = len(_ps), 0.0
    _holm = []
    for _i, _pv in enumerate(_ps):
        _prev = max(_prev, min(1.0, _pv * (_m - _i)))
        _holm.append(_prev)
    check('menor p ajustado por Holm', f'${min(_holm):.2f}$',
          'e2, derivado')
    assert min(_holm) > 0.05, 'alguna campana pasa a ser significativa'
    # la sd entre semillas que el texto usa como vara de medir
    _sds = [_S['referencia']['sd']] + [_v['sd']
                                       for _v in _S['campanas'].values()]
    check('rango de sd entre semillas',
          f'${min(_sds):.2f}$--${max(_sds):.2f}$', 'e2, derivado')
    # el uso de terminales, los tres que el texto cita
    _fr = {_c: {_k: 100.0 * _n / sum(_u.values())
                for _k, _n in _u.items()}
           for _c, _u in _S['terminales'].items()}
    _ref = _fr['TA11-TA14']
    check('WKRW en la referencia', f"${_ref['WKRW']:.1f}\\%$",
          'e2/terminales')
    check('EST en la referencia', f"${_ref['EST']:.1f}\\%$",
          'e2/terminales')
    for _t in ('WKRW', 'EST'):
        _o = [_fr[_c][_t] for _c in _TA]
        check(f'rango de {_t} en las otras campanas',
              f'${min(_o):.1f}$--${max(_o):.1f}\\%$', 'e2/terminales')

# E3 (revision r1.4): el caso ilustrativo. Las cifras salen de
# scripts/e3_caso_ilustrativo.py; la figura, de make_e3_figure.py
# sobre el mismo json, asi que texto y dibujo no pueden separarse.
_e3 = os.path.join(REPO, 'benchmarks/e3_caso/caso.json')
if not os.path.exists(_e3):
    print('\n== E3: sin benchmarks/e3_caso/caso.json ==')
else:
    import json as _json
    _C = _json.load(open(_e3, encoding='utf-8'))
    print('\n== E3: caso ilustrativo ==')
    # las nueve duraciones, tal como el texto las enumera
    for _j, _fila in enumerate(_C['durations']):
        for _lo, _up in _fila:
            check(f'duracion de J{_j + 1}', f'$[{_lo},{_up}]$',
                  'e3_caso/durations')
    # la tabla de la decision: terminales y las dos puntuaciones
    _T, _el, _oi = _C['terminales'], _C['elegibles'], _C['op_idx']
    for _i, _j in enumerate(_el):
        _et = f'$o_{{{_j + 1}{_oi[_i] + 1}}}$'
        check(f'duracion de {_et}',
              f"$[{_C['pt_lo'][_i]:.0f},{_T['PT'][_i]:.0f}]$",
              'e3_caso/decision')
        for _k in ('WKR', 'WKRW', 'SLACK'):
            check(f'{_k} de {_et}', f'{_T[_k][_i]:.0f}',
                  'e3_caso/decision')
        check(f'Ec.(4) en {_et}', f"{_C['score_b1'][_i]:.0f}",
              'e3_caso/decision')
        check(f'beta=0 en {_et}', f"{_C['score_b0'][_i]:.0f}",
              'e3_caso/decision')
    # el trabajo restante de los dos candidatos que se disputan
    for _i, _j in enumerate(_el):
        if _j not in (_C['elige']['gp'], _C['elige']['b0']):
            continue
        _up = _T['WKR'][_i]
        check(f'trabajo restante de J{_j + 1}',
              f"$[{_up - _T['WKRW'][_i]:.0f},{_up:.0f}]$",
              'e3_caso/decision')
    # los cuatro makespans
    for _m, _et in (('gp', 'la regla'), ('b0', 'beta=0'),
                    ('spt', 'SPT'), ('mwkr', 'MWKR')):
        _lo, _up = _C['makespan'][_m]
        # sin los delimitadores: el primero va dentro de un
        # \mathbf{C}_{\max} = ... y los otros tres sueltos
        check(f'makespan de {_et}', f'[{_lo:.0f},{_up:.0f}]',
              'e3_caso/makespan')
    # el censo, que es lo que acota la lectura del ejemplo
    _z = _C['censo']
    for _k, _et in (('n', 'instancias del censo'),
                    ('igual', 'trazas que no cambian'),
                    ('divergen', 'trazas que cambian'),
                    ('empata', 'cambian y empatan'),
                    ('mejora', 'la anchura mejora'),
                    ('empeora', 'la anchura empeora')):
        check(_et, f'${_z[_k]}$', 'e3_caso/censo')
    assert _z['igual'] + _z['divergen'] == _z['n'], 'censo descuadrado'
    assert (_z['empata'] + _z['mejora'] + _z['empeora']
            == _z['divergen']), 'censo descuadrado'
    # y que el ejemplo siga siendo el que la figura dibuja
    check('la figura del caso', 'figures/fig_case.pdf', 'e3_caso')

# E5 (revision r3.3): convenios de intervalo y decodificador.
# Las cifras salen de scripts/e5_decodificador_baselines.py sobre
# benchmarks/e5_decodificador/resumen.json.
_e5 = os.path.join(REPO, 'benchmarks/e5_decodificador/resumen.json')
if not os.path.exists(_e5):
    print('\n== E5: sin benchmarks/e5_decodificador/resumen.json ==')
else:
    import json as _json
    _D = _json.load(open(_e5, encoding='utf-8'))
    print('\n== E5: convenios y decodificador ==')
    # el rango que abre cada regla entre los tres convenios
    for _r in ('SPT', 'LPT', 'MWKR', 'EST'):
        _v = _D['convenios'][_r]
        check(f'rango de {_r} entre convenios',
              f'${min(_v.values()):.1f}$ to ${max(_v.values()):.1f}$',
              'e5/convenios')
    # la mayor dispersion entre convenios, que el texto acota
    _sp = max(max(_v.values()) - min(_v.values())
              for _v in _D['convenios'].values()
              if max(_v.values()) < 100)
    check('mayor dispersion entre convenios', f'${_sp:.1f}$ points',
          'e5, derivado')
    # el cuadro de dos por dos del decodificador
    _dec = _D['decodificador']
    check('la regla en semiactivo, media y sd',
          f"$\\mathbf{{{_dec['gp_semiactivo']['media']:.2f}}} \\pm "
          f"{_dec['gp_semiactivo']['sd']:.2f}$", 'e5/decodificador')
    check('la regla en G&T, media y sd',
          f"${_dec['gp_en_gt']['media']:.2f} \\pm "
          f"{_dec['gp_en_gt']['sd']:.2f}$", 'e5/decodificador')
    check('la destacada en semiactivo',
          f"{_dec['gp_semiactivo']['destacada']:.2f}",
          'e5/decodificador')
    check('la destacada en G&T',
          f"{_dec['gp_en_gt']['destacada']:.2f}", 'e5/decodificador')
    check('SPT dentro del conflict set',
          f"{_dec['gt_spt']['media']:.2f}", 'e5/decodificador')
    # lo que cuesta a la regla entrar en el conflict set
    _d = _dec['gp_en_gt']['media'] - _dec['gp_semiactivo']['media']
    check('lo que pierde la regla en G&T', f'${_d:.1f}$ points',
          'e5, derivado')
    check('el contraste de la destacada',
          f"$p = {_dec['contraste_destacada']['p']:.2f}$",
          'e5/decodificador')
    # y que G&T-MWKR sigue siendo el de la tabla de baselines
    assert abs(_dec['gt_mwkr']['media'] - 29.5) < 0.1, (
        'G&T-MWKR ya no reproduce la tabla de baselines')

print(f"\n{ok} comprobaciones correctas, {bad} fallos")
sys.exit(1 if bad else 0)
