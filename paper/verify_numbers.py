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
en_tex("$29.4\\%$ mean RE")
check("G&T-MWKR sobre las 70 (texto 29.4)", 29.4, ab["G&T-MWKR"])
check("MOR sobre las 70 (texto 45.4)", 45.4, ab["MOR"])
check("G&T-SPT sobre las 70 (texto 70.6)", 70.6, ab["G&T-SPT"])
if ab["EST"] < ab["MOR"]:
    print(f"  AVISO EST ({ab['EST']:.1f}) < MOR ({ab['MOR']:.1f}): 'MOR is "
          "uniformly the strongest' vale solo dentro de {SPT,LPT,MOR,MWKR}")

DEV = [f"TA{k}" for k in range(15, 21)]
mor_dev = sum(MOR_RE[t] for t in DEV) / len(DEV)
check("MOR medio en desarrollo (abstract ~46)", 46.0, mor_dev, tol=0.55)

# =========================================================================
print("\n== tab:insize: recomputo desde schedules (componentwise) ==")
TAB_INSIZE = {
    "v2-full":        {"TA15": (34.1, 31.9), "TA16": (26.8, 22.8),
                       "TA17": (28.1, 24.8), "TA18": (26.2, 24.9),
                       "TA19": (28.9, 24.1), "TA20": (24.0, 21.6)},
    "v2-full-300ep":  {"TA15": (18.7, 17.1), "TA16": (16.1, 15.4),
                       "TA17": (13.5, 12.3), "TA18": (16.9, 16.4),
                       "TA19": (16.3, 15.5), "TA20": (16.8, 16.1)},
    "v2-full-1000ep": {"TA15": (13.6, 12.1), "TA16": (12.5, 11.8),
                       "TA17": (13.0, 11.8), "TA18": (15.9, 14.6),
                       "TA19": (12.0, 11.6), "TA20": (13.4, 12.0)},
}
MEDIAS = {"v2-full": 28.0, "v2-full-300ep": 16.4, "v2-full-1000ep": 13.4}
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
            "TA18": 54.3, "TA19": 43.2, "TA20": 43.7}
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
    check_exacto("std de makespan por instancia 10-24 unidades",
                 8.0 <= min(stds) and max(stds) <= 26.0,
                 f"rango {min(stds):.0f}-{max(stds):.0f}")

# =========================================================================
print("\n== tab:insize-attn ==")
TAB_ATTN = {"v2-attn-300ep": (17.5, 16.1), "v2-attn-1000ep": (15.0, 13.9)}
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
for tag_a, tag_b, delta_tex in [("v2-full-300ep", "v2-attn-300ep", 1.2),
                                ("v2-full-1000ep", "v2-attn-1000ep", 1.6)]:
    da, db = bench_por_instancia(tag_a), bench_por_instancia(tag_b)
    if da and db:
        base = sum(sum(d["mids"]) for d in da.values())
        attn = sum(sum(d["mids"]) for d in db.values())
        check(f"makespan medio {tag_b} vs base (texto +{delta_tex}%)",
              delta_tex, (attn / base - 1) * 100, tol=0.1)

# =========================================================================
print("\n== especialista vs multi-tamano ==")
ESPECIALISTA = {"TA5": 8.7, "TA25": 15.9, "TA31": 13.9,
                "TA41": 24.5, "TA61": 15.1}  # tab:crosssize
CLAIM_12K = {"TA5": 9.5, "TA25": 18.5, "TA41": 28.3}
for etiqueta, patron in [("matched-total (3000)", "benchmarks/v2-multisize_seed*.json"),
                         ("matched-per-instance (12k)", "benchmarks/v2-multisize-12k_seed*.json")]:
    ficheros = sorted(glob.glob(patron))
    if not ficheros:
        pendiente(etiqueta, "sin registros")
        continue
    acum = {}
    for f in ficheros:
        d = json.load(open(f, encoding="utf-8"))
        for inst, r in d["results"].items():
            ta = ta_de(inst)
            lb = r.get("lower_bound_lit") or LB[ta]
            acum.setdefault(ta, []).append((r["rl_makespan"] - lb) / lb * 100)
    medias = {ta: sum(v) / len(v) for ta, v in acum.items()}
    if "12k" in patron:
        # los registros guardan el mejor makespan de ENTRENAMIENTO; las
        # celdas del texto (9.5/18.5/28.3) salieron de una evaluacion
        # best-of-64 de los checkpoints que no quedo registrada
        for ta, v_tex in CLAIM_12K.items():
            pendiente(f"multi-12k {ta} (texto {v_tex})",
                      f"registro de entrenamiento da {medias[ta]:.1f}; "
                      "falta la eval bo64")
    comunes = [ta for ta in ESPECIALISTA if ta in medias]
    gana = [ta for ta in comunes if ESPECIALISTA[ta] < medias[ta]]
    check_exacto(f"{etiqueta}: especialista gana en las {len(comunes)} comunes",
                 len(gana) == len(comunes),
                 f"gana {len(gana)}/{len(comunes)}")

# =========================================================================
print("\n== presupuesto de inferencia y posicionamiento ==")
filas = open("benchmarks/fair_v2_greedy.csv",
             encoding="utf-8").read().splitlines()[1:]
vals = [float(l.split(",")[3]) for l in filas]
check("politica greedy sobre las 70 (texto 19.4)", 19.4,
      sum(vals) / len(vals))
pendiente("best-of-1024 = 12.7 sobre las 70",
          "sin CSV localizado (solo fair_gp_eps.csv, que es del GP)")
pendiente("a 2.2-4.6 puntos del fEABC por clase",
          "necesita las medias por clase de fEABC y el bo1024 por clase")

# =========================================================================
print("\n== coste computacional ==")
d = json.load(open(sorted(glob.glob(
    "benchmarks/v2-full-1000ep__*.json"))[-1], encoding="utf-8"))
minutos = [s["wall_time_s"] / 60 for s in d["seeds"].values()]
media_min = sum(minutos) / len(minutos)
check_exacto("~80 min por semilla (4x1000 episodios)",
             70 <= media_min <= 90,
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
pendiente("14.73 vs 13.52 (campana 2, elite #22)",
          "registro del elite 22 no localizado en benchmarks/")
pendiente("330 y 300 experimentos de las dos campanas",
          "contar en tuning/ (rdata_backups, runner_logs)")

# =========================================================================
print("\n== tab:crosssize (zero-shot) ==")
CROSS = {"TA1": (14.4, 29.7), "TA2": (7.0, 34.8), "TA5": (8.7, 50.7),
         "TA21": (9.6, 40.8), "TA25": (15.9, 53.2), "TA31": (13.9, 34.4),
         "TA41": (24.5, 53.5), "TA51": (25.0, 38.2), "TA61": (15.1, 48.7)}
for ta, (pol, mor) in CROSS.items():
    check(f"columna MOR {ta}", mor, MOR_RE[ta])
gana_todas = all(pol < mor for pol, mor in CROSS.values())
check_exacto("la politica bate a MOR en las 9 de la tabla", gana_todas)
pendiente("columna Policy de tab:crosssize",
          "sin registro guardado; recomputar requiere rerun de "
          "eval_v2_crosssize con los checkpoints (best-of-64)")

# =========================================================================
print(f"\n{ok_n} comprobaciones correctas, {fallo_n} fallos, "
      f"{pend_n} pendientes de fuente")
