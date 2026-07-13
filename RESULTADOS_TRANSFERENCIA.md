# Generalización y transferencia de los generadores — resumen consolidado

Índice único de todos los hallazgos sobre (a) la caracterización de los
generadores de semillas y (b) la transferencia de sus soluciones a otros
modelos de incertidumbre. Datos en `benchmarks/`, figuras en
`benchmarks/figures/`, código en `scripts/` y en las carpetas
`transfer_experiment/` y `stochastic_experiment/`.

Fecha: 2026-07-13. Todo reproducible desde la rama `research`.

---

## 1. Caracterización de los 4 generadores (71 Taillard, pools de 1024)

Generadores, de peor a mejor: **graspmor** (MOR+ε) < **gtmwkr** (G&T+ε) <
**gp** (regla GP tuneada+ε) < **v2** (política RL).

| Eje | graspmor | gtmwkr | gp | v2 | Script / figura |
|---|---|---|---|---|---|
| RE medio pool | 51.1% | 30.4% | 21.4% | 21.2% | compare_generators.py |
| RE mejor individuo | 38.3% | 22.7% | 13.2% | 12.6% | fig_quality_diversity / fig_class_quality |
| Diversidad estructural | 0.78 | 0.88 | 0.92 | 0.95 | pool_diversity.py |
| σ_RE (dispersión) | 5.56 | 2.56 | 3.22 | 3.29 | pool_diversity.py |
| Anchura interv. (robustez) | 14.5% | 13.7% | 12.6% | 12.4% | pool_robustness.py / fig_robustness |
| Dominancia (media) | 0/71 | 0/71 | 34/71 | 37/71 | compare_generators.py |

**Hallazgos clave:**
- Escalera limpia y consistente en TODOS los ejes (calidad, mejor, diversidad,
  robustez): los dos generadores aprendidos (v2, gp) dominan a los heurísticos.
- **v2 y GP EMPATAN en calidad media** (21.2 vs 21.4), pero en el **mejor
  individuo** el v2 gana más claro (47/71 vs 23/71) — su ventaja vive en la
  cola del best-of-N (más diversidad estructural).
- **El GP GANA en las clases grandes 50×N** (invariante al tamaño; el v2 es
  especialista 20×15 y se degrada cross-size).
- Sin duplicados en ningún pool (unicidad ≈ 1.00). Combinar v2+GP por instancia
  (oracle) baja a 12.1% global.

---

## 2. Transferencia a otros modelos de incertidumbre

Las soluciones se generaron para el problema de **intervalo** (minimizan el
peor caso). Pregunta: ¿una secuencia buena en intervalo sigue siendo buena al
evaluarla bajo otra aritmética? (misma secuencia re-decodificada, sin
reentrenar). Referencia común: LB crisp de Taillard (válido para todos como
suelo; ver nota metodológica al final).

### 2.1 Crisp (determinista) — `transfer_experiment/`
`run_crisp_transfer.py` → `benchmarks/crisp_transfer.csv`,
`fig_crisp_transfer.png`, `fig_transfer_summary.png`.
- **Transferencia SIN pérdida.** Escalera idéntica (v2 12.4% / gp 13.0% mejor).
- Sin precio de robustez (RE crisp ≈ RE intervalo, incluso ~0.3 pts menor).
- Correlación de rankings intervalo→crisp **~0.995**.

### 2.2 Fuzzy triangular — `transfer_experiment/`
TFN = (lo_intervalo, valor_crisp, up_intervalo). `run_fuzzy_transfer.py` →
`benchmarks/fuzzy_transfer.csv`, `fig_transfer_summary.png`.
- **Transferencia SIN pérdida** (aún más limpia). Escalera idéntica
  (v2 12.6% / gp 13.2% mejor E[C]).
- Correlación de rankings intervalo→fuzzy **~0.998**.

### 2.3 Estocástico (Monte Carlo, uniforme) — `stochastic_experiment/`
`run_stochastic.py` + `run_spectrum.py` → `benchmarks/stochastic_transfer.csv`,
`stochastic_spectrum.csv`, `fig_stochastic_risk.png`, `fig_risk_spectrum.png`.
- Modelo GENUINAMENTE distinto (no una interpolación del intervalo).
- Escalera preservada bajo esperado y CVaR-95.
- **Hallazgo diferenciado — gradiente de riesgo monótono** (correlación
  intervalo→objetivo, v2): optimista **0.972** < esperado **0.980** <
  CVaR-95 **0.986**. Confirmado en los 4 generadores. Las semillas de
  intervalo (peor-caso-óptimas) se alinean tanto mejor cuanto más
  riesgo-averso es el objetivo. 139/140 instancias con CVaR>esperado.
- **Negativo honesto**: la simetría hipotetizada "bordes del intervalo ↔ colas"
  NO se sostuvo (upper→optimista 0.972 > lower→optimista 0.968; el upper es
  mejor rankeador en todo).

**Síntesis transferencia**: los generadores de intervalo (v2 y GP) inicializan
crisp y fuzzy **sin pérdida**, y estocástico **bien** (>0.98) con alineamiento
creciente hacia el riesgo-averso. Resultado de generalización fuerte para los
dos papers, y conexión con robust/stochastic scheduling.

---

## 3. Implicaciones para los papers

- Refuerza a ambos: "nuestros generadores de intervalo transfieren como
  inicializadores a JSP determinista, fuzzy y estocástico".
- El GP luce como método PORTABLE (regla directa sobre crisp/fuzzy — pendiente
  medirlo, P1). El v2 domina en best-of-N y diversidad.
- El gradiente de riesgo conecta con la literatura de scheduling robusto.

## 4. Experimentos pendientes (apuntados)
- `transfer_experiment/README.md`: P1 (regla GP directa sobre crisp, gratis),
  P2 (vs generadores crisp-nativos), P3-B (regla GP viva sobre fuzzy).
- `stochastic_experiment/README.md`: comparar vs generador estocástico-nativo.
- TFN asimétrico (escorar el modal) como análogo fuzzy de la aversión al riesgo.

## Nota metodológica — el LB crisp como referencia común
Se usa el LB crisp de Taillard para calcular el RE de TODOS los modelos. Es un
suelo VÁLIDO (todas las medidas ≥ makespan crisp ≥ LB crisp) y permite
comparar RE entre modelos. NO es la cota más ajustada para los no-crisp, así
que el RE sobreestima la distancia al óptimo específico de cada modelo (las
soluciones son al menos tan buenas como el RE indica). Crucialmente, las
CONCLUSIONES (transferencia, ranking, escalera) no dependen del LB — solo fija
la escala absoluta. Para claims de optimalidad por modelo haría falta la cota
inferior específica de cada uno (existe en la literatura de IJSP).
