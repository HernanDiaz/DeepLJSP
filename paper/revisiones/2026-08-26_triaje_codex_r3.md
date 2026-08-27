# Triaje de la revisión Codex, ronda 3 (2026-08-26)

Informe crudo: `2026-08-26_revision_codex_eaai_r3_raw.md`. Recomendación:
**major revision** (r1 fue reject, r2 major revision). Revisión a ciegas
sobre el manuscrito en elsarticle, con el depósito de la curva con
extremos y el reanálisis de irace ya dentro del espacio de trabajo.

Lo que las dos rondas anteriores forzaron sale ahora validado sin
reservas: aritmética intervalar, criterio lexicográfico, recompensa,
arquitectura Deep Sets con sus 120.322 parámetros, unidad estadística,
protocolo best-of-N de los evaluadores autónomos y la mayoría de las
cifras impresas. Dice explícitamente que no ve motivo de rechazo por
los resultados centrales. **La curva de presupuesto ya no aparece como
hallazgo**: la reejecución con extremos y selección (U, L) se da por
buena sin que se le sugiriera.

## Hallazgos, con mi verificación

### R3-1 (REAL, medido, impacto ínfimo): `evaluate_policy` no aplica el desempate

`AgentV2.evaluate_policy` (`agent.py:216-230`) retiene por
`makespan < best_makespan` con `_episode_makespan` = upper solo; en
empate exacto del upper gana el primero visto, no el de menor lower.
No es un detalle interno: `scripts/eval_classic12_bo1024*.py` lo llaman,
y de ahí salen filas de la tabla de instancias clásicas.

Medido sobre el depósito de la curva (239.400 rollouts con ambos
extremos), a B=64 y 28.000 sorteos: **la elección difiere en el 1,47 %
de los sorteos** y el RE reportado se mueve **+0,009 puntos de media**,
como mucho +0,13 en una unidad (instancia, tirada). Es decir: la
inconsistencia con la Eq. (3) es real, y su efecto es indistinguible
de cero a la precisión que el paper imprime.

Las tablas principales de las 70 Taillard NO usan esta vía: salen de
`eval_val_brazos.py` y `eval_treinta_semillas.py`, que sí ordenan por
(upper, lower).

Acción: corregir la clave en `evaluate_policy` (una línea), declarar la
medición, y no reejecutar nada.

### R3-2 (REAL en el código, NO toca los resultados publicados)

Es el M4/R2-4 de rondas anteriores: `_episode_makespan` toma el `max`
lexicográfico de Python, así que con λ>0 el lower puede ser el de otro
trabajo y el f_λ rastreado queda inflado. Codex sostiene que declararlo
no repara el experimento y pide reejecutar los brazos robustos.

Comprobación decisiva: **los dos evaluadores de los brazos robustos
cargan el checkpoint del BLOQUE FINAL** (`INT__TAI20_15_04...pt`, en
`eval_lambda_ext_rollouts.py:39` y `eval_lambda_sweep_rollouts.py:45`),
no `best_model.pt`. La clave defectuosa gobierna `best_agent` y, con
él, `best_model.pt`, que esas evaluaciones no abren: solo comprueban
que exista, como señal de tirada completa. Por tanto ningún número de
7.4 depende de la clave errónea.

Lo que sí queda afectado es la cadena de transferencia entre bloques
durante el entrenamiento, que podría haber sido otra con la clave
correcta. Pero eso es una propiedad del procedimiento, ya declarada en
5.4, idéntica en todos los brazos, no un error de medición. Y la
conclusión de la frontera está corroborada por una vía que no depende
del entrenamiento en absoluto: rerankear el depósito del brazo por
defecto con cada f_λ la reproduce casi punto por punto.

Acción: corregir el código (usar `final_makespan`) y precisar en 7.4
que las evaluaciones cargan el checkpoint del bloque final, con lo que
el defecto no las alcanza. Reejecutar no está justificado.

### R3-3 (MAYORMENTE artefacto del espacio de revisión, con un núcleo real)

Dice que el verificador reporta un fallo y seis pendientes. En el repo
da **834 comprobaciones, 0 fallos, 0 pendientes**. La diferencia es que
`review_ws` no lleva `paper/main.log`, `paper/main.aux` ni los 21
registros `idea-*` (el repo los tiene). Mismo tipo de falso positivo
que el r2-7.

Núcleo real y verificado: **el verificador termina con código de salida
0 aunque haya fallos**. Eso sí conviene arreglarlo, porque anula su
valor como comprobación automatizable. También es cierto que
`fig_budget` no lo genera `paper/make_figures.py` sino un script de
`scripts/`, y que algunas figuras llevan valores incrustados
(`make_figures.py:42-44,87-88,153`).

### R3-4 (REAL en el repo, ya resuelto en el depósito)

Sin README en la raíz del repo, y `DEEPLJSP_AGENT` sin definir
selecciona **AgentV1 en silencio**: una invocación ingenua entrena el
agente equivocado. El depósito Zenodo v3 ya documenta la variable, los
comandos por brazo y las versiones fijadas; el repo de trabajo no.

### R3-5 (posición ya declarada, no defecto)

Pide control de multiplicidad. 5.1 declara explícitamente que no se
aplica corrección y que cada contraste se interpreta individualmente.
Es una postura defendible y transparente. Se puede reforzar reportando
tamaños de efecto junto a los p, que el paper ya hace en las
comparaciones principales.

### Menores que merecen entrar

- 3: el `max` lexicográfico de la visualización (`job_shop_env.py:493`)
  debería usar la rutina componente a componente. No afecta a números.
- 4: explicar el extremo B=341 con 342 rollouts guardados (el índice 0
  es la pasada greedy).
- 8: "what the policy attends to" es permutation importance, no
  atención; el término induce a error habiendo un variante de atención
  en el suplementario.
- 5: el punto medio como "expected makespan"; ya matizado en §3, se
  puede revisar la coherencia del término en el resto del texto.

## Lectura global

Tres rondas seguidas y la trayectoria es clara: reject, major revision,
major revision sin motivo de rechazo en los resultados. Lo que queda no
son errores de medición sino de higiene de código y de paquete: una
clave de desempate que no se aplica en una vía secundaria (efecto
medido: 0,009 puntos), un rastreador defectuoso que no alcanza a los
números publicados, un verificador que no señala fallo al sistema
operativo y un repo sin README. Ninguno exige reejecutar experimentos.
