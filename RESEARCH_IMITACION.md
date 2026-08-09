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

## Piloto v1 (2026-08-10): TSN2 como experto

Ficheros verificados en T2N2/results/phaseB_TS/N2_tuned: 82 instancias
(las 70 TA + 12 clasicas), 30 runs cada una, formato decodificado
(id de operacion = trabajo*m + k) y CONFIRMADO por replay bit a bit en
nuestro entorno. Calidad del experto: 3.66% RE medio sobre las 70
(mejor-de-30: 2.51%) -- 5.7 puntos mejor que fEABC.

Resultado v1 (mismo protocolo que v0, solo cambia el experto):
acierto de imitacion 56% -> 64% (y subiendo al corte: el experto
coherente ES mas aprendible), pero clon greedy en dev 23.74% -- peor
que v0 (19.58%) y que la politica RL (18.25%). Diagnostico:
desplazamiento de distribucion (Ross & Bagnell): los estados de las
trayectorias TS son casi-optimos; el clon, al fallar, cae fuera de lo
enseñado y los errores se componen 300 pasos.

El par v0/v1 cierra el diagnostico: v0 fallo por profesor incoherente,
v1 por distribucion ajena. Remedios por orden de baratura para v2:
 1. warm start desde el checkpoint RL (base sensata off-manifold);
 2. dataset mixto (estados del experto + estados de rollouts propios);
 3. escala: TS cubre las 82 instancias, no solo TA11-14;
 4. ruido de replay (corromper prefijos del experto y continuar):
    la idea del denoising reaparece como remedio del shift;
 5. evaluar el clon como distribucion (best-of-64), no solo su argmax.

## Palanca 5 medida (2026-08-10): los clones como distribucion

best-of-64 en TA15-20: clon v0 = 13.94% (!), clon v1-TS = 20.42%.
Referencia: politica RL desplegada 13.4% (protocolo benchmark; no
identico -- 3 checkpoints con historia vs una red y 64 muestras).

EL RESULTADO DEL PILOTO: el clon v0, entrenado 4 minutos por CE sobre
64 secuencias muestreadas, casi iguala como distribucion a la politica
PPO de 4000 episodios. El argmax destilado es mediocre; la
DISTRIBUCION destilada casi no pierde nada. Rima con la tesis del
paper (el valor vive en la distribucion) y sugiere que PPO podria ser
necesario solo para generar las primeras muestras, no para el
refinamiento -- la hipotesis central a confirmar en v2 con validacion
seria (mas instancias, split por secuencias, varias tiradas).

v1-TS mejora con muestreo (23.7 -> 20.4) pero el shift sigue
dominando: tampoco la distribucion del clon de TS pisa los estados
adecuados. El warm start + dataset mixto siguen siendo el camino.
