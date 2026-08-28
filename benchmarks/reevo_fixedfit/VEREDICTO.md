# Veredicto campaña 30×3 con fitness corregido

| Config | n | media±std RE global | mejor seed |
|---|---|---|---|
| default (full terminals) | 30 | 18.68 ± 0.84 | 17.30 |
| tuned (irace #15) | 30 | 18.99 ± 1.33 | 17.71 |
| ablación no-width | 30 | 18.39 ± 0.59 | 17.73 |

## Tests de Wilcoxon signed-rank pareados (mismos seeds)
- tuning: default vs tuned (n=30): W+=186.0, z=-0.96
- interval-awareness: default vs no-width (n=30): W+=294.0, z=1.26
  (|z|>1.96 -> significativo al 5%; el signo de z indica la dirección)

## Lectura de la ablación (LA NOVEDAD)
Δ = no-width − full = -0.29 pts de RE global.
Si no-width es PEOR (Δ>0) y significativo -> los terminales de
anchura (PTW/ESTW/WKRW) aportan: la interval-awareness paga.
Si Δ≈0 -> las cotas de peor caso portan casi toda la señal (hallazgo
honesto: primer estudio que lo cuantifica).

Referencia (3 seeds publicados, convención corregida): default
best 18.59 / media 19.21; tuned best 17.71 / media 18.73.
Detalles por seed en summary.csv.
