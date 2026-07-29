# Ideas para un segundo paper: busqueda local sobre el espacio de reglas

Material surgido mientras se cerraba el paper de GP para IJSP. Todo lo que
lleva cifra esta medido sobre la regla destacada (`gp_tuned_seed1`) o sobre
los 30 arboles del brazo principal; lo que no, esta marcado como conjetura.

## 1. La invarianza al argmin

Las reglas de despacho se aplican por `argmin` sobre el conjunto elegible, asi
que la prioridad es invariante a

    f  ->  a*f + b        para todo a > 0

Ningun despacho cambia. Consecuencias:

- **El *linear scaling* de Keijzer (EuroGP 2003) no sirve aqui.** No es que
  ayude poco: su efecto es exactamente cero. Y es una de las tecnicas
  estandar que la literatura de GP-para-scheduling importa de la regresion
  simbolica sin comprobar si sobrevive al cambio de objetivo.
- **Solo los pesos RELATIVOS son libres**: k-1 para una regla con k terminos
  aditivos. En la regla destacada, 4 terminos -> 3 grados de libertad, no 5.
- **El control de bloat se vuelve arbitrario.** `2*(SLACK^2 + 2PT - WKR -
  WKRW - 1)` es LA MISMA REGLA que la destacada: mismos despachos, mismo
  fitness. Pero gasta mas nodos y el tope de 30 la penaliza. Se castiga
  sintaxis, no comportamiento.
- **La diversidad y la semantica estan mal medidas.** Dos individuos con
  prioridades `f` y `2f+3` producen schedules identicos, pero cualquier
  distancia semantica sobre el vector de salidas los cuenta como distintos.
  La representacion semantica correcta de una regla de despacho es **el orden
  que induce**, no el vector de valores.

**PENDIENTE ANTES DE PLANTEARLO COMO APORTACION:** busqueda bibliografica
seria. Durasevic y Jakobovic han trabajado mucho en GP para scheduling,
incluida diversidad, y podria existir ya trabajo sobre semantica basada en
rangos. Si esta hecho, la idea se cae; si esta a medias, el angulo sigue.

## 2. Coeficientes: la evolucion deja valor sin recoger

Medido (Figura 5 del paper, `benchmarks/coefficient_sweep.csv`):

| peso | evolucionado | optimo del barrido | RE |
|---|---|---|---|
| alpha (PT) | 2 | **2** | 17.71 (minimo) |
| beta (WKRW) | 1 | **0.5** | 17.54 vs 17.71 |

alpha esta clavado; beta no. 0.17 puntos disponibles por ajuste posterior en
una sola regla.

Ademas **el terminal set no tiene constantes efimeras**: la unica constante es
`ONE`. La evolucion construye los coeficientes estructuralmente, y eso gasta
nodos contra el tope. En la regla destacada, `min(PT, PT)` usa **tres nodos
para expresar PT**.

Tres vias, por relacion beneficio/coste:

1. **Constantes efimeras en el terminal set.** Lo mas barato; libera nodos.
2. **Busqueda local sobre pesos relativos, post-hoc.** Automatizar lo que se
   hizo a mano con alpha y beta: canonizar el arbol y optimizar los k-1 pesos.
3. **GP memetico**: lo anterior dentro del bucle, sobre los elites.

## 3. Busqueda local sobre el espacio de reglas

Medido sobre la regla destacada
(`scripts/neighbourhood_analysis.py`, reproducible):

| | |
|---|---|
| nodos / hojas / funciones | 26 / 12 / 14 |
| vecinos por sustitucion de un simbolo | **151** |
| de ellos NEUTROS (mismo schedule en las 4 de entrenamiento) | **40 = 26%** |

**El vecindario es diminuto**: 151 vecinos a ~0.4 s cada uno, un minuto para
explorarlo entero frente a los 30 min de una evolucion. Lo hace manejable el
tope de 30 nodos, y no es lo habitual en GP.

**El obstaculo es la neutralidad.** Un cuarto de los movimientos no cambia
ningun despacho, en parte por la invarianza del punto 1: se alteran los
valores de prioridad sin alterar el orden. El paisaje esta lleno de mesetas.
Eso decide el metodo:

- **Hill climbing se atasca**: sin señal en un cuarto de los movimientos.
- **Tabu encaja**: fuerza el movimiento, y una lista sobre pares (nodo,
  simbolo) recien cambiados impide volver. Las mesetas pasan de trampa a
  corredor.
- **Desempate por tamaño en las mesetas**: entre vecinos de igual fitness,
  quedarse con el menor. Convierte la neutralidad en simplificacion gratuita
  y encaja con el argumento de interpretabilidad.

**Precedente**, ya citado en el paper: el SSHE de Gil-Gala et
al. (`GilGala2025SSHE`, Journal of Heuristics 2025) hace busqueda sistematica
en arbol sobre el espacio de expresiones y reporta reglas de calidad
comparable pero mas pequeñas. Buscar directamente en el espacio de reglas ya
funciona en scheduling; lo que no esta hecho es **tabu** sobre ese espacio ni
**caracterizar la neutralidad** que lo condiciona.

## Diseño posible

GP genera el arbol, tabu refina por sustitucion de simbolos, desempate por
tamaño en las mesetas. Tres ingredientes medibles por separado, con la
neutralidad del 26% como motivacion cuantificada. La invarianza del punto 1
da el marco teorico que explica por que ese paisaje es como es.
