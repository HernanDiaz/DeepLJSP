# Las treinta reglas GP a presupuesto 64 — material en reserva

Campaña del 2026-08-31, no citada por el paper. Se guarda por si la
revisión pide el contraste a nivel de artefacto en el presupuesto
muestreado, que es lo que señaló la ronda r7 como problema mayor.

## Qué hay

`pool_0.csv` a `pool_5.csv`: las treinta reglas del brazo principal
(`benchmarks/reevo_fixedfit/gp_tuned_seed{1..30}.json`) sobre las
setenta Taillard intervalares, 64 rollouts por (regla, instancia), con
los DOS extremos de cada rollout. 2100 pares, 134 400 rollouts. El
rollout 0 es la pasada determinista de la regla; los 63 restantes son
epsilon-greedy con epsilon=0.1. Semilla del muestreo fijada por
(regla, instancia).

Lo produce `scripts/eval_gp_treinta_bo64.py` (reanudable, seis
carriles); lo cruza `scripts/analiza_artefactos_bo64.py`, que escribe
`contraste_bo64.json`.

## Qué dice

Diez artefactos de política (los del depósito de la curva, semillas 2
a 11) contra las treinta reglas, B=64, promediando dentro de familia
por instancia y con la instancia como unidad:

    politica 15.297   regla 15.941   dif -0.644
    mejor en 47/70 instancias, Wilcoxon exacto p=0.0105

Con la política como media de 200 subconjuntos en vez de una
realización: 15.338 contra 15.941, p=0.0171. Los rangos por artefacto
se solapan: política 14.34-16.40 (mediana 15.25), regla 14.88-18.23
(mediana 15.45).

## Por qué NO se publicó tal cual

Los diez artefactos de política no representan a los treinta: a una
pasada dan 19.47% frente al 19.82% que el paper reporta para los
treinta, o sea 0.35 puntos mejores, y entre ellos está la semilla 5,
que es la desplegada y fue elegida por rendimiento en validación.
Trasladado ese sesgo a B=64, la ventaja de 0.644 se quedaría en torno
a 0.3 y probablemente dejaría de separar. Es un diez contra treinta,
no un treinta contra treinta.

Cerrarlo cuesta evaluar las veinte semillas restantes a B=64 sobre las
setenta: 89 600 rollouts de política, unas once horas en seis
carriles. Los checkpoints existen, bajo las etiquetas
`v2-full-1000ep-ext30-a` y `-ext30-b`; `scripts/eval_curva_intervalo.py`
simplemente no las lista en su tupla TAGS.

## Lo que sí es limpio de aquí

Un hecho que no depende del subconjunto de política, porque vive
entero dentro de la familia GP: a B=64 la regla destacada da 15.21%,
y su familia tiene mediana 15.45 y rango 14.88-18.23. El artefacto
que el estudio de GP presenta está cerca del mejor de los treinta, de
modo que el empate a 64 del par seleccionado no sale de haber
enfrentado a la política contra una regla floja.
