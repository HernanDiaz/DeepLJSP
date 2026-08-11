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

**Resultado (tirada real, 3 semillas x 10 rondas, n=64, top=4)**:
POSITIVO 3/3 — el primer entrenamiento de la linea que mejora la
metrica de despliegue. bo64: 13.90->11.95, 13.83->13.07, 13.83->13.26
(media 13.86->12.76, −1.10); las tres bajo la referencia PPO 13.4.
Elite en entrenamiento: 11.36% de media (mejor instancia: 8.96%).
Log en logs/clon_v3_real.log y benchmarks/clon_v3/.

Lecturas finas del log:
- Patron reproducido en las tres semillas: rondas 1-2 malas y
  despegue en la ronda 3. La paciencia de 4 corto a la semilla 2 en
  la ronda 4, exactamente donde las otras dos despegaron: paciencia
  mas larga (6-8) es la variante obvia si se itera.
- La semilla 1 seguia acelerando al agotar las 10 rondas
  (13.19->12.93->12.62->11.95): mas rondas, segunda variante obvia.
- La entropia no se degrada (H estable por semilla: 0.96 / 1.31-1.35 /
  1.12-1.18): la mejora no viene de afilar sino de RECOLOCAR la masa
  — la tesis del diagnostico v2, ahora con confirmacion positiva.
- El greedy medio empeora (18.25->18.81): el bucle optimiza la
  distribucion, no el argmax; el comercio argmax/distribucion cambia
  de signo respecto a la v2, como predice el origen de las etiquetas.

**Conclusion**: la auto-mejora supervisada funciona donde la
imitacion de experto externo fallo, con la misma perdida y las mismas
guardas; la unica diferencia es de QUIEN son las etiquetas. Queda
como punto de datos central de la linea; el rumbo (decision del
autor) sigue siendo el denoising/v4, con la v3 como evidencia de que
la politica aun tenia margen dentro de su propia distribucion.

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

**Incidente de encolado (16:42-22:28)**: el lanzador ps1 murio al
instante de arrancar la v4 real: en PowerShell 5.1, `*>` sobre un
ejecutable nativo convierte cada linea de stderr en ErrorRecord, y
con `$ErrorActionPreference = "Stop"` el primer INFO del logging de
Python (stderr) mato el script. Seis horas perdidas. Leccion: los
lanzadores llaman a python con Start-Process y redirecciones nativas
(-RedirectStandardOutput/-RedirectStandardError), nunca con `*>` ni
`2>&1` dentro del ps1. Relanzada a las 22:29.

**Resultado (18 pares, 3 politicas x 6 dev)**: DERROTA CLARA de la
reparacion ciega — R&R 16.16% vs bo64 13.86% (4/18, dif media +2.30,
Wilcoxon p=0.001). Diagnosticos: (a) paralisis de aceptacion, 3.7/63
movimientos aceptados de media y dos paralisis totales; (b) la
correlacion greedy-deficit 0.52 — la destruccion de cola no repara
errores tempranos (con d<=150 de ~300, medio horario es inmutable);
(c) las victorias son por decimas, las derrotas por puntos.

**Conclusion**: el resultado que la via necesitaba, con simetria
util para el paper: la politica constructiva NUNCA vio estados de
reparacion — covariate shift en inferencia, como la v1 lo sufrio en
entrenamiento. Reparar es otra distribucion de estados; hay que
entrenar sobre ella. La linea base queda medida y es batible.

**Diseño v5 (el denoiser aprendido) que esto dicta**:
1. Datos: pares (solucion buena corrompida -> restauracion), la
   maquinaria de la fase B de la v2 con soluciones TSN2/elites como
   objetivo — la distribucion de entrenamiento ES la de inferencia
   del arnes R&R.
2. Corrupcion en cualquier tramo (no solo cola), via resto_experto;
   y d hasta T para incluir reinicios.
3. Evaluacion: el MISMO arnes v4 a presupuesto igual, sustituyendo
   la politica de reconstruccion por la entrenada; exito = batir
   tanto al bo64 como al R&R ciego con p<0.05.
4. Los checkpoints v3 (mejor distribucion) son el warm start natural.

## 2026-08-10 · v3-ext: la asintota (encolada, nocturna)

30 rondas, paciencia 8, 3 semillas, salida benchmarks/clon_v3_ext/
(--salida nuevo; nada se sobreescribe). Mide donde aplana la
configuracion que a 10 rondas dio 12.76 de media.

**Resultado**: LA ASINTOTA ERA LA TIRADA CORTA. 11.95 / 13.07 / 13.25,
media 12.75 contra 12.76 — una centesima en 3x mas computo. Las dos
hipotesis de margen quedaron refutadas por sus propios casos de
prueba: la semilla 1 no siguio acelerando (paro en la ronda 14 sin
batir su ronda 6) y la semilla 2 no tenia despegue podado (paro en la
8 sin batir su ronda 0). Un reinicio del equipo a mitad de tirada
verifico ademas la reproducibilidad: 24 rondas de replay identicas
numero a numero.

**Conclusion**: las ganancias del bucle llegan en las primeras ~6
rondas o no llegan. La elite de train siguio mejorando (11.36->11.04)
con dev plano: la restriccion activa es la DIVERSIDAD DE DATOS (4
instancias), no el presupuesto de optimizacion. Esto redirige el
esfuerzo a la escala de instancias (opcion D) y a la v5, y cierra la
v3 con numeros finales: bo64 13.86 -> 12.76 de media, tres de tres.

## 2026-08-11 · v4b/v4c: dos brazos baratos antes de la v5

(a) v4b: el arnes R&R con los CLONES v3 reconstruyendo — ¿una
distribucion mejor repara mejor, o la paralisis de aceptacion es
independiente de la calidad del muestreador? (b) v4c: R&R original
con d ~ U[15, T] — ¿cuanto del deficit era no poder tocar el primer
medio horario? Ambos con --salida propia; nada se sobreescribe.

**Resultado v4b (clones, cola corta)**: los clones reparan PEOR en
relativo: R&R 16.79 contra su bo64 12.76 (+4.03, 1/18, p=0.0004),
frente al +2.30 de las politicas originales. El muestreador no es la
palanca. De regalo, validacion independiente de la v3: el bo64
recalculado de los tres clones da 11.95 / 13.07 / 13.26 — identico
al entrenamiento, media 12.76 exacta.

**Resultado v4c (originales, d hasta T)**: EMPATE ESTADISTICO con el
bo64: R&R 13.73 contra 13.86 (10/18, p=0.67), cero paralisis (5.5
aceptaciones de media, ningun cero) y valles que el bo64 no
encuentra (10.55, 10.83, 11.22, 11.45). De perder por +2.30 con
p=0.001 a empatar, solo ampliando d de U[15,150] a U[15,299]. La
gama de destruccion era el grueso del deficit; ademas R&R sigue
usando ~la mitad de forwards de red a presupuesto igual de pasos.

**Lectura conjunta**: reparar exige (i) el vecindario correcto
(destruccion profunda incluida — los reinicios completos forman
parte del operador) y (ii) probablemente entrenamiento sobre estados
de reparacion, que es lo que la v5 mide. El listón de la v5 se fija
con el cruce v4d (clones + d completo), lanzado a las 4:41.

## 2026-08-11 · v4d: clones v3 + destruccion completa (en curso)

El cruce que falta: la mejor distribucion (bo64 12.76) con el
vecindario correcto. Si ya baja de 12.76, la reparacion ciega bate
al mejor despliegue conocido y la v5 tiene que superar ESO.
**Resultado**: (pendiente)
