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

- **Full**: `benchmarks/idea-05-full__1a20609__*.json`
  (research + idea-05; makespan medio por problema ≈ 1994–2238)
- **Quick**: `benchmarks/idea-05-quick__1a20609__*.json`
  (semillas 2,3; 30 episodios)

Referencias anteriores: candidato-fixes-full__7805b6e (hasta idea-04),
idea-04-full__c263095 (hasta idea-05).

## Historial de ideas

| ID | Fecha | Idea | Quick (dif. media) | Full (dif. media) | Decisión | Commit |
|----|-------|------|--------------------|-------------------|----------|--------|
| idea-01 | 2026-07-03 | Suelo del decaimiento de entropía 10% → 30% (ppo_agent.py:403, factor 0.9→0.7) | **+9.87%** (peor en 2/2) | no ejecutado | **Descartada (quick)** | — |
| idea-02 | 2026-07-03 | gae_lambda 0.95 → 0.98 (main.py agent_params, modo batch) | **+88.44%** (peor en 2/2, std ±2500: divergencia) | no ejecutado | **Descartada (quick)** | — |
| idea-03 | 2026-07-03 | Value loss MSE → Huber/SmoothL1 (ppo_agent.py, ambas rutas de update) | −2.85% (pasó el filtro; std ±752→±397) | **+7.59%** (peor en 5/6) | **Descartada (full)** | — |
| idea-04 | 2026-07-03 | local_improvement_weight 0.15 → 0.3 (main.py reward_params, modo batch) | **−7.74%** (mejor en 2/2) | **−1.89%** (mejor en 3/6, peor en 0) | **ACEPTADA** (regla: ≥3 mejor, 0 peor) | 1a20609 |
| idea-05 | 2026-07-03 | Alinear resto de pesos batch con adaptive.py (idle 0.15, critical 0.05, balance 0.15, progress 0.05) | **−6.82%** (mejor en 2/2) | **−5.10%** (mejor en 5/6, peor en 0) | **ACEPTADA** | e010e08 |
| idea-06 | 2026-07-03 | local_improvement_weight 0.3 → 0.4 | **+26.92%** (peor en 2/2) | no ejecutado | **Descartada (quick)** | — |

Notas idea-06: la relación no es monótona — 0.4 es claramente peor que 0.3.
El óptimo del peso de local_improvement está alrededor de 0.3; este eje queda
explorado (0.15 < 0.3 > 0.4) y no merece más barridos finos por ahora.

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
