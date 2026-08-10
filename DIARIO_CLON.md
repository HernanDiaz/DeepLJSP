# Diario de mejoras del clon (imitacion / auto-mejora)

Registro cronologico de cada variante probada y su resultado. El diseño
largo y la discusion viven en RESEARCH_IMITACION.md; esto es el parte
de guerra: que se probo, con que numeros, y que se concluyo.

Referencias fijas (clase 20x15, dev TA15-20, RE %):
politica RL greedy 18.25 / bo64 13.4 · experto TSN2 ~3.66 · objetivo
por hitos: greedy < 18.25 -> bo64 < 13.4 -> acercarse a 3.66.

---

## 2026-08-09 · v0: auto-clon (destilacion one-shot)

**Que**: CE hacia las mejores muestras de la PROPIA politica PPO
(one-shot, sin iterar). 4 min de entrenamiento supervisado.
**Resultado**: bo64 13.94 ≈ PPO 13.4. La distribucion destilada casi
iguala a la original.
**Conclusion**: clonar colas afortunadas da etiquetas incoherentes
(techo de acierto bajo), pero la destilacion PRESERVA la distribucion.
Semilla de la v3.

## 2026-08-09 · v1: clon puro de TSN2

**Que**: CE hacia los replays de TSN2 (30 runs x 4 instancias), red
desde cero.
**Resultado**: acierto dev 56->64% (TS es mas aprendible que la
politica), pero despliegue 23.74% dev: fracaso por covariate shift —
un error y el clon cae fuera de la distribucion del experto.
**Conclusion**: el experto externo necesita warm start y datos que
cubran los estados propios.

## 2026-08-10 · v2: warm start + dataset mixto 50/25/25 + ancla KL

**Que**: warm start rotatorio desde PPO; dataset A/B/C (replay puro /
prefijo corrompido / auto-seleccion); lr 5e-5; perdida
CE − 0.01·H + 0.5·KL(p_warm‖p); seleccion de epoca por dev bo16;
guarda de restauracion. Dos humos previos: el 1 destapo el colapso de
entropia (una epoca de CE pura: bo64 13.90->17.80) y un bug de
restauracion; el 2 valido el ancla (H estable ~1.9).
**Resultado** (3 semillas, log en logs/clon_v2_real.log): NULO
PROTEGIDO — ninguna semilla batio su bo16; restauradas las tres.
Pero el greedy mejoro mucho en epocas intermedias: 17.72->15.97,
18.79->16.14, 18.23->16.59.
**Conclusion**: la imitacion de TS afila el argmax (~2 puntos bajo el
argmax RL) pero la masa se va de donde el best-of-N la explota, con
entropia intacta: el valor de la distribucion RL es DONDE pone la
masa, no cuanta entropia tiene. Decision del autor: descartar el
producto greedy/ensemble (mejora residual); ir a la auto-mejora.

## 2026-08-10 · v3: bucle de auto-mejora (SLIM, en curso)

**Que**: iterar la v0 — cada ronda muestrea n=64 por instancia de
entrenamiento con la politica ACTUAL, conserva las top-4 bajo la
Eq. (3) mas la elite historica (trinquete anti-regresion), replay a
etiquetas y 3 epocas de CE; ancla KL contra la politica al inicio de
la RONDA (region de confianza: deriva acumulada libre, colapso por
ronda no); seleccion de ronda por dev bo16; guarda de restauracion.
10 rondas, paciencia 4, 3 semillas. Script: scripts/clon_v3.py,
salida benchmarks/clon_v3/.
**Apuesta medible**: la ronda 0 es la v0 (13.94); iterar con
re-muestreo fresco deberia mover la masa hacia su propia cola buena y
bajar del 13.4. Señal interna a vigilar: `sel RE` (calidad media de lo
seleccionado) deberia decrecer ronda a ronda.
**Humo (1 semilla, 2 rondas, n=16)**: las etiquetas son buenas (top-2
de 16 muestras: 13.32% de RE) y el bo16 mejora ronda a ronda
(15.89 -> 15.32 -> 15.10) con la entropia estable (0.96 -> 0.98) y el
greedy sacrificado (17.72 -> 19.13). PERO el bo64 final EMPEORO:
13.90 -> 14.24. Salidas archivadas en benchmarks/clon_v3/humo/.

**Correccion antes de la tirada real**: el criterio de seleccion y la
metrica de despliegue divergen. El bucle afila lo justo para ganar con
16 muestras y perder con 64, asi que elegir ronda por bo16 optimiza un
proxy sesgado. `evalua_dev` pasa a hacer UNA pasada de 64 muestras y
devolver greedy / bo16 / bo64 -- el bo16 es el prefijo de las mismas
semillas, luego las dos curvas son el mismo experimento a dos
presupuestos y cuestan una sola evaluacion -- y la seleccion de ronda
se hace por bo64. Coste: ~9.7 min por ronda en vez de 5.7.

**Resultado (tirada real)**: (pendiente, ~5 h 30 desde las 13:37)

## 2026-08-10 · v4: ruin & recreate, la linea base del denoising

**Decision de rumbo** (del autor): tras la v3, pasar a la via del
denoising en lugar de seguir iterando la construccion. Motivo tecnico:
la Eq. (9) implica que en construccion los anchos no pueden informar
al objetivo, pero un operador de MEJORA ve horarios completos, donde
el ancho es observable y accionable — es el escenario donde la
estructura intervalar deja de ser decorativa.

**Que**: antes de aprender un denoiser, medir la reparacion SIN
aprender: destruir las ultimas d ~ U[15,150] decisiones del incumbente
y reconstruir muestreando con la politica desplegada; aceptar si
mejora la clave de la Eq. (3). Presupuesto igual al bo64 (64xT pasos
de entorno, replays incluidos: contabilidad conservadora). bo64
recalculado en el mismo script con las semillas de evaluacion de
siempre -> 18 pares exactos, Wilcoxon. Script scripts/clon_v4_rr.py,
salida benchmarks/clon_v4_rr/, encolado tras la v3.

**Humo (1 politica, 2 instancias, presupuesto 8xT, 25 s)**: arnes
correcto de punta a punta; con 7 iteraciones R&R ya gano en TA16
(11.84 vs 13.68 del bo8) y perdio en TA15 (15.46 vs 14.04). A 8xT el
muestreo de d apenas itera; el veredicto es a 64xT.

**Criterio para el siguiente paso**: si R&R >= bo64, el denoiser
aprendido tiene una linea base que superar y la via queda abierta con
listón; si R&R < bo64, la reconstruccion ciega no basta y el
argumento para APRENDER el operador de reparacion es directo.

**Resultado**: (pendiente)
