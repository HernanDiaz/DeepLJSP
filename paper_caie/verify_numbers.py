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
# el material suplementario tambien afirma cifras: se verifican igual. Cada
# fichero se une con una linea en blanco, que no crea coincidencias entre
# el final de uno y el principio del otro
_SUPL = os.path.join(HERE, "supplementary.tex")
if os.path.exists(_SUPL):
    TEX += "\n\n" + open(_SUPL, encoding="utf-8").read()
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
    # 7.5 ya no da las cinco medias: da su recorrido, de la menor a la
    # mayor, y lo compara con el del brazo completo
    medias = {lam: stats(v)[0] for lam, v in porlam.items()}
    # lambda = 1 no esta en este CSV: es el brazo robusto sin anchuras de
    # la ablacion, con sus treinta evoluciones
    _abl1 = [float(r["ancho"]) for r in csv.DictReader(open(os.path.join(
        REPO, "benchmarks/ablation_por_regla.csv"), encoding="utf-8"))
        if r["objetivo"] == "robust" and r["terminales"] != "full"]
    assert len(_abl1) == 30, len(_abl1)
    medias["1.0"] = stats(_abl1)[0]
    assert len(medias) == 5, sorted(medias)
    check("sin anchuras: recorrido del ancho",
          f"between ${min(medias.values()):.2f}$ and "
          f"${max(medias.values()):.2f}$", "lambda_nowidth_por_regla_completo")
    # la amplitud, de los valores sin redondear (el pie de fig:lambda);
    # restar los extremos ya redondeados da una centesima de mas
    check("sin anchuras: amplitud del recorrido",
          f"fall within ${max(medias.values()) - min(medias.values()):.2f}$ "
          f"points", "lambda_nowidth_por_regla_completo")

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

# ---- anatomia de las 30 reglas (7.1) -----------------------------------
# Se recomputa desde los arboles, con las funciones de rule_anatomy.py, y
# el CSV que va al deposito tiene que coincidir fila a fila.
sys.path.insert(0, os.path.join(REPO, "scripts"))
sys.path.insert(0, REPO)
import glob as _glob
import json as _json
import rule_anatomy as _ra
_an = {}
for _f in sorted(_glob.glob(os.path.join(
        REPO, "benchmarks/reevo_fixedfit/gp_tuned_seed*.json"))):
    _tr = _json.load(open(_f, encoding="utf-8"))["tree"]
    _nodos = list(_ra.walk(_tr))
    _ts = [_n for _n in _nodos if _n in _ra.TERMINALS]
    _an[os.path.basename(_f)] = (len(_nodos), _ra.depth(_tr), len(_ts),
                                 sum(_t in _ra.WIDTH_TERMS for _t in _ts))
assert len(_an) == 30, len(_an)
print("\n== anatomia de las 30 reglas ==")
_csv = {r["rule"]: (int(r["size"]), int(r["depth"]), int(r["n_terminals"]),
                    int(r["width_terms"]))
        for r in csv.DictReader(open(os.path.join(
            REPO, "benchmarks/rule_anatomy.csv"), encoding="utf-8"))}
assert _csv == _an, "rule_anatomy.csv no coincide con los arboles"
_sz = [v[0] for v in _an.values()]
_dp = [v[1] for v in _an.values()]
check("tamano medio y rango",
      f"mean tree size of ${sum(_sz) / 30:.0f}$ nodes (${min(_sz)}$--${max(_sz)}$)",
      "reglas")
check("profundidad media", f"mean depth ${sum(_dp) / 30:.0f}$", "reglas")
check("cuota de terminales de anchura",
      f"account for ${100 * sum(v[3] for v in _an.values()) / sum(v[2] for v in _an.values()):.1f}\\%$",
      "reglas")
check("reglas con algun terminal de anchura",
      f"appear in ${sum(v[3] > 0 for v in _an.values())}$ of the $30$", "reglas")

# ---- la mejor regla de cada generacion (6.1, figura 2) -----------------
_evm = os.path.join(REPO, "benchmarks/evolucion_mejores.json")
if os.path.exists(_evm):
    import numpy as _np
    _EM = _json.load(open(_evm, encoding="utf-8"))["semillas"]
    print("\n== la mejor regla de cada generacion ==")
    assert len(_EM) == 30

    def _med(g, k):
        return float(_np.median([_EM[s][str(g)][k] for s in _EM]))
    # el RE de entrenamiento recalculado es el del log
    assert max(abs(f["ent"] - f["re_log"]) for s in _EM.values()
               for f in s.values()) < 0.01
    check("entrenamiento, generaciones 10 y 50",
          f"falls from ${_med(10, 'ent'):.2f}$ to ${_med(50, 'ent'):.2f}$",
          "evolucion_mejores")
    check("prueba, generaciones 10 y 50",
          f"falls only from ${_med(10, 'pru'):.2f}$ to ${_med(50, 'pru'):.2f}$",
          "evolucion_mejores")
    check("validacion, generaciones 10 y 50",
          f"from ${_med(10, 'val'):.2f}$ to ${_med(50, 'val'):.2f}$:",
          "evolucion_mejores")
    check("tamano mediano al final",
          f"median of ${_med(50, 'size'):.0f}$ nodes", "evolucion_mejores")
    _an50 = 100 * _np.mean([_EM[s]["50"]["ancho"] for s in _EM])
    assert 15 < _an50 < 25, "los terminales de anchura ya no son un quinto"
    # el hueco que el texto afirma: entrenamiento baja mucho mas que fuera
    assert (_med(10, "ent") - _med(50, "ent")) > 3 * (
        _med(10, "pru") - _med(50, "pru"))

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
    # la cota inferior con que se leen SPT y MWKR: la carga mayor de un
    # trabajo o de una maquina, componente a componente
    _carga = {}
    for _j, _fila in enumerate(_C['durations']):
        for _k, (_a, _b) in enumerate(_fila):
            for _clave in (('J', _j), ('M', _C['sequences'][_j][_k])):
                _x = _carga.setdefault(_clave, [0, 0])
                _x[0] += _a
                _x[1] += _b
    _cota = (max(v[0] for v in _carga.values()),
             max(v[1] for v in _carga.values()))
    check('cota inferior del ejemplo', f'$[{_cota[0]:.0f},{_cota[1]:.0f}]$',
          'e3_caso/durations')
    _dueno = [k for k, v in _carga.items() if tuple(v) == _cota]
    assert _dueno == [('J', 0)], f'la cota no es la carga de J1: {_dueno}'
    check('la cota es el trabajo de J1', 'total work of $J_1$', 'e3_caso')
    # MWKR se separa de la regla en la segunda decision de su traza
    _sg, _sm, _ss = (_C['schedules'][m] for m in ('gp', 'mwkr', 'spt'))
    _k = next(k for k, (a, b) in enumerate(zip(_sg, _sm))
              if (a['job'], a['op']) != (b['job'], b['op']))
    assert _k == 1, f'MWKR diverge en la decision {_k + 1}'
    check('MWKR diverge en la segunda', 'at the second decision', 'e3_caso')

    def _op(sch, j, o):
        return next(x for x in sch if x['job'] == j and x['op'] == o)

    # MWKR: o32 antes que o21 en M1, que queda libre hasta el inicio de
    # o32, y o21 (primera de su trabajo) empieza despues de o32
    _o32, _o21 = _op(_sm, 2, 1), _op(_sm, 1, 0)
    assert _sm.index(_o32) < _sm.index(_o21)
    assert not [x for x in _sm if x['machine'] == 0
                and _sm.index(x) < _sm.index(_o32)], 'M1 no esta libre'
    check('MWKR deja M1 libre hasta', f"idle until $[{_o32['s_lo']:.0f},{_o32['s_up']:.0f}]$",
          'e3_caso/schedules')
    check('MWKR: inicio de o21', f"starts at $[{_o21['s_lo']:.0f},{_o21['s_up']:.0f}]$",
          'e3_caso/schedules')
    # SPT: el hueco de M3 entre dos operaciones consecutivas de la maquina
    _m3 = [x for x in _ss if x['machine'] == 2]
    _hueco = max(zip(_m3, _m3[1:]), key=lambda p: p[1]['s_up'] - p[0]['c_up'])
    check('SPT: hueco de M3',
          f"$M_3$ idle from $[{_hueco[0]['c_lo']:.0f},{_hueco[0]['c_up']:.0f}]$"
          f" to $[{_hueco[1]['s_lo']:.0f},{_hueco[1]['s_up']:.0f}]$",
          'e3_caso/schedules')
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

# la figura de 7.6 sale de e7_cvar/por_instancia.csv, que es tambien la
# fuente de las cifras de |Delta| y del exceso en la cola que cita el texto
check('la figura de 7.6', 'figures/fig_robustness_plane.pdf', 'e7_cvar')

# Dificultad por clase (6.3): las cotas del JSP crisp de Taillard de la
# tabla 14 de Coupvent des Graviers et al. (2025), frente a las cotas con
# que se calcula el RE (jobshop_rl/data/literature_bounds.py)
_cot = os.path.join(REPO, 'benchmarks/taillard_cotas_2025.csv')
if not os.path.exists(_cot):
    print('\n== dificultad por clase: sin benchmarks/taillard_cotas_2025.csv ==')
else:
    print('\n== dificultad por clase (taillard_cotas_2025.csv) ==')
    sys.path.insert(0, REPO)
    from jobshop_rl.data.literature_bounds import TAILLARD_LB as _TLB
    _cb = {r['instancia']: (int(r['lb']), int(r['ub'])) for r in csv.DictReader(
        l for l in open(_cot, encoding='utf-8') if not l.startswith('#'))}
    assert len(_cb) == 70
    _clases = ['15x15', '20x15', '20x20', '30x15', '30x20', '50x15', '50x20']
    _ab, _hu = {}, {}
    for _c, _cl in enumerate(_clases):
        _ks = [f'TA{10 * _c + k}' for k in range(1, 11)]
        _ab[_cl] = sum(_cb[k][0] < _cb[k][1] for k in _ks)
        _hu[_cl] = sum((_cb[k][1] - _TLB[k]) / _TLB[k] * 100 for k in _ks) / 10
    # las dos de 50 trabajos: todas cerradas y nuestra cota es el optimo
    for _cl in ('50x15', '50x20'):
        assert _ab[_cl] == 0, f'{_cl} tiene instancias abiertas'
        assert all(_cb[f'TA{k}'][1] == _TLB[f'TA{k}'] for k in
                   range(10 * _clases.index(_cl) + 1,
                         10 * _clases.index(_cl) + 11)), f'{_cl}: cota != optimo'
    check('las de 50 trabajos, resueltas',
          'every crisp counterpart has been solved to optimality', _cot)
    # 30x20: la clase con mas abiertas, y el hueco de su cota
    assert max(_ab, key=_ab.get) == '30x20' and _ab['30x20'] == 9, _ab
    check('30x20: abiertas', 'the most open instances, nine of ten', _cot)
    check('30x20: mejor conocida sobre la cota',
          f'by ${_hu["30x20"]:.1f}\\%$ on average', _cot)

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

# E6 version 2 (6.5): calidad frente a presupuesto en segundos, en las
# 12 clasicas y en las clases 15x15, 30x15 y 50x15 de Taillard. Las
# cifras salen de scripts/e6_v2_resumen.py y la figura de
# scripts/make_e6_presupuesto_caie.py, sobre las mismas curvas
# (benchmarks/e6_clasicas/curvas.csv y benchmarks/e6_tamanos/curvas.csv).
_e6v = os.path.join(REPO, 'benchmarks/e6_v2/resumen.json')
if not os.path.exists(_e6v):
    print('\n== E6: sin benchmarks/e6_v2/resumen.json ==')
else:
    import json as _json
    _V = _json.load(open(_e6v, encoding='utf-8'))
    print('\n== E6 v2: presupuesto en segundos (e6_v2/resumen.json) ==')
    _K6 = ('clasicas', '15_15', '30_15', '50_15')
    _C6 = _V['clasicas']
    # el diseno: corridas por instancia y horizontes
    assert all(_C6['corridas'][m] == 360 for m in ('regla_bon', 'ga', 'ga_sembrado'))
    for _k in _K6[1:]:
        assert all(_V[_k]['corridas'][m] == 30
                   for m in ('regla_bon', 'ga', 'ga_sembrado')), _k
    check('horizontes', '$900$, $1800$ and $3600$~s', 'e6_v2')
    # la calibracion que abre 6.5
    check('el genetico publicado',
          f"against the ${_C6['publicado']['GA']:.1f}\\%$ $\\RE$\npublished",
          'e6_v2')
    check('ESABC publicado', f"${_C6['publicado']['ESABC']:.1f}\\%$ of ESABC",
          'e6_v2')
    _gaf, _ga100 = _C6['re']['final']['ga'], _C6['re']['100']['ga']
    _hueco = _gaf - _C6['publicado']['ESABC']
    assert _C6['horizonte'] == 900.0
    check('el genetico a 900 s en las clasicas',
          f"it reaches ${_gaf:.1f}\\%$ in ${_C6['horizonte']:.0f}$~s per instance",
          'e6_v2')
    check('distancia a ESABC', f"still ${_hueco:.1f}$ points above", 'e6_v2')
    check('lo que mejora de 100 a 900 s',
          f"from ${_ga100:.1f}\\%$ to ${_gaf:.1f}\\%$", 'e6_v2')
    assert _gaf < _C6['publicado']['GA'], 'la reimplementacion no es fiel'
    # "levels off": lo que gana en los ultimos 800 s es menos de lo que le
    # falta para ESABC
    assert _ga100 - _gaf < _hueco, (
        'el genetico no se estanca antes de ESABC: reescribir 6.5')
    # lo que cuesta una muestra de la regla en decodificaciones del genetico
    _rat = {k: _V[k]['ms_schedule']['regla_bon'] / _V[k]['ms_schedule']['ga']
            for k in _K6}
    check('coste de una muestra de la regla',
          f"${min(_rat.values()):.0f}$ to ${max(_rat.values()):.0f}$ decodings",
          'e6_v2')
    assert _rat['15_15'] < _rat['30_15'] < _rat['50_15'], 'el coste no crece con el tamano'
    # un segundo en las clasicas
    _r1 = _C6['re']['1']
    check('un segundo en las clasicas',
          f"${_r1['regla_bon']:.1f}\\%$, against ${_r1['ga_sembrado']:.1f}\\%$ "
          f"for the seeded genetic algorithm and ${_r1['ga']:.1f}\\%$", 'e6_v2')
    assert _r1['regla_bon'] < _r1['ga_sembrado'] < _r1['ga']
    # el genetico iguala la pasada unica
    _gp = [_V[k]['cruce']['ga_pasada'] for k in _K6]
    check('el genetico iguala la pasada',
          f"after ${min(_gp):.0f}$ to ${max(_gp):.0f}$~s per instance", 'e6_v2')

    def _redondea(x):
        return f"{round(x):.0f}" if x < 100 else f"{round(x, -1):.0f}"

    # el genetico cruza al mejor-de-N, cada vez mas tarde
    _cg = [_V[k]['cruce']['ga_bon'] for k in _K6]
    assert all(c is not None for c in _cg) and _cg == sorted(_cg), _cg
    check('cruces del genetico con el mejor-de-N',
          f"from about ${_redondea(_cg[0])}$~s on the classical instances, "
          f"${_redondea(_cg[1])}$~s on $15{{\\times}}15$, ${_redondea(_cg[2])}$~s "
          f"on $30{{\\times}}15$ and ${_redondea(_cg[3])}$~s on", 'e6_v2')
    # al final, los dos geneticos por debajo del mejor-de-N en media
    for _k in _K6:
        _f = _V[_k]['re']['final']
        assert _f['ga'] < _f['regla_bon'] and _f['ga_sembrado'] < _f['regla_bon'], _k
    _fs = {k: _V[k]['final']['sembrado_bon'] for k in _K6}
    check('sembrado contra mejor-de-N, clasicas',
          f"better on {_fs['clasicas']['a_mejor']} of {_fs['clasicas']['n']}, "
          f"$p={_fs['clasicas']['p']:.3f}$", 'e6_v2')
    check('sembrado contra mejor-de-N, 50x15',
          f"{_fs['50_15']['a_mejor']} of\n10, $p={_fs['50_15']['p']:.3f}$", 'e6_v2')
    assert _fs['15_15']['p'] > 0.05 and _fs['30_15']['p'] > 0.05
    assert _fs['clasicas']['p'] < 0.05 and _fs['50_15']['p'] < 0.05
    _g50 = _V['50_15']['final']['ga_bon']
    assert _g50['p'] < 0.05 and _g50['media_a'] < _g50['media_b']
    check('genetico contra mejor-de-N, 50x15',
          f"significantly better\n($p={_g50['p']:.3f}$)", 'e6_v2')
    # la semilla en el tiempo
    for _k in _K6:
        assert _V[_k]['semilla']['1']['p'] < 0.05, _k
        for _t, _c in _V[_k]['semilla'].items():
            if _t == 'final' or float(_t) >= 100:
                assert _c['p'] > 0.05, (_k, _t)
    assert _V['50_15']['semilla']['30']['p'] < 0.05
    check('la ventaja de la semilla dura hasta', 'for up to $30$~s on', 'e6_v2')
    check('la semilla deja de notarse', 'from $100$~s per instance on', 'e6_v2')
    _cs = {k: _V[k]['cruce']['sembrado_bon'] for k in _K6}
    for _k in ('clasicas', '15_15', '50_15'):
        assert _cs[_k] < _V[_k]['cruce']['ga_bon'], _k
    assert _cs['30_15'] > _V['30_15']['cruce']['ga_bon']
    check('cruces del sembrado',
          f"at about ${_redondea(_cs['clasicas'])}$~s on the classical\ninstances, "
          f"${_redondea(_cs['15_15'])}$~s on $15{{\\times}}15$ and "
          f"${_redondea(_cs['50_15'])}$~s on $50{{\\times}}15$", 'e6_v2')
    check('el sembrado sigue al mejor-de-N en 30x15',
          f"until about ${_redondea(_cs['30_15'])}$~s", 'e6_v2')
    _s42 = _V['semilla_42']
    assert _s42['n'] == 42 and _s42['p'] > 0.05
    check('las 42 al final', f"better on {_s42['a_mejor']} ($p={_s42['p']:.2f}$",
          'e6_v2')
    # la tabla S de la semilla, celda a celda
    for _t in ('1', '3', '10', '30', '100', '300', '1000', 'final'):
        _cel = []
        for _k in _K6:
            _c = _V[_k]['semilla'].get(_t)
            _cel.append('---' if _c is None else f"{_c['a_mejor']} ({_c['p']:.3f})")
        _et = 'End of horizon' if _t == 'final' else _t
        check(f'tabla S de la semilla, {_et}',
              f"{_et} & " + ' & '.join(_cel) + ' \\\\', 'e6_v2')
    # conclusiones (iv)
    check('conclusiones: el cruce en las clasicas y en 50x15',
          f"from about ${_redondea(_cg[0])}$~s per instance on\nthe classical "
          f"instances to about ${_redondea(_cg[3])}$~s on $50{{\\times}}15$",
          'e6_v2')
    check('la figura de 6.5', 'figures/fig_budget.pdf', 'e6_v2')

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
    # 7.5 ya no da las pendientes de cada tramo: dice que el precio de la
    # estrechez sube a lo largo del barrido, y el assert de abajo (_t2 > _t1)
    # es lo que sostiene esa frase
    check('el precio sube a lo largo del barrido',
          'the price of narrowness rises along the sweep', 'lambda_sweep')
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
    # 5.2 ya no cuenta la calibracion (cuatro configuraciones a 2x10^5
    # construcciones): solo la configuracion, que el assert de arriba
    # sigue atando a la ganadora de calibracion.json
    for _f in ('A population of $250$ individuals',
               'tournaments of size $3$', 'with probability $0.9$',
               'probability $0.2$ by swapping'):
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
