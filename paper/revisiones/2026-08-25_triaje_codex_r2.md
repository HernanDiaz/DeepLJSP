# Triaje de la revisión Codex, ronda 2 (2026-08-25)

Informe crudo: `2026-08-25_revision_codex_eaai_r2_raw.md`. Recomendación
del revisor: **major revision** (la ronda 1 fue reject). Revisión a
ciegas sobre el manuscrito post-Ruta A y el espejo del depósito v3.

Lo que la ronda 1 forzó a arreglar sale ahora verificado como correcto:
§5.4 (regla de transferencia y artefacto, `batch_experimenter.py`),
la aritmética intervalar y el criterio lexicográfico, la arquitectura
(120.322 parámetros exactos), los evaluadores autónomos, la convención
estadística de los scripts de ablación y cinco números trazados hasta
los CSV primarios.

## Hallazgos nuevos, todos verificados por mí en código y con medición

### R2-1 (MAYOR, confirmado): los pesos de la recompensa de §4.1 no son los entrenados

La ruta real de las campañas es `scripts/run_benchmark.py` →
`python -m jobshop_rl.main --mode batch`, y `run_batch_experiment`
(`jobshop_rl/main.py:251-260`) pasa un vector explícito que anula el
generador adaptativo (`factory.py:121-143`: con `reward_params` no
vacío el generador no se consulta). Reproducido instanciando
`AdaptiveRewardStrategy` con ese vector sobre TA11–TA14: los pesos
efectivos en los cuatro bloques son

    mk 1.0, id 0.15, cr 0.05, ba 0.10, pr 0.05, li 0.30

(el balance baja de 0.15 a 0.10 por la única regla por instancia que
llega a actuar, la de varianza de carga, disparada en las cuatro).
El §4.1 actual imprime pr 0.26, id 0.237–0.243, li 0.15, cr 0.1: es el
vector del generador `AdaptiveConfigGenerator`, una ruta que las
campañas nunca ejecutaron. El error es de la Ruta A: en la ronda 1 medí
el generador en aislamiento en lugar de seguir la ruta de entrada real,
y el check (3) del verificador valida esa misma ruta muerta.

Arreglo (texto + verificador, sin reentrenar): reescribir el párrafo de
pesos de §4.1 con el vector real y la regla del balance; sustituir el
check del verificador por uno que reproduzca la ruta
`main.py → factory → AdaptiveRewardStrategy` de punta a punta.

### R2-2 (MAYOR, confirmado): la curva de presupuesto no usa el decodificador desplegado

`scripts/eval_curva_diez.py:53-75` guarda solo el punto medio
componente a componente de cada rollout (descarta los extremos).
`scripts/analiza_curva_diez.py:81-97` construye los pools best-of-B
con las 341 muestras EXCLUYENDO el rollout greedy (índice 0) y
selecciona por punto medio mínimo, no por el criterio (U, L). El
protocolo desplegado de §5.4 es 1 greedy + (B−1) muestras con
selección lexicográfica. Los cruces de §7.2 (supera al greedy en B=3,
a la regla GP en B=8) y las ganancias por duplicación miden por tanto
otro decodificador. Los depósitos no permiten reanalizar porque los
extremos no se guardaron.

Opciones: (a) reejecutar la campaña de la curva guardando extremos y
rehacer el análisis con el protocolo desplegado (coste ≈ la campaña
original, días de CPU); (b) Ruta A textual: describir la curva como lo
que es, un barrido de pools muestreados seleccionados por punto medio,
y reformular los cruces como propiedad de ese barrido. La (b) debilita
§7.2 pero es honesta y inmediata.

### R2-3 (MAYOR, confirmado): la confirmación del ganador de irace viola las dos convenciones

`scripts/confirma_ganador_reward.py`: (i) el Wilcoxon corre sobre los
18 pares instancia×semilla (`:150-160`), no sobre las 6 medias por
instancia que la convención de §5.1 exige; (ii) el brazo afinado se
entrena con transferencia secuencial (`:79-91`, siempre del bloque
inmediatamente anterior), no con la regla del mejor bloque de §5.4.
El p=0.21 del suplementario no está calculado bajo el protocolo del
paper. Nota: los dos brazos de la confirmación comparten la
transferencia secuencial entre sí (el default carga
`models/v2_final_deepsets_1000ep_seed*`, entrenados por el clon con la
misma lógica), así que la comparación es internamente simétrica; lo que
no es es representativa del protocolo principal.

Arreglo mínimo: reanalizar con las 6 medias por instancia y Wilcoxon
exacto (los RE por instancia y semilla están en los logs de la
campaña) y decir en el suplementario que la confirmación usa
transferencia secuencial en ambos brazos. Arreglo completo: repetir la
confirmación con la regla del mejor bloque (3 semillas × 2 brazos ×
1000 episodios).

### R2-4 (moderado, confirmado): el extremo inferior de f_lambda puede ser erróneo en el rastreo de los brazos robustos

La recompensa robusta es correcta: `MakespanRewardComponent.calculate`
usa `final_makespan` componente a componente (`makespan.py:88-97`).
El defecto queda confinado a `AgentV2._episode_makespan`
(`agent.py:121-135`), que toma el `max` lexicográfico de Python: su
upper es correcto (lambda=0 intacto), pero con lambda>0 el lower puede
ser el de otro trabajo, y ese f_lambda alimenta el rastreo del mejor
episodio y la elección del mejor bloque en la transferencia. Los
artefactos desplegados se evalúan fuera con el makespan correcto.
Arreglo: usar `final_makespan` ahí, y auditar si en las 40 tiradas
robustas la clave errónea cambió alguna elección de bloque.

### R2-5 (moderado, confirmado): dos artefactos según el punto de entrada

`BatchExperimenter.evaluate_on_test_set` (`:299-308`) restaura
`best_model_state` (mejor episodio) para el `test_results.csv`
inmediato, mientras `best_model.pt` y los evaluadores autónomos usan la
red al final del bloque. Las tablas del paper usan lo segundo; el
paquete expone los dos significados sin avisar. Arreglo: nota en el
README del depósito (o eliminar la restauración implícita) y una frase
en §5.4.

### R2-6 (terminología, decisión de autor): "expected makespan" para el punto medio

Eq. (4) llama E[C] al punto medio del intervalo. Es la convención de la
literatura IJSP que el paper hereda (y cita), pero el revisor tiene
razón en que no es una esperanza sin un modelo probabilístico. Opciones:
renombrar a "midpoint makespan" en todo el texto, o una frase que
declare el punto medio como proxy convencional del campo con las citas.

### R2-7 (paquete, confirmado con matices): autocontención

- `paper/verify_numbers.py:2324` abre `paper/main.aux` sin guarda: en
  el paquete (sin auxiliares) CASCA con FileNotFoundError. Mismo guard
  que ya lleva `main.log`.
- El check "trece modificaciones rechazadas" lee `os.listdir` de
  `benchmarks/` buscando carpetas `idea-*`: 17 en el repo, 0 en el
  depósito (el preparador solo captura rutas citadas entre comillas).
  En el paquete el check falla. Añadir las carpetas `idea-*` (§7.4 las
  cita) o los marcadores mínimos.
- `benchmarks/fair_gp_eps.csv` (fuente primaria de las filas GP
  muestreadas) no tiene productor en el árbol: vino del arnés del
  estudio GP. Documentar su procedencia en el README o añadir un
  productor.
- `models/` lleva las semillas 2–4 pero no el campeón (semilla 5), que
  solo vive en `outputs/`. Exportarlo con nombre inequívoco.
- Parte de las quejas (sin README, sin requirements) son artefacto del
  espacio de revisión: el README y requirements.txt del depósito v3 no
  se copiaron a `review_ws`. No obstante, lo del `.aux`, `idea-*`,
  `fair_gp_eps` y la semilla 5 es real también en el depósito.

### Menores aceptables sin discusión

1. Progreso: el episodio suma (nm−1)/nm, no 1 (el componente devuelve
   0 en la transición terminal). Corregir la frase de §4.1.
2. Mejora local: 0 en la primera transición (previo None). Una frase.
3. Con gamma=1 y horizonte fijo el término de progreso es constante e
   independiente de la acción: matizar "señal de progreso".
4. Los generadores aleatorios se resiembran al inicio de cada bloque,
   no una vez por tirada. Una frase en §5.4.
5. Nombrar la construcción de los IC del 95% (t sobre diferencias por
   instancia).
6. Comentario obsoleto en `scripts/run_benchmark.py:45-48` (niega el
   cross-size que el paper demuestra).
7. Suplementario: "two configuration studies" pero se reportan tres
   campañas.
8. Abstract: "improves on every hand-crafted rule" → añadir "the
   validation-selected policy".
9. Nota pendiente de declaración de IA generativa en `main.tex`
   (decisión del autor, ya conocida).
10. Plantilla JIM → convertir a elsarticle cuando se elija revista (ya
    previsto).

## Lectura global

Ninguno de los hallazgos toca los números de cabecera (15.0 vs 15.9 a
bo64, 13.92±0.60 de validación, la frontera lambda, los tiempos): el
revisor los ha trazado y cuadran. Lo que toca es (1) la descripción del
método (pesos), que se arregla como la Ruta A; (2) una figura de
análisis (curva de presupuesto), que exige reejecutar o reencuadrar;
(3) un resultado del suplementario (p=0.21), que exige reanálisis; y
(4) higiene del paquete. El patrón del error R2-1 es el mismo que
destapó la ronda 1: verificar una ruta de código plausible en lugar de
la ruta que las campañas ejecutaron de verdad.
