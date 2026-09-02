---
name: escribir-papers
description: Escribir, auditar y preparar para envío artículos de investigación con resultados computacionales (LaTeX + experimentos + datos). Usar siempre que se redacte o revise un paper, se integren resultados nuevos en el texto, se preparen tablas o figuras, se compruebe que las cifras del manuscrito cuadran con los datos, se elija revista de destino o se descarguen su plantilla y su guía para autores, se adapte el manuscrito a sus normas, se responda a una revisión, o se prepare el depósito de datos. También cuando el usuario pida "revisa esta sección", "mete estos resultados", "a qué revista lo mandamos", "pásaselo a otro modelo como revisor", "prepara el envío", "rellena el formulario" o "comprueba los números", aunque no diga la palabra paper.
---

# Escribir papers con resultados computacionales

Destilado de dos artículos completos del repositorio (`paper_gp/`, GP
hiper-heurístico; `paper/`, política DRL, rechazado en escritorio por
Journal of Intelligent Manufacturing y reencuadrado para Engineering
Applications of Artificial Intelligence). Las prácticas de abajo no son
teoría: cada una nació de un fallo real que llegó al manuscrito y
sobrevivió a varias relecturas humanas, o a una ronda de revisión.

Estado de automatización: **el verificador de números lo está; el resto es
disciplina asistida**. Lo que no se puede automatizar se marca como tal.

## 1. El verificador de números (la práctica central)

Cada cifra del texto se recomputa desde los datos primarios. Referencias:
`paper/verify_numbers.py` (885 comprobaciones) y
`paper_gp/verify_numbers.py` (84). Patrón: una comprobación por afirmación, `OK`/`FALLO`/`PEND`, y un
recuento final.

```python
def check(desc, esperado, real, tol=0.051):   # esperado = lo que dice el texto
def check_exacto(desc, cond, detalle="")      # condiciones booleanas
def pendiente(desc, motivo)                   # dato aún no disponible
```

Reglas aprendidas:

- **Recomputar, no releer.** Comparar el texto contra el CSV que lo generó no
  detecta nada; hay que recalcular desde los ficheros crudos (schedules,
  logs, JSON de la campaña).
- **Comprobar celda a celda, no solo la media.** Las 350 celdas del apéndice
  y las 108 de la tabla de clásicas se verifican una a una.
- **`PEND` en vez de `FALLO` si el dato está a medias.** Un CSV que se está
  regenerando no es un paper equivocado. Guardar con un conteo:
  `if len(datos) < 15: pendiente(...)` y saltar el bloque.
- **Colapsar espacios antes de buscar literales** en el `.tex`: una frase
  partida por el salto de línea no debe fallar espuriamente.
- **Reanclar, nunca debilitar.** Al reescribir prosa, las comprobaciones
  que buscan frases literales fallan. La reacción correcta es moverlas a la
  frase nueva; relajarlas para que pasen convierte el verificador en
  decorado. Si una comprobación pierde su ancla dos veces, anclarla a algo
  estructural (una fila de tabla, un `\label`) en vez de a la redacción.
- **Guardar fichero a fichero, no por carpeta.** Un bloque que comprobaba
  `if os.path.exists("envio/")` y luego abría dos ficheros de dentro
  reventaba con `FileNotFoundError` justo en la copia anónima, que lleva
  uno y no el otro. Cada `open` con su guarda.

Qué ha cazado en la práctica: una celda de tiempo de una tirada contaminada,
un test estadístico citado que nunca se calculó, "ambas curvas tienen un
único mínimo" cuando una tenía cinco, redondeos truncados (29,4 por 29,5),
un rango de varianza inventado, y una convención de makespan distinta entre
el texto y el código.

## 2. Definir antes de usar

Auditoría manual, repetida por sección. Buscar cada término técnico y cada
símbolo, y comprobar que nace antes de gastarse.

Casos reales que sobrevivieron a muchas relecturas: `policy` en la primera
frase del método sin definir; SPT/LPT/MOR/MWKR **nunca** expandidas en todo
el manuscrito; "Deep Sets" en las contribuciones y en las tablas pero jamás
en el cuerpo; `π(a|s)` con `a` y `s` sin ligar; γ sin presentarse como factor
de descuento; *rollout*, *greedy*, *checkpoint*, *zero-shot*, *specialist*,
la "carrera" de irace y sus "elites".

Orden que funciona en una sección de método: **(1)** el marco conceptual
completo con sus términos, **(2)** por qué la arquitectura necesita cada
pieza, **(3)** la instanciación en el problema, **(4)** el recorrido de la
figura caja por caja, **(5)** el formalismo.

Una figura se recorre donde se menciona, y se declara donde se menciona: un
`\begin{figure}` colocado en la subsección equivocada flota dos páginas.

## 3. Trazar la procedencia de cada número ajeno

Antes de citar una cifra propia publicada en otro artículo, localizar el
fichero que la respalda. En este repositorio convivían **tres** valores del
mismo experimento (18,59 / 17,30 / 17,71) y solo el último era el publicado.

Procedimiento: buscar la cifra publicada en el `.tex` del otro paper →
localizar el script que generó esa tabla → identificar el CSV y la clave
exacta (aquí, `reevo_fixedfit/summary.csv` con `method == gp_tuned_seed1`) →
recomputar y comprobar que da el valor publicado con todos sus decimales.

## 4. Comparaciones: declarar el eje de equidad

Ningún resultado comparativo es interpretable sin decir qué se iguala.
Error real cometido: enfrentar **una pasada** de una regla contra **1024
muestras** de una política. Al emparejar presupuestos, la ventaja cayó de
67/70 a 46/70 y la mediana de +4,5 a +1,3 puntos.

- Si los métodos tienen presupuestos ajustables, **una figura por
  presupuesto emparejado**, no una comparación agregada.
- Nombrar en los ejes quién es quién (`GP rule` / `DRL policy`), no
  "método A".
- Declarar qué **no** está emparejado (aquí: los costes de entrenamiento),
  y decir explícitamente que se comparan artefactos publicados y no un
  estudio controlado.
- **Artefacto no es familia.** Un Wilcoxon con la instancia como unidad
  mide variación entre instancias, no entre artefactos entrenados. Si cada
  lado es *un* modelo seleccionado, la conclusión es sobre ese par y no
  sobre los paradigmas, por muy pequeño que salga el *p*. Dos rondas de
  revisión seguidas señalaron lo mismo. O se evalúan varios artefactos por
  familia bajo un protocolo de selección declarado, o la afirmación se
  acota al par en el resumen, en los *highlights* y en las conclusiones,
  que es donde se lee sin los matices del cuerpo.

## 5. Honestidad en tablas y figuras

- **Marcar las columnas contaminadas.** La clase 20×15 de una tabla eran
  las diez instancias de entrenamiento y desarrollo: ni una era no vista, y
  nada lo decía. Ahora lleva daga, nota en el pie y sombreado en la figura.
  El verificador no puede cazar esto: todas las cifras eran correctas.
- **Diagramas de caja con n pequeña mienten.** Con 10 instancias por clase,
  una caja colapsaba a una línea y `showfliers=False` escondía justo los
  extremos que contaban la historia. Con n≲20, puntos y mediana.
- **Comprobar que el sombreado marca lo que dice la leyenda.** Un
  `fill_between` señalaba la región donde el método *pierde* mientras la
  etiqueta decía "policy better".
- **Retirar figuras que otra subsume.** Nueve barras contra un baseline
  débil sobran cuando existe una con 70 instancias y el baseline fuerte.

## 6. Resultados negativos: el molde de "delimitación"

Un hallazgo negativo se publica cuando se le pone frontera. Molde probado:
*qué aporta y qué no aporta X, en dos mitades*.

Ejemplo real: "la conciencia intervalar no aporta nada al makespan esperado
(quitar las features de anchura no cambia nada, y entrenar sobre instancias
crisp tampoco); su valor aparece bajo un objetivo que penaliza la anchura,
que no tiene contrapartida en el problema determinista".

Corolario operativo: **si un resultado sale inerte, comprobar primero qué
optimiza de verdad la función objetivo**. Aquí las features de anchura eran
inertes porque el objetivo era función únicamente de los límites superiores,
que ya eran entradas — la redundancia era estructural, no empírica.

## 7. Estructura y retórica

Arquitectura que funcionó en ambos papers:

```
1 Introducción      hecho del mundo real → hueco → preguntas → contribuciones → mapa
2 Trabajo relacionado   con una subsección por familia de métodos comparados
3 Problema          notación y métrica, con la elección de ranking acotada
4 Método            conceptos → figura recorrida → formalismo
5 Metodología       instancias y partición, configuración, baselines
6 Resultados        qué consigue
7 Análisis          qué lo explica + limitaciones enumeradas al cierre
8 Conclusiones      respuestas a las preguntas de §1 + trabajo futuro con contenido
```

- **Separar Resultados de Análisis.** Nueve subsecciones peleándose en una
  sola sección se ordenan solas al dividirlas en *qué pasó* / *qué lo
  explica*.
- **Preguntas explícitas en la introducción** (Q1–Q3) y respuestas
  literales en las conclusiones.
- **Un movimiento de acotación**: declarar qué pregunta *no* se reabre y
  citar el estudio que la fijó. Desactiva una objeción antes de que llegue.
- **Limitaciones enumeradas** ("cuatro limitaciones acotan estas
  conclusiones: primero… finalmente…"), al final del análisis, no enterradas
  en las conclusiones.
- **Trabajo futuro con sustancia técnica**: la pregunta que un experimento
  concreto deja abierta, no "exploraremos otras arquitecturas".

Si hay un artículo companion, **copiar su arquitectura y no su prosa**: la
organización no es plagio, el texto sí. Redactar contra el original abierto
para divergir a conciencia.

## 8. Elegir revista y conseguir sus normas

### Qué decide la elección

El factor de impacto casi nunca decide: en el caso real las cuatro
candidatas eran Q1 en la misma categoría. Lo que decidió fue esto, en
orden:

1. **El ámbito declarado.** *Swarm and Evolutionary Computation* dice
   ser de "computación evolutiva y de enjambre"; PPO con Deep Sets no
   es ninguna de las dos, y el editor lo rechazaría por ámbito antes de
   mandarlo a revisión. Leer la sección *Aims and scope*, no la
   reputación.
2. **Si la revista tolera el posicionamiento del artículo.** El paper
   de la política no gana a las metaheurísticas y no pretende hacerlo:
   vende velocidad y generalización. En una revista de investigación
   operativa el primer revisor pregunta por qué pierde contra lo que ya
   existe, y "es otra clase computacional" no le basta. En una revista
   de aprendizaje ese marco es el de partida y no hay que defenderlo.
   **Este criterio pesa más que el cuartil.**
3. **La categoría JCR que el autor necesita** para su evaluación
   (aquí, *Computer Science, Artificial Intelligence*). Comprobarlo,
   no suponerlo.
4. **Concentración de envíos.** Con dos artículos ya en revisión en la
   misma revista, repartir reduce el riesgo de que un solo cuello de
   botella editorial frene tres trabajos.
5. **El coste de los conflictos.** Excluir coautores recientes y el
   propio grupo es obligado; en un campo pequeño eso deja el artículo
   en manos de revisores que no son del subcampo, y conviene anticipar
   qué secciones tendrán que defenderse solas.

Sobre las métricas: los agregadores discrepan entre sí (7,7 frente a
7,88 para la misma revista). Sirven para decidir; para un CV o un
informe, solo vale el JCR.

### Conseguir la guía para autores

- **Springer**: `https://link.springer.com/journal/<id>/submission-guidelines`.
  Suele dejarse leer. Si el usuario la guarda como HTML, extraer el
  texto plano y buscar por palabras clave (`Abstract`, `Keywords`,
  `Statements and Declarations`, `Reference`, `ORCID`, `LLM`).
- **Elsevier**: `https://www.sciencedirect.com/journal/<slug>/publish/guide-for-authors`
  devuelve **403** a la descarga automática. Pedir al usuario que la
  guarde; si la guarda como *Imprimir a PDF*, no tendrá capa de texto y
  hay que leerla como imágenes por páginas.
- Extraer siempre lo **verificable y accionable**: límite de palabras
  del abstract, número de keywords, estilo de citas, secciones
  obligatorias (sin ellas devuelven el envío), política de preprints,
  tipo de revisión (anónima simple o doble: decide si un preprint
  compromete el anonimato) y declaración de IA generativa.

### Descargar la plantilla LaTeX

- **Springer Nature** (`sn-jnl`): la URL de descarga cambia. La estable
  es la página `https://www.springernature.com/gp/authors/campaigns/latex-author-support`;
  extraer de ahí el enlace al zip. La antigua `resource-cms...` devuelve
  400; la vigente es del dominio `cms-resources.apps.public.k8s.springernature.io`.
- **Elsevier**: `elsarticle` viene con cualquier distribución TeX.
- Copiar al directorio del paper la clase y los `.bst` que use, para que
  compile en cualquier máquina sin depender del gestor de paquetes.
- **Si falta un paquete que la clase exige** y el gestor no lo conoce
  (`cuted` para `sn-jnl` en MiKTeX), bajarlo de CTAN y generarlo:

```bash
curl -o sttools.zip https://mirrors.ctan.org/macros/latex/contrib/sttools.zip
# descomprimir y, en el directorio del .ins:
pdftex -interaction=nonstopmode sttools.ins    # docstrip genera los .sty
```

Al convertir a la plantilla, comprobar lo que la clase **no** hace: la
de Springer no carga `fontenc`, no compone el ORCID en la portada (se
introduce en el sistema de envío) y trae su propio `natbib` e
`hyperref`, así que las cargas manuales sobran.

## 9. Normas de revista y compilación

- Leer la guía y extraer lo verificable: límite del abstract, estilo de
  citas, secciones obligatorias, ORCID, política de preprints. El propio
  PDF de la guía suele estar en el repo.
- **Comprobar las fuentes del PDF**: `pdffonts main.pdf`. Un solo Type 3 y
  producción lo rechaza. Causas vistas: `fontenc` T1 sin `lmodern` (cae en
  las EC de mapa de bits) y matplotlib, que por defecto incrusta Type 3
  (`pdf.fonttype = 42` lo arregla).
- **Las tablas centradas se desbordan en silencio**, sin `Overfull`. Medir
  con una caja de sonda:

```latex
\newsavebox{\probebox}\begin{lrbox}{\probebox} ...tabular... \end{lrbox}
\typeout{ancho=\the\wd\probebox\space linewidth=\the\linewidth}\usebox{\probebox}
```

- Comprobar en cada compilación: errores, `Overfull`, páginas, citas sin
  resolver y palabras del abstract. Script de referencia en el scratchpad de
  la sesión (`chk_compila.py`).

## 10. Higiene de experimentos que alimentan el paper

- **Guardar el resultado crudo, no el agregado.** Un barrido que guardó solo
  el mejor de 1024 muestras obligó a repetir 10 horas para poder dibujar la
  curva del presupuesto.
- **CSV largo y reanudable**: una fila por evento, saltar lo ya hecho,
  `flush()` por fila. Un proceso muerto no debe costar la campaña.
- **Los selectores por variable de entorno con defecto silencioso queman
  días.** `DEEPLJSP_AGENT` con defecto `v1` entrenó tres semillas del agente
  equivocado sin un solo aviso. Los lanzadores deben **abortar** si la
  configuración no es la esperada.
- **Una figura no puede tumbar una campaña**: envolver la visualización en
  `try/except`.
- **Los heredocs de shell destrozan las contrabarras.** Un script de Python
  pegado en un heredoc convierte `\ref` en otra cosa y corrompe el `.tex`
  en silencio. Escribir el script a fichero y ejecutarlo, o construir las
  contrabarras con `chr(92)`. Es el fallo operativo que más veces se repitió.
- **En Windows, lanzar con `.bat` y redirección de `cmd`**, no con tuberías
  de PowerShell: un reinicio del proceso padre congela al hijo escribiendo
  en una tubería muerta, y `Select-Object -First N` mata el proceso de
  origen.

## 11. Revisión ciega simulada antes de enviar

Pasar el manuscrito **y el código** a un modelo distinto con el papel de
revisor de la revista de destino, en rondas sucesivas. Cinco rondas
movieron el veredicto de *reject* a *no hay motivo de rechazo sobre los
resultados centrales*, y los dos hallazgos más profundos salieron de ahí.

Dos reglas que costaron horas aprender:

- **El workspace del revisor debe ser idéntico al repo, fichero a
  fichero.** Se le entrega una copia aislada; si esa copia se refrescó
  parcialmente, el revisor audita código que ya no existe. En la ronda 6,
  dos de los tres problemas mayores eran ficheros desfasados, y en la 7
  uno más. Comprobarlo con un `diff` de todo el árbol de fuentes antes de
  lanzar, y correr el verificador dentro del workspace.
- **Verificar cada hallazgo antes de tocar nada.** Alrededor de la mitad no
  eran ciertos. Clasificar en tres montones: real, falso, y *culpa mía por
  cómo se lo he entregado*. Ese tercero es el más incómodo y el más
  frecuente.

Qué preguntarle además del guion habitual: si la contribución basta para
esa revista *dado* el resultado que sea (si nadie gana, decirlo); si el
resumen, los *highlights* y las conclusiones enuncian la aportación sin
exagerarla ni enterrarla; y si el ejemplo dibujado en las figuras es lo que
el código calcula de verdad.

## 12. Sobreafirmación: decir lo que el dato sostiene

Lo que más veces han marcado los revisores, y siempre con razón.

- **«No cambia» no es «no se detecta cambio».** Un experimento que no
  encuentra desplazamiento sistemático bajo un criterio fijo no demuestra
  que los pesos estén intactos: no compara parámetros. La redacción honesta
  es la del efecto medido, no la del mecanismo supuesto.
- **Suelo del *p* exacto.** Con seis observaciones pareadas del mismo
  signo, el mínimo alcanzable a dos colas es *p*=0,03125. Ver ese valor
  repetido en varios contrastes no es una racha de significación: es el
  suelo. Declararlo, y decir cuántos contrastes relacionados se examinaron
  sin corrección de multiplicidad.
- **Adverbios que salvan un párrafo**: «mainly», «predominantly», «no
  systematic ... was detected». Cuestan una palabra y quitan una objeción
  mayor.
- Al suavizar una afirmación, **buscarla en todo el manuscrito**. Se
  suaviza el pasaje técnico y quedan en pie la lista de contribuciones, el
  resumen y las conclusiones diciendo la versión fuerte.

## 13. El depósito publicado no es el repositorio

El paquete que cita el paper se prueba **como lo probaría un extraño**, no
desde el árbol de trabajo donde todo resuelve por accidente.

- **Las rutas por defecto de los scripts.** El depósito colocaba las reglas
  comparadas en `rules/` mientras el código las leía de
  `benchmarks/...`; en el repo funcionaba y en el paquete no. Lo cazó un
  revisor cuya copia imitaba el depósito.
- **Las dependencias que nadie declara.** `requirements.txt` listaba cuatro
  paquetes y faltaba pandas, que importaban cuatro módulos del
  entrenamiento: un entorno limpio hecho con ese fichero no entrenaba.
  Reconstruir el fichero desde los `import` reales, no de memoria.
- **Las notas internas se cuelan.** Empaquetar la carpeta entera metió en
  el zip una guía de trabajo que decía de sí misma que no debía publicarse.
  Los ficheros de una versión publicada no se pueden editar: sale caro.
- Un comprobador que recorra las rutas que el verificador consulta y diga
  si el paquete las cubre todas paga su coste el primer día.

## 14. Del rechazo en escritorio al formulario de envío

- **Un desk-reject no es un veredicto sobre el contenido.** El de este
  paper vino por encaje. Reencuadrar cuesta menos de lo que parece si la
  arquitectura ya está: cambio de clase LaTeX, separación de identidad y
  ajuste del resumen a las condiciones de la revista nueva.
- **Doble anonimato**: marcar los bloques con identidad en el fuente
  (`%<<IDENTIDAD ... %IDENTIDAD>>`) y generar la copia anónima con un
  script que los elimine y **aborte** si queda algún rastro. A mano se
  olvida uno.
- **Medir antes de elegir opción de clase.** `elsarticle` con `review` da
  interlineado doble: en este paper, 51 páginas contra un límite duro de
  50, frente a 37 con `preprint`. La guía pedía una columna, que ambas
  cumplen.
- **El formulario manda sobre la guía.** Al llegar a la pantalla de subida,
  cuatro cosas que habíamos deducido de la guía eran falsas: un envío en
  LaTeX sube **PDF y no fuente** (las fuentes, en la revisión), los
  conflictos se confirman con una **casilla** y no con el .docx de la
  herramienta, las figuras **no** van aparte en el envío inicial, y la
  **carta de presentación es obligatoria**. Leer el formulario real antes
  de dar por cerrado el plan de ficheros.
- **La carta de presentación** dice qué aporta el trabajo separando la
  parte de IA de la aplicación, confirma originalidad y no envío
  simultáneo, y **declara cualquier trabajo relacionado en revisión en otra
  revista** con su DOI de preprint. Esa transparencia es mejor darla que
  esperar a que la pregunten.

## 15. Lo que NO está automatizado

Honestidad sobre el estado real:

- **La lectura completa del PDF.** Ninguna comprobación sustituye a leerlo
  entero una vez.
- **Detectar qué falta.** El verificador comprueba lo que está escrito, no
  lo que debería estar. Las tres ablaciones que faltaban las señaló el autor.
- **La decisión de encuadre.** Qué hallazgo es el titular y cuál es una nota
  al pie es criterio, no cálculo.
- **La equidad de una comparación.** El emparejamiento de presupuestos lo
  detectó el autor mirando una figura, no el verificador.
- **Los identificadores externos** (DOI del preprint, ORCID) y las decisiones
  de autoría.

Cuando algo de esta lista aparezca, **decirlo en voz alta** en vez de
simularlo. Un mensaje de commit describió una vez un cambio que nunca llegó
al fichero porque el comando que lo aplicaba fue bloqueado y nadie lo
comprobó.
