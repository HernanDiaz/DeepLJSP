# Campana con la configuracion ganadora de irace

Config: tournament 7, crossover 0.7695, maxtree 30, elitism 2.
Todas las cifras sobre las 70 instancias Taillard de intervalo.

## Resultados principales (objetivo makespan)

| brazo | n | RE (%) | ancho (%) | nodos |
|---|---|---|---|---|
| full (tuned) | 30 | 18.99 ± 1.33 | 12.41 ± 0.30 | 26.4 |
| no-width (tuned) | 30 | 18.66 ± 1.08 | 12.62 ± 0.23 | 27.2 |

Wilcoxon pareado no-width vs full: RE z=-0.83, ancho z=3.40 (n=30)

Mejor regla: gp_tuned_seed1 -> RE 17.71%, ancho 12.28%, 26 nodos

## Objetivo robusto (upper + lambda*ancho, lambda=1)

| brazo | n | RE (%) | ancho (%) |
|---|---|---|---|
| robust+width | 30 | 19.62 ± 1.52 | 12.04 ± 0.75 |
| robust+nowidth | 30 | 18.42 ± 0.87 | 12.47 ± 0.20 |

Wilcoxon pareado sobre el ancho (nowidth - width): z=3.22 (n=30)

## Frontera calidad-predictibilidad

| lambda | n | RE (%) | ancho (%) |
|---|---|---|---|
| 0.5 | 10 | 19.20 ± 1.52 | 12.18 ± 0.50 |
| 1.0 | 30 | 19.62 ± 1.52 | 12.04 ± 0.75 |
| 2.0 | 10 | 19.86 ± 1.74 | 11.80 ± 0.81 |
| 4.0 | 10 | 23.27 ± 3.80 | 10.54 ± 1.26 |
