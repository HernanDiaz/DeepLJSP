---
name: escribir-papers
description: Escribir, auditar y preparar para envío artículos de investigación con resultados computacionales (LaTeX + experimentos + datos). Usar siempre que se redacte o revise un paper, se integren resultados nuevos en el texto, se preparen tablas o figuras, se compruebe que las cifras del manuscrito cuadran con los datos, se adapte a las normas de una revista o se prepare el depósito de datos. También cuando el usuario pida "revisa esta sección", "mete estos resultados", "prepara el envío" o "comprueba los números", aunque no diga la palabra paper.
---

# Escribir papers con resultados computacionales

Destilado de dos artículos completos del repositorio (`paper_gp/`, GP
hiper-heurístico, enviado a Swarm and Evolutionary Computation; `paper/`,
política DRL, en preparación para Journal of Intelligent Manufacturing).
Las prácticas de abajo no son teoría: cada una nació de un fallo real que
llegó al manuscrito y sobrevivió a varias relecturas humanas.

Estado de automatización: **el verificador de números lo está; el resto es
disciplina asistida**. Lo que no se puede automatizar se marca como tal.

## 1. El verificador de números (la práctica central)

Cada cifra del texto se recomputa desde los datos primarios. Referencias:
`paper/verify_numbers.py` (201 comprobaciones) y `paper_gp/verify_numbers.py`
(84). Patrón: una comprobación por afirmación, `OK`/`FALLO`/`PEND`, y un
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

## 8. Normas de revista y compilación

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

## 9. Higiene de experimentos que alimentan el paper

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
- **En Windows, lanzar con `.bat` y redirección de `cmd`**, no con tuberías
  de PowerShell: un reinicio del proceso padre congela al hijo escribiendo
  en una tubería muerta, y `Select-Object -First N` mata el proceso de
  origen.

## 10. Lo que NO está automatizado

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
