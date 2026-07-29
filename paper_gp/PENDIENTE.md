# Pendiente del paper GP

## 1. eps-robustez sobre las 30 reglas (asimetria entre 7.2 y 7.3)

**Motivo.** La Tabla 7 (ablacion) sostiene su afirmacion sobre **30 reglas por
brazo** con Wilcoxon pareado sobre las semillas compartidas. La Tabla 8
(eps-robustez) la sostiene sobre **una sola regla por fila**, la mejor de cada
brazo. Sus tests (`z=-5.96`, `z=-4.42`, `z=-0.17`) son pareados sobre las 70
instancias, asi que responden a *"esta regla es mas robusta que este
baseline?"* y no a *"el metodo produce reglas mas robustas?"*.

Esta etiquetado con honestidad ("best of 30" en ambas filas GP) y es practica
habitual, pero un revisor puede senalar la asimetria.

**Que lanzar.** eps-barra de las 30 reglas del brazo principal y las 30 del
brazo ablado, **solo al nivel nominal** (sin los +20% y +40%): es un tercio del
coste completo, unas 5 h frente a ~15 h.

```
python scripts/eval_ablation_robustness.py \
    --arm "full=benchmarks/reevo_fixedfit/gp_tuned_seed*.json" \
    --arm "nowidth=benchmarks/tuned/ablation/nowidth_seed*.json"
```

`scripts/eval_ablation_robustness.py` ya existe y calcula exactamente eso: una
eps-barra por regla, media +- sd por brazo, y Wilcoxon pareado entre brazos.
Habria que reducir `K` o limitar a `width=1.0` para quedarse en el tercio de
coste.

**Que cambiaria en el paper.** La afirmacion de 7.3 sobre el origen de la
ventaja ("los terminales de anchura no son la fuente") pasaria a apoyarse en 30
reglas por brazo, igual que 7.2. La Tabla 8 puede quedarse como esta, con la
regla destacada, anadiendo una frase en el texto con el contraste de brazos.

**No lanzar hasta** que termine `scripts/time_gp_arm.py`, que ocupa la maquina
y cuyo resultado va a la celda vacia de la columna de tiempos en tab:baselines.

## 2. DOI de Zenodo

Unico `\todo` que queda en main.tex. Al depositar.
