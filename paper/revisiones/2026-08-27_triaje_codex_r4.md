# Triaje de la revisión Codex, ronda 4 (2026-08-27)

Informe crudo: `2026-08-27_revision_codex_eaai_r4_raw.md`. Recomendación:
**major revision**. Espacio de trabajo ya sin huecos: lleva los 21
registros `idea-*`, el depósito de la curva, los auxiliares y el README,
de modo que el verificador corre dentro de él con 803 comprobaciones,
0 fallos y 4 pendientes, todos ficheros que viven fuera del paquete a
propósito.

## R4-1 (GRAVE, CONFIRMADO): la significación de 6.2 se apoya en las diez instancias vistas

El contraste principal corre sobre las 70 Taillard. Diez de ellas
—TA11-TA20, la clase 20x15— son las de entrenamiento (TA11-14) y
validación (TA15-20). Recomputado con
`scripts/comprueba_sesenta_no_vistas.py`, excluyéndolas:

| contraste | 70 instancias | 60 no vistas |
|---|---|---|
| 1 pasada, 30 pol vs 30 GP | 19.82 vs 18.99, p=0.0065 | 20.02 vs 19.15, **p=0.0059** |
| 1 pasada, campeón vs destacada | 18.49 vs 17.71, p=0.0284 | 18.68 vs 17.89, **p=0.0343** |
| 64 muestras, campeón vs destacada | 15.02 vs 15.88, p=0.0200 | 15.40 vs 15.88, **p=0.2613** |
| 1024 muestras, campeón vs destacada | 13.25 vs 14.07, p=0.0101 | 13.59 vs 14.08, **p=0.2305** |

Lectura: **la dirección del cruce sobrevive** (a una pasada gana la
regla, muestreando gana la política), pero **la significación a
presupuestos muestreados no**. Sobre datos no vistos la ventaja de la
política a 64 y 1024 cae de 0.86 a 0.48 puntos y deja de ser
distinguible del ruido con n=60.

Defensa parcial que NO basta: ambas familias se entrenaron y ajustaron
sobre las mismas diez instancias, así que la contaminación es simétrica
por diseño. Pero no lo es en efecto: la política es especialista de la
clase 20x15 y saca allí ~3.1 puntos de ventaja, frente a 0.48 en el
resto, así que incluirlas infla su ventaja y es lo que carga la
significación.

Consecuencia: la frase "they differ significantly at every budget
evaluated" —abstract, contribución 2, 6.2 y conclusiones— no se
sostiene como afirmación sobre instancias no vistas. Hay que
reencuadrarla.

## R4-2 (CONFIRMADO en el código): a presupuestos muestreados es 1 contra 1

`scripts/enfrenta_gp_treinta.py:120-133`: el contraste de 30 contra 30
existe SOLO a una pasada (`1pass_media`); a 64 y 1024 los contrastes
son `campeon vs regla destacada`. El abstract dice "thirty trained
artifacts per family evaluated in one harness at matched inference
budgets", que induce a leer 30 contra 30 en todos los presupuestos.
Hay que acotarlo o evaluar los treinta a los presupuestos muestreados.

Segundo punto suyo, también cierto: la política optimiza el peor caso y
las reglas GP destacadas se evolucionaron contra RE del punto medio.
Es una comparación de dos sistemas desplegados, no un aislamiento de la
familia de modelos. Conviene una tabla explícita de lo igualado y lo no
igualado, con el objetivo dentro.

## R4-3 (cierto, consecuencia de arreglar el código): el código publicado ya no reproduce los brazos robustos históricos

Al corregir `_episode_makespan` a `final_makespan`, el código actual no
reproduce la ruta de transferencia de las tiradas λ>0 depositadas. Hay
que archivar la semántica histórica tras una opción de compatibilidad,
o declarar que reentrenar los brazos robustos con el código corregido
puede dar otros pesos.

## R4-4 (parcialmente cierto): el paquete no soporta todo lo que promete

El README nombra `requirements.txt` que vive en `zenodo_drl/code/`, no
en la raíz; `fair_gp_eps.csv` sigue sin productor propio; y la suite de
tests no está verde (los 8 fallos preexistentes de parsing de
intervalos, anteriores a este trabajo). Los tres son de higiene.

## Lectura global

Cuatro rondas: reject, major, major sin motivo de rechazo, y ahora
major con un hallazgo estadístico de fondo que las tres anteriores no
vieron. R4-1 no es un defecto de implementación sino de diseño del
contraste, y es el tipo de cosa que hunde un paper en revisión si la
encuentra el árbitro de la revista en vez del nuestro. Arreglarlo
debilita una afirmación y refuerza la credibilidad del resto.
