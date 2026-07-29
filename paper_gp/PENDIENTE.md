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

## 2. Barrido de lambda tambien para el brazo sin anchura

**Motivo.** El barrido de la Ec. 13 solo esta hecho para el brazo CON
terminales de anchura (lambda = 0.5, 1, 2, 4). Del brazo sin anchura solo
tenemos dos puntos: 12.62 bajo objetivo makespan y 12.47 bajo lambda = 1. De
ahi sale la linea discontinua de fig:lambda y la afirmacion de 7.2 de que ese
brazo "se queda en ~12.5% bajo ambos objetivos".

Con el barrido completo la linea pasaria a ser una **segunda curva**, y se
veria si el brazo ablado es realmente plano frente a lambda o si tambien
desciende, mas lentamente. La afirmacion "no tiene frontera disponible" pasaria
de aserción sobre dos puntos a resultado medido.

**Que lanzar.** 30 evoluciones: 10 semillas x lambda en {0.5, 2, 4}, con
`--no-width` y la configuracion de irace. Unas 5 h. Reutilizar
`scripts/lambda_sweep.py` anadiendo `--no-width` a los argumentos de cada job,
y escribir a un directorio propio para no pisar
`benchmarks/lambda_sweep/`.

**Que cambiaria en el paper.** fig:lambda con dos curvas en vez de curva +
linea; el parrafo final de 7.2 podria comparar pendientes en lugar de comparar
una curva contra un punto.

## 3. irace no se corrio para el brazo sin anchura

**Motivo.** irace se ejecuto **una sola vez**, sobre el conjunto de terminales
completo, y su configuracion ganadora (tournament 7, crossover 0.7695, maxtree
30, elitism 2) se aplica a todos los brazos, incluido el ablado. Ese brazo
compite por tanto con hiperparametros ajustados para un espacio de busqueda que
no es el suyo.

**No es necesariamente un fallo:** mantener la configuracion fija es lo que
hace que la ablacion sea *controlada*; si cada brazo se tunease por separado
cambiarian dos cosas a la vez y el efecto medido ya no seria atribuible a los
terminales. Pero conviene **decirlo explicitamente en 7.2** en lugar de dejarlo
implicito, porque un revisor puede plantearlo.

**Opcion barata (recomendada):** una frase en 7.2 declarando que la
configuracion se mantiene fija entre brazos y por que.

**Opcion cara:** repetir el estudio de irace con el terminal set reducido y
relanzar el brazo ablado con su propia configuracion. Anade ~200 evoluciones y
debilita la comparacion controlada; solo si un revisor lo exige.

## 4. DOI de Zenodo

Unico `\todo` que queda en main.tex. Al depositar.
