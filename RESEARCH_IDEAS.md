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

- **Full**: `benchmarks/candidato-fixes-full__7805b6e__20260702_124523.json`
  (rama fix/code-review-findings; makespan medio por problema ≈ 2129–2397;
  gap medio vs límite inferior ≈ 77.4%)
- **Quick**: `benchmarks/candidato-fixes__413f0a8__20260702_105626.json`
  (semillas 2,3; 30 episodios)

## Historial de ideas

| ID | Fecha | Idea | Quick (dif. media) | Full (dif. media) | Decisión | Commit |
|----|-------|------|--------------------|-------------------|----------|--------|
| — | — | (ninguna probada aún) | — | — | — | — |

## Backlog de ideas candidatas (orientativo, no vinculante)

- **Pesos del reward adaptive**: tras corregir la fuga de estado, el peso 0.4
  de local_improvement puede estar sobredimensionado; probar 0.15-0.2.
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
