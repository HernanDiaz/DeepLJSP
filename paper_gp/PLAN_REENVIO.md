# Plan de reenvío del paper de GP

Tras el rechazo de Swarm and Evolutionary Computation
(`revisiones/2026-09-21_swevo_reject.md`). Tres revisiones, ninguna
señala un error de cálculo: las tres dicen que las afirmaciones van por
delante de la evidencia y que las comparaciones no están igualadas.

El umbral que hay que superar lo fija el revisor 2: *ser el primer GP para
IJSP no basta; hay que demostrar bajo qué escenario, objetivo y presupuesto
hay una ventaja cuantificable*. Todo lo demás es reparación; **E6 es lo que
crea la contribución**.

## Experimentos, en orden

### E0 — Selección sin contaminación *(gratis, primero)*

R3.1 sostiene que la regla destacada se eligió mirando las setenta
instancias, incluidas las sesenta de prueba. Comprobar qué se hizo
realmente; si fue así, reseleccionar usando **solo** el conjunto de
desarrollo (TA15--TA20) y publicar como resultado principal la **media y
desviación de las treinta reglas**, con la destacada como resultado
secundario.

Sin tiradas nuevas: reanálisis de los depósitos existentes. Es el que
arregla el número principal del artículo, así que va primero.

### E1 — Robustez sin efecto denominador *(barato)*

R3.2, la crítica más afilada del lote. ε̄ va normalizado por E[Cmax] y el
brazo robusto tiene un RE más alto, de modo que parte de la mejora puede
ser del denominador. Hacer tres cosas:

- reportar la **desviación absoluta** junto a la normalizada;
- comparar métodos a **niveles de RE comparables**;
- añadir realizaciones **no uniformes** (triangular centrada, beta
  sesgada) y de **caso peor**, para separar el hallazgo de la hipótesis
  uniforme.

Sin reevolución: se reevalúan los órdenes ya almacenados bajo sorteos
nuevos. Horas.

### E2 — Sensibilidad al conjunto de entrenamiento *(medio; lo piden los tres)*

`scripts/evolve_gp_rule.py` ya acepta `--train-ids`, así que **no hace falta
código nuevo**. Dos ejes:

- **qué cuatro**: tres o cuatro cuádruplas alternativas de la clase
  20×15, distintas de TA11--TA14;
- **cuántas**: conjuntos de 2, 4 y 8 instancias.

Treinta semillas por campaña. Reportar media y desviación por campaña, y
si la estructura de la regla (uso de terminales) es estable entre ellas.

Coste: una campaña de treinta artefactos son unas 4,4 h; seis campañas,
unas 26 h de un carril, en torno a 4--5 h en seis. Sirve además al paper de
DRL, que entrena en las mismas cuatro instancias y tiene el mismo hueco.

### E3 — Caso ilustrativo pequeño *(barato)*

R1.4. Una instancia pequeña donde se comparen las puntuaciones de
prioridad de la regla evolucionada contra SPT y MWKR, y se trace cómo el
terminal de anchura inclina la decisión hacia resolver antes la
incertidumbre. Reutilizar el dibujo de Gantt intervalar del paper de DRL
(`scripts/make_gantt_figure.py`), que ya usa la convención de flancos
inclinados.

### E4 — Intervalos asimétricos *(medio)*

R3.4. Todas las instancias tienen intervalos simétricos, así que la
contribución de las anchuras podría depender del esquema de generación.
Generar instancias con anchura asimétrica, reevolucionar treinta semillas y
rehacer el análisis de robustez.

### E5 — Decodificador y baselines intervalares *(medio)*

R3.3. Describir explícitamente cómo trata los intervalos cada baseline,
añadir baselines lexicográficas intervalares, y evaluar la regla bajo el
decodificador Giffler--Thompson para aislar la diferencia de decodificador
de la diferencia de regla.

### E6 — Presupuesto igualado contra las metaheurísticas *(el caro, y el que decide)*

R2 y R3.5. Hoy las metaheurísticas solo se comparan en las doce clásicas,
con lenguajes y presupuestos distintos. Hay que correr GA/fEABC/ESABC bajo
presupuesto igualado sobre las setenta.

**Este experimento no es defensivo, es la contribución.** Una regla de
despacho produce un schedule en milisegundos; una metaheurística necesita
segundos. Si se traza calidad frente a presupuesto de tiempo, **tiene que
existir un régimen de presupuesto bajo donde la regla gana**, y encontrarlo
y acotarlo es exactamente la «ventaja cuantificable bajo un escenario,
objetivo y presupuesto» que el revisor 2 exige. La figura que sale de aquí
es la que justifica el artículo.

Riesgo: si ese cruce cae en un presupuesto irrelevante para la práctica, el
artículo tiene que decirlo y conformarse con el encuadre de «baseline
rápido e interpretable» que propone R1.3.

## Reescritura

- **Contribución 3** consistente con la evidencia: las anchuras no mejoran
  el makespan esperado bajo el objetivo por defecto, y su valor aparece
  bajo un objetivo que paga por la anchura. Añadir orientación accionable
  para elegir λ y declarar la frontera de aplicabilidad.
- **Abstract**: quitar toda implicación de eficiencia (el mejor-de-1024 no
  es más rápido que las metaheurísticas) y acotar el «la información
  intervalar no aporta al makespan» con «bajo el objetivo por defecto y
  este banco de pruebas».
- **Mejor-de-N** encuadrado como herramienta de comparación emparentada
  con GRASP y el arranque múltiple, no como vía rápida.
- **Muestreo uniforme** declarado explícitamente como oráculo posterior de
  medición que no interviene en la evolución ni en la formulación.
- **Posicionamiento**: «baseline rápido, interpretable y de alta calidad»,
  no «solución general al IJSP», salvo que E6 diga otra cosa.
- **Conclusiones** reescritas sobre lo que demuestre E6.

## Revista

Descartada EAAI: el paper de DRL está allí y concentrar los dos envíos en
la misma revista multiplica el riesgo de un cuello de botella editorial.

Candidatas, por encaje con el posicionamiento:

- **International Journal of Production Research**. Audiencia de
  planificación de taller, valora interpretabilidad y velocidad de
  decisión, y no exige ganar a las metaheurísticas para publicar.
- **Applied Soft Computing**. Amplia y tolerante con hiperheurísticas
  aplicadas. *Comprobar antes si este trabajo ya pasó por allí.*
- **Computers & Industrial Engineering**. Similar a la primera, algo más
  orientada a operaciones.

Menos recomendables: *Journal of Scheduling* y *Computers & Operations
Research* presionarán sobre la distancia con las metaheurísticas, que es
justo el flanco débil.

## Antes de enviar

Pasar una ronda de revisión ciega simulada, con el guion de la sección
correspondiente del skill `escribir-papers`: entregar una copia **idéntica
al repositorio**, fichero a fichero, y verificar cada hallazgo antes de
tocar nada.
