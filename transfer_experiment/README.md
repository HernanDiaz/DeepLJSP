# Experimento de transferencia intervalo → crisp / fuzzy

Aislado del resto del proyecto. Pregunta: las soluciones generadas para el
IJSP (intervalo), que minimizan el peor caso, ¿transfieren a los modelos
CRISP (determinista) y FUZZY (triangular)?

## Estructura
- `decode.py` — decodificadores de secuencias a schedule semiactivo bajo
  aritmética crisp / intervalo / TFN (mismo esqueleto de despacho).
- `validate_decoder.py` — valida el decodificador contra los `[lo,up]`
  guardados en los pools (1192/1200 exactos; los 8 fallos son el problema de
  dependencia del *lower* en aritmética de intervalos — irrelevante para
  crisp, que usa aritmética escalar).
- `run_crisp_transfer.py` — MITAD A (crisp): re-decodifica los pools de
  intervalo bajo crisp y mide RE, precio de robustez y correlación de
  rankings. → `benchmarks/crisp_transfer.csv`.
- `plot_crisp_transfer.py` — figura intervalo-vs-crisp.

## Resultado crisp (2026-07-13) — transferencia SIN pérdidas

RE del mejor individuo (global, 70 Taillard): la **escalera se conserva
idéntica** bajo evaluación crisp — graspmor 38.2% > gtmwkr 22.5% >
gp 13.0% > v2 12.4% (los mismos números que en intervalo).

Tres hallazgos:
1. **Escalera preservada**: el orden de calidad intervalo se mantiene en crisp.
2. **Sin precio de robustez**: RE crisp ≈ RE intervalo (de hecho ~0.3 pts
   MENOR — la aritmética de intervalos sobreestima; optimizar el peor caso NO
   cuesta calidad puntual).
3. **Correlación de rankings ~0.99** (Spearman): la mejor solución en
   intervalo sigue siendo la mejor en crisp. Puedes elegir seeds por calidad
   intervalo y son los seeds correctos para crisp.

Conclusión: los generadores entrenados en intervalo (v2 y GP) sirven
directamente para inicializar algoritmos crisp — sin reentrenar, sin pérdida.

## Resultado FUZZY (2026-07-13) — transferencia SIN pérdida (Mitad A)

TFN por operación = (lo_intervalo, valor_crisp, up_intervalo): soporte = el
intervalo, modal = el valor crisp. `run_fuzzy_transfer.py` → RE del valor
esperado E[C]=(A+2B+C)/4 vs LB crisp. `benchmarks/fuzzy_transfer.csv`.

Resultado aún más limpio que crisp: escalera IDÉNTICA (v2 12.6%, gp 13.2%
mejor E[C], global — los mismos números que en intervalo), precio de
robustez ~−0.16 (menor que crisp, E[C] pondera el modal), y correlación de
rankings intervalo→fuzzy **~0.998** (más alta que crisp). El GP vuelve a
ganar en las clases grandes (50×N). Figura conjunta:
`benchmarks/figures/fig_transfer_summary.png`.

**Síntesis Mitad A**: las secuencias optimizadas para el peor caso en
intervalo transfieren a crisp Y a fuzzy esencialmente sin pérdida
(Spearman 0.995–0.998), sin penalización de robustez. Los generadores de
intervalo (v2, GP) inicializan los tres modelos de incertidumbre — un
resultado de generalización fuerte para los dos papers.

## EXPERIMENTOS PENDIENTES (apuntados 2026-07-13)

Ordenados de más barato a más caro. El resultado crisp actual (transferencia
de semillas sin pérdida) ya se sostiene solo; lo de abajo lo refuerza.

### P1 — Regla GP directa sobre crisp (GRATIS, sin entrenar) — Mitad B / GP
Aplicar la regla GP evolucionada en intervalo DIRECTAMENTE sobre instancias
crisp: los terminales de anchura (PTW, ESTW, WKRW) valen 0, la fórmula sigue
dando un ranking válido. Comparar su RE crisp (rollout determinista) con
reglas crisp nativas (MOR, MWKR). Si iguala o gana → el GP es un heurístico
PORTABLE entre modelos de incertidumbre sin reentrenar. Requiere cablear el
cómputo de features/terminales sobre una instancia crisp (aritmética escalar;
`decode_crisp` ya existe). ~1 tarde, 0 cómputo pesado.

### P2 — vs generadores CRISP-NATIVOS (barato, sobre subconjunto)
Comparar los seeds de intervalo transferidos contra seeds generados
nativamente en crisp, sobre un subconjunto representativo (dev set o unas
pocas por clase — NO las 71). Responde "¿tan buenos como los nativos?".
- GP nativo: re-evolucionar en crisp (fitness crisp), ~50 min/semilla.
- v2 nativo: reentrenar el PPO en Taillard crisp representadas como
  intervalos degenerados [d,d] (sin código de entorno nuevo; las features de
  incertidumbre quedan a 0), ~4h/3 semillas. Luego generar pools crisp y
  comparar best/mean RE + dominancia contra los transferidos.

### P3 — Mitad A FUZZY: HECHA (ver arriba). Pendiente Mitad B fuzzy
- Mitad A fuzzy COMPLETADA (transferencia de semillas sin pérdida).
- Pendiente Mitad B fuzzy: aplicar la regla GP directa sobre fuzzy
  (terminales derivados del TFN) como método vivo — junto con P1 (crisp).
- Nota de modelado: se usó el TFN natural (lo, crisp, up); si se quiere
  explorar otros spreads/asimetrías, `build_tfn` en run_fuzzy_transfer.py es
  el punto de cambio. El max fuzzy tiene el mismo problema de dependencia del
  lower (A) que el intervalo, pero E[C] pondera A solo 1/4 y el modal (B, la
  parte exacta) 1/2, así que el efecto en el ranking es despreciable
  (Spearman 0.998).
