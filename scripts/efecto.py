# -*- coding: utf-8 -*-
"""El tamano de efecto que usa el articulo, en un solo sitio.

El articulo reporta |r| como la correlacion biserial por rangos de pares
emparejados, |W+ - W-| / (W+ + W-) sobre las diferencias no nulas, con
rangos medios en los empates. Es lo que calcula el verificador para
todos los |r| del texto original.

Los analisis de E1 y E4 calcularon al principio |z|/sqrt(n), que es otra
medida y no coincide con esta: con todas las diferencias del mismo signo
la biserial vale 1 y |z|/sqrt(n) no. Este modulo existe para que todos
los scripts usen la misma.
"""


def biserial(x, y):
    """|r| biserial por rangos de pares emparejados."""
    d = [a - b for a, b in zip(x, y) if a != b]
    if not d:
        return 0.0
    orden = sorted(range(len(d)), key=lambda i: abs(d[i]))
    rangos, i = {}, 0
    while i < len(d):
        j = i
        while j + 1 < len(d) and abs(d[orden[j + 1]]) == abs(d[orden[i]]):
            j += 1
        for k in range(i, j + 1):
            rangos[orden[k]] = (i + j) / 2 + 1
        i = j + 1
    wp = sum(rangos[k] for k in range(len(d)) if d[k] > 0)
    wn = sum(rangos[k] for k in range(len(d)) if d[k] < 0)
    return abs(wp - wn) / (wp + wn)
