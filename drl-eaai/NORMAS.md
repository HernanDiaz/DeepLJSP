# EAAI — normas extraídas de la guía para autores

Fuente: `guia_autores_eaai.pdf` (Guide for authors de ScienceDirect,
guardada por el autor el 2026-04-13; revisar en la web si cambia antes
del envío). Revista de IFAC. Revisión: **doblemente anónima**, mínimo
dos revisores.

## Condiciones de desk-reject (verificadas el 2026-08-26)

1. Nada de metaheurísticas nuevas basadas en metáforas — no aplica.
2. El abstract debe separar con claridad la contribución en IA y la
   aplicación de ingeniería — CUMPLE, revisar redacción al convertir.
3. Prohibidas siglas sin definir en título y abstract — CUMPLE
   (título sin siglas; abstract solo IJSP, definida).
4. Formato a una columna — CUMPLE con elsarticle.

Límites duros adicionales: **50 páginas máximo** por envío (el PDF de
JIM tiene 39; VIGILAR al convertir, elsarticle con interlineado de
revisión puede inflar), fichero principal ≤50 MB, envío total ≤100 MB.

## Doble anonimato (el cambio estructural respecto a JIM)

Dos ficheros separados:

- **Title page** (con identidad): título, autor, afiliación completa
  con dirección postal y email, corresponding author,
  agradecimientos, financiación (formato Elsevier: "Funding: This
  work was supported by MCIN/AEI/10.13039/501100011033 [grant number
  PID2022-141746OB-I00]"), y declaración de conflictos si no va en
  fichero aparte.
- **Manuscrito anonimizado**: sin nombres, sin afiliación, sin
  agradecimientos. Autocitas en tercera persona (ya lo están).

Puntos delicados a decidir en la conversión:
- La declaración de disponibilidad de datos cita el depósito Zenodo
  propio, cuyo registro lleva el nombre del autor. Opciones: dejarla
  (práctica tolerada; el benchmark compartido ya delata al grupo a un
  revisor decidido) o sustituir el DOI por "[reference anonymized for
  review]" en la versión anónima y restaurarlo en la revisión.
- La cita al companion GP (en revisión en ASOC): la guía pide marcar
  lo no publicado como "unpublished results" en la lista de
  referencias, y permite citar preprints centrales marcándolos como
  preprint con su DOI. Si el companion tuviera preprint, citar el
  preprint es la vía limpia.

## Estructura y ficheros del envío

- Manuscrito .tex editable (PDF no vale como fuente); figuras como
  ficheros separados, vectoriales EPS/PDF (las nuestras son PDF).
- Secciones numeradas 1, 1.1, 1.1.1; apéndices A, B con Eq. (A.1),
  Table A.1.
- Abstract ≤250 palabras (tenemos 224), sin referencias, sin siglas
  no definidas.
- Keywords: 1–6, en inglés, evitar "and"/"of" en lo posible.
- Highlights: opcionales pero recomendados — 3 a 5 puntos de ≤85
  caracteres cada uno, fichero aparte con "highlights" en el nombre.
- Graphical abstract: opcional (531×1328 px, legible a 5×13 cm). SIN
  IA generativa: Elsevier lo prohíbe para figuras/artwork.
- Hasta 6 códigos de clasificación Inspec (opcional).
- Unidades SI; tablas como texto editable, sin reglas verticales ni
  sombreado.

## Declaraciones obligatorias

- **CRediT**: obligatorio (autor único: todos los roles aplicables).
- **Competing interests**: obligatoria aunque sea "nothing to
  declare"; herramienta de declaración de Elsevier, se sube en Word.
- **Data statement**: obligatorio; la revista aplica la **Opción C**
  de datos: depositar en repositorio + citar y enlazar en el
  artículo — el depósito Zenodo v3 lo cumple tal cual.
- **IA generativa**: si se usaron herramientas de IA en la
  preparación, declaración OBLIGATORIA al primer envío, en sección
  nueva antes de las referencias, título "Declaration of generative
  AI and AI-assisted technologies in the manuscript preparation
  process", con la plantilla "During the preparation of this work the
  author(s) used [TOOL] in order to [REASON]. After using this
  tool/service, the author(s) reviewed and edited the content as
  needed and take(s) full responsibility for the content of the
  published article." (No aplica a correctores gramaticales básicos.)

## Referencias

- Estilo autor-año (Allan, 2020a; Allan and Jones, 2019); lista
  alfabética y cronológica; en elsarticle: `elsarticle-harv` +
  natbib authoryear. Formato flexible al envío mientras sea
  consistente; DOIs recomendados.
- Datasets: citar con `[dataset]` delante de la referencia (no
  aparece publicado); creador, título, repositorio, versión, año,
  DOI. Software: igual, con versión (formato FORCE11; ejemplo de la
  guía es justamente Zenodo).
- Preprints: marcar "preprint" o el nombre del servidor + DOI del
  preprint; si ya está publicado, citar la versión publicada.

## Proceso

- Preprints permitidos sin contar como publicación previa; ofrecen
  posteo gratuito en SSRN durante el propio envío (opcional, tras
  pasar el desk).
- Pre-proof online con DOI nada más aceptar; correcciones de pruebas
  en 2 días.
- Sugerencia de revisores: el checklist la menciona "según requiera
  la revista" — preparar 3–4 candidatos sin conflicto.
- Inglés americano o británico, no mezclados (el manuscrito está en
  americano).
