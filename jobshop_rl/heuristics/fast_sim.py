# -*- coding: utf-8 -*-
"""Simulador intervalar rapido, compartido por todos los metodos de E6.

La revision r2 objeta, con razon, que el articulo compara la regla
evolucionada con metaheuristicas publicadas en otro lenguaje, con otro
presupuesto y otro proceso de evaluacion. La unica manera de cerrar esa
objecion es medirlo todo con el MISMO decodificador y el MISMO evaluador
en el mismo lenguaje, y eso es lo que hay aqui: un decodificador
semiactivo intervalar sin dependencias del entorno, que sirve tanto para
despachar con una regla de prioridad como para decodificar la
permutacion con repeticion que usa el algoritmo genetico.

Es el mismo decodificador semiactivo del entorno, escrito sin construir
la matriz de features en cada paso, y los tests lo contrastan contra el
entorno operacion a operacion.

Convenios, identicos a los de jobshop_rl/environment/job_shop_env.py:
  - elegibles en orden de trabajo ascendente;
  - WKR y NOR excluyen la operacion en curso;
  - SLACK se mide contra el minimo del extremo superior de los elegibles;
  - makespan COMPONENTE A COMPONENTE, [max de los inferiores, max de los
    superiores];
  - empates de prioridad: gana el primer elegible, como np.argmin.

Modulo NUEVO: no modifica nada del codigo existente.
"""
import numpy as np

from jobshop_rl.models.interval import Interval

TERMINALES = ["PT", "PTW", "EST", "ESTW", "WKR", "WKRW", "NOR", "SLACK",
              "ONE"]


def _arr(v):
    return np.asarray(v, dtype=np.float64)


def _ones(k):
    return np.ones(k, dtype=np.float64)


def compila(arbol):
    """Compila un arbol a una funcion sobre listas de Python.

    Sobre los conjuntos elegibles de estas instancias, de unas decenas
    de elementos, numpy pierde por sobrecarga: la misma expresion
    evaluada con listas va un orden de magnitud mas rapida, y eso
    importa porque E6 compara costes por evaluacion. La aritmetica es la
    misma operacion a operacion, incluida la division protegida de
    jobshop_rl/heuristics/gp_rule.py, asi que el resultado coincide
    bit a bit con la ruta de numpy; los tests lo comprueban.
    """
    if isinstance(arbol, str):
        clave = arbol
        return lambda t: t[clave]
    op = arbol[0]
    if op == "neg":
        f = compila(arbol[1])
        return lambda t: [-x for x in f(t)]
    f, g = compila(arbol[1]), compila(arbol[2])
    if op == "add":
        return lambda t: [x + y for x, y in zip(f(t), g(t))]
    if op == "sub":
        return lambda t: [x - y for x, y in zip(f(t), g(t))]
    if op == "mul":
        return lambda t: [x * y for x, y in zip(f(t), g(t))]
    if op == "div":
        return lambda t: [x / (y if abs(y) > 1e-9 else 1.0)
                          for x, y in zip(f(t), g(t))]
    if op == "min":
        return lambda t: [x if x < y else y for x, y in zip(f(t), g(t))]
    if op == "max":
        return lambda t: [x if x > y else y for x, y in zip(f(t), g(t))]
    raise ValueError(op)


def prioridad_de(arbol):
    """La politica que despacha el minimo de un arbol, sin numpy."""
    f = compila(arbol)

    def politica(terms):
        v = f(terms)
        mejor_i, mejor_v = 0, v[0]
        for i in range(1, len(v)):
            if v[i] < mejor_v:       # empates al primero, como argmin
                mejor_i, mejor_v = i, v[i]
        return mejor_i
    return politica


class Instancia:
    """Una instancia desplegada en listas planas, lista para iterar."""

    __slots__ = ("n", "m", "seq", "lo", "up", "suf_up", "suf_w", "ops")

    def __init__(self, datos):
        self.n = int(datos["num_jobs"])
        self.m = int(datos["num_machines"])
        self.seq = [[int(x) for x in fila] for fila in datos["sequences"]]
        self.lo, self.up = [], []
        for fila in datos["durations"]:
            a, b = [], []
            for d in fila:
                if isinstance(d, Interval):
                    a.append(float(d.lower))
                    b.append(float(d.upper))
                else:
                    a.append(float(d))
                    b.append(float(d))
            self.lo.append(a)
            self.up.append(b)
        # sumas por la cola: el trabajo pendiente DESPUES de cada operacion
        self.suf_up, self.suf_w = [], []
        for j in range(self.n):
            s, w = [0.0] * (self.m + 1), [0.0] * (self.m + 1)
            for k in range(self.m - 1, -1, -1):
                s[k] = s[k + 1] + self.up[j][k]
                w[k] = w[k + 1] + (self.up[j][k] - self.lo[j][k])
            self.suf_up.append(s)
            self.suf_w.append(w)
        # por trabajo, sus operaciones como (maquina, inferior, superior),
        # que es lo unico que lee el decodificador de permutaciones
        self.ops = [[(self.seq[j][k], self.lo[j][k], self.up[j][k])
                     for k in range(self.m)] for j in range(self.n)]


def _makespan(jc_lo, jc_up):
    return max(jc_lo), max(jc_up)


def decodifica(inst, perm):
    """Decodifica una permutacion con repeticion de trabajos.

    La k-esima aparicion del trabajo j es su k-esima operacion, asi que
    recorrer la lista de izquierda a derecha respeta el orden del trabajo
    sin comprobaciones: basta un iterador por trabajo sobre sus
    operaciones. Las mismas sumas y comparaciones, en el mismo orden,
    que el despacho con una regla.
    """
    n, m = inst.n, inst.m
    jc_lo, jc_up = [0.0] * n, [0.0] * n
    mc_lo, mc_up = [0.0] * m, [0.0] * m
    sig = [iter(o) for o in inst.ops]
    for j in perm:
        q, d_lo, d_up = next(sig[j])
        a, x = jc_lo[j], mc_lo[q]
        jc_lo[j] = mc_lo[q] = (a if a > x else x) + d_lo
        a, x = jc_up[j], mc_up[q]
        jc_up[j] = mc_up[q] = (a if a > x else x) + d_up
    return _makespan(jc_lo, jc_up)


def despacha(inst, prioridad, orden=False, eps=0.0, rng=None):
    """Construye el schedule despachando con una regla de prioridad.

    `prioridad(terms)` recibe un diccionario de listas, una entrada por
    elegible y en el orden de los elegibles, y devuelve el indice del que
    se despacha. Con `orden=True` devuelve tambien la permutacion
    construida, que es lo que permite sembrar con ella al genetico.

    Con `eps > 0` se despacha uniformemente del conjunto elegible con esa
    probabilidad: es la aleatorizacion tipo GRASP del mejor-de-N del
    articulo, aqui para poder medirla con el mismo decodificador que el
    resto.
    """
    n, m, seq, lo, up = inst.n, inst.m, inst.seq, inst.lo, inst.up
    suf_up, suf_w = inst.suf_up, inst.suf_w
    jc_lo, jc_up = [0.0] * n, [0.0] * n
    mc_lo, mc_up = [0.0] * m, [0.0] * m
    op = [0] * n
    perm = []
    for _ in range(n * m):
        elig = [j for j in range(n) if op[j] < m]
        if eps > 0.0 and rng.random() < eps:
            # el azar no necesita los terminales: se salta calcularlos
            i = rng.randrange(len(elig))
            j = elig[i]
            k = op[j]
            q = seq[j][k]
            a = jc_lo[j] if jc_lo[j] > mc_lo[q] else mc_lo[q]
            b = jc_up[j] if jc_up[j] > mc_up[q] else mc_up[q]
            jc_lo[j] = mc_lo[q] = a + lo[j][k]
            jc_up[j] = mc_up[q] = b + up[j][k]
            op[j] = k + 1
            perm.append(j)
            continue
        est_lo, est_up, pt, ptw = [], [], [], []
        wkr, wkrw, nor, maq = [], [], [], []
        for j in elig:
            k = op[j]
            q = seq[j][k]
            maq.append(q)
            a = jc_lo[j] if jc_lo[j] > mc_lo[q] else mc_lo[q]
            b = jc_up[j] if jc_up[j] > mc_up[q] else mc_up[q]
            est_lo.append(a)
            est_up.append(b)
            pt.append(up[j][k])
            ptw.append(up[j][k] - lo[j][k])
            wkr.append(suf_up[j][k + 1])
            wkrw.append(suf_w[j][k + 1])
            nor.append(float(m - k - 1))
        base = min(est_up)
        terms = {"PT": pt, "PTW": ptw, "EST": est_up,
                 "ESTW": [b - a for a, b in zip(est_lo, est_up)],
                 "WKR": wkr, "WKRW": wkrw, "NOR": nor,
                 "SLACK": [b - base for b in est_up],
                 "ONE": [1.0] * len(elig),
                 # extras que NO son terminales del conjunto evolutivo:
                 # ninguna regla evolucionada puede leerlos, y estan aqui
                 # para que una politica externa, como el conflict set de
                 # Giffler y Thompson, pueda construirse sin salirse del
                 # decodificador
                 "_MAQ": maq, "_EST_LO": est_lo}
        i = prioridad(terms)
        j = elig[i]
        k = op[j]
        q = seq[j][k]
        s_lo, s_up = est_lo[i], est_up[i]
        jc_lo[j] = mc_lo[q] = s_lo + lo[j][k]
        jc_up[j] = mc_up[q] = s_up + up[j][k]
        op[j] = k + 1
        perm.append(j)
    cm = _makespan(jc_lo, jc_up)
    return (cm, perm) if orden else cm


def mejor(a, b):
    """Criterio lexicografico del articulo: antes el superior, luego el
    inferior. Devuelve True si `a` es preferible a `b`."""
    return a[1] < b[1] or (a[1] == b[1] and a[0] < b[0])
