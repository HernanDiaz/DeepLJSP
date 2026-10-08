# Envío a Applied Soft Computing: checklist

Generar todo con:

```
python paper_asoc/make_graphical_abstract.py
python paper_asoc/build_envio.py
python paper_asoc/verify_numbers.py
```

## Ficheros que se suben (paper_asoc/envio/)

| Tipo en Editorial Manager | Fichero |
|---|---|
| Manuscript (fuente LaTeX) | `manuscript_source.zip` (main.tex, main.bbl, refs.bib, supplementary.aux, 9 figuras) |
| Manuscript (PDF, si lo pide) | `manuscript.pdf` |
| Highlights | `highlights.txt` (editable, "highlights" en el nombre, 5 puntos ≤ 85 caracteres) |
| Graphical Abstract | `graphical_abstract.tif` (2656 × 1062 px; hay un `.pdf` vectorial si lo prefiere) |
| Supplementary Material | `supplementary.pdf` |
| Cover Letter | `cover_letter.pdf` |

No hay portada aparte: ASOC revisa con anonimato simple y el manuscrito
lleva autor, afiliación, CRediT, agradecimientos y competing interests.

## Campos del formulario

- **Article type:** Research paper / technical paper (41 páginas; tope 50).
- **Keywords (6):** interval job shop scheduling; genetic programming;
  hyper-heuristics; dispatching rules; scheduling under uncertainty; robustness.
- **Funding:** Spanish Ministry of Science, Innovation and Universities
  (MCIN/AEI/10.13039/501100011033), grant PID2022-141746OB-I00.
- **Data statement:** datos y código en Zenodo,
  doi:10.5281/zenodo.21716972 (versión 2.0: doi:10.5281/zenodo.23156759).
- **Declaration of interests:** sin conflictos (rellenar la herramienta).
- **Generative AI:** declarado en el manuscrito, antes de las referencias.
- **Preprint:** ya existe en SSRN (doi:10.2139/ssrn.7214286). **No aceptar**
  el preprint de SSRN que ofrece el formulario: sería un duplicado.

## Decisiones que solo puede tomar el autor

- Open access o suscripción.
- Revisores sugeridos u opuestos, si el formulario los pide.
- Si el formulario pregunta por envíos anteriores del mismo trabajo:
  SWEVO-D-26-02115 (rechazado tras revisión, 2026-09-21) y
  CAIE-D-26-07701 (rechazado sin revisión, 2026-10-08).
- Si se declara en la carta el artículo de DRL en revisión en EAAI. La carta
  de C&IE lo dejó fuera a propósito, y esta también.
- Firmar la carta y comprobar la fecha.
