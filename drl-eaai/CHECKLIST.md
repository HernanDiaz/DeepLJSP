# Envío a EAAI — lista de control

Sistema: Editorial Manager de Elsevier (enlace "submit your paper" de
la guía). Revisión doblemente anónima. Regenerar esta carpeta tras
cada recompilación con `python scripts/prepara_envio_eaai.py`.

## Ficheros a subir

- [ ] `manuscript.tex` — manuscrito ANÓNIMO (fuente; el sistema
      compila su propio PDF). `manuscript.pdf` es la copia de control
      local (37 págs., límite 50; sin fuentes Type 3).
- [ ] `title_page.tex`/`.pdf` — el único fichero con identidad:
      autor, afiliación postal, email, funding, conflictos, CRediT.
- [ ] `highlights.tex`/`.pdf` — 5 puntos, ≤85 caracteres (fichero con
      "highlights" en el nombre, como pide la guía).
- [ ] Las 11 figuras PDF vectoriales (el sistema las pide aparte).
- [ ] `supplementary.pdf` — se publica tal cual; ya es anónimo.
- [ ] Declaración de conflictos: generar el .docx con la
      "declarations tool" de Elsevier durante el envío ("I have
      nothing to declare").

## Campos del formulario

- [ ] Abstract: 243 palabras (copiar del manuscrito).
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

- [ ] **Declaración de IA generativa**: el manuscrito la lleva
      antes de las referencias, acotada a redacción y edición según
      decisión del autor. REVISARLA Y APROBARLA — es su firma, no la
      del asistente.
- [ ] **DOI de Zenodo en el manuscrito anónimo**: se mantiene visible
      (práctica tolerada y exigida por la Opción C de datos). La
      alternativa ortodoxa sería "[anonymized for review]".
- [ ] **Cita del companion GP** (en revisión en ASOC): va como
      preprint de SSRN con DOI 10.2139/ssrn.7214286, que es lo que la
      guía admite. Revisar si al enviar ya está aceptado, para
      actualizarla.
- [ ] **Revisores sugeridos** (3–4, si el formulario los pide): elegir
      de la literatura citada, sin coautores ni Oviedo. Candidatos
      naturales por área: DRL para scheduling (autores de los métodos
      L2D/Corsini citados), hiperheurísticas GP para scheduling
      (grupo de Zagreb citado: Đurašević/Jakobović; o Mei/Zhang en
      Wellington), scheduling bajo incertidumbre intervalar (los
      grupos citados fuera de Oviedo). Comprobar conflictos antes.

## Pendiente antes de enviar

- [ ] **Zenodo v4**: `drl-eaai/zenodo_drl_v4.zip` (283 MiB, 3277
      ficheros, construido el 2026-09-01) SUBIR como versión nueva del
      depósito. Corrige dos fallos de reproducibilidad del v3: las
      treinta reglas GP viajan también en
      `records/benchmarks/reevo_fixedfit/`, que es donde el código las
      busca, y `requirements.txt` incluye pandas, sin el cual un
      entorno limpio no entrena. El DOI de concepto no cambia, así que
      el manuscrito sigue citando bien.
- [ ] **Lectura completa del manuscrito por el autor**, que ninguna
      comprobación automática sustituye.

## Notas técnicas

- Referencias: elsarticle-harv (autor-año). BibTeX avisa de "empty
  pages" en 9 entradas de congreso (NeurIPS/ICLR sin páginas):
  admisible al envío, el formato es flexible; revisar en producción.
- El límite de 50 páginas queda a 13 de margen con la opción
  `preprint` de elsarticle, que es la que usa el manuscrito
  (`verify_numbers.py` lo comprueba). La opción `review`, con su
  interlineado doble, se midió el 2026-08-31 y da 51 páginas, una por
  encima del límite; no se usa por eso, y la guía no la exige: lo que
  pide es una columna, que ambas cumplen.
- `sup:` las referencias cruzadas del suplementario a números
  literales del paper (Table 5, Eq. 5, Figure 1, Table 8) las vigila
  el verificador contra main.aux.
