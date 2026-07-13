# Experimento de transferencia intervalo → estocástico (Monte Carlo)

Aislado (no toca transfer_experiment/ ni nada más). Complementa la
transferencia crisp/fuzzy con un modelo de incertidumbre GENUINAMENTE
distinto: duraciones aleatorias (uniforme en [lo,up]), evaluadas por Monte
Carlo con números aleatorios comunes (misma nube de K=300 escenarios por
instancia para todas las secuencias).

A diferencia de crisp/fuzzy (casos particulares del intervalo → transferencia
sin pérdida, Spearman ~1.0), aquí el objetivo puede DIVERGIR del peor caso:
- ESPERADO (riesgo-neutral): media del makespan sobre los escenarios.
- CVaR-95 (riesgo-averso): media del peor 5% de escenarios.

## Ficheros
- `decode_vec.py` — decodificador semiactivo vectorizado (numpy) + E[·] y CVaR.
- `run_stochastic.py` — experimento → `benchmarks/stochastic_transfer.csv`.
- `plot_stochastic.py` — figura del hallazgo → `benchmarks/figures/fig_stochastic_risk.png`.

## Resultado (2026-07-13)

**La escalera se conserva** bajo ambos objetivos (RE mejor individuo, global):
- Esperado: graspmor 38.6 > gtmwkr 23.1 > gp 13.8 > v2 13.1.
- CVaR-95:  graspmor 40.7 > gtmwkr 24.9 > gp 15.3 > v2 14.6.
Los generadores aprendidos (v2, gp) siguen dominando; el GP vuelve a ganar en
las clases grandes 50×N.

**El hallazgo diferenciado (hipótesis CONFIRMADA):** las semillas de intervalo
(peor-caso-óptimas) se alinean MEJOR con el objetivo riesgo-averso que con el
riesgo-neutral. Correlación de rankings intervalo→objetivo (v2, global):
- intervalo → esperado (riesgo-neutral): **0.980**
- intervalo → CVaR-95 (riesgo-averso):   **0.986**
El efecto es pequeño en magnitud pero EXTREMADAMENTE consistente:
**139/140 instancias** (v2+gp) tienen mayor correlación con CVaR que con el
esperado (fig_stochastic_risk.png, todos los puntos sobre la diagonal).

**Interpretación**: minimizar el peor caso (intervalo) está más cerca de
minimizar la cola de riesgo (CVaR) que de minimizar la media — justo lo que
predice la teoría. Las semillas de intervalo son buenas para scheduling
estocástico en general (ambas correlaciones >0.98), con una ventaja
sistemática para objetivos riesgo-aversos. Es la primera transferencia con
una diferencia REAL (no una interpolación sin tensión como crisp/fuzzy), y
conecta con la literatura de robust/stochastic scheduling.

## Espectro de riesgo completo (run_spectrum.py, 2026-07-13)

Añadida la cola OPTIMISTA (media del mejor 5%) para completar el gradiente.
Correlación intervalo(upper)→objetivo (Spearman global), por generador:

| generador | optimista | esperado | CVaR-95 |
|---|---|---|---|
| graspmor | 0.985 | 0.990 | 0.993 |
| gtmwkr | 0.951 | 0.965 | 0.974 |
| gp | 0.972 | 0.981 | 0.986 |
| v2 | 0.972 | 0.980 | 0.986 |

**Predicción CONFIRMADA en los 4 generadores**: la correlación crece
monótonamente de optimista → esperado → CVaR. No es una diferencia de dos
puntos: es un gradiente limpio y consistente. El alineamiento de las semillas
de intervalo con un objetivo escala con cuánto de riesgo-averso sea
(fig_risk_spectrum.png). RE del mejor por objetivo (v2): optimista 11.6% <
esperado 13.1% < CVaR 14.6%.

**El "bonus" (bordes del intervalo ↔ colas) NO se sostuvo** — honestamente:
predije que rankear por el LOWER del intervalo se alinearía mejor con la cola
optimista que rankear por el upper. Salió al revés: upper→optimista=0.972 vs
lower→optimista=0.968. El upper es simplemente mejor rankeador de la calidad
en TODOS los objetivos (domina la estructura del makespan); el lower es más
ruidoso. La simetría elegante era demasiado bonita para ser cierta.

## Decisiones de modelado y límites
- Distribución: uniforme en [lo,up] (opción por defecto sin compromisos).
  `sample_durations` en decode_vec.py es el punto de cambio para otras
  (beta, triangular como densidad, etc.).
- K=300 escenarios (números comunes). Subir K afina la cola del CVaR.
- Referencia RE: LB crisp de Taillard (cota inferior válida para cualquier
  realización). El RE esperado (13.1%) sale ~0.5 pts por encima del RE
  intervalo (12.6%): pequeño "precio" de no optimizar la media directamente.
- Pendiente si se quiere ir más lejos: comparar contra un generador
  estocástico-nativo (política/GP entrenados con recompensa = makespan
  esperado o CVaR), análogo a P2 del experimento crisp.
