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

### E0 — Selección sin contaminación — **HECHO**

R3.1 sostiene que la regla destacada se eligió mirando las setenta
instancias, incluidas las sesenta de prueba. Comprobar qué se hizo
realmente; si fue así, reseleccionar usando **solo** el conjunto de
desarrollo (TA15--TA20) y publicar como resultado principal la **media y
desviación de las treinta reglas**, con la destacada como resultado
secundario.

Sin tiradas nuevas: reanálisis de los depósitos existentes. Es el que
arregla el número principal del artículo, así que va primero.

### E1 — Robustez sin efecto denominador — **HECHO**

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

### E2 — Sensibilidad al conjunto de entrenamiento — **HECHO**

`scripts/evolve_gp_rule.py` ya acepta `--train-ids`, así que **no hace falta
código nuevo**. Dos ejes:

- **qué cuatro**: tres o cuatro cuádruplas alternativas de la clase
  20×15, distintas de TA11--TA14;
- **cuántas**: conjuntos de 2, 4 y 8 instancias.

Treinta semillas por campaña. Reportar media y desviación por campaña, y
si la estructura de la regla (uso de terminales) es estable entre ellas.

Cinco campañas de treinta evoluciones, unas 16 h en seis carriles
(`scripts/e2_sensibilidad_entrenamiento.py`, análisis en
`scripts/e2_analiza.py`, depósito en `benchmarks/e2_entrenamiento/`).

**Resultado.** Sobre las sesenta instancias que ninguna campaña toca, las
seis medias caben en 0,66 puntos (18,95 % a 19,61 %) contra una
desviación entre semillas de 0,93--1,35 dentro de cada campaña: importa
más la semilla que el conjunto. Ninguna campaña se separa de TA11--TA14
tras Holm sobre los cinco contrastes (menor p ajustado, 0,12). El eje del
tamaño se mueve poco y en el sentido esperado: bajar a dos instancias
cuesta 0,46 puntos y subir a ocho gana 0,20. Lo que sí cambia es la forma
de las reglas: WKRW cae del 12,0 % al 5,8--11,8 % del recuento de
terminales y EST sube del 9,7 % al 10,8--14,4 %.

Escrito en §7.6 (`sec:trainset`, tabla `tab:trainset`) y anclado en el
verificador. Sirve además al paper de DRL, que entrena en las mismas
cuatro instancias y tiene el mismo hueco.

### E3 — Caso ilustrativo pequeño — **HECHO**

R1.4. `scripts/e3_caso_ilustrativo.py` genera instancias 3x3 con el
esquema de la §5.1 y busca una en la que quitar el término de anchura
cambie **una sola** decisión y empeore el makespan. El criterio no mira
a SPT ni a MWKR, así que lo que hagan ellas en el caso es un hallazgo y
no una condición de la búsqueda. La figura,
`scripts/make_e3_figure.py`, usa la convención de flancos inclinados del
paper de DRL.

**Resultado.** La primera instancia así es la semilla 300. En la tercera
decisión los tres candidatos pueden empezar a la vez, de modo que SLACK
se anula y decide el resto. Sin el término de anchura gana `o22` (5
contra 6); el término aporta −4 a `o31` contra −2 a `o22` y da la vuelta
a un punto de diferencia, así que la regla adelanta `o31`, la primera
operación del trabajo cuyo trabajo pendiente es el más incierto ([41,45]
contra [16,18]). El schedule cierra en [103,117] contra [113,133] sin el
término; SPT da [147,170] y MWKR [143,161].

**Y el censo, que es lo que acota la lectura.** En las primeras 800
instancias generadas así, quitar el término no cambia la traza en 668;
de las 132 que cambian, 93 acaban en el mismo makespan, 21 mejor con el
término y 18 peor. A esa escala el terminal de anchura actúa poco y poco
mejor que una moneda: el ejemplo enseña el mecanismo, no su tamaño, y
eso se dice en el texto.

Escrito en §7.2 (`sec:case`, tabla `tab:case`, figura `fig:case`) y
anclado en el verificador.

**De paso.** Las seis figuras del paper salían en **Type 3**, que las
imprentas de Elsevier rechazan. Faltaba `pdf.fonttype: 42` en los seis
scripts que las generan; puesto y regeneradas. Ahora todas van en
TrueType embebido.

### E4 — Intervalos asimétricos *(medio)*

R3.4. Todas las instancias tienen intervalos simétricos, así que la
contribución de las anchuras podría depender del esquema de generación.
Generar instancias con anchura asimétrica, reevolucionar treinta semillas y
rehacer el análisis de robustez.

### E5 — Decodificador y baselines intervalares *(medio)*

R3.3. `scripts/e5_decodificador_baselines.py` mide las tres cosas.

**Convenios.** Cada regla clásica, ordenando por el extremo inferior,
por el punto medio y por el superior: SPT 633,1--642,5; LPT
703,1--704,4; MWKR 62,9--64,6; EST 42,7--45,1. La mayor dispersión que
abre un convenio es 2,4 puntos, contra los 23,3 que separan a la mejor
regla llana de la evolucionada. Cómo se resumen los intervalos no es lo
que la comparación mide.

**Decodificador.** El cuadro de dos por dos, por fin separado:

| | Semiactivo | Giffler--Thompson |
|---|---|---|
| MWKR | 64,7 | 29,5 |
| Evolucionada, media de 30 | **18,99 ± 1,33** | 23,18 ± 7,47 |
| Evolucionada, destacada | 17,71 | 18,15 |

A decodificador fijo la regla gana a MWKR con los dos. A regla fija cada
una prefiere el suyo: la evolucionada pierde 4,2 puntos al entrar en el
conflict set —y su desviación se dispara de 1,33 a 7,47, porque alguna
regla se rompe cuando le restringen los candidatos— y MWKR gana 35,2 al
entrar. La destacada es el caso en que el decodificador casi no importa,
17,71 contra 18,15, p = 0,32.

Escrito en §6.4 (`sec:decoder`, tabla `tab:decoder`) y anclado en el
verificador.

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
