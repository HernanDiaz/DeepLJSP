# Auditoría de números del paper GP tras el fix del makespan (2026-07-24)

Contexto: el 2026-07-18 se corrigió la agregación final del makespan de
intervalo (lex-por-upper → componente a componente, commits `3989757` y
`5e226f8`). El **upper es invariante** (ningún ranking por upper cambia); el
**lower/midpoint** sube ligeramente en ~11% de soluciones. La métrica RE del
paper usa el midpoint → todos los RE publicados se calcularon con la
convención vieja y cambian.

**Nota clave**: la §3 del paper ya define C_max **componente a componente** —
el código viejo se desviaba de la definición del propio paper en la agregación
final. El fix alinea implementación con paper; los números corregidos son los
que corresponden a la definición publicada.

Procedencia validada: los rollouts re-ejecutados reproducen EXACTAMENTE los
números publicados bajo la convención vieja (18.52, 17.67/18.68, 45.43,
29.41, tabla gp70 celda a celda) → la cadena número→script está verificada.

## Números basados en rollout determinista (delta despreciable)

| Número del paper | Publicado | Corregido | Δ | Texto nuevo |
|---|---|---|---|---|
| Mejor regla single-shot (abstract, tab gp70) | 18.5 | 18.59 | +0.07 | **18.6** |
| GP seed 2 / seed 3 global | 19.5 / 19.5 | 19.50 / 19.54 | +0.04 | 19.5 (igual) |
| Tuned best-of-3 | 17.67 | 17.71 | +0.04 | **17.7** (igual a 1 dec) |
| Tuned media / default media | 18.68 / 19.17 | 18.73 / 19.21 | +0.05 | gap idéntico (0.5) |
| MOR | 45.4 | 45.46 | +0.03 | **45.5** |
| GT-MWKR | 29.4 | 29.48 | +0.07 | **29.5** |
| Mejora vs mejor baseline ("10.9 points") | 10.9 | 29.48−18.59=10.89 | — | 10.9 (igual) |
| Tabla gp70 por clase | — | ±0.0–0.2 por celda | — | regenerar tabla |

## Fitness de entrenamiento (fig. convergencia, texto §resultados)

| Seed | Publicado | Corregido | Δ |
|---|---|---|---|
| 1 | 15.60 | 15.61 | +0.01 |
| 2 | 15.62 | 15.62 | 0.00 |
| 3 | 15.87 | 16.17 | **+0.31** |

⚠️ El texto dice "a spread of 0.27 points": con la corrección el spread pasa a
**0.56** → actualizar la frase (sigue siendo estabilidad razonable, pero el
número cambia). La evolución en sí usó la convención vieja como fitness
interno (ver "Decisión pendiente" abajo).

## Best-of-N (fig_bestofN, tab:matched) — AQUÍ ESTÁ EL PUNTO DELICADO

Dos efectos superpuestos:

1. **Efecto del fix** (misma muestra, convención vieja→nueva): +0.04 a +0.18
   pts, creciente con N (la selección amplifica el sesgo optimista del lower
   viejo). Forma de las curvas y orden GP>v2 intactos.
2. **Efecto de la realización** (corrida publicada `fair_gp_eps` de
   2026-07-07, **script no conservado / no reproducible**, vs pools de
   `seeds/`): ~0.4–0.5 pts, mayor que el efecto del fix.

| Número | Publicado (corrida vieja) | Desde pools corregidos |
|---|---|---|
| GP best-of-1024 | 14.1 | **13.69** |
| DRL best-of-1024 | 12.7 | **13.08** |
| Brecha GP−DRL a 1024 | **1.4 pts** | **0.6 pts** |
| GP mejora N=1→1024 ("−4.4 points") | 4.4 | 4.9 (18.59−13.69) |

⚠️ El claim "the learned sampling distribution retains an advantage" se
mantiene en dirección pero su magnitud baja de 1.4 a 0.6 pts medida sobre los
pools. Además los pools dan una comparación MÁS limpia (mismas 1024 muestras
por generador, mismo evaluador, reproducible desde el repo).

## Números de pools (comparativa de generadores; también RL §7)

| Métrica global | Viejo | Nuevo | Δ |
|---|---|---|---|
| GP best / media del pool | 13.25 / 21.35 | 13.43 / 21.40 | +0.19 / +0.05 |
| v2 best / media del pool | 12.58 / 21.25 | 12.79 / 21.30 | +0.21 / +0.05 |

Dominancia por instancia sin cambios (v2 37 / GP 34).

## Pendiente de auditar

- DRL greedy (19.4): requiere rollout del checkpoint; delta esperado +0.0x
  como el resto de rollouts deterministas.

## Decisión pendiente (recomendación)

1. **Best-of-N**: regenerar figura y tab:matched desde los pools corregidos
   (reproducible; N=1 = rollout determinista corregido) y reescribir la
   magnitud del claim vs DRL (0.6 pts, no 1.4). Alternativa: relanzar un
   experimento best-of-N dedicado.
2. **Re-evolución (opcional, limpieza total)**: la evolución usó la convención
   vieja como fitness. Re-evolucionar 3+3 seeds con el fitness corregido
   (~49 min/seed, paralelizable) elimina todo rastro de la convención vieja;
   a cambio, las reglas (y todos los números aguas abajo) cambiarían de nuevo.
   Dado que el spread entre seeds (~2 pts) domina sobre el efecto del fix
   (~0.05), mantener las reglas actuales y reevaluarlas con el evaluador
   corregido es defendible; re-evolucionar es lo más limpio si hay tiempo.

Datos: `benchmarks/audit_gp_numbers.csv` (por método×instancia, ambas
convenciones), `scripts/audit_paper_gp_numbers.py`,
`scripts/audit_bestofn_pools.py`, backups de CSVs viejos en el scratchpad de
la sesión.
