---
name: escribir-papers
description: Escribir, auditar y preparar para envío artículos de investigación con resultados computacionales (LaTeX + experimentos + datos). Cubre la estructura obligatoria del artículo, las normas de referencias, tablas y figuras, la verificación de que las cifras cuadran con los datos, la elección de revista y la preparación del envío y del depósito. Usar siempre que se redacte o revise un paper, se integren resultados nuevos, se preparen tablas o figuras, se revisen las referencias, se elija revista de destino o se adapte el manuscrito a sus normas, se responda a una revisión, o se prepare el depósito de datos. También cuando el usuario pida "revisa esta sección", "mete estos resultados", "repasa las referencias", "a qué revista lo mandamos", "pásaselo a otro modelo como revisor", "prepara el envío" o "comprueba los números", aunque no diga la palabra paper.
---

# Escribir papers con resultados computacionales

Normas para un artículo cuyas afirmaciones se apoyan en experimentos
propios, sea cual sea el dominio. Las secciones 1 a 4 dicen **cómo tiene
que ser el artículo**; las siguientes, cómo comprobarlo y cómo sacarlo.

## 1. Estructura del artículo

Este esqueleto sirve para casi cualquier revista de aplicaciones y
metodología computacional. Los nombres se adaptan a la revista; el orden y
el contenido de cada bloque, no.

**Introducción.** Cuatro movimientos, en este orden: el hecho del mundo
real que motiva el problema; el hueco concreto en la literatura, no un
"poco explorado" genérico; las preguntas u objetivos del trabajo,
numerados si son varios; y al final, obligatoriamente, **las aportaciones
enumeradas y el mapa del artículo**. Cada aportación se enuncia como lo que
el trabajo añade, no como lo que hace: "una política que se aplica a
cualquier tamaño sin reentrenar" y no "se ha implementado un método". El
mapa es un párrafo corto que dice qué hay en cada sección.

**Estado del arte.** Una subsección por familia de métodos con los que el
trabajo se compara o de los que hereda, no un catálogo cronológico. Cada
subsección cierra diciendo qué deja sin resolver, y la sección entera cierra
declarando el hueco que el artículo llena. Si un método aparece luego en
las tablas de resultados, tiene que estar aquí.

**Descripción del problema.** Definición formal con toda la notación que el
resto del artículo va a usar, la función objetivo o criterio, y las
restricciones. Aquí se fija el vocabulario: todo símbolo que aparezca
después nace en esta sección o en la del método.

**Dataset.** Origen de las instancias o de los datos, tamaños y cuántos,
disponibilidad y licencia, y **la partición** en entrenamiento, validación
y prueba, declarada antes de que aparezca ningún resultado. Si alguna parte
se usó para ajustar algo, decirlo aquí y marcarlo después en las tablas.

**Método o algoritmo.** Conceptos antes que formalismo: primero qué hace y
por qué, con una figura de arquitectura recorrida caja por caja, y después
las ecuaciones. Pseudocódigo si el procedimiento no se entiende sin él.
Coste computacional en notación asintótica si es relevante.

**Entorno de trabajo.** Una tabla con el hardware (CPU, GPU si se usó,
memoria) y el software con versiones exactas: lenguaje, librerías
numéricas, framework de aprendizaje, sistema operativo. Es lo que permite
interpretar los tiempos y es condición de reproducibilidad.

**Configuración paramétrica.** Una tabla con **todos** los hiperparámetros
y su valor, y una frase por cada uno diciendo de dónde sale: valor por
defecto de la referencia original, búsqueda automática, o elección manual.
Si la configuración no es la misma en todos los experimentos, decir dónde
cambia y por qué.

**Métricas de evaluación.** Definición formal de cada métrica, sus
unidades, y si menor es mejor. Si hay contraste estadístico: qué test, de
una o dos colas, cuál es la unidad experimental y cómo se agregan las
repeticiones antes de contrastar. Las métricas se definen antes de usarse,
nunca en el pie de una tabla.

**Resultados.** Qué ocurrió, con sus tablas y figuras. Descripción, no
interpretación causal: los porqués van en la sección siguiente.

**Análisis.** Por qué ocurrió: ablaciones, estudios de sensibilidad,
análisis por subgrupos, casos donde falla. Cierra con las **limitaciones
enumeradas**, no escondidas en las conclusiones.

**Conclusiones.** Respuestas literales a las preguntas de la introducción,
en el mismo orden. No se introducen cifras nuevas ni resultados que no
estén antes. El trabajo futuro es la pregunta concreta que un experimento
deja abierta, no "exploraremos otras arquitecturas".

Dos reglas transversales:

- **Separar Resultados de Análisis.** Muchas subsecciones peleándose en una
  sola sección se ordenan solas al dividirlas en *qué pasó* / *qué lo
  explica*.
- **Definir antes de usar.** Auditar sección por sección que cada término,
  cada sigla y cada símbolo nace antes de gastarse. Lo que sobrevive a
  muchas relecturas: siglas nunca expandidas, el nombre de la arquitectura
  solo en las contribuciones y las tablas, subíndices sin ligar, letras
  griegas sin presentar. Y si se declara una convención para un símbolo
  (por ejemplo los extremos de un intervalo), extenderla explícitamente a
  los demás símbolos que la usen.

## 2. Referencias

- **Actuales.** Una proporción alta de los últimos cinco años, y las
  imprescindibles del área aunque sean antiguas. Un estado del arte cuya
  cita más reciente tiene ocho años se lee como un trabajo parado.
- **Cerradas por los dos lados.** Toda entrada de la bibliografía se cita
  en el texto y toda cita del texto existe en la bibliografía. Se comprueba
  automáticamente: extraer las claves citadas del fuente, las definidas del
  `.bib`, y contrastar los dos conjuntos.
- **Campos completos y correctos por tipo.** Artículo de revista: autores,
  título, revista, volumen, número, páginas, año y **DOI**. Congreso:
  actas, páginas, editorial y año. Capítulo: libro, editores, editorial.
  Preprint: repositorio e identificador, y marcarlo como preprint. Tesis:
  universidad y tipo.
- **DOI que resuelva.** Comprobar que cada DOI existe y apunta a lo que
  dice. Un DOI mal copiado sobrevive a todas las relecturas porque nadie
  lee cadenas de dígitos.
- **Sin duplicados ni entradas fantasma.** Dos claves distintas para el
  mismo trabajo, o una referencia que nunca se citó, delatan una
  bibliografía heredada de otro paper.
- **Nombres de revista consistentes**: completos o abreviados, pero no
  mezclados. El estilo lo fija la revista de destino.
- **Equilibrio de fuentes.** Un exceso de autocitas o de citas al propio
  grupo es lo primero que ve un editor. Si el trabajo se apoya en un
  artículo companion propio, citarlo por su versión publicada o su
  preprint con DOI, y declararlo en la carta de presentación.
- Revisar los avisos de BibTeX: campos vacíos, entradas sin año, autores
  mal separados. Son baratos de arreglar y caros de dejar.

## 3. Tablas y figuras

**El artículo tiene que llevarlas.** Una sección de método sin una figura
de arquitectura, o unos resultados sin una figura que los resuma, se leen
como un muro. Medir la densidad en vez de estimarla: contar palabras de
prosa por sección, descontando tablas y figuras, y mirar las que pasen de
unas seiscientas sin una sola ilustración.

**Calidad y formato**

- **Vectorial siempre que se pueda** (PDF, EPS); si tiene que ser mapa de
  bits, 300 dpi como mínimo, 600 para figuras con texto.
- **Fuentes incrustadas y vectoriales.** Comprobar que no hay Type 3: un
  solo Type 3 y producción lo rechaza.
- **Dibujar cada figura a su tamaño final.** Si se incluye al 62 % del
  ancho de línea, se dibuja con ese ancho en pulgadas: escala 1.0, y el
  cuerpo de letra del código es el que se ve en página. Estrechar el ancho
  natural manteniendo el ancho de inclusión **agranda** las fuentes.

**Estilo común**

- Una sola paleta para todo el artículo, con un color por método o familia,
  el mismo en todas las figuras.
- Una sola familia tipográfica, a ser posible la del cuerpo del texto, y
  dos cuerpos: uno para ejes y rótulos, otro menor para texto secundario.
  Iguales en todas las figuras.
- Legibles en escala de grises y con deficiencias de visión del color: no
  distinguir solo por color, sino también por marcador, trazo o relleno.
- Ejes rotulados con magnitud y unidad; leyendas dentro del área de ejes si
  caben; rejilla discreta o ninguna.
- **Los símbolos de la figura son los del artículo.** Etiquetar entidades
  con una notación que el texto no define es introducir símbolos nuevos en
  el peor sitio.

**Leyendas (captions)**

- **Concisas.** La leyenda dice **qué es** la figura o la tabla, en una o
  dos frases. Nada más.
- **La explicación va donde se referencia**, en el párrafo que la llama:
  cómo se lee, qué convención usa, qué hay que mirar y qué conclusión
  soporta. Una leyenda que enseña a leer el dibujo obliga a leerla dos
  veces.
- Las unidades y el significado de las marcas (barras de error, sombreados,
  daga de una columna contaminada) sí van en la leyenda, porque son parte
  de qué es.
- Tabla y figura numeradas y **citadas en el texto**; ninguna aparece sin
  que un párrafo la llame.

**Honestidad**

- Marcar las columnas o series contaminadas: si una columna contiene las
  instancias de entrenamiento o validación, decirlo con una daga, una nota
  al pie y un sombreado en la figura. Las cifras pueden ser correctas y la
  tabla, engañosa.
- Diagramas de caja con pocas observaciones mienten: con n≲20, puntos y
  mediana.
- Comprobar que el sombreado marca lo que dice la leyenda, y no lo
  contrario.
- Retirar las figuras que otra subsume.

## 4. Redacción y estilo

- **El artículo es una fotografía de la versión final, no el diario de las
  correcciones.** No se narra lo que se arregló ni lo que se descubrió
  tarde: se describe el sistema tal como quedó. La excepción es cuando el
  hallazgo *es* un resultado, y entonces se cuenta como resultado.
- **Registro académico**: sin coloquialismos, sin meta-narración ("en esta
  sección vamos a..."), sin negrita en la prosa. Cada párrafo abre por el
  hecho, no por lo que se propone hacer.
- **Las aportaciones, delante.** El resultado más fuerte y menos
  condicional va en las primeras frases del resumen y abre las
  conclusiones. Abrir con la concesión antes de haber enunciado nada
  regala la lectura.
- **Un movimiento de acotación**: declarar qué pregunta *no* se reabre y
  citar el trabajo que la fijó. Desactiva una objeción antes de que llegue.
- Si hay un artículo companion, **copiar su arquitectura y no su prosa**.

## 5. El verificador de números

Cada cifra del texto se recomputa desde los datos primarios, con un script
que se escribe una vez por proyecto y crece con el manuscrito: una
comprobación por afirmación, `OK`/`FALLO`/`PEND`, un recuento final, y
**código de salida distinto de cero si algo falla**.

- **Recomputar, no releer.** Comparar el texto contra el fichero agregado
  que lo generó no detecta nada.
- **Celda a celda, no solo la media.** Las tablas grandes y los apéndices
  se verifican valor a valor.
- **`PEND` en vez de `FALLO`** si el dato está a medias.
- **Colapsar espacios antes de buscar literales** en el fuente.
- **Reanclar, nunca debilitar.** Al reescribir prosa las comprobaciones
  literales fallan; se mueven a la frase nueva. Relajarlas convierte el
  verificador en decorado.
- **Cada apertura de fichero con su guarda**, para que el script no reviente
  en una copia parcial del proyecto.

Incluir aquí las comprobaciones de conformidad: palabras del resumen,
número de palabras clave, límite de páginas, secciones obligatorias
presentes, y las referencias cerradas por los dos lados.

## 6. Procedencia y reproducibilidad

- Antes de citar una cifra propia publicada en otro trabajo, localizar el
  fichero que la respalda: buscar la cifra en el fuente del otro artículo →
  localizar el script que generó esa tabla → identificar el fichero de
  datos y la clave exacta → recomputar con todos sus decimales.
- **Solo se puede construir sobre lo publicado.** Si un resultado propio no
  se reproduce con la versión publicada del método, no se documenta la
  discrepancia: se repite el experimento con la versión publicada.
- Guardar el resultado **crudo**, no el agregado: un barrido que guarda
  solo el mejor de N obliga a repetirlo entero el día que haga falta una
  curva.

## 7. Comparaciones justas

- **Declarar el eje de equidad.** Ningún resultado comparativo es
  interpretable sin decir qué se iguala. Enfrentar una pasada de un método
  barato contra cientos de muestras de uno caro no compara nada.
- Si los métodos tienen presupuestos ajustables, **una figura por
  presupuesto emparejado**.
- Declarar qué **no** está emparejado, típicamente el coste de
  entrenamiento.
- **Artefacto no es familia.** Un test con la instancia como unidad mide
  variación entre instancias, no entre modelos entrenados. Si cada lado es
  *un* artefacto seleccionado, la conclusión es sobre ese par y no sobre
  los paradigmas. O se evalúan varios artefactos por familia bajo un
  protocolo de selección declarado, o la afirmación se acota **en el
  resumen y en las conclusiones**, que es donde se lee sin matices.

## 8. Sobreafirmación

- **«No cambia» no es «no se detecta cambio».** Un experimento sin efecto
  bajo un criterio fijo no demuestra que el mecanismo esté intacto.
- **Suelo del *p* exacto.** Con pocas observaciones pareadas del mismo
  signo, el mínimo alcanzable es un valor fijo; verlo repetido no es una
  racha de significación. Declararlo, y decir cuántos contrastes se
  examinaron sin corrección de multiplicidad.
- Al suavizar una afirmación, **buscarla en todo el manuscrito**: se
  corrige el pasaje técnico y quedan en pie las contribuciones, el resumen
  y las conclusiones con la versión fuerte.

## 9. Elegir revista y conseguir sus normas

Qué decide, en orden: el **ámbito declarado** (una revista cuyo *aims and
scope* nombra una familia de métodos rechaza por ámbito un trabajo de otra
familia); si la revista **tolera el posicionamiento** del artículo, que pesa
más que el cuartil; la **categoría del índice** que el autor necesita;
la concentración de envíos propios en la misma revista; y el coste de los
conflictos al excluir revisores.

De la guía para autores hay que extraer lo verificable: límite de palabras
del resumen, número de palabras clave, estilo de citas, secciones
obligatorias, límite de páginas, política de preprints, tipo de revisión
(anónima simple o doble, que decide si un preprint compromete el
anonimato) y declaración de IA generativa. Las guías de algunas editoriales
no se dejan descargar automáticamente; conviene que el usuario las guarde.

De la plantilla: copiar al directorio del artículo la clase y los estilos
bibliográficos que use, para que compile en cualquier máquina. Comprobar lo
que la clase **no** hace (si carga o no codificación de fuentes, si compone
el ORCID, si trae su propio gestor de citas).

## 10. Compilación y conformidad

- **Cuatro pasadas de LaTeX, no tres.** Cuando la paginación cambia, tres
  no bastan y el PDF puede salir **sin bibliografía**, con las citas en
  interrogante y sin un solo error en pantalla.
- **Comprobar las fuentes del PDF** con `pdffonts`: ningún Type 3.
- **Las tablas centradas se desbordan en silencio**, sin aviso de
  `Overfull`. Medir con una caja de sonda:

```latex
\newsavebox{\probebox}\begin{lrbox}{\probebox} ...tabular... \end{lrbox}
\typeout{ancho=\the\wd\probebox\space linewidth=\the\linewidth}\usebox{\probebox}
```

- **Medir antes de elegir una opción de clase**: las opciones de revisión
  con interlineado doble pueden pasarse del límite de páginas.
- En cada compilación: errores, `Overfull`, páginas, citas y referencias
  sin resolver, y palabras del resumen. `chk_compila.py`, junto a este
  fichero, hace ese resumen.

## 11. Higiene de experimentos

- **Fichero de resultados largo y reanudable**: una fila por evento, saltar
  lo ya hecho al arrancar, volcar a disco por fila.
- **Los selectores por variable de entorno con defecto silencioso queman
  días**: entrenan el modelo equivocado sin un aviso. Los lanzadores deben
  **abortar** si la configuración no es la esperada.
- **Una figura no puede tumbar una campaña**: envolver la visualización en
  `try/except`.
- **Los heredocs de shell destrozan las contrabarras** y corrompen un
  fuente LaTeX en silencio. Escribir el script a fichero, o construir las
  contrabarras con `chr(92)`.
- En Windows, lanzar con `.bat` y redirección nativa, no con tuberías de
  PowerShell.

## 12. Revisión ciega simulada antes de enviar

Pasar el manuscrito **y el código** a un modelo distinto con el papel de
revisor de la revista de destino, en rondas sucesivas.

- **La copia que se le entrega debe ser idéntica al repositorio, fichero a
  fichero.** Si se refrescó parcialmente, devuelve problemas mayores que
  son fantasmas. Comprobarlo con un `diff` del árbol de fuentes y correr el
  verificador dentro de esa copia.
- **Verificar cada hallazgo antes de tocar nada.** Alrededor de la mitad no
  son ciertos. Clasificar en real, falso, y *culpa mía por cómo se lo he
  entregado*.

Preguntarle además: si la contribución basta para esa revista dado el
resultado que sea; si el resumen y las conclusiones enuncian la aportación
sin exagerarla ni enterrarla; y si el ejemplo dibujado en las figuras es lo
que el código calcula.

## 13. El depósito de datos y código

Se prueba **como lo probaría un extraño**, no desde el árbol de trabajo.

- Las rutas por defecto de los scripts dejan de resolver si el depósito
  reorganiza las carpetas.
- Reconstruir el fichero de requisitos desde los `import` reales, no de
  memoria.
- Empaquetar una carpeta entera mete notas internas que no deben
  publicarse; los ficheros de una versión publicada no se pueden editar.
- Citar el depósito en el artículo con su DOI de concepto, que apunta
  siempre a la última versión.

## 14. El envío

- **Doble anonimato**: marcar los bloques con identidad en el fuente con
  comentarios delimitadores y generar la copia anónima con un script que
  los elimine y **aborte** si queda algún rastro.
- **El formulario manda sobre la guía.** En la pantalla de subida aparecen
  requisitos que la guía no dice: si se sube fuente o PDF, si los
  conflictos van por fichero o por casilla, si las figuras van aparte, si
  la carta de presentación es obligatoria.
- **La carta de presentación** dice qué aporta el trabajo separando la
  contribución metodológica de la aplicación, confirma originalidad y no
  envío simultáneo, y declara cualquier trabajo relacionado en revisión en
  otra revista con su DOI de preprint.
- Mantener un **checklist del envío** en el repositorio con los ficheros a
  subir, los campos del formulario redactados para pegar y las decisiones
  que solo el autor puede tomar. Revisarlo contra el formulario real.

## 15. Lo que NO está automatizado

- **La lectura completa del PDF.** Ninguna comprobación la sustituye.
- **Detectar qué falta.** El verificador comprueba lo que está escrito, no
  lo que debería estar.
- **La decisión de encuadre**: qué hallazgo es el titular.
- **La equidad de una comparación**, que se ve mirando una figura.
- **Los identificadores externos** (DOI, ORCID) y las decisiones de
  autoría, orden de firmas y CRediT.
- **Las declaraciones que firma el autor**: originalidad, conflictos, uso
  de IA generativa. Se redactan, no se aprueban en su nombre.

Cuando algo de esta lista aparezca, **decirlo en voz alta** en vez de
simularlo.
