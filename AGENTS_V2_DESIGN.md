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

## Configuración paramétrica con irace (2026-07-05)

Racing de 330 experimentos (irace 4.4.3, 8 parámetros, semillas como
instancias, fidelidad 1×TA11×300 eps + eval TA15-17 best-of-16, 16.5 h).
**Las 5 élites coinciden** en un régimen de aprendizaje más rápido que la
default: lr 7-9e-4 (default 3e-4), clip 0.3 (0.2), minibatch 128 (256),
update cada 2 episodios (4), GAE λ 0.90 (0.95); entropía ~0.004-0.017;
ancho insensible (64/128/256 entre élites); K_epochs=4 confirmado.

Élite #27 (mejor por suma de rangos): lr 8e-4, entropy 0.0171, clip 0.3,
kepochs 4, minibatch 128, update-every 2, gae 0.90, hidden 64.

**Advertencia pre-registrada**: óptimo a fidelidad de tuning ≠ óptimo a
1000 eps (lección de la atención). La adopción depende EXCLUSIVAMENTE de la
confirmación full (v2-elite27-1000ep vs v2-full-1000ep, regla estándar).
Inyección vía env vars DEEPLJSP_V2_* (AgentFactory).

**VEREDICTO CONFIRMACIÓN (2026-07-05)**: la élite #27 a 1000 eps da
+1.66% (5/6 ruido, 1 peor; RE 14.5% vs 13.4%) con entrenamiento ~60% más
lento → NO se adopta. La advertencia se materializó: el óptimo de baja
fidelidad no transfiere al punto de operación. **La configuración default
(valores estándar de literatura) queda validada como robusta** — resultado
de sensibilidad valioso para el paper: el rendimiento del v2 no depende de
tuning fino. La default sigue siendo la configuración final; los pools se
completan con los checkpoints actuales.

## Próxima fase (plan acordado con el usuario, 2026-07-05)

1. **Doble campaña irace con default sembrada** (configurationsFile):
   - Deep Sets: espacio estándar, default como candidata inicial
     (scenario_deepsets.txt), 330 experimentos (~16 h).
   - Atención: espacio ampliado con capas {1,2,3} y cabezas {2,4,8}, default
     L=2/H=4 sembrada (scenario_attention.txt), 400 experimentos (~20-24 h,
     sus evaluaciones son ~30% más lentas).
   - Confirmación a 1000 eps de las top élites de CADA campaña, y después la
     comparación arquitectónica final tuned-vs-tuned.
   - Orden: tras completar los pools (competirían por CPU).
2. **COMPLETADO (2026-07-06) — Baseline GP (hiper-heurística)**:
   infraestructura en jobshop_rl/heuristics/gp_rule.py +
   scripts/evolve_gp_rule.py. Evolución completa: pop 100 × 50 gens,
   3 semillas, mismas TA11-14 que el v2 (comparación justa
   simbólico-vs-neuronal), sin tuning paramétrico (decisión: es un baseline
   y el v2 tampoco usa configuración afinada; salvaguarda de varianza entre
   semillas no activada).
   - **Cómo funciona** (línea Branke et al., IEEE TEC 2016): un INDIVIDUO
     es una regla de despacho completa = árbol de expresión que asigna
     prioridad a cada operación elegible; se despacha la de MENOR
     prioridad. Hojas = 9 terminales interval-aware por operación (PT,
     PTW, EST, ESTW, WKR, WKRW, NOR, SLACK, ONE — las anchuras W hacen a
     la regla sensible a la incertidumbre); nodos internos = +, −, ×,
     división protegida, min, max, neg. SPT ≡ árbol `PT` y MWKR ≡
     `neg(WKR)`: ambas se inyectan como individuos semilla. FITNESS = RE
     medio del rollout determinista sobre TA11-14 (mismo entorno que el
     RL). EVOLUCIÓN generacional: elitismo 2, selección por torneo de 4,
     cruce de subárboles (p=0.8) o mutación de subárbol (p=0.2), y
     control de bloat: >40 nodos ⇒ fitness ∞. La regla ganadora es
     drop-in de HeuristicStrategy (misma interfaz que SPT/MOR/GT).
   - **Fitness entrenamiento (TA11-14)**: s1 15.60%, s2 15.62%, s3 15.87%
     — varianza entre semillas casi nula, settings convencionales bastan.
   - **Generalización a las 70 Taillard** (1 rollout determinista por
     instancia, RE por punto medio):

     | Clase | GP s1 | GP s2 | GP s3 |
     |---|---|---|---|
     | 15×15 | 16.0% | 16.5% | 18.6% |
     | 20×15 | 18.7% | 18.4% | 18.5% |
     | 20×20 | 19.4% | 21.2% | 20.0% |
     | 30×15 | 20.9% | 21.8% | 22.7% |
     | 30×20 | 25.0% | 26.9% | 25.7% |
     | 50×15 | 14.5% | 15.1% | 15.2% |
     | 50×20 | 15.1% | 16.3% | 15.7% |
     | **Global** | **18.5%** | 19.5% | 19.5% |

   - **Lectura**: la regla s1 (18.5% global, UN solo rollout determinista)
     bate a GT-MWKR (29.4%) en ~11 puntos y a todas las reglas fijas;
     generaliza cross-size sin reentrenar (entrenó solo en 20×15 y su mejor
     clase es 50×15). La escalera de baselines queda: reglas fijas (45.4%
     MOR) < GT-MWKR (29.4%) < **GP evolucionado (18.5%)** < v2
     best-of-1024 (12.7%). El v2 mantiene ~6 puntos de ventaja sobre el
     mejor baseline aprendido interpretable — ese margen es la contribución
     neta de la red + best-of-N para el paper.
   - Mejor regla (s1, benchmarks/gp_rule_seed1.json; s2/s3 en JSONs
     hermanos): árbol de 40 nodos dominado por WKR/EST/SLACK×PT — MWKR
     corregido por inicio temprano y holgura.
   - La regla es drop-in de HeuristicStrategy (misma interfaz que
     SPT/MOR/GT): integrarla en evaluador, gráficos o pools no requiere
     código nuevo. Pendiente menor: sección GP del paper (ablation de
     baselines aprendidos).
3. **COMPLETADO (2026-07-06) — Vectorización + GPU** (RTX 5060 Ti 16GB,
   torch 2.9.1+cu130). Perfil del rollout secuencial: el forward de la red
   (batch de 1) era el 64-77% del tiempo → batchear forwards es la palanca.
   Módulos NUEVOS (caminos secuenciales intactos):
   - jobshop_rl/agents_v2/batched_eval.py: best-of-N con N entornos en
     lockstep, un forward (N, M_max, 16) por paso, CPU o GPU. Misma
     semántica que evaluate_policy (muestra 0 greedy, resto estocásticas).
   - jobshop_rl/agents_v2/batched_train.py: drop-in de agent.train que
     recolecta los update_every episodios de cada ciclo PPO en lockstep
     (mismo algoritmo on-policy: esos episodios ya compartían pesos);
     buffer contiguo por episodio (requisito del GAE); greedy eval
     periódica como fila extra del lockstep.
   - **Verificación** (scripts/test_batched_eval.py, test_batched_train.py):
     greedy batcheado == greedy secuencial BIT-IDÉNTICO en CPU y GPU en
     15×15/20×15/30×20/50×20 (criterio bloqueante); calidad best-of-64 y
     de entrenamiento equivalente (ruido de semilla).
   - **Speedups medidos**: evaluación best-of-64: 5.5×/6.8× (CPU-batch/GPU)
     en 15×15, 4.7×/5.5× en 20×15, 2.9×/3.3× en 30×20, 2.0×/2.3× en 50×20
     (la fracción Python —encode+env.step— crece con el tamaño).
     Entrenamiento (100 eps, TA11): 1.74× CPU-batch, **3.01× GPU**.
   - scripts/train_eval_config.py acepta --batched/--device/--eval-samples
     (default = caminos secuenciales; la campaña irace en curso no se ve
     afectada).

4. **PREPARADO — Campaña irace SERIA a fidelidad de operación**
   (tuning/{scenario,parameters,configurations,target_runner}_serious.*):
   motivada porque dos campañas a fidelidad baja (300 eps) produjeron
   élites que no transfirieron a 1000 eps. Fidelidad: 2 instancias
   (TA11+TA12) × 1000 episodios con rutas batcheadas en GPU + eval
   best-of-64 en TA15-17; espacio reducido a 6 parámetros (kepochs=4 y
   hidden=128 fijados por insensibilidad observada), default sembrada,
   280 experimentos, ~1 día de cómputo estimado. ANTES DE LANZAR: sembrar
   también las élites supervivientes de la campaña Deep Sets en curso y
   revalidar que kepochs/hidden siguen insensibles en sus élites finales.
   DECISIÓN (2026-07-06): NO se lanza la campaña attention a fidelidad
   baja (scenario_attention.txt queda como referencia): el usuario pidió
   configuración seria a 1000 eps y el patrón élite-no-transfiere ya se
   observó dos veces; el presupuesto va a la campaña seria.

## Datos del modelo final (política de exclusión para experimentos posteriores)

- **Entrenamiento del checkpoint final** (especialista Deep Sets 1000 eps):
  **TA11-TA14** (tai20_15_01..04) — únicas instancias que han generado
  gradientes en el modelo final. Exclusión OBLIGATORIA en toda evaluación.
- **Desarrollo/validación**: **TA15-TA20** (tai20_15_05..10) — nunca
  entrenaron, pero TODAS las decisiones de configuración (16 ideas del bucle,
  Deep Sets vs atención, presupuesto) se seleccionaron con su rendimiento
  (test-set reuse). Exclusión RECOMENDADA de la evaluación principal; si se
  reportan, etiquetar como conjunto de desarrollo.
- Los modelos multisize (entrenaron además TA1-4 y TA21-24) y el sanity de
  overfit (TA1) fueron DESCARTADOS y no forman parte del modelo final.
- **Para el experimento híbrido con TS**: excluir además las 17 Taillard del
  tuning irace del TS (TA3, TA8, TA12, TA17, TA21, TA24, TA29, TA32, TA36,
  TA43, TA47, TA50, TA52, TA57, TA63, TA67, TA70). Conjunto limpio para ambos
  métodos: ~45-48 instancias con los 7 tamaños representados.

## FASE 2 (atención): VEREDICTO FINAL — no rentable a estos presupuestos (2026-07-04)

Ablación limpia (mismo código, flag DEEPLJSP_V2_ATTENTION; 2 bloques pre-LN,
4 cabezas), 3 semillas por punto:

| Punto | Deep Sets | Atención | Veredicto |
|---|---|---|---|
| Overfit TA1 500 eps | 1508 | 1534 | ligeramente peor, curva sana |
| Full 300 eps | RE 16.4% | RE 17.5% (+1.20%) | paridad (6/6 ruido) |
| Full 1000 eps | RE 13.4% | RE 15.0% (+1.62%) | paridad-peor (5/6 ruido, 1 peor) |

La hipótesis "la atención remonta con presupuesto" queda refutada: paridad o
peor en ambos puntos de operación con ~30% más de coste por episodio. El
pooling media+máx ya captura las interacciones necesarias a estas escalas.
**Configuración final del v2: Deep Sets, 1000 eps/problema, best-of-64 →
RE 13.4% media / 12.3% mejor semilla.** La implementación de atención queda
en el código (flag) y en la rama phase2-attention para la comparativa del
paper. Siguiente valor: hibridación con el TS del usuario (reservada al final
por decisión suya).

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
(12000 eps) lanzada para cerrar B.

**VEREDICTO FINAL B (2026-07-04, presupuesto igualado 1000 eps/instancia)**:
el especialista sigue ganando en las 5 instancias de comparación (RE mid,
multisize media de 3 semillas): 15×15_05 8.7 vs 9.5; 20×20_05 15.9 vs 18.5;
30×15_01 13.9 vs 16.1; 30×20_01 24.5 vs 28.3; 50×20_01 15.1 vs 15.7. B
cerrado sin confounders: la diversidad de tamaños no aporta; el claim del
paper es el del especialista ("entrenado en un tamaño, generaliza a toda la
parrilla"). La fase 2 (atención) recupera el gatillo → arrancada según el
plan acordado con el usuario.

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
