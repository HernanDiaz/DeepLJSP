# Envío a EAAI — lista de control

Sistema: Editorial Manager de Elsevier (enlace "submit your paper" de
la guía). Revisión doblemente anónima. Regenerar esta carpeta tras
cada recompilación con `python scripts/prepara_envio_eaai.py`.

## Ficheros a subir

- [ ] `manuscript.tex` — manuscrito ANÓNIMO (fuente; el sistema
      compila su propio PDF). `manuscript.pdf` es la copia de control
      local (49 págs., límite 50; sin fuentes Type 3).
- [ ] `title_page.tex`/`.pdf` — el único fichero con identidad:
      autor, afiliación postal, email, funding, conflictos, CRediT.
- [ ] `highlights.tex`/`.pdf` — 5 puntos, ≤85 caracteres (fichero con
      "highlights" en el nombre, como pide la guía).
- [ ] Las 9 figuras PDF vectoriales (el sistema las pide aparte).
- [ ] `supplementary.pdf` — se publica tal cual; ya es anónimo.
- [ ] Declaración de conflictos: generar el .docx con la
      "declarations tool" de Elsevier durante el envío ("I have
      nothing to declare").

## Campos del formulario

- [ ] Abstract: 224 palabras (copiar del manuscrito).
- [ ] Keywords (6): job shop scheduling; interval uncertainty; deep
      reinforcement learning; neural combinatorial optimization;
      genetic programming hyper-heuristics; size invariance.
- [ ] Códigos Inspec (hasta 6, opcionales): C1230L (learning), C1180
      (optimisation), E1550 (production/manufacturing scheduling).
- [ ] Data statement: instancias, código, registros y checkpoints en
      Zenodo, DOI de concepto 10.5281/zenodo.21970431 (el artículo lo
      cita; enlazar cuando el formulario lo pida).
- [ ] Funding: MCIN/AEI/10.13039/501100011033, PID2022-141746OB-I00.
- [ ] ORCID del autor de correspondencia (se introduce en el sistema).
- [ ] SSRN: el sistema ofrece publicar el preprint gratis al pasar el
      desk; decisión del autor (no afecta al proceso editorial).

## Decisiones del autor ANTES de enviar

- [ ] **Declaración de IA generativa**: el manuscrito lleva un
      borrador (sección antes de las referencias) que declara Claude
      (Anthropic) para redacción/edición y para el desarrollo y
      verificación de los scripts de análisis. REVISARLA Y APROBARLA
      (o recortarla) — es la firma del autor, no del asistente.
- [ ] **DOI de Zenodo en el manuscrito anónimo**: se mantiene visible
      (práctica tolerada y exigida por la Opción C de datos). La
      alternativa ortodoxa sería "[anonymized for review]".
- [ ] **Cita del companion GP** (en revisión en ASOC): hoy va como
      referencia normal con año; la guía pide marcar lo no publicado
      como "unpublished results" o citar un preprint con DOI si
      existiera. Ajustar según el estado en el momento del envío.
- [ ] **Revisores sugeridos** (3–4, si el formulario los pide): elegir
      de la literatura citada, sin coautores ni Oviedo. Candidatos
      naturales por área: DRL para scheduling (autores de los métodos
      L2D/Corsini citados), hiperheurísticas GP para scheduling
      (grupo de Zagreb citado: Đurašević/Jakobović; o Mei/Zhang en
      Wellington), scheduling bajo incertidumbre intervalar (los
      grupos citados fuera de Oviedo). Comprobar conflictos antes.

## Notas técnicas

- Referencias: elsarticle-harv (autor-año). BibTeX avisa de "empty
  pages" en 9 entradas de congreso (NeurIPS/ICLR sin páginas):
  admisible al envío, el formato es flexible; revisar en producción.
- El límite de 50 páginas queda a 1 página de margen: si la revisión
  de la curva de presupuesto añade texto, vigilar
  (`verify_numbers.py` lo comprueba).
- `sup:` las referencias cruzadas del suplementario a números
  literales del paper (Table 5, Eq. 5, Figure 1, Table 8) las vigila
  el verificador contra main.aux.
