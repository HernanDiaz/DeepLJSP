# -*- coding: utf-8 -*-
"""Copia congelada de la implementacion de E6 ANTERIOR a la optimizacion
(commit f6035d4): el decodificador de fast_sim y el genetico de
ga_interval tal como produjeron las primeras curvas. Solo la usan los
tests, para comprobar que la version optimizada da lo mismo.
"""
import random
import time

from jobshop_rl.heuristics.fast_sim import _makespan, mejor


def decodifica(inst, perm):
    """Decodifica una permutacion con repeticion de trabajos.

    La k-esima aparicion del trabajo j es su k-esima operacion, asi que
    recorrer la lista de izquierda a derecha respeta el orden del trabajo
    sin comprobaciones.
    """
    n, m, seq, lo, up = inst.n, inst.m, inst.seq, inst.lo, inst.up
    jc_lo, jc_up = [0.0] * n, [0.0] * n
    mc_lo, mc_up = [0.0] * m, [0.0] * m
    op = [0] * n
    for j in perm:
        k = op[j]
        q = seq[j][k]
        s_lo = jc_lo[j] if jc_lo[j] > mc_lo[q] else mc_lo[q]
        s_up = jc_up[j] if jc_up[j] > mc_up[q] else mc_up[q]
        e_lo = s_lo + lo[j][k]
        e_up = s_up + up[j][k]
        jc_lo[j] = mc_lo[q] = e_lo
        jc_up[j] = mc_up[q] = e_up
        op[j] = k + 1
    return _makespan(jc_lo, jc_up)


def aleatoria(inst, rng):
    perm = [j for j in range(inst.n) for _ in range(inst.m)]
    rng.shuffle(perm)
    return perm


def jox(p1, p2, n, rng):
    """Job Order Crossover: un subconjunto de trabajos conserva sus
    posiciones del primer padre, el resto se rellena con el orden en que
    aparecen en el segundo."""
    conserva = {j for j in range(n) if rng.random() < 0.5}
    hijo = [j if j in conserva else None for j in p1]
    resto = [j for j in p2 if j not in conserva]
    k = 0
    for i, v in enumerate(hijo):
        if v is None:
            hijo[i] = resto[k]
            k += 1
    return hijo


def muta(perm, rng):
    """Intercambio de dos posiciones: cualquier permutacion con
    repeticion es factible, asi que no hace falta reparar."""
    i, j = rng.randrange(len(perm)), rng.randrange(len(perm))
    perm[i], perm[j] = perm[j], perm[i]


def evoluciona(inst, presupuesto, rng, pop=250, torneo=3, p_cruce=0.9,
               p_muta=0.2, elite=2, siembra=None, puntos=None,
               limite_s=None):
    # pop=250 es la poblacion del genetico publicado para el IJSP, y es
    # ademas la mejor de las cuatro configuraciones que se probaron a
    # presupuesto alto (scripts/e6_calibra_ga.py): a 200.000
    # decodificaciones llega a 13.4 de RE en TA11 contra 20.4 con 100.
    """Corre el genetico hasta agotar `presupuesto` decodificaciones.

    Devuelve {evaluaciones: (mejor makespan, segundos)} en los `puntos`
    pedidos, de modo que una sola tirada da la curva entera y su coste
    en reloj, que es la segunda moneda de la comparacion.

    Con limite_s se para tambien al agotar ese tiempo, y entonces no se
    rellenan los puntos no alcanzados: la curva acaba en el ultimo que
    se midio, mas un punto final en las evaluaciones hechas.
    """
    puntos = sorted(puntos or [presupuesto])
    t0 = time.time()
    curva, usadas = {}, 0
    poblacion = []
    if siembra is not None:
        poblacion.append(list(siembra))
    while len(poblacion) < pop:
        poblacion.append(aleatoria(inst, rng))

    mejor_cm = None

    def agotado():
        return usadas >= presupuesto or (
            limite_s is not None and time.time() - t0 >= limite_s)

    def anota(cm):
        nonlocal mejor_cm, usadas
        usadas += 1
        if mejor_cm is None or mejor(cm, mejor_cm):
            mejor_cm = cm
        while puntos and usadas >= puntos[0]:
            curva[puntos.pop(0)] = (mejor_cm, time.time() - t0)

    puntuada = []
    for ind in poblacion:
        cm = decodifica(inst, ind)
        anota(cm)
        puntuada.append((cm, ind))
        if agotado():
            break

    while not agotado():
        puntuada.sort(key=lambda x: (x[0][1], x[0][0]))
        nueva = [p for p in puntuada[:elite]]
        while len(nueva) < pop and not agotado():
            a = min((puntuada[rng.randrange(len(puntuada))]
                     for _ in range(torneo)), key=lambda x: (x[0][1], x[0][0]))
            b = min((puntuada[rng.randrange(len(puntuada))]
                     for _ in range(torneo)), key=lambda x: (x[0][1], x[0][0]))
            hijo = (jox(a[1], b[1], inst.n, rng) if rng.random() < p_cruce
                    else list(a[1]))
            if rng.random() < p_muta:
                muta(hijo, rng)
            cm = decodifica(inst, hijo)
            anota(cm)
            nueva.append((cm, hijo))
        puntuada = nueva

    if limite_s is not None:    # parado por tiempo: el ultimo punto real
        curva[usadas] = (mejor_cm, time.time() - t0)
        return curva, mejor_cm
    for p in puntos:            # por si el presupuesto acabo antes
        curva[p] = (mejor_cm, time.time() - t0)
    return curva, mejor_cm


def azar(inst, presupuesto, rng, puntos=None, limite_s=None):
    """Muestreo uniforme de permutaciones: el suelo contra el que se mide
    cualquier busqueda, con el mismo decodificador.

    Con `limite_s` se para tambien al agotar ese tiempo, sin rellenar los
    puntos no alcanzados, como en evoluciona."""
    puntos = sorted(puntos or [presupuesto])
    t0 = time.time()
    curva, mejor_cm = {}, None
    for k in range(1, presupuesto + 1):
        cm = decodifica(inst, aleatoria(inst, rng))
        if mejor_cm is None or mejor(cm, mejor_cm):
            mejor_cm = cm
        while puntos and k >= puntos[0]:
            curva[puntos.pop(0)] = (mejor_cm, time.time() - t0)
        if limite_s is not None and time.time() - t0 >= limite_s:
            curva[k] = (mejor_cm, time.time() - t0)
            return curva, mejor_cm
    for p in puntos:
        curva[p] = (mejor_cm, time.time() - t0)
    return curva, mejor_cm
