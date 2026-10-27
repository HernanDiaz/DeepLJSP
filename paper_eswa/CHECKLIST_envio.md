# Envío a Expert Systems with Applications: checklist

Artículo DRL frente a GP para el IJSP. Coautor: Jesús Gil Ruiz.
Rechazado sin revisión en EAAI (EAAI-26-28022, 2026-10-25); `paper/` y
`drl-eaai/` quedan como la versión de EAAI.

```
paper_eswa\compila.bat
venv\Scripts\python.exe -X utf8 paper_eswa\verify_numbers.py
venv\Scripts\python.exe -X utf8 paper_eswa\build_envio.py
```

## Por qué ESWA (comprobado el 2026-10-25, leyendo resúmenes)

- DRL para el JSSP evaluado solo en benchmarks (TA, DMU, LA...), sin caso
  industrial: 10.1016/j.eswa.2025.130249 (citado como Ou et al., 2026).
- DRL para el FJSP sobre Brandimarte/Hurink, comparado con reglas de
  prioridad: 10.1016/j.eswa.2023.123019 (Yuan et al., 2024).
- Tiempos de procesamiento en intervalo gris sin caso real:
  10.1016/j.eswa.2026.133484.

## Requisitos de la guía

Doble anonimato (title page aparte), resumen ≤ 250 palabras (236), 1–7
palabras clave (6), 3–5 highlights ≤ 85 caracteres (5, máx. 78), citas
APA autor-año, declaración de IA antes de las referencias, sin límite de
páginas (38) ni graphical abstract obligatorio.

## Ficheros que se suben (paper_eswa/envio/)

| Tipo | Fichero |
|---|---|
| Manuscript (anónimo) | `manuscript.pdf` (si pide fuente: `manuscript.tex` + figuras) |
| Title page | `title_page.pdf` |
| Highlights | `highlights.txt` |
| Supplementary material | `supplementary.pdf` |
| Cover letter | `cover_letter.pdf` |

## Campos del formulario

- Palabras clave: job shop scheduling; interval uncertainty; deep
  reinforcement learning; neural combinatorial optimization; genetic
  programming hyper-heuristics; size invariance. Si el formulario admite
  solo 5, quitar "size invariance".
- Financiación: State Agency of Research (AEI), PID2022-141746OB-I00.
- Datos: Zenodo, https://doi.org/10.5281/zenodo.21970431.
- Preprint SSRN del portal: decisión de los autores. Este artículo no
  tiene preprint todavía.
- Envíos anteriores, si lo pregunta: EAAI-26-28022 (rechazo sin revisión).

## Cambios respecto a la versión de EAAI

- Citas autor-año (`authoryear`); en EAAI salían numéricas.
- Fuera la frase final del resumen sobre la "engineering application",
  propia de EAAI.
- La selección de la regla GP ya no es asimétrica: la versión en revisión
  en ASOC la elige en validación (`paper_asoc/`). El verificador contrasta
  ahora contra `paper_asoc/main.tex`, no contra `paper_gp/` (SWEVO).
- Nota sobre tiempos: el estudio GP mide 20,6 ms por pasada con su
  simulador; la tabla de costes de este artículo mide en el entorno
  compartido.
- El barrido de λ del estudio GP se describe "hasta 4" (su 1,64 va de
  0,5 a 4).
- Dos citas de ESWA en el estado del arte.
- Subsección 7.5 "Practical implications" con la tabla 12 (qué método
  usar según el tiempo por instancia y el tamaño), una frase en el
  resumen y otra en las conclusiones que remiten a ella. Solo usa cifras
  que el artículo ya demuestra; el verificador lo comprueba cifra a cifra.

## Decisiones de los autores antes de enviar

- [ ] Acuerdo de Jesús Gil Ruiz con ESWA y con la carta.
- [ ] Transferencia de EAAI: si ESWA figura entre las revistas ofrecidas,
      aceptarla ahorra el formulario; si no, rechazarla y enviar directo.
- [ ] Preprint SSRN del artículo GP: es la versión de SWEVO (elige la
      regla sobre las 70). Este artículo describe ya la de ASOC (elige en
      validación) y la cita como "revised version under review".
      Valorar subir a SSRN la versión revisada para que coincidan.
- [ ] Revisar la declaración de IA y leer el PDF completo.
- [ ] Confirmar que ningún autor está en el consejo editorial de ESWA
      (casilla de conflictos).
