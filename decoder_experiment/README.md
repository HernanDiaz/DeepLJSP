# Experimento: decodificador ACTIVO por inserción vs semiactivo

Aislado (no toca nada más). Pregunta: ¿mejora el RE al re-decodificar las
secuencias de los pools con un SGS activo por inserción en vez del semiactivo?

`active_decode.py` — decodificador activo por inserción (crisp).
`run_active_decoder.py` — compara crisp activo vs crisp semiactivo por
generador y clase → `benchmarks/active_decoder.csv`.

## Resultado (2026-07-13)

RE del mejor individuo (global), semiactivo → activo:
- graspmor: 38.2% → 22.9% (**+15.2**)
- gtmwkr:  22.5% → 20.8% (+1.7)
- gp:      13.0% → 12.7% (+0.25)
- v2:      12.4% → 12.2% (+0.19)

**Hallazgo**: el decodificador activo es un IGUALADOR — mejora muchísimo a los
generadores malos y apenas nada a los buenos. La razón es cuántos huecos deja
cada uno: v2 y GP ya producen schedules **casi sin huecos** (near-active), así
que la inserción no tiene qué aprovechar; graspmor deja schedules llenos de
huecos desperdiciados. Que la mejora del v2/GP sea diminuta es una PRUEBA de
que ya generan schedules compactos.

**Spearman semiactivo↔activo**: graspmor 0.083 (el activo reordena por
completo las soluciones — la mejor semiactiva ≠ la mejor activa), v2/gp ~0.96
(ranking preservado, otra señal de compacidad). gtmwkr 0.705 (intermedio).

**Por tamaño**: el activo ayuda algo más en instancias grandes (v2 50×15
+0.66, 50×20 +0.35; 15×15 +0.02) — más máquinas = más huecos. Aun así, poco.

## Conclusión y límite
- Directamente sobre las semillas buenas (v2, GP): mejora despreciable, porque
  ya son near-active. Resultado informativo (elogio a los generadores), no una
  mejora aprovechable.
- Caveat: mide "mejora gratis" sobre secuencias optimizadas para semiactivo.
  REENTRENAR los generadores CON el decodificador activo en el bucle es otra
  pregunta (no probada); el techo de la mejora "gratis" es bajo.
- Extensión: versión INTERVALO del decodificador activo (gap-fitting con
  intervalos, elegir convención por upper) — aquí se hizo crisp por limpieza.
