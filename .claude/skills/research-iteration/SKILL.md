---
name: research-iteration
description: Ejecuta UNA iteración del bucle de investigación - lee RESEARCH_IDEAS.md, propone una idea nueva, la implementa, la evalúa con el benchmark (quick como filtro, full como confirmación), hace commit si mejora o rollback si no, y registra el resultado. Usar cuando el usuario pida iterar la investigación, probar una idea nueva del backlog, o ejecutar el bucle de mejora.
---

# Iteración del bucle de investigación

Ejecuta exactamente UNA iteración del protocolo definido en `RESEARCH_IDEAS.md`
(léelo primero — sus reglas mandan sobre este resumen si difieren).

## Precondiciones

1. Rama `research` activa y árbol de trabajo limpio (`git status`). Si hay
   cambios sin commitear, detente e informa al usuario.
2. Lee `RESEARCH_IDEAS.md` completo: protocolo, referencia actual, historial
   y backlog.

## Pasos

1. **Proponer idea**: elige del backlog o propón una nueva que NO esté en el
   historial. Criterios: diff pequeño, hipótesis medible, no toca los scripts
   de benchmark ni (salvo marcarlo `[CAMBIA-ENTORNO]`) la semántica del
   entorno. Asigna el siguiente ID (idea-01, idea-02, ...). Anuncia al usuario
   la idea elegida y la hipótesis antes de implementar.

2. **Implementar** la idea en el código con el diff mínimo necesario.
   Ejecuta `pytest tests/ -q` — los 8 fallos preexistentes son aceptables;
   cualquier fallo NUEVO debe arreglarse antes de seguir.

3. **Filtro quick** (~25 min):
   `venv\Scripts\python.exe scripts\run_benchmark.py --tier quick --seeds 2,3 --tag idea-NN-quick`
   y comparar con la referencia quick de RESEARCH_IDEAS.md usando
   `scripts\compare_benchmarks.py`. Si la diferencia media es > +3% (peor) →
   ir al paso 6 (descartar).

4. **Confirmación full** (~2.5-3 h):
   `venv\Scripts\python.exe scripts\run_benchmark.py --tier full --tag idea-NN-full`
   y comparar con la referencia full. Ejecutar en segundo plano y esperar.
   **Aceptar solo si**: diferencia media ≤ −3%, o mejor en ≥3 problemas con 0
   peores. Verificar además que las anclas deterministas son idénticas (si
   cambiaron y la idea no es `[CAMBIA-ENTORNO]`, es una regresión: descartar).

5. **Si se acepta**: actualizar el historial y la sección "Referencia actual"
   de RESEARCH_IDEAS.md (la referencia full pasa a ser el JSON de esta idea);
   commit de código + benchmarks/*.json + RESEARCH_IDEAS.md con mensaje
   `research: idea-NN <resumen> (aceptada, <dif>% en full)`.

6. **Si se descarta**: `git restore` de los archivos de código modificados
   (NO restaurar RESEARCH_IDEAS.md ni benchmarks/); registrar la idea en el
   historial con sus números y el motivo; commit solo de RESEARCH_IDEAS.md +
   los JSON del intento con mensaje `research: idea-NN <resumen> (descartada, <dif>%)`.

7. **Informar**: resumen final con la idea, los números de quick/full, la
   decisión y el estado del repositorio. Si el usuario pidió iterar en bucle,
   este es el punto de corte natural entre iteraciones.

## Reglas duras

- Nunca modificar `scripts/run_benchmark.py`, `scripts/compare_benchmarks.py`
  ni los tiers desde este bucle.
- Nunca aceptar por resultados del quick: el quick solo descarta.
- Toda idea probada queda en el historial, también las descartadas.
- Un solo cambio conceptual por iteración; si la implementación revela que se
  necesitan dos cambios independientes, registrar el segundo en el backlog.
