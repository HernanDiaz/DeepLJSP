# -*- coding: utf-8 -*-
"""Contrasta las cifras clave de main.tex contra los ficheros de datos.

No comprueba la redaccion, solo que cada numero que el paper afirma aparezca
igual en su fuente. Pensado para pasarlo antes de enviar: si una campana se
rehace y alguna cifra se queda atras, aqui salta.

Uso: python paper_caie/verify_numbers.py
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


def check_zr(label, z, r, source):
    """El |r| tiene que ir en el mismo parentesis que su z: sin esto, un
    |r| pasa por coincidir con otro cualquiera del articulo."""
    global ok, bad
    pat = (r"z=" + re.escape(z) + r"\$,[^()]{0,40}?\$\|r\|="
           + re.escape(r))
    if re.search(pat, TEX_1L):
        ok += 1
        print(f"  OK    {label:<46} z={z} |r|={r}")
    else:
        bad += 1
        print(f"  FALLA {label:<46} esperaba z={z} con |r|={r} de {source}")


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

# ---- tiempos: tabla de baselines, 6.2 y 6.4 ----------------------------
# Todos los tiempos del articulo salen del simulador rapido, medidos en
# seis copias simultaneas (scripts/tiempos_fast.py, tiempos_fast_brazo.py
# y tiempos_fast_promedia.py). Se comprueba la fila entera, no solo la
# cifra, para que un numero no pase por aparecer en otro sitio.
tfj = os.path.join(REPO, "benchmarks/tiempos_fast.json")
if not os.path.exists(tfj):
    print("\n== tiempos: sin benchmarks/tiempos_fast.json ==")
else:
    import json as _json
    TF = _json.load(open(tfj, encoding="utf-8"))
    print("\n== tiempos (simulador rapido, seis copias) ==")
    _ms = {m: v["ms_media"] for m, v in TF["taillard"].items()}
    _ab = {r["method"]: r for r in csv.DictReader(open(os.path.join(
        REPO, "benchmarks/all_baselines.csv"), encoding="utf-8-sig"))}
    for _m, _et in (("LPT", "LPT"), ("SPT", "SPT"), ("CR", "CR"),
                    ("G&T-SPT", "G\\&T-SPT"), ("MWKR", "MWKR"),
                    ("MOR", "MOR"), ("EST", "EST"),
                    ("G&T-MWKR", "G\\&T-MWKR")):
        _r = _ab[_m]
        # cada baseline del simulador reproduce su RE de la tabla
        assert abs(TF["taillard"][_m]["re"] - float(_r["all"])) < 0.01, _m
        check(f"fila de baselines, {_m}",
              f"{_et} & {float(_r['all']):.1f} & {float(_r['sd']):.1f} & "
              f"{_ms[_m]:.1f} \\\\", "tiempos_fast.json")
    check("fila del despachador aleatorio",
          f"\\textit{{127.2}} & \\textit{{13.9}} & \\textit{{{_ms['Random']:.1f}}}",
          "tiempos_fast.json")
    _br = TF["brazo"]
    assert abs(_br["re_media"] - 18.99) < 0.005
    check("fila GP media de 30",
          f"GP rule (mean of 30) & 18.99 & 4.96 & {_br['ms_media']:.1f} \\\\",
          "tiempos_fast.json")
    check("fila GP mejor de 30",
          f"GP rule (best of 30) & 17.71 & 5.23 & {_br['ms_destacada_arbol']:.1f} \\\\",
          "tiempos_fast.json")
    check("fila GP simplificada",
          f"& 17.71 & 5.23 & {_ms['GP rule']:.1f} \\\\", "tiempos_fast.json")
    check("6.2, coste de la regla",
          f"${_br['ms_destacada_arbol']:.1f}$~ms as evolved, against "
          f"${_ms['MOR']:.1f}$~ms for MOR and ${_ms['G&T-MWKR']:.1f}$~ms",
          "tiempos_fast.json")
    check("6.2, forma simplificada",
          f"the same rule takes ${_ms['GP rule']:.1f}$~ms", "tiempos_fast.json")
    # la regla es mas cara que un atributo, pero no un orden de magnitud
    assert _br["ms_destacada_arbol"] < 10 * _ms["MOR"]
    _rc = TF["resumen_clasicas"]
    check("6.4, una pasada en las clasicas",
          f"${_rc['una_min'] * 1000:.0f}$--${_rc['una_max'] * 1000:.0f}$~ms",
          "tiempos_fast.json")
    check("6.4, mejor-de-1024 en las clasicas",
          f"${_rc['bon_min']:.1f}$--${_rc['bon_max']:.1f}$~s",
          "tiempos_fast.json")
    # no mas rapido que el genetico publicado (0.5-2.2 s) y del orden de
    # fEABC (1.9-6.8 s)
    assert _rc["bon_min"] > 0.5 and _rc["bon_max"] > 2.2
    assert _rc["bon_min"] < 6.8 and _rc["bon_max"] < 3 * 6.8

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
    # los contrastes sobre la medida absoluta: |r| es la biserial por
    # rangos (rb_abs), y va atado a su z
    for _par, _et in (('GP vs EST', 'GP contra EST'),
                      ('GP vs GT-MWKR', 'GP contra G&T-MWKR'),
                      ('GP-rob1 vs GP', 'robusto contra makespan'),
                      ('GP-rob1 vs GP-rob1-nw', 'robusto contra su ablacion'),
                      ('GP-rob4 vs GT-MWKR', 'lambda=4 contra G&T-MWKR')):
        _c = _u['contrastes'][_par]
        check_zr(f'z y |r| absolutos, {_et}',
                 f"-{abs(_c['z_abs']):.2f}", f"{_c['rb_abs']:.2f}",
                 'e1_robustez/uniform')
    # en cuantas de las 70 se desvia menos: se cuenta, no se deduce de |r|
    _uf = os.path.join(REPO, 'benchmarks/e1_robustez/uniform.csv')
    _dv = defaultdict(dict)
    for _r in csv.DictReader(open(_uf, encoding='utf-8')):
        if float(_r['width']) == 1.0:
            _dv[_r['method']][_r['instance']] = float(_r['abs_dev'])
    _nm = sum(_dv['GP-rob4'][i] < _dv['GT-MWKR'][i] for i in _dv['GP-rob4'])
    check('instancias en que lambda=4 se desvia menos que G&T-MWKR',
          f'smaller on {_nm} of the {len(_dv["GP-rob4"])} instances',
          'e1_robustez/uniform.csv')
    # la comparacion a RE parecido: los dos E[Cmax] y la reduccion
    _mu = _u['metodos']
    check('E[Cmax] lambda=4', f"${_mu['GP-rob4']['e_mid']:.0f}$",
          'e1_robustez/uniform')
    check('E[Cmax] G&T-MWKR', f"${_mu['GT-MWKR']['e_mid']:.0f}$",
          'e1_robustez/uniform')
    _red = 100 * (1 - _mu['GP-rob4']['abs'] / _mu['GT-MWKR']['abs'])
    check('reduccion de la desviacion a RE parecido', f"${_red:.1f}\\%$",
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

# E7: la cola del makespan ejecutado (CVaR al 0.95). Se recomputa desde
# las cifras por instancia de scripts/e7_cvar.py, no desde su resumen:
# medias, contrastes pareados y recuentos.
_e7 = os.path.join(REPO, 'benchmarks/e7_cvar/por_instancia.csv')
if not os.path.exists(_e7):
    print('\n== E7: sin benchmarks/e7_cvar/por_instancia.csv ==')
else:
    import numpy as _np
    from scipy import stats as _st
    sys.path.insert(0, os.path.join(REPO, 'scripts'))
    from efecto import biserial as _bis
    print('\n== E7: cola del makespan ejecutado (CVaR 0.95) ==')
    _T = defaultdict(lambda: defaultdict(dict))
    for _r in csv.DictReader(open(_e7, encoding='utf-8')):
        _T[_r['law']][_r['method']][_r['instance']] = (
            float(_r['cvar95_over']), float(_r['re_cvar']))

    def _media(ley, m, k):
        v = _T[ley][m]
        return sum(x[k] for x in v.values()) / len(v)

    def _contraste(ley, a, b, k):
        ins = sorted(_T[ley][a])
        x = [_T[ley][a][i][k] for i in ins]
        y = [_T[ley][b][i][k] for i in ins]
        d = _np.array(x) - _np.array(y)
        w = _st.wilcoxon(x, y, method='exact', zero_method='wilcox')
        n = int(_np.sum(_np.abs(d) > 1e-12))
        z = (w.statistic - n * (n + 1) / 4) / (
            n * (n + 1) * (2 * n + 1) / 24) ** 0.5
        z = abs(z) if d.mean() > 0 else -abs(z)
        return z, float(w.pvalue), _bis(x, y), int(_np.sum(d > 0))

    for _m in ('GP', 'GP-nowidth', 'GP-rob1', 'GP-rob4', 'GT-MWKR', 'EST'):
        check(f'CVaR del exceso, {_m}', f"${_media('uniform', _m, 0):.2f}",
              'e7_cvar/uniform')
    for _m in ('GP', 'GP-rob1', 'GP-rob4', 'GT-MWKR'):
        check(f'cola en RE, {_m}', f"{_media('uniform', _m, 1):.2f}",
              'e7_cvar/uniform')
    _g = _media('uniform', 'GP', 0)
    check('reduccion de la cola, lambda=1',
          f"${100 * (1 - _media('uniform', 'GP-rob1', 0) / _g):.1f}\\%$ less",
          'e7_cvar/uniform')
    check('reduccion de la cola a RE parecido',
          f"${100 * (1 - _media('uniform', 'GP-rob4', 0) / _media('uniform', 'GT-MWKR', 0)):.1f}\\%$ less",
          'e7_cvar/uniform')
    _d = _media('uniform', 'GP-rob1', 0) - _media('uniform', 'GP-rob1-nw', 0)
    check('lambda=1 contra su ablacion', f'${abs(_d):.2f}$ less than its own',
          'e7_cvar/uniform')
    # z sueltos y z con |r|
    for _a, _b, _k, _conr in (('GP', 'GT-MWKR', 0, False),
                              ('GP', 'EST', 0, False),
                              ('GP', 'GP-nowidth', 0, False),
                              ('GP-rob1', 'GP', 0, True),
                              ('GP-rob1', 'GP-rob1-nw', 0, True),
                              ('GP-rob4', 'GT-MWKR', 0, True),
                              ('GP-rob4', 'GT-MWKR', 1, True)):
        _z, _p, _rb, _ = _contraste('uniform', _a, _b, _k)
        if _conr:
            check_zr(f'CVaR, {_a} vs {_b} ({_k})', f'{_z:.2f}', f'{_rb:.2f}',
                     'e7_cvar/uniform')
        else:
            check(f'CVaR, z de {_a} vs {_b}', f'z={_z:.2f}$',
                  'e7_cvar/uniform')
        if _k == 1:
            check('p de la cola lambda=4 contra G&T-MWKR', f'p={_p:.3f}$',
                  'e7_cvar/uniform')
    # en cuantas instancias la cola del robusto es mas larga
    _n1 = _contraste('uniform', 'GP-rob1', 'GP', 1)[3]
    _n4 = _contraste('uniform', 'GP-rob4', 'GP', 1)[3]
    check('colas mas largas de los robustos',
          f'higher on {_n1} and on {_n4} of the 70 instances', 'e7_cvar')
    # las otras dos leyes: las reducciones citadas, y que todo conserva el
    # signo y la significacion salvo el contraste marginal que se nombra
    for _ley in ('triangular', 'pessimistic'):
        _v = _media(_ley, 'GP', 0) - _media(_ley, 'GP-rob1', 0)
        check(f'reduccion de la cola lambda=1, {_ley}', f'${_v:.2f}$',
              f'e7_cvar/{_ley}')
        for _a, _b, _k in (('GP', 'GT-MWKR', 0), ('GP', 'EST', 0),
                           ('GP-rob1', 'GP', 0), ('GP-rob1', 'GP-rob1-nw', 0),
                           ('GP-rob4', 'GT-MWKR', 0), ('GP-rob4', 'GT-MWKR', 1),
                           ('GP-rob1', 'GP', 1), ('GP-rob4', 'GP', 1)):
            _z, _p, _, _ = _contraste(_ley, _a, _b, _k)
            _z0 = _contraste('uniform', _a, _b, _k)[0]
            assert _z * _z0 > 0 and _p < 0.05, (_ley, _a, _b, _k, _z, _p)
            if _p > 0.01:
                check(f'contraste marginal, {_ley}', f'p={_p:.3f}$',
                      f'e7_cvar/{_ley}')
        _z, _p, _, _ = _contraste(_ley, 'GP', 'GP-nowidth', 0)
        assert _p > 0.05, ('la ablacion se separa', _ley, _p)

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
    # la dispersion entre convenios, por grupos DECLARADOS en el texto:
    # EST y MWKR (las que miran el estado del taller) y SPT y LPT. Antes
    # habia aqui un filtro "< 100" que dejaba fuera a SPT y hacia pasar
    # una afirmacion falsa; el grupo ahora es explicito.
    def _rango(_r):
        _v = _D['convenios'][_r]
        return max(_v.values()) - min(_v.values())
    check('dispersion maxima, EST y MWKR',
          f'more than ${max(_rango(r) for r in ("EST", "MWKR")):.1f}$ points',
          'e5, derivado')
    check('dispersion maxima, SPT y LPT',
          f'by at most ${max(_rango(r) for r in ("SPT", "LPT")):.1f}$',
          'e5, derivado')
    # el lexicografico de la tabla de baselines contra los tres convenios
    _bl = os.path.join(REPO, 'benchmarks/all_baselines.csv')
    _lex = {r['method']: float(r['all'])
            for r in csv.DictReader(open(_bl, encoding='utf-8'))}
    for _r in ('SPT', 'EST'):
        assert _lex[_r] < min(_D['convenios'][_r].values()), (
            f'{_r}: el lexicografico ya no es mejor que los tres convenios')
    _gap = max(_lex[_r] - min(_D['convenios'][_r].values())
               for _r in ('LPT', 'MWKR'))
    assert _gap > 0, 'LPT y MWKR ya no quedan por detras del mejor convenio'
    check('distancia del lexicografico al mejor convenio',
          f'within ${_gap:.1f}$ points of the best', 'e5 + all_baselines')
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
    # SPT dentro del conflict set es G&T-SPT, con el valor de la tabla de
    # baselines: antes el texto daba 71.03, del convenio de un solo
    # extremo, y la tabla 70.6, del lexicografico
    check('SPT dentro del conflict set, como G&T-SPT',
          f"reaches ${_lex['G&T-SPT']:.1f}$ inside the", 'all_baselines')
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

# r1.3: de que esta hecha la distancia con las metaheuristicas. Las
# cifras salen de scripts/e6_calibra_clasicas.py, que corre el
# genetico de jobshop_rl/heuristics/ga_interval.py sobre las doce
# clasicas con el decodificador y el evaluador del articulo.
_cc = os.path.join(REPO,
                   'benchmarks/e6_presupuesto/calibracion_clasicas.json')
if not os.path.exists(_cc):
    print('\n== r1.3: sin calibracion_clasicas.json ==')
else:
    import json as _json
    import math as _math
    _K = _json.load(open(_cc, encoding='utf-8'))
    print('\n== r1.3: la brecha, medida en construcciones ==')
    _m = _K['medias']
    _ga = {int(_k): _v for _k, _v in _m['ga'].items()}
    # la calibracion que abre 6.5: dos puntos de la curva y las dos
    # referencias publicadas
    check('el genetico a 5x10^5 construcciones',
          f'${_ga[500000]:.1f}\\%$ at $5\\times10^{{5}}$',
          'e6/calibracion_clasicas')
    check('el genetico publicado', f"${_m['ga_publicado']:.1f}\\%$",
          'eval_classic12.PUB_AVG')
    check('ESABC publicado', f"${_m['esabc_publicado']:.1f}\\%$",
          'eval_classic12.PUB_AVG')
    # nuestra version supera a la publicada, y se estanca antes de ESABC:
    # lo que baja de 10^5 a 5x10^5 es menos de lo que le falta
    assert _ga[500000] < _m['ga_publicado'], 'la reimplementacion no es fiel'
    assert (_ga[100000] - _ga[500000]
            < _ga[500000] - _m['esabc_publicado']), (
        'el genetico no se estanca antes de ESABC: reescribir 6.5')

# E6 (revision r2 y r3.5): calidad frente a presupuesto. Las cifras
# salen de scripts/e6_analiza.py sobre las curvas que deja
# scripts/e6_presupuesto.py, y la figura se dibuja del mismo json,
# asi que texto y dibujo no pueden separarse.
_e6 = os.path.join(REPO, 'benchmarks/e6_presupuesto/resumen.json')
if not os.path.exists(_e6):
    print('\n== E6: sin benchmarks/e6_presupuesto/resumen.json ==')
else:
    import json as _json
    import math as _math
    _B = _json.load(open(_e6, encoding='utf-8'))
    print('\n== E6: calidad frente a presupuesto ==')
    assert _B['n_instancias'] == 70, 'E6 no cubre las setenta'
    _E = _B['por_evaluaciones']
    check('la regla en una pasada', f"${_E['regla']['1']:.2f}\\%$",
          'e6/por_evaluaciones')
    # los dos cruces, interpolados en log sobre la rejilla

    def _cruza(_tab, _obj):
        _ks = sorted(int(_k) for _k in _tab)
        for _a, _b in zip(_ks, _ks[1:]):
            _va, _vb = _tab[str(_a)], _tab[str(_b)]
            if _va >= _obj > _vb:
                _f = (_va - _obj) / (_va - _vb)
                return 10 ** (_math.log10(_a) + _f *
                              (_math.log10(_b) - _math.log10(_a)))
        return None

    def _sci(_x):
        _e = int(_math.floor(_math.log10(_x)))
        return f'${_x / 10 ** _e:.1f}\\times10^{{{_e}}}$'

    check('donde el genetico iguala la pasada unica',
          _sci(_cruza(_E['ga'], _E['regla']['1'])), 'e6, derivado')
    # y que el genetico NO alcanza al mejor-de-1024 en el rango, que
    # es la afirmacion que sostiene la seccion entera
    assert _cruza(_E['ga'], _E['regla_bon']['1024']) is None, (
        'el genetico ya alcanza al mejor-de-1024: reescribir 6.5')
    # el coste de una pasada en evaluaciones del genetico
    _c = _B['coste_pasada_en_decodificaciones']
    check('lo que cuesta una pasada de la regla',
          f"${_c['min']:.0f}$ to ${_c['max']:.0f}$", 'e6/coste')

    # la tabla de 6.5, recomputada desde las curvas con las funciones de
    # scripts/e6_tabla.py, celda a celda
    sys.path.insert(0, os.path.join(REPO, 'scripts'))
    _cwd = os.getcwd()
    os.chdir(REPO)
    try:
        import e6_tabla as _t6
        _d6 = _t6.carga_completa()
    finally:
        os.chdir(_cwd)
    _in6 = sorted(_d6['ga'])
    _et6 = {'regla': 'Evolved rule, one pass',
            'gt_mwkr': 'G\\&T-MWKR, one pass',
            'regla_bon': 'Evolved rule, best-of-$N$',
            'ga': 'Genetic algorithm',
            'ga_sembrado': 'Genetic algorithm, seeded',
            'azar': 'Random permutations'}
    _pt6 = {}
    for _m6, _nom in _et6.items():
        _cel = []
        for _b in _t6.PRESUPUESTOS:
            _v = _t6.por_instancia_presupuesto(_d6, _m6, _b, _in6)
            _cel.append(f'{sum(_v) / len(_v):.2f}' if _v else '---')
        for _s in _t6.TIEMPOS:
            _v = _t6.por_instancia_tiempo(_d6, _m6, _s, _in6)
            _pt6[(_m6, _s)] = _v
            _cel.append(f'{sum(_v) / len(_v):.2f}' if _v else '---')
        check(f'fila de la tabla 6.5, {_m6}',
              _nom + ' & ' + ' & '.join(_cel) + ' \\\\', 'e6 curvas')
    # el tiempo de una pasada que el texto y la leyenda citan
    _seg = [_d6['regla'][_i][0][0][2] for _i in _in6]
    check('segundos de una pasada',
          f'complete after ${sum(_seg) / len(_seg):.2f}$~s', 'e6 curvas')

    def _m6(_m, _s):
        _v = _pt6[(_m, _s)]
        return f'{sum(_v) / len(_v):.2f}'

    for _a, _b, _s, _et in (('regla', 'ga', 20.0, 'pasada contra genetico'),
                            ('ga_sembrado', 'ga', 20.0, 'sembrado contra genetico')):
        _c6 = _t6.contraste(_pt6[(_a, _s)], _pt6[(_b, _s)])
        check_zr(f'{_et} a {_s:g} s', f"{_c6['z']:.2f}", f"{_c6['rb']:.2f}",
                 'e6 curvas')
        if _a == 'regla':
            check('instancias en que el genetico sigue por encima',
                  f"on ${_c6['menor']}$ of the 70", 'e6 curvas')
            assert _c6['p'] < 0.001 and _c6['d'] < 0
        if _a == 'ga_sembrado':
            check('ventaja del sembrado a 20 s',
                  f"${abs(_c6['d']):.2f}$ points below", 'e6 curvas')
    # la extension: el genetico se iguala con la pasada hacia los 50 s
    _c6 = _t6.contraste(_pt6[('regla', 50.0)], _pt6[('ga', 50.0)])
    assert _c6['p'] > 0.05, 'a 50 s el genetico ya no empata con la pasada'
    check('empate con la pasada a 50 s', f"($z={_c6['z']:.2f}$, n.s.)",
          'e6 curvas')
    _c6 = _t6.contraste(_pt6[('regla_bon', 150.0)], _pt6[('ga', 150.0)])
    assert _c6['p'] < 0.001
    check('mejor-de-N contra genetico a 150 s',
          f"still ${abs(_c6['d']):.2f}$ points below it ($z={_c6['z']:.2f}$",
          'e6 curvas')
    check_zr('mejor-de-N contra genetico a 150 s', f"{_c6['z']:.2f}",
             f"{_c6['rb']:.2f}", 'e6 curvas')
    # el sembrado alcanza al mejor-de-N: cruce y empate a 150 s
    _c6 = _t6.contraste(_pt6[('ga_sembrado', 150.0)], _pt6[('regla_bon', 150.0)])
    assert _c6['p'] > 0.05
    _a6 = _pt6[('ga_sembrado', 150.0)]
    _b6 = _pt6[('regla_bon', 150.0)]
    check('sembrado y mejor-de-N a 150 s',
          f"${sum(_a6) / len(_a6):.2f}\\%$ against ${sum(_b6) / len(_b6):.2f}\\%$,"
          f" $z={_c6['z']:.2f}$, n.s.", 'e6 curvas')
    import numpy as _np6
    _cr6 = None
    for _s in _np6.logspace(0, _np6.log10(150.0), 120):
        _a = _t6.por_instancia_tiempo(_d6, 'ga_sembrado', float(_s), _in6)
        _b = _t6.por_instancia_tiempo(_d6, 'regla_bon', float(_s), _in6)
        if _a and _b and sum(_a) < sum(_b):
            _cr6 = float(_s)
            break
    check('donde el sembrado alcanza al mejor-de-N',
          f"draw level at about ${_cr6:.0f}$~s", 'e6 curvas')
    # el genetico no alcanza al mejor-de-N en ningun presupuesto comun:
    # en schedules, hasta 2^13; en segundos, en una rejilla fina hasta
    # donde el mejor-de-N fue medido en las 70
    for _k in range(14):
        _x = _t6.por_instancia_presupuesto(_d6, 'regla_bon', 2 ** _k, _in6)
        _y = _t6.por_instancia_presupuesto(_d6, 'ga', 2 ** _k, _in6)
        assert sum(_x) < sum(_y), f'el genetico alcanza al mejor-de-N en 2^{_k}'
    for _s in [float(_v) for _v in __import__('numpy').logspace(-1, 3, 80)]:
        _x = _t6.por_instancia_tiempo(_d6, 'regla_bon', _s, _in6)
        _y = _t6.por_instancia_tiempo(_d6, 'ga', _s, _in6)
        if _x and _y:
            assert sum(_x) < sum(_y), f'el genetico alcanza al mejor-de-N a {_s:.1f} s'
    # la siembra: el final del sembrado, y lo que tarda el de inicio al azar
    _gac = {2 ** _k: sum(_v) / len(_v) for _k in range(21)
            for _v in [_t6.por_instancia_presupuesto(_d6, 'ga', 2 ** _k, _in6)]}
    _sv = _t6.por_instancia_presupuesto(_d6, 'ga_sembrado', 131072, _in6)
    _sf = sum(_sv) / len(_sv)
    _ks = sorted(_gac)
    for _a, _b in zip(_ks, _ks[1:]):
        if _gac[_a] >= _sf > _gac[_b]:
            _f = (_gac[_a] - _sf) / (_gac[_a] - _gac[_b])
            _xs = 10 ** (_math.log10(_a) + _f * (_math.log10(_b) - _math.log10(_a)))
    assert 131072 / _xs < 1 / 3, 'la siembra ya no ahorra dos tercios'

# E4 (revision r3.4): los cuatro brazos sobre intervalos asimetricos.
# Las cifras salen de scripts/e4_analiza.py sobre el banco que genera
# scripts/e4_genera_asimetricas.py.
_e4 = os.path.join(REPO, 'benchmarks/e4_asimetrico/resumen.json')
_e4g = os.path.join(REPO,
                    'benchmarks/e4_asimetrico/resumen_generacion.json')
if not os.path.exists(_e4):
    print('\n== E4: sin benchmarks/e4_asimetrico/resumen.json ==')
else:
    import json as _json
    sys.path.insert(0, os.path.join(REPO, 'scripts'))
    from efecto import biserial as _biserial
    _A = _json.load(open(_e4, encoding='utf-8'))
    print('\n== E4: intervalos asimetricos ==')
    assert _A['n_instancias'] == 70, 'E4 no cubre las setenta'
    check('realizaciones por instancia', f"${_A['K']}$ realizations",
          'e4/resumen')
    _ET = {'full': 'makespan full', 'nowidth': 'makespan sin anchura',
           'rob1': 'robusto full', 'rob1_nowidth': 'robusto sin anchura'}
    for _r, _et in _ET.items():
        _v = _A['ramas'][_r]
        assert _v['n'] == 15, f'{_r} no tiene quince semillas'
        for _k, _ek in (('re', 'RE'), ('anchura', 'anchura'),
                        ('abs', '|Delta|')):
            check(f'{_ek} de {_et}',
                  f"${_v[_k]['media']:.2f} \\pm {_v[_k]['sd']:.2f}$",
                  f'e4/{_r}')
    # los contrastes que el texto cita, y su correccion
    _C = _A['contrastes']
    for _par, _k, _et in (
            ('rob1 vs rob1_nowidth', 'anchura', 'anchura, robusto'),
            ('rob1 vs rob1_nowidth', 'abs', 'desviacion, robusto'),
            ('rob1 vs full', 'abs', 'desviacion, robusto vs makespan')):
        _c = _C[_par][_k]
        _a, _b = _par.split(' vs ')
        _ps = _A['ramas']
        _x = [_ps[_a]['por_semilla'][s][_k]
              for s in sorted(_ps[_a]['por_semilla'], key=int)]
        _y = [_ps[_b]['por_semilla'][s][_k]
              for s in sorted(_ps[_b]['por_semilla'], key=int)]
        check_zr(f'z y |r| de {_et}', f"-{abs(_c['z']):.2f}",
                 f"{_biserial(_x, _y):.2f}", f'e4/{_par}')
    # "en cada una de las quince semillas" solo si la biserial vale 1
    _ps = _A['ramas']
    _x = [_ps['rob1']['por_semilla'][s]['abs']
          for s in sorted(_ps['rob1']['por_semilla'], key=int)]
    _y = [_ps['full']['por_semilla'][s]['abs']
          for s in sorted(_ps['full']['por_semilla'], key=int)]
    assert (abs(_biserial(_x, _y) - 1.0) < 1e-12) == (
        'for every one of the fifteen seeds' in TEX_1L), (
        'el texto dice "cada una de las quince" y la biserial no es 1')
    check('Holm del RE bajo makespan, que no sobrevive',
          f"$p={_C['full vs nowidth']['re']['p_holm']:.2f}$ adjusted",
          'e4/full vs nowidth')
    # el mayor p ajustado entre los que el texto declara supervivientes
    _vivos = [_v['p_holm'] for _par, _d in _C.items() for _k, _v in
              _d.items() if _v['p_holm'] < 0.05]
    check('el mayor p ajustado de los que sobreviven',
          f'${max(_vivos):.4f}$', 'e4, derivado')
    assert len(_vivos) == 5, f'{len(_vivos)} contrastes sobreviven, no 5'
    # y los dos que NO sobreviven, que el texto tambien declara
    check('lo que cuesta la anchura bajo makespan',
          f"${_C['full vs nowidth']['re']['d']:.2f}$ points",
          'e4/full vs nowidth')
    check('la anchura bajo makespan no separa',
          f"$p={_C['full vs nowidth']['anchura']['p']:.2f}$",
          'e4/full vs nowidth')
if os.path.exists(_e4g):
    import json as _json2
    _G = _json2.load(open(_e4g, encoding='utf-8'))
    check('anchura media del banco asimetrico',
          f"${100 * _G['anchura_media_rel']:.1f}\\%$",
          'e4/resumen_generacion')
    check('operaciones del banco', f"${_G['n_operaciones']:,}$"
          .replace(',', '{,}'), 'e4/resumen_generacion')

# ---- tabla de baselines: la columna de RE, que antes nadie comprobaba --
_bl = os.path.join(REPO, 'benchmarks/all_baselines.csv')
if os.path.exists(_bl):
    print('\n== tab:baselines, columna de RE (all_baselines.csv) ==')
    _nombre = {'G&T-SPT': 'G\\&T-SPT', 'G&T-MWKR': 'G\\&T-MWKR',
               'GP (best)': 'GP rule (best of 30)'}
    for _r in csv.DictReader(open(_bl, encoding='utf-8')):
        # la fila 'GP (best)' de este fichero es de una campana anterior; las
        # filas GP de la tabla salen de summary.csv y se comprueban arriba
        if _r['method'] == 'GP (best)':
            continue
        _n = _nombre.get(_r['method'], _r['method'])
        _dec = 2 if _r['method'] == 'GP (best)' else 1
        check(f"RE y sd de {_r['method']}",
              f"{_n} & {float(_r['all']):.{_dec}f} & {float(_r['sd']):.1f}",
              'all_baselines.csv')

# ---- la guia de lambda, a nivel de brazo (lambda_sweep_tuned.csv) ----------
_sw = os.path.join(REPO, 'benchmarks/lambda_sweep/lambda_sweep_tuned.csv')
if os.path.exists(_sw):
    print('\n== guia de lambda (lambda_sweep_tuned.csv) ==')
    _L = {float(r['lambda']): r for r in csv.DictReader(open(_sw, encoding='utf-8'))}
    _re = {k: float(v['re_mean']) for k, v in _L.items()}
    _w = {k: float(v['width_mean']) for k, v in _L.items()}
    _sd = {k: float(v['re_sd']) for k, v in _L.items()}
    _t1 = (_re[2.0] - _re[0.5]) / (_w[0.5] - _w[2.0])
    _t2 = (_re[4.0] - _re[2.0]) / (_w[2.0] - _w[4.0])
    check('coste por punto de anchura, 0.5 a 2', f'costs\n${_t1:.1f}$ points',
          'lambda_sweep')
    check('RE perdido de 0.5 a 2', f'range costs ${_re[2.0] - _re[0.5]:.2f}$ points',
          'lambda_sweep')
    check('coste por punto de anchura, 2 a 4', f'rate rises to ${_t2:.1f}$',
          'lambda_sweep')
    check('anchura de 2 a 4', f'${_w[2.0] - _w[4.0]:.2f}$ points of width',
          'lambda_sweep')
    check('RE de 2 a 4', f'costing ${_re[4.0] - _re[2.0]:.2f}$ points',
          'lambda_sweep')
    check('dispersion de 2 a 4', f'from ${_sd[2.0]:.2f}$ to ${_sd[4.0]:.2f}$',
          'lambda_sweep')
    assert _t2 > _t1, 'el tramo alto ya no es mas caro: la guia no se sostiene'

# ---- las dos anchuras medias de los bancos ------------------------------
try:
    sys.path.insert(0, REPO)
    import contextlib as _cl
    import io as _io
    with _cl.redirect_stdout(_io.StringIO()):
        from jobshop_rl.data import PROBLEM_REGISTRY as _PR
        from jobshop_rl.models.interval import Interval as _Iv
    _cls = {(15, 15), (20, 15), (20, 20), (30, 15), (30, 20), (50, 15), (50, 20)}
    _ws = []
    for _p in _PR:
        _mm = re.fullmatch(r'int__tai(\d+)_(\d+)_(\d+)', _p)
        if not _mm or (int(_mm[1]), int(_mm[2])) not in _cls:
            continue
        for _fila in _PR[_p]()['durations']:
            for _dd in _fila:
                _lo, _up = ((_dd.lower, _dd.upper) if isinstance(_dd, _Iv)
                            else (_dd, _dd))
                _ws.append((_up - _lo) / ((_lo + _up) / 2))
    print('\n== anchura media de los dos bancos ==')
    check('anchura media del banco simetrico',
          f'against ${100 * sum(_ws) / len(_ws):.1f}\\%$ for the', 'instancias')
    # la diferencia entre los dos bancos, desde las medias sin redondear
    if os.path.exists(_e4g):
        _G2 = _json.load(open(_e4g, encoding='utf-8'))
        _dw = 100 * (_G2['anchura_media_rel'] - sum(_ws) / len(_ws))
        check('diferencia de anchura entre bancos',
              f'wider on average, by ${_dw:.1f}$ points of $p$',
              'e4/resumen_generacion e instancias')
except ImportError as _e:
    print(f'\n== anchura del banco simetrico: PEND ({_e}) ==')

# ---- el genetico de referencia, tal como lo describe 5.3 ---------------
_cg = os.path.join(REPO, 'benchmarks/e6_presupuesto/calibracion.json')
if os.path.exists(_cg):
    import json as _json3
    _G = _json3.load(open(_cg, encoding='utf-8'))
    print('\n== el genetico de referencia (calibracion.json) ==')
    assert _G['mejor'] == 'pop250 tor3 pm0.2', (
        'la configuracion del genetico ya no es la que describe 5.3')
    for _f in ('A population of $250$ individuals',
               'tournaments of size $3$', 'with probability $0.9$',
               'probability $0.2$ by swapping', 'of four configurations tried',
               f"${_G['presupuesto'] // 100000}\\times10^{{5}}$ constructions"):
        check('configuracion del genetico', _f, 'calibracion.json')

# ---- el deposito de Zenodo: lo que el articulo dice que contiene ---------
_zp = os.path.join(REPO, 'zenodo_caie', 'ijsp_gp_dataset.zip')
if os.path.exists(_zp):
    import zipfile as _zf
    with _zf.ZipFile(_zp) as _z:
        _nz = _z.namelist()
    print('\n== deposito de Zenodo (zenodo_caie/ijsp_gp_dataset.zip) ==')
    _nr = sum(1 for x in _nz if x.startswith('rules/') and x.endswith('.json'))
    check('reglas en el deposito', f'the {_nr} evolved rules', 'zip')
    for _d in ('interval_taillard', 'asymmetric_taillard', 'interval_classical'):
        _ni = sum(1 for x in _nz if x.startswith(f'instances/{_d}/'))
        assert _ni == {'interval_classical': 12}.get(_d, 70), (
            f'{_d}: {_ni} instancias en el deposito')
else:
    print('\n== deposito de Zenodo: PEND (falta zenodo_caie/ijsp_gp_dataset.zip) ==')

# ---- conformidad con la revista (Computers & Industrial Engineering) ----
print('\n== conformidad con C&IE ==')
_ab = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', TEX, re.S).group(1)
_npal = len(re.sub(r'\\[a-zA-Z]+\{?|[{}$]', ' ', _ab).split())
if _npal <= 250:
    ok += 1
    print(f'  OK    resumen en {_npal} palabras (tope 250)')
else:
    bad += 1
    print(f'  FALLA resumen en {_npal} palabras, tope 250')
_kw = re.search(r'\\begin\{keyword\}(.*?)\\end\{keyword\}', TEX, re.S).group(1)
_nkw = len(_kw.split(r'\sep'))
if 1 <= _nkw <= 7:
    ok += 1
    print(f'  OK    {_nkw} palabras clave (1 a 7)')
else:
    bad += 1
    print(f'  FALLA {_nkw} palabras clave, deben ser de 1 a 7')


print(f"\n{ok} comprobaciones correctas, {bad} fallos")
sys.exit(1 if bad else 0)
