---
name: escribir-papers
description: Escribir, auditar y preparar para envío artículos de investigación con resultados computacionales (LaTeX + experimentos + datos). Usar siempre que se redacte o revise un paper, se integren resultados nuevos en el texto, se preparen tablas o figuras, se compruebe que las cifras del manuscrito cuadran con los datos, se elija revista de destino o se descarguen su plantilla y su guía para autores, se adapte el manuscrito a sus normas, se responda a una revisión, o se prepare el depósito de datos. También cuando el usuario pida "revisa esta sección", "mete estos resultados", "a qué revista lo mandamos", "pásaselo a otro modelo como revisor", "prepara el envío", "rellena el formulario" o "comprueba los números", aunque no diga la palabra paper.
---

# Escribir papers con resultados computacionales

Prácticas para cualquier artículo cuyas afirmaciones se apoyen en
experimentos propios, sea cual sea el dominio, el método y la revista.
Ninguna es teoría: todas nacieron de fallos que llegaron a un manuscrito
real y sobrevivieron a varias relecturas humanas, o a una ronda de
revisión.

Estado de automatización: **el verificador de números lo está; el resto es
disciplina asistida**. Lo que no se puede automatizar se marca como tal.

## 1. El verificador de números (la práctica central)

Cada cifra del texto se recomputa desde los datos primarios, con un script
que se escribe una vez por proyecto y crece con el manuscrito. Patrón: una
comprobación por afirmación, `OK`/`FALLO`/`PEND`, un recuento final, y
**código de salida distinto de cero si algo falla**, sin lo cual no sirve
como comprobación automatizable.

```python
def check(desc, esperado, real, tol=0.051):   # esperado = lo que dice el texto
def check_exacto(desc, cond, detalle="")      # condiciones booleanas
def pendiente(desc, motivo)                   # dato aún no disponible
```

Reglas:

- **Recomputar, no releer.** Comparar el texto contra el fichero agregado
  que lo generó no detecta nada; hay que recalcular desde los datos crudos.
- **Comprobar celda a celda, no solo la media.** Las tablas grandes y los
  apéndices por instancia se verifican entero, valor a valor.
- **`PEND` en vez de `FALLO` si el dato está a medias.** Una campaña a
  medio regenerar no es un paper equivocado. Guardar con un conteo y saltar
  el bloque.
- **Colapsar espacios antes de buscar literales** en el fuente: una frase
  partida por el salto de línea no debe fallar espuriamente.
- **Reanclar, nunca debilitar.** Al reescribir prosa, las comprobaciones
  que buscan frases literales fallan. La reacción correcta es moverlas a la
  frase nueva; relajarlas para que pasen convierte el verificador en
  decorado. Si una pierde su ancla dos veces, anclarla a algo estructural
  (una fila de tabla, una etiqueta) en vez de a la redacción.
- **Guardar fichero a fichero, no por carpeta.** Un bloque que comprueba
  que existe un directorio y luego abre dos ficheros de dentro revienta en
  cualquier copia parcial. Cada apertura con su guarda.

Qué caza en la práctica: una celda contaminada por una tirada mala, un test
estadístico citado que nunca se calculó, una afirmación sobre la forma de
una curva que los datos desmienten, redondeos truncados, un rango
inventado, y convenciones que difieren entre el texto y el código.

## 2. Definir antes de usar

Auditoría manual, repetida por sección. Buscar cada término técnico y cada
símbolo, y comprobar que nace antes de gastarse.

Lo que sobrevive a muchas relecturas: siglas nunca expandidas; el nombre de
la arquitectura en las contribuciones y en las tablas pero jamás en el
cuerpo; una fórmula cuyos subíndices no están ligados a nada; una letra
griega que aparece sin presentarse; y la jerga del subcampo, que al autor
le resulta invisible.

- **Declarar la convención de componentes donde se define el símbolo.** Un
  artículo que declara un intervalo como `x = [x^L, x^U]` y luego gasta
  `y^L`, `y^U`, `z^U` durante veinte páginas está usando una convención que
  nunca extendió a esos símbolos.
- Orden que funciona en una sección de método: **(1)** el marco conceptual
  completo con sus términos, **(2)** por qué la arquitectura necesita cada
  pieza, **(3)** la instanciación en el problema, **(4)** el recorrido de
  la figura caja por caja, **(5)** el formalismo.
- Una figura se recorre donde se menciona y **se declara donde se
  menciona**: colocada en la subsección equivocada, flota dos páginas.

## 3. Trazar la procedencia de cada número ajeno

Antes de citar una cifra propia publicada en otro artículo, localizar el
fichero que la respalda. Es corriente que en un repositorio convivan varios
valores del mismo experimento y solo uno sea el publicado.

Procedimiento: buscar la cifra en el fuente del otro trabajo → localizar el
script que generó esa tabla → identificar el fichero de datos y la clave
exacta → recomputar y comprobar que da el valor publicado con todos sus
decimales.

**Corolario, el más caro de aprender: solo se puede construir sobre lo
publicado.** Si un resultado propio no se reproduce con la versión
publicada del método —otra variante, otro fichero de parámetros, una
configuración que nunca salió— no se documenta la discrepancia: se repite
el experimento con la versión publicada.

## 4. Comparaciones: declarar el eje de equidad

Ningún resultado comparativo es interpretable sin decir qué se iguala. El
error típico es enfrentar una pasada de un método barato contra cientos de
muestras de uno caro; al emparejar presupuestos, las ventajas se desploman.

- Si los métodos tienen presupuestos ajustables, **una figura por
  presupuesto emparejado**, no una comparación agregada.
- Nombrar en los ejes quién es quién, no "método A".
- Declarar qué **no** está emparejado (típicamente, el coste de
  entrenamiento) y decir si se comparan artefactos publicados o un estudio
  controlado.
- **Artefacto no es familia.** Un test con la instancia como unidad mide
  variación entre instancias, no entre modelos entrenados. Si cada lado es
  *un* artefacto seleccionado, la conclusión es sobre ese par y no sobre
  los paradigmas, por pequeño que salga el *p*. O se evalúan varios
  artefactos por familia bajo un protocolo de selección declarado, o la
  afirmación se acota al par **en el resumen, en los *highlights* y en las
  conclusiones**, que es donde se lee sin los matices del cuerpo.

## 5. Honestidad en tablas y figuras

- **Marcar las columnas contaminadas.** Si una columna contiene las
  instancias de entrenamiento o de validación, hay que decirlo con una
  daga, una nota al pie y sombreado en la figura. El verificador no puede
  cazarlo: todas las cifras son correctas.
- **Los diagramas de caja con n pequeña mienten.** Con una decena de
  observaciones, una caja colapsa a una línea y ocultar los atípicos
  esconde justo los extremos que cuentan la historia. Con n≲20, puntos y
  mediana.
- **Comprobar que el sombreado marca lo que dice la leyenda.** Es fácil que
  una región rellenada señale exactamente lo contrario de lo que la
  etiqueta afirma.
- **Retirar figuras que otra subsume.**
- **Dibujar cada figura a su tamaño final.** Si se incluye a
  `width=0.62\linewidth`, se dibuja con ese ancho en pulgadas: escala 1.0,
  y el cuerpo de letra del código es el que se ve en página. Estrechar el
  ancho natural manteniendo `\linewidth` **agranda** las fuentes, que suele
  ser lo contrario de lo que se busca.
- **Un sistema tipográfico único**: un cuerpo para ejes y rótulos, otro
  menor para texto secundario, iguales en todas las figuras.
- **Los símbolos de la figura son los del paper.** Etiquetar entidades con
  una notación que el artículo no define es introducir símbolos nuevos en
  el peor sitio posible.

## 6. Resultados negativos: el molde de "delimitación"

Un hallazgo negativo se publica cuando se le pone frontera. Molde probado:
*qué aporta y qué no aporta X, en dos mitades*. La forma es "X no aporta
nada bajo el objetivo A, y estas dos ablaciones lo miden; su valor aparece
bajo el objetivo B, que el problema simplificado no tiene".

Corolario operativo: **si un resultado sale inerte, comprobar primero qué
optimiza de verdad la función objetivo**. Una entrada puede ser inerte
porque el objetivo es función de otras que ya están presentes: la
redundancia es estructural, no empírica, y decirlo así es más fuerte que
reportar un contraste sin efecto.

## 7. Estructura y retórica

Arquitectura que funciona:

```
1 Introducción      hecho del mundo real → hueco → preguntas → contribuciones → mapa
2 Trabajo relacionado   con una subsección por familia de métodos comparados
3 Problema          notación y métrica, con la elección de criterio acotada
4 Método            conceptos → figura recorrida → formalismo
5 Metodología       instancias y partición, configuración, baselines
6 Resultados        qué consigue
7 Análisis          qué lo explica + limitaciones enumeradas al cierre
8 Conclusiones      respuestas a las preguntas de §1 + trabajo futuro con contenido
```

- **Separar Resultados de Análisis.** Muchas subsecciones peleándose en una
  sola sección se ordenan solas al dividirlas en *qué pasó* / *qué lo
  explica*.
- **Preguntas explícitas en la introducción** y respuestas literales en las
  conclusiones.
- **Un movimiento de acotación**: declarar qué pregunta *no* se reabre y
  citar el estudio que la fijó. Desactiva una objeción antes de que llegue.
- **Limitaciones enumeradas** al final del análisis, no enterradas en las
  conclusiones.
- **Trabajo futuro con sustancia técnica**: la pregunta que un experimento
  concreto deja abierta, no "exploraremos otras arquitecturas".
- **Las aportaciones, delante.** El resultado más fuerte y menos
  condicional va en las primeras frases del resumen y abre las
  conclusiones. Abrir con la concesión ("ninguno de los dos domina") antes
  de haber enunciado nada regala la lectura.

Si hay un artículo companion, **copiar su arquitectura y no su prosa**: la
organización no es plagio, el texto sí. Redactar contra el original abierto
para divergir a conciencia.

## 8. Disciplina de redacción

- **El artículo es una fotografía de la versión final, no el diario de las
  correcciones.** No se narra lo que se arregló, ni lo que se descubrió
  tarde, ni que una revisión obligó a rehacer algo: se describe el sistema
  tal como quedó. La excepción es cuando el hallazgo *es* un resultado —un
  defecto del propio diseño que el estudio mide—, y entonces se cuenta como
  resultado, no como confesión.
- **La leyenda es breve; la explicación va donde se referencia la figura.**
  Una leyenda que enseña a leer el dibujo obliga a leerla dos veces. En la
  leyenda, qué es; en el párrafo que la llama, cómo se lee y qué dice.
- **Medir la densidad, no estimarla.** Contar palabras de prosa por
  sección, descontando tablas y figuras, y mirar las que pasen de unas
  seiscientas sin una sola ilustración. Una lista de viñetas donde cada
  elemento lleva su fórmula y su escala es una tabla mal puesta:
  convertirla ahorra cientos de palabras y se lee mejor.
- **Registro académico**: sin coloquialismos, sin meta-narración ("en esta
  sección vamos a..."), sin negrita en la prosa, y abriendo cada párrafo
  por el hecho y no por lo que el párrafo se propone hacer.

## 9. Sobreafirmación: decir lo que el dato sostiene

Lo que más veces marcan los revisores, y casi siempre con razón.

- **«No cambia» no es «no se detecta cambio».** Un experimento que no
  encuentra efecto bajo un criterio fijo no demuestra que el mecanismo esté
  intacto: no lo compara. La redacción honesta es la del efecto medido, no
  la del mecanismo supuesto.
- **Suelo del *p* exacto.** Con pocas observaciones pareadas del mismo
  signo, el mínimo alcanzable a dos colas es un valor fijo (con seis,
  0,03125). Verlo repetido en varios contrastes no es una racha de
  significación: es el suelo. Declararlo, y decir cuántos contrastes
  relacionados se examinaron sin corrección de multiplicidad.
- **Adverbios que salvan un párrafo**: "principalmente", "no se detectó un
  cambio sistemático". Cuestan una palabra y quitan una objeción mayor.
- Al suavizar una afirmación, **buscarla en todo el manuscrito**. Se
  suaviza el pasaje técnico y quedan en pie la lista de contribuciones, el
  resumen y las conclusiones diciendo la versión fuerte.

## 10. Elegir revista y conseguir sus normas

### Qué decide la elección

El factor de impacto casi nunca decide, sobre todo si las candidatas están
en el mismo cuartil y categoría. Lo que decide, en orden:

1. **El ámbito declarado.** Una revista cuyo *aims and scope* nombra una
   familia de métodos rechazará por ámbito un trabajo de otra familia, por
   bueno que sea, antes de mandarlo a revisión. Leer esa sección, no la
   reputación.
2. **Si la revista tolera el posicionamiento del artículo.** Un trabajo que
   no gana a lo mejor que existe y vende otra cosa (velocidad,
   generalización, interpretabilidad) tiene que defender ese marco en una
   revista del área clásica, y no tiene que defenderlo en una del área
   metodológica. **Este criterio pesa más que el cuartil.**
3. **La categoría del índice que el autor necesita** para su evaluación.
   Comprobarlo, no suponerlo.
4. **Concentración de envíos.** Con otros trabajos ya en revisión en la
   misma revista, repartir reduce el riesgo de que un cuello de botella
   editorial frene varios a la vez.
5. **El coste de los conflictos.** Excluir coautores recientes y el propio
   grupo es obligado; en un campo pequeño eso deja el artículo en manos de
   revisores de otro subcampo, y conviene anticipar qué secciones tendrán
   que defenderse solas.

Los agregadores de métricas discrepan entre sí; sirven para decidir, pero
para un CV o un informe solo vale el índice oficial.

### Conseguir la guía para autores

- **Springer**: `https://link.springer.com/journal/<id>/submission-guidelines`
  suele dejarse leer. Si el usuario la guarda como HTML, extraer el texto
  plano y buscar por palabras clave.
- **Elsevier**: la guía en ScienceDirect devuelve **403** a la descarga
  automática. Pedir al usuario que la guarde; si la guarda como *Imprimir
  a PDF*, no tendrá capa de texto y hay que leerla como imágenes.
- Extraer siempre lo **verificable y accionable**: límite de palabras del
  resumen, número de palabras clave, estilo de citas, secciones
  obligatorias (sin ellas devuelven el envío), límite de páginas, política
  de preprints, tipo de revisión (anónima simple o doble: decide si un
  preprint compromete el anonimato) y declaración de IA generativa.

### Descargar la plantilla LaTeX

- Las URL de descarga de las plantillas cambian; la estable es la página de
  soporte LaTeX de la editorial, de donde se extrae el enlace al zip.
- Muchas clases vienen con cualquier distribución TeX y no hay que
  descargar nada.
- Copiar al directorio del paper la clase y los `.bst` que use, para que
  compile en cualquier máquina sin depender del gestor de paquetes.
- **Si falta un paquete que la clase exige** y el gestor no lo conoce,
  bajarlo de CTAN y generarlo con docstrip:

```bash
curl -o paquete.zip https://mirrors.ctan.org/macros/latex/contrib/paquete.zip
# descomprimir y, en el directorio del .ins:
pdftex -interaction=nonstopmode paquete.ins    # genera los .sty
```

Al convertir a una plantilla nueva, comprobar lo que la clase **no** hace:
si carga o no `fontenc`, si compone el ORCID en la portada, y si trae su
propio `natbib` e `hyperref`, en cuyo caso las cargas manuales sobran.

## 11. Compilación y conformidad

- **Cuatro pasadas de LaTeX, no tres.** Cuando la paginación cambia, tres
  no bastan y el PDF puede salir **sin bibliografía**, con todas las citas
  en interrogante y sin un solo error en pantalla.
- **Comprobar las fuentes del PDF** con `pdffonts`. Un solo Type 3 y
  producción lo rechaza. Causas habituales: `fontenc` T1 sin una fuente
  vectorial que lo respalde, y matplotlib, que por defecto incrusta Type 3
  (`pdf.fonttype = 42` lo arregla).
- **Las tablas centradas se desbordan en silencio**, sin aviso de
  `Overfull`. Medir con una caja de sonda:

```latex
\newsavebox{\probebox}\begin{lrbox}{\probebox} ...tabular... \end{lrbox}
\typeout{ancho=\the\wd\probebox\space linewidth=\the\linewidth}\usebox{\probebox}
```

- **Medir antes de elegir una opción de clase.** Las opciones de revisión
  con interlineado doble pueden inflar un manuscrito por encima del límite
  de páginas de la revista. Compilar las dos y contar.
- Comprobar en cada compilación: errores, `Overfull`, páginas, citas sin
  resolver y palabras del resumen. `chk_compila.py`, junto a este fichero,
  hace ese resumen.

## 12. Higiene de experimentos que alimentan el paper

- **Guardar el resultado crudo, no el agregado.** Un barrido que guarda
  solo el mejor de N muestras obliga a repetirlo entero el día que haga
  falta la curva.
- **Fichero de resultados largo y reanudable**: una fila por evento, saltar
  lo ya hecho al arrancar, volcar a disco por fila. Un proceso muerto no
  debe costar la campaña.
- **Los selectores por variable de entorno con defecto silencioso queman
  días**: entrenan el modelo equivocado sin un solo aviso. Los lanzadores
  deben **abortar** si la configuración no es la esperada.
- **Una figura no puede tumbar una campaña**: envolver la visualización en
  `try/except`.
- **Los heredocs de shell destrozan las contrabarras.** Un script pegado en
  un heredoc convierte `\ref` en otra cosa y corrompe el fuente en
  silencio. Escribir el script a fichero y ejecutarlo, o construir las
  contrabarras con `chr(92)`.
- **En Windows, lanzar con `.bat` y redirección de `cmd`**, no con tuberías
  de PowerShell: un reinicio del proceso padre congela al hijo escribiendo
  en una tubería muerta, y truncar la salida mata el proceso de origen.

## 13. Revisión ciega simulada antes de enviar

Pasar el manuscrito **y el código** a un modelo distinto con el papel de
revisor de la revista de destino, en rondas sucesivas. Es lo que más
levanta el nivel del envío, y los hallazgos más profundos salen de ahí.

Dos reglas que cuestan horas aprender:

- **La copia que se le entrega debe ser idéntica al repositorio, fichero a
  fichero.** Si se refrescó parcialmente, el revisor audita código que ya
  no existe y devuelve problemas mayores que son fantasmas. Comprobarlo con
  un `diff` de todo el árbol de fuentes antes de lanzar, y correr el
  verificador dentro de esa copia.
- **Verificar cada hallazgo antes de tocar nada.** Alrededor de la mitad no
  son ciertos. Clasificar en tres montones: real, falso, y *culpa mía por
  cómo se lo he entregado*. El tercero es el más incómodo y el más
  frecuente.

Qué preguntarle además del guion habitual: si la contribución basta para
esa revista *dado* el resultado que sea; si el resumen, los *highlights* y
las conclusiones enuncian la aportación sin exagerarla ni enterrarla; y si
el ejemplo dibujado en las figuras es lo que el código calcula.

## 14. El depósito publicado no es el repositorio

El paquete que cita el paper se prueba **como lo probaría un extraño**, no
desde el árbol de trabajo donde todo resuelve por accidente.

- **Las rutas por defecto de los scripts.** Si el depósito reorganiza las
  carpetas, los scripts que traen rutas fijas dejan de resolver: funcionan
  en el repositorio y no en el paquete.
- **Las dependencias que nadie declara.** Reconstruir el fichero de
  requisitos desde los `import` reales, no de memoria; falta siempre alguna
  que el entorno de desarrollo tenía por otro motivo.
- **Las notas internas se cuelan.** Empaquetar una carpeta entera mete en
  el zip guías de trabajo que no deben publicarse. Los ficheros de una
  versión publicada no se pueden editar: sale caro.
- Un comprobador que recorra las rutas de datos que el verificador consulta
  y diga si el paquete las cubre todas paga su coste el primer día.

## 15. Del rechazo en escritorio al formulario de envío

- **Un desk-reject no suele ser un veredicto sobre el contenido**, sino
  sobre el encaje. Reencuadrar cuesta menos de lo que parece si la
  arquitectura ya está: cambio de clase, separación de identidad y ajuste
  del resumen a las condiciones de la revista nueva.
- **Doble anonimato**: marcar los bloques con identidad en el fuente con
  comentarios delimitadores y generar la copia anónima con un script que
  los elimine y **aborte** si queda algún rastro. A mano se olvida uno.
- **El formulario manda sobre la guía.** Al llegar a la pantalla de subida
  aparecen requisitos que la guía no dice: si un envío en LaTeX sube fuente
  o PDF, si los conflictos se declaran con un fichero o con una casilla, si
  las figuras van aparte, y si la carta de presentación es obligatoria.
  Leer el formulario real antes de dar por cerrado el plan de ficheros.
- **La carta de presentación** dice qué aporta el trabajo separando la
  contribución metodológica de la aplicación, confirma originalidad y no
  envío simultáneo, y **declara cualquier trabajo relacionado en revisión
  en otra revista** con su DOI de preprint. Esa transparencia es mejor
  darla que esperar a que la pregunten.
- Mantener un **checklist del envío** en el repositorio, con los ficheros a
  subir, los campos del formulario ya redactados para pegar y las
  decisiones que solo el autor puede tomar. Revisarlo contra el formulario
  real, porque envejece.

## 16. Lo que NO está automatizado

Honestidad sobre el estado real:

- **La lectura completa del PDF.** Ninguna comprobación sustituye a leerlo
  entero una vez.
- **Detectar qué falta.** El verificador comprueba lo que está escrito, no
  lo que debería estar.
- **La decisión de encuadre.** Qué hallazgo es el titular y cuál es una
  nota al pie es criterio, no cálculo.
- **La equidad de una comparación.** El emparejamiento de presupuestos se
  detecta mirando una figura, no recomputando.
- **Los identificadores externos** (DOI, ORCID) y las decisiones de
  autoría, orden de firmas y CRediT.
- **Las declaraciones que firma el autor**: originalidad, conflictos, uso
  de IA generativa. Se redactan, no se aprueban en su nombre.

Cuando algo de esta lista aparezca, **decirlo en voz alta** en vez de
simularlo. Un mensaje de commit puede describir un cambio que nunca llegó
al fichero porque el comando que lo aplicaba fue bloqueado y nadie lo
comprobó.
