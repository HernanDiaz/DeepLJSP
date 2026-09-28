# -*- coding: utf-8 -*-
"""Despacho con una regla GP compilada a una sola funcion de Python.

fast_sim.despacha calcula en cada paso los nueve terminales de todos los
elegibles, los guarda en listas dentro de un diccionario y evalua el
arbol creando una lista intermedia por nodo. Aqui el arbol se traduce a
codigo fuente y se genera un despachador que:

  - guarda por trabajo los terminales de su operacion siguiente (PT,
    PTW, WKR, WKRW, NOR y la maquina) y solo los actualiza para el
    trabajo despachado, porque los de los demas no cambian;
  - en cada paso calcula con listas por comprension el inicio mas
    temprano de los elegibles y el valor del arbol, escrito como una
    unica expresion, y despacha el primer minimo;
  - calcula solo los terminales que el arbol lee.

El resultado tiene que ser IDENTICO al de fast_sim.despacha con
prioridad_de(arbol): mismas operaciones de coma flotante en el mismo
orden (incluida la division protegida), mismo desempate (gana el primer
elegible, como min() y list.index, que recorren igual que el bucle de
prioridad_de), y el mismo consumo del generador aleatorio con eps > 0,
de modo que el mejor-de-N da los mismos schedules con la misma semilla.
tests/test_fast_regla.py lo comprueba schedule a schedule.

Modulo NUEVO: no modifica nada del codigo existente.
"""
from jobshop_rl.heuristics.fast_sim import TERMINALES

# cada terminal para el elegible j; a y b son su inicio mas temprano
# inferior y superior, y base el minimo de b sobre los elegibles
_TERMINAL = {
    "PT": "pt_[j]",
    "PTW": "ptw_[j]",
    "EST": "b",
    "ESTW": "(b - a)",
    "WKR": "wkr_[j]",
    "WKRW": "wkrw_[j]",
    "NOR": "nor_[j]",
    "SLACK": "(b - base)",
    "ONE": "1.0",
}
# como se recalcula el terminal guardado cuando el trabajo j pasa a su
# operacion k; los mismos calculos que fast_sim.despacha
_ACTUALIZA = {
    "PT": "pt_[j] = up[j][k]",
    "PTW": "ptw_[j] = up[j][k] - lo[j][k]",
    "WKR": "wkr_[j] = suf_up[j][k + 1]",
    "WKRW": "wkrw_[j] = suf_w[j][k + 1]",
    "NOR": "nor_[j] = float(m - k - 1)",
}


def _terminales(arbol, usados):
    if isinstance(arbol, str):
        usados.add(arbol)
    else:
        for hijo in arbol[1:]:
            _terminales(hijo, usados)
    return usados


def _expresion(arbol, cont):
    """El arbol como una sola expresion de Python. Los nodos que leen un
    operando dos veces (min, max, div) lo nombran con := para no
    evaluarlo dos veces."""
    if isinstance(arbol, str):
        return _TERMINAL[arbol]
    op = arbol[0]
    x = _expresion(arbol[1], cont)
    if op == "neg":
        return f"(-{x})"
    y = _expresion(arbol[2], cont)
    if op in ("add", "sub", "mul"):
        return f"({x} {dict(add='+', sub='-', mul='*')[op]} {y})"
    cont[0] += 1
    u, w = f"_x{cont[0]}", f"_y{cont[0]}"
    if op == "div":
        # la division protegida de gp_rule: abs(y) > 1e-9, o 1.0
        return (f"({x} / ({w} if (({w} := {y}) > 1e-9 or {w} < -1e-9)"
                f" else 1.0))")
    if op == "min":
        return f"({u} if ({u} := {x}) < ({w} := {y}) else {w})"
    if op == "max":
        return f"({u} if ({u} := {x}) > ({w} := {y}) else {w})"
    raise ValueError(op)


def fuente(arbol):
    """El codigo fuente del despachador de un arbol."""
    usados = _terminales(arbol, set())
    desconocidos = usados - set(TERMINALES)
    if desconocidos:
        raise ValueError(f"terminales desconocidos: {sorted(desconocidos)}")
    guardados = [t for t in TERMINALES if t in _ACTUALIZA and t in usados]
    expr = _expresion(arbol, [0])
    usa_a = "ESTW" in usados
    usa_b = bool(usados & {"EST", "ESTW", "SLACK"})

    src = [
        "def despacha(inst, orden=False, eps=0.0, rng=None):",
        "    n, m, seq, lo, up = inst.n, inst.m, inst.seq, inst.lo, inst.up",
        "    suf_up, suf_w = inst.suf_up, inst.suf_w",
        "    jc_lo, jc_up = [0.0] * n, [0.0] * n",
        "    mc_lo, mc_up = [0.0] * m, [0.0] * m",
        "    op = [0] * n",
        "    perm = []",
        "    elig = list(range(n))",
        "    maq_ = [seq[j][0] for j in range(n)]",
    ]
    for t in guardados:
        src.append(f"    {t.lower()}_ = [0.0] * n")
    if guardados:
        src += ["    k = 0",
                "    for j in range(n):"]
        src += ["        " + _ACTUALIZA[t] for t in guardados]
    src += [
        "    for _ in range(n * m):",
        "        if eps > 0.0 and rng.random() < eps:",
        "            i = rng.randrange(len(elig))",
        "        else:",
    ]
    iters = ["j"]
    if usa_b:
        src.append("            bs = [jc_up[j] if jc_up[j] > mc_up[maq_[j]]"
                   " else mc_up[maq_[j]] for j in elig]")
        iters.append("b")
    if usa_a:
        src.append("            as_ = [jc_lo[j] if jc_lo[j] > mc_lo[maq_[j]]"
                   " else mc_lo[maq_[j]] for j in elig]")
        iters.append("a")
    if "SLACK" in usados:
        src.append("            base = min(bs)")
    fuentes = {"j": "elig", "b": "bs", "a": "as_"}
    if len(iters) == 1:
        bucle = "for j in elig"
    else:
        bucle = (f"for {', '.join(iters)} in "
                 f"zip({', '.join(fuentes[v] for v in iters)})")
    src += [f"            vs = [{expr} {bucle}]",
            "            i = vs.index(min(vs))"]
    src += [
        "        j = elig[i]",
        "        k = op[j]",
        "        q = maq_[j]",
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
        "            maq_[j] = seq[j][k]",
    ]
    src += ["            " + _ACTUALIZA[t] for t in guardados]
    src += ["    cm = (max(jc_lo), max(jc_up))",
            "    return (cm, perm) if orden else cm"]
    return "\n".join(src) + "\n"


def despachador(arbol):
    """Compila un arbol a despacha(inst, orden=False, eps=0.0, rng=None),
    con la misma firma y el mismo resultado que fast_sim.despacha con
    prioridad_de(arbol)."""
    espacio = {}
    exec(compile(fuente(arbol), "<regla compilada>", "exec"), espacio)
    return espacio["despacha"]


def mejor_de_n(inst, desp, semilla, limite_s, eps=0.1, estado=None,
               con_estado=False):
    """El mejor-de-N de una regla compilada, parado por tiempo.

    La misma logica que scripts/e6_extension2.bon_por_tiempo: la muestra
    0 es la pasada determinista, las demas despachan con probabilidad
    eps un elegible al azar, y la curva anota el mejor makespan
    (criterio lexicografico) en cada potencia de dos y en la ultima
    muestra, con los segundos transcurridos.

    Con con_estado=True devuelve tambien el estado al pararse; pasandolo
    como `estado` con un limite_s mayor (contado desde el principio de
    la corrida), sigue exactamente donde se paro."""
    import random
    import time
    from jobshop_rl.heuristics.fast_sim import mejor
    rng = random.Random(semilla)
    if estado is None:
        t0 = time.time()
        mejor_cm = desp(inst)                      # muestra 0: determinista
        curva, k = {1: (mejor_cm, time.time() - t0)}, 1
    else:
        rng.setstate(estado["rng"])
        curva, k = dict(estado["curva"]), estado["k"]
        mejor_cm = estado["mejor_cm"]
        t0 = time.time() - estado["segundos"]
    while time.time() - t0 < limite_s:
        cm = desp(inst, eps=eps, rng=rng)
        k += 1
        if mejor(cm, mejor_cm):
            mejor_cm = cm
        if k & (k - 1) == 0:
            curva[k] = (mejor_cm, time.time() - t0)
    fin = time.time() - t0
    est = None
    if con_estado:
        est = {"rng": rng.getstate(), "curva": dict(curva), "k": k,
               "mejor_cm": mejor_cm, "segundos": fin}
    curva[k] = (mejor_cm, fin)
    return (curva, est) if con_estado else curva
