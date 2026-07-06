# Piloto de hibridación TS + v2 — instrucciones de uso de los pools

Documento de traspaso para ejecutar el piloto de siembra de la población
inicial del TS con soluciones del agente RL (v2). Generado el 2026-07-04.

**ACTUALIZACIÓN 2026-07-06**: el set COMPLETO está generado en `seeds/`
(145 archivos): las 70 Taillard (TA1-TA70) + ft10_interval, cada una con
pool v2 (1024 soluciones) y pool graspmor (MOR+ε, 1024), más los 3 pools
graspmix del piloto. Mismo formato en todos. Para el experimento completo,
recuerda la política de exclusión (AGENTS_V2_DESIGN.md): TA11-14
(entrenamiento RL), TA15-20 (desarrollo RL) y las 17 del irace del TS.

---

## 1. Inventario de pools (directorio `seeds/`, fuera de git)

3 instancias piloto × 3 generadores = 9 archivos, 1024 soluciones cada uno:

| Archivo | Generador | Best E[Cmax] (RE) | Media (RE) |
|---|---|---|---|
| `int__tai15_15_05_v2_pool.csv` | política v2 | 1323 (8.1%) | 1426 (16.5%) |
| `int__tai15_15_05_graspmor_pool.csv` | MOR + ε=0.1 | 1632 (33.4%) | 1847 (50.9%) |
| `int__tai15_15_05_graspmix_pool.csv` | regla aleatoria + ε | 1630 (33.2%) | 3931 (221%) |
| `int__tai20_20_02_v2_pool.csv` | política v2 | 1768 (13.2%) | 1918 (22.9%) |
| `int__tai20_20_02_graspmor_pool.csv` | MOR + ε | 2245 (43.8%) | 2447 (56.8%) |
| `int__tai20_20_02_graspmix_pool.csv` | mixto + ε | 2244 (43.8%) | 6010 (285%) |
| `int__tai30_20_04_v2_pool.csv` | política v2 | 2308 (18.5%) | 2464 (26.5%) |
| `int__tai30_20_04_graspmor_pool.csv` | MOR + ε | 2915 (49.6%) | 3145 (61.5%) |
| `int__tai30_20_04_graspmix_pool.csv` | mixto + ε | 2972 (52.6%) | 8551 (339%) |

Instancias (limpias para ambos métodos — ni entrenamiento/desarrollo del RL
ni tuning irace del TS): **TA5** = tai15_15_05 (LB 1224), **TA22** =
tai20_20_02 (LB 1561), **TA44** = tai30_20_04 (LB 1948).

## 2. Formato de cada línea

```
j1 j2 j3 ... jN;[lower, upper]
```

- `j1..jN`: permutación con repetición de trabajos, **1-based** — la k-ésima
  aparición del trabajo j = k-ésima operación del trabajo j, en orden de
  despacho.
- Tras `;`: intervalo de makespan del schedule **semiactivo** de esa
  permutación, con aritmética de intervalos: inicio de cada operación =
  máximo componente a componente entre el fin de la operación anterior del
  trabajo y el fin de la anterior en la máquina (`[max lowers, max uppers]`);
  fin = inicio + duración. Makespan = máx lexicográfico (por upper) de las
  finalizaciones de trabajo.

## 3. PASO PREVIO OBLIGATORIO — test de consistencia del decodificador

Antes de ningún experimento: carga las 1024 líneas de un pool, decodifícalas
con tu constructor semiactivo y comprueba que reproduces **exactamente** el
`[lower, upper]` de cada línea. Si alguna no cuadra, hay discrepancia
semántica entre evaluadores y los resultados no serían comparables — repórtala
antes de seguir (instancia, línea, valor esperado y obtenido).

## 4. Diseño experimental del piloto

**5 brazos** (población de 250 individuos, fracción sembrada p):

| Brazo | Composición de los 250 |
|---|---|
| A0 control | 250 con tu inicialización aleatoria estándar |
| A1 v2@10% | 25 del pool v2 + 225 aleatorios |
| A2 v2@50% | 125 del pool v2 + 125 aleatorios |
| A3 v2@100% | 250 del pool v2 |
| A4 MOR@50% | 125 del pool graspmor + 125 aleatorios |

(Opcional A5: graspmix@50% como baseline débil, si quieres la escala completa.)

**Runs**: 10 por brazo y por instancia (5 brazos × 3 instancias × 10 = 150
runs). **Presupuesto**: tu estándar de 15 min/run si el cluster lo permite
(≈37 h); con 5 min/run (≈12 h) el piloto sigue siendo informativo porque la
señal esperada está al principio de la curva.

**Emparejamiento para la estadística**: usa la MISMA semilla RNG del TS para
el run r en todos los brazos (semillas 1..10). Así la comparación entre brazos
es pareada por run (Wilcoxon pareado, como en tus papers).

## 5. Asignación de individuos del pool a cada run

Para el run r (r = 0..9) del brazo con k individuos sembrados:

- Toma las líneas del pool `[(r·k) mod 1024, (r·k + k) mod 1024)` — bloques
  consecutivos con envoltura circular.
- Con k=25 (10%): 10 runs × 25 = 250 líneas, todo disjunto.
- Con k=125 (50%): 1250 > 1024 → los 2 últimos runs reutilizan ~200 líneas
  de los primeros. Aceptable y documentado (coste de generación).
- Con k=250 (100%): reutilización mayor (30 runs compartirían pool; con 10
  runs son 2500 líneas → ~2.4 vueltas). Documentado.
- Rellena los 250−k restantes con tu init aleatoria (con la semilla RNG del run).

**No reordenes ni filtres el pool**: las líneas son muestras i.i.d. de cada
generador; coger solo las mejores fabricaría poblaciones de clones.

## 6. Qué registrar (para que pueda analizarlo yo directamente)

Un CSV único (o uno por instancia) con una fila por **evento de mejora** del
mejor individuo del run, más una fila final al agotar presupuesto:

```
instance,arm,run,t_seconds,best_lower,best_upper
tai20_20_02,A2,3,0.00,1834,1998      <- estado inicial (mejor de la población)
tai20_20_02,A2,3,12.41,1801,1962
...
tai20_20_02,A2,3,900.00,1610,1751    <- fila final (presupuesto agotado)
```

Con `t_seconds` desde el arranque del run y el makespan como intervalo (yo
calculo E[C_max] y RE). Con eso construyo: curvas anytime por brazo,
time-to-target (tiempo hasta alcanzar el RE final del control), Best/Avg RE a
presupuestos {10 s, 1 min, fin}, y los Wilcoxon pareados.

## 7. Hipótesis pre-registradas del piloto

- **H1 (principal)**: los brazos v2 alcanzan el RE final del control en una
  fracción del tiempo (time-to-target ≪ presupuesto).
- **H2**: v2@p supera a MOR@p a igual fracción p (el beneficio es del
  generador, no de "cualquier semilla").
- **H3 (trade-off)**: existe un p intermedio óptimo; con p=100% la pérdida de
  diversidad puede penalizar el resultado final aunque acelere el arranque.
- Neutral: si al presupuesto completo todos los brazos convergen a lo mismo,
  el claim del paper es "anytime superior", no "mejor calidad final".

## 8. Reproducibilidad de los pools

Cada pool se regenera bit a bit desde este repo (rama `research`):

```
python scripts/export_v2_seeds.py --instance <id> --n 1024 --generator v2 \
    --checkpoints models/v2_final_deepsets_1000ep_seed2.pt,models/v2_final_deepsets_1000ep_seed3.pt,models/v2_final_deepsets_1000ep_seed4.pt \
    --seed 1 --out seeds
python scripts/export_v2_seeds.py --instance <id> --n 1024 --generator grasp \
    --rules mor --epsilon 0.1 --seed 1 --out seeds        # renombrar a _graspmor
```

Checkpoints del modelo final versionados en `models/` (entrenados SOLO en
TA11-14; ver política de exclusión en AGENTS_V2_DESIGN.md).
