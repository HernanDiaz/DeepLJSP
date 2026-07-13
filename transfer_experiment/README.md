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

## Pendiente — MITAD A (fuzzy) y MITAD B (método vivo)
- **Fuzzy**: falta generar las instancias TFN (decisión de modelado del
  spread; `decode_tfn` ya implementado en decode.py) y re-decodificar los
  pools bajo aritmética TFN. Comparar RE fuzzy y correlación de rankings.
- **Mitad B (método como regla viva)**: aplicar la regla GP directamente
  sobre instancias crisp/fuzzy (los terminales de anchura → 0 en crisp) y
  medir vs re-evolucionar nativo; aplicar el v2 en crisp (features OOD) para
  cuantificar su degradación. Requiere cablear un entorno crisp/fuzzy para
  el cómputo de features.
