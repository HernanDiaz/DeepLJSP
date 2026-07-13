# Piloto de hibridación TS + v2 — instrucciones de uso de los pools

Documento de traspaso para ejecutar el piloto de siembra de la población
inicial del TS con soluciones del agente RL (v2). Generado el 2026-07-04.

**ACTUALIZACIÓN 2026-07-13**: el set para el EXPERIMENTO COMPLETO cubre
las 70 Taillard (TA1-TA70) + ft10_interval con CUATRO generadores por
instancia (escalera de calidad completa). Estado por generador:

| Generador | Qué es | Pools | Estado |
|---|---|---|---|
| `v2` | política RL (3 checkpoints default) | 71/71 | ✅ completo |
| `graspmor` | MOR + ε=0.1 | 71/71 | ✅ completo |
| `gtmwkr` | Giffler-Thompson + ε en el conflict set | 71/71 | ⏳ generándose 2026-07-13 (workers desacoplados; ver seeds_gen_*.log) |
| `gp` | regla GP evolucionada y tuneada + ε | 71/71 | ⏳ generándose 2026-07-13 (ídem) |
| `graspmix` | mixto débil | solo 3 piloto | ❌ DESCARTADO (decisión 2026-07-13: no hace falta) |

Todos con 1024 soluciones por pool y el mismo formato. Para el experimento
completo, recuerda la política de exclusión (AGENTS_V2_DESIGN.md): TA11-14
(entrenamiento RL+GP), TA15-20 (desarrollo RL+GP, incluye el tuning de
ambos) y las 17 del irace del TS.

---

## 1. Inventario del piloto (directorio `seeds/`, fuera de git)

Calidad de los pools en las 3 instancias piloto (E[Cmax] mejor/media, RE):

| Archivo | Generador | Best E[Cmax] (RE) | Media (RE) |
|---|---|---|---|
| `int__tai15_15_05_v2_pool.csv` | política v2 | 1323 (8.1%) | 1426 (16.5%) |
| `int__tai15_15_05_graspmor_pool.csv` | MOR + ε=0.1 | 1632 (33.4%) | 1847 (50.9%) |
| `int__tai20_20_02_v2_pool.csv` | política v2 | 1768 (13.2%) | 1918 (22.9%) |
| `int__tai20_20_02_graspmor_pool.csv` | MOR + ε | 2245 (43.8%) | 2447 (56.8%) |
| `int__tai30_20_04_v2_pool.csv` | política v2 | 2308 (18.5%) | 2464 (26.5%) |
| `int__tai30_20_04_graspmor_pool.csv` | MOR + ε | 2915 (49.6%) | 3145 (61.5%) |

(los pools gtmwkr y gp del piloto están medidos por upper mejor/mediana en
los bloques A6/A7 de la sección 4; los graspmix del piloto siguen en disco
pero el brazo está descartado)

Instancias piloto (limpias para ambos métodos — ni entrenamiento/desarrollo
del RL/GP ni tuning irace del TS): **TA5** = tai15_15_05 (LB 1224),
**TA22** = tai20_20_02 (LB 1561), **TA44** = tai30_20_04 (LB 1948).

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

(A5 graspmix: DESCARTADO 2026-07-13 — no aporta sobre la escalera
MOR-ε < GT-ε < GP-ε.)

**A6 recomendado — baseline heurístico FUERTE (añadido 2026-07-06)**: pools
`*_gtmwkr_pool.csv` con G&T aleatorizado (ruido ε=0.1 DENTRO del conflict
set → cada individuo es un schedule activo). Calidad muy superior a MOR+ε
(upper, mejor/mediana): TA5 1554/1705 vs 1632/1847; TA22 2068/2221 vs
2245/2447; TA44 2672/2814 vs 2915/3145. Si el TS sembrado con v2 supera
también a GT-ε@p, el resultado es inatacable. Mismo formato y misma
asignación por bloques.

**A7 — el baseline heurístico MÁS fuerte (añadido 2026-07-13)**: pools
`*_gp_pool.csv` con la regla GP evolucionada y TUNEADA (paper_gp, config
irace #15) + ruido ε=0.1 estilo GRASP. Bate a GT-ε en las 3 instancias
(upper, mejor/mediana): TA5 **1400/1539** vs 1554/1705; TA22
**1903/2032** vs 2068/2221; TA44 **2429/2600** vs 2672/2814. Es el
generador heurístico más fuerte disponible: si v2@p supera también a
GP-ε@p, el claim de que el valor viene de la política aprendida (y no de
"cualquier buen constructivo") queda blindado. Mismo formato y asignación.
Regeneración:
```
python scripts/export_v2_seeds.py --instance <id> --n 1024 --generator grasp \
    --rules gp --epsilon 0.1 --suffix gp --seed 1 --out seeds
```
(la regla se carga de benchmarks/gp_tuned_seed3.json vía --gp-json)

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
# v2 (política RL)
python scripts/export_v2_seeds.py --instance <id> --n 1024 --generator v2 \
    --checkpoints models/v2_final_deepsets_1000ep_seed2.pt,models/v2_final_deepsets_1000ep_seed3.pt,models/v2_final_deepsets_1000ep_seed4.pt \
    --seed 1 --out seeds
# graspmor (MOR + eps)
python scripts/export_v2_seeds.py --instance <id> --n 1024 --generator grasp \
    --rules mor --epsilon 0.1 --suffix graspmor --seed 1 --out seeds
# gtmwkr (G&T + eps interno)
python scripts/export_v2_seeds.py --instance <id> --n 1024 --generator grasp \
    --rules gtmwkr --epsilon 0.1 --suffix gtmwkr --seed 1 --out seeds
# gp (regla GP tuneada + eps; regla en benchmarks/gp_tuned_seed3.json)
python scripts/export_v2_seeds.py --instance <id> --n 1024 --generator grasp \
    --rules gp --epsilon 0.1 --suffix gp --seed 1 --out seeds

# regeneración masiva de lo que falte (reanudable, salta existentes):
python scripts/gen_missing_pools.py --classes 15_15,20_15,20_20,30_15,30_20,50_15,50_20 \
    --generators gp,gtmwkr --ft10
```

Checkpoints del modelo final versionados en `models/` (entrenados SOLO en
TA11-14; ver política de exclusión en AGENTS_V2_DESIGN.md).
