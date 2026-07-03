# Propuestas de diseño — siguientes pasos del bucle de investigación

Estado tras 10 iteraciones del bucle (ver RESEARCH_IDEAS.md): el espacio de
ajustes de una línea está agotado (2 aceptadas en reward shaping, 8 descartadas
con motivo). Las tres direcciones siguientes requieren decisiones de diseño.

---

## Propuesta A — Features de incertidumbre para la política (RECOMENDADA)

**Qué**: hoy la política ve, para cada operación elegible, los bounds de
duración/inicio/trabajo restante (10 features), pero NO ve la **anchura** de
los intervalos — es decir, no puede distinguir una operación de duración
`[10,11]` (casi determinista) de una `[5,16]` (muy incierta) con el mismo
punto medio. Para un agente que optimiza el peor caso, esa es exactamente la
información que debería usar. Añadimos 4 features por operación:

1. `dur_width` — anchura del intervalo de duración (normalizada)
2. `start_width` — anchura del earliest start (incertidumbre acumulada aguas arriba)
3. `remaining_width` — anchura del trabajo restante
4. `dur_midpoint` — punto medio de duración (normalizado)

El extractor `ImprovedOperationFeatures` (jobshop_rl/models/improved_features.py)
ya calcula exactamente esto — está implementado y nunca conectado.

**Cómo (diseño de compatibilidad)**: NO reemplazar el layout actual (las
heurísticas leen los índices 0-9 y `ORToolsHeuristic` hace `int(feature[0])`,
y el extractor mejorado normaliza índices → los rompería). En su lugar,
**anexar** las 4 features nuevas al final (índices 10-13):

- `OperationFeatures.to_array()` (data_models.py): añadir las 4 columnas al
  final del caso intervalo → ancho 14. Caso escalar sin cambios (7).
- `HeuristicStrategy._is_interval_features` (heuristics/strategies.py:57):
  cambiar `shape[1] == 10` por `shape[1] >= 10` (los índices 0-9 no se mueven).
- Dimensiones hardcodeadas: factory.py:162 y job_shop_env.py:204
  (`10 if intervals else 7` → `14 if intervals else 7`) y
  data_models.py `feature_dimension`.

**Coste**: ~60 líneas en 4 archivos. Validación: pytest + quick + full ≈ 3.5 h
de máquina. **Riesgo**: bajo (anclas verificables: si SPT/MWKR cambian, el
diseño de compatibilidad falló y se ve al instante).

**Advertencia**: los checkpoints antiguos (redes de entrada 10) dejan de ser
cargables en problemas con intervalos. Asumible en fase de investigación.

**Por qué es la recomendada**: es LA dirección alineada con la contribución
científica del proyecto (decisiones conscientes de la incertidumbre), reutiliza
código propio ya escrito y testeado, y es la más barata de las tres.

---

## Propuesta B — Rediseño del update con lr compensado

**Qué**: la ruta de update activa da un paso de optimizador POR MUESTRA
(~1200 pasos/episodio). El bucle demostró (ideas 07/08/09) que es un equilibrio
frágil: cualquier reducción del volumen de pasos sin compensar el learning rate
colapsa el aprendizaje. El rediseño correcto cambia tres cosas A LA VEZ:
mini-batches (32) + lr escalado (~10×: 3e-4 → 3e-3) + posiblemente épocas.

**Cómo**: es un mini-proyecto de tuning, no una idea del bucle: barrido de
lr ∈ {1e-3, 3e-3} × batch ∈ {16, 32} con el tier quick (4 × 25 min) y full
solo para el ganador (+3 h).

**Coste**: ~5-6 h de máquina + una tarde de trabajo. **Riesgo**: medio-alto —
la evidencia del bucle sugiere que la zona es hostil; puede acabar en empate.
**Payoff si funciona**: updates ~10× más rápidos (menos overhead por paso) y
menos varianza entre semillas; abre la puerta a más episodios al mismo coste.

---

## Propuesta C — Reparar y conectar el prioritized replay

**Qué**: jobshop_rl/agents/prioritized_replay.py (394 líneas) existe sin
conectar y con bugs conocidos (deltas de GAE mal formados, pesos de importance
sampling incorrectos, `insert(0,...)` O(T²)). Repararlo e integrarlo tras un
flag `use_replay` en PPOAgent.

**Cómo**: (1) arreglar los 3 bugs documentados en la code review; (2) adaptar
la interfaz a la de PPOMemory real (`get_tensors`, `features_list`); (3) flag
en agent_params; (4) benchmark.

**Coste**: 1-2 días de trabajo + benchmarks. **Riesgo**: alto — PPO es
on-policy y reutilizar episodios viejos introduce sesgo que el clipping solo
mitiga en parte. **Consideración científica**: cambia el algoritmo estudiado;
es una línea de investigación en sí (eficiencia muestral), no una mejora
incremental. Decidir si encaja en la narrativa del trabajo antes de invertir.

---

## Recomendación

**A → (si funciona, considerar C como línea nueva) → B solo si la velocidad
de entrenamiento se vuelve el cuello de botella.** A es barata, de bajo riesgo,
reutiliza trabajo propio y es la única de las tres que además fortalece la
historia científica del proyecto (el agente usa la estructura de intervalos,
no solo el peor caso).
