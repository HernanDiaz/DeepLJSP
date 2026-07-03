# Diseño de agents_v2 — agente RL con representación invariante al tamaño

Propuesta de arquitectura para la opción A (salto arquitectónico). Objetivo:
sacar al agente de la liga de las reglas de despacho (v1: RE ≈ 44% media /
31% mejor semilla vs MOR ≈ 46%) y acercarlo a la banda que la literatura de
neural combinatorial optimization consigue en JSP (RE ~25-35% constructivo).

## Por qué desde cero (evidencia de la sesión 2026-07-02/03)

- El v1 es un óptimo local co-adaptado: 16 ideas de una variable probadas con
  benchmark; cualquier perturbación aislada de escala de entrada, régimen de
  updates o descuento lo degrada (ver RESEARCH_IDEAS.md). No es reformable.
- Diagnóstico del techo: la política ve 10 features locales por operación,
  sin contexto global (cargas de máquinas, congestión), y su explotación
  apenas supera la suerte de la exploración temprana (en 5/12 series el mejor
  makespan salió de los episodios 1-3).
- La red de valor depende de num_jobs y num_machines → imposible evaluar o
  transferir entre tamaños. El v2 elimina esa dependencia por construcción.

## Qué se reutiliza (validado) y qué se escribe nuevo

**Se reutiliza sin tocar**: entorno (semántica anclada por las heurísticas
deterministas), aritmética de intervalos, loaders de las 167 instancias,
sistema de recompensas afinado (pesos de idea-04/05), heurísticas de
referencia, benchmark quick/full y protocolo de RESEARCH_IDEAS.md.

**Se escribe nuevo, sin importar nada del v1**:

```
jobshop_rl/agents_v2/
    state_encoder.py   # representación invariante al tamaño
    networks.py        # policy head + value head sobre el encoder
    ppo_trainer.py     # entrenamiento co-diseñado (batches + normalización + lr)
    agent.py           # misma interfaz que v1: select_action / evaluate_policy /
                       # save_checkpoint — el benchmark lo ejecuta sin cambios
```

## Arquitectura

### 1. Features por operación elegible (normalizadas por el LB del problema)

Para cada operación elegible, un vector de ~16 valores, TODOS adimensionales
(divididos por el LB del problema o por ratios), porque la normalización se
co-diseña con la inicialización y el lr — lección de las ideas 11/12:

- duración: lower/LB, upper/LB, anchura relativa (up−lo)/mid
- earliest start: lower/LB, upper/LB, anchura relativa
- trabajo restante del job: lower/LB, upper/LB; ops restantes / num_machines
- progreso del job: op_idx / num_machines
- contexto de SU máquina: carga restante de la máquina / LB, tiempo libre de
  la máquina hasta el earliest start (gap potencial) / LB, ratio de congestión
  (carga restante de la máquina / carga media de máquinas)
- holgura: earliest_start_upper − min(earliest_start_upper de las elegibles),
  normalizada

### 2. Contexto global (invariante al tamaño, por pooling)

Vector fijo (~12 valores) construido con agregados, nunca concatenando por
índice: progreso global (% ops programadas), makespan parcial /LB, media, máx
y desviación de cargas restantes por máquina /LB, media y máx del trabajo
restante por job /LB, anchura relativa media de lo pendiente (incertidumbre
restante), número de elegibles / num_jobs.

### 3. Redes

- **Encoder por operación** φ: MLP(16 → 128 → 128) con LayerNorm.
- **Contexto agregado**: mean-pooling + max-pooling de los embeddings de las
  elegibles, concatenado con el contexto global → MLP → vector g (128).
- **Policy head**: score_i = MLP(φ_i ⊕ g) → softmax sobre elegibles.
  Invariante al tamaño: puntúa cada operación, sea cual sea su número.
- **Value head**: V = MLP(g). Sin dependencia de num_jobs/num_machines →
  desbloquea evaluación y transferencia entre tamaños.

Fase 2 opcional (solo si la fase 1 se queda corta): sustituir el pooling por
1-2 capas de atención sobre las elegibles (estilo Kool et al.). Empezar por
Deep Sets: más barato, menos riesgo, y suele bastar en JSP.

### 4. Entrenamiento (co-diseñado, no heredado)

- PPO estándar moderno: rollouts de N episodios → mini-batches de 256
  transiciones, 4 épocas, Adam lr 3e-4 con decay coseno, clip 0.2, GAE 0.95,
  entropía 0.01 con decay lineal, value loss con clipping (estilo PPO2),
  grad clip 0.5, inicialización ortogonal.
- gamma = 1.0 (horizonte finito, señal terminal sin descuento — viable aquí
  porque el crítico nace calibrado para esa escala, no injertado).
- **Muestreo de instancia por episodio** (en vez de bloques secuenciales por
  problema): mejor generalización y sin resets de optimizador — posible
  gracias a la invarianza al tamaño. Entrenamiento mixto 15×15 + 20×15.
- Evaluación greedy periódica (cada K episodios) para seleccionar el mejor
  modelo sin el ruido del muestreo de entrenamiento.

## Validación (con los instrumentos actuales)

1. **Test de invarianza** (unit test): la misma red procesa estados de 15×15,
   20×15 y 30×15 sin errores y con el mismo número de parámetros.
2. **Sanity de aprendizaje**: overfit a UNA instancia (200 episodios) — si no
   logra RE < 20% memorizando, hay un bug antes de seguir.
3. **Benchmark quick** contra la referencia v1 consolidada.
4. **Benchmark full** + tabla RE con LBs de literatura (TA15-20) + evaluación
   zero-shot cross-size (15×15 y 30×15, ahora posible).
5. Anclas deterministas: idénticas por construcción (v2 no toca el entorno).

**Criterio de éxito** (pre-registrado): RE medio ≤ 35% en TA15-20 (≥10 puntos
sobre MOR) con las 3 semillas, y cross-size sin degradación catastrófica.
**Criterio de abandono de fase 1**: si tras el hito 2 el overfit no funciona o
tras el hito 4 no supera al v1, revisar antes de escalar a atención.

## Hitos estimados

| Hito | Contenido | Esfuerzo | Estado |
|---|---|---|---|
| 1 | Revisión de este diseño (usuario) | — | ✔ aprobado 2026-07-03 |
| 2 | encoder + networks + agent con interfaz v1 + tests de invarianza | 1 sesión | ✔ commit 9bb52c2, 9/9 tests |
| 3 | ppo_trainer + sanity de overfit en 1 instancia | 1 sesión | ✔ TA1 500 eps: best 1508 → RE 22.5% (upper) / ~14% (E[Cmax]); curva sana, loss_v 302→11 |
| 4 | quick benchmark vs v1; iterar hiperparámetros base | 1-2 sesiones | ✔ quick: −14.28% vs v1 (commit d15a325), sin tuning |
| 5 | full + RE literatura + cross-size → decisión fase 2 (atención) | 1 sesión + ~3h máquina | ✔ **CRITERIO DE ÉXITO CUMPLIDO** — ver resultados |

## Resultados del hito 5 (2026-07-03)

- **Full vs v1 (idea-16-full)**: −7.41% de media, **mejor en 6/6** con 0 peores;
  varianza entre semillas ±126-180 → ±22-57. Anclas idénticas.
- **RE literatura (TA15-20)**: **28.0% media / 25.0% mejor semilla** (v1 final:
  38.6%/29.7%; MOR ≈ 46%). Criterio pre-registrado (≤35%) cumplido con margen.
- **Cross-size zero-shot** (checkpoint 20×15, best-of-64): 15×15 → RE 18-25%
  (MOR 30-43%); 30×15 → RE 26-38% (MOR 34-56%). Gana a MOR en 6/6 tamaños no
  vistos. Capacidad inexistente en v1.
- **Decisión fase 2 (atención)**: NO necesaria por ahora — Deep Sets supera el
  criterio. Siguientes palancas más baratas primero: entrenamiento mixto por
  muestreo de instancias (régimen nativo del diseño) y más episodios (el v2
  entrena ~5× más rápido y su curva de overfit no muestra plateau).

## Sonda: presupuesto de episodios (2026-07-03)

300 episodios/problema (vs 100 del tier estándar), 3 semillas: −9.34% vs
v2-full, **mejor en 6/6**, varianza ±13-24. **RE literatura: 16.4% media /
15.5% mejor semilla** (100 eps: 28.0%). La curva de escalado no muestra
plateau: 100→28.0%, 300→16.4%. El cross-size también mejora con el checkpoint
de 300 eps: 15×15 → RE 11-14.5% (antes 18-25%), 30×15 → 19-27% (antes 26-38%).
Contexto de literatura: fEABC ≈ 9.6% en TA15-20 — el constructivo queda a ~7
puntos de una metaheurística ABC. Fase 2 (atención) sigue sin justificarse:
el presupuesto aún paga. Sonda de 1000 episodios lanzada para mapear el techo.
(Nota: el primer intento de esta sonda fue inválido — quirk de --episodes 300
en main.py, corregido en run_benchmark con --episodes-per-problem.)

**Curva completa (1000 eps, 2026-07-03)**: RE 13.4% media / 12.3% mejor
semilla. La curva 100→28.0%, 300→16.4%, 1000→13.4% muestra rendimientos
decrecientes claros (×3.3 cómputo → −3 puntos, vs −11.6 del salto anterior):
el techo del presupuesto puro ronda ~11-12%. **El gatillo de la fase 2 se
activa**: para seguir bajando hacen falta expresividad (atención), datos
(mixto multi-tamaño) o hibridación (sembrar el TS con soluciones del v2).
Decisión de dirección pendiente del usuario.

## Cross-size ampliado (2026-07-03, checkpoint 300 eps entrenado solo en 20×15)

Zero-shot, best-of-64, RE por E[Cmax] vs LB crisp: 15×15 → 11-14.5%,
20×20 → 16.4%, 30×15 → 19-27%, 30×20 → 32.3%, 50×15 → 25.0%, 50×20 → 12.8%.
**Gana a MOR en 10/10 instancias de 6 tamaños distintos** sin haberlos visto.
Sin acantilado de degradación (episodios de 1000 ops OK, ~4 s/rollout).
Matiz: en las clases 50×N los LB son relativamente más alcanzables (el TS de
la literatura baja a RE ~0-2%), así que la distancia al estado del arte allí
es mayor de lo que sugiere el RE. La variante multi-tamaño del entrenamiento
mixto queda como palanca natural para cerrar la brecha en 30×20.

## Cross-size con checkpoint 1000 eps (2026-07-03)

Mejora casi en todo respecto al de 300 eps: 15×15 → 7.0-14.4%, 20×20 → 9.6%,
30×15 → 13.9%, 30×20 → 24.5% (antes 32.3%), 50×20 → 15.1%. Más entrenamiento
in-size también mejora la transferencia. El 30×20 sigue siendo el punto débil
→ objetivo del experimento B (mixto multi-tamaño), decidido con el usuario:
B antes que A (atención), con la hibridación al final.

## Experimento B: mixto multi-tamaño (2026-07-04)

3000 episodios sobre 12 instancias de 3 tamaños (15×15+20×15+20×20), 3
semillas, vs especialista 1000ep (solo 20×15). **El especialista gana en
TODO** (RE mid, mismas instancias): 15×15_05 8.7 vs 15.5; 20×20_05 15.9 vs
20.0; 30×15_01 13.9 vs 19.6; 30×20_01 24.5 vs 30.6; 50×20_01 15.1 vs 19.2 —
incluso en los tamaños que el multisize entrenó y el especialista no.
Conclusión provisional: **profundidad por instancia > diversidad de tamaños**;
la hipótesis "más diversidad de datos mejora también el in-size" queda
refutada a este presupuesto (in-size: multisize +3.2% peor). Confounder
pendiente: 250 eps/instancia vs 1000 — variante con presupuesto igualado
(12000 eps) lanzada para cerrar B. Si se confirma, la fase 2 (atención)
recupera el gatillo para el in-size, y el claim elegante del paper es el del
especialista: "entrenado en un tamaño, generaliza a toda la parrilla".

## Sonda: entrenamiento mixto (2026-07-03)

Mismo presupuesto (400 episodios), muestreo de instancia por episodio, 3
semillas (scripts/train_v2_mixed.py): media global 1859.9 vs 1877.5 del
secuencial por bloques → **paridad dentro del ruido** (−0.9%; mejor en 3/6,
peor en 3/6). En instancias del MISMO tamaño el régimen mixto no aporta;
el pipeline por bloques sigue siendo el estándar para el benchmark. La
variante con potencial real es el mixto MULTI-TAMAÑO (15×15 + 20×15 juntos,
solo posible con este régimen) — pendiente, con la vista puesta en mejorar
el cross-size. Dato operativo: el entrenamiento mixto completo tarda ~6.5
min (400 eps), útil para iteración rápida de hiperparámetros.

## Riesgos conocidos

- El muestreo por episodio cambia la dinámica respecto al v1 (que entrena por
  bloques con transferencia): si generaliza peor de lo esperado, hay fallback
  a bloques mezclados.
- best-of-N en evaluación se hereda del v1 (idea-16) — aplicar igual al v2
  para comparación justa.
- La banda RE 25-35% es la referencia realista de métodos constructivos
  aprendidos en JSP crisp; el setting de intervalos puede desplazarla. El
  criterio de éxito se fija contra MOR, no contra el TS (liga distinta).
