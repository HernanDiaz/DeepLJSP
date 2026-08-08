# -*- coding: utf-8 -*-
"""Verificador de numeros del paper DRL (paper/main.tex).

Mismo contrato que paper_gp/verify_numbers.py: cada afirmacion numerica
del texto se recomputa desde los datos primarios y se compara. Ejecutar
desde la raiz del repo:

    python paper/verify_numbers.py

Los RE derivados de schedules se recomputan con el makespan COMPONENTE A
COMPONENTE ([max lowers, max uppers], la Eq. 2 del propio paper); cuando
la convencion lexicografica pre-fix (la de scripts/re_report.py) da otro
valor, se informa del delta.
"""
import glob
import json
import math
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

if not os.path.exists("paper/main.tex"):
    sys.exit("Ejecutar desde la raiz del repo")

TEX = open("paper/main.tex", encoding="utf-8").read()
TEX_PLANO = " ".join(TEX.split())

ok_n, fallo_n, pend_n = 0, 0, 0


def check(desc, esperado, real, tol=0.051):
    """esperado: valor que afirma el texto; real: recomputado."""
    global ok_n, fallo_n
    bien = abs(esperado - real) <= tol
    marca = "OK   " if bien else "FALLO"
    extra = "" if bien else f"  (texto={esperado}, datos={real:.3f})"
    print(f"  {marca} {desc:<58} {real:.2f}{extra}")
    ok_n += bien
    fallo_n += not bien


def check_exacto(desc, cond, detalle=""):
    global ok_n, fallo_n
    marca = "OK   " if cond else "FALLO"
    print(f"  {marca} {desc:<58} {detalle}")
    ok_n += cond
    fallo_n += not cond


def pendiente(desc, motivo):
    global pend_n
    pend_n += 1
    print(f"  PEND  {desc:<58} {motivo}")


def en_tex(literal):
    if " ".join(literal.split()) not in TEX_PLANO:
        print(f"  AVISO el literal no aparece en el tex: {literal[:60]!r}")


# --- mapa instancia -> (TA, LB de literatura) ----------------------------

TA_BASE = {"15_15": 0, "20_15": 10, "20_20": 20, "30_15": 30,
           "30_20": 40, "50_15": 50, "50_20": 60}
LB = {}      # "TA15" -> 1339
MOR_RE = {}  # "TA15" -> 51.3...   (constructive_per_instance, componentwise)
GT_RE = {}
for linea in open("benchmarks/constructive_per_instance.csv",
                  encoding="utf-8").read().splitlines()[1:]:
    c = linea.split(",")
    LB[c[0]] = float(c[2])
    MOR_RE[c[0]] = float(c[3])
    GT_RE[c[0]] = float(c[5])


def ta_de(nombre):
    m = re.search(r"tai(\d+_\d+)_(\d+)", nombre.lower())
    return f"TA{TA_BASE[m.group(1)] + int(m.group(2))}"


# --- makespan desde un schedule guardado ---------------------------------

def makespans(path):
    """(mid componentwise, mid lexicografico) del schedule JSON."""
    lo_max, up_max, lex = 0.0, 0.0, (0.0, 0.0)
    for t in json.load(open(path)):
        e = t["end"]
        lo, up = (e["lower"], e["upper"]) if isinstance(e, dict) else (e, e)
        lo_max, up_max = max(lo_max, lo), max(up_max, up)
        if up > lex[1] or (up == lex[1] and lo > lex[0]):
            lex = (lo, up)
    return (lo_max + up_max) / 2.0, (lex[0] + lex[1]) / 2.0


def bench_por_instancia(tag):
    """{TA: {'mids':[por semilla], 'lex':[...]}} de un benchmark."""
    dirs = sorted(glob.glob(f"outputs/bench_{tag}__*_seed*"))
    if not dirs:
        return None
    out = {}
    for d in dirs:
        for p in glob.glob(f"{d}/plots/test/*_schedule.json"):
            ta = ta_de(os.path.basename(p))
            mid, lexm = makespans(p)
            out.setdefault(ta, {"mids": [], "lex": []})
            out[ta]["mids"].append(mid)
            out[ta]["lex"].append(lexm)
    return out


def re_pct(mid, ta):
    return (mid - LB[ta]) / LB[ta] * 100


# =========================================================================
print("== seccion 5.4: baselines (all_baselines.csv, componentwise) ==")
ab = {}
for linea in open("benchmarks/all_baselines.csv",
                  encoding="utf-8").read().splitlines()[1:]:
    c = linea.split(",")
    ab[c[0]] = float(c[8])
en_tex("$29.5\\%$ mean RE")
check("G&T-MWKR sobre las 70 (texto 29.5)", 29.5, ab["G&T-MWKR"])
check("MOR sobre las 70 (texto 45.5)", 45.5, ab["MOR"])
check("G&T-SPT sobre las 70 (texto 70.6)", 70.6, ab["G&T-SPT"])
check("EST sobre las 70 (texto 42.3)", 42.3, ab["EST"])
check_exacto("EST es la mejor regla suelta sobre las 70",
             ab["EST"] < min(ab["MOR"], ab["MWKR"], ab["SPT"], ab["LPT"]),
             f"EST {ab['EST']:.1f}")

# 5.5 afirma que las cuatro reglas que NO se reportan luego (SPT, LPT,
# MWKR, G&T-SPT) estan dominadas en TODAS las clases por la mas fuerte
# de su familia, que es lo que justifica no arrastrarlas a los resultados
_clases = {}
for _linea in open("benchmarks/all_baselines.csv",
                   encoding="utf-8").read().splitlines()[1:]:
    _c = _linea.split(",")
    if _c[0]:
        _clases[_c[0]] = [float(x) for x in _c[1:8]]
_mejor_por_clase = [min(_clases["MOR"][i], _clases["EST"][i],
                        _clases["G&T-MWKR"][i]) for i in range(7)]
check_exacto("5.5: SPT, LPT, MWKR y G&T-SPT dominadas en las siete clases",
             all(_clases[r][i] > _mejor_por_clase[i]
                 for r in ("SPT", "LPT", "MWKR", "G&T-SPT")
                 for i in range(7)))
check_exacto("5.5: las tres que siguen son MOR, EST y G&T-MWKR",
             all(f"{r} &" in TEX or f"{r} " in TEX
                 for r in ("MOR", "EST", "G\\&T-MWKR")))

# el resumen tiene un limite duro de la revista: 150-250 palabras
# ("Please provide an abstract of 150 to 250 words", guia de JIM). Se
# cuenta sobre el texto renderizado, no sobre las ordenes de LaTeX.
_ab = TEX[TEX.index("\\abstract{") + len("\\abstract{"):
           TEX.index("\\keywords")].strip().rstrip("}")
_ab = _ab.replace("{\\times}", "x").replace("\\%", "%")
_ab = re.sub(r"\\[a-zA-Z]+|[{}$]", " ", _ab).replace("---", " ")
_n_ab = len([w for w in _ab.split() if any(ch.isalnum() for ch in w)])
check_exacto("el resumen cabe en las 150-250 palabras de JIM",
             150 <= _n_ab <= 250, f"{_n_ab} palabras")

# EST en desarrollo es PEOR que MOR: el ~46 del abstract (MOR) sigue siendo
# la mejor regla en la clase de entrenamiento
est_pi = {r.split(",")[0]: float(r.split(",")[3])
          for r in open("benchmarks/est_per_instance.csv",
                        encoding="utf-8").read().splitlines()[1:]}
est_dev = sum(est_pi[f"TA{k}"] for k in range(15, 21)) / 6
check_exacto("en desarrollo MOR < EST (sostiene el ~46 del abstract)",
             est_dev > 46.0, f"EST dev {est_dev:.1f}")

# centinela (el texto ya no lo imprime): greedy gana a MOR, EST y G&T
gre = {}
for r in open("benchmarks/fair_v2_greedy.csv",
              encoding="utf-8").read().splitlines()[1:]:
    c = r.split(",")
    gre.setdefault(ta_de(c[0]), []).append(float(c[3]))
gre = {ta: sum(v) / len(v) for ta, v in gre.items()}
for nombre, otro in [("MOR", MOR_RE), ("G&T", GT_RE), ("EST", est_pi)]:
    gana = sum(gre[ta] < otro[ta] for ta in gre)
    check_exacto(f"greedy gana a {nombre} en las 70", gana == 70,
                 f"{gana}/70")

DEV = [f"TA{k}" for k in range(15, 21)]
mor_dev = sum(MOR_RE[t] for t in DEV) / len(DEV)
check("MOR medio en desarrollo (abstract ~46)", 46.0, mor_dev, tol=0.55)

# =========================================================================
print("\n== tab:insize: recomputo desde schedules (componentwise) ==")
# Cada presupuesto agrega su brazo original (semillas 2-4) y su
# extension (5-11): diez tiradas identicas salvo la semilla.
TAB_INSIZE = {
    ("v2-full", "v2-full-100ep-ext"):
        {"TA15": (30.2, 21.9), "TA16": (26.3, 19.7), "TA17": (26.8, 18.1),
         "TA18": (26.7, 18.4), "TA19": (28.7, 21.5), "TA20": (25.8, 18.5)},
    ("v2-full-300ep", "v2-full-300ep-ext"):
        {"TA15": (19.0, 16.3), "TA16": (16.3, 14.3), "TA17": (16.6, 13.3),
         "TA18": (18.5, 16.2), "TA19": (17.2, 13.3), "TA20": (16.6, 14.9)},
    ("v2-full-1000ep", "v2-full-1000ep-ext-c"):
        {"TA15": (14.9, 12.1), "TA16": (13.2, 11.8), "TA17": (12.9, 10.4),
         "TA18": (16.3, 14.6), "TA19": (12.8, 11.1), "TA20": (12.8, 10.5)},
}
MEDIAS = {"v2-full": (27.4, 4.69), "v2-full-300ep": (17.4, 1.30),
          "v2-full-1000ep": (13.8, 0.47)}
DEV6 = [f"TA{k}" for k in range(15, 21)]
delta_max = 0.0
_medias_presupuesto = {}
for tags, celdas in TAB_INSIZE.items():
    por_semilla = {}
    for tag in tags:
        for d in sorted(glob.glob(f"outputs/bench_{tag}__*_seed*")):
            s = d.split("_seed")[-1]
            for p in glob.glob(f"{d}/plots/test/*_schedule.json"):
                ta = ta_de(os.path.basename(p))
                por_semilla.setdefault(ta, {})[s] = makespans(p)
    if not por_semilla:
        pendiente(f"benchmark {tags[0]}", "sin directorios en outputs/")
        continue
    semillas = sorted(por_semilla["TA15"])
    check_exacto(f"{tags[0]}: diez semillas", len(semillas) == 10,
                 f"{len(semillas)} semillas")
    res_mean, res_best = {}, {}
    for ta in DEV6:
        mids = [por_semilla[ta][s][0] for s in semillas]
        lex = [por_semilla[ta][s][1] for s in semillas]
        res_mean[ta] = re_pct(sum(mids) / len(mids), ta)
        res_best[ta] = re_pct(min(mids), ta)
        delta_max = max(delta_max,
                        abs(res_mean[ta] - re_pct(sum(lex) / len(lex), ta)))
    for ta, (m_tex, b_tex) in celdas.items():
        check(f"{tags[0]} {ta} media", m_tex, res_mean[ta])
        check(f"{tags[0]} {ta} mejor", b_tex, res_best[ta])
    m_tex, sd_tex = MEDIAS[tags[0]]
    check(f"{tags[0]}: media de la fila (texto {m_tex})", m_tex,
          sum(res_mean.values()) / 6)
    _medias_presupuesto[tags[0]] = sum(res_mean.values()) / 6
    import statistics as _si
    por_sem = [_si.mean(re_pct(por_semilla[ta][s][0], ta) for ta in DEV6)
               for s in semillas]
    check(f"{tags[0]}: sd entre las diez semillas (texto {sd_tex})",
          sd_tex, _si.stdev(por_sem), tol=0.006)
    # los extremos por semilla ya no se imprimen en el texto: son la
    # banda mejor-peor de fig:scaling, cuyos valores viven en
    # make_figures.fig_scaling
    if tags[0] == "v2-full-1000ep":
        check("fig:scaling: peor semilla a 1000 eps (banda 14.6)", 14.6,
              max(por_sem), tol=0.051)
        check("fig:scaling: mejor semilla a 1000 eps (banda 13.1)", 13.1,
              min(por_sem), tol=0.051)
        tres = [_si.mean(re_pct(por_semilla[ta][s][0], ta) for ta in DEV6)
                for s in ("2", "3", "4")]
        check("7.4: las tres de las ablaciones (texto 13.44)", 13.44,
              _si.mean(tres))
        check("7.4: las diez del brazo principal (texto 13.82)", 13.82,
              _si.mean(por_sem))
    if tags[0] == "v2-full":
        check("fig:scaling: banda a 100 eps, minimo (21.3)", 21.3,
              min(por_sem), tol=0.051)
        check("fig:scaling: banda a 100 eps, maximo (36.2)", 36.2,
              max(por_sem), tol=0.051)
print(f"  nota: delta maximo lex vs componentwise = {delta_max:.3f} puntos")

# fila MOR de la tabla (viene de constructive_per_instance)
FILA_MOR = {"TA15": 51.3, "TA16": 35.8, "TA17": 50.1,
            "TA18": 54.2, "TA19": 43.2, "TA20": 43.7}
for ta, v in FILA_MOR.items():
    check(f"fila MOR {ta}", v, MOR_RE[ta])

# 6.1(i): el rendimiento decreciente se enuncia como tasa medida, no
# como extrapolacion a un techo. Los dos saltos son de x3 y x3.3 en
# presupuesto, y el texto los llama "por triplicar"
if len(_medias_presupuesto) == 3:
    # las tasas se restan de las medias IMPRESAS, que es lo unico que el
    # lector puede reproducir; sin redondear serian 10.06 y 3.54
    _m = {k: round(v, 1) for k, v in _medias_presupuesto.items()}
    _r1 = _m["v2-full"] - _m["v2-full-300ep"]
    _r2 = _m["v2-full-300ep"] - _m["v2-full-1000ep"]
    check("6.1: primer salto, 10.0 puntos (texto)", 10.0, _r1, tol=0.02)
    check("6.1: segundo salto, 3.6 puntos (texto)", 3.6, _r2, tol=0.02)
    check_exacto("6.1: el retorno decrece", _r2 < _r1,
                 f"{_r1:.1f} -> {_r2:.1f}")
else:
    pendiente("6.1: las dos tasas de retorno", "faltan brazos de presupuesto")

# fig:scaling: sus dos lineas de referencia van sobre TA15-TA20, no
# sobre las 70. G&T da 29.5 en las setenta y 27.9 aqui; usar el de las
# setenta pondria la linea en el sitio equivocado de este eje.
DEV6 = [f"TA{k}" for k in range(15, 21)]
check("fig:scaling: G&T en TA15-TA20 (texto 27.9)", 27.9,
      sum(GT_RE[t] for t in DEV6) / 6)
_pub2 = {}
_t2 = open("scripts/compare_pools_published.py", encoding="utf-8").read()
exec(re.search(r"(FEABC_BEST.*?)(?=\n# |\ndef |\Z)", _t2, re.S).group(1),
     {}, _pub2)
check("fig:scaling: fEABC en TA15-TA20 (texto 9.6)", 9.6,
      sum(_pub2["FEABC_AVG"][14:20]) / 6)

datos1000 = bench_por_instancia("v2-full-1000ep")
if datos1000:
    mejor_media = sum(re_pct(min(d["mids"]), ta)
                      for ta, d in datos1000.items()) / len(datos1000)
    check("mejor semilla a 1000 eps (abstract 12.3)", 12.3, mejor_media)
    # el factor de 6.1 va contra la media de las DIEZ semillas (13.82),
    # no contra la de las tres con que van pareadas las ablaciones. Y la
    # referencia es G&T-MWKR, la mejor constructiva, no MOR
    _gt_dev = sum(GT_RE[t] for t in DEV6) / 6
    factor = _gt_dev / 13.82
    check_exacto("factor ~2.0 frente a G&T-MWKR", 1.95 <= factor <= 2.05,
                 f"{factor:.2f}")
    # la fila de tab:insize: G&T-MWKR instancia a instancia
    TAB_INSIZE_GT = [30.6, 34.0, 17.7, 31.8, 29.3, 24.1]
    for _ta, _v_tex in zip(DEV6, TAB_INSIZE_GT):
        check(f"tab:insize fila G&T-MWKR {_ta} (texto {_v_tex})", _v_tex,
              GT_RE[_ta])
    check("tab:insize fila G&T-MWKR, media (texto 27.9)", 27.9, _gt_dev)
    stds = []
    for ta, d in datos1000.items():
        m = sum(d["mids"]) / len(d["mids"])
        stds.append(math.sqrt(sum((x - m) ** 2 for x in d["mids"])
                              / (len(d["mids"]) - 1)))
    check_exacto("std de makespan por instancia 6-22 unidades",
                 5.5 <= min(stds) and max(stds) <= 22.5,
                 f"rango {min(stds):.0f}-{max(stds):.0f}")

# =========================================================================
print("\n== tab:insize-attn ==")
TAB_ATTN = {"v2-attn-300ep": (17.6, 16.3), "v2-attn-1000ep": (15.2, 14.0)}
attn_media = {}
for tag, (m_tex, b_tex) in TAB_ATTN.items():
    datos = bench_por_instancia(tag)
    if datos is None:
        pendiente(f"benchmark {tag}", "sin directorios en outputs/")
        continue
    medias = {ta: re_pct(sum(d["mids"]) / len(d["mids"]), ta)
              for ta, d in datos.items()}
    bests = {ta: re_pct(min(d["mids"]), ta) for ta, d in datos.items()}
    attn_media[tag] = sum(medias.values()) / len(medias)
    check(f"{tag}: media (texto {m_tex})", m_tex, attn_media[tag])
    check(f"{tag}: mejor (texto {b_tex})", b_tex,
          sum(bests.values()) / len(bests))

# el makespan medio ya no se imprime (7.3 lo cuenta en puntos de RE y
# con test pareado), pero se sigue comprobando como centinela del dato
for tag_a, tag_b, delta_tex in [("v2-full-300ep", "v2-attn-300ep", 0.9),
                                ("v2-full-1000ep", "v2-attn-1000ep", 1.5)]:
    da, db = bench_por_instancia(tag_a), bench_por_instancia(tag_b)
    if da and db:
        base = sum(sum(d["mids"]) for d in da.values())
        attn = sum(sum(d["mids"]) for d in db.values())
        check(f"centinela: makespan medio {tag_b} vs base (+{delta_tex}%)",
              delta_tex, (attn / base - 1) * 100, tol=0.1)

# 7.3, la comparacion pareada que SI imprime el texto: 18 pares
# (instancia, semilla), delta en puntos de RE, cuentas y Wilcoxon
from scipy.stats import wilcoxon as _wilc  # noqa: E402

for _tb, _d_tex, _pares_tex, _inst_tex, _p_tex in [
        ("300ep", 1.03, 12, 5, 0.067), ("1000ep", 1.76, 16, 6, None)]:
    _da = bench_por_instancia("v2-full-" + _tb)
    _db = bench_por_instancia("v2-attn-" + _tb)
    if not (_da and _db):
        pendiente(f"7.3 pareado {_tb}", "sin directorios en outputs/")
        continue
    _dif = [re_pct(y, ta) - re_pct(x, ta) for ta in sorted(_da)
            for x, y in zip(_da[ta]["mids"], _db[ta]["mids"])]
    check_exacto(f"7.3 {_tb}: 18 pares (instancia, semilla)",
                 len(_dif) == 18, str(len(_dif)))
    check(f"7.3 {_tb}: la atencion pierde {_d_tex} puntos de RE",
          _d_tex, sum(_dif) / len(_dif), tol=0.011)
    check_exacto(f"7.3 {_tb}: peor en {_pares_tex} de los 18 pares",
                 sum(1 for d in _dif if d > 0) == _pares_tex,
                 str(sum(1 for d in _dif if d > 0)))
    _pi = sum(1 for ta in _da
              if sum(re_pct(v, ta) for v in _db[ta]["mids"])
              > sum(re_pct(v, ta) for v in _da[ta]["mids"]))
    check_exacto(f"7.3 {_tb}: peor en {_inst_tex} de las 6 instancias",
                 _pi == _inst_tex, str(_pi))
    _p = _wilc(_dif).pvalue
    if _p_tex is None:
        check_exacto(f"7.3 {_tb}: p<0.001", _p < 0.001, f"p={_p:.5f}")
    else:
        check(f"7.3 {_tb}: Wilcoxon p={_p_tex}", _p_tex, _p, tol=0.0011)

# El sobrecoste por episodio que cita 7.3. Se mide a 300 episodios y NO
# a 1000: alli el brazo base tiene un 1.87x de dispersion entre sus tres
# semillas (3.97 / 6.30 / 7.41 s por episodio, misma configuracion), o
# sea contencion de maquina, y dividir por esa media inflada rebajaba el
# factor a 1.7. A 300 episodios los dos brazos son consistentes.
_seg = {}
for _t in ("v2-full-300ep", "v2-attn-300ep",
           "v2-full-1000ep", "v2-attn-1000ep"):
    _f = glob.glob(f"benchmarks/{_t}__*.json")
    if _f:
        _r = json.load(open(_f[0], encoding="utf-8"))
        _seg[_t] = sorted(_s["wall_time_s"] / _r["config"]["episodes"]
                          for _s in _r["seeds"].values())
if len(_seg) == 4:
    for _t in ("v2-full-300ep", "v2-attn-300ep"):
        check_exacto(f"7.3: {_t} es consistente entre semillas (<4%)",
                     _seg[_t][-1] / _seg[_t][0] < 1.04,
                     " ".join(f"{x:.2f}" for x in _seg[_t]))
    check("7.3: 2.2x el reloj por episodio (300 ep)", 2.2,
          (sum(_seg["v2-attn-300ep"]) / 3) / (sum(_seg["v2-full-300ep"]) / 3),
          tol=0.051)
    check_exacto("7.3: por que no se mide a 1000 ep (base dispersa 1.87x)",
                 _seg["v2-full-1000ep"][-1] / _seg["v2-full-1000ep"][0] > 1.5,
                 " ".join(f"{x:.2f}" for x in _seg["v2-full-1000ep"]))
    # y que la variante de atencion si es estable a los dos presupuestos,
    # lo que confirma que el disperso es el base y no la medida
    check_exacto("7.3: la variante de atencion cuesta lo mismo a 300 y 1000",
                 abs(sum(_seg["v2-attn-300ep"]) / sum(_seg["v2-attn-1000ep"])
                     - 1) < 0.1,
                 f"{sum(_seg['v2-attn-300ep'])/3:.2f} vs "
                 f"{sum(_seg['v2-attn-1000ep'])/3:.2f} s/ep")

# =========================================================================
print("\n== especialista vs multi-tamano ==")
# bo64, media de 3 semillas, la MISMA agregacion en ambos lados
_multi = {}
for r in __import__("csv").DictReader(
        open("benchmarks/eval_multisize_bo64.csv", encoding="utf-8")):
    brazo = "12k" if "-12k" in r["checkpoint"] else "3000"
    _multi.setdefault((brazo, ta_de(r["instance"])), []).append(
        float(r["re_comp"]))
_multi = {k: sum(v) / len(v) for k, v in _multi.items()}
_espec = {}
for r in __import__("csv").DictReader(
        open("benchmarks/eval_crosssize_bo64.csv", encoding="utf-8")):
    _espec.setdefault(ta_de(r["instance"]), []).append(float(r["re_comp"]))
_espec = {ta: sum(v) / len(v) for ta, v in _espec.items()}
CINCO = ["TA5", "TA25", "TA31", "TA41", "TA61"]
for ta, v_tex in [("TA5", 15.9), ("TA25", 20.0), ("TA41", 30.6)]:
    check(f"multi-3000 {ta} (texto {v_tex})", v_tex, _multi[("3000", ta)])
for ta, v_tex in [("TA5", 9.6), ("TA25", 19.4), ("TA41", 28.3),
                  ("TA61", 15.8)]:
    check(f"multi-12k {ta} (texto {v_tex})", v_tex, _multi[("12k", ta)])
for ta, v_tex in [("TA5", 10.5), ("TA25", 15.0), ("TA31", 15.8),
                  ("TA41", 25.9), ("TA61", 16.8)]:
    check(f"especialista {ta} (texto {v_tex})", v_tex, _espec[ta])
gana3000 = sum(_espec[ta] < _multi[("3000", ta)] for ta in CINCO)
check_exacto("presupuesto total igualado: especialista 5/5",
             gana3000 == 5, f"{gana3000}/5")
gana12k = sum(_espec[ta] < _multi[("12k", ta)] for ta in CINCO)
check_exacto("triple presupuesto: el multi recupera 2 de 5",
             gana12k == 3, f"especialista gana {gana12k}/5")

# =========================================================================
print("\n== presupuesto de inferencia y posicionamiento ==")
filas = open("benchmarks/fair_v2_greedy.csv",
             encoding="utf-8").read().splitlines()[1:]
vals = [float(l.split(",")[3]) for l in filas]
check("politica greedy sobre las 70 (texto 19.4)", 19.4,
      sum(vals) / len(vals))
_bo = {}
for r in __import__("csv").DictReader(
        open("benchmarks/eval_fair_bo1024.csv", encoding="utf-8")):
    _bo.setdefault(ta_de(r["instance"]), []).append(float(r["re_comp"]))
_bo = {ta: min(v) for ta, v in _bo.items()}
check_exacto("bo1024: 70 instancias, 3 checkpoints", len(_bo) == 70,
             f"{len(_bo)}")
check("bo1024 media sobre las 70 (texto 13.0)", 13.0,
      sum(_bo.values()) / 70)
gana_bo = {n: sum(_bo[ta] < d[ta] for ta in _bo)
           for n, d in [("MOR", MOR_RE), ("G&T", GT_RE), ("EST", est_pi)]}
check_exacto("centinela: bo1024 gana a MOR, G&T y EST en las 70",
             all(v == 70 for v in gana_bo.values()), str(gana_bo))
_bo_clases = [sum(_bo[f"TA{i * 10 + j + 1}"] for j in range(10)) / 10
              for i in range(7)]
TAB70_BO = [8.8, 11.2, 12.9, 15.0, 19.6, 10.4, 13.4]
for c, (v_tex, v_dat) in enumerate(zip(TAB70_BO, _bo_clases)):
    check(f"tab:seventy bo1024 clase {c + 1} (texto {v_tex})", v_tex,
          v_dat)
_gre_clases = [sum(gre[f"TA{i * 10 + j + 1}"] for j in range(10)) / 10
               for i in range(7)]
TAB70_GREEDY = [16.9, 18.3, 18.5, 21.2, 26.1, 15.8, 18.8]
for c, (v_tex, v_dat) in enumerate(zip(TAB70_GREEDY, _gre_clases)):
    check(f"tab:seventy greedy clase {c + 1} (texto {v_tex})", v_tex,
          v_dat)
# filas MOR y G&T de tab:seventy, por clase, desde el mismo CSV
TAB70_MOR = [41.4, 46.7, 47.3, 44.1, 58.8, 34.1, 45.9]
TAB70_GT = [26.7, 29.0, 30.9, 33.6, 36.8, 23.9, 25.5]
for nombre, tab, d in (("MOR", TAB70_MOR, MOR_RE),
                       ("G&T", TAB70_GT, GT_RE)):
    for c, v_tex in enumerate(tab):
        v_dat = sum(d[f"TA{c * 10 + j + 1}"] for j in range(10)) / 10
        check(f"tab:seventy {nombre} clase {c + 1} (texto {v_tex})",
              v_tex, v_dat)
# distancias al fEABC: tras definirse feabc_clases, mas abajo

# los publicados por instancia del suplemento (compare_pools_published)
_pub = {}
_t = open("scripts/compare_pools_published.py", encoding="utf-8").read()
exec(re.search(r"(FEABC_BEST.*?)(?=\n# |\ndef |\Z)", _t, re.S).group(1),
     {}, _pub)
feabc_clases = [sum(_pub["FEABC_AVG"][i * 10:(i + 1) * 10]) / 10
                for i in range(7)]
ts_clases = [sum(_pub["TS_AVG"][i * 10:(i + 1) * 10]) / 10
             for i in range(7)]
check_exacto("intro: fEABC ~6-16% por clase (solo publicado)",
             5.5 <= min(feabc_clases) <= 6.0
             and 15.5 <= max(feabc_clases) <= 16.5,
             f"fEABC {min(feabc_clases):.1f} .. {max(feabc_clases):.1f}")
check("posicionamiento: fEABC medio (texto 9.4)", 9.4,
      sum(_pub["FEABC_AVG"]) / 70)
# el lector solo puede computar las distancias desde las celdas
# impresas, asi que el texto cita ese redondeo
_dist = [round(b, 1) - round(f, 1)
         for b, f in zip(_bo_clases, feabc_clases)]
check("centinela: distancia minima al fEABC (2.5)", 2.5, min(_dist))
check("centinela: distancia maxima al fEABC (5.2)", 5.2, max(_dist))

# =========================================================================
print("\n== coste computacional ==")
d = json.load(open(sorted(glob.glob(
    "benchmarks/v2-full-1000ep__*.json"))[-1], encoding="utf-8"))
minutos = [s["wall_time_s"] / 60 for s in d["seeds"].values()]
media_min = sum(minutos) / len(minutos)
check_exacto("centinela: 66-123 min por semilla",
             round(min(minutos)) == 66 and round(max(minutos)) == 123,
             f"semillas: {', '.join(f'{m:.0f}' for m in minutos)} min "
             f"(media {media_min:.0f})")

# =========================================================================
print("\n== afirmaciones cerradas ==")
check("0.99^300 ~ 0.05 (atenuacion del retorno)", 0.05, 0.99 ** 300,
      tol=0.002)
quick = set(re.findall(r"idea-(\w+)-quick", " ".join(
    os.listdir("benchmarks"))))
full = set(re.findall(r"idea-(\w+)-full", " ".join(os.listdir("benchmarks"))))
rechazadas = quick - full
check_exacto("trece modificaciones rechazadas (idea-* sin full)",
             len(rechazadas) == 13, f"{len(rechazadas)} rechazadas")

# 7.4 nombra dos de esas modificaciones con su cifra. La fuente es el
# registro de la epoca, no la memoria: si alguien lo corrige, salta aqui
if not os.path.exists("RESEARCH_IDEAS.md"):
    pendiente("las dos ideas de 7.4", "sin RESEARCH_IDEAS.md")
else:
    _log = open("RESEARCH_IDEAS.md", encoding="utf-8").read()
    for _id, _v_tex, _que in [("idea-11", 9.11, "features anexadas"),
                              ("idea-12", 112.65, "normalizacion")]:
        _m = re.search(re.escape(_id) + r".*?\*\*\+([\d.]+)%\*\*", _log)
        check(f"7.4: {_id} ({_que}) en el registro", _v_tex,
              float(_m.group(1)) if _m else -1, tol=0.006)
    check_exacto("7.4: el texto cita 9.1 y 112.7",
                 "$9.1\\%$" in TEX and "$112.7\\%$" in TEX)

try:
    import torch

    def _cuenta(o):
        if hasattr(o, "numel"):
            return o.numel()
        if isinstance(o, dict):
            return sum(_cuenta(v) for v in o.values())
        return 0

    sd = torch.load(glob.glob("benchmarks/v2-multisize_seed2_model.pt")[0],
                    map_location="cpu", weights_only=True)
    n = _cuenta(sd["network"])  # solo la red; el checkpoint guarda tambien Adam
    check_exacto("~1.2e5 parametros (red sola)", 1.0e5 <= n <= 1.4e5,
                 f"{n:,}")
except Exception as e:
    pendiente("~1.2e5 parametros", f"no medible aqui ({type(e).__name__})")

# 4.4: lo que cuesta la atencion. Se instancian las dos redes en vez de
# creer al texto: un bloque ~1.3e5, y B=2 multiplica por 3.2 la red base
try:
    import sys as _sys

    _sys.path.insert(0, ".")
    from jobshop_rl.agents_v2.networks import (AttentionBlock,  # noqa: E402
                                               PolicyValueNetV2)

    def _np(mod):
        return sum(p.numel() for p in mod.parameters())

    _base, _b2 = _np(PolicyValueNetV2()), _np(PolicyValueNetV2(
        num_attention_layers=2))
    check("4.4: un bloque de atencion, ~1.3e5 (texto)", 1.3e5,
          _np(AttentionBlock(128, 4)), tol=0.06e5)
    check("4.4: la variante B=2, ~3.9e5 (texto)", 3.9e5, _b2, tol=0.06e5)
    check("4.4 y 7.3: el factor 3.2 en parametros", 3.2, _b2 / _base,
          tol=0.06)

    # tab:layers: cada celda se recomputa del modulo real, no del texto
    _red = PolicyValueNetV2()
    TAB_LAYERS = [("op_encoder", "16\\to128\\to128", 18944),
                  ("context", "268\\to128\\to128", 51200),
                  ("policy_head", "256\\to128\\to1", 33281),
                  ("value_head", "128\\to128\\to1", 16897)]
    _suma = 0
    for _attr, _forma, _n_tex in TAB_LAYERS:
        _n = _np(getattr(_red, _attr))
        _suma += _n
        check_exacto(f"tab:layers {_attr}: {_n_tex} parametros",
                     _n == _n_tex, f"{_n:,}")
        check_exacto(f"tab:layers {_attr}: forma {_forma}",
                     f"${_forma}$" in TEX)
    # que la suma de los cuatro bloques SEA la red entera es la prueba de
    # que el pooling (y el softmax) no aportan parametros, como dice la
    # tabla con su guion
    check_exacto("tab:layers: la base suma 120.322", _suma == _base == 120322,
                 f"{_suma:,} / {_base:,}")
    check_exacto("tab:layers: el pooling no tiene parametros",
                 _base - _suma == 0)
    check_exacto("tab:layers: el bloque de atencion, 132.480",
                 _np(AttentionBlock(128, 4)) == 132480,
                 f"{_np(AttentionBlock(128, 4)):,}")
    # y la forma interna que 4.4 afirma: 4 cabezas de 32, FF 128->256->128
    _blk = AttentionBlock(128, 4)
    check_exacto("4.4: 4 cabezas de dimension 32",
                 _blk.attn.num_heads == 4 and _blk.attn.head_dim == 32,
                 f"{_blk.attn.num_heads}x{_blk.attn.head_dim}")
    check_exacto("4.4: feed-forward 128->256->128",
                 [_l.out_features for _l in _blk.ff
                  if hasattr(_l, "out_features")] == [256, 128])
    check_exacto("4.4: sin dropout en la atencion",
                 float(getattr(_blk.attn, "dropout", 0.0)) == 0.0)
    # 4.3: LayerNorm y ReLU entre las dos capas, salida lineal
    import torch.nn as _nn
    _tipos = [type(m).__name__ for m in _red.op_encoder]
    check_exacto("4.3: encoder = Linear, LayerNorm, ReLU, Linear",
                 _tipos == ["Linear", "LayerNorm", "ReLU", "Linear"],
                 str(_tipos))
    check_exacto("4.3: sesgos inicializados a cero",
                 all(float(m.bias.abs().sum()) == 0.0
                     for m in _red.modules() if isinstance(m, _nn.Linear)))
    # el cableado que afirma la Eq. de puntuacion: la politica lee
    # [phi_i; g] (256) y el valor lee g solo (128)
    check_exacto("4.3: la politica lee [phi_i; g], el valor solo g",
                 _red.policy_head[0].in_features == 256
                 and _red.value_head[0].in_features == 128,
                 f"{_red.policy_head[0].in_features} / "
                 f"{_red.value_head[0].in_features}")
    # y donde va la atencion: ENTRE el encoder y el pooling, que sigue
    # ahi. 7.3 llego a decir que la sustituia; que no vuelva a pasar
    _fw = __import__("inspect").getsource(PolicyValueNetV2.forward)
    check_exacto("4.4 y 7.3: la atencion va antes del pooling, que sigue",
                 _fw.index("self.attention") < _fw.index("mean_pool")
                 < _fw.index("max_pool") and "self.attention" in _fw)
    check_exacto("4.4: la red base no lleva bloques de atencion",
                 len(_red.attention) == 0
                 and len(PolicyValueNetV2(num_attention_layers=2).attention) == 2)
    # los dos cardinales del encoder que 4.2 y 4.3 afirman, contra el
    # codigo y contra el numero de filas de cada tabla de features
    from jobshop_rl.agents_v2.networks import (  # noqa: E402
        GLOBAL_FEATURE_DIM, OP_FEATURE_DIM)

    check_exacto("4.2: 16 features por operacion", OP_FEATURE_DIM == 16,
                 str(OP_FEATURE_DIM))
    check_exacto("4.2: 12 features globales", GLOBAL_FEATURE_DIM == 12,
                 str(GLOBAL_FEATURE_DIM))
    check_exacto("4.3: el encoder recibe esas 16 y el contexto 2h+12",
                 _red.op_encoder[0].in_features == OP_FEATURE_DIM
                 and _red.context[0].in_features == 2 * 128
                 + GLOBAL_FEATURE_DIM,
                 f"{_red.op_encoder[0].in_features} / "
                 f"{_red.context[0].in_features}")
    # las tablas numeran por rangos (1--2, 9--10...), asi que se suman
    _filas = {}
    for _lab, _tab in (("op", "tab:opfeatures"),
                       ("glob", "tab:globalfeatures")):
        _bloque = TEX.split(_tab)[1].split(r"\end{tabular")[0]
        _n = 0
        for _l in _bloque.splitlines():
            _m = re.match(r"\s*(\d+)(?:--(\d+))?\s*&", _l)
            if _m:
                _n += (int(_m.group(2)) - int(_m.group(1)) + 1
                       if _m.group(2) else 1)
        _filas[_lab] = _n
    check_exacto("4.2: la Tabla 1 enumera las 16", _filas["op"] == 16,
                 str(_filas["op"]))
    check_exacto("4.2: la Tabla 2 enumera las 12", _filas["glob"] == 12,
                 str(_filas["glob"]))
except Exception as e:
    pendiente("estructura de la red", f"no medible aqui ({type(e).__name__})")

# el abstract de Journal of Intelligent Manufacturing va limitado a
# 150-250 palabras; llego a estar en 250 justas
_abs = TEX.split("\\abstract{")[1].split("\\keywords")[0].rsplit("}", 1)[0]
_abs = re.sub(r"\\[a-zA-Z]+", " ", _abs)
_abs = re.sub(r"[{}$\\]", " ", _abs)
_npal = len([x for x in _abs.split() if any(c.isalnum() for c in x)])
check_exacto("abstract dentro de 150-250 palabras (con margen)",
             150 <= _npal <= 245, f"{_npal} palabras")

# bibliografia: que ninguna clave citada falte y que no sobre ninguna
_bib = open("paper/refs.bib", encoding="utf-8").read()
_citadas = set()
for _m in re.finditer(r"\\cite[a-zA-Z]*\*?(?:\[[^\]]*\])*\{([^}]*)\}", TEX):
    _citadas.update(_k.strip() for _k in _m.group(1).split(","))
_citadas.discard("")
_enbib = set(re.findall(r"@\w+\{([^,]+),", _bib))
check_exacto("toda clave citada existe en refs.bib",
             not (_citadas - _enbib), str(sorted(_citadas - _enbib)))
check_exacto("refs.bib no arrastra entradas sin citar",
             not (_enbib - _citadas), str(sorted(_enbib - _citadas)))

try:
    pass
except Exception as e:
    pendiente("coste de la atencion", f"no medible aqui ({type(e).__name__})")

# tab:environment: las versiones se leen de lo que hay instalado, no del
# texto. Si alguien actualiza una libreria y no toca la tabla, salta aqui
print("\n== tab:environment: la maquina y el software ==")
try:
    import importlib
    import platform as _pl

    _tex_env = {"Python": _pl.python_version(),
                "PyTorch": importlib.import_module("torch").__version__,
                "NumPy": importlib.import_module("numpy").__version__,
                "SciPy": importlib.import_module("scipy").__version__,
                "Matplotlib": importlib.import_module("matplotlib").__version__,
                "svglib": importlib.import_module("svglib").__version__}
    for nombre, v in _tex_env.items():
        v = v.split("+")[0]                     # 2.9.1+cu130 -> 2.9.1
        check_exacto(f"tab:environment, {nombre} {v}",
                     f"${v}$" in TEX, v)
    # la construccion CUDA de torch, y que la tabla no invente una GPU
    _cu = importlib.import_module("torch").version.cuda
    check_exacto(f"tab:environment, CUDA {_cu}", f"CUDA ${_cu}$" in TEX,
                 str(_cu))
except Exception as e:
    pendiente("tab:environment", f"no medible aqui ({type(e).__name__})")

# =========================================================================
print("\n== irace ==")
datos_e = bench_por_instancia("v2-elite27-1000ep")
if datos_e:
    media_e = sum(re_pct(sum(d["mids"]) / len(d["mids"]), ta)
                  for ta, d in datos_e.items()) / len(datos_e)
    media_e_lex = sum(re_pct(sum(d["lex"]) / len(d["lex"]), ta)
                      for ta, d in datos_e.items()) / len(datos_e)
    print(f"  info  v2-elite27-1000ep: {media_e:.2f}% comp / "
          f"{media_e_lex:.2f}% lex (texto: 14.5 campana 1 / 14.73 campana 2)")
    check("5.3: el elite de la campana 1 a 1000 eps (texto 14.5)", 14.5,
          media_e_lex, tol=0.051)
    check_exacto("el elite confirmado no mejora el 13.4 por defecto",
                 media_e > 13.4, f"{media_e:.2f} > 13.4")
    # 5.3 ya NO afirma nada sobre el coste de ese brazo: los relojes de
    # las dos corridas no son comparables (el brazo por defecto dispersa
    # 1.87x entre sus propias semillas), y el ~60% que decia el texto
    # ademas invertia el sentido -- el elite corrio mas barato, no mas caro
    check_exacto("5.3 no afirma un sobrecoste del elite (dato no fiable)",
                 "higher training cost" not in TEX)
# confirmacion del elite 22 (campana 2): tuning/confirm_elite22.log
t22 = open("tuning/confirm_elite22.log", encoding="utf-8",
           errors="replace").read()
m = re.search(r"MEDIA\s+([\d.]+)\s+([\d.]+)\s+\+([\d.]+)", t22)
if m:
    check("elite 22: media (texto 14.73)", 14.73, float(m.group(1)))
    check("default en esa confirmacion (texto 13.52)", 13.52,
          float(m.group(2)))
    check("delta (texto +1.21)", 1.21, float(m.group(3)))
    check_exacto("mejor en 2, peor en 4",
                 "mejor en 2 instancias, peor en 4" in t22)
else:
    pendiente("confirmacion del elite 22", "formato inesperado del log")

# presupuestos de las dos campanas de irace
raw = open("tuning/irace_deepsets.log", "rb").read()
try:
    t1 = raw.decode("utf-16")
except Exception:
    t1 = raw.decode("utf-8", errors="replace").replace(chr(0), "")
u1 = [int(x) for x in re.findall(r"experimentsUsed:\s*(\d+)", t1)]
t2 = open("tuning/irace_serious.log", encoding="utf-8",
          errors="replace").read()
u2 = [int(x) for x in re.findall(r"experimentsUsed:\s*(\d+)", t2)]
check_exacto("campana 1: presupuesto 330, 309 usados",
             bool(u1) and max(u1) == 309 and "remainingBudget: 330" in t1,
             f"usados {max(u1) if u1 else '?'}")
check_exacto("campana 2: 295 de 300",
             bool(u2) and max(u2) == 295, f"usados {max(u2) if u2 else '?'}")

# las elites finales de la campana 1, leidas del propio log: el texto
# dice tres, con clip 0.3, 8 epochs, GAE 0.90, minibatch y update-every
# en sus defaults, e insensibles al ancho de la red
_cola1 = t1[t1.rfind("Elite configurations"):]
_el1 = re.findall(r"\n\s*\d+\s+([0-9.e-]+)\s+[0-9.]+\s+([0-9.]+)\s+"
                  r"(\d+)\s+(\d+)\s+(\d+)\s+([0-9.]+)\s+(\d+)",
                  _cola1[:_cola1.find("# Total")])
check_exacto("campana 1: tres elites finales (texto)", len(_el1) == 3,
             f"{len(_el1)} elites")
check_exacto("elites: clip 0.3, 8 epochs, GAE 0.90 (texto)",
             all(c == "0.3" and k == "8" and g == "0.90"
                 for _, c, k, _mb, _u, g, _h in _el1))
check_exacto("elites: minibatch 256 y update-every 4, los defaults",
             all(mb == "256" and u == "4"
                 for _, _c, _k, mb, u, _g, _h in _el1))
check_exacto("elites: anchos 128 y 256 presentes (insensibles)",
             {h for *_, h in _el1} == {"128", "256"})

# =========================================================================
print("\n== 6.2: la transferencia mejora con el presupuesto ==")
# La tabla de nueve instancias desaparecio (6.2 va por clase sobre las
# 70), pero el texto sigue citando TA41 y TA51 a dos presupuestos, y esa
# comparacion vive en los CSV de crosssize.
_cs = {}
for r in __import__("csv").DictReader(
        open("benchmarks/eval_crosssize_bo64.csv", encoding="utf-8")):
    _cs.setdefault(ta_de(r["instance"]), []).append(float(r["re_comp"]))

# la transferencia mejora con el presupuesto (300ep vs 1000ep, medias)
_c300 = {}
for r in __import__("csv").DictReader(
        open("benchmarks/eval_crosssize_bo64_300ep.csv", encoding="utf-8")):
    _c300.setdefault(ta_de(r["instance"]), []).append(float(r["re_comp"]))
_c300 = {ta: sum(v) / len(v) for ta, v in _c300.items()}
check("centinela: TA41 con 300 eps (30.3)", 30.3, _c300["TA41"])
check("centinela: TA51 con 300 eps (22.2)", 22.2, _c300["TA51"])
check_exacto("centinela: mas presupuesto mejora la transferencia",
             _c300["TA41"] > sum(_cs["TA41"]) / 3
             and _c300["TA51"] > sum(_cs["TA51"]) / 3)

# =========================================================================
print("\n== robustez ejecucional (eval_eps_all.csv, x1000) ==")
# El fichero es el nuevo, no eval_eps_policy.csv: aquel sembraba las
# realizaciones con hash() de la cadena, que Python aleatoriza por
# proceso, y su barrido se relanzo a mitad. Este se calculo entero en un
# proceso con semilla crc32 y trae el brazo robusto.
_eps, _anch = {}, {}
for r in __import__("csv").DictReader(
        open("benchmarks/eval_eps_all.csv", encoding="utf-8")):
    m = r["method"]
    if m.startswith("lam1-") and m.endswith("-bo64"):
        g = "lam1-bo64"
    elif m.startswith("lam1-"):
        g = "lam1-greedy"
    elif m.startswith("policy-greedy"):
        g = "policy-greedy"
    elif m.startswith("policy-bo64"):
        g = "policy-bo64"
    else:
        g = m
    _eps.setdefault(g, {}).setdefault(r["instance"], []).append(
        float(r["eps"]) * 1000)
    _anch.setdefault(g, {}).setdefault(r["instance"], []).append(
        float(r["width_rel"]))
_eps = {g: {i: sum(v) / len(v) for i, v in d.items()}
        for g, d in _eps.items()}
_anch = {g: {i: sum(v) / len(v) for i, v in d.items()}
         for g, d in _anch.items()}
# El CSV se regenera por instancias: comprobar contra una tirada a medias
# daria fallos que no son del paper sino del reloj.
_n_eps = len(_eps.get("EST", {}))
if _n_eps < 15:
    pendiente("robustez ejecucional",
              f"eval_eps_policy.csv incompleto ({_n_eps}/15 instancias)")
else:
    for g, v_tex in [("MOR", 7.14), ("GT-MWKR", 6.86), ("EST", 6.35),
                     ("GP", 6.12), ("policy-greedy", 6.18),
                     ("policy-bo64", 6.12), ("lam1-bo64", 5.83)]:
        vals = list(_eps[g].values())
        check(f"eps x1000 {g} (texto {v_tex})", v_tex,
              sum(vals) / len(vals), tol=0.006)
    # los anchos que 7.6 contrasta: el brazo robusto predice mas estrecho
    for g, v_tex in [("policy-bo64", 12.3), ("lam1-bo64", 11.5)]:
        check(f"ancho relativo {g} (texto {v_tex})", v_tex,
              sum(_anch[g].values()) / 15, tol=0.051)
    _ii = sorted(_eps["EST"])
    for g, gana_tex in [("MOR", 14), ("GT-MWKR", 13), ("EST", 9),
                        ("GP", 9), ("lam1-bo64", 6)]:
        gana = sum(_eps[g][i] > _eps["policy-bo64"][i] for i in _ii)
        check_exacto(f"la politica es mas fiel que {g} en {gana_tex}/15",
                     gana == gana_tex, f"{gana}/15")
    try:
        from scipy import stats as _st
        for g, lo, hi, etiq in [("MOR", 0, 1e-3, "p<0.001"),
                                ("GT-MWKR", 0, 1e-3, "p<0.001"),
                                ("EST", 0.27, 0.34, "p=0.30"),
                                ("GP", 0.68, 0.77, "p=0.72"),
                                ("lam1-bo64", 0.20, 0.26, "p=0.23")]:
            d = [_eps[g][i] - _eps["policy-bo64"][i] for i in _ii]
            p = _st.wilcoxon(d)[1]
            check_exacto(f"eps frente a {g} ({etiq})", lo <= p <= hi,
                         f"p={p:.3f}")
        # la afirmacion de fondo: el GP y la politica, indistinguibles
        check_exacto("GP y politica empatados en cabeza",
                     abs(sum(_eps["GP"].values()) / 15
                         - sum(_eps["policy-bo64"].values()) / 15) < 0.15,
                     "diferencia < 0.15")
        # y la nueva: el brazo robusto encabeza, pero sin significacion
        check_exacto("el brazo robusto es el mas fiel de los siete",
                     sum(_eps["lam1-bo64"].values()) / 15
                     == min(sum(v.values()) / 15 for v in _eps.values()),
                     f"{sum(_eps['lam1-bo64'].values()) / 15:.2f}")
    except ImportError:
        pendiente("Wilcoxon de eps", "sin scipy")

print("\n== clasicas (tab:classics) ==")
_clas = {r["inst"]: r for r in __import__("csv").DictReader(
    open("benchmarks/classic12_tuned.csv", encoding="utf-8"))}
_est12 = {r["inst"]: float(r["est_re"]) for r in __import__("csv").DictReader(
    open("benchmarks/classic12_est.csv", encoding="utf-8"))}
_pol12 = {}
for r in __import__("csv").DictReader(
        open("benchmarks/eval_classic12_policy.csv", encoding="utf-8")):
    _pol12.setdefault(r["name"], []).append(float(r["re"]))
# La tupla anterior comprobaba una columna MOR que la tabla no imprime y
# se saltaba la de GP, que si imprime: nunca se verifico. Ahora el orden
# es EXACTAMENTE el de tab:classics, con las dos columnas nuevas.
_gre12 = {}
for r in __import__("csv").DictReader(
        open("benchmarks/eval_classic12_greedy.csv", encoding="utf-8")):
    _gre12.setdefault(r["name"], []).append(float(r["re"]))
check_exacto("greedy en las 12: 3 checkpoints cada una",
             len(_gre12) == 12 and all(len(v) == 3
                                       for v in _gre12.values()),
             f"{len(_gre12)} instancias")

# El brazo GP a los tres presupuestos. OJO: "mejor" es la mejor REGLA
# por su media sobre las 12, no el minimo instancia a instancia, que no
# corresponde a ninguna regla real (el virtual best da 11.97 a una
# pasada y seria una cifra inventada).
_bon = {}
for _f in glob.glob("benchmarks/classic12_arm_bon/*.csv"):
    _r_id = os.path.splitext(os.path.basename(_f))[0]
    _bon[_r_id] = {r["inst"]: (float(r["gp"]), float(r["gp64"]),
                               float(r["gp1024"]))
                   for r in __import__("csv").DictReader(
                       open(_f, encoding="utf-8"))}
if len(_bon) < 30:
    pendiente("brazo GP a 3 presupuestos", f"{len(_bon)}/30 reglas")
    _mejor_regla = {}
else:
    check_exacto("brazo GP a 3 presupuestos: 30 reglas x 12",
                 all(len(v) == 12 for v in _bon.values()), "30 reglas")
    _INST12 = sorted(_bon["gp_tuned_seed1"])
    _mejor_regla = {}
    for _k, _v_med, _v_mej in [(0, 19.0, 15.3), (1, 14.6, 12.8),
                               (2, 12.2, 11.0)]:
        _med = {r: sum(_bon[r][i][_k] for i in _INST12) / 12 for r in _bon}
        _mejor_regla[_k] = min(_med, key=_med.get)
        check(f"6.3: media de las 30, presupuesto {_k} (texto {_v_med})",
              _v_med, sum(_med.values()) / 30, tol=0.051)
        check(f"6.3: mejor regla, presupuesto {_k} (texto {_v_mej})",
              _v_mej, _med[_mejor_regla[_k]], tol=0.051)
        check_exacto(f"6.3: la destacada bate a la media de 30 (pres. {_k})",
                     _med["gp_tuned_seed1"] < sum(_med.values()) / 30,
                     f"{_med['gp_tuned_seed1']:.2f} < "
                     f"{sum(_med.values()) / 30:.2f}")

# G&T, GP mn[bst], Pol.gre mn[bst], GP64 mn[bst], Pol.64 mn[bst], GA, ES.
# Los corchetes de la politica son la mejor semilla de tres; los del GP,
# la mejor regla de treinta. El pie de la tabla lo advierte.
# el 1024 por semilla, que la tabla usa en su tercer grupo (el fichero
# agregado se lee mas abajo, para el numero que cita 6.4)
_ps = {}
for r in __import__("csv").DictReader(
        open("benchmarks/eval_classic12_bo1024_porsemilla.csv",
             encoding="utf-8")):
    _ps.setdefault(r["name"], []).append(float(r["re"]))

# Tabla 2 de Diaz et al. (2023), Natural Computing: columna Best de GA
GA_BEST = {"ABZ7": 6.3, "ABZ8": 11.3, "ABZ9": 13.0, "FT10": 1.8,
           "FT20": 1.5, "La21": 3.2, "La24": 4.1, "La25": 1.9,
           "La27": 4.6, "La29": 11.1, "La38": 6.0, "La40": 5.1}
TAB_CLASSICS = {
    "FT10": (32.2, 17.0, 7.2, 16.7, 16.0, 11.8, 5.2, 8.5, 6.3,
             8.5, 4.2, 6.1, 5.4, 5.2, 1.8),
    "FT20": (40.0, 18.5, 9.4, 8.6, 4.4, 13.3, 5.8, 5.8, 4.4,
             10.3, 5.4, 4.4, 3.6, 4.4, 1.5),
    "La21": (24.1, 15.9, 10.3, 18.3, 15.5, 12.6, 10.0, 12.6, 10.4,
             10.7, 6.8, 10.8, 10.7, 5.0, 3.2),
    "La24": (26.3, 16.1, 10.1, 19.3, 17.1, 11.5, 8.6, 11.9, 10.9,
             9.2, 6.2, 9.1, 8.1, 6.3, 4.1),
    "La25": (16.9, 17.6, 9.6, 17.3, 16.7, 12.3, 8.7, 9.6, 9.2,
             9.3, 5.1, 8.9, 8.2, 5.1, 1.9),
    "La27": (34.8, 18.3, 12.3, 15.0, 13.8, 12.5, 10.7, 11.3, 10.9,
             11.3, 8.2, 9.0, 8.1, 10.2, 4.6),
    "La29": (24.5, 19.9, 12.9, 21.1, 16.2, 15.0, 11.4, 16.6, 14.0,
             12.6, 9.7, 13.3, 12.9, 14.2, 11.1),
    "La38": (27.0, 17.4, 9.2, 17.2, 16.6, 14.3, 9.2, 12.8, 11.7,
             12.0, 7.1, 9.6, 8.3, 9.2, 6.0),
    "La40": (27.9, 16.7, 11.7, 12.0, 9.3, 12.3, 8.8, 9.3, 8.1,
             10.0, 7.1, 7.2, 6.5, 8.7, 5.1),
    "ABZ7": (28.7, 17.6, 13.3, 16.7, 15.9, 14.3, 11.7, 13.4, 12.0,
             12.2, 8.9, 11.9, 11.1, 12.5, 6.3),
    "ABZ8": (36.9, 24.6, 18.1, 21.8, 19.1, 20.9, 17.0, 17.3, 16.9,
             18.6, 15.0, 15.8, 15.6, 18.5, 11.3),
    "ABZ9": (41.8, 29.0, 19.5, 22.6, 19.7, 24.0, 17.9, 19.2, 18.8,
             21.5, 17.4, 17.1, 16.6, 18.0, 13.0),
}
fallos_clas = 0
for inst, fila in TAB_CLASSICS.items():
    c = _clas[inst]

    def _gp(k, i=inst):
        if not _bon:
            return -1, -1
        v = [_bon[r][i][k] for r in _bon]
        return sum(v) / len(v), min(v)

    reales = (float(c["gt"]),
              *_gp(0), sum(_gre12[inst]) / 3, min(_gre12[inst]),
              *_gp(1), sum(_pol12[inst]) / len(_pol12[inst]),
              min(_pol12[inst]),
              *_gp(2), sum(_ps[inst]) / 3, min(_ps[inst]),
              float(c["GA"]), GA_BEST[inst])
    for v_tex, v_dat in zip(fila, reales):
        if abs(v_tex - v_dat) > 0.051:
            print(f"  FALLO celda {inst}: texto={v_tex} datos={v_dat:.2f}")
            fallos_clas += 1
check_exacto("las 180 celdas de tab:classics", fallos_clas == 0,
             f"{fallos_clas} celdas mal")
check("GA: media de sus mejores publicados (texto 5.8)", 5.8,
      sum(GA_BEST.values()) / 12, tol=0.051)
check_exacto("tab:classics ya no imprime ESABC",
             "ESABC" not in TEX[TEX.index("\\label{tab:classics}"):
                                TEX.index("\\end{table}",
                                          TEX.index("\\label{tab:classics}"))])
# 6.3: la dispersion de las 30 reglas evolucionadas. OJO: la media POR
# REGLA sobre las 12, no el minimo instancia a instancia (ese "virtual
# best" da 11.97 y no corresponde a ninguna regla real)
_arm12 = {}
for r in __import__("csv").DictReader(
        open("benchmarks/classic12_arm.csv", encoding="utf-8")):
    _arm12.setdefault(r["rule"], {})[r["inst"]] = float(r["re"])
check_exacto("las 30 reglas GP sobre las 12", len(_arm12) == 30
             and all(len(v) == 12 for v in _arm12.values()),
             f"{len(_arm12)} reglas")
_m_regla = {k: sum(v.values()) / 12 for k, v in _arm12.items()}
check("6.3: mejor regla de las 30 (texto 15.3)", 15.3, min(_m_regla.values()))
check("6.3: peor regla de las 30 (texto 23.3)", 23.3, max(_m_regla.values()))
check("6.3: media de las 30 reglas (texto 19.0)", 19.0,
      sum(_m_regla.values()) / 30)
_pub = _m_regla["gp_tuned_seed1"]
# el analisis de la transferencia de la seleccion GP salio del texto:
# queda como centinela del dato
check_exacto("centinela: la regla publicada es la 13 de 30 en las clasicas",
             sum(1 for v in _m_regla.values() if v < _pub) == 12,
             f"{sum(1 for v in _m_regla.values() if v < _pub)}/30 mejores")
try:
    import statistics as _stt
    _insts12 = sorted(_arm12["gp_tuned_seed1"])
    _sd_gp = sum(_stt.stdev([_arm12[r][i] for r in _arm12])
                 for i in _insts12) / 12
    _sd_pol = sum(_stt.stdev(v) for v in _gre12.values()) / 12
    check("6.3: sd entre reglas GP (texto 4.3)", 4.3, _sd_gp, tol=0.06)
    check("6.3: sd entre semillas DRL (texto 2.2)", 2.2, _sd_pol, tol=0.06)
except Exception as e:
    pendiente("dispersion GP vs DRL", type(e).__name__)

# 6.3 y 6.4 afirman COMO se eligio la regla destacada. Es una afirmacion
# sobre el otro paper, asi que se contrasta contra su fuente, no de
# memoria: la destacada es la mejor de 30 sobre las 70, y la media de las
# 30 es 18.99. Si el companero cambia el protocolo, esto salta.
_GP_TEX = "paper_gp/main.tex"
if not os.path.exists(_GP_TEX):
    pendiente("protocolo de la regla destacada", "sin paper_gp/main.tex")
else:
    _g = open(_GP_TEX, encoding="utf-8").read()
    check_exacto("6.3: la destacada es la de menor RE sobre las 70",
                 "the one with\nthe lowest mean $\\RE$ is the \\emph{featured "
                 "rule}" in _g)
    check_exacto("6.3: las 12 clasicas no intervienen en la eleccion",
                 "the 12 classical instances play no part in any choice" in _g)
    check_exacto("6.4: media de las 30 sobre las 70 es 18.99",
                 "$18.99\\%$ ($\\pm1.33$)" in _g and "$18.99\\%$" in TEX)
    check_exacto("6.4: la destacada sobre las 70 es 17.71",
                 "best rule attains\n$17.71\\%$" in _g)
    # 7.5 compara nuestro brazo robusto con el barrido de lambda del
    # companero. Son afirmaciones sobre SU paper: se leen de su fuente.
    check_exacto("7.5: el companero usa el mismo f_lambda con lambda=1",
                 "$\\lambda$ setting the balance between the two; we take "
                 "$\\lambda = 1$" in _g)
    check_exacto("7.5: su barrido mueve 1.64 puntos de anchura",
                 "$1.64$\nthe full arm covers" in _g)
    check_exacto("7.5: y 0.13 sin los terminales de anchura",
                 "a range of $0.13$ points against the" in _g)
    check_exacto("7.5: su conclusion es que el objetivo actua por la "
                 "representacion",
                 "the first works through the second" in _g)
    # el precio del intercambio en su barrido: 0.5 -> 4 en lambda
    _w_gp = (12.18 - 10.54)
    _re_gp = (23.27 - 19.20)
    check("7.5: el companero paga ~2.5 RE por punto de anchura", 2.5,
          _re_gp / _w_gp, tol=0.06)
    check("7.5: nuestro brazo paga ~2.0 RE por punto de anchura", 2.0,
          (15.38 - 13.44) / (12.85 - 11.90), tol=0.06)

# 6.3: el enfrentamiento a presupuesto igualado sobre las 12
_gp1 = {i: float(_clas[i]["gp"]) for i in _clas}
_gp64 = {i: float(_clas[i]["gp64"]) for i in _clas}
_pg = {i: sum(v) / 3 for i, v in _gre12.items()}
_pb = {i: sum(v) / len(v) for i, v in _pol12.items()}
check("clasicas: GP una pasada (texto 17.9)", 17.9,
      sum(_gp1.values()) / 12)
check("clasicas: politica greedy (texto 17.2)", 17.2,
      sum(_pg.values()) / 12)
check("clasicas: GP con 64 (texto 14.2)", 14.2, sum(_gp64.values()) / 12)
_gp1024c = {i: float(_clas[i]["gp1024"]) for i in _clas}
_p1024 = {}
for r in __import__("csv").DictReader(
        open("benchmarks/eval_classic12_bo1024.csv", encoding="utf-8")):
    _p1024.setdefault(r["name"], []).append(float(r["re"]))
check_exacto("clasicas a 1024: 12 instancias x 3 checkpoints",
             len(_p1024) == 12 and all(len(v) == 3 for v in _p1024.values()),
             f"{len(_p1024)} instancias")
_p1024 = {i: min(v) for i, v in _p1024.items()}   # agrega los tres, como
# el bo1024 de las Taillard: 342 por checkpoint, mejor global al juntar
check("clasicas: GP con 1024 (texto 11.3)", 11.3,
      sum(_gp1024c.values()) / 12)
check("clasicas: politica con 1024 agregada (texto 10.13)", 10.13,
      sum(_p1024.values()) / 12, tol=0.006)

# 6.3: por que los corchetes ordenan al reves que las medias. Son minimos
# por instancia sobre muestras desiguales (30 evoluciones contra 3
# semillas) y dispersiones desiguales; se recomputan ambas y el
# contrafactual de seleccionar la politica sobre 30
import statistics as _stt
_C3, _C30 = 0.8463, 2.0428


def _disp_gp(k):
    _sd, _mn = [], []
    for _i in _INST12:
        _v = [_bon[_r][_i][k] for _r in _bon]
        _sd.append(_stt.stdev(_v))
        _mn.append(min(_v))
    return _stt.mean(_sd), _stt.mean(_mn)


def _disp_pol(fichero, col="re"):
    _d = {}
    for _r in __import__("csv").DictReader(open(fichero, encoding="utf-8")):
        _d.setdefault(_r["name"], []).append(float(_r[col]))
    assert all(len(v) == 3 for v in _d.values())
    return (_stt.mean([_stt.stdev(v) for v in _d.values()]),
            _stt.mean([min(v) for v in _d.values()]),
            _stt.mean([_stt.mean(v) for v in _d.values()]))


if _mejor_regla:
    _POL_F = ["benchmarks/eval_classic12_greedy.csv",
              "benchmarks/eval_classic12_policy.csv",
              "benchmarks/eval_classic12_bo1024_porsemilla.csv"]
    _SD_GP_TEX = [4.3, 2.3, 2.0]
    _SD_POL_TEX = [2.2, 1.4, 0.7]
    _CONTRA_TEX = [12.7, 9.6, 8.8]
    for _k, (_f, _sg_tex, _sp_tex, _c_tex) in enumerate(
            zip(_POL_F, _SD_GP_TEX, _SD_POL_TEX, _CONTRA_TEX)):
        _sd_gp, _min_gp = _disp_gp(_k)
        _sd_pol, _min_pol, _mu_pol = _disp_pol(_f)
        check(f"6.3: sd de las 30 reglas, presupuesto {_k} (texto {_sg_tex})",
              _sg_tex, _sd_gp, tol=0.051)
        check(f"6.3: sd de las 3 semillas, presupuesto {_k} "
              f"(texto {_sp_tex})", _sp_tex, _sd_pol, tol=0.051)
        check(f"6.3: contrafactual c30 sobre la politica (texto {_c_tex})",
              _c_tex, _mu_pol - _C30 * _sd_pol, tol=0.06)
        check_exacto(f"6.3: el corchete de GP es menor, presupuesto {_k}",
                     _min_gp < _min_pol,
                     f"GP {_min_gp:.1f} vs Pol {_min_pol:.1f}")
        check_exacto(f"6.3: la sd de la politica es menor, presupuesto {_k}",
                     _sd_pol < _sd_gp, f"{_sd_pol:.2f} < {_sd_gp:.2f}")

# el 1024 POR SEMILLA: cada checkpoint con sus propias 1024 muestras,
# que es lo comparable con "una regla con 1024" del lado GP
_ps = {}
for r in __import__("csv").DictReader(
        open("benchmarks/eval_classic12_bo1024_porsemilla.csv",
             encoding="utf-8")):
    _ps.setdefault(r["name"], []).append(float(r["re"]))
check_exacto("1024 por semilla: 12 instancias x 3 checkpoints",
             len(_ps) == 12 and all(len(v) == 3 for v in _ps.values()),
             f"{len(_ps)} instancias")
_ps_m = {i: sum(v) / 3 for i, v in _ps.items()}
# 6.3: en que instancias la mejor semilla (bo64) bate a la media del GA
_gana_ga = {i for i, t in TAB_CLASSICS.items() if t[8] < t[13]}
check_exacto("6.3: mejor semilla > media GA en La29, La40, ABZ7, ABZ8",
             _gana_ga == {"La29", "La40", "ABZ7", "ABZ8"},
             str(sorted(_gana_ga)))
check("clasicas: politica con 1024 por semilla (texto 10.27)", 10.27,
      sum(_ps_m.values()) / 12, tol=0.006)
if _mejor_regla:
    _gp1024m = {i: sum(_bon[r][i][2] for r in _bon) / len(_bon)
                for i in _INST12}
    _n1024 = sum(_ps_m[i] < _gp1024m[i] for i in _INST12)
    check_exacto("clasicas a 1024 por semilla: gana 10 de 12",
                 _n1024 == 10, f"{_n1024}/12")
    try:
        from scipy import stats as _st3
        _p1024w = _st3.wilcoxon([_ps_m[i] - _gp1024m[i]
                                 for i in _INST12])[1]
        check_exacto("clasicas a 1024: significativo (texto p=0.009)",
                     0.008 <= _p1024w <= 0.011, f"p={_p1024w:.4f}")
    except ImportError:
        pendiente("Wilcoxon de las clasicas a 1024", "sin scipy")
for etiq, riv, pol_d, n_tex in [("una pasada", _gp1, _pg, 7),
                                ("64 muestras", _gp64, _pb, 9)]:
    n = sum(pol_d[i] < riv[i] for i in _clas)
    check_exacto(f"clasicas, {etiq}: la politica gana {n_tex} de 12",
                 n == n_tex, f"{n}/12")
try:
    from scipy import stats as _st2
    _p1 = _st2.wilcoxon([_pg[i] - _gp1[i] for i in _clas])[1]
    _p2 = _st2.wilcoxon([_pb[i] - _gp64[i] for i in _clas])[1]
    check_exacto("clasicas, una pasada: empate (texto p=0.73)",
                 0.70 <= _p1 <= 0.76, f"p={_p1:.3f}")
    check_exacto("clasicas, 64 muestras: marginal (texto p=0.077)",
                 0.070 <= _p2 <= 0.085, f"p={_p2:.4f}")
except ImportError:
    pendiente("Wilcoxon de las 12 clasicas", "sin scipy")
_medias_pol = [sum(v) / len(v) for v in _pol12.values()]
check("clasicas: politica media (texto 12.4)", 12.4,
      sum(_medias_pol) / 12)
check("clasicas: G&T media (texto 30.1)", 30.1,
      sum(float(c["gt"]) for c in _clas.values()) / 12)
for col, v_tex in [("GA", 9.8), ("ESABC", 5.5)]:
    check(f"clasicas: {col} media (texto {v_tex})", v_tex,
          sum(float(c[col]) for c in _clas.values()) / 12)
gana12 = sum(sum(_pol12[i]) / len(_pol12[i]) <
             min(_est12[i], float(_clas[i]["mor"]), float(_clas[i]["gt"]))
             for i in _clas)
check_exacto("la politica gana a las tres reglas en las 12", gana12 == 12,
             f"{gana12}/12")
mejor = {i: min(_pol12[i]) for i in _pol12}
check_exacto("mejor semilla < GA en La40, ABZ7 y ABZ8",
             all(mejor[i] < float(_clas[i]["GA"])
                 for i in ("La40", "ABZ7", "ABZ8")))

print("\n== importancia de features ==")
# 7.1 cita la medida con CINCO permutaciones por columna; la de una sola
# extraccion se conserva en feature_importance.csv y se comprueba abajo
# como centinela, porque sus magnitudes ya no se imprimen
_rep = {}
for r in __import__("csv").DictReader(
        open("benchmarks/feature_importance_rep.csv", encoding="utf-8")):
    _rep.setdefault(r["feature"], []).append(float(r["delta_puntos"]))
    _base = float(r["re_base"])
check_exacto("importancia: 16 features x 5 permutaciones",
             len(_rep) == 16 and all(len(v) == 5 for v in _rep.values()),
             f"{len(_rep)} features")
check("base greedy del test (texto 18.2)", 18.2, _base)
_med = {f: sum(v) / len(v) for f, v in _rep.items()}
_sd = {f: _stt.stdev(v) for f, v in _rep.items()}
for f, m_tex, s_tex in [("holgura", 56.5, 2.4), ("pos_restante", 33.6, 1.4),
                        ("rem_up", 9.6, 1.0)]:
    check(f"7.1: permutar {f} (texto +{m_tex})", m_tex, _med[f], tol=0.051)
    check(f"7.1: su desviacion sobre las cinco (texto {s_tex})", s_tex,
          _sd[f], tol=0.051)
# el segundo escalon y el suelo que describe el texto
_orden = sorted(_med.items(), key=lambda kv: -kv[1])
check_exacto("7.1: el orden de cabeza es holgura, pos_restante, rem_up",
             [f for f, _ in _orden[:3]] == ["holgura", "pos_restante",
                                            "rem_up"],
             str([f for f, _ in _orden[:3]]))
check_exacto("7.1: segundo escalon de tres, entre 1.8 y 2.9 puntos",
             all(1.75 <= v <= 2.95 for _, v in _orden[3:6]),
             " ".join(f"{f}={v:.2f}" for f, v in _orden[3:6]))
check_exacto("7.1: suelo de diez features entre +0.3 y +1.0",
             len(_orden[6:]) == 10
             and all(0.25 <= v <= 1.0 for _, v in _orden[6:]),
             " ".join(f"{v:.2f}" for _, v in _orden[6:]))
check_exacto("7.1: las dos anchuras estan en el suelo, una la ultima",
             _orden[-1][0] == "dur_width_rel"
             and "est_width_rel" in [f for f, _ in _orden[6:]],
             f"ultima: {_orden[-1][0]}")
for f, m_tex, s_tex in [("dur_width_rel", 0.3, 0.3),
                        ("est_width_rel", 0.9, 0.5)]:
    check(f"7.1 y 8: {f} (texto +{m_tex})", m_tex, _med[f], tol=0.051)
    check(f"7.1: su desviacion (texto {s_tex})", s_tex, _sd[f], tol=0.051)
# centinela del fichero de una sola extraccion: sus magnitudes eran las
# que el texto citaba antes (51.0 / 28.1 / 10.6) y las de anchura casi
# nulas; se guarda para que se vea de donde viene el cambio
_imp = {r["feature"]: float(r["delta_puntos"])
        for r in __import__("csv").DictReader(
            open("benchmarks/feature_importance.csv", encoding="utf-8"))}
for f, v in [("holgura", 51.0), ("pos_restante", 28.1), ("rem_up", 10.6)]:
    check(f"centinela: una sola permutacion daba {f} = {v}", v, _imp[f],
          tol=0.06)
# 7.1 dice que una sola extraccion reordena la mitad baja pero no las
# tres de cabeza; es exactamente lo que separa los dos ficheros
_o1 = [f for f, _ in sorted(_imp.items(), key=lambda kv: -kv[1])]
_o5 = [f for f, _ in _orden]
check_exacto("7.1: una extraccion conserva las tres de cabeza",
             _o1[:3] == _o5[:3], str(_o1[:3]))
check_exacto("7.1: pero reordena la mitad baja",
             _o1[8:] != _o5[8:],
             f"{sum(a == b for a, b in zip(_o1, _o5))}/16 posiciones iguales")

# =========================================================================

print("\n== la regla del companion como baseline publicado ==")
_clas = {r["inst"]: r for r in __import__("csv").DictReader(
    open("benchmarks/classic12_tuned.csv", encoding="utf-8"))}
_est12 = {r["inst"]: float(r["est_re"]) for r in __import__("csv").DictReader(
    open("benchmarks/classic12_est.csv", encoding="utf-8"))}
_pol12 = {}
for r in __import__("csv").DictReader(
        open("benchmarks/eval_classic12_policy.csv", encoding="utf-8")):
    _pol12.setdefault(r["name"], []).append(float(r["re"]))
_gp = {}
for r in __import__("csv").DictReader(
        open("benchmarks/reevo_fixedfit/summary.csv", encoding="utf-8")):
    if r["method"] == "gp_tuned_seed1":
        _gp[ta_de(r["instance"])] = float(r["re"])
check_exacto("la regla destacada cubre las 70", len(_gp) == 70, str(len(_gp)))
check("GP sobre las 70 (publicado 17.71)", 17.71, sum(_gp.values()) / 70)
_gp_clases = [sum(_gp[f"TA{i * 10 + j + 1}"] for j in range(10)) / 10
              for i in range(7)]
for c, v_tex in enumerate([15.7, 16.6, 18.1, 21.1, 24.1, 13.8, 14.6]):
    check(f"tab:seventy GP clase {c + 1} (texto {v_tex})", v_tex,
          _gp_clases[c])

# el enfrentamiento, a PRESUPUESTOS EMPAREJADOS: una pasada contra una
# pasada, y 1024 muestras contra 1024 (comparar 1 contra 1024 sesgaba)
_gp1024 = {ta_de(r["instance"]): float(r["best_at_1024"]) for r in
           __import__("csv").DictReader(
               open("benchmarks/fair_gp_eps.csv", encoding="utf-8"))}
check("GP una pasada sobre las 70 (texto 17.7)", 17.7,
      sum(_gp.values()) / 70)
check("GP con 1024 muestras (texto 14.1)", 14.1,
      sum(_gp1024.values()) / 70)

# tab:seventy: las dos filas de best-of-64 que la tabla fusionada anade.
# Las de GP salen del mismo deposito que su 1024 (fair_gp_eps.csv), donde
# el brazo va aleatorizado con epsilon-greedy; su "una pasada" NO es esa
# columna sino la regla determinista, que es lo que la caption declara
_gp_bon = {}
for _r in __import__("csv").DictReader(
        open("benchmarks/fair_gp_eps.csv", encoding="utf-8")):
    _gp_bon[ta_de(_r["instance"])] = (float(_r["best_at_1"]),
                                      float(_r["best_at_64"]))
_gp64_clases = [sum(_gp_bon[f"TA{i * 10 + j + 1}"][1] for j in range(10)) / 10
                for i in range(7)]
TAB70_GP64 = [12.6, 15.9, 16.8, 17.4, 23.4, 11.7, 13.4]
for c, (v_tex, v_dat) in enumerate(zip(TAB70_GP64, _gp64_clases)):
    check(f"tab:seventy GP-64 clase {c + 1} (texto {v_tex})", v_tex, v_dat)
check("tab:seventy GP con 64 sobre las 70 (texto 15.9)", 15.9,
      sum(v[1] for v in _gp_bon.values()) / 70)
check_exacto("aviso: el 1-sample de fair_gp_eps NO es la pasada "
             "determinista (18.5 vs 17.7)",
             abs(sum(v[0] for v in _gp_bon.values()) / 70 - 17.7) > 0.5,
             f"{sum(v[0] for v in _gp_bon.values()) / 70:.1f} vs 17.7")
check("politica greedy sobre las 70 (texto 19.4)", 19.4,
      sum(gre[ta] for ta in _gp) / 70)

for etiqueta, rival, pol, gana_tex, med_tex in [
        ("una pasada", _gp, gre, 21, -2.0),
        ("1024 muestras", _gp1024, _bo, 46, 1.3)]:
    gana = sum(pol[ta] < rival[ta] for ta in rival)
    check_exacto(f"{etiqueta}: la politica gana {gana_tex} de 70",
                 gana == gana_tex, f"{gana}/70")
    d = sorted(rival[ta] - pol[ta] for ta in rival)
    check(f"{etiqueta}: mediana (texto {med_tex:+.1f})", med_tex, d[35],
          tol=0.06)
try:
    from scipy import stats as _st
    p1 = _st.wilcoxon([_gp[ta] - gre[ta] for ta in _gp])[1]
    p2 = _st.wilcoxon([_gp1024[ta] - _bo[ta] for ta in _gp1024])[1]
    check_exacto("una pasada: p ~4.6e-4", 4.0e-4 <= p1 <= 5.2e-4,
                 f"{p1:.2e}")
    check_exacto("1024 muestras: p ~1.4e-3", 1.1e-3 <= p2 <= 1.7e-3,
                 f"{p2:.2e}")
except ImportError:
    pendiente("Wilcoxon frente al GP", "sin scipy")

# la fila de medias de tab:classics
_med_tex = [40.6, 30.1, 17.9, 12.4, 11.1, 9.8, 6.4, 5.8, 5.5]
_med_dat = [
    sum(_est12.values()) / 12,
    sum(float(c["gt"]) for c in _clas.values()) / 12,
    sum(float(c["gp"]) for c in _clas.values()) / 12,
    sum(sum(v) / len(v) for v in _pol12.values()) / 12,
    sum(min(v) for v in _pol12.values()) / 12,
    sum(float(c["GA"]) for c in _clas.values()) / 12,
    sum(float(c["ABCE3"]) for c in _clas.values()) / 12,
    sum(float(c["fEABC"]) for c in _clas.values()) / 12,
    sum(float(c["ESABC"]) for c in _clas.values()) / 12,
]
_mal_med = sum(abs(a - b) > 0.051 for a, b in zip(_med_tex, _med_dat))
check_exacto("la fila de medias de tab:classics", _mal_med == 0,
             f"{_mal_med} mal")

print("\n== apendice por instancia ==")
_blk = TEX[TEX.index("\\label{tab:perinstance}"):]
_blk = _blk[_blk.index("\\midrule"):_blk.index("\\bottomrule")]
_n = len(re.findall(r"TA\d+ & \d+ &", _blk))
check_exacto("filas del apendice: 70/70", _n == 70, f"{_n}/70")
# y sus columnas coinciden con las fuentes, no solo su numero
_filas = {m[0]: m[1:] for m in re.findall(
    r"(TA\d+) & \d+ & ([\d.]+) & ([\d.]+) & ([\d.]+) & ([\d.]+) & ([\d.]+)",
    _blk)}
_mal = 0
for ta, celdas in _filas.items():
    reales = (est_pi[ta], GT_RE[ta], _gp[ta], gre[ta], _bo[ta])
    for v_tex, v_dat in zip(celdas, reales):
        if abs(float(v_tex) - v_dat) > 0.051:
            _mal += 1
check_exacto(f"las {len(_filas) * 5} celdas del apendice", _mal == 0,
             f"{_mal} mal")
# y la columna de cotas, que es el denominador de todas las demas
_lbs = dict(re.findall(r"(TA\d+) & (\d+) &", _blk))
_mal_lb = [ta for ta, v in _lbs.items() if int(v) != LB[ta]]
check_exacto("las 70 cotas inferiores del apendice", not _mal_lb,
             str(_mal_lb[:5]))


print("\n== delimitacion de la conciencia intervalar ==")

# 7.5 afirma que NINGUN componente de recompensa lee la cota inferior
# salvo en la rama de lambda. Es la premisa de todo el argumento, asi
# que se comprueba contra el codigo y no contra la memoria: si alguien
# anade un componente que use .lower, la afirmacion deja de ser cierta
# y hay que enterarse aqui, no en la revision.
_comp = glob.glob("jobshop_rl/rewards/components/*.py")
check_exacto("hay 6 componentes de recompensa mas __init__",
             len(_comp) == 8, f"{len(_comp)} ficheros")
_con_lower = {}
for _p in _comp:
    _src = open(_p, encoding="utf-8").read()
    # se ignoran comentarios y docstrings: lo que importa es el codigo
    _codigo = re.sub(r'""".*?"""', "", _src, flags=re.S)
    _codigo = "\n".join(l for l in _codigo.splitlines()
                        if not l.strip().startswith("#"))
    _n = _codigo.count(".lower")
    if _n:
        _con_lower[os.path.basename(_p)] = _n
check_exacto("solo makespan.py lee la cota inferior",
             list(_con_lower) == ["makespan.py"], str(_con_lower))
# y ese unico .lower vive dentro del if de lambda: se comprueba sobre el
# codigo sin docstrings, donde el env var aparece una sola vez
_ms = open("jobshop_rl/rewards/components/makespan.py",
           encoding="utf-8").read()
_ms_cod = re.sub(r'""".*?"""', "", _ms, flags=re.S)
_i = _ms_cod.index("DEEPLJSP_V2_LAMBDA")
_j = _ms_cod.index(".lower", _i)
check_exacto("y ese unico .lower esta dentro de la rama de lambda",
             0 < _j - _i < 200 and "if lam" in _ms_cod[_i:_j],
             f"{_j - _i} caracteres tras el env var")

# 4.1 imprime los pesos EFECTIVOS del reward en las instancias de
# entrenamiento. Se recomputan con el propio generador de la factoria
# (la clase AdaptiveRewardStrategy tiene otros defaults que NO rigen:
# el generador los sobreescribe, y eso es lo que confundio al borrador)
try:
    sys.path.insert(0, ".")
    from jobshop_rl.data import PROBLEM_REGISTRY as _REG
    from jobshop_rl.utils.problem_analyzer import (ProblemAnalyzer as _PA,
                                                   AdaptiveConfigGenerator
                                                   as _ACG)
    _ws = []
    for _k in range(1, 5):
        _pd = _REG[f"int__tai20_15_{_k:02d}"]()
        _an = _PA.analyze_problem(_pd["sequences"], _pd["durations"])
        _ws.append(_ACG.generate_reward_config(_an))
    for _clave, _v_tex in [("makespan_weight", 1.0),
                           ("progress_weight", 0.26),
                           ("local_improvement_weight", 0.15),
                           ("critical_weight", 0.1),
                           ("balance_weight", 0.1)]:
        _vals = [w[_clave] for w in _ws]
        check_exacto(f"4.1: {_clave} efectivo (texto {_v_tex})",
                     all(abs(v - _v_tex) < 0.005 for v in _vals),
                     f"{min(_vals):.3f}..{max(_vals):.3f}")
    _idle = [w["idle_weight"] for w in _ws]
    check_exacto("4.1: idle_weight efectivo ~0.24 (texto)",
                 all(0.23 <= v <= 0.25 for v in _idle),
                 f"{min(_idle):.3f}..{max(_idle):.3f}")
    check_exacto("4.1: progreso = 0.2 x 1.3 por intervalos (texto)",
                 '"progress_weight"] *= 1.3' in
                 open("jobshop_rl/utils/problem_analyzer.py",
                      encoding="utf-8").read())
except Exception as _e:
    pendiente("pesos efectivos del reward", f"{type(_e).__name__}: {_e}")
check_exacto("4.1: bonus dentro del 5% del limite (codigo)",
             "gap <= 0.05" in _ms_cod)
_li = open("jobshop_rl/rewards/components/local_improvement.py",
           encoding="utf-8").read()
check_exacto("4.1: deterioros penalizados x2 (codigo)",
             "* 2.0" in _li)


def _por_par(*tags):
    """{(TA, semilla): RE} de una o varias campanas, componentwise.

    Acepta varias porque los brazos extendidos viven en un tag propio:
    v2-full-1000ep y v2-full-1000ep-ext-c son las mismas diez tiradas.
    """
    out = {}
    for tag in tags:
        for d in sorted(glob.glob(f"outputs/bench_{tag}__*_seed*")):
            s = d.split("_seed")[-1]
            for p in glob.glob(f"{d}/plots/test/*_schedule.json"):
                ta = ta_de(os.path.basename(p))
                out[(ta, s)] = re_pct(makespans(p)[0], ta)
    return out


_full = _por_par("v2-full-1000ep")
_nw = _por_par("v2-nowidth-1000ep-b")
_mp = _por_par("v2-midpoint-1000ep-b")

# 7.5: el punto medio a DIEZ semillas, que es donde el efecto se
# detecta. El brazo de no-width sigue en tres: su d=0.12 necesitaria
# unas noventa, y el texto lo dice en vez de pedirlas.
_full10 = _por_par("v2-full-1000ep", "v2-full-1000ep-ext-c")
_mp10 = _por_par("v2-midpoint-1000ep-b", "v2-midpoint-1000ep-ext")
_c10 = sorted(set(_full10) & set(_mp10))
check_exacto("punto medio: diez semillas x seis instancias",
             len(_c10) == 60, f"{len(_c10)} pares")
check("punto medio a diez semillas (texto 14.45)", 14.45,
      sum(_mp10[k] for k in _c10) / 60, tol=0.006)
_d10 = [_mp10[k] - _full10[k] for k in _c10]
check("punto medio: diferencia (texto +0.63)", 0.63,
      sum(_d10) / 60, tol=0.006)
check_exacto("punto medio: peor en 36 de 60",
             sum(x > 0 for x in _d10) == 36,
             f"{sum(x > 0 for x in _d10)}/60")
_sem10 = sorted({k[1] for k in _c10}, key=int)
_pos = sum(1 for s in _sem10
           if sum(_mp10[k] - _full10[k] for k in _c10 if k[1] == s) > 0)
check_exacto("punto medio: positivo en 8 de las 10 semillas",
             _pos == 8, f"{_pos}/10")
try:
    from scipy import stats as _stmp
    _pmp = _stmp.wilcoxon(_d10)[1]
    check_exacto("punto medio a diez semillas: significativo (texto 0.045)",
                 0.040 <= _pmp <= 0.050, f"p={_pmp:.4f}")
except ImportError:
    pendiente("Wilcoxon del punto medio a diez", "sin scipy")
for nombre, arm, v_tex in [("no-width", _nw, 13.62),
                           ("punto medio", _mp, 14.18)]:
    if not arm:
        pendiente(f"brazo {nombre}", "sin directorios en outputs/")
        continue
    check_exacto(f"{nombre}: 3 semillas x 6 instancias", len(arm) == 18,
                 f"{len(arm)} pares")
    check(f"{nombre}: media (texto {v_tex})", v_tex,
          sum(arm.values()) / len(arm))
    comunes = sorted(set(_full) & set(arm))
    d = [arm[k] - _full[k] for k in comunes]
    peor = sum(x > 0 for x in d)
    try:
        from scipy import stats as _st
        p = _st.wilcoxon(d)[1]
        if nombre == "no-width":
            check("no-width: delta medio (texto +0.18)", 0.18,
                  sum(d) / len(d), tol=0.02)
            # 7.5 razona con el tamano del efecto, no solo con el p
            import statistics as _s7
            _sd = _s7.stdev(d)
            check("no-width: sd de las diferencias (texto 1.54)", 1.54,
                  _sd, tol=0.006)
            check("no-width: d de Cohen (texto 0.12)", 0.12,
                  abs(sum(d) / len(d)) / _sd, tol=0.006)
            check_exacto("no-width: harian falta ~90 semillas",
                         80 <= (2.8 / (abs(sum(d) / len(d)) / _sd)) ** 2 / 6
                         <= 100,
                         f"{(2.8 / (abs(sum(d) / len(d)) / _sd)) ** 2 / 6:.0f}")
            check_exacto("no-width: peor en 12 de 18", peor == 12,
                         f"{peor}/18")
            check_exacto("no-width: no significativo (texto p=0.47)",
                         0.44 <= p <= 0.50, f"p={p:.3f}")
        else:
            print(f"  info  punto medio a tres semillas: p={p:.3f} "
                  f"(el texto usa las diez)")
    except ImportError:
        pendiente(f"Wilcoxon {nombre}", "sin scipy")
check("brazo principal de referencia (texto 13.44)", 13.44,
      sum(_full.values()) / len(_full))

# 6.1: las diez semillas. El 13.44 son las tres del paper; conviene que
# el texto no pueda separarse de la distribucion completa sin avisar
_ext = _por_par("v2-full-1000ep-ext-c")
if not _ext:
    pendiente("extension de semillas", "sin directorios en outputs/")
else:
    _diez = {}
    for k, v in list(_full.items()) + list(_ext.items()):
        _diez.setdefault(k[1], []).append(v)
    check_exacto("diez semillas de seis instancias",
                 len(_diez) == 10 and all(len(v) == 6
                                          for v in _diez.values()),
                 f"{len(_diez)} semillas")
    _m = sorted(sum(v) / len(v) for v in _diez.values())
    check("diez semillas: media (texto 13.82)", 13.82,
          sum(_m) / len(_m), tol=0.006)
    check("diez semillas: minimo (texto 13.12)", 13.12, _m[0], tol=0.006)
    check("diez semillas: maximo (texto 14.62)", 14.62, _m[-1], tol=0.006)
    try:
        import statistics as _stat
        check("diez semillas: sd entre medias (texto 0.47)", 0.47,
              _stat.stdev(_m), tol=0.006)
    except Exception:
        pendiente("sd de las diez semillas", "no calculable")


# --- el brazo robusto lambda=1: RE Y ancho, que es lo que lambda toca ---
def _extremos(path):
    lo_max = up_max = 0.0
    for t in json.load(open(path)):
        e = t["end"]
        lo, up = (e["lower"], e["upper"]) if isinstance(e, dict) else (e, e)
        lo_max, up_max = max(lo_max, lo), max(up_max, up)
    return lo_max, up_max


def _re_y_ancho(tag):
    """{(TA, semilla): (RE, ancho relativo %)} desde los schedules."""
    out = {}
    for d in sorted(glob.glob(f"outputs/bench_{tag}__*_seed*")):
        s = d.split("_seed")[-1]
        for p in glob.glob(f"{d}/plots/test/*_schedule.json"):
            ta = ta_de(os.path.basename(p))
            lo, up = _extremos(p)
            mid = (lo + up) / 2
            out[(ta, s)] = (re_pct(mid, ta), (up - lo) / mid * 100)
    return out


_lam = _re_y_ancho("v2-robust-lam1")
_base_a = _re_y_ancho("v2-full-1000ep")
if not _lam:
    pendiente("brazo lambda=1", "sin directorios en outputs/")
else:
    check_exacto("lambda=1: 3 semillas x 6 instancias", len(_lam) == 18,
                 f"{len(_lam)} pares")
    check("lambda=1: RE media (texto 15.38)", 15.38,
          sum(v[0] for v in _lam.values()) / len(_lam))
    check("lambda=1: ancho medio (texto 11.90)", 11.90,
          sum(v[1] for v in _lam.values()) / len(_lam))
    check("brazo principal: ancho medio (texto 12.85)", 12.85,
          sum(v[1] for v in _base_a.values()) / len(_base_a))
    _com = sorted(set(_base_a) & set(_lam))
    _dre = [_lam[k][0] - _base_a[k][0] for k in _com]
    _dan = [_lam[k][1] - _base_a[k][1] for k in _com]
    check("lambda=1: RE sube 1.94 puntos (texto)", 1.94,
          sum(_dre) / len(_dre), tol=0.02)
    check_exacto("lambda=1: mas estrecho en 13 de 18",
                 sum(x < 0 for x in _dan) == 13,
                 f"{sum(x < 0 for x in _dan)}/18")
    try:
        from scipy import stats as _st
        _p_re, _p_an = _st.wilcoxon(_dre)[1], _st.wilcoxon(_dan)[1]
        check_exacto("lambda=1: RE significativa (texto p=0.007)",
                     0.006 <= _p_re <= 0.009, f"p={_p_re:.4f}")
        check_exacto("lambda=1: ancho significativo (texto p=0.010)",
                     0.009 <= _p_an <= 0.012, f"p={_p_an:.4f}")
    except ImportError:
        pendiente("Wilcoxon lambda=1", "sin scipy")

# el control que separa entrenamiento de seleccion: mismo deposito de
# rollouts, mismo criterio, solo cambian los pesos
_ROLL = "benchmarks/robust_lambda/rollouts.csv"
if not os.path.exists(_ROLL):
    pendiente("control de seleccion fijada", "sin rollouts.csv")
else:
    import csv as _csv
    _pool = {}
    for r in _csv.DictReader(open(_ROLL, encoding="utf-8")):
        _pool.setdefault((r["arm"], r["seed"], r["instance"]), []).append(
            (float(r["lower"]), float(r["upper"])))
    check_exacto("deposito: 36 combinaciones de 64 rollouts",
                 len(_pool) == 36 and all(len(v) == 64
                                          for v in _pool.values()),
                 f"{len(_pool)} combinaciones")

    def _ancho_medio(brazo, criterio):
        anchos = []
        for k, v in _pool.items():
            if k[0] != brazo:
                continue
            lo, up = min(v, key=(lambda t: (t[1], t[0])) if criterio == "up"
                         else (lambda t: 2 * t[1] - t[0]))
            anchos.append((up - lo) / ((lo + up) / 2) * 100)
        return sum(anchos) / len(anchos)

    for brazo, crit, v_tex in [("base", "up", 12.80), ("lam1", "up", 12.69),
                               ("base", "rob", 11.74), ("lam1", "rob", 12.20)]:
        check(f"seleccion fijada, {brazo} por {crit} (texto {v_tex})",
              v_tex, _ancho_medio(brazo, crit), tol=0.02)

    # el barrido: frontera desplegada monotona, nulo con seleccion
    # fijada, y la misma frontera gratis desde el deposito del base
    _ROLL2 = "benchmarks/robust_lambda/rollouts_sweep.csv"
    if not os.path.exists(_ROLL2):
        pendiente("barrido de lambda", "sin rollouts_sweep.csv")
    else:
        _lbs2 = {}
        for _ruta in (_ROLL, _ROLL2):
            for r in _csv.DictReader(open(_ruta, encoding="utf-8")):
                _pool.setdefault((r["arm"], r["seed"], r["instance"]),
                                 []).append((float(r["lower"]),
                                             float(r["upper"])))
                _lbs2[r["instance"]] = float(r["lb"])
        # rollouts.csv se relee: dedup por longitud
        for k in list(_pool):
            _pool[k] = _pool[k][:64]
        check_exacto("barrido: 90 combinaciones de 64 rollouts",
                     len(_pool) == 90 and all(len(v) == 64
                                              for v in _pool.values()),
                     f"{len(_pool)} combinaciones")

        def _sel64(v, lam):
            if lam == 0.0:
                return min(v, key=lambda t: (t[1], t[0]))
            return min(v, key=lambda t: t[1] + lam * (t[1] - t[0]))

        def _re_anc(brazo, lam):
            re, anc = [], []
            for k, v in sorted(_pool.items()):
                if k[0] != brazo:
                    continue
                lo, up = _sel64(v, lam)
                mid = (lo + up) / 2
                re.append((mid - _lbs2[k[2]]) / _lbs2[k[2]] * 100)
                anc.append((up - lo) / mid * 100)
            return (sum(re) / len(re), sum(anc) / len(anc),
                    re, anc)

        _BRAZOS = [("base", 0.0, 12.80), ("lam0p5", 0.5, 12.38),
                   ("lam1", 1.0, 12.20), ("lam2", 2.0, 11.88),
                   ("lam4", 4.0, 10.99)]
        _prop = {}
        for brazo, lam, v_tex in _BRAZOS:
            _prop[brazo] = _re_anc(brazo, lam)
            check(f"barrido desplegado, ancho {brazo} (texto {v_tex})",
                  v_tex, _prop[brazo][1], tol=0.02)
        check_exacto("barrido: el ancho desplegado cae monotonamente",
                     all(_prop[a][1] > _prop[b][1] for (a, _, _), (b, _, _)
                         in zip(_BRAZOS, _BRAZOS[1:])))
        check("barrido: RE de lam4 desplegado (texto 17.75)", 17.75,
              _prop["lam4"][0])
        check("barrido: lam4 sube 3.49 puntos sobre base (texto)", 3.49,
              _prop["lam4"][0] - _prop["base"][0], tol=0.02)

        # seleccion fijada por cota superior para los cuatro brazos
        _fija = {b: _re_anc(b, 0.0) for b, _, _ in _BRAZOS}
        _mas_anchos = sum(_fija[b][1] > _fija["base"][1]
                          for b in ("lam0p5", "lam1", "lam2", "lam4"))
        check_exacto("barrido fijado: 3 de 4 mas anchos que base (texto)",
                     _mas_anchos == 3, f"{_mas_anchos}/4")
        try:
            from scipy import stats as _st2
            _p4 = _st2.wilcoxon([a - b for a, b in
                                 zip(_prop["lam4"][2],
                                     _prop["base"][2])])[1]
            check_exacto("barrido: RE lam4 significativa (texto p=0.0002)",
                         0.0001 <= _p4 <= 0.0003, f"p={_p4:.5f}")
            _pmin = min(_st2.wilcoxon([a - b for a, b in
                                       zip(_fija[br][3],
                                           _fija["base"][3])])[1]
                        for br in ("lam0p5", "lam1", "lam2", "lam4"))
            check_exacto("barrido fijado: ancho nunca significativo "
                         "(texto: smallest p=0.37)",
                         0.365 <= _pmin <= 0.375, f"p_min={_pmin:.3f}")
        except ImportError:
            pendiente("Wilcoxon del barrido", "sin scipy")

        # la frontera gratis: el deposito del base bajo f_4
        _re_g, _anc_g, _, _ = _re_anc("base", 4.0)
        check("frontera gratis: base bajo f_4, ancho (texto 11.09)",
              11.09, _anc_g, tol=0.02)
        check("frontera gratis: base bajo f_4, RE (texto 17.05)",
              17.05, _re_g, tol=0.02)
        check("precio del barrido: 1.9 RE por punto de ancho (texto)",
              1.9, (_prop["lam4"][0] - _prop["base"][0])
              / (_prop["base"][1] - _prop["lam4"][1]), tol=0.06)


print("\n== tab:crosssize: best-of-64 sobre las 70 por clase ==")
_B64 = "benchmarks/bo64_70.csv"
if not os.path.exists(_B64):
    pendiente("tab:crosssize sobre las 70", "sin bo64_70.csv")
else:
    _b64 = list(__import__("csv").DictReader(open(_B64, encoding="utf-8")))
    check_exacto("bo64_70: las 70 instancias", len(_b64) == 70,
                 f"{len(_b64)} filas")
    _pc = {}
    for r in _b64:
        _pc.setdefault(r["cls"], []).append((float(r["re_mean"]),
                                             float(r["re_best"])))
    TAB7 = {"15x15": (11.0, 9.6), "20x15": (13.6, 13.0),
            "20x20": (14.8, 14.0), "30x15": (16.8, 16.0),
            "30x20": (22.0, 20.7), "50x15": (12.2, 11.1),
            "50x20": (15.5, 13.9)}
    _mal7 = 0
    for cls, (m_tex, b_tex) in TAB7.items():
        v = _pc[cls]
        check_exacto(f"tab:seventy {cls}: diez instancias", len(v) == 10,
                     f"{len(v)}")
        for tex, dat in ((m_tex, sum(a for a, _ in v) / 10),
                         (b_tex, sum(b for _, b in v) / 10)):
            if abs(tex - dat) > 0.051:
                print(f"  FALLO {cls}: texto={tex} datos={dat:.2f}")
                _mal7 += 1
    # la media por clase va impresa en tab:seventy; el "mejor por semilla"
    # ya no se imprime desde que la tabla se fusiono, pero se sigue
    # comprobando como centinela del dato
    check_exacto("las 14 celdas de politica a 64 (media y mejor)",
                 _mal7 == 0, f"{_mal7} mal")
    _todo7 = [x for v in _pc.values() for x in v]
    check("tab:seventy fila Policy-64, All (texto 15.1)", 15.1,
          sum(a for a, _ in _todo7) / 70)
    check("centinela: mejor por semilla a 64 sobre las 70 (14.0)", 14.0,
          sum(b for _, b in _todo7) / 70)
    # la afirmacion de 6.2 es POR SEMILLA ("every seed's network"), no
    # sobre la media: hay que reconstruir el best-of-64 de cada checkpoint
    # desde el deposito de rollouts, 210 pares (instancia, semilla)
    import collections as _col
    _dep = _col.defaultdict(lambda: _col.defaultdict(list))
    _lb_dep = {}
    for _r in __import__("csv").DictReader(
            open("benchmarks/eval_budget_curve.csv", encoding="utf-8")):
        _s = re.search(r"seed(\d+)", _r["checkpoint"]).group(1)
        _dep[_r["instance"]][_s].append(float(_r["mid_comp"]))
        _lb_dep[_r["instance"]] = float(_r["lb"])
    _pares = _malG = _malM = 0
    for _inst, _seeds in _dep.items():
        _ta, _lb = ta_de(_inst), _lb_dep[_inst]
        for _s, _vals in _seeds.items():
            _re64 = (min(_vals[:64]) - _lb) / _lb * 100
            _pares += 1
            _malG += _re64 >= GT_RE[_ta]
            _malM += _re64 >= MOR_RE[_ta]
    check_exacto("6.2: 210 pares (instancia, semilla)", _pares == 210,
                 f"{_pares}")
    check_exacto("6.2: cada semilla bate a G&T-MWKR en las 70",
                 _malG == 0, f"{_malG} pares sin batirla")
    check_exacto("6.2: y tambien a MOR (afirmacion mas debil)",
                 _malM == 0, f"{_malM} pares sin batirla")
    # y que 50x15 transfiere mejor que las de 30 maquinas, como dice 6.2
    check_exacto("6.2: 50x15 transfiere mejor que 30x15 y 30x20",
                 sum(a for a, _ in _pc["50x15"]) / 10
                 < min(sum(a for a, _ in _pc[c]) / 10
                       for c in ("30x15", "30x20")))

print("\n== fig:budget: la curva de presupuesto ==")
_POOL = "benchmarks/eval_budget_curve.csv"
if not os.path.exists(_POOL):
    pendiente("curva de presupuesto", "sin eval_budget_curve.csv")
else:
    _cur = {}
    _lbc = {}
    for r in __import__("csv").DictReader(open(_POOL, encoding="utf-8")):
        _cur.setdefault((r["instance"], r["checkpoint"]), []).append(
            (int(r["sample_idx"]), float(r["mid_comp"])))
        _lbc[r["instance"]] = float(r["lb"])
    _inst_c = {i for i, _ in _cur}
    check_exacto("la curva cubre las 70 con 3 checkpoints",
                 len(_inst_c) == 70 and len(_cur) == 210
                 and all(len(v) == 342 for v in _cur.values()),
                 f"{len(_inst_c)} instancias, {len(_cur)} pares")
    # el greedy del deposito (indice 0), agregado como la curva: el mejor
    # de los tres checkpoints, no la media, que es el 19.4 de 6.4
    _gre_pool = {}
    for (i, ck), v in _cur.items():
        _gre_pool.setdefault(i, []).append(dict(v)[0])
    check("fig:budget: greedy mejor de 3 semillas (texto 17.0)", 17.0,
          sum((min(v) - _lbc[i]) / _lbc[i] * 100
              for i, v in _gre_pool.items()) / 70, tol=0.051)
    # y que la referencia del GP de la figura sea la DESTACADA, no la
    # columna GP_re de constructive_per_instance (que es otra regla)
    _gp_cpi = {r["ta"]: float(r["GP_re"]) for r in
               __import__("csv").DictReader(
                   open("benchmarks/constructive_per_instance.csv",
                        encoding="utf-8"))}
    check_exacto("aviso: GP_re de constructive_per_instance NO es la "
                 "destacada", abs(sum(_gp_cpi.values()) / 70 - 17.71) > 0.5,
                 f"{sum(_gp_cpi.values()) / 70:.2f} vs 17.71")

    print("\n== tab:budget-rate: rendimiento y coste por duplicacion ==")
    # misma reconstruccion que la figura (reparto del presupuesto entre los
    # tres checkpoints, min del subconjunto), remuestreada con semilla fija
    import numpy as _np
    _NCK, _R = 341, 150
    _POT = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1023]
    _pools = {}
    for (i, ck), v in _cur.items():
        _pools.setdefault(i, []).append(
            [x for idx, x in sorted(v) if idx != 0][:_NCK])
    _pools = {i: _np.array(p) for i, p in _pools.items() if len(p) == 3}
    _rng = _np.random.RandomState(20260807)
    _curva = []
    for _b in _POT:
        _tot = 0.0
        for _i, _pl in _pools.items():
            _lb, _acc = _lbc[_i], 0.0
            for _ in range(_R):
                _q, _rst = divmod(_b, 3)
                _cnt = [_q] * 3
                for _c in _rng.choice(3, _rst, replace=False):
                    _cnt[_c] += 1
                _mej = float("inf")
                for _c in range(3):
                    if _cnt[_c]:
                        _ix = _rng.choice(_NCK, _cnt[_c], replace=False)
                        _mej = min(_mej, _pl[_c, _ix].min())
                _acc += (_mej - _lb) / _lb * 100
            _tot += _acc / _R
        _curva.append(_tot / len(_pools))
    _re = dict(zip(_POT, _curva))
    _gan = {_POT[k]: _curva[k - 1] - _curva[k] for k in range(1, len(_POT))}
    # en B=1 la esperanza es exacta (la media de las 1023 muestras), no
    # hace falta remuestrear: es ademas el 21.4 que ya citaba el texto
    check("tab:budget-rate RE en B=1 (exacta)", 21.4,
          sum((_pl.mean() - _lbc[_i]) / _lbc[_i] * 100
              for _i, _pl in _pools.items()) / len(_pools), tol=0.051)
    for _b, _esp in ((8, 17.1), (64, 14.9), (128, 14.3),
                     (256, 13.8), (512, 13.3), (1023, 12.9)):
        check(f"tab:budget-rate RE en B={_b}", _esp, _re[_b], tol=0.11)
    for _b, _esp in ((8, 1.03), (64, 0.62), (128, 0.57), (256, 0.50),
                     (512, 0.46), (1023, 0.42)):
        check(f"tab:budget-rate ganancia sobre B/2 en B={_b}", _esp,
              _gan[_b], tol=0.055)
    # la pendiente log-lineal de las tres ultimas octavas que cita el texto
    _x = [math.log2(_b) for _b in _POT[-4:]]
    _y = _curva[-4:]
    _mx, _my = sum(_x) / 4, sum(_y) / 4
    _pend = (sum((_a - _mx) * (_c - _my) for _a, _c in zip(_x, _y))
             / sum((_a - _mx) ** 2 for _a in _x))
    check("7.2: pendiente 0.46 puntos por duplicacion", 0.46, -_pend,
          tol=0.03)
    check("7.2: cuatro duplicaciones mas llegarian al 11%", 11.0,
          _curva[-1] + 4 * _pend, tol=0.15)
    # "cada octava rinde una decima parte menos que la anterior"
    _raz = [_gan[_POT[k]] / _gan[_POT[k - 1]] for k in range(6, len(_POT))]
    check_exacto("7.2: la ganancia mengua ~10% por octava en la cola",
                 all(0.82 <= _r <= 0.98 for _r in _raz),
                 " ".join(f"{_r:.2f}" for _r in _raz))
    # el coste: lineal en B sobre el tiempo por muestra medido
    _tie = {r["clase"]: r for r in __import__("csv").DictReader(
        open("benchmarks/tiempos_inferencia.csv", encoding="utf-8"))}
    _s2015 = float(_tie["20x15"]["bo64_s"]) / 64
    _s5020 = float(_tie["50x20"]["bo64_s"]) / 64
    check("7.2: segundos por muestra en 20x15", 1.03, _s2015, tol=0.006)
    check("7.2: segundos por muestra en 50x20", 6.4, _s5020, tol=0.05)
    check("7.2: B=1023 son 18 min en 20x15", 18.0, 1023 * _s2015 / 60,
          tol=0.5)
    check("7.2: B=1023 son 1.8 h en 50x20", 1.8, 1023 * _s5020 / 3600,
          tol=0.05)
    check("7.2: x16 el presupuesto son 4.7 h en 20x15", 4.7,
          16 * 1023 * _s2015 / 3600, tol=0.05)
    check("7.2: x16 el presupuesto son 29 h en 50x20", 29.0,
          16 * 1023 * _s5020 / 3600, tol=0.5)

    print("\n== 8: el hueco entre el argmax y la cola de su distribucion ==")
    # la cuarta direccion de las conclusiones: cuanto separa la decision
    # comprometida de la mejor que la propia distribucion produce, en la
    # politica y en la regla, y con que dispersion
    _mu = _sg = _zg = _zt = 0.0
    for _i, _pl in _pools.items():
        _lb = _lbc[_i]
        _r = (_pl.ravel() - _lb) / _lb * 100
        _gre = min((_v - _lb) / _lb * 100 for _v in _gre_pool[_i])
        _m, _s = _r.mean(), _r.std()
        _mu += _m
        _sg += _s
        _zg += (_m - _gre) / _s
        _zt += (_m - _r.min()) / _s
    _n = len(_pools)
    check("8: sd de la distribucion muestreada (3.2 puntos)", 3.2,
          _sg / _n, tol=0.051)
    check("8: el argmax esta a 1.4 sd de la media", 1.4, _zg / _n,
          tol=0.051)
    check("8: la mejor de mil esta a 2.6 sd de la media", 2.6, _zt / _n,
          tol=0.051)
    # y el mismo hueco en la regla evolucionada, desde su propio deposito
    _gp = list(__import__("csv").DictReader(
        open("benchmarks/fair_gp_eps.csv", encoding="utf-8")))
    check_exacto("8: fair_gp_eps cubre las 70", len(_gp) == 70, str(len(_gp)))
    check("8: la regla a 1024 muestras (tab:seventy 14.1)", 14.1,
          sum(float(r["best_at_1024"]) for r in _gp) / 70, tol=0.051)
    check("8: y a 64, para identificar que es la destacada (15.9)", 15.9,
          sum(float(r["best_at_64"]) for r in _gp) / 70, tol=0.051)
    # la fila parte en dos lineas del .tex, asi que se une antes de cortar
    _lin = TEX.splitlines()
    _k = next(k for k, l in enumerate(_lin) if l.startswith("GP rule, one pass"))
    _paso_gp = float((_lin[_k] + " " + _lin[_k + 1]).split("&")[8]
                     .replace("\\\\", "").strip())
    check("8: la pasada unica de la regla (tab:seventy)", 17.7, _paso_gp)

# 7.3 explica el nulo de la atencion diciendo que dos features ya son
# relacionales (holgura contra el minimo de las elegibles, congestion
# contra la carga media). Si esas definiciones cambian en la Tabla 1,
# la explicacion deja de sostenerse y hay que enterarse aqui
_fila_slack = next((l for l in TEX.splitlines()
                    if "& slack &" in l), "")
_fila_cong = next((l for l in TEX.splitlines()
                   if "machine congestion" in l), "")
check_exacto("7.3: la holgura se mide contra el minimo de las elegibles",
             r"\min_{o'\in\mathcal{E}}" in _fila_slack,
             _fila_slack.strip()[:60])
check_exacto("7.3: la congestion se mide contra la carga media",
             r"\bar L" in _fila_cong, _fila_cong.strip()[:60])

print("\n== tab:irace: el espacio de busqueda ==")


def _espacio(path):
    """{nombre: (tipo, [valores])} de un parameters.txt de irace."""
    out = {}
    for linea in open(path, encoding="utf-8"):
        linea = linea.strip()
        if not linea or linea.startswith("#"):
            continue
        m = re.match(r'(\w+)\s+"[^"]*"\s+(\S+)\s+\((.*)\)', linea)
        if m:
            out[m.group(1)] = (m.group(2),
                               [x.strip() for x in m.group(3).split(",")])
    return out


_c1 = _espacio("tuning/parameters.txt")
_c2 = _espacio("tuning/parameters_serious.txt")
print("\n== campana 3: los pesos del reward ==")
_t3 = open("tuning/confirm_reward.log", encoding="utf-8",
           errors="replace").read()
_m3 = re.search(r"MEDIA\s+([\d.]+)\s+([\d.]+)\s+([+-][\d.]+)", _t3)
check("5.3: la ganadora de pesos a 1000 eps (texto 14.04)", 14.04,
      float(_m3.group(1)), tol=0.005)
check("5.3: el default en la misma confirmacion (texto 13.55)", 13.55,
      float(_m3.group(2)), tol=0.005)
check_exacto("5.3: mejor en 7 de los 18 pares",
             "mejor en 7 de 18 pares" in _t3)
check("5.3: Wilcoxon de la confirmacion (texto 0.21)", 0.21,
      float(re.search(r"Wilcoxon pareado: p=([\d.]+)", _t3).group(1)),
      tol=0.005)
check_exacto("5.3: el veredicto es la regla 1 del plan",
             "sin mejora significativa" in _t3)
# el espacio que se corrio: seis pesos, cada uno en [0,1]
_p3 = _espacio("tuning/parameters_reward.txt")
check_exacto("5.3: seis pesos, todos en [0, 1]",
             len(_p3) == 6 and all(v[1] == ["0.0", "1.0"]
                                   for v in _p3.values()),
             str(sorted(_p3)))
_l3 = open("tuning/irace_reward.log", encoding="utf-8",
           errors="replace").read()
check_exacto("5.3: 299 experimentos",
             "# experimentsUsed: 299" in _l3)
# la solo-terminal, eliminada en la primera ronda
_sem = [l.split() for l in
        open("tuning/configurations_reward.txt", encoding="utf-8")
        .read().splitlines()[1:]]
check_exacto("5.3: se sembro la solo-terminal (1,0,0,0,0,0)",
             ["1.0", "0.0", "0.0", "0.0", "0.0", "0.0"] in _sem,
             str(_sem))
_it1 = _l3.split("Iteration 2 of")[0]
_el1 = _it1.rsplit("Elite configurations", 1)[-1]
check_exacto("5.3: la solo-terminal no sobrevive la primera ronda",
             not re.search(r"^\s*2\s+1\.0+\s+0\.0+", _el1, re.M),
             _el1.strip().splitlines()[-1][:60])
# las cuatro elites finales: dispersion y concordancia entre semillas
_fin = _l3.split("# Best configurations (")[1]
_elites = [[float(x) for x in m.group(2).split()]
           for m in re.finditer(r"\s*(\d+)\s+((?:[\d.]+\s*){6})$",
                                _fin, re.M)]
check_exacto("5.3: cuatro elites finales", len(_elites) == 4,
             str(len(_elites)))
_rango = max(max(c[j] for c in _elites) - min(c[j] for c in _elites)
             for j in range(6))
check("5.3: se diferencian hasta 0.48 en una componente", 0.48, _rango,
      tol=0.005)
_kw = [float(w) for _, w in re.findall(
    r"\|\s*[-=x.:!]\s*\|.*?\|([-+][\d.]+)\|([\d.]+)\|",
    _l3.rsplit("Iteration 5 of 5", 1)[-1])]
check_exacto("5.3: Kendall W de 0.02 a 0.05 al final de la carrera",
             _kw and 0.02 <= min(_kw[-5:]) and max(_kw[-5:]) <= 0.05,
             " ".join(f"{w:.2f}" for w in _kw[-5:]))

# el limite de resolucion que 5.3 declara: sd 0.47 entre medias de
# semilla y n=3 por brazo dan ~1 punto de efecto minimo detectable
_mde = 2.8 * 0.47 * (2.0 / 3) ** 0.5
check("5.3: tres semillas resuelven ~1 punto de RE", 1.0, _mde, tol=0.11)
check_exacto("5.3: y el 0.47 es el de 6.1",
             "$0.47$ at $1000$" in TEX)
# la contraprueba de que la inyeccion por entorno llega al modelo: la
# elite 27 llevaba hidden=64 y su checkpoint no tiene 120.322 parametros
try:
    import torch as _th

    _d27 = sorted(glob.glob("outputs/bench_v2-elite27-1000ep__*_seed2"))
    if _d27:
        _sd27 = _th.load(_d27[0] + "/best_model.pt", map_location="cpu",
                         weights_only=True)
        _r27 = _sd27.get("network", _sd27)
        _w27 = next(v for k, v in _r27.items()
                    if k.endswith("weight") and v.dim() == 2
                    and v.shape[1] == 16)
        check_exacto("5.3: la inyeccion por entorno llego al modelo "
                     "(elite 27, hidden 64)", int(_w27.shape[0]) == 64,
                     f"hidden={int(_w27.shape[0])}")
except Exception as e:
    pendiente("inyeccion de la elite 27", f"no medible ({type(e).__name__})")

check_exacto("campana 1: 8 parametros", len(_c1) == 8, str(len(_c1)))
check_exacto("campana 2: 6 parametros", len(_c2) == 6, str(len(_c2)))
check_exacto("campana 2 fija minibatch y update-every",
             "minibatch" not in _c2 and "updateevery" not in _c2)

# los rangos que imprime la tabla, contra los ficheros
ESPERADO = {
    "lr": ("0.0001", "0.001"), "entropy": ("0.003", "0.03"),
    "clip": ("0.1", "0.2", "0.3"), "kepochs": ("2", "4", "8"),
    "minibatch": ("128", "256", "512"), "updateevery": ("2", "4", "8"),
    "gae": ("0.90", "0.95", "0.98"), "hidden": ("64", "128", "256"),
}
_mal = [k for k, v in ESPERADO.items() if tuple(_c1[k][1]) != v]
check_exacto("tab:irace, columna de la campana 1", not _mal, str(_mal))
ESPERADO2 = {"kepochs": ("4", "8"), "hidden": ("128", "256"),
             "clip": ("0.1", "0.2", "0.3"),
             "gae": ("0.90", "0.95", "0.98")}
_mal2 = [k for k, v in ESPERADO2.items() if tuple(_c2[k][1]) != v]
check_exacto("tab:irace, columna de la campana 2", not _mal2, str(_mal2))

# la afirmacion del pie: todo defecto cae dentro del espacio buscado
DEFECTOS = {"lr": 3e-4, "entropy": 0.01, "clip": 0.2, "kepochs": 4,
            "minibatch": 256, "updateevery": 4, "gae": 0.95, "hidden": 128}
_fuera = []
for k, d in DEFECTOS.items():
    tipo, vals = _c1[k]
    if tipo.startswith("r"):
        if not float(vals[0]) <= d <= float(vals[1]):
            _fuera.append(k)
    elif str(d) not in [v.lstrip("0") or "0" for v in vals] \
            and not any(abs(float(v) - d) < 1e-9 for v in vals):
        _fuera.append(k)
check_exacto("todo defecto esta dentro del espacio buscado", not _fuera,
             str(_fuera))

# los presupuestos declarados en los escenarios
for fichero, v_tex in [("tuning/scenario.txt", 330),
                       ("tuning/scenario_serious.txt", 300)]:
    txt = open(fichero, encoding="utf-8").read()
    m = re.search(r"maxExperiments\s*=\s*(\d+)", txt)
    check_exacto(f"{fichero.split('/')[-1]}: presupuesto {v_tex}",
                 m and int(m.group(1)) == v_tex,
                 m.group(1) if m else "?")

print(f"\n{ok_n} comprobaciones correctas, {fallo_n} fallos, "
      f"{pend_n} pendientes de fuente")
