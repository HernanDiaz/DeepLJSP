# -*- coding: utf-8 -*-
"""Los baselines de la tabla 6.2, escritos como la regla compilada.

scripts/tiempos_fast.py los implementa como politicas de
fast_sim.despacha: en cada paso se calculan los nueve terminales de todos
los elegibles y la politica los recorre. Para que la tabla de tiempos
compare reglas implementadas con el mismo cuidado que la regla evolucionada
(fast_regla), aqui cada baseline es un despachador propio que

  - guarda por trabajo los datos de su operacion siguiente (maquina,
    duracion superior e inferior, trabajo restante superior e inferior,
    operaciones restantes) y solo los actualiza para el trabajo
    despachado;
  - en cada paso calcula con listas por comprension las claves que lee
    y elige con min o max y list.index.

Las claves son las mismas tuplas (superior, inferior) de tiempos_fast.py
con la misma aritmetica, y la comparacion de tuplas de Python es
exactamente su orden lexicografico. min y max recorren igual que _arg
(se quedan con el primero en caso de empate, max tambien), y list.index
devuelve el primer elegible con ese valor, asi que el schedule es el
mismo operacion a operacion; tests/test_fast_baselines.py lo comprueba.

Modulo NUEVO: no modifica nada del codigo existente.
"""

# lo que cada baseline hace en un paso no aleatorio; deja en i el indice
# del elegible elegido
_ELIGE = {
    "SPT": ["vs = [(pt_[j], ptl_[j]) for j in elig]",
            "i = vs.index(min(vs))"],
    "LPT": ["vs = [(pt_[j], ptl_[j]) for j in elig]",
            "i = vs.index(max(vs))"],
    "EST": ["bs = [jc_up[j] if jc_up[j] > mc_up[mach_[j]] else mc_up[mach_[j]] for j in elig]",
            "as_ = [jc_lo[j] if jc_lo[j] > mc_lo[mach_[j]] else mc_lo[mach_[j]] for j in elig]",
            "vs = list(zip(bs, as_))",
            "i = vs.index(min(vs))"],
    "MWKR": ["vs = [(wkr_[j], wkrl_[j]) for j in elig]",
             "i = vs.index(max(vs))"],
    "MOR": ["vs = [nor_[j] for j in elig]",
            "i = vs.index(max(vs))"],
    "CR": ["vs = [wkr_[j] / (nor_[j] + 1e-10) for j in elig]",
           "i = vs.index(min(vs))"],
}
# Giffler y Thompson: el conflict set de la maquina del menor fin, y dentro
# el desempate SPT (min) o MWKR (max)
_GT = ["bs = [jc_up[j] if jc_up[j] > mc_up[mach_[j]] else mc_up[mach_[j]] for j in elig]",
       "as_ = [jc_lo[j] if jc_lo[j] > mc_lo[mach_[j]] else mc_lo[mach_[j]] for j in elig]",
       "fins = [(b + pt_[j], a + ptl_[j]) for j, b, a in zip(elig, bs, as_)]",
       "c = fins.index(min(fins))",
       "fc, mq = fins[c], mach_[elig[c]]",
       "conf = [x for x, (j, b, a) in enumerate(zip(elig, bs, as_))"
       " if mach_[j] == mq and (b, a) < fc]",
       "if not conf:",
       "    conf = [c]"]
_ELIGE["G&T-SPT"] = _GT + [
    "ks = [(pt_[elig[x]], ptl_[elig[x]]) for x in conf]",
    "i = conf[ks.index(min(ks))]"]
_ELIGE["G&T-MWKR"] = _GT + [
    "ks = [(wkr_[elig[x]], wkrl_[elig[x]]) for x in conf]",
    "i = conf[ks.index(max(ks))]"]
# lo que se guarda por trabajo, recalculado al pasar a su operacion k: la
# misma aritmetica que las claves de tiempos_fast.py
_ACTUALIZA = ["pt_[j] = up[j][k]",
              "ptl_[j] = up[j][k] - (up[j][k] - lo[j][k])",
              "wkr_[j] = suf_up[j][k + 1]",
              "wkrl_[j] = suf_up[j][k + 1] - suf_w[j][k + 1]",
              "nor_[j] = float(m - k - 1)"]
METODOS = tuple(_ELIGE)


def fuente(metodo):
    eleccion = _ELIGE[metodo]
    src = [
        "def despacha(inst, orden=False, eps=0.0, rng=None):",
        "    n, m, seq, lo, up = inst.n, inst.m, inst.seq, inst.lo, inst.up",
        "    suf_up, suf_w = inst.suf_up, inst.suf_w",
        "    jc_lo, jc_up = [0.0] * n, [0.0] * n",
        "    mc_lo, mc_up = [0.0] * m, [0.0] * m",
        "    op = [0] * n",
        "    perm = []",
        "    elig = list(range(n))",
        "    mach_ = [seq[j][0] for j in range(n)]",
        "    pt_, ptl_, wkr_, wkrl_, nor_ = ([0.0] * n for _ in range(5))",
        "    k = 0",
        "    for j in range(n):",
    ]
    src += ["        " + s for s in _ACTUALIZA]
    src += [
        "    for _ in range(n * m):",
        "        if eps > 0.0 and rng.random() < eps:",
        "            i = rng.randrange(len(elig))",
        "        else:",
    ]
    src += ["            " + s for s in eleccion]
    src += [
        "        j = elig[i]",
        "        k = op[j]",
        "        q = mach_[j]",
        "        a = jc_lo[j] if jc_lo[j] > mc_lo[q] else mc_lo[q]",
        "        b = jc_up[j] if jc_up[j] > mc_up[q] else mc_up[q]",
        "        jc_lo[j] = mc_lo[q] = a + lo[j][k]",
        "        jc_up[j] = mc_up[q] = b + up[j][k]",
        "        k += 1",
        "        op[j] = k",
        "        perm.append(j)",
        "        if k == m:",
        "            del elig[i]",
        "        else:",
        "            mach_[j] = seq[j][k]",
    ]
    src += ["            " + s for s in _ACTUALIZA]
    src += ["    cm = (max(jc_lo), max(jc_up))",
            "    return (cm, perm) if orden else cm"]
    return "\n".join(src) + "\n"


def despachador(metodo):
    """despacha(inst, orden=False, eps=0.0, rng=None) del baseline, con el
    mismo resultado que fast_sim.despacha con su politica de
    scripts/tiempos_fast.py."""
    espacio = {}
    exec(compile(fuente(metodo), f"<{metodo}>", "exec"), espacio)
    return espacio["despacha"]
