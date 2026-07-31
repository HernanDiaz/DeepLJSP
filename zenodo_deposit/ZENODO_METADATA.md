# Metadatos para el formulario de Zenodo

(Este fichero es una guia para rellenar el registro; no forma parte del
deposito publicado. Borrar antes de subir o dejar fuera del zip.)

**Tipo de registro**: Dataset (con software)

**Titulo**:
Genetic Programming Dispatching Rules for the Interval Job Shop:
Instances, Evolved Rules, Results and Code

**Autor**: Díaz, Hernán — University of Oviedo (añadir ORCID en el formulario)

**Descripcion** (campo Description):
Companion data and code for the article "Genetic Programming
Hyper-Heuristics for the Job Shop Scheduling Problem with Interval
Durations: Robustness-Aware Interpretable Rules that Generalize Across
Instance Sizes". The deposit contains the 70 interval Taillard instances
and the 12 classical interval instances used as benchmarks; the 220
dispatching rules evolved for the article's experimental arms (main,
terminal ablation, robust objective, lambda sweeps and crisp-midpoint
control); the primary CSV result files behind every table and figure; and
a self-contained Python package (ijsp_gp) implementing the interval
arithmetic, the semi-active decoder, the hand-crafted baselines, the GP
evolution and the Monte Carlo executional-robustness measure. An
equivalence test re-derives the deposited results from the code and data
alone.

**Keywords**: interval job shop scheduling; genetic programming;
hyper-heuristics; dispatching rules; scheduling under uncertainty;
robustness; benchmark instances

**Licencias**: código MIT; datos CC BY 4.0 (elegir "mixta" o declarar en
la descripción; Zenodo permite una sola licencia por registro — si obliga
a elegir una, CC BY 4.0 y el LICENSE del código dentro del zip).

**Funding**: MCIN/AEI/10.13039/501100011033, grant PID2022-141746OB-I00

**Related identifiers**:
- "is supplement to" → DOI del artículo cuando exista (o dejar pendiente)

**Pasos**:
1. Crear el registro en borrador y subir el zip.
2. En el borrador, usar "Reserve DOI" para obtener el DOI SIN publicar.
3. Pasar el DOI reservado al manuscrito (el \todo de Data availability).
4. Publicar el registro al enviar el artículo.
