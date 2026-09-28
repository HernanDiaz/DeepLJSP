# -*- coding: utf-8 -*-
"""Algoritmo genetico intervalar sobre permutacion con repeticion.

Es la metaheuristica de referencia de E6, escrita en el mismo lenguaje,
con el mismo decodificador y el mismo evaluador que la regla
evolucionada, que es lo unico que permite responder a la objecion de que
el articulo compara con metaheuristicas publicadas en C++ y con otro
presupuesto. No pretende reproducir cifra por cifra el genetico
publicado para el IJSP~[Diaz et al., IPMU 2020]: reproduce su diseno
--- permutacion con repeticion, cruce por orden de trabajos, seleccion
por torneo, elitismo y comparacion lexicografica del makespan
intervalar --- para poder medir el intercambio entre calidad y
presupuesto dentro de una misma implementacion.

El coste se contabiliza en EVALUACIONES DE SCHEDULE, que es la moneda
independiente de la implementacion, y quien llama mide aparte el reloj.

Modulo NUEVO: no modifica nada del codigo existente.
"""
import random
import time

from jobshop_rl.heuristics.fast_sim import decodifica, mejor


def aleatoria(inst, rng):
    perm = [j for j in range(inst.n) for _ in range(inst.m)]
    rng.shuffle(perm)
    return perm


def jox(p1, p2, n, rng):
    """Job Order Crossover: un subconjunto de trabajos conserva sus
    posiciones del primer padre, el resto se rellena con el orden en que
    aparecen en el segundo."""
    conserva = [rng.random() < 0.5 for _ in range(n)]
    resto = iter([j for j in p2 if not conserva[j]])
    return [j if conserva[j] else next(resto) for j in p1]


def muta(perm, rng):
    """Intercambio de dos posiciones: cualquier permutacion con
    repeticion es factible, asi que no hace falta reparar."""
    i, j = rng.randrange(len(perm)), rng.randrange(len(perm))
    perm[i], perm[j] = perm[j], perm[i]


def evoluciona(inst, presupuesto, rng, pop=250, torneo=3, p_cruce=0.9,
               p_muta=0.2, elite=2, siembra=None, puntos=None,
               limite_s=None, estado=None, con_estado=False):
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

    Con con_estado=True devuelve ademas el estado de la corrida al
    pararse (poblacion, generacion a medias, generador, mejor, reloj).
    Pasandolo como `estado`, con un rng cualquiera (se le restaura el
    estado guardado), la corrida sigue exactamente donde se paro: con un
    presupuesto o un limite_s mayores, que cuentan desde el principio de
    la corrida, da la misma curva que una corrida sin interrumpir.
    """
    if estado is None:
        puntos = sorted(puntos or [presupuesto])
        curva, usadas, mejor_cm, previo = {}, 0, None, 0.0
        poblacion = []
        if siembra is not None:
            poblacion.append(list(siembra))
        while len(poblacion) < pop:
            poblacion.append(aleatoria(inst, rng))
        pendientes, puntuada, nueva = poblacion, [], None
    else:
        rng.setstate(estado["rng"])
        puntos, curva = list(estado["puntos"]), dict(estado["curva"])
        usadas, mejor_cm = estado["usadas"], estado["mejor_cm"]
        previo = estado["segundos"]
        pendientes, puntuada = estado["pendientes"], estado["puntuada"]
        nueva = estado["nueva"]
    t0 = time.time() - previo

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

    # la poblacion inicial, entera generada antes de evaluar nada
    parado = False
    while pendientes:
        ind = pendientes.pop(0)
        cm = decodifica(inst, ind)
        anota(cm)
        puntuada.append((cm, ind))
        if agotado():
            parado = True
            break

    while not parado:
        if nueva is None:               # empieza una generacion
            if agotado():
                break
            puntuada.sort(key=lambda x: (x[0][1], x[0][0]))
            nueva = puntuada[:elite]
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
        if len(nueva) < pop:            # parado a mitad de generacion
            break
        puntuada, nueva = nueva, None

    fin = time.time() - t0
    est = None
    if con_estado:
        est = {"rng": rng.getstate(), "puntos": list(puntos),
               "curva": dict(curva), "usadas": usadas, "mejor_cm": mejor_cm,
               "segundos": fin, "pendientes": pendientes,
               "puntuada": puntuada, "nueva": nueva}
    if limite_s is not None:    # parado por tiempo: el ultimo punto real
        curva[usadas] = (mejor_cm, fin)
    else:
        for p in puntos:        # por si el presupuesto acabo antes
            curva[p] = (mejor_cm, fin)
    return (curva, mejor_cm, est) if con_estado else (curva, mejor_cm)


def azar(inst, presupuesto, rng, puntos=None, limite_s=None, estado=None,
         con_estado=False):
    """Muestreo uniforme de permutaciones: el suelo contra el que se mide
    cualquier busqueda, con el mismo decodificador.

    Con `limite_s` se para tambien al agotar ese tiempo, sin rellenar los
    puntos no alcanzados, como en evoluciona; `estado` y `con_estado`
    permiten continuar una corrida parada, tambien como en evoluciona."""
    if estado is None:
        puntos = sorted(puntos or [presupuesto])
        curva, mejor_cm, k0, previo = {}, None, 0, 0.0
    else:
        rng.setstate(estado["rng"])
        puntos, curva = list(estado["puntos"]), dict(estado["curva"])
        mejor_cm, k0, previo = estado["mejor_cm"], estado["k"], estado["segundos"]
    t0 = time.time() - previo
    k = k0
    parado = False
    for k in range(k0 + 1, presupuesto + 1):
        cm = decodifica(inst, aleatoria(inst, rng))
        if mejor_cm is None or mejor(cm, mejor_cm):
            mejor_cm = cm
        while puntos and k >= puntos[0]:
            curva[puntos.pop(0)] = (mejor_cm, time.time() - t0)
        if limite_s is not None and time.time() - t0 >= limite_s:
            parado = True
            break
    fin = time.time() - t0
    est = None
    if con_estado:
        est = {"rng": rng.getstate(), "puntos": list(puntos),
               "curva": dict(curva), "k": k, "mejor_cm": mejor_cm,
               "segundos": fin}
    if parado:
        curva[k] = (mejor_cm, fin)
    else:
        for p in puntos:
            curva[p] = (mejor_cm, fin)
    return (curva, mejor_cm, est) if con_estado else (curva, mejor_cm)
