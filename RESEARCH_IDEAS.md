# Registro de ideas de investigación

Bucle de mejora del agente PPO para JSP con intervalos. Cada iteración propone
una idea, la implementa, la evalúa con el benchmark y la acepta o descarta.
Este archivo es la memoria del bucle: **toda idea probada queda registrada
aquí con su resultado, se acepte o no.**

## Protocolo (pre-registrado — no cambiar entre iteraciones)

1. **Una idea por iteración**, con diff pequeño y una hipótesis medible.
2. **Filtro (quick)**: `run_benchmark.py --tier quick --seeds 2,3 --tag idea-NN-quick`,
   comparar contra la referencia quick. Si la media es **> +3% (peor)** → descartar
   ya (rollback del código, se registra el resultado).
3. **Confirmación (full)**: si pasa el filtro, `--tier full --tag idea-NN-full`,
   comparar contra la referencia full. **Aceptar solo si**: media ≤ −3%, **o**
   mejor en ≥3 problemas con 0 peores. En cualquier otro caso → descartar.
4. **Aceptada** → commit del código + JSON del benchmark + este archivo; la
   referencia full pasa a ser el JSON de esta idea.
   **Descartada** → `git restore` del código; se commitea solo este archivo
   (y el JSON del intento, para el histórico).
5. **Invariantes**: las anclas deterministas (SPT/LPT/MOR/MWKR) deben ser
   idénticas a la referencia. Si una idea necesita cambiar la semántica del
   entorno, se marca como `[CAMBIA-ENTORNO]` y se regenera la referencia.
   Los scripts de benchmark y los tiers **no se tocan** desde el bucle.

## Referencia actual

- **Full**: `benchmarks/idea-16-full__059b4ee__*.json`
  (research + idea-16 best-of-64; makespan medio por problema ≈ 1969–2106)
- **Quick**: `benchmarks/idea-16-quick__059b4ee__*.json`
  (semillas 2,3; 30 episodios)

Referencias anteriores: candidato-fixes-full__7805b6e (hasta idea-04),
idea-04-full__c263095 (hasta idea-05), idea-05-full__1a20609 (hasta idea-16).

## Historial de ideas

| ID | Fecha | Idea | Quick (dif. media) | Full (dif. media) | Decisión | Commit |
|----|-------|------|--------------------|-------------------|----------|--------|
| idea-01 | 2026-07-03 | Suelo del decaimiento de entropía 10% → 30% (ppo_agent.py:403, factor 0.9→0.7) | **+9.87%** (peor en 2/2) | no ejecutado | **Descartada (quick)** | — |
| idea-02 | 2026-07-03 | gae_lambda 0.95 → 0.98 (main.py agent_params, modo batch) | **+88.44%** (peor en 2/2, std ±2500: divergencia) | no ejecutado | **Descartada (quick)** | — |
| idea-03 | 2026-07-03 | Value loss MSE → Huber/SmoothL1 (ppo_agent.py, ambas rutas de update) | −2.85% (pasó el filtro; std ±752→±397) | **+7.59%** (peor en 5/6) | **Descartada (full)** | — |
| idea-04 | 2026-07-03 | local_improvement_weight 0.15 → 0.3 (main.py reward_params, modo batch) | **−7.74%** (mejor en 2/2) | **−1.89%** (mejor en 3/6, peor en 0) | **ACEPTADA** (regla: ≥3 mejor, 0 peor) | 1a20609 |
| idea-05 | 2026-07-03 | Alinear resto de pesos batch con adaptive.py (idle 0.15, critical 0.05, balance 0.15, progress 0.05) | **−6.82%** (mejor en 2/2) | **−5.10%** (mejor en 5/6, peor en 0) | **ACEPTADA** | e010e08 |
| idea-06 | 2026-07-03 | local_improvement_weight 0.3 → 0.4 | **+26.92%** (peor en 2/2) | no ejecutado | **Descartada (quick)** | — |
| idea-07 | 2026-07-03 | Mini-batches de 32 en la ruta de update estándar (paso por batch en vez de por muestra) | **+92.46%** (peor en 2/2, aprendizaje casi nulo) | no ejecutado | **Descartada (quick)** | — |
| idea-08 | 2026-07-03 | K_epochs 4 → 2 | **+48.17%** (peor en 2/2) | no ejecutado | **Descartada (quick)** | — |
| idea-09 | 2026-07-03 | K_epochs 4 → 8 | **+61.51%** (peor en 2/2) | no ejecutado | **Descartada (quick)** | — |
| idea-10 | 2026-07-03 | Conectar GapPenaltyComponent a adaptive (peso 0.1) | **+24.36%** (peor en 2/2) | no ejecutado | **Descartada (quick)** | — |
| idea-11 | 2026-07-03 | Propuesta A: anexar 4 features de incertidumbre (widths + midpoint, índices 10-13) | **+9.11%** (peor en 2/2; anclas idénticas) | no ejecutado | **Descartada (quick)** | — |
| idea-12 | 2026-07-03 | A2 parte 1: normalizar features temporales por el límite inferior del problema | **+112.65%** (peor en 2/2, aprendizaje colapsado) | no ejecutado | **Descartada (quick)** | — |

| idea-13 | 2026-07-03 | Rediseño conjunto: mini-batches 32 + lr compensado (a: lr 1e-3 → **+14.75%**; b: lr 3e-3 → **+232%**, divergencia) | peor en 2/2 en ambas configs | no ejecutado | **Descartada (quick, barrido acotado)** | — |
| idea-14 | 2026-07-03 | gamma 0.99 → 0.999 (señal terminal del makespan: 0.99^300 ≈ 0.05 la borra) | **+3.96%** (borderline: peor en 1, ruido en 1) | no ejecutado | **Descartada (quick)** | — |

Notas idea-14: el fallo más suave de todos los ejes nuevos — la teoría es sólida
(el descuento borra la señal terminal en episodios de 300 pasos) pero 0.999
también multiplica ~5× la escala de los retornos que ve el crítico. Probar la
dosis intermedia 0.995 (señal ×0.22 en vez de ×0.05, escala más contenida) → idea-15.

Notas idea-13: el barrido acota la ventana — 1e-3 aprende lento, 3e-3 explota;
el mejor punto intermedio como mucho EMPATA con el régimen actual, y empatar no
supera el umbral de aceptación. El rediseño conjunto del update queda cerrado:
el régimen por muestra actual no es un accidente, es competitivo.

| idea-15 | 2026-07-03 | gamma 0.99 → 0.995 (dosis intermedia de idea-14) | **+14.70%** (peor en 2/2) | no ejecutado | **Descartada (quick)** | — |
| idea-16 | 2026-07-03 | Inferencia best-of-64 en evaluación de test (1 greedy + 63 muestreos, mejor por peor caso) | **−6.26%** (mejor en 2/2) | **−3.64%** (mejor en 3/6, peor en 0; std ↓) | **ACEPTADA** | ver commit |

Notas idea-16: cambia el procedimiento de INFERENCIA (más cómputo en test,
estándar en neural CO), no el entrenamiento. Motivada por el hallazgo de que
el mejor makespan solía venir de muestreos afortunados: la política estocástica
vale más como distribución que como su argmax. En 2 problemas el best-of-64 no
superó al greedy (0.00%) — coherente con ese diagnóstico.

Notas idea-14/15: eje de gamma cerrado en ambas direcciones y sin monotonía
(0.995 peor que 0.999) — el descuento 0.99 es otro parámetro co-adaptado: las
escalas de los componentes de recompensa (makespan_scale, etc.) y el crítico
están calibrados alrededor de él. Refuerza la conclusión general de abajo.

## Conclusión tras 15 iteraciones (2026-07-03)

El sistema es un óptimo local FUERTEMENTE CO-ADAPTADO: inicialización, learning
rate, régimen de updates por muestra y escala cruda de las features encajan
entre sí. Cualquier perturbación aislada de escala (normalizar features:
+112%), de volumen de updates (batching/K_epochs: +48% a +92%) o de señal
(entropía, gap penalty: +9% a +27%) lo rompe. Las únicas mejoras vinieron de
ajustar la MEZCLA de recompensas dentro del régimen existente (idea-04/05,
−7% acumulado).

Implicación: no quedan mejoras de una variable. El siguiente salto requiere
un REDISEÑO CONJUNTO (features normalizadas + arquitectura con capa de
normalización de entrada + lr y updates re-tuneados a la vez), que es un
mini-proyecto con barrido propio, no una iteración del bucle. Ver
RESEARCH_PROPOSALS.md — decisión y presupuesto del usuario.

Notas idea-11: el diseño de compatibilidad funcionó (anclas idénticas con ancho
14), pero LECCIÓN CLAVE: las 4 features eran combinaciones LINEALES de features
ya presentes (width = upper − lower; midpoint = (lower+upper)/2) — la primera
capa de la red ya puede formarlas, así que no aportaban información, solo
entradas redundantes que ralentizan el arranque (+9% a 30 episodios). Un retry
con sentido necesita información NO derivable linealmente de la fila:
ratios de incertidumbre relativa (width/midpoint) y/o normalización por el
límite inferior del problema (contexto a nivel de problema que la fila no
contiene). Requiere decisión del usuario (ver RESEARCH_PROPOSALS.md).

Notas idea-10: penalizar huecos entra en conflicto con esperas estratégicas
(dejar hueco para un trabajo crítico es a menudo lo correcto). La composición
de reward actual (idea-05) parece un óptimo local robusto: añadir componentes
o mover pesos individualmente lo empeora. Próximos pasos con mejor pinta son
de diff mediano: features enriquecidas (sin romper índices de heurísticas),
mini-batching con lr compensado, o reparar+conectar prioritized replay.

Notas idea-07/08/09: EJE CERRADO — la mecánica de updates (K_epochs=4 con pasos
por muestra) es un equilibrio muy fino: reducir el volumen de pasos (batches,
menos épocas) O aumentarlo (más épocas) degrada fuerte. No insistir en dials de
K_epochs/batching sin rediseñar el update completo (lr, clipping y épocas a la
vez). El eje productivo sigue siendo el reward shaping (idea-04/05 aceptadas).

Notas idea-06: la relación no es monótona — 0.4 es claramente peor que 0.3.
El óptimo del peso de local_improvement está alrededor de 0.3; este eje queda
explorado (0.15 < 0.3 > 0.4) y no merece más barridos finos por ahora.

Notas idea-07: promediar en mini-batches de 32 redujo los pasos de optimizador
por episodio de ~1200 a ~40 con el mismo lr → la magnitud efectiva de
actualización cayó ~30× y el agente casi no aprende (+92%, makespans cerca de
aleatorio). Variante pendiente si se retoma: mini-batches + lr escalado
(p.ej. 1e-3) o batches pequeños (8). El paso por muestra actual actúa de facto
como un lr efectivo alto.

Notas idea-04/05: el eje ganador es el reward shaping — los pesos que main.py
pasaba en batch eran anteriores al ajuste de adaptive.py. Con ambas aceptadas,
el makespan medio de referencia bajó de ≈2129–2397 a ≈1994–2238 (−7% acumulado
aprox. respecto a la referencia post-fixes).

Notas idea-01: con 30 episodios más entropía final = menos explotación, así que
el quick puede estar sesgado contra ideas que aumentan exploración; aún así el
+9.9% es demasiado grande para justificar 3h de full. Si se retoma, considerar
probarla directamente en full.

Notas idea-02: degradación catastrófica (+88%, std ±2500) — no parece ruido sino
divergencia del entrenamiento en al menos una semilla: λ alto aumenta la varianza
de las ventajas y este agente no tiene clipping de value loss. Si se quiere
retomar el eje de gae_lambda, probar hacia abajo (0.90) o añadir antes
estabilización del value update.

Notas idea-03: caso de libro del valor del gate en dos etapas — el quick la
habría aceptado (−2.85%, menos varianza) pero el full la rechaza con claridad
(+7.6%, peor en 5/6). Interpretación: Huber estabiliza el crítico al inicio pero
acota sus gradientes y a 100 episodios el value network aprende demasiado lento.
El eje "estabilizar el crítico" no queda descartado, pero no vía Huber a secas
(alternativas: value clipping estilo PPO2, o lr separado más alto para el crítico).

## Backlog de ideas candidatas (orientativo, no vinculante)

- ~~Pesos del reward adaptive: reducir local_improvement de 0.4~~ **Moot**: en
  modo batch main.py ya sobreescribe los pesos (local_improvement=0.15); el 0.4
  del código solo aplica cuando no se pasan parámetros explícitos. Una variante
  válida sería barrer los pesos que main.py pasa (p.ej. local_improvement 0.15→0.3).
- **Suelo y forma del decaimiento de entropía**: hoy lineal hasta 10%; probar
  suelo más alto (20-30%) o decaimiento coseno.
- **Barrido de gae_lambda**: 0.90 / 0.98 (ahora que la rama gae_lambda=0
  funciona, el parámetro es fiable).
- **Conectar improved_features**: existe un extractor de 14 características de
  intervalos (jobshop_rl/models/improved_features.py) que hoy es código muerto;
  integrarlo requiere alinear dimensiones de red (14 vs 10). Diff mediano.
- **K_epochs / learning rate**: valores actuales heredados, sin barrido conocido.
- **Normalización de ventajas por mini-batch** en lugar de por episodio.
- **Prioritized replay**: el módulo existe sin conectar
  (jobshop_rl/agents/prioritized_replay.py) pero tiene bugs conocidos (GAE mal
  formado, pesos IS incorrectos) — arreglarlo antes de conectarlo. Diff grande.
- **[BLOQUEADA] Curriculum entre tamaños / eval cross-size**: requiere
  representación de estado independiente del tamaño (la red de valor depende
  de num_jobs y num_machines).
