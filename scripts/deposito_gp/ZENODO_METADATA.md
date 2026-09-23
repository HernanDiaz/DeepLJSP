# Metadatos para la versión 2.0 en Zenodo

(Guía para rellenar el formulario. **No forma parte del depósito**: no va
dentro del zip ni se sube como fichero suelto.)

## Cómo subirla

El registro 1.0 está publicado (31 de julio de 2026). La 2.0 se sube como
**nueva versión del mismo registro**, no como registro nuevo, para que el
DOI de concepto que cita el artículo siga valiendo:

- DOI de concepto (el que cita el artículo, apunta siempre a la última
  versión): `10.5281/zenodo.21716972`
- DOI de la versión 1.0: `10.5281/zenodo.21716973`

Pasos:

1. Entrar en el registro https://zenodo.org/records/21716973 con tu cuenta.
2. Pulsar **New version**. Zenodo crea un borrador con los metadatos de la
   1.0 y sin ficheros.
3. Borrar del borrador los ficheros heredados si aparecen, y subir los
   tres de esta carpeta: `ijsp_gp_dataset.zip`, `README.md` y
   `LICENSE-DATA`.
4. Cambiar los campos de abajo (versión, fecha, descripción). El resto
   se hereda de la 1.0.
5. Publicar. Una versión publicada no se puede editar: revisar antes.

El artículo no hay que tocarlo: cita el DOI de concepto, que pasará a
resolver a la 2.0.

## Campos que cambian

**Version**: `2.0`

**Publication date**: el día que se publique.

**Title** (igual que la 1.0):
Genetic Programming Dispatching Rules for the Interval Job Shop:
Instances, Evolved Rules, Results and Code

**Description**:

Companion data and code for the article "Genetic Programming
Hyper-Heuristics for the Job Shop Scheduling Problem with Interval
Durations". The deposit contains the 70 interval Taillard instances, their
right-skewed asymmetric versions, and the 12 classical interval instances
used as benchmarks; the 430 dispatching rules evolved for the article's
experimental arms (main arm, terminal ablation, robust objective, lambda
sweeps, crisp-midpoint control, five alternative training sets and four
arms on asymmetric intervals); the primary result files behind every table
and figure; and a self-contained Python package (ijsp_gp) implementing the
interval arithmetic, the semi-active decoder, the hand-crafted baselines,
the GP evolution, the Monte Carlo executional-robustness measure, a fast
simulator shared by all methods of the budget comparison, the genetic
algorithm of that comparison, and the generator of the asymmetric
instances. An equivalence test re-derives at least one deposited result
of every experiment from the code and data alone.

Version 2.0 adds the asymmetric instances, the 210 rules of the
training-set and asymmetric campaigns, the genetic algorithm and the fast
simulator, and the results of the experiments on training-set
sensitivity, asymmetric intervals, alternative realization laws, interval
conventions and decoders, the worked example, quality against
computational budget, and the tail risk of the executed makespan.

**Keywords** (se heredan; añadir `computational budget` si se quiere):
interval job shop scheduling; genetic programming; hyper-heuristics;
dispatching rules; scheduling under uncertainty; robustness; benchmark
instances

**Licencias**: se heredan (código MIT dentro del zip, datos CC BY 4.0).

**Funding**: se hereda (MCIN/AEI/10.13039/501100011033,
PID2022-141746OB-I00).

**Related identifiers**: cuando el artículo tenga DOI, añadir
"is supplement to" → DOI del artículo.

## Si cambia el título del artículo

El README y la descripción citan el título sin el subtítulo de SWEVO. Si
el título definitivo cambia, actualizar las dos cosas antes de publicar:
`scripts/deposito_gp/README.md` y esta hoja, y volver a correr
`python scripts/prepara_zenodo_gp.py`.
