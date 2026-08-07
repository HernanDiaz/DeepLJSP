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

## Qué NO se toca

Ningún fichero de campañas anteriores (parameters/scenario/logs con
otros nombres); ningún checkpoint existente; la ruta estándar del
reward (sin la variable de entorno, comportamiento bit a bit igual).
