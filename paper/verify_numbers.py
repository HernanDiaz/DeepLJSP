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

# la frase estadistica de 6.6: greedy gana a MOR, EST y G&T en las 70
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
TAB_INSIZE = {
    "v2-full":        {"TA15": (34.1, 31.9), "TA16": (26.8, 22.8),
                       "TA17": (28.2, 24.9), "TA18": (26.2, 24.9),
                       "TA19": (29.2, 24.1), "TA20": (24.3, 22.4)},
    "v2-full-300ep":  {"TA15": (18.7, 17.1), "TA16": (16.1, 15.4),
                       "TA17": (14.6, 13.3), "TA18": (16.9, 16.4),
                       "TA19": (16.3, 15.5), "TA20": (16.8, 16.1)},
    "v2-full-1000ep": {"TA15": (13.7, 12.1), "TA16": (12.6, 11.8),
                       "TA17": (13.0, 11.8), "TA18": (15.9, 14.6),
                       "TA19": (12.1, 11.6), "TA20": (13.4, 12.2)},
}
MEDIAS = {"v2-full": 28.1, "v2-full-300ep": 16.6, "v2-full-1000ep": 13.4}
delta_max = 0.0
for tag, celdas in TAB_INSIZE.items():
    datos = bench_por_instancia(tag)
    if datos is None:
        pendiente(f"benchmark {tag}", "sin directorios en outputs/")
        continue
    res_mean, res_best = {}, {}
    for ta, d in datos.items():
        res_mean[ta] = re_pct(sum(d["mids"]) / len(d["mids"]), ta)
        res_best[ta] = re_pct(min(d["mids"]), ta)
        lex_mean = re_pct(sum(d["lex"]) / len(d["lex"]), ta)
        delta_max = max(delta_max, abs(res_mean[ta] - lex_mean))
    for ta, (m_tex, b_tex) in celdas.items():
        check(f"{tag} {ta} media", m_tex, res_mean[ta])
        check(f"{tag} {ta} mejor", b_tex, res_best[ta])
    media = sum(res_mean.values()) / len(res_mean)
    check(f"{tag}: media de la fila (texto {MEDIAS[tag]})",
          MEDIAS[tag], media)
print(f"  nota: delta maximo lex vs componentwise = {delta_max:.3f} puntos")

# fila MOR de la tabla (viene de constructive_per_instance)
FILA_MOR = {"TA15": 51.3, "TA16": 35.8, "TA17": 50.1,
            "TA18": 54.2, "TA19": 43.2, "TA20": 43.7}
for ta, v in FILA_MOR.items():
    check(f"fila MOR {ta}", v, MOR_RE[ta])

datos1000 = bench_por_instancia("v2-full-1000ep")
if datos1000:
    mejor_media = sum(re_pct(min(d["mids"]), ta)
                      for ta, d in datos1000.items()) / len(datos1000)
    check("mejor semilla a 1000 eps (abstract 12.3)", 12.3, mejor_media)
    factor = mor_dev / (sum(re_pct(sum(d["mids"]) / len(d["mids"]), ta)
                            for ta, d in datos1000.items()) / len(datos1000))
    check_exacto("factor ~3.5 frente a MOR", 3.3 <= factor <= 3.7,
                 f"{factor:.2f}")
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

# +1.2% / +1.6% de makespan medio (pareado por instancia y semilla)
for tag_a, tag_b, delta_tex in [("v2-full-300ep", "v2-attn-300ep", 0.9),
                                ("v2-full-1000ep", "v2-attn-1000ep", 1.5)]:
    da, db = bench_por_instancia(tag_a), bench_por_instancia(tag_b)
    if da and db:
        base = sum(sum(d["mids"]) for d in da.values())
        attn = sum(sum(d["mids"]) for d in db.values())
        check(f"makespan medio {tag_b} vs base (texto +{delta_tex}%)",
              delta_tex, (attn / base - 1) * 100, tol=0.1)

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
check_exacto("bo1024 gana a MOR, G&T y EST en las 70",
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
_dist = [b - f for b, f in zip(_bo_clases, feabc_clases)]
check("distancia minima al fEABC (texto 2.5)", 2.5, min(_dist))
check("distancia maxima al fEABC (texto 5.1)", 5.1, max(_dist))

# =========================================================================
print("\n== coste computacional ==")
d = json.load(open(sorted(glob.glob(
    "benchmarks/v2-full-1000ep__*.json"))[-1], encoding="utf-8"))
minutos = [s["wall_time_s"] / 60 for s in d["seeds"].values()]
media_min = sum(minutos) / len(minutos)
check_exacto("66-123 min por semilla (4x1000 episodios)",
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
                "Matplotlib": importlib.import_module("matplotlib").__version__}
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
    check_exacto("el elite confirmado no mejora el 13.4 por defecto",
                 media_e > 13.4, f"{media_e:.2f} > 13.4")
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

# =========================================================================
print("\n== tab:crosssize (zero-shot) ==")
CROSS = {"TA1": (13.1, 11.0, 29.7), "TA2": (9.7, 7.0, 34.8),
         "TA5": (10.5, 8.8, 50.7), "TA21": (13.2, 11.1, 40.8),
         "TA25": (15.0, 14.4, 53.2), "TA31": (15.8, 13.9, 34.4),
         "TA41": (25.9, 24.5, 53.5), "TA51": (15.3, 12.9, 38.2),
         "TA61": (16.8, 15.5, 48.7)}
_cs = {}
for r in __import__("csv").DictReader(
        open("benchmarks/eval_crosssize_bo64.csv", encoding="utf-8")):
    _cs.setdefault(ta_de(r["instance"]), []).append(float(r["re_comp"]))
for ta, (media_tex, mejor_tex, mor_tex) in CROSS.items():
    check(f"crosssize {ta} media", media_tex, sum(_cs[ta]) / len(_cs[ta]))
    check(f"crosssize {ta} mejor", mejor_tex, min(_cs[ta]))
    check(f"columna MOR {ta}", mor_tex, MOR_RE[ta])
check_exacto("cada semilla bate a MOR en las 9",
             all(max(_cs[ta]) < MOR_RE[ta] for ta in CROSS))

# la transferencia mejora con el presupuesto (300ep vs 1000ep, medias)
_c300 = {}
for r in __import__("csv").DictReader(
        open("benchmarks/eval_crosssize_bo64_300ep.csv", encoding="utf-8")):
    _c300.setdefault(ta_de(r["instance"]), []).append(float(r["re_comp"]))
_c300 = {ta: sum(v) / len(v) for ta, v in _c300.items()}
check("TA41 con 300 eps (texto 30.3)", 30.3, _c300["TA41"])
check("TA51 con 300 eps (texto 22.2)", 22.2, _c300["TA51"])
check_exacto("mas presupuesto -> mejor transferencia en ambas",
             _c300["TA41"] > sum(_cs["TA41"]) / 3
             and _c300["TA51"] > sum(_cs["TA51"]) / 3)

# =========================================================================
print("\n== robustez ejecucional (eval_eps_policy.csv, x1000) ==")
_eps = {}
for r in __import__("csv").DictReader(
        open("benchmarks/eval_eps_policy.csv", encoding="utf-8")):
    m = r["method"]
    g = ("policy-greedy" if m.startswith("policy-greedy") else
         "policy-bo64" if m.startswith("policy-bo64") else m)
    _eps.setdefault(g, {}).setdefault(r["instance"], []).append(
        float(r["eps"]) * 1000)
_eps = {g: {i: sum(v) / len(v) for i, v in d.items()}
        for g, d in _eps.items()}
# El CSV se regenera por instancias: comprobar contra una tirada a medias
# daria fallos que no son del paper sino del reloj.
_n_eps = len(_eps.get("EST", {}))
if _n_eps < 15:
    pendiente("robustez ejecucional",
              f"eval_eps_policy.csv incompleto ({_n_eps}/15 instancias)")
else:
    for g, v_tex in [("MOR", 7.1), ("GT-MWKR", 6.9), ("EST", 6.3),
                     ("GP", 6.1), ("policy-greedy", 6.2),
                     ("policy-bo64", 6.2)]:
        vals = list(_eps[g].values())
        check(f"eps x1000 {g} (texto {v_tex})", v_tex, sum(vals) / len(vals))
    _ii = sorted(_eps["EST"])
    for g, gana_tex in [("MOR", 15), ("GT-MWKR", 13), ("EST", 8), ("GP", 7)]:
        gana = sum(_eps[g][i] > _eps["policy-bo64"][i] for i in _ii)
        check_exacto(f"la politica es mas fiel que {g} en {gana_tex}/15",
                     gana == gana_tex, f"{gana}/15")
    try:
        from scipy import stats as _st
        for g, lo, hi, etiq in [("MOR", 0, 1e-3, "p<0.001"),
                                ("GT-MWKR", 2e-3, 4e-3, "p=0.003"),
                                ("EST", 0.55, 0.65, "p=0.60"),
                                ("GP", 0.93, 1.01, "p=0.98")]:
            d = [_eps[g][i] - _eps["policy-bo64"][i] for i in _ii]
            p = _st.wilcoxon(d)[1]
            check_exacto(f"eps frente a {g} ({etiq})", lo <= p <= hi,
                         f"p={p:.3f}")
        # la afirmacion de fondo: el GP y la politica, indistinguibles
        check_exacto("GP y politica empatados en cabeza",
                     abs(sum(_eps["GP"].values()) / 15
                         - sum(_eps["policy-bo64"].values()) / 15) < 0.15,
                     "diferencia < 0.15")
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
TAB_CLASSICS = {
    "FT10": (32.6, 41.8, 32.2, 8.5, 6.3, 5.2, 4.1, 3.5, 3.0),
    "FT20": (27.7, 43.5, 40.0, 5.8, 4.4, 4.4, 1.7, 1.8, 1.8),
    "La21": (40.2, 48.7, 24.1, 12.6, 10.4, 5.0, 5.0, 4.2, 4.0),
    "La24": (42.2, 34.3, 26.3, 11.9, 10.9, 6.3, 5.1, 4.9, 5.0),
    "La25": (36.6, 47.4, 16.9, 9.6, 9.2, 5.1, 3.9, 3.4, 2.7),
    "La27": (47.2, 45.0, 34.8, 11.3, 10.9, 10.2, 4.7, 4.6, 4.1),
    "La29": (47.9, 46.4, 24.5, 16.6, 14.0, 14.2, 8.6, 7.4, 7.0),
    "La38": (54.8, 47.7, 27.0, 12.8, 11.7, 9.2, 6.9, 6.1, 5.8),
    "La40": (20.9, 41.6, 27.9, 9.3, 8.1, 8.7, 4.2, 4.6, 4.1),
    "ABZ7": (51.6, 36.1, 28.7, 13.4, 12.0, 12.5, 7.3, 6.6, 6.7),
    "ABZ8": (43.0, 57.7, 36.9, 17.3, 16.9, 18.5, 12.1, 11.1, 10.9),
    "ABZ9": (42.7, 59.0, 41.8, 19.2, 18.8, 18.0, 13.1, 11.6, 11.2),
}
fallos_clas = 0
for inst, fila in TAB_CLASSICS.items():
    c = _clas[inst]
    reales = (_est12[inst], float(c["mor"]), float(c["gt"]),
              sum(_pol12[inst]) / len(_pol12[inst]), min(_pol12[inst]),
              float(c["GA"]), float(c["ABCE3"]), float(c["fEABC"]),
              float(c["ESABC"]))
    for v_tex, v_dat in zip(fila, reales):
        if abs(v_tex - v_dat) > 0.051:
            print(f"  FALLO celda {inst}: texto={v_tex} datos={v_dat:.2f}")
            fallos_clas += 1
check_exacto("las 108 celdas de tab:classics", fallos_clas == 0,
             f"{fallos_clas} celdas mal")
_medias_pol = [sum(v) / len(v) for v in _pol12.values()]
check("clasicas: politica media (texto 12.4)", 12.4,
      sum(_medias_pol) / 12)
check("clasicas: G&T media (texto 30.1)", 30.1,
      sum(float(c["gt"]) for c in _clas.values()) / 12)
for col, v_tex in [("GA", 9.8), ("fEABC", 5.8), ("ESABC", 5.5)]:
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
_imp = {r["feature"]: float(r["delta_puntos"])
        for r in __import__("csv").DictReader(
            open("benchmarks/feature_importance.csv", encoding="utf-8"))}
_base = float(next(__import__("csv").DictReader(
    open("benchmarks/feature_importance.csv",
         encoding="utf-8")))["re_base"])
check("base greedy del test (texto 18.2)", 18.2, _base)
for f, v_tex in [("holgura", 51.0), ("pos_restante", 28.1),
                 ("rem_up", 10.6), ("dur_up", 3.9)]:
    check(f"permutar {f} (texto +{v_tex})", v_tex, _imp[f], tol=0.06)
check_exacto("las features de anchura no aportan (|delta|<=0.5)",
             abs(_imp["dur_width_rel"]) <= 0.5
             and abs(_imp["est_width_rel"]) <= 0.5,
             f"{_imp['dur_width_rel']:+.2f} / {_imp['est_width_rel']:+.2f}")

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


print("\n== delimitacion de la conciencia intervalar ==")


def _por_par(tag):
    """{(TA, semilla): RE} de una campaña, componentwise."""
    out = {}
    for d in sorted(glob.glob(f"outputs/bench_{tag}__*_seed*")):
        s = d.split("_seed")[-1]
        for p in glob.glob(f"{d}/plots/test/*_schedule.json"):
            ta = ta_de(os.path.basename(p))
            out[(ta, s)] = re_pct(makespans(p)[0], ta)
    return out


_full = _por_par("v2-full-1000ep")
_nw = _por_par("v2-nowidth-1000ep-b")
_mp = _por_par("v2-midpoint-1000ep-b")
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
            check_exacto("no-width: peor en 12 de 18", peor == 12,
                         f"{peor}/18")
            check_exacto("no-width: no significativo (texto p=0.47)",
                         0.44 <= p <= 0.50, f"p={p:.3f}")
        else:
            check_exacto("punto medio: no significativo (texto p=0.28)",
                         0.25 <= p <= 0.31, f"p={p:.3f}")
    except ImportError:
        pendiente(f"Wilcoxon {nombre}", "sin scipy")
check("brazo principal de referencia (texto 13.44)", 13.44,
      sum(_full.values()) / len(_full))


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
