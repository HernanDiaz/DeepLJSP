# Nota de diseño: imitación y denoising para el IJSP (2026-08-09)

Semilla del siguiente paper, de la conversación de esta madrugada.
NADA de esto entra en el paper DRL actual.

## Motivación (medida, no intuición)

El canal de señal de PPO es débil y caro en este problema: sd entre
semillas 0.47, tres campañas de irace sin resolución por debajo de ~1
punto, y los seis pesos del reward PLANOS en [0,1]^6 (Kendall W
0.02-0.05). La vía supervisada elimina reward, pesos y cabeza de valor.

## Idea 1: imitación de un experto (TSN2)

Replay: cualquier orden de proceso -> nm decisiones etiquetadas en
nuestro entorno. Clon neuronal (mismo encoder, CE) o regla por
imitación (GP con fitness = acuerdo; Ingimundardottir & Runarsson,
J. Scheduling 2018).

**Piloto v0 (hecho, benchmarks/proto_imitacion/)**: experto = top-16
del pool v2 por instancia de entrenamiento (RE 13.00%), 19.134
decisiones, 40 épocas en 4 min. Resultado: acierto de imitación se
estanca en 56%; clon greedy 19.58% vs maestros greedy 18.25% en
TA15-20. NEGATIVO E INFORMATIVO: las colas muestreadas son suerte, no
una regla de decisión coherente — confirmación experimental del
argumento de estadísticos de orden de la seccion 8 del paper.

Palancas, en orden: (1) TSN2 como experto — estructura de decisión
coherente, calidad ~9-10%; el usuario copia los ficheros; (2) warm
start desde el checkpoint maestro; (3) escala (pools de 71 instancias
existen en seeds/); (4) bucle de auto-mejora (Corsini NeurIPS 2024).

## Idea 2: denoising (difusión discreta sobre schedules)

Ruido = k movimientos (la permutación con repetición hace TODO estado
de ruido factible: no hay proyección de ciclos, la pega de DIFUSCO).
Denoiser = operador de mejora aprendido supervisadamente; si el
vecindario de ruido es N1/N2, se está destilando el paisaje del TS.
Regimen de ruido bajo = descenso local supervisado (empezar aquí);
alto = modelar la distribución de schedules buenos.

Cautelas: la entrada es un schedule COMPLETO (features nuevas:
comienzo/criticidad/holgura en la solución), miopía del ruido bajo
(sin lista tabú), techo = experto.

Piloto barato pre-modelo: curvas (degradación por nivel de ruido k) y
(identificabilidad del movimiento inverso desde features locales).

## Pipeline conjunto

constructor (política actual o clon) -> denoiser iterativo ->
auto-mejora. Solver anytime enteramente aprendido; es la dirección de
despliegue de la seccion 8 llevada un paso más.
