# Campaña de pesos del reward — protocolo pre-registrado (2026-08-05)

Escrito ANTES de mirar ningún resultado, para que la regla de decisión
no se pueda acomodar a lo que salga.

## Diseño

- Espacio: los **seis** pesos del reward en **[0, 1]** (decisión del
  autor; sin anclas ni techos asimétricos, el 0 incluido para poder
  apagar componentes). Optimizador congelado en los defaults de
  tab:hyper — la condicional de despliegue.
- Fidelidad de operación (la única informativa según §5.3): 2
  instancias × 1000 episodios por evaluación, batched, eval
  best-of-64 en TA15–17, semillas de entrenamiento como instancias de
  carrera. Presupuesto 300, firstTest 6, parallel 3.
- Sembradas: (1) pesos efectivos actuales congelados
  (1.0, 0.24, 0.1, 0.1, 0.26, 0.15) — además testea si el ajuste por
  instancia es prescindible; (2) solo-terminal (1, 0, 0, 0, 0, 0) —
  ¿sirve de algo el shaping?; (3) uniforme (0.5 × 6).
- Mecanismo: DEEPLJSP_REWARD_WEIGHTS fija los seis pesos y anula tanto
  el generador como el reajuste por instancia (bypass verificado:
  ruta estándar intacta sin la variable).

## Confirmación (idéntica al élite 22)

El ganador de la carrera se reentrena a 3 semillas sobre las 4
instancias de entrenamiento completas (4×1000, batched) y se evalúa
best-of-64 sobre las 6 de desarrollo, contra los checkpoints default
existentes, pareado por (instancia, semilla), Wilcoxon.

## Regla de decisión (pre-registrada)

1. Si el ganador NO mejora los defaults en la confirmación (como en
   las campañas 1 y 2): los pesos a mano quedan validados por una
   carrera dedicada; una frase en §5.3 y otra en §4.1.
2. Si el ganador SÍ mejora significativamente (p<0.05 pareado):
   se asume el reentrenamiento del aparato experimental con los pesos
   nuevos (decisión ya tomada por el autor: «que haya que repetir los
   experimentos no es excusa»).
3. La sembrada efectivo-congelado se compara además contra el
   desplegado (adaptativo): si hay paridad, el ajuste por instancia
   se declara prescindible y la recomendación pasa a un vector fijo.
4. La sembrada solo-terminal responde, gane o pierda, si el shaping
   denso es necesario; su resultado se reporta sea cual sea.

## Parada obligatoria antes de adoptar (2026-08-07)

La confirmación MIDE y escribe el veredicto; no adopta nada. Al
terminar se para y la decisión —reejecutar el aparato con los pesos
nuevos o mantener los actuales— se toma con el autor, viendo el
resultado. La regla 2 dice qué haríamos si la mejora es clara, pero
la ejecución de esa rama no arranca sin su visto bueno; su criterio
declarado es que una diferencia pequeña no justifica el cambio.

## Lo que dio la carrera (2026-08-08 02:14, ANTES de la confirmación)

299 de 300 experimentos, 44 horas, 6 iteraciones. Sobreviven **cuatro**
élites. Ganadora #15: makespan 0.4487, idle 0.1779, critical 0.5513,
balance 0.2669, progress 0.9154, local 0.5014.

Lo informativo no es la ganadora, es la dispersión entre las cuatro
supervivientes (`scripts/analiza_irace_reward.py`):

| peso | #15 | #20 | #30 | #35 | rango | actual |
|---|---|---|---|---|---|---|
| makespan | 0.449 | 0.768 | 0.569 | 0.581 | 0.32 | 1.00 |
| idle | 0.178 | 0.023 | 0.182 | 0.178 | 0.16 | 0.24 |
| critical | 0.551 | 0.287 | 0.768 | 0.468 | 0.48 | 0.10 |
| balance | 0.267 | 0.500 | 0.277 | 0.319 | 0.23 | 0.10 |
| progress | 0.915 | 0.645 | 0.987 | 0.892 | 0.34 | 0.26 |
| local | 0.501 | 0.330 | 0.491 | 0.648 | 0.32 | 0.15 |

Cuatro vectores que difieren hasta en 0.48 en una componente empatan.
Y la concordancia entre semillas sobre cuál es mejor, en la última
carrera, es **Kendall W = 0.02–0.05**: prácticamente ninguna. A
fidelidad de operación los seis pesos no son identificables; el ruido
de semilla domina el efecto del peso. Ése es el resultado, gane quien
gane la confirmación.

Dos cosas sí son consistentes entre las cuatro élites: `idle` es el
peso más pequeño en las cuatro, y `progress` el más grande en tres de
cuatro. Ninguna reproduce la ordenación del vector desplegado
(makespan > progress > idle > local > critical > balance).

Sobre las sembradas, y esto responde a la regla 4 del plan sin esperar
a la confirmación:

- **solo-terminal (1,0,0,0,0,0): eliminada en la primera ronda**. El
  shaping denso no es prescindible.
- **uniforme (0.5×6): eliminada en la primera ronda.**
- **efectivo-congelado (el vector actual a mano): sobrevivió la
  primera carrera** —élite 3ª de 3 en la iteración 1— y cayó en la
  segunda. Es decir, compite, pero no queda entre las mejores.

## Confirmación y decisión (2026-08-08 04:02)

Ganadora #15 reentrenada a 3 semillas sobre TA11-14, best-of-64 sobre
TA15-20, pareada contra los checkpoints por defecto:

| semilla | ganadora #15 | default |
|---|---|---|
| 2 | 13.03 | 12.93 |
| 3 | 14.22 | 14.04 |
| 4 | 14.87 | 13.67 |
| **media** | **14.04** | **13.55** |

Peor en las tres semillas. Mejor en 7 de los 18 pares. Wilcoxon
pareado **p = 0.2097**.

**Se aplica la regla 1**: no hay mejora significativa —de hecho no hay
mejora ninguna—, así que los pesos a mano quedan validados por una
carrera dedicada, **no se reejecuta nada** y los checkpoints
desplegados siguen siendo los mismos. La rama 2, la que obligaba a
parar y decidir con el autor, no se activa: su condición era una
mejora significativa y no la hay. El criterio declarado del autor
—«si es muy cercano quizás no merezca la pena cambiarlo»— apunta en
la misma dirección con más razón todavía, porque la ganadora es peor.

Escrito en el paper: §5.3 gana la campaña como tercer párrafo (con la
eliminación de la solo-terminal y la planitud del objetivo en los
pesos, que valen más que el veredicto) y §4.1 deja de decir que los
pesos nunca entraron en el estudio de configuración. Catorce
comprobaciones nuevas leen el log de la confirmación y el de la
carrera.

## Qué NO se toca

Ningún fichero de campañas anteriores (parameters/scenario/logs con
otros nombres); ningún checkpoint existente; la ruta estándar del
reward (sin la variable de entorno, comportamiento bit a bit igual).
