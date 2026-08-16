# Checklist de envío — Journal of Intelligent Manufacturing

(Guía para el formulario; este fichero no se sube.)

## Antes de subir NADA — bloqueantes

- [ ] El barrido de lambda a diez semillas cerrado y §7.3 reescrita
      (los PDF de esta carpeta se regeneran después:
      `python scripts/prepara_envio.py`).
- [ ] DOI del depósito Zenodo propio en la declaración de datos
      (sustituye el \todo en rojo de la última página).
- [ ] Decisión sobre la declaración de LLM: documentar en Methods o
      acogerse a la exención de "AI assisted copy editing" (nota
      comentada junto a las Declarations). La guía no da término medio.
- [ ] Lectura completa del PDF por el autor.

## Qué se sube

- `manuscript.pdf` — el manuscrito (38 pp., una columna, sn-jnl).
- `supplementary_material.pdf` — como Supplementary Information.
- `fuente/` — tex + bib + bbl + clase + bst + sty + figuras; el
  sistema los pide para manuscritos LaTeX.

## Qué teclear en el formulario

- **Título**: Deep Reinforcement Learning for the Interval Job Shop
  Scheduling Problem: A Comparison with Genetic Programming
  Hyper-Heuristics across Inference Budgets
- **Abstract**: copiar del PDF (218 palabras; el sistema lo pide aparte).
- **Keywords (6)**: job shop scheduling; interval uncertainty; deep
  reinforcement learning; neural combinatorial optimization; genetic
  programming hyper-heuristics; size invariance
- **Autor**: Hernán Díaz Rodríguez, Department of Computing,
  University of Oviedo, Gijón, Spain — diazhernan@uniovi.es + ORCID.
- **Funding**: MCIN/AEI/10.13039/501100011033, grant
  PID2022-141746OB-I00 (nombre del organismo completo, lo pide la guía).
- **Competing interests**: sin conflictos (ya en el PDF).
- **Data availability**: instancias en doi:10.5281/zenodo.21716972;
  checkpoints, registros y código en el depósito propio (DOI al subir)
  y en https://github.com/HernanDiaz/ijsp-drl.

## Verificaciones ya hechas (no repetir)

- 776 comprobaciones numéricas contra datos primarios, 0 fallos.
- Formato contra la guía: abstract 150-250, 6 keywords, APA autor-año,
  DOIs como enlace completo, Statements and Declarations completas,
  tres niveles de encabezado, sin notas al pie.
- Sin fuentes Type 3, sin desbordes de caja, citas resueltas.
- Referencias: 49 entradas, todas citadas, DOIs resueltos uno a uno.
